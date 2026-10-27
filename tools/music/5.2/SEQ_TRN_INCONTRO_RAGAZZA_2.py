"""Incontro: ragazzine, gemelle, escursioniste."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from notazione import Brano, Giro  # noqa: E402

SIMBOLO = 'SEQ_TRN_INCONTRO_RAGAZZA_2'
BANCO = 'BANK_BASIC'
VOLUME = 97
SCHEDA = {
    'titolo': 'Incontro — ragazzine',
    'carattere': 'girotondo in 6/8: celesta e flauto dolce, saltelli di sesta, come una filastrocca',
    'tonalita': 'Do maggiore',
    'forma': 'introduzione di 1 battuta; ritornello di 8 battute, in 6/8',
}

INTRO = Giro('C')
GIRO = Giro('C | Am | F | G | C | Am | Dm G | C')

MELODIA = (
    '| g5/8 c6 e6 g6/4 r/8 | e6/4 c6/8 g5/4 c6/8 | a5/4 c6/8 e6/4 c6/8 | f5/8 a5 c6 f6/4 c6/8 '
    '| d6/4 b5/8 g5/4. | c6/8 e6 g6 e6/4 c6/8 | a5/8 c6 e6 a6/4 e6/8 | f6/4 d6/8 b5/4 d6/8 | c6/4. r/4. |'
)


def partitura(A):
    b = Brano(A, bpm=168, metro=(6, 8))
    ce = b.voce('celesta', 27, volume=110, pan=64)
    fd = b.voce('flauto dolce', 38, volume=84, pan=100)
    pz = b.voce('pizzicato', 16, volume=84, pan=30)
    bs = b.voce('basso', 19, volume=104, pan=64)
    bt = b.voce('batteria', 39, volume=80, pan=40)
    ce.suona(MELODIA, da=0, vel=100)
    fd.suona(MELODIA, da=0, vel=86, trasponi=-12)
    giro = INTRO + GIRO
    pz.accordi(giro, '.xx.xx', da=0, registro=(55, 70), vel=66, gate=0.5)
    bs.basso(giro, '1 . . 5 . .', da=0, registro=(31, 50))
    bt.batteria({'legnetto': 'x..x..', 'triangolo': '.....o'}, da=1, battute=8)
    b.ritornello(1, 9)
    return b.fine()
