"""La zolfara di Gabbara, i valloni della SS626 e il cantiere del Viadotto Salso 2."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from notazione import Brano, Giro  # noqa: E402

SIMBOLO = 'SEQ_CL_ZOLFARA_VALLONI'
BANCO = 'BANK_BGM_DUNGEON6'
VOLUME = 79
SCHEDA = {
    'titolo': 'La zolfara',
    'carattere': 'gallerie di zolfo e valloni senza strada: modo frigio di Mi (il Fa accanto al Mi), '
                 'ostinato grave di fagotto, colpi di piccone sul legnetto e sui tamburi, archi '
                 'scuri; sopra, un lamento d\'ancia per i «carusi» che ci lavoravano da bambini',
    'tonalita': 'Mi frigio (parte B in La minore)',
    'forma': 'introduzione di 2 battute (fagotto e picconi); ritornello A (8) + B (8)',
}

INTRO = Giro('Em | F')
A_ = Giro('Em | F | Em | F | Dm | C | F | E')
B_ = Giro('Am | G | F | E | Am | Dm | F | E7')

LAMENTO = (
    '| e5/2 g5/4 b5/4 | a5/2. f5/4 | g5/4 e5/4 b4/2 | c5/1 '
    '| d5/4 f5/4 a5/2 | g5/4. e5/8 c5/2 | f5/4 a5/4 c6/2 | b5/2 g#5/2 '
    '| c6/4 a5/4 e5/2 | d5/4. b4/8 g4/2 | a4/4 c5/4 f5/4 a5/4 | g#5/2 e5/2 '
    '| a5/4 c6/4 e6/2 | d6/4. a5/8 f5/2 | f5/4 a5/4 c6/4 a5/4 | g#5/2 d5/2 |'
)


def partitura(A):
    b = Brano(A, bpm=100)
    ob = b.voce('lamento', 33, volume=104, pan=64)
    fg = b.voce('fagotto', 36, volume=96, pan=48)
    cb = b.voce('contrabbasso', 25, volume=96, pan=64)
    ar = b.voce('archi', 23, volume=68, pan=88)
    bt = b.voce('picconi', 39, volume=80, pan=64)
    ob.suona(LAMENTO, da=2, vel=94)
    giro = INTRO + A_ + B_
    fg.arpeggi(giro, '1 . 1 5 1 . 8 .', da=0, registro=(40, 60), vel=84, gate=0.7)
    cb.basso(giro, '1 - - - 1 - - -', da=0)
    ar.accordi(A_ + B_, 'x-------', da=2, registro=(52, 67), vel=56)
    bt.batteria({'legnetto': 'x..x..x.', 'tom_b': 'x.......', 'tom_m': '......x.'}, da=0, battute=18)
    b.eco(ob, 'lamento eco', ritardo=24, volume=34)
    b.ritornello(2, 18)
    return b.fine()
