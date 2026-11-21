-- Histórico de respostas do simulador (único dado que fica no D1; as questões são arquivos estáticos).
CREATE TABLE IF NOT EXISTS resposta (
  id         INTEGER PRIMARY KEY AUTOINCREMENT,
  questao_id INTEGER NOT NULL,
  marcada    TEXT,
  acertou    INTEGER,
  em         TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS ix_resposta_questao ON resposta(questao_id, id);
