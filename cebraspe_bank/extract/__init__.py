"""Fases 3 e 4 — extração de questões e gabaritos, vínculo e validação por prova."""
from __future__ import annotations

import json
import logging
import re
from pathlib import Path

from .. import anos, config, db
from ..crawl import recalcular_ano, reclassificar
from ..texto import norm
from . import combinado, gabarito as gab, justificativa as just
from .pdf import Documento, ler, recorte
from .prova import Item, ResultadoProva

log = logging.getLogger(__name__)

TIPOS_PROVA = ("prova", "prova_com_gabarito_preliminar", "prova_com_gabarito_definitivo")
TIPOS_GAB = ("gabarito_preliminar", "gabarito_definitivo")
VERSAO_EXTRATOR = "13"


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
                 data_edital=None, data_aplicacao=None, origem="pdf", variantes: dict[str, dict[int, str]] | None = None):
    con.execute("DELETE FROM gabarito_bruto WHERE documento_id=? AND grupo=?", (doc_id, grupo))
    con.execute(
        "INSERT OR REPLACE INTO gabarito_grupo(documento_id, grupo, codigo_prova, caderno, cargo, fase, data_edital, "
        "data_aplicacao, n, origem) VALUES (?,?,?,?,?,?,?,?,?,?)",
        (doc_id, grupo, codigo, caderno, cargo, fase, data_edital, data_aplicacao,
         len(respostas) + sum(len(v) for v in (variantes or {}).values()), origem))
    linhas = [(doc_id, grupo, codigo, caderno, cargo, fase, "", n, r) for n, r in sorted(respostas.items())]
    for var, resp in (variantes or {}).items():
        linhas += [(doc_id, grupo, codigo, caderno, cargo, fase, var, n, r) for n, r in sorted(resp.items())]
    con.executemany(
        "INSERT INTO gabarito_bruto(documento_id, grupo, codigo_prova, caderno, cargo, fase, variante, numero, resposta) "
        "VALUES (?,?,?,?,?,?,?,?,?)", linhas)


def _resolve_doc(con, doc, etapas=("gabarito", "extracao")) -> None:
    """Pendências do próprio documento são recalculadas a cada reprocessamento."""
    con.execute(f"UPDATE pendencia SET resolvido_em=? WHERE resolvido_em IS NULL AND documento_id=? "
                f"AND etapa IN ({','.join('?' * len(etapas))})", (db.agora(), doc["id"], *etapas))


