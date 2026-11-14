"""Fases 3 e 4 — extração de questões e gabaritos, vínculo e validação por prova."""
from __future__ import annotations

import json
import logging
import re
from pathlib import Path

from .. import anos, config, db
from ..crawl import recalcular_ano
from ..texto import norm
from . import combinado, gabarito as gab, justificativa as just
from .pdf import Documento, ler, recorte
from .prova import Item, ResultadoProva

log = logging.getLogger(__name__)

TIPOS_PROVA = ("prova", "prova_com_gabarito_preliminar", "prova_com_gabarito_definitivo")
TIPOS_GAB = ("gabarito_preliminar", "gabarito_definitivo")
VERSAO_EXTRATOR = "4"


def _abs(p: str) -> Path:
    q = Path(p)
    return q if q.is_absolute() else config.ROOT / q


def _ja_feito(con, doc, refazer: bool) -> bool:
    if refazer:
        return False
    ck = con.execute("SELECT status, detalhe FROM checkpoint WHERE etapa='extract' AND chave=?",
                     (str(doc["id"]),)).fetchone()
    return bool(ck and ck["detalhe"] == f"{doc['sha256']}:{VERSAO_EXTRATOR}" and ck["status"] == "ok")


def _marca(con, doc, status="ok"):
    db.checkpoint(con, "extract", str(doc["id"]), status, f"{doc['sha256']}:{VERSAO_EXTRATOR}")


# ---------------------------------------------------------------- gabaritos
def _grava_grupo(con, doc_id, grupo, fase, respostas: dict[int, str], codigo=None, caderno=None, cargo=None,
                 data_edital=None, data_aplicacao=None, origem="pdf"):
    con.execute("DELETE FROM gabarito_bruto WHERE documento_id=? AND grupo=?", (doc_id, grupo))
    con.execute(
        "INSERT OR REPLACE INTO gabarito_grupo(documento_id, grupo, codigo_prova, caderno, cargo, fase, data_edital, "
        "data_aplicacao, n, origem) VALUES (?,?,?,?,?,?,?,?,?,?)",
        (doc_id, grupo, codigo, caderno, cargo, fase, data_edital, data_aplicacao, len(respostas), origem))
    con.executemany(
        "INSERT INTO gabarito_bruto(documento_id, grupo, codigo_prova, caderno, cargo, fase, numero, resposta) "
        "VALUES (?,?,?,?,?,?,?,?)",
        [(doc_id, grupo, codigo, caderno, cargo, fase, n, r) for n, r in sorted(respostas.items())])


def _processa_gabarito(con, doc) -> None:
    caminho = _abs(doc["arquivo_local"])
    grupos = gab.agrupa(gab.parse(caminho))
    con.execute("DELETE FROM gabarito_bruto WHERE documento_id=?", (doc["id"],))
    con.execute("DELETE FROM gabarito_grupo WHERE documento_id=?", (doc["id"],))
    if not grupos:
        db.pendencia(con, "gabarito", "nenhuma tabela de gabarito reconhecida no PDF", doc["concurso_id"], doc["id"])
        return
    fase_doc = "preliminar" if doc["tipo"] == "gabarito_preliminar" else "definitivo"
    for k, g in enumerate(grupos):
        fase = g.fase or fase_doc
        if g.fase and g.fase != fase_doc:
            db.pendencia(con, "gabarito", f"fase no PDF ({g.fase}) difere da classificação ({fase_doc})",
                         doc["concurso_id"], doc["id"])
        _grava_grupo(con, doc["id"], k, fase, g.respostas, g.codigo_prova or doc["codigo_prova"],
                     g.caderno or doc["caderno"], g.cargo or doc["cargo"], g.data_edital, g.data_aplicacao, g.origem)
        for a in g.avisos:
            db.pendencia(con, "gabarito", a, doc["concurso_id"], doc["id"])
    db.resolver_pendencias(con, "gabarito", doc["concurso_id"], doc["id"], "nenhuma tabela")


# ---------------------------------------------------------------- provas
def _cargos(texto: str | None) -> list[str]:
    if not texto:
        return []
    t = norm(texto)
    m = re.search(r"CARGOS?\s+(?:DE\s+)?(\d+)\s+(?:AO?|A)\s+(\d+)", t)
    if m:
        a, b = int(m.group(1)), int(m.group(2))
        if a <= b <= a + 200:
            return [f"CARGO {i}" for i in range(a, b + 1)]
    m = re.search(r"CARGOS?\s+((?:\d+\s*(?:,|E)\s*)*\d+)", t)
    if m:
        return [f"CARGO {int(x)}" for x in re.findall(r"\d+", m.group(1))]
    return [texto.strip()]


