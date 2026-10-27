"""Costruzione della grafica del blocco 4.2 (tileset e modelli 3D di Catania, Siracusa, Ragusa e
Caltanissetta). Uso (da Windows, serve g3dcvtr: documento 4.1, §2):

    python -I tools/grafica/4.2/costruisci42.py [--repo R] [--rom ROM] [--senza-anteprime] [--solo CHIAVE…]

Scrive tutto in build/grafica/4.2/ (fuori da git): texture PNG, IMD, NSBMD, NSBTX, voci di land
data, anteprime PNG e manifesto.json, che `trinacria_gfx.py applica` porta nel repository.
Ultima riga: GRAFICA_OK / GRAFICA_FAILED.
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
sys.path.insert(0, os.path.join(PROJ, 'tools'))
import trinacria_gfx as G  # noqa: E402
import tex42  # noqa: E402
import texint42  # noqa: E402
import motore42 as M  # noqa: E402
import esterni42 as E  # noqa: E402
import interni42 as I  # noqa: E402
import mondo42  # noqa: E402
import schede42  # noqa: E402
import stanze42  # noqa: E402
import anteprima42  # noqa: E402
import ingressi42  # noqa: E402

BLOCCO = '4.2'
OUT = os.path.join(PROJ, 'build', 'grafica', BLOCCO)
PRIMA_CELLA = 676       # voci di a/0/6/5 di HeartGold: le nuove vanno in coda (R-GFX-09)
PRIMO_TILESET = 106     # a/0/4/4
PRIMA_AREA = 106        # a/0/4/2
TEX_EDIFICI_CENTRO = 91  # set di a/0/7/0 più piccolo con le texture del Centro (modelli 40 e 15)
TEX_EDIFICI_VUOTO_INT = 65
TEX_EDIFICI_VUOTO_GROTTA = 85
TEX_EDIFICI_VUOTO_EST = 20

TILESET = [  # chiave, texture, variante
    ('SICILIA', tex42.SICILIA_4_2, None),
    ('SICILIA_GIALLO', tex42.SICILIA_4_2, 'giallo'),
    ('INTERNI_4_2', tex42.SICILIA_4_2 + texint42.INTERNI_4_2, None),
    ('INTERNI_4_2_GIALLO', tex42.SICILIA_4_2 + texint42.INTERNI_4_2, 'giallo'),
]
AREE = [  # chiave, tileset, texture edifici, esterno, luce (dati d'area: documento 4.1 §4.4)
    ('SICILIA', 'SICILIA', TEX_EDIFICI_CENTRO, 1, 1),
    ('SICILIA_GIALLO', 'SICILIA_GIALLO', TEX_EDIFICI_CENTRO, 1, 1),
    ('INTERNI_4_2', 'INTERNI_4_2', TEX_EDIFICI_VUOTO_INT, 0, 0),
    ('GROTTE_4_2', 'INTERNI_4_2', TEX_EDIFICI_VUOTO_GROTTA, 1, 0),
    ('APERTI_4_2', 'INTERNI_4_2', TEX_EDIFICI_VUOTO_EST, 1, 1),
    ('APERTI_4_2_GIALLO', 'INTERNI_4_2_GIALLO', TEX_EDIFICI_VUOTO_EST, 1, 1),
]
GIALLO = {'MAP_SR_AUGUSTA': 'SICILIA_GIALLO', 'MAP_SR_PRIOLO': 'SICILIA_GIALLO',
          'MAP_SR_POLO_PONTILI_SERBATOI': 'APERTI_4_2_GIALLO', 'MAP_SR_POLO_SALA_CONTROLLO_TORCIA': 'APERTI_4_2_GIALLO'}

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
        sch = dict(schede42.SCHEDE.get((x, y), {}))
        sch['chiave'] = 'E_%02d_%02d' % (x, y)
        sch['mappa'] = sym
        sch['cella'] = (x, y)
        sch['lati'] = w.lati(x, y)
        sch['diag_mare'] = w.diag_mare(x, y)
        if m['provincia'] == 'ROADS':
            sch.setdefault('tema', schede42.TEMI_STRADE.get(sym, 'strada'))
            sch.setdefault('titolo', sym[10:].replace('_', ' '))
        sch.setdefault('tema', 'paese')
        v = w.volo.get(sym)
        sch['pc'] = (v is not None and v[:2] == (x, y) and sym != 'MAP_RG_MODICA') or (x, y) in schede42.CENTRI_SENZA_VOLO
        sch.setdefault('erba', 'G' in metodi.get(sym, ''))
        if sch.get('faraglioni'):
            sch['elementi'] = list(sch.get('elementi', [])) + [dict(tipo='faraglioni', pos=(19, 4))]
        out.append(sch)
    return out


def cella_paesaggio(tipo):
    c = M.Cella('P_' + tipo.upper(), base={'mare': 'mare', 'etna': 'sciara', 'campagna': 'erba', 'colline': 'campo'}[tipo])
    c.rng = tex42.Rng('paesaggio:' + tipo)
    if tipo != 'mare':
        alberi = {'etna': ('pino', 'cespuglio'), 'campagna': ('albero', 'fico_india', 'cespuglio'),
                  'colline': ('albero', 'cespuglio')}[tipo]
        for r in range(0, 32, 3):
            for k in range(0, 32, 4):
                cc = (k + (r * 7) % 4) % 31
                if c.rng.p(0.6):
                    tex = alberi[c.rng.u32() % len(alberi)]
                    c.aggiungi(M.Sagoma(tex, cc, r, larghezza_caselle=2 if tex in ('albero', 'pino') else None))
        if tipo == 'colline':
            for r in range(5, 32, 9):
                c.aggiungi(M.Volume(0, r, 32, 1, 16, 'muro_calcare', 'muro_calcare'))
        if tipo == 'campagna':
            c.dipingi(2, 2, 12, 10, 'campo')
            c.dipingi(18, 16, 12, 12, 'campo')
    for r in range(32):
        for cc in range(32):
            c.blk[r][cc] = True       # il paesaggio non si calpesta (intestazione MAP_EVERYWHERE)
    return c


def laboratorio():
    """Laboratorio di cioccolato di Modica: fa da Centro (R-MAP-14): tappeto a (8,19) e ritorno dopo
    una sconfitta a (8,13) davanti al bancone, come la matrice dei Centri di HeartGold."""
    c = M.Cella('I_RG_MODICA_LABORATORIO_0', base='vuoto')
    c.rng = tex42.Rng('stanza:laboratorio')
    chiavi = I.stanza(c, 1, 7, 15, 12, 'laboratorio', 'tappeto', False, 'laboratorio', 0)
    for cc in range(5, 12):
        c.aggiungi(M.Volume(cc, 12, 1, 1, 16, 'bancone', 'bancone'))
        c.beh[(cc, 12)] = M.B['BANCONE']
    c.aggiungi(M.Volume(12, 9, 3, 1, 16, 'bancone', 'bancone'))
    for cc in range(12, 15):
        c.beh[(cc, 9)] = M.B['BANCONE']
    c.punto('cioccolataia', 8, 11, 'S-RG-02: la cioccolataia dietro il bancone (cura)')
    c.punto('ritorno', 8, 13, 'R-MAP-14: ritorno dopo una sconfitta')
    c.punto('negozio', 13, 10, 'R-MAP-15: bancone del negozio')
    if (8, 13) not in c.raggiungibili(chiavi[:1]):
        raise M.ErroreCella('laboratorio: (8,13) non raggiungibile')
    return c


def stanze_mappa(sym, spec, figlia):
    """Celle di una mappa interna: lista di Cella, una per colonna della matrice."""
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


def costruisci_cella(c, dim, tex_dir, trasparenti, bdhc, tileset_b, cartella):
    quads = c.quads(dim)
    text, st = G.imd_scena(quads, tex_dir, c.chiave, trasparenti)
    imd = os.path.join(cartella, 'imd', c.chiave + '.imd')
    scrivi(imd, text, testo=True)
    tmp = os.path.join(os.environ.get('TEMP', '/tmp'), 'trn42_' + c.chiave + '.nsbmd')
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
    w = mondo42.Mondo()
    piano = json.load(open(os.path.join(PROJ, 'docs', 'MODULO_3', '3.1_PIANO_INCONTRI.json'), encoding='utf-8'))
    metodi = {x['mappa']: x['metodi'] for x in piano['mappe']}
    hdrs, ids = G.map_headers(repo)
    land = G.Narc(G.originale(repo, 'a/0/6/5', rom)).files
    blds = G.Narc(G.originale(repo, 'a/0/7/0', rom)).files
    bdhc = G.land_split(land[1])['bdhc']

    # 1. texture e tileset
    tex_dirs, dims, trasp, tileset_b = {}, {}, {}, {}
    for chiave, nomi, var in TILESET:
        d = os.path.join(OUT, 'texture', chiave.lower())
        if os.path.isdir(d):
            shutil.rmtree(d)
        ts = tex42.salva(nomi, d, var)
        for n in nomi:
            for e in G.png_check(os.path.join(d, n + '.png'), bpp=4):
                err('%s %s' % e)
        tex_dirs[chiave] = d
        dims[chiave] = {n: (t.w, t.h) for n, t in ts.items()}
        trasp[chiave] = {n for n, t in ts.items() if t.sagoma}
        imd = os.path.join(OUT, 'imd', 'tileset_%s.imd' % chiave.lower())
        scrivi(imd, tileset_imd(nomi, d, trasp[chiave]), testo=True)
        b = G.g3d_run(imd, os.path.join(OUT, 'tileset', chiave.lower() + '.nsbtx'), 'etex')
        tileset_b[chiave] = b
        got = {t['nome'] for t in G.nsbtx_parse(b)['texture']}
        if got != set(nomi):
            err('K16 tileset %s: %d texture invece di %d' % (chiave, len(got), len(nomi)))
    texs = {}
    for n in tex42.SICILIA_4_2 + texint42.INTERNI_4_2:
        texs[n] = tex42.disegna(n)
    for chiave, ts, edifici, est, luce in AREE:
        for e in G.limiti_tileset(tileset_b[ts], blds[edifici], 'area %s' % chiave):
            err('%s %s' % e)

    # 2. celle
    celle = []        # (Cella, tileset, info)
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
    for tipo in ('mare', 'campagna', 'etna', 'colline'):
        c = cella_paesaggio(tipo)
        c.scheda = {'mappa': None, 'titolo': 'paesaggio: %s' % tipo}
        paesaggi[tipo] = c
        if not a.solo:
            celle.append((c, 'SICILIA'))
    interni = {}
    for sym, spec in stanze42.STANZE.items():
        if a.solo and not any(k.startswith('I_%s' % sym[4:]) for k in a.solo):
            continue
        try:
            if spec == 'laboratorio':
                cs = [laboratorio()]
            else:
                cs = stanze_mappa(sym, spec, stanze42.FIGLIE.get(sym))
        except M.ErroreCella as e:
            err('K16 %s' % e)
            continue
        interni[sym] = cs
        for c in cs:
            c.scheda = {'mappa': sym}
            celle.append((c, 'INTERNI_4_2'))

    # 3. 3D e voci di land data
    info = {}
    for k, (c, ts) in enumerate(celle):
        try:
            info[c.chiave] = costruisci_cella(c, dims[ts], tex_dirs[ts], trasp[ts], bdhc, tileset_b[ts], OUT)
        except G.GfxError as e:
            err('%s %s: %s' % (e.code, c.chiave, e.msg))
            continue
        info[c.chiave]['voce'] = PRIMA_CELLA + k
        if not a.senza_anteprime:
            anteprima42.disegna(c, texs).salva(os.path.join(OUT, 'anteprime', c.chiave + '.png'))
        print('%-48s voce %d, %d poligoni' % (c.chiave, PRIMA_CELLA + k, info[c.chiave]['poligoni']))
    if a.solo:
        print('GRAFICA_FAILED' if errors else 'GRAFICA_OK')
        return 1 if errors else 0

    # 4. anteprime d'ingresso dei dungeon (src/map_preview_graphic.c)
    d_ing = os.path.join(OUT, 'ingressi')
    orig = None
    if rom is not None:
        orig = os.path.join(OUT, 'ingressi_originali')
        os.makedirs(orig, exist_ok=True)
        for f in os.listdir(os.path.join(repo, ingressi42.PREVIEW)):
            if f.endswith(('.png', '.NSCR')):
                shutil.copy(os.path.join(repo, ingressi42.PREVIEW, f), orig)
    ing, lim = ingressi42.costruisci(repo, d_ing, orig)
    for x in ing:
        for e in x['errori']:
            err(e)
    # 5. manifesto
    man = manifesto(w, celle, info, interni, paesaggi, hdrs, repo)
    man['ingressi'] = {'cartella': 'ingressi', 'destinazione': ingressi42.PREVIEW.replace(os.sep, '/'),
                       'limite_tile_hg': lim, 'file': ing}
    scrivi(os.path.join(OUT, 'manifesto.json'), json.dumps(man, ensure_ascii=False, indent=1), testo=True)
    if not a.senza_anteprime:
        mosaico(w, celle, texs)
    print('celle %d, voci %d–%d' % (len(celle), PRIMA_CELLA, PRIMA_CELLA + len(celle) - 1))
    print('GRAFICA_FAILED' if errors else 'GRAFICA_OK')
    return 1 if errors else 0


def assoluto(c_idx, x, z):
    return c_idx * 32 + x, z


def manifesto(w, celle, info, interni, paesaggi, hdrs, repo):
    per_chiave = {c.chiave: c for c, _ in celle}
    aree_idx = {k: PRIMA_AREA + i for i, (k, *_r) in enumerate(AREE)}
    ts_idx = {k: PRIMO_TILESET + i for i, (k, *_r) in enumerate(TILESET)}
    nuove = w.matrici_nuove()
    # matrice 0
    m0 = []
    for c, _ in celle:
        x_y = c.scheda.get('cella')
        if x_y:
            m0.append({'x': x_y[0], 'y': x_y[1], 'cella': c.chiave, 'voce': info[c.chiave]['voce'], 'altitudine': 0,
                       'mappa': c.scheda['mappa']})
    for (x, y), tipo in w.paesaggio_blocco().items():
        m0.append({'x': x, 'y': y, 'cella': paesaggi[tipo].chiave, 'voce': info[paesaggi[tipo].chiave]['voce'],
                   'altitudine': 0, 'mappa': 'MAP_EVERYWHERE', 'paesaggio': tipo})
    # matrici nuove
    matrici = []
    fatte = set()
    for sym, cs in interni.items():
        mt = nuove[w.per_simbolo[sym]['matrice']['simbolo']]
        if mt['simbolo'] in fatte:
            continue
        fatte.add(mt['simbolo'])
        matrici.append({'file': os.path.basename(mt['file']), 'simbolo': mt['simbolo'], 'nome': mt['nome_interno'],
                        'larghezza': mt['larghezza'], 'altezza': mt['altezza'],
                        'voci': [info[c.chiave]['voce'] for c in cs], 'mappe': mt['mappe']})
        if len(cs) != mt['larghezza'] * mt['altezza']:
            err('K04 %s: %d celle disegnate, la matrice ne ha %d' % (mt['file'], len(cs), mt['larghezza'] * mt['altezza']))
    # mappe -> area
    mappe = []
    for m in w.mappe:
        if not (w.del_blocco(m)):
            continue
        sym = m['simbolo']
        mx = m['matrice']['simbolo']
        if 'EVERYWHERE' in mx:
            area = 'SICILIA'
        elif sym in interni or sym in stanze42.STESSA_MATRICE:
            base = stanze42.STESSA_MATRICE.get(sym, sym)
            spec = stanze42.STANZE[base]
            if spec != 'laboratorio' and any(col[0][0] == 'aperta' for col in spec):
                area = 'APERTI_4_2'
            elif spec != 'laboratorio' and all(I.PRESET[s[2]].get('grotta') for col in spec for s in col):
                area = 'GROTTE_4_2'
            else:
                area = 'INTERNI_4_2'
        else:
            area = None
        voce = {'simbolo': sym, 'simbolo_hg': m['simbolo_hg_sostituito'], 'matrice': mx}
        if area:
            voce.update(area=area, areaDataBank=aree_idx[area])
            if sym in GIALLO:
                voce.update(variante_gialla=GIALLO[sym], areaDataBank_giallo=aree_idx[GIALLO[sym]])
        elif m['profilo'].startswith('SAFARI'):
            voce.update(area='HG', areaDataBank=int(m['intestazione']['areaDataBank']), nota='Zona Safari: valori HeartGold (R-MAP-08)')
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
        if c.scheda.get('cella'):
            ox, oz = c.scheda['cella'][0] * 32, c.scheda['cella'][1] * 32
        else:
            ox, oz = int(c.chiave.rsplit('_', 1)[1]) * 32, 0
        for v in c.varchi:
            varchi.setdefault(sym, []).append(dict(v, x=ox + v['x'], z=oz + v['z'], cella=c.chiave))
    for base, alias in ((b, a) for a, b in stanze42.STESSA_MATRICE.items()):
        varchi[alias] = [dict(v) for v in varchi.get(base, [])]
    coll = collegamenti(w, varchi, hdrs, repo)
    punti = {}
    for c, _ in celle:
        sym = c.scheda.get('mappa')
        if not sym:
            continue
        ox, oz = (c.scheda['cella'][0] * 32, c.scheda['cella'][1] * 32) if c.scheda.get('cella') else \
            (int(c.chiave.rsplit('_', 1)[1]) * 32, 0)
        for p in c.punti:
            punti.setdefault(sym, []).append(dict(p, x=ox + p['x'], z=oz + p['z'], cella=c.chiave))
    return {
        'blocco': BLOCCO, 'prima_cella': PRIMA_CELLA, 'primo_tileset': PRIMO_TILESET, 'prima_area': PRIMA_AREA,
        'tileset': [{'chiave': k, 'indice': ts_idx[k], 'file': 'tileset/%s.nsbtx' % k.lower(), 'texture': len(n),
                     'byte': len(open(os.path.join(OUT, 'tileset', k.lower() + '.nsbtx'), 'rb').read()),
                     'variante': v, 'condiviso_matrice_0': k.startswith('SICILIA')} for k, n, v in TILESET],
        'aree': [{'chiave': k, 'indice': aree_idx[k], 'tileset': ts_idx[t], 'tex_edifici': e, 'tex_dinamiche': 0xFFFF,
                  'esterno': es, 'luce': lu} for k, t, e, es, lu in AREE],
        'celle': [dict(chiave=c.chiave, file='celle/%s.bin' % c.chiave, mappa=c.scheda.get('mappa'),
                       titolo=c.scheda.get('titolo', ''), tileset=ts, **info[c.chiave]) for c, ts in celle],
        'matrice_0': m0, 'matrici': matrici, 'mappe': mappe, 'varchi': varchi, 'collegamenti': coll, 'punti': punti,
    }


def collegamenti(w, varchi, hdrs, repo):
    out = []

    def giu(sym):
        vs = [v for v in varchi.get(sym, []) if v.get('ruolo') == 'giu']
        return vs[0] if vs else None

    def su(sym):
        vs = [v for v in varchi.get(sym, []) if v.get('ruolo') == 'su']
        return vs

    def add(a_sym, a, b_sym, b, nota):
        out.append({'da': {'mappa': a_sym, 'x': a['x'], 'z': a['z']}, 'a': {'mappa': b_sym, 'x': b['x'], 'z': b['z']},
                    'nota': nota})

    centri = {}
    for m in w.interni_blocco():
        if m['profilo'] == 'CENTRO':
            centri[(int(m['intestazione']['worldMapX']), int(m['intestazione']['worldMapY']))] = m['simbolo']
    for sym, vs in varchi.items():
        m = w.per_simbolo.get(sym)
        if not m or m['tipo'] != 'esterno':
            continue
        for v in vs:
            dest = v.get('verso')
            if not dest:
                continue
            if dest == 'CENTRO_POKEMON':
                cx, cy = v['x'] // 32, v['z'] // 32
                dest = centri.get((cx, cy))
                if not dest:
                    err('K16 %s: porta del Centro senza mappa del Centro per la cella %s' % (sym, (cx, cy)))
                    continue
            if dest in varchi:
                g = giu(dest) if dest != 'MAP_CT_ETNA_CRATERI_SILVESTRI' else (su(dest) or [None])[-1]
                if g:
                    add(sym, v, dest, g, v.get('nota', ''))
                continue
            dm = w.per_simbolo[dest]
            u = uscita_hg(repo, hdrs, dm['simbolo_hg_sostituito'])
            if u is None:
                err('K16 %s: nessun warp verso l\'esterno nello slot HeartGold %s' % (dest, dm['simbolo_hg_sostituito']))
                continue
            add(sym, v, dest, {'x': u[0], 'z': u[1]}, v.get('nota', '') + ' (interno HeartGold riusato: warp dello slot)')
    # dentro le mappe interne: su della stanza k <-> giù della stanza k+1, poi la mappa figlia
    for sym in list(stanze42.STANZE) + list(stanze42.STESSA_MATRICE):
        if sym not in varchi:
            continue
        sus = [v for v in varchi[sym] if v.get('ruolo') == 'su']
        gius = [v for v in varchi[sym] if v.get('ruolo') == 'giu']
        for k in range(len(gius) - 1):
            if k < len(sus):
                add(sym, sus[k], sym, gius[k + 1], 'scala interna')
        f = stanze42.FIGLIE.get(sym)
        if f and len(sus) >= len(gius):
            if f == 'MAP_CT_ETNA_SUD':
                continue      # già collegato dall'imbocco di Etna Sud
            g = giu(f)
            if g:
                add(sym, sus[-1], f, g, 'verso la mappa figlia')
    return out


def mosaico(w, celle, texs):
    """Panoramica della matrice 0 del blocco: 1 pixel ogni 8 unità."""
    xs = [c.scheda['cella'][0] for c, _ in celle if c.scheda.get('cella')] + [x for x, _ in w.paesaggio_blocco()]
    ys = [c.scheda['cella'][1] for c, _ in celle if c.scheda.get('cella')] + [y for _, y in w.paesaggio_blocco()]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    tela = anteprima42.Tela((x1 - x0 + 1) * 64, (y1 - y0 + 1) * 64 + 16)
    per = {c.scheda['cella']: c for c, _ in celle if c.scheda.get('cella')}
    pae = {c.chiave: c for c, _ in celle if c.chiave.startswith('P_')}
    for (x, y), tipo in w.paesaggio_blocco().items():
        per.setdefault((x, y), pae['P_' + tipo.upper()])
    for (x, y), c in sorted(per.items(), key=lambda kv: (kv[0][1], kv[0][0])):
        anteprima42.disegna(c, texs, tela, (x - x0) * 64, (y - y0) * 64 + 16, scala=8)
    tela.salva(os.path.join(OUT, 'anteprime', 'matrice_0_blocco_4_2.png'))


if __name__ == '__main__':
    sys.exit(main())
