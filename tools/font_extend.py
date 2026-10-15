#!/usr/bin/env python3
"""Pokémon Trinacria - font table extension for pokeheartgold.

Adds 16 new characters (« » € – — [ ] < > | ^ ` £ § © ±) into the 16 glyph slots
0x01ED-0x01FC, which are unmapped in tools/msgenc/charmap.txt and blank in the font.
Glyphs are written into font members 0, 1, 2, 4 and 10 (member 3 is the special
font used only by ScrCmd_527 and is left untouched). The shadow pixels are derived
from the ink pixels with the same rule the original glyphs follow (right, down,
down-right), so new glyphs match the HeartGold style.

Usage (run from the pokeheartgold root):
    python tools/trinacria/font_extend.py check     # verifies slots are free, self-tests the codec
    python tools/trinacria/font_extend.py apply     # patches font.narc, font/*.bin, charmap.txt
    python tools/trinacria/font_extend.py specimen out.png   # renders all new glyphs (needs Pillow)

Every command prints a final line FONT_OK or FONT_FAILED.
"""
import os
import struct
import sys

ROOT = os.getcwd()
NARC = os.path.join(ROOT, 'files', 'graphic', 'font.narc')
BIN_DIR = os.path.join(ROOT, 'files', 'graphic', 'font')
CHARMAP = os.path.join(ROOT, 'tools', 'msgenc', 'charmap.txt')
MEMBERS = (0, 1, 2, 4, 10)
GLYPH_BYTES = 64
TOP_ROW = 3  # first row of the cap height in the original glyphs