def _processa_gabarito(con, doc) -> None:
    _resolve_doc(con, doc)
    caminho = _abs(doc["arquivo_local"])
    paginas = gab.parse_todas(caminho)
    for g in paginas:
        if not g.respostas:
            for a in g.avisos:
                db.pendencia(con, "gabarito", a, doc["concurso_id"], doc["id"])
    grupos = gab.agrupa([g for g in paginas if g.respostas])
    con.execute("DELETE FROM gabarito_bruto WHERE documento_id=?", (doc["id"],))
    con.execute("DELETE FROM gabarito_grupo WHERE documento_id=?", (doc["id"],))
    if not grupos:
        # sem tabela: lista de anulações/alterações por versão ("Questão 13 Alterada de D p/ B Versão de prova 1.1"),
        # que só vale junto com o gabarito preliminar (as demais questões são mantidas)
        alt = gab.alteracoes(gab.texto_leitura(caminho))
        if alt:
            for k, (versao, itens) in enumerate(sorted(alt.items())):
                _grava_grupo(con, doc["id"], k, "definitivo", {n: d for n, (_, d) in itens.items()},
                             doc["codigo_prova"], versao, doc["cargo"], origem="alteracoes")
            db.resolver_pendencias(con, "gabarito", doc["concurso_id"], doc["id"], "nenhuma tabela")
            return
        db.pendencia(con, "gabarito", "nenhuma tabela de gabarito reconhecida no PDF", doc["concurso_id"], doc["id"])
        return
    fase_doc = "preliminar" if doc["tipo"] == "gabarito_preliminar" else "definitivo"
    for k, g in enumerate(grupos):
        fase = g.fase or fase_doc
        if g.fase and g.fase != fase_doc:
            db.pendencia(con, "gabarito", f"fase no PDF ({g.fase}) difere da classificação ({fase_doc})",
                         doc["concurso_id"], doc["id"])
        _grava_grupo(con, doc["id"], k, fase, g.respostas, g.codigo_prova or doc["codigo_prova"],
                     g.caderno or doc["caderno"], g.cargo or doc["cargo"], g.data_edital, g.data_aplicacao, g.origem,
                     g.variantes)
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
    _resolve_doc(con, doc)
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

    con.execute("DELETE FROM questao_fts WHERE questao_id IN (SELECT q.id FROM questao q JOIN prova p ON p.id=q.prova_id "
                "WHERE p.documento_id=?)", (doc["id"],))
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
        if (it.numero, it.tipo, it.variante) in vistos:
            avisos.append(f"item {it.numero} repetido na segmentação; mantida a 1ª ocorrência")
            continue
        vistos.add((it.numero, it.tipo, it.variante))
        ocr = any(l.origem == "ocr" for l in it.linhas)
        alts = it.alternativas_texto() if it.alternativas else None
        cur = con.execute(
            "INSERT INTO questao(prova_id, numero, variante, tipo, texto_base_id, enunciado, alternativas_json, "
            "codigo_item, secao, imagens, origem_texto, pagina) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
            (prova_id, it.numero, it.variante, it.tipo, tb_ids.get(id(it.bloco)) if it.bloco else None, it.enunciado,
             json.dumps(alts, ensure_ascii=False) if alts else None, getattr(it, "codigo_item", None), it.secao,
             json.dumps(imgs.get(id(it))) if imgs.get(id(it)) else None, "ocr" if ocr else "pdf", it.pagina + 1))
        qid = cur.lastrowid
        tb = it.bloco.texto if it.bloco else ""
        con.execute("INSERT INTO questao_fts(questao_id, enunciado, texto_base) VALUES (?,?,?)",
                    (qid, it.enunciado + (" " + " ".join(alts.values()) if alts else ""), tb))
        if it.justificativa:
            con.execute("INSERT OR IGNORE INTO gabarito(questao_id, justificativa, fonte_justificativa) VALUES (?,?,?)",
                        (qid, " ".join(l.texto for l in it.justificativa), doc["id"]))
    if doc["tipo"] != "prova" and doc["modalidade"] == "discursiva" and res.itens:
        # prova discursiva publicada junto com o padrão de resposta: o padrão é o próprio documento
        texto = d.texto
        for qid in [r[0] for r in con.execute("SELECT id FROM questao WHERE prova_id=? AND tipo='DISC'", (prova_id,))]:
            con.execute("INSERT INTO gabarito(questao_id, padrao_resposta, fonte_padrao) VALUES (?,?,?) "
                        "ON CONFLICT(questao_id) DO UPDATE SET padrao_resposta=excluded.padrao_resposta, "
                        "fonte_padrao=excluded.fonte_padrao", (qid, texto, doc["id"]))
    elif resp_emb:
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
    _resolve_doc(con, doc)
    linhas = just.parse(ler(_abs(doc["arquivo_local"]), colunas=False))
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
    con.execute("UPDATE pendencia SET resolvido_em=? WHERE resolvido_em IS NULL AND concurso_id=? AND "
                "((etapa='gabarito' AND (motivo LIKE 'justificativas da seção%' OR motivo LIKE 'padrão de resposta%' "
                "OR motivo LIKE 'gabarito ambíguo%')) OR (etapa='validacao' AND motivo LIKE 'descrição de cargo diverge%'))",
                (db.agora(), concurso_id))
    provas = con.execute(
        "SELECT p.*, d.descricao, d.tipo AS doc_tipo, d.caderno AS doc_caderno FROM prova p "
        "JOIN documento d ON d.id=p.documento_id WHERE p.concurso_id=?", (concurso_id,)).fetchall()
    grupos = con.execute(
        "SELECT g.*, d.descricao, d.tipo AS doc_tipo, d.versao FROM gabarito_grupo g JOIN documento d ON d.id=g.documento_id "
        "WHERE d.concurso_id=?", (concurso_id,)).fetchall()
    respostas = {}
    for r in con.execute("SELECT b.documento_id, b.grupo, b.variante, b.numero, b.resposta FROM gabarito_bruto b "
                         "JOIN documento d ON d.id=b.documento_id WHERE d.concurso_id=?", (concurso_id,)):
        respostas.setdefault((r[0], r[1]), {})[(r[2], r[3])] = r[4]
    datas_ed, datas_ap = [], []
    for p in provas:
        qs = con.execute("SELECT id, numero, tipo, variante, secao FROM questao WHERE prova_id=?", (p["id"],)).fetchall()
        tipo_de = {(q["variante"], q["numero"]): q["tipo"] for q in qs if q["tipo"] != "DISC"}
        secao_de = {(q["variante"], q["numero"]): norm(q["secao"] or "") for q in qs if q["tipo"] != "DISC"}
        nums = set(tipo_de)
        escolhido: dict[str, list] = {}
        if nums:
            for fase in ("preliminar", "definitivo"):
                escolhido[fase] = _compoe(con, p, [g for g in grupos if g["fase"] == fase], respostas, nums,
                                          tipo_de, secao_de)
        pre = escolhido.get("preliminar") or []
        de = escolhido.get("definitivo") or []
        # definitivo publicado só como lista de alterações/anulações: os demais itens mantêm o preliminar
        so_alteracoes = bool(de and pre) and all(g["origem"] == "alteracoes" for g, _ in de)
        ap = [g["data_aplicacao"] for g, _ in de if g["data_aplicacao"]]
        if ap:
            con.execute("UPDATE prova SET data_aplicacao=? WHERE id=?", (min(ap), p["id"]))
        for g, _ in pre + de:
            if g["data_edital"]:
                datas_ed.append(g["data_edital"])
            if g["data_aplicacao"]:
                datas_ap.append(g["data_aplicacao"])
        n_gab = 0
        for q in qs:
            if q["tipo"] == "DISC":
                con.execute("INSERT OR IGNORE INTO gabarito(questao_id) VALUES (?)", (q["id"],))
                continue
            fp, rp = _resposta_composta(pre, q["variante"], q["numero"])
            fd, rd = _resposta_composta(de, q["variante"], q["numero"])
            if rd is None and so_alteracoes and rp is not None:
                fd, rd = de[0][0]["documento_id"], rp
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
                (q["id"], rp, rd, anulada, alterada, fp, fd))
        cobertos = set()
        for g, r in (pre if so_alteracoes else (de or pre)):
            cobertos |= {k for k in r if k in nums or (k[0] == "" and any(v == k[1] for _, v in nums))}
        n_gab_total = len(cobertos)
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


