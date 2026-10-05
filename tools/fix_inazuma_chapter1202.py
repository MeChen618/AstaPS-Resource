#!/usr/bin/env python3
from __future__ import annotations

import fix_inazuma_chapter1201  # noqa: F401 - extends the shared manifest on import
import fix_liyue_prerequisites as base
from fix_quest_prerequisites import Repair, one


# Inazuma Chapter 1202 prerequisite repairs.
#
# Evidence:
# - GCResource 3.7 and 4.0 are byte-identical for MQ2011, MQ2012, MQ2013 and MQ2003-MQ2007.
# - Current 7.1 BinOutput keeps the same 77 subquests but has lost acceptCond on all 77.
# - Current flattened QuestExcel keeps 58 historical prerequisite rows intact and damages exactly 19.
CHAPTER_1202_REPAIRS = (
    # MQ2011
    Repair("2011.json", 2011, 201101, -1, one(200212), (one(0),)),
    Repair("2011.json", 2011, 201102, -1, one(201101), ()),
    Repair("2011.json", 2011, 201103, -1, one(201102), ()),
    Repair("2011.json", 2011, 201104, -1, one(201103), ()),
    Repair("2011.json", 2011, 201105, -1, one(201104), ()),
    Repair("2011.json", 2011, 201106, -1, one(201105), ()),
    Repair("2011.json", 2011, 201107, -1, one(201106), ()),

    # MQ2012
    Repair("2012.json", 2012, 201201, -1, one(201107), (one(0),)),
    Repair("2012.json", 2012, 201202, -1, one(201201), ()),
    Repair("2012.json", 2012, 201203, -1, one(201202), ()),
    Repair("2012.json", 2012, 201204, -1, one(201203), ()),
    Repair("2012.json", 2012, 201205, -1, one(201204), ()),
    Repair("2012.json", 2012, 201206, -1, one(201205), ()),
    Repair("2012.json", 2012, 201207, -1, one(201212), ()),
    Repair("2012.json", 2012, 201208, -1, one(201213), ()),
    Repair("2012.json", 2012, 201209, -1, one(201214), ()),
    Repair("2012.json", 2012, 201210, -1, one(201206), ()),
    Repair("2012.json", 2012, 201211, -1, one(201210), ()),
    Repair("2012.json", 2012, 201212, -1, one(201217), ()),
    Repair("2012.json", 2012, 201213, -1, one(201207), ()),
    Repair("2012.json", 2012, 201214, -1, one(201208), ()),
    Repair("2012.json", 2012, 201215, -1, one(201209), ()),
    Repair("2012.json", 2012, 201216, -1, one(201211), ()),
    Repair("2012.json", 2012, 201217, -1, one(201216), ()),

    # MQ2013
    Repair("2013.json", 2013, 201301, -1, one(201215), (one(0),)),
    Repair("2013.json", 2013, 201302, -1, one(201311), ()),
    Repair("2013.json", 2013, 201303, -1, one(201302), ()),
    Repair("2013.json", 2013, 201304, -1, one(201303), ()),
    Repair("2013.json", 2013, 201305, -1, one(99902), (one(201304),)),
    Repair("2013.json", 2013, 201306, -1, one(201304), (one(201305),)),
    Repair("2013.json", 2013, 201307, -1, one(201306), ()),
    Repair("2013.json", 2013, 201308, -1, one(201307), ()),
    Repair("2013.json", 2013, 201309, -1, one(201308), ()),
    Repair("2013.json", 2013, 201310, -1, one(201309), (one(201312),)),
    Repair("2013.json", 2013, 201311, -1, one(201301), ()),
    Repair("2013.json", 2013, 201312, -1, one(201309, state=4), (one(201309),)),

    # MQ2003
    Repair("2003.json", 2003, 200301, -1, one(200305), ()),
    Repair("2003.json", 2003, 200302, -1, one(200301), ()),
    Repair("2003.json", 2003, 200303, -1, one(99902), (one(200302),)),
    Repair("2003.json", 2003, 200304, -1, one(200302), (one(200303),)),
    Repair("2003.json", 2003, 200305, -1, one(201310), (one(0),)),

    # MQ2004
    Repair("2004.json", 2004, 200401, -1, one(200304), (one(0),)),
    Repair("2004.json", 2004, 200402, -1, one(200408), ()),
    Repair("2004.json", 2004, 200403, -1, one(200402), ()),
    Repair("2004.json", 2004, 200404, -1, one(200403), ()),
    Repair("2004.json", 2004, 200405, -1, one(200404), ()),
    Repair("2004.json", 2004, 200406, -1, one(200401), ()),
    Repair("2004.json", 2004, 200407, -1, one(200401), (one(200406),)),
    Repair(
        "2004.json",
        2004,
        200408,
        -1,
        one(200407) + one(200406),
        (one(200407),),
        expected_comb="LOGIC_AND",
    ),

    # MQ2005
    Repair("2005.json", 2005, 200501, -1, one(200405), (one(0),)),
    Repair("2005.json", 2005, 200502, -1, one(200507), ()),
    Repair("2005.json", 2005, 200503, -1, one(200502), ()),
    Repair("2005.json", 2005, 200504, -1, one(200503), ()),
    Repair("2005.json", 2005, 200505, -1, one(200504), ()),
    Repair("2005.json", 2005, 200506, -1, one(200501), ()),
    Repair("2005.json", 2005, 200507, -1, one(200506), ()),

    # MQ2006
    Repair("2006.json", 2006, 200601, -1, one(200505), (one(0),)),
    Repair("2006.json", 2006, 200602, -1, one(200601), ()),
    Repair("2006.json", 2006, 200603, -1, one(200602), ()),
    Repair("2006.json", 2006, 200604, -1, one(200609), ()),
    Repair("2006.json", 2006, 200605, -1, one(200604), ()),
    Repair("2006.json", 2006, 200606, -1, one(200605), ()),
    Repair("2006.json", 2006, 200607, -1, one(200606), ()),
    Repair("2006.json", 2006, 200608, -1, one(200603), ()),
    Repair("2006.json", 2006, 200609, -1, one(200608), ()),
    Repair("2006.json", 2006, 200610, -1, one(99902), (one(200607),)),

    # MQ2007
    Repair("2007.json", 2007, 200701, -1, one(200607), (one(0),)),
    Repair("2007.json", 2007, 200702, -1, one(200710), ()),
    Repair("2007.json", 2007, 200703, -1, one(200702), ()),
    Repair("2007.json", 2007, 200704, -1, one(200703), ()),
    Repair("2007.json", 2007, 200705, -1, one(200706), ()),
    Repair("2007.json", 2007, 200706, -1, one(200704), ()),
    Repair("2007.json", 2007, 200707, -1, one(200709), ()),
    Repair("2007.json", 2007, 200708, -1, one(99902), (one(200711),)),
    Repair("2007.json", 2007, 200709, -1, one(200705), ()),
    Repair("2007.json", 2007, 200710, -1, one(200701), ()),
    Repair("2007.json", 2007, 200711, -1, one(200709), (one(200707),)),
)

base.REPAIRS += CHAPTER_1202_REPAIRS


if __name__ == "__main__":
    raise SystemExit(base.main())
