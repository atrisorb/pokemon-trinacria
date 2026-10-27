"""Anteprime d'ingresso (src/map_preview_graphic.c) delle mappe del blocco 4.3 che stanno su uno slot
di HeartGold con l'anteprima. Ogni scena è disegnata qui (R-GFX-17) a 256×192, poi:
  - si divide in tile 8×8, si tengono i tile distinti (anche capovolti), come fa l'NSCR originale;
  - il PNG nuovo ha le stesse misure e la stessa profondità dell'originale (R-GFX-02): i tile distinti
    in ordine dall'alto, il resto a indice 0;
  - l'NSCR nuovo ha l'intestazione dell'originale e la mappa dei tile nuova.
Le varianti mattino / giorno / sera / notte sono la stessa scena con la luce cambiata.
"""
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..', '4.2'))
import tex42  # noqa: E402
from tex42 import hexc, mix, C  # noqa: E402
import trinacria_gfx as G  # noqa: E402

PREVIEW = os.path.join('files', 'fielddata', 'graphic', 'preview_graphic', 'preview_graphic')
W, H = 256, 192

# slot HeartGold -> (mappa di Trinacria, scena)
# (le mappe dell'ovest sugli slot con l'anteprima: registri 2.2 e 2.3, simbolo_hg_sostituito)
SLOT = {
    'ruins_of_alph': ('MAP_TP_MARSALA_STAGNONE', 'saline'),
    'bell_tower': ('MAP_ME_MISTRETTA', 'nebrodi'),
    'victory_road': ('MAP_AG_VALLE_DEI_TEMPLI', 'templi'),
}
LUCE = {'morning': (hexc('f8d8a8'), 0.18), 'day': (None, 0), 'evening': (hexc('f08040'), 0.30),
        'night': (hexc('101838'), 0.55)}


