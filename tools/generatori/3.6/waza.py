"""Elenca i dati delle mosse da waza_tbl.narc, per scrivere le descrizioni.
Uso: python -I tools/generatori/3.6/waza.py <da> <a> <file json di uscita>   (es. 121 240 mosse.json)
"""
import json, os, struct, sys, re
REPO = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..', 'pokeheartgold'))

def narc_members(path):
    d = open(path, 'rb').read()
    assert d[:4] == b'NARC'
    off = struct.unpack_from('<H', d, 12)[0]
    assert d[off:off + 4] == b'BTAF'
    sz, n = struct.unpack_from('<IH', d, off + 4)
    fat = [struct.unpack_from('<II', d, off + 12 + 8 * i) for i in range(n)]
    o2 = off + sz
    assert d[o2:o2 + 4] == b'BTNF'
    o3 = o2 + struct.unpack_from('<I', d, o2 + 4)[0]
    assert d[o3:o3 + 4] == b'GMIF'
    base = o3 + 8
    return [d[base + a:base + b] for a, b in fat]

TYPES = ['NORMAL', 'FIGHTING', 'FLYING', 'POISON', 'GROUND', 'ROCK', 'BUG', 'GHOST', 'STEEL', 'MYSTERY', 'FIRE', 'WATER',
         'GRASS', 'ELECTRIC', 'PSYCHIC', 'ICE', 'DRAGON', 'DARK']
CAT = ['fisica', 'speciale', 'stato']
mem = narc_members(REPO + '/files/poketool/waza/waza_tbl.narc')
moves_h = open(REPO + '/include/constants/moves.h', encoding='utf-8').read()
sym = {int(n): s for s, n in re.findall(r'#define\s+(MOVE_\w+)\s+(\d+)', moves_h) if not s.startswith('MOVE_ATTRIBUTE_')}
names = json.load(open(REPO + '/files/msgdata/msg/msg_0750.json', encoding='utf-8'))['messages']
descs = json.load(open(REPO + '/files/msgdata/msg/msg_0749.json', encoding='utf-8'))['messages']
out = []
lo, hi = int(sys.argv[1]), int(sys.argv[2])
for i in range(lo, hi + 1):
    m = mem[i]
    eff, cat, pw, ty, acc, pp, ch, rng, pri, flg = struct.unpack_from('<HBBBBBBHbB', m, 0)
    out.append({'n': i, 'simbolo': sym.get(i), 'originale': names[i]['en_US'], 'tipo': 'TYPE_' + TYPES[ty],
                'classe': CAT[cat], 'potenza': pw, 'precisione': acc, 'pp': pp, 'effetto': eff, 'prob': ch,
                'bersaglio': rng, 'priorita': pri, 'flag': flg, 'desc_en': ''.join(descs[i]['en_US']).replace('\n', ' ').strip()})
print(len(mem))
json.dump(out, open(sys.argv[3], 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
for o in out:
    print(o['n'], o['simbolo'], o['originale'], o['tipo'][5:], o['classe'], o['potenza'], o['precisione'], o['pp'], 'eff', o['effetto'], 'ch', o['prob'], 'rng', o['bersaglio'], 'pri', o['priorita'], '|', o['desc_en'])
