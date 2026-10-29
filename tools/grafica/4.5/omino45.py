"""Blocco 4.5 — il «manichino» che disegna un personaggio di campo in un fotogramma 32×32 (R-GFX-17).

Un personaggio è una scheda (dizionario: colori, capelli, vestiti, accessori, corporatura); una posa è
(direzione, posa, fase). `disegna(scheda, posa)` restituisce 1024 indici di palette 0–15 (riga per riga,
riga 0 in alto). Niente è copiato dagli sprite di HeartGold: le misure (testa di 14×13 pixel, corpo di 12
righe, piedi alla riga 29, contorno scuro) seguono solo l'ingombro degli originali, che il gioco si aspetta.

Ruoli della palette (uguali per tutti gli sprite del blocco):
 0 trasparente · 1 contorno · 2/3 pelle e ombra · 4/5 capelli e ombra · 6/7 sopra e ombra
 8/9 sotto e ombra · 10 scarpe · 11 bianco · 12 accento A · 13 accento B · 14 accento C · 15 occhi
Direzioni: 'su' (di spalle), 'giu' (di fronte), 'sx' (verso sinistra), 'dx' (specchio di 'sx').
Solo libreria standard."""

W = H = 32
RUOLI = {'T': 0, 'O': 1, 'SK': 2, 'SKs': 3, 'HA': 4, 'HAs': 5, 'TO': 6, 'TOs': 7, 'BO': 8, 'BOs': 9,
         'SH': 10, 'WH': 11, 'A1': 12, 'A2': 13, 'A3': 14, 'EY': 15}
OMBRA = {'SK': 'SKs', 'HA': 'HAs', 'TO': 'TOs', 'BO': 'BOs'}
PIEDE = 28          # prima riga delle scarpe del piede appoggiato (scarpe 28–29, contorno fino a 30)


