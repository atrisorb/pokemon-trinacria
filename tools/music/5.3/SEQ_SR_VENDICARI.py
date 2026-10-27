"""La riserva di Vendicari: le aree Safari."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from notazione import Brano, Giro  # noqa: E402

SIMBOLO = 'SEQ_SR_VENDICARI'
BANCO = 'BANK_BGM_FIELD18'
VOLUME = 87
SCHEDA = {
    'titolo': 'La riserva di Vendicari',
    'carattere': 'la caccia nelle zone della riserva: allegra e curiosa, flauto che corre sopra un '
                 'ostinato di marimba, archi a mezze note, basso e batteria vivaci; è la musica che '
                 'accompagna i Pokémon più rari della provincia',
    'tonalita': 'Sol maggiore',
    'forma': 'introduzione di 2 battute (marimba e batteria); ritornello A (8) + B (8)',
}

INTRO = Giro('G | D')
A_ = Giro('G | Em | C | D | G | Bm | C D | G')
B_ = Giro('C | D | Bm | Em | Am | D | C | D7')

MELODIA = (
    '| g5/8 a5/8 b5/4 d6/4 b5/4 | e6/4. d6/8 b5/2 | c6/4 e6/4 g6/4 e6/4 | f#6/2 d6/2 '
    '| b5/4 g5/4 d5/4 g5/4 | f#5/4. b5/8 d6/2 | e6/4 c6/4 d6/4 a5/4 | g5/2. r/4 '
    '| e5/4 g5/4 c6/4. b5/8 | a5/2 f#5/2 | d5/4 f#5/4 b5/4. a5/8 | g5/2 e5/2 '
    '| c6/4 a5/4 e6/4 c6/4 | d6/4. c6/8 a5/2 | g5/4 e5/4 c6/4 e6/4 | f#6/2 c6/2 |'
)


def partitura(A):
    b = Brano(A, bpm=136)
    fl = b.voce('flauto', 35, volume=110, pan=64)
    mr = b.voce('marimba', 18, volume=86, pan=40)
    ar = b.voce('archi', 23, volume=76, pan=88)
    bs = b.voce('basso', 22, volume=98, pan=64)
    bt = b.voce('batteria', 39, volume=76, pan=64)
    fl.suona(MELODIA, da=2, vel=96)
    giro = INTRO + A_ + B_
    mr.arpeggi(giro, '1 8 5 8 10 8 5 8', da=0, registro=(55, 79), vel=72)
    ar.accordi(A_ + B_, 'x---x---', da=2, registro=(55, 72), vel=60)
    bs.basso(giro, '1 . 1 5 1 . 5 .', da=0)
    bt.batteria({'cassa': 'x...x...', 'rullante': '..x...x.', 'hh': 'xxxxxxxx'}, da=0, battute=18)
    b.eco(fl, 'flauto eco', ritardo=12, volume=36)
    b.ritornello(2, 18)
    return b.fine()
