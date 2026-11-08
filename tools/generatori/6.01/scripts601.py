"""Script (.s), intestazioni, header degli eventi e zone_event delle tre mappe del blocco 6.01.

Le macro sono quelle reali di asm/macros/script.inc e movement.inc (il controllo e' trinacria_script_check.py).
Indentazione a tabulazione, fine riga LF, come i file di HeartGold.
"""

# --- schema: variabile di scena del Prologo (R-VAR-03), valori in sezione «risorse» del blocco -------
VAR = 'VAR_TR_SCENE_CT_01'


def corpo(righe):
    """Etichette a margine; ogni altra riga con una tabulazione (come i file di HeartGold)."""
    return ''.join((r if (not r or r.endswith(':')) else '\t' + r) + '\n' for r in righe)


def testata(codice, banco):
    return ('#include "constants/scrcmd.h"\n'
            '#include "fielddata/script/scr_seq/event_%s.h"\n'
            '#include "msgdata/msg/%s.h"\n'
            '#include "macros/script.inc"\n\n\n' % (codice, banco))


def scrdef(codice, n):
    return ''.join('\tScrDef scr_seq_%s_%03d\n' % (codice, i) for i in range(n)) + '\tScrDefEnd\n\n'


def msg(banco, i):
    return '%s_%05d' % (banco, i)


# ----------------------------------------------------------------------------------------------
# Cubbar (T25SP0101)

def cubbar():
    C, B = 'T25SP0101', 'msg_0603_T25SP0101'

    def m(i):
        return msg(B, i)

    def umano(n, i):
        return ['scr_seq_%s_%03d:' % (C, n), 'PlaySE SEQ_SE_DP_SELECT', 'LockAll', 'FacePlayer',
                'BufferPlayersName 0', 'NPCMsg ' + m(i), 'WaitButton', 'CloseMsg', 'ReleaseAll', 'End', '']

    def pokemon(n, i, specie):
        return ['scr_seq_%s_%03d:' % (C, n), 'PlaySE SEQ_SE_DP_SELECT', 'LockAll', 'FacePlayer',
                'PlayCry %s, 0' % specie, 'NPCMsg ' + m(i), 'WaitCry', 'WaitButton', 'CloseMsg', 'ReleaseAll', 'End', '']

    s = []
    s += ['scr_seq_%s_000:' % C, 'PlaySE SEQ_SE_DP_SELECT', 'LockAll', 'FacePlayer', 'BufferPlayersName 0',
          'Compare %s, 3' % VAR, 'GoToIfGe _christian_dopo']
    s += ['NPCMsg ' + m(i) for i in (8, 9, 10, 11, 12)]
    s += ['SetVar %s, 3' % VAR, 'WaitButton', 'CloseMsg', 'ReleaseAll', 'End', '',
          '_christian_dopo:', 'BufferPlayersName 0', 'NPCMsg ' + m(13), 'WaitButton', 'CloseMsg', 'ReleaseAll', 'End', '']
    s += pokemon(1, 14, 'SPECIES_EXPLOUD')
    s += umano(2, 2) + pokemon(3, 15, 'SPECIES_PERSIAN')
    s += umano(4, 3) + pokemon(5, 16, 'SPECIES_NINETALES')
    s += umano(6, 4) + umano(7, 5) + umano(8, 6)
    s += umano(9, 7) + pokemon(10, 17, 'SPECIES_HOUNDOOM')
    # 011: arrivo nel Cubbar (OnFrame, variabile = 1)
    s += ['scr_seq_%s_011:' % C, 'LockAll', 'NPCMsg ' + m(0), 'NPCMsg ' + m(1), 'WaitButton', 'CloseMsg',
          'SetVar %s, 2' % VAR, 'ReleaseAll', 'End', '']
    # 012: uscita chiusa finche' non si e' parlato con Christian (coords, variabile = 2)
    s += ['scr_seq_%s_012:' % C, 'LockAll', 'NPCMsg ' + m(18), 'WaitButton', 'CloseMsg',
          'ApplyMovement obj_player, _indietro', 'WaitMovement', 'ReleaseAll', 'End', '',
          '.balign 4, 0', '_indietro:', 'WalkNormalNorth', 'EndMovement', '']
    # 013: uscita (coords, variabile = 3): fine del flashback, M-CT-00 completata
    s += ['scr_seq_%s_013:' % C, 'LockAll', 'NPCMsg ' + m(19), 'WaitButton', 'CloseMsg',
          'SetFlag FLAG_M_CT_00', 'SetVar %s, 4' % VAR,
          'FadeScreen 6, 1, 0, RGB_BLACK', 'WaitFade',
          'Warp MAP_CT_CATANIA_CASA_PROTAGONISTA_2F, 0, 5, 6, DIR_SOUTH',
          'FadeScreen 6, 1, 1, RGB_BLACK', 'WaitFade', 'ReleaseAll', 'End', '']
    n = 14
    testo = testata(C, B) + scrdef(C, n) + corpo(s) + '\t.balign 4, 0\n'
    hdr = ('#include "constants/scrcmd.h"\n#include "fielddata/script/scr_seq/event_%s.h"\n'
           '#include "constants/init_script_types.h"\n#include "macros/script.inc"\n\n\n\n'
           '\tInitScriptEntry_OnFrameTable scr_seq_%s_map_scripts_2\n\tInitScriptEntryEnd\n\n'
           'scr_seq_%s_map_scripts_2:\n\tInitScriptGoToIfEqual %s, 1, _EV_scr_seq_%s_011 + 1\n'
           '\tInitScriptFrameTableEnd\n\n\tInitScriptEnd\n' % (C, C, C, VAR, C))
    return testo, hdr, n


