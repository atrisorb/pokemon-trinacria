"""«U Sistema»: lotta (Scagnozzu, Infiltrata, Cambiavoti, Cassieri, Caporali, CollettuBian., Fantasmi)."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from notazione import Brano, Giro  # noqa: E402

SIMBOLO = 'SEQ_TRN_SISTEMA_LOTTA'
BANCO = 'BANK_BGM_BATTLE1'
VOLUME = 102
SCHEDA = {
    'titolo': '«U Sistema» — lotta',
    'carattere': 'lotta contro il cartello: si apre con una discesa cromatica d\'ottoni; parte A '
                 'minacciosa, parte B in Fa minore che spinge, parte C a colpi secchi; ostinato '
                 'd\'archi in semicrome e il Re bemolle napoletano prima di ogni ritorno',
    'tonalita': 'Do minore',
    'forma': 'introduzione di 2 battute; ritornello A (8) + B (8) + C (8)',
}

INTRO = Giro('Cm | G7')
A_ = Giro('Cm | Cm | Ab | Bb | Cm | Cm | Ab | G7')
B_ = Giro('Fm | Cm | Fm | G | Ab | Eb | F | G7')
C_ = Giro('Cm | Bb | Ab | G | Cm | Bb | Db | G7')

MELODIA = (
    '| g5/4. f5/8 eb5/4 c5 | g4/8 c5 eb5 g5 c6/4 g5 | ab5/4. g5/8 eb5/4 c5 | d5/4. f5/8 bb5/4 d6 '
    '| eb6/4. d6/8 c6/4 g5 | eb5/8 f5 g5 ab5 g5/4 eb5 | eb5/4 ab5 c6 eb6 | d6/2 b5/4 g5 '
    '| c6/4. ab5/8 f5/4 c5 | eb5/4. d5/8 c5/4 g4 | ab4/8 c5 f5 ab5 c6/4 ab5 | b5/2 d6/4 g6 '
    '| eb6/4. c6/8 ab5/4 eb5 | g5/4 bb5 eb6 g6 | f6/4. c6/8 a5/4 f5 | g5/2 b5/4 d6 '
    '| c6/8> c6 r c6 g5/8 eb5 c5/4 | d6/8> d6 r d6 bb5/8 f5 d5/4 | c6/8> c6 r c6 ab5/8 eb5 c5/4 '
    '| b5/8> b5 r b5 g5/8 d5 b4/4 | eb6/4 d6/8 c6 g5/4 c6 | d6/4 c6/8 bb5 f5/4 bb5 '
    '| db6/4 c6/8 ab5 f5/4 ab5 | g5/2 f5/4 d5 |'
)


def partitura(A):
    b = Brano(A, bpm=184)
    ot = b.voce('ottoni', 29, volume=116, pan=60)
    os_ = b.voce('ostinato', 17, volume=92, pan=100)
    tb = b.voce('tromboni', 30, volume=96, pan=30)
    bs = b.voce('basso', 22, volume=116, pan=64)
    tp = b.voce('timpani', 28, volume=104, pan=64)
    bt = b.voce('batteria', 39, volume=100, pan=64)
    ot.suona('| c6/8 b5 bb5 a5 ab5 g5 gb5 f5 | e5/8 eb5 d5 db5 c5/4 g4 |', da=0, vel=104)
    ot.suona(MELODIA, da=2, vel=102)
    b.eco(ot, 'archi ottava', ritardo=0, volume=76, pan=20, trasponi=-12, programma=23)
    giro = INTRO + A_ + B_ + C_
    os_.accordi(A_ + B_ + C_, 'x.xx.xx.x.xx.xx.', da=2, registro=(55, 67), vel=66, voci=2, gate=0.5)
    tb.accordi(C_, 'X..X..X.', da=18, registro=(48, 62), vel=88, gate=0.4)
    bs.basso(giro, '1 1 8 1 1 1 8 1', da=0, registro=(31, 50), gate=0.6)
    tp.basso(giro, '1 . . . . . . .', da=0, registro=(43, 55), vel=110, gate=0.5)
    bt.batteria({'cassa': 'x.x.x.x.', 'rullante': 'xxxxxxxx'}, da=0, battute=1)
    bt.batteria({'cassa': 'x.x.xxxx', 'rullante': 'xxxxXXXX'}, da=1, battute=1)
    bt.batteria({'cassa': 'x...x...x...x...', 'rullante': '....x.......x..o', 'hh': 'x.x.x.x.x.x.x.x.'},
                da=2, battute=24)
    b.ritornello(2, 26)
    return b.fine()