class Scena:
    def __init__(self, nome):
        self.px = [[(0, 0, 0)] * W for _ in range(H)]
        self.rng = tex42.Rng('ingresso:' + nome)

    def rect(self, x, y, w, h, c):
        for yy in range(max(0, y), min(H, y + h)):
            for xx in range(max(0, x), min(W, x + w)):
                self.px[yy][xx] = c

    def poli(self, pts, c):
        """Poligono pieno (scanline)."""
        ys = [p[1] for p in pts]
        for y in range(max(0, int(min(ys))), min(H, int(max(ys)) + 1)):
            xs = []
            for k in range(len(pts)):
                (x1, y1), (x2, y2) = pts[k], pts[(k + 1) % len(pts)]
                if (y1 <= y < y2) or (y2 <= y < y1):
                    xs.append(x1 + (y - y1) * (x2 - x1) / (y2 - y1))
            xs.sort()
            for a, b in zip(xs[0::2], xs[1::2]):
                for x in range(max(0, int(a)), min(W, int(b) + 1)):
                    self.px[y][x] = c

    def disco(self, cx, cy, r, c, ry=None):
        ry = ry or r
        for y in range(int(cy - ry), int(cy + ry) + 1):
            for x in range(int(cx - r), int(cx + r) + 1):
                if 0 <= x < W and 0 <= y < H and ((x - cx) / r) ** 2 + ((y - cy) / ry) ** 2 <= 1:
                    self.px[y][x] = c

    def cielo(self, alto, basso, fino=120, bande=6):
        for k in range(bande):
            self.rect(0, k * fino // bande, W, fino // bande + 1, mix(alto, basso, k / (bande - 1)))

    def colline(self, base_y, amp, c, passo=32, seme=0):
        pts = [(0, H)]
        for x in range(0, W + passo, passo):
            pts.append((x, base_y - amp * ((x * 7 + seme * 13) % 5) / 4))
        pts.append((W, H))
        self.poli(pts, c)


def scena(tipo):
    s = Scena(tipo)
    if tipo == 'saline':
        # le saline dello Stagnone al tramonto: vasche rosate, mulino a vento, mucchi di sale
        s.cielo(hexc('5a8ad0'), hexc('f0d8b0'), 110)
        s.rect(0, 100, W, 8, hexc('3a6a9a'))
        s.colline(104, 6, hexc('6a8a5a'), passo=48, seme=2)
        for k in range(4):
            y = 112 + k * 20
            s.rect(0, y, W, 18, hexc('dcb4b0') if k % 2 else hexc('c89a9a'))
            s.rect(0, y + 18, W, 2, hexc('82603c'))
        s.rect(150, 40, 30, 70, hexc('f0ece0'))
        s.rect(150, 40, 6, 70, hexc('c8c0b0'))
        s.poli([(146, 42), (165, 22), (184, 42)], hexc('a84c2a'))
        for k in range(6):
            s.poli([(165, 34), (165 + 50 * ((-1) ** k) * (k % 3 == 0), 34 - 40 * (k % 3 == 1)),
                    (169, 38)], hexc('f8f4e8'))
        for x in range(10, 130, 30):
            s.poli([(x, 172), (x + 12, 150), (x + 24, 172)], hexc('fafaf6'))
            s.poli([(x + 12, 150), (x + 24, 172), (x + 18, 172)], hexc('c8c4bc'))
        s.rect(0, 172, W, 20, hexc('9a7650'))
    elif tipo == 'nebrodi':
        # Mistretta sul crinale dei Nebrodi: faggete, case di pietra, il campanile
        s.cielo(hexc('6a9ad8'), hexc('dce8f0'), 100)
        s.colline(90, 30, hexc('3e6a2c'), passo=40, seme=1)
        s.colline(120, 20, hexc('2c5222'), passo=32, seme=4)
        for k in range(9):
            x = 20 + k * 26
            h = 30 + (k * 7) % 20
            s.rect(x, 150 - h, 22, h, hexc('c8b894') if k % 2 else hexc('a89878'))
            s.rect(x, 150 - h, 22, 4, hexc('a84c2a'))
            s.rect(x + 8, 150 - h + 12, 6, 8, hexc('3a3020'))
        s.rect(118, 70, 16, 80, hexc('d8c8a4'))
        s.poli([(114, 72), (126, 54), (138, 72)], hexc('8a3a22'))
        for x in range(0, W, 18):
            s.disco(x + 8, 166, 12, hexc('1e3a1a'), 10)
            s.disco(x + 6, 162, 6, hexc('3e6a2c'), 5)
        s.rect(0, 178, W, 14, hexc('5a4a30'))
    elif tipo == 'templi':
        # la Valle dei Templi: il Tempio della Concordia fra i mandorli, il mare in fondo
        s.cielo(hexc('4a7ad0'), hexc('f8e0b0'), 110)
        s.rect(0, 100, W, 12, hexc('3a6a9a'))
        s.colline(118, 10, hexc('b0904a'), passo=40, seme=3)
        s.rect(60, 70, 136, 10, hexc('dcbc80'))
        s.poli([(60, 70), (128, 46), (196, 70)], hexc('cca86a'))
        for x in range(64, 196, 14):
            s.rect(x, 80, 8, 50, hexc('dcbc80'))
            s.rect(x, 80, 2, 50, hexc('b8955a'))
        s.rect(56, 130, 144, 8, hexc('b8955a'))
        for x in (20, 220):
            s.rect(x, 130, 6, 40, hexc('4a2e1a'))
            s.disco(x + 3, 120, 22, hexc('f4d4dc'), 16)
            s.disco(x + 1, 116, 12, hexc('fcf0f2'), 8)
        s.rect(0, 166, W, 26, hexc('9a7650'))
        s.rect(0, 166, W, 3, hexc('5a7a3a'))
    return s


def colori_luce(px, luce):
    tinta, f = LUCE[luce]
    cache = {}
    out = []
    for row in px:
        r2 = []
        for c in row:
            if c not in cache:
                cache[c] = C(*c) if tinta is None else mix(c, tinta, f)
            r2.append(cache[c])
        out.append(r2)
    return out


def tile(px, tx, ty):
    return tuple(tuple(px[ty * 8 + y][tx * 8 + x] for x in range(8)) for y in range(8))


def nscr_e_png(px, nscr_orig, limite_tile):
    pal = [(0, 0, 0)]
    idx = {}
    for row in px:
        for c in row:
            if c not in idx:
                idx[c] = len(pal)
                pal.append(c)
    if len(pal) > 256:
        raise G.GfxError('K12', 'anteprima con %d colori' % len(pal))
    unici, mappa = [], []
    noti = {}
    for ty in range(H // 8):
        for tx in range(W // 8):
            t = tile(px, tx, ty)
            hit = None
            for flag, var in ((0, t), (0x400, tuple(r[::-1] for r in t)), (0x800, t[::-1]),
                              (0xC00, tuple(r[::-1] for r in t[::-1]))):
                if var in noti:
                    hit = noti[var] | flag
                    break
            if hit is None:
                noti[t] = len(unici)
                hit = len(unici)
                unici.append(t)
            mappa.append(hit)
    if len(unici) > limite_tile:
        raise G.GfxError('K21', 'anteprima con %d tile distinti, il massimo di HeartGold è %d' % (len(unici), limite_tile))
    pixel = [0] * (W * H)
    for k, t in enumerate(unici):
        ox, oy = (k % 32) * 8, (k // 32) * 8
        for y in range(8):
            for x in range(8):
                pixel[(oy + y) * W + ox + x] = idx[t[y][x]]
    o = nscr_orig.find(b'NRCS')
    n = struct.unpack_from('<I', nscr_orig, o + 16)[0] // 2
    if n != len(mappa):
        raise G.GfxError('K11', 'NSCR originale con %d caselle invece di %d' % (n, len(mappa)))
    nscr = nscr_orig[:o + 20] + struct.pack('<%dH' % n, *mappa) + nscr_orig[o + 20 + 2 * n:]
    return pal + [(0, 0, 0)] * (256 - len(pal)), pixel, nscr, len(unici)


def limite_hg(repo):
    """Tile distinti massimi nelle anteprime di HeartGold (dagli NSCR originali)."""
    m = 0
    d = os.path.join(repo, PREVIEW)
    for f in os.listdir(d):
        if f.endswith('.NSCR'):
            b = G.read(os.path.join(d, f))
            o = b.find(b'NRCS')
            n = struct.unpack_from('<I', b, o + 16)[0] // 2
            m = max(m, len({x & 0x3FF for x in struct.unpack_from('<%dH' % n, b, o + 20)}))
    return m


def costruisci(repo, out_dir, originali=None):
    """Scrive PNG e NSCR nuovi in out_dir; `originali` = cartella con gli originali (default il repository)."""
    src = originali or os.path.join(repo, PREVIEW)
    lim = limite_hg(repo)
    fatti = []
    os.makedirs(out_dir, exist_ok=True)
    for slot, (mappa, tipo) in SLOT.items():
        base = scena(tipo)
        for luce in ('morning', 'day', 'evening', 'night'):
            nome = 'preview_graphic_%s_%s' % (slot, luce)
            if not os.path.isfile(os.path.join(src, nome + '.NSCR')):
                continue
            px = colori_luce(base.px, luce)
            pal, pixel, nscr, n = nscr_e_png(px, G.read(os.path.join(src, nome + '.NSCR')), lim)
            G.png_write_indexed(os.path.join(out_dir, nome + '.png'), W, H, pal, pixel)
            with open(os.path.join(out_dir, nome + '.NSCR'), 'wb') as fh:
                fh.write(nscr)
            e = G.png_check(os.path.join(out_dir, nome + '.png'), come=os.path.join(src, nome + '.png'))
            fatti.append({'slot': slot, 'mappa': mappa, 'scena': tipo, 'ora': luce, 'png': nome + '.png',
                          'nscr': nome + '.NSCR', 'tile_distinti': n, 'colori': len({c for r in px for c in r}),
                          'errori': ['%s %s' % x for x in e]})
    return fatti, lim
