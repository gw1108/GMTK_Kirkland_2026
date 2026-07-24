# Enemies & Bosses

This file is the source of truth for the initial enemy and boss roster. The assets were selected from the SourceArt catalog because they have combat-ready animation coverage. Ambient creatures and non-combat NPCs are intentionally excluded. On implementation, every scalar in these tables must be added to `game/data/balance.csv`; the values here are the matching initial balance targets, not GDScript constants.

## Stat conventions

`Health` is starting hit points. `Damage` is the attack's base damage before increases, reductions, armor, or other mitigation. `Move speed` is pixels per second. Values are per individual enemy unless a pattern explicitly says otherwise.

Enemy targeting follows the GDD: enemies normally advance on the middle wizard(s), but target the warrior for at least five seconds when the warrior is within 1.3 times their attack range.

### Attack timing

Enemy attack timing comes from the supplied attack animations rather than a universal cooldown. Epic/ERW animation packs play at 12 frames per second. An attack's base duration is therefore its complete authored anticipation, follow-through, active, and recovery frame count divided by 12. Loop sections play once unless an attack pattern explicitly calls for a sustained loop.

For every melee attack, pause on the final anticipation pose for a default 1.0-second telegraph hold before playing the follow-through and enabling the damaging hitbox. The hold duration is a balance-data field and may be overridden per attack. Ranged attacks use their authored anticipation timing without this extra melee hold. An enemy cannot begin another attack until its current animation, effects, and recovery have completed.

## Level encounter plan

Continuous-spawn weights below total 100% for each level. Every enemy from a level's primary environment pack appears with non-zero weight. Native enemies contribute 75% of ordinary continuous spawns; the remaining 25% comes from other environments to keep a useful mixture of weaker and stronger enemies. Event waves may temporarily override these weights.

Combined-boss levels spawn all listed bosses together as one encounter. Level 4 combines the bosses from levels 2 and 3, level 7 combines the bosses from levels 5 and 6, and level 13 combines the bosses from levels 10, 11, and 12.

Exact enemy-minimum curves, event-wave counts, boss spawn times, victory handling, and boss XP drops are defined in [Levels.md](Levels.md).

| Level | Primary environment | Native enemies: 75% combined | Guest enemies: 25% combined | Boss encounter |
| --- | --- | --- | --- | --- |
| 1 | Grass Land | Grass Land Goblin 45%, Hostile Warrior 30% | Viper 15%, Cemetery Bat 10% | None |
| 2 | Village | The Village has no combat-character roster; Grass Land Goblin 25%, Hostile Warrior 20%, Orc Mage 15%, Orc Warrior 15% form its regional roster | Viper 15%, Cemetery Bat 10% | Moose |
| 3 | Grass Land 2.0 | Orc Mage 35%, Orc Warrior 40% | Grass Land Goblin 15%, Cemetery Bat 10% | Mountain Boss |
| 4 | Sea Adventures | Sea Raider 75% | Orc Mage 10%, Viper 8%, Cemetery Bat 7% | Moose and Mountain Boss |
| 5 | Highlands | Little Dragon 40%, Troll 35% | Sea Raider 15%, Grass Land Goblin 10% | Electric Golem |
| 6 | Desert | Mummy 45%, Sandworm 30% | Viper 15%, Mountain Enemy 2 10% | Anubis |
| 7 | Mountain | Mountain Enemy 1 30%, Mountain Enemy 2 25%, Pot Creature 20% | Mummy 15%, Troll 10% | Electric Golem and Anubis |
| 8 | Ancient Ruins | Ancient Ruins has no standard combat-character roster; Mountain Enemy 1 20%, Mountain Enemy 2 20%, Hostile Warrior 18%, Orc Warrior 17% form its regional roster | Troll 10%, Mummy 10%, Viper 5% | Stone Golem |
| 9 | Sewers | Mutant Rat 40%, Viper 35% | Cemetery Bat 10%, Prison Assassin 10%, Pot Creature 5% | Beholder |
| 10 | Old Prison | Prison Assassin 25%, Mage Skeleton 25%, Prison Skeleton 25% | Crypt Skeleton 10%, Undead 10%, Orc Mage 5% | Fire Elemental |
| 11 | Cemetery | Cemetery Bat 40%, Undead 35% | Crypt Spider 10%, Prison Skeleton 10%, Mummy 5% | Crab-Claw Terror |
| 12 | Crypt | Big Worm 1 18%, Big Worm 2 17%, Crypt Skeleton 22%, Crypt Spider 18% | Undead 10%, Mage Skeleton 10%, Cemetery Bat 5% | Lava Giant |
| 13 | Volcano | Imp-like Demon 40%, Rocky Dude 35% | Big Worm 2 8%, Troll 7%, Orc Warrior 6%, Prison Assassin 4% | Fire Elemental, Crab-Claw Terror, and Lava Giant |

