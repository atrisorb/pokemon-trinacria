"""Esterni del blocco 4.3 (copia di esterni42.py, R-GFX-17): dalla scheda di una cella della matrice 0
alla cella del motore. Aggiunte del 4.3: temi dell'ovest, templi dorici, saline e mulini, condotte,
caselli, pilone dello Stretto, chiese con le cupole rosse, rupi, piloni interrotti, labirinto del Cretto.

La scheda (schede43.py) dice il tema, i lati (dai registri 2.1–2.3), gli ingressi verso gli interni,
i monumenti e i punti della trama. Qui si decide tutto il resto in modo deterministico: il seme
di ogni scelta è il nome della cella.
"""
import motore43 as M
from motore43 import B, Volume, Cilindro, Sagoma, Pannello, ErroreCella
import tex42
import tex43  # noqa: F401  (registra le texture nuove del 4.3)

# --------------------------------------------------------------------------- temi

TEMI = {
    'citta_ct': dict(base='marciapiede', strada='basolato', piazza='basolato', vicolo='basolato',
                     bordo='palazzi', riempi='palazzi', facciate=('fac_lavica', 'fac_barocca', 'fac_intonaco', 'fac_negozio'),
                     tetti=('tetto_piano', 'tetto_piano', 'tetto_coppi'), altezze=(48, 64, 64, 96),
                     props=('lampione', 'cassonetto', 'motorino', 'lampione'), alberi=('palma', 'albero'),
                     riva='sabbia_nera', verde='erba', muro='muro_lavico'),
    'periferia': dict(base='terra', strada='asfalto', piazza='asfalto', vicolo='terra', bordo='palazzi',
                      riempi='palazzi', facciate=('fac_cemento', 'fac_cemento', 'fac_intonaco'),
                      tetti=('tetto_cemento', 'tetto_piano'), altezze=(64, 96, 128),
                      props=('lampione', 'cass_brucia', 'sacchi', 'cassonetto', 'auto'), alberi=('albero', 'cespuglio'),
                      riva='sabbia', verde='erba', muro='muro_lavico'),
    'paese_etna': dict(base='terra', strada='basolato', piazza='basolato', vicolo='basolato', bordo='muro',
                       riempi='case', facciate=('fac_lavica', 'fac_intonaco', 'fac_intonaco'),
                       tetti=('tetto_coppi', 'tetto_piano'), altezze=(32, 48, 48, 64),
                       props=('lampione', 'motorino'), alberi=('albero', 'pino', 'cespuglio'),
                       riva='sabbia_nera', verde='erba', muro='muro_lavico'),
    'etna': dict(base='sciara', strada='cenere', piazza='cenere', vicolo='cenere', bordo='roccia', riempi='sciara',
                 facciate=('fac_lavica',), tetti=('tetto_coppi',), altezze=(32, 48), props=('cartello',),
                 alberi=('pino', 'pino', 'cespuglio'), riva='sabbia_nera', verde='cenere', muro='muro_lavico',
                 roccia='roccia_nera'),
    'costa_lavica': dict(base='basolato', strada='basolato', piazza='basolato', vicolo='basolato', bordo='muro',
                         riempi='case', facciate=('fac_intonaco', 'fac_lavica', 'fac_barocca'),
                         tetti=('tetto_piano', 'tetto_coppi'), altezze=(32, 48, 48),
                         props=('lampione', 'barca', 'motorino'), alberi=('palma', 'albero'),
                         riva='sabbia_nera', verde='erba', muro='muro_lavico', scogli=True),
    'barocco': dict(base='lastricato', strada='lastricato', piazza='lastricato', vicolo='lastricato', bordo='palazzi',
                    riempi='palazzi', facciate=('fac_barocca', 'fac_barocca', 'fac_intonaco', 'fac_negozio'),
                    tetti=('tetto_coppi', 'tetto_piano'), altezze=(48, 64, 64),
                    props=('lampione', 'tavolino', 'motorino'), alberi=('palma', 'albero'),
                    riva='scoglio', verde='erba', muro='muro_calcare'),
    'paese': dict(base='terra', strada='asfalto', piazza='lastricato', vicolo='lastricato', bordo='muro',
                  riempi='case', facciate=('fac_intonaco', 'fac_intonaco', 'fac_barocca', 'fac_negozio'),
                  tetti=('tetto_piano', 'tetto_coppi'), altezze=(32, 48, 48, 64),
                  props=('lampione', 'motorino', 'cassonetto'), alberi=('albero', 'fico_india', 'palma'),
                  riva='sabbia', verde='erba', muro='muro_calcare'),
    'spiaggia': dict(base='sabbia', strada='asfalto', piazza='lastricato', vicolo='lastricato', bordo='alberi',
                     riempi='case', facciate=('fac_intonaco',), tetti=('tetto_piano',), altezze=(32, 48),
                     props=('ombrellone', 'lampione', 'ombrellone'), alberi=('palma', 'cespuglio'),
                     riva='sabbia', verde='erba', muro='muro_calcare'),
    'industria': dict(base='ghiaia', strada='asfalto', piazza='asfalto', vicolo='ghiaia', bordo='recinzione',
                      riempi='industria', facciate=('lamiera', 'fac_cemento'), tetti=('lamiera', 'tetto_cemento'),
                      altezze=(48, 64), props=('traliccio', 'lampione', 'cartello'), alberi=('cespuglio',),
                      riva='scoglio', verde='erba', muro='muro_calcare'),
    'campagna': dict(base='erba', strada='asfalto', piazza='terra', vicolo='terra', bordo='alberi', riempi='campi',
                     facciate=('fac_intonaco',), tetti=('tetto_coppi',), altezze=(32,), props=('cartello',),
                     alberi=('albero', 'albero', 'fico_india', 'cespuglio'), riva='sabbia', verde='erba',
                     muro='muro_calcare'),
    'nisseno': dict(base='terra', strada='asfalto', piazza='lastricato', vicolo='lastricato', bordo='muro',
                    riempi='case', facciate=('fac_intonaco', 'fac_intonaco', 'fac_barocca', 'fac_negozio'),
                    tetti=('tetto_coppi', 'tetto_piano'), altezze=(32, 48, 48, 64),
                    props=('lampione', 'motorino'), alberi=('albero', 'fico_india', 'cespuglio'),
                    riva='sabbia', verde='argilla', muro='muro_calcare'),
    'calanchi': dict(base='argilla', strada='asfalto', piazza='terra', vicolo='terra', bordo='roccia',
                     riempi='calanchi', facciate=('fac_intonaco',), tetti=('tetto_coppi',), altezze=(32,),
                     props=('cartello',), alberi=('cespuglio', 'fico_india'), riva='sabbia', verde='argilla',
                     muro='muro_calcare', roccia='roccia'),
    'bosco': dict(base='erba', strada='terra', piazza='terra', vicolo='terra', bordo='alberi', riempi='bosco',
                  facciate=('fac_intonaco',), tetti=('tetto_coppi',), altezze=(32,), props=('cartello',),
                  alberi=('albero', 'albero', 'pino', 'cespuglio'), riva='sabbia', verde='erba',
                  muro='muro_calcare'),
}
# ---- temi del 4.3
TEMI.update({
    'palermo': dict(base='marciapiede', strada='basolato', piazza='basolato', vicolo='basolato', bordo='palazzi',
                    riempi='palazzi', facciate=('fac_liberty', 'fac_barocca', 'fac_intonaco', 'fac_negozio', 'fac_normanna'),
                    tetti=('tetto_piano', 'tetto_piano', 'tetto_coppi'), altezze=(48, 64, 64, 96),
                    props=('lampione', 'motorino', 'cassonetto', 'lampione', 'sacchi'), alberi=('palma', 'albero'),
                    riva='scoglio', verde='erba', muro='muro_calcare'),
    'messina': dict(base='marciapiede', strada='asfalto', piazza='lastricato', vicolo='lastricato', bordo='palazzi',
                    riempi='palazzi', facciate=('fac_liberty', 'fac_intonaco', 'fac_cemento', 'fac_negozio'),
                    tetti=('tetto_piano', 'tetto_cemento'), altezze=(48, 64, 80),
                    props=('lampione', 'motorino', 'cassonetto'), alberi=('palma', 'albero'),
                    riva='sabbia', verde='erba', muro='muro_calcare'),
    'tufo': dict(base='lastricato', strada='lastricato', piazza='lastricato', vicolo='lastricato', bordo='palazzi',
                 riempi='palazzi', facciate=('fac_tufo', 'fac_tufo', 'fac_intonaco', 'fac_barocca', 'fac_negozio'),
                 tetti=('tetto_piano', 'tetto_coppi'), altezze=(32, 48, 48, 64),
                 props=('lampione', 'motorino', 'barca'), alberi=('palma', 'albero'),
                 riva='scoglio', verde='erba', muro='tufo'),
    'paese_tufo': dict(base='terra', strada='asfalto', piazza='lastricato', vicolo='lastricato', bordo='muro',
                       riempi='case', facciate=('fac_tufo', 'fac_intonaco', 'fac_tufo'), tetti=('tetto_piano', 'tetto_coppi'),
                       altezze=(32, 48, 48), props=('lampione', 'motorino'), alberi=('palma', 'fico_india', 'albero'),
                       riva='sabbia', verde='erba', muro='tufo'),
    'montagna': dict(base='erba', strada='terra', piazza='terra', vicolo='terra', bordo='alberi', riempi='bosco',
                     facciate=('muro_calcare',), tetti=('tetto_coppi',), altezze=(32,), props=('cartello',),
                     alberi=('faggio', 'faggio', 'pino', 'cespuglio'), riva='sabbia', verde='erba', muro='muro_calcare'),
    'paese_monti': dict(base='terra', strada='lastricato', piazza='lastricato', vicolo='lastricato', bordo='muro',
                        riempi='case', facciate=('fac_intonaco', 'muro_calcare', 'fac_barocca', 'fac_intonaco'),
                        tetti=('tetto_coppi', 'tetto_coppi', 'tetto_piano'), altezze=(32, 48, 48, 64),
                        props=('lampione', 'motorino'), alberi=('albero', 'faggio', 'cespuglio'),
                        riva='sabbia', verde='erba', muro='muro_calcare'),
    'templi': dict(base='terra', strada='terra', piazza='lastricato', vicolo='terra', bordo='alberi', riempi='campi',
                   facciate=('tufo',), tetti=('tufo',), altezze=(32,), props=('cartello',),
                   alberi=('mandorlo', 'mandorlo', 'albero', 'fico_india'), riva='sabbia', verde='erba', muro='tufo'),
    'vigne': dict(base='terra', strada='asfalto', piazza='terra', vicolo='terra', bordo='alberi', riempi='campi',
                  facciate=('fac_tufo', 'fac_intonaco'), tetti=('tetto_coppi',), altezze=(32,), props=('cartello',),
                  alberi=('vite', 'albero', 'fico_india'), riva='sabbia', verde='erba', muro='muro_calcare'),
    'saline': dict(base='terra', strada='terra', piazza='terra', vicolo='terra', bordo='muro', riempi='campi',
                   facciate=('fac_tufo',), tetti=('tetto_coppi',), altezze=(32,), props=('mucchio_sale', 'cartello'),
                   alberi=('palma_nana', 'cespuglio'), riva='sabbia', verde='terra', muro='tufo'),
    'macchia': dict(base='terra', strada='terra', piazza='terra', vicolo='terra', bordo='roccia', riempi='bosco',
                    facciate=('fac_tufo',), tetti=('tetto_coppi',), altezze=(32,), props=('cartello',),
                    alberi=('palma_nana', 'palma_nana', 'cespuglio', 'fico_india'), riva='scoglio', verde='erba',
                    muro='muro_calcare', roccia='roccia'),
    'memoria': dict(base='erba', strada='lastricato', piazza='lastricato', vicolo='lastricato', bordo='alberi',
                    riempi='campi', facciate=('fac_intonaco',), tetti=('tetto_coppi',), altezze=(32,), props=(),
                    alberi=('cipresso', 'albero', 'cipresso'), riva='sabbia', verde='erba', muro='muro_calcare'),
    'cava': dict(base='tufo', strada='terra', piazza='tufo', vicolo='terra', bordo='roccia', riempi='calanchi',
                 facciate=('tufo',), tetti=('tufo',), altezze=(32,), props=('cartello',),
                 alberi=('palma_nana', 'cespuglio', 'fico_india'), riva='scoglio', verde='terra', muro='tufo',
                 roccia='tufo'),
    'cretto': dict(base='cretto', strada='cretto', piazza='cretto', vicolo='cretto', bordo='roccia', riempi='cretto',
                   facciate=('cretto',), tetti=('cretto',), altezze=(24,), props=(), alberi=('cespuglio',),
                   riva='sabbia', verde='cretto', muro='cretto', roccia='cretto'),
    'vulcano': dict(base='sciara', strada='cenere', piazza='cenere', vicolo='cenere', bordo='roccia', riempi='sciara',
                    facciate=('fac_intonaco',), tetti=('tetto_piano',), altezze=(32,), props=('cartello',),
                    alberi=('fico_india', 'cespuglio', 'palma_nana'), riva='sabbia_nera', verde='cenere',
                    muro='muro_lavico', roccia='roccia_nera'),
    'eolie': dict(base='terra', strada='lastricato', piazza='lastricato', vicolo='lastricato', bordo='muro',
                  riempi='case', facciate=('fac_intonaco', 'fac_intonaco', 'fac_tufo'), tetti=('tetto_piano',),
                  altezze=(32, 48), props=('lampione', 'barca', 'motorino'), alberi=('palma', 'fico_india', 'cespuglio'),
                  riva='sabbia_nera', verde='erba', muro='muro_lavico', scogli=True),
    'rocca': dict(base='terra', strada='lastricato', piazza='lastricato', vicolo='terra', bordo='roccia',
                  riempi='calanchi', facciate=('muro_calcare',), tetti=('tetto_coppi',), altezze=(32,), props=(),
                  alberi=('cespuglio', 'cipresso'), riva='sabbia', verde='erba', muro='muro_calcare', roccia='roccia'),
    'villa_mostri': dict(base='erba', strada='lastricato', piazza='lastricato', vicolo='lastricato', bordo='muro',
                         riempi='campi', facciate=('fac_barocca',), tetti=('tetto_coppi',), altezze=(48,),
                         props=('statua',), alberi=('albero', 'palma', 'cipresso'), riva='sabbia', verde='erba',
                         muro='muro_calcare'),
    'autodromo': dict(base='erba', strada='cordolo', piazza='asfalto', vicolo='terra', bordo='alberi', riempi='campi',
                      facciate=('fac_cemento',), tetti=('tetto_cemento',), altezze=(32,), props=('guardrail', 'cartello'),
                      alberi=('pino', 'albero', 'cespuglio'), riva='sabbia', verde='erba', muro='muro_calcare'),
})
TEMI['strada'] = dict(TEMI['campagna'], riempi='campi', bordo='alberi')
TEMI['strada_etna'] = dict(TEMI['etna'], strada='asfalto', riempi='sciara')
TEMI['strada_costa'] = dict(TEMI['campagna'], riva='scoglio')
TEMI['strada_calanchi'] = dict(TEMI['calanchi'])
TEMI['autostrada'] = dict(TEMI['campagna'], props=('guardrail', 'guardrail', 'cartello'), passo_props=5)
TEMI['autostrada_costa'] = dict(TEMI['autostrada'], riva='scoglio')
TEMI['strada_monti'] = dict(TEMI['montagna'], strada='asfalto', riempi='bosco')
TEMI['strada_vigne'] = dict(TEMI['vigne'])
TEMI['strada_citta'] = dict(TEMI['periferia'], props=('auto', 'lampione', 'auto', 'cassonetto'))
ALBERI_LARGHI = ('albero', 'pino', 'faggio', 'mandorlo')
CITTADINI = {'citta_ct', 'periferia', 'barocco', 'palermo', 'messina', 'tufo'}


