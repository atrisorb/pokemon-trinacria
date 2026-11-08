#include "constants/scrcmd.h"
#include "fielddata/script/scr_seq/event_T20R0201.h"
#include "constants/init_script_types.h"
#include "macros/script.inc"



	InitScriptEntry_OnFrameTable scr_seq_T20R0201_map_scripts_2
	InitScriptEntryEnd

scr_seq_T20R0201_map_scripts_2:
	InitScriptGoToIfEqual VAR_TR_SCENE_CT_01, 5, _EV_scr_seq_T20R0201_000 + 1
	InitScriptFrameTableEnd

	InitScriptEnd
