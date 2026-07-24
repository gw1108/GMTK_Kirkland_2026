# Player & Skill Tree Design

The player is the warrior using sprites from `Tiny Swords (Free Pack)\Tiny Swords (Free Pack)\Units\Blue Units\Warrior`. This file defines the player's combat presentation, attack families, and the node types available in the between-run skill tree. All scalar values named here must be authored in `game/data/balance.csv` during implementation; this document defines the effects and relationships, not hard-coded values.

## Movement presentation

The warrior moves using the normal movement physics and collision shape, but does not use a walking sprite sheet. The visible body rotates back and forth around its own origin while moving, creating a cheap walk-like sway that can play continuously alongside an attack.

- The physics body, collision shape, and attack targeting direction do not rotate with the visual sway.
- Sway only plays while the warrior has movement input; it returns smoothly to the resting orientation when movement stops.
- Sway amplitude and sway cadence are art/balance values, not GDScript constants.
- The attack animation is played on an independent visual layer or child sprite, so a slash never cancels movement sway and movement never cancels an attack.

## Attacks

The player auto-casts attacks. An attack selects a valid nearby enemy according to its targeting rule, then performs its wind-up, active hit, and recovery without stopping the warrior's movement.

## Common Stats

Abilities used by the warrior and the wizards have the following stats, which affect most abilities.

- **ID:** Stable identifier for the ability.
- **Damage:** The damage an instance of this weapon does.
- **Area:** The size of the projectile or AOE. By default 100% for all abilities.
- **Projectile Speed:** Weapon projectile speed.
- **Amount:** The number of projectiles or instances that occur.
- **Pierce:** The number of enemies a projectile can hit before being destroyed or, for melee attacks, the number of enemies the attack can hit.
- **Cooldown:** The amount of seconds that must pass before activating again. For fast attacks it is 1s. For medium attacks 4s. For slow attacks 10s.
- **Projectile Interval:** The amount of seconds that must pass in between projectiles if it is a multi projectile sequential attack. Rarely used.
- **Knockback:** The amount to knockback enemies.
- **Pool Limit:** The number of projectiles that may be on screen at the same time. If an ability attempts to spawn another projectile while already at the pool limit, recycle a random active projectile. Default is 70.
- **Crit Chance:** The chance of getting a critical strike which applies the critical damage bonus. Default is 5%. By default each projectile rolls their critical strike chance separately. If a projectile has AOE or hits multiple enemies, those enemies share the same crit chance roll.
- **Critical Damage Bonus:** Multiplies damage on a critical strike. The default is 150%, so critical damage is multiplied by 1.5.
- **Blocked by Walls:** If true, the projectile is destroyed when it hits a wall. By default it is true.
- **Duration:** The duration of the effect or damaging aoe circle. Not the life time of the projectile. Usually not used.
- **Projectile Duration:** The duration that a projectile lives before being destroyed. By default it is 20 seconds.
- **Charges:** If an ability specifies it can build up charges or start the level with charges. Charges are expended on activation. By default, the cooldown stat determines how much time before 1 charge is replenished.
- **Animation Speed:** Only Slash attacks benefit from this. Default is 100%; at 200%, the animation plays twice as fast.
- **Ability Armor Penetration:** The amount of target armor ignored by this ability. This is the ability-specific counterpart to the entity's generic Armor Penetration stat.

The warrior player, the wizards, structures, and enemies also have the following generic stats that apply to themselves.

- **Health:** If this reaches 0 the entity dies.
- **Invulnerable:** Some traps are invulnerable and cannot take damage, but are still consumed when triggered.
- **Armor:** A % reduction to incoming damage. Max 90%.
- **Evasion:** A chance to avoid incoming damage. Max 90%.
- **Accuracy:** A % reduction to the enemy's evasion stat. For example if the enemy has 50% evasion but the player has 60% accuracy the chance to hit is 110%. Chance to hit beyond 100% is wasted.
- **Armor Penetration:** A percentage reduction to the enemy's armor stat. Similar to Accuracy.
- **Increased Damage:** A generic % increased damage to all abilities.
- **Increased Crit Chance:** A generic % increased crit chance. For example, if the player upgrades enough nodes for 110% increased crit chance and they use an ability with base 5% crit chance, their chance to crit would be 10.5%.
- **Increased Crit Damage Bonus:** A generic percentage increase to the bonus portion of critical damage. For example, 100% increased critical damage bonus changes a 150% base critical multiplier into 200%: `1 + (0.5 × 2) = 2`.
- **More Damage:** A generic multiplier on damage similar to crit. For example, if a node gives 5% more damage you multiply the final damage number by 1.05.
- **Attack Speed:** Increases the animation speed of attacks.
- **Base Movement Speed:** Base movement speed before increases and reductions.
- **Movement Speed:** Multiplier to the movement speed of this character. For example a 130% means 1.3 * base movement speed. Default is 100%. Can be reduced by status effects.
- **Projectile Count:** Amount of extra projectiles for all abilities that benefit from Amount. Default is 0. For example, if it is 2 then an ice volley will shoot 3 total projectiles in sequence.

