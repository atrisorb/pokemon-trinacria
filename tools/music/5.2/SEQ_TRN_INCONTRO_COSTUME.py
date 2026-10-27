"""Incontro: donne in costume tradizionale."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from notazione import Brano, Giro  # noqa: E402

SIMBOLO = 'SEQ_TRN_INCONTRO_COSTUME'
BANCO = 'BANK_BASIC'
VOLUME = 84
SCHEDA = {
    'titolo': 'Incontro — costume tradizionale',
    'carattere': 'tarantella in 6/8 in La minore: tamburello con l\'accento sul primo tempo, mandolino '
                 'arpeggiato, fisarmonica che gira veloce',
    'tonalita': 'La minore',
    'forma': 'introduzione di 1 battuta; ritornello di 8 battute, in 6/8',
}

INTRO = Giro('Am')
GIRO = Giro('Am | Am | Dm | E | Am | G | F E | Am')

MELODIA = (
    '| e5/8 a5 c6 e6/4 r/8 | a5/8 b5 c6 e6/4 c6/8 | c6/8 b5 a5 e5/4. | d5/8 f5 a5 d6/4 a5/8 '
    '| g#5/8 a5 b5 e5/4. | a5/8 c6 e6 a6/4 e6/8 | g6/8 f6 e6 d6/4 b5/8 | c6/8 a5 f5 b5/4 g#5/8 | a5/4. r/4. |'
)


def partitura(A):
    b = Brano(A, bpm=168, metro=(6, 8))
    fs = b.voce('fisarmonica', 13, volume=110, pan=64)
    md = b.voce('mandolino', 42, volume=88, pan=96)
    bs = b.voce('basso', 19, volume=106, pan=64)
    bt = b.voce('tamburello', 39, volume=92, pan=40)
    fs.suona(MELODIA, da=0, vel=100)
    giro = INTRO + GIRO
    md.arpeggi(giro, '1 5 8 5 10 8', da=0, registro=(57, 81), vel=74)
    bs.basso(giro, '1 . . 5 . .', da=0, registro=(33, 50))
    bt.batteria({'tamburello': 'Xooxoo', 'cassa': 'x.....'}, da=0, battute=9)
    b.ritornello(1, 9)
    return b.fine()
