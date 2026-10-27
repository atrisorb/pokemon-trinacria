"""Dentro il Padiglione Torre Lotta della Fiera del Mediterraneo (P-09)."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from notazione import Brano, Giro  # noqa: E402

SIMBOLO = 'SEQ_PA_FIERA_TORRE_LOTTA'
BANCO = 'BANK_BGM_DUNGEON4'
VOLUME = 70
SCHEDA = {
    'titolo': 'Il Padiglione Torre Lotta',
    'carattere': 'concentrazione prima della sfida: ostinato di marimba a crome che non si ferma, basso '
                 'sintetico, archi lenti e un vibrafono che lascia cadere poche note; il charleston '
                 'tiene il tempo come un cronometro',
    'tonalita': 'Mi minore (parte B in Sol maggiore)',
    'forma': 'introduzione di 2 battute (marimba); ritornello A (8) + B (8)',
}

INTRO = Giro('Em | B7')
A_ = Giro('Em | C | Am | B7 | Em | C | Am B7 | Em')
B_ = Giro('G | D | C | B7 | G | D | C | B7')

MELODIA = (
    '| b5/2 g5/4 e5 | c6/2 g5/4 e5 | a5/2 c6/4 e6 | d#6/2 b5/4 f#5 '
    '| g5/4. f#5/8 e5/4 b5 | e6/2 c6/4 g5 | a5/4 e5 f#5 a5 | e5/2. r/4 '
    '| d6/2 b5/4 g5 | a5/2 f#5/4 d5 | e5/4 g5 c6 e6 | d#6/2 a5/4 f#5 '
    '| g5/4. a5/8 b5/4 d6 | f#6/2 d6/4 a5 | g5/4 c6 e6 g6 | f#6/2 d#6/4 b5 |'
)


def partitura(A):
    b = Brano(A, bpm=120)
    vb = b.voce('vibrafono', 5, volume=100, pan=64)
    mr = b.voce('marimba', 18, volume=82, pan=94)
    ar = b.voce('archi', 24, volume=64, pan=34)
    bs = b.voce('basso', 21, volume=100, pan=64)
    bt = b.voce('cronometro', 39, volume=62, pan=64)
    vb.suona(MELODIA, da=2, vel=94)
    b.eco(vb, 'vibrafono eco', ritardo=48, volume=40)
    giro = INTRO + A_ + B_
    mr.arpeggi(giro, '1 5 8 5 10 5 8 5', da=0, registro=(52, 76), vel=70, gate=0.6)
    ar.accordi(A_ + B_, 'x-------', da=2, registro=(55, 70), vel=56)
    bs.basso(giro, '1 . 1 . 1 . 5, .', da=0, registro=(28, 47), gate=0.7)
    bt.batteria({'hh': 'x.x.x.x.x.x.x.x.', 'bordo': '....x.......x...'}, da=2, battute=16)
    b.ritornello(2, 18)
    return b.fine()
