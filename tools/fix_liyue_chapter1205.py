#!/usr/bin/env python3
from __future__ import annotations

import fix_inazuma_chapter1204  # noqa: F401 - extends the shared manifest on import
import fix_liyue_prerequisites as base
from fix_quest_prerequisites import Repair, one

QUEST_GLOBAL_VAR_EQUAL = "QUEST_COND_QUEST_GLOBAL_VAR_EQUAL"


def global_var_equal(var_id: int, value: int) -> tuple[dict, ...]:
    return ({"type": QUEST_GLOBAL_VAR_EQUAL, "param": [var_id, value, 0, 0, 0], "param_str": ""},)


# Liyue Chapter 1205 prerequisite repairs.
# Evidence: GCResource 3.7 + 4.0 byte-identical for MQ11009/11013/11014/11015;
# current 7.1 BinOutput lost acceptCond on all 81 rows; flattened QuestExcel damages exactly 38.
CHAPTER_1205_REPAIRS = (
    # MQ11009
    Repair("11009.json", 11009, 1100901, -1, global_var_equal(10006, 1), (one(0),)),
    Repair("11009.json", 11009, 1100902, -1, one(1100905), ()),
    Repair("11009.json", 11009, 1100903, -1, one(1100902), ()),
    Repair("11009.json", 11009, 1100904, -1, one(99902), (one(0),)),
    Repair("11009.json", 11009, 1100905, -1, one(1100901), ()),
    Repair("11009.json", 11009, 1100906, -1, one(1100902), (one(1100907),)),
    Repair("11009.json", 11009, 1100907, -1, one(1100902), (one(1100903),)),

    # MQ11013
    Repair("11013.json", 11013, 1101301, -1, one(1100903), (one(0),)),
    Repair("11013.json", 11013, 1101302, -1, one(99902), (one(0),)),
    Repair("11013.json", 11013, 1101303, -1, one(99902), (one(1101302),)),
    Repair("11013.json", 11013, 1101304, -1, one(99902), (one(1101303),)),
    Repair("11013.json", 11013, 1101305, -1, one(1101326), (one(1101327),)),
    Repair("11013.json", 11013, 1101306, -1, one(1101305), ()),
    Repair("11013.json", 11013, 1101307, -1, one(1101306), (one(1101328),)),
    Repair("11013.json", 11013, 1101308, -1, one(1101307), ()),
    Repair("11013.json", 11013, 1101309, -1, one(1101308), (one(1101329),)),
    Repair("11013.json", 11013, 1101310, -1, one(1101309), ()),
    Repair("11013.json", 11013, 1101311, -1, one(1101310), ()),
    Repair("11013.json", 11013, 1101312, -1, one(1101323), ()),
    Repair("11013.json", 11013, 1101313, -1, one(1101312), ()),
    Repair("11013.json", 11013, 1101314, -1, one(1101313), (one(1101331),)),
    Repair("11013.json", 11013, 1101315, -1, one(1101314), ()),
    Repair("11013.json", 11013, 1101316, -1, one(1101315), ()),
    Repair("11013.json", 11013, 1101317, -1, one(1101332), ()),
    Repair("11013.json", 11013, 1101318, -1, one(1101317), ()),
    Repair("11013.json", 11013, 1101319, -1, one(1101336), ()),
    Repair("11013.json", 11013, 1101320, -1, one(1101319), ()),
    Repair("11013.json", 11013, 1101321, -1, one(1101320), ()),
    Repair("11013.json", 11013, 1101322, -1, one(1101321), (one(1101333),)),
    Repair("11013.json", 11013, 1101323, -1, one(1101311), (one(1101330),)),
    Repair("11013.json", 11013, 1101324, -1, one(1101322), (one(1101337),)),
    Repair("11013.json", 11013, 1101325, -1, one(1101335), ()),
    Repair("11013.json", 11013, 1101326, -1, one(1101301), (one(0),)),
    Repair("11013.json", 11013, 1101327, -1, one(1101326), ()),
    Repair("11013.json", 11013, 1101328, -1, one(1101305), (one(1101306),)),
    Repair("11013.json", 11013, 1101329, -1, one(1101307), (one(1101308),)),
    Repair("11013.json", 11013, 1101330, -1, one(1101310), (one(1101311),)),
    Repair("11013.json", 11013, 1101331, -1, one(1101312), (one(1101334),)),
    Repair("11013.json", 11013, 1101332, -1, one(1101316), ()),
    Repair("11013.json", 11013, 1101333, -1, one(1101320), (one(1101321),)),
    Repair("11013.json", 11013, 1101334, -1, one(1101312), (one(1101313),)),
    Repair("11013.json", 11013, 1101335, -1, one(1101324), ()),
    Repair("11013.json", 11013, 1101336, -1, one(1101318), ()),
    Repair("11013.json", 11013, 1101337, -1, one(1101321), (one(1101322),)),

    # MQ11014
    Repair("11014.json", 11014, 1101401, -1, one(1101325), (one(1101421),)),
    Repair("11014.json", 11014, 1101402, -1, one(1101401), ()),
    Repair("11014.json", 11014, 1101403, -1, one(1101418), ()),
    Repair("11014.json", 11014, 1101404, -1, one(1101403), ()),
    Repair("11014.json", 11014, 1101405, -1, one(1101404), ()),
    Repair("11014.json", 11014, 1101406, -1, one(1101416), ()),
    Repair("11014.json", 11014, 1101407, -1, one(1101424), (one(1101426),)),
    Repair("11014.json", 11014, 1101408, -1, one(99902), (one(0),)),
    Repair("11014.json", 11014, 1101409, -1, one(99902), (one(1101408),)),
    Repair("11014.json", 11014, 1101410, -1, one(1101407), ()),
    Repair("11014.json", 11014, 1101411, -1, one(1101405), ()),
    Repair("11014.json", 11014, 1101412, -1, one(1101404), (one(1101411),)),
    Repair("11014.json", 11014, 1101413, -1, one(1101412), ()),
    Repair("11014.json", 11014, 1101414, -1, one(1101404), (one(1101413),)),
    Repair("11014.json", 11014, 1101415, -1, one(1101414), ()),
    Repair("11014.json", 11014, 1101416, -1, one(1101415), ()),
    Repair("11014.json", 11014, 1101417, -1, one(1101402), ()),
    Repair("11014.json", 11014, 1101418, -1, one(1101417), ()),
    Repair("11014.json", 11014, 1101419, -1, one(99902), (one(0),)),
    Repair("11014.json", 11014, 1101420, -1, one(1101325), (one(0),)),
    Repair("11014.json", 11014, 1101421, -1, one(1101420), ()),
    Repair("11014.json", 11014, 1101422, -1, one(1101423), ()),
    Repair("11014.json", 11014, 1101423, -1, one(1101406), ()),
    Repair("11014.json", 11014, 1101424, -1, one(1101422), ()),
    Repair("11014.json", 11014, 1101425, -1, one(1101422), (one(1101424),)),
    Repair("11014.json", 11014, 1101426, -1, one(1101423), (one(1101425),)),

    # MQ11015
    Repair("11015.json", 11015, 1101501, -1, one(1101410), (one(0),)),
    Repair("11015.json", 11015, 1101502, -1, one(1101509), ()),
    Repair("11015.json", 11015, 1101503, -1, one(1101508), ()),
    Repair("11015.json", 11015, 1101504, -1, one(1101503), ()),
    Repair("11015.json", 11015, 1101505, -1, one(1101504), (one(1101511),)),
    Repair("11015.json", 11015, 1101506, -1, one(1101501), ()),
    Repair("11015.json", 11015, 1101507, -1, one(1101501), (one(1101506),)),
    Repair("11015.json", 11015, 1101508, -1, one(1101502), ()),
    Repair("11015.json", 11015, 1101509, -1, one(1101506), (one(1101510),)),
    Repair("11015.json", 11015, 1101510, -1, one(1101501), (one(1101507),)),
    Repair("11015.json", 11015, 1101511, -1, one(1101504), ()),
)

base.REPAIRS += CHAPTER_1205_REPAIRS


if __name__ == "__main__":
    raise SystemExit(base.main())
