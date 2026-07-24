# Middle Wizard Design

The middle wizard is a stationary objective that the warrior protects while it completes the level-ending ritual. It uses sprites from `Epic RPG World - The Village V2.0/NPCs/old wise wizard`. One wizard is present by default; the Second Wizard unlock from the skill tree adds a second wizard and doubles the maximum health of each wizard, as defined in the GDD.

This document replaces the GDD's pending wizard-ability list. It defines defensive, conditional auto-casts only: wizards protect themselves when enemies become threatening, but are not intended to kill most enemies. The warrior, towers, and barricades remain the primary means of clearing waves.

## Core behaviour

- A wizard never moves, targets enemies with normal movement, or pursues an enemy.
- Enemies normally target the middle wizard(s), following the targeting rules in the GDD.
- Each wizard has its own health, armor, damage intake, spell cooldowns, and active barrier state.
- Each wizard evaluates its spell conditions automatically. It casts an eligible spell as soon as that spell's cooldown is ready; no player input is required.
- If more than one spell is eligible at once, cast Barrier first, then Wind Burst, then Fireball, then Lightning Strike. A successful cast starts only that spell's cooldown and does not delay the ritual timer.
- A spell may be cast by either wizard independently. When two wizards are present, they do not cast the same spell at the same moment against the same nearby threat if the first cast has already resolved that threat.
- All spell visual scale, ranges, damage, durations, cooldowns, projectile values, and mitigation values are authored in `game/data/balance.csv`. They must not be hard-coded in GDScript.

## Level-ending ritual

From the start of a level, every middle wizard continuously performs the ritual that completes the level after the GDD's level-specific cast time. The ritual is not an attack and is not interrupted by casting a defensive spell, taking damage, or having an active barrier.

When the level timer completes, lightning strikes every enemy on screen, instantly kills them, and the level ends in victory as specified by the GDD. The defensive spells below do not shorten this timer. The existing `Wizard auto-cast interval` skill-tree entry should be re-authored during implementation to improve one of the defensive spell cooldowns or removed; it must not contradict the fixed level ritual duration.

## Wizard abilities

Each spell uses the common ability and generic-stat conventions in [Player.md](Player.md). Its balance row should use a stable `wizard_`-prefixed ID.

### Wind Burst

The wizard releases a circular wind pulse centered on itself when one or more enemies enter its Wind Burst threat radius.

- **Purpose:** Create space between the wizard and nearby attackers.
- **Targeting:** All enemies in the threat radius when the spell resolves.
- **Effect:** Push affected enemies directly away from the wizard, then daze them so they cannot immediately return to attack range or attack.
- **Damage:** None by default. This is positioning and delay, not a wave-clearing ability.
- **Cast condition:** At least one enemy is in the threat radius and no active Barrier is currently absorbing damage for that wizard.
- **Balance fields:** threat radius, effect radius, knockback, daze duration, cooldown, cast delay, visual scale.
- **Skill-tree scaling:** Wind Burst upgrades increase either knockback distance or daze duration for affected enemies. Daze prevents an affected enemy from moving or attacking for its balance-defined duration; it is applied after the push.

### Fireball

The wizard launches a fireball at the most threatening nearby enemy. On impact, it deals area damage around that enemy.

- **Purpose:** Remove a compact group that has already reached the wizard's immediate defense zone.
- **Targeting:** Select the nearest enemy inside the Fireball threat radius. If enemies are tied, select the one with the lowest health.
- **Effect:** The projectile travels to the selected target. On reaching the target or colliding with a wall, it explodes in an area, damaging enemies inside the explosion radius. It does not damage the warrior, wizard(s), towers, or barricades.
- **Damage role:** Its base damage and area should be tuned to dispatch only close, threatening enemies rather than clear the bulk of the screen.
- **Cast condition:** At least the configured minimum number of enemies are inside the Fireball threat radius, or an enemy in that radius is a boss. Do not cast if no valid target exists.
- **Balance fields:** threat radius, minimum nearby-enemy count, damage, projectile speed, projectile duration, explosion radius, pierce, cooldown, cast delay, visual scale.
- **Skill-tree scaling:** Fireball upgrades increase its explosion damage or explosion radius. It remains a close-defense tool rather than the primary way to clear ordinary waves.

