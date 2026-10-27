"""Vittoria sui capi dei padiglioni della Fiera del Mediterraneo."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from notazione import Brano, Giro  # noqa: E402

SIMBOLO = 'SEQ_TRN_VITTORIA_FIERA'
BANCO = 'BANK_BASIC'
VOLUME = 97
SCHEDA = {
    'titolo': 'Vittoria alla Fiera',
    'carattere': 'la coppa del torneo: due battute di fanfara, poi un tema largo in Si bemolle per '
                 'tromba e flauto all\'ottava, archi ribattuti, tromboni al basso, timpani',
    'tonalita': 'Si bemolle maggiore',
    'forma': 'introduzione di 2 battute; ritornello A (8)',
}

INTRO = Giro('Bb | F7')
A_ = Giro('Bb | Gm | Eb | F | Bb | Gm | Eb F | Bb')

FANFARA = '| f5/8 bb5 d6 f6 bb6/4 f6 | a6/2 c7/4 a6 |'
MELODIA = (
    '| d6/4. c6/8 bb5/4 f5 | g5/4 bb5 d6 g6 | g6/4. f6/8 eb6/4 bb5 | c6/2 a5/4 f5 '
    '| f5/4 bb5 d6 f6 | g6/4. f6/8 d6/4 bb5 | g5/4 bb5 a5 c6 | bb5/2. r/4 |'
)


def partitura(A):
    b = Brano(A, bpm=152)
    tr = b.voce('tromba', 29, volume=118, pan=64)
    fl = b.voce('flauto', 35, volume=64, pan=40)
    ar = b.voce('archi', 23, volume=88, pan=20)
    bs = b.voce('tromboni', 30, volume=108, pan=80)
    tp = b.voce('timpani', 28, volume=98, pan=64)
    bt = b.voce('batteria', 39, volume=90, pan=40)
    tr.suona(FANFARA, da=0, vel=108).suona(MELODIA, da=2, vel=104)
    fl.suona(MELODIA, da=2, vel=90, trasponi=12)
    giro = INTRO + A_
    ar.accordi(giro, 'x.xx.xx.', da=0, registro=(58, 72), vel=70, gate=0.6)
    bs.basso(giro, '1 . 5 . 1 . 5 .', da=0, registro=(34, 50))
    tp.basso(giro, '1 . . . 5, . . .', da=0, registro=(41, 53), vel=98, gate=0.5)
    bt.batteria({'cassa': 'x...x...', 'rullante': '..x...x.', 'hh': 'xxxxxxxx'}, da=0, battute=10)
    b.ritornello(2, 10)
    return b.fine()
