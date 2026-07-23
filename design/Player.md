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

## Common Stats

Abilities the warrior player and the wizards that the player is defending have the following stats that effect most of their abilities.

- **ID:** Id label of the weapon.
- **Damage:** The damage an instance of this weapon does.
- **Area:** The size of the projectile or AOE. By default 100% for all abilities.
- **Projectile Speed:** Weapon projectile speed.
- **Amount:** The amount of projectiles or instances that occurs.
- **Pierce:** The amount of enemies the projectile can hit before being destroyed or for melee the amount of enemies that it can hit.
- **Cooldown:** The amount of seconds that must pass before activating again. For fast attacks it is 1s. For medium attacks 4s. For slow attacks 10s.
- **Projectile Interval:** The amount of seconds that must pass in between projectiles if it is a multi projectile sequential attack. Rarely used.
- **Knockback:** The amount to knockback enemies.
- **Pool Limit:** The amount of projectiles that are allowed on screen at the same time. If attempting to spawn another projectile but already at the pool limit delete a random projectile for reuse. Default is 70.
- **Crit Chance:** The chance of getting a critical strike which applies the critical damage bonus. Default is 5%.
- **Critical Damage Bonus:** Multiply the damage by the critical damage bonus. Default is 150% so multiply the damage by 1.5.
- **Blocked by Walls:** If true, the projectile is destroyed when it hits a wall. By default it is true.
- **Duration:** The duration of the effect or damaging aoe circle. Not the life time of the projectile. Usually not used.
- **Projectile Duration:** The duration that a projectile lives before being destroyed. By default it is 20 seconds.
- **Charges:** If an ability specifies it can build up charges or start the level with charges. Charges are expended on activation. By default, the cooldown stat determines how much time before 1 charge is replenished.
- **Animation Speed**: Only slash attacks benefit from this. Default is 100%. But if it is increased to 200% the animation is played twice as fast.
- **Armor Penetration**: Increased amount of armor that is ignored. Similar to Accuracy.

The warrior player, the wizards, structures, and enemies also have the following generic stats that apply to themselves.

- **Health:** If this reaches 0 the entity dies.
- **Invulnerable:** Some barricades or traps are invulnerable and cannot take damage. They can still die if they are consumed when they are triggered if they are a trap.
- **Armor:** A % reduction to incoming damage. Max 90%.
- **Evasion:** A chance to avoid incoming damage. Max 90%.
- **Accuracy:** A % reduction to the enemy's evasion stat. For example if the enemy has 50% evasion but the player has 60% accuracy the chance to hit is 110%. Chance to hit beyond 100% is wasted.
- **Armor Penetration**: A % reduction to the enemy's armor stat. Similar to accuracy.
- **Increased Damage:** A generic % increased damage to all abilities.
- **Increased Crit Chance:** A generic % increased crit chance. For example, if the player upgrades enough nodes for 110% increased crit chance and they use an ability with base 5% crit chance, their chance to crit would be 10.5%.
- **Increased Crit Damage Bonus:** A generic % increased crit damage bonus. For example, if the player upgrades enough nodes for 100% increased crit damage bonus and they use an ability with 150% base crit damage bonus they will multiply their final damage by 2=(50% * 2 + 1)
- **More Damage:** A generic multiplier on damage similar to crit. For example, if a node gives 5% more damage you multiply the final damage number by 1.05.
- **Attack Speed:** Increases the animation speed of attacks.
- **Base Movement Speed:** Base movement speed before increases and reductions.
- **Movement Speed:** Multiplier to the movement speed of this character. For example a 130% means 1.3 * base movement speed. Default is 100%. Can be reduced by status effects.
- **Projectile Count:** Amount of extra projectiles for all abilities that benefit from Amount. Default is 0. For example, if it is 2 then an ice volley will shoot 3 total projectiles in sequence.

### Starting attack: slash

The warrior starts every run with Slash, using `warrior-single swing 1.png` from the warrior art folder. The slash does not benefit from area, projectile speed, amount, projectile interval, duration, projectile duration. Blocked by walls = false.

- **Targeting:** nearest target in slash range; if none is available, the warrior remains ready rather than swinging into empty space.
- **Shape:** a forward melee arc in the selected target's direction.
- **Hit timing:** the hitbox is active only on the impact frames of the attack animation.
- **Damage:** one hit per enemy per slash by default (pierce = 1). There is a node upgrade that upgrades this value beyond 1. If there are multiple enemies in the hitbox choose the enemy that is closest to the player.
- **Movement:** the warrior can continue to move and sway while the independent slash animation is playing.
- **Tuning:** slash damage, interval, range, arc width, knockback, and critical values are all balance-data fields.

