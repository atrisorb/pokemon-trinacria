"""Agrigento, la Valle dei Templi e i cantieri di Villaseta."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from notazione import Brano, Giro  # noqa: E402

SIMBOLO = 'SEQ_AG_AGRIGENTO_TEMPLI'
BANCO = 'BANK_BGM_DUNGEON2'
VOLUME = 62
SCHEDA = {
    'titolo': 'La Valle dei Templi',
    'carattere': 'colonne doriche al tramonto: solenne e antica, modo dorico di Mi (il La maggiore '
                 'dentro il Mi minore), arpa come una lira, corni gravi nella parte A, tromba che sale '
                 'nella parte B, archi tenuti e timpani lontani',
    'tonalita': 'Mi dorico',
    'forma': 'introduzione di 2 battute (arpa e timpani); ritornello A (8) + B (8)',
}

INTRO = Giro('Em | A/E')
A_ = Giro('Em | A | Em | D | C | D | Em | Bm')
B_ = Giro('C | G | D | A | C | D | Bm | B7')

CORNI = (
    '| e4/2 g4/4 b4/4 | c#5/2. a4/4 | b4/4 g4/4 e4/2 | f#4/2 a4/4 d5/4 '
    '| e5/2 g5/4 e5/4 | f#5/2 d5/2 | e5/4 b4/4 g4/4 b4/4 | f#4/1 |'
)
TROMBA = (
    '| g5/2 c6/4 e6/4 | d6/2. b5/4 | a5/4 d6/4 f#6/2 | e6/2 c#6/2 '
    '| e6/4 c6/4 g5/4 c6/4 | a5/2 f#5/4 a5/4 | b5/4 d6/4 f#6/4 d6/4 | d#6/2 a5/2 |'
)


def partitura(A):
    b = Brano(A, bpm=76)
    co = b.voce('corni', 32, volume=110, pan=56)
    tr = b.voce('tromba', 29, volume=104, pan=72)
    ap = b.voce('arpa', 26, volume=90, pan=36)
    ar = b.voce('archi', 23, volume=76, pan=92)
    cb = b.voce('contrabbasso', 25, volume=94, pan=64)
    tp = b.voce('timpani', 28, volume=88, pan=64)
    co.suona(CORNI, da=2, vel=94)
    tr.suona(TROMBA, da=10, vel=94)
    giro = INTRO + A_ + B_
    ap.arpeggi(giro, '1 5 8 10 12 10 8 5', da=0, registro=(52, 84), vel=74)
    ar.accordi(A_ + B_, 'x-------', da=2, registro=(52, 70), vel=60)
    cb.basso(giro, '1 - - - - - - -', da=0)
    tp.basso(giro, '1 . . . . . 1 .', da=0, registro=(40, 55), vel=90, gate=0.5)
    b.ritornello(2, 18)
    return b.fine()
