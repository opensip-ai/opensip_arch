#!/usr/bin/env python3
"""Mechanical enforcement of IMPLEMENTATION-FREEZE §3 <-> IMPLEMENTER-BLUEPRINT §1.1.

The freeze states, in prose, "These digests must equal blueprint §1.1."  Nothing
executed that sentence, so it degraded into an aspiration and both documents
drifted: D9 stayed at v1.13 after v1.14 passed, EVIDENCE stayed at a REJECTED v8
after v10 passed, and C-2 kept pointing implementers at `c2-plan-stage-schema.v3`
plus `check-c2.py` -- the exact bytes carrying LB-C2-01.  A reader following the
package would have built the defect deliberately, from the document written to
prevent it.

This checker makes that sentence executable.

WHAT IT DOES NOT DO -- deliberately.  It does not pin either document by hash.
Every other checker in this corpus pins its inputs because it guards AUTHORITY:
changing the bytes must invalidate the verdict.  This one guards AGREEMENT
between two documents and the files on disk.  Pinning would make each legitimate
edit a failure and would train the next author to regenerate the pin without
reading the diff -- converting a live guard into a rubber stamp.  So it reads
prose as data, asserts relationships, and holds no opinion about wording.

It executes nothing.  Every input is opened as inert bytes and parsed as text or
JSON, so the hash-before-execution trust order has no subject here; there is no
check/read gap to close because nothing is ever run.

Counts in the banner are MEASURED on the current run, never declared targets.

Exit codes
  0  no findings
  1  findings
  2  bad invocation
  3  --selftest refused on a dirty base, or the mutation suite did not run
"""

from __future__ import annotations

import hashlib
import json
import pathlib
import re
import sys

COOP = pathlib.Path(__file__).resolve().parent.parent
FREEZE = COOP / "IMPLEMENTATION-FREEZE.md"
BLUEPRINT = COOP / "IMPLEMENTER-BLUEPRINT.md"

HEX64 = re.compile(r"`([0-9a-f]{64})`")
MDLINK = re.compile(r"\]\((artifacts/[^)\s]+)\)")
TOKEN = re.compile(r"\]\((artifacts/[^)\s]+)\)|`([0-9a-f]{64})`")
VERSIONED = re.compile(r"^(?P<base>.+)\.v(?P<ver>\d+(?:\.\d+)*)$")

# A path is a binding artifact unless its stem marks it as a review-side
# document.  Reviews and adjudications are evidence ABOUT a surface, never the
# surface's own normative bytes, and must not be version-compared as heads.
REVIEW_MARKERS = ("review", "adjudication", "rereview", "litmus", "closure-coordinator")


class DuplicateKey(ValueError):
    """A JSON object carried the same key twice. Named, never silently kept."""


def _no_duplicates(pairs: list[tuple[str, object]]) -> dict:
    """`object_pairs_hook` that refuses duplicates and NAMES the key.

    `json.loads` without this keeps the LAST of duplicate keys, so a document
    can say one thing to a reader and another to every instrument, with the
    parsed object byte-identical to the honest one.  It has now been exploited
    twice in this corpus in unrelated lineages -- C-2 v6 (`IR-C2V6-01`, an
    18-byte insert to a full green banner) and versioning-policy v12 (three
    paper seals planted at exit 0, one of them in the sentence stating the
    closure).  A corpus sweep then measured 40 of 92 checkers exploitable, and
    found THIS checker among them at 1,810 unhooked decodes per run.

    Naming the key is not decoration: the sweep measured that 6 of 47 rejecting
    checkers never say which key was duplicated, so their operator learns a file
    is bad but not where.
    """
    seen: dict[str, object] = {}
    for key, value in pairs:
        if key in seen:
            raise DuplicateKey(f"duplicate key {key!r}")
        seen[key] = value
    return seen


def loads_strict(text: str) -> object:
    """The only JSON entry point in this file. One place to keep hooked."""
    return json.loads(text, object_pairs_hook=_no_duplicates)


def sha256_of(path: pathlib.Path) -> str | None:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError:
        return None


def is_review_side(rel: str) -> bool:
    stem = pathlib.PurePosixPath(rel).name.lower()
    return any(m in stem for m in REVIEW_MARKERS)


def split_version(rel: str) -> tuple[str, tuple[int, ...]] | None:
    """('artifacts/evidence.v10.json') -> ('evidence', (10,)).

    Returns None when the stem carries no numeric version, so review files such
    as `evidence.v10.review-independent-prefreeze.json` -- whose text after
    `.v` is not purely numeric -- are never mistaken for versioned heads.
    """
    name = pathlib.PurePosixPath(rel).name
    if not name.endswith(".json"):
        return None
    m = VERSIONED.match(name[: -len(".json")])
    if not m:
        return None
    return m.group("base"), tuple(int(p) for p in m.group("ver").split("."))


