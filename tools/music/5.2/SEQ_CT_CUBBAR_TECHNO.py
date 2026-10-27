"""La techno del Cubbar (Prologo, M-CT-00: la notte al Cubbar alle 3:30) e del Privè Zagara."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from notazione import Brano, Giro  # noqa: E402

SIMBOLO = 'SEQ_CT_CUBBAR_TECHNO'
BANCO = 'BANK_BGM_FIELD5'
VOLUME = 80
SCHEDA = {
    'titolo': 'Cubbar techno',
    'carattere': 'discoteca alle 3:30 di notte, il Prologo: cassa dritta, basso in levare, arpeggio a onda '
                 'quadra (PSG) che gira sempre, accordi «stab»; nella seconda metà entra il riff acuto. '
                 'Serve anche al Privè Zagara (M-CT-04)',
    'tonalita': 'La minore',
    'forma': 'introduzione di 2 battute (cassa e charleston); ritornello di 16 battute: '
             '8 di arpeggio e accordi, 8 col riff',
}

GIRO = Giro('Am | Am | F | G') * 2 + Giro('Dm | Am | F | E') * 2

RIFF = (
    '| d6/8 a5 f5 a5 d6 a5 f5 e5 | e6/8 c6 a5 c6 e6 c6 a5 g#5 '
    '| f5/8 a5 c6 a5 f6 c6 a5 c6 | g#5/8 b5 e6 b5 g#5/4 e5 |'
)


def partitura(A):
    b = Brano(A, bpm=128)
    ld = b.voce('riff', 9, volume=96, pan=64)
    ar = b.voce('arpeggio PSG', 48, volume=70, pan=40)
    st = b.voce('stab', 29, volume=78, pan=96)
    bs = b.voce('basso', 21, volume=116, pan=64)
    bt = b.voce('batteria', 39, volume=100, pan=64)
    ld.suona(RIFF, da=10, vel=96).suona(RIFF, da=14)
    ar.arpeggi(GIRO, '1 5 8 5 10 8 5 8 1 5 8 5 12 10 8 5', da=2, registro=(57, 84), vel=70, gate=0.6)
    st.accordi(GIRO, '..x...x...x...x.', da=2, registro=(57, 72), vel=66, gate=0.4)
    bs.basso(GIRO, '. 1 . 1 . 1 . 8', da=2, registro=(33, 50), gate=0.6)
    cassa = {'cassa': 'X...x...x...x...', 'hha': '..x...x...x...x.'}
    bt.batteria(cassa, da=0, battute=2)
    bt.batteria(dict(cassa, battimani='....x.......x...', hh='o.o.o.o.o.o.o.o.'), da=2, battute=16)
    b.ritornello(2, 18)
    return b.fine()
