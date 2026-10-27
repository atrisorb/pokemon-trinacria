"""La burocrazia magnetica dal 1971 negli Archivi della Società Stretto Eterna."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from notazione import Brano, Giro  # noqa: E402

SIMBOLO = 'SEQ_ME_ARCHIVI_MAGNETICI'
BANCO = 'BANK_BASIC'
VOLUME = 89
SCHEDA = {
    'titolo': 'Gli Archivi magnetici',
    'carattere': 'cinquant\'anni di progetti del Ponte su nastro magnetico: musica ripetitiva che non '
                 'arriva mai da nessuna parte, marimba che gira come le bobine, legnetto da orologio, '
                 'bordo da macchina da scrivere col campanello (triangolo) a fine riga, clarinetto '
                 'che sospira note lunghe; ogni frase chiude sull\'accordo napoletano (Sol maggiore in '
                 'Fa diesis minore), la firma di «U Sistema» (R-AUD-21)',
    'tonalita': 'Fa diesis minore',
    'forma': 'introduzione di 2 battute (marimba e orologio); ritornello A (8) + B (8)',
}

INTRO = Giro('F#m | F#m')
A_ = Giro('F#m | D | Bm | C#7 | F#m | D | G | C#7')
B_ = Giro('D | A | Bm | F#m | D | Bm | G | C#7')

CLARINETTO = (
    '| c#5/1 | d5/2 f#5/2 | f#5/2. d5/4 | e#5/1 '
    '| a5/2 c#6/2 | a5/2. f#5/4 | b5/2 g5/2 | g#5/2 e#5/2 '
    '| f#5/4 a5/4 d6/2 | c#6/2 e5/2 | d5/4 f#5/4 b5/2 | a5/1 '
    '| a5/4 f#5/4 d5/2 | b4/2 d5/2 | g5/2. b5/4 | b5/2 g#5/2 |'
)
UFFICIO = {'legnetto': 'x...x...', 'bordo': '.o.o..o.'}
FINE_RIGA = {'legnetto': 'x...x...', 'bordo': '.o.o....', 'triangolo': '......x.'}


def partitura(A):
    b = Brano(A, bpm=112)
    cl = b.voce('clarinetto', 34, volume=100, pan=64)
    mr = b.voce('bobine', 18, volume=86, pan=40)
    ce = b.voce('celesta', 27, volume=66, pan=92)
    bs = b.voce('basso', 21, volume=96, pan=64)
    bt = b.voce('ufficio', 39, volume=70, pan=64)
    cl.suona(CLARINETTO, da=2, vel=92)
    giro = INTRO + A_ + B_
    mr.arpeggi(giro, '1 5 8 5 10 5 8 5', da=0, registro=(54, 78), vel=72)
    ce.arpeggi(B_, '12 . 10 . 8 . 10 .', da=10, registro=(66, 90), vel=60)
    bs.basso(giro, '1 . . . 1 . . .', da=0)
    bt.batteria([UFFICIO, FINE_RIGA, UFFICIO, UFFICIO], da=0, battute=18)   # campanello a fine frase
    b.ritornello(2, 18)
    return b.fine()