def table_rows(text: str, heading: str) -> list[str]:
    """Pipe-table rows following `heading`, stopping at the next heading."""
    lines = text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.strip().startswith(heading):
            start = i
            break
    if start is None:
        return []
    rows: list[str] = []
    for line in lines[start + 1 :]:
        s = line.strip()
        if s.startswith("#"):
            break
        if s.startswith("|") and s.endswith("|"):
            cells = [c.strip() for c in s.strip("|").split("|")]
            if len(cells) < 2:
                continue
            if set("".join(cells)) <= set("-: "):  # separator row
                continue
            if cells[0].lower() in ("surface", "candidate", "gap", "decision"):
                continue
            rows.append(s)
    return rows


def cell0(row: str) -> str:
    raw = row.strip("|").split("|")[0].strip()
    raw = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", raw)
    return raw.replace("*", "").replace("`", "").strip()


def bind_pairs(row: str) -> list[tuple[str, str | None]]:
    """Bind each binding-artifact path to the digest that follows it.

    Rows may carry several artifacts (RUST-PROVIDER-PROTOCOL names five, as
    `file<br>hash<br>file<br>hash`), so binding is positional: a digest belongs
    to the most recent binding artifact seen, and review-side links never
    capture one.
    """
    pairs: list[tuple[str, str | None]] = []
    pending: str | None = None
    for m in TOKEN.finditer(row):
        path, digest = m.group(1), m.group(2)
        if path is not None:
            if is_review_side(path) or not path.endswith(".json"):
                continue
            if pending is not None:
                pairs.append((pending, None))
            pending = path
        elif digest is not None and pending is not None:
            pairs.append((pending, digest))
            pending = None
    if pending is not None:
        pairs.append((pending, None))
    return pairs


def verdict_of(row: str) -> str:
    """Normalised verdict token, so `**PASSED**` and `PASSED` compare equal.

    The verdict is the EARLIEST token in the row, not the most severe.  Ledger
    rows routinely recite version history after stating the current verdict --
    "**PASSED**, 0 blocking ... `evidence.v8` and `evidence.v9` were both
    `REJECTED` and are history" -- so a severity-ordered scan reads the current
    verdict of a passing surface off its own changelog and reports a
    disagreement that does not exist.  Ties go to the longest match so that
    "PASSED with changes" is not shadowed by "PASSED".
    """
    up = row.upper()
    best: tuple[int, int, str] | None = None
    for token in ("PASSED WITH CHANGES", "REJECTED", "PASSED", "PARTIAL"):
        pos = up.find(token)
        if pos == -1:
            continue
        cand = (pos, -len(token), token)
        if best is None or cand < best:
            best = cand
    return best[2] if best else "UNSTATED"


def surface_map(text: str, heading: str) -> dict[str, dict]:
    out: dict[str, dict] = {}
    for row in table_rows(text, heading):
        name = cell0(row)
        if not name:
            continue
        pairs = bind_pairs(row)
        if not pairs:
            continue
        out[name] = {"pairs": pairs, "verdict": verdict_of(row), "row": row}
    return out


