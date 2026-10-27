"""La costa e l'entroterra palermitano: Partinico, la diga Jato, Piana degli Albanesi, Bagheria,
Termini Imerese, Cefalù, Monte Pellegrino e le Madonie."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from notazione import Brano, Giro  # noqa: E402

SIMBOLO = 'SEQ_PA_CONCA_D_ORO_CEFALU'
BANCO = 'BANK_BGM_FIELD9'
VOLUME = 85
SCHEDA = {
    'titolo': 'La Conca d\'Oro e Cefalù',
    'carattere': 'campagna di limoni fra il mare e i monti: flauto disteso sopra la chitarra '
                 'arpeggiata e gli archi; nella parte B il Do naturale dentro il Re maggiore (modo '
                 'misolidio) e le campanelle ricordano le chiese bizantine di Piana degli Albanesi',
    'tonalita': 'Re maggiore (parte B misolidia)',
    'forma': 'introduzione di 2 battute (chitarra); ritornello A (8) + B (8)',
}

INTRO = Giro('D | G/D')
A_ = Giro('D | G/D | D | A | Bm | G | Em A | D')
B_ = Giro('C | G | D | D | C | G | A | A')

MELODIA = (
    '| f#5/4. e5/8 d5/4 a5 | b5/2 g5/4 d5 | a5/4. f#5/8 d6/4 a5 | e6/2 c#6/4 a5 '
    '| d6/4. c#6/8 b5/4 f#5 | g5/4 b5/8 a5 g5/4 d5 | e5/4 g5 a5 c#6 | d6/2. r/4 '
    '| e6/4. d6/8 c6/4 g5 | b5/4. a5/8 g5/4 d5 | f#5/4 a5 d6 f#6 | f#6/8 e6 d6 c#6 a5/2 '
    '| g5/4. e5/8 c5/4 e5 | d5/4 g5 b5 d6 | c#6/4. b5/8 a5/4 e5 | e5/2 a4/2 |'
)


def partitura(A):
    b = Brano(A, bpm=108)
    fl = b.voce('flauto', 35, volume=108, pan=64)
    ch = b.voce('chitarra', 7, volume=80, pan=90)
    ar = b.voce('archi', 24, volume=66, pan=36)
    gl = b.voce('campanelle', 10, volume=58, pan=100)
    bs = b.voce('basso', 19, volume=98, pan=64)
    bt = b.voce('batteria', 39, volume=60, pan=64)
    fl.suona(MELODIA, da=2, vel=96)
    b.eco(fl, 'flauto eco', ritardo=24, volume=40)
    giro = INTRO + A_ + B_
    ch.arpeggi(giro, '1 5 8 10 12 10 8 5', da=0, registro=(50, 76), vel=70)
    ar.accordi(A_ + B_, 'x-------', da=2, registro=(55, 70), vel=58)
    gl.accordi(B_, 'x.......', da=10, registro=(74, 88), vel=56, voci=2)
    bs.basso(giro, '1 . . 5 1 . . .', da=0, registro=(33, 52))
    bt.batteria({'hh': 'x.x.x.x.', 'bordo': '..x...x.'}, da=2, battute=16)
    b.ritornello(2, 18)
    return b.fine()
