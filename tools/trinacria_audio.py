#!/usr/bin/env python3
"""Strumento audio di Pokémon Trinacria (Modulo 5, blocco 5.1).

Legge e riscrive l'archivio audio di HeartGold (files/data/sound/gs_sound_data.sdat),
converte un file MIDI (SMF 0/1) in una sequenza SSEQ e la mette al posto dei dati
di uno slot SEQ_* esistente e del suo gemello SEQ_GS_P_* («suoni GB»).
Solo libreria standard di Python (3.8+).

Comandi:
  --selftest                         collaudo completo (SELFTEST_OK)
  info     --sdat F                  conteggi dell'archivio
  slot     --sdat F SEQ_X [...]      dati di uno o più slot (banco, volume, lettore, byte)
  banco    --sdat F BANK_X           strumenti di un banco SBNK
  mid2sseq IN.mid OUT.sseq           conversione MIDI -> SSEQ (con controllo)
  sseq2mid --sdat F SEQ_X OUT.mid    sequenza HeartGold -> MIDI (per studiarla)
  txt      (--sdat F SEQ_X | IN.sseq) disassemblato della sequenza
  onde     --sdat F BANK_X --out DIR  onde del banco in WAV (per ascoltare gli strumenti)
  catalogo --sdat F --out F.json      catalogo dei banchi musicali
  applica  --manifesto M [--hg H] [--out G]
                                     archivio di Trinacria: ogni brano del manifesto
                                     al posto dello slot e del suo gemello GB
  controlla --sdat F [--manifesto M] [--hg H]
                                     confronta un archivio modificato con l'originale
Senza --sdat si usa files/data/sound/gs_sound_data.sdat del repository (--repo o
TRINACRIA_REPO); l'originale è --hg, oppure files/data/sound/gs_sound_data_hg.sdat.
Ultima riga: AUDIO_OK / AUDIO_FAILED (SELFTEST_OK / SELFTEST_FAILED); ogni problema è
una riga "ERRORE <codice> <messaggio>". Documento: docs/MODULO_5/5.1_PIPELINE_E_SFX.md.
"""
import argparse
import json
import os
import re
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

# --------------------------------------------------------------------------- binario

def u16(b, o):
    return struct.unpack_from('<H', b, o)[0]


def u32(b, o):
    return struct.unpack_from('<I', b, o)[0]


def s16(b, o):
    return struct.unpack_from('<h', b, o)[0]


def align(n, a):
    return (n + a - 1) // a * a


class AudioError(Exception):
    pass


# --------------------------------------------------------------------------- SDAT

REC_NAMES = ['SEQ', 'SEQARC', 'BANK', 'WAVEARC', 'PLAYER', 'GROUP', 'PLAYER2', 'STRM']
FILE_ALIGN = 0x20


class Sdat:
    """Archivio SDAT. I blocchi SYMB e INFO restano byte per byte com'erano:
    le voci INFO hanno lunghezza fissa e si modificano sul posto. Si riscrivono
    solo FAT e FILE, con la stessa disposizione dell'originale."""

    def __init__(self, data):
        self.raw = bytes(data)
        b = self.raw
        if b[:4] != b'SDAT':
            raise AudioError('non è un file SDAT')
        self.header_size = u16(b, 0x0C)
        nblocks = u16(b, 0x0E)
        self.symb_off, self.symb_size = u32(b, 0x10), u32(b, 0x14)
        self.info_off, self.info_size = u32(b, 0x18), u32(b, 0x1C)
        self.fat_off, self.fat_size = u32(b, 0x20), u32(b, 0x24)
        self.file_off, self.file_size = u32(b, 0x28), u32(b, 0x2C)
        if nblocks != 4 or self.symb_off == 0:
            raise AudioError('SDAT senza blocco SYMB: nomi non disponibili')
        self.names = self._read_symb()
        self.info = bytearray(b[self.info_off:self.info_off + self.info_size])
        self.entries = self._read_info()
        self.fat = []
        n = u32(b, self.fat_off + 8)
        for i in range(n):
            o = self.fat_off + 12 + 16 * i
            self.fat.append((u32(b, o), u32(b, o + 4)))
        self.files = [b[o:o + s] for o, s in self.fat]
        self.index = {}
        for kind, names in self.names.items():
            for i, nm in enumerate(names):
                if nm:
                    self.index[nm] = (kind, i)

    # --- SYMB
    def _read_symb(self):
        b, base = self.raw, self.symb_off
        out = {}
        for r, kind in enumerate(REC_NAMES):
            ro = u32(b, base + 8 + 4 * r)
            if ro == 0:
                out[kind] = []
                continue
            cnt = u32(b, base + ro)
            names = []
            step = 8 if kind == 'SEQARC' else 4
            for i in range(cnt):
                no = u32(b, base + ro + 4 + step * i)
                names.append(self._cstr(base + no) if no else None)
            out[kind] = names
        return out

    def _cstr(self, o):
        e = self.raw.index(b'\0', o)
        return self.raw[o:e].decode('ascii')

    # --- INFO
    def _read_info(self):
        b = self.info
        out = {}
        for r, kind in enumerate(REC_NAMES):
            ro = u32(b, 8 + 4 * r)
            cnt = u32(b, ro)
            lst = []
            for i in range(cnt):
                eo = u32(b, ro + 4 + 4 * i)
                lst.append(eo if eo else None)
            out[kind] = lst
        return out

    def seq_info(self, i):
        eo = self.entries['SEQ'][i]
        if eo is None:
            return None
        b = self.info
        return {'file': u16(b, eo), 'banco': u16(b, eo + 4), 'volume': b[eo + 6],
                'prio_canale': b[eo + 7], 'prio_lettore': b[eo + 8], 'lettore': b[eo + 9]}

    def set_seq_info(self, i, banco=None, volume=None):
        eo = self.entries['SEQ'][i]
        if banco is not None:
            struct.pack_into('<H', self.info, eo + 4, banco)
        if volume is not None:
            self.info[eo + 6] = volume

    def bank_info(self, i):
        eo = self.entries['BANK'][i]
        if eo is None:
            return None
        b = self.info
        return {'file': u16(b, eo), 'wavearc': [u16(b, eo + 4 + 2 * k) for k in range(4)]}

    def wavearc_info(self, i):
        eo = self.entries['WAVEARC'][i]
        if eo is None:
            return None
        return {'file': u32(self.info, eo) & 0xFFFFFF}

    def player_info(self, i):
        eo = self.entries['PLAYER'][i]
        if eo is None:
            return None
        b = self.info
        return {'max_seq': b[eo], 'canali': u16(b, eo + 2), 'heap': u32(b, eo + 4)}

    def group(self, i):
        eo = self.entries['GROUP'][i]
        if eo is None:
            return []
        b = self.info
        cnt = u32(b, eo)
        out = []
        for k in range(cnt):
            o = eo + 4 + 8 * k
            out.append((b[o], b[o + 1], u32(b, o + 4)))  # tipo, flag di carico, indice
        return out

    def name(self, kind, i):
        lst = self.names[kind]
        return lst[i] if i < len(lst) and lst[i] else '%s_%d' % (kind, i)

    def seq_index(self, nome):
        k = self.index.get(nome)
        if not k or k[0] != 'SEQ':
            raise AudioError('sequenza sconosciuta: %s' % nome)
        return k[1]

    def bank_index(self, nome):
        k = self.index.get(nome)
        if not k or k[0] != 'BANK':
            raise AudioError('banco sconosciuto: %s' % nome)
        return k[1]

    def seq_data(self, i):
        return self.files[self.seq_info(i)['file']]

    def bank_data(self, i):
        return self.files[self.bank_info(i)['file']]

    def bank_load_size(self, i):
        """Byte del banco più quelli dei suoi archivi d'onda (ciò che va nell'heap)."""
        bi = self.bank_info(i)
        tot = len(self.files[bi['file']])
        for w in bi['wavearc']:
            if w != 0xFFFF:
                tot += len(self.files[self.wavearc_info(w)['file']])
        return tot

    # --- scrittura
    def add_file(self, data):
        """Aggiunge un file in coda (FAT e FILE crescono). Ritorna il suo numero."""
        self.files.append(bytes(data))
        return len(self.files) - 1

    def build(self):
        """Riscrive l'archivio: SYMB e INFO al loro posto, poi FAT e FILE. I file
        restano nell'ordine dell'originale (per offset), quelli aggiunti in coda,
        ognuno allineato a 32 byte come in HeartGold. Senza modifiche il risultato
        è identico byte per byte all'originale."""
        b = self.raw
        nfiles = len(self.files)
        norig = len(self.fat)
        out = bytearray(b[:self.fat_off])
        out[self.info_off:self.info_off + self.info_size] = self.info
        fat = bytearray(b[self.fat_off:self.fat_off + 12]) + bytearray(16 * nfiles)
        struct.pack_into('<II', fat, 4, len(fat), nfiles)
        file_off = self.fat_off + len(fat)
        hdr = bytearray(b[self.file_off:self.file_off + 0x10])
        struct.pack_into('<I', hdr, 8, nfiles)
        order = sorted(range(norig), key=lambda k: (self.fat[k][0], k)) + list(range(norig, nfiles))
        body = bytearray(hdr)
        for k in order:
            pos = file_off + len(body)
            body += b'\0' * (align(pos, FILE_ALIGN) - pos)
            struct.pack_into('<I', fat, 12 + 16 * k, file_off + len(body))
            struct.pack_into('<I', fat, 16 + 16 * k, len(self.files[k]))
            body += self.files[k]
        pos = file_off + len(body)
        body += b'\0' * (align(pos, FILE_ALIGN) - pos)
        struct.pack_into('<I', body, 4, len(body))
        out += fat + body
        struct.pack_into('<I', out, 0x08, len(out))
        struct.pack_into('<IIII', out, 0x20, self.fat_off, len(fat), file_off, len(body))
        return bytes(out)


def gb_twins(repo):
    """Coppie (DS, GB) della tabella di asm/unk_02004A44.s."""
    path = os.path.join(repo, 'asm', 'unk_02004A44.s')
    pairs = []
    with open(path, encoding='utf-8') as f:
        for line in f:
            m = re.match(r'\s*\.short (SEQ_\w+), (SEQ_\w+)\s*$', line)
            if m:
                pairs.append((m.group(1), m.group(2)))
    return pairs


def add_aliases(sd, repo):
    """Nomi di include/constants/sndseq.h che il decomp ha cambiato rispetto al
    blocco SYMB (per esempio SEQ_SE_DP_THROW = SEQ_SE_DP_NAGERU): diventano alias.
    Ritorna le coppie (nome del decomp, nome dell'archivio)."""
    out = []
    for nm, v in sndseq_values(repo).items():
        if nm in sd.index or v >= len(sd.entries['SEQ']) or sd.entries['SEQ'][v] is None:
            continue
        sd.index[nm] = ('SEQ', v)
        out.append((nm, sd.name('SEQ', v)))
    return out


