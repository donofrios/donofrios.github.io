#!/usr/bin/env python3
"""Post-process INSPIRE's papers.bib for al-folio:
  - abbr journal badge (from the journal name)
  - inspirehep_id (from inspire_ids.json) so the INSPIRE citation badge renders
  - optional selected = {true} for featured papers"""
import re
import json
import os

BIB = "_bibliography/papers.bib"
IDS = "inspire_ids.json"

JOURNAL_ABBR = {
    "Phys. Rev. D": "PRD", "Phys. Rev. Lett.": "PRL",
    "Phys. Dark Univ.": "PDU", "Eur. Phys. J. C": "EPJC",
    "JHEP": "JHEP", "Annals Phys.": "AoP", "Universe": "Universe",
    "Int. J. Geom. Meth. Mod. Phys.": "IJGMMP",
    "Class. Quant. Grav.": "CQG", "Phys. Lett. B": "PLB",
    "Gen. Rel. Grav.": "GRG", "Symmetry": "Symmetry",
}

SELECTED = set([
    # "DOnofrio:2025cuk",
])

id_map = {}
if os.path.exists(IDS):
    with open(IDS, encoding="utf-8") as f:
        for hit in json.load(f).get("hits", {}).get("hits", []):
            meta = hit.get("metadata", {})
            cn = meta.get("control_number")
            if cn:
                for tk in meta.get("texkeys", []):
                    id_map[tk] = cn

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
    if key in id_map and "inspirehep_id" not in e:
        inserts.append("    inspirehep_id = {%s}," % id_map[key])
    if key in SELECTED and "selected" not in e:
        inserts.append("    selected = {true},")
    if inserts:
        e = re.sub(r'(@\w+\{[^,]+,\n)', r'\1' +
                   "\n".join(inserts) + "\n", e, count=1)
    out.append(e)

with open(BIB, "w", encoding="utf-8") as f:
    f.write("".join(out))
print("Done: %d entries, %d INSPIRE ids mapped." %
      (len(entries) - 1, len(id_map)))
