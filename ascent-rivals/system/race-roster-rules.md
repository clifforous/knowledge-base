# Ascent Rivals - Race Roster Rules

## Related
- [[game-client]]
- [[ascent-rivals/archive/initiatives/reconnect-state-restoration/reconnect-state-restoration-initial-implementation-plan-2026-04-29|historical reconnect implementation plan]]

## Status
This document defines the implemented behavior for ordinary multiplayer, multi-heat races. Gauntlet- and finals-specific roster policies are deferred.

## Core Rule
A heat roster is frozen when the heat starts. Racers may disconnect or reconnect, but ordinary players and bots are not added to, removed from, or substituted into that roster until the heat ends unless `LateJoinersMustSpectate` is explicitly disabled. Disabling that setting enables immediate human-for-bot replacement as a configured exception.

## Heat Rosters And Bot Backfill
- At each heat boundary, connected eligible humans receive racer seats first.
- Ordinary backfill bots fill the remaining seats up to the configured racer limit. With a limit of 16 and backfill enabled, every heat should start with exactly 16 racers.
- Humans waiting as temporary spectators do not count as current-heat racers, although they still consume connection/session capacity.
- When one or more humans are ready for the next heat, remove exactly as many ordinary backfill bots as needed. Multiple joins are reconciled together so the racer count never exceeds the limit.
- Bots own their own loadout, stats, ARC, and heat result. A normal backfill bot never inherits a disconnected human's state or races on that human's behalf.
- A true substitute bot or AI takeover is a separate feature and is not part of these rules.
- Editor-only manual bot injection is a debug exception and may intentionally alter an active heat roster. Production automatic backfill still occurs only at heat boundaries.

## New Players
- With `LateJoinersMustSpectate` enabled, a new player who joins during a heat spectates for the rest of that heat, even if a bot is currently occupying the future seat.
- In that mode, the active bot completes the heat and remains on that heat's scoreboard and heat summary. At the next heat boundary, the waiting human receives priority over an ordinary backfill bot and starts from the normal starting line.
- With `LateJoinersMustSpectate` disabled, an ordinary late joiner becomes a racer immediately. If the racer limit is full and a bot is active, one bot is removed and the human takes the available racer seat for the current heat.
- Immediate replacement does not transfer the bot's progress, placement, stats, loadout, or ARC. The removed bot is discarded from the current heat's scoreboard and result, while the human starts with their own state and is committed to that heat.
- Gameplay telemetry the bot emitted before removal remains an immutable record, but the bot produces no heat-end result for the replaced heat.
- Historical heat results produced by that bot in earlier heats remain unchanged.
- A late joiner receives the passive ARC baseline appropriate for the heat in which they first become a racer.

## Disconnect And Reconnect
- A racer who disconnects remains a participant in the heat they started. No bot replaces them during that heat.
- While the same-heat reservation remains valid, their TAB row stays visible and greyed out. Their progress is frozen, so their provisional placement drops naturally as connected racers pass them.
- Same-heat reconnect behavior follows the configured reconnect mode. Checkpoint respawn is allowed only because the player was already on that heat's frozen roster; temp-spectator and reject modes wait until a later heat.
- Reconnect snapshots preserve restorable race progress but do not preserve a computed placement. A returning racer is briefly unplaced at the bottom of the live board, then the normal authoritative placement pass recomputes their rank from restored progress alongside every other racer.
- If the player is still absent when the next heat roster is frozen, an ordinary bot may fill that heat's racer seat. The human is not a participant in that heat.
- A player who reconnects during a heat they did not start spectates until the next heat, then receives priority over an ordinary backfill bot.
- An active seat reservation protects the human's right to return in a future heat. It does not prevent a bot from temporarily filling a heat while the human is absent.
- When the reservation expires, the human loses the guaranteed future seat. Rejoining is then handled as an ordinary late join.
- A disconnected racer receives no result or circuit points for a heat they did not start. When they later return as a racer, passive ARC for missed heat baselines is applied once so they are not economically behind an equivalent new late joiner; previously earned or spent ARC remains part of their restored balance.

## Scoreboards And Results
- The in-race TAB scoreboard shows only racers committed to the current heat. Normally this is the frozen heat-start roster; immediate replacement mode swaps the removed bot out and commits the late-joining human.
- Current TAB identity, avatar, team, stats, and placement come from the stable participant row. A live racer entity may supply transient presentation details such as local-player state and ping, but reuse of a SnapNet player index must never transfer the previous entity's identity to the new participant.
- A heat summary shows only racers committed to that heat, including racers who disconnected during it. A bot removed by immediate replacement has no result for that heat, and the replacing human does.
- A racer who disconnects before producing an eligible heat result becomes DNF and unplaced when the heat is finalized. The historical row remains visible, but it receives no new circuit points.
- A result completed before a later disconnect remains valid.
- The match summary is built from the final heat's committed roster, not every participant who appeared earlier in the match.
- A final-heat DNF remains visible on the match summary but has no numbered final placement and receives no placement award. Eligible placements must remain unique and contiguous.
- In timed modes such as Ascent, an eligible result does not require crossing a traditional finish line. A racer still active when the authoritative heat timer ends can receive the normal ranked result.
- Spectators, shoutcasters, and temporary spectators never appear as racers on TAB, heat summaries, or the match summary.
- Lobby presentation uses live lobby/session players. Historical participant rows must not make absent players appear as dimmed lobby entries.
- Previous-heat summaries use immutable participant heat-result rows, and the overall match summary uses finalized participant standings. Live entity-cache replacement and current TAB decoration must not rewrite those historical identities or results.

## Example
1. A human starts Heat 1, disconnects, and does not return before Heat 2 starts. Their Heat 1 row remains and finalizes as DNF if they did not complete an eligible result.
2. A normal bot starts Heat 2 in the open racer slot. The human reconnects during Heat 2 and spectates; the bot owns the Heat 2 result.
3. At the Heat 3 boundary, the human replaces an ordinary backfill bot, receives the appropriate missed-heat passive ARC adjustment, and starts Heat 3 from the starting line.
4. If `LateJoinersMustSpectate` were disabled instead, the human would immediately replace a bot in Heat 2; the bot would disappear from Heat 2 results and the human would own the remaining Heat 2 participation.
