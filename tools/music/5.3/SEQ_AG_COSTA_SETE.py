"""Le terre della sete e la costa agrigentina: Licata, Palma di Montechiaro, Canicattì, Favara,
Porto Empedocle, Realmonte, l'Acquedotto costiero e Sciacca."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from notazione import Brano, Giro  # noqa: E402

SIMBOLO = 'SEQ_AG_COSTA_SETE'
BANCO = 'BANK_BGM_FIELD17'
VOLUME = 80
SCHEDA = {
    'titolo': 'Le terre della sete',
    'carattere': 'caldo secco, rubinetti a secco e il mare sotto la marna bianca: chitarra '
                 'arpeggiata, una voce d\'ancia che si muove sulla scala minore armonica (il Do diesis '
                 'sopra il Si bemolle, colore arabo della costa africana), tamburello asciutto; '
                 'nella parte B gli archi lenti portano un po\' d\'ombra',
    'tonalita': 'Re minore (minore armonica)',
    'forma': 'introduzione di 2 battute (chitarra e tamburello); ritornello A (8) + B (8)',
}

INTRO = Giro('Dm | A')
A_ = Giro('Dm | Dm | Gm | A | Bb | Gm | A7 | Dm')
B_ = Giro('F | C | Bb | A | Gm | Dm | Bb A | A7')

MELODIA = (
    '| d5/4 f5/4 a5/2 | a5/4. bb5/8 a5/4 f5/4 | g5/4 bb5/4 d6/4 bb5/4 | c#6/2 a5/2 '
    '| d6/4. c6/8 bb5/4 f5/4 | g5/4 d5/4 bb4/4 d5/4 | e5/4 g5/4 c#5/4 e5/4 | d5/2. r/4 '
    '| a5/4 c6/4 f6/2 | e6/4. d6/8 c6/2 | d6/4 bb5/4 f5/2 | e5/4 c#5/4 a4/2 '
    '| bb4/4 d5/4 g5/2 | f5/4. e5/8 d5/2 | f5/4 d5/4 e5/4 c#5/4 | a4/2 g5/2 |'
)


def partitura(A):
    b = Brano(A, bpm=104)
    ob = b.voce('canto', 33, volume=106, pan=64)
    ch = b.voce('chitarra', 7, volume=84, pan=40)
    ar = b.voce('archi', 24, volume=66, pan=88)
    cb = b.voce('contrabbasso', 25, volume=94, pan=64)
    pc = b.voce('tamburello', 39, volume=70, pan=96)
    ob.suona(MELODIA, da=2, vel=96)
    giro = INTRO + A_ + B_
    ch.arpeggi(giro, '1 5 8 5 10 5 8 5', da=0, registro=(50, 74), vel=74)
    ar.accordi(B_, 'x-------', da=10, registro=(55, 70), vel=58)
    cb.basso(giro, '1 - - 1 5 - - -', da=0)
    pc.batteria({'tamburello': 'x..x..x.', 'bordo': '....x...'}, da=0, battute=18)
    b.eco(ob, 'canto eco', ritardo=12, volume=36)
    b.ritornello(2, 18)
    return b.fine()