### Upgrade-unlocked attack families

These attacks are unlocked by skill-tree nodes and use the same automatic, movement-compatible casting model as Slash.

| Attack family | Targeting and behavior | Non-upgrade hooks |
| --- | --- | --- |
| "Ice Volley": Thrown weapon uses Ice Effect 01, IceVfx 1 as the projectile. | A projectile fires toward the nearest enemy. When adding multiple projectiles they fire sequentially one after the other using the projectile interval = 0.2s. | Does not benefit from Area or Duration. |
| "Bubble Shield": Defensive bubble shield. which uses the pipo-btleffect208_192.png animation when the player would take damage from a hit. | It plays in the direction that the player got hit from either left or right (animation is default left). For each upgrade the player will reduce incoming damage to 0. Does not recharge or replenish during the level. Starts with charges = to the number of times it has been upgraded with + charges. | Does not benefit from most upgrades except charges = 1 by default. Has 0 base cooldown. |

### Combo Slash upgrade

Combo Slash replaces the default `warrior-single swing 1.png` animation with `warrior-full combo attack with 3 swings.png` from the warrior art folder. It performs three sequential swings at the selected target. The first swing uses normal Slash base damage; the second deals base damage + 2, and the third deals base damage + 4. Each swing has its own active hit frames, so the same enemy can be hit once by each swing if it remains in range.

## Skill tree authoring rules

The tree uses the GDD's four directions. Each node type has a CSV-defined maximum level from 1 to 100 and an effect that scales per level. A node's cost follows the GDD's global price rule unless it is a red-gem node. Nodes unlock mechanics only when their level rises from 0 to 1; later levels improve the listed effect.

### Up: player power

| Node type | Effect |
| --- | --- |
| Slash damage | Increases base Slash damage. |
| Slash interval | Reduces the time between Slash attacks. |
| Slash knockback | Pushes enemies hit by Slash farther away. |
| Combo Slash | Replaces the single-swing Slash with `warrior-full combo attack with 3 swings.png`. The second and third swings deal +2 and +4 base damage respectively. |
| Critical chance | Increases the chance for player attacks to critically hit. |
| Critical damage | Increases the damage multiplier of critical hits. |
| Armor penetration | Ignores more enemy armor when armor is introduced. |
| Warrior health | Increases maximum player health. |
| Increased Armor | Increases the warrior's armor. |
| Move speed | Increases warrior movement speed. |
| Dash distance | Increases the Space-dash travel distance. |
| Dash recovery | Reduces the wait before dashing again. |
| Thrown weapon unlock | Unlocks the "Ice Volley" Thrown weapon attack. |
| Projectile count | Adds projectiles to player projectile attacks. |
| Projectile damage | Increases player projectile damage. |
| Projectile speed | Increases player projectile speed. |
| Projectile pierce | Increases projectile pierce stat to pass through more enemies. |

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
| Gem XP value | Increases XP gained from collected XP gems which drop from enemies. |
| Gem pickup range | Increases the distance at which the warrior collects XP gems. |
| Enemy XP-drop chance | Increases the chance that an enemy drops an extra XP gem. This is a surpassing chance so if it is 150% the enemy will drop 2 xp gems and a 50% chance to drop an additional one for a total of 3 xp gems. |
| Additional XP Reward | Adds a flat XP reward at the end of the level. |
| Win XP reward | Increases the XP reward at the end of the level by a %. |
| Win XP multiplier| % more xp reward at the end of the level. |

### Right: wizard(s) in the middle

| Node type | Effect |
| --- | --- |
| Second wizard unlock | Adds the second middle wizard. This is the branch's major red-gem unlock. The second wizard passively doubles the health of the wizards. |
| Wizard health | Increases each wizard's maximum health. |
| Wizard armor | Increases each wizard's damage mitigation. |
| Wizard auto-cast interval | Reduces the wait before the wizard casts the ultimate spell to beat the level. |
| Wizard barrier unlock | Unlocks a temporary defensive barrier around a threatened wizard. Same as the player's "Bubble Shield" which prevents damage. |

## Implementation handoff

Implement the warrior as a physics/movement body with separate visual children for the swaying body and active attack animation. Do not advance a walking sprite-sheet animation while moving. Build the tree from CSV node definitions so every node type, maximum level, cost, and scalar effect can be tuned without changing GDScript.