### Starting attack: slash

The warrior starts every run with Slash, using `Warrior_Attack1` from the warrior art folder. The slash does not benefit from area, projectile speed, amount, projectile interval, duration, projectile duration. Blocked by walls = false.

- **Targeting:** nearest target in slash range; if none is available, the warrior remains ready rather than swinging into empty space.
- **Shape:** a forward melee arc in the selected target's direction.
- **Hit timing:** the hitbox is active only on the impact frames of the attack animation.
- **Damage:** Slash hits one enemy by default (pierce = 1). A node can raise this value. If more enemies are inside the hitbox than Slash can hit, choose the enemies closest to the player.
- **Movement:** the warrior can continue to move and sway while the independent slash animation is playing.
- **Tuning:** slash damage, interval, range, arc width, knockback, and critical values are all balance-data fields.

### Upgrade-unlocked attack families

These attacks are unlocked by skill-tree nodes and use the same automatic, movement-compatible casting model as Slash.

| Attack family | Targeting and behavior | Non-upgrade hooks |
| --- | --- | --- |
| "Ice Volley": Thrown weapon uses Ice Effect 01, IceVfx 1 as the projectile. | A projectile fires toward the nearest enemy. When adding multiple projectiles they fire sequentially one after the other using the projectile interval = 0.2s. | Does not benefit from Area or Duration. |
| "Bubble Shield": A defensive shield using the `pipo-btleffect208_192.png` animation when the player would take damage from a hit. | Each charge negates one incoming hit. Play the animation facing the direction the hit came from; the animation faces left by default and may be flipped for hits from the right. Charges do not replenish during the level. The red-gem unlock grants one base charge, and the normal-XP Bubble Shield charges node adds more starting charges. | Does not benefit from most upgrades. It has no cooldown; its limited charges control its use. |
| "Holy Hammer": An AOE hammer attack using the `Pixel Art Animations - Paladin - FREE Version/VFX5` animation on a slow projectile interval. | Targets the enemies closest to the player. Multiple projectiles cause multiple strikes, each targeting a different enemy when enough targets are available. | Projectile speed increases the animation speed of the AOE strike. On the hit frame, it deals AOE damage centered on the targeted enemy. It has infinite pierce by default and is not blocked by walls. |
| "Frost Hammer": An AOE hammer attack using `Pixel Art VFX - Frost Knight - FREE Version/VFX1` for the hammer and `Pixel Art VFX - Frost Knight - FREE Version/VFX3` for the explosion. | Targets the enemies closest to the player. Each additional projectile creates one additional explosion traveling away from the hammer animation. | Projectile speed increases the animation speed of the AOE strike. Additional explosions use a default projectile interval of 0.3 seconds. Overlapping explosion areas may hit the same enemy more than once. It has infinite pierce by default and is not blocked by walls. |

### Combo Slash upgrade

Combo Slash upgrades the Slash chain in two stages using the Tiny Swords Warrior animations. The first stage is a two-hit chain: `Warrior_Attack1`, then `Warrior_Attack2`. The final stage is a three-hit chain: `Warrior_Attack1`, then `Warrior_Attack2`, then `Warrior_Attack3`. The first swing uses normal Slash base damage; the second and third have default flat damage bonuses of +2 and +4, respectively. Those bonuses must be authored as separate balance-data fields. Each swing has its own active hit frames, so the same enemy can be hit once by each swing if it remains in range. The local Tiny Swords Free Pack currently contains `Warrior_Attack1.png` and `Warrior_Attack2.png`, but not `Warrior_Attack3.png`; add that matching source asset before implementing the final three-hit stage.

## Defensive units and tower

Archers and Lancers are placed during pre-wave and remain fixed at their placement positions. They have health and can be attacked; neither unit moves after placement.

### Archer unit and tower

Archer is the ranged defensive placement and the only mechanic that becomes a tower. It begins as a Blue Units Archer standing alone. Purchasing the late, one-level Archer Tower transformation node replaces that presentation with `SourceArt/Tiny Swords (Free Pack)/Tiny Swords (Free Pack)/Buildings/Blue Buildings/Tower.png` and positions the Archer at the top. Use the Archer idle and shooting art from `SourceArt/Tiny Swords (Free Pack)/Tiny Swords (Free Pack)/Units/Blue Units/Archer/`; its fired projectile uses `Arrow.png` from that same folder.

