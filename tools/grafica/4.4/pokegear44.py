"""Blocco 4.4 — mappa della Sicilia nel Pokégear (GFX-PGMAP-*), tabella del Volo e tabella dei luoghi.

Disegna in pixel la mappa 47×20 tile (una tile per cella della matrice 0, due righe di mare sopra) e
tutte le toppe che il codice copia dalla schermata `pgmap_gra_00000011.NSCR` (unk_170):
  - righe 0–19, colonne 0–46: la mappa (ov101_021EAF40);
  - colonne 48–56: toppe del livello di sblocco 0 e 1 = copia della mappa (nessun lato nascosto, R-GFX-30);
  - (41,20), (41,27), (48,27) 5×6: toppe di Safari/Fiordoro = copia della mappa in (1,9);
  - (55,20) 3×4: toppa di Sinjoh (Pantelleria) = copia della mappa in (19,1);
  - (55,24) 3×3: toppa della S.S. Aqua (Favignana, traghetto di Lampedusa) = traghetto sul mare in (24,15);
  - righe 20–31 dalla colonna 0: le 27 toppe «non visitata» dei punti di volo (grigie);
  - righe 32–63: le cornici gialle dei luoghi (una per misura).
Tutto passa per un foglio di al massimo 768 tile a 8 bit (pgmap_gra_00000010.png) con gli indici di colore
che la mappa di HeartGold usa già: le 6 palette dei temi del Pokégear (NCLR 20–25) restano quelle."""
import math

import comune44 as C
from dati44 import Dati, W0, LUOGHI, COLONNA_EST

WT, HT = 47, 20            # mappa a schermo, in tile
NW, NH = 64, 64            # schermata unk_170
TILE_MAX = 768             # 512×96 a 8 bit

# ruoli degli indici della palette 20 (letti sulla mappa di HeartGold, tutti fra 2 e 47)
I = dict(mare4=40, mare3=39, mare2=38, mare1=37, sabbia=23, pianura=28, pianura2=29, bosco=30, albero=31,
         prato=11, collina=24, collina2=25, monte=26, monte2=27, bianco=10, scuro=16, ombra=18,
         rosso1=4, rosso2=3, rosso3=2, grigio1=20, grigio2=19, grigio3=18, grigio4=9,
         giallo=44, arancio=45, rosso_cornice=47, lago=13, fiume=7)

# isole minori disegnate nel mare (tile del Pokégear, centro e raggi in pixel)
ISOLE = {
    'MAP_TP_FAVIGNANA': (0, 6, [(4, 4, 5, 3)]),
    'MAP_AG_LAMPEDUSA': (16, 18, [(4, 4, 6, 3)]),
    'MAP_TP_PANTELLERIA': (4, 15, [(4, 4, 5, 4)]),
    'MAP_ME_ISOLE_EOLIE': (37, 0, [(3, 6, 3, 2), (11, 4, 3, 3), (18, 7, 2, 2), (24, 4, 3, 2), (29, 9, 2, 2)]),
}
ISOLE_TILE = {'MAP_TP_FAVIGNANA': (0, 6, 1, 1), 'MAP_AG_LAMPEDUSA': (16, 18, 1, 1),
              'MAP_TP_PANTELLERIA': (4, 15, 1, 1), 'MAP_ME_ISOLE_EOLIE': (37, 0, 4, 2)}


def _rumore(x, y, seme=7):
    v = (x * 374761393 + y * 668265263 + seme * 2147483647) & 0xFFFFFFFF
    v = ((v ^ (v >> 13)) * 1274126177) & 0xFFFFFFFF
    return ((v ^ (v >> 16)) & 0xFFFF) / 65535.0


def _liscio(x, y):
    """Rumore di valore a passo 6 px, fra -1 e 1."""
    gx, gy = x / 6.0, y / 6.0
    x0, y0 = int(math.floor(gx)), int(math.floor(gy))
    fx, fy = gx - x0, gy - y0
    fx, fy = fx * fx * (3 - 2 * fx), fy * fy * (3 - 2 * fy)
    a, b = _rumore(x0, y0), _rumore(x0 + 1, y0)
    c, d = _rumore(x0, y0 + 1), _rumore(x0 + 1, y0 + 1)
    return ((a * (1 - fx) + b * fx) * (1 - fy) + (c * (1 - fx) + d * fx) * fy) * 2 - 1


