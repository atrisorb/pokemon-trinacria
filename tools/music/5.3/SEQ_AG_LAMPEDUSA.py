"""Il vento e il mare di Lampedusa e la Spiaggia dei Conigli."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from notazione import Brano, Giro  # noqa: E402

SIMBOLO = 'SEQ_AG_LAMPEDUSA'
BANCO = 'BANK_BGM_FIELD14'
VOLUME = 87
SCHEDA = {
    'titolo': 'Lampedusa',
    'carattere': 'l\'isola più vicina all\'Africa che all\'Italia: acqua trasparente, vento costante, '
                 'una bellezza che sa anche di malinconia; flauto largo con l\'eco, chitarra '
                 'arpeggiata, archi lenti come le onde lunghe, triangolo e tamburello nella parte B',
    'tonalita': 'Sol maggiore',
    'forma': 'introduzione di 2 battute (chitarra e archi); ritornello A (8) + B (8)',
}

INTRO = Giro('Gmaj7 | Cmaj7')
A_ = Giro('G | D/F# | Em | C | G | D | Am7 | D')
B_ = Giro('C | G/B | Am | Em | C | D | Bm Em | Am7 D')

MELODIA = (
    '| d5/4 g5/4 b5/2 | a5/4. f#5/8 d5/2 | e5/4 g5/4 b5/4 e6/4 | e6/2 c6/2 '
    '| b5/4 d6/4 g6/2 | f#6/4. d6/8 a5/2 | g5/4 e5/4 c6/4 a5/4 | a5/2. r/4 '
    '| g5/4 e6/4 c6/2 | d6/4. b5/8 g5/2 | a5/4 c6/4 e6/2 | b5/2 g5/2 '
    '| c6/4 e6/4 g6/2 | f#6/4. e6/8 d6/2 | d6/4 b5/4 b5/4 g5/4 | c6/4 a5/4 a5/4 f#5/4 |'
)


def partitura(A):
    b = Brano(A, bpm=96)
    fl = b.voce('flauto', 35, volume=110, pan=64)
    ch = b.voce('chitarra', 7, volume=82, pan=40)
    ar = b.voce('archi', 24, volume=70, pan=88)
    cb = b.voce('contrabbasso', 25, volume=92, pan=64)
    pc = b.voce('percussioni', 39, volume=62, pan=96)
    fl.suona(MELODIA, da=2, vel=96)
    giro = INTRO + A_ + B_
    ch.arpeggi(giro, '1 5 8 5 10 5 8 5', da=0, registro=(50, 76), vel=72)
    ar.accordi(giro, 'x-------', da=0, registro=(55, 71), vel=58)
    cb.basso(A_ + B_, '1 - - - 5 - - -', da=2)
    pc.batteria({'tamburello': '..x...x.', 'triangolo': 'x.......'}, da=10, battute=8)
    b.eco(fl, 'flauto eco', ritardo=24, volume=38)
    b.ritornello(2, 18)
    return b.fine()
