"""Generatore del blocco 4.1 (inventario degli asset HeartGold, riusi e pipeline grafica).
Uso: python -I tools/generatori/4.1/gen41.py

Scrive docs/MODULO_4/4.1_INVENTARIO_PIPELINE.md e docs/MODULO_4/4.1_INVENTARIO_ASSET.json leggendo i
sorgenti e gli archivi di pokeheartgold (accanto al progetto, F:/Progetti/pokeheartgold), i registri
2.1–2.5, i blocchi 3.1–3.5 e la trama. Rifà il collaudo di tools/trinacria_gfx.py (circa 30 secondi);
le prove di nitrogfx (servono WSL e la ROM originale) sono costanti qui sotto. Testi fissi in text41.py.
"""
import collections
import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
REPO = os.path.normpath(os.path.join(PROJ, '..', 'pokeheartgold'))
DOCS = PROJ + '/docs'
OUT_MD = DOCS + '/MODULO_4/4.1_INVENTARIO_PIPELINE.md'
OUT_JSON = DOCS + '/MODULO_4/4.1_INVENTARIO_ASSET.json'
sys.stdout.reconfigure(errors='backslashreplace')
sys.path.insert(0, HERE)
sys.path.insert(0, PROJ + '/tools')
import trinacria_gfx as G  # noqa: E402
import text41 as T  # noqa: E402

# Prove di nitrogfx del 27/10/2026 (PowerShell: python -I tools/trinacria_gfx.py nitrogfx --rom
# F:/Progetti/pokemon-trinacria-orig/build/pokeheartgold.us.nds --nitrogfx /home/atrisorb/trn_gfx/nitrogfx --wsl
# -> GRAFICA_OK). Il generatore controlla che l'elenco coincida con quello dello strumento.
NITRO = [
    ('pgmap_gra_00000001.png', '.NCGR', '/a/1/4/4', 1),
    ('pgmap_gra_00000010.png', '.NCGR', '/a/1/4/4', 10),
    ('pgmap_gra_00000012.png', '.NCGR', '/a/1/4/4', 12),
    ('titledemo_00000001.png', '.NCGR', '/a/0/4/6', 1),
    ('titledemo_00000015.png', '.NCGR', '/a/0/4/6', 15),
    ('areawindow_0.png', '.NCGR', '/a/1/6/3', 0),
    ('areawindow_0.png', '.NCLR', '/a/1/6/3', 1),
    ('preview_graphic_ruins_of_alph_day.png', '.NCGR.lz', '/a/1/5/0', 31),
    ('preview_graphic_ruins_of_alph_day.png', '.NCLR', '/a/1/5/0', 27),
]
NITRO_AR = [  # andata e ritorno NCGR -> PNG -> NCGR: (NARC, voce, PNG prodotto, opzioni)
    ('/a/0/5/8', 0, '80×80, 16 colori', '-clobbersize -version101 -mappingtype 64 -vram'),
    ('/a/0/5/8', 4, '160×80, 16 colori', '-scanfronttoback'),
    ('/a/0/0/6', 0, '80×640, 16 colori', '-clobbersize -version101 -mappingtype 64 -vram'),
    ('/a/0/0/6', 4, '160×80, 16 colori', '-scanfronttoback'),
]
ROM_CONFRONTO = 'tutte uguali (censimento con --rom, 27/10/2026)'

errors = []


def err(msg):
    errors.append(msg)
    print('ERRORE', msg)


def num(n):
    s = str(n)
    return s if len(s) <= 4 else '{:,}'.format(n).replace(',', '\u2009')


if [(p, e, r, v) for (_, p, e, r, v, _) in G.NITRO_PROVE] != NITRO or \
        [(r, i) for (r, i, _, _, _) in G.NITRO_ANDATA_RITORNO] != [(r, i) for (r, i, _, _) in NITRO_AR]:
    # le voci None dello strumento sono cercate: confronta solo nomi e uscite
    if [(p, e) for (_, p, e, _, _, _) in G.NITRO_PROVE] != [(p, e) for (p, e, _, _) in NITRO]:
        err('l\'elenco delle prove nitrogfx è cambiato nello strumento: rifai le prove e aggiorna NITRO')

# --------------------------------------------------------------------------- collaudo
print('collaudo di tools/trinacria_gfx.py…')
st_errs, st_log = G.selftest(REPO, verbose=False)
for c, m in st_errs:
    err('selftest %s %s' % (c, m))

