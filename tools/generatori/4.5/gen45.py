"""Generatore del blocco 4.5 (sprite di campo dei personaggi).
Uso: python -I tools/generatori/4.5/gen45.py [--senza-costruzione]

Rilancia tools/grafica/4.5/costruisci45.py (pochi secondi), prova `trinacria_gfx.py applica --blocchi 4.5
--prova` in una cartella temporanea, poi scrive docs/MODULO_4/4.5_SPRITE_PERSONAGGI.md e
docs/MODULO_4/4.5_SPRITE_PERSONAGGI.json dal manifesto. Testi fissi in text45.py.
"""
import json
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
G45 = os.path.join(PROJ, 'tools', 'grafica', '4.5')
BUILD = os.path.join(PROJ, 'build', 'grafica', '4.5')
OUT_MD = os.path.join(PROJ, 'docs', 'MODULO_4', '4.5_SPRITE_PERSONAGGI.md')
OUT_JSON = os.path.join(PROJ, 'docs', 'MODULO_4', '4.5_SPRITE_PERSONAGGI.json')
sys.stdout.reconfigure(errors='backslashreplace')
sys.path.insert(0, HERE)
sys.path.insert(0, G45)
sys.path.insert(0, os.path.join(PROJ, 'tools'))
import trinacria_gfx as G  # noqa: E402
import costruisci45  # noqa: E402
import schede45 as S  # noqa: E402
import text45 as T  # noqa: E402

errors = []


def err(m):
    errors.append(m)
    print('ERRORE', m)


if '--senza-costruzione' not in sys.argv:
    print('costruzione (tools/grafica/4.5/costruisci45.py)…')
    if costruisci45.main([]) != 0:
        err('costruisci45: GRAFICA_FAILED')
man = json.load(open(os.path.join(BUILD, 'manifesto.json'), encoding='utf-8'))
repo = G.find_repo(None)

tmp = tempfile.mkdtemp(prefix='trn45_applica_')
try:
    e_ap, log_ap = G.applica_file(repo, os.path.dirname(BUILD), '4.5', tmp)
    for c, m in e_ap:
        err('applica %s %s' % (c, m))
    scritti = sum(len(fs) for _, _, fs in os.walk(tmp))
finally:
    shutil.rmtree(tmp, ignore_errors=True)
prova = dict(righe=log_ap, file_scritti=scritti)

tabelle = {n: {str(k): v for k, v in sorted(S.tabella(n).items())}
           for n in ('cammina16', 'eroe32', 'bici24', 'surf4', 'pesca16', 'scala6', 'salva2', 'banzai12', 'spinta8')}
dati = {
    'modulo': 4, 'blocco': '4.5', 'titolo': 'Sprite di campo dei personaggi',
    'versione': '1.0', 'data': T.DATA, 'progetto': 'Pokémon Trinacria (autore: atrisorb)',
    'documento': 'docs/MODULO_4/4.5_SPRITE_PERSONAGGI.md',
    'lettore': 'Modulo 6 (spriteId degli eventi: SPRITE_TRN_*), blocco 4.6 (immagini di lotta), Modulo 7 (7.4)',
    'ruoli_palette': T.RUOLI,
    'personaggi': man['personaggi'],
    'protagonista': {'schede': man['schede_protagonista'], 'sprite': man['protagonista'],
                     'restano_di_heartgold': man['non_usati']},
    'tabelle_fotogrammi': tabelle,
    'file': man['file'],
    'prova_forma': man['prova_forma'],
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
