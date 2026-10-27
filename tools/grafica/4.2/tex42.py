"""Texture del blocco 4.2 (R-GFX-17): ogni texture è disegnata qui, da zero, in modo riproducibile.

Ogni texture è un PNG indicizzato di al massimo 16 colori (R-GFX-11) presi dalla scala 555 di
nitrogfx (R-GFX-03). Le sagome (alberi, lampioni, oggetti in piedi) usano l'indice 0 come
trasparente. Lo stesso nome dà sempre lo stesso disegno: il generatore pseudocasuale è un
xorshift con il seme ricavato dal nome (niente `random`, che cambia fra versioni di Python).

Uso come modulo: `disegna(nome)` -> Tex; `salva_area(area, cartella)` scrive i PNG di un'area.
"""
import math
import os
import sys
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, os.path.join(PROJ, 'tools'))
import trinacria_gfx as G  # noqa: E402

# --------------------------------------------------------------------------- colori


def q(v):
    """Componente 0–255 -> valore più vicino della scala 555 di nitrogfx (R-GFX-03)."""
    return min(G.CANON, key=lambda c: abs(c - v))


def C(r, g, b):
    return (q(r), q(g), q(b))


def hexc(s):
    return C(int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16))


def mix(a, b, t):
    return C(*(a[i] + (b[i] - a[i]) * t for i in range(3)))


def scala(base, n, scuro=0.55, chiaro=1.25):
    """n tonalità dello stesso colore, dalla più scura alla più chiara."""
    out = []
    for i in range(n):
        f = scuro + (chiaro - scuro) * (i / max(1, n - 1))
        out.append(C(*(min(255, base[k] * f) for k in range(3))))
    return out


class Rng:
    def __init__(self, seme):
        self.s = (zlib.crc32(seme.encode('utf-8')) or 1) & 0xFFFFFFFF

    def u32(self):
        s = self.s
        s ^= (s << 13) & 0xFFFFFFFF
        s ^= s >> 17
        s ^= (s << 5) & 0xFFFFFFFF
        self.s = s
        return s

    def f(self):
        return self.u32() / 4294967296.0

    def i(self, a, b):
        return a + self.u32() % (b - a + 1)

    def p(self, prob):
        return self.f() < prob


# --------------------------------------------------------------------------- tela


class Tex:
    def __init__(self, nome, w, h, pal, sagoma=False):
        assert len(pal) <= 16, nome
        self.nome, self.w, self.h, self.sagoma = nome, w, h, sagoma
        self.pal = list(pal)
        self.px = [0] * (w * h)
        self.rng = Rng(nome)

    # indici: per le sagome 0 = trasparente
    def put(self, x, y, i, wrap=True):
        if wrap:
            x %= self.w
            y %= self.h
        elif not (0 <= x < self.w and 0 <= y < self.h):
            return
        self.px[y * self.w + x] = i

    def get(self, x, y):
        return self.px[(y % self.h) * self.w + x % self.w]

    def fill(self, i):
        self.px = [i] * (self.w * self.h)

    def rect(self, x, y, w, h, i, wrap=True):
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                self.put(xx, yy, i, wrap)

    def frame(self, x, y, w, h, i, wrap=True):
        for xx in range(x, x + w):
            self.put(xx, y, i, wrap)
            self.put(xx, y + h - 1, i, wrap)
        for yy in range(y, y + h):
            self.put(x, yy, i, wrap)
            self.put(x + w - 1, yy, i, wrap)

    def hline(self, x, y, w, i, wrap=True):
        self.rect(x, y, w, 1, i, wrap)

    def vline(self, x, y, h, i, wrap=True):
        self.rect(x, y, 1, h, i, wrap)

    def disc(self, cx, cy, r, i, wrap=False, ry=None):
        ry = r if ry is None else ry
        for yy in range(int(cy - ry - 1), int(cy + ry + 2)):
            for xx in range(int(cx - r - 1), int(cx + r + 2)):
                if ((xx + 0.5 - cx) / max(r, 0.01)) ** 2 + ((yy + 0.5 - cy) / max(ry, 0.01)) ** 2 <= 1.0:
                    self.put(xx, yy, i, wrap)

    def speckle(self, idx, prob, area=None, wrap=True):
        x0, y0, w, h = area or (0, 0, self.w, self.h)
        for yy in range(y0, y0 + h):
            for xx in range(x0, x0 + w):
                if self.rng.p(prob):
                    self.put(xx, yy, idx if isinstance(idx, int) else idx[self.rng.u32() % len(idx)], wrap)

    def remap(self, mappa):
        self.px = [mappa.get(i, i) for i in self.px]

    def png(self, path):
        pal = (self.pal + [(0, 0, 0)] * 16)[:16]
        G.png_write_indexed(path, self.w, self.h, pal, self.px)

    def rgb(self, x, y):
        i = self.get(x, y)
        if self.sagoma and i == 0:
            return None
        return self.pal[i]


# --------------------------------------------------------------------------- motivi di base


def rumore(t, livelli, prob=0.18, macchie=0):
    """Fondo a grana: indice 1 di base, poi chiari e scuri sparsi (livelli = indici)."""
    for i in livelli:
        t.speckle(i, prob / len(livelli))
    for _ in range(macchie):
        cx, cy, r = t.rng.i(0, t.w - 1), t.rng.i(0, t.h - 1), t.rng.i(2, 4)
        t.disc(cx, cy, r, livelli[t.rng.u32() % len(livelli)], wrap=True)


