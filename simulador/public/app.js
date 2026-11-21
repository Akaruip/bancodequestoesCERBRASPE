"use strict";
// Simulador CEBRASPE — interface. As questões vêm de /dados (arquivos estáticos gerados por exportar.py);
// o histórico de respostas fica no D1, via /api.

const $ = (s) => document.querySelector(s);
const TELAS = ["carregando", "filtros", "questao", "resultado"];
const FILA_KEY = "sim.fila";       // respostas ainda não enviadas (sem internet)
const FILTROS_KEY = "sim.filtros";
const NOMES_BLOCO = {
  basicos: "Conhecimentos básicos", gerais: "Conhecimentos gerais", especificos: "Conhecimentos específicos",
  complementares: "Conhecimentos complementares", especializados: "Conhecimentos especializados",
  discursiva: "Discursiva", objetiva: "Prova objetiva (sem bloco)", "": "Sem bloco",
};

let CAT = null;            // catálogo
let POS = new Map();       // questao_id -> posição no catálogo
let HIST = new Map();      // questao_id -> {a: acertou 0/1/null, m: marcada}
const blocos = new Map();  // cache de /dados/q/N.json
let sim = null;            // simulado em andamento

function mostrar(nome) {
  for (const t of TELAS) $(`#tela-${t}`).hidden = t !== nome;
  window.scrollTo(0, 0);
}

function esc(s) {
  return String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
}

function guardar(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch {} }
function ler(k, padrao) { try { const v = localStorage.getItem(k); return v ? JSON.parse(v) : padrao; } catch { return padrao; } }

async function pegarJson(url, opts) {
  const r = await fetch(url, { credentials: "same-origin", ...opts });
  if (r.status === 403 || r.redirected) throw new Error("login expirado: recarregue a página para entrar de novo");
  if (!r.ok) throw new Error(`${url}: ${r.status}`);
  return r.json();
}

// ---------- carga ----------
async function iniciar() {
  try {
    const [cat, hist] = await Promise.all([pegarJson("/dados/catalogo.json"), pegarJson("/api/historico").catch(() => [])]);
    CAT = cat;
    CAT.id.forEach((id, i) => POS.set(id, i));
    for (const [id, a, m] of hist) HIST.set(id, { a, m });
  } catch (e) {
    $("#tela-carregando").innerHTML = `<p class="centro">Não consegui carregar o banco: ${esc(e.message)}</p>`;
    return;
  }
  enviarFila();
  montarFiltros();
  mostrar("filtros");
}

function montarFiltros() {
  const contaDisc = new Map(), contaOrg = new Map();
  for (let i = 0; i < CAT.id.length; i++) {
    contaDisc.set(CAT.disc[i], (contaDisc.get(CAT.disc[i]) || 0) + 1);
    contaOrg.set(CAT.org[i], (contaOrg.get(CAT.org[i]) || 0) + 1);
  }
  const opcoes = (lista, conta) => [...conta.entries()]
    .filter(([i]) => lista[i])
    .sort((a, b) => b[1] - a[1])
    .map(([i, n]) => `<option value="${esc(lista[i])}">${n} questões</option>`).join("");
  $("#lista-disc").innerHTML = opcoes(CAT.disciplinas, contaDisc);
  $("#lista-org").innerHTML = opcoes(CAT.orgaos, contaOrg);
  $("#f-bloco").innerHTML = `<option value="">Todos</option>` +
    CAT.blocos.map((b, i) => `<option value="${i}">${esc(NOMES_BLOCO[b] ?? b)}</option>`).join("");

  const f = ler(FILTROS_KEY, null);
  if (f) {
    $("#f-disc").value = f.disc || ""; $("#f-org").value = f.org || "";
    $("#f-ano-de").value = f.de || ""; $("#f-ano-ate").value = f.ate || "";
    $("#f-bloco").value = f.bloco ?? ""; $("#f-hist").value = f.hist || "novas";
    $("#f-anul").checked = !!f.anul; $("#f-qtd").value = String(f.qtd || 20);
    document.querySelectorAll("input[name=tipo]").forEach((c) => { c.checked = (f.tipos || ["CE", "ME"]).includes(c.value); });
  }
  document.querySelectorAll("#tela-filtros input, #tela-filtros select").forEach((el) => el.addEventListener("input", contar));
  contar();
  estatisticas();
}

