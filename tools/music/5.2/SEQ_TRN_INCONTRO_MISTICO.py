"""Incontro: frati, eremiti, maghe."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from notazione import Brano, Giro  # noqa: E402

SIMBOLO = 'SEQ_TRN_INCONTRO_MISTICO'
BANCO = 'BANK_BASIC'
VOLUME = 84
SCHEDA = {
    'titolo': 'Incontro — mistici',
    'carattere': 'saio, candele e malocchio: modo frigio di Re (il Mi bemolle accanto al Re), organo '
                 'tenuto, flauto dolce che canta, campanelle acute',
    'tonalita': 'Re frigio',
    'forma': 'introduzione di 1 battuta; ritornello di 8 battute',
}

INTRO = Giro('Dm Eb')
GIRO = Giro('Dm | Eb | Dm | C | Bb | Eb | Gm A | Dm')

MELODIA = (
    '| d5/2 eb5 | d5/4. eb5/8 f5/4 a5 | g5/4. f5/8 eb5/4 bb4 | a5/4 f5 d5 f5 | e5/2 g5/4 c5 '
    '| d5/4 f5 bb5 f5 | eb5/2 g5/4 bb5 | bb5/4 g5 a5 c#5 | d5/1 |'
)


def partitura(A):
    b = Brano(A, bpm=108)
    fd = b.voce('flauto dolce', 38, volume=112, pan=64)
    og = b.voce('organo', 11, volume=80, pan=40)
    cp = b.voce('campanelle', 10, volume=72, pan=100)
    bs = b.voce('contrabbasso', 25, volume=100, pan=64)
    tm = b.voce('tamburo', 39, volume=72, pan=64)
    fd.suona(MELODIA, da=0, vel=98)
    giro = INTRO + GIRO
    og.accordi(giro, 'x---x---', da=0, registro=(53, 67), vel=70, gate=0.97)
    cp.arpeggi(GIRO, '8 . . . 12 . . .', da=1, registro=(74, 90), vel=76)
    bs.basso(giro, '1 - - - 1 - - -', da=0, registro=(26, 45), gate=0.95)
    tm.batteria({'tom_b': 'x.......', 'tom_m': '....o...'}, da=1, battute=8)
    b.ritornello(1, 9)
    return b.fine()
