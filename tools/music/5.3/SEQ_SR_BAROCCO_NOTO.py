"""Il barocco di Noto e Avola."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from notazione import Brano, Giro  # noqa: E402

SIMBOLO = 'SEQ_SR_BAROCCO_NOTO'
BANCO = 'BANK_BGM_FIELD14'
VOLUME = 63
SCHEDA = {
    'titolo': 'Il barocco di Noto',
    'carattere': 'la città d\'oro ricostruita dopo il 1693: concerto barocco per tromba in Re, continuo '
                 'di tastiera a crome, archi e violoncello, timpani alle cadenze; la parte B scende '
                 'per gradi come le scalinate delle chiese, col flauto all\'ottava sopra la tromba',
    'tonalita': 'Re maggiore',
    'forma': 'introduzione di 2 battute (continuo); ritornello A (8) + B (8)',
}

INTRO = Giro('D | A7')
A_ = Giro('D | A/C# | Bm | F#m/A | G | D/F# | Em7 A7 | D')
B_ = Giro('Bm | F#m | G | D | Em | A | D/F# G | A7')

TROMBA = (
    '| a4/4 d5/8 e5/8 f#5/4 a5/4 | e5/4 c#5/8 d5/8 e5/2 | d5/4 f#5/4 b5/4. a5/8 | a5/4 f#5/4 c#5/2 '
    '| b4/4 d5/8 e5/8 g5/4 b5/4 | a5/4. f#5/8 d5/2 | e5/4 g5/4 c#5/4 e5/4 | d5/2. r/4 '
    '| f#5/4 b5/4 d6/4 b5/4 | c#6/4. a5/8 f#5/2 | g5/4 b5/4 d6/4 g5/4 | f#5/2 a5/2 '
    '| e5/4 g5/4 b5/4 e6/4 | c#6/4. b5/8 a5/2 | f#5/4 a5/4 b5/4 d6/4 | e6/2 c#6/4 a5/4 |'
)


def partitura(A):
    b = Brano(A, bpm=112)
    tr = b.voce('tromba', 29, volume=108, pan=64)
    co = b.voce('continuo', 2, volume=84, pan=40)
    ar = b.voce('archi', 23, volume=78, pan=88)
    vc = b.voce('violoncello', 25, volume=96, pan=64)
    tp = b.voce('timpani', 28, volume=88, pan=64)
    tr.suona(TROMBA, da=2, vel=96)
    giro = INTRO + A_ + B_
    co.arpeggi(giro, '1 5 8 5 1 5 8 5', da=0, registro=(50, 74), vel=72)
    ar.accordi(A_ + B_, 'x...x...', da=2, registro=(60, 76), vel=62)
    vc.basso(giro, '1 . 1 . 1 . 1 .', da=0)
    tp.basso(A_ + B_, '1 . . . . . . .', da=2, registro=(45, 57), vel=90, gate=0.5)
    b.eco(tr, 'flauto ottava', ritardo=0, programma=35, trasponi=12, volume=56)
    b.ritornello(2, 18)
    return b.fine()
