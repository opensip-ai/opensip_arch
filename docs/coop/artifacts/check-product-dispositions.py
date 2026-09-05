#!/usr/bin/env python3
"""Validate the Phase-2 product dispositions and their live contract joins.

Two guards live here.

1. The original *candidate lane*: the exact Phase-1A retention candidate bound by
   digest may not manufacture the product disposition this authority still marks
   pending.
2. The *assertion lane* (added 2026-08-03): every parsed JSON artifact in this
   directory is read, and any product-decision assertion it carries must agree
   with the binding packet. This exists because a fabricated `CD-RT-5` sign-off
   lived in `claim-register.v1.json` for three days while guard 1 printed a green
   banner — guard 1 covered the artifact where the defect was first seen instead
   of the class of artifact that can carry it.

The assertion lane detects by meaning, not by literal string. It normalises
text, extracts the disposition family a site asserts (CLOSED_POSITIVE / PENDING
/ CLOSED_NEGATIVE), and requires agreement with the packet row. A reworded
sign-off ("ratified by the product owner", "product acceptance granted") is
caught; the corrected register value, which *quotes and retracts* the
fabrication, is not.
"""

from __future__ import annotations

import copy
import hashlib
import json
import re
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
PRODUCT_PATH = HERE / "product-dispositions.v1.json"
REGISTER_PATH = HERE / "claim-register.v1.json"
RI_PATH = HERE / "resolved-inputs.v2.json"
VERSIONING_PATH = HERE / "versioning-policy.v2.json"
DELIVERY_PATH = HERE / "delivery.v2.json"
EVALUATION_PROOF_BINDING = {
    "path": "evaluation-proof.v5.json",
    "sha256": "e05f6d8d9dd5f1f98dc1972a178c7fe58981c71b06a69feb00a717e03475988b",
}
RETENTION_BINDING = {
    "path": "retention-tiers.v10.json",
    "sha256": "606b5e7125d4a3a46f44f1a7565f9c9ea69132d9ab2783d00339e1b8aac5e026",
}
EVALUATION_PROOF_PATH = HERE / EVALUATION_PROOF_BINDING["path"]
RETENTION_PATH = HERE / RETENTION_BINDING["path"]
RETENTION_V10_TOP_KEYS = {
    "artifact", "version", "status", "claimId", "supersedesAsArchitectureCandidate",
    "capabilityClosure", "leaseProtocol", "storageAndLineage", "d9Derivation",
    "custodyPolicy", "authority", "integrationState", "invariants", "assurance",
    "retainedResiduals", "sealRecommendation", "rawPhysicalIdentityContract",
}
TOTALITY_ROOT_CASES = (
    ("string", "hostile-root"),
    ("null", None),
    ("list", []),
    ("empty-object", {}),
)
TOTALITY_NESTED_CASES = TOTALITY_ROOT_CASES
MALFORMED_SHAPE_EXCEPTIONS = (
    AttributeError, IndexError, KeyError, StopIteration, TypeError, ValueError,
)


EXPECTED_CHOICES = {
    "P-1": "NO_ECOSYSTEM_DEPTH_FOR_V1",
    "P-2": "NARROW_CONTRIBUTION_ONTOLOGY",
    "A1-RI-04": "CI_IGNORES_LAYER_4",
    "VER-PIVOT-COST": "EXPLICIT_COMPARE_ON_DETECTOR_MAJOR_CHANGE_ONLY",
    "PUBLIC-RULE-IR": "DO_NOT_FREEZE_FOR_V1",
    "SUPPORT-WINDOWS": "PROVISIONAL_GUESSED_NOT_SLA",
    "G3-SUBSTRATE": "DELIVERY_V2_BINDING",
}


EXIT_OK = 0
EXIT_FINDINGS = 1
EXIT_USAGE = 2
EXIT_REFUSED = 3
DECLARED_FLAGS = ("--selftest",)


# ---------------------------------------------------------------------------
# Assertion lane: semantic vocabulary.
#
# Every list below is a CONCEPT, not a spelling. Detection normalises text first
# (case, punctuation, hyphen/underscore) so SIGNED_OFF / signed-off / Signed Off
# collapse to one token, and each concept carries enough distinct stems that a
# rename or a synonym does not evade it. Nothing here greps for the historical
# "SIGNED OFF 2026-07-31" literal.
# ---------------------------------------------------------------------------

# A completed closure PREDICATED of a decision (participle / perfect forms).
# Referential nouns ("acceptance", "sign-off", "disposition") are deliberately
# absent: they name the act rather than assert it happened, and including them
# collapsed precision from 100% to 8% against this corpus.
CLOSURE_PREDICATIVE = (
    "signed off", "signedoff", "countersigned", "counter signed", "accepted",
    "approved", "ratified", "endorsed", "discharged", "granted", "resolved",
    "closed", "decided", "confirmed", "sealed", "settled", "adopted",
    "dispositioned", "cleared", "signed", "carried", "blessed", "okayed",
    "greenlit", "green lit", "authorised", "authorized",
)
# Bare/imperative forms. A disposition map records its verdict as a leading
# token ("ACCEPT direction ...", "POSTPONE (agree B)"), so the HEAD of a
# key-anchored value reads these as dispositional too. They are not enough on
# their own inside free prose, where they are almost always infinitival.
CLOSURE_HEAD_BARE = (
    "accept", "approve", "ratify", "endorse", "discharge", "grant", "resolve",
    "close", "decide", "confirm", "seal", "settle", "adopt", "clear", "carry",
    "sign off", "signoff",
)
# Dispositional: these say the DECISION is not closed.
CLOSURE_PENDING_STRONG = (
    "blocked", "blocking", "pending", "unresolved", "undecided", "awaiting",
    "await", "deferred", "defer", "postpone", "postponed", "tbd", "unset",
    "unsigned", "open", "indeterminate", "not decided", "not discharged",
)
# Editorial: these say the RECORD is unchanged/parked. They suppress a closure
# reading but are not themselves a claim about the decision, so they never
# create a conflict on their own.
CLOSURE_PENDING_WEAK = (
    "remains", "remain", "still", "unchanged", "untouched", "unpromoted",
    "separate", "separately", "in flight", "not applied", "unapplied",
    "outstanding",
)
CLOSURE_PENDING = CLOSURE_PENDING_STRONG + CLOSURE_PENDING_WEAK
CLOSURE_NEGATIVE = (
    "reject", "rejected", "rejects", "denied", "denies", "refused", "refuses",
    "withdraw", "withdrawn", "withdraws", "revoked", "revokes", "rescinded",
    "rescinds", "struck", "strike", "abandoned", "superseded", "invalid",
)
# The authority the fabrication borrowed. An architecture verdict ("ACCEPT
# direction sealedTier immutable") carries none of these and is not a product
# claim; "accepted by product owner" is.
PRODUCT_AUTHORITY = (
    "product owner", "product authority", "product acceptance", "product accepted",
    "product decision", "product decided", "product signed", "product sign off",
    "product signoff", "product disposition", "by product", "productowner",
    "product accept",
)
NEGATORS = (
    "not", "no", "never", "none", "nor", "without", "cannot", "neither",
    "nothing", "non", "false", "un",
)
# Reporting verbs. "X says CD-RT-5 is signed" reports an assertion; it does not
# make one.
ATTRIBUTIVE = (
    "says", "say", "said", "asserts", "assert", "asserted", "claims", "claim",
    "claimed", "states", "state", "stated", "reports", "report", "reported",
    "describes", "describe", "described", "alleges", "purports", "records",
    "record", "recorded", "reads", "noted", "notes", "flagged", "observed",
    "declare", "declares", "declared", "scenario", "expected",
)
MODAL = (
    "must", "should", "shall", "can", "could", "may", "might", "would", "will",
    "require", "requires", "required", "recommend", "recommends", "recommended",
    "recommendation", "propose", "proposes", "proposed", "needs", "ought", "only",
)
SUBORDINATOR = (
    "if", "unless", "until", "when", "once", "while", "after", "before",
    "whenever", "whether", "either", "or",
)
HISTORICAL = (
    "previously", "formerly", "prior", "historical", "history", "superseded",
    "supersedes", "originated", "originates", "citation repair", "was already",
    "stale", "earlier", "no longer", "used to", "at the time", "paraphrase",
    "struck", "strike", "retracted", "rescinded", "fabricated", "corrected",
    "correction", "verbatim", "regression", "fixture", "mutation", "probe",
)

# ---------------------------------------------------------------------------
# Standing: does the artifact making an assertion have any authority?
#
# An artifact that an independent review REJECTED, or that a later head has
# superseded, asserts nothing — it is a historical record, and freeze §7.2
# forbids editing reviewed bytes in place, so its text can never be repaired.
# Failing forever on a finding nobody is permitted to fix destroys the signal
# the guard exists to carry. Such assertions are reported as HISTORICAL
# OBSERVATIONS, never dropped, and never silently.
#
# Standing is DISCOVERED, not listed. Nothing below names an artifact.
# ---------------------------------------------------------------------------
HEAD_DOC_NAMES = ("IMPLEMENTATION-FREEZE.md", "IMPLEMENTER-BLUEPRINT.md")
VERSIONED_RE = re.compile(r"^(?P<base>.+)\.v(?P<ver>\d+(?:\.\d+)*)$")
REVIEW_MARKERS = ("review", "adjudication", "rereview", "litmus",
                  "closure-coordinator")
# Keys through which a review declares what it reviews. Declarations nest:
# ep9's is {"subject": {"candidate": {"file": "evaluation-proof.v9.json"}}}.
SUBJECT_KEYS = ("artifact", "artifactUnderReview", "subject", "reviewed",
                "target", "reviewOf", "candidate", "subjectArtifact")
BLOCKING_SEVERITY = ("CRITICAL", "BLOCKER", "HIGH", "MAJOR")
OPEN_FINDING_MARKERS = ("FINDINGS-OPEN", "FINDINGS OPEN", "OPEN-FINDINGS",
                        "UNRESOLVED", "REJECT")