## Standard enemies

| Enemy | Source art group | Health | Damage | Move speed | Attack pattern |
| --- | --- | ---: | ---: | ---: | --- |
| Mummy | `Epic RPG World - Desert V1.6/characters/mummy/` | 4 | 1 | 78 | Slow melee swipe; its second attack pulls a nearby target slightly closer before striking. |
| Sandworm | `Epic RPG World - Desert V1.6/characters/sandworm/` | 8 | 2 | 0 while buried | Burrows between attacks, repositions through a special burrow action, then emerges under a target for a short-range area bite before retreating underground. Its burrow distance and timing still need to be specified. |
| Little Dragon | `Epic RPG World - Highlands V1.4.1/characters/Little Dragon/` | 5 | 1 | 130 | Flies directly toward its target, alternates a close bite with a small projectile shot, then repositions. |
| Troll | `Epic RPG World - Highlands V1.4.1/characters/Troll/` | 10 | 3 | 54 | Slow pursuit; long wind-up heavy smash with a small circular impact area. |
| Mutant Rat | `EPIC RPG World - Sewers V1.5/Characters/Mutant Rat/` | 4 | 1 | 112 | Quick bite in melee; every third attack is a slower bubble projectile. |
| Viper | `EPIC RPG World - Sewers V1.5/Characters/Viper/` | 3 | 1 | 126 | Fast slither and short lunge bite; pauses briefly after the lunge. |
| Mountain Enemy 1 | `Epic RPG World - The dephs of the Mountain V1.5.1/Characters/Enemy 1/` | 5 | 1 | 92 | Base and variation sprites share a forward melee swing with a readable wind-up. |
| Mountain Enemy 2 | `Epic RPG World - The dephs of the Mountain V1.5.1/Characters/Enemy 2/` | 6 | 2 | 82 | Deliberate melee attack, then a short recovery that creates a dodge window. |
| Pot Creature | `Epic RPG World - The dephs of the Mountain V1.5.1/Characters/Pot Creature/` | 4 | 1 | 70 | Begins disguised/hidden; reveals when a target is close, fires one projectile, then uses a close shove. |
| Imp-like Demon | `Epic RPG World - Volcano V1.6/Characters/imp-like demon/` | 5 | 2 | 104 | Short claw attack at close range; periodically leaves a brief lava-pool hazard before retreating. |
| Rocky Dude | `Epic RPG World - Volcano V1.6/Characters/rocky dude/` | 7 | 2 | 66 | Slow stone punch; alternate attack throws a short-range rock burst. Shadow and no-shadow exports are visual variants only. |
| Cemetery Bat | `EPIC RPG World Pack - Cemetery V 1.6/Characters/bat/` | 2 | 1 | 152 | Fast flying swoop, bite, then pulls away before circling back. Two sprite variants are cosmetic. |
| Undead | `EPIC RPG World Pack - Cemetery V 1.6/Characters/undead/` | 5 | 1 | 66 | Slow direct pursuit and a single close swipe. Alternate idle is cosmetic. |
| Big Worm 1 | `EPIC RPG World Pack - Crypt V.1.6/Characters/Big Worm 1/` | 9 | 2 | 0 while burrowed | Emerges with a telegraphed 29-frame bite, remains exposed briefly, then retreats. |
| Big Worm 2 | `EPIC RPG World Pack - Crypt V.1.6/Characters/Big Worm 2/` | 10 | 2 | 0 while burrowed | Same ambush role as Big Worm 1, but stays exposed longer and has a wider bite area. |
| Crypt Skeleton | `EPIC RPG World Pack - Crypt V.1.6/Characters/Skeleton/` | 4 | 1 | 88 | Direct melee strike after a short wind-up. The two animated variants spawn as visual variety. |
| Crypt Spider | `EPIC RPG World Pack - Crypt V.1.6/Characters/Spider/` | 3 | 1 | 124 | Fast close bite; occasionally makes a short leap instead of walking. The two animated variants spawn as visual variety. |
| Grass Land Goblin | `EPIC RPG World Pack - Grass Land V. 1.6/Characters/Enemy1/` | 4 | 1 | 98 | Basic melee attacker; base and variant sprites use the same timing. |
| Hostile Warrior | `EPIC RPG World Pack - Grass Land V. 1.6/Characters/Warrior/` | 6 | 2 | 86 | Armed humanoid opponent with a readable sword swing and brief recovery. This is a hostile use of the same art family as the player, not the player character. |
| Prison Assassin | `EPIC RPG World Pack - Old Prison V1.7.1/Characters/Assassin like enemy/` | 4 | 2 | 142 | Rapid dash into a melee strike, then backs off before repeating. |
| Mage Skeleton | `EPIC RPG World Pack - Old Prison V1.7.1/Characters/Mage Skeleton/` | 5 | 2 | 72 | Holds range and casts a slow projectile; shield/no-shield/rusty variants alter visuals and the shielded version gains 2 health. |
| Prison Skeleton | `EPIC RPG World Pack - Old Prison V1.7.1/Characters/Skeleton 1/` | 5 | 2 | 80 | Melee weapon swing; shield/no-shield/rusty variants alter visuals and the shielded version gains 2 health. |
| Orc Mage | `ERW - Grass Land 2.0 v2.1/Characters/orc mage/` | 6 | 2 | 68 | Keeps range and casts a hand-effect projectile after a conspicuous wind-up. Orc 1 and Orc 2 are visual variants. |
| Orc Warrior | `ERW - Grass Land 2.0 v2.1/Characters/orc warrior/` | 8 | 3 | 76 | Pursues into melee, using a staged spin attack that damages all targets close to it. Orc 1 and Orc 2 are visual variants. |
| Sea Raider | `ERW - Sea Adventures (GL 2.0 expansion) V1.4.2/Characters/female enemy/` | 6 | 2 | 86 | Fires a direct shot at range; at close range, channels a staged area attack before releasing it. |

