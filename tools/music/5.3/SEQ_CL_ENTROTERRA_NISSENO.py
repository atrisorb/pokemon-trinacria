"""L'entroterra nisseno: Caltanissetta, San Cataldo, Riesi, Mazzarino, Mussomeli, Sutera."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from notazione import Brano, Giro  # noqa: E402

SIMBOLO = 'SEQ_CL_ENTROTERRA_NISSENO'
BANCO = 'BANK_BGM_FIELD11'
VOLUME = 64
SCHEDA = {
    'titolo': 'L\'entroterra nisseno',
    'carattere': 'paesi di zolfo e di grano nel cuore dell\'isola: una marcia lenta di banda di paese, '
                 'quella delle processioni, col clarinetto che canta, i tromboni in levare, la cassa '
                 'sul primo e terzo tempo; nella parte B la tromba prende la melodia',
    'tonalita': 'Re minore (parte B in Fa maggiore)',
    'forma': 'introduzione di 2 battute (tromboni e basso); ritornello A (8) + B (8)',
    'perche_volume': 'HeartGold suona lo slot a 58 con 11 tracce (lo stesso file di '
                     '`SEQ_GS_C_NIBI` e `SEQ_GS_C_TOKIWA`); le 5 voci di questa partitura a 58 resterebbero sotto le musiche vicine '
                     '(zolfara 79, Gela 85)',
}

INTRO = Giro('Dm | A7')
A_ = Giro('Dm | Gm | A7 | Dm | Bb | Gm | E7 A7 | Dm')
B_ = Giro('F | C | Dm | A | Bb | F | Gm A7 | A7')

CLARINETTO = (
    '| a4/4 d5/4 f5/4. e5/8 | d5/4 bb4/4 g4/2 | c#5/4 e5/4 g5/4 a5/4 | f5/2 d5/2 '
    '| d5/4 f5/4 bb5/4. a5/8 | g5/4 d5/4 bb4/2 | b4/4 g#4/4 c#5/4 e5/4 | d5/2. r/4 |'
)
TROMBA = (
    '| c5/4 f5/4 a5/2 | g5/4. e5/8 c5/2 | d5/4 f5/4 a5/4 d6/4 | c#6/2 a5/2 '
    '| bb5/4 f5/4 d5/4 f5/4 | a5/2 c6/2 | bb5/4 g5/4 a5/4 e5/4 | c#5/2 e5/2 |'
)


def partitura(A):
    b = Brano(A, bpm=84)
    cl = b.voce('clarinetto', 34, volume=108, pan=56)
    tr = b.voce('tromba', 29, volume=104, pan=72)
    tb = b.voce('tromboni', 30, volume=78, pan=40)
    cb = b.voce('tuba', 25, volume=98, pan=64)
    bt = b.voce('banda', 39, volume=76, pan=64)
    cl.suona(CLARINETTO, da=2, vel=96)
    tr.suona(TROMBA, da=10, vel=96)
    tb.accordi(INTRO + A_ + B_, '..x...x.', da=0, registro=(50, 64), vel=66, gate=0.6)
    cb.basso(INTRO + A_ + B_, '1 . . . 5 . . .', da=0)
    bt.batteria({'cassa': 'x...x...', 'rullante': '..o...o.'}, da=2, battute=16)
    b.ritornello(2, 18)
    return b.fine()