DECISION_ID_RE = re.compile(r"\bCD-[A-Z0-9]+(?:-[A-Z0-9]+)*\b")
FILE_REFERENCE_RE = re.compile(r"[A-Za-z0-9._-]+\.(?:json|md|py)\b")
PLACEHOLDER_RE = re.compile(r"<[A-Z_0-9]+>|\[[A-Z _0-9-]+\]")
POINTER_RE = re.compile(r"(\.json#|\.md#|^artifacts/|^docs/)")
QUOTE_CHARS = "\"'‘’“”`"
# Sub-object fields that carry a decision's recorded state. Covers both the
# bare-string form and the structured {decidedBy, decision, rationale} form the
# register uses for genuine product decisions (claim P-4).
DISPOSITION_FIELDS = (
    "status", "state", "currentstate", "decision", "disposition", "verdict",
    "outcome", "choice", "decidedby", "signoff", "signedoff", "resolution",
    "acceptedby", "approval", "productacceptance", "productdecision",
)


def load(path: Path) -> dict:
    return json.loads(path.read_text())


def _normalise(text: str) -> str:
    """Case/punctuation-insensitive token stream, space-padded for phrase match."""
    lowered = text.lower().replace("—", " ").replace("–", " ")
    flattened = "".join(ch if ch.isalnum() else " " for ch in lowered)
    return " " + " ".join(flattened.split()) + " "


def _find_term(norm: str, terms: tuple[str, ...]) -> tuple[int, str] | None:
    """Earliest occurrence of any concept stem, as (offset, stem)."""
    best: tuple[int, str] | None = None
    for term in terms:
        index = norm.find(" " + term.strip() + " ")
        if index >= 0 and (best is None or index < best[0]):
            best = (index, term)
    return best


def _has_term(norm: str, terms: tuple[str, ...]) -> bool:
    return _find_term(norm, terms) is not None


def _clause_units(text: str) -> list[str]:
    """Sentence-level units. Sub-clauses stay attached to their subject."""
    return [part for part in re.split(r"(?<=[.!?])\s+|\n+", text) if part.strip()]


def _head_family(text: str, bare_ok: bool = True) -> tuple[str, str | None]:
    """Disposition family asserted by the leading disposition token of a value.

    A disposition map records its verdict first and its rationale afterwards, so
    the earliest state token in the head unit is what the site asserts. The
    fabricated value led with a sign-off; the corrected value leads with
    BLOCKED_ON_PHASE_1A and only then narrates the retraction.
    """
    norm = _normalise(text)
    positive_terms = CLOSURE_PREDICATIVE + (CLOSURE_HEAD_BARE if bare_ok else ())
    positive = _find_term(norm, positive_terms)
    if positive is not None and _has_term(norm[: positive[0]] + " ", NEGATORS):
        positive = None
    candidates = [
        (found[0], family, found[1])
        for found, family in (
            (positive, "CLOSED_POSITIVE"),
            (_find_term(norm, CLOSURE_PENDING_STRONG), "PENDING"),
            (_find_term(norm, CLOSURE_NEGATIVE), "CLOSED_NEGATIVE"),
        )
        if found is not None
    ]
    if not candidates:
        return "UNKNOWN", None
    candidates.sort()
    return candidates[0][1], candidates[0][2]


def asserts_completed_product_closure(clause: str) -> tuple[bool, str]:
    """Does this clause CONSTITUTE a completed product closure?

    True only for an unhedged, unattributed, unnegated present assertion that a
    product authority has closed something. Every other reading — quoting it,
    retracting it, requiring it, predicting it, or reporting that another
    artifact said it — is not an assertion and returns the reason why.
    """
    norm = _normalise(clause)
    if any(quote in clause for quote in QUOTE_CHARS):
        return False, "quoted"
    if (FILE_REFERENCE_RE.search(clause) or PLACEHOLDER_RE.search(clause)
            or POINTER_RE.search(clause.strip())):
        return False, "citation-or-template"
    closure = _find_term(norm, CLOSURE_PREDICATIVE)
    if closure is None:
        return False, "no-completed-closure-predicate"
    if not _has_term(norm, PRODUCT_AUTHORITY):
        return False, "no-product-authority"
    for reason, terms in (
        ("negated", NEGATORS), ("pending", CLOSURE_PENDING),
        ("retracted", CLOSURE_NEGATIVE), ("hedged", MODAL),
        ("attributed", ATTRIBUTIVE), ("subordinated", SUBORDINATOR),
        ("historical", HISTORICAL),
    ):
        found = _find_term(norm, terms)
        if found is not None:
            return False, f"{reason}:{found[1]}"
    return True, closure[1]


def packet_decision_states(product: object) -> dict[str, str]:
    """The binding packet's own recorded state per decision id, read live.

    Never hardcoded: the packet is the authority, so its rows — decided and
    pending alike — are what every other artifact is measured against.
    """
    states: dict[str, str] = {}
    if not isinstance(product, dict):
        return states
    for section in ("decisions", "pendingDecisions"):
        rows = product.get(section)
        if not isinstance(rows, dict):
            continue
        for decision_id, row in rows.items():
            status = row.get("status") if isinstance(row, dict) else row
            family = _head_family(str(status))[0] if isinstance(status, str) else "UNKNOWN"
            if family == "UNKNOWN":
                family = "CLOSED_POSITIVE" if section == "decisions" else "PENDING"
            states[str(decision_id)] = family
    return states


def _disposition_value_text(value: object) -> str:
    """The recorded state carried by a decision-keyed value, in any shape."""
    if isinstance(value, str):
        return value
    if isinstance(value, bool) or value is None or isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, dict):
        parts = [
            field for key, field in value.items()
            if isinstance(field, str)
            and "".join(ch for ch in str(key).lower() if ch.isalpha()) in DISPOSITION_FIELDS
        ]
        return " ".join(parts)
    if isinstance(value, list):
        return " ".join(item for item in value if isinstance(item, str))
    return ""


def _subtree_strings(value: object, limit: int = 400) -> list[str]:
    """Every string leaf below a decision-keyed value (bounded)."""
    found: list[str] = []

    def walk(node: object) -> None:
        if len(found) >= limit:
            return
        if isinstance(node, str):
            found.append(node)
        elif isinstance(node, dict):
            for child in node.values():
                walk(child)
        elif isinstance(node, list):
            for child in node:
                walk(child)

    walk(value)
    return found


def _document_sites(doc: object, known_ids: tuple[str, ...]) -> tuple[list, list, list]:
    """Extract every product-decision assertion site from one parsed artifact.

    Returns (key_anchored, key_scoped_strings, prose) where key_anchored is the
    form in which a disposition is CONSTITUTED (a decision id used as a key) and
    prose is the recall net over free text that names a decision id.
    """
    id_alternation = re.compile(
        r"\b(?:CD-[A-Z0-9]+(?:-[A-Z0-9]+)*"
        + "".join("|" + re.escape(i) for i in known_ids) + r")\b"
    )
    key_anchored: list[tuple[str, str, object]] = []
    key_scoped: list[tuple[str, str, str]] = []
    prose: list[tuple[str, str, str]] = []

    def walk(node: object, path: str) -> None:
        if isinstance(node, dict):
            for key, value in node.items():
                key_text = str(key)
                if key_text in known_ids or DECISION_ID_RE.fullmatch(key_text):
                    location = f"{path}.{key_text}"
                    key_anchored.append((key_text, location, value))
                    if not isinstance(value, str):
                        for leaf in _subtree_strings(value):
                            key_scoped.append((key_text, location, leaf))
                walk(value, f"{path}.{key_text}")
        elif isinstance(node, list):
            for index, value in enumerate(node):
                walk(value, f"{path}[{index}]")
        elif isinstance(node, str):
            for decision_id in sorted(set(id_alternation.findall(node))):
                prose.append((decision_id, path, node))

    walk(doc, "$")
    return key_anchored, key_scoped, prose


def document_assertion_failures(states: dict[str, str], name: str, doc: object,
                                prefix: str) -> tuple[list[str], dict[str, int]]:
    """Cross-check one artifact's product-decision assertions against the packet.

    Two rules, both anchored on the decision id rather than on a field name:

      CONFLICT  the packet carries this decision and the artifact asserts a
                different disposition family than the packet records.
      UNBACKED  the artifact asserts a completed *product* closure of a decision
                the packet does not carry at all. The packet is the only place a
                product decision can be constituted; an artifact may cite one.
    """
    known = tuple(sorted(states))
    key_anchored, key_scoped, prose = _document_sites(doc, known)
    counts = {
        "keyAnchoredSites": len(key_anchored),
        "keyScopedStrings": len(key_scoped),
        "proseSites": len(prose),
        "sitesAgainstPacketRow": 0,
        "sitesAgainstUnbackedRule": 0,
        "clausesClassified": 0,
    }
    failures: list[str] = []
    seen: set[tuple[str, str]] = set()

    def record(decision_id: str, location: str, message: str) -> None:
        if (decision_id, location) in seen:
            return
        seen.add((decision_id, location))
        failures.append(message)

    for decision_id, location, value in key_anchored:
        packet_state = states.get(decision_id)
        if packet_state is not None:
            counts["sitesAgainstPacketRow"] += 1
        else:
            counts["sitesAgainstUnbackedRule"] += 1
        text = _disposition_value_text(value)
        if not text.strip():
            continue
        if POINTER_RE.search(text.strip()) or PLACEHOLDER_RE.search(text):
            continue
        units = _clause_units(text)
        counts["clausesClassified"] += len(units)
        family, term = _head_family(units[0])
        # A CLOSED_NEGATIVE head is ambiguous: "struck", "superseded" and
        # "withdrawn" are routinely editorial statements about the RECORD
        # ("this line was struck") rather than dispositional statements about
        # the decision ("product rejected it"). Only the latter is a product
        # claim, and only the latter names a product authority.
        if family == "CLOSED_NEGATIVE" and not _has_term(
                _normalise(text), PRODUCT_AUTHORITY):
            family = "UNKNOWN"
        if packet_state is not None and family != "UNKNOWN" and family != packet_state:
            record(decision_id, location, (
                f"{prefix}-CONFLICT {name}{location}: asserts {decision_id} "
                f"{family} (via {term!r}) while the binding product packet "
                f"records {packet_state}"
            ))
            continue
        if packet_state == "CLOSED_POSITIVE":
            continue
        for unit in units:
            asserted, why = asserts_completed_product_closure(unit)
            if asserted:
                record(decision_id, location, (
                    f"{prefix}-UNBACKED {name}{location}: constitutes a product "
                    f"closure of {decision_id} (via {why!r}) that the binding "
                    f"product packet does not carry"
                ))
                break

    for decision_id, location, leaf in key_scoped:
        if states.get(decision_id) == "CLOSED_POSITIVE":
            continue
        for unit in _clause_units(leaf):
            counts["clausesClassified"] += 1
            asserted, why = asserts_completed_product_closure(unit)
            if asserted:
                record(decision_id, location, (
                    f"{prefix}-UNBACKED {name}{location}: a field under "
                    f"{decision_id} constitutes a product closure (via {why!r}) "
                    f"that the binding product packet does not carry"
                ))
                break

    for decision_id, location, leaf in prose:
        if states.get(decision_id) == "CLOSED_POSITIVE":
            continue
        for unit in _clause_units(leaf):
            if decision_id not in unit:
                continue
            counts["clausesClassified"] += 1
            asserted, why = asserts_completed_product_closure(unit)
            if asserted:
                record(decision_id, f"{location}<prose>", (
                    f"{prefix}-UNBACKED {name}{location}: prose constitutes a "
                    f"product closure of {decision_id} (via {why!r}) that the "
                    f"binding product packet does not carry"
                ))
                break

    counts["conflicts"] = len(failures)
    return failures, counts


