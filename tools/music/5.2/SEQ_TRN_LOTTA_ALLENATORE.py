"""Lotta con un allenatore comune."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from notazione import Brano, Giro  # noqa: E402

SIMBOLO = 'SEQ_TRN_LOTTA_ALLENATORE'
BANCO = 'BANK_BGM_BATTLE1'
VOLUME = 111
SCHEDA = {
    'titolo': 'Lotta con un allenatore',
    'carattere': 'la lotta di tutti i giorni, energica e cantabile: scala che sale fino al Mi acuto, '
                 'tema A in La minore ripetuto con un\'altra chiusa, parte B che si apre in Do maggiore, '
                 'parte C che torna scura su Re minore e Si settima prima di ricominciare',
    'tonalita': 'La minore',
    'forma': 'introduzione di 2 battute; ritornello A (8) + A\' (8) + B (8) + C (8)',
}

INTRO = Giro('Am | E')
A_ = Giro('Am | F | G | E | Am | F | Dm | E')
A2 = Giro('Am | F | G | E | Am | F | G E | Am')
B_ = Giro('F | G | C | Am | F | G | C | E7')
C_ = Giro('Dm | Am | Dm | E | Dm | Am | B7 | E7')

TEMA = (
    '| e5/8 a5 c6 e6 c6/4 a5 | a5/4. g5/8 f5/4 c5 | d5/8 g5 b5 d6 b5/4 g5 | g#5/4. e5/8 b4/2 '
    '| c6/8 b5 a5 e5 a5/4 c6 | c6/4. a5/8 f5/4 a5 |'
)
MELODIA = (
    TEMA + '| f5/8 e5 d5 f5 a5/4 d6 | b5/2 g#5/4 e5 ' + TEMA + '| d6/4 b5 b5 g#5 | a5/2. r/4 '
    '| a5/4. c6/8 f6/4 c6 | b5/4. d6/8 g6/4 d6 | e6/4. d6/8 c6/4 g5 | a5/4 c6 e6 a6 '
    '| f6/4 c6 a5/8 c6 f6/4 | g6/4 d6 b5/8 d6 g6/4 | e6/2 g6/4 c6 | b5/2 g#5/4 d6 '
    '| d5/8 f5 a5 d6 f6/4 d6 | e6/8 c6 a5 e5 c5/4 e5 | f5/8 a5 d6 f6 a6/4 f6 | e6/4. d6/8 b5/4 g#5 '
    '| f6/4 e6/8 d6 a5/4 f5 | e6/4 c6/8 a5 e5/4 a5 | d#6/4 b5 f#5 a5 | g#5/4 b5 d6 e6 |'
)


def partitura(A):
    b = Brano(A, bpm=178)
    ot = b.voce('tromba', 29, volume=116, pan=60)
    os_ = b.voce('ostinato', 17, volume=88, pan=100)
    bs = b.voce('basso', 22, volume=116, pan=64)
    tp = b.voce('timpani', 28, volume=100, pan=64)
    bt = b.voce('batteria', 39, volume=100, pan=64)
    ot.suona('| a4/16 b4 c5 d5 e5 f5 g5 a5 b5 c6 d6 e6 f6/8 e6 | e6/4 r e5> e5> |', da=0, vel=104)
    ot.suona(MELODIA, da=2, vel=102)
    b.eco(ot, 'archi ottava', ritardo=0, volume=78, pan=24, trasponi=-12, programma=23)
    giro = INTRO + A_ + A2 + B_ + C_
    os_.accordi(A_ + A2 + B_ + C_, 'x.xx.xx.x.xx.xx.', da=2, registro=(55, 67), vel=64, voci=2, gate=0.5)
    bs.basso(giro, '1 1 8 1 5 1 8 1', da=0, registro=(31, 50), gate=0.6)
    tp.basso(giro, '1 . . . . . . .', da=0, registro=(43, 55), vel=104, gate=0.5)
    bt.batteria({'rullante': 'x.x.x.x.x.x.xxxx'}, da=0, battute=2)
    norm = {'cassa': 'x.....x.x.......', 'rullante': '....x.......x...', 'hh': 'x.x.x.x.x.x.x.x.'}
    fill = {'cassa': 'x.....x.x.......', 'rullante': '....x.....x.xxxx', 'hh': 'x.x.x.x.x.......'}
    bt.batteria([norm] * 7 + [fill], da=2, battute=32)
    b.ritornello(2, 34)
    return b.fine()
