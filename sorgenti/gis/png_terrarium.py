"""Il PNG di Terrarium, letto con la libreria standard.

Un tassello di elevazione è un PNG RGB a 8 bit con compressione zlib: si
decodifica in poche decine di righe, con i cinque filtri di riga che specifica
il formato (RFC 2083, §6.2). Non serve Pillow, e il progetto non installa
pacchetti per un controllo: è la stessa scelta già fatta per gli shapefile, dove
`shapefile_lettore.py` fa il lavoro di `pyshp` senza `pyshp`.

**Perché sta in un modulo suo e non dentro `rilievo.py`.** `rilievo_senza_pil.py`
importa `rilievo`, quindi se il codice di decodifica stesse dentro `rilievo.py`
i due si importerebbero a vicenda e l'import diventerebbe un trucco fragile: il
funzionamento dipenderebbe dall'ordine con cui i moduli vengono caricati. Un
modulo che non importa nessuno dei due elimina la questione, e lascia un solo
decodificatore per tutto il progetto.

Il valore di un pixel Terrarium è `quota = (R*256 + G + B/256) - 32768`, in
metri sopra il livello del mare.
"""
import struct
import zlib

ORIGINE = 32768.0


def decodifica_png(blob):
    """Un PNG in una griglia di triple (R, G, B), una riga per riga d'immagine."""
    if blob[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("non e' un PNG")
    i, idat, w, h, ct = 8, b"", None, None, None
    while i < len(blob):
        ln = struct.unpack(">I", blob[i:i + 4])[0]
        tipo = blob[i + 4:i + 8]
        dati = blob[i + 8:i + 8 + ln]
        i += 12 + ln
        if tipo == b"IHDR":
            w, h, _profondita, ct = struct.unpack(">IIBB", dati[:10])
            if _profondita != 8:
                raise ValueError("solo 8 bit per canale")
            if ct not in (0, 2, 4, 6):
                raise ValueError("tipo di pixel %d non previsto" % ct)
        elif tipo == b"IDAT":
            idat += dati
        elif tipo == b"IEND":
            break
    grezzo = zlib.decompress(idat)
    bpp = {0: 1, 2: 3, 4: 2, 6: 4}[ct]          # byte per pixel
    passo = w * bpp
    griglia, riga_prec, k = [], bytearray(passo), 0
    for _ in range(h):
        filtro = grezzo[k]
        k += 1
        riga = bytearray(grezzo[k:k + passo])
        k += passo
        # i cinque filtri di riga del formato PNG (RFC 2083, 6.2)
        for x in range(passo):
            a = riga[x - bpp] if x >= bpp else 0
            b = riga_prec[x]
            c = riga_prec[x - bpp] if x >= bpp else 0
            if filtro == 1:
                riga[x] = (riga[x] + a) & 255
            elif filtro == 2:
                riga[x] = (riga[x] + b) & 255
            elif filtro == 3:
                riga[x] = (riga[x] + ((a + b) >> 1)) & 255
            elif filtro == 4:
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                riga[x] = (riga[x] + (a if pa <= pb and pa <= pc
                                      else b if pb <= pc else c)) & 255
        griglia.append([(riga[i], riga[i + 1], riga[i + 2])
                        for i in range(0, passo, bpp)])
        riga_prec = riga
    return griglia


def quota_di(blob):
    """Le triple in metri: quello che l'algoritmo di rilievo calcola."""
    return [[(R * 256 + G + B / 256.0) - ORIGINE for (R, G, B) in riga]
            for riga in decodifica_png(blob)]