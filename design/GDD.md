# I Need More Time to Cast This Spell

## Goal

Survive until the wizard in the middle finishes casting a spell that kills all enemies. The player begins by protecting one wizard. The Second Wizard skill-tree upgrade adds a second wizard and doubles the maximum health of each wizard from 12 to 24, for 48 total wizard health across both wizards.

The wizard you need to protect takes 70 seconds on level 1, +10 seconds per level after (level 2 = 80s, level 3 = 90s, etc.). Levels are meant to be retried: expect the player to attempt level 1 about 4–5 times before beating it, level 2 about 4–6 times, level 3 about 5–6 times, and level 4+ about 5–7 times, upgrading between attempts.

**Win:** when the cast timer completes, lightning strikes every enemy on screen, instantly killing them and ending the level. Show the round summary panel with a "You Win" title.

**Loss:** the level ends as a game loss if either the player dies or any wizard in the middle dies.

- Player health default: 8
- Wizards (middle) health at start: 12 for the single starting wizard; the Second Wizard upgrade adds another wizard and raises both wizards to 24 maximum health each
- Enemy health default: 4
- First boss health: 40

## Game Flow / Screens

1. **Main menu** — Play, Settings, Quit.
2. **Pre-wave phase** — place unlocked defensive units and traps before starting the wave. On level 1 the player has none available, so all they can do is start the wave.
3. **Main loop** — survivor-like gameplay: WASD movement, auto-casting, defend yourself and the wizard(s) until the spell finishes.
4. **Round summary** — panel overlay on win or loss.
5. **Skill tree screen** — spend acquired resources on upgrades, then a button returns to the pre-wave placement phase.

### Level progression and persistence

- Only level 1 is unlocked in a new save.
- Winning a level unlocks the next level. Previously unlocked and completed levels remain replayable.
- Losing does not change the selected level or remove any progression.
- After every attempt, win or lose, the player proceeds from the round summary to the skill tree and then to the pre-wave phase for the selected level.
- The game automatically saves unlocked levels, completed levels, the selected level, collected and spent XP, purchased skill-tree upgrades, and first-win red-gem rewards.

## Levels & Entrances

An "entrance" is a screen edge where enemies spawn off-screen and enter from that side.

- Levels 1–2: one entrance (defend against waves from a single direction).
- Levels 3–5: two entrances, in various combinations.
- Levels 6–9: three entrances.
- Levels 10–13: four entrances.

The exact environment pack, entrance-edge combination, and per-edge spawn weight for every level are defined in [Levels.md](Levels.md).

## Arena & Camera

Each arena is approximately two base viewports across and two base viewports down; with the 960×540 base viewport, the initial arena target is approximately 1920×1080. Arena dimensions are balance-data values and may be adjusted to fit each environment's tile geometry.

The camera uses a fixed zoom for the entire attempt and never zooms dynamically. Its position follows the midpoint between the player and the center of the living wizard group, clamped to the arena bounds. Player movement is restricted by a wizard-visibility leash: a proposed movement is clamped if the player and every living wizard would not all fit inside the fixed camera view with the configured safe-edge margin. The initial safe-edge margin is 10% of the viewport on each side. Camera zoom, safe-edge margin, and leash bounds are balance-data values.

The player also cannot cross the arena's collision bounds. Together, the fixed zoom, midpoint tracking, and movement leash guarantee that the wizard objective remains visible at all times.

Arena layouts are mostly open so the player, enemies, projectiles, and defensive placements have room to function. Some maps use broad chokepoints, especially early levels where fewer entrance directions make lane defense easier to understand. Chokepoints must remain wide enough for several enemies and a Lancer placement; they are not single-tile funnels.

Environment terrain never deals damage or applies status effects. Lava, deep water, holes, cliffs, walls, and similar features are either visual-only decoration or impassable collision. Player movement, enemy navigation, projectiles that are blocked by walls, and placement validation all respect impassable terrain.

## Gameplay

The player character is a warrior. They move with WASD and auto-cast everything. Their spells kill things in their vicinity, like in Vampire Survivors. Use sprites from `Tiny Swords (Free Pack)\Tiny Swords (Free Pack)\Units\Blue Units\Warrior`.

There is no leveling up during gameplay — upgrades are bought on the skill tree screen between attempts. Enemies drop XP gems that the player walks over to pick up. XP gems use the four-frame green gem animation at `SourceArt/Coin_Gems/spr_coin_strip4.png`; its playback speed is a balance-data field. XP from collected gems is always kept, win or lose, and can only be spent at the skill tree step between runs.

**Dash (Space):** quickly moves the player in the direction they are already moving. No i-frames.

### Player abilities

Player attacks, the warrior's movement presentation, and the full skill-tree node catalog are defined in [Player.md](Player.md). The player begins with the automatic Slash attack; upgrade-unlocked attacks use the same movement-compatible auto-cast model.

## Enemy Behaviour

Enemies generally move toward the wizard(s) in the middle to attack them. But if the warrior is within enemy attack range × 1.3, they will target the warrior for at least 5 seconds.

A Lancer overrides the enemy's current target when it physically blocks that enemy's path or enters that enemy's immediate attack range. If multiple Lancers qualify, target the nearest one. Continue targeting that Lancer until it dies, stops blocking the path, or leaves immediate attack range; then resume the normal wizard/warrior targeting rule.

After level 1, 20% of enemies are ranged.

**Melee attack:** the enemy plays a wind-up animation, then after a short delay creates a hitbox that damages the player if they are inside it. A purchasable upgrade visualizes the red hitbox during the wind-up.

