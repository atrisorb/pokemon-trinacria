"""Blocco 4.6 — il «figurino» che disegna le immagini di lotta e i ritratti delle transizioni (R-GFX-17).

Stesse schede e stessi 16 ruoli di colore del manichino del 4.5 (tools/grafica/4.5/omino45.py, schede45.py):
un personaggio ha lo stesso aspetto in campo, in lotta e nella transizione. Tre viste:

  fronte(scheda, posa)        80×80, figura intera di fronte (immagini frontali, files/a/0/5/8)
  retro(scheda, fase)         80×80, mezza figura di spalle che lancia la Poké Ball (dorsi, files/a/0/0/6)
  ritratto(scheda, verso)     96×64, testa e spalle (ritratti delle transizioni, files/a/1/0/9)

Ogni vista restituisce una lista di indici di palette 0–15 riga per riga. Il disegno è fatto di parti (ellissi,
poligoni, capsule): ogni parte si riempie col suo ruolo, prende l'ombra sul lato destro (luce da sinistra) e un
contorno scuro sul bordo; le parti disegnate dopo coprono quelle di prima. Niente è copiato o ricalcato dalle
immagini di HeartGold: di loro si tengono solo le misure dei fotogrammi. Solo libreria standard."""
import math
import os
import sys

QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(QUI, '..', '4.5'))
from omino45 import RUOLI, OMBRA      # noqa: E402  (ruoli condivisi col 4.5, R-GFX-35)

N4 = ((1, 0), (-1, 0), (0, 1), (0, -1))


# ------------------------------------------------------------------------------------------------ tela

class Tela:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.m = [['T'] * w for _ in range(h)]

    def dentro(self, x, y):
        return 0 <= x < self.w and 0 <= y < self.h

    def p(self, x, y, r):
        if self.dentro(x, y):
            self.m[y][x] = r

    def g(self, x, y):
        return self.m[y][x] if self.dentro(x, y) else 'T'

    def parte(self, mask, r, ombra=0, basso=0, bordo=True):
        """Riempie `mask` col ruolo r; i pixel a meno di `ombra` dal bordo destro (o `basso` dal bordo inferiore)
        prendono l'ombra del ruolo; il bordo della parte (verso pixel della tela fuori dalla parte) è contorno."""
        mask = {q for q in mask if self.dentro(*q)}

        def fuori(x, y):
            return self.dentro(x, y) and (x, y) not in mask
        sh = OMBRA.get(r)
        for x, y in mask:
            q = r
            if sh:
                if ombra and any(fuori(x + k, y) for k in range(1, ombra + 1)):
                    q = sh
                elif basso and any(fuori(x, y + k) for k in range(1, basso + 1)):
                    q = sh
            self.m[y][x] = q
        if bordo:
            for x, y in mask:
                if any(fuori(x + a, y + b) for a, b in N4):
                    self.m[y][x] = 'O'
        return mask

    def segna(self, pts, r):
        for x, y in pts:
            self.p(x, y, r)

    def indici(self):
        return [RUOLI[c] for row in self.m for c in row]


# ----------------------------------------------------------------------------------------------- forme

def _f(v):
    return int(math.floor(v))


def ellisse(cx, cy, rx, ry):
    s = set()
    for y in range(_f(cy - ry) - 1, _f(cy + ry) + 2):
        for x in range(_f(cx - rx) - 1, _f(cx + rx) + 2):
            dx, dy = (x + 0.5 - cx) / rx, (y + 0.5 - cy) / ry
            if dx * dx + dy * dy <= 1.0:
                s.add((x, y))
    return s


def poligono(pts):
    s = set()
    ys = [p[1] for p in pts]
    n = len(pts)
    for y in range(_f(min(ys)), _f(max(ys)) + 1):
        yc = y + 0.5
        xs = []
        for i in range(n):
            (x0, y0), (x1, y1) = pts[i], pts[(i + 1) % n]
            if (y0 <= yc < y1) or (y1 <= yc < y0):
                xs.append(x0 + (yc - y0) * (x1 - x0) / (y1 - y0))
        xs.sort()
        for a, b in zip(xs[0::2], xs[1::2]):
            for x in range(int(math.ceil(a - 0.5)), _f(b - 0.5) + 1):
                s.add((x, y))
    return s


def capsula(x0, y0, x1, y1, r0, r1=None):
    """Segmento spesso (raggio r0 all'inizio, r1 alla fine)."""
    r1 = r0 if r1 is None else r1
    s = set()
    R = max(r0, r1)
    vx, vy = x1 - x0, y1 - y0
    L = vx * vx + vy * vy
    for y in range(_f(min(y0, y1) - R) - 1, _f(max(y0, y1) + R) + 2):
        for x in range(_f(min(x0, x1) - R) - 1, _f(max(x0, x1) + R) + 2):
            px, py = x + 0.5, y + 0.5
            t = 0.0 if L == 0 else max(0.0, min(1.0, ((px - x0) * vx + (py - y0) * vy) / L))
            qx, qy = x0 + t * vx, y0 + t * vy
            r = r0 + (r1 - r0) * t
            if (px - qx) ** 2 + (py - qy) ** 2 <= r * r:
                s.add((x, y))
    return s


def rett(x0, y0, x1, y1):
    return {(x, y) for y in range(_f(min(y0, y1)), _f(max(y0, y1)) + 1)
            for x in range(_f(min(x0, x1)), _f(max(x0, x1)) + 1)}


def linea(x0, y0, x1, y1):
    x0, y0, x1, y1 = (int(round(v)) for v in (x0, y0, x1, y1))
    pts = set()
    dx, dy = abs(x1 - x0), -abs(y1 - y0)
    sx, sy = (1 if x0 < x1 else -1), (1 if y0 < y1 else -1)
    e = dx + dy
    while True:
        pts.add((x0, y0))
        if x0 == x1 and y0 == y1:
            return pts
        e2 = 2 * e
        if e2 >= dy:
            e += dy
            x0 += sx
        if e2 <= dx:
            e += dx
            y0 += sy


def arco(cx, cy, rx, ry, a0, a1, passo=None):
    """Punti di un arco d'ellisse fra gli angoli a0 e a1 (gradi, 0 = destra, 90 = in basso)."""
    passo = passo or max(2, int(abs(a1 - a0) * max(rx, ry) / 40))
    pts = []
    for k in range(passo + 1):
        a = math.radians(a0 + (a1 - a0) * k / passo)
        pts.append((cx + rx * math.cos(a), cy + ry * math.sin(a)))
    return pts


def sopra(mask, y):
    return {q for q in mask if q[1] <= y}


def sotto(mask, y):
    return {q for q in mask if q[1] >= y}


def tratto(pts, spessore=0.6):
    s = set()
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        s |= capsula(x0, y0, x1, y1, spessore)
    return s


# ------------------------------------------------------------------------------------------------ testa

class Testa:
    def __init__(self, cx, cy, rx, ry):
        self.cx, self.cy, self.rx, self.ry = cx, cy, rx, ry

    @property
    def grande(self):
        return self.rx >= 11


def acc(s, nome):
    return nome in s.get('accessori', ())


CAPPELLI = ('casco', 'capitano', 'paglia', 'berretto_lana', 'berretto', 'berretto_rovescio', 'fedora')