def analyse(
    freeze_text: str, blueprint_text: str, register_text: str | None = None
) -> tuple[list[dict], dict]:
    """`register_text` is injectable so the mutation suite can reach PC-6.

    A check the selftest cannot perturb is a check the selftest does not test.
    Reading the register from disk unconditionally would leave PC-6 outside the
    suite while still printing findings -- exactly the shape of "coverage claim
    over an unobservable region" that freeze §7 records as this corpus's
    dominant failure mode.
    """
    findings: list[dict] = []
    observations: list[str] = []
    counts = {
        "freezeRows": 0,
        "blueprintRows": 0,
        "pathsReferenced": 0,
        "pathsMissing": 0,
        "digestsBound": 0,
        "digestsVerified": 0,
        "surfacesCompared": 0,
        "headCandidatesExamined": 0,
        "registerBindingsChecked": 0,
    }

    def add(fid: str, statement: str, detail: str) -> None:
        findings.append({"id": fid, "statement": statement, "detail": detail})

    # PC-1 -- every artifacts/ link in either document resolves on disk.
    # Covers prose links too, not only tables: a dead link in a defect record is
    # as misleading as one in the ledger.
    seen_paths: set[str] = set()
    for label, text in (("FREEZE", freeze_text), ("BLUEPRINT", blueprint_text)):
        for m in MDLINK.finditer(text):
            rel = m.group(1)
            seen_paths.add(rel)
            if not (COOP / rel).exists():
                counts["pathsMissing"] += 1
                add("PC-1-DEAD-LINK", f"{label} links a file that does not exist", rel)
    counts["pathsReferenced"] = len(seen_paths)

    freeze = surface_map(freeze_text, "## 3.")
    blueprint = surface_map(blueprint_text, "### 1.1")
    counts["freezeRows"] = len(freeze)
    counts["blueprintRows"] = len(blueprint)

    # PC-2 -- every recorded digest equals the file's true SHA-256.
    for label, table in (("FREEZE", freeze), ("BLUEPRINT", blueprint)):
        for name, rec in table.items():
            for rel, digest in rec["pairs"]:
                if digest is None:
                    add(
                        "PC-2-NO-DIGEST",
                        f"{label} names a binding artifact with no recorded digest",
                        f"{name}: {rel}",
                    )
                    continue
                counts["digestsBound"] += 1
                actual = sha256_of(COOP / rel)
                if actual is None:
                    add("PC-2-UNREADABLE", f"{label} digest target unreadable", f"{name}: {rel}")
                elif actual != digest:
                    add(
                        "PC-2-DIGEST-DRIFT",
                        f"{label} records a digest that is not the file's SHA-256",
                        f"{name}: {rel} recorded {digest[:12]}... actual {actual[:12]}...",
                    )
                else:
                    counts["digestsVerified"] += 1

    # PC-3 / PC-4 -- the two documents must agree, ARTIFACT BY ARTIFACT.
    #
    # Comparison is keyed on the artifact path, not the row label.  The two
    # documents legitimately group differently: the freeze carries
    # RUST-PROVIDER-PROTOCOL's five files in one ledger row, the blueprint
    # spreads them across five §1.1 rows, and the freeze records unapplied
    # candidates in a separate table from its surface ledger.  Matching on row
    # labels reports all of that as disagreement when the documents in fact
    # agree perfectly about every file.  The claim under test is about DIGESTS,
    # so the key is the thing a digest belongs to.
    def path_index(table: dict[str, dict]) -> dict[str, tuple[str | None, str, str]]:
        idx: dict[str, tuple[str | None, str, str]] = {}
        for surface, rec in table.items():
            for rel, digest in rec["pairs"]:
                if rel not in idx or (idx[rel][0] is None and digest is not None):
                    idx[rel] = (digest, rec["verdict"], surface)
        return idx

    f_idx = path_index(freeze)
    b_idx = path_index(blueprint)

    for rel in sorted(set(f_idx) & set(b_idx)):
        counts["surfacesCompared"] += 1
        f_digest, f_verdict, f_surface = f_idx[rel]
        b_digest, b_verdict, b_surface = b_idx[rel]
        if f_digest != b_digest:
            add(
                "PC-3-DIGEST-DISAGREE",
                "freeze §3 and blueprint §1.1 record different digests for one artifact",
                f"{rel}: freeze={f_digest} blueprint={b_digest}",
            )
        # A verdict is a row-level property, and the documents attach it at
        # different granularity: the blueprint spreads a five-file set across
        # five rows and states the verdict on one of them.  Silence on one side
        # is therefore not disagreement -- only two STATED and different
        # verdicts are.  Reporting silence as a defect would train a reader to
        # paste a verdict token onto every row to quiet the checker, which is
        # how a guard becomes a rubber stamp.
        # PC-7 -- a pinned artifact whose OWN review REJECTS it.
        #
        # This is the defect that failed the gating litmus, and this checker
        # looked straight at it and cleared it.  `rust-provider-protocol.v2.json`
        # is pinned in blueprint §1.1's "normative byte set" and named by freeze
        # §3.2 as half the Rust wire contract; the review binding its exact
        # digest returns REJECT with `effect: "must not ... be used as
        # implementation authority"`; neither document mentions that review at
        # all; and freeze §2 rule 3 says a REJECTED version "is not normative and
        # must not be implemented".
        #
        # It printed as a benign observation because verdict comparison only ever
        # asked whether the two DOCUMENTS agree.  They did -- one said PASSED and
        # the other said nothing -- and agreement between two documents is not a
        # fact about the artifact.  The verdict a row records must also be true
        # of the bytes it pins, and that is a question only the review answers.
        state = review_state_of(COOP / rel)
        if state == "REJECT":
            add(
                "PC-7-PINNED-ARTIFACT-IS-REJECTED",
                "a pinned binding artifact's own independent review REJECTS those exact bytes",
                f"{rel}: review state REJECT, yet it is pinned as normative "
                f"(freeze says {f_verdict}, blueprint says {b_verdict}) — freeze §2 rule 3 "
                f"forbids implementing a REJECTED version",
            )

        if f_verdict != b_verdict:
            if "UNSTATED" in (f_verdict, b_verdict):
                stated, silent = (
                    (f_verdict, "blueprint §1.1") if b_verdict == "UNSTATED" else (b_verdict, "freeze §3")
                )
                observations.append(
                    f"{rel}: verdict {stated} stated on one side, unstated in {silent} "
                    f"-- row grouping differs, not a disagreement"
                )
            else:
                add(
                    "PC-4-VERDICT-DISAGREE",
                    "freeze §3 and blueprint §1.1 record different review verdicts",
                    f"{rel}: freeze={f_verdict} ({f_surface}) blueprint={b_verdict} ({b_surface})",
                )

    for rel in sorted(set(f_idx) - set(b_idx)):
        add(
            "PC-3-ARTIFACT-ONLY-IN-FREEZE",
            "freeze names a binding artifact the blueprint byte set does not",
            f"{rel} (freeze row: {f_idx[rel][2]})",
        )
    for rel in sorted(set(b_idx) - set(f_idx)):
        add(
            "PC-3-ARTIFACT-ONLY-IN-BLUEPRINT",
            "blueprint byte set names a binding artifact the freeze ledger does not",
            f"{rel} (blueprint row: {b_idx[rel][2]})",
        )

    # PC-5 -- staleness.  A named head is stale when a higher-numbered sibling
    # exists on disk AND carries a review recording no blocking findings.  A
    # higher sibling that is unreviewed or REJECTED is reported as an
    # observation only: evaluation-proof.v9 exists and is REJECTED, so EP's head
    # correctly remains v8 and must not be flagged as stale.
    named: dict[str, tuple[int, ...]] = {}
    for table in (freeze, blueprint):
        for rec in table.values():
            for rel, _ in rec["pairs"]:
                sv = split_version(rel)
                if sv is None:
                    continue
                base, ver = sv
                if base not in named or ver > named[base]:
                    named[base] = ver

    for base, named_ver in sorted(named.items()):
        for cand in sorted((COOP / "artifacts").glob(f"{base}.v*.json")):
            sv = split_version(f"artifacts/{cand.name}")
            if sv is None or sv[0] != base:
                continue
            cand_ver = sv[1]
            if cand_ver <= named_ver:
                continue
            counts["headCandidatesExamined"] += 1
            state = review_state_of(cand)
            where = f"{base}: documents name v{'.'.join(map(str, named_ver))}, disk has v{'.'.join(map(str, cand_ver))}"
            if state == "PASS":
                add("PC-5-STALE-HEAD", "a reviewed-passing successor exists but is not named", f"{where} ({cand.name} review records no blocking findings)")
            else:
                observations.append(f"{where} -- successor review state {state}; head correctly unchanged")

    # PC-6 -- the claim register is the THIRD authority, and it drifts hardest.
    #
    # freeze §3 requires "final reconciliation against every row above" before
    # signature, and check-completeness.py computes contract-shape, review and
    # seal-readiness numbers FROM the register.  So a stale binding citation
    # does not merely mis-name a file: it silently makes the seal-readiness
    # number describe superseded artifacts.  The register was found citing
    # `retention-tiers.v5` -- independently REJECTED -- while v22 was head, and
    # `evidence.v1` while v10 was head.  Nothing was watching, because the
    # freeze/blueprint pair checked each other and neither checked the register.
    register = COOP / "artifacts" / "claim-register.v1.json"
    raw_register = register_text
    if raw_register is None and register.exists():
        try:
            raw_register = register.read_text()
        except OSError:
            raw_register = None
    if raw_register is not None:
        try:
            reg = loads_strict(raw_register)
        except ValueError as exc:
            add("PC-6-REGISTER-UNPARSEABLE", "claim register is not valid JSON", str(exc))
            reg = None
        if isinstance(reg, dict):
            doc_heads = {rel for rel in set(f_idx) | set(b_idx)}
            doc_by_base: dict[str, tuple[tuple[int, ...], str]] = {}
            for rel in doc_heads:
                sv = split_version(rel)
                if sv is None:
                    continue
                base, ver = sv
                if base not in doc_by_base or ver > doc_by_base[base][0]:
                    doc_by_base[base] = (ver, rel)

            for claim in reg.get("claims") or []:
                if not isinstance(claim, dict):
                    continue
                cited = claim.get("bindingArtifact")
                if not isinstance(cited, str) or not cited.startswith("artifacts/"):
                    continue
                counts["registerBindingsChecked"] += 1
                if not (COOP / cited).exists():
                    add(
                        "PC-6-REGISTER-DEAD-BINDING",
                        "claim register cites a binding artifact that does not exist",
                        f"{claim.get('id')}: {cited}",
                    )
                    continue
                sv = split_version(cited)
                if sv is None:
                    continue
                base, ver = sv
                doc = doc_by_base.get(base)
                if doc is None:
                    observations.append(
                        f"{claim.get('id')}: register cites {cited}, which no ledger row names "
                        f"-- outside the freeze §3 / blueprint §1.1 surface set"
                    )
                    continue
                doc_ver, doc_rel = doc
                if ver < doc_ver:
                    add(
                        "PC-6-REGISTER-STALE-BINDING",
                        "claim register cites an older version than the documents name as head",
                        f"{claim.get('id')}: register={cited} documents={doc_rel}",
                    )
                elif ver > doc_ver:
                    add(
                        "PC-6-REGISTER-AHEAD-OF-LEDGER",
                        "claim register cites a version the documents do not name as head",
                        f"{claim.get('id')}: register={cited} documents={doc_rel}",
                    )

    return findings, {"counts": counts, "observations": observations}


