"""Motore delle celle del blocco 4.2: dalla scheda di una cella al modello 3D, ai permessi e ai varchi.

Una cella è 32×32 caselle (R-GFX-10): un terreno per casella (texture, comportamento, collisione)
e una lista di oggetti 3D (volumi degli edifici, cilindri, sagome, porte). Il motore:
  - dipinge i lati (mare, ostacoli dei confini chiusi, varchi alle caselle 13–18: R-GFX-19);
  - mette gli edifici con la porta sul lato sud e la casella davanti libera;
  - traccia strade e vicoli col percorso più breve fra varchi, porte e punti;
  - riempie, decora e controlla che ogni porta, varco e punto sia raggiungibile.
Coordinate: casella (c, r) = colonna, riga; riga 0 a nord. Unità del mondo: una casella = 16,
origine al centro della cella (documento 4.1, §4.3).
"""
import collections
import math

# --------------------------------------------------------------------------- comportamenti
# include/constants/metatile_behavior.h (valori contati nell'enum) e uso nelle celle di HeartGold
B = dict(
    NORMALE=0x00, ERBA_ALTA=0x02, BOTTINTESTA=0x06, GROTTA=0x08, FIUME=0x10, MARE=0x15, GHIACCIO=0x20,
    SABBIA=0x21, ARRAMPICATA=0x4B, USCITA_SUD=0x65, PORTA=0x69, VARCO_NORD=0x6E, BANCONE=0x80,
)
LIBERO, BLOCCATO = 0x00, 0x80

# terreno: chiave -> (texture o None, comportamento, collisione)
TERRENI = {
    'vuoto': (None, B['NORMALE'], BLOCCATO),
    'basolato': ('basolato', B['NORMALE'], LIBERO),
    'lastricato': ('lastricato', B['NORMALE'], LIBERO),
    'asfalto': ('asfalto', B['NORMALE'], LIBERO),
    'marciapiede': ('marciapiede', B['NORMALE'], LIBERO),
    'erba': ('erba', B['NORMALE'], LIBERO),
    'erba_alta': ('erba_alta', B['ERBA_ALTA'], LIBERO),
    'fiori': ('fiori', B['NORMALE'], LIBERO),
    'aiuola': ('fiori', B['NORMALE'], BLOCCATO),
    'terra': ('terra', B['NORMALE'], LIBERO),
    'sabbia': ('sabbia', B['SABBIA'], LIBERO),
    'sabbia_nera': ('sabbia_nera', B['SABBIA'], LIBERO),
    'mare': ('mare', B['MARE'], LIBERO),
    'mare_basso': ('mare_basso', B['MARE'], LIBERO),
    'acqua': ('acqua_dolce', B['FIUME'], LIBERO),
    'fango': ('fango', B['NORMALE'], BLOCCATO),
    'sciara': ('sciara', B['NORMALE'], LIBERO),
    'sciara_dura': ('sciara', B['NORMALE'], BLOCCATO),
    'cenere': ('cenere', B['NORMALE'], LIBERO),
    'campo': ('campo', B['NORMALE'], LIBERO),
    'campo_chiuso': ('campo', B['NORMALE'], BLOCCATO),
    'argilla': ('argilla', B['NORMALE'], LIBERO),
    'argilla_dura': ('argilla', B['NORMALE'], BLOCCATO),
    'scoglio': ('scoglio', B['NORMALE'], BLOCCATO),
    'scalinata': ('scalinata', B['NORMALE'], LIBERO),
    'piastrelle': ('piastrelle', B['NORMALE'], LIBERO),
    'binario_v': ('binario_v', B['NORMALE'], LIBERO),
    'binario_h': ('binario_h', B['NORMALE'], LIBERO),
    'ghiaia': ('ghiaia', B['NORMALE'], LIBERO),
    'parete': ('roccia', B['ARRAMPICATA'], BLOCCATO),
}

LATI = ('N', 'S', 'O', 'E')
VARCO = range(13, 19)          # caselle del varco su ogni lato aperto (R-GFX-19)
MARE_PROF = 8                  # profondità della fascia di mare verso una cella di mare
RIVA = 2                       # riva (sabbia o scogli) dopo il mare
STRISCIA = 2                   # profondità dell'ostacolo lungo un confine chiuso


