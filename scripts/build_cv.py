#!/usr/bin/env python3
"""Render the LaTeX CV in cv-latex/, plus the small pieces of /cv/ that need
LaTeX converted to plain text first.

_pages/cv.md renders most of the HTML CV directly from existing site data, in
the same style as /talks/, /theses/, and /publications/: education from
_data/theses.yml (badges), publications via {% bibliography %}, conferences
and seminars from _data/talks.yml (badges) -- all read straight in Liquid, no
generation needed. This script only handles what's left: cv-latex/main.tex's
sections, and the few HTML sections whose source data (_data/cv_latex/*.yml)
is raw LaTeX and needs converting to plain text first.

Sources:
  _data/cv_latex/sections.yml                      (on/off switches for the PDF)
  _data/cv_latex/education.yml
  _data/cv_latex/skills.yml
  _data/cv_latex/visiting.yml
  _data/cv_latex/outreach.yml
  _data/cv_latex/scientific_activities_extra.yml   (undated standing entries)
  _data/talks.yml                                  (Conference/Poster -> CONFERENCES,
                                                      Seminar -> SCIENTIFIC ACTIVITIES)
  _bibliography/papers.bib                         (copied to cv-latex/Bibliography.bib)

Outputs (all regenerated on every run, safe to overwrite):
  cv-latex/generated/education.tex
  cv-latex/generated/skills.tex
  cv-latex/generated/conferences.tex
  cv-latex/generated/scientific_activities.tex
  cv-latex/generated/visiting.tex
  cv-latex/generated/outreach.tex
  cv-latex/generated/flags.tex
  cv-latex/Bibliography.bib
  _data/cv_extra.yml   (delatexed Skills/Visiting/Outreach/standing-activities for /cv/)

_data/cv_latex/profile.yml is plain text (no LaTeX) and is read directly by
_pages/cv.md as site.data.cv_latex.profile -- this script doesn't touch it.
"""

import re
import sys
import unicodedata
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "_data"
CV_DATA_DIR = DATA_DIR / "cv_latex"
CV_DIR = REPO_ROOT / "cv-latex"
GENERATED_DIR = CV_DIR / "generated"

_LATEX_ESCAPE_MAP = {
    "\\": r"\textbackslash{}",
    "&": r"\&",
    "%": r"\%",
    "$": r"\$",
    "#": r"\#",
    "_": r"\_",
    "{": r"\{",
    "}": r"\}",
    "~": r"\textasciitilde{}",
    "^": r"\textasciicircum{}",
}


def latex_escape(text):
    """Escape plain text (e.g. from _data/talks.yml) for safe use in LaTeX."""
    if not text:
        return ""
    return "".join(_LATEX_ESCAPE_MAP.get(ch, ch) for ch in text)


def load_yaml(path):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


# biber decomposes LaTeX accent macros (e.g. Garc{\'\i}a, Nordstr{\"o}m -- INSPIRE's
# standard BibTeX escaping) into a base letter + combining Unicode mark when it writes
# the .bbl, and pdflatex can't render a bare combining mark on its own. Precompose those
# to a single Unicode codepoint before biber ever sees them, so the CV compiles
# regardless of which INSPIRE-fetched names/titles show up in _bibliography/papers.bib.
# Also used when pulling bib text into the HTML CV, where leaving the raw LaTeX macro
# in place would show up as literal backslashes instead of the accented letter.
_ACCENT_COMBINING = {
    "'": "́",
    "`": "̀",
    "^": "̂",
    '"': "̈",
    "~": "̃",
    "=": "̄",
}
_ACCENT_RE = re.compile(r"""\{?\\(['`^"~=])\{?(\\[ij]|[A-Za-z])\}?\}?""")


def fix_latex_accents(text):
    def repl(m):
        mark = _ACCENT_COMBINING.get(m.group(1))
        if not mark:
            return m.group(0)
        base = {"\\i": "i", "\\j": "j"}.get(m.group(2), m.group(2))
        return base + mark

    return unicodedata.normalize("NFC", _ACCENT_RE.sub(repl, text))


# ---------------------------------------------------------------------------
# LaTeX CV (cv-latex/generated/*.tex)
# ---------------------------------------------------------------------------


def sub_heading_entry(heading, date, description, description_extra=""):
    """One \\resumeSubHeadingListStart ... \\resumeSubHeadingListEnd block."""
    lines = [
        r"\resumeSubHeadingListStart",
        rf"\resumeSubheading{{{heading}}}{{{date}}}{{{{}}}}{{}}",
    ]
    if description:
        lines.append(r"\begin{indentedtext}")
        lines.append(rf"\textit{{{description_extra}{description}}}")
        lines.append(r"\end{indentedtext}")
    lines.append(r"\resumeSubHeadingListEnd")
    return "\n".join(lines)


