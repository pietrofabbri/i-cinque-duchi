"""Variante di `miniature.py` per il computer di Pietro, dove il limite di
Commons è più largo: due download in parallelo, a blocchi di trenta salvati
subito, e un tempo massimo per chiamata (la shell remota chiude i processi dopo
tre minuti). Si rilancia finché ogni lingua è completa; riparte da dove era.

Uso (nella cartella con miniature.py e immagini_oggetti.json):
    python3 parallelo.py 140 IT      # 140 secondi, solo l'italiano
"""
import base64, json, os, sys, time, concurrent.futures as cf
import miniature as m
risultati = json.load(open(m.ESITO, encoding="utf-8"))["risultati"]
os.makedirs(m.USCITA, exist_ok=True)
per = {}
for r in risultati:
    for c in r["candidati"]:
        per.setdefault(r["lingua"], set()).add(c["file"])
fine = time.time() + float(sys.argv[1] if len(sys.argv) > 1 else 120)
def scarica(u):
    import urllib.request, urllib.error
    for k in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": m.UA}), timeout=20) as f:
                return f.read(), f.headers.get("Content-Type", "")
        except urllib.error.HTTPError as e:
            if e.code == 429 and time.time() < fine:
                time.sleep(3 * (k + 1)); continue
            return None, str(e)
        except Exception as e:
            return None, str(e)
    return None, "429"
solo = sys.argv[2:]
for lingua, titoli in sorted(per.items()):
    if solo and lingua not in solo: continue
    p = os.path.join(m.USCITA, lingua + ".json")
    fatte = json.load(open(p)) if os.path.exists(p) else {}
    mancano = sorted(t for t in titoli if t not in fatte)
    if not mancano:
        print(lingua, "completa", len(fatte), "/", len(titoli)); continue
    errori = 0
    for i in range(0, len(mancano), 30):
        if time.time() > fine: break
        blocco = mancano[i:i+30]
        url = m.indirizzi(blocco)
        with cf.ThreadPoolExecutor(2) as ex:
            for t, (c, ty) in zip(blocco, ex.map(lambda t: scarica(url[t]) if t in url else (None, "senza url"), blocco)):
                if c: fatte[t] = "data:%s;base64,%s" % ((ty.split(";")[0] or "image/jpeg"), base64.b64encode(c).decode())
                else: errori += 1
        json.dump(fatte, open(p, "w"))
    print(lingua, len(fatte), "/", len(titoli), "errori", errori, flush=True)
    if time.time() > fine: break
