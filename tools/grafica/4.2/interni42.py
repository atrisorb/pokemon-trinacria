"""Interni, grotte e mappe aperte del blocco 4.2 (le stanze delle matrici nuove 0288–0329).

Schema uniforme dei collegamenti (R-GFX-21): ogni stanza ha un «giù» e, se serve, un «su».
  - prima stanza di una mappa: il giù è il tappeto d'uscita in basso (USCITA_SUD, come HeartGold);
  - stanze seguenti: il giù è una scala nel muro nord, a sinistra; il su è una scala nel muro nord,
    a destra (VARCO_NORD); nelle mappe aperte giù e su sono varchi nei bordi sud e nord.
Coppie: su della stanza k ↔ giù della stanza k+1; su dell'ultima stanza ↔ giù della prima stanza
della mappa figlia; giù della prima stanza ↔ porta esterna (o su della mappa madre).
"""
import motore42 as M
from motore42 import B, Volume, Cilindro, Sagoma, ErroreCella
import esterni42 as E
import tex42

M.TERRENI.update({
    'pav_marmo': ('pav_marmo', B['NORMALE'], M.LIBERO),
    'parquet': ('parquet', B['NORMALE'], M.LIBERO),
    'pav_ufficio': ('pav_ufficio', B['NORMALE'], M.LIBERO),
    'moquette': ('moquette', B['NORMALE'], M.LIBERO),
    'cemento': ('cemento', B['NORMALE'], M.LIBERO),
    'grotta': ('pav_grotta', B['GROTTA'], M.LIBERO),
    'grotta_lava': ('sciara', B['GROTTA'], M.LIBERO),
    'grotta_calcare': ('lastricato', B['GROTTA'], M.LIBERO),
    'ghiaccio': ('ghiaccio', B['GHIACCIO'], M.LIBERO),
    'zolfo': ('pav_zolfo', B['GROTTA'], M.LIBERO),
    'tappeto': ('tappeto', B['USCITA_SUD'], M.LIBERO),
    'scala': ('scala', B['VARCO_NORD'], M.LIBERO),
    'vasca': ('mare', B['NORMALE'], M.BLOCCATO),
    'terrazza': ('tetto_piano', B['NORMALE'], M.LIBERO),
})

