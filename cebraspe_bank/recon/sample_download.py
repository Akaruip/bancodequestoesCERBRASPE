import json,os,sys,time,urllib.request,urllib.parse,hashlib
UA="cebraspe-bank/0.1 (estudo pessoal; crawler educacional)"
R=sys.argv[1]; items=[l.split() for l in sys.argv[2:]]
want=[("INSS_2015","234INSS_001_01_Caderno_LUA.PDF"),("INSS_2015","Gab_Definitivo_234INSS_001_01.PDF"),
("SEE_16_DF","291_SEEDF_007_01.pdf"),("SEE_16_DF","Gab_Definitivo_291_SEEDF_007_01.pdf"),
("ABIN_17","378_ABIN_CB1_01.PDF"),("ABIN_17","GAB_DEFINITIVO_378_ABIN_CB1_01.PDF"),("ABIN_17","ABIN_17_PADR__O_DEFINITIVO_CARGO_1.PDF"),
("TRE_BA_17","TRE_BA_17_JUSTIFICATIVAS_DE_ALTERA____O_DE_GABARITO.PDF"),
("SEED_PR_20_PROFESSOR","566_SEED_001_01.PDF"),("SEED_PR_20_PROFESSOR","GAB_DEFINITIVO_566_SEED_001_01.PDF"),
("TELEBRAS_21","657_TELEBRAS_CB1_01.PDF"),("TELEBRAS_21","GAB_PRELIMINAR_657_TELEBRAS_CB1_01.PDF"),
("CAPES_23","947_CAPES_001_01.PDF"),("CAPES_23","GAB_DEFINITIVO_947_CAPES_001_01.PDF"),("CAPES_23","947_CAPES_001_DISC.PDF"),
("CAESB_24","MATRIZ_039_CAESB_CG1_00_Com Justificativas_atualizado.pdf"),("CAESB_24","Gab_Definitivo_MATRIZ_039_CAESB_CG1_00.pdf"),
("AGSUS_25_CCE","5B0C591D4033C261FC602C2A3E48D29E9DC447ECB4A2845D17E7652B2B8A7100.pdf")]
for s,n in want:
    d=json.load(open(f"{R}/all_det/{s}.json"))
    names={x["nomeArquivo"] for x in (d["arquivosGabarito"] or [])+(d["arquivosEdital"] or [])}
    if n not in names: print("NAO LISTADO",s,n); continue
    os.makedirs(f"{R}/pdfs/{s}",exist_ok=True); p=f"{R}/pdfs/{s}/{n}"
    if os.path.exists(p): continue
    u=f"https://cdn.cebraspe.org.br/concursos/{s}/arquivos/"+urllib.parse.quote(n)
    time.sleep(1)
    try:
        with urllib.request.urlopen(urllib.request.Request(u,headers={"User-Agent":UA}),timeout=120) as r: b=r.read(); ct=r.headers.get("Content-Type")
        open(p,"wb").write(b); print("OK",s,n,len(b),ct,hashlib.sha256(b).hexdigest()[:12])
    except Exception as e: print("ERR",s,n,e)
