"""Incontro: montanari, pescatori, karateka, zaùddi, marinai."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from notazione import Brano, Giro  # noqa: E402

SIMBOLO = 'SEQ_TRN_INCONTRO_DURO'
BANCO = 'BANK_BASIC'
VOLUME = 86
SCHEDA = {
    'titolo': 'Incontro — tipi duri',
    'carattere': 'gente di fatica e di mare: riff grave di tromboni che scende La–Sol–Fa–Mi, una tromba '
                 'che grida note lunghe sopra, cassa pesante',
    'tonalita': 'La minore',
    'forma': 'introduzione di 1 battuta (due colpi); ritornello di 8 battute',
}

GIRO = Giro('Am | Am | G | G | F | F | E | E')

RIFF = (
    '| a4/8 a4 c5 a4 e5 a4 c5 a4 | a4/8 a4 c5 a4 e5 d5 c5/4 | g4/8 g4 b4 g4 d5 g4 b4 g4 '
    '| g4/8 g4 b4 g4 d5 c5 b4/4 | f4/8 f4 a4 f4 c5 f4 a4 f4 | f4/8 f4 a4 f4 c5 b4 a4/4 '
    '| e4/8 e4 g#4 e4 b4 e4 g#4 e4 | e4/8 g#4 b4 d5 e5/4 r |'
)
GRIDO = '| e5/1 | e5/2 c5 | d5/1 | b4/2 d5 | c5/1 | a4/2 c5 | b4/1 | g#4/1 |'


def partitura(A):
    b = Brano(A, bpm=140)
    tb = b.voce('tromboni', 30, volume=112, pan=40)
    tr = b.voce('tromba', 29, volume=96, pan=90)
    bs = b.voce('basso', 22, volume=114, pan=64)
    bt = b.voce('batteria', 39, volume=100, pan=64)
    tb.suona('| a3+e4/4> r a3+e4> r |', da=0, vel=110)
    tb.suona(RIFF, da=1, vel=100)
    tr.suona(GRIDO, da=1, vel=92, gate=0.95)
    bs.basso(GIRO, '1 . 1 . 1 . 5, .', da=1, registro=(33, 50), gate=0.6)
    bt.batteria({'cassa': 'X.......X.......'}, da=0, battute=1)
    bt.batteria({'cassa': 'x..x..x.x..x..x.', 'rullante': '....X.......X...', 'hh': 'x.x.x.x.x.x.x.x.'},
                da=1, battute=8)
    b.ritornello(1, 9)
    return b.fine()
