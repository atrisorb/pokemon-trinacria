"""Le strade della Sicilia occidentale: autostrade, statali e scorrimenti veloci (17 arterie nella
regione Johto del motore)."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from notazione import Brano, Giro  # noqa: E402

SIMBOLO = 'SEQ_TRN_STRADE_OCCIDENTALI'
BANCO = 'BANK_BGM_FIELD3'
VOLUME = 93
SCHEDA = {
    'titolo': 'Strade d\'occidente',
    'carattere': 'le statali lunghe fra le saline, le colline del vino e la Conca d\'Oro: brano di '
                 'strada più largo e caldo di quello d\'oriente, tromba che canta, chitarra in levare, '
                 'mandolino, basso e batteria; la parte B prende il Re minore e il La maggiore come un '
                 'vento di scirocco',
    'tonalita': 'Fa maggiore (parte B in Re minore)',
    'forma': 'introduzione di 2 battute (chitarra e mandolino); ritornello A (8) + B (8)',
}

INTRO = Giro('F | C')
A_ = Giro('F | C | Dm | Bb | F | C | Bb C | F')
B_ = Giro('Dm | A | Dm | A | Bb | F | Gm | C7')

MELODIA = (
    '| c5/4 f5/8 g5 a5/4 c6 | e5/2 g5/4 c6 | d6/4. c6/8 a5/4 f5 | f5/2 d5/4 bb4 '
    '| a4/4 c5/8 f5 a5/4 c6 | e6/4. d6/8 c6/4 g5 | f5/4 d5 e5 g5 | f5/2. r/4 '
    '| a5/4. f5/8 d5/4 a5 | c#6/2 e6/4 a5 | f5/4 a5 d6 f6 | e6/2 c#6/4 a5 '
    '| bb5/4. a5/8 f5/4 d5 | c5/4 f5 a5 c6 | bb5/4. a5/8 g5/4 d5 | e5/2 g5/4 bb5 |'
)


def partitura(A):
    b = Brano(A, bpm=126)
    tr = b.voce('tromba', 29, volume=104, pan=64)
    ch = b.voce('chitarra', 14, volume=74, pan=34)
    md = b.voce('mandolino', 42, volume=66, pan=96)
    bs = b.voce('basso', 19, volume=100, pan=64)
    bt = b.voce('batteria', 39, volume=80, pan=64)
    tr.suona(MELODIA, da=2, vel=96)
    b.eco(tr, 'tromba eco', ritardo=24, volume=40)
    giro = INTRO + A_ + B_
    ch.accordi(giro, '.x.x.x.x', da=0, registro=(55, 69), vel=64, gate=0.5)
    md.arpeggi(giro, '1 5 8 5 10 5 8 5', da=0, registro=(60, 79), vel=58, gate=0.5)
    bs.basso(giro, '1 . 5 . 1 . 5 .', da=0, registro=(29, 48))
    bt.batteria({'cassa': 'x...x...', 'hh': 'x.x.x.x.', 'rullante': '..x...x.'}, da=2, battute=16)
    b.ritornello(2, 18)
    return b.fine()
