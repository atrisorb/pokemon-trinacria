"""Acireale barocca e la Timpa (S-CT-02, S-CT-03)."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from notazione import Brano, Giro  # noqa: E402

SIMBOLO = 'SEQ_CT_ACIREALE'
BANCO = 'BANK_BGM_FIELD8'
VOLUME = 72
SCHEDA = {
    'titolo': 'Acireale',
    'carattere': 'piazze barocche di pietra bianca e la discesa della Timpa: minuetto in 3/4 con continuo '
                 'di tastiera, archi e flauto; nella parte B il tamburello ricorda il Carnevale acese',
    'tonalita': 'Fa maggiore',
    'forma': 'introduzione di 2 battute (continuo); ritornello A (8) + B (8) in Fa maggiore, poi le stesse 16 battute in Si bemolle (il «trio» alla sottodominante), in 3/4',
}

INTRO = Giro('F | C7')
A_ = Giro('F | Bb | C | F | Dm | G7 | C | C7')
B_ = Giro('F | Dm | Bb | C | Am | Dm | Gm | C7')

MELODIA = (
    '| c6/4 a5/8 bb5 c6/4 | d6/4 bb5 f5 | e5/8 f5 g5/4 c6 | a5/2. '
    '| d6/4 f6/8 e6 d6/4 | b5/4 g5 d6 | e6/4 c6 g5 | bb5/2 g5/4 '
    '| a5/4 c6/8 a5 f5/4 | f5/4 a5 d6 | d6/8 c6 bb5/4 f5 | e5/4 g5 c6 '
    '| c6/4 e6/8 c6 a5/4 | a5/4 f5 d5 | g5/4 bb5 d6 | c6/4 bb5 e5 |'
)


def partitura(A):
    b = Brano(A, bpm=132, metro=(3, 4))
    fl = b.voce('flauto', 35, volume=108, pan=64)
    cb = b.voce('continuo', 2, volume=92, pan=36)
    ar = b.voce('archi', 23, volume=76, pan=96)
    vc = b.voce('violoncello', 25, volume=100, pan=64)
    pc = b.voce('tamburello', 39, volume=72, pan=90)
    fl.suona(MELODIA, da=2, vel=96)
    giro = INTRO + A_ + B_
    cb.arpeggi(giro, '1 5 8 5 10 5', da=0, registro=(48, 76), vel=72)
    ar.accordi(A_ + B_, '.xx', da=2, registro=(57, 72), vel=58, gate=0.7)
    vc.basso(giro, '1 . .', da=0, gate=0.8)
    pc.batteria({'tamburello': 'xoo'}, da=10, battute=8)
    b.ripeti(2, 16, 18, trasponi=-7)
    b.ritornello(2, 34)
    return b.fine()
