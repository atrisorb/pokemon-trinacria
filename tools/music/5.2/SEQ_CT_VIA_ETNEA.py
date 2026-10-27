"""Via Etnea: il caos della strada principale di Catania (M-CT-02, S-CT-01)."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from notazione import Brano, Giro  # noqa: E402

SIMBOLO = 'SEQ_CT_VIA_ETNEA'
BANCO = 'BANK_BGM_FIELD4'
VOLUME = 72
SCHEDA = {
    'titolo': 'Via Etnea',
    'carattere': 'traffico, promoter e strilloni, folla e vetrine fino a Villa Bellini: allegro e affollato, '
                 'coi clacson degli ottoni a fine frase; la parte B si apre verso il giardino',
    'tonalita': 'Si bemolle maggiore',
    'forma': 'introduzione di 2 battute (clacson e batteria); ritornello A (8) + B (8)',
}

INTRO = Giro('Bb | F7')
A_ = Giro('Bb | Gm7 | Cm7 | F7 | Bb | Bb7 | Eb Edim7 | Bb/F F7')
B_ = Giro('Ebmaj7 | Dm7 | Cm7 | F7 | Ebmaj7 | Dm7 G7 | Cm7 F7 | Bb F7')

MELODIA = (
    '| d5/8 f5 r f5 d5/8 c5 bb4/4 | g4/8 bb4 d5 g5 f5/4 d5 | eb5/8 eb5 r c5 eb5/8 g5 bb5/4 '
    '| a5/4. f5/8 c5/4 eb5 | d5/8 f5 r f5 d5/8 c5 bb4/4 | ab5/8 g5 f5 d5 bb4/4 ab4 '
    '| g4/8 bb4 eb5 g5 bb5/4 g5 | f5/4 d5/8 bb4 a4/4 c5 '
    '| g5/2 bb5/4 g5 | f5/2. d5/4 | eb5/4. d5/8 c5/4 g4 | a4/2 c5/4 eb5 '
    '| d5/4 eb5/8 f5 g5/4 bb5 | a5/4 f5 g5 b4 | c5/4 eb5 f5 a4 | bb4/2 r/4 c5 |'
)
CLACSON = '| r/1 | r/2. f4+a4/16> r/16 f4+a4/8> |'


def partitura(A):
    b = Brano(A, bpm=138)
    tr = b.voce('tromba', 29, volume=108, pan=70)
    fl = b.voce('flauto', 35, volume=52, pan=100)
    cl = b.voce('clacson', 30, volume=96, pan=30)
    ch = b.voce('accordi', 3, volume=88, pan=36)
    bs = b.voce('basso', 22, volume=110, pan=64)
    bt = b.voce('batteria', 39, volume=84, pan=64)
    tr.suona(MELODIA, da=2, vel=100)
    fl.suona(MELODIA, da=2, vel=90, trasponi=12)
    for n in (0, 4, 8):                           # clacson a fine frase della parte A e nell'intro
        cl.suona(CLACSON, da=n, vel=100)
    giro = INTRO + A_ + B_
    ch.accordi(giro, '.x.x.x.x', da=0, registro=(58, 74), vel=70)
    bs.basso(giro, '1 - 5 - 8 - 5 3', da=0)
    bt.batteria({'cassa': 'x..x..x.', 'rullante': '..x...x.', 'hh': 'xoxoxoxo'}, da=0, battute=18)
    b.ritornello(2, 18)
    return b.fine()
