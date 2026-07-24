# Ascent Rivals - Game Client

## Related
- [[overview]]
- [[race-roster-rules]]
- [[accelbyte-game-records]]
- [[eventun/overview|eventun]]
- [[eventun/interface-architecture|eventun-interface-architecture]]
- [[eventun/data-model|eventun-data-model]]
- [[eventun/gauntlet-stage-runtime-contract|gauntlet-stage-runtime-contract]]
- [[website]]
- [[game-design]]
- [[ascent-rivals/initiatives/mmr-v2/mmr-v2-design-and-implementation-plan|mmr-v2-design-and-implementation-plan]]
- [[lore]]
- [[ascent-rivals/initiatives/teams-and-team-gauntlets/teams-solution-design|teams-solution-design]]
- [[ascent-rivals/initiatives/teams-and-team-gauntlets/team-experience-and-progression-solution-design|team-experience-and-progression-solution-design]]
- [[ascent-rivals/initiatives/teams-and-team-gauntlets/team-gauntlets-and-brackets-solution-design|team-gauntlets-and-brackets-solution-design]]

## Role
Primary gameplay execution surface for racing/combat sessions, player experience, and in-session competitive behavior.

## Functional Domains
- client and server runtime gameplay logic
- race, lobby, and session orchestration
- player, ship, loadout, and progression systems
- in-game UI routes and interaction flows
- stats tracking and end-of-match progression handling

## Current Skill Rating Role

- The statistics historically named MMR are not currently used for matchmaking, admission, rewards, qualification, or a public competitive rank.
- The only identified game-runtime consumer is the item recommender. It uses skill rating to choose a recommendation archetype only after uncertainty is below its confidence threshold; otherwise it falls back to career rank.
- The current model family is Weng-Lin Plackett-Luce, but the v1 implementation and accumulated values are not approved for continued use because tie handling, participant selection, asynchronous loading, and persistence can corrupt results.
- [[ascent-rivals/initiatives/mmr-v2/mmr-v2-design-and-implementation-plan|MMR v2]] retains the model family, resets every account to the configured new-player defaults, and limits the initial replacement to authoritative Ascent results for the item recommender.

## Current Identified Telemetry Producer
- Client/local and dedicated-server paths record one complete-match envelope from `MatchStart` through terminal `MatchEnd`, with stable batch/event identities, zero-based producer sequence, and game-build context.
- Both paths call the shared Eventun `ClientServiceIngestMatch` and `ClientServiceCreateMatchArtifact` generated operations; authorization does not create duplicate server-specific APIs.
- The match envelope omits the earlier `SessionStart` event. `MatchStart` records both `raceMode` and the explicit canonical `singlePlayerMode` enum name from the session entity. Time trial therefore emits `raceMode = Classic` and `singlePlayerMode = TimeTrial`; Eventun does not infer play context from race mode.
- Each recorded event receives its UUID and stable sequence when appended to the active match request. The sender remains best-effort/at-most-once and clears the active request before asynchronous dispatch; automatic retransmission is still deferred.
- Global events retain the nonnegative ambient heat supplied by the generated Unreal shape. MatchStart may carry heat 0, and PlayerMatchEnd/MatchEnd may carry the final heat after its boundary; only explicitly heat-scoped event types are constrained to HeatStart/HeatEnd intervals.

## Player Identity UI Terminology
- **Nameplate**: the in-game label shown when viewing another player's name during live gameplay.
- **Player card**: the player identity presentation shown outside live gameplay, including the main menu and career screen.
- Do not use `player card` for the in-session name label, and do not use `nameplate` for the main-menu or career-screen identity surface.

