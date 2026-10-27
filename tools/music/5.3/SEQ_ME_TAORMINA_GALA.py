"""Il lusso mondano di Taormina: Isola Bella, Giardini Naxos e il Galà del Teatro Antico."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from notazione import Brano, Giro  # noqa: E402

SIMBOLO = 'SEQ_ME_TAORMINA_GALA'
BANCO = 'BANK_BASIC'
VOLUME = 86
SCHEDA = {
    'titolo': 'Il Galà di Taormina',
    'carattere': 'terrazze sul mare, abiti da sera e il Galà nel Teatro Antico: valzer elegante, '
                 'flauto raddoppiato dal vibrafono, archi in levare, arpa che scintilla nella parte '
                 'B e il triangolo sul primo tempo; un lusso perfetto e un po\' finto',
    'tonalita': 'Mi bemolle maggiore (seconda passata in La bemolle maggiore)',
    'forma': 'introduzione di 2 battute (archi e basso); ritornello A (8) + B (8) in Mi bemolle, poi le stesse 16 battute in La bemolle, in 3/4',
}

INTRO = Giro('Eb | Bb7')
A_ = Giro('Eb | Eb | Bb7 | Bb7 | Bb7 | Bb7 | Eb | Eb')
B_ = Giro('Ab | Ab | Eb | Eb | F7 | F7 | Bb7 | Bb7')

MELODIA = (
    '| bb4/4 eb5/4 g5/4 | bb5/2. | ab5/4 f5/4 d5/4 | bb4/2. '
    '| d5/4 f5/4 ab5/4 | bb5/4. ab5/8 f5/4 | g5/4 eb5/4 bb4/4 | eb5/2. '
    '| c6/4 eb6/4 c6/4 | ab5/2. | g5/4 bb5/4 eb6/4 | bb5/2. '
    '| a5/4 c6/4 eb6/4 | f6/4. eb6/8 c6/4 | d6/4 bb5/4 ab5/4 | f5/2. |'
)


def partitura(A):
    b = Brano(A, bpm=168, metro=(3, 4))
    fl = b.voce('flauto', 35, volume=108, pan=64)
    ar = b.voce('archi', 23, volume=78, pan=88)
    ap = b.voce('arpa', 26, volume=80, pan=36)
    bs = b.voce('basso', 19, volume=96, pan=64)
    tr = b.voce('triangolo', 39, volume=58, pan=100)
    fl.suona(MELODIA, da=2, vel=96)
    giro = INTRO + A_ + B_
    ar.accordi(giro, '..x.x.', da=0, registro=(58, 72), vel=62, gate=0.7)
    ap.arpeggi(B_, '1 5 8 10 8 5', da=10, registro=(63, 87), vel=66)
    bs.basso(giro, '1 . . . . .', da=0)
    tr.batteria({'triangolo': 'x.....'}, da=2, battute=16)
    b.eco(fl, 'vibrafono', ritardo=0, programma=5, volume=60)
    b.ripeti(2, 16, 18, trasponi=5)
    b.ritornello(2, 34)
    return b.fine()
