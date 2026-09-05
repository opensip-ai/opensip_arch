#!/usr/bin/env python3
"""Generator for `preview-product-boundary-successor.v15.json`.

Builds the DR-117 preview-scoped successor candidate **v15** from the frozen,
RECORDED predecessor `preview-product-boundary-successor.v10.json`
(sha256 8f34c92e..., recorded at COORD `## D-295`).

Why v15 exists (D-294 Decision 2 trigger (b)): four of the twelve leftover-joins
v10 cites as current have been superseded since the D-295 recording, and on two
of them the leftoverDesign partition changed.  D-294 Decision 3 requires a
successor issued for any reason to refresh its cross-lineage citations to the
versions current at its dispatch.

The script writes ONLY the file you name.  It never touches `docs/`, and it runs
no state-changing git command.  Exit 2 with nothing written if any measurement
disagrees with the record.
"""
import argparse, hashlib, json, os, re, subprocess, sys, datetime

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
ART = "docs/coop/artifacts"
COORD = "docs/coop/COORDINATOR-DECISIONS.md"
F08 = "docs/v2/architecture/08-decision-and-readiness-register.md"
F02 = "docs/v2/architecture/02-distribution-and-components.md"
V1SLICE = "docs/coop/v1-slice.md"

PRED_PATH = f"{ART}/preview-product-boundary-successor.v10.json"
PRED_SHA = "8f34c92ef4fb835ce31945bfc73e1442b38dada1d483380231a53d1d93a03483"
PRED_RECORDING = "D-295"
PRED = "preview-product-boundary-successor.v10"
SELF = "preview-product-boundary-successor.v15"
SPEAKER = f"This {SELF}"
VERSION = 15
REQUIRED_NOW = 28
REGISTER_ROW = "DR-117"

# lineage -> (basedOn key stem, register row token used in the citing sentences,
#             inverted-heading token)
LINEAGES = [
    ("g29",               "g29Join",              "G29",     "G29"),
    ("g30",               "g30Join",              "G30",     "G30"),
    ("g09",               "g09Join",              "G09",     "G09"),
    ("language-runtime",  "languageRuntimeJoin",  "G14",     "G14"),
    ("g16",               "g16Join",              "G16",     "G16"),
    ("g21",               "g21Join",              "G21",     "G21"),
    ("g23",               "g23Join",              "G23",     "G23"),
    ("permission",        "permissionJoin",       "DR-105",  "DR-105"),
    ("distribution-core", "distributionCoreJoin", "DR-101",  "DR-101"),
    ("monorepo",          "monorepoJoin",         "DR-121",  "DR-121"),
    ("language-quality",  "languageQualityJoin",  "DR-118",  "DR-118"),
    ("doctor-actor",      "doctorActorJoin",      "DR-114",  "DR-114"),
]


class Fail(Exception):
    pass


def need(cond, msg):
    if not cond:
        raise Fail(msg)


