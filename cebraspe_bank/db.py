"""Esquema SQLite e utilitários de acesso."""
from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from . import config

SCHEMA = r"""
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS concurso (
    id                INTEGER PRIMARY KEY,
    slug              TEXT NOT NULL UNIQUE,
    id_evento         INTEGER,
    orgao             TEXT,              -- prefixo do slug antes do ano (ex.: TRE_BA)
    orgao_nome        TEXT,              -- nome por extenso lido do cabeçalho dos PDFs (Fase 3/4)
    nome              TEXT,              -- eventoNomeAbreviado
    ano               INTEGER,           -- ano do concurso = ano do edital de abertura (ver ano_fonte)
    ano_edital        INTEGER,
    ano_aplicacao     INTEGER,
    ano_fonte         TEXT,              -- edital_pdf | edital_publicacao | slug | aplicacao
    ano_slug          INTEGER,
    ano_api           INTEGER,           -- eventoAno da API: só evidência, fora da precedência
    data_edital       TEXT,              -- ISO, quando conhecida
    data_edital_pdf   TEXT,              -- data do Edital nº 1 lida nos PDFs (gabaritos/provas)
    data_aplicacao    TEXT,              -- primeira data de aplicação lida nos gabaritos
    url               TEXT,
    status            TEXT,              -- novos | inscricoes-abertas | em-andamento | encerrado
    periodo_inscricao TEXT,
    detalhe_ok        INTEGER NOT NULL DEFAULT 0,
    detalhe_http      INTEGER,
    json_sha256       TEXT,
    atualizado_em     TEXT
);
CREATE INDEX IF NOT EXISTS ix_concurso_ano ON concurso(ano);
CREATE INDEX IF NOT EXISTS ix_concurso_orgao_ano ON concurso(orgao, ano);

CREATE TABLE IF NOT EXISTS documento (
    id               INTEGER PRIMARY KEY,
    concurso_id      INTEGER NOT NULL REFERENCES concurso(id),
    tipo             TEXT NOT NULL,      -- prova | prova_com_gabarito | gabarito_preliminar | gabarito_definitivo
                                         -- | justificativa | padrao_resposta | edital | edital_abertura | outro
    modalidade       TEXT,               -- objetiva | discursiva | NULL
    revisar          INTEGER NOT NULL DEFAULT 0,
    motivo_revisao   TEXT,
    acessibilidade   INTEGER NOT NULL DEFAULT 0,  -- adaptada/superampliada/ledor/braille/vlibras/txt
    versao           TEXT,               -- atualizado | sem_efeito | NULL
    cargo            TEXT,
    caderno          TEXT,               -- cor/nome/tipo do caderno, quando houver
    codigo_prova     TEXT,               -- ex.: 947_CAPES_001_01
    bloco            TEXT,               -- CB1 | CG1 | 001 | DISC ...
    descricao        TEXT,
    nome_arquivo     TEXT NOT NULL,
    extensao         TEXT,
    lista_origem     TEXT,               -- edital | gabarito
    data_publicacao  TEXT,               -- ISO (dataArquivoObj) ou NULL quando inválida
    url              TEXT NOT NULL UNIQUE,
    arquivo_local    TEXT,
    sha256           TEXT,
    tamanho          INTEGER,
    http_status      INTEGER,
    baixado_em       TEXT,
    visto_em         TEXT,
    removido_do_site INTEGER NOT NULL DEFAULT 0
);
CREATE INDEX IF NOT EXISTS ix_doc_concurso ON documento(concurso_id, tipo);
CREATE INDEX IF NOT EXISTS ix_doc_codigo ON documento(concurso_id, codigo_prova);

CREATE TABLE IF NOT EXISTS prova (
    id              INTEGER PRIMARY KEY,
    concurso_id     INTEGER NOT NULL REFERENCES concurso(id),
    documento_id    INTEGER NOT NULL UNIQUE REFERENCES documento(id),
    codigo_prova    TEXT,
    bloco           TEXT,
    cargo           TEXT,
    caderno         TEXT,
    ano             INTEGER,
    data_aplicacao  TEXT,
    banca           TEXT NOT NULL DEFAULT 'Cebraspe',
    tipo            TEXT,               -- CE | ME | DISC | misto
    extracao_status TEXT,               -- completa | parcial | falhou
    n_itens         INTEGER,
    n_gabarito      INTEGER,
    avisos          TEXT
);
CREATE INDEX IF NOT EXISTS ix_prova_ano ON prova(ano);

CREATE TABLE IF NOT EXISTS prova_cargo (
    prova_id INTEGER NOT NULL REFERENCES prova(id) ON DELETE CASCADE,
    cargo    TEXT NOT NULL,
    PRIMARY KEY (prova_id, cargo)
);

CREATE TABLE IF NOT EXISTS texto_base (
    id        INTEGER PRIMARY KEY,
    prova_id  INTEGER NOT NULL REFERENCES prova(id) ON DELETE CASCADE,
    rotulo    TEXT,
    tipo      TEXT,                      -- texto | comando
    faixa_ini INTEGER,
    faixa_fim INTEGER,
    conteudo  TEXT NOT NULL,
    imagens   TEXT,                      -- JSON: lista de caminhos relativos
    pagina    INTEGER
);

CREATE TABLE IF NOT EXISTS questao (
    id                INTEGER PRIMARY KEY,
    prova_id          INTEGER NOT NULL REFERENCES prova(id) ON DELETE CASCADE,
    numero            INTEGER NOT NULL,
    tipo              TEXT NOT NULL CHECK (tipo IN ('CE','ME','DISC')),
    texto_base_id     INTEGER REFERENCES texto_base(id),
    enunciado         TEXT NOT NULL,
    alternativas_json TEXT,
    codigo_item       TEXT,
    disciplina        TEXT,
    assunto           TEXT,
    imagens           TEXT,
    secao             TEXT,              -- marcador de bloco da prova ("CONHECIMENTOS BÁSICOS" ...)
    origem_texto      TEXT NOT NULL DEFAULT 'pdf',  -- pdf | ocr
    pagina            INTEGER,
    UNIQUE (prova_id, numero, tipo)
);

CREATE TABLE IF NOT EXISTS gabarito (
    id                  INTEGER PRIMARY KEY,
    questao_id          INTEGER NOT NULL UNIQUE REFERENCES questao(id) ON DELETE CASCADE,
    resposta_preliminar TEXT,
    resposta_definitiva TEXT,
    anulada             INTEGER NOT NULL DEFAULT 0,
    alterada            INTEGER NOT NULL DEFAULT 0,
    justificativa       TEXT,
    padrao_resposta     TEXT,             -- discursivas: padrão de resposta publicado
    fonte_preliminar    INTEGER REFERENCES documento(id),
    fonte_definitiva    INTEGER REFERENCES documento(id),
    fonte_justificativa INTEGER REFERENCES documento(id),
    fonte_padrao        INTEGER REFERENCES documento(id)
);

-- Respostas lidas dos gabaritos antes do vínculo com as questões (permite reprocessar o vínculo).
CREATE TABLE IF NOT EXISTS gabarito_bruto (
    documento_id INTEGER NOT NULL REFERENCES documento(id) ON DELETE CASCADE,
    grupo        INTEGER NOT NULL DEFAULT 0,  -- um PDF pode trazer vários gabaritos (cadernos/cargos)
    codigo_prova TEXT,
    caderno      TEXT,
    cargo        TEXT,
    fase         TEXT NOT NULL,          -- preliminar | definitivo
    numero       INTEGER NOT NULL,
    resposta     TEXT NOT NULL,          -- C | E | A..E | X
    PRIMARY KEY (documento_id, grupo, numero)
);

CREATE TABLE IF NOT EXISTS gabarito_grupo (
    documento_id   INTEGER NOT NULL REFERENCES documento(id) ON DELETE CASCADE,
    grupo          INTEGER NOT NULL,
    codigo_prova   TEXT,
    caderno        TEXT,
    cargo          TEXT,
    fase           TEXT NOT NULL,
    data_edital    TEXT,
    data_aplicacao TEXT,
    n              INTEGER,
    origem         TEXT,                 -- pdf | ocr | embutido
    PRIMARY KEY (documento_id, grupo)
);

-- Linhas das tabelas de justificativas de alteração/anulação.
CREATE TABLE IF NOT EXISTS justificativa_bruta (
    documento_id INTEGER NOT NULL REFERENCES documento(id) ON DELETE CASCADE,
    secao        TEXT,
    ordem        INTEGER NOT NULL,
    numero       INTEGER NOT NULL,
    preliminar   TEXT,
    definitiva   TEXT,                   -- X quando anulada
    situacao     TEXT,
    texto        TEXT,
    PRIMARY KEY (documento_id, ordem)
);

CREATE TABLE IF NOT EXISTS pendencia (
    id            INTEGER PRIMARY KEY,
    concurso_id   INTEGER REFERENCES concurso(id),
    documento_id  INTEGER REFERENCES documento(id),
    etapa         TEXT NOT NULL,         -- crawl | ano | classificacao | download | extracao | gabarito | validacao
    motivo        TEXT NOT NULL,
    criado_em     TEXT NOT NULL,
    resolvido_em  TEXT,
    UNIQUE (concurso_id, documento_id, etapa, motivo)
);

CREATE TABLE IF NOT EXISTS checkpoint (
    etapa         TEXT NOT NULL,
    chave         TEXT NOT NULL,
    status        TEXT NOT NULL,
    detalhe       TEXT,
    atualizado_em TEXT NOT NULL,
    PRIMARY KEY (etapa, chave)
);

CREATE VIRTUAL TABLE IF NOT EXISTS questao_fts USING fts5(
    questao_id UNINDEXED, enunciado, texto_base, tokenize='unicode61 remove_diacritics 2'
);
"""

