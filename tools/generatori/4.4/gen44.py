"""Generatore del blocco 4.4 (titolo, copyright, Pokégear e Sondaggio).
Uso: python -I tools/generatori/4.4/gen44.py [--senza-costruzione]

Rilancia tools/grafica/4.4/costruisci44.py (pochi secondi), prova `trinacria_gfx.py applica --blocchi 4.4
--prova` in una cartella temporanea, poi scrive docs/MODULO_4/4.4_UI_TITOLO_POKEGEAR.md e
docs/MODULO_4/4.4_POKEGEAR.json dal manifesto. Testi fissi in text44.py.
"""
import json
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
G44 = os.path.join(PROJ, 'tools', 'grafica', '4.4')
BUILD = os.path.join(PROJ, 'build', 'grafica', '4.4')
OUT_MD = os.path.join(PROJ, 'docs', 'MODULO_4', '4.4_UI_TITOLO_POKEGEAR.md')
OUT_JSON = os.path.join(PROJ, 'docs', 'MODULO_4', '4.4_POKEGEAR.json')
sys.stdout.reconfigure(errors='backslashreplace')
sys.path.insert(0, HERE)
sys.path.insert(0, G44)
sys.path.insert(0, os.path.join(PROJ, 'tools'))
import trinacria_gfx as G  # noqa: E402
import costruisci44  # noqa: E402
import text44 as T  # noqa: E402

errors = []


def err(m):
    errors.append(m)
    print('ERRORE', m)


if '--senza-costruzione' not in sys.argv:
    print('costruzione (tools/grafica/4.4/costruisci44.py)…')
    if costruisci44.main([]) != 0:
        err('costruisci44: GRAFICA_FAILED')
man = json.load(open(os.path.join(BUILD, 'manifesto.json'), encoding='utf-8'))
repo = G.find_repo(None)

tmp = tempfile.mkdtemp(prefix='trn44_applica_')
try:
    e_ap, log_ap = G.applica_file(repo, os.path.dirname(BUILD), '4.4', tmp)
    for c, m in e_ap:
        err('applica %s %s' % (c, m))
    scritti = sum(len(fs) for _, _, fs in os.walk(tmp))
finally:
    shutil.rmtree(tmp, ignore_errors=True)
prova = dict(righe=log_ap, file_scritti=scritti)

pg = man['pokegear']
dati = {
    'modulo': 4, 'blocco': '4.4', 'titolo': 'Titolo, copyright, Pokégear e Sondaggio',
    'versione': '1.0', 'data': T.DATA, 'progetto': 'Pokémon Trinacria (autore: atrisorb)',
    'documento': 'docs/MODULO_4/4.4_UI_TITOLO_POKEGEAR.md',
    'lettore': 'Modulo 6 (ScrCmd_804 2, VAR_TRINACRIA_CONSENSO), blocco 4.5 (sprite), Modulo 7 (7.4: TASK a schermo)',
    'regioni': T.REGIONI_JSON,
    'tabella_volo': pg['volo'],
    'luoghi': pg['luoghi'],
    'mappe_senza_luogo': pg['escluse'],
    'piantine': pg['piantine'],
    'file': man['file'],
    'blocchi_testo': [{k: v for k, v in b.items() if k != 'testo'} for b in man['blocchi_testo']],
    'modifiche_codice': man['sostituzioni'],
    'sondaggio': man['sondaggio'],
    'copyright': man['copyright'],
    'titolo_schermata': man['titolo'],
    'prova_applica': prova,
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
