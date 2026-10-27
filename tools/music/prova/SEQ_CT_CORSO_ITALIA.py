"""Partitura DI PROVA della pipeline (blocco 5.1): non è il brano di Corso Italia.

Serve solo a provare componi.py e trinacria_audio.py su uno slot vero (SEQ_GS_T_WAKABA).
La partitura definitiva di SEQ_CT_CORSO_ITALIA la scrive il blocco 5.2 in tools/music/5.2/.
Tarantella in La minore, 6/8, otto battute ripetute, coi programmi comuni 0-59 dei banchi.
"""
SIMBOLO = 'SEQ_CT_CORSO_ITALIA'
BANCO = 'BANK_BGM_FIELD1'          # il banco dello slot HeartGold
VOLUME = 80

CROMA = 24                         # 48 tick per semiminima
BATTUTA = 6 * CROMA

MELODIA = [  # (tasto, crome)
    [(76, 1), (81, 1), (84, 1), (83, 1), (81, 1), (76, 1)],
    [(84, 1), (83, 1), (81, 1), (80, 1), (81, 1), (83, 1)],
    [(86, 1), (84, 1), (81, 1), (77, 1), (81, 1), (86, 1)],
    [(88, 1), (86, 1), (83, 1), (80, 1), (83, 1), (76, 1)],
    [(81, 1), (84, 1), (88, 1), (88, 1), (86, 1), (84, 1)],
    [(83, 1), (84, 1), (86, 1), (84, 1), (83, 1), (81, 1)],
    [(80, 1), (83, 1), (86, 1), (83, 1), (80, 1), (76, 1)],
    [(81, 3), (None, 1), (76, 1), (80, 1)],
]
ACCORDI = [(57, 60, 64), (57, 60, 64), (57, 62, 65), (56, 59, 62),
           (57, 60, 64), (57, 60, 64), (56, 59, 62), (57, 60, 64)]
BASSI = [45, 45, 38, 40, 45, 45, 40, 45]


def partitura(A):
    mw = A.MidiWriter(48)
    t0 = mw.track('tempo')
    mw.tempo(t0, 0, 168)
    mw.loop(t0, 0, 8 * BATTUTA)
    voci = {0: (35, 110, 64), 1: (23, 80, 50), 2: (22, 100, 64), 9: (39, 96, 72)}
    tr = {}
    for ch, (prg, vol, pan) in voci.items():
        tr[ch] = mw.track('canale %d' % ch)
        mw.program(tr[ch], 0, ch, prg)
        mw.cc(tr[ch], 0, ch, 7, vol)
        mw.cc(tr[ch], 0, ch, 10, pan)
    for b in range(8):
        t = b * BATTUTA
        for key, n in MELODIA[b]:
            if key is not None:
                mw.note(tr[0], t, 0, key, 100, n * CROMA - 4)
            t += n * CROMA
        t = b * BATTUTA
        for pos in (1, 2, 4, 5):
            for key in ACCORDI[b]:
                mw.note(tr[1], t + pos * CROMA, 1, key, 70, CROMA - 8)
        for pos in (0, 3):
            mw.note(tr[2], t + pos * CROMA, 2, BASSI[b], 100, 2 * CROMA)
            mw.note(tr[9], t + pos * CROMA, 9, 36, 110, CROMA)
        mw.note(tr[9], t + 3 * CROMA, 9, 38, 90, CROMA)
        for pos in range(6):
            mw.note(tr[9], t + pos * CROMA, 9, 42, 60 if pos % 3 else 80, CROMA // 2)
    return mw