## Current Team And Social Surfaces
- Session player entities carry a team index, and session state carries team identity metadata.
- The dedicated server populates that session identity from Eventun `Player` reads when registering human players, then replicates the resulting team index and team metadata to clients.
- Dedicated-server reads retain their existing `ClientService` operation names. Eventun permits subjectless service tokens on exactly ten reviewed Client reads after a Server `READ` check, while ordinary player callers use those same operations without that custom permission. The generated GameServer view selects those ten reads and the two shared Client writes alongside Eventun's four `ServerService` gauntlet runtime operations; it does not create auth-only API duplicates.
- The reusable player-card path can render team tag, primary color, and team icon. Race-roster rows and ranking/match-summary rows use this team-aware path.
- The minimap defines a green `FriendlyPlayerIconColor`, but current decoration logic uses blue for the spectated racer and red for every other racer. It does not compare team identity, so the friendly color is currently unused.
- `AHGShipEntityRenderer` exposes bounty state to Blueprint, but the reviewed C++ does not own the visible bounty beam or its color. A teammate-specific bounty-beam treatment requires Blueprint/content inspection.
- `HGTeamMenu` and `HGNoTeamMenu` routes exist, but their reviewed C++ implementations are stubs. `HGTeamMenu` has no C++ team behavior, and the Find Team and Create Team handlers in `HGNoTeamMenu` are empty. Blueprint presentation still requires visual verification.
- The game client has no Eventun-backed team subsystem or cached `PlayerMe` team snapshot. The generated Eventun client API already exposes team list/detail/create/update, membership, pending-request, designation, and rank operations.
- Regenerated Eventun client, game-server, and model outputs no longer expose token catalog, token registration/sync, team gate-token, or `token_gated` types. Authored game-client code had no dependency on those retired generated operations. Token gating is unsupported until a provider-neutral asset-source contract is separately designed.
- Menu-side racing-team helpers in `UHGClientLocalPlayerSubsystem` still read AccelByte Groups with configuration code `racing-team` and expose the legacy roles `Member` and `Captain`. This is a second team source that does not match Eventun's canonical team roster, designation, and rank model.
- The next team implementation uses Eventun as the sole game-client team source and removes the legacy AccelByte Groups racing-team path rather than synchronizing both systems.
- The current Eventun team list API returns all teams. Client-side filtering and complete rosters are deliberate for the current small catalog and expected five-to-six-member teams; pagination is deferred until payload measurements justify it.
- `UHGChatSubsystem` queries AccelByte Chat persistent and transient system messages, tracks unread state, creates popups, and marks persistent messages read. `UHGSocialSubsystem` adapts those messages into the existing inbox and popup surfaces. Team notifications still require an Eventun outbox, category/routing policy, and a prototype for typed action payloads such as accepting an invitation.
- Existing party/social code supports retained parties and party invites. A team-roster action may reuse that path through the member's linked AccelByte id, but the teams iteration does not change party approval, automatic membership, friend synchronization, or the party subsystem.
- Career XP is currently player-scoped through AccelByte Statistics, and Battle Pass XP is player-scoped through AccelByte Season Pass. These integrations do not provide authoritative progression for an Eventun-owned team.
- AccelByte Challenges and Achievements are deliberately not used. Eventun's own goal system evaluates the richer gameplay events submitted to Eventun rather than relying on AccelByte stat-code requirements.

## Current Eventun Gauntlet And Challenge Client Support
- `UHGGauntletSubsystem` already caches gauntlets, calendar entries, standings, sponsors, and player gauntlet state.
- The current join flow locates the active public AccelByte session, calls Eventun `GetGauntletStageJoinStatus`, matches the exact `stage_run_id` and `session_id`, and lets `HGPlayRootMenu` join the approved session.
- This is functional player-stage support, not a blank gauntlet-client stub. Team-qualified and mixed-allocation stages still need player/team slot ownership, provisional and locked roster, allocation-label, and team-standing response data and UI states.
- `UHGChallengesSubsystem` already consumes Eventun `MyActiveChallenges` and exposes active challenge snapshots, progress, lanes, and reward previews. Team challenges can reuse its presentation patterns, but Eventun's current progression contracts and storage are player-scoped.

## Current Shoutcasting And Streaming

- Current gauntlet broadcasts are user-operated: a shoutcaster launches the game, joins as a spectator, and streams the running client through their own Twitch channel.
- There is no first-party server-rendered gauntlet stream and no canonical Website/Eventun registry for broadcaster assignment, stream URL, or live status.
- Existing gauntlet-stage design work does not yet provide a complete role-aware spectator/shoutcaster admission contract; the current manual spectator workflow must not be treated as proof that formal stage broadcast admission is solved.
- Website surfaces therefore cannot automatically discover or safely label a gauntlet stream without a later registration, authorization, and status design.

## Sponsor Advertising And Billboard Direction

