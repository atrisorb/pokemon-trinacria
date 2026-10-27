"""Grotte, cave e sotterranei: sotterranei del Castello Ursino, Latomie, Ipogei, Scala dei Turchi..."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from notazione import Brano, Giro  # noqa: E402

SIMBOLO = 'SEQ_TRN_GROTTA'
BANCO = 'BANK_BGM_DUNGEON1'
VOLUME = 80
SCHEDA = {
    'titolo': 'Grotta',
    'carattere': 'buio, umidità e roccia lavica: pizzicato grave che cammina, clarinetto basso a note '
                 'lunghe, contrabbasso; gocce d\'acqua di celesta che cadono fuori tempo',
    'tonalita': 'Mi minore',
    'forma': 'ritornello A (8) + B (8) dalla prima battuta',
}

A_ = Giro('Em | C | Am | B | Em | C | Am B7 | Em')
B_ = Giro('Am | Em | Am | B7 | C | Am | F#m7b5 | B7')

MELODIA = (
    '| e4/2 g4/4 b4 | c5/2. g4/4 | a4/4. c5/8 e5/2 | d#5/2 b4 '
    '| e5/4. d5/8 b4/4 g4 | g4/2 e4/4 c4 | a4/2 f#4/4 d#4 | e4/1 '
    '| c5/2 a4/4 e4 | b4/2 g4/4 e4 | a4/4. b4/8 c5/2 | b4/2 a4 '
    '| g4/2 e4 | e4/2 c4/4 a3 | a4/2 c5/4 e4 | d#4/2 f#4 |'
)
GOCCE = '| r/4 b6/16 r/16 r/8 r/2 | r/2. e7/16 r/16 r/8 | r/8 g6/16 r/16 r/4 r/2 | r/1 |'


def partitura(A):
    b = Brano(A, bpm=96)
    cl = b.voce('clarinetto', 34, volume=108, pan=64)
    pz = b.voce('pizzicato', 17, volume=96, pan=36)
    vc = b.voce('contrabbasso', 25, volume=96, pan=64)
    gc = b.voce('gocce', 27, volume=70, pan=100)
    cl.suona(MELODIA, da=0, vel=92, gate=0.95)
    for n in range(0, 16, 4):
        gc.suona(GOCCE, da=n, vel=80)
    giro = A_ + B_
    pz.arpeggi(giro, '1 5 8 5 1 5 8 5', da=0, registro=(40, 64), vel=80, gate=0.5)
    vc.basso(giro, '1 - - - - - - -', da=0, registro=(28, 45), gate=0.95)
    b.ritornello(0, 16)
    return b.fine()
