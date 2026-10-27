"""Vittoria e il mercato ortofrutticolo all'alba."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from notazione import Brano, Giro  # noqa: E402

SIMBOLO = 'SEQ_RG_MERCATO_ALBA'
BANCO = 'BANK_BGM_FIELD9'
VOLUME = 64
SCHEDA = {
    'titolo': 'Il mercato all\'alba',
    'carattere': 'i padiglioni di Vittoria prima che sorga il sole: due battute di campanelle come '
                 'la prima luce, poi il via vai dei carichi, mandolino svelto, fisarmonica in levare, '
                 'tamburello e battimani; nella parte B il clarinetto canta la fatica di chi '
                 'lavora dalle quattro del mattino',
    'tonalita': 'Do maggiore (parte B in La minore)',
    'forma': 'introduzione di 2 battute (campanelle); ritornello A (8) + B (8)',
    'perche_volume': 'HeartGold suona lo slot a 59 con 11 tracce (lo stesso file di '
                     '`SEQ_GS_C_NIBI` e `SEQ_GS_C_YAMABUKI`); le 6 voci di questa partitura a 59 resterebbero sotto le musiche vicine '
                     '(costa iblea 75)',
}

INTRO = Giro('C | G')
A_ = Giro('C | G | Am | Em | F | C | Dm G | C')
B_ = Giro('Am | Em | F | C | Dm | Am | F G | G7')

MANDOLINO = (
    '| e5/8 g5 c6/4 g5/8 e5 c5/4 | d5/8 g5 b5/4 d6/2 | c6/8 b5 a5/4 e5/4 a5/4 | g5/2 e5/2 '
    '| f5/8 a5 c6/4 a5/8 f5 c5/4 | e5/8 g5 c6/4 e6/2 | f5/8 a5 d6/4 b5/8 g5 d5/4 | c5/2. r/4 |'
)
CLARINETTO = (
    '| a4/4 c5/4 e5/2 | g5/4. e5/8 b4/2 | a4/4 c5/4 f5/2 | e5/2. g5/4 '
    '| f5/4 a5/4 d6/2 | c6/4. a5/8 e5/2 | f5/4 a5/4 g5/4 b5/4 | d6/2 f5/2 |'
)


def partitura(A):
    b = Brano(A, bpm=126)
    md = b.voce('mandolino', 42, volume=100, pan=64)
    cl = b.voce('clarinetto', 34, volume=104, pan=56)
    gl = b.voce('campanelle', 10, volume=80, pan=80)
    fs = b.voce('fisarmonica', 13, volume=70, pan=40)
    bs = b.voce('basso', 19, volume=96, pan=64)
    bt = b.voce('batteria', 39, volume=72, pan=88)
    md.suona(MANDOLINO, da=2, vel=96)
    md.arpeggi(B_, '1 5 8 5 10 5 8 5', da=10, registro=(55, 79), vel=70)
    cl.suona(CLARINETTO, da=10, vel=96)
    gl.arpeggi(INTRO, '8 12 15 12 8 12 15 12', da=0, registro=(72, 96), vel=72)
    fs.accordi(A_ + B_, '.x.x.x.x', da=2, registro=(55, 70), vel=58, gate=0.6)
    bs.basso(A_ + B_, '1 . 5 . 1 . 5 .', da=2)
    bt.batteria({'tamburello': 'x.x.x.x.', 'battimani': '....x...', 'cassa': 'x...x...'}, da=2, battute=16)
    b.ritornello(2, 18)
    return b.fine()
