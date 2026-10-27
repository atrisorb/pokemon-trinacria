"""Corso Italia: la Catania «bene», tema di casa del protagonista (M-CT-01)."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from notazione import Brano, Giro  # noqa: E402

SIMBOLO = 'SEQ_CT_CORSO_ITALIA'
BANCO = 'BANK_BGM_FIELD1'
VOLUME = 80
SCHEDA = {
    'titolo': 'Corso Italia',
    'carattere': 'casa e quartiere elegante, caldo e un po\' malinconico: il pomeriggio del risveglio, '
                 'la madre che urla dal salone, la vita «per bene» che non è andata come doveva',
    'tonalita': 'Re maggiore',
    'forma': 'introduzione di 2 battute (pianoforte); ritornello A (8) + B (8)',
}

INTRO = Giro('Dmaj7 | A7sus4 A7')
A_ = Giro('Dmaj7 | Bm7 | Em7 | A7 | Dmaj7 | F#m7 B7 | Em7 A7 | D')
B_ = Giro('Gmaj7 | F#m7 | Em7 | A7 | Bm7 | Gmaj7 | Em7 A7 | A7sus4 A7')

MELODIA = (
    '| f#5/4. e5/8 d5/4 e5/8 f#5 | d5/2 b4/4 c#5/8 d5 | g5/4. f#5/8 e5/4 d5/8 e5 | c#5/2 a4/4 r '
    '| f#5/4. e5/8 d5/4 a5 | a5/4. g#5/8 f#5/4 d#5 | e5/4 g5 c#5 e5 | d5/2. r/4 '
    '| b5/4. a5/8 g5/4 f#5 | a5/2 e5/4 f#5/8 a5 | g5/4. f#5/8 e5/4 d5 | c#5/2 e5/4 a5 '
    '| b5/4. a5/8 f#5/4 d5 | d5/4 g5/8 f#5 g5/4 b5 | b5/4. g5/8 e5/4 g5 | a5/2 e5/4 c#5 |'
)


def partitura(A):
    b = Brano(A, bpm=108)
    fl = b.voce('flauto', 35, volume=112, pan=64)
    pf = b.voce('pianoforte', 0, volume=92, pan=40)
    ar = b.voce('archi', 23, volume=70, pan=90)
    bs = b.voce('basso', 19, volume=104, pan=64)
    bt = b.voce('batteria', 39, volume=80, pan=64)
    fl.suona(MELODIA, da=2, vel=100)
    giro = A_ + B_
    pf.arpeggi(INTRO + giro, '1 5 8 10 12 10 8 5', da=0, registro=(48, 80), vel=70)
    ar.accordi(INTRO + giro, 'x-------', da=0, registro=(57, 72), vel=56)
    bs.basso(giro, '1 - - 1 5 - - .', da=2)
    bt.batteria({'cassa': 'x....x..', 'bordo': '..x...x.', 'hh': 'oooooooo'}, da=2, battute=16)
    b.eco(fl, 'flauto eco', ritardo=12, volume=40)
    b.ritornello(2, 18)
    return b.fine()