function lerFiltros() {
  return {
    disc: $("#f-disc").value.trim(), org: $("#f-org").value.trim(),
    de: parseInt($("#f-ano-de").value) || null, ate: parseInt($("#f-ano-ate").value) || null,
    bloco: $("#f-bloco").value, hist: $("#f-hist").value, anul: $("#f-anul").checked,
    qtd: parseInt($("#f-qtd").value) || 20,
    tipos: [...document.querySelectorAll("input[name=tipo]:checked")].map((c) => c.value),
  };
}

// Posições do catálogo que passam nos filtros.
function filtrar(f) {
  const iDisc = f.disc ? CAT.disciplinas.indexOf(f.disc) : -1;
  const iOrg = f.org ? CAT.orgaos.indexOf(f.org) : -1;
  if ((f.disc && iDisc < 0) || (f.org && iOrg < 0)) return [];
  const bloco = f.bloco === "" ? -1 : parseInt(f.bloco);
  const tipos = new Set(f.tipos);
  const out = [];
  for (let i = 0; i < CAT.id.length; i++) {
    if (!tipos.has(CAT.tipo[i])) continue;
    if (iDisc >= 0 && CAT.disc[i] !== iDisc) continue;
    if (iOrg >= 0 && CAT.org[i] !== iOrg) continue;
    if (bloco >= 0 && CAT.bloco[i] !== bloco) continue;
    if (f.de && CAT.ano[i] < f.de) continue;
    if (f.ate && CAT.ano[i] > f.ate) continue;
    if (!f.anul && CAT.anul[i]) continue;
    if (f.hist !== "todas") {
      const h = HIST.get(CAT.id[i]);
      if (f.hist === "novas" && h) continue;
      if (f.hist === "erradas" && !(h && h.a === 0)) continue;
    }
    out.push(i);
  }
  return out;
}

function contar() {
  const f = lerFiltros();
  const n = filtrar(f).length;
  $("#f-contagem").textContent = `${n.toLocaleString("pt-BR")} questões com esses filtros.`;
  $("#btn-comecar").disabled = n === 0;
}

function estatisticas() {
  if (!HIST.size) return;
  let ac = 0, er = 0;
  const porDisc = new Map();
  for (const [id, h] of HIST) {
    if (h.a == null) continue;
    h.a ? ac++ : er++;
    const p = POS.get(id);
    const d = p == null ? "" : CAT.disciplinas[CAT.disc[p]] || "Sem disciplina";
    const s = porDisc.get(d) || [0, 0];
    s[h.a ? 0 : 1]++;
    porDisc.set(d, s);
  }
  const tot = ac + er;
  const linhas = [...porDisc.entries()].sort((a, b) => (b[1][0] + b[1][1]) - (a[1][0] + a[1][1])).slice(0, 15)
    .map(([d, [a, e]]) => `<tr><td>${esc(d)}</td><td class="num">${a + e}</td><td class="num">${Math.round(100 * a / (a + e))}%</td></tr>`).join("");
  $("#estatisticas").innerHTML = `
    <div class="placar">
      <div><strong>${HIST.size.toLocaleString("pt-BR")}</strong>respondidas</div>
      <div><strong>${tot ? Math.round(100 * ac / tot) : 0}%</strong>de acerto</div>
    </div>
    <table><tr><th>Disciplina</th><th class="num">Feitas</th><th class="num">Acerto</th></tr>${linhas}</table>`;
}

