"""I santuari segreti del post-game: la vetta di Rocca Busambra, Pantelleria e lo Specchio di
Venere, la Sciara del Fuoco e l'Abisso di Cariddi (P-03…P-08)."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from notazione import Brano, Giro  # noqa: E402

SIMBOLO = 'SEQ_TRN_FANTASMI_LEGGENDARI'
BANCO = 'BANK_BASIC'
VOLUME = 89
SCHEDA = {
    'titolo': 'I Fantasmi della Prima Repubblica',
    'carattere': 'luoghi antichi dove i vecchi burattinai custodiscono i leggendari: organo tenuto, '
                 'coro lento, arpa e celesta come una reliquia, una voce d\'ancia che racconta; i '
                 'Fantasmi hanno creato «U Sistema», quindi le frasi chiudono sul La bemolle '
                 'napoletano (R-AUD-21)',
    'tonalita': 'Sol minore',
    'forma': 'introduzione di 2 battute (organo); ritornello A (8) + B (8)',
}

INTRO = Giro('Gm | D')
A_ = Giro('Gm | Gm | Eb | D | Gm | Cm | Ab | D')
B_ = Giro('Cm | Gm | Ab | D | Eb | Bb | Ab | D7')

MELODIA = (
    '| d5/2. bb4/4 | g5/2 d5/4 bb5 | g5/4. f5/8 eb5/4 bb4 | a4/2 f#5/4 d5 '
    '| bb5/4. a5/8 g5/4 d5 | eb5/4 g5 c6 eb6 | eb6/2 c6/4 ab5 | a5/2. r/4 '
    '| c6/2 g5/4 eb5 | d5/4 g5 bb5 d6 | c6/4. bb5/8 ab5/4 eb5 | f#5/2 a5/4 d6 '
    '| eb6/4. d6/8 bb5/4 g5 | f5/4 bb5 d6 f6 | eb6/4 c6 ab5 c6 | c6/2 a5/4 f#5 |'
)


def partitura(A):
    b = Brano(A, bpm=80)
    ob = b.voce('racconto', 33, volume=104, pan=60)
    og = b.voce('organo', 12, volume=66, pan=40)
    co = b.voce('coro', 32, volume=70, pan=90)
    ar = b.voce('arpa', 26, volume=70, pan=100)
    ce = b.voce('celesta', 27, volume=52, pan=24)
    cb = b.voce('contrabbasso', 25, volume=90, pan=64)
    tp = b.voce('timpani', 28, volume=70, pan=64)
    ob.suona(MELODIA, da=2, vel=92)
    giro = INTRO + A_ + B_
    og.accordi(giro, 'x-------', da=0, registro=(55, 69), vel=58)
    co.accordi(B_, 'x---x---', da=10, registro=(60, 74), vel=56)
    ar.arpeggi(giro, '1 5 8 10 12 10 8 5', da=0, registro=(43, 72), vel=60)
    ce.arpeggi(A_, '. . . . 15 . . .', da=2, registro=(67, 86), vel=54)
    cb.basso(giro, '1 - - - - - - -', da=0, registro=(26, 45), gate=0.95)
    tp.basso(giro, '1 . . . . . . .', da=0, registro=(41, 53), vel=72, gate=0.5)
    b.ritornello(2, 18)
    return b.fine()
