"""Blocco 4.7 - medaglie dei 9 Dossier (R-GFX-42).

Le medaglie della Scheda Allenatore stanno nel NARC `files/a/0/4/9` (NARC id 49), voci
62-77: sedici NCGR a 8 bit di 110 tile ciascuno, uno per medaglia, in ordine di indice
badge (0 ZEPHYR .. 15 EARTH). Le nove medaglie dei Dossier usano gli slot 0-7 (Johto) e
15 (Kanto, BADGE_EARTH) del registro 2.5, quindi le voci 62, 63, 64, 65, 66, 67, 68, 69
e 77.

Il disegno e' interamente a script: ogni voce viene svuotata (indice 0 = trasparente) e
riempita con l'emblema del suo Dossier. La FORMA del file non cambia mai (R-GFX-01):
stesso numero di tile, stesse misure, stessi indici di palette gia' presenti nella voce
(65-79). Nessuna immagine e' copiata da HeartGold.

Uso: python -I tools/grafica/4.7/medaglie47.py
Esito: MEDAGLIE_OK
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, os.path.join(PROJ, 'tools'))
sys.path.insert(0, os.path.join(PROJ, 'tools', 'grafica', '4.4'))
sys.stdout.reconfigure(errors='backslashreplace')

import trinacria_gfx as G          # noqa: E402
import comune44 as C               # noqa: E402

sys.path.insert(0, HERE)
import schede47 as S               # noqa: E402

REL = 'files/a/0/4/9'
VOCO = 10                          # 110 tile = 10 colonne x 11 righe
RIGHE = 11
SIZE = 8                           # lato di una tile in pixel

# slot del registro 2.5 -> (voce del NARC, alias, emblema)
DOSSIER = [
    (0, 62, 'BADGE_DOSSIER_LIOTRU', 'liotru'),
    (1, 63, 'BADGE_DOSSIER_ARETUSA', 'aretusa'),
    (2, 64, 'BADGE_DOSSIER_CARRUBBA', 'carrubba'),
    (3, 65, 'BADGE_DOSSIER_PIRRERA', 'pirrera'),
    (4, 66, 'BADGE_DOSSIER_TELAMUNI', 'telamuni'),
    (5, 67, 'BADGE_DOSSIER_MULINU', 'mulinu'),
    (6, 68, 'BADGE_DOSSIER_PILUNU', 'pilunu'),
    (7, 69, 'BADGE_DOSSIER_GENIU', 'geniu'),
    (15, 77, 'BADGE_DOSSIER_CERERE', 'cerere'),
]

# le sette medaglie di Kanto che la trama non usa restano com'e' (R-GFX-43)

W = VOCO * SIZE                    # 80 pixel
H = RIGHE * SIZE                   # 88 pixel


def trova_repo(arg=None):
    for c in (arg, os.environ.get('TRINACRIA_REPO'),
              os.path.join(PROJ, '..', 'pokeheartgold'), r'F:\Progetti\pokeheartgold'):
        if c and os.path.isdir(c):
            return os.path.abspath(c)
    raise C.Errore('repository di HeartGold non trovato')


class Tela:
    """Griglia di pixel a indici di palette, con le primitive che servono agli emblemi."""

    def __init__(self, w, h):
        self.w, self.h = w, h
        self.p = [0] * (w * h)

    def metti(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.p[y * self.w + x] = c

    def rett(self, x0, y0, x1, y1, c):
        for y in range(min(y0, y1), max(y0, y1) + 1):
            for x in range(min(x0, x1), max(x0, x1) + 1):
                self.metti(x, y, c)

    def cornice(self, x0, y0, x1, y1, c, sp=1):
        for k in range(sp):
            self.rett(x0 + k, y0 + k, x1 - k, y0 + k, c)
            self.rett(x0 + k, y1 - k, x1 - k, y1 - k, c)
            self.rett(x0 + k, y0 + k, x0 + k, y1 - k, c)
            self.rett(x1 - k, y0 + k, x1 - k, y1 - k, c)

    def disco(self, cx, cy, r, c):
        for y in range(cy - r, cy + r + 1):
            for x in range(cx - r, cx + r + 1):
                if (x - cx) ** 2 + (y - cy) ** 2 <= r * r:
                    self.metti(x, y, c)

    def anello(self, cx, cy, r, sp, c):
        for y in range(cy - r - sp, cy + r + sp + 1):
            for x in range(cx - r - sp, cx + r + sp + 1):
                d = (x - cx) ** 2 + (y - cy) ** 2
                if (r - sp) ** 2 <= d <= r * r:
                    self.metti(x, y, c)

    def triangolo(self, x0, y0, x1, y1, x2, y2, c):
        pts = [(x0, y0), (x1, y1), (x2, y2)]
        minx = min(p[0] for p in pts)
        maxx = max(p[0] for p in pts)
        miny = min(p[1] for p in pts)
        maxy = max(p[1] for p in pts)

        def segno(ax, ay, bx, by, cx_, cy_):
            return (ax - cx_) * (by - cy_) - (bx - cx_) * (ay - cy_)

        for y in range(miny, maxy + 1):
            for x in range(minx, maxx + 1):
                b1 = segno(x0, y0, x1, y1, x, y) < 0
                b2 = segno(x1, y1, x2, y2, x, y) < 0
                b3 = segno(x2, y2, x0, y0, x, y) < 0
                if b1 == b2 == b3:
                    self.metti(x, y, c)

    def linea(self, x0, y0, x1, y1, c, sp=1):
        dx, dy = abs(x1 - x0), -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        e = dx + dy
        while True:
            for k in range(sp):
                self.metti(x0 + k, y0, c)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * e
            if e2 >= dy:
                e += dy
                x0 += sx
            if e2 <= dx:
                e += dx
                y0 += sy

    def tile(self):
        """-> [[[8 righe di 8 indici]]] nell'ordine delle tile del NCGR."""
        out = []
        for ty in range(RIGHE):
            for tx in range(VOCO):
                t = []
                for y in range(SIZE):
                    t.append([self.p[(ty * SIZE + y) * self.w + tx * SIZE + x] for x in range(SIZE)])
                out.append(t)
        return out


