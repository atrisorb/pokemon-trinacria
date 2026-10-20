#!/usr/bin/env python3
"""Pokemon Trinacria - controllo dei blocchi delle specie e del piano degli incontri (Modulo 3, blocchi 3.1-3.5;
D08 dal 3.2, sciami e radio in D08 e vaganti V01-V05 dal 3.3).

Uso (dalla cartella di F:\\Progetti\\pokémon-sicilia oppure da F:\\Progetti\\pokeheartgold):
    python -I tools/trinacria_dex_check.py --selftest
    python -I tools/trinacria_dex_check.py check docs/MODULO_3/3.1_POKEMON_1-100.json [blocchi 3.2-3.5]
           --plan docs/MODULO_3/3.1_PIANO_INCONTRI.json [--repo F:/Progetti/pokeheartgold] [--docs <docs>]
    python -I tools/trinacria_dex_check.py export --plan docs/MODULO_3/3.1_PIANO_INCONTRI.json --repo <pokeheartgold>
           [--vaganti docs/MODULO_3/3.3_POKEMON_201-300.json] [--write]

Ultima riga stampata: DEX_OK / EXPORT_OK / SELFTEST_OK (oppure *_FAILED).
Ogni problema e' una riga "ERRORE <codice> <dove>: <messaggio>".
Senza --write il comando export non modifica nulla: elenca i file e le voci che cambierebbe.
"""
import argparse
import collections
import glob
import json
import os
import re
import struct
import sys

# ----------------------------------------------------------------------------------------------
# Limiti del blocco 3.0 (L-01, L-02, L-12, D-01) e formato delle misure (R-SPE-06)

NAME_LIMIT = (10, 60)
ART_LIMIT = (20, 76)
CAT_LIMIT = (19, 110)
DEX_PROFILE = (3, 43, 222)
MAX_BANKS = 255
LAND, SURF, ROCK, FISH = 12, 5, 2, 5
SAFARI_AREAS, SAFARI_SLOTS = 12, 10
MITICI = {'SPECIES_' + x for x in 'MEW CELEBI JIRACHI DEOXYS PHIONE MANAPHY DARKRAI SHAYMIN ARCEUS'.split()}
EVO_METHODS = {'EVO_LEVEL', 'EVO_STONE', 'EVO_ITEM_DAY', 'EVO_ITEM_NIGHT'}
UNO_RE = re.compile(r'(?i)(s[^aeiouàèéìòù]|z|gn|ps|x|y)')
KG_RE = re.compile('^\u2009*([0-9]{1,3}),([0-9]) kg$')
M_RE = re.compile('^\u2009*([0-9]{1,2}),([0-9]) m$')
CMD_RE = re.compile(r'\{[^{}]*\}')