def render_education(entries):
    blocks = []
    n = len(entries)
    for i, e in enumerate(entries):
        thesis = rf"Thesis: \textbf{{{e['thesis_title']}}}"
        if e.get("thesis_status"):
            thesis += rf" \textit{{{e['thesis_status']}}}"
        if e.get("thesis_link"):
            thesis += rf" \href{{{e['thesis_link']}}}{{(\underline{{Link}})}}"
        thesis += rf" \\\small{{Supervisor:}} \textbf{{{e['supervisor']}}}"

        block = "\n".join(
            [
                r"\resumeSubHeadingListStart",
                r"    \resumeSubheading",
                rf"      {{{e['degree']}, {e['field']}}}{{{e['date_range']}}}",
                rf"      {{{e['institution']}}}{{{e['location']}}}",
                r"  \resumeSubHeadingListEnd",
                r"\vspace{0.9cm}",
                r"\begin{indentedtext}",
                rf"\normalsize{{{thesis}",
                r"}",
                r"\end{indentedtext}",
                r"\vspace{-0.2cm}" if i < n - 1 else r"\vspace{-15pt}",
            ]
        )
        blocks.append(block)
    return "\n\n".join(blocks) + "\n"


def render_skills(entries):
    lines = [r"\begin{itemize}"]
    for e in entries:
        lines.append(rf"\item\textbf{{\normalsize{{{e['label']}:}}}} \normalsize{{{e['details']}}}")
    lines.append(r"\end{itemize}")
    lines.append(r"\vspace{-15pt}")
    return "\n".join(lines) + "\n"


def build_talk_entries(talks, kind):
    """kind: 'conference' (Conference/Poster) or 'seminar' (Seminar).

    Returns structured, UNESCAPED dicts {heading, date, description} shared by
    both the LaTeX and HTML renderers, so heading/description composition
    only lives in one place.
    """
    wanted_types = {"Conference", "Poster"} if kind == "conference" else {"Seminar"}
    filtered = [t for t in talks if t.get("type") in wanted_types]
    filtered.sort(key=lambda t: str(t.get("date", "")), reverse=True)

    entries = []
    for t in filtered:
        title = t.get("title") or ""
        event = t.get("event") or ""
        location = t.get("location") or ""
        note = t.get("note") or ""
        date = t.get("display_date") or ""
        invited = bool(t.get("invited"))

        event_qualifier = ""
        if kind == "conference":
            # Keep the heading short (it shares a line with the date in a rigid
            # two-column layout in the PDF, so a long heading collides with the
            # date there). Any ", session/qualifier" suffix on the event moves
            # into the description instead.
            event_name, _, event_qualifier = event.partition(", ")
            heading = event_name or location
        else:
            prefix = "Invited " if invited else ""
            heading = f"{prefix}Seminar at {location}" if location else f"{prefix}Seminar"

        description_parts = []
        if event_qualifier:
            description_parts.append(f"{event_qualifier}.")
        if kind == "conference" and location and location != heading:
            description_parts.append(f"{location}.")
        if note:
            description_parts.append(note)
        if title:
            description_parts.append(f"Talk title: {title}.")

        entries.append({"heading": heading, "date": date, "description": " ".join(description_parts)})
    return entries


def render_talks_section_tex(talks, kind):
    blocks = []
    for e in build_talk_entries(talks, kind):
        blocks.append(
            sub_heading_entry(latex_escape(e["heading"]), latex_escape(e["date"]), latex_escape(e["description"]))
        )
    return blocks


def render_conferences(talks):
    blocks = render_talks_section_tex(talks, "conference")
    return "\n\n".join(blocks) + "\n" if blocks else "% (no CONFERENCES entries in _data/talks.yml)\n"


def render_scientific_activities(talks, extra_entries):
    blocks = render_talks_section_tex(talks, "seminar")
    for e in extra_entries:
        blocks.append(sub_heading_entry(e["title"], "", e.get("description", "")))
    return "\n\n".join(blocks) + "\n" if blocks else "% (no SCIENTIFIC ACTIVITIES entries)\n"


def render_visiting(entries):
    blocks = [sub_heading_entry(e["title"], e["date_range"], e.get("description", "")) for e in entries]
    return "\n\n".join(blocks) + "\n"


def render_outreach(data):
    lines = []
    if data.get("preamble"):
        lines.append(rf"\textit{{{data['preamble']}}}")
    blocks = []
    for e in data.get("entries", []):
        description = e.get("description", "")
        extra = r"\large " if description else ""
        blocks.append(sub_heading_entry(e["title"], e["date_range"], description, description_extra=extra))
    lines.append("\n\n".join(blocks))
    return "\n".join(lines) + "\n"


def render_flags(toggles):
    names = {
        "education": "CvEducation",
        "skills": "CvSkills",
        "conferences": "CvConferences",
        "scientific_activities": "CvScientificActivities",
        "visiting": "CvVisiting",
        "outreach": "CvOutreach",
    }
    lines = []
    for key, cmd in names.items():
        enabled = toggles.get(key, True)
        lines.append(rf"\{cmd}{'true' if enabled else 'false'}")
    return "\n".join(lines) + "\n"


def write_fragment(name, content):
    GENERATED_DIR.mkdir(parents=True, exist_ok=True)
    path = GENERATED_DIR / name
    path.write_text(content, encoding="utf-8")
    print(f"wrote {path.relative_to(REPO_ROOT)}")


