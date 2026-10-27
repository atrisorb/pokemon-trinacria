"""Lotta con gli altri leggendari antichi (Groudon, Kyogre, Rayquaza)."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from notazione import Brano, Giro  # noqa: E402

SIMBOLO = 'SEQ_TRN_LOTTA_LEGGENDARI_ANTICHI'
BANCO = 'BANK_BGM_BATTLE1'
VOLUME = 110
SCHEDA = {
    'titolo': 'I leggendari antichi',
    'carattere': 'forze più vecchie dell\'isola, la terra, il mare e il cielo: due battute di colpi '
                 'all\'unisono, poi un tema pesante in Re minore per tromba e archi gravi sopra '
                 'tromboni a crome, tom e timpani; la parte B tocca il Mi bemolle (la seconda abbassata) '
                 'come un terremoto',
    'tonalita': 'Re minore',
    'forma': 'introduzione di 2 battute; ritornello A (8) + B (8)',
}

INTRO = Giro('Dm | Dm')
A_ = Giro('Dm | C | Bb | A | Dm | C | Bb | A')
B_ = Giro('Gm | Dm | Eb | A | Gm | Dm | Eb | A7')

APERTURA = '| d5/8> d5 r/4 d5/8> d5 r/4 | d5/8 f5 a5 d6 f6/4 a6 |'
MELODIA = (
    '| d5/4. f5/8 a5/4 d6 | c6/4. g5/8 e5/4 g5 | f5/4 bb5 d6 f6 | e6/2 c#6/4 a5 '
    '| a5/4. d6/8 f6/4 a6 | g6/4. e6/8 c6/4 g5 | bb5/4 d6 f6 d6 | c#6/2. r/4 '
    '| g5/4. bb5/8 d6/4 g6 | f6/4. e6/8 d6/4 a5 | g5/4 bb5 eb6 g6 | e6/2 c#6/4 a5 '
    '| d6/4 bb5 g5 bb5 | a5/4 f5 d5 f5 | eb5/4 g5 bb5 eb6 | e6/2 c#6/4 g5 |'
)


def partitura(A):
    b = Brano(A, bpm=168)
    tr = b.voce('tromba', 29, volume=116, pan=64)
    tb = b.voce('tromboni', 30, volume=100, pan=30)
    bs = b.voce('basso', 22, volume=114, pan=64)
    tp = b.voce('timpani', 28, volume=108, pan=64)
    bt = b.voce('tamburi', 39, volume=100, pan=64)
    tr.suona(APERTURA, da=0, vel=108).suona(MELODIA, da=2, vel=104)
    b.eco(tr, 'archi gravi', ritardo=0, volume=82, pan=96, trasponi=-12, programma=23)
    giro = INTRO + A_ + B_
    tb.accordi(giro, 'x.x.x.x.', da=0, registro=(45, 60), vel=78, voci=2, gate=0.5)
    bs.basso(giro, '1 1 8 1 1 1 8 1', da=0, registro=(26, 45), gate=0.6)
    tp.basso(giro, '1 . 1 . 1 . 1 .', da=0, registro=(38, 50), vel=104, gate=0.5)
    bt.batteria({'tom_b': 'x.....x.x.....x.', 'tom_m': '....x.......x...'}, da=0, battute=2)
    bt.batteria({'cassa': 'x..x..x.x..x..x.', 'rullante': '....x.......x...', 'tom_b': '..............xx',
                 'hh': 'x.x.x.x.x.x.x.x.'}, da=2, battute=16)
    b.ritornello(2, 18)
    return b.fine()