def sndseq_values(repo):
    vals = {}
    with open(os.path.join(repo, 'include', 'constants', 'sndseq.h'), encoding='utf-8') as f:
        for line in f:
            m = re.match(r'#define (SEQ_\w+)\s+(\d+)\s*$', line)
            if m:
                vals[m.group(1)] = int(m.group(2))
    return vals


# --------------------------------------------------------------------------- SSEQ

TPQ = 48            # tick per semiminima delle sequenze Nitro
SSEQ_DATA = 0x1C    # inizio dei comandi nel file SSEQ

# Argomenti dei comandi: 'v' varlen, 'b' u8, 'c' s8, 'h' s16, 'H' u16, 't' u24
ARGS = {0x80: 'v', 0x81: 'v', 0x93: 'bt', 0x94: 't', 0x95: 't',
        0xE0: 'h', 0xE1: 'H', 0xE3: 'h', 0xFC: '', 0xFD: '', 0xFE: 'H', 0xFF: ''}
for _c in range(0xB0, 0xBE):
    ARGS[_c] = 'bh'
for _c in range(0xC0, 0xD8):
    ARGS[_c] = 'c' if _c in (0xC3, 0xC4) else 'b'

CMD_NAMES = {0x80: 'wait', 0x81: 'prg', 0x93: 'opentrack', 0x94: 'jump', 0x95: 'call',
             0xA0: 'random', 0xA1: 'var', 0xA2: 'if', 0xB0: 'setvar', 0xB1: 'addvar',
             0xB2: 'subvar', 0xB3: 'mulvar', 0xB4: 'divvar', 0xB5: 'shiftvar', 0xB6: 'randvar',
             0xB8: 'cmp_eq', 0xB9: 'cmp_ge', 0xBA: 'cmp_gt', 0xBB: 'cmp_le', 0xBC: 'cmp_lt',
             0xBD: 'cmp_ne', 0xC0: 'pan', 0xC1: 'volume', 0xC2: 'main_volume', 0xC3: 'transpose',
             0xC4: 'pitchbend', 0xC5: 'bendrange', 0xC6: 'prio', 0xC7: 'notewait', 0xC8: 'tie',
             0xC9: 'porta', 0xCA: 'mod_depth', 0xCB: 'mod_speed', 0xCC: 'mod_type',
             0xCD: 'mod_range', 0xCE: 'porta_sw', 0xCF: 'porta_time', 0xD0: 'attack',
             0xD1: 'decay', 0xD2: 'sustain', 0xD3: 'release', 0xD4: 'loop_start',
             0xD5: 'volume2', 0xD6: 'printvar', 0xD7: 'mute', 0xE0: 'mod_delay', 0xE1: 'tempo',
             0xE3: 'sweep_pitch', 0xFC: 'loop_end', 0xFD: 'ret', 0xFE: 'alloctrack', 0xFF: 'fin'}


def read_var(b, pc):
    v = 0
    for _ in range(4):
        c = b[pc]
        pc += 1
        v = (v << 7) | (c & 0x7F)
        if not c & 0x80:
            return v, pc
    raise AudioError('varlen troppo lungo a 0x%X' % pc)


def write_var(v):
    if v < 0 or v >= 1 << 28:
        raise AudioError('valore varlen fuori intervallo: %d' % v)
    out = [v & 0x7F]
    v >>= 7
    while v:
        out.append(0x80 | (v & 0x7F))
        v >>= 7
    return bytes(reversed(out))


def _read_args(b, pc, kinds):
    vals = []
    for k in kinds:
        if k == 'v':
            v, pc = read_var(b, pc)
        elif k == 'b':
            v, pc = b[pc], pc + 1
        elif k == 'c':
            v, pc = struct.unpack_from('<b', b, pc)[0], pc + 1
        elif k == 'h':
            v, pc = s16(b, pc), pc + 2
        elif k == 'H':
            v, pc = u16(b, pc), pc + 2
        elif k == 't':
            v, pc = b[pc] | b[pc + 1] << 8 | b[pc + 2] << 16, pc + 3
        vals.append(v)
    return vals, pc


def kinds_of(cmd):
    if cmd < 0x80:
        return 'bv'                      # velocità, durata
    if cmd not in ARGS:
        raise AudioError('comando SSEQ sconosciuto 0x%02X' % cmd)
    return ARGS[cmd]


def decode(b, pc):
    """Un comando a pc (offset nei dati). Ritorna (cmd, args, prefisso, pc_dopo).
    prefisso: None, ('random', min, max), ('var', n) o ('if',)."""
    cmd = b[pc]
    pc += 1
    if cmd in (0xA0, 0xA1, 0xA2):
        sub = b[pc]
        pc += 1
        kinds = kinds_of(sub)
        if cmd == 0xA2:
            args, pc = _read_args(b, pc, kinds)
            return sub, args, ('if',), pc
        args, pc = _read_args(b, pc, kinds[:-1])
        if cmd == 0xA0:
            (lo, hi), pc = _read_args(b, pc, 'hh')
            return sub, args + [lo], ('random', lo, hi), pc
        (n,), pc = _read_args(b, pc, 'b')
        return sub, args + [0], ('var', n), pc
    args, pc = _read_args(b, pc, kinds_of(cmd))
    return cmd, args, None, pc


def sseq_body(f):
    if f[:4] != b'SSEQ':
        raise AudioError('non è un file SSEQ')
    return f[u32(f, 0x18):]


def disasm(f):
    b = sseq_body(f)
    starts = {0: 'traccia 0'}
    out = []
    pc = 0
    labels = set()
    # prima passata: etichette
    while pc < len(b):
        try:
            cmd, args, pre, nxt = decode(b, pc)
        except (AudioError, IndexError):
            break
        if cmd == 0x93:
            starts[args[1]] = 'traccia %d' % args[0]
        if cmd in (0x94, 0x95):
            labels.add(args[0])
        pc = nxt
    pc = 0
    while pc < len(b):
        if pc in starts:
            out.append('; ---- %s' % starts[pc])
        try:
            cmd, args, pre, nxt = decode(b, pc)
        except (AudioError, IndexError):
            out.append('%06X  db %s' % (pc, b[pc:].hex(' ')))
            break
        if cmd < 0x80:
            txt = 'note %s v%d d%d' % (note_name(cmd), args[0], args[1])
        else:
            nm = CMD_NAMES.get(cmd, '0x%02X' % cmd)
            if cmd in (0x94, 0x95):
                txt = '%s L_%06X' % (nm, args[0])
            elif cmd == 0x93:
                txt = '%s %d L_%06X' % (nm, args[0], args[1])
            elif cmd == 0xFE:
                txt = '%s 0x%04X' % (nm, args[0])
            else:
                txt = ' '.join([nm] + [str(a) for a in args])
        if pre:
            txt = '%s(%s) %s' % (pre[0], ','.join(str(x) for x in pre[1:]), txt)
        lab = 'L_%06X:' % pc if pc in labels else ''
        out.append('%06X %-10s %s' % (pc, lab, txt))
        pc = nxt
    return '\n'.join(out)


NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']


