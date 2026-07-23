# Enemies & Bosses

This file is the source of truth for the initial enemy and boss roster. The assets were selected from the SourceArt catalog because they have combat-ready animation coverage. Ambient creatures and non-combat NPCs are intentionally excluded. On implementation, every scalar in these tables must be added to `game/data/balance.csv`; the values here are the matching initial balance targets, not GDScript constants.

## Stat conventions

`Health` is starting hit points. `Attack power` is the attack's raw value before mitigation; `Damage` is the HP loss against zero armor, so these are equal until a target has armor. `Move speed` is pixels per second. `Attack speed` is the seconds an enemy must wait after an attack before it can attack again; it is 0.3 seconds by default and 3 seconds for the Sandworm. Values are per individual enemy unless a pattern explicitly says otherwise.

Enemy targeting follows the GDD: enemies normally advance on the middle wizard(s), but target the warrior for at least five seconds when the warrior is within 1.3 times their attack range.

## Standard enemies

| Enemy | Source art group | Health | Attack power | Damage | Move speed | Attack speed (s) | Attack pattern |
| --- | ---: | --- | ---: | ---: | ---: | ---: | --- |
| Mummy | `Epic RPG World - Desert V1.6/characters/mummy/` | 4 | 1 | 1 | 78 | 0.3 | Slow melee swipe; its second attack pulls a nearby target slightly closer before striking. |
| Sandworm | `Epic RPG World - Desert V1.6/characters/sandworm/` | 8 | 2 | 2 | 0 while buried | 3.0 | Burrows between attacks, then emerges under a target for a short-range area bite before retreating underground. Also burrows up and down to move. The movespeed here actually indicates with burrowed movement style it will move what other enemies move 2 in 1 second when it chooses how to attack move. |
| Little Dragon | `Epic RPG World - Highlands V1.4.1/characters/Little Dragon/` | 5 | 1 | 1 | 130 | 0.3 | Flies directly toward its target, alternates a close bite with a small projectile shot, then repositions. |
| Troll | `Epic RPG World - Highlands V1.4.1/characters/Troll/` | 10 | 3 | 3 | 54 | 0.3 | Slow pursuit; long wind-up heavy smash with a small circular impact area. |
| Mutant Rat | `EPIC RPG World - Sewers V1.5/Characters/Mutant Rat/` | 4 | 1 | 1 | 112 | 0.3 | Quick bite in melee; every third attack is a slower bubble projectile. |
| Viper | `EPIC RPG World - Sewers V1.5/Characters/Viper/` | 3 | 1 | 1 | 126 | 0.3 | Fast slither and short lunge bite; pauses briefly after the lunge. |
| Mountain Enemy 1 | `Epic RPG World - The dephs of the Mountain V1.5.1/Characters/Enemy 1/` | 5 | 1 | 1 | 92 | 0.3 | Base and variation sprites share a forward melee swing with a readable wind-up. |
| Mountain Enemy 2 | `Epic RPG World - The dephs of the Mountain V1.5.1/Characters/Enemy 2/` | 6 | 2 | 2 | 82 | 0.3 | Deliberate melee attack, then a short recovery that creates a dodge window. |
| Pot Creature | `Epic RPG World - The dephs of the Mountain V1.5.1/Characters/Pot Creature/` | 4 | 1 | 1 | 70 | 0.3 | Begins disguised/hidden; reveals when a target is close, fires one projectile, then uses a close shove. |
| Imp-like Demon | `Epic RPG World - Volcano V1.6/Characters/imp-like demon/` | 5 | 2 | 2 | 104 | 0.3 | Short claw attack at close range; periodically leaves a brief lava-pool hazard before retreating. |
| Rocky Dude | `Epic RPG World - Volcano V1.6/Characters/rocky dude/` | 7 | 2 | 2 | 66 | 0.3 | Slow stone punch; alternate attack throws a short-range rock burst. Shadow and no-shadow exports are visual variants only. |
| Cemetery Bat | `Epic RPG World - Cemetery V1.6/Characters/bat/` | 2 | 1 | 1 | 152 | 0.3 | Fast flying swoop, bite, then pulls away before circling back. Two sprite variants are cosmetic. |
| Undead | `Epic RPG World - Cemetery V1.6/Characters/undead/` | 5 | 1 | 1 | 66 | 0.3 | Slow direct pursuit and a single close swipe. Alternate idle is cosmetic. |
| Big Worm 1 | `EPIC RPG World Pack - Crypt V.1.6/Characters/Big Worm 1/` | 9 | 2 | 2 | 0 while burrowed | 0.3 | Emerges with a telegraphed 29-frame bite, remains exposed briefly, then retreats. |
| Big Worm 2 | `EPIC RPG World Pack - Crypt V.1.6/Characters/Big Worm 2/` | 10 | 2 | 2 | 0 while burrowed | 0.3 | Same ambush role as Big Worm 1, but stays exposed longer and has a wider bite area. |
| Crypt Skeleton | `EPIC RPG World Pack - Crypt V.1.6/Characters/Skeleton/` | 4 | 1 | 1 | 88 | 0.3 | Direct melee strike after a short wind-up. The two animated variants spawn as visual variety. |
| Crypt Spider | `EPIC RPG World Pack - Crypt V.1.6/Characters/Spider/` | 3 | 1 | 1 | 124 | 0.3 | Fast close bite; occasionally makes a short leap instead of walking. The two animated variants spawn as visual variety. |
| Grass Land Goblin | `EPIC RPG World Pack - Grass Land V. 1.6/Characters/Enemy1/` | 4 | 1 | 1 | 98 | 0.3 | Basic melee attacker; base and variant sprites use the same timing. |
| Hostile Warrior | `EPIC RPG World Pack - Grass Land V. 1.6/Characters/Warrior/` | 6 | 2 | 2 | 86 | 0.3 | Armed humanoid opponent with a readable sword swing and brief recovery. This is a hostile use of the same art family as the player, not the player character. |
| Prison Assassin | `Epic RPG World - Old Prison/Characters/Assassin like enemy/` | 4 | 2 | 2 | 142 | 0.3 | Rapid dash into a melee strike, then backs off before repeating. |
| Mage Skeleton | `Epic RPG World - Old Prison/Characters/Mage Skeleton/` | 5 | 2 | 2 | 72 | 0.3 | Holds range and casts a slow projectile; shield/no-shield/rusty variants alter visuals and the shielded version gains 2 health. |
| Prison Skeleton | `Epic RPG World - Old Prison/Characters/Skeleton 1/` | 5 | 2 | 2 | 80 | 0.3 | Melee weapon swing; shield/no-shield/rusty variants alter visuals and the shielded version gains 2 health. |
| Orc Mage | `Epic RPG World Pack - Grass Land 2.0/Characters/orc mage/` | 6 | 2 | 2 | 68 | 0.3 | Keeps range and casts a hand-effect projectile after a conspicuous wind-up. Orc 1 and Orc 2 are visual variants. |
| Orc Warrior | `Epic RPG World Pack - Grass Land 2.0/Characters/orc warrior/` | 8 | 3 | 3 | 76 | 0.3 | Pursues into melee, using a staged spin attack that damages all targets close to it. Orc 1 and Orc 2 are visual variants. |
| Sea Raider | `ERW - Sea Adventures (GL 2.0 expansion) V1.4.2/Characters/female enemy/` | 6 | 2 | 2 | 86 | 0.3 | Fires a direct shot at range; at close range, channels a staged area attack before releasing it. |

