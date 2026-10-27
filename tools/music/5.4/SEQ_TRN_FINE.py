"""La schermata «Fine» dopo i titoli di coda: il carillon (src/credits/credits.c lo avvia dopo
380 fotogrammi sulla schermata finale)."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from notazione import Brano, Giro  # noqa: E402

SIMBOLO = 'SEQ_TRN_FINE'
BANCO = 'BANK_BGM_OPEND'
VOLUME = 74
SCHEDA = {
    'titolo': 'Fine',
    'carattere': 'un carillon: il tema delle dimissioni un\'ottava sopra sul glockenspiel, come nella '
                 'scatola musicale di HeartGold, con la celesta che arpeggia piano; l\'ultima battuta '
                 'chiude in Do maggiore invece che in Do minore, l\'unica luce dopo i titoli di coda',
    'tonalita': 'Do minore (ultima battuta in Do maggiore)',
    'forma': 'ritornello di 8 battute, dalla prima battuta',
}

GIRO = Giro('Cm | Ab | Fm | G | Cm | Ab | Dm7b5 G | C')
MELODIA = ('| g5/2 eb5/4 c5 | c6/2. ab5/4 | f5/4. g5/8 ab5/4 c6 | b5/2 d5/2 '
           '| eb5/4. f5/8 g5/4 c6 | eb6/2 c6/4 ab5 | ab5/4 f5 g5 b4 | c5/1 |')


def partitura(A):
    b = Brano(A, bpm=70)
    gl = b.voce('carillon', 10, volume=110, pan=64)
    ce = b.voce('celesta', 27, volume=70, pan=40)
    gl.suona(MELODIA, da=0, vel=86, trasponi=12)
    ce.arpeggi(GIRO, '1 5 8 5 10 5 8 5', da=0, registro=(60, 84), vel=58)
    b.ritornello(0, 8)
    return b.fine()