# preset: pavimento, parete, altezza dei muri, oggetti
PRESET = {
    'condominio': dict(pav='cemento', par='par_mattoni', h=48, ogg=[('casse', 3), ('fusti', 2), ('sacchi', 3)]),
    'sportelli': dict(pav='pav_ufficio', par='par_ufficio', h=48, ogg=[('bancone', 1), ('sedie_file', 3), ('piante', 2)]),
    'ufficio': dict(pav='pav_ufficio', par='par_ufficio', h=48, ogg=[('scaffali_nord', 3), ('scrivanie', 4), ('piante', 2)]),
    'archivio': dict(pav='pav_ufficio', par='par_ufficio', h=48, ogg=[('scaffali_nord', 5), ('scaffali_file', 3)]),
    'salone': dict(pav='moquette', par='par_legno', h=56, ogg=[('scaffali_nord', 2), ('scrivania_grande', 1), ('piante', 4), ('statue', 2)]),
    'chiesa': dict(pav='pav_marmo', par='par_intonaco', h=64, ogg=[('altare', 1), ('panche', 6), ('candelore', 6)]),
    'museo': dict(pav='parquet', par='par_intonaco', h=56, ogg=[('vetrine', 6), ('statue', 3)]),
    'club': dict(pav='pav_marmo', par='par_club', h=48, ogg=[('bancone', 1), ('tavolini', 8)]),
    'terminal': dict(pav='pav_ufficio', par='par_ufficio', h=56, ogg=[('quadri_nord', 2), ('sedie_file', 4), ('piante', 2)]),
    'magazzino': dict(pav='cemento', par='par_mattoni', h=48, ogg=[('casse', 6), ('scaffali_file', 2), ('fusti', 2)]),
    'frigo': dict(pav='ghiaccio', par='par_piastr', h=48, ogg=[('casse', 6)]),
    'hangar': dict(pav='cemento', par='lamiera', h=64, ogg=[('casse', 5), ('macchine', 3), ('fusti', 3)]),
    'bunker': dict(pav='cemento', par='par_mattoni', h=40, ogg=[('quadri_nord', 2), ('casse', 3), ('fusti', 2)]),
    'controllo': dict(pav='pav_ufficio', par='par_ufficio', h=48, ogg=[('quadri_nord', 3), ('scrivanie', 3)]),
    'radar': dict(pav='cemento', par='par_ufficio', h=48, ogg=[('quadri_nord', 3), ('macchine', 2), ('scrivanie', 2)]),
    'cabina': dict(pav='cemento', par='par_ufficio', h=40, ogg=[('quadri_nord', 2), ('macchine', 2)]),
    'tonnara': dict(pav='cemento', par='muro_calcare', h=56, ogg=[('vasca', 1), ('casse', 2)]),
    'mercato': dict(pav='cemento', par='lamiera', h=56, ogg=[('banchi', 4), ('casse', 4)]),
    'treno': dict(pav='moquette', par='par_ufficio', h=40, ogg=[('sedili', 1)]),
    'laboratorio': dict(pav='pav_marmo', par='par_piastr', h=48, ogg=[('scaffali_nord', 2), ('piante', 2)]),
    'casa': dict(pav='parquet', par='par_intonaco', h=48, ogg=[('scaffali_nord', 1), ('sedie', 2), ('piante', 1)]),
    'castello': dict(pav='lastricato', par='muro_calcare', h=64, ogg=[('statue', 3), ('panche', 2), ('candelore', 2)]),
    'castello_lavico': dict(pav='basolato', par='muro_lavico', h=64, ogg=[('statue', 2), ('vetrine', 2)]),
    'terrazza': dict(pav='terrazza', par='muro_calcare', h=16, ogg=[('parabole', 3), ('fusti', 1)]),
    'grotta': dict(pav='grotta', par='roccia', h=32, grotta=True, ogg=[('massi', 8), ('stalagmiti', 5)]),
    'grotta_lavica': dict(pav='grotta', par='muro_lavico', h=32, grotta=True, ogg=[('massi', 6), ('stalagmiti', 3)]),
    'grotta_gelo': dict(pav='ghiaccio', par='roccia_nera', h=32, grotta=True, ogg=[('massi', 6), ('stalagmiti', 4)]),
    'latomia': dict(pav='grotta_calcare', par='muro_calcare', h=48, grotta=True, ogg=[('massi', 6), ('alberi', 4)]),
    'zolfara': dict(pav='zolfo', par='roccia', h=32, grotta=True, ogg=[('binari', 1), ('carrelli', 3), ('massi', 4), ('fusti', 2)]),
}


def _sx(cella, c, r):
    return cella.dentro(c, r) and cella.t[r][c] != 'vuoto'


