"""Generatore del blocco 4.3 (tileset e modelli 3D di AG, TP, PA, EN, ME).
Uso (Windows, serve g3dcvtr): python -I tools/generatori/4.3/gen43.py [--senza-costruzione]

Rilancia tools/grafica/4.3/costruisci43.py (alcuni minuti), prova `trinacria_gfx.py applica --blocchi 4.2 4.3
--prova` in una cartella temporanea (serve anche build/grafica/4.2, cioè costruisci42.py già eseguito), poi
scrive docs/MODULO_4/4.3_TILESET_OVEST.md e docs/MODULO_4/4.3_CELLE_OVEST.json dal manifesto. Testi fissi
in text43.py.
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
G43 = os.path.join(PROJ, 'tools', 'grafica', '4.3')
BUILD = os.path.join(PROJ, 'build', 'grafica', '4.3')
BUILD42 = os.path.join(PROJ, 'build', 'grafica', '4.2')
OUT_MD = os.path.join(PROJ, 'docs', 'MODULO_4', '4.3_TILESET_OVEST.md')
OUT_JSON = os.path.join(PROJ, 'docs', 'MODULO_4', '4.3_CELLE_OVEST.json')
sys.stdout.reconfigure(errors='backslashreplace')
sys.path.insert(0, HERE)
sys.path.insert(0, G43)
sys.path.insert(0, os.path.join(PROJ, 'tools'))
import trinacria_gfx as G  # noqa: E402
import costruisci43  # noqa: E402
import mondo43  # noqa: E402
import esterni43  # noqa: E402
import interni43  # noqa: E402
import tex42  # noqa: E402
import tex43  # noqa: E402
import texint43  # noqa: E402
import text43 as T  # noqa: E402

errors = []


def err(m):
    errors.append(m)
    print('ERRORE', m)


if '--senza-costruzione' not in sys.argv:
    print('costruzione (tools/grafica/4.3/costruisci43.py)…')
    if costruisci43.main([]) != 0:
        err('costruisci43: GRAFICA_FAILED')
man = json.load(open(os.path.join(BUILD, 'manifesto.json'), encoding='utf-8'))
man42 = json.load(open(os.path.join(BUILD42, 'manifesto.json'), encoding='utf-8'))

# prova di applica (4.2 e 4.3 insieme) in una cartella temporanea
tmp = tempfile.mkdtemp(prefix='trn43_applica_')
try:
    e_ap, log_ap = G.applica(REPO, ['4.2', '4.3'], os.path.dirname(BUILD), None, tmp)
    for c, m in e_ap:
        err('applica %s %s' % (c, m))
    land = G.Narc(G.read(os.path.join(tmp, 'files', 'a', '0', '6', '5'))).files
    aree = G.area_entries(G.read(os.path.join(tmp, 'files', 'a', '0', '4', '2')))
    tiles = G.Narc(G.read(os.path.join(tmp, 'files', 'a', '0', '4', '4'))).files
    m0 = G.matrix_parse(G.read(os.path.join(tmp, 'files', 'fielddata', 'mapmatrix', 'map_matrix',
                                             'map_matrix_0000_EVERYWHERE.bin')))
    # ogni cella della matrice 0 dei due blocchi: voce giusta, texture nel tileset condiviso ricostruito
    ts_sic = tiles[106]
    k20 = {'4.2': 0, '4.3': 0}
    for blocco, mm in (('4.2', man42), ('4.3', man)):
        for c in mm['matrice_0']:
            v = m0['modelli'][c['y'] * 47 + c['x']]
            if v != c['voce']:
                err('applica: matrice 0 (%d,%d) = %d invece di %d' % (c['x'], c['y'], v, c['voce']))
            if G.texture_mancanti(G.land_split(land[v])['modello'], ts_sic):
                k20[blocco] += 1
    if any(k20.values()):
        err('K20: celle della matrice 0 con texture assenti nel tileset condiviso: %s' % k20)
    for a in man['aree']:
        x = aree[a['indice']]
        if (x['tex_mappa'], x['tex_edifici'], x['esterno'], x['luce']) != (a['tileset'], a['tex_edifici'], a['esterno'], a['luce']):
            err('applica: area %s scritta diversa' % a['chiave'])
    if aree[106]['tex_mappa'] != 106 or tiles[106] != G.read(os.path.join(BUILD, 'tileset', 'sicilia.nsbtx')):
        err('applica: il tileset condiviso 106 non è quello ricostruito dal 4.3')
    prova = {'righe': log_ap, 'voci_a065': len(land), 'voci_a044': len(tiles), 'voci_a042': len(aree),
             'k20_matrice_0': k20}
finally:
    shutil.rmtree(tmp, ignore_errors=True)

# --------------------------------------------------------------------------- dati per il documento
w = mondo43.Mondo()
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
blds = G.Narc(G.originale(REPO, 'a/0/7/0')).files
b_sic = G.read(os.path.join(BUILD, ts_sic['file']))
b_int = G.read(os.path.join(BUILD, ts_int['file']))
vram_sic = sum(G.tex_bytes(b_sic)) + sum(G.tex_bytes(blds[costruisci43.TEX_EDIFICI_CENTRO]))
vram_int = sum(G.tex_bytes(b_int)) + sum(G.tex_bytes(blds[costruisci43.TEX_EDIFICI_CENTRO]))
ing = man['ingressi']['file']
mappe_area = collections.Counter(m['area'] for m in man['mappe'])
b42 = man42['tileset'][0]['byte']

dati = dict(man=man, man42=man42, w=w, est=est, pae=pae, inte=inte, coll=coll, n_varchi=n_varchi, n_punti=n_punti,
            pol=pol, vram_sic=vram_sic, vram_int=vram_int, ing=ing, mappe_area=mappe_area, prova=prova,
            temi=esterni43.TEMI, temi42=('citta_ct', 'periferia', 'paese_etna', 'etna', 'costa_lavica', 'barocco', 'paese',
                                          'spiaggia', 'industria', 'campagna', 'nisseno', 'calanchi', 'bosco', 'strada',
                                          'strada_etna', 'strada_costa', 'strada_calanchi'),
            preset=interni43.PRESET, sic42=tex42.SICILIA_4_2, sic43=tex43.SICILIA_4_3, intx=texint43.INTERNI_4_3_NUOVE,
            limiti=G.LIMITI, b_sic=len(b_sic), b_int=len(b_int), b42=b42, nomi_int=ts_int['nomi'])
md = T.documento(dati)
riga = T.riga_finale(dati)
md += '\n## 14. Riga di controllo\n\n`%s`\n' % riga
with open(OUT_MD, 'w', encoding='utf-8', newline='\n') as fh:
    fh.write(md)

out = {
    'modulo': 4, 'blocco': '4.3', 'titolo': 'Tileset e modelli 3D di Agrigento, Trapani, Palermo, Enna e Messina',
    'versione': '1.0', 'data': '27/10/2026', 'progetto': 'Pokémon Trinacria (autore: atrisorb)',
    'documento': 'docs/MODULO_4/4.3_TILESET_OVEST.md',
    'lettore': 'Modulo 6 (warp, punti, oggetti nelle mappe), 7.4 (TASK)',
    'numerazione': {'prima_cella_a065': man['prima_cella'], 'ultima_cella_a065': man['prima_cella'] + len(celle) - 1,
                    'tileset_a044': {t['chiave']: t['indice'] for t in man['tileset']},
                    'aree_a042': {a['chiave']: a['indice'] for a in man['aree']},
                    'prossima_cella': man['prima_cella'] + len(celle),
                    'prossimo_tileset': man['primo_tileset'] + 1, 'prossima_area': man['prima_area'] + len(man['aree'])},
    'tileset': [{k: v for k, v in t.items()} for t in man['tileset']], 'aree': man['aree'],
    'celle': [{k: c[k] for k in ('chiave', 'voce', 'mappa', 'titolo', 'tileset', 'poligoni', 'byte_voce')} for c in celle],
    'matrice_0': man['matrice_0'], 'matrici': man['matrici'], 'mappe': man['mappe'],
    'varchi': man['varchi'], 'collegamenti': coll, 'collegamenti_modulo_6': man['collegamenti_modulo_6'],
    'punti': man['punti'], 'ingressi': man['ingressi'], 'prova_applica': prova, 'riga_finale': riga,
}
with open(OUT_JSON, 'w', encoding='utf-8', newline='\n') as fh:
    json.dump(out, fh, ensure_ascii=False, indent=1)
print(riga)
print('GEN43_FAILED' if errors else 'GEN43_OK')
sys.exit(1 if errors else 0)