_GENERICAS_GAB = {"GABARITO", "GABARITOS", "DEFINITIVO", "DEFINITIVOS", "PRELIMINAR", "PRELIMINARES", "OFICIAL",
                  "OFICIAIS", "PROVA", "PROVAS", "OBJETIVA", "OBJETIVAS", "CADERNO", "DE", "DA", "DO", "DOS", "DAS", "E",
                  "A", "O", "OS", "AS", "PARA", "TODOS", "TODAS", "CARGO", "CARGOS", "CONHECIMENTOS", "BASICOS", "GERAIS",
                  "ESPECIFICOS", "ESPECIALIZADOS", "COMPLEMENTARES", "NIVEL", "SUPERIOR", "MEDIO", "FUNDAMENTAL", "AREA",
                  "AREAS", "EXCETO", "P1", "P2", "P3", "AO", "EM", "COM", "JUSTIFICATIVAS", "MATRIZ", "ATUALIZADO", "TIPO",
                  "OPCAO", "OPCOES", "EMPREGO", "EMPREGOS", "FUNCAO", "FUNCOES", "PERFIL", "PERFIS", "CONHECIMENTO",
                  "BLOCO", "I", "II", "III", "IV", "PAG", "SEM", "EFEITO", "VERSAO", "COMUNS"}


def _num_cargos(t: str | None) -> set[int]:
    t = norm(t)
    if "EXCETO" in t:
        return set()
    m = re.search(r"(?:CARGOS?|EMPREGOS?|OPCOES|PERFIS?)\s+(?:DE\s+)?(\d+)\s+(?:AO?|A)\s+(\d+)", t)
    if m and int(m.group(1)) <= int(m.group(2)) <= int(m.group(1)) + 300:
        return set(range(int(m.group(1)), int(m.group(2)) + 1))
    out = set()
    for m in re.finditer(r"(?:CARGOS?|EMPREGOS?|PERFIS?)\s+((?:\d+\s*(?:,|E)\s*)*\d+)", t):
        out |= {int(x) for x in re.findall(r"\d+", m.group(1))}
    return out


