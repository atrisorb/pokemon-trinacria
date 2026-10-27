"""La brezza dello Stretto: Messina, Torre Faro, Ganzirri, Giostra e i Gorghi di Cariddi."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from notazione import Brano, Giro  # noqa: E402

SIMBOLO = 'SEQ_ME_STRETTO_MESSINA'
BANCO = 'BANK_BGM_FIELD1'
VOLUME = 78
SCHEDA = {
    'titolo': 'Lo Stretto di Messina',
    'carattere': 'la Calabria a tre chilometri, le correnti che si incrociano e i laghi di Ganzirri: '
                 'flauto ampio sopra l\'arpa nella parte A; nella parte B gli archi girano a sedicesime '
                 'come i gorghi di Cariddi',
    'tonalita': 'Si minore (parte B verso Re maggiore)',
    'forma': 'introduzione di 2 battute (arpa); ritornello A (8) + B (8)',
}

INTRO = Giro('Bm | F#7')
A_ = Giro('Bm | G | D | A | Bm | G | Em F#7 | Bm')
B_ = Giro('G | D | A | Bm | G | D | Em | F#7')

MELODIA = (
    '| f#5/4 b5/4 d6/4. c#6/8 | b5/4 g5/4 d5/2 | f#5/4 a5/4 d6/4 f#6/4 | e6/2 c#6/2 '
    '| d6/4. c#6/8 b5/4 f#5/4 | g5/4 b5/4 d6/2 | e6/4 b5/4 a#5/4 c#6/4 | b5/2. r/4 '
    '| d6/4 g6/4 b5/2 | a5/4. f#5/8 d5/2 | c#5/4 e5/4 a5/4 c#6/4 | d6/2 b5/2 '
    '| b5/4 d6/4 g6/4 d6/4 | f#6/2 a5/2 | g5/4 b5/4 e6/4 g6/4 | f#6/2 e6/2 |'
)


def partitura(A):
    b = Brano(A, bpm=112)
    fl = b.voce('flauto', 35, volume=110, pan=64)
    ap = b.voce('arpa', 26, volume=88, pan=40)
    ar = b.voce('gorghi', 23, volume=74, pan=88)
    bs = b.voce('basso', 19, volume=96, pan=64)
    bt = b.voce('batteria', 39, volume=64, pan=64)
    fl.suona(MELODIA, da=2, vel=96)
    ap.arpeggi(INTRO + A_ + B_, '1 5 8 10 12 10 8 5', da=0, registro=(47, 79), vel=74)
    ar.arpeggi(B_, '1 3 5 8 5 3 1 3 5 8 10 8 5 3 1 5', da=10, registro=(59, 83), vel=62, gate=0.7)
    bs.basso(INTRO + A_ + B_, '1 . . 1 5 . . .', da=0)
    bt.batteria({'hh': 'x.x.x.x.', 'bordo': '....x...'}, da=2, battute=16)
    b.eco(fl, 'flauto eco', ritardo=12, volume=38)
    b.ritornello(2, 18)
    return b.fine()
