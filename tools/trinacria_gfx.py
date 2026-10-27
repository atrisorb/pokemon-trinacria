#!/usr/bin/env python3
"""Strumento grafico di Pokémon Trinacria (Modulo 4, blocco 4.1).

Legge e riscrive gli archivi grafici di HeartGold e controlla i file nuovi prima che
entrino nel repository. Solo libreria standard di Python (3.8+): i PNG si leggono qui,
senza Pillow; nitrogfx e g3dcvtr sono programmi esterni (documento 4.1, §2).

Comandi:
  --selftest                           collaudo completo (SELFTEST_OK)
  censimento [--rom R] [--out F.json]  ogni file del filesystem: formato, voci dei NARC,
                                       e con --rom confronto byte per byte con la ROM
  narc unpack NARC DIR | narc pack DIR NARC
                                       voci 0000.bin, 0001.bin…; pack(unpack) è identico
  rom   --rom R PERCORSO OUT           un file della ROM (percorso del filesystem, /a/0/4/4)
  landdata split VOCE DIR | landdata join DIR VOCE
                                       voce di files/a/0/6/5: permessi, edifici, NSBMD, BDHC
  permessi GRIGLIA LEGENDA OUT.bin     2048 byte di permessi (colonne tipo, collisione della legenda)
  edifici CSV OUT.bin                  edifici di una cella (colonne modello, x, y, z in unità del mondo)
  cella VOCE.bin [--tileset T.nsbtx]   limiti di una voce nuova (K21) e texture nel tileset (K20)
  tileset T.nsbtx [--edifici E.nsbtx]  limiti di un tileset nuovo e VRAM dell'area (K21)
  area                                 tabella dei dati d'area (files/a/0/4/2)
  matrice FILE.bin                     larghezza, altezza, intestazioni, modelli
  nsbtx FILE | nsbtx NARC:VOCE         texture (nome, formato, misure) e palette
  png   FILE.png [--come ORIG.png] [--bpp 4|8] [--colori N]
                                       controllo di un PNG nuovo (regole R-GFX-03…07)
  imd   GRIGLIA LEGENDA TEXDIR OUT.imd modello piatto 32×32 per g3dcvtr (R-GFX-10)
  g3d   IN.imd OUT (--modello|--texture) [--g3dcvtr EXE]
                                       g3dcvtr da Windows, poi lettura del risultato
  nitrogfx --rom R --nitrogfx CMD [--wsl]
                                       prova della catena 2D: PNG del repository → NCGR
                                       con le opzioni del meson.build, confrontato con la ROM
  overworld [SPECIE ...]               sprite di campo dei Pokémon (Follower e scene)
  applica --blocchi 4.2 [4.3] [--build DIR] [--rom R] [--prova DIR] [--polo-giallo]
                                       porta nel repository i manifesti dei blocchi grafici
                                       (build/grafica/<blocco>/manifesto.json, blocco 4.2)
Senza --repo si cerca il repository di HeartGold (TRINACRIA_REPO, cartella corrente,
F:\\Progetti\\pokeheartgold). Ultima riga: GRAFICA_OK / GRAFICA_FAILED (SELFTEST_OK /
SELFTEST_FAILED); ogni problema è una riga "ERRORE <codice> <messaggio>".
Documento: docs/MODULO_4/4.1_INVENTARIO_PIPELINE.md.
"""
import argparse
import csv
import hashlib
import json
import os
import re
import shutil
import struct
import subprocess
import sys
import tempfile
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT = os.path.abspath(os.path.join(HERE, '..'))

# --------------------------------------------------------------------------- binario


def u16(b, o):
    return struct.unpack_from('<H', b, o)[0]


def u32(b, o):
    return struct.unpack_from('<I', b, o)[0]


def align(n, a):
    return (n + a - 1) // a * a


def sha1(b):
    return hashlib.sha1(b).hexdigest()


class GfxError(Exception):
    def __init__(self, code, msg):
        Exception.__init__(self, '%s %s' % (code, msg))
        self.code = code
        self.msg = msg


MAGIC = {
    b'NARC': 'NARC', b'RGCN': 'NCGR', b'RLCN': 'NCLR', b'RCSN': 'NSCR', b'RECN': 'NCER',
    b'RNAN': 'NANR', b'BMD0': 'NSBMD', b'BTX0': 'NSBTX', b'BCA0': 'NSBCA', b'BTA0': 'NSBTA',
    b'BTP0': 'NSBTP', b'BMA0': 'NSBMA', b'BVA0': 'NSBVA', b'RTFN': 'NFTR', b'SDAT': 'SDAT',
    b'BDHC': 'BDHC', b'RPCN': 'NCPR', b'RCMN': 'NMCR', b'RNMA': 'NMAR',
}


def kind(b):
    """Formato di un file dai primi byte (R-GFX-01)."""
    if len(b) >= 4 and b[:4] in MAGIC:
        return MAGIC[b[:4]]
    if len(b) >= 4 and b[0] in (0x10, 0x11) and (b[1] | b[2] << 8 | b[3] << 16) > 0:
        size = b[1] | b[2] << 8 | b[3] << 16
        if size >= len(b) - 4:
            return 'LZ%02X' % b[0]
    if not b:
        return 'vuoto'
    return 'dati'


# --------------------------------------------------------------------------- LZ (lettura)


def lz_decompress(b):
    """LZ10/LZ11 di BIOS (come nitrogfx): serve solo per riconoscere cosa c'è dentro."""
    typ = b[0]
    size = b[1] | b[2] << 8 | b[3] << 16
    out = bytearray()
    i = 4
    while len(out) < size:
        if i >= len(b):
            raise GfxError('K00', 'LZ troncato')
        flags = b[i]
        i += 1
        for bit in range(8):
            if len(out) >= size:
                break
            if not flags & (0x80 >> bit):
                out.append(b[i])
                i += 1
                continue
            if typ == 0x10:
                n = (b[i] >> 4) + 3
                d = ((b[i] & 0xF) << 8 | b[i + 1]) + 1
                i += 2
            else:
                ind = b[i] >> 4
                if ind == 0:
                    n = ((b[i] & 0xF) << 4 | b[i + 1] >> 4) + 0x11
                    d = ((b[i + 1] & 0xF) << 8 | b[i + 2]) + 1
                    i += 3
                elif ind == 1:
                    n = ((b[i] & 0xF) << 12 | b[i + 1] << 4 | b[i + 2] >> 4) + 0x111
                    d = ((b[i + 2] & 0xF) << 8 | b[i + 3]) + 1
                    i += 4
                else:
                    n = ind + 1
                    d = ((b[i] & 0xF) << 8 | b[i + 1]) + 1
                    i += 2
            for _ in range(n):
                out.append(out[-d])
    return bytes(out[:size])


VUOTA = b'\0\0\0\0'


def deep_kind(b):
    if b == VUOTA:
        return 'vuota'
    k = kind(b)
    if k.startswith('LZ'):
        try:
            return k + ':' + kind(lz_decompress(b))
        except (GfxError, IndexError):
            return k + ':?'
    return k


# --------------------------------------------------------------------------- NARC


class Narc:
    """Archivio NARC. pack() riproduce l'originale byte per byte (selftest K01)."""

    def __init__(self, data):
        if data[:4] != b'NARC':
            raise GfxError('K01', 'non è un NARC')
        self.header = data[:16]
        o = u16(data, 12)
        if data[o:o + 4] != b'BTAF':
            raise GfxError('K01', 'blocco BTAF mancante')
        btaf_size = u32(data, o + 4)
        n = u16(data, o + 8)
        self.btaf_pad = data[o + 10:o + 12]
        spans = [(u32(data, o + 12 + 8 * i), u32(data, o + 16 + 8 * i)) for i in range(n)]
        o2 = o + btaf_size
        if data[o2:o2 + 4] != b'BTNF':
            raise GfxError('K01', 'blocco BTNF mancante')
        self.btnf = data[o2:o2 + u32(data, o2 + 4)]
        o3 = o2 + len(self.btnf)
        if data[o3:o3 + 4] != b'GMIF':
            raise GfxError('K01', 'blocco GMIF mancante')
        base = o3 + 8
        gmif_end = o3 + u32(data, o3 + 4)
        self.files = [data[base + s:base + e] for s, e in spans]
        # riempimento: byte usato fra le voci e in coda
        self.pad = 0xFF
        for i, (s, e) in enumerate(spans):
            nxt = spans[i + 1][0] if i + 1 < n else gmif_end - base
            if nxt > e:
                self.pad = data[base + e]
                break
        self.tail = data[gmif_end:]
        self.offsets = spans
        self.gmif_len = gmif_end - base

    def pack(self):
        offs = []
        body = bytearray()
        for i, f in enumerate(self.files):
            s = len(body)
            body += f
            offs.append((s, len(body)))
            if i + 1 < len(self.files):
                while len(body) % 4:
                    body.append(self.pad)
        while len(body) % 4:
            body.append(self.pad)
        btaf = bytearray(b'BTAF' + struct.pack('<I', 12 + 8 * len(self.files)) +
                         struct.pack('<H', len(self.files)) + self.btaf_pad)
        for s, e in offs:
            btaf += struct.pack('<II', s, e)
        gmif = b'GMIF' + struct.pack('<I', 8 + len(body)) + bytes(body)
        total = 16 + len(btaf) + len(self.btnf) + len(gmif) + len(self.tail)
        head = self.header[:8] + struct.pack('<I', total) + self.header[12:16]
        return head + bytes(btaf) + self.btnf + gmif + self.tail

    @staticmethod
    def build(files, pad=0xFF):
        n = Narc.__new__(Narc)
        n.header = b'NARC\xfe\xff\x00\x01' + b'\0' * 4 + b'\x10\x00\x03\x00'
        n.btaf_pad = b'\0\0'
        n.btnf = b'BTNF\x10\x00\x00\x00\x04\x00\x00\x00\x00\x00\x01\x00'
        n.files = list(files)
        n.pad = pad
        n.tail = b''
        return n


# --------------------------------------------------------------------------- ROM (filesystem NitroROM)


class Rom:
    """File della ROM per percorso (/a/0/4/4). Serve a confrontare il repository con l'originale."""

    def __init__(self, path):
        with open(path, 'rb') as fh:
            self.data = fh.read()
        d = self.data
        fnt, fat = u32(d, 0x40), u32(d, 0x48)
        nfiles = u32(d, 0x4C) // 8
        self.fat = [(u32(d, fat + 8 * i), u32(d, fat + 8 * i + 4)) for i in range(nfiles)]
        self.paths = {}

        def walk(dir_id, prefix):
            o = fnt + 8 * (dir_id & 0xFFF)
            sub, fid = u32(d, o), u16(d, o + 4)
            p = fnt + sub
            while d[p]:
                ln = d[p] & 0x7F
                isdir = d[p] & 0x80
                name = d[p + 1:p + 1 + ln].decode('ascii')
                p += 1 + ln
                if isdir:
                    walk(u16(d, p), prefix + name + '/')
                    p += 2
                else:
                    self.paths[prefix + name] = fid
                    fid += 1
        walk(0xF000, '/')

    def read(self, path):
        path = '/' + path.lstrip('/')
        if path not in self.paths:
            raise GfxError('K02', 'file non presente nella ROM: %s' % path)
        s, e = self.fat[self.paths[path]]
        return self.data[s:e]


# --------------------------------------------------------------------------- repository


def find_repo(arg=None):
    for c in (arg, os.environ.get('TRINACRIA_REPO'), os.getcwd(),
              os.path.join(HERE, '..', '..', 'pokeheartgold'), r'F:\Progetti\pokeheartgold'):
        if c and os.path.isfile(os.path.join(c, 'include', 'constants', 'sprites.h')):
            return os.path.abspath(c)
    return None


def read(path):
    with open(path, 'rb') as fh:
        return fh.read()


def filesystem(repo):
    """Righe di heartgold.us/filesystem.csv: (sorgente nel repository, percorso nella ROM)."""
    rows = []
    with open(os.path.join(repo, 'heartgold.us', 'filesystem.csv'), encoding='utf-8') as fh:
        for r in csv.reader(fh):
            if r and r[0] != 'Source File':
                rows.append((r[0], r[1]))
    return rows


def narc_ids(repo):
    """NARC_* -> numero (include/filesystem_files_def.h) e numero -> nome."""
    out = {}
    for m in re.finditer(r'(NARC_\w+)\s*=\s*(\d+)', open(os.path.join(repo, 'include', 'filesystem_files_def.h'), encoding='utf-8').read()):
        out[m.group(1)] = int(m.group(2))
    return out


def defines(path, prefix):
    out = {}
    for m in re.finditer(r'#define\s+(%s\w*)\s+(\d+|0x[0-9A-Fa-f]+)\b' % prefix, open(path, encoding='utf-8').read()):
        out[m.group(1)] = int(m.group(2), 0)
    return out


