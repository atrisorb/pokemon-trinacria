"""La costa iblea: Marina di Ragusa, Pozzallo, Santa Croce Camerina, Punta Secca."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from notazione import Brano, Giro  # noqa: E402

SIMBOLO = 'SEQ_RG_COSTA_IBLEA'
BANCO = 'BANK_BGM_FIELD17'
VOLUME = 75
SCHEDA = {
    'titolo': 'La costa iblea',
    'carattere': 'estate sul mare del sud, lungomari, il faro di Punta Secca e la granita a metà '
                 'pomeriggio: canzone leggera col flauto, chitarra in levare, vibrafono che gira, '
                 'charleston e bordo',
    'tonalita': 'Mi maggiore',
    'forma': 'introduzione di 2 battute (chitarra e vibrafono); ritornello A (8) + B (8)',
}

INTRO = Giro('E | A')
A_ = Giro('E | B | C#m | A | E | B | A B | E')
B_ = Giro('A | E/G# | F#m | B | A | E/G# | F#m7 | B7')

MELODIA = (
    '| b4/4 e5/8 f#5/8 g#5/4 b5/4 | b5/4 f#5/4 d#5/2 | e5/4 g#5/4 c#6/4. b5/8 | a5/2 e5/2 '
    '| g#5/4. f#5/8 e5/4 g#5/4 | f#5/2 b5/2 | c#6/4 a5/4 b5/4 d#5/4 | e5/2. r/4 '
    '| c#6/4 e6/4 a5/2 | b5/4. g#5/8 e5/2 | f#5/4 a5/4 c#6/2 | d#6/2 b5/2 '
    '| e6/4 c#6/4 a5/4 c#6/4 | b5/2 g#5/2 | a5/4 f#5/4 c#5/4 e5/4 | d#5/2 f#5/2 |'
)


def partitura(A):
    b = Brano(A, bpm=116)
    fl = b.voce('flauto', 35, volume=110, pan=64)
    ch = b.voce('chitarra', 14, volume=74, pan=40)
    vb = b.voce('vibrafono', 5, volume=64, pan=92)
    bs = b.voce('basso', 19, volume=96, pan=64)
    bt = b.voce('batteria', 39, volume=72, pan=64)
    fl.suona(MELODIA, da=2, vel=96)
    giro = INTRO + A_ + B_
    ch.accordi(giro, '.x.x.x.x', da=0, registro=(56, 71), vel=62, gate=0.5)
    vb.arpeggi(giro, '1 5 8 5 10 5 8 5', da=0, registro=(64, 84), vel=62)
    bs.basso(giro, '1 . . 5 1 . 5 .', da=0)
    bt.batteria({'hh': 'x.x.x.x.', 'bordo': '..x...x.', 'cassa': 'x...x...'}, da=0, battute=18)
    b.ritornello(2, 18)
    return b.fine()
