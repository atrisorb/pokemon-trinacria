#include "constants/scrcmd.h"
#include "fielddata/script/scr_seq/event_T25SP0101.h"
#include "msgdata/msg/msg_0603_T25SP0101.h"
#include "macros/script.inc"


	ScrDef scr_seq_T25SP0101_000
	ScrDef scr_seq_T25SP0101_001
	ScrDef scr_seq_T25SP0101_002
	ScrDef scr_seq_T25SP0101_003
	ScrDef scr_seq_T25SP0101_004
	ScrDef scr_seq_T25SP0101_005
	ScrDef scr_seq_T25SP0101_006
	ScrDef scr_seq_T25SP0101_007
	ScrDef scr_seq_T25SP0101_008
	ScrDef scr_seq_T25SP0101_009
	ScrDef scr_seq_T25SP0101_010
	ScrDef scr_seq_T25SP0101_011
	ScrDef scr_seq_T25SP0101_012
	ScrDef scr_seq_T25SP0101_013
	ScrDefEnd

scr_seq_T25SP0101_000:
	PlaySE SEQ_SE_DP_SELECT
	LockAll
	FacePlayer
	BufferPlayersName 0
	Compare VAR_TR_SCENE_CT_01, 3
	GoToIfGe _christian_dopo
	NPCMsg msg_0603_T25SP0101_00008
	NPCMsg msg_0603_T25SP0101_00009
	NPCMsg msg_0603_T25SP0101_00010
	NPCMsg msg_0603_T25SP0101_00011
	NPCMsg msg_0603_T25SP0101_00012
	SetVar VAR_TR_SCENE_CT_01, 3
	WaitButton
	CloseMsg
	ReleaseAll
	End

_christian_dopo:
	BufferPlayersName 0
	NPCMsg msg_0603_T25SP0101_00013
	WaitButton
	CloseMsg
	ReleaseAll
	End

scr_seq_T25SP0101_001:
	PlaySE SEQ_SE_DP_SELECT
	LockAll
	FacePlayer
	PlayCry SPECIES_EXPLOUD, 0
	NPCMsg msg_0603_T25SP0101_00014
	WaitCry
	WaitButton
	CloseMsg
	ReleaseAll
	End

scr_seq_T25SP0101_002:
	PlaySE SEQ_SE_DP_SELECT
	LockAll
	FacePlayer
	BufferPlayersName 0
	NPCMsg msg_0603_T25SP0101_00002
	WaitButton
	CloseMsg
	ReleaseAll
	End

scr_seq_T25SP0101_003:
	PlaySE SEQ_SE_DP_SELECT
	LockAll
	FacePlayer
	PlayCry SPECIES_PERSIAN, 0
	NPCMsg msg_0603_T25SP0101_00015
	WaitCry
	WaitButton
	CloseMsg
	ReleaseAll
	End

scr_seq_T25SP0101_004:
	PlaySE SEQ_SE_DP_SELECT
	LockAll
	FacePlayer
	BufferPlayersName 0
	NPCMsg msg_0603_T25SP0101_00003
	WaitButton
	CloseMsg
	ReleaseAll
	End

scr_seq_T25SP0101_005:
	PlaySE SEQ_SE_DP_SELECT
	LockAll
	FacePlayer
	PlayCry SPECIES_NINETALES, 0
	NPCMsg msg_0603_T25SP0101_00016
	WaitCry
	WaitButton
	CloseMsg
	ReleaseAll
	End

scr_seq_T25SP0101_006:
	PlaySE SEQ_SE_DP_SELECT
	LockAll
	FacePlayer
	BufferPlayersName 0
	NPCMsg msg_0603_T25SP0101_00004
	WaitButton
	CloseMsg
	ReleaseAll
	End

scr_seq_T25SP0101_007:
	PlaySE SEQ_SE_DP_SELECT
	LockAll
	FacePlayer
	BufferPlayersName 0
	NPCMsg msg_0603_T25SP0101_00005
	WaitButton
	CloseMsg
	ReleaseAll
	End

scr_seq_T25SP0101_008:
	PlaySE SEQ_SE_DP_SELECT
	LockAll
	FacePlayer
	BufferPlayersName 0
	NPCMsg msg_0603_T25SP0101_00006
	WaitButton
	CloseMsg
	ReleaseAll
	End

scr_seq_T25SP0101_009:
	PlaySE SEQ_SE_DP_SELECT
	LockAll
	FacePlayer
	BufferPlayersName 0
	NPCMsg msg_0603_T25SP0101_00007
	WaitButton
	CloseMsg
	ReleaseAll
	End

scr_seq_T25SP0101_010:
	PlaySE SEQ_SE_DP_SELECT
	LockAll
	FacePlayer
	PlayCry SPECIES_HOUNDOOM, 0
	NPCMsg msg_0603_T25SP0101_00017
	WaitCry
	WaitButton
	CloseMsg
	ReleaseAll
	End

scr_seq_T25SP0101_011:
	LockAll
	NPCMsg msg_0603_T25SP0101_00000
	NPCMsg msg_0603_T25SP0101_00001
	WaitButton
	CloseMsg
	SetVar VAR_TR_SCENE_CT_01, 2
	ReleaseAll
	End

scr_seq_T25SP0101_012:
	LockAll
	NPCMsg msg_0603_T25SP0101_00018
	WaitButton
	CloseMsg
	ApplyMovement obj_player, _indietro
	WaitMovement
	ReleaseAll
	End

	.balign 4, 0
_indietro:
	WalkNormalNorth
	EndMovement

scr_seq_T25SP0101_013:
	LockAll
	NPCMsg msg_0603_T25SP0101_00019
	WaitButton
	CloseMsg
	SetFlag FLAG_M_CT_00
	SetVar VAR_TR_SCENE_CT_01, 4
	FadeScreen 6, 1, 0, RGB_BLACK
	WaitFade
	Warp MAP_CT_CATANIA_CASA_PROTAGONISTA_2F, 0, 5, 6, DIR_SOUTH
	FadeScreen 6, 1, 1, RGB_BLACK
	WaitFade
	ReleaseAll
	End

	.balign 4, 0