def indici(voce):
    """Gli indici di palette gia' presenti nella voce, dal piu' scuro al piu' chiaro."""
    g = C.ncgr_leggi(voce)
    usati = set()
    for t in g['tile']:
        for riga in t:
            usati |= set(riga)
    usati.discard(0)
    return g, sorted(usati)


def emblema(nome, c_chiaro, c_medio, c_scuro):
    """Disegna l'emblema del Dossier su una tela 80x88 gia' vuota."""
    t = Tela(W, H)
    cx, cy = W // 2, H // 2

    if nome == 'liotru':
        # Liotru: elefante stilizzato su una base, la testa verso sinistra
        t.rett(12, 70, 67, 73, c_scuro)
        t.rett(20, 48, 58, 68, c_medio)
        t.rett(24, 44, 54, 48, c_medio)
        t.disco(30, 42, 11, c_medio)
        t.rett(14, 40, 22, 46, c_medio)
        t.rett(16, 34, 20, 42, c_scuro)
        t.rett(22, 52, 30, 60, c_chiaro)
        t.rett(34, 52, 42, 60, c_chiaro)
        t.rett(46, 52, 54, 60, c_chiaro)
        t.rett(24, 68, 30, 76, c_scuro)
        t.rett(50, 68, 56, 76, c_scuro)
        t.linea(58, 46, 68, 40, c_medio, 2)
        t.disco(69, 39, 2, c_scuro)

    elif nome == 'aretusa':
        # Aretusa: la fonte, con l'acqua che zampilla e il cerchio della ninfa
        t.anello(cx, 34, 22, 2, c_scuro)
        t.disco(cx, 34, 15, c_medio)
        t.disco(cx, 34, 10, c_chiaro)
        t.rett(cx - 2, 40, cx + 2, 62, c_scuro)
        for k, dx in enumerate((-14, -7, 0, 7, 14)):
            t.linea(cx + dx, 56, cx + dx + (2 if dx > 0 else -2 if dx < 0 else 0), 70, c_medio)
        t.rett(18, 70, 62, 73, c_scuro)

    elif nome == 'carrubba':
        # Carrubba: il baccello del carrubo, con i semi
        t.anello(cx - 2, cy, 24, 3, c_scuro)
        t.disco(cx - 2, cy, 18, c_medio)
        for k in range(-2, 3):
            t.disco(cx + k * 7 - 2, cy, 4, c_chiaro)
            t.disco(cx + k * 7 - 2, cy, 2, c_scuro)
        t.linea(cx - 26, cy - 22, cx - 34, cy - 30, c_scuro, 2)

    elif nome == 'pirrera':
        # Pirrera: la cava, con i gradoni di pietra
        t.triangolo(6, 78, 40, 22, 74, 78, c_medio)
        t.triangolo(16, 78, 40, 38, 64, 78, c_chiaro)
        for y in (52, 62, 72):
            t.linea(10 + (78 - y) // 3, y, 70 - (78 - y) // 3, y, c_scuro, 1)
        t.rett(34, 18, 46, 24, c_scuro)

    elif nome == 'telamuni':
        # Telamuni: il telamone, la colonna del tempio
        t.rett(20, 70, 60, 76, c_scuro)
        t.rett(26, 26, 54, 70, c_medio)
        for x in (30, 38, 46, 52):
            t.rett(x, 28, x + 3, 68, c_chiaro)
        t.rett(18, 18, 62, 26, c_scuro)
        t.rett(22, 14, 58, 18, c_chiaro)
        t.disco(cx, 40, 5, c_scuro)

    elif nome == 'mulinu':
        # Mulinu: il mulino a vento, con le pale
        t.rett(34, 40, 46, 80, c_medio)
        t.rett(30, 36, 50, 42, c_scuro)
        t.disco(cx, 38, 4, c_scuro)
        for dx, dy in ((1, 1), (-1, 1), (1, -1), (-1, -1)):
            t.linea(cx, 38, cx + dx * 30, 38 + dy * 30, c_chiaro, 3)
        t.triangolo(30, 14, 34, 24, 26, 24, c_scuro)
        t.triangolo(50, 14, 54, 24, 46, 24, c_scuro)

    elif nome == 'pilunu':
        # Pilunu: i piloni dello Stretto, con l'acqua sotto
        t.rett(18, 16, 24, 74, c_scuro)
        t.rett(56, 16, 62, 74, c_scuro)
        t.rett(12, 12, 30, 18, c_medio)
        t.rett(50, 12, 68, 18, c_medio)
        t.linea(24, 20, 56, 20, c_chiaro, 1)
        t.linea(24, 26, 56, 26, c_chiaro, 1)
        for y in (76, 80, 84):
            for x in range(8, 72, 12):
                t.linea(x, y, x + 6, y, c_medio)

    elif nome == 'geniu':
        # Geniu: l'arco del Genio, con la lampada
        t.anello(cx, 62, 28, 5, c_scuro)
        t.rett(6, 62, 74, 78, c_medio)
        t.disco(cx, 62, 24, c_chiaro)
        t.rett(4, 60, 76, 64, c_medio)
        t.disco(cx, 30, 9, c_medio)
        t.triangolo(cx - 6, 24, cx + 6, 24, cx, 14, c_chiaro)

    elif nome == 'cerere':
        # Cerere: la spiga di grano
        t.linea(cx, 78, cx, 20, c_scuro, 2)
        for y in range(22, 66, 8):
            t.linea(cx, y, cx - 12, y - 8, c_medio, 2)
            t.linea(cx, y, cx + 12, y - 8, c_medio, 2)
            t.disco(cx - 13, y - 9, 3, c_chiaro)
            t.disco(cx + 13, y - 9, 3, c_chiaro)
        t.disco(cx, 16, 4, c_chiaro)
        t.rett(18, 78, 62, 82, c_scuro)

    else:
        raise C.Errore('emblema sconosciuto: %s' % nome)
    return t


def costruisci(repo, build=None):
    """Riscrive le nove voci delle medaglie. -> (voci cambiate, elenco per il JSON)"""
    build = build or os.path.join(PROJ, 'build', 'grafica', '4.7')
    sorgente = os.path.join(repo, *REL.split('/'))
    with open(sorgente, 'rb') as fh:
        narc = G.Narc(fh.read())
    if len(narc.files) < 78:
        raise C.Errore('%s: %d voci, attese almeno 78' % (REL, len(narc.files)))

    voci = []
    for slot, voce, alias, nome in DOSSIER:
        orig = narc.files[voce]
        g, usati = indici(orig)
        if not usati:
            raise C.Errore('voce %d senza colori' % voce)
        chiaro = usati[-1]
        medio = usati[len(usati) // 2]
        scuro = usati[0]
        tela = emblema(nome, chiaro, medio, scuro)
        tile = tela.tile()
        nuovo = C.ncgr_patch(orig, tile)
        if len(nuovo) != len(orig):
            raise C.Errore('voce %d: %d byte invece di %d (R-GFX-01)'
                           % (voce, len(nuovo), len(orig)))
        narc.files[voce] = nuovo
        voci.append({'slot': slot, 'voce': voce, 'alias': alias, 'emblema': nome,
                     'byte': len(nuovo), 'sha1_hg': G.sha1(orig), 'sha1_nuovo': G.sha1(nuovo),
                     'colori': len(usati)})

    dati = narc.pack()
    dest = os.path.join(build, *REL.split('/'))
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, 'wb') as fh:
        fh.write(dati)

    # prova: l'archivio riletto ha le stesse voci nuove e le altre invariate
    riletto = G.Narc(dati)
    if len(riletto.files) != len(narc.files):
        raise C.Errore('archivio riscritto con %d voci invece di %d'
                       % (len(riletto.files), len(narc.files)))
    for slot, voce, alias, nome in DOSSIER:
        if riletto.files[voce] != narc.files[voce]:
            raise C.Errore('voce %d diversa dopo la riscrittura' % voce)
    return voci, dest


def anteprime(voci, cartella, build=None):
    """Un PNG per medaglia (indici di palette, 80x88) per la revisione a schermo."""
    build = build or os.path.join(PROJ, 'build', 'grafica', '4.7')
    os.makedirs(cartella, exist_ok=True)
    fuori = []
    for v in voci:
        b = open(os.path.join(build, *REL.split('/')), 'rb').read()
        g = C.ncgr_leggi(G.Narc(b).files[v['voce']])
        pix = [0] * (W * H)
        for ty in range(RIGHE):
            for tx in range(VOCO):
                t = g['tile'][ty * VOCO + tx]
                for y in range(SIZE):
                    for x in range(SIZE):
                        pix[(ty * SIZE + y) * W + tx * SIZE + x] = t[y][x]
        # palette grigia leggibile: gli indici 65-79 diventano 1-15
        base = sorted({p for p in pix if p})
        mappa = {0: 0}
        for k, p in enumerate(base):
            mappa[p] = 1 + k % 15
        grigia = [(0, 0, 0)] + [(16 * k, 16 * k, 16 * k) for k in range(1, 16)]
        path = os.path.join(cartella, 'medaglia_%02d_%s.png' % (v['slot'], v['emblema']))
        C.salva_png(path, W, H, grigia, [mappa[p] for p in pix], bpp=4)
        fuori.append(path)
    return fuori


def main(argv=None):
    repo = trova_repo()
    voci, dest = costruisci(repo)
    print('medaglie: %d voci riscritte in %s' % (len(voci), REL))
    for v in voci:
        print('  slot %2d voce %2d %-24s %-9s %5d byte' % (v['slot'], v['voce'], v['alias'],
                                                           v['emblema'], v['byte']))
    anteprime(voci, os.path.join(PROJ, 'build', 'grafica', '4.7', 'anteprime'))
    print('MEDAGLIE_OK')
    return 0


if __name__ == '__main__':
    sys.exit(main())
