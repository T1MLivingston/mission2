# Mission 02 · Spec Check

A single-page, self-contained learning module for 6th grade Computer Science. It **is** the Mission 2
directions — link it from the daily document and students can work it top to bottom without any other handout.

Open `index.html` in a browser. No server, no build step, no internet required except for the web fonts
and the image-export library.

## What the page does

| Stage | What happens |
| --- | --- |
| **01 Briefing** | The mission, what counts as done, and the standards table |
| **02 Build** | Pick one of the 26 bots, then spend a 20-point hardware budget across RAM, storage type, storage capacity, ports, and special capability |
| **03 Indexing** | Four lesson cards + a live **Index Lab** (click a list item or type `crew[-2]`, `crew[1:3]`, `len(crew)` and see the result), then a 10-question pop-up test |
| **04 Files & Drive** | JPEG / PNG / PDF compared, what Google Drive actually is, a drag-to-upload practice window, then an 8-question pop-up test |
| **05 Turn It In** | The generated report, PDF/PNG/JPEG export, the naming convention, the five upload steps, and a final checklist |

Correct answers on the two tests earn **build credits** (+1 each, capped at 8) that raise the budget in
Stage 02 — so training is worth doing before the build is final. Max budget is 28 points against 33 points
of available parts, which keeps the trade-off real: nobody can afford everything.

Progress is saved in the browser's `localStorage` on that device only. Nothing is submitted from the page —
the graded artifact is the file the student uploads to Drive.

### Easter egg

**Triple-tap (or triple-click) the Stage 04 headline** — "JPEG, PNG, PDF — and where your file goes" —
to open **The Extension Vault**, a reference of all ~30 file types the course covers, grouped by kind.

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
- `FILE_VAULT` — the easter-egg file type reference
- `STANDARDS` — benchmarks from the 6th Grade Computer Science Standards Map, tagged by stage;
  they show as chips under each stage heading and print on the student's report
- `RANKS` — Bronze / Silver / Gold / Platinum thresholds

## Hosting

Any static host works. For GitHub Pages: **Settings → Pages → Deploy from branch**, pick the branch and
`/ (root)`; the page is then served at the Pages URL and can be linked from the daily document.