# ----------------------------------------------------------------------------------------------
# Camera (T20R0202)

def camera():
    C, B = 'T20R0202', 'msg_0546_T20R0202'

    def m(i):
        return msg(B, i)

    def lettura(n, i):
        return ['scr_seq_%s_%03d:' % (C, n), 'PlaySE SEQ_SE_DP_SELECT', 'LockAll', 'NPCMsg ' + m(i), 'WaitButton',
                'CloseMsg', 'ReleaseAll', 'End', '']

    s = []
    # 000: PC (logica di HeartGold: posta sul PC)
    s += ['scr_seq_%s_000:' % C, 'ScrCmd_609', 'LockAll', 'PlaySE SEQ_SE_DP_PC_ON', 'BufferPlayersName 0',
          'NPCMsg ' + m(0), 'CloseMsg', 'ScrCmd_377 VAR_SPECIAL_RESULT', 'Compare VAR_SPECIAL_RESULT, 0',
          'GoToIfEq _pc_nessuna_mail', 'FadeScreen 6, 1, 0, RGB_BLACK', 'WaitFade', 'ScrCmd_376',
          'RestoreOverworld', 'FadeScreen 6, 1, 1, RGB_BLACK', 'WaitFade', 'ReleaseAll', 'End', '',
          '_pc_nessuna_mail:', 'NPCMsg ' + m(1), 'WaitButton', 'CloseMsg', 'ReleaseAll', 'End', '']
    s += lettura(1, 2)
    # 002: inizio partita, flashback (OnFrame, variabile = 0)
    s += ['scr_seq_%s_002:' % C, 'LockAll', 'NPCMsg ' + m(5), 'WaitButton', 'CloseMsg', 'SetVar %s, 1' % VAR,
          'FadeScreen 6, 1, 0, RGB_BLACK', 'WaitFade', 'Warp MAP_CT_MISTERBIANCO_CUBBAR, 0, 16, 22, DIR_NORTH',
          'FadeScreen 6, 1, 1, RGB_BLACK', 'WaitFade', 'ReleaseAll', 'End', '']
    # 003: risveglio (OnFrame, variabile = 4): primo script di M-CT-01 (ScrCmd_804 2, 4.4 R-GFX-33)
    s += ['scr_seq_%s_003:' % C, 'LockAll', 'ScrCmd_804 2', 'BufferPlayersName 0',
          'NPCMsg ' + m(6), 'NPCMsg ' + m(7), 'NPCMsg ' + m(8), 'NPCMsg ' + m(9), 'WaitButton', 'CloseMsg',
          'SetVar %s, 5' % VAR, 'ReleaseAll', 'End', '']
    s += lettura(4, 3) + lettura(5, 4)
    n = 6
    testo = testata(C, B) + scrdef(C, n) + corpo(s) + '\t.balign 4, 0\n'
    hdr = ('#include "constants/scrcmd.h"\n#include "fielddata/script/scr_seq/event_%s.h"\n'
           '#include "constants/init_script_types.h"\n#include "macros/script.inc"\n\n\n\n'
           '\tInitScriptEntry_OnFrameTable scr_seq_%s_map_scripts_2\n\tInitScriptEntryEnd\n\n'
           'scr_seq_%s_map_scripts_2:\n\tInitScriptGoToIfEqual %s, 0, _EV_scr_seq_%s_002 + 1\n'
           '\tInitScriptGoToIfEqual %s, 4, _EV_scr_seq_%s_003 + 1\n'
           '\tInitScriptFrameTableEnd\n\n\tInitScriptEnd\n' % (C, C, C, VAR, C, VAR, C))
    return testo, hdr, n


