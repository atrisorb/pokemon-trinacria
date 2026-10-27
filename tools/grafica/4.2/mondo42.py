"""Il mondo dei registri 2.1–2.3 visto dal blocco 4.2: celle della matrice 0, lati, mare, zona del blocco.

Tutto si ricava dai registri; l'unica cosa scritta a mano qui è il tipo di paesaggio delle celle
senza mappa («#» dei registri e «.» interne), in PAESAGGIO.
"""
import collections
import glob
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
DOCS = os.path.join(PROJ, 'docs')

W, H = 47, 17
PROVINCE_4_2 = ('CT', 'SR', 'RG', 'CL')

# Celle senza mappa vicine alle mappe del 4.2: tipo di paesaggio. «mare» per il Golfo di Catania, la
# costa ionica, la costa iblea e il Golfo di Gela; i rilievi secondo la geografia (versanti dell'Etna,
# Piana di Catania, Iblei). Le celle «.» non scritte qui sono mare se toccano il bordo della matrice
# attraverso altre celle «.», campagna se sono buchi interni.
PAESAGGIO = {}
for _c in ((35, 1), (36, 1), (37, 1), (35, 2), (36, 2), (35, 3), (36, 3), (38, 2), (39, 2), (40, 2),
           (38, 3), (39, 3), (40, 3), (39, 4), (40, 4)):
    PAESAGGIO[_c] = 'etna'
for _c in ((35, 4), (36, 4), (33, 8), (34, 8), (35, 8), (36, 8), (37, 8), (33, 9), (34, 9), (35, 9),
           (33, 10), (34, 10), (35, 10), (36, 10), (36, 14), (37, 14)):
    PAESAGGIO[_c] = 'campagna'
for _c in ((33, 11), (34, 11), (35, 11), (36, 11), (37, 11), (36, 12), (37, 12), (38, 12)):
    PAESAGGIO[_c] = 'colline'
for _c in ((42, 3), (39, 6), (40, 6), (41, 6), (39, 7), (40, 7), (41, 7), (39, 8), (40, 9), (40, 10),
           (40, 12), (40, 13), (40, 14), (40, 15), (31, 15), (32, 15), (33, 15), (34, 15), (35, 15),
           (36, 15), (37, 15), (37, 16), (38, 16)):
    PAESAGGIO[_c] = 'mare'


def carica():
    regs = {}
    mappe = []
    for f in sorted(glob.glob(os.path.join(DOCS, 'MODULO_2', '2.[123]_*.json'))):
        d = json.load(open(f, encoding='utf-8'))
        regs[os.path.basename(f)[:3]] = d
        mappe += d['mappe']
    return regs, mappe


