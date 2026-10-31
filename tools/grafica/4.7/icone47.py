"""Blocco 4.7 - icone del Pokegear (R-GFX-42, R-GFX-44).

`files/application/pokegear/map/pgmap_gra/pgmap_gra_00000001.png` e' un PNG indicizzato
a 4 bit, 8 pixel di larghezza x 456 di altezza (57 tile 8x8 in colonna), palette di 16
colori. Il gioco lo converte in NCGR con le opzioni CLOBBER_SIZE_VERSION101_NCGR_FLAGS
(vedi il meson.build della cartella).

Il blocco ridisegna due figure che il gioco mostra sulla mappa del Pokegear:
  - il SEGNALINO del protagonista (la testa), nella prima figura del foglio;
  - l'ICONA DEL VAGANTE, nello slot 2 del Pokegear: in HeartGold e' ancora la testa di
    Latias e in Trinacria il vagante e' un'altra specie (blocco 3.3), quindi va rifatta.

La forma del file non cambia mai (R-GFX-01): 8x456, 16 colori, 4 bit. La palette non
cambia: si usano solo gli indici gia' presenti. Niente e' copiato da HeartGold.

Uso: python -I tools/grafica/4.7/icone47.py
Esito: ICONE_OK
"""
import os
import struct
import sys
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, os.path.join(PROJ, 'tools'))
sys.stdout.reconfigure(errors='backslashreplace')

import trinacria_gfx as G          # noqa: E402

REL = 'files/application/pokegear/map/pgmap_gra/pgmap_gra_00000001.png'
W, H = 8, 456

# Le due figure del foglio (righe misurate sull'originale: 259-287 la prima figura,
# 289-320 la seconda). Lo slot 2 del Pokegear e' la seconda (blocco 3.3).
SLOT_SEGNALINO = (259, 287)
SLOT_VAGANTE = (289, 320)


