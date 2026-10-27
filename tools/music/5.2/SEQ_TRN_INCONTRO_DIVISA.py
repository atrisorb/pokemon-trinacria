"""Incontro: agenti e vigili, coppie di amici."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from notazione import Brano, Giro  # noqa: E402

SIMBOLO = 'SEQ_TRN_INCONTRO_DIVISA'
BANCO = 'BANK_BASIC'
VOLUME = 89
SCHEDA = {
    'titolo': 'Incontro — divise',
    'carattere': 'il vigile al crocevia: tre colpi di fischietto (ottavino), poi una marcia d\'ordinanza '
                 'in Si bemolle col rullante da banda',
    'tonalita': 'Si bemolle maggiore',
    'forma': 'introduzione di 1 battuta (fischietto); ritornello di 8 battute',
}

INTRO = Giro('F7')
GIRO = Giro('Bb | F | Bb | F7 | Bb | Eb | F7 | Bb')

MELODIA = (
    '| d5/8 d5 f5 bb5 d6/4 bb5 | c6/4. a5/8 f5/4 c5 | d5/8 f5 bb5 d6 f6/4 d6 | eb6/4 c6 a5 f5 '
    '| d6/4. bb5/8 f5/4 d5 | eb5/8 g5 bb5 eb6 g6/4 eb6 | f6/4 eb6 c6 a5 | bb5/2. r/4 |'
)


def partitura(A):
    b = Brano(A, bpm=132)
    fi = b.voce('fischietto', 37, volume=96, pan=90)
    tr = b.voce('tromba', 29, volume=112, pan=60)
    ch = b.voce('ottoni', 30, volume=84, pan=30)
    bs = b.voce('basso', 22, volume=108, pan=64)
    bt = b.voce('batteria', 39, volume=96, pan=64)
    fi.suona("| f6/8'> r f6'> r f6/4> r |", da=0, vel=100)
    tr.suona(MELODIA, da=1, vel=102)
    giro = INTRO + GIRO
    ch.accordi(giro, '.x.x.x.x', da=0, registro=(53, 67), vel=70, gate=0.5)
    bs.basso(giro, '1 . 5 . 1 . 5 .', da=0, registro=(34, 50))
    bt.batteria({'rullante': 'x.oox.oox.oox.oo', 'cassa': 'x.......x.......'}, da=0, battute=9)
    b.ritornello(1, 9)
    return b.fine()
