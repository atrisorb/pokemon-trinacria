#include "constants/scrcmd.h"
#include "fielddata/script/scr_seq/event_T20R0201.h"
#include "msgdata/msg/msg_0545_T20R0201.h"
#include "macros/script.inc"


	ScrDef scr_seq_T20R0201_000
	ScrDef scr_seq_T20R0201_001
	ScrDef scr_seq_T20R0201_002
	ScrDef scr_seq_T20R0201_003
	ScrDef scr_seq_T20R0201_004
	ScrDef scr_seq_T20R0201_005
	ScrDef scr_seq_T20R0201_006
	ScrDef scr_seq_T20R0201_007
	ScrDefEnd

scr_seq_T20R0201_000:
	ScrCmd_609
	LockAll
	ApplyMovement obj_player, _scena_giocatore
	ApplyMovement obj_t20r0201_graziella, _scena_madre_1
	WaitMovement
	CallStd std_play_mom_music
	Wait 30, VAR_SPECIAL_RESULT
	ApplyMovement obj_t20r0201_graziella, _scena_madre_2
	WaitMovement
	BufferPlayersName 0
	GenderMsgBox msg_0545_T20R0201_00000, msg_0545_T20R0201_00001
	SetFlag FLAG_GOT_BAG
	PlayFanfare SEQ_SE_PL_KIRAKIRA
	WaitFanfare
	NPCMsg msg_0545_T20R0201_00002
	SetFlag FLAG_GOT_TRAINER_CARD
	PlayFanfare SEQ_SE_PL_KIRAKIRA
	WaitFanfare
	NPCMsg msg_0545_T20R0201_00003
	SetFlag FLAG_GOT_SAVE_BUTTON
	PlayFanfare SEQ_SE_PL_KIRAKIRA
	WaitFanfare
	NPCMsg msg_0545_T20R0201_00004
	SetFlag FLAG_GOT_OPTIONS_BUTTON
	PlayFanfare SEQ_SE_PL_KIRAKIRA
	WaitFanfare
	NPCMsg msg_0545_T20R0201_00005
	NPCMsg msg_0545_T20R0201_00006
	BufferPlayersName 0
	NPCMsg msg_0545_T20R0201_00007
	SetFlag FLAG_GOT_POKEGEAR
	PlayFanfare SEQ_ME_ITEM
	WaitFanfare
	NPCMsg msg_0545_T20R0201_00008
	NPCMsg msg_0545_T20R0201_00009
	TouchscreenMenuHide
	GetMenuChoice VAR_SPECIAL_RESULT
	TouchscreenMenuShow
	Compare VAR_SPECIAL_RESULT, 0
	GoToIfNe _scena_telefono_no
	NPCMsg msg_0545_T20R0201_00010
	GoTo _scena_telefono_fine

_scena_telefono_no:
	NPCMsg msg_0545_T20R0201_00011
_scena_telefono_fine:
	NPCMsg msg_0545_T20R0201_00012
	WaitButtonOrDpad
	CloseMsg
	SetFlag FLAG_M_CT_01
	SetVar VAR_TRINACRIA_ATTO, 1
	SetVar VAR_TR_SCENE_CT_01, 6
	ApplyMovement obj_t20r0201_graziella, _scena_madre_3
	WaitMovement
	CallStd std_fade_end_mom_music
	ReleaseAll
	End

	.balign 4, 0
_scena_giocatore:
	Delay4
	WalkOnSpotNormalSouth
	EndMovement

	.balign 4, 0
_scena_madre_1:
	WalkOnSpotNormalNorth
	EndMovement

	.balign 4, 0
_scena_madre_2:
	WalkNormalNorth 2
	WalkNormalWest 3
	WalkNormalNorth
	EndMovement

	.balign 4, 0
_scena_madre_3:
	WalkOnSpotNormalSouth
	WalkNormalSouth 3
	WalkNormalEast 3
	WalkOnSpotNormalNorth
	EndMovement

