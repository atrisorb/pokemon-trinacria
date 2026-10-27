"""Vittoria su un Pokémon selvatico."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from notazione import Brano, Giro  # noqa: E402

SIMBOLO = 'SEQ_TRN_VITTORIA_SELVATICO'
BANCO = 'BANK_BASIC'
VOLUME = 110
SCHEDA = {
    'titolo': 'Vittoria su un selvatico',
    'carattere': 'più breve e leggera della vittoria sugli allenatori: un arpeggio di Sol in su, poi '
                 'una frase serena di tromba e flauto',
    'tonalita': 'Sol maggiore',
    'forma': 'introduzione di 1 battuta; ritornello di 8 battute',
}

INTRO = Giro('G')
GIRO = Giro('G | Em | C | D | G | Em | Am D7 | G')

MELODIA = (
    '| g5/8 b5 d6 g6 d6/4 r | b5/4. a5/8 g5/4 d5 | e5/4 g5/8 b5 e6/4 b5 | c6/4. b5/8 g5/4 e5 '
    '| d5/4 f#5 a5 d6 | d6/4. b5/8 g5/4 b5 | g5/4 e5/8 g5 b5/4 e6 | c6/4 a5 a5 f#5 | g5/2. r/4 |'
)


def partitura(A):
    b = Brano(A, bpm=150)
    tr = b.voce('tromba', 29, volume=116, pan=60)
    tr.suona(MELODIA, da=0, vel=102)
    b.eco(tr, 'flauto ottava', ritardo=0, volume=64, pan=100, trasponi=12, programma=35)
    ar = b.voce('archi', 23, volume=84, pan=20)
    bs = b.voce('basso', 25, volume=108, pan=100)
    bt = b.voce('batteria', 39, volume=92, pan=40)
    giro = INTRO + GIRO
    ar.accordi(giro, 'x---x---', da=0, registro=(55, 71), vel=68)
    bs.basso(giro, '1 . 5 . 1 . 5 .', da=0, registro=(31, 50))
    bt.batteria({'cassa': 'x...x...', 'rullante': '..x...x.', 'hh': 'o.o.o.o.'}, da=1, battute=8)
    b.ritornello(1, 9)
    return b.fine()
