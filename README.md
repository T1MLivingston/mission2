# Mission 02 · Spec Check

A single-page, self-contained learning module for 6th grade Computer Science. It **is** the Mission 2
directions — link it from the daily document and students can work it top to bottom without any other handout.

Open `index.html` in a browser. No server, no build step, no internet required except for the web fonts
and the image-export library.

## What the page does

| Step | What happens |
| --- | --- |
| **1 Start here** | The four step cards, the team form — team, bot, period, Students 1–4, who uploads — and the skills list |
| **2 Build** | A 20-point budget across five spec boxes, each hosted by one of the crew bots |
| **2.5 Extra points** | File types (JPEG/PNG/PDF + Drive), Python indexing (Index Lab, Slicing lab, index math, Data types), and both pop-up checks |
| **3 Turn it in** | The report, PDF/PNG/JPEG export, the exact folder and file names, and two sets of directions — one for every student, one for the organizer |

Three steps carry the mission. 2.5 sits between 2 and 3 because the points it pays out get spent back in 2.

## How Mission 2 is turned in

One student is the **organizer** — Student 1 unless the team swaps it. They build the folder and share it with
the team as Editor; everyone then fills their own corner of it. The naming panel draws the whole thing live
from the team, period, and crew names, so nobody has to invent a name:

```
Period1_India                    ← the organizer makes this
 ├─ Student1_Ada                 ← one folder per student
 │    Ada_India_Mission2.pdf
 │    Ada_India_Mission2.png
 │    Ada_India_Mission2.jpg
 ├─ Student2_Ben
 │    ...
```

Each student uploads their own three files into their own folder. When it is all there and correctly named,
the organizer copies the team folder's share link and pastes it into the class **spreadsheet** — that
spreadsheet lives in the daily document, not on this page. The link is the hand-in.

**Mission Check** — the end-of-class checklist — lives behind the ✓ button in the sticky rail, not on the page,
so the page itself stays uncluttered. It saves per device, and splits into "everyone" and "organizer only".

The Index Lab's output clears itself every fifth run, so nobody can spam it into a mile-long page.

Correct answers in Step 2.5 earn **build points** (+1 each, capped at 8) that raise the budget in Step 2. Max
budget is 28 points against 33 points of available parts, which keeps the trade-off real: nobody can afford
everything.

Progress is saved in the browser's `localStorage` on that device only. Nothing is submitted from the page.
Side quests are not turned in here either; those use the links in the daily document.

The report carries the team name, the bot's name and call sign, its portrait, all four students with the
uploader marked, the five specs with stars, the rank, the training score, and the skills demonstrated.

## The bots

26 chassis, one per call sign (Alpha → Zulu), used for team selection, the masthead, and the report portrait.

- `assets/bots/original/` — the full-resolution source art
- `assets/bots/web/` — 320px grayscale copies used on the page
- The web copies are **inlined into `index.html` as data URIs**, which is why the page is one file that still
  works from a Chromebook's Downloads folder with no assets folder next to it.
- They keep their **transparent background** on purpose — the team's chosen color is painted behind them.

To change or add art, drop PNGs into `assets/bots/original/`, update the `BOTS` array in `index.html`
to match the filenames, and run:

```
python3 tools/build-bots.py     # needs pillow: pip install pillow
```

That regenerates `assets/bots/web/` and rewrites the `BOT_IMG` block between the `/* BOT_IMG_START */`
and `/* BOT_IMG_END */` markers.

## Editing the content

Everything a teacher would want to change sits in named arrays at the top of the `<script>` block:

- `CATEGORIES` — the build options, their point costs, and star ratings
- `BASE_BUDGET` / `CREDIT_CAP` — the 20-point budget and the 8-credit cap
- `PY_QUESTIONS` / `FD_QUESTIONS` — the two tests (prompt, options, correct index, explanation)
- `CREW` — the five bots used in the indexing lesson and lab
- `CHIEFS` — which chassis hosts each spec box, plus its job title and one-line story
- `DEFAULT_COLOR` — the starting team color, `#FAE74C`
- `--g1` … `--g5` — the grey spectrum, light to dark, that runs the five spec boxes
- `--num-bg` / `--num-fg` / `--stroke` — the orange-on-blue number chips and the black outline they share
  with the color plates
- `FILE_VAULT` — the easter-egg file type reference
- `STANDARDS` — five plain-language skills, listed in Step 1 and printed on the report
- `RANKS` — Bronze / Silver / Gold / Platinum thresholds

## Hosting

Any static host works. For GitHub Pages: **Settings → Pages → Deploy from branch**, pick the branch and
`/ (root)`; the page is then served at the Pages URL and can be linked from the daily document.