def _split_version(name: str) -> tuple[str, tuple[int, ...]] | None:
    """'retention-tiers.v5.json' -> ('retention-tiers', (5,)); None if unversioned."""
    if not name.endswith(".json"):
        return None
    match = VERSIONED_RE.match(name[: -len(".json")])
    if not match:
        return None
    return match.group("base"), tuple(int(p) for p in match.group("ver").split("."))


def _is_review_side(name: str) -> bool:
    return any(marker in name.lower() for marker in REVIEW_MARKERS)


def _harvest_strings(node: object, out: list[str], depth: int = 0) -> None:
    if depth > 6:
        return
    if isinstance(node, str):
        out.append(node)
    elif isinstance(node, dict):
        for child in node.values():
            _harvest_strings(child, out, depth + 1)
    elif isinstance(node, list):
        for child in node:
            _harvest_strings(child, out, depth + 1)


def primary_reviews_of(target: str, docs: list[tuple[str, object]]
                       ) -> list[tuple[str, dict, str]]:
    """Reviews whose PRIMARY subject is `target`, found two ways.

    Review filenames are not reliably derived from their subject —
    `evidence.v10`'s review is `evidence.v10.review-independent-prefreeze.json`
    but `evaluation-proof.v9`'s is `ep9.review-independent.json`, which a stem
    glob misses entirely. So the filename convention is used where it holds and
    every other review document is opened and asked what it reviews.

    Two false attributions this must not make, both observed live:

      * `d9-exit-contract.v1.10.review-….json` starts with `d9-exit-contract.v1.`
        and would be read as a review of `d9-exit-contract.v1.json`. The segment
        after the stem must not begin a longer version number.
      * `claim-status-integrity.repair.review-b.json` names the claim register
        in a PROSE subject listing three repaired files. Reading it as a review
        OF the register would mark the register historical and excuse exactly
        the fabrication this guard exists to catch. A structured declaration
        assigns roles (candidate vs checker) so a `.py` companion is expected;
        a prose sentence has no roles, so a second file means it describes a
        pass rather than declaring a subject.
    """
    found: list[tuple[str, dict, str]] = []
    stem = target[: -len(".json")] if target.endswith(".json") else target
    for name, data in docs:
        if name == target or not _is_review_side(name) or not isinstance(data, dict):
            continue
        if name.startswith(stem + "."):
            if not name[len(stem) + 1:][:1].isdigit():
                found.append((name, data, "filename-convention"))
            continue
        structured = False
        strings: list[str] = []
        for key in SUBJECT_KEYS:
            if key in data:
                if isinstance(data[key], (dict, list)):
                    structured = True
                _harvest_strings(data[key], strings)
        if not strings:
            continue
        claimed = " ".join(strings)
        if target not in claimed:
            continue
        named = set(FILE_REFERENCE_RE.findall(claimed))
        if structured:
            declared = {item for item in named if item.endswith(".json")} == {target}
        else:
            declared = named == {target}
        if declared:
            found.append((name, data, "declared-subject"))
    return found


def review_outcome(data: dict) -> tuple[str, str]:
    """REJECT / PASS / UNCLEAR for one review document, read as data.

    `sealRecommendation` is deliberately NEVER consulted. Nothing in this corpus
    is sealed, so essentially every PASSING review also records DO-NOT-SEAL;
    reading it as a rejection would mark every reviewed surface rejected.

    Absent an explicit verdict, severity alone is NOT read as rejection —
    findings may since have been repaired, and inferring rejection from them
    marked live binding contracts (`threat-model.v3`, `delivery.v2`) REJECTED.
    Only a review that self-declares its findings still open is read that way.
    """
    verdict = data.get("verdict")
    decision, blocking = "", None
    if isinstance(verdict, str):
        decision = verdict.upper()
    elif isinstance(verdict, dict):
        decision = str(verdict.get("decision") or "").upper()
        count = verdict.get("blockingFindingCount")
        if isinstance(count, int) and not isinstance(count, bool):
            blocking = count
    if not decision:
        decision = str(data.get("decision") or "").upper()
    if blocking is None:
        count = data.get("blockingFindingCount")
        if isinstance(count, int) and not isinstance(count, bool):
            blocking = count

    if "REJECT" in decision:
        return "REJECT", f"decision={decision!r}"
    if blocking is not None:
        if blocking > 0:
            return "REJECT", f"blockingFindingCount={blocking}"
        return "PASS", "blockingFindingCount=0"
    blockers = data.get("blockers")
    if isinstance(blockers, list) and blockers:
        return "REJECT", f"{len(blockers)} declared blocker(s)"
    if "PASS" in decision or "ACCEPT" in decision:
        return "PASS", f"decision={decision!r}"

    status = str(data.get("status") or "").upper()
    findings = data.get("findings")
    if (any(marker in status for marker in OPEN_FINDING_MARKERS)
            and isinstance(findings, list) and findings):
        severities = [str((row or {}).get("severity", "")).upper()
                      for row in findings if isinstance(row, dict)]
        blocking_rows = [s for s in severities
                         if any(level in s for level in BLOCKING_SEVERITY)]
        if blocking_rows:
            return "REJECT", (f"status={data.get('status')!r} with "
                              f"{len(blocking_rows)} blocking-severity finding(s) "
                              "and no passing verdict")
    return "UNCLEAR", "no explicit verdict"


def head_named_artifacts(root: Path = HERE) -> tuple[set[str], list[str]]:
    """Artifacts the freeze/blueprint name. Returns (names, documents_read).

    If neither document can be read the set is empty, so nothing is treated as
    superseded and every assertion keeps full standing. Unknown standing must
    produce MORE findings, never fewer.
    """
    names: set[str] = set()
    read: list[str] = []
    for doc_name in HEAD_DOC_NAMES:
        path = root.parent / doc_name
        try:
            names.update(FILE_REFERENCE_RE.findall(path.read_text()))
            read.append(doc_name)
        except (OSError, UnicodeError):
            continue
    return names, read


def artifact_standing(name: str, docs: list[tuple[str, object]],
                      heads: set[str]) -> tuple[str, str]:
    """LIVE / REJECTED / SUPERSEDED for one asserting artifact, plus the reason."""
    reasons: list[str] = []
    for review_name, data, how in primary_reviews_of(name, docs):
        outcome, why = review_outcome(data)
        if outcome == "REJECT":
            reasons.append(f"independently REJECTED by {review_name} "
                           f"({why}; matched by {how})")
            break
    version = _split_version(name)
    if version is not None and not _is_review_side(name):
        base, current = version
        later: list[tuple[tuple[int, ...], str]] = []
        for other, _ in docs:
            if other == name or _is_review_side(other) or other not in heads:
                continue
            other_version = _split_version(other)
            if other_version and other_version[0] == base and other_version[1] > current:
                later.append((other_version[1], other))
        if later:
            later.sort()
            reasons.append(
                f"superseded by {later[-1][1]}, which "
                f"{' / '.join(HEAD_DOC_NAMES)} name as head"
            )
    if not reasons:
        return "LIVE", "no rejecting review and no later head supersedes it"
    standing = "REJECTED" if reasons[0].startswith("independently") else "SUPERSEDED"
    return standing, "; ".join(reasons)


def scan_artifacts(root: Path = HERE) -> tuple[list[tuple[str, object]], list[str], int]:
    """Parse every JSON artifact under root. Returns (docs, unreadable, discovered).

    Unreadable files are NAMED and counted, never silently dropped — a coverage
    number that quietly excludes what the instrument could not open is the §7
    failure this checker exists to stop repeating.
    """
    docs: list[tuple[str, object]] = []
    unreadable: list[str] = []
    paths = sorted(p for p in root.glob("*.json") if p.is_file())
    for path in paths:
        try:
            docs.append((path.name, json.loads(path.read_text())))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            unreadable.append(f"{path.name} ({type(exc).__name__})")
    return docs, unreadable, len(paths)


def assertion_lane_failures(product: object, root: Path = HERE
                            ) -> tuple[list[str], list[str], dict[str, object]]:
    """Guard 2: every artifact that can assert a product disposition.

    Returns (failures, historical_observations, report).

    `claim-register.v1.json` is read explicitly and reported under its own PD-REG
    check id, because it is the artifact the fabrication survived in; the same
    rule then runs over every other artifact under PD-SCAN.

    A conflicting assertion fails only when the artifact making it has standing.
    An assertion in a REJECTED or SUPERSEDED artifact is a historical record: it
    is reported, with the review or head that removed its authority, and does not
    fail. Unknown standing counts as LIVE, so the fail-closed direction is more
    findings, never fewer.
    """
    docs, unreadable, discovered = scan_artifacts(root)
    heads, head_docs = head_named_artifacts(root)
    return classify_assertions(product, docs, heads, unreadable, discovered, head_docs)


