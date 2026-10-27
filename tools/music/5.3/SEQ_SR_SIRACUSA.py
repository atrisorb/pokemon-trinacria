"""Siracusa e il mare di Ortigia (con la radio di Siracusa)."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from notazione import Brano, Giro  # noqa: E402

SIMBOLO = 'SEQ_SR_SIRACUSA'
BANCO = 'BANK_BGM_FIELD12'
VOLUME = 73
SCHEDA = {
    'titolo': 'Siracusa e Ortigia',
    'carattere': 'la città greca sul mare: arpa arpeggiata come una lira, flauto disteso, archi '
                 'pieni; l\'accordo di Fa maggiore dentro il Mi bemolle (quarta aumentata) dà la luce '
                 'chiara del mare di Ortigia, il triangolo luccica nella parte B',
    'tonalita': 'Mi bemolle maggiore',
    'forma': 'introduzione di 2 battute (arpa); ritornello A (8) + B (8)',
}

INTRO = Giro('Eb | Ab/Eb')
A_ = Giro('Eb | Bb/D | Cm | Ab | Eb | F | Bb7sus4 | Bb7')
B_ = Giro('Ab | Eb/G | Fm | Bb | Cm | Ab | F7 | Bb7')

MELODIA = (
    '| g5/4. ab5/8 bb5/2 | f5/4 d5/4 bb4/2 | c5/4 eb5/4 g5/4 c6/4 | c6/2. ab5/4 '
    '| bb5/4. g5/8 eb5/4 g5/4 | a5/2 f5/4 c6/4 | eb6/4 bb5/4 f5/4 ab5/4 | d6/2. r/4 '
    '| c6/4 eb6/4 ab6/2 | g6/4. f6/8 eb6/2 | f6/4 c6/4 ab5/4 c6/4 | d6/2 bb5/2 '
    '| eb6/4 c6/4 g5/2 | ab5/4 c6/4 eb6/2 | eb6/4 c6/4 a5/4 f5/4 | d5/2 f5/2 |'
)


def partitura(A):
    b = Brano(A, bpm=96)
    fl = b.voce('flauto', 35, volume=110, pan=64)
    ap = b.voce('arpa', 26, volume=92, pan=40)
    ar = b.voce('archi', 23, volume=80, pan=88)
    cb = b.voce('contrabbasso', 25, volume=96, pan=64)
    tr = b.voce('triangolo', 39, volume=60, pan=96)
    fl.suona(MELODIA, da=2, vel=96)
    ap.arpeggi(INTRO + A_ + B_, '1 5 8 10 12 10 8 5', da=0, registro=(51, 79), vel=76)
    ar.accordi(A_ + B_, 'x-------', da=2, registro=(55, 72), vel=62)
    cb.basso(INTRO + A_ + B_, '1 - - - 5 - - -', da=0)
    tr.batteria({'triangolo': '....x...'}, da=10, battute=8)
    b.eco(fl, 'flauto eco', ritardo=12, volume=38)
    b.ritornello(2, 18)
    return b.fine()