def _codigo_barras(doc: Documento) -> str | None:
    for t in doc.cabecalho[:6]:
        m = re.search(r"\|\|\s*([0-9A-Z_]+?)N\d{4,}\s*\|\|", t) or re.search(r"\b(\d{3}[0-9A-Z_]*_\d{2})N\d{5,}\b", t)
        if m:
            return m.group(1).upper()
    return None


def _segmentos(res: ResultadoProva):
    """(página, coluna, y_ini, y_fim, elemento) de cada item/bloco, para localizar imagens."""
    segs = []
    for el in list(res.itens) + list(res.blocos):
        linhas = list(getattr(el, "linhas", []))
        if isinstance(el, Item):
            for v in el.alternativas.values():
                linhas += v
        por = {}
        for l in linhas:
            k = (l.pagina, l.col)
            y0, y1 = por.get(k, (l.y0, l.y1))
            por[k] = (min(y0, l.y0), max(y1, l.y1))
        for (p, c), (y0, y1) in por.items():
            segs.append([p, c, y0, y1, el])
    segs.sort(key=lambda s: (s[0], s[1], s[2]))
    # estende o fim até o início do próximo elemento na mesma coluna (figuras ficam entre as linhas)
    for i, s in enumerate(segs):
        prox = next((t for t in segs[i + 1:] if t[0] == s[0] and t[1] == s[1]), None)
        s[3] = prox[2] - 1 if prox else 10_000
    return segs