def classify_assertions(product: object, docs: list[tuple[str, object]],
                        heads: set[str], unreadable: list[str], discovered: int,
                        head_docs: list[str]
                        ) -> tuple[list[str], list[str], dict[str, object]]:
    """The assertion lane over an already-loaded corpus, so it is testable."""
    states = packet_decision_states(product)
    report: dict[str, object] = {
        "artifactsDiscovered": discovered,
        "artifactsParsed": len(docs),
        "artifactsUnreadable": unreadable,
        "packetDecisionIds": len(states),
        "registerRead": False,
        "keyAnchoredSites": 0,
        "keyScopedStrings": 0,
        "proseSites": 0,
        "sitesAgainstPacketRow": 0,
        "sitesAgainstUnbackedRule": 0,
        "clausesClassified": 0,
        "conflicts": 0,
        "headDocumentsRead": head_docs,
        "headNamedArtifacts": len([n for n in heads if n.endswith(".json")]),
        "artifactsLive": 0,
        "artifactsRejected": 0,
        "artifactsSuperseded": 0,
        "conflictingArtifactsLive": 0,
        "conflictingArtifactsHistorical": 0,
        "historicalObservations": 0,
    }
    failures: list[str] = []
    observations: list[str] = []
    if not states:
        return ([
            "PD-REG: cannot read the binding packet's decision rows; "
            "no artifact assertion can be cross-checked"
        ], observations, report)

    for name, doc in docs:
        is_register = name == REGISTER_PATH.name
        if is_register:
            report["registerRead"] = True
        found, counts = document_assertion_failures(
            states, name, doc, "PD-REG" if is_register else "PD-SCAN"
        )
        for key, value in counts.items():
            if key in report and key != "conflicts":
                report[key] = int(report[key]) + value  # type: ignore[arg-type]
        standing, reason = artifact_standing(name, docs, heads)
        report[f"artifacts{standing.title()}"] = int(
            report[f"artifacts{standing.title()}"]) + 1  # type: ignore[arg-type]
        if not found:
            continue
        if standing == "LIVE":
            report["conflictingArtifactsLive"] = int(
                report["conflictingArtifactsLive"]) + 1  # type: ignore[arg-type]
            failures.extend(found)
        else:
            report["conflictingArtifactsHistorical"] = int(
                report["conflictingArtifactsHistorical"]) + 1  # type: ignore[arg-type]
            report["historicalObservations"] = int(
                report["historicalObservations"]) + len(found)  # type: ignore[arg-type]
            observations.append(f"{name} — {standing}: {reason}")
            observations.extend(f"    {item}" for item in found)

    if not report["registerRead"]:
        failures.append(
            f"PD-REG: {REGISTER_PATH.name} was not readable, so the artifact the "
            "fabricated CD-RT-5 sign-off survived in went un-cross-checked"
        )
    report["conflicts"] = len(failures)
    return failures, observations, report


def format_scan_report(report: dict[str, object]) -> list[str]:
    """MEASURED coverage. Every number is recomputed per run, none is baked in."""
    lines = [
        "assertion-lane coverage (measured this run, not declared):",
        f"  artifacts discovered      {report['artifactsDiscovered']}",
        f"  artifacts parsed+scanned  {report['artifactsParsed']}",
        f"  artifacts unreadable      {len(report['artifactsUnreadable'])}"
        + (f" -> {', '.join(report['artifactsUnreadable'])}"  # type: ignore[arg-type]
           if report["artifactsUnreadable"] else ""),
        f"  claim-register.v1.json    {'READ' if report['registerRead'] else 'NOT READ'}",
        f"  packet decision ids       {report['packetDecisionIds']}",
        f"  disposition sites found   "
        f"{int(report['keyAnchoredSites']) + int(report['keyScopedStrings']) + int(report['proseSites'])}"
        f" (key-anchored {report['keyAnchoredSites']},"
        f" key-scoped fields {report['keyScopedStrings']},"
        f" prose {report['proseSites']})",
        f"  cross-checked vs a packet row  {report['sitesAgainstPacketRow']}",
        f"  checked vs unbacked-closure rule  {report['sitesAgainstUnbackedRule']}",
        f"  clauses semantically classified   {report['clausesClassified']}",
        "  standing of asserting artifacts (discovered, not listed):",
        f"    head documents read     {len(report['headDocumentsRead'])}"
        + (f" ({', '.join(report['headDocumentsRead'])})"  # type: ignore[arg-type]
           if report["headDocumentsRead"] else " — NOTHING treated as superseded"),
        f"    artifacts named as head {report['headNamedArtifacts']}",
        f"    LIVE {report['artifactsLive']}"
        f" / REJECTED {report['artifactsRejected']}"
        f" / SUPERSEDED {report['artifactsSuperseded']}",
        f"  conflicting assertions in LIVE artifacts       {report['conflicts']}"
        " (these fail)",
        f"  conflicting assertions in historical artifacts "
        f"{report['historicalObservations']} across "
        f"{report['conflictingArtifactsHistorical']} artifact(s) (reported below)",
        "  NOT observed by this instrument: non-JSON artifacts (*.md, *.py),",
        "  anything outside this directory, unparseable bytes listed above, and",
        "  any closure assertion that names no decision id and sits under no",
        "  decision-id key. Prose is gated only when a clause names the decision,",
        "  predicates a completed closure and invokes product authority without",
        "  hedging, quoting, negating or attributing it.",
        "  A historical classification depends on a DISCOVERABLE rejecting review",
        "  or a later head named by the freeze/blueprint. An artifact rejected",
        "  only in prose, with no review document and no successor, is classified",
        "  LIVE and its assertions fail — the fail-closed direction. The converse",
        "  residual is real: a review document that declares this artifact its",
        "  subject and carries a rejecting verdict removes its standing, so a",
        "  forged review would launder a false claim into an observation.",
    ]
    return lines


def retention_binding_failures(binding: object = RETENTION_BINDING,
                               proof_binding: object = EVALUATION_PROOF_BINDING) -> list[str]:
    """Prove the product join consumes the exact EP5/RT10 successor bytes."""
    if not isinstance(binding, dict) or set(binding) != {"path", "sha256"}:
        return ["PD-RT-BINDING: retention binding must be closed path+sha256"]
    if binding != RETENTION_BINDING:
        return ["PD-RT-BINDING: checker is not bound to the exact retention-tiers.v10.json successor digest"]
    if not isinstance(proof_binding, dict) or set(proof_binding) != {"path", "sha256"}:
        return ["PD-EP-BINDING: evaluation-proof binding must be closed path+sha256"]
    if proof_binding != EVALUATION_PROOF_BINDING:
        return ["PD-EP-BINDING: checker is not bound to the exact evaluation-proof.v5.json successor digest"]
    path = HERE / binding["path"]
    proof_path = HERE / proof_binding["path"]
    try:
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        proof_digest = hashlib.sha256(proof_path.read_bytes()).hexdigest()
    except OSError as exc:
        return [f"PD-RT-BINDING: cannot read exact EP5/RT10 candidate ({type(exc).__name__})"]
    if path != RETENTION_PATH or digest != binding["sha256"]:
        return [f"PD-RT-BINDING: live retention bytes hash {digest} differ from exact v10 digest"]
    if proof_path != EVALUATION_PROOF_PATH or proof_digest != proof_binding["sha256"]:
        return [f"PD-EP-BINDING: live evaluation-proof bytes hash {proof_digest} differ from exact v5 digest"]
    try:
        candidate = load(path)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return [f"PD-RT-BINDING: cannot parse exact retention candidate ({type(exc).__name__})"]
    source = ((candidate.get("capabilityClosure") or {}).get("source") or {})
    if source.get("artifact") != proof_binding["path"] or source.get("sha256") != proof_binding["sha256"]:
        return ["PD-EP-BINDING: RT10 does not transitively bind the exact EP5 artifact and digest"]
    return []


def self_signing_retention_fixture() -> dict:
    """Known-bad architecture candidate used only by the PD-RT regression.

    Keep this fixture independent of the live Phase-1A candidate: once the live
    candidate correctly stops self-signing, it is the positive input and can no
    longer double as the mutation this checker must reject.
    """
    return {
        "decision": {
            "custodyPolicy": {
                "defaultPosture": {
                    "status": "PRODUCT-SIGNED-OFF",
                    "signOff": "CD-RT-5 accepted by the architecture candidate",
                }
            }
        },
        "resolves": {"CD-RT-5": "SIGNED OFF by candidate"},
    }


