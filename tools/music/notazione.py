"""Notazione delle partiture di Pokémon Trinacria (Modulo 5, blocchi 5.2-5.4).

Le partiture (R-AUD-12) scrivono il MIDI con MidiWriter di tools/trinacria_audio.py;
questo modulo dà una scrittura compatta e controllata, con sola libreria standard.
Una partitura lo carica così (runpy dà __file__):

    import os, sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from notazione import Brano, Giro

    def partitura(A):
        b = Brano(A, bpm=112, metro=(4, 4))
        fl = b.voce('flauto', 35, volume=110)
        fl.suona('| d5/4 f#5/8 a5 b5/4. a5/8 | g5/2 e5 |', da=0)
        b.ritornello(0, 2)                     # in battute
        return b.fine()

Notazione di Voce.suona():
  nota      lettera c d e f g a b, alterazione # oppure b, ottava (do centrale c4 = 60): eb4, f#5
  pausa     r
  accordo   note unite da +: c4+e4+g4
  durata    /1 /2 /4 /8 /16 /32; . puntata (/4.), t terzina (/8t), *N moltiplica (r/1*4);
            senza durata vale quella del simbolo precedente
  segni     dopo la durata: ~ legatura (la nota continua nella successiva uguale, anche
            oltre la stanghetta), > accento, ' staccato, _ tenuto (durata piena)
  | ||      stanghetta (|| doppia): il cursore deve essere all'inizio di una battuta (NotaErrata se no)
  vNN       velocità delle note seguenti (1-127)

Sigle degli accordi (Giro): fondamentale A-G con # o b, poi una qualità di QUALITA
(«», m, 7, m7, maj7, dim, ...) e facoltativo /basso: «Am», «F#m7», «Bb/D», «E7b9».
Un Giro è una stringa di battute separate da |; gli accordi di una battuta la
dividono in parti uguali: 'Am | Dm E7 | Am'.

Schemi ritmici (accordi, arpeggi, basso, batteria): una battuta di passi uguali,
la lunghezza della stringa dà la griglia (8 caratteri in 4/4 = crome).
"""
import re

QUALITA = {
    '': (0, 4, 7), 'm': (0, 3, 7), '5': (0, 7), '6': (0, 4, 7, 9), 'm6': (0, 3, 7, 9),
    '7': (0, 4, 7, 10), 'm7': (0, 3, 7, 10), 'maj7': (0, 4, 7, 11), 'mmaj7': (0, 3, 7, 11),
    'dim': (0, 3, 6), 'dim7': (0, 3, 6, 9), 'm7b5': (0, 3, 6, 10), 'aug': (0, 4, 8),
    'sus4': (0, 5, 7), 'sus2': (0, 2, 7), '7sus4': (0, 5, 7, 10), 'add9': (0, 4, 7, 14),
    'madd9': (0, 3, 7, 14), '9': (0, 4, 7, 10, 14), 'm9': (0, 3, 7, 10, 14),
    'maj9': (0, 4, 7, 11, 14), '7b9': (0, 4, 7, 10, 13),
}
PC = {'c': 0, 'd': 2, 'e': 4, 'f': 5, 'g': 7, 'a': 9, 'b': 11}

# Batteria: programma 39 della tavolozza comune (tasti F1-A5). Nomi dei tasti usati,
# disposizione General MIDI che i brani di HeartGold seguono (blocco 5.1, §9.2).
BATTERIA = {
    'cassa': 36, 'cassa2': 35, 'rullante': 38, 'rullante2': 40, 'bordo': 37,
    'battimani': 39, 'hh': 42, 'hha': 46, 'tom_a': 48, 'tom_m': 45, 'tom_b': 43,
    'tamburello': 54, 'legnetto': 76, 'legnetto2': 77, 'triangolo': 80, 'triangolo_a': 81,
}
DINAMICA = {'X': 120, 'x': 96, 'o': 58}

_NOTA = re.compile(r'([a-g])(#|b)?(-?\d)$')
_TOKEN = re.compile(r"(?P<p>r|[a-g][#b]?-?\d(?:\+[a-g][#b]?-?\d)*)"
                    r"(?:/(?P<d>\d+)(?P<dot>\.?)(?P<tri>t?)(?:\*(?P<mul>\d+))?)?"
                    r"(?P<seg>[~>'_]*)$")
