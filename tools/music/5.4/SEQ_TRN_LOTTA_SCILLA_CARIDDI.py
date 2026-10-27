"""Lotta con Colapisci (Lugia) nei gorghi di Cariddi, sul fondo dello Stretto (P-08)."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from notazione import Brano, Giro  # noqa: E402

SIMBOLO = 'SEQ_TRN_LOTTA_SCILLA_CARIDDI'
BANCO = 'BANK_BGM_BATTLE8'
VOLUME = 102
SCHEDA = {
    'titolo': 'Colapisci nei gorghi',
    'carattere': 'il guardiano che regge l\'isola dal fondo dello Stretto: arpa e celesta girano a '
                 'semicrome come i gorghi di Cariddi, corni gravi col tema e archi all\'ottava sopra, '
                 'contrabbasso e timpani profondi; la parte B sale verso la luce in Re e Mi maggiore',
    'tonalita': 'Fa diesis minore',
    'forma': 'introduzione di 2 battute; ritornello A (8) + B (8)',
}

INTRO = Giro('F#m | C#7')
A_ = Giro('F#m | D | Bm | C# | F#m | D | E | C#')
B_ = Giro('D | E | C#m | F#m | Bm | E | D | C#7')

APERTURA = '| f#4/8 a4 c#5 f#5 a5/4 c#6 | e#5/4 g#5 b5 c#6 |'
MELODIA = (
    '| c#5/2 f#5/4 a5 | a5/4. f#5/8 d5/4 a5 | b5/2 d6/4 f#6 | e#6/2 c#6/4 g#5 '
    '| a5/4. g#5/8 f#5/4 c#6 | d6/4 f#6 a6 f#6 | g#6/4. f#6/8 e6/4 b5 | e#6/2 c#6/4 g#5 '
    '| f#5/4 a5 d6 f#6 | e6/4. d6/8 b5/4 g#5 | g#5/4 c#6 e6 g#6 | f#6/2 c#6/4 a5 '
    '| d6/4. c#6/8 b5/4 f#5 | g#5/4 b5 e6 g#6 | f#6/4. e6/8 d6/4 a5 | g#5/2 b5/4 e#5 |'
)


def partitura(A):
    b = Brano(A, bpm=152)
    co = b.voce('corni', 32, volume=116, pan=60)
    ar = b.voce('gorghi', 26, volume=80, pan=98)
    ce = b.voce('celesta', 27, volume=56, pan=24)
    cb = b.voce('contrabbasso', 25, volume=106, pan=64)
    tp = b.voce('timpani', 28, volume=100, pan=64)
    bt = b.voce('batteria', 39, volume=90, pan=64)
    co.suona(APERTURA, da=0, vel=102).suona(MELODIA, da=2, vel=102)
    b.eco(co, 'archi ottava', ritardo=0, volume=76, pan=36, trasponi=12, programma=23)
    giro = INTRO + A_ + B_
    ar.arpeggi(giro, '1 5 8 10 12 10 8 5 1 5 8 10 12 10 8 5', da=0, registro=(42, 72), vel=68, gate=0.6)
    ce.arpeggi(B_, '. . . . . . . . 15 12 10 8 . . . .', da=10, registro=(66, 90), vel=54, gate=0.6)
    cb.basso(giro, '1 . 1 . 5, . 1 .', da=0, registro=(28, 45), gate=0.7)
    tp.basso(giro, '1 . . . . . 5, .', da=0, registro=(40, 52), vel=102, gate=0.6)
    bt.batteria({'cassa': 'x.......x.......', 'rullante': 'x.x.x.x.xxxxxxxx'}, da=0, battute=2)
    bt.batteria({'cassa': 'x.....x.x.......', 'rullante': '....x.......x...', 'hh': 'x.x.x.x.x.x.x.x.'},
                da=2, battute=16)
    b.ritornello(2, 18)
    return b.fine()
