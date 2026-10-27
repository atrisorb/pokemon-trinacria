"""Marzamemi, Pachino, Portopalo e la tonnara."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from notazione import Brano, Giro  # noqa: E402

SIMBOLO = 'SEQ_SR_MARZAMEMI'
BANCO = 'BANK_BGM_FIELD15'
VOLUME = 73
SCHEDA = {
    'titolo': 'Marzamemi e la tonnara',
    'carattere': 'il borgo della tonnara e la punta più a sud dell\'isola: nella parte A una voce sola '
                 'chiama e il coro dei tonnaroti (corni e tromboni) risponde, alla maniera della '
                 'cialoma; chitarra arpeggiata e colpi di cassa come i remi; nella parte B la voce '
                 'canta distesa sopra la fisarmonica',
    'tonalita': 'La minore',
    'forma': 'introduzione di 2 battute (chitarra e remi); ritornello A (8: due domande e due risposte) + B (8)',
}

INTRO = Giro('Am | E')
A_ = Giro('Am | Am | Dm | E | Am | C | G E | Am')
B_ = Giro('F | C | G | Am | F | C | Dm E | E7')

CANTO_A = (
    '| e5/4. d5/8 c5/4 e5/4 | a5/2 e5/2 | r/1*2 '
    '| a5/4 c6/4 e6/4 c6/4 | g5/2 e5/4 c5/4 | r/1*2 |'
)
CORO_A = '| r/1*2 | d4/4 f4/4 a4/2 | g#4/4. b4/8 e4/2 | r/1*2 | d4/4 b3/4 g#3/4 b3/4 | a3/2. r/4 |'
CANTO_B = (
    '| c6/4 a5/4 f5/4 a5/4 | g5/2. e5/4 | d5/4 g5/4 b5/4 d6/4 | c6/2 a5/2 '
    '| a5/4 c6/4 f6/4 c6/4 | e6/2 c6/2 | d6/4 a5/4 b5/4 g#5/4 | e5/2. r/4 |'
)


def partitura(A):
    b = Brano(A, bpm=100)
    ca = b.voce('canto', 33, volume=108, pan=64)
    co = b.voce('coro', 32, volume=100, pan=48)
    ch = b.voce('chitarra', 7, volume=80, pan=88)
    fs = b.voce('fisarmonica', 13, volume=70, pan=40)
    cb = b.voce('contrabbasso', 25, volume=96, pan=64)
    rm = b.voce('remi', 39, volume=72, pan=64)
    ca.suona(CANTO_A, da=2, vel=98).suona(CANTO_B, da=10, vel=96)
    co.suona(CORO_A, da=2, vel=94)
    giro = INTRO + A_ + B_
    ch.arpeggi(giro, '1 5 8 5 10 5 8 5', da=0, registro=(52, 76), vel=72)
    fs.accordi(B_, 'x.x.x.x.', da=10, registro=(57, 72), vel=58, gate=0.7)
    cb.basso(giro, '1 - - - 5 - - -', da=0)
    rm.batteria({'cassa': 'x.......', 'tamburello': '..x...x.'}, da=0, battute=18)
    b.eco(co, 'coro grave', ritardo=0, programma=30, trasponi=-12, volume=80)
    b.ritornello(2, 18)
    return b.fine()
