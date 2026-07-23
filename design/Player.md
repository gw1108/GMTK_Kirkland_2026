# Player & Skill Tree Design

The player is the warrior using sprites from `EPIC RPG World Pack - Grass Land V. 1.6\Characters\Warrior`. This file defines the player's combat presentation, attack families, and the node types available in the between-run skill tree. All scalar values named here must be authored in `game/data/balance.csv` during implementation; this document defines the effects and relationships, not hard-coded values.

## Movement presentation

The warrior moves using the normal movement physics and collision shape, but does not use a walking sprite sheet. The visible body rotates back and forth around its own origin while moving, creating a cheap walk-like sway that can play continuously alongside an attack.

- The physics body, collision shape, and attack targeting direction do not rotate with the visual sway.
- Sway only plays while the warrior has movement input; it returns smoothly to the resting orientation when movement stops.
- Sway amplitude and sway cadence are art/balance values, not GDScript constants.
- The attack animation is played on an independent visual layer or child sprite, so a slash never cancels movement sway and movement never cancels an attack.

## Attacks

The player auto-casts attacks. An attack selects a valid nearby enemy according to its targeting rule, then performs its wind-up, active hit, and recovery without stopping the warrior's movement.

### Starting attack: slash

The warrior starts every run with Slash, using `warrior-single swing 1.png` from the warrior art folder.

- **Targeting:** nearest target in slash range; if none is available, the warrior remains ready rather than swinging into empty space.
- **Shape:** a forward melee arc in the selected target's direction.
- **Hit timing:** the hitbox is active only on the impact frames of the attack animation.
- **Damage:** one hit per enemy per slash unless the Combo Slash upgrade is active.
- **Movement:** the warrior can continue to move and sway while the independent slash animation is playing.
- **Tuning:** slash damage, interval, range, arc width, knockback, and critical values are all balance-data fields.

### Upgrade-unlocked attack families

These attacks are unlocked by skill-tree nodes and use the same automatic, movement-compatible casting model as Slash.

| Attack family | Targeting and behavior | Primary upgrade hooks |
| --- | --- | --- |
| Cleave | A wider forward melee arc that can hit multiple clustered enemies. | Area, damage, targets hit, interval |
| Whirlwind | A short circular attack centered on the warrior, useful when surrounded. | Radius, duration, damage tick interval |
| Thrown weapon | A projectile fires toward a selected enemy and can travel through a line of enemies. | Projectile count, damage, speed, lifetime, pierce |
| Returning weapon | A projectile travels outward, then returns to the warrior and can hit on both paths. | Damage, travel distance, return speed, pierce |
| Ground shockwave | A short-range outward wave from the warrior that creates space rather than serving as the main damage source. | Radius, damage, knockback, slow |
| Retaliation burst | Automatically triggers after the warrior takes damage, striking close enemies. | Cooldown, radius, damage, knockback |

### Combo Slash upgrade

Combo Slash replaces the default `warrior-single swing 1.png` animation with `warrior-full combo attack with 3 swings.png` from the warrior art folder. It performs three sequential swings at the selected target. The first swing uses normal Slash base damage; the second deals base damage + 2, and the third deals base damage + 4. Each swing has its own active hit frames, so the same enemy can be hit once by each swing if it remains in range.

## Skill tree authoring rules

The tree uses the GDD's four directions. Each node type has a CSV-defined maximum level from 1 to 100 and an effect that scales per level. A node's cost follows the GDD's global price rule unless it is a red-gem node. Nodes unlock mechanics only when their level rises from 0 to 1; later levels improve the listed effect.

### Up: player power

| Node type | Effect |
| --- | --- |
| Slash damage | Increases base Slash damage. |
| Slash interval | Reduces the time between Slash attacks. |
| Slash range | Extends the forward reach of Slash. |
| Slash arc | Widens the Slash hit arc. |
| Slash knockback | Pushes enemies hit by Slash farther away. |
| Combo Slash | Replaces the single-swing Slash with `warrior-full combo attack with 3 swings.png`. The second and third swings deal +2 and +4 base damage respectively. |
| Critical chance | Increases the chance for player attacks to critically hit. |
| Critical damage | Increases the damage multiplier of critical hits. |
| Armor penetration | Ignores more enemy armor when armor is introduced. |
| Warrior health | Increases maximum player health. |
| Health regeneration | Restores player health over time. |
| Damage reduction | Reduces incoming damage to the warrior. |
| Move speed | Increases warrior movement speed. |
| Dash distance | Increases the Space-dash travel distance. |
| Dash recovery | Reduces the wait before dashing again. |
| Sway control | Improves movement-sway responsiveness and reduces the time to return to rest; presentation-only. |
| Auto-target range | Lets automatic player attacks acquire enemies farther away. |
| Cleave unlock | Unlocks the Cleave attack family. |
| Cleave damage | Increases Cleave damage. |
| Cleave area | Increases Cleave arc width and reach. |
| Whirlwind unlock | Unlocks the Whirlwind attack family. |
| Whirlwind radius | Increases Whirlwind radius. |
| Whirlwind damage | Increases Whirlwind damage. |
| Thrown weapon unlock | Unlocks the Thrown weapon attack family. |
| Projectile count | Adds projectiles to player projectile attacks. |
| Projectile damage | Increases player projectile damage. |
| Projectile speed | Increases player projectile speed. |
| Projectile lifetime | Increases projectile travel time. |
| Projectile pierce | Allows projectiles to pass through more enemies. |
| Returning weapon unlock | Unlocks the Returning weapon attack family. |
| Return distance | Increases the outward travel distance of returning weapons. |
| Return speed | Increases the speed of a returning weapon's return path. |
| Ground shockwave unlock | Unlocks Ground shockwave. |
| Shockwave force | Increases Ground shockwave knockback. |
| Retaliation burst unlock | Unlocks Retaliation burst. |
| Retaliation cooldown | Reduces the cooldown of Retaliation burst. |