# --------------------------------------------------------------------------- dati del progetto
maps = []
for f in sorted(glob.glob(DOCS + '/MODULO_2/2.[123]_*.json')):
    maps += json.load(open(f, encoding='utf-8'))['mappe']
names = {}
for f in sorted(glob.glob(DOCS + '/MODULO_3/3.[1-5]_POKEMON_*.json')):
    for s in json.load(open(f, encoding='utf-8'))['specie']:
        names[s['simbolo']] = s['nome']
if len(names) != 493:
    err('nomi delle specie: %d invece di 493' % len(names))
plan = json.load(open(DOCS + '/MODULO_3/3.1_PIANO_INCONTRI.json', encoding='utf-8'))
trama = open(DOCS + '/00_TRAMA_ESPANSA_E_SIDEQUEST.md', encoding='utf-8').read()

# --------------------------------------------------------------------------- censimento e codice
cen, cen_errs = G.census(REPO)
for c, m in cen_errs:
    err('censimento %s %s' % (c, m))
narc_users = collections.defaultdict(set)
for d in ('src', 'src/field', 'src/battle', 'src/application', 'asm'):
    for fn in glob.glob(os.path.join(REPO, d, '*.[cs]')):
        rel = os.path.relpath(fn, REPO).replace('\\', '/')
        for tok in set(re.findall(r'\bNARC_\w+', open(fn, encoding='utf-8', errors='replace').read())):
            narc_users[tok].add(rel)
for e in cen:
    if 'costante' in e:
        e['usato_da'] = sorted(narc_users.get(e['costante'], ()))
n_bin = sum(1 for e in cen if e['nel_repository'] == 'binario')
n_narc_bin = sum(1 for e in cen if e.get('formato') == 'NARC' and e['nel_repository'] == 'binario')
n_voci = sum(e.get('voci', 0) for e in cen if e.get('formato') == 'NARC' and e['nel_repository'] == 'binario')

# --------------------------------------------------------------------------- aree, tileset, celle
tiles = G.Narc(G.originale(REPO, 'a/0/4/4')).files
blds = G.Narc(G.originale(REPO, 'a/0/7/0')).files
land = G.Narc(G.originale(REPO, 'a/0/6/5')).files
areas = G.area_entries(G.originale(REPO, 'a/0/4/2'))
mm, hdrs = G.map_models(REPO)
area_hg = collections.defaultdict(list)
for name, h in hdrs.items():
    area_hg[int(h['areaDataBank'], 0)].append(name)
area_trn = collections.defaultdict(list)
for m in maps:
    area_trn[int(m['intestazione']['areaDataBank'])].append(m['simbolo'])


def tex_summary(b):
    if b == G.VUOTA:
        return {'vuota': True}
    t = G.nsbtx_parse(b)
    fm = collections.Counter(x['formato'] for x in t['texture'])
    tb, pb = G.tex_bytes(b)
    return {'byte': len(b), 'texture': len(t['texture']), 'palette': len(t['palette']),
            'formati': dict(fm.most_common()), 'vram_texture': tb, 'vram_palette': pb}


aree_json = []
for a in areas:
    ts = tex_summary(tiles[a['tex_mappa']])
    bs = tex_summary(blds[a['tex_edifici']])
    vram = sum(G.tex_bytes(tiles[a['tex_mappa']])) + sum(G.tex_bytes(blds[a['tex_edifici']]))
    aree_json.append(dict(a, tileset=ts, texture_edifici=bs, vram=vram,
                          mappe_hg=sorted(area_hg.get(a['indice'], [])),
                          mappe_trinacria=sorted(area_trn.get(a['indice'], []))))
uses = collections.defaultdict(list)
for name, ms in mm.items():
    for x in ms:
        uses[x].append(name)
celle = []
n_bdhc66 = n_bdhc_ug = n_suoni = n_edifici_hg = 0
b1 = G.land_split(land[1])['bdhc']
for i, f in enumerate(land):
    p = G.land_split(f)
    md = G.nsbmd_models(p['modello'])
    nb = len(p['edifici']) // 48
    n_edifici_hg += nb
    n_bdhc66 += len(p['bdhc']) == 66
    n_bdhc_ug += p['bdhc'] == b1
    n_suoni += len(p['suoni']) > 0
    celle.append({'indice': i, 'edifici': nb, 'modelli_edifici': sorted({x['modello'] for x in G.land_buildings(p['edifici'])}),
                  'byte_modello': len(p['modello']), 'byte_bdhc': len(p['bdhc']), 'byte_piastre_sonore': len(p['suoni']),
                  'texture_citate': md['usa_texture'], 'mappe_hg': sorted(uses.get(i, []))})