def reviews_naming(artifact: pathlib.Path) -> list[tuple[pathlib.Path, dict]]:
    """Every review document that reviews `artifact`, found two ways.

    Review filenames are NOT derived from their subject.  `evidence.v10`'s
    review is `evidence.v10.review-independent-prefreeze.json`, but
    `evaluation-proof.v9`'s is `ep9.review-independent.json` -- a stem glob
    finds the first and misses the second entirely, which would silently report
    a reviewed artifact as unreviewed.  So the filename convention is used when
    it holds, and every other review document is opened and asked what it
    reviews.  Absence of a review must be established, not inferred from a
    naming habit.
    """
    out: list[tuple[pathlib.Path, dict]] = []
    target = artifact.name
    stem = target[: -len(".json")] if target.endswith(".json") else target
    for rev in sorted(artifact.parent.glob("*.json")):
        name = rev.name
        if not any(m in name.lower() for m in ("review", "adjudication")):
            continue
        if name == target:
            continue
        try:
            data = loads_strict(rev.read_text())
        except (OSError, ValueError):
            continue
        if not isinstance(data, dict):
            continue
        if name.startswith(stem + "."):
            out.append((rev, data))
            continue
        # Not named after its subject: ask the document itself.  Declarations
        # nest -- ep9's is {"subject": {"candidate": {"file": "...json"}}} -- so
        # collect strings recursively, but only from the subject-declaring keys.
        # Scanning the whole body would match any review that merely cites the
        # file in passing.
        strings: list[str] = []

        def harvest(node: object, depth: int = 0) -> None:
            if depth > 6:
                return
            if isinstance(node, str):
                strings.append(node)
            elif isinstance(node, dict):
                for x in node.values():
                    harvest(x, depth + 1)
            elif isinstance(node, list):
                for x in node:
                    harvest(x, depth + 1)

        # A PROSE subject declaration does not assign subjecthood.
        #
        # `claim-status-integrity.repair.review-b.json` declares its subject as
        # the sentence "Agent-3 turn-3 repairs to artifacts/check-claims.py,
        # claim-register.v1.json, and status restatements" -- a description of a
        # PASS over several files, not a verdict on any one of them.  Reading it
        # as a subject declaration made a `reject-require-v2` verdict attach to
        # the claim register, which would have excused the register from PC-7
        # and, worse, marked the corpus's own bookkeeping authority rejected.
        #
        # A STRUCTURED declaration assigns roles -- {"candidate": {...},
        # "checker": {...}} -- and means this file is the subject.  A bare string
        # naming several paths means this review describes a pass over them.
        # Filename convention is unaffected and still matches above.
        structured = False
        for key in ("artifact", "artifactUnderReview", "subject", "reviewed", "target"):
            if key not in data:
                continue
            if isinstance(data[key], (dict, list)):
                structured = True
            harvest(data[key])
        claimed = " ".join(strings)
        if structured and target in claimed:
            out.append((rev, data))
    return out