- Eventun and the current gauntlet form support two advertising-media owners: an associated sponsor entity and the gauntlet itself. Both media-purpose catalogs currently include `Billboard` and `WideBillboard`.
- Current organizer practice commonly uploads campaign-specific billboard artwork directly to the gauntlet instead of creating and associating a reusable sponsor record.
- When building runtime gauntlet data, `UHGGauntletSubsystem` copies associated sponsor `Billboard` and `CourseFlag` media with the sponsor id and tier from that sponsor–gauntlet relationship. It copies gauntlet-owned media with the synthetic sponsor id `Gauntlet` and tier `0`.
- The subsystem also parses `WideBillboard` media into `FHGGauntletData.WideBillboards`, but the reviewed game-client source only populates and sorts that array; no runtime consumer of `WideBillboards` was found.
- `UHGCourseServerSubsystem` populates course advertising from `FHGGauntletData.Billboards`, groups those images by tier and sponsor identifier, balances sponsor/image usage, and respects tier placement limits where possible.
- Ribbon billboard entities require `ImageDefinition.Tileable = true`. That value is parsed from the media metadata; a separate `WideBillboard` purpose is not used for this compatibility decision.
- A sponsor's tier therefore belongs to its relationship with one gauntlet and affects automatic placement only for sponsor-associated assets. It is not a global sponsor rank or stable public presentation hierarchy.
- Current production use is predominantly square billboard artwork. Earlier media-purpose and metadata design anticipated more placement types and possible dimension-based aspect-ratio matching, but that is not an established runtime/content workflow.
- The current automatic billboard handling is expected to receive a separate game-client/content design pass. Direct gauntlet `Billboard` uploads remain the required initial Website workflow because campaign artwork may be unique to one tournament. Website V2 should expose `Tileable` as a purpose-specific control rather than requiring raw metadata editing; its preview only needs to show three adjacent copies of the square artwork.
- Candidate direction includes author-defined advertising locations per course, manual selection from compatible locations, multiple billboard shapes/aspect ratios, trackside placements, vehicle-mounted advertising, and holographic treatments.
- If sponsors later need stable identity beyond billboard assets, a future sponsor–gauntlet campaign model could keep tournament-specific creative and placement choices on the relationship rather than treating one global sponsor asset set as reusable everywhere.
- Organizers may perform manual selection initially. Direct sponsor selection remains only a candidate until sponsor identity, authorization, asset approval, preview, and publication workflows are designed.
- Website V2 should preserve direct gauntlet billboard upload and retain sponsor-entity association as an optional advanced capability, without treating spatial billboard placement as an initial Website requirement. Existing `WideBillboard` records should remain intact at cutover, but new `WideBillboard` authoring should be withheld pending a live-data audit and coordinated cleanup decision.

## Service Relationship
- Consumes competition domain state represented by [[eventun/overview|eventun]].
- Uses service-owned persistent state for competition/accounting concerns instead of treating client runtime as the source of truth.
- Course definitions remain owned by AccelByte session data and game-client course assets. Eventun course sync/admin APIs are backend/admin concerns and should not become game-client course-definition sources.
- Must not treat public AccelByte session visibility as gauntlet join authorization.
- Should call Eventun `GetGauntletStageJoinStatus(gauntlet_id, stage)` before joining a gauntlet stage AccelByte session.
- Should expose gauntlet-stage join only when Eventun returns an advisory joinable status.
- Must treat Eventun preflight as advisory; the dedicated server remains the final admission authority.
- Must treat returned `session_id` as the AccelByte session id.
- Should treat returned `stage_run_id` as Eventun run context, not as a join token.
- Must treat dedicated-server rejection or kick during gauntlet stage admission as a normal competition-rules flow, not just a transport failure.
- Should refresh Eventun-backed gauntlet state after rejection, kick, stage completion, or run completion.
- Can use `run_phase`, accepted/required match counts, and `current_match_id` from join status to distinguish prestart, match-in-progress, between-match, ready-to-complete, and completed stage states.
- Post-match Insights should treat Eventun readiness as bounded and non-blocking. Manual/debug entry may show the no-insights empty state after its timeout window, but automatic pre-summary entry must advance directly to the normal match summary for every non-ready outcome. Late responses must not overwrite a terminal Insights UI state or reopen the Insights route.
- Challenge assignment and progress UI should consume Eventun active challenge APIs, not AccelByte Challenge APIs. The existing game-client challenge subsystem and widgets are the intended presentation seam; Eventun should provide assignment scope, period, progress, and reward-preview data needed by that subsystem.

## Open Questions
- What is the canonical sequence from match completion to externalized competition state updates?
- Which caches are authoritative versus convenience layers for UI responsiveness?
- Which gameplay outputs are required for downstream standings and accounting workflows?
- Which gauntlet-stage rejection and abort reasons should have distinct UX messaging?
- What UI state should represent "between stage matches and rejoinable" for stage runs?
