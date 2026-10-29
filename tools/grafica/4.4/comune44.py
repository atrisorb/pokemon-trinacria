"""Blocco 4.4 — funzioni comuni agli script di disegno dell'interfaccia (R-GFX-17).

Lettura e riscrittura «a forma invariata» (R-GFX-29) di NCLR, NSCR e NCGR lineari: il file nuovo è
l'originale con i soli dati (colori, voci della schermata, pixel delle tile) cambiati, stessa lunghezza e
stesse intestazioni. Testo disegnato coi glifi del font del gioco (files/graphic/font, membro 0), che il
Modulo 1 §5 tiene; il © viene dal glifo di tools/font_extend.py.
Solo libreria standard e tools/trinacria_gfx.py."""
import os
import struct
import sys

QUI = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(QUI, '..', '..', '..'))
sys.path.insert(0, os.path.join(PROJ, 'tools'))
import trinacria_gfx as G          # noqa: E402
import font_extend as FE           # noqa: E402

OUT = os.path.join(PROJ, 'build', 'grafica', '4.4')


class Errore(Exception):
    pass


# ---------------------------------------------------------------------------------------------- file

def leggi(repo, rel):
    return G.read(os.path.join(repo, *rel.split('/')))


def _blocco(b, magia):
    o = b.find(magia)
    if o < 0:
        raise Errore('blocco %s assente' % magia.decode())
    return o


def nclr_leggi(b):
    """-> (profondità 3/4, [colori RGB]) dal blocco TTLP."""
    o = _blocco(b, b'TTLP')
    bd, _, size, off = struct.unpack_from('<IIII', b, o + 8)
    d = b[o + 8 + off:o + 8 + off + size]
    return bd, [G.rgb_of(struct.unpack_from('<H', d, i)[0]) for i in range(0, len(d), 2)]


