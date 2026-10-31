"""Blocco 4.7 - costruzione (medaglie, Scheda Allenatore, icone del Pokegear).

Uso: python -I tools/grafica/4.7/costruisci47.py
Esito: GRAFICA_OK

R-GFX-17: gli script di disegno di un blocco stanno in `tools/grafica/<blocco>/`.
Il blocco 4.7 non riscrive nulla del 4.6: ne riusa il figurino (`figura46.ritratto`) e le
schede (`schede46.SCHEDE`), come chiede la traccia della richiesta 4.7.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, os.path.join(PROJ, 'tools'))
sys.path.insert(0, os.path.join(PROJ, 'tools', 'grafica', '4.4'))
sys.path.insert(0, os.path.join(PROJ, 'tools', 'grafica', '4.6'))
sys.path.insert(0, HERE)
sys.stdout.reconfigure(errors='backslashreplace')

import trinacria_gfx as G          # noqa: E402
import comune44 as C44             # noqa: E402
import comune46 as C46             # noqa: E402
import figura46 as F46             # noqa: E402
import schede46 as S46             # noqa: E402
import medaglie47                  # noqa: E402
import icone47                     # noqa: E402

BUILD = os.path.join(PROJ, 'build', 'grafica', '4.7')
ANTE = os.path.join(BUILD, 'anteprime')
PROTAGONISTI = ('PROTAGONISTA_RAGAZZO', 'PROTAGONISTA_RAGAZZA')


def repo_hg():
    for c in (os.environ.get('TRINACRIA_REPO'), os.path.join(PROJ, '..', 'pokeheartgold'),
              r'F:\Progetti\pokeheartgold'):
        if c and os.path.isdir(c):
            return c
    raise G.GfxError('K00', 'repository di HeartGold non trovato')


def ritratti_scheda():
    """I due ritratti 96x64 del protagonista per la Scheda Allenatore."""
    errori = []
    voci = []
    for nome in PROTAGONISTI:
        s = S46.SCHEDE[nome]
        pix = F46.ritratto(s, 1, 'sorriso')
        pal = C46.palette(s)
        if len(pix) != 96 * 64:
            errori.append('K40 %s: %d pixel invece di %d' % (nome, len(pix), 96 * 64))
            continue
        path = os.path.join(ANTE, 'scheda_%s.png' % nome.lower())
        C44.salva_png(path, 96, 64, pal, pix, bpp=4)
        voci.append({'scheda': nome, 'misure': [96, 64], 'file': path,
                     'sha1': G.sha1(open(path, 'rb').read())})
    return voci, errori


def main(argv=None):
    repo = repo_hg()
    errori = []

    print('1. medaglie dei 9 Dossier (voce 62-69 e 77 del NARC a/0/4/9)')
    try:
        medaglie, dest = medaglie47.costruisci(repo, BUILD)
        medaglie47.anteprime(medaglie, ANTE, BUILD)
        print('   %d medaglie riscritte' % len(medaglie))
    except Exception as e:                       # noqa: BLE001
        medaglie = []
        errori.append('medaglie: %s' % e)

    print('2. icone del Pokegear (segnalino e vagante nello slot 2)')
    try:
        icone = icone47.costruisci(repo, BUILD)
        icone47.anteprima(icone, os.path.join(ANTE, 'pgmap_icone.png'))
        print('   %d pixel cambiati' % icone['pixel_cambiati'])
    except Exception as e:                       # noqa: BLE001
        icone = {}
        errori.append('icone: %s' % e)

    print('3. ritratti del protagonista per la Scheda Allenatore')
    ritratti, err = ritratti_scheda()
    errori += err
    print('   %d ritratti' % len(ritratti))

    for e in errori:
        print('ERRORE', e)
    if errori:
        print('GRAFICA_FAILED')
        return 1
    print('GRAFICA_OK')
    return 0


if __name__ == '__main__':
    sys.exit(main())
