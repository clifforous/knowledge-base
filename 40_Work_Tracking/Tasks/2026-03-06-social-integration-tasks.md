# 2026-03-06 Social Integration Tasks

## Active Tasks (Required Now)
- [x] Implement core friends flow: invite, accept, reject.
- [x] Implement core party flow for group matchmaking.
- [x] Separate friend sources in Social UI: Ascent Rivals friends vs platform friends.
- [x] Scope platform support to Steam for this phase.
- [x] Add party status widget in the client route host near matchmaking state.
- [x] Enforce party leader control of matchmaking start.
- [x] Disable/lock matchmaking actions for non-leader party members.
- [x] Add clear visual queue state for non-leader members when leader starts matchmaking.
- [x] Add party management actions: promote leader, disband party, kick member (leader), leave party.
- [x] Add friend request indicator badge support on social-related icon buttons.
- [x] Replace profile friend-code-only action with an Add Friend button that opens the Social add flow prefilled from profile context.
- [x] Validate end-to-end behavior in dev standalone mode with Steam login.
- [x] Review platform service docs for friends, parties, and invites; prefer OSS path unless blocked.

## Discovery Tasks
- [x] Determine source of Recent Players list.
- [x] Compare using match history from event service versus platform session history from OSS.
- [x] If needed, define an event service API for Recent Players.

## Deferred (Low Priority)
- [x] Make social widgets fully gamepad navigable.

## Clarified Decisions
1. Required now: Friends and Party.
2. Platform scope now: Steam only.
3. Recent Players source: unresolved, requires evaluation.
4. Matchmaking authority: party leader starts queue; non-leader players must receive clear visual queue state.
5. Profile integration: Add Friend from profile should carry friend context into Social add flow for confirm.

## Carryover Notes
- Teams work remains separate.
- Social route remains primary surface for party/friends interactions.

## Friend Panel
- Let user navigate to the friend Panel and select each row
- Four collasible groups (row selectable to collapse it)
  - Friend Requests
    - Sort by request time oldest first
    - On Row Select Show the following
      - Accept
      - Ignore
      - Block
  - Friends
    - Sort in-game friends, online friends, then offline friends with alphabetical sort secondary
    - On Row select show the following
      - Invite to Game - Only if they are not in party already and Online
      - Join Party - Only if they have room in their party and their party is "Open to friends"
      - Unlink Friend - needs a confirmation dialog
  - Platform Friends 
    - Only show online platform friends
    - Sort in-game friends to the top secondary sort alphabetically
    - On Row select show the following
      - Connect To Ascent
      - Invite to Game - Only if the friend is not in party already
      - Join Party - Only if they have room in their party and their party is "Open to friends"
  - Recent
    - Sort by recent player then alphabetically
    - On Row select option to "Send Friend Request"
- Global Options
  - Add Friend By Friend Code
- On Row select of any player
  - Go To Profile Button

## Party Panel
- For now fixed size lets say 4 but may adjust
- Global Options
  - Leave Party - If not party leader
  - Disband Party - If party leader
- On Row select show the following
  - Promote to leader - If you are leader and you haven't selected yourself
  - Kick from party - If you are the leader and you haven't selected yourself
  
## Party Status
- Show "In a party of #" in the matchaking status area (even if not matchmaking)
- Clicking it should take you to the party view if you aren't already there

## Notifications
- Somebody Left the party
- Somebody Joined the party
- Leader disbanded the party
- Friend Request Received

## Some Notes
- Add padding to the left of friend icon on friends/party view
- The accept button just says "TEXT" in the party invite notification
- Make the view profile button use a thumbstick down instead of a bumper
- Add the recent players section to the social page
- Make the friend code unfocusable 
- Matchmaking pool name doesn't need to be shown when queuing
- My local queue didn't show the (x/y) players but stevens did
- The "In Menus, In Party" should be iconified.
