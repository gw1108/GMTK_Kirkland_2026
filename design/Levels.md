# Level Pacing and Wave Schedule

This file defines the first-pass pacing for all 13 levels. Enemy eligibility and ordinary spawn weights come from [Enemies.md](Enemies.md). Every scalar in this file must be authored in `game/data/balance.csv`; these values are initial balance targets rather than GDScript constants.

## Arena environments and entrances

Each level uses a different Epic/ERW environment pack. Build its Godot TileSet from the matching `.tsx` geometry and terrain definitions in `SourceArt/_catalog/TILED_INDEX.md`, and use that pack's indexed `.tmx` example maps as layout references.

Entrance weights divide ordinary spawns and event-wave slots among the active screen edges. All entrances spawn enemies just beyond the arena boundary. Levels 10–13 necessarily use all four edges, so their dominant edge and secondary weighting rotate to keep consecutive levels from feeling identical.

| Level | Environment pack | Active entrance weights | Layout profile |
| --- | --- | --- | --- |
| 1 | `EPIC RPG World Pack - Grass Land V. 1.6` | East 100% | One broad eastern approach with two wide defensive chokepoints before the wizard clearing. |
| 2 | `Epic RPG World - The Village V2.0` | North 100% | Broad village streets create two readable approach lanes that merge near the wizard. |
| 3 | `ERW - Grass Land 2.0 v2.1` | West 50%, East 50% | Mostly open field with sparse fences and two broad opposing lanes. |
| 4 | `ERW - Sea Adventures (GL 2.0 expansion) V1.4.2` | North 50%, South 50% | Open shore and dock space with impassable water shaping two wide routes. |
| 5 | `Epic RPG World - Highlands V1.4.1` | North 50%, East 50% | Open plateau with sparse cliff and fortress pieces creating partial cover rather than narrow funnels. |
| 6 | `Epic RPG World - Desert V1.6` | North 34%, East 33%, West 33% | Open sand with scattered impassable rocks and oasis water; all three approaches remain wide. |
| 7 | `Epic RPG World - The dephs of the Mountain V1.5.1` | North 34%, East 33%, South 33% | Broad central basin with rock walls producing a few optional side chokepoints. |
| 8 | `ERW - Ancient Ruins V 2.3` | East 34%, South 33%, West 33% | Open ruins with broken walls and pillars that split movement briefly without creating tight corridors. |
| 9 | `EPIC RPG World - Sewers V1.5` | North 34%, South 33%, West 33% | Large open sewer floor with water channels and walls used as impassable boundaries. |
| 10 | `EPIC RPG World Pack - Old Prison V1.7.1` | North 35%, East 25%, South 20%, West 20% | Open prison yard; cell walls and structures remain primarily around the perimeter. |
| 11 | `EPIC RPG World Pack - Cemetery V 1.6` | North 20%, East 35%, South 25%, West 20% | Open graveyard with spaced grave and fence clusters forming broad lanes. |
| 12 | `EPIC RPG World Pack - Crypt V.1.6` | North 20%, East 20%, South 35%, West 25% | Open crypt chamber with sparse pillars and wall fragments; no narrow corridors around the wizard. |
| 13 | `Epic RPG World - Volcano V1.6` | North 25%, East 20%, South 20%, West 35% | Very open final arena with impassable lava rivers and cliffs separated by several wide crossings. |

## Wave terminology

- **Enemy minimum:** The spawner fills toward this many living standard enemies. Bosses do not count toward this minimum. Killing a standard enemy allows the spawner to replace it while the living count is below the active minimum.
- **Event wave:** A one-time burst added on top of continuous minimum-based spawning. Event-wave enemies may temporarily push the living count above the minimum. Burst enemies enter through the active entrances at the normal 0.25-second spawn interval rather than appearing in one frame.
- **Strong enemy:** The level-specific enemy listed below. When multiple strong enemies are listed, divide the requested strong-enemy count as evenly as possible between them.
- **Mixed enemy:** Draw from the level's ordinary spawn weights in [Enemies.md](Enemies.md).
- **Break:** No event burst occurs and the enemy minimum drops. Existing enemies are not despawned.
- **Boss support minimum:** The enemy minimum applied when the boss encounter begins. Existing enemies are not despawned if the living count is already above it.

The standard spawn interval remains 0.25 seconds while the spawner is filling toward its current minimum.

## Strong-enemy assignments

| Level | Strong enemy selection |
| --- | --- |
| 1 | Hostile Warrior |
| 2 | Hostile Warrior and Orc Warrior |
| 3 | Orc Warrior |
| 4 | Sea Raider |
| 5 | Troll |
| 6 | Sandworm |
| 7 | Mountain Enemy 2 |
| 8 | Mountain Enemy 2 and Orc Warrior |
| 9 | Mutant Rat |
| 10 | Prison Assassin and Prison Skeleton |
| 11 | Undead |
| 12 | Big Worm 2 |
| 13 | Rocky Dude and Big Worm 2 |

