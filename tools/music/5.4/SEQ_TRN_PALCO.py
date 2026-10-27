"""Il palco di Piazza Duomo a Catania: il comizio finale del nuovo Presidente della Regione (M-EN-07)."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from notazione import Brano, Giro  # noqa: E402

SIMBOLO = 'SEQ_TRN_PALCO'
BANCO = 'BANK_BGM_FIELD1'
VOLUME = 99
SCHEDA = {
    'titolo': 'Il palco',
    'carattere': 'la festa sotto il Liotru: la fanfara della vittoria, in Do maggiore, la stessa tonica '
                 'del Do minore di «U Sistema» e del finale, ma in luce piena; tromba e corni, '
                 'glockenspiel come i coriandoli, archi ribattuti, tromboni, timpani e batteria da banda. '
                 'È la fanfara che nella dissolvenza «si spegne di colpo» (M-EN-08)',
    'tonalita': 'Do maggiore',
    'forma': 'introduzione di 2 battute (fanfara); ritornello A (8) + B (8)',
}

INTRO = Giro('C | G7')
A_ = Giro('C | G | Am | F | C | G | F G | C')
B_ = Giro('F | G | Em | Am | Dm | G | F | G7')

FANFARA = '| c5/8 e5 g5 c6 e6/4 g6 | f6/4 d6 b5 g5 |'
MELODIA = (
    '| c5/4 e5/8 f5 g5/4 c6 | b5/4. a5/8 g5/4 d5 | e5/4 a5 c6 e6 | f6/2 c6/4 a5 '
    '| g5/4. a5/8 g5/4 e5 | d5/4 g5 b5 d6 | c6/4 a5 b5 d6 | c6/2. r/4 '
    '| a5/4. g5/8 f5/4 c6 | b5/4. a5/8 g5/4 d6 | e6/4 b5 g5 b5 | c6/2 a5/4 e5 '
    '| f5/4 a5 d6 f6 | g6/4. f6/8 d6/4 b5 | a6/4 f6 c6 a5 | b5/2 d6/4 f6 |'
)


def partitura(A):
    b = Brano(A, bpm=152)
    tr = b.voce('tromba', 29, volume=116, pan=64)
    gl = b.voce('coriandoli', 10, volume=58, pan=100)
    co = b.voce('corni', 32, volume=82, pan=30)
    ar = b.voce('archi', 23, volume=78, pan=90)
    bs = b.voce('tromboni', 30, volume=104, pan=64)
    tp = b.voce('timpani', 28, volume=96, pan=64)
    bt = b.voce('banda', 39, volume=90, pan=64)
    tr.suona(FANFARA, da=0, vel=108).suona(MELODIA, da=2, vel=104)
    gl.suona(MELODIA, da=2, vel=78, trasponi=12)
    giro = INTRO + A_ + B_
    co.accordi(A_ + B_, 'x---x---', da=2, registro=(52, 67), vel=64, voci=2)
    ar.accordi(giro, 'x.xx.xx.', da=0, registro=(57, 72), vel=66, gate=0.6)
    bs.basso(giro, '1 . 5 . 1 . 5 .', da=0, registro=(31, 50))
    tp.basso(giro, '1 . . . 5, . . .', da=0, registro=(41, 53), vel=98, gate=0.5)
    bt.batteria({'cassa': 'x...x...', 'rullante': 'xxxxXXXX'}, da=0, battute=2)
    bt.batteria({'cassa': 'x...x...', 'rullante': '..x...x.', 'hh': 'xxxxxxxx'}, da=2, battute=16)
    b.ritornello(2, 18)
    return b.fine()
