#!/usr/bin/env python3
"""Successor to check-product-dispositions.py. Edits nothing; replaces three lanes.

WHY A SUCCESSOR AND NOT AN EDIT
-------------------------------
Freeze section 7.2 forbids changing reviewed bytes in place; the sanctioned repair
is a new file. This file is that repair. `check-product-dispositions.py` is a
runtime input here, hash-verified before use, which section 7.3 explicitly
permits: "executing a verified closure is not building against it". Its semantic
vocabulary, its site extraction and its whole retention/RI/VER/G3 lane are reused
BYTE-IDENTICALLY rather than retyped, so this successor cannot silently drift from
the detection semantics that were reviewed.

WHAT CHANGES, AND WHY EACH IS A DERIVED PROPERTY
------------------------------------------------
The predecessor states the right doctrine at its lines 175-186:

    "An artifact that an independent review REJECTED, or that a later head has
     superseded, asserts nothing - it is a historical record ... Such assertions
     are reported as HISTORICAL OBSERVATIONS, never dropped, and never silently.
     Standing is DISCOVERED, not listed."

It then under-applies it in two places and hardcodes the pre-decision world in a
third. Nothing below names an artifact. Every predicate is computed from the
document's own bytes, its own filename, and the corpus's own version lineage.

(A) A REVIEW RECORD IS A HISTORICAL RECORD BY CONSTRUCTION.
    Section 7.2.1 requires a review's subject to be frozen at dispatch, and a
    review to record the digest it actually reviewed. A review, adjudication or
    rereview is therefore a measurement taken at a moment. It cannot be repaired:
    editing it destroys the evidence it exists to carry, and section 7.2 forbids
    the edit anyway. So a product-decision assertion inside a review record is an
    OBSERVATION about that moment, never a live finding.

    The predecessor already computes `_is_review_side()` and uses it to decide
    what may REVIEW something. It never asks what a review's own standing is.

(B) A SUPERSEDED PREDECESSOR IS A HISTORICAL RECORD - AND THE PREDECESSOR'S
    SUPERSESSION LIMB SILENTLY NEVER FIRES.
    Root cause, measured, two layers deep:

      1. ENVIRONMENT. `head_named_artifacts()` reads IMPLEMENTATION-FREEZE.md and
         IMPLEMENTER-BLUEPRINT.md from `HERE.parent` - a location OUTSIDE the
         directory the instrument otherwise scans. The supersession limb then
         tests `other not in heads`. If those two markdown files are not present
         at that exact relative path, `heads` is empty, the test is true for every
         candidate successor, and supersession NEVER fires for ANY artifact.
         Measured on the amendment-applied tree: head docs present -> 22
         observations / 25 findings; head docs absent -> 15 observations / 32
         findings. That is the same class as the third row of section 7.2's own
         table (an undeclared `rg` dependency that changed a verdict).

      2. PROSE. Even when both documents ARE readable, a successor only counts if
         a markdown document happens to mention its filename. That makes a
         structural fact about the corpus depend on narrative nobody maintains -
         section 7.7's exact hazard. This file does not assert that the gap is
         non-empty; `--selftest` COUNTS the artifacts that exist on disk as a
         strictly later version of some base and are named in NEITHER head
         document, and fails if that count is zero (which would mean this
         paragraph had gone stale). No artifact is named to make the point.

    The repair drops both dependencies. Supersession is derived from the artifact
    set itself, with one gate the predecessor lacks entirely and that turns out to
    be load-bearing: A REJECTED SUCCESSOR SUPERSEDES NOTHING. A version that was
    independently rejected is itself a historical record and cannot be the repair
    of anything. That single gate is what keeps a lineage whose every later
    version was rejected correctly LIVE and correctly failing.

(C) THE DECISION-SET LANE HARDCODES THE PRE-DECISION WORLD.
    `PD-1` requires `set(decisions) == EXPECTED_CHOICES` and `PD-5` requires
    "CD-RT-5 must be the sole pending Phase-2 decision" and "CD-RT-5 is not
    visibly blocked on Phase 1A". Applying ANY decision necessarily trips all
    three. A guard that cannot survive the event it is guarding is not a guard.
    This successor accepts EITHER state and enforces the requirements of each.

WHAT DOES NOT CHANGE
--------------------
Fail-closed remains the priority. Unknown standing is LIVE. A demotion is never a
drop: every demoted assertion is printed under HISTORICAL OBSERVATIONS with the
derivation that removed its standing. A prose-only artifact with no review and no
successor stays LIVE and fails. The current head of a lineage asserting a stale
state stays LIVE and fails - that is the corpus working, not a defect.

WHAT THIS INSTRUMENT CANNOT DO - stated before the evidence, not after.
Section 7.8's measured bound applies in full: this binds structure and type, not
the truth of content. The residual the predecessor names ("a forged review would
launder a false claim into an observation") is not closed here. It is narrowed,
measured, and the surviving width is printed by `--selftest` as a number rather
than described. See RESIDUAL-1 through RESIDUAL-4 at the foot of this file; each
is exercised by a case in the evasion corpus that is EXPECTED TO ESCAPE, so the
count is produced by execution rather than by assertion.
"""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import re
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent

# ---------------------------------------------------------------------------
# The predecessor is a RUNTIME INPUT, hash-verified before execution (7.3).
# A drift here is EXIT_REFUSED, never a silent fallback: this successor's whole
# claim to reuse reviewed detection semantics rests on these exact bytes.
# ---------------------------------------------------------------------------
PREDECESSOR_BINDING = {
    "path": "check-product-dispositions.py",
    "sha256": "c64d31b4489afc37193f6f37a7de89e39688d4efdb47d7c7d2a0c4c6cc9f79b4",
}

EXIT_OK = 0
EXIT_FINDINGS = 1
EXIT_USAGE = 2
EXIT_REFUSED = 3
DECLARED_FLAGS = ("--selftest",)