# ----------------------------------------------------------------------------------------------
# Casa, piano terra (T20R0201)

def casa():
    C, B = 'T20R0201', 'msg_0545_T20R0201'
    MAMMA = 'obj_t20r0201_graziella'

    def m(i):
        return msg(B, i)

    def lettura(n, i):
        return ['scr_seq_%s_%03d:' % (C, n), 'PlaySE SEQ_SE_DP_SELECT', 'LockAll', 'NPCMsg ' + m(i), 'WaitButton',
                'CloseMsg', 'ReleaseAll', 'End', '']

    s = []
    # 000: scena della madre (OnFrame, variabile = 5): chiude M-CT-01
    s += ['scr_seq_%s_000:' % C, 'ScrCmd_609', 'LockAll',
          'ApplyMovement obj_player, _scena_giocatore', 'ApplyMovement %s, _scena_madre_1' % MAMMA, 'WaitMovement',
          'CallStd std_play_mom_music', 'Wait 30, VAR_SPECIAL_RESULT',
          'ApplyMovement %s, _scena_madre_2' % MAMMA, 'WaitMovement', 'BufferPlayersName 0',
          'GenderMsgBox %s, %s' % (m(0), m(1)),
          'SetFlag FLAG_GOT_BAG', 'PlayFanfare SEQ_SE_PL_KIRAKIRA', 'WaitFanfare', 'NPCMsg ' + m(2),
          'SetFlag FLAG_GOT_TRAINER_CARD', 'PlayFanfare SEQ_SE_PL_KIRAKIRA', 'WaitFanfare', 'NPCMsg ' + m(3),
          'SetFlag FLAG_GOT_SAVE_BUTTON', 'PlayFanfare SEQ_SE_PL_KIRAKIRA', 'WaitFanfare', 'NPCMsg ' + m(4),
          'SetFlag FLAG_GOT_OPTIONS_BUTTON', 'PlayFanfare SEQ_SE_PL_KIRAKIRA', 'WaitFanfare', 'NPCMsg ' + m(5),
          'NPCMsg ' + m(6), 'BufferPlayersName 0', 'NPCMsg ' + m(7),
          'SetFlag FLAG_GOT_POKEGEAR', 'PlayFanfare SEQ_ME_ITEM', 'WaitFanfare',
          'NPCMsg ' + m(8), 'NPCMsg ' + m(9), 'TouchscreenMenuHide', 'GetMenuChoice VAR_SPECIAL_RESULT',
          'TouchscreenMenuShow', 'Compare VAR_SPECIAL_RESULT, 0', 'GoToIfNe _scena_telefono_no',
          'NPCMsg ' + m(10), 'GoTo _scena_telefono_fine', '',
          '_scena_telefono_no:', 'NPCMsg ' + m(11),
          '_scena_telefono_fine:', 'NPCMsg ' + m(12), 'WaitButtonOrDpad', 'CloseMsg',
          'SetFlag FLAG_M_CT_01', 'SetVar VAR_TRINACRIA_ATTO, 1', 'SetVar %s, 6' % VAR,
          'ApplyMovement %s, _scena_madre_3' % MAMMA, 'WaitMovement', 'CallStd std_fade_end_mom_music',
          'ReleaseAll', 'End', '',
          '.balign 4, 0', '_scena_giocatore:', 'Delay4', 'WalkOnSpotNormalSouth', 'EndMovement', '',
          '.balign 4, 0', '_scena_madre_1:', 'WalkOnSpotNormalNorth', 'EndMovement', '',
          '.balign 4, 0', '_scena_madre_2:', 'WalkNormalNorth 2', 'WalkNormalWest 3', 'WalkNormalNorth', 'EndMovement', '',
          '.balign 4, 0', '_scena_madre_3:', 'WalkOnSpotNormalSouth', 'WalkNormalSouth 3', 'WalkNormalEast 3',
          'WalkOnSpotNormalNorth', 'EndMovement', '']
    # 001: Graziella (dialogo e risparmi di HeartGold, ex «mamma»)
    s += ['scr_seq_%s_001:' % C, 'GoToIfSet FLAG_GOT_STARTER, _madre_risparmi', 'SimpleNPCMsg ' + m(13), 'End', '',
          '_madre_risparmi:', 'PlaySE SEQ_SE_DP_SELECT', 'LockAll', 'FacePlayer',
          'GoToIfSet FLAG_TALKED_TO_MOM_AFTER_NAMING_RIVAL, _madre_menu',
          'CheckBadge BADGE_DOSSIER_LIOTRU, VAR_TEMP_x4000', 'Compare VAR_TEMP_x4000, 0',
          'GoToIfNe _madre_prima_dossier', 'NPCMsg ' + m(14), 'GoTo _madre_prima_scelta', '',
          '_madre_prima_dossier:', 'BufferPlayersName 0', 'NPCMsg ' + m(15),
          '_madre_prima_scelta:', 'SetFlag FLAG_TALKED_TO_MOM_AFTER_NAMING_RIVAL',
          'TouchscreenMenuHide', 'GetMenuChoice VAR_SPECIAL_RESULT', 'TouchscreenMenuShow',
          'Compare VAR_SPECIAL_RESULT, 0', 'GoToIfNe _madre_prima_no', 'NPCMsg ' + m(16),
          'SetFlag FLAG_SYS_MOMS_SAVINGS', 'GoTo _madre_prima_fine', '',
          '_madre_prima_no:', 'NPCMsg ' + m(17), 'ClearFlag FLAG_SYS_MOMS_SAVINGS',
          '_madre_prima_fine:', 'WaitButton', 'CloseMsg', 'ReleaseAll', 'End', '',
          '_madre_menu:', 'NPCMsg ' + m(18), 'ScrCmd_795 1, 1', 'TouchscreenMenuHide',
          'MenuInit 1, 1, 0, 1, VAR_SPECIAL_RESULT', 'MenuItemAdd 27, 255, 0', 'MenuItemAdd 28, 255, 1',
          'MenuItemAdd 29, 255, 2', 'MenuItemAdd 30, 255, 3', 'MenuExec', 'Switch VAR_SPECIAL_RESULT',
          'Case 0, _madre_preleva', 'Case 1, _madre_deposita', 'Case 2, _madre_cambia', 'GoTo _madre_esci', 'End', '',
          '_madre_preleva:', 'BankOrWalletIsFull 1, VAR_SPECIAL_RESULT', 'Compare VAR_SPECIAL_RESULT, 1',
          'GoToIfEq _madre_portafoglio_pieno', 'CheckBankBalance VAR_SPECIAL_RESULT, 1',
          'Compare VAR_SPECIAL_RESULT, 0', 'GoToIfEq _madre_niente_risparmi',
          'BankTransaction 1, VAR_SPECIAL_RESULT', 'ScrCmd_796', 'TouchscreenMenuShow',
          'Switch VAR_SPECIAL_RESULT', 'Case 0, _madre_dopo_preleva', 'Case 1, _madre_arrivederci', 'ReleaseAll', 'End', '',
          '_madre_deposita:', 'BankOrWalletIsFull 0, VAR_SPECIAL_RESULT', 'Compare VAR_SPECIAL_RESULT, 1',
          'GoToIfEq _madre_salvadanaio_pieno', 'HasEnoughMoneyVar VAR_SPECIAL_RESULT, 1',
          'Compare VAR_SPECIAL_RESULT, 0', 'GoToIfEq _madre_niente_soldi',
          'BankTransaction 0, VAR_SPECIAL_RESULT', 'ScrCmd_796', 'TouchscreenMenuShow',
          'Switch VAR_SPECIAL_RESULT', 'Case 0, _madre_dopo_deposita', 'Case 1, _madre_arrivederci', 'ReleaseAll', 'End', '',
          '_madre_niente_soldi:', 'TouchscreenMenuShow', 'ScrCmd_796', 'NPCMsg ' + m(24), 'WaitButton', 'CloseMsg',
          'ReleaseAll', 'End', '',
          '_madre_cambia:', 'NPCMsg ' + m(23), 'TouchscreenMenuHide', 'GetMenuChoice VAR_SPECIAL_RESULT',
          'TouchscreenMenuShow', 'ScrCmd_796', 'Compare VAR_SPECIAL_RESULT, 0', 'GoToIfNe _madre_cambia_no',
          'BufferPlayersName 0', 'NPCMsg ' + m(16), 'SetFlag FLAG_SYS_MOMS_SAVINGS', 'GoTo _madre_cambia_fine', '',
          '_madre_cambia_no:', 'NPCMsg ' + m(17), 'ClearFlag FLAG_SYS_MOMS_SAVINGS',
          '_madre_cambia_fine:', 'WaitButton', 'CloseMsg', 'ReleaseAll', 'End', '',
          '_madre_esci:', 'ScrCmd_796', 'TouchscreenMenuShow', 'NPCMsg ' + m(19), 'WaitButton', 'CloseMsg',
          'ReleaseAll', 'End', '',
          '_madre_dopo_preleva:', 'CloseMsg', 'Wait 8, VAR_SPECIAL_RESULT', 'PlaySE SEQ_SE_GS_OKOZUKAI',
          'BufferPlayersName 0', 'NPCMsg ' + m(22), 'WaitButton', 'CloseMsg', 'ReleaseAll', 'End', '',
          '_madre_dopo_deposita:', 'CloseMsg', 'Wait 8, VAR_SPECIAL_RESULT', 'PlaySE SEQ_SE_GS_OKOZUKAI',
          'NPCMsg ' + m(21), 'WaitButton', 'CloseMsg', 'ReleaseAll', 'End', '',
          '_madre_arrivederci:', 'NPCMsg ' + m(19), 'WaitButton', 'CloseMsg', 'ReleaseAll', 'End', '',
          '_madre_niente_risparmi:', 'TouchscreenMenuShow', 'ScrCmd_796', 'NPCMsg ' + m(20), 'WaitButton',
          'CloseMsg', 'ReleaseAll', 'End', '',
          '_madre_salvadanaio_pieno:', 'TouchscreenMenuShow', 'ScrCmd_796', 'NPCMsg ' + m(25), 'WaitButton',
          'CloseMsg', 'ReleaseAll', 'End', '',
          '_madre_portafoglio_pieno:', 'TouchscreenMenuShow', 'ScrCmd_796', 'NPCMsg ' + m(26), 'WaitButton',
          'CloseMsg', 'ReleaseAll', 'End', '']
    s += lettura(2, 31) + lettura(3, 32) + lettura(4, 33) + lettura(5, 34)
    # Pokemon di casa: Puparu (Mr. Mime) e Leccu (Delcatty)
    for n, i, sp in ((6, 35, 'SPECIES_MR_MIME'), (7, 36, 'SPECIES_DELCATTY')):
        s += ['scr_seq_%s_%03d:' % (C, n), 'PlaySE SEQ_SE_DP_SELECT', 'LockAll', 'FacePlayer',
              'PlayCry %s, 0' % sp, 'NPCMsg ' + m(i), 'WaitCry', 'WaitButton', 'CloseMsg', 'ReleaseAll', 'End', '']
    n = 8
    testo = testata(C, B) + scrdef(C, n) + corpo(s) + '\t.balign 4, 0\n'
    hdr = ('#include "constants/scrcmd.h"\n#include "fielddata/script/scr_seq/event_%s.h"\n'
           '#include "constants/init_script_types.h"\n#include "macros/script.inc"\n\n\n\n'
           '\tInitScriptEntry_OnFrameTable scr_seq_%s_map_scripts_2\n\tInitScriptEntryEnd\n\n'
           'scr_seq_%s_map_scripts_2:\n\tInitScriptGoToIfEqual %s, 5, _EV_scr_seq_%s_000 + 1\n'
           '\tInitScriptFrameTableEnd\n\n\tInitScriptEnd\n' % (C, C, C, VAR, C))
    return testo, hdr, n