# Índice pedido na especificação: (concurso, cargo, caderno, numero) — via view materializada em índices.
EXTRA = r"""
CREATE INDEX IF NOT EXISTS ix_prova_chave ON prova(concurso_id, cargo, caderno);
CREATE INDEX IF NOT EXISTS ix_questao_num ON questao(prova_id, numero);
"""


def agora() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def conectar(path: Path | str | None = None) -> sqlite3.Connection:
    path = Path(path or config.DB_PATH)
    path.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(path)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA journal_mode=WAL")
    _migra(con)
    con.executescript(SCHEMA + EXTRA)
    return con


def _migra(con) -> None:
    """Tabelas derivadas (recriáveis) com definição antiga são descartadas antes de aplicar o esquema."""
    def cols(t):
        return {r[1] for r in con.execute(f"PRAGMA table_info({t})")}
    existentes = {r[0] for r in con.execute("SELECT name FROM sqlite_master")}
    if "concurso" in existentes:
        for c in ("data_edital_pdf", "data_aplicacao"):
            if c not in cols("concurso"):
                con.execute(f"ALTER TABLE concurso ADD COLUMN {c} TEXT")
    derivadas = {"gabarito_bruto": "grupo", "questao": "secao", "gabarito": "padrao_resposta",
                 "texto_base": "tipo", "prova": "avisos", "questao_fts": "questao_id"}
    for t, c in derivadas.items():
        if t in existentes and c not in cols(t):
            con.execute(f"DROP TABLE {t}")
    con.commit()


