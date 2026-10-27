"""La Fiera del Mediterraneo riaperta: viali e padiglioni della Frontiera Lotta (P-09)."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from notazione import Brano, Giro  # noqa: E402

SIMBOLO = 'SEQ_PA_FIERA_MEDITERRANEO'
BANCO = 'BANK_BGM_DUNGEON4'
VOLUME = 97
SCHEDA = {
    'titolo': 'La Fiera del Mediterraneo',
    'carattere': 'l\'ex fiera abbandonata riaperta come cittadella dello sport, senza raccomandazioni: '
                 'brano sportivo e luminoso, tromba e glockenspiel sopra gli archi staccati, basso '
                 'elettrico e batteria piena, come l\'ingresso di uno stadio',
    'tonalita': 'Si bemolle maggiore',
    'forma': 'introduzione di 2 battute (archi e batteria); ritornello A (8) + B (8)',
}

INTRO = Giro('Bb | F7')
A_ = Giro('Bb | F | Gm | Eb | Bb | F | Eb F | Bb')
B_ = Giro('Eb | F | Dm | Gm | Cm | F | Eb | F7')

MELODIA = (
    '| f5/4 bb5/8 c6 d6/4 bb5 | c6/2 a5/4 f5 | g5/4. a5/8 bb5/4 d6 | eb6/2 bb5/4 g5 '
    '| f5/8 g5 bb5 c6 d6/4 f6 | f6/4. eb6/8 c6/4 a5 | g5/4 bb5 a5 c6 | bb5/2. r/4 '
    '| bb5/4. g5/8 eb5/4 g5 | a5/4. f5/8 c5/4 f5 | a5/4 d6 f6 d6 | d6/2 bb5/4 g5 '
    '| eb6/4. d6/8 c6/4 g5 | a5/4 c6 f6 c6 | g6/4. f6/8 eb6/4 bb5 | a5/2 c6/4 eb6 |'
)


def partitura(A):
    b = Brano(A, bpm=132)
    tr = b.voce('tromba', 29, volume=112, pan=64)
    ar = b.voce('archi', 23, volume=78, pan=30)
    gl = b.voce('glockenspiel', 10, volume=60, pan=100)
    bs = b.voce('basso', 22, volume=108, pan=64)
    bt = b.voce('batteria', 39, volume=90, pan=64)
    tr.suona(MELODIA, da=2, vel=100)
    gl.suona(MELODIA, da=2, vel=80, trasponi=12)
    giro = INTRO + A_ + B_
    ar.accordi(giro, 'x.xx.xx.', da=0, registro=(57, 72), vel=68, gate=0.5)
    bs.basso(giro, '1 1 8 1 1 1 8 1', da=0, registro=(34, 50), gate=0.6)
    bt.batteria({'cassa': 'x.x.x.x.', 'rullante': 'xxxxxxxx'}, da=0, battute=1)
    bt.batteria({'cassa': 'x.x.x.x.', 'rullante': 'xxxxXXXX'}, da=1, battute=1)
    bt.batteria({'cassa': 'x...x...x...x...', 'rullante': '....x.......x...', 'hh': 'x.x.x.x.x.x.x.x.'},
                da=2, battute=16)
    b.ritornello(2, 18)
    return b.fine()
