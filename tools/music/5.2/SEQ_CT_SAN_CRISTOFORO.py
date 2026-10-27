"""San Cristoforo e via Plebiscito: braci e vicoli (M-CT-03, l'officina e il pizzo biologico)."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from notazione import Brano, Giro  # noqa: E402

SIMBOLO = 'SEQ_CT_SAN_CRISTOFORO'
BANCO = 'BANK_BGM_FIELD5'
VOLUME = 64
SCHEDA = {
    'titolo': 'San Cristoforo',
    'carattere': 'quartiere popolare stretto, fumo delle braci di carne di cavallo, officine: passo lento '
                 'e pesante, cadenza «andalusa» La minore–Sol–Fa–Mi col Mi maggiore, clarinetto che '
                 'ricama, pizzicato e tamburi a mano',
    'tonalita': 'La minore (modo frigio di Mi nelle cadenze)',
    'forma': 'ritornello A (8) + B (8) dalla prima battuta',
    'perche_volume': 'HeartGold suona lo slot a 54 con 9 tracce; le 6 voci di questa partitura a 54 '
                     'resterebbero sotto le musiche vicine (via Etnea 72, Vermut 78)',
}

A_ = Giro('Am | G | F | E | Am | G | F | E7')
B_ = Giro('Dm | Am | Dm | E7 | F | G | F | E')

MELODIA = (
    '| e5/4. f5/8 e5/4 c5 | d5/4 b4/8 c5 d5/4 g4 | a4/8 c5 f5/4 a5/8 g5 f5/4 | g#5/4. f5/8 e5/2 '
    '| a5/4 g#5/8 a5 c6/4 b5/8 a5 | b5/4 a5/8 g5 d5/2 | c5/8 d5 c5 a4 f4/4 a4 | b4/2 g#4 '
    '| d5/4. f5/8 a5/4 f5 | e5/2 c5/4 a4 | f5/4. e5/8 d5/4 a4 | g#4/2 b4/4 d5 '
    '| c5/4. d5/8 c5/4 a4 | b4/4. c5/8 d5/4 g5 | a5/4 g5/8 f5 c5/4 a4 | g#4/2. r/4 |'
)


def partitura(A):
    b = Brano(A, bpm=92)
    cl = b.voce('clarinetto', 34, volume=112, pan=64)
    pz = b.voce('pizzicato', 42, volume=96, pan=32)
    ar = b.voce('archi', 23, volume=60, pan=96)
    bs = b.voce('contrabbasso', 25, volume=104, pan=64)
    tm = b.voce('tamburi', 39, volume=88, pan=64)
    cl.suona(MELODIA, da=0, vel=96)
    giro = A_ + B_
    pz.arpeggi(giro, '1 . 5 8 . 5 3 .', da=0, registro=(48, 72), vel=80)
    ar.accordi(giro, 'x-------', da=0, registro=(52, 67), vel=52)
    bs.basso(giro, '1 - - - 5 - - -', da=0, gate=0.95)
    tm.batteria({'tom_b': 'x..x....', 'tom_m': '....x.x.', 'tamburello': 'o.o.o.oo'}, da=0, battute=16)
    b.eco(cl, 'clarinetto eco', ritardo=24, volume=36)
    b.ritornello(0, 16)
    return b.fine()
