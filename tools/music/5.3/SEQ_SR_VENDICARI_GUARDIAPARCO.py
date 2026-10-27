"""La casa del guardiaparco di Vendicari."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from notazione import Brano, Giro  # noqa: E402

SIMBOLO = 'SEQ_SR_VENDICARI_GUARDIAPARCO'
BANCO = 'BANK_BGM_FIELD18'
VOLUME = 79
SCHEDA = {
    'titolo': 'Il guardiaparco',
    'carattere': 'la stanza dove si ritira l\'attrezzatura della riserva: tranquilla e accogliente, '
                 'vibrafono su accordi di settima, chitarra arpeggiata, basso morbido e un bordo di '
                 'rullante appena accennato',
    'tonalita': 'Si bemolle maggiore',
    'forma': 'introduzione di 2 battute (chitarra); ritornello A (8) + B (8)',
}

INTRO = Giro('Bbmaj7 | Ebmaj7')
A_ = Giro('Bbmaj7 | Gm7 | Cm7 | F7 | Bbmaj7 | Gm7 | Cm7 F7 | Bbmaj7')
B_ = Giro('Ebmaj7 | Dm7 | Cm7 | F7 | Ebmaj7 | Dm7 G7 | Cm7 | F7')

MELODIA = (
    '| d5/4 f5/4 a5/2 | bb5/4. g5/8 d5/2 | eb5/4 g5/4 bb5/4 g5/4 | a5/2 f5/2 '
    '| f5/4 bb5/4 d6/2 | d6/4. bb5/8 g5/2 | g5/4 eb5/4 f5/4 a5/4 | bb5/2. r/4 '
    '| g5/4 bb5/4 d6/2 | c6/4. a5/8 f5/2 | eb5/4 g5/4 c6/4 bb5/4 | a5/2. c6/4 '
    '| bb5/4 g5/4 eb5/2 | f5/4 a5/4 b5/4 d6/4 | eb6/2 c6/2 | a5/2 f5/2 |'
)


def partitura(A):
    b = Brano(A, bpm=92)
    vb = b.voce('vibrafono', 5, volume=104, pan=64)
    ch = b.voce('chitarra', 7, volume=84, pan=40)
    bs = b.voce('basso', 20, volume=96, pan=64)
    bt = b.voce('batteria', 39, volume=58, pan=80)
    vb.suona(MELODIA, da=2, vel=94)
    giro = INTRO + A_ + B_
    ch.arpeggi(giro, '1 5 8 10 7 5 8 5', da=0, registro=(48, 72), vel=70)
    bs.basso(giro, '1 - - - 5 - - -', da=0)
    bt.batteria({'bordo': '....x...', 'hh': 'o.o.o.o.'}, da=2, battute=16)
    b.eco(vb, 'vibrafono eco', ritardo=12, volume=40)
    b.ritornello(2, 18)
    return b.fine()
