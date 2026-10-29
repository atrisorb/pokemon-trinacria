"""Blocco 4.4 — piantine delle città nel Pokégear (GFX-PGMAP-PIANTINE: pgmap_gra_00000012.png e
pgmap_gra_00000013.NSCR, unk_174).

Il riquadro in alto a destra dello schermo superiore mostra la piantina della città sotto il cursore:
20 blocchi di 7×7 tile (blocco b in ((b-1) % 4 · 7, (b-1) // 4 · 7) della schermata 32×35), scelti dal campo
tilemapUnk174BlockID della tabella dei luoghi (0 = nessuna piantina). Qui ogni piantina è la cella del Centro
Pokémon della città, rigenerata con gli script dei blocchi 4.2 e 4.3 (stesse schede, stesso seme: è la cella
che c'è nel gioco) e ridotta a 28×28 caselle da 2 pixel: strade e piazze bianche, spazi aperti grigio chiaro, Centro rosso, edifici con
una porta arancioni, acqua azzurra, uscite verdi, il resto a righe grigie come le piantine di HeartGold.
Colori: palette 2 della schermata (indici 32–47 delle palette 14–19, uguali nei 6 temi)."""
import os
import sys

import comune44 as C

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '4.2'))
sys.path.insert(0, os.path.join(HERE, '..', '4.3'))

PAL = 2
K = dict(vuoto=0, strada=2, righe_scure=3, righe_chiare=4, punto=5, scuro=6, rosso_scuro=8, rosso=9,
         blu_scuro=10, blu=11, verde=12, grigio=14, arancio=15)
TILE_MAX = 576
BLOCCHI = 20

# città con la piantina, nell'ordine dei blocchi 1–20: i 9 capoluoghi, poi 11 città col Volo
CITTA = ['MAP_CT_CATANIA_VIA_ETNEA', 'MAP_SR_SIRACUSA', 'MAP_RG_RAGUSA', 'MAP_CL_CALTANISSETTA',
         'MAP_AG_AGRIGENTO', 'MAP_TP_TRAPANI', 'MAP_ME_MESSINA_CENTRO', 'MAP_PA_PALERMO_POLITEAMA',
         'MAP_EN_ENNA_ALTA', 'MAP_CT_ACIREALE', 'MAP_CT_CALTAGIRONE', 'MAP_SR_NOTO', 'MAP_RG_VITTORIA',
         'MAP_ME_TAORMINA', 'MAP_PA_CEFALU', 'MAP_TP_MARSALA', 'MAP_AG_SCIACCA', 'MAP_CL_GELA',
         'MAP_SR_AUGUSTA', 'MAP_ME_MILAZZO']


def _celle_centro():
    """-> {mappa: Cella} per le celle col Centro Pokémon dei blocchi 4.2 e 4.3."""
    import json
    import costruisci42 as K42
    import costruisci43 as K43
    import mondo42
    import mondo43
    piano = json.load(open(os.path.join(C.PROJ, 'docs', 'MODULO_3', '3.1_PIANO_INCONTRI.json'), encoding='utf-8'))
    metodi = {x['mappa']: x['metodi'] for x in piano['mappe']}
    out = {}
    for K_, mondo in ((K42, mondo42), (K43, mondo43)):
        w = mondo.Mondo()
        for sch in K_.schede_esterne(w, metodi):
            if sch.get('pc') and sch['mappa'] in CITTA and sch['mappa'] not in out:
                c = K_.E.esterno(sch)
                c.scheda = sch
                out[sch['mappa']] = c
    return out


def classe(cella, c, r, uscite):
    M = sys.modules[type(cella).__module__]
    if (c, r) in uscite:
        return 'uscita'
    tag = cella.occ[r][c]
    if tag == 'centro':
        return 'centro'
    tex, beh, col = M.TERRENI[cella.t[r][c]]
    beh = cella.beh.get((c, r), beh)
    if beh in (M.B['MARE'], M.B['FIUME']) or tag == 'acqua':
        return 'acqua'
    if tag in ('strada', 'marciapiede'):
        return 'strada'
    if tag == 'edificio':
        return 'edificio'
    if cella.calpestabile(c, r):
        return 'libero'
    return 'chiuso'


def disegna(cella):
    """-> 56×56 pixel (indici 0–15 della palette 2)."""
    uscite = set()
    for (c, r) in getattr(cella, 'bocche', []):
        uscite.add((c, r))
    W = 56
    pix = [0] * (W * W)
    cls = [[classe(cella, c, r, uscite) for c in range(32)] for r in range(32)]
    for r in range(2, 30):
        for c in range(2, 30):
            k = cls[r][c]
            for dy in range(2):
                for dx in range(2):
                    y, x = (r - 2) * 2 + dy, (c - 2) * 2 + dx
                    if k == 'strada':
                        v = K['strada']
                    elif k == 'libero':
                        v = K['righe_chiare']
                    elif k == 'centro':
                        v = K['rosso']
                    elif k == 'edificio':
                        v = K['arancio']
                    elif k == 'acqua':
                        v = K['blu']
                    elif k == 'uscita':
                        v = K['verde']
                    else:
                        v = K['righe_scure'] if y % 2 == 0 else K['righe_chiare']
                    pix[y * W + x] = v
    # contorni scuri attorno a Centro ed edifici (un pixel dentro la sagoma)
    out = list(pix)
    for y in range(W):
        for x in range(W):
            v = pix[y * W + x]
            if v in (K['rosso'], K['arancio']):
                bordo = any(not (0 <= x + dx < W and 0 <= y + dy < W) or pix[(y + dy) * W + x + dx] != v
                            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
                if bordo:
                    out[y * W + x] = K['rosso_scuro'] if v == K['rosso'] else K['scuro']
    # cornice esterna del riquadro
    for k in range(W):
        for p in ((k, 0), (k, W - 1), (0, k), (W - 1, k)):
            out[p[1] * W + p[0]] = K['scuro']
    return out


def costruisci():
    celle = _celle_centro()
    mancanti = [m for m in CITTA if m not in celle]
    if mancanti:
        raise C.Errore('piantine: nessuna cella col Centro per %s' % ', '.join(mancanti))
    fog = C.Foglio(TILE_MAX, flip=True, prime=[[[0] * 8 for _ in range(8)]])
    W, H = 32, 35
    scr = [C.voce(0, PAL)] * (W * H)
    immagini = {}
    for b, sym in enumerate(CITTA):
        pix = disegna(celle[sym])
        immagini[sym] = pix
        bx, by = (b % 4) * 7, (b // 4) * 7
        for ty in range(7):
            for tx in range(7):
                t = [[pix[(ty * 8 + y) * 56 + tx * 8 + x] for x in range(8)] for y in range(8)]
                scr[(by + ty) * W + bx + tx] = fog.aggiungi(t, PAL)
    blocchi = {sym: b + 1 for b, sym in enumerate(CITTA)}
    return dict(foglio=fog, schermata=scr, blocchi=blocchi, immagini=immagini,
                celle={s: celle[s].chiave for s in CITTA})


if __name__ == '__main__':
    r = costruisci()
    print('tile', len(r['foglio'].tile))
