"""Il viaggio: traghetto per Lampedusa e dello Stretto, aliscafi per Favignana e le Eolie, pullman
regionale delle 5:40. Lo slot HeartGold (SEQ_GS_E_LINEAR) non si ripete: il brano finisce (A10)."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from notazione import Brano, Giro  # noqa: E402

SIMBOLO = 'SEQ_TRN_TRAGHETTO'
BANCO = 'BANK_BASIC'
VOLUME = 100
SCHEDA = {
    'titolo': 'Il viaggio',
    'carattere': 'si parte: due colpi di sirena della nave (tromboni gravi), poi il motore che batte '
                 'a crome sotto un flauto sereno che guarda il mare allontanarsi; finisce su un '
                 'accordo tenuto, come nello slot HeartGold che non si ripete',
    'tonalita': 'Fa maggiore',
    'forma': 'introduzione di 2 battute (sirena e motore); frase di 8 battute; accordo finale di 1 battuta; nessun ritornello',
}

FRASE = Giro('F | C | Dm | Bb | F | C | Bb C | F')
FINE = Giro('F')

SIRENA = '| f2+c3/2_ r/2 | f2+c3/1_ |'
MELODIA = (
    '| c5/4 f5/4 a5/4. g5/8 | g5/2 e5/2 | f5/4 a5/4 d6/2 | d6/4. c6/8 bb5/2 '
    '| a5/4 c6/4 f6/2 | e6/4. d6/8 c6/2 | d6/4 bb5/4 c6/4 e6/4 | f6/2. r/4 | f5/1 |'
)


def partitura(A):
    b = Brano(A, bpm=116)
    sr = b.voce('sirena', 30, volume=110, pan=64, pedale=True)
    fl = b.voce('flauto', 35, volume=110, pan=64)
    ar = b.voce('archi', 23, volume=80, pan=88)
    cb = b.voce('motore', 25, volume=92, pan=40)
    bt = b.voce('batteria', 39, volume=58, pan=64)
    sr.suona(SIRENA, da=0, vel=100)
    fl.suona(MELODIA, da=2, vel=96)
    ar.accordi(FRASE + FINE, 'x-------', da=2, registro=(55, 72), vel=64)
    cb.basso(Giro('F | F') + FRASE, '1 . 1 . 1 . 1 .', da=0, gate=0.6)
    cb.basso(FINE, '1 - - - - - - -', da=10)
    bt.batteria({'hh': 'x.x.x.x.'}, da=0, battute=10)
    b.fine_a(11)
    return b.fine()