def _imagens(doc: Documento, res: ResultadoProva, destino_dir: Path) -> dict[int, list[str]]:
    """Recorta imagens/tabelas/figuras e devolve {id(elemento): [caminhos]}."""
    out: dict[int, list[str]] = {}
    if not any(doc.graficos.values()):
        return out
    segs = _segmentos(res)
    W = doc.largura
    usados = set()
    for p, c, y0, y1, el in segs:
        xa, xb = (0, W) if c == -1 else ((0, W / 2 + 5) if c == 0 else (W / 2 - 5, W))
        for k, r in enumerate(doc.graficos.get(p, [])):
            cx, cy = (r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2
            if (p, k) in usados or not (xa <= cx <= xb and y0 - 3 <= cy <= y1 + 3):
                continue
            usados.add((p, k))
            nome = f"{type(el).__name__.lower()}_{getattr(el, 'numero', getattr(el, 'id', 0))}_p{p + 1}_{k}.png"
            arq = destino_dir / nome
            try:
                recorte(doc.caminho, p, r + (-2, -2, 2, 2), arq)
            except Exception as e:  # noqa: BLE001
                log.warning("recorte falhou %s: %s", arq, e)
                continue
            out.setdefault(id(el), []).append(str(arq.relative_to(config.ROOT)) if arq.is_relative_to(config.ROOT) else str(arq))
    return out


def _processa_prova(con, doc, concurso) -> None:
    caminho = _abs(doc["arquivo_local"])
    d = ler(caminho)
    esperados = None
    if doc["codigo_prova"]:
        rows = con.execute(
            "SELECT DISTINCT b.numero FROM gabarito_bruto b JOIN documento x ON x.id=b.documento_id "
            "WHERE x.concurso_id=? AND REPLACE(UPPER(b.codigo_prova),'_','')=?",
            (doc["concurso_id"], doc["codigo_prova"].replace("_", "").upper())).fetchall()
        esperados = {r[0] for r in rows} or None
    res, resp_emb, formato = combinado.segmentar_auto(d, doc["modalidade"], esperados)

    con.execute("DELETE FROM prova WHERE documento_id=?", (doc["id"],))
    codigo = doc["codigo_prova"] or _codigo_barras(d)
    ano_ap = anos.ano_aplicacao_texto("\n".join(d.cabecalho[:3]))
    m_ed = re.search(r"EDITAL:\s*((?:19|20)\d{2})", norm("\n".join(d.cabecalho[:3])))
    avisos = list(res.avisos)
    if d.paginas_ocr:
        avisos.append(f"OCR nas páginas {[p + 1 for p in d.paginas_ocr]}")
    cur = con.execute(
        "INSERT INTO prova(concurso_id, documento_id, codigo_prova, bloco, cargo, caderno, ano, tipo, avisos) "
        "VALUES (?,?,?,?,?,?,?,?,?)",
        (doc["concurso_id"], doc["id"], codigo, doc["bloco"], doc["cargo"], doc["caderno"], concurso["ano"],
         res.tipo, json.dumps(avisos, ensure_ascii=False) if avisos else None))
    prova_id = cur.lastrowid
    for cg in _cargos(doc["cargo"]):
        con.execute("INSERT OR IGNORE INTO prova_cargo(prova_id, cargo) VALUES (?,?)", (prova_id, cg))

    slug = concurso["slug"]
    imgs = _imagens(d, res, config.IMG_DIR / slug / str(doc["id"]))
    tb_ids: dict[int, int] = {}
    for b in res.blocos:
        cur = con.execute(
            "INSERT INTO texto_base(prova_id, rotulo, tipo, faixa_ini, faixa_fim, conteudo, imagens, pagina) "
            "VALUES (?,?,?,?,?,?,?,?)",
            (prova_id, (re.match(r"^(Texto\s+\S+)", b.texto) or [None])[0], b.tipo,
             b.faixa[0] if b.faixa else None, b.faixa[1] if b.faixa else None, b.texto,
             json.dumps(imgs.get(id(b))) if imgs.get(id(b)) else None, b.linhas[0].pagina + 1 if b.linhas else None))
        tb_ids[id(b)] = cur.lastrowid
    vistos = set()
    for it in res.itens:
        if (it.numero, it.tipo) in vistos:
            avisos.append(f"item {it.numero} repetido na segmentação; mantida a 1ª ocorrência")
            continue
        vistos.add((it.numero, it.tipo))
        ocr = any(l.origem == "ocr" for l in it.linhas)
        alts = it.alternativas_texto() if it.alternativas else None
        cur = con.execute(
            "INSERT INTO questao(prova_id, numero, tipo, texto_base_id, enunciado, alternativas_json, codigo_item, "
            "secao, imagens, origem_texto, pagina) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
            (prova_id, it.numero, it.tipo, tb_ids.get(id(it.bloco)) if it.bloco else None, it.enunciado,
             json.dumps(alts, ensure_ascii=False) if alts else None, getattr(it, "codigo_item", None), it.secao,
             json.dumps(imgs.get(id(it))) if imgs.get(id(it)) else None, "ocr" if ocr else "pdf", it.pagina + 1))
        qid = cur.lastrowid
        tb = it.bloco.texto if it.bloco else ""
        con.execute("INSERT INTO questao_fts(questao_id, enunciado, texto_base) VALUES (?,?,?)",
                    (qid, it.enunciado + (" " + " ".join(alts.values()) if alts else ""), tb))
        if it.justificativa:
            con.execute("INSERT OR IGNORE INTO gabarito(questao_id, justificativa, fonte_justificativa) VALUES (?,?,?)",
                        (qid, " ".join(l.texto for l in it.justificativa), doc["id"]))
    if resp_emb:
        fase = "definitivo" if doc["tipo"] == "prova_com_gabarito_definitivo" else "preliminar"
        _grava_grupo(con, doc["id"], 0, fase, resp_emb, codigo, doc["caderno"], doc["cargo"], origem="embutido")
    elif doc["tipo"] != "prova":
        db.pendencia(con, "gabarito", "prova com gabarito embutido, mas nenhuma resposta reconhecida",
                     doc["concurso_id"], doc["id"])
    if not res.itens:
        db.pendencia(con, "extracao", "nenhuma questão segmentada", doc["concurso_id"], doc["id"])
    con.execute("UPDATE prova SET n_itens=?, avisos=? WHERE id=?",
                (len(vistos), json.dumps(avisos, ensure_ascii=False) if avisos else None, prova_id))
    # evidências de ano no cabeçalho da prova
    if ano_ap and not concurso["ano_aplicacao"]:
        con.execute("UPDATE concurso SET ano_aplicacao=? WHERE id=? AND ano_aplicacao IS NULL", (ano_ap, doc["concurso_id"]))
    if m_ed:
        db.checkpoint(con, "ano_cabecalho_prova", concurso["slug"], "info", m_ed.group(1))


# ---------------------------------------------------------------- justificativas e padrões
def _processa_justificativa(con, doc) -> None:
    linhas = just.parse(ler(_abs(doc["arquivo_local"])))
    con.execute("DELETE FROM justificativa_bruta WHERE documento_id=?", (doc["id"],))
    con.executemany(
        "INSERT INTO justificativa_bruta(documento_id, secao, ordem, numero, preliminar, definitiva, situacao, texto) "
        "VALUES (?,?,?,?,?,?,?,?)",
        [(doc["id"], l.secao, k, l.numero, l.preliminar, l.definitiva, l.situacao, l.texto) for k, l in enumerate(linhas)])
    if not linhas:
        db.pendencia(con, "gabarito", "justificativas: nenhuma linha de tabela reconhecida", doc["concurso_id"], doc["id"])
    else:
        db.resolver_pendencias(con, "gabarito", doc["concurso_id"], doc["id"], "justificativas: nenhuma")


# ---------------------------------------------------------------- vínculo
def _resto_desc(t: str | None) -> str:
    t = norm(t)
    t = re.sub(r"^(GABARITOS?( OFICIAIS?)? (DEFINITIVOS?|PRELIMINAR(ES)?)|PROVAS? E GABARITOS? (DEFINITIVOS?|PRELIMINAR(ES)?)"
               r"|PROVAS? OBJETIVAS?( \(P\d\))?( E GABARITO PRELIMINAR COM JUSTIFICATIVAS)?|CADERNO DE PROVAS?)\s*[-|]?\s*", "", t)
    t = re.sub(r"\((ATUALIZADO|SEM EFEITO)\)|PROVA OBJETIVA", "", t)
    return re.sub(r"[^A-Z0-9]+", " ", t).strip()


def vincular(con, concurso_id: int) -> None:
    # pendências geradas pelo vínculo são recalculadas a cada execução
    con.execute("UPDATE pendencia SET resolvido_em=? WHERE resolvido_em IS NULL AND concurso_id=? AND etapa='gabarito' "
                "AND (motivo LIKE 'justificativas da seção%' OR motivo LIKE 'padrão de resposta%')", (db.agora(), concurso_id))
    provas = con.execute(
        "SELECT p.*, d.descricao, d.tipo AS doc_tipo, d.caderno AS doc_caderno FROM prova p "
        "JOIN documento d ON d.id=p.documento_id WHERE p.concurso_id=?", (concurso_id,)).fetchall()
    grupos = con.execute(
        "SELECT g.*, d.descricao, d.tipo AS doc_tipo, d.versao FROM gabarito_grupo g JOIN documento d ON d.id=g.documento_id "
        "WHERE d.concurso_id=?", (concurso_id,)).fetchall()
    respostas = {}
    for r in con.execute("SELECT b.documento_id, b.grupo, b.numero, b.resposta FROM gabarito_bruto b JOIN documento d "
                         "ON d.id=b.documento_id WHERE d.concurso_id=?", (concurso_id,)):
        respostas.setdefault((r[0], r[1]), {})[r[2]] = r[3]
    datas_ed, datas_ap = [], []
    for p in provas:
        qs = con.execute("SELECT id, numero, tipo FROM questao WHERE prova_id=?", (p["id"],)).fetchall()
        nums = {q["numero"] for q in qs if q["tipo"] != "DISC"}
        escolhido: dict[str, tuple] = {}
        for g in grupos:
            r = respostas.get((g["documento_id"], g["grupo"]), {})
            if not r:
                continue
            cod_ok = p["codigo_prova"] and g["codigo_prova"] and \
                p["codigo_prova"].replace("_", "").upper() == g["codigo_prova"].replace("_", "").upper()
            desc_ok = _resto_desc(p["descricao"]) and _resto_desc(p["descricao"]) == _resto_desc(g["descricao"])
            mesmo_doc = g["documento_id"] == p["documento_id"]
            cad_ok = not (p["caderno"] and g["caderno"]) or p["caderno"].upper() == g["caderno"].upper()
            inter = len(nums & set(r))
            cobertura = inter / max(1, len(nums | set(r)))
            if not cad_ok or not nums:
                continue
            if mesmo_doc or cod_ok or (desc_ok and cobertura >= 0.8):
                pontos = (3 if mesmo_doc else 2 if cod_ok else 1, cobertura, 0 if g["versao"] == "sem_efeito" else 1)
                f = g["fase"]
                if f not in escolhido or pontos > escolhido[f][0]:
                    escolhido[f] = (pontos, g, r)
        pre = escolhido.get("preliminar")
        de = escolhido.get("definitivo")
        if de and de[1]["data_aplicacao"]:
            con.execute("UPDATE prova SET data_aplicacao=? WHERE id=?", (de[1]["data_aplicacao"], p["id"]))
        for x in (pre, de):
            if x:
                if x[1]["data_edital"]:
                    datas_ed.append(x[1]["data_edital"])
                if x[1]["data_aplicacao"]:
                    datas_ap.append(x[1]["data_aplicacao"])
        n_gab = 0
        for q in qs:
            if q["tipo"] == "DISC":
                con.execute("INSERT OR IGNORE INTO gabarito(questao_id) VALUES (?)", (q["id"],))
                continue
            rp = pre[2].get(q["numero"]) if pre else None
            rd = de[2].get(q["numero"]) if de else None
            if rp is None and rd is None:
                continue
            n_gab += 1
            anulada = int(rd == "X")
            alterada = int(bool(rp and rd and rd != "X" and rp != rd))
            con.execute(
                "INSERT INTO gabarito(questao_id, resposta_preliminar, resposta_definitiva, anulada, alterada, "
                "fonte_preliminar, fonte_definitiva) VALUES (?,?,?,?,?,?,?) "
                "ON CONFLICT(questao_id) DO UPDATE SET resposta_preliminar=excluded.resposta_preliminar, "
                "resposta_definitiva=excluded.resposta_definitiva, anulada=excluded.anulada, alterada=excluded.alterada, "
                "fonte_preliminar=excluded.fonte_preliminar, fonte_definitiva=excluded.fonte_definitiva",
                (q["id"], rp, rd, anulada, alterada, pre[1]["documento_id"] if pre else None,
                 de[1]["documento_id"] if de else None))
        n_gab_total = len(set((de or pre)[2])) if (de or pre) else 0
        con.execute("UPDATE prova SET n_gabarito=? WHERE id=?", (n_gab_total or None, p["id"]))
    _aplica_justificativas(con, concurso_id)
    _aplica_padroes(con, concurso_id)
    if datas_ed or datas_ap:
        con.execute("UPDATE concurso SET data_edital_pdf=COALESCE(?, data_edital_pdf), data_aplicacao=?, "
                    "ano_aplicacao=COALESCE(?, ano_aplicacao) WHERE id=?",
                    (min(datas_ed) if datas_ed else None, min(datas_ap) if datas_ap else None,
                     int(min(datas_ap)[:4]) if datas_ap else None, concurso_id))
    recalcular_ano(con, concurso_id)
    con.execute("UPDATE prova SET ano=(SELECT ano FROM concurso WHERE id=?) WHERE concurso_id=?", (concurso_id, concurso_id))


def _aplica_justificativas(con, concurso_id: int) -> None:
    linhas = con.execute("SELECT j.* FROM justificativa_bruta j JOIN documento d ON d.id=j.documento_id "
                         "WHERE d.concurso_id=? ORDER BY j.documento_id, j.ordem", (concurso_id,)).fetchall()
    if not linhas:
        return
    defin = {}
    for r in con.execute(
            "SELECT q.prova_id, q.numero, q.id, g.resposta_definitiva, g.resposta_preliminar FROM questao q "
            "JOIN prova p ON p.id=q.prova_id LEFT JOIN gabarito g ON g.questao_id=q.id "
            "WHERE p.concurso_id=? AND q.tipo<>'DISC'", (concurso_id,)):
        defin.setdefault(r[0], {})[r[1]] = (r[2], r[3], r[4])
    secoes: dict[tuple, list] = {}
    for l in linhas:
        secoes.setdefault((l["documento_id"], l["secao"]), []).append(l)
    descr = {r[0]: set(re.findall(r"[A-Z0-9]+", norm(f"{r[1] or ''} {r[2] or ''}"))) for r in con.execute(
        "SELECT p.id, d.descricao, p.cargo FROM prova p JOIN documento d ON d.id=p.documento_id WHERE p.concurso_id=?",
        (concurso_id,))}
    genericas = {"PROVA", "PROVAS", "DE", "DA", "DO", "DOS", "DAS", "CONHECIMENTOS", "BASICOS", "GERAIS", "ESPECIFICOS",
                 "PARA", "O", "OS", "A", "AS", "CARGO", "CARGOS", "TODOS", "NIVEL", "SUPERIOR", "MEDIO", "E", "BLOCO",
                 "I", "II", "III", "OBJETIVA", "OBJETIVAS", "EM", "AREA", "ESPECIALIDADE", "-", "/", "|"}
    for (doc_id, secao), ls in secoes.items():
        placar = []
        for pid, mapa in defin.items():
            ok = sum(1 for l in ls if l["numero"] in mapa and mapa[l["numero"]][1] == l["definitiva"])
            if ok >= max(1, 0.5 * len(ls)):
                placar.append((ok, pid))
        if not placar:
            db.pendencia(con, "gabarito", f"justificativas da seção '{secao}' sem prova correspondente",
                         concurso_id, doc_id)
            continue
        topo = max(o for o, _ in placar)
        alvos = [pid for o, pid in placar if o == topo]
        especificas = {t for t in re.findall(r"[A-Z0-9]+", norm(secao or "")) if t not in genericas and not t.isdigit()}
        nums_cargo = set(re.findall(r"CARGO\s+(\d+)", norm(secao or "")))
        if len(alvos) > 1 and (especificas or nums_cargo):
            filtrados = [pid for pid in alvos if especificas <= descr.get(pid, set())
                         and all(n in descr.get(pid, set()) for n in nums_cargo)]
            alvos = filtrados or alvos
        if len(alvos) > 1 and (especificas or nums_cargo):
            db.pendencia(con, "gabarito", f"justificativas da seção '{secao}' ambíguas entre {len(alvos)} provas",
                         concurso_id, doc_id)
            continue
        for melhor in alvos:
            _grava_just(con, ls, defin[melhor], doc_id)


def _grava_just(con, ls, mapa, doc_id) -> None:
    for l in ls:
        q = mapa.get(l["numero"])
        if not q:
            continue
        texto = f"[{l['situacao']}] {l['texto']}".strip() if l["situacao"] else l["texto"]
        con.execute(
            "UPDATE gabarito SET justificativa=?, fonte_justificativa=?, "
            "resposta_preliminar=COALESCE(resposta_preliminar, ?), "
            "anulada=CASE WHEN ?='X' THEN 1 ELSE anulada END WHERE questao_id=?",
            (texto, doc_id, l["preliminar"], l["definitiva"], q[0]))
        con.execute("UPDATE gabarito SET alterada=1 WHERE questao_id=? AND resposta_preliminar IS NOT NULL "
                    "AND resposta_definitiva IS NOT NULL AND resposta_definitiva<>'X' "
                    "AND resposta_preliminar<>resposta_definitiva", (q[0],))


def _aplica_padroes(con, concurso_id: int) -> None:
    pads = con.execute("SELECT * FROM documento WHERE concurso_id=? AND tipo='padrao_resposta' AND arquivo_local IS NOT NULL "
                       "AND acessibilidade=0 AND COALESCE(versao,'')<>'sem_efeito'", (concurso_id,)).fetchall()
    if not pads:
        return
    discs = con.execute("SELECT p.id, p.cargo, d.descricao FROM prova p JOIN documento d ON d.id=p.documento_id "
                        "WHERE p.concurso_id=? AND EXISTS (SELECT 1 FROM questao q WHERE q.prova_id=p.id AND q.tipo='DISC')",
                        (concurso_id,)).fetchall()
    for pad in pads:
        alvo = [p for p in discs if p["cargo"] and pad["cargo"] and norm(p["cargo"]) == norm(pad["cargo"])]
        if not alvo and len(discs) == 1:
            alvo = discs
        if len(alvo) != 1:
            db.pendencia(con, "gabarito", f"padrão de resposta sem prova discursiva correspondente ({len(alvo)} candidatas)",
                         concurso_id, pad["id"])
            continue
        texto = ler(_abs(pad["arquivo_local"])).texto
        partes = re.split(r"(?im)^\s*QUEST[ÃA]O\s+(\d+)\s*$", texto)
        qs = con.execute("SELECT id, numero FROM questao WHERE prova_id=? AND tipo='DISC'", (alvo[0]["id"],)).fetchall()
        por_num = {}
        if len(partes) >= 5:
            for i in range(1, len(partes) - 1, 2):
                por_num[int(partes[i])] = partes[i + 1].strip()
        for q in qs:
            t = por_num.get(q["numero"], texto)
            con.execute("INSERT INTO gabarito(questao_id, padrao_resposta, fonte_padrao) VALUES (?,?,?) "
                        "ON CONFLICT(questao_id) DO UPDATE SET padrao_resposta=excluded.padrao_resposta, "
                        "fonte_padrao=excluded.fonte_padrao", (q["id"], t, pad["id"]))
        db.resolver_pendencias(con, "gabarito", concurso_id, pad["id"], "padrão")


# ---------------------------------------------------------------- validação por prova
def validar_provas(con, concurso_id: int) -> None:
    for p in con.execute("SELECT * FROM prova WHERE concurso_id=?", (concurso_id,)).fetchall():
        qs = con.execute("SELECT q.numero, q.tipo, g.resposta_definitiva, g.resposta_preliminar FROM questao q "
                         "LEFT JOIN gabarito g ON g.questao_id=q.id WHERE q.prova_id=?", (p["id"],)).fetchall()
        obj = [q for q in qs if q["tipo"] != "DISC"]
        sem = [q["numero"] for q in obj if q["resposta_definitiva"] is None and q["resposta_preliminar"] is None]
        db.resolver_pendencias(con, "validacao", p["concurso_id"], p["documento_id"])
        status = "completa"
        if not qs:
            status = "falhou"
        elif obj and p["n_gabarito"] is None:
            status = "parcial"
            db.pendencia(con, "validacao", "prova sem gabarito vinculado", p["concurso_id"], p["documento_id"])
        elif obj and p["n_gabarito"] != len(obj):
            status = "parcial"
            db.pendencia(con, "validacao", f"nº de itens extraídos ({len(obj)}) difere do gabarito ({p['n_gabarito']})",
                         p["concurso_id"], p["documento_id"])
        if sem and status == "completa":
            status = "parcial"
        if sem:
            db.pendencia(con, "validacao", f"{len(sem)} questão(ões) sem gabarito: {sem[:15]}",
                         p["concurso_id"], p["documento_id"])
        con.execute("UPDATE prova SET extracao_status=? WHERE id=?", (status, p["id"]))


# ---------------------------------------------------------------- orquestração
def extract(con, slugs=None, ano=None, desde=None, refazer: bool = False) -> dict:
    q = "SELECT * FROM concurso WHERE detalhe_ok=1"
    args: list = []
    if slugs:
        q += f" AND slug IN ({','.join('?' * len(slugs))})"
        args += slugs
    if ano:
        q += " AND ano=?"
        args.append(ano)
    if desde:
        q += " AND ano>=?"
        args.append(desde)
    st = {"concursos": 0, "gabaritos": 0, "provas": 0, "justificativas": 0, "erros": 0, "pulados": 0}
    for c in con.execute(q + " ORDER BY ano DESC, slug", args).fetchall():
        docs = con.execute(
            "SELECT * FROM documento WHERE concurso_id=? AND arquivo_local IS NOT NULL AND sha256 IS NOT NULL "
            "AND acessibilidade=0 AND COALESCE(versao,'')<>'sem_efeito' AND removido_do_site=0", (c["id"],)).fetchall()
        if not docs:
            continue
        st["concursos"] += 1
        mudou = False
        ordem = sorted(docs, key=lambda d: (0 if d["tipo"] in TIPOS_GAB else 1 if d["tipo"] in TIPOS_PROVA else 2))
        for d in ordem:
            if d["tipo"] not in TIPOS_GAB + TIPOS_PROVA + ("justificativa",):
                continue
            if _ja_feito(con, d, refazer):
                st["pulados"] += 1
                continue
            try:
                if d["tipo"] in TIPOS_GAB:
                    _processa_gabarito(con, d)
                    st["gabaritos"] += 1
                elif d["tipo"] in TIPOS_PROVA:
                    _processa_prova(con, d, c)
                    st["provas"] += 1
                else:
                    _processa_justificativa(con, d)
                    st["justificativas"] += 1
                db.resolver_pendencias(con, "extracao", c["id"], d["id"], "erro")
                _marca(con, d)
                mudou = True
            except Exception as e:  # noqa: BLE001
                con.rollback()
                st["erros"] += 1
                log.exception("erro extraindo %s/%s", c["slug"], d["nome_arquivo"])
                db.pendencia(con, "extracao", f"erro: {type(e).__name__}: {str(e)[:200]}", c["id"], d["id"])
                _marca(con, d, "erro")
            con.commit()
        if mudou or refazer:
            vincular(con, c["id"])
            validar_provas(con, c["id"])
            con.commit()
            log.info("%s: extraído", c["slug"])
    return st
