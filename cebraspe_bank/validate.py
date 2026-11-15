"""Validação: consistência do banco e amostra aleatória para revisão manual (HTML lado a lado)."""
from __future__ import annotations

import html
import json
import random
from pathlib import Path

import pymupdf

from . import config, db
from .extract import validar_provas


def _filtro(slugs, ano, desde, alias="c"):
    q, a = "", []
    if slugs:
        q += f" AND {alias}.slug IN ({','.join('?' * len(slugs))})"
        a += slugs
    if ano:
        q += f" AND {alias}.ano=?"
        a.append(ano)
    if desde:
        q += f" AND {alias}.ano>=?"
        a.append(desde)
    return q, a


def validate(con, slugs=None, ano=None, desde=None, amostra: int = 20, seed: int = 42) -> dict:
    fq, fa = _filtro(slugs, ano, desde)
    res: dict = {}
    for (cid,) in con.execute(f"SELECT DISTINCT c.id FROM concurso c JOIN prova p ON p.concurso_id=c.id WHERE 1=1{fq}", fa).fetchall():
        validar_provas(con, cid)
    # todo concurso e toda prova com ano
    sem_ano = con.execute(f"SELECT c.id, c.slug FROM concurso c WHERE c.ano IS NULL{fq}", fa).fetchall()
    for c in sem_ano:
        db.pendencia(con, "ano", "concurso sem ano identificável", c["id"])
    provas_sem_ano = con.execute(f"SELECT p.id, p.concurso_id, p.documento_id FROM prova p JOIN concurso c ON c.id=p.concurso_id "
                                 f"WHERE p.ano IS NULL{fq}", fa).fetchall()
    for p in provas_sem_ano:
        db.pendencia(con, "ano", "prova sem ano", p["concurso_id"], p["documento_id"])
    sem_gab = con.execute(
        f"""SELECT COUNT(*) FROM questao q JOIN prova p ON p.id=q.prova_id JOIN concurso c ON c.id=p.concurso_id
            LEFT JOIN gabarito g ON g.questao_id=q.id
            WHERE q.tipo<>'DISC' AND (g.id IS NULL OR (g.resposta_definitiva IS NULL AND g.resposta_preliminar IS NULL)){fq}""",
        fa).fetchone()[0]
    con.commit()
    res["concursos_sem_ano"] = len(sem_ano)
    res["provas_sem_ano"] = len(provas_sem_ano)
    res["questoes_objetivas_sem_gabarito"] = sem_gab
    res["provas_por_status"] = dict(con.execute(
        f"SELECT COALESCE(p.extracao_status,'?'), COUNT(*) FROM prova p JOIN concurso c ON c.id=p.concurso_id WHERE 1=1{fq} "
        "GROUP BY 1", fa).fetchall())
    res["revisao_html"] = str(gerar_revisao(con, amostra, seed, fq, fa))
    return res


