"""Costruzione della grafica del blocco 4.3 (tileset e modelli 3D di Agrigento, Trapani, Palermo, Enna e
Messina). Uso (da Windows, serve g3dcvtr: documento 4.1, §2):

    python -I tools/grafica/4.3/costruisci43.py [--repo R] [--rom ROM] [--senza-anteprime] [--solo CHIAVE…]

Scrive tutto in build/grafica/4.3/ (fuori da git): texture PNG, IMD, NSBMD, NSBTX, voci di land
data, anteprime PNG e manifesto.json, che `trinacria_gfx.py applica --blocchi 4.2 4.3` porta nel
repository. Il tileset condiviso della matrice 0 (SICILIA, R-GFX-18) si ricostruisce qui con le
texture del 4.2 e del 4.3 e sostituisce quello del 4.2 allo stesso indice. Ultima riga: GRAFICA_OK /
GRAFICA_FAILED.
"""
import argparse
import json
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..', '4.2'))
sys.path.insert(0, os.path.join(PROJ, 'tools'))
import trinacria_gfx as G  # noqa: E402
import tex42  # noqa: E402
import tex43  # noqa: E402
import texint43  # noqa: E402
import motore43 as M  # noqa: E402
import esterni43 as E  # noqa: E402
import interni43 as I  # noqa: E402
import mondo43  # noqa: E402
import schede43  # noqa: E402
import stanze43  # noqa: E402
import anteprima43  # noqa: E402
import ingressi43  # noqa: E402

BLOCCO = '4.3'
OUT = os.path.join(PROJ, 'build', 'grafica', BLOCCO)
PRIMA_CELLA = 870       # dopo le 194 voci del 4.2 (R-GFX-09)
PRIMO_TILESET = 110     # a/0/4/4: 106–109 sono del 4.2
PRIMA_AREA = 112        # a/0/4/2: 106–111 sono del 4.2
AREA_SICILIA = 106      # area del 4.2 della matrice 0: il suo tileset 106 è quello ricostruito qui
TEX_EDIFICI_CENTRO = 91  # set di a/0/7/0 più piccolo con le texture del Centro (modelli 40 e 15)
TEX_EDIFICI_VUOTO_INT = 65
TEX_EDIFICI_VUOTO_GROTTA = 85

# chiave, indice in a/0/4/4, variante. INTERNI_4_3 non ha una lista fissa: si calcola dalle celle.
TILESET = [('SICILIA', 106, None), ('SICILIA_GIALLO', 107, 'giallo'), ('INTERNI_4_3', PRIMO_TILESET, None)]
AREE = [  # chiave, tileset, texture edifici, esterno, luce (dati d'area: documento 4.1 §4.4)
    ('INTERNI_4_3', 'INTERNI_4_3', TEX_EDIFICI_VUOTO_INT, 0, 0),
    ('GROTTE_4_3', 'INTERNI_4_3', TEX_EDIFICI_VUOTO_GROTTA, 1, 0),
    ('APERTI_4_3', 'INTERNI_4_3', TEX_EDIFICI_CENTRO, 1, 1),   # mappe aperte e isole (Centro di Lampedusa)
]

errors = []


def err(msg):
    errors.append(msg)
    print('ERRORE', msg)


def scrivi(path, data, testo=False):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if testo:
        with open(path, 'w', encoding='utf-8', newline='\n') as fh:
            fh.write(data)
    else:
        with open(path, 'wb') as fh:
            fh.write(data)


# --------------------------------------------------------------------------- schede