# larghezze del membro 0 di files/graphic/font.narc (lette il 18/10/2026); con --repo si leggono dal font vero
WIDTHS = {c: 6 for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdeghkmnopqrstuvwxyz0123456789-!?…()“”àèéòùÀÈÉÌÒÙçëüñ\u2009'}
WIDTHS.update({'i': 3, 'l': 4, 'ì': 4, 'î': 4, ' ': 4, 'f': 5, 'j': 5, '’': 5, '.': 5, ',': 5, ':': 5, ';': 5})

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DOCS = [os.path.join(HERE, '..', 'docs'), 'F:/Progetti/pokémon-sicilia/docs']
DEFAULT_REPOS = [os.path.join(HERE, '..', '..', 'pokeheartgold'), 'F:/Progetti/pokeheartgold']
REGISTRI = ['2.1_MAPS_CT_SR_RG.json', '2.2_MAPS_CL_AG_TP.json', '2.3_MAPS_ME_PA_EN_ROADS.json']

# ----------------------------------------------------------------------------------------------


class Report:
    def __init__(self, quiet=False):
        self.errors = []
        self.quiet = quiet

    def err(self, code, where, msg):
        self.errors.append((code, where, msg))
        if not self.quiet:
            print('ERRORE %s %s: %s' % (code, where, msg))

    def codes(self):
        return sorted(set(c for c, _, _ in self.errors))


class Font:
    def __init__(self, repo=None):
        self.widths = dict(WIDTHS)
        self.charmap = None
        if repo:
            cm = {}
            with open(os.path.join(repo, 'tools', 'msgenc', 'charmap.txt'), encoding='utf-8') as f:
                for line in f:
                    m = re.match(r'\s*([0-9A-Fa-f]{4})=(.+)$', line.split('//')[0].rstrip('\n'))
                    if m and len(m.group(2)) == 1:
                        cm.setdefault(m.group(2), int(m.group(1), 16))
            data = open(os.path.join(repo, 'files', 'graphic', 'font', 'font_00000000.bin'), 'rb').read()
            _, wds, n = struct.unpack_from('<III', data, 0)
            table = data[wds:wds + n]
            self.charmap = cm
            self.widths = {c: table[code - 1] for c, code in cm.items() if 0 < code <= n}

    def px(self, s):
        return sum(self.widths.get(c, 6) for c in CMD_RE.sub('', s))

    def known(self, c):
        return c in self.charmap if self.charmap is not None else c in WIDTHS


def vis(s):
    return len(CMD_RE.sub('', s))


def load_json(path):
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def find_docs(arg):
    for d in ([arg] if arg else []) + DEFAULT_DOCS:
        if d and os.path.isfile(os.path.join(d, 'MODULO_3', '3.0_REGOLE_E_GLOSSARIO.json')):
            return d
    return None


def repo_species(repo):
    if not repo:
        return None
    txt = open(os.path.join(repo, 'include', 'constants', 'species.h'), encoding='utf-8').read()
    return {m.group(1): int(m.group(2)) for m in re.finditer(r'#define\s+(SPECIES_\w+)\s+(\d+)', txt)}


def repo_items(repo):
    if not repo:
        return None
    txt = open(os.path.join(repo, 'include', 'constants', 'items.h'), encoding='utf-8').read()
    return set(re.findall(r'#define\s+(ITEM_\w+)', txt))

# ----------------------------------------------------------------------------------------------
# Blocchi delle specie


def article(name):
    return ('uno ' if UNO_RE.match(name) else 'un ') + '{COLOR 255}' + name + '{COLOR 0}'


def check_species(paths, glossary, rep, font, species_ids=None, entries=None):
    seen = {}
    names = {}
    for e in glossary:
        if e.get('categoria') == 'specie' and isinstance(e.get('sostituisce'), dict):
            names[e['sostituisce'].get('indice')] = e
    for p in paths:
        try:
            j = load_json(p)
            block = j['specie']
        except Exception as ex:  # noqa: BLE001
            rep.err('D00', os.path.basename(p), 'file illeggibile o senza «specie» (%s)' % ex)
            continue
        for e in j.get('glossario_aggiunte', []):
            if e.get('categoria') == 'specie' and isinstance(e.get('sostituisce'), dict):
                names[e['sostituisce'].get('indice')] = e
        for s in block:
            n = s.get('n')
            where = '%s n.%s %s' % (os.path.basename(p), n, s.get('nome'))
            if not isinstance(n, int) or not 1 <= n <= 493 or n in seen:
                rep.err('D06', where, 'numero fuori intervallo o ripetuto')
                continue
            seen[n] = p
            if entries is not None:
                entries.append((p, s))
            if species_ids is not None and species_ids.get(s.get('simbolo')) != n:
                rep.err('D06', where, 'il simbolo %s non vale %d in species.h' % (s.get('simbolo'), n))
            nm = s.get('nome', '')
            art = s.get('con_articolo', '')
            if len(nm) > NAME_LIMIT[0] or font.px(nm) > NAME_LIMIT[1]:
                rep.err('D01', where, '%d caratteri, %d px oltre L-01' % (len(nm), font.px(nm)))
            if art != article(nm) or vis(art) > ART_LIMIT[0] or font.px(art) > ART_LIMIT[1]:
                rep.err('D01', where, 'forma con l’articolo «%s» sbagliata o oltre L-02 (%d px)' % (art, font.px(art)))
            g = names.get(n)
            if not g or g.get('forma') != nm or g.get('id') != s.get('glossario'):
                rep.err('D05', where, 'nome assente dal Glossario o diverso (%s)' % (g.get('forma') if g else '—'))
            cat = s.get('categoria', '')
            if not cat.startswith('Pokémon ') or vis(cat) > CAT_LIMIT[0] or font.px(cat) > CAT_LIMIT[1]:
                rep.err('D02', where, 'categoria «%s» (%d px) oltre L-12' % (cat, font.px(cat)))
            lines = s.get('atlante') or []
            ok = 1 <= len(lines) <= DEX_PROFILE[0]
            for L in lines:
                if '\n' in L or vis(L) > DEX_PROFILE[1] or font.px(L) > DEX_PROFILE[2] or \
                        any(not font.known(c) for c in L):
                    ok = False
            msg = s.get('msg_0803') or []
            if msg != [x + '\n' for x in lines[:-1]] + lines[-1:]:
                ok = False
            if not ok:
                rep.err('D03', where, 'voce dell’Atlante fuori dal profilo D-01: %s' % ' | '.join(lines))
            if not KG_RE.match(s.get('peso', '')) or not M_RE.match(s.get('altezza', '')) or \
                    len(s.get('peso', '')) != 8 or len(s.get('altezza', '')) != 6:
                rep.err('D04', where, 'misure «%s» «%s» fuori formato' % (s.get('peso'), s.get('altezza')))
            b = s.get('banchi') or {}
            if b.get('msg_0237') != nm or b.get('msg_0238') != art or b.get('msg_0816') != cat or \
                    b.get('msg_0803') != msg or b.get('msg_0812') != s.get('peso') or b.get('msg_0814') != s.get('altezza'):
                rep.err('D07', where, 'banchi diversi dai campi della voce')
        for row in (j.get('misure_pokedex') or {}).get('valori', []):
            for k, rx in (('msg_0812', KG_RE), ('msg_0813', KG_RE), ('msg_0814', M_RE), ('msg_0815', M_RE)):
                if k in row and not rx.match(row[k]):
                    rep.err('D04', 'misure n.%s' % row.get('n'), '%s «%s» fuori formato' % (k, row[k]))
    return len(seen)

# ----------------------------------------------------------------------------------------------
# Piano degli incontri


def load_maps(docs):
    out = {}
    for f in REGISTRI:
        p = os.path.join(docs, 'MODULO_2', f) if docs else None
        if p and os.path.isfile(p):
            for m in load_json(p)['mappe']:
                out[m['simbolo']] = m
    return out


def mon_species(mon):
    s = mon.get('species')
    return list(s.values()) if isinstance(s, dict) else [s]

# ----------------------------------------------------------------------------------------------
# Distribuzione ricavata dal piano (R-SPE-07, R-INC-07): stesso calcolo per i blocchi 3.1-3.5

TIMES = ('morn', 'day', 'nite')
# probabilita' degli slot (src/field/encounter_check.c, EncounterSlot_WildMonSlotRoll_*)
PROB = {'erba': [20, 20, 10, 10, 10, 10, 5, 5, 4, 4, 1, 1], 'surf': [60, 30, 5, 4, 1], 'canne': [40, 30, 15, 10, 5],
        'spaccaroccia': [80, 20], 'bottintesta': [50, 15, 15, 10, 5, 5]}
NIGHT_FISH_SLOT = {'good_rod': 3, 'super_rod': 1}
SAFARI_ENTRANCE = 'SR_VENDICARI_RISERVA'  # ultimo banco: copia di D47R0102, mai usato per gli incontri
SAFARI_MAP = 'MAP_SR_VENDICARI_ZONA_01…14'
SAFARI_WATER = (('surf', 'surf'), ('oldrod', 'Canna Vecchia'), ('goodrod', 'Canna Buona'), ('superrod', 'Super Canna'))
FISH_RODS = (('old_rod', 'Canna Vecchia'), ('good_rod', 'Canna Buona'), ('super_rod', 'Super Canna'))
SWARM_FISH_SLOTS = {'old_rod': (2,), 'good_rod': (0, 2, 3), 'super_rod': (0, 1, 2, 3, 4)}
SWARM_NOTE = 'solo nei giorni dello sciame su questa mappa (sSwarmMapLUT)'
RADIO = (('hoenn', 'radio (Hoenn)'), ('sinnoh', 'radio (Sinnoh)'))
RADIO_NOTE = 'col programma del Pokégear acceso (post-game)'


def dist_row(maps, mp, metodo, lv, perc, ora, nota=None):
    m = maps.get(mp) or {}
    r = {'mappa': mp, 'comune': m.get('comune'), 'provincia': m.get('provincia'), 'metodo': metodo,
         'livelli': [min(lv), max(lv)], 'percentuale': perc}
    if nota is not None:
        r['nota'] = nota
    r['ora'] = ora
    return r


def safari_row(metodo, lv, perc, ora, nota):
    return {'mappa': SAFARI_MAP, 'comune': 'Noto', 'provincia': 'SR', 'metodo': metodo,
            'livelli': [min(lv), max(lv)], 'percentuale': perc, 'nota': nota, 'ora': ora}


def swarm_rows(maps, mp, e, swarms, sp):
    """R-SPE-15: sciami delle 20 righe di sSwarmMapLUT (src/field/encounter_check.c, EncSlots_Update_*Swarm):
    erba = slot 0-1, surf = slot 0, canne = slot 2 (Vecchia), 0/2/3 (Buona), 0-4 (Super)."""
    rows = []
    for r in swarms:
        if r['specie'] != sp:
            continue
        if r['tipo'] == 'erba':
            mons = e['land']['mons'][:2]
            rows.append(dist_row(maps, mp, 'sciame (erba)', [m['level'] for m in mons], sum(PROB['erba'][:2]), 'sempre', SWARM_NOTE))
        elif r['tipo'] == 'surf':
            m = e['surf']['mons'][0]
            rows.append(dist_row(maps, mp, 'sciame (surf)', [m['level']['min'], m['level']['max']], PROB['surf'][0], 'sempre', SWARM_NOTE))
        else:
            for key, name in FISH_RODS:
                mons = e['fishing'][key]['mons']
                slots = [i for i in SWARM_FISH_SLOTS[key] if i < len(mons)]
                if slots:
                    lv = [x for i in slots for x in (mons[i]['level']['min'], mons[i]['level']['max'])]
                    rows.append(dist_row(maps, mp, 'sciame (%s)' % name, lv, sum(PROB['canne'][i] for i in slots), 'sempre', SWARM_NOTE))
    return rows


def radio_rows(maps, mp, e, sp):
    """R-SPE-15: suoni di Hoenn e Sinnoh del Pokégear (EncSlotArray_Update_HoennSinnohSounds): la prima specie
    prende gli slot 2-3 dell'erba, la seconda gli slot 4-5, a ogni ora; solo nelle mappe con l'erba."""
    rows = []
    if not e['land'].get('rate'):
        return rows
    for key, name in RADIO:
        lv, p = [], 0
        for k, slots in enumerate(((2, 3), (4, 5))):
            if k < len(e.get(key, [])) and e[key][k] == sp:
                for i in slots:
                    p += PROB['erba'][i]
                    lv.append(e['land']['mons'][i]['level'])
        if p:
            rows.append(dist_row(maps, mp, name, lv, p, 'sempre', RADIO_NOTE))
    return rows


def plan_distribution(plan, maps, sp):
    """Righe della «distribuzione» di una specie: per mappa (ordine dei banchi, metodi in ordine alfabetico),
    poi Safari, poi regali, statici e leggendari."""
    out = []
    trees = collections.defaultdict(list)
    for h in plan.get('bottintesta', []):
        trees['MAP_' + h['map']].append(h)
    swarms = collections.defaultdict(list)
    for r in (plan.get('sciami') or {}).get('righe', []):
        swarms[r['mappa']].append(r)
    for e in plan['gs_enc_data']['encounters']:
        if e['map'] == SAFARI_ENTRANCE:
            continue
        mp = 'MAP_' + e['map']
        rows = []
        for h in trees.get(mp, []):
            for key, name in (('CommonMons', 'Bottintesta (alberi comuni)'), ('RareMons', 'Bottintesta (alberi rari)')):
                lv, p = [], 0
                for i, m in enumerate(h.get(key, [])):
                    if m['species'] == sp:
                        p += PROB['bottintesta'][i]
                        lv += [m['minLevel'], m['maxLevel']]
                if p:
                    rows.append(dist_row(maps, mp, name, lv, p, 'sempre'))
        lv, perc = [], {}
        for i, m in enumerate(e['land']['mons']):
            for t in TIMES:
                if m['species'].get(t) == sp:
                    perc[t] = perc.get(t, 0) + PROB['erba'][i]
                    lv.append(m['level'])
        if perc:
            perc = {t: perc[t] for t in TIMES if t in perc}
            rows.append(dist_row(maps, mp, 'erba', lv, perc, '/'.join(perc)))
        for key, name, probs in (('surf', 'surf', PROB['surf']), ('rock_smash', 'Martiddata (Spaccaroccia)', PROB['spaccaroccia'])):
            lv, p = [], 0
            for i, m in enumerate(e[key]['mons']):
                if m['species'] == sp:
                    p += probs[i]
                    lv += [m['level']['min'], m['level']['max']]
            if p:
                rows.append(dist_row(maps, mp, name, lv, p, 'sempre'))
        for key, name in FISH_RODS:
            mons = e['fishing'][key]['mons']
            lv, p = [], 0
            for i, m in enumerate(mons):
                if m['species'] == sp:
                    p += PROB['canne'][i]
                    lv += [m['level']['min'], m['level']['max']]
            if p:
                rows.append(dist_row(maps, mp, name, lv, p, 'sempre'))
            slot = NIGHT_FISH_SLOT.get(key)
            if slot is not None and len(mons) > slot and e.get('nightFish') == sp:
                m = mons[slot]
                rows.append(dist_row(maps, mp, name, [m['level']['min'], m['level']['max']],
                                     {'nite': PROB['canne'][slot]}, 'nite', 'slot notturno (nightFish)'))
        rows += swarm_rows(maps, mp, e, swarms.get(mp, []), sp) + radio_rows(maps, mp, e, sp)
        rows.sort(key=lambda r: r['metodo'])
        out += rows
    out += plan_safari(plan, sp)
    for x in plan.get('speciali', []) + plan.get('leggendari', []):
        if x.get('specie') == sp:
            nota = x.get('quando', '') + (' — ' + x['chi'] if x.get('chi') else '')
            out.append(dist_row(maps, x.get('mappa'), x.get('metodo'), [x.get('livello', 0)], None, 'sempre', nota))
    return out


def plan_safari(plan, sp):
    rows = []
    areas = plan.get('safari', [])
    for a in areas:
        lv, perc = [], {}
        for t in TIMES:
            for m in a['dati']['land']['mons'][t]:
                if m['species'] == sp:
                    perc[t] = perc.get(t, 0) + 10
                    lv.append(m['level'])
        if perc:
            rows.append(safari_row('Zona Safari, erba (%s)' % a.get('habitat_vendicari'), lv, perc, '/'.join(perc), a['area']))

    def water_row(metodo, lv, perc, nota):
        if len(perc) == 3 and len(set(perc.values())) == 1:
            return safari_row(metodo, lv, perc['morn'], 'sempre', nota)
        return safari_row(metodo, lv, perc, '/'.join(perc), nota)
    for key, name in SAFARI_WATER:
        found = []
        for a in areas:
            lv, perc = [], {}
            for t in TIMES:
                for m in a['dati'][key]['mons'][t]:
                    if m['species'] == sp:
                        perc[t] = perc.get(t, 0) + 10
                        lv.append(m['level'])
            if perc:
                found.append((a, lv, perc))
        if not found:
            continue
        if len(found) == len(areas) and all((x[1], x[2]) == (found[0][1], found[0][2]) for x in found):
            rows.append(water_row('Zona Safari, ' + name, found[0][1], found[0][2], 'tutte le aree'))
        else:
            for a, lv, perc in found:
                rows.append(water_row('Zona Safari, %s (%s)' % (name, a.get('habitat_vendicari')), lv, perc, a['area']))
    for a in areas:
        for key, name in (('land', None),) + SAFARI_WATER:
            lv, times = [], set()
            for b in a['dati'][key].get('bonus_mons', []):
                for t in TIMES:
                    if b[t]['species'] == sp:
                        lv.append(b[t]['level'])
                        times.add(t)
            if lv:
                ts = [t for t in TIMES if t in times]
                metodo = 'Zona Safari, bonus degli oggetti' + ('' if name is None else ', ' + name) + \
                    ' (%s)' % a.get('habitat_vendicari')
                rows.append(safari_row(metodo, lv, None, 'sempre' if len(ts) == 3 else '/'.join(ts), a['area']))
    rows.sort(key=lambda r: r['metodo'])
    return rows


def check_distribution(entries, plan, maps, rep):
    """D08: la «distribuzione» di ogni specie e' quella che il piano da' (R-INC-07)."""
    for p, s in entries:
        try:
            want = plan_distribution(plan, maps, s.get('simbolo'))
        except (KeyError, TypeError, IndexError, ValueError) as ex:
            rep.err('D08', '%s n.%s' % (os.path.basename(p), s.get('n')), 'piano non leggibile per la distribuzione (%s)' % ex)
            return
        got = s.get('distribuzione')
        if got != want:
            diff = next((i for i, (a, b) in enumerate(zip(got or [], want)) if a != b), min(len(got or []), len(want)))
            rep.err('D08', '%s n.%s %s' % (os.path.basename(p), s.get('n'), s.get('nome')),
                    'distribuzione diversa dal piano: %d righe invece di %d, prima differenza alla riga %d'
                    % (len(got or []), len(want), diff))


# ----------------------------------------------------------------------------------------------
# Pokémon vaganti (R-INC-09, blocco 3.3 R-SPE-18): src/field_roamer.c e include/constants/roamer.h

ROAMER_NEIGHBORS = 6  # MAX_ROAM_NEIGHBOR di src/field_roamer.c
ROAMER_SLOTS = 4      # ROAMER_MAX: dimensione dei dati di salvataggio, non cambia


def roamer_loc_const(mp):
    return 'ROAMER_LOC_' + mp[len('MAP_'):]


def render_roamer_h(v):
    out = ['#ifndef POKEHEARTGOLD_CONSTANTS_ROAMER_H', '#define POKEHEARTGOLD_CONSTANTS_ROAMER_H', '']
    w = max(len(s['costante']) for s in v['slot'])
    for s in v['slot']:
        out.append('#define %-*s %d' % (w, s['costante'], s['indice']))
    out.append('#define %-*s %d' % (w, 'ROAMER_MAX', len(v['slot'])))
    out.append('')
    w = max(len(roamer_loc_const(x['mappa'])) for x in v['luoghi'])
    for x in v['luoghi']:
        out.append('#define %-*s %d' % (w, roamer_loc_const(x['mappa']), x['indice']))
    out.append('#define %-*s %d' % (w, 'ROAMER_LOC_COUNT', len(v['luoghi'])))
    out += ['', '#endif // POKEHEARTGOLD_CONSTANTS_ROAMER_H', '']
    return '\n'.join(out)


def render_roamer_blocks(v):
    """I quattro pezzi di src/field_roamer.c che il blocco 3.3 riscrive (export --vaganti)."""
    luoghi = v['luoghi']
    a = ['static const u32 sRoamerLocations[ROAMER_LOC_COUNT] = {']
    a += ['    %s, // %d' % (x['mappa'], x['indice']) for x in luoghi]
    a += ['};', '', '// vicini: strade raggiungibili passando al massimo per una mappa che non e\' una strada (blocco 3.3, R-SPE-18)',
          'static const struct RoamerAdjacency sRoamerAdjacencyTable[ROAMER_LOC_COUNT] = {']
    for x in luoghi:
        nb = [roamer_loc_const(luoghi[i]['mappa']) for i in x['vicini']] + ['-1'] * (ROAMER_NEIGHBORS - len(x['vicini']))
        a.append('    { %d, { %s } }, // %s' % (len(x['vicini']), ', '.join(nb), roamer_loc_const(x['mappa'])))
    a.append('};')
    attivi = [s for s in v['slot'] if s.get('specie')]
    b = ['    switch (idx) {']
    for s in attivi:
        b += ['    case %s:' % s['costante'], '        species = %s;' % s['specie'], '        level = %d;' % s['livello'], '        break;']
    b += ['    default:', '        GF_ASSERT(FALSE);', '        return;', '    }']
    c = ['u8 SpeciesToRoamerIdx(u16 species) {', '    switch (species) {']
    for s in attivi:
        c += ['    case %s:' % s['specie'], '        return %s;' % s['costante']]
    c += ['    default:', '        GF_ASSERT(FALSE);', '        return ROAMER_MAX;', '    }', '}']
    d = ['    loc_num = ROAMER_LOC_COUNT; // tutti i vaganti girano su tutte le strade dell\'isola (blocco 3.3)', '    loc_min = 0;']
    return {'luoghi_e_vicini': '\n'.join(a), 'creazione': '\n'.join(b), 'specie_a_slot': '\n'.join(c),
            'luogo_casuale': '\n'.join(d)}


def roamer_spans(txt):
    """Posizioni (inizio, fine) dei quattro pezzi in src/field_roamer.c, prima o dopo la modifica."""
    spans = {}
    a = txt.find('static const u32 sRoamerLocations[ROAMER_LOC_COUNT] = {')
    t = txt.find('sRoamerAdjacencyTable[ROAMER_LOC_COUNT] = {', a)
    e = txt.find('\n};', t)
    if a >= 0 and t >= 0 and e >= 0:
        spans['luoghi_e_vicini'] = (a, e + 3)
    f = txt.find('void Save_CreateRoamerByID(')
    s = txt.find('    switch (idx) {', f)
    e = txt.find('\n    }\n', s)
    if f >= 0 and s >= 0 and e >= 0:
        spans['creazione'] = (s, e + 6)
    s = txt.find('u8 SpeciesToRoamerIdx(u16 species) {')
    e = txt.find('\n}\n', s)
    if s >= 0 and e >= 0:
        spans['specie_a_slot'] = (s, e + 2)
    k = 'roamer_cur_loc = sRoamerLocations[Roamer_GetLocation(roamer, roamer_idx)];\n'
    s = txt.find(k)
    e = txt.find('\n    do {', s)
    if s >= 0 and e >= 0:
        spans['luogo_casuale'] = (s + len(k), e)
    return spans


def check_roamers(path, v, plan, maps, rep):
    where = os.path.basename(path) + ' vaganti'
    luoghi, slot = v.get('luoghi') or [], v.get('slot') or []
    roads = [x.get('mappa') for x in luoghi]
    if len(slot) != ROAMER_SLOTS or [s.get('indice') for s in slot] != list(range(ROAMER_SLOTS)):
        rep.err('V01', where, '%d slot invece di %d (ROAMER_MAX non cambia)' % (len(slot), ROAMER_SLOTS))
    if not luoghi or [x.get('indice') for x in luoghi] != list(range(len(luoghi))) or len(set(roads)) != len(roads):
        rep.err('V01', where, 'luoghi non numerati da 0 o ripetuti')
    for mp in roads:
        m = maps.get(mp)
        if not m or not (mp.startswith('MAP_STRADA_') or m.get('profilo') == 'STRADA'):
            rep.err('V01', '%s %s' % (where, mp), 'non è una strada dei registri 2.1–2.3')
    banks = {'MAP_' + e['map'] for e in plan['gs_enc_data']['encounters']} if plan else None
    for x in luoghi:
        w = '%s %s' % (where, x.get('mappa'))
        nb = x.get('vicini') or []
        if banks is not None and x.get('mappa') not in banks:
            rep.err('V02', w, 'strada senza banco di incontri: il vagante non si incontra mai')
        if not 1 <= len(nb) <= ROAMER_NEIGHBORS or len(set(nb)) != len(nb) or \
                any(not isinstance(i, int) or not 0 <= i < len(luoghi) or i == x.get('indice') for i in nb):
            rep.err('V02', w, 'vicini non validi (da 1 a %d indici diversi, mai sé stessa): %s' % (ROAMER_NEIGHBORS, nb))
            continue
        for i in nb:
            if x.get('indice') not in (luoghi[i].get('vicini') or []):
                rep.err('V03', w, 'vicino %d senza il ritorno' % i)
    legg = {x['specie']: x for x in (plan or {}).get('leggendari', []) if x.get('metodo') == 'vagante'}
    attivi = [s.get('specie') for s in slot if s.get('specie')]
    if plan is not None and sorted(attivi) != sorted(legg):
        rep.err('V04', where, 'specie degli slot %s diverse dai vaganti del piano %s' % (attivi, sorted(legg)))
    for s in slot:
        if s.get('specie') in legg and s.get('livello') != legg[s['specie']].get('livello'):
            rep.err('V04', '%s %s' % (where, s.get('specie')), 'livello %s invece di %s (piano)' % (s.get('livello'), legg[s['specie']].get('livello')))
    try:
        want = {'include/constants/roamer.h': render_roamer_h(v), 'src/field_roamer.c': render_roamer_blocks(v)}
    except (KeyError, TypeError, ValueError, IndexError) as ex:
        rep.err('V05', where, 'dati dei vaganti non leggibili (%s)' % ex)
        return
    if v.get('codice') != want:
        rep.err('V05', where, 'il codice della sezione «codice» non corrisponde ai dati (rigenerarlo)')


def export_roamers(path, repo, write, rep):
    v = load_json(path)['vaganti']
    changes = []
    p = os.path.join(repo, 'include', 'constants', 'roamer.h')
    new = v['codice']['include/constants/roamer.h']
    if open(p, encoding='utf-8', newline='').read() != new:
        changes.append('include/constants/roamer.h')
        if write:
            open(p, 'w', encoding='utf-8', newline='\n').write(new)
    p = os.path.join(repo, 'src', 'field_roamer.c')
    txt = open(p, encoding='utf-8', newline='').read()
    spans = roamer_spans(txt)
    blocks = v['codice']['src/field_roamer.c']
    for k in blocks:
        if k not in spans:
            rep.err('E00', 'src/field_roamer.c', 'pezzo «%s» non trovato' % k)
            return changes
    for k in sorted(blocks, key=lambda k: -spans[k][0]):
        a, b = spans[k]
        txt = txt[:a] + blocks[k] + txt[b:]
    if open(p, encoding='utf-8', newline='').read() != txt:
        changes.append('src/field_roamer.c')
        if write:
            open(p, 'w', encoding='utf-8', newline='\n').write(txt)
    return changes


def check_plan(path, rep, species_ids=None, items=None, maps=None):
    try:
        plan = load_json(path)
        encs = plan['gs_enc_data']['encounters']
    except Exception as ex:  # noqa: BLE001
        rep.err('P00', os.path.basename(path), 'piano illeggibile (%s)' % ex)
        return None
    known_sp = set(species_ids) if species_ids else None

    def species_ok(s, where):
        if not isinstance(s, str) or not s.startswith('SPECIES_') or (known_sp is not None and s not in known_sp):
            rep.err('P03', where, 'specie inesistente %r' % s)

    banks = plan.get('banchi', {})
    syms = [h['wildEncounterBank'] for h in plan.get('intestazioni', [])]
    if len(encs) > MAX_BANKS or len(syms) != len(set(syms)) or len(syms) != len(encs):
        rep.err('P01', 'banchi', '%d banchi, %d simboli (%d distinti)' % (len(encs), len(syms), len(set(syms))))
    no_wild = {x['mappa'] for x in plan.get('mappe_senza_selvatici', [])}
    for i, e in enumerate(encs):
        where = 'banco %d %s' % (i, e.get('map'))
        if maps is not None and 'MAP_' + e.get('map', '') not in maps:
            rep.err('P04', where, 'mappa assente dai registri 2.1–2.3')
        if 'MAP_' + e.get('map', '') in no_wild:
            rep.err('P04', where, 'mappa senza selvatici (R-INC-03) con un banco')
        land = e['land']['mons']
        if land and (len(land) != LAND or any(not 1 <= m['level'] <= 100 for m in land)):
            rep.err('P02', where, 'erba: %d slot o livelli fuori da 1–100' % len(land))
        for m in land:
            for t in ('morn', 'day', 'nite'):
                species_ok(m['species'].get(t), where)
        for key, n in (('surf', SURF), ('rock_smash', ROCK)):
            mons = e[key]['mons']
            if mons and (len(mons) != n or any(not 1 <= m['level']['min'] <= m['level']['max'] <= 100 for m in mons)):
                rep.err('P02', where, '%s: %d slot o livelli non validi' % (key, len(mons)))
            for m in mons:
                species_ok(m['species'], where)
        for key in ('old_rod', 'good_rod', 'super_rod'):
            mons = e['fishing'][key]['mons']
            if mons and (len(mons) != FISH or any(not 1 <= m['level']['min'] <= m['level']['max'] <= 100 for m in mons)):
                rep.err('P02', where, '%s: %d slot o livelli non validi' % (key, len(mons)))
            for m in mons:
                species_ok(m['species'], where)
        for key in ('hoenn', 'sinnoh'):
            if e[key] and len(e[key]) != 2:
                rep.err('P02', where, '%s: %d specie invece di 2' % (key, len(e[key])))
            for s in e[key]:
                species_ok(s, where)
    sw = plan.get('sciami', {}).get('righe', [])
    by_map = {'MAP_' + e['map']: e for e in encs}
    if len(sw) != 20:
        rep.err('P05', 'sciami', '%d righe invece di 20' % len(sw))
    for r in sw:
        e = by_map.get(r['mappa'])
        need = {'erba': lambda x: x['land']['mons'], 'surf': lambda x: x['surf']['mons'],
                'canne': lambda x: x['fishing']['good_rod']['mons']}.get(r['tipo'])
        if not e or not need or not need(e):
            rep.err('P05', r['mappa'], 'sciame «%s» su una mappa senza quel metodo' % r['tipo'])
        species_ok(r['specie'], r['mappa'])
        key = {'erba': 'landSwarm', 'surf': 'surfSwarm', 'canne': 'fishSwarm'}.get(r['tipo'])
        if e and e.get(key) != r['specie']:
            rep.err('P05', r['mappa'], '%s del banco diverso dalla specie dello sciame' % key)
    for ev in plan.get('evoluzioni', []):
        t = ev.get('trinacria', {})
        where = '%s → %s' % (ev.get('specie'), ev.get('bersaglio'))
        if t.get('method') not in EVO_METHODS:
            rep.err('P06', where, 'metodo %s non ammesso' % t.get('method'))
        p = t.get('param')
        if t.get('method') == 'EVO_LEVEL' and not (isinstance(p, int) and 1 <= p <= 100):
            rep.err('P06', where, 'livello %r non valido' % p)
        if t.get('method') != 'EVO_LEVEL' and (not isinstance(p, str) or (items is not None and p not in items)):
            rep.err('P06', where, 'strumento %r inesistente' % p)
        species_ok(ev.get('specie'), where)
        species_ok(ev.get('bersaglio'), where)
    saf = plan.get('safari', [])
    if len(saf) != SAFARI_AREAS:
        rep.err('P08', 'safari', '%d aree invece di %d' % (len(saf), SAFARI_AREAS))
    for a in saf:
        d = a.get('dati', {})
        for key in ('land', 'surf', 'oldrod', 'goodrod', 'superrod'):
            for t in ('morn', 'day', 'nite'):
                mons = d.get(key, {}).get('mons', {}).get(t, [])
                if len(mons) != SAFARI_SLOTS:
                    rep.err('P08', a.get('area'), '%s %s: %d slot' % (key, t, len(mons)))
                for m in mons:
                    species_ok(m['species'], a.get('area'))
    for h in plan.get('bottintesta', []):
        for key in ('CommonMons', 'RareMons'):
            if len(h.get(key, [])) != 6:
                rep.err('P02', h.get('map'), '%s: %d slot invece di 6' % (key, len(h.get(key, []))))
            for m in h.get(key, []):
                species_ok(m['species'], h.get('map'))
    for x in plan.get('speciali', []) + plan.get('leggendari', []):
        species_ok(x.get('specie'), x.get('mappa'))
        mp = x.get('mappa', '')
        if maps is not None and mp.startswith('MAP_') and mp not in maps:
            rep.err('P04', mp, 'mappa assente dai registri 2.1–2.3')
    return plan


def coverage(plan, evo_json, rep):
    """R-INC-06: ogni specie non mitica e' ottenibile (tabelle, Safari, alberi, speciali, evoluzione o uovo)."""
    direct = set()
    for e in plan['gs_enc_data']['encounters']:
        for m in e['land']['mons']:
            direct.update(m['species'].values())
        for k in ('surf', 'rock_smash'):
            direct.update(m['species'] for m in e[k]['mons'])
        for k in ('old_rod', 'good_rod', 'super_rod'):
            direct.update(m['species'] for m in e['fishing'][k]['mons'])
        direct.update(e['hoenn'] + e['sinnoh'])
        direct.update(x for x in (e.get('landSwarm'), e.get('surfSwarm'), e.get('fishSwarm'), e.get('nightFish')) if x)
    for a in plan.get('safari', []):
        for key, v in a['dati'].items():
            if isinstance(v, dict):
                for t, mons in v.get('mons', {}).items():
                    direct.update(m['species'] for m in mons)
                for b in v.get('bonus_mons', []):
                    direct.update(b[t]['species'] for t in ('morn', 'day', 'nite'))
    for h in plan.get('bottintesta', []):
        direct.update(m['species'] for k in ('CommonMons', 'RareMons') for m in h[k])
    direct.update(x['specie'] for x in plan.get('speciali', []) + plan.get('leggendari', []))
    direct.discard('SPECIES_NONE')
    nxt = collections.defaultdict(set)
    prv = collections.defaultdict(set)
    for ent in evo_json:
        for ev in ent['evos']:
            if ev['method'] != 'EVO_NONE':
                nxt[ent['baseSpecies']].add(ev['target'])
                prv[ev['target']].add(ent['baseSpecies'])
    ok = set(direct)
    changed = True
    while changed:
        changed = False
        for s in list(nxt) + list(prv):
            if s in ok:
                continue
            if prv[s] & ok or nxt[s] & ok:
                ok.add(s)
                changed = True
    return ok


def check_coverage(plan, repo, species_ids, rep):
    if not repo or not species_ids:
        return
    evo = load_json(os.path.join(repo, 'files', 'poketool', 'personal', 'evo.json'))['evoTable']
    ok = coverage(plan, evo, rep)
    for s, n in sorted(species_ids.items(), key=lambda x: x[1]):
        if 1 <= n <= 493 and s not in MITICI and s not in ok and not s.endswith(('_EGG', '_BAD_EGG')):
            rep.err('P07', s, 'specie non mitica non ottenibile')

# ----------------------------------------------------------------------------------------------
# Esportazione nel repository


def export(plan_path, repo, write, rep, docs):
    plan = load_json(plan_path)
    maps = load_maps(docs)
    changes = []

    def put(rel, text):
        p = os.path.join(repo, rel)
        if not os.path.isfile(p):
            rep.err('E00', rel, 'file del repository non trovato')
            return
        old = open(p, encoding='utf-8', newline='').read()
        if old != text:
            changes.append(rel)
            if write:
                open(p, 'w', encoding='utf-8', newline='\n').write(text)

    def jtext(obj):
        return json.dumps(obj, ensure_ascii=False, indent=4) + '\n'

    put('files/fielddata/encountdata/gs_enc_data.json', jtext(plan['gs_enc_data']))
    put('include/encounter_tables_narc.h', plan['encounter_tables_narc_h'])
    p = os.path.join(repo, 'files', 'arc', 'safari_enc.json')
    if os.path.isfile(p):
        put('files/arc/safari_enc.json', jtext({'encounters': [a['dati'] for a in plan['safari']]}))
    p = os.path.join(repo, 'files', 'arc', 'headbutt.json')
    if os.path.isfile(p):
        hb = load_json(p)
        by_code = {t['Map']: t for t in hb['tables']}
        for h in plan['bottintesta']:
            m = maps.get('MAP_' + h['map'])
            code = m.get('codice_file_hg') if m else None
            if code not in by_code:
                rep.err('E00', h['map'], 'voce di headbutt.json non trovata (%s)' % code)
                continue
            by_code[code]['CommonMons'] = h['CommonMons']
            by_code[code]['RareMons'] = h['RareMons']
        put('files/arc/headbutt.json', jtext(hb))
    p = os.path.join(repo, 'files', 'poketool', 'personal', 'evo.json')
    if os.path.isfile(p):
        txt = open(p, encoding='utf-8', newline='').read()
        for ev in plan['evoluzioni']:
            hg, tr = ev['heartgold'], ev['trinacria']
            fmt = lambda v: json.dumps(v)  # noqa: E731
            old = '{ "method": "%s", "param": %s, "target": "%s" }' % (hg['method'], fmt(hg['param']), ev['bersaglio'])
            new = '{ "method": "%s", "param": %s, "target": "%s" }' % (tr['method'], fmt(tr['param']), ev['bersaglio'])
            # la voce di una specie va da "baseSpecies": "<specie>" al "baseSpecies" successivo (una o piu' righe)
            key = '"baseSpecies": "%s"' % ev['specie']
            done = False
            pos = txt.find(key)
            while pos >= 0:
                end = txt.find('"baseSpecies"', pos + len(key))
                end = len(txt) if end < 0 else end
                part = txt[pos:end]
                if old in part or new in part:
                    txt = txt[:pos] + part.replace(old, new) + txt[end:]
                    done = True
                pos = txt.find(key, pos + len(key))
            if not done:
                rep.err('E00', ev['specie'], 'evoluzione %s non trovata in evo.json' % old)
        put('files/poketool/personal/evo.json', txt)
    p = os.path.join(repo, 'src', 'unk_02097F6C.c')
    if os.path.isfile(p):
        txt = open(p, encoding='utf-8', newline='').read()
        a = txt.find('#define SWARM_MAP_COUNT')
        b = txt.find('};', a)
        if a < 0 or b < 0:
            rep.err('E00', 'src/unk_02097F6C.c', 'sSwarmMapLUT non trovata')
        else:
            put('src/unk_02097F6C.c', txt[:a] + plan['sciami']['codice'] + txt[b + 2:])
    p = os.path.join(repo, 'src', 'data', 'map_headers.h')
    if os.path.isfile(p):
        txt = open(p, encoding='utf-8', newline='').read()
        for h in plan['intestazioni']:
            m = maps.get(h['mappa'])
            keys = [h['mappa']] + ([m['simbolo_hg_sostituito']] if m else [])
            done = False
            for k in keys:
                rx = re.compile(r'(\[%s\] = \{\s*\.wildEncounterBank = )(\w+)(,)' % re.escape(k))
                if rx.search(txt):
                    txt = rx.sub(lambda mm: mm.group(1) + h['wildEncounterBank'] + mm.group(3), txt, count=1)
                    done = True
                    break
            if not done:
                rep.err('E00', h['mappa'], 'intestazione non trovata in map_headers.h')
        put('src/data/map_headers.h', txt)
    for c in changes:
        print(('scritto ' if write else 'da scrivere ') + c)
    return changes

# ----------------------------------------------------------------------------------------------


def run_check(args, rep):
    font = Font(args.repo)
    docs = find_docs(args.docs)
    glossary = []
    if docs:
        glossary = load_json(os.path.join(docs, 'MODULO_3', '3.0_REGOLE_E_GLOSSARIO.json'))['glossario']
    sids = repo_species(args.repo)
    entries = []
    n = check_species(args.files, glossary, rep, font, sids, entries)
    print('specie controllate: %d' % n)
    if args.plan:
        maps = load_maps(docs) if docs else None
        plan = check_plan(args.plan, rep, sids, repo_items(args.repo), maps)
        if plan is not None:
            check_coverage(plan, args.repo, sids, rep)
            check_distribution(entries, plan, maps or {}, rep)
            print('banchi del piano: %d' % len(plan['gs_enc_data']['encounters']))
    for p in args.files:
        try:
            v = load_json(p).get('vaganti')
        except Exception:  # noqa: BLE001 - D00 l'ha gia' segnalato
            continue
        if v is not None:
            check_roamers(p, v, plan if args.plan else None, load_maps(docs) if docs else {}, rep)
            print('vaganti controllati: %d slot, %d luoghi' % (len(v.get('slot') or []), len(v.get('luoghi') or [])))


def selftest():
    docs = find_docs(None)
    root = os.path.join(HERE, '..')
    ok_files = [os.path.join(root, 'docs', 'MODULO_3', '3.1_POKEMON_1-100.json')]
    plan = os.path.join(root, 'docs', 'MODULO_3', '3.1_PIANO_INCONTRI.json')
    ko = os.path.join(HERE, 'testdata', 'dex_prova_ko.json')
    repo = next((r for r in DEFAULT_REPOS if os.path.isfile(os.path.join(r, 'include', 'constants', 'species.h'))), None)
    print('repository per il collaudo: %s' % (repo or 'nessuno (P07 non si controlla)'))
    good = True
    rep = Report(quiet=True)
    ok_files += sorted(glob.glob(os.path.join(root, 'docs', 'MODULO_3', '3.[2-5]_POKEMON_*.json')))

    class A:
        pass
    a = A()
    a.files, a.plan, a.repo, a.docs = ok_files, plan, repo, docs
    run_check(a, rep)
    if rep.errors:
        good = False
        print('collaudo: i blocchi %s danno errori: %s' % (', '.join(os.path.basename(f)[:3] for f in ok_files), rep.codes()))
        for e in rep.errors[:10]:
            print('   ', *e)
    rep2 = Report(quiet=True)
    a.files, a.plan = [ko], ko
    run_check(a, rep2)
    expected = [c for c in load_json(ko)['errori_attesi'] if repo or c != 'P07']
    if rep2.codes() != sorted(expected):
        good = False
        print('collaudo: dex_prova_ko.json dà %s invece di %s' % (rep2.codes(), sorted(expected)))
    print('SELFTEST_OK' if good else 'SELFTEST_FAILED')
    return 0 if good else 1


def main():
    # la console di Windows (cp1252) non ha U+2009 e simili: senza questo un messaggio d'errore fa crashare lo strumento
    sys.stdout.reconfigure(errors='backslashreplace')
    if '--selftest' in sys.argv:
        return selftest()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)
    c = sub.add_parser('check')
    c.add_argument('files', nargs='+')
    c.add_argument('--plan')
    c.add_argument('--repo')
    c.add_argument('--docs')
    x = sub.add_parser('export')
    x.add_argument('--plan', required=True)
    x.add_argument('--repo', required=True)
    x.add_argument('--docs')
    x.add_argument('--vaganti', help='blocco 3.3: scrive anche include/constants/roamer.h e src/field_roamer.c')
    x.add_argument('--write', action='store_true')
    args = ap.parse_args()
    rep = Report()
    if args.cmd == 'check':
        run_check(args, rep)
        print('DEX_OK' if not rep.errors else 'DEX_FAILED')
    else:
        export(args.plan, args.repo, args.write, rep, find_docs(args.docs))
        if args.vaganti:
            for c in export_roamers(args.vaganti, args.repo, args.write, rep):
                print(('scritto ' if args.write else 'da scrivere ') + c)
        print('EXPORT_OK' if not rep.errors else 'EXPORT_FAILED')
    return 1 if rep.errors else 0


if __name__ == '__main__':
    sys.exit(main())
