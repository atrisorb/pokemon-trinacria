"""Centro Pokémon: tutti i Centri di Trinacria (40 mappe nel registro 2.5)."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from notazione import Brano, Giro  # noqa: E402

SIMBOLO = 'SEQ_TRN_CENTRO_POKEMON'
BANCO = 'BANK_BGM_FIELD1'
VOLUME = 75
SCHEDA = {
    'titolo': 'Centro Pokémon',
    'carattere': 'riposo e cura, uguale in tutta l\'isola: melodia di campanelli, mandolino arpeggiato '
                 'come tocco siciliano, archi morbidi; il brano che si sente più spesso, quindi '
                 'semplice e cantabile',
    'tonalita': 'Re maggiore',
    'forma': 'ritornello A (8) + B (8) dalla prima battuta',
}

A_ = Giro('D | G/D | D | A7 | Bm7 | G | Em7 A7 | D')
B_ = Giro('G | A | F#m | Bm | Em | A | G A7 | D')

MELODIA = (
    '| f#5/4 a5 d6 a5 | b5/4. a5/8 g5/4 d5 | f#5/4 e5/8 f#5 a5/2 | g5/2 e5/4 c#5 '
    '| d5/4 f#5 b5 a5 | b5/4. a5/8 g5/4 d5 | e5/4 g5 e5 c#5 | d5/2. r/4 '
    '| d6/4. b5/8 g5/4 d5 | c#6/4. a5/8 e5/4 a5 | a5/4. f#5/8 c#5/4 f#5 | d5/2 b4/4 d5 '
    '| e5/4 g5 b5 g5 | a5/2 c#6/4 e6 | d6/4 b5 c#6 a5 | d6/2. r/4 |'
)


def partitura(A):
    b = Brano(A, bpm=112)
    cp = b.voce('campanelli', 5, volume=108, pan=64)
    md = b.voce('mandolino', 42, volume=84, pan=36)
    ar = b.voce('archi', 23, volume=60, pan=96)
    bs = b.voce('basso', 19, volume=106, pan=64)
    bt = b.voce('batteria', 39, volume=72, pan=64)
    cp.suona(MELODIA, da=0, vel=96)
    giro = A_ + B_
    md.arpeggi(giro, '1 5 8 5 10 5 8 5', da=0, registro=(55, 79), vel=72)
    ar.accordi(giro, 'x---x---', da=0, registro=(57, 72), vel=50)
    bs.basso(giro, '1 - - 5 8 - 5 -', da=0)
    bt.batteria({'bordo': '..x...x.', 'hh': 'o.o.o.o.', 'cassa': 'x...x...'}, da=0, battute=16)
    b.eco(cp, 'campanelli eco', ritardo=12, volume=44)
    b.ritornello(0, 16)
    return b.fine()