_SIGLA = re.compile(r'([A-G])(#|b)?([^/]*)(?:/([A-G])(#|b)?)?$')


class NotaErrata(Exception):
    pass


def tasto(nome):
    m = _NOTA.match(nome)
    if not m:
        raise NotaErrata('nota sconosciuta %r' % nome)
    acc = {'#': 1, 'b': -1, None: 0}[m.group(2)]
    k = (int(m.group(3)) + 1) * 12 + PC[m.group(1)] + acc
    if not 0 <= k <= 127:
        raise NotaErrata('nota fuori da 0-127: %r' % nome)
    return k


class Accordo:
    def __init__(self, sigla):
        m = _SIGLA.match(sigla)
        if not m or m.group(3) not in QUALITA:
            raise NotaErrata('accordo sconosciuto %r' % sigla)
        self.sigla = sigla
        self.radice = (PC[m.group(1).lower()] + {'#': 1, 'b': -1, None: 0}[m.group(2)]) % 12
        self.intervalli = QUALITA[m.group(3)]
        self.basso = self.radice
        if m.group(4):
            self.basso = (PC[m.group(4).lower()] + {'#': 1, 'b': -1, None: 0}[m.group(5)]) % 12

    def trasposto(self, semitoni):
        a = Accordo.__new__(Accordo)
        a.sigla = '%s%+d' % (self.sigla, semitoni) if semitoni else self.sigla
        a.radice = (self.radice + semitoni) % 12
        a.basso = (self.basso + semitoni) % 12
        a.intervalli = self.intervalli
        return a

    def classi(self):
        return {(self.radice + i) % 12 for i in self.intervalli} | {self.basso}

    def grado(self, g, radice_tasto):
        """Tasto del grado g ('1','3','5','7','8','9','10','12','15', con ',' un'ottava sotto)."""
        giu = g.endswith(',')
        g = g.rstrip(',')
        iv = list(self.intervalli)
        base = {'1': iv[0], '3': iv[1] if len(iv) > 1 else 12, '5': iv[2] if len(iv) > 2 else iv[-1],
                '7': iv[3] if len(iv) > 3 and iv[3] < 12 else 12,
                '9': next((i for i in iv if i > 12), 14), '8': 12, '6': 9, '4': 5, '2': 2}
        alto = {'10': '3', '12': '5', '14': '7', '15': '8'}
        if g in alto:
            off = base[alto[g]] + 12
        elif g in base:
            off = base[g]
        else:
            raise NotaErrata('grado sconosciuto %r' % g)
        return radice_tasto + off - (12 if giu else 0)


class Giro:
    """Successione di accordi per battute: Giro('Am | Dm E7 | Am')."""

    def __init__(self, testo):
        self.battute = []
        for parte in testo.split('|'):
            sig = parte.split()
            if sig:
                self.battute.append([Accordo(s) for s in sig])
        if not self.battute:
            raise NotaErrata('giro vuoto')

    def __len__(self):
        return len(self.battute)

    def __add__(self, altro):
        g = Giro.__new__(Giro)
        g.battute = self.battute + altro.battute
        return g

    def __mul__(self, n):
        g = Giro.__new__(Giro)
        g.battute = self.battute * n
        return g

    def accordo(self, battuta, frazione):
        acc = self.battute[battuta % len(self.battute)]
        return acc[min(len(acc) - 1, int(frazione * len(acc) + 1e-9))]


def _passi(schema):
    """'x--.x-x.' -> [(passo, lunghezza in passi, carattere)]"""
    out = []
    for i, c in enumerate(schema):
        if c in '.- ':
            continue
        n = 1
        while i + n < len(schema) and schema[i + n] == '-':
            n += 1
        out.append((i, n, c))
    return out


