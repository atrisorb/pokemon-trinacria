"""Gela, Niscemi e la Sughereta."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from notazione import Brano, Giro  # noqa: E402

SIMBOLO = 'SEQ_CL_GELA_NISCEMI'
BANCO = 'BANK_BGM_FIELD16'
VOLUME = 85
SCHEDA = {
    'titolo': 'Gela e la Sughereta',
    'carattere': 'in cammino fra le mura greche di Gela, la raffineria sul mare e il bosco di '
                 'sughere di Niscemi: brano di strada deciso, flauto con l\'eco, accordi di tastiera '
                 'in levare, basso elettrico e batteria piena',
    'tonalita': 'La minore',
    'forma': 'introduzione di 2 battute (batteria e basso); ritornello A (8) + B (8)',
}

INTRO = Giro('Am | G')
A_ = Giro('Am | F | C | G | Am | F | Dm | E')
B_ = Giro('F | G | Em | Am | F | G | Am | E7')

MELODIA = (
    '| a5/4 e5/8 a5/8 c6/4 e6/4 | f6/4. e6/8 c6/2 | e6/4 c6/4 g5/4 c6/4 | d6/2 b5/2 '
    '| c6/4 a5/4 e5/4 a5/4 | c6/4. a5/8 f5/2 | f5/4 a5/4 d6/4 f6/4 | e6/2 g#5/2 '
    '| a5/4 c6/4 f6/2 | d6/4 b5/4 g5/2 | g5/4 b5/4 e6/4. d6/8 | c6/2 a5/2 '
    '| f5/4 a5/4 c6/4 f6/4 | g6/4. f6/8 d6/2 | e6/4 c6/4 a5/4 c6/4 | b5/2 g#5/2 |'
)


def partitura(A):
    b = Brano(A, bpm=140)
    fl = b.voce('flauto', 35, volume=110, pan=64)
    ac = b.voce('accordi', 3, volume=72, pan=40)
    bs = b.voce('basso', 22, volume=100, pan=64)
    bt = b.voce('batteria', 39, volume=80, pan=64)
    fl.suona(MELODIA, da=2, vel=98)
    giro = INTRO + A_ + B_
    ac.accordi(A_ + B_, '.x.x.x.x', da=2, registro=(55, 70), vel=62, gate=0.6)
    bs.basso(giro, '1 . 8 . 1 . 5 .', da=0)
    bt.batteria({'cassa': 'x...x...', 'rullante': '..x...x.', 'hh': 'xxxxxxxx'}, da=0, battute=18)
    b.eco(fl, 'flauto eco', ritardo=12, volume=38)
    b.ritornello(2, 18)
    return b.fine()