**Ranged attack:** same wind-up pattern, but instead of a hitbox the enemy creates a moving projectile.

### Enemy & boss roster

All enemy and boss definitions, including their art sources, initial health, base damage, movement speed, attack timing, attack patterns, level assignments, and spawn weights, live in [Enemies.md](Enemies.md). Bosses appear at level 2 or later, including combined-boss encounters on levels 4, 7, and 13.

## Spawning & Waves

Continuous spawning with event-waves, Vampire Survivors style: there is a minimum number of enemies on the map that slowly increases over time, and timed event waves spawn a burst of enemies (detailed in the balance CSV per level). Event waves can also change the enemy minimum. Default spawn interval: 0.25s.

The complete first-pass level curves, event waves, boss times, and XP rewards are defined in [Levels.md](Levels.md).

Wave tables use the columns `time|enemies|enemy minimum|bosses & treasures|map events|notes`. Each row **replaces** the previous enemy roster and minimum: only the enemies listed in the row's `enemies` column keep spawning, at the row's minimum. To keep an earlier enemy type spawning, list it again alongside the new one (comma-separated). Entries in `bosses & treasures` and `map events` are names of bosses/treasures and events defined elsewhere.

Illustrative 70-second wave table:

```
time|enemies|enemy minimum|bosses & treasures|map events|notes
0:00|bat|15|-|-|-
0:30|bat|60|-|-|-
1:00|skeleton|50|-|-|-
```

Here the 1:00 row replaces bats entirely — only skeletons spawn from then on. If bats should continue alongside skeletons, the row would instead be:

```
1:00|bat,skeleton|50|glowing_bat|bat_swarm|-
```

The names in this example are placeholders. Production rows must use stable IDs from the implemented enemy, boss, treasure, and map-event data.

## Defensive Placements

Archers, Lancers, Frost Traps, and Poison Traps are placed during the pre-wave phase. The player has a separate capacity of 0 for each type by default until they buy the corresponding red-gem unlock.

- Unlocking a type makes placements free; there is no per-placement currency.
- Every placement type has its own independent capacity. Increasing Archer capacity does not increase Lancer or trap capacity.
- Capacity is a free allotment that refreshes at the start of every pre-wave phase.
- Placements do not persist between attempts. The player rebuilds the layout before each wave.
- Before starting the wave, the player may place, move, and remove unlocked objects freely within their capacity.
- A placement cannot overlap the player, a wizard, another placed unit or trap, or an enemy entrance lane.
- Starting the wave locks all placements for the remainder of that attempt.

Archers and Lancers have health and armor and can be attacked by enemies. Lancers are the dedicated HP walls: they physically block enemies, draw aggro, and occasionally attack.

### Placement types

Archer, Lancer, Frost Trap, and Poison Trap behaviors are defined in [Player.md](Player.md). Archer is the game's only tower progression: it begins as a placed Archer unit and upgrades into the full Archer Tower presentation after purchasing a late normal-XP transformation node. The tree should be authored so a typical player reaches that node around levels 8–11 rather than gating it directly by campaign level. Lancers are defensive units, not towers.

## Skill Tree

The tree is a grid with four main directions, authored so it's easy to create/visualize in a CSV. Nodes are clicked repeatedly to level them from 0 to max, where max is between 1 and 100.

**Costs:** base cost 4 XP. Before purchasing a normal node level, calculate `4 × 1.15^M` and round it to the nearest whole XP, with 0.5 rounding up. Equivalently, for these positive prices use `floor(4 × 1.15^M + 0.5)`. `M` is the total number of non-red-gem node levels already purchased across the entire tree, including repeated levels of the same node. Each newly purchased normal node level increases `M` by 1. Red-gem purchases cost exactly 1 red gem and neither use nor increase `M`.

**Red gems:** the only way to earn a special red gem is beating a level for the first time. Red gems use the four-frame red gem animation at `SourceArt/Coin_Gems/spr_coin_roj.png`; its playback speed is a balance-data field. The tree contains one red-gem node per level, minus one (no gem node for the last level) — i.e. total red-gem nodes = level count − 1.

The 13-level game therefore contains exactly 12 red-gem nodes. Each is a one-time major unlock for a new weapon, trap, unit, tower progression, or wizard spell. The complete list is defined in [Player.md](Player.md).

**Rewards for beating a level:** XP, plus a special red gem if the level has never been beaten before.

Four main directions:

- **Up — player power:** faster movement, more player damage, more health, more player projectiles.
- **Down — defensive placements:** unlock Archers, Lancers, Frost Traps, and Poison Traps, then improve their separate capacities and combat stats. A late normal-XP transformation node upgrades Archers into the game's only tower presentation. Lancers serve as attacking HP walls.
- **Left — XP and rewards:** increased XP and rewards for beating the level; chance for enemies to drop health orbs; enemies drop more XP.
- **Right — the wizard(s) in the middle:** they cast spells for you when certain conditions are met — for example, emitting a shockwave that pushes and slows enemies when enemies get close. They auto-cast their spells when appropriate. Their spells defend themselves and rarely kill close, threatening enemies in case something slips through the other defenses — they are not for killing the majority of the enemies. One wizard is present by default; the tree can upgrade this to two.

### Skill tree first pass

The complete first-pass node catalog is in [Player.md](Player.md). It should be authored as a CSV during implementation.

### Wizard (middle) abilities

The wizard's conditional auto-cast defensive spells and related skill-tree nodes are defined in [wizard.md](wizard.md). Use sprites from `Epic RPG World - The Village V2.0/NPCs/old wise wizard`.