def _retention_candidate_failures(retention_candidate: object) -> list[str]:
    """Reject retention candidates that manufacture product/integration authority."""
    if not isinstance(retention_candidate, dict) or not retention_candidate:
        return ["PD-RT: retention candidate root must be a non-empty object"]

    failures: list[str] = []

    if (retention_candidate.get("artifact") == "opensip.retention-custody"
            or retention_candidate.get("version") == 10):
        if retention_candidate.get("artifact") != "opensip.retention-custody" or retention_candidate.get("version") != 10:
            failures.append("PD-RT: live retention candidate identity/version is not exact v10")
        if set(retention_candidate) != RETENTION_V10_TOP_KEYS:
            failures.append("PD-RT: retention v10 top-level binding is not recursively closed")
        if retention_candidate.get("status") != "CANDIDATE-AWAITING-INDEPENDENT-COMBINED-REREVIEW-AND-PRODUCT-DISPOSITION":
            failures.append("PD-RT: retention v10 must remain awaiting independent combined rereview and product disposition")
        source = ((retention_candidate.get("capabilityClosure") or {}).get("source") or {})
        if (not isinstance(source, dict)
                or source.get("artifact") != EVALUATION_PROOF_BINDING["path"]
                or source.get("sha256") != EVALUATION_PROOF_BINDING["sha256"]):
            failures.append("PD-RT: retention v10 does not bind the exact evaluation-proof v5 successor")
        authority = retention_candidate.get("authority") or {}
        if (not isinstance(authority, dict)
                or authority.get("candidateState") != "NOT-APPLIED"
                or authority.get("mayRecordProductAcceptance") is not False):
            failures.append("PD-RT: retention v10 authoring authority must remain NOT-APPLIED and unable to record product acceptance")

    forbidden_keys = {
        "resolves", "productdecision", "productacceptance", "signoff", "signedoff",
        "approval", "acceptedby",
    }
    positive_values = {
        "RESOLVED", "COMPLETE", "COMPLETED", "ACCEPTED", "SIGNED", "SIGNEDOFF",
        "PRODUCTSIGNEDOFF", "APPROVED", "SEALED",
    }

    def walk(node: object, path: str) -> None:
        if isinstance(node, dict):
            for key, child in node.items():
                normalized_key = "".join(ch for ch in str(key).lower() if ch.isalpha())
                if normalized_key in forbidden_keys:
                    failures.append(f"PD-RT: forbidden product/integration authority alias at {path}.{key}")
                if isinstance(child, str) and normalized_key in {
                    "status", "state", "currentstate", "disposition", "verdict", "outcome",
                }:
                    normalized_value = "".join(ch for ch in child.upper() if ch.isalpha())
                    if normalized_value in positive_values:
                        failures.append(f"PD-RT: forbidden positive authority value at {path}.{key}")
                walk(child, path + "." + str(key))
        elif isinstance(node, list):
            for index, child in enumerate(node):
                walk(child, f"{path}[{index}]")

    walk(retention_candidate, "$retention")

    # Historical v5 self-sign shape retained as a regression.
    decision = retention_candidate.get("decision")
    if decision is not None and not isinstance(decision, dict):
        failures.append("PD-RT: retention decision must be an object when present")
        decision = {}
    custody_decision = (decision or {}).get("custodyPolicy")
    if custody_decision is not None and not isinstance(custody_decision, dict):
        failures.append("PD-RT: retention decision.custodyPolicy must be an object")
        custody_decision = {}
    posture = (custody_decision or {}).get("defaultPosture")
    if posture is not None and not isinstance(posture, dict):
        failures.append("PD-RT: retention defaultPosture must be an object")
        posture = {}

    resolves = retention_candidate.get("resolves")
    if resolves is not None and not isinstance(resolves, dict):
        failures.append("PD-RT: retention resolves must be an object when present")
        resolves = {}
    retained_resolution = (resolves or {}).get("CD-RT-5", "")
    if (
        "SIGNED" in str((posture or {}).get("status", "")).upper()
        or "accepted" in str((posture or {}).get("signOff", "")).lower()
        or "SIGNED OFF" in str(retained_resolution).upper()
    ):
        failures.append(
            "PD-RT: retention candidate self-asserts CD-RT-5 product sign-off "
            "while the product authority still marks it BLOCKED_ON_PHASE_1A"
        )

    # Current successor integration shape: no candidate may resolve V10/Phase 1A or
    # add an alternate resolution object before independent/product authority.
    integration = retention_candidate.get("integrationState")
    if integration is not None and not isinstance(integration, dict):
        failures.append("PD-RT: retention integrationState must be an object")
        integration = {}
    if isinstance(integration, dict):
        if integration.get("candidateState") != "NOT-APPLIED" or integration.get("externalClosureClaim") != "NONE":
            failures.append("PD-RT: retention successor must remain NOT-APPLIED with no external closure claim")
        pending = integration.get("pending")
        if pending is not None and not isinstance(pending, list):
            failures.append("PD-RT: retention integrationState.pending must be an array")
            pending = []
        for row in pending or []:
            if not isinstance(row, dict):
                failures.append("PD-RT: retention pending integration row must be an object")
                continue
            target = row.get("target")
            state = row.get("currentState")
            if target == "threat-model.v3.json#V10" and state == "RESOLVED":
                failures.append(
                    "PD-RT: retention candidate prematurely resolves V10 before "
                    "independent review and product disposition"
                )
            if target == "product-dispositions.v1.json#CD-RT-5" and state != "BLOCKED_ON_PHASE_1A":
                failures.append("PD-RT: retention candidate changes product-owned CD-RT-5 blocked state")
        if "resolves" in integration:
            failures.append(
                "PD-RT: retention candidate adds a forbidden nested integrationState.resolves "
                "authority path"
            )

    custody = retention_candidate.get("custodyPolicy")
    if custody is not None and not isinstance(custody, dict):
        failures.append("PD-RT: retention custodyPolicy must be an object")
        custody = {}
    if isinstance(custody, dict) and "productAcceptance" in custody:
        acceptance = custody.get("productAcceptance")
        if not isinstance(acceptance, dict):
            failures.append("PD-RT: custodyPolicy.productAcceptance must be an object")
        else:
            failures.append(
                "PD-RT: retention candidate records productAcceptance while CD-RT-5 "
                "remains product-owned and BLOCKED_ON_PHASE_1A"
            )
    return failures


def _validate(product: dict, ri: dict, versioning: dict, delivery: dict,
              retention_candidate: dict | None = None) -> list[str]:
    failures: list[str] = []

    if product.get("artifact") != "opensip.product-dispositions" or product.get("version") != 1:
        failures.append("PD-0: wrong artifact identity/version")

    decisions = product.get("decisions")
    if not isinstance(decisions, dict):
        return failures + ["PD-1: decisions must be an object"]

    if set(decisions) != set(EXPECTED_CHOICES):
        failures.append(
            "PD-1: decision set differs from the required non-retention Phase-2 set"
        )
    for decision_id, expected in EXPECTED_CHOICES.items():
        row = decisions.get(decision_id) or {}
        if row.get("status") not in {"DECIDED", "CONFIRMED"}:
            failures.append(f"PD-1 {decision_id}: status is not DECIDED/CONFIRMED")
        if row.get("choice") != expected:
            failures.append(
                f"PD-1 {decision_id}: choice {row.get('choice')!r} != {expected!r}"
            )

    pending = product.get("pendingDecisions") or {}
    if set(pending) != {"CD-RT-5"}:
        failures.append("PD-5: CD-RT-5 must be the sole pending Phase-2 decision")
    retention_row = pending.get("CD-RT-5") or {}
    if retention_row.get("status") != "BLOCKED_ON_PHASE_1A":
        failures.append("PD-5: CD-RT-5 is not visibly blocked on Phase 1A")
    if "No implementer may choose" not in retention_row.get("ruleWhilePending", ""):
        failures.append("PD-5: pending retention permits implementer invention")

    # An architecture candidate cannot manufacture the product disposition that
    # this authority artifact still marks pending. This join is optional only
    # while no Phase-1A candidate exists.
    if retention_candidate is not None:
        failures.extend(_retention_candidate_failures(retention_candidate))

    # A1-RI-04 must select one branch the live resolved-inputs contract permits.
    posture = ((ri.get("configuration") or {}).get("untrackedOverridePosture") or {})
    binding = posture.get("bindingProductDecision") or {}
    binding_rule = binding.get("rule", "").lower()
    layer4_rule = (decisions.get("A1-RI-04") or {}).get("rule", "").lower()
    if posture.get("status") != "PRODUCT_DECIDED" or \
            posture.get("productDecisionStillOpen") is not False:
        failures.append("PD-RI: live resolved-inputs layer-4 posture is not product-decided")
    if binding.get("id") != "A1-RI-04" or \
            binding.get("source") != \
            "artifacts/product-dispositions.v1.json#decisions.A1-RI-04" or \
            binding.get("choice") != "CI_IGNORES_LAYER_4":
        failures.append("PD-RI: live resolved-inputs binding does not join the product authority")
    if "does not load or resolve layer 4" not in binding_rule:
        failures.append("PD-RI: live resolved-inputs does not bind CI to ignore layer 4")
    if "does not fail because the file exists" not in binding_rule:
        failures.append("PD-RI: live resolved-inputs still permits layer-4 presence to hard-fail CI")
    if "does not load or resolve layer-4" not in layer4_rule:
        failures.append("PD-RI: product choice does not unambiguously select ignore-layer-4")
    if "presence is not an admission failure" not in layer4_rule:
        failures.append("PD-RI: product choice still permits the hard-fail branch")

    # The pivot choice must remain the live conservative default, never a cost claim.
    pivot = versioning.get("detectorSemanticDelta") or {}
    ship_gate = pivot.get("shipGate") or {}
    live_default = ship_gate.get("defaultUntilDisposition", "").lower()
    chosen_pivot = decisions.get("VER-PIVOT-COST") or {}
    chosen_rule = chosen_pivot.get("rule", "").lower()
    if "detector major changes" not in live_default or "explicitly requested" not in live_default:
        failures.append("PD-VER: selected pivot posture is absent from live VERSIONING")
    if "ordinary analysis never invokes" not in chosen_rule:
        failures.append("PD-VER: choice does not keep pivot off ordinary analysis")
    if chosen_pivot.get("evidencePosture") != "Affordability remains UNMEASURED; no cheap/free claim is authorized.":
        failures.append("PD-VER: product disposition overclaims pivot affordability")

    # G3 confirms, rather than silently changing, DELIVERY v2.
    substrate = delivery.get("rustSemanticSubstrate") or {}
    if substrate.get("decision") != "bundled-pinned-rustc-driver-sidecar":
        failures.append("PD-G3: live DELIVERY no longer binds the pinned rustc_driver sidecar")
    platforms = ((delivery.get("platformMatrix") or {}).get("supported") or [])
    if len(platforms) != 5:
        failures.append("PD-G3: live DELIVERY supported-platform set is not the accepted five-row set")
    profiles = delivery.get("installProfiles") or {}
    if profiles.get("defaultProfile") != "full":
        failures.append("PD-G3: live DELIVERY default profile is not full")

    # Guessed windows stay visibly provisional and cannot become release evidence.
    support = versioning.get("supportWindows") or {}
    if "provisional" not in support.get("consumerFacingRule", "").lower():
        failures.append("PD-WINDOW: live VERSIONING does not require a provisional label")
    support_row = decisions.get("SUPPORT-WINDOWS") or {}
    if "NOT DISCHARGED" not in support_row.get("evidencePosture", ""):
        failures.append("PD-WINDOW: guessed support windows were paper-discharged")

    return failures


