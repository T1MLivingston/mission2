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
| **2.5 Extra points** | File types (JPEG/PNG/PDF), Python indexing (Index Lab, Slicing lab, index math, Data types), and both pop-up checks |
| **3 Turn it in** | The report, the one-click `.zip`, the exact file names, a role picker (three steps for the organizer, three for everyone else), and where in Drive it all goes |

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

## The three file-type demos

Section A teaches by letting students break things rather than by describing them:

- **JPEG** — a quality slider re-encodes the photograph live and prints the size, so *lossy* is something you
  watch happen: 62 KB and crisp at 100%, 2 KB and blocky at 5%, with the caption smearing on the way down.
  The photo travels with the page as a data URI, so it works on a blocked school network and with no assets
  folder. `PHOTO_SRC` is still fetched and used instead when the host allows re-encoding it.
- **PNG** — a bot on a checkerboard that drags, resizes and swaps. Nothing ever covers the background.
- **PDF** — the school calendar, the real one, riding inside the page. The card shows its first page; click
  to enlarge it, or open the actual PDF in its own tab.

**Hidden round:** triple-tap the *B · Python indexing* heading to unlock four slicing questions. They raise
the point ceiling from 8 to 12 rather than sharing it. (Triple-tapping the *A · File types* heading still
opens the Extension Vault.)

## The two links a teacher swaps

Both sit at the top of the `<script>` block, and both fail politely: with nothing pasted in, each says
*"link is in the daily document"* rather than handing a class of 6th graders a dead link.

```js
const CLASS_DRIVE_FOLDER = "";   // one Drive folder for every mission
const ORGANIZER_VIDEO    = "";   // how Student 1 builds the team folder
const SCHEDULE_PDF_...           // (the sample PDF, see below)
```

Only Student 1 creates anything: the team folder, and one `Student#_Name` folder inside it for each
teammate. Everyone else opens the class folder, walks down **period → Mission 2 → their team → the folder
with their own name on it**, and drops three files in. The crumb trail in Step 3 tracks whatever period,
team and student are set above it.

## One download instead of three

**Download all three · .zip** renders the report once and packs the PDF, PNG and JPEG into a single archive.
Both containers are written by hand in `index.html` — no library — because the page has to work with no
network:

- `zipStore()` writes **stored** (uncompressed) entries, since PNG and JPEG are already compressed. Deflating
  them again buys nothing and costs a dependency.
- `jpegPdf()` wraps the report's JPEG in the smallest legal PDF that can hold it — catalog, pages, page,
  image XObject, content stream, xref.

**Picture size** (1× / 2× / 3×) sets the render scale, and the size table underneath prints what each format
weighs afterwards. That is the resolution lesson: the same report at 3× is roughly double the bytes of 2×,
and the numbers are right there to compare.

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

## The landscape

The JPEG demo needs pixels the browser will let us read back, so the page carries its own alpine lake —
generated, not photographed, and deliberately full of the fine detail JPEG destroys first: ridge texture,
broken snow, ripples, film grain.

```
python3 tools/build-photo.py    # needs pillow + numpy
```

## The sample PDF

`assets/pdf/school-calendar.pdf` and a JPEG of its first page are both inlined, and

```
python3 tools/build-pdf.py      # needs pillow
```

rewrites them between the `/* PDFDOC_START */` and `/* PDFDOC_END */` markers. To use a different document,
drop it at that path, re-render the preview, and run it again — keep the pair under about 400 KB, because
whatever it weighs lands in every student's download.

The card and the enlarge view show the **JPEG**, not the PDF: a PDF in an `<iframe>` needs a plugin a
locked-down Chromebook may not run, and a blank grey box in front of a class is worse than a picture. The
real PDF is one click further on, where the browser opens it in a tab of its own.

That rewrites `assets/photo/lake.jpg` and the `PHOTO_LOCAL` data URI between the `/* PHOTO_START */` and
`/* PHOTO_END */` markers. To use a real photograph instead, save it as `assets/photo/lake.jpg`, comment out
the `render()` call, and re-run — or just point `PHOTO_SRC` at a host that sends CORS headers.

## Editing the content

Everything a teacher would want to change sits in named arrays at the top of the `<script>` block:

- `CATEGORIES` — the build options, their point costs, and star ratings
- `BASE_BUDGET` / `CREDIT_CAP` — the 20-point budget and the 8-credit cap
- `PY_QUESTIONS` / `FD_QUESTIONS` — the two tests (prompt, options, correct index, explanation)
- `CREW` — the five bots used in the indexing lesson and lab
- `CHIEFS` — which chassis hosts each spec box, and its job title
- `ROLE_BOTS` — the two bots fronting the Step 3 directions (Oscar the organizer, Golf for everyone)
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
