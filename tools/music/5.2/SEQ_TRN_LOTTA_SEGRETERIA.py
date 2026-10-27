"""Lotta coi Segretari 1-8 e coi Campioni dell'ARS."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from notazione import Brano, Giro  # noqa: E402

SIMBOLO = 'SEQ_TRN_LOTTA_SEGRETERIA'
BANCO = 'BANK_BGM_BATTLE1'
VOLUME = 108
SCHEDA = {
    'titolo': 'Lotta coi Segretari',
    'carattere': 'il boss della Segreteria al suo tavolo: introduzione a colpi ribattuti e scala che '
                 'sale sul La settima; tema eroico in Re minore, ripreso più in alto (A\'), parte B '
                 'luminosa in Si bemolle e Fa, parte C che riprende fiato su Sol minore prima della '
                 'stretta finale; il legnetto del timbro torna dalla musica delle Segreterie',
    'tonalita': 'Re minore',
    'forma': 'introduzione di 2 battute; ritornello A (8) + A\' (8) + B (8) + C (8)',
}

INTRO = Giro('Dm | A7')
A_ = Giro('Dm | Bb | C | A | Dm | Bb | Gm | A')
A2 = Giro('Dm | Bb | C | F | Gm | Bb | Gm A | Dm')
B_ = Giro('Bb | C | F | Dm | Gm | C | F | A7')
C_ = Giro('Gm | Dm | Gm | A | Bb | C | Dm | A7')

MELODIA = (
    '| d5/8 f5 a5 d6 a5/4 f5 | bb5/4. a5/8 f5/4 d5 | e5/8 g5 c6 e6 c6/4 g5 | c#6/4. e6/8 a5/2 '
    '| d6/4. e6/8 f6/4 d6 | d6/4. c6/8 bb5/4 f5 | g5/8 bb5 d6 g6 d6/4 bb5 | a5/2 c#6/4 e6 '
    '| f6/4. e6/8 d6/4 a5 | f6/4 d6/8 bb5 f5/4 bb5 | g6/4 e6/8 c6 g5/4 c6 | a5/4 c6 f6 c6 '
    '| bb5/4 d6 g6 d6 | f6/4 d6 bb5 f5 | g5/4 bb5 c#6 e6 | d6/2. r/4 '
    '| f5/4 bb5 d6 f6 | e6/4 c6 g5 e5 | f5/4. a5/8 c6/4 f6 | f6/4 e6/8 d6 a5/4 f5 '
    '| g5/4. bb5/8 d6/4 g6 | g6/4 e6/8 c6 g5/4 e5 | f5/4 a5 c6 f6 | e6/4 c#6 a5 g5 '
    '| bb5/8 a5 g5 d5 bb4/4 d5 | f5/8 e5 d5 a4 f4/4 a4 | g5/8 bb5 d6 g6 bb6/4 g6 | a6/4 e6 c#6 a5 '
    '| bb5/4. c6/8 d6/4 f6 | e6/4. d6/8 c6/4 g5 | f5/4 a5 d6 f6 | e6/4 c#6 a5 g5 |'
)


def partitura(A):
    b = Brano(A, bpm=186)
    ot = b.voce('tromba', 29, volume=118, pan=60)
    os_ = b.voce('ostinato', 17, volume=88, pan=100)
    tb = b.voce('tromboni', 30, volume=92, pan=30)
    bs = b.voce('basso', 22, volume=116, pan=64)
    tp = b.voce('timpani', 28, volume=104, pan=64)
    bt = b.voce('batteria', 39, volume=100, pan=64)
    ot.suona('| d6/8> r d6 r d6 r d6/4 | c#6/8 d6 e6 f6 g6 a6 bb6 c#7 |', da=0, vel=106)
    ot.suona(MELODIA, da=2, vel=102)
    b.eco(ot, 'archi ottava', ritardo=0, volume=78, pan=24, trasponi=-12, programma=23)
    giro = INTRO + A_ + A2 + B_ + C_
    os_.accordi(A_ + A2 + B_ + C_, 'x.xx.xx.x.xx.xx.', da=2, registro=(53, 65), vel=64, voci=2, gate=0.5)
    tb.accordi(INTRO, 'X.X.X.X.', da=0, registro=(50, 62), vel=90, gate=0.4)
    bs.basso(giro, '1 1 8 1 1 1 8 1', da=0, registro=(26, 45), gate=0.6)
    tp.basso(giro, '1 . . . 1 . . .', da=0, registro=(38, 50), vel=104, gate=0.5)
    norm = {'cassa': 'x.....x.x.......', 'rullante': '....x.......x...', 'hh': 'x.x.x.x.x.x.x.x.',
            'legnetto': '..............x.'}
    fill = {'cassa': 'x.....x.x.......', 'rullante': '....x.....xxxxxx', 'hh': 'x.x.x.x.x.......'}
    bt.batteria({'rullante': 'x.x.x.x.x.x.x.x.'}, da=0, battute=2)
    bt.batteria([norm] * 7 + [fill], da=2, battute=32)
    b.ritornello(2, 34)
    return b.fine()