def validate(product: object, ri: dict, versioning: dict, delivery: dict,
             retention_candidate: dict | None = None) -> list[str]:
    """Total product-authority boundary for malformed parsed JSON."""
    if not isinstance(product, dict) or not product:
        return ["PD-TOTALITY-ROOT: product root must be a non-empty object"]
    if not isinstance(product.get("decisions"), dict):
        return ["PD-TOTALITY-SHAPE: decisions must be an object"]
    try:
        return _validate(product, ri, versioning, delivery, retention_candidate)
    except MALFORMED_SHAPE_EXCEPTIONS as exc:
        return [f"PD-TOTALITY-EXCEPTION: malformed contract shape "
                f"({type(exc).__name__})"]


def _retention_v10_resolved(candidate: dict) -> None:
    pending = candidate["integrationState"]["pending"]
    row = next(item for item in pending
               if item.get("target") == "threat-model.v3.json#V10")
    row["currentState"] = "RESOLVED"


def _retention_nested_resolves(candidate: dict) -> None:
    candidate["integrationState"]["resolves"] = {
        "V10": "RESOLVED",
        "Phase1A": "COMPLETE",
    }


def _retention_product_acceptance(candidate: dict) -> None:
    candidate["custodyPolicy"]["productAcceptance"] = {
        "status": "ACCEPTED",
        "decisionId": "CD-RT-5",
        "by": "architecture-candidate",
    }


def _retention_hidden_product_decision(candidate: dict) -> None:
    candidate["repairs"] = [{
        "productDecision": {
            "decisionId": "CD-RT-5",
            "outcome": "APPROVED",
            "by": "architecture-candidate",
        }
    }]


def _retention_nested_assurance_signoff(candidate: dict) -> None:
    candidate["assurance"]["reviewMetadata"] = {
        "signOff": "architecture candidate accepted CD-RT-5",
    }


def _retention_nested_lease_approval(candidate: dict) -> None:
    candidate["leaseProtocol"]["reviewMetadata"] = {
        "approval": {"status": "APPROVED"},
    }


def _retention_nested_storage_accepted_by(candidate: dict) -> None:
    candidate["storageAndLineage"]["reviewMetadata"] = {
        "acceptedBy": "architecture-candidate",
    }


def _retention_nested_d9_outcome(candidate: dict) -> None:
    candidate["d9Derivation"]["reviewMetadata"] = {"outcome": "APPROVED"}


def _retention_nested_residual_state(candidate: dict) -> None:
    candidate["retainedResiduals"][0]["reviewMetadata"] = {"state": "SEALED"}


def _retention_nested_closure_verdict(candidate: dict) -> None:
    candidate["capabilityClosure"]["source"]["reviewMetadata"] = {
        "verdict": "ACCEPTED",
    }


RETENTION_AUTHORITY_MUTATIONS = (
    ("set integrationState V10 currentState=RESOLVED (RT10 authority regression)",
     _retention_v10_resolved),
    ("add integrationState.resolves authority alias (RT10 authority regression)",
     _retention_nested_resolves),
    ("self-sign custodyPolicy.productAcceptance=ACCEPTED (RT10 authority regression)",
     _retention_product_acceptance),
    ("hide repairs[0].productDecision outcome=APPROVED (recursive authority regression)",
     _retention_hidden_product_decision),
    ("hide assurance.reviewMetadata.signOff", _retention_nested_assurance_signoff),
    ("hide leaseProtocol.reviewMetadata.approval", _retention_nested_lease_approval),
    ("hide storageAndLineage.reviewMetadata.acceptedBy", _retention_nested_storage_accepted_by),
    ("hide d9Derivation.reviewMetadata outcome=APPROVED", _retention_nested_d9_outcome),
    ("hide retainedResiduals reviewMetadata state=SEALED", _retention_nested_residual_state),
    ("hide capabilityClosure.source reviewMetadata verdict=ACCEPTED", _retention_nested_closure_verdict),
)


# ---------------------------------------------------------------------------
# Assertion-lane regressions.
#
# Each mutation writes a product-decision assertion into an in-memory copy of a
# real artifact and must be caught by its own named check. The FABRICATION row
# reproduces the exact string that survived three days in claim-register.v1.json;
# the rows after it reword it, restructure it and relocate it, so a checker that
# passed by grepping for the literal would fail here.
# ---------------------------------------------------------------------------

FABRICATED_REGISTER_STRING = (
    "SIGNED OFF 2026-07-31 by product owner — zero implicit durable retention "
    "for greenfield."
)


def _register_disposition_map(register: dict) -> dict | None:
    """The live disposition map that carried the fabrication, located by shape."""
    for claim in register.get("claims") or []:
        if isinstance(claim, dict) and isinstance(claim.get("disposition"), dict):
            if any(DECISION_ID_RE.fullmatch(str(k)) for k in claim["disposition"]):
                return claim["disposition"]
    return None


def _register_fabricated_verbatim(register: dict) -> None:
    _register_disposition_map(register)["CD-RT-5"] = FABRICATED_REGISTER_STRING


def _register_fabricated_reworded(register: dict) -> None:
    _register_disposition_map(register)["CD-RT-5"] = (
        "Ratified 2026-08-02 by the product owner; the durable-retention default "
        "is settled for greenfield."
    )


def _register_fabricated_structured(register: dict) -> None:
    _register_disposition_map(register)["CD-RT-5"] = {
        "decidedBy": "product owner",
        "decision": "Zero implicit durable retention, accepted for greenfield.",
        "rationale": "Recorded in the register in the genuine structured form.",
    }


def _register_fabricated_relocated(register: dict) -> None:
    for claim in register.get("claims") or []:
        if isinstance(claim, dict) and isinstance(claim.get("disposition"), dict):
            claim["reviewNote"] = (
                "The product owner accepted CD-RT-5 on 2026-08-02 and the "
                "retention default is now product-accepted."
            )
            return


def _register_fabricated_alias_key(register: dict) -> None:
    _register_disposition_map(register)["CD-RT-5"] = {
        "productAcceptance": "Granted by the product owner for greenfield.",
    }


REGISTER_FABRICATION_MUTATIONS = (
    ("register re-asserts the verbatim 2026-07-31 CD-RT-5 sign-off",
     _register_fabricated_verbatim),
    ("register re-asserts the same sign-off REWORDED (no literal 'SIGNED OFF')",
     _register_fabricated_reworded),
    ("register re-asserts it in the STRUCTURED {decidedBy, decision} form",
     _register_fabricated_structured),
    ("register re-asserts it as PROSE in a sibling claim field",
     _register_fabricated_relocated),
    ("register re-asserts it under a renamed productAcceptance key",
     _register_fabricated_alias_key),
)


def _synthetic_unbacked_cd_id() -> dict:
    return {"artifact": "synthetic", "dispositions": {
        "CD-RT-9": "SIGNED OFF by product owner — direction accepted."}}


def _synthetic_contradicts_decided_row() -> dict:
    return {"artifact": "synthetic", "dispositions": {
        "A1-RI-04": "BLOCKED pending a product review that has not happened."}}


def _synthetic_prose_closure() -> dict:
    return {"artifact": "synthetic", "notes": [
        "Confirmed with the product owner: CD-RT-5 is discharged."]}


SYNTHETIC_ASSERTION_MUTATIONS = (
    ("foreign artifact signs off a CD id the packet does not carry",
     _synthetic_unbacked_cd_id),
    ("foreign artifact contradicts a DECIDED packet row",
     _synthetic_contradicts_decided_row),
    ("foreign artifact closes CD-RT-5 in free prose",
     _synthetic_prose_closure),
)

# Negative controls. A guard that rejects everything is not a guard; these are
# real live values (and the corrected register text) that MUST survive, and they
# are what stops the assertion lane being tightened into a blanket refusal.
ASSERTION_NEGATIVE_CONTROLS = (
    ("packet-agreeing pending state",
     {"d": {"CD-RT-5": "BLOCKED_ON_PHASE_1A"}}),
    ("architecture-review verdict on a non-packet CD id",
     {"d": {"CD-RT-3": "ACCEPT direction sealedTier immutable + availability projection"}}),
    ("review recording a negated acceptance",
     {"d": {"CD-RT-5": "UNCHANGED / NOT ACCEPTED BY THIS REVIEW"}}),
    ("live decided row restated by a consumer",
     {"d": {"A1-RI-04": "RESOLVED BY PRODUCT — CI does not load or resolve layer 4."}}),
    ("template/citation pointing at the product authority",
     {"d": {"CD-RT-5": "artifacts/product-dispositions.v1.json#<PRODUCT_AUTHORITY_CD_RT_5_DECISION>"}}),
    ("quoted-and-retracted fabrication (the corrected register shape)",
     {"d": {"CD-RT-5": "BLOCKED_ON_PHASE_1A. This field previously asserted "
                       "'SIGNED OFF 2026-07-31 by product owner'. No such "
                       "sign-off occurred."}}),
    # The product owner is striking the register line concurrently, and may do
    # it in any of these shapes. None of them is a product-decision assertion,
    # so none of them may trip the guard.
    ("editorial strike marker on the register line",
     {"d": {"CD-RT-5": "[STRUCK 2026-08-03 — fabricated; see freeze §4.4]"}}),
    ("decision key removed entirely", {"d": {}}),
    ("decision key emptied", {"d": {"CD-RT-5": ""}}),
    ("decision key nulled", {"d": {"CD-RT-5": None}}),
    ("register defers to the packet in structured form",
     {"d": {"CD-RT-5": {"status": "BLOCKED_ON_PHASE_1A",
                        "decidedBy": "product owner (see the binding packet)"}}}),
)