def cappello(s):
    for c in CAPPELLI:
        if acc(s, c):
            return c
    return None


def capelli_dietro(t, s, h, vista):
    """Ciocche che stanno dietro la testa e le spalle (vanno disegnate prima del corpo)."""
    c, cx, cy, rx, ry = s['capelli'], h.cx, h.cy, h.rx, h.ry
    om = max(1, int(rx / 5))
    if c == 'lunghi':
        if vista == 'fronte':
            t.parte(ellisse(cx, cy + 0.45 * ry, 1.22 * rx, 1.45 * ry), 'HA', ombra=om)
        elif vista == 'ritratto':
            t.parte(poligono([(cx - 1.25 * rx, cy - 0.2 * ry), (cx + 1.25 * rx, cy - 0.2 * ry),
                              (cx + 1.45 * rx, cy + 1.9 * ry), (cx - 1.45 * rx, cy + 1.9 * ry)]), 'HA', ombra=om)
    elif c == 'caschetto' and vista != 'retro':
        t.parte(sopra(ellisse(cx, cy, 1.14 * rx, 1.04 * ry), cy + 0.82 * ry), 'HA', ombra=om)
    elif c == 'cotonati' and vista != 'retro':
        t.parte(sopra(ellisse(cx, cy - 0.18 * ry, 1.4 * rx, 1.12 * ry), cy + 0.6 * ry), 'HA', ombra=om)
    elif c == 'coda' and vista != 'retro':
        lato = 1
        t.parte(ellisse(cx + lato * 1.02 * rx, cy + 0.42 * ry, 0.34 * rx, 0.95 * ry), 'HA', ombra=om)


def orecchie(t, h):
    for lato in (-1, 1):
        t.parte(ellisse(h.cx + lato * 0.98 * h.rx, h.cy + 0.12 * h.ry, 0.24 * h.rx, 0.3 * h.ry), 'SK',
                ombra=1 if lato > 0 else 0)


def faccia(t, s, h, espr, verso):
    """Viso visto di fronte: pelle, barba, occhi, sopracciglia, naso, bocca, baffi."""
    cx, cy, rx, ry, G = h.cx, h.cy, h.rx, h.ry, h.grande
    orecchie(t, h)
    viso = ellisse(cx, cy, rx, ry)
    t.parte(viso, 'SK', ombra=max(1, int(rx / 4.5)))
    if acc(s, 'barba'):
        b = sotto(viso, cy + 0.22 * ry) | sotto(ellisse(cx, cy + 0.62 * ry, 0.82 * rx, 0.55 * ry), cy + 0.3 * ry)
        t.parte(b, 'HA', ombra=max(1, int(rx / 5)))
    ey = cy + 0.1 * ry
    for lato in (-1, 1):
        ex = cx + lato * 0.37 * rx
        if G:
            w, hh = max(3.0, 0.3 * rx), max(3.0, 0.32 * ry)
            sc = ellisse(ex, ey, w / 2 + 0.4, hh / 2)
            t.parte(sc, 'WH', bordo=False)
            top = min(y for _, y in sc)
            t.segna({(x, y) for x, y in sc if y == top}, 'O')
            ir = ellisse(ex + verso * 0.14 * w, ey + 0.35, 0.3 * w + 0.25, 0.4 * hh)
            t.parte(ir & sc, 'EY', bordo=False)
            gx = int(round(ex + verso * 0.14 * w - 0.3 * w))
            t.p(gx + 1, int(round(ey - 0.25 * hh)) + 1, 'WH')
            yb = int(round(ey - hh / 2 - 1.6))
            inner = -lato * (1 if espr in ('ghigno', 'severo') else 0)
            t.segna(tratto([(ex - w / 2 - 0.5, yb + (inner if lato > 0 else 0)),
                            (ex + w / 2 + 0.5, yb + (inner if lato < 0 else 0))], 0.75), 'HAs')
        else:
            x0, y0 = int(round(ex - 0.5)), int(round(ey - 1.2))
            t.segna(rett(x0, y0, x0 + 1, y0 + 2), 'EY')
            t.p(x0 + (1 if verso < 0 else 0), y0, 'WH')
            yb = y0 - 2
            t.segna({(x0, yb), (x0 + 1, yb)}, 'HAs')
            if espr in ('ghigno', 'severo'):
                t.p(x0 + (1 if lato < 0 else 0), yb + 1, 'HAs')
    # naso
    if G:
        nx = cx + verso * 0.06 * rx
        t.segna(tratto([(nx + 1.2, ey + 0.12 * ry), (nx + 1.8, ey + 0.36 * ry), (nx, ey + 0.42 * ry)], 0.55), 'SKs')
    else:
        t.p(int(round(cx + 0.5)), int(round(ey + 2)), 'SKs')
    # bocca
    my = cy + 0.56 * ry
    mw = (0.38 if G else 0.3) * rx
    if acc(s, 'rossetto'):
        lw = mw * (0.75 if G else 1.0)
        t.segna(rett(cx - lw, my + (1 if G else 0), cx + lw - (0 if G else 1), my + (1 if G else 0)), 'A1')
    a, b = (cx - mw, my), (cx + mw, my)
    if espr == 'sorriso':
        pts = [(a[0], a[1] - 1), (cx, my + (1 if G else 0)), (b[0], b[1] - 1)]
    elif espr == 'ghigno':
        pts = [(a[0], a[1] + (0.5 if G else 0)), (b[0] - (1 if G else 0.5), b[1]), (b[0] + 0.5, b[1] - 1)]
    else:
        pts = [a, b]
    t.segna(tratto(pts, 0.55 if G else 0.45), 'O')
    if acc(s, 'baffi'):
        bw = 0.46 * rx
        th = max(1.2, 0.14 * ry)
        y0 = my - (1.4 if G else 0.6)
        t.parte(poligono([(cx - bw, y0), (cx + bw, y0), (cx + 0.32 * rx, y0 - th), (cx - 0.32 * rx, y0 - th)]),
                'HAs', bordo=False)


def _calotta(h, krx, kry, linea_y, alza=0.0):
    m = ellisse(h.cx, h.cy - (0.05 + alza) * h.ry, h.rx * krx, h.ry * kry)
    return sopra(m, h.cy + linea_y * h.ry)


def _basette(h, giu=0.12):
    s = set()
    for lato in (-1, 1):
        x0, x1 = h.cx + lato * 1.04 * h.rx, h.cx + lato * 0.8 * h.rx
        s |= rett(min(x0, x1), h.cy - 0.45 * h.ry, max(x0, x1), h.cy + giu * h.ry)
    return s