## Bosses

Bosses appear from level 2 onward. The listed level is their earliest intended appearance, so the Mountain Boss is the first boss and keeps the GDD's starting 40 health. A boss's phases use its supplied animation states and effects; they are not decorative-only sequences.

| Boss | Source art group | Earliest level | Health | Attack power | Damage | Move speed | Attack speed (s) | Attack pattern |
| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | --- |
| Mountain Boss | `Epic RPG World - The dephs of the Mountain V1.5.1/Characters/Boss/` | 2 | 40 | 3 | 3 | 66 | 0.3 | Phase 1 walks and alternates its first two attacks. At 50% health, it adds attack 3 and projectile volleys; its supplied wind-up, loop, recovery, hurt, death, and resurrect states make every phase readable. |
| Beholder | `EPIC RPG World - Sewers V1.5/Characters/Beholder/` | 3 | 52 | 3 | 3 | 78 hover | 0.3 | Cycles three attacks: aimed eye projectile, sweeping beam, and spinning projectile burst. Each has anticipation, loop, and recovery; it relocates during recovery. |
| Anubis | `Epic RPG World - Desert V1.6/characters/anubis/` | 4 | 64 | 4 | 4 | 82 | 0.3 | Uses a melee strike at close range and a spell attack at distance. At 50% health, alternates black-hole pull and plague-cloud areas, with sandworm effects marking its strongest attack. |
| Electric Golem | `Epic RPG World - Highlands V1.4.1/characters/Electric Golem/` | 5 | 76 | 4 | 4 | 58 | 0.3 | Pursues with attack 1, then pauses to charge attack 2 through its prep, loop, and rest states. The charged release sends lightning in a straight line and briefly slows targets hit. |
| Stone Golem | `ERW - Ancient Ruins V 2.3/Characters/Stone  Golem/` | 6 | 90 | 5 | 5 | 50 | 0.3 | Alternates a close stone slam with a forward charge. Two large visual variants use the same combat behavior. |
| Moose | `ERW - Ancient Ruins V 2.3/Characters/Moose/` | 7 | 82 | 5 | 5 | 116 | 0.3 | Runs to build charge distance, telegraphs, then charges through targets. Six supplied variants and dust/smear animations support its charge readability. |
| Fire Elemental | `Epic RPG World - Volcano V1.6/Characters/elemental/` | 8 | 98 | 5 | 5 | 74 | 0.3 | Fires a basic flame attack, then performs a staged meteor/skull summon that lands as a delayed area strike. Its long death animation is reserved for the kill finish. |
| Crab-Claw Terror | `ERW - Sea Adventures (GL 2.0 expansion) V1.4.2/Characters/crab-claw enemy/` | 9 | 112 | 6 | 6 | 62 | 0.3 | Alternates two claw attacks, then enters a staged tentacle-summon sequence. Tentacles strike nearby targets before the boss returns to an idle state. |
| Lava Giant | `Epic RPG World - Volcano V1.6/Characters/giant boss/` | 10 | 140 | 7 | 7 | 44 | 0.3 | Requires assembly from the supplied modular body parts. Uses a slow ground smash, a forward lava burst, and an eye/head telegraphed eruption; the parts must be assembled before this boss is implemented. |

## Art not assigned to combat

Tiny sewer rats, cemetery crows, Grass Land small animals, Ancient Ruins silly-luck creatures, and catalogued NPC/merchant/vendor/blacksmith groups have no combat animation evidence. Do not turn them into enemies without a later design decision and suitable animation coverage.