class Voce:
    def __init__(self, brano, nome, canale, programma, volume, pan):
        self.b = brano
        self.nome, self.canale, self.programma = nome, canale, programma
        self.volume, self.pan = volume, pan
        self.note = []                 # (t, tasto, velocità, durata)
        self.ctrl = []                 # (t, 'pc'|numero cc, valore)
        self.t = 0
        self.vel = 100
        self.su_giro = False           # True se suona schemi sugli accordi
        self.copia_di = None           # nome della voce copiata (eco, raddoppio)
        self.intonata = programma != 39   # la batteria non si traspone
        self.pedale = False
        self._dur = brano.ppq
        self._legate = {}              # tasto -> [inizio, velocità, fine]

    # --- cursore e controlli
    def a(self, battuta):
        self._chiudi_legature()
        self.t = int(round(battuta * self.b.battuta))
        return self

    def cambia_programma(self, prg, battuta):
        self.ctrl.append((int(round(battuta * self.b.battuta)), 'pc', prg))
        return self

    def cc(self, num, val, battuta):
        self.ctrl.append((int(round(battuta * self.b.battuta)), num, val))
        return self

    def nota(self, t, key, vel, dur):
        if not 0 <= key <= 127:
            raise NotaErrata('%s: tasto %d fuori da 0-127' % (self.nome, key))
        if dur < 1:
            raise NotaErrata('%s: durata %d' % (self.nome, dur))
        self.note.append((int(t), key, max(1, min(127, int(vel))), int(dur)))

    # --- notazione
    def _durata(self, m):
        if m.group('d') is None:
            return self._dur
        den = int(m.group('d'))
        if den not in (1, 2, 4, 8, 16, 32):
            raise NotaErrata('%s: durata /%d' % (self.nome, den))
        d = self.b.ppq * 4 // den
        if m.group('dot'):
            d += d // 2
        if m.group('tri'):
            if d * 2 % 3:
                raise NotaErrata('%s: terzina di /%d non intera' % (self.nome, den))
            d = d * 2 // 3
        if m.group('mul'):
            d *= int(m.group('mul'))
        return d

    def _chiudi_legature(self, tranne=()):
        for k in list(self._legate):
            if k in tranne:
                continue
            ini, vel, fine = self._legate.pop(k)
            self.nota(ini, k, vel, fine - ini)

    def suona(self, testo, da=None, vel=None, trasponi=0, gate=0.9):
        """Scrive le note del testo dal cursore (o dalla battuta da)."""
        if da is not None:
            self.a(da)
        if vel is not None:
            self.vel = vel
        for tok in testo.split():
            if tok in ('|', '||'):
                if self.t % self.b.battuta:
                    raise NotaErrata('%s: stanghetta a metà battuta (battuta %.3f) prima di %r' % (
                        self.nome, self.t / self.b.battuta, testo[:60]))
                continue
            if re.match(r'v\d+$', tok):
                self.vel = int(tok[1:])
                continue
            m = _TOKEN.match(tok)
            if not m:
                raise NotaErrata('%s: simbolo sconosciuto %r' % (self.nome, tok))
            d = self._durata(m)
            self._dur = d
            seg = m.group('seg')
            if m.group('p') == 'r':
                self._chiudi_legature()
                self.t += d
                continue
            keys = [tasto(n) + trasponi for n in m.group('p').split('+')]
            v = self.vel + (20 if '>' in seg else 0)
            self._chiudi_legature(tranne=keys)
            for k in keys:
                if k in self._legate:
                    self._legate[k][2] = self.t + d
                    if '~' not in seg:
                        ini, vv, _ = self._legate.pop(k)
                        self.nota(ini, k, vv, self.t + d - ini - (0 if '_' in seg else max(1, int(d * (1 - gate)))))
                    continue
                if '~' in seg:
                    self._legate[k] = [self.t, v, self.t + d]
                    continue
                if "'" in seg:
                    dur = max(1, d // 2)
                elif '_' in seg:
                    dur = d
                else:
                    dur = max(1, d - max(1, int(d * (1 - gate))))
                self.nota(self.t, k, v, dur)
            self.t += d
        self._chiudi_legature()
        return self

    # --- schemi sugli accordi
    def _schema(self, giro, schema, da, volte, funzione):
        """Chiama funzione(t, durata, accordo, carattere, indice) per ogni colpo dello schema."""
        bt = self.b.battuta
        if bt % len(schema):
            raise NotaErrata('%s: schema di %d passi non divide la battuta' % (self.nome, len(schema)))
        passo = bt // len(schema)
        self.su_giro = True
        for n in range(len(giro) * volte):
            t0 = int(round((da + n) * bt))
            accs = giro.battute[n % len(giro)]
            for j, acc in enumerate(accs):
                self.b.armonia[t0 + j * bt // len(accs)] = (t0 + (j + 1) * bt // len(accs), acc)
            for i, lung, c in _passi(schema):
                acc = giro.accordo(n, i / len(schema))
                funzione(t0 + i * passo, lung * passo, acc, c, i)
        self.t = int(round((da + len(giro) * volte) * bt))
        return self

    def accordi(self, giro, schema, da, volte=1, registro=(55, 72), vel=72, voci=3, gate=0.9):
        """Accordi a blocchi con condotta delle parti: 'x' colpo, 'X' accento, '-' tiene."""
        prec = [None]

        def colpo(t, dur, acc, c, i):
            keys = _disponi(acc, registro, voci, prec[0])
            prec[0] = keys
            for k in keys:
                self.nota(t, k, vel + (18 if c == 'X' else 0), max(1, int(dur * gate)))
        return self._schema(giro, schema, da, volte, colpo)

    def arpeggi(self, giro, figura, da, volte=1, registro=(55, 79), vel=78, gate=0.9):
        """figura = gradi per passo separati da spazi ('1 5 8 10 12 10 8 5'), '.' pausa, '-' tiene."""
        toks = figura.split()
        schema = ''.join('x' if g not in '.-' else g for g in toks)

        def colpo(t, dur, acc, c, i):
            r = _radice(acc.radice, registro[0])
            self.nota(t, acc.grado(toks[i], r), vel, max(1, int(dur * gate)))
        return self._schema(giro, schema, da, volte, colpo)

    def basso(self, giro, figura, da, volte=1, registro=(28, 52), vel=100, gate=0.85):
        """Come arpeggi, ma il grado 1 è il basso dell'accordo (anche nelle sigle con /)."""
        toks = figura.split()
        schema = ''.join('x' if g not in '.-' else g for g in toks)

        def colpo(t, dur, acc, c, i):
            g = toks[i]
            if g.rstrip(',') in ('1', '8'):
                k = _radice(acc.basso, registro[0]) + (12 if g.rstrip(',') == '8' else 0) \
                    - (12 if g.endswith(',') else 0)
            else:
                k = acc.grado(g, _radice(acc.radice, registro[0]))
            self.nota(t, k, vel, max(1, int(dur * gate)))
        return self._schema(giro, schema, da, volte, colpo)

    def batteria(self, schemi, da, battute=1, dur_max=12):
        """schemi = {nome o tasto: 'x...x...'} (X forte, x normale, o leggero), per battuta;
        oppure una lista di dizionari, uno per battuta, ripetuta per 'battute' battute."""
        if isinstance(schemi, dict):
            schemi = [schemi]
        bt = self.b.battuta
        for n in range(battute):
            sch = schemi[n % len(schemi)]
            t0 = int(round((da + n) * bt))
            for nome, s in sch.items():
                key = BATTERIA[nome] if isinstance(nome, str) else nome
                if bt % len(s):
                    raise NotaErrata('%s: schema di %d passi non divide la battuta' % (self.nome, len(s)))
                passo = bt // len(s)
                for i, lung, c in _passi(s):
                    if c not in DINAMICA:
                        raise NotaErrata('%s: colpo %r' % (self.nome, c))
                    self.nota(t0 + i * passo, key, DINAMICA[c], min(dur_max, passo))
        self.t = int(round((da + battute) * bt))
        return self

    # --- ripetizioni
    def copia(self, da, battute, a, volte=1, trasponi=0):
        """Copia le note delle battute [da, da+battute) a partire dalla battuta a."""
        bt = self.b.battuta
        t0, t1 = int(round(da * bt)), int(round((da + battute) * bt))
        src = [n for n in self.note if t0 <= n[0] < t1]
        for v in range(volte):
            off = int(round((a + v * battute) * bt)) - t0
            for t, k, vel, dur in src:
                self.nota(t + off, k + trasponi, vel, dur)
        return self


def _nome(k):
    return ('c', 'c#', 'd', 'eb', 'e', 'f', 'f#', 'g', 'ab', 'a', 'bb', 'b')[k % 12] + str(k // 12 - 1)


def _radice(pc, minimo):
    k = minimo + ((pc - minimo) % 12)
    return k


def _disponi(acc, registro, voci, prec):
    """Disposizione dell'accordo in registro, la più vicina alla precedente."""
    iv = list(acc.intervalli)
    for togli in (7, 0):                        # si toglie prima la quinta, poi la fondamentale
        if len(iv) > voci and togli in iv:
            iv.remove(togli)
    pcs = [(acc.radice + i) % 12 for i in iv[-voci:]]
    lo, hi = registro
    base = list(pcs)
    while len(pcs) < voci:                      # raddoppi: fondamentale, poi le altre, se c'è posto
        posto = [pc for pc in base if sum(1 for k in range(lo, hi + 1) if k % 12 == pc) > pcs.count(pc)]
        if not posto:
            raise NotaErrata('registro %s troppo stretto per %d voci di %s' % (registro, voci, acc.sigla))
        pcs.append(posto[0])
    opzioni = []
    for pc in pcs:
        ks = [k for k in range(lo, hi + 1) if k % 12 == pc]
        if not ks:
            raise NotaErrata('registro %s troppo stretto per %s' % (registro, acc.sigla))
        opzioni.append(ks)
    centro = (lo + hi) / 2
    best, best_s = None, None
    def scegli(i, cur):
        nonlocal best, best_s
        if i == len(opzioni):
            s = sorted(cur)
            if len(set(s)) < len(s):
                return
            if s[-1] - s[0] > 14:
                return
            if prec:
                score = sum(abs(a - b) for a, b in zip(s, sorted(prec)))
            else:
                score = abs(sum(s) / len(s) - centro)
            if best_s is None or score < best_s:
                best, best_s = s, score
            return
        for k in opzioni[i]:
            scegli(i + 1, cur + [k])
    scegli(0, [])
    if best is None:
        raise NotaErrata('nessuna disposizione di %s in %s' % (acc.sigla, registro))
    return best


class Brano:
    def __init__(self, A, bpm, metro=(4, 4), ppq=48):
        self.A = A
        self.ppq = ppq
        self.bpm = bpm
        self.metro = metro
        self.battuta = ppq * 4 * metro[0] // metro[1]
        self.voci = []
        self.tempi = [(0, bpm)]
        self.loop = None
        self.durata = None
        self.armonia = {}              # inizio -> (fine, Accordo), dagli schemi sugli accordi

    def note_estranee(self, voce, min_dur=None):
        """Note della voce che cadono su un movimento, durano almeno min_dur (default una
        croma) e non appartengono all'accordo del momento: [(battuta, movimento, nota, sigla)].
        Serve a rileggere le melodie (appoggiature e note di passaggio volute restano)."""
        min_dur = min_dur or self.ppq // 2
        mov = self.battuta // self.metro[0]
        if self.metro[1] == 8 and self.metro[0] % 3 == 0:      # 6/8, 9/8, 12/8: movimento puntato
            mov *= 3
        spans = sorted((t, f, a) for t, (f, a) in self.armonia.items())
        out = []
        for t, k, vel, d in sorted(voce.note):
            if t % self.battuta % mov or d < min_dur - 2:
                continue
            acc = next((a for s, f, a in spans if s <= t < f), None)
            if acc and k % 12 not in acc.classi():
                out.append((t // self.battuta, (t % self.battuta) // mov + 1,
                            _nome(k), acc.sigla))
        return out

    def voce(self, nome, programma, volume=100, pan=64, canale=None, pedale=False):
        """Una voce = un canale MIDI = una traccia SSEQ. pedale=True per un bordone o una nota
        tenuta sotto accordi diversi: note_estranee() non la controlla."""
        usati = {v.canale for v in self.voci}
        if canale is None:
            canale = next(c for c in range(16) if c not in usati)
        if canale in usati or not 0 <= canale <= 15:
            raise NotaErrata('canale %r già usato o fuori da 0-15' % canale)
        v = Voce(self, nome, canale, programma, volume, pan)
        v.pedale = pedale
        self.voci.append(v)
        return v

    def eco(self, sorgente, nome, ritardo, volume=45, pan=None, trasponi=0, vel=None, programma=None):
        """Voce che ripete le note di un'altra in ritardo (l'eco dei brani di HeartGold);
        con ritardo 0 e un altro programma è un raddoppio (anche all'ottava, con trasponi)."""
        v = self.voce(nome, programma if programma is not None else sorgente.programma, volume,
                      pan if pan is not None else 128 - sorgente.pan)
        v.copia_di = sorgente.nome
        if programma is None:
            v.ctrl = [c for c in sorgente.ctrl]
        for t, k, vv, d in sorgente.note:
            v.nota(t + ritardo, k + trasponi, vel or vv, d)
        return v

    def ripeti(self, da, battute, a, trasponi=0):
        """Copia le battute [da, da+battute) di tutte le voci dalla battuta a, trasposte di
        trasponi semitoni (la batteria resta com'è): la seconda passata in un'altra tonalità.
        L'armonia trasposta si registra anche lei, per note_estranee()."""
        for v in self.voci:
            v.copia(da, battute, a, trasponi=trasponi if v.intonata else 0)
        t0, t1 = int(round(da * self.battuta)), int(round((da + battute) * self.battuta))
        off = int(round(a * self.battuta)) - t0
        for t, (f, acc) in list(self.armonia.items()):
            if t0 <= t < t1:
                self.armonia[t + off] = (f + off, acc.trasposto(trasponi))

    def tempo(self, battuta, bpm):
        self.tempi.append((int(round(battuta * self.battuta)), bpm))

    def ritornello(self, da, a):
        """Ritornello dalle battute da (compresa) ad a (esclusa)."""
        self.loop = (da, a)

    def fine_a(self, battuta):
        """Fine del brano che non si ripete."""
        self.durata = battuta

    def fine(self):
        mw = self.A.MidiWriter(self.ppq)
        t0 = mw.track('tempo')
        for t, bpm in sorted(self.tempi):
            mw.tempo(t0, t, bpm)
        lim = None
        if self.loop:
            mw.loop(t0, self.loop[0] * self.battuta, self.loop[1] * self.battuta)
            lim = self.loop[1] * self.battuta
        elif self.durata:
            lim = self.durata * self.battuta
        info = []
        for v in self.voci:
            k = mw.track(v.nome)
            ch = v.canale
            mw.program(k, 0, ch, v.programma)
            mw.cc(k, 0, ch, 7, v.volume)
            mw.cc(k, 0, ch, 10, v.pan)
            for t, num, val in sorted(v.ctrl, key=lambda c: c[0]):
                if lim is not None and t >= lim:
                    continue
                if num == 'pc':
                    mw.program(k, t, ch, val)
                else:
                    mw.cc(k, t, ch, num, val)
            note = sorted(set(v.note))
            n = 0
            for t, key, vel, dur in note:
                if lim is not None:
                    if t >= lim:
                        continue
                    dur = min(dur, lim - t)
                mw.note(k, t, ch, key, vel, dur)
                n += 1
            keys = [x[1] for x in note]
            melodica = (not v.su_giro and v.copia_di is None and v.intonata and not v.pedale
                        and bool(self.armonia))
            info.append({'nome': v.nome, 'canale': ch, 'programma': v.programma, 'volume': v.volume,
                         'pan': v.pan, 'note': n, 'copia_di': v.copia_di, 'su_giro': v.su_giro,
                         'pedale': v.pedale,
                         'estranee': [list(e) for e in self.note_estranee(v)] if melodica else None,
                         'programmi': sorted({v.programma} | {c[2] for c in v.ctrl if c[1] == 'pc'}),
                         'registro': (min(keys), max(keys)) if keys else None})
        mw.trinacria = {'bpm': self.bpm, 'tempi': sorted(self.tempi), 'metro': self.metro,
                        'battuta': self.battuta, 'ritornello': self.loop, 'durata': self.durata,
                        'voci': info}
        mw.brano = self
        return mw