def capelli_fronte(t, s, h):
    c, cx, cy, rx, ry = s['capelli'], h.cx, h.cy, h.rx, h.ry
    om = max(1, int(rx / 5))
    if c == 'corti':
        t.parte(_calotta(h, 1.08, 0.97, -0.38) | _basette(h), 'HA', ombra=om)
    elif c == 'pettinati':
        m = _calotta(h, 1.1, 1.02, -0.46, alza=0.06) | _basette(h, 0.05)
        t.parte(m, 'HA', ombra=om)
        t.segna(tratto(arco(cx + 0.3 * rx, cy - 0.15 * ry, 0.75 * rx, 0.8 * ry, 200, 250, 4), 0.5), 'HAs')
    elif c == 'rasati':
        t.parte(_calotta(h, 1.03, 0.95, -0.52), 'HAs', bordo=True)
    elif c == 'ciuffo':
        m = _calotta(h, 1.08, 0.97, -0.38) | _basette(h)
        m |= poligono([(cx - 0.75 * rx, cy - 0.62 * ry), (cx - 1.0 * rx, cy - 1.32 * ry), (cx - 0.1 * rx, cy - 1.42 * ry),
                       (cx + 0.55 * rx, cy - 1.12 * ry), (cx + 0.6 * rx, cy - 0.7 * ry)])
        t.parte(m, 'HA', ombra=om)
    elif c == 'ricci':
        m = _calotta(h, 1.05, 0.95, -0.28)
        for a in range(195, 350, 22):
            r = math.radians(a)
            m |= ellisse(cx + 0.98 * rx * math.cos(r), cy - 0.12 * ry + 0.98 * ry * math.sin(r), 0.34 * rx, 0.32 * ry)
        t.parte(sopra(m, cy - 0.12 * ry), 'HA', ombra=om)
    elif c == 'lunghi':
        m = _calotta(h, 1.1, 1.0, -0.42)
        for lato in (-1, 1):
            m |= poligono([(cx + lato * 1.1 * rx, cy - 0.3 * ry), (cx + lato * 0.78 * rx, cy - 0.42 * ry),
                           (cx + lato * 0.84 * rx, cy + 0.9 * ry), (cx + lato * 1.18 * rx, cy + 1.0 * ry)])
        t.parte(m, 'HA', ombra=om)
    elif c == 'caschetto':
        m = _calotta(h, 1.12, 1.0, -0.3)
        for lato in (-1, 1):
            m |= poligono([(cx + lato * 1.13 * rx, cy - 0.3 * ry), (cx + lato * 0.8 * rx, cy - 0.3 * ry),
                           (cx + lato * 0.8 * rx, cy + 0.8 * ry), (cx + lato * 1.13 * rx, cy + 0.8 * ry)])
        t.parte(m, 'HA', ombra=om)
    elif c == 'coda':
        t.parte(_calotta(h, 1.07, 0.99, -0.42, alza=0.03) | _basette(h, 0.0), 'HA', ombra=om)
        t.parte(ellisse(cx + 0.97 * rx, cy - 0.32 * ry, max(1.0, 0.17 * rx), max(1.2, 0.17 * ry)), 'A1', bordo=h.grande)
    elif c == 'cotonati':
        m = _calotta(h, 1.22, 1.08, -0.3, alza=0.05)
        for k in range(-2, 3):
            m |= ellisse(cx + k * 0.38 * rx, cy - 0.42 * ry, 0.26 * rx, 0.2 * ry)
        t.parte(m, 'HA', ombra=om)
    elif c in ('riporto', 'calvo'):
        m = set()
        for lato in (-1, 1):
            m |= rett(min(cx + lato * 1.05 * rx, cx + lato * 0.8 * rx), cy - 0.42 * ry,
                      max(cx + lato * 1.05 * rx, cx + lato * 0.8 * rx), cy + 0.05 * ry)
        t.parte(m, 'HA', ombra=0, bordo=h.grande)
        if c == 'riporto':
            t.segna(tratto(arco(cx + 0.1 * rx, cy - 0.05 * ry, 0.95 * rx, 0.85 * ry, 195, 290, 5),
                           0.7 if h.grande else 0.45), 'HAs')
    else:
        raise KeyError(c)


def copricapo_fronte(t, s, h):
    cx, cy, rx, ry, G = h.cx, h.cy, h.rx, h.ry, h.grande
    c = cappello(s)
    if c == 'casco':
        t.parte(sopra(ellisse(cx, cy - 0.3 * ry, 1.17 * rx, 0.92 * ry), cy - 0.3 * ry), 'A2')
        t.parte(rett(cx - 1.3 * rx, cy - 0.38 * ry, cx + 1.3 * rx, cy - 0.38 * ry + max(1, 0.1 * ry)), 'A2')
        t.segna(linea(cx, cy - 1.15 * ry, cx, cy - 0.45 * ry), 'O')
    elif c == 'capitano':
        t.parte(ellisse(cx, cy - 0.78 * ry, 1.18 * rx, 0.42 * ry), 'A2')
        t.parte(rett(cx - 1.0 * rx, cy - 0.62 * ry, cx + 1.0 * rx, cy - 0.42 * ry), 'A2')
        t.parte(poligono([(cx - 1.05 * rx, cy - 0.44 * ry), (cx + 1.05 * rx, cy - 0.44 * ry),
                          (cx + 0.8 * rx, cy - 0.28 * ry), (cx - 0.8 * rx, cy - 0.28 * ry)]), 'EY', bordo=G)
        t.parte(ellisse(cx, cy - 0.62 * ry, max(1.0, 0.16 * rx), max(1.0, 0.13 * ry)), 'A3', bordo=False)
    elif c == 'paglia':
        t.parte(ellisse(cx, cy - 0.5 * ry, 1.75 * rx, 0.3 * ry), 'A3')
        t.parte(sopra(ellisse(cx, cy - 0.62 * ry, 0.92 * rx, 0.62 * ry), cy - 0.55 * ry), 'A3')
        t.parte(rett(cx - 0.9 * rx, cy - 0.72 * ry, cx + 0.9 * rx, cy - 0.6 * ry), 'A1', bordo=False)
    elif c == 'berretto_lana':
        t.parte(sopra(ellisse(cx, cy - 0.38 * ry, 1.1 * rx, 0.82 * ry), cy - 0.32 * ry), 'A2')
        t.parte(rett(cx - 1.1 * rx, cy - 0.55 * ry, cx + 1.1 * rx, cy - 0.3 * ry), 'A2')
    elif c in ('berretto', 'berretto_rovescio'):
        t.parte(sopra(ellisse(cx, cy - 0.35 * ry, 1.08 * rx, 0.85 * ry), cy - 0.38 * ry), 'A2')
        if c == 'berretto':
            t.parte(ellisse(cx - 0.45 * rx, cy - 0.38 * ry, 1.0 * rx, max(1.2, 0.17 * ry)), 'A2')
        else:
            t.parte(rett(cx + 0.7 * rx, cy - 0.62 * ry, cx + 1.25 * rx, cy - 0.4 * ry), 'A2')
    elif c == 'fedora':
        t.parte(ellisse(cx, cy - 0.5 * ry, 1.55 * rx, 0.26 * ry), 'A2')
        t.parte(poligono([(cx - 0.95 * rx, cy - 0.52 * ry), (cx + 0.95 * rx, cy - 0.52 * ry),
                          (cx + 0.8 * rx, cy - 1.18 * ry), (cx - 0.8 * rx, cy - 1.18 * ry)]), 'A2')
        t.parte(rett(cx - 0.94 * rx, cy - 0.7 * ry, cx + 0.94 * rx, cy - 0.56 * ry), 'A1', bordo=False)
    if acc(s, 'cuffie'):
        t.segna(tratto(arco(cx, cy - 0.05 * ry, 1.08 * rx, 1.08 * ry, 185, 355, 8), 0.9 if G else 0.55), 'A2')
        for lato in (-1, 1):
            t.parte(ellisse(cx + lato * 1.02 * rx, cy + 0.08 * ry, 0.3 * rx, 0.36 * ry), 'A2')
    if acc(s, 'auricolare'):
        t.parte(ellisse(cx + 1.0 * rx, cy + 0.15 * ry, max(0.9, 0.13 * rx), max(0.9, 0.13 * ry)), 'WH', bordo=False)