def review_state_of(artifact: pathlib.Path) -> str:
    """PASS / REJECT / NONE for the review(s) of one artifact, read as data.

    Reviews in this corpus carry `verdict` in two shapes: a bare string
    ("PASS"), and an object whose `decision` holds the verdict alongside
    `blockingFindingCount` and a SEPARATE `sealRecommendation`.

    `sealRecommendation` is deliberately NOT consulted.  Nothing in this corpus
    is sealed, so essentially every passing review also records
    `DO-NOT-SEAL` -- that is the correct standing for a reviewed candidate, not
    a rejection.  Reading it as one would mark every passing surface rejected.
    Freeze §6 law 17 keeps these axes distinct ("checker success, architecture
    seal, release qualification ... are distinct states") and this function
    respects that: it reports REVIEW outcome only.
    """
    states: list[str] = []
    for rev, data in reviews_naming(artifact):

        verdict = data.get("verdict")
        decision = ""
        blocking: int | None = None
        if isinstance(verdict, str):
            decision = verdict.upper()
        elif isinstance(verdict, dict):
            decision = str(verdict.get("decision") or "").upper()
            bc = verdict.get("blockingFindingCount")
            if isinstance(bc, int) and not isinstance(bc, bool):
                blocking = bc

            # SPLIT VERDICTS.  A review may adjudicate parts of one artifact
            # separately -- `retention-tiers.v24`'s review carries
            # {overall, partA: {decision, ...}, partB: {decision, ...}} because
            # its two halves were designed to be rejected independently.  There
            # is no top-level `decision`, so the simple read above returns "" and
            # the artifact scores UNCLEAR: safe, since UNCLEAR is not PASS and
            # cannot promote a head, but unable to tell "passed" from "cannot
            # tell", which is exactly the distinction PC-5 exists to make.
            #
            # Every part must pass for the whole to pass; one REJECT decides it.
            if not decision:
                parts = [v for v in verdict.values() if isinstance(v, dict) and "decision" in v]
                if parts:
                    part_decisions = [str(p.get("decision") or "").upper() for p in parts]
                    if any("REJECT" in d for d in part_decisions):
                        decision = "REJECT"
                    elif all("PASS" in d for d in part_decisions):
                        decision = "PASS"
                    counts = [
                        p.get("blockingFindingCount")
                        for p in parts
                        if isinstance(p.get("blockingFindingCount"), int)
                        and not isinstance(p.get("blockingFindingCount"), bool)
                    ]
                    if counts:
                        blocking = sum(counts)
                elif isinstance(verdict.get("overall"), str):
                    decision = verdict["overall"].upper()
        if not decision:
            decision = str(data.get("decision") or "").upper()
        if blocking is None:
            bc = data.get("blockingFindingCount")
            if isinstance(bc, int) and not isinstance(bc, bool):
                blocking = bc
        if blocking is None:
            blockers = data.get("blockers")
            if isinstance(blockers, list):
                blocking = len(blockers)

        # COUNTS BEFORE PROSE, and never a bare substring.
        #
        # `c2-plan-stage-schema.v9`'s verdict is a paragraph beginning "NO
        # BLOCKING FINDING. IR-C2V8-01 IS REPAIRED, and it is repaired..." with
        # `blockers: []`.  An earlier revision tested `"REJECT" in decision`
        # first, so any verdict whose PROSE mentions rejecting -- describing what
        # the checker rejects, or what a predecessor's verdict was -- scored
        # REJECT.  It produced a false PC-7 against an artifact that passed with
        # zero blockers, and it could equally have made PC-5 read a passing
        # successor as rejected and leave a stale head unflagged.
        #
        # A count is a measurement; a paragraph is not.  Where a review states a
        # blocking count -- explicitly or as a `blockers` list -- that decides.
        # Text is consulted only when no count exists, and then only as a LEADING
        # token, because a verdict states its outcome first and explains after.
        if blocking is not None:
            states.append("REJECT" if blocking > 0 else "PASS")
        else:
            head = decision.lstrip("* ").split(".")[0].split(",")[0].strip()
            if "REJECT" in head or "DO-NOT-SEAL-OR-APPLY" in head:
                states.append("REJECT")
            elif "PASS" in head or "NO BLOCKING" in head:
                states.append("PASS")
            else:
                states.append("UNCLEAR")

    if not states:
        return "NONE"
    if "REJECT" in states:
        return "REJECT"
    return "PASS" if all(s == "PASS" for s in states) else "UNCLEAR"


