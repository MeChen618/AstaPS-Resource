#!/usr/bin/env python3
from __future__ import annotations

import fix_liyue_chapter1102  # noqa: F401 - extends the shared manifest on import
import fix_liyue_prerequisites as base
from fix_quest_prerequisites import Repair, one, state_equal

QUEST_GLOBAL_VAR_EQUAL = "QUEST_COND_QUEST_GLOBAL_VAR_EQUAL"


def quest_global_var_equal(var_id: int, value: int) -> dict:
    return {
        "type": QUEST_GLOBAL_VAR_EQUAL,
        "param": [var_id, value, 0],
        "param_str": "",
    }


# Liyue Chapter 1103 prerequisite repairs.
#
# Evidence:
# - GCResource 3.7 and 4.0 are byte-identical for MQ1020 through MQ1025.
# - Current 7.1 BinOutput has lost the subquest acceptCond graph.
# - The flattened resource synthesizes order-based predecessor edges, corrupting
#   roots, fan-outs, convergence gates, non-state conditions and independent
#   99902 controllers.
CHAPTER_1103_REPAIRS = (
    # MQ1020: Chapter 1103 entry. Historical graph is linear; source still needs
    # full restoration while only the root is semantically wrong after flattening.
    Repair("1020.json", 1020, 102001, -1, one(101610), (one(0),)),
    Repair("1020.json", 1020, 102002, -1, one(102001), (one(102001),)),
    Repair("1020.json", 1020, 102003, -1, one(102002), (one(102002),)),
    Repair("1020.json", 1020, 102007, -1, one(102003), (one(102003),)),
    Repair("1020.json", 1020, 102004, -1, one(102007), (one(102007),)),
    Repair("1020.json", 1020, 102005, -1, one(102004), (one(102004),)),
    Repair("1020.json", 1020, 102006, -1, one(102005), (one(102005),)),

    # MQ1021: three parallel preparations fan out from 102006 and reconverge at
    # 102111. Flattening turns the fan-out into an order chain and drops the
    # three-way AND gate.
    Repair("1021.json", 1021, 102109, -1, one(102006), (one(0),)),
    Repair("1021.json", 1021, 102110, -1, one(102006), (one(102109),)),
    Repair("1021.json", 1021, 102101, -1, one(102006), (one(102110),)),
    Repair("1021.json", 1021, 102102, -1, one(102101), (one(102101),)),
    Repair("1021.json", 1021, 102107, -1, one(102102), (one(102102),)),
    Repair("1021.json", 1021, 102108, -1, one(102107), (one(102107),)),
    Repair(
        "1021.json",
        1021,
        102111,
        -1,
        (state_equal(102109), state_equal(102110), state_equal(102108)),
        (one(102108),),
        expected_comb="LOGIC_AND",
    ),
    Repair("1021.json", 1021, 102103, -1, one(102111), (one(102111),)),
    Repair("1021.json", 1021, 102104, -1, one(102103), (one(102103),)),
    Repair("1021.json", 1021, 102113, -1, one(102104), (one(102104),)),
    Repair("1021.json", 1021, 102105, -1, one(102113), (one(102113),)),
    Repair("1021.json", 1021, 102106, -1, one(102105), (one(102105),)),
    Repair("1021.json", 1021, 102112, -1, one(102106), (one(102106),)),

    # MQ1022: eight-node linear continuation. Flattening preserves the internal
    # predecessor chain but loses the true chapter-to-chapter root edge in QuestExcel,
    # while current BinOutput has no subquest acceptCond at all.
    Repair("1022.json", 1022, 102201, -1, one(102112), (one(0),)),
    Repair("1022.json", 1022, 102202, -1, one(102201), (one(102201),)),
    Repair("1022.json", 1022, 102203, -1, one(102202), (one(102202),)),
    Repair("1022.json", 1022, 102204, -1, one(102203), (one(102203),)),
    Repair("1022.json", 1022, 102205, -1, one(102204), (one(102204),)),
    Repair("1022.json", 1022, 102206, -1, one(102205), (one(102205),)),
    Repair("1022.json", 1022, 102207, -1, one(102206), (one(102206),)),
    Repair("1022.json", 1022, 102208, -1, one(102207), (one(102207),)),

    # MQ1023: dungeon chain followed by two independent hidden controllers.
    # 102306 and 102307 are both historically rooted at 99902 and must not be
    # serialized as continuations of the visible dungeon sequence.
    Repair("1023.json", 1023, 102301, -1, one(102208), (one(0),)),
    Repair("1023.json", 1023, 102303, -1, one(102301), (one(102301),)),
    Repair("1023.json", 1023, 102302, -1, one(102303), (one(102303),)),
    Repair("1023.json", 1023, 102304, -1, one(102302), (one(102302),)),
    Repair("1023.json", 1023, 102305, -1, one(102304), (one(102304),)),
    Repair("1023.json", 1023, 102306, -1, one(99902), (one(102305),)),
    Repair("1023.json", 1023, 102307, -1, one(99902), (one(102306),)),

    # MQ1024: dungeon retry state machine. Two roots are driven by quest-global
    # variable 10009 rather than another subquest, and 102403/102406 are hidden
    # 99902 controllers. The 7.1 source moves those controllers to orders 98/99
    # after losing acceptCond; the historical prerequisite semantics remain clear.
    Repair(
        "1024.json",
        1024,
        102407,
        -1,
        (quest_global_var_equal(10009, 2),),
        (one(0),),
    ),
    Repair("1024.json", 1024, 102408, -1, one(102407), (one(102407),)),
    Repair(
        "1024.json",
        1024,
        102401,
        -1,
        (quest_global_var_equal(10009, 1),),
        (one(102408),),
    ),
    Repair("1024.json", 1024, 102402, -1, one(102401), (one(102401),)),
    Repair("1024.json", 1024, 102404, -1, one(102402), (one(102402),)),
    Repair("1024.json", 1024, 102405, -1, one(102404), (one(102404),)),
    Repair("1024.json", 1024, 102403, -1, one(99902), (one(0),)),
    Repair("1024.json", 1024, 102406, -1, one(99902), (one(102403),)),

    # MQ1025: Chapter 1103 finale. The first six nodes form the entry chain,
    # then 102517 fans out to four preparations. 102512 feeds the visible 102505
    # -> 102506 chain; 102506 then fans out to eight parallel/progress nodes.
    # The final visible handoff is 102514 -> 102510, the chapter endQuestId.
    Repair("1025.json", 1025, 102501, -1, one(102405), (one(0),)),
    Repair("1025.json", 1025, 102516, -1, one(102501), (one(102501),)),
    Repair("1025.json", 1025, 102515, -1, one(102516), (one(102516),)),
    Repair("1025.json", 1025, 102521, -1, one(102515), (one(102515),)),
    Repair("1025.json", 1025, 102502, -1, one(102521), (one(102521),)),
    Repair("1025.json", 1025, 102517, -1, one(102502), (one(102502),)),
    Repair("1025.json", 1025, 102503, -1, one(102517), (one(102517),)),
    Repair("1025.json", 1025, 102504, -1, one(102517), (one(102503),)),
    Repair("1025.json", 1025, 102511, -1, one(102517), (one(102504),)),
    Repair("1025.json", 1025, 102512, -1, one(102517), (one(102511),)),
    Repair("1025.json", 1025, 102505, -1, one(102512), (one(102512),)),
    Repair("1025.json", 1025, 102506, -1, one(102505), (one(102505),)),
    Repair("1025.json", 1025, 102507, -1, one(102506), (one(102506),)),
    Repair("1025.json", 1025, 102508, -1, one(102506), (one(102507),)),
    Repair("1025.json", 1025, 102509, -1, one(102506), (one(102508),)),
    Repair("1025.json", 1025, 102518, -1, one(102506), (one(102509),)),
    Repair("1025.json", 1025, 102519, -1, one(102506), (one(102518),)),
    Repair("1025.json", 1025, 102520, -1, one(102506), (one(102519),)),
    Repair("1025.json", 1025, 102513, -1, one(102506), (one(102520),)),
    Repair("1025.json", 1025, 102514, -1, one(102506), (one(102513),)),
    Repair("1025.json", 1025, 102510, -1, one(102514), (one(102514),)),
)

base.REPAIRS += CHAPTER_1103_REPAIRS


if __name__ == "__main__":
    raise SystemExit(base.main())
