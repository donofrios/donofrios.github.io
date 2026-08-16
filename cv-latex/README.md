# CV (LaTeX + HTML)

`main.tex` is a [sb2nov/Abey George](https://github.com/sb2nov/resume)-style resume. Its styling and macros
(`\resumeSubheading`, `\resumeSubHeadingListStart/End`, `indentedtext`, colors, fonts) are hand-tuned and should
not be touched for a routine content update. The dynamic sections are `\input`s of files under `generated/`,
which [`scripts/build_cv.py`](../scripts/build_cv.py) renders from YAML data on every push. Nothing under
`generated/` or `Bibliography.bib` in this directory is hand-edited — both are build output (see `.gitignore`).

The same generator also writes [`_data/cv.yml`](../_data/cv.yml), which drives the HTML CV at `/cv/` (via the
`al_folio_cv` gem). One edit updates both the PDF and the live page.

## How to update the CV

| To change...                             | Edit...                                                                                                                             |
| ---------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| Your name/email/phone/location/bio       | [`_data/cv_latex/profile.yml`](../_data/cv_latex/profile.yml) (HTML CV only — `main.tex`'s header is hand-edited separately)        |
| A conference, poster, or seminar         | [`_data/talks.yml`](../_data/talks.yml) (also feeds the public /talks/ page)                                                        |
| The undated "Refereeing activities" line | [`_data/cv_latex/scientific_activities_extra.yml`](../_data/cv_latex/scientific_activities_extra.yml)                               |
| Education entries                        | [`_data/cv_latex/education.yml`](../_data/cv_latex/education.yml)                                                                   |
| Skills                                   | [`_data/cv_latex/skills.yml`](../_data/cv_latex/skills.yml)                                                                         |
| Visiting experiences                     | [`_data/cv_latex/visiting.yml`](../_data/cv_latex/visiting.yml)                                                                     |
| Outreach activities                      | [`_data/cv_latex/outreach.yml`](../_data/cv_latex/outreach.yml)                                                                     |
| Which sections go in the **PDF**         | [`_data/cv_latex/sections.yml`](../_data/cv_latex/sections.yml) — on/off switches, PDF only. The HTML CV always shows all sections. |
| Publications                             | nothing here — the same INSPIRE-generated `_bibliography/papers.bib` the site uses is copied into `Bibliography.bib` at build time  |

Each `_data/cv_latex/*.yml` file documents its own schema in a header comment.

Values in `education.yml`, `skills.yml`, `visiting.yml`, `outreach.yml`, and `scientific_activities_extra.yml`
are raw LaTeX (`\textbf{}`, `$math$`, `\\` line breaks, etc.), matching what they replaced in `main.tex`. The
generator also reuses them for the HTML CV, running them through a small LaTeX→text/Markdown converter
(`delatex()` in `build_cv.py`) — `$...$` math is left alone since MathJax is enabled site-wide. Values sourced
from `_data/talks.yml` and `_bibliography/papers.bib` are already plain text, used as-is for the HTML CV and
LaTeX-escaped for the PDF.

Push to `main` and [`build-cv.yml`](../.github/workflows/build-cv.yml) regenerates `assets/pdf/CV.pdf` and
`assets/pdf/cv_latex.zip`, updates `_data/cv.yml`, and redeploys the site — no manual steps. To do the same
locally:

```bash
python3 -m pip install pyyaml
python3 scripts/build_cv.py
cd cv-latex && latexmk -pdf main.tex   # optional: only needed to check the PDF itself
```