# --------------------------------------------------------------------------
# selftest
# --------------------------------------------------------------------------

MUTATIONS: list[tuple[str, str]] = [
    ("PC-2-DIGEST-DRIFT", "corrupt one recorded digest in the freeze ledger"),
    ("PC-2-DIGEST-DRIFT", "corrupt one recorded digest in the blueprint byte set"),
    ("PC-3-DIGEST-DISAGREE", "change a blueprint digest so the two documents disagree"),
    ("PC-1-DEAD-LINK", "repoint a freeze link at a file that does not exist"),
    ("PC-4-VERDICT-DISAGREE", "flip a blueprint verdict token"),
    ("PC-3-ARTIFACT-ONLY-IN-FREEZE", "delete a blueprint row that the freeze still carries"),
    ("PC-6-REGISTER-STALE-BINDING", "roll one register binding citation back a version"),
    ("PC-6-REGISTER-DEAD-BINDING", "repoint a register binding at a file that does not exist"),
    ("PC-6-REGISTER-UNPARSEABLE", "corrupt the register's JSON"),
]


def _first_row_with_digest(text: str, heading: str) -> str | None:
    for row in table_rows(text, heading):
        if HEX64.search(row) and bind_pairs(row):
            return row
    return None


def _register_claim_citing_a_head(
    register_text: str, freeze_text: str, blueprint_text: str
) -> tuple[dict, str, tuple[int, ...]] | None:
    """A register claim whose citation the documents also name, for mutation."""
    try:
        reg = loads_strict(register_text)
    except ValueError:
        return None
    f_idx = {r for rec in surface_map(freeze_text, "## 3.").values() for r, _ in rec["pairs"]}
    b_idx = {r for rec in surface_map(blueprint_text, "### 1.1").values() for r, _ in rec["pairs"]}
    known = f_idx | b_idx
    for claim in reg.get("claims") or []:
        if not isinstance(claim, dict):
            continue
        cited = claim.get("bindingArtifact")
        if not isinstance(cited, str) or cited not in known:
            continue
        sv = split_version(cited)
        if sv is None or sv[1][-1] <= 0:
            continue
        return claim, cited, sv[1]
    return None