- The Archer does not move after placement.
- It automatically fires ranged arrows at enemies in range, dealing damage.
- Archer damage, attack interval, range, arrow speed, projectile pierce, health, and armor are authored through skill-tree and balance data.
- Every placed Archer uses the player's current Archer stats and transformation state.

### Lancer unit

The Lancer is a stationary frontline unit represented by art from `SourceArt/Tiny Swords (Free Pack)/Tiny Swords (Free Pack)/Units/Blue Units/Lancer/`. It is not a tower.

- It does not move and physically blocks enemies.
- Its primary purpose is to act as an HP wall, draw enemy attacks, and protect the wizard. It occasionally attacks nearby enemies and knocks them back.
- It can face all eight directions. Whenever an enemy is in attack range, it automatically turns to face that enemy before attacking.
- Lancer health, armor, damage, attack interval, attack range, and knockback are balance-data fields. Lancer interception targeting follows the deterministic rule in the GDD rather than a random aggro chance.

## Traps

Traps are placed during pre-wave, remain at their placement position, and are consumed when an enemy steps on them. Both trap variants use the four-frame snapping animation at `SourceArt/Bear_Trap.png` as their base sprite. Apply a subtle blue tint for Frost Trap and a subtle green tint for Poison Trap so their effect is legible before triggering. Trap capacity, trigger radius, effect radius, duration, damage, and debuff strength are balance-data fields.

### Frost Trap

Frost Trap is the blue slow trap. When an enemy steps on it, the trap is consumed and plays `SourceArt/Super Pixel Effects Gigapack (Free Version) v2.7.0/Super Pixel Effects Gigapack (Free Version)/spritesheet/Impacts/directional_impact_001/directional_impact_001_large_blue/spritesheet.png`, rotated 90 degrees clockwise, as its explosion. Enemies in the explosion area, including the enemy that triggered it, receive a significant movement-speed slow for the configured debuff duration. The explosion is a crowd-control effect and does not deal damage unless a later design change explicitly adds damage.

### Poison Trap

Poison Trap is the green damage-over-time trap. When an enemy steps on it, the trap is consumed and plays `SourceArt/Super Pixel Effects Gigapack (Free Version) v2.7.0/Super Pixel Effects Gigapack (Free Version)/spritesheet/Fantasy Spells/spell_poison_001/spell_poison_001_large_green/spritesheet.png` as its explosion. Enemies in the explosion area, including the enemy that triggered it, receive a damaging poison debuff for the configured duration. While poisoned, each affected enemy displays `SourceArt/Super Pixel Effects Gigapack (Free Version) v2.7.0/Super Pixel Effects Gigapack (Free Version)/spritesheet/Fantasy Spells/status_poison_001/status_poison_001_large_green/spritesheet.png` as its status-effect visual.

## Skill tree authoring rules

The tree uses the GDD's four directions. Each node type has a CSV-defined maximum level from 1 to 100 and an effect that scales per level. A node's cost follows the GDD's global price rule unless it is a red-gem node. Red-gem major nodes unlock mechanics when purchased; normal-XP nodes improve unlocked or starting mechanics.

### Red-gem major upgrades

The tree contains exactly 12 red-gem major nodes. Each has a maximum level of 1, costs exactly 1 red gem, and does not increase the normal-cost exponent `M`. A major node becomes purchasable after the player has purchased at least one level of its immediately preceding normal-XP node in the authored tree. Later normal-XP nodes scale the unlocked mechanic.

| Direction | Major node | One-time unlock effect |
| --- | --- | --- |
| Up | Ice Volley unlock | Unlocks the automatic Ice Volley projectile attack. |
| Up | Holy Hammer unlock | Unlocks the automatic Holy Hammer AOE attack. |
| Up | Frost Hammer unlock | Unlocks the automatic Frost Hammer AOE attack. |
| Down | Archer unlock | Unlocks Archer placement with a base capacity of 1. |
| Down | Lancer unlock | Unlocks Lancer placement with a base capacity of 1. |
| Down | Frost Trap unlock | Unlocks Frost Trap placement with a base capacity of 1. |
| Down | Poison Trap unlock | Unlocks Poison Trap placement with a base capacity of 1. |
| Right | Second Wizard unlock | Adds the second middle wizard and raises both wizards to 24 maximum health before other wizard-health modifiers. |
| Right | Wizard Wind Burst unlock | Unlocks Wind Burst for every wizard. |
| Right | Wizard Fireball unlock | Unlocks Fireball for every wizard. |
| Right | Wizard Barrier unlock | Unlocks Barrier for every wizard. |
| Right | Wizard Lightning Strike unlock | Unlocks Lightning Strike for every wizard. |

All base capacities, attack values, and spell values granted by these nodes are balance-data fields. Bubble Shield is a normal-XP defensive unlock rather than a red-gem weapon major.

