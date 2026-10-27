"""Lotta col Segretario di Enna (classe ex LEADER_BLUE) e coi Segretari nella regione Kanto del
motore: stesso brano di SEQ_TRN_LOTTA_SEGRETERIA, con lo stesso banco e lo stesso volume."""
import os
import runpy

_BASE = runpy.run_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'SEQ_TRN_LOTTA_SEGRETERIA.py'))

SIMBOLO = 'SEQ_TRN_LOTTA_SEGRETERIA_EST'
BANCO = _BASE['BANCO']
VOLUME = _BASE['VOLUME']
SCHEDA = dict(_BASE['SCHEDA'], stesso_brano='SEQ_TRN_LOTTA_SEGRETERIA')
partitura = _BASE['partitura']
