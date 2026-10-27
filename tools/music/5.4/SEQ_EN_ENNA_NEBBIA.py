"""La nebbia d'altura dell'ombelico di Sicilia: Enna Alta e Bassa, la Rocca di Cerere, Pergusa,
Nicosia, Sperlinga, Leonforte, Agira, Centuripe e Aidone."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from notazione import Brano, Giro  # noqa: E402

SIMBOLO = 'SEQ_EN_ENNA_NEBBIA'
BANCO = 'BANK_BGM_DUNGEON6'
VOLUME = 87
SCHEDA = {
    'titolo': 'Enna nella nebbia',
    'carattere': 'la rocca più alta dell\'isola dentro la nebbia, la terra di Cerere e Proserpina: '
                 'modo dorico di Re (il Sol maggiore dentro il Re minore), un flauto antico con la '
                 'sua eco lontana, arpa arpeggiata, organo dolce tenuto sotto e una celesta che '
                 'brilla a tratti come il sole che non passa',
    'tonalita': 'Re dorico',
    'forma': 'introduzione di 2 battute (organo e arpa); ritornello A (8) + B (8)',
}

INTRO = Giro('Dm | A')
A_ = Giro('Dm | C | Dm | G | Dm | C | Bb | A')
B_ = Giro('F | C | G | Dm | Bb | F | G | A')

MELODIA = (
    '| a5/2 f5/4 d5 | e5/2 g5/4 c6 | d6/2. a5/4 | b5/2 d6/4 g5 '
    '| f5/4. e5/8 d5/4 a5 | g5/2 e5/4 c5 | d5/2 f5/4 bb5 | a5/2. r/4 '
    '| c6/2 a5/4 f5 | g5/2 e5/4 c6 | b5/2 d6/4 b5 | a5/2. f5/4 '
    '| f5/4 bb5 d6 f6 | f6/4. e6/8 c6/4 a5 | b5/2 g5/4 d6 | c#6/2. r/4 |'
)


def partitura(A):
    b = Brano(A, bpm=72)
    fl = b.voce('flauto', 35, volume=104, pan=58)
    ar = b.voce('arpa', 26, volume=76, pan=92)
    og = b.voce('organo', 12, volume=60, pan=40)
    ce = b.voce('celesta', 27, volume=50, pan=100)
    cb = b.voce('contrabbasso', 25, volume=86, pan=64)
    fl.suona(MELODIA, da=2, vel=92)
    b.eco(fl, 'flauto eco', ritardo=48, volume=38)
    giro = INTRO + A_ + B_
    ar.arpeggi(giro, '1 5 8 10 12 10 8 5', da=0, registro=(50, 79), vel=64)
    og.accordi(giro, 'x-------', da=0, registro=(55, 69), vel=56)
    ce.arpeggi(B_, '. . . . 12 . 15 .', da=10, registro=(62, 86), vel=54)
    cb.basso(giro, '1 - - - 5, - - -', da=0, registro=(26, 45), gate=0.95)
    b.ritornello(2, 18)
    return b.fine()