# --------------------------------------------------------------------------- land data (files/a/0/6/5)

LAND_SIG = 0x1234


def land_split(b):
    """Voce di land data -> dict con le sezioni (formato del documento 4.1, §3.3)."""
    if len(b) < 0x14:
        raise GfxError('K03', 'voce troppo corta')
    lp, lb, lm, lh = struct.unpack_from('<4I', b, 0)
    sig, nbg = u16(b, 0x10), u16(b, 0x12)
    if sig != LAND_SIG:
        raise GfxError('K03', 'firma 0x%04X invece di 0x1234' % sig)
    o = 0x14
    bgs = b[o:o + nbg]
    o += nbg
    parts = {'suoni': bgs}
    for name, n in (('permessi', lp), ('edifici', lb), ('modello', lm), ('bdhc', lh)):
        parts[name] = b[o:o + n]
        if len(parts[name]) != n:
            raise GfxError('K03', 'sezione %s troncata' % name)
        o += n
    parts['coda'] = b[o:]
    if lp != 2048:
        raise GfxError('K03', 'permessi di %d byte invece di 2048' % lp)
    if lb % 48:
        raise GfxError('K03', 'edifici di %d byte, non multiplo di 48' % lb)
    if parts['modello'][:4] != b'BMD0':
        raise GfxError('K03', 'il modello non è un NSBMD')
    if parts['bdhc'][:4] != b'BDHC':
        raise GfxError('K03', 'il terreno non è un BDHC')
    return parts


def land_join(parts):
    head = struct.pack('<4IHH', len(parts['permessi']), len(parts['edifici']), len(parts['modello']),
                       len(parts['bdhc']), LAND_SIG, len(parts['suoni']))
    return head + parts['suoni'] + parts['permessi'] + parts['edifici'] + parts['modello'] + parts['bdhc'] + parts.get('coda', b'')


FX = 4096   # punto fisso 20.12 del DS


