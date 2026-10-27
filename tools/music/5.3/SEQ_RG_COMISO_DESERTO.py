"""L'aeroporto di Comiso e la base NATO: la cattedrale nel deserto."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from notazione import Brano, Giro  # noqa: E402

SIMBOLO = 'SEQ_RG_COMISO_DESERTO'
BANCO = 'BANK_BGM_DUNGEON5'
VOLUME = 87
SCHEDA = {
    'titolo': 'La cattedrale nel deserto',
    'carattere': 'un aeroporto grande e vuoto con le luci a risparmio: il «din-don» degli annunci '
                 '(lo stesso timbro di Fontanarossa) senza nessun annuncio, poche note lunghe di '
                 'vibrafono che rimbalzano in due echi lontani, organo dolce tenuto, contrabbasso e '
                 'una celesta che si accende a tratti come un neon',
    'tonalita': 'La minore (accordi sospesi)',
    'forma': 'introduzione di 2 battute («din-don» e silenzio); ritornello A (8) + B (8)',
}

INTRO = Giro('Asus2 | Asus2')
A_ = Giro('Am | Fmaj7 | C | G | Am | Fmaj7 | Dm7 | Esus4 E')
B_ = Giro('Fmaj7 | G | Em7 | Am | Fmaj7 | G | Asus2 | Asus2')

VIBRAFONO = (
    '| e6/4 b5/4 r/2 | r/1 '
    '| e5/2. r/4 | a5/2 c6/4 r/4 | g5/1 | r/2 d5/4 b4/4 '
    '| c5/2. e5/4 | a5/2. e5/4 | f5/2 d5/2 | a4/2 g#4/2 '
    '| c6/2 e6/2 | d6/2. b5/4 | g5/2 e5/4 d5/4 | e5/1 '
    '| a5/2 c6/2 | b5/2 d6/2 | e6/1 | r/1 |'
)


def partitura(A):
    b = Brano(A, bpm=76)
    vb = b.voce('vibrafono', 5, volume=104, pan=64)
    og = b.voce('organo dolce', 12, volume=58, pan=64)
    cb = b.voce('contrabbasso', 25, volume=88, pan=64)
    ce = b.voce('neon', 27, volume=56, pan=100)
    vb.suona(VIBRAFONO, da=0, vel=92)
    og.accordi(A_ + B_, 'x-------', da=2, registro=(52, 67), vel=56)
    cb.basso(A_ + B_, '1 - - - - - - -', da=2, vel=84)
    ce.arpeggi(B_, '. . . 12 . . . .', da=10, registro=(72, 96), vel=60)
    b.eco(vb, 'vibrafono eco', ritardo=24, volume=50)
    b.eco(vb, 'eco lontana', ritardo=72, volume=30, pan=20)
    b.ritornello(2, 18)
    return b.fine()
