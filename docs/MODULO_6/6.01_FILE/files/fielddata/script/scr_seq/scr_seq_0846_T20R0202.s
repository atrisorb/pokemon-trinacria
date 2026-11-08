#include "constants/scrcmd.h"
#include "fielddata/script/scr_seq/event_T20R0202.h"
#include "msgdata/msg/msg_0546_T20R0202.h"
#include "macros/script.inc"


	ScrDef scr_seq_T20R0202_000
	ScrDef scr_seq_T20R0202_001
	ScrDef scr_seq_T20R0202_002
	ScrDef scr_seq_T20R0202_003
	ScrDef scr_seq_T20R0202_004
	ScrDef scr_seq_T20R0202_005
	ScrDefEnd

scr_seq_T20R0202_000:
	ScrCmd_609
	LockAll
	PlaySE SEQ_SE_DP_PC_ON
	BufferPlayersName 0
	NPCMsg msg_0546_T20R0202_00000
	CloseMsg
	ScrCmd_377 VAR_SPECIAL_RESULT
	Compare VAR_SPECIAL_RESULT, 0
	GoToIfEq _pc_nessuna_mail
	FadeScreen 6, 1, 0, RGB_BLACK
	WaitFade
	ScrCmd_376
	RestoreOverworld
	FadeScreen 6, 1, 1, RGB_BLACK
	WaitFade
	ReleaseAll
	End

_pc_nessuna_mail:
	NPCMsg msg_0546_T20R0202_00001
	WaitButton
	CloseMsg
	ReleaseAll
	End

scr_seq_T20R0202_001:
	PlaySE SEQ_SE_DP_SELECT
	LockAll
	NPCMsg msg_0546_T20R0202_00002
	WaitButton
	CloseMsg
	ReleaseAll
	End

scr_seq_T20R0202_002:
	LockAll
	NPCMsg msg_0546_T20R0202_00005
	WaitButton
	CloseMsg
	SetVar VAR_TR_SCENE_CT_01, 1
	FadeScreen 6, 1, 0, RGB_BLACK
	WaitFade
	Warp MAP_CT_MISTERBIANCO_CUBBAR, 0, 16, 22, DIR_NORTH
	FadeScreen 6, 1, 1, RGB_BLACK
	WaitFade
	ReleaseAll
	End

scr_seq_T20R0202_003:
	LockAll
	ScrCmd_804 2
	BufferPlayersName 0
	NPCMsg msg_0546_T20R0202_00006
	NPCMsg msg_0546_T20R0202_00007
	NPCMsg msg_0546_T20R0202_00008
	NPCMsg msg_0546_T20R0202_00009
	WaitButton
	CloseMsg
	SetVar VAR_TR_SCENE_CT_01, 5
	ReleaseAll
	End

scr_seq_T20R0202_004:
	PlaySE SEQ_SE_DP_SELECT
	LockAll
	NPCMsg msg_0546_T20R0202_00003
	WaitButton
	CloseMsg
	ReleaseAll
	End

scr_seq_T20R0202_005:
	PlaySE SEQ_SE_DP_SELECT
	LockAll
	NPCMsg msg_0546_T20R0202_00004
	WaitButton
	CloseMsg
	ReleaseAll
	End

	.balign 4, 0
