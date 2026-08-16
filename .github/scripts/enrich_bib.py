#!/usr/bin/env python3
"""Post-process INSPIRE's papers.bib for al-folio: add journal `abbr` badges,
and optionally flag featured papers with `selected = {true}`."""
import re

BIB = "_bibliography/papers.bib"

# INSPIRE journal string -> al-folio badge text. Add rows as needed.
JOURNAL_ABBR = {
    "Phys. Rev. D": "PRD",
    "Phys. Rev. Lett.": "PRL",
    "JCAP": "JCAP",
    "J. Cosmol. Astropart. Phys.": "JCAP",
    "Eur. Phys. J. C": "EPJC",
    "Eur. Phys. J. Plus": "EPJP",
    "Phys. Lett. B": "PLB",
    "Class. Quant. Grav.": "CQG",
    "Gen. Rel. Grav.": "GRG",
    "Phys. Dark Univ.": "PDU",
    "Astrophys. J.": "ApJ",
    "Mon. Not. Roy. Astron. Soc.": "MNRAS",
    "Astron. Astrophys.": "A&A",
    "Int. J. Mod. Phys. D": "IJMPD",
    "Nucl. Phys. B": "NPB",
    "Universe": "Universe",
    "Symmetry": "Symmetry",
    "JHEP": "JHEP",
    "Int. J. Geom. Meth. Mod. Phys.": "IJGMMP",
    "Annals Phys.": "AoP",
}

# INSPIRE texkeys to feature on the homepage. Leave empty to feature none.
SELECTED = set([
    # "DOnofrio:2025aaa",
])

with open(BIB, encoding="utf-8") as f:
    text = f.read()

entries = re.split(r'(?=@\w+\{)', text)
out = []
for e in entries:
    if not e.lstrip().startswith("@"):
        out.append(e)
        continue
    mkey = re.match(r'@\w+\{([^,]+),', e)
    key = mkey.group(1).strip() if mkey else ""
    mj = re.search(r'journal\s*=\s*[{"]([^}"]+)[}"]', e)
    inserts = []
    if mj:
        abbr = JOURNAL_ABBR.get(mj.group(1).strip())
        if abbr and "abbr" not in e:
            inserts.append("    abbr = {%s}," % abbr)
    if key in SELECTED and "selected" not in e:
        inserts.append("    selected = {true},")
    if inserts:
        e = re.sub(r'(@\w+\{[^,]+,\n)', r'\1' +
                   "\n".join(inserts) + "\n", e, count=1)
    out.append(e)

with open(BIB, "w", encoding="utf-8") as f:
    f.write("".join(out))
print("Enriched %d entries." % (len(entries) - 1))