## Event-wave rules

All counts are per level `L`.

| Time | Phase | Event burst |
| --- | --- | --- |
| 0:00 | Small opening | No burst. |
| 0:15 | Early rise | No burst. |
| 0:30 | Strong-enemy warning | Spawn `1 + floor(L / 3)` strong enemies. |
| 0:45 | Pre-horde rise | No burst. |
| 1:00 | Horde | Spawn `10 + 2L` mixed enemies. Replace `floor(L / 4)` of those selections with strong enemies. |
| 1:15 | Break | No burst. |
| 1:30 | Major challenge | Spawn `2 + ceil(L / 2)` strong enemies and `8 + L` mixed enemies. |
| 1:45 | Break | No burst. |
| 2:00 | Major challenge | Spawn `3 + ceil(L / 2)` strong enemies and `10 + L` mixed enemies. |
| 2:15 | Break | No burst. |
| 2:30 | Major challenge | Spawn `4 + ceil(L / 2)` strong enemies and `12 + L` mixed enemies. |

Only events at least 10 seconds earlier than the level's boss time occur. This safety window allows the queued burst to enter before the boss arrives. Level 1 has no boss, so its 1:00 Horde is its final event before the ritual completes at 1:10.

## Enemy-minimum curves

A dash means the boss has already spawned or the ritual has already ended, so that phase does not occur. The final two columns give the exact boss spawn time and the lower support minimum that becomes active at that moment.

| Level | Duration | 0:00 | 0:15 | 0:30 | 0:45 | 1:00 | 1:15 break | 1:30 challenge | 1:45 break | 2:00 challenge | 2:15 break | 2:30 challenge | Boss time | Boss support minimum |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 1:10 | 8 | 12 | 14 | 18 | 31 | — | — | — | — | — | — | — | — |
| 2 | 1:20 | 10 | 14 | 16 | 20 | — | — | — | — | — | — | — | 0:55 | 16 |
| 3 | 1:30 | 12 | 16 | 18 | 22 | — | — | — | — | — | — | — | 1:04 | 18 |
| 4 | 1:40 | 14 | 18 | 20 | 24 | 40 | — | — | — | — | — | — | 1:13 | 20 |
| 5 | 1:50 | 16 | 20 | 22 | 26 | 43 | — | — | — | — | — | — | 1:22 | 22 |
| 6 | 2:00 | 18 | 22 | 24 | 28 | 46 | 26 | — | — | — | — | — | 1:31 | 24 |
| 7 | 2:10 | 20 | 24 | 26 | 30 | 49 | 28 | 53 | — | — | — | — | 1:40 | 26 |
| 8 | 2:20 | 22 | 26 | 28 | 32 | 52 | 30 | 56 | — | — | — | — | 1:50 | 28 |
| 9 | 2:30 | 24 | 28 | 30 | 34 | 55 | 32 | 59 | 34 | — | — | — | 1:59 | 30 |
| 10 | 2:40 | 26 | 30 | 32 | 36 | 58 | 34 | 62 | 36 | — | — | — | 2:08 | 32 |
| 11 | 2:50 | 28 | 32 | 34 | 38 | 61 | 36 | 65 | 38 | 69 | — | — | 2:17 | 34 |
| 12 | 3:00 | 30 | 34 | 36 | 40 | 64 | 38 | 68 | 40 | 72 | 42 | — | 2:26 | 36 |
| 13 | 3:10 | 32 | 36 | 38 | 42 | 67 | 40 | 71 | 42 | 75 | 44 | — | 2:35 | 38 |

## Boss timing and victory

Boss lead time increases from 25 seconds on level 2 to 35 seconds on level 13. The exact lead time is `round(25 + (L - 2) × 10 / 11)` seconds, and boss time is the ritual duration minus that lead.

| Level | Boss encounter |
| --- | --- |
| 1 | None |
| 2 | Moose |
| 3 | Mountain Boss |
| 4 | Moose and Mountain Boss |
| 5 | Electric Golem |
| 6 | Anubis |
| 7 | Electric Golem and Anubis |
| 8 | Stone Golem |
| 9 | Beholder |
| 10 | Fire Elemental |
| 11 | Crab-Claw Terror |
| 12 | Lava Giant |
| 13 | Fire Elemental, Crab-Claw Terror, and Lava Giant |

All bosses listed for a combined encounter spawn simultaneously. Bosses are deliberately strong enough to threaten the stationary wizard objective, but killing them is not required for victory. If the ritual completes while a boss is alive, the screen-wide ritual lightning kills that boss with every other surviving enemy and the level ends in victory.

## Boss XP

A standard enemy drops one normal XP gem before drop modifiers. Each defeated boss drops 15 normal XP gems, and each boss in a combined encounter drops its own 15-gem reward. These drops occur immediately on death, use the ordinary gem pickup behavior, and are affected by the same XP-value and extra-drop modifiers as standard enemy gems.
