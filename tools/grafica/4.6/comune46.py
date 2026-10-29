"""Blocco 4.6 — funzioni comuni: immagini di lotta e grafica delle transizioni a forma invariata (R-GFX-29).

Formati (letti nel repository, vedi 4.6 §2):
- immagini degli allenatori (files/a/0/5/8 fronte, files/a/0/0/6 dorso): cinque voci per classe
  (src/pokemon.c, sub_02070D3C): NCGR «a celle» con un blocco di 100 tile per fotogramma (trasferimento in VRAM),
  NCLR, NCER, NANR e un NCGR «scansionato» 160×80 cifrato, che la lotta mostra (PokepicManager): metà sinistra =
  fotogramma 0, metà destra = fotogramma 1 (vuota se la classe ha un solo fotogramma). La cifratura va
  dall'ultima parola alla prima («-encodebacktofront» di nitrogfx, come in Diamante e Perla): si tiene la
  chiave dell'originale e le ultime 4 colonne dell'ultima riga restano trasparenti.
- grafica delle transizioni (files/a/1/0/9): sprite OBJ a 4 bit con mappatura 1D da 32 KB (indice di tile =
  tile da 32 byte) disposti da una cella dell'NCER; sfondi con NSCR.
Tutto si riscrive cambiando solo pixel e colori: stessa lunghezza, stesse intestazioni. Solo libreria standard."""
import os
import struct
import sys

QUI = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(QUI, '..', '..', '..'))
sys.path.insert(0, os.path.join(PROJ, 'tools'))
sys.path.insert(0, os.path.join(QUI, '..', '4.4'))
sys.path.insert(0, os.path.join(QUI, '..', '4.5'))
import trinacria_gfx as G          # noqa: E402
import comune44 as C44             # noqa: E402
import comune45 as C45             # noqa: E402

OUT = os.path.join(PROJ, 'build', 'grafica', '4.6')
FRONTI = 'files/a/0/5/8'
DORSI = 'files/a/0/0/6'
TRANSIZIONI = 'files/a/1/0/9'
LATO = 80            # fotogramma degli allenatori 80×80
TILE_FOT = 100       # tile per fotogramma


class Errore(Exception):
    pass


def leggi(repo, rel):
    return G.read(os.path.join(repo, *rel.split('/')))


# ---------------------------------------------------------------------------------------------- NCGR

def _rahc(b):
    o = b.find(b'RAHC')
    if o < 0:
        raise Errore('NCGR senza blocco RAHC')
    return o


def ncgr_dati(b):
    o = _rahc(b)
    size = struct.unpack_from('<I', b, o + 0x18)[0]
    off = o + 8 + struct.unpack_from('<I', b, o + 0x1C)[0]
    return off, size


def ncgr_byte(b):
    off, size = ncgr_dati(b)
    return b[off:off + size]


def ncgr_con_byte(b, dati):
    off, size = ncgr_dati(b)
    if len(dati) != size:
        raise Errore('NCGR: %d byte di dati invece di %d' % (len(dati), size))
    out = bytearray(b)
    out[off:off + size] = dati
    return bytes(out)


