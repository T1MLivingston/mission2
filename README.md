# Mafia: Shadows

A multiplayer game of secrets for 4 to 15 players. A few players are secretly the Mafia; everyone else has
to work out who before it's too late.

The whole game is one file, `index.html`.

## How a game runs

1. One player creates a room and shares its 4-letter code. Others open the same page and join with it.
2. The host can add bots to fill seats and sets the timers, whether roles are revealed when someone is out,
   and how tied votes are broken.
3. Each round has a **night** (the Mafia picks a target; the Doctor, Detective and Sheriff act), a
   **dawn** report, a **day** of discussion in the Town chat, and a **vote**.
4. The Town wins when every Mafia member is out. The Mafia wins when it matches or outnumbers everyone
   else. The Jester wins on their own by getting voted out.

| Role | Team | Night move |
| --- | --- | --- |
| Citizen | Town | None |
| Detective | Town | Learns one player's role (the Godfather reads as Citizen) |
| Doctor | Town | Protects one player; not the same one two nights in a row |
| Sheriff | Town | Learns if one player seems suspicious (Jester yes, Godfather no) |
| Mafia | Mafia | Votes with the crew on a target |
| Godfather | Mafia | Votes with the crew and breaks ties |
| Jester | On their own | None |

## Hosting

The game keeps rooms, players and chat in shared storage provided by `window.claude.use('db')`, so it has
to run as a published Claude Artifact with the `db` capability. Opened anywhere else (a static host, a local
file) it loads, but Create and Join stay disabled and the page says it can't reach its shared storage.