# Assertions that must still be REJECTED however they are spelled. These exist
# so that tightening the negative controls above can never quietly re-open the
# hole: a rename, a case change, an underscore or a synonym must all fail.
ASSERTION_EVASION_CASES = (
    ("verbatim historical string", FABRICATED_REGISTER_STRING),
    ("case + underscore obfuscation", "signed_off  2026-07-31  BY  PRODUCT  OWNER"),
    ("synonym: ratified", "Ratified by the product owner on 2026-08-02."),
    ("synonym: acceptance granted", "Product acceptance granted; default fixed."),
    ("synonym: discharged", "Discharged by product decision 2026-08-02."),
    ("synonym: authorised", "Authorised by the product authority."),
    ("leading imperative verdict", "ACCEPT — the product owner agrees."),
    ("product rejection the packet does not carry",
     "REJECTED outright by the product owner 2026-08-02."),
)


def assertion_lane_selftest(product: dict, register: object) -> int:
    """Every assertion-lane mutation must be rejected; every control must pass."""
    states = packet_decision_states(product)
    if "CD-RT-5" not in states or states["CD-RT-5"] == "CLOSED_POSITIVE":
        print("REFUSING to self-test: packet no longer holds CD-RT-5 pending")
        return EXIT_REFUSED
    if not isinstance(register, dict) or _register_disposition_map(register) is None:
        print("REFUSING to self-test: claim-register disposition map is unreadable")
        return EXIT_REFUSED

    live, _ = document_assertion_failures(
        states, REGISTER_PATH.name, register, "PD-REG")
    if live:
        print("REFUSING to self-test: live claim register already conflicts with "
              "the packet, so the fabrication regression cannot be isolated")
        print("  - " + live[0])
        return EXIT_REFUSED
    print("  reject  (baseline) live claim register agrees with the product packet")

    for label, mutation in REGISTER_FABRICATION_MUTATIONS:
        mutated = copy.deepcopy(register)
        mutation(mutated)
        if mutated == register:
            print(f"  NON-APPLYING (BUG)  {label}")
            return EXIT_FINDINGS
        found, _ = document_assertion_failures(
            states, REGISTER_PATH.name, mutated, "PD-REG")
        if not found:
            print(f"  ACCEPTED (BUG)  {label}")
            return EXIT_FINDINGS
        print(f"  reject  {label}")
        print("          " + found[0])

    for label, builder in SYNTHETIC_ASSERTION_MUTATIONS:
        found, _ = document_assertion_failures(
            states, "synthetic.json", builder(), "PD-SCAN")
        if not found:
            print(f"  ACCEPTED (BUG)  {label}")
            return EXIT_FINDINGS
        print(f"  reject  {label}")
        print("          " + found[0])

    for label, spelling in ASSERTION_EVASION_CASES:
        doc = {"dispositions": {"CD-RT-5": spelling}}
        found, _ = document_assertion_failures(states, "evasion.json", doc, "PD-SCAN")
        if not found:
            print(f"  ESCAPED (BUG)  evasion by {label}")
            return EXIT_FINDINGS
        print(f"  reject  evasion by {label}")

    for label, doc in ASSERTION_NEGATIVE_CONTROLS:
        found, _ = document_assertion_failures(states, "control.json", doc, "PD-SCAN")
        if found:
            print(f"  REJECTED (BUG — false positive)  {label}")
            print("          " + found[0])
            return EXIT_FINDINGS
        print(f"  accept  (control) {label}")
    return standing_selftest(product, register)


# ---------------------------------------------------------------------------
# Standing regressions.
#
# Two behaviours must hold together and are the reason the guard is usable:
# a conflicting assertion in an artifact WITH standing fails, and the same
# assertion in an artifact WITHOUT standing is an observation. Either one alone
# is a broken guard — the first alone is permanently red on bytes freeze §7.2
# forbids repairing, the second alone excuses the fabrication.
# ---------------------------------------------------------------------------

STANDING_CHECKS: list[int] = []


def _rejecting_review(subject: str) -> dict:
    return {"artifact": "opensip.synthetic.review", "subject": subject,
            "verdict": {"decision": "REJECT", "blockingFindingCount": 2}}


def _do_not_seal_only_review(subject: str) -> dict:
    """A PASSING review. Nothing here is sealed, so it still says DO-NOT-SEAL."""
    return {"artifact": "opensip.synthetic.review", "subject": subject,
            "verdict": {"decision": "PASS", "blockingFindingCount": 0},
            "sealRecommendation": {"verdict": "DO-NOT-SEAL",
                                   "reason": "nothing in this corpus is sealed"}}


def _prose_multi_subject_review(subject_files: str) -> dict:
    return {"artifact": "opensip.synthetic.repair.review",
            "subject": f"turn-3 repairs to {subject_files}",
            "verdict": "reject-require-v2"}


def standing_selftest(product: dict, register: object) -> int:
    """Standing must be discovered correctly, and must gate the right way."""
    states = packet_decision_states(product)
    fabricated = copy.deepcopy(register)
    _register_fabricated_verbatim(fabricated)
    reg = REGISTER_PATH.name

    def run(docs, heads):
        return classify_assertions(product, docs, heads, [], len(docs), ["synthetic"])

    checks: list[tuple[str, bool, str]] = []

    # 1. Standing discovery, each rule in isolation.
    base_docs = [("thing.v1.json", {}), ("thing.v2.json", {})]
    standing, why = artifact_standing("thing.v1.json", base_docs, {"thing.v2.json"})
    checks.append(("later head named by the documents supersedes",
                   standing == "SUPERSEDED", why))
    standing, why = artifact_standing("thing.v1.json", base_docs, set())
    checks.append(("later version NOT named as head does not supersede",
                   standing == "LIVE", why))
    docs = [("thing.v1.json", {}),
            ("thing.v1.review-independent.json", _rejecting_review("thing.v1.json"))]
    standing, why = artifact_standing("thing.v1.json", docs, set())
    checks.append(("rejecting review removes standing", standing == "REJECTED", why))
    docs = [("thing.v1.json", {}),
            ("thing.v1.review-independent.json", _do_not_seal_only_review("thing.v1.json"))]
    standing, why = artifact_standing("thing.v1.json", docs, set())
    checks.append(("DO-NOT-SEAL on a PASSING review is NOT a rejection",
                   standing == "LIVE", why))
    docs = [("thing.v1.json", {}),
            ("pass.repair.review-b.json",
             _prose_multi_subject_review("checker.py, thing.v1.json, and notes"))]
    standing, why = artifact_standing("thing.v1.json", docs, set())
    checks.append(("prose subject naming several files is not a review OF one",
                   standing == "LIVE", why))
    docs = [("thing.v1.json", {}),
            ("thing.v1.10.review-independent.json", _rejecting_review("thing.v1.10.json"))]
    standing, why = artifact_standing("thing.v1.json", docs, set())
    checks.append(("a longer version's review is not this artifact's review",
                   standing == "LIVE", why))
    docs = [("ep.v9.json", {}),
            ("shortname.review-independent.json",
             {"artifact": "opensip.review",
              "subject": {"candidate": {"file": "ep.v9.json"},
                          "checker": {"file": "check-ep-v9.py"}},
              "verdict": "REJECT"})]
    standing, why = artifact_standing("ep.v9.json", docs, set())
    checks.append(("review not named after its subject is still found",
                   standing == "REJECTED", why))

    # 2. The gate itself, end to end, both directions.
    live_docs = [(reg, fabricated), ("product-dispositions.v1.json", product)]
    failures, observations, _ = run(live_docs, set())
    checks.append(("fabrication in an artifact WITH standing FAILS",
                   bool(failures) and not observations,
                   failures[0] if failures else "no failure produced"))

    superseded_docs = live_docs + [("claim-register.v2.json", {})]
    failures, observations, _ = run(superseded_docs, {"claim-register.v2.json"})
    checks.append(("same fabrication in a SUPERSEDED artifact is an observation",
                   not failures and bool(observations),
                   observations[0] if observations else "no observation produced"))

    rejected_docs = live_docs + [
        (reg[: -len(".json")] + ".review-independent.json", _rejecting_review(reg))]
    failures, observations, _ = run(rejected_docs, set())
    checks.append(("same fabrication in a REJECTED artifact is an observation",
                   not failures and bool(observations),
                   observations[0] if observations else "no observation produced"))

    failures, observations, _ = run([(reg, register)], set())
    checks.append(("the live corrected register produces neither",
                   not failures and not observations, "clean"))

    for label, ok, detail in checks:
        if not ok:
            print(f"  WRONG STANDING (BUG)  {label}")
            print(f"          {detail}")
            return EXIT_FINDINGS
        print(f"  standing  {label}")
        print(f"            {detail}")
    STANDING_CHECKS.append(len(checks))
    return EXIT_OK