def leggi_png(path):
    """-> (larghezza, altezza, bpp, palette [(r,g,b)], pixel [indici])."""
    with open(path, 'rb') as fh:
        d = fh.read()
    if d[:8] != b'\x89PNG\r\n\x1a\n':
        raise G.GfxError('K02', 'non e\' un PNG')
    pos = 8
    plte = None
    idat = b''
    w = h = bpp = 0
    while pos < len(d):
        ln = struct.unpack('>I', d[pos:pos + 4])[0]
        typ = d[pos + 4:pos + 8]
        data = d[pos + 8:pos + 8 + ln]
        if typ == b'IHDR':
            w, h, bpp, ct = struct.unpack('>IIBB', data[:10])
            if ct != 3:
                raise G.GfxError('K02', 'PNG non indicizzato')
        elif typ == b'PLTE':
            plte = [tuple(data[i:i + 3]) for i in range(0, len(data), 3)]
        elif typ == b'IDAT':
            idat += data
        pos += 12 + ln
    raw = zlib.decompress(idat)
    stride = (w * bpp + 7) // 8
    pix = [0] * (w * h)
    prev = bytearray(stride)
    o = 0
    for y in range(h):
        f = raw[o]
        o += 1
        line = bytearray(raw[o:o + stride])
        o += stride
        for x in range(stride):
            a = line[x - 1] if x >= 1 else 0
            b = prev[x]
            c = prev[x - 1] if x >= 1 else 0
            if f == 1:
                line[x] = (line[x] + a) & 255
            elif f == 2:
                line[x] = (line[x] + b) & 255
            elif f == 3:
                line[x] = (line[x] + (a + b) // 2) & 255
            elif f == 4:
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                pr = a if (pa <= pb and pa <= pc) else (b if pb <= pc else c)
                line[x] = (line[x] + pr) & 255
        for x in range(w):
            byte = line[x // 2]
            pix[y * w + x] = (byte >> 4) if x % 2 == 0 else (byte & 15)
        prev = line
    return w, h, bpp, plte, pix


def scrivi_png(path, w, h, bpp, palette, pix):
    """PNG indicizzato con la palette data, senza toccarne i colori (R-GFX-01/R-GFX-04)."""
    os.makedirs(os.path.dirname(path), exist_ok=True)

    def chunk(t, d):
        return struct.pack('>I', len(d)) + t + d + struct.pack('>I', zlib.crc32(t + d) & 0xFFFFFFFF)
    raw = bytearray()
    for y in range(h):
        raw.append(0)
        row = pix[y * w:(y + 1) * w]
        if bpp == 4:
            raw += bytes((row[x] << 4) | (row[x + 1] if x + 1 < len(row) else 0)
                         for x in range(0, w, 2))
        else:
            raw += bytes(row)
    out = b'\x89PNG\r\n\x1a\n'
    out += chunk(b'IHDR', struct.pack('>IIBBBBB', w, h, bpp, 3, 0, 0, 0))
    out += chunk(b'PLTE', b''.join(bytes(c) for c in palette))
    out += chunk(b'IDAT', zlib.compress(bytes(raw), 9)) + chunk(b'IEND', b'')
    with open(path, 'wb') as fh:
        fh.write(out)


def colori_usati(pix, y0, y1):
    """Gli indici gia' presenti nella figura, escluso lo 0 (trasparente)."""
    u = set()
    for y in range(y0, y1 + 1):
        for x in range(W):
            u.add(pix[y * W + x])
    u.discard(0)
    return sorted(u)


def pixel(pix, x, y, c):
    if 0 <= x < W and 0 <= y < 0xFFFF:
        pix[y * W + x] = c


def segnalino(pix, y0, y1, colori):
    """Il segnalino del protagonista: la testa con il berretto, vista dall'alto."""
    scuro = colori[0]
    medio = colori[len(colori) // 2]
    chiaro = colori[-1]
    cx = W // 2
    h = y1 - y0
    # berretto
    for k in range(4):
        pixel(pix, cx - 3 + k, y0 + 1 + k, medio)
        pixel(pix, cx + 2 - k, y0 + 1 + k, medio)
        pixel(pix, cx - 2 + k, y0 + 2 + k, medio)
        pixel(pix, cx + 1 - k, y0 + 2 + k, medio)
    # testa
    for y in range(y0 + 5, y0 + h - 12):
        for x in range(1, W - 1):
            pixel(pix, x, y, chiaro)
    # visiera del berretto
    for x in range(1, W - 1):
        pixel(pix, x, y0 + h - 13, scuro)
    # spalle
    for y in range(y0 + h - 11, y1 - 1):
        for x in range(0, W):
            pixel(pix, x, y, medio)
    for y in range(y0 + h - 11, y1 - 2):
        pixel(pix, cx, y, scuro)


def vagante(pix, y0, y1, colori):
    """L'icona del vagante: un quadrupede in corsa (non piu' la testa di Latias)."""
    scuro = colori[0]
    medio = colori[len(colori) // 2]
    chiaro = colori[-1]
    h = y1 - y0
    cx = W // 2
    # corpo
    for y in range(y0 + 10, y0 + 18):
        for x in range(1, W - 1):
            pixel(pix, x, y, medio)
    # testa e muso
    for y in range(y0 + 6, y0 + 12):
        for x in range(1, 4):
            pixel(pix, x, y, chiaro)
    pixel(pix, 1, y0 + 7, scuro)
    # coda alzata
    pixel(pix, W - 2, y0 + 8, chiaro)
    pixel(pix, W - 2, y0 + 9, claro_sicuro(scuro))
    # zampe
    for x in (1, 3, W - 4, W - 2):
        for y in range(y0 + 18, y0 + h - 2):
            pixel(pix, x, y, scuro)
    # criniera
    for y in range(y0 + 5, y0 + 11):
        pixel(pix, 4, y, chiaro)


def claro_sicuro(c):
    return c


def costruisci(repo, build=None):
    build = build or os.path.join(PROJ, 'build', 'grafica', '4.7')
    sorgente = os.path.join(repo, *REL.split('/'))
    w, h, bpp, palette, pix = leggi_png(sorgente)
    if (w, h, bpp) != (W, H, 4):
        raise G.GfxError('K02', 'forma inattesa: %dx%d a %d bit' % (w, h, bpp))

    prima = list(pix)
    # svuota le due figure e ridisegnale
    for y0, y1 in (SLOT_SEGNALINO, SLOT_VAGANTE):
        for y in range(y0, y1 + 1):
            for x in range(W):
                pix[y * W + x] = 0
    segnalino(pix, SLOT_SEGNALINO[0], SLOT_SEGNALINO[1],
              colori_usati(prima, SLOT_SEGNALINO[0], SLOT_SEGNALINO[1]))
    vagante(pix, SLOT_VAGANTE[0], SLOT_VAGANTE[1],
            colori_usati(prima, SLOT_VAGANTE[0], SLOT_VAGANTE[1]))

    if len(pix) != len(prima) or max(pix) > 15:
        raise G.GfxError('K02', 'indice oltre 15 o numero di pixel cambiato (R-GFX-01)')

    dest = os.path.join(build, *REL.split('/'))
    scrivi_png(dest, w, h, bpp, palette, pix)

    # prova di forma: riletto deve avere la stessa forma e la stessa palette
    w2, h2, b2, pal2, pix2 = leggi_png(dest)
    if (w2, h2, b2) != (w, h, bpp) or pal2 != palette:
        raise G.GfxError('K02', 'forma o palette cambiate nella riscrittura')
    return {'file': REL, 'sorgente': dest, 'byte': os.path.getsize(dest),
            'sha1_hg': G.sha1(open(sorgente, 'rb').read()),
            'sha1_nuovo': G.sha1(open(dest, 'rb').read()),
            'slot_segnalino': SLOT_SEGNALINO, 'slot_vagante': SLOT_VAGANTE,
            'pixel_cambiati': sum(1 for a, b in zip(prima, pix) if a != b)}


def anteprima(dati, path, scala=6):
    """PNG in scala leggibile per la revisione a schermo."""
    build = os.path.dirname(os.path.dirname(dati['sorgente']))
    w, h, bpp, palette, pix = leggi_png(dati['sorgente'])
    Wp, Hp = w * scala, h * scala
    righe = bytearray()
    for y in range(Hp):
        righe.append(0)
        for x in range(Wp):
            c = palette[pix[(y // scala) * w + (x // scala)]]
            righe += bytes(c)
    def chunk(t, d):
        return struct.pack('>I', len(d)) + t + d + struct.pack('>I', zlib.crc32(t + d) & 0xFFFFFFFF)
    out = b'\x89PNG\r\n\x1a\n'
    out += chunk(b'IHDR', struct.pack('>IIBBBBB', Wp, Hp, 8, 2, 0, 0, 0))
    out += chunk(b'IDAT', zlib.compress(bytes(righe), 9)) + chunk(b'IEND', b'')
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'wb') as fh:
        fh.write(out)
    return path


def main(argv=None):
    repo = None
    for c in (os.environ.get('TRINACRIA_REPO'), os.path.join(PROJ, '..', 'pokeheartgold'),
              r'F:\Progetti\pokeheartgold'):
        if c and os.path.isdir(c):
            repo = c
            break
    if not repo:
        raise G.GfxError('K00', 'repository di HeartGold non trovato')
    dati = costruisci(repo)
    print('icone: %s' % dati['file'])
    print('  segnalino righe %d-%d, vagante righe %d-%d' % (dati['slot_segnalino'] +
                                                            dati['slot_vagante']))
    print('  pixel cambiati %d, byte %d' % (dati['pixel_cambiati'], dati['byte']))
    anteprima(dati, os.path.join(PROJ, 'build', 'grafica', '4.7', 'anteprime', 'pgmap_icone.png'))
    print('ICONE_OK')
    return 0


if __name__ == '__main__':
    sys.exit(main())
