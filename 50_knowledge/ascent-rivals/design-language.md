# Ascent Rivals - Design Language

## Related
- [[overview]]
- [[game-client]]

## Scope
This note captures currently confirmed game-client theme colors and primary font usage.

## Source
- User-provided `HGTheme` C++ constants on 2026-03-19.
- User note on 2026-03-19 that the game client mostly uses Opinion Pro Condensed.

## Typography
- Primary in-client font: Opinion Pro Condensed

## Brand Colors
| Token | Hex | Notes |
|---|---|---|
| `BrandGold` | `#F2A900` | Primary Ascent: Rivals brand gold |
| `BrandDarkBlue` | `#11111F` | Primary Ascent: Rivals brand dark blue |

## General Palette
| Token | Hex |
|---|---|
| `White` | `#E8E4D8` |
| `Black` | `#121216` |
| `Red` | `#C95644` |
| `Orange` | `#D98226` |
| `Yellow` | `#C9B13F` |
| `Green` | `#4F9A68` |
| `Blue` | `#3F74C2` |
| `LightBlue` | `#63B8E8` |
| `Purple` | `#7157A8` |

## Text Colors
| Token | Hex | Notes |
|---|---|---|
| `LightPrimaryText` | `#E8E4D8` | Alias of `White` |
| `LightSecondaryText` | `#B9B3A6` | Secondary text on dark surfaces |
| `DarkPrimaryText` | `#121216` | Alias of `Black` |
| `DarkSecondaryText` | `#35353D` | Secondary text on light surfaces |

## Tier Metals
| Token | Hex | Notes |
|---|---|---|
| `Bronze` | `#CD7F32` | Tier metal |
| `Silver` | `#A2A2A2` | Tier metal |
| `Gold` | `#F2A900` | Alias of `BrandGold` |

## Known Gaps
- Confirm font weights, fallback fonts, and route-specific typography rules.
- Confirm whether any additional client palette tokens exist outside `HGTheme`.
