"""Musei, castelli e siti archeologici: Castello Ursino, Palazzo di Giustizia, Neapolis, Cava d'Ispica..."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from notazione import Brano, Giro  # noqa: E402

SIMBOLO = 'SEQ_TRN_MONUMENTO'
BANCO = 'BANK_BGM_DUNGEON7'
VOLUME = 93
SCHEDA = {
    'titolo': 'Monumento',
    'carattere': 'pietre antiche, vetrine e silenzio: arpa che arpeggia, flauto in modo dorico (il Re '
                 'maggiore dentro il La minore dà il sapore «greco»), archi lontani; la parte B scende '
                 'verso il Mi maggiore come in una cadenza antica',
    'tonalita': 'La dorico',
    'forma': 'introduzione di 2 battute (arpa); ritornello A (8) + B (8)',
}

INTRO = Giro('Am | D')
A_ = Giro('Am | G | Am | D | Am | G | Em | Am')
B_ = Giro('F | G | Am | Em | F | G | Dm E | E')

MELODIA = (
    '| e5/2 a5/4 c6 | b5/2 d6/4 b5 | a5/4. g5/8 e5/2 | f#5/2 a5/4 d6 '
    '| c6/4. b5/8 a5/4 e5 | d5/4 g5 b5/2 | b4/4 e5 g5 b5 | a5/1 '
    '| a5/4. g5/8 f5/4 c5 | d5/2 g5/4 b5 | c6/2 e6/4 c6 | b5/2 g5/4 e5 '
    '| f5/4 a5 c6 a5 | b5/4 d6 g5 b4 | d5/4 f5 g#5 b5 | e5/1 |'
)


def partitura(A):
    b = Brano(A, bpm=84)
    fl = b.voce('flauto', 35, volume=106, pan=64)
    ap = b.voce('arpa', 26, volume=92, pan=36)
    ar = b.voce('archi', 24, volume=60, pan=96)
    vc = b.voce('contrabbasso', 25, volume=90, pan=64)
    fl.suona(MELODIA, da=2, vel=94)
    giro = INTRO + A_ + B_
    ap.arpeggi(giro, '1 5 8 10 12 10 8 5', da=0, registro=(45, 76), vel=78)
    ar.accordi(A_ + B_, 'x-------', da=2, registro=(57, 72), vel=50)
    vc.basso(A_ + B_, '1 - - - - - - -', da=2, gate=0.95)
    b.eco(fl, 'flauto eco', ritardo=24, volume=42)
    b.ritornello(2, 18)
    return b.fine()
