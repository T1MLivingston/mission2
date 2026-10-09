# MAFIA: Shadows

An online social deduction game for 4 to 15 friends. A few players are the Mafia. Everyone else has to work out who before it's too late.

The whole game is one file: `index.html`.

## Stage 1 (this version)

- Room codes, lobby, ready up, host settings, bots to fill seats
- Seven roles: Citizen, Mafia, Godfather, Detective, Doctor, Sheriff, Jester
- Night, morning story scene, day chat, vote, verdict
- Private Crew chat for the Mafia and a Ghosts chat for eliminated players
- Win check, results screen with a timeline, play again

## Known limit

Multiplayer uses Claude's built-in artifact storage. That storage only exists when the page is opened inside Claude. On GitHub Pages the page loads, but Create a room and Join a room stay disabled. Moving the storage to a hosted database (Firebase is the plan) fixes this.

## Where the old lesson went

This repo used to hold the Mission 02: Spec Check lesson. That version is saved on the `mission2-lesson-backup` branch.
