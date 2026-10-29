"""Blocco 4.4 — dati letti dai registri del progetto per la mappa del Pokégear.

Coordinate: la mappa del Pokégear è la matrice 0 casella per cella (una tile 8×8 per cella), spostata di
due righe in giù: la cella (x, y) della matrice sta alla tile (x, y + 2) (src/application/pokegear/map/
pokegear_map.c: playerY = matrixYCoord + 2). La tabella del Volo usa le coordinate della matrice, quella
dei luoghi (sLocationSpecs) quelle del Pokégear."""
import json
import os
import re

from comune44 import PROJ

DOCS = os.path.join(PROJ, 'docs')
REGISTRI = ['2.1_MAPS_CT_SR_RG', '2.2_MAPS_CL_AG_TP', '2.3_MAPS_ME_PA_EN_ROADS']
W0, H0 = 47, 17
LUOGHI = 100           # PGMAP_NUM_LOCATIONS
VOLI = 27              # PGMAP_NUM_FLYPOINTS
PARTENZA = 'MAP_CT_CATANIA_CORSO_ITALIA'   # casa del protagonista (M-CT-01)
COLONNA_EST = 24       # trama R-09.6: colonna >= 24 = Sicilia orientale (lato Kanto del motore)


def _j(*p):
    return json.load(open(os.path.join(DOCS, *p), encoding='utf-8'))


class Dati:
    def __init__(self):
        self.mappe = {}
        for r in REGISTRI:
            for m in _j('MODULO_2', r + '.json')['mappe']:
                self.mappe[m['simbolo']] = m
        self.celle = {}          # (x, y) -> riga della matrice 0 (4.2/4.3)
        for f in ('4.2_CELLE_EST.json', '4.3_CELLE_OVEST.json'):
            for r in _j('MODULO_4', f)['matrice_0']:
                self.celle[(r['x'], r['y'])] = r
        self.celle_mappa = {}
        for (x, y), r in sorted(self.celle.items()):
            if not r.get('paesaggio'):
                self.celle_mappa.setdefault(r['mappa'], []).append((x, y))
        r25 = _j('MODULO_2', '2.5_TRAINERS_SPRITES_FLY_SEQ.json')
        self.voli = r25['tabella_volo_pokegear']['righe']
        self.vaganti = [v['mappa'] for v in _j('MODULO_3', '3.3_POKEMON_201-300.json')['vaganti']['luoghi']]
        self.isole = {s: m for s, m in self.mappe.items() if m['profilo'] == 'ISOLA'}

    # ------------------------------------------------------------------------------------------
    def terreno(self, x, y):
        """'mare', 'campagna', 'colline', 'bosco', 'etna', 'mappa' oppure None (fuori dalle celle)."""
        r = self.celle.get((x, y))
        if r is None:
            return None
        return r.get('paesaggio') or 'mappa'

    def mappa(self, x, y):
        r = self.celle.get((x, y))
        return None if r is None or r.get('paesaggio') else r['mappa']

    def nome(self, sym):
        return self.mappe[sym]['pokegear']['nome']

    def profilo(self, sym):
        return self.mappe[sym]['profilo']

    def principale(self, sym):
        c = self.mappe[sym]['matrice'].get('cella_principale')
        return tuple(c) if c else None

    def mondo(self, sym):
        h = self.mappe[sym]['intestazione']
        return int(h['worldMapX']), int(h['worldMapY'])

    # ------------------------------------------------------------------------------------------
    def rettangolo(self, sym):
        """Il rettangolo più grande fatto solo di celle della mappa che contiene la cella principale."""
        cs = set(self.celle_mappa[sym])
        px, py = self.principale(sym) or min(cs)
        best = None
        xs = [x for x, _ in cs]
        ys = [y for _, y in cs]
        for x0 in range(min(xs), px + 1):
            for y0 in range(min(ys), py + 1):
                for x1 in range(px, max(xs) + 1):
                    for y1 in range(py, max(ys) + 1):
                        if all((x, y) in cs for x in range(x0, x1 + 1) for y in range(y0, y1 + 1)):
                            a = (x1 - x0 + 1) * (y1 - y0 + 1)
                            if best is None or a > best[0]:
                                best = (a, x0, y0, x1 - x0 + 1, y1 - y0 + 1)
        return best[1:]

    def punteggio(self, sym):
        m = self.mappe[sym]
        trama = ' '.join(m.get('contenuti_trama') or [])
        s = 0.0
        s += 6 * len(set(re.findall(r'M-[A-Z]{2}-\d\d', trama)))
        s += 2 * len(set(re.findall(r'D-[A-Z]{2}-\d\d', trama)))
        s += 1 * len(set(re.findall(r'S-[A-Z]{2}-\d\d', trama)))
        s += {'CITTA': 2, 'PAESE': 1, 'LOCALITA': 1}.get(m['profilo'], 0)
        s += 0.5 * len(self.celle_mappa.get(sym, ()))
        return s

    def scelta_luoghi(self):
        """Le mappe che hanno una voce in sLocationSpecs (R-GFX-31): strade dei vaganti, città col Volo,
        isole, poi le altre mappe della matrice 0 per punteggio fino a 100 voci."""
        volo = [r['mapIDforName'] for r in self.voli]
        obb = []
        for s in self.vaganti + volo + sorted(self.isole) + [PARTENZA]:
            if s not in obb:
                obb.append(s)
        resto = sorted((s for s in self.celle_mappa if s not in obb),
                       key=lambda s: (-self.punteggio(s), s))
        scelte = obb + resto[:LUOGHI - len(obb)]
        escluse = resto[LUOGHI - len(obb):]
        return scelte, escluse
