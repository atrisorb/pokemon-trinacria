"""Il lungomare: Ognina, Plaia, Aci Castello, Aci Trezza e i Faraglioni (S-CT-04)."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from notazione import Brano, Giro  # noqa: E402

SIMBOLO = 'SEQ_CT_LUNGOMARE'
BANCO = 'BANK_BGM_FIELD6'
VOLUME = 78
SCHEDA = {
    'titolo': 'Il lungomare',
    'carattere': 'brezza di mare dalla scogliera lavica di Ognina ai Faraglioni dei Ciclopi: barcarola '
                 'in 6/8 che ondeggia, chitarra arpeggiata, flauto disteso, triangolo come luccichio '
                 'dell\'acqua',
    'tonalita': 'La maggiore',
    'forma': 'introduzione di 2 battute (chitarra); ritornello A (8) + B (8) in La maggiore, poi le stesse 16 battute in Re maggiore, in 6/8',
}

INTRO = Giro('A | E')
A_ = Giro('A | F#m | D | E | A | C#m | D E | A')
B_ = Giro('D | A/C# | Bm | E | F#m | C#m | D | E7')

MELODIA = (
    '| c#6/4. e5/8 a5 b5 | c#6/4 a5/8 f#5/4. | a5/4 f#5/8 d5/4 e5/8 | e5/4. g#5/4 b5/8 '
    '| c#6/4. e6/4 c#6/8 | e6/4 c#6/8 g#5/4. | f#5/8 a5 d6 b5/4 g#5/8 | a5/4. r/4. '
    '| f#5/4 a5/8 d6/4 a5/8 | e5/4 a5/8 c#6/4. | d6/4 b5/8 f#5/4 d5/8 | e5/4. g#5/4. '
    '| a5/4 c#6/8 f#6/4 c#6/8 | e6/4. g#5/4 c#6/8 | a5/8 f#5 d5 f#5/4 a5/8 | g#5/4. d5/4 e5/8 |'
)


def partitura(A):
    b = Brano(A, bpm=114, metro=(6, 8))
    fl = b.voce('flauto', 35, volume=110, pan=64)
    gt = b.voce('chitarra', 7, volume=96, pan=36)
    ar = b.voce('archi', 24, volume=56, pan=96)
    bs = b.voce('contrabbasso', 25, volume=100, pan=64)
    pc = b.voce('triangolo', 39, volume=64, pan=96)
    fl.suona(MELODIA, da=2, vel=96)
    giro = INTRO + A_ + B_
    gt.arpeggi(giro, '1 5 8 10 8 5', da=0, registro=(45, 76), vel=78)
    ar.accordi(A_ + B_, 'x-----', da=2, registro=(56, 71), vel=50)
    bs.basso(A_ + B_, '1 - - 5 - -', da=2)
    pc.batteria([{'triangolo': 'x.....'}, {'triangolo': '...o..'}], da=2, battute=16)
    b.ripeti(2, 16, 18, trasponi=-7)
    b.eco(fl, 'flauto eco', ritardo=24, volume=40)
    b.ritornello(2, 34)
    return b.fine()
