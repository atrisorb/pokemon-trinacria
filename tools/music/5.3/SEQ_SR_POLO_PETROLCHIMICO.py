"""Dentro il polo petrolchimico: pontili, serbatoi, sala controllo e torcia."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from notazione import Brano, Giro  # noqa: E402

SIMBOLO = 'SEQ_SR_POLO_PETROLCHIMICO'
BANCO = 'BANK_BGM_DUNGEON6'
VOLUME = 64
SCHEDA = {
    'titolo': 'Il polo petrolchimico',
    'carattere': 'dentro gli impianti: ostinato di pizzicato e basso sintetico a crome come pompe e '
                 'valvole, colpi di tromboni, corni che salgono a fatica; nella parte B l\'accordo '
                 'napoletano (Re bemolle) ricorda che il polo lavora per «U Sistema»',
    'tonalita': 'Do minore',
    'forma': 'introduzione di 2 battute (pompe e basso); ritornello A (8) + B (8)',
    'perche_volume': 'HeartGold suona lo slot a 50 con 8 tracce; le 6 voci di questa '
                     'partitura a 50 resterebbero sotto le musiche vicine (Augusta 62, Siracusa 73)',
}

INTRO = Giro('Cm | Cm')
A_ = Giro('Cm | Cm | Ab | Ab | Fm | Fm | G | G')
B_ = Giro('Cm | Bb | Ab | G | Fm | Db | G7 | G7')

CORNI = (
    '| c5/2 eb5/4 g5/4 | g5/2. eb5/4 | ab5/2 c6/4 eb5/4 | c5/1 '
    '| f5/2 ab5/4 c6/4 | ab5/2. f5/4 | g5/2 b4/4 d5/4 | g4/1 '
    '| eb5/4 g5/4 c6/2 | d6/4. bb5/8 f5/2 | eb6/4. c6/8 ab5/2 | b5/2 g5/2 '
    '| ab5/4 c6/4 f6/2 | f6/4 db6/4 ab5/2 | g5/4 b5/4 d6/4 f6/4 | g6/2. r/4 |'
)


def partitura(A):
    b = Brano(A, bpm=132)
    co = b.voce('corni', 32, volume=110, pan=64)
    pz = b.voce('pompe', 17, volume=90, pan=36)
    bs = b.voce('basso', 21, volume=100, pan=64)
    tb = b.voce('tromboni', 30, volume=76, pan=92)
    tp = b.voce('timpani', 28, volume=90, pan=64)
    bt = b.voce('batteria', 39, volume=80, pan=64)
    co.suona(CORNI, da=2, vel=96)
    giro = INTRO + A_ + B_
    pz.arpeggi(giro, '1 1 5 1 8 1 5 1', da=0, registro=(36, 60), vel=82, gate=0.5)
    bs.basso(giro, '1 1 1 1 1 1 1 1', da=0, gate=0.5, vel=92)
    tb.accordi(A_ + B_, 'X...x...', da=2, registro=(48, 64), vel=66, gate=0.6)
    tp.basso(giro, '1 . . . . . . .', da=0, registro=(43, 55), vel=96, gate=0.5)
    bt.batteria({'cassa': 'x...x...', 'rullante': '....x...', 'hh': 'xxxxxxxx', 'legnetto': '..x...x.'},
                da=0, battute=18)
    b.ritornello(2, 18)
    return b.fine()
