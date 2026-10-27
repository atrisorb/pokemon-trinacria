"""Le Segreterie: tutte e nove (Palazzo degli Elefanti, Castello Maniace, ...: le «palestre»)."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from notazione import Brano, Giro  # noqa: E402

SIMBOLO = 'SEQ_TRN_SEGRETERIA'
BANCO = 'BANK_BGM_FIELD8'
VOLUME = 80
SCHEDA = {
    'titolo': 'Segreteria',
    'carattere': 'uffici del potere, code infinite e sportelli «torna domani»: marcia burocratica e tesa, '
                 'rullante da parata, archi staccati, tromba; il legnetto in levare è il timbro che cade '
                 'sulle pratiche',
    'tonalita': 'La minore',
    'forma': 'introduzione di 1 battuta (rullante e timbro); ritornello A (8) + B (8)',
}

A_ = Giro('Am | Am | Dm | E | Am | F | Dm E | Am')
B_ = Giro('F | G | C | Am | Dm | G | E | E7')

MELODIA = (
    '| a4/8 a4 a4 c5 e5/4 a4 | c5/8 b4 a4 b4 c5/4 e5 | d5/8 d5 d5 f5 a5/4 f5 | g#5/4. f5/8 e5/2 '
    '| a5/8 g5 a5 b5 c6/4 a5 | a5/4 c6 f5 a5 | f5/4 d5 e5 g#4 | a4/2. r/4 '
    '| c5/4. a4/8 f4/4 a4 | b4/4. g4/8 d5/4 g5 | e5/4. c5/8 g5/4 e5 | a5/2 e5/4 c5 '
    '| d5/4 f5 a5 d6 | b5/4. a5/8 g5/4 d5 | e5/4 g#5 b5 e6 | d6/4 b5 g#5 e5 |'
)


def partitura(A):
    b = Brano(A, bpm=120)
    tr = b.voce('tromba', 29, volume=112, pan=70)
    ar = b.voce('archi', 23, volume=86, pan=30)
    tp = b.voce('timpani', 28, volume=100, pan=64)
    bs = b.voce('basso', 20, volume=112, pan=64)
    bt = b.voce('batteria', 39, volume=92, pan=64)
    tr.suona(MELODIA, da=1, vel=100)
    giro = A_ + B_
    ar.accordi(giro, 'x.x.x.x.', da=1, registro=(55, 71), vel=70, gate=0.5)
    tp.basso(giro, '1 . . . 5, . . .', da=1, registro=(40, 52), vel=96, gate=0.5)
    bs.basso(giro, '1 . 1 . 5 . 1 .', da=1)
    bt.batteria({'rullante': 'x..ox.o.x..ox.oo', 'legnetto': '..........x.....'}, da=0, battute=1)
    bt.batteria({'rullante': 'x..ox.o.x..ox.oo', 'cassa': 'x.......x.......', 'legnetto': '....x.......x...'},
                da=1, battute=16)
    b.ritornello(1, 17)
    return b.fine()
