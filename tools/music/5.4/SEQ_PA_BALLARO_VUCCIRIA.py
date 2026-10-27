"""I mercati e le periferie di Palermo: Ballarò, Vucciria, Kalsa, Borgo Vecchio, ZEN 2, la casa di
Totò e il covo del Cassiere."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from notazione import Brano, Giro  # noqa: E402

SIMBOLO = 'SEQ_PA_BALLARO_VUCCIRIA'
BANCO = 'BANK_BGM_FIELD1'
VOLUME = 92
SCHEDA = {
    'titolo': 'Ballarò e Vucciria',
    'carattere': 'il caos vitale dei mercati: una voce d\'ancia lancia le «abbanniate» dei venditori, '
                 'una nota lunga e poi il ricciolo che scende, e la sua eco risponde dall\'altro banco; '
                 'mandolino in tremolo, fisarmonica in levare, tamburello e battimani; la parte B apre '
                 'in maggiore come una contrattazione andata a buon fine',
    'tonalita': 'La minore (col Mi maggiore della cadenza)',
    'forma': 'introduzione di 2 battute (mandolino e tamburello); ritornello A (8) + B (8)',
}

INTRO = Giro('Am | E7')
A_ = Giro('Am | Am | Dm | Am | E7 | E7 | Am | E7')
B_ = Giro('F | G | C | Am | Dm | E7 | Am | E7')

MELODIA = (
    '| e5/2~ e5/8 d5 c5 b4 | a4/2 r/2 | f5/2~ f5/8 e5 d5 c5 | a4/2 r/2 '
    '| g#5/4. f5/8 e5/4 d5 | e5/8 f5 g#5 b5 e6/2 | c6/4 a5/8 b5 c6/4 e5 | b4/2 g#5/4 e5 '
    '| a5/4. g5/8 f5/4 c6 | b5/4. a5/8 g5/4 d6 | e6/4 c6/8 d6 e6/4 g5 | a5/2 e5/4 c5 '
    '| d5/8 e5 f5 a5 d6/4 a5 | g#5/4 b5/8 d6 e6/4 d6 | c6/4 a5 e5 a5 | b5/2. r/4 |'
)


def partitura(A):
    b = Brano(A, bpm=144)
    ob = b.voce('abbanniata', 33, volume=112, pan=56)
    md = b.voce('mandolino', 42, volume=78, pan=96)
    fs = b.voce('fisarmonica', 13, volume=72, pan=30)
    bs = b.voce('basso', 19, volume=104, pan=64)
    bt = b.voce('batteria', 39, volume=84, pan=64)
    ob.suona(MELODIA, da=2, vel=100)
    b.eco(ob, 'abbanniata eco', ritardo=36, volume=46)
    giro = INTRO + A_ + B_
    md.arpeggi(giro, '1 5 8 5 1 5 8 5 1 5 8 5 1 5 8 5', da=0, registro=(57, 76), vel=60, gate=0.5)
    fs.accordi(A_ + B_, '.x.x.x.x', da=2, registro=(55, 69), vel=64, gate=0.5)
    bs.basso(giro, '1 . 5 . 1 . 5 .', da=0, registro=(33, 52), gate=0.6)
    bt.batteria({'tamburello': 'x.xx.xx.x.xx.xx.'}, da=0, battute=2)
    bt.batteria({'tamburello': 'x.xx.xx.x.xx.xx.', 'battimani': '....x.......x...',
                 'cassa': 'x.......x.......'}, da=2, battute=16)
    b.ritornello(2, 18)
    return b.fine()