def _niveis(t: str | None) -> set[str]:
    return set(re.findall(r"NIVEL (SUPERIOR|MEDIO|FUNDAMENTAL)", norm(t)))


def _especificas(t: str | None) -> set[str]:
    return {x for x in re.findall(r"[A-Z]{3,}", norm(t)) if x not in _GENERICAS_GAB}


def _cod_base(c: str | None) -> tuple[str, str] | None:
    if not c:
        return None
    c = c.upper()
    m = re.match(r"^(.*?)(?:_(\d{2}))?$", c)
    return m.group(1).replace("_", ""), (m.group(2) or "")


def _mesmo_codigo(a: str | None, b: str | None) -> bool:
    x, y = _cod_base(a), _cod_base(b)
    if not x or not y:
        return False
    if a.replace("_", "").upper() == b.replace("_", "").upper():
        return True
    # mesma base; sufixo de caderno igual, ou "00" (matriz), ou ausente em um dos lados
    return x[0] == y[0] and (x[1] == y[1] or "00" in (x[1], y[1]) or "" in (x[1], y[1]))


def _versao_caderno(cad: str | None) -> int | None:
    """Caderno numérico do gabarito ('1.3' = versão 3 da prova 1; '3') -> 3. Nomes (cores etc.) -> None."""
    m = re.fullmatch(r"(?:\d{1,2}\.)?(\d{1,2})", (cad or "").strip())
    return int(m.group(1)) if m else None


def _mesma_aplicacao(a: str | None, b: str | None) -> bool:
    """Códigos de arquivo da mesma aplicação começam pelo mesmo número (579_ANM, 579_ANM_001_00). Sem código: aceita."""
    ma, mb = re.match(r"\d{3}", a or ""), re.match(r"\d{3}", b or "")
    return not (ma and mb) or ma.group(0) == mb.group(0)


_CURSO = re.compile(r"CURSO DE (FORMACAO|PREPARACAO)|VERIFICACAO DE APRENDIZAGEM|\bPROCAP\b|CAPACITACAO")
_SEC_ESP = re.compile(r"ESPECIFIC|ESPECIALIZAD")
_SEC_BAS = re.compile(r"BASIC|GERA")


def _secao_compativel(desc_g: str, secoes: list[str]) -> bool:
    """Gabarito só de específicos/especializados não vale para itens em seção de básicos/gerais, e vice-versa.
    Seções vazias ou neutras não contam."""
    d = norm(desc_g)
    g_esp, g_bas = bool(_SEC_ESP.search(d)), bool(_SEC_BAS.search(d))
    if g_esp == g_bas:
        return True
    for s in secoes:
        s_esp, s_bas = bool(_SEC_ESP.search(s)), bool(_SEC_BAS.search(s))
        if s_esp != s_bas and s_esp != g_esp:
            return False
    return True


def _sufixo_codigo(c: str | None) -> int | None:
    m = re.search(r"_(\d{2})$", c or "")
    return int(m.group(1)) if m else None