# Ink bitmaps: '#' = ink, '.' = empty. Row 0 of each list is font row TOP_ROW (3).
NEW_GLYPHS = [
    (0x01ED, '«', ['', '', '..#.#', '.#.#.', '#.#..', '.#.#.', '..#.#']),
    (0x01EE, '»', ['', '', '#.#..', '.#.#.', '..#.#', '.#.#.', '#.#..']),
    (0x01EF, '€', ['..###', '.#...', '#....', '####.', '#....', '####.', '#....', '.#...', '..###']),
    (0x01F0, '–', ['', '', '', '', '######']),
    (0x01F1, '—', ['', '', '', '', '#########']),
    (0x01F2, '[', ['###', '#..', '#..', '#..', '#..', '#..', '#..', '#..', '#..', '###']),
    (0x01F3, ']', ['###', '..#', '..#', '..#', '..#', '..#', '..#', '..#', '..#', '###']),
    (0x01F4, '<', ['', '', '...#', '..#.', '.#..', '#...', '.#..', '..#.', '...#']),
    (0x01F5, '>', ['', '', '#...', '.#..', '..#.', '...#', '..#.', '.#..', '#...']),
    (0x01F6, '|', ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#']),
    (0x01F7, '^', ['..#..', '.#.#.', '#...#']),
    (0x01F8, '`', ['#.', '.#']),
    (0x01F9, '£', ['..##.', '.#..#', '.#...', '####.', '.#...', '.#...', '.#...', '#.#..', '#####']),
    (0x01FA, '§', ['.###', '#...', '.##.', '#..#', '#..#', '.##.', '...#', '###.']),
    (0x01FB, '©', ['.#####.', '#.....#', '#..##.#', '#.#...#', '#.#...#', '#..##.#', '#.....#', '.#####.']),
    (0x01FC, '±', ['', '..#..', '..#..', '#####', '..#..', '..#..', '', '#####']),
]


def decode_glyph(raw):
    grid = [[0] * 16 for _ in range(16)]
    for t in range(4):
        tx, ty = (t % 2) * 8, (t // 2) * 8
        for r in range(8):
            b0, b1 = raw[t * 16 + r * 2], raw[t * 16 + r * 2 + 1]
            px = [(b1 >> 6) & 3, (b1 >> 4) & 3, (b1 >> 2) & 3, b1 & 3,
                  (b0 >> 6) & 3, (b0 >> 4) & 3, (b0 >> 2) & 3, b0 & 3]
            for c in range(8):
                grid[ty + r][tx + c] = px[c]
    return grid


def encode_glyph(grid):
    out = bytearray(GLYPH_BYTES)
    for t in range(4):
        tx, ty = (t % 2) * 8, (t // 2) * 8
        for r in range(8):
            px = [grid[ty + r][tx + c] for c in range(8)]
            b1 = (px[0] << 6) | (px[1] << 4) | (px[2] << 2) | px[3]
            b0 = (px[4] << 6) | (px[5] << 4) | (px[6] << 2) | px[7]
            out[t * 16 + r * 2] = b0
            out[t * 16 + r * 2 + 1] = b1
    return bytes(out)


def build_grid(rows):
    """Returns (grid, width). 1 = ink, 2 = shadow, 3 = cell background, 0 = outside."""
    ink = set()
    for r, line in enumerate(rows):
        for c, ch in enumerate(line):
            if ch == '#':
                ink.add((TOP_ROW + r, c))
    if not ink:
        raise ValueError('empty glyph')
    max_col = max(c for _, c in ink)
    width = max_col + 2
    grid = [[0] * 16 for _ in range(16)]
    for r in range(TOP_ROW, 14):
        for c in range(width):
            grid[r][c] = 3
    for (r, c) in ink:
        grid[r][c] = 1
    for (r, c) in ink:
        for dr, dc in ((0, 1), (1, 0), (1, 1)):
            rr, cc = r + dr, c + dc
            if rr < 16 and cc < 16 and (rr, cc) not in ink:
                grid[rr][cc] = 2
    return grid, width


def read_charmap():
    codes, chars = {}, {}
    with open(CHARMAP, encoding='utf-8') as f:
        for line in f:
            body = line.split('//')[0].rstrip('\n')
            if '=' not in body:
                continue
            code, _, val = body.strip().partition('=')
            try:
                c = int(code, 16)
            except ValueError:
                continue
            codes.setdefault(c, val)
            chars.setdefault(val, c)
    return codes, chars


def narc_layout(data):
    fatb = data.find(b'BTAF')
    count = struct.unpack_from('<H', data, fatb + 8)[0]
    entries = [struct.unpack_from('<II', data, fatb + 12 + 8 * k) for k in range(count)]
    gmif = data.find(b'GMIF')
    return gmif + 8, entries


def check():
    ok = True
    codes, chars = read_charmap()
    narc = open(NARC, 'rb').read()
    base, entries = narc_layout(narc)
    for m in MEMBERS:
        path = os.path.join(BIN_DIR, f'font_{m:08d}.bin')
        member = open(path, 'rb').read()
        start, end = entries[m]
        if narc[base + start: base + end] != member:
            print(f'ERROR member {m}: {path} differs from font.narc member {m}')
            ok = False
        hs, wds, n = struct.unpack_from('<III', member, 0)
        for i in range(n):  # codec self-test on every original glyph
            raw = member[hs + i * GLYPH_BYTES: hs + (i + 1) * GLYPH_BYTES]
            if encode_glyph(decode_glyph(raw)) != raw:
                print(f'ERROR member {m}: codec round-trip failed on glyph {i}')
                ok = False
                break
        for code, ch, _ in NEW_GLYPHS:
            raw = member[hs + (code - 1) * GLYPH_BYTES: hs + code * GLYPH_BYTES]
            already = codes.get(code) == ch
            if any(raw) and not already:
                print(f'ERROR member {m}: slot {code:#06x} is not blank')
                ok = False
    for code, ch, _ in NEW_GLYPHS:
        if code in codes and codes[code] != ch:
            print(f'ERROR charmap: {code:04X} already maps to {codes[code]!r}')
            ok = False
        if ch in chars and chars[ch] != code:
            print(f'ERROR charmap: {ch!r} already mapped to {chars[ch]:04X}')
            ok = False
    return ok


def apply():
    if not check():
        return False
    codes, _ = read_charmap()
    narc = bytearray(open(NARC, 'rb').read())
    base, entries = narc_layout(narc)
    for m in MEMBERS:
        path = os.path.join(BIN_DIR, f'font_{m:08d}.bin')
        member = bytearray(open(path, 'rb').read())
        hs, wds, n = struct.unpack_from('<III', member, 0)
        for code, ch, rows in NEW_GLYPHS:
            grid, width = build_grid(rows)
            member[hs + (code - 1) * GLYPH_BYTES: hs + code * GLYPH_BYTES] = encode_glyph(grid)
            member[wds + code - 1] = width
        open(path, 'wb').write(member)
        start, end = entries[m]
        assert end - start == len(member)
        narc[base + start: base + end] = member
    open(NARC, 'wb').write(narc)
    missing = [(code, ch) for code, ch, _ in NEW_GLYPHS if codes.get(code) != ch]
    if missing:
        raw = open(CHARMAP, 'rb').read()
        eol = '\r\n' if b'\r\n' in raw else '\n'  # charmap.txt is checked out as CRLF (.gitattributes)
        lead = '' if raw.endswith(b'\n') else eol
        with open(CHARMAP, 'a', encoding='utf-8', newline='') as f:
            f.write(lead + eol + '// Pokemon Trinacria: extra glyphs (tools/trinacria/font_extend.py)' + eol)
            for code, ch in missing:
                f.write(f'{code:04X}={ch}{eol}')
    print(f'patched members {MEMBERS}, added {len(missing)} charmap lines')
    return True


def specimen(out_png):
    from PIL import Image
    member = open(os.path.join(BIN_DIR, 'font_00000000.bin'), 'rb').read()
    hs, wds, n = struct.unpack_from('<III', member, 0)
    pal = {0: (255, 255, 255), 1: (64, 64, 64), 2: (200, 200, 200), 3: (248, 248, 248)}
    img = Image.new('RGB', (16 * len(NEW_GLYPHS) * 4, 16 * 4), 'white')
    for k, (code, _, _) in enumerate(NEW_GLYPHS):
        grid = decode_glyph(member[hs + (code - 1) * GLYPH_BYTES: hs + code * GLYPH_BYTES])
        for r in range(16):
            for c in range(16):
                for dy in range(4):
                    for dx in range(4):
                        img.putpixel((k * 64 + c * 4 + dx, r * 4 + dy), pal[grid[r][c]])
    img.save(out_png)
    print('specimen written to', out_png)
    return True


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'check'
    try:
        ok = {'check': check, 'apply': apply}.get(cmd, lambda: specimen(sys.argv[2]))()
    except Exception as e:  # noqa: BLE001
        print('ERROR', e)
        ok = False
    print('FONT_OK' if ok else 'FONT_FAILED')
    sys.exit(0 if ok else 1)
