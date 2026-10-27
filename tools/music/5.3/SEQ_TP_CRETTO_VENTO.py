"""Il vento dei luoghi della memoria: Grande Cretto di Burri, Gibellina, Presidio Civico di
Castelvetrano, Porta d'Europa (M-TP-02: nessuna musica allegra, solo il vento)."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from notazione import Brano  # noqa: E402

SIMBOLO = 'SEQ_TP_CRETTO_VENTO'
BANCO = 'BANK_BGM_DUNGEON1'
VOLUME = 87
SCHEDA = {
    'titolo': 'Il vento del Cretto',
    'carattere': 'nessuna musica, come chiede la trama: solo il vento sul cemento bianco, scritto '
                 'col canale di rumore (programma 53); le raffiche salgono e calano con '
                 'l\'espressione (CC11) e cambiano colore con l\'altezza della nota, con lunghi tratti '
                 'quasi in silenzio',
    'tonalita': 'nessuna (rumore)',
    'forma': 'ritornello di 16 battute di raffiche e pause, dalla prima battuta',
}

# (battuta, nota, durata in battute): nota più acuta = vento più sottile e fischiante
RAFFICHE = [(0, 'c4', 2), (2, 'g4', 1), (3, 'eb4', 2), (5, 'c5', 1), (6, 'a4', 2),
            (8, 'd4', 3), (11, 'f4', 1), (12, 'bb4', 2), (14, 'e4', 2)]
# (battuta, espressione): fra un punto e l'altro l'espressione cambia a quarti di battuta
ESPRESSIONE = [(0, 20), (1, 70), (2, 96), (2.5, 50), (3, 40), (4, 84), (5, 110), (5.75, 40),
               (6, 30), (7, 64), (8, 24), (9.5, 76), (11, 100), (11.5, 30), (12, 46), (13, 90),
               (14, 36), (15, 60), (16, 20)]


def partitura(A):
    b = Brano(A, bpm=60)
    v = b.voce('vento', 53, volume=100, pan=64, pedale=True)
    for t, nota, dur in RAFFICHE:
        v.suona('%s/1*%d_' % (nota, dur), da=t, vel=90)
    for (t0, e0), (t1, e1) in zip(ESPRESSIONE, ESPRESSIONE[1:]):
        passi = max(1, int((t1 - t0) * 4))
        for i in range(passi):
            v.cc(11, round(e0 + (e1 - e0) * i / passi), t0 + (t1 - t0) * i / passi)
    b.ritornello(0, 16)
    return b.fine()
