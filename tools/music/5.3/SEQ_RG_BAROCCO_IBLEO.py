"""Il barocco ibleo: Ragusa, Ibla, Modica, Scicli, Ispica, Comiso."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from notazione import Brano, Giro  # noqa: E402

SIMBOLO = 'SEQ_RG_BAROCCO_IBLEO'
BANCO = 'BANK_BGM_FIELD16'
VOLUME = 64
SCHEDA = {
    'titolo': 'Il barocco ibleo',
    'carattere': 'le città di pietra chiara sui canyon degli Iblei, la provincia di Maria: una '
                 '«siciliana», la danza barocca in 6/8 col ritmo puntato, per oboe sopra arpa, archi '
                 'lenti e violoncello; intima e un po\' nostalgica',
    'tonalita': 'Sol minore (seconda passata in Re minore)',
    'forma': 'introduzione di 2 battute (arpa); ritornello A (8) + B (8) in Sol minore, poi le stesse 16 battute in Re minore, in 6/8',
    'perche_volume': 'HeartGold suona lo slot a 59 con 11 tracce (lo stesso file di '
                     '`SEQ_GS_C_TOKIWA` e `SEQ_GS_C_YAMABUKI`); le 5 voci di questa partitura a 59 resterebbero sotto le musiche vicine '
                     '(costa iblea 75)',
}

INTRO = Giro('Gm | D7')
A_ = Giro('Gm | Cm | D7 | Gm | Eb | Cm | D7 | Gm')
B_ = Giro('Bb | F | Gm | D | Eb | Cm | Am7b5 D7 | D7')

MELODIA = (
    '| d5/8. eb5/16 d5/8 g5/4. | g5/8. ab5/16 g5/8 eb5/4. | f#5/8. g5/16 a5/8 c6/4 a5/8 | bb5/4. g5/4. '
    '| g5/8. ab5/16 bb5/8 eb6/4 bb5/8 | c6/8. bb5/16 ab5/8 g5/4 eb5/8 | d5/8. eb5/16 f#5/8 a5/4 c6/8 | g5/4. r/4. '
    '| d6/8. eb6/16 d6/8 bb5/4. | c6/8. d6/16 c6/8 a5/4. | bb5/8. c6/16 bb5/8 g5/4 d5/8 | f#5/4. a5/4. '
    '| bb5/8. c6/16 bb5/8 g5/4 eb5/8 | eb6/8. d6/16 c6/8 g5/4. | c6/8. bb5/16 a5/8 f#5/4 a5/8 | d5/4. r/4. |'
)


def partitura(A):
    b = Brano(A, bpm=108, metro=(6, 8))
    ob = b.voce('oboe', 33, volume=108, pan=64)
    ap = b.voce('arpa', 26, volume=88, pan=40)
    ar = b.voce('archi', 24, volume=72, pan=88)
    vc = b.voce('violoncello', 25, volume=92, pan=64)
    ob.suona(MELODIA, da=2, vel=96)
    giro = INTRO + A_ + B_
    ap.arpeggi(giro, '1 5 8 10 8 5', da=0, registro=(43, 67), vel=74)
    ar.accordi(A_ + B_, 'x-----', da=2, registro=(55, 70), vel=58)
    vc.basso(giro, '1 - - 5 - -', da=0)
    b.ripeti(2, 16, 18, trasponi=-5)
    b.eco(ob, 'oboe eco', ritardo=12, volume=36)
    b.ritornello(2, 34)
    return b.fine()
