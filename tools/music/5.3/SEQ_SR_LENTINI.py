"""Lentini e Carlentini: gli aranceti e il Biviere."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from notazione import Brano, Giro  # noqa: E402

SIMBOLO = 'SEQ_SR_LENTINI'
BANCO = 'BANK_BGM_FIELD13'
VOLUME = 73
SCHEDA = {
    'titolo': 'Lentini, gli aranceti',
    'carattere': 'campagna di agrumi fino al lago del Biviere: danza leggera in 6/8, flauto che salta '
                 'fra i filari, mandolino arpeggiato, chitarra e tamburello col triangolo; profuma di '
                 'zagara anche se i magazzini sono occupati',
    'tonalita': 'Sol maggiore (seconda passata in Do maggiore)',
    'forma': 'introduzione di 2 battute (mandolino); ritornello A (8) + B (8) in Sol maggiore, poi le stesse 16 battute in Do maggiore, in 6/8',
}

INTRO = Giro('G | D')
A_ = Giro('G | C | G | D | G | C | Am D | G')
B_ = Giro('Em | Bm | C | G | Am | D | C D | G')

MELODIA = (
    '| d5/8 g5 b5 d6/4 b5/8 | c6/4. e6/8 d6 c6 | b5/4 a5/8 g5/4 d5/8 | a5/4. f#5/4. '
    '| g5/8 a5 b5 d6/4 g6/8 | e6/4 c6/8 g5/4 e5/8 | a5/4 c6/8 d6/4 f#5/8 | g5/4. r/4. '
    '| b5/8 c6 b5 g5/4 e5/8 | f#5/4. d5/4 f#5/8 | e5/8 g5 c6 e6/4 c6/8 | d6/4. b5/4. '
    '| c6/8 b5 a5 e5/4 a5/8 | f#5/4. a5/4 d6/8 | e6/4 c6/8 d6/4 a5/8 | g5/4. r/4. |'
)


def partitura(A):
    b = Brano(A, bpm=116, metro=(6, 8))
    fl = b.voce('flauto', 35, volume=108, pan=64)
    md = b.voce('mandolino', 42, volume=88, pan=40)
    ch = b.voce('chitarra', 14, volume=70, pan=88)
    bs = b.voce('basso', 19, volume=96, pan=64)
    pc = b.voce('tamburello', 39, volume=66, pan=96)
    fl.suona(MELODIA, da=2, vel=96)
    md.arpeggi(INTRO + A_ + B_, '1 5 8 10 8 5', da=0, registro=(55, 79), vel=74)
    ch.accordi(A_ + B_, 'x..x..', da=2, registro=(52, 67), vel=60, gate=0.6)
    bs.basso(A_ + B_, '1 - - 5 - -', da=2)
    pc.batteria({'tamburello': 'x..o..', 'triangolo': '...x..'}, da=2, battute=16)
    b.ripeti(2, 16, 18, trasponi=5)
    b.eco(fl, 'flauto eco', ritardo=12, volume=36)
    b.ritornello(2, 34)
    return b.fine()
