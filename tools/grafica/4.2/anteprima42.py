"""Anteprime PNG delle celle (vista obliqua dall'alto, come la telecamera del gioco ma senza
prospettiva): servono a guardare le celle prima della prova a schermo del 7.4. Solo libreria standard.
Scala: un pixel ogni 2 unità del mondo (una casella = 8 pixel)."""
import os
import struct
import zlib

from motore42 import Volume, Cilindro, Sagoma, Pannello, TERRENI

K = 0.7          # schiacciamento delle altezze
MARGINE = 48     # pixel sopra la cella per gli edifici alti della prima riga


def png_rgb(path, w, h, rows):
    def chunk(t, d):
        return struct.pack('>I', len(d)) + t + d + struct.pack('>I', zlib.crc32(t + d) & 0xFFFFFFFF)
    raw = bytearray()
    for row in rows:
        raw.append(0)
        raw += row
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'wb') as fh:
        fh.write(b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', w, h, 8, 2, 0, 0, 0)) +
                 chunk(b'IDAT', zlib.compress(bytes(raw), 6)) + chunk(b'IEND', b''))


class Tela:
    def __init__(self, w, h, sfondo=(16, 16, 20)):
        self.w, self.h = w, h
        self.px = [bytearray(bytes(sfondo) * w) for _ in range(h)]

    def put(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            r = self.px[y]
            r[3 * x:3 * x + 3] = bytes(c)

    def salva(self, path):
        png_rgb(path, self.w, self.h, self.px)


def campiona(tx, s, t):
    """Colore del texel (s, t) con la ripetizione; None se trasparente."""
    return tx.rgb(int(s) % tx.w, int(t) % tx.h)


def disegna(cella, texs, tela=None, ox=0, oy=0, scala=2):
    if tela is None:
        tela = Tela(512 // scala, 512 // scala + MARGINE)
        oy = MARGINE
    n = 16 // scala
    # terreno
    for r in range(32):
        for c in range(32):
            nome = TERRENI[cella.t[r][c]][0]
            if nome is None:
                continue
            tx = texs[nome]
            for py in range(n):
                for px in range(n):
                    s, t = c * 16 + px * scala, r * 16 + py * scala
                    col = campiona(tx, s, t)
                    tela.put(ox + c * n + px, oy + r * n + py, col)
    # oggetti, da nord a sud

    def fronte_z(o):
        if isinstance(o, (Volume, Cilindro)):
            return (o.r + (o.d if isinstance(o, Volume) else o.n)) * 16, 0
        if isinstance(o, Sagoma):
            return o.r * 16 + o.dz, 1
        return (o.rf + 1) * 16 + 0.5, 2
    for o in sorted(cella.ogg, key=fronte_z):
        if isinstance(o, (Volume, Cilindro)):
            w = o.w if isinstance(o, Volume) else o.n
            d = o.d if isinstance(o, Volume) else o.n
            y0 = getattr(o, 'y0', 0)
            hh = o.h
            x0, z0 = o.c * 16, o.r * 16
            x1, z1 = x0 + 16 * w, z0 + 16 * d
            tetto = texs.get(o.tetto) if o.tetto else None
            fronte = texs.get(o.fronte)
            if fronte:
                th = fronte.h
                fondo = th * -(-hh // th)
                for yy in range(0, int(hh), scala):
                    sy = oy + int((z1 - (y0 + yy) * K) / scala)
                    for xx in range(x0, x1, scala):
                        col = campiona(fronte, xx - x0, fondo - yy - 1)
                        if col:
                            tela.put(ox + xx // scala, sy, col)
            if tetto:
                for zz in range(z0, z1, scala):
                    sy = oy + int((zz - (y0 + hh) * K) / scala)
                    for xx in range(x0, x1, scala):
                        col = campiona(tetto, xx, zz)
                        if col:
                            tela.put(ox + xx // scala, sy, col)
        elif isinstance(o, (Sagoma, Pannello)):
            tx = texs[o.tex]
            if isinstance(o, Sagoma):
                wtot = o.n * tx.w
                x0 = o.c * 16 + ((16 * (o.lc or 1) - tx.w) / 2 if o.n == 1 else 0)
                z = o.r * 16 + o.dz
            else:
                wtot = tx.w
                x0 = o.c * 16
                z = (o.rf + 1) * 16 + 0.5
            for yy in range(0, tx.h, scala):
                sy = oy + int((z - (o.y0 + tx.h - yy) * K) / scala)
                for xx in range(0, int(wtot), scala):
                    col = campiona(tx, xx, yy)
                    if col:
                        tela.put(ox + int((x0 + xx) / scala), sy, col)
    # Centro Pokémon di HeartGold (modelli 40 e 15): segnaposto rosso
    for idx, x, y, z in cella.hg:
        if idx != 40:
            continue
        cx, cz = x + 256, z + 256 + 24
        for zz in range(int(cz - 64), int(cz + 8), scala):
            for xx in range(int(cx - 40), int(cx + 40), scala):
                tela.put(ox + xx // scala, oy + int((zz - 48 * K) / scala), (200, 56, 48))
        for yy in range(0, 48, scala):
            for xx in range(int(cx - 40), int(cx + 40), scala):
                c = (232, 224, 208) if abs(xx - cx) > 8 or yy > 28 else (90, 140, 200)
                tela.put(ox + xx // scala, oy + int((cz + 8 - yy * K) / scala), c)
    return tela