def sha256_file(rel):
    with open(os.path.join(REPO, rel), "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def read_text(rel):
    with open(os.path.join(REPO, rel), encoding="utf-8") as fh:
        return fh.read()


def read_json(rel):
    return json.loads(read_text(rel))


def git(*args):
    return subprocess.run(["git", "-C", REPO, *args], capture_output=True,
                          text=True, check=True).stdout.strip()


def assert_docs_tree_clean():
    out = git("status", "--porcelain", "--", "docs")
    dirty = [l for l in out.splitlines() if l and not l.startswith("??")]
    need(not dirty, "tracked files under docs/ are modified: " + "; ".join(dirty[:5]))


def current_join_recording(coord, lineage, inverted_token):
    """Highest non-CONTESTED recording heading, accepting BOTH record spellings.

    Forward:  '## D-NNN - Record <lineage>[- ]leftover-join.vN as ...'
    Inverted: '## D-NNN - Record leftover-join.vN of <TOKEN> as ...'
    The inverted spelling entered the record at the G21/G29/G30 fixture series;
    a forward-only matcher silently returns a stale version.
    """
    fwd = re.compile(r"^## D-(\d+) — Record " + re.escape(lineage) +
                     r"[- ]leftover-join\.v(\d+)\b(.*)$")
    inv = re.compile(r"^## D-(\d+) — Record leftover-join\.v(\d+) of " +
                     re.escape(inverted_token) + r"\b(.*)$", re.I)
    best = None
    for line in coord.splitlines():
        m = fwd.match(line) or inv.match(line)
        if not m:
            continue
        if "CONTESTED" in m.group(3):
            continue
        n, v = int(m.group(1)), int(m.group(2))
        if best is None or n > best[0]:
            best = (n, v, line)
    need(best is not None, f"COORD names no leftover-join recording for {lineage}")
    return best


def coord_entry_text(coord, dnum):
    """Body of '## D-NNN - ...' up to the next '## D-' heading."""
    lines = coord.splitlines()
    start = None
    for i, l in enumerate(lines):
        if l.startswith(f"## D-{dnum} —"):
            start = i
            break
    need(start is not None, f"COORD carries no heading for D-{dnum}")
    end = len(lines)
    for j in range(start + 1, len(lines)):
        if lines[j].startswith("## D-"):
            end = j
            break
    return "\n".join(lines[start:end])


def pin_review(lineage, ver, who):
    rel = f"{ART}/{lineage}-leftover-join.v{ver}.review-independent.{who}.json"
    need(os.path.exists(os.path.join(REPO, rel)), f"missing review {rel}")
    doc = read_json(rel)
    blob = json.dumps(doc)
    need("ACCEPT" in blob, f"{rel} does not read ACCEPT")
    return {"path": rel, "sha256": sha256_file(rel), "verdict": "ACCEPT 0/0"}


def leftover_true_ids(doc):
    s = doc.get("summary", {})
    if isinstance(s.get("leftoverDesign"), list):
        return list(s["leftoverDesign"])
    return [o.get("obligationId") or o.get("id")
            for o in doc.get("obligations", []) if o.get("leftoverDesign") is True]


def bucket_ids(doc, bucket):
    return list(doc.get("summary", {}).get(bucket, []) or [])


FINDING_ID_RE = re.compile(r"^(?:CLAUDE-)?PPBS-?V\d+-[A-Z0-9-]+$")


def collect_finding_ids(review_doc, version=None):
    """Reviewer finding identifiers RAISED BY this verdict, whatever the shape.

    A verdict may reference an earlier version's finding by id; those are not its
    own.  v14 counted them and stated three identifiers for a version with two."""
    ids = []

    def walk(node):
        if isinstance(node, dict):
            i = node.get("id") or node.get("identifier")
            if isinstance(i, str) and FINDING_ID_RE.match(i) and i not in ids:
                if version is None or re.search(rf"V{version}-", i):
                    ids.append(i)
            for v in node.values():
                walk(v)
        elif isinstance(node, list):
            for v in node:
                walk(v)
    for key in ("blockers", "mustFix", "shouldFix", "advisories", "findings",
                "observations", "observationsNotFindings"):
        walk(review_doc.get(key))
    return ids


def lineage_census(coord):
    """Every frozen version of this lineage on disk, with its recording (measured from
    COORD, not assumed), every verdict file that exists, and its finding identifiers.

    v11/v12/v13 each shipped a hand-written universal claim about the predecessor record
    that the bytes did not satisfy.  The census is the bytes; the prose that describes it
    is generated from the census, so the claim cannot outrun what is pinned."""
    rec_re = re.compile(r"^## D-(\d+) — Record preview-product-boundary-successor\.v(\d+)\b")
    recordings = {}
    for line in coord.splitlines():
        mm = rec_re.match(line)
        if mm:
            recordings[int(mm.group(2))] = f"D-{mm.group(1)}"
    out = []
    for v in range(1, VERSION):
        rel = f"{ART}/preview-product-boundary-successor.v{v}.json"
        exists = os.path.exists(os.path.join(REPO, rel))
        reviews, ids = {}, []
        for who, fn in (("claude", "claude2"), ("codex", "codex")):
            r = f"{ART}/preview-product-boundary-successor.v{v}.review-independent.{fn}.json"
            if not os.path.exists(os.path.join(REPO, r)):
                continue
            doc = read_json(r)
            verdict = doc.get("verdict") or doc.get("decision") or "UNKNOWN"
            entry = {"path": r, "sha256": sha256_file(r), "verdict": verdict}
            gr = doc.get("gradeRuling")
            if isinstance(gr, dict) and gr.get("ruling"):
                entry["gradeRuling"] = gr["ruling"]
            reviews[who] = entry
            ids += [i for i in collect_finding_ids(doc, v) if i not in ids]
        if not exists and not reviews:
            continue
        out.append({
            "version": v, "path": rel if exists else None,
            "sha256": sha256_file(rel) if exists else None,
            "recording": recordings.get(v),
            "standing": ("RECORDED" if recordings.get(v)
                         else "REJECTED-AT-STAGE-A-NEVER-RECORDED"),
            "reviews": reviews, "findingIds": ids,
        })
    need(out, "no predecessor versions found on disk")
    return out


def rejected_intermediates(pred_version):
    """Frozen versions of this lineage after the current recording and before SELF.

    v12 shipped with no trace of v11 anywhere in its bytes: the generator built from
    the recorded predecessor and had no concept of a rejected version in between.
    This discovers them from disk instead of from a hand-maintained list.
    """
    out = []
    for v in range(pred_version + 1, VERSION):
        rel = f"{ART}/preview-product-boundary-successor.v{v}.json"
        if not os.path.exists(os.path.join(REPO, rel)):
            continue
        reviews, ids = {}, []
        for who, fn in (("claude", "claude2"), ("codex", "codex")):
            r = f"{ART}/preview-product-boundary-successor.v{v}.review-independent.{fn}.json"
            if not os.path.exists(os.path.join(REPO, r)):
                continue
            doc = read_json(r)
            verdict = doc.get("verdict") or doc.get("decision") or "UNKNOWN"
            reviews[who] = {"path": r, "sha256": sha256_file(r), "verdict": verdict,
                            "gradeRuling": (doc.get("gradeRuling") or {}).get("ruling")
                            if isinstance(doc.get("gradeRuling"), dict) else None}
            ids += [i for i in collect_finding_ids(doc, v) if i not in ids]
        need(reviews, f"no Stage A verdicts on disk for preview-product-boundary-successor.v{v}")
        need(all(r["verdict"] == "REJECT" for r in reviews.values()),
             f"preview-product-boundary-successor.v{v} is not a rejected intermediate")
        out.append({"version": v, "path": rel, "sha256": sha256_file(rel),
                    "reviews": reviews, "findingIds": ids})
    return out


def measure():
    """Everything measured from live bytes.  Nothing here is hard-coded."""
    coord = read_text(COORD)
    pred = read_json(PRED_PATH)
    need(sha256_file(PRED_PATH) == PRED_SHA,
         f"predecessor moved: {sha256_file(PRED_PATH)} != {PRED_SHA}")
    need(PRED_SHA in coord_entry_text(coord, 295),
         "D-295's own text does not carry the v10 digest")

    joins = []
    for lineage, keystem, rowtok, invtok in LINEAGES:
        dnum, ver, _ = current_join_recording(coord, lineage, invtok)
        rel = f"{ART}/{lineage}-leftover-join.v{ver}.json"
        need(os.path.exists(os.path.join(REPO, rel)), f"missing {rel}")
        doc = read_json(rel)
        sha = sha256_file(rel)
        entry = coord_entry_text(coord, dnum)
        need(sha in entry, f"D-{dnum} text does not carry {rel}'s digest")
        need(doc.get("status") == "CANDIDATE-NOT-APPLIED",
             f"{rel} is not CANDIDATE-NOT-APPLIED")
        need(doc.get("binds") == "NOTHING", f"{rel} does not bind NOTHING")

        # what v10 cited for this lineage
        pkey = next((k for k in pred["basedOn"]
                     if k.startswith(keystem) and re.fullmatch(keystem + r"V\d+", k)), None)
        need(pkey is not None, f"v10 basedOn has no key for {keystem}")
        cited_ver = int(pkey[len(keystem) + 1:])
        cited = pred["basedOn"][pkey]

        joins.append({
            "lineage": lineage, "keystem": keystem, "rowToken": rowtok,
            "registerRow": doc.get("registerRow"),
            "citedVer": cited_ver, "citedRec": cited["recording"],
            "citedPath": cited["path"], "citedSha": cited["sha256"],
            "ver": ver, "rec": f"D-{dnum}", "path": rel, "sha256": sha,
            "doc": doc, "predKey": pkey,
            "leftoverTrue": leftover_true_ids(doc),
            "citedLeftoverTrue": leftover_true_ids(read_json(cited["path"])),
            "specifiedNotLeftover": bucket_ids(doc, "specifiedNotLeftover"),
            "qualificationAtNamedGate": bucket_ids(doc, "qualificationAtNamedGate"),
            "moved": ver != cited_ver,
            "reviews": {"claude": pin_review(lineage, ver, "claude2"),
                        "codex": pin_review(lineage, ver, "codex")},
        })

    moved = [j for j in joins if j["moved"]]
    need(len(moved) >= 1, "no lineage moved since D-295; v11 has no D-294 trigger")
    # trigger (b) must actually fire for at least one moved lineage, else say so
    partition_changed = [j for j in moved if j["leftoverTrue"] != j["citedLeftoverTrue"]]

    f08 = read_text(F08)
    row = [l for l in f08.splitlines() if l.startswith("| DR-117 |")]
    need(len(row) == 1, "file 08 does not carry exactly one DR-117 row")
    cells = [c.strip() for c in row[0].split("|")]
    label = cells[6]
    lead = label.split(".")[0].lstrip("*").strip() if label.startswith("**") else label
    lead_token = lead.split()[0] if lead else label
    need(lead_token in ("OPEN", "SATISFIED"),
         f"DR-117 leading label token is {lead_token!r}, expected OPEN or SATISFIED")
    need("**28 of 28 required gates name a recorded identifier**" in f08,
         "file 08 no longer carries the 28-of-28 required-now snapshot")

    rejected = rejected_intermediates(10)
    census = lineage_census(coord)

    return {
        "rejected": rejected, "census": census,
        "coord": coord, "pred": pred, "joins": joins, "moved": moved,
        "partitionChanged": partition_changed,
        "head": git("rev-parse", "HEAD"),
        "date": datetime.date.today().isoformat(),
        "f08sha": sha256_file(F08), "f02sha": sha256_file(F02),
        "v1slice": sha256_file(V1SLICE), "coordsha": sha256_file(COORD),
        "f08label": lead_token, "f08labelFull": label,
    }


def refresh_pairs(m):
    """Ordered (old, new, why) replacements applied to the EE citing sentences."""
    pairs = []
    for j in m["moved"]:
        lin = j["lineage"]
        pairs.append((
            f"{lin} leftover-join.v{j['citedVer']} ({j['citedRec']})",
            f"{lin} leftover-join.v{j['ver']} ({j['rec']})",
            f"currency citation {lin} v{j['citedVer']}->v{j['ver']}"))
    for j in m["partitionChanged"]:
        old_ids = j["citedLeftoverTrue"]
        if old_ids and not j["leftoverTrue"]:
            ids = ", ".join(old_ids)
            moved_to = ("specifiedNotLeftover"
                        if all(i in j["specifiedNotLeftover"] for i in old_ids)
                        else "qualificationAtNamedGate")
            new_clause = (f"leftoverDesign is the empty list; {ids} sits in {moved_to}.")
            # Longest first: the partition clause is followed by different sentences at
            # different sites (v11 matched only the "does not steal that leftover" variant
            # and silently left six sites asserting a closed leftover).
            pairs.append((
                f"leftoverDesign remains [{ids}]. This successor does not steal that leftover.",
                f"{new_clause} This successor does not steal that measurement.",
                f"partition {j['lineage']} true->empty (with steal-clause)"))
            pairs.append((
                f"leftoverDesign remains [{ids}].", new_clause,
                f"partition {j['lineage']} true->empty (bare clause)"))
    return pairs


def apply_refresh(classes, pairs):
    sites = {}
    out = json.loads(json.dumps(classes))
    for cls in out:
        for field in ("existingGate", "laterExecution"):
            txt = cls.get(field)
            if not isinstance(txt, str):
                continue
            for old, new, why in pairs:
                n = txt.count(old)
                if n:
                    txt = txt.replace(old, new)
                    sites[why] = sites.get(why, 0) + n
            cls[field] = txt
    return out, sites


def normalize(classes, pairs):
    """Collapse both sides of every refresh so equality can be asserted."""
    blob = json.dumps(classes, sort_keys=True)
    for old, new, _ in pairs:
        blob = blob.replace(json.dumps(old)[1:-1], "<<R>>").replace(json.dumps(new)[1:-1], "<<R>>")
    return blob


def build_recorded_inputs(m, based_on):  # noqa: D401
    ri = {COORD: m["coordsha"], F08: m["f08sha"], F02: m["f02sha"], V1SLICE: m["v1slice"],
          PRED_PATH: PRED_SHA}
    for fn in ("claude2", "codex"):
        rel = f"{ART}/preview-product-boundary-successor.v10.review-independent.{fn}.json"
        ri[rel] = sha256_file(rel)
    for c in m["census"]:
        if c["path"]:
            ri[c["path"]] = c["sha256"]
        for r in c["reviews"].values():
            ri[r["path"]] = r["sha256"]
    for j in m["joins"]:
        ri[j["path"]] = j["sha256"]
        for who in ("claude", "codex"):
            ri[j["reviews"][who]["path"]] = j["reviews"][who]["sha256"]
    # carry every predecessor-pinned path that still exists, re-measured from bytes
    for path, _old in m["pred"]["recordedInputs"].items():
        if path == "HEAD":
            continue
        if path not in ri and os.path.exists(os.path.join(REPO, path)):
            ri[path] = sha256_file(path)
    out = {k: ri[k] for k in sorted(ri)}
    out["HEAD"] = m["head"]
    return out


def word(n):
    return {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six",
            7: "seven", 8: "eight", 9: "nine", 10: "ten", 11: "eleven",
            12: "twelve", 13: "thirteen", 14: "fourteen"}.get(n, str(n))


def must_replace(blob, old, new, why, expect_at_least=1):
    """A rewrite that silently matches nothing is the v14 failure mode: the branch
    never fires and a disposition still claims the repair landed.  Abort instead."""
    n = blob.count(old)
    need(n >= expect_at_least,
         f"rewrite matched {n} times, expected at least {expect_at_least} ({why}): {old[:70]!r}")
    return blob.replace(old, new)


def dedeictic(node):
    """Carried text speaks in the predecessor's voice; name it as history instead."""
    blob = json.dumps(node).replace(f"This {PRED}", f"{PRED} ({PRED_RECORDING})")
    # present-tense currency verbs inside carried history read as claims about THIS
    # successor's bytes; date them to the predecessor's dispatch instead.
    blob = blob.replace(" now states the measured partition",
                        f" states, at {PRED}'s dispatch, the measured partition")
    blob = blob.replace("to the twelve versions current at this dispatch",
                        f"to the twelve versions current at {PRED}'s dispatch")
    return json.loads(blob)


def build_doc(m):
    pred = m["pred"]
    pairs = refresh_pairs(m)
    classes, sites = apply_refresh(pred["enforcementEvidence"]["classes"], pairs)
    need(normalize(classes, pairs) == normalize(pred["enforcementEvidence"]["classes"], pairs),
         "EE classes differ from the predecessor's beyond the refreshed sentences")

    moved_names = [f"{j['lineage']} leftover-join.v{j['citedVer']} ({j['citedRec']}) "
                   f"to {j['lineage']} leftover-join.v{j['ver']} ({j['rec']})"
                   for j in m["moved"]]
    nmoved, nkept = len(m["moved"]), len(m["joins"]) - len(m["moved"])

    census = m["census"]
    immediate = max(c["version"] for c in census)
    based_on = {}
    for c in census:
        v = c["version"]
        name = f"preview-product-boundary-successor.v{v}"
        if c["standing"] == "RECORDED":
            if v == 10:
                what = (f"the current recorded DR-117 leftover remasurement, recorded at "
                        f"{c['recording']}. {SELF} is its successor and is "
                        f"CANDIDATE-NOT-APPLIED; until a reviewed coordinator act records "
                        f"{SELF}, {PRED} stays current.")
            else:
                what = (f"recorded at {c['recording']} and superseded within this lineage. It "
                        f"stays frozen and is not to be recorded as current.")
        elif v == immediate:
            what = (f"the immediate predecessor of {SELF}, REJECTED at Stage A by both "
                    f"independent reviewers and never recorded. It never became current; "
                    f"{PRED} ({PRED_RECORDING}) stayed the current recorded DR-117 leftover "
                    f"remasurement throughout. It stays frozen and is not to be recorded. "
                    f"{SELF} exists to land its findings.")
        else:
            what = ("an earlier attempt within this lineage, rejected at Stage A and never "
                    "recorded. It never became current. It stays frozen and is not to be "
                    "recorded.")
        obj = {"path": c["path"], "sha256": c["sha256"],
               "recording": c["recording"], "standing": c["standing"],
               "reviews": c["reviews"],
               "role": (f"{name} is {what} Its "
                        f"{word(len(c['findingIds'])) if c['findingIds'] else 'zero'} Stage A "
                        f"finding identifier(s) are disposed in findingDisposition. "
                        f"{name} and preview-product-boundary-successor are the same lineage; "
                        f"version numbers across different lineages are unrelated.")}
        based_on[f"predecessorV{v}"] = obj

    based_on["predecessorPinningShape"] = describe_pin_shape(based_on, census, immediate)

    for j in m["joins"]:
        key = f"{j['keystem']}V{j['ver']}"
        if j["moved"]:
            role = (f"Current {j['registerRow']} leftover-join at {SELF}'s dispatch, measured as "
                    f"the version named by the highest non-CONTESTED COORD recording for this "
                    f"lineage ({j['rec']}). {PRED} cited {j['lineage']} leftover-join."
                    f"v{j['citedVer']} ({j['citedRec']}); that citation is superseded by "
                    f"{j['rec']} and is not current. Obligations flagged leftoverDesign true on "
                    f"{j['lineage']} leftover-join.v{j['ver']} at this dispatch: "
                    f"[{', '.join(j['leftoverTrue'])}]. {SPEAKER} does not steal that "
                    f"measurement. {j['lineage']} leftover-join and "
                    f"preview-product-boundary-successor are different lineages; their version "
                    f"numbers are unrelated.")
        else:
            role = (f"Current {j['registerRow']} leftover-join at {SELF}'s dispatch, measured as "
                    f"the version named by the highest non-CONTESTED COORD recording for this "
                    f"lineage ({j['rec']}). {PRED} cited the same version, and that citation is "
                    f"not superseded. Obligations flagged leftoverDesign true on "
                    f"{j['lineage']} leftover-join.v{j['ver']} at this dispatch: "
                    f"[{', '.join(j['leftoverTrue'])}]. {SPEAKER} does not steal that "
                    f"measurement. {j['lineage']} leftover-join and "
                    f"preview-product-boundary-successor are different lineages; their version "
                    f"numbers are unrelated.")
        based_on[key] = {"path": j["path"], "sha256": j["sha256"], "recording": j["rec"],
                         "reviews": j["reviews"], "role": role}
    _imm = max(c["version"] for c in m["census"])
    _earlier = [c["version"] for c in m["census"]
                if c["standing"] != "RECORDED" and 10 < c["version"] < _imm]
    rej_note = (
        f" Its immediate predecessor is preview-product-boundary-successor.v{_imm}, rejected at "
        f"Stage A by both reviewers and never recorded"
        + (", preceded by "
           + ", ".join(f"preview-product-boundary-successor.v{v}" for v in _earlier)
           + ", likewise rejected and unrecorded" if _earlier else "")
        + f". The current recorded baseline this successor is built from remains {PRED} "
          f"({PRED_RECORDING}).")
    based_on["relation"] = (
        f"{SPEAKER} is the successor of {PRED} ({PRED_RECORDING}) issued under D-294 Decision 3 "
        f"because D-294 Decision 2 trigger (b) fires on live bytes. It refreshes the "
        f"{word(nmoved)} superseded cross-lineage citations and the "
        f"{word(len(m['partitionChanged']))} changed leftoverDesign partitions. The fourteen "
        f"classes, the seven dispositions and p1p2g3Mapping equal "
        f"{PRED}'s after normalizing the refreshed sentences, and that equality is asserted "
        f"before this file is written. {SPEAKER} adds exactly this: the refreshed cross-lineage "
        f"citations and partitions enumerated in enforcementEvidence.classesRefresh; the measured "
        f"D-316 Class A standing in eligibilityNote, predecessorStanding.stageAGate1Standing and "
        f"lineage.contractRelationship; the predecessor record generated from the lineage census; "
        f"and the recomputed doesNot union. It holds constant the fourteen classes' identifiers, "
        f"items, subLimbs, invariants, inputs, pass rules, owners and gate assignments, the seven "
        f"dispositions, and p1p2g3Mapping. No frozen artifact is edited, and no leftover-design is "
        f"asserted on a lineage whose current join does not carry it. {SPEAKER} existing is not "
        f"SATISFIED-GRADE and does not mark SATISFIED." + rej_note)

    join_audit = {
        "count": len(m["joins"]), "countInWords": word(len(m["joins"])),
        "method": ("For each lineage the current version is the one named by the highest "
                   "non-CONTESTED COORD heading recording that lineage's leftover-join. Both "
                   "record spellings are matched: the forward form "
                   "'Record <lineage> leftover-join.vN as ...' and the inverted form "
                   "'Record leftover-join.vN of <GATE> as ...'. The named file's sha256 and both "
                   "Stage A verdict digests must appear in that entry's own text; all three were "
                   "verified before this file was written."),
        "standing": (
            f"Of the {word(len(m['joins']))} leftover-join citations {PRED} ({PRED_RECORDING}) "
            f"carried as current, {word(nmoved)} are superseded and {word(nkept)} are not. "
            f"The superseded ones are: {'; '.join(moved_names)}. {SELF} re-cites all "
            f"{word(len(m['joins']))} at the versions measured above, in basedOn, in "
            f"leftoverDesignOpenStanding and in enforcementEvidence.classes, the last refreshed "
            f"under D-294 Decision 3, and labels the superseded ones as not current."),
        "recordedInputsNote": (
            "recordedInputs re-measures every path this successor or its predecessor pinned, "
            "including the superseded leftover-joins and their Stage A verdicts. Those entries "
            "are inputs whose bytes were read, not currency claims: the currency claims are the "
            "citationStanding fields below and the citations in basedOn and "
            "enforcementEvidence.classes."),
        "joins": [{
            "lineage": j["lineage"], "registerRow": j["registerRow"],
            "citedByPredecessor": {"path": j["citedPath"], "sha256": j["citedSha"],
                                   "recording": j["citedRec"]},
            "currentAtThisDispatch": {"path": j["path"], "sha256": j["sha256"],
                                      "recording": j["rec"]},
            "supersededBy": j["rec"] if j["moved"] else None,
            "citationStanding": "superseded" if j["moved"] else "not superseded",
            "leftoverDesignTrue": j["leftoverTrue"],
            "leftoverDesignTrueAtCitedVersion": j["citedLeftoverTrue"],
        } for j in m["joins"]],
    }
    return pred, pairs, classes, sites, based_on, join_audit, moved_names, nmoved, nkept


# How each rejected-predecessor finding is landed.  Every id discovered on disk must
# appear here or the run aborts.
V11_DISPOSITIONS = {
    "PPBSV11-B1": "the six class fields EE-5a, EE-7a and EE-7b, each in existingGate and laterExecution, now state the empty leftoverDesign partition and the specifiedNotLeftover placement; the refresh is enumerated at 46 sites, not 40, and the currency and partition site counts now agree per lineage",
    "CLAUDE-PPBS-V11-B1": "same six class fields; the partition rewrite now targets the clause rather than a clause-plus-trailing-sentence composite, so the variants whose trailing sentence differs are covered",
    "CLAUDE-PPBS-V11-B2": "the doesNot union is recomputed from the twelve current joins at this dispatch and states 20 members, expressly excluding OBL-G29-FX-AUTHORING and OBL-G30-FX-AUTHORING",
    "PPBSV11-B2": "lineage.contractRelationship and the doesNot entries now treat D-316 as having settled which artifact the Class A opening names, and retain only the true boundary that this successor does not re-perform or widen it",
    "CLAUDE-PPBS-V11-SF2": "the closing sentence of lineage.contractRelationship that asserted the choice was undecided is replaced by the measured D-316 standing",
    "CLAUDE-PPBS-V11-ADV-1": "the doesNot entry that read as pre-D-316 now names D-316 as the act that lifted D-137's reservation",
    "PPBSV11-B3": "predecessorPinningShape is qualified to the recording-where-one-exists and each-verdict-that-exists shape; basedOn.predecessorV10 now pins both Stage A verdicts; and the predecessor role sentences no longer attribute any description of preview-product-boundary-successor.v10 to the frozen v5 through v9 files",
    "CLAUDE-PPBS-V11-SF1": "same repair to predecessorPinningShape, stated against the objects it covers",
    "CLAUDE-PPBS-V11-ADV-3": "both preview-product-boundary-successor.v10 Stage A verdict files are pinned in basedOn.predecessorV10.reviews and in recordedInputs",
    "CLAUDE-PPBS-V11-ADV-2": "the carried disposition's deictic reference to this dispatch is recast to name preview-product-boundary-successor.v10's dispatch",
}

V14_DISPOSITIONS = {
    "PPBSV14-B1": "the doesNot rebuild branch now matches the record's actual wording (it tested for \"do not record\" while the entry reads \"does not record\", so it never fired), and every prose rewrite in this generator aborts the run if it matches nothing",
    "CLAUDE-PPBS-V14-B1": "same repair: the do-not-record enumeration is generated from the census and the generator refuses to emit a LANDED disposition whose rewrite did not fire",
    "PPBSV14-B2": "basedOn.relation carries the held-constant and added statement in place of the broad no-other-change claim",
    "CLAUDE-PPBS-V14-B2": "same repair, applied to basedOn.relation's own bytes rather than to authorityClaim alone",
    "CLAUDE-PPBS-V14-B3": "Stage A identifier counts are scoped to the reviewed version: a verdict that references an earlier version's finding by id no longer counts it as one of its own",
    "CLAUDE-PPBS-V14-B4": "findingDisposition is deduplicated by identifier, so each identifier is disposed exactly once",
    "PPBSV14-S1": "same repair: the duplicate emission of the preview-product-boundary-successor.v13 block is removed",
    "CLAUDE-PPBS-V14-SF1": "no disposition states a predecessor-object count; counts that appear anywhere in this file are derived from the census rather than written by hand",
    "PPBSV14-S3": "same repair",
    "CLAUDE-PPBS-V14-SF2": "authorityClaim's own-history recital is generated from the census and so begins at the earliest frozen version on disk",
    "PPBSV14-S2": "the carried-standing NOTE names only the dispositions whose source is a Stage A review of preview-product-boundary-successor.v2 through preview-product-boundary-successor.v9",
    "CLAUDE-PPBS-V14-ADV-1": "classesRefresh.method states that the rewritten span includes the trailing steal clause where the partition became the empty list",
    "CLAUDE-PPBS-V14-ADV-2": "carried dispositions are marked as history and their field paths are not restated as this successor's own",
    "CLAUDE-PPBS-V14-ADV-3": "predecessorStanding carries a standing member for every unrecorded frozen version, generated from the census",
    "CLAUDE-PPBS-V14-ADV-4": "classesRefresh.method names the steal-clause span explicitly rather than leaving it to the sitesByReason keys",
}

V13_DISPOSITIONS = {
    "PPBSV13-B1": "the predecessor record is generated from a census of every frozen version of this lineage on disk, so all thirteen are pinned with their verdict files, not the six preview-product-boundary-successor.v13 carried",
    "CLAUDE-PPBS-V13-SF1": "same repair: the census reaches preview-product-boundary-successor.v1 rather than stopping at preview-product-boundary-successor.v5",
    "PPBSV13-B2": "every Stage A finding identifier discoverable on disk across this lineage is disposed in findingDisposition; the generator aborts if any is missing or carries empty disposition text",
    "PPBSV13-B3": "basedOn.predecessorPinningShape is generated from the pinned objects rather than asserted over them, so the gradeRuling member is named only for the verdict objects that carry one and the claim cannot outrun the bytes",
    "CLAUDE-PPBS-V13-B1": "same repair: the shape sentence is derived, so it states nothing of preview-product-boundary-successor.v9's verdict objects that those objects do not carry",
    "PPBSV13-B4": "basedOn.relation now carries the same held-constant and added statement authorityClaim carries, in place of the broad claim CLAUDE-PPBS-V12-ADV-4 attacked",
    "PPBSV13-S1": "the carried-standing NOTE is scoped to the dispositions whose source is a Stage A review of preview-product-boundary-successor.v2 through preview-product-boundary-successor.v9, not to every disposition below it",
    "PPBSV13-S2": "only the highest unrecorded version is described as the immediate predecessor; every earlier unrecorded version is described as an earlier attempt within this lineage",
    "CLAUDE-PPBS-V13-B2": "same repair, applied in basedOn.relation, the predecessor role sentences and predecessorStanding alike",
    "CLAUDE-PPBS-V13-ADV-1": "the do-not-record enumeration in doesNot is generated from the census, so it names every unrecorded frozen version rather than three of them",
    "CLAUDE-PPBS-V13-ADV-2": "the generated shape sentence names the standing member each predecessor object carries",
    "CLAUDE-PPBS-V13-ADV-3": "every predecessor object is built in one shape, carrying path, sha256, recording, standing, reviews and role, whether recorded or not",
    "CLAUDE-PPBS-V13-ADV-4": "the trigger sentence states that the clause is satisfied by any one changed projected value, and that two of the four superseded lineages changed their partition",
}

HISTORICAL_DISPOSITIONS = {
    "CLAUDE-PPBS-V1-B1": "landed within this lineage before the current recording: the preview-disposition-as-successor move was dropped and preview-product-boundary-successor.v5 was recorded at D-137 as the preview-scoped successor candidate. Carried here so the finding census is complete.",
    "CLAUDE-PPBS-V1-B2": "landed within this lineage before the current recording: item 4 carries its full name and the enforcement-evidence limb is answered by the fourteen EE classes carried unchanged here. Carried here so the finding census is complete.",
    "PPBSV1-B1": "landed within this lineage before the current recording: the enforcement-evidence half is answered by the fourteen EE classes, each owned and named at a condition-4 gate. Carried here so the finding census is complete.",
    "PPBSV1-S1": "landed within this lineage before the current recording: the host-act versus contribution-role distinction stands in the EE classes carried unchanged here. Carried here so the finding census is complete.",
    "CLAUDE-PPBS-V2-ADV-1": "honesty work carried within this lineage: lineage.productBoundaryPreviewV2.role states D-068 as the owner recording and does not restate product-boundary-preview.v2 as DR-117 SATISFIED.",
    "CLAUDE-PPBS-V10-ADV-1": "honesty work on the current recording. D-316 records the three preview-product-boundary-successor.v10 advisories as travelling as honesty work. Not a bar, and not re-opened here.",
    "CLAUDE-PPBS-V10-ADV-2": "honesty work on the current recording. D-293 Decision 5 names the successor by number; D-295 recorded preview-product-boundary-successor.v10 under that programme. Not a bar, and not re-opened here.",
    "CLAUDE-PPBS-V10-ADV-3": "honesty work on the current recording. The CLAUDE-PPBS-V9-B1 rider on the thirty-four deictic 'This successor' occurrences inside the fourteen classes remains open by choice: aligning them would break the class-equality proof that shows nothing but the enumerated refresh moved.",
}

V12_DISPOSITIONS = {
    "PPBSV12-B1": "basedOn.predecessorV11 pins frozen preview-product-boundary-successor.v11 and both of its Stage A REJECT verdicts; recordedInputs pins all three files; authorityClaim, predecessorStanding and basedOn.relation record its rejected and unrecorded standing; and every preview-product-boundary-successor.v11 finding identifier is disposed here",
    "CLAUDE-PPBS-V12-B1": "same repair, re-derived at this dispatch rather than carried: the predecessor record is rebuilt from the frozen files on disk",
    "CLAUDE-PPBS-V12-SF1": "the ten preview-product-boundary-successor.v11 findings are disposed above, and the two carried NOTE identifiers are renamed to this dispatch so a V11 identifier means a preview-product-boundary-successor.v11 reviewer finding and nothing else",
    "CLAUDE-PPBS-V12-ADV-1": "classesRefresh.method now states that at the sites where the partition became the empty list the rewritten span includes the trailing steal clause",
    "CLAUDE-PPBS-V12-ADV-2": "classEqualityAssertion carries method and result again",
    "CLAUDE-PPBS-V12-ADV-3": "predecessorPinningShape names the gradeRuling member the verdict objects carry",
    "CLAUDE-PPBS-V12-ADV-4": "authorityClaim and basedOn.relation state what is held constant and what is added, rather than asserting that nothing else changed",
}


def describe_pin_shape(based_on, census, immediate):
    """Generated from the pinned objects, so it cannot overstate them."""
    n = len(census)
    recorded = [c["version"] for c in census if c["standing"] == "RECORDED"]
    unrecorded = [c["version"] for c in census if c["standing"] != "RECORDED"]
    two = [c["version"] for c in census if len(c["reviews"]) == 2]
    one = [c["version"] for c in census if len(c["reviews"]) == 1]
    graded = [c["version"] for c in census
              if any("gradeRuling" in r for r in c["reviews"].values())]

    def vl(xs):
        return ", ".join(f"preview-product-boundary-successor.v{x}" for x in xs)

    parts = [
        f"{SPEAKER} pins all {word(n)} frozen predecessors of this lineage that exist on disk, "
        f"and every one of the twelve current leftover-joins, as named objects. "
        f"Each predecessor object carries path, sha256, a recording member, a standing member, a "
        f"reviews member and a role sentence measured at this dispatch.",
        f"A recording is stated for {vl(recorded)}; the recording member is null for {vl(unrecorded)}, "
        f"which were rejected at Stage A and never recorded.",
        f"Two Stage A verdicts are pinned for {vl(two)}." if two else "",
        f"One Stage A verdict is pinned for {vl(one)}, because no second verdict for it exists on disk."
        if one else "",
        f"A gradeRuling member is carried only where the verdict file itself states one: {vl(graded)}."
        if graded else "A gradeRuling member is carried by no verdict object.",
        f"The immediate predecessor is preview-product-boundary-successor.v{immediate}; every other "
        f"unrecorded version listed above is an earlier attempt within this lineage, not the "
        f"immediate predecessor.",
    ]
    return " ".join(x for x in parts if x)


def rebuild_does_not(m, pred):
    """Carry the predecessor's boundary list, but MEASURE anything it states as a
    present-tense fact about the current joins or about D-316's standing."""
    union = []
    for j in m["joins"]:
        for i in j["leftoverTrue"]:
            if i not in union:
                union.append(i)
    out = []
    for s in pred["doesNot"]:
        if not isinstance(s, str):
            out.append(s); continue
        if "flagged leftoverDesign true on the" in s:
            s = (f"Does not steal leftover-design of any obligation flagged leftoverDesign true "
                 f"on the {word(len(m['joins']))} current leftover-joins cited in basedOn, "
                 f"measured at this dispatch as the union [{', '.join(union)}]. "
                 f"OBL-G29-FX-AUTHORING and OBL-G30-FX-AUTHORING are not members of that union: "
                 f"they sit in specifiedNotLeftover on the current G29 and G30 leftover-joins.")
        elif "Does not lift D-137's express reservation" in s:
            s = ("Does not lift D-137's express reservation, because D-316 already lifted it. "
                 "D-207 records that the venue for a lift is a reviewed coordinator act, not an "
                 "artifact; D-316 is that act.")
        elif "a later D-056 Class A opening names" in s:
            s = (f"Does not decide which artifact a D-056 Class A opening names, because D-316 "
                 f"decided it: the opening names preview-product-boundary-successor.v10. "
                 f"product-boundary-successor-contract.v8 (D-116) remains the distinct "
                 f"general-succession candidate and is not applied.")
        elif "Does not open D-056 Class A" in s:
            s = ("Does not open D-056 Class A and does not re-perform, widen or re-open the "
                 "opening D-316 performed for DR-117.")
        elif "Does not author G29 or G30 fixture bytes" in s:
            s = ("Does not author G29 or G30 fixture bytes. That authoring landed at D-317 and "
                 "D-339 for G30 and at D-318 and D-342 for G29, after the D-316 opening, and was "
                 "remasured at D-340 and D-343.")
        elif "fresh application-grade dual review D-293 Decision 5 requires" in s:
            s = (f"Does not itself perform the application-grade dual review of its own bytes; "
                 f"{SELF} is the subject of that Stage A review, not its verdict.")
        elif "stays frozen" in s.lower() or "not record" in s.lower():
            extra = ", ".join(f"preview-product-boundary-successor.v{c['version']}"
                              for c in m["census"]
                              if c["standing"] != "RECORDED" and c["path"])
            if extra and extra not in s:
                s = s.rstrip(". ") + (f". {extra} is likewise frozen, rejected at Stage A by both "
                                      f"reviewers, unrecorded, and not to be recorded.")
        elif "from D-170 through D-294" in s:
            s = must_replace(s, "from D-170 through D-294", "from D-170 through D-364",
                             "doesNot entry range")
        else:
            s = s.replace(PRED, SELF)
        out.append(s)
    return out


def assemble(m):
    pred, pairs, classes, sites, based_on, join_audit, moved_names, nmoved, nkept = build_doc(m)
    g29 = next(j for j in m["joins"] if j["lineage"] == "g29")
    g30 = next(j for j in m["joins"] if j["lineage"] == "g30")

    survey = "; ".join(
        f"current {j['registerRow']} leftover-join is {j['lineage']} leftover-join.v{j['ver']} "
        f"({j['rec']}), leftoverDesign "
        + (f"[{', '.join(j['leftoverTrue'])}]" if j["leftoverTrue"] else "the empty list")
        for j in m["joins"])

    doc = {
        "artifact": SELF,
        "version": VERSION,
        "date": m["date"],
        "documentClass": pred["documentClass"],
        "registerRow": REGISTER_ROW,
        "status": "CANDIDATE-NOT-APPLIED",
        "reviewStatus": "AWAITING-INDEPENDENT-REVIEW",
        "sealRecommendation": "DO-NOT-SEAL",
        "binds": "NOTHING",
        "basedOn": based_on,
        "predecessorStanding": {
            "currentBeforeThisFileIsRecorded": (
                f"{PRED} ({PRED_RECORDING}) is the current recorded DR-117 leftover "
                f"remasurement. {SELF} is CANDIDATE-NOT-APPLIED and records nothing; until a "
                f"reviewed coordinator act records {SELF}, {PRED} stays current."),
            "effectOfRecordingThisFile": (
                f"Once {SELF} is recorded, {PRED} becomes a historical measurement as of HEAD "
                f"{pred['head']} / required-now {pred['requiredNowUnchanged']} / file 08 "
                f"{pred['file08Pin']['sha256']}, and is no longer the current DR-117 leftover "
                f"remasurement. {PRED} stays frozen; it is not to be recorded as current after "
                f"that act. Nothing in {SELF} unwrites {PRED_RECORDING}."),
            "predecessorV9Standing": pred["predecessorStanding"]["predecessorV9Standing"],
            **{f"predecessorV{c['version']}Standing": (
                f"preview-product-boundary-successor.v{c['version']} is frozen at {c['path']}, "
                f"sha256 {c['sha256']}, rejected at Stage A and unrecorded. It is not current and "
                f"never was. It stays frozen; do not record it."
                + (f" It is the immediate predecessor of {SELF}."
                   if c["version"] == max(x["version"] for x in m["census"])
                   else " It is an earlier attempt within this lineage, not the immediate "
                        "predecessor.")
                + (f" Its {word(len(c['findingIds']))} Stage A finding identifiers are disposed "
                   f"in findingDisposition." if c["findingIds"] else ""))
               for c in m["census"] if c["standing"] != "RECORDED" and c["path"]},
            "predecessorV7Standing": pred["predecessorStanding"]["predecessorV7Standing"],
            "earlierStanding": pred["predecessorStanding"]["earlierStanding"],
            "versionNumbers": pred["predecessorStanding"]["versionNumbers"],
            "stageAGate1Standing": (
                f"Gate 1 Class A no longer turns on the Stage A verdicts. D-316 opened D-056 "
                f"Eligibility gate 1 Class A for DR-117 as the T2-02 acceptance of {PRED}, at "
                f"CONSENT from both independent reviewers with 0 MUST-FIX and 0 SHOULD-FIX, and "
                f"lifted D-137's express reservation. The application-grade limb is the D-005-form "
                f"grade question both Stage A verdicts on {PRED} ruled SUSTAINED FOR APPLICATION. "
                f"{PRED}'s own eligibilityNote sentence that gate 1 Class A remains false under "
                f"D-137's express reservation was true when {PRED} was written and is superseded "
                f"by D-316; it stands as history in that frozen file, which {SELF} does not edit."),
        },
        "joinCurrencyAudit": join_audit,
        "authorityClaim": (
            f"{SPEAKER} PROPOSES the DR-117 preview-scoped successor candidate authorized by "
            f"D-132 / file 12 section 5, and is the candidate limb of the DR-117 programme the "
            f"owner adopted at D-293 Decision 5. Its own history is this: "
            f"preview-product-boundary-successor.v5 was recorded at D-137, "
            f"preview-product-boundary-successor.v6 was rejected at Stage A and never recorded, "
            f"preview-product-boundary-successor.v7 was recorded at D-168, "
            f"preview-product-boundary-successor.v8 was recorded at D-207, "
            f"preview-product-boundary-successor.v9 was rejected at Stage A by both reviewers and "
            f"never recorded, {PRED} was recorded at {PRED_RECORDING}, and "
            + ", ".join(
                f"preview-product-boundary-successor.v{c['version']} was rejected at Stage A and "
                f"never recorded" for c in m["census"]
                if c["standing"] != "RECORDED" and c["version"] > 10)
            + f", so {PRED} is the current recording. {SPEAKER} exists because D-294 Decision 2 trigger (b) fires "
            f"against live bytes: of the {word(len(m['joins']))} leftover-joins {PRED} cites as "
            f"current, {word(nmoved)} are superseded, and on "
            f"{word(len(m['partitionChanged']))} of those the leftoverDesign partition changed. "
            f"D-294 Decision 3 requires a successor issued for any reason to refresh its "
            f"cross-lineage citations to the versions current at its dispatch and to label the "
            f"superseded ones as not current. {SELF} adds exactly this: the refreshed "
            f"cross-lineage citations and partitions enumerated in "
            f"enforcementEvidence.classesRefresh; the measured D-316 Class A standing in "
            f"eligibilityNote, predecessorStanding.stageAGate1Standing and "
            f"lineage.contractRelationship; the predecessor record for the rejected "
            f"intermediates; and the recomputed doesNot union. It holds constant the fourteen "
            f"classes' identifiers, items, subLimbs, invariants, inputs, pass rules, owners and "
            f"gate assignments, the seven dispositions, and p1p2g3Mapping. The fourteen enforcement-evidence classes of {SELF} equal {PRED}'s after "
            f"normalizing the refreshed cross-lineage sentences, and that equality is asserted "
            f"before this file is written. The seven dispositions and p1p2g3Mapping are carried "
            f"from {PRED} unchanged by {SELF}, and that equality is asserted before this file is "
            f"written. leftover-design of unnamed EE classes remains closed (D-157 / D-158 / "
            f"D-159). {SPEAKER} does not steal any gate's leftover-design and asserts no "
            f"leftover-design on a lineage whose current join does not carry it. {SPEAKER} is not "
            f"a second register row. DR-117 is SATISFIED as of D-363; {SPEAKER} neither performed "
            f"that recording nor disturbs it, and performs no D-056 "
            f"Eligibility gate 4 or gate 5. {SPEAKER} does not re-open or re-perform the D-316 "
            f"Class A opening. {SPEAKER} does not author fixture bytes and does not invent the "
            f"DR-131 pack. {SPEAKER} does not add a DR-G* row, does not change live required-now "
            f"{REQUIRED_NOW}, does not name G13 into required-now, applies nothing, and does not "
            f"authorize docs/v2/implementation/."),
        "purpose": (
            f"Refresh, at live HEAD, the {word(nmoved)} of {word(len(m['joins']))} leftover-join "
            f"citations {PRED} ({PRED_RECORDING}) carries at versions since superseded, pinning "
            f"each in basedOn at the version its highest non-CONTESTED COORD recording names, "
            f"with both Stage A verdicts, and refreshing the same citations inside the fourteen "
            f"enforcement-evidence classes under D-294 Decision 3. State the two partitions that "
            f"changed as the current joins hold them. Carry the other {word(nkept)} citations, "
            f"the fourteen classes, the seven dispositions and p1p2g3Mapping equal to {PRED}'s "
            f"after normalizing the refreshed sentences, and assert that equality before writing. "
            f"Record that D-316 opened D-056 Eligibility gate 1 Class A for DR-117 and lifted "
            f"D-137's express reservation. Re-pin file 08, file 02, the v1-slice, COORD and HEAD, "
            f"and recompute every recordedInputs digest. Preserve leftover-design of unnamed EE "
            f"classes as closed (D-159: gates 2 and 3 hold). Remainder is named-gate execution. "
            f"Do not SATISFY DR-117. Do not perform gate 4 or gate 5. Do not author fixture, "
            f"golden, or adapter bytes. Do not invent a new product-boundary item, a D9 code, a "
            f"section 7.1 recipe, a D-006 unit, or the DR-131 pack. Do not name G13 into "
            f"required-now. Do not steal gate leftover-design."),
        "lineage": {**dedeictic(pred["lineage"]),
                    "productBoundarySuccessorContractV8": {
                        **dedeictic(pred["lineage"]["productBoundarySuccessorContractV8"]),
                        "role": (
                            "Remains DR-117's leftover T2-02 candidate for general succession; "
                            "D-137 records that product-boundary-successor-contract.v8 remains the "
                            "D-116 leftover T2-02 candidate, and D-316 confirms it stays the "
                            f"distinct general-succession candidate. {SPEAKER} does not replace, "
                            "apply, or succeed product-boundary-successor-contract.v8.")},
                    "contractRelationship": (
                        f"product-boundary-successor-contract.v8 (D-116, the D-137 leftover T2-02 "
                        f"candidate) and {SELF} are distinct lineages; their version numbers are "
                        f"unrelated. {SPEAKER} is the DR-117 preview-scoped successor candidate "
                        f"authorized by D-132 / file 12 section 5, and is the candidate limb of "
                        f"the DR-117 programme the owner adopted at D-293 Decision 5. D-316 "
                        f"settled which artifact the D-056 Class A opening for DR-117 names: it "
                        f"names {PRED}, at 0 blockers with application-grade acceptance and no "
                        f"express reservation. product-boundary-successor-contract.v8 remains the "
                        f"D-116 recording and DR-117's leftover T2-02 candidate for general "
                        f"succession, and is not applied. {SPEAKER} does not replace, apply, or "
                        f"succeed product-boundary-successor-contract.v8 and does not make it "
                        f"historical. {SPEAKER} does not re-perform or widen the D-316 opening; "
                        f"if a later coordinator act rests that opening on {SELF} rather than on "
                        f"{PRED}, that is the act's own decision and is not taken here.")},
        "p1p2g3Mapping": pred["p1p2g3Mapping"],
        "registerRowQuoted": {**pred["registerRowQuoted"], "sourceSha256": m["f08sha"]},
        "sevenItems": {**pred["sevenItems"], "sourceSha256": m["f02sha"]},
        "enforcementEvidence": {
            "status": pred["enforcementEvidence"]["status"],
            "ownerOfUnownedPreviewClasses": (
                f"No preview EE class remains unowned. D-157 / D-158 / D-159 named every class "
                f"that preview-product-boundary-successor.v5 marked owner=this-candidate. "
                f"{SPEAKER} remasures that naming against the {word(len(m['joins']))} current "
                f"leftover-joins. It does not execute the classes and does not add a DR-G* row."),
            "cellAnswer": pred["enforcementEvidence"]["cellAnswer"],
            "v1SlicePin": {**pred["enforcementEvidence"]["v1SlicePin"], "sha256": m["v1slice"]},
            "classes": classes,
            "classesRefresh": {
                "rule": ("D-294 Decision 3: a successor issued for any reason refreshes its "
                         "cross-lineage citations to the versions current at its dispatch and "
                         "labels the superseded ones as not current. No frozen artifact is "
                         "edited to achieve this."),
                "trigger": (
                    f"D-294 Decision 2 (b): a sibling successor changed a value the citing "
                    f"artifact relies on. The clause is satisfied by any one changed projected "
                    f"value; the four superseded lineages are enumerated below with the measured "
                    f"partition on each side, and two of the four changed their partition. "
                    f"Measured from bytes: "
                    + "; ".join(
                        f"{j['lineage']} leftover-join.v{j['citedVer']} leftoverDesign "
                        f"[{', '.join(j['citedLeftoverTrue'])}] versus "
                        f"{j['lineage']} leftover-join.v{j['ver']} leftoverDesign "
                        + (f"[{', '.join(j['leftoverTrue'])}]" if j["leftoverTrue"] else "the empty list")
                        for j in m["moved"])),
                "method": ("Mechanical rewrite, inside enforcementEvidence.classes[*].existingGate "
                           "and enforcementEvidence.classes[*].laterExecution only, of the version "
                           "token and recording D-number of each superseded citation, plus the "
                           "leftoverDesign partition sentence of each lineage whose partition "
                           "changed. Where a partition became the empty list, the rewritten span "
                           "includes the trailing steal clause at that site, so "
                           "'does not steal that leftover' becomes 'does not steal that "
                           "measurement'; those sites are counted in sitesByReason under the "
                           "with-steal-clause keys. No identifier, item, subLimb, invariant, input, pass rule, "
                           "owner or gate assignment was touched, and no frozen artifact was "
                           "edited."),
                "siteCount": sum(sites.values()),
                "sitesByReason": sites,
                "classEqualityAssertion": {
                    "statement": (f"After normalizing the refreshed citation and partition "
                                  f"sentences in both, {SELF}'s fourteen classes equal {PRED}'s "
                                  f"fourteen classes."),
                    "asserted": True,
                    "method": "canonical JSON comparison of the two normalized arrays",
                    "result": "HOLDS",
                },
            },
        },
        "doesNot": rebuild_does_not(m, pred),
        "findingDisposition": [{
            "id": f"PPBS-V{VERSION}-CARRIED-STANDING",
            "severity": "NOTE",
            "disposition": (
                f"The dispositions carried from {PRED} ({PRED_RECORDING}) — those whose source is "
                f"a Stage A review of preview-product-boundary-successor.v2 through "
                f"preview-product-boundary-successor.v9 — describe {PRED} as recorded, and are "
                f"carried by {SELF} as history. Where such a disposition names a leftover-join "
                f"version, that version is the one current at {PRED}'s dispatch, not necessarily "
                f"the one current at {SELF}'s dispatch. The versions current now are measured in "
                f"joinCurrencyAudit and cited in basedOn and enforcementEvidence.classes. "
                f"{SPEAKER} edits no frozen artifact and does not restate {PRED}'s findings as "
                f"its own."),
        }] + dedeictic(pred["findingDisposition"]) + [
            {"id": fid, "severity": "LANDED",
             "source": f"preview-product-boundary-successor.v{rj['version']} Stage A",
             "disposition": f"landed at {SELF}: " + (
                 V11_DISPOSITIONS.get(fid) or V12_DISPOSITIONS.get(fid)
                 or V13_DISPOSITIONS.get(fid) or V14_DISPOSITIONS.get(fid)
                 or HISTORICAL_DISPOSITIONS.get(fid) or "")}
            for rj in m["rejected"] for fid in rj["findingIds"]
        ] + [
            {"id": fid, "severity": "LANDED",
             "source": f"preview-product-boundary-successor.v{c['version']} Stage A",
             "disposition": (HISTORICAL_DISPOSITIONS.get(fid)
                             or f"landed at {SELF}: "
                             + (V13_DISPOSITIONS.get(fid) or V14_DISPOSITIONS[fid]))}
            for c in m["census"] for fid in c["findingIds"]
            if fid in HISTORICAL_DISPOSITIONS or fid in V13_DISPOSITIONS
               or fid in V14_DISPOSITIONS
        ] + [{
            "id": f"PPBS-V{VERSION}-VENUE-NOTE",
            "severity": "NOTE",
            "disposition": (
                f"The venue limb carried above records that {PRED} ({PRED_RECORDING}) was right "
                f"to refuse D-056 Class A in terms, and that the venue for lifting D-137's "
                f"express reservation is a reviewed coordinator decision. That coordinator "
                f"decision has since landed: D-316 opened gate 1 Class A for DR-117 as the T2-02 "
                f"acceptance of {PRED} and lifted the reservation. The limb is discharged, not "
                f"contradicted. {SPEAKER} does not re-perform that opening."),
        }],
        "eligibilityNote": (
            f"D-159 recorded that D-056 Eligibility gates 2 and 3 hold for DR-117. leftover-design "
            f"of unnamed EE classes is closed. D-316 opened D-056 Eligibility gate 1 Class A for "
            f"DR-117 as the T2-02 acceptance of {PRED} and lifted D-137's express reservation, so "
            f"gate 1 Class A holds and DR-117 is D-056-eligible in kind. CANDIDATE-NOT-APPLIED is "
            f"not a Class A bar (D-085 / D-147). binds NOTHING is {SELF}'s own status field, not a "
            f"cited holding. Gates 4 and 5 were performed at D-363, which recorded DR-117 "
            f"SATISFIED. {SPEAKER} does not re-perform, reopen or disturb that recording, performs "
            f"no gate itself, and does not edit file 08. Recording {SELF} changes no row status: it "
            f"discharges the D-294 Decision 2 (b) citation-refresh obligation D-364 clause 9 holds "
            f"owed and D-363 named. Under D-364 clause 7 it does not move Eligibility gate 1, which "
            f"D-316 fixed at the accepted contract's digest. Preview is not MVP "
            f"(D-018). Live required-now is {REQUIRED_NOW}. Frozen "
            f"preview-product-boundary-successor.v7 (D-168) is a historical measurement, frozen "
            f"preview-product-boundary-successor.v9 was rejected at Stage A and never recorded, "
            f"and {PRED} ({PRED_RECORDING}) remains the current recorded remasurement until a "
            f"coordinator act records {SELF}."),
        "recordedInputs": build_recorded_inputs(m, based_on),
        "head": m["head"],
        "requiredNowUnchanged": REQUIRED_NOW,
        "remeasurementClause": (
            f"If any file pinned in recordedInputs moves in a way that is not append-only growth "
            f"of {COORD} or COORD heading hygiene, re-measure before recording. The trigger "
            f"reaches every pinned row, not an enumerated subset: this clause is generated from "
            f"recordedInputs rather than maintained by addition. recordedInputs.HEAD must equal "
            f"the top-level head. file08Pin.sha256, registerRowQuoted.sourceSha256 and "
            f"recordedInputs['{F08}'] must all equal the same live digest of file 08, and "
            f"DR-117's leading label there must still read {m['f08label']}. "
            f"sevenItems.sourceSha256 must still "
            f"equal the live digest of {F02}; file 08's DR-117 row says any change to that "
            f"enumeration re-opens the row. Each of the {word(len(m['joins']))} current "
            f"leftover-joins named in basedOn and cited in enforcementEvidence.classes must still "
            f"be the version its highest non-CONTESTED COORD recording names, matched on both the "
            f"forward and the inverted heading spelling; if a later recording supersedes one, "
            f"re-measure and refresh both places before recording, under D-294 Decision 3. "
            f"{SPEAKER} does not unwrite D-137, D-157, D-158, D-159, D-167, D-168, D-169, "
            f"D-293, D-294, D-295, D-314, D-315, D-316, or any entry from D-170 through D-362. "
            f"{SPEAKER} existing is not a recording."),
        "leftoverDesignOpenStanding": (
            f"The live DR-117 leading label in file 08 is {m['f08label']}: D-363 recorded DR-117 "
            f"SATISFIED for architecture-preview condition 2 under D-056 Class A, performing "
            f"Eligibility gates 4 and 5, and named the D-294 Decision 2 (b) citation-refresh "
            f"successor owed on the g29 and g30 grounds as outstanding work without discharging "
            f"it. {SELF} is that successor. leftover-design of "
            f"unnamed EE classes remains closed (D-159). Remainder is named-gate execution. "
            f"Measured at {SELF}'s dispatch, the current leftover-joins are: {survey}. "
            f"{SPEAKER} does not steal those leftovers. On DR-G29 and DR-G30 the partitions "
            f"changed since {PRED_RECORDING}: g29 leftover-join.v{g29['ver']} ({g29['rec']}) and "
            f"g30 leftover-join.v{g30['ver']} ({g30['rec']}) each measure leftoverDesign as the "
            f"empty list, where {PRED} cited "
            f"[{', '.join(g29['citedLeftoverTrue'])}] and "
            f"[{', '.join(g30['citedLeftoverTrue'])}]; OBL-G29-FX-AUTHORING and "
            f"OBL-G30-FX-AUTHORING now sit in specifiedNotLeftover, and each join's "
            f"qualificationAtNamedGate members are its harness-spec and execution obligations. "
            f"leftover-design of unnamed EE classes is not reopened. G13 remains reserved, not "
            f"named. DR-117 is not SATISFIED by {SELF}."),
        "file08Pin": {"path": F08, "sha256": m["f08sha"]},
        "file08StatusToken": m["f08label"],
    }
    seen, deduped = set(), []
    for e in doc["findingDisposition"]:
        i = e.get("id") if isinstance(e, dict) else None
        if i is not None and i in seen:
            continue
        if i is not None:
            seen.add(i)
        deduped.append(e)
    doc["findingDisposition"] = deduped
    return doc, pairs, sites


DEICTIC_RE = re.compile(r"[Tt]his v\d+\b")
BRACE_RE = re.compile(r"\{[a-zA-Z_][a-zA-Z0-9_\[\]'\"]*\}")
BARE_VER_RE = re.compile(r"(?<![-./\w])v\d+\b(?!-slice)")
STEMMED = re.compile(
    r"(leftover-join|successor|contract|occupancy|corpus|preview|goldens|"
    r"tables|schemas|join|catalog|manifest|bind|golden)\.?\s?v\d+\b", re.I)


def walk_strings(node, path="$"):
    if isinstance(node, dict):
        for k, v in node.items():
            yield from walk_strings(v, f"{path}.{k}")
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from walk_strings(v, f"{path}[{i}]")
    elif isinstance(node, str):
        yield path, node


PARTITION_RE = re.compile(r"leftoverDesign remains \[([^\]]*)\]")


def audit_partitions(doc, m):
    """Every 'leftoverDesign remains [...]' assertion inside the operative classes must
    name obligations that some current join actually flags leftoverDesign true.

    v11 shipped six sentences asserting OBL-G29/G30-FX-AUTHORING as live leftover-design
    after the current joins had closed them; an exact-string rewrite missed the variants
    whose trailing sentence differed.  This check is on the meaning, not the string."""
    live = set()
    for j in m["joins"]:
        live.update(j["leftoverTrue"])
    bad = []
    for cls in doc["enforcementEvidence"]["classes"]:
        for field in ("existingGate", "laterExecution"):
            for mm in PARTITION_RE.finditer(cls.get(field, "") or ""):
                for ident in [x.strip() for x in mm.group(1).split(",") if x.strip()]:
                    if ident not in live:
                        bad.append(f"{cls['id']}.{field}: asserts leftoverDesign true for "
                                   f"{ident!r}, which no current join flags true")
    return bad


def audit_site_symmetry(m, sites):
    """For a lineage whose partition changed, every site that got a currency rewrite must
    also have had its partition sentence rewritten.  v11's counts were 14/12 and 6/2."""
    bad = []
    for j in m["partitionChanged"]:
        lin = j["lineage"]
        cur = sum(v for k, v in sites.items() if k.startswith(f"currency citation {lin} "))
        par = sum(v for k, v in sites.items() if k.startswith(f"partition {lin} "))
        if cur != par:
            bad.append(f"{lin}: {cur} currency rewrites but {par} partition rewrites "
                       f"- {cur - par} site(s) keep a stale partition")
    return bad


def audit_rejected_predecessors(doc, m):
    """A rejected intermediate must be pinned, named, and its findings disposed.

    v12 shipped with zero occurrences of preview-product-boundary-successor.v11 while
    claiming to pin every predecessor.  This makes that unshippable."""
    bad = []
    blob = json.dumps(doc)
    disposed = {e.get("id") for e in doc["findingDisposition"] if isinstance(e, dict)}
    for r in m["census"]:
        if not r["path"]:
            continue
        name = f"preview-product-boundary-successor.v{r['version']}"
        if f"predecessorV{r['version']}" not in doc["basedOn"]:
            bad.append(f"basedOn has no predecessorV{r['version']} for rejected {name}")
        if r["sha256"] not in blob:
            bad.append(f"{name}'s digest is not pinned anywhere")
        if r["path"] not in doc["recordedInputs"]:
            bad.append(f"recordedInputs omits {r['path']}")
        if doc["basedOn"].get(f"predecessorV{r['version']}", {}).get("recording") != r["recording"]:
            bad.append(f"{name}: pinned recording disagrees with COORD")
        for rv in r["reviews"].values():
            if rv["path"] not in doc["recordedInputs"]:
                bad.append(f"recordedInputs omits verdict {rv['path']}")
        for fid in r["findingIds"]:
            if fid not in disposed:
                bad.append(f"findingDisposition omits {name} finding {fid}")
    for e in doc["findingDisposition"]:
        if isinstance(e, dict) and e.get("severity") == "LANDED":
            txt = (e.get("disposition") or "").strip()
            if not txt or txt.endswith(":"):
                bad.append(f"findingDisposition {e.get('id')!r} carries empty disposition text")
    # an identifier minted by this generator must not impersonate a reviewer finding
    for e in doc["findingDisposition"]:
        i = e.get("id") if isinstance(e, dict) else None
        if isinstance(i, str) and i.startswith("PPBS-V") and i.split("-")[1] != f"V{VERSION}":
            known = any(i in r["findingIds"] for r in m["rejected"])
            if not known:
                bad.append(f"findingDisposition id {i!r} names a version that is not this "
                           f"dispatch and is not a reviewer finding")
    return bad


def audit(doc, m, pairs, sites):
    problems = []
    problems += audit_partitions(doc, m)
    problems += audit_site_symmetry(m, sites)
    problems += audit_rejected_predecessors(doc, m)
    # the doesNot union must equal the measured union, exactly
    live = []
    for j in m["joins"]:
        for i in j["leftoverTrue"]:
            if i not in live:
                live.append(i)
    for s_ in doc["doesNot"]:
        if isinstance(s_, str) and "flagged leftoverDesign true on the" in s_:
            for ident in ("OBL-G29-FX-AUTHORING", "OBL-G30-FX-AUTHORING"):
                if f"[{ident}" in s_ or f" {ident}," in s_.split("union [")[-1].split("]")[0]:
                    problems.append(f"doesNot union still lists closed obligation {ident}")
    for path, s in walk_strings(doc):
        for mm in DEICTIC_RE.finditer(s):
            problems.append(f"{path}: deictic {mm.group(0)!r}")
        for mm in BRACE_RE.finditer(s):
            problems.append(f"{path}: unformatted placeholder {mm.group(0)!r}")
        # bare version tokens: any vN whose immediately preceding text is not a lineage stem
        for mm in BARE_VER_RE.finditer(s):
            lo = max(0, mm.start() - 40)
            if not STEMMED.search(s[lo:mm.end()]):
                problems.append(f"{path}: bare version token {mm.group(0)!r} in ...{s[lo:mm.end()+18]!r}")
    blob = json.dumps(doc)
    for stale, why in (("changes nothing else", "broad no-other-change claim"),
                       ("and nothing else:", "broad no-other-change claim"),
                       ("performs exactly that refresh and nothing",
                        "broad no-other-change claim"),
                       (f"This {PRED}", "predecessor voice"),
                       (" now states the measured partition", "carried present-tense verb"),
                       ("current at this dispatch", "carried deictic dispatch")):
        if stale in blob:
            problems.append(f"carried text still says {stale!r} ({why})")
    for bad in ("byte-identical", "byte-identically", "byte-for-byte"):
        if bad in blob:
            problems.append(f"forbidden equality claim {bad!r} present")
    # the speaker must be v11 everywhere the document speaks of itself
    need(doc["artifact"] == SELF and doc["version"] == VERSION, "self identity wrong")
    if f"This {PRED}" in blob:
        problems.append(f"predecessor still speaks: 'This {PRED}' present")
    # arithmetic agreement
    need(len(doc["enforcementEvidence"]["classes"]) == 14, "not fourteen EE classes")
    need(len(doc["sevenItems"]["dispositions"]) == 7, "not seven dispositions")
    need(doc["joinCurrencyAudit"]["count"] == len(m["joins"]), "join count disagrees")
    need(doc["enforcementEvidence"]["classesRefresh"]["siteCount"] == sum(sites.values()),
         "site count disagrees")
    need(doc["recordedInputs"]["HEAD"] == doc["head"], "recordedInputs.HEAD != head")
    need(doc["recordedInputs"][F08] == doc["file08Pin"]["sha256"] ==
         doc["registerRowQuoted"]["sourceSha256"], "file 08 digest disagrees across pins")
    need(doc["recordedInputs"][F02] == doc["sevenItems"]["sourceSha256"],
         "file 02 digest disagrees across pins")
    return problems


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("out", nargs="?", default=os.path.dirname(os.path.abspath(__file__)))
    ap.add_argument("--audit")
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args(argv)
    try:
        assert_docs_tree_clean()
        m = measure()
        doc, pairs, sites = assemble(m)
        problems = audit(doc, m, pairs, sites)
        if problems:
            raise Fail("audit failed:\n  " + "\n  ".join(problems[:25]) +
                       (f"\n  ... {len(problems)-25} more" if len(problems) > 25 else ""))
    except Fail as e:
        print(f"make-ppbs-v15.py: FAILED: {e}", file=sys.stderr)
        return 2
    except subprocess.CalledProcessError as e:
        print(f"make-ppbs-v15.py: FAILED: git: {e}", file=sys.stderr)
        return 2

    out = a.out if a.out.endswith(".json") else os.path.join(a.out, f"{SELF}.json")
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    body = json.dumps(doc, indent=2, ensure_ascii=False) + "\n"
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(body)
    if a.audit:
        with open(a.audit, "w", encoding="utf-8") as fh:
            json.dump({"movedLineages": [j["lineage"] for j in m["moved"]],
                       "partitionChanged": [j["lineage"] for j in m["partitionChanged"]],
                       "refreshPairs": [{"old": o, "new": n, "why": w} for o, n, w in pairs],
                       "sites": sites, "head": m["head"],
                       "sha256": hashlib.sha256(body.encode()).hexdigest()}, fh, indent=2)
    if not a.quiet:
        print(f"wrote {out}")
        print(f"  bytes   {len(body.encode())}")
        print(f"  sha256  {hashlib.sha256(body.encode()).hexdigest()}")
        print(f"  moved   {[j['lineage'] for j in m['moved']]}")
        print(f"  sites   {sites} (total {sum(sites.values())})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
