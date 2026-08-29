# Mission 02 · Spec Check

A single-page, self-contained learning module for 6th grade Computer Science. It **is** the Mission 2
directions — link it from the daily document and students can work it top to bottom without any other handout.

Open `index.html` in a browser. No server, no build step, no internet required except for the web fonts
and the image-export library.

## What the page does

| Stage | What happens |
| --- | --- |
| **01 Start here** | Five step cards, the "done means" chips, and the standards table |
| **02 Build** | Bot name, Student 1–4, and who uploads — then spend a 20-point budget across five color-coded specs |
| **03 File types** | JPEG / PNG / PDF compared, what Google Drive is, states of data, then an 8-question pop-up test |
| **04 Indexing** | Four lesson cards, the live **Index Lab** (the list is the bot roster: `crew = ["Alpha", "Beta", "Charlie", "Delta", "Echo"]`), a **Slicing lab** with start/stop steppers, a **Data types** reference (int, float, str, bool, list), then a 12-question pop-up test |
| **05 Turn it in** | The generated report, PDF/PNG/JPEG export, the naming convention, and the four upload steps |

The header carries the whole team identity: the chassis on the left under **Team leader** with ‹ › arrows to
flip through all 26, and the **Team** name field top right.

**Mission Check** — the end-of-class checklist — lives behind the ✓ button in the sticky rail, not on the page,
so the page itself stays uncluttered. It saves per device.

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
- `FILE_VAULT` — the easter-egg file type reference
- `STANDARDS` — five benchmarks from the 6th Grade Computer Science Standards Map, tagged by stage;
  they show as chips under each stage heading and print on the student's report. Deliberately five, not
  fifteen — these are the ones this mission actually assesses
- `RANKS` — Bronze / Silver / Gold / Platinum thresholds

## Hosting

Any static host works. For GitHub Pages: **Settings → Pages → Deploy from branch**, pick the branch and
`/ (root)`; the page is then served at the Pages URL and can be linked from the daily document.
