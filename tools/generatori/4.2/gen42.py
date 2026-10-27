"""Generatore del blocco 4.2 (tileset e modelli 3D di CT, SR, RG, CL).
Uso (Windows, serve g3dcvtr): python -I tools/generatori/4.2/gen42.py [--senza-costruzione]

Rilancia tools/grafica/4.2/costruisci42.py (circa 3 minuti), prova `trinacria_gfx.py applica --prova`
in una cartella temporanea, poi scrive docs/MODULO_4/4.2_TILESET_EST.md e
docs/MODULO_4/4.2_CELLE_EST.json dal manifesto. Testi fissi in text42.py.
"""
import collections
import json
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
REPO = os.path.normpath(os.path.join(PROJ, '..', 'pokeheartgold'))
G42 = os.path.join(PROJ, 'tools', 'grafica', '4.2')
BUILD = os.path.join(PROJ, 'build', 'grafica', '4.2')
OUT_MD = os.path.join(PROJ, 'docs', 'MODULO_4', '4.2_TILESET_EST.md')
OUT_JSON = os.path.join(PROJ, 'docs', 'MODULO_4', '4.2_CELLE_EST.json')
sys.stdout.reconfigure(errors='backslashreplace')
sys.path.insert(0, HERE)
sys.path.insert(0, G42)
sys.path.insert(0, os.path.join(PROJ, 'tools'))
import trinacria_gfx as G  # noqa: E402
import costruisci42  # noqa: E402
import mondo42  # noqa: E402
import esterni42  # noqa: E402
import interni42  # noqa: E402
import tex42  # noqa: E402
import texint42  # noqa: E402
import text42 as T  # noqa: E402

errors = []


def err(m):
    errors.append(m)
    print('ERRORE', m)


if '--senza-costruzione' not in sys.argv:
    print('costruzione (tools/grafica/4.2/costruisci42.py)…')
    if costruisci42.main([]) != 0:
        err('costruisci42: GRAFICA_FAILED')
man = json.load(open(os.path.join(BUILD, 'manifesto.json'), encoding='utf-8'))

# prova di applica in una cartella temporanea
tmp = tempfile.mkdtemp(prefix='trn42_applica_')
try:
    e_ap, log_ap = G.applica(REPO, ['4.2'], os.path.dirname(BUILD), None, tmp)
    for c, m in e_ap:
        err('applica %s %s' % (c, m))
    land = G.Narc(G.read(os.path.join(tmp, 'files', 'a', '0', '6', '5'))).files
    aree = G.area_entries(G.read(os.path.join(tmp, 'files', 'a', '0', '4', '2')))
    tiles = G.Narc(G.read(os.path.join(tmp, 'files', 'a', '0', '4', '4'))).files
    m0 = G.matrix_parse(G.read(os.path.join(tmp, 'files', 'fielddata', 'mapmatrix', 'map_matrix',
                                             'map_matrix_0000_EVERYWHERE.bin')))
    # ogni cella della matrice 0 del blocco: voce giusta, texture nel tileset dell'area SICILIA
    k20 = 0
    ts_sic = tiles[man['tileset'][0]['indice']]
    for c in man['matrice_0']:
        v = m0['modelli'][c['y'] * 47 + c['x']]
        if v != c['voce']:
            err('applica: matrice 0 (%d,%d) = %d invece di %d' % (c['x'], c['y'], v, c['voce']))
        if G.texture_mancanti(G.land_split(land[v])['modello'], ts_sic):
            k20 += 1
    if k20:
        err('K20: %d celle della matrice 0 con texture assenti nel tileset condiviso' % k20)
    for a in man['aree']:
        x = aree[a['indice']]
        if (x['tex_mappa'], x['tex_edifici'], x['esterno'], x['luce']) != (a['tileset'], a['tex_edifici'], a['esterno'], a['luce']):
            err('applica: area %s scritta diversa' % a['chiave'])
    prova = {'righe': log_ap, 'voci_a065': len(land), 'voci_a044': len(tiles), 'voci_a042': len(aree),
             'k20_matrice_0': k20}