npairs, e20 = G.area_texture_check(REPO)
difetti = [m for _, m in e20]
tf = collections.Counter()
tsz = collections.Counter()
for f in tiles:
    for x in G.nsbtx_parse(f)['texture']:
        tf[x['formato']] += 1
        tsz['%d×%d' % (x['larghezza'], x['altezza'])] += 1

# --------------------------------------------------------------------------- sprite e Pokémon
rows, sp, mmc = G.sprite_table(REPO)
sp_inv = {v: k for k, v in sp.items()}
ow = G.overworld(REPO)
static = {r['sprite'][len('SPRITE_FOLLOWER_MON_STATIC_'):]: r for r in rows if r['sprite'].startswith('SPRITE_FOLLOWER_MON_STATIC_')}
by_sprite = {r['sprite']: r for r in rows}
for k, r in static.items():
    base = by_sprite.get('SPRITE_FOLLOWER_MON_' + k)
    if base is None or (base['mmodel'], base['param'], base['tipo']) != (r['mmodel'], r['param'], r['tipo']):
        err('lo sprite statico di %s non coincide con quello del Follower' % k)
ev_use = collections.Counter()
for fn in glob.glob(os.path.join(REPO, 'files', 'fielddata', 'eventdata', 'zone_event', '*.json')):
    for o in json.load(open(fn, encoding='utf-8')).get('objects', []):
        ev_use[str(o.get('spriteId'))] += 1
n_follower_in_events = sum(v for k, v in ev_use.items() if k.startswith('SPRITE_FOLLOWER_MON_') and 'STATIC' not in k)
if n_follower_in_events:
    err('ci sono eventi HeartGold con sprite del Follower non statici: R-GFX-15 va rivista')
SPECIALI = {('SPECIES_SNORLAX', 'statico'): 'SPRITE_KABIGON', ('SPECIES_HO_OH', 'statico'): 'SPRITE_HOU_OBJ01',
            ('SPECIES_LUGIA', 'statico'): 'SPRITE_LUG_OBJ01'}
for v in SPECIALI.values():
    if v not in sp:
        err('sprite speciale %s inesistente' % v)
ow_json = []
for r in ow:
    key = r['nome_indice'][len('FOLLOWER_MON_'):]
    ow_json.append(dict(r, nome_trinacria=names.get(r['specie']),
                        sprite_statico=('SPRITE_FOLLOWER_MON_STATIC_' + key) if key in static else None))


def scene_sprite(sym, ctx):
    if (sym, ctx) in SPECIALI:
        return SPECIALI[(sym, ctx)], 'speciale di HeartGold'
    r = ow_json[int(SPECIES_N[sym]) - 1]
    if r['sprite_statico']:
        return r['sprite_statico'], 'statico di HeartGold'
    return r['sprite'][0]['sprite'], 'Follower'


SPECIES_N = {r['specie']: r['n'] for r in ow}
norm = {re.sub(r'[^A-Z0-9]', '', s[len('SPECIES_'):]): s for s in SPECIES_N}
sec = trama[trama.index('#### R-10.3'):trama.index('#### R-10.4')]
scene = collections.OrderedDict()
mismatch = []
for line in sec.splitlines():
    m = re.match(r'\|\s*(\d+)\s*\|\s*\*\*(.+?)\*\*\s*\|[^|]*\|([^|]*)\|', line)
    if not m:
        continue
    op = int(m.group(1))
    for sic, eng in re.findall(r'`([^`]+)`\s*\(([^)]+)\)', m.group(3)):
        cands = [norm.get(re.sub(r'[^A-Z0-9]', '', e.upper())) for e in eng.split('/')]
        sym = next((s for s in cands if s and names.get(s) == sic), None)
        if sym is None:
            mismatch.append('%s (%s) in R-10.3 n. %d: nessuna specie con quel nome nei blocchi 3.1–3.5' % (sic, eng, op))
            continue
        e = scene.setdefault(sym, {'specie': sym, 'n': SPECIES_N[sym], 'nome': sic, 'operazioni': []})
        if op not in e['operazioni']:
            e['operazioni'].append(op)
for e in scene.values():
    e['sprite'], e['tipo'] = scene_sprite(e['specie'], 'scena')
