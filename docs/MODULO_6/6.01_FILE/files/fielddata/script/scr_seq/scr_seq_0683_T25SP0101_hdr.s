#include "constants/scrcmd.h"
#include "fielddata/script/scr_seq/event_T25SP0101.h"
#include "constants/init_script_types.h"
#include "macros/script.inc"



	InitScriptEntry_OnFrameTable scr_seq_T25SP0101_map_scripts_2
	InitScriptEntryEnd

scr_seq_T25SP0101_map_scripts_2:
	InitScriptGoToIfEqual VAR_TR_SCENE_CT_01, 1, _EV_scr_seq_T25SP0101_011 + 1
	InitScriptFrameTableEnd

	InitScriptEnd
