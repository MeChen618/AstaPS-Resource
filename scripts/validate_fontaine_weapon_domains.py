#!/usr/bin/env python3
"""Static structural check for Fontaine weapon-domain compatibility Lua scripts.

No Lua VM dependency; checks only explicit contract with MissingDomainFallbackManager.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1] / "Scripts" / "Scene"
WAVE_IDS = {
    40770: (1001, 1002, 1003, 1004, 1005, 1006),
    40771: (1001, 1002, 1003, 1004, 1005, 1006, 1007),
    40772: (1001, 1002, 1003, 1004, 1005),
    40773: (1001, 1002, 1003, 1004, 1005),
}

def check():
    for scene, expected in WAVE_IDS.items():
        directory = ROOT / str(scene)
        combat_group = 240000000 + (scene - 40000) * 1000 + 1
        reward_group = combat_group + 3
        src = (directory / f"scene{scene}.lua").read_text(encoding="utf-8")
        assert re.search(rf"blocks\s*=\s*\{{\s*{scene}\s*\}}", src), scene
        block = (directory / f"scene{scene}_block{scene}.lua").read_text(encoding="utf-8")
        assert set(map(int,re.findall(r"\bid\s*=\s*(240\d{6})",block))) == {
            combat_group, reward_group
        }, scene
        combat = (directory / f"scene{scene}_group{combat_group}.lua").read_text(encoding="utf-8")
        reward = (directory / f"scene{scene}_group{reward_group}.lua").read_text(encoding="utf-8")
        for text,gid in ((combat,combat_group),(reward,reward_group)):
            assert f"group_id = {gid}" in text
            assert "init_config" in text and "suites" in text
        assert re.search(r"config_id\s*=\s*9001,\s*gadget_id\s*=\s*70360010",combat),scene
        monster_definitions = combat.split("npcs = {}")[0]
        actual=tuple(map(int,re.findall(r"config_id\s*=\s*(\d+),\s*monster_id",monster_definitions)))
        assert actual == expected,(scene,actual,expected)
        assert re.search(r"monsters\s*=\s*\{\s*\},\s*gadgets\s*=\s*\{\s*9001\s*\}",combat),scene
        # Require the native two-piece layout (reward base + generic accessory).
        # These scenes have no native groups. Reuse the 40650 reference layout.
        assert re.search(r"config_id\s*=\s*5001,\s*gadget_id\s*=\s*70340012",reward),scene
        assert re.search(r"config_id\s*=\s*5002,\s*gadget_id\s*=\s*70350008",reward),scene
        assert "gadgets = {5001, 5002}" in reward, scene
        # All four synthetic scenes share the native 40650/40801 reward layout.
        # All 4470-4473 claims were client-verified; exact native drop rates remain unknown.
        assert re.search(r"config_id\s*=\s*5001[^\n]*x\s*=\s*0\.016,\s*y\s*=\s*-0\.438,\s*z\s*=\s*-40\.416", reward), scene
        assert re.search(r"config_id\s*=\s*5002[^\n]*x\s*=\s*0\.000,\s*y\s*=\s*2\.394,\s*z\s*=\s*-35\.712", reward), scene
        assert re.search(rf"id\s*=\s*{reward_group}[^\n]*x\s*=\s*-3\.074,\s*y\s*=\s*1\.574,\s*z\s*=\s*-35\.813", block), scene
        assert "DUNGEON_SETTLE_5003" in reward, scene
        assert "event = EventType.EVENT_DUNGEON_SETTLE" in reward, scene
        assert re.search(
            r"function condition_EVENT_DUNGEON_SETTLE_5003\(context, evt\)\s*"
            r"return evt\.param1 == 1\s*end", reward
        ), scene
        assert reward.count(
            "ScriptLib.SetGadgetStateByConfigId(context, 5001, GadgetState.StatueActive)"
        ) == 1, scene
        # The accompanying prop must never become a second claim target.
        assert "SetGadgetStateByConfigId(context, 5002" not in reward, scene
        assert re.search(r"config_id\s*=\s*9001,\s*gadget_id\s*=\s*70360010,\s*pos\s*=\s*\{\s*x\s*=\s*0\.000,\s*y\s*=\s*0\.000,\s*z\s*=\s*0\.000",combat),scene
        print(f"OK {scene}: key=9001, worktop=70360010, waves={len(actual)}, reward=5001+5002")
if __name__=="__main__":
    check()
