// Simulador CEBRASPE — Worker da Cloudflare.
// Todo pedido passa primeiro por aqui (assets.run_worker_first): sem o login do Cloudflare Access
// válido e um e-mail permitido, nada é servido, nem as questões nem as imagens.

const CERTS_TTL_MS = 60 * 60 * 1000;
let certsCache = { em: 0, dominio: "", chaves: new Map() };

function b64url(s) {
  s = s.replace(/-/g, "+").replace(/_/g, "/");
  while (s.length % 4) s += "=";
  return Uint8Array.from(atob(s), (c) => c.charCodeAt(0));
}

function lerJson(parte) {
  return JSON.parse(new TextDecoder().decode(b64url(parte)));
}

async function chavesAccess(dominio, forcar = false) {
  if (!forcar && certsCache.dominio === dominio && Date.now() - certsCache.em < CERTS_TTL_MS) {
    return certsCache.chaves;
  }
  const r = await fetch(`${dominio}/cdn-cgi/access/certs`);
  if (!r.ok) throw new Error(`certs ${r.status}`);
  const { keys = [] } = await r.json();
  const chaves = new Map();
  for (const jwk of keys) {
    const k = await crypto.subtle.importKey("jwk", jwk, { name: "RSASSA-PKCS1-v1_5", hash: "SHA-256" }, false, ["verify"]);
    chaves.set(jwk.kid, k);
  }
  certsCache = { em: Date.now(), dominio, chaves };
  return chaves;
}

function cookie(request, nome) {
  const c = request.headers.get("cookie") || "";
  const m = c.match(new RegExp(`(?:^|;\\s*)${nome}=([^;]+)`));
  return m ? m[1] : null;
}

// Devolve o e-mail autenticado, ou null.
export async function autenticar(request, env) {
  if (env.DEV_SEM_LOGIN === "1") return "dev@local";
  const dominio = (env.TEAM_DOMAIN || "").replace(/\/+$/, "");
  const aud = env.POLICY_AUD || "";
  const permitidos = (env.EMAILS_PERMITIDOS || "").toLowerCase().split(",").map((s) => s.trim()).filter(Boolean);
  if (!dominio || !aud || !permitidos.length) return null; // configuração incompleta: bloqueia

  const token = request.headers.get("cf-access-jwt-assertion") || cookie(request, "CF_Authorization");
  if (!token) return null;
  const partes = token.split(".");
  if (partes.length !== 3) return null;
  let cab, carga;
  try {
    cab = lerJson(partes[0]);
    carga = lerJson(partes[1]);
  } catch {
    return null;
  }
  if (cab.alg !== "RS256") return null;

  let chaves = await chavesAccess(dominio);
  if (!chaves.has(cab.kid)) chaves = await chavesAccess(dominio, true); // rotação de chaves
  const chave = chaves.get(cab.kid);
  if (!chave) return null;
  const ok = await crypto.subtle.verify("RSASSA-PKCS1-v1_5", chave, b64url(partes[2]),
    new TextEncoder().encode(`${partes[0]}.${partes[1]}`));
  if (!ok) return null;

  const agora = Math.floor(Date.now() / 1000);
  const auds = Array.isArray(carga.aud) ? carga.aud : [carga.aud];
  if (!auds.includes(aud)) return null;
  if (carga.iss && carga.iss.replace(/\/+$/, "") !== dominio) return null;
  if (!carga.exp || carga.exp < agora) return null;
  if (carga.nbf && carga.nbf > agora + 60) return null;
  const email = String(carga.email || "").toLowerCase();
  return permitidos.includes(email) ? email : null;
}

const json = (dados, status = 200) =>
  new Response(JSON.stringify(dados), {
    status,
    headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store" },
  });

async function api(request, env, url, email) {
  const db = env.DB;
  if (url.pathname === "/api/eu") return json({ email });

  if (url.pathname === "/api/historico" && request.method === "GET") {
    // última resposta de cada questão: [questao_id, acertou(0/1/null), marcada]
    const { results } = await db
      .prepare(
        `SELECT questao_id, acertou, marcada FROM resposta r
         WHERE id = (SELECT MAX(id) FROM resposta WHERE questao_id = r.questao_id)`
      )
      .all();
    return json(results.map((r) => [r.questao_id, r.acertou, r.marcada]));
  }

  if (url.pathname === "/api/respostas" && request.method === "POST") {
    let corpo;
    try {
      corpo = await request.json();
    } catch {
      return json({ erro: "json inválido" }, 400);
    }
    const lista = Array.isArray(corpo) ? corpo : [corpo];
    const validas = lista
      .filter((r) => Number.isInteger(r.questao_id) && r.questao_id > 0)
      .slice(0, 200)
      .map((r) => ({
        q: r.questao_id,
        m: r.marcada == null ? null : String(r.marcada).slice(0, 4),
        a: r.acertou === true || r.acertou === 1 ? 1 : r.acertou === false || r.acertou === 0 ? 0 : null,
      }));
    if (!validas.length) return json({ gravadas: 0 });
    const st = db.prepare("INSERT INTO resposta (questao_id, marcada, acertou, em) VALUES (?, ?, ?, ?)");
    const em = new Date().toISOString();
    await db.batch(validas.map((v) => st.bind(v.q, v.m, v.a, em)));
    return json({ gravadas: validas.length });
  }

  return json({ erro: "não encontrado" }, 404);
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    let email;
    try {
      email = await autenticar(request, env);
    } catch (e) {
      return new Response("Falha ao validar o login.", { status: 503 });
    }
    if (!email) {
      return new Response("Acesso restrito. Entre pelo login do Cloudflare Access.", {
        status: 403,
        headers: { "content-type": "text/plain; charset=utf-8" },
      });
    }
    if (url.pathname.startsWith("/api/")) return api(request, env, url, email);

    const resp = await env.ASSETS.fetch(request);
    // conteúdo privado: o navegador pode guardar, proxies/CDN compartilhados não
    const h = new Headers(resp.headers);
    const imutavel = url.pathname.startsWith("/img/");
    h.set("cache-control", imutavel ? "private, max-age=604800" : "private, no-cache");
    return new Response(resp.body, { status: resp.status, headers: h });
  },
};
