"""Vittoria su un allenatore."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from notazione import Brano, Giro  # noqa: E402

SIMBOLO = 'SEQ_TRN_VITTORIA_ALLENATORE'
BANCO = 'BANK_BASIC'
VOLUME = 110
SCHEDA = {
    'titolo': 'Vittoria su un allenatore',
    'carattere': 'fanfara di quattro battute d\'ottoni, poi una marcetta contenta in Do maggiore che si '
                 'ripete mentre scorrono i messaggi (esperienza, soldi)',
    'tonalita': 'Do maggiore',
    'forma': 'fanfara di 4 battute; ritornello di 8 battute',
}

FANFARA = Giro('C | C | F | G7')
GIRO = Giro('C | Am | F | G | C | Am | Dm G7 | C')

SQUILLI = '| c5/8 e5 g5 c6 e6/4 c6 | g6/2. r/4 | f6/8 e6 d6 c6 a5/4 f5 | g5/2 b5/4 d6 |'
MELODIA = (
    '| e5/4. g5/8 c6/4 g5 | a5/4 c6/8 b5 a5/4 e5 | f5/4. a5/8 c6/4 a5 | g5/4 b5 d6 b5 '
    '| c6/4. e6/8 g6/4 e6 | e6/4 c6/8 a5 e5/4 a5 | f5/4 a5 g5 b5 | c6/2. r/4 |'
)


def partitura(A):
    b = Brano(A, bpm=156)
    tr = b.voce('tromba', 29, volume=116, pan=60)
    fl = b.voce('flauto', 35, volume=70, pan=96)
    ar = b.voce('archi', 23, volume=86, pan=20)
    bs = b.voce('tromboni', 30, volume=112, pan=100)
    bt = b.voce('batteria', 39, volume=96, pan=40)
    tr.suona(SQUILLI, da=0, vel=108).suona(MELODIA, da=4, vel=104)
    fl.suona(MELODIA, da=4, vel=90, trasponi=12)
    giro = FANFARA + GIRO
    ar.accordi(giro, 'x.x.x.x.', da=0, registro=(55, 71), vel=72, gate=0.6)
    bs.basso(giro, '1 . 5 . 1 . 5 .', da=0, registro=(33, 50))
    bt.batteria({'cassa': 'x...x...', 'rullante': '..x...x.', 'hh': 'xxxxxxxx'}, da=0, battute=12)
    b.ritornello(4, 12)
    return b.fine()