scr_seq_T20R0201_001:
	GoToIfSet FLAG_GOT_STARTER, _madre_risparmi
	SimpleNPCMsg msg_0545_T20R0201_00013
	End

_madre_risparmi:
	PlaySE SEQ_SE_DP_SELECT
	LockAll
	FacePlayer
	GoToIfSet FLAG_TALKED_TO_MOM_AFTER_NAMING_RIVAL, _madre_menu
	CheckBadge BADGE_DOSSIER_LIOTRU, VAR_TEMP_x4000
	Compare VAR_TEMP_x4000, 0
	GoToIfNe _madre_prima_dossier
	NPCMsg msg_0545_T20R0201_00014
	GoTo _madre_prima_scelta

_madre_prima_dossier:
	BufferPlayersName 0
	NPCMsg msg_0545_T20R0201_00015
_madre_prima_scelta:
	SetFlag FLAG_TALKED_TO_MOM_AFTER_NAMING_RIVAL
	TouchscreenMenuHide
	GetMenuChoice VAR_SPECIAL_RESULT
	TouchscreenMenuShow
	Compare VAR_SPECIAL_RESULT, 0
	GoToIfNe _madre_prima_no
	NPCMsg msg_0545_T20R0201_00016
	SetFlag FLAG_SYS_MOMS_SAVINGS
	GoTo _madre_prima_fine

_madre_prima_no:
	NPCMsg msg_0545_T20R0201_00017
	ClearFlag FLAG_SYS_MOMS_SAVINGS
_madre_prima_fine:
	WaitButton
	CloseMsg
	ReleaseAll
	End

_madre_menu:
	NPCMsg msg_0545_T20R0201_00018
	ScrCmd_795 1, 1
	TouchscreenMenuHide
	MenuInit 1, 1, 0, 1, VAR_SPECIAL_RESULT
	MenuItemAdd 27, 255, 0
	MenuItemAdd 28, 255, 1
	MenuItemAdd 29, 255, 2
	MenuItemAdd 30, 255, 3
	MenuExec
	Switch VAR_SPECIAL_RESULT
	Case 0, _madre_preleva
	Case 1, _madre_deposita
	Case 2, _madre_cambia
	GoTo _madre_esci
	End

_madre_preleva:
	BankOrWalletIsFull 1, VAR_SPECIAL_RESULT
	Compare VAR_SPECIAL_RESULT, 1
	GoToIfEq _madre_portafoglio_pieno
	CheckBankBalance VAR_SPECIAL_RESULT, 1
	Compare VAR_SPECIAL_RESULT, 0
	GoToIfEq _madre_niente_risparmi
	BankTransaction 1, VAR_SPECIAL_RESULT
	ScrCmd_796
	TouchscreenMenuShow
	Switch VAR_SPECIAL_RESULT
	Case 0, _madre_dopo_preleva
	Case 1, _madre_arrivederci
	ReleaseAll
	End

_madre_deposita:
	BankOrWalletIsFull 0, VAR_SPECIAL_RESULT
	Compare VAR_SPECIAL_RESULT, 1
	GoToIfEq _madre_salvadanaio_pieno
	HasEnoughMoneyVar VAR_SPECIAL_RESULT, 1
	Compare VAR_SPECIAL_RESULT, 0
	GoToIfEq _madre_niente_soldi
	BankTransaction 0, VAR_SPECIAL_RESULT
	ScrCmd_796
	TouchscreenMenuShow
	Switch VAR_SPECIAL_RESULT
	Case 0, _madre_dopo_deposita
	Case 1, _madre_arrivederci
	ReleaseAll
	End

_madre_niente_soldi:
	TouchscreenMenuShow
	ScrCmd_796
	NPCMsg msg_0545_T20R0201_00024
	WaitButton
	CloseMsg
	ReleaseAll
	End

