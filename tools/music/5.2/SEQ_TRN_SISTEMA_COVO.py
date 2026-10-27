"""«U Sistema»: covi e uffici del cartello (si suona negli eventi con PlayBGM; nessuna mappa lo ha fisso)."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from notazione import Brano, Giro  # noqa: E402

SIMBOLO = 'SEQ_TRN_SISTEMA_COVO'
BANCO = 'BANK_BASIC'
VOLUME = 89
SCHEDA = {
    'titolo': '«U Sistema» — covo',
    'carattere': 'retrobottega, uffici con le tapparelle abbassate, registri contabili: passo felpato '
                 'e sospetto, pizzicato staccato, fagotto grave, charleston che ticchetta; nella parte B '
                 'il Sol bemolle (napoletano di Fa minore) e i colpi d\'ottone',
    'tonalita': 'Fa minore',
    'forma': 'introduzione di 2 battute (pizzicato e basso); ritornello A (8) + B (8)',
}

INTRO = Giro('Fm | C7')
A_ = Giro('Fm | Fm | Db | C | Fm | Fm | Bbm | C7')
B_ = Giro('Db | Eb | Cm | Fm | Bbm | Gb | C | C7')

MELODIA = (
    '| f3/4. ab3/8 c4/4 f4 | f4/8 e4 f4 g4 ab4/2 | db4/4. f4/8 ab4/4 f4 | e4/2 g4/4 c4 '
    '| c4/8 f4 ab4 c5 ab4/4 f4 | ab4/8 g4 f4 g4 c4/2 | bb3/4 db4 f4 bb4 | bb4/2 g4/4 e4 '
    '| ab4/4. f4/8 db4/4 f4 | g4/4. eb4/8 bb3/4 eb4 | c4/4 eb4 g4 c5 | ab4/2. f4/4 '
    '| db5/4 bb4 f4 db4 | db4/4 gb4 bb4 db5 | c5/4 g4 e4 c4 | bb3/2 e4/4 g4 |'
)


def partitura(A):
    b = Brano(A, bpm=116)
    fg = b.voce('fagotto', 36, volume=116, pan=64)
    pz = b.voce('pizzicato', 17, volume=96, pan=100)
    tb = b.voce('ottoni', 30, volume=88, pan=30)
    bs = b.voce('basso', 21, volume=108, pan=64)
    bt = b.voce('batteria', 39, volume=80, pan=64)
    fg.suona(MELODIA, da=2, vel=100)
    b.eco(fg, 'clarinetto ottava', ritardo=0, volume=60, pan=96, trasponi=12, programma=34)
    giro = INTRO + A_ + B_
    pz.arpeggi(giro, '1 . 1 5 . 1 8 .', da=0, registro=(48, 72), vel=84, gate=0.4)
    tb.accordi(B_, '......X.', da=10, registro=(53, 67), vel=84, gate=0.5)
    bs.basso(giro, '1 . . 1 . . 1 .', da=0, registro=(29, 46))
    bt.batteria({'hh': 'x.o.x.o.x.o.x.o.', 'cassa': 'x.....x...x.....', 'bordo': '....x.......x...'},
                da=2, battute=16)
    b.ritornello(2, 18)
    return b.fine()