# ----------------------------------------------------------------------------------------------
# Eventi (zone_event) e header

def oggetto(oid, sprite, x, z, script, direzione, flag='FLAG_NOTHING'):
    return {'id': oid, 'spriteId': sprite, 'movement': 0, 'type': 0, 'eventFlag': flag,
            'scriptId': '_EV_scr_seq_%s + 1' % script if script else 0, 'facingDirection': direzione,
            'param0': 0, 'param1': 0, 'param2': 0, 'xRange': 0, 'yRange': 0, 'x': x, 'z': z, 'y': 0}


def bg(script, x, z, d=0):
    return {'scriptId': '_EV_scr_seq_%s + 1' % script, 'type': 0, 'x': x, 'z': z, 'y': 0, 'dir': d}


def coord(script, x, z, val):
    return {'scriptId': '_EV_scr_seq_%s + 1' % script, 'x': x, 'z': z, 'w': 1, 'h': 1, 'y': 0, 'val': val, 'var': VAR}


def warp(x, z, mappa, ancora):
    return {'x': x, 'z': z, 'header': mappa, 'anchor': ancora, 'y': 0}


# direzioni dei sillabari: 0 nord, 1 sud, 2 ovest, 3 est
def eventi():
    C = 'T25SP0101'
    S = lambda n: '%s_%03d' % (C, n)
    A = 'FLAG_M_CT_00'
    cubbar_obj = [
        oggetto('obj_t25sp0101_christian', 'SPRITE_TRN_CHRISTIAN', 13, 11, S(0), 1, A),
        oggetto('obj_t25sp0101_subwoofer', 'SPRITE_FOLLOWER_MON_EXPLOUD', 14, 11, S(1), 1, A),
        oggetto('obj_t25sp0101_figlio_avvocato', 'SPRITE_GORGGEOUSM', 8, 16, S(2), 1),
        oggetto('obj_t25sp0101_gattupardu', 'SPRITE_FOLLOWER_MON_STATIC_PERSIAN', 9, 16, S(3), 1),
        oggetto('obj_t25sp0101_figlia_magistrato', 'SPRITE_GORGGEOUSW', 11, 16, S(4), 2),
        oggetto('obj_t25sp0101_novicudi', 'SPRITE_FOLLOWER_MON_NINETALES', 12, 16, S(5), 1),
        oggetto('obj_t25sp0101_praticante', 'SPRITE_ASSISTANTM', 14, 16, S(6), 1),
        oggetto('obj_t25sp0101_pr_locale', 'SPRITE_SUNGLASSES', 18, 16, S(7), 1),
        oggetto('obj_t25sp0101_figlia_magistrato_2', 'SPRITE_LADY', 21, 16, S(8), 3),
        oggetto('obj_t25sp0101_figlio_imprenditore', 'SPRITE_BADMAN', 24, 16, S(9), 1),
        oggetto('obj_t25sp0101_diavulazzu', 'SPRITE_FOLLOWER_MON_HOUNDOOM', 25, 16, S(10), 1),
    ]
    cubbar = {'header': 'fielddata/script/scr_seq/event_%s.h' % C, 'bgs': [], 'objects': cubbar_obj,
              'warps': [warp(16, 24, 'MAP_CT_MISTERBIANCO', 0)],
              'coords': [coord(S(12), 16, 23, 2), coord(S(13), 16, 23, 3)]}

    C = 'T20R0202'
    S = lambda n: '%s_%03d' % (C, n)
    camera = {'header': 'fielddata/script/scr_seq/event_%s.h' % C,
              'bgs': [bg(S(0), 6, 4), bg(S(4), 7, 4), bg(S(1), 8, 4), bg(S(5), 10, 4)],
              'objects': [],
              'warps': [warp(3, 4, 'MAP_CT_CATANIA_CASA_PROTAGONISTA_1F', 1)]}

    C = 'T20R0201'
    S = lambda n: '%s_%03d' % (C, n)
    casa = {'header': 'fielddata/script/scr_seq/event_%s.h' % C,
            'bgs': [bg(S(2), 5, 3), bg(S(2), 6, 3), bg(S(4), 8, 3), bg(S(3), 9, 3), bg(S(5), 11, 3)],
            'objects': [oggetto('obj_t20r0201_graziella', 'SPRITE_TRN_GRAZIELLA', 6, 7, S(1), 3),
                        oggetto('obj_t20r0201_puparu', 'SPRITE_FOLLOWER_MON_MR_MIME', 8, 9, S(6), 2),
                        oggetto('obj_t20r0201_leccu', 'SPRITE_FOLLOWER_MON_DELCATTY', 7, 6, S(7), 1)],
            'warps': [warp(3, 10, 'MAP_CT_CATANIA_CORSO_ITALIA', 1),
                      warp(3, 3, 'MAP_CT_CATANIA_CASA_PROTAGONISTA_2F', 0)]}
    return {'MAP_CT_MISTERBIANCO_CUBBAR': cubbar, 'MAP_CT_CATANIA_CASA_PROTAGONISTA_2F': camera,
            'MAP_CT_CATANIA_CASA_PROTAGONISTA_1F': casa}


def header_eventi(codice, n_script, oggetti):
    righe = ['#ifndef SCR_SEQ_%s_H_' % codice, '#define SCR_SEQ_%s_H_' % codice, '']
    righe += ['#define _EV_scr_seq_%s_%03d %d' % (codice, i, i) for i in range(n_script)]
    righe += ['']
    righe += ['#define %s %d' % (o['id'], i) for i, o in enumerate(oggetti)]
    righe += ['', '#endif // SCR_SEQ_%s_H_' % codice, '']
    return '\n'.join(righe)
