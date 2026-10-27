"""Palermo liberty e monumentale: Politeama, Teatro Massimo e via Maqueda, Mondello, Monreale."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from notazione import Brano, Giro  # noqa: E402

SIMBOLO = 'SEQ_PA_PALERMO_LIBERTA'
BANCO = 'BANK_BGM_FIELD6'
VOLUME = 83
SCHEDA = {
    'titolo': 'Palermo liberty',
    'carattere': 'i salotti di via Libertà e il fasto del Massimo: un valzer da sala dei tempi dei '
                 'Florio, violini che cantano sopra l\'«um-pa-pa» del pianoforte, arpa e contrabbasso; '
                 'la parte B passa in Re minore, un\'ombra dietro le facciate eleganti',
    'tonalita': 'Fa maggiore (parte B in Re minore)',
    'forma': 'introduzione di 2 battute (pianoforte); ritornello A (16) + B (16), in 3/4',
}

INTRO = Giro('F | C7')
A_ = Giro('F | F | C7 | C7 | C7 | C7 | F | F | F | F7 | Bb | Bb | F/C | C7 | F | F')
B_ = Giro('Dm | Dm | A7 | A7 | A7 | A7 | Dm | Dm | Gm | Gm | Dm | Dm | Bb | C7 | F | C7')

MELODIA = (
    '| c5/2 f5/4 | a5/2. | g5/2 e5/4 | c5/2. | bb4/4 c5 e5 | g5/2 bb5/4 | a5/2 f5/4 | c5/2. '
    '| c5/4 f5 a5 | c6/2 eb6/4 | d6/2 bb5/4 | f5/2. | a5/4 c6 a5 | g5/4 e5 bb5 | a5/2. | f5/2 r/4 '
    '| a5/2 d6/4 | f6/2. | e6/2 c#6/4 | a5/2. | g5/4 a5 c#6 | e6/2 g6/4 | f6/2 d6/4 | a5/2. '
    '| bb5/4 d6 g6 | g6/2 d6/4 | f6/4 d6 a5 | f5/2. | f5/4 bb5 d6 | e6/4 c6 bb5 | a5/2 c6/4 | g5/2. |'
)


def partitura(A):
    b = Brano(A, bpm=168, metro=(3, 4))
    vl = b.voce('violini', 23, volume=110, pan=70)
    pf = b.voce('pianoforte', 0, volume=84, pan=44)
    ar = b.voce('arpa', 26, volume=70, pan=96)
    cb = b.voce('contrabbasso', 25, volume=98, pan=64)
    bt = b.voce('triangolo', 39, volume=50, pan=84)
    vl.suona(MELODIA, da=2, vel=96)
    giro = INTRO + A_ + B_
    pf.accordi(giro, '.xx', da=0, registro=(55, 70), vel=66, gate=0.6)
    ar.arpeggi(B_, '1 5 8 10 12 8', da=18, registro=(55, 84), vel=62)
    cb.basso(giro, '1 . .', da=0, registro=(29, 48), gate=0.7)
    bt.batteria({'triangolo': 'x.....'}, da=2, battute=32)
    b.ritornello(2, 34)
    return b.fine()