def nclr_patch(b, colori):
    """Originale con i colori dati (lista di RGB, None = colore invariato). Stessa lunghezza."""
    o = _blocco(b, b'TTLP')
    _, _, size, off = struct.unpack_from('<IIII', b, o + 8)
    base = o + 8 + off
    out = bytearray(b)
    if len(colori) > size // 2:
        raise Errore('NCLR: %d colori, il file ne ha %d' % (len(colori), size // 2))
    for i, c in enumerate(colori):
        if c is not None:
            struct.pack_into('<H', out, base + 2 * i, G.bgr555(c))
    return bytes(out)


def nscr_leggi(b):
    """-> (larghezza in tile, altezza in tile, [voci u16])."""
    o = _blocco(b, b'NRCS')
    w, h, _, size = struct.unpack_from('<HHII', b, o + 8)
    return w // 8, h // 8, list(struct.unpack_from('<%dH' % (size // 2), b, o + 20))


def nscr_patch(b, voci):
    o = _blocco(b, b'NRCS')
    w, h, _, size = struct.unpack_from('<HHII', b, o + 8)
    if len(voci) != size // 2:
        raise Errore('NSCR: %d voci invece di %d' % (len(voci), size // 2))
    out = bytearray(b)
    struct.pack_into('<%dH' % len(voci), out, o + 20, *voci)
    return bytes(out)


def voce(tile, pal=0, hf=0, vf=0):
    return (tile & 0x3FF) | (hf << 10) | (vf << 11) | (pal << 12)


def ncgr_leggi(b):
    """NCGR lineare (tile in ordine, non a celle né cifrato) -> dict(bpp, tile [[8 righe di 8 indici]])."""
    o = _blocco(b, b'RAHC')
    th, tw, bd, mapping, tiled, size, off = struct.unpack_from('<HHIIIII', b, o + 8)
    d = b[o + 8 + off:o + 8 + off + size]
    bpp = 4 if bd == 3 else 8
    n = size * 8 // (64 * bpp)
    t = []
    for k in range(n):
        if bpp == 4:
            s = d[k * 32:k * 32 + 32]
            t.append([[(s[y * 4 + x // 2] >> (4 * (x & 1))) & 15 for x in range(8)] for y in range(8)])
        else:
            s = d[k * 64:k * 64 + 64]
            t.append([[s[y * 8 + x] for x in range(8)] for y in range(8)])
    return {'bpp': bpp, 'tile': t, 'mapping': mapping, 'tiled': tiled}


def ncgr_patch(b, tile):
    """Originale con le tile date (stesso numero): 4 bpp col pixel di sinistra nel nibble basso."""
    o = _blocco(b, b'RAHC')
    th, tw, bd, mapping, tiled, size, off = struct.unpack_from('<HHIIIII', b, o + 8)
    if tiled or mapping:
        raise Errore('NCGR non lineare: va convertito con nitrogfx (R-GFX-08)')
    bpp = 4 if bd == 3 else 8
    n = size * 8 // (64 * bpp)
    if len(tile) != n:
        raise Errore('NCGR: %d tile invece di %d' % (len(tile), n))
    d = bytearray()
    for t in tile:
        for row in t:
            if bpp == 4:
                for x in range(0, 8, 2):
                    if row[x] > 15 or row[x + 1] > 15:
                        raise Errore('NCGR a 4 bit: indice oltre 15')
                    d.append(row[x] | (row[x + 1] << 4))
            else:
                d += bytes(row)
    out = bytearray(b)
    out[o + 8 + off:o + 8 + off + size] = d
    return bytes(out)


# --------------------------------------------------------------------------------------------- tile

def tile_di(pix, w, tx, ty):
    return tuple(tuple(pix[(ty * 8 + y) * w + tx * 8 + x] for x in range(8)) for y in range(8))


def capovolta(t, hf, vf):
    rows = t[::-1] if vf else t
    return tuple(tuple(r[::-1]) if hf else tuple(r) for r in rows)


class Foglio:
    """Raccolta di tile senza doppioni (con capovolgimenti se ammessi) -> voci di schermata."""

    def __init__(self, massimo, flip=True, prime=()):
        self.tile = list(prime)
        self.idx = {}
        self.massimo = massimo
        self.flip = flip
        for k, t in enumerate(self.tile):
            self.idx.setdefault(tuple(map(tuple, t)), (k, 0, 0))

    def aggiungi(self, t, pal=0):
        t = tuple(map(tuple, t))
        for hf, vf in ((0, 0), (1, 0), (0, 1), (1, 1)) if self.flip else ((0, 0),):
            k = self.idx.get(capovolta(t, hf, vf))
            if k is not None:
                return voce(k[0], pal, hf, vf)
        if len(self.tile) >= self.massimo:
            raise Errore('foglio pieno: più di %d tile' % self.massimo)
        self.tile.append(t)
        self.idx[t] = (len(self.tile) - 1, 0, 0)
        return voce(len(self.tile) - 1, pal)

    def immagine(self, larghezza_tile, altezza_tile=None):
        """-> pixel di un foglio largo `larghezza_tile` tile (indici)."""
        n = len(self.tile)
        h = altezza_tile or (n + larghezza_tile - 1) // larghezza_tile
        W = larghezza_tile * 8
        pix = [0] * (W * h * 8)
        for k, t in enumerate(self.tile):
            tx, ty = k % larghezza_tile, k // larghezza_tile
            for y in range(8):
                for x in range(8):
                    pix[(ty * 8 + y) * W + tx * 8 + x] = t[y][x]
        return W, h * 8, pix


# ------------------------------------------------------------------------------------------- testo

class Font:
    """Glifi del font 0 del gioco: 16×16 a 2 bit (1 inchiostro, 2 ombra, 3 fondo della cella)."""

    def __init__(self, repo):
        b = leggi(repo, 'files/graphic/font/font_00000000.bin')
        go, wo, n = struct.unpack_from('<III', b, 0)
        self.b, self.go, self.wid, self.n = b, go, b[wo:wo + n], n
        self.cm = {}
        for line in open(os.path.join(repo, 'tools', 'msgenc', 'charmap.txt'), encoding='utf-8'):
            body = line.split('//')[0].rstrip('\n')
            if '=' in body:
                code, _, val = body.lstrip().partition('=')
                try:
                    c = int(code, 16)
                except ValueError:
                    continue
                if len(val) == 1:
                    self.cm.setdefault(val, c)
        self.extra = {}
        for code, ch, rows in FE.NEW_GLYPHS:
            grid, w = FE.build_grid(rows)
            self.extra[ch] = (grid, w)

    def glifo(self, ch):
        if ch in self.cm and 0 < self.cm[ch] <= self.n:
            c = self.cm[ch]
            return FE.decode_glyph(self.b[self.go + (c - 1) * 64:self.go + c * 64]), self.wid[c - 1]
        if ch in self.extra:
            return self.extra[ch]
        raise Errore('carattere %r assente dal font' % ch)

    def larghezza(self, s):
        return sum(self.glifo(c)[1] for c in s)

    def scrivi(self, pix, W, H, x0, y0, s, ink, ombra=None):
        """Disegna `s` coi colori dati (ombra None = senza ombra). Restituisce la larghezza."""
        x = x0
        for ch in s:
            g, w = self.glifo(ch)
            for r in range(16):
                for c in range(min(w, 16)):
                    v = g[r][c]
                    col = ink if v == 1 else (ombra if v == 2 else None)
                    if col is not None and 0 <= x + c < W and 0 <= y0 + r < H:
                        pix[(y0 + r) * W + x + c] = col
            x += w
        return x - x0


# ----------------------------------------------------------------------------------------- disegno

def rett(pix, W, x, y, w, h, col, H=None):
    for yy in range(max(0, y), y + h):
        if H is not None and yy >= H:
            break
        for xx in range(max(0, x), min(W, x + w)):
            pix[yy * W + xx] = col


def salva_png(path, w, h, palette, pix, bpp=8):
    """PNG indicizzato a 4 o 8 bit (R-GFX-04) coi colori portati alla scala di nitrogfx (R-GFX-03)."""
    import zlib
    os.makedirs(os.path.dirname(path), exist_ok=True)
    n = 16 if bpp == 4 else 256
    pal = [scala5(c) for c in list(palette)[:n]]
    pal += [(0, 0, 0)] * (n - len(pal))
    if max(pix) >= n:
        raise Errore('%s: indice %d oltre %d colori' % (os.path.basename(path), max(pix), n))

    def chunk(t, d):
        return struct.pack('>I', len(d)) + t + d + struct.pack('>I', zlib.crc32(t + d) & 0xFFFFFFFF)
    raw = bytearray()
    for y in range(h):
        raw.append(0)
        row = pix[y * w:(y + 1) * w]
        if bpp == 4:
            raw += bytes((row[x] << 4) | (row[x + 1] if x + 1 < w else 0) for x in range(0, w, 2))
        else:
            raw += bytes(row)
    out = b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', w, h, bpp, 3, 0, 0, 0))
    out += chunk(b'PLTE', b''.join(bytes(c) for c in pal))
    out += chunk(b'IDAT', zlib.compress(bytes(raw), 9)) + chunk(b'IEND', b'')
    with open(path, 'wb') as fh:
        fh.write(out)


def scala5(c):
    """Colore nella scala dei 32 valori di nitrogfx (R-GFX-03)."""
    return tuple(G.rgb_of(G.bgr555(c)))


def anteprima(path, w, h, pix, palette, scala=2):
    """PNG a colori pieni (8 bit indicizzato, ingrandito) per guardare il risultato."""
    W, H = w * scala, h * scala
    big = [0] * (W * H)
    for y in range(H):
        row = pix[(y // scala) * w:(y // scala) * w + w]
        big[y * W:(y + 1) * W] = [row[x // scala] for x in range(W)]
    salva_png(path, W, H, list(palette) + [(0, 0, 0)] * (256 - len(palette)), big)


def schermata_pixel(foglio_tile, voci, wt, ht, colori, bpp8):
    """Rende una schermata (voci NSCR) in pixel RGB-indice: restituisce (w, h, pixel indici 0–255)
    dove l'indice è pal*16+v (4 bit) o v (8 bit): serve alle anteprime."""
    W, H = wt * 8, ht * 8
    pix = [0] * (W * H)
    for i, e in enumerate(voci[:wt * ht]):
        t = e & 0x3FF
        if t >= len(foglio_tile):
            continue
        tt = capovolta(foglio_tile[t], e >> 10 & 1, e >> 11 & 1)
        p = e >> 12
        bx, by = i % wt * 8, i // wt * 8
        for y in range(8):
            for x in range(8):
                v = tt[y][x]
                pix[(by + y) * W + bx + x] = v if bpp8 else p * 16 + v
    return W, H, pix
