"""Configuração central: caminhos, rede e constantes do site."""
from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(os.environ.get("CEBRASPE_ROOT", Path(__file__).resolve().parent.parent))
DATA_DIR = Path(os.environ.get("CEBRASPE_DATA", ROOT / "data"))
RAW_DIR = DATA_DIR / "raw"          # PDFs: raw/{ano}/{slug}/{nome_original}
API_DIR = DATA_DIR / "api"          # respostas JSON cruas da API (auditoria)
IMG_DIR = DATA_DIR / "img"          # recortes de imagens/tabelas das provas
DB_PATH = Path(os.environ.get("CEBRASPE_DB", DATA_DIR / "cebraspe.db"))

USER_AGENT = "cebraspe-bank/0.1 (estudo pessoal; crawler educacional; 1 req/s)"
MIN_INTERVAL_S = 1.0     # no máximo 1 requisição por segundo, somando todos os hosts
MAX_RETRIES = 5
TIMEOUT_S = 120

API_BASE = "https://apis.cebraspe.org.br/cebraspe/"
LISTA_CONCURSOS = API_BASE + "eventos/tipo/concursos/"
DETALHE_EVENTO = API_BASE + "eventos/{slug}"
CDN_BASE = "https://cdn.cebraspe.org.br/"
SITE_CONCURSO = "https://www.cebraspe.org.br/concursos/{slug}"
