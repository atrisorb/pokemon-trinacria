"""Corleone, il bosco di Ficuzza e le voliere dei pizzini alati, Villa Palagonia, l'ex
stabilimento di Termini Imerese."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from notazione import Brano, Giro  # noqa: E402

SIMBOLO = 'SEQ_PA_CORLEONE_FICUZZA'
BANCO = 'BANK_BGM_FIELD7'
VOLUME = 85
SCHEDA = {
    'titolo': 'Corleone e Ficuzza',
    'carattere': 'tensione di campagna: pizzicato d\'archi e contrabbasso che camminano piano, una '
                 'chitarra sola, una voce d\'ancia che si guarda alle spalle; nella parte B il Fa '
                 'accanto al Mi (modo frigio) e i timpani lontani come le ali dei corvi nella notte',
    'tonalita': 'Mi minore (parte B frigia)',
    'forma': 'introduzione di 2 battute (pizzicato e contrabbasso); ritornello A (8) + B (8)',
}

INTRO = Giro('Em | B7')
A_ = Giro('Em | Em | C | B7 | Em | Em | Am | B7')
B_ = Giro('F | Em | F | Em | Am | Em | C | B7')

MELODIA = (
    '| e5/2. g5/4 | b5/2 r/4 g5 | e5/4. g5/8 c6/4 g5 | f#5/2 d#5/4 a5 '
    '| g5/4. f#5/8 e5/4 b4 | e5/2. r/4 | c6/4. b5/8 a5/4 e5 | d#5/2 f#5/4 b4 '
    '| f5/2 a5/4 c6 | b5/2. r/4 | a5/4. g5/8 f5/4 c5 | e5/2. r/4 '
    '| a5/4 c6 e6 c6 | b5/4. a5/8 g5/4 e5 | e5/4 g5 c6 e6 | d#6/2 b5/4 f#5 |'
)


def partitura(A):
    b = Brano(A, bpm=96)
    ob = b.voce('canto', 33, volume=104, pan=60)
    pz = b.voce('pizzicato', 17, volume=86, pan=94)
    ch = b.voce('chitarra', 7, volume=70, pan=30)
    cb = b.voce('contrabbasso', 25, volume=100, pan=64)
    tp = b.voce('timpani', 28, volume=88, pan=64)
    bt = b.voce('batteria', 39, volume=58, pan=64)
    ob.suona(MELODIA, da=2, vel=94)
    giro = INTRO + A_ + B_
    pz.accordi(giro, 'x.x.x.x.', da=0, registro=(52, 64), vel=70, voci=2, gate=0.5)
    ch.arpeggi(A_ + B_, '1 5 8 . 10 . 8 .', da=2, registro=(52, 76), vel=62)
    cb.basso(giro, '1 . . . 5, . . .', da=0, registro=(28, 47))
    tp.basso(B_, '1 . . . . . 1 .', da=10, registro=(40, 52), vel=86, gate=0.5)
    bt.batteria({'tom_b': 'x.......', 'bordo': '....x...'}, da=2, battute=16)
    b.ritornello(2, 18)
    return b.fine()
