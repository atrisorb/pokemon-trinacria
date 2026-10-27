"""Il mondo dei registri 2.1–2.3 visto dal blocco 4.3: celle della matrice 0, lati, mare, zona del blocco.

Tutto si ricava dai registri e dal JSON del 4.2 (celle e paesaggio già messi nella matrice 0, che il
4.3 non ridisegna); l'unica cosa scritta a mano qui è il tipo di paesaggio delle celle senza mappa
vicine alle mappe dell'ovest, in PAESAGGIO.
"""
import collections
import glob
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
DOCS = os.path.join(PROJ, 'docs')

W, H = 47, 17
PROVINCE_4_3 = ('AG', 'TP', 'PA', 'EN', 'ME')

# Matrice 0 del blocco 4.2 (celle delle mappe e paesaggio): il 4.3 non le tocca e ne rispetta i tipi.
_M42 = json.load(open(os.path.join(DOCS, 'MODULO_4', '4.2_CELLE_EST.json'), encoding='utf-8'))
CELLE_4_2 = {(c['x'], c['y']) for c in _M42['matrice_0']}
PAESAGGIO_4_2 = {(c['x'], c['y']): c['paesaggio'] for c in _M42['matrice_0'] if c.get('paesaggio')}
VOCI_PAESAGGIO_4_2 = {c['paesaggio']: c['voce'] for c in _M42['matrice_0'] if c.get('paesaggio')}
MAPPE_4_2 = {c['mappa'] for c in _M42['matrice_0'] if not c.get('paesaggio')}

# Celle senza mappa vicine alle mappe del 4.3: tipo di paesaggio. Le «.» che toccano il bordo sono
# mare (Tirreno, Canale di Sicilia, Mare Africano); qui si correggono quelle che nella realtà sono
# monti: i Nebrodi fra la costa tirrenica messinese e Sperlinga/Nicosia («bosco»), i Sicani fra
# Corleone e l'Agrigentino («colline»). Le coordinate fuori dalla matrice valgono solo per i lati:
# a nord della costa tirrenica messinese e a est dello Stretto c'è il mare, non la campagna.
PAESAGGIO = {}
for _c in ((25, 1), (25, 2), (26, 2), (27, 2), (28, 2), (29, 2), (30, 2)):
    PAESAGGIO[_c] = 'bosco'
for _c in ((14, 7), (15, 7), (16, 7), (17, 7), (18, 7), (15, 8), (16, 8), (17, 8), (18, 8)):
    PAESAGGIO[_c] = 'colline'
for _x in range(25, W + 1):
    PAESAGGIO[(_x, -1)] = 'mare'
for _y in range(-1, 4):
    PAESAGGIO[(W, _y)] = 'mare'


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
        # strade del blocco: tutte quelle che il 4.2 non ha disegnato
        self.strade = sorted(m['simbolo'] for m in self.mappe if m['provincia'] == 'ROADS' and
                             'EVERYWHERE' in m['matrice']['simbolo'] and m['simbolo'] not in MAPPE_4_2)
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
        """Per una cella senza mappa: mare, etna, campagna, colline, bosco (None se ha una mappa)."""
        if (x, y) in self.cella:
            return None
        if (x, y) in PAESAGGIO_4_2:
            return PAESAGGIO_4_2[(x, y)]
        if (x, y) in PAESAGGIO:
            return PAESAGGIO[(x, y)]
        if (x, y) in self.paesaggio_hash:
            return 'campagna'
        return 'mare' if (x, y) in self._mare else 'campagna'

    def del_blocco(self, m):
        return m['provincia'] in PROVINCE_4_3 or m['simbolo'] in self.strade

    def celle_blocco(self):
        return sorted(((c, m) for c, m in self.cella.items() if self.del_blocco(m) and c not in CELLE_4_2),
                      key=lambda x: (x[0][1], x[0][0]))

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
        ricevono un modello di paesaggio condiviso (R-GFX-20). Quelle già messe dal 4.2 restano sue."""
        mie = {c for c, _ in self.celle_blocco()}
        out = {}
        for x, y in mie:
            for dx in (-2, -1, 0, 1, 2):
                for dy in (-2, -1, 0, 1, 2):
                    n = (x + dx, y + dy)
                    vicina = abs(dx) <= 1 and abs(dy) <= 1
                    # le «#» dei registri anche a due celle (niente buchi fra i rilievi), le «.» solo accanto
                    if 0 <= n[0] < W and 0 <= n[1] < H and n not in self.cella and n not in CELLE_4_2 and (
                            vicina or n in self.paesaggio_hash or n in PAESAGGIO):
                        out[n] = self.tipo_paesaggio(*n)
        return dict(sorted(out.items(), key=lambda kv: (kv[0][1], kv[0][0])))

    def interni_blocco(self):
        return [m for m in self.mappe if m['provincia'] in PROVINCE_4_3 and m['tipo'] == 'interno']

    def matrici_nuove(self):
        out = {}
        for d in self.regs.values():
            for mt in d.get('matrici_nuove', []):
                out[mt['simbolo']] = mt
        return out
