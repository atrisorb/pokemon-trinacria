"""Lotta con Tramontana (Raikou), il secondo dei Tre Venti di Sicilia (P-07)."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from notazione import Brano, Giro  # noqa: E402

SIMBOLO = 'SEQ_TRN_LOTTA_TRAMONTANA'
BANCO = 'BANK_BGM_BATTLE6'
VOLUME = 98
SCHEDA = {
    'titolo': 'Tramontana',
    'carattere': 'la tempesta elettrica che scende dai monti: archi all\'unisono con un\'onda quadra '
                 '(PSG) un\'ottava sotto, come una scarica, basso sintetico a crome ribattute, rullante '
                 'serrato e timpani come tuoni; stesso inizio di frase dei Tre Venti, in Si minore',
    'tonalita': 'Si minore',
    'forma': 'introduzione di 2 battute; ritornello A (8) + B (8)',
}

INTRO = Giro('Bm | F#7')
A_ = Giro('Bm | G | A | F# | Bm | G | Em | F#')
B_ = Giro('D | A | Bm | F# | G | D | Em | F#7')

APERTURA = '| b4/8 c#5 d5 e5 f#5/4 b5 | c#6/4. a#5/8 f#5/4 e5 |'
MELODIA = (
    '| b5/4. f#5/8 d5/4 b4 | d5/8 g5 b5 d6 g6/4 d6 | e6/4. c#6/8 a5/4 e5 | f#5/4 a#5 c#6 f#6 '
    '| f#6/4. e6/8 d6/4 b5 | b5/4 d6 g6 d6 | e6/4. f#6/8 g6/4 b5 | a#5/2 c#6/4 f#6 '
    '| f#6/4. e6/8 d6/4 a5 | c#6/4. e6/8 a6/4 e6 | d6/4 b5 f#5 b5 | c#6/2 a#5/4 f#5 '
    '| g5/8 b5 d6 g6 b6/4 g6 | f#6/4. a6/8 f#6/4 d6 | e6/4 g6 b6 g6 | a#6/2 e6/4 c#6 |'
)


def partitura(A):
    b = Brano(A, bpm=184)
    ar = b.voce('archi', 23, volume=116, pan=64)
    bs = b.voce('basso', 21, volume=112, pan=64)
    co = b.voce('corni', 32, volume=80, pan=30)
    tp = b.voce('tuono', 28, volume=104, pan=64)
    bt = b.voce('batteria', 39, volume=100, pan=64)
    ar.suona(APERTURA, da=0, vel=104).suona(MELODIA, da=2, vel=102)
    b.eco(ar, 'scarica PSG', ritardo=0, volume=54, pan=96, trasponi=-12, programma=48)
    giro = INTRO + A_ + B_
    co.accordi(A_ + B_, 'x---x---', da=2, registro=(52, 66), vel=66, voci=2)
    bs.basso(giro, '1 1 1 1 1 1 8 1', da=0, registro=(30, 49), gate=0.5)
    tp.basso(giro, '1 . . . . . 1 .', da=0, registro=(40, 52), vel=108, gate=0.6)
    bt.batteria({'rullante': 'x.x.x.x.xxxxxxxx', 'cassa': 'x.......x.......'}, da=0, battute=2)
    bt.batteria({'cassa': 'x..x..x.x..x..x.', 'rullante': '....x.......x.xx', 'hh': 'xxxxxxxxxxxxxxxx'},
                da=2, battute=16)
    b.ritornello(2, 18)
    return b.fine()
