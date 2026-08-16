# CV (LaTeX + HTML)

`main.tex` is a [sb2nov/Abey George](https://github.com/sb2nov/resume)-style resume. Its styling and macros
(`\resumeSubheading`, `\resumeSubHeadingListStart/End`, `indentedtext`, colors, fonts) are hand-tuned and should
not be touched for a routine content update. The dynamic sections are `\input`s of files under `generated/`,
which [`scripts/build_cv.py`](../scripts/build_cv.py) renders from YAML data on every push. Nothing under
`generated/` or `Bibliography.bib` in this directory is hand-edited — both are build output (see `.gitignore`).

The HTML CV at `/cv/` ([`_pages/cv.md`](../_pages/cv.md)) is a **separate page that reads most of its content
directly** from the same underlying sources — `_data/theses.yml` for Education, the site's own bibliography for
Publications, `_data/talks.yml` for Conferences/Scientific Activities — no generator involved for those. The
exception is Skills, Visiting Experiences, Outreach Activities, and the standing "Refereeing activities" line:
those live in `_data/cv_latex/*.yml` as **raw LaTeX** (`\textbf{}`, math mode, `\\` line breaks), which HTML can't
render directly, so `build_cv.py` converts them to plain text and writes the result to `_data/cv_extra.yml`.

**`_data/cv_extra.yml` is a build artifact, not something you ever edit or even need to look at** — same as
`generated/*.tex`. It's gitignored; edit `_data/cv_latex/skills.yml` (etc.) instead and it gets regenerated:
`build-cv.yml` regenerates it (among other things) on every push that touches CV data, and `deploy.yml`
regenerates it fresh before every site build, so the HTML page is always current even though the file itself
never gets committed.

## How to update the CV

| To change...                             | Edit...                                                                                                                                                                             |
| ---------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Your name/email/location/bio (HTML CV)   | [`_data/cv_latex/profile.yml`](../_data/cv_latex/profile.yml) (`main.tex`'s header is hand-edited separately)                                                                       |
| A conference, poster, or seminar         | [`_data/talks.yml`](../_data/talks.yml) (also feeds the public /talks/ page)                                                                                                        |
| Education entries                        | [`_data/theses.yml`](../_data/theses.yml) (also feeds the public /theses/ page) for the HTML CV; [`_data/cv_latex/education.yml`](../_data/cv_latex/education.yml) for the PDF only |
| The undated "Refereeing activities" line | [`_data/cv_latex/scientific_activities_extra.yml`](../_data/cv_latex/scientific_activities_extra.yml)                                                                               |
| Skills                                   | [`_data/cv_latex/skills.yml`](../_data/cv_latex/skills.yml)                                                                                                                         |
| Visiting experiences                     | [`_data/cv_latex/visiting.yml`](../_data/cv_latex/visiting.yml)                                                                                                                     |
| Outreach activities                      | [`_data/cv_latex/outreach.yml`](../_data/cv_latex/outreach.yml)                                                                                                                     |
| Which sections go in the **PDF**         | [`_data/cv_latex/sections.yml`](../_data/cv_latex/sections.yml) — on/off switches, PDF only. The HTML CV always shows every section.                                                |
| Publications                             | nothing here — the same INSPIRE-generated `_bibliography/papers.bib` the site uses is copied into `Bibliography.bib` at build time                                                  |

Note Education is the one section that _doesn't_ share a single source between the PDF and the HTML page: the
PDF needs a `field`/`location` breakdown the theses page has no use for, so it kept its own `education.yml`
rather than being migrated onto `_data/theses.yml` the way Conferences moved onto `_data/talks.yml`.

Each `_data/cv_latex/*.yml` file documents its own schema in a header comment. Values in `education.yml`,
`skills.yml`, `visiting.yml`, `outreach.yml`, and `scientific_activities_extra.yml` are raw LaTeX, matching what
they replaced in `main.tex` — `$...$` math is left alone when converted for HTML since MathJax is enabled
site-wide (see `delatex()` in `build_cv.py`).

Push to `main` and CI handles the rest — no manual steps. To preview locally:

```bash
python3 -m pip install pyyaml
python3 scripts/build_cv.py       # writes cv-latex/generated/*.tex and _data/cv_extra.yml
cd cv-latex && latexmk -pdf main.tex   # optional: only needed to check the PDF itself
```

(Without that first step, `bundle exec jekyll serve` still works — Skills/Visiting/Outreach/the standing
activities line on `/cv/` just render empty until `_data/cv_extra.yml` exists.)