def stanza(cella, x0, y0, w, h, preset, giu, su, nome, n_punti=0):
    """Stanza col pavimento x0..x0+w-1, y0..y0+h-1; muri attorno (nord alto, sud basso)."""
    p = PRESET[preset]
    cella.dipingi(x0, y0, w, h, p['pav'])
    par, hh = p['par'], p['h']
    cima = 'muro_cima'
    scale = {}
    if giu == 'scala':
        scale[x0 + 1] = 'giu'
    if su:
        scale[x0 + w - 2] = 'su'
    # muro nord in tratti, con le scale
    tratto = []
    for c in list(range(x0 - 1, x0 + w + 1)) + [None]:
        if c is None or c in scale:
            if tratto:
                cella.aggiungi(Volume(tratto[0], y0 - 2, len(tratto), 2, hh, cima, par))
            tratto = []
            if c is not None:
                cella.aggiungi(Volume(c, y0 - 2, 1, 1, hh, cima, par))
                cella.t[y0 - 1][c] = 'scala'
                cella.varco('scala', c, y0 - 1, None, '%s: scala %s' % (nome, scale[c]))
                cella.varchi[-1]['ruolo'] = scale[c]
                cella.varchi[-1]['stanza'] = nome
            continue
        tratto.append(c)
    cella.aggiungi(Volume(x0 - 1, y0, 1, h, hh, cima, par))
    cella.aggiungi(Volume(x0 + w, y0, 1, h, hh, cima, par))
    uscita = x0 + w // 2 if giu == 'tappeto' else None
    for seg in ((x0 - 1, uscita), (uscita + 1 if uscita is not None else None, x0 + w + 1)):
        a, b = seg
        if a is None or b is None:
            continue
        if b > a:
            cella.aggiungi(Volume(a, y0 + h, b - a, 1, 16, cima, par))
    if uscita is None:
        cella.aggiungi(Volume(x0 - 1, y0 + h, w + 2, 1, 16, cima, par))
    else:
        cella.t[y0 + h][uscita] = 'tappeto'
        cella.varco('uscita', uscita, y0 + h, None, '%s: tappeto d’uscita' % nome)
        cella.varchi[-1]['ruolo'] = 'giu'
        cella.varchi[-1]['stanza'] = nome
    chiavi = [(v['x'], v['z'] + (1 if v['tipo'] == 'scala' else -1)) for v in cella.varchi if v.get('stanza') == nome]
    oggetti(cella, x0, y0, w, h, p, chiavi)
    for k in range(n_punti):
        E.punto_libero_in(cella, '%s_%d' % (nome, k + 1), (x0, y0, w, h), k, n_punti, chiavi)
    return chiavi


def _prova(cella, chiavi, fn):
    """Mette un oggetto e lo toglie se separa le caselle chiave della stanza."""
    n_ogg, blk = len(cella.ogg), [row[:] for row in cella.blk]
    t = [row[:] for row in cella.t]
    beh = dict(cella.beh)
    fn()
    if len(chiavi) > 1:
        r = cella.raggiungibili(chiavi[:1])
        if any(k not in r for k in chiavi[1:]):
            cella.ogg, cella.blk, cella.t, cella.beh = cella.ogg[:n_ogg], blk, t, beh
            return False
    for k in chiavi:
        if cella.blk[k[1]][k[0]]:
            cella.ogg, cella.blk, cella.t, cella.beh = cella.ogg[:n_ogg], blk, t, beh
            return False
    return True