def _compoe(con, p, grupos, respostas, nums, tipo_de, secao_de) -> list:
    """Escolhe um ou mais gabaritos (grupos) com vínculo verdadeiro para a prova, sem sobreposição de itens."""
    desc_p = f"{p['descricao'] or ''} {p['cargo'] or ''}"
    cargos_p = _num_cargos(desc_p)
    niveis_p = _niveis(desc_p)
    toks_p = _especificas(desc_p)
    so_especificos = bool(re.search(r"ESPECIFIC|ESPECIALIZAD|COMPLEMENTAR", norm(p["descricao"]))) and \
        not re.search(r"BASIC|GERA", norm(p["descricao"]))
    # o caderno pode ter seção de conhecimentos gerais/básicos mesmo com descrição "específicos"
    tem_basicos = any(re.search(r"BASIC|GERA", s) for s in secao_de.values())
    # rótulos de texto do caderno ("Texto CG1A1-I", "texto CB2A3") indicam o bloco de conhecimentos gerais/básicos
    rotulos = " ".join(r[0] or "" for r in con.execute(
        "SELECT conteudo FROM texto_base WHERE prova_id=? UNION ALL SELECT enunciado FROM questao WHERE prova_id=?",
        (p["id"], p["id"])))
    blocos_p = set(re.findall(r"\b(C[BG]\d{1,2})A\d", rotulos.upper()))
    cands = []
    for g in grupos:
        r = respostas.get((g["documento_id"], g["grupo"]), {})
        if not r:
            continue
        chaves = {k for k in r if k in nums or (k[0] == "" and any(n == k[1] and v for v, n in nums) and
                                                not any(v for v, _ in r))}
        # versão numérica do caderno (gabarito '1.3') x sufixo do arquivo da prova (_03)
        vg, vp = _versao_caderno(g["caderno"]), _sufixo_codigo(p["codigo_prova"])
        if vg is not None and vp is not None and vg != vp:
            continue
        mesma_versao = vg is not None and vg == vp
        # um gabarito por versão pode cobrir dois cadernos (básicos 1-60 + específicos 61-80): basta cobrir a prova toda
        cobre_prova = mesma_versao and chaves == nums
        # lista de alterações da mesma versão vale para a prova toda, mesmo sem nenhum item alterado nela
        if mesma_versao and g["origem"] == "alteracoes":
            cobre_prova = True
        if (not chaves and not cobre_prova) or (len(chaves) < 0.9 * len(r) and not cobre_prova):
            continue                                   # itens do gabarito não existem nesta prova
        # tipo de resposta compatível com o tipo das questões
        ce = [k for k in chaves if tipo_de.get(k, tipo_de.get(("",) + k[1:], "CE")) == "CE"]
        if any(r[k] not in ("C", "E", "X") for k in ce):
            continue
        me = [k for k in chaves if k not in ce]
        if len(me) >= 5 and all(r[k] in ("C", "E", "X") for k in me):
            continue
        desc_g = f"{g['descricao'] or ''} {g['cargo'] or ''}"
        if g["documento_id"] == p["documento_id"]:
            prio = 4
        elif mesma_versao and not g["codigo_prova"]:
            prio = 3
        elif _mesmo_codigo(p["codigo_prova"], g["codigo_prova"]):
            prio = 3
            cg = _num_cargos(g["descricao"])
            if cargos_p and cg and not (cargos_p & cg):
                db.pendencia(con, "validacao", f"descrição de cargo diverge entre prova e gabarito "
                             f"(mesmo código de arquivo {g['codigo_prova']}); vinculado pelo código",
                             p["concurso_id"], p["documento_id"])
        else:
            cg = _num_cargos(desc_g)
            esp = _especificas(desc_g)
            nv = _niveis(desc_g)
            if nv and niveis_p and not (nv & niveis_p):
                continue
            if not _secao_compativel(desc_g, [secao_de.get(k, "") for k in chaves]):
                continue                               # ex.: gabarito de especializados (P3) x itens de básicos (P1)
            if bool(_CURSO.search(norm(desc_g))) != bool(_CURSO.search(norm(desc_p))):
                continue                               # curso de formação é outra prova, mesmo com o mesmo cargo
            if cg:
                if not cargos_p or not cargos_p <= cg:
                    continue
                prio = 2
            elif esp:
                if not esp <= toks_p:
                    continue
                prio = 2
            elif re.search(r"ESPECIFIC|ESPECIALIZAD", norm(desc_g)) and not re.search(r"BASIC|GERA", norm(desc_g)):
                # gabarito só de conhecimentos específicos, sem cargo: vale para itens de seção específica da prova
                # (prova "matriz" com básicos + específicos), desde que seja da mesma aplicação (prefixo do código)
                if not all("ESPECIFIC" in secao_de.get(k, "") for k in chaves) or \
                        not _mesma_aplicacao(p["codigo_prova"], g["codigo_prova"]):
                    continue
                prio = 1
            else:
                # gabarito genérico (ex.: conhecimentos básicos para todos os cargos)
                parte_g, parte_p = set(re.findall(r"\bP\d\b", norm(desc_g))), set(re.findall(r"\bP\d\b", norm(desc_p)))
                if parte_g and parte_p and parte_g != parte_p:
                    continue                           # gabarito da P1 x prova P2
                # gabarito neutro da mesma parte ("GABARITO DEFINITIVO – PROVA OBJETIVA (P2)") vale também para
                # itens de específicos
                mesma_parte = bool(parte_g) and parte_g == parte_p and not _SEC_BAS.search(norm(desc_g))
                if not mesma_parte and ((so_especificos and not tem_basicos) or
                                        any("ESPECIFIC" in secao_de.get(k, "") for k in chaves)):
                    continue
                prio = 1
                bloco_g = re.search(r"(C[BG]\d{1,2})(?:_\d{2})?$", (g["codigo_prova"] or "").upper())
                if blocos_p and bloco_g:
                    if bloco_g.group(1) not in blocos_p:
                        continue                       # o caderno usa textos de outro bloco (ex.: CG2 x CG1)
                    prio = 1.5
        sem_efeito = g["versao"] == "sem_efeito"
        cands.append((prio, not sem_efeito, len(chaves), g, r, chaves))
    cands.sort(key=lambda c: (c[0], c[1], c[2]), reverse=True)
    escolhidos, cobertos, vetados = [], set(), set()
    for i, (prio, _, _, g, r, chaves) in enumerate(cands):
        if i in vetados or chaves & cobertos:
            continue
        rivais = [j for j, d in enumerate(cands) if j != i and j not in vetados and d[0] == prio
                  and d[5] & chaves and any(d[4].get(k) != r.get(k) for k in d[5] & chaves)]
        if rivais:
            nomes = sorted({cands[j][3]["descricao"] or "" for j in rivais} | {g["descricao"] or ""})
            db.pendencia(con, "gabarito", "gabarito ambíguo para a prova (respostas diferentes): " +
                         " | ".join(n[:80] for n in nomes), p["concurso_id"], p["documento_id"])
            vetados.update(rivais + [i])
            continue
        escolhidos.append((g, r))
        cobertos |= chaves
    return escolhidos


