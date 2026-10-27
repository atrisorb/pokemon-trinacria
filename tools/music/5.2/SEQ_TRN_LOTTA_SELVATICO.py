"""Lotta con un Pokémon selvatico."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from notazione import Brano, Giro  # noqa: E402

SIMBOLO = 'SEQ_TRN_LOTTA_SELVATICO'
BANCO = 'BANK_BGM_BATTLE1'
VOLUME = 110
SCHEDA = {
    'titolo': 'Lotta con un Pokémon selvatico',
    'carattere': 'l\'erba alta si muove: scatto in semicrome e due colpi, poi un tema nervoso in '
                 'Mi minore; la parte B sale verso il La minore, la parte C corre su Do–Re–Si come '
                 'un inseguimento',
    'tonalita': 'Mi minore',
    'forma': 'introduzione di 2 battute; ritornello A (8) + B (8) + C (8)',
}

INTRO = Giro('Em | B')
A_ = Giro('Em | Em | C | D | Em | Em | C | B')
B_ = Giro('Am | Em | Am | B | C | D | Em | B7')
C_ = Giro('C | D | Bm | Em | C | D | B | B7')

MELODIA = (
    '| b4/8 e5 g5 b5 g5/4 e5 | g5/8 f#5 e5/4 b5 g5 | c6/4. b5/8 g5/4 e5 | d6/4. c6/8 a5/4 f#5 '
    '| e6/8 d6 b5 g5 e5/4 g5 | b5/4 e6 g6 e6 | e6/4. d6/8 c6/4 g5 | f#6/2 d#6/4 b5 '
    '| c6/4. b5/8 a5/4 e5 | b5/4. a5/8 g5/4 e5 | a5/8 c6 e6 a6 e6/4 c6 | d#6/2 f#6/4 b5 '
    '| g6/4. e6/8 c6/4 g5 | a5/4. f#5/8 d5/4 a5 | b5/8 g5 e5 g5 b5/4 e6 | d#6/4 b5 a5 f#5 '
    '| e5/8 g5 c6 e6 g6/4 e6 | f#6/8 d6 a5 f#5 d5/4 a5 | b5/4. d6/8 f#6/4 d6 | e6/2 b5 '
    '| c6/8 e6 g6 e6 c6/4 g5 | d6/8 f#6 a6 f#6 d6/4 a5 | b5/4 d#6 f#6 b6 | a6/4 f#6 d#6 b5 |'
)


def partitura(A):
    b = Brano(A, bpm=176)
    vl = b.voce('archi', 23, volume=114, pan=40)
    ot = b.voce('tromba', 29, volume=84, pan=88)
    os_ = b.voce('ostinato', 17, volume=88, pan=100)
    bs = b.voce('basso', 22, volume=116, pan=64)
    tp = b.voce('timpani', 28, volume=96, pan=64)
    bt = b.voce('batteria', 39, volume=100, pan=64)
    vl.suona('| e5/16 f#5 g5 a5 b5 c6 d6 e6 f#6/4 e6 | b5/8> b5 r b5 b5/4> r |', da=0, vel=104)
    vl.suona(MELODIA, da=2, vel=102)
    b.eco(vl, 'tromba ottava', ritardo=0, volume=80, pan=88, trasponi=-12, programma=29)
    giro = INTRO + A_ + B_ + C_
    os_.accordi(A_ + B_ + C_, 'x.xx.xx.x.xx.xx.', da=2, registro=(52, 64), vel=64, voci=2, gate=0.5)
    bs.basso(giro, '1 1 8 1 1 1 5 1', da=0, registro=(28, 47), gate=0.6)
    tp.basso(giro, '1 . . . 1 . . .', da=0, registro=(40, 52), vel=100, gate=0.5)
    bt.batteria({'cassa': 'x.x.x.x.', 'hh': 'xxxxxxxx'}, da=0, battute=2)
    norm = {'cassa': 'x..x..x.x.......', 'rullante': '....x.......x...', 'hh': 'x.x.x.x.x.x.x.x.'}
    fill = {'cassa': 'x..x..x.x.......', 'rullante': '....x.....xxxxxx', 'hh': 'x.x.x.x.x.......'}
    bt.batteria([norm] * 7 + [fill], da=2, battute=24)
    b.ritornello(2, 26)
    return b.fine()
