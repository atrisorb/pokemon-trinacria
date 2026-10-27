"""Lotta coi capi dei padiglioni della Fiera del Mediterraneo (P-09)."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from notazione import Brano, Giro  # noqa: E402

SIMBOLO = 'SEQ_TRN_LOTTA_FIERA_CAPI'
BANCO = 'BANK_BGM_BATTLE4'
VOLUME = 100
SCHEDA = {
    'titolo': 'I capi della Fiera',
    'carattere': 'la finale di un torneo pulito, senza raccomandazioni: tema sportivo e tirato in Sol '
                 'minore per tromba e archi all\'ottava, accordi ribattuti di tastiera, basso elettrico '
                 'e batteria piena; la parte B si apre in Si bemolle come un pubblico che si alza',
    'tonalita': 'Sol minore',
    'forma': 'introduzione di 2 battute; ritornello A (8) + B (8)',
}

INTRO = Giro('Gm | D7')
A_ = Giro('Gm | Eb | Bb | F | Gm | Eb | Cm | D')
B_ = Giro('Eb | F | Bb | Gm | Cm | F | Eb | D7')

APERTURA = '| g5/8 bb5 d6 g6 bb6/4 g6 | a6/4 f#6 d6 c6 |'
MELODIA = (
    '| g5/4 bb5/8 c6 d6/4 g6 | g6/4. f6/8 eb6/4 bb5 | d6/4 f6 bb6 f6 | a6/2 f6/4 c6 '
    '| d6/4. c6/8 bb5/4 g5 | g5/4 bb5 eb6 g6 | g6/4. f6/8 eb6/4 c6 | d6/2 f#6/4 a6 '
    '| g6/4. f6/8 eb6/4 bb5 | a5/4. bb5/8 c6/4 f6 | f6/4 d6 bb5 d6 | g6/2 d6/4 bb5 '
    '| c6/4 eb6 g6 eb6 | f6/4. eb6/8 c6/4 a5 | bb5/4 eb6 g6 bb6 | a6/2 f#6/4 c6 |'
)


def partitura(A):
    b = Brano(A, bpm=176)
    tr = b.voce('tromba', 29, volume=116, pan=64)
    ta = b.voce('tastiera', 3, volume=80, pan=96)
    bs = b.voce('basso', 22, volume=112, pan=64)
    tp = b.voce('timpani', 28, volume=96, pan=64)
    bt = b.voce('batteria', 39, volume=98, pan=64)
    tr.suona(APERTURA, da=0, vel=106).suona(MELODIA, da=2, vel=102)
    b.eco(tr, 'archi ottava', ritardo=0, volume=76, pan=28, trasponi=-12, programma=23)
    giro = INTRO + A_ + B_
    ta.accordi(giro, 'x.xx.xx.x.xx.xx.', da=0, registro=(55, 69), vel=64, gate=0.5)
    bs.basso(giro, '1 1 8 1 1 1 8 1', da=0, registro=(31, 50), gate=0.6)
    tp.basso(giro, '1 . . . 5, . . .', da=0, registro=(41, 53), vel=100, gate=0.5)
    norm = {'cassa': 'x.....x.x.......', 'rullante': '....x.......x...', 'hh': 'x.x.x.x.x.x.x.x.'}
    fill = {'cassa': 'x.....x.x.......', 'rullante': '....x.....xxxxxx', 'hh': 'x.x.x.x.x.......'}
    bt.batteria({'rullante': 'x.x.x.x.x.x.x.x.'}, da=0, battute=2)
    bt.batteria([norm] * 7 + [fill], da=2, battute=16)
    b.ritornello(2, 18)
    return b.fine()
