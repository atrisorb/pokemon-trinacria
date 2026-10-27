"""Dopo la lotta con Maria sul tetto del tribunale (P-02): solo il vento, nessuna fanfara."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from notazione import Brano  # noqa: E402

SIMBOLO = 'SEQ_TRN_VITTORIA_MARIA_VENTO'
BANCO = 'BANK_BASIC'
VOLUME = 72
SCHEDA = {
    'titolo': 'Il vento sul tetto',
    'carattere': 'nessuna fanfara: l\'alba sul tetto del Palazzo di Giustizia, la cenere dell\'Etna e '
                 'il vento, scritto col canale di rumore (programma 53) come il Cretto e Capaci; una '
                 'raffica lunga che sale e cala, più breve e più calma di quelle dei luoghi della memoria',
    'tonalita': 'nessuna (rumore)',
    'forma': 'ritornello di 8 battute di vento, dalla prima battuta',
}

RAFFICHE = [(0, 'd4', 3), (3, 'f4', 2), (5, 'c4', 3)]
ESPRESSIONE = [(0, 24), (1, 64), (2, 80), (3, 36), (4, 70), (5, 30), (6, 58), (7, 40), (8, 24)]


def partitura(A):
    b = Brano(A, bpm=60)
    v = b.voce('vento', 53, volume=96, pan=64, pedale=True)
    for t, nota, dur in RAFFICHE:
        v.suona('%s/1*%d_' % (nota, dur), da=t, vel=84)
    for (t0, e0), (t1, e1) in zip(ESPRESSIONE, ESPRESSIONE[1:]):
        passi = max(1, int((t1 - t0) * 4))
        for i in range(passi):
            v.cc(11, round(e0 + (e1 - e0) * i / passi), t0 + (t1 - t0) * i / passi)
    b.ritornello(0, 8)
    return b.fine()
