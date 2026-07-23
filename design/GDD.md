# I Need More Time to Cast This Spell

## Goal

Survive until the wizard in the middle finishes casting a spell that kills all enemies. The player begins by protecting one wizard; a skill-tree upgrade later adds a second wizard and also doubles the wizard's health because there are now 2 wizards.

The wizard you need to protect takes 70 seconds on level 1, +10 seconds per level after (level 2 = 80s, level 3 = 90s, etc.). Levels are meant to be retried: expect the player to attempt level 1 about 4–5 times before beating it, level 2 about 4–6 times, level 3 about 5–6 times, and level 4+ about 5–7 times, upgrading between attempts.

**Win:** when the cast timer completes, lightning strikes every enemy on screen, instantly killing them and ending the level. Show the round summary panel with a "You Win" title.

**Loss:** the level ends as a game loss if either the player dies or any wizard in the middle dies.

- Player health default: 8
- Wizards (middle) health at start: 12 each; one wizard by default, two after the relevant skill-tree upgrade
- Enemy health default: 4
- First boss health: 40

## Game Flow / Screens

1. **Main menu** — Play, Settings, Quit.
2. **Pre-wave phase** — place towers/barricades before starting the wave. On level 1 the player has none available, so all they can do is start the wave.
3. **Main loop** — survivor-like gameplay: WASD movement, auto-casting, defend yourself and the wizard(s) until the spell finishes.
4. **Round summary** — panel overlay on win or loss.
5. **Skill tree screen** — spend acquired resources on upgrades, then a button returns to the pre-wave tower placement phase.

## Levels & Entrances

An "entrance" is a screen edge where enemies spawn off-screen and enter from that side.

- Levels 1–2: one entrance (defend against waves from a single direction).
- Levels 3–5: two entrances, in various combinations.
- Levels 6–9: three entrances.
- Levels 10–13: four entrances.

## Arena & Camera

The arena is somewhat large — about 2 screens across and 2 screens down — but small enough that the player can always see the wizard(s) in the middle. The camera follows the player and tries to keep both the player and the wizard(s) in view. The player cannot walk outside the camera bounds.

## Gameplay

The player character is a warrior. They move with WASD and auto-cast everything. Their spells kill things in their vicinity, like in Vampire Survivors. Use sprites from `EPIC RPG World Pack - Grass Land V. 1.6\Characters\Warrior`.

There is no leveling up during gameplay — upgrades are bought on the skill tree screen between attempts. Enemies drop XP gems that the player walks over to pick up. XP from collected gems is always kept, win or lose, and can only be spent at the skill tree step between runs.

**Dash (Space):** quickly moves the player in the direction they are already moving. No i-frames.

### Player abilities

Player attacks, the warrior's movement presentation, and the full skill-tree node catalog are defined in [Player.md](Player.md). The player begins with the automatic Slash attack; upgrade-unlocked attacks use the same movement-compatible auto-cast model.

## Enemy Behaviour

Enemies generally move toward the wizard(s) in the middle to attack them. But if the warrior is within enemy attack range × 1.3, they will target the warrior for at least 5 seconds.

After level 1, 20% of enemies are ranged.

**Melee attack:** the enemy plays a wind-up animation, then after a short delay creates a hitbox that damages the player if they are inside it. A purchasable upgrade visualizes the red hitbox during the wind-up.

**Ranged attack:** same wind-up pattern, but instead of a hitbox the enemy creates a moving projectile.

### Enemy & boss roster

All enemy and boss definitions, including their art sources, initial health, attack power, damage, movement speed, attack speed, and attack patterns, live in [Enemies.md](Enemies.md). Bosses appear at level 2 or later.

## Spawning & Waves

Continuous spawning with event-waves, Vampire Survivors style: there is a minimum number of enemies on the map that slowly increases over time, and timed event waves spawn a burst of enemies (detailed in the balance CSV per level). Event waves can also change the enemy minimum. Default spawn interval: 0.25s.

Wave tables use the columns `time|enemies|enemy minimum|bosses & treasures|map events|notes`. Each row **replaces** the previous enemy roster and minimum: only the enemies listed in the row's `enemies` column keep spawning, at the row's minimum. To keep an earlier enemy type spawning, list it again alongside the new one (comma-separated). Entries in `bosses & treasures` and `map events` are names of bosses/treasures and events defined elsewhere.

Example for level 1:

```
time|enemies|enemy minimum|bosses & treasures|map events|notes
0:00|bat|15|-|-|-
2:00|bat|60|-|-|-
3:00|skeleton|50|-|-|-
```

Here the 3:00 row replaces bats entirely — only skeletons spawn from then on. If bats should continue alongside skeletons, the row would instead be:

```
3:00|bats,skeletons|50|glowing bat|bat swarm|-
```

where `glowing bat` is an enemy defined in the enemy roster and `bat swarm` is an event defined elsewhere.

## Towers & Barricades

Placed during the pre-wave phase. The player has a max of 0 of each by default until they buy the corresponding upgrade on the skill tree. By default towers/barricades have health and armor and can be attacked by enemies that are in the way or that they draw aggro from (varies by tower/barricade type).

### Tower & barricade types (TODO)

Specific towers/barricades, stats, and behaviors to be filled in by a later pass.

## Skill Tree

The tree is a grid with four main directions, authored so it's easy to create/visualize in a CSV. Nodes are clicked repeatedly to level them from 0 to max, where max is between 1 and 100.

**Costs:** base cost 4 XP. Price = base cost × 1.15^M, where M is the number of upgrades the player has already obtained that don't cost a special red gem. Some upgrades instead cost exactly 1 special red gem.

**Red gems:** the only way to earn a special red gem is beating a level for the first time. The tree contains one red-gem node per level, minus one (no gem node for the last level) — i.e. total red-gem nodes = level count − 1.

**Rewards for beating a level:** XP, plus a special red gem if the level has never been beaten before.

Four main directions:

- **Up — player power:** faster movement, more player damage, more health, more player projectiles.
- **Down — towers and barricades:** unlock placement, plus more health and damage, slow effects, AoE damage. Each level 1 tower starts at 30% of the player's level 1 power, slowly increasing up to 100% of the player's damage.
- **Left — XP and rewards:** increased XP and rewards for beating the level; chance for enemies to drop health orbs; enemies drop more XP.
- **Right — the wizard(s) in the middle:** they cast spells for you when certain conditions are met — for example, emitting a shockwave that pushes and slows enemies when enemies get close. They auto-cast their spells when appropriate. Their spells defend themselves and rarely kill close, threatening enemies in case something slips through the other defenses — they are not for killing the majority of the enemies. One wizard is present by default; the tree can upgrade this to two.

### Skill tree first pass

The complete first-pass node catalog is in [Player.md](Player.md). It should be authored as a CSV during implementation.

### Wizard (middle) abilities (TODO)

Still being decided, same status as player abilities: conditional auto-cast defensive spells. A later pass will fill in the specific list and values. Use sprites from `C:\GameDev\GMTK_Kirkland_2026\SourceArt\Epic RPG World - The Village V2.0\NPCs\old wise wizard`.