_madre_cambia:
	NPCMsg msg_0545_T20R0201_00023
	TouchscreenMenuHide
	GetMenuChoice VAR_SPECIAL_RESULT
	TouchscreenMenuShow
	ScrCmd_796
	Compare VAR_SPECIAL_RESULT, 0
	GoToIfNe _madre_cambia_no
	BufferPlayersName 0
	NPCMsg msg_0545_T20R0201_00016
	SetFlag FLAG_SYS_MOMS_SAVINGS
	GoTo _madre_cambia_fine

_madre_cambia_no:
	NPCMsg msg_0545_T20R0201_00017
	ClearFlag FLAG_SYS_MOMS_SAVINGS
_madre_cambia_fine:
	WaitButton
	CloseMsg
	ReleaseAll
	End

_madre_esci:
	ScrCmd_796
	TouchscreenMenuShow
	NPCMsg msg_0545_T20R0201_00019
	WaitButton
	CloseMsg
	ReleaseAll
	End

_madre_dopo_preleva:
	CloseMsg
	Wait 8, VAR_SPECIAL_RESULT
	PlaySE SEQ_SE_GS_OKOZUKAI
	BufferPlayersName 0
	NPCMsg msg_0545_T20R0201_00022
	WaitButton
	CloseMsg
	ReleaseAll
	End

_madre_dopo_deposita:
	CloseMsg
	Wait 8, VAR_SPECIAL_RESULT
	PlaySE SEQ_SE_GS_OKOZUKAI
	NPCMsg msg_0545_T20R0201_00021
	WaitButton
	CloseMsg
	ReleaseAll
	End

_madre_arrivederci:
	NPCMsg msg_0545_T20R0201_00019
	WaitButton
	CloseMsg
	ReleaseAll
	End

_madre_niente_risparmi:
	TouchscreenMenuShow
	ScrCmd_796
	NPCMsg msg_0545_T20R0201_00020
	WaitButton
	CloseMsg
	ReleaseAll
	End

_madre_salvadanaio_pieno:
	TouchscreenMenuShow
	ScrCmd_796
	NPCMsg msg_0545_T20R0201_00025
	WaitButton
	CloseMsg
	ReleaseAll
	End

_madre_portafoglio_pieno:
	TouchscreenMenuShow
	ScrCmd_796
	NPCMsg msg_0545_T20R0201_00026
	WaitButton
	CloseMsg
	ReleaseAll
	End

scr_seq_T20R0201_002:
	PlaySE SEQ_SE_DP_SELECT
	LockAll
	NPCMsg msg_0545_T20R0201_00031
	WaitButton
	CloseMsg
	ReleaseAll
	End

scr_seq_T20R0201_003:
	PlaySE SEQ_SE_DP_SELECT
	LockAll
	NPCMsg msg_0545_T20R0201_00032
	WaitButton
	CloseMsg
	ReleaseAll
	End

scr_seq_T20R0201_004:
	PlaySE SEQ_SE_DP_SELECT
	LockAll
	NPCMsg msg_0545_T20R0201_00033
	WaitButton
	CloseMsg
	ReleaseAll
	End

scr_seq_T20R0201_005:
	PlaySE SEQ_SE_DP_SELECT
	LockAll
	NPCMsg msg_0545_T20R0201_00034
	WaitButton
	CloseMsg
	ReleaseAll
	End

scr_seq_T20R0201_006:
	PlaySE SEQ_SE_DP_SELECT
	LockAll
	FacePlayer
	PlayCry SPECIES_MR_MIME, 0
	NPCMsg msg_0545_T20R0201_00035
	WaitCry
	WaitButton
	CloseMsg
	ReleaseAll
	End

scr_seq_T20R0201_007:
	PlaySE SEQ_SE_DP_SELECT
	LockAll
	FacePlayer
	PlayCry SPECIES_DELCATTY, 0
	NPCMsg msg_0545_T20R0201_00036
	WaitCry
	WaitButton
	CloseMsg
	ReleaseAll
	End

	.balign 4, 0
