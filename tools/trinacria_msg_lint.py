#!/usr/bin/env python3
"""Pokémon Trinacria - text linter for pokeheartgold message banks (files/msgdata/msg/*.json).

Checks, for every message of the given banks:
  1. every character outside {...} commands exists in tools/msgenc/charmap.txt;
  2. every printed line is <= 36 characters AND <= the pixel width of the window
     (field box: 216 px = 27 tiles x 8 px; widths from font member 0);
  3. the DS box rule: a box holds 2 lines; after "\\n" the next separator must be
     "\\r", "\\f" or the end of the message (never a third line);
  4. with --pair PRE POST: both banks have the same number of messages and the same
     {STRVAR...} commands in each message (needed by the FLAG_POST_RESIGNATION bank swap).

Placeholders are measured at their worst case: {STRVAR_1 3, 0, 0} (player name) = 7 chars
of 6 px; any other STRVAR = 10 chars of 6 px.

Usage (run from the pokeheartgold root):
    python tools/trinacria/trinacria_msg_lint.py files/msgdata/msg/msg_0829.json [more.json ...]
    python tools/trinacria/trinacria_msg_lint.py --profile battle files/msgdata/msg/msg_0728.json
    python tools/trinacria/trinacria_msg_lint.py --pair files/msgdata/msg/msg_0829.json files/msgdata/msg/msg_0830.json
    python tools/trinacria/trinacria_msg_lint.py --fix files/msgdata/msg/msg_0829.json   # ' -> ’ and " -> “ ”
Last line printed: LINT_OK or LINT_FAILED.
"""
import json
import re
import struct
import sys

MAX_CHARS = 36
PROFILES = {'field': 216, 'battle': 208, 'menu': 216}
LANG_KEY = 'en_US'
CMD_RE = re.compile(r'\{[^{}]*\}')
PLAYER_NAME = '{STRVAR_1 3, 0, 0}'


def load_charmap(root):
    chars = {}
    with open(f'{root}/tools/msgenc/charmap.txt', encoding='utf-8') as f:
        for line in f:
            body = line.split('//')[0].rstrip('\n')
            m = re.match(r'\s*([0-9A-Fa-f]{4})=(.+)$', body)
            if m and len(m.group(2)) == 1:
                chars.setdefault(m.group(2), int(m.group(1), 16))
    return chars


def load_widths(root):
    d = open(f'{root}/files/graphic/font/font_00000000.bin', 'rb').read()
    _, wds, n = struct.unpack_from('<III', d, 0)
    return d[wds:wds + n]


def message_text(entry):
    val = entry.get(LANG_KEY, '')
    return ''.join(val) if isinstance(val, list) else val


def split_lines(text):
    """Yields (line_text, separator_after) where separator is '\\n', '\\r', '\\f' or ''."""
    cur = ''
    for ch in text:
        if ch in '\n\r\f':
            yield cur, ch
            cur = ''
        else:
            cur += ch
    yield cur, ''


def measure(line, charmap, widths):
    chars = px = 0
    pos = 0
    for m in CMD_RE.finditer(line):
        for ch in line[pos:m.start()]:
            chars += 1
            code = charmap.get(ch)
            px += widths[code - 1] if code else 6
        cmd = m.group(0)
        if cmd.startswith('{STRVAR'):
            n = 7 if cmd == PLAYER_NAME else 10
            chars += n
            px += 6 * n
        pos = m.end()
    for ch in line[pos:]:
        chars += 1
        code = charmap.get(ch)
        px += widths[code - 1] if code else 6
    return chars, px


def lint_bank(path, charmap, widths, max_px, problems):
    data = json.load(open(path, encoding='utf-8'))
    for entry in data['messages']:
        mid = entry.get('id', '?')
        text = message_text(entry)
        bare = CMD_RE.sub('', text)
        for ch in bare:
            if ch in '\n\r\f':
                continue
            if ch not in charmap:
                hint = {"'": ' (use ’)', '"': ' (use “ or ”)'}.get(ch, '')
                problems.append(f'{path}: {mid}: character {ch!r} not in charmap{hint}')
        line_in_box = 1
        for line, sep in split_lines(text):
            chars, px = measure(line, charmap, widths)
            if chars > MAX_CHARS or px > max_px:
                problems.append(f'{path}: {mid}: line too long ({chars} chars, {px} px > {MAX_CHARS}/{max_px}): {line!r}')
            if sep == '\n':
                if line_in_box == 2:
                    problems.append(f'{path}: {mid}: third line in one box (use \\r or \\f): {line!r}')
                line_in_box = 2
            elif sep == '\r':
                line_in_box = 2
            elif sep == '\f':
                line_in_box = 1
    return data


def pair_check(pre_path, post_path, problems):
    pre = json.load(open(pre_path, encoding='utf-8'))['messages']
    post = json.load(open(post_path, encoding='utf-8'))['messages']
    if len(pre) != len(post):
        problems.append(f'pair: {pre_path} has {len(pre)} messages, {post_path} has {len(post)}')
    for a, b in zip(pre, post):
        ca = sorted(c for c in CMD_RE.findall(message_text(a)) if c.startswith('{STRVAR'))
        cb = sorted(c for c in CMD_RE.findall(message_text(b)) if c.startswith('{STRVAR'))
        if ca != cb:
            problems.append(f'pair: {a.get("id")} / {b.get("id")}: STRVAR differ {ca} vs {cb}')


def fix_bank(path):
    data = json.load(open(path, encoding='utf-8'))
    changed = 0
    for entry in data['messages']:
        val = entry.get(LANG_KEY)
        parts = val if isinstance(val, list) else [val]
        new_parts = []
        open_quote = True
        for p in parts:
            out = ''
            pos = 0
            for m in list(CMD_RE.finditer(p)) + [None]:
                seg = p[pos:m.start()] if m else p[pos:]
                seg = seg.replace("'", '’')
                while '"' in seg:
                    seg = seg.replace('"', '“' if open_quote else '”', 1)
                    open_quote = not open_quote
                out += seg + (m.group(0) if m else '')
                if m:
                    pos = m.end()
            new_parts.append(out)
        if new_parts != parts:
            changed += 1
            entry[LANG_KEY] = new_parts if isinstance(val, list) else new_parts[0]
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write('\n')
    print(f'{path}: fixed {changed} messages')


def main(argv):
    sys.stdout.reconfigure(encoding='utf-8')
    root = '.'
    profile = 'field'
    pairs = []
    files = []
    fix = False
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == '--profile':
            profile = argv[i + 1]
            i += 2
        elif a == '--root':
            root = argv[i + 1]
            i += 2
        elif a == '--pair':
            pairs.append((argv[i + 1], argv[i + 2]))
            files += [argv[i + 1], argv[i + 2]]
            i += 3
        elif a == '--fix':
            fix = True
            i += 1
        else:
            files.append(a)
            i += 1
    if fix:
        for p in files:
            fix_bank(p)
    charmap = load_charmap(root)
    widths = load_widths(root)
    problems = []
    for p in dict.fromkeys(files):
        lint_bank(p, charmap, widths, PROFILES[profile], problems)
    for a, b in pairs:
        pair_check(a, b, problems)
    for line in problems:
        print(line)
    print(f'checked {len(set(files))} banks, problems: {len(problems)}')
    print('LINT_OK' if not problems else 'LINT_FAILED')
    return 0 if not problems else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
