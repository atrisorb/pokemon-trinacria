"""L'Etna: Etna Sud, Monti Rossi, Crateri Silvestri, Sciara, Cratere Centrale (M-CT-06, D-CT-01)."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from notazione import Brano, Giro  # noqa: E402

SIMBOLO = 'SEQ_CT_ETNA'
BANCO = 'BANK_BGM_DUNGEON3'
VOLUME = 70
SCHEDA = {
    'titolo': 'L\'Etna',
    'carattere': 'la Muntagna: solenne e minacciosa, ostinato grave degli archi come il brontolio del '
                 'vulcano, timpani, corno che sale lento; nella parte B la melodia passa agli archi '
                 'acuti e il corno risponde',
    'tonalita': 'Re minore (eolio, col Do maggiore)',
    'forma': 'introduzione di 2 battute (ostinato e timpani); ritornello A (8) + B (8)',
}

INTRO = Giro('Dm | Dm')
A_ = Giro('Dm | C | Bb | C | Dm | F | Gm | A')
B_ = Giro('Bb | F | C | Dm | Bb | Gm | A | A7')

CORNO_A = (
    '| d4/2 a4 | g4/4. e4/8 c4/2 | d4/4. f4/8 bb4/2 | c5/2 g4 '
    '| f4/4. e4/8 d4/4 a4 | c5/2 a4/4 f4 | g4/4. bb4/8 d5/2 | c#5/2. r/4 |'
)
ARCHI_B = (
    '| d5/2 f5/4 d5 | c5/2 a4 | g4/4 c5 e5/2 | f5/2. d5/4 '
    '| f5/4. e5/8 d5/4 bb4 | g4/4 bb4 d5 g5 | e5/2 c#5 | e5/4 g5 c#5 a4 |'
)
CORNO_B = '| bb3/1 | a3/1 | g3/1 | a3/1 | f3/1 | g3/2 bb3 | a3/1 | c#4/2 e4 |'


def partitura(A):
    b = Brano(A, bpm=84)
    co = b.voce('corno', 32, volume=112, pan=56)
    vl = b.voce('archi', 23, volume=100, pan=80)
    os_ = b.voce('ostinato', 25, volume=104, pan=64)
    tb = b.voce('ottoni', 30, volume=70, pan=30)
    tp = b.voce('timpani', 28, volume=100, pan=64)
    tm = b.voce('tamburi', 39, volume=80, pan=64)
    co.suona(CORNO_A, da=2, vel=96).suona(CORNO_B, da=10, vel=84)
    vl.suona(ARCHI_B, da=10, vel=96)
    giro = INTRO + A_ + B_
    os_.arpeggi(giro, '1 1 8 1 1 1 5 1', da=0, registro=(38, 55), vel=84, gate=0.7)
    tb.accordi(A_, 'x---x---', da=2, registro=(50, 65), vel=60)
    tp.basso(giro, '1 . . . 1 . 1 .', da=0, registro=(43, 55), vel=96, gate=0.5)
    tm.batteria({'tom_b': 'x.......x.....o.', 'cassa': 'x...............'}, da=0, battute=18)
    b.ritornello(2, 18)
    return b.fine()