def occhiali_fronte(t, s, h):
    cx, cy, rx, ry, G = h.cx, h.cy, h.rx, h.ry, h.grande
    ey = cy + 0.1 * ry
    if acc(s, 'occhiali_sole'):
        for lato in (-1, 1):
            ex = cx + lato * 0.37 * rx
            m = ellisse(ex, ey, 0.27 * rx + (0.6 if G else 0.8), 0.22 * ry + 0.6)
            t.parte(m, 'EY', bordo=False)
            t.p(int(round(ex - 0.12 * rx)), int(round(ey - 0.08 * ry)), 'WH')
        t.segna(linea(cx - 0.12 * rx, ey - 0.05 * ry, cx + 0.12 * rx, ey - 0.05 * ry), 'EY')
    elif acc(s, 'occhiali'):
        for lato in (-1, 1):
            ex = cx + lato * 0.37 * rx
            w, hh = (0.3 * rx + 1.4, 0.3 * ry + 1.2) if G else (2.0, 1.6)
            x0, x1, y0, y1 = (int(round(v)) for v in (ex - w / 2 - 0.3, ex + w / 2 - 0.3, ey - hh / 2, ey + hh / 2))
            if not G:
                x0, x1 = int(round(ex - 0.5)) - 1, int(round(ex - 0.5)) + 2
                y0, y1 = int(round(ey - 1.2)) - 1, int(round(ey - 1.2)) + 3
            cornice = (rett(x0, y0, x1, y0) | rett(x0, y1, x1, y1) | rett(x0, y0, x0, y1) | rett(x1, y0, x1, y1))
            t.segna(cornice, 'O' if G else 'A2')
        t.segna(linea(cx - 0.18 * rx, ey - 0.1 * ry, cx + 0.18 * rx, ey - 0.1 * ry), 'O' if G else 'A2')


def testa_fronte(t, s, h, espr='serio', verso=-1):
    faccia(t, s, h, espr, verso)
    capelli_fronte(t, s, h)
    copricapo_fronte(t, s, h)
    occhiali_fronte(t, s, h)


def testa_retro(t, s, h):
    """Testa vista da dietro (dorsi): nuca, capelli, cappello."""
    c, cx, cy, rx, ry = s['capelli'], h.cx, h.cy, h.rx, h.ry
    om = max(1, int(rx / 5))
    orecchie(t, h)
    t.parte(ellisse(cx, cy, rx, ry), 'SK', ombra=om)
    copre = sopra(ellisse(cx, cy - 0.02 * ry, 1.04 * rx, 1.02 * ry), cy + 0.55 * ry)
    if c in ('corti', 'pettinati', 'ciuffo'):
        m = copre
        if c == 'ciuffo':
            m |= ellisse(cx - 0.2 * rx, cy - 0.98 * ry, 0.45 * rx, 0.22 * ry)
        t.parte(m, 'HA', ombra=om)
        t.segna(tratto(arco(cx, cy + 0.2 * ry, 0.5 * rx, 0.5 * ry, 200, 330, 5), 0.6), 'HAs')
    elif c == 'rasati':
        t.parte(sopra(ellisse(cx, cy, 1.02 * rx, 1.0 * ry), cy + 0.5 * ry), 'HAs')
    elif c == 'ricci':
        m = copre
        for a in range(150, 400, 22):
            r = math.radians(a)
            m |= ellisse(cx + 0.98 * rx * math.cos(r), cy + 0.95 * ry * math.sin(r), 0.3 * rx, 0.28 * ry)
        t.parte(sopra(m, cy + 0.62 * ry), 'HA', ombra=om)
    elif c == 'lunghi':
        t.parte(poligono([(cx - 1.06 * rx, cy - 0.1 * ry), (cx + 1.06 * rx, cy - 0.1 * ry),
                          (cx + 1.2 * rx, cy + 2.1 * ry), (cx - 1.2 * rx, cy + 2.1 * ry)])
                | ellisse(cx, cy - 0.02 * ry, 1.06 * rx, 1.04 * ry), 'HA', ombra=om)
    elif c == 'caschetto':
        t.parte(sopra(ellisse(cx, cy + 0.05 * ry, 1.12 * rx, 1.08 * ry), cy + 0.85 * ry), 'HA', ombra=om)
    elif c == 'coda':
        t.parte(copre, 'HA', ombra=om)
        t.parte(capsula(cx + 0.05 * rx, cy + 0.45 * ry, cx + 0.15 * rx, cy + 1.95 * ry, 0.3 * rx, 0.16 * rx), 'HA', ombra=1)
        t.parte(ellisse(cx + 0.05 * rx, cy + 0.42 * ry, 0.24 * rx, 0.14 * ry), 'A1')
    elif c == 'cotonati':
        t.parte(sopra(ellisse(cx, cy - 0.12 * ry, 1.36 * rx, 1.14 * ry), cy + 0.65 * ry), 'HA', ombra=om)
    elif c in ('calvo', 'riporto'):
        anello = sopra(sotto(ellisse(cx, cy, 1.04 * rx, 1.02 * ry), cy + 0.05 * ry), cy + 0.55 * ry)
        t.parte(anello, 'HA', ombra=om)
        if c == 'riporto':
            t.segna(tratto([(cx - 0.8 * rx, cy - 0.3 * ry), (cx, cy - 0.7 * ry), (cx + 0.7 * rx, cy - 0.45 * ry)], 0.7), 'HAs')
    else:
        raise KeyError(c)
    k = cappello(s)
    if k == 'casco':
        t.parte(sopra(ellisse(cx, cy - 0.1 * ry, 1.18 * rx, 1.0 * ry), cy - 0.05 * ry), 'A2', ombra=0)
        t.parte(rett(cx - 1.28 * rx, cy - 0.12 * ry, cx + 1.28 * rx, cy - 0.12 * ry + 1.5), 'A2')
    elif k == 'capitano':
        t.parte(ellisse(cx, cy - 0.68 * ry, 1.2 * rx, 0.46 * ry), 'A2')
        t.parte(rett(cx - 1.02 * rx, cy - 0.55 * ry, cx + 1.02 * rx, cy - 0.3 * ry), 'A2')
    elif k == 'paglia':
        t.parte(ellisse(cx, cy - 0.3 * ry, 1.8 * rx, 0.36 * ry), 'A3')
        t.parte(sopra(ellisse(cx, cy - 0.5 * ry, 0.95 * rx, 0.7 * ry), cy - 0.35 * ry), 'A3')
        t.parte(rett(cx - 0.93 * rx, cy - 0.58 * ry, cx + 0.93 * rx, cy - 0.44 * ry), 'A1', bordo=False)
    elif k == 'berretto_lana':
        t.parte(sopra(ellisse(cx, cy - 0.25 * ry, 1.1 * rx, 0.95 * ry), cy - 0.05 * ry), 'A2')
        t.parte(rett(cx - 1.1 * rx, cy - 0.3 * ry, cx + 1.1 * rx, cy - 0.05 * ry), 'A2')
    elif k in ('berretto', 'berretto_rovescio'):
        t.parte(sopra(ellisse(cx, cy - 0.2 * ry, 1.1 * rx, 0.95 * ry), cy - 0.15 * ry), 'A2')
        if k == 'berretto':
            t.parte(rett(cx - 0.25 * rx, cy - 0.22 * ry, cx + 0.25 * rx, cy - 0.12 * ry), 'WH', bordo=False)
        else:
            t.parte(ellisse(cx, cy - 0.12 * ry, 0.85 * rx, 0.22 * ry), 'A2')
    elif k == 'fedora':
        t.parte(ellisse(cx, cy - 0.32 * ry, 1.6 * rx, 0.3 * ry), 'A2')
        t.parte(poligono([(cx - 0.98 * rx, cy - 0.35 * ry), (cx + 0.98 * rx, cy - 0.35 * ry),
                          (cx + 0.82 * rx, cy - 1.08 * ry), (cx - 0.82 * rx, cy - 1.08 * ry)]), 'A2')
        t.parte(rett(cx - 0.96 * rx, cy - 0.55 * ry, cx + 0.96 * rx, cy - 0.4 * ry), 'A1', bordo=False)
    if acc(s, 'cuffie'):
        t.segna(tratto(arco(cx, cy, 1.06 * rx, 1.06 * ry, 185, 355, 8), 1.0), 'A2')
        for lato in (-1, 1):
            t.parte(ellisse(cx + lato * 1.0 * rx, cy + 0.12 * ry, 0.28 * rx, 0.34 * ry), 'A2')


