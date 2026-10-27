"""Caltagirone e la Scalinata di Santa Maria del Monte: 142 gradini di ceramica (S-CT-07, D-CT-05)."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from notazione import Brano, Giro  # noqa: E402

SIMBOLO = 'SEQ_CT_CALTAGIRONE'
BANCO = 'BANK_BGM_FIELD7'
VOLUME = 68
SCHEDA = {
    'titolo': 'Caltagirone',
    'carattere': 'la città della ceramica: luminosa e colorata; nella parte A il basso sale di grado '
                 '(La–Si–Do#–Re–Mi–Fa#) e la melodia sale con lui come i gradini della Scalinata; '
                 'marimba e vibrafono come piastrelle lucide',
    'tonalita': 'La maggiore',
    'forma': 'introduzione di 2 battute (marimba); ritornello A (8) + B (8)',
}

INTRO = Giro('A | E')
A_ = Giro('A | Bm | C#m | D | E | F#m | D E | A')
B_ = Giro('D | E | C#m | F#m | Bm | E7 | A/C# D | E7')

MELODIA = (
    '| e5/8 f#5 a5/4 c#6 a5 | f#5/8 g#5 b5/4 d6 b5 | g#5/8 a5 c#6/4 e6 c#6 | a5/8 b5 d6/4 f#6 d6 '
    '| e6/4. d6/8 b5/4 g#5 | a5/4. f#5/8 c#6/4 a5 | f#5/4 a5 g#5 b5 | a5/2. r/4 '
    '| f#6/4. e6/8 d6/4 a5 | g#5/2 b5/4 e6 | e6/4. c#6/8 g#5/4 e5 | f#5/2 a5/4 c#6 '
    '| d6/4. c#6/8 b5/4 f#5 | g#5/4 b5 e6 d6 | c#6/4 a5 a5 f#5 | g#5/2 b5/4 d6 |'
)


def partitura(A):
    b = Brano(A, bpm=116)
    fl = b.voce('flauto', 35, volume=106, pan=64)
    mr = b.voce('marimba', 18, volume=90, pan=36)
    vb = b.voce('vibrafono', 5, volume=70, pan=100)
    bs = b.voce('basso', 19, volume=104, pan=64)
    bt = b.voce('batteria', 39, volume=72, pan=64)
    fl.suona(MELODIA, da=2, vel=98)
    giro = INTRO + A_ + B_
    mr.arpeggi(giro, '1 3 5 8 5 3 1 3', da=0, registro=(57, 81), vel=76)
    vb.accordi(A_ + B_, 'x---x---', da=2, registro=(64, 79), vel=56)
    bs.basso(giro, '1 - 5 - 8 - 5 -', da=0)
    bt.batteria({'bordo': '..x...x.', 'hh': 'oooooooo', 'tamburello': '...o...o'}, da=2, battute=16)
    b.eco(fl, 'flauto eco', ritardo=12, volume=40)
    b.ritornello(2, 18)
    return b.fine()
