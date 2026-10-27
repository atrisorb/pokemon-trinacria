"""Lotta con Scirocco (Entei), il primo dei Tre Venti di Sicilia (P-07)."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from notazione import Brano, Giro  # noqa: E402

SIMBOLO = 'SEQ_TRN_LOTTA_SCIROCCO'
BANCO = 'BANK_BGM_BATTLE6'
VOLUME = 98
SCHEDA = {
    'titolo': 'Scirocco',
    'carattere': 'il vento africano infuocato: modo frigio di Mi col Sol diesis (il Fa accanto al Mi), '
                 'voce d\'ancia raddoppiata dagli archi, pizzicato in ostinato, tamburi a mano e tom; i '
                 'Tre Venti hanno lo stesso inizio di frase (quarta che sale e terza che scende), ognuno '
                 'nel suo modo',
    'tonalita': 'Mi frigio (dominante)',
    'forma': 'introduzione di 2 battute; ritornello A (8) + B (8)',
}

INTRO = Giro('E | F')
A_ = Giro('E | F | E | Dm | E | F | Dm | E')
B_ = Giro('Am | G | F | E | Am | G | F | E7')

APERTURA = '| e5/8 f5 g#5 a5 b5/4 e6 | f6/4. e6/8 c6/4 a5 |'
MELODIA = (
    '| e5/4 g#5/8 a5 b5/4 e6 | f6/4. e6/8 c6/4 a5 | g#5/4 b5 e6 g#6 | f6/4. e6/8 d6/4 a5 '
    '| b5/4. c6/8 b5/4 g#5 | a5/4 c6 f6 c6 | d6/4 f6/8 e6 d6/4 a5 | e6/2. r/4 '
    '| a5/4. b5/8 c6/4 e6 | d6/4. c6/8 b5/4 g5 | a5/4 c6 f6 a6 | g#6/2 e6/4 b5 '
    '| c6/8 b5 a5 e5 a5/4 c6 | b5/8 a5 g5 d5 g5/4 b5 | a5/4 f5 c6 a5 | g#5/2 d6/4 b5 |'
)


def partitura(A):
    b = Brano(A, bpm=168)
    ob = b.voce('canto', 33, volume=116, pan=60)
    pz = b.voce('ostinato', 17, volume=88, pan=100)
    bs = b.voce('basso', 22, volume=114, pan=64)
    tp = b.voce('timpani', 28, volume=98, pan=64)
    bt = b.voce('tamburi', 39, volume=96, pan=64)
    ob.suona(APERTURA, da=0, vel=104).suona(MELODIA, da=2, vel=102)
    b.eco(ob, 'archi ottava', ritardo=0, volume=76, pan=24, trasponi=-12, programma=23)
    giro = INTRO + A_ + B_
    pz.accordi(giro, 'x.xx.xx.x.xx.xx.', da=0, registro=(52, 64), vel=66, voci=2, gate=0.5)
    bs.basso(giro, '1 1 8 1 1 1 8 1', da=0, registro=(28, 47), gate=0.6)
    tp.basso(giro, '1 . . . 5, . . .', da=0, registro=(40, 52), vel=100, gate=0.5)
    bt.batteria({'cassa': 'x..x..x.x..x..x.', 'tom_m': '....x.......x.x.', 'tamburello': 'x.xx.xx.x.xx.xx.'},
                da=0, battute=18)
    b.ritornello(2, 18)
    return b.fine()
