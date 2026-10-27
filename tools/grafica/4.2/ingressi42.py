"""Anteprime d'ingresso (src/map_preview_graphic.c) delle mappe del blocco 4.2 che stanno su uno slot
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
import tex42  # noqa: E402
from tex42 import hexc, mix, C  # noqa: E402
import trinacria_gfx as G  # noqa: E402

PREVIEW = os.path.join('files', 'fielddata', 'graphic', 'preview_graphic', 'preview_graphic')
W, H = 256, 192

# slot HeartGold -> (mappa di Trinacria, scena)
SLOT = {
    'sprout_tower': ('MAP_CT_CATANIA_PALAZZO_CEMENTO_P01_P02', 'cemento'),
    'burned_tower': ('MAP_CT_CATANIA_PALAZZO_CEMENTO_P07_P08', 'cemento_alto'),
    'ilex_forest': ('MAP_CT_ETNA_MONTI_ROSSI', 'pineta'),
    'union_cave': ('MAP_CT_BRONTE_SCIARA', 'sciara'),
    'ice_path': ('MAP_CT_ETNA_GROTTA_DEL_GELO', 'gelo'),
    'slowpoke_well': ('MAP_SR_SIRACUSA_LATOMIE', 'latomie'),
    'dark_cave_r45': ('MAP_RG_CAVA_D_ISPICA', 'cava'),
    'diglett_cave': ('MAP_CL_SAN_CATALDO', 'zolfara'),
    'mt_moon': ('MAP_CL_SUTERA', 'sutera'),
    'viridian_forest': ('MAP_CL_CASTELLO_MANFREDONICO', 'castello'),
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
    lava = [hexc('20202a'), hexc('34343e'), hexc('4a4a56')]
    if tipo in ('cemento', 'cemento_alto'):
        s.cielo(hexc('4a6a9a'), hexc('e8b878'), 130)
        s.colline(150, 20, hexc('5a5a64'))
        for k, (x, w, h) in enumerate(((10, 50, 90), (190, 56, 100), (70, 110, 150 if tipo == 'cemento_alto' else 130))):
            s.rect(x, 170 - h, w, h, hexc('7a7a7c') if k < 2 else hexc('8c8c8a'))
            for yy in range(170 - h + 8, 166, 12):
                for xx in range(x + 6, x + w - 8, 12):
                    s.rect(xx, yy, 6, 6, hexc('2e3640') if (xx + yy) % 3 else hexc('e8c870'))
            s.rect(x, 170 - h, w, 3, hexc('5c5c5e'))
        for k in range(5):
            y = 50 + k * 18
            for x in range(70, 180):
                s.px[y + (x - 70) // 30][x] = hexc('141414')
        s.rect(0, 170, W, 22, hexc('3a3a40'))
    elif tipo == 'pineta':
        s.cielo(hexc('3a1a2a'), hexc('f87830'), 140)
        s.poli([(60, 140), (150, 30), (170, 30), (250, 140)], hexc('3a2a2e'))
        for k in range(14):
            x = 8 + k * 18
            s.rect(x + 5, 110, 4, 60, hexc('2a1a10'))
            s.disco(x + 7, 100, 12, hexc('1e3418'), 9)
            if k % 3 == 1:
                s.disco(x + 7, 92, 7, hexc('f8a030'), 10)
                s.disco(x + 7, 96, 4, hexc('f8e070'), 5)
        s.rect(0, 168, W, 24, lava[1])
    elif tipo == 'sciara':
        s.cielo(hexc('6a9ad8'), hexc('d8e8f0'), 110)
        s.poli([(30, 110), (140, 20), (160, 20), (256, 110)], hexc('5a5a68'))
        s.poli([(128, 30), (140, 20), (160, 20), (172, 30)], hexc('f0f0f0'))
        for k in range(5):
            y = 110 + k * 16
            s.rect(0, y, W, 16, lava[k % 3])
            s.rect(0, y, W, 2, hexc('6a5a4a'))
            for x in range(6 + (k % 2) * 10, W, 20):
                s.disco(x, y + 6, 7, hexc('5a8a3a'), 5)
                s.disco(x - 2, y + 4, 3, hexc('a8c860'), 2)
    elif tipo == 'gelo':
        s.cielo(hexc('2a3a6a'), hexc('9ab8e0'), 120)
        s.rect(0, 40, W, 152, lava[0])
        s.disco(128, 130, 70, hexc('6a9ac8'), 60)
        s.disco(128, 140, 56, hexc('bcdcec'), 48)
        s.disco(128, 150, 36, hexc('f0f8ff'), 30)
        for x in range(70, 190, 16):
            s.poli([(x, 72), (x + 8, 72), (x + 4, 98)], hexc('e0f0f8'))
        s.rect(0, 176, W, 16, lava[1])
    elif tipo == 'latomie':
        s.cielo(hexc('5a8ad0'), hexc('d0e4f0'), 70)
        s.rect(0, 50, W, 142, hexc('c4b494'))
        for x in range(0, W, 24):
            s.rect(x, 50, 2, 142, hexc('a89878'))
        s.poli([(100, 190), (112, 70), (128, 50), (140, 70), (150, 190)], hexc('1a1610'))
        for x in (20, 200):
            s.rect(x, 140, 8, 40, hexc('3a2a1a'))
            s.disco(x + 4, 130, 20, hexc('3e6c30'), 16)
        s.rect(0, 178, W, 14, hexc('7a6a50'))
    elif tipo == 'cava':
        s.cielo(hexc('5a8ad0'), hexc('e0ecf0'), 60)
        s.poli([(0, 40), (110, 70), (110, 192), (0, 192)], hexc('b8a888'))
        s.poli([(256, 40), (146, 70), (146, 192), (256, 192)], hexc('a89878'))
        for k in range(8):
            x = 14 + (k % 4) * 22 if k < 4 else 160 + (k % 4) * 22
            y = 90 + (k // 4 % 2) * 40
            s.rect(x, y, 12, 14, hexc('2a2218'))
            s.disco(x + 6, y, 6, hexc('2a2218'), 4)
        s.rect(110, 150, 36, 42, hexc('7a8a4a'))
    elif tipo == 'zolfara':
        s.cielo(hexc('7aa0d0'), hexc('f0e0b0'), 110)
        s.colline(120, 30, hexc('a49a7a'))
        for k in range(6):
            s.rect(20 + k * 14, 90 - k * 4, 12, 30 + k * 4, hexc('dcc8a0'))
            s.rect(22 + k * 14, 96 - k * 4, 4, 5, hexc('3a3020'))
        s.rect(170, 60, 4, 90, hexc('2a2a2a'))
        s.rect(200, 60, 4, 90, hexc('2a2a2a'))
        s.rect(166, 58, 42, 6, hexc('2a2a2a'))
        s.disco(187, 66, 10, hexc('4a4a4a'))
        s.rect(0, 150, W, 42, hexc('c8b040'))
        s.rect(0, 150, W, 4, hexc('8a7a30'))
    elif tipo == 'sutera':
        s.cielo(hexc('6a9ad8'), hexc('f0e8d0'), 100)
        s.poli([(40, 160), (120, 30), (150, 26), (220, 160)], hexc('d8d0c0'))
        s.poli([(120, 30), (150, 26), (160, 40), (110, 44)], hexc('f0ece0'))
        s.rect(128, 18, 14, 10, hexc('f8f4e8'))
        for k in range(10):
            x = 10 + k * 24
            s.rect(x, 140 + (k % 3) * 6, 20, 30, hexc('e0d0b0') if k % 2 else hexc('c8a070'))
            s.rect(x, 140 + (k % 3) * 6, 20, 4, hexc('a84c2a'))
        s.rect(0, 176, W, 16, hexc('9a8a6a'))
    elif tipo == 'castello':
        s.cielo(hexc('4a6aa8'), hexc('f0d0a0'), 120)
        s.poli([(40, 192), (90, 90), (180, 80), (230, 192)], hexc('a49478'))
        s.rect(96, 50, 80, 44, hexc('c8b894'))
        for x in range(96, 176, 10):
            s.rect(x, 44, 6, 6, hexc('c8b894'))
        s.rect(150, 30, 22, 64, hexc('d8c8a4'))
        for x in (110, 130, 158):
            s.rect(x, 62, 6, 12, hexc('2a2218'))
        s.disco(136, 88, 8, hexc('2a2218'), 6)
        s.colline(180, 10, hexc('6a7a40'))
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