def _repoint_binding(register_text: str, cited: str, replacement: str) -> str:
    """Repoint a `bindingArtifact` value, and only that.

    A bare string replace hits the first occurrence of the path anywhere in the
    register -- typically a `reviewArtifacts` entry -- leaving the binding
    intact, so the mutation silently perturbs nothing and the suite reports a
    check as untested when it was merely never reached.
    """
    pat = re.compile(r'("bindingArtifact"\s*:\s*)"' + re.escape(cited) + r'"')
    return pat.sub(lambda m: m.group(1) + '"' + replacement + '"', register_text, count=1)


def apply_mutation(
    idx: int, freeze_text: str, blueprint_text: str, register_text: str
) -> tuple[str, str, str] | None:
    f_row = _first_row_with_digest(freeze_text, "## 3.")
    b_row = _first_row_with_digest(blueprint_text, "### 1.1")
    if f_row is None or b_row is None:
        return None

    def flip(row: str) -> str:
        m = HEX64.search(row)
        d = m.group(1)
        return row.replace(d, ("0" if d[0] != "0" else "1") + d[1:], 1)

    if idx == 0:
        return freeze_text.replace(f_row, flip(f_row), 1), blueprint_text, register_text
    if idx == 1:
        return freeze_text, blueprint_text.replace(b_row, flip(b_row), 1), register_text
    if idx == 2:
        # Move a blueprint digest that the freeze also carries, so the two
        # documents disagree even though each is internally shaped correctly.
        fm = surface_map(freeze_text, "## 3.")
        bm = surface_map(blueprint_text, "### 1.1")
        for name in sorted(set(fm) & set(bm)):
            fp = {r: d for r, d in fm[name]["pairs"] if d}
            bp = {r: d for r, d in bm[name]["pairs"] if d}
            for rel in sorted(set(fp) & set(bp)):
                if fp[rel] == bp[rel]:
                    d = bp[rel]
                    swapped = ("0" if d[0] != "0" else "1") + d[1:]
                    return (
                        freeze_text,
                        blueprint_text.replace(
                            bm[name]["row"], bm[name]["row"].replace(d, swapped, 1), 1
                        ),
                        register_text,
                    )
        return None
    if idx == 3:
        m = MDLINK.search(f_row)
        if not m:
            return None
        return (
            freeze_text.replace(
                f_row, f_row.replace(m.group(1), "artifacts/does-not-exist.v999.json", 1), 1
            ),
            blueprint_text,
            register_text,
        )
    if idx == 4:
        for token, other in (("PASSED", "REJECTED"), ("REJECTED", "PASSED")):
            if token in b_row:
                return (
                    freeze_text,
                    blueprint_text.replace(b_row, b_row.replace(token, other, 1), 1),
                    register_text,
                )
        return None
    if idx == 5:
        bm = surface_map(blueprint_text, "### 1.1")
        fm = surface_map(freeze_text, "## 3.")
        for name in sorted(set(fm) & set(bm)):
            return freeze_text, blueprint_text.replace(bm[name]["row"] + "\n", "", 1), register_text
        return None
    if idx == 6:
        # Roll one register citation back a version.  This is the drift that
        # went unnoticed until the register was found citing a REJECTED
        # retention-tiers.v5 while v22 was head.
        found = _register_claim_citing_a_head(register_text, freeze_text, blueprint_text)
        if found is None:
            return None
        _, cited, ver = found
        older = list(ver)
        older[-1] -= 1
        rolled = cited.replace(
            ".v" + ".".join(map(str, ver)) + ".json",
            ".v" + ".".join(map(str, older)) + ".json",
            1,
        )
        if rolled == cited:
            return None
        return freeze_text, blueprint_text, _repoint_binding(register_text, cited, rolled)
    if idx == 7:
        found = _register_claim_citing_a_head(register_text, freeze_text, blueprint_text)
        if found is None:
            return None
        _, cited, _ = found
        return (
            freeze_text,
            blueprint_text,
            _repoint_binding(register_text, cited, "artifacts/does-not-exist.v999.json"),
        )
    if idx == 8:
        return freeze_text, blueprint_text, register_text + "  {trailing garbage"
    return None