### Up: player power

| Node type | Effect |
| --- | --- |
| Slash damage | Increases base Slash damage. |
| Slash interval | Reduces the time between Slash attacks. |
| Slash knockback | Pushes enemies hit by Slash farther away. |
| Combo Slash | Level 1 upgrades Slash to the two-hit `Warrior_Attack1` → `Warrior_Attack2` chain. Level 2 upgrades it to the three-hit `Warrior_Attack1` → `Warrior_Attack2` → `Warrior_Attack3` chain. The second- and third-swing flat damage bonuses are separate balance-data fields with defaults of +2 and +4. |
| Slash pierce | Increases the number of enemies Slash can hit per swing. |
| Critical chance | Increases the chance for player attacks to critically hit. |
| Critical damage | Increases the damage multiplier of critical hits. |
| Armor penetration | Ignores more enemy armor when armor is introduced. |
| Warrior health | Increases maximum player health. |
| Increased Armor | Increases the warrior's armor. |
| Move speed | Increases warrior movement speed. |
| Dash distance | Increases the Space-dash travel distance. |
| Dash recovery | Reduces the wait before dashing again. |
| Bubble Shield unlock | Unlocks Bubble Shield with one base charge. This normal-XP node has a maximum level of 1. |
| Bubble Shield charges | Adds one Bubble Shield charge at the start of each run. Requires the normal-XP Bubble Shield unlock. |
| Projectile count | Adds projectiles to player projectile attacks. |
| Projectile damage | Increases player projectile damage. |
| Projectile speed | Increases player projectile speed. |
| Projectile pierce | Increases projectile pierce stat to pass through more enemies. |

### Down: defensive placements

| Node type | Effect |
| --- | --- |
| Archer capacity | Increases the maximum number of Archers that can be placed. |
| Archer rank | Improves Archer health and damage. |
| Archer Tower transformation | A one-level normal-XP node that changes every placed Archer to the full tower-and-Archer presentation. Place it late in the Down branch, with enough prerequisite depth that a typical player reaches it around campaign levels 8–11. This is an expected progression window, not a campaign-level requirement. |
| Archer health | Increases Archer health. |
| Archer armor | Increases Archer armor. |
| Archer damage | Increases Archer attack damage. |
| Archer attack interval | Reduces the wait between Archer attacks. |
| Archer range | Increases Archer targeting range. |
| Archer projectile speed | Increases arrow speed. |
| Archer projectile pierce | Adds arrow pierce. |
| Lancer capacity | Increases the maximum number of Lancers that can be placed. |
| Lancer health | Increases Lancer health. |
| Lancer armor | Increases Lancer armor. |
| Lancer damage | Increases Lancer attack damage. |
| Lancer attack interval | Reduces the wait between Lancer attacks. |
| Lancer range | Increases Lancer attack range. |
| Lancer knockback | Pushes enemies struck by Lancers farther away. |
| Frost Trap capacity | Increases the maximum number of Frost Traps that can be placed. |
| Frost Trap slow strength | Increases the movement-speed reduction applied by Frost Traps. |
| Frost Trap slow duration | Increases the duration of the Frost Trap slow debuff. |
| Poison Trap capacity | Increases the maximum number of Poison Traps that can be placed. |
| Poison Trap damage | Increases Poison Trap poison damage over time. |
| Poison Trap duration | Increases the duration of the Poison Trap poison debuff. |

### Left: XP and rewards

| Node type | Effect |
| --- | --- |
| Gem XP value | Increases XP gained from collected XP gems which drop from enemies. |
| Gem pickup range | Increases the distance at which the warrior collects XP gems. |
| Enemy XP-drop chance | Increases the chance that an enemy drops extra XP gems. Each full 100% guarantees one extra gem, and the remainder is the chance for one more. For example, 150% grants one guaranteed extra gem plus a 50% chance for a second extra gem, in addition to the enemy's normal drop. |
| Additional XP Reward | Adds a flat XP reward at the end of the level. |
| Win XP reward | Increases the XP reward at the end of the level by a %. |
| Win XP multiplier| % more xp reward at the end of the level. |

### Right: wizard(s) in the middle

| Node type | Effect |
| --- | --- |
| Wizard health | Increases each wizard's maximum health. |
| Wizard armor | Increases each wizard's damage mitigation. |

The wizard spell scaling nodes that complete this branch are defined in [wizard.md](wizard.md). They require the Wizard defensive spells red-gem major. Defensive spell upgrades do not change the fixed level-ending ritual duration.

## Implementation handoff

Implement the warrior as a physics/movement body with separate visual children for the swaying body and active attack animation. Do not advance a walking sprite-sheet animation while moving. Build the tree from CSV node definitions so every node type, maximum level, cost, and scalar effect can be tuned without changing GDScript.
