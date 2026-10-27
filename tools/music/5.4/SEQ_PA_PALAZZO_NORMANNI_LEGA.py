"""Il potere: Palazzo dei Normanni, la Via della Lega, le sale dei 4 Campioni dell'ARS, la Sala
d'Ercole e l'Archivio dei Presidenti."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from notazione import Brano, Giro  # noqa: E402

SIMBOLO = 'SEQ_PA_PALAZZO_NORMANNI_LEGA'
BANCO = 'BANK_BGM_FIELD9'
VOLUME = 82
SCHEDA = {
    'titolo': 'Palazzo dei Normanni',
    'carattere': 'la solennità del potere sotto i mosaici d\'oro: processione lenta di ottoni e '
                 'organo, timpani e rullante da cerimonia; i Campioni dell\'ARS sono l\'ultimo livello '
                 'di «U Sistema», quindi ogni frase chiude col Re bemolle napoletano (R-AUD-21)',
    'tonalita': 'Do minore',
    'forma': 'introduzione di 2 battute (organo e timpani); ritornello A (8) + B (8)',
}

INTRO = Giro('Cm | G')
A_ = Giro('Cm | Ab | Fm | G | Cm | Ab | Db | G')
B_ = Giro('Eb | Bb | Cm | G | Ab | Eb | Db | G7')

MELODIA = (
    '| c5/2 eb5/4 g5 | ab5/2. c6/4 | f5/4. g5/8 ab5/4 c6 | b5/2 d6/4 g5 '
    '| g5/4. ab5/8 g5/4 eb5 | c5/4 eb5 ab5 c6 | db6/2 f5/4 ab5 | g5/2. r/4 '
    '| g5/4. f5/8 eb5/4 bb5 | d6/2 bb5/4 f5 | eb6/4. d6/8 c6/4 g5 | d6/2 b5/4 g5 '
    '| c6/4 ab5 eb5 ab5 | bb5/4. ab5/8 g5/4 eb5 | f5/4 ab5 db6 f6 | f6/2 d6/4 b5 |'
)


def partitura(A):
    b = Brano(A, bpm=92)
    tr = b.voce('tromba', 29, volume=108, pan=64)
    co = b.voce('corni', 32, volume=80, pan=36)
    og = b.voce('organo', 12, volume=64, pan=96)
    tb = b.voce('tromboni', 30, volume=96, pan=64)
    tp = b.voce('timpani', 28, volume=96, pan=64)
    bt = b.voce('rullante', 39, volume=66, pan=64)
    tr.suona(MELODIA, da=2, vel=98)
    giro = INTRO + A_ + B_
    co.accordi(A_ + B_, 'x---x---', da=2, registro=(52, 67), vel=62, voci=2)
    og.accordi(giro, 'x-------', da=0, registro=(55, 72), vel=58)
    tb.basso(giro, '1 - - - 5, - - -', da=0, registro=(31, 50))
    tp.basso(giro, '1 . . . 5, . . .', da=0, registro=(41, 53), vel=96, gate=0.5)
    bt.batteria({'rullante': 'x..x....x.......'}, da=2, battute=16)
    b.ritornello(2, 18)
    return b.fine()
