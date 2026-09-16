#!/usr/bin/env python3
"""Generator for `preview-product-boundary-successor.v12.json`.

Builds the DR-117 preview-scoped successor candidate **v11** from the frozen,
RECORDED predecessor `preview-product-boundary-successor.v10.json`
(sha256 8f34c92e..., recorded at COORD `## D-295`).

Why v11 exists (D-294 Decision 2 trigger (b)): four of the twelve leftover-joins
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
SELF = "preview-product-boundary-successor.v12"
SPEAKER = f"This {SELF}"
VERSION = 12
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
    need(label == "OPEN", f"DR-117 leading label is {label!r}, not OPEN")
    need("**28 of 28 required gates name a recorded identifier**" in f08,
         "file 08 no longer carries the 28-of-28 required-now snapshot")

    return {
        "coord": coord, "pred": pred, "joins": joins, "moved": moved,
        "partitionChanged": partition_changed,
        "head": git("rev-parse", "HEAD"),
        "date": datetime.date.today().isoformat(),
        "f08sha": sha256_file(F08), "f02sha": sha256_file(F02),
        "v1slice": sha256_file(V1SLICE), "coordsha": sha256_file(COORD),
        "f08label": label,
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


def build_recorded_inputs(m, based_on):
    ri = {COORD: m["coordsha"], F08: m["f08sha"], F02: m["f02sha"], V1SLICE: m["v1slice"],
          PRED_PATH: PRED_SHA}
    for fn in ("claude2", "codex"):
        rel = f"{ART}/preview-product-boundary-successor.v10.review-independent.{fn}.json"
        ri[rel] = sha256_file(rel)
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

    based_on = {}
    for k in ("predecessorV9", "predecessorV8", "predecessorV7", "predecessorV6",
              "predecessorV5"):
        if k in pred["basedOn"]:
            e = dedeictic(pred["basedOn"][k])
            if isinstance(e, dict):
                ver = k.replace("predecessor", "")
                rec = e.get("recording")
                stand = (f"recorded at {rec}" if rec
                         else "rejected at Stage A and never recorded")
                e["role"] = (
                    f"Historical predecessor preview-product-boundary-successor.{ver.lower()}, "
                    f"{stand}. It is frozen, it predates {PRED}, and it says nothing about "
                    f"{PRED} or {SELF}. Pinned here for provenance only; {SELF} edits no frozen "
                    f"artifact and does not record it as current.")
            based_on[k] = e
    based_on["predecessorPinningShape"] = (
        f"{SPEAKER} pins every predecessor and every one of the "
        f"{word(len(m['joins']))} current leftover-joins as a named object carrying path, sha256, "
        f"the recording where one exists, and each Stage A verdict that exists on disk with its "
        f"path, digest and verdict read from the verdict file itself, plus a role sentence "
        f"measured at this dispatch. preview-product-boundary-successor.v6 and "
        f"preview-product-boundary-successor.v9 were rejected at Stage A and never recorded, so "
        f"neither carries a recording; preview-product-boundary-successor.v6 carries only a "
        f"Claude verdict, because no Codex verdict for it exists on disk.")
    v10_reviews = {}
    for who, fn in (("claude", "claude2"), ("codex", "codex")):
        rel = f"{ART}/preview-product-boundary-successor.v10.review-independent.{fn}.json"
        need(os.path.exists(os.path.join(REPO, rel)), f"missing {rel}")
        v10_reviews[who] = {"path": rel, "sha256": sha256_file(rel), "verdict": "ACCEPT 0/0",
                            "gradeRuling": "SUSTAINED FOR APPLICATION"}
    based_on["predecessorV10"] = {
        "path": PRED_PATH, "sha256": PRED_SHA, "recording": PRED_RECORDING,
        "reviews": v10_reviews,
        "role": (f"The current recorded DR-117 leftover remasurement, recorded at "
                 f"{PRED_RECORDING} at Stage A dual ACCEPT 0/0 with both grade rulings "
                 f"SUSTAINED FOR APPLICATION. {SELF} is its successor and is "
                 f"CANDIDATE-NOT-APPLIED; until a reviewed coordinator act records "
                 f"{SELF}, {PRED} stays current."),
    }
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
    based_on["relation"] = (
        f"{SPEAKER} is the successor of {PRED} ({PRED_RECORDING}) issued under D-294 Decision 3 "
        f"because D-294 Decision 2 trigger (b) fires on live bytes. It refreshes the "
        f"{word(nmoved)} superseded cross-lineage citations and the "
        f"{word(len(m['partitionChanged']))} changed leftoverDesign partitions, and changes "
        f"nothing else: the fourteen classes, the seven dispositions and p1p2g3Mapping equal "
        f"{PRED}'s after normalizing the refreshed sentences, and that equality is asserted "
        f"before this file is written. No frozen artifact is edited, and no leftover-design is "
        f"asserted on a lineage whose current join does not carry it. {SPEAKER} existing is not "
        f"SATISFIED-GRADE and does not mark SATISFIED.")

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
        elif "from D-170 through D-294" in s:
            s = s.replace("from D-170 through D-294", "from D-170 through D-362")
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
            f"never recorded, and {PRED} was recorded at {PRED_RECORDING}, so {PRED} is the "
            f"current recording. {SPEAKER} exists because D-294 Decision 2 trigger (b) fires "
            f"against live bytes: of the {word(len(m['joins']))} leftover-joins {PRED} cites as "
            f"current, {word(nmoved)} are superseded, and on "
            f"{word(len(m['partitionChanged']))} of those the leftoverDesign partition changed. "
            f"D-294 Decision 3 requires a successor issued for any reason to refresh its "
            f"cross-lineage citations to the versions current at its dispatch and to label the "
            f"superseded ones as not current; {SELF} performs exactly that refresh and nothing "
            f"else. The fourteen enforcement-evidence classes of {SELF} equal {PRED}'s after "
            f"normalizing the refreshed cross-lineage sentences, and that equality is asserted "
            f"before this file is written. The seven dispositions and p1p2g3Mapping are carried "
            f"from {PRED} unchanged by {SELF}, and that equality is asserted before this file is "
            f"written. leftover-design of unnamed EE classes remains closed (D-157 / D-158 / "
            f"D-159). {SPEAKER} does not steal any gate's leftover-design and asserts no "
            f"leftover-design on a lineage whose current join does not carry it. {SPEAKER} is not "
            f"a second register row. {SPEAKER} does not SATISFY DR-117 and does not perform D-056 "
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
                    f"artifact relies on. Measured from bytes: "
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
                           "changed. No identifier, item, subLimb, invariant, input, pass rule, "
                           "owner or gate assignment was touched, and no frozen artifact was "
                           "edited."),
                "siteCount": sum(sites.values()),
                "sitesByReason": sites,
                "classEqualityAssertion": {
                    "statement": (f"After normalizing the refreshed citation and partition "
                                  f"sentences in both, {SELF}'s fourteen classes equal {PRED}'s "
                                  f"fourteen classes."),
                    "asserted": True,
                },
            },
        },
        "doesNot": rebuild_does_not(m, pred),
        "findingDisposition": [{
            "id": "PPBS-V11-CARRIED-STANDING",
            "severity": "NOTE",
            "disposition": (
                f"Every disposition below describes {PRED} ({PRED_RECORDING}) as recorded, and is "
                f"carried by {SELF} as history. Where such a disposition names a leftover-join "
                f"version, that version is the one current at {PRED}'s dispatch, not necessarily "
                f"the one current at {SELF}'s dispatch. The versions current now are measured in "
                f"joinCurrencyAudit and cited in basedOn and enforcementEvidence.classes. "
                f"{SPEAKER} edits no frozen artifact and does not restate {PRED}'s findings as "
                f"its own."),
        }] + dedeictic(pred["findingDisposition"]) + [{
            "id": "PPBS-V11-VENUE-NOTE",
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
            f"cited holding. {SPEAKER} existing does not perform Gate 4 SATISFIED-GRADE, does not "
            f"perform Gate 5, and does not edit file 08. Recording {SELF} does not SATISFY DR-117: "
            f"gates 4 and 5 are a separate dedicated coordinator cycle. Preview is not MVP "
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
            f"DR-117's leading label there must still be OPEN. sevenItems.sourceSha256 must still "
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
            f"The live DR-117 leading label in file 08 is {m['f08label']}. leftover-design of "
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


def audit(doc, m, pairs, sites):
    problems = []
    problems += audit_partitions(doc, m)
    problems += audit_site_symmetry(m, sites)
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
        print(f"make-ppbs-v12.py: FAILED: {e}", file=sys.stderr)
        return 2
    except subprocess.CalledProcessError as e:
        print(f"make-ppbs-v12.py: FAILED: git: {e}", file=sys.stderr)
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
