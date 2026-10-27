"""Le strade della Sicilia orientale e centrale: autostrade, statali e trazzere (23 arterie nella
regione Kanto del motore)."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from notazione import Brano, Giro  # noqa: E402

SIMBOLO = 'SEQ_TRN_STRADE_ORIENTALI'
BANCO = 'BANK_BGM_FIELD1'
VOLUME = 63
SCHEDA = {
    'titolo': 'Strade d\'oriente',
    'carattere': 'in viaggio fra l\'Etna, gli Iblei e lo Stretto: brano di strada luminoso e in '
                 'movimento, flauto con l\'eco, chitarra ritmica, archi a crome, basso elettrico e '
                 'batteria; la parte B sale verso il Si minore e torna a casa sul La',
    'tonalita': 'Re maggiore',
    'forma': 'introduzione di 2 battute (chitarra e batteria); ritornello A (8) + B (8)',
}

INTRO = Giro('D | A7')
A_ = Giro('D | A | Bm | G | D | A | G A | D')
B_ = Giro('G | A | F#m | Bm | Em | A | G | A7')

MELODIA = (
    '| a5/4. f#5/8 d5/4 f#5 | e5/4 a5/8 b5 c#6/4 a5 | d6/4. c#6/8 b5/4 f#5 | g5/2 b5/4 d6 '
    '| f#6/4. e6/8 d6/4 a5 | c#6/4 e6/8 c#6 a5/4 e5 | b5/4 g5 a5 c#6 | d6/2. r/4 '
    '| d6/4. b5/8 g5/4 b5 | c#6/4. a5/8 e5/4 a5 | a5/4 c#6 f#6 c#6 | d6/2 b5/4 f#5 '
    '| g5/4. f#5/8 e5/4 b5 | a5/4 c#6 e6 a6 | g6/4. f#6/8 d6/4 b5 | a5/2 g5/4 e5 |'
)


def partitura(A):
    b = Brano(A, bpm=138)
    fl = b.voce('flauto', 35, volume=110, pan=64)
    ch = b.voce('chitarra', 14, volume=76, pan=92)
    ar = b.voce('archi', 23, volume=68, pan=34)
    bs = b.voce('basso', 22, volume=104, pan=64)
    bt = b.voce('batteria', 39, volume=84, pan=64)
    fl.suona(MELODIA, da=2, vel=98)
    b.eco(fl, 'flauto eco', ritardo=24, volume=42)
    giro = INTRO + A_ + B_
    ch.accordi(giro, 'x.xx.xx.', da=0, registro=(55, 69), vel=66, gate=0.5)
    ar.accordi(A_ + B_, 'x-x-x-x-', da=2, registro=(57, 72), vel=56, voci=2)
    bs.basso(giro, '1 . 1 5 1 . 1 5', da=0, registro=(33, 52), gate=0.6)
    bt.batteria({'cassa': 'x...x...', 'hh': 'x.x.x.x.'}, da=0, battute=2)
    bt.batteria({'cassa': 'x..x..x.x.......', 'rullante': '....x.......x...', 'hh': 'x.x.x.x.x.x.x.x.'},
                da=2, battute=16)
    b.ritornello(2, 18)
    return b.fine()
