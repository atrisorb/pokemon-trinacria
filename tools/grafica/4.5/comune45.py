"""Blocco 4.5 — funzioni comuni: sprite di campo (NSBTX di files/data/mmodel/mmodel) a forma invariata.

Uno sprite di campo è un NSBTX con un fotogramma per texture (palette16, 32×32, nomi «<sprite>.<n>») e una
sola palette di 16 colori. Fotogrammi uguali condividono i dati (stesso indirizzo nel blocco delle texture).
`riscrivi()` scrive i pixel nuovi e i colori nuovi nei dati esistenti: stessa lunghezza, stesse intestazioni,
stessi nomi, stessi indirizzi (R-GFX-29 esteso agli NSBTX: R-GFX-34). Solo libreria standard."""
import os
import struct
import sys

QUI = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(QUI, '..', '..', '..'))
sys.path.insert(0, os.path.join(PROJ, 'tools'))
sys.path.insert(0, os.path.join(QUI, '..', '4.4'))
import trinacria_gfx as G          # noqa: E402
import comune44 as C44             # noqa: E402

OUT = os.path.join(PROJ, 'build', 'grafica', '4.5')
MMODEL = 'files/data/mmodel/mmodel/mmodel_%08d.NSBTX'
SPRITE_DATA = 'asm/overlay_01_sprite_data.s'


class Errore(Exception):
    pass


def u16(b, o):
    return struct.unpack_from('<H', b, o)[0]


def u32(b, o):
    return struct.unpack_from('<I', b, o)[0]


def leggi(repo, rel):
    return G.read(os.path.join(repo, *rel.split('/')))


# ---------------------------------------------------------------------------------------------- NSBTX

def struttura(b):
    """-> dict(fotogrammi={n: (indirizzo, w, h)}, nome, tex_dati, pal_dati, pal_off, colori)."""
    if b[:4] != b'BTX0':
        raise Errore('non è un NSBTX')
    o = u32(b, 0x10)
    tex_dati = o + u32(b, o + 0x14)
    pal_dati = o + u32(b, o + 0x38)
    fot = {}
    nome = None
    for n, d in G._dict(b, o + u16(b, o + 0x0E)):
        p = u32(d, 0)
        if (p >> 26) & 7 != 3:
            raise Errore('%s: formato %s, non palette16' % (n, G.TEX_FORMATS[(p >> 26) & 7]))
        base, _, num = n.rpartition('.')
        if not base or not num.isdigit():
            raise Errore('%s: nome di texture senza numero di fotogramma' % n)
        nome = nome or base
        fot[int(num)] = ((p & 0xFFFF) << 3, 8 << ((p >> 20) & 7), 8 << ((p >> 23) & 7))
    pals = G._dict(b, o + u32(b, o + 0x34))
    if len(pals) != 1:
        raise Errore('%d palette invece di una' % len(pals))
    pal_off = pal_dati + (u16(pals[0][1], 0) << 3)
    colori = [u16(b, pal_off + 2 * i) for i in range(16)]
    return dict(fotogrammi=fot, nome=nome, tex_dati=tex_dati, pal_off=pal_off, colori=colori, palette=pals[0][0])