finally:
    shutil.rmtree(tmp, ignore_errors=True)

# --------------------------------------------------------------------------- dati per il documento
w = mondo42.Mondo()
celle = man['celle']
est = [c for c in celle if c['chiave'].startswith('E_')]
pae = [c for c in celle if c['chiave'].startswith('P_')]
inte = [c for c in celle if c['chiave'].startswith('I_')]
coll = man['collegamenti']
n_varchi = sum(len(v) for v in man['varchi'].values())
n_punti = sum(len(v) for v in man['punti'].values())
pol = [c['poligoni'] for c in celle]
ts_sic = man['tileset'][0]
ts_int = man['tileset'][2]
vram_sic = None
blds = G.Narc(G.originale(REPO, 'a/0/7/0')).files
b_sic = G.read(os.path.join(BUILD, ts_sic['file']))
b_int = G.read(os.path.join(BUILD, ts_int['file']))
vram_sic = sum(G.tex_bytes(b_sic)) + sum(G.tex_bytes(blds[costruisci42.TEX_EDIFICI_CENTRO]))
vram_int = sum(G.tex_bytes(b_int))
ing = man['ingressi']['file']
mappe_area = collections.Counter(m['area'] for m in man['mappe'])

dati = dict(man=man, w=w, est=est, pae=pae, inte=inte, coll=coll, n_varchi=n_varchi, n_punti=n_punti, pol=pol,
            vram_sic=vram_sic, vram_int=vram_int, ing=ing, mappe_area=mappe_area, prova=prova,
            temi=esterni42.TEMI, preset=interni42.PRESET, sic=tex42.SICILIA_4_2, intx=texint42.INTERNI_4_2,
            limiti=G.LIMITI, b_sic=len(b_sic), b_int=len(b_int))
md = T.documento(dati)
riga = T.riga_finale(dati)
md += '\n## 14. Riga di controllo\n\n`%s`\n' % riga
with open(OUT_MD, 'w', encoding='utf-8', newline='\n') as fh:
    fh.write(md)

out = {
    'modulo': 4, 'blocco': '4.2', 'titolo': 'Tileset e modelli 3D di Catania, Siracusa, Ragusa e Caltanissetta',
    'versione': '1.0', 'data': '27/10/2026', 'progetto': 'Pokémon Trinacria (autore: atrisorb)',
    'documento': 'docs/MODULO_4/4.2_TILESET_EST.md',
    'lettore': 'Modulo 6 (warp, punti, oggetti nelle mappe), blocco 4.3 (tileset condiviso, numerazione), 7.4 (TASK)',
    'numerazione': {'prima_cella_a065': man['prima_cella'], 'ultima_cella_a065': man['prima_cella'] + len(celle) - 1,
                    'primo_tileset_a044': man['primo_tileset'], 'prima_area_a042': man['prima_area'],
                    'prossima_cella_4_3': man['prima_cella'] + len(celle),
                    'prossimo_tileset_4_3': man['primo_tileset'] + len(man['tileset']),
                    'prossima_area_4_3': man['prima_area'] + len(man['aree'])},
    'tileset': man['tileset'], 'aree': man['aree'],
    'celle': [{k: c[k] for k in ('chiave', 'voce', 'mappa', 'titolo', 'tileset', 'poligoni', 'byte_voce')} for c in celle],
    'matrice_0': man['matrice_0'], 'matrici': man['matrici'], 'mappe': man['mappe'],
    'varchi': man['varchi'], 'collegamenti': coll, 'punti': man['punti'], 'ingressi': man['ingressi'],
    'prova_applica': prova, 'riga_finale': riga,
}
with open(OUT_JSON, 'w', encoding='utf-8', newline='\n') as fh:
    json.dump(out, fh, ensure_ascii=False, indent=1)
print(riga)
print('GEN42_FAILED' if errors else 'GEN42_OK')
sys.exit(1 if errors else 0)
