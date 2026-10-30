"""Generatore del blocco 4.6 (immagini di lotta e transizioni).
Uso: python -I tools/generatori/4.6/gen46.py [--senza-costruzione]

Rilancia tools/grafica/4.6/costruisci46.py (una decina di secondi), prova `trinacria_gfx.py applica --blocchi 4.6
--prova` in una cartella temporanea, poi scrive docs/MODULO_4/4.6_IMMAGINI_DI_LOTTA.md e
docs/MODULO_4/4.6_IMMAGINI_DI_LOTTA.json dal manifesto. Testi fissi in text46.py.
"""
import json
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
G46 = os.path.join(PROJ, 'tools', 'grafica', '4.6')
BUILD = os.path.join(PROJ, 'build', 'grafica', '4.6')
OUT_MD = os.path.join(PROJ, 'docs', 'MODULO_4', '4.6_IMMAGINI_DI_LOTTA.md')
OUT_JSON = os.path.join(PROJ, 'docs', 'MODULO_4', '4.6_IMMAGINI_DI_LOTTA.json')
sys.stdout.reconfigure(errors='backslashreplace')
sys.path.insert(0, HERE)
sys.path.insert(0, G46)
sys.path.insert(0, os.path.join(PROJ, 'tools'))
import trinacria_gfx as G  # noqa: E402
import costruisci46  # noqa: E402
import figura46 as F  # noqa: E402
import schede46 as S  # noqa: E402
import text46 as T  # noqa: E402

errors = []


def err(m):
    errors.append(m)
    print('ERRORE', m)


if '--senza-costruzione' not in sys.argv:
    print('costruzione (tools/grafica/4.6/costruisci46.py)…')
    if costruisci46.main([]) != 0:
        err('costruisci46: GRAFICA_FAILED')
man = json.load(open(os.path.join(BUILD, 'manifesto.json'), encoding='utf-8'))
repo = G.find_repo(None)

tmp = tempfile.mkdtemp(prefix='trn46_applica_')
try:
    e_ap, log_ap = G.applica_file(repo, os.path.dirname(BUILD), '4.6', tmp)
    for c, m in e_ap:
        err('applica %s %s' % (c, m))
    scritti = sum(len(fs) for _, _, fs in os.walk(tmp))
finally:
    shutil.rmtree(tmp, ignore_errors=True)
prova = dict(righe=log_ap, file_scritti=scritti)

dati = {
    'modulo': 4, 'blocco': '4.6', 'titolo': 'Immagini di lotta e transizioni',
    'versione': '1.0', 'data': T.DATA, 'progetto': 'Pokémon Trinacria (autore: atrisorb)',
    'documento': 'docs/MODULO_4/4.6_IMMAGINI_DI_LOTTA.md',
    'lettore': 'Modulo 6 (nomi degli allenatori nelle transizioni), blocco 4.7, Modulo 7 (7.2 modifica E-GFX-05, 7.4)',
    'ruoli_palette': T.RUOLI,
    'fronti': man['fronti'], 'dorsi': man['dorsi'], 'ritratti': man['ritratti'], 'timbri': man['timbri'],
    'fasi_dorso': [dict(fase=k, gomito=list(g), mano=list(m), palla=p) for k, (g, m, p) in enumerate(F.RETRO_FASI)],
    'pose': [dict(posa=a, descrizione=b) for a, b in S.DESCRIZIONE_POSE],
    'modifica_codice': man['sostituzioni'],
    'file': man['file'],
    'prova_forma': man['prova_forma'],
    'prova_applica': prova,
    'anteprime': man['anteprime'],
}
riga = T.riga_finale(man)
dati['riga_finale'] = riga
with open(OUT_JSON, 'w', encoding='utf-8', newline='\n') as fh:
    json.dump(dati, fh, ensure_ascii=False, indent=1)
    fh.write('\n')
md = T.documento(man, prova, riga)
with open(OUT_MD, 'w', encoding='utf-8', newline='\n') as fh:
    fh.write(md)
print('%s (%d byte), %s (%d byte)' % (OUT_MD, len(md.encode('utf-8')), OUT_JSON, os.path.getsize(OUT_JSON)))
print(riga)
print('GENERATORE_FAILED' if errors else 'GENERATORE_OK')
sys.exit(1 if errors else 0)
