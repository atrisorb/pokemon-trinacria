"""Fontanarossa in crisi: allarme cenere al Terminal A (M-CT-09, dungeon D-CT-04)."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from notazione import Brano, Giro  # noqa: E402

SIMBOLO = 'SEQ_CT_FONTANAROSSA_CRISI'
BANCO = 'BANK_BGM_DUNGEON9'
VOLUME = 81
SCHEDA = {
    'titolo': 'Fontanarossa in crisi',
    'carattere': 'pioggia di cenere, tabelloni «CANCELLATO», folla a terra: si apre col «din-don» degli '
                 'annunci e una sirena, poi ostinato teso degli archi, timpani e ottoni; nella parte B '
                 'la sirena sale all\'acuto e l\'accordo napoletano (Mi bemolle) chiude la frase',
    'tonalita': 'Re minore',
    'forma': 'introduzione di 2 battute (annuncio e sirena); ritornello A (8) + B (8)',
}

INTRO = Giro('Dm | A7')
A_ = Giro('Dm | Dm | Bb | A | Dm | Dm | Gm | A7')
B_ = Giro('Bb | C | A/C# | Dm | Bb | Gm | Eb | A7')

MELODIA = (
    '| d5/4. a4/8 d5 e5 f5/4 | f5/8 e5 d5 e5 a4/2 | bb4/4. c5/8 d5/4 f5 | e5/2 c#5 '
    '| d5/4. a4/8 d5 e5 f5/4 | a5/8 g5 f5 e5 d5/2 | g5/4. f5/8 d5/4 bb4 | c#5/2 e5/4 a5 '
    '| d6/2 f6 | e6/2 g6 | e6/2 c#6 | d6/2 a5 '
    '| bb5/4 a5/8 bb5 d6/4 f6 | g6/4 d6 bb5/2 | g6/4 eb6 bb5 g5 | a5/2 c#6/4 e6 |'
)


def partitura(A):
    b = Brano(A, bpm=138)
    ot = b.voce('ottoni', 29, volume=110, pan=60)
    an = b.voce('annuncio', 5, volume=96, pan=64)
    sr = b.voce('sirena', 37, volume=70, pan=20)
    os_ = b.voce('ostinato', 17, volume=96, pan=100)
    tb = b.voce('tromboni', 30, volume=84, pan=30)
    bs = b.voce('basso', 22, volume=112, pan=64)
    tp = b.voce('timpani', 28, volume=100, pan=64)
    bt = b.voce('batteria', 39, volume=92, pan=64)
    an.suona('| a5/4 f5 d5/2 | r/1 |', da=0, vel=100)
    sr.suona('| r/1 | a5/4 d6 a5 d6 |', da=0, vel=90)
    ot.suona(MELODIA, da=2, vel=100)
    giro = INTRO + A_ + B_
    os_.arpeggi(A_ + B_, '1 1 5 1 8 1 5 1', da=2, registro=(50, 74), vel=80, gate=0.6)
    tb.accordi(A_ + B_, 'x---.x.x', da=2, registro=(50, 65), vel=72, gate=0.7)
    bs.basso(giro, '1 1 . 1 1 . 5 .', da=0, gate=0.7)
    tp.basso(giro, '1 . . . . . 1 1', da=0, registro=(45, 57), vel=96, gate=0.5)
    bt.batteria({'cassa': 'x..x..x.x..x..x.', 'rullante': '....x.......x...', 'hh': 'x.x.x.x.x.x.x.x.'},
                da=2, battute=16)
    b.ritornello(2, 18)
    return b.fine()