# ------------------------------------------------------------------------------------------ corpo, fronte

def _maniche(s):
    if s['sopra'] == 'canotta':
        return 'nude'
    return 'corte' if s.get('maniche') == 'corta' else 'lunghe'


def braccio(t, s, lato, spalla, gomito, mano, maniche, r=3.0, oggetto=None):
    """Un braccio di due segmenti con la mano; `oggetto` (una funzione) si disegna prima della mano."""
    ruolo = 'A1' if (s.get('bicolore') and lato > 0) else 'TO'
    (sx, sy), (gx, gy), (mx, my) = spalla, gomito, mano
    om = 1 if r < 4 else 2
    if maniche == 'nude':
        t.parte(capsula(sx, sy, gx, gy, r, r * 0.9) | capsula(gx, gy, mx, my, r * 0.9, r * 0.78), 'SK', ombra=om)
    elif maniche == 'corte':
        mid = (sx + (gx - sx) * 0.55, sy + (gy - sy) * 0.55)
        t.parte(capsula(mid[0], mid[1], gx, gy, r * 0.82, r * 0.78) | capsula(gx, gy, mx, my, r * 0.78, r * 0.7), 'SK', ombra=om)
        t.parte(capsula(sx, sy, mid[0], mid[1], r * 1.05, r), ruolo, ombra=om)
    else:
        t.parte(capsula(sx, sy, gx, gy, r, r * 0.92) | capsula(gx, gy, mx, my, r * 0.92, r * 0.85), ruolo, ombra=om)
    if oggetto:
        oggetto()
    t.parte(ellisse(mx, my + 0.4, r * 0.9, r * 0.9), 'SK', ombra=1 if r < 4 else 2)


def palla(t, x, y, r):
    m = ellisse(x, y, r, r)
    t.parte(m, 'WH', bordo=False)
    t.segna(sopra(m, y - 0.5), 'A1')
    t.segna({(xx, yy) for xx, yy in m if any((xx + a, yy + b) not in m for a, b in N4)}, 'O')
    t.segna({(int(round(x - 1)), int(round(y - 0.5))), (int(round(x)), int(round(y - 0.5)))}, 'O')


def figura_fronte(s, posa):
    """Immagine frontale 80×80. posa = dict(L=..., R=..., espr=...): L è il braccio a sinistra dell'immagine."""
    t = Tela(80, 80)
    cx = 40
    pan = s.get('pancia', 0)
    gonna = s['sotto'] == 'gonna'
    h = Testa(cx, 14.5, 9.0, 10.0)
    sw, ww, hw = 13.5 + 1.5 * pan, 9.5 + 4.0 * pan, 10.0 + 1.0 * pan
    lungo = s['sopra'] in ('cappotto', 'camice')
    yb = 66 if s['sopra'] == 'cappotto' else (61 if s['sopra'] == 'camice' else 50)
    capelli_dietro(t, s, h, 'fronte')
    # gambe e scarpe
    if gonna:
        for lato in (-1, 1):
            t.parte(capsula(cx + lato * 4.2, 60, cx + lato * 4.6, 73.5, 2.6, 2.2), 'SK', ombra=1)
    else:
        for lato in (-1, 1):
            a, b = (cx + lato * 0.4, cx + lato * hw) if lato > 0 else (cx + lato * hw, cx + lato * 0.4)
            t.parte(poligono([(a, 49), (b, 49), (b - lato * 1.0 if lato > 0 else b + 1.2, 75), (a + (0.6 if lato > 0 else -0.6) * 1, 75)]),
                    'BO', ombra=2)
    for lato in (-1, 1):
        t.parte(ellisse(cx + lato * 5.2 + (-0.6 if lato < 0 else 0.6), 75.8, 4.6, 2.5), 'SH', ombra=0)
    if gonna:
        t.parte(poligono([(cx - ww - 0.5, 46), (cx + ww + 0.5, 46), (cx + ww + 4.0, 63), (cx - ww - 4.0, 63)]), 'BO', ombra=3)
    # collo e busto
    t.parte(rett(cx - 2.4, 21, cx + 2.4, 28), 'SK', ombra=1)
    if s['sopra'] == 'canotta':
        t.parte(poligono([(cx - sw + 2.5, 26), (cx + sw - 2.5, 26), (cx + sw - 1, 31), (cx - sw + 1, 31)]), 'SK', ombra=2)
    top = 30 if s['sopra'] == 'canotta' else 26
    pts = [(cx - sw + 2.5, top), (cx + sw - 2.5, top), (cx + sw, 28.5), (cx + sw - 0.5, 33), (cx + ww, 46),
           (cx + hw + (2.5 if lungo else 0), yb), (cx - hw - (2.5 if lungo else 0), yb), (cx - ww, 46),
           (cx - sw + 0.5, 33), (cx - sw, 28.5)]
    busto = poligono(pts)
    if pan:
        busto |= ellisse(cx, 42, ww + 1.2, 8.5)
    ruolo_busto = 'TO'
    t.parte(busto, ruolo_busto, ombra=3)
    if s.get('bicolore'):
        t.parte({q for q in busto if q[0] >= cx}, 'A1', bordo=False)
        t.segna({q for q in busto if q[0] >= cx and any((q[0] + a, q[1] + b) not in busto for a, b in N4)}, 'O')
    if s['sopra'] == 'canotta':
        for lato in (-1, 1):
            t.parte(rett(cx + lato * 5 - 1, 25.5, cx + lato * 5 + 1, 30.5), 'TO', ombra=0)
    dettagli_busto(t, s, cx, sw, ww, hw, yb, busto)
    # braccia
    maniche = _maniche(s)
    spalle = {-1: (cx - sw + 1.5, 29.5), 1: (cx + sw - 1.5, 29.5)}
    for lato in (-1, 1):
        nome = posa.get('L' if lato < 0 else 'R', 'giu')
        braccio_posa(t, s, lato, nome, spalle[lato], cx, sw, ww, h, maniche, posa.get('fase', 0))
    testa_fronte(t, s, h, posa.get('espr', 'serio'), -1)
    return t.indici()


