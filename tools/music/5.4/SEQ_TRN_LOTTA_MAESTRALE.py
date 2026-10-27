"""Lotta con Maestrale (Suicune), il terzo dei Tre Venti di Sicilia (P-07)."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from notazione import Brano, Giro  # noqa: E402

SIMBOLO = 'SEQ_TRN_LOTTA_MAESTRALE'
BANCO = 'BANK_BGM_BATTLE6'
VOLUME = 98
SCHEDA = {
    'titolo': 'Maestrale',
    'carattere': 'la corrente che purifica i mari e le sorgenti: flauto agile sopra l\'arpa che scorre '
                 'a semicrome come l\'acqua, archi tenuti, basso elettrico e batteria più leggera degli '
                 'altri due Venti; stesso inizio di frase dei Tre Venti, in Re minore',
    'tonalita': 'Re minore (parte B in Fa maggiore)',
    'forma': 'introduzione di 2 battute; ritornello A (8) + B (8)',
}

INTRO = Giro('Dm | A7')
A_ = Giro('Dm | Bb | F | C | Dm | Bb | Gm | A')
B_ = Giro('F | C | Dm | Am | Bb | F | Gm | A7')

APERTURA = '| d5/8 e5 f5 g5 a5/4 d6 | e6/4. c#6/8 a5/4 g5 |'
MELODIA = (
    '| a5/4 d6/8 e6 f6/4 d6 | d6/4. c6/8 bb5/4 f5 | a5/4 c6 f6 c6 | e6/2 g6/4 e6 '
    '| f6/4. e6/8 d6/4 a5 | bb5/4 d6 f6 bb6 | g6/4. f6/8 d6/4 bb5 | a5/2 c#6/4 e6 '
    '| f6/4. g6/8 a6/4 f6 | e6/4. d6/8 c6/4 g5 | a5/4 d6 f6 a6 | e6/2 c6/4 a5 '
    '| d6/4. c6/8 bb5/4 f5 | a5/4 c6 f6 a6 | g6/4. f6/8 d6/4 bb5 | c#6/2 e6/4 g6 |'
)


def partitura(A):
    b = Brano(A, bpm=172)
    fl = b.voce('flauto', 35, volume=114, pan=64)
    ar = b.voce('arpa', 26, volume=78, pan=96)
    ac = b.voce('archi', 24, volume=70, pan=30)
    bs = b.voce('basso', 22, volume=110, pan=64)
    bt = b.voce('batteria', 39, volume=88, pan=64)
    fl.suona(APERTURA, da=0, vel=102).suona(MELODIA, da=2, vel=100)
    b.eco(fl, 'archi ottava', ritardo=0, volume=72, pan=40, trasponi=-12, programma=23)
    giro = INTRO + A_ + B_
    ar.arpeggi(giro, '1 5 8 10 12 10 8 5 1 5 8 10 12 10 8 5', da=0, registro=(50, 81), vel=66, gate=0.6)
    ac.accordi(A_ + B_, 'x-------', da=2, registro=(55, 70), vel=58)
    bs.basso(giro, '1 . 1 8 1 . 5 8', da=0, registro=(26, 45), gate=0.6)
    bt.batteria({'cassa': 'x.......x.......', 'rullante': '....x.......x...', 'hh': 'x.x.x.x.x.x.x.x.'},
                da=0, battute=18)
    b.ritornello(2, 18)
    return b.fine()
