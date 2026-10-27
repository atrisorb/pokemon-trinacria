"""La nebbia medievale di Erice e del Castello di Venere."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from notazione import Brano, Giro  # noqa: E402

SIMBOLO = 'SEQ_TP_ERICE_NEBBIA'
BANCO = 'BANK_BGM_DUNGEON8'
VOLUME = 87
SCHEDA = {
    'titolo': 'Erice nella nebbia',
    'carattere': 'il borgo medievale sulla vetta, avvolto dalle nuvole: danza antica in 3/4 nel modo '
                 'dorico di Re (il Si naturale), flauto dolce con un\'eco che si perde nella nebbia, '
                 'arpa, bordone d\'organo di Re e La sempre tenuto e un tamburo leggero',
    'tonalita': 'Re dorico (seconda passata in La dorico)',
    'forma': 'introduzione di 2 battute (arpa e bordone); ritornello A (8) + B (8) in Re dorico, poi le stesse 16 battute in La dorico, in 3/4',
}

INTRO = Giro('Dm | C')
A_ = Giro('Dm | C | Dm | Am | F | C | G | Dm')
B_ = Giro('F | C | Dm | Am | Bb | F | G | A')

MELODIA = (
    '| d5/4 f5/4 a5/4 | g5/2 e5/4 | f5/4 a5/8 g5/8 f5/4 | e5/2. '
    '| a5/4 c6/4 a5/4 | g5/4 e5/4 c5/4 | b4/4 d5/4 g5/4 | a4/2. '
    '| c6/2 a5/4 | g5/2 e5/4 | f5/4 d5/4 a5/4 | c6/2. '
    '| d6/4 bb5/4 f5/4 | a5/2 c6/4 | b5/4 g5/4 d5/4 | c#5/2. |'
)


def partitura(A):
    b = Brano(A, bpm=100, metro=(3, 4))
    fd = b.voce('flauto dolce', 38, volume=108, pan=64)
    ap = b.voce('arpa', 26, volume=86, pan=40)
    og = b.voce('bordone', 12, volume=58, pan=64, pedale=True)
    tm = b.voce('tamburo', 39, volume=66, pan=88)
    fd.suona(MELODIA, da=2, vel=94)
    ap.arpeggi(INTRO + A_ + B_, '1 5 8 10 8 5', da=0, registro=(50, 76), vel=72)
    for n in range(18):                           # bordone di Re e La, battuta per battuta
        og.suona('d3+a3/2._', da=n, vel=62)
    tm.batteria({'tom_m': 'x...o.'}, da=2, battute=16)
    b.ripeti(2, 16, 18, trasponi=-5)
    b.eco(fd, 'flauto dolce eco', ritardo=24, volume=34)
    b.ritornello(2, 34)
    return b.fine()
