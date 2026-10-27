"""I luoghi della memoria: le steli di Capaci, Casa Memoria a Cinisi, Portella della Ginestra,
il CIDMA di Corleone (M-PA-02: solo vento e auto sull'asfalto, nessuna musica)."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from notazione import Brano  # noqa: E402

SIMBOLO = 'SEQ_PA_CAPACI_MEMORIA'
BANCO = 'BANK_BGM_FIELD1'
VOLUME = 105
SCHEDA = {
    'titolo': 'Il vento di Capaci',
    'carattere': 'nessuna musica, come chiede la trama: il vento sul tratto dell\'A29 con le steli, '
                 'scritto col canale di rumore (programma 53) come quello del Cretto; fra una raffica '
                 'e l\'altra passa un\'auto, una nota di rumore più acuta che sale e si spegne in un '
                 'movimento, poi il vento riprende',
    'tonalita': 'nessuna (rumore)',
    'forma': 'ritornello di 16 battute di vento con quattro auto che passano, dalla prima battuta',
}

# (battuta, nota, durata in quarti, cosa): le note si toccano senza sovrapporsi (un solo canale
# di rumore, A07). Vento grave e lungo; auto acute e brevi.
EVENTI = [(0, 'c4', 8, 'vento'), (2, 'a5', 2, 'auto'), (2.5, 'eb4', 10, 'vento'),
          (5, 'g4', 4, 'vento'), (6, 'g5', 2, 'auto'), (6.5, 'd4', 14, 'vento'),
          (10, 'b5', 2, 'auto'), (10.5, 'f4', 6, 'vento'), (12, 'bb4', 8, 'vento'),
          (14, 'a5', 2, 'auto'), (14.5, 'e4', 6, 'vento')]
# (battuta, espressione): raffiche lente; ogni auto sale di colpo e cala in un movimento
ESPRESSIONE = [(0, 18), (1, 60), (2, 24), (2.25, 112), (2.5, 30), (3.5, 80), (4.5, 40), (5, 56),
               (6, 26), (6.25, 100), (6.5, 22), (8, 70), (9, 90), (10, 20), (10.25, 118), (10.5, 34),
               (11.5, 66), (12, 30), (13, 84), (14, 24), (14.25, 104), (14.5, 28), (15.5, 58), (16, 18)]


def partitura(A):
    b = Brano(A, bpm=60)
    v = b.voce('vento e auto', 53, volume=100, pan=64, pedale=True)
    for t, nota, quarti, cosa in EVENTI:
        v.suona('%s/4*%d_' % (nota, quarti), da=t, vel=90 if cosa == 'vento' else 100)
    for (t0, e0), (t1, e1) in zip(ESPRESSIONE, ESPRESSIONE[1:]):
        passi = max(1, int((t1 - t0) * 4))
        for i in range(passi):
            v.cc(11, round(e0 + (e1 - e0) * i / passi), t0 + (t1 - t0) * i / passi)
    b.ritornello(0, 16)
    return b.fine()