### Down: towers and barricades

| Node type | Effect |
| --- | --- |
| Tower placement unlock | Allows placement of the first tower type during pre-wave. |
| Tower capacity | Increases the maximum number of towers that can be placed. |
| Tower health | Increases tower health. |
| Tower armor | Increases tower armor. |
| Tower damage | Increases tower attack damage. |
| Tower attack interval | Reduces the wait between tower attacks. |
| Tower range | Increases tower targeting range. |
| Tower projectile speed | Increases tower projectile speed. |
| Tower projectile pierce | Adds tower projectile pierce. |
| Slow tower unlock | Unlocks a tower that slows enemies. |
| Slow strength | Increases the slow effect from slowing towers. |
| Area tower unlock | Unlocks a tower with area damage. |
| Area tower radius | Increases area-tower hit radius. |
| Barricade placement unlock | Allows placement of barricades during pre-wave. |
| Barricade capacity | Increases the maximum number of barricades. |
| Barricade health | Increases barricade health. |
| Barricade armor | Increases barricade armor. |
| Barricade aggro | Makes barricades draw enemy attention more reliably. |

### Left: XP and rewards

| Node type | Effect |
| --- | --- |
| Gem XP value | Increases XP gained from every collected XP gem. |
| Gem pickup range | Increases the distance at which the warrior collects XP gems. |
| Gem attraction speed | Increases how quickly loose XP gems move to the warrior. |
| Enemy XP-drop chance | Increases the chance that an enemy drops an XP gem. |
| XP-gem quantity | Increases the number of XP gems produced by a successful drop. |
| Health-orb drop chance | Increases the chance for enemies to drop health orbs. |
| Health-orb value | Increases the health restored by a health orb. |
| Win XP reward | Increases the XP reward for winning a level. |
| First-clear XP bonus | Increases the one-time XP bonus for a level's first completion. |
| Treasure reward chance | Increases the chance that a boss/treasure event grants an extra non-red reward. |

### Right: wizard(s) in the middle

| Node type | Effect |
| --- | --- |
| Second wizard unlock | Adds the second middle wizard. This is the branch's major red-gem unlock. |
| Wizard health | Increases each wizard's maximum health. |
| Wizard armor | Increases each wizard's damage mitigation. |
| Wizard health regeneration | Restores each wizard's health over time. |
| Wizard auto-cast interval | Reduces the wait between wizard spells. |
| Wizard spell range | Increases the range at which wizards react to threats. |
| Wizard shockwave unlock | Unlocks the close-threat push-and-slow shockwave. |
| Shockwave radius | Increases shockwave radius. |
| Shockwave force | Increases shockwave pushback. |
| Shockwave slow | Increases shockwave slow strength and duration. |
| Wizard barrier unlock | Unlocks a temporary defensive barrier around a threatened wizard. |
| Barrier health | Increases barrier durability. |
| Barrier duration | Increases barrier duration. |
| Emergency blast unlock | Unlocks a close-range emergency blast for enemies that reach the wizard. |
| Emergency blast damage | Increases emergency-blast damage. |
| Emergency blast cooldown | Reduces the emergency-blast cooldown. |
| Wizard projectile unlock | Unlocks a low-frequency defensive projectile for distant threats. |
| Wizard projectile count | Adds projectiles to the wizard's defensive cast. |
| Wizard projectile damage | Increases wizard-projectile damage. |
| Wizard spell area | Increases the area of wizard spells that have an area effect. |

## Implementation handoff

Implement the warrior as a physics/movement body with separate visual children for the swaying body and active attack animation. Do not advance a walking sprite-sheet animation while moving. Build the tree from CSV node definitions so every node type, maximum level, cost, and scalar effect can be tuned without changing GDScript.
