import json, os, sys, time, urllib.request, urllib.error
UA = "cebraspe-bank/0.1 (estudo pessoal; crawler educacional)"
R = sys.argv[1]
out = os.path.join(R, "all_det"); os.makedirs(out, exist_ok=True)
evs = [e for g in json.load(open(os.path.join(R, "all.json"))) for e in g["eventos"]]
slugs = sorted({e["eventoURL"] for e in evs})
log = open(os.path.join(R, "scan.log"), "a")
for s in slugs:
    p = os.path.join(out, s + ".json")
    if os.path.exists(p): continue
    status = None
    for att in range(4):
        time.sleep(1.0 * (2 ** att) if att else 1.0)
        try:
            req = urllib.request.Request(f"https://apis.cebraspe.org.br/cebraspe/eventos/{urllib.parse.quote(s)}", headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=60) as r:
                status = r.status; body = r.read()
            break
        except urllib.error.HTTPError as e:
            status = e.code; body = e.read()
            if e.code < 500: break
        except Exception as e:
            status = f"exc:{e}"; body = b""
    with open(p, "wb") as f: f.write(body)
    print(s, status, len(body), file=log, flush=True)
print("DONE", file=log, flush=True)