def selftest(freeze_text: str, blueprint_text: str, register_text: str) -> int:
    base_findings, _ = analyse(freeze_text, blueprint_text, register_text)
    if base_findings:
        print("SELFTEST-REFUSED: base is dirty; the mutation suite proves nothing")
        print(f"  base findings: {len(base_findings)}")
        for f in base_findings[:12]:
            print(f"    {f['id']}: {f['detail']}")
        if len(base_findings) > 12:
            print(f"    ... and {len(base_findings) - 12} more")
        print("SELFTEST-NOT-RUN: 0 of "
              f"{len(MUTATIONS)} mutations executed")
        return 3

    executed = 0
    rejected = 0
    failures: list[str] = []
    for i, (expect_id, label) in enumerate(MUTATIONS):
        mutated = apply_mutation(i, freeze_text, blueprint_text, register_text)
        if mutated is None:
            failures.append(f"mutation {i} ({label}) could not be constructed")
            continue
        executed += 1
        found, _ = analyse(mutated[0], mutated[1], mutated[2])
        ids = {f["id"] for f in found}
        if expect_id in ids:
            rejected += 1
            print(f"  mutation {i} REJECTED by {expect_id} -- {label}")
        else:
            failures.append(f"mutation {i} ({label}) NOT caught; expected {expect_id}, got {sorted(ids) or 'nothing'}")

    print()
    print(f"SELFTEST: {executed} of {len(MUTATIONS)} mutations executed, {rejected} rejected")
    if failures or executed != len(MUTATIONS):
        for f in failures:
            print(f"  FAILURE: {f}")
        return 3
    return 0


def main(argv: list[str]) -> int:
    args = argv[1:]
    if args not in ([], ["--selftest"]):
        print(f"usage: {pathlib.Path(argv[0]).name} [--selftest]", file=sys.stderr)
        return 2

    for p in (FREEZE, BLUEPRINT):
        if not p.exists():
            print(f"INPUT-MISSING: {p}", file=sys.stderr)
            return 2

    freeze_text = FREEZE.read_text()
    blueprint_text = BLUEPRINT.read_text()
    register_path = COOP / "artifacts" / "claim-register.v1.json"
    register_text = register_path.read_text() if register_path.exists() else ""

    # Dispatched BEFORE any findings return.  The evidence.v8 defect was a
    # --selftest branch placed after an early return, so normal and selftest
    # output were byte-identical and the suite never ran.
    if args == ["--selftest"]:
        return selftest(freeze_text, blueprint_text, register_text)

    findings, extra = analyse(freeze_text, blueprint_text, register_text)
    counts = extra["counts"]

    print("PACKAGE COHERENCE -- freeze §3 <-> blueprint §1.1, and both <-> disk")
    print()
    print("  inputs read as data (this checker executes nothing):")
    for p in (FREEZE, BLUEPRINT):
        print(f"    {p.name:<28} {sha256_of(p)}")
    print()
    print("  measured this run:")
    for k in (
        "freezeRows",
        "blueprintRows",
        "surfacesCompared",
        "pathsReferenced",
        "pathsMissing",
        "digestsBound",
        "digestsVerified",
        "headCandidatesExamined",
        "registerBindingsChecked",
    ):
        print(f"    {k:<24} {counts[k]}")

    if extra["observations"]:
        print()
        print("  observations (not findings):")
        for o in extra["observations"]:
            print(f"    {o}")

    print()
    if not findings:
        print(f"OK: {counts['surfacesCompared']} surfaces agree across both documents; "
              f"{counts['digestsVerified']} recorded digests equal their file's SHA-256")
        print("  scope: document/disk coherence only. Says nothing about seal, freeze,")
        print("  review quality, or whether a named artifact is architecturally correct.")
        return 0

    print(f"FINDINGS: {len(findings)}")
    for f in findings:
        print(f"  {f['id']}: {f['statement']}")
        print(f"    {f['detail']}")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