def dettagli_busto(t, s, cx, sw, ww, hw, yb, busto, k=1.0, top=26):
    """Colletti, cravatte, bottoni e accessori sul petto. k scala le misure (1 = figura intera)."""
    so = s['sopra']
    y0 = top

    def V(larg, giu):
        return poligono([(cx - larg * k, y0), (cx + larg * k, y0), (cx, y0 + giu * k)])
    if so in ('giacca', 'tailleur', 'cappotto', 'camice'):
        interno = 'A2' if s.get('camice_interno') == 'A2' else 'WH'
        if so == 'camice':
            t.parte(poligono([(cx - 3.2 * k, y0), (cx + 3.2 * k, y0), (cx + 2.6 * k, yb), (cx - 2.6 * k, yb)]) & busto,
                    'A2', bordo=False)
            t.segna(linea(cx - 3.2 * k, y0, cx - 2.6 * k, yb) | linea(cx + 3.2 * k, y0, cx + 2.6 * k, yb), 'O')
            t.parte(V(2.2, 6), 'WH', bordo=False)
        else:
            t.parte(V(3.6, 11), interno, bordo=False)
            t.segna(linea(cx - 3.6 * k, y0, cx - 0.4 * k, y0 + 11 * k) | linea(cx + 3.6 * k, y0, cx + 0.4 * k, y0 + 11 * k), 'TOs')
            if so in ('giacca', 'cappotto') and yb > y0 + 14 * k:
                t.segna(linea(cx, y0 + 12 * k, cx, yb), 'TOs')
    elif so in ('camicia', 'polo'):
        if not acc(s, 'gilet'):
            t.segna(linea(cx, y0 + 2 * k, cx, (y0 + 8 * k) if so == 'polo' else yb - 1), 'TOs')
        for lato in (-1, 1):
            t.parte(poligono([(cx, y0 + 0.5), (cx + lato * 4.2 * k, y0 - 0.5), (cx + lato * 3.2 * k, y0 + 3.5 * k)]), 'TO', ombra=0)
    elif so == 'maglia' or so == 'righe':
        t.segna(tratto(arco(cx, y0 - 0.5, 3.4 * k, 2.6 * k, 20, 160, 6), 0.5), 'TOs')
    elif so == 'felpa':
        t.parte(poligono([(cx - 5 * k, y0 - 1), (cx + 5 * k, y0 - 1), (cx + 3 * k, y0 + 3 * k), (cx - 3 * k, y0 + 3 * k)]), 'TO', ombra=0)
        t.segna(linea(cx - 1.5 * k, y0 + 2 * k, cx - 1.5 * k, y0 + 8 * k) | linea(cx + 1.5 * k, y0 + 2 * k, cx + 1.5 * k, y0 + 7 * k), 'WH')
        t.segna(rett(cx - 6 * k, y0 + 15 * k, cx + 6 * k, y0 + 15 * k) | rett(cx - 6 * k, y0 + 15 * k, cx - 6 * k, y0 + 20 * k)
                | rett(cx + 6 * k, y0 + 15 * k, cx + 6 * k, y0 + 20 * k), 'TOs')
    elif so == 'tuta_lavoro':
        t.segna(linea(cx, y0 + 1, cx, yb - 1), 'TOs')
        for lato in (-1, 1):
            t.parte(poligono([(cx, y0 + 1), (cx + lato * 4.5 * k, y0 - 0.5), (cx + lato * 3.5 * k, y0 + 3.5 * k)]), 'TO', ombra=0)
        t.segna(rett(cx + 3 * k, y0 + 6 * k, cx + 8 * k, y0 + 6 * k) | rett(cx + 3 * k, y0 + 6 * k, cx + 3 * k, y0 + 10 * k)
                | rett(cx + 8 * k, y0 + 6 * k, cx + 8 * k, y0 + 10 * k), 'TOs')
    elif so == 'abito':
        t.parte(ellisse(cx, y0, 4.6 * k, 3.4 * k), 'SK', ombra=0)
    if so == 'righe':
        for y in range(int(y0 + 4 * k), int(yb), max(3, int(4 * k))):
            t.segna({q for q in busto if y <= q[1] < y + max(1, int(1.5 * k)) and t.g(*q) in ('TO', 'TOs')}, 'WH')
    if acc(s, 'gilet'):
        for lato in (-1, 1):
            t.parte(poligono([(cx + lato * (sw - 3) * k / k, y0 + 2 * k), (cx + lato * 0.6, y0 + 4 * k),
                              (cx + lato * 0.6, yb - 1), (cx + lato * ww, yb - 1)]) & busto, 'A2', ombra=0)
    if acc(s, 'alta_visibilita'):
        for yy in (y0 + 10 * k, y0 + 16 * k):
            t.segna({q for q in busto if yy <= q[1] < yy + max(1, int(1.6 * k)) and t.g(*q) != 'O'}, 'A3')
    if acc(s, 'cravatta'):
        t.parte(poligono([(cx - 1.1 * k, y0 + 1), (cx + 1.1 * k, y0 + 1), (cx + 1.7 * k, y0 + 11 * k), (cx, y0 + 13 * k),
                          (cx - 1.7 * k, y0 + 11 * k)]), 'A1', bordo=k > 1.5)
        t.segna(rett(cx - 1.2 * k, y0, cx + 1.2 * k, y0 + 1.2 * k), 'A1')
    if acc(s, 'bottoni_oro') or so in ('giacca', 'tailleur', 'cappotto'):
        ruolo = 'A3' if acc(s, 'bottoni_oro') else 'O'
        cols = (-3 * k, 3 * k) if s.get('doppiopetto') else (0.0,)
        for dxb in cols:
            for yy in (y0 + 14 * k, y0 + 19 * k):
                if yy < yb - 1:
                    t.parte(ellisse(cx + dxb, yy, max(0.8, 0.8 * k), max(0.8, 0.8 * k)), ruolo, bordo=False)
    if acc(s, 'pochette'):
        t.parte(rett(cx + 5 * k, y0 + 7 * k, cx + 7.5 * k, y0 + 8.4 * k), 'A1', bordo=False)
    if acc(s, 'collana'):
        t.segna(tratto(arco(cx, y0 + 0.5, 4.2 * k, 4.6 * k, 20, 160, 8), 0.5), 'A3')
    if acc(s, 'perle'):
        for x, y in arco(cx, y0 + 0.5, 4.2 * k, 4.2 * k, 20, 160, 6):
            t.p(int(round(x)), int(round(y)), 'WH')
    if acc(s, 'stetoscopio'):
        t.segna(tratto([(cx - 4.5 * k, y0), (cx - 4.6 * k, y0 + 9 * k)], 0.5) | tratto([(cx + 4.5 * k, y0), (cx + 4.8 * k, y0 + 7 * k)], 0.5), 'A3')
        t.parte(ellisse(cx + 4.8 * k, y0 + 8.5 * k, 1.4 * k, 1.4 * k), 'A3')
    if acc(s, 'fischietto'):
        t.segna(tratto([(cx - 3.5 * k, y0), (cx + 0.5, y0 + 8 * k), (cx + 3.5 * k, y0)], 0.45), 'A3')
        t.parte(rett(cx, y0 + 8 * k, cx + 2 * k, y0 + 9.5 * k), 'A3', bordo=False)
    if acc(s, 'sciarpa'):
        t.parte(rett(cx - 5 * k, y0 - 1.5 * k, cx + 5 * k, y0 + 1.5 * k), 'A1')
        t.parte(rett(cx + 1.5 * k, y0 + 1.5 * k, cx + 4 * k, y0 + 15 * k), 'A1')
        t.parte(rett(cx - 4 * k, y0 + 1.5 * k, cx - 1.5 * k, y0 + 11 * k), 'A1')
    if acc(s, 'maglione'):
        t.parte(poligono([(cx - sw + 1.5, y0 - 0.5), (cx + sw - 1.5, y0 - 0.5), (cx + sw - 2.5, y0 + 3.5 * k), (cx - sw + 2.5, y0 + 3.5 * k)]), 'A1')
        t.parte(capsula(cx - 6 * k, y0 + 3 * k, cx, y0 + 7 * k, 1.4 * k) | capsula(cx + 6 * k, y0 + 3 * k, cx, y0 + 7 * k, 1.4 * k), 'A1')
    if acc(s, 'borsello'):
        t.segna(tratto([(cx - sw + 2.5, y0 + 1), (cx + ww, y0 + 20 * k)], 0.8 * k), 'A2')
        t.parte(rett(cx + ww - 3 * k, y0 + 19 * k, cx + ww + 3 * k, y0 + 24 * k), 'A2')
    if acc(s, 'cintura') and yb > y0 + 20 * k:
        yy = y0 + 22.5 * k
        t.segna({q for q in busto if yy <= q[1] < yy + max(1, int(1.5 * k)) and t.g(*q) != 'O'}, 'A3')
        t.parte(rett(cx - 1.2 * k, yy - 0.2, cx + 1.2 * k, yy + 1.3 * k), 'WH', bordo=False)
    if acc(s, 'auricolare'):
        t.segna(tratto([(cx + 6.5 * k, y0 - 6 * k), (cx + 4.5 * k, y0 + 1.5 * k)], 0.4), 'EY')