### Standard-enemy attack timing

These are the initial art-derived timings at 12 FPS. A melee total includes the default 1.0-second telegraph hold. Looping attacks use one loop by default.

| Enemy | Initial attack timing |
| --- | --- |
| Mummy | Attack 1: 5 frames / 0.42 seconds native, 1.42 seconds with melee hold. Attack 2: 4 frames / 0.33 seconds native, 1.33 seconds with melee hold. |
| Sandworm | Appear/attack, loop, and retreat: 45 frames / 3.75 seconds native, 4.75 seconds with melee hold. Any additional exposed-idle time is a separate balance field. |
| Little Dragon | Bite: 5 frames / 0.42 seconds native, 1.42 seconds with melee hold. Projectile: 4 frames / 0.33 seconds. |
| Troll | Basic attack: 4 frames / 0.33 seconds native, 1.33 seconds with melee hold. Heavy attack with one loop: 16 frames / 1.33 seconds native, 2.33 seconds with melee hold. |
| Mutant Rat | Bite: 14 frames / 1.17 seconds native, 2.17 seconds with melee hold. Every third attack uses the 10-frame / 0.83-second alternate attack as the bubble-projectile cast. |
| Viper | Lunge bite: 9 frames / 0.75 seconds native, 1.75 seconds with melee hold. |
| Mountain Enemy 1 | Primary attack: 16 frames / 1.33 seconds native, 2.33 seconds with melee hold. |
| Mountain Enemy 2 | Attack and return: 11 frames / 0.92 seconds native, 1.92 seconds with melee hold. |
| Pot Creature | Close attack: 23 frames / 1.92 seconds native, 2.92 seconds with melee hold. Projectile attack: 24 frames / 2.00 seconds. |
| Imp-like Demon | Melee: 13 frames / 1.08 seconds native, 2.08 seconds with melee hold. Lava attack with one loop: 31 frames / 2.58 seconds. |
| Rocky Dude | Basic melee: 19 frames / 1.58 seconds native, 2.58 seconds with melee hold. Heavy attack: 26 frames / 2.17 seconds native, 3.17 seconds with melee hold. |
| Cemetery Bat | Full transition, attack-instance, and attack chain: 30 frames / 2.50 seconds native, 3.50 seconds with melee hold. |
| Undead | Attack: 18 frames / 1.50 seconds native, 2.50 seconds with melee hold. |
| Big Worm 1 | Appear/attack and retreat: 61 frames / 5.08 seconds native, 6.08 seconds with melee hold. Any additional exposed-idle time is a separate balance field. |
| Big Worm 2 | Appear/attack and retreat: 61 frames / 5.08 seconds native, 6.08 seconds with melee hold. Any additional exposed-idle time is a separate balance field. |
| Crypt Skeleton | Attack: 17 frames / 1.42 seconds native, 2.42 seconds with melee hold. |
| Crypt Spider | Attack: 12 frames / 1.00 second native, 2.00 seconds with melee hold. |
| Grass Land Goblin | Attack 1: 17 frames / 1.42 seconds native, 2.42 seconds with melee hold. Attack 2: 14 frames / 1.17 seconds native, 2.17 seconds with melee hold. |
| Hostile Warrior | Single sword swing: 11 frames / 0.92 seconds native, 1.92 seconds with melee hold. |
| Prison Assassin | Dash attack: 22 frames / 1.83 seconds native, 2.83 seconds with melee hold. Back-off movement occurs after this sequence. |
| Mage Skeleton | Ranged cast with one loop: 21 frames / 1.75 seconds. |
| Prison Skeleton | Attack 1: 18 frames / 1.50 seconds native, 2.50 seconds with melee hold. Attack 2: 13 frames / 1.08 seconds native, 2.08 seconds with melee hold. |
| Orc Mage | Ranged Attack 1: 18 frames / 1.50 seconds. |
| Orc Warrior | Basic attack: 16 frames / 1.33 seconds native, 2.33 seconds with melee hold. Spin with one loop: 20 frames / 1.67 seconds native, 2.67 seconds with melee hold. |
| Sea Raider | Direct ranged attack: 21 frames / 1.75 seconds. Area attack with one loop: 27 frames / 2.25 seconds. |

