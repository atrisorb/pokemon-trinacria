"""Chiese e cattedrali: la Cattedrale di Sant'Agata, il Santuario di Tindari, il Duomo di Monreale."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from notazione import Brano, Giro  # noqa: E402

SIMBOLO = 'SEQ_TRN_CHIESA'
BANCO = 'BANK_BGM_DUNGEON3'
VOLUME = 80
SCHEDA = {
    'titolo': 'Chiesa',
    'carattere': 'navate di pietra e incenso: corale a quattro voci d\'organo a note lunghe, una voce '
                 'd\'ancia che canta sopra, rintocchi di campana (il programma 67 del banco, lo stesso '
                 'che HeartGold suona nella Torre Campana); nessuna percussione ritmica',
    'tonalita': 'Fa maggiore',
    'forma': 'ritornello A (8) + B (8) dalla prima battuta',
}

A_ = Giro('F | Dm | Bb | C | Am | Dm | Gm C | F')
B_ = Giro('Bb | F | Gm | Dm | Bb | F/A | Gm7 C7 | F')

CANTO = (
    '| a5/2 c6 | d6/2 a5 | bb5/2 d6 | c6/1 | c6/2 e6 | d6/2 f6 | d6/2 c6 | a5/1 '
    '| bb5/2 f5 | a5/2 c6 | bb5/2 g5 | a5/1 | d6/2 bb5 | c6/2 a5 | bb5/2 e5 | f5/1 |'
)


def partitura(A):
    b = Brano(A, bpm=72)
    ca = b.voce('canto', 33, volume=100, pan=64)
    og = b.voce('organo', 12, volume=96, pan=64)
    vc = b.voce('contrabbasso', 25, volume=96, pan=64)
    cm = b.voce('campana', 67, volume=84, pan=30)
    ca.suona(CANTO, da=0, vel=88, gate=0.96)
    giro = A_ + B_
    og.accordi(giro, 'x-x-', da=0, registro=(53, 70), vel=74, voci=4, gate=0.97)
    vc.basso(giro, '1 1', da=0, registro=(29, 48), gate=0.95)
    for n in (0, 7, 15):                          # solo sugli accordi di Fa
        cm.suona('| c4/1 |', da=n, vel=100)
    b.ritornello(0, 16)
    return b.fine()