def _load_predecessor():
    """Hash-verify then execute the predecessor as a library. Never falls back."""
    path = HERE / PREDECESSOR_BINDING["path"]
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise RuntimeError(
            f"cannot read pinned predecessor {PREDECESSOR_BINDING['path']} "
            f"({type(exc).__name__})"
        ) from exc
    digest = hashlib.sha256(raw).hexdigest()
    if digest != PREDECESSOR_BINDING["sha256"]:
        raise RuntimeError(
            f"pinned predecessor {PREDECESSOR_BINDING['path']} hashes {digest}, "
            f"expected {PREDECESSOR_BINDING['sha256']}"
        )
    spec = importlib.util.spec_from_file_location("_pd_v1", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot build an import spec for the pinned predecessor")
    module = importlib.util.module_from_spec(spec)
    # NO BYTECODE, EVER. Sibling instruments in this directory snapshot
    # `__pycache__/*.pyc` and compare the snapshot across a run or against a
    # pinned digest. Executing the predecessor as a library would drop a .pyc
    # into a directory those instruments measure - a new instrument silently
    # perturbing another instrument's evidence. Measured: without this guard a
    # single run of this file adds one .pyc. The flag is restored either way.
    previous = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    try:
        spec.loader.exec_module(module)
    finally:
        sys.dont_write_bytecode = previous
    return module


# ---------------------------------------------------------------------------
# (A) Review-record derivation.
#
# DOCUMENT CLASS, NOT DOCUMENT NAME. Every list below is a vocabulary of what a
# review CALLS ITSELF and what a review STRUCTURALLY IS. None of them names an
# artifact, and a document is classified from its own bytes plus its own filename.
#
# The conjunction is deliberate. Each conjunct alone is trivially forged; the
# selftest measures exactly how much each one narrows the class, so the claim
# "this conjunction is load-bearing" is a number this file computes, not a boast.
# ---------------------------------------------------------------------------

# What a review-class document calls itself, in a filename or in its own
# declared identity. "response" is deliberately ABSENT: an author response to a
# review is authored by the party under review and is not an independent record.
REVIEW_CLASS_TOKENS = (
    "review", "rereview", "re-review", "adjudication", "adjudicat",
    "litmus", "closure-coordinator",
)
# Where a document declares what it IS. Deliberately narrow, and the narrowing
# was forced by measurement rather than chosen: `role`, `purpose` and `status`
# were tried and REMOVED. They carry free prose, and a live candidate whose
# `role` reads "a successor to X, whose independent review returned a SPLIT
# verdict" was demoted to a historical record by the word "review" inside its own
# description of WHY IT EXISTS. That is over-demotion of a current head - the
# exact failure this successor must not commit. Only fields whose VALUE is an
# identity or a document class survive here.
IDENTITY_FIELDS = ("artifact", "documentClass", "reviewType")
# An independent observer identifies itself and its distance from the subject.
# Stems, not exact keys: `reviewerIndependenceAndLineage` and `reviewBinding`
# are both real live spellings of the same concept.
REVIEWER_ROLE_STEMS = (
    "reviewer", "adjudicat", "rereview", "reviewbinding", "reviewbasis",
    "reviewdate", "reviewtype", "reviewscope", "reviewonly", "reviewedby",
    "reviewedcandidate", "independence", "artifactunderreview",
    "whatididnotcheck", "hashwindow", "reviewwindow",
)
# An adjudication reaches a verdict. A proposal does not.
VERDICT_STEMS = (
    "verdict", "decision", "blocker", "blockingfinding", "finding",
    "escapesfound", "disposition", "outcome",
)
ISO_DATE_RE = re.compile(r"\b20\d\d-\d\d-\d\d\b")

VERSIONED_RE = re.compile(r"^(?P<base>.+)\.v(?P<ver>\d+(?:\.\d+)*)$")

# Keys that carry only a document's own identity. A successor consisting of
# nothing but these carries no content with which to supersede anything.
IDENTITY_ONLY_KEYS = {
    "artifact", "version", "schemaversion", "date", "id", "name", "title",
}

# (C) Placeholder vocabulary for an authority field. A bracketed template, or a
# value whose text says it has not been filled in, is not an authority.
UNFILLED_STEMS = (
    "unset", "tbd", "to be determined", "to be filled", "fill in", "fillin",
    "placeholder", "pending", "unknown", "n a", "none", "xxx", "todo",
    "not yet", "awaiting", "blank", "empty",
)
BRACKETED_RE = re.compile(r"^\s*[\[<(].*[\]>)]\s*$", re.DOTALL)

DECIDED_STATUSES = {"DECIDED", "CONFIRMED"}
RETENTION_DECISION_ID = "CD-RT-5"


def _norm_key(text: object) -> str:
    return "".join(ch for ch in str(text).lower() if ch.isalnum())


def _norm_text(text: object) -> str:
    lowered = str(text).lower()
    flattened = "".join(ch if ch.isalnum() else " " for ch in lowered)
    return " " + " ".join(flattened.split()) + " "


def _keys_within(node: object, max_depth: int, depth: int = 0,
                 out: set[str] | None = None, budget: list[int] | None = None) -> set[str]:
    """Normalised key names at or above `max_depth`. Bounded so a hostile
    document cannot make classification expensive."""
    if out is None:
        out = set()
    if budget is None:
        budget = [20000]
    if depth > max_depth or budget[0] <= 0:
        return out
    if isinstance(node, dict):
        for key, value in node.items():
            budget[0] -= 1
            if budget[0] <= 0:
                return out
            out.add(_norm_key(key))
            _keys_within(value, max_depth, depth + 1, out, budget)
    elif isinstance(node, list):
        for value in node:
            _keys_within(value, max_depth, depth + 1, out, budget)
    return out


def declares_review_class(name: str, doc: object) -> str:
    """Does this document declare itself review-class? Filename OR own identity.

    Two independent routes on purpose. A review whose filename does not follow
    the convention is still caught by its declared identity; a document merely
    RENAMED to look like a review still has to satisfy the other conjuncts.
    """
    low = name.lower()
    for token in REVIEW_CLASS_TOKENS:
        if token in low:
            return f"filename~{token!r}"
    if isinstance(doc, dict):
        for field in IDENTITY_FIELDS:
            value = doc.get(field)
            if not isinstance(value, str):
                continue
            normalised = _norm_key(value)
            for token in REVIEW_CLASS_TOKENS:
                if token.replace("-", "") in normalised:
                    return f"{field}~{token!r}"
    return ""


def has_reviewer_role(doc: object) -> str:
    if not isinstance(doc, dict):
        return ""
    for key in _keys_within(doc, 2):
        for stem in REVIEWER_ROLE_STEMS:
            if stem in key:
                return f"key~{key!r}"
    return ""


def has_verdict_shape(doc: object) -> str:
    if not isinstance(doc, dict):
        return ""
    for key in _keys_within(doc, 1):
        for stem in VERDICT_STEMS:
            if stem in key:
                return f"key~{key!r}"
    return ""


def _document_text(doc: object, limit: int = 4_000_000) -> str:
    try:
        text = json.dumps(doc, ensure_ascii=False)
    except (TypeError, ValueError):
        return ""
    return text[:limit]


def names_other_corpus_files(name: str, doc: object, corpus: set[str],
                             file_re: re.Pattern) -> int:
    text = _document_text(doc)
    return len({f for f in file_re.findall(text) if f != name and f in corpus})


def dispatch_date(doc: object) -> str:
    """The moment a review record froze, as an ISO date. '' if it declares none.

    A review that records no date recorded no moment; section 7.2.1 requires the
    moment, so its absence is a reason to WITHHOLD the demotion, never to grant
    it.
    """
    if not isinstance(doc, dict):
        return ""
    for field in ("date", "reviewDate", "dispatchDate", "reviewedOn",
                  "completedOn", "finalisedOn", "finalizedOn"):
        value = doc.get(field)
        if isinstance(value, str):
            match = ISO_DATE_RE.search(value)
            if match:
                return match.group(0)
    return ""


def review_record_reason(name: str, doc: object, corpus: set[str],
                         file_re: re.Pattern) -> str:
    """Non-empty iff this document is a frozen review record by construction.

    FIVE conjuncts, each independently measurable:
      1. it declares itself review-class (filename or own identity);
      2. it identifies an independent-observer role;
      3. it reaches a verdict rather than proposing one;
      4. it names at least one OTHER file that exists in this corpus - a review
         with no subject reviewed nothing;
      5. it records the moment it froze, as an ISO date (section 7.2.1).
    """
    declaration = declares_review_class(name, doc)
    if not declaration:
        return ""
    role = has_reviewer_role(doc)
    if not role:
        return ""
    verdict = has_verdict_shape(doc)
    if not verdict:
        return ""
    subjects = names_other_corpus_files(name, doc, corpus, file_re)
    if subjects < 1:
        return ""
    when = dispatch_date(doc)
    if not when:
        return ""
    return (f"frozen review record (declared {declaration}; role {role}; "
            f"verdict {verdict}; {subjects} corpus subject(s); dispatched {when})")


# ---------------------------------------------------------------------------
# (B) Supersession derivation. No head document is consulted, by design: the
# predecessor's dependency on two markdown files OUTSIDE the scanned directory
# is the measured root cause of the limb never firing.
# ---------------------------------------------------------------------------

def split_version(name: str) -> tuple[str, tuple[int, ...]] | None:
    if not name.endswith(".json"):
        return None
    match = VERSIONED_RE.match(name[: -len(".json")])
    if not match:
        return None
    try:
        return match.group("base"), tuple(int(p) for p in match.group("ver").split("."))
    except ValueError:
        return None


def carries_content(doc: object) -> bool:
    """A successor must carry something beyond its own identity block."""
    if not isinstance(doc, dict) or not doc:
        return False
    return any(_norm_key(k) not in IDENTITY_ONLY_KEYS for k in doc)


def supersession_reason(name: str, doc: object, docs: list[tuple[str, object]],
                        rejected: dict[str, str], records: dict[str, str]) -> str:
    """Non-empty iff a later version of the same base, WITH STANDING, exists.

    Four gates, and the third is the one the predecessor lacks entirely:
      1. same filename base, strictly greater version tuple;
      2. the successor is not itself a review record (a review of v8 is not v9);
      3. THE SUCCESSOR IS NOT ITSELF INDEPENDENTLY REJECTED. A rejected version
         is a historical record; it repairs nothing and displaces nothing. This
         is what keeps a lineage whose every later version was rejected LIVE;
      4. the successor carries content beyond its own identity block.

    A review record is never treated as superseded by version arithmetic - it is
    already historical under (A), and its filename version, where it has one,
    belongs to its SUBJECT rather than to itself.
    """
    if name in records:
        return ""
    version = split_version(name)
    if version is None:
        return ""
    base, current = version
    best: tuple[tuple[int, ...], str] | None = None
    for other, other_doc in docs:
        if other == name or other in records:
            continue
        other_version = split_version(other)
        if other_version is None or other_version[0] != base:
            continue
        if not (other_version[1] > current):
            continue
        if other in rejected:
            continue
        if not carries_content(other_doc):
            continue
        if best is None or other_version[1] > best[0]:
            best = (other_version[1], other)
    if best is None:
        return ""
    return (f"superseded by {best[1]}, a later version of the same base that "
            f"exists on disk, carries content, and is not itself rejected")


# ---------------------------------------------------------------------------
# Standing, combined.
# ---------------------------------------------------------------------------

def rejecting_reviews(docs: list[tuple[str, object]], v1) -> dict[str, str]:
    """{artifact: why} for every artifact an independent review REJECTED.

    Delegates verdict reading and subject attribution to the pinned predecessor
    UNCHANGED, so this successor cannot quietly loosen either.
    """
    out: dict[str, str] = {}
    for name, _ in docs:
        for review_name, data, how in v1.primary_reviews_of(name, docs):
            outcome, why = v1.review_outcome(data)
            if outcome == "REJECT":
                out[name] = (f"independently REJECTED by {review_name} "
                             f"({why}; matched by {how})")
                break
    return out


def review_records(docs: list[tuple[str, object]], v1) -> dict[str, str]:
    corpus = {name for name, _ in docs}
    return {
        name: reason
        for name, doc in docs
        if (reason := review_record_reason(name, doc, corpus, v1.FILE_REFERENCE_RE))
    }


def standing_of(name: str, doc: object, docs: list[tuple[str, object]],
                rejected: dict[str, str], records: dict[str, str],
                decision_dates: dict[str, str]) -> tuple[str, str]:
    """LIVE / REJECTED / REVIEW-RECORD / SUPERSEDED, plus the derivation.

    Order is by strength of evidence, and every non-LIVE branch prints why.
    Unknown standing is LIVE: the fail-closed direction is more findings.
    """
    if name in rejected:
        return "REJECTED", rejected[name]
    if name in records:
        # A review dated ON OR AFTER the decision it contradicts is NOT excused:
        # it could have read the decided packet. The cut-off is the EARLIEST
        # recorded decision date, not the latest - min() is the fail-closed
        # choice, because adding a new, later decision then EXCUSES nothing that
        # was not already excused, while max() would quietly excuse more reviews
        # every time the packet advanced. The gate is inapplicable when the
        # packet records no usable decision date at all, and says so rather than
        # silently defaulting either way.
        cutoff = min(decision_dates.values()) if decision_dates else ""
        when = dispatch_date(doc)
        if cutoff and when and when >= cutoff:
            return "LIVE", (
                f"review record dispatched {when}, on or after the earliest "
                f"packet decision date {cutoff} - it could have read the decided "
                "packet, so its assertion is not excused as historical"
            )
        return "REVIEW-RECORD", records[name] + (
            f"; earliest packet decision date {cutoff}, strictly later than dispatch"
            if cutoff else "; packet records no usable decision date"
        )
    reason = supersession_reason(name, doc, docs, rejected, records)
    if reason:
        return "SUPERSEDED", reason
    return "LIVE", "no rejecting review, not a frozen review record, no successor with standing"


# ---------------------------------------------------------------------------
# Assertion lane, rebuilt on the predecessor's UNCHANGED site extraction.
# ---------------------------------------------------------------------------

def packet_decision_dates(product: object) -> dict[str, str]:
    """{decision id: ISO decidedOn} for rows that record a usable one."""
    dates: dict[str, str] = {}
    if not isinstance(product, dict):
        return dates
    rows = product.get("decisions")
    if not isinstance(rows, dict):
        return dates
    for decision_id, row in rows.items():
        if not isinstance(row, dict):
            continue
        value = row.get("decidedOn")
        if isinstance(value, str) and not is_unfilled(value):
            match = ISO_DATE_RE.search(value)
            if match:
                dates[str(decision_id)] = match.group(0)
    return dates


def classify(product: object, docs: list[tuple[str, object]], unreadable: list[str],
             discovered: int, v1) -> tuple[list[str], list[str], dict[str, object]]:
    """The assertion lane. Detection is the predecessor's; standing is this file's."""
    states = v1.packet_decision_states(product)
    decision_dates = packet_decision_dates(product)
    report: dict[str, object] = {
        "artifactsDiscovered": discovered,
        "artifactsParsed": len(docs),
        "artifactsUnreadable": unreadable,
        "packetDecisionIds": len(states),
        "packetDecisionDates": decision_dates,
        "registerRead": False,
        "keyAnchoredSites": 0,
        "keyScopedStrings": 0,
        "proseSites": 0,
        "sitesAgainstPacketRow": 0,
        "sitesAgainstUnbackedRule": 0,
        "clausesClassified": 0,
        "conflicts": 0,
        "artifactsLive": 0,
        "artifactsRejected": 0,
        "artifactsReviewRecord": 0,
        "artifactsSuperseded": 0,
        "conflictingArtifactsLive": 0,
        "conflictingArtifactsHistorical": 0,
        "historicalObservations": 0,
        "demotedByStanding": {"REJECTED": 0, "REVIEW-RECORD": 0, "SUPERSEDED": 0},
    }
    failures: list[str] = []
    observations: list[str] = []
    if not states:
        return ([
            "PD2-REG: cannot read the binding packet's decision rows; "
            "no artifact assertion can be cross-checked"
        ], observations, report)

    rejected = rejecting_reviews(docs, v1)
    records = review_records(docs, v1)
    register_name = v1.REGISTER_PATH.name

    for name, doc in docs:
        is_register = name == register_name
        if is_register:
            report["registerRead"] = True
        found, counts = v1.document_assertion_failures(
            states, name, doc, "PD2-REG" if is_register else "PD2-SCAN"
        )
        for key, value in counts.items():
            if key in report and key != "conflicts":
                report[key] = int(report[key]) + value  # type: ignore[arg-type]
        standing, reason = standing_of(name, doc, docs, rejected, records, decision_dates)
        bucket = {
            "LIVE": "artifactsLive", "REJECTED": "artifactsRejected",
            "REVIEW-RECORD": "artifactsReviewRecord", "SUPERSEDED": "artifactsSuperseded",
        }[standing]
        report[bucket] = int(report[bucket]) + 1  # type: ignore[arg-type]
        if not found:
            continue
        if standing == "LIVE":
            report["conflictingArtifactsLive"] = int(report["conflictingArtifactsLive"]) + 1  # type: ignore[arg-type]
            failures.extend(found)
        else:
            report["conflictingArtifactsHistorical"] = int(report["conflictingArtifactsHistorical"]) + 1  # type: ignore[arg-type]
            report["historicalObservations"] = int(report["historicalObservations"]) + len(found)  # type: ignore[arg-type]
            report["demotedByStanding"][standing] += len(found)  # type: ignore[index]
            observations.append(f"{name} - {standing}: {reason}")
            observations.extend(f"    {item}" for item in found)

    if not report["registerRead"]:
        failures.append(
            f"PD2-REG: {register_name} was not readable, so the artifact the "
            "fabricated CD-RT-5 sign-off survived in went un-cross-checked"
        )
    report["conflicts"] = len(failures)
    return failures, observations, report


# ---------------------------------------------------------------------------
# (C) The decision-set lane, accepting either state of the retention decision.
# ---------------------------------------------------------------------------

def is_unfilled(value: object) -> bool:
    """Is this authority field a placeholder rather than an authority?

    RULING, AND THE JUSTIFICATION, BECAUSE THIS ONE IS A JUDGEMENT CALL.
    `[UNSET - the authority's date]` and `[UNSET - the authority's name]` FAIL.

      1. The defect this whole instrument exists for was a FABRICATED sign-off
         that at least named an authority and a date. A row whose authority is a
         template is strictly weaker evidence than the fabrication it must catch.
         Admitting it would mean the guard accepts less than what it rejects.
      2. Section 7.2.2's rider: "a measurement that cannot fail the build is
         prose." `decidedBy: "[UNSET]"` is prose sitting in the field the packet's
         entire authority rests on.
      3. The predecessor already rules this way for every OTHER site: its
         `asserts_completed_product_closure` classifies a bracketed template as
         "citation-or-template" and refuses to read it as an assertion. Reading a
         template as a decision only in the packet would be the inconsistency.
      4. The amendment draft itself agrees, in its own bytes: it declares
         `constitutesADecision: false` and `status: "DRAFT - NOT APPLIED"`, and
         cites freeze 4.5 that only the product authority constitutes a decision.
         Applying the draft verbatim applies a draft, not a decision.

    So the decided state is reachable, and reaching it requires the authority to
    actually fill in its own name and date. That is the whole point.
    """
    if value is None:
        return True
    if not isinstance(value, str):
        return False
    stripped = value.strip()
    if not stripped:
        return True
    if BRACKETED_RE.match(stripped):
        return True
    normalised = _norm_text(stripped)
    return any(f" {stem} " in normalised for stem in UNFILLED_STEMS)


def _non_empty_leaf(value: object) -> bool:
    if isinstance(value, str):
        return bool(value.strip()) and not is_unfilled(value)
    if isinstance(value, dict):
        return any(_non_empty_leaf(v) for v in value.values())
    if isinstance(value, list):
        return any(_non_empty_leaf(v) for v in value)
    return value is not None


def _forbids_implementer_invention(text: str) -> bool:
    """Semantic gate (7.2.2): a continuing invariant, not a recorded measurement.

    The pending rule reads "No implementer may choose a retention default ...";
    the drafted post-decision rule reads "No implementer may still choose a
    retention DEFAULT." A byte pin on either spelling fails on the very advance
    the invariant anticipates, so this asks for the meaning: a prohibition, on
    implementers, over choosing a retention default.
    """
    norm = _norm_text(text)
    prohibits = " no implementer " in norm or " implementer may not " in norm
    chooses = any(f" {stem} " in norm for stem in ("choose", "chooses", "choosing",
                                                   "select", "selects", "invent",
                                                   "invents", "pick", "picks"))
    subject = " default " in norm or " defaults " in norm
    return prohibits and chooses and subject


def decision_set_failures(product: object, expected_choices: dict[str, str]) -> list[str]:
    """PD2-1/PD2-5. Accepts pending-and-blocked OR decided-with-required-fields.

    Every requirement below can fail the build; none is narrated into a report.
    """
    failures: list[str] = []
    if not isinstance(product, dict) or not product:
        return ["PD2-1: product root must be a non-empty object"]
    decisions = product.get("decisions")
    pending = product.get("pendingDecisions")
    if not isinstance(decisions, dict):
        return ["PD2-1: decisions must be an object"]
    if pending is None:
        pending = {}
    if not isinstance(pending, dict):
        return ["PD2-1: pendingDecisions must be an object when present"]

    # The seven non-retention choices are unchanged and still hard-compared.
    non_retention = {k: v for k, v in decisions.items() if k != RETENTION_DECISION_ID}
    if set(non_retention) != set(expected_choices):
        failures.append(
            "PD2-1: non-retention decision set differs from the required "
            f"Phase-2 set (extra {sorted(set(non_retention) - set(expected_choices))}, "
            f"missing {sorted(set(expected_choices) - set(non_retention))})"
        )
    for decision_id, expected in expected_choices.items():
        row = decisions.get(decision_id) or {}
        if not isinstance(row, dict):
            failures.append(f"PD2-1 {decision_id}: decision row must be an object")
            continue
        if row.get("status") not in DECIDED_STATUSES:
            failures.append(f"PD2-1 {decision_id}: status is not DECIDED/CONFIRMED")
        if row.get("choice") != expected:
            failures.append(
                f"PD2-1 {decision_id}: choice {row.get('choice')!r} != {expected!r}")

    # The retention decision is in exactly one state. Never both, never neither.
    in_decided = RETENTION_DECISION_ID in decisions
    in_pending = RETENTION_DECISION_ID in pending
    if in_decided and in_pending:
        failures.append(
            f"PD2-5: {RETENTION_DECISION_ID} appears in BOTH decisions and "
            "pendingDecisions; the packet records two contradictory states")
        return failures
    if not in_decided and not in_pending:
        failures.append(
            f"PD2-5: {RETENTION_DECISION_ID} appears in neither decisions nor "
            "pendingDecisions; the retention decision has vanished from the "
            "authority that owns it")
        return failures

    # Whichever state holds, no OTHER decision may quietly become pending.
    stray = sorted(set(pending) - {RETENTION_DECISION_ID})
    if stray:
        failures.append(
            f"PD2-5: unexpected pending Phase-2 decision(s) {stray}; only "
            f"{RETENTION_DECISION_ID} may be pending")

    if in_pending:
        failures.extend(_pending_state_failures(pending[RETENTION_DECISION_ID]))
    else:
        failures.extend(_decided_state_failures(decisions[RETENTION_DECISION_ID]))
    return failures


def _pending_state_failures(row: object) -> list[str]:
    """STATE P - the pre-decision world. The predecessor's requirements, kept."""
    failures: list[str] = []
    if not isinstance(row, dict):
        return [f"PD2-5: pending {RETENTION_DECISION_ID} row must be an object"]
    if row.get("status") != "BLOCKED_ON_PHASE_1A":
        failures.append(
            f"PD2-5: {RETENTION_DECISION_ID} is pending but not visibly blocked "
            f"on Phase 1A (status {row.get('status')!r})")
    if not _forbids_implementer_invention(str(row.get("ruleWhilePending", ""))):
        failures.append(
            "PD2-5: pending retention permits implementer invention - the rule "
            "while pending must forbid an implementer choosing a retention default")
    return failures


def _decided_state_failures(row: object) -> list[str]:
    """STATE D - the decision has been taken. What must be true for that to hold."""
    failures: list[str] = []
    if not isinstance(row, dict):
        return [f"PD2-5: decided {RETENTION_DECISION_ID} row must be an object"]
    status = row.get("status")
    if status not in DECIDED_STATUSES:
        failures.append(
            f"PD2-5: {RETENTION_DECISION_ID} sits in decisions with status "
            f"{status!r}, which is not DECIDED/CONFIRMED")
    for field, what in (("decidedOn", "the date the authority decided"),
                        ("decidedBy", "the authority that decided")):
        value = row.get(field)
        if field not in row:
            failures.append(
                f"PD2-5: decided {RETENTION_DECISION_ID} records no {field!r} "
                f"({what}); a decision with no recorded authority is not a decision")
        elif is_unfilled(value):
            failures.append(
                f"PD2-5: decided {RETENTION_DECISION_ID} carries an UNFILLED "
                f"{field!r} ({value!r}); {what} is a placeholder, so the row is "
                "a drafted amendment rather than a taken decision")
    decided_on = row.get("decidedOn")
    if isinstance(decided_on, str) and not is_unfilled(decided_on) \
            and not ISO_DATE_RE.search(decided_on):
        failures.append(
            f"PD2-5: decided {RETENTION_DECISION_ID} 'decidedOn' {decided_on!r} "
            "carries no ISO date, so the decision moment cannot be ordered "
            "against any review that contradicts it")
    if "decision" not in row:
        failures.append(
            f"PD2-5: decided {RETENTION_DECISION_ID} records no 'decision'; "
            "a status without a substance is a sign-off with nothing signed")
    elif not _non_empty_leaf(row.get("decision")):
        failures.append(
            f"PD2-5: decided {RETENTION_DECISION_ID} 'decision' is empty or "
            "entirely placeholder text")
    rule_text = " ".join(
        str(row.get(field, "")) for field in
        ("ruleAfterDecision", "ruleWhilePending", "rule", "ruleAfter", "implementerRule")
    )
    if not _forbids_implementer_invention(rule_text):
        failures.append(
            f"PD2-5: decided {RETENTION_DECISION_ID} drops the standing "
            "prohibition on an implementer choosing a retention default; "
            "deciding the default does not license inventing one")
    return failures


DECISION_SET_PREFIXES = ("PD-1", "PD-5", "PD2-1", "PD2-5")


def validate_v2(product: object, ri: dict, versioning: dict, delivery: dict,
                retention: dict | None, v1) -> list[str]:
    """The predecessor's validate MINUS its decision-set lane, PLUS this one.

    The partition is explicit and is regression-tested three ways, on FIXTURES
    rather than on whatever state the live packet happens to be in:
      * on a pre-decision fixture both lanes are silent - the old world is
        unchanged;
      * on a fully-formed decided fixture the predecessor lane FIRES and this one
        does not - that difference is the entire behavioural delta of (C), and
        the selftest prints the predecessor's findings so it can be read;
      * on the live packet every NON-decision-set finding is carried through
        byte-identically.
    """
    if not isinstance(product, dict) or not product:
        return ["PD2-TOTALITY-ROOT: product root must be a non-empty object"]
    if not isinstance(product.get("decisions"), dict):
        return ["PD2-TOTALITY-SHAPE: decisions must be an object"]
    inherited = [
        item for item in v1.validate(product, ri, versioning, delivery, retention)
        if not item.startswith(DECISION_SET_PREFIXES)
    ]
    try:
        own = decision_set_failures(product, v1.EXPECTED_CHOICES)
    except v1.MALFORMED_SHAPE_EXCEPTIONS as exc:
        own = [f"PD2-TOTALITY-EXCEPTION: malformed decision shape ({type(exc).__name__})"]
    return inherited + own


# ---------------------------------------------------------------------------
# EVASION AND CONTROL CORPORA for the NEW predicates.
#
# The predecessor's corpora (lines 1288-1370) cover the DETECTION semantics and
# are re-run here unchanged. These cover the DEMOTION semantics, which are new
# and are the only place this successor can have widened a hole.
#
# Each evasion carries an EXPECTED verdict. Cases marked ESCAPES are residuals
# this instrument does NOT close; they are executed rather than described so the
# residual count is measured. A residual that stops escaping is ALSO a failure -
# it means the corpus drifted and the printed residual width is stale.
# ---------------------------------------------------------------------------

_ASSERTION = {"dispositions": {RETENTION_DECISION_ID:
                               "SIGNED OFF 2026-07-31 by product owner."}}


def _doc(**extra) -> dict:
    out = copy.deepcopy(_ASSERTION)
    out.update(extra)
    return out


def _full_review(**extra) -> dict:
    out = _doc(reviewer="independent-reviewer-1",
               verdict={"decision": "PASS", "blockingFindingCount": 0},
               date="2026-08-01",
               subject="thing.v1.json")
    out.update(extra)
    return out


# (label, filename, document, extra corpus docs, expected standing, note[, "DATED"])
# A trailing "DATED" runs the case against a packet that records a decision date,
# which is what makes the 7.2.1 temporal gate applicable.
DEMOTION_EVASIONS = (
    ("bare rename to a review filename, nothing else",
     "forged.review-independent.json", _doc(), (), "LIVE",
     "no reviewer role, no verdict, no subject, no date"),
    ("review filename + verdict only",
     "forged.review-independent.json", _doc(verdict="PASS"), (), "LIVE",
     "reaches a verdict but declares no observer and no frozen moment"),
    ("review filename + reviewer only",
     "forged.review-independent.json", _doc(reviewer="me"), (), "LIVE",
     "declares an observer but no verdict"),
    ("review filename + reviewer + verdict, no subject",
     "forged.review-independent.json",
     _doc(reviewer="me", verdict="PASS", date="2026-08-01"), (), "LIVE",
     "a review with no corpus subject reviewed nothing"),
    ("review filename + reviewer + verdict + subject, NO date",
     "forged.review-independent.json",
     _doc(reviewer="me", verdict="PASS", subject="thing.v1.json"),
     (("thing.v1.json", {}),), "LIVE",
     "records no frozen moment, so 7.2.1 does not apply to it"),
    ("subject names a file that is not in this corpus",
     "forged.review-independent.json",
     _doc(reviewer="me", verdict="PASS", date="2026-08-01",
          subject="does-not-exist.v1.json"), (), "LIVE",
     "naming an absent file is not reviewing an artifact"),
    ("self-referential review - names only itself",
     "forged.review-independent.json",
     _doc(reviewer="me", verdict="PASS", date="2026-08-01",
          subject="forged.review-independent.json"), (), "LIVE",
     "a document is not its own frozen subject"),
    ("stub successor carrying only an identity block",
     "thing.v1.json", copy.deepcopy(_ASSERTION),
     (("thing.v2.json", {"artifact": "thing", "version": 2, "date": "2026-08-05"}),),
     "LIVE", "an identity-only successor carries no content to supersede with"),
    ("successor that is itself independently REJECTED",
     "thing.v1.json", copy.deepcopy(_ASSERTION),
     (("thing.v2.json", {"artifact": "thing", "version": 2, "body": "real"}),
      ("thing.v2.review-independent.json",
       {"subject": "thing.v2.json", "verdict": {"decision": "REJECT",
                                                "blockingFindingCount": 2}})),
     "LIVE", "a rejected successor repairs nothing and displaces nothing"),
    ("successor is a REVIEW of this artifact, not a new version",
     "thing.v1.json", copy.deepcopy(_ASSERTION),
     (("thing.v2.review-independent.json",
       {"reviewer": "r", "verdict": "PASS", "date": "2026-08-01",
        "subject": "thing.v1.json", "body": "x"}),),
     "LIVE", "version arithmetic must not read a review as a later version"),
    ("successor of a DIFFERENT base with a higher number",
     "thing.v1.json", copy.deepcopy(_ASSERTION),
     (("other-thing.v9.json", {"artifact": "other", "version": 9, "body": "y"}),),
     "LIVE", "lineage is per base, not per number"),
    ("lower-numbered sibling only",
     "thing.v9.json", copy.deepcopy(_ASSERTION),
     (("thing.v2.json", {"artifact": "thing", "version": 2, "body": "y"}),),
     "LIVE", "a predecessor never supersedes its successor"),
    ("dotted version - v1.10 must not be read as lower than v1.2",
     "thing.v1.10.json", copy.deepcopy(_ASSERTION),
     (("thing.v1.2.json", {"artifact": "thing", "version": "1.2", "body": "y"}),),
     "LIVE", "1.10 > 1.2 under tuple comparison, not string comparison"),
    # The next four run against a packet that RECORDS a decision date, so the
    # 7.2.1 temporal gate is applicable. They are the only cases that need one,
    # and they carry it explicitly rather than depending on the live packet's
    # state - which is exactly the environment coupling gap (B) was made of.
    ("review dispatched BEFORE the packet decision date",
     "early.review-independent.json",
     _full_review(date="2026-08-01"), (("thing.v1.json", {}),), "REVIEW-RECORD",
     "it could not have read a decision taken later", "DATED"),
    ("review dispatched ON the packet decision date",
     "late.review-independent.json",
     _full_review(date="2026-08-05"), (("thing.v1.json", {}),), "LIVE",
     "it could have read the decided packet, so it is not excused", "DATED"),
    ("review dispatched AFTER the packet decision date",
     "late.review-independent.json",
     _full_review(date="2026-08-09"), (("thing.v1.json", {}),), "LIVE",
     "same", "DATED"),
    ("review with NO date against a dated packet",
     "undated.review-independent.json",
     _full_review(date=None) | {"date": None}, (("thing.v1.json", {}),), "LIVE",
     "no recorded moment means 7.2.1 cannot excuse it", "DATED"),
    # --- residuals: these ESCAPE by construction and are measured, not hidden.
    ("RESIDUAL-1 complete forged review record",
     "forged.review-independent.json",
     _full_review(), (("thing.v1.json", {}),), "REVIEW-RECORD",
     "a document that satisfies all five conjuncts IS a review record to this "
     "instrument; nothing here can tell a real review from a well-built forgery"),
    ("RESIDUAL-2 review-class declared in identity, ordinary filename",
     "ordinary.json",
     _full_review(artifact="opensip.thing.review-independent"),
     (("thing.v1.json", {}),), "REVIEW-RECORD",
     "the identity route is the point - a review not named like one is still "
     "caught - and it is also the cheapest forgery, costing one string"),
    ("RESIDUAL-3 minimal but genuine-shaped successor",
     "thing.v1.json", copy.deepcopy(_ASSERTION),
     (("thing.v2.json", {"artifact": "thing", "version": 2, "note": "wip"}),),
     "SUPERSEDED",
     "one substantive key is enough; this instrument does not grade repair "
     "quality, and a near-stub successor demotes its predecessor"),
    ("RESIDUAL-4 rejecting review forged against a live artifact",
     "thing.v1.json", copy.deepcopy(_ASSERTION),
     (("thing.v1.review-independent.json",
       {"subject": "thing.v1.json",
        "verdict": {"decision": "REJECT", "blockingFindingCount": 1}}),),
     "REJECTED",
     "inherited from the predecessor unchanged and NOT closed here - a forged "
     "rejecting review still launders a live claim into an observation"),
)

# Live artifacts that MUST keep standing. A demotion rule that demotes everything
# is not a rule; these are the shapes that stop this successor over-demoting.
DEMOTION_CONTROLS = (
    ("head of a lineage with no successor at all",
     "thing.v9.json", copy.deepcopy(_ASSERTION), (), "LIVE"),
    ("head whose only later versions were all rejected",
     "thing.v8.json", copy.deepcopy(_ASSERTION),
     (("thing.v9.json", {"artifact": "thing", "version": 9, "body": "x"}),
      ("thing.v9.review-independent.json",
       {"subject": "thing.v9.json",
        "verdict": {"decision": "REJECT", "blockingFindingCount": 1}}),
      ("thing.v10.json", {"artifact": "thing", "version": 10, "body": "x"}),
      ("thing.v10.review-independent.json",
       {"subject": "thing.v10.json",
        "verdict": {"decision": "REJECT", "blockingFindingCount": 3}}))),
    ("unversioned prose artifact with no review and no successor",
     "prose-only.json", copy.deepcopy(_ASSERTION), (), "LIVE"),
    ("artifact with a PASSING review of it - reviewed is not rejected",
     "thing.v1.json", copy.deepcopy(_ASSERTION),
     (("thing.v1.review-independent.json",
       {"subject": "thing.v1.json",
        "verdict": {"decision": "PASS", "blockingFindingCount": 0},
        "sealRecommendation": {"verdict": "DO-NOT-SEAL"}}),)),
    ("artifact whose name merely contains 'previewer'",
     "previewer-notes.json", copy.deepcopy(_ASSERTION), ()),
)

# (C) The decision-set lane: states that must be ACCEPTED and states that must FAIL.
_DECIDED_GOOD = {
    "status": "DECIDED",
    "decidedOn": "2026-08-05",
    "decidedBy": "the product authority",
    "decision": {"boundedRetention": "Retention is bounded."},
    "ruleAfterDecision": "No implementer may still choose a retention DEFAULT.",
}


def _packet(v1, **kw) -> dict:
    """A minimal well-formed packet: the seven live choices plus a retention state."""
    decisions = {
        key: {"status": "DECIDED", "choice": choice}
        for key, choice in v1.EXPECTED_CHOICES.items()
    }
    pending: dict[str, object] = {}
    if "decided" in kw:
        decisions[RETENTION_DECISION_ID] = kw["decided"]
    if "pending" in kw:
        pending[RETENTION_DECISION_ID] = kw["pending"]
    for extra_id, row in (kw.get("extraPending") or {}).items():
        pending[extra_id] = row
    return {"artifact": "opensip.product-dispositions", "version": 1,
            "decisions": decisions, "pendingDecisions": pending}


_PENDING_GOOD = {
    "status": "BLOCKED_ON_PHASE_1A",
    "ruleWhilePending": "No implementer may choose a retention default and no "
                        "freeze may claim V10 resolved.",
}


def decision_state_cases(v1) -> tuple[tuple, tuple]:
    """(must_pass, must_fail) for the dual-state decision lane."""
    def d(**over):
        row = copy.deepcopy(_DECIDED_GOOD)
        row.update(over)
        return row

    must_pass = (
        ("STATE P - pending and blocked", _packet(v1, pending=copy.deepcopy(_PENDING_GOOD))),
        ("STATE D - decided with every required field",
         _packet(v1, decided=d())),
        ("STATE D - CONFIRMED is an accepted decided status",
         _packet(v1, decided=d(status="CONFIRMED"))),
        ("STATE D - post-decision rule reworded but semantically intact",
         _packet(v1, decided=d(ruleAfterDecision="No implementer may select a "
                                                 "retention default."))),
    )
    must_fail = (
        ("STATE D with UNSET decidedBy (the drafted amendment verbatim)",
         _packet(v1, decided=d(decidedBy="[UNSET — the authority's name]"))),
        ("STATE D with UNSET decidedOn (the drafted amendment verbatim)",
         _packet(v1, decided=d(decidedOn="[UNSET — the authority's date]"))),
        ("STATE D with decidedBy missing entirely",
         _packet(v1, decided={k: v for k, v in _DECIDED_GOOD.items() if k != "decidedBy"})),
        ("STATE D with decidedOn missing entirely",
         _packet(v1, decided={k: v for k, v in _DECIDED_GOOD.items() if k != "decidedOn"})),
        ("STATE D with decision missing entirely",
         _packet(v1, decided={k: v for k, v in _DECIDED_GOOD.items() if k != "decision"})),
        ("STATE D with an empty decision body",
         _packet(v1, decided=d(decision={}))),
        ("STATE D with a placeholder decision body",
         _packet(v1, decided=d(decision="TBD"))),
        ("STATE D with decidedBy = 'TBD'", _packet(v1, decided=d(decidedBy="TBD"))),
        ("STATE D with decidedBy = '' ", _packet(v1, decided=d(decidedBy=""))),
        ("STATE D with a non-ISO decidedOn",
         _packet(v1, decided=d(decidedOn="last Tuesday"))),
        ("STATE D with status still PENDING",
         _packet(v1, decided=d(status="PENDING"))),
        ("STATE D dropping the implementer prohibition",
         _packet(v1, decided=d(ruleAfterDecision="Implementers may now choose a "
                                                 "retention default."))),
        ("STATE D with no post-decision rule at all",
         _packet(v1, decided={k: v for k, v in _DECIDED_GOOD.items()
                              if k != "ruleAfterDecision"})),
        ("STATE P with status silently flipped to DECIDED",
         _packet(v1, pending=dict(_PENDING_GOOD, status="DECIDED"))),
        ("STATE P permitting implementer invention",
         _packet(v1, pending={"status": "BLOCKED_ON_PHASE_1A",
                              "ruleWhilePending": "Implementers may pick one."})),
        ("BOTH states at once", _packet(v1, decided=d(),
                                        pending=copy.deepcopy(_PENDING_GOOD))),
        ("NEITHER state - the decision has vanished", _packet(v1)),
        ("a second Phase-2 decision quietly becomes pending",
         _packet(v1, pending=copy.deepcopy(_PENDING_GOOD),
                 extraPending={"CD-XX-1": {"status": "BLOCKED_ON_PHASE_1A"}})),
        ("a non-retention choice silently reopened",
         _packet(v1, pending=copy.deepcopy(_PENDING_GOOD)) | {
             "decisions": dict(
                 {k: {"status": "DECIDED", "choice": c}
                  for k, c in v1.EXPECTED_CHOICES.items()},
                 **{"P-1": {"status": "DECIDED", "choice": "MAYBE"}})}),
    )
    return must_pass, must_fail


# ---------------------------------------------------------------------------
# Selftest.
# ---------------------------------------------------------------------------

def _standing_in(name: str, doc: object, extras, product: dict, v1) -> tuple[str, str]:
    docs = [(name, doc)] + [(n, d) for n, d in extras]
    rejected = rejecting_reviews(docs, v1)
    records = review_records(docs, v1)
    return standing_of(name, doc, docs, rejected, records,
                       packet_decision_dates(product))


def selftest(product: dict, ri: dict, versioning: dict, delivery: dict,
             retention: dict | None, register: object, v1) -> int:
    """Every claim this file makes, executed. A green run here is author-side
    evidence only - section 7.8's bound is not discharged by more assertions
    from the same lane."""
    failed = 0
    refused: list[str] = []
    counts: dict[str, int] = {}

    def check(bucket: str, ok: bool, label: str, detail: str = "") -> None:
        nonlocal failed
        counts[bucket] = counts.get(bucket, 0) + 1
        if ok:
            print(f"  ok      [{bucket}] {label}")
            if detail:
                print(f"            {detail}")
        else:
            failed += 1
            print(f"  FAILED  [{bucket}] {label}")
            print(f"            {detail}")

    # Every fixture below carries its own packet. The predecessor's suites read
    # the LIVE packet, which is why they go inert the moment the decision they
    # were written around is taken - the same coupling as gap (C). This
    # successor's own suites must stay meaningful in BOTH states, so they build
    # the world they test.
    pending_packet = _packet(v1, pending=copy.deepcopy(_PENDING_GOOD))
    decided_packet = _packet(v1, decided=copy.deepcopy(_DECIDED_GOOD))

    # --- 0. The predecessor's OWN suites, unchanged. This is the only way to
    # claim "no detection semantics were weakened" as a measurement rather than
    # as a sentence. It is scoped to the pre-decision world by construction: it
    # refuses once the packet advances. A refusal is NOT a pass - it is recorded
    # as INAPPLICABLE and forces EXIT_REFUSED, so a green selftest can never be
    # produced without this suite having actually executed (section 7.2, the
    # dead `--selftest` instance).
    print("predecessor regression - its own selftest, re-run through this successor")
    inherited_status = v1.mutation_selftest(product, ri, versioning, delivery,
                                            retention, register)
    if inherited_status == EXIT_REFUSED:
        refused.append(
            "the pinned predecessor's suite REFUSED (exit 3): it is written "
            "around the pre-decision packet and cannot run once the retention "
            "decision is taken. Its guarantee is NOT claimed by this run.")
        print("  INAPPLICABLE  [inherited] predecessor suite refused - "
              "SELFTEST-PARTIAL")
    else:
        check("inherited", inherited_status == EXIT_OK,
              "the pinned predecessor's full mutation/assertion/standing suite",
              f"exit={inherited_status}")

    # --- 1. Lane-partition equivalence, measured on fixtures rather than on
    # whatever state the live packet happens to be in.
    print("lane partition - what the replaced decision-set lane did and did not change")

    def v1_lane_of(packet: dict) -> list[str]:
        return [i for i in v1.validate(packet, ri, versioning, delivery, None)
                if i.startswith(DECISION_SET_PREFIXES)]

    check("partition", not v1_lane_of(pending_packet)
          and not decision_set_failures(pending_packet, v1.EXPECTED_CHOICES),
          "STATE P: predecessor lane and successor lane are BOTH silent",
          "the pre-decision world is unchanged")
    v1_on_decided = v1_lane_of(decided_packet)
    v2_on_decided = decision_set_failures(decided_packet, v1.EXPECTED_CHOICES)
    check("partition", bool(v1_on_decided) and not v2_on_decided,
          "STATE D: the predecessor lane FIRES and the successor lane does not",
          f"this is the entire behavioural delta of (C) - predecessor emits "
          f"{len(v1_on_decided)} finding(s) on a fully-formed decision, "
          f"successor emits {len(v2_on_decided)}: "
          + "; ".join(i[:70] for i in v1_on_decided[:3]))
    v1_all = v1.validate(product, ri, versioning, delivery, retention)
    v1_rest = [i for i in v1_all if not i.startswith(DECISION_SET_PREFIXES)]
    v2_all = validate_v2(product, ri, versioning, delivery, retention, v1)
    check("partition",
          [i for i in v2_all if not i.startswith(DECISION_SET_PREFIXES)] == v1_rest,
          "every NON-decision-set finding is carried through byte-identically",
          f"{len(v1_rest)} inherited finding(s) on the live packet")

    # --- 2. (C) the dual-state decision lane.
    print("decision-set lane - both states accepted, every required field enforced")
    must_pass, must_fail = decision_state_cases(v1)
    for label, packet in must_pass:
        found = decision_set_failures(packet, v1.EXPECTED_CHOICES)
        check("decision-accept", not found, label,
              found[0] if found else "no finding")
    for label, packet in must_fail:
        found = decision_set_failures(packet, v1.EXPECTED_CHOICES)
        check("decision-reject", bool(found), label,
              found[0] if found else "ESCAPED - no finding produced")

    # --- 3. (A)+(B) demotion evasions.
    print("demotion evasion corpus - a forged demotion must not launder a claim")
    escapes_expected = 0
    dated_packet = _packet(v1, decided=copy.deepcopy(_DECIDED_GOOD))
    check("evasion", packet_decision_dates(dated_packet) == {RETENTION_DECISION_ID: "2026-08-05"},
          "the dated fixture packet really does record a decision date",
          "otherwise the four temporal cases below would pass vacuously")
    for row in DEMOTION_EVASIONS:
        label, name, doc, extras, expected, note = row[:6]
        packet = dated_packet if (len(row) > 6 and row[6] == "DATED") else product
        standing, why = _standing_in(name, doc, extras, packet, v1)
        if expected != "LIVE" and label.startswith("RESIDUAL"):
            escapes_expected += 1
        check("evasion", standing == expected, f"{label} -> {expected}",
              f"got {standing}: {why[:150]} | {note}")

    # --- 4. (A)+(B) controls: nothing over-demoted.
    print("demotion control corpus - a live artifact must keep its standing")
    for row in DEMOTION_CONTROLS:
        label, name, doc, extras = row[0], row[1], row[2], row[3]
        standing, why = _standing_in(name, doc, extras, product, v1)
        check("control", standing == "LIVE", label, f"got {standing}: {why[:150]}")

    # --- 5. The gate itself, end to end, both directions. A demotion must be an
    # OBSERVATION, never a drop; a live conflict must still FAIL.
    # The packet here is a FIXTURE that holds the retention decision pending, so
    # the fabrication conflicts with it in either live state. Using the live
    # packet made these go inert the moment the decision was taken.
    print("gate direction - demoted is reported, live still fails")
    gate_packet = pending_packet
    fabricated = copy.deepcopy(register)
    v1._register_fabricated_verbatim(fabricated)
    reg = v1.REGISTER_PATH.name
    live_docs = [(reg, fabricated)]
    f, o, _ = classify(gate_packet, live_docs, [], 1, v1)
    check("gate", bool(f) and not o, "fabrication in a LIVE artifact FAILS",
          f[0][:150] if f else "no failure produced")
    reg_base = split_version(reg)
    check("gate", reg_base is not None,
          "the register filename carries a parseable version, so a successor "
          "fixture can be constructed for it",
          f"{reg} -> {reg_base}")
    successor_name = f"{reg_base[0]}.v{reg_base[1][0] + 1}.json" if reg_base else "x.v2.json"
    sup_docs = live_docs + [(successor_name,
                             {"artifact": "reg", "version": 2, "body": "real"})]
    f, o, _ = classify(gate_packet, sup_docs, [], 2, v1)
    check("gate", not f and bool(o),
          "the same fabrication in a SUPERSEDED artifact is an OBSERVATION",
          o[0][:150] if o else "no observation produced")
    rev_docs = live_docs + [(reg[: -len(".json")] + ".review-independent.json",
                             {"subject": reg, "verdict": {"decision": "REJECT",
                                                          "blockingFindingCount": 1}})]
    f, o, _ = classify(gate_packet, rev_docs, [], 2, v1)
    check("gate", not f and bool(o),
          "the same fabrication in a REJECTED artifact is an OBSERVATION",
          o[0][:150] if o else "no observation produced")
    f, o, _ = classify(gate_packet, [(reg, register)], [], 1, v1)
    check("gate", not f and not o, "the live corrected register produces neither",
          "clean")

    # --- 6. Non-vacuity of each conjunct, measured over the LIVE corpus. If a
    # conjunct excludes nothing it is decoration, and this prints the number.
    print("conjunct non-vacuity - measured over the live corpus, not asserted")
    docs, unreadable, discovered = v1.scan_artifacts(HERE)
    corpus = {n for n, _ in docs}
    fre = v1.FILE_REFERENCE_RE
    d1 = [n for n, d in docs if declares_review_class(n, d)]
    d2 = [n for n, d in docs if declares_review_class(n, d) and has_reviewer_role(d)]
    d3 = [n for n, d in docs if declares_review_class(n, d) and has_reviewer_role(d)
          and has_verdict_shape(d)]
    d4 = [n for n, d in docs if declares_review_class(n, d) and has_reviewer_role(d)
          and has_verdict_shape(d) and names_other_corpus_files(n, d, corpus, fre)]
    d5 = [n for n, d in docs if review_record_reason(n, d, corpus, fre)]
    for label, before, after in (
        ("reviewer-role conjunct", d1, d2),
        ("verdict conjunct", d2, d3),
        ("corpus-subject conjunct", d3, d4),
        ("dispatch-date conjunct", d4, d5),
    ):
        check("nonvacuity", len(after) < len(before),
              f"{label} excludes at least one live document",
              f"{len(before)} -> {len(after)} (excluded {len(before) - len(after)})")
    check("nonvacuity", len(d5) < len(docs),
          "review records are a proper subset of the corpus",
          f"{len(d5)} of {len(docs)}")

    # --- 7. Environment independence. The measured root cause of gap (B) was a
    # dependency on two markdown files outside the scanned directory. This
    # successor must produce the identical verdict with and without them.
    print("environment independence - the gap (B) root cause must not recur")
    heads, head_docs = v1.head_named_artifacts(HERE)
    # Source-level: no standing predicate may even mention the head-document API.
    import inspect
    predicates = (declares_review_class, has_reviewer_role, has_verdict_shape,
                  names_other_corpus_files, dispatch_date, review_record_reason,
                  split_version, carries_content, supersession_reason,
                  rejecting_reviews, review_records, standing_of, classify,
                  decision_set_failures)
    leaked = sorted(
        fn.__name__ for fn in predicates
        if any(token in inspect.getsource(fn)
               for token in ("head_named_artifacts", "HEAD_DOC_NAMES"))
    )
    check("environment", not leaked,
          f"none of the {len(predicates)} standing/decision predicates consults "
          "a head document",
          f"leaked: {leaked}" if leaked else "verified by inspect.getsource")
    # Behavioural: with the head-document reader neutered, the verdict is byte-
    # identical. This is the check that would have caught the predecessor's bug.
    baseline = classify(product, docs, unreadable, discovered, v1)
    saved = v1.head_named_artifacts
    try:
        v1.head_named_artifacts = lambda root=None: (set(), [])
        blinded = classify(product, docs, unreadable, discovered, v1)
    finally:
        v1.head_named_artifacts = saved
    check("environment", baseline[0] == blinded[0] and baseline[1] == blinded[1],
          "removing every head document changes NOTHING about the verdict",
          f"{len(head_docs)} head doc(s) readable, {len(heads)} names harvested; "
          f"findings {len(baseline[0])}=={len(blinded[0])}, "
          f"observations {len(baseline[1])}=={len(blinded[1])}")
    # Root cause layer 2, counted rather than asserted: how many real successors
    # would the predecessor's prose-gated limb be unable to see? If this is 0 the
    # module docstring has gone stale and must be corrected, so 0 FAILS.
    bases: dict[str, list[tuple[tuple[int, ...], str]]] = {}
    record_names = review_records(docs, v1)
    for other, _ in docs:
        version = split_version(other)
        if version and other not in record_names:
            bases.setdefault(version[0], []).append((version[1], other))
    invisible = sorted(
        name
        for members in bases.values() if len(members) > 1
        for version, name in members
        if version > min(members)[0] and name not in heads
    )
    # Non-interference: this instrument must leave no trace in a directory other
    # instruments measure. A .pyc dropped by loading the predecessor would do so.
    cache = HERE / "__pycache__"
    before = {p.name for p in cache.glob("*.pyc")} if cache.is_dir() else set()
    _load_predecessor()
    after = {p.name for p in cache.glob("*.pyc")} if cache.is_dir() else set()
    check("environment", before == after,
          "loading the pinned predecessor writes NO bytecode into a directory "
          "sibling instruments snapshot",
          f"__pycache__ delta: {sorted(after - before) or 'none'}")

    check("environment", bool(invisible),
          "successors that exist on disk yet NO head document names - the "
          "predecessor's supersession limb is structurally blind to every one",
          f"{len(invisible)} of {sum(len(v) for v in bases.values() if len(v) > 1)} "
          "non-earliest versioned artifacts")

    print()
    print("selftest summary - " + ", ".join(
        f"{bucket} {n}" for bucket, n in sorted(counts.items())))
    print(f"  demotion evasions attempted {len(DEMOTION_EVASIONS)}, "
          f"caught {len(DEMOTION_EVASIONS) - escapes_expected}, "
          f"NOT closed (measured residuals) {escapes_expected}")
    print(f"  demotion controls held {len(DEMOTION_CONTROLS)}")
    print(f"  decision states accepted {len(must_pass)}, rejected {len(must_fail)}")
    if failed:
        print(f"SELFTEST FAILED - {failed} check(s) did not hold")
        return EXIT_FINDINGS
    if refused:
        print("SELFTEST-PARTIAL / SELFTEST-REFUSED - every check that RAN held, "
              "but at least one suite did not run:")
        for item in refused:
            print(f"  - {item}")
        print("A partial run is not a green run. Exit 3, distinct from green (0), "
              "findings (1) and bad invocation (2).")
        return EXIT_REFUSED
    print("SELFTEST PASSED - every claim in this file is one this file can falsify")
    return EXIT_OK


# ---------------------------------------------------------------------------
# Reporting.
# ---------------------------------------------------------------------------

def format_report(report: dict[str, object], head_docs: list[str]) -> list[str]:
    demoted = report["demotedByStanding"]  # type: ignore[index]
    sites = (int(report["keyAnchoredSites"]) + int(report["keyScopedStrings"])
             + int(report["proseSites"]))
    return [
        "assertion-lane coverage (measured this run, not declared):",
        f"  artifacts discovered      {report['artifactsDiscovered']}",
        f"  artifacts parsed+scanned  {report['artifactsParsed']}",
        f"  artifacts unreadable      {len(report['artifactsUnreadable'])}"
        + (f" -> {', '.join(report['artifactsUnreadable'])}"  # type: ignore[arg-type]
           if report["artifactsUnreadable"] else ""),
        f"  claim register            {'READ' if report['registerRead'] else 'NOT READ'}",
        f"  packet decision ids       {report['packetDecisionIds']}"
        f" (with a usable decidedOn: {len(report['packetDecisionDates'])})",  # type: ignore[arg-type]
        f"  disposition sites found   {sites}"
        f" (key-anchored {report['keyAnchoredSites']},"
        f" key-scoped fields {report['keyScopedStrings']},"
        f" prose {report['proseSites']})",
        f"  cross-checked vs a packet row     {report['sitesAgainstPacketRow']}",
        f"  checked vs unbacked-closure rule  {report['sitesAgainstUnbackedRule']}",
        f"  clauses semantically classified   {report['clausesClassified']}",
        "  standing of asserting artifacts (DISCOVERED, not listed):",
        f"    LIVE {report['artifactsLive']}"
        f" / REJECTED {report['artifactsRejected']}"
        f" / REVIEW-RECORD {report['artifactsReviewRecord']}"
        f" / SUPERSEDED {report['artifactsSuperseded']}",
        f"    head documents readable {len(head_docs)}"
        + (f" ({', '.join(head_docs)})" if head_docs else "")
        + " - READ FOR THIS LINE ONLY; no predicate consults them",
        f"  conflicting assertions in LIVE artifacts   {report['conflicts']}"
        " (these fail)",
        f"  demoted to observations                    "
        f"{report['historicalObservations']} across "
        f"{report['conflictingArtifactsHistorical']} artifact(s)"
        f" - REJECTED {demoted['REJECTED']},"  # type: ignore[index]
        f" REVIEW-RECORD {demoted['REVIEW-RECORD']},"  # type: ignore[index]
        f" SUPERSEDED {demoted['SUPERSEDED']}",  # type: ignore[index]
        "  NOT observed by this instrument: non-JSON artifacts (*.md, *.py),",
        "  anything outside this directory, unparseable bytes listed above, and",
        "  any closure assertion that names no decision id and sits under no",
        "  decision-id key.",
        "  RESIDUALS THIS INSTRUMENT DOES NOT CLOSE, each executed by a case in",
        "  the --selftest evasion corpus that is EXPECTED to escape:",
        "    R1  a document satisfying all five review-record conjuncts IS a",
        "        review record here; a well-built forgery is indistinguishable.",
        "    R2  the identity route costs one string, so a forger need not even",
        "        rename the file. Kept because a real review not named like one",
        "        must still be found.",
        "    R3  one substantive key makes a successor; repair QUALITY is not",
        "        graded, so a near-stub successor demotes its predecessor.",
        "    R4  the predecessor's forged-rejecting-review hole is INHERITED",
        "        UNCHANGED and is not narrowed here.",
        "  Section 7.8's bound applies in full: this binds structure and type,",
        "  never the truth of content.",
    ]


def _load(path: Path, required: bool = True) -> tuple[object, str | None]:
    if not path.exists():
        return (None, f"required input {path.name} is missing") if required else (None, None)
    try:
        return json.loads(path.read_text()), None
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return None, f"cannot read {path.name} ({type(exc).__name__})"


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    unknown = [a for a in args if a not in DECLARED_FLAGS]
    if unknown:
        print(f"usage: {Path(__file__).name} [--selftest]")
        print(f"  unrecognised argument(s): {' '.join(unknown)}")
        return EXIT_USAGE
    want_selftest = "--selftest" in args

    try:
        v1 = _load_predecessor()
    except RuntimeError as exc:
        print("REFUSING to run: the pinned predecessor closure is dirty")
        print(f"  - {exc}")
        print("SELFTEST-NOT-RUN" if want_selftest else "SCAN-NOT-RUN")
        return EXIT_REFUSED

    inputs: dict[str, object] = {}
    refusals: list[str] = []
    for key, path, required in (
        ("product", v1.PRODUCT_PATH, True),
        ("ri", v1.RI_PATH, True),
        ("versioning", v1.VERSIONING_PATH, True),
        ("delivery", v1.DELIVERY_PATH, True),
        ("register", v1.REGISTER_PATH, True),
        ("retention", v1.RETENTION_PATH, False),
    ):
        value, problem = _load(path, required)
        if problem:
            refusals.append(problem)
        inputs[key] = value
    if refusals:
        print("REFUSING to run: the checker's own base is dirty")
        for problem in refusals:
            print(f"  - {problem}")
        print("SELFTEST-NOT-RUN" if want_selftest else "SCAN-NOT-RUN")
        return EXIT_REFUSED

    product = inputs["product"]
    ri, versioning, delivery = inputs["ri"], inputs["versioning"], inputs["delivery"]
    retention, register = inputs["retention"], inputs["register"]

    print(f"successor to {PREDECESSOR_BINDING['path']}"
          f"@sha256:{PREDECESSOR_BINDING['sha256']} (hash-verified, executed as a "
          "runtime input under freeze 7.3)")

    if want_selftest:
        return selftest(product, ri, versioning, delivery, retention, register, v1)

    failures = v1.retention_binding_failures()
    failures.extend(validate_v2(product, ri, versioning, delivery, retention, v1))
    docs, unreadable, discovered = v1.scan_artifacts(HERE)
    assertion_failures, observations, report = classify(
        product, docs, unreadable, discovered, v1)
    failures.extend(assertion_failures)
    _, head_docs = v1.head_named_artifacts(HERE)

    for line in format_report(report, head_docs):
        print(line)
    if observations:
        print("HISTORICAL OBSERVATIONS - a product-decision assertion conflicting "
              "with the binding")
        print("packet, in an artifact with no standing to make it. Not a finding: "
              "freeze 7.2")
        print("forbids editing reviewed bytes and 7.2.1 forbids repairing a "
              "review at all, so")
        print("these cannot be repaired. Reported in full, never dropped:")
        for line in observations:
            print(f"  {line}")
    if failures:
        print("product dispositions INVALID")
        for failure in failures:
            print(f"  - {failure}")
        return EXIT_FINDINGS
    print(
        f"product dispositions OK - {len(v1.EXPECTED_CHOICES)} non-retention "
        f"choices bound; the retention decision is in exactly one valid state; "
        f"no artifact with standing ({report['artifactsLive']} of "
        f"{report['artifactsParsed']} scanned) asserts a product decision the "
        f"binding packet does not carry; {report['historicalObservations']} such "
        f"assertion(s) remain in {report['conflictingArtifactsHistorical']} "
        f"historical artifact(s), listed above; consumed "
        f"{v1.EVALUATION_PROOF_BINDING['path']}@sha256:"
        f"{v1.EVALUATION_PROOF_BINDING['sha256']} -> "
        f"{v1.RETENTION_BINDING['path']}@sha256:{v1.RETENTION_BINDING['sha256']}"
    )
    return EXIT_OK


if __name__ == "__main__":
    raise SystemExit(main())
