"""I paesi etnei: Misterbianco, Nicolosi, Paternò, Adrano, Bronte, Randazzo (M-CT-07, S-CT-05/06/08)."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from notazione import Brano, Giro  # noqa: E402

SIMBOLO = 'SEQ_CT_PAESI_ETNEI'
BANCO = 'BANK_BGM_FIELD3'
VOLUME = 73
SCHEDA = {
    'titolo': 'I paesi etnei',
    'carattere': 'paesi di pietra lavica, pistacchieti e vigne: pastorale in 6/8 alla maniera di '
                 'ciaramella e zampogna (melodia d\'ancia acuta sopra un bordone di Sol e Re che non si '
                 'ferma mai), tamburello leggero solo nella parte B',
    'tonalita': 'Sol maggiore',
    'forma': 'introduzione di 2 battute (bordone e zampogna); ritornello A (8) + B (8) in Sol maggiore, poi le stesse 16 battute in Re maggiore col bordone che scende a Re–La, in 6/8',
}

INTRO = Giro('G | D')
A_ = Giro('G | G | D | G | C | G | D | G')
B_ = Giro('Em | Bm | C | D | G | C | D7 | G')

MELODIA = (
    '| b5/8 c6 d6 b5/4 g5/8 | d6/8 c6 b5 b5/4 a5/8 | a5/4 f#5/8 d5/4 a5/8 | g5/4. b5/4 d6/8 '
    '| e6/8 d6 c6 g5/4 e5/8 | d6/4 b5/8 g5/4 b5/8 | a5/8 b5 c6 a5/4 f#5/8 | g5/4. r/4. '
    '| g5/8 a5 b5 e6/4 b5/8 | d6/8 c#6 b5 f#5/4 d5/8 | e5/8 g5 c6 e6/4 c6/8 | d6/4. a5/4 f#5/8 '
    '| b5/8 c6 d6 g6/4 d6/8 | e6/8 d6 c6 e6/4 g5/8 | f#5/8 a5 d6 c6/4 a5/8 | g5/4. r/4. |'
)


def partitura(A):
    b = Brano(A, bpm=120, metro=(6, 8))
    ci = b.voce('ciaramella', 33, volume=108, pan=64)
    bo = b.voce('bordone', 12, volume=70, pan=64, pedale=True)
    zp = b.voce('zampogna', 34, volume=84, pan=40)
    bs = b.voce('contrabbasso', 25, volume=90, pan=64)
    pc = b.voce('tamburello', 39, volume=70, pan=90)
    ci.suona(MELODIA, da=2, vel=98)
    for n in range(18):                           # bordone di Sol e Re, battuta per battuta
        bo.suona('g3+d4/2._', da=n, vel=70)
    giro = INTRO + A_ + B_
    zp.arpeggi(giro, '1 . 5 8 . 5', da=0, registro=(55, 67), vel=72)
    bs.basso(A_ + B_, '1 - - - - -', da=2, gate=0.95)
    pc.batteria({'tamburello': 'x..o..'}, da=10, battute=8)
    b.ripeti(2, 16, 18, trasponi=-5)
    b.eco(ci, 'ciaramella eco', ritardo=12, volume=36)
    b.ritornello(2, 34)
    return b.fine()