def braccio_posa(t, s, lato, nome, spalla, cx, sw, ww, h, maniche, fase):
    sx, sy = spalla
    giu = ((cx + lato * (sw + 1.5), 40), (cx + lato * (sw + 1.6), 49.5))
    ogg = None
    if nome == 'giu':
        g, m = giu
    elif nome == 'fianchi':
        g, m = (cx + lato * (sw + 6.5), 39), (cx + lato * (ww + 0.8), 46.5)
    elif nome == 'indica':
        g, m = (cx + lato * (sw + 6.5), 33.5), (cx + lato * (sw + 13.5), 32.5)

        def ogg():
            t.parte(capsula(m[0], m[1] - 0.5, m[0] + lato * 4.2, m[1] - 1.0, 0.9), 'SK', bordo=True)
    elif nome == 'pugno':
        g, m = (cx + lato * (sw + 5.5), 24.5), (cx + lato * (sw + 3.0), 15.0)
    elif nome == 'telefono':
        g, m = (cx + lato * (sw + 3.5), 38.5), (cx + lato * (h.rx + 0.8), h.cy + 3.0)

        def ogg():
            t.parte(rett(m[0] - 1.2, m[1] - 5.0, m[0] + 1.4, m[1] + 1.5), 'A2')
    elif nome == 'tablet':
        g, m = (cx + lato * (sw + 1.0), 40), (cx + lato * 7.5, 43)

        def ogg():
            if lato < 0:
                t.parte(rett(cx - 8, 34, cx + 8, 45), 'A3')
                t.parte(rett(cx - 6, 36, cx + 6, 43), 'A2', bordo=False)
    elif nome == 'cartellina':
        g, m = (cx + lato * (sw + 2.5), 40), (cx + lato * 3.5, 41.5)

        def ogg():
            x0, x1 = (cx + lato * 2, cx + lato * 12)
            t.parte(rett(min(x0, x1), 32.5, max(x0, x1), 46.5), 'A2', ombra=0)
            t.segna(rett(min(x0, x1) + 1, 34.5, max(x0, x1) - 1, 34.5), 'WH')
    elif nome == 'valigetta':
        g, m = giu

        def ogg():
            t.parte(rett(m[0] - 5.5, m[1] + 2.0, m[0] + 5.5, m[1] + 9.0), 'A2', ombra=2)
            t.segna(rett(m[0] - 1.5, m[1] + 0.5, m[0] + 1.5, m[1] + 0.5), 'O')
    elif nome == 'buste':
        g, m = (cx + lato * (sw + 2.5), 41), (cx + lato * 5.0, 40)

        def ogg():
            for k in range(3):
                x0 = cx + lato * (3 + 2 * k)
                y0 = 33.5 + k
                b = rett(min(x0, x0 + lato * 8), y0, max(x0, x0 + lato * 8), y0 + 5)
                t.parte(b, 'WH')
                t.p(int(round(x0 + lato * 4)), int(y0 + 2), 'A1')
    elif nome == 'bastone':
        g, m = (cx + lato * (sw + 3.0), 40), (cx + lato * (sw + 4.0), 50.0)

        def ogg():
            t.parte(capsula(m[0] + lato * 0.5, m[1], m[0] + lato * 1.5, 77.5, 1.0), 'A3', bordo=True)
            t.parte(ellisse(m[0], m[1] - 1.0, 2.0, 1.6), 'A3')
    elif nome == 'lancio':
        tab = [((cx + lato * (sw + 1.5), 40), (cx + lato * (sw + 1.6), 49.5), True),
               ((cx + lato * (sw + 5.5), 41), (cx + lato * (sw + 9.0), 47.0), True),
               ((cx + lato * (sw + 6.0), 27), (cx + lato * (sw + 6.0), 15.0), True),
               ((cx + lato * (sw + 2.0), 21), (cx + lato * 3.0, 9.5), True),
               ((cx - lato * 2.0, 27), (cx - lato * (sw + 6.0), 26.0), False),
               ((cx - lato * 1.0, 34), (cx - lato * (sw + 2.0), 42.0), False),
               ((cx + lato * 2.0, 38), (cx - lato * (sw - 2.0), 47.5), False),
               ((cx - lato * 3.0, 31), (cx - lato * (sw + 9.0), 36.0), False)]
        g, m, con_palla = tab[fase]
        if con_palla:
            def ogg():
                pass
        braccio(t, s, lato, spalla, g, m, maniche, oggetto=ogg)
        if con_palla:
            palla(t, m[0] + lato * 1.0, m[1] - 2.5, 2.6)
        return
    else:
        raise KeyError(nome)
    braccio(t, s, lato, spalla, g, m, maniche, oggetto=ogg)


# ------------------------------------------------------------------------------------------- dorso

RETRO_FASI = [
    # (gomito, mano, palla) del braccio che lancia (a destra dell'immagine)
    ((62, 63), (63, 75), True),
    ((65, 60), (58, 70), True),
    ((69, 45), (65, 30), True),
    ((69, 36), (74, 22), True),
    ((71, 41), (79, 33), False),
    ((69, 52), (76, 59), False),
    ((67, 56), (72, 66), False),
    ((67, 54), (74, 61), False),
]