def tile4(d):
    """byte a 4 bit -> lista di tile (8 righe di 8 indici, pixel di sinistra nel nibble basso)."""
    return [[[(d[k * 32 + y * 4 + x // 2] >> (4 * (x & 1))) & 15 for x in range(8)] for y in range(8)]
            for k in range(len(d) // 32)]


def byte4(tiles):
    out = bytearray()
    for t in tiles:
        for row in t:
            for x in range(0, 8, 2):
                if row[x] > 15 or row[x + 1] > 15:
                    raise Errore('indice oltre 15 in un NCGR a 4 bit')
                out.append(row[x] | (row[x + 1] << 4))
    return bytes(out)


# ---------------------------------------------------------------------------------------------- NCER

FORME = {(0, 0): (8, 8), (0, 1): (16, 16), (0, 2): (32, 32), (0, 3): (64, 64), (1, 0): (16, 8), (1, 1): (32, 8),
         (1, 2): (32, 16), (1, 3): (64, 32), (2, 0): (8, 16), (2, 1): (8, 32), (2, 2): (16, 32), (2, 3): (32, 64)}


def ncer_celle(b):
    """-> lista di celle; cella = lista di OAM dict(x, y, w, h, tile, hf, vf, pal)."""
    o = b.find(b'KBEC')
    if o < 0:
        raise Errore('NCER senza blocco KBEC')
    n, attr, off = struct.unpack_from('<HHI', b, o + 8)
    base = o + 8 + off
    sz = 16 if attr & 1 else 8
    celle = []
    for i in range(n):
        no, _, oo = struct.unpack_from('<HHI', b, base + i * sz)
        p = base + n * sz + oo
        oam = []
        for k in range(no):
            a0, a1, a2 = struct.unpack_from('<HHH', b, p + k * 6)
            y = a0 & 0xFF
            x = a1 & 0x1FF
            w, h = FORME[(a0 >> 14, a1 >> 14)]
            oam.append(dict(x=x - 512 if x >= 256 else x, y=y - 256 if y >= 128 else y, w=w, h=h, tile=a2 & 0x3FF,
                            hf=(a1 >> 12) & 1, vf=(a1 >> 13) & 1, pal=a2 >> 12))
        celle.append(oam)
    return celle


def cornice(cella):
    xs = [o['x'] for o in cella] + [o['x'] + o['w'] for o in cella]
    ys = [o['y'] for o in cella] + [o['y'] + o['h'] for o in cella]
    return min(xs), min(ys), max(xs) - min(xs), max(ys) - min(ys)


def immagine_da_cella(tiles, cella, base=0, passo=1):
    """Pixel (w×h, riga per riga) della cella; `passo` = tile per unità di indice (2 con la mappatura da 64 KB)."""
    x0, y0, W, H = cornice(cella)
    pix = [0] * (W * H)
    for o in cella:
        k = base + o['tile'] * passo
        for ty in range(o['h'] // 8):
            for tx in range(o['w'] // 8):
                t = tiles[k]
                k += 1
                for y in range(8):
                    for x in range(8):
                        xx, yy = tx * 8 + x, ty * 8 + y
                        if o['hf']:
                            xx = o['w'] - 1 - xx
                        if o['vf']:
                            yy = o['h'] - 1 - yy
                        pix[(o['y'] - y0 + yy) * W + o['x'] - x0 + xx] = t[y][x]
    return W, H, pix


def cella_da_immagine(tiles, cella, W, pix, base=0, passo=1):
    """Scrive in `tiles` (lista, cambiata sul posto) i pixel dell'immagine secondo le OAM della cella."""
    x0, y0, _, _ = cornice(cella)
    for o in cella:
        if o['hf'] or o['vf']:
            raise Errore('OAM capovolta: non prevista')
        k = base + o['tile'] * passo
        for ty in range(o['h'] // 8):
            for tx in range(o['w'] // 8):
                tiles[k] = [[pix[(o['y'] - y0 + ty * 8 + y) * W + o['x'] - x0 + tx * 8 + x] for x in range(8)]
                            for y in range(8)]
                k += 1


def passo_tile(ncgr):
    """Tile per unità di indice nelle OAM: mappatura 1D da 32 KB = 1, da 64 KB = 2 (campo mapping dell'NCGR)."""
    o = _rahc(ncgr)
    mapping = struct.unpack_from('<I', ncgr, o + 0x10)[0]
    return 1 << ((mapping >> 20) & 7)


# ------------------------------------------------------------------------------------ NCGR cifrato

def decifra(d):
    """-> (byte in chiaro, chiave) come nitrogfx con -encodebacktofront."""
    d = bytearray(d)
    n = len(d)
    enc = (d[n - 1] << 8) | d[n - 2]
    for i in range(n, 0, -2):
        v = ((d[i - 1] << 8) | d[i - 2]) ^ (enc & 0xFFFF)
        d[i - 1], d[i - 2] = v >> 8, v & 0xFF
        enc = (enc * 1103515245 + 24691) & 0xFFFFFFFF
    return bytes(d), enc


def cifra(d, chiave):
    d = bytearray(d)
    enc = chiave
    for i in range(1, len(d), 2):
        v = (d[i] << 8) | d[i - 1]
        enc = ((enc - 24691) * 4005161829) & 0xFFFFFFFF
        v ^= enc & 0xFFFF
        d[i], d[i - 1] = v >> 8, v & 0xFF
    return bytes(d)


def scansione_pixel(d):
    pix = []
    for b in d:
        pix += [b & 15, b >> 4]
    return pix


def pixel_scansione(pix):
    return bytes(pix[i] | (pix[i + 1] << 4) for i in range(0, len(pix), 2))


# ------------------------------------------------------------------------------- immagini di lotta

def allenatore(files, idx):
    """Legge le cinque voci della classe (o del dorso) idx -> dict."""
    f0, f1, f2, f3, f4 = files[idx * 5:idx * 5 + 5]
    for b, k in ((f0, 'NCGR'), (f1, 'NCLR'), (f2, 'NCER'), (f4, 'NCGR')):
        if G.kind(b) != k:
            raise Errore('voce %d: %s invece di %s' % (idx * 5, G.kind(b), k))
    tiles = tile4(ncgr_byte(f0))
    if len(tiles) % TILE_FOT:
        raise Errore('classe %d: %d tile, non multiplo di %d' % (idx, len(tiles), TILE_FOT))
    nf = len(tiles) // TILE_FOT
    celle = ncer_celle(f2)
    passo = passo_tile(f0)
    fot = []
    for k in range(nf):
        cella = celle[k] if k < len(celle) else celle[0]
        W, H, pix = immagine_da_cella(tiles, cella, base=k * TILE_FOT, passo=passo)
        if (W, H) != (LATO, LATO):
            raise Errore('classe %d fotogramma %d: %d×%d' % (idx, k, W, H))
        fot.append(pix)
    chiaro, chiave = decifra(ncgr_byte(f4))
    sc = scansione_pixel(chiaro)
    if len(sc) != 2 * LATO * LATO:
        raise Errore('classe %d: immagine scansionata di %d pixel' % (idx, len(sc)))
    return dict(nf=nf, fotogrammi=fot, celle=celle, passo=passo, chiave=chiave, scansione=sc,
                colori=C44.nclr_leggi(f1)[1], file=(f0, f1, f2, f3, f4))


def metà(sc, lato):
    return [sc[y * 2 * LATO + lato * LATO + x] for y in range(LATO) for x in range(LATO)]


def scrivi_allenatore(a, fotogrammi, colori):
    """Voci nuove (NCGR a celle, NCLR, NCER, NANR, NCGR cifrato) coi fotogrammi e i 16 colori dati.
    Il colore 0 resta quello dell'originale."""
    f0, f1, f2, f3, f4 = a['file']
    if len(fotogrammi) != a['nf']:
        raise Errore('%d fotogrammi invece di %d' % (len(fotogrammi), a['nf']))
    tiles = tile4(ncgr_byte(f0))
    for k, pix in enumerate(fotogrammi):
        cella = a['celle'][k] if k < len(a['celle']) else a['celle'][0]
        cella_da_immagine(tiles, cella, LATO, pix, base=k * TILE_FOT, passo=a['passo'])
    n0 = ncgr_con_byte(f0, byte4(tiles))
    sx = fotogrammi[0]
    dx = fotogrammi[1] if len(fotogrammi) > 1 else [0] * (LATO * LATO)
    sc = []
    for y in range(LATO):
        sc += sx[y * LATO:(y + 1) * LATO] + dx[y * LATO:(y + 1) * LATO]
    if any(sc[-4:]):
        raise Errore('gli ultimi 4 pixel dell’immagine scansionata devono essere trasparenti')
    chiaro = pixel_scansione(sc)
    cif = cifra(chiaro, a['chiave'])
    if decifra(cif)[0] != chiaro:
        raise Errore('cifratura: andata e ritorno diversi')
    n4 = ncgr_con_byte(f4, cif)
    n1 = C44.nclr_patch(f1, [None] + list(colori[1:16]))
    return [n0, n1, f2, f3, n4]


def prova_allenatore(files, idx):
    """Letto e riscritto coi suoi pixel e colori: deve essere identico (prova di forma). -> (identico, relazione
    fra immagine scansionata e fotogrammi)."""
    a = allenatore(files, idx)
    f0, f1, f2, f3, f4 = a['file']
    tiles = tile4(ncgr_byte(f0))
    for k, pix in enumerate(a['fotogrammi']):
        cella = a['celle'][k] if k < len(a['celle']) else a['celle'][0]
        cella_da_immagine(tiles, cella, LATO, pix, base=k * TILE_FOT, passo=a['passo'])
    ok = ncgr_con_byte(f0, byte4(tiles)) == f0 and cifra(pixel_scansione(a['scansione']), a['chiave']) == ncgr_byte(f4)
    sx, dx = metà(a['scansione'], 0), metà(a['scansione'], 1)
    rel = 'sx=f0' if sx == a['fotogrammi'][0] else 'sx?'
    if a['nf'] > 1:
        rel += ', dx=f1' if dx == a['fotogrammi'][1] else ', dx?'
    else:
        rel += ', dx vuota' if not any(dx) else ', dx?'
    return ok, rel


# ------------------------------------------------------------------------------------------- sprite

def sprite(files, i_ncgr, i_ncer, cella=0):
    """Immagine di uno sprite di a/1/0/9 secondo la cella dell'NCER."""
    g = files[i_ncgr]
    tiles = tile4(ncgr_byte(g))
    return immagine_da_cella(tiles, ncer_celle(files[i_ncer])[cella], passo=passo_tile(g))


def scrivi_sprite(files, i_ncgr, i_ncer, W, pix, cella=0):
    g = files[i_ncgr]
    tiles = tile4(ncgr_byte(g))
    cella_da_immagine(tiles, ncer_celle(files[i_ncer])[cella], W, pix, passo=passo_tile(g))
    return ncgr_con_byte(g, byte4(tiles))


# ------------------------------------------------------------------------------------------ colori

def palette(scheda):
    return C45.palette(scheda['colori'])


def c555(rgb):
    return G.bgr555(C44.scala5(rgb))
