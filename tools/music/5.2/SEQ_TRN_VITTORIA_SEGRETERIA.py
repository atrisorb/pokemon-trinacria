"""Vittoria sui Segretari, sui Campioni dell'ARS e su Mistretta."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from notazione import Brano, Giro  # noqa: E402

SIMBOLO = 'SEQ_TRN_VITTORIA_SEGRETERIA'
BANCO = 'BANK_BASIC'
VOLUME = 102
SCHEDA = {
    'titolo': 'Vittoria su una Segreteria',
    'carattere': 'la vittoria che apre un Dossier: due battute di fanfara, poi un inno largo in Re '
                 'maggiore per ottoni e flauto con timpani; la parte B sale fino al La acuto',
    'tonalita': 'Re maggiore',
    'forma': 'introduzione di 2 battute; ritornello A (8) + B (8)',
}

INTRO = Giro('D | A7')
A_ = Giro('D | Bm | G | A | D | Bm | Em7 A7 | D')
B_ = Giro('G | A | F#m | Bm | G | A | G A | D')

FANFARA = '| d5/8 f#5 a5 d6 f#6/4 d6 | a6/2 g6/4 e6 |'
MELODIA = (
    '| f#5/4. a5/8 d6/4 a5 | b5/4. d6/8 f#6/4 d6 | g5/4 b5/8 d6 g6/4 d6 | e6/2 c#6/4 a5 '
    '| d6/4. f#6/8 a6/4 f#6 | f#6/4 d6/8 b5 f#5/4 b5 | g5/4 b5 c#6 e6 | d6/2. r/4 '
    '| d6/4. b5/8 g5/4 b5 | c#6/4. e6/8 a6/4 e6 | f#6/4. c#6/8 a5/4 c#6 | d6/2 b5/4 f#5 '
    '| g5/4 b5 d6 g6 | a6/4 e6 c#6 a5 | b5/4 d6 c#6 e6 | d6/2. r/4 |'
)


def partitura(A):
    b = Brano(A, bpm=160)
    tr = b.voce('tromba', 29, volume=118, pan=64)
    ar = b.voce('archi', 23, volume=90, pan=20)
    co = b.voce('corni', 32, volume=84, pan=100)
    bs = b.voce('tromboni', 30, volume=110, pan=80)
    tp = b.voce('timpani', 28, volume=100, pan=64)
    bt = b.voce('batteria', 39, volume=92, pan=40)
    tr.suona(FANFARA, da=0, vel=108).suona(MELODIA, da=2, vel=104)
    fl = b.voce('flauto', 35, volume=66, pan=40)
    fl.suona(MELODIA, da=2, vel=92, trasponi=12)
    giro = INTRO + A_ + B_
    ar.accordi(giro, 'x.xx.xx.', da=0, registro=(57, 72), vel=70, gate=0.6)
    co.accordi(A_ + B_, 'x---x---', da=2, registro=(50, 65), vel=64, voci=2)
    bs.basso(giro, '1 . 5 . 1 . 5 .', da=0, registro=(33, 50))
    tp.basso(giro, '1 . . . 5, . . .', da=0, registro=(43, 55), vel=100, gate=0.5)
    bt.batteria({'cassa': 'x...x...', 'rullante': '..x...x.', 'hh': 'xxxxxxxx'}, da=0, battute=18)
    b.ritornello(2, 18)
    return b.fine()