def fotogramma(b, st, n):
    """Indici 0–15 del fotogramma n (per le anteprime e i controlli)."""
    off, w, h = st['fotogrammi'][n]
    raw = b[st['tex_dati'] + off: st['tex_dati'] + off + w * h // 2]
    pix = []
    for by in raw:
        pix += [by & 15, by >> 4]
    return pix


def riscrivi(b, fotogrammi, colori555):
    """b: NSBTX originale; fotogrammi: {n: 1024 indici}; colori555: 16 valori BGR555 (lo 0 resta quello
    dell'originale). Fotogrammi che nell'originale condividono i dati devono essere identici."""
    st = struttura(b)
    out = bytearray(b)
    per_indirizzo = {}
    for n, (off, w, h) in st['fotogrammi'].items():
        if n not in fotogrammi:
            raise Errore('manca il fotogramma %d di %s' % (n, st['nome']))
        pix = fotogrammi[n]
        if len(pix) != w * h:
            raise Errore('fotogramma %d: %d pixel invece di %d' % (n, len(pix), w * h))
        if off in per_indirizzo and per_indirizzo[off][1] != pix:
            raise Errore('%s: i fotogrammi %d e %d condividono i dati ma sono diversi'
                         % (st['nome'], per_indirizzo[off][0], n))
        per_indirizzo[off] = (n, pix)
        dati = bytes(pix[i] | (pix[i + 1] << 4) for i in range(0, len(pix), 2))
        out[st['tex_dati'] + off: st['tex_dati'] + off + len(dati)] = dati
    for i in range(1, 16):
        struct.pack_into('<H', out, st['pal_off'] + 2 * i, colori555[i])
    if len(out) != len(b) or out[:16] != b[:16]:
        raise Errore('K22 forma diversa')
    return bytes(out)


def prova_forma(b):
    """Letto e riscritto coi suoi stessi pixel e colori dev'essere identico (R-GFX-34)."""
    st = struttura(b)
    return riscrivi(b, {n: fotogramma(b, st, n) for n in st['fotogrammi']}, st['colori']) == b


# ---------------------------------------------------------------------------------------------- tabelle

def mmodel_di(repo):
    """{SPRITE_*: MMODEL_*} dalla tabella di overlay_01 (prima riga di ogni sprite) e {MMODEL_*: numero}."""
    import re
    righe = leggi(repo, SPRITE_DATA).decode('utf-8').splitlines()
    sp = {}
    for r in righe:
        m = re.match(r'\s*\.short (SPRITE_\w+), (MMODEL_\w+),', r)
        if m and m.group(1) not in sp:
            sp[m.group(1)] = m.group(2)
    num = {}
    for r in leggi(repo, 'include/constants/mmodel.h').decode('utf-8').splitlines():
        m = re.match(r'#define (MMODEL_\w+)\s+(\d+)', r)
        if m:
            num[m.group(1)] = int(m.group(2))
    usi = {}
    for s, m in sp.items():
        usi.setdefault(m, []).append(s)
    return sp, num, usi


# ---------------------------------------------------------------------------------------------- colori

def c555(rgb):
    return G.bgr555(C44.scala5(rgb))


def scuro(rgb, f=0.7):
    return C44.scala5(tuple(int(v * f) for v in rgb))


def chiaro(rgb, f=0.35):
    return C44.scala5(tuple(int(v + (255 - v) * f) for v in rgb))


def palette(colori):
    """colori: dict coi ruoli pelle, capelli, sopra, sotto, scarpe, A1, A2, A3 (e facoltativi occhi,
    contorno, bianco). -> 16 colori RGB nell'ordine dei ruoli di omino45 (lo 0 è un segnaposto)."""
    k = colori
    pal = [(0, 0, 0)] * 16
    pal[1] = C44.scala5(k.get('contorno', (41, 32, 41)))
    pal[2] = C44.scala5(k['pelle'])
    pal[3] = scuro(k['pelle'], 0.82)
    pal[4] = C44.scala5(k['capelli'])
    pal[5] = scuro(k['capelli'], 0.68)
    pal[6] = C44.scala5(k['sopra'])
    pal[7] = scuro(k['sopra'], 0.7)
    pal[8] = C44.scala5(k['sotto'])
    pal[9] = scuro(k['sotto'], 0.72)
    pal[10] = C44.scala5(k['scarpe'])
    pal[11] = C44.scala5(k.get('bianco', (246, 246, 238)))
    pal[12] = C44.scala5(k['A1'])
    pal[13] = C44.scala5(k['A2'])
    pal[14] = C44.scala5(k['A3'])
    pal[15] = C44.scala5(k.get('occhi', (32, 24, 32)))
    return pal
