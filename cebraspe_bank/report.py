"""Relatório final (REPORT_FINAL.md) e exportação das pendências (data/pendencias.csv)."""
from __future__ import annotations

import csv
from pathlib import Path

from . import config, db


def _tab(cab: list[str], linhas) -> str:
    out = ["| " + " | ".join(cab) + " |", "|" + "---|" * len(cab)]
    for l in linhas:
        out.append("| " + " | ".join("" if v is None else str(v) for v in l) + " |")
    return "\n".join(out)


def report(con, saida: str, slugs=None, ano=None, desde=None) -> dict:
    from .validate import _filtro
    fq, fa = _filtro(slugs, ano, desde)
    um = lambda q, a=fa: con.execute(q, a).fetchone()[0]  # noqa: E731
    n_conc = um(f"SELECT COUNT(*) FROM concurso c WHERE 1=1{fq}")
    n_det = um(f"SELECT COUNT(*) FROM concurso c WHERE c.detalhe_ok=1{fq}")
    n_com_prova = um(f"SELECT COUNT(DISTINCT c.id) FROM concurso c JOIN prova p ON p.concurso_id=c.id WHERE 1=1{fq}")
    n_docs = um(f"SELECT COUNT(*) FROM documento d JOIN concurso c ON c.id=d.concurso_id WHERE d.sha256 IS NOT NULL{fq}")
    n_bytes = um(f"SELECT COALESCE(SUM(d.tamanho),0) FROM documento d JOIN concurso c ON c.id=d.concurso_id WHERE d.sha256 IS NOT NULL{fq}")
    st = dict(con.execute(f"SELECT COALESCE(p.extracao_status,'?'), COUNT(*) FROM prova p JOIN concurso c ON c.id=p.concurso_id "
                          f"WHERE 1=1{fq} GROUP BY 1", fa).fetchall())
    n_prov = sum(st.values())
    pct = 100.0 * st.get("completa", 0) / n_prov if n_prov else 0.0
    por_tipo = con.execute(f"SELECT q.tipo, COUNT(*) FROM questao q JOIN prova p ON p.id=q.prova_id JOIN concurso c "
                           f"ON c.id=p.concurso_id WHERE 1=1{fq} GROUP BY 1 ORDER BY 2 DESC", fa).fetchall()
    n_obj = um(f"SELECT COUNT(*) FROM questao q JOIN prova p ON p.id=q.prova_id JOIN concurso c ON c.id=p.concurso_id "
               f"WHERE q.tipo<>'DISC'{fq}")
    n_apoio = con.execute(f"""SELECT SUM(q.texto_id IS NOT NULL), SUM(q.texto_id IS NOT NULL AND q.texto_id<>q.texto_base_id)
                          FROM questao q JOIN prova p ON p.id=q.prova_id JOIN concurso c ON c.id=p.concurso_id
                          WHERE q.tipo<>'DISC'{fq}""", fa).fetchone()
    # provas cujas questões com resposta têm só o gabarito preliminar (definitivo não publicado ou não vinculado)
    so_pre = con.execute(f"""SELECT COUNT(*), COALESCE(SUM(n), 0) FROM (SELECT p.id, COUNT(*) n FROM questao q
                         JOIN prova p ON p.id=q.prova_id JOIN concurso c ON c.id=p.concurso_id
                         JOIN gabarito g ON g.questao_id=q.id WHERE q.tipo<>'DISC'
                         AND (g.resposta_definitiva IS NOT NULL OR g.resposta_preliminar IS NOT NULL){fq}
                         GROUP BY p.id HAVING SUM(g.resposta_definitiva IS NOT NULL)=0)""", fa).fetchone()
    sem_gab = um(f"""SELECT COUNT(*) FROM questao q JOIN prova p ON p.id=q.prova_id JOIN concurso c ON c.id=p.concurso_id
                     LEFT JOIN gabarito g ON g.questao_id=q.id WHERE q.tipo<>'DISC'
                     AND (g.id IS NULL OR (g.resposta_definitiva IS NULL AND g.resposta_preliminar IS NULL)){fq}""")
    gab = con.execute(f"""SELECT SUM(g.resposta_definitiva IS NOT NULL), SUM(g.resposta_preliminar IS NOT NULL),
                          SUM(g.anulada), SUM(g.alterada), SUM(g.justificativa IS NOT NULL), SUM(g.padrao_resposta IS NOT NULL)
                          FROM gabarito g JOIN questao q ON q.id=g.questao_id JOIN prova p ON p.id=q.prova_id
                          JOIN concurso c ON c.id=p.concurso_id WHERE 1=1{fq}""", fa).fetchone()
    por_ano = con.execute(
        f"""SELECT c.ano, COUNT(DISTINCT c.id), COUNT(DISTINCT p.id), COUNT(q.id)
            FROM concurso c LEFT JOIN prova p ON p.concurso_id=c.id LEFT JOIN questao q ON q.prova_id=p.id
            WHERE 1=1{fq} GROUP BY c.ano ORDER BY c.ano""", fa).fetchall()
    fontes = con.execute(f"SELECT COALESCE(c.ano_fonte,'(sem ano)'), COUNT(*) FROM concurso c WHERE 1=1{fq} GROUP BY 1 "
                         "ORDER BY 2 DESC", fa).fetchall()
    pend = con.execute(
        f"""SELECT x.etapa, x.motivo, COUNT(*) FROM pendencia x LEFT JOIN concurso c ON c.id=x.concurso_id
            WHERE x.resolvido_em IS NULL{fq.replace('c.', 'c.')} GROUP BY 1,2 ORDER BY 1, 3 DESC""", fa).fetchall()
    # agrupa motivos com números variáveis
    import re
    agrup: dict[tuple, int] = {}
    for e, m, n in pend:
        chave = (e, re.sub(r"\d+", "N", re.sub(r"\[.*?\]", "[…]", m))[:140])
        agrup[chave] = agrup.get(chave, 0) + n
    csv_path = config.DATA_DIR / "pendencias.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["etapa", "slug", "documento", "motivo", "criado_em"])
        for r in con.execute(
                f"""SELECT x.etapa, c.slug, d.nome_arquivo, x.motivo, x.criado_em FROM pendencia x
                    LEFT JOIN concurso c ON c.id=x.concurso_id LEFT JOIN documento d ON d.id=x.documento_id
                    WHERE x.resolvido_em IS NULL{fq} ORDER BY x.etapa, c.slug""", fa):
            w.writerow(list(r))
    jq = f"FROM questao q JOIN prova p ON p.id=q.prova_id JOIN concurso c ON c.id=p.concurso_id WHERE 1=1{fq}"
    n_q = um(f"SELECT COUNT(*) {jq}")
    n_disc = um(f"SELECT COUNT(*) {jq} AND q.disciplina IS NOT NULL")
    n_ass = um(f"SELECT COUNT(*) {jq} AND q.assunto IS NOT NULL")
    disc_fonte = con.execute(f"SELECT COALESCE(q.disciplina_fonte,'(não identificada)'), COUNT(*) {jq} GROUP BY 1 "
                             "ORDER BY 2 DESC", fa).fetchall()
    disc_tipo = con.execute(f"""SELECT q.disciplina, COUNT(*), SUM(q.tipo='CE'), SUM(q.tipo='ME'), SUM(q.tipo='DISC')
                            {jq} AND q.disciplina IS NOT NULL GROUP BY 1 ORDER BY 2 DESC""", fa).fetchall()
    n_conc_ed = um(f"""SELECT COUNT(DISTINCT e.concurso_id) FROM edital_disciplina e JOIN concurso c ON c.id=e.concurso_id
                       WHERE e.tipo<>'vazio'{fq}""")
    n_conc_vazio = um(f"""SELECT COUNT(DISTINCT e.concurso_id) FROM edital_disciplina e JOIN concurso c ON c.id=e.concurso_id
                          WHERE e.tipo='vazio'{fq}""")
    blocos = con.execute(f"SELECT COALESCE(q.bloco,'(sem título de bloco)'), COUNT(*), SUM(q.disciplina IS NOT NULL) "
                         f"{jq} GROUP BY 1 ORDER BY 2 DESC", fa).fetchall()
    falhos_crawl = [r[0] for r in con.execute(
        f"SELECT c.slug FROM concurso c WHERE c.detalhe_ok=0{fq} ORDER BY c.slug", fa)]

    md = ["# Relatório final — banco de questões Cebraspe\n",
          f"Gerado em {db.agora()} a partir de `{config.DB_PATH.name}`.\n",
          "## Visão geral\n",
          _tab(["Métrica", "Valor"], [
              ("Concursos listados", n_conc),
              ("Concursos com detalhe na API", n_det),
              ("Concursos com provas extraídas", n_com_prova),
              ("Documentos baixados", f"{n_docs} ({n_bytes / 1e9:.2f} GB)"),
              ("Provas processadas", n_prov),
              ("Provas com extração completa", f"{st.get('completa', 0)} ({pct:.1f}%)"),
              ("Provas parciais / falhas", f"{st.get('parcial', 0)} / {st.get('falhou', 0)}"),
          ]),
          "\n## Questões por tipo\n",
          _tab(["Tipo", "Questões"], por_tipo),
          "\n### Itens de opção de língua estrangeira\n",
          _tab(["Variante", "Questões", "Com gabarito definitivo"], con.execute(
              f"""SELECT q.variante, COUNT(*), SUM(g.resposta_definitiva IS NOT NULL) FROM questao q
                  JOIN prova p ON p.id=q.prova_id JOIN concurso c ON c.id=p.concurso_id
                  LEFT JOIN gabarito g ON g.questao_id=q.id WHERE q.variante<>''{fq} GROUP BY 1 ORDER BY 2 DESC""",
              fa).fetchall()),
          "\n## Gabaritos\n",
          f"Questões objetivas (C/E e ME) sem nenhum gabarito vinculado: **{sem_gab}** "
          f"({100.0 * sem_gab / max(1, n_obj):.1f}% de {n_obj}). Cada caso tem pendência com o motivo.\n",
          f"\nQuestões objetivas com **texto de apoio** (`texto_id`): **{n_apoio[0]}**, das quais {n_apoio[1]} "
          f"ligadas pelo rótulo citado no comando (\"do texto CB1A1\").\n",
          f"\nProvas com **somente o gabarito preliminar** (definitivo não publicado ou não vinculado): **{so_pre[0]}** "
          f"({so_pre[1]} questões). Nelas `resposta_definitiva` fica vazia e a resposta está em `resposta_preliminar`; "
          f"cada prova tem a pendência de validação correspondente.\n",
          _tab(["Com definitivo", "Com preliminar", "Anuladas", "Alteradas", "Com justificativa", "Com padrão de resposta"],
               [tuple(v or 0 for v in gab)]),
          "\n## Disciplinas (Fase 5)\n",
          f"Questões com **disciplina** identificada: **{n_disc}** ({100.0 * n_disc / max(1, n_q):.1f}% de {n_q}); "
          f"com **assunto** literal do comando: **{n_ass}** ({100.0 * n_ass / max(1, n_q):.1f}%). "
          "As provas do Cebraspe quase nunca têm título de disciplina: a disciplina vem do idioma da opção de língua "
          "(`variante`), do título do bloco quando ele é uma disciplina (`titulo_pdf`), do idioma do comando "
          "(`regra_comando`), do conteúdo programático do edital de abertura comparado ao assunto literal "
          "(`edital_assunto`), da tabela de palavras-chave aplicada ao assunto (`regra_assunto`), da única "
          "disciplina/área do cargo no edital (`edital_unica`) ou da área declarada na prova quando o concurso não "
          "tem conteúdo programático (`area_prova`). Sem nenhuma dessas fontes fica NULL.\n",
          f"\nEditais de abertura lidos com conteúdo programático: **{n_conc_ed}** concursos; "
          f"sem conteúdo programático legível: **{n_conc_vazio}** (pendência `disciplina`).\n",
          _tab(["disciplina_fonte", "Questões"], disc_fonte),
          "",
          _tab(["Disciplina", "Questões", "CE", "ME", "DISC"], disc_tipo),
          "\n### Blocos da prova\n",
          _tab(["Bloco", "Questões", "Com disciplina"], blocos),
          "\n## Concursos e questões por ano\n",
          _tab(["Ano", "Concursos", "Provas", "Questões"], por_ano),
          "\n## Fonte do ano do concurso\n",
          _tab(["ano_fonte", "Concursos"], fontes),
          "\n## Pendências (abertas)\n",
          f"Lista completa em `{csv_path.relative_to(config.ROOT) if csv_path.is_relative_to(config.ROOT) else csv_path}`.\n",
          _tab(["Etapa", "Motivo (números agrupados)", "Ocorrências"],
               [(e, m, n) for (e, m), n in sorted(agrup.items(), key=lambda kv: (kv[0][0], -kv[1]))]),
          "\n## Observações de método\n",
          "- Nada é estimado: resposta, ano ou texto que não pôde ser lido fica NULL e gera pendência.\n"
          "- `alterada=1` só quando há evidência (preliminar e definitivo publicados, ou tabela de justificativas). "
          "O site costuma retirar o gabarito preliminar após o definitivo, então a ausência de alteração não é prova "
          "de que o item não mudou.\n"
          "- Itens de opção de língua estrangeira (ex.: itens 1–10 em espanhol e em inglês) são guardados por língua "
          "(`questao.variante`, `gabarito_bruto.variante`): na prova pelo título 'LÍNGUA X' de cada bloco e no "
          "gabarito pela cor da célula e a legenda. Conflitos que a legenda não resolve ficam sem resposta.\n"
          "- Versões de acessibilidade (adaptada, superampliada, ledor, braile, VLibras) foram ignoradas.\n"
          "- Números de itens ofuscados (substituição de glifos, comum em 2015–2017) são decodificados pela "
          "restrição de sequência consecutiva.\n",
          "\n### Concursos sem detalhe na API\n",
          ", ".join(f"`{s}`" for s in falhos_crawl) or "nenhum",
          ""]
    Path(saida).write_text("\n".join(md), encoding="utf-8")
    return {"saida": saida, "provas": n_prov, "completas_pct": round(pct, 1), "pendencias_csv": str(csv_path)}
