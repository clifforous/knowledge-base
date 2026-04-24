# Gauntlet Finals And Brackets Research Notes

Date: 2026-04-09

## Related
- [[../../30_designs/ascent-rivals/gauntlet-finals-and-tournament-modes-design-review|gauntlet-finals-and-tournament-modes-design-review]]
- [[../../30_designs/ascent-rivals/gauntlet-stage-orchestration-improvements|gauntlet-stage-orchestration-improvements]]
- [[../../50_knowledge/ascent-rivals/eventun/gauntlet-stage-runtime-contract|gauntlet-stage-runtime-contract]]

## Why this note exists

This note captures the external format research plus the bracket-specific thoughts that were still too light in the main design note.

The goal is to keep the future path for brackets well defined before implementing them.

## Research Summary

## Motorsport pattern: separate individual competition from team qualification

What matters:

- many real racing formats score drivers and teams separately
- the race is still run by individuals, but advancement or title calculations can happen at team level
- some series cap how many cars or results count toward the team total

Why it matters for Ascent Rivals:

- team qualified finals do not require the runtime competition unit to stop being individual racers
- team qualification can be computed from a team aggregate such as `top N` player scores
- admission into the final can still cap the number of active racers from that team

References:

- Formula 1 constructors overview: https://www.formula1.com/en/latest/article/the-beginners-guide-to-the-f1-constructors-championship.66nTfWSqrUYv3bnbosPkHV
- Formula E rules and regulations hub: https://www.fiaformulae.com/en/championship/rules-and-regulations
- FIA WEC regulations hub: https://www.fia.com/Regulations/WEC

## Invitational pattern: materialize the field explicitly

What matters:

- invitation-based events resolve the field before the competition begins
- the runtime event does not depend on a live leaderboard query to decide who belongs
- team invitation and player invitation are both handled as explicit entrants

Why it matters for Ascent Rivals:

- invite-only finals should resolve explicit entrants before the server starts enforcing joins
- bracket rounds should also work this way once the prior round is completed

Reference:

- Race Of Champions overview and event structure: https://www.raceofchampions.com/
- Race Of Champions field announcement example: https://www.raceofchampions.com/post/final-20-driver-field-confirmed-for-roc-sydney-2025

## Esports pattern: qualification, seeding, and bracket execution are separate phases

What matters:

- qualification determines who reaches the tournament phase
- seeding determines where entrants start
- bracket execution then advances entrants through explicit winner and loser paths

Why it matters for Ascent Rivals:

- the dedicated server should not infer the bracket from global standings at join time
- Eventun should resolve entrants for each round and hand that attempt snapshot to the DS
- retries and manual intervention are much easier if the round entrants are materialized explicitly

References:

- ALGS Championship overview: https://algs.ea.com/en/year-4/champs-2025/competition-overview
- VALORANT Champions Paris overview: https://playvalorant.com/en-us/news/esports/everything-you-need-to-know-champions-paris/

## Design implications for Eventun

The most important shared pattern across these examples is this:

- qualification is not the same thing as runtime admission
- seeding is not the same thing as invite storage
- progression is not the same thing as a live filter over all competitors

That leads to the Eventun rule:

- stage config describes how entrants should be selected
- Eventun resolves that into explicit entrants for a specific stage attempt
- the DS only enforces that resolved attempt snapshot

## Bracket path within the current model

## Minimum bracket inputs

For the future bracket builder, the minimum useful inputs are:

- participant type: `player` or `team`
- elimination type: `single_elimination` or `double_elimination`
- initial field size
- seed source

Optional later additions:

- third-place match
- byes policy
- consolation paths
- rematch avoidance
- manual reseeding

Those should stay out of phase one.

## What the bracket builder should output

The bracket system should not only output stages. It should output a bracket skeleton:

- rounds or stages
- each bracket node or match slot
- winner and loser routing
- expected entrant count for each node
- which nodes belong to winners bracket or losers bracket

Manual operators can still set the time for each resulting stage.

That keeps scheduling manual while keeping bracket structure deterministic.

## How opening rounds should work

Opening round entrants can come from any of these selection sources:

- player standings
- team standings
- explicit player invites
- explicit team invites
- open field, though this is weaker for serious tournament play

Once the opening round closes, the selected entrants should be materialized explicitly for that stage attempt.

## How later bracket rounds should work

Later bracket rounds should not re-run qualification logic. They should use `progression`.

That means:

- prior round results are accepted by Eventun
- Eventun advances the right players or teams to the next round
- Eventun materializes the explicit entrants for the next round
- the DS for that next round receives only that explicit entrant snapshot

This is the cleanest way to support:

- retries
- manual repairs
- double elimination
- team brackets
- admin overrides

## Why global win/loss filters are not enough

The existing idea of filtering by required wins and losses is useful as summary state, but not strong enough to be the sole bracket router.

Problems with win/loss-only routing:

- it does not express which exact opponent pairing belongs in the next round
- it becomes ambiguous when multiple lobbies exist for the same round
- it makes retries harder because the system has to reconstruct who belonged in a failed attempt
- it does not handle manual repairs or reseeding cleanly
- it is especially weak for team brackets where the next round is really a team-versus-team assignment problem

Conclusion:

- keep wins and losses as summary or debugging state
- do not use them as the only source of truth for round routing

## Recommended bracket runtime model

The runtime model should be:

- bracket config resolves to explicit round slots
- stage attempt resolves to explicit entrants for a specific slot or shard
- DS fetches the attempt snapshot once and caches it
- Eventun only consumes participation when the round completes successfully

Recommended future tables:

- `gauntlet_bracket`
- `gauntlet_bracket_slot`
- `gauntlet_stage_session_entry`
- optionally `gauntlet_stage_session_player` for team entrant rosters

These names are not final, but the shape matters.

## Captured product decisions from this discussion

These are the current intended rules and should be preserved when brackets are eventually added.

## Participation consumption rule

A player or team is only considered to have competed if:

- the race actually starts
- the attempt reaches accepted completion

This implies:

- joined lobby and left before start: not competed
- server crashed before accepted completion: not competed
- aborted attempt due to insufficient players: not competed
- disconnected mid-race but round completed successfully: competed

## Retry rule

If a bracket attempt fails after allocation but before accepted completion:

- the round should replay with the same explicit entrants
- those entrants should not lose eligibility because the failed attempt did not complete

## Team finals and team brackets rule

For team-based stages:

- qualification may happen at team level
- runtime racing may still happen with individual players
- the DS should enforce `players_per_team` and any ordered member priority supplied by Eventun
- if a higher-priority teammate joins before race start, replacing a lower-priority teammate is acceptable if the policy says so

## Recommended implementation order for brackets

Brackets should not be implemented before the explicit entrant model exists.

Recommended order:

1. finish player invited finals and stage attempt orchestration
2. add explicit team invite management and DS support for team-stage eligibility
3. add team standings resolution with configurable `top N` aggregation
4. add explicit entrant snapshot tables for stage attempts
5. add bracket skeleton generation from participant type, elimination type, field size, and seed source
6. add progression materialization from accepted round results
7. only then let the DS enforce bracket rounds from explicit round entrants

## Practical conclusion

The future bracket path should be:

- author a bracket configuration
- generate bracket structure
- manually schedule the resulting stages
- resolve opening entrants from standings or invites
- resolve later entrants from progression
- enforce only the explicit attempt snapshot at runtime

That keeps the model aligned with how real tournaments are usually run and avoids turning Eventun into a large collection of one-off stage rules.
