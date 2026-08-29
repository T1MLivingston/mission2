# Mission 02 · Spec Check

A single-page, self-contained learning module for 6th grade Computer Science. It **is** the Mission 2
directions — link it from the daily document and students can work it top to bottom without any other handout.

Open `index.html` in a browser. No server, no build step, no internet required except for the web fonts
and the image-export library.

## What the page does

| Stage | What happens |
| --- | --- |
| **01 Start here** | Five step cards, the "done means" chips, and the standards table |
| **02 Build** | Bot name, Student 1–4, and who uploads — then spend a 20-point budget across five color-coded specs, each with its own chief |
| **03 File types** | JPEG / PNG / PDF compared, what Google Drive is, states of data |
| **04 Indexing** | Four lesson cards, the live **Index Lab** (the list is the bot roster: `crew = ["Alpha", "Beta", "Charlie", "Delta", "Echo"]`), a **Slicing lab** with start/stop steppers, and a **Data types** reference (int, float, str, bool, list) |
| **05 Turn it in** | The generated report, PDF/PNG/JPEG export, the exact folder and file names, and two sets of directions — one for every student, one for the organizer |

The header carries the whole team identity: the chassis on the left under **Team leader** with ‹ › arrows to
flip through all 26, and the **Team** dropdown top right. The two are the same choice — picking Team Sierra
swings the banner to Sierra, and arrowing to Sierra sets the team. The call sign also becomes the filename
(`Sierra_Mission2.pdf`), so no two teams can collide.

Under the dropdown, **Team color** is a hex code the team types in — it starts at `#FAE74C`. It accepts
`fae74c`, `#fae74c`, or the three-digit shorthand, turns red on anything else, and keeps the last good value.
The swatch beside it opens the system color picker and fills the code in. That color paints the plate behind
every bot on the page — banner, section chiefs, both labs, the report portrait — plus the band across the top
of the report, so it rides into the downloaded file and survives Save as PDF.

### Section chiefs

The five spec boxes are hosted by the crew from the indexing lesson — Delta on memory, Beta on storage type,
Alpha on capacity, Echo on ports, Charlie on specialty function — so the same five bots students index in
Stage 04 are the ones running Stage 02. The two training stages are hosted by undrafted chassis: Sierra over
file types, Uniform over indexing. Set in `CHIEFS` and the two `data-chief` attributes in the markup, so
reassign them whenever the draft changes.

### How Mission 2 is turned in

One student per team is the **organizer** (set by "Who uploads the file?"). They build the shared folder;
everyone fills their own corner of it:

```
Period3_Sierra              ← organizer makes this, shares it with the team as Editor
 └─ Ada                     ← each student's own first-name folder
     └─ Mission 2 Data      ← that student's three files
         ├─ Ada_Sierra_Mission2.pdf
         ├─ Ada_Sierra_Mission2.png
         └─ Ada_Sierra_Mission2.jpg
```

Every name on that tree is generated live on the page from the team, period, and student, so students copy
rather than invent. When every folder is complete and correctly named, the organizer shares the team folder
with the teacher's account — **the address lives in the daily document, not on this page** — and that share
is the submission. The page says plainly not to share early.

### Progress

Each of the five steps starts in a soft yellow and fills to solid `#FAE74C` with a check when it is finished —
the marker beside the heading, the card in the briefing strip, and the number in the sticky rail all flip
together, and a yellow bar under the rail fills a fifth at a time. A step counts as done when: the team
details are filled in (1), all five parts are picked (2), every file-types question is answered (3), every
indexing question is answered (4), and the report exists with all of Mission Check ticked (5). One definition,
`stageDone()`, drives all of it.

Both pop-up tests live in one **Extra points** round at the very bottom, under the upload directions, with a
running total of points earned. Keeping them together — and last — means the page reads as *learn, then turn
it in, then earn extra* rather than scattering the scoring through the lesson.

**Mission Check** — the end-of-class checklist — lives behind the ✓ button in the sticky rail, not on the page,
so the page itself stays uncluttered. It saves per device, and splits into "everyone" and "organizer only".

The Index Lab's output clears itself every fifth run, so nobody can spam it into a mile-long page.

Correct answers on the two tests earn **build points** (+1 each, capped at 8) that raise the budget in
Stage 02 — so the checks are worth doing before the build is final. Max budget is 28 points against 33 points
of available parts, which keeps the trade-off real: nobody can afford everything.

Progress is saved in the browser's `localStorage` on that device only. Nothing is submitted from the page —
the graded artifact is the one file per team that gets uploaded to Drive. Side quests are not turned in here;
those use the links in the daily document.

The report carries the team name, the bot's name and call sign, its portrait, all four students with the
uploader marked, the five specs with stars, the rank, the training score, and the standards demonstrated.

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
- `CHIEFS` — which chassis hosts each spec box
- `DEFAULT_COLOR` — the starting team color, `#FAE74C`
- `--g1` … `--g5` — the grey spectrum, light to dark, that runs the five spec boxes
- `--num-bg` / `--num-fg` / `--stroke` — the orange-on-blue number chips and the black outline they share
  with the color plates
- `FILE_VAULT` — the easter-egg file type reference
- `STANDARDS` — five benchmarks from the 6th Grade Computer Science Standards Map, tagged by stage;
  they show as chips under each stage heading and print on the student's report. Deliberately five, not
  fifteen — these are the ones this mission actually assesses
- `RANKS` — Bronze / Silver / Gold / Platinum thresholds

## Hosting

Any static host works. For GitHub Pages: **Settings → Pages → Deploy from branch**, pick the branch and
`/ (root)`; the page is then served at the Pages URL and can be linked from the daily document.
