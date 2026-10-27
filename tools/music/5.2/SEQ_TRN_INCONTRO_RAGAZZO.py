"""Incontro: ragazzi, studenti, escursionisti (e le classi senza riga: valore di partenza del motore)."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from notazione import Brano, Giro  # noqa: E402

SIMBOLO = 'SEQ_TRN_INCONTRO_RAGAZZO'
BANCO = 'BANK_BASIC'
VOLUME = 102
SCHEDA = {
    'titolo': 'Incontro — ragazzi',
    'carattere': 'il ragazzo che ti sfida per strada: arpeggio di Sol che scatta, tromba sfacciata, '
                 'ritmo da marcetta svelta',
    'tonalita': 'Sol maggiore',
    'forma': 'introduzione di 1 battuta; ritornello di 8 battute',
}

INTRO = Giro('G')
GIRO = Giro('G | C | G | D | G | C | Am D | G')

MELODIA = (
    '| d5/8 g5 b5 d6 g6/4 r | g5/8 g5 b5 d6 b5/4 g5 | e5/8 g5 c6 e6 c6/4 g5 | b5/4 d6/8 b5 g5/4 d5 '
    '| a5/8 f#5 d5 f#5 a5/4 d6 | g5/8 a5 b5 d6 g6/4 d6 | e6/4 c6/8 g5 e5/4 c6 | a5/4 c6 a5 f#5 '
    '| g5/2. r/4 |'
)


def partitura(A):
    b = Brano(A, bpm=160)
    tr = b.voce('tromba', 29, volume=112, pan=60)
    ch = b.voce('accordi', 3, volume=86, pan=100)
    bs = b.voce('basso', 22, volume=110, pan=64)
    bt = b.voce('batteria', 39, volume=96, pan=40)
    tr.suona(MELODIA, da=0, vel=102)
    b.eco(tr, 'tromba eco', ritardo=12, volume=44)
    giro = INTRO + GIRO
    ch.accordi(giro, '.x.x.x.x', da=0, registro=(55, 71), vel=70, gate=0.5)
    bs.basso(giro, '1 . 5 . 8 . 5 .', da=0, registro=(31, 50))
    bt.batteria({'cassa': 'x...x...', 'rullante': '..x...x.', 'hh': 'xoxoxoxo'}, da=0, battute=9)
    b.ritornello(1, 9)
    return b.fine()
