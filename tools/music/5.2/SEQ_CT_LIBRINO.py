"""Librino e periferie: Galermo, case popolari, Palazzo di Cemento (M-CT-04, M-CT-05)."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from notazione import Brano, Giro  # noqa: E402

SIMBOLO = 'SEQ_CT_LIBRINO'
BANCO = 'BANK_BGM_FIELD6'
VOLUME = 73
SCHEDA = {
    'titolo': 'Librino',
    'carattere': 'periferia di cemento, ascensori rotti dal 1998, panni stesi: battito lento da hip hop, '
                 'pianoforte che gira in minore e una melodia cantabile di fisarmonica alla maniera '
                 'neomelodica; malinconia ma dignità',
    'tonalita': 'Do minore',
    'forma': 'introduzione di 2 battute (pianoforte); ritornello A (8) + B (8)',
}

INTRO = Giro('Cm | G7')
A_ = Giro('Cm | Ab | Eb | Bb | Cm | Ab | Fm | G7')
B_ = Giro('Abmaj7 | Bb | Gm7 | Cm | Fm7 | Bb7 | Ebmaj7 | G7')

MELODIA = (
    '| g5/4. f5/8 eb5/4 c5 | eb5/4. f5/8 ab5/2 | g5/4 bb5 g5/8 f5 eb5/4 | d5/2. r/4 '
    '| c5/8 d5 eb5/4 g5 c6 | c6/4. bb5/8 ab5/2 | ab5/4 f5 c5/8 db5 c5/4 | b4/2 d5/4 f5 '
    '| c6/2 eb5/4 g5 | f5/2 d5/4 bb4 | bb4/4. d5/8 g5/4 f5 | eb5/2. c5/4 '
    '| c5/4. ab4/8 f4/4 eb5 | d5/4. f5/8 ab5/4 bb5 | g5/2 bb5/4 g5 | f5/4 d5 b4 g4 |'
)


def partitura(A):
    b = Brano(A, bpm=88)
    fs = b.voce('fisarmonica', 13, volume=100, pan=64)
    pf = b.voce('pianoforte', 0, volume=96, pan=36)
    ar = b.voce('archi', 23, volume=58, pan=100)
    bs = b.voce('basso', 21, volume=110, pan=64)
    bt = b.voce('batteria', 39, volume=92, pan=64)
    fs.suona(MELODIA, da=2, vel=96)
    giro = INTRO + A_ + B_
    pf.arpeggi(giro, '1 . 5 8 10 . 8 5', da=0, registro=(48, 76), vel=76)
    ar.accordi(A_ + B_, 'x-------', da=2, registro=(55, 70), vel=50)
    bs.basso(A_ + B_, '1 - - 1 . . 5 .', da=2)
    bt.batteria({'cassa': 'x......x..x.....', 'rullante': '....x.......x...', 'hh': 'o.o.o.o.o.o.o.oo'},
                da=2, battute=16)
    b.ritornello(2, 18)
    return b.fine()
