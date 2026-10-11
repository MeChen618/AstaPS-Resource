# Fontaine weapon-domain starter-key compatibility (7.1)

The pinned 7.1 resource pack has a valid `scene40770.lua` through
`scene40773.lua`, each referencing a block that was absent from the pack.
Consequently, entering dungeon 4473 reported missing
`scene40773_block40773.lua`, no combat/reward groups, and no starter key.

These **synthetic compatibility** scripts provide the minimal block and groups
expected by AstaPS `MissingDomainFallbackManager` for scenes 40770–40773:
combat group `24077N001`, reward group `24077N004`, starter key config
`9001` (gadget 70360010, worktop option 7), and reward configs `5001` (gadget 70340012) and `5002` (gadget 70350008). Monster configs correspond to the Java fallback waves.
These scripts are **not native 7.1 group reconstructions**. Combat monsters,
their positions and levels are compatibility substitutes.

The server-side default challenge and reward logic remains authoritative.
A complete test must verify scene script loading, worktop interaction, both
combat waves, success settlement, the reward gadget, and resin deduction.
Run `python scripts/validate_fontaine_weapon_domains.py` for static checks.

Deploy only under `resources/Scripts/Scene/{40770..40773}` from this
resource branch alongside the AstaPS test build. Restart the server so its
Lua group/block metadata is reloaded.

## Visible challenge-key prefab

The first compatibility pass used gadget 70350096 at (0, 0.15, 4). Server logs
confirmed entity creation and option 7, but client users reported no visible key
or monsters. The known-working domain 40501 uses 70360010 at approximately
(0, 0, 0), so compatibility keys now use the same worktop prefab and location.
This is a targeted compatibility hypothesis pending client confirmation;
server-side presence alone is insufficient to prove client visibility.

## Reward fixture alignment

The first compatibility fixture copied scene 40501's layout at z≈-70.
In scene 40773 (dungeon 4473), the client had no accessible claim button
because the fixture was misplaced. Once its 70340012 base was placed near
the actual finish, the user confirmed both UI opening and successful drops.
The server log showed `GadgetRewardStatue open UI` and
`StatueDrop ok uid=... dungeon=4473 ...`.

Comparing native scene 40650 and 40801 revealed the same born/reborn
positions, starter key, and reward fixture. All four Fontaine weapon
scenes (40770–40773) have closely matching born/reborn positions.
The synthetic reward groups now reuse this **native reference** layout:

- config 5001, gadget 70340012: `(0.016, -0.438, -40.416)`
- config 5002, gadget 70350008: `(0.000, 2.394, -35.712)`
- reward group anchor: `(-3.074, 1.574, -35.813)`
- on successful `EVENT_DUNGEON_SETTLE`, activate config 5001 only.

In these four scenes, the server handles 70340012 as the resin claim
target and leaves 70350008 as a noninteractive accompanying prop.
The native 40650 scripts are the coordinate reference, not a claim
that original 4077x reward-group scripts were recovered.

**Client-verified:** dungeons 4470–4473 complete their challenges,
open the resin claim interface and grant rewards. The 4470–4472
verification used the same reference fixture as the 4473 test.
This does not validate native item drop rates or the dungeon-reentry
lifecycle; 4471 produced a transient missing-gadget observation during
a repeated entry but subsequently recovered and completed.
