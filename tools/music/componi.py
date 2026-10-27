#!/usr/bin/env python3
"""Compone le musiche di Pokémon Trinacria (Modulo 5, blocchi 5.2-5.4).

Uso:
    python -I tools/music/componi.py [--partiture DIR ...] [--out DIR (default build/musica)]
           [--registro docs/MODULO_2/2.5_TRAINERS_SPRITES_FLY_SEQ.json | --seq-h include/trinacria/trinacria_seq.h]

Ogni partitura è un file <blocco>/<SIMBOLO>.py dentro tools/music/ (per esempio
tools/music/5.2/SEQ_CT_VERMUT.py) con:
    SIMBOLO = 'SEQ_CT_VERMUT'      # alias del registro 2.5 (sezione «musiche»)
    BANCO = 'BANK_BGM_FIELD2'      # facoltativo: senza, il banco dello slot HeartGold
    VOLUME = 78                    # facoltativo: senza, il volume dello slot HeartGold
    def partitura(A):              # A = il modulo tools/trinacria_audio.py
        mw = A.MidiWriter(48)
        ...
        return mw
Scrive <out>/<SIMBOLO>.mid e <out>/manifesto.json (build/ non va nel repository:
si rigenera), che si passa a
    python -I tools/trinacria_audio.py applica --manifesto <out>/manifesto.json
Ultima riga: COMPONI_OK oppure COMPONI_FAILED (ogni problema è «ERRORE Cnn ...»).
"""
import argparse
import glob
import json
import os
import re
import runpy
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.dirname(HERE)
PROJ = os.path.dirname(TOOLS)
sys.path.insert(0, TOOLS)
import trinacria_audio as A  # noqa: E402

BLOCCHI = ('5.2', '5.3', '5.4')


def alias_from_registry(path):
    with open(path, encoding='utf-8') as f:
        mus = json.load(f)['musiche']
    out = {r['simbolo']: r['slot_hg_sostituito'] for r in mus['campo']}
    out.update({r['simbolo']: r['slot_hg'] for r in mus['lotta']})
    return out


def alias_from_header(path):
    out = {}
    with open(path, encoding='utf-8') as f:
        for line in f:
            m = re.match(r'#define (SEQ_\w+)\s+(SEQ_GS_\w+)\s*$', line)
            if m:
                out[m.group(1)] = m.group(2)
    return out


def componi(partiture, out_dir, alias):
    errs, brani, seen = [], [], {}
    for path in partiture:
        nome = os.path.splitext(os.path.basename(path))[0]
        try:
            mod = runpy.run_path(path)
        except Exception as e:                      # la partitura è codice: qualsiasi errore
            errs.append(('C01', '%s: la partitura non si esegue: %s' % (path, e)))
            continue
        sim = mod.get('SIMBOLO')
        if sim != nome:
            errs.append(('C02', '%s: SIMBOLO %r diverso dal nome del file' % (path, sim)))
            continue
        if sim not in alias:
            errs.append(('C03', '%s: %s non è una musica del registro 2.5' % (path, sim)))
            continue
        if sim in seen:
            errs.append(('C04', '%s: %s già scritto da %s' % (path, sim, seen[sim])))
            continue
        seen[sim] = path
        try:
            mw = mod['partitura'](A)
            data = mw.data()
        except Exception as e:
            errs.append(('C01', '%s: partitura() non restituisce un MidiWriter valido: %s' % (path, e)))
            continue
        A.write(os.path.join(out_dir, sim + '.mid'), data)
        b = {'simbolo': sim, 'slot': alias[sim], 'file': sim + '.mid'}
        if mod.get('BANCO'):
            b['banco'] = mod['BANCO']
        if mod.get('VOLUME') is not None:
            b['volume'] = mod['VOLUME']
        brani.append(b)
    order = list(alias)
    brani.sort(key=lambda b: order.index(b['simbolo']))
    return {'manifesto': 'musiche di Pokémon Trinacria', 'brani': brani}, errs


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--partiture', nargs='*', help='cartelle con le partiture (default: tools/music/5.2-5.4)')
    ap.add_argument('--out', default=os.path.join(PROJ, 'build', 'musica'))
    ap.add_argument('--registro')
    ap.add_argument('--seq-h')
    a = ap.parse_args(argv)
    if a.seq_h:
        alias = alias_from_header(a.seq_h)
    else:
        reg = a.registro or os.path.join(PROJ, 'docs', 'MODULO_2', '2.5_TRAINERS_SPRITES_FLY_SEQ.json')
        alias = alias_from_registry(reg)
    dirs = a.partiture if a.partiture is not None else [os.path.join(HERE, b) for b in BLOCCHI]
    files = sorted(p for d in dirs for p in glob.glob(os.path.join(d, 'SEQ_*.py')))
    man, errs = componi(files, a.out, alias)
    for code, msg in errs:
        print('ERRORE %s %s' % (code, msg))
    if errs:
        print('COMPONI_FAILED')
        return 1
    A.write(os.path.join(a.out, 'manifesto.json'),
            (json.dumps(man, ensure_ascii=False, indent=1) + '\n').encode('utf-8'))
    print('%d partiture, manifesto in %s' % (len(man['brani']), os.path.join(a.out, 'manifesto.json')))
    print('COMPONI_OK')
    return 0


if __name__ == '__main__':
    sys.exit(main())
