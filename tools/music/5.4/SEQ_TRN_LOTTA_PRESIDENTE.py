"""Lotta con l'On. Mistretta (M-EN-06) e con Maria sul tetto del tribunale (P-02)."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from notazione import Brano, Giro  # noqa: E402

SIMBOLO = 'SEQ_TRN_LOTTA_PRESIDENTE'
BANCO = 'BANK_BGM_BATTLE3'
VOLUME = 113
SCHEDA = {
    'titolo': 'Lotta col Presidente',
    'carattere': 'l\'ultima lotta della storia: quattro battute d\'introduzione (colpi, arpeggio che '
                 'sale, il Re bemolle tenuto, la discesa sul Sol), poi un tema eroico in Do minore per '
                 'tromba e archi all\'ottava, parte B larga in Mi bemolle, parte C a colpi secchi; '
                 'ogni frase chiude sul Re bemolle napoletano di «U Sistema» (R-AUD-21). Lo stesso '
                 'brano torna per Maria sul tetto: la sfida più alta del post-game',
    'tonalita': 'Do minore',
    'forma': 'introduzione di 4 battute; ritornello A (8) + B (8) + C (8)',
}

INTRO = Giro('Cm | Cm | Db | G7')
A_ = Giro('Cm | Ab | Fm | G | Cm | Ab | Db | G')
B_ = Giro('Eb | Bb | Ab | Eb | Fm | Cm | Db | G')
C_ = Giro('Ab | Bb | Gm | Cm | Ab | Bb | Db | G7')

APERTURA = '| c5/8> c5 r/4 c5/8> c5 r/4 | c5/8 eb5 g5 c6 eb6 g6 c7/4 | db7/2. r/4 | b6/8 g6 f6 d6 b5 g5 f5 d5 |'
MELODIA = (
    '| c6/4. g5/8 eb5/4 c5 | eb5/8 ab5 c6 eb6 ab6/4 eb6 | f6/4. eb6/8 c6/4 ab5 | b5/2 d6/4 g6 '
    '| g6/4. f6/8 eb6/4 c6 | c6/4 eb6 ab6 eb6 | f6/4. db6/8 ab5/4 f5 | g5/2 b5/4 d6 '
    '| eb6/4. f6/8 g6/4 bb5 | bb5/4. c6/8 d6/4 f6 | eb6/4. c6/8 ab5/4 c6 | bb5/2 g5/4 eb5 '
    '| f5/8 g5 ab5 c6 f6/4 c6 | eb6/4. d6/8 c6/4 g5 | ab5/4 db6 f6 ab6 | g6/2 d6/4 b5 '
    '| c6/8> c6 r c6 eb6/4 ab5 | d6/8> d6 r d6 f6/4 bb5 | bb5/8> bb5 r bb5 d6/4 g5 | c6/4 eb6 g6 c7 '
    '| c7/4. bb6/8 ab6/4 eb6 | d6/4. eb6/8 f6/4 bb5 | db6/4 f6 ab6 f6 | g6/2 f6/4 d6 |'
)


def partitura(A):
    b = Brano(A, bpm=176)
    ot = b.voce('tromba', 29, volume=118, pan=60)
    os_ = b.voce('ostinato', 17, volume=90, pan=100)
    tb = b.voce('tromboni', 30, volume=96, pan=30)
    bs = b.voce('basso', 22, volume=116, pan=64)
    tp = b.voce('timpani', 28, volume=106, pan=64)
    bt = b.voce('batteria', 39, volume=100, pan=64)
    ot.suona(APERTURA, da=0, vel=106).suona(MELODIA, da=4, vel=104)
    b.eco(ot, 'archi ottava', ritardo=0, volume=78, pan=22, trasponi=-12, programma=23)
    giro = INTRO + A_ + B_ + C_
    os_.accordi(A_ + B_ + C_, 'x.xx.xx.x.xx.xx.', da=4, registro=(55, 67), vel=66, voci=2, gate=0.5)
    tb.accordi(INTRO, 'X.X.X.X.', da=0, registro=(48, 62), vel=92, gate=0.4)
    tb.accordi(C_, 'X..X..X.', da=20, registro=(48, 62), vel=88, gate=0.4)
    bs.basso(giro, '1 1 8 1 1 1 8 1', da=0, registro=(31, 50), gate=0.6)
    tp.basso(giro, '1 . . . 5, . . .', da=0, registro=(41, 53), vel=110, gate=0.5)
    norm = {'cassa': 'x.....x.x.......', 'rullante': '....x.......x...', 'hh': 'x.x.x.x.x.x.x.x.'}
    fill = {'cassa': 'x.....x.x.......', 'rullante': '....x.....xxxxxx', 'hh': 'x.x.x.x.x.......'}
    bt.batteria({'rullante': 'x.x.x.x.x.x.x.x.', 'cassa': 'x.......x.......'}, da=0, battute=3)
    bt.batteria({'rullante': 'xxxxxxxxXXXXXXXX'}, da=3, battute=1)
    bt.batteria([norm] * 7 + [fill], da=4, battute=24)
    b.ritornello(4, 28)
    return b.fine()