# ---------------------------------------------------------------------------
# The few HTML CV pieces that need LaTeX converted to plain text first
# (_data/cv_extra.yml, read by _pages/cv.md as site.data.cv_extra)
# ---------------------------------------------------------------------------

_DELATEX_RULES = [
    (re.compile(r"\\href\{([^}]*)\}\{([^}]*)\}"), r"\2 (\1)"),
    (re.compile(r"\\textbf\{([^}]*)\}"), r"\1"),
    (re.compile(r"\\textit\{([^}]*)\}"), r"\1"),
]

_LATEX_UNESCAPE_MAP = {
    r"\#": "#",
    r"\&": "&",
    r"\%": "%",
    r"\_": "_",
    r"\$": "$",
    r"\textasciitilde{}": "~",
    r"\textasciicircum{}": "^",
    r"\textbackslash{}": "\\",
}


def delatex(text):
    """Convert a raw-LaTeX string from _data/cv_latex/*.yml into plain text for
    the HTML CV. $...$ math is left as-is (MathJax is on site-wide, see
    _config.yml enable_math)."""
    if not text:
        return ""
    text = text.replace("\n", " ")  # source YAML sometimes wraps long values across lines
    text = fix_latex_accents(text)
    for pattern, repl in _DELATEX_RULES:
        text = pattern.sub(repl, text)
    for escaped, plain in _LATEX_UNESCAPE_MAP.items():
        text = text.replace(escaped, plain)
    # \\ is LaTeX's manual line-break, used in cv_latex/*.yml purely for PDF
    # justification -- it carries no semantic meaning in flowing HTML text.
    text = text.replace(r"\underline", "").replace("\\\\", ", ")
    text = re.sub(r"\\quad", " ", text)
    text = text.replace(":,", ":")  # tidy the ", " line-break separator landing right after a colon
    text = re.sub(r"[ \t]+", " ", text).strip(" ,")
    return text


def html_skills(entries):
    # `details` is free prose for some entries ("Deep knowledge of C, C++, ...
    # Ability to use...") and a clean comma list for others ("Expertise"), so
    # it isn't safe to split on commas in general -- keep it as one string.
    return [{"label": delatex(e["label"]), "details": delatex(e["details"])} for e in entries]


def html_dated_entries(entries):
    return [
        {"title": delatex(e["title"]), "date_range": e["date_range"], "description": delatex(e.get("description", ""))}
        for e in entries
    ]


def html_outreach(data):
    return {
        "preamble": delatex(data.get("preamble", "")),
        "entries": html_dated_entries(data.get("entries", [])),
    }


def html_sci_extra(entries):
    return [{"title": delatex(e["title"]), "description": delatex(e.get("description", ""))} for e in entries]


def write_cv_extra(skills, sci_extra, visiting, outreach):
    data = {
        "skills": html_skills(skills),
        "scientific_activities_extra": html_sci_extra(sci_extra),
        "visiting": html_dated_entries(visiting),
        "outreach": html_outreach(outreach),
    }
    path = DATA_DIR / "cv_extra.yml"
    header = (
        "# Generated by scripts/build_cv.py from _data/cv_latex/{skills,visiting,outreach,\n"
        "# scientific_activities_extra}.yml. Do not edit by hand -- edit those sources and\n"
        "# rerun the generator (or push; CI does it for you). See cv-latex/README.md.\n"
    )
    body = yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=100)
    path.write_text(header + body, encoding="utf-8")
    print(f"wrote {path.relative_to(REPO_ROOT)}")


def main():
    education = load_yaml(CV_DATA_DIR / "education.yml")
    skills = load_yaml(CV_DATA_DIR / "skills.yml")
    visiting = load_yaml(CV_DATA_DIR / "visiting.yml")
    outreach = load_yaml(CV_DATA_DIR / "outreach.yml")
    sci_extra = load_yaml(CV_DATA_DIR / "scientific_activities_extra.yml")
    talks = load_yaml(DATA_DIR / "talks.yml")
    sections = load_yaml(CV_DATA_DIR / "sections.yml")

    write_fragment("education.tex", render_education(education))
    write_fragment("skills.tex", render_skills(skills))
    write_fragment("conferences.tex", render_conferences(talks))
    write_fragment("scientific_activities.tex", render_scientific_activities(talks, sci_extra))
    write_fragment("visiting.tex", render_visiting(visiting))
    write_fragment("outreach.tex", render_outreach(outreach))
    write_fragment("flags.tex", render_flags(sections))

    bib_src = REPO_ROOT / "_bibliography" / "papers.bib"
    bib_dst = CV_DIR / "Bibliography.bib"
    bib_text = bib_src.read_text(encoding="utf-8")
    bib_text = fix_latex_accents(bib_text)
    bib_dst.write_text(bib_text, encoding="utf-8")
    print(f"copied {bib_src.relative_to(REPO_ROOT)} -> {bib_dst.relative_to(REPO_ROOT)} (accent-normalized)")

    write_cv_extra(skills, sci_extra, visiting, outreach)


if __name__ == "__main__":
    sys.exit(main())
