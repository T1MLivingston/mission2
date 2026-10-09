# MAFIA: Shadows

An online social deduction game for 4 to 15 friends. A few players are the Mafia. Everyone else has to work out who before it's too late.

The whole game is one file: `index.html`.

## Stage 1 (this version)

- Room codes, lobby, ready up, host settings, bots to fill seats
- Seven roles: Citizen, Mafia, Godfather, Detective, Doctor, Sheriff, Jester
- Night, morning story scene, day chat, vote, verdict
- Private Crew chat for the Mafia and a Ghosts chat for eliminated players
- Win check, results screen with a timeline, play again

## Game server

Multiplayer needs a shared database. The game supports two:

- **Firebase (Cloud Firestore).** Paste your web app config into `FIREBASE_CONFIG` near the top of the script in `index.html`. With that filled in, the game works from GitHub Pages and anyone with the link can play.
- **Claude's built-in storage.** Used when `projectId` is empty and the page is opened inside Claude.

With neither, the page loads but Create a room and Join a room stay disabled.

### Firestore rules

```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /rooms/{room} {
      allow read, write: if true;
      match /{sub}/{doc} {
        allow read, write: if true;
      }
    }
  }
}
```

These rules let anyone with the link read and write game rooms, and nothing else. Roles are hidden by the game screen, not by the server, so a technical player could look them up. Fine for friends. Not built for strangers.

## Where the old lesson went

This repo used to hold the Mission 02: Spec Check lesson. That version is saved on the `mission2-lesson-backup` branch.
