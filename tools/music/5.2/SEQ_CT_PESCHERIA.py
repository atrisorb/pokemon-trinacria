"""Piazza Duomo e il mercato della Pescheria: le «abbanniate» dei venditori."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from notazione import Brano, Giro  # noqa: E402

SIMBOLO = 'SEQ_CT_PESCHERIA'
BANCO = 'BANK_BGM_FIELD1'
VOLUME = 68
SCHEDA = {
    'titolo': 'La Pescheria',
    'carattere': 'mercato del pesce dietro Piazza Duomo: ritmo di danza popolare in 6/8 col tamburello, '
                 'fisarmonica e mandolino; nella parte B le note lunghe acute sono le «abbanniate», i '
                 'richiami cantati dei pescivendoli',
    'tonalita': 'Re minore (parte B in Fa maggiore)',
    'forma': 'introduzione di 2 battute (tamburello e chitarra); ritornello A (8) + B (8) in Re minore, poi le stesse 16 battute in Sol minore (come nelle tarantelle che cambiano tono), in 6/8',
}

INTRO = Giro('Dm | A7')
A_ = Giro('Dm | Dm | Gm | A7 | Dm | C | Bb A7 | Dm')
B_ = Giro('F | C | Gm Dm | A7 | F | C | Bb A7 | Dm A7')

MELODIA = (
    '| a5/4 f5/8 d5/4 a4/8 | d5/8 e5 f5 a5/4 f5/8 | g5/4 bb5/8 d6/4 bb5/8 | a5/4. e5/4 c#5/8 '
    '| d5/4 f5/8 a5/4 d6/8 | c6/4 bb5/8 g5/4 e5/8 | d5/4 f5/8 e5/4 c#5/8 | d5/4. r/4. '
    '| c6/4. a5/4 f5/8 | g5/4. e5/4 c5/8 | d5/4 bb4/8 a4/4 f5/8 | e5/4. c#5/4 a4/8 '
    '| f5/8 g5 a5 c6/4 a5/8 | g5/8 a5 g5 e5/4 c5/8 | d5/4 f5/8 e5/4 g5/8 | f5/4 d5/8 e5/4 c#5/8 |'
)


def partitura(A):
    b = Brano(A, bpm=168, metro=(6, 8))
    fs = b.voce('fisarmonica', 13, volume=104, pan=64)
    md = b.voce('mandolino', 42, volume=84, pan=96)
    gt = b.voce('chitarra', 14, volume=80, pan=32)
    bs = b.voce('basso', 19, volume=106, pan=64)
    bt = b.voce('percussioni', 39, volume=86, pan=64)
    fs.suona(MELODIA, da=2, vel=98)
    giro = INTRO + A_ + B_
    md.arpeggi(A_ + B_, '8 5 10 5 12 5', da=2, registro=(55, 84), vel=70)
    gt.accordi(giro, '.xx.xx', da=0, registro=(52, 67), vel=64)
    bs.basso(giro, '1 . . 5 . .', da=0)
    bt.batteria({'tamburello': 'Xooxoo', 'cassa': 'x.....'}, da=0, battute=18)
    b.ripeti(2, 16, 18, trasponi=5)
    b.ritornello(2, 34)
    return b.fine()