// ---------- simulado ----------
function sortear(lista, n) {
  const a = lista.slice();
  for (let i = 0; i < Math.min(n, a.length); i++) {
    const j = i + Math.floor(Math.random() * (a.length - i));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a.slice(0, n);
}

async function carregarBloco(n) {
  if (!blocos.has(n)) blocos.set(n, pegarJson(`/dados/q/${n}.json`));
  return blocos.get(n);
}

async function questaoNaPos(p) {
  const b = await carregarBloco(Math.floor(p / CAT.tam_bloco));
  const id = CAT.id[p];
  const q = b.q.find((x) => x.id === id);
  return { q, texto: q && q.t ? b.t[q.t] : null };
}

async function comecar() {
  const f = lerFiltros();
  guardar(FILTROS_KEY, f);
  const posicoes = sortear(filtrar(f), f.qtd);
  sim = { posicoes, i: 0, respostas: [] };
  await exibir();
}

function imagens(lista) {
  if (!lista || !lista.length) return "";
  return `<div class="imagens">${lista.map((p) =>
    `<img loading="lazy" alt="Figura da questão" src="/img/${p.split("/").map(encodeURIComponent).join("/")}">`).join("")}</div>`;
}

async function exibir() {
  mostrar("questao");
  const p = sim.posicoes[sim.i];
  $("#questao").innerHTML = `<p class="discreto">Carregando…</p>`;
  $("#acoes").innerHTML = "";
  $("#barra").style.width = `${(100 * sim.i) / sim.posicoes.length}%`;
  $("#topo-info").textContent = `${sim.i + 1} de ${sim.posicoes.length}`;
  let dados;
  try {
    dados = await questaoNaPos(p);
  } catch (e) {
    $("#questao").innerHTML = `<p>Não consegui carregar esta questão (${esc(e.message)}).</p>`;
    acoesSeguinte();
    return;
  }
  const { q, texto } = dados;
  sim.atual = q;
  const meta = [q.d, q.o || q.c, q.an, q.ca].filter(Boolean).map(esc).join(" · ");
  let html = `<div class="meta">${meta}${q.n ? ` · item ${q.n}` : ""}</div>`;
  if (q.v) html += `<div class="aviso">${esc(q.v)}</div>`;
  if (texto) {
    html += `<details open><summary>${esc(texto.r || "Texto de apoio")}</summary>
      <div class="texto-apoio">${esc(texto.c)}${imagens(texto.im)}</div></details>`;
  }
  html += `<div class="enunciado">${esc(q.e)}</div>${imagens(q.im)}`;
  if (q.tp === "ME") {
    const letras = q.a ? Object.keys(q.a) : ["A", "B", "C", "D", "E"];
    html += `<ul class="alternativas">${letras.map((l) =>
      `<li><button class="opcao" type="button" data-l="${esc(l)}"><b>${esc(l)}</b>${esc(q.a ? q.a[l] : "")}</button></li>`).join("")}</ul>`;
  }
  if (q.tp === "DISC") html += `<label class="campo">Sua resposta (opcional)<textarea id="disc-resp" rows="8" style="width:100%"></textarea></label>`;
  html += `<div id="feedback"></div>`;
  $("#questao").innerHTML = html;

  if (q.tp === "CE") {
    $("#acoes").innerHTML = `
      <button class="primario btn-certo" data-l="C" type="button">Certo</button>
      <button class="primario btn-errado" data-l="E" type="button">Errado</button>
      <button class="secundario" data-l="" type="button">Pular</button>`;
    $("#acoes").querySelectorAll("button").forEach((b) => b.addEventListener("click", () => responder(b.dataset.l || null)));
  } else if (q.tp === "ME") {
    $("#questao").querySelectorAll(".opcao").forEach((b) => b.addEventListener("click", () => responder(b.dataset.l)));
    $("#acoes").innerHTML = `<button class="secundario" type="button">Pular</button>`;
    $("#acoes button").addEventListener("click", () => responder(null));
  } else {
    $("#acoes").innerHTML = `<button class="primario" type="button">Ver padrão de resposta</button>`;
    $("#acoes button").addEventListener("click", () => responder(null));
  }
}

function responder(marcada) {
  const q = sim.atual;
  if (!q || sim.respondida === q.id) return;
  sim.respondida = q.id;
  let acertou = null, classe = "neutro", titulo;
  if (q.tp === "DISC") {
    titulo = "Padrão de resposta";
  } else if (q.x) {
    titulo = "Questão anulada pela banca";
  } else if (marcada == null) {
    titulo = `Em branco. Gabarito: ${rotulo(q, q.r)}`;
  } else {
    acertou = marcada === q.r;
    classe = acertou ? "ok" : "nok";
    titulo = acertou ? `Acertou! Gabarito: ${rotulo(q, q.r)}` : `Errou. Você marcou ${rotulo(q, marcada)}; gabarito: ${rotulo(q, q.r)}`;
  }
  if (q.tp === "ME") {
    $("#questao").querySelectorAll(".opcao").forEach((b) => {
      b.disabled = true;
      if (b.dataset.l === q.r) b.classList.add("certa");
      else if (b.dataset.l === marcada) b.classList.add("errada");
    });
  }
  let html = `<div class="feedback ${classe}"><strong>${esc(titulo)}</strong>`;
  if (q.pre) html += `<div class="aviso">Só há gabarito preliminar para esta prova.</div>`;
  if (q.alt) html += `<div class="aviso">O gabarito preliminar era ${esc(rotulo(q, q.alt))} e foi alterado.</div>`;
  if (q.j) html += `<details><summary>Justificativa da banca</summary><div class="justificativa">${esc(q.j)}</div></details>`;
  if (q.tp === "DISC") html += `<div class="justificativa">${esc(q.p || "A banca não publicou padrão de resposta para esta questão.")}</div>`;
  html += `</div>`;
  $("#feedback").innerHTML = html;
  $("#feedback").scrollIntoView({ behavior: "smooth", block: "nearest" });

  sim.respostas.push({ q, marcada, acertou });
  if (q.tp !== "DISC" && !q.x) {
    HIST.set(q.id, { a: acertou, m: marcada });
    enfileirar({ questao_id: q.id, marcada, acertou });
  }
  acoesSeguinte();
}

function rotulo(q, l) {
  if (q.tp === "CE") return l === "C" ? "Certo" : l === "E" ? "Errado" : String(l);
  return String(l);
}

function acoesSeguinte() {
  const ultima = sim.i >= sim.posicoes.length - 1;
  $("#acoes").innerHTML = `<button class="primario" type="button">${ultima ? "Ver resultado" : "Próxima"}</button>`;
  $("#acoes button").addEventListener("click", () => {
    if (ultima) return resultado();
    sim.i++;
    exibir();
  });
  // pré-carrega a próxima
  const prox = sim.posicoes[sim.i + 1];
  if (prox != null) carregarBloco(Math.floor(prox / CAT.tam_bloco)).catch(() => {});
}

function resultado() {
  mostrar("resultado");
  $("#topo-info").textContent = "";
  const r = sim.respostas;
  const ce = r.filter((x) => x.q.tp === "CE" && !x.q.x);
  const me = r.filter((x) => x.q.tp === "ME" && !x.q.x);
  const conta = (l) => ({ c: l.filter((x) => x.acertou === true).length, e: l.filter((x) => x.acertou === false).length, b: l.filter((x) => x.acertou == null).length });
  const a = conta(ce), m = conta(me);
  let html = `<h1>Resultado</h1><div class="placar">`;
  if (ce.length) html += `<div><strong>${a.c - a.e}</strong>nota líquida C/E<br><span class="discreto">${a.c} certas, ${a.e} erradas, ${a.b} em branco</span></div>`;
  if (me.length) html += `<div><strong>${m.c}/${me.length}</strong>múltipla escolha</div>`;
  html += `</div><p class="discreto">Na nota líquida do Cebraspe, cada item errado anula um certo; em branco não conta.</p>`;
  html += `<button class="primario" id="btn-novo" type="button">Novo simulado</button>`;
  $("#resultado").innerHTML = html;
  $("#btn-novo").addEventListener("click", voltar);
}

function voltar() {
  sim = null;
  $("#topo-info").textContent = "";
  contar();
  estatisticas();
  mostrar("filtros");
}

// ---------- envio do histórico (com fila para quando faltar internet) ----------
function enfileirar(item) {
  const fila = ler(FILA_KEY, []);
  fila.push(item);
  guardar(FILA_KEY, fila);
  enviarFila();
}

let enviando = false;
async function enviarFila() {
  if (enviando) return;
  const fila = ler(FILA_KEY, []);
  if (!fila.length) return;
  enviando = true;
  try {
    const lote = fila.slice(0, 200);
    await pegarJson("/api/respostas", { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify(lote) });
    guardar(FILA_KEY, ler(FILA_KEY, []).slice(lote.length));
  } catch {
    // fica na fila; tenta de novo na próxima resposta ou quando a conexão voltar
  } finally {
    enviando = false;
  }
}
window.addEventListener("online", enviarFila);

$("#btn-comecar").addEventListener("click", comecar);
$("#btn-inicio").addEventListener("click", () => { if (CAT) voltar(); });
iniciar();
