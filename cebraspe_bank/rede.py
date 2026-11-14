"""Cliente HTTP com limite global de 1 req/s, retry com backoff exponencial e robots.txt."""
from __future__ import annotations

import logging
import time
import urllib.robotparser
from dataclasses import dataclass
from urllib.parse import urlsplit

import requests

from . import config

log = logging.getLogger(__name__)


@dataclass
class Resposta:
    url: str
    status: int
    content: bytes
    content_type: str | None


class Cliente:
    def __init__(self, min_interval: float = config.MIN_INTERVAL_S, max_retries: int = config.MAX_RETRIES):
        self.s = requests.Session()
        self.s.headers["User-Agent"] = config.USER_AGENT
        self.min_interval = min_interval
        self.max_retries = max_retries
        self._ultimo = 0.0
        self._robots: dict[str, urllib.robotparser.RobotFileParser | None] = {}
        self.n_requisicoes = 0

    def _espera(self) -> None:
        dt = time.monotonic() - self._ultimo
        if dt < self.min_interval:
            time.sleep(self.min_interval - dt)
        self._ultimo = time.monotonic()

    def _permitido(self, url: str) -> bool:
        p = urlsplit(url)
        base = f"{p.scheme}://{p.netloc}"
        if base not in self._robots:
            rp = urllib.robotparser.RobotFileParser()
            try:
                self._espera()
                self.n_requisicoes += 1
                r = self.s.get(base + "/robots.txt", timeout=30)
                if r.status_code == 200 and "text/plain" in r.headers.get("Content-Type", ""):
                    rp.parse(r.text.splitlines())
                    self._robots[base] = rp
                else:
                    self._robots[base] = None  # sem robots.txt válido => sem restrições
            except requests.RequestException:
                self._robots[base] = None
        rp = self._robots[base]
        return True if rp is None else rp.can_fetch(config.USER_AGENT, url)

    def get(self, url: str, retry_status=(429, 500, 502, 503, 504)) -> Resposta:
        if not self._permitido(url):
            raise PermissionError(f"robots.txt não permite: {url}")
        ultimo_erro: Exception | None = None
        status = 0
        corpo = b""
        for tentativa in range(self.max_retries):
            if tentativa:
                atraso = min(60.0, 2.0 ** tentativa)
                log.info("retry %d em %.0fs: %s", tentativa, atraso, url)
                time.sleep(atraso)
            self._espera()
            self.n_requisicoes += 1
            try:
                r = self.s.get(url, timeout=config.TIMEOUT_S)
            except requests.RequestException as e:
                ultimo_erro = e
                continue
            status = r.status_code
            corpo = r.content
            if status in retry_status:
                ra = r.headers.get("Retry-After")
                if ra and ra.isdigit():
                    time.sleep(min(int(ra), 120))
                ultimo_erro = None
                continue
            return Resposta(url, status, r.content, r.headers.get("Content-Type"))
        if ultimo_erro is not None and status == 0:
            raise ultimo_erro
        return Resposta(url, status, corpo, None)
