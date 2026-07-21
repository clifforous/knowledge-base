# Ascent Rivals Course Leaderboards Page Spec

Date: 2026-04-13
Status: Approved desktop calibration; course mobile validation remains open
Last reviewed: 2026-07-20

## Related
- [[../unified-design]]
- [[../information-architecture]]
- [[../terminal-ops-design-system]]
- [[../tone-and-voice]]
- [[player-profile]]
- [[ascent-rivals/system/competition-runtime-terms|competition-runtime-terms]]
- [[ascent-rivals/system/eventun/api|eventun-api]]
- [[ascent-rivals/system/eventun/data-model|eventun-data-model]]
- [[ascent-rivals/decisions/README#ar-2026-013--course-discovery-and-course-records-use-separate-routes|course route decision]]

## Purpose

Define the IA and page requirements for course-based leaderboards.

This page should help players and followers answer:

- which courses exist
- which players are fastest on each course
- who owns the best lap and best finish records
- where the logged-in player stands
- which leaderboard category is being viewed

## Route

Working route:

- `/courses`
- `/courses/[code]`

Approved route direction:

- use `/courses` for a compact directory of currently published courses;
- use `/courses/[code]` for one course briefing, category leaderboard, record context, and personal placement;
- treat the course code as the stable URL identifier and the display name as mutable presentation data;
- link directly to course detail from the directory, pilot profiles, gauntlets, and global search results;
- do not embed a persistent course selector on the detail route;
- do not add page-local course search, result counts, archive scopes, or cross-course record summaries at the current catalog size;
- use ordinary route navigation, browser history, and optional framework prefetching rather than an in-place course swap or bespoke transition;
- preserve the selected leaderboard category in query state so the exact view is shareable.

Query shape:

- `/courses/{courseCode}?category={category}`

## Audience

Primary:

- players comparing best times
- players trying to improve on a specific course
- followers checking who owns course records

Secondary:

- gauntlet organizers
- teams
- sponsors
- press/community viewers

## Page Goals

- make course discovery and detail navigation clear
- make leaderboard category selection clear
- foreground best lap and best finish records
- show personal placement for logged-in users where available
- connect course competition to player profiles
- keep course metadata and lore available without overwhelming the stat task
- avoid confusing course runtime heats/laps with gauntlet qualifiers

## Current V1 Data Availability

Foundation readiness note (updated 2026-07-20): Eventun serves current course records and player ranks from incremental projections. The production-scale local cutover and retained-data smoke passed, while shared-development and production cutovers remain pending. Website V2 launch use requires deployed production behavior.

### Course metadata

Authoritative in AccelByte Cloud Save `Courses`:

- course code
- display name
- planet
- description
- difficulty
- heats
- laps
- feature state and the configured production-ready feature state
- other course configuration

Currently exposed through the Eventun public course read:

- course code
- display name
- planet
- description
- difficulty
- heats
- laps
- derived active state
- media

Source authority:

- AccelByte Cloud Save `Courses`

Current Website API access path:

- `GET /v1/course`, backed by Eventun's controlled cache of the AccelByte record

Contract caution:

- the current public response exposes only a derived `active` boolean rather than the source feature state;
- it returns inactive rows as well as active rows;
- that boolean is not sufficient to distinguish a previously public archived course from alpha, internal, or otherwise unreleased content.

Terminology note:

- course `heats` and `laps` describe course/match runtime settings
- they are not gauntlet qualifiers

### Course Visibility and Archive Policy

Approved public behavior:

- show only production-ready courses on `/courses` and in public global search;
- do not show publication-state labels or an archived-course filter in the initial directory;
- keep explicitly archived course detail pages and historical records accessible through direct
  links only if the eventual public projection deliberately supports that state;
- treat archived-course browsing as a later requirement rather than inventing it for a catalog
  that is not expected to retire courses frequently.

Visibility guardrails:

- AccelByte feature state is authoritative; Website V2 must not treat the Eventun course table as the owner of publication state;
- `Prod` is the currently documented officially released state, but consumers should honor the configured enabled feature state rather than hard-code that string;
- alpha, internal, and other unreleased courses must not appear in anonymous directories, global search, metadata, sitemaps, or deep-link responses;
- do not classify every `active = false` course as archived, because the current derived boolean collapses retired and unreleased states;
- classify a course as `published` when its AccelByte feature state matches the configured enabled/production-ready state and it is not marked archived;
- classify a course as `archived` only when an explicit AccelByte course-metadata marker asserts that the previously public course was deliberately retired;
- classify alpha, internal, disabled, unknown, incomplete, conflicting, and otherwise unreleased configurations as `hidden`;
- fail closed: `hidden` is an internal classification and must not be serialized by a public Website read or distinguished from a missing course through the public detail route.

Website-facing API requirement:

- derive visibility on the server from AccelByte source metadata or a controlled cache of that metadata;
- expose only the stable public values `published` and, when deliberately supported for
  historical deep links, `archived`;
- return only published courses in directory and global-search collections;
- return not found for hidden/unreleased course detail requests;
- feed directories, global search, page metadata, canonical links, and sitemaps from the same public-safe projection;
- do not use the current unfiltered `GET /v1/course` response directly unless it is revised to enforce this boundary; a purpose-built Website read is acceptable.

### Top leaderboard entries

Available:

- top leaderboard entries grouped by course
- category-specific arrays
- player id
- player name
- player avatar URL
- rank
- time in milliseconds
- loadout value

Source:

- `GET /v1/leaderboard?limit={n}`

Categories:

- `clientFinish`
- `clientLap`
- `clientLowCostFinish`
- `clientLowCostLap`
- `clientHighCostFinish`
- `clientHighCostLap`
- `serverFinish`
- `serverLap`

### Player-specific leaderboard placement

Available:

- player-specific leaderboard placement by course and category
- rank
- time in milliseconds

Source:

- `GET /v1/leaderboard/player/{playerId}`

V1 usage:

- show the logged-in user's placement when they are viewing course leaderboards
- show placements on player profiles when viewing a player

### Player profile linking

Available:

- leaderboard rows include player id/name/avatar

V1 usage:

- each row should link to `/players/[id]`

## Category Model

The raw API categories should be presented in player-readable groups.

Player-facing groups and internal mappings:

| Group | Player-facing category | Eventun field |
|---|---|---|
| Race | `Race Finish` | `serverFinish` |
| Race | `Race Lap` | `serverLap` |
| Time Trial | `Time Trial Finish` | `clientFinish` |
| Time Trial | `Time Trial Lap` | `clientLap` |
| Time Trial / Loadout Class | `3K Class Finish` | `clientLowCostFinish` |
| Time Trial / Loadout Class | `3K Class Lap` | `clientLowCostLap` |
| Time Trial / Loadout Class | `10K Class Finish` | `clientHighCostFinish` |
| Time Trial / Loadout Class | `10K Class Lap` | `clientHighCostLap` |

Default category:

- `Race Finish`

Design guardrail:

- do not show all eight categories as eight full tables at once
- use accessible tabs or segmented controls with ordinary player-facing labels; command-like text may be secondary decoration but not the only label
- keep the current route's course and selected category obvious at all times
- preserve the selected category in the shareable URL query state
- if `Race Finish` has no entries, show its honest empty state and make the other categories easy to select; do not silently substitute a different category
- keep Eventun source selection and validation policy internal; public copy should describe race and time-trial contexts, not server/client implementation or relative trust

Loadout-class explanation:

- `3K Class` means a time-trial record set with a total loadout value of 3,000 or less;
- `10K Class` means a time-trial record set with a total loadout value of 10,000 or less;
- show this concise threshold explanation in help text or the category control, not in every leaderboard row;
- the Eventun thresholds are inclusive, and the Website V2 labels must preserve that meaning.

### Race-Mode Scope

`Race` is the public umbrella for records produced in race sessions. It is not a synonym for one specific race mode.

Current product context:

- nearly all current races use Ascent Mode;
- after podium positions are secured, the remaining racers enter the ascension phase and must reach the designated zone without being eliminated;
- Classic Race and Deathmatch Race exist but are rarely used;
- Website V2 may foreground Ascent Mode in gameplay explanation without presenting all three modes as equal navigation choices.

Current data constraint:

- Eventun's course-record projection is not keyed by race mode;
- the initial `Race Finish` and `Race Lap` boards can therefore contain eligible records from more than one race mode;
- do not label those boards `Ascent` or `Ascension` unless Eventun first exposes mode-scoped records and ranks.

Future direction:

- consider an explicit race-mode selector when mode-scoped leaderboard contracts exist;
- prioritize Ascent Mode in that selector while preserving Classic and Deathmatch for historical and future use;
- preserve the selected mode in shareable query state once the filter is supported.

## V1 Page Structure

The directory and detail are separate compositions.

Directory priority:

1. command header and route context;
2. complete published-course collection;
3. compact footer.

Detail priority:

1. course identity and factual briefing;
2. selected category controls;
3. current record and top-five gap context;
4. logged-in personal placement when available;
5. exact leaderboard table.

## Visualization Direction

The leaderboard table remains canonical for exact rank, pilot, time, and loadout values. Charts supplement it only when they answer a different question.

Candidate initial visualization:

- a compact horizontal time-gap view for the selected course and category;
- anchor every bar to the winning time and label the exact delta;
- use only the returned top-N population and label it as top-N, not as a distribution or percentile;
- keep the exact leaderboard table adjacent or immediately available;
- do not combine finish and lap values or values from different courses on one quantitative scale.

Conditional visualization:

- a checkpoint-route trace is useful when the game exports approved checkpoint geometry through a stable website contract;
- without that contract, use course identity, factual metadata, current approved captures, and record summaries rather than invented geometry.

Deferred until new Eventun contracts exist:

- whole-population distributions and percentiles;
- historical record-progression timelines;
- checkpoint or sector performance comparisons.

## 1. Course Directory

Purpose:

- let a visitor scan the current published-course catalog and open one canonical detail route.

Approved desktop composition:

- one restrained `/courses` command header;
- a two-column collection of uniform, lightly seamed course entries;
- course name, planet or location when available, difficulty, and default laps;
- one approved image or image-neutral signal fallback that does not invent a course map,
  checkpoint trace, planet illustration, gameplay capture, or live telemetry;
- a whole-entry link to `/courses/[code]` with the approved directional-chevron affordance.

Directory guardrails:

- render only published courses;
- do not repeat `Published` on every entry;
- do not show record times, ranks, leaderboard categories, or cross-course comparison metrics;
- do not add a page-local search, result count, archived scope, sort control, pagination, or
  selected-course state at the current catalog size;
- use the persistent global search for direct course discovery;
- use one entry silhouette and one internal layout across the collection.

The no-course and failed-directory states remain required implementation states. The reviewed
default calibration does not retain a hidden search-specific empty state.

## 2. Course Record Command Header

Purpose:

- establish `/courses/[code]` as one canonical course record surface.

Content:

- breadcrumb linking `Courses` back to `/courses`;
- `Course Records` title and current course name;
- concise explanation that the route shows record times and pilot placement by race or
  time-trial category;
- no selected-category repetition, selector, or search control in the header.

Terminal Ops components:

- `HeroBriefing`
- `PathBar`

## 3. Selected Course Briefing

Purpose:

- orient the user before the table

Content:

- course name
- planet
- description
- difficulty
- media
- default laps

Do not show default heats in the public course briefing. Heat count belongs to the configured
race or gauntlet context rather than this stable course identity summary.

Optional later:

- course lore excerpt
- planet link
- course hazards
- gauntlets currently using the course

## 4. Category Filter

Purpose:

- let users switch leaderboard types without losing course context

Recommended initial categories:

- Race Finish
- Race Lap
- Time Trial Finish
- Time Trial Lap
- 3K Class Finish
- 3K Class Lap
- 10K Class Finish
- 10K Class Lap

Design guidance:

- use concise labels in the UI
- present `Race` and `Time Trial` as the primary context, then `Finish` and `Lap` as the measure;
- expose `Open`, `3K Class`, and `10K Class` only when `Time Trial` is selected;
- do not render the eight semantic combinations as eight equal top-level tabs
- use player-facing context copy such as `Best times set in races` and `Best times set in time trial` only when helper text is needed
- explain `3K Class` as `Loadout value: 3,000 or less` and `10K Class` as `Loadout value: 10,000 or less`
- do not expose server/client authority, event submission, validation, or anti-cheat implementation details in public copy
- preserve selected category in URL query

## 5. Record Context and Leaderboard Table

Purpose:

- show the current record, the bounded top-five gap-to-record comparison, and the exact top
  performers for the selected course/category.

Columns:

- rank
- player
- time
- loadout value
- team, if the row or related player data supports it later

Row actions:

- open player profile
- compare to logged-in player's time, later

Display guidance:

- time should be the visual anchor
- show loadout value as a compact secondary column on desktop for every category; it records the run conditions and explains the ordering of otherwise equal times
- give loadout value stronger category context on `3K Class` and `10K Class` boards because it determines class eligibility
- on mobile, keep loadout value visible in the primary row for `3K Class` and `10K Class`; move it into accessible row details for ordinary Race and Time Trial boards
- top ranks can receive stronger framing
- do not over-decorate every row
- preserve scan clarity over lore styling

Terminal Ops components:

- `DataTable`
- `RankPill`
- `PilotIdentityCell`
- `TelemetryValue`

Progressive reveal:

- start with 10 rows from one already-fetched bounded collection of 50;
- `Show 10 more` appends the next ten locally, updates the natural-number shown count, and hides
  when complete;
- preserve scroll position and do not add server pagination for this initial bounded board.

## 6. Personal Placement Strip

Only when the user is logged in and player placement data is available.

Purpose:

- show "where am I?" without requiring the player to find themselves in the top-N table

Content:

- user's rank
- user's best time
- delta to top time if derivable client-side from table data
- selected course/category

Source:

- `GET /v1/leaderboard/player/{playerId}`

Tone examples:

- `Pilot placement acquired`
- `No registered time for this course/category`

Guardrail:

- do not expose private ELO or rating here

## 7. Related Context

Optional V1/later content:

- active/upcoming gauntlets using this course
- planet/lore link
- course media
- related VODs or watch links
- ship part/loadout notes later

V1 caution:

- keep this secondary
- do not block leaderboard usability on lore/content completeness

## Auth and Permission States

| State | Behavior |
|---|---|
| Anonymous | can view the course directory and any public course detail, selected leaderboard, course metadata, and player profile links |
| Logged-in player | same plus personal placement strip when player leaderboard data is available |
| Admin | same as logged-in; no special admin actions required for V1 unless course administration is added later |

## Empty / Loading / Error States

Required states:

- no courses
- no production-ready courses
- no leaderboard entries for selected course/category
- logged-in player has no time for selected course/category
- failed course fetch
- failed leaderboard fetch
- failed player-placement fetch
- course media missing

Tone:

- `No course records detected.`
- `No registered time for this category.`
- `Course manifest unavailable.`
- `Timing board sync failed.`

Guardrail:

- missing data should not imply the player has a zero or poor result

## Responsive Behavior

Desktop:

- selected course briefing and leaderboard table should be visible without excessive scrolling
- course directory uses the reviewed two-column collection
- category filter can be tabs or segmented controls

Tablet:

- reduce the directory to one or two columns according to available width
- preserve rank, player, and time columns

Mobile:

- stack modules
- keep login/avatar visible in top bar
- stack directory entries without adding a course dropdown to the detail page
- table can horizontal-scroll or convert to rank cards
- preserve rank, player, time, and category
- validate the exact directory and detail composition in the next Pencil checkpoint

## SEO and Sharing

The course index should support:

- title: `Courses - Ascent Rivals`
- description focused on available courses and their record pages
- canonical `/courses` URL

Each course detail should support:

- title: `{Course Name} {Category} Leaderboard - Ascent Rivals`
- description using course, planet, and leaderboard category
- canonical `/courses/[code]` URL;
- shareable category query state without generating conflicting canonicals for every filter combination.

Do not expose private player status in metadata.

## V2 Candidate Data Needs

These ideas are valuable but should not block V1:

- season filters
- gauntlet/event filters
- race-mode-scoped records, ranks, and filtering
- team filters
- ship part/loadout filters
- deltas between player and world record
- percentile placement
- checkpoint/split breakdowns
- course hazard/lore modules
- planet/manufacturer relationship modules
- VODs or run recaps

## Terminology Guardrails

- `Lap` is a course/match runtime concept.
- `Finish Time` is the total time for the relevant run/match category.
- `Race` is the public context label for records produced in race sessions; it does not imply ranked matchmaking.
- `Ascent Mode` is the dominant current race mode, while `Classic Race` and `Deathmatch Race` remain supported concepts.
- Do not imply that the initial `Race` leaderboard is Ascent-only while the Eventun record contract remains mode-agnostic.
- `Time Trial` is the public context label for time-trial records.
- `3K Class` and `10K Class` are inclusive time-trial loadout-value caps, not divisions of pilot skill.
- Do not use `Official`, `Server`, `Client`, `Authoritative`, or `Verified` as public leaderboard-category labels.
- `Heat` is a match-internal runtime round.
- `Qualifier` is a gauntlet/tournament window.
- Do not call leaderboard categories qualifiers.
- Do not call course heats qualifier rounds.

## Next Steps

- Validate the directory and detail routes at mobile width without reintroducing an embedded
  selector.
- Review implementation-facing loading, empty, error, stale, and partial-data states.