class Mappa:
    def __init__(self, dati=None):
        self.d = dati or Dati()
        self.W, self.H = WT * 8, HT * 8
        self.pix = [I['mare4']] * (self.W * self.H)
        self.terra = [False] * (self.W * self.H)
        self.tipo_px = [None] * (self.W * self.H)

    # ---------------------------------------------------------------- terra e mare
    def _terra_cella(self, tx, ty):
        t = self.d.terreno(tx, ty - 2)
        return 1.0 if t not in (None, 'mare') else 0.0

    def disegna_terra(self):
        W, H = self.W, self.H
        for py in range(H):
            for px in range(W):
                fx, fy = px / 8.0 - 0.5, py / 8.0 - 0.5
                x0, y0 = int(math.floor(fx)), int(math.floor(fy))
                ax, ay = fx - x0, fy - y0
                v = (self._terra_cella(x0, y0) * (1 - ax) * (1 - ay) + self._terra_cella(x0 + 1, y0) * ax * (1 - ay)
                     + self._terra_cella(x0, y0 + 1) * (1 - ax) * ay + self._terra_cella(x0 + 1, y0 + 1) * ax * ay)
                if v > 0.5 + 0.16 * _liscio(px, py):
                    self.terra[py * W + px] = True
        for sym, (tx, ty, blobs) in ISOLE.items():
            for ox, oy, rx, ry in blobs:
                cx, cy = tx * 8 + ox, ty * 8 + oy
                for py in range(cy - ry - 1, cy + ry + 2):
                    for px in range(cx - rx - 1, cx + rx + 2):
                        if 0 <= px < W and 0 <= py < H and ((px - cx) / rx) ** 2 + ((py - cy) / ry) ** 2 <= 1.0:
                            self.terra[py * W + px] = True
        # distanza dalla terra per le sfumature del mare (BFS a 4 vicini, fino a 12 px)
        dist = [99] * (W * H)
        coda = [i for i in range(W * H) if self.terra[i]]
        for i in coda:
            dist[i] = 0
        k = 0
        while k < len(coda):
            i = coda[k]
            k += 1
            if dist[i] >= 12:
                continue
            x, y = i % W, i // W
            for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if 0 <= nx < W and 0 <= ny < H and dist[ny * W + nx] > dist[i] + 1:
                    dist[ny * W + nx] = dist[i] + 1
                    coda.append(ny * W + nx)
        for i in range(W * H):
            x, y = i % W, i // W
            if self.terra[i]:
                continue
            dd = dist[i]
            self.pix[i] = I['mare1'] if dd <= 1 else I['mare2'] if dd <= 3 else I['mare3'] if dd <= 7 else I['mare4']
            # onde regolari in mare aperto (motivo a passo 8, uguale in ogni tile: non costa tile)
            if dd > 9 and (x % 16, y % 16) in ((3, 4), (4, 4), (11, 12), (12, 12)):
                self.pix[i] = I['mare3']
        for i in range(W * H):
            if not self.terra[i]:
                continue
            x, y = i % W, i // W
            t = self.d.terreno(x // 8, y // 8 - 2) or 'campagna'
            costa = any(not self.terra[ny * W + nx] for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1))
                        if 0 <= nx < W and 0 <= ny < H)
            self.tipo_px[i] = t
            if costa:
                c = I['sabbia']
            elif t == 'colline':
                c = I['collina'] if (x + y) % 2 == 0 else I['pianura2']
            elif t == 'bosco':
                c = I['albero'] if (x % 4, y % 4) in ((1, 1), (3, 3)) else I['bosco']
            elif t == 'etna':
                c = I['collina2'] if (x + y) % 2 == 0 else I['pianura2']
            else:
                c = I['pianura2'] if (x % 8, y % 8) == (5, 2) else I['pianura']
            self.pix[i] = c

    def disegna_etna(self):
        cs = [(x, y) for (x, y), r in self.d.celle.items() if r.get('paesaggio') == 'etna']
        cx = sum(x for x, _ in cs) / len(cs) * 8 + 4
        cy = (sum(y for _, y in cs) / len(cs) + 2) * 8 + 4
        h, r = 16, 15
        for py in range(int(cy - h), int(cy + 5)):
            dy = py - (cy - h)
            half = r * dy / (h + 5)
            for px in range(int(cx - half), int(cx + half) + 1):
                i = py * self.W + px
                if not self.terra[i]:
                    continue
                if dy < 4:
                    c = I['bianco'] if px < cx + 1 else I['grigio1']
                else:
                    c = I['monte'] if px < cx + (dy % 3) - 1 else I['monte2']
                self.pix[i] = c
        # pennacchio di cenere
        for k in range(6):
            px, py = int(cx + 1 + k), int(cy - h - 2 - k // 2)
            for dx in (0, 1):
                self.pix[py * self.W + px + dx] = I['grigio2']

    def disegna_laghi(self):
        # Pergusa e il lago di Ficuzza/Jato: un ovale d'acqua dolce nella cella principale
        for sym in ('MAP_EN_LAGO_DI_PERGUSA', 'MAP_PA_DIGA_JATO'):
            p = self.d.principale(sym)
            if not p:
                continue
            cx, cy = p[0] * 8 + 4, (p[1] + 2) * 8 + 4
            for py in range(cy - 2, cy + 3):
                for px in range(cx - 3, cx + 4):
                    if ((px - cx) / 3.2) ** 2 + ((py - cy) / 2.2) ** 2 <= 1:
                        self.pix[py * self.W + px] = I['lago']

    # ---------------------------------------------------------------- strade e città
    def _linea(self, x0, y0, x1, y1, c, spessore=2):
        n = max(abs(x1 - x0), abs(y1 - y0), 1)
        for k in range(n + 1):
            x = round(x0 + (x1 - x0) * k / n)
            y = round(y0 + (y1 - y0) * k / n)
            for dx in range(spessore):
                for dy in range(spessore):
                    if 0 <= x + dx < self.W and 0 <= y + dy < self.H:
                        self.pix[(y + dy) * self.W + x + dx] = c

    def disegna_strade(self):
        """Strade = mappe di profilo STRADA: le celle della stessa strada fra loro, più un tratto verso
        ogni mappa vicina raggiunta da un confine percorribile (registri 2.1–2.3)."""
        d = self.d
        def tratto(a, b):
            self._linea(a[0] * 8 + 3, (a[1] + 2) * 8 + 3, b[0] * 8 + 3, (b[1] + 2) * 8 + 3, I['bianco'])
        for s in sorted(d.celle_mappa):
            if d.profilo(s) != 'STRADA':
                continue
            cs = set(d.celle_mappa[s])
            for (x, y) in sorted(cs):
                for n in ((x + 1, y), (x, y + 1)):
                    if n in cs:
                        tratto((x, y), n)
            visti = set()
            for c in d.mappe[s].get('confini_percorribili') or ():
                if c['verso'] in visti or c['verso'] not in d.celle_mappa:
                    continue
                visti.add(c['verso'])
                tratto(tuple(c['da_cella']), tuple(c['a_cella']))

    def _scatola(self, x, y, w, h, fill, bordo, luce):
        for py in range(y, y + h):
            for px in range(x, x + w):
                ang = (px in (x, x + w - 1)) and (py in (y, y + h - 1))
                if ang:
                    continue
                c = bordo if px in (x, x + w - 1) or py in (y, y + h - 1) else (luce if py == y + 1 else fill)
                self.pix[py * self.W + px] = c

    def citta_volo(self, riga, grigia=False, pix=None):
        x, y, w, h = riga['x'], riga['y'] + 2, riga['width'], riga['height']
        if grigia:
            self._scatola(x * 8 + 1, y * 8 + 1, w * 8 - 2, h * 8 - 2, I['grigio2'], I['scuro'], I['grigio1'])
        else:
            self._scatola(x * 8 + 1, y * 8 + 1, w * 8 - 2, h * 8 - 2, I['rosso2'], I['rosso3'], I['rosso1'])

    def disegna_citta(self):
        d = self.d
        volo = {r['mapIDforName'] for r in d.voli}
        for s, cs in d.celle_mappa.items():
            if s in volo or d.profilo(s) == 'STRADA':
                continue
            p = d.principale(s) or cs[0]
            cx, cy = p[0] * 8 + 2, (p[1] + 2) * 8 + 2
            if d.profilo(s) == 'CITTA':
                self._scatola(cx, cy, 5, 5, I['rosso2'], I['rosso3'], I['rosso1'])
            elif d.profilo(s) == 'PAESE':
                self._scatola(cx + 1, cy + 1, 4, 4, I['rosso2'], I['rosso3'], I['rosso2'])
            else:
                self._scatola(cx + 1, cy + 1, 3, 3, I['arancio'], I['rosso3'], I['arancio'])
        for r in d.voli:
            self.citta_volo(r)

    def disegna(self):
        self.disegna_terra()
        self.disegna_etna()
        self.disegna_laghi()
        self.disegna_strade()
        self.disegna_citta()
        return self

    # ---------------------------------------------------------------- ritagli in tile
    def tile(self, tx, ty, pix=None):
        pix = pix or self.pix
        return [[pix[(ty * 8 + y) * self.W + tx * 8 + x] for x in range(8)] for y in range(8)]


def traghetto(m):
    """Copia della mappa con il traghetto disegnato al centro della zona (24,15)–(26,17)."""
    pix = list(m.pix)
    cx, cy = 25 * 8 + 1, 16 * 8 + 3
    for x in range(-6, 7):
        pix[(cy + 2) * m.W + cx + x] = I['scuro']
        if abs(x) < 6:
            pix[(cy + 1) * m.W + cx + x] = I['bianco']
    for x in range(-3, 4):
        pix[cy * m.W + cx + x] = I['bianco']
    pix[(cy - 1) * m.W + cx] = I['rosso2']
    pix[(cy - 2) * m.W + cx] = I['rosso2']
    for x in range(-8, 9, 4):
        pix[(cy + 4) * m.W + cx + x] = I['mare1']
    return pix


def cornice(w, h, interna=False):
    """Cornice gialla di un luogo largo w×h tile: (w+2)×(h+2) tile attorno (interna=False) o w×h dentro."""
    tw, th = (w, h) if interna else (w + 2, h + 2)
    W, H = tw * 8, th * 8
    pix = [0] * (W * H)
    x0, y0 = (0, 0) if interna else (8, 8)
    x1, y1 = (W, H) if interna else (W - 8, H - 8)
    for y in range(H):
        for x in range(W):
            dx = max(x0 - x, x - (x1 - 1), 0)
            dy = max(y0 - y, y - (y1 - 1), 0)
            if interna:
                dx = min(x - x0, x1 - 1 - x)
                dy = min(y - y0, y1 - 1 - y)
                dd = min(dx, dy)
                if dd == 0:
                    pix[y * W + x] = I['rosso_cornice']
                elif dd == 1:
                    pix[y * W + x] = I['giallo']
                continue
            dd = max(dx, dy)
            if 1 <= dd <= 1 and not (dx == 1 and dy == 1):
                pix[y * W + x] = I['giallo']
            elif dd == 2 and not (dx == 2 and dy == 2) and not (dx >= 2 and dy >= 1) and not (dy >= 2 and dx >= 1):
                pix[y * W + x] = I['rosso_cornice']
    return tw, th, W, pix


class Impaginatore:
    """Mette rettangoli di tile in una zona della schermata, a scaffali."""

    def __init__(self, x0, y0, x1, y1):
        self.x0, self.y0, self.x1, self.y1 = x0, y0, x1, y1
        self.x, self.y, self.h = x0, y0, 0

    def posto(self, w, h):
        if self.x + w > self.x1:
            self.x, self.y, self.h = self.x0, self.y + self.h, 0
        if self.y + h > self.y1:
            raise C.Errore('zona della schermata piena (%d×%d)' % (w, h))
        p = (self.x, self.y)
        self.x += w
        self.h = max(self.h, h)
        return p


def costruisci(dati=None):
    """-> dict con foglio (tile), voci della schermata 64×64, tabella del volo, tabella dei luoghi, pixel della mappa."""
    d = dati or Dati()
    m = Mappa(d).disegna()
    fog = C.Foglio(TILE_MAX, flip=True, prime=[[[0] * 8 for _ in range(8)]])
    vuota = C.voce(0)
    scr = [vuota] * (NW * NH)

    def metti(dx, dy, w, h, pix, sx, sy, Wp=None):
        Wp = Wp or m.W
        for ty in range(h):
            for tx in range(w):
                t = [[pix[((sy + ty) * 8 + y) * Wp + (sx + tx) * 8 + x] for x in range(8)] for y in range(8)]
                scr[(dy + ty) * NW + dx + tx] = fog.aggiungi(t)

    # mappa e toppe che la ricopiano
    metti(0, 0, WT, HT, m.pix, 0, 0)
    metti(48, 0, 6, 20, m.pix, 22, 0)
    metti(54, 0, 3, 20, m.pix, 29, 0)
    for sx, sy in ((41, 20), (41, 27), (48, 27)):
        metti(sx, sy, 5, 6, m.pix, 1, 9)
    metti(55, 20, 3, 4, m.pix, 19, 1)
    metti(55, 24, 3, 3, traghetto(m), 24, 15)

    # toppe «non visitata» dei punti di volo
    imp = Impaginatore(0, 20, 41, 32)
    volo = []
    for k, r in enumerate(d.voli):
        g = Mappa(d)
        g.pix = list(m.pix)
        g.citta_volo(r, grigia=True)
        dw, dh = r['width'] + 2, r['height'] + 2
        dxo, dyo = 1, 1
        px0, py0 = r['x'] - dxo, r['y'] + 2 - dyo
        if px0 < 0:
            dxo, dw, px0 = 0, dw - 1, 0
        if py0 < 0:
            dyo, dh, py0 = 0, dh - 1, 0
        sx, sy = imp.posto(dw, dh)
        metti(sx, sy, dw, dh, g.pix, px0, py0)
        volo.append(dict(riga=k, simbolo=r['mapIDforName'], flypoint=r['flypoint'], x=r['x'], y=r['y'],
                         width=r['width'], height=r['height'], unk_05=k, unk170SrcX=sx, unk170SrcY=sy,
                         unk170DestWidth=dw, unk170DestHeight=dh, unk170DestX=dxo, unk170DestY=dyo))

    # luoghi (sLocationSpecs) e loro cornici
    scelte, escluse = d.scelta_luoghi()
    luoghi = []
    cornici = {}
    imp2 = Impaginatore(0, 32, NW, NH)
    for s in scelte:
        if s in ISOLE_TILE:
            x, y, w, h = ISOLE_TILE[s]
        else:
            x, y, w, h = d.rettangolo(s)
            y += 2
        interna = x == 0 or y == 0
        chiave = (w, h, interna)
        if chiave not in cornici:
            tw, th, Wp, pix = cornice(w, h, interna)
            sx, sy = imp2.posto(tw, th)
            metti(sx, sy, tw, th, pix, 0, 0, Wp)
            cornici[chiave] = (sx, sy, tw, th)
        sx, sy, tw, th = cornici[chiave]
        if interna and tw * th >= 9:
            raise C.Errore('%s: cornice interna di %d×%d tile, il codice la sposterebbe' % (s, tw, th))
        luoghi.append(dict(mapId=s, x=x, y=y, width=w, height=h, objXoffset=0, objYoffset=0,
                           tilemapUnk170SrcX=sx, tilemapUnk170SrcY=sy, tilemapUnk170DestWidth=tw,
                           tilemapUnk170DestHeight=th, nome=d.nome(s), profilo=d.profilo(s),
                           regione='est' if x >= COLONNA_EST else 'ovest'))
    if len(luoghi) != LUOGHI:
        raise C.Errore('%d luoghi invece di %d' % (len(luoghi), LUOGHI))
    # nessuna sovrapposizione fra i rettangoli (la ricerca per coordinate prende il primo)
    occ = {}
    for L in luoghi:
        for xx in range(L['x'], L['x'] + L['width']):
            for yy in range(L['y'], L['y'] + L['height']):
                if (xx, yy) in occ:
                    raise C.Errore('%s e %s si sovrappongono in (%d,%d)' % (occ[(xx, yy)], L['mapId'], xx, yy))
                occ[(xx, yy)] = L['mapId']
    return dict(mappa=m, foglio=fog, schermata=scr, volo=volo, luoghi=luoghi, escluse=escluse,
                cornici=len(cornici))


if __name__ == '__main__':
    import os
    r = costruisci()
    print('tile', len(r['foglio'].tile), 'cornici', r['cornici'], 'luoghi', len(r['luoghi']))