class ErroreCella(Exception):
    pass


# --------------------------------------------------------------------------- oggetti 3D


def _t_facciata(h, th):
    """t in basso = multiplo dell'altezza della texture: il piano terra della facciata poggia a terra."""
    fondo = th * math.ceil(h / th)
    return fondo - h, fondo


class Volume:
    """Parallelepipedo: tetto, facciata sud, fianchi est e ovest (il lato nord non si vede mai)."""

    def __init__(self, c, r, w, d, h, tetto, fronte, lato=None, y0=0, blocca=True):
        self.c, self.r, self.w, self.d, self.h = c, r, w, d, h
        self.tetto, self.fronte, self.lato, self.y0, self.blocca = tetto, fronte, lato or fronte, y0, blocca

    def caselle(self):
        return [(c, r) for r in range(self.r, self.r + self.d) for c in range(self.c, self.c + self.w)]

    def quads(self, dim):
        x0, z0 = self.c * 16 - 256, self.r * 16 - 256
        x1, z1 = x0 + 16 * self.w, z0 + 16 * self.d
        y0, y1 = self.y0, self.y0 + self.h
        out = []
        if self.tetto:
            out.append((self.tetto, [(x0, y1, z0), (x0, y1, z1), (x1, y1, z1), (x1, y1, z0)],
                        [(x0 + 256, z0 + 256), (x0 + 256, z1 + 256), (x1 + 256, z1 + 256), (x1 + 256, z0 + 256)]))
        if self.fronte:
            t0, t1 = _t_facciata(self.h, dim[self.fronte][1])
            out.append((self.fronte, [(x0, y1, z1), (x0, y0, z1), (x1, y0, z1), (x1, y1, z1)],
                        [(0, t0), (0, t1), (x1 - x0, t1), (x1 - x0, t0)]))
        if self.lato:
            t0, t1 = _t_facciata(self.h, dim[self.lato][1])
            for x in (x0, x1):
                out.append((self.lato, [(x, y1, z0), (x, y0, z0), (x, y0, z1), (x, y1, z1)],
                            [(0, t0), (0, t1), (z1 - z0, t1), (z1 - z0, t0)]))
        return out


class Cilindro:
    """Prisma di 8 lati (serbatoi, torri tonde): solo le facce che guardano a sud, più il coperchio."""

    def __init__(self, c, r, lato, h, fronte, tetto, blocca=True):
        self.c, self.r, self.n, self.h, self.fronte, self.tetto, self.blocca = c, r, lato, h, fronte, tetto, blocca

    def caselle(self):
        return [(c, r) for r in range(self.r, self.r + self.n) for c in range(self.c, self.c + self.n)]

    def quads(self, dim):
        cx = self.c * 16 - 256 + 8 * self.n
        cz = self.r * 16 - 256 + 8 * self.n
        R = 8 * self.n - 1
        pts = [(cx + R * math.cos(math.radians(22.5 + 45 * k)), cz + R * math.sin(math.radians(22.5 + 45 * k)))
               for k in range(8)]
        out = []
        tw = dim[self.fronte][0]
        t0, t1 = _t_facciata(self.h, dim[self.fronte][1])
        lato = math.dist(pts[0], pts[1])
        for k in range(8):
            (ax, az), (bx, bz) = pts[k], pts[(k + 1) % 8]
            nz = (az + bz) / 2 - cz
            if nz < -0.3 * R:
                continue
            s0 = (k * lato) % tw
            out.append((self.fronte, [(ax, self.h, az), (ax, 0, az), (bx, 0, bz), (bx, self.h, bz)],
                        [(s0, t0), (s0, t1), (s0 + lato, t1), (s0 + lato, t0)]))
        if self.tetto:
            y = self.h
            for a, b, c, d in ((7, 0, 1, 2), (2, 3, 6, 7), (3, 4, 5, 6)):
                vs = [pts[a], pts[b], pts[c], pts[d]]
                out.append((self.tetto, [(x, y, z) for x, z in vs], [(x + 256, z + 256) for x, z in vs]))
        return out