class Tela:
    def __init__(self):
        self.m = [['T'] * W for _ in range(H)]

    def p(self, x, y, r):
        if 0 <= x < W and 0 <= y < H:
            self.m[y][x] = r

    def g(self, x, y):
        return self.m[y][x] if 0 <= x < W and 0 <= y < H else 'T'

    def rett(self, x0, y0, x1, y1, r):
        """Rettangolo pieno con gli estremi inclusi."""
        for y in range(min(y0, y1), max(y0, y1) + 1):
            for x in range(min(x0, x1), max(x0, x1) + 1):
                self.p(x, y, r)

    def righe(self, y0, spans, r, dx=0):
        """spans = [(x0, x1), ...] una per riga a partire da y0."""
        for k, (a, b) in enumerate(spans):
            if a is not None:
                for x in range(a, b + 1):
                    self.p(x + dx, y0 + k, r)

    def specchio(self):
        for row in self.m:
            row.reverse()

    def ombreggia(self, solo_destra=False):
        """Luce da sinistra in alto: l'ultimo pixel a destra (e in basso) di ogni zona prende l'ombra."""
        nuova = [row[:] for row in self.m]
        for y in range(H):
            for x in range(W):
                r = self.m[y][x]
                if r not in OMBRA:
                    continue
                destra = self.g(x + 1, y) not in (r, OMBRA[r])
                sotto = self.g(x, y + 1) not in (r, OMBRA[r]) and r != 'SK' and not solo_destra
                if destra or sotto:
                    nuova[y][x] = OMBRA[r]
        self.m = nuova

    def contorna(self):
        """Ogni pixel vuoto accanto (4 vicini) a un pixel pieno diventa contorno."""
        nuova = [row[:] for row in self.m]
        for y in range(H):
            for x in range(W):
                if self.m[y][x] == 'T' and any(self.g(x + a, y + b) not in ('T', 'O')
                                               for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                    nuova[y][x] = 'O'
        self.m = nuova

    def indici(self):
        return [RUOLI[self.m[y][x]] for y in range(H) for x in range(W)]


# ------------------------------------------------------------------------------------------ la testa

TESTA = [(11, 20), (10, 21)] + [(9, 22)] * 9 + [(10, 21), (11, 20)]   # 13 righe, dalla riga 5


def testa(t, s, d, dy, dx=0):
    y0 = 5 + dy
    grande = s.get('testa_grande', 0)
    spans = [(a - grande, b + grande) for a, b in TESTA]
    t.righe(y0, spans, 'SK', dx)
    capelli(t, s, d, y0, dx)
    if d == 'giu':
        faccia_fronte(t, s, y0, dx)
    elif d == 'sx':
        faccia_lato(t, s, y0, dx)


def _cap(t, x, y, s):
    t.p(x, y, 'HA')


def capelli(t, s, d, y0, dx):
    """Capelli sulla testa (y0 = prima riga della testa). Gli stili sono maschere per direzione."""
    st = s.get('capelli', 'corti')
    x0 = 9 + dx

    def riga(r, a, b):
        for x in range(a, b + 1):
            t.p(x0 + x, y0 + r, 'HA')
    if st == 'nessuno':
        return
    calvo = st in ('calvo', 'riporto')
    if d == 'su':
        if calvo:
            for r in range(6, 12):
                riga(r, 0, 13)
            if st == 'riporto':
                riga(2, 3, 10)
            return
        for r in range(0, 13):
            a, b = TESTA[r][0] - 9, TESTA[r][1] - 9
            riga(r, a, b)
        if st in ('lunghi', 'caschetto', 'coda', 'cotonati', 'raccolti'):
            pass
        return
    if d == 'giu':
        if calvo:
            riga(5, 0, 1); riga(6, 0, 1); riga(7, 0, 1); riga(5, 12, 13); riga(6, 12, 13); riga(7, 12, 13)
            if st == 'riporto':
                riga(1, 3, 10)
            return
        if st == 'rasati':
            riga(0, 2, 11); riga(1, 1, 12); riga(2, 0, 13)
            riga(3, 0, 1); riga(3, 12, 13)
            return
        riga(0, 2, 11); riga(1, 1, 12); riga(2, 0, 13); riga(3, 0, 13)
        if st in ('corti', 'ciuffo', 'ricci', 'pettinati', 'coda', 'raccolti'):
            riga(4, 0, 4); riga(4, 9, 13)
            if st == 'pettinati':
                riga(4, 0, 6); riga(5, 0, 2)          # riga di lato
            for r in range(5, 8):
                riga(r, 0, 0); riga(r, 13, 13)
            if st == 'coda':
                for r in range(5, 10):
                    riga(r, 0, 1); riga(r, 12, 13)
            if st == 'ricci':
                for r in range(4, 9):
                    riga(r, 0, 1); riga(r, 12, 13)
            if st == 'ciuffo':
                riga(-1, 4, 10); riga(4, 5, 8)
        elif st in ('lunghi', 'caschetto', 'cotonati'):
            riga(4, 0, 3); riga(4, 10, 13)
            fine = 12 if st != 'caschetto' else 10
            for r in range(5, fine + 1):
                riga(r, 0, 1); riga(r, 12, 13)
            if st == 'cotonati':
                riga(-1, 3, 10)
                for r in range(1, 9):
                    t.p(x0 - 1, y0 + r, 'HA'); t.p(x0 + 14, y0 + r, 'HA')
        return
    # profilo verso sinistra: faccia a sinistra (colonne 0–7), nuca a destra
    if calvo:
        for r in range(5, 11):
            riga(r, 9, 13)
        if st == 'riporto':
            riga(1, 4, 12)
        return
    riga(0, 2, 11); riga(1, 1, 12); riga(2, 0, 13); riga(3, 2, 13)
    riga(4, 6, 13)
    for r in range(5, 10):
        riga(r, 8, 13)
    riga(10, 9, 13)
    if st == 'rasati':
        t.righe(y0 + 3, [(x0 + 2, x0 + 5)], 'SK')
        for r in range(6, 11):
            riga(r, 10, 13)
        return
    if st == 'ciuffo':
        riga(-1, 1, 8); riga(3, 0, 1)
    if st == 'pettinati':
        riga(3, 0, 13)
    if st in ('lunghi', 'caschetto', 'cotonati'):
        riga(3, 0, 13); riga(4, 0, 1)
        for r in range(10, 13):
            riga(r, 7, 13)
        if st == 'cotonati':
            riga(-1, 2, 11)


def faccia_fronte(t, s, y0, dx):
    x0 = 9 + dx
    ey = y0 + 7
    occhi = s.get('occhi', 'normali')
    for x in (3, 4, 9, 10):
        if occhi == 'chiusi':
            t.p(x0 + x, ey + 1, 'EY')
        else:
            t.p(x0 + x, ey, 'EY')
            t.p(x0 + x, ey + 1, 'EY')
    if occhi != 'chiusi':
        t.p(x0 + 3, ey, 'WH'); t.p(x0 + 10, ey, 'WH')
    if s.get('sopracciglia'):
        for x in (3, 4, 9, 10):
            t.p(x0 + x, ey - 1, 'HAs')
    acc = s.get('accessori', ())
    if 'occhiali_sole' in acc:
        t.righe(ey, [(x0 + 2, x0 + 11), (x0 + 2, x0 + 5)], 'EY')
        t.righe(ey + 1, [(x0 + 8, x0 + 11)], 'EY')
        t.p(x0 + 3, ey, 'A3'); t.p(x0 + 9, ey, 'A3')
    elif 'occhiali' in acc:
        for x in (2, 5, 8, 11):
            t.p(x0 + x, ey, 'A2'); t.p(x0 + x, ey + 1, 'A2')
        t.righe(ey - 1, [(x0 + 2, x0 + 11)], 'A2')
    if 'baffi' in acc:
        t.righe(ey + 3, [(x0 + 4, x0 + 9)], 'HAs')
    if 'barba' in acc:
        t.righe(ey + 2, [(x0 + 1, x0 + 2), (x0 + 1, x0 + 12)], 'HAs')
        t.righe(ey + 2, [(x0 + 11, x0 + 12)], 'HAs')
        t.righe(ey + 3, [(x0 + 2, x0 + 3), (x0 + 3, x0 + 10)], 'HAs')
        t.righe(ey + 3, [(x0 + 10, x0 + 11)], 'HAs')
        t.p(x0 + 5, ey + 3, 'SK'); t.p(x0 + 8, ey + 3, 'SK')
    if 'guance' in acc:
        t.p(x0 + 2, ey + 2, 'A1'); t.p(x0 + 11, ey + 2, 'A1')
    if 'rossetto' in acc:
        t.p(x0 + 6, ey + 3, 'A1'); t.p(x0 + 7, ey + 3, 'A1')


def faccia_lato(t, s, y0, dx):
    x0 = 9 + dx
    ey = y0 + 7
    occhi = s.get('occhi', 'normali')
    if occhi == 'chiusi':
        t.p(x0 + 2, ey + 1, 'EY'); t.p(x0 + 3, ey + 1, 'EY')
    else:
        t.p(x0 + 2, ey, 'EY'); t.p(x0 + 2, ey + 1, 'EY'); t.p(x0 + 3, ey, 'WH')
    t.p(x0 - 1, ey + 1, 'SK')                      # naso
    acc = s.get('accessori', ())
    if 'occhiali_sole' in acc:
        t.righe(ey, [(x0 + 0, x0 + 4), (x0 + 1, x0 + 3)], 'EY')
        t.righe(ey, [(x0 + 5, x0 + 8)], 'A2')
    elif 'occhiali' in acc:
        t.righe(ey - 1, [(x0 + 1, x0 + 8)], 'A2')
        t.p(x0 + 1, ey, 'A2'); t.p(x0 + 4, ey, 'A2'); t.p(x0 + 1, ey + 1, 'A2'); t.p(x0 + 4, ey + 1, 'A2')
    if 'baffi' in acc:
        t.righe(ey + 3, [(x0 + 0, x0 + 3)], 'HAs')
    if 'barba' in acc:
        t.righe(ey + 2, [(x0 + 3, x0 + 8), (x0 + 0, x0 + 8), (x0 + 1, x0 + 6)], 'HAs')
    if 'rossetto' in acc:
        t.p(x0 + 0, ey + 3, 'A1')
    if 'guance' in acc:
        t.p(x0 + 4, ey + 2, 'A1')


def copricapo(t, s, d, dy, dx=0):
    """Cappelli e cuffie sopra i capelli."""
    acc = s.get('accessori', ())
    y0 = 5 + dy
    x0 = 9 + dx
    if 'coppola' in acc or 'berretto' in acc or 'berretto_rovescio' in acc or 'casco' in acc \
            or 'capitano' in acc or 'berretto_lana' in acc:
        col = 'A2'
        t.righe(y0 - 1, [(x0 + 2, x0 + 11), (x0 + 1, x0 + 12), (x0, x0 + 13), (x0, x0 + 13)], col)
        if 'casco' in acc:
            t.righe(y0 - 2, [(x0 + 4, x0 + 9)], col)
            t.righe(y0 + 3, [(x0 - 1, x0 + 14)], col)
            if d != 'su':
                t.p(x0 + 6, y0 - 1, 'WH'); t.p(x0 + 7, y0 - 1, 'WH')
        elif 'capitano' in acc:
            t.righe(y0 - 2, [(x0 + 1, x0 + 12)], 'WH')
            t.righe(y0 - 1, [(x0 + 1, x0 + 12)], 'WH')
            if d == 'giu':
                t.righe(y0 + 3, [(x0 + 2, x0 + 11)], 'EY')
                t.p(x0 + 6, y0 + 1, 'A1'); t.p(x0 + 7, y0 + 1, 'A1')
            elif d == 'sx':
                t.righe(y0 + 3, [(x0 - 2, x0 + 4)], 'EY')
        elif 'berretto_lana' in acc:
            t.righe(y0 + 2, [(x0, x0 + 13)], 'A3')
        else:
            if d == 'giu' and 'berretto_rovescio' not in acc:
                t.righe(y0 + 3, [(x0 + 1, x0 + 12)], 'A3' if 'berretto' in acc else col)
            elif d == 'sx':
                visiera = (x0 - 3, x0 + 3) if 'berretto_rovescio' not in acc else (x0 + 11, x0 + 16)
                t.righe(y0 + 3, [visiera], 'A3' if 'berretto' in acc or 'berretto_rovescio' in acc else col)
            elif d == 'su' and 'berretto_rovescio' in acc:
                t.righe(y0 + 3, [(x0 + 1, x0 + 12)], 'A3')
    if 'fedora' in acc or 'paglia' in acc:
        col = 'A2' if 'fedora' in acc else 'A3'
        t.righe(y0 - 2, [(x0 + 3, x0 + 10), (x0 + 2, x0 + 11), (x0 + 2, x0 + 11)], col)
        t.righe(y0 + 1, [(x0 + 2, x0 + 11)], 'A1' if 'fedora' in acc else 'A1')
        t.righe(y0 + 2, [(x0 - 2, x0 + 15)], col)
    if 'cuffie' in acc:
        t.righe(y0 - 1, [(x0 + 2, x0 + 11)], 'A2')
        if d in ('giu', 'su'):
            t.rett(x0 - 1, y0 + 5, x0, y0 + 8, 'A2'); t.rett(x0 + 13, y0 + 5, x0 + 14, y0 + 8, 'A2')
        else:
            t.rett(x0 + 8, y0 + 5, x0 + 10, y0 + 8, 'A2')
    if 'auricolare' in acc:
        if d == 'giu':
            t.p(x0, y0 + 8, 'A2')
        elif d == 'sx':
            t.p(x0 + 9, y0 + 8, 'A2'); t.p(x0 + 9, y0 + 9, 'A2')
    if 'fiocco' in acc and d != 'giu':
        t.rett(x0 + 5, y0 - 1, x0 + 8, y0, 'A1')


# ------------------------------------------------------------------------------------------ il corpo

def corpo_fronte(t, s, d, posa, dy):
    """Corpo di fronte o di spalle. posa: dict con braccia (b_sx, b_dx) e gambe (g_sx, g_dx)."""
    y0 = 18 + dy
    largo = s.get('pancia', 0)
    xa, xb = 11 - largo, 20 + largo
    sopra = s.get('sopra', 'maglia')
    sotto = s.get('sotto', 'pantaloni')
    lungo = sopra in ('camice', 'cappotto', 'abito', 'toga', 'mantello')
    # gambe e scarpe
    for lato, (g0, g1) in (('sx', (11, 14)), ('dx', (17, 20))):
        st = posa.get('g_' + lato, 'giu')
        piede = PIEDE - {'giu': 0, 'alza': 1, 'alza2': 2, 'seduto': 0}.get(st, 0)
        if st == 'seduto':
            continue
        gamba = 'BO' if sotto in ('pantaloni', 'tuta') else ('SK' if sotto in ('gonna', 'pantaloncini', 'gonna_lunga') and not s.get('calze') else 'A3')
        if sotto == 'gonna_lunga':
            gamba = 'BO'
        t.rett(g0, y0 + 8, g1, piede - 1, gamba)
        t.rett(g0, piede, g1, piede + 1, 'SH')
    # parte di sotto
    if sotto in ('pantaloni', 'tuta', 'pantaloncini'):
        t.rett(xa, y0 + 6, xb, y0 + 7, 'BO')
        t.p(15, y0 + 7, 'BOs'); t.p(16, y0 + 7, 'BOs')
    elif sotto in ('gonna', 'gonna_lunga'):
        t.righe(y0 + 6, [(xa, xb), (xa - 1, xb + 1), (xa - 1, xb + 1)], 'BO')
        if sotto == 'gonna_lunga':
            t.righe(y0 + 9, [(xa - 1, xb + 1), (xa - 1, xb + 1)], 'BO')
    # busto
    t.righe(y0, [(xa + 1, xb - 1)] + [(xa, xb)] * 5, 'TO')
    if lungo:
        t.righe(y0 + 6, [(xa, xb), (xa - 1, xb + 1), (xa - 1, xb + 1)], 'TO')
        if d == 'giu' and sopra in ('camice', 'cappotto'):
            t.rett(15, y0 + 6, 16, y0 + 8, 'O' if sopra == 'cappotto' else 'TOs')
    if 'cintura' in s.get('accessori', ()) and not lungo:
        t.righe(y0 + 6, [(xa, xb)], 'A3')
    dettagli_busto(t, s, d, y0, xa, xb)
    # braccia
    for lato in ('sx', 'dx'):
        braccio_fronte(t, s, d, lato, posa.get('b_' + lato, 'giu'), y0, xa, xb)


def dettagli_busto(t, s, d, y0, xa, xb):
    sopra = s.get('sopra', 'maglia')
    acc = s.get('accessori', ())
    if d == 'giu':
        if sopra in ('giacca', 'cappotto', 'tailleur', 'camice'):
            interno = 'WH' if sopra != 'camice' else s.get('camice_interno', 'A2')
            t.righe(y0, [(14, 17), (14, 17), (15, 16), (15, 16), (15, 16)], interno)
            if 'cravatta' in acc:
                t.righe(y0 + 1, [(15, 16), (15, 16), (15, 16), (15, 16)], 'A1')
            if sopra == 'giacca' and s.get('doppiopetto'):
                t.p(14, y0 + 4, 'A3'); t.p(17, y0 + 4, 'A3')
        elif sopra in ('camicia', 'polo'):
            t.p(14, y0, 'WH' if sopra == 'camicia' else 'TOs'); t.p(17, y0, 'WH' if sopra == 'camicia' else 'TOs')
            t.p(15, y0 + 1, 'TOs'); t.p(15, y0 + 3, 'TOs')
            if 'cravatta' in acc:
                t.righe(y0 + 1, [(15, 16), (15, 16), (15, 16), (15, 16)], 'A1')
        elif sopra in ('maglia', 'canotta', 'felpa'):
            t.righe(y0, [(14, 17)], 'SK' if sopra == 'canotta' else 'TOs')
            if sopra == 'felpa':
                t.rett(13, y0 + 3, 18, y0 + 4, 'TOs')
        elif sopra == 'abito':
            t.righe(y0, [(13, 18)], 'SK')
        elif sopra == 'tuta_lavoro':
            t.righe(y0, [(14, 17)], 'TOs')
            t.rett(12, y0 + 2, 13, y0 + 3, 'TOs')
        elif sopra == 'righe':
            for k in (1, 3, 5):
                t.righe(y0 + k, [(xa, xb)], 'WH')
        elif sopra == 'toga':
            t.righe(y0, [(14, 17), (15, 16)], 'WH')
        if 'gilet' in acc:
            t.rett(xa, y0 + 1, xa + 2, y0 + 5, 'A2'); t.rett(xb - 2, y0 + 1, xb, y0 + 5, 'A2')
            t.righe(y0 + 3, [(xa, xa + 2)], 'WH'); t.righe(y0 + 3, [(xb - 2, xb)], 'WH')
        if 'collana' in acc:
            t.righe(y0 + 1, [(13, 13), (14, 14), (15, 16)], 'A3')
            t.righe(y0 + 1, [(18, 18), (17, 17)], 'A3')
        if 'perle' in acc:
            for x in (13, 15, 16, 18):
                t.p(x, y0 + 1, 'WH')
        if 'fascia' in acc:
            for k in range(6):
                t.p(xa + 1 + k, y0 + k, 'A1'); t.p(xa + 2 + k, y0 + k, 'WH'); t.p(xa + 3 + k, y0 + k, 'A2')
        if 'stetoscopio' in acc:
            t.righe(y0, [(13, 13), (13, 13), (14, 14), (14, 15)], 'A3')
            t.righe(y0, [(18, 18), (18, 18)], 'A3')
        if 'bottoni_oro' in acc:
            t.p(13, y0 + 2, 'A3'); t.p(18, y0 + 2, 'A3'); t.p(13, y0 + 4, 'A3'); t.p(18, y0 + 4, 'A3')
        if 'fischietto' in acc:
            t.p(16, y0 + 1, 'A3'); t.p(16, y0 + 2, 'A2')
        if 'pochette' in acc:
            t.p(13, y0 + 2, 'A1'); t.p(12, y0 + 2, 'A1')
    if s.get('bicolore') and d in ('giu', 'su'):
        for y in range(y0, y0 + 6):
            for x in range(16, xb + 1):
                if t.g(x, y) == 'TO':
                    t.p(x, y, 'A1')
    if 'sciarpa' in acc and d in ('giu', 'su'):
        t.righe(y0, [(xa + 1, xb - 1)], 'A1')
        if d == 'giu':
            t.rett(13, y0 + 1, 13, y0 + 5, 'A1'); t.rett(18, y0 + 1, 18, y0 + 5, 'A1')
    if 'maglione' in acc and d in ('giu', 'su'):
        t.righe(y0, [(xa, xb)], 'A1')
        if d == 'giu':
            t.rett(15, y0 + 1, 16, y0 + 2, 'A1')
    if 'borsello' in acc or 'tracolla' in acc:
        # cinghia da una spalla al fianco opposto, borsello al fianco
        if d in ('giu', 'su'):
            for k in range(6):
                x = xb - 1 - k if d == 'giu' else xa + 1 + k
                t.p(x, y0 + k, 'A2')
            bx = xa - 1 if d == 'giu' else xb - 1
            t.rett(bx, y0 + 5, bx + 2, y0 + 7, 'A2')
    if 'alta_visibilita' in acc and d in ('giu', 'su'):
        t.righe(y0 + 3, [(xa, xb)], 'A3')
        t.righe(y0 + 4, [(xa, xb)], 'WH')
    if d == 'su' and sopra == 'felpa':
        t.righe(y0, [(13, 18), (14, 17)], 'TOs')
    if d == 'su' and s.get('capelli') in ('lunghi', 'cotonati'):
        t.righe(y0, [(12, 19), (12, 19), (13, 18)], 'HA')
    if d == 'su' and s.get('capelli') == 'caschetto':
        t.righe(y0, [(12, 19)], 'HA')
    if d == 'su' and 'fiocco' in acc:
        pass


def braccio_fronte(t, s, d, lato, st, y0, xa, xb):
    """Braccio di fronte/di spalle. lato 'sx' = a sinistra dello schermo."""
    corto = s.get('maniche') == 'corte' or s.get('sopra') == 'canotta'
    sleeve = 'SK' if s.get('sopra') == 'canotta' else 'TO'
    sgn = -1 if lato == 'sx' else 1
    xo = xa - 1 if lato == 'sx' else xb + 1          # cucitura
    x1, x2 = (xa - 3, xa - 2) if lato == 'sx' else (xb + 2, xb + 3)

    def manica(yy0, yy1, xx1, xx2):
        for y in range(yy0, yy1 + 1):
            r = sleeve if (not corto or y <= yy0 + 1) else 'SK'
            t.rett(xx1, y, xx2, y, r)
    if st in ('giu', 'avanti', 'dietro'):
        fine = {'giu': y0 + 4, 'avanti': y0 + 5, 'dietro': y0 + 3}[st]
        manica(y0 + 1, fine, x1, x2)
        t.rett(x1, fine + 1, x2, fine + 1, 'SK')
        t.rett(xo, y0 + 1, xo, fine, 'O')
    elif st == 'piegato':
        manica(y0 + 1, y0 + 3, x1, x2)
        t.rett(xo, y0 + 1, xo, y0 + 3, 'O')
        hx = x2 + 1 if lato == 'sx' else x1 - 1
        t.rett(hx - (0 if lato == 'sx' else 1), y0 + 3, hx + (1 if lato == 'sx' else 0), y0 + 4, 'SK')
    elif st == 'alto':
        manica(y0 - 6, y0 + 1, x1 + sgn, x2 + sgn)
        t.rett(x1 + sgn, y0 - 8, x2 + sgn, y0 - 7, 'SK')
    elif st == 'medio':
        a, b = (x1 - 3, x2) if lato == 'sx' else (x1, x2 + 3)
        t.rett(a, y0 + 1, b, y0 + 2, sleeve)
        hx = a - 1 if lato == 'sx' else b + 1
        t.rett(hx, y0, hx, y0 + 2, 'SK')
    elif st == 'su_mezzo':
        manica(y0 - 3, y0 + 1, x1 + sgn, x2 + sgn)
        t.rett(x1 + sgn, y0 - 5, x2 + sgn, y0 - 4, 'SK')
    elif st == 'spinta':
        # avanti verso chi guarda (di fronte) o verso il fondo (di spalle): mani davanti al busto
        manica(y0 + 1, y0 + 2, x1, x2)
        t.rett(xo, y0 + 1, xo, y0 + 2, 'O')
        hx = 12 if lato == 'sx' else 18
        t.rett(hx, y0 + 2, hx + 1, y0 + 3, 'SK' if d == 'giu' else sleeve)
    elif st == 'manubrio':
        manica(y0 + 1, y0 + 2, x1, x2)
        t.rett(x1, y0 + 3, x2, y0 + 3, 'SK')
    elif st == 'nascosto':
        pass


def corpo_lato(t, s, posa, dy):
    """Corpo di profilo verso sinistra."""
    y0 = 18 + dy
    largo = s.get('pancia', 0)
    xa, xb = 12 - largo, 19 + largo
    sopra = s.get('sopra', 'maglia')
    sotto = s.get('sotto', 'pantaloni')
    lungo = sopra in ('camice', 'cappotto', 'abito', 'toga', 'mantello')
    gamba = 'BO' if sotto in ('pantaloni', 'tuta', 'gonna_lunga') else ('A3' if s.get('calze') else 'SK')
    passo = posa.get('passo', 0)        # 0 fermo, 1 passo, 2 corsa
    braccio = posa.get('braccio', 'giu')
    # braccio lontano (dietro il corpo), solo quando oscilla
    if braccio == 'avanti' or (braccio == 'corsa_a'):
        t.rett(xb - 1, y0 + 1, xb + 1, y0 + 3, 'TOs')
        t.rett(xb, y0 + 4, xb + 1, y0 + 4, 'SKs')
    # gambe
    if posa.get('seduto'):
        pass
    elif passo == 0:
        t.rett(13, y0 + 8, 18, PIEDE - 1, gamba)
        t.rett(15, y0 + 8, 15, PIEDE - 1, 'BOs' if gamba == 'BO' else ('SKs' if gamba == 'SK' else 'A3'))
        t.rett(12, PIEDE, 18, PIEDE + 1, 'SH')
    else:
        av = 3 if passo == 1 else 4
        for k, y in enumerate(range(y0 + 8, PIEDE)):
            f = (k + 1) * av // (PIEDE - y0 - 8)
            t.rett(13 - f, y, 15 - f, y, gamba)
            t.rett(16 + f, y, 18 + f, y, gamba)
        alza = 0 if passo == 1 else 1
        t.rett(13 - av - 1, PIEDE - alza, 15 - av, PIEDE + 1 - alza, 'SH')
        t.rett(16 + av, PIEDE, 18 + av + 1, PIEDE + 1, 'SH')
    if sotto in ('pantaloni', 'tuta', 'pantaloncini'):
        t.rett(xa + 1, y0 + 6, xb - 1, y0 + 7, 'BO')
    elif sotto in ('gonna', 'gonna_lunga'):
        t.righe(y0 + 6, [(xa, xb), (xa - 1, xb + 1), (xa - 1, xb + 1)], 'BO')
        if sotto == 'gonna_lunga':
            t.righe(y0 + 9, [(xa - 1, xb + 1), (xa - 1, xb + 1)], 'BO')
    t.righe(y0, [(xa + 1, xb - 1)] + [(xa, xb)] * 5, 'TO')
    if lungo:
        t.righe(y0 + 6, [(xa, xb), (xa - 1, xb + 1), (xa - 1, xb + 1)], 'TO')
    acc = s.get('accessori', ())
    if 'cravatta' in acc and sopra in ('giacca', 'camicia', 'cappotto', 'tailleur'):
        t.righe(y0, [(xa, xa + 1), (xa, xa)], 'WH')
        t.rett(xa, y0 + 1, xa, y0 + 3, 'A1')
    elif sopra in ('giacca', 'cappotto', 'tailleur', 'camice'):
        t.righe(y0, [(xa, xa + 1)], 'WH')
    if 'alta_visibilita' in acc:
        t.righe(y0 + 3, [(xa, xb)], 'A3'); t.righe(y0 + 4, [(xa, xb)], 'WH')
    if 'gilet' in acc:
        t.rett(xa, y0 + 1, xa + 1, y0 + 5, 'A2')
    if 'fascia' in acc:
        for k in range(6):
            t.p(xa + k + 1, y0 + k, 'A1')
    if 'cintura' in acc and not lungo:
        t.righe(y0 + 6, [(xa + 1, xb - 1)], 'A3')
    if 'sciarpa' in acc:
        t.righe(y0, [(xa, xb - 1)], 'A1'); t.rett(xa, y0 + 1, xa, y0 + 4, 'A1')
    if 'maglione' in acc:
        t.righe(y0, [(xa, xb)], 'A1'); t.p(xa, y0 + 1, 'A1')
    if 'borsello' in acc or 'tracolla' in acc:
        t.rett(xb - 1, y0 + 5, xb + 1, y0 + 7, 'A2')
    if s.get('capelli') in ('lunghi', 'cotonati'):
        t.righe(y0, [(xb - 3, xb), (xb - 2, xb)], 'HA')
    if s.get('capelli') == 'coda':
        t.righe(y0 - 4, [(xb + 1, xb + 2), (xb + 1, xb + 3), (xb + 1, xb + 3), (xb, xb + 2), (xb - 1, xb + 1)], 'HA')
    # braccio vicino
    braccio_lato(t, s, braccio, y0, xa, xb)


def braccio_lato(t, s, st, y0, xa, xb):
    corto = s.get('maniche') == 'corte' or s.get('sopra') == 'canotta'
    sleeve = 'SK' if s.get('sopra') == 'canotta' else 'TOs'
    cx = (xa + xb) // 2

    def seg(x0, y0_, x1, y1_):
        for y in range(y0_, y1_ + 1):
            t.rett(x0, y, x1, y, sleeve if (not corto or y <= y0_ + 1) else 'SK')
    if st in ('giu', 'nascosto_no'):
        seg(cx - 1, y0 + 1, cx + 1, y0 + 4)
        t.rett(cx - 1, y0 + 5, cx + 1, y0 + 5, 'SK')
        t.rett(cx - 2, y0 + 2, cx - 2, y0 + 4, 'O')
    elif st == 'avanti':
        seg(cx - 2, y0 + 1, cx, y0 + 3)
        t.rett(cx - 4, y0 + 4, cx - 2, y0 + 4, 'SK')
        t.p(cx - 3, y0 + 4, 'SK')
    elif st == 'dietro':
        seg(cx + 1, y0 + 1, cx + 3, y0 + 3)
        t.rett(cx + 2, y0 + 4, cx + 4, y0 + 4, 'SK')
        t.rett(cx, y0 + 2, cx, y0 + 3, 'O')
    elif st in ('corsa_a', 'corsa_b', 'piegato'):
        seg(cx - 1, y0 + 1, cx + 1, y0 + 2)
        t.rett(cx - 3, y0 + 2, cx - 2, y0 + 3, 'SK')
    elif st == 'spinta':
        seg(cx - 4, y0 + 1, cx, y0 + 2)
        t.rett(cx - 6, y0 + 1, cx - 5, y0 + 2, 'SK')
    elif st == 'alto':
        seg(cx - 1, y0 - 6, cx + 1, y0 + 1)
        t.rett(cx - 1, y0 - 8, cx + 1, y0 - 7, 'SK')
    elif st == 'su_mezzo':
        seg(cx - 2, y0 - 3, cx, y0 + 1)
        t.rett(cx - 2, y0 - 5, cx, y0 - 4, 'SK')
    elif st == 'manubrio':
        seg(cx - 3, y0 + 1, cx, y0 + 2)
        t.rett(cx - 5, y0 + 2, cx - 4, y0 + 3, 'SK')
    elif st == 'nascosto':
        pass


def oggetto_in_mano(t, s, d, posa, dy):
    """Valigetta, cartellina, telefono, bastone, tablet: nella mano destra del personaggio."""
    acc = s.get('accessori', ())
    y0 = 18 + dy
    if posa.get('b_dx', posa.get('braccio', 'giu')) not in ('giu', 'avanti', 'dietro'):
        return
    xb = 20 + s.get('pancia', 0)
    if d in ('giu', 'su'):
        hx = xb + 2 if d == 'giu' else 11 - s.get('pancia', 0) - 3
        if 'valigetta' in acc:
            t.rett(hx - 1, y0 + 6, hx + 2, y0 + 8, 'A2'); t.p(hx, y0 + 5, 'A3'); t.p(hx + 1, y0 + 5, 'A3')
        elif 'cartellina' in acc or 'buste' in acc or 'tablet' in acc:
            col = 'WH' if 'buste' in acc else ('A3' if 'tablet' in acc else 'A2')
            t.rett(hx, y0 + 3, hx + 1, y0 + 7, col)
        elif 'bastone' in acc:
            t.rett(hx + 1, y0 + 5, hx + 1, PIEDE + 1, 'A3')
        elif 'telefono' in acc and d == 'giu':
            t.rett(hx, y0 + 4, hx + 1, y0 + 5, 'A2')
    else:
        cx = (12 + 19) // 2
        if 'valigetta' in acc:
            t.rett(cx - 2, y0 + 6, cx + 2, y0 + 8, 'A2'); t.p(cx, y0 + 5, 'A3')
        elif 'cartellina' in acc or 'buste' in acc or 'tablet' in acc:
            col = 'WH' if 'buste' in acc else ('A3' if 'tablet' in acc else 'A2')
            t.rett(cx - 3, y0 + 4, cx - 2, y0 + 7, col)
        elif 'bastone' in acc:
            t.rett(cx - 3, y0 + 5, cx - 3, PIEDE + 1, 'A3')


# ------------------------------------------------------------------------------------------ mezzi e attrezzi

def bici(t, d, fase, davanti):
    """Bicicletta. davanti=True: le parti che coprono il corpo (si disegnano dopo)."""
    if d == 'sx':
        if davanti:
            t.rett(9, 19, 11, 19, 'A2')                       # manubrio
            return
        for cx, cy in ((9, 25), (22, 25)):
            for y in range(cy - 4, cy + 5):
                for x in range(cx - 4, cx + 5):
                    r2 = (x - cx) ** 2 + (y - cy) ** 2
                    if 13 <= r2 <= 20:
                        t.p(x, y, 'A3')
                    elif r2 <= 2:
                        t.p(x, y, 'A2')
        for x in range(10, 22):
            t.p(x, 23 + (x % 2 if fase else 0), 'A2')
        t.rett(10, 19, 10, 24, 'A2')
        t.rett(19, 21, 19, 24, 'A2')
    else:
        if davanti and d == 'giu':
            t.rett(14, 23, 17, 30, 'A3'); t.rett(15, 24, 16, 29, 'O')
            t.rett(9, 21, 22, 21, 'A2')
        elif not davanti and d == 'su':
            t.rett(14, 23, 17, 30, 'A3'); t.rett(15, 24, 16, 29, 'O')
        elif davanti and d == 'su':
            t.rett(12, 23, 19, 23, 'A2')


def canna(t, d, fase):
    """Canna da pesca nelle quattro fasi (0 indietro, 1 alta, 2 lanciata, 3 tesa con la lenza)."""
    if d == 'sx':
        pts = {0: [(18, 18), (20, 15), (22, 12), (24, 9)],
               1: [(14, 17), (14, 13), (14, 9), (14, 5), (14, 2)],
               2: [(12, 20), (9, 19), (6, 18), (3, 17), (1, 16)],
               3: [(12, 20), (9, 20), (6, 20), (3, 20), (1, 20)]}[fase]
    elif d == 'giu':
        pts = {0: [(21, 17), (22, 13), (23, 9), (24, 5)],
               1: [(21, 17), (21, 12), (21, 7), (21, 3)],
               2: [(21, 22), (21, 24), (21, 27), (21, 30)],
               3: [(21, 22), (21, 25), (21, 28), (21, 31)]}[fase]
    else:
        pts = {0: [(10, 22), (9, 25), (8, 28), (7, 30)],
               1: [(10, 17), (10, 12), (10, 7), (10, 3)],
               2: [(10, 16), (10, 12), (10, 8), (10, 4), (10, 0)],
               3: [(10, 16), (10, 11), (10, 6), (10, 1)]}[fase]
    for (xa, ya), (xb, yb) in zip(pts, pts[1:]):
        n = max(abs(xb - xa), abs(yb - ya))
        for k in range(n + 1):
            t.p(xa + (xb - xa) * k // max(n, 1), ya + (yb - ya) * k // max(n, 1), 'A3')


# ------------------------------------------------------------------------------------------ disegno

def disegna(s, posa):
    """posa = dict(dir=…, tipo=…, fase=…). Restituisce 1024 indici."""
    d = posa['dir']
    specchio = d == 'dx'
    dd = 'sx' if specchio else d
    tipo = posa.get('tipo', 'fermo')
    fase = posa.get('fase', 0)
    t = Tela()
    dy = 0
    p = {}
    if tipo == 'fermo':
        p = dict(b_sx='giu', b_dx='giu', braccio='giu', passo=0)
    elif tipo == 'passo':
        dy = -1
        if dd == 'sx':
            p = dict(passo=1, braccio='avanti' if fase == 0 else 'dietro')
        else:
            p = dict(g_sx='giu' if fase == 0 else 'alza', g_dx='alza' if fase == 0 else 'giu',
                     b_sx='dietro' if fase == 0 else 'avanti', b_dx='avanti' if fase == 0 else 'dietro')
    elif tipo == 'corsa_fermo':
        dy = 1
        p = dict(b_sx='piegato', b_dx='piegato', braccio='corsa_a', passo=0)
    elif tipo == 'corsa':
        dy = 0
        if dd == 'sx':
            p = dict(passo=2, braccio='corsa_a' if fase == 0 else 'corsa_b')
        else:
            p = dict(g_sx='giu' if fase == 0 else 'alza2', g_dx='alza2' if fase == 0 else 'giu',
                     b_sx='piegato', b_dx='piegato')
    elif tipo == 'banzai':
        st = ['giu', 'medio', 'su_mezzo', 'alto'][fase]
        p = dict(b_sx=st, b_dx=st, braccio=st if st != 'medio' else 'avanti', passo=0)
    elif tipo == 'spinta':
        dy = 0 if fase == 0 else -1
        p = dict(b_sx='spinta', b_dx='spinta', braccio='spinta', passo=0)
    elif tipo == 'scala':
        dy = -1 if fase == 1 else 0
        p = dict(b_sx='alto' if fase != 2 else 'su_mezzo', b_dx='su_mezzo' if fase != 2 else 'alto',
                 g_sx='alza' if fase == 1 else 'giu', g_dx='giu' if fase == 1 else 'alza')
    elif tipo == 'salva':
        p = dict(b_sx='giu', b_dx='giu' if fase == 0 else 'piegato')
    elif tipo == 'pesca':
        p = dict(b_sx='piegato', b_dx='piegato', braccio='piegato' if fase != 1 else 'su_mezzo', passo=0)
    elif tipo == 'surf':
        dy = 2
        p = dict(g_sx='seduto', g_dx='seduto', b_sx='piegato', b_dx='piegato', braccio='piegato', seduto=True)
    elif tipo in ('bici', 'bici_salto'):
        dy = -1 if tipo == 'bici' else -3
        if dd == 'sx':
            p = dict(braccio='manubrio', seduto=True)
        else:
            p = dict(b_sx='manubrio', b_dx='manubrio', g_sx='alza' if fase == 2 else 'giu',
                     g_dx='alza' if fase == 1 else 'giu')
    if tipo in ('bici', 'bici_salto'):
        bici(t, dd, fase, False)
    if dd == 'sx':
        if tipo in ('bici', 'bici_salto'):
            # gambe sui pedali
            y0 = 18 + dy
            gamba = 'BO' if s.get('sotto') in ('pantaloni', 'tuta') else 'SK'
            a = {0: 1, 1: 0, 2: 2}[fase]
            t.rett(13 - a, y0 + 7, 15 - a, y0 + 9, gamba); t.rett(12 - a, y0 + 10, 14 - a, y0 + 10, 'SH')
            t.rett(16, y0 + 7, 18, y0 + 8 + a, gamba); t.rett(16, y0 + 9 + a, 18, y0 + 9 + a, 'SH')
        corpo_lato(t, s, p, dy)
        if tipo == 'surf':
            t.rett(10, 24 + dy + 2, 19, 27, 'BO')
    else:
        corpo_fronte(t, s, dd, p, dy)
        if tipo == 'surf':
            t.rett(10, 26, 21, 27, 'BO')
    oggetto_in_mano(t, s, dd, p, dy)
    testa(t, s, dd, dy)
    if dd == 'su' and s.get('capelli') == 'coda':
        t.righe(15 + dy, [(15, 16), (14, 17), (14, 17), (14, 17), (15, 16), (15, 16)], 'HA')
        t.p(15, 15 + dy, 'A1'); t.p(16, 15 + dy, 'A1')
    if dd == 'sx' and s.get('capelli') == 'coda':
        t.righe(10 + dy, [(23, 23), (23, 24), (23, 24), (23, 24), (23, 24), (22, 23), (22, 23)], 'HA')
        t.p(22, 10 + dy, 'A1'); t.p(22, 11 + dy, 'A1')
    copricapo(t, s, dd, dy)
    if tipo in ('bici', 'bici_salto'):
        bici(t, dd, fase, True)
    if tipo == 'pesca':
        canna(t, dd, fase)
    t.ombreggia()
    t.contorna()
    if specchio:
        t.specchio()
    return t.indici()
