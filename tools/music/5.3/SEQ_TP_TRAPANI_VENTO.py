"""Il vento di Trapani: Saline, Marsala, Stagnone, Mazara, Castelvetrano, Selinunte, Alcamo,
Castellammare, lo Zingaro, San Vito e Favignana."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from notazione import Brano, Giro  # noqa: E402

SIMBOLO = 'SEQ_TP_TRAPANI_VENTO'
BANCO = 'BANK_BGM_FIELD12'
VOLUME = 87
SCHEDA = {
    'titolo': 'Il vento di Trapani',
    'carattere': 'la provincia del vento, dei mulini delle saline e della casbah di Mazara: archi a '
                 'sedicesime che non si fermano come il maestrale, flauto con la seconda aumentata '
                 '(Fa–Sol diesis) della costa africana, chitarra, basso e un ritmo di tamburi a '
                 'mano alla maniera della darbuka',
    'tonalita': 'La minore (minore armonica; parte B in Do maggiore)',
    'forma': 'introduzione di 2 battute (archi e tamburi); ritornello A (8) + B (8)',
}

INTRO = Giro('Am | E')
A_ = Giro('Am | Am | Dm | E | F | Dm | E | E7')
B_ = Giro('F | G | C | Am | Dm | G | E | E7')

MELODIA = (
    '| a5/4 c6/8 b5/8 a5/4 e5/4 | e6/4. d6/8 c6/4 a5/4 | d6/4 f6/4 a6/4 f6/4 | g#6/4. f6/8 e6/2 '
    '| f6/4 c6/4 a5/4 c6/4 | d6/4. f6/8 a5/2 | b5/4 g#5/4 e5/4 g#5/4 | b5/2 d6/2 '
    '| c6/4 a5/4 f5/4 a5/4 | b5/4. d6/8 g6/2 | e6/4 g6/4 c6/2 | a5/4 c6/4 e6/2 '
    '| f6/4 d6/4 a5/4 d6/4 | b5/2 d6/2 | e6/4 b5/4 g#5/4 b5/4 | d6/2 g#5/2 |'
)


def partitura(A):
    b = Brano(A, bpm=144)
    fl = b.voce('flauto', 35, volume=110, pan=64)
    ar = b.voce('vento', 23, volume=82, pan=40)
    ch = b.voce('chitarra', 14, volume=66, pan=92)
    bs = b.voce('basso', 22, volume=98, pan=64)
    bt = b.voce('tamburi', 39, volume=80, pan=64)
    fl.suona(MELODIA, da=2, vel=98)
    giro = INTRO + A_ + B_
    ar.arpeggi(giro, '1 5 8 5 1 5 8 5 1 5 8 5 1 5 8 5', da=0, registro=(52, 72), vel=70, gate=0.6)
    ch.accordi(A_ + B_, 'x...x...', da=2, registro=(55, 70), vel=58, gate=0.6)
    bs.basso(giro, '1 . 1 8 1 . 5 .', da=0)
    bt.batteria({'cassa': 'x.....x...x.....', 'bordo': '...x.....x..x...', 'tamburello': '..x...x...x...x.'},
                da=0, battute=18)
    b.eco(fl, 'flauto eco', ritardo=12, volume=36)
    b.ritornello(2, 18)
    return b.fine()
