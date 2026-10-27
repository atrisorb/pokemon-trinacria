#!/usr/bin/env python3
"""Collaudo delle partiture di un blocco del Modulo 5 (5.2-5.4), senza toccare il repository.

Uso:
    python -I tools/music/collauda.py --blocchi 5.2 [--repo F:/Progetti/pokeheartgold]
           [--out DIR (default build/collaudo)] [--json F] [--sdat]

Compone le partiture dei blocchi (come componi.py), le mette in una copia dell'archivio
originale di HeartGold (applica), confronta il risultato con l'originale (controlla) e
stampa per ogni brano: slot, banco, byte, tracce, note insieme (PCM/PSG/rumore),
ritornello e carico. Con --json scrive gli stessi dati (li legge il generatore del
documento del blocco); con --sdat salva anche DIR/gs_sound_data.sdat da provare
nell'emulatore. Ultima riga: AUDIO_OK oppure AUDIO_FAILED.
"""
import argparse
import glob
import json
import os
import runpy
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.dirname(HERE)
PROJ = os.path.dirname(TOOLS)
sys.path.insert(0, TOOLS)
sys.path.insert(0, HERE)
import trinacria_audio as A  # noqa: E402
import componi as C  # noqa: E402


def partiture(blocchi):
    return sorted(p for b in blocchi for p in glob.glob(os.path.join(HERE, b, 'SEQ_*.py')))


def scheda(path):
    """SCHEDA, BANCO, VOLUME e i dati della notazione (mw.trinacria) di una partitura."""
    mod = runpy.run_path(path)
    mw = mod['partitura'](A)
    return {'scheda': mod.get('SCHEDA', {}), 'banco': mod.get('BANCO'), 'volume': mod.get('VOLUME'),
            'notazione': getattr(mw, 'trinacria', None), 'doc': (mod.get('__doc__') or '').strip()}


def collauda(blocchi, out, repo):
    reg = os.path.join(PROJ, 'docs', 'MODULO_2', '2.5_TRAINERS_SPRITES_FLY_SEQ.json')
    alias = C.alias_from_registry(reg)
    files = partiture(blocchi)
    man, errs = C.componi(files, out, alias)
    if errs:
        return None, None, errs
    A.write(os.path.join(out, 'manifesto.json'),
            (json.dumps(man, ensure_ascii=False, indent=1) + '\n').encode('utf-8'))
    hg, _ = A.hg_original(repo)
    new, rep, errs = A.applica(hg, man, out, repo=repo)
    if errs:
        return None, rep, errs
    errs = A.controlla(hg, new, man, out)
    if errs:
        return None, rep, errs
    sd = A.Sdat(hg)
    A.add_aliases(sd, repo)
    righe = []
    per_file = {os.path.splitext(os.path.basename(p))[0]: p for p in files}
    for br in man['brani']:
        sseq, info = A.midi_to_sseq(A.read(os.path.join(out, br['file'])))
        inf = sd.seq_info(sd.seq_index(br['slot']))
        banco = br.get('banco') or sd.name('BANK', inf['banco'])
        volume = br.get('volume', inf['volume'])
        tracks = A.simulate(sseq)
        lp = A.song_loop(tracks)
        insts = A.parse_sbnk(sd.bank_data(sd.bank_index(banco)))
        poly = A.polyphony(tracks, A.kind_func(insts), until=lp[1] if lp else None)
        sch = scheda(per_file[br['simbolo']])
        righe.append({'simbolo': br['simbolo'], 'slot': br['slot'], 'gemello': A.twin_of(sd, br['slot']),
                      'lettore': sd.name('PLAYER', inf['lettore']), 'banco': banco, 'volume': volume,
                      'byte': len(sseq), 'tracce': info['tracce'], 'note': info['note'],
                      'ritornello': list(lp) if lp else None, 'polifonia': poly,
                      'carico': len(sseq) + sd.bank_load_size(sd.bank_index(banco)),
                      'byte_hg': len(sd.seq_data(sd.seq_index(br['slot']))),
                      'partitura': os.path.relpath(per_file[br['simbolo']], PROJ).replace('\\', '/'),
                      **sch})
    return new, righe, []


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--blocchi', nargs='+', required=True)
    ap.add_argument('--repo')
    ap.add_argument('--out', default=os.path.join(PROJ, 'build', 'collaudo'))
    ap.add_argument('--json')
    ap.add_argument('--sdat', action='store_true')
    a = ap.parse_args(argv)
    repo = a.repo or A.default_repo()
    if not repo:
        print('ERRORE A00 repository di HeartGold non trovato (--repo)')
        print('AUDIO_FAILED')
        return 1
    os.makedirs(a.out, exist_ok=True)
    try:
        new, righe, errs = collauda(a.blocchi, a.out, repo)
    except A.AudioError as e:
        errs, righe, new = [('A00', str(e))], None, None
    if errs:
        for r in righe or []:
            if isinstance(r, str):
                print(r)
        A.print_errs(errs)
        print('AUDIO_FAILED')
        return 1
    for r in righe:
        p = r['polifonia']
        print('%-34s %-26s %-18s %6d byte %2d tracce  note insieme %2d (PSG %d, rumore %d)  carico %d' % (
            r['simbolo'], r['slot'], r['banco'], r['byte'], r['tracce'], p['totale'], p.get('psg', 0),
            p.get('rumore', 0), r['carico']))
    if a.json:
        A.write(a.json, (json.dumps(righe, ensure_ascii=False, indent=1) + '\n').encode('utf-8'))
    if a.sdat:
        A.write(os.path.join(a.out, 'gs_sound_data.sdat'), new)
    print('%d brani, archivio di %d byte, controllo con l\'originale superato' % (len(righe), len(new)))
    print('AUDIO_OK')
    return 0


if __name__ == '__main__':
    sys.exit(main())
