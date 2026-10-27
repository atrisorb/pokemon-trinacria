"""Incontro: tipi loschi, giocolieri, secchioni, ladri."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from notazione import Brano, Giro  # noqa: E402

SIMBOLO = 'SEQ_TRN_INCONTRO_LOSCO'
BANCO = 'BANK_BASIC'
VOLUME = 73
SCHEDA = {
    'titolo': 'Incontro — tipi loschi',
    'carattere': 'passi in punta di piedi: scala cromatica in salita, clarinetto staccato che si '
                 'guarda intorno, pizzicato e spazzole',
    'tonalita': 'Mi minore',
    'forma': 'introduzione di 1 battuta; ritornello di 8 battute',
}

INTRO = Giro('B7')
GIRO = Giro('Em | Em | Am | B7 | Em | C | Am B7 | Em')

MELODIA = (
    "| e4/8' f4' f#4' g4' g#4' a4' a#4' b4' "
    "| e5/8' r g5' r b5/4 a#5/8 b5 | e5/8' r g5' r b5/2 | c6/8' r a5' r e5/4 d#5/8 e5 | f#5/4 d#5 a5 b4 "
    "| g5/8' r b5' r e6/4 d#6/8 e6 | e6/8' r c6' r g5/2 | a5/4 c6 b5 a5 | e5/2. r/4 |"
)


def partitura(A):
    b = Brano(A, bpm=132)
    cl = b.voce('clarinetto', 34, volume=112, pan=64)
    pz = b.voce('pizzicato', 17, volume=92, pan=30)
    bs = b.voce('contrabbasso', 25, volume=104, pan=64)
    bt = b.voce('batteria', 39, volume=78, pan=100)
    cl.suona(MELODIA, da=0, vel=98)
    giro = INTRO + GIRO
    pz.accordi(GIRO, '.x.x.x.x', da=1, registro=(52, 67), vel=68, gate=0.4)
    bs.basso(giro, '1 . 5 . 8 . 5 .', da=0, registro=(28, 47), gate=0.5)
    bt.batteria({'bordo': '..x...x.', 'hh': 'o.o.o.o.'}, da=1, battute=8)
    b.ritornello(1, 9)
    return b.fine()