## Bosses

Bosses appear from level 2 onward according to the level encounter plan above. Moose is the first boss and uses the GDD's starting 40 health. Boss health and damage are retuned for campaign position; their movement and attack identities remain asset-specific. A boss's phases use its supplied animation states and effects; they are not decorative-only sequences.

| Boss | Source art group | First solo level | Health | Damage | Move speed | Attack pattern |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| Moose | `ERW - Ancient Ruins V 2.3/Characters/Moose/` | 2 | 40 | 3 | 116 | Runs to build charge distance, telegraphs, then charges through targets. Six supplied variants and dust/smear animations support its charge readability. |
| Mountain Boss | `Epic RPG World - The dephs of the Mountain V1.5.1/Characters/Boss/` | 3 | 52 | 3 | 66 | Phase 1 walks and alternates its first two attacks. At 50% health, it adds attack 3 and projectile volleys; its supplied wind-up, loop, recovery, hurt, death, and resurrect states make every phase readable. |
| Electric Golem | `Epic RPG World - Highlands V1.4.1/characters/Electric Golem/` | 5 | 68 | 4 | 58 | Pursues with attack 1, then pauses to charge attack 2 through its prep, loop, and rest states. The charged release sends lightning in a straight line and briefly slows targets hit. |
| Anubis | `Epic RPG World - Desert V1.6/characters/anubis/` | 6 | 80 | 4 | 82 | Uses a melee strike at close range and a spell attack at distance. At 50% health, alternates black-hole pull and plague-cloud areas, with sandworm effects marking its strongest attack. |
| Stone Golem | `ERW - Ancient Ruins V 2.3/Characters/Stone  Golem/` | 8 | 96 | 5 | 50 | Alternates a close stone slam with a forward charge. Two large visual variants use the same combat behavior. |
| Beholder | `EPIC RPG World - Sewers V1.5/Characters/Beholder/` | 9 | 108 | 5 | 78 hover | Cycles three attacks: aimed eye projectile, sweeping beam, and spinning projectile burst. Each has anticipation, loop, and recovery; it relocates during recovery. |
| Fire Elemental | `Epic RPG World - Volcano V1.6/Characters/elemental/` | 10 | 120 | 5 | 74 | Fires a basic flame attack, then performs a staged meteor/skull summon that lands as a delayed area strike. Its long death animation is reserved for the kill finish. |
| Crab-Claw Terror | `ERW - Sea Adventures (GL 2.0 expansion) V1.4.2/Characters/crab-claw enemy/` | 11 | 132 | 6 | 62 | Alternates two claw attacks, then enters a staged tentacle-summon sequence. Tentacles strike nearby targets before the boss returns to an idle state. |
| Lava Giant | `Epic RPG World - Volcano V1.6/Characters/giant boss/` | 12 | 148 | 7 | 44 | Requires assembly from the supplied modular body parts. Uses a slow ground smash, a forward lava burst, and an eye/head telegraphed eruption; the parts must be assembled before this boss is implemented. |