def figura_retro(s, fase):
    """Dorso 80×80: mezza figura di spalle, braccio destro che lancia la Poké Ball (fasi 0–7, tabella RETRO_FASI)."""
    t = Tela(80, 80)
    pan = s.get('pancia', 0)
    h = Testa(31, 25, 12.0, 13.0)
    sw = 27 + 2 * pan
    # busto
    so = s['sopra']
    maniche = _maniche(s)
    if so == 'canotta':
        t.parte(poligono([(h.cx - sw + 6, 44), (h.cx + sw - 6, 44), (h.cx + sw - 2, 52), (h.cx - sw + 2, 52)]), 'SK', ombra=3)
    top = 47 if so == 'canotta' else 43
    busto = poligono([(h.cx - sw + 7, top), (h.cx + sw - 7, top), (h.cx + sw - 1, top + 6), (h.cx + sw + 1, 81),
                      (h.cx - sw - 1, 81), (h.cx - sw + 1, top + 6)])
    t.parte(rett(h.cx - 5, 32, h.cx + 5, 46), 'SK', ombra=2)
    t.parte(busto, 'TO', ombra=4)
    if s.get('bicolore'):
        t.parte({q for q in busto if q[0] >= h.cx}, 'A1', bordo=False)
    if so == 'canotta':
        for lato in (-1, 1):
            t.parte(rett(h.cx + lato * 8 - 2, 42, h.cx + lato * 8 + 2, 48), 'TO', ombra=0)
    if so in ('giacca', 'tailleur', 'cappotto', 'camice', 'camicia', 'polo', 'tuta_lavoro'):
        t.parte(poligono([(h.cx - 7, 41), (h.cx + 7, 41), (h.cx + 8, 45), (h.cx - 8, 45)]),
                'WH' if so in ('giacca', 'tailleur', 'cappotto') else 'TO', ombra=0)
    if so in ('giacca', 'tailleur', 'cappotto', 'camice'):
        t.segna(linea(h.cx + 1, 58, h.cx + 1, 79), 'TOs')
    if so == 'felpa':
        t.parte(poligono([(h.cx - 11, 40), (h.cx + 11, 40), (h.cx + 8, 54), (h.cx - 8, 54)]), 'TO', ombra=2)
    if so == 'righe':
        for y in range(50, 80, 5):
            t.segna({q for q in busto if y <= q[1] < y + 2 and t.g(*q) in ('TO', 'TOs')}, 'WH')
    if acc(s, 'alta_visibilita'):
        for yy in (58, 68):
            t.segna({q for q in busto if yy <= q[1] < yy + 3 and t.g(*q) != 'O'}, 'A3')
    if acc(s, 'maglione'):
        t.parte(poligono([(h.cx - sw + 7, 42), (h.cx + sw - 7, 42), (h.cx + sw - 3, 49), (h.cx - sw + 3, 49)]), 'A1')
    if acc(s, 'sciarpa'):
        t.parte(rett(h.cx - 9, 40, h.cx + 9, 45), 'A1')
    if acc(s, 'borsello'):
        t.segna(tratto([(h.cx + sw - 6, 46), (h.cx - sw + 4, 78)], 1.2), 'A2')
    # braccio sinistro, lungo il fianco
    ruoloL = 'TO'
    rL = 5.2
    if maniche == 'lunghe':
        t.parte(capsula(h.cx - sw + 3, 50, h.cx - sw - 1, 80, rL, rL * 0.9), ruoloL, ombra=2)
    else:
        t.parte(capsula(h.cx - sw + 3, 50, h.cx - sw - 1, 80, rL * 0.9, rL * 0.82), 'SK', ombra=2)
        if maniche == 'corte':
            t.parte(capsula(h.cx - sw + 3, 50, h.cx - sw + 1.5, 60, rL * 1.05), ruoloL, ombra=2)
    if s['capelli'] == 'lunghi':
        pass
    testa_retro(t, s, h)
    # braccio che lancia
    g, m, con_palla = RETRO_FASI[fase]
    spalla = (h.cx + sw - 4, 50)
    braccio(t, s, 1, spalla, g, m, maniche, r=5.0)
    if con_palla:
        palla(t, m[0] - 0.5, m[1] - 4.5, 3.6)
    return t.indici()


# ------------------------------------------------------------------------------------------- ritratto

def ritratto(s, verso=-1, espr='serio'):
    """Ritratto 96×64 delle transizioni: testa e spalle."""
    t = Tela(96, 64)
    pan = s.get('pancia', 0)
    h = Testa(48, 29, 16.5, 18.5)
    capelli_dietro(t, s, h, 'ritratto')
    sw = 40 + 3 * pan
    so = s['sopra']
    k = 2.3
    top = 50
    if so == 'canotta':
        t.parte(poligono([(h.cx - sw + 8, 50), (h.cx + sw - 8, 50), (h.cx + sw, 64), (h.cx - sw, 64)]), 'SK', ombra=3)
    t.parte(rett(h.cx - 7, 40, h.cx + 7, 54), 'SK', ombra=3)
    busto = poligono([(h.cx - 22, top), (h.cx + 22, top), (h.cx + sw - 6, 55), (h.cx + sw, 65), (h.cx - sw, 65),
                      (h.cx - sw + 6, 55)])
    if so == 'canotta':
        busto = {q for q in busto if q[1] >= 56} | rett(h.cx - 21, top, h.cx - 15, 57) | rett(h.cx + 15, top, h.cx + 21, 57)
    t.parte(busto, 'TO', ombra=5)
    if s.get('bicolore'):
        t.parte({q for q in busto if q[0] >= h.cx}, 'A1', bordo=False)
        t.segna({q for q in busto if q[0] >= h.cx and any((q[0] + a, q[1] + b) not in busto for a, b in N4)}, 'O')
    dettagli_busto(t, s, h.cx, 22, 26, 26, 66, busto, k=k / 1.6, top=top)
    if acc(s, 'cuffie'):
        pass
    testa_fronte(t, s, h, espr, verso)
    return t.indici()


# --------------------------------------------------------------------------------------------- emblema

def emblema(w, h, cx, cy, r, pieno=True):
    """Il timbro di «U Sistema»: un anello con dentro una piramide a quattro gradoni (R-10.2: piramide a 4 livelli).
    -> dict con le maschere 'pieno' (da riempire) e 'bordo' (contorno). Coordinate dentro w×h."""
    anello = ellisse(cx, cy, r, r) - ellisse(cx, cy, r * 0.74, r * 0.74)
    pir = set()
    base = cy + 0.42 * r
    alt = 0.19 * r
    for k in range(4):
        larg = r * (0.98 - 0.2 * k)
        y1 = base - k * alt
        pir |= rett(cx - larg / 2, y1 - alt + 1, cx + larg / 2, y1)
    forma = {q for q in (anello | pir) if 0 <= q[0] < w and 0 <= q[1] < h}
    bordo = {q for q in forma if any((q[0] + a, q[1] + b) not in forma for a, b in N4)}
    return {'forma': forma, 'bordo': bordo, 'pieno': forma - bordo if pieno else set()}
