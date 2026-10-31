"""Generatore del blocco 4.7 (medaglie, Scheda Allenatore e icone del Pokegear).

Uso: python -I tools/generatori/4.7/gen47.py

Rilancia `tools/grafica/4.7/costruisci47.py` (pochi secondi), raccoglie il manifesto delle
tre parti e scrive `docs/MODULO_4/4.7_MEDAGLIE_ICONE.md` e `.json`. I testi fissi stanno
in text47.py.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
G47 = os.path.join(PROJ, 'tools', 'grafica', '4.7')
OUT_MD = os.path.join(PROJ, 'docs', 'MODULO_4', '4.7_MEDAGLIE_ICONE.md')
OUT_JSON = os.path.join(PROJ, 'docs', 'MODULO_4', '4.7_MEDAGLIE_ICONE.json')
sys.stdout.reconfigure(errors='backslashreplace')

sys.path.insert(0, HERE)
sys.path.insert(0, G47)
sys.path.insert(0, os.path.join(PROJ, 'tools'))
sys.path.insert(0, os.path.join(PROJ, 'tools', 'grafica', '4.4'))
sys.path.insert(0, os.path.join(PROJ, 'tools', 'grafica', '4.6'))

import trinacria_gfx as G          # noqa: E402
import medaglie47                  # noqa: E402
import icone47                     # noqa: E402
import costruisci47 as K           # noqa: E402
import text47 as T                 # noqa: E402

BUILD = os.path.join(PROJ, 'build', 'grafica', '4.7')
ANTE = os.path.join(BUILD, 'anteprime')

NOMI = {
    'liotru': ('Dossier Liotru', 'CT', 'elefante stilizzato su una base'),
    'aretusa': ('Dossier Aretusa', 'SR', 'la fonte con l\'acqua che zampilla'),
    'carrubba': ('Dossier Carrubba', 'RG', 'il baccello di carrubo coi semi'),
    'pirrera': ('Dossier Pirrera', 'CL', 'i gradoni della cava'),
    'telamuni': ('Dossier Telamuni', 'AG', 'il telamone, la colonna del tempio'),
    'mulinu': ('Dossier Mulinu', 'TP', 'il mulino a vento con le pale'),
    'pilunu': ('Dossier Pilunu', 'ME', 'i piloni dello Stretto'),
    'geniu': ('Dossier Geniu', 'PA', 'l\'arco del Genio con la lampada'),
    'cerere': ('Dossier Cerere', 'EN', 'la spiga di grano'),
}


def main(argv=None):
    if K.main([]) != 0:
        print('costruzione fallita: il documento non si scrive')
        return 1

    repo = K.repo_hg()
    medaglie, _ = medaglie47.costruisci(repo, BUILD)
    icone = icone47.costruisci(repo, BUILD)
    ritratti, _ = K.ritratti_scheda()

    for m in medaglie:
        m['dossier'], m['provincia'], m['descrizione'] = NOMI[m['emblema']]

    riga = T.riga_finale(len(medaglie), len(ritratti), icone['pixel_cambiati'])

    md = [T.INTESTAZIONE.format(versione=T.VERSIONE, data=T.DATA), T.IN_BREVE,
          T.COSTRUZIONE, T.FORMATI]
    md.append(T.MEDAGLIE)
    for m in medaglie:
        md.append('| %d | %s | %s | `%s` | %d | %d | %s |\n' % (
            m['slot'], m['dossier'], m['provincia'], m['alias'], m['slot'], m['voce'],
            m['descrizione']))
    md.append('\n')
    md.append(T.ICONE.format(seg0=icone['slot_segnalino'][0], seg1=icone['slot_segnalino'][1],
                             vag0=icone['slot_vagante'][0], vag1=icone['slot_vagante'][1]))
    md.append(T.RITRATTI)
    for r in ritratti:
        md.append('| `%s` | %dx%d | `%s` |\n' % (r['scheda'], r['misure'][0], r['misure'][1],
                                                os.path.relpath(r['file'], PROJ).replace('\\', '/')))
    md.append('\n')
    md.append(T.REGOLE)
    md.append(T.PROVE)
    md.append(T.APERTI)
    md.append(T.CHIUSURA)
    md.append('---\n\n`%s`\n' % riga)

    os.makedirs(os.path.dirname(OUT_MD), exist_ok=True)
    with open(OUT_MD, 'w', encoding='utf-8') as fh:
        fh.write(''.join(md))

    dati = {
        'modulo': 4,
        'blocco': '4.7',
        'titolo': 'Medaglie, Scheda Allenatore e icone del Pokegear',
        'versione': T.VERSIONE,
        'data': T.DATA,
        'progetto': 'Pokemon Trinacria',
        'documento': 'docs/MODULO_4/4.7_MEDAGLIE_ICONE.md',
        'lettore': 'Modulo 6 (consegna delle medaglie con GiveBadge), Modulo 7 (7.4, prova a schermo)',
        'file': [
            {'destinazione': 'files/a/0/4/9', 'byte': 335464,
             'nota': 'sedici voci delle medaglie della Scheda Allenatore; il blocco ne riscrive nove'},
            {'destinazione': icone['file'], 'byte': icone['byte'],
             'sha1_hg': icone['sha1_hg'], 'sha1_nuovo': icone['sha1_nuovo'],
             'nota': 'segnalino del protagonista e icona del vagante nello slot 2'},
        ],
        'medaglie': medaglie,
        'icone': {k: v for k, v in icone.items() if k != 'sorgente'},
        'ritratti_protagonista': ritratti,
        'regole': [
            {'id': 'R-GFX-42', 'testo': 'Le medaglie dei Dossier sono nove (voci 62-69 e 77 di a/0/4/9); ogni emblema riusa i colori gia presenti nella voce.'},
            {'id': 'R-GFX-43', 'testo': 'Le sette medaglie di Kanto (slot 8-14) restano quelle di HeartGold: il gioco non le consegna.'},
            {'id': 'R-GFX-44', 'testo': 'Il foglio delle icone del Pokegear si modifica solo per figura, lasciando forma e palette invariate.'},
        ],
        'prove': {'costruzione': 'GRAFICA_OK', 'medaglie': 'MEDAGLIE_OK', 'icone': 'ICONE_OK'},
        'punti_aperti': [
            'La voce esatta del ritratto nella Scheda Allenatore va confermata a schermo (7.4).',
            'La posizione delle due figure del foglio delle icone va guardata a schermo (7.4).',
            'Le sette medaglie di Kanto restano di HeartGold per R-GFX-43.',
        ],
        'riga_finale': riga,
    }
    with open(OUT_JSON, 'w', encoding='utf-8') as fh:
        json.dump(dati, fh, ensure_ascii=False, indent=1)
        fh.write('\n')

    print('scritti %s e %s' % (os.path.basename(OUT_MD), os.path.basename(OUT_JSON)))
    print(riga)
    print('BLOCCO_47_OK')
    return 0


if __name__ == '__main__':
    sys.exit(main())
