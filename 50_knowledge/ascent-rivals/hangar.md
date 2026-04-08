# Ascent Rivals - Hangar

## Related
- [[overview]]
- [[game-design]]
- [[game-client]]
- [[lore]]
- [[design-language]]

## Scope
This note captures the current product direction for the Headquarters Hangar as the player-facing ship cosmetic, unlock, purchase, and equip surface.

## Position In Product
- The Hangar sits within Headquarters rather than existing as a standalone gameplay level.
- The Hangar is where players inspect ship parts, understand unlock requirements, browse compatible cosmetics, purchase eligible cosmetics, and equip owned cosmetics.
- The Hangar is not the place for pre-race gameplay loadout changes during normal matchmaking flow.

## Current Direction

### Parts and progression
- Ship parts are expected to unlock through a long-term progression system.
- Ship parts affect gameplay stats and are therefore not cosmetics.
- The progression system itself is not yet designed in detail.
- Players in the Hangar should still be able to see locked parts.
- Locked parts should expose a short explanation of their unlock requirement directly in the Hangar UI.

### Cosmetics and compatibility
- The Hangar functions as a cosmetic shop as well as an equip/customization surface.
- Cosmetics include ship-part skins and particle-effect treatments.
- Some cosmetics are part-specific and should remain unavailable until the corresponding ship part is unlocked.
- Some cosmetics are expected to be generic across compatible part classes rather than tied to one specific part.
- Example generic categories include engine flare particle effects and warp-boost effects that can apply to multiple compatible parts.

### Ownership and equip flow
- Once a player has unlocked a part, they should be able to browse compatible cosmetics for that part.
- Once a player owns a compatible cosmetic, the Hangar should allow selection and equip from the same surface.
- Shop and equip behavior therefore depends on player state, not only on the cosmetic definition itself.
- Current plan is that players cannot preview cosmetics for a part until that part is unlocked.
- Preview behavior may be revisited later if layout exploration shows strong value in previewing cosmetics on locked parts.

## Player-Visible States
| State | Meaning | Required player-facing information |
|---|---|---|
| Locked part | Player cannot yet use the ship part | Show the part plus a concise unlock requirement |
| Unlocked part, cosmetic not owned | Player can browse compatible cosmetics and buy eligible ones | Show price or source status |
| Owned cosmetic, not equipped | Player owns the cosmetic but is using another option | Show ownership and allow equip |
| Owned cosmetic, equipped | Cosmetic is active on the current ship configuration | Show equipped status clearly |
| Non-purchasable cosmetic | Cosmetic exists but cannot currently be bought | Show the reason it is unavailable |

## Economy Direction
- The shop direction is a dual-currency model with one free currency and one premium currency.
- Initial implementation is expected to support only the free currency.
- The free Hangar currency is **ARC**.
- Not every cosmetic needs to be sold directly through the shop.

## Battle Pass And Time-Limited Sources
- The battle pass is currently planned for cosmetics only, not ship parts.
- Some cosmetics may originate from sources such as a battle pass rather than the base shop inventory.
- During an active battle pass period, those cosmetics should only be obtainable through battle pass progression.
- During that active period, those cosmetics may be visible in the Hangar but not shop-purchasable.
- In that state, the Hangar should explain why the item is unavailable.
- Example messaging: `Tier 5 premium unlock from Starforge battle pass`
- Current direction is that after a battle pass ends there may be an intermediate period where its cosmetics are not obtainable at all.
- During that post-pass unavailable period, unowned items may show source-history messaging rather than a purchase option.
- Example messaging: `Was available from Starforge battle pass 2026`
- Current direction is that at least some past battle pass cosmetics may later become shop-purchasable after that unavailable period ends.
- That post-season resale policy is not yet finalized and should be treated as provisional.

## UX Implications For Layout Exploration
- Locked parts should remain inspectable instead of disappearing from the Hangar.
- Unlock requirements should be presented close to the locked part or cosmetic rather than hidden behind a separate flow.
- The same Hangar route needs to support browse, purchase, preview where allowed, and equip behavior.
- Cosmetic cards or list rows therefore need state treatment for locked, purchasable, owned, equipped, and unavailable cases.
- Unavailable items need explicit reason text when the blocker is not simple currency shortage.

## Open Questions
- What is the authoritative long-term progression model for unlocking parts?
- Are unlocks granted at part-slot, part-family, or individual-part level?
- Which cosmetic categories are generic across compatible parts versus authored per specific part?
- What is the premium Hangar currency called?
- What are the exact rules for battle pass exclusivity, visibility, and post-season resale timing?
