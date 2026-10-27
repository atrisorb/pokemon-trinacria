"""Augusta, Priolo, Melilli: la cortina di fumo del polo industriale."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from notazione import Brano, Giro  # noqa: E402

SIMBOLO = 'SEQ_SR_AUGUSTA'
BANCO = 'BANK_BGM_FIELD10'
VOLUME = 62
SCHEDA = {
    'titolo': 'Augusta, la cortina di fumo',
    'carattere': 'costa industriale sotto la nebbia gialla: ostinato di pizzicato e basso sintetico che '
                 'non si ferma, come le macchine del polo, il legnetto che batte le sedicesime, archi '
                 'lenti e una voce d\'ancia triste che canta sopra il fumo',
    'tonalita': 'Mi minore',
    'forma': 'introduzione di 2 battute (ostinato e macchine); ritornello A (8) + B (8)',
}

INTRO = Giro('Em | Em')
A_ = Giro('Em | C | Am | B7 | Em | C | D | B7')
B_ = Giro('C | G | Am | Em | C | Am | B7 | B7')

MELODIA = (
    '| e5/2 g5/4 b5/4 | c6/4. b5/8 g5/2 | a5/4 c6/8 b5/8 a5/4 e5/4 | f#5/2 d#5/4 b4/4 '
    '| e5/4 g5/8 a5/8 b5/2 | e6/4. d6/8 c6/2 | d6/4 a5/4 f#5/4 a5/4 | b5/2. r/4 '
    '| g5/4 c6/4 e6/2 | d6/4. b5/8 g5/2 | a5/4 c6/4 e6/4 c6/4 | b5/1 '
    '| e6/4 c6/4 g5/2 | a5/4 e5/4 c6/4 a5/4 | b5/4 a5/4 f#5/4 d#5/4 | b4/2. r/4 |'
)


def partitura(A):
    b = Brano(A, bpm=100)
    ob = b.voce('canto', 33, volume=104, pan=64)
    pz = b.voce('ostinato', 17, volume=92, pan=40)
    ar = b.voce('archi', 24, volume=78, pan=88)
    bs = b.voce('basso', 21, volume=100, pan=64)
    bt = b.voce('macchine', 39, volume=74, pan=64)
    ob.suona(MELODIA, da=2, vel=96)
    giro = INTRO + A_ + B_
    pz.arpeggi(giro, '1 5 8 5 1 5 8 5', da=0, registro=(40, 64), vel=80, gate=0.6)
    ar.accordi(A_ + B_, 'x-------', da=2, registro=(52, 71), vel=64)
    bs.basso(giro, '1 . . 1 . . 5 .', da=0, gate=0.8)
    bt.batteria({'legnetto': 'x.o.x.o.x.o.x.o.', 'cassa': 'x.......x.......'}, da=0, battute=18)
    b.eco(ob, 'canto eco', ritardo=12, volume=38)
    b.ritornello(2, 18)
    return b.fine()
