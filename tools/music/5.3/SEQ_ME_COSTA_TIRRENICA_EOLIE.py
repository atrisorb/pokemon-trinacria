"""La costa tirrenica messinese e le Eolie: Sant'Agata, Capo d'Orlando, Patti e Tindari,
Barcellona, Milazzo e le Isole Eolie."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from notazione import Brano, Giro  # noqa: E402

SIMBOLO = 'SEQ_ME_COSTA_TIRRENICA_EOLIE'
BANCO = 'BANK_BGM_FIELD12'
VOLUME = 80
SCHEDA = {
    'titolo': 'La costa tirrenica e le Eolie',
    'carattere': 'la lunga costa nord con le isole vulcaniche all\'orizzonte: brano di strada '
                 'luminoso e svelto, tromba con l\'eco che apre gli spazi, archi, basso che salta '
                 'd\'ottava e batteria piena',
    'tonalita': 'La maggiore',
    'forma': 'introduzione di 2 battute (batteria e basso); ritornello A (8) + B (8)',
}

INTRO = Giro('A | E')
A_ = Giro('A | E | F#m | D | A | E | D E | A')
B_ = Giro('D | E | C#m | F#m | Bm | E | D | E7')

MELODIA = (
    '| e5/4 a5/8 b5/8 c#6/4 e6/4 | b5/4. g#5/8 e5/2 | f#5/4 a5/4 c#6/4 a5/4 | d6/2 a5/2 '
    '| c#6/4 e6/4 a6/4. e6/8 | g#6/4 e6/4 b5/2 | a5/4 f#5/4 g#5/4 b5/4 | a5/2. r/4 '
    '| f#5/4 a5/4 d6/2 | e6/4. b5/8 g#5/2 | g#5/4 c#6/4 e6/2 | c#6/2 a5/2 '
    '| b5/4 d6/4 f#6/2 | e6/4. d6/8 b5/2 | a5/4 f#5/4 d5/4 f#5/4 | g#5/2 b5/2 |'
)


def partitura(A):
    b = Brano(A, bpm=144)
    tr = b.voce('tromba', 29, volume=108, pan=64)
    ar = b.voce('archi', 23, volume=78, pan=40)
    bs = b.voce('basso', 22, volume=100, pan=64)
    bt = b.voce('batteria', 39, volume=80, pan=64)
    tr.suona(MELODIA, da=2, vel=96)
    giro = INTRO + A_ + B_
    ar.accordi(A_ + B_, 'x---x---', da=2, registro=(55, 72), vel=64)
    bs.basso(giro, '1 . 8 . 1 5 8 .', da=0)
    bt.batteria({'cassa': 'x...x...', 'rullante': '..x...x.', 'hh': 'x.x.x.x.'}, da=0, battute=18)
    b.eco(tr, 'tromba eco', ritardo=12, volume=40)
    b.ritornello(2, 18)
    return b.fine()