class Sagoma:
    """Quadrilatero verticale con la texture a colore 0 trasparente (alberi, lampioni, oggetti).
    `n` sagome uguali in fila diventano un solo quadrilatero con la texture ripetuta (filare)."""

    def __init__(self, tex, c, r, n=1, y0=0, blocca=True, larghezza_caselle=None, dz=8):
        self.tex, self.c, self.r, self.n, self.y0, self.blocca, self.dz = tex, c, r, n, y0, blocca, dz
        self.lc = larghezza_caselle

    def largh(self, dim):
        return self.lc or max(1, dim[self.tex][0] // 16)

    def caselle(self, dim=None):
        w = self.lc or 1
        return [(self.c + k, self.r) for k in range(self.n * w)]

    def quads(self, dim):
        tw, th = dim[self.tex]
        w = self.n * tw
        x0 = self.c * 16 - 256 + (16 * (self.lc or 1) - tw) / 2 if self.n == 1 else self.c * 16 - 256
        z = self.r * 16 - 256 + self.dz
        y0, y1 = self.y0, self.y0 + th
        return [(self.tex, [(x0, y1, z), (x0, y0, z), (x0 + w, y0, z), (x0 + w, y1, z)],
                 [(0, 0), (0, th), (w, th), (w, 0)])]


class Pannello:
    """Porta o apertura disegnata davanti a una facciata (mezza unità più a sud, niente z-fighting)."""

    def __init__(self, tex, c, r_fronte, y0=0, blocca=False):
        self.tex, self.c, self.rf, self.y0, self.blocca = tex, c, r_fronte, y0, blocca

    def caselle(self):
        return []

    def quads(self, dim):
        tw, th = dim[self.tex]
        x0 = self.c * 16 - 256
        z = (self.rf + 1) * 16 - 256 + 0.5
        return [(self.tex, [(x0, self.y0 + th, z), (x0, self.y0, z), (x0 + tw, self.y0, z), (x0 + tw, self.y0 + th, z)],
                 [(0, 0), (0, th), (tw, th), (tw, 0)])]


# --------------------------------------------------------------------------- cella


class Cella:
    def __init__(self, chiave, base='erba'):
        self.chiave = chiave
        self.t = [[base] * 32 for _ in range(32)]
        self.occ = [[None] * 32 for _ in range(32)]     # chi occupa la casella (pianificazione)
        self.blk = [[False] * 32 for _ in range(32)]    # bloccata da un oggetto
        self.beh = {}                                   # comportamento al posto di quello del terreno
        self.ogg = []
        self.hg = []                                    # modelli di HeartGold: (indice bm_field, x, y, z)
        self.varchi = []                                # caselle di warp
        self.punti = []                                 # punti per il Modulo 6
        self.porte = []                                 # (c, r) porta -> casella davanti
        self.note = []

    # ---- caselle
    def dentro(self, c, r):
        return 0 <= c < 32 and 0 <= r < 32

    def libera(self, c, r):
        if not self.dentro(c, r) or self.blk[r][c] or self.occ[r][c] is not None:
            return False
        return TERRENI[self.t[r][c]][2] == LIBERO and TERRENI[self.t[r][c]][1] not in (B['MARE'], B['FIUME'])

    def calpestabile(self, c, r):
        if not self.dentro(c, r) or self.blk[r][c]:
            return False
        tex, beh, col = TERRENI[self.t[r][c]]
        beh = self.beh.get((c, r), beh)
        return col == LIBERO and beh not in (B['MARE'], B['FIUME'], B['PORTA'])

    def dipingi(self, c, r, w, h, ter, solo_se=None):
        for rr in range(r, r + h):
            for cc in range(c, c + w):
                if self.dentro(cc, rr) and (solo_se is None or self.t[rr][cc] in solo_se):
                    self.t[rr][cc] = ter

    def riserva(self, c, r, w, h, tag):
        for rr in range(r, r + h):
            for cc in range(c, c + w):
                if self.dentro(cc, rr):
                    self.occ[rr][cc] = tag

    def rect_libero(self, c, r, w, h, margine=0):
        for rr in range(r - margine, r + h + margine):
            for cc in range(c - margine, c + w + margine):
                if not self.dentro(cc, rr):
                    if margine and not (c <= cc < c + w and r <= rr < r + h):
                        continue
                    return False
                nucleo = c <= cc < c + w and r <= rr < r + h
                if nucleo and not self.libera(cc, rr):
                    return False
                if not nucleo and not (self.libera(cc, rr) or (not self.blk[rr][cc] and
                                                              self.occ[rr][cc] in ('strada', 'marciapiede'))):
                    return False
        return True

    def aggiungi(self, o):
        self.ogg.append(o)
        if getattr(o, 'blocca', False):
            for c, r in o.caselle():
                if self.dentro(c, r):
                    self.blk[r][c] = True
                    self.occ[r][c] = self.occ[r][c] or 'oggetto'
        return o

    def punto(self, nome, c, r, nota=''):
        self.punti.append({'nome': nome, 'x': c, 'z': r, 'nota': nota})

    def varco(self, tipo, c, r, verso=None, nota=''):
        self.varchi.append({'tipo': tipo, 'x': c, 'z': r, 'verso': verso, 'nota': nota})

    # ---- uscite: permessi, mesh
    def permessi(self):
        out = bytearray()
        for r in range(32):
            for c in range(32):
                tex, beh, col = TERRENI[self.t[r][c]]
                beh = self.beh.get((c, r), beh)
                if self.blk[r][c]:
                    col = BLOCCATO
                out += bytes((beh, col))
        return bytes(out)

    def quads(self, dim):
        out = []
        grid = [[TERRENI[self.t[r][c]][0] for c in range(32)] for r in range(32)]
        used = [[False] * 32 for _ in range(32)]
        for r in range(32):
            for c in range(32):
                if used[r][c] or grid[r][c] is None:
                    continue
                tex = grid[r][c]
                w = 1
                while c + w < 32 and not used[r][c + w] and grid[r][c + w] == tex:
                    w += 1
                h = 1
                while r + h < 32 and all(not used[r + h][k] and grid[r + h][k] == tex for k in range(c, c + w)):
                    h += 1
                for rr in range(r, r + h):
                    for cc in range(c, c + w):
                        used[rr][cc] = True
                x0, z0 = c * 16 - 256, r * 16 - 256
                x1, z1 = x0 + 16 * w, z0 + 16 * h
                out.append((tex, [(x0, 0, z0), (x0, 0, z1), (x1, 0, z1), (x1, 0, z0)],
                            [(x0 + 256, z0 + 256), (x0 + 256, z1 + 256), (x1 + 256, z1 + 256), (x1 + 256, z0 + 256)]))
        for o in self.ogg:
            out += o.quads(dim)
        return out

    def texture(self, dim):
        return sorted({q[0] for q in self.quads(dim)})

    # ---- raggiungibilità
    def raggiungibili(self, partenze):
        seen = set()
        dq = collections.deque()
        for p in partenze:
            if self.calpestabile(*p):
                seen.add(p)
                dq.append(p)
        while dq:
            c, r = dq.popleft()
            for dc, dr in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                n = (c + dc, r + dr)
                if n not in seen and self.calpestabile(*n):
                    seen.add(n)
                    dq.append(n)
        return seen


# --------------------------------------------------------------------------- percorsi


def percorso(cella, da, a, passabile):
    """Percorso più breve (4 direzioni) da `da` ad `a` sulle caselle per cui passabile(c, r) è vero;
    preferisce andare dritto (meno curve)."""
    if da == a:
        return [da]
    prev = {da: None}
    dq = collections.deque([da])
    while dq:
        cur = dq.popleft()
        if cur == a:
            break
        c, r = cur
        dirs = ((0, 1), (0, -1), (1, 0), (-1, 0))
        p = prev[cur]
        if p is not None:
            d0 = (c - p[0], r - p[1])
            dirs = (d0,) + tuple(d for d in dirs if d != d0)
        for dc, dr in dirs:
            n = (c + dc, r + dr)
            if n in prev or not cella.dentro(*n):
                continue
            if n != a and not passabile(*n):
                continue
            prev[n] = cur
            dq.append(n)
    if a not in prev:
        return None
    out = [a]
    while prev[out[-1]] is not None:
        out.append(prev[out[-1]])
    return out[::-1]
