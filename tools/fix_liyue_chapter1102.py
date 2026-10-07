#!/usr/bin/env python3
from __future__ import annotations

import fix_liyue_act1_branches  # noqa: F401 - extends the shared manifest on import
import fix_liyue_prerequisites as base
from fix_quest_prerequisites import Repair, one, state_equal

# Chapter 1102 finale.
#
# Evidence:
# - GCResource 3.7 and 4.0 are byte-identical for MQ1015 and MQ1016.
# - Current 7.1 BinOutput has lost the subquest acceptCond graph.
# - The flattened resource synthesizes order-based predecessor edges, which hides
#   the loss on linear rows and corrupts independent / compound controller rows.
#
# Running this script also applies every prerequisite repair imported by
# fix_liyue_act1_branches, so it is the single entry point for the audited early
# Liyue batch through the end of Chapter 1102.
CHAPTER_1102_FINALE_REPAIRS = (
    # MQ1015: production sequence after the bargaining finale.
    # 101516 is an independent hidden controller rooted at 99902 and shares
    # order=3 with 101509; the current flattened resource serializes it as [0,3].
    Repair("1015.json", 1015, 101501, -1, one(101320), (one(0),)),
    Repair("1015.json", 1015, 101513, -1, one(101501), (one(101501),)),
    Repair("1015.json", 1015, 101516, -1, one(99902), (one(0),)),
    Repair("1015.json", 1015, 101509, -1, one(101513), (one(101516),)),
    Repair("1015.json", 1015, 101502, -1, one(101509), (one(101509),)),
    Repair("1015.json", 1015, 101508, -1, one(101502), (one(101502),)),
    Repair("1015.json", 1015, 101503, -1, one(101508), (one(101508),)),
    Repair("1015.json", 1015, 101504, -1, one(101503), (one(101503),)),
    Repair("1015.json", 1015, 101505, -1, one(101504), (one(101504),)),
    Repair("1015.json", 1015, 101506, -1, one(101505), (one(101505),)),
    Repair("1015.json", 1015, 101515, -1, one(101506), (one(101506),)),
    Repair("1015.json", 1015, 101510, -1, one(101515), (one(101515),)),
    Repair("1015.json", 1015, 101514, -1, one(101510), (one(101510),)),
    Repair("1015.json", 1015, 101507, -1, one(101514), (one(101514),)),
    Repair("1015.json", 1015, 101511, -1, one(101507), (one(101507),)),
    Repair("1015.json", 1015, 101512, -1, one(101511), (one(101511),)),

    # MQ1016: Chapter 1102 conclusion.
    # 101601 accepts either FINISHED or FAILED state of 101605. 101602 and
    # 101603 are independent 99902-rooted hidden controllers. 101606 is a
    # sibling of 101609, both fanning out from 101608.
    Repair("1016.json", 1016, 101604, -1, one(101512), (one(0),)),
    Repair("1016.json", 1016, 101605, -1, one(101604), (one(101604),)),
    Repair(
        "1016.json",
        1016,
        101601,
        -1,
        (state_equal(101605), state_equal(101605, state=4)),
        (one(101605),),
        expected_comb="LOGIC_OR",
    ),
    Repair("1016.json", 1016, 101608, -1, one(101601), (one(101601),)),
    Repair("1016.json", 1016, 101609, -1, one(101608), (one(101608),)),
    Repair("1016.json", 1016, 101606, -1, one(101608), (one(101609),)),
    Repair("1016.json", 1016, 101607, -1, one(101606), (one(101606),)),
    Repair("1016.json", 1016, 101602, -1, one(99902), (one(101607),)),
    Repair("1016.json", 1016, 101603, -1, one(99902), (one(101602),)),
    Repair("1016.json", 1016, 101610, -1, one(101609), (one(101603),)),
)

base.REPAIRS += CHAPTER_1102_FINALE_REPAIRS


if __name__ == "__main__":
    raise SystemExit(base.main())