### Barrier

The wizard creates a temporary personal barrier when it is threatened with incoming damage.

- **Purpose:** Prevent a limited amount of damage from reaching that wizard when defenses are breached.
- **Targeting:** Self only; one barrier belongs to one wizard.
- **Effect:** While active, the barrier absorbs incoming damage up to its damage-absorption budget. Damage absorbed by the barrier does not reduce wizard health. Any portion of a hit that exceeds the remaining budget damages the wizard normally. The barrier ends when its budget is exhausted or its duration expires.
- **Damage:** None.
- **Cast condition:** The wizard is about to receive damage, or has at least one enemy within Barrier threat radius; the barrier must not already be active.
- **Balance fields:** damage-absorption budget, duration, threat radius, cooldown, cast delay, visual scale.
- **Skill-tree scaling:** Barrier upgrades increase its damage-absorption budget or reduce its cooldown. Cooldown reduction must stop at a balance-defined minimum cooldown, preventing continuous Barrier casting.

### Lightning Strike

Lightning Strike is a defensive, single-target spell separate from the screen-wide lightning that ends the level. It uses `PixelArtRPGVFXLite/Textures/Electricity` to call down a bolt on a visible enemy.

- **Purpose:** Quickly remove one high-priority enemy that has breached the wizard's defense zone.
- **Targeting:** Select a random visible enemy inside the Lightning Strike threat radius. A boss is valid but receives only the spell's normal single-target damage.
- **Effect:** After a visible targeting and cast delay, a bolt strikes the selected target for direct damage. It does not chain, splash, or damage other enemies or allied entities.
- **Cast condition:** At least one valid enemy is inside the Lightning Strike threat radius. Do not cast when a Barrier, Wind Burst, or Fireball has higher priority and is eligible to resolve the immediate threat.
- **Balance fields:** threat radius, damage, cooldown, minimum cooldown, cast delay, visual scale.
- **Skill-tree scaling:** Lightning Strike upgrades increase direct damage or reduce its cooldown. Cooldown reduction must stop at a balance-defined minimum cooldown, preventing it from becoming a continuous single-target attack.

## Skill-tree relationship

The right-hand skill-tree branch retains the GDD and [Player.md](Player.md) entries for Second Wizard unlock, Wizard health, Wizard armor, and Wizard Barrier unlock. The Barrier unlock enables Barrier at level 1; later levels improve its balance-defined absorption budget, duration, or cooldown.

Add the following right-branch unlocks during CSV skill-tree authoring:

| Node type | Effect | Non-upgrade hooks |
| --- | --- | --- |
| Wizard Wind Burst unlock | Enables Wind Burst auto-casting. Later levels increase balance-defined knockback distance or daze duration. | Uses the wizard's defensive threat rules. |
| Wizard Fireball unlock | Enables Fireball auto-casting. Later levels increase balance-defined damage or explosion radius. | Uses the wizard's defensive threat rules. |
| Wizard Barrier scaling | Improves Barrier's balance-defined damage-absorption budget or reduces its cooldown down to its minimum cooldown. | Barrier remains self-only. |
| Wizard Lightning Strike unlock | Enables Lightning Strike auto-casting. Later levels increase balance-defined single-target damage or reduce its cooldown down to its minimum cooldown. | Uses `PixelArtRPGVFXLite/Textures/Electricity`; Lightning Strike never gains area damage. |

Wind Burst, Fireball, Barrier, and Lightning Strike have independent cooldowns. Any skill-tree scalar must reference a corresponding `balance.csv` row rather than a GDScript constant.

## Implementation handoff

Implement each wizard as a stationary damageable entity with an independent ritual visual and a separate spell visual/effect layer, so defensive casts never stop the ritual presentation. Give every spell an explicit wind-up, resolve, and recovery visual state. Wind Burst and Barrier must resolve around their owner; Fireball must resolve its area damage at the impact point; Lightning Strike must resolve on one target only. Ensure an enemy is affected at most once by a single Wind Burst or Fireball explosion.

Before implementation, add every listed balance field and all wizard health/armor values to `game/data/balance.csv`, using the documented values as the source of truth. Keep all spell damage, cooldown, minimum cooldown, range, area, knockback, daze, barrier, and visual-scale values tunable there.