### Boss attack timing

| Boss | Initial attack timing |
| --- | --- |
| Mountain Boss | Attack 1 and return: 31 frames / 2.58 seconds native, 3.58 seconds with melee hold. Attack 2: 19 frames / 1.58 seconds native, 2.58 seconds with melee hold. Projectile-based Attack 3 with one loop and return: 47 frames / 3.92 seconds. |
| Beholder | Attack 1 with one loop: 48 frames / 4.00 seconds. Attacks 2 and 3 with one loop: 16 frames / 1.33 seconds each. |
| Anubis | Melee: 5 frames / 0.42 seconds native, 1.42 seconds with melee hold. Spell timing follows the selected black-hole or plague VFX sequence because the packed Attack 2 body sheet does not expose an unambiguous sequential frame count. |
| Electric Golem | Basic melee: 5 frames / 0.42 seconds native, 1.42 seconds with melee hold. Charged attack with one loop: 54 frames / 4.50 seconds. |
| Stone Golem | Slam: 17 frames / 1.42 seconds native, 2.42 seconds with melee hold. The forward charge reuses this combat animation while moving the boss; the source pack does not contain a distinct second attack sheet. |
| Moose | Charge attack: 30 frames / 2.50 seconds native, 3.50 seconds with melee hold. |
| Fire Elemental | Basic ranged attack: 20 frames / 1.67 seconds. Special VFX chain with one summon loop: 43 frames / 3.58 seconds. |
| Crab-Claw Terror | Claw attack: 17 frames / 1.42 seconds native, 2.42 seconds with melee hold. Tentacle attack body sequence with one loop: 40 frames / 3.33 seconds; the 25-frame / 2.08-second tentacle sequence plays concurrently. |
| Lava Giant | No art-derived duration is available because the source contains modular static body parts rather than assembled attack animations. Its procedural assembly and attack timings must be authored before implementation. |

## Art not assigned to combat

Tiny sewer rats, cemetery crows, Grass Land small animals, Ancient Ruins silly-luck creatures, and catalogued NPC/merchant/vendor/blacksmith groups have no combat animation evidence. Do not turn them into enemies without a later design decision and suitable animation coverage.
