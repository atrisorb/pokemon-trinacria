"""La Grotta del Gelo: ghiaccio perenne dentro la lava dell'Etna, versante nord (D-CT-06)."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from notazione import Brano, Giro  # noqa: E402

SIMBOLO = 'SEQ_TRN_GROTTA_GELO'
BANCO = 'BANK_BGM_DUNGEON1'
VOLUME = 72
SCHEDA = {
    'titolo': 'Grotta del Gelo',
    'carattere': 'il ghiacciaio più a sud d\'Europa, dentro la lava: valzer cristallino in 3/4, celesta '
                 'e glockenspiel che luccicano, archi sospesi, flauto freddo e chiaro',
    'tonalita': 'Si minore',
    'forma': 'introduzione di 2 battute (celesta); ritornello A (8) + B (8) in Si minore, poi le stesse 16 battute in Mi minore, in 3/4',
}

INTRO = Giro('Bm | F#7')
A_ = Giro('Bm | G | Em | F# | Bm | D | Em | F#7')
B_ = Giro('G | D | A | Bm | G | D | Em | F#7')

MELODIA = (
    '| f#5/2 b5/4 | d6/2 b5/4 | g5/4 e5 b5 | a#5/2. '
    '| b5/4 d6 f#6 | a6/2 f#6/4 | e6/4 g6 b5 | c#6/2 a#5/4 '
    '| b5/2 d6/4 | a5/2 f#5/4 | e5/4 a5 c#6 | d6/2 b5/4 '
    '| g5/4 b5 d6 | f#6/2 d6/4 | e6/4 b5 g5 | f#5/2 e5/4 |'
)


def partitura(A):
    b = Brano(A, bpm=132, metro=(3, 4))
    fl = b.voce('flauto', 35, volume=104, pan=64)
    ce = b.voce('celesta', 27, volume=88, pan=36)
    gl = b.voce('glockenspiel', 10, volume=64, pan=100)
    ar = b.voce('archi', 24, volume=62, pan=90)
    vc = b.voce('contrabbasso', 25, volume=88, pan=64)
    fl.suona(MELODIA, da=2, vel=92)
    giro = INTRO + A_ + B_
    ce.arpeggi(giro, '1 5 8 10 8 5', da=0, registro=(71, 95), vel=72)
    gl.arpeggi(A_ + B_, '8 . .', da=2, registro=(79, 96), vel=70)
    ar.accordi(A_ + B_, 'x--', da=2, registro=(54, 69), vel=52, gate=0.97)
    vc.basso(A_ + B_, '1 . .', da=2)
    b.ripeti(2, 16, 18, trasponi=-7)
    b.eco(fl, 'flauto eco', ritardo=24, volume=40)
    b.ritornello(2, 34)
    return b.fine()
