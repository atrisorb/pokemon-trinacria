"""Lotta con la Fenice dell'Etna (Ho-Oh, FeniceEtna) sulla bocca del Cratere Centrale (P-04)."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from notazione import Brano, Giro  # noqa: E402

SIMBOLO = 'SEQ_TRN_LOTTA_FENICE_ETNEA'
BANCO = 'BANK_BGM_BATTLE7'
VOLUME = 79
SCHEDA = {
    'titolo': 'La Fenice dell\'Etna',
    'carattere': 'il fuoco antico del vulcano che si placa solo con la riconciliazione: inno maestoso '
                 'in Mi bemolle per tromba e corni, archi che salgono a crome come la lava, timpani e '
                 'piatti; la parte B scende in Do minore, la collera della montagna, e risale',
    'tonalita': 'Mi bemolle maggiore (parte B in Do minore)',
    'forma': 'introduzione di 2 battute; ritornello A (8) + B (8)',
}

INTRO = Giro('Cm | Bb')
A_ = Giro('Eb | Bb | Cm | Ab | Eb | Bb | Ab Bb | Eb')
B_ = Giro('Cm | G | Ab | Eb | Fm | Bb | Ab | Bb7')

APERTURA = '| c5/8 eb5 g5 c6 eb6/4 g6 | f6/4 d6 bb5 f5 |'
MELODIA = (
    '| eb5/4 g5/8 ab5 bb5/4 eb6 | d6/2 bb5/4 f5 | g5/4. ab5/8 g5/4 eb5 | c6/4 eb6 ab6 eb6 '
    '| g6/4. f6/8 eb6/4 bb5 | bb5/4 d6 f6 bb6 | ab6/4 eb6 f6 d6 | eb6/2. r/4 '
    '| c6/4. d6/8 eb6/4 g6 | g6/4. f6/8 d6/4 b5 | c6/4 eb6 ab6 eb6 | g6/2 eb6/4 bb5 '
    '| ab5/4. g5/8 f5/4 c6 | d6/4 f6 bb6 f6 | eb6/4. c6/8 ab5/4 c6 | d6/2 ab5/4 f5 |'
)


def partitura(A):
    b = Brano(A, bpm=160)
    tr = b.voce('tromba', 29, volume=116, pan=64)
    co = b.voce('corni', 32, volume=84, pan=30)
    ar = b.voce('lava', 23, volume=80, pan=98)
    bs = b.voce('tromboni', 30, volume=106, pan=64)
    tp = b.voce('timpani', 28, volume=104, pan=64)
    bt = b.voce('batteria', 39, volume=92, pan=64)
    tr.suona(APERTURA, da=0, vel=106).suona(MELODIA, da=2, vel=104)
    giro = INTRO + A_ + B_
    co.accordi(A_ + B_, 'x---x---', da=2, registro=(51, 65), vel=68, voci=2)
    ar.arpeggi(giro, '1 5 8 10 12 10 8 5', da=0, registro=(51, 79), vel=70, gate=0.6)
    bs.basso(giro, '1 . 5 . 1 . 5 .', da=0, registro=(31, 50))
    tp.basso(giro, '1 . . . 5, . . .', da=0, registro=(41, 53), vel=106, gate=0.5)
    bt.batteria({'cassa': 'x.......x.......', 'rullante': 'xxxxxxxxXXXXXXXX'}, da=0, battute=2)
    bt.batteria({'cassa': 'x.....x.x.......', 'rullante': '....x.......x...', 'hh': 'x.x.x.x.x.x.x.x.'},
                da=2, battute=16)
    b.ritornello(2, 18)
    return b.fine()