def note_name(k):
    return '%s%d' % (NOTE_NAMES[k % 12], k // 12 - 1)


# --- esecuzione simulata

# comandi di controllo che la simulazione registra (e che il convertitore sa scrivere)
CTRL_CMDS = (0xC0, 0xC1, 0xC2, 0xC4, 0xC5, 0xC6, 0xC8, 0xC9, 0xCA, 0xCB, 0xCC, 0xCD,
             0xCE, 0xCF, 0xD0, 0xD1, 0xD2, 0xD3, 0xD5, 0xE0, 0xE3)

MAX_TICKS = TPQ * 4 * 2000


class Track:
    def __init__(self, n, pc):
        self.n, self.pc = n, pc
        self.t = 0
        self.notes = []          # (t, key, vel, dur, prg, ordine)
        self.ctrls = []          # (t, cmd, valore, ordine); 0x81 = cambio di programma
        self.tempi = []          # (t, bpm)
        self.prg = 0
        self.transpose = 0
        self.notewait = True
        self.loop = None         # (t_inizio, t_fine) del ritornello
        self.end = None
        self.stack = []          # ritorni delle call
        self.loops = []          # (pc, contatore) dei loop_start
        self.first_t = {}        # pc -> tempo della prima esecuzione
        self.stats = {}
        self.cond = False


def simulate(f, max_ticks=MAX_TICKS):
    """Esegue la sequenza fino al ritornello (salto all'indietro) o alla fine di
    ogni traccia. Ritorna l'elenco delle tracce con note e controlli."""
    b = sseq_body(f)
    tracks = [Track(0, 0)]
    variables = [0] * 32
    k = 0
    while k < len(tracks):
        tr = tracks[k]
        k += 1
        steps = 0
        while tr.end is None:
            steps += 1
            if steps > 200000 or tr.t > max_ticks:
                raise AudioError('traccia %d: nessuna fine né ritornello' % tr.n)
            pc0 = tr.pc
            if pc0 not in tr.first_t:
                tr.first_t[pc0] = tr.t
            cmd, args, pre, tr.pc = decode(b, pc0)
            key = CMD_NAMES.get(cmd, 'note') if cmd >= 0x80 else 'note'
            if pre:
                key = pre[0] + ':' + key
            tr.stats[key] = tr.stats.get(key, 0) + 1
            if pre and pre[0] == 'if' and not tr.cond:
                continue
            if pre and pre[0] == 'random':
                args[-1] = pre[1]
            if pre and pre[0] == 'var':
                args[-1] = variables[pre[1]]
            if cmd < 0x80:
                vel, dur = args
                tr.notes.append((tr.t, cmd + tr.transpose, vel, dur, tr.prg, steps))
                if tr.notewait:
                    tr.t += dur
            elif cmd == 0x80:
                tr.t += args[0]
            elif cmd == 0x81:
                tr.prg = args[0]
                tr.ctrls.append((tr.t, 0x81, args[0], steps))
            elif cmd == 0x93:
                if tr.n != 0:
                    raise AudioError('opentrack fuori dalla traccia 0')
                tracks.append(Track(args[0], args[1]))
            elif cmd == 0x94:
                dst = args[0]
                if dst in tr.first_t:
                    tr.loop = (tr.first_t[dst], tr.t)
                    tr.end = tr.t
                else:
                    tr.pc = dst
            elif cmd == 0x95:
                tr.stack.append(tr.pc)
                tr.pc = args[0]
            elif cmd == 0xFD:
                if not tr.stack:
                    raise AudioError('ret senza call')
                tr.pc = tr.stack.pop()
            elif cmd == 0xD4:
                tr.loops.append([tr.pc, args[0]])
            elif cmd == 0xFC:
                if not tr.loops:
                    raise AudioError('loop_end senza loop_start')
                lp = tr.loops[-1]
                if lp[1] == 0:                       # ripetizione infinita
                    tr.loop = (tr.first_t[lp[0]], tr.t)
                    tr.end = tr.t
                else:
                    lp[1] -= 1
                    if lp[1] > 0:
                        tr.pc = lp[0]
                    else:
                        tr.loops.pop()
            elif cmd == 0xFF:
                tr.end = tr.t
            elif cmd == 0xE1:
                tr.tempi.append((tr.t, args[0]))
            elif cmd == 0xC3:
                tr.transpose = args[0]
            elif cmd == 0xC7:
                tr.notewait = bool(args[0])
            elif cmd in CTRL_CMDS:
                tr.ctrls.append((tr.t, cmd, args[0], steps))
            elif 0xB0 <= cmd <= 0xBD:
                n, v = args
                x = variables[n]
                if cmd == 0xB0:
                    variables[n] = v
                elif cmd == 0xB1:
                    variables[n] = x + v
                elif cmd == 0xB2:
                    variables[n] = x - v
                elif cmd == 0xB3:
                    variables[n] = x * v
                elif cmd == 0xB4:
                    variables[n] = int(x / v) if v else x
                elif cmd == 0xB5:
                    variables[n] = x << v if v >= 0 else x >> -v
                elif cmd == 0xB6:
                    variables[n] = 0
                elif cmd >= 0xB8:
                    tr.cond = {0xB8: x == v, 0xB9: x >= v, 0xBA: x > v, 0xBB: x <= v,
                               0xBC: x < v, 0xBD: x != v}[cmd]
            # 0xFE, 0xD6, 0xD7: nessun effetto sul tempo
    tracks.sort(key=lambda t: t.n)
    return tracks


def song_loop(tracks):
    """Ritornello comune a tutte le tracce che lo hanno, o None."""
    loops = set(t.loop for t in tracks if t.loop)
    return loops.pop() if len(loops) == 1 else (None if not loops else 'diversi')


def polyphony(tracks, kind_of=None, until=None):
    """Massimo numero di note contemporanee: totale e per tipo (kind_of(prg, key))."""
    ev = []
    for tr in tracks:
        for t, key, vel, dur, prg, _ in tr.notes:
            if vel == 0 or dur == 0 or (until is not None and t >= until):
                continue
            kd = kind_of(prg, key) if kind_of else 'pcm'
            ev.append((t, 1, kd))
            ev.append((t + dur, -1, kd))
    ev.sort(key=lambda e: (e[0], e[1]))
    cur, best = {}, {}
    tot = mx = 0
    for t, d, kd in ev:
        cur[kd] = cur.get(kd, 0) + d
        tot += d
        best[kd] = max(best.get(kd, 0), cur[kd])
        mx = max(mx, tot)
    best['totale'] = mx
    return best


# --- scrittura

def encode_cmd(c):
    """Byte di un comando ('note', key, vel, dur) o (cmd, [args])."""
    out = bytearray()
    if c[0] == 'note':
        _, key, vel, dur = c
        if not (0 <= key <= 127 and 0 <= vel <= 127):
            raise AudioError('nota fuori intervallo: %d/%d' % (key, vel))
        out.append(key)
        out.append(vel)
        out += write_var(dur)
        return bytes(out)
    cmd, args = c
    out.append(cmd)
    for kind, v in zip(ARGS[cmd], args):
        if kind == 'v':
            out += write_var(v)
        elif kind == 'b':
            if not 0 <= v <= 255:
                raise AudioError('argomento fuori intervallo: %02X %d' % (cmd, v))
            out.append(v)
        elif kind == 'c':
            if not -128 <= v <= 127:
                raise AudioError('argomento fuori intervallo: %02X %d' % (cmd, v))
            out += struct.pack('<b', v)
        elif kind == 'h':
            if not -32768 <= v <= 32767:
                raise AudioError('argomento fuori intervallo: %02X %d' % (cmd, v))
            out += struct.pack('<h', v)
        elif kind == 'H':
            if not 0 <= v <= 65535:
                raise AudioError('argomento fuori intervallo: %02X %d' % (cmd, v))
            out += struct.pack('<H', v)
    return bytes(out)


CALL_COST = 4           # byte di una call (0x95 + 3)
WINDOWS = (192, 128, 96, 64, 48, 32, 24, 16, 12, 8, 6, 4, 3)


def compress(cmds, prefix):
    """Raccoglie le serie di comandi ripetute in sottoprogrammi (call/ret, un solo
    livello: lo stack delle call di una traccia Nitro ha 3 posti). Il tempo non
    cambia: call e ret non durano."""
    body = list(cmds)
    subs = []
    while True:
        toks = [None if c[0] in ('label', 'jump', 'call') else encode_cmd(c) for c in body]
        n = len(toks)
        ids, tid = [], {}
        for tk in toks:
            ids.append(-1 if tk is None else tid.setdefault(tk, len(tid)))
        brk = [0]
        for x in ids:
            brk.append(brk[-1] + (x < 0))
        M, B = (1 << 61) - 1, 1000003
        h = [0]
        for x in ids:
            h.append((h[-1] * B + x + 2) % M)
        powB = [1]
        for _ in range(n):
            powB.append(powB[-1] * B % M)
        best = None
        for L in WINDOWS:
            if 2 * L > n:
                continue
            groups = {}
            for i in range(n - L + 1):
                if brk[i + L] - brk[i]:
                    continue
                key = (h[i + L] - h[i] * powB[L]) % M
                groups.setdefault(key, []).append(i)
            for pos in groups.values():
                if len(pos) < 2:
                    continue
                sel, end = [], -1
                for p in pos:
                    if p >= end:
                        sel.append(p)
                        end = p + L
                if len(sel) < 2:
                    continue
                size = sum(len(toks[k]) for k in range(sel[0], sel[0] + L))
                save = len(sel) * size - (len(sel) * CALL_COST + size + 1)
                if save > 0 and (best is None or save > best[0]):
                    best = (save, L, sel)
        if best is None:
            break
        save, L, sel = best
        ref = toks[sel[0]:sel[0] + L]
        sel = [p for p in sel if toks[p:p + L] == ref]         # contro le collisioni
        if len(sel) < 2:
            break
        name = '%s_sub%d' % (prefix, len(subs))
        subs.append((name, body[sel[0]:sel[0] + L]))
        for p in reversed(sel):
            body[p:p + L] = [('call', name)]
    out = body
    for name, seg in subs:
        out = out + [('label', name)] + seg + [(0xFD, [])]
    return out


def assemble(tracks_cmds):
    """tracks_cmds: per ogni traccia una lista di elementi
    ('label', nome) | ('jump', nome) | (cmd, [args]) | ('note', key, vel, dur).
    La traccia 0 riceve in testa alloctrack e gli opentrack."""
    n = len(tracks_cmds)
    if not 1 <= n <= 16:
        raise AudioError('servono da 1 a 16 tracce, non %d' % n)
    head = 3 + 5 * (n - 1)
    bodies, labels, fixups = [], [], []
    for cmds in tracks_cmds:
        out = bytearray()
        lab, fix = {}, []
        for c in cmds:
            if c[0] == 'label':
                lab[c[1]] = len(out)
            elif c[0] in ('jump', 'call'):
                out.append(0x94 if c[0] == 'jump' else 0x95)
                fix.append((len(out), c[1]))
                out += b'\0\0\0'
            else:
                out += encode_cmd(c)
        bodies.append(out)
        labels.append(lab)
        fixups.append(fix)
    starts, pos = [], head
    for bd in bodies:
        starts.append(pos)
        pos += len(bd)
    data = bytearray()
    data.append(0xFE)
    data += struct.pack('<H', (1 << n) - 1)
    for k in range(1, n):
        data += bytes([0x93, k]) + struct.pack('<I', starts[k])[:3]
    for k, bd in enumerate(bodies):
        for at, nm in fixups[k]:
            if nm not in labels[k]:
                raise AudioError('etichetta mancante: %s' % nm)
            bd[at:at + 3] = struct.pack('<I', starts[k] + labels[k][nm])[:3]
        data += bd
    while len(data) % 4:
        data.append(0)
    size = SSEQ_DATA + len(data)
    hdr = b'SSEQ' + struct.pack('<HHIHH', 0xFEFF, 0x0100, size, 0x10, 1)
    hdr += b'DATA' + struct.pack('<II', size - 0x10, SSEQ_DATA)
    return bytes(hdr + data)


# --------------------------------------------------------------------------- MIDI

# Convenzione Trinacria: controller MIDI <-> comando SSEQ (valore grezzo, 0-127).
CC_OF = {0xC0: 10, 0xC1: 7, 0xC2: 21, 0xC6: 20, 0xC8: 68, 0xC9: 84, 0xCA: 1, 0xCB: 16,
         0xCC: 17, 0xCD: 18, 0xCE: 65, 0xCF: 5, 0xD0: 73, 0xD1: 75, 0xD2: 79, 0xD3: 72,
         0xD5: 11}
CMD_OF = {v: k for k, v in CC_OF.items()}
CC14_OF = {0xE0: (19, 51, 0), 0xE3: (22, 54, 8192)}      # MSB, LSB, scostamento
LOOP_START = ('loopstart',)
LOOP_END = ('loopend',)


class MidiWriter:
    """Scrive un file MIDI di tipo 1. Tempi in tick (ppq a scelta, 48 di default).
    È l'API delle partiture del Modulo 5: nessuna libreria esterna."""

    def __init__(self, ppq=TPQ):
        self.ppq = ppq
        self.tracks = []

    def track(self, name=None):
        self.tracks.append([])
        k = len(self.tracks) - 1
        if name:
            self.meta(k, 0, 0x03, name.encode('utf-8'))
        return k

    def _add(self, k, t, prio, data):
        tr = self.tracks[k]
        tr.append((t, prio, len(tr), bytes(data)))

    def meta(self, k, t, kind, payload):
        self._add(k, t, 1, bytes([0xFF, kind]) + write_var(len(payload)) + payload)

    def tempo(self, k, t, bpm):
        us = int(round(60000000 / bpm))
        self.meta(k, t, 0x51, us.to_bytes(3, 'big'))

    def marker(self, k, t, text):
        self.meta(k, t, 0x06, text.encode('ascii'))

    def loop(self, k, start, end):
        self.marker(k, start, 'loopStart')
        self.marker(k, end, 'loopEnd')

    def cc(self, k, t, ch, num, val):
        self._add(k, t, 2, [0xB0 | ch, num, val])

    def program(self, k, t, ch, prg):
        """Programma SBNK (anche oltre 127: banco MIDI = prg // 128 su CC0)."""
        self.cc(k, t, ch, 0, prg >> 7)
        self._add(k, t, 2, [0xC0 | ch, prg & 0x7F])

    def bend(self, k, t, ch, value14):
        self._add(k, t, 2, [0xE0 | ch, value14 & 0x7F, value14 >> 7])

    def bend_range(self, k, t, ch, semitoni):
        for num, val in ((101, 0), (100, 0), (6, semitoni)):
            self.cc(k, t, ch, num, val)

    def note(self, k, t, ch, key, vel, dur):
        if vel < 1:
            raise AudioError('velocità 0 non è una nota')
        self._add(k, t, 2, [0x90 | ch, key, vel])
        # la fine di una nota va prima degli inizi nello stesso tick, tranne con durata 0
        self._add(k, t + dur, 3 if dur == 0 else 0, [0x80 | ch, key, 0])

    def data(self):
        out = b'MThd' + struct.pack('>IHHH', 6, 1, len(self.tracks), self.ppq)
        for tr in self.tracks:
            body = bytearray()
            last = 0
            for t, prio, idx, ev in sorted(tr):
                body += write_var(t - last) + ev
                last = t
            body += b'\x00\xFF\x2F\x00'
            out += b'MTrk' + struct.pack('>I', len(body)) + bytes(body)
        return out

    def save(self, path):
        with open(path, 'wb') as f:
            f.write(self.data())


def read_midi(data):
    """SMF 0/1. Ritorna (ppq, eventi) con eventi (tick, ordine, tipo, ...):
    ('on', ch, key, vel) ('off', ch, key) ('cc', ch, n, v) ('pc', ch, p)
    ('bend', ch, v14) ('tempo', us) ('marker', testo)."""
    if data[:4] != b'MThd':
        raise AudioError('non è un file MIDI')
    hl, fmt, ntrk, div = struct.unpack_from('>IHHH', data, 4)
    if div & 0x8000:
        raise AudioError('MIDI con tempo SMPTE non supportato')
    if fmt not in (0, 1):
        raise AudioError('MIDI di formato %d non supportato' % fmt)
    pos = 8 + hl
    events = []
    order = 0
    for _ in range(ntrk):
        while data[pos:pos + 4] != b'MTrk':
            if pos + 8 > len(data):
                raise AudioError('tracce MIDI mancanti')
            pos += 8 + struct.unpack_from('>I', data, pos + 4)[0]
        ln = struct.unpack_from('>I', data, pos + 4)[0]
        p, end = pos + 8, pos + 8 + ln
        pos = end
        t, status = 0, None
        while p < end:
            dt, p = read_var(data, p)
            t += dt
            b0 = data[p]
            if b0 == 0xFF:
                kind = data[p + 1]
                ln2, p = read_var(data, p + 2)
                payload = data[p:p + ln2]
                p += ln2
                if kind == 0x2F:
                    break
                if kind == 0x51:
                    events.append((t, order, 'tempo', int.from_bytes(payload, 'big')))
                elif kind in (0x01, 0x06, 0x07):
                    events.append((t, order, 'marker', payload.decode('latin-1')))
                order += 1
                continue
            if b0 in (0xF0, 0xF7):
                ln2, p = read_var(data, p + 1)
                p += ln2
                continue
            if b0 & 0x80:
                status = b0
                p += 1
            elif status is None:
                raise AudioError('running status senza stato')
            hi, ch = status & 0xF0, status & 0x0F
            if hi in (0xC0, 0xD0):
                a = data[p]
                p += 1
                if hi == 0xC0:
                    events.append((t, order, 'pc', ch, a))
            else:
                a, c = data[p], data[p + 1]
                p += 2
                if hi == 0x90 and c > 0:
                    events.append((t, order, 'on', ch, a, c))
                elif hi == 0x80 or hi == 0x90:
                    events.append((t, order, 'off', ch, a))
                elif hi == 0xB0:
                    events.append((t, order, 'cc', ch, a, c))
                elif hi == 0xE0:
                    events.append((t, order, 'bend', ch, a | c << 7))
            order += 1
    events.sort(key=lambda e: (e[0], e[1]))
    return div, events


def midi_to_sseq(data, avvisi=None, comprimi=True):
    """Converte un MIDI in SSEQ. Un canale MIDI usato = una traccia SSEQ (in ordine
    di canale). Ritorna (bytes, info)."""
    ppq, events = read_midi(data)

    def q(t):
        return (t * TPQ * 2 + ppq) // (2 * ppq)

    warn = avvisi if avvisi is not None else []
    loop_s = loop_e = None
    tempi = []
    per_ch = {}
    pending = {}
    rpn = {}
    msb14 = {}
    bank = {}
    for ev in events:
        t, order, kind = ev[0], ev[1], ev[2]
        if kind == 'marker':
            txt = ev[3].strip().lower()
            if txt == 'loopstart':
                loop_s = q(t)
            elif txt == 'loopend':
                loop_e = q(t)
            continue
        if kind == 'tempo':
            tempi.append((q(t), order, (0xE1, [int(round(60000000 / ev[3]))])))
            continue
        ch = ev[3]
        lst = per_ch.setdefault(ch, [])
        if kind == 'on':
            item = ['note', ev[4], ev[5], None, t]
            lst.append((q(t), order, item))
            pending.setdefault((ch, ev[4]), []).append(item)
        elif kind == 'off':
            pend = pending.get((ch, ev[4]))
            if not pend:
                warn.append('canale %d: fine nota %s senza inizio a %d' % (ch, note_name(ev[4]), t))
                continue
            item = pend.pop(0)
            on = item[4]
            dur = q(t) - q(on)
            if dur == 0 and t > on:
                dur = 1
            item[3] = dur
        elif kind == 'pc':
            lst.append((q(t), order, (0x81, [bank.get(ch, 0) * 128 + ev[4]])))
        elif kind == 'bend':
            v = (ev[4] - 8192) // 64
            lst.append((q(t), order, (0xC4, [max(-128, min(127, v))])))
        elif kind == 'cc':
            num, val = ev[4], ev[5]
            if num == 0:
                bank[ch] = val
            elif num == 101:
                rpn[ch] = (val, rpn.get(ch, (127, 127))[1])
            elif num == 100:
                rpn[ch] = (rpn.get(ch, (127, 127))[0], val)
            elif num == 6:
                if rpn.get(ch) == (0, 0):
                    lst.append((q(t), order, (0xC5, [val])))
            elif num in CMD_OF:
                lst.append((q(t), order, (CMD_OF[num], [val])))
            else:
                hit = False
                for cmd, (m, l, off) in CC14_OF.items():
                    if num == m:
                        msb14[(ch, cmd)] = val
                        hit = True
                    elif num == l:
                        v = (msb14.get((ch, cmd), 0) << 7 | val) - off
                        lst.append((q(t), order, (cmd, [v])))
                        hit = True
                if not hit and num not in (32, 38, 98, 99, 121, 123):
                    warn.append('canale %d: controller %d ignorato' % (ch, num))
    for (ch, key), pend in pending.items():
        for item in pend:
            warn.append('canale %d: nota %s senza fine' % (ch, note_name(key)))
            item[3] = 1
    if (loop_s is None) != (loop_e is None):
        raise AudioError('serve la coppia di marcatori loopStart e loopEnd')
    if loop_s is not None and loop_e <= loop_s:
        raise AudioError('loopEnd deve venire dopo loopStart')
    chans = sorted(c for c in per_ch if any(it[2][0] == 'note' for it in per_ch[c])
                   or per_ch[c])
    if not chans:
        raise AudioError('nessun evento sui canali MIDI')
    if len(chans) > 16:
        raise AudioError('più di 16 canali')
    out_tracks = []
    info = {'tracce': len(chans), 'canali': chans, 'ritornello': None, 'note': 0}
    for k, ch in enumerate(chans):
        items = list(per_ch[ch])
        if k == 0:
            items += tempi
        items.sort(key=lambda e: (e[0], e[1]))
        cmds = [(0xC7, [0])]
        cur = 0
        if loop_s is not None:
            items = [it for it in items if it[0] < loop_e]
        placed = False
        last_end = 0
        for t, order, it in items:
            if loop_s is not None and not placed and t >= loop_s:
                if loop_s > cur:
                    cmds.append((0x80, [loop_s - cur]))
                    cur = loop_s
                cmds.append(('label', 'ritornello'))
                placed = True
            if t > cur:
                cmds.append((0x80, [t - cur]))
                cur = t
            if it[0] == 'note':
                cmds.append(('note', it[1], it[2], it[3]))
                last_end = max(last_end, t + it[3])
                info['note'] += 1
            else:
                cmds.append(it)
        if loop_s is not None:
            if not placed:
                if loop_s > cur:
                    cmds.append((0x80, [loop_s - cur]))
                    cur = loop_s
                cmds.append(('label', 'ritornello'))
            if loop_e > cur:
                cmds.append((0x80, [loop_e - cur]))
            cmds.append(('jump', 'ritornello'))
        else:
            if last_end > cur:
                cmds.append((0x80, [last_end - cur]))
            cmds.append((0xFF, []))
        out_tracks.append(compress(cmds, 't%d' % k) if comprimi else cmds)
    if loop_s is not None:
        info['ritornello'] = (loop_s, loop_e)
    return assemble(out_tracks), info


def sseq_to_midi(f):
    """Sequenza SSEQ -> MIDI di tipo 1 (ppq 48), una traccia MIDI per traccia SSEQ,
    canale = numero della traccia. Il ritornello diventa loopStart/loopEnd."""
    tracks = simulate(f)
    mw = MidiWriter(TPQ)
    lp = song_loop(tracks)
    skipped = 0
    for tr in tracks:
        k = mw.track('traccia %d' % tr.n)
        ch = tr.n
        if k == 0:
            for t2 in tracks:
                for t, bpm in t2.tempi:
                    mw.tempo(0, t, bpm)
            if lp and lp != 'diversi':
                mw.loop(0, lp[0], lp[1])
        evs = [(t, o, 'c', cmd, v) for t, cmd, v, o in tr.ctrls]
        evs += [(t, o, 'n', key, vel, dur) for t, key, vel, dur, prg, o in tr.notes]
        evs.sort(key=lambda e: (e[0], e[1]))
        for e in evs:
            t = e[0]
            if e[2] == 'n':
                key, vel, dur = e[3:]
                if vel == 0:
                    skipped += 1
                    continue
                mw.note(k, t, ch, key, vel, dur)
                continue
            cmd, v = e[3], e[4]
            if cmd == 0x81:
                mw.program(k, t, ch, v)
            elif cmd == 0xC4:
                mw.bend(k, t, ch, 8192 + v * 64)
            elif cmd == 0xC5:
                mw.bend_range(k, t, ch, v)
            elif cmd in CC_OF:
                if v > 127:
                    raise AudioError('valore %d del comando %02X oltre 127' % (v, cmd))
                mw.cc(k, t, ch, CC_OF[cmd], v)
            elif cmd in CC14_OF:
                m, l, off = CC14_OF[cmd]
                x = v + off
                if not 0 <= x < 16384:
                    raise AudioError('valore %d del comando %02X fuori intervallo' % (v, cmd))
                mw.cc(k, t, ch, m, x >> 7)
                mw.cc(k, t, ch, l, x & 0x7F)
    return mw.data(), {'tracce': len(tracks), 'ritornello': lp, 'note_mute_saltate': skipped}


def timeline(tracks, until=None):
    """Note, controlli e tempi della prima passata, per confronti."""
    out = []
    for tr in tracks:
        notes = [(t, k, v, d, p) for t, k, v, d, p, _ in tr.notes
                 if v > 0 and (until is None or t < until)]
        ctr = [(t, c, v) for t, c, v, _ in sorted(tr.ctrls, key=lambda x: (x[0], x[3]))
               if until is None or t < until]
        if notes or ctr:
            out.append((notes, ctr))
    tempi = sorted((t, b) for tr in tracks for t, b in tr.tempi if until is None or t < until)
    return out, tempi


# --------------------------------------------------------------------------- SBNK e SWAR

INST_KIND = {0: None, 1: 'pcm', 2: 'psg', 3: 'rumore', 4: 'pcm', 5: None,
             16: 'batteria', 17: 'divisione'}


def _region(f, o):
    return {'tipo': None, 'swav': u16(f, o),
            'swar': u16(f, o + 2), 'nota_base': f[o + 4], 'adsr': list(f[o + 5:o + 9]),
            'pan': f[o + 9]}


def parse_sbnk(f):
    """Strumenti di un banco: lista di dict (None per i programmi vuoti).
    Ogni strumento ha 'tipo' e 'regioni' [(tasto_min, tasto_max, regione)]."""
    if f[:4] != b'SBNK':
        raise AudioError('non è un file SBNK')
    cnt = u32(f, 0x38)
    out = []
    for i in range(cnt):
        o = 0x3C + 4 * i
        typ, off = f[o], u16(f, o + 1)
        kind = INST_KIND.get(typ, '?')
        if kind is None:
            out.append(None)
            continue
        regs = []
        if typ in (1, 2, 3, 4):
            r = _region(f, off)
            r['tipo'] = kind
            regs.append((0, 127, r))
        elif typ == 16:
            lo, hi = f[off], f[off + 1]
            for k in range(hi - lo + 1):
                p = off + 2 + 12 * k
                r = _region(f, p + 2)
                r['tipo'] = INST_KIND.get(u16(f, p), '?')
                regs.append((lo + k, lo + k, r))
        elif typ == 17:
            tops = list(f[off:off + 8])
            lo = 0
            k = 0
            for top in tops:
                if top == 0:
                    break
                p = off + 8 + 12 * k
                r = _region(f, p + 2)
                r['tipo'] = INST_KIND.get(u16(f, p), '?')
                regs.append((lo, top, r))
                lo = top + 1
                k += 1
        else:
            raise AudioError('tipo di strumento sconosciuto %d (programma %d)' % (typ, i))
        out.append({'tipo': kind, 'regioni': regs})
    return out


def region_for(inst, key):
    for lo, hi, r in inst['regioni']:
        if lo <= key <= hi:
            return r
    return None


SWAV_FMT = {0: 'PCM8', 1: 'PCM16', 2: 'ADPCM'}


def parse_swar(f):
    if f[:4] != b'SWAR':
        raise AudioError('non è un file SWAR')
    cnt = u32(f, 0x38)
    offs = [u32(f, 0x3C + 4 * i) for i in range(cnt)] + [len(f)]
    out = []
    for i in range(cnt):
        o = offs[i]
        fmt, loop, rate = f[o], f[o + 1], u16(f, o + 2)
        lstart, llen = u16(f, o + 6), u32(f, o + 8)
        data = f[o + 12:offs[i + 1]] if i + 1 < cnt else f[o + 12:o + 12 + 4 * (lstart + llen)]
        data = data[:4 * (lstart + llen)]
        out.append({'formato': SWAV_FMT.get(fmt, '?'), 'loop': bool(loop), 'hz': rate,
                    'loop_inizio': lstart * 4, 'dati': data})
    return out


IMA_STEP = [7, 8, 9, 10, 11, 12, 13, 14, 16, 17, 19, 21, 23, 25, 28, 31, 34, 37, 41, 45,
            50, 55, 60, 66, 73, 80, 88, 97, 107, 118, 130, 143, 157, 173, 190, 209, 230,
            253, 279, 307, 337, 371, 408, 449, 494, 544, 598, 658, 724, 796, 876, 963,
            1060, 1166, 1282, 1411, 1552, 1707, 1878, 2066, 2272, 2499, 2749, 3024, 3327,
            3660, 4026, 4428, 4871, 5358, 5894, 6484, 7132, 7845, 8630, 9493, 10442, 11487,
            12635, 13899, 15289, 16818, 18500, 20350, 22385, 24623, 27086, 29794, 32767]
IMA_IDX = [-1, -1, -1, -1, 2, 4, 6, 8]


def swav_pcm16(w):
    """Campioni a 16 bit di un'onda (per l'ascolto)."""
    d = w['dati']
    if w['formato'] == 'PCM8':
        return [struct.unpack_from('<b', d, i)[0] * 256 for i in range(len(d))]
    if w['formato'] == 'PCM16':
        return list(struct.unpack_from('<%dh' % (len(d) // 2), d))
    pred, idx = s16(d, 0), min(88, d[2])
    out = []
    for byte in d[4:]:
        for nib in (byte & 0xF, byte >> 4):
            step = IMA_STEP[idx]
            diff = step >> 3
            if nib & 1:
                diff += step >> 2
            if nib & 2:
                diff += step >> 1
            if nib & 4:
                diff += step
            pred = max(-32768, min(32767, pred - diff if nib & 8 else pred + diff))
            idx = max(0, min(88, idx + IMA_IDX[nib & 7]))
            out.append(pred)
    return out


def wav_bytes(samples, hz):
    data = struct.pack('<%dh' % len(samples), *samples)
    return (b'RIFF' + struct.pack('<I', 36 + len(data)) + b'WAVEfmt ' +
            struct.pack('<IHHIIHH', 16, 1, 1, hz, hz * 2, 2, 16) + b'data' +
            struct.pack('<I', len(data)) + data)


# --------------------------------------------------------------------------- catalogo

HG_SHA1 = '1ea1ac174ea25f28a2446bee1b8b7be4d4ca1264'
MUSIC_BANK = re.compile(r'BANK_(BASIC|BGM_\w+)$')
PSG_CH = set(range(8, 14))
NOISE_CH = {14, 15}


def is_music_slot(name):
    return (name.startswith('SEQ_GS_') and not name.startswith('SEQ_GS_P_')
            and not name.startswith('SEQ_GS_SE_'))


def twin_of(sd, name):
    m = re.match(r'(SEQ_[A-Z]+_)(\w+)$', name)
    if not m or m.group(2).startswith('P_'):
        return None
    tw = m.group(1) + 'P_' + m.group(2)
    k = sd.index.get(tw)
    return tw if k and k[0] == 'SEQ' and sd.seq_info(k[1]) else None


def player_channels(sd, p):
    mask = sd.player_info(p)['canali']
    ch = {c for c in range(16) if mask >> c & 1}
    return {'totale': len(ch), 'psg': len(ch & PSG_CH), 'rumore': len(ch & NOISE_CH)}


def kind_func(insts):
    def kind_of(prg, key):
        inst = insts[prg] if prg < len(insts) else None
        if inst is None:
            return 'vuoto'
        r = region_for(inst, key)
        if r is None:
            return 'fuori'
        return 'psg' if r['tipo'] == 'psg' else ('rumore' if r['tipo'] == 'rumore' else 'pcm')
    return kind_of


def player_limits(sd):
    """Per ogni lettore usato dalle musiche di HeartGold: il carico massimo
    (sequenza + banco + onde) e la sequenza più lunga."""
    lim = {}
    for i, nm in enumerate(sd.names['SEQ']):
        if not nm or not is_music_slot(nm) or not sd.seq_info(i):
            continue
        inf = sd.seq_info(i)
        p = sd.name('PLAYER', inf['lettore'])
        seq = len(sd.files[inf['file']])
        load = seq + sd.bank_load_size(inf['banco'])
        cur = lim.setdefault(p, {'carico_max': 0, 'carico_max_da': None, 'sseq_max': 0,
                                 'sseq_max_da': None})
        if load > cur['carico_max']:
            cur['carico_max'], cur['carico_max_da'] = load, nm
        if seq > cur['sseq_max']:
            cur['sseq_max'], cur['sseq_max_da'] = seq, nm
    for p, cur in lim.items():
        pi = sd.player_info(sd.index[p][1])
        cur['heap_lettore'] = pi['heap']
        cur['canali'] = player_channels(sd, sd.index[p][1])
    return lim


def check_song(sd, slot, sseq, banco, volume, lim, errs, where):
    """Controlli di un brano nuovo per uno slot. Aggiunge (codice, messaggio) a errs."""
    i = sd.seq_index(slot)
    inf = sd.seq_info(i)
    pname = sd.name('PLAYER', inf['lettore'])
    try:
        tracks = simulate(sseq)
    except AudioError as e:
        errs.append(('A02', '%s: sequenza non eseguibile: %s' % (where, e)))
        return None
    bi = sd.bank_index(banco)
    insts = parse_sbnk(sd.bank_data(bi))
    lp = song_loop(tracks)
    if lp == 'diversi':
        errs.append(('A10', '%s: le tracce hanno ritornelli diversi' % where))
    orig_loop = song_loop(simulate(sd.seq_data(i))) is not None
    if (lp is not None) != orig_loop:
        errs.append(('A10', '%s: %s' % (where, 'lo slot ripete il brano: servono i marcatori loopStart e loopEnd'
                                       if orig_loop else 'lo slot non si ripete: niente marcatori di ritornello')))
    bad = {}
    for tr in tracks:
        for t, key, vel, dur, prg, _ in tr.notes:
            if vel == 0:
                continue
            inst = insts[prg] if prg < len(insts) else None
            if inst is None:
                bad.setdefault(('vuoto', prg), key)
            elif region_for(inst, key) is None:
                bad.setdefault(('fuori', prg), key)
    for (why, prg), key in sorted(bad.items()):
        errs.append(('A05', '%s: programma %d di %s %s (nota %s)' % (
            where, prg, banco, 'vuoto o inesistente' if why == 'vuoto' else
            'non ha la nota', note_name(key))))
    poly = polyphony(tracks, kind_func(insts), until=lp[1] if lp and lp != 'diversi' else None)
    ch = lim[pname]['canali']
    if poly['totale'] > ch['totale']:
        errs.append(('A06', '%s: %d note insieme, il lettore %s ha %d canali' % (
            where, poly['totale'], pname, ch['totale'])))
    for k in ('psg', 'rumore'):
        if poly.get(k, 0) > ch[k]:
            errs.append(('A07', '%s: %d note %s insieme, il lettore %s ne ha %d' % (
                where, poly[k], k.upper() if k == 'psg' else 'di rumore', pname, ch[k])))
    heap = lim[pname]['heap_lettore']
    if heap and len(sseq) > heap:
        errs.append(('A08', '%s: sequenza di %d byte, heap del lettore %s = %d' % (
            where, len(sseq), pname, heap)))
    load = len(sseq) + sd.bank_load_size(bi)
    if load > lim[pname]['carico_max']:
        errs.append(('A09', '%s: carico %d byte (sequenza + %s), massimo di HeartGold su %s = %d (%s)' % (
            where, load, banco, pname, lim[pname]['carico_max'], lim[pname]['carico_max_da'])))
    if not 0 <= volume <= 127:
        errs.append(('A04', '%s: volume %d fuori da 0-127' % (where, volume)))
    return {'lettore': pname, 'polifonia': poly, 'ritornello': lp, 'byte': len(sseq),
            'carico': load, 'tracce': len(tracks)}


def load_song(path, avvisi):
    with open(path, 'rb') as f:
        data = f.read()
    if data[:4] == b'MThd':
        return midi_to_sseq(data, avvisi)[0]
    if data[:4] == b'SSEQ':
        return data
    raise AudioError('né MIDI né SSEQ: %s' % path)


def applica(hg_bytes, manifest, base_dir, strict_sha=True, repo=None):
    """Costruisce l'archivio di Trinacria dall'originale di HeartGold e dal manifesto.
    Ritorna (bytes, righe di rapporto, errori)."""
    errs, report = [], []
    if strict_sha:
        import hashlib
        if hashlib.sha1(hg_bytes).hexdigest() != HG_SHA1:
            errs.append(('A22', 'l\'archivio di partenza non è l\'originale di HeartGold (SHA-1)'))
            return None, report, errs
    sd = Sdat(hg_bytes)
    if repo:
        add_aliases(sd, repo)
    lim = player_limits(sd)
    plan, seen = [], {}
    for n, b in enumerate(manifest.get('brani', [])):
        where = 'brani[%d] %s' % (n, b.get('slot'))
        slot = b.get('slot', '')
        k = sd.index.get(slot)
        if not k or k[0] != 'SEQ' or not is_music_slot(slot):
            errs.append(('A01', '%s: non è uno slot musicale SEQ_GS_* di HeartGold' % where))
            continue
        if slot in seen:
            errs.append(('A11', '%s: slot già usato da brani[%d]' % (where, seen[slot])))
            continue
        seen[slot] = n
        inf = sd.seq_info(k[1])
        banco = b.get('banco') or sd.name('BANK', inf['banco'])
        if not MUSIC_BANK.match(banco) or banco not in sd.index:
            errs.append(('A03', '%s: %s non è un banco musicale (BANK_BASIC o BANK_BGM_*)' % (where, banco)))
            continue
        volume = b.get('volume', inf['volume'])
        avv = []
        try:
            sseq = load_song(os.path.join(base_dir, b.get('file', '')), avv)
        except (AudioError, OSError, IndexError, struct.error) as e:
            errs.append(('A02', '%s: %s' % (where, e)))
            continue
        for a in avv:
            errs.append(('A12', '%s: %s' % (where, a)))
        res = check_song(sd, slot, sseq, banco, volume, lim, errs, where)
        if res is None:
            continue
        plan.append((slot, twin_of(sd, slot), sseq, banco, volume, res))
    if errs:
        return None, report, errs
    redirected = set()
    for slot, twin, *_ in plan:
        redirected.add(sd.seq_index(slot))
        if twin:
            redirected.add(sd.seq_index(twin))
    users = {}
    for kind in ('SEQ', 'BANK', 'WAVEARC'):
        for i, eo in enumerate(sd.entries[kind]):
            if eo is None:
                continue
            fid = (sd.seq_info(i)['file'] if kind == 'SEQ' else sd.bank_info(i)['file']
                   if kind == 'BANK' else sd.wavearc_info(i)['file'])
            users.setdefault(fid, set()).add((kind, i))
    free = sorted(fid for fid, us in users.items()
                  if all(kd == 'SEQ' and i in redirected for kd, i in us))
    taken = set()
    for slot, twin, sseq, banco, volume, res in plan:
        si = sd.seq_index(slot)
        cands = [sd.seq_info(si)['file']]
        if twin:
            cands.append(sd.seq_info(sd.seq_index(twin))['file'])
        cands += free
        fid = next((c for c in cands if c in free and c not in taken), None)
        if fid is None:
            fid = sd.add_file(sseq)
        taken.add(fid)
        sd.files[fid] = sseq
        bnk = sd.bank_index(banco)
        for s in (si, sd.seq_index(twin) if twin else None):
            if s is None:
                continue
            struct.pack_into('<H', sd.info, sd.entries['SEQ'][s], fid)
            sd.set_seq_info(s, banco=bnk, volume=volume)
        report.append('%s%s -> file %d, %d byte, %s, volume %d, %d tracce, polifonia %d, carico %d' % (
            slot, (' + ' + twin) if twin else '', fid, len(sseq), banco, volume, res['tracce'],
            res['polifonia']['totale'], res['carico']))
    report.append('file nuovi in coda: %d' % (len(sd.files) - len(sd.fat)))
    return sd.build(), report, errs


def controlla(hg_bytes, new_bytes, manifest=None, base_dir='.'):
    """Confronta l'archivio di Trinacria con l'originale. Fuori dagli slot del
    manifesto (e dai loro gemelli) tutto deve essere identico: effetti, versi,
    jingle, banchi, onde, gruppi, lettori e le altre musiche. Ritorna gli errori."""
    errs = []
    a, b = Sdat(hg_bytes), Sdat(new_bytes)
    if a.raw[:8] != b.raw[:8] or a.names != b.names:
        errs.append(('A20', 'intestazione o nomi (SYMB) diversi dall\'originale'))
        return errs
    slots = set()
    if manifest is not None:
        for br in manifest.get('brani', []):
            s = br.get('slot')
            if s in a.index:
                slots.add(a.seq_index(s))
                tw = twin_of(a, s)
                if tw:
                    slots.add(a.seq_index(tw))
    for kind in REC_NAMES:
        for i, (ea, eb) in enumerate(zip(a.entries[kind], b.entries[kind])):
            if kind == 'SEQ' and i in slots:
                continue
            ra = rb = None
            if kind == 'SEQ' and ea is not None:
                ra, rb = bytes(a.info[ea:ea + 12]), bytes(b.info[eb:eb + 12])
                da, db = a.seq_data(i), b.seq_data(i)
            elif kind == 'BANK' and ea is not None:
                ra, rb = bytes(a.info[ea:ea + 12]), bytes(b.info[eb:eb + 12])
                da, db = a.bank_data(i), b.bank_data(i)
            elif kind == 'WAVEARC' and ea is not None:
                ra, rb = bytes(a.info[ea:ea + 4]), bytes(b.info[eb:eb + 4])
                da, db = a.files[a.wavearc_info(i)['file']], b.files[b.wavearc_info(i)['file']]
            else:
                continue
            if ra != rb or da != db:
                errs.append(('A20', '%s cambiato fuori dal manifesto' % a.name(kind, i)))
        if len(a.entries[kind]) != len(b.entries[kind]):
            errs.append(('A20', 'numero di voci %s diverso' % kind))
    ia, ib = bytearray(a.info), bytearray(b.info)
    for i in slots:
        eo = a.entries['SEQ'][i]
        ia[eo:eo + 2] = ib[eo:eo + 2]                    # file
        ia[eo + 4:eo + 7] = ib[eo + 4:eo + 7]            # banco, volume
    if ia != ib:
        errs.append(('A20', 'blocco INFO cambiato oltre file, banco e volume degli slot'))
    if manifest is not None:
        for br in manifest.get('brani', []):
            s = br.get('slot')
            if s not in a.index:
                continue
            avv = []
            try:
                want = load_song(os.path.join(base_dir, br.get('file', '')), avv)
            except (AudioError, OSError) as e:
                errs.append(('A21', '%s: %s' % (s, e)))
                continue
            for t in [s] + ([twin_of(a, s)] if twin_of(a, s) else []):
                i = a.seq_index(t)
                inf = b.seq_info(i)
                if b.files[inf['file']] != want:
                    errs.append(('A21', '%s: i dati non sono il brano del manifesto' % t))
                if br.get('banco') and b.name('BANK', inf['banco']) != br['banco']:
                    errs.append(('A21', '%s: banco %s invece di %s' % (t, b.name('BANK', inf['banco']), br['banco'])))
                if 'volume' in br and inf['volume'] != br['volume']:
                    errs.append(('A21', '%s: volume %d invece di %d' % (t, inf['volume'], br['volume'])))
    return errs


def catalog(sd):
    """Banchi musicali con i loro strumenti e l'uso che ne fanno le musiche di
    HeartGold (sequenze, note più bassa e più alta, numero di note)."""
    use = {}
    for i, nm in enumerate(sd.names['SEQ']):
        if not nm or not is_music_slot(nm) or not sd.seq_info(i):
            continue
        bank = sd.name('BANK', sd.seq_info(i)['banco'])
        for tr in simulate(sd.seq_data(i)):
            for t, key, vel, dur, prg, _ in tr.notes:
                if vel == 0:
                    continue
                u = use.setdefault((bank, prg), {'sequenze': set(), 'min': 127, 'max': 0, 'note': 0})
                u['sequenze'].add(nm)
                u['min'] = min(u['min'], key)
                u['max'] = max(u['max'], key)
                u['note'] += 1
    basic = parse_sbnk(sd.bank_data(sd.bank_index('BANK_BASIC')))
    out = []
    for bi, bn in enumerate(sd.names['BANK']):
        if not bn or not MUSIC_BANK.match(bn):
            continue
        info = sd.bank_info(bi)
        insts = parse_sbnk(sd.bank_data(bi))
        swars = [w for w in info['wavearc']]
        waves = {}
        for k, w in enumerate(swars):
            if w != 0xFFFF:
                waves[k] = parse_swar(sd.files[sd.wavearc_info(w)['file']])
        progs = []
        for p, inst in enumerate(insts):
            if inst is None:
                continue
            regs = []
            for lo, hi, r in inst['regioni']:
                rr = {'tasti': [lo, hi], 'tipo': r['tipo'], 'nota_base': r['nota_base'],
                      'adsr': r['adsr'], 'pan': r['pan']}
                if r['tipo'] in ('pcm',):
                    arc = swars[r['swar']] if r['swar'] < 4 else 0xFFFF
                    rr['onda'] = '%s/%d' % (sd.name('WAVEARC', arc), r['swav'])
                    wv = waves.get(r['swar'], [])
                    if r['swav'] < len(wv):
                        w = wv[r['swav']]
                        nsamp = (len(w['dati']) - (4 if w['formato'] == 'ADPCM' else 0)) * (
                            2 if w['formato'] == 'ADPCM' else 1) // (2 if w['formato'] == 'PCM16' else 1)
                        rr['campione'] = {'formato': w['formato'], 'hz': w['hz'], 'loop': w['loop'],
                                          'ms': round(1000 * nsamp / w['hz']) if w['hz'] else 0}
                elif r['tipo'] == 'psg':
                    rr['duty'] = r['swav']
                regs.append(rr)
            u = use.get((bn, p))
            comune = p < len(basic) and basic[p] is not None and json.dumps(basic[p], sort_keys=True) == json.dumps(inst, sort_keys=True)
            entry = {'programma': p, 'tipo': inst['tipo'], 'comune': comune, 'regioni': regs}
            if u:
                entry['uso_heartgold'] = {'sequenze': sorted(u['sequenze']), 'nota_min': note_name(u['min']),
                                          'nota_max': note_name(u['max']), 'note': u['note']}
            progs.append(entry)
        users = sorted(n for i, n in enumerate(sd.names['SEQ'])
                       if n and sd.seq_info(i) and sd.seq_info(i)['banco'] == bi)
        out.append({'banco': bn, 'indice': bi, 'byte_carico': sd.bank_load_size(bi),
                    'archivi_onda': [sd.name('WAVEARC', w) for w in swars if w != 0xFFFF],
                    'programmi': progs, 'sequenze_heartgold': users})
    return out


def field_sounds(repo, sd):
    """Effetti, fanfare e versi che gli script di campo di HeartGold suonano già."""
    cnt = {'PlaySE': {}, 'PlayFanfare': {}, 'PlayCry': {}}
    d = os.path.join(repo, 'files', 'fielddata', 'script', 'scr_seq')
    for fn in sorted(os.listdir(d)):
        with open(os.path.join(d, fn), encoding='utf-8', errors='replace') as f:
            for line in f:
                m = re.match(r'\s*(PlaySE|PlayFanfare|PlayCry)\s+(\w+)', line)
                if m:
                    c = cnt[m.group(1)]
                    c[m.group(2)] = c.get(m.group(2), 0) + 1
    return cnt


# --------------------------------------------------------------------------- comandi

def default_repo():
    for c in (os.environ.get('TRINACRIA_REPO'), os.getcwd(),
              os.path.join(HERE, '..'), os.path.join(HERE, '..', '..'),
              os.path.join(HERE, '..', '..', 'pokeheartgold')):
        if c and os.path.isfile(os.path.join(c, 'include', 'constants', 'sndseq.h')):
            return os.path.abspath(c)
    return None


def sdat_path(repo):
    return os.path.join(repo, 'files', 'data', 'sound', 'gs_sound_data.sdat')


def read(path):
    with open(path, 'rb') as f:
        return f.read()


def write(path, data):
    d = os.path.dirname(os.path.abspath(path))
    os.makedirs(d, exist_ok=True)
    with open(path, 'wb') as f:
        f.write(data)


def print_errs(errs):
    for code, msg in errs:
        print('ERRORE %s %s' % (code, msg))


def hg_original(repo, path=None):
    """L'archivio originale: --hg, oppure gs_sound_data_hg.sdat accanto a quello
    del gioco, oppure gs_sound_data.sdat se è ancora quello di HeartGold."""
    import hashlib
    cands = [path] if path else [os.path.join(repo, 'files', 'data', 'sound', 'gs_sound_data_hg.sdat'),
                                 sdat_path(repo)]
    for c in cands:
        if c and os.path.isfile(c):
            data = read(c)
            if hashlib.sha1(data).hexdigest() == HG_SHA1:
                return data, c
    raise AudioError('archivio originale di HeartGold non trovato (SHA-1 %s): %s' % (HG_SHA1, cands))


# --------------------------------------------------------------------------- collaudo

def demo_song(seed=1, loop=True, notes=None, prg=0, ch_extra=True, ppq=96):
    """Brano di prova scritto con MidiWriter. Ritorna (bytes MIDI, note attese
    nel tempo SSEQ come (canale, t, key, vel, dur, prg))."""
    mw = MidiWriter(ppq)
    k0 = mw.track('prova')
    mw.tempo(k0, 0, 132)
    expect = []
    x = seed
    bar = ppq * 4
    for ch in ([0, 1, 9] if ch_extra else [0]):
        k = mw.track('canale %d' % ch)
        p = 39 if ch == 9 else prg + ch
        mw.program(k, 0, ch, p)
        mw.cc(k, 0, ch, 7, 100 - ch)
        mw.cc(k, 0, ch, 10, 64)
        if ch == 1:
            mw.bend_range(k, 0, ch, 2)
            mw.bend(k, bar, ch, 8192 + 64 * 10)
            mw.bend(k, bar + ppq, ch, 8192)
        n = notes if notes is not None else 32
        for i in range(n):
            x = (x * 1103515245 + 12345) & 0x7FFFFFFF
            t = i * ppq // 2
            key = (36 + x % 12) if ch == 9 else (48 + 12 * ch + x % 24)
            vel = 60 + x % 60
            dur = ppq // 2 - (x % 3) * ppq // 8
            mw.note(k, t, ch, key, vel, dur)
            expect.append((ch, t * TPQ // ppq, key, vel, dur * TPQ // ppq, p))
    if loop:
        mw.loop(k0, bar, bar * 4)
    return mw.data(), expect


def selftest(repo=None):
    import hashlib
    import tempfile
    fails = []

    def ok(cond, msg):
        if not cond:
            fails.append(msg)
            print('ERRORE T %s' % msg)
        return cond

    repo = repo or default_repo()
    if not repo:
        print('ERRORE T repository di HeartGold non trovato (--repo o TRINACRIA_REPO)')
        print('SELFTEST_FAILED')
        return 1
    try:
        hg, hg_path = hg_original(repo)
    except AudioError as e:
        print('ERRORE T %s' % e)
        print('SELFTEST_FAILED')
        return 1
    sd = Sdat(hg)
    # 1. archivio identico
    ok(sd.build() == hg, 'la ricostruzione dell\'archivio non è identica all\'originale')
    # 2. gemelli
    pairs = gb_twins(repo)
    ok(len(pairs) == 136, 'tabella dei gemelli: %d coppie invece di 136' % len(pairs))
    for ds, gb in pairs:
        ok(twin_of(sd, ds) == gb, 'gemello di %s: %s invece di %s' % (ds, twin_of(sd, ds), gb))
    vals = sndseq_values(repo)
    aliases = add_aliases(sd, repo)
    for nm, v in vals.items():
        if nm == 'SEQ_NONE':
            continue
        k = sd.index.get(nm)
        ok(k is not None and k[0] == 'SEQ' and k[1] == v and sd.seq_info(v) is not None,
           '%s: valore %s in sndseq.h, %s nell\'archivio' % (nm, v, k))
    # 3. andata e ritorno di tutte le sequenze
    n_rt = 0
    for i, nm in enumerate(sd.names['SEQ']):
        if not nm or not sd.seq_info(i):
            continue
        f = sd.seq_data(i)
        t1 = simulate(f)
        lp = song_loop(t1)
        if lp == 'diversi':
            continue
        w = []
        s2 = midi_to_sseq(sseq_to_midi(f)[0], w)[0]
        t2 = simulate(s2)
        u = lp[1] if lp else None
        ok(timeline(t1, u) == timeline(t2, u) and song_loop(t2) == lp and not w,
           'andata e ritorno diversi: %s' % nm)
        n_rt += 1
    ok(n_rt >= 1371, 'solo %d sequenze provate' % n_rt)
    # 4. brano di prova
    mid, expect = demo_song()
    sseq, info = midi_to_sseq(mid)
    got = []
    for k, tr in enumerate(simulate(sseq)):
        ch = info['canali'][k]
        got += [(ch, t, key, vel, dur, prg) for t, key, vel, dur, prg, _ in tr.notes]
    ok(sorted(got) == sorted(expect), 'brano di prova: note diverse da quelle scritte')
    ok(info['ritornello'] == (4 * TPQ, 16 * TPQ), 'brano di prova: ritornello %s' % (info['ritornello'],))
    # 5. applica: slot con file condiviso e slot di lotta col gemello
    tmp = tempfile.mkdtemp(prefix='trinacria_audio_')
    songs = {'a.mid': demo_song(2)[0], 'b.mid': demo_song(3)[0], 'c.mid': demo_song(4)[0]}
    for nm, data in songs.items():
        write(os.path.join(tmp, nm), data)
    man = {'brani': [
        {'slot': 'SEQ_GS_C_NIBI', 'file': 'a.mid', 'banco': 'BANK_BGM_FIELD16', 'volume': 70},
        {'slot': 'SEQ_GS_C_YAMABUKI', 'file': 'b.mid'},
        {'slot': 'SEQ_GS_VS_TRAINER', 'file': 'c.mid', 'banco': 'BANK_BGM_BATTLE1', 'volume': 110}]}
    out, rep, errs = applica(hg, man, tmp, repo=repo)
    print_errs(errs)
    if ok(out is not None and not errs, 'applica: manifesto valido rifiutato'):
        out2 = applica(hg, man, tmp)[0]
        ok(out == out2, 'applica non è deterministico')
        e2 = controlla(hg, out, man, tmp)
        print_errs(e2)
        ok(not e2, 'controlla: archivio valido rifiutato')
        nb = Sdat(out)
        fa = nb.seq_info(nb.seq_index('SEQ_GS_C_NIBI'))['file']
        fb = nb.seq_info(nb.seq_index('SEQ_GS_C_YAMABUKI'))['file']
        ok(fa != fb, 'due slot sullo stesso file')
        ok(nb.seq_data(nb.seq_index('SEQ_GS_C_TOKIWA')) == sd.seq_data(sd.seq_index('SEQ_GS_C_TOKIWA')),
           'SEQ_GS_C_TOKIWA (stesso file di NIBI e YAMABUKI) cambiato')
        ok(nb.seq_info(nb.seq_index('SEQ_GS_P_VS_TRAINER'))['file'] ==
           nb.seq_info(nb.seq_index('SEQ_GS_VS_TRAINER'))['file'], 'il gemello GB non suona il brano nuovo')
        ok(nb.name('BANK', nb.seq_info(nb.seq_index('SEQ_GS_P_C_NIBI'))['banco']) == 'BANK_BGM_FIELD16',
           'il gemello GB non ha il banco del brano')
        # un effetto cambiato deve essere trovato
        bad = Sdat(out)
        se = bad.seq_index('SEQ_SE_DP_SELECT')
        bad.files[bad.seq_info(se)['file']] = bad.seq_data(se)[:-4] + b'\0\0\0\0'
        e3 = controlla(hg, bad.build(), man, tmp)
        ok(any(c == 'A20' for c, m in e3), 'controlla non trova un effetto cambiato')
    # 6. manifesto con errori voluti
    write(os.path.join(tmp, 'noloop.mid'), demo_song(5, loop=False)[0])
    write(os.path.join(tmp, 'vuoto.mid'), demo_song(6, prg=70, ch_extra=False)[0])
    mw = MidiWriter(48)
    k = mw.track()
    mw.tempo(k, 0, 120)
    for i in range(14):
        mw.program(k, 0, i if i < 9 else i + 1, 0)
        mw.note(k, 0, i if i < 9 else i + 1, 60 + i, 100, 48)
    mw.loop(k, 0, 192)
    write(os.path.join(tmp, 'poli.mid'), mw.data())
    mw = MidiWriter(48)
    k = mw.track()
    mw.tempo(k, 0, 120)
    for i in range(6):
        mw.program(k, 0, i, 43)
        mw.note(k, 0, i, 60, 100, 48)
    mw.loop(k, 0, 192)
    write(os.path.join(tmp, 'psg.mid'), mw.data())
    mw = MidiWriter(48)
    k = mw.track()
    mw.tempo(k, 0, 120)
    mw.program(k, 0, 0, 0)
    x = 7
    for i in range(16000):
        x = (x * 1103515245 + 12345) & 0x7FFFFFFF
        mw.note(k, i * 2 + x % 2, 0, 24 + x % 96, 1 + x % 127, 1 + x % 5)
    mw.loop(k, 0, 32002)
    write(os.path.join(tmp, 'lungo.mid'), mw.data())
    mw = MidiWriter(48)
    k = mw.track()
    mw.cc(k, 0, 0, 3, 5)
    mw.note(k, 0, 0, 60, 100, 48)
    mw.loop(k, 0, 192)
    write(os.path.join(tmp, 'cc.mid'), mw.data())
    ko = {'brani': [
        {'slot': 'SEQ_SE_DP_SELECT', 'file': 'a.mid'},                         # A01
        {'slot': 'SEQ_GS_T_WAKABA', 'file': 'manca.mid'},                      # A02
        {'slot': 'SEQ_GS_C_KIKYOU', 'file': 'a.mid', 'banco': 'BANK_SE_FIELD'},  # A03
        {'slot': 'SEQ_GS_C_ASAGI', 'file': 'a.mid', 'volume': 200},            # A04
        {'slot': 'SEQ_GS_C_ENJU', 'file': 'vuoto.mid'},                        # A05
        {'slot': 'SEQ_GS_C_TANBA', 'file': 'poli.mid'},                        # A06
        {'slot': 'SEQ_GS_C_FUSUBE', 'file': 'psg.mid'},                        # A07
        {'slot': 'SEQ_GS_C_KOGANE', 'file': 'lungo.mid'},                      # A08
        {'slot': 'SEQ_GS_VS_GYMREADER', 'file': 'lungo.mid'},                  # A09
        {'slot': 'SEQ_GS_GYM', 'file': 'noloop.mid'},                          # A10
        {'slot': 'SEQ_GS_C_ENJU', 'file': 'a.mid'},                            # A11
        {'slot': 'SEQ_GS_POKESEN', 'file': 'cc.mid'}]}                         # A12
    out, rep, errs = applica(hg, ko, tmp, repo=repo)
    codes = {c for c, m in errs}
    want = {'A01', 'A02', 'A03', 'A04', 'A05', 'A06', 'A07', 'A08', 'A09', 'A10', 'A11', 'A12'}
    ok(out is None and codes == want, 'manifesto con errori: codici %s invece di %s' % (
        sorted(codes), sorted(want)))
    e4 = applica(hg[:-1] + b'\x01', man, tmp)[2]
    ok([c for c, m in e4] == ['A22'], 'archivio di partenza diverso non rifiutato')
    print('collaudo: %d sequenze in andata e ritorno, %d coppie di gemelli, %d nomi di sndseq.h '
          '(%d rinominati dal decomp), %d codici d\'errore' % (
              n_rt, len(pairs), len(vals) - 1, len(aliases), len(want) + 1))
    print('SELFTEST_FAILED' if fails else 'SELFTEST_OK')
    return 1 if fails else 0


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if argv and argv[0] == '--selftest':
        rp = argv[argv.index('--repo') + 1] if '--repo' in argv else None
        return selftest(rp)
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('comando', choices=['info', 'slot', 'banco', 'mid2sseq', 'sseq2mid', 'txt',
                                        'onde', 'applica', 'controlla', 'catalogo'])
    ap.add_argument('argomenti', nargs='*')
    ap.add_argument('--repo')
    ap.add_argument('--sdat')
    ap.add_argument('--hg')
    ap.add_argument('--out')
    ap.add_argument('--manifesto')
    a = ap.parse_args(argv)
    repo = a.repo or default_repo()
    try:
        if a.comando == 'mid2sseq':
            src, dst = a.argomenti
            w = []
            data, info = midi_to_sseq(read(src), w)
            for x in w:
                print('ERRORE A12 %s' % x)
            write(dst, data)
            print('%s: %d byte, %d tracce (canali %s), %d note, ritornello %s' % (
                dst, len(data), info['tracce'], info['canali'], info['note'], info['ritornello']))
            print('AUDIO_FAILED' if w else 'AUDIO_OK')
            return 1 if w else 0
        if a.comando == 'txt' and a.argomenti and a.argomenti[0].lower().endswith('.sseq'):
            print(disasm(read(a.argomenti[0])))
            return 0
        sd = Sdat(read(a.sdat or sdat_path(repo)))
        if repo:
            add_aliases(sd, repo)
        if a.comando == 'info':
            for kind in REC_NAMES:
                print('%-8s %d' % (kind, len([x for x in sd.entries[kind] if x is not None])))
            print('file     %d, %d byte' % (len(sd.files), len(sd.raw)))
            for p, v in sorted(player_limits(sd).items()):
                print(p, json.dumps(v, ensure_ascii=False))
        elif a.comando == 'slot':
            for nm in a.argomenti:
                i = sd.seq_index(nm)
                inf = sd.seq_info(i)
                tracks = simulate(sd.seq_data(i))
                print('%s %d: file %d (%d byte), %s, volume %d, %s, gemello %s, ritornello %s, tracce %d' % (
                    nm, i, inf['file'], len(sd.seq_data(i)), sd.name('BANK', inf['banco']), inf['volume'],
                    sd.name('PLAYER', inf['lettore']), twin_of(sd, nm), song_loop(tracks), len(tracks)))
        elif a.comando == 'banco':
            for nm in a.argomenti:
                for p, inst in enumerate(parse_sbnk(sd.bank_data(sd.bank_index(nm)))):
                    if inst:
                        print('%s %3d %-9s %s' % (nm, p, inst['tipo'], ' '.join(
                            '%s-%s:%s/%d' % (note_name(lo), note_name(hi), r['tipo'], r['swav'])
                            for lo, hi, r in inst['regioni'][:6])))
        elif a.comando == 'sseq2mid':
            nm, dst = a.argomenti
            data, info = sseq_to_midi(sd.seq_data(sd.seq_index(nm)))
            write(dst, data)
            print('%s: %d tracce, ritornello %s' % (dst, info['tracce'], info['ritornello']))
        elif a.comando == 'txt':
            print(disasm(sd.seq_data(sd.seq_index(a.argomenti[0]))))
        elif a.comando == 'onde':
            nm = a.argomenti[0]
            dst = a.out or '.'
            info = sd.bank_info(sd.bank_index(nm))
            n = 0
            for w in info['wavearc']:
                if w == 0xFFFF:
                    continue
                an = sd.name('WAVEARC', w)
                for k, wv in enumerate(parse_swar(sd.files[sd.wavearc_info(w)['file']])):
                    write(os.path.join(dst, '%s_%03d.wav' % (an, k)), wav_bytes(swav_pcm16(wv), wv['hz']))
                    n += 1
            print('%d onde scritte in %s' % (n, dst))
        elif a.comando == 'catalogo':
            write(a.out, json.dumps(catalog(sd), ensure_ascii=False, indent=1).encode('utf-8'))
            print('catalogo scritto in %s' % a.out)
        elif a.comando == 'applica':
            hg, hg_path = hg_original(repo, a.hg)
            with open(a.manifesto, encoding='utf-8') as f:
                man = json.load(f)
            out, rep, errs = applica(hg, man, os.path.dirname(os.path.abspath(a.manifesto)), repo=repo)
            for r in rep:
                print(r)
            print_errs(errs)
            if errs:
                print('AUDIO_FAILED')
                return 1
            write(a.out or sdat_path(repo), out)
            print('%s: %d byte (originale %d)' % (a.out or sdat_path(repo), len(out), len(hg)))
            print('AUDIO_OK')
        elif a.comando == 'controlla':
            hg, hg_path = hg_original(repo, a.hg)
            man = None
            base = '.'
            if a.manifesto:
                with open(a.manifesto, encoding='utf-8') as f:
                    man = json.load(f)
                base = os.path.dirname(os.path.abspath(a.manifesto))
            errs = controlla(hg, sd.raw, man, base)
            print_errs(errs)
            print('AUDIO_FAILED' if errs else 'AUDIO_OK')
            return 1 if errs else 0
    except (AudioError, OSError, ValueError) as e:
        print('ERRORE A00 %s' % e)
        print('AUDIO_FAILED')
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
