"""Incontro: ragazze, belle, bagnanti."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from notazione import Brano, Giro  # noqa: E402

SIMBOLO = 'SEQ_TRN_INCONTRO_RAGAZZA'
BANCO = 'BANK_BASIC'
VOLUME = 84
SCHEDA = {
    'titolo': 'Incontro — ragazze',
    'carattere': 'grazioso e un po\' civettuolo: vibrafono e flauto all\'unisono, ritmo puntato '
                 'leggero, Fa maggiore',
    'tonalita': 'Fa maggiore',
    'forma': 'introduzione di 1 battuta; ritornello di 8 battute',
}

INTRO = Giro('F')
GIRO = Giro('F | Dm | Bb | C | F | Dm | Gm C7 | F')

MELODIA = (
    '| c6/8 a5 f5 a5 c6/4 r | a5/4. c6/8 f6/4 c6 | d6/4. f6/8 a5/4 d6 | bb5/8 d6 f6 d6 bb5/4 f5 '
    '| g5/4 c6 e6 g6 | f6/4. e6/8 c6/4 a5 | a5/8 d6 f6 d6 a5/4 f5 | g5/4 bb5 c6 e6 | f6/2. r/4 |'
)


def partitura(A):
    b = Brano(A, bpm=148)
    vb = b.voce('vibrafono', 5, volume=110, pan=64)
    fl = b.voce('flauto', 35, volume=70, pan=100)
    ap = b.voce('arpa', 26, volume=84, pan=30)
    bs = b.voce('basso', 19, volume=106, pan=64)
    bt = b.voce('batteria', 39, volume=84, pan=40)
    vb.suona(MELODIA, da=0, vel=100)
    fl.suona(MELODIA, da=0, vel=90)
    giro = INTRO + GIRO
    ap.arpeggi(giro, '1 5 8 10 12 10 8 5', da=0, registro=(53, 79), vel=70)
    bs.basso(giro, '1 - - 5 1 - 5 -', da=0, registro=(29, 48))
    bt.batteria({'bordo': '..x...x.', 'hh': 'o.o.o.o.', 'triangolo': 'x.......'}, da=1, battute=8)
    b.ritornello(1, 9)
    return b.fine()