# --------------------------------------------------------------------------- utilità


def scegli(cella, seq):
    return seq[cella.rng.u32() % len(seq)]


def zona_ordine(zona):
    """Ordine dei centri in cui provare a mettere qualcosa (zona = nord, sud, ovest, est,
    nordovest, …, centro): righe e colonne preferite."""
    cc = {'ovest': 7, 'est': 23, 'nordovest': 7, 'sudovest': 7, 'nordest': 23, 'sudest': 23}.get(zona, 15)
    rr = {'nord': 7, 'sud': 23, 'nordovest': 7, 'nordest': 7, 'sudovest': 23, 'sudest': 23}.get(zona, 15)
    return cc, rr


def posizioni(cella, w, d, zona, margine=1):
    cc, rr = zona_ordine(zona)
    cand = [(c, r) for r in range(0, 32 - d + 1) for c in range(0, 32 - w + 1)]
    cand.sort(key=lambda p: (abs(p[0] + w / 2 - cc) + abs(p[1] + d / 2 - rr), p[1], p[0]))
    for c, r in cand:
        if cella.rect_libero(c, r, w, d, margine):
            yield c, r


# --------------------------------------------------------------------------- lati


def dipingi_mare(cella, lati, diag, tema):
    mare = set()
    P = M.MARE_PROF
    for lato, (tipo, _) in lati.items():
        if tipo != 'mare':
            continue
        if lato == 'N':
            rect = (0, 0, 32, P)
        elif lato == 'S':
            rect = (0, 32 - P, 32, P)
        elif lato == 'O':
            rect = (0, 0, P, 32)
        else:
            rect = (32 - P, 0, P, 32)
        c0, r0, w, h = rect
        mare |= {(c, r) for r in range(r0, r0 + h) for c in range(c0, c0 + w)}
    for k in diag:
        c0 = 0 if 'O' in k else 32 - P
        r0 = 0 if 'N' in k else 32 - P
        mare |= {(c, r) for r in range(r0, r0 + P) for c in range(c0, c0 + P)}
    for c, r in mare:
        cella.t[r][c] = 'mare'
        cella.occ[r][c] = 'mare'
    # acqua bassa lungo la riva e riva di sabbia o scogli
    for c, r in list(mare):
        if any((c + dc, r + dr) not in mare and cella.dentro(c + dc, r + dr)
               for dc, dr in ((1, 0), (-1, 0), (0, 1), (0, -1))):
            cella.t[r][c] = 'mare_basso'
    riva = tema['riva']
    riva_ter = {'scoglio': 'sabbia_nera' if tema.get('scogli') else 'sabbia'}.get(riva, riva)
    for _ in range(M.RIVA):
        nuove = []
        for r in range(32):
            for c in range(32):
                if (c, r) in mare or cella.occ[r][c] == 'riva':
                    continue
                if any(cella.dentro(c + dc, r + dr) and ((c + dc, r + dr) in mare or cella.occ[r + dr][c + dc] == 'riva')
                       for dc, dr in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                    nuove.append((c, r))
        for c, r in nuove:
            cella.t[r][c] = riva_ter
            cella.occ[r][c] = 'riva'
    # scogli sparsi sulla riva (bloccati), mai nei varchi
    if riva == 'scoglio' or tema.get('scogli'):
        for r in range(32):
            for c in range(32):
                if cella.occ[r][c] == 'riva' and c not in M.VARCO and r not in M.VARCO and cella.rng.p(0.18):
                    cella.t[r][c] = 'scoglio'
    for r in range(32):
        for c in range(32):
            if cella.occ[r][c] == 'riva':
                cella.occ[r][c] = None
    return mare


def striscia(lato, k=None, prof=M.STRISCIA):
    """Caselle della striscia lungo un lato (k = indice lungo il lato o tutte)."""
    out = []
    for i in (range(32) if k is None else [k]):
        for j in range(prof):
            if lato == 'N':
                out.append((i, j))
            elif lato == 'S':
                out.append((i, 31 - j))
            elif lato == 'O':
                out.append((j, i))
            else:
                out.append((31 - j, i))
    return out


def bocca(lato):
    """Casella del bordo al centro del varco e direzione verso l'interno."""
    return {'N': ((15, 0), (0, 1)), 'S': ((15, 31), (0, -1)), 'O': ((0, 15), (1, 0)), 'E': ((31, 15), (-1, 0))}[lato]


def ostacoli_bordo(cella, lati, tema, sch):
    """Confini chiusi e aperti: ostacolo di 2 caselle, con il varco 13–18 dove si passa (R-GFX-19)."""
    stile = sch.get('bordo', tema['bordo'])
    for lato, (tipo, _) in lati.items():
        if tipo == 'mare':
            continue
        aperto = tipo in ('aperto', 'interno')
        largo = range(8, 24) if tipo == 'interno' else M.VARCO
        segm = []      # tratti continui di ostacolo lungo il lato
        cur = []
        for i in range(32):
            libero_mare = all(cella.occ[r][c] is None and cella.t[r][c] not in ('mare', 'mare_basso')
                              for c, r in striscia(lato, i))
            if (aperto and i in largo) or not libero_mare:
                if cur:
                    segm.append(cur)
                cur = []
                continue
            cur.append(i)
        if cur:
            segm.append(cur)
        for s in segm:
            disegna_tratto(cella, lato, s, stile, tema)
        if aperto:
            # bocca della strada nel varco
            for i in largo:
                for c, r in striscia(lato, i, M.STRISCIA + 1):
                    if cella.occ[r][c] is None:
                        cella.t[r][c] = tema['strada'] if i in M.VARCO else tema.get('piazza', tema['strada'])
                        cella.occ[r][c] = 'strada'


def disegna_tratto(cella, lato, idx, stile, tema):
    caselle = [p for i in idx for p in striscia(lato, i)]
    for c, r in caselle:
        if cella.occ[r][c] is None:
            cella.occ[r][c] = 'bordo'
    i0, n = idx[0], len(idx)
    if stile == 'palazzi':
        k = 0
        while k < n:
            lung = min(n - k, cella.rng.i(3, 7))
            a = i0 + k
            fac, tetto, h = scegli(cella, tema['facciate']), scegli(cella, tema['tetti']), scegli(cella, tema['altezze'])
            if lato in ('N', 'S'):
                r = 0 if lato == 'N' else 30
                cella.aggiungi(Volume(a, r, lung, 2, h, tetto, fac))
            else:
                c = 0 if lato == 'O' else 30
                cella.aggiungi(Volume(c, a, 2, lung, h, tetto, fac))
            k += lung
    elif stile == 'muro':
        if lato in ('N', 'S'):
            r = 0 if lato == 'N' else 31
            cella.aggiungi(Volume(i0, r, n, 1, 24, tema['muro'], tema['muro']))
            r2 = 1 if lato == 'N' else 30
            filare(cella, i0, r2, n, tema)
        else:
            c = 0 if lato == 'O' else 31
            cella.aggiungi(Volume(c, i0, 1, n, 24, tema['muro'], tema['muro']))
            c2 = 1 if lato == 'O' else 30
            for i in idx:
                cella.aggiungi(Sagoma(scegli(cella, ('cespuglio', 'fico_india')), c2, i))
    elif stile == 'roccia':
        tex = tema.get('roccia', 'roccia')
        if lato in ('N', 'S'):
            cella.aggiungi(Volume(i0, 0 if lato == 'N' else 30, n, 2, 32, tex, tex))
        else:
            cella.aggiungi(Volume(0 if lato == 'O' else 30, i0, 2, n, 32, tex, tex))
    elif stile == 'recinzione':
        if lato in ('N', 'S'):
            r = 1 if lato == 'N' else 30
            cella.aggiungi(Sagoma('recinzione', i0, r, n=n))
            for i in idx:
                cella.blk[0 if lato == 'N' else 31][i] = True
        else:
            c = 1 if lato == 'O' else 30
            for i in idx:
                cella.aggiungi(Sagoma('recinzione', c, i))
                cella.blk[i][0 if lato == 'O' else 31] = True
    else:   # alberi
        if lato in ('N', 'S'):
            for j, r in enumerate((0, 1) if lato == 'N' else (31, 30)):
                filare(cella, i0, r, n, tema, sfalsa=j)
        else:
            for j, c in enumerate((0, 1) if lato == 'O' else (31, 30)):
                for i in idx:
                    if (i + j) % 2 == 0:
                        cella.aggiungi(Sagoma(scegli(cella, tema['alberi']), c, i, blocca=True))
                    cella.blk[i][c] = True
            for i in idx:
                for c in ((0, 1) if lato == 'O' else (31, 30)):
                    cella.beh[(c, i)] = B['BOTTINTESTA']


def filare(cella, c0, r, n, tema, sfalsa=0):
    """Fila di alberi su una riga: sagome da 2 caselle, una ogni 2; tutte le caselle bloccate."""
    k = sfalsa % 2
    while k < n:
        tex = scegli(cella, tema['alberi'])
        larg = 2 if tex in ALBERI_LARGHI else 1
        if k + larg <= n:
            cella.aggiungi(Sagoma(tex, c0 + k, r, larghezza_caselle=larg))
        k += larg + (1 if cella.rng.p(0.3) else 0)
    for i in range(n):
        if cella.dentro(c0 + i, r):
            cella.blk[r][c0 + i] = True
            cella.beh[(c0 + i, r)] = B['BOTTINTESTA']
            cella.occ[r][c0 + i] = cella.occ[r][c0 + i] or 'bordo'


# --------------------------------------------------------------------------- edifici e porte


def edificio(cella, c, r, w, d, h, fac, tetto, porta='porta', dx=None, verso=None, nota='', lato=None, tipo='porta',
             tag='edificio'):
    """Volume con la porta sul lato sud: casella della porta (bloccata, comportamento PORTA) e
    casella davanti libera. Restituisce (porta, davanti)."""
    v = cella.aggiungi(Volume(c, r, w, d, h, tetto, fac, lato))
    cella.riserva(c, r, w, d, tag)
    if porta is None:
        return None
    dx = w // 2 if dx is None else dx
    pc, pr = c + dx, r + d - 1
    tw = {'portone': 32, 'imbocco': 32}.get(porta, 16)
    pan = cella.aggiungi(Pannello(porta, pc, pr))
    if tw == 32:
        pan.c = pc - 0.5
    if tipo == 'porta' and verso is None:
        # porta solo disegnata (edificio senza interno): niente warp, la casella resta un muro
        cella.porte.append(((pc, pr), (pc, pr + 1)))
        return (pc, pr), (pc, pr + 1)
    if tipo == 'porta':
        cella.beh[(pc, pr)] = B['PORTA']
    else:
        # imbocco e cancello: casella libera con il warp verso nord (come le grotte di HeartGold)
        cella.blk[pr][pc] = False
        cella.beh[(pc, pr)] = B['VARCO_NORD']
    cella.varco(tipo, pc, pr, verso, nota)
    cella.porte.append(((pc, pr), (pc, pr + 1)))
    return (pc, pr), (pc, pr + 1)


def centro_pokemon(cella):
    """Centro Pokémon di HeartGold (R-MAP-14): porta alla casella (16,19), corpo bm_field 40 una casella
    e mezza a nord della porta, porta bm_field 15 1,73 unità a sud; set di texture d'edificio 91."""
    if not cella.rect_libero(14, 15, 5, 5) or not cella.libera(16, 20):
        raise ErroreCella('%s: (14..18, 15..19) non libero per il Centro Pokémon' % cella.chiave)
    for r in range(15, 20):
        for c in range(14, 19):
            cella.blk[r][c] = True
    cella.riserva(14, 15, 5, 5, 'centro')
    x, z = 16 * 16 - 248, 19 * 16 - 248
    cella.hg += [(40, x, 0, z - 24), (15, x, 0, z + 1.7314453125)]
    cella.beh[(16, 19)] = B['PORTA']
    cella.varco('porta', 16, 19, 'CENTRO_POKEMON', 'porta del Centro Pokémon (R-MAP-14), atterraggio del Volo a (16,20)')
    cella.porte.append(((16, 19), (16, 20)))


# --------------------------------------------------------------------------- monumenti e gruppi
# Ogni voce: (larghezza, profondità) dell'ingombro e una funzione che disegna a partire da (c, r).


def _cattedrale(cella, c, r, a):
    edificio(cella, c, r, 9, 6, 80, a.get('fac', 'fac_barocca'), 'tetto_coppi', 'portone', 4, a.get('verso'), a.get('nota', ''))
    cella.aggiungi(Volume(c + 7, r - 2, 2, 2, 112, 'tetto_coppi', a.get('fac', 'fac_barocca')))
    cella.riserva(c + 7, r - 2, 2, 2, 'edificio')


def _palazzo(cella, c, r, a):
    if a.get('torri'):
        for cc in (c, c + a['w']):
            cella.aggiungi(Cilindro(cc, r + a['d'] - 2, 2, a.get('h', 64) + 16, a.get('fac', 'muro_lavico'),
                                    a.get('tetto', 'tetto_piano')))
            cella.riserva(cc, r + a['d'] - 2, 2, 2, 'edificio')
        c += 1
    edificio(cella, c, r, a['w'], a['d'], a.get('h', 64), a.get('fac', 'fac_barocca'), a.get('tetto', 'tetto_piano'),
             a.get('porta', 'portone'), a.get('dx'), a.get('verso'), a.get('nota', ''))
    if a.get('insegna'):
        cella.aggiungi(Sagoma('insegna', c + a['w'] // 2 - 1, r + a['d'] - 1, y0=36, blocca=False, larghezza_caselle=2, dz=16.5))
    if a.get('parabole'):
        for k in range(0, a['w'] - 1, 3):
            cella.aggiungi(Sagoma('parabola', c + k, r + 1, y0=a.get('h', 64), blocca=False))


def _casa(cella, c, r, a):
    edificio(cella, c, r, a.get('w', 4), a.get('d', 3), a.get('h', 48), a.get('fac', 'fac_intonaco'),
             a.get('tetto', 'tetto_coppi'), a.get('porta', 'porta'), a.get('dx'), a.get('verso'), a.get('nota', ''))


def _imbocco(cella, c, r, a):
    tex = a.get('roccia', 'roccia')
    edificio(cella, c, r, a.get('w', 5), a.get('d', 3), a.get('h', 48), tex, tex, 'imbocco', a.get('dx'),
             a.get('verso'), a.get('nota', ''), tipo='imbocco')


def _cancello(cella, c, r, a):
    """Ingresso recintato (polo, base, cantiere, MUOS, pineta): guardiola, recinzione e cancello col warp."""
    w = a.get('w', 9)
    cella.riserva(c, r, w, 3, 'edificio')
    gx = c + w // 2
    for k in range(w):
        if c + k != gx:
            cella.aggiungi(Sagoma('recinzione', c + k, r + 2))
    cella.aggiungi(Volume(c, r, 2, 2, 32, 'tetto_cemento', 'fac_cemento'))
    cella.blk[r + 2][gx] = False
    cella.beh[(gx, r + 2)] = B['VARCO_NORD']
    cella.varco('cancello', gx, r + 2, a.get('verso'), a.get('nota', ''))
    cella.porte.append(((gx, r + 2), (gx, r + 3)))
    for k in range(w):
        for rr in (r, r + 1):
            cella.blk[rr][c + k] = True
    for x in a.get('dentro', ()):
        if x == 'serbatoi':
            for k in range(2, w - 2, 3):
                cella.aggiungi(Cilindro(c + k, r, 2, 48, 'serbatoio', 'tetto_cemento', blocca=True))
        elif x == 'traliccio':
            cella.aggiungi(Sagoma('traliccio', c + w - 2, r, blocca=True))
        elif x == 'torcia':
            cella.aggiungi(Sagoma('torcia', c + 2, r, blocca=True))
        elif x == 'alberi':
            for k in range(0, w, 2):
                if c + k != gx and c + k + 1 != gx:
                    cella.aggiungi(Sagoma('pino', c + k, r, larghezza_caselle=2, blocca=True))


def _monumento(cella, c, r, a):
    cella.dipingi(c, r, 3, 3, 'lastricato')
    cella.aggiungi(Volume(c, r + 1, 3, 2, 8, 'lastricato', 'muro_calcare'))
    cella.aggiungi(Sagoma(a.get('sagoma', 'statua'), c + 1, r + 2, y0=8, blocca=True))
    cella.riserva(c, r + 1, 3, 2, 'monumento')
    if a.get('punto'):
        cella.punto(a['punto'], c + 1, r + 3, a.get('nota', ''))


def _gruppo(cella, c, r, a):
    """Gruppo di oggetti in un'area w×d: tavolini, braci, sacchi e cassonetti, ombrelloni, barche…"""
    w, d = a['w'], a['d']
    pezzi = a['pezzi']
    k = 0
    for rr in range(r, r + d):
        for cc in range(c, c + w):
            if (cc - c + rr - r) % a.get('passo', 2) == 0:
                cella.aggiungi(Sagoma(pezzi[k % len(pezzi)], cc, rr, blocca=a.get('blocca', True)))
                k += 1
    cella.riserva(c, r, w, d, 'gruppo')
    if a.get('terreno'):
        cella.dipingi(c, r, w, d, a['terreno'])
    if a.get('punto'):
        cella.punto(a['punto'], c + w // 2, r + d, a.get('nota', ''))


def _specchio(cella, c, r, a):
    """Specchio d'acqua (lago, stagno, pantano) con la riva e i punti d'osservazione sul bordo sud."""
    w, d = a['w'], a['d']
    for rr in range(r, r + d):
        for cc in range(c, c + w):
            bordo = rr in (r, r + d - 1) or cc in (c, c + w - 1)
            cella.t[rr][cc] = a.get('riva', 'sabbia') if bordo else a.get('acqua', 'acqua')
    cella.riserva(c + 1, r + 1, w - 2, d - 2, 'acqua')
    for k in range(a.get('punti', 0)):
        cc = c + 1 + (k * (w - 2)) // max(1, a['punti'] - 1) if a['punti'] > 1 else c + w // 2
        cella.punto('%s_%d' % (a.get('nome', 'osservazione'), k + 1), min(cc, c + w - 2), r + d - 1, a.get('nota', ''))


def _serbatoi(cella, c, r, a):
    for k in range(a.get('n', 3)):
        cella.aggiungi(Cilindro(c + 3 * k, r, 3, a.get('h', 64), 'serbatoio', 'tetto_cemento'))
    cella.riserva(c, r, 3 * a.get('n', 3), 3, 'edificio')


def _binari(cella, c, r, a):
    """Stazione: binario da ovest a est, banchina e fabbricato viaggiatori."""
    for cc in range(0, 32):
        if cella.occ[r][cc] in (None, 'strada') and cella.occ[r + 1][cc] in (None, 'strada'):
            cella.t[r][cc] = 'binario_h'
            cella.t[r + 1][cc] = 'binario_h'
            if cc in M.VARCO:      # passaggio a livello
                cella.occ[r][cc] = cella.occ[r + 1][cc] = 'strada'
            else:
                cella.blk[r][cc] = cella.blk[r + 1][cc] = True
                cella.occ[r][cc] = cella.occ[r + 1][cc] = 'binario'
    cella.dipingi(c, r + 2, a.get('w', 12), 1, 'marciapiede')
    cella.punto(a.get('punto', 'binario'), c + a.get('w', 12) // 2, r + 2, a.get('nota', ''))
    edificio(cella, c + 2, r - 4, 6, 4, 48, 'fac_intonaco', 'tetto_coppi', None)


def _scalinata(cella, c, r, a):
    """Scalinata da nord a sud (Caltagirone, Ibla): gradini e pianerottoli, un punto per rampa."""
    w, d, n = a.get('w', 6), a.get('d', 26), a.get('rampe', 7)
    cella.dipingi(c, r, w, d, 'scalinata')
    cella.riserva(c, r, w, d, 'strada')
    for k in range(n):
        rr = r + 1 + (k * (d - 2)) // max(1, n - 1)
        cella.dipingi(c, rr, w, 1, 'lastricato')
        cella.punto('%s_%d' % (a.get('nome', 'rampa'), k + 1), c + w // 2, rr, a.get('nota', ''))
    for rr in range(r, r + d, 3):
        cella.aggiungi(Sagoma('ringhiera', c - 1, rr, blocca=True))
        cella.aggiungi(Sagoma('ringhiera', c + w, rr, blocca=True))
        for rrr in (rr, rr + 1, rr + 2):
            if cella.dentro(c - 1, rrr):
                cella.blk[rrr][c - 1] = True
            if cella.dentro(c + w, rrr):
                cella.blk[rrr][c + w] = True


def _parete(cella, c, r, a):
    """Parete da Scalaroccia (P-04, P-03): caselle di arrampicata e, in cima, il varco verso nord."""
    w, d = a.get('w', 2), a.get('d', 6)
    roccia = a.get('roccia', 'roccia_nera')
    for rr in range(r + 1, r + d):
        for cc in range(c, c + w):
            cella.t[rr][cc] = 'parete'
    cella.riserva(c - 2, r, w + 4, d, 'parete')
    cella.aggiungi(Volume(c - 2, r, 2, d, 48, roccia, roccia))
    cella.aggiungi(Volume(c + w, r, 2, d, 48, roccia, roccia))
    cella.t[r][c] = a.get('cima', 'sciara')
    cella.beh[(c, r)] = B['VARCO_NORD']
    cella.varco('arrampicata', c, r, a.get('verso'), a.get('nota', ''))
    cella.porte.append(((c, r + d - 1), (c, r + d)))


def _rovine(cella, c, r, a):
    w, d = a['w'], a['d']
    tex = a.get('muro', 'muro_calcare')
    cella.aggiungi(Volume(c, r, w, 1, 16, tex, tex))
    cella.aggiungi(Volume(c, r + 1, 1, d - 1, 16, tex, tex))
    cella.aggiungi(Volume(c + w - 1, r + 1, 1, d - 2, 24, tex, tex))
    cella.aggiungi(Volume(c + 2, r + d - 1, w - 4, 1, 8, tex, tex))
    cella.riserva(c, r, w, d, 'rovine')
    cella.dipingi(c + 1, r + 1, w - 2, d - 2, 'terra')
    if a.get('punto'):
        cella.punto(a['punto'], c + w // 2, r + d, a.get('nota', ''))


def _faro(cella, c, r, a):
    cella.aggiungi(Cilindro(c, r, 2, 112, 'serbatoio', 'tetto_cemento'))
    cella.riserva(c, r, 2, 2, 'edificio')
    if a.get('punto'):
        cella.punto(a['punto'], c, r + 2, a.get('nota', ''))


def _faraglioni(cella, c, r, a):
    for k, (dc, dr, n, h) in enumerate(((0, 0, 2, 64), (4, 2, 3, 96), (9, 1, 2, 48))):
        cella.aggiungi(Cilindro(c + dc, r + dr, n, h, 'roccia_nera', 'roccia_nera'))


def _castello(cella, c, r, a):
    w, d = a.get('w', 9), a.get('d', 7)
    tex = a.get('fac', 'muro_lavico')
    edificio(cella, c + 1, r + 1, w - 2, d - 1, a.get('h', 64), tex, 'tetto_piano', 'portone', (w - 2) // 2,
             a.get('verso'), a.get('nota', ''))
    for cc, rr in ((c, r), (c + w - 2, r), (c, r + d - 2), (c + w - 2, r + d - 2)):
        cella.aggiungi(Cilindro(cc, rr, 2, a.get('h', 64) + 24, tex, 'tetto_piano'))
        cella.riserva(cc, rr, 2, 2, 'edificio')


def _teatro(cella, c, r, a):
    """Cavea del Teatro Greco: gradinate a semicerchio di pietra, non calpestabili."""
    w, d = a.get('w', 14), a.get('d', 8)
    cx = c + w / 2
    for rr in range(r, r + d):
        for cc in range(c, c + w):
            if ((cc + 0.5 - cx) / (w / 2)) ** 2 + ((rr + 0.5 - (r + d)) / d) ** 2 <= 1.0:
                cella.t[rr][cc] = 'scalinata'
                cella.blk[rr][cc] = True
    cella.riserva(c, r, w, d, 'teatro')
    cella.dipingi(c + w // 2 - 2, r + d - 2, 4, 2, 'lastricato')
    if a.get('punto'):
        cella.punto(a['punto'], c + w // 2, r + d, a.get('nota', ''))


def _serre(cella, c, r, a):
    for k in range(a.get('n', 3)):
        cella.aggiungi(Volume(c + 4 * k, r, 3, a.get('d', 6), 24, 'vetrata', 'vetrata'))
    cella.riserva(c, r, 4 * a.get('n', 3) - 1, a.get('d', 6), 'edificio')


def _filari(cella, c, r, a):
    """Campo coltivato con filari (agrumi, ulivi, pistacchi, vigne): righe di sagome."""
    w, d = a['w'], a['d']
    cella.dipingi(c, r, w, d, a.get('terreno', 'terra'))
    for rr in range(r, r + d, 2):
        cella.aggiungi(Sagoma(a.get('pianta', 'albero'), c, rr, n=w // 2, larghezza_caselle=2) if a.get('pianta', 'albero') in ALBERI_LARGHI
                       else Sagoma(a.get('pianta'), c, rr, n=w))
        for cc in range(c, c + w):
            cella.blk[rr][cc] = True
            cella.beh[(cc, rr)] = B['BOTTINTESTA']
    cella.riserva(c, r, w, d, 'campo')


def _fango(cella, c, r, a):
    """Salinelle: pozze di fango (bloccate) e i punti di ispezione accanto."""
    w, d = a.get('w', 14), a.get('d', 10)
    cella.dipingi(c, r, w, d, 'terra')
    pozze = [(c + 2, r + 2), (c + w - 4, r + 2), (c + 2, r + d - 4), (c + w - 4, r + d - 4)]
    for k, (cc, rr) in enumerate(pozze[:a.get('punti', 4)]):
        cella.dipingi(cc, rr, 2, 2, 'fango')
        cella.punto('%s_%d' % (a.get('nome', 'ispezione'), k + 1), cc, rr + 2, a.get('nota', ''))
    cella.riserva(c, r, w, d, 'campo')
    for cc, rr in pozze:
        for k in range(2):
            for j in range(2):
                cella.occ[rr + j][cc + k] = 'fango'
    for rr in range(r, r + d):
        for cc in range(c, c + w):
            if cella.occ[rr][cc] == 'campo':
                cella.occ[rr][cc] = 'strada'


def _ponte(cella, c, r, a):
    """Fiume da nord a sud con un ponte di pietra da ovest a est (Ponte dei Saraceni)."""
    w = a.get('w', 4)
    for rr in range(2, 30):
        for cc in range(c, c + w):
            if cella.occ[rr][cc] in (None,):
                cella.t[rr][cc] = 'acqua'
                cella.occ[rr][cc] = 'acqua'
    for cc in range(c - 1, c + w + 1):
        cella.t[r][cc] = 'lastricato'
        cella.t[r + 1][cc] = 'lastricato'
        cella.occ[r][cc] = cella.occ[r + 1][cc] = 'strada'
    cella.aggiungi(Sagoma('ringhiera', c - 1, r - 1, n=w + 2, blocca=False))
    if a.get('punto'):
        cella.punto(a['punto'], c + w // 2, r, a.get('nota', ''))


# ---- prefabbricati del 4.3


def _tempio(cella, c, r, a):
    """Tempio dorico (Concordia, Giunone, Ercole, Selinunte): stilobate, peristilio sul lato sud,
    trabeazione. `rovina=True`: solo lo stilobate, qualche colonna in piedi e i rocchi a terra."""
    w, d = a.get('w', 10), a.get('d', 6)
    cella.aggiungi(Volume(c, r, w, d, 8, 'tufo', 'tufo'))
    cella.riserva(c, r, w, d + (2 if a.get('rovina') else 0), 'tempio')
    if a.get('rovina'):
        for k in range(0, w, 2):
            if (k * 7 + c) % 3 != 1:
                cella.aggiungi(Sagoma('colonnato', c + k, r + d - 1, y0=8, blocca=False, dz=16.25))
        for k in range(a.get('rocchi', 3)):
            cella.aggiungi(Cilindro(c + 1 + (k * 3) % max(1, w - 2), r + d + 1, 1, 6, 'tufo', 'tufo'))
    else:
        cella.aggiungi(Sagoma('colonnato', c, r + d - 1, n=w, y0=8, blocca=False, dz=16.25))
        cella.aggiungi(Volume(c, r, w, d - 1, 16, 'tufo', 'trabeazione', y0=40, blocca=False))
    if a.get('punto'):
        cella.punto(a['punto'], c + w // 2, r + d + (2 if a.get('rovina') else 0), a.get('nota', ''))


def _saline(cella, c, r, a):
    """Vasche delle saline (Trapani, Stagnone): acqua bassa bloccata, argini ogni 4 righe, un mulino a
    vento e i mucchi di sale sul bordo sud; i punti dei salinai sotto il bordo sud."""
    w, d = a.get('w', 14), a.get('d', 9)
    for rr in range(r, r + d):
        for cc in range(c, c + w):
            argine = (rr - r) % 4 == 3 or cc in (c, c + w - 1)
            cella.t[rr][cc] = 'terra' if argine else 'salina'
    cella.riserva(c, r, w, d, 'acqua')
    if a.get('mulino', True):
        cella.aggiungi(Sagoma('mulino', c + w - 3, r, larghezza_caselle=2))
    for k in range(0, w - 1, 3):
        cella.aggiungi(Sagoma('mucchio_sale', c + k, r + d - 1, blocca=False))
    n = a.get('punti', 0)
    for k in range(n):
        cella.punto('%s_%d' % (a.get('nome', 'salina'), k + 1), c + 1 + k * max(1, (w - 2) // max(1, n)),
                    r + d, a.get('nota', ''))


def _condotta(cella, c, r, a):
    """Condotta dell'acquedotto (tubo basso da ovest a est) con le autobotti del consorzio accanto."""
    w = a.get('w', 20)
    cella.aggiungi(Volume(c, r, w, 1, 8, 'tubo', 'tubo'))
    cella.riserva(c, r, w, 1, 'edificio')
    for k in range(a.get('autobotti', 2)):
        cc = c + 2 + k * 6
        if cc + 1 < c + w:
            cella.aggiungi(Sagoma('autobotte', cc, r + 1, larghezza_caselle=2))
            cella.riserva(cc, r + 1, 2, 1, 'oggetto')
    if a.get('punto'):
        cella.punto(a['punto'], c + w // 2 + 1, r + 2, a.get('nota', ''))


def _casello(cella, c, r, a):
    """Casello autostradale: le cabine sono un volume, le corsie restano libere davanti."""
    w = a.get('w', 6)
    cella.aggiungi(Volume(c, r, w, 2, 32, 'tetto_cemento', 'casello'))
    cella.riserva(c, r, w, 2, 'edificio')
    if a.get('punto'):
        cella.punto(a['punto'], c + w // 2, r + 2, a.get('nota', ''))


def _pilone(cella, c, r, a):
    """Il pilone di Torre Faro: traliccio ottagonale altissimo su una base di cemento."""
    cella.aggiungi(Volume(c, r, 4, 4, 8, 'tetto_cemento', 'fac_cemento'))
    cella.aggiungi(Cilindro(c + 1, r + 1, 2, 160, 'pilone', 'tetto_cemento', blocca=False, y0=8))
    cella.riserva(c, r, 4, 4, 'edificio')
    if a.get('punto'):
        cella.punto(a['punto'], c + 2, r + 4, a.get('nota', ''))


def _chiesa_normanna(cella, c, r, a):
    """Chiesa arabo-normanna con le cupole rosse (San Giovanni degli Eremiti, San Cataldo)."""
    w, d, h = a.get('w', 7), a.get('d', 4), a.get('h', 40)
    edificio(cella, c, r, w, d, h, 'fac_normanna', 'tetto_piano', 'portone' if a.get('verso') else 'porta',
             a.get('dx'), a.get('verso'), a.get('nota', ''))
    n = a.get('cupole', 3)
    for k in range(n):
        cc = c + k * (w - 2) // max(1, n - 1) if n > 1 else c + w // 2 - 1
        cella.aggiungi(Cilindro(cc, r, 2, 12, 'cupola_rossa', 'cupola_rossa', blocca=False, y0=h))


def _rupe(cella, c, r, a):
    """Rupe o sperone di roccia (la Rocca di Cefalù, la rupe di Sperlinga, la scogliera di marna)."""
    w, d = a['w'], a['d']
    tex = a.get('roccia', 'roccia')
    cella.aggiungi(Volume(c, r, w, d, a.get('h', 64), tex, tex))
    cella.riserva(c, r, w, d, 'edificio')
    if a.get('punto'):
        cella.punto(a['punto'], c + w // 2, r + d, a.get('nota', ''))


def _piloni_rotti(cella, c, r, a):
    """Viadotto interrotto dell'A19: piloni di cemento in fila, senza impalcato."""
    w = a.get('w', 20)
    for k in range(0, w - 1, 4):
        cella.aggiungi(Volume(c + k, r, 2, 2, a.get('h', 80) - (k * 11) % 32, 'tetto_cemento', 'fac_cemento'))
        cella.riserva(c + k, r, 2, 2, 'edificio')
    if a.get('punto'):
        cella.punto(a['punto'], c + w // 2, r + 2, a.get('nota', ''))


PREFAB = {
    'cattedrale': ((9, 8), _cattedrale),
    'palazzo': (None, _palazzo),
    'casa': (None, _casa),
    'imbocco': (None, _imbocco),
    'cancello': (None, _cancello),
    'monumento': ((3, 4), _monumento),
    'gruppo': (None, _gruppo),
    'specchio': (None, _specchio),
    'serbatoi': (None, _serbatoi),
    'binari': (None, _binari),
    'scalinata': (None, _scalinata),
    'parete': (None, _parete),
    'rovine': (None, _rovine),
    'faro': ((2, 3), _faro),
    'faraglioni': ((12, 6), _faraglioni),
    'castello': (None, _castello),
    'teatro': (None, _teatro),
    'serre': (None, _serre),
    'filari': (None, _filari),
    'fango': (None, _fango),
    'ponte': (None, _ponte),
    'tempio': (None, _tempio),
    'saline': (None, _saline),
    'condotta': (None, _condotta),
    'casello': (None, _casello),
    'pilone': ((4, 4), _pilone),
    'chiesa_normanna': (None, _chiesa_normanna),
    'rupe': (None, _rupe),
    'piloni_rotti': (None, _piloni_rotti),
}


def ingombro(tipo, a):
    dim, _ = PREFAB[tipo]
    if dim:
        return dim
    if tipo == 'palazzo':
        return a['w'] + (2 if a.get('torri') else 0), a['d']
    if tipo == 'casa':
        return a.get('w', 4), a.get('d', 3)
    if tipo == 'imbocco':
        return a.get('w', 5), a.get('d', 3)
    if tipo == 'cancello':
        return a.get('w', 9), 3
    if tipo == 'serbatoi':
        return 3 * a.get('n', 3), 3
    if tipo == 'binari':
        return a.get('w', 12), 3
    if tipo == 'scalinata':
        return a.get('w', 6), a.get('d', 26)
    if tipo == 'parete':
        return a.get('w', 2) + 4, a.get('d', 6)
    if tipo == 'serre':
        return 4 * a.get('n', 3) - 1, a.get('d', 6)
    if tipo == 'castello':
        return a.get('w', 9), a.get('d', 7)
    if tipo == 'teatro':
        return a.get('w', 14), a.get('d', 8)
    if tipo == 'fango':
        return a.get('w', 14), a.get('d', 10)
    if tipo == 'ponte':
        return a.get('w', 4), 2
    if tipo == 'tempio':
        return a.get('w', 10), a.get('d', 6) + (2 if a.get('rovina') else 0)
    if tipo == 'saline':
        return a.get('w', 14), a.get('d', 9) + 1
    if tipo == 'condotta':
        return a.get('w', 20), 3
    if tipo == 'casello':
        return a.get('w', 6), 3
    if tipo == 'chiesa_normanna':
        return a.get('w', 7), a.get('d', 4)
    if tipo == 'piloni_rotti':
        return a.get('w', 20), 3
    return a['w'], a['d']


def metti(cella, el):
    """Mette un monumento, un ingresso o un gruppo: alla posizione data (`pos`) o nella zona preferita."""
    tipo = el['tipo']
    w, d = ingombro(tipo, el)
    fn = PREFAB[tipo][1]
    if 'pos' in el:
        c, r = el['pos']
        fn(cella, c, r, el)
        return c, r
    con_porta = tipo in ('cattedrale', 'palazzo', 'casa', 'imbocco', 'cancello', 'castello', 'chiesa_normanna') and \
        el.get('verso')
    for c, r in posizioni(cella, w, d, el.get('zona', 'centro'), el.get('margine', 1)):
        if con_porta:
            dx = el.get('dx', (w - (2 if el.get('torri') else 0)) // 2 if tipo == 'palazzo' else None)
            if tipo == 'cancello':
                fx, fr = c + w // 2, r + 3
            elif tipo == 'cattedrale':
                fx, fr = c + 4, r + 8
            elif tipo == 'castello':
                fx, fr = c + 1 + (w - 2) // 2, r + d
            else:
                fx, fr = c + (dx if dx is not None else w // 2), r + d
            if not cella.libera_o_strada(fx, fr) or not cella.libera_o_strada(fx, fr + 1):
                continue
        fn(cella, c, r + (2 if tipo == 'cattedrale' else 0), el)
        return c, r
    raise ErroreCella('%s: nessun posto per %s %s' % (cella.chiave, tipo, el.get('verso') or el.get('nome', '')))


# --------------------------------------------------------------------------- strade


def rete_stradale(cella, tema, mete, partenze):
    """Collega ogni meta (casella) alla rete già tracciata: percorsi più brevi sulle caselle libere,
    larghi 2 (vicoli) o 3 (strade dai varchi)."""
    rete = set(partenze)

    def passa(c, r):
        return cella.occ[r][c] in (None, 'strada') and cella.libera_o_strada(c, r)

    for meta in mete:
        meta, larg, ter, obbl = (meta + (True,))[:4]
        if meta in rete:
            continue
        best = None
        for p in sorted(rete, key=lambda q: abs(q[0] - meta[0]) + abs(q[1] - meta[1]))[:24]:
            pth = M.percorso(cella, p, meta, passa)
            if pth and (best is None or len(pth) < len(best)):
                best = pth
        if best is None:
            if not obbl:
                continue
            raise ErroreCella('%s: nessuna strada verso %s' % (cella.chiave, meta))
        for c, r in best:
            if cella.occ[r][c] is None:
                cella.t[r][c] = ter
                cella.occ[r][c] = 'strada'
            for dc in range(larg):
                for dr in range(larg):
                    cc, rr = c + dc, r + dr
                    if cella.dentro(cc, rr) and cella.occ[rr][cc] is None and cella.libera(cc, rr):
                        cella.t[rr][cc] = ter
                        cella.occ[rr][cc] = 'strada'
            rete.add((c, r))
    return rete


def _libera_o_strada(self, c, r):
    if not self.dentro(c, r) or self.blk[r][c]:
        return False
    if self.occ[r][c] == 'strada':
        return True
    return self.libera(c, r)


M.Cella.libera_o_strada = _libera_o_strada


# --------------------------------------------------------------------------- riempimento e decorazioni


def riempi(cella, tema, sch):
    stile = sch.get('riempi', tema['riempi'])
    rng = cella.rng
    if stile in ('palazzi', 'case', 'industria'):
        tagli = ((6, 4), (5, 4), (4, 4), (4, 3), (3, 3), (5, 3), (3, 2), (2, 2)) if stile != 'industria' else \
            ((8, 5), (6, 4), (4, 3), (3, 3))
        for w, d in tagli:
            for r in range(0, 32 - d + 1):
                for c in range(0, 32 - w + 1):
                    if not cella.rect_libero(c, r, w, d, 1 if stile == 'palazzi' else 0):
                        continue
                    if stile == 'case' and rng.p(0.45):
                        continue
                    if stile == 'palazzi' and rng.p(0.12):
                        continue
                    if stile == 'industria' and w >= 4 and rng.p(0.4):
                        n = w // 3
                        for k in range(n):
                            cella.aggiungi(Cilindro(c + 3 * k, r, min(3, d), 48, 'serbatoio', 'tetto_cemento'))
                        cella.riserva(c, r, w, d, 'riempi')
                        continue
                    fac, tetto, h = scegli(cella, tema['facciate']), scegli(cella, tema['tetti']), scegli(cella, tema['altezze'])
                    cella.aggiungi(Volume(c, r, w, d, h, tetto, fac))
                    cella.riserva(c, r, w, d, 'riempi')
        if stile == 'case':
            giardini(cella, tema)
    elif stile == 'cretto':
        # il Grande Cretto: blocchi bianchi alti un uomo e mezzo, le vecchie vie fra i blocchi
        for r in range(0, 32, 5):
            for c in range(0, 32, 6):
                w, d = 4 + (c * 3 + r) % 2, 3 + (r // 5) % 2
                if cella.rect_libero(c, r, w, d, 0):
                    cella.aggiungi(Volume(c, r, w, d, 24, 'cretto', 'cretto'))
                    cella.riserva(c, r, w, d, 'riempi')
    elif stile in ('campi', 'bosco', 'sciara', 'calanchi'):
        giardini(cella, tema, densita={'campi': 0.18, 'bosco': 0.55, 'sciara': 0.2, 'calanchi': 0.1}[stile])
        if stile == 'campi':
            for r in range(0, 32):
                for c in range(0, 32):
                    if cella.occ[r][c] is None and cella.t[r][c] == tema['base'] and rng.p(0.5):
                        cella.t[r][c] = 'campo'
        if stile == 'sciara':
            for r in range(0, 32):
                for c in range(0, 32):
                    if cella.occ[r][c] is None and rng.p(0.12):
                        cella.t[r][c] = 'sciara_dura'
        if stile == 'calanchi':
            for r in range(0, 32):
                for c in range(0, 32):
                    if cella.occ[r][c] is None and rng.p(0.15):
                        cella.t[r][c] = 'argilla_dura'


def giardini(cella, tema, densita=0.3):
    rng = cella.rng
    for r in range(0, 31):
        for c in range(0, 31):
            if cella.rect_libero(c, r, 2, 1) and rng.p(densita * 0.5):
                tex = scegli(cella, tema['alberi'])
                if tex in ALBERI_LARGHI:
                    cella.aggiungi(Sagoma(tex, c, r, larghezza_caselle=2))
                    cella.riserva(c, r, 2, 1, 'albero')
                    cella.beh[(c, r)] = cella.beh[(c + 1, r)] = B['BOTTINTESTA']
                else:
                    cella.aggiungi(Sagoma(tex, c, r))
                    cella.riserva(c, r, 1, 1, 'albero')


def decora(cella, tema, sch):
    rng = cella.rng
    props = sch.get('props', tema['props'])
    if not props:
        return
    davanti = {f for _, f in cella.porte}
    vicino_strada = []
    for r in range(1, 31):
        for c in range(1, 31):
            if cella.occ[r][c] in (None, 'marciapiede') and not cella.blk[r][c] and (c, r) not in davanti and \
                    any(cella.dentro(c + dc, r + dr) and cella.occ[r + dr][c + dc] == 'strada'
                        for dc, dr in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                vicino_strada.append((c, r))
    for k, (c, r) in enumerate(vicino_strada):
        if (c * 7 + r * 13) % sch.get('passo_props', tema.get('passo_props', 9)) == 0:
            tex = props[rng.u32() % len(props)]
            if tex in ('auto', 'barca', 'insegna', 'autobotte', 'carretto', 'bancarella'):
                if not cella.libera(c + 1, r):
                    continue
                cella.aggiungi(Sagoma(tex, c, r, larghezza_caselle=2))
                cella.riserva(c, r, 2, 1, 'oggetto')
            else:
                cella.aggiungi(Sagoma(tex, c, r))
                cella.riserva(c, r, 1, 1, 'oggetto')


def erba_alta(cella, tema, n=3):
    rng = cella.rng
    fatte = 0
    for r in range(2, 27):
        for c in range(2, 26):
            if fatte >= n:
                return fatte
            w, d = rng.i(4, 6), rng.i(3, 4)
            if all(cella.dentro(cc, rr) and cella.occ[rr][cc] is None and cella.libera(cc, rr)
                   for rr in range(r, r + d) for cc in range(c, c + w)) and rng.p(0.08):
                cella.dipingi(c, r, w, d, 'erba_alta')
                cella.riserva(c, r, w, d, 'erba')
                fatte += 1
    return fatte


# --------------------------------------------------------------------------- cella esterna


def esterno(sch):
    tema = dict(TEMI[sch['tema']])
    tema.update(sch.get('tema_extra', {}))
    cella = M.Cella(sch['chiave'], base=sch.get('base', tema['base']))
    cella.rng = tex42.Rng('cella:' + sch['chiave'])
    lati = sch['lati']
    dipingi_mare(cella, lati, sch.get('diag_mare', ()), tema)
    ostacoli_bordo(cella, lati, tema, sch)
    for c, r, w, h, ter in sch.get('pre', ()):
        cella.dipingi(c, r, w, h, ter)
        if ter in ('acqua', 'mare', 'mare_basso', 'sciara_dura', 'campo_chiuso', 'argilla_dura', 'scoglio'):
            cella.riserva(c, r, w, h, 'acqua')
        else:
            cella.riserva(c, r, w, h, None)
    if sch.get('pc'):
        centro_pokemon(cella)
    # piazza centrale delle città (attorno al Centro, se c'è)
    if sch.get('piazza', tema['bordo'] == 'palazzi' or sch['tema'] in CITTADINI):
        pz = sch.get('rett_piazza', (9, 12, 14, 11) if sch.get('pc') else (11, 12, 10, 8))
        c0, r0, w, h = pz
        for rr in range(r0, r0 + h):
            for cc in range(c0, c0 + w):
                if cella.occ[rr][cc] is None and not cella.blk[rr][cc]:
                    cella.t[rr][cc] = tema['piazza']
                    cella.occ[rr][cc] = 'strada'
    for el in sch.get('elementi', ()):
        metti(cella, el)
    # strade: dalle bocche dei varchi, poi verso porte e punti
    mete = []
    partenze = []
    for lato, (tipo, _) in lati.items():
        if tipo in ('aperto', 'interno'):
            (c, r), (dc, dr) = bocca(lato)
            partenze.append((c, r))
            mete.append(((c, r), 3, tema['strada']))
    if not partenze:
        # cella senza varchi (stanze aperte, celle di scena): la rete parte dalla prima porta
        partenze = [cella.porte[0][1]] if cella.porte else [(15, 15)]
    hub = (16, 20) if sch.get('pc') else sch.get('centro', (15, 15))
    inizio = [partenze[0]]
    if cella.libera_o_strada(*hub):
        mete.insert(0, (hub, 3, tema['strada'], bool(sch.get('pc'))))
    for _, front in cella.porte:
        mete.append((front, 2, tema['vicolo']))
    for p in cella.punti:
        if cella.calpestabile(p['x'], p['z']):
            mete.append(((p['x'], p['z']), 1, tema['vicolo']))
    if cella.occ[inizio[0][1]][inizio[0][0]] is None:
        cella.t[inizio[0][1]][inizio[0][0]] = tema['strada']
        cella.occ[inizio[0][1]][inizio[0][0]] = 'strada'
    rete_stradale(cella, tema, mete, inizio)
    if sch['tema'] in CITTADINI or tema['riempi'] == 'palazzi':
        for r in range(32):
            for c in range(32):
                if cella.occ[r][c] is None and not cella.blk[r][c] and any(
                        cella.dentro(c + dc, r + dr) and cella.occ[r + dr][c + dc] == 'strada'
                        for dc, dr in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                    cella.occ[r][c] = 'marciapiede'
    if sch.get('erba'):
        erba_alta(cella, tema, sch.get('n_erba', 3))
    riempi(cella, tema, sch)
    decora(cella, tema, sch)
    cella.bocche = partenze
    for nome, zona, nota in sch.get('punti', ()):
        punto_libero(cella, nome, zona, nota)
    verifica(cella, partenze)
    return cella


def punto_libero(cella, nome, zona, nota):
    cc, rr = zona_ordine(zona)
    raggiunti = cella.raggiungibili([(15, 15)] + [f for _, f in cella.porte] + list(getattr(cella, 'bocche', [])))
    cand = sorted((p for p in raggiunti if cella.occ[p[1]][p[0]] in (None, 'strada', 'erba')),
                  key=lambda p: (abs(p[0] - cc) + abs(p[1] - rr), p[1], p[0]))
    if not cand:
        raise ErroreCella('%s: nessun posto per il punto %s' % (cella.chiave, nome))
    c, r = cand[0]
    cella.punto(nome, c, r, nota)
    cella.occ[r][c] = 'punto'


def verifica(cella, partenze):
    raggiunti = cella.raggiungibili(partenze)
    mancano = []
    for (pc, pr), front in cella.porte:
        if front not in raggiunti:
            mancano.append('davanti alla porta %s' % ((pc, pr),))
    for p in partenze:
        if p not in raggiunti:
            mancano.append('varco %s' % (p,))
    for p in cella.punti:
        if (p['x'], p['z']) not in raggiunti and cella.calpestabile(p['x'], p['z']):
            mancano.append('punto %s' % p['nome'])
    if len(partenze) > 1:
        a = cella.raggiungibili(partenze[:1])
        for p in partenze[1:]:
            if p not in a:
                mancano.append('varchi non collegati fra loro: %s' % (p,))
    if mancano:
        raise ErroreCella('%s: non raggiungibili: %s' % (cella.chiave, '; '.join(mancano)))
