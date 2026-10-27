"""Il Vermut di via Gemmellaro: il «chill» dell'aperitivo (M-CT-02, Il Vermut e la scintilla)."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from notazione import Brano, Giro  # noqa: E402

SIMBOLO = 'SEQ_CT_VERMUT'
BANCO = 'BANK_BGM_FIELD2'
VOLUME = 78
SCHEDA = {
    'titolo': 'Il Vermut',
    'carattere': 'aperitivo tranquillo in via Gemmellaro, bossa nova da locale: accordi di settima, '
                 'chitarra in levare, clarinetto morbido; il posto dove Turi, Maria e il Prof. Strano '
                 'accendono la «scintilla»',
    'tonalita': 'Fa maggiore',
    'forma': 'introduzione di 2 battute (chitarra e basso); ritornello A (8) + B (8)',
}

INTRO = Giro('Fmaj7 | Gm7 C7')
A_ = Giro('Fmaj7 | Fmaj7 | Gm7 | C7 | Am7 | D7 | Gm7 | C7')
B_ = Giro('Bbmaj7 | Bbm6 | Am7 | D7b9 | Gm7 | C9 | Fmaj7 | Gm7 C7')

MELODIA = (
    '| a4/4. g4/8 a4/4 c5 | e5/2 r/4 c5/8 d5 | f5/4. d5/8 bb4/4 g4 | e5/2. r/4 '
    '| e5/4. d5/8 c5/4 a4 | f#5/4. e5/8 d5/4 c5 | bb4/4 d5/8 f5 g5/4 f5 | e5/2 g4/4 bb4 '
    '| d5/4. c5/8 d5/4 f5 | db5/2 bb4/4 g4 | c5/4. b4/8 c5/4 e5 | f#5/2 eb5/4 c5 '
    '| bb4/4. a4/8 bb4/4 d5 | e5/4 d5 bb4 g4 | a4/2. r/4 | g4/4 bb4 c5 e5 |'
)


def partitura(A):
    b = Brano(A, bpm=100)
    cl = b.voce('clarinetto', 34, volume=110, pan=60)
    gt = b.voce('chitarra', 7, volume=96, pan=30)
    vb = b.voce('vibrafono', 5, volume=72, pan=100)
    bs = b.voce('basso', 19, volume=108, pan=64)
    bt = b.voce('batteria', 39, volume=70, pan=64)
    cl.suona(MELODIA, da=2, vel=96)
    giro = INTRO + A_ + B_
    gt.accordi(giro, 'x..x..x...x..x..', da=0, registro=(55, 70), vel=68, voci=4)
    vb.arpeggi(A_ + B_, '. . . 10 . 12 . .', da=2, registro=(62, 84), vel=64)
    bs.basso(giro, '1 - - 5 5 - - .', da=0)
    bt.batteria({'bordo': 'x..x..x...x..x..', 'hh': 'oooooooooooooooo', 'cassa': 'x.......x.......'},
                da=0, battute=18, dur_max=6)
    b.eco(cl, 'clarinetto eco', ritardo=16, volume=38)
    b.ritornello(2, 18)
    return b.fine()
