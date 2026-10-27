"""Le onde ad alta frequenza del MUOS di Niscemi (recinzione e parabole)."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from notazione import Brano, Giro  # noqa: E402

SIMBOLO = 'SEQ_CL_MUOS_ONDE'
BANCO = 'BANK_BASIC'
VOLUME = 92
SCHEDA = {
    'titolo': 'Le onde del MUOS',
    'carattere': 'le grandi parabole dentro la sughereta: un segnale elettronico che pulsa a '
                 'sedicesime sulle onde quadre (PSG), bip acuti a intervalli fissi, un basso '
                 'sintetico tenuto e archi lenti in basso; il Si bemolle in Mi minore (il tritono) '
                 'rende il segnale inquietante',
    'tonalita': 'Mi minore (col Si bemolle)',
    'forma': 'introduzione di 1 battuta (impulsi); ritornello di 8 battute',
}

INTRO = Giro('Em')
GIRO = Giro('Em | Em | C | C | Em | Em | Bb | B7')

SEGNALE = (
    '| e6/8 r/8 e6/8 r/8 b6/4 r/4 | r/1 | e6/8 r/8 e6/8 r/8 g6/4 r/4 | r/1 '
    '| b6/8 r/8 b6/8 r/8 e7/4 r/4 | r/1 | bb6/8 r/8 bb6/8 r/8 f6/4 r/4 | a6/8 r/8 a6/8 r/8 d#6/4 r/4 |'
)


def partitura(A):
    b = Brano(A, bpm=120)
    im = b.voce('impulsi PSG', 48, volume=64, pan=40)
    sg = b.voce('segnale PSG', 49, volume=72, pan=88)
    bs = b.voce('basso', 21, volume=96, pan=64)
    ar = b.voce('archi', 24, volume=62, pan=64)
    im.arpeggi(INTRO + GIRO, '1 5 8 5 12 5 8 5 1 5 8 5 12 5 8 5', da=0, registro=(64, 88), vel=70, gate=0.5)
    sg.suona(SEGNALE, da=1, vel=90)
    bs.basso(INTRO + GIRO, '1 - - - - - - -', da=0)
    ar.accordi(GIRO, 'x-------', da=1, registro=(48, 64), vel=56)
    b.ritornello(1, 9)
    return b.fine()