def _resposta_composta(grupos: list, variante: str, numero: int) -> tuple[int | None, str | None]:
    for g, r in grupos:
        v = _resposta(r, variante, numero)
        if v is not None:
            return g["documento_id"], v
    return None, None


def _resposta(mapa: dict, variante: str, numero: int) -> str | None:
    """Resposta do item (variante, número). Item de língua só herda a resposta comum se o gabarito não tem variantes;
    item comum nunca herda a de uma variante."""
    if (variante, numero) in mapa:
        return mapa[(variante, numero)]
    if variante and not any(v for v, _ in mapa):
        return mapa.get(("", numero))
    return None


def _aplica_justificativas(con, concurso_id: int) -> None:
    linhas = con.execute("SELECT j.* FROM justificativa_bruta j JOIN documento d ON d.id=j.documento_id "
                         "WHERE d.concurso_id=? ORDER BY j.documento_id, j.ordem", (concurso_id,)).fetchall()
    if not linhas:
        return
    defin = {}
    for r in con.execute(
            "SELECT q.prova_id, q.numero, q.id, g.resposta_definitiva, g.resposta_preliminar, q.variante FROM questao q "
            "JOIN prova p ON p.id=q.prova_id LEFT JOIN gabarito g ON g.questao_id=q.id "
            "WHERE p.concurso_id=? AND q.tipo<>'DISC'", (concurso_id,)):
        defin.setdefault(r[0], {})[(r[5], r[1])] = (r[2], r[3], r[4])
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
        m_l = re.search(r"L[ÍI]NGUA\s+(INGLESA|ESPANHOLA|FRANCESA|ALEM[ÃA]|ITALIANA)", secao or "", re.I)
        var = f"LÍNGUA {norm(m_l.group(1))}".replace("ALEMA", "ALEMÃ") if m_l else ""
        placar = []
        for pid, mapa in defin.items():
            ok = sum(1 for l in ls if (q := _chave_just(mapa, var, l["numero"])) and q[1] == l["definitiva"])
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
            _grava_just(con, ls, defin[melhor], doc_id, var)


def _chave_just(mapa: dict, var: str, numero: int):
    if (var, numero) in mapa:
        return mapa[(var, numero)]
    if var and not any(v for v, _ in mapa):
        return mapa.get(("", numero))
    return None