def mutation_selftest(base: dict, ri: dict, versioning: dict, delivery: dict,
                      retention: dict | None, register: object = None) -> int:
    binding_failures = retention_binding_failures()
    if binding_failures:
        print("REFUSING to self-test: exact EP5/RT10 successor binding is dirty")
        print("  - " + binding_failures[0])
        return EXIT_REFUSED
    base_failures = validate(base, ri, versioning, delivery, None)
    if base_failures:
        print(
            "REFUSING to self-test: non-retention base has "
            f"{len(base_failures)} finding(s)"
        )
        for failure in base_failures:
            print(f"  - {failure}")
        return EXIT_REFUSED

    mutations = []
    non_applying: list[str] = []

    def mutate(label, fn):
        candidate = copy.deepcopy(base)
        fn(candidate)
        if candidate == base:
            non_applying.append(label)
        mutations.append((label, candidate))

    mutate("reopen P-1 as a menu", lambda c: c["decisions"]["P-1"].update(choice="MAYBE"))
    mutate("let CI hard-fail on layer-4 presence", lambda c: c["decisions"]["A1-RI-04"].update(
        rule="CI fails admission whenever layer 4 is present."
    ))
    mutate("run pivot on ordinary analysis", lambda c: c["decisions"]["VER-PIVOT-COST"].update(
        rule="Run the pivot on every ordinary analysis."
    ))
    mutate("claim pivot affordability", lambda c: c["decisions"]["VER-PIVOT-COST"].update(
        evidencePosture="Affordability is DEMONSTRATED."
    ))
    mutate("freeze the public rule IR", lambda c: c["decisions"]["PUBLIC-RULE-IR"].update(
        choice="FREEZE_PUBLIC_IR"
    ))
    mutate("paper-discharge guessed windows", lambda c: c["decisions"]["SUPPORT-WINDOWS"].update(
        evidencePosture="DISCHARGED"
    ))
    mutate("silently decide retention", lambda c: c["pendingDecisions"]["CD-RT-5"].update(
        status="DECIDED"
    ))
    if non_applying:
        print("REFUSING to self-test: product mutation did not apply")
        print("  - " + non_applying[0])
        return EXIT_REFUSED

    missed = 0
    print("mutation self-test — each row must be REJECTED")
    for label, root in TOTALITY_ROOT_CASES:
        failures = validate(copy.deepcopy(root), ri, versioning, delivery, None)
        if failures:
            print(f"  reject  parsed-JSON root {label}\n          {failures[0]}")
        else:
            missed += 1
            print(f"  ACCEPTED (BUG)  parsed-JSON root {label}")
    for label, value in TOTALITY_NESTED_CASES:
        candidate = copy.deepcopy(base)
        candidate["decisions"] = copy.deepcopy(value)
        failures = validate(candidate, ri, versioning, delivery, None)
        if failures:
            print(f"  reject  decisions nested {label}\n          {failures[0]}")
        else:
            missed += 1
            print(f"  ACCEPTED (BUG)  decisions nested {label}")
    for label, candidate in mutations:
        # Product-choice mutations are isolated from any live in-flight Phase-1A
        # contradiction, which is exercised separately below.
        failures = validate(candidate, ri, versioning, delivery, None)
        if failures:
            print(f"  reject  {label}\n          {failures[0]}")
        else:
            missed += 1
            print(f"  ACCEPTED (BUG)  {label}")
    if missed:
        total = len(mutations) + len(TOTALITY_ROOT_CASES) + len(TOTALITY_NESTED_CASES)
        print(f"self-test FAILED — {missed}/{total} retained cases escaped")
        return 1
    if retention is not None:
        live_failures = validate(base, ri, versioning, delivery, retention)
        live_retention_failures = [item for item in live_failures if item.startswith("PD-RT:")]
        if live_retention_failures:
            print("REFUSING to self-test: live retention candidate self-signs CD-RT-5")
            print("  - " + live_retention_failures[0])
            return EXIT_REFUSED
    else:
        print("REFUSING to self-test: live retention candidate is unavailable")
        return EXIT_REFUSED

    stale_bindings = [
        {"path": "retention-tiers.v9.json", "sha256": "4391c98c31a626a07573952d24a94755aedc0553d2d51f43a73e28948a6cb753"},
        {"path": "retention-tiers.v8.json", "sha256": "7a754b0eac75f5335c9a48646f19825f3b3ffaad44c8a7daf99360253dacb989"},
    ]
    for stale_binding in stale_bindings:
        stale_failures = retention_binding_failures(stale_binding)
        if not stale_failures:
            print(f"  ACCEPTED (BUG)  stale {stale_binding['path']} checker binding")
            return 1
        print(f"  reject  stale {stale_binding['path']} checker binding")
        print("          " + stale_failures[0])
    stale_proof_bindings = [
        {"path": "evaluation-proof.v4.json", "sha256": "f854a6e5731b0f2c32fedb617279379c39051074f3cd051c14eadc61109b9de1"},
        {"path": "evaluation-proof.v3.json", "sha256": "b1f10c9b7bd88d5e794c428d176084e497ba0ffbd8234b3b8c712ea532d8a40e"},
    ]
    for stale_proof_binding in stale_proof_bindings:
        stale_proof_failures = retention_binding_failures(RETENTION_BINDING, stale_proof_binding)
        if not stale_proof_failures:
            print(f"  ACCEPTED (BUG)  stale {stale_proof_binding['path']} checker binding")
            return 1
        print(f"  reject  stale {stale_proof_binding['path']} checker binding")
        print("          " + stale_proof_failures[0])

    retention_failures = validate(
        base, ri, versioning, delivery, self_signing_retention_fixture()
    )
    if not any(item.startswith("PD-RT:") for item in retention_failures):
        print("  ACCEPTED (BUG)  architecture candidate self-signs CD-RT-5")
        return 1
    print("  reject  architecture candidate self-signs CD-RT-5")
    print("          " + next(item for item in retention_failures if item.startswith("PD-RT:")))
    for label, mutation in RETENTION_AUTHORITY_MUTATIONS:
        candidate = copy.deepcopy(retention)
        mutation(candidate)
        if candidate == retention:
            print(f"  NON-APPLYING (BUG)  {label}")
            return 1
        failures = validate(base, ri, versioning, delivery, candidate)
        retained = [item for item in failures if item.startswith("PD-RT:")]
        if not retained:
            print(f"  ACCEPTED (BUG)  {label}")
            return 1
        print(f"  reject  {label}")
        print("          " + retained[0])

    print("assertion-lane self-test — register/corpus product-decision claims")
    assertion_status = assertion_lane_selftest(base, register)
    if assertion_status != EXIT_OK:
        return assertion_status

    live_scan, live_observations, live_report = assertion_lane_failures(base)
    print(f"  measured  live corpus scan: "
          f"{live_report['artifactsParsed']}/{live_report['artifactsDiscovered']} "
          f"artifacts parsed, "
          f"{int(live_report['keyAnchoredSites']) + int(live_report['keyScopedStrings']) + int(live_report['proseSites'])}"
          f" assertion sites, "
          f"{live_report['sitesAgainstPacketRow']} cross-checked against a packet "
          f"row, {len(live_scan)} conflicting in LIVE artifacts, "
          f"{live_report['historicalObservations']} historical")
    for finding in live_scan:
        print(f"            live finding (reported by the main run): {finding}")

    print(
        f"all {len(mutations)} product-choice mutations, "
        f"{1 + len(RETENTION_AUTHORITY_MUTATIONS)} retention authority regressions, "
        f"{len(REGISTER_FABRICATION_MUTATIONS)} register fabrication regressions, "
        f"{len(SYNTHETIC_ASSERTION_MUTATIONS)} foreign-artifact assertion regressions, "
        f"{len(ASSERTION_EVASION_CASES)} spelling/synonym evasions, "
        f"{len(ASSERTION_NEGATIVE_CONTROLS)} assertion negative controls held, "
        f"{sum(STANDING_CHECKS)} standing regressions (discovery plus both "
        "gate directions) held, "
        f"{len(stale_bindings) + len(stale_proof_bindings)} stale-binding regressions, "
        f"{len(TOTALITY_ROOT_CASES)} root-shape cases and "
        f"{len(TOTALITY_NESTED_CASES)} nested-shape cases rejected — "
        "product authority is load-bearing"
    )
    return EXIT_OK


def _load_or_refuse(path: Path, required: bool = True) -> tuple[object, str | None]:
    if not path.exists():
        if required:
            return None, f"required input {path.name} is missing"
        return None, None
    try:
        return json.loads(path.read_text()), None
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return None, f"cannot read {path.name} ({type(exc).__name__})"


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    unknown = [arg for arg in args if arg not in DECLARED_FLAGS]
    if unknown:
        print(f"usage: {Path(__file__).name} [--selftest]")
        print(f"  unrecognised argument(s): {' '.join(unknown)}")
        return EXIT_USAGE
    selftest = "--selftest" in args

    inputs: dict[str, object] = {}
    refusals: list[str] = []
    for key, path, required in (
        ("product", PRODUCT_PATH, True),
        ("ri", RI_PATH, True),
        ("versioning", VERSIONING_PATH, True),
        ("delivery", DELIVERY_PATH, True),
        ("register", REGISTER_PATH, True),
        ("retention", RETENTION_PATH, False),
    ):
        value, problem = _load_or_refuse(path, required)
        if problem:
            refusals.append(problem)
        inputs[key] = value
    if refusals:
        print("REFUSING to run: the checker's own base is dirty")
        for problem in refusals:
            print(f"  - {problem}")
        return EXIT_REFUSED

    product = inputs["product"]
    ri, versioning, delivery = inputs["ri"], inputs["versioning"], inputs["delivery"]
    retention, register = inputs["retention"], inputs["register"]

    # The selftest branch is dispatched BEFORE any findings return, so a run with
    # findings and a self-test run can never produce identical output.
    if selftest:
        return mutation_selftest(product, ri, versioning, delivery, retention, register)

    failures = retention_binding_failures()
    failures.extend(validate(product, ri, versioning, delivery, retention))
    assertion_failures, observations, report = assertion_lane_failures(product)
    failures.extend(assertion_failures)

    for line in format_scan_report(report):
        print(line)
    if observations:
        print("HISTORICAL OBSERVATIONS — a product-decision assertion that "
              "conflicts with the")
        print("binding packet, in an artifact that has no standing to make it. "
              "Not a finding:")
        print("freeze §7.2 forbids editing reviewed bytes in place, so these "
              "cannot be repaired.")
        for line in observations:
            print(f"  {line}")
    if failures:
        print("product dispositions INVALID")
        for failure in failures:
            print(f"  - {failure}")
        return EXIT_FINDINGS
    # The banner states exactly what was measured. It must not widen to "no
    # artifact asserts a product decision the packet does not carry": three such
    # assertions exist, in an artifact with no standing, and are listed above.
    print(
        "product dispositions OK — 7 non-retention choices bound; "
        "CD-RT-5 remains BLOCKED_ON_PHASE_1A; "
        f"no artifact with standing ({report['artifactsLive']} of "
        f"{report['artifactsParsed']} scanned) asserts a product decision the "
        f"binding packet does not carry; "
        f"{report['historicalObservations']} such assertion(s) remain in "
        f"{report['conflictingArtifactsHistorical']} historical artifact(s), "
        "listed above; consumed "
        f"{EVALUATION_PROOF_BINDING['path']}@sha256:{EVALUATION_PROOF_BINDING['sha256']} -> "
        f"{RETENTION_BINDING['path']}@sha256:{RETENTION_BINDING['sha256']}"
    )
    return EXIT_OK


if __name__ == "__main__":
    raise SystemExit(main())