def schede_esterne(w, metodi):
    out = []
    for (x, y), m in w.celle_blocco():
        sym = m['simbolo']
        sch = dict(schede43.SCHEDE.get((x, y), {}))
        sch['chiave'] = 'E_%02d_%02d' % (x, y)
        sch['mappa'] = sym
        sch['cella'] = (x, y)
        sch['lati'] = w.lati(x, y)
        sch['diag_mare'] = w.diag_mare(x, y)
        if m['provincia'] == 'ROADS':
            sch.setdefault('tema', schede43.TEMI_STRADE.get(sym, 'strada'))
            sch.setdefault('titolo', sym[10:].replace('_', ' '))
        sch.setdefault('tema', schede43.TEMA_MAPPA.get(sym, 'paese'))
        sch.setdefault('titolo', m.get('pokegear', {}).get('nome') or sym[4:].replace('_', ' ').title())
        v = w.volo.get(sym)
        sch['pc'] = (v is not None and v[:2] == (x, y) and sym not in schede43.SENZA_CENTRO) or \
            (x, y) in schede43.CENTRI_SENZA_VOLO
        sch.setdefault('erba', 'G' in metodi.get(sym, ''))
        if sch.get('faraglioni'):
            sch['elementi'] = list(sch.get('elementi', [])) + [dict(tipo='faraglioni', pos=(19, 4))]
        out.append(sch)
    return out


def cella_paesaggio(tipo):
    """Modelli di paesaggio (R-GFX-20). Il 4.3 costruisce solo «bosco» (Nebrodi); gli altri quattro sono le
    voci del 4.2 (si ridisegnano qui solo per le anteprime: stesso seme, stesso disegno)."""
    c = M.Cella('P_' + tipo.upper(), base={'mare': 'mare', 'etna': 'sciara', 'campagna': 'erba', 'colline': 'campo',
                                           'bosco': 'erba'}[tipo])
    c.rng = tex42.Rng('paesaggio:' + tipo)
    if tipo != 'mare':
        alberi = {'etna': ('pino', 'cespuglio'), 'campagna': ('albero', 'fico_india', 'cespuglio'),
                  'colline': ('albero', 'cespuglio'), 'bosco': ('faggio', 'faggio', 'pino')}[tipo]
        passo = 2 if tipo == 'bosco' else 3
        for r in range(0, 32, passo):
            for k in range(0, 32, 4 if tipo != 'bosco' else 3):
                cc = (k + (r * 7) % 4) % 31
                if c.rng.p(0.6 if tipo != 'bosco' else 0.85):
                    tex = alberi[c.rng.u32() % len(alberi)]
                    c.aggiungi(M.Sagoma(tex, cc, r, larghezza_caselle=2 if tex in E.ALBERI_LARGHI else None))
        if tipo == 'colline':
            for r in range(5, 32, 9):
                c.aggiungi(M.Volume(0, r, 32, 1, 16, 'muro_calcare', 'muro_calcare'))
        if tipo == 'campagna':
            c.dipingi(2, 2, 12, 10, 'campo')
            c.dipingi(18, 16, 12, 12, 'campo')
        if tipo == 'bosco':
            for cc, rr in ((5, 9), (20, 4), (13, 22), (26, 18)):
                c.aggiungi(M.Volume(cc, rr, 3, 2, 24, 'roccia', 'roccia'))
    for r in range(32):
        for cc in range(32):
            c.blk[r][cc] = True       # il paesaggio non si calpesta (intestazione MAP_EVERYWHERE)
    return c


def stanze_mappa(sym, spec, figlia):
    """Celle di una mappa con matrice nuova: lista di Cella, una per colonna della matrice."""
    celle = []
    tutte = [s for col in spec for s in col]
    k = 0
    for i, col in enumerate(spec):
        chiave = 'I_%s_%d' % (sym[4:], i)
        if col[0][0] == 'aperta':
            _, nome, tema, el, pt, erba, extra = col[0]
            su = (k < len(tutte) - 1) or bool(figlia)
            c = I.cella_aperta(chiave, tema, 'giu', su, el, pt, erba, extra)
            k += 1
        else:
            st = []
            for s in col:
                _, nome, preset, ww, hh, punti = s
                giu = 'tappeto' if k == 0 else 'scala'
                su = (k < len(tutte) - 1) or bool(figlia)
                st.append((nome, preset, giu, su, punti, ww, hh))
                k += 1
            c = I.cella_stanze(chiave, st)
        celle.append(c)
    return celle


# --------------------------------------------------------------------------- 3D