def _grava_just(con, ls, mapa, doc_id, var: str = "") -> None:
    for l in ls:
        q = _chave_just(mapa, var, l["numero"])
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
    genericas = {"PADRAO", "PADROES", "DEFINITIVO", "DEFINITIVOS", "PRELIMINAR", "PRELIMINARES", "PROVISORIO", "DE",
                 "DA", "DO", "RESPOSTA", "RESPOSTAS", "PROVA", "PROVAS", "DISCURSIVA", "DISCURSIVAS", "ESCRITA", "E", "A",
                 "O", "PARA", "OS", "AS", "TODOS", "CADERNO"}

    def toks(t):
        return {str(int(x)) if x.isdigit() else x for x in re.findall(r"[A-Z0-9]+", norm(t)) if x not in genericas}

    for pad in pads:
        alvo = [p for p in discs if p["cargo"] and pad["cargo"] and toks(p["cargo"]) == toks(pad["cargo"])]
        if not alvo:
            tp = toks(f"{pad['descricao'] or ''} {pad['cargo'] or ''}")
            if tp:
                alvo = [p for p in discs if tp <= toks(f"{p['descricao'] or ''} {p['cargo'] or ''}")]
                if len(alvo) > 1:   # prefere a correspondência exata do conjunto de palavras
                    exatos = [p for p in alvo if toks(f"{p['descricao'] or ''} {p['cargo'] or ''}") == tp]
                    alvo = exatos or alvo
        if not alvo and len(discs) == 1:
            alvo = discs
        if len(alvo) != 1:
            db.pendencia(con, "gabarito", f"padrão de resposta sem prova discursiva correspondente ({len(alvo)} candidatas)",
                         concurso_id, pad["id"])
            continue
        caminho = _abs(pad["arquivo_local"])
        if not caminho.exists():
            # revínculo sem os PDFs locais: mantém o padrão já gravado
            db.resolver_pendencias(con, "gabarito", concurso_id, pad["id"], "padrão")
            continue
        texto = ler(caminho, colunas=False).texto
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


def _remove_provas_fora(con) -> int:
    """Provas extraídas de documentos que, reclassificados, deixaram de ser prova (capa, justificativas...)."""
    ids = con.execute(f"SELECT p.id, p.concurso_id, p.documento_id FROM prova p JOIN documento d ON d.id=p.documento_id "
                      f"WHERE d.tipo NOT IN ({','.join('?' * len(TIPOS_PROVA))})", TIPOS_PROVA).fetchall()
    for pid, cid, did in ids:
        con.execute("DELETE FROM questao_fts WHERE questao_id IN (SELECT id FROM questao WHERE prova_id=?)", (pid,))
        con.execute("DELETE FROM gabarito WHERE questao_id IN (SELECT id FROM questao WHERE prova_id=?)", (pid,))
        con.execute("DELETE FROM questao WHERE prova_id=?", (pid,))
        con.execute("DELETE FROM texto_base WHERE prova_id=?", (pid,))
        con.execute("DELETE FROM prova_cargo WHERE prova_id=?", (pid,))
        con.execute("DELETE FROM prova WHERE id=?", (pid,))
        con.execute("DELETE FROM gabarito_bruto WHERE documento_id=? AND grupo IN "
                    "(SELECT grupo FROM gabarito_grupo WHERE documento_id=? AND origem='embutido')", (did, did))
        con.execute("DELETE FROM gabarito_grupo WHERE documento_id=? AND origem='embutido'", (did,))
        for etapa in ("validacao", "gabarito", "extracao"):
            db.resolver_pendencias(con, etapa, cid, did)
    con.commit()
    return len(ids)


# ---------------------------------------------------------------- orquestração
def extract(con, slugs=None, ano=None, desde=None, refazer: bool = False, revincular: bool = False) -> dict:
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
    st = {"concursos": 0, "gabaritos": 0, "provas": 0, "justificativas": 0, "erros": 0, "pulados": 0,
          "reclassificados": reclassificar(con), "provas_removidas": _remove_provas_fora(con),
          "orfaos_removidos": db.limpar_orfaos(con)}
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
        if mudou or refazer or revincular:
            vincular(con, c["id"])
            validar_provas(con, c["id"])
            con.commit()
            log.info("%s: extraído", c["slug"])
    return st
