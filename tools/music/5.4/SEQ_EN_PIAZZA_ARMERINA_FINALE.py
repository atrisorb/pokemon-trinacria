"""Il finale: la marcia sotto il temporale a Piazza Armerina, le gallerie della Villa Romana del
Casale e la Sala della Grande Caccia dove aspetta l'On. Mistretta (M-EN-05, M-EN-06)."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from notazione import Brano, Giro  # noqa: E402

SIMBOLO = 'SEQ_EN_PIAZZA_ARMERINA_FINALE'
BANCO = 'BANK_BGM_FIELD4'
VOLUME = 69
SCHEDA = {
    'titolo': 'Sotto il temporale a Piazza Armerina',
    'carattere': 'la marcia verso Mistretta sotto la pioggia battente: archi in tremolo a semicrome, '
                 'corni che salgono, tromboni e tuba gravi, i timpani come tuoni e la pioggia sul '
                 'charleston; il Sol bemolle napoletano (R-AUD-21) chiude le frasi: la casa di «U '
                 'Sistema» è vicina',
    'tonalita': 'Fa minore',
    'forma': 'introduzione di 2 battute (tremolo e tuono); ritornello A (8) + B (8)',
}

INTRO = Giro('Fm | C')
A_ = Giro('Fm | Fm | Db | C | Fm | Fm | Gb | C')
B_ = Giro('Bbm | Fm | Bbm | C | Db | Ab | Gb | C7')

MELODIA = (
    '| f5/2 ab5/4 c6 | c6/4. bb5/8 ab5/4 f5 | f5/4 ab5 db6 f6 | e6/2 c6/4 g5 '
    '| ab5/4. g5/8 f5/4 c5 | f5/4 ab5 c6 f6 | gb6/2 db6/4 bb5 | c6/2. r/4 '
    '| bb5/2 db6/4 f6 | f6/4. eb6/8 c6/4 ab5 | db6/4 bb5 f5 bb5 | c6/2 e5/4 g5 '
    '| ab5/4. bb5/8 db6/4 f6 | eb6/4. db6/8 c6/4 ab5 | bb5/4 db6 gb6 db6 | e6/2 bb5/4 g5 |'
)


def partitura(A):
    b = Brano(A, bpm=132)
    co = b.voce('corni', 32, volume=110, pan=60)
    tr = b.voce('tremolo', 23, volume=80, pan=96)
    tb = b.voce('tromboni', 30, volume=90, pan=30)
    tu = b.voce('tuba', 25, volume=100, pan=64)
    tp = b.voce('tuono', 28, volume=104, pan=64)
    bt = b.voce('pioggia', 39, volume=62, pan=64)
    co.suona(MELODIA, da=2, vel=100)
    b.eco(co, 'archi ottava', ritardo=0, volume=70, pan=20, trasponi=12, programma=23)
    giro = INTRO + A_ + B_
    tr.arpeggi(giro, '1 5 1 5 1 5 1 5 1 5 1 5 1 5 1 5', da=0, registro=(53, 72), vel=58, gate=0.5)
    tb.accordi(A_ + B_, 'x...x...', da=2, registro=(48, 62), vel=76, voci=2, gate=0.6)
    tu.basso(giro, '1 . 1 . 5, . 1 .', da=0, registro=(29, 46), gate=0.7)
    tp.basso(giro, '1 . . . . . . .', da=0, registro=(41, 53), vel=110, gate=0.9)
    bt.batteria({'hh': 'o.o.o.o.o.o.o.o.', 'tom_b': 'x.....x.........'}, da=0, battute=2)
    bt.batteria({'hh': 'o.o.o.o.o.o.o.o.', 'cassa': 'x.......x.......', 'rullante': '....x..x....x...'},
                da=2, battute=16)
    b.ritornello(2, 18)
    return b.fine()
