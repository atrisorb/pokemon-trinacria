"""Le faggete e i pascoli dei Nebrodi: San Fratello, Mistretta e il Bosco dei Nebrodi."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from notazione import Brano, Giro  # noqa: E402

SIMBOLO = 'SEQ_ME_NEBRODI_PASCOLI'
BANCO = 'BANK_BGM_FIELD4'
VOLUME = 92
SCHEDA = {
    'titolo': 'I pascoli dei Nebrodi',
    'carattere': 'boschi di faggi, cavalli sanfratellani e mandrie al pascolo: ländler di montagna '
                 'in 3/4, richiamo dei corni nell\'introduzione, flauto nella parte A, corni nella '
                 'parte B, archi in levare e i campanacci (legnetto e triangolo)',
    'tonalita': 'Fa maggiore (seconda passata in Do maggiore)',
    'forma': 'introduzione di 2 battute (richiamo dei corni); ritornello A (8) + B (8) in Fa maggiore, poi le stesse 16 battute in Do maggiore, in 3/4',
}

INTRO = Giro('F | C')
A_ = Giro('F | F | C | C | Bb | F | C | F')
B_ = Giro('Dm | Am | Bb | F | Gm | C | Bb C | C7')

RICHIAMO = '| c5/4 f5/4 a5/4 | c6/2. |'
FLAUTO = (
    '| a5/4 c6/4 f6/4 | f6/4. e6/8 c6/4 | g5/2 c6/4 | e6/2. '
    '| d6/4 bb5/4 f5/4 | a5/4 c6/4 f6/4 | e6/4 g6/4 e6/4 | f6/2. |'
)
CORNI = (
    '| d5/4 f5/4 a5/4 | c5/2 e5/4 | f5/4 d5/4 bb4/4 | c5/2. '
    '| bb4/4 d5/4 g5/4 | e5/2 g5/4 | f5/4 d5/8 e5/8 g5/4 | bb5/2. |'
)


def partitura(A):
    b = Brano(A, bpm=126, metro=(3, 4))
    fl = b.voce('flauto', 35, volume=108, pan=64)
    co = b.voce('corni', 32, volume=106, pan=56)
    ar = b.voce('archi', 23, volume=76, pan=88)
    cb = b.voce('contrabbasso', 25, volume=94, pan=64)
    pc = b.voce('campanacci', 39, volume=64, pan=36)
    co.suona(RICHIAMO, da=0, vel=96).suona(CORNI, da=10, vel=96)
    fl.suona(FLAUTO, da=2, vel=96)
    ar.accordi(A_ + B_, '..x.x.', da=2, registro=(55, 70), vel=62, gate=0.7)
    cb.basso(INTRO + A_ + B_, '1 . . . . .', da=0)
    pc.batteria({'legnetto': 'x...x.', 'triangolo': '..x...'}, da=2, battute=16)
    b.ripeti(2, 16, 18, trasponi=-5)
    b.ritornello(2, 34)
    return b.fine()