def lastre(t, lato_x, lato_y, giunto, sfalsa=True, vari=()):
    """Pavimento a lastre rettangolari con giunti; vari = indici per variare le lastre."""
    for ry in range(0, t.h, lato_y):
        off = (lato_x // 2) if sfalsa and (ry // lato_y) % 2 else 0
        for rx in range(0, t.w, lato_x):
            x0 = rx + off
            if vari:
                v = vari[t.rng.u32() % len(vari)]
                t.rect(x0 + 1, ry + 1, lato_x - 1, lato_y - 1, v)
            t.hline(x0, ry, lato_x, giunto)
            t.vline(x0, ry, lato_y, giunto)


def mattoni(t, bw, bh, malta, colori):
    for ry in range(0, t.h, bh):
        off = bw // 2 if (ry // bh) % 2 else 0
        for rx in range(0, t.w, bw):
            c = colori[t.rng.u32() % len(colori)]
            t.rect(rx + off, ry, bw, bh, c)
            t.hline(rx + off, ry, bw, malta)
            t.vline(rx + off, ry, bh, malta)


def pietre(t, colori, giunto, n=14, rmin=3, rmax=6):
    """Pietre irregolari (muri a secco, scogli): dischi sovrapposti con contorno."""
    t.fill(giunto)
    for _ in range(n):
        cx, cy = t.rng.i(0, t.w - 1), t.rng.i(0, t.h - 1)
        r = t.rng.i(rmin, rmax)
        c = colori[t.rng.u32() % len(colori)]
        t.disc(cx, cy, r, c, wrap=True, ry=r * 0.75)
    # contorni: un pixel di giunto dove cambia colore verso il basso
    src = list(t.px)
    for y in range(t.h):
        for x in range(t.w):
            a = src[y * t.w + x]
            b = src[((y + 1) % t.h) * t.w + x]
            if a != b and a != giunto and b != giunto:
                t.put(x, y, giunto)


def onde(t, base, chiaro, scuro, passo=8):
    t.fill(base)
    for y in range(0, t.h, passo):
        for x in range(t.w):
            k = (x + (y // passo) * 3) % 12
            if k in (0, 1, 2):
                t.put(x, y + (1 if k == 1 else 0), chiaro)
            elif k in (6, 7):
                t.put(x, y + passo // 2, scuro)


def doghe(t, larghezza, colori, giunto, verticali=False):
    n = t.w if verticali else t.h
    for k in range(0, n, larghezza):
        c = colori[(k // larghezza) % len(colori)]
        if verticali:
            t.rect(k, 0, larghezza, t.h, c)
            t.vline(k, 0, t.h, giunto)
        else:
            t.rect(0, k, t.w, larghezza, c)
            t.hline(0, k, t.w, giunto)


# --------------------------------------------------------------------------- catalogo

CATALOGO = {}


def tex(nome, w, h, sagoma=False):
    def deco(fn):
        CATALOGO[nome] = (w, h, sagoma, fn)
        return fn
    return deco


def disegna(nome):
    w, h, sagoma, fn = CATALOGO[nome]
    return fn(nome, w, h, sagoma)


# Tinte comuni
NERO = C(16, 16, 24)
LAVA = [hexc('2a2a30'), hexc('3a3a42'), hexc('4a4a52'), hexc('5c5c66'), hexc('70707a')]
CALCARE = [hexc('a89878'), hexc('c4b494'), hexc('d8caa8'), hexc('e8dcc0'), hexc('f4ecd8')]
ERBA = [hexc('3a6a2a'), hexc('4a7e32'), hexc('5c923c'), hexc('74a84a'), hexc('90bc5c')]
MARE = [hexc('1c4a7c'), hexc('2a5e94'), hexc('3c74aa'), hexc('6a9cc8'), hexc('b8d8ec')]
TERRA = [hexc('6a4a2e'), hexc('82603c'), hexc('9a7650'), hexc('b08c62')]
COTTO = [hexc('8a3a22'), hexc('a84c2a'), hexc('c4623a'), hexc('d8805a')]
FOGLIA = [hexc('1e3e1e'), hexc('2c5426'), hexc('3e6c30'), hexc('58863e'), hexc('74a050')]
LEGNO = [hexc('4a2e1a'), hexc('6a4426'), hexc('8a5c34'), hexc('a8784a')]
METALLO = [hexc('4a525a'), hexc('6a747e'), hexc('8c96a0'), hexc('b0b8c0'), hexc('d4dadf')]


# ---- terreni (32×32 salvo dove detto) ------------------------------------------------------


@tex('basolato', 32, 32)
def _basolato(n, w, h, s):
    t = Tex(n, w, h, [LAVA[0], LAVA[1], LAVA[2], LAVA[3], LAVA[4], hexc('26262c')])
    t.fill(2)
    lastre(t, 16, 8, 0, vari=(1, 2, 3, 2))
    t.speckle([1, 3, 4], 0.10)
    return t


@tex('lastricato', 32, 32)
def _lastricato(n, w, h, s):
    t = Tex(n, w, h, [hexc('8a7c62')] + CALCARE)
    t.fill(3)
    lastre(t, 16, 16, 0, sfalsa=True, vari=(2, 3, 4, 3))
    t.speckle([1, 2, 5], 0.08)
    return t


@tex('asfalto', 32, 32)
def _asfalto(n, w, h, s):
    t = Tex(n, w, h, [hexc('34343a'), hexc('404048'), hexc('4c4c54'), hexc('5a5a62'), hexc('2a2a2e')])
    t.fill(1)
    t.speckle([0, 2, 3, 4], 0.35)
    return t


@tex('marciapiede', 32, 32)
def _marciapiede(n, w, h, s):
    t = Tex(n, w, h, [hexc('6c6c70'), hexc('8a8a8e'), hexc('9c9ca0'), hexc('b0b0b2'), hexc('c4c4c4')])
    t.fill(2)
    lastre(t, 16, 16, 0, sfalsa=False, vari=(2, 3, 2))
    t.speckle([1, 4], 0.06)
    return t


@tex('erba', 32, 32)
def _erba(n, w, h, s):
    t = Tex(n, w, h, ERBA)
    t.fill(2)
    rumore(t, [1, 3, 4], 0.35, macchie=3)
    for _ in range(14):
        x, y = t.rng.i(0, 31), t.rng.i(0, 31)
        t.put(x, y, 4)
        t.put(x, y + 1, 1)
    return t


@tex('erba_alta', 16, 16)
def _erba_alta(n, w, h, s):
    t = Tex(n, w, h, [hexc('24461c'), ERBA[0], ERBA[1], ERBA[2], ERBA[3], ERBA[4]])
    t.fill(2)
    for x0 in range(0, 16, 4):
        for y0 in (0, 8):
            ox = x0 + (2 if y0 else 0)
            for k in range(6):
                t.put(ox + 1, y0 + k + 1, 0 if k > 3 else 4)
                t.put(ox + 2, y0 + k, 0 if k > 4 else 5)
                t.put(ox, y0 + k + 2, 1 if k > 2 else 3)
    return t


@tex('fiori', 16, 16)
def _fiori(n, w, h, s):
    t = Tex(n, w, h, ERBA[:4] + [hexc('e8d040'), hexc('d84a4a'), hexc('f0f0f0'), hexc('c070c8')])
    t.fill(2)
    t.speckle([1, 3], 0.3)
    for _ in range(9):
        x, y, c = t.rng.i(0, 15), t.rng.i(0, 15), t.rng.i(4, 7)
        t.put(x, y, c)
        t.put(x + 1, y, c)
        t.put(x, y + 1, c)
    return t


@tex('terra', 32, 32)
def _terra(n, w, h, s):
    t = Tex(n, w, h, TERRA + [hexc('c8a47a')])
    t.fill(2)
    rumore(t, [0, 1, 3, 4], 0.4, macchie=2)
    return t


@tex('sabbia', 32, 32)
def _sabbia(n, w, h, s):
    t = Tex(n, w, h, [hexc('b89c68'), hexc('ccb27c'), hexc('dcc490'), hexc('e8d4a4'), hexc('f4e4bc')])
    t.fill(2)
    rumore(t, [0, 1, 3, 4], 0.3)
    return t


@tex('sabbia_nera', 32, 32)
def _sabbia_nera(n, w, h, s):
    t = Tex(n, w, h, [hexc('1e1e22'), hexc('2c2c30'), hexc('3a3a3e'), hexc('4c4a4a'), hexc('646060')])
    t.fill(2)
    rumore(t, [0, 1, 3, 4], 0.4)
    return t


@tex('mare', 32, 32)
def _mare(n, w, h, s):
    t = Tex(n, w, h, MARE)
    onde(t, 1, 3, 0)
    t.speckle([2], 0.08)
    return t


@tex('mare_basso', 32, 32)
def _mare_basso(n, w, h, s):
    t = Tex(n, w, h, [hexc('2c7aa0'), hexc('3c8eb0'), hexc('5aa8c4'), hexc('8ccadc'), hexc('d4eef4')])
    onde(t, 1, 3, 0, passo=8)
    t.speckle([2, 4], 0.06)
    return t


@tex('acqua_dolce', 32, 32)
def _acqua_dolce(n, w, h, s):
    t = Tex(n, w, h, [hexc('2a4a3a'), hexc('34604a'), hexc('46765a'), hexc('6a9a7a'), hexc('a8c8b0')])
    onde(t, 1, 3, 0, passo=8)
    t.speckle([2], 0.1)
    return t


@tex('fango', 32, 32)
def _fango(n, w, h, s):
    t = Tex(n, w, h, [hexc('3c3830'), hexc('4e483c'), hexc('62584a'), hexc('786c5a'), hexc('948670')])
    t.fill(2)
    rumore(t, [0, 1, 3], 0.3)
    for _ in range(5):
        cx, cy = t.rng.i(0, 31), t.rng.i(0, 31)
        t.disc(cx, cy, 2.5, 4, wrap=True)
        t.disc(cx, cy, 1.2, 0, wrap=True)
    return t


@tex('sciara', 32, 32)
def _sciara(n, w, h, s):
    t = Tex(n, w, h, LAVA + [hexc('7a5040')])
    pietre(t, [1, 2, 3, 2], 0, n=18, rmin=2, rmax=5)
    t.speckle([4, 5], 0.04)
    return t


@tex('cenere', 32, 32)
def _cenere(n, w, h, s):
    t = Tex(n, w, h, [hexc('4a4848'), hexc('5c5a5a'), hexc('6e6c6a'), hexc('82807c'), hexc('98948e')])
    t.fill(2)
    rumore(t, [0, 1, 3, 4], 0.45)
    return t


@tex('campo', 32, 32)
def _campo(n, w, h, s):
    t = Tex(n, w, h, [hexc('8a7234'), hexc('a68a40'), hexc('bea050'), hexc('d4b866'), hexc('6a7a34')])
    t.fill(2)
    for y in range(0, 32, 4):
        t.hline(0, y, 32, 1)
        for x in range(0, 32, 3):
            if t.rng.p(0.5):
                t.put(x, y + 2, 3)
    t.speckle([0, 4], 0.05)
    return t


@tex('argilla', 32, 32)
def _argilla(n, w, h, s):
    t = Tex(n, w, h, [hexc('6e6a5e'), hexc('847e70'), hexc('9a9484'), hexc('b0a896'), hexc('c4bca8')])
    t.fill(2)
    for x0 in range(0, 32, 6):
        x = x0
        for y in range(32):
            t.put(x, y, 0 if y % 7 else 1)
            x += 1 if t.rng.p(0.3) else 0
    rumore(t, [1, 3, 4], 0.2)
    return t


@tex('scoglio', 32, 32)
def _scoglio(n, w, h, s):
    t = Tex(n, w, h, LAVA + [hexc('2e5a7a')])
    pietre(t, [2, 3, 4, 3], 0, n=10, rmin=4, rmax=7)
    t.speckle([1], 0.08)
    return t


@tex('scalinata', 32, 32)
def _scalinata(n, w, h, s):
    # gradini di pietra con le alzate di maiolica (la Scalinata di Caltagirone)
    t = Tex(n, w, h, [hexc('7a6a50'), CALCARE[1], CALCARE[2], CALCARE[3], hexc('2a5ca8'), hexc('e8c040'),
                      hexc('f0f0e8'), hexc('3c8a5a')])
    for y0 in range(0, 32, 8):
        t.rect(0, y0, 32, 5, 2)
        t.hline(0, y0, 32, 3)
        t.rect(0, y0 + 5, 32, 3, 6)
        for x in range(0, 32, 4):
            t.put(x + 1, y0 + 6, 4)
            t.put(x + 2, y0 + 6, 5 if (x // 4 + y0 // 8) % 2 else 7)
            t.put(x + 3, y0 + 6, 4)
        t.hline(0, y0 + 7, 32, 0)
    t.speckle([1], 0.04)
    return t


@tex('piastrelle', 32, 32)
def _piastrelle(n, w, h, s):
    t = Tex(n, w, h, [hexc('7a6448'), hexc('d8ccb0'), hexc('ece2c8'), hexc('2a5ca8'), hexc('c8a030')])
    t.fill(2)
    for y0 in range(0, 32, 8):
        for x0 in range(0, 32, 8):
            t.frame(x0, y0, 8, 8, 1)
            t.put(x0 + 3, y0 + 3, 3)
            t.put(x0 + 4, y0 + 4, 3)
            t.put(x0 + 4, y0 + 3, 4)
            t.put(x0 + 3, y0 + 4, 4)
    return t


@tex('binario_v', 16, 32)
def _binario_v(n, w, h, s):
    t = Tex(n, w, h, [hexc('4a4038'), hexc('5c5048'), hexc('6e6258'), hexc('6a4a2c'), METALLO[2], METALLO[4]])
    t.fill(1)
    t.speckle([0, 2], 0.4)
    for y in range(0, 32, 6):
        t.rect(1, y, 14, 2, 3)
    t.rect(3, 0, 1, 32, 4)
    t.rect(12, 0, 1, 32, 4)
    t.vline(4, 0, 32, 5)
    t.vline(11, 0, 32, 5)
    return t


@tex('binario_h', 32, 16)
def _binario_h(n, w, h, s):
    t = Tex(n, w, h, [hexc('4a4038'), hexc('5c5048'), hexc('6e6258'), hexc('6a4a2c'), METALLO[2], METALLO[4]])
    t.fill(1)
    t.speckle([0, 2], 0.4)
    for x in range(0, 32, 6):
        t.rect(x, 1, 2, 14, 3)
    t.rect(0, 3, 32, 1, 4)
    t.rect(0, 12, 32, 1, 4)
    t.hline(0, 4, 32, 5)
    t.hline(0, 11, 32, 5)
    return t


@tex('ghiaia', 32, 32)
def _ghiaia(n, w, h, s):
    t = Tex(n, w, h, [hexc('5a5650'), hexc('726c64'), hexc('8a847a'), hexc('a49c90'), hexc('beb6a8')])
    t.fill(2)
    rumore(t, [0, 1, 3, 4], 0.7)
    return t


# ---- muri e facciate (32×32: un modulo ogni 2 caselle, l'altezza dei volumi è multipla di 32) --


def facciata(n, w, h, muro, cornice, finestra, persiana, balcone=None, zoccolo=None, righe=True):
    """Modulo di facciata: una finestra con persiane al centro, cornice in alto, zoccolo in basso."""
    pal = [muro[0], muro[1], muro[2], cornice, finestra, persiana, hexc('1a1a1e')]
    if balcone:
        pal.append(balcone)
    if zoccolo:
        pal.append(zoccolo)
    t = Tex(n, w, h, pal)
    t.fill(1)
    t.speckle([0, 2], 0.12)
    if righe:
        t.hline(0, 0, 32, 3)
        t.hline(0, 1, 32, 0)
    t.rect(11, 8, 10, 15, 3)        # cornice della finestra
    t.rect(12, 9, 8, 13, 4)         # vetro
    t.rect(12, 9, 2, 13, 5)         # persiane aperte
    t.rect(18, 9, 2, 13, 5)
    t.vline(16, 9, 13, 6)
    t.hline(10, 7, 12, 3)
    if balcone:
        b = len(pal) - (2 if zoccolo else 1)
        t.rect(9, 23, 14, 1, b)
        for x in range(9, 23, 2):
            t.vline(x, 20, 3, b)
        t.hline(9, 20, 14, b)
    if zoccolo:
        z = len(pal) - 1
        t.rect(0, 29, 32, 3, z)
    return t


@tex('fac_barocca', 32, 32)
def _fac_barocca(n, w, h, s):
    t = facciata(n, w, h, [hexc('c8b088'), hexc('dcc8a0'), hexc('ece0c0')], hexc('f8f0dc'),
                 hexc('3a4a5c'), hexc('5a7a4a'), balcone=hexc('2c2c2c'))
    # lesene ai lati del modulo
    t.rect(0, 2, 2, 30, 3)
    t.rect(30, 2, 2, 30, 3)
    return t


@tex('fac_lavica', 32, 32)
def _fac_lavica(n, w, h, s):
    # pietra lavica con le cornici di calcare bianco: il barocco di Catania
    t = facciata(n, w, h, [LAVA[1], LAVA[2], LAVA[3]], hexc('e8e0cc'), hexc('2c3a4a'), hexc('6a4a2e'),
                 balcone=hexc('1e1e1e'))
    t.rect(0, 2, 2, 30, 3)
    t.rect(30, 2, 2, 30, 3)
    return t


@tex('fac_intonaco', 32, 32)
def _fac_intonaco(n, w, h, s):
    return facciata(n, w, h, [hexc('c89a6a'), hexc('dcb07c'), hexc('e8c494')], hexc('f0e2c4'),
                    hexc('3a4250'), hexc('4a6a8a'), zoccolo=hexc('9a7a5a'))


@tex('fac_cemento', 32, 32)
def _fac_cemento(n, w, h, s):
    t = Tex(n, w, h, [hexc('5c5c5e'), hexc('747476'), hexc('8a8a8a'), hexc('2e3640'), hexc('3c3c3e'),
                      hexc('1a1a1a'), hexc('a0a09c'), hexc('6a5040')])
    t.fill(2)
    t.speckle([1, 6], 0.15)
    t.hline(0, 0, 32, 4)
    t.hline(0, 16, 32, 4)
    for y0 in (3, 19):
        t.rect(4, y0, 9, 8, 3)
        t.rect(19, y0, 9, 8, 3)
        t.hline(4, y0 + 8, 9, 1)
        t.hline(19, y0 + 8, 9, 1)
    # colature e cavi d'allaccio abusivo
    for x in (2, 15, 29):
        t.vline(x, 1, 30, 1)
    x = 8
    for y in range(32):
        t.put(x, y, 5)
        if y % 5 == 4:
            x += 1
    for xx in range(0, 32):
        t.put(xx, 13 + (1 if 10 < xx < 22 else 0), 5)
    t.speckle([7], 0.03)
    return t


@tex('fac_negozio', 32, 32)
def _fac_negozio(n, w, h, s):
    # piano terra: saracinesca e insegna; sopra intonaco
    t = Tex(n, w, h, [hexc('c89a6a'), hexc('dcb07c'), hexc('e8c494'), hexc('8a8e92'), hexc('a4a8ac'),
                      hexc('5a5e62'), hexc('b83a2a'), hexc('f0e8d0'), hexc('2a2e34')])
    t.fill(1)
    t.speckle([0, 2], 0.12)
    t.rect(0, 6, 32, 5, 6)
    for x in range(3, 29, 3):
        t.put(x, 8, 7)
        t.put(x + 1, 8, 7)
    t.rect(2, 12, 28, 20, 8)
    t.rect(3, 13, 26, 19, 4)
    for y in range(13, 32, 2):
        t.hline(3, y, 26, 3)
    t.hline(3, 31, 26, 5)
    return t


@tex('lamiera', 32, 32)
def _lamiera(n, w, h, s):
    t = Tex(n, w, h, METALLO + [hexc('8a5a3a'), hexc('6a4030')])
    for x in range(32):
        k = x % 4
        t.vline(x, 0, 32, (1, 2, 3, 2)[k])
    t.speckle([5, 6], 0.03)
    t.hline(0, 0, 32, 0)
    return t


@tex('vetrata', 32, 32)
def _vetrata(n, w, h, s):
    t = Tex(n, w, h, [hexc('2a3a4a'), hexc('3c5a74'), hexc('5a80a0'), hexc('8ab4cc'), hexc('c4dce8'),
                      METALLO[1], METALLO[3]])
    t.fill(2)
    for x in range(32):
        for y in range(32):
            if (x + y) % 16 < 3:
                t.put(x, y, 3)
            elif (x + y) % 16 == 3:
                t.put(x, y, 4)
    t.rect(0, 0, 32, 2, 5)
    t.rect(0, 0, 2, 32, 5)
    t.rect(15, 0, 2, 32, 6)
    t.rect(0, 15, 32, 2, 6)
    return t


@tex('muro_lavico', 32, 32)
def _muro_lavico(n, w, h, s):
    t = Tex(n, w, h, LAVA + [hexc('1c1c20')])
    pietre(t, [1, 2, 3, 2, 4], 5, n=22, rmin=3, rmax=6)
    return t


@tex('muro_calcare', 32, 32)
def _muro_calcare(n, w, h, s):
    t = Tex(n, w, h, [hexc('6a5e48')] + CALCARE)
    pietre(t, [2, 3, 4, 3, 5], 0, n=22, rmin=3, rmax=6)
    return t


@tex('roccia', 32, 32)
def _roccia(n, w, h, s):
    t = Tex(n, w, h, [hexc('4e4436'), hexc('6a5e4a'), hexc('86785e'), hexc('a09276'), hexc('bcae90')])
    t.fill(2)
    for x0 in range(0, 32, 5):
        x = x0
        for y in range(32):
            t.put(x, y, 0)
            t.put(x + 1, y, 3)
            if t.rng.p(0.25):
                x += 1
    t.speckle([1, 4], 0.1)
    for y in range(0, 32, 11):
        t.hline(0, y, 32, 1)
    return t


@tex('roccia_nera', 32, 32)
def _roccia_nera(n, w, h, s):
    t = Tex(n, w, h, LAVA + [hexc('7a4a3a')])
    t.fill(1)
    for x0 in range(0, 32, 4):
        x = x0
        for y in range(32):
            t.put(x, y, 0)
            t.put(x + 1, y, 3 if y % 3 else 2)
            if t.rng.p(0.3):
                x += 1
    t.speckle([4, 5], 0.05)
    return t


@tex('serbatoio', 32, 32)
def _serbatoio(n, w, h, s):
    t = Tex(n, w, h, [hexc('9aa0a4'), hexc('b4babe'), hexc('cdd2d4'), hexc('e2e6e6'), hexc('8a5a3a'),
                      hexc('6a7074'), hexc('c4a030')])
    t.fill(2)
    for y in range(0, 32, 8):
        t.hline(0, y, 32, 5)
    for x in range(0, 32, 2):
        t.vline(x, 0, 32, 1 if x % 8 == 0 else 2)
    t.hline(0, 4, 32, 6)
    for _ in range(6):
        x = t.rng.i(0, 31)
        t.vline(x, t.rng.i(8, 20), t.rng.i(3, 9), 4)
    return t


# ---- tetti --------------------------------------------------------------------------------


@tex('tetto_coppi', 32, 32)
def _tetto_coppi(n, w, h, s):
    t = Tex(n, w, h, COTTO + [hexc('5a2614')])
    t.fill(2)
    for y0 in range(0, 32, 4):
        off = 2 if (y0 // 4) % 2 else 0
        for x0 in range(0, 32, 4):
            x = x0 + off
            t.put(x, y0, 3)
            t.put(x + 1, y0, 3)
            t.put(x + 1, y0 + 1, 2)
            t.put(x + 3, y0 + 2, 1)
            t.put(x + 3, y0 + 3, 4)
            t.put(x, y0 + 3, 0)
    t.speckle([1], 0.05)
    return t


@tex('tetto_piano', 32, 32)
def _tetto_piano(n, w, h, s):
    # terrazza: cocciopesto chiaro a quadrotti, tipico dei tetti piani siciliani
    t = Tex(n, w, h, [hexc('9a8c78'), hexc('b4a690'), hexc('c8bca6'), hexc('dcd2bc'), hexc('8a6a4a')])
    t.fill(2)
    lastre(t, 8, 8, 1, sfalsa=False, vari=(2, 3, 2))
    t.speckle([0, 4], 0.04)
    return t


@tex('tetto_cemento', 32, 32)
def _tetto_cemento(n, w, h, s):
    # lastrico di cemento con i serbatoi dell'acqua e le parabole
    t = Tex(n, w, h, [hexc('545456'), hexc('6c6c6e'), hexc('828282'), hexc('9a9a98'), hexc('4a6ab0'),
                      hexc('2c4a8a'), hexc('d8d8d4'), hexc('1a1a1a')])
    t.fill(2)
    t.speckle([1, 3], 0.25)
    t.rect(4, 5, 7, 5, 4)
    t.hline(4, 5, 7, 5)
    t.rect(19, 18, 6, 4, 4)
    t.hline(19, 18, 6, 5)
    t.disc(24, 7, 3, 6)
    t.put(24, 7, 7)
    t.hline(0, 26, 32, 7)
    return t


# ---- porte (aperture disegnate sulla facciata) -------------------------------------------


@tex('porta', 16, 32)
def _porta(n, w, h, s):
    t = Tex(n, w, h, [hexc('2a1a10'), LEGNO[1], LEGNO[2], LEGNO[3], hexc('f0e2c4'), hexc('d8b040'),
                      hexc('8a8a8a')])
    t.fill(4)
    t.rect(2, 6, 12, 26, 0)
    t.rect(3, 7, 10, 25, 1)
    t.rect(4, 8, 3, 10, 2)
    t.rect(9, 8, 3, 10, 2)
    t.rect(4, 20, 3, 10, 2)
    t.rect(9, 20, 3, 10, 2)
    t.vline(8, 7, 25, 0)
    t.put(10, 19, 5)
    t.hline(1, 4, 14, 3)
    t.rect(0, 31, 16, 1, 6)
    return t


@tex('porta_vetro', 16, 32)
def _porta_vetro(n, w, h, s):
    t = Tex(n, w, h, [METALLO[0], METALLO[2], hexc('3c5a74'), hexc('8ab4cc'), hexc('c4dce8'), hexc('dcdcdc')])
    t.fill(5)
    t.rect(1, 4, 14, 28, 0)
    t.rect(2, 5, 12, 27, 2)
    for k in range(10):
        t.put(3 + k, 6 + k, 3)
        t.put(4 + k, 6 + k, 4)
    t.vline(8, 5, 27, 1)
    return t


@tex('saracinesca', 16, 32)
def _saracinesca(n, w, h, s):
    t = Tex(n, w, h, METALLO + [hexc('2a2a2a'), hexc('7a4a30')])
    t.fill(2)
    t.rect(0, 0, 16, 4, 5)
    for y in range(4, 32, 2):
        t.hline(0, y, 16, 1)
    t.vline(0, 4, 28, 0)
    t.vline(15, 4, 28, 0)
    t.speckle([6], 0.04)
    return t


@tex('portone', 32, 32)
def _portone(n, w, h, s):
    # portale ad arco di pietra chiara col portone di legno (chiese, palazzi, castelli)
    t = Tex(n, w, h, [CALCARE[1], CALCARE[2], CALCARE[3], hexc('2a1a10'), LEGNO[1], LEGNO[2], hexc('d8b040')])
    t.fill(2)
    t.speckle([0, 1], 0.1)
    t.rect(6, 12, 20, 20, 3)
    t.disc(16, 12, 10, 3)
    t.rect(8, 13, 16, 19, 4)
    t.disc(16, 13, 8, 4)
    t.vline(16, 6, 26, 3)
    for y in range(14, 32, 5):
        t.hline(8, y, 16, 5)
    t.put(14, 22, 6)
    t.put(18, 22, 6)
    for x in range(2, 30, 2):
        t.put(x, 1, 0)
    return t


@tex('imbocco', 32, 32)
def _imbocco(n, w, h, s):
    # bocca di grotta o di galleria: arco scuro nella roccia
    t = Tex(n, w, h, [hexc('0c0c10'), hexc('1c1a1c'), hexc('4e4436'), hexc('6a5e4a'), hexc('86785e')])
    t.fill(3)
    t.speckle([2, 4], 0.2)
    t.rect(7, 14, 18, 18, 1)
    t.disc(16, 14, 9, 1)
    t.rect(9, 15, 14, 17, 0)
    t.disc(16, 15, 7, 0)
    return t


# ---- sagome (indice 0 trasparente) --------------------------------------------------------


def chioma(t, cx, cy, rx, ry, colori, scuro):
    t.disc(cx, cy, rx, colori[0], ry=ry)
    t.disc(cx - 1, cy - 1, rx - 1.5, colori[1], ry=ry - 1.5)
    for _ in range(int(rx * ry)):
        x = t.rng.i(int(cx - rx), int(cx + rx))
        y = t.rng.i(int(cy - ry), int(cy + ry))
        if t.get(x, y) in colori:
            t.put(x, y, colori[t.rng.u32() % len(colori)], wrap=False)
    for x in range(int(cx - rx), int(cx + rx) + 1):
        for y in range(int(cy), int(cy + ry) + 1):
            if t.get(x, y) and t.get(x, y + 1) == 0 and y + 1 < t.h:
                t.put(x, y, scuro, wrap=False)


@tex('albero', 32, 32, sagoma=True)
def _albero(n, w, h, s):
    # ulivo / carrubo: tronco nodoso e chioma argentata
    t = Tex(n, w, h, [(0, 0, 0), LEGNO[0], LEGNO[1], hexc('2e4a26'), hexc('46643a'), hexc('62804e'),
                      hexc('8aa070'), hexc('1e3418')], sagoma=True)
    t.rect(14, 20, 4, 12, 2)
    t.vline(14, 20, 12, 1)
    t.put(13, 30, 2)
    t.put(18, 31, 2)
    chioma(t, 16, 13, 13, 10, [4, 5, 6, 5], 7)
    chioma(t, 9, 16, 6, 5, [3, 4, 5], 7)
    return t


@tex('pino', 32, 32, sagoma=True)
def _pino(n, w, h, s):
    # pino domestico o laricio: fusto alto e chioma a ombrello
    t = Tex(n, w, h, [(0, 0, 0), LEGNO[0], LEGNO[2], FOGLIA[0], FOGLIA[1], FOGLIA[2], FOGLIA[3]], sagoma=True)
    t.rect(15, 12, 3, 20, 2)
    t.vline(15, 12, 20, 1)
    chioma(t, 16, 8, 14, 7, [4, 5, 6, 5], 3)
    return t


@tex('palma', 16, 32, sagoma=True)
def _palma(n, w, h, s):
    t = Tex(n, w, h, [(0, 0, 0), hexc('6a5030'), hexc('8a6a40'), FOGLIA[1], FOGLIA[2], FOGLIA[3]], sagoma=True)
    for y in range(8, 32):
        t.put(7 + (1 if y < 18 else 0), y, 1 if y % 3 == 0 else 2, wrap=False)
        t.put(8 + (1 if y < 18 else 0), y, 2, wrap=False)
    for k, (dx, dy) in enumerate(((-7, 3), (7, 3), (-6, -2), (6, -2), (-2, -6), (3, -6))):
        for i in range(8):
            x = 8 + dx * i / 7
            y = 7 + dy * i / 7 + (i * i) / 16
            t.put(int(x), int(y), 3 + (i % 3), wrap=False)
            t.put(int(x), int(y) + 1, 3, wrap=False)
    return t


@tex('cipresso', 16, 32, sagoma=True)
def _cipresso(n, w, h, s):
    t = Tex(n, w, h, [(0, 0, 0), LEGNO[0], FOGLIA[0], FOGLIA[1], FOGLIA[2]], sagoma=True)
    t.rect(7, 28, 2, 4, 1)
    for y in range(1, 29):
        r = min(4.5, 1 + y / 4) if y < 18 else 4.5 - (y - 18) / 5
        t.hline(int(8 - r), y, int(2 * r), 3, wrap=False)
        t.put(int(8 - r), y, 2, wrap=False)
        if y % 3 == 0:
            t.put(8 + int(r) - 2, y, 4, wrap=False)
    return t


@tex('fico_india', 16, 16, sagoma=True)
def _fico_india(n, w, h, s):
    t = Tex(n, w, h, [(0, 0, 0), hexc('3a6a3a'), hexc('4e8448'), hexc('6aa05a'), hexc('d84a2a'),
                      hexc('e8a030')], sagoma=True)
    for cx, cy, r in ((8, 11, 4), (4, 7, 3), (11, 5, 3), (8, 3, 2.5)):
        t.disc(cx, cy, r, 2, ry=r * 1.2)
        t.disc(cx - 1, cy - 1, r - 1.5, 3, ry=(r - 1.5) * 1.2)
    for x, y in ((6, 3), (13, 2), (2, 4), (9, 1)):
        t.put(x, y, 4 if x % 2 else 5, wrap=False)
    return t


@tex('cespuglio', 16, 16, sagoma=True)
def _cespuglio(n, w, h, s):
    t = Tex(n, w, h, [(0, 0, 0), FOGLIA[0], FOGLIA[1], FOGLIA[2], FOGLIA[3], FOGLIA[4]], sagoma=True)
    chioma(t, 8, 9, 7, 6, [2, 3, 4, 5], 1)
    return t


def palo(t, x, y0, y1, c, cc=None):
    for y in range(y0, y1):
        t.put(x, y, c, wrap=False)
        if cc:
            t.put(x + 1, y, cc, wrap=False)


@tex('lampione', 16, 32, sagoma=True)
def _lampione(n, w, h, s):
    t = Tex(n, w, h, [(0, 0, 0), hexc('2a2e32'), hexc('4a5056'), hexc('f8e8a0'), hexc('fff8d8')], sagoma=True)
    palo(t, 7, 6, 32, 1, 2)
    t.rect(5, 30, 6, 2, 1)
    t.hline(4, 5, 8, 1)
    t.rect(3, 2, 10, 3, 2)
    t.hline(4, 5, 8, 3)
    t.put(7, 6, 4)
    t.put(8, 6, 4)
    return t


def scatola(t, x, y, w, h, faccia, lato, cima, bordo):
    t.rect(x, y, w, h, faccia, wrap=False)
    t.rect(x, y, w, 2, cima, wrap=False)
    t.vline(x + w - 1, y + 2, h - 2, lato, wrap=False)
    t.frame(x, y, w, h, bordo, wrap=False)


@tex('cassonetto', 16, 16, sagoma=True)
def _cassonetto(n, w, h, s):
    t = Tex(n, w, h, [(0, 0, 0), hexc('1e2a1e'), hexc('2e5a3a'), hexc('3c7448'), hexc('5a9060'),
                      hexc('1a1a1a')], sagoma=True)
    scatola(t, 1, 4, 14, 10, 3, 2, 4, 1)
    t.put(3, 14, 5)
    t.put(12, 14, 5)
    t.put(3, 15, 5)
    t.put(12, 15, 5)
    return t


@tex('cass_brucia', 16, 16, sagoma=True)
def _cass_brucia(n, w, h, s):
    # cassonetto bruciato: plastica fusa e annerita
    t = Tex(n, w, h, [(0, 0, 0), hexc('121212'), hexc('2a2a2a'), hexc('3e3a36'), hexc('5a4a3a'),
                      hexc('2e5a3a'), hexc('8a8a8a')], sagoma=True)
    scatola(t, 1, 6, 14, 8, 2, 1, 3, 1)
    for x in range(1, 15):
        t.put(x, 6 + (x * 7 % 3), 0, wrap=False)
    t.speckle([4, 5], 0.15, (2, 8, 12, 5), wrap=False)
    t.put(5, 4, 6)
    t.put(6, 3, 6)
    t.put(9, 2, 6)
    return t


@tex('sacchi', 16, 16, sagoma=True)
def _sacchi(n, w, h, s):
    # i sacchi della spazzatura attorno ai Munnizza
    t = Tex(n, w, h, [(0, 0, 0), hexc('121216'), hexc('24242c'), hexc('3a3a46'), hexc('5a5a6a'),
                      hexc('5a7a3a'), hexc('c4c4b4')], sagoma=True)
    for cx, cy, r in ((5, 11, 4), (11, 11, 4), (8, 7, 3.5), (13, 6, 2.5)):
        t.disc(cx, cy, r, 3)
        t.disc(cx - 1, cy - 1, r - 1.5, 4)
        t.put(int(cx), int(cy - r), 2)
    t.put(3, 14, 5)
    t.put(4, 14, 6)
    t.put(12, 15, 6)
    return t


@tex('motorino', 16, 16, sagoma=True)
def _motorino(n, w, h, s):
    t = Tex(n, w, h, [(0, 0, 0), hexc('1a1a1a'), hexc('4a4a4a'), hexc('b82a2a'), hexc('d84a3a'),
                      hexc('c4c4c4')], sagoma=True)
    t.disc(3.5, 12.5, 2.5, 1)
    t.disc(12.5, 12.5, 2.5, 1)
    t.disc(3.5, 12.5, 1, 2)
    t.disc(12.5, 12.5, 1, 2)
    t.rect(5, 8, 7, 4, 3)
    t.rect(6, 7, 5, 2, 4)
    t.rect(4, 6, 4, 2, 1)
    t.vline(12, 4, 7, 2)
    t.hline(11, 4, 3, 5)
    return t


@tex('auto', 32, 16, sagoma=True)
def _auto(n, w, h, s):
    # l'auto blu di via Santa Filomena
    t = Tex(n, w, h, [(0, 0, 0), hexc('0e0e14'), hexc('1a2a5a'), hexc('2a3e7a'), hexc('3c56a0'),
                      hexc('8ab4cc'), hexc('c4c4c4'), hexc('e8d040')], sagoma=True)
    t.rect(2, 7, 28, 6, 3)
    t.rect(8, 3, 15, 5, 4)
    t.rect(10, 4, 5, 3, 5)
    t.rect(16, 4, 5, 3, 5)
    t.hline(2, 12, 28, 2)
    t.disc(8, 13, 2.6, 1)
    t.disc(24, 13, 2.6, 1)
    t.put(8, 13, 6)
    t.put(24, 13, 6)
    t.put(29, 9, 7)
    t.put(2, 9, 6)
    return t


@tex('tavolino', 16, 16, sagoma=True)
def _tavolino(n, w, h, s):
    # tavolini e sedie dei locali di via Gemmellaro
    t = Tex(n, w, h, [(0, 0, 0), hexc('2a2a2a'), METALLO[2], hexc('f0f0e8'), hexc('b83a2a'),
                      hexc('8a6a40')], sagoma=True)
    t.disc(8, 6, 5, 3, ry=2)
    palo(t, 8, 7, 14, 1)
    t.hline(6, 14, 5, 1)
    for x0 in (1, 13):
        t.rect(x0, 8, 2, 4, 5)
        palo(t, x0, 12, 16, 1)
        palo(t, x0 + 1, 12, 16, 1)
    t.put(8, 5, 4)
    return t


@tex('braciere', 16, 16, sagoma=True)
def _braciere(n, w, h, s):
    # le braci di via Plebiscito: griglia, carbone acceso e fumo
    t = Tex(n, w, h, [(0, 0, 0), hexc('1a1a1a'), hexc('3a3a3a'), hexc('d83a1a'), hexc('f8a030'),
                      hexc('a0a0a0'), hexc('c8c8c8')], sagoma=True)
    t.rect(2, 9, 12, 3, 2)
    t.hline(2, 9, 12, 1)
    for x in range(3, 13, 2):
        t.put(x, 10, 3 if x % 4 == 1 else 4)
    palo(t, 3, 12, 16, 1)
    palo(t, 12, 12, 16, 1)
    for y in range(0, 8):
        t.put(7 + (y % 3) - 1, y, 5 if y > 3 else 6, wrap=False)
        t.put(9 + (y % 2), y + 1, 5, wrap=False)
    return t


@tex('cartello', 16, 16, sagoma=True)
def _cartello(n, w, h, s):
    t = Tex(n, w, h, [(0, 0, 0), hexc('2a2e32'), hexc('f0f0e8'), hexc('2a5ca8'), hexc('b83a2a'),
                      hexc('5a5e62')], sagoma=True)
    palo(t, 7, 8, 16, 5, 1)
    t.rect(1, 1, 14, 8, 3)
    t.frame(1, 1, 14, 8, 2)
    for x in range(3, 13, 2):
        t.put(x, 4, 2)
    t.hline(3, 6, 6, 2)
    return t


@tex('ringhiera', 16, 16, sagoma=True)
def _ringhiera(n, w, h, s):
    t = Tex(n, w, h, [(0, 0, 0), hexc('1e1e22'), hexc('3a3a42')], sagoma=True)
    t.rect(0, 4, 16, 2, 2)
    t.hline(0, 4, 16, 1)
    t.rect(0, 14, 16, 1, 1)
    for x in range(1, 16, 3):
        t.vline(x, 6, 8, 1)
    return t


@tex('recinzione', 16, 32, sagoma=True)
def _recinzione(n, w, h, s):
    # rete metallica con filo spinato: polo, base NATO, MUOS
    t = Tex(n, w, h, [(0, 0, 0), METALLO[0], METALLO[2], METALLO[3]], sagoma=True)
    for y in range(6, 32):
        for x in range(16):
            if (x + y) % 4 == 0 or (x - y) % 4 == 0:
                t.put(x, y, 2)
    palo(t, 0, 2, 32, 1)
    t.hline(0, 6, 16, 1)
    for x in range(0, 16, 2):
        t.put(x, 3 + (x // 2) % 2, 3)
    return t


@tex('traliccio', 16, 32, sagoma=True)
def _traliccio(n, w, h, s):
    t = Tex(n, w, h, [(0, 0, 0), METALLO[0], METALLO[2], hexc('d83a2a')], sagoma=True)
    for y in range(0, 32):
        half = 1 + y * 6 // 31
        t.put(8 - half, y, 1, wrap=False)
        t.put(7 + half, y, 1, wrap=False)
        if y % 5 == 0:
            t.hline(8 - half, y, 2 * half, 2, wrap=False)
        if y % 5 == 2:
            t.put(8 - half // 2, y, 2, wrap=False)
            t.put(7 + half // 2, y, 2, wrap=False)
    t.rect(4, 3, 8, 1, 2)
    t.put(8, 0, 3)
    return t


@tex('barca', 32, 16, sagoma=True)
def _barca(n, w, h, s):
    # barca di pescatori (le «varche» di Aci Trezza e Marzamemi)
    t = Tex(n, w, h, [(0, 0, 0), hexc('1a2a4a'), hexc('2a5ca8'), hexc('f0f0e8'), hexc('d8b040'),
                      hexc('b83a2a'), LEGNO[1]], sagoma=True)
    for y in range(8, 15):
        k = y - 8
        t.hline(2 + k, y, 28 - 2 * k, 2 if y > 10 else 3, wrap=False)
    t.hline(2, 8, 28, 4)
    t.hline(3, 10, 26, 5)
    palo(t, 15, 1, 8, 6)
    t.hline(12, 3, 7, 6)
    return t


@tex('statua', 16, 32, sagoma=True)
def _statua(n, w, h, s):
    # statua su piedistallo (Archimede, monumenti)
    t = Tex(n, w, h, [(0, 0, 0), hexc('3a4a3a'), hexc('4e6450'), hexc('6a8268'), CALCARE[1], CALCARE[3]],
            sagoma=True)
    t.rect(3, 22, 10, 10, 4)
    t.rect(3, 22, 10, 2, 5)
    t.disc(8, 5, 2.5, 3)
    t.rect(6, 8, 5, 8, 2)
    t.rect(5, 9, 1, 6, 2)
    t.rect(11, 6, 1, 6, 3)
    t.rect(6, 16, 2, 6, 1)
    t.rect(9, 16, 2, 6, 1)
    return t


@tex('liotru', 16, 32, sagoma=True)
def _liotru(n, w, h, s):
    # u Liotru: l'elefante di pietra lavica con l'obelisco, simbolo di Catania
    t = Tex(n, w, h, [(0, 0, 0), LAVA[0], LAVA[1], LAVA[3], hexc('e8e0cc'), hexc('c8b088'), hexc('d8b040')],
            sagoma=True)
    t.rect(2, 27, 12, 5, 5)
    t.hline(2, 27, 12, 4)
    t.rect(3, 20, 10, 5, 2)
    t.disc(3.5, 20, 2.5, 2)
    t.vline(1, 20, 6, 2)
    t.rect(4, 25, 2, 2, 1)
    t.rect(10, 25, 2, 2, 1)
    t.hline(4, 20, 8, 3)
    t.rect(4, 18, 8, 2, 4)
    t.rect(7, 2, 2, 16, 5)
    t.vline(8, 2, 16, 4)
    t.put(7, 1, 6)
    t.put(8, 0, 6)
    return t


@tex('insegna', 32, 16, sagoma=True)
def _insegna(n, w, h, s):
    # insegna luminosa di un locale (il Cubbar e gli altri): scritta illeggibile a quella distanza
    t = Tex(n, w, h, [(0, 0, 0), hexc('14141c'), hexc('c83ac8'), hexc('f070f0'), hexc('40d8e8'), hexc('f8f8f8')],
            sagoma=True)
    t.rect(1, 3, 30, 10, 1)
    t.frame(1, 3, 30, 10, 2)
    for i, x in enumerate(range(4, 28, 4)):
        t.rect(x, 6, 3, 4, 3 if i % 2 else 4)
        t.put(x + 1, 7, 5)
    palo(t, 4, 13, 16, 1)
    palo(t, 27, 13, 16, 1)
    return t


@tex('ombrellone', 16, 32, sagoma=True)
def _ombrellone(n, w, h, s):
    t = Tex(n, w, h, [(0, 0, 0), hexc('6a6a6a'), hexc('d84a2a'), hexc('f0e8d0'), hexc('e8c040'),
                      hexc('2a5ca8')], sagoma=True)
    palo(t, 8, 8, 30, 1)
    for y in range(2, 9):
        r = (y - 1) * 1.1
        for x in range(int(8 - r), int(8 + r) + 1):
            t.put(x, y, 2 if (x // 2) % 2 else 3, wrap=False)
    t.rect(1, 28, 12, 3, 5)
    t.hline(1, 28, 12, 4)
    return t


@tex('torcia', 16, 32, sagoma=True)
def _torcia(n, w, h, s):
    # la torcia del polo petrolchimico: ciminiera a traliccio con la fiamma
    t = Tex(n, w, h, [(0, 0, 0), METALLO[0], METALLO[2], hexc('d83a1a'), hexc('f88a20'), hexc('f8e070'),
                      hexc('6a6a6a')], sagoma=True)
    t.rect(7, 10, 3, 22, 2)
    t.vline(7, 10, 22, 1)
    for y in range(12, 32, 4):
        t.hline(5, y, 7, 1)
    t.disc(8, 6, 3.5, 3, ry=5)
    t.disc(8, 6, 2.5, 4, ry=4)
    t.disc(8, 7, 1.2, 5, ry=2)
    t.put(6, 0, 6)
    t.put(9, 1, 6)
    return t


@tex('parabola', 16, 16, sagoma=True)
def _parabola(n, w, h, s):
    t = Tex(n, w, h, [(0, 0, 0), METALLO[0], METALLO[2], METALLO[4], hexc('d8d8d4')], sagoma=True)
    t.disc(8, 6, 6, 3, ry=5)
    t.disc(9, 6, 4, 4, ry=3.5)
    t.vline(8, 11, 5, 1)
    t.put(4, 6, 2)
    t.hline(6, 15, 5, 1)
    return t


# --------------------------------------------------------------------------- aree
# Tileset unico della matrice 0 (R-GFX-18): 4.2 usa questi 70 nomi; il 4.3 aggiunge i suoi.
SICILIA_4_2 = [
    # terreni
    'basolato', 'lastricato', 'asfalto', 'marciapiede', 'erba', 'erba_alta', 'fiori', 'terra', 'sabbia',
    'sabbia_nera', 'mare', 'mare_basso', 'acqua_dolce', 'fango', 'sciara', 'cenere', 'campo', 'argilla',
    'scoglio', 'scalinata', 'piastrelle', 'binario_v', 'binario_h', 'ghiaia',
    # muri e facciate
    'fac_barocca', 'fac_lavica', 'fac_intonaco', 'fac_cemento', 'fac_negozio', 'lamiera', 'vetrata',
    'muro_lavico', 'muro_calcare', 'roccia', 'roccia_nera', 'serbatoio',
    # tetti
    'tetto_coppi', 'tetto_piano', 'tetto_cemento',
    # porte
    'porta', 'porta_vetro', 'saracinesca', 'portone', 'imbocco',
    # sagome
    'albero', 'pino', 'palma', 'cipresso', 'fico_india', 'cespuglio', 'lampione', 'cassonetto',
    'cass_brucia', 'sacchi', 'motorino', 'auto', 'tavolino', 'braciere', 'cartello', 'ringhiera',
    'recinzione', 'traliccio', 'barca', 'statua', 'liotru', 'insegna', 'ombrellone', 'torcia', 'parabola',
]

GIALLO = hexc('e8d060')


def ingiallisci(t, forza=0.32):
    """Variante della tinta gialla del polo petrolchimico (documento 4.1 §10): stessi indici,
    colori spostati verso il giallo nella scala 555."""
    t.pal = [mix(c, GIALLO, forza) if (i or not t.sagoma) else c for i, c in enumerate(t.pal)]
    return t


def salva(nomi, cartella, variante=None):
    os.makedirs(cartella, exist_ok=True)
    out = {}
    for n in nomi:
        t = disegna(n)
        if variante == 'giallo':
            ingiallisci(t)
        t.png(os.path.join(cartella, n + '.png'))
        out[n] = t
    return out