def gerar_revisao(con, n: int, seed: int, fq: str = "", fa: list | None = None) -> Path:
    ids = [r[0] for r in con.execute(
        f"SELECT q.id FROM questao q JOIN prova p ON p.id=q.prova_id JOIN concurso c ON c.id=p.concurso_id WHERE 1=1{fq} "
        "ORDER BY q.id", fa or []).fetchall()]
    rnd = random.Random(seed)
    escolha = rnd.sample(ids, min(n, len(ids)))
    out_dir = config.DATA_DIR / "revisao"
    (out_dir / "pag").mkdir(parents=True, exist_ok=True)
    blocos = []
    for k, qid in enumerate(escolha, 1):
        q = con.execute(
            """SELECT q.*, p.cargo, p.caderno, p.codigo_prova, c.slug, c.ano, d.arquivo_local, d.nome_arquivo, d.url,
                      t.conteudo AS tb, g.resposta_preliminar, g.resposta_definitiva, g.anulada, g.alterada, g.justificativa,
                      g.padrao_resposta
               FROM questao q JOIN prova p ON p.id=q.prova_id JOIN concurso c ON c.id=p.concurso_id
               JOIN documento d ON d.id=p.documento_id LEFT JOIN texto_base t ON t.id=q.texto_base_id
               LEFT JOIN gabarito g ON g.questao_id=q.id WHERE q.id=?""", (qid,)).fetchone()
        pdf = Path(q["arquivo_local"])
        pdf = pdf if pdf.is_absolute() else config.ROOT / pdf
        imgs = []
        try:
            with pymupdf.open(pdf) as doc:
                for pno in {q["pagina"] - 1, q["pagina"]} & set(range(doc.page_count)):
                    arq = out_dir / "pag" / f"q{qid}_p{pno + 1}.png"
                    if not arq.exists():
                        doc[pno].get_pixmap(dpi=110).save(arq)
                    imgs.append(arq.relative_to(out_dir))
        except Exception:  # noqa: BLE001
            imgs = []
        e = html.escape
        alts = json.loads(q["alternativas_json"]) if q["alternativas_json"] else {}
        alts_html = "".join(f"<li><b>{e(a)}</b> {e(t)}</li>" for a, t in alts.items())
        figs = "".join(f'<img class="fig" src="../../{e(x)}">' for x in json.loads(q["imagens"] or "[]"))
        lado_esq = "".join(f'<img class="pag" src="{e(str(i))}">' for i in imgs) or "<p>(página indisponível)</p>"
        blocos.append(f"""
<section>
  <h2>{k}. {e(q['slug'])} ({q['ano']}) — questão {q['numero']}{' — ' + e(q['variante']) if q['variante'] else ''} [{q['tipo']}] — pág. {q['pagina']}</h2>
  <p class="meta">{e(q['nome_arquivo'])} · cargo: {e(q['cargo'] or '-')} · caderno: {e(q['caderno'] or '-')} ·
     código: {e(q['codigo_prova'] or '-')} · seção: {e(q['secao'] or '-')} · texto: {q['origem_texto']} ·
     <a href="{e(q['url'])}">PDF original</a></p>
  <div class="cols">
    <div class="esq">{lado_esq}</div>
    <div class="dir">
      {"<details><summary>Texto-base</summary><p>" + e(q['tb']) + "</p></details>" if q['tb'] else ""}
      <p class="enun">{e(q['enunciado'])}</p>
      {"<ol class='alts'>" + alts_html + "</ol>" if alts_html else ""}
      {figs}
      <table><tr><th>Preliminar</th><th>Definitivo</th><th>Anulada</th><th>Alterada</th></tr>
      <tr><td>{e(q['resposta_preliminar'] or '-')}</td><td>{e(q['resposta_definitiva'] or '-')}</td>
          <td>{'sim' if q['anulada'] else 'não'}</td><td>{'sim' if q['alterada'] else 'não'}</td></tr></table>
      {"<p class='just'><b>Justificativa:</b> " + e(q['justificativa']) + "</p>" if q['justificativa'] else ""}
      {"<details><summary>Padrão de resposta</summary><p>" + e(q['padrao_resposta'][:4000]) + "</p></details>" if q['padrao_resposta'] else ""}
      <fieldset><legend>Revisão</legend>
        <label><input type="radio" name="r{qid}" value="ok"> correto</label>
        <label><input type="radio" name="r{qid}" value="texto"> erro no texto</label>
        <label><input type="radio" name="r{qid}" value="gabarito"> erro no gabarito</label>
        <label><input type="radio" name="r{qid}" value="vinculo"> texto-base/vínculo errado</label>
        <input type="text" name="obs{qid}" placeholder="observação">
      </fieldset>
    </div>
  </div>
</section>""")
    pagina = f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>Revisão da amostra</title>
<style>
:root {{ --fundo:#fff; --texto:#1a1a1a; --borda:#ddd; --suave:#666; }}
@media (prefers-color-scheme: dark) {{ :root {{ --fundo:#16181c; --texto:#e8e8e8; --borda:#3a3d44; --suave:#a0a4ab; }} }}
body {{ background:var(--fundo); color:var(--texto); font:15px/1.5 system-ui, sans-serif; margin:0 16px; }}
section {{ border-bottom:1px solid var(--borda); padding:16px 0; }}
.cols {{ display:grid; grid-template-columns: minmax(0,1fr) minmax(0,1fr); gap:16px; }}
@media (max-width: 900px) {{ .cols {{ grid-template-columns: 1fr; }} }}
.pag {{ width:100%; border:1px solid var(--borda); margin-bottom:8px; }}
.fig {{ max-width:100%; border:1px solid var(--borda); }}
.meta {{ color:var(--suave); font-size:13px; }}
table {{ border-collapse:collapse; margin:8px 0; }} td,th {{ border:1px solid var(--borda); padding:4px 10px; }}
.enun {{ white-space:pre-wrap; }} fieldset {{ border:1px solid var(--borda); }}
</style></head><body>
<h1>Revisão manual — {len(escolha)} questões (semente {seed})</h1>
<p>Compare cada questão extraída (direita) com a página original do PDF (esquerda) e marque o resultado.</p>
{''.join(blocos)}
</body></html>"""
    arq = out_dir / "revisao_amostra.html"
    arq.write_text(pagina, encoding="utf-8")
    return arq