statici = []
for x in plan['speciali'] + plan['leggendari']:
    if x['metodo'] != 'statico':
        continue
    spr, tipo = scene_sprite(x['specie'], 'statico')
    statici.append({'specie': x['specie'], 'n': SPECIES_N[x['specie']], 'nome': names[x['specie']], 'mappa': x['mappa'],
                    'quando': x.get('quando', ''), 'sprite': spr, 'tipo': tipo, 'usi_negli_eventi_hg': ev_use.get(spr, 0)})
for x in list(scene.values()) + statici:
    if x['sprite'] not in sp:
        err('sprite di scena inesistente: %s' % x['sprite'])

# --------------------------------------------------------------------------- Follower nelle mappe
fm = collections.Counter(m['intestazione']['followMode'] for m in maps)
bell = [m for m in maps if re.match(r'MAP_BELL_TOWER_(\d+F|ROOF)$', m['simbolo_hg_sostituito'])]
mem_codes = ('M-PA-02', 'M-PA-01', 'M-TP-02', 'M-TP-01', 'S-PA-07', 'M-PA-04', 'M-AG-04')
memoria = []
for m in maps:
    s = json.dumps(m['contenuti_trama'], ensure_ascii=False)
    if re.search(r'memoria|R-05\.4|sobri', s, re.I) and (any(c in s for c in mem_codes) or 'POZZALLO' in m['simbolo']):
        memoria.append({'mappa': m['simbolo'], 'tipo': m['tipo'], 'followMode': m['intestazione']['followMode']})