def land_buildings(edifici):
    """Edifici di una cella: 48 byte l'uno = u32 modello, x/y/z (fx32, unità del mondo, origine al
    centro della cella, una casella = 16), 3 rotazioni (sempre 0 in HeartGold), 3 scale (1,0) e 8 byte a 0."""
    out = []
    for i in range(0, len(edifici), 48):
        e = edifici[i:i + 48]
        m, x, y, z = struct.unpack_from('<I3i', e, 0)
        rot = struct.unpack_from('<3I', e, 16)
        scala = struct.unpack_from('<3I', e, 28)
        if rot != (0, 0, 0) or scala != (FX, FX, FX) or e[40:48] != b'\0' * 8:
            raise GfxError('K03', 'edificio %d: rotazione o scala diverse da quelle di HeartGold' % (i // 48))
        out.append({'modello': m, 'x': x / FX, 'y': y / FX, 'z': z / FX})
    return out


def buildings_build(rows):
    b = bytearray()
    for r in rows:
        b += struct.pack('<I3i3I3I8x', int(r['modello']), round(float(r['x']) * FX), round(float(r['y']) * FX),
                         round(float(r['z']) * FX), 0, 0, 0, FX, FX, FX)
    return bytes(b)


def tile_center(col, row):
    """Centro della casella locale (colonna, riga) in unità del mondo: x, z."""
    return col * 16 - 248, row * 16 - 248


def permissions_build(grid, legend_rows):
    """2048 byte di permessi: per casella (comportamento, collisione), riga 0 = nord."""
    leg = {}
    for r in legend_rows:
        leg[r['carattere']] = (int(r.get('tipo') or '0', 0), int(r.get('collisione') or '0', 0))
    out = bytearray()
    for row, line in enumerate(grid):
        for col, ch in enumerate(line):
            if ch not in leg:
                raise GfxError('K16', 'carattere %r (riga %d, colonna %d) non è nella legenda' % (ch, row, col))
            out += bytes(leg[ch])
    return bytes(out)


# --------------------------------------------------------------------------- dati d'area, matrici


def area_entries(b_narc):
    out = []
    for i, f in enumerate(Narc(b_narc).files):
        if len(f) != 8:
            raise GfxError('K05', 'dati d\'area %d: %d byte invece di 8' % (i, len(f)))
        out.append({'indice': i, 'tex_edifici': u16(f, 0), 'tex_mappa': u16(f, 2),
                    'tex_dinamiche': u16(f, 4), 'esterno': f[6], 'luce': f[7]})
    return out


def matrix_parse(b):
    w, h, has_hdr, has_alt, nl = b[0], b[1], b[2], b[3], b[4]
    o = 5
    name = b[o:o + nl].decode('ascii')
    o += nl
    hdr = alt = None
    if has_hdr:
        hdr = list(struct.unpack_from('<%dH' % (w * h), b, o))
        o += 2 * w * h
    if has_alt:
        alt = list(b[o:o + w * h])
        o += w * h
    models = list(struct.unpack_from('<%dH' % (w * h), b, o))
    o += 2 * w * h
    if o != len(b):
        raise GfxError('K04', 'matrice %s: %d byte in più' % (name, len(b) - o))
    return {'larghezza': w, 'altezza': h, 'nome': name, 'intestazioni': hdr, 'altitudini': alt, 'modelli': models}


def matrix_build(m):
    w, h = m['larghezza'], m['altezza']
    b = bytes([w, h, 1 if m['intestazioni'] is not None else 0, 1 if m['altitudini'] is not None else 0,
               len(m['nome'])]) + m['nome'].encode('ascii')
    if m['intestazioni'] is not None:
        b += struct.pack('<%dH' % (w * h), *m['intestazioni'])
    if m['altitudini'] is not None:
        b += bytes(m['altitudini'])
    return b + struct.pack('<%dH' % (w * h), *m['modelli'])


# --------------------------------------------------------------------------- NSBTX / TEX0

TEX_FORMATS = {0: 'nessuno', 1: 'A3I5', 2: 'palette4', 3: 'palette16', 4: 'palette256',
               5: 'compresso4x4', 6: 'A5I3', 7: 'diretto'}


def _dict(b, o):
    """Dizionario 3D NITRO: [(nome, dati)]. Dati di 8 byte per le texture, 4 per le palette."""
    n = b[o + 1]
    o2 = o + 4
    hdr_size = u16(b, o2)
    o2 += hdr_size + 4 * n if hdr_size == 8 else 8 + 4 * n
    unit = u16(b, o2)
    data = o2 + 4
    names = data + unit * n
    return [(b[names + 16 * i:names + 16 * i + 16].rstrip(b'\0').decode('latin-1'),
             b[data + unit * i:data + unit * (i + 1)]) for i in range(n)]


def tex0_parse(b, o=None):
    """Elenco texture e palette di un blocco TEX0 (dentro NSBTX o NSBMD)."""
    if o is None:
        o = b.find(b'TEX0')
        if o < 0:
            return {'texture': [], 'palette': []}
    tex_info = o + u16(b, o + 0x0E)
    pal_size = u16(b, o + 0x30) << 3
    pal_info = o + u32(b, o + 0x34)
    texs = []
    for name, d in _dict(b, tex_info):
        p = u32(d, 0)
        texs.append({'nome': name, 'formato': TEX_FORMATS[(p >> 26) & 7],
                     'larghezza': 8 << ((p >> 20) & 7), 'altezza': 8 << ((p >> 23) & 7),
                     'colore0_trasparente': bool((p >> 29) & 1)})
    pals = []
    raw = _dict(b, pal_info)
    offs = sorted({u16(d, 0) << 3 for _, d in raw}) + [pal_size]
    for name, d in raw:
        start = u16(d, 0) << 3
        nxt = min(x for x in offs if x > start) if any(x > start for x in offs) else pal_size
        pals.append({'nome': name, 'colori': (nxt - start) // 2})
    return {'texture': texs, 'palette': pals}


def nsbtx_parse(b):
    if b[:4] != b'BTX0':
        raise GfxError('K06', 'non è un NSBTX')
    return tex0_parse(b, u32(b, 0x10))


def tex_bytes(b):
    """(byte di texture, byte di palette) di un NSBTX: quello che occupa la VRAM."""
    if b == VUOTA:
        return 0, 0
    o = u32(b, 0x10)
    return u16(b, o + 0x0C) << 3, u16(b, o + 0x30) << 3


# Massimi misurati sugli originali di HeartGold (selftest K21 li ricalcola): un file nuovo
# che resta dentro questi valori ha la stessa forma di qualcosa che il gioco carica già (R-GFX-13).
LIMITI = {
    'tileset_byte': 58704,          # NSBTX più grande di a/0/4/4
    'tileset_texture': 126,         # texture in un tileset
    'area_vram': 87424,             # texture + palette del tileset e degli edifici di un'area (area 6)
    'modello_cella': 61420,         # NSBMD più grande dentro a/0/6/5
    'edifici_cella': 30,            # edifici in una cella
    'bdhc_cella': 10794,            # BDHC più grande
    'suoni_cella': 392,             # sezione delle piastre sonore più grande
    'poligoni_cella': 1706,         # poligoni del modello di una cella (blocco 4.2)
}

# SHA-1 degli archivi originali: il collaudo li legge dal repository solo se sono ancora questi,
# altrimenti dalla ROM originale (--rom).
ORIGINALI = {
    'a/0/6/5': 'e98a8d144035f8b8f4373d203aab62c04d7c05f7',
    'a/0/4/2': '3693dbec3678c13c79aeda468c8a6c09fdcc359a',
    'a/0/4/4': 'cab5cc3f0cc28238363f27cd574ce718d719715c',
    'a/0/7/0': '546a543b11555d572bcf78888269602d6f2c7883',
    'a/0/9/2': '2aeed7ccfeb04e52ce1eecf40d0e32a20999ac57',
}
HG_DIFETTI_TEXTURE = 17   # coppie mappa–modello di HeartGold che citano texture assenti (K20)


def originale(repo, rel, rom=None):
    p = os.path.join(repo, 'files', *rel.split('/'))
    b = read(p) if os.path.isfile(p) else b''
    if sha1(b) == ORIGINALI[rel]:
        return b
    if rom is None:
        raise GfxError('K00', '%s del repository è già modificato: serve --rom con la ROM originale' % rel)
    b = rom.read('/' + rel)
    if sha1(b) != ORIGINALI[rel]:
        raise GfxError('K02', '%s della ROM non è l\'originale' % rel)
    return b


def limiti_tileset(b, edifici=None, nome='tileset'):
    errs = []
    t = nsbtx_parse(b)
    if len(b) > LIMITI['tileset_byte']:
        errs.append(('K21', '%s: %d byte, il massimo è %d' % (nome, len(b), LIMITI['tileset_byte'])))
    if len(t['texture']) > LIMITI['tileset_texture']:
        errs.append(('K21', '%s: %d texture, il massimo è %d' % (nome, len(t['texture']), LIMITI['tileset_texture'])))
    if edifici is not None:
        tot = sum(tex_bytes(b)) + sum(tex_bytes(edifici))
        if tot > LIMITI['area_vram']:
            errs.append(('K21', '%s + texture degli edifici: %d byte di VRAM, il massimo è %d' % (nome, tot, LIMITI['area_vram'])))
    return errs


def limiti_cella(parts, nome='cella'):
    errs = []
    for k, lim, what in (('modello', 'modello_cella', 'modello'), ('bdhc', 'bdhc_cella', 'BDHC'),
                         ('suoni', 'suoni_cella', 'piastre sonore')):
        if len(parts[k]) > LIMITI[lim]:
            errs.append(('K21', '%s: %s di %d byte, il massimo è %d' % (nome, what, len(parts[k]), LIMITI[lim])))
    if len(parts['edifici']) // 48 > LIMITI['edifici_cella']:
        errs.append(('K21', '%s: %d edifici, il massimo è %d' % (nome, len(parts['edifici']) // 48, LIMITI['edifici_cella'])))
    npol = nsbmd_poligoni(parts['modello'])
    if npol > LIMITI['poligoni_cella']:
        errs.append(('K21', '%s: %d poligoni nel modello, il massimo è %d' % (nome, npol, LIMITI['poligoni_cella'])))
    return errs


def nsbmd_models(b):
    """Nomi dei modelli di un NSBMD, texture e palette che i materiali citano per nome
    (le cerca nel tileset dell'area, R-GFX-12) e texture incorporate."""
    if b[:4] != b'BMD0':
        raise GfxError('K06', 'non è un NSBMD')
    nblocks = u16(b, 14)
    mdl = u32(b, 16)
    models = _dict(b, mdl + 8)
    names = [n for n, _ in models]
    usa_tex, usa_pal = [], []
    for _, d in models:
        m = mdl + u32(d, 0)
        mat = m + u32(b, m + 8)
        for n, _ in _dict(b, mat + u16(b, mat)):
            if n not in usa_tex:
                usa_tex.append(n)
        for n, _ in _dict(b, mat + u16(b, mat + 2)):
            if n not in usa_pal:
                usa_pal.append(n)
    tex = tex0_parse(b, u32(b, 20)) if nblocks > 1 else {'texture': [], 'palette': []}
    return {'modelli': names, 'usa_texture': usa_tex, 'usa_palette': usa_pal,
            'texture': tex['texture'], 'palette': tex['palette']}


def map_headers(repo):
    """src/data/map_headers.h -> {MAP_X: {campo: valore}} e include/constants/maps.h -> {MAP_X: id}."""
    src = open(os.path.join(repo, 'src', 'data', 'map_headers.h'), encoding='utf-8').read()
    out = {}
    for m in re.finditer(r'\[(MAP_\w+)\]\s*=\s*\{(.*?)\n\s*\},', src, re.S):
        out[m.group(1)] = dict(re.findall(r'\.(\w+)\s*=\s*([^,\n]+),', m.group(2)))
    ids = defines(os.path.join(repo, 'include', 'constants', 'maps.h'), 'MAP_')
    return out, ids


def matrix_file(repo, sym):
    m = re.match(r'NARC_map_matrix_map_matrix_(\d{4}_\w+)_bin$', sym)
    return os.path.join(repo, 'files', 'fielddata', 'mapmatrix', 'map_matrix', 'map_matrix_%s.bin' % m.group(1))


def map_models(repo):
    """Per ogni mappa HeartGold: voci di land data (a/0/6/5) che disegnano le sue celle."""
    hdrs, ids = map_headers(repo)
    cache = {}
    out = {}
    for name, h in hdrs.items():
        sym = h.get('matrixId', '').strip()
        if not sym.startswith('NARC_map_matrix'):
            continue
        if sym not in cache:
            cache[sym] = matrix_parse(read(matrix_file(repo, sym)))
        m = cache[sym]
        mid = ids.get(name)
        cells = [i for i in range(len(m['modelli'])) if m['modelli'][i] != 0xFFFF and
                 (m['intestazioni'] is None or m['intestazioni'][i] == mid)]
        out[name] = sorted({m['modelli'][i] for i in cells})
    return out, hdrs


def texture_mancanti(modello, tileset):
    """Nomi di texture e palette che un NSBMD cita e il NSBTX non ha (R-GFX-12)."""
    md = nsbmd_models(modello)
    tx = nsbtx_parse(tileset)
    have_t = {x['nome'] for x in tx['texture']}
    have_p = {x['nome'] for x in tx['palette']}
    return [x for x in md['usa_texture'] if x not in have_t] + [x for x in md['usa_palette'] if x not in have_p]


def area_texture_check(repo, maps=None, rom=None):
    """R-GFX-12 sulle mappe di HeartGold: le texture citate dal modello di ogni cella esistono nel
    tileset dell'area della mappa. Restituisce (coppie controllate, eccezioni)."""
    land = Narc(originale(repo, 'a/0/6/5', rom)).files
    areas = area_entries(originale(repo, 'a/0/4/2', rom))
    tiles = Narc(originale(repo, 'a/0/4/4', rom)).files
    mm, hdrs = map_models(repo)
    tcache, mcache = {}, {}
    errs = []
    n = 0
    for name, models in sorted(mm.items()):
        if maps is not None and name not in maps:
            continue
        area = int(hdrs[name]['areaDataBank'], 0)
        t = areas[area]['tex_mappa']
        if t not in tcache:
            tx = nsbtx_parse(tiles[t])
            tcache[t] = ({x['nome'] for x in tx['texture']}, {x['nome'] for x in tx['palette']})
        have_t, have_p = tcache[t]
        for mid in models:
            if mid not in mcache:
                mcache[mid] = nsbmd_models(land_split(land[mid])['modello'])
            md = mcache[mid]
            miss = [x for x in md['usa_texture'] if x not in have_t] + [x for x in md['usa_palette'] if x not in have_p]
            n += 1
            if miss:
                errs.append(('K20', '%s: il modello %d cita %s, assenti nel tileset %d dell\'area %d' % (
                    name, mid, ', '.join(miss[:4]), t, area)))
    return n, errs


# --------------------------------------------------------------------------- colori 555 (R-GFX-03)


def up5(x):
    """5 bit -> 8 bit come nitrogfx (gfx.c UPCONVERT_BIT_DEPTH)."""
    return x * 255 // 31


def down8(x):
    """8 bit -> 5 bit come nitrogfx e il DS (gfx.c DOWNCONVERT_BIT_DEPTH)."""
    return x // 8


CANON = [up5(i) for i in range(32)]


def bgr555(rgb):
    r, g, b = (down8(c) for c in rgb)
    return r | g << 5 | b << 10


def rgb_of(c555):
    return (up5(c555 & 31), up5(c555 >> 5 & 31), up5(c555 >> 10 & 31))


# --------------------------------------------------------------------------- PNG (lettura, solo stdlib)


def png_read(path):
    """PNG -> dict(larghezza, altezza, tipo, profondità, palette [(r,g,b)], pixel [indici]).
    Legge PNG indicizzati (tipo 3) e grigi (tipo 0), come nitrogfx; gli altri tipi danno K10."""
    b = read(path)
    if b[:8] != b'\x89PNG\r\n\x1a\n':
        raise GfxError('K10', '%s non è un PNG' % path)
    o = 8
    idat = bytearray()
    pal = None
    trns = b''
    while o < len(b):
        n = struct.unpack_from('>I', b, o)[0]
        t = b[o + 4:o + 8]
        d = b[o + 8:o + 8 + n]
        if t == b'IHDR':
            w, h, depth, ctype, _, _, inter = struct.unpack('>IIBBBBB', d)
        elif t == b'PLTE':
            pal = [tuple(d[i:i + 3]) for i in range(0, len(d), 3)]
        elif t == b'tRNS':
            trns = d
        elif t == b'IDAT':
            idat += d
        o += 12 + n
    if ctype not in (0, 3):
        raise GfxError('K10', '%s: PNG di tipo %d, serve un PNG indicizzato (tipo 3)' % (os.path.basename(path), ctype))
    if inter:
        raise GfxError('K10', '%s: PNG interlacciato' % os.path.basename(path))
    raw = zlib.decompress(bytes(idat))
    bpp_bits = depth
    stride = (w * bpp_bits + 7) // 8
    px = []
    prev = bytearray(stride)
    o = 0
    for _ in range(h):
        f = raw[o]
        line = bytearray(raw[o + 1:o + 1 + stride])
        o += 1 + stride
        bpp = max(1, bpp_bits // 8)
        for i in range(stride):
            a = line[i - bpp] if i >= bpp else 0
            up = prev[i]
            c = prev[i - bpp] if i >= bpp else 0
            if f == 1:
                line[i] = (line[i] + a) & 255
            elif f == 2:
                line[i] = (line[i] + up) & 255
            elif f == 3:
                line[i] = (line[i] + (a + up) // 2) & 255
            elif f == 4:
                p = a + up - c
                pa, pb, pc = abs(p - a), abs(p - up), abs(p - c)
                pr = a if pa <= pb and pa <= pc else (up if pb <= pc else c)
                line[i] = (line[i] + pr) & 255
        prev = line
        if depth == 8:
            px.extend(line[:w])
        else:
            per = 8 // depth
            mask = (1 << depth) - 1
            row = []
            for byte in line:
                for k in range(per):
                    row.append(byte >> (8 - depth * (k + 1)) & mask)
            px.extend(row[:w])
    return {'larghezza': w, 'altezza': h, 'tipo': ctype, 'profondita': depth,
            'palette': pal or [], 'trasparenza': bytes(trns), 'pixel': px}


def png_write_indexed(path, w, h, palette, pixels):
    """PNG indicizzato a 8 bit (serve al collaudo e agli script di disegno senza Pillow)."""
    def chunk(t, d):
        return struct.pack('>I', len(d)) + t + d + struct.pack('>I', zlib.crc32(t + d) & 0xFFFFFFFF)
    raw = bytearray()
    for y in range(h):
        raw.append(0)
        raw += bytes(pixels[y * w:(y + 1) * w])
    out = b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', w, h, 8, 3, 0, 0, 0))
    out += chunk(b'PLTE', b''.join(bytes(c) for c in palette))
    out += chunk(b'IDAT', zlib.compress(bytes(raw), 9)) + chunk(b'IEND', b'')
    with open(path, 'wb') as fh:
        fh.write(out)


def png_check(path, come=None, bpp=None, colori=None, avvisi=None):
    """Regole R-GFX-03…07 su un PNG nuovo. Restituisce la lista degli errori (codice, testo);
    gli avvisi (colori doppi, K14) vanno in `avvisi` se è una lista."""
    errs = []
    name = os.path.basename(path)
    try:
        p = png_read(path)
    except GfxError as e:
        return [(e.code, e.msg)]
    o = None
    if come:
        try:
            o = png_read(come)
        except GfxError as e:
            return [(e.code, 'originale: ' + e.msg)]
    if p['tipo'] != 3:
        if o is not None and o['tipo'] == 0:
            if p['profondita'] != o['profondita']:
                errs.append(('K11', '%s: grigio a %d bit invece di %d come l\'originale' % (name, p['profondita'], o['profondita'])))
            return errs
        errs.append(('K10', '%s: PNG in scala di grigi, serve la palette (tipo 3)' % name))
        return errs
    used = sorted(set(p['pixel']))
    if o is not None:
        if (o['larghezza'], o['altezza']) != (p['larghezza'], p['altezza']):
            errs.append(('K11', '%s: %d×%d invece di %d×%d come l\'originale' % (
                name, p['larghezza'], p['altezza'], o['larghezza'], o['altezza'])))
        if bpp is None:
            bpp = 4 if o['profondita'] <= 4 and len(o['palette']) <= 16 else 8
        if colori is None:
            colori = len(o['palette'])
    limit = colori or (16 if bpp == 4 else 256 if bpp == 8 else None)
    if limit and used and used[-1] >= limit:
        errs.append(('K12', '%s: usa l\'indice %d, il massimo è %d (%s)' % (
            name, used[-1], limit - 1, '%d bpp' % bpp if bpp else 'palette dell\'originale')))
    bad = sorted({c for i, rgb in enumerate(p['palette']) if i in used for c in rgb if c not in CANON})
    if bad:
        errs.append(('K13', '%s: componenti di colore fuori dalla scala 555 (%s): usa %s' % (
            name, ', '.join(map(str, bad[:6])), 'i 32 valori di R-GFX-03')))
    seen = {}
    for i, rgb in enumerate(p['palette']):
        if i in used and i != 0:
            k = bgr555(rgb)
            if k in seen:
                if avvisi is not None:
                    avvisi.append(('K14', '%s: gli indici %d e %d hanno lo stesso colore sul DS (0x%04X)' % (name, seen[k], i, k)))
                break
            seen[k] = i
    if p['larghezza'] % 8 or p['altezza'] % 8:
        errs.append(('K15', '%s: %d×%d non è multiplo di 8 (tile 8×8)' % (name, p['larghezza'], p['altezza'])))
    return errs


# --------------------------------------------------------------------------- IMD per g3dcvtr (R-GFX-10)

IMD_TILE = 0.25
IMD_HALF = 16 * IMD_TILE
IMD_POS_SCALE = 6
IMD_NORMAL = '0.000000 0.997000 0.000000'


def _f6(v):
    return '%.6f' % (round(v * 100000) / 100000)


def imd_texture(path):
    p = png_read(path)
    name = os.path.splitext(os.path.basename(path))[0]
    for n in (p['larghezza'], p['altezza']):
        if n < 8 or n > 1024 or n & (n - 1):
            raise GfxError('K16', '%s: lato %d, serve una potenza di 2 fra 8 e 1024' % (name, n))
    if p['tipo'] != 3:
        raise GfxError('K10', '%s: serve un PNG indicizzato' % name)
    if len(name) > 13 or not re.match(r'[a-z0-9_]+$', name):
        raise GfxError('K17', '%s: il nome della texture ha al massimo 13 caratteri fra a–z, 0–9 e _ '
                              '(la palette si chiama <nome>_pl e i nomi stanno in 16 byte, R-GFX-11)' % name)
    if max(p['pixel']) > 15:
        raise GfxError('K12', '%s: usa l\'indice %d, il formato palette16 arriva a 15' % (name, max(p['pixel'])))
    pal = (p['palette'] + [(0, 0, 0)] * 16)[:16]
    bad = sorted({c for rgb in pal[:len(p['palette'])] for c in rgb if c not in CANON})
    if bad:
        raise GfxError('K13', '%s: componenti fuori dalla scala 555: %s' % (name, bad[:6]))
    idx = p['pixel']
    data = bytearray()
    for i in range(0, len(idx), 2):
        data.append((idx[i] & 0xF) | ((idx[i + 1] & 0xF) << 4))
    words = [data[i] | data[i + 1] << 8 for i in range(0, len(data), 2)]
    return {'nome': name, 'w': p['larghezza'], 'h': p['altezza'], 'parole': len(words),
            'bitmap': ' '.join('%04x' % x for x in words),
            'palette': ' '.join('%04x' % bgr555(c) for c in pal)}


def imd_rects(grid, legend):
    used = [[False] * 32 for _ in range(32)]
    rects = []
    for row in range(32):
        for col in range(32):
            if used[row][col]:
                continue
            tex = legend[grid[row][col]]
            if not tex:
                used[row][col] = True
                continue
            w = 1
            while col + w < 32 and not used[row][col + w] and legend.get(grid[row][col + w]) == tex:
                w += 1
            h = 1
            while row + h < 32 and all(not used[row + h][c] and legend.get(grid[row + h][c]) == tex
                                       for c in range(col, col + w)):
                h += 1
            for r in range(row, row + h):
                for c in range(col, col + w):
                    used[r][c] = True
            rects.append((tex, col, row, w, h))
    return rects


def imd_read_grid(path):
    with open(path, encoding='utf-8') as fh:
        rows = [ln.rstrip('\r\n') for ln in fh if ln.strip('\r\n')]
    if len(rows) != 32 or any(len(r) != 32 for r in rows):
        raise GfxError('K16', '%s: servono 32 righe di 32 caratteri' % path)
    return rows


def imd_read_legend(path):
    out = {}
    with open(path, encoding='utf-8', newline='') as fh:
        for r in csv.DictReader(fh):
            out[r['carattere']] = (r.get('texture') or '').strip()
    return out


def imd_build(grid, legend, tex_dir, nome='cella'):
    """Testo IMD di una cella piatta: un quadrato di 16 unità per casella, riga 0 = nord.
    Stessa struttura dell'IMD provato in gioco nel progetto precedente (documento 4.1, §6)."""
    for r, line in enumerate(grid):
        for c, ch in enumerate(line):
            if ch not in legend:
                raise GfxError('K16', 'carattere %r (riga %d, colonna %d) non è nella legenda' % (ch, r, c))
    rects = imd_rects(grid, legend)
    textures = sorted({r[0] for r in rects})
    if not textures:
        raise GfxError('K16', 'nessuna casella con texture')
    info = {t: imd_texture(os.path.join(tex_dir, t + '.png')) for t in textures}
    n = len(textures)
    out = ['<?xml version="1.0" encoding="UTF-8" standalone="no"?>', '<imd version="1.6.0">',
           '<head><create date="2026-10-27T00:00:00" host="trinacria" source="%s" user="atrisorb"/>'
           '<title>Model Data for NINTENDO NITRO-System</title>'
           '<generator name="trinacria_gfx.py" version="4.1"/></head>' % nome, '<body>']
    w = out.append
    w('<model_info pos_scale="%d" scaling_rule="standard" vertex_style="direct" magnify="1" '
      'tool_start_frame="1" tex_matrix_mode="maya" compress_node="merge" node_size="1 1" '
      'compress_material="on" material_size="%d %d" output_texture="used" '
      'force_full_weight="off" use_primitive_strip="on"/>' % (IMD_POS_SCALE, n, n))
    w('<box_test pos_scale="%d" xyz="%s %s %s" whd="%s %s %s"/>' % (
        IMD_POS_SCALE + 1, _f6(-IMD_HALF / 2), _f6(-0.125), _f6(-IMD_HALF / 2), _f6(IMD_HALF), _f6(0.25), _f6(IMD_HALF)))
    w('<tex_image_array size="%d">' % n)
    for i, t in enumerate(textures):
        x = info[t]
        w('<tex_image index="%d" name="%s" width="%d" height="%d" original_width="%d" original_height="%d" '
          'format="palette16" color0_mode="color" palette_name="%s_pl" path="%s.png"><bitmap size="%d">%s</bitmap>'
          '</tex_image>' % (i, t, x['w'], x['h'], x['w'], x['h'], t, t, x['parole'], x['bitmap']))
    w('</tex_image_array>')
    w('<tex_palette_array size="%d">' % n)
    for i, t in enumerate(textures):
        w('<tex_palette index="%d" name="%s_pl" color_size="16">%s</tex_palette>' % (i, t, info[t]['palette']))
    w('</tex_palette_array>')
    w('<material_array size="%d">' % n)
    for i, t in enumerate(textures):
        w('<material index="%d" name="%s" light0="on" light1="off" light2="off" light3="off" face="both" '
          'alpha="31" wire_mode="off" polygon_mode="modulate" polygon_id="0" fog_flag="on" '
          'depth_test_decal="off" translucent_update_depth="off" render_1_pixel="off" far_clipping="off" '
          'diffuse="25 25 25" ambient="31 31 31" specular="0 0 0" emission="0 0 0" shininess_table_flag="off" '
          'tex_image_idx="%d" tex_palette_idx="%d" tex_tiling="repeat repeat" tex_scale="1.000000 1.000000" '
          'tex_rotate="0.000000" tex_translate="0.000000 0.000000" tex_gen_mode="none"/>' % (i, t, i, i))
    w('</material_array>')
    w('<matrix_array size="1"><matrix index="0" mtx_weight="1" node_idx="0"/></matrix_array>')
    w('<polygon_array size="%d">' % n)
    tv = tq = 0
    for i, t in enumerate(textures):
        tw, th = info[t]['w'], info[t]['h']
        quads = [r for r in rects if r[0] == t]
        el = ['<mtx idx="0"/>']
        first = True
        for _, col, row, rw, rh in quads:
            x0, z0 = -IMD_HALF + col * IMD_TILE, -IMD_HALF + row * IMD_TILE
            x1, z1 = x0 + rw * IMD_TILE, z0 + rh * IMD_TILE
            for x, z, s, tt in ((x0, z0, 0, 0), (x0, z1, 0, rh * th), (x1, z1, rw * tw, rh * th), (x1, z0, rw * tw, 0)):
                el.append('<tex st="%s %s"/>' % (_f6(s), _f6(tt)))
                if first:
                    el.append('<nrm xyz="%s"/>' % IMD_NORMAL)
                    first = False
                el.append('<pos_xyz xyz="%s %s %s"/>' % (_f6(x), _f6(0.0), _f6(z)))
        nv = 4 * len(quads)
        tv += nv
        tq += len(quads)
        w('<polygon index="%d" name="polygon%d" vertex_size="%d" polygon_size="%d" triangle_size="0" '
          'quad_size="%d" volume_min="3.000000 3.000000 3.000000" volume_max="3.000000 3.000000 3.000000" '
          'volume_r="3.000000" mtx_prim_size="1" nrm_flag="on" clr_flag="off" tex_flag="on">'
          '<mtx_prim index="0"><mtx_list size="1">0</mtx_list><primitive_array size="1">'
          '<primitive index="0" type="quads" vertex_size="%d">%s</primitive></primitive_array></mtx_prim>'
          '</polygon>' % (i, i, nv, len(quads), len(quads), nv, ''.join(el)))
    w('</polygon_array>')
    w('<node_array size="1"><node index="0" name="world_root" kind="mesh" parent="-1" child="-1" '
      'brother_next="-1" brother_prev="-1" draw_mtx="on" billboard="off" scale="1.000000 1.000000 1.000000" '
      'rotate="0.000000 0.000000 0.000000" translate="0.000000 0.000000 0.000000" visibility="on" '
      'display_size="%d" vertex_size="%d" polygon_size="%d" triangle_size="0" quad_size="%d" '
      'volume_min="0.000000 0.000000 0.000000" volume_max="0.000000 0.000000 0.000000" volume_r="0.000000">'
      % (n, tv, tq, tq))
    for i in range(n):
        w('<display index="%d" material="%d" polygon="%d" priority="0"/>' % (i, i, i))
    w('</node></node_array>')
    w('<output_info vertex_size="%d" polygon_size="%d" triangle_size="0" quad_size="%d"/>' % (tv, tq, tq))
    w('</body>')
    w('</imd>')
    return '\n'.join(out) + '\n', {'texture': n, 'quadrilateri': tq, 'vertici': tv}


def imd_scena(quads, tex_dir, nome='cella', trasparenti=()):
    """IMD di una scena 3D fatta di quadrilateri (blocco 4.2): terreno, volumi degli edifici,
    sagome. Ogni quadrilatero è (texture, 4 vertici (x, y, z) in unità del mondo con l'origine al
    centro della cella, 4 coordinate (s, t) in texel). Stessa intestazione, stessi materiali e stessa
    scala dell'IMD piatto provato in gioco (imd_build); le texture in `trasparenti` hanno il colore 0
    trasparente (sagome)."""
    if not quads:
        raise GfxError('K16', 'scena vuota')
    textures = sorted({q[0] for q in quads})
    info = {t: imd_texture(os.path.join(tex_dir, t + '.png')) for t in textures}
    n = len(textures)
    k = 1.0 / 64   # unità del mondo -> unità IMD con pos_scale 6
    xs = [v[0] for q in quads for v in q[1]]
    ys = [v[1] for q in quads for v in q[1]]
    zs = [v[2] for q in quads for v in q[1]]
    b0 = (min(xs) / 128, min(ys) / 128 - 0.125, min(zs) / 128)
    b1 = ((max(xs) - min(xs)) / 128, (max(ys) - min(ys)) / 128 + 0.25, (max(zs) - min(zs)) / 128)
    out = ['<?xml version="1.0" encoding="UTF-8" standalone="no"?>', '<imd version="1.6.0">',
           '<head><create date="2026-10-27T00:00:00" host="trinacria" source="%s" user="atrisorb"/>'
           '<title>Model Data for NINTENDO NITRO-System</title>'
           '<generator name="trinacria_gfx.py" version="4.2"/></head>' % nome, '<body>']
    w = out.append
    w('<model_info pos_scale="%d" scaling_rule="standard" vertex_style="direct" magnify="1" '
      'tool_start_frame="1" tex_matrix_mode="maya" compress_node="merge" node_size="1 1" '
      'compress_material="on" material_size="%d %d" output_texture="used" '
      'force_full_weight="off" use_primitive_strip="on"/>' % (IMD_POS_SCALE, n, n))
    w('<box_test pos_scale="%d" xyz="%s %s %s" whd="%s %s %s"/>' % (
        IMD_POS_SCALE + 1, _f6(b0[0]), _f6(b0[1]), _f6(b0[2]), _f6(b1[0]), _f6(b1[1]), _f6(b1[2])))
    w('<tex_image_array size="%d">' % n)
    for i, t in enumerate(textures):
        x = info[t]
        w('<tex_image index="%d" name="%s" width="%d" height="%d" original_width="%d" original_height="%d" '
          'format="palette16" color0_mode="%s" palette_name="%s_pl" path="%s.png"><bitmap size="%d">%s</bitmap>'
          '</tex_image>' % (i, t, x['w'], x['h'], x['w'], x['h'], 'transparency' if t in trasparenti else 'color',
                            t, t, x['parole'], x['bitmap']))
    w('</tex_image_array>')
    w('<tex_palette_array size="%d">' % n)
    for i, t in enumerate(textures):
        w('<tex_palette index="%d" name="%s_pl" color_size="16">%s</tex_palette>' % (i, t, info[t]['palette']))
    w('</tex_palette_array>')
    w('<material_array size="%d">' % n)
    for i, t in enumerate(textures):
        w('<material index="%d" name="%s" light0="on" light1="off" light2="off" light3="off" face="both" '
          'alpha="31" wire_mode="off" polygon_mode="modulate" polygon_id="0" fog_flag="on" '
          'depth_test_decal="off" translucent_update_depth="off" render_1_pixel="off" far_clipping="off" '
          'diffuse="25 25 25" ambient="31 31 31" specular="0 0 0" emission="0 0 0" shininess_table_flag="off" '
          'tex_image_idx="%d" tex_palette_idx="%d" tex_tiling="repeat repeat" tex_scale="1.000000 1.000000" '
          'tex_rotate="0.000000" tex_translate="0.000000 0.000000" tex_gen_mode="none"/>' % (i, t, i, i))
    w('</material_array>')
    w('<matrix_array size="1"><matrix index="0" mtx_weight="1" node_idx="0"/></matrix_array>')
    w('<polygon_array size="%d">' % n)
    tv = tq = 0
    for i, t in enumerate(textures):
        qs = [q for q in quads if q[0] == t]
        el = ['<mtx idx="0"/>']
        first = True
        for _, verts, uvs in qs:
            for (x, y, z), (s, tt) in zip(verts, uvs):
                el.append('<tex st="%s %s"/>' % (_f6(s), _f6(tt)))
                if first:
                    el.append('<nrm xyz="%s"/>' % IMD_NORMAL)
                    first = False
                el.append('<pos_xyz xyz="%s %s %s"/>' % (_f6(x * k), _f6(y * k), _f6(z * k)))
        nv = 4 * len(qs)
        tv += nv
        tq += len(qs)
        w('<polygon index="%d" name="polygon%d" vertex_size="%d" polygon_size="%d" triangle_size="0" '
          'quad_size="%d" volume_min="3.000000 3.000000 3.000000" volume_max="3.000000 3.000000 3.000000" '
          'volume_r="3.000000" mtx_prim_size="1" nrm_flag="on" clr_flag="off" tex_flag="on">'
          '<mtx_prim index="0"><mtx_list size="1">0</mtx_list><primitive_array size="1">'
          '<primitive index="0" type="quads" vertex_size="%d">%s</primitive></primitive_array></mtx_prim>'
          '</polygon>' % (i, i, nv, len(qs), len(qs), nv, ''.join(el)))
    w('</polygon_array>')
    w('<node_array size="1"><node index="0" name="world_root" kind="mesh" parent="-1" child="-1" '
      'brother_next="-1" brother_prev="-1" draw_mtx="on" billboard="off" scale="1.000000 1.000000 1.000000" '
      'rotate="0.000000 0.000000 0.000000" translate="0.000000 0.000000 0.000000" visibility="on" '
      'display_size="%d" vertex_size="%d" polygon_size="%d" triangle_size="0" quad_size="%d" '
      'volume_min="0.000000 0.000000 0.000000" volume_max="0.000000 0.000000 0.000000" volume_r="0.000000">'
      % (n, tv, tq, tq))
    for i in range(n):
        w('<display index="%d" material="%d" polygon="%d" priority="0"/>' % (i, i, i))
    w('</node></node_array>')
    w('<output_info vertex_size="%d" polygon_size="%d" triangle_size="0" quad_size="%d"/>' % (tv, tq, tq))
    w('</body>')
    w('</imd>')
    return '\n'.join(out) + '\n', {'texture': n, 'quadrilateri': tq, 'vertici': tv}


def nsbmd_poligoni(b):
    """Poligoni (triangoli + quadrilateri) dei modelli di un NSBMD, dall'intestazione del modello."""
    mdl = u32(b, 16)
    tot = 0
    for _, d in _dict(b, mdl + 8):
        info = mdl + u32(d, 0) + 20
        tot += struct.unpack_from('<4H', b, info + 16)[1]
    return tot


G3D_DEFAULT = r'F:\Progetti\pokémon-trinacria\tools\g3dcvtr\g3dcvtr.exe'
G3D_SHA256 = '545882466f0a7e02a152aba8c87077ff9b716fc170d9232cde730db4d9c4c733'


def g3d_run(imd, out, modo, exe=None):
    """g3dcvtr.exe (solo Windows). modo: 'emdl' (modello), 'etex' (texture), 'eboth'."""
    exe = exe or os.environ.get('TRINACRIA_G3DCVTR') or G3D_DEFAULT
    if not os.path.isfile(exe):
        raise GfxError('K18', 'g3dcvtr non trovato: %s' % exe)
    if hashlib.sha256(read(exe)).hexdigest() != G3D_SHA256:
        raise GfxError('K18', 'g3dcvtr diverso da quello provato (SHA-256 del documento 4.1, §2)')
    # g3dcvtr non regge i percorsi con lettere accentate («pokémon»): lavora in una cartella temporanea
    tmp = tempfile.mkdtemp(prefix='trn_g3d_')
    try:
        t_in, t_out = os.path.join(tmp, 'in.imd'), os.path.join(tmp, 'out' + os.path.splitext(out)[1])
        with open(t_in, 'wb') as fh:
            fh.write(read(imd))
        r = subprocess.run([exe, t_in, '-' + modo, '-o', t_out], capture_output=True, text=True, errors='replace')
        if r.returncode != 0 or not os.path.isfile(t_out):
            msg = (r.stdout + r.stderr).strip().splitlines()
            raise GfxError('K18', 'g3dcvtr: ' + (msg[-1] if msg else 'codice %d' % r.returncode))
        b = read(t_out)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    with open(out, 'wb') as fh:
        fh.write(b)
    return b


# --------------------------------------------------------------------------- sprite di campo


def sprite_table(repo):
    """SPRITE_* -> MMODEL_* da asm/overlay_01_sprite_data.s (tabella del gioco)."""
    sp = defines(os.path.join(repo, 'include', 'constants', 'sprites.h'), 'SPRITE_')
    mm = defines(os.path.join(repo, 'include', 'constants', 'mmodel.h'), 'MMODEL_')
    rows = []
    for m in re.finditer(r'\.short\s+(SPRITE_\w+),\s*(MMODEL_\w+),\s*(0x[0-9A-Fa-f]+)\s*\|\s*\((\d+)\s*<<\s*10\)',
                         open(os.path.join(repo, 'asm', 'overlay_01_sprite_data.s'), encoding='utf-8').read()):
        rows.append({'sprite': m.group(1), 'sprite_id': sp.get(m.group(1)), 'mmodel': m.group(2),
                     'mmodel_id': mm.get(m.group(2)), 'param': int(m.group(3), 16), 'tipo': int(m.group(4))})
    return rows, sp, mm


def _c_array(src, name):
    m = re.search(r'%s\[\]\s*=\s*\{(.*?)\};' % name, src, re.S)
    return [x.strip() for x in re.sub(r'//[^\n]*', '', m.group(1)).split(',') if x.strip()]


def follower_tables(repo):
    """Tabelle del Pokémon a seguito: specie -> indice del modello, forme, femmina, tp_param."""
    src = open(os.path.join(repo, 'src', 'follow_mon.c'), encoding='utf-8').read()
    idx = defines(os.path.join(repo, 'include', 'constants', 'follow_mon_idx.h'), '')
    lut = _c_array(src, 'sModelIndexLUT')
    forms = [int(x, 0) for x in _c_array(src, 'sFormMaxLUT')]
    female = [x in ('TRUE', '1') for x in _c_array(src, 'sFemaleFlagLUT')]
    tp = []
    with open(os.path.join(repo, 'files', 'fielddata', 'tsurepoke', 'tp_param.csv'), encoding='utf-8') as fh:
        for r in csv.DictReader(fh):
            tp.append(r)
    return {'lut': [idx.get(x, None) if not x.isdigit() else int(x) for x in lut], 'lut_nomi': lut,
            'forme': forms, 'femmina': female, 'tp': tp, 'idx': idx}


def species_constants(repo):
    out = {}
    for m in re.finditer(r'#define\s+(SPECIES_\w+)\s+(\d+)\b', open(os.path.join(repo, 'include', 'constants', 'species.h'), encoding='utf-8').read()):
        out.setdefault(int(m.group(2)), m.group(1))
    return out


def overworld(repo):
    """Per ogni specie 1–493: sprite di campo (forma 0, femmina, forme), file mmodel, parametri."""
    rows, sp, mm = sprite_table(repo)
    by_sprite = {r['sprite_id']: r for r in rows}
    sp_name = {v: k for k, v in sp.items() if k.startswith('SPRITE_FOLLOWER_MON_')}
    ft = follower_tables(repo)
    spc = species_constants(repo)
    base = sp['SPRITE_FOLLOWER_MON_BULBASAUR']
    last = sp['SPRITE_FOLLOWER_MON_ARCEUS_DARK']
    mdir = os.path.join(repo, 'files', 'data', 'mmodel', 'mmodel')
    out = []
    for s in range(1, 494):
        off = ft['lut'][s]
        sid = base + off
        n_var = 1 + (1 if ft['femmina'][s - 1] else ft['forme'][s - 1])
        sprites = []
        for k in range(n_var):
            x = sid + k
            r = by_sprite.get(x)
            f = os.path.join(mdir, 'mmodel_%08d.NSBTX' % r['mmodel_id']) if r else None
            sprites.append({'sprite': sp_name.get(x), 'sprite_id': x, 'mmodel': r['mmodel'] if r else None,
                            'mmodel_id': r['mmodel_id'] if r else None,
                            'file': os.path.relpath(f, repo).replace('\\', '/') if f else None,
                            'esiste': bool(f and os.path.isfile(f)), 'oltre_arceus': x > last})
        tp = ft['tp'][off] if off < len(ft['tp']) else None
        out.append({'n': s, 'specie': spc.get(s), 'indice_follower': off, 'nome_indice': ft['lut_nomi'][s],
                    'femmina_diversa': ft['femmina'][s - 1], 'forme': ft['forme'][s - 1], 'sprite': sprites,
                    'troppo_alto': tp is not None and tp['too_tall'] == 'true',
                    'fluttua': tp is not None and tp['hover'] == 'true',
                    'tp_param': tp['index'] if tp else None})
    return out


def overworld_check(ow):
    errs = []
    for r in ow:
        if r['tp_param'] is None or r['tp_param'] != 'TSURE_POKE_' + r['nome_indice'][len('FOLLOWER_MON_'):]:
            errs.append(('K09', 'specie %d: riga di tp_param.csv %s, attesa %s' % (r['n'], r['tp_param'], r['nome_indice'])))
        for s in r['sprite']:
            if not s['sprite'] or not s['esiste'] or s['oltre_arceus']:
                errs.append(('K08', 'specie %d (%s): sprite %s senza file mmodel' % (r['n'], r['specie'], s['sprite'] or s['sprite_id'])))
    return errs


# --------------------------------------------------------------------------- censimento


def census(repo, rom=None, limit_narc=True):
    """Ogni file di filesystem.csv: formato, voci (NARC) e confronto con la ROM."""
    out = []
    errs = []
    nid = narc_ids(repo)
    for src, dst in filesystem(repo):
        path = os.path.join(repo, src)
        entry = {'sorgente': src, 'rom': dst}
        if os.path.isfile(path):
            b = read(path)
            entry['nel_repository'] = 'binario'
            entry['byte'] = len(b)
        elif rom is not None:
            b = rom.read(dst)
            entry['nel_repository'] = 'costruito dal build'
            entry['byte'] = len(b)
        else:
            entry['nel_repository'] = 'costruito dal build'
            out.append(entry)
            continue
        entry['formato'] = kind(b)
        if rom is not None and entry['nel_repository'] == 'binario':
            rb = rom.read(dst)
            entry['uguale_alla_rom'] = rb == b
            if rb != b:
                errs.append(('K02', '%s diverso dalla ROM originale' % src))
        if entry['formato'] == 'NARC':
            try:
                n = Narc(b)
                cnt = {}
                for f in n.files:
                    k = deep_kind(f)
                    cnt[k] = cnt.get(k, 0) + 1
                entry['voci'] = len(n.files)
                entry['contenuto'] = dict(sorted(cnt.items(), key=lambda kv: -kv[1]))
            except GfxError as e:
                errs.append((e.code, '%s: %s' % (src, e.msg)))
        key = 'NARC_' + re.sub(r'[^0-9A-Za-z]', '_', src[len('files/'):]).replace('_narc', '')
        m = re.match(r'files/a/(\d)/(\d)/(\d)$', src)
        if m:
            key = 'NARC_a_%s_%s_%s' % m.groups()
        if key in nid:
            entry['narc_id'] = nid[key]
            entry['costante'] = key
        out.append(entry)
    return out, errs


def code_users(repo, const):
    hits = []
    for d in ('src', os.path.join('src', 'field'), 'asm'):
        p = os.path.join(repo, d)
        for f in sorted(os.listdir(p)):
            fp = os.path.join(p, f)
            if os.path.isfile(fp) and f.endswith(('.c', '.s')):
                if re.search(r'\b%s\b' % const, open(fp, encoding='utf-8', errors='replace').read()):
                    hits.append(os.path.join(d, f).replace('\\', '/'))
    return hits


# --------------------------------------------------------------------------- prova nitrogfx


PREVIEW = 'files/fielddata/graphic/preview_graphic/preview_graphic'
NITRO_PROVE = [
    # (cartella del meson.build, PNG, uscita, NARC della ROM, voce o None = cercala, opzioni del meson.build)
    ('files/application/pokegear/map/pgmap_gra', 'pgmap_gra_00000001.png', '.NCGR', '/a/1/4/4', 1,
     ['-clobbersize', '-version101']),
    ('files/application/pokegear/map/pgmap_gra', 'pgmap_gra_00000010.png', '.NCGR', '/a/1/4/4', 10,
     ['-version101', '-sopc', '-bitdepth', '8']),
    ('files/application/pokegear/map/pgmap_gra', 'pgmap_gra_00000012.png', '.NCGR', '/a/1/4/4', 12,
     ['-version101', '-sopc']),
    ('files/demo/title/titledemo', 'titledemo_00000001.png', '.NCGR', '/a/0/4/6', 1,
     ['-version101', '-sopc', '-bitdepth', '8']),
    ('files/demo/title/titledemo', 'titledemo_00000015.png', '.NCGR', '/a/0/4/6', 15,
     ['-version101', '-sopc']),
    ('files/data/gs_areawindow', 'areawindow_0.png', '.NCGR', '/a/1/6/3', None, ['-version101', '-sopc']),
    ('files/data/gs_areawindow', 'areawindow_0.png', '.NCLR', '/a/1/6/3', None, []),
    (PREVIEW, 'preview_graphic_ruins_of_alph_day.png', '.NCGR.lz', '/a/1/5/0', None,
     ['-version101', '-sopc', '-bitdepth', '8', '-nopad']),
    (PREVIEW, 'preview_graphic_ruins_of_alph_day.png', '.NCLR', '/a/1/5/0', None, ['-bitdepth', '8', '-nopad']),
]


def ncgr_flags(b):
    """Opzioni di nitrogfx che riproducono un NCGR (come scripts/guess_ncgr_flags.py del progetto
    precedente): -version101, -sopc, -clobbersize, -mappingtype N, -bitdepth 8."""
    if b[:4] != b'RGCN':
        raise GfxError('K06', 'non è un NCGR')
    flags = []
    o = 16
    sopc = clobber = scanned = vram = False
    mapping = 0
    depth = 4
    for _ in range(u16(b, 14)):
        magic, size = b[o:o + 4], u32(b, o + 4)
        if magic == b'SOPC':
            sopc = True
        elif magic == b'RAHC':
            h, w, fmt, mapping = u16(b, o + 8), u16(b, o + 10), u32(b, o + 12), u32(b, o + 16)
            clobber = h == 0xFFFF
            depth = 8 if fmt == 4 else 4
            scanned = bool(b[o + 0x14])
            vram = bool(b[o + 0x15])
        o += size
    if clobber:
        flags.append('-clobbersize')
    if sopc:
        flags.append('-sopc')
    if u16(b, 6) == 0x101:
        flags.append('-version101')
    if mapping:
        flags += ['-mappingtype', str(32 * 2 ** (mapping >> 20))]
    if depth == 8:
        flags += ['-bitdepth', '8']
    if vram:
        flags.append('-vram')
    if scanned:
        # cifrato come gli sprite dei Pokémon (tools/scripts/makeotherpoke.sh): la chiave va nel file
        # <png>.key che nitrogfx scrive leggendo l'NCGR e rilegge scrivendolo
        flags.append('-scanfronttoback')
    return flags


# NCGR che stanno solo negli archivi binari: NCGR -> PNG -> NCGR con le opzioni lette dall'NCGR
NITRO_ANDATA_RITORNO = [
    # (NARC, voce NCGR, voce NCLR, larghezza in tile del PNG, cosa)
    ('/a/0/5/8', 0, 1, 10, 'fronte della classe 0 (4.4: sprite degli allenatori)'),
    ('/a/0/5/8', 4, 1, None, 'quinta voce della classe 0, NCGR scansionato e cifrato'),
    ('/a/0/0/6', 0, 1, 10, 'dorso del protagonista (4.4: dorsi dei compagni)'),
    ('/a/0/0/6', 4, 1, None, 'quinta voce del dorso, NCGR scansionato e cifrato'),
]


def nitrogfx_round_trip(rom, cmd, use_wsl, prove=None):
    res, errs = [], []
    tmp = tempfile.mkdtemp(prefix='trn_gfx_')
    for narc_path, ig, ip, width, what in prove or NITRO_ANDATA_RITORNO:
        files = Narc(rom.read(narc_path)).files
        ncgr, nclr = files[ig], files[ip]
        base = os.path.join(tmp, '%s_%d' % (narc_path.strip('/').replace('/', '_'), ig))
        with open(base + '.NCGR', 'wb') as fh:
            fh.write(ncgr)
        with open(base + '.NCLR', 'wb') as fh:
            fh.write(nclr)
        flags = ncgr_flags(ncgr)
        if width is None:
            width = u16(ncgr, 16 + 10)   # larghezza in tile scritta nell'NCGR (senza -clobbersize)
        try:
            scan = ['-scanfronttoback'] if '-scanfronttoback' in flags else []
            nitrogfx_run(cmd, [base + '.NCGR', base + '.png', '-palette', base + '.NCLR', '-width', str(width)] + scan,
                         use_wsl)
            nitrogfx_run(cmd, [base + '.png', base + '_2.NCGR'] + flags, use_wsl)
            ok = read(base + '_2.NCGR') == ncgr
            p = png_read(base + '.png')
            res.append({'rom': '%s voce %d' % (narc_path, ig), 'cosa': what, 'opzioni': flags, 'identico': ok,
                        'png': '%d×%d, %d colori' % (p['larghezza'], p['altezza'], len(p['palette']))})
            if not ok:
                errs.append(('K19', '%s voce %d: NCGR -> PNG -> NCGR diverso' % (narc_path, ig)))
        except GfxError as e:
            errs.append((e.code, e.msg))
    return res, errs


def wslpath(p):
    p = os.path.abspath(p).replace('\\', '/')
    m = re.match(r'([A-Za-z]):/(.*)', p)
    return '/mnt/%s/%s' % (m.group(1).lower(), m.group(2)) if m else p


def nitrogfx_run(cmd, args, use_wsl):
    if use_wsl:
        full = ['wsl', '-d', 'Ubuntu', '--', cmd] + [wslpath(a) if os.path.isabs(a) else a for a in args]
    else:
        full = [cmd] + args
    r = subprocess.run(full, capture_output=True, text=True, errors='replace')
    if r.returncode != 0:
        raise GfxError('K19', 'nitrogfx: ' + (r.stdout + r.stderr).strip()[-200:])


def nitrogfx_prove(repo, rom, cmd, use_wsl, prove=None):
    """PNG del repository -> NCGR con le opzioni del build: deve uscire uguale alla voce della ROM."""
    res = []
    errs = []
    tmp = tempfile.mkdtemp(prefix='trn_gfx_')
    for folder, png, ext, narc_path, voce, flags in prove or NITRO_PROVE:
        out = os.path.join(tmp, png[:-4] + ext)
        try:
            nitrogfx_run(cmd, [os.path.join(repo, folder, png), out] + flags, use_wsl)
            mine = read(out)
            files = Narc(rom.read(narc_path)).files
            if voce is None:
                voce = next((i for i, f in enumerate(files) if f == mine), None)
            ok = voce is not None and files[voce] == mine
            res.append({'png': folder + '/' + png, 'uscita': ext, 'opzioni': flags,
                        'rom': '%s voce %s' % (narc_path, voce), 'byte': len(mine), 'identico': ok})
            if not ok:
                errs.append(('K19', '%s -> %s: diverso dalla voce %s di %s' % (png, ext, voce, narc_path)))
        except GfxError as e:
            errs.append((e.code, e.msg))
    return res, errs


# --------------------------------------------------------------------------- collaudo


def selftest(repo, rom_path=None, verbose=True):
    errs = []
    log = []

    def note(s):
        log.append(s)
        if verbose:
            print(s)

    rom = Rom(rom_path) if rom_path else None
    if rom is not None:
        if sha1(rom.data) != '4fcded0e2713dc03929845de631d0932ea2b5a37':
            errs.append(('K02', 'la ROM non è la build originale (SHA-1 diverso)'))
    # 1. tutti i NARC binari del repository: pack(unpack) identico
    n_narc = n_files = 0
    for src, dst in filesystem(repo):
        p = os.path.join(repo, src)
        if not os.path.isfile(p):
            continue
        b = read(p)
        if b[:4] != b'NARC':
            continue
        try:
            n = Narc(b)
            if n.pack() != b:
                errs.append(('K01', '%s: pack(unpack) diverso' % src))
            n_narc += 1
            n_files += len(n.files)
        except GfxError as e:
            errs.append((e.code, '%s: %s' % (src, e.msg)))
    note('NARC binari del repository: %d (voci %d), riscritti identici' % (n_narc, n_files))
    # 2. land data (dagli originali: il repository può essere già modificato dai blocchi 4.2–4.3)
    try:
        land = Narc(originale(repo, 'a/0/6/5', rom))
        tiles = Narc(originale(repo, 'a/0/4/4', rom)).files
        blds = Narc(originale(repo, 'a/0/7/0', rom)).files
        areas = area_entries(originale(repo, 'a/0/4/2', rom))
    except GfxError as e:
        errs.append((e.code, e.msg))
        return errs, log
    n_ok = n_bld = 0
    mis = {'modello_cella': 0, 'edifici_cella': 0, 'bdhc_cella': 0, 'suoni_cella': 0, 'poligoni_cella': 0}
    for i, f in enumerate(land.files):
        try:
            parts = land_split(f)
            if land_join(parts) != f:
                errs.append(('K03', 'land data %d: split+join diverso' % i))
            else:
                n_ok += 1
            bl = land_buildings(parts['edifici'])
            if buildings_build(bl) != parts['edifici']:
                errs.append(('K03', 'land data %d: edifici riscritti diversi' % i))
            n_bld += len(bl)
            mis['modello_cella'] = max(mis['modello_cella'], len(parts['modello']))
            mis['edifici_cella'] = max(mis['edifici_cella'], len(parts['edifici']) // 48)
            mis['bdhc_cella'] = max(mis['bdhc_cella'], len(parts['bdhc']))
            mis['suoni_cella'] = max(mis['suoni_cella'], len(parts['suoni']))
            mis['poligoni_cella'] = max(mis['poligoni_cella'], nsbmd_poligoni(parts['modello']))
        except GfxError as e:
            errs.append((e.code, 'land data %d: %s' % (i, e.msg)))
    note('land data (a/0/6/5): %d voci, %d divise e ricomposte identiche; %d edifici riscritti identici'
         % (len(land.files), n_ok, n_bld))
    p1 = land_split(land.files[1])['permessi']
    leg = [{'carattere': chr(33 + k), 'tipo': str(t), 'collisione': str(c)}
           for k, (t, c) in enumerate(sorted(set(zip(p1[0::2], p1[1::2]))))]
    code = {(int(r['tipo']), int(r['collisione'])): r['carattere'] for r in leg}
    grid = [''.join(code[(p1[2 * (32 * r + c)], p1[2 * (32 * r + c) + 1])] for c in range(32)) for r in range(32)]
    if permissions_build(grid, leg) != p1:
        errs.append(('K03', 'permessi della voce 1 riscritti diversi'))
    # 3. dati d'area
    ntex, nbld = len(tiles), len(blds)
    mis['tileset_byte'] = max(len(f) for f in tiles)
    mis['tileset_texture'] = max(len(nsbtx_parse(f)['texture']) for f in tiles)
    mis['area_vram'] = max(sum(tex_bytes(tiles[a['tex_mappa']])) + sum(tex_bytes(blds[a['tex_edifici']])) for a in areas)
    for k, v in mis.items():
        if LIMITI[k] != v:
            errs.append(('K21', 'limite %s: %d misurato, %d nello strumento' % (k, v, LIMITI[k])))
    note('limiti R-GFX-13 ricalcolati sugli originali: %s' % ', '.join('%s %d' % kv for kv in sorted(mis.items())))
    for a in areas:
        if a['tex_mappa'] >= ntex:
            errs.append(('K05', 'area %d: tileset %d oltre i %d di a/0/4/4' % (a['indice'], a['tex_mappa'], ntex)))
        if a['tex_edifici'] >= nbld:
            errs.append(('K05', 'area %d: texture edifici %d oltre le %d di a/0/7/0' % (a['indice'], a['tex_edifici'], nbld)))
    note('dati d\'area (a/0/4/2): %d voci; tileset a/0/4/4: %d; texture edifici a/0/7/0: %d' % (len(areas), ntex, nbld))
    # 4. matrici
    mdir = os.path.join(repo, 'files', 'fielddata', 'mapmatrix', 'map_matrix')
    nm = 0
    for f in sorted(os.listdir(mdir)):
        if f.endswith('.bin'):
            b = read(os.path.join(mdir, f))
            try:
                if matrix_build(matrix_parse(b)) != b:
                    errs.append(('K04', '%s: ricostruzione diversa' % f))
                nm += 1
            except (GfxError, struct.error) as e:
                errs.append(('K04', '%s: %s' % (f, e)))
    note('matrici: %d lette e riscritte identiche' % nm)
    # 5. NSBTX dei tileset, degli edifici e degli sprite di campo
    nt = nvuote = 0
    for rel, files in (('a/0/4/4', tiles), ('a/0/7/0', blds)):
        for i, f in enumerate(files):
            if f == VUOTA:
                nvuote += 1
                continue
            try:
                t = nsbtx_parse(f)
                if not t['texture']:
                    errs.append(('K06', '%s voce %d: nessuna texture' % (rel, i)))
                nt += 1
            except (GfxError, struct.error, KeyError, IndexError) as e:
                errs.append(('K06', '%s voce %d: %s' % (rel, i, e)))
    mm = os.path.join(repo, 'files', 'data', 'mmodel', 'mmodel')
    for f in sorted(os.listdir(mm)):
        if f.endswith('.NSBTX'):
            try:
                nsbtx_parse(read(os.path.join(mm, f)))
                nt += 1
            except (GfxError, struct.error, KeyError, IndexError) as e:
                errs.append(('K06', '%s: %s' % (f, e)))
    note('NSBTX letti: %d (tileset, edifici, sprite di campo); voci vuote di 4 byte: %d' % (nt, nvuote))
    npairs, e20 = area_texture_check(repo, rom=rom)
    if len(e20) != HG_DIFETTI_TEXTURE:
        errs.append(('K20', 'mappe HeartGold con texture assenti: %d invece di %d' % (len(e20), HG_DIFETTI_TEXTURE)))
    note('texture dei modelli nel tileset dell\'area (R-GFX-12): %d coppie mappa–modello, %d difetti noti di HeartGold'
         % (npairs, len(e20)))
    # 6. sprite di campo e Follower
    rows, sp, mmc = sprite_table(repo)
    for r in rows:
        if r['sprite_id'] is None or r['mmodel_id'] is None:
            errs.append(('K07', 'riga della tabella sprite con costante sconosciuta: %s %s' % (r['sprite'], r['mmodel'])))
        elif not os.path.isfile(os.path.join(mm, 'mmodel_%08d.NSBTX' % r['mmodel_id'])) and \
                not os.path.isfile(os.path.join(mm, 'mmodel_%08d.NSBMD' % r['mmodel_id'])):
            errs.append(('K07', '%s -> %s: file mmodel_%08d mancante' % (r['sprite'], r['mmodel'], r['mmodel_id'])))
    ow = overworld(repo)
    errs += overworld_check(ow)
    nvar = sum(len(r['sprite']) for r in ow)
    note('tabella sprite: %d righe; Follower: 493 specie, %d sprite (forme e femmine comprese)' % (len(rows), nvar))
    # 7. colori 555 e PNG
    for x in range(32):
        if down8(up5(x)) != x:
            errs.append(('K13', 'scala 555: %d non torna' % x))
    tmp = tempfile.mkdtemp(prefix='trn_gfx_')
    good = os.path.join(tmp, 'buono.png')
    png_write_indexed(good, 16, 8, [(0, 0, 0), (up5(31), up5(10), 0)], [i % 2 for i in range(128)])
    bad = os.path.join(tmp, 'cattivo.png')
    png_write_indexed(bad, 12, 8, [(0, 0, 0), (250, 3, 3), (251, 4, 4)] + [(0, 0, 0)] * 15, [i % 3 + (16 if i == 5 else 0) for i in range(96)])
    if png_check(good, bpp=4):
        errs.append(('K10', 'PNG di prova buono rifiutato: %s' % png_check(good, bpp=4)))
    av = []
    codes = sorted({c for c, _ in png_check(bad, bpp=4, avvisi=av)})
    if codes != ['K12', 'K13', 'K15'] or [c for c, _ in av] != ['K14']:
        errs.append(('K10', 'PNG di prova cattivo: codici %s e avvisi %s invece di K12 K13 K15 e K14' % (codes, av)))
    npng = nzero = 0
    for root, _, fs in os.walk(os.path.join(repo, 'files')):
        for f in fs:
            if f.endswith('.png'):
                p = os.path.join(root, f)
                if os.path.getsize(p) == 0:
                    nzero += 1   # segnaposto: forma femminile uguale a quella maschile
                    continue
                e = png_check(p, come=p)
                if e:
                    errs.append((e[0][0], 'PNG del repository: %s' % e[0][1]))
                npng += 1
    note('PNG: controlli K10–K15 collaudati; %d PNG del repository passano i controlli rispetto a se stessi '
         '(%d segnaposto di 0 byte saltati)' % (npng, nzero))
    # 8. IMD
    tex = os.path.join(tmp, 'tex')
    os.makedirs(tex)
    png_write_indexed(os.path.join(tex, 'erba.png'), 32, 32, [(0, 0, 0), (up5(8), up5(20), up5(6))], [1] * 1024)
    png_write_indexed(os.path.join(tex, 'mare.png'), 32, 32, [(0, 0, 0), (up5(4), up5(12), up5(24))], [1] * 1024)
    grid = ['~' * 32] * 8 + [',' * 32] * 24
    text, st = imd_build(grid, {'~': 'mare', ',': 'erba'}, tex, 'prova')
    if st['texture'] != 2 or st['quadrilateri'] != 2:
        errs.append(('K16', 'IMD di prova: %s' % st))
    note('IMD: cella di prova con %d texture e %d quadrilateri' % (st['texture'], st['quadrilateri']))
    exe = os.environ.get('TRINACRIA_G3DCVTR') or G3D_DEFAULT
    if os.name == 'nt' and os.path.isfile(exe):
        imd = os.path.join(tmp, 'prova.imd')
        with open(imd, 'w', encoding='utf-8', newline='\n') as fh:
            fh.write(text)
        try:
            tx = nsbtx_parse(g3d_run(imd, os.path.join(tmp, 'prova.nsbtx'), 'etex', exe))
            md = nsbmd_models(g3d_run(imd, os.path.join(tmp, 'prova.nsbmd'), 'emdl', exe))
            got = sorted((t['nome'], t['formato'], t['larghezza'], t['altezza']) for t in tx['texture'])
            if got != [('erba', 'palette16', 32, 32), ('mare', 'palette16', 32, 32)] or \
                    sorted(p['colori'] for p in tx['palette']) != [16, 16] or len(md['modelli']) != 1 or md['texture']:
                errs.append(('K18', 'g3dcvtr: risultato inatteso %s %s' % (got, md)))
            # la cella nuova entra in una voce di land data al posto del modello originale
            parts = land_split(land.files[1])
            parts['modello'] = read(os.path.join(tmp, 'prova.nsbmd'))
            if land_split(land_join(parts))['modello'] != parts['modello']:
                errs.append(('K03', 'land data con il modello nuovo non si rilegge'))
            errs += limiti_cella(parts, 'cella di prova')
            tb = read(os.path.join(tmp, 'prova.nsbtx'))
            errs += limiti_tileset(tb, blds[0], 'tileset di prova')
            miss = texture_mancanti(parts['modello'], tb)
            if miss:
                errs.append(('K20', 'cella di prova: texture assenti %s' % miss))
            if texture_mancanti(parts['modello'], tiles[0]) == []:
                errs.append(('K20', 'il controllo delle texture non vede le texture mancanti'))
            note('g3dcvtr: NSBTX con 2 texture palette16 32×32 e NSBMD con 1 modello; voce di land data ricomposta')
            # scena 3D del blocco 4.2: terreno, un volume (tetto e tre facce) e una sagoma trasparente
            png_write_indexed(os.path.join(tex, 'sagoma.png'), 16, 32, [(0, 0, 0), (up5(20), up5(8), 0)],
                              [(i % 16 > 3) * 1 for i in range(512)])
            q = [('erba', [(-256, 0, -256), (-256, 0, 256), (256, 0, 256), (256, 0, -256)],
                  [(0, 0), (0, 512), (512, 512), (512, 0)])]
            for vs in (((-32, 48, -32), (-32, 48, 0), (32, 48, 0), (32, 48, -32)),
                       ((-32, 48, 0), (-32, 0, 0), (32, 0, 0), (32, 48, 0)),
                       ((-32, 48, -32), (-32, 0, -32), (-32, 0, 0), (-32, 48, 0)),
                       ((32, 48, 0), (32, 0, 0), (32, 0, -32), (32, 48, -32))):
                q.append(('mare', list(vs), [(0, 0), (0, 32), (64, 32), (64, 0)]))
            q.append(('sagoma', [(64, 32, 8), (64, 0, 8), (80, 0, 8), (80, 32, 8)], [(0, 0), (0, 32), (16, 32), (16, 0)]))
            text, st = imd_scena(q, tex, 'scena', trasparenti={'sagoma'})
            imd = os.path.join(tmp, 'scena.imd')
            with open(imd, 'w', encoding='utf-8', newline='\n') as fh:
                fh.write(text)
            mb = g3d_run(imd, os.path.join(tmp, 'scena.nsbmd'), 'emdl', exe)
            tb = g3d_run(imd, os.path.join(tmp, 'scena.nsbtx'), 'etex', exe)
            tr = {t['nome']: t['colore0_trasparente'] for t in nsbtx_parse(tb)['texture']}
            if nsbmd_poligoni(mb) != 6 or tr != {'erba': False, 'mare': False, 'sagoma': True}:
                errs.append(('K18', 'scena 3D: %d poligoni, trasparenze %s' % (nsbmd_poligoni(mb), tr)))
            note('scena 3D (blocco 4.2): %d poligoni (terreno, volume, sagoma), colore 0 trasparente solo nella sagoma'
                 % nsbmd_poligoni(mb))
        except GfxError as e:
            errs.append((e.code, e.msg))
    else:
        note('g3dcvtr: non trovato (%s), prova saltata' % exe)
    # 9. censimento (con la ROM se c'è)
    cen, e2 = census(repo, rom)
    errs += e2
    note('censimento: %d file del filesystem%s' % (len(cen), ', confrontati con la ROM' if rom else ''))
    return errs, log


# --------------------------------------------------------------------------- comandi


AREA_STRUTTURA = '<HHHBB'


def applica(repo, blocchi, build_dir, rom=None, prova=None, giallo=False):
    """Porta nel repository i manifesti dei blocchi grafici (4.2, 4.3), nell'ordine dato.

    Parte sempre dagli archivi originali (repository intatto o --rom): celle (a/0/6/5), tileset
    (a/0/4/4) e dati d'area (a/0/4/2) nuovi vanno in coda nell'ordine dei manifesti (R-GFX-09); un
    tileset con la stessa chiave di uno precedente (il tileset condiviso della matrice 0, R-GFX-18)
    lo sostituisce allo stesso indice. Nella matrice 0 cambiano solo modelli e altitudini delle celle
    elencate; le matrici nuove si scrivono intere; in src/data/map_headers.h cambia solo
    .areaDataBank delle mappe elencate. Con `prova` scrive in quella cartella invece che nel repository.
    Restituisce (errori, righe di resoconto)."""
    errs, log = [], []
    dest = prova or repo

    def scrivi(rel, b):
        p = os.path.join(dest, *rel.split('/'))
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, 'wb') as fh:
            fh.write(b)

    land = Narc(originale(repo, 'a/0/6/5', rom))
    tiles = Narc(originale(repo, 'a/0/4/4', rom))
    aree = Narc(originale(repo, 'a/0/4/2', rom))
    chiavi_ts = {}
    m0_rel = 'files/fielddata/mapmatrix/map_matrix/map_matrix_0000_EVERYWHERE.bin'
    m0 = matrix_parse(read(os.path.join(repo, *m0_rel.split('/'))))
    hdr_rel = 'src/data/map_headers.h'
    hdr = open(os.path.join(repo, *hdr_rel.split('/')), encoding='utf-8').read()
    n_mappe = 0
    for blocco in blocchi:
        bdir = os.path.join(build_dir, blocco)
        man = json.load(open(os.path.join(bdir, 'manifesto.json'), encoding='utf-8'))
        if man['prima_cella'] != len(land.files):
            errs.append(('K01', '%s: le celle cominciano a %d ma a/0/6/5 ne ha %d (blocchi in ordine?)'
                         % (blocco, man['prima_cella'], len(land.files))))
            return errs, log
        for c in man['celle']:
            land.files.append(read(os.path.join(bdir, c['file'])))
        idx_ts = {}
        for t in man['tileset']:
            b = read(os.path.join(bdir, t['file']))
            if t['chiave'] in chiavi_ts:
                tiles.files[chiavi_ts[t['chiave']]] = b
            else:
                chiavi_ts[t['chiave']] = len(tiles.files)
                tiles.files.append(b)
            idx_ts[t['indice']] = chiavi_ts[t['chiave']]
            if chiavi_ts[t['chiave']] != t['indice']:
                errs.append(('K05', '%s: tileset %s all\'indice %d invece di %d' % (blocco, t['chiave'], chiavi_ts[t['chiave']], t['indice'])))
        for a in man['aree']:
            if a['indice'] < len(aree.files):
                continue      # area già scritta da un blocco precedente con lo stesso indice
            if a['indice'] != len(aree.files):
                errs.append(('K05', '%s: area %s all\'indice %d, attesa %d' % (blocco, a['chiave'], len(aree.files), a['indice'])))
            aree.files.append(struct.pack(AREA_STRUTTURA, a['tex_edifici'], idx_ts.get(a['tileset'], a['tileset']),
                                          a['tex_dinamiche'], a['esterno'], a['luce']))
        W = m0['larghezza']
        for c in man['matrice_0']:
            i = c['y'] * W + c['x']
            m0['modelli'][i] = c['voce']
            if m0['altitudini'] is not None:
                m0['altitudini'][i] = c['altitudine']
        for mt in man['matrici']:
            m = {'larghezza': mt['larghezza'], 'altezza': mt['altezza'], 'nome': mt['nome'], 'intestazioni': None,
                 'altitudini': None, 'modelli': mt['voci']}
            scrivi('files/fielddata/mapmatrix/map_matrix/' + mt['file'], matrix_build(m))
        for mp in man['mappe']:
            val = mp.get('areaDataBank_giallo') if giallo and mp.get('areaDataBank_giallo') is not None else mp.get('areaDataBank')
            if val is None:
                errs.append(('K05', '%s: nessuna area per %s' % (blocco, mp['simbolo'])))
                continue
            for sym in (mp['simbolo'], mp['simbolo_hg']):
                pat = re.compile(r'(\[%s\]\s*=\s*\{.*?\.areaDataBank\s*=\s*)([^,\n]+)(,)' % re.escape(sym), re.S)
                hdr2, n = pat.subn(lambda mm: mm.group(1) + str(val) + mm.group(3), hdr, count=1)
                if n:
                    hdr = hdr2
                    n_mappe += 1
                    break
            else:
                errs.append(('K05', '%s: %s non trovata in map_headers.h' % (blocco, mp['simbolo'])))
        ing = man.get('ingressi')
        if ing:
            for f in ing['file']:
                for k in ('png', 'nscr'):
                    scrivi(ing['destinazione'] + '/' + f[k], read(os.path.join(bdir, ing['cartella'], f[k])))
        log.append('%s: %d celle, %d tileset, %d aree, %d celle della matrice 0, %d matrici nuove, %d anteprime'
                   % (blocco, len(man['celle']), len(man['tileset']), len(man['aree']), len(man['matrice_0']),
                      len(man['matrici']), len(ing['file']) if ing else 0))
    scrivi('files/a/0/6/5', land.pack())
    scrivi('files/a/0/4/4', tiles.pack())
    scrivi('files/a/0/4/2', aree.pack())
    scrivi(m0_rel, matrix_build(m0))
    scrivi(hdr_rel, hdr.encode('utf-8'))
    log.append('a/0/6/5: %d voci; a/0/4/4: %d; a/0/4/2: %d; areaDataBank scritto per %d mappe'
               % (len(land.files), len(tiles.files), len(aree.files), n_mappe))
    return errs, log


def print_errs(errs):
    for c, m in errs:
        print('ERRORE %s %s' % (c, m))


def main(argv=None):
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('--repo')
    ap.add_argument('--rom')
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('comando', nargs='?')
    ap.add_argument('argomenti', nargs='*')
    ap.add_argument('--out')
    ap.add_argument('--come')
    ap.add_argument('--bpp', type=int)
    ap.add_argument('--colori', type=int)
    ap.add_argument('--modello', action='store_true')
    ap.add_argument('--texture', action='store_true')
    ap.add_argument('--g3dcvtr')
    ap.add_argument('--nitrogfx')
    ap.add_argument('--wsl', action='store_true')
    ap.add_argument('--tileset')
    ap.add_argument('--edifici')
    ap.add_argument('--blocchi', nargs='*')
    ap.add_argument('--build')
    ap.add_argument('--prova')
    ap.add_argument('--polo-giallo', action='store_true')
    a = ap.parse_args(argv)
    repo = find_repo(a.repo)
    if repo is None:
        print('ERRORE K00 repository di HeartGold non trovato (--repo o TRINACRIA_REPO)')
        print('SELFTEST_FAILED' if a.selftest else 'GRAFICA_FAILED')
        return 1
    try:
        if a.selftest:
            errs, _ = selftest(repo, a.rom)
            print_errs(errs)
            print('SELFTEST_FAILED' if errs else 'SELFTEST_OK')
            return 1 if errs else 0
        c, args = a.comando, a.argomenti
        errs = []
        if c == 'censimento':
            rom = Rom(a.rom) if a.rom else None
            cen, errs = census(repo, rom)
            if a.out:
                with open(a.out, 'w', encoding='utf-8') as fh:
                    json.dump(cen, fh, ensure_ascii=False, indent=1)
            else:
                for e in cen:
                    print('%-60s %-10s %s' % (e['sorgente'], e.get('formato', '-'), e.get('voci', '')))
        elif c == 'narc' and args[:1] == ['unpack']:
            n = Narc(read(args[1]))
            os.makedirs(args[2], exist_ok=True)
            for i, f in enumerate(n.files):
                with open(os.path.join(args[2], '%04d.bin' % i), 'wb') as fh:
                    fh.write(f)
            print('%d voci in %s' % (len(n.files), args[2]))
        elif c == 'narc' and args[:1] == ['pack']:
            names = sorted(f for f in os.listdir(args[1]) if re.match(r'\d{4}\.bin$', f))
            if [int(f[:4]) for f in names] != list(range(len(names))):
                raise GfxError('K01', 'le voci devono essere 0000.bin… senza buchi')
            with open(args[2], 'wb') as fh:
                fh.write(Narc.build([read(os.path.join(args[1], f)) for f in names]).pack())
            print('%d voci in %s' % (len(names), args[2]))
        elif c == 'applica':
            build = a.build or os.path.join(PROJECT, 'build', 'grafica')
            errs, log = applica(repo, a.blocchi or ['4.2'], build, Rom(a.rom) if a.rom else None, a.prova, a.polo_giallo)
            for line in log:
                print(line)
        elif c == 'rom':
            with open(args[1], 'wb') as fh:
                fh.write(Rom(a.rom).read(args[0]))
        elif c == 'landdata' and args[:1] == ['split']:
            parts = land_split(read(args[1]))
            os.makedirs(args[2], exist_ok=True)
            for k, ext in (('suoni', 'bgs.bin'), ('permessi', 'permessi.bin'), ('edifici', 'edifici.bin'),
                           ('modello', 'modello.nsbmd'), ('bdhc', 'terreno.bdhc')):
                with open(os.path.join(args[2], ext), 'wb') as fh:
                    fh.write(parts[k])
            print(json.dumps({'edifici': land_buildings(parts['edifici'])}, ensure_ascii=False))
        elif c == 'landdata' and args[:1] == ['join']:
            d = args[1]
            parts = {k: read(os.path.join(d, ext)) for k, ext in (
                ('suoni', 'bgs.bin'), ('permessi', 'permessi.bin'), ('edifici', 'edifici.bin'),
                ('modello', 'modello.nsbmd'), ('bdhc', 'terreno.bdhc'))}
            b = land_join(parts)
            land_split(b)
            errs = limiti_cella(parts, args[2])
            with open(args[2], 'wb') as fh:
                fh.write(b)
        elif c == 'permessi':
            with open(args[1], encoding='utf-8', newline='') as fh:
                b = permissions_build(imd_read_grid(args[0]), list(csv.DictReader(fh)))
            with open(args[2], 'wb') as fh:
                fh.write(b)
            print('%s: 2048 byte' % args[2])
        elif c == 'edifici':
            with open(args[0], encoding='utf-8', newline='') as fh:
                rows = list(csv.DictReader(fh))
            b = buildings_build(rows)
            if len(rows) > LIMITI['edifici_cella']:
                errs.append(('K21', '%d edifici, il massimo è %d' % (len(rows), LIMITI['edifici_cella'])))
            with open(args[1], 'wb') as fh:
                fh.write(b)
            print('%s: %d edifici' % (args[1], len(rows)))
        elif c == 'cella':
            parts = land_split(read(args[0]))
            errs = limiti_cella(parts, os.path.basename(args[0]))
            if a.tileset:
                miss = texture_mancanti(parts['modello'], read(a.tileset))
                if miss:
                    errs.append(('K20', '%s: texture assenti nel tileset: %s' % (os.path.basename(args[0]), ', '.join(miss))))
            print('%s: %d edifici, modello %d byte, BDHC %d byte, piastre sonore %d byte' % (
                os.path.basename(args[0]), len(parts['edifici']) // 48, len(parts['modello']),
                len(parts['bdhc']), len(parts['suoni'])))
        elif c == 'tileset':
            b = read(args[0])
            errs = limiti_tileset(b, read(a.edifici) if a.edifici else None, os.path.basename(args[0]))
            t = nsbtx_parse(b)
            print('%s: %d texture, %d palette, %d+%d byte di VRAM' % (
                os.path.basename(args[0]), len(t['texture']), len(t['palette']), *tex_bytes(b)))
        elif c == 'area':
            for e in area_entries(read(os.path.join(repo, 'files', 'a', '0', '4', '2'))):
                print(json.dumps(e))
        elif c == 'matrice':
            m = matrix_parse(read(args[0]))
            print('%s %d×%d intestazioni=%s altitudini=%s' % (m['nome'], m['larghezza'], m['altezza'],
                                                             m['intestazioni'] is not None, m['altitudini'] is not None))
            for y in range(m['altezza']):
                print(' '.join('%4s' % ('.' if v == 0xFFFF else v) for v in m['modelli'][y * m['larghezza']:(y + 1) * m['larghezza']]))
        elif c == 'nsbtx':
            spec = args[0]
            if ':' in spec[2:]:
                p, i = spec.rsplit(':', 1)
                b = Narc(read(p)).files[int(i)]
            else:
                b = read(spec)
            print(json.dumps(nsbtx_parse(b) if b[:4] == b'BTX0' else nsbmd_models(b), ensure_ascii=False, indent=1))
        elif c == 'png':
            av = []
            errs = png_check(args[0], a.come, a.bpp, a.colori, av)
            for k, m in av:
                print('AVVISO %s %s' % (k, m))
            if not errs:
                p = png_read(args[0])
                print('%s: %d×%d, %d colori in palette, indici usati %d' % (
                    os.path.basename(args[0]), p['larghezza'], p['altezza'], len(p['palette']), len(set(p['pixel']))))
        elif c == 'imd':
            text, st = imd_build(imd_read_grid(args[0]), imd_read_legend(args[1]), args[2],
                                 os.path.splitext(os.path.basename(args[3]))[0])
            with open(args[3], 'w', encoding='utf-8', newline='\n') as fh:
                fh.write(text)
            print('%s: %d texture, %d quadrilateri' % (args[3], st['texture'], st['quadrilateri']))
        elif c == 'g3d':
            modo = 'emdl' if a.modello else 'etex' if a.texture else 'eboth'
            b = g3d_run(args[0], args[1], modo, a.g3dcvtr)
            info = nsbtx_parse(b) if b[:4] == b'BTX0' else nsbmd_models(b)
            print('%s: %s, %d byte, %d texture' % (args[1], kind(b), len(b), len(info['texture'])))
        elif c == 'nitrogfx':
            rom = Rom(a.rom)
            res, errs = nitrogfx_prove(repo, rom, a.nitrogfx, a.wsl)
            for r in res:
                print('%s -> %s %s = %s: %s' % (r['png'], r['uscita'], ' '.join(r['opzioni']), r['rom'],
                                                'identico' if r['identico'] else 'DIVERSO'))
            res2, e2 = nitrogfx_round_trip(rom, a.nitrogfx, a.wsl)
            errs += e2
            for r in res2:
                print('%s (%s) NCGR -> PNG %s -> NCGR %s: %s' % (r['rom'], r['cosa'], r.get('png', ''),
                                                               ' '.join(r['opzioni']),
                                                               'identico' if r['identico'] else 'DIVERSO'))
        elif c == 'opzioni-ncgr':
            print(' '.join(ncgr_flags(read(args[0]))))
        elif c == 'overworld':
            ow = overworld(repo)
            want = {x.upper() for x in args}
            for r in ow:
                if not want or str(r['n']) in want or (r['specie'] or '').upper() in want or \
                        (r['specie'] or '').upper() == 'SPECIES_' + next(iter(want), ''):
                    print(json.dumps(r, ensure_ascii=False))
        else:
            ap.print_help()
            return 2
        print_errs(errs)
        print('GRAFICA_FAILED' if errs else 'GRAFICA_OK')
        return 1 if errs else 0
    except GfxError as e:
        print('ERRORE %s %s' % (e.code, e.msg))
        print('SELFTEST_FAILED' if a.selftest else 'GRAFICA_FAILED')
        return 1


if __name__ == '__main__':
    sys.exit(main())
