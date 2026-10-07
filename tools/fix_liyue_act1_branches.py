#!/usr/bin/env python3
from __future__ import annotations

import fix_liyue_prerequisites as base
from fix_quest_prerequisites import Repair, one, state_equal

# Early Liyue branch / convergence repairs through Chapter 1102.
#
# Evidence:
# - GCResource 3.7 and 4.0 agree on these prerequisite graphs.
# - Current 7.1 BinOutput has lost acceptCond on the corresponding subquests.
# - The flattened resource collapses fan-outs and compound gates into order chains.
#
# Importing the base module makes this script apply the already-audited
# 400 -> MQ1000 -> MQ1002 -> MQ1003 repairs in the same pass.
BRANCH_REPAIRS = (
    # MQ1008: 100801/100802/100803 fan out from 100808.
    Repair("1008.json", 1008, 100808, -1, one(100205), (one(0),)),
    Repair("1008.json", 1008, 100801, -1, one(100808), (one(100808),)),
    Repair("1008.json", 1008, 100802, -1, one(100808), (one(100801),)),
    Repair("1008.json", 1008, 100803, -1, one(100808), (one(100802),)),
    Repair(
        "1008.json",
        1008,
        100804,
        -1,
        (state_equal(100802), state_equal(100803, state=2)),
        (one(100803),),
        expected_comb="LOGIC_AND",
    ),
    Repair(
        "1008.json",
        1008,
        100805,
        -1,
        (state_equal(100803), state_equal(100804)),
        (one(100804),),
        expected_comb="LOGIC_OR",
    ),
    Repair("1008.json", 1008, 100806, -1, one(100805), (one(100805),)),
    Repair("1008.json", 1008, 100807, -1, one(100806), (one(100806),)),

    # MQ1009: fan out from 100915, then again from 100906.
    Repair("1009.json", 1009, 100901, -1, one(100205), (one(0),)),
    Repair("1009.json", 1009, 100915, -1, one(100901), (one(100901),)),
    Repair("1009.json", 1009, 100902, -1, one(100915), (one(100915),)),
    Repair("1009.json", 1009, 100903, -1, one(100915), (one(100902),)),
    Repair("1009.json", 1009, 100904, -1, one(100915), (one(100903),)),
    Repair("1009.json", 1009, 100905, -1, one(100915), (one(100904),)),
    Repair("1009.json", 1009, 100906, -1, one(100915), (one(100905),)),
    Repair("1009.json", 1009, 100907, -1, one(100906), (one(100906),)),
    Repair("1009.json", 1009, 100908, -1, one(100906), (one(100907),)),
    Repair("1009.json", 1009, 100909, -1, one(100906), (one(100908),)),
    Repair("1009.json", 1009, 100910, -1, one(100906), (one(100909),)),
    Repair("1009.json", 1009, 100911, -1, one(100906), (one(100910),)),
    Repair("1009.json", 1009, 100912, -1, one(100911), (one(100911),)),
    Repair("1009.json", 1009, 100913, -1, one(99902), (one(100912),)),
    Repair("1009.json", 1009, 100914, -1, one(100912), (one(100913),)),

    # MQ1018: convergence gate for all three investigation branches.
    Repair(
        "1018.json",
        1018,
        101801,
        -1,
        (state_equal(100317), state_equal(100807), state_equal(100914)),
        (one(0),),
        expected_comb="LOGIC_AND",
    ),

    # MQ1010: Chapter 1102 entry after the three-branch convergence.
    # 101004 is an independent hidden controller rooted at 99902; the flattened
    # order chain incorrectly makes 101007 depend on it.
    Repair("1010.json", 1010, 101001, -1, one(101801), (one(0),)),
    Repair("1010.json", 1010, 101002, -1, one(101001), (one(101001),)),
    Repair("1010.json", 1010, 101003, -1, one(101002), (one(101002),)),
    Repair("1010.json", 1010, 101004, -1, one(99902), (one(101003),)),
    Repair("1010.json", 1010, 101007, -1, one(101003), (one(101004),)),
    Repair("1010.json", 1010, 101008, -1, one(101007), (one(101007),)),
    Repair("1010.json", 1010, 101005, -1, one(101008), (one(101008),)),
    Repair("1010.json", 1010, 101006, -1, one(101005), (one(101005),)),

    # MQ1011: Chapter 1102 incense / cleansing sequence.
    # 101127 is a hidden progress controller. Many sibling steps require both a
    # concrete predecessor to be FINISHED and 101127 to remain ACTIVE (state 2).
    Repair("1011.json", 1011, 101101, -1, one(101006), (one(0),)),
    Repair("1011.json", 1011, 101116, -1, one(101101), (one(101101),)),
    Repair("1011.json", 1011, 101102, -1, one(101101), (one(101116),)),
    Repair("1011.json", 1011, 101103, -1, one(101102), (one(101102),)),
    Repair("1011.json", 1011, 101112, -1, one(101103), (one(101103),)),
    Repair("1011.json", 1011, 101104, -1, one(101112), (one(101112),)),
    Repair("1011.json", 1011, 101128, -1, one(101112), (one(101104),)),
    Repair(
        "1011.json",
        1011,
        101105,
        -1,
        (state_equal(101104), state_equal(101127, state=2)),
        (one(101128),),
        expected_comb="LOGIC_AND",
    ),
    Repair(
        "1011.json",
        1011,
        101123,
        -1,
        (state_equal(101104), state_equal(101127, state=2)),
        (one(101105),),
        expected_comb="LOGIC_AND",
    ),
    Repair(
        "1011.json",
        1011,
        101113,
        -1,
        (state_equal(101123), state_equal(101127, state=2)),
        (one(101123),),
        expected_comb="LOGIC_AND",
    ),
    Repair(
        "1011.json",
        1011,
        101124,
        -1,
        (state_equal(101104), state_equal(101127, state=2)),
        (one(101113),),
        expected_comb="LOGIC_AND",
    ),
    Repair(
        "1011.json",
        1011,
        101114,
        -1,
        (state_equal(101124), state_equal(101127, state=2)),
        (one(101124),),
        expected_comb="LOGIC_AND",
    ),
    Repair(
        "1011.json",
        1011,
        101125,
        -1,
        (state_equal(101104), state_equal(101127, state=2)),
        (one(101114),),
        expected_comb="LOGIC_AND",
    ),
    Repair(
        "1011.json",
        1011,
        101115,
        -1,
        (state_equal(101125), state_equal(101127, state=2)),
        (one(101125),),
        expected_comb="LOGIC_AND",
    ),
    Repair(
        "1011.json",
        1011,
        101126,
        -1,
        (state_equal(101104), state_equal(101127, state=2)),
        (one(101115),),
        expected_comb="LOGIC_AND",
    ),
    Repair(
        "1011.json",
        1011,
        101106,
        -1,
        (state_equal(101126), state_equal(101127, state=2)),
        (one(101126),),
        expected_comb="LOGIC_AND",
    ),
    Repair("1011.json", 1011, 101127, -1, one(101104), (one(101106),)),
    Repair("1011.json", 1011, 101110, -1, one(101127), (one(101127),)),
    Repair("1011.json", 1011, 101111, -1, one(101127), (one(101110),)),
    Repair("1011.json", 1011, 101107, -1, one(101127), (one(101111),)),
    Repair("1011.json", 1011, 101108, -1, one(101107), (one(101107),)),
    Repair("1011.json", 1011, 101109, -1, one(101108), (one(101108),)),

    # MQ1012: Chapter 1102 purchase / collection sequence.
    # Orders 9-13 are five siblings that all fan out from 101214. The flattened
    # order chain incorrectly serializes them as a linear collection sequence.
    Repair("1012.json", 1012, 101202, -1, one(101109), (one(0),)),
    Repair("1012.json", 1012, 101212, -1, one(101202), (one(101202),)),
    Repair("1012.json", 1012, 101203, -1, one(101212), (one(101212),)),
    Repair("1012.json", 1012, 101204, -1, one(101203), (one(101203),)),
    Repair("1012.json", 1012, 101205, -1, one(101204), (one(101204),)),
    Repair("1012.json", 1012, 101213, -1, one(101205), (one(101205),)),
    Repair("1012.json", 1012, 101206, -1, one(101213), (one(101213),)),
    Repair("1012.json", 1012, 101214, -1, one(101206), (one(101206),)),
    Repair("1012.json", 1012, 101210, -1, one(101214), (one(101214),)),
    Repair("1012.json", 1012, 101211, -1, one(101214), (one(101210),)),
    Repair("1012.json", 1012, 101207, -1, one(101214), (one(101211),)),
    Repair("1012.json", 1012, 101208, -1, one(101214), (one(101207),)),
    Repair("1012.json", 1012, 101201, -1, one(101214), (one(101208),)),
    Repair("1012.json", 1012, 101215, -1, one(101210), (one(101201),)),
    Repair("1012.json", 1012, 101209, -1, one(101215), (one(101215),)),

    # MQ1014: Chapter 1102 dungeon sequence. This graph is linear, but source
    # acceptCond was still lost wholesale; only the root is visibly wrong after
    # flattening because later synthetic order edges happen to match history.
    Repair("1014.json", 1014, 101401, -1, one(101209), (one(0),)),
    Repair("1014.json", 1014, 101406, -1, one(101401), (one(101401),)),
    Repair("1014.json", 1014, 101402, -1, one(101406), (one(101406),)),
    Repair("1014.json", 1014, 101405, -1, one(101402), (one(101402),)),
    Repair("1014.json", 1014, 101408, -1, one(101405), (one(101405),)),
    Repair("1014.json", 1014, 101403, -1, one(101408), (one(101408),)),
    Repair("1014.json", 1014, 101404, -1, one(101403), (one(101403),)),
    Repair("1014.json", 1014, 101407, -1, one(101404), (one(101404),)),

    # MQ1013: Chapter 1102 bargaining finale. Three bargaining branches fan out
    # from 101301. Failed/finished state=4 gates and OR recovery controllers are
    # semantically significant and must survive flattening exactly.
    Repair("1013.json", 1013, 101301, -1, one(101407), (one(0),)),
    Repair("1013.json", 1013, 101302, -1, one(99902), (one(101301),)),
    Repair("1013.json", 1013, 101303, -1, one(101301), (one(101302),)),
    Repair("1013.json", 1013, 101321, -1, one(101301), (one(101303),)),
    Repair("1013.json", 1013, 101304, -1, one(101303, state=4), (one(101321),)),
    Repair("1013.json", 1013, 101305, -1, one(101304, state=4), (one(101304),)),
    Repair("1013.json", 1013, 101306, -1, one(101305), (one(101305),)),
    Repair("1013.json", 1013, 101307, -1, one(101301), (one(101306),)),
    Repair("1013.json", 1013, 101322, -1, one(101301), (one(101307),)),
    Repair("1013.json", 1013, 101308, -1, one(101307, state=4), (one(101322),)),
    Repair("1013.json", 1013, 101309, -1, one(101308, state=4), (one(101308),)),
    Repair("1013.json", 1013, 101310, -1, one(101309), (one(101309),)),
    Repair("1013.json", 1013, 101311, -1, one(101301), (one(101310),)),
    Repair("1013.json", 1013, 101323, -1, one(101301), (one(101311),)),
    Repair("1013.json", 1013, 101312, -1, one(101311, state=4), (one(101323),)),
    Repair("1013.json", 1013, 101313, -1, one(101312, state=4), (one(101312),)),
    Repair("1013.json", 1013, 101314, -1, one(101313), (one(101313),)),
    Repair("1013.json", 1013, 101315, -1, one(101301), (one(101314),)),
    Repair("1013.json", 1013, 101316, -1, one(101301), (one(101315),)),
    Repair(
        "1013.json",
        1013,
        101317,
        -1,
        (state_equal(101303), state_equal(101303, state=4)),
        (one(101316),),
        expected_comb="LOGIC_OR",
    ),
    Repair(
        "1013.json",
        1013,
        101318,
        -1,
        (state_equal(101307), state_equal(101307, state=4)),
        (one(101317),),
        expected_comb="LOGIC_OR",
    ),
    Repair(
        "1013.json",
        1013,
        101319,
        -1,
        (state_equal(101311), state_equal(101311, state=4)),
        (one(101318),),
        expected_comb="LOGIC_OR",
    ),
    Repair("1013.json", 1013, 101320, -1, one(101316), (one(101319),)),
)

base.REPAIRS += BRANCH_REPAIRS


if __name__ == "__main__":
    raise SystemExit(base.main())