memoria_alti = [x['mappa'] for x in memoria if x['followMode'] == 'MAP_FOLLOWMODE_HEIGHT_RESTRICT']
pre = G.Narc(G.originale(REPO, 'a/0/9/2')).files
preload = []
for i, f in enumerate(pre):
    ids = [x for x in G.struct.unpack('<%dH' % (len(f) // 2), f)]
    lst = []
    for x in ids:
        if x == 0xFFFF:
            break
        lst.append(sp_inv.get(x, x))
    preload.append({'moveModelBank': i, 'sprite': lst})

# --------------------------------------------------------------------------- PNG di HeartGold
png_gray = png_dup = 0
for root, _, fs in os.walk(os.path.join(REPO, 'files')):
    for f in fs:
        p = os.path.join(root, f)
        if f.endswith('.png') and os.path.getsize(p):
            if G.png_read(p)['tipo'] == 0:
                png_gray += 1
            av = []
            G.png_check(p, come=p, avvisi=av)
            png_dup += bool(av)

# --------------------------------------------------------------------------- testo
LOG = {k: v for k, v in (ln.split(':', 1) for ln in st_log)}
n_png = int(re.search(r'(\d+) PNG del repository', LOG['PNG']).group(1))
alti = [r for r in ow if r['troppo_alto']]
pgear = sum(1 for e in glob.glob(REPO + '/files/application/pokegear/**/*.png', recursive=True))
vals = dict(
    versione=T.VERSIONE, data=T.DATA, n_fs=len(cen), n_aree=len(areas), n_land=len(land), n_sprite_tab=len(rows),
    n_mappe=len(maps), n_narc_bin=n_narc_bin, n_voci=num(n_voci), n_bin=n_bin, n_matrici=288,
    n_nsbtx=num(1032), n_png=num(n_png), n_nitro=len(NITRO) + len(NITRO_AR), n_coppie=npairs, n_difetti=len(difetti),
    n_ok_coppie=npairs - len(difetti), n_follow_sprite=sum(len(r['sprite']) for r in ow), n_scene=len(scene) + len(statici),
    n_scene_r103=len(scene), n_statici=len(statici),
    n_scene_static=sum(1 for x in list(scene.values()) + statici if x['tipo'] != 'Follower'),
    g3d_sha=G.G3D_SHA256, n_ncgr_tr=0, n_tileset=len(tiles), n_edifici_tex=len(blds),
    n_vuote=sum(1 for f in blds if f == G.VUOTA), n_bm_field=len(G.Narc(G.read(REPO + '/files/fielddata/build_model/bm_field.narc')).files),
    n_bm_room=len(G.Narc(G.read(REPO + '/files/fielddata/build_model/bm_room.narc')).files),
    n_anim=len(G.Narc(G.read(REPO + '/files/a/1/0/6')).files),
    n_preview=len(glob.glob(REPO + '/files/fielddata/graphic/preview_graphic/preview_graphic/*.png')),
    n_pgear=pgear, n_opening=len(os.listdir(REPO + '/files/demo/opening/gs_opening')),
    n_weather=len(G.Narc(G.read(REPO + '/files/data/weather_sys.narc')).files),
    n_bdhc66=n_bdhc66, n_bdhc_uguali=n_bdhc_ug, n_suoni=n_suoni, n_edifici_hg=num(n_edifici_hg),
    formati_tileset=', '.join('%s %s' % (k, num(v)) for k, v in tf.most_common()),
    misure_tileset=', '.join('%s %s' % (k, num(v)) for k, v in tsz.most_common(4)),
    n_mmodel_tx=len(glob.glob(REPO + '/files/data/mmodel/mmodel/*.NSBTX')),
    n_mmodel_md=len(glob.glob(REPO + '/files/data/mmodel/mmodel/*.NSBMD')),
    n_mmodel_js=len(glob.glob(REPO + '/files/data/mmodel/mmodel/*.json')),
    n_preload=len(pre), max_preload=24,
    canon=', '.join(map(str, G.CANON)), n_png_grigi=png_gray, n_png_doppi=png_dup, n_static=len(static),
    n_alti=len(alti), n_femmine=sum(r['femmina_diversa'] for r in ow), n_con_forme=sum(1 for r in ow if r['forme']),
    alti=', '.join('`%s` (%s)' % (names[r['specie']], r['specie'][8:].title().replace('_', '-')) for r in alti),
    **{'lim_' + k: num(v) for k, v in G.LIMITI.items()})
tr_counts = collections.Counter()
for rel in ('a/0/5/8', 'a/0/0/6'):
    fl = G.Narc(G.read(REPO + '/files/' + rel)).files
    tr_counts[rel] = len(fl) // 5
    vals['n_ncgr_tr'] += sum(1 for f in fl if f[:4] == b'RGCN')
vals['n_tr_front'], vals['n_tr_back'] = tr_counts['a/0/5/8'], tr_counts['a/0/0/6']

righe_st = '\n'.join('| %s | %s |' % (k.strip(), v.strip()) for k, v in (ln.split(':', 1) for ln in st_log))
righe_nitro = []
for (folder, png, ext, narc, voce, flags), (_, _, _, v2) in zip(G.NITRO_PROVE, NITRO):
    righe_nitro.append('| `%s/%s` | `%s` %s | `%s` voce %d | identico |' % (
        folder, png, ext, ' '.join('`%s`' % f for f in flags) or '(nessuna opzione)', narc, v2))
for narc, voce, pngd, flags in NITRO_AR:
    righe_nitro.append('| `%s` voce %d (NCGR) | NCGR → PNG %s → NCGR, %s | stessa voce | identico |' % (
        narc, voce, pngd, ' '.join('`%s`' % f for f in flags.split())))
g3d = next((ln.split(':', 1)[1].strip() for ln in st_log if ln.startswith('g3dcvtr')), 'prova saltata')
if 'saltata' in g3d:
    err('g3dcvtr non provato: il generatore va lanciato su Windows con g3dcvtr.exe')

righe_scene = []
for e in scene.values():
    righe_scene.append('| %s | `%s` | `%s` | R-10.3 n. %s | `%s` | %s |' % (
        e['n'], e['specie'], e['nome'], ', '.join(map(str, e['operazioni'])), e['sprite'], e['tipo']))
for e in statici:
    righe_scene.append('| %s | `%s` | `%s` | statico, `%s`%s | `%s` | %s |' % (
        e['n'], e['specie'], e['nome'], e['mappa'], (' (%s)' % e['quando'].split(':')[0]) if e['quando'] else '',
        e['sprite'], e['tipo']))
nota_scene = ('Tutte le specie di R-10.3 hanno trovato il loro nome nei blocchi 3.1–3.5.' if not mismatch else
              'Nomi della trama senza riscontro nei blocchi 3.1–3.5: ' + '; '.join(mismatch) + '.')
fmc = ', '.join('%d `%s`' % (v, k) for k, v in fm.most_common())
top = sorted(area_trn.items(), key=lambda kv: -len(kv[1]))[:12]
righe_aree = []
for a, ms in top:
    x = aree_json[a]
    righe_aree.append('| %d | %d | %d | %s | %s | %d | %s |' % (
        a, x['tex_mappa'], x['tileset'].get('texture', 0), num(x['vram']), 'sì' if x['esterno'] else 'no', len(ms),
        ', '.join('`%s`' % h for h in x['mappe_hg'][:3]) + ('…' if len(x['mappe_hg']) > 3 else '')))

riga = ('BLOCCO COMPLETO: 4.1 — strumento tools/trinacria_gfx.py (K00–K21) collaudato: %d NARC binari (%s voci) '
        'riscritti identici, %d copie binarie uguali alla ROM, %d celle e %s edifici ricomposti identici, %d matrici, '
        '%s NSBTX, %s PNG; catena 2D %d/%d identica alla ROM, catena 3D IMD → g3dcvtr provata; texture per nome '
        '%d/%d coppie (%d difetti di HeartGold); %d aree, %d tileset, %d sprite di campo, 493 specie (%d sprite del '
        'Follower), %d Pokémon in scena (%d specie di R-10.3, %d statici); 17 regole R-GFX; modifica E-GFX-01'
        % (n_narc_bin, num(n_voci), n_bin, len(land), num(n_edifici_hg), 288, num(1032), num(n_png),
           vals['n_nitro'], vals['n_nitro'], npairs - len(difetti), npairs, len(difetti), len(areas), len(tiles),
           len(rows), vals['n_follow_sprite'], len(scene) + len(statici), len(scene), len(statici)))
vals.update(righe_selftest=righe_st, righe_nitro='\n'.join(righe_nitro), g3d_esito=g3d, righe_scene='\n'.join(righe_scene),
            nota_scene=nota_scene, follow_conteggi=fmc,
            memoria_alti=', '.join('`%s`' % x for x in memoria_alti),
            bell_maps=' e '.join('`%s` (al posto di `%s`)' % (m['simbolo'], m['simbolo_hg_sostituito']) for m in bell),
            n_aree_usate=len(area_trn), righe_aree='\n'.join(righe_aree), riga=riga)

md = '\n'.join(t.format(**vals) for t in (
    T.INTESTAZIONE, T.IN_BREVE, T.STRUMENTO, T.AMBIENTE, T.COLLAUDO, T.FORMATI, T.DOVE, T.REGOLE,
    T.PIPELINE_2D, T.PIPELINE_3D, T.POKEMON, T.AREE, T.CODICI, T.NOTE, T.RIGA))

inv = {
    'modulo': 4, 'blocco': '4.1', 'titolo': 'Inventario degli asset HeartGold, riusi e pipeline grafica',
    'versione': T.VERSIONE, 'data': T.DATA, 'progetto': 'Pokémon Trinacria (autore: atrisorb)',
    'file': 'docs/MODULO_4/4.1_INVENTARIO_ASSET.json', 'documento': 'docs/MODULO_4/4.1_INVENTARIO_PIPELINE.md',
    'lettore': 'blocchi 4.2–4.4, Modulo 6 (sprite delle scene), Modulo 7 (7.4)',
    'strumento': {'file': 'tools/trinacria_gfx.py', 'codici': 'K00–K21', 'limiti_R_GFX_13': G.LIMITI,
                  'originali_sha1': G.ORIGINALI, 'g3dcvtr_sha256': G.G3D_SHA256},
    'collaudo': {'selftest': st_log, 'nitrogfx': [dict(zip(('png', 'uscita', 'rom', 'voce'), x)) for x in NITRO],
                 'andata_e_ritorno': [dict(zip(('rom', 'voce', 'png', 'opzioni'), x)) for x in NITRO_AR],
                 'confronto_con_la_rom': ROM_CONFRONTO},
    'filesystem': cen,
    'aree': aree_json,
    'texture_edifici': [dict(indice=i, **tex_summary(f)) for i, f in enumerate(blds)],
    'celle': celle,
    'difetti_texture_hg': difetti,
    'sprite_di_campo': rows,
    'precarico_moveModelBank': preload,
    'pokemon_overworld': ow_json,
    'scene_u_sistema': list(scene.values()),
    'statici': statici,
    'follower_mappe_trinacria': {'conteggi': dict(fm), 'luoghi_della_memoria': memoria,
                                 'diglett_dugtrio_vietati_in_hg': [{'mappa': m['simbolo'], 'slot_hg': m['simbolo_hg_sostituito']} for m in bell],
                                 'troppo_alti': [r['specie'] for r in alti]},
    'riga_finale': riga,
}
os.makedirs(os.path.dirname(OUT_MD), exist_ok=True)
with open(OUT_MD, 'w', encoding='utf-8', newline='\n') as f:
    f.write(md)
with open(OUT_JSON, 'w', encoding='utf-8', newline='\n') as f:
    json.dump(inv, f, ensure_ascii=False, indent=1)
    f.write('\n')
print(riga)
print('GEN41_FAILED' if errors else 'GEN41_OK')
sys.exit(1 if errors else 0)
