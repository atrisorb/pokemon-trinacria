"""La costa di Vendicari (esterno della riserva)."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from notazione import Brano, Giro  # noqa: E402

SIMBOLO = 'SEQ_SR_VENDICARI_COSTA'
BANCO = 'BANK_BGM_FIELD18'
VOLUME = 73
SCHEDA = {
    'titolo': 'La costa di Vendicari',
    'carattere': 'dune, pantani e la torre sveva prima di entrare nella riserva: passeggiata '
                 'luminosa col flauto, celesta che gira in alto come il volo dei fenicotteri, '
                 'pizzicato leggero e spazzole',
    'tonalita': 'Fa maggiore',
    'forma': 'introduzione di 2 battute (celesta); ritornello A (8) + B (8)',
}

INTRO = Giro('F | C')
A_ = Giro('F | Am | Bb | C | F | Dm | Gm C | F')
B_ = Giro('Bb | C | Am | Dm | Gm | C | Bb C | C7')

MELODIA = (
    '| c5/4 f5/8 g5/8 a5/4 c6/4 | e6/4. c6/8 a5/2 | bb5/4 d6/4 f6/4 d6/4 | e6/2 c6/2 '
    '| a5/4 c6/8 a5/8 f5/4 a5/4 | d6/4. a5/8 f5/2 | g5/4 bb5/4 c6/4 e5/4 | f5/2. r/4 '
    '| d6/4 f6/8 d6/8 bb5/2 | c6/4 e6/4 g6/2 | e6/4. c6/8 a5/2 | f5/4 a5/4 d6/2 '
    '| bb5/4 g5/4 d6/4 bb5/4 | c6/2. g5/4 | f5/4 d5/4 e5/4 g5/4 | bb5/2 c6/2 |'
)


def partitura(A):
    b = Brano(A, bpm=120)
    fl = b.voce('flauto', 35, volume=110, pan=64)
    ce = b.voce('celesta', 27, volume=78, pan=36)
    pz = b.voce('pizzicato', 16, volume=76, pan=92)
    bs = b.voce('basso', 19, volume=96, pan=64)
    bt = b.voce('spazzole', 39, volume=64, pan=64)
    fl.suona(MELODIA, da=2, vel=96)
    giro = INTRO + A_ + B_
    ce.arpeggi(giro, '8 5 10 5 12 5 10 5', da=0, registro=(60, 84), vel=70)
    pz.accordi(A_ + B_, '..x...x.', da=2, registro=(55, 70), vel=64, gate=0.6)
    bs.basso(giro, '1 . . 1 5 . . .', da=0)
    bt.batteria({'hh': 'x.x.x.x.', 'bordo': '....x...'}, da=2, battute=16)
    b.ritornello(2, 18)
    return b.fine()