def pendencia(con, etapa: str, motivo: str, concurso_id=None, documento_id=None) -> None:
    con.execute(
        "INSERT OR IGNORE INTO pendencia(concurso_id, documento_id, etapa, motivo, criado_em) VALUES (?,?,?,?,?)",
        (concurso_id, documento_id, etapa, motivo, agora()),
    )
    # reabre se havia sido resolvida e voltou a ocorrer
    con.execute(
        "UPDATE pendencia SET resolvido_em=NULL WHERE concurso_id IS ? AND documento_id IS ? AND etapa=? AND motivo=?",
        (concurso_id, documento_id, etapa, motivo),
    )


def resolver_pendencias(con, etapa: str, concurso_id=None, documento_id=None, prefixo: str = "") -> None:
    con.execute(
        "UPDATE pendencia SET resolvido_em=? WHERE resolvido_em IS NULL AND etapa=? AND concurso_id IS ? "
        "AND documento_id IS ? AND motivo LIKE ?",
        (agora(), etapa, concurso_id, documento_id, prefixo + "%"),
    )


def checkpoint(con, etapa: str, chave: str, status: str, detalhe: str | None = None) -> None:
    con.execute(
        "INSERT INTO checkpoint(etapa, chave, status, detalhe, atualizado_em) VALUES (?,?,?,?,?) "
        "ON CONFLICT(etapa, chave) DO UPDATE SET status=excluded.status, detalhe=excluded.detalhe, "
        "atualizado_em=excluded.atualizado_em",
        (etapa, chave, status, detalhe, agora()),
    )