def tileset_imd(nomi, tex_dir, trasparenti):
    quads = []
    for k, n in enumerate(nomi):
        x = (k % 16) * 16 - 128
        z = (k // 16) * 16 - 128
        quads.append((n, [(x, 0, z), (x, 0, z + 16), (x + 16, 0, z + 16), (x + 16, 0, z)],
                      [(0, 0), (0, 16), (16, 16), (16, 0)]))
    return G.imd_scena(quads, tex_dir, 'tileset', trasparenti)[0]


def costruisci_tileset(chiave, nomi, var):
    d = os.path.join(OUT, 'texture', chiave.lower())
    if os.path.isdir(d):
        shutil.rmtree(d)
    ts = tex42.salva(nomi, d, var)
    for n in nomi:
        for e in G.png_check(os.path.join(d, n + '.png'), bpp=4):
            err('%s %s' % e)
    trasp = {n for n, t in ts.items() if t.sagoma}
    imd = os.path.join(OUT, 'imd', 'tileset_%s.imd' % chiave.lower())
    scrivi(imd, tileset_imd(nomi, d, trasp), testo=True)
    b = G.g3d_run(imd, os.path.join(OUT, 'tileset', chiave.lower() + '.nsbtx'), 'etex')
    got = {t['nome'] for t in G.nsbtx_parse(b)['texture']}
    if got != set(nomi):
        err('K16 tileset %s: %d texture invece di %d' % (chiave, len(got), len(nomi)))
    return d, trasp, b


def costruisci_cella(c, dim, tex_dir, trasparenti, bdhc, tileset_b, cartella):
    quads = c.quads(dim)
    text, st = G.imd_scena(quads, tex_dir, c.chiave, trasparenti)
    imd = os.path.join(cartella, 'imd', c.chiave + '.imd')
    scrivi(imd, text, testo=True)
    tmp = os.path.join(os.environ.get('TEMP', '/tmp'), 'trn43_' + c.chiave + '.nsbmd')
    mb = G.g3d_run(imd, tmp, 'emdl')
    os.remove(tmp)
    edifici = G.buildings_build([{'modello': i, 'x': x, 'y': y, 'z': z} for i, x, y, z in c.hg])
    parts = {'suoni': b'', 'permessi': c.permessi(), 'edifici': edifici, 'modello': mb, 'bdhc': bdhc, 'coda': b''}
    voce = G.land_join(parts)
    for e in G.limiti_cella(G.land_split(voce), c.chiave):
        err('%s %s' % e)
    miss = G.texture_mancanti(mb, tileset_b)
    if miss:
        err('K20 %s: texture assenti nel tileset: %s' % (c.chiave, ', '.join(miss)))
    scrivi(os.path.join(cartella, 'celle', c.chiave + '.bin'), voce)
    return {'quadrilateri': st['quadrilateri'], 'poligoni': G.nsbmd_poligoni(mb), 'byte_modello': len(mb),
            'byte_voce': len(voce), 'texture': st['texture']}


# --------------------------------------------------------------------------- warp delle mappe HeartGold


def uscita_hg(repo, hdrs, slot):
    """Casella del warp verso l'esterno nell'interno HeartGold dello slot (matrici riusate)."""
    ev = hdrs[slot]['eventsBank'].strip()
    m = re.match(r'NARC_zone_event_(\d+_\w+)_bin', ev)
    d = json.load(open(os.path.join(repo, 'files', 'fielddata', 'eventdata', 'zone_event', m.group(1) + '.json')))
    for wp in d['warps']:
        dest = str(wp['header'])
        if dest in hdrs and 'EVERYWHERE' in hdrs[dest].get('matrixId', ''):
            return wp['x'], wp['z']
    return None


def area_hg(repo, hdrs, matrice):
    """Area di HeartGold per una matrice riusata: quella delle mappe HeartGold che la usano."""
    for name, h in hdrs.items():
        if h.get('matrixId', '').strip() == matrice:
            return int(h['areaDataBank'])
    return None


# --------------------------------------------------------------------------- principale


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo')
    ap.add_argument('--rom')
    ap.add_argument('--senza-anteprime', action='store_true')
    ap.add_argument('--solo', nargs='*')
    a = ap.parse_args(argv)
    repo = G.find_repo(a.repo)
    rom = G.Rom(a.rom) if a.rom else None
    sys.stdout.reconfigure(errors='backslashreplace')
    w = mondo43.Mondo()
    piano = json.load(open(os.path.join(PROJ, 'docs', 'MODULO_3', '3.1_PIANO_INCONTRI.json'), encoding='utf-8'))
    metodi = {x['mappa']: x['metodi'] for x in piano['mappe']}
    hdrs, ids = G.map_headers(repo)
    land = G.Narc(G.originale(repo, 'a/0/6/5', rom)).files
    blds = G.Narc(G.originale(repo, 'a/0/7/0', rom)).files
    bdhc = G.land_split(land[1])['bdhc']
    texs = {n: tex42.disegna(n) for n in tex42.CATALOGO}
    dims = {n: (t.w, t.h) for n, t in texs.items()}
    trasp_cat = {n for n, t in texs.items() if t.sagoma}

    # 1. tileset condiviso della matrice 0: 4.2 + 4.3 (R-GFX-18)
    tex_dirs, tileset_b = {}, {}
    for chiave, _idx, var in TILESET[:2]:
        tex_dirs[chiave], _t, tileset_b[chiave] = costruisci_tileset(chiave, tex43.SICILIA, var)

    # 2. celle (solo il motore: niente 3D ancora)
    celle = []        # (Cella, tileset)
    for sch in schede_esterne(w, metodi):
        if a.solo and sch['chiave'] not in a.solo:
            continue
        try:
            c = E.esterno(sch)
        except M.ErroreCella as e:
            err('K16 %s' % e)
            continue
        c.scheda = sch
        celle.append((c, 'SICILIA'))
    paesaggi = {}
    for tipo in ('mare', 'campagna', 'etna', 'colline', 'bosco'):
        c = cella_paesaggio(tipo)
        c.scheda = {'mappa': None, 'titolo': 'paesaggio: %s' % tipo}
        paesaggi[tipo] = c
        if tipo not in mondo43.VOCI_PAESAGGIO_4_2 and not a.solo:
            celle.append((c, 'SICILIA'))
    nuove = w.matrici_nuove()
    interni = {}
    for sym, spec in stanze43.STANZE.items():
        if a.solo and not any(k.startswith('I_%s' % sym[4:]) for k in a.solo):
            continue
        try:
            cs = stanze_mappa(sym, spec, stanze43.FIGLIE.get(sym))
        except M.ErroreCella as e:
            err('K16 %s' % e)
            continue
        interni[sym] = cs
        for c in cs:
            c.scheda = {'mappa': sym}
            celle.append((c, 'INTERNI_4_3'))
    mancano = [mt['simbolo'] for mt in nuove.values() if mt['numero'] >= 330 and
               not any(mp in stanze43.STANZE for mp in mt['mappe'])]
    if mancano and not a.solo:
        err('K04 matrici nuove del 4.3 senza stanze: %s' % ', '.join(mancano))

    # 3. tileset degli interni: le texture che le stanze, le grotte, le mappe aperte e le isole citano
    usate = set()
    for c, ts in celle:
        if ts == 'INTERNI_4_3':
            usate |= set(c.texture(dims))
    nomi_int = sorted(usate)
    tex_dirs['INTERNI_4_3'], _t, tileset_b['INTERNI_4_3'] = costruisci_tileset('INTERNI_4_3', nomi_int, None)
    nomi_ts = {'SICILIA': tex43.SICILIA, 'SICILIA_GIALLO': tex43.SICILIA, 'INTERNI_4_3': nomi_int}
    for e in G.limiti_tileset(tileset_b['SICILIA'], blds[TEX_EDIFICI_CENTRO], 'tileset SICILIA'):
        err('%s %s' % e)
    for chiave, ts, edifici, est, luce in AREE:
        for e in G.limiti_tileset(tileset_b[ts], blds[edifici], 'area %s' % chiave):
            err('%s %s' % e)

    # 4. 3D e voci di land data
    info = {}
    for k, (c, ts) in enumerate(celle):
        try:
            info[c.chiave] = costruisci_cella(c, dims, tex_dirs[ts], trasp_cat & set(nomi_ts[ts]), bdhc,
                                              tileset_b[ts], OUT)
        except G.GfxError as e:
            err('%s %s: %s' % (e.code, c.chiave, e.msg))
            continue
        info[c.chiave]['voce'] = PRIMA_CELLA + k
        if not a.senza_anteprime:
            anteprima43.disegna(c, texs).salva(os.path.join(OUT, 'anteprime', c.chiave + '.png'))
        print('%-48s voce %d, %d poligoni' % (c.chiave, PRIMA_CELLA + k, info[c.chiave]['poligoni']))
    if a.solo:
        print('GRAFICA_FAILED' if errors else 'GRAFICA_OK')
        return 1 if errors else 0

    # 5. anteprime d'ingresso dei dungeon (src/map_preview_graphic.c)
    d_ing = os.path.join(OUT, 'ingressi')
    orig = None
    if rom is not None:
        orig = os.path.join(OUT, 'ingressi_originali')
        os.makedirs(orig, exist_ok=True)
        for f in os.listdir(os.path.join(repo, ingressi43.PREVIEW)):
            if f.endswith(('.png', '.NSCR')):
                shutil.copy(os.path.join(repo, ingressi43.PREVIEW, f), orig)
    ing, lim = ingressi43.costruisci(repo, d_ing, orig)
    for x in ing:
        for e in x['errori']:
            err(e)
    # 6. manifesto
    man = manifesto(w, celle, info, interni, paesaggi, hdrs, repo, nomi_ts)
    man['ingressi'] = {'cartella': 'ingressi', 'destinazione': ingressi43.PREVIEW.replace(os.sep, '/'),
                       'limite_tile_hg': lim, 'file': ing}
    scrivi(os.path.join(OUT, 'manifesto.json'), json.dumps(man, ensure_ascii=False, indent=1), testo=True)
    if not a.senza_anteprime:
        mosaico(w, celle, paesaggi, texs)
    print('celle %d, voci %d–%d' % (len(celle), PRIMA_CELLA, PRIMA_CELLA + len(celle) - 1))
    print('GRAFICA_FAILED' if errors else 'GRAFICA_OK')
    return 1 if errors else 0


def origine(c):
    """Origine della cella nelle coordinate assolute della sua matrice (come gli eventi di HeartGold)."""
    if c.scheda.get('cella'):
        return c.scheda['cella'][0] * 32, c.scheda['cella'][1] * 32
    return int(c.chiave.rsplit('_', 1)[1]) * 32, 0


def manifesto(w, celle, info, interni, paesaggi, hdrs, repo, nomi_ts):
    aree_idx = {k: PRIMA_AREA + i for i, (k, *_r) in enumerate(AREE)}
    aree_idx['SICILIA'] = AREA_SICILIA
    ts_idx = {k: i for k, i, _v in TILESET}
    nuove = w.matrici_nuove()
    # matrice 0
    m0 = []
    for c, _ in celle:
        x_y = c.scheda.get('cella')
        if x_y:
            m0.append({'x': x_y[0], 'y': x_y[1], 'cella': c.chiave, 'voce': info[c.chiave]['voce'], 'altitudine': 0,
                       'mappa': c.scheda['mappa']})
    for (x, y), tipo in w.paesaggio_blocco().items():
        voce = mondo43.VOCI_PAESAGGIO_4_2.get(tipo) or info[paesaggi[tipo].chiave]['voce']
        m0.append({'x': x, 'y': y, 'cella': paesaggi[tipo].chiave, 'voce': voce, 'altitudine': 0,
                   'mappa': 'MAP_EVERYWHERE', 'paesaggio': tipo,
                   'blocco_modello': '4.2' if tipo in mondo43.VOCI_PAESAGGIO_4_2 else '4.3'})
    # matrici nuove
    matrici = []
    for sym, cs in interni.items():
        mt = nuove[w.per_simbolo[sym]['matrice']['simbolo']]
        matrici.append({'file': os.path.basename(mt['file']), 'simbolo': mt['simbolo'], 'nome': mt['nome_interno'],
                        'larghezza': mt['larghezza'], 'altezza': mt['altezza'],
                        'voci': [info[c.chiave]['voce'] for c in cs], 'mappe': mt['mappe']})
        if len(cs) != mt['larghezza'] * mt['altezza']:
            err('K04 %s: %d celle disegnate, la matrice ne ha %d' % (mt['file'], len(cs), mt['larghezza'] * mt['altezza']))
    # mappe -> area
    mappe = []
    for m in w.mappe:
        if not w.del_blocco(m):
            continue
        sym = m['simbolo']
        mx = m['matrice']['simbolo']
        if 'EVERYWHERE' in mx:
            area = 'SICILIA'
        elif sym in interni:
            spec = stanze43.STANZE[sym]
            if any(col[0][0] == 'aperta' for col in spec):
                area = 'APERTI_4_3'
            elif all(I.PRESET[s[2]].get('grotta') for col in spec for s in col):
                area = 'GROTTE_4_3'
            else:
                area = 'INTERNI_4_3'
        else:
            area = None
        voce = {'simbolo': sym, 'simbolo_hg': m['simbolo_hg_sostituito'], 'matrice': mx}
        if area:
            voce.update(area=area, areaDataBank=aree_idx[area])
        else:
            a_hg = area_hg(repo, hdrs, mx)
            voce.update(area='HG', areaDataBank=a_hg, nota='matrice riusata di HeartGold: area delle mappe HeartGold che la usano')
        mappe.append(voce)
    # varchi e collegamenti
    varchi = {}
    for c, _ in celle:
        sym = c.scheda.get('mappa')
        if not sym:
            continue
        ox, oz = origine(c)
        for v in c.varchi:
            varchi.setdefault(sym, []).append(dict(v, x=ox + v['x'], z=oz + v['z'], cella=c.chiave))
    coll, senza = collegamenti(w, varchi, hdrs, repo)
    punti = {}
    for c, _ in celle:
        sym = c.scheda.get('mappa')
        if not sym:
            continue
        ox, oz = origine(c)
        for p in c.punti:
            punti.setdefault(sym, []).append(dict(p, x=ox + p['x'], z=oz + p['z'], cella=c.chiave))
    return {
        'blocco': BLOCCO, 'prima_cella': PRIMA_CELLA, 'primo_tileset': PRIMO_TILESET, 'prima_area': PRIMA_AREA,
        'tileset': [{'chiave': k, 'indice': i, 'file': 'tileset/%s.nsbtx' % k.lower(), 'texture': len(nomi_ts[k]),
                     'byte': len(open(os.path.join(OUT, 'tileset', k.lower() + '.nsbtx'), 'rb').read()),
                     'variante': v, 'condiviso_matrice_0': k.startswith('SICILIA'), 'nomi': nomi_ts[k]}
                    for k, i, v in TILESET],
        'aree': [{'chiave': k, 'indice': aree_idx[k], 'tileset': ts_idx[t], 'tex_edifici': e, 'tex_dinamiche': 0xFFFF,
                  'esterno': es, 'luce': lu} for k, t, e, es, lu in AREE],
        'celle': [dict(chiave=c.chiave, file='celle/%s.bin' % c.chiave, mappa=c.scheda.get('mappa'),
                       titolo=c.scheda.get('titolo', ''), tileset=ts, **info[c.chiave]) for c, ts in celle],
        'matrice_0': m0, 'matrici': matrici, 'mappe': mappe, 'varchi': varchi, 'collegamenti': coll,
        'collegamenti_modulo_6': senza, 'punti': punti,
    }


def collegamenti(w, varchi, hdrs, repo):
    """Coppie di warp già decise (R-GFX-21). Restituisce (coppie, casi lasciati al Modulo 6)."""
    out, senza = [], []

    def giu(sym):
        vs = [v for v in varchi.get(sym, []) if v.get('ruolo') == 'giu']
        return vs[0] if vs else None

    def add(a_sym, a, b_sym, b, nota):
        out.append({'da': {'mappa': a_sym, 'x': a['x'], 'z': a['z']}, 'a': {'mappa': b_sym, 'x': b['x'], 'z': b['z']},
                    'nota': nota})

    def verso_hg(a_sym, a, dest, nota):
        dm = w.per_simbolo[dest]
        u = uscita_hg(repo, hdrs, dm['simbolo_hg_sostituito'])
        if u is None:
            senza.append({'da': {'mappa': a_sym, 'x': a['x'], 'z': a['z']}, 'a': {'mappa': dest},
                          'nota': nota + ' (interno HeartGold riusato senza warp verso la matrice 0: il Modulo 6 '
                                         'sceglie il warp d’ingresso dello slot)'})
            return
        add(a_sym, a, dest, {'x': u[0], 'z': u[1]}, nota + ' (interno HeartGold riusato: warp dello slot)')

    centri = {}
    for m in w.interni_blocco():
        if m['profilo'] == 'CENTRO' and m['matrice']['simbolo'].endswith('T21PC0101_bin') and m.get('accesso_da'):
            h = m['intestazione']
            centri[(m['accesso_da'], int(h['worldMapX']), int(h['worldMapY']))] = m['simbolo']
            centri.setdefault((m['accesso_da'], None, None), m['simbolo'])
    for sym, vs in varchi.items():
        m = w.per_simbolo.get(sym)
        if not m or m['tipo'] != 'esterno':
            continue
        for v in vs:
            dest = v.get('verso')
            if not dest:
                continue
            if dest == 'CENTRO_POKEMON':
                if 'EVERYWHERE' in m['matrice']['simbolo']:
                    dest = centri.get((sym, v['x'] // 32, v['z'] // 32))
                else:
                    dest = centri.get((sym, None, None))      # isole: il Centro della mappa
                if not dest:
                    err('K16 %s: porta del Centro senza mappa del Centro (%d,%d)' % (sym, v['x'] // 32, v['z'] // 32))
                    continue
            if dest in varchi:
                g = giu(dest)
                if g:
                    add(sym, v, dest, g, v.get('nota', ''))
                continue
            verso_hg(sym, v, dest, v.get('nota', ''))
    # dentro le mappe: su della stanza k <-> giù della stanza k+1, poi la mappa figlia
    for sym in stanze43.STANZE:
        if sym not in varchi:
            continue
        sus = [v for v in varchi[sym] if v.get('ruolo') == 'su']
        gius = [v for v in varchi[sym] if v.get('ruolo') == 'giu']
        for k in range(len(gius) - 1):
            if k < len(sus):
                add(sym, sus[k], sym, gius[k + 1], 'scala interna')
        f = stanze43.FIGLIE.get(sym)
        if f and len(sus) >= len(gius):
            g = giu(f)
            if g:
                add(sym, sus[-1], f, g, 'verso la mappa figlia')
            else:
                verso_hg(sym, sus[-1], f, 'verso la mappa figlia')
    return out, senza


def mosaico(w, celle, paesaggi, texs):
    """Panoramica della matrice 0 del blocco: 1 pixel ogni 8 unità."""
    per = {c.scheda['cella']: c for c, _ in celle if c.scheda.get('cella')}
    for (x, y), tipo in w.paesaggio_blocco().items():
        per.setdefault((x, y), paesaggi[tipo])
    xs = [x for x, _ in per]
    ys = [y for _, y in per]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    tela = anteprima43.Tela((x1 - x0 + 1) * 64, (y1 - y0 + 1) * 64 + 16)
    for (x, y), c in sorted(per.items(), key=lambda kv: (kv[0][1], kv[0][0])):
        anteprima43.disegna(c, texs, tela, (x - x0) * 64, (y - y0) * 64 + 16, scala=8)
    tela.salva(os.path.join(OUT, 'anteprime', 'matrice_0_blocco_4_3.png'))


if __name__ == '__main__':
    sys.exit(main())
