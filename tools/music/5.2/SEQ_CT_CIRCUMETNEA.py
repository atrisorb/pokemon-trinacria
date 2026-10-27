"""Il trenino della Circumetnea: la littorina da Randazzo a Bronte (S-CT-08, E-CT-03)."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from notazione import Brano, Giro  # noqa: E402

SIMBOLO = 'SEQ_CT_CIRCUMETNEA'
BANCO = 'BANK_BGM_DUNGEON8'
VOLUME = 77
SCHEDA = {
    'titolo': 'La Circumetnea',
    'carattere': 'la littorina a scartamento ridotto che si ferma ovunque: charleston e rullante come '
                 'il ritmo delle rotaie, basso «um-pa», clarinetto allegro; si apre col fischio a due '
                 'note del treno',
    'tonalita': 'Sol maggiore',
    'forma': 'introduzione di 2 battute (fischio e rotaie); ritornello A (8) + B (8) in Sol maggiore, poi le stesse 16 battute in Do maggiore',
}

INTRO = Giro('G | D7')
A_ = Giro('G | G | C | G | Em | Am | D7 | G')
B_ = Giro('C | G | Am | D | Bm | Em | A7 | D7')

MELODIA = (
    '| d5/8 g5 b5 d6 b5/4 g5 | b5/8 a5 g5 a5 b5/2 | c6/8 b5 c6 e6 g5/4 e5 | d5/2. r/4 '
    '| e5/8 g5 b5 e6 b5/4 g5 | a5/8 c6 e6 c6 a5/4 e5 | f#5/8 a5 d6 c6 a5/4 f#5 | g5/2 d5/4 g4 '
    '| e6/4 d6/8 c6 g5/4 e5 | d6/2 b5/4 g5 | c6/4 b5/8 a5 e5/4 c5 | d5/4 f#5 a5 d6 '
    '| d6/4. c#6/8 b5/4 f#5 | e5/4 g5 b5 e6 | c#6/4 a5/8 g5 e5/4 c#5 | d5/4 f#5 a5 c6 |'
)


def partitura(A):
    b = Brano(A, bpm=150)
    cl = b.voce('clarinetto', 34, volume=110, pan=64)
    fi = b.voce('fischio', 37, volume=90, pan=90)
    ch = b.voce('accordi', 3, volume=84, pan=36)
    bs = b.voce('basso', 22, volume=108, pan=64)
    bt = b.voce('batteria', 39, volume=86, pan=64)
    fi.suona('| b5/4~ b5/8 g5/8~ g5/2 | r/1 |', da=0, vel=100)
    cl.suona(MELODIA, da=2, vel=96)
    giro = INTRO + A_ + B_
    ch.accordi(giro, '.x.x.x.x', da=0, registro=(55, 70), vel=68, gate=0.6)
    bs.basso(giro, '1 . 5 . 1 . 5 .', da=0)
    bt.batteria({'hh': 'xoxoxoxoxoxoxoxo', 'rullante': '....o.......o...', 'cassa': 'x.......x.......'},
                da=0, battute=18, dur_max=8)
    b.ripeti(2, 16, 18, trasponi=-7)
    b.ritornello(2, 34)
    return b.fine()