def oggetti(cella, x0, y0, w, h, p, chiavi):
    rng = cella.rng
    vietate = set()
    for c, r in chiavi:
        for dc in (-1, 0, 1):
            for dr in (-1, 0, 1):
                vietate.add((c + dc, r + dr))

    def libera(c, r, ww=1, dd=1):
        return all(x0 <= cc < x0 + w and y0 <= rr < y0 + h and not cella.blk[rr][cc] and (cc, rr) not in vietate
                   and M.TERRENI[cella.t[rr][cc]][2] == M.LIBERO for cc in range(c, c + ww) for rr in range(r, r + dd))

    def sparsi(tex, n, ww=1):
        k = 0
        for _ in range(n * 8):
            if k >= n:
                break
            c, r = rng.i(x0, x0 + w - ww), rng.i(y0, y0 + h - 1)
            if libera(c, r, ww) and _prova(cella, chiavi, lambda: cella.aggiungi(Sagoma(tex, c, r, larghezza_caselle=ww if ww > 1 else None))):
                k += 1

    def volumi(n, ww, dd, hh, tetto, fronte, righe=None, beh=None):
        k = 0
        for _ in range(n * 10):
            if k >= n:
                break
            c = rng.i(x0, x0 + w - ww)
            r = rng.i(y0, y0 + h - dd) if righe is None else righe
            if libera(c, r, ww, dd):
                def put():
                    cella.aggiungi(Volume(c, r, ww, dd, hh, tetto, fronte))
                    if beh:
                        for cc in range(c, c + ww):
                            cella.beh[(cc, r)] = beh
                if _prova(cella, chiavi, put):
                    k += 1

    for tipo, n in p['ogg']:
        if tipo == 'casse':
            volumi(n, rng.i(1, 2), rng.i(1, 2), 16, 'cassa', 'cassa')
        elif tipo == 'fusti':
            sparsi('fusto', n)
        elif tipo == 'sacchi':
            sparsi('sacchi', n)
        elif tipo in ('piante', 'alberi'):
            sparsi('pianta' if tipo == 'piante' else 'cespuglio', n)
        elif tipo == 'statue':
            sparsi('statua', n)
        elif tipo == 'candelore':
            sparsi('candelora', n)
        elif tipo == 'stalagmiti':
            sparsi('stalagmite', n)
        elif tipo == 'carrelli':
            sparsi('carrello', n)
        elif tipo == 'parabole':
            sparsi('parabola', n)
        elif tipo == 'sedie':
            sparsi('sedia', n)
        elif tipo == 'tavolini':
            sparsi('tavolino', n)
        elif tipo == 'massi':
            volumi(n, rng.i(1, 2), rng.i(1, 2), 24, p['par'], p['par'])
        elif tipo == 'macchine':
            volumi(n, 2, 1, 24, 'lamiera', 'lamiera')
        elif tipo == 'vetrine':
            volumi(n, 2, 1, 16, 'vetrata', 'bancone')
        elif tipo == 'scaffali_nord':
            volumi(n, 2, 1, 40, 'muro_cima', 'scaffale', righe=y0)
        elif tipo == 'quadri_nord':
            volumi(n, 2, 1, 24, 'muro_cima', 'quadro_com', righe=y0)
        elif tipo == 'scaffali_file':
            for k in range(n):
                volumi(1, 2, 1, 40, 'muro_cima', 'scaffale', righe=y0 + 3 + 3 * k)
        elif tipo == 'scrivanie':
            volumi(n, 2, 1, 12, 'scrivania', 'scrivania')
        elif tipo == 'scrivania_grande':
            volumi(1, 4, 1, 12, 'scrivania', 'scrivania', righe=y0 + 2)
        elif tipo == 'bancone':
            r = y0 + 2
            cs = [c for c in range(x0 + 1, x0 + w - 1) if c != x0 + w // 2 - 3]
            ok = all(libera(c, r) for c in cs)
            if ok:
                def put():
                    for c in cs:
                        cella.aggiungi(Volume(c, r, 1, 1, 16, 'bancone', 'bancone'))
                        cella.beh[(c, r)] = B['BANCONE']
                _prova(cella, chiavi, put)
        elif tipo == 'altare':
            volumi(1, 4, 1, 16, 'pav_marmo', 'bancone', righe=y0 + 1)
        elif tipo == 'panche':
            for k in range(n):
                r = y0 + 4 + 2 * (k // 2)
                if r >= y0 + h - 2:
                    break
                c = x0 + 1 if k % 2 == 0 else x0 + w - 4
                if libera(c, r, 3):
                    _prova(cella, chiavi, lambda: cella.aggiungi(Volume(c, r, 3, 1, 10, 'panca', 'panca')))
        elif tipo == 'sedie_file':
            for k in range(n):
                r = y0 + 4 + 2 * k
                if r >= y0 + h - 2:
                    break
                for c in range(x0 + 1, x0 + w - 1, 2):
                    if c in (x0 + w // 2, x0 + w // 2 - 1):
                        continue
                    if libera(c, r):
                        _prova(cella, chiavi, lambda: cella.aggiungi(Sagoma('sedia', c, r)))
        elif tipo == 'banchi':
            for k in range(n):
                r = y0 + 3 + 3 * (k // 2)
                c = x0 + 1 if k % 2 == 0 else x0 + w - 5
                if r < y0 + h - 2 and libera(c, r, 4):
                    _prova(cella, chiavi, lambda: cella.aggiungi(Volume(c, r, 4, 1, 16, 'bancone', 'bancone')))
        elif tipo == 'vasca':
            cw, ch = max(2, w - 6), max(2, h - 6)
            c, r = x0 + 3, y0 + 2
            if libera(c, r, cw, ch):
                _prova(cella, chiavi, lambda: cella.dipingi(c, r, cw, ch, 'vasca'))
        elif tipo == 'binari':
            r = y0 + h // 2
            cella.dipingi(x0, r, w, 1, 'binario_h')
        elif tipo == 'sedili':
            for r in (y0, y0 + h - 1):
                for c in range(x0 + 1, x0 + w - 1, 3):
                    if libera(c, r, 2):
                        _prova(cella, chiavi, lambda: cella.aggiungi(Volume(c, r, 2, 1, 12, 'panca', 'panca')))


def _punto_libero_in(cella, nome, rect, k, n, chiavi):
    x0, y0, w, h = rect
    cx = x0 + 1 + (k + 0.5) * (w - 2) / max(1, n)
    cy = y0 + h // 2
    raggiunti = cella.raggiungibili(chiavi[:1])
    cand = sorted((p for p in raggiunti if x0 <= p[0] < x0 + w and y0 <= p[1] < y0 + h and
                   p not in [(q['x'], q['z']) for q in cella.punti]),
                  key=lambda p: (abs(p[0] - cx) + abs(p[1] - cy), p))
    if cand:
        cella.punto(nome, cand[0][0], cand[0][1], '')


E.punto_libero_in = _punto_libero_in


def cella_stanze(chiave, stanze):
    """Una cella con 1–3 stanze affiancate. stanze: [(nome, preset, giu, su, punti, larghezza, altezza)]."""
    cella = M.Cella(chiave, base='vuoto')
    cella.rng = tex42.Rng('stanza:' + chiave)
    n = len(stanze)
    fascia = 32 // n
    for k, (nome, preset, giu, su, punti, w, h) in enumerate(stanze):
        w = min(w, fascia - 3)
        h = min(h, 24)
        x0 = k * fascia + (fascia - w) // 2
        y0 = 4 + (24 - h) // 2
        chiavi = stanza(cella, x0, y0, w, h, preset, giu, su, nome, punti)
        r = cella.raggiungibili(chiavi[:1])
        miss = [c for c in chiavi if c not in r]
        if miss:
            raise ErroreCella('%s: stanza %s non collegata (%s)' % (chiave, nome, miss))
    return cella


def cella_aperta(chiave, tema, giu, su, elementi=(), punti=(), erba=False, extra=None):
    """Mappa aperta (pineta, polo, MUOS, cantiere…): una cella esterna senza confini percorribili, col
    giù nel bordo sud e il su nel bordo nord (caselle 15 e 16)."""
    lati = {'N': ('aperto' if su else 'chiuso', None), 'S': ('aperto', None), 'O': ('chiuso', None), 'E': ('chiuso', None)}
    sch = dict(chiave=chiave, tema=tema, lati=lati, elementi=list(elementi), punti=list(punti), erba=erba, piazza=False)
    sch.update(extra or {})
    cella = E.esterno(sch)
    for r, ruolo in ((31, 'giu'), (0, 'su') if su else (None, None)):
        if r is None:
            continue
        for c in M.VARCO:
            if c in (15, 16):
                cella.beh[(c, r)] = B['USCITA_SUD'] if r == 31 else B['VARCO_NORD']
                cella.varco('uscita' if r == 31 else 'varco', c, r, None, '%s: %s' % (chiave, ruolo))
                cella.varchi[-1]['ruolo'] = ruolo
                cella.varchi[-1]['stanza'] = chiave
            else:
                cella.blk[r][c] = True
    return cella