class Mondo:
    def __init__(self):
        self.regs, self.mappe = carica()
        self.per_simbolo = {m['simbolo']: m for m in self.mappe}
        self.cella = {}
        for m in self.mappe:
            if 'EVERYWHERE' in m['matrice']['simbolo']:
                for c in m['matrice']['celle']:
                    self.cella[tuple(c)] = m
        self.paesaggio_hash = set()
        for d in self.regs.values():
            pg = d.get('piano_globale') or {}
            for c in pg.get('celle_paesaggio', []):
                self.paesaggio_hash.add(tuple(c))
        self._mare = self._mare_aperto()
        # confini percorribili in entrambe le direzioni
        self.passi = set()
        for m in self.mappe:
            for cf in m.get('confini_percorribili', []):
                a, b = tuple(cf['da_cella']), tuple(cf['a_cella'])
                self.passi.add((a, b))
                self.passi.add((b, a))
        # strade del blocco: quelle riservate dal 2.1 e quelle tutte dentro le celle di Caltanissetta
        g = self.regs['2.1']['piano_globale']
        riservate = {s['simbolo'] for s in g['strade_riservate']}
        cl = {tuple(c) for c in g['celle_riservate_altri_blocchi']['CL']}
        self.strade = sorted(m['simbolo'] for m in self.mappe if m['provincia'] == 'ROADS' and (
            m['simbolo'] in riservate or all(tuple(c) in cl for c in m['matrice']['celle'])))
        # Centri con punto di volo: cella dell'atterraggio dalla tabella degli spawn (R-MAP-14)
        self.volo = {}
        for d in self.regs.values():
            for r in d['tabella_spawn']['righe']:
                if r.get('isFlyPoint'):
                    self.volo[r['flyPointMapNo']] = (r['flyPointX'] // 32, r['flyPointY'] // 32,
                                                    r['flyPointX'] % 32, r['flyPointY'] % 32)

    def _mare_aperto(self):
        seen = set()
        dq = collections.deque()
        for x in range(W):
            for y in range(H):
                if (x in (0, W - 1) or y in (0, H - 1)) and self.vuota(x, y):
                    seen.add((x, y))
                    dq.append((x, y))
        while dq:
            x, y = dq.popleft()
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                n = (x + dx, y + dy)
                if 0 <= n[0] < W and 0 <= n[1] < H and n not in seen and self.vuota(*n):
                    seen.add(n)
                    dq.append(n)
        return seen

    def vuota(self, x, y):
        return (x, y) not in self.cella and (x, y) not in self.paesaggio_hash

    def tipo_paesaggio(self, x, y):
        """Per una cella senza mappa: mare, etna, campagna, colline (None se ha una mappa)."""
        if (x, y) in self.cella:
            return None
        if (x, y) in PAESAGGIO:
            return PAESAGGIO[(x, y)]
        if (x, y) in self.paesaggio_hash:
            return 'campagna'
        return 'mare' if (x, y) in self._mare else 'campagna'

    def del_blocco(self, m):
        return m['provincia'] in PROVINCE_4_2 or m['simbolo'] in self.strade

    def celle_blocco(self):
        return sorted(((c, m) for c, m in self.cella.items() if self.del_blocco(m)), key=lambda x: (x[0][1], x[0][0]))

    def lati(self, x, y):
        m = self.cella[(x, y)]
        out = {}
        for lato, (dx, dy) in (('N', (0, -1)), ('S', (0, 1)), ('O', (-1, 0)), ('E', (1, 0))):
            n = (x + dx, y + dy)
            nm = self.cella.get(n)
            if nm is m:
                out[lato] = ('interno', m['simbolo'])
            elif nm is not None and ((x, y), n) in self.passi:
                out[lato] = ('aperto', nm['simbolo'])
            elif nm is None and self.tipo_paesaggio(*n) == 'mare':
                out[lato] = ('mare', None)
            else:
                out[lato] = ('chiuso', nm['simbolo'] if nm else self.tipo_paesaggio(*n))
        return out

    def diag_mare(self, x, y):
        out = []
        for k, (dx, dy) in (('NO', (-1, -1)), ('NE', (1, -1)), ('SO', (-1, 1)), ('SE', (1, 1))):
            if (x + dx, y + dy) not in self.cella and self.tipo_paesaggio(x + dx, y + dy) == 'mare':
                out.append(k)
        return out

    def paesaggio_blocco(self):
        """Celle senza mappa che toccano (anche di spigolo) una cella del blocco, e le «#» a due celle:
        ricevono un modello di paesaggio condiviso (R-GFX-20)."""
        mie = {c for c, _ in self.celle_blocco()}
        out = {}
        for x, y in mie:
            for dx in (-2, -1, 0, 1, 2):
                for dy in (-2, -1, 0, 1, 2):
                    n = (x + dx, y + dy)
                    vicina = abs(dx) <= 1 and abs(dy) <= 1
                    # le «#» dei registri anche a due celle (niente buchi fra i rilievi), le «.» solo accanto
                    if 0 <= n[0] < W and 0 <= n[1] < H and n not in self.cella and                             (vicina or n in self.paesaggio_hash or n in PAESAGGIO):
                        out[n] = self.tipo_paesaggio(*n)
        return dict(sorted(out.items(), key=lambda kv: (kv[0][1], kv[0][0])))

    def interni_blocco(self):
        return [m for m in self.mappe if m['provincia'] in PROVINCE_4_2 and m['tipo'] == 'interno']

    def matrici_nuove(self):
        out = {}
        for d in self.regs.values():
            for mt in d.get('matrici_nuove', []):
                out[mt['simbolo']] = mt
        return out
