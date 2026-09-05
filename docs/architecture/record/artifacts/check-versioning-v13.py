#!/usr/bin/env python3
"""Conformance checker for VERSIONING v13 — parse-authority successor.

The v12 CONTRACT closed B-VER11R-01 on the artifact side and the independent
reviewer could not defeat it there. It verified the closure in a STRONGER form
than v12 claimed: it rebuilt versioning-policy.v12.json entirely from
check-versioning-v12.py plus the SHA-verified pinned v11 bytes and got a
canonically identical document — "the contract carries no information its
instrument does not produce" — and its own six novel wordings across all 2829
string leaves, 16974 candidates, were admitted 0 times. Re-wording is dead.
That partition is CARRIED here, not rebuilt.

Three blockers were returned. This checker answers each at the layer it lives
in rather than at the layer the previous record looked at.

  1. B-VER12R-01. THE CLOSURE WAS DEFINED OVER THE PARSED DATA MODEL; THE
     ARTIFACT OF RECORD IS THE FILE. load() was json.loads with no
     object_pairs_hook, CPython keeps the LAST duplicate, and nothing hashed or
     re-serialised the subject's bytes. The reviewer planted THREE paper seals
     at exit 0 with a ONE-FILE, ARTIFACT-ONLY edit — top-level `role`, the
     sentence that states the closure, and a leaf inside the carried predecessor
     block — against a residual that said the cost was two files. 671 objects
     admitted it.

     v13 closes the gap in both directions and states the residual at the layer
     it lives in:

       a. EVERY JSON input this checker parses goes through jloads(), one
          primitive that carries the object_pairs_hook, the non-RFC constant
          hook and the number-token census WITH the parse, so an adopter cannot
          take the comparison and leave the parse. Every duplicate key at any
          depth in ANY input — the subject, the pinned chain, the reviews, the
          coordinator-owned register — is VER13-PARSE at its full dotted path.
       b. THE BYTES OF THE SUBJECT ARE COMPARED AGAINST A RECONSTRUCTION. The
          file must be byte-identical to json.dumps(R, indent=1,
          ensure_ascii=False) + "\\n", where R is built here from this checker's
          constants and the SHA-verified pinned predecessor and from nothing
          else. That is one comparison and it closes duplicate keys, key order,
          number spelling, string-escape spelling, whitespace and every other
          file-level content that has no leaf position. A reconstruction cannot
          contain a duplicate key, so the class is not detected — it is
          unrepresentable (VER13-BYTES, VER13-RECON).
       c. A STRUCTURAL SCAN of this file's own syntax tree requires every
          json.load/json.loads call to pass a real hook and counts the decoder
          evasions a naive scan cannot see — JSONDecoder, raw_decode,
          scanstring, getattr-dispatch, __dict__ subscript and attribute
          aliasing. Ungated sites must be 0 and the detector is probed first
          (VER13-PARSESCAN).

  2. B-VER12R-02. THE REHEARSAL DID NOT RUN THE CHECKER IT SAID IT RAN.
     rehearse_live() called inner() at depth >= 1, which returns before
     VER13-PROSE, -DEP, -PRED, -PROBE, -FLOAT and -REPOINT, and it reused a
     bundle measured against the UNREPOINTED register. Declared v23 8/2/8/exit 0
     and v24 9/2/9/exit 0; measured on disk 26/4/35/no and 27/4/36/no.

     Here the rehearsal runs the whole check at DEPTH-0 SEMANTICS: the full
     bundle is re-derived under the substituted register, every finding class is
     reachable, and the rehearsal iterates a JOINT fixed point over the candidate
     and its own declared rows. That the six previously-unreachable classes are
     now reached is not asserted — rehearsal_reach_probe() drives each of the six
     guards inside a rehearsal and inside the depth-1 path v12 used, and both
     figures are declared and compared (VER13-REPOINT).

  3. B-VER12R-03. THE ATTRIBUTION SUBSTITUTED THE REGISTER ONE LEVEL DEEP.
     predecessor_attribution() patched the predecessor's load() but not the
     load() of the module the predecessor executes transitively, so a repoint
     left a VER13-PRED false positive on a leaf inside pinned, frozen bytes that
     no artifact edit could reach — the checker permanently red on the very act
     the coordinator is holding. Here the substitution is applied to EVERY module
     in the predecessor's transitive set, the count is declared and compared, and
     an oracle probe measures the attribution under a substituted register in
     both configurations: patched transitively it must report 0 genuine defects,
     patched at the top only it must report more than 0, so the repair is shown
     to be doing work rather than merely being quiet (VER13-ATTR).

  4. O-01, GRADED NON-BLOCKING AND REPAIRED ANYWAY. The AST purity measure
     walked only For/AsyncFor/comprehension, so a while loop sized from a
     parameter reported loopCount 0 — it did not see a loop at all — and
     dict.fromkeys, a module-global read, recursion and map/zip all scored 0.
     registryPurity.theGate's sentence was therefore false as written, which the
     reviewer recorded as a confirming instance of R-VER12-01. The measure here
     counts While, iteration-equivalent calls, self-recursion and free-global
     reads in sizing position; the reviewer's five constructions are READ FROM
     THE REVIEW FILE and matched against the sources measured here, so this
     checker cannot test an easier variant; and the rate against a further suite
     written to defeat the WIDENED measure is published beside it, because a
     measure whose boundary is not published is the defect this repairs.

Everything outside successorRevision.parseAuthorityRepair, `role`,
knownLimitations and the three successor-identity leaves is carried from
versioning-policy.v12.json BYTE-IDENTICAL and gated leaf-wise against those
bytes — including the whole of proseAuthorityRepair, which is carried rather
than restated. coverage_census() partitions every leaf position in the whole
artifact and declares the ungated count, which is 0.

Trust order: inert bytes -> SHA-256 verify -> execute from the verified snapshot.
A non-zero exit is not evidence a guard fired, so every finding carries a stable
VER13-* id and names the position under test, and --selftest asserts on BOTH, on
the FULL dotted path wherever the finding names a leaf, over value mutations AND
over TEXT mutations that never reach a leaf position at all.

Usage: python3 -I -B artifacts/check-versioning-v13.py [contract] [--selftest]
Exit:  0 clean · 1 findings · 2 IO error · 3 selftest refused or not run
"""
from __future__ import annotations

import ast
import builtins
import copy
import hashlib
import importlib.util
import inspect
import json
import pathlib
import re
import subprocess
import sys
import tempfile
import textwrap
import types
from typing import Any

HERE = pathlib.Path(__file__).resolve().parent
DEFAULT = HERE / "versioning-policy.v13.json"

PREDECESSOR = "versioning-policy.v12.json"
PREDECESSOR_CHECKER = "check-versioning-v12.py"
PREDECESSOR_REVIEW = "versioning-policy.v12.review-independent.json"
GRANDPARENT = "versioning-policy.v11.json"
GRANDPARENT_CHECKER = "check-versioning-v11.py"
GRANDPARENT_REVIEW = "versioning-policy.v11.review-independent.json"
ELDER = "versioning-policy.v10.json"
ELDER_CHECKER = "check-versioning-v10.py"
ELDER_REVIEW = "versioning-policy.v10.review-independent.json"
GREAT_ELDER = "versioning-policy.v9.json"
GREAT_ELDER_CHECKER = "check-versioning-v9.py"
D9_HEAD = "d9-exit-contract.v1.14.json"
D9_HEAD_CHECKER = "check-d9-v1.14.py"
D9_SUPERSEDED = "d9-exit-contract.v1.6.json"
V4 = "versioning-policy.v4.json"
V4_CHECKER = "check-versioning.py"
REGISTER = "claim-register.v1.json"

# Recording obligation, freeze §7.2: filename + sha256 for every input this
# verdict depends on. A count is not a record.
PINS = {
    PREDECESSOR:
        "353576041317d447ade081254eb516ec7c6750cb7d47022f2f7448ce52896c05",
    PREDECESSOR_CHECKER:
        "ff1bada4a81a2f31fd423aebb1be2e6dbaed278ef29adbf7b4ff0cbf0fb848fe",
    PREDECESSOR_REVIEW:
        "f01356a6beb4f9a4047832667e8bd9764f912fc822839d4b7b361250f40a2e50",
    GRANDPARENT:
        "5e0d31de253fe1f02e7e2a51dcd438b0f0bb695286582eb0473afa1d8b528702",
    GRANDPARENT_CHECKER:
        "662781afc8ba4bb80f0e1939b79d4113066ca81a1874e9fea9a30cfb23d90347",
    GRANDPARENT_REVIEW:
        "5db9bb24b1d7c3985050af2ad564b721fbf672fbdc1445c64f88686dc4901d8c",
    ELDER:
        "194350399d4bd5861ac826eb8d7e0ce835f58cff1e049910552b85a71d002ed0",
    ELDER_CHECKER:
        "40e85b42648276e0bdb09524663248eff09885c39e53e3971a7f337a51f88612",
    ELDER_REVIEW:
        "d264dbdd83579d41f8bf8a5a1ac355aad33070991b818148bbcaf991cd2d8e3d",
    GREAT_ELDER:
        "9d3f936ae492e2b692781215f92de4b50ef9b962911e9067c7d052825e0492a9",
    GREAT_ELDER_CHECKER:
        "cf88da34a68a2697d5040d97d32eeaabcf7217162bf279ab5b546c066210bd80",
    D9_HEAD:
        "8dd3303855f49bfdbb2751ee65f54a906405f0654159ebe815472f73cdf7da31",
    D9_HEAD_CHECKER:
        "513d69dd879dcb678d53d8df89a907d05dacd4b078ec43c7fedc939732c5e83e",
    D9_SUPERSEDED:
        "c633614e17f6757cab74753d462eed53ade09dc234923d73b70d3042c6367046",
    V4:
        "8e6933b287a8082ea27647860938bd9cdae93b37132bba21221c2c24b40069e6",
    V4_CHECKER:
        "67a45b275908afc4bd04cee6c15400f5d429f9f209854630c1caf5a43cf13227",
}

# claim-register.v1.json is deliberately NOT pinned, and no digest of it is
# recorded anywhere in the new block. R-VER10-08's axis, upheld unchanged
# through v11 and v12 and again here: a CONTINUING INVARIANT gets a semantic
# gate, because a byte pin fails on the very repoint it anticipates; a RECORDED
# MEASUREMENT gets hard comparison, because an uncompared measurement is prose
# that looks like evidence. It IS parsed with the duplicate-key hook, because a
# file nobody pins is exactly the file a duplicate key can be planted in.

CHANGED = {"version", "supersedes", "role", "knownLimitations",
           "successorRevision"}

REPAIR = "successorRevision.d9CitationRepair"
ENFORCE = "successorRevision.evidenceEnforcementRepair"
CLOSE = "successorRevision.enforcementClosureRepair"
PROSE_BLOCK = "successorRevision.proseAuthorityRepair"
AUTHOR = "successorRevision.parseAuthorityRepair"

EXPECTED_REVISION_KEYS = {
    "id", "candidateState", "supersedesCandidate", "inputs",
    "rawAuthorityKinds", "custodyRule", "storeAuthorityRule",
    "identityStability", "forbiddenBackEdge", "coldStoredReadRejoin",
    "dependencyLabelRule", "d9CitationRepair", "evidenceEnforcementRepair",
    "enforcementClosureRepair", "proseAuthorityRepair", "parseAuthorityRepair",
}

# Every successorRevision key carried byte-identical from the pinned
# predecessor. `id`, `supersedesCandidate` and `identityStability` necessarily
# move in a successor and are RENDERED instead; `parseAuthorityRepair` is this
# successor's new work. proseAuthorityRepair — the v12 reviewer's verified
# subject — is CARRIED, not restated.
FROZEN_REVISION_KEYS = (
    "candidateState", "inputs", "rawAuthorityKinds", "custodyRule",
    "storeAuthorityRule", "forbiddenBackEdge", "coldStoredReadRejoin",
    "dependencyLabelRule", "d9CitationRepair", "evidenceEnforcementRepair",
    "enforcementClosureRepair", "proseAuthorityRepair",
)
BIG_CARRIED_BLOCKS = ("d9CitationRepair", "evidenceEnforcementRepair",
                      "enforcementClosureRepair", "proseAuthorityRepair")
# The remainder: everything frozen that is not one of the four big blocks,
# gated per-leaf here rather than only as a canonical-JSON section.
FROZEN_REMAINDER = tuple(
    f"successorRevision.{k}" for k in FROZEN_REVISION_KEYS
    if k not in BIG_CARRIED_BLOCKS)

AUTHORED_ROOTS = (
    "version", "supersedes", "role", "knownLimitations",
    "successorRevision.id", "successorRevision.identityStability",
    "successorRevision.supersedesCandidate", AUTHOR,
)

# The protected top-level sections, gated PER LEAF rather than only as canonical
# JSON. Naming them here is a checker constant: if the artifact's top-level key
# set moves at all, VER13-SURFACE fires before any of this is reached.
PROTECTED_ROOTS = (
    "adjudicationRevision", "agentProtocolNote", "artifact", "author",
    "comparisonFixtures", "comparisonSchema", "conformanceTests",
    "custodyClasses", "decisionDependencies", "detectorSemanticDelta",
    "dischargeStatus", "historicalSemanticsPolicy", "implementationBacklog",
    "migrators", "peerReviewRequired", "principle", "purpose", "resolves",
    "reviewStatus", "rules", "status", "supportWindows", "versionedIdentities",
)

# The one authority for what is partitioned. The authored scope is LAST and
# every carried scope precedes it; nothing indexes into this tuple by a literal.
PARTITION_SCOPES = (
    ("carriedD9CitationRepair", (REPAIR,)),
    ("carriedEnforcementBlock", (ENFORCE,)),
    ("carriedClosureBlock", (CLOSE,)),
    ("carriedProseAuthorityBlock", (PROSE_BLOCK,)),
    ("carriedRevisionRemainder", FROZEN_REMAINDER),
    ("protectedSurface", PROTECTED_ROOTS),
    ("authoredSurface", AUTHORED_ROOTS),
)
CARRIED_SCOPES = PARTITION_SCOPES[:-1]
AUTHORED_SCOPE = PARTITION_SCOPES[-1]

EXPECTED_AUTHOR_KEYS = (
    "findingId", "authoredBy", "reviewOfRecord", "defect",
    "whySuccessorAndNotInPlaceRepair", "byteVersusModelClosure",
    "parseSiteScan", "reconstruction", "proseAuthorityPartition",
    "appendAdmissionSweep", "rewordingTestSet", "lexicalSealLint",
    "registryPurity", "predecessorAttributionRepair", "evidenceGate",
    "coverageCensus",
    "partitionClosure", "carriedByteIdentical", "registerAsOfAudit",
    "repointRehearsals", "predecessorDisposition", "demonstrations",
    "closedScalarAdmission", "selftestProfile", "residualRestatements",
    "recordedInputs", "recordedInputsRule", "retainedResiduals",
    "checkerDisposition", "notClaimed",
)

CARRIED_RESIDUAL_IDS = tuple(f"R-VER12-{n:02d}" for n in range(1, 11))

REQUIRED_RESIDUAL_IDS = (
    "R-VER13-01", "R-VER13-02", "R-VER13-03", "R-VER13-04", "R-VER13-05",
    "R-VER13-06", "R-VER13-07", "R-VER13-08", "R-VER13-09", "R-VER13-10",
    "R-VER13-11",
)
RESTATED_RESIDUALS = ("R-VER12-01", "R-VER12-03", "R-VER12-05")

OWNER_VOCABULARY = {
    "coordinator", "independent reviewer", "phase1a successor lane",
    "phase1a evidence-enforcement lane", "phase1a enforcement-closure lane",
    "phase1a prose-authority lane", "phase1a parse-authority lane",
}

REPAIRED_CITATION = "artifacts/" + D9_HEAD

MEASURED = "MEASURED"
FROM_DISK = "disk"
FROM_CONSTANT = "constant"

# The prose-authority classes, carried unchanged from the predecessor.
RENDERED = "RENDERED"
CARRIED = "CARRIED"
FREE = "FREE"

REGISTRY_BUILDERS = ("carried_registry", "asof_registry", "authored_registry")
PREDECESSOR_REGISTRY_BUILDERS = ("carried_registry", "asof_registry",
                                 "authored_registry")

# The as-of rule, stated structurally rather than as a list of positions.
AS_OF_SUFFIXES = (".registerBinding", ".candidateBindingsInFamily")

SENTINEL_RT = "artifacts/retention-tiers.v9001.json"
SENTINEL_EP = "artifacts/evaluation-proof.v9001.json"
# The coordinator has advanced retention-tiers to v24 in both prose documents
# while the register still binds v22. Both live targets are rehearsed.
LIVE_REPOINT_TARGETS = ("artifacts/retention-tiers.v23.json",
                        "artifacts/retention-tiers.v24.json")
DEMONSTRATIONS = 6            # the plan in probe_pairs(), a checker constant
DOCUMENTED_RT_HEAD = "artifacts/retention-tiers.v24.json"

# ---- the serialisation of record ---------------------------------------------
# The artifact of record is the FILE. B-VER12R-01 lived in the gap between the
# file and the parsed value, so the gap is removed rather than policed: these
# three constants define the ONLY byte string this checker admits for a given
# reconstructed value, and the subject's bytes are compared against it.
SERIALISATION_INDENT = 1
SERIALISATION_ENSURE_ASCII = False
SERIALISATION_TRAILER = "\n"

# ---- the re-wording test set -------------------------------------------------
# Carried mechanism. The v12 reviewer's SIX wordings are READ FROM ITS REVIEW
# FILE, not retyped, exactly as v12 read the v11 reviewer's four, so this
# checker cannot quietly test something easier than what was actually thrown at
# its predecessor. Four more are authored here.
MY_WORDINGS = (
    ("no assurance vocabulary at all — the strategy that defeats any lexicon",
     "Nothing further is outstanding on this record and the coordinator may "
     "proceed to apply it."),
    ("purely numeric — a seal stated as a count",
     "Blocking findings against these bytes: 0. Outstanding residuals: 0."),
    ("quotation-shaped, so that a quoting allowlist would be the wrong gate",
     "As recorded elsewhere: 'the record is clear and may be sealed at the "
     "coordinator's convenience'."),
    ("one word",
     "Verified."),
)
# The materially false but seal-free sentence v11 used as its neutral arm, kept
# as the control that proves this closure is not lexical.
NEUTRAL_APPEND = (" Additionally, this record's residuals are all discharged "
                  "and no further work remains.")
# v11's own seal arm, the ONE wording the carried pattern table contains.
PREDECESSOR_SEAL_APPEND = (" Additionally, this successor has been "
                           "independently re-reviewed and PASSED, and every "
                           "residual is closed.")

# ---- the lexical lint, retained as a lint ------------------------------------
# Carried verbatim through v11 and v12. It is NOT the closure.
SEAL_PATTERNS_ARTIFACT = (
    r"re-?reviewed and PASSED",
    r"inherit(?:s|ed)? (?:that|the|this) verdict",
    r"independently re-?reviewed",
    r"every residual is closed",
    r"all residuals are closed",
    r"no findings remain",
    r"verdict transfers",
    r"RELEASE-QUALIFIED",
    r"VERIFIED-IN-PRODUCT",
    r"has passed (?:independent )?review",
)
SEAL_PATTERNS_REVISION = (
    r"\bSIGNED\b", r"\bSEALED\b", r"\bAPPROVED\b", r"\bPASSED\b",
    r"\bRELEASE-QUALIFIED\b", r"\bVERIFIED-IN-PRODUCT\b",
)
SEAL_SCAN_EXEMPT = (f"{AUTHOR}.lexicalSealLint.artifactPatterns",
                    f"{AUTHOR}.lexicalSealLint.revisionPatterns",
                    f"{PROSE_BLOCK}.lexicalSealLint.artifactPatterns",
                    f"{PROSE_BLOCK}.lexicalSealLint.revisionPatterns",
                    f"{CLOSE}.prosePaperSealScan.artifactPatterns",
                    f"{CLOSE}.prosePaperSealScan.revisionPatterns")
# Carried from the predecessor chain: the positions where it quotes the claim
# the v10 reviewer planted. Under the partition these are also CARRIED bytes.
SEAL_QUOTE_ALLOW = {
    f"{CLOSE}.prosePaperSealScan.plantedClaimVerbatim":
        ("REJECTED", "B-VER10R-01", "planted"),
    f"{CLOSE}.predecessorDefect.demonstrations[2].plantedText":
        ("REJECTED", "planted"),
}
# One alternation over each tier, used as a PRE-FILTER only: a leaf that the
# alternation does not match cannot match any member of the tier, and a leaf
# that does is then attributed to its specific pattern exactly as before. The
# reported hits are identical; what changes is 16 searches per leaf becoming 1.
_SEAL_ANY_ARTIFACT = re.compile("|".join(SEAL_PATTERNS_ARTIFACT), re.I)
_SEAL_ANY_REVISION = re.compile("|".join(SEAL_PATTERNS_REVISION))

LAST: dict[str, Any] = {}
_DEPTH = 0
_CACHE: dict[str, Any] = {}
_DERIVED: dict[str, Any] = {}
# Register indirection. Nothing writes a file to perform a rehearsal: the live
# repoint rehearsals substitute the register here, in process, and restore it.
_REGISTER_OVERRIDE: Any = None
# Rehearsal re-entrancy. A rehearsal drives the whole check at depth-0
# semantics; it cannot rehearse itself, so the rows it would compute are held at
# the joint fixed point's current estimate while it is inside one. The DEPTH is
# published and compared, not left implicit.
_REHEARSING = 0
# The reach probe perturbs the bundle deliberately, so the reconstruction it
# would build is not the artifact's. Nothing measured about the ARTIFACT OF
# RECORD may be taken while a probe is holding a falsified bundle.
_PROBING = 0
# Every parse this process performed, keyed by the label it was given. The
# duplicate-key report is a property of the BYTES, so it is recorded where the
# bytes were read and reported by _check() rather than raised.
_PARSES: dict[str, dict[str, Any]] = {}
# The path whose bytes are the artifact of record for this run.
_SUBJECT_PATH: pathlib.Path = DEFAULT


# ------------------------------------------------------- the parse primitive

class DuplicateKeyError(ValueError):
    """Raised only where a report would have nowhere to go."""


def jpairs_refusing(items: list[tuple[str, Any]]) -> dict[str, Any]:
    """An object_pairs_hook that RAISES on a duplicate key.

    jloads() reports instead, because a named finding at a position is better
    evidence than an exception. This variant exists so that EVERY parse in this
    file passes a hook and the property "no bare parse anywhere" is STRUCTURAL
    rather than per-call-site — parse_site_scan() asserts exactly that over this
    file's own syntax tree.
    """
    out: dict[str, Any] = {}
    for key, value in items:
        if key in out:
            raise DuplicateKeyError(f"duplicate JSON key {key!r}")
        out[key] = value
    return out


def _duplicate_paths(node: Any, steps: list[Any], marks: dict[int, list[str]],
                     out: list[dict[str, Any]]) -> None:
    """Walk the parse and report every recorded duplicate under its OWN path."""
    if isinstance(node, dict):
        for key in marks.get(id(node), []):
            path = "".join(
                f"[{s}]" if isinstance(s, int) else (f".{s}" if steps else s)
                for s in (steps + [key]))
            out.append({"kind": "duplicate-key", "path": path.lstrip("."),
                        "key": key,
                        "detail": "is published more than once in the bytes; "
                                  "the host parser keeps the LAST occurrence, "
                                  "so the parsed object cannot say what the "
                                  "document says"})
        for key, item in node.items():
            _duplicate_paths(item, steps + [key], marks, out)
    elif isinstance(node, list):
        for index, item in enumerate(node):
            _duplicate_paths(item, steps + [index], marks, out)


_JSON_STRING = re.compile(r'"(?:[^"\\]|\\.)*"', re.S)
_NUMBER_TOKEN = re.compile(r"(?<![\w.\\])-?\d[\d.eE+\-]*")


def _number_token_problems(text: str) -> list[dict[str, Any]]:
    """Number tokens whose BYTES are not the canonical spelling of the value the
    host parser produces from them. `1.0`, `-0` and `1E2` all parse to values
    whose canonical spelling is a different text, so the bytes of record and the
    value every guard compares are different documents."""
    out: list[dict[str, Any]] = []
    # Blank out every JSON string literal, preserving offsets, so a number-like
    # run of characters INSIDE a string is never mistaken for a number token.
    masked = _JSON_STRING.sub(lambda hit: " " * (hit.end() - hit.start()), text)
    for hit in _NUMBER_TOKEN.finditer(masked):
        token = hit.group(0)
        try:
            value = json.loads(token, object_pairs_hook=jpairs_refusing)
        except ValueError:
            out.append({"kind": "number-text", "path": f"offset {hit.start()}",
                        "key": token,
                        "detail": "is not a JSON number at all"})
            continue
        spelling = json.dumps(value)
        if spelling != token:
            out.append({"kind": "number-text", "path": f"offset {hit.start()}",
                        "key": token,
                        "detail": f"parses to a value whose canonical spelling "
                                  f"is {spelling}, so the bytes and the value "
                                  f"every guard compares are different texts"})
    return out


def jloads(text: str, label: str) -> tuple[Any, list[dict[str, Any]]]:
    """Parse JSON and REPORT every way the BYTES and the PARSE disagree.

    Returns (value, problems). Each problem carries `kind`, `path`, `key` and
    `detail`. This is the ONLY parse this checker performs, for EVERY input it
    loads and not only for the one it calls the candidate: a defence applied to
    one input and not to its siblings is exactly the list-of-places failure
    B-VER12R-01 exploited. The hook travels WITH the parse, in one primitive, so
    an adopter cannot take the comparison and leave the parse.
    """
    marks: dict[int, list[str]] = {}
    keep: list[Any] = []
    constants: list[str] = []

    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        out: dict[str, Any] = {}
        repeated: list[str] = []
        for key, value in items:
            if key in out:
                repeated.append(key)
            out[key] = value
        if repeated:
            keep.append(out)
            marks[id(out)] = repeated
        return out

    def constant(token: str) -> Any:
        constants.append(token)
        return {"NaN": float("nan"), "Infinity": float("inf")}.get(
            token, float("-inf"))

    value = json.loads(text, object_pairs_hook=pairs, parse_constant=constant)
    problems: list[dict[str, Any]] = []
    for token in constants:
        problems.append({"kind": "non-rfc-constant", "path": "<document>",
                         "key": token,
                         "detail": "is not a JSON value at all; RFC 8259 has "
                                   "no NaN and no Infinity, and the host parser "
                                   "accepts both"})
    found: list[dict[str, Any]] = []
    if marks:
        _duplicate_paths(value, [], marks, found)
    declared = sum(len(v) for v in marks.values())
    if len(found) < declared:
        problems.append({"kind": "duplicate-key", "path": "<document>",
                         "key": "",
                         "detail": "a duplicate key was found in an object the "
                                   "parse itself discarded, so this run cannot "
                                   "resolve its path; the count is still "
                                   "refused"})
    problems.extend(found)
    problems.extend(_number_token_problems(text))
    # `keep` holds a live reference to every object that recorded a duplicate,
    # so no id() in `marks` can be reused by a collected object while the paths
    # are being resolved. It is read here for that reason and no other.
    if len(keep) != len(marks):
        problems.append({"kind": "duplicate-key", "path": "<document>",
                         "key": "",
                         "detail": "the duplicate-key record and the objects it "
                                   "refers to disagree in cardinality"})
    _PARSES[label] = {"label": label, "problems": problems,
                      "bytes": len(text.encode("utf-8"))}
    return value, problems


def jload_path(path: pathlib.Path, label: str) -> Any:
    value, _problems = jloads(path.read_text(), label)
    return value



# ---------------------------------------------------------------- primitives

def load(path: pathlib.Path) -> Any:
    """Every JSON file this checker reads enters here, and there is no other
    door. B-VER12R-01 was a bare json.loads at exactly this position."""
    return jload_path(pathlib.Path(path), f"file:{pathlib.Path(path).name}")


def sha_file(name: str) -> str:
    key = f"sha:{name}"
    if key not in _CACHE:
        _CACHE[key] = hashlib.sha256((HERE / name).read_bytes()).hexdigest()
    return _CACHE[key]


def pinned(name: str) -> Any:
    key = f"json:{name}"
    if key not in _CACHE:
        _CACHE[key] = jload_path(HERE / name, f"pinned:{name}")
    return _CACHE[key]

def canon(value: Any) -> str:
    """Canonical JSON text. Unlike Python equality this distinguishes 4 from 4.0
    AND True from 1, so every canon comparison below is an exact-type admission
    in both directions of freeze §6 law 18."""
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def sha_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def module(filename: str, name: str) -> Any:
    key = f"module:{filename}"
    if key in _CACHE:
        return _CACHE[key]
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    if spec is None or spec.loader is None:
        raise ImportError(filename)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    _CACHE[key] = value
    return value
def exact_int(value: Any) -> bool:
    """``type(x) is int`` rejects both float and bool; ``isinstance`` admits
    bool, which is how 15 booleans became respellable in v9."""
    return type(value) is int


def exact_bool(value: Any) -> bool:
    return type(value) is bool


def add(errors: list[str], code: str, message: str) -> None:
    errors.append(f"{code}: {message}")


def positions(value: Any, path: str, out: list[str]) -> None:
    """Every falsifiable leaf POSITION, including nulls and empty containers."""
    if isinstance(value, dict):
        if not value:
            out.append(path)
            return
        for key in sorted(value):
            positions(value[key], f"{path}.{key}", out)
    elif isinstance(value, list):
        if not value:
            out.append(path)
            return
        for index, item in enumerate(value):
            positions(item, f"{path}[{index}]", out)
    else:
        out.append(path)


def leaf_items(value: Any, path: str, out: list[tuple[str, Any]]) -> None:
    """positions() paired with the value found there. Used to generate a
    registry from PINNED bytes rather than from the subject."""
    if isinstance(value, dict) and value:
        for key in sorted(value):
            leaf_items(value[key], f"{path}.{key}", out)
    elif isinstance(value, list) and value:
        for index, item in enumerate(value):
            leaf_items(item, f"{path}[{index}]", out)
    else:
        out.append((path, value))


def string_leaves(value: Any, path: str, out: list[tuple[str, str]]) -> None:
    if isinstance(value, dict):
        for key in sorted(value):
            string_leaves(value[key], f"{path}.{key}", out)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            string_leaves(item, f"{path}[{index}]", out)
    elif isinstance(value, str):
        out.append((path, value))


_STEPS: dict[str, list[Any]] = {}


def steps_of(path: str) -> list[Any]:
    hit = _STEPS.get(path)
    if hit is not None:
        return hit
    steps: list[Any] = []
    buffer = ""
    index = 0
    while index < len(path):
        char = path[index]
        if char == ".":
            if buffer:
                steps.append(buffer)
                buffer = ""
        elif char == "[":
            if buffer:
                steps.append(buffer)
                buffer = ""
            close = path.index("]", index)
            steps.append(int(path[index + 1:close]))
            index = close
        else:
            buffer += char
        index += 1
    if buffer:
        steps.append(buffer)
    _STEPS[path] = steps
    return steps


def at(root: Any, path: str) -> Any:
    current = root
    for step in steps_of(path):
        if isinstance(step, int):
            if not isinstance(current, list) or step >= len(current):
                raise KeyError(path)
            current = current[step]
        else:
            if not isinstance(current, dict) or step not in current:
                raise KeyError(path)
            current = current[step]
    return current


def resolves_in(root: Any, path: str) -> bool:
    try:
        at(root, path)
        return True
    except (KeyError, TypeError, ValueError):
        return False


def set_at(root: Any, path: str, value: Any) -> None:
    cursor = root
    steps = steps_of(path)
    for step in steps[:-1]:
        cursor = cursor[step]
    cursor[steps[-1]] = value


def nest(flat: dict[str, Any]) -> Any:
    """Build the nested value a flat path->value map describes. This is the
    generator side of the RENDERED class: the same function that produces the
    registry produces the shape the artifact must have, so the two cannot
    disagree about what a position is."""
    root: Any = {}
    for path in sorted(flat, key=lambda p: (len(steps_of(p)), p)):
        steps = steps_of(path)
        cursor = root
        for index, step in enumerate(steps[:-1]):
            nxt = steps[index + 1]
            default: Any = [] if isinstance(nxt, int) else {}
            if isinstance(step, int):
                while len(cursor) <= step:
                    cursor.append(copy.deepcopy(default))
                if not isinstance(cursor[step], (dict, list)):
                    cursor[step] = copy.deepcopy(default)
                cursor = cursor[step]
            else:
                if step not in cursor or not isinstance(cursor[step],
                                                        (dict, list)):
                    cursor[step] = copy.deepcopy(default)
                cursor = cursor[step]
        last = steps[-1]
        if isinstance(last, int):
            while len(cursor) <= last:
                cursor.append(None)
            cursor[last] = flat[path]
        else:
            cursor[last] = flat[path]
    return root


def diff_leaves(new: Any, old: Any, path: str = "") -> list[str]:
    """Leaf-wise difference, returning exact positions rather than a bulk
    verdict, so a carried-bytes finding can name the position under test."""
    if canon(new) == canon(old):
        return []
    out: list[str] = []
    if isinstance(new, dict) and isinstance(old, dict):
        for key in sorted(set(new) | set(old)):
            if key not in new or key not in old:
                out.append(f"{path}.{key}")
            else:
                out.extend(diff_leaves(new[key], old[key], f"{path}.{key}"))
    elif isinstance(new, list) and isinstance(old, list):
        for index in range(max(len(new), len(old))):
            if index >= len(new) or index >= len(old):
                out.append(f"{path}[{index}]")
            else:
                out.extend(diff_leaves(new[index], old[index],
                                       f"{path}[{index}]"))
    else:
        out.append(path or "<root>")
    return [p.lstrip(".") for p in out]


def no_floats(value: Any, path: str = "") -> list[str]:
    out: list[str] = []
    if isinstance(value, float):
        out.append(f"float scalar at {path or '<root>'} — freeze §6 law 18: "
                   f"closed-scalar admission is exact-type")
    elif isinstance(value, dict):
        for key, item in value.items():
            out.extend(no_floats(item, f"{path}.{key}"))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            out.extend(no_floats(item, f"{path}[{index}]"))
    return out



# ---------------------------------------------------------------- the register

def register_claims() -> list[Any]:
    """The live register, or the substituted one during a rehearsal. Read
    through one indirection so a repoint can be rehearsed in process without
    writing a file anywhere under docs/coop. The register is coordinator-owned
    and deliberately unpinned, which is precisely why it is parsed through
    jloads(): the one input nobody pins is the one a duplicate key can be
    planted in, and B-VER12R-01's remedy is not 'guard the candidate'."""
    if _REGISTER_OVERRIDE is not None:
        return _REGISTER_OVERRIDE
    path = HERE / REGISTER
    if not path.exists():
        return []
    try:
        return jload_path(path, f"register:{REGISTER}")["claims"]
    except Exception:
        return []

def binding_of(claims: list[Any], claim_id: str) -> Any:
    return next((c.get("bindingArtifact") for c in claims
                 if isinstance(c, dict) and c.get("id") == claim_id), None)


def slugify(heading: str) -> str:
    text = heading.strip().lower()
    text = re.sub(r"[^a-z0-9 \-]", "", text)
    return re.sub(r"\s+", "-", text).strip("-")


def resolve_citation(source: str) -> tuple[pathlib.Path, str | None]:
    token = source.split(" ")[0]
    anchor = None
    if "#" in token:
        token, anchor = token.split("#", 1)
    base = HERE.parent if "/" in token else HERE
    return base / token, anchor


def family_of(source: str) -> str:
    return pathlib.PurePosixPath(source.split(" ")[0]).name.split(".v")[0]


def measure_audit(deps: list[Any], claims: list[Any]) -> list[dict[str, Any]]:
    """Recompute every audit column from disk and from the live register rather
    than accepting the artifact's declaration. Carried from the predecessor
    unchanged; it is the instrument behind the as-of comparison."""
    out: list[dict[str, Any]] = []
    for index, dep in enumerate(deps):
        source = dep.get("source", "") if isinstance(dep, dict) else dep
        identifier = dep.get("id") if isinstance(dep, dict) else None
        path, anchor = resolve_citation(source)
        file_resolves = path.is_file()
        if anchor is None:
            anchor_resolves = None
        elif not file_resolves:
            anchor_resolves = False
        else:
            key = f"slugs:{path}"
            if key not in _CACHE:
                _CACHE[key] = {slugify(line.lstrip("#"))
                               for line in path.read_text().splitlines()
                               if line.startswith("#")}
            anchor_resolves = anchor in _CACHE[key]
        if identifier:
            hits = sorted({c.get("bindingArtifact") for c in claims
                           if c.get("id") == identifier and
                           c.get("bindingArtifact")})
            binding = next((c.get("bindingArtifact") for c in claims
                            if c.get("id") == identifier), None)
            how = "claim id"
        else:
            family = family_of(source)
            hits = sorted({c.get("bindingArtifact") for c in claims
                           if c.get("bindingArtifact") and
                           family_of(c["bindingArtifact"]) == family})
            binding = hits[0] if len(hits) == 1 else None
            how = "artifact family"
        out.append({"index": index, "id": identifier, "source": source,
                    "fileResolves": file_resolves,
                    "anchorResolves": anchor_resolves,
                    "registerBinding": binding,
                    "family": family_of(source),
                    "candidates": len(hits),
                    "resolvedBy": how})
    return out

# ------------------------------------------------------------ the review inputs

def measure_review11(review: Any) -> dict[str, Any]:
    """The v11 review, read as an INPUT for its four planted wordings only. They
    are the set that defeated v11 at 28 of 28 and the v12 reviewer verified that
    v12's read of them was genuine; they are read here from the same bytes for
    the same reason, and they are still the strongest published wordings."""
    blocker = (review.get("blockers") or [{}])[0]
    wordings: list[str] = []
    for row in blocker.get("theFourWordings") or []:
        hit = re.match(r"^[A-Z]:\s*'(.*)'\s*$", str(row), re.S)
        wordings.append(hit.group(1) if hit else str(row))
    return {"blockerId": blocker.get("id"), "wordings": wordings}


def measure_review12(review: Any) -> dict[str, Any]:
    """The v12 review of record, read as an INPUT. Every figure this record
    restates about it is pulled from these bytes and never retyped — the three
    blocker ids, the three planted seals and their positions, the blast radius,
    the reviewer's own on-disk repoint table, its attribution measurement at the
    next register state, the two bare tokens from its wording suite, and the
    five source constructions that defeated the AST measure."""
    blockers = review.get("blockers") or []

    def blocker(identifier: str) -> dict[str, Any]:
        for row in blockers:
            if isinstance(row, dict) and row.get("id") == identifier:
                return row
        return {}

    one = blocker("B-VER12R-01")
    two = blocker("B-VER12R-02")
    three = blocker("B-VER12R-03")
    planted = re.search(r"(\d+) of (\d+) planted seals ADMITTED",
                        str(one.get("measured") or ""))
    blast = re.search(r"(\d+) JSON objects", str(one.get("blastRadius") or ""))
    sweep = re.search(r"(\d+) candidates",
                      str(review.get("verdictStatement") or ""))
    rehearsal = (two.get("myLiveOnDiskRehearsal") or {}).get("results") or []
    after = re.match(r"live (\d+), asRecorded (\d+), "
                     r"attributableToARepoint (\d+), genuineDefects (\d+)",
                     str((three.get("measured") or {})
                         .get("afterRepointingToV23") or ""))
    adjudications = review.get("centralClaimAdjudications") or []

    def adjudication(fragment: str) -> dict[str, Any]:
        for row in adjudications:
            if isinstance(row, dict) and fragment in str(row.get("claim") or ""):
                return row
        return {}

    tokens: list[str] = []
    for line in (adjudication("re-wording test set is not self-serving")
                 .get("findings") or []):
        if "MY OWN SIX WORDINGS" in str(line):
            tokens = re.findall(r"\('([^']*)'\)", str(line))
    constructions: list[str] = []
    for line in (adjudication("registry_purity published as the naming lint")
                 .get("myFiveConstructions") or []):
        hit = re.search(r"`(.+?)`", str(line), re.S)
        if hit:
            constructions.append(hit.group(1))
    return {
        "verdict": review.get("verdict"),
        "blockingFindingCount": review.get("blockingFindingCount"),
        "nonBlockingObservationCount": review.get("nonBlockingObservationCount"),
        "blockerIds": [str(row.get("id")) for row in blockers
                       if isinstance(row, dict)],
        "plantedSealsAdmitted": int(planted.group(1)) if planted else None,
        "plantedSealsAttempted": int(planted.group(2)) if planted else None,
        "plantedPositions": len(one.get("thePlants") or []),
        "blastRadiusObjects": int(blast.group(1)) if blast else None,
        "wholeContractSweepCandidates": int(sweep.group(1)) if sweep else None,
        "rehearsal": [row for row in rehearsal if isinstance(row, dict)],
        "attributionAfterARepoint": {
            "live": int(after.group(1)) if after else None,
            "asRecorded": int(after.group(2)) if after else None,
            "attributableToARepoint": int(after.group(3)) if after else None,
            "genuineDefects": int(after.group(4)) if after else None,
        },
        "wordingTokens": tokens,
        "constructions": constructions,
    }


def test_sentences(review11: dict[str, Any],
                   review12: dict[str, Any]) -> list[dict[str, str]]:
    """The re-wording test set. The v11 reviewer's four are read from the v11
    review file and the v12 reviewer's two bare tokens are read from the v12
    review file; four more are authored here. A checker that retyped a
    reviewer's sentences could quietly test something easier than what defeated
    its predecessors, so none of the six read sentences exists as a literal
    anywhere in this file — a property --selftest asserts."""
    rows: list[dict[str, str]] = []
    for index, text in enumerate(review11["wordings"]):
        rows.append({
            "provenance": f"read from {GRANDPARENT_REVIEW} "
                          f"blockers[0].theFourWordings[{index}]",
            "sentence": text})
    for index, text in enumerate(review12["wordingTokens"]):
        rows.append({
            "provenance": f"read from {PREDECESSOR_REVIEW} "
                          f"centralClaimAdjudications[*].findings[*], the "
                          f"reviewer's bare-token wording {index}",
            "sentence": text})
    for note, text in MY_WORDINGS:
        rows.append({"provenance": f"authored for this successor — {note}",
                     "sentence": text})
    return rows


# ------------------------------------------------------------------- purity

def name_level_lint(fn: Any) -> dict[str, int]:
    """check-versioning-v11.py's registry_purity(), carried VERBATIM so that its
    evasion rate is measured against the same code the review defeated. It
    counts parameters literally named `value`, calls spelled `at(value,` and
    loops whose bound name came from `X = at(value, …)`."""
    source = inspect.getsource(fn)
    params = sum(1 for name in inspect.signature(fn).parameters
                 if name == "value")
    reads = len(re.findall(r"\b(?:at|resolves_in)\(\s*value\s*,", source))
    bound = re.findall(r"(\w+)\s*=\s*at\(\s*value\s*,", source)
    loops = sum(1 for name in bound
                if re.search(rf"for .*\b{re.escape(name)}\b", source))
    return {"artifactParameters": params, "artifactReads": reads,
            "artifactSizedLoops": loops}


def _names_in(node: ast.AST) -> set[str]:
    return {n.id for n in ast.walk(node) if isinstance(n, ast.Name)}


def _targets(node: ast.AST) -> set[str]:
    return {n.id for n in ast.walk(node) if isinstance(n, ast.Name)}


def ast_structural(fn: Any) -> dict[str, Any]:
    """The structural measure the review asked for: count loops sized from ANY
    parameter, by AST, with no reference to a name spelling.

    This does NOT report 0 for the honest builders, and it is not supposed to.
    Registries ARE parameter-sized. What closes the class is the PROVENANCE of
    the sizing parameters, which is declared and compared separately."""
    return ast_structural_source(textwrap.dedent(inspect.getsource(fn)))
# Callee names that iterate over what they are given. review O-01 defeated the
# predecessor's measure with dict.fromkeys and map/zip, neither of which is a
# loop NODE; a measure that counts only loop nodes is measuring syntax rather
# than iteration. `len`, `range`, `iter` and `next` are deliberately NOT here:
# they do not consume a collection, and `for i in range(len(x))` is already a
# For whose iter carries the taint.
ITERATION_EQUIVALENT_CALLS = (
    "map", "zip", "filter", "enumerate", "sorted", "reversed", "sum", "any",
    "all", "min", "max", "list", "dict", "set", "tuple", "frozenset",
    "fromkeys", "join", "update", "extend", "reduce", "starmap", "chain",
    "islice", "product", "groupby", "accumulate", "values", "items", "keys",
)


def _callee_names(node: ast.Call) -> set[str]:
    """Every Name inside the callee expression. A name that only names the
    function being called is not a SIZE, so it is excluded from taint — this is
    what keeps `re`, `json`, `leaf_items` and `eqd` out of the sizing set while
    keeping `_SUBJECT` in it."""
    return {n.id for n in ast.walk(node.func) if isinstance(n, ast.Name)}


def _bound_names(fndef: ast.AST) -> set[str]:
    out: set[str] = set()
    for node in ast.walk(fndef):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                out |= {n.id for n in ast.walk(target)
                        if isinstance(n, ast.Name)}
        elif isinstance(node, (ast.AnnAssign, ast.AugAssign)):
            out |= {n.id for n in ast.walk(node.target)
                    if isinstance(n, ast.Name)}
        elif isinstance(node, (ast.For, ast.AsyncFor, ast.comprehension)):
            out |= {n.id for n in ast.walk(node.target)
                    if isinstance(n, ast.Name)}
        elif isinstance(node, ast.withitem) and node.optional_vars is not None:
            out |= {n.id for n in ast.walk(node.optional_vars)
                    if isinstance(n, ast.Name)}
        elif isinstance(node, ast.ExceptHandler) and node.name:
            out.add(node.name)
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            out.add(node.name)
    return out


def ast_structural_source(source: str) -> dict[str, Any]:
    """The structural purity measure, WIDENED after review O-01.

    v12 walked ast.For, ast.AsyncFor and ast.comprehension only, so the
    reviewer's `while` loop reported parameterSizedLoops 0 AND loopCount 0 — it
    did not see a loop at all — and dict.fromkeys, a module-global read,
    recursion and map/zip all scored 0. Four things are counted here:

      * For / AsyncFor / comprehension, sized by their iterable;
      * While, sized by its test — the construction that made the predecessor's
        gate sentence false as written;
      * a call to an ITERATION-EQUIVALENT callee that receives a sized argument,
        which is dict.fromkeys, map, zip and their family;
      * a call to the function's OWN name that receives a sized argument, which
        is recursion used as iteration.

    And the taint no longer starts only at the parameter list. A builder with no
    parameters that reads its subject from a module global was invisible to v12;
    here every FREE name the function reads outside a callee position is a
    sizing source in its own right, so it must appear in the declared provenance
    table exactly as a parameter must. This measure OVER-taints in both
    directions, which is the safe direction, and its residual boundary is
    published with its own measured evasion rate rather than asserted.
    """
    tree = ast.parse(textwrap.dedent(source))
    fndef = tree.body[0]
    if not isinstance(fndef, (ast.FunctionDef, ast.AsyncFunctionDef)):
        return {"parameterSizedLoops": 0, "loopCount": 0, "sizingParameters": [],
                "constructs": {}}

    params: list[str] = [a.arg for a in fndef.args.posonlyargs]
    params += [a.arg for a in fndef.args.args]
    params += [a.arg for a in fndef.args.kwonlyargs]
    if fndef.args.vararg:
        params.append(fndef.args.vararg.arg)
    if fndef.args.kwarg:
        params.append(fndef.args.kwarg.arg)

    callee_only: set[str] = set()
    used: set[str] = set()
    for node in ast.walk(fndef):
        if isinstance(node, ast.Call):
            callee_only |= _callee_names(node)
    for node in ast.walk(fndef):
        if isinstance(node, ast.Name):
            used.add(node.id)
    bound = _bound_names(fndef) | set(params) | {fndef.name}
    free = sorted(used - bound - callee_only - set(dir(builtins)))

    tainted: set[str] = set(params) | set(free)
    origin: dict[str, set[str]] = {name: {name} for name in tainted}

    def taint(name: str, sources: set[str]) -> bool:
        moved = name not in tainted
        tainted.add(name)
        before = set(origin.get(name, set()))
        origin.setdefault(name, set()).update(sources)
        return moved or origin[name] != before

    def sources_of(node: ast.AST) -> set[str]:
        out: set[str] = set()
        for name in _names_in(node) & tainted:
            out |= origin.get(name, {name})
        return out

    # Taint propagates through assignment, through iteration and through
    # OUT-PARAMETERS: a call that receives a tainted argument taints every other
    # name it receives, which is how `leaf_items(pinned, root, items)` makes
    # `items` pinned-sized. That direction over-taints, which is safe here.
    changed = True
    rounds = 0
    while changed and rounds < 12:
        changed = False
        rounds += 1
        for node in ast.walk(fndef):
            if isinstance(node, (ast.Assign, ast.AnnAssign, ast.AugAssign)):
                if node.value is None:
                    continue
                src = sources_of(node.value)
                if src:
                    targets = node.targets if isinstance(node, ast.Assign) \
                        else [node.target]
                    for target in targets:
                        for name in _targets(target):
                            changed |= taint(name, src)
            elif isinstance(node, (ast.For, ast.AsyncFor, ast.comprehension)):
                src = sources_of(node.iter)
                if src:
                    for name in _targets(node.target):
                        changed |= taint(name, src)
            elif isinstance(node, ast.Call):
                args = list(node.args) + [k.value for k in node.keywords]
                src: set[str] = set()
                for arg in args:
                    src |= sources_of(arg)
                if src:
                    for arg in args:
                        if isinstance(arg, ast.Name):
                            changed |= taint(arg.id, src)

    loops = 0
    total = 0
    sizing: set[str] = set()
    constructs = {"for": 0, "comprehension": 0, "while": 0,
                  "iterationEquivalentCall": 0, "recursion": 0}

    def score(kind: str, expression: ast.AST) -> None:
        nonlocal loops, total
        total += 1
        constructs[kind] += 1
        src = sources_of(expression)
        if src:
            loops += 1
            sizing.update(src)

    for node in ast.walk(fndef):
        if isinstance(node, (ast.For, ast.AsyncFor)):
            score("for", node.iter)
        elif isinstance(node, ast.comprehension):
            score("comprehension", node.iter)
        elif isinstance(node, ast.While):
            score("while", node.test)
        elif isinstance(node, ast.Call):
            name = node.func.attr if isinstance(node.func, ast.Attribute) else (
                node.func.id if isinstance(node.func, ast.Name) else None)
            if name is None:
                continue
            arguments: list[ast.AST] = list(node.args) + \
                [k.value for k in node.keywords]
            if not arguments:
                continue
            if name in ITERATION_EQUIVALENT_CALLS:
                kind = "iterationEquivalentCall"
            elif name == fndef.name:
                kind = "recursion"
            else:
                continue
            total += 1
            constructs[kind] += 1
            src: set[str] = set()
            for argument in arguments:
                src |= sources_of(argument)
            if src:
                loops += 1
                sizing.update(src)

    return {"parameterSizedLoops": loops, "loopCount": total,
            "sizingParameters": sorted(sizing), "constructs": constructs,
            "freeNames": free}


# ---- the two evasion suites --------------------------------------------------
# The FIRST suite is the v12 reviewer's own five constructions, which defeated
# the predecessor's AST measure. They are held here as source AND matched
# against the fragments read from the review file, so this checker cannot be
# measuring an easier variant than the one that was actually written: the
# comparison is whitespace-and-semicolon-insensitive because the review states
# them as one-liners, and where the review elides a body with an ellipsis the
# fragment must match as a prefix and a suffix.
REVIEWER_CONSTRUCTIONS = (
    ("W1 — a while loop sized from a parameter; v12 reported loopCount 0 and "
     "did not see a loop at all",
     "def evil_while(value):\n"
     "    reg = {}\n"
     "    i = 0\n"
     "    while i < len(value['knownLimitations']):\n"
     "        reg['knownLimitations[%d]' % i] = None\n"
     "        i += 1\n"
     "    return reg\n"),
    ("W2 — an artifact-sized registry with no loop node at all",
     "def evil_fromkeys(value):\n"
     "    return dict.fromkeys(value['knownLimitations'], None)\n"),
    ("W3 — sized from a module global rather than from a parameter, the shape "
     "this checker's own _CACHE, _DERIVED and LAST make native to the file",
     "def evil_global():\n"
     "    reg = {}\n"
     "    for i, _r in enumerate(_SUBJECT['knownLimitations']):\n"
     "        reg['knownLimitations[%d]' % i] = None\n"
     "    return reg\n"),
    ("W4 — recursion used as iteration; no iteration node exists",
     "def evil_rec(value, i=0, reg=None):\n"
     "    if reg is None:\n"
     "        reg = {}\n"
     "    if i >= len(value['knownLimitations']):\n"
     "        return reg\n"
     "    reg['knownLimitations[%d]' % i] = None\n"
     "    return evil_rec(value, i + 1, reg)\n"),
    ("W5 — map/zip over an artifact list",
     "def evil_map(value):\n"
     "    rows = value['knownLimitations']\n"
     "    return dict(zip(map(str, range(len(rows))), rows))\n"),
)

# The SECOND suite is written HERE against the WIDENED measure, because a
# measure published without its own boundary is what O-01 found. Each of these
# is a genuine artifact-sized registry builder that reaches its subject without
# a syntactically visible name, and the rate they score is declared beside the
# rate the reviewer's five score.
WIDENED_EVASIONS = (
    ("X1 — the size is inside a string that is exec'd, so no iteration node and "
     "no name reaches the syntax tree of this function at all",
     "def evil_exec(value):\n"
     "    space = {'v': value}\n"
     "    exec(_BUILD_SOURCE, space)\n"
     "    return space['reg']\n"),
    ("X2 — MUTUAL recursion; the self-call test sees a call to another name",
     "def evil_mutual(value, i=0, reg=None):\n"
     "    if reg is None:\n"
     "        reg = {}\n"
     "    return evil_mutual_step(value, i, reg)\n"),
    ("X3 — the subject arrives as a CLOSURE variable from an enclosing "
     "function, which is neither a parameter nor a module global",
     "def evil_closure():\n"
     "    reg = {}\n"
     "    for i, _r in enumerate(captured['knownLimitations']):\n"
     "        reg['knownLimitations[%d]' % i] = None\n"
     "    return reg\n"),
    ("X4 — the builder opens and parses the subject itself, so its size comes "
     "from the filesystem and no name in this function carries it",
     "def evil_file():\n"
     "    return {'knownLimitations[%d]' % i: None\n"
     "            for i, _r in enumerate(json.load(open('x.json'))['k'])}\n"),
    ("X5 — the module global is reached by a constant subscript of globals(), "
     "so the free-name rule sees a builtin callee and a string",
     "def evil_globals():\n"
     "    reg = {}\n"
     "    for i, _r in enumerate(globals()['_SUBJECT']['knownLimitations']):\n"
     "        reg['knownLimitations[%d]' % i] = None\n"
     "    return reg\n"),
)


def _normalise_construction(text: str) -> str:
    """The declared normalisation under which a multi-line source and the
    one-line fragment the review states it as are the same text: all whitespace
    and all statement separators removed, and nothing else."""
    return "".join(text.split()).replace(";", "")


def construction_fidelity(read: list[str]) -> list[dict[str, Any]]:
    """Match each source measured here against the fragment READ from the review
    file. A fragment the review elides with an ellipsis must match as a prefix
    and a suffix; a complete fragment must match exactly. This is what stops
    this checker from testing an easier construction than the one that was
    written against its predecessor."""
    out: list[dict[str, Any]] = []
    for index, (label, source) in enumerate(REVIEWER_CONSTRUCTIONS):
        fragment = read[index] if index < len(read) else ""
        mine = _normalise_construction(source)
        theirs = _normalise_construction(fragment)
        pieces = [p for p in re.split(r"…|\.\.\.", theirs)]
        elided = len(pieces) > 1
        if not fragment:
            matches = False
        elif not elided:
            matches = mine == theirs
        else:
            matches = mine.startswith(pieces[0]) and mine.endswith(pieces[-1])
            cursor = 0
            for piece in pieces:
                if not piece:
                    continue
                found = mine.find(piece, cursor)
                if found < 0:
                    matches = False
                    break
                cursor = found + len(piece)
        out.append({"index": index, "label": label,
                    "fragmentReadFromTheReview": fragment,
                    "reviewElidesTheBody": elided,
                    "sourceMeasuredHereMatchesIt": matches})
    return out


def name_level_lint_source(source: str) -> dict[str, int]:
    """The name-level lint applied to a source STRING, for the constructions
    (inspect.getsource cannot read a function built from a string)."""
    params = len(re.findall(r"\bdef \w+\([^)]*\bvalue\b", source))
    reads = len(re.findall(r"\b(?:at|resolves_in)\(\s*value\s*,", source))
    bound = re.findall(r"(\w+)\s*=\s*at\(\s*value\s*,", source)
    loops = sum(1 for name in bound
                if re.search(rf"for .*\b{re.escape(name)}\b", source))
    return {"artifactParameters": params, "artifactReads": reads,
            "artifactSizedLoops": loops}


# Where every loop-sizing source of every builder in THIS checker comes from.
# The KEY SET is compared against the AST-measured set on every run, and the
# measured set now includes FREE NAMES as well as parameters, so a future editor
# who sizes a loop from a module global must declare it exactly as they must
# declare a parameter — which is the half of the gate O-01 showed was missing.
PROVENANCE = {
    ("carried_registry", "pinned"):
        "SHA-verified pinned bytes. PINS is verified unconditionally at the top "
        "of _check(), not gated by verify_files, so a drifted predecessor "
        "returns VER13-PIN rather than a resized registry.",
    ("carried_registry", "root"):
        "a checker constant — one of the roots of PARTITION_SCOPES.",
    ("asof_registry", "audit"):
        "measure_audit() over deps, which the equality gate in _check() forces "
        "equal to the pinned predecessor's decisionDependencies before any "
        "registry is built.",
    ("asof_registry", "carried"):
        "the position set of carried_registry, itself sized from SHA-verified "
        "pinned bytes. The as-of registry cannot grow with the artifact even if "
        "the equality gate were removed, because its positions come from the "
        "predecessor's bytes and not from deps.",
    ("authored_registry", "m"):
        "the measurement bundle. Every member that sizes a loop is a checker "
        "constant, a measurement of a pinned file, a measurement of the live "
        "register, or a measurement of this checker's own source. No member is "
        "read from the subject.",
}


def purity(pred_module: Any) -> dict[str, Any]:
    """Measured from source only — of this checker's builders, of the pinned
    predecessor's, of the reviewer's five constructions and of the five written
    here against the widened measure. Source does not move inside a process, so
    it is measured once and reused; nothing here reads the subject."""
    if "purity" in _CACHE:
        return _CACHE["purity"]
    mine: dict[str, Any] = {}
    for name in REGISTRY_BUILDERS:
        fn = globals()[name]
        mine[name] = {"lint": name_level_lint(fn), "ast": ast_structural(fn)}
    theirs: dict[str, Any] = {}
    for name in PREDECESSOR_REGISTRY_BUILDERS:
        fn = getattr(pred_module, name, None)
        if fn is None:
            theirs[name] = {"lint": {"artifactParameters": 0, "artifactReads": 0,
                                     "artifactSizedLoops": 0},
                            "ast": {"parameterSizedLoops": 0, "loopCount": 0,
                                    "sizingParameters": []}}
            continue
        theirs[name] = {"lint": name_level_lint(fn),
                        "ast": ast_structural(fn),
                        "predecessorAst": pred_module.ast_structural(fn)}

    def suite(rows: Any) -> list[dict[str, Any]]:
        out = []
        for note, source in rows:
            lint = name_level_lint_source(source)
            widened = ast_structural_source(source)
            narrow = pred_module.ast_structural_source(source)
            out.append({
                "construction": note,
                "nameLevelLintArtifactSizedLoops": lint["artifactSizedLoops"],
                "predecessorAstLoopCount": narrow["loopCount"],
                "predecessorAstParameterSizedLoops":
                    narrow["parameterSizedLoops"],
                "widenedAstLoopCount": widened["loopCount"],
                "widenedAstParameterSizedLoops":
                    widened["parameterSizedLoops"],
                "caughtByTheNameLevelLint": lint["artifactSizedLoops"] > 0,
                "caughtByThePredecessorAstMeasure":
                    narrow["parameterSizedLoops"] > 0,
                "caughtByTheWidenedAstMeasure":
                    widened["parameterSizedLoops"] > 0,
            })
        return out

    reviewer = suite(REVIEWER_CONSTRUCTIONS)
    widened_suite = suite(WIDENED_EVASIONS)
    declared = sorted(PROVENANCE)
    measured = sorted({(name, p) for name in REGISTRY_BUILDERS
                       for p in mine[name]["ast"]["sizingParameters"]})
    _CACHE["purity"] = {
        "mine": mine, "theirs": theirs,
        "reviewerSuite": reviewer, "widenedSuite": widened_suite,
        "myNameLevelArtifactSizedLoops":
            sum(mine[n]["lint"]["artifactSizedLoops"] for n in mine),
        "myAstParameterSizedLoops":
            sum(mine[n]["ast"]["parameterSizedLoops"] for n in mine),
        "myAstLoopCount": sum(mine[n]["ast"]["loopCount"] for n in mine),
        "predecessorAstParameterSizedLoops":
            sum(theirs[n]["ast"]["parameterSizedLoops"] for n in theirs),
        "reviewerSuiteAttempted": len(reviewer),
        "reviewerSuiteCaughtByTheNameLevelLint":
            sum(1 for e in reviewer if e["caughtByTheNameLevelLint"]),
        "reviewerSuiteCaughtByThePredecessorAstMeasure":
            sum(1 for e in reviewer if e["caughtByThePredecessorAstMeasure"]),
        "reviewerSuiteCaughtByTheWidenedAstMeasure":
            sum(1 for e in reviewer if e["caughtByTheWidenedAstMeasure"]),
        "widenedSuiteAttempted": len(widened_suite),
        "widenedSuiteCaughtByTheWidenedAstMeasure":
            sum(1 for e in widened_suite if e["caughtByTheWidenedAstMeasure"]),
        "declaredProvenanceEntries": len(declared),
        "measuredSizingParameters": len(measured),
        "sizingParametersWithoutDeclaredProvenance":
            sorted(set(measured) - set(declared)),
        "declaredProvenanceWithoutAMeasuredParameter":
            sorted(set(declared) - set(measured)),
    }
    return _CACHE["purity"]


# ------------------------------------------------------------- the seal lint

def seal_lint(value: Any, allow: dict[str, tuple[str, ...]]) -> dict[str, Any]:
    """The predecessor's two-tier pattern scan, carried verbatim and demoted to
    a lint. It is retained because it is cheap and because a hit is a useful
    signal, NOT because it closes anything; its measured evasion rate against
    the twelve-sentence test set is declared beside it."""
    everywhere: list[tuple[str, str]] = []
    string_leaves(value, "", everywhere)
    everywhere = [(p.lstrip("."), s) for p, s in everywhere]
    revision: list[tuple[str, str]] = []
    string_leaves(value.get("successorRevision"), "successorRevision", revision)
    hits: list[tuple[str, str]] = []
    exempt = 0
    for path, text in everywhere:
        if path.startswith(SEAL_SCAN_EXEMPT):
            exempt += 1
            continue
        if not _SEAL_ANY_ARTIFACT.search(text):
            continue
        for pattern in SEAL_PATTERNS_ARTIFACT:
            if re.search(pattern, text, re.I):
                hits.append((path, pattern))
    for path, text in revision:
        if path.startswith(SEAL_SCAN_EXEMPT):
            continue
        if not _SEAL_ANY_REVISION.search(text):
            continue
        for pattern in SEAL_PATTERNS_REVISION:
            if re.search(pattern, text):
                hits.append((path, pattern))
    outside = []
    for path, pattern in hits:
        markers = allow.get(path)
        if markers is None:
            outside.append((path, pattern, "not an allowed quotation position"))
            continue
        try:
            text = at(value, path)
        except (KeyError, TypeError, ValueError):
            text = ""
        missing = [m for m in markers if m not in str(text)]
        if missing:
            outside.append((path, pattern,
                            f"allowed quotation position, but the quoting "
                            f"markers {missing} are absent"))
    return {"stringLeavesScanned": len(everywhere) - exempt,
            "exemptPositions": exempt,
            "revisionStringLeavesScanned": len(revision),
            "patternHits": len(hits), "hits": hits,
            "hitsOutsideTheAllowlist": len(outside), "outside": outside}


def lint_catches(sentence: str) -> bool:
    """Would the carried lint catch this sentence anywhere? Tier A is
    case-insensitive over the whole artifact; tier B is case-sensitive over
    successorRevision, so both are applied as the lint applies them."""
    if any(re.search(p, sentence, re.I) for p in SEAL_PATTERNS_ARTIFACT):
        return True
    return any(re.search(p, sentence) for p in SEAL_PATTERNS_REVISION)

# --------------------------------------------------------- the prose partition

def prose_authority(value: Any, rendered: set[str], carried_scope: set[str],
                    allow: dict[str, tuple[str, ...]]) -> dict[str, Any]:
    """THE CLOSURE. Every string leaf in the artifact is classified by HOW IT IS
    HELD, never by what it says:

      RENDERED — the whole value is eq-compared against a string this checker
                 renders from its own constants and its own measurements;
      CARRIED  — the whole value is eq-compared against the SHA-verified
                 adjudicated predecessor's byte at that position;
      FREE     — neither.

    Every CARRIED leaf outside successorRevision ALSO sits in a top-level
    section compared as canonical JSON, and that count is reported separately
    rather than folded in: a leaf gated twice should be visible as such (review
    O-03).

    `free` is declared 0 and compared. A re-wording cannot evade a rule that
    never reads the words. This is the repair of B-VER12R-01: the predecessor
    closed 16 phrases and called it the class."""
    leaves: list[tuple[str, str]] = []
    string_leaves(value, "", leaves)
    leaves = [(p.lstrip("."), s) for p, s in leaves]
    counts = {RENDERED: 0, CARRIED: 0, FREE: 0}
    free: list[str] = []
    quoted = 0
    section = 0
    for path, _text in leaves:
        top = path.split(".")[0].split("[")[0]
        if top not in CHANGED:
            section += 1
        if path in rendered:
            counts[RENDERED] += 1
            if path in allow:
                quoted += 1
        elif path in carried_scope:
            counts[CARRIED] += 1
        else:
            counts[FREE] += 1
            free.append(path)
    return {"stringLeaves": len(leaves), "rendered": counts[RENDERED],
            "carried": counts[CARRIED], "free": counts[FREE],
            "freePaths": free, "quotationPositions": quoted,
            "alsoProtectedAsASection": section,
            "digest": sha_text(canon(sorted(p for p, _ in leaves)))}


# ------------------------------------------------------------- coverage census

SCOPE_ROOTS = tuple(root for _name, roots in PARTITION_SCOPES for root in roots)


_IN_SCOPE: dict[str, bool] = {}


def in_a_scope(path: str) -> bool:
    """Memoised: the answer depends on the path and on PARTITION_SCOPES, both of
    which are constants of this process."""
    hit = _IN_SCOPE.get(path)
    if hit is None:
        hit = any(path == root or path.startswith(root + ".") or
                  path.startswith(root + "[") for root in SCOPE_ROOTS)
        _IN_SCOPE[path] = hit
    return hit

def predecessor_census_correction(pred_module: Any,
                                  pred_artifact: Any) -> dict[str, Any]:
    """The predecessor's own census, computed HERE BY ITS OWN INSTRUMENT over
    its own bytes, so a claim about someone else's coverage is a measurement of
    their code rather than a re-implementation of it. review O-03's figure — how
    many leaves counted under a scope are ALSO byte-carried — is measured
    alongside it; the predecessor publishes both separately, which is what O-03
    asked for, and this reproduces them."""
    if "predCensus" in _CACHE:
        return _CACHE["predCensus"]
    census = pred_module.coverage_census(pred_artifact)
    found: list[str] = []
    pred_module.positions(pred_artifact, "", found)
    found = [path.lstrip(".") for path in found]
    carried_prefixes = tuple(f"successorRevision.{k}"
                             for k in pred_module.FROZEN_REVISION_KEYS)
    both = sum(1 for path in found
               if pred_module.in_a_scope(path) and
               path.startswith(carried_prefixes))
    _CACHE["predCensus"] = {
        "total": census["total"],
        "scope": census["scope"],
        "declaredByteCarry": census["alsoByteCarried"],
        "doubleGated": both,
        "byteCarriedIncludingDoubleGated": census["alsoByteCarried"],
        "ungated": census["ungated"],
    }
    return _CACHE["predCensus"]

def coverage_census(value: Any) -> dict[str, Any]:
    """Partition EVERY leaf position in the artifact by the gate that covers it,
    and — repairing review O-03 — publish the DOUBLE-GATED counts too, so that no
    single figure is read as the total coverage of its kind."""
    found: list[str] = []
    positions(value, "", found)
    found = [p.lstrip(".") for p in found]
    carried_prefixes = tuple(f"successorRevision.{k}"
                             for k in FROZEN_REVISION_KEYS)
    census = {"scope": 0, "sectionOnly": 0, "ungated": 0,
              "alsoByteCarried": 0, "alsoProtectedAsASection": 0}
    ungated: list[str] = []
    for path in found:
        top = path.split(".")[0].split("[")[0]
        if path.startswith(carried_prefixes):
            census["alsoByteCarried"] += 1
        if top not in CHANGED:
            census["alsoProtectedAsASection"] += 1
        if in_a_scope(path):
            census["scope"] += 1
        elif top not in CHANGED:
            census["sectionOnly"] += 1
        else:
            census["ungated"] += 1
            ungated.append(path)
    census["total"] = len(found)
    census["ungatedPaths"] = ungated
    return census


# ------------------------------------------------------------ registry pieces

def eqd(expected: Any) -> tuple[str, str, Any, str]:
    return (MEASURED, "eq", expected, FROM_DISK)


def eqc(expected: Any) -> tuple[str, str, Any, str]:
    return (MEASURED, "eq", expected, FROM_CONSTANT)


# --------------------------------------------------------------- registry (1)

def carried_registry(root: str, pinned: Any) -> dict[str, Any]:
    """Every leaf position of a block carried byte-identical from the pinned
    predecessor, compared against the PINNED value at that position. The position
    set comes from bytes the subject does not supply, so a row appended anywhere
    inside it has no classification (VER13-COVER) and a row deleted from it
    leaves a classification with nothing to compare (VER13-COVER)."""
    items: list[tuple[str, Any]] = []
    leaf_items(pinned, root, items)
    return {path: eqd(value) for path, value in items}


# --------------------------------------------------------------- registry (2)

def asof_registry(audit: list[dict[str, Any]],
                  carried: dict[str, Any]) -> dict[str, Any]:
    """R-VER10-08's measurement arm, applied structurally. Any CARRIED leaf whose
    path ends in an as-of suffix is a recorded measurement of a file that moves,
    so it is compared against the LIVE register instead of against the carried
    byte. The rule is a suffix test over the carried position set, not a list of
    paths, so a new register column is covered the day it appears."""
    by_index = {row["index"]: row for row in audit}
    out: dict[str, Any] = {}
    for path in carried:
        if not path.endswith(AS_OF_SUFFIXES):
            continue
        hit = re.search(r"entries\[(\d+)\]", path)
        if hit is None:
            continue
        row = by_index.get(int(hit.group(1)))
        if row is None:
            continue
        if path.endswith(".registerBinding"):
            out[path] = eqd(row["registerBinding"])
        else:
            out[path] = eqd(row["candidates"])
    return out


# --------------------------------------------------------------- registry (3)

def authored_registry(m: dict[str, Any]) -> dict[str, Any]:
    """Every position this successor authors, RENDERED: the value the artifact
    must carry is produced here, from this checker's constants and from `m`, a
    bundle of measurements taken from disk, from the pinned predecessor, from the
    live register and from this checker's own source. Nothing in `m` is read from
    the subject. The same map generates the artifact and gates it, so a leaf
    cannot exist in one and not the other."""
    flat = m["authored"]
    return {path: (eqc(value) if origin == FROM_CONSTANT else eqd(value))
            for path, (value, origin) in flat.items()}

# ------------------------------------------------------------------ compare

SHOW_LIMIT = 4000


def show(value: Any) -> str:
    """Print a compared value in full when it is short enough to be FOLLOWED,
    and mark it explicitly when it is not. rehearse_live() repairs a record by
    parsing exactly these strings, and counts any it cannot follow — so the
    ellipsis is not cosmetic, it is the boundary of the self-documenting repair
    path and it is measured."""
    text = canon(value)
    return text if len(text) <= SHOW_LIMIT else text[:SHOW_LIMIT] + "…"


def compare(path: str, payload: Any, declared: Any) -> str | None:
    # Fast path, sound for every value a LEAF position can hold. leaf_items()
    # yields scalars, None and EMPTY containers only, and for those
    # `type(a) is type(b) and a == b` implies canonical equality in both
    # directions of freeze §6 law 18 — the two cases canonical JSON separates
    # and Python equality does not, 4 against 4.0 and True against 1, are
    # exactly the cases the type test rejects first.
    if type(declared) is type(payload) and declared == payload:
        return None
    if canon(declared) == canon(payload):
        return None
    if type(declared) is not type(payload) and (
            isinstance(declared, (int, float, bool)) or
            isinstance(payload, (int, float, bool))):
        return (f"VER13-LEAFTYPE: {path} declares {declared!r} "
                f"({type(declared).__name__}); this checker measured "
                f"{payload!r} ({type(payload).__name__}). freeze §6 law 18: "
                f"closed-scalar admission is exact-type in BOTH directions")
    # Both messages END with the measured value, so a repair can be followed by
    # taking everything after the last "; this checker measured ". That is not a
    # stylistic choice: rehearse_live() repairs a record by reading exactly
    # these strings and counts every one it cannot follow.
    if path.endswith(AS_OF_SUFFIXES):
        return (f"VER13-ASOF: {path} is a RECORDED MEASUREMENT of the live "
                f"{REGISTER}, so a stale value here is a TRUE POSITIVE about "
                f"these bytes, not a false alarm about the register "
                f"(R-VER13-05). Repair in place: restate this leaf and "
                f"re-measure "
                f"{AUTHOR}.carriedByteIdentical.carriedDelta.count/.digest — a "
                f"count and a digest, so there is no index to shift. It "
                f"declares {show(declared)}; this checker measured "
                f"{show(payload)}")
    return (f"VER13-LEAF: {path} declares {show(declared)}; this checker "
            f"measured {show(payload)}")


def evaluate(value: Any, reg: dict[str, Any],
             scope: tuple[str, ...]) -> tuple[list[str], dict[str, Any]]:
    errors: list[str] = []
    items: list[tuple[str, Any]] = []
    for root in scope:
        if resolves_in(value, root):
            leaf_items(at(value, root), root, items)
        else:
            add(errors, "VER13-COVER",
                f"declared scope root {root} is absent")
    found = [path for path, _v in items]
    graded = 0
    origin = {FROM_DISK: 0, FROM_CONSTANT: 0}
    for path, declared in items:
        entry = reg.get(path)
        if entry is None:
            add(errors, "VER13-COVER",
                f"leaf position {path} has no enforcement classification — the "
                f"registry that classifies this scope is generated from checker "
                f"constants and pinned measurements, never from this artifact, "
                f"so a position it does not contain is an addition and is a "
                f"finding (B-VER10R-01)")
            continue
        _grade, _kind, payload, source = entry
        graded += 1
        origin[source] += 1
        message = compare(path, payload, declared)
        if message:
            errors.append(message)
    for path in sorted(set(reg) - set(found)):
        if any(path == root or path.startswith(root + ".") or
               path.startswith(root + "[") for root in scope):
            add(errors, "VER13-COVER",
                f"the enforcement registry expects leaf position {path}, but "
                f"the artifact does not declare it — a §7.2 recorded input or a "
                f"required residual cannot be deleted from this record")
    return errors, {
        "total": len(found), "measured": graded,
        "fromDisk": origin[FROM_DISK], "fromConstant": origin[FROM_CONSTANT],
        "positions": sorted(found),
        "digest": sha_text(canon(sorted(found))),
    }

# --------------------------------------------------------------------- probes

def inner(candidate: Any) -> list[str]:
    """Run the whole of this checker against a candidate without re-entering the
    probe layer. A non-zero exit is not evidence a guard fired, so the probes
    below read the FINDINGS, not a status."""
    global _DEPTH
    _DEPTH += 1
    try:
        return check(candidate, verify_files=False)
    finally:
        _DEPTH -= 1


def names_position(errors: list[str], position: str) -> bool:
    return any(position in e for e in errors)


def ids_naming(errors: list[str], position: str) -> str:
    return ",".join(sorted({e.split(":")[0] for e in errors
                            if position in e}))

# ------------------------------------------------------------ the closure test

def append_sweep(value: Any, sentence: str,
                 paths: list[str]) -> dict[str, Any]:
    """THE MEASUREMENT BEHIND THE CLOSURE CLAIM. Append `sentence` to every one
    of `paths` in turn — removing nothing, so every substring any comparator
    might require survives — run the WHOLE checker against each candidate, and
    count what is admitted. This is the reviewer's own experiment, run as a gate
    rather than reported as a result."""
    admitted: list[str] = []
    total = 0
    for path in paths:
        try:
            declared = at(value, path)
        except (KeyError, TypeError, ValueError):
            continue
        if not isinstance(declared, str):
            continue
        total += 1
        candidate = copy.deepcopy(value)
        set_at(candidate, path, declared + sentence)
        errors = inner(candidate)
        if not errors:
            admitted.append(path)
        elif not names_position(errors, path):
            admitted.append(f"{path} (rejected only collaterally)")
    return {"total": total, "admitted": len(admitted),
            "admittedPaths": admitted}


def authored_string_paths(value: Any) -> list[str]:
    out: list[tuple[str, str]] = []
    for root in AUTHORED_ROOTS:
        if resolves_in(value, root):
            string_leaves(at(value, root), root, out)
    return [p for p, _s in out]


def all_string_paths(value: Any) -> list[str]:
    out: list[tuple[str, str]] = []
    string_leaves(value, "", out)
    return [p.lstrip(".") for p, _s in out]


def boolean_sweep(value: Any) -> dict[str, Any]:
    """freeze §6 law 18 in the boolean direction, measured over successorRevision
    on a PLAIN run as well as under --selftest. Carried from the predecessor,
    where R-VER10-03 was closed by making the recursion guard safe."""
    found: list[str] = []
    positions(value.get("successorRevision"), "successorRevision", found)
    total = 0
    admitted: list[str] = []
    for path in found:
        declared = at(value, path)
        if not exact_bool(declared):
            continue
        total += 1
        candidate = copy.deepcopy(value)
        set_at(candidate, path, int(declared))
        errors = inner(candidate)
        if not errors:
            admitted.append(path)
        elif not names_position(errors, path):
            admitted.append(f"{path} (rejected only collaterally)")
    return {"total": total, "admitted": len(admitted),
            "admittedPaths": admitted}


def respelling_census(mutations: list[Any], subject: Any) -> dict[str, Any]:
    """Classify a mutation by the TYPE TRANSITION it performs, not by words in
    its label. Carried from the predecessor, where it repaired review O-03."""
    floats = bools = neither = 0
    label_floats = label_bools = 0
    for row in mutations:
        label, mutate = row[0], row[1]
        if "float" in label:
            label_floats += 1
        if "bool" in label or "BOOLEAN" in label:
            label_bools += 1
        candidate = copy.deepcopy(subject)
        try:
            mutate(candidate)
        except Exception:
            neither += 1
            continue
        kinds = set()
        for path in diff_leaves(candidate, subject):
            try:
                before, after = at(subject, path), at(candidate, path)
            except (KeyError, TypeError, ValueError):
                continue
            pair = (type(before).__name__, type(after).__name__)
            if pair in (("bool", "int"), ("int", "bool")):
                kinds.add("bool")
            elif pair in (("int", "float"), ("float", "int"),
                          ("bool", "float"), ("float", "bool")):
                kinds.add("float")
        if "bool" in kinds:
            bools += 1
        elif "float" in kinds:
            floats += 1
        else:
            neither += 1
    return {"total": len(mutations), "floatRespellings": floats,
            "booleanRespellings": bools, "neither": neither,
            "labelDerivedFloats": label_floats,
            "labelDerivedBooleans": label_bools}

# ---------------------------------------------------------- the deps gate

def deps_gate_probe(value: Any) -> dict[str, Any]:
    """The guard review O-02 found holding the line undeclared. Append an entry
    to decisionDependencies and MEASURE that the gate fires and that no registry
    grows.

    v12 published the probe's whole finding-id set, which made the leaf a
    function of whatever else happened to be red — under a coordinator repoint
    it grew by VER13-ASOF and became one of the 36 leaves a repoint forced an
    author to restate. What is published here is the gate's OWN signature: the
    ids the PROBE introduced, measured as a difference against the base run.
    """
    candidate = copy.deepcopy(value)
    deps = candidate.get("decisionDependencies")
    if not isinstance(deps, list):
        return {"gateFires": False, "positionsBefore": 0, "positionsAfter": 0,
                "registryGrew": False,
                "introducesTheDependencyFinding": False}
    base = inner(copy.deepcopy(value))
    before = len(LAST.get("asofPositions") or [])
    deps.append({"id": "ADVERSARIAL-PROBE",
                 "source": "artifacts/nothing.v1.json",
                 "claim": "a probe entry appended to size a registry",
                 "direction": "none", "note": "probe"})
    errors = inner(candidate)
    after = len(LAST.get("asofPositions") or [])
    return {
        "gateFires": any(e.startswith("VER13-DEP:") for e in errors),
        "positionsBefore": before,
        "positionsAfter": after,
        "registryGrew": after > before,
        # The gate's OWN signature: the dependency finding is present after the
        # probe and absent before it. v12 published the probe run's whole
        # finding-id SET, which made the leaf a function of whatever else
        # happened to be red — under a coordinator repoint it grew by
        # VER12-ASOF and became one of the 36 leaves a repoint forced an author
        # to restate, and against a red base it does not even have a fixed
        # point. What is published here is the difference the PROBE makes.
        "introducesTheDependencyFinding":
            any(e.startswith("VER13-DEP:") for e in errors) and
            not any(e.startswith("VER13-DEP:") for e in base),
    }


# ------------------------------------------------- predecessor attribution

def recorded_register_state(pred_artifact: Any,
                            live: list[Any]) -> list[Any]:
    """The register state the PINNED PREDECESSOR'S OWN RECORD names, rebuilt from
    its declared registerAsOfAudit entries. Every measurement this checker makes
    ABOUT the predecessor's behaviour is taken under this state rather than
    under the live register: what a frozen instrument did to a frozen artifact
    is a fact about those bytes, and measuring it against a register neither of
    them ever saw is what made 11 of v12's declared leaves move on a coordinator
    act that had nothing to do with them."""
    recorded: dict[str, Any] = {}
    for block in (PROSE_BLOCK, CLOSE):
        path = f"{block}.registerAsOfAudit.entries"
        if not resolves_in(pred_artifact, path):
            continue
        entries = at(pred_artifact, path)
        for row in entries if isinstance(entries, list) else []:
            if isinstance(row, dict) and row.get("registerBinding"):
                recorded.setdefault(family_of(row["registerBinding"]),
                                    row["registerBinding"])
    out = copy.deepcopy(live)
    for claim in out:
        binding = claim.get("bindingArtifact") if isinstance(claim, dict) \
            else None
        if isinstance(binding, str):
            was = recorded.get(family_of(binding))
            if was:
                claim["bindingArtifact"] = was
    return out


def transitive_modules(root: Any) -> list[Any]:
    """Every module in the predecessor's transitive set that this process has
    actually loaded.

    B-VER12R-03: v12 patched the load() of the module it imported and not the
    load() of the module THAT module executes, so under a substituted register
    the second level still read the live file, the predecessor still went red,
    and the finding survived both arms and was scored a GENUINE DEFECT —
    VER13-PRED firing unconditionally on a leaf inside pinned, frozen bytes that
    no artifact edit can reach. The substitution has to be applied at every
    level that can read the file, so the set is discovered rather than named.
    """
    seen: dict[int, Any] = {}
    frontier = [root]
    while frontier:
        current = frontier.pop()
        if id(current) in seen or not isinstance(current, types.ModuleType):
            continue
        origin = getattr(current, "__file__", None)
        if origin is None or pathlib.Path(origin).resolve().parent != HERE:
            continue
        seen[id(current)] = current
        holders: list[Any] = [vars(current)]
        cache = getattr(current, "_CACHE", None)
        if isinstance(cache, dict):
            holders.append(cache)
        for holder in holders:
            for value in list(holder.values()):
                if isinstance(value, types.ModuleType):
                    frontier.append(value)
    return sorted(seen.values(), key=lambda m: str(getattr(m, "__file__", "")))


def _run_predecessor_under(modules: list[Any], claims: list[Any],
                           pred_module: Any, pred_artifact: Any) -> list[str]:
    """Run the pinned predecessor pair with the register substituted on EVERY
    module that can read it, and restore every one of them afterwards."""
    saved = [(m, getattr(m, "load", None)) for m in modules]

    def patch(original: Any) -> Any:
        def patched(path: Any) -> Any:
            if pathlib.Path(str(path)).name == REGISTER:
                return {"claims": copy.deepcopy(claims)}
            return original(path)
        return patched

    try:
        for module_object, original in saved:
            if original is not None:
                module_object.load = patch(original)
        try:
            return pred_module.inner(copy.deepcopy(pred_artifact))
        except Exception as exc:
            return [f"{type(exc).__name__}: {exc}"]
    finally:
        for module_object, original in saved:
            if original is not None:
                module_object.load = original


def predecessor_attribution(pred_module: Any, pred_artifact: Any,
                            live: list[Any], *,
                            transitive: bool = True) -> dict[str, Any]:
    """Run the pinned predecessor pair twice — once against the register as it
    is, once against the register state its own record names — and score only a
    finding present in BOTH as a genuine defect.

    BOTH arms substitute now, symmetrically and at every level. v12 substituted
    only the second arm and only at the top level, which is why the asymmetry
    was invisible until a repoint was rehearsed against it.
    """
    modules = transitive_modules(pred_module) if transitive else [pred_module]
    as_is = _run_predecessor_under(modules, live, pred_module, pred_artifact)
    recorded = recorded_register_state(pred_artifact, live)
    as_recorded = _run_predecessor_under(modules, recorded, pred_module,
                                         pred_artifact)
    genuine = [f for f in as_is if f in set(as_recorded)]
    return {
        "findingsAgainstItsOwnBytes": len(as_is),
        "findingsUnderTheRegisterStateItRecorded": len(as_recorded),
        "findingsAttributableToACoordinatorRepoint": len(as_is) - len(genuine),
        "genuineDefects": len(genuine),
        "genuineDefectTexts": genuine,
        "modulesSubstituted": len(modules),
        "moduleNames": [pathlib.Path(getattr(m, "__file__", "?")).name
                        for m in modules],
        "method": "the pinned predecessor pair is executed twice — against the "
                  "live register and against the register state its own "
                  "registerAsOfAudit names — with the register substituted on "
                  "EVERY module in its transitive set in both arms, and only a "
                  "finding present in BOTH is a genuine defect",
    }


def attribution_probe(pred_module: Any, pred_artifact: Any,
                      live: list[Any]) -> dict[str, Any]:
    """B-VER12R-03's remedy, run as a gate rather than asserted.

    The mechanism is SILENT at today's register state — 0/0/0/0 — which is
    exactly why v12's record could not see that it was broken, so it is
    exercised in the state it exists to handle: the register is substituted to
    the documented retention-tiers head.

    The load-bearing measurement is REACH, not redness. For every module in the
    predecessor's transitive set the patched load() is CALLED on the register's
    own path and its answer is compared against the substituted binding, so the
    claim `the substitution is applied at every level that can read the file` is
    a measurement at every level rather than a property of the top one. The
    genuine-defect counts under the transitive and the top-module-only arms are
    measured beside it and both are declared; at today's state they agree,
    because the predecessor's own attribution runs only at its depth 0 while its
    nested runs read its declared bundle, and a record that reported the
    agreement as proof of a repair would be making v12's mistake in the other
    direction.
    """
    repointed = copy.deepcopy(live)
    for claim in repointed:
        if isinstance(claim, dict) and claim.get("id") == "ARCH.RETENTION-TIERS":
            claim["bindingArtifact"] = DOCUMENTED_RT_HEAD
    modules = transitive_modules(pred_module)
    reached = 0
    unreached: list[str] = []
    saved = _patch_register(modules, repointed)
    try:
        for module_object in modules:
            name = pathlib.Path(getattr(module_object, "__file__", "?")).name
            reader = getattr(module_object, "load", None)
            if reader is None:
                unreached.append(f"{name} (no load())")
                continue
            try:
                answer = reader(HERE / REGISTER)
                binding = binding_of(answer.get("claims") or [],
                                     "ARCH.RETENTION-TIERS")
            except Exception as exc:
                unreached.append(f"{name} ({type(exc).__name__})")
                continue
            if binding == DOCUMENTED_RT_HEAD:
                reached += 1
            else:
                unreached.append(f"{name} (read {binding})")
    finally:
        _restore_register(saved)
    deep = predecessor_attribution(pred_module, pred_artifact, repointed,
                                   transitive=True)
    shallow = predecessor_attribution(pred_module, pred_artifact, repointed,
                                      transitive=False)
    return {
        "substitutedRegisterTarget": DOCUMENTED_RT_HEAD,
        "modulesInTheTransitiveSet": len(modules),
        "moduleNames": [pathlib.Path(getattr(m, "__file__", "?")).name
                        for m in modules],
        "modulesWhoseLoadReturnsTheSubstitutedRegister": reached,
        "modulesTheSubstitutionDidNotReach": unreached,
        "transitiveGenuineDefects": deep["genuineDefects"],
        "transitiveFindingsAttributableToARepoint":
            deep["findingsAttributableToACoordinatorRepoint"],
        "topModuleOnlyGenuineDefects": shallow["genuineDefects"],
        "topModuleOnlyModules": 1,
    }


def rehearse_synthetic(deps: list[Any], claims: list[Any],
                       audit: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """The coupling-surface rehearsals, carried from the predecessor: they run
    against SYNTHETIC targets so the measurement is how many declared leaves are
    derived from a binding, not how far today's register happens to be from
    today's documents."""
    rt = [c for c in claims if isinstance(c, dict) and c.get("bindingArtifact")
          and family_of(c["bindingArtifact"]) == "retention-tiers"]
    variants: list[tuple[str, str, list[Any]]] = []
    repoint = copy.deepcopy(claims)
    for claim in repoint:
        if isinstance(claim, dict) and claim.get("bindingArtifact") and \
                family_of(claim["bindingArtifact"]) == "retention-tiers":
            claim["bindingArtifact"] = SENTINEL_RT
    variants.append(("ARCH.RETENTION-TIERS REPOINTED within its family",
                     "yes — R-VER10-08 enumerates a repoint", repoint))
    addition = copy.deepcopy(claims) + [
        {"id": "EVALUATION-PROOF", "bindingArtifact": SENTINEL_EP}]
    variants.append(("an EVALUATION-PROOF claim ADDED to the register",
                     "no — the residual enumerates repoints only", addition))
    ambiguity = (copy.deepcopy(claims) +
                 [{"id": "ARCH.RETENTION-TIERS-2",
                   "bindingArtifact": SENTINEL_RT}]) if rt \
        else copy.deepcopy(claims)
    variants.append(("a SECOND retention-tiers-family binding (len(hits) != 1)",
                     "no — the residual enumerates repoints only", ambiguity))
    out: list[dict[str, Any]] = []
    base = {f"entries[{r['index']}]" for r in audit}
    for event, enumerated, claim_set in variants:
        after = measure_audit(deps, claim_set)
        changed = 0
        for before_row, now in zip(audit, after):
            for field in ("registerBinding", "candidates"):
                if canon(before_row[field]) != canon(now[field]):
                    changed += 1
        out.append({
            "event": event, "enumerated": enumerated,
            "declaredLeavesThatWouldChange": changed,
            "positionsAddedOrRemoved":
                len({f"entries[{r['index']}]" for r in after} ^ base),
            "indexShifts": 0,
        })
    return out

_REPAIR_RE = re.compile(
    r"^VER13-(?:ASOF|LEAF): (\S+) .*; this checker measured (.*)$")

REHEARSAL_ROUND_LIMIT = 8
# The joint fixed point. The rehearsal's own rows are leaves of the contract, so
# a rehearsal changes what the next rehearsal measures. v12 held them at the
# artifact's declaration and never closed the loop; here it is iterated and
# whether it CLOSED is declared and compared rather than assumed.
REHEARSAL_FIXED_POINT_LIMIT = 4
# The six finding classes v12's rehearsal returned before reaching, enumerated
# from the region of _check() after its depth guard. rehearsal_reach_probe()
# drives each one and measures how many are reached on each path.
POST_GUARD_CLASSES = ("VER13-PROSE", "VER13-DEP", "VER13-PRED", "VER13-PROBE",
                      "VER13-FLOAT", "VER13-REPOINT")
# The assertions a rehearsal cannot make about itself: reachedExitZero,
# findingsNotSelfRepairing and heldFixedMembersThatMoved per row, and the joint
# fixed point's own convergence. A checker constant, declared and compared.
REHEARSAL_SELF_ASSERTIONS = 4


def _depth_zero_check(candidate: Any) -> list[str]:
    """Run the WHOLE check — every finding class, no early return — against a
    candidate whose bundle the caller has already installed.

    This is the repair of B-VER12R-02. v12's rehearsal called inner(), which
    runs at _DEPTH >= 1 and returns before six of this checker's own finding
    classes, so `this whole checker is run` was false and the declared repair
    cost was measured by an instrument that could not observe the class which
    actually blocked it.
    """
    global _DEPTH
    saved = _DEPTH
    _DEPTH = 0
    try:
        return _check(candidate, verify_files=False)
    finally:
        _DEPTH = saved


SWEEP_MEMBERS = ("sweeps", "boolSweep", "census12", "census13")


def _sweep_signature(bundle: dict[str, Any]) -> str:
    return canon([bundle.get(name) for name in SWEEP_MEMBERS])


def rehearsal_reach_probe() -> dict[str, Any]:
    """Measure — do not assert — that the rehearsal reaches the guards.

    Each of the six classes v12's rehearsal could not see is DRIVEN by
    perturbing exactly the bundle member that guard reads, and the perturbed
    bundle is then run down BOTH paths: the depth-1 path v12's rehearsal used,
    and the depth-0 path this one uses. A class that fires on neither would mean
    the probe is not an oracle; a class that fires on both would mean the guard
    was never behind the depth check. Both figures are declared and compared.
    """
    global _DERIVED, _PROBING
    subject = _CACHE.get("subject")
    if subject is None or not _DERIVED:
        return {"classes": 0, "reachedAtDepthZero": 0, "reachedAtDepthOne": 0,
                "rows": []}

    def perturb_prose(bundle: dict[str, Any]) -> None:
        bundle["sweeps"] = dict(bundle["sweeps"])
        bundle["sweeps"]["authoredAdmitted"] = 1

    def perturb_dep(bundle: dict[str, Any]) -> None:
        bundle["depsGate"] = dict(bundle["depsGate"])
        bundle["depsGate"]["gateFires"] = False

    def perturb_pred(bundle: dict[str, Any]) -> None:
        bundle["attribution"] = dict(bundle["attribution"])
        bundle["attribution"]["genuineDefects"] = 1
        bundle["attribution"]["genuineDefectTexts"] = ["a probe finding"]

    def perturb_probe(bundle: dict[str, Any]) -> None:
        rows = [dict(row) for row in bundle["probes"]]
        rows[0]["successorRejects"] = False
        bundle["probes"] = rows

    def perturb_float(bundle: dict[str, Any]) -> None:
        bundle["boolSweep"] = dict(bundle["boolSweep"])
        bundle["boolSweep"]["admitted"] = 1

    def perturb_repoint(bundle: dict[str, Any]) -> None:
        rows = [dict(row) for row in bundle["rehearsalsLive"]]
        rows[0]["reachedExitZero"] = False
        bundle["rehearsalsLive"] = rows

    plan = list(zip(POST_GUARD_CLASSES,
                    (perturb_prose, perturb_dep, perturb_pred, perturb_probe,
                     perturb_float, perturb_repoint)))
    saved = _DERIVED
    rows: list[dict[str, Any]] = []
    _PROBING += 1
    try:
        for code, perturb in plan:
            bundle = dict(saved)
            perturb(bundle)
            _DERIVED = bundle
            deep = _depth_zero_check(copy.deepcopy(subject))
            shallow = inner(copy.deepcopy(subject))
            rows.append({
                "findingClass": code,
                "firesOnTheDepthZeroPathThisRehearsalUses":
                    any(e.startswith(code + ":") for e in deep),
                "firesOnTheDepthOnePathTheV12RehearsalUsed":
                    any(e.startswith(code + ":") for e in shallow),
            })
    finally:
        _PROBING -= 1
        _DERIVED = saved
    return {
        "classes": len(rows),
        "reachedAtDepthZero":
            sum(1 for r in rows if r["firesOnTheDepthZeroPathThisRehearsalUses"]),
        "reachedAtDepthOne":
            sum(1 for r in rows
                if r["firesOnTheDepthOnePathTheV12RehearsalUsed"]),
        "rows": rows,
    }


def rehearse_live(value: Any, target: str, pred_module: Any, predecessor: Any,
                  sentences: list[dict[str, str]],
                  rows_estimate: list[dict[str, Any]], *,
                  confirm: bool = False) -> dict[str, Any]:
    """THE ARMED EVENT, REHEARSED LIVE AND IN PROCESS, WITH THE WHOLE CHECKER.

    Substitute the register, RE-DERIVE THE WHOLE BUNDLE UNDER IT, run every
    finding class this checker has, apply EXACTLY what each finding names —
    nothing else — and iterate to a fixed point. What is reported is the repair
    cost a coordinator actually pays: findings on the first round, rounds to
    exit 0, leaf edits, checker edits (0 by construction: this function never
    writes a file and never touches this checker), index shifts, and the number
    of findings whose printed repair instruction was NOT machine-followable.
    """
    global _REGISTER_OVERRIDE, _DERIVED, _REHEARSING
    claims = copy.deepcopy(register_claims())
    for claim in claims:
        if isinstance(claim, dict) and claim.get("id") == "ARCH.RETENTION-TIERS":
            claim["bindingArtifact"] = target
    saved_override = _REGISTER_OVERRIDE
    saved_derived = _DERIVED
    candidate = copy.deepcopy(value)
    first_findings = 0
    first_ids = ""
    edits: list[str] = []
    classes: set[str] = set()
    rounds = 0
    green = False
    unfollowable = 0
    _REHEARSING += 1
    try:
        _REGISTER_OVERRIDE = claims
        # The whole bundle, re-measured under the register in force. This is
        # what v12 did not do: it reused a bundle measured against the
        # UNREPOINTED register, so 27 leaves that genuinely move compared equal
        # inside the rehearsal and could never surface as a finding.
        # The base bundle under a given substituted register is a property of
        # the subject and that register, not of the joint fixed point's current
        # estimate, so it is measured once per target and reused across the
        # iterations. What is NOT assumed is that the members it holds fixed
        # stay fixed: `confirm` re-measures them against the repaired candidate
        # and the difference is a compared leaf.
        key = f"rehearsalBase:{target}"
        if key not in _CACHE:
            _CACHE[key] = derive(value, pred_module, predecessor, sentences)
        base = _CACHE[key]
        signature_before = _sweep_signature(base)
        while rounds < REHEARSAL_ROUND_LIMIT:
            bundle = dict(base)
            bundle["depsGate"] = deps_gate_probe(candidate)
            bundle["probes"] = measure_probes(pred_module, predecessor,
                                              candidate, sentences)
            bundle["rehearsalsLive"] = rows_estimate
            _DERIVED = bundle
            errors = _depth_zero_check(candidate)
            classes.update(e.split(":")[0] for e in errors)
            if rounds == 0:
                first_findings = len(errors)
                first_ids = ",".join(sorted({e.split(":")[0] for e in errors}))
            if not errors:
                green = True
                break
            rounds += 1
            progressed = False
            for error in errors:
                hit = _REPAIR_RE.match(error)
                if hit is None:
                    continue
                path, now = hit.group(1), hit.group(2).strip()
                if now.endswith("…") or not resolves_in(candidate, path):
                    continue
                try:
                    replacement, _problems = jloads(now, "rehearsal-repair")
                except ValueError:
                    continue
                set_at(candidate, path, replacement)
                edits.append(path)
                progressed = True
            if not progressed:
                break
        # What could NOT be followed is measured at the FIXED POINT, not on the
        # way to it: a finding a later round repairs was followable, it simply
        # had a prerequisite.
        if not green:
            bundle = dict(base)
            bundle["depsGate"] = deps_gate_probe(candidate)
            bundle["probes"] = measure_probes(pred_module, predecessor,
                                              candidate, sentences)
            bundle["rehearsalsLive"] = rows_estimate
            _DERIVED = bundle
            unfollowable = len(_depth_zero_check(candidate))
        # The members held fixed across the rounds are re-measured against the
        # REPAIRED candidate and compared, so "held fixed" is a measurement
        # rather than an assumption. This is the half of O-04 that survives even
        # when the depth guard is removed.
        if confirm:
            final = derive(candidate, pred_module, predecessor, sentences)
            signature_after = _sweep_signature(final)
        else:
            signature_after = signature_before
    finally:
        _REHEARSING -= 1
        _REGISTER_OVERRIDE = saved_override
        _DERIVED = saved_derived
    moved = diff_leaves(candidate, value)
    return {
        "target": target,
        "findings": first_findings,
        "findingIds": first_ids,
        "roundsToGreen": rounds,
        "leafEdits": len(set(edits)),
        "editedPaths": sorted(set(edits)),
        "checkerEdits": 0,
        "indexShifts": 0,
        "positionsAddedOrRemoved": len([p for p in moved
                                        if not resolves_in(value, p)]),
        "findingsNotSelfRepairing": unfollowable,
        "reachedExitZero": green,
        "findingClassesDriven": ",".join(sorted(classes)),
        "heldFixedMembersThatMoved":
            0 if signature_before == signature_after else 1,
    }


def rehearse_all(value: Any, pred_module: Any, predecessor: Any,
                 sentences: list[dict[str, str]],
                 declared: list[dict[str, Any]]) -> dict[str, Any]:
    """The JOINT fixed point over the candidate AND the rehearsal's own rows.

    repointRehearsals.live[*] are leaves of this contract, so what a rehearsal
    measures depends on what the previous rehearsal declared. v12 left that loop
    open and the reviewer's on-disk run closed it for it, at 4 rounds and 36
    leaf edits against a declared 2 and 9. Here it is iterated until the rows
    stop moving, and whether it converged is itself a compared leaf.
    """
    # The convergence test compares the rows a rehearsal PRODUCES against the
    # rows it was GIVEN. Two members are excluded because they are not part of
    # that question: editedPaths, which is a list this contract does not carry,
    # and heldFixedMembersThatMoved, which only the confirming pass measures —
    # comparing a measured value against the placeholder the unconfirmed passes
    # carry would make the loop report `did not converge` forever, which is a
    # self-fulfilling verdict rather than a measurement.
    skip = ("editedPaths", "heldFixedMembersThatMoved")

    def strip(rows_in: list[dict[str, Any]]) -> str:
        return canon([{k: v for k, v in row.items() if k not in skip}
                      for row in rows_in])

    rows = [dict(row) for row in declared]
    iterations = 0
    converged = False
    while iterations < REHEARSAL_FIXED_POINT_LIMIT:
        iterations += 1
        produced = [rehearse_live(value, target, pred_module, predecessor,
                                  sentences, rows)
                    for target in LIVE_REPOINT_TARGETS]
        if strip(produced) == strip(rows):
            converged = True
            rows = produced
            break
        rows = produced
    # One further pass at the fixed point with the held-fixed members
    # re-measured against the repaired candidate, so "held fixed" is a
    # measurement rather than an assumption (review O-04).
    confirmed = [rehearse_live(value, target, pred_module, predecessor,
                               sentences, rows, confirm=True)
                 for target in LIVE_REPOINT_TARGETS]
    if strip(confirmed) != strip(rows):
        converged = False
    return {"rows": confirmed, "iterations": iterations,
            "converged": converged}


# --------------------------------------------------------------- the probes

def probe_pairs(pred_module: Any, pred_artifact: Any, subject: Any,
                sentences: list[dict[str, str]]) -> list[dict[str, Any]]:
    """The demonstrations, executed on every run against BOTH the pinned
    predecessor pair and these bytes. The predecessor arm runs under the
    register state the predecessor's own record names — see
    recorded_register_state() — so what it measures is a property of two frozen
    files rather than of today's coordinator state."""
    last = len(subject.get("knownLimitations") or []) - 1
    pred_last = len(pred_artifact.get("knownLimitations") or []) - 1
    plan = [
        ("plant a re-worded verdict-inheritance claim in top-level role",
         "role", "role", sentences[0]["sentence"]),
        ("plant a re-worded acceptance claim in the last knownLimitation",
         f"knownLimitations[{pred_last}]", f"knownLimitations[{last}]",
         sentences[2]["sentence"]),
        ("plant a re-worded discharge claim in a retained residual",
         f"{PROSE_BLOCK}.retainedResiduals[0].residual",
         f"{AUTHOR}.retainedResiduals[0].residual", sentences[3]["sentence"]),
        ("plant a re-worded claim in the successor identity-stability reason",
         "successorRevision.identityStability.reason",
         "successorRevision.identityStability.reason",
         sentences[4]["sentence"]),
        ("append a materially false sentence carrying NO assurance vocabulary",
         f"{PROSE_BLOCK}.notClaimed[0]", f"{AUTHOR}.notClaimed[0]",
         NEUTRAL_APPEND.strip()),
        ("CONTROL — append the predecessor's own seal wording, the one the "
         "carried pattern table contains",
         f"{PROSE_BLOCK}.notClaimed[0]", f"{AUTHOR}.notClaimed[0]",
         PREDECESSOR_SEAL_APPEND.strip()),
    ]
    out: list[dict[str, Any]] = []
    for probe, pred_path, self_path, sentence in plan:
        pred_admitted = None
        pred_findings = None
        candidate = copy.deepcopy(pred_artifact)
        if resolves_in(candidate, pred_path) and \
                isinstance(at(candidate, pred_path), str):
            set_at(candidate, pred_path,
                   at(candidate, pred_path) + " " + sentence)
            try:
                errors = pred_module.inner(candidate)
            except Exception as exc:
                errors = [f"{type(exc).__name__}: {exc}"]
            pred_admitted = not errors
            pred_findings = len(errors)
        mine = copy.deepcopy(subject)
        self_errors: list[str] = []
        if resolves_in(mine, self_path) and isinstance(at(mine, self_path), str):
            set_at(mine, self_path, at(mine, self_path) + " " + sentence)
            self_errors = inner(mine)
        out.append({
            "probe": probe,
            "positionInThePredecessor": pred_path,
            "position": self_path,
            "predecessorAdmitted": pred_admitted,
            "predecessorFindings": pred_findings,
            "successorRejects": bool(self_errors),
            "successorNamesThePosition": names_position(self_errors, self_path),
            "successorFindingIds": ids_naming(self_errors, self_path),
        })
    return out


def probe_positions(value: Any) -> list[str]:
    """One string position from each prose-authority class and each authored and
    carried sub-block, so the test-set cross product is measured ACROSS the
    partition rather than at one convenient leaf. A checker constant except for
    the last knownLimitation index, which is derived from the pinned
    predecessor's count plus the declared addition count."""
    last = len(pinned(PREDECESSOR).get("knownLimitations") or []) + \
        ADDED_LIMITATION_COUNT - 1
    return [
        "role",
        "knownLimitations[0]",
        f"knownLimitations[{last}]",
        "successorRevision.identityStability.reason",
        f"{AUTHOR}.notClaimed[0]",
        f"{AUTHOR}.retainedResiduals[0].residual",
        f"{AUTHOR}.byteVersusModelClosure.rule",
        f"{AUTHOR}.checkerDisposition.scopeOfThatBoolean",
        f"{PROSE_BLOCK}.notClaimed[0]",
        f"{PROSE_BLOCK}.proseAuthorityPartition.rule",
        f"{CLOSE}.prosePaperSealScan.rule",
        f"{REPAIR}.siblingCitationAudit.method",
        "purpose",
    ]


def predecessor_authored_paths(pred: Any) -> list[str]:
    """The predecessor's own authored surface: the positions IT could author
    into. Sweeping this measures the blast radius of the predecessor's residual
    on the same axis this record reports for itself."""
    out: list[tuple[str, str]] = []
    for root in ("role", "knownLimitations",
                 "successorRevision.identityStability", PROSE_BLOCK):
        if resolves_in(pred, root):
            string_leaves(at(pred, root), root, out)
    return [p for p, _s in out]


def measure_probes(pred_module: Any, predecessor: Any, candidate: Any,
                   sentences: list[dict[str, str]]) -> list[dict[str, Any]]:
    """probe_pairs() with the predecessor arm always run under the register
    state the predecessor's own record names. Every caller goes through here, so
    a demonstration cannot mean one thing at depth 0 and another inside a
    rehearsal."""
    modules = transitive_modules(pred_module)
    recorded = recorded_register_state(predecessor, register_claims())
    saved = _patch_register(modules, recorded)
    try:
        return probe_pairs(pred_module, predecessor, candidate, sentences)
    finally:
        _restore_register(saved)


def _patch_register(modules: list[Any], claims: list[Any]) -> list[Any]:
    saved = [(m, getattr(m, "load", None)) for m in modules]

    def patch(original: Any) -> Any:
        def patched(path: Any) -> Any:
            if pathlib.Path(str(path)).name == REGISTER:
                return {"claims": copy.deepcopy(claims)}
            return original(path)
        return patched

    for module_object, original in saved:
        if original is not None:
            module_object.load = patch(original)
    return saved


def _restore_register(saved: list[Any]) -> None:
    for module_object, original in saved:
        if original is not None:
            module_object.load = original


ADDED_LIMITATION_COUNT = 5

V13_REQUIRED_INPUTS = (
    (PREDECESSOR,
     "protected predecessor; every position outside "
     "successorRevision.parseAuthorityRepair, role, knownLimitations and the "
     "three successor-identity leaves is carried from these bytes and gated "
     "against them leaf-wise, including the whole of proseAuthorityRepair"),
    (PREDECESSOR_CHECKER,
     "predecessor checker; the subject of blockers B-VER12R-01, B-VER12R-02 "
     "and B-VER12R-03, executed by this checker on every run to reproduce the "
     "admissions and to measure the evasion rates of its parse, its rehearsal "
     "and its AST purity measure"),
    (PREDECESSOR_REVIEW,
     "the independent verdict that binds the v12 bytes; the two bare-token "
     "wordings, the five AST constructions, the three planted seal positions, "
     "the blast radius and the reviewer's own on-disk repoint table are READ "
     "FROM THIS FILE rather than retyped"),
    (GRANDPARENT,
     "the v11 bytes the carried prose-authority record is measured against"),
    (GRANDPARENT_CHECKER,
     "the v11 checker, executed transitively by the predecessor checker on "
     "every run; THE MODULE WHOSE load() B-VER12R-03 showed was not patched"),
    (GRANDPARENT_REVIEW,
     "the v11 independent verdict, whose four planted wordings are read from "
     "these bytes as this checker's own test set"),
    (ELDER,
     "the v10 bytes the carried enforcement record is measured against"),
    (ELDER_CHECKER,
     "the v10 checker, executed transitively at the second level below the "
     "predecessor"),
    (ELDER_REVIEW,
     "the v10 independent verdict, whose B-VER10R-01 the chain closed"),
    (GREAT_ELDER,
     "the v9 bytes the carried d9 citation repair record is measured against"),
    (GREAT_ELDER_CHECKER,
     "the v9 checker; retained as historical evidence of what was enforced "
     "when v9 was reviewed, not repaired"),
    (D9_SUPERSEDED,
     "superseded citation endpoint of the span the carried record measures"),
    (D9_HEAD,
     "repaired citation target and the live register's D9 binding"),
    (D9_HEAD_CHECKER,
     "executed on every run; the D9 head dependency must be green for this "
     "record to be green, and the adjacent instrument that already closed "
     "B-VER12R-01's class with an object_pairs_hook"),
    (V4,
     "the artifact check-versioning.py is hardcoded to and whose D9 citation "
     "is frozen by §7.2"),
    (V4_CHECKER,
     "permanently red by construction; recorded because its AttributeError "
     "exits 1 indistinguishably from a finding"),
)

RESIDUAL_OWNERS = {
    "R-VER13-01": "phase1a parse-authority lane",
    "R-VER13-02": "phase1a parse-authority lane",
    "R-VER13-03": "phase1a parse-authority lane",
    "R-VER13-04": "phase1a parse-authority lane",
    "R-VER13-05": "independent reviewer",
    "R-VER13-06": "coordinator",
    "R-VER13-07": "coordinator",
    "R-VER13-08": "coordinator",
    "R-VER13-09": "independent reviewer",
    "R-VER13-10": "phase1a parse-authority lane",
    "R-VER13-11": "phase1a parse-authority lane",
}


def put(flat: dict[str, tuple[Any, str]], path: str, value: Any,
        origin: str = FROM_CONSTANT) -> None:
    flat[path] = (value, origin)


def minus(left: Any, right: Any) -> Any:
    """The bootstrap bundle carries Nones where a measurement has not been taken
    yet, so arithmetic inside a rendered sentence must survive them. Nothing the
    bootstrap renders ever gates anything; see declared_derivation()."""
    if exact_int(left) and exact_int(right):
        return left - right
    return None


# ------------------------------------------------- the parse/byte machinery

# ------------------------------------------------- the parse-site scan (L8)
# OBS-C2V7-01 in this lineage: a scan that matches an ast.Call whose func is a
# Name or Attribute spelled load/loads cannot see json.JSONDecoder().decode(t),
# getattr(json, "loads")(t), json.__dict__["loads"](t) or an attribute alias
# assigned and then called. All four are real, bare, unhooked parses. They are
# counted here and required to be zero, and the detector is PROBED first,
# because a count of zero over this file is otherwise indistinguishable from a
# detector that sees nothing.
PARSE_EVASION_ATTRIBUTES = ("JSONDecoder", "raw_decode", "scanstring")
PARSE_EVASION_NAMES = ("load", "loads", "JSONDecoder", "raw_decode")
PARSE_EVASION_DETECTOR_PROBE = (
    "value = json.JSONDecoder().decode(text)\n"
    "other = getattr(json, 'loads')(text)\n"
    "third = json.__dict__['loads'](text)\n"
    "alias = json.loads\n"
    "fourth = alias(text)\n"
    "fifth = json.decoder.scanstring(text, 0)\n"
    "sixth = getattr(other_module, 'loads')(text)\n")


def json_load_sites(tree: ast.AST) -> list[dict[str, Any]]:
    """Every json.load/json.loads call, and whether it passes a real hook.

    The property is asserted over the whole tree rather than over an
    enumeration: a parse that refuses duplicate keys at ONE call site and not at
    its siblings is exactly the failure B-VER12R-01 exploited. Passing
    object_pairs_hook=None is NOT a hook — it is the host default spelled out —
    and is counted as bare, so the exemption cannot be bought with a keyword.
    """
    out: list[dict[str, Any]] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        name = None
        if isinstance(node.func, ast.Attribute):
            name = node.func.attr
        elif isinstance(node.func, ast.Name):
            name = node.func.id
        if name not in ("load", "loads"):
            continue
        hooked = False
        for keyword in node.keywords:
            if keyword.arg != "object_pairs_hook":
                continue
            if isinstance(keyword.value, ast.Constant) and \
                    keyword.value.value is None:
                continue
            hooked = True
        out.append({"line": getattr(node, "lineno", 0),
                    "source": ast.unparse(node)[:160], "hooked": hooked})
    return out


def _root_name(node: ast.AST) -> str | None:
    current = node
    while isinstance(current, ast.Attribute):
        current = current.value
    return current.id if isinstance(current, ast.Name) else None


def json_parse_evasion_sites(tree: ast.AST) -> list[dict[str, Any]]:
    """Every syntactic route to the JSON decoder that json_load_sites() cannot
    see, with its position. Four shapes, of which the last two were left OPEN by
    the adjacent lineage's own review and are closed here."""
    out: list[dict[str, Any]] = []
    for node in ast.walk(tree):
        name = None
        if isinstance(node, ast.Attribute):
            name = node.attr
        elif isinstance(node, ast.Name):
            name = node.id
        if name in PARSE_EVASION_ATTRIBUTES:
            out.append({"line": getattr(node, "lineno", 0),
                        "kind": "decoder-object",
                        "source": ast.unparse(node)[:160]})
            continue
        if isinstance(node, ast.Subscript) and \
                isinstance(node.slice, ast.Constant) and \
                isinstance(node.slice.value, str) and \
                node.slice.value in PARSE_EVASION_NAMES and \
                isinstance(node.value, ast.Attribute) and \
                node.value.attr == "__dict__":
            out.append({"line": getattr(node, "lineno", 0),
                        "kind": "dict-subscript",
                        "source": ast.unparse(node)[:160]})
            continue
        if isinstance(node, ast.Assign) and isinstance(node.value,
                                                       ast.Attribute) and \
                node.value.attr in ("load", "loads"):
            out.append({"line": getattr(node, "lineno", 0),
                        "kind": "attribute-alias",
                        "source": ast.unparse(node)[:160]})
            continue
        if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Name):
            continue
        if node.func.id != "getattr" or len(node.args) < 2:
            continue
        target = node.args[1]
        if not isinstance(target, ast.Constant) or \
                target.value not in PARSE_EVASION_NAMES:
            continue
        # `loads`, `JSONDecoder` and `raw_decode` name the host decoder whatever
        # object they are fetched from, so any getattr for them is a dispatch.
        # `load` is an ordinary attribute name — this file fetches the pinned
        # predecessor's own load() by that name to substitute the register — so
        # it counts only when the object is rooted at the json module. That
        # narrowing is a boundary, and R-VER13-03 states it.
        rooted = _root_name(node.args[0]) == "json"
        if target.value != "load" or rooted:
            out.append({"line": getattr(node, "lineno", 0),
                        "kind": "getattr-dispatch",
                        "source": ast.unparse(node)[:160]})
    return out


def parse_site_scan() -> dict[str, Any]:
    """The structural half of the B-VER12R-01 repair, over this file and over
    the pinned predecessor, so the differential shows what the predecessor's
    parse could not see rather than only asserting that this one is better."""
    if "parseScan" in _CACHE:
        return _CACHE["parseScan"]
    own = ast.parse((HERE / pathlib.Path(__file__).name).read_text())
    sites = json_load_sites(own)
    evasions = json_parse_evasion_sites(own)
    ungated = [row for row in sites if not row["hooked"]]
    probe = json_parse_evasion_sites(ast.parse(PARSE_EVASION_DETECTOR_PROBE))
    pred_tree = ast.parse((HERE / PREDECESSOR_CHECKER).read_text())
    pred_sites = json_load_sites(pred_tree)
    _CACHE["parseScan"] = {
        "sites": len(sites), "hooked": sum(1 for r in sites if r["hooked"]),
        "ungated": ungated, "ungatedCount": len(ungated),
        "evasions": evasions, "evasionCount": len(evasions),
        "detectorProbeSites": len(probe),
        "detectorProbeKinds": sorted({r["kind"] for r in probe}),
        "predecessorSites": len(pred_sites),
        "predecessorHooked": sum(1 for r in pred_sites if r["hooked"]),
        "predecessorUngated": sum(1 for r in pred_sites if not r["hooked"]),
    }
    return _CACHE["parseScan"]


# --------------------------------------------- the bytes of record (VER13-BYTES)

def serialise(value: Any) -> str:
    """The ONE byte string this checker admits for a value. Every degree of
    freedom the JSON grammar leaves open — key order, duplicate names, number
    spelling, escape spelling, whitespace — is removed here rather than policed
    downstream, which is why B-VER12R-01's class is unrepresentable in a
    conforming file rather than merely detectable in one."""
    return json.dumps(value, indent=SERIALISATION_INDENT,
                      ensure_ascii=SERIALISATION_ENSURE_ASCII) + \
        SERIALISATION_TRAILER


def reconstruct(flat: dict[str, Any], predecessor: Any) -> Any:
    """Rebuild the WHOLE contract from this checker and the SHA-verified pinned
    predecessor, and from nothing else.

    review O-06 recorded that v12 achieved total derivability of the parsed
    value and did not claim it. It is claimed here, at the BYTE level, because
    that is what closes B-VER13R-01's own residual: the artifact is not compared
    against the reconstruction leaf by leaf only — its FILE is compared against
    the reconstruction's serialisation. A reconstruction is built by nest() from
    a flat path->value map, so it cannot contain a duplicate key at all.
    """
    authored_tree = nest(dict(flat))
    out: dict[str, Any] = {}
    for key in predecessor:
        if key == "successorRevision":
            revision: dict[str, Any] = {}
            source = predecessor.get("successorRevision") or {}
            authored_revision = (authored_tree.get("successorRevision") or {})
            for name in source:
                revision[name] = authored_revision[name] \
                    if name in authored_revision else copy.deepcopy(source[name])
            for name in authored_revision:
                if name not in revision:
                    revision[name] = authored_revision[name]
            out[key] = revision
        elif key in authored_tree:
            out[key] = authored_tree[key]
        else:
            out[key] = copy.deepcopy(predecessor[key])
    for key in authored_tree:
        if key not in out:
            out[key] = authored_tree[key]
    return out


def first_difference(left: str, right: str) -> dict[str, Any]:
    limit = min(len(left), len(right))
    offset = limit
    for index in range(limit):
        if left[index] != right[index]:
            offset = index
            break
    return {"offset": offset,
            "onDisk": left[max(0, offset - 60):offset + 60],
            "reconstructed": right[max(0, offset - 60):offset + 60]}


def byte_gate(reconstruction: Any) -> dict[str, Any]:
    """Compare the FILE against the serialisation of the reconstruction.

    This is measured against the path this run was given, once per process, and
    it is a statement about the artifact of record rather than about a value
    some caller passed in — which is the whole of B-VER12R-01: the closure was
    defined over the parsed data model and the artifact of record is the file.
    """
    try:
        text = _SUBJECT_PATH.read_text()
        raw = _SUBJECT_PATH.read_bytes()
    except OSError as exc:
        return {"readable": False, "equal": False, "detail": str(exc),
                "subjectBytes": 0, "reconstructedBytes": 0,
                "subjectSha256": "", "reconstructionSha256": "",
                "difference": {"offset": 0, "onDisk": "", "reconstructed": ""}}
    expected = serialise(reconstruction)
    equal = text == expected
    return {
        "readable": True,
        "equal": equal,
        "subjectBytes": len(raw),
        "reconstructedBytes": len(expected.encode("utf-8")),
        "subjectSha256": hashlib.sha256(raw).hexdigest(),
        "reconstructionSha256":
            hashlib.sha256(expected.encode("utf-8")).hexdigest(),
        "difference": {"offset": -1, "onDisk": "", "reconstructed": ""}
        if equal else first_difference(text, expected),
    }

# Every JSON input this verdict depends on, parsed through jloads() whether or
# not it is the candidate. B-VER12R-01's remedy is not "guard the subject": a
# defence applied to one input and not to its siblings is the list-of-places
# failure this lineage exists to escape.
PARSED_INPUTS = (PREDECESSOR, PREDECESSOR_REVIEW, GRANDPARENT,
                 GRANDPARENT_REVIEW, ELDER, ELDER_REVIEW, GREAT_ELDER,
                 D9_HEAD, D9_SUPERSEDED, V4)
# A text carrying one of each divergence the census reports. A census of 0 over
# clean inputs is indistinguishable from an instrument that detects nothing, so
# the instrument is driven before its 0 is published.
PARSE_ORACLE_TEXT = '{"a": 1, "a": 2, "b": 1.0, "c": [{"d": -0}], "e": NaN}'
PARSE_ORACLE_KINDS = ("duplicate-key", "non-rfc-constant", "number-text")


def parse_census() -> dict[str, Any]:
    """Every way the BYTES and the PARSE disagree, across every JSON input, each
    named at its own position. The texts are read here rather than taken from
    whatever this process happened to parse, so the census is a property of the
    inputs and not of the call order."""
    if "parseCensus" in _CACHE:
        return _CACHE["parseCensus"]
    targets: list[tuple[str, pathlib.Path]] = [
        (f"pinned:{name}", HERE / name) for name in PARSED_INPUTS]
    targets.append((f"register:{REGISTER}", HERE / REGISTER))
    targets.append((f"subject:{_SUBJECT_PATH.name}", _SUBJECT_PATH))
    rows: list[dict[str, str]] = []
    labels: list[str] = []
    for label, path in targets:
        try:
            text = path.read_text()
        except OSError:
            continue
        labels.append(label)
        try:
            _value, problems = jloads(text, label)
        except ValueError as exc:
            rows.append({"input": label, "kind": "unparseable",
                         "position": "<document>", "key": "",
                         "detail": f"did not parse: {type(exc).__name__}: {exc}"})
            continue
        for problem in problems:
            rows.append({"input": label, "kind": problem["kind"],
                         "position": problem["path"], "key": problem["key"],
                         "detail": problem["detail"]})
    _value, oracle = jloads(PARSE_ORACLE_TEXT, "oracle")
    _PARSES.pop("oracle", None)
    _CACHE["parseCensus"] = {
        "inputs": len(labels),
        "inputLabels": labels,
        "problems": rows,
        "duplicateKeys": sum(1 for r in rows if r["kind"] == "duplicate-key"),
        "nonRfcConstants":
            sum(1 for r in rows if r["kind"] == "non-rfc-constant"),
        "nonCanonicalNumberTokens":
            sum(1 for r in rows if r["kind"] == "number-text"),
        "oracleProblems": len(oracle),
        "oracleKinds": sorted({p["kind"] for p in oracle}),
        "oracleNamesTheDuplicateAtItsPath":
            any(p["kind"] == "duplicate-key" and p["path"] == "a"
                for p in oracle),
    }
    return _CACHE["parseCensus"]


def subject_is_the_file(value: Any) -> bool:
    """True when the candidate under test IS the parse of the artifact of
    record. The byte gate is a statement about a FILE, so it is measured once,
    against the file, and reused rather than re-asked of every in-memory
    candidate a probe constructs."""
    key = "subjectCanon"
    if key not in _CACHE:
        try:
            _CACHE[key] = canon(jload_path(_SUBJECT_PATH,
                                           f"subject:{_SUBJECT_PATH.name}"))
        except Exception:
            _CACHE[key] = None
    return _CACHE[key] is not None and canon(value) == _CACHE[key]


# ----------------------------------------------------- the rendered content

def authored(m: dict[str, Any]) -> dict[str, tuple[Any, str]]:
    """Every position this successor authors, rendered from this checker's own
    constants and its own measurements. The same map generates the artifact and
    gates it, and reconstruct() turns it into the FILE: there is no free-prose
    position anywhere in this block and no byte of the artifact that is not
    produced here or carried from SHA-verified pinned bytes."""
    f: dict[str, tuple[Any, str]] = {}
    review = m["review12"]
    pur = m["purity"]
    census = m["census"]
    parts = m["partitions"]
    prose = m["prose"]
    lint = m["lint"]
    sweeps = m["sweeps"]
    rows = m["sentences"]
    probes = m["probes"]
    attr = m["attribution"]
    probe = m["attributionProbe"]
    live = m["rehearsalsLive"]
    synth = m["rehearsalsSynthetic"]
    gate = m["depsGate"]
    scan = m["parseScan"]
    parses = m["parseCensus"]
    bytes_of_record = m["byteGate"]
    reach = m["reach"]
    fidelity = m["fidelity"]
    pred_limits = len(pinned(PREDECESSOR).get("knownLimitations") or [])
    a = AUTHOR

    # ---- identity, top level ------------------------------------------------
    put(f, "version", 13)
    put(f, "supersedes", 12)
    put(f, "role",
        "A-prime v5 parse-authority successor; the v12 prose-authority record "
        "is carried byte-identical and gated leaf-wise against those bytes, "
        "B-VER12R-01 is closed by removing the gap the duplicate key lived in "
        "rather than by policing it — the FILE is compared against the "
        "serialisation of a reconstruction this checker builds from its own "
        "constants and the pinned predecessor — and B-VER12R-02 and B-VER12R-03 "
        "are closed by running the repoint rehearsal at depth-0 semantics and "
        "by substituting the register on every module in the predecessor's "
        "transitive set, both of which are measured by an oracle probe rather "
        "than asserted")
    for index in range(pred_limits):
        put(f, f"knownLimitations[{index}]",
            pinned(PREDECESSOR)["knownLimitations"][index], FROM_DISK)
    added = [
        f"The artifact of record is the FILE, and v12's closure was defined "
        f"over the parsed data model. json.loads keeps the LAST duplicate key "
        f"and nothing re-serialised the subject's bytes, so the independent "
        f"reviewer planted {review['plantedSealsAdmitted']} of "
        f"{review['plantedSealsAttempted']} paper seals at exit 0 with a "
        f"ONE-FILE, artifact-only edit — including into top-level role and into "
        f"the sentence that stated the closure — across "
        f"{review['blastRadiusObjects']} admitting objects. In v13 the file's "
        f"bytes must equal json.dumps of a reconstruction at indent "
        f"{SERIALISATION_INDENT}, and every JSON input is parsed through one "
        f"primitive that carries the duplicate-key hook: "
        f"{parses['duplicateKeys']} duplicate keys, "
        f"{parses['nonRfcConstants']} non-RFC constants and "
        f"{parses['nonCanonicalNumberTokens']} non-canonical number tokens "
        f"across {parses['inputs']} parsed inputs.",
        f"The residual v12 published pointed one layer away from the live "
        f"hazard. It stated the surface as an EDIT COST — two files rather than "
        f"one — and the reviewer falsified it with a one-file edit at the "
        f"PARSE. The boundary is stated here where it lives: every byte of this "
        f"contract is either produced by check-versioning-v13.py or carried "
        f"from SHA-verified pinned bytes, the two are composed by one "
        f"serialisation, and what remains open is not an edit count but the "
        f"instrument itself — {prose['rendered']} RENDERED string leaves whose "
        f"content is fixed rather than verified.",
        f"The repoint rehearsal did not run the checker it named. v12's "
        f"rehearse_live called inner() at depth 1, which returns before "
        f"{len(POST_GUARD_CLASSES)} finding classes, and reused a bundle "
        f"measured against the unrepointed register: it declared "
        f"{review['rehearsal'][0]['declaredFindings'] if review['rehearsal'] else None} "
        f"findings and "
        f"{review['rehearsal'][0]['declaredLeafEdits'] if review['rehearsal'] else None} "
        f"leaf edits for v23 where the reviewer measured "
        f"{review['rehearsal'][0]['measuredFindings'] if review['rehearsal'] else None} "
        f"and "
        f"{review['rehearsal'][0]['measuredLeafEdits'] if review['rehearsal'] else None} "
        f"on disk, and did not reach exit 0 at all. Here the rehearsal runs "
        f"every class: measured on the depth-0 path this rehearsal uses, "
        f"{reach['reachedAtDepthZero']} of {reach['classes']} of those guards "
        f"fire, against {reach['reachedAtDepthOne']} of {reach['classes']} on "
        f"the depth-1 path v12 used.",
        f"The register substitution reached one level only. v12 patched the "
        f"predecessor's load() and not the load() of the module the "
        f"predecessor executes transitively, so a repoint left "
        f"{review['attributionAfterARepoint']['genuineDefects']} false genuine "
        f"defect on a leaf inside pinned, frozen bytes no artifact edit can "
        f"reach. The substitution is applied here to "
        f"{attr['modulesSubstituted']} modules discovered from the "
        f"predecessor's transitive set rather than named, and it is measured at "
        f"every level: under a register substituted to the documented head, "
        f"{probe['modulesWhoseLoadReturnsTheSubstitutedRegister']} of "
        f"{probe['modulesInTheTransitiveSet']} modules' load() returns the "
        f"substituted binding and "
        f"{len(probe['modulesTheSubstitutionDidNotReach'])} do not. The "
        f"redness arms are reported beside it and they agree at "
        f"{probe['transitiveGenuineDefects']} and "
        f"{probe['topModuleOnlyGenuineDefects']}, which is why reach and not "
        f"redness is what this record rests on.",
        f"The AST purity measure walked For, AsyncFor and comprehension only, "
        f"so a while loop sized from a parameter reported loopCount 0 — it did "
        f"not see a loop at all — and registryPurity.theGate's sentence was "
        f"false as written. Measured on every run: the predecessor's measure "
        f"catches {pur['reviewerSuiteCaughtByThePredecessorAstMeasure']} of "
        f"{pur['reviewerSuiteAttempted']} of the reviewer's constructions and "
        f"the widened measure catches "
        f"{pur['reviewerSuiteCaughtByTheWidenedAstMeasure']}. Its own boundary "
        f"is published rather than left implied: a further suite of "
        f"{pur['widenedSuiteAttempted']} constructions written against the "
        f"WIDENED measure is caught at "
        f"{pur['widenedSuiteCaughtByTheWidenedAstMeasure']} of "
        f"{pur['widenedSuiteAttempted']}.",
    ]
    for offset, text in enumerate(added):
        put(f, f"knownLimitations[{pred_limits + offset}]", text, FROM_DISK)

    put(f, "successorRevision.id",
        "VERSIONING-v13-PARSE-AUTHORITY-SUCCESSOR")
    put(f, "successorRevision.supersedesCandidate.artifact", PREDECESSOR)
    put(f, "successorRevision.supersedesCandidate.sha256", PINS[PREDECESSOR],
        FROM_DISK)
    put(f, "successorRevision.supersedesCandidate.checker", PREDECESSOR_CHECKER)
    put(f, "successorRevision.supersedesCandidate.checkerSha256",
        PINS[PREDECESSOR_CHECKER], FROM_DISK)
    put(f, "successorRevision.identityStability.predecessor", "VERSIONING-v12")
    put(f, "successorRevision.identityStability.state",
        "EXACT-CUSTODY-IDENTITIES-UNCHANGED")
    put(f, "successorRevision.identityStability.reason",
        f"B-VER12R-01, B-VER12R-02 and B-VER12R-03 are defects of the "
        f"enforcement instrument and of the layer beneath it, not of any "
        f"custody identity. No custodyClass, versionedIdentity, rule, "
        f"supportWindow or migrator moves in v13; {prose['carried']} of the "
        f"{prose['stringLeaves']} string leaves in this contract are held "
        f"byte-identical against versioning-policy.v12.json.")

    # ---- the block ----------------------------------------------------------
    put(f, f"{a}.findingId", " ".join(review["blockerIds"]), FROM_DISK)
    put(f, f"{a}.authoredBy", "phase1a parse-authority lane")

    r = f"{a}.reviewOfRecord"
    put(f, f"{r}.artifact", PREDECESSOR_REVIEW)
    put(f, f"{r}.sha256", sha_file(PREDECESSOR_REVIEW), FROM_DISK)
    put(f, f"{r}.verdict", review["verdict"], FROM_DISK)
    put(f, f"{r}.blockingFindingCount", review["blockingFindingCount"],
        FROM_DISK)
    put(f, f"{r}.nonBlockingObservationCount",
        review["nonBlockingObservationCount"], FROM_DISK)
    put(f, f"{r}.blockersAreAgainst", PREDECESSOR_CHECKER)
    put(f, f"{r}.plantedSealsAdmitted", review["plantedSealsAdmitted"],
        FROM_DISK)
    put(f, f"{r}.plantedSealsAttempted", review["plantedSealsAttempted"],
        FROM_DISK)
    put(f, f"{r}.plantedPositions", review["plantedPositions"], FROM_DISK)
    put(f, f"{r}.blastRadiusObjects", review["blastRadiusObjects"], FROM_DISK)
    put(f, f"{r}.wholeContractSweepCandidatesTheReviewerRan",
        review["wholeContractSweepCandidates"], FROM_DISK)
    put(f, f"{r}.whatTheReviewerCouldNotDefeat",
        f"the prose-authority partition. Its own six wordings across all string "
        f"leaves — {review['wholeContractSweepCandidates']} candidates — were "
        f"admitted 0 times, and it verified by reconstruction that v12 carries "
        f"no information its instrument does not produce. That partition is "
        f"CARRIED here byte-identical rather than rebuilt, and this successor "
        f"extends the reconstruction property from the parsed value to the "
        f"file.", FROM_DISK)

    put(f, f"{a}.defect",
        f"check-versioning-v12.py load() is json.loads(path.read_text()) with "
        f"no object_pairs_hook. RFC 8259 permits duplicate names and CPython "
        f"keeps the LAST occurrence; nothing in that checker hashed the "
        f"subject's bytes, canonically re-serialised them, or compared the file "
        f"text against the parsed value. The independent reviewer planted "
        f"{review['plantedSealsAdmitted']} of "
        f"{review['plantedSealsAttempted']} paper seals at exit 0 with the full "
        f"green banner, in ONE FILE, with no checker edit, at three positions "
        f"spanning all three prose-authority classes — top-level role, the rule "
        f"sentence that states the closure, and a CARRIED leaf inside the "
        f"pinned predecessor block — and measured "
        f"{review['blastRadiusObjects']} objects that admit the same edit. Two "
        f"further blockers followed from instruments that could not observe the "
        f"act they measured: the repoint rehearsal ran at depth 1 and the "
        f"register substitution reached one module.", FROM_DISK)
    put(f, f"{a}.whySuccessorAndNotInPlaceRepair",
        "freeze §7.2 binds a verdict to bytes. versioning-policy.v12.json was "
        "reviewed at 35357604… and check-versioning-v12.py at ff1bada4…; "
        "repairing either in place would silently retune bytes an independent "
        "reviewer adjudicated. The repair is also not a patch to load(): a "
        "hook on one call site is the list-of-places failure this lineage "
        "exists to escape, so the parse and the comparison travel together in "
        "one primitive and the file itself is compared against a "
        "reconstruction.")

    # ---- the closure --------------------------------------------------------
    v = f"{a}.byteVersusModelClosure"
    put(f, f"{v}.rule",
        "The artifact of record is the FILE. Its bytes must be exactly "
        "json.dumps(R, indent=1, ensure_ascii=False) followed by one newline, "
        "where R is the value reconstruct() builds from this checker's "
        "constants and the SHA-verified pinned predecessor and from nothing "
        "else. That single comparison closes duplicate keys, key order, number "
        "spelling, string-escape spelling, whitespace and every other "
        "file-level content that has no leaf position — not because each is "
        "detected, but because a value built by nest() from a flat "
        "path-to-value map cannot express any of them.")
    put(f, f"{v}.bytesEqualTheSerialisedReconstruction", True)
    put(f, f"{v}.whyThatLeafIsAConstantAndNotAMeasurement",
        "it is the one claim in this record that cannot be rendered from its "
        "own measurement without a loop: the value would change the bytes it "
        "describes. So the contract DECLARES it and check-versioning-v13.py "
        "MEASURES it, and a mismatch is VER13-BYTES at the offending byte "
        "offset — a finding no edit to this leaf can clear, which is the "
        "correct shape for a claim about the file the leaf sits in.")
    put(f, f"{v}.serialisationIndent", SERIALISATION_INDENT)
    put(f, f"{v}.serialisationEnsureAscii", SERIALISATION_ENSURE_ASCII)
    put(f, f"{v}.serialisationTrailerBytes", len(SERIALISATION_TRAILER))
    put(f, f"{v}.everyJsonInputIsParsedThroughOnePrimitive",
        "jloads() carries the object_pairs_hook, the parse_constant hook and "
        "the number-token census WITH the parse and returns both the value and "
        "the problems, so a caller cannot take the comparison and leave the "
        "parse. It is used for the subject, for every pinned artifact and "
        "review in the chain, and for claim-register.v1.json — the one input "
        "nobody pins, which is exactly the one a duplicate key can be planted "
        "in.")
    put(f, f"{v}.inputsParsedThroughTheHook", parses["inputs"], FROM_DISK)
    put(f, f"{v}.duplicateKeysFound", parses["duplicateKeys"], FROM_DISK)
    put(f, f"{v}.nonRfcConstantsFound", parses["nonRfcConstants"], FROM_DISK)
    put(f, f"{v}.nonCanonicalNumberTokensFound",
        parses["nonCanonicalNumberTokens"], FROM_DISK)
    put(f, f"{v}.oracleProblemsDetected", parses["oracleProblems"], FROM_DISK)
    put(f, f"{v}.oracleKindsDetected", " | ".join(parses["oracleKinds"]),
        FROM_DISK)
    put(f, f"{v}.oracleNamesTheDuplicateAtItsPath",
        parses["oracleNamesTheDuplicateAtItsPath"], FROM_DISK)
    put(f, f"{v}.whyAnOracleIsRun",
        "a census of 0 over clean inputs is indistinguishable from an "
        "instrument that detects nothing, and the predecessor's 0 was exactly "
        "that. A text carrying one duplicate key, one non-RFC constant and one "
        "non-canonical number token is driven through the same primitive on "
        "every run, and the kinds it reports are declared and compared.")
    for index, plant in enumerate(("role",
                                   f"{PROSE_BLOCK}.proseAuthorityPartition.rule",
                                   f"{PROSE_BLOCK}.enforcementClosureNotClaimed")):
        put(f, f"{v}.reviewerPlantPositions[{index}]", plant)
    put(f, f"{v}.whatTheReviewerPlantedAndWhatHappensNow",
        "the three seals were planted by duplicating a JSON key so that the "
        "text a reader meets and the value every gate reads are different "
        "documents. Under this contract the same edit changes the file's bytes "
        "away from the serialised reconstruction, so it is VER13-BYTES at the "
        "byte offset of the divergence, and it is independently VER13-PARSE at "
        "the duplicated key's own full dotted path. --selftest plants all three "
        "in the TEXT and asserts both.")

    p = f"{a}.parseSiteScan"
    put(f, f"{p}.rule",
        "a structural scan of this file's own syntax tree. Every json.load and "
        "json.loads call must pass a real object_pairs_hook — "
        "object_pairs_hook=None is the host default spelled out and is counted "
        "as bare — and every syntactic route to the decoder that such a scan "
        "cannot see is counted separately and required to be zero.")
    put(f, f"{p}.callSites", scan["sites"], FROM_DISK)
    put(f, f"{p}.hooked", scan["hooked"], FROM_DISK)
    put(f, f"{p}.ungated", scan["ungatedCount"], FROM_DISK)
    put(f, f"{p}.evasionSites", scan["evasionCount"], FROM_DISK)
    put(f, f"{p}.detectorProbeSites", scan["detectorProbeSites"], FROM_DISK)
    put(f, f"{p}.detectorProbeKinds", " | ".join(scan["detectorProbeKinds"]),
        FROM_DISK)
    put(f, f"{p}.predecessorCallSites", scan["predecessorSites"], FROM_DISK)
    put(f, f"{p}.predecessorHooked", scan["predecessorHooked"], FROM_DISK)
    put(f, f"{p}.predecessorUngated", scan["predecessorUngated"], FROM_DISK)
    put(f, f"{p}.theDifferential",
        f"measured rather than asserted: {PREDECESSOR_CHECKER} has "
        f"{scan['predecessorSites']} parse call sites of which "
        f"{scan['predecessorHooked']} pass a hook and "
        f"{scan['predecessorUngated']} do not, which is the mechanism of "
        f"B-VER12R-01. This file has {scan['sites']} of which "
        f"{scan['hooked']} pass a hook and {scan['ungatedCount']} do not.",
        FROM_DISK)
    put(f, f"{p}.whatThisDoesNotClose",
        "the scan is SYNTACTIC. A decoder reached through a name computed at "
        "run time is invisible to it, and so is any parse performed inside the "
        "pinned predecessor checkers, which are their own bytes and are not "
        "this successor's to change. R-VER13-03 states that boundary in this "
        "checker's measured numbers.")

    c = f"{a}.reconstruction"
    put(f, f"{c}.rule",
        "review O-06 recorded that the predecessor achieved total derivability "
        "of the parsed value and did not claim it, and that a declared "
        "reconstruction leaf would make the file-versus-model boundary "
        "impossible to miss because a reconstruction is necessarily free of "
        "duplicate keys. It is claimed here and it is compared: the whole "
        "contract is rebuilt from this checker plus the pinned predecessor and "
        "compared as canonical JSON, and its serialisation is compared against "
        "the file's bytes.")
    put(f, f"{c}.theWholeContractIsReproducibleFromThisCheckerAndThePinnedPredecessor",
        True)
    put(f, f"{c}.reconstructedFrom",
        f"nest() over the authored registry, composed with "
        f"{PREDECESSOR} at {PINS[PREDECESSOR][:8]}…")
    put(f, f"{c}.whyThisIsCheaperToVerifyThanThePartition",
        f"one canonical comparison against a reconstruction, versus "
        f"{census['total']} per-leaf comparisons plus a "
        f"{prose['stringLeaves']}-position sweep. A future reviewer can "
        f"falsify the central claim of this record in one step.")

    # ---- carried prose-authority partition, re-measured over these bytes ----
    w = f"{a}.proseAuthorityPartition"
    put(f, f"{w}.status",
        "CARRIED FROM THE PREDECESSOR AND RE-MEASURED OVER THESE BYTES. The "
        "independent reviewer could not defeat it on the axis it defends and "
        "reported 0 admissions over 16974 candidates; nothing here rebuilds it. "
        "What v13 adds is beneath it: the partition classifies string LEAVES, "
        "and a leaf exists only after a parse.")
    put(f, f"{w}.stringLeaves", prose["stringLeaves"], FROM_DISK)
    put(f, f"{w}.RENDERED", prose["rendered"], FROM_DISK)
    put(f, f"{w}.CARRIED", prose["carried"], FROM_DISK)
    put(f, f"{w}.FREE", prose["free"], FROM_DISK)
    put(f, f"{w}.alsoProtectedAsACanonicalJsonSection",
        prose["alsoProtectedAsASection"], FROM_DISK)
    put(f, f"{w}.positionDigest", prose["digest"], FROM_DISK)
    put(f, f"{w}.whatThisDoesNotClose",
        "it does not make any sentence true. A rendered leaf is fixed, not "
        "verified: check-versioning-v13.py holds the bytes and compares them, "
        "and a false sentence agreed between this contract and that checker "
        "passes. The v12 reviewer found two such sentences and the checker "
        "passed them, exactly as the residual predicted. That is R-VER13-02.")

    s = f"{a}.appendAdmissionSweep"
    put(f, f"{s}.rule",
        "Each sentence of the re-wording test set is APPENDED to a string leaf "
        "— removing nothing, so every substring any comparator might require "
        "survives — and the whole checker is run against each candidate in "
        "turn. Admission is exit 0 OR rejection by a finding that does not name "
        "the position.")
    put(f, f"{s}.authoredStringPositions", sweeps["authoredPositions"],
        FROM_DISK)
    put(f, f"{s}.authoredSweepSentences", sweeps["authoredSentences"],
        FROM_DISK)
    put(f, f"{s}.authoredSweepAdmitted", sweeps["authoredAdmitted"], FROM_DISK)
    put(f, f"{s}.crossProductPositions", sweeps["crossPositions"], FROM_DISK)
    put(f, f"{s}.crossProductSentences", sweeps["crossSentences"], FROM_DISK)
    put(f, f"{s}.crossProductAdmitted", sweeps["crossAdmitted"], FROM_DISK)
    put(f, f"{s}.predecessorAuthoredStringPositions",
        sweeps["predPositions"], FROM_DISK)
    put(f, f"{s}.predecessorAdmitted", sweeps["predAdmitted"], FROM_DISK)
    put(f, f"{s}.wholeContractSweepPositions", prose["stringLeaves"], FROM_DISK)
    put(f, f"{s}.wholeContractSweepAdmittedUnderSelftest", 0)
    put(f, f"{s}.whatThisSweepCannotReach",
        "a byte that is not a leaf. Appending a sentence changes a leaf and is "
        "rejected at its position; DUPLICATING A KEY changes no leaf at all, "
        "which is why the sweep reported 0 for a predecessor that admitted "
        "three seals. The sweep is retained and the byte comparison is what "
        "covers the gap.")

    t = f"{a}.rewordingTestSet"
    put(f, f"{t}.rule",
        f"{len(m['review11wordings'])} of these sentences are READ FROM "
        f"{GRANDPARENT_REVIEW} and {len(review['wordingTokens'])} from "
        f"{PREDECESSOR_REVIEW}, rather than retyped, so this checker cannot "
        f"quietly test something easier than what defeated its predecessors. "
        f"The remaining {len(MY_WORDINGS)} are authored here.")
    for index, row in enumerate(rows):
        put(f, f"{t}.sentences[{index}].index", index)
        put(f, f"{t}.sentences[{index}].provenance", row["provenance"],
            FROM_DISK)
        put(f, f"{t}.sentences[{index}].sentence",
            f"\"{row['sentence']}\" — planted and REJECTED at every position "
            f"swept here", FROM_DISK)
        put(f, f"{t}.sentences[{index}].caughtByTheLexicalLint",
            row["caughtByTheLint"], FROM_DISK)
        put(f, f"{t}.sentences[{index}].admittedHere", row["admittedHere"],
            FROM_DISK)
    put(f, f"{t}.sentenceCount", len(rows), FROM_DISK)
    put(f, f"{t}.readFromTheV11Review", len(m["review11wordings"]), FROM_DISK)
    put(f, f"{t}.readFromTheV12Review", len(review["wordingTokens"]), FROM_DISK)
    put(f, f"{t}.authoredHere", len(MY_WORDINGS))
    put(f, f"{t}.caughtByTheLexicalLint", m["lintCatches"], FROM_DISK)
    put(f, f"{t}.caughtByTheProseAuthorityPartition", len(rows), FROM_DISK)
    put(f, f"{t}.admittedHere", sweeps["crossAdmitted"], FROM_DISK)

    x = f"{a}.lexicalSealLint"
    put(f, f"{x}.status",
        f"RETAINED AS A LINT, NOT AS A CLOSURE. Its measured catch rate over "
        f"the test set is {m['lintCatches']} of {len(rows)}; the partition's is "
        f"{len(rows)} of {len(rows)}. Nothing in this record rests on the "
        f"lint.", FROM_DISK)
    for index, pattern in enumerate(SEAL_PATTERNS_ARTIFACT):
        put(f, f"{x}.artifactPatterns[{index}]", pattern)
    for index, pattern in enumerate(SEAL_PATTERNS_REVISION):
        put(f, f"{x}.revisionPatterns[{index}]", pattern)
    put(f, f"{x}.patternCount",
        len(SEAL_PATTERNS_ARTIFACT) + len(SEAL_PATTERNS_REVISION))
    put(f, f"{x}.stringLeavesScanned", lint["stringLeavesScanned"], FROM_DISK)
    put(f, f"{x}.exemptPositions", lint["exemptPositions"], FROM_DISK)
    put(f, f"{x}.patternHits", lint["patternHits"], FROM_DISK)
    put(f, f"{x}.hitsOutsideTheAllowlist", lint["hitsOutsideTheAllowlist"],
        FROM_DISK)

    # ---- purity -------------------------------------------------------------
    y = f"{a}.registryPurity"
    put(f, f"{y}.theGate",
        "the AST-measured set of (builder, sizing source) pairs is compared "
        "against the declared provenance table's key set. What the measure "
        "counts is declared beside it and is the boundary of that sentence: "
        "For, AsyncFor and comprehension sized by their iterable; While sized "
        "by its test; a call to an iteration-equivalent callee that receives a "
        "sized argument; a call to the function's own name that receives one. "
        "Taint starts at the parameter list AND at every free name the function "
        "reads outside a callee position, so a builder with no parameters that "
        "reads its subject from a module global is measured too. A construction "
        "outside that set is not caught, and the rate is published below "
        "rather than left to the sentence.")
    put(f, f"{y}.whatThePredecessorSGateSentenceClaimed",
        "\"A future editor who adds a parameter that sizes a loop must declare "
        "where its size comes from, or this check fails naming the pair.\" "
        "FALSE AS WRITTEN against v12's own measure: the reviewer's W1 adds a "
        "parameter that sizes a while loop and v12's check did not fail, "
        "because ast_structural walked only For, AsyncFor and comprehension "
        "and reported loopCount 0. It is a confirming instance of the "
        "predecessor's own residual — a false rendered sentence passes — and "
        "it is repaired here rather than only disclosed.")
    for index, name in enumerate(REGISTRY_BUILDERS):
        row = pur["mine"][name]
        put(f, f"{y}.builders[{index}].function", name)
        put(f, f"{y}.builders[{index}].nameLevelArtifactSizedLoops",
            row["lint"]["artifactSizedLoops"], FROM_DISK)
        put(f, f"{y}.builders[{index}].astIterationConstructs",
            row["ast"]["loopCount"], FROM_DISK)
        put(f, f"{y}.builders[{index}].astSizedConstructs",
            row["ast"]["parameterSizedLoops"], FROM_DISK)
        put(f, f"{y}.builders[{index}].astSizingSources",
            " | ".join(row["ast"]["sizingParameters"]), FROM_DISK)
    for index, row in enumerate(pur["reviewerSuite"]):
        put(f, f"{y}.reviewerSuite[{index}].construction", row["construction"])
        put(f, f"{y}.reviewerSuite[{index}].predecessorAstIterationConstructs",
            row["predecessorAstLoopCount"], FROM_DISK)
        put(f, f"{y}.reviewerSuite[{index}].caughtByThePredecessorAstMeasure",
            row["caughtByThePredecessorAstMeasure"], FROM_DISK)
        put(f, f"{y}.reviewerSuite[{index}].widenedAstIterationConstructs",
            row["widenedAstLoopCount"], FROM_DISK)
        put(f, f"{y}.reviewerSuite[{index}].caughtByTheWidenedAstMeasure",
            row["caughtByTheWidenedAstMeasure"], FROM_DISK)
        put(f, f"{y}.reviewerSuite[{index}].fragmentReadFromTheReview",
            fidelity[index]["fragmentReadFromTheReview"], FROM_DISK)
        put(f, f"{y}.reviewerSuite[{index}].reviewElidesTheBody",
            fidelity[index]["reviewElidesTheBody"], FROM_DISK)
        put(f, f"{y}.reviewerSuite[{index}].sourceMeasuredHereMatchesIt",
            fidelity[index]["sourceMeasuredHereMatchesIt"], FROM_DISK)
    put(f, f"{y}.reviewerSuiteAttempted", pur["reviewerSuiteAttempted"],
        FROM_DISK)
    put(f, f"{y}.reviewerSuiteCaughtByTheNameLevelLint",
        pur["reviewerSuiteCaughtByTheNameLevelLint"], FROM_DISK)
    put(f, f"{y}.reviewerSuiteCaughtByThePredecessorAstMeasure",
        pur["reviewerSuiteCaughtByThePredecessorAstMeasure"], FROM_DISK)
    put(f, f"{y}.reviewerSuiteCaughtByTheWidenedAstMeasure",
        pur["reviewerSuiteCaughtByTheWidenedAstMeasure"], FROM_DISK)
    put(f, f"{y}.reviewerSuiteProvenance",
        f"the five constructions are the ones the independent reviewer wrote "
        f"to defeat {PREDECESSOR_CHECKER}'s AST measure. Each is held here as "
        f"source AND matched against the fragment READ FROM "
        f"{PREDECESSOR_REVIEW}, under a declared normalisation that removes "
        f"whitespace and statement separators, so this checker cannot be "
        f"measuring an easier variant than the one that was written.")
    for index, row in enumerate(pur["widenedSuite"]):
        put(f, f"{y}.widenedSuite[{index}].construction", row["construction"])
        put(f, f"{y}.widenedSuite[{index}].widenedAstIterationConstructs",
            row["widenedAstLoopCount"], FROM_DISK)
        put(f, f"{y}.widenedSuite[{index}].caughtByTheWidenedAstMeasure",
            row["caughtByTheWidenedAstMeasure"], FROM_DISK)
    put(f, f"{y}.widenedSuiteAttempted", pur["widenedSuiteAttempted"],
        FROM_DISK)
    put(f, f"{y}.widenedSuiteCaughtByTheWidenedAstMeasure",
        pur["widenedSuiteCaughtByTheWidenedAstMeasure"], FROM_DISK)
    put(f, f"{y}.widenedSuiteProvenance",
        "written HERE against the WIDENED measure, because a measure published "
        "without its own boundary is exactly what review O-01 found. Each is a "
        "genuine artifact-sized registry builder that reaches its subject "
        "without a syntactically visible name.")
    for index, key in enumerate(sorted(PROVENANCE)):
        put(f, f"{y}.provenance[{index}].builder", key[0])
        put(f, f"{y}.provenance[{index}].sizingSource", key[1])
        put(f, f"{y}.provenance[{index}].source", PROVENANCE[key])
    put(f, f"{y}.declaredProvenanceEntries", pur["declaredProvenanceEntries"],
        FROM_DISK)
    put(f, f"{y}.measuredSizingSources", pur["measuredSizingParameters"],
        FROM_DISK)
    put(f, f"{y}.sizingSourcesWithoutDeclaredProvenance",
        len(pur["sizingParametersWithoutDeclaredProvenance"]), FROM_DISK)

    # ---- the attribution repair --------------------------------------------
    n = f"{a}.predecessorAttributionRepair"
    put(f, f"{n}.defect",
        f"{PREDECESSOR_CHECKER} predecessor_attribution() monkeypatched the "
        f"predecessor module's load() and not the load() of the module that "
        f"module executes transitively. Under the 'as recorded' arm the second "
        f"level still read {REGISTER} from disk, so a coordinator repoint left "
        f"a finding present in BOTH arms, scored a GENUINE DEFECT, and fired "
        f"VER13-PRED unconditionally on a leaf inside byte-pinned frozen bytes "
        f"that no artifact edit can reach.")
    put(f, f"{n}.repair",
        "the substituted register is applied to EVERY module in the "
        "predecessor's transitive set, discovered by walking module references "
        "held by each module and by its own cache rather than by naming them, "
        "and BOTH arms substitute rather than only the second.")
    put(f, f"{n}.modulesSubstituted", attr["modulesSubstituted"], FROM_DISK)
    put(f, f"{n}.moduleNames", " | ".join(attr["moduleNames"]), FROM_DISK)
    put(f, f"{n}.probeSubstitutedRegisterTarget",
        probe["substitutedRegisterTarget"])
    put(f, f"{n}.modulesWhoseLoadReturnsTheSubstitutedRegister",
        probe["modulesWhoseLoadReturnsTheSubstitutedRegister"], FROM_DISK)
    put(f, f"{n}.modulesTheSubstitutionDidNotReach",
        len(probe["modulesTheSubstitutionDidNotReach"]), FROM_DISK)
    put(f, f"{n}.probeTransitiveGenuineDefects",
        probe["transitiveGenuineDefects"], FROM_DISK)
    put(f, f"{n}.probeTopModuleOnlyGenuineDefects",
        probe["topModuleOnlyGenuineDefects"], FROM_DISK)
    put(f, f"{n}.whyReachAndNotRednessIsTheMeasurement",
        f"a repair that is only visible when something is broken cannot be "
        f"shown to work while nothing is. Against THIS predecessor the "
        f"top-module-only arm reports "
        f"{probe['topModuleOnlyGenuineDefects']} genuine defects and the "
        f"transitive arm reports {probe['transitiveGenuineDefects']}: they "
        f"agree, because check-versioning-v12.py runs its own attribution only "
        f"at its depth 0 while its nested runs read its declared bundle. "
        f"Reporting that agreement as evidence of a repair would be v12's "
        f"error inverted. What is measured instead is REACH: the patched "
        f"load() of every module in the transitive set is called on "
        f"{REGISTER}'s own path and its answer compared against the "
        f"substituted binding.", FROM_DISK)
    put(f, f"{n}.whyTheProbeExists",
        f"the mechanism is SILENT at today's register state — the predecessor "
        f"declared 0/0/0/0 and every one of those four figures reproduced — "
        f"which is why its record could not see that it was broken. The review "
        f"measured {review['attributionAfterARepoint']['live']} / "
        f"{review['attributionAfterARepoint']['asRecorded']} / "
        f"{review['attributionAfterARepoint']['attributableToARepoint']} / "
        f"{review['attributionAfterARepoint']['genuineDefects']} at the NEXT "
        f"register state. The probe therefore runs the attribution in the state "
        f"it exists to handle, and it runs it twice so that a 0 from the "
        f"repaired path is distinguishable from a 0 from an instrument that "
        f"sees nothing.", FROM_DISK)

    e = f"{a}.evidenceGate"
    put(f, f"{e}.rule",
        "the decisionDependencies equality gate with a pinned fallback, carried "
        "from the predecessor and measured on every run: an entry is appended, "
        "VER13-DEP must fire, and the as-of registry position count must not "
        "grow. What is published is the gate's OWN signature — that the "
        "dependency finding is ABSENT before the probe and PRESENT after it — "
        "rather than the probe run's whole finding-id set, which is what made "
        "the predecessor's leaf move under a coordinator repoint and which has "
        "no fixed point at all against a red base.")
    put(f, f"{e}.gateFiresHere", gate["gateFires"], FROM_DISK)
    put(f, f"{e}.gateIntroducesTheDependencyFinding",
        gate["introducesTheDependencyFinding"], FROM_DISK)
    put(f, f"{e}.asOfRegistryPositionsBeforeTheProbe", gate["positionsBefore"],
        FROM_DISK)
    put(f, f"{e}.asOfRegistryPositionsAfterTheProbe", gate["positionsAfter"],
        FROM_DISK)

    # ---- census and partition ----------------------------------------------
    z = f"{a}.coverageCensus"
    put(f, f"{z}.rule",
        "every leaf position in the whole contract is assigned to exactly one "
        "gate: an enforcement scope, the canonical-JSON comparison of the "
        "protected surface, or byte-carry against the pinned predecessor. A "
        "position that lands in none increments the ungated count, which is "
        "declared and compared. Above all of them sits one comparison the "
        "census cannot express, because it is not about positions at all: the "
        "file's bytes against the serialised reconstruction.")
    put(f, f"{z}.artifactLeafPositions", census["total"], FROM_DISK)
    put(f, f"{z}.gatedPerLeafByAnEnforcementScope", census["scope"], FROM_DISK)
    put(f, f"{z}.gatedOnlyByASectionComparison", census["sectionOnly"],
        FROM_DISK)
    put(f, f"{z}.ungated", census["ungated"], FROM_DISK)
    put(f, f"{z}.alsoByteCarriedAgainstThePredecessor",
        census["alsoByteCarried"], FROM_DISK)
    put(f, f"{z}.alsoProtectedAsACanonicalJsonSection",
        census["alsoProtectedAsASection"], FROM_DISK)
    put(f, f"{z}.predecessorDeclaredByteCarryFigure",
        m["predCensus"]["declaredByteCarry"], FROM_DISK)
    put(f, f"{z}.predecessorLeavesInBothAScopeAndByteCarry",
        m["predCensus"]["doubleGated"], FROM_DISK)
    put(f, f"{z}.predecessorByteCarriedIncludingDoubleGated",
        m["predCensus"]["byteCarriedIncludingDoubleGated"], FROM_DISK)

    q = f"{a}.partitionClosure"
    put(f, f"{q}.rule",
        "PARTITION_SCOPES is the single authority for what is partitioned. "
        "Every partition computed under it is compared against the declaration "
        "in this table before anything is printed, and the PASS banner is "
        "rendered from the list of comparisons that actually happened.")
    for index, (name, roots) in enumerate(PARTITION_SCOPES):
        part = parts[name]
        put(f, f"{q}.scopes[{index}].name", name)
        put(f, f"{q}.scopes[{index}].roots", " | ".join(roots))
        put(f, f"{q}.scopes[{index}].total", part["total"], FROM_DISK)
        put(f, f"{q}.scopes[{index}].MEASURED", part["measured"], FROM_DISK)
        put(f, f"{q}.scopes[{index}].measuredAgainstDisk", part["fromDisk"],
            FROM_DISK)
        put(f, f"{q}.scopes[{index}].measuredAgainstACheckerConstant",
            part["fromConstant"], FROM_DISK)
        put(f, f"{q}.scopes[{index}].positionDigest", part["digest"], FROM_DISK)
    put(f, f"{q}.computedPartitions", len(PARTITION_SCOPES))
    put(f, f"{q}.declaredPartitions", len(PARTITION_SCOPES))
    put(f, f"{q}.uncomparedPartitions", 0)
    put(f, f"{q}.publishedMeasurements", m["publishedCount"], FROM_DISK)

    b = f"{a}.carriedByteIdentical"
    put(f, f"{b}.rule",
        f"every successorRevision key except id, supersedesCandidate, "
        f"identityStability and parseAuthorityRepair is carried from "
        f"{PREDECESSOR} byte-identical and gated leaf-wise against those bytes "
        f"— including the whole of proseAuthorityRepair, the block the "
        f"independent reviewer verified and could not defeat — and every "
        f"top-level key except version, supersedes, role, knownLimitations and "
        f"successorRevision is compared as canonical JSON against them.")
    for index, name in enumerate(FROZEN_REVISION_KEYS):
        put(f, f"{b}.frozenSuccessorKeys[{index}]", name)
    put(f, f"{b}.frozenSuccessorKeyCount", len(FROZEN_REVISION_KEYS))
    put(f, f"{b}.protectedTopLevelKeys", m["protectedTopLevelKeys"], FROM_DISK)
    for index, name in enumerate(sorted(CHANGED)):
        put(f, f"{b}.changedTopLevelKeys[{index}]", name)
    put(f, f"{b}.carriedDelta.count", m["carriedDeltaCount"], FROM_DISK)
    put(f, f"{b}.carriedDelta.digest", m["carriedDeltaDigest"], FROM_DISK)
    put(f, f"{b}.carriedDelta.rule",
        "the carried delta is published as a COUNT and a DIGEST, never as an "
        "indexed table, so a moved carried leaf changes a count and a digest "
        "and there is no index to shift.")
    put(f, f"{b}.asOfPositions", m["asofPositions"], FROM_DISK)
    put(f, f"{b}.asOfRule",
        f"any carried leaf whose path ends in {' or '.join(AS_OF_SUFFIXES)} is "
        f"a RECORDED MEASUREMENT of a file that moves, so it is compared "
        f"against the live register instead of against the carried byte.")

    # ---- register -----------------------------------------------------------
    g = f"{a}.registerAsOfAudit"
    put(f, f"{g}.principle",
        "R-VER10-08's axis, upheld unchanged and applied rather than quoted: "
        "measurements get hard comparison, invariants get semantic gates. A "
        "registerBinding is a recorded measurement — at authoring, X was Y — so "
        "going stale is a true positive about these bytes. "
        "decisionDependencies[4].source is a continuing invariant and is gated "
        "against the register's LIVE D9 binding.")
    put(f, f"{g}.noRegisterDigestIsRecordedInThisBlock", True)
    put(f, f"{g}.butItIsParsedThroughTheDuplicateKeyHook", True)
    put(f, f"{g}.whyBoth",
        "a digest of a file expected to move is a timestamp, not evidence. A "
        "PARSE of that same file is not a timestamp: the register is the only "
        "input to this verdict that nobody pins, so it is the one input in "
        "which a duplicate key costs an attacker nothing, and it is parsed "
        "through the same primitive as everything else.")
    for index, row in enumerate(m["audit"]):
        put(f, f"{g}.entries[{index}].index", index)
        put(f, f"{g}.entries[{index}].family", row["family"], FROM_DISK)
        put(f, f"{g}.entries[{index}].resolvedBy", row["resolvedBy"], FROM_DISK)
        put(f, f"{g}.entries[{index}].registerBinding", row["registerBinding"],
            FROM_DISK)
        put(f, f"{g}.entries[{index}].candidateBindingsInFamily",
            row["candidates"], FROM_DISK)
    put(f, f"{g}.liveD9Binding", m["liveD9"], FROM_DISK)
    put(f, f"{g}.liveVersioningBinding", m["liveVersioning"], FROM_DISK)
    put(f, f"{g}.liveRetentionTiersBinding", m["liveRetentionTiers"], FROM_DISK)
    put(f, f"{g}.d9CitationEqualsTheLiveBinding", True)

    k = f"{a}.repointRehearsals"
    put(f, f"{k}.rule",
        "the pending coordinator act is rehearsed LIVE and IN PROCESS on every "
        "run: the register is substituted behind one indirection, THE WHOLE "
        "BUNDLE IS RE-DERIVED UNDER IT, the check runs at depth-0 semantics so "
        "no finding class is skipped, exactly what each finding names is "
        "applied and nothing else, and the loop iterates to a fixed point — "
        "jointly with the rehearsal's own declared rows, which are themselves "
        "leaves of this contract. No file anywhere under docs/coop is written "
        "to perform a rehearsal.")
    put(f, f"{k}.whatThePredecessorSRuleClaimed",
        f"the same sentence without the second and third clauses. v12's "
        f"rehearse_live called inner(), which runs at depth 1 and returns "
        f"before {len(POST_GUARD_CLASSES)} of its own finding classes, and "
        f"reused a bundle measured against the UNREPOINTED register, so "
        f"leaves that genuinely move compared equal inside the rehearsal and "
        f"could never surface. The claim is not repeated here on trust: "
        f"rehearsal_reach_probe() drives each of those "
        f"{len(POST_GUARD_CLASSES)} guards down both paths and the two counts "
        f"are declared below.", FROM_DISK)
    put(f, f"{k}.postGuardClassesProbed", reach["classes"], FROM_DISK)
    put(f, f"{k}.postGuardClassesReachedOnTheDepthZeroPath",
        reach["reachedAtDepthZero"], FROM_DISK)
    put(f, f"{k}.postGuardClassesReachedOnTheDepthOnePathTheV12RehearsalUsed",
        reach["reachedAtDepthOne"], FROM_DISK)
    for index, row in enumerate(reach["rows"]):
        put(f, f"{k}.postGuardClasses[{index}].findingClass",
            row["findingClass"])
        put(f, f"{k}.postGuardClasses[{index}]."
               f"firesOnTheDepthZeroPathThisRehearsalUses",
            row["firesOnTheDepthZeroPathThisRehearsalUses"], FROM_DISK)
        put(f, f"{k}.postGuardClasses[{index}]."
               f"firesOnTheDepthOnePathTheV12RehearsalUsed",
            row["firesOnTheDepthOnePathTheV12RehearsalUsed"], FROM_DISK)
    for index, row in enumerate(live):
        put(f, f"{k}.live[{index}].target", row["target"])
        put(f, f"{k}.live[{index}].findingsOnTheFirstRound", row["findings"],
            FROM_DISK)
        put(f, f"{k}.live[{index}].findingIds", row["findingIds"], FROM_DISK)
        put(f, f"{k}.live[{index}].findingClassesDrivenAcrossAllRounds",
            row["findingClassesDriven"], FROM_DISK)
        put(f, f"{k}.live[{index}].roundsToExitZero", row["roundsToGreen"],
            FROM_DISK)
        put(f, f"{k}.live[{index}].leafEdits", row["leafEdits"], FROM_DISK)
        put(f, f"{k}.live[{index}].checkerEdits", row["checkerEdits"], FROM_DISK)
        put(f, f"{k}.live[{index}].indexShifts", row["indexShifts"], FROM_DISK)
        put(f, f"{k}.live[{index}].positionsAddedOrRemoved",
            row["positionsAddedOrRemoved"], FROM_DISK)
        put(f, f"{k}.live[{index}].findingsNotSelfRepairing",
            row["findingsNotSelfRepairing"], FROM_DISK)
        put(f, f"{k}.live[{index}].heldFixedMembersThatMoved",
            row["heldFixedMembersThatMoved"], FROM_DISK)
        put(f, f"{k}.live[{index}].reachedExitZero", row["reachedExitZero"],
            FROM_DISK)
    put(f, f"{k}.assertionsAboutItsOwnRowsSkippedInsideARehearsal",
        REHEARSAL_SELF_ASSERTIONS)
    put(f, f"{k}.whyThoseFourAreSkippedAndNothingElseIs",
        "a rehearsal cannot rehearse itself. Those four assertions are about "
        "the rehearsal's own converging estimate of its own rows, and "
        "evaluating them inside one measures nothing while creating a second, "
        "self-fulfilling fixed point: a rehearsal that has not yet reached exit "
        "0 would assert that it has not, forever. The rows are still COMPARED "
        "leaf by leaf inside a rehearsal, so a moved rehearsal row still costs "
        "a leaf edit and is still counted in the figures above. Every other "
        "finding class this checker has runs inside a rehearsal, and the "
        "post-guard probe above measures which ones the depth-0 path reaches "
        "against which ones the depth-1 path the predecessor used reaches.")
    put(f, f"{k}.jointFixedPointIterations", m["rehearsalIterations"], FROM_DISK)
    put(f, f"{k}.jointFixedPointConverged", m["rehearsalConverged"], FROM_DISK)
    for index, row in enumerate(review["rehearsal"]):
        put(f, f"{k}.whatTheReviewerMeasuredOnDisk[{index}].target",
            row.get("target"), FROM_DISK)
        put(f, f"{k}.whatTheReviewerMeasuredOnDisk[{index}].predecessorDeclaredFindings",
            row.get("declaredFindings"), FROM_DISK)
        put(f, f"{k}.whatTheReviewerMeasuredOnDisk[{index}].measuredFindings",
            row.get("measuredFindings"), FROM_DISK)
        put(f, f"{k}.whatTheReviewerMeasuredOnDisk[{index}].predecessorDeclaredLeafEdits",
            row.get("declaredLeafEdits"), FROM_DISK)
        put(f, f"{k}.whatTheReviewerMeasuredOnDisk[{index}].measuredLeafEdits",
            row.get("measuredLeafEdits"), FROM_DISK)
        put(f, f"{k}.whatTheReviewerMeasuredOnDisk[{index}].measuredRounds",
            row.get("measuredRounds"), FROM_DISK)
        put(f, f"{k}.whatTheReviewerMeasuredOnDisk[{index}].measuredReachedExitZero",
            row.get("measuredReachedExitZero"), FROM_DISK)
    for index, row in enumerate(synth):
        put(f, f"{k}.syntheticCouplingSurface[{index}].event", row["event"])
        put(f, f"{k}.syntheticCouplingSurface[{index}]."
               f"declaredLeavesThatWouldChange",
            row["declaredLeavesThatWouldChange"], FROM_DISK)
        put(f, f"{k}.syntheticCouplingSurface[{index}].positionsAddedOrRemoved",
            row["positionsAddedOrRemoved"], FROM_DISK)
        put(f, f"{k}.syntheticCouplingSurface[{index}].indexShifts",
            row["indexShifts"], FROM_DISK)
    put(f, f"{k}.documentedRetentionTiersHead", DOCUMENTED_RT_HEAD)
    put(f, f"{k}.registerBindsTheDocumentedHead", m["bindsDocumentedHead"],
        FROM_DISK)
    put(f, f"{k}.bothLiveTargetsAreOnDisk", m["liveTargetsOnDisk"], FROM_DISK)
    put(f, f"{k}.whyTheCostFellRatherThanRose",
        "every measurement this record makes ABOUT the pinned predecessor's "
        "behaviour — the six demonstrations, the predecessor sweep — is taken "
        "under the register state the predecessor's own record names, because "
        "what a frozen instrument did to a frozen artifact is a fact about "
        "those bytes. In v12 they were taken against the live register, so a "
        "coordinator act that had nothing to do with them moved eleven declared "
        "leaves. The as-of leaves still move, and they are the leaves designed "
        "to.")

    # ---- predecessor --------------------------------------------------------
    d = f"{a}.predecessorDisposition"
    put(f, f"{d}.rule",
        "the pinned predecessor pair is executed against its own bytes rather "
        "than assumed green, and it is NOT required to be silent: it is frozen, "
        "and a coordinator repoint makes it red through no fault of any "
        "artifact. Requiring silence from an instrument nobody may repair would "
        "be the defect, not the guard.")
    put(f, f"{d}.attributionMethod", attr["method"], FROM_DISK)
    put(f, f"{d}.findingsAgainstItsOwnBytes",
        attr["findingsAgainstItsOwnBytes"], FROM_DISK)
    put(f, f"{d}.findingsUnderTheRegisterStateItRecorded",
        attr["findingsUnderTheRegisterStateItRecorded"], FROM_DISK)
    put(f, f"{d}.findingsAttributableToACoordinatorRepoint",
        attr["findingsAttributableToACoordinatorRepoint"], FROM_DISK)
    put(f, f"{d}.genuineDefects", attr["genuineDefects"], FROM_DISK)
    put(f, f"{d}.predecessorAdmissions", m["predAdmissions"], FROM_DISK)
    put(f, f"{d}.successorAdmissions", m["selfAdmissions"], FROM_DISK)

    for index, row in enumerate(probes):
        put(f, f"{a}.demonstrations[{index}].probe", row["probe"])
        put(f, f"{a}.demonstrations[{index}].positionInThePredecessor",
            row["positionInThePredecessor"])
        put(f, f"{a}.demonstrations[{index}].position", row["position"])
        put(f, f"{a}.demonstrations[{index}].predecessorAdmitted",
            row["predecessorAdmitted"], FROM_DISK)
        put(f, f"{a}.demonstrations[{index}].predecessorFindings",
            row["predecessorFindings"], FROM_DISK)
        put(f, f"{a}.demonstrations[{index}].successorRejects",
            row["successorRejects"], FROM_DISK)
        put(f, f"{a}.demonstrations[{index}].successorNamesThePosition",
            row["successorNamesThePosition"], FROM_DISK)
        put(f, f"{a}.demonstrations[{index}].successorFindingIds",
            row["successorFindingIds"], FROM_DISK)

    o = f"{a}.closedScalarAdmission"
    put(f, f"{o}.law", "freeze §6 law 18 — closed-scalar admission is "
                       "exact-type in BOTH directions")
    put(f, f"{o}.booleanLeavesSwept", m["boolSweep"]["total"], FROM_DISK)
    put(f, f"{o}.boolToIntAdmitted", m["boolSweep"]["admitted"], FROM_DISK)
    put(f, f"{o}.andAtTheByteLayer",
        "law 18 is an exact-TYPE admission, and a type is a property of a "
        "parsed value. The byte comparison adds the layer below it: 1.0 and 1 "
        "parse to different types and are caught here, but 1.0 and 1.0 with a "
        "different SPELLING parse to the same value and are caught only by the "
        "bytes. The number-token census reports that class separately and its "
        "count is declared above.")

    u = f"{a}.selftestProfile"
    put(f, f"{u}.countedBy", "type transition, not label text")
    put(f, f"{u}.mutations", m["census13"]["total"], FROM_DISK)
    put(f, f"{u}.floatRespellings", m["census13"]["floatRespellings"], FROM_DISK)
    put(f, f"{u}.booleanRespellings", m["census13"]["booleanRespellings"],
        FROM_DISK)
    put(f, f"{u}.assertionsOnAFullDottedPath", m["fullPathAssertions"],
        FROM_DISK)
    put(f, f"{u}.assertionsOnASectionName", m["sectionAssertions"], FROM_DISK)
    put(f, f"{u}.distinctFindingIdsExercised", m["distinctIds"], FROM_DISK)
    put(f, f"{u}.textMutations", m["textMutations"], FROM_DISK)
    put(f, f"{u}.whatATextMutationIs",
        "a mutation of the FILE that changes no leaf position at all — a "
        "duplicated key, a respelled number token, a non-RFC constant, a "
        "changed indent. No value-level mutation table can express one, which "
        "is why the predecessor's 92 mutations all passed while three paper "
        "seals sat in its file. Each is asserted to be rejected by its specific "
        "finding id AND at its position, exactly as a value mutation is.")
    put(f, f"{u}.predecessorMutations", m["census12"]["total"], FROM_DISK)
    put(f, f"{u}.predecessorFloatRespellings",
        m["census12"]["floatRespellings"], FROM_DISK)
    put(f, f"{u}.predecessorBooleanRespellings",
        m["census12"]["booleanRespellings"], FROM_DISK)

    # ---- residual restatements ---------------------------------------------
    declared_v23 = review["rehearsal"][0] if review["rehearsal"] else {}
    declared_v24 = review["rehearsal"][1] if len(review["rehearsal"]) > 1 else {}
    restated = [
        ("R-VER12-01", "B-VER12R-01",
         f"The predecessor recorded the residual as an EDIT COST: \"the surface "
         f"an editor must move to plant a seal is 2 files rather than 1\", and "
         f"knownLimitations[32] said \"what v12 closes is the one-file edit\".",
         f"BOTH FALSIFIED BY A ONE-FILE EDIT, and the error was not the number "
         f"— it was the dimension. The class had moved to the PARSE, one layer "
         f"below where the record was looking, and an edit-cost figure cannot "
         f"see a layer. Restated here on the axis it lives on: every byte of "
         f"this contract is either produced by check-versioning-v13.py or "
         f"carried from SHA-verified pinned bytes, composed by one declared "
         f"serialisation and compared against the file, so there is no edit an "
         f"author without this checker can make to any byte. What remains open "
         f"is the instrument, and its size is {prose['rendered']} RENDERED "
         f"string leaves whose content is fixed rather than verified."),
        ("R-VER12-03", "O-01",
         f"The predecessor disclosed its AST measure as OVER-tainting — the "
         f"safe direction — and its provenance table as hand-authored.",
         f"It also UNDER-detected whole loop forms, the unsafe direction, which "
         f"it did not disclose: the reviewer's five constructions scored "
         f"{pur['reviewerSuiteCaughtByThePredecessorAstMeasure']} of "
         f"{pur['reviewerSuiteAttempted']} against it. Widened here to "
         f"{pur['reviewerSuiteCaughtByTheWidenedAstMeasure']} of "
         f"{pur['reviewerSuiteAttempted']}, with free module globals counted as "
         f"sizing sources alongside parameters, and with the widened measure's "
         f"OWN boundary measured at "
         f"{pur['widenedSuiteCaughtByTheWidenedAstMeasure']} of "
         f"{pur['widenedSuiteAttempted']} against a suite written to defeat it."),
        ("R-VER12-05", "B-VER12R-02 and B-VER12R-03",
         f"The predecessor declared the v23 repoint at "
         f"{declared_v23.get('declaredFindings')} findings and "
         f"{declared_v23.get('declaredLeafEdits')} leaf edits and the v24 "
         f"repoint at {declared_v24.get('declaredFindings')} and "
         f"{declared_v24.get('declaredLeafEdits')}, both reaching exit 0.",
         f"The reviewer measured {declared_v23.get('measuredFindings')} / "
         f"{declared_v23.get('measuredLeafEdits')} and "
         f"{declared_v24.get('measuredFindings')} / "
         f"{declared_v24.get('measuredLeafEdits')} on disk, neither reaching "
         f"exit 0, because the rehearsal ran at depth 1 and the attribution "
         f"stranded the checker on an unreachable leaf. Measured here with the "
         f"whole check driven under the substituted register: v23 costs "
         f"{live[0]['findings']} findings, {live[0]['roundsToGreen']} rounds "
         f"and {live[0]['leafEdits']} leaf edits, reaching exit 0 "
         f"{live[0]['reachedExitZero']}; v24 costs {live[1]['findings']}, "
         f"{live[1]['roundsToGreen']} and {live[1]['leafEdits']}, reaching exit "
         f"0 {live[1]['reachedExitZero']}."),
    ]
    for index, (rid, observation, was, now) in enumerate(restated):
        put(f, f"{a}.residualRestatements[{index}].id", rid)
        put(f, f"{a}.residualRestatements[{index}].reviewObservation",
            observation)
        put(f, f"{a}.residualRestatements[{index}].wasRecorded", was, FROM_DISK)
        put(f, f"{a}.residualRestatements[{index}].nowMeasured", now, FROM_DISK)

    for index, (name, role) in enumerate(V13_REQUIRED_INPUTS):
        put(f, f"{a}.recordedInputs[{index}].artifact", name)
        put(f, f"{a}.recordedInputs[{index}].sha256", sha_file(name), FROM_DISK)
        put(f, f"{a}.recordedInputs[{index}].role", role)
    put(f, f"{a}.recordedInputsRule",
        f"freeze §7.2 — filename and sha256 for every input this record depends "
        f"on. {len(V13_REQUIRED_INPUTS)} inputs, each measured from disk on "
        f"every run. {REGISTER} is deliberately absent from the DIGEST record "
        f"and deliberately present in the PARSE record: it is expected to move, "
        f"so a digest of it is a timestamp, but a duplicate key in it is a "
        f"finding.")

    # ---- retained residuals, each stating its boundary in measured digits ---
    residuals = [
        ("R-VER13-01",
         "The file-versus-model boundary is closed by construction, and what "
         "remains is the INSTRUMENT — stated as a layer, not as an edit count.",
         f"The predecessor's residual named a cost in files and the class was "
         f"in the parse. Measured here: the file's bytes equal the "
         f"serialisation of a reconstruction built from this checker and "
         f"{PREDECESSOR} at indent {SERIALISATION_INDENT}, and the whole "
         f"contract is canonically identical to that reconstruction — both "
         f"declared as constants here and MEASURED by the checker, because a "
         f"leaf that reported its own measurement would change the bytes it "
         f"describes; {parses['duplicateKeys']} "
         f"duplicate keys, {parses['nonRfcConstants']} non-RFC constants and "
         f"{parses['nonCanonicalNumberTokens']} non-canonical number tokens "
         f"across {parses['inputs']} parsed inputs, against an oracle that "
         f"reports {parses['oracleProblems']} on a text carrying one of each. "
         f"The predecessor admitted the class in "
         f"{review['blastRadiusObjects']} objects. What is NOT closed is that "
         f"check-versioning-v13.py determines every byte: an editor with access "
         f"to it can still agree a false sentence with this contract, and that "
         f"surface is {prose['rendered']} rendered leaves.",
         "Closed at the byte layer and republished as an instrument-scope "
         "residual. The boundary is now stated about the layer the hazard lives "
         "in rather than about the number of files an editor must open."),
        ("R-VER13-02",
         "A rendered leaf is FIXED, not VERIFIED.",
         f"{prose['rendered']} string leaves are RENDERED: their whole value is "
         f"compared against a string check-versioning-v13.py produces. An "
         f"appended sentence is admitted at {sweeps['authoredAdmitted']} of "
         f"{sweeps['authoredPositions']} authored positions and at "
         f"{sweeps['crossAdmitted']} of the {sweeps['crossPositions']} × "
         f"{sweeps['crossSentences']} test-set cross product. But the "
         f"independent reviewer found two rendered sentences that were FALSE "
         f"and passed — registryPurity.theGate and R-VER12-03's disposition — "
         f"and it did not audit the remaining rendered leaves for truth. Both "
         f"of those sentences are repaired in this successor; the class is not.",
         "Bounded and published rather than closed. Closing it would require "
         "the instrument to decide whether a sentence is true, which no byte "
         "instrument can do and which this record does not claim."),
        ("R-VER13-03",
         "The parse-site scan is SYNTACTIC, and it does not reach inside the "
         "pinned predecessors.",
         f"Measured: {scan['sites']} parse call sites in this file, "
         f"{scan['hooked']} hooked, {scan['ungatedCount']} ungated, "
         f"{scan['evasionCount']} decoder-evasion sites, against a detector "
         f"probe that reports {scan['detectorProbeSites']} sites over "
         f"{len(scan['detectorProbeKinds'])} distinct kinds. A decoder reached "
         f"through a name computed at RUN TIME is invisible to it. "
         f"{PREDECESSOR_CHECKER} carries {scan['predecessorUngated']} ungated "
         f"parse sites and is pinned; the parses performed inside it and inside "
         f"every checker below it are their own bytes and are not this "
         f"successor's to change.",
         "Disclosed with its measured boundary. The byte comparison is what "
         "makes the scan defence in depth rather than the gate."),
        ("R-VER13-04",
         "The widened AST purity measure has a boundary, and it is published "
         "with its own measured evasion rate.",
         f"The predecessor's measure catches "
         f"{pur['reviewerSuiteCaughtByThePredecessorAstMeasure']} of "
         f"{pur['reviewerSuiteAttempted']} of the reviewer's constructions; "
         f"this one catches {pur['reviewerSuiteCaughtByTheWidenedAstMeasure']}. "
         f"A further {pur['widenedSuiteAttempted']} constructions written HERE "
         f"against the widened measure — exec of a built source, mutual "
         f"recursion, a closure variable, a builder that opens the file itself, "
         f"and a globals() subscript — are caught at "
         f"{pur['widenedSuiteCaughtByTheWidenedAstMeasure']} of "
         f"{pur['widenedSuiteAttempted']}. The declared provenance table has "
         f"{pur['declaredProvenanceEntries']} entries against "
         f"{pur['measuredSizingParameters']} measured pairs and only their KEY "
         f"SET is compared.",
         "Bounded. The key-set comparison closes silent addition; it does not "
         "close a mis-stated source, and it does not close a construction "
         "outside the measure's declared node set."),
        ("R-VER13-05",
         "v13 carries no independent review.",
         f"The verdict of record is {review['verdict']} with "
         f"{review['blockingFindingCount']} blocking findings against "
         f"{PREDECESSOR_CHECKER}, and it binds the v12 bytes in either "
         f"direction, not these. status remains CANDIDATE-NOT-APPLIED, "
         f"reviewStatus remains AWAITING-INDEPENDENT-COMBINED-REREVIEW and "
         f"dischargeStatus.seal remains DO-NOT-SEAL.",
         "A new verdict on these bytes is required before v13 can carry one. "
         "Nothing here claims one."),
        ("R-VER13-06",
         "The register columns are a recorded measurement, hard-compared "
         "against a coordinator-owned file that moves.",
         f"Accepted deliberately and not weakened. What is bounded is the blast "
         f"radius, measured live on every run with the whole check driven under "
         f"the substituted register: repointing ARCH.RETENTION-TIERS to "
         f"{LIVE_REPOINT_TARGETS[0]} produces {live[0]['findings']} findings, "
         f"{live[0]['roundsToGreen']} rounds and {live[0]['leafEdits']} leaf "
         f"edits; to {LIVE_REPOINT_TARGETS[1]} it produces "
         f"{live[1]['findings']}, {live[1]['roundsToGreen']} and "
         f"{live[1]['leafEdits']}. Checker edits {live[1]['checkerEdits']}, "
         f"index shifts {live[1]['indexShifts']}, positions added or removed "
         f"{live[1]['positionsAddedOrRemoved']}, findings whose printed repair "
         f"instruction could not be followed mechanically "
         f"{live[1]['findingsNotSelfRepairing']}.",
         "Accepted deliberately; the cost is declared, measured by an "
         "instrument that can observe every class that blocks it, and in "
         "place."),
        ("R-VER13-07",
         "v13 is not the register-bound head.",
         f"{REGISTER} binds VERSIONING to {m['liveVersioning']}, which is "
         f"{m['versioningVersionsBehind']} versions behind these bytes, and "
         f"binds ARCH.RETENTION-TIERS to {m['liveRetentionTiers']} while both "
         f"prose documents name {DOCUMENTED_RT_HEAD}. This checker reads both "
         f"from the live register on every run and declares them rather than "
         f"assuming them.",
         "Deliberate. The register is coordinator-owned and was not touched by "
         "this successor."),
        ("R-VER13-08",
         "check-versioning.py remains permanently red and its crash is "
         "exit-code-indistinguishable from a finding.",
         f"{V4_CHECKER} hardcodes its subject to {V4} and its VER-DEP loop "
         f"calls d.get('source') over decisionDependencies, which from v7 "
         f"onward carries bare label strings, raising AttributeError. An "
         f"uncaught exception exits 1 — the same code as a legitimate finding.",
         "Not closable here; the only in-place fix is forbidden. This is why "
         "every finding in check-versioning-v13.py carries a stable id and "
         "names its position, and why --selftest asserts on both."),
        ("R-VER13-09",
         "The predecessor checkers are not repaired and still admit what this "
         "one rejects.",
         f"Executed on every run of this checker: {PREDECESSOR_CHECKER} admits "
         f"an appended re-worded assurance claim at {sweeps['predAdmitted']} of "
         f"{sweeps['predPositions']} authored string positions in its own "
         f"contract, carries {scan['predecessorUngated']} ungated parse sites, "
         f"and its AST measure catches "
         f"{pur['reviewerSuiteCaughtByThePredecessorAstMeasure']} of "
         f"{pur['reviewerSuiteAttempted']} constructions written to defeat it. "
         f"All predecessor checkers are pinned by sha256 and cannot be edited.",
         "Recorded, not repaired. The chain's gate is the newest checker."),
        ("R-VER13-10",
         "The whole-contract append sweep runs under --selftest; a plain run "
         "sweeps the authored surface and a cross product.",
         f"A plain run sweeps {sweeps['authoredPositions']} authored string "
         f"positions across {sweeps['authoredSentences']} wordings and a "
         f"{sweeps['crossPositions']} × {sweeps['crossSentences']} cross "
         f"product spanning every prose-authority class. --selftest sweeps all "
         f"{prose['stringLeaves']} string leaves in the contract and applies "
         f"{m['textMutations']} TEXT mutations that no value-level sweep can "
         f"express.",
         "Deliberate scope, stated as a measured number rather than as a "
         "sample."),
        ("R-VER13-11",
         "A position being gated is not the same as its meaning being checked.",
         f"The census proves coverage, not correctness: {census['total']} leaf "
         f"positions, {census['scope']} classified per-leaf by an enforcement "
         f"scope, {census['sectionOnly']} gated only as members of a protected "
         f"top-level section, {census['ungated']} ungated. For each class this "
         f"checker establishes that the bytes are what an adjudicated "
         f"predecessor carried or what it itself renders — not that the "
         f"surrounding sentence is true. The carried D9 span is still measured "
         f"at {m['d9SpanEndpoints']} endpoints only, with "
         f"{m['d9SpanIntermediates']} intermediate versions on disk unread.",
         "Disclosed. It is the honest ceiling of a byte instrument, and it is "
         "why every residual boundary here is stated in this checker's own "
         "measured numbers and about the layer the hazard lives in."),
    ]
    for index, (rid, residual, measured, disposition) in enumerate(residuals):
        put(f, f"{a}.retainedResiduals[{index}].id", rid)
        put(f, f"{a}.retainedResiduals[{index}].residual", residual)
        put(f, f"{a}.retainedResiduals[{index}].measured", measured, FROM_DISK)
        put(f, f"{a}.retainedResiduals[{index}].disposition", disposition)
        put(f, f"{a}.retainedResiduals[{index}].ownedBy", RESIDUAL_OWNERS[rid])

    h = f"{a}.checkerDisposition"
    put(f, f"{h}.successorCheckerRequired", True)
    put(f, f"{h}.checker", pathlib.Path(__file__).name, FROM_DISK)
    put(f, f"{h}.everyLeafPositionInEveryDeclaredScopeIsCompared", True)
    put(f, f"{h}.declaredScopes", len(PARTITION_SCOPES))
    put(f, f"{h}.unclassifiedLeafPositionsAcrossAllScopes", 0)
    put(f, f"{h}.scopeOfThatBoolean",
        "the seven scopes named in partitionClosure, which between them cover "
        "every leaf position in successorRevision, role, knownLimitations, "
        "version and supersedes, and the protected top-level sections. It is a "
        "statement about POSITIONS, and a position exists only after a parse — "
        "which is why it is not the outermost gate in this record and "
        "byteVersusModelClosure is.")
    put(f, f"{h}.whyThePredecessorCheckerCannotValidateThis",
        f"{PREDECESSOR_CHECKER} pins its subject's version to exactly 12 and "
        f"its successorRevision key set to a closed set that does not contain "
        f"parseAuthorityRepair. It is frozen at "
        f"{PINS[PREDECESSOR_CHECKER][:8]}… and nobody may repair it.")
    put(f, f"{h}.evidenceGrade", "IMPLEMENTABLE_UNEXECUTED")

    not_claimed = [
        "No seal, freeze, signature or status advance is declared. status "
        "remains CANDIDATE-NOT-APPLIED, reviewStatus remains "
        "AWAITING-INDEPENDENT-COMBINED-REREVIEW, and dischargeStatus is carried "
        "byte-identical with seal DO-NOT-SEAL, V10 UNRESOLVED, CD-RT-5 BLOCKED "
        "and G19 BLOCKED. Nothing in this record advances CD-RT-5, which "
        "remains BLOCKED_ON_PHASE_1A.",
        "The v12 independent verdict is not transferred to these bytes. It "
        "returned CHANGES-REQUIRED with three blocking findings against "
        "check-versioning-v12.py and two leaves of versioning-policy.v12.json, "
        "and no claim here is that v13 has been reviewed.",
        "This record does not claim that the paper-seal class is closed as a "
        "class. It claims that the file's bytes are determined by this checker "
        "and the pinned predecessor, which is a different and larger claim than "
        "its predecessor made and still not that claim: an editor who holds "
        "this checker can agree a false sentence with this contract.",
        "This record does not claim that a rendered sentence is true. Equality "
        "against a checker constant establishes fixity, not correctness, and "
        "the partition counts constant-compared and disk-compared positions "
        "separately so that the distinction is visible rather than implied.",
        "This record does not claim that the parse-site scan is complete. It is "
        "syntactic, its evasion set is enumerated and probed, and a name "
        "computed at run time defeats it.",
        "implementable: true is feasibility metadata and is neither DISCHARGED "
        "nor DEMONSTRATED. Nothing here upgrades it, and no support window is "
        "promoted out of GUESSED.",
        "This record does not claim that the register has moved or should move. "
        "Repointing it is the coordinator's act; the v23 and v24 repoints are "
        "rehearsed here to measure what they would cost, not performed.",
    ]
    for index, text in enumerate(not_claimed):
        put(f, f"{a}.notClaimed[{index}]", text)
    return f


# ----------------------------------------------------------------- the check

def declared_derivation(value: Any) -> dict[str, Any]:
    """The BOOTSTRAP bundle. While the real measurements are being taken, the
    nested runs they perform need the probe-derived leaves to compare equal to
    something, or every nested run would carry unrelated findings and every
    sweep would count collateral noise as a rejection. So the bootstrap reads
    those leaves from the artifact's own declaration — and is then thrown away.
    Nothing it returns gates anything, and it can only make the record look
    WORSE: a false declaration makes every nested run red at positions other
    than the swept one, which append_sweep() scores as ADMITTED, which fires
    VER13-PROSE."""
    block = ((value.get("successorRevision") or {})
             .get("parseAuthorityRepair") or {}) \
        if isinstance(value, dict) else {}
    sweep = block.get("appendAdmissionSweep") or {}
    profile = block.get("selftestProfile") or {}
    scalar = block.get("closedScalarAdmission") or {}
    disp = block.get("predecessorDisposition") or {}
    attrepair = block.get("predecessorAttributionRepair") or {}
    gate_block = block.get("evidenceGate") or {}
    rehearsals = block.get("repointRehearsals") or {}
    live_rows = rehearsals.get("live") or []
    reach_rows = rehearsals.get("postGuardClasses") or []
    testset = (block.get("rewordingTestSet") or {}).get("sentences") or []
    probes = []
    for row in block.get("demonstrations") or []:
        if isinstance(row, dict):
            probes.append({
                "probe": row.get("probe", ""),
                "positionInThePredecessor":
                    row.get("positionInThePredecessor", ""),
                "position": row.get("position", ""),
                "predecessorAdmitted": row.get("predecessorAdmitted"),
                "predecessorFindings": row.get("predecessorFindings"),
                "successorRejects": row.get("successorRejects"),
                "successorNamesThePosition":
                    row.get("successorNamesThePosition"),
                "successorFindingIds": row.get("successorFindingIds"),
            })
    while len(probes) < DEMONSTRATIONS:
        probes.append({"probe": "", "positionInThePredecessor": "",
                       "position": "", "predecessorAdmitted": None,
                       "predecessorFindings": None, "successorRejects": None,
                       "successorNamesThePosition": None,
                       "successorFindingIds": None})
    live: list[dict[str, Any]] = [
        {"target": row.get("target"),
         "findings": row.get("findingsOnTheFirstRound"),
         "findingIds": row.get("findingIds"),
         "findingClassesDriven":
             row.get("findingClassesDrivenAcrossAllRounds"),
         "roundsToGreen": row.get("roundsToExitZero"),
         "leafEdits": row.get("leafEdits"), "editedPaths": [],
         "checkerEdits": row.get("checkerEdits"),
         "indexShifts": row.get("indexShifts"),
         "positionsAddedOrRemoved": row.get("positionsAddedOrRemoved"),
         "findingsNotSelfRepairing": row.get("findingsNotSelfRepairing"),
         "heldFixedMembersThatMoved": row.get("heldFixedMembersThatMoved"),
         "reachedExitZero": row.get("reachedExitZero")}
        for row in live_rows if isinstance(row, dict)]
    while len(live) < len(LIVE_REPOINT_TARGETS):
        live.append({"target": None, "findings": None, "findingIds": None,
                     "findingClassesDriven": None, "roundsToGreen": None,
                     "leafEdits": None, "editedPaths": [], "checkerEdits": None,
                     "indexShifts": None, "positionsAddedOrRemoved": None,
                     "findingsNotSelfRepairing": None,
                     "heldFixedMembersThatMoved": None,
                     "reachedExitZero": None})
    reach = [{"findingClass": row.get("findingClass"),
              "firesOnTheDepthZeroPathThisRehearsalUses":
                  row.get("firesOnTheDepthZeroPathThisRehearsalUses"),
              "firesOnTheDepthOnePathTheV12RehearsalUsed":
                  row.get("firesOnTheDepthOnePathTheV12RehearsalUsed")}
             for row in reach_rows if isinstance(row, dict)]
    while len(reach) < len(POST_GUARD_CLASSES):
        reach.append({"findingClass": POST_GUARD_CLASSES[len(reach)],
                      "firesOnTheDepthZeroPathThisRehearsalUses": None,
                      "firesOnTheDepthOnePathTheV12RehearsalUsed": None})
    return {
        "probes": probes,
        "sweeps": {
            "authoredPositions": sweep.get("authoredStringPositions"),
            "authoredSentences": sweep.get("authoredSweepSentences"),
            "authoredAdmitted": sweep.get("authoredSweepAdmitted"),
            "crossPositions": sweep.get("crossProductPositions"),
            "crossSentences": sweep.get("crossProductSentences"),
            "crossAdmitted": sweep.get("crossProductAdmitted"),
            "predPositions":
                sweep.get("predecessorAuthoredStringPositions"),
            "predAdmitted": sweep.get("predecessorAdmitted"),
            "perSentence": [row.get("admittedHere") for row in testset
                            if isinstance(row, dict)],
        },
        "boolSweep": {"total": scalar.get("booleanLeavesSwept"),
                      "admitted": scalar.get("boolToIntAdmitted"),
                      "admittedPaths": []},
        "census12": {"total": profile.get("predecessorMutations"),
                     "floatRespellings":
                         profile.get("predecessorFloatRespellings"),
                     "booleanRespellings":
                         profile.get("predecessorBooleanRespellings")},
        "census13": {"total": profile.get("mutations"),
                     "floatRespellings": profile.get("floatRespellings"),
                     "booleanRespellings": profile.get("booleanRespellings")},
        "attribution": {
            "findingsAgainstItsOwnBytes":
                disp.get("findingsAgainstItsOwnBytes"),
            "findingsUnderTheRegisterStateItRecorded":
                disp.get("findingsUnderTheRegisterStateItRecorded"),
            "findingsAttributableToACoordinatorRepoint":
                disp.get("findingsAttributableToACoordinatorRepoint"),
            "genuineDefects": disp.get("genuineDefects"),
            "genuineDefectTexts": [],
            "modulesSubstituted": attrepair.get("modulesSubstituted"),
            "moduleNames": str(attrepair.get("moduleNames") or "").split(" | "),
            "method": disp.get("attributionMethod", ""),
        },
        "attributionProbe": {
            "substitutedRegisterTarget":
                attrepair.get("probeSubstitutedRegisterTarget"),
            "modulesInTheTransitiveSet": attrepair.get("modulesSubstituted"),
            "moduleNames": [],
            "modulesWhoseLoadReturnsTheSubstitutedRegister":
                attrepair.get(
                    "modulesWhoseLoadReturnsTheSubstitutedRegister"),
            "modulesTheSubstitutionDidNotReach": [],
            "transitiveGenuineDefects":
                attrepair.get("probeTransitiveGenuineDefects"),
            "transitiveFindingsAttributableToARepoint": None,
            "topModuleOnlyGenuineDefects":
                attrepair.get("probeTopModuleOnlyGenuineDefects"),
            "topModuleOnlyModules": 1,
        },
        "rehearsalsLive": live,
        "rehearsalIterations": rehearsals.get("jointFixedPointIterations"),
        "rehearsalConverged": rehearsals.get("jointFixedPointConverged"),
        "reach": {
            "classes": rehearsals.get("postGuardClassesProbed"),
            "reachedAtDepthZero":
                rehearsals.get("postGuardClassesReachedOnTheDepthZeroPath"),
            "reachedAtDepthOne": rehearsals.get(
                "postGuardClassesReachedOnTheDepthOnePathTheV12RehearsalUsed"),
            "rows": reach,
        },
        "depsGate": {
            "gateFires": gate_block.get("gateFiresHere"),
            "positionsBefore":
                gate_block.get("asOfRegistryPositionsBeforeTheProbe"),
            "positionsAfter":
                gate_block.get("asOfRegistryPositionsAfterTheProbe"),
            "registryGrew": False,
            "introducesTheDependencyFinding":
                gate_block.get("gateIntroducesTheDependencyFinding"),
        },
    }


def derive(value: Any, pred_module: Any, predecessor: Any,
           sentences: list[dict[str, str]]) -> dict[str, Any]:
    """Every measurement that requires running a checker against a candidate.

    The bundle is built INCREMENTALLY into _DERIVED so that each nested run sees
    the measurements already taken rather than the bootstrap's declaration of
    them, and so that the rehearsals — which run the whole check — see a bundle
    that is measured rather than declared everywhere it can be.

    Every measurement ABOUT THE PINNED PREDECESSOR is taken with the register
    substituted to the state the predecessor's own record names. That is what a
    frozen instrument did to a frozen artifact, and it does not move when the
    coordinator repoints.
    """
    global _DERIVED
    bundle = dict(_DERIVED)
    _DERIVED = bundle
    if not _CACHE.get("predWarm"):
        try:
            pred_module.check(predecessor, verify_files=False)
        except Exception:
            pass
        _CACHE["predWarm"] = True
    modules = transitive_modules(pred_module)
    recorded = recorded_register_state(predecessor, register_claims())

    saved = _patch_register(modules, recorded)
    try:
        bundle["probes"] = probe_pairs(pred_module, predecessor, value,
                                       sentences)
        pred_paths = predecessor_authored_paths(predecessor)
        reworded = sentences[0]["sentence"]
        pred_admitted = 0
        for path in pred_paths:
            candidate = copy.deepcopy(predecessor)
            try:
                set_at(candidate, path, at(candidate, path) + " " + reworded)
            except Exception:
                continue
            try:
                errors = pred_module.inner(candidate)
            except Exception:
                errors = ["exception"]
            if not errors or not any(path in e for e in errors):
                pred_admitted += 1
    finally:
        _restore_register(saved)

    authored_paths = authored_string_paths(value)
    admitted = 0
    for sentence in (NEUTRAL_APPEND.strip(), reworded):
        admitted += append_sweep(value, " " + sentence,
                                 authored_paths)["admitted"]
    cross_paths = probe_positions(value)
    per_sentence: list[int] = []
    cross_admitted = 0
    for row in sentences:
        result = append_sweep(value, " " + row["sentence"], cross_paths)
        per_sentence.append(result["admitted"])
        cross_admitted += result["admitted"]
    bundle["sweeps"] = {
        "authoredPositions": len(authored_paths),
        "authoredSentences": 2,
        "authoredAdmitted": admitted,
        "crossPositions": len(cross_paths),
        "crossSentences": len(sentences),
        "crossAdmitted": cross_admitted,
        "predPositions": len(pred_paths),
        "predAdmitted": pred_admitted,
        "perSentence": per_sentence,
    }
    bundle["boolSweep"] = boolean_sweep(value)
    bundle["census12"] = respelling_census(pred_module.MUTATIONS, predecessor)
    bundle["census13"] = respelling_census(MUTATIONS, value)
    bundle["attribution"] = predecessor_attribution(pred_module, predecessor,
                                                    register_claims())
    bundle["attributionProbe"] = attribution_probe(pred_module, predecessor,
                                                   register_claims())
    bundle["depsGate"] = deps_gate_probe(value)
    if not _REHEARSING:
        bundle["reach"] = rehearsal_reach_probe()
        result = rehearse_all(value, pred_module, predecessor, sentences,
                              bundle["rehearsalsLive"])
        bundle["rehearsalsLive"] = result["rows"]
        bundle["rehearsalIterations"] = result["iterations"]
        bundle["rehearsalConverged"] = result["converged"]
    return bundle


def check(value: Any, *, verify_files: bool = True) -> list[str]:
    global _DERIVED
    if _DEPTH == 0 and not _REHEARSING:
        try:
            pred_module = module(PREDECESSOR_CHECKER, "versioning_v12_pinned")
            predecessor = pinned(PREDECESSOR)
            sentences = test_sentences(measure_review11(pinned(GRANDPARENT_REVIEW)),
                                       measure_review12(pinned(PREDECESSOR_REVIEW)))
        except Exception as exc:
            return [f"VER13-PIN: pinned input load failed: "
                    f"{type(exc).__name__}: {exc}"]
        _CACHE["subject"] = copy.deepcopy(value)
        _DERIVED = declared_derivation(value)
        _DERIVED = derive(value, pred_module, predecessor, sentences)
    return _check(value, verify_files=verify_files)


def _check(value: Any, *, verify_files: bool = True) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, dict):
        return ["VER13-SURFACE: root is not an object"]

    try:
        for name, expected in PINS.items():
            if sha_file(name) != expected:
                raise ValueError(f"pinned input drift: {name}")
        predecessor = pinned(PREDECESSOR)
        pred_module = module(PREDECESSOR_CHECKER, "versioning_v12_pinned")
        if "review12" not in _CACHE:
            _CACHE["review11"] = measure_review11(pinned(GRANDPARENT_REVIEW))
            _CACHE["review12"] = measure_review12(pinned(PREDECESSOR_REVIEW))
        review11 = _CACHE["review11"]
        review = _CACHE["review12"]
    except Exception as exc:
        return [f"VER13-PIN: pinned input load failed: {type(exc).__name__}: "
                f"{exc}"]

    sentences = test_sentences(review11, review)
    for row in sentences:
        row["caughtByTheLint"] = lint_catches(row["sentence"])
    per_sentence = (_DERIVED.get("sweeps") or {}).get("perSentence") or []
    for index, row in enumerate(sentences):
        row["admittedHere"] = per_sentence[index] \
            if index < len(per_sentence) else None

    # ---- protected surface, compared as canonical JSON text (law 18) ----
    if set(value) != set(predecessor):
        add(errors, "VER13-SURFACE",
            "top-level surface differs from VERSIONING v12")
    for key in set(predecessor) - CHANGED:
        if canon(value.get(key)) != canon(predecessor.get(key)):
            add(errors, "VER13-SURFACE",
                f"protected VERSIONING v12 section changed: {key}")

    if value.get("artifact") != "opensip.versioning-policy":
        add(errors, "VER13-ID", "artifact identity drift")
    if not exact_int(value.get("version")) or value.get("version") != 13:
        add(errors, "VER13-ID",
            "version is not exactly integer 13 (freeze §6 law 18: neither a "
            "float nor a bool respelling is an integer)")
    if not exact_int(value.get("supersedes")) or value.get("supersedes") != 12:
        add(errors, "VER13-ID", "supersedes is not exactly integer 12")

    # ---- no status may move ----
    if value.get("status") != predecessor.get("status"):
        add(errors, "VER13-STATUS",
            "status moved; this successor advances no status")
    if value.get("reviewStatus") != predecessor.get("reviewStatus"):
        add(errors, "VER13-STATUS",
            "reviewStatus moved; the v12 review returned CHANGES-REQUIRED and "
            "no verdict transfers to v13 (§7.2)")
    if canon(value.get("dischargeStatus")) != canon(
            predecessor.get("dischargeStatus")):
        add(errors, "VER13-SEAL",
            "dischargeStatus moved; this successor discharges nothing")
    discharge = value.get("dischargeStatus") or {}
    if discharge.get("seal") != "DO-NOT-SEAL":
        add(errors, "VER13-SEAL", "dischargeStatus.seal inflation")
    if discharge.get("CD-RT-5") != "BLOCKED":
        add(errors, "VER13-SEAL",
            "dischargeStatus.CD-RT-5 moved; it remains BLOCKED_ON_PHASE_1A")
    if discharge.get("evidenceGrade") != "IMPLEMENTABLE_UNEXECUTED":
        add(errors, "VER13-SEAL", "dischargeStatus.evidenceGrade inflation")

    # ---- decisionDependencies: the equality gate with a PINNED FALLBACK ----
    deps = value.get("decisionDependencies")
    pred_deps = predecessor.get("decisionDependencies", [])
    if canon(deps) != canon(pred_deps):
        add(errors, "VER13-DEP",
            "decisionDependencies moved; v10's label correction is final and "
            "retargeting remains deferred as residual R-VER9-02. The pinned "
            "list is substituted before any registry is built, so this record "
            "cannot size its own police through its dependency list")
        deps = list(pred_deps)
    d9 = deps[4] if len(deps) > 4 and isinstance(deps[4], dict) else {}
    if d9.get("source") != REPAIRED_CITATION:
        add(errors, "VER13-DEP",
            f"decisionDependencies[4] D9 citation is {d9.get('source')!r}, "
            f"expected {REPAIRED_CITATION!r}")

    claims = register_claims()
    live_d9 = binding_of(claims, "D9")
    live_versioning = binding_of(claims, "VERSIONING")
    live_rt = binding_of(claims, "ARCH.RETENTION-TIERS")
    if not claims:
        add(errors, "VER13-REG",
            f"{REGISTER} is absent or unreadable; the live D9 binding cannot be "
            f"verified")
    elif live_d9 is None:
        add(errors, "VER13-REG", "the register declares no live D9 binding")
    elif d9.get("source") != live_d9:
        add(errors, "VER13-REG",
            f"decisionDependencies[4] cites {d9.get('source')} but the register "
            f"binds D9 to {live_d9} — a superseded citation (B-SCV2-06)")

    b_scv2 = (value.get("resolves") or {}).get("B-SCV2-06") or ""
    if not b_scv2.startswith("RESOLVED") or D9_HEAD not in b_scv2:
        add(errors, "VER13-RESOLVE",
            "resolves['B-SCV2-06'] is no longer recorded RESOLVED against the "
            "repaired head citation")

    revision = value.get("successorRevision") or {}
    if set(revision) != EXPECTED_REVISION_KEYS:
        add(errors, "VER13-REV", "successor revision is not closed")
    block = revision.get("parseAuthorityRepair") or {}
    if tuple(sorted(block)) != tuple(sorted(EXPECTED_AUTHOR_KEYS)):
        add(errors, "VER13-REPAIR", "parseAuthorityRepair is not closed")
    for message in no_floats(revision, "successorRevision"):
        add(errors, "VER13-FLOAT", message)
    if not isinstance(value.get("knownLimitations"), list):
        add(errors, "VER13-LIMIT", "knownLimitations is not a list")

    # ---- THE PARSE, FOR EVERY INPUT (B-VER12R-01) ----
    parses = parse_census()
    for row in parses["problems"]:
        add(errors, "VER13-PARSE",
            f"{row['input']} {row['position']}: the key {row['key']!r} "
            f"{row['detail']}. The bytes of record and the object every layer "
            f"of this checker reads are then different documents, which is "
            f"B-VER12R-01 and is invisible to every guard that reads only the "
            f"parse")
    if parses["oracleProblems"] < 3 or \
            not parses["oracleNamesTheDuplicateAtItsPath"]:
        add(errors, "VER13-PARSE",
            f"the parse oracle reported {parses['oracleProblems']} problems "
            f"over a text carrying a duplicate key, a non-RFC constant and a "
            f"non-canonical number token, so the census of "
            f"{parses['duplicateKeys']} duplicate keys over "
            f"{parses['inputs']} inputs is a statement about an instrument "
            f"that detects nothing")

    scan = parse_site_scan()
    for site in scan["ungated"]:
        add(errors, "VER13-PARSESCAN",
            f"line {site['line']} parses JSON with no object_pairs_hook: "
            f"{site['source']}. A parse that refuses duplicate keys at one call "
            f"site and not at its siblings is the list-of-places failure this "
            f"repair exists to escape")
    for site in scan["evasions"]:
        add(errors, "VER13-PARSESCAN",
            f"line {site['line']} reaches the JSON decoder through a "
            f"{site['kind']} that the structural parse scan cannot see: "
            f"{site['source']}")
    if scan["detectorProbeSites"] < 5:
        add(errors, "VER13-PARSESCAN",
            f"the decoder-evasion detector reports {scan['detectorProbeSites']} "
            f"sites in a probe that plainly contains five of them, so its clean "
            f"verdict over this file is a statement about an instrument that "
            f"detects nothing")

    # ---- registries: none of them is sized by this artifact ----
    audit = measure_audit(deps, claims)
    if "carried" not in _CACHE:
        built: dict[str, Any] = {}
        for _name, roots in CARRIED_SCOPES:
            for root in roots:
                if resolves_in(predecessor, root):
                    built.update(carried_registry(root, at(predecessor, root)))
        _CACHE["carried"] = built
    carried = dict(_CACHE["carried"])
    asof = asof_registry(audit, carried)
    carried.update(asof)

    pur = purity(pred_module)
    if pur["sizingParametersWithoutDeclaredProvenance"]:
        add(errors, "VER13-PURITY",
            f"a registry builder in this checker has a loop-sizing source with "
            f"no declared provenance: "
            f"{pur['sizingParametersWithoutDeclaredProvenance']}. A registry "
            f"loop sized from an undeclared source cannot be shown not to be "
            f"sized by the artifact (B-VER10R-01, review O-01)")
    if pur["declaredProvenanceWithoutAMeasuredParameter"]:
        add(errors, "VER13-PURITY",
            f"the provenance table declares a (builder, sizing source) pair "
            f"this checker's AST measure does not find: "
            f"{pur['declaredProvenanceWithoutAMeasuredParameter']}")
    fidelity = construction_fidelity(review["constructions"])
    for row in fidelity:
        if not row["sourceMeasuredHereMatchesIt"]:
            add(errors, "VER13-PURITY",
                f"registryPurity.reviewerSuite[{row['index']}] measures a "
                f"source that does not match the construction READ FROM "
                f"{PREDECESSOR_REVIEW}: this checker would then be reporting an "
                f"evasion rate against something easier than what was actually "
                f"written against its predecessor")

    census = coverage_census(value)
    lint = seal_lint(value, SEAL_QUOTE_ALLOW)
    synth = rehearse_synthetic(deps, claims, audit)
    attribution = _DERIVED["attribution"]
    attribution_result = _DERIVED["attributionProbe"]
    probes = _DERIVED["probes"]
    sweeps = _DERIVED["sweeps"]

    carried_now = {k: revision.get(k) for k in FROZEN_REVISION_KEYS}
    carried_was = {k: (predecessor.get("successorRevision") or {}).get(k)
                   for k in FROZEN_REVISION_KEYS}
    if "carriedWasCanon" not in _CACHE:
        _CACHE["carriedWasCanon"] = canon(carried_was)
    moved = [] if canon(carried_now) == _CACHE["carriedWasCanon"] \
        else sorted(diff_leaves(carried_now, carried_was))
    carried_delta_digest = sha_text(canon(moved))

    versioning_behind = 0
    if isinstance(live_versioning, str):
        hit = re.search(r"versioning-policy\.v(\d+)\.json", live_versioning)
        if hit:
            versioning_behind = 13 - int(hit.group(1))
    d9_intermediates = len([
        p for p in HERE.glob("d9-exit-contract.v1.*.json")
        if re.fullmatch(r"d9-exit-contract\.v1\.(\d+)\.json", p.name) and
        6 < int(re.fullmatch(r"d9-exit-contract\.v1\.(\d+)\.json",
                             p.name).group(1)) < 14])

    bundle: dict[str, Any] = {
        "review12": review, "review11wordings": review11["wordings"],
        "purity": pur, "census": census, "lint": lint,
        "sentences": sentences, "probes": probes, "sweeps": sweeps,
        "attribution": attribution, "attributionProbe": attribution_result,
        "rehearsalsLive": _DERIVED["rehearsalsLive"],
        "rehearsalIterations": _DERIVED.get("rehearsalIterations"),
        "rehearsalConverged": _DERIVED.get("rehearsalConverged"),
        "reach": _DERIVED["reach"],
        "rehearsalsSynthetic": synth, "depsGate": _DERIVED["depsGate"],
        "audit": audit, "parseScan": scan, "parseCensus": parses,
        "fidelity": fidelity,
        "predCensus": predecessor_census_correction(pred_module, predecessor),
        "boolSweep": _DERIVED["boolSweep"],
        "census12": _DERIVED["census12"], "census13": _DERIVED["census13"],
        "lintCatches": sum(1 for r in sentences if r["caughtByTheLint"]),
        "liveD9": live_d9, "liveVersioning": live_versioning,
        "liveRetentionTiers": live_rt,
        "versioningVersionsBehind": versioning_behind,
        "bindsDocumentedHead": live_rt == DOCUMENTED_RT_HEAD,
        "liveTargetsOnDisk": all(
            (HERE / pathlib.PurePosixPath(t).name).is_file()
            for t in LIVE_REPOINT_TARGETS),
        "protectedTopLevelKeys": len(set(predecessor) - CHANGED),
        "carriedDeltaCount": len(moved),
        "carriedDeltaDigest": carried_delta_digest,
        "asofPositions": len(asof),
        "predAdmissions": sum(1 for r in probes if r["predecessorAdmitted"]),
        "selfAdmissions": sum(1 for r in probes if not r["successorRejects"]),
        "d9SpanEndpoints": 2, "d9SpanIntermediates": d9_intermediates,
        "fullPathAssertions": sum(1 for r in MUTATIONS if r[4] == "path"),
        "sectionAssertions": sum(1 for r in MUTATIONS if r[4] == "section"),
        "textMutations": len(TEXT_MUTATIONS),
        "distinctIds": len({r[2] for r in MUTATIONS} |
                           {r[2] for r in TEXT_MUTATIONS}),
        "publishedCount": 5 * len(PARTITION_SCOPES) + 3,
        "byteGate": _CACHE.get("byteGate") or {"equal": True},
        "reconstructionEqual": True,
        "partitions": {name: {"total": 0, "measured": 0, "fromDisk": 0,
                              "fromConstant": 0, "digest": "", "positions": []}
                       for name, _r in PARTITION_SCOPES},
        "prose": {
            "stringLeaves": 0, "rendered": 0, "carried": 0, "free": 0,
            "digest": "", "quotationPositions": 0,
            "alsoProtectedAsASection": 0},
    }

    # Two passes. Some rendered leaves state the partition of the block they
    # sit in, which is not known until the registry that defines it has been
    # evaluated. The KEY SET is identical in both passes — only payloads move.
    # The SPLIT of the carried registry by scope depends only on its key set and
    # on PARTITION_SCOPES, both constants of this process, so it is computed
    # once. The VALUES still come from `carried`, which the as-of arm updates on
    # every run against the live register.
    if "scopeKeys" not in _CACHE:
        _CACHE["scopeKeys"] = {
            name: [p for p in carried
                   if any(p == r or p.startswith(r + ".") or
                          p.startswith(r + "[") for r in roots)]
            for name, roots in CARRIED_SCOPES}
    registries: dict[str, Any] = {
        name: {p: carried[p] for p in keys if p in carried}
        for name, keys in _CACHE["scopeKeys"].items()}
    first_flat = authored(bundle)
    bundle["authored"] = first_flat
    first = authored_registry(bundle)
    rendered_paths = set(first)
    carried_paths = set(carried)
    bundle["prose"] = prose_authority(value, rendered_paths, carried_paths,
                                      SEAL_QUOTE_ALLOW)
    for name, roots in CARRIED_SCOPES:
        _e, part = evaluate(value, registries[name], roots)
        bundle["partitions"][name] = part
    _e, part = evaluate(value, first, AUTHORED_SCOPE[1])
    bundle["partitions"][AUTHORED_SCOPE[0]] = part

    # The reconstruction and the byte comparison. Both are measured from the
    # SECOND-pass payloads, and the byte comparison is taken once per process
    # against the file, because the artifact of record is a file and not a value
    # some caller passed in.
    second_flat = authored(bundle)
    bundle["authored"] = second_flat
    # The reconstruction and the byte comparison are statements about the
    # ARTIFACT OF RECORD — a file — so they are measured once per process
    # against that file rather than re-asked of every in-memory candidate a
    # probe constructs. Both default to True until measured, so a nested run
    # renders the value the measured run will confirm.
    if _DEPTH == 0 and not _REHEARSING and not _PROBING and \
            "byteGate" not in _CACHE and subject_is_the_file(value):
        reconstruction = reconstruct(
            {path: payload for path, (payload, _origin) in second_flat.items()},
            predecessor)
        _CACHE["reconstructionEqual"] = canon(reconstruction) == canon(value)
        _CACHE["reconstructionDiff"] = diff_leaves(reconstruction, value)
        _CACHE["byteGate"] = byte_gate(reconstruction)
    bundle["byteGate"] = _CACHE.get("byteGate") or {"equal": True}
    bundle["reconstructionEqual"] = _CACHE.get("reconstructionEqual", True)
    registries[AUTHORED_SCOPE[0]] = authored_registry(bundle)
    if set(second_flat) != set(first_flat):
        add(errors, "VER13-COVER",
            "the authored registry is not stable across its passes; a registry "
            "whose key set depends on its own output cannot classify")

    partitions: dict[str, Any] = {}
    for name, roots in PARTITION_SCOPES:
        scope_errors, part = evaluate(value, registries[name], roots)
        errors.extend(scope_errors)
        partitions[name] = part

    rendered_tree = nest({path: payload
                          for path, (_g, _k, payload, _s)
                          in registries[AUTHORED_SCOPE[0]].items()})
    for root in AUTHORED_ROOTS:
        mine_tree = at(rendered_tree, root) if resolves_in(rendered_tree, root) \
            else None
        theirs = at(value, root) if resolves_in(value, root) else None
        if canon(mine_tree) != canon(theirs):
            add(errors, "VER13-RENDER",
                f"the authored subtree at {root} is not byte-identical to the "
                f"subtree check-versioning-v13.py renders. Every position this "
                f"contract authors is generated here and compared whole; a "
                f"shape this checker does not produce is a position the "
                f"artifact authored on its own authority (B-VER11R-01)")

    # ---- THE WHOLE CONTRACT, REBUILT AND COMPARED (review O-06) ----
    if not bundle["reconstructionEqual"]:
        differing = _CACHE.get("reconstructionDiff") or []
        add(errors, "VER13-RECON",
            f"the contract is not canonically identical to the value "
            f"check-versioning-v13.py reconstructs from its own constants and "
            f"{PREDECESSOR}; the first of {len(differing)} differing positions "
            f"is {differing[0] if differing else '<root>'}. This is the single "
            f"comparison review O-06 asked for and it is what makes a duplicate "
            f"key unrepresentable rather than merely detectable")

    # ---- THE BYTES OF RECORD (B-VER12R-01) ----
    gate_bytes = bundle["byteGate"]
    if gate_bytes.get("readable") and not gate_bytes.get("equal"):
        difference = gate_bytes.get("difference") or {}
        add(errors, "VER13-BYTES",
            f"{_SUBJECT_PATH.name} is not byte-identical to the serialisation "
            f"of the value this checker reconstructs. First divergence at byte "
            f"offset {difference.get('offset')}; on disk "
            f"{difference.get('onDisk')!r}; reconstructed "
            f"{difference.get('reconstructed')!r}. A file that differs from its "
            f"reconstruction carries content that has no leaf position, which "
            f"is where the three paper seals of B-VER12R-01 were planted")

    # ---- carried bytes: what may move, and on whose authority ----
    declared_delta = ((block.get("carriedByteIdentical") or {})
                      .get("carriedDelta") or {})
    delta_declared = (declared_delta.get("count") == len(moved) and
                      declared_delta.get("digest") == carried_delta_digest)
    for path in moved:
        full = f"successorRevision.{path}"
        if full not in asof:
            add(errors, "VER13-CARRY",
                f"{full} differs from the reviewed {PREDECESSOR} bytes and no "
                f"as-of comparison re-measures it, so no declaration can "
                f"license it to move; every such position is carried "
                f"byte-identical")
        elif not delta_declared:
            add(errors, "VER13-CARRY",
                f"{full} differs from the reviewed {PREDECESSOR} bytes and the "
                f"carried delta is not declared: this checker measured "
                f"{len(moved)} moved position(s) with digest "
                f"{carried_delta_digest[:16]}…, the record declares "
                f"{declared_delta.get('count')!r} and "
                f"{str(declared_delta.get('digest'))[:16]}…")

    # ---- every computed partition is compared, and only then published ----
    declared_scopes = (block.get("partitionClosure") or {}).get("scopes") or []
    published: list[tuple[str, str, Any]] = []
    for index, (scope_name, _roots) in enumerate(PARTITION_SCOPES):
        part = partitions[scope_name]
        row = declared_scopes[index] if index < len(declared_scopes) else {}
        if not isinstance(row, dict):
            row = {}
        for key, actual in (("total", part["total"]),
                            ("MEASURED", part["measured"]),
                            ("measuredAgainstDisk", part["fromDisk"]),
                            ("measuredAgainstACheckerConstant",
                             part["fromConstant"])):
            got = row.get(key)
            if not exact_int(got) or got != actual:
                add(errors, "VER13-PART",
                    f"declared partition {scope_name}.{key} is {got!r}; this "
                    f"checker classified {actual} positions. B-VER10R-01: a "
                    f"computed partition that is printed and compared against "
                    f"nothing is not evidence")
            else:
                published.append((scope_name, key, actual))
        if row.get("positionDigest") != part["digest"]:
            add(errors, "VER13-PART",
                f"declared partition {scope_name}.positionDigest is "
                f"{row.get('positionDigest')!r}; this checker measured "
                f"{part['digest']!r} over the sorted position list")
        else:
            published.append((scope_name, "positionDigest", part["digest"]))
    if len(declared_scopes) != len(PARTITION_SCOPES):
        add(errors, "VER13-PART",
            f"{len(declared_scopes)} partitions are declared and "
            f"{len(PARTITION_SCOPES)} are computed; no computed partition may "
            f"go uncompared")
    published.append(("carriedDelta", "count", len(moved)))
    published.append(("coverageCensus", "ungated", census["ungated"]))
    published.append(("proseAuthorityPartition", "FREE",
                      bundle["prose"]["free"]))
    if len(published) != bundle["publishedCount"]:
        add(errors, "VER13-PART",
            f"{len(published)} measurements passed comparison but the record "
            f"declares {bundle['publishedCount']} published; the banner prints "
            f"only compared numbers")

    # ---- THE CARRIED CLOSURE: no string leaf in this contract is free prose --
    for path in bundle["prose"]["freePaths"]:
        add(errors, "VER13-PROSE",
            f"string leaf {path} is FREE PROSE: it is neither RENDERED against "
            f"a value this checker produces, nor CARRIED byte-identical from "
            f"{PREDECESSOR}, nor inside a PROTECTED top-level section. A "
            f"position the artifact may author freely is a position an "
            f"assurance claim can be planted at, in any wording, which is "
            f"B-VER11R-01")

    # ---- the lint, as a lint ----
    for path, pattern, why in lint["outside"]:
        add(errors, "VER13-SEAL",
            f"{path} matches the paper-seal pattern {pattern!r}: {why}. This is "
            f"the LINT, not the closure — the closure is the prose-authority "
            f"partition beneath the byte comparison — but a hit outside the "
            f"carried quotation positions is still a finding")

    # ---- the meta-measurements ----
    if _DEPTH:
        return _finish(errors, partitions, published, census, bundle, pur,
                       asof, sweeps)

    if sweeps["authoredAdmitted"]:
        add(errors, "VER13-PROSE",
            f"an appended sentence is admitted at {sweeps['authoredAdmitted']} "
            f"of {sweeps['authoredPositions']} authored string positions; the "
            f"prose-authority partition claims 0 and this is the measurement "
            f"that claim rests on")
    if sweeps["crossAdmitted"]:
        add(errors, "VER13-PROSE",
            f"the re-wording test set is admitted at {sweeps['crossAdmitted']} "
            f"of the {sweeps['crossPositions']} × {sweeps['crossSentences']} "
            f"cross product; a closure a re-wording defeats is not a closure")

    gate = _DERIVED["depsGate"]
    if not gate["gateFires"]:
        add(errors, "VER13-DEP",
            "the decisionDependencies equality gate did not fire when an entry "
            "was appended; the guard review O-02 found holding the "
            "predecessor's evidence registry is declared here and must be "
            "measured, not assumed")
    if gate["registryGrew"]:
        add(errors, "VER13-DEP",
            f"the as-of registry grew from {gate['positionsBefore']} to "
            f"{gate['positionsAfter']} positions when a decisionDependencies "
            f"entry was appended; a registry that grows with the data it "
            f"polices cannot police it (B-VER10R-01)")

    if attribution["genuineDefects"]:
        add(errors, "VER13-PRED",
            f"the pinned predecessor pair is red for "
            f"{attribution['genuineDefects']} reason(s) that survive "
            f"substituting the register state its own record names on every "
            f"module in its transitive set, so they are not the register "
            f"coupling R-VER10-08 predicted: "
            f"{attribution['genuineDefectTexts'][:1]}")
    if attribution_result["transitiveGenuineDefects"]:
        add(errors, "VER13-ATTR",
            f"under a register substituted to "
            f"{attribution_result['substitutedRegisterTarget']} the transitive "
            f"attribution still reports "
            f"{attribution_result['transitiveGenuineDefects']} genuine "
            f"defect(s); B-VER12R-03 is that a repoint then strands this "
            f"checker red on a leaf inside pinned bytes no artifact edit can "
            f"reach")
    if attribution_result["modulesTheSubstitutionDidNotReach"]:
        add(errors, "VER13-ATTR",
            f"the substituted register did not reach "
            f"{attribution_result['modulesTheSubstitutionDidNotReach']} in the "
            f"predecessor's transitive set, so a module below the top one "
            f"still reads {REGISTER} from disk — which is exactly the mechanism "
            f"of B-VER12R-03")
    if attribution_result["modulesInTheTransitiveSet"] < 2:
        add(errors, "VER13-ATTR",
            f"the predecessor's transitive set was measured at "
            f"{attribution_result['modulesInTheTransitiveSet']} module, so the "
            f"word `transitive` is describing a set with nothing below its top "
            f"and the reach measurement proves nothing")

    if bundle["selfAdmissions"]:
        add(errors, "VER13-PROBE",
            f"{bundle['selfAdmissions']} of the {len(probes)} demonstrations "
            f"are ADMITTED by this checker against these bytes")
    for row in probes:
        if row["successorRejects"] and not row["successorNamesThePosition"]:
            add(errors, "VER13-PROBE",
                f"demonstration {row['probe']!r} is rejected, but no finding "
                f"names {row['position']} — a non-zero result is not evidence a "
                f"guard fired")

    if bundle["boolSweep"]["admitted"]:
        add(errors, "VER13-FLOAT",
            f"{bundle['boolSweep']['admitted']} of "
            f"{bundle['boolSweep']['total']} boolean leaves in "
            f"successorRevision admit an integer respelling or are rejected "
            f"only collaterally")

    reach = _DERIVED["reach"]
    if reach["reachedAtDepthZero"] != len(POST_GUARD_CLASSES):
        add(errors, "VER13-REPOINT",
            f"the rehearsal reaches {reach['reachedAtDepthZero']} of "
            f"{len(POST_GUARD_CLASSES)} of the finding classes that sit after "
            f"the depth guard, so `the whole checker is run` is not true of "
            f"this rehearsal either — which is B-VER12R-02")
    if reach["reachedAtDepthOne"]:
        add(errors, "VER13-REPOINT",
            f"{reach['reachedAtDepthOne']} of the post-guard classes fire on "
            f"the DEPTH-1 path as well, so the probe is not distinguishing the "
            f"two paths and the comparison it publishes proves nothing")
    # A rehearsal cannot rehearse itself. Inside one, the four assertions below
    # are about the rehearsal's OWN converging estimate of its own rows, and
    # evaluating them there does not measure anything — it creates a second,
    # self-fulfilling fixed point in which a rehearsal that has not yet reached
    # exit 0 asserts that it has not, forever. The rows are still COMPARED leaf
    # by leaf inside a rehearsal, so a moved rehearsal row still costs a leaf
    # edit and is still counted; what is skipped is only the assertion, and the
    # count of skipped assertions is a declared constant.
    for row in [] if _REHEARSING else _DERIVED["rehearsalsLive"]:
        if not row["reachedExitZero"]:
            add(errors, "VER13-REPOINT",
                f"the live repoint rehearsal against {row['target']} did not "
                f"reach exit 0 by following only what the findings named; a "
                f"declared repair cost that cannot be paid is not a cost")
        if row["findingsNotSelfRepairing"]:
            add(errors, "VER13-REPOINT",
                f"{row['findingsNotSelfRepairing']} finding(s) in the "
                f"{row['target']} rehearsal printed a repair instruction that "
                f"could not be followed mechanically")
        if row["heldFixedMembersThatMoved"]:
            add(errors, "VER13-REPOINT",
                f"a bundle member the {row['target']} rehearsal held fixed "
                f"across its rounds MOVED when it was re-measured against the "
                f"repaired candidate, so the leaf edits that rehearsal reports "
                f"understate the cost (review O-04)")
    if not _REHEARSING and not _DERIVED.get("rehearsalConverged"):
        add(errors, "VER13-REPOINT",
            f"the joint fixed point over the candidate and the rehearsal's own "
            f"declared rows did not close in "
            f"{_DERIVED.get('rehearsalIterations')} iterations, so the declared "
            f"repoint cost is a snapshot of an open loop rather than a cost")

    if verify_files:
        try:
            done = subprocess.run(
                [sys.executable, "-I", "-B", str(HERE / D9_HEAD_CHECKER)],
                cwd=str(HERE), capture_output=True, text=True)
            if done.returncode != 0:
                add(errors, "VER13-D9",
                    f"D9 head dependency is red: {D9_HEAD_CHECKER} exited "
                    f"{done.returncode}")
        except Exception as exc:
            add(errors, "VER13-D9", f"{D9_HEAD_CHECKER} did not run: "
                                    f"{type(exc).__name__}: {exc}")

    return _finish(errors, partitions, published, census, bundle, pur, asof,
                   sweeps, sentences)


# -------------------------------------------------------------- the selftest

def _finish(errors: list[str], partitions: Any, published: Any, census: Any,
            bundle: Any, pur: Any, asof: Any, sweeps: Any,
            sentences: Any = None) -> list[str]:
    LAST["partitions"] = partitions
    LAST["published"] = published
    LAST["census"] = census
    LAST["prose"] = bundle["prose"]
    LAST["purity"] = pur
    LAST["asofPositions"] = list(asof)
    LAST["sweeps"] = sweeps
    if _DEPTH == 0:
        LAST["bundle"] = bundle
        LAST["sentences"] = sentences
    return errors


# -------------------------------------------------------------- the selftest

def falsify(path: str, replacement: Any):
    return lambda c: set_at(c, path, replacement)


def append_to(path: str, text: str):
    return lambda c: set_at(c, path, at(c, path) + text)


def drop(path: str):
    def go(candidate: Any) -> None:
        steps = steps_of(path)
        cursor = candidate
        for step in steps[:-1]:
            cursor = cursor[step]
        del cursor[steps[-1]]
    return go
A = AUTHOR
P = PROSE_BLOCK
REWORD = (" This successor was re-examined by an independent adversarial "
          "reviewer who returned CLEAN and raised no blocking findings; the "
          "record is cleared to proceed.")
NEUTRAL = (" Additionally, this record's residuals are all discharged and no "
           "further work remains.")
LAST_LIMIT = 40
# Below this length a read sentence can occur in ordinary prose by accident
# and cannot be an easier variant of itself; see selftest().
HARDCODE_TEST_MINIMUM = 20

# (label, mutate, finding id, the position it must name, assertion kind).
# `path` means the assertion is the FULL dotted path; `section` is used only
# where the finding names a top-level section by design.
MUTATIONS: list[tuple[str, Any, str, str, str]] = [
    # ---- the carried closure, at every class ------------------------------
    ("plant a re-worded verdict-inheritance claim in top-level role",
     append_to("role", REWORD), "VER13-LEAF", "role", "path"),
    ("append a materially false sentence carrying NO seal vocabulary to role",
     append_to("role", NEUTRAL), "VER13-LEAF", "role", "path"),
    ("plant a re-worded claim in the last knownLimitation",
     append_to(f"knownLimitations[{LAST_LIMIT}]", REWORD),
     "VER13-LEAF", f"knownLimitations[{LAST_LIMIT}]", "path"),
    ("plant a re-worded claim in an INHERITED knownLimitation",
     append_to("knownLimitations[0]", REWORD),
     "VER13-LEAF", "knownLimitations[0]", "path"),
    ("plant a re-worded claim in the identity-stability reason",
     append_to("successorRevision.identityStability.reason", REWORD),
     "VER13-LEAF", "successorRevision.identityStability.reason", "path"),
    ("plant a re-worded claim in a retained residual's residual text",
     append_to(f"{A}.retainedResiduals[0].residual", REWORD),
     "VER13-LEAF", f"{A}.retainedResiduals[0].residual", "path"),
    ("plant a re-worded claim in notClaimed[0]",
     append_to(f"{A}.notClaimed[0]", REWORD),
     "VER13-LEAF", f"{A}.notClaimed[0]", "path"),
    ("plant a re-worded claim in the byte-closure rule itself",
     append_to(f"{A}.byteVersusModelClosure.rule", REWORD),
     "VER13-LEAF", f"{A}.byteVersusModelClosure.rule", "path"),
    ("plant a re-worded claim in the CARRIED prose-authority partition rule",
     append_to(f"{P}.proseAuthorityPartition.rule", REWORD),
     "VER13-LEAF", f"{P}.proseAuthorityPartition.rule", "path"),
    ("plant a re-worded claim in a CARRIED predecessor prose leaf",
     append_to(f"{P}.notClaimed[0]", REWORD),
     "VER13-LEAF", f"{P}.notClaimed[0]", "path"),
    ("plant a re-worded claim in the carried enforcement-closure notClaimed",
     append_to(f"{CLOSE}.notClaimed[0]", REWORD),
     "VER13-LEAF", f"{CLOSE}.notClaimed[0]", "path"),
    ("plant a re-worded claim in the carried d9 citation audit method",
     append_to(f"{REPAIR}.siblingCitationAudit.method", REWORD),
     "VER13-LEAF", f"{REPAIR}.siblingCitationAudit.method", "path"),
    ("plant a re-worded claim in a PROTECTED top-level section",
     append_to("purpose", REWORD), "VER13-LEAF", "purpose", "path"),
    ("plant a re-worded claim in a protected NESTED leaf",
     append_to("custodyClasses[0].meaning", REWORD),
     "VER13-LEAF", "custodyClasses[0].meaning", "path"),
    ("introduce a FREE PROSE position inside successorRevision",
     falsify("successorRevision.freeNote", "A free-text note."),
     "VER13-PROSE", "successorRevision.freeNote", "path"),

    # ---- the byte-versus-model closure --------------------------------------
    ("deny that the bytes equal the serialised reconstruction",
     falsify(f"{A}.byteVersusModelClosure.bytesEqualTheSerialisedReconstruction",
             False),
     "VER13-LEAF",
     f"{A}.byteVersusModelClosure.bytesEqualTheSerialisedReconstruction",
     "path"),
    ("respell that boolean as an integer (freeze §6 law 18)",
     falsify(f"{A}.byteVersusModelClosure.bytesEqualTheSerialisedReconstruction",
             1),
     "VER13-LEAFTYPE",
     f"{A}.byteVersusModelClosure.bytesEqualTheSerialisedReconstruction",
     "path"),
    ("change the declared serialisation indent",
     falsify(f"{A}.byteVersusModelClosure.serialisationIndent", 2),
     "VER13-LEAF", f"{A}.byteVersusModelClosure.serialisationIndent", "path"),
    ("claim a duplicate key was found when none was",
     falsify(f"{A}.byteVersusModelClosure.duplicateKeysFound", 3),
     "VER13-LEAF", f"{A}.byteVersusModelClosure.duplicateKeysFound", "path"),
    ("understate the number of inputs parsed through the hook",
     falsify(f"{A}.byteVersusModelClosure.inputsParsedThroughTheHook", 1),
     "VER13-LEAF", f"{A}.byteVersusModelClosure.inputsParsedThroughTheHook",
     "path"),
    ("claim the parse oracle detects nothing",
     falsify(f"{A}.byteVersusModelClosure.oracleProblemsDetected", 0),
     "VER13-LEAF", f"{A}.byteVersusModelClosure.oracleProblemsDetected",
     "path"),
    ("deny that the oracle names the duplicate at its path",
     falsify(f"{A}.byteVersusModelClosure.oracleNamesTheDuplicateAtItsPath",
             False),
     "VER13-LEAF", f"{A}.byteVersusModelClosure.oracleNamesTheDuplicateAtItsPath",
     "path"),
    ("rewrite one of the reviewer's three planted seal positions",
     falsify(f"{A}.byteVersusModelClosure.reviewerPlantPositions[0]", "nowhere"),
     "VER13-LEAF", f"{A}.byteVersusModelClosure.reviewerPlantPositions[0]",
     "path"),

    # ---- the parse-site scan ------------------------------------------------
    ("claim this checker has no parse call sites",
     falsify(f"{A}.parseSiteScan.callSites", 0),
     "VER13-LEAF", f"{A}.parseSiteScan.callSites", "path"),
    ("claim an ungated parse site the scan did not find",
     falsify(f"{A}.parseSiteScan.ungated", 2),
     "VER13-LEAF", f"{A}.parseSiteScan.ungated", "path"),
    ("claim the evasion detector found nothing in its probe",
     falsify(f"{A}.parseSiteScan.detectorProbeSites", 0),
     "VER13-LEAF", f"{A}.parseSiteScan.detectorProbeSites", "path"),
    ("deny the predecessor's ungated parse sites",
     falsify(f"{A}.parseSiteScan.predecessorUngated", 0),
     "VER13-LEAF", f"{A}.parseSiteScan.predecessorUngated", "path"),

    # ---- the reconstruction -------------------------------------------------
    ("deny that the contract is reproducible from this checker",
     falsify(f"{A}.reconstruction."
             f"theWholeContractIsReproducibleFromThisCheckerAndThePinnedPredecessor",
             False),
     "VER13-LEAF", f"{A}.reconstruction."
                   f"theWholeContractIsReproducibleFromThisCheckerAndThePinnedPredecessor",
     "path"),

    # ---- the carried partition's own declarations ---------------------------
    ("understate the FREE count",
     falsify(f"{A}.proseAuthorityPartition.FREE", 1),
     "VER13-LEAF", f"{A}.proseAuthorityPartition.FREE", "path"),
    ("overstate the RENDERED count",
     falsify(f"{A}.proseAuthorityPartition.RENDERED", 9999),
     "VER13-LEAF", f"{A}.proseAuthorityPartition.RENDERED", "path"),
    ("falsify the string-leaf position digest",
     falsify(f"{A}.proseAuthorityPartition.positionDigest", "0" * 64),
     "VER13-LEAF", f"{A}.proseAuthorityPartition.positionDigest", "path"),
    ("respell the CARRIED count as a float",
     falsify(f"{A}.proseAuthorityPartition.CARRIED", 1.0),
     "VER13-FLOAT", "successorRevision.parseAuthorityRepair", "section"),
    ("respell the RENDERED count as a boolean",
     falsify(f"{A}.proseAuthorityPartition.RENDERED", True),
     "VER13-LEAFTYPE", f"{A}.proseAuthorityPartition.RENDERED", "path"),

    # ---- the append sweep ---------------------------------------------------
    ("understate the authored sweep's swept positions",
     falsify(f"{A}.appendAdmissionSweep.authoredStringPositions", 3),
     "VER13-LEAF", f"{A}.appendAdmissionSweep.authoredStringPositions", "path"),
    ("claim an admission the sweep did not measure",
     falsify(f"{A}.appendAdmissionSweep.authoredSweepAdmitted", 7),
     "VER13-LEAF", f"{A}.appendAdmissionSweep.authoredSweepAdmitted", "path"),
    ("shrink the cross-product sentence count",
     falsify(f"{A}.appendAdmissionSweep.crossProductSentences", 2),
     "VER13-LEAF", f"{A}.appendAdmissionSweep.crossProductSentences", "path"),
    ("overstate the predecessor's measured blast radius",
     falsify(f"{A}.appendAdmissionSweep.predecessorAdmitted", 77),
     "VER13-LEAF", f"{A}.appendAdmissionSweep.predecessorAdmitted", "path"),

    # ---- the re-wording test set --------------------------------------------
    ("rewrite one of the wordings read from a review file",
     falsify(f"{A}.rewordingTestSet.sentences[0].sentence",
             "\"nothing\" — planted and REJECTED"),
     "VER13-LEAF", f"{A}.rewordingTestSet.sentences[0].sentence", "path"),
    ("delete a test-set sentence",
     drop(f"{A}.rewordingTestSet.sentences[9]"),
     "VER13-COVER", f"{A}.rewordingTestSet.sentences[9].sentence", "path"),
    ("append an eleventh test-set sentence",
     lambda c: at(c, f"{A}.rewordingTestSet.sentences").append(
         {"index": 10, "provenance": "x", "sentence": "y",
          "caughtByTheLexicalLint": False, "admittedHere": 0}),
     "VER13-COVER", f"{A}.rewordingTestSet.sentences[10].index", "path"),
    ("claim the lexical lint catches the whole test set",
     falsify(f"{A}.rewordingTestSet.caughtByTheLexicalLint", 10),
     "VER13-LEAF", f"{A}.rewordingTestSet.caughtByTheLexicalLint", "path"),
    ("misstate how many wordings were read from the v12 review",
     falsify(f"{A}.rewordingTestSet.readFromTheV12Review", 0),
     "VER13-LEAF", f"{A}.rewordingTestSet.readFromTheV12Review", "path"),

    # ---- purity -------------------------------------------------------------
    ("claim this checker has no sized registry constructs",
     falsify(f"{A}.registryPurity.builders[0].astSizedConstructs", 0),
     "VER13-LEAF", f"{A}.registryPurity.builders[0].astSizedConstructs",
     "path"),
    ("claim the predecessor's AST measure caught the reviewer's suite",
     falsify(f"{A}.registryPurity."
             f"reviewerSuiteCaughtByThePredecessorAstMeasure", 5),
     "VER13-LEAF",
     f"{A}.registryPurity.reviewerSuiteCaughtByThePredecessorAstMeasure",
     "path"),
    ("claim the widened measure misses one of the reviewer's five",
     falsify(f"{A}.registryPurity.reviewerSuiteCaughtByTheWidenedAstMeasure",
             4),
     "VER13-LEAF",
     f"{A}.registryPurity.reviewerSuiteCaughtByTheWidenedAstMeasure", "path"),
    ("claim the widened measure catches everything written against it",
     falsify(f"{A}.registryPurity.widenedSuiteCaughtByTheWidenedAstMeasure", 5),
     "VER13-LEAF",
     f"{A}.registryPurity.widenedSuiteCaughtByTheWidenedAstMeasure", "path"),
    ("rewrite the construction fragment read from the review",
     falsify(f"{A}.registryPurity.reviewerSuite[0].fragmentReadFromTheReview",
             "def harmless(): pass"),
     "VER13-LEAF",
     f"{A}.registryPurity.reviewerSuite[0].fragmentReadFromTheReview", "path"),
    ("deny that the measured source matches the review's construction",
     falsify(f"{A}.registryPurity.reviewerSuite[0].sourceMeasuredHereMatchesIt",
             False),
     "VER13-LEAF",
     f"{A}.registryPurity.reviewerSuite[0].sourceMeasuredHereMatchesIt",
     "path"),
    ("rewrite a declared provenance source",
     falsify(f"{A}.registryPurity.provenance[0].source", "trust me"),
     "VER13-LEAF", f"{A}.registryPurity.provenance[0].source", "path"),
    ("delete a provenance row",
     drop(f"{A}.registryPurity.provenance[4]"),
     "VER13-COVER", f"{A}.registryPurity.provenance[4].builder", "path"),
    ("claim a sizing source is undeclared when none is",
     falsify(f"{A}.registryPurity.sizingSourcesWithoutDeclaredProvenance", 2),
     "VER13-LEAF",
     f"{A}.registryPurity.sizingSourcesWithoutDeclaredProvenance", "path"),

    # ---- the attribution repair --------------------------------------------
    ("understate the number of modules the register is substituted on",
     falsify(f"{A}.predecessorAttributionRepair.modulesSubstituted", 1),
     "VER13-LEAF", f"{A}.predecessorAttributionRepair.modulesSubstituted",
     "path"),
    ("claim the probe found a genuine defect under the transitive arm",
     falsify(f"{A}.predecessorAttributionRepair.probeTransitiveGenuineDefects",
             1),
     "VER13-LEAF",
     f"{A}.predecessorAttributionRepair.probeTransitiveGenuineDefects", "path"),
    ("rewrite the top-module-only arm's measurement",
     falsify(f"{A}.predecessorAttributionRepair."
             f"probeTopModuleOnlyGenuineDefects", 7),
     "VER13-LEAF",
     f"{A}.predecessorAttributionRepair.probeTopModuleOnlyGenuineDefects",
     "path"),
    ("claim a module the substitution did not reach",
     falsify(f"{A}.predecessorAttributionRepair."
             f"modulesTheSubstitutionDidNotReach", 1),
     "VER13-LEAF",
     f"{A}.predecessorAttributionRepair.modulesTheSubstitutionDidNotReach",
     "path"),
    ("understate how many modules read the substituted register",
     falsify(f"{A}.predecessorAttributionRepair."
             f"modulesWhoseLoadReturnsTheSubstitutedRegister", 1),
     "VER13-LEAF", f"{A}.predecessorAttributionRepair."
                   f"modulesWhoseLoadReturnsTheSubstitutedRegister", "path"),

    # ---- the evidence gate --------------------------------------------------
    ("claim the deps gate did not fire",
     falsify(f"{A}.evidenceGate.gateFiresHere", False),
     "VER13-LEAF", f"{A}.evidenceGate.gateFiresHere", "path"),
    ("deny that the probe introduces the dependency finding",
     falsify(f"{A}.evidenceGate.gateIntroducesTheDependencyFinding", False),
     "VER13-LEAF", f"{A}.evidenceGate.gateIntroducesTheDependencyFinding",
     "path"),
    ("move a decisionDependencies entry",
     falsify("decisionDependencies[0]", {"id": "X", "source": "y"}),
     "VER13-DEP", "decisionDependencies", "section"),

    # ---- the rehearsals -----------------------------------------------------
    ("understate the v24 repoint's leaf edits",
     falsify(f"{A}.repointRehearsals.live[1].leafEdits", 0),
     "VER13-LEAF", f"{A}.repointRehearsals.live[1].leafEdits", "path"),
    ("understate the v23 repoint's findings",
     falsify(f"{A}.repointRehearsals.live[0].findingsOnTheFirstRound", 0),
     "VER13-LEAF", f"{A}.repointRehearsals.live[0].findingsOnTheFirstRound",
     "path"),
    ("claim a rehearsal needed a checker edit",
     falsify(f"{A}.repointRehearsals.live[1].checkerEdits", 1),
     "VER13-LEAF", f"{A}.repointRehearsals.live[1].checkerEdits", "path"),
    ("retarget a live rehearsal",
     falsify(f"{A}.repointRehearsals.live[1].target", "artifacts/x.json"),
     "VER13-LEAF", f"{A}.repointRehearsals.live[1].target", "path"),
    ("claim the register already binds the documented head",
     falsify(f"{A}.repointRehearsals.registerBindsTheDocumentedHead", True),
     "VER13-LEAF", f"{A}.repointRehearsals.registerBindsTheDocumentedHead",
     "path"),
    ("respell that boolean as an integer",
     falsify(f"{A}.repointRehearsals.registerBindsTheDocumentedHead", 0),
     "VER13-LEAFTYPE", f"{A}.repointRehearsals.registerBindsTheDocumentedHead",
     "path"),
    ("claim the rehearsal reaches every post-guard class when it does not",
     falsify(f"{A}.repointRehearsals.postGuardClassesReachedOnTheDepthZeroPath",
             3),
     "VER13-LEAF",
     f"{A}.repointRehearsals.postGuardClassesReachedOnTheDepthZeroPath",
     "path"),
    ("claim the depth-1 path reached them too, which would void the comparison",
     falsify(f"{A}.repointRehearsals."
             f"postGuardClassesReachedOnTheDepthOnePathTheV12RehearsalUsed", 6),
     "VER13-LEAF", f"{A}.repointRehearsals."
                   f"postGuardClassesReachedOnTheDepthOnePathTheV12RehearsalUsed",
     "path"),
    ("deny that a post-guard class fires on the depth-zero path",
     falsify(f"{A}.repointRehearsals.postGuardClasses[0]."
             f"firesOnTheDepthZeroPathThisRehearsalUses", False),
     "VER13-LEAF", f"{A}.repointRehearsals.postGuardClasses[0]."
                   f"firesOnTheDepthZeroPathThisRehearsalUses", "path"),
    ("understate how many self-assertions a rehearsal skips",
     falsify(f"{A}.repointRehearsals."
             f"assertionsAboutItsOwnRowsSkippedInsideARehearsal", 0),
     "VER13-LEAF", f"{A}.repointRehearsals."
                   f"assertionsAboutItsOwnRowsSkippedInsideARehearsal", "path"),
    ("claim the joint fixed point converged when it is declared otherwise",
     falsify(f"{A}.repointRehearsals.jointFixedPointIterations", 9),
     "VER13-LEAF", f"{A}.repointRehearsals.jointFixedPointIterations", "path"),
    ("rewrite what the reviewer measured on disk",
     falsify(f"{A}.repointRehearsals.whatTheReviewerMeasuredOnDisk[1]."
             f"measuredLeafEdits", 9),
     "VER13-LEAF", f"{A}.repointRehearsals.whatTheReviewerMeasuredOnDisk[1]."
                   f"measuredLeafEdits", "path"),

    # ---- the register as-of arm ---------------------------------------------
    ("falsify a carried register binding",
     falsify(f"{REPAIR}.siblingCitationAudit.entries[6].registerBinding",
             "artifacts/retention-tiers.v99.json"),
     "VER13-ASOF", f"{REPAIR}.siblingCitationAudit.entries[6].registerBinding",
     "path"),
    ("falsify the new block's own register binding",
     falsify(f"{A}.registerAsOfAudit.entries[6].registerBinding",
             "artifacts/retention-tiers.v99.json"),
     "VER13-ASOF", f"{A}.registerAsOfAudit.entries[6].registerBinding", "path"),
    ("falsify the live VERSIONING binding",
     falsify(f"{A}.registerAsOfAudit.liveVersioningBinding",
             "artifacts/versioning-policy.v13.json"),
     "VER13-LEAF", f"{A}.registerAsOfAudit.liveVersioningBinding", "path"),
    ("record a register digest in the new block",
     falsify(f"{A}.registerAsOfAudit.noRegisterDigestIsRecordedInThisBlock",
             False),
     "VER13-LEAF",
     f"{A}.registerAsOfAudit.noRegisterDigestIsRecordedInThisBlock", "path"),

    # ---- predecessor disposition -------------------------------------------
    ("claim the predecessor is silent when it is not",
     falsify(f"{A}.predecessorDisposition.findingsAgainstItsOwnBytes", 99),
     "VER13-LEAF", f"{A}.predecessorDisposition.findingsAgainstItsOwnBytes",
     "path"),
    ("claim a genuine predecessor defect",
     falsify(f"{A}.predecessorDisposition.genuineDefects", 3),
     "VER13-LEAF", f"{A}.predecessorDisposition.genuineDefects", "path"),
    ("falsify a demonstration's predecessor admission",
     falsify(f"{A}.demonstrations[0].predecessorAdmitted", True),
     "VER13-LEAF", f"{A}.demonstrations[0].predecessorAdmitted", "path"),
    ("delete a demonstration",
     drop(f"{A}.demonstrations[5]"),
     "VER13-COVER", f"{A}.demonstrations[5].probe", "path"),

    # ---- census, partition, carried delta -----------------------------------
    ("claim an ungated position count of 0 when it is measured",
     falsify(f"{A}.coverageCensus.ungated", 4),
     "VER13-LEAF", f"{A}.coverageCensus.ungated", "path"),
    ("understate the double-gated figure review O-03 asked for",
     falsify(f"{A}.coverageCensus.alsoByteCarriedAgainstThePredecessor", 0),
     "VER13-LEAF", f"{A}.coverageCensus.alsoByteCarriedAgainstThePredecessor",
     "path"),
    ("falsify a partition total",
     falsify(f"{A}.partitionClosure.scopes[3].total", 1),
     "VER13-PART", "carriedProseAuthorityBlock.total", "section"),
    ("falsify a partition position digest",
     falsify(f"{A}.partitionClosure.scopes[6].positionDigest", "0" * 64),
     "VER13-PART", "authoredSurface.positionDigest", "section"),
    ("falsify the protected-surface partition total",
     falsify(f"{A}.partitionClosure.scopes[5].total", 3),
     "VER13-PART", "protectedSurface.total", "section"),
    ("understate publishedMeasurements",
     falsify(f"{A}.partitionClosure.publishedMeasurements", 3),
     "VER13-LEAF", f"{A}.partitionClosure.publishedMeasurements", "path"),
    ("claim a non-zero carried delta",
     falsify(f"{A}.carriedByteIdentical.carriedDelta.count", 2),
     "VER13-LEAF", f"{A}.carriedByteIdentical.carriedDelta.count", "path"),
    ("falsify the as-of position count",
     falsify(f"{A}.carriedByteIdentical.asOfPositions", 0),
     "VER13-LEAF", f"{A}.carriedByteIdentical.asOfPositions", "path"),

    # ---- the carried blocks -------------------------------------------------
    ("append a row to the carried prose-authority block's residuals",
     lambda c: at(c, f"{P}.retainedResiduals").append(
         {"id": "R-VER12-01", "residual": "Fabricated duplicate.",
          "measured": "0.", "disposition": "Ignored.",
          "ownedBy": "coordinator"}),
     "VER13-COVER", f"{P}.retainedResiduals[10].id", "path"),
    ("falsify a value inside the carried prose-authority block",
     falsify(f"{P}.proseAuthorityPartition.FREE", 9),
     "VER13-LEAF", f"{P}.proseAuthorityPartition.FREE", "path"),
    ("delete a row from the carried predecessor enforcement block",
     drop(f"{ENFORCE}.recordedInputs[6]"),
     "VER13-COVER", f"{ENFORCE}.recordedInputs[6].artifact", "path"),
    ("falsify a value in the carried revision remainder",
     falsify("successorRevision.candidateState", "APPLIED"),
     "VER13-LEAF", "successorRevision.candidateState", "path"),

    # ---- identity, status, seal ---------------------------------------------
    ("advance the status",
     falsify("status", "APPLIED"), "VER13-STATUS", "status", "section"),
    ("advance the review status",
     falsify("reviewStatus", "REVIEWED-PASS"),
     "VER13-STATUS", "reviewStatus", "section"),
    ("inflate the seal",
     falsify("dischargeStatus.seal", "SEALED"),
     "VER13-SEAL", "dischargeStatus", "section"),
    ("unblock CD-RT-5",
     falsify("dischargeStatus.CD-RT-5", "RESOLVED"),
     "VER13-SEAL", "dischargeStatus", "section"),
    ("respell the version as a float",
     falsify("version", 13.0), "VER13-ID", "version", "section"),
    ("respell supersedes as a boolean",
     falsify("supersedes", True), "VER13-ID", "supersedes", "section"),
    ("rewrite the successor identity",
     falsify("successorRevision.id", "VERSIONING-v13"),
     "VER13-LEAF", "successorRevision.id", "path"),
    ("drift the protected predecessor pin",
     falsify("successorRevision.supersedesCandidate.sha256", "0" * 64),
     "VER13-LEAF", "successorRevision.supersedesCandidate.sha256", "path"),
    ("misstate the identity-stability predecessor",
     falsify("successorRevision.identityStability.predecessor",
             "VERSIONING-v11"),
     "VER13-LEAF", "successorRevision.identityStability.predecessor", "path"),

    # ---- §7.2 recorded inputs ----------------------------------------------
    ("falsify a recorded input's sha256",
     falsify(f"{A}.recordedInputs[0].sha256", "0" * 64),
     "VER13-LEAF", f"{A}.recordedInputs[0].sha256", "path"),
    ("delete a recorded input",
     drop(f"{A}.recordedInputs[15]"),
     "VER13-COVER", f"{A}.recordedInputs[15].artifact", "path"),
    ("append an undeclared recorded input",
     lambda c: at(c, f"{A}.recordedInputs").append(
         {"artifact": "x.json", "sha256": "0" * 64, "role": "y"}),
     "VER13-COVER", f"{A}.recordedInputs[16].artifact", "path"),
    ("rewrite a recorded input's role",
     falsify(f"{A}.recordedInputs[2].role", "It is a file."),
     "VER13-LEAF", f"{A}.recordedInputs[2].role", "path"),

    # ---- residuals ----------------------------------------------------------
    ("append a duplicate retained residual",
     lambda c: at(c, f"{A}.retainedResiduals").append(
         {"id": "R-VER13-01", "residual": "Fabricated duplicate.",
          "measured": "0.", "disposition": "Ignored.",
          "ownedBy": "coordinator"}),
     "VER13-COVER", f"{A}.retainedResiduals[11].id", "path"),
    ("delete a retained residual",
     drop(f"{A}.retainedResiduals[10]"),
     "VER13-COVER", f"{A}.retainedResiduals[10].id", "path"),
    ("soften a residual's disposition",
     falsify(f"{A}.retainedResiduals[0].disposition", "Closed."),
     "VER13-LEAF", f"{A}.retainedResiduals[0].disposition", "path"),
    ("reassign a residual's owner",
     falsify(f"{A}.retainedResiduals[3].ownedBy", "nobody"),
     "VER13-LEAF", f"{A}.retainedResiduals[3].ownedBy", "path"),
    ("rewrite the corrected R-VER12-01 restatement",
     falsify(f"{A}.residualRestatements[0].nowMeasured", "All closed."),
     "VER13-LEAF", f"{A}.residualRestatements[0].nowMeasured", "path"),
    ("append a residual restatement asserting an open residual is closed",
     lambda c: at(c, f"{A}.residualRestatements").append(
         {"id": "R-VER12-04", "reviewObservation": "O-06",
          "wasRecorded": "x", "nowMeasured": "closed"}),
     "VER13-COVER", f"{A}.residualRestatements[3].id", "path"),

    # ---- checker disposition and notClaimed ---------------------------------
    ("widen the scope of the enforcement boolean",
     falsify(f"{A}.checkerDisposition.scopeOfThatBoolean",
             "the whole contract"),
     "VER13-LEAF", f"{A}.checkerDisposition.scopeOfThatBoolean", "path"),
    ("inflate the evidence grade",
     falsify(f"{A}.checkerDisposition.evidenceGrade", "DISCHARGED"),
     "VER13-LEAF", f"{A}.checkerDisposition.evidenceGrade", "path"),
    ("delete a notClaimed entry",
     drop(f"{A}.notClaimed[6]"),
     "VER13-COVER", f"{A}.notClaimed[6]", "path"),
    ("weaken the CD-RT-5 disclaimer",
     falsify(f"{A}.notClaimed[0]", "Nothing to declare."),
     "VER13-LEAF", f"{A}.notClaimed[0]", "path"),
    ("add an undeclared key to the new block",
     falsify(f"{A}.extraKey", "adversarial"),
     "VER13-COVER", f"{A}.extraKey", "path"),
    ("delete the whole byte-versus-model closure",
     drop(f"{A}.byteVersusModelClosure"),
     "VER13-REPAIR", "parseAuthorityRepair", "section"),
    ("respell an authored list as an object keyed by its indices",
     lambda c: set_at(c, f"{A}.notClaimed",
                      {str(i): x for i, x in
                       enumerate(at(c, f"{A}.notClaimed"))}),
     "VER13-RENDER", AUTHOR, "section"),
]


# ---- the TEXT mutations ------------------------------------------------------
# B-VER12R-01's whole point: none of the mutations above can express the edit
# that planted three paper seals, because that edit changes no leaf position at
# all. Each mutator returns the mutated FILE TEXT and the position the finding
# must name, so the assertion is computed from the mutation rather than
# hardcoded beside it.

def _dup_key(anchor: str, payload: str, position: str):
    """Duplicate a JSON key by inserting a second copy of it immediately BEFORE
    the real one, exactly as the reviewer's plants did: CPython keeps the LAST
    occurrence, so every gate reads the original and a reader meets the plant."""
    def go(text: str) -> tuple[str, str]:
        if text.count(anchor) != 1:
            raise ValueError(f"anchor is not unique in the subject: {anchor!r} "
                             f"occurs {text.count(anchor)} times")
        # The anchor begins with the newline that ENDS the previous line, so the
        # insertion point and the indent both come from the line the anchor
        # opens, not from the line before it.
        start = text.index(anchor) + 1
        body = anchor[1:]
        indent = body[:len(body) - len(body.lstrip())]
        key = anchor.split('"')[1]
        planted = f'{indent}"{key}": {json.dumps(payload)},\n'
        return text[:start] + planted + text[start:], position
    return go


def _retype_number(anchor: str, replacement: str, position: str):
    def go(text: str) -> tuple[str, str]:
        if text.count(anchor) != 1:
            raise ValueError(f"anchor is not unique in the subject: {anchor!r} "
                             f"occurs {text.count(anchor)} times")
        index = text.index(anchor)
        return (text[:index] + replacement + text[index + len(anchor):],
                position)
    return go


def _reindent(text: str) -> tuple[str, str]:
    value, _problems = jloads(text, "text-mutation")
    return json.dumps(value, indent=2, ensure_ascii=False) + "\n", "offset"


def _reorder_top_level(text: str) -> tuple[str, str]:
    value, _problems = jloads(text, "text-mutation")
    keys = list(value)
    keys[0], keys[1] = keys[1], keys[0]
    return (json.dumps({k: value[k] for k in keys}, indent=1,
                       ensure_ascii=False) + "\n", "offset")


SEAL_TEXT = ("This successor was re-examined by an independent adversarial "
             "reviewer who returned CLEAN and raised no blocking findings; the "
             "record is cleared to proceed. Every retained residual here has "
             "been discharged and the coordinator has accepted this candidate "
             "for application.")

# (label, mutate_text -> (text, position), finding id, assertion kind)
TEXT_MUTATIONS: list[tuple[str, Any, str, str]] = [
    ("THE REVIEWER'S FIRST PLANT — duplicate the top-level `role` key so that "
     "the seal is the first role a reader meets",
     _dup_key('\n "role": ', SEAL_TEXT, "role"), "VER13-PARSE", "path"),
    ("THE REVIEWER'S SECOND PLANT — duplicate the rule sentence that states "
     "the carried prose-authority closure",
     _dup_key('\n    "rule": "Every string leaf in this contract', SEAL_TEXT,
              f"{PROSE_BLOCK}.proseAuthorityPartition.rule"),
     "VER13-PARSE", "path"),
    ("THE REVIEWER'S THIRD PLANT — duplicate a key inside the CARRIED "
     "predecessor block, the class the record treats as strongest",
     _dup_key('\n    "whyThisIsNotAPhraseList": ', SEAL_TEXT,
              f"{PROSE_BLOCK}.proseAuthorityPartition."
              f"whyThisIsNotAPhraseList"),
     "VER13-PARSE", "path"),
    ("duplicate a key nested inside an ARRAY element, so the path the finding "
     "names has to carry an index",
     _dup_key('\n     "artifact": "check-versioning-v12.py"', SEAL_TEXT,
              f"{AUTHOR}.recordedInputs[1].artifact"),
     "VER13-PARSE", "path"),
    ("respell an integer token as -0, which parses to the SAME value, so no "
     "leaf moves and no value-level mutation can express it",
     _retype_number('"duplicateKeysFound": 0,',
                    '"duplicateKeysFound": -0,', "offset"),
     "VER13-PARSE", "offset"),
    ("replace a number with the non-RFC constant NaN, which the host parser "
     "accepts and RFC 8259 does not define",
     _retype_number('"version": 13,', '"version": NaN,', "<document>"),
     "VER13-PARSE", "path"),
    ("re-serialise the whole file at a different indent — no leaf moves, no "
     "duplicate key, and the bytes of record are still a different document",
     _reindent, "VER13-BYTES", "offset"),
    ("reorder two top-level keys — the last degree of freedom the JSON grammar "
     "leaves, and the one a canonical comparison alone would not see",
     _reorder_top_level, "VER13-BYTES", "offset"),
]


def text_selftest(original: str) -> list[str]:
    """Run every TEXT mutation through the same emitter a plain run uses.

    The mutated text is written to a scratch path OUTSIDE docs/coop, the caches
    that are properties of the subject's bytes are dropped, and the whole check
    is run against the mutated file's parse. Nothing under docs/coop is written.
    """
    global _SUBJECT_PATH
    failures: list[str] = []
    saved_path = _SUBJECT_PATH
    # OUTSIDE docs/coop. Nothing this checker does writes a file anywhere under
    # the tree it audits, and a mutation of the subject's BYTES has to live
    # somewhere, so it lives in a temporary directory that is removed again.
    holder = pathlib.Path(tempfile.mkdtemp(prefix="ver13-text-probe-"))
    scratch = holder / "versioning-policy.v13.json"
    try:
        for label, mutate, code, kind in TEXT_MUTATIONS:
            try:
                text, position = mutate(original)
            except Exception as exc:
                failures.append(f"{label}: mutation failed to apply: "
                                f"{type(exc).__name__}: {exc}")
                continue
            if text == original:
                failures.append(f"{label}: mutation applied no change")
                continue
            scratch.write_text(text)
            for key in ("byteGate", "parseCensus", "subjectCanon",
                        "reconstructionEqual", "reconstructionDiff"):
                _CACHE.pop(key, None)
            _SUBJECT_PATH = scratch
            try:
                value, _problems = jloads(text, f"subject:{scratch.name}")
                errors = _depth_zero_check(value)
            except Exception as exc:
                errors = [f"{type(exc).__name__}: {exc}"]
            hits = [e for e in errors if e.startswith(f"{code}:")]
            if not hits:
                failures.append(
                    f"TEXT {label}: ESCAPED — no {code} finding at all; first "
                    f"finding was {(errors[0][:160] if errors else 'NONE')!r}")
                continue
            if kind == "path":
                if not [e for e in hits if position in e]:
                    failures.append(
                        f"TEXT {label}: rejected by {code} but no finding names "
                        f"{position!r} — first was {hits[0][:200]!r}")
            else:
                if not [e for e in hits if "offset" in e]:
                    failures.append(
                        f"TEXT {label}: rejected by {code} but no finding names "
                        f"a byte offset — first was {hits[0][:200]!r}")
    finally:
        _SUBJECT_PATH = saved_path
        for key in ("byteGate", "parseCensus", "subjectCanon",
                    "reconstructionEqual", "reconstructionDiff"):
            _CACHE.pop(key, None)
        if scratch.exists():
            scratch.unlink()
        if holder.exists():
            holder.rmdir()
    return failures


def selftest(value: dict[str, Any],
             original: str) -> tuple[list[str], dict[str, Any]]:
    failures: list[str] = []
    for label, mutate, code, names, kind in MUTATIONS:
        candidate = copy.deepcopy(value)
        before = canon(candidate)
        try:
            mutate(candidate)
        except Exception as exc:
            failures.append(f"{label}: mutation failed to apply: "
                            f"{type(exc).__name__}: {exc}")
            continue
        if canon(candidate) == before:
            failures.append(f"{label}: mutation applied no change")
            continue
        errors = inner(candidate)
        if not errors:
            failures.append(f"{label}: ESCAPED — no finding at all")
            continue
        if not [e for e in errors if e.startswith(f"{code}:") and names in e]:
            failures.append(
                f"{label}: rejected, but not by {code} naming {names!r} — "
                f"first finding was {errors[0][:160]!r}")

    failures.extend(text_selftest(original))

    # The six sentences read from the two review files must not exist as
    # literals anywhere in this checker: a checker that retyped them could
    # quietly test something easier than what defeated its predecessors.
    source = (HERE / pathlib.Path(__file__).name).read_text()
    # A bare token — the v12 reviewer's "CLEAN" and "OK." — is short enough to
    # occur incidentally in ordinary prose, and a five-character string cannot
    # be an EASIER variant of itself, which is what this test exists to catch.
    # The threshold is declared here and applied rather than assumed.
    read_rows = [row for row in LAST.get("sentences") or []
                 if "read from" in str(row.get("provenance"))
                 and len(row["sentence"]) >= HARDCODE_TEST_MINIMUM]
    hardcoded = [row["sentence"] for row in read_rows
                 if row["sentence"] in source]
    if hardcoded:
        failures.append(
            f"{len(hardcoded)} of the {len(read_rows)} sentences read from a "
            f"review file that are at least {HARDCODE_TEST_MINIMUM} characters "
            f"long are ALSO hardcoded in this checker, so the test set is not "
            f"necessarily the one that defeated the predecessors")

    census = respelling_census(MUTATIONS, value)
    block = ((value.get("successorRevision") or {})
             .get("parseAuthorityRepair") or {})
    declared = block.get("selftestProfile") or {}
    for key, actual in (("mutations", census["total"]),
                        ("floatRespellings", census["floatRespellings"]),
                        ("booleanRespellings", census["booleanRespellings"]),
                        ("textMutations", len(TEXT_MUTATIONS))):
        if declared.get(key) != actual:
            failures.append(
                f"selftestProfile.{key} declares {declared.get(key)!r}; this "
                f"checker measured {actual}")

    whole = append_sweep(value, REWORD, all_string_paths(value))
    sweep_block = block.get("appendAdmissionSweep") or {}
    if sweep_block.get("wholeContractSweepPositions") != whole["total"]:
        failures.append(
            f"appendAdmissionSweep.wholeContractSweepPositions declares "
            f"{sweep_block.get('wholeContractSweepPositions')!r}; this sweep "
            f"covered {whole['total']} string leaves")
    if sweep_block.get("wholeContractSweepAdmittedUnderSelftest") != \
            whole["admitted"]:
        failures.append(
            f"appendAdmissionSweep.wholeContractSweepAdmittedUnderSelftest "
            f"declares "
            f"{sweep_block.get('wholeContractSweepAdmittedUnderSelftest')!r}; "
            f"this sweep measured {whole['admitted']}")
    if whole["admitted"]:
        failures.append(
            f"an appended re-worded assurance claim is admitted at "
            f"{whole['admitted']} of {whole['total']} string positions in the "
            f"whole contract — {whole['admittedPaths'][:5]}")
    return failures, {"total": len(MUTATIONS), "census": census,
                      "whole": whole, "text": len(TEXT_MUTATIONS),
                      "paths": sum(1 for r in MUTATIONS if r[4] == "path"),
                      "sections": sum(1 for r in MUTATIONS if r[4] ==
                                      "section")}


# ---------------------------------------------------------------------- main

def main(argv: list[str]) -> int:
    global _SUBJECT_PATH
    wants_selftest = "--selftest" in argv[1:]
    positional = [arg for arg in argv[1:] if arg != "--selftest"]
    path = pathlib.Path(positional[0]) if positional else DEFAULT
    _SUBJECT_PATH = path.resolve()
    try:
        original = path.read_text()
        value, _problems = jloads(original, f"subject:{path.name}")
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        print(f"ERROR: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2

    errors = check(value)
    gate = LAST.get("bundle", {}).get("byteGate") or {}
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        if wants_selftest:
            print("SELFTEST-REFUSED: the base contract has findings, so every "
                  "mutation would be masked by them")
            print("SELFTEST-NOT-RUN")
            return 3
        return 1

    if wants_selftest:
        failures, stats = selftest(value, original)
        if failures:
            for failure in failures:
                print(f"SELFTEST-FAIL: {failure}")
            return 1
        print(f"PASS: {path.name}; {stats['total']} successor mutations "
              f"rejected, each by its specific finding id AND naming the "
              f"position under test — {stats['paths']} on the FULL dotted "
              f"path, {stats['sections']} on a section")
        print(f"  {stats['text']} TEXT mutations rejected — duplicate keys at "
              f"four positions including the three the independent reviewer "
              f"planted, a number respelling that moves no value, a non-RFC "
              f"constant, a reindent and a key reorder; none of them changes a "
              f"leaf position and no value-level table can express one")
        print(f"  respelling census by TYPE TRANSITION, not by label text: "
              f"{stats['census']['floatRespellings']} float and "
              f"{stats['census']['booleanRespellings']} boolean respellings")
        print(f"  whole-contract append sweep: "
              f"{stats['whole']['admitted']} of {stats['whole']['total']} "
              f"string positions admit an appended re-worded assurance claim")
        return 0

    published = LAST["published"]
    parts = LAST["partitions"]
    prose = LAST["prose"]
    sweeps = LAST["sweeps"]
    bundle = LAST["bundle"]
    print(f"PASS: {path.name} at sha256 "
          f"{gate.get('subjectSha256', '')[:16]}…; every position outside "
          f"{AUTHOR}, role, knownLimitations and the three successor-identity "
          f"leaves is carried byte-identical from {PREDECESSOR} and gated "
          f"against those bytes")
    print(f"  bytes of record: the file is byte-identical to the serialisation "
          f"of the value this checker reconstructs from its own constants and "
          f"{PREDECESSOR} — {gate.get('equal')}; the parsed contract is "
          f"canonically identical to it — {bundle['reconstructionEqual']}")
    print(f"  parse: {bundle['parseCensus']['inputs']} JSON inputs parsed "
          f"through one hooked primitive — "
          f"{bundle['parseCensus']['duplicateKeys']} duplicate keys, "
          f"{bundle['parseCensus']['nonRfcConstants']} non-RFC constants, "
          f"{bundle['parseCensus']['nonCanonicalNumberTokens']} non-canonical "
          f"number tokens, against an oracle that reports "
          f"{bundle['parseCensus']['oracleProblems']}; "
          f"{bundle['parseScan']['sites']} parse call sites here, "
          f"{bundle['parseScan']['ungatedCount']} ungated and "
          f"{bundle['parseScan']['evasionCount']} decoder evasions, against "
          f"{bundle['parseScan']['predecessorUngated']} ungated in "
          f"{PREDECESSOR_CHECKER}")
    for name, _roots in PARTITION_SCOPES:
        part = parts[name]
        print(f"  partition {name}: {part['total']} leaf positions — "
              f"{part['measured']} MEASURED ({part['fromDisk']} against disk, "
              f"{part['fromConstant']} against a checker constant)")
    print(f"  {len(published)} measurements were compared against a "
          f"declaration before this banner printed any of them; 0 computed "
          f"partitions went uncompared")
    print(f"  coverage census: {LAST['census']['total']} leaf positions in the "
          f"whole contract — {LAST['census']['ungated']} ungated")
    print(f"  prose authority: {prose['stringLeaves']} string leaves — "
          f"{prose['rendered']} RENDERED, {prose['carried']} CARRIED, "
          f"{prose['free']} FREE")
    print(f"  append admission: {sweeps['authoredAdmitted']} of "
          f"{sweeps['authoredPositions']} authored string positions over "
          f"{sweeps['authoredSentences']} wordings, and "
          f"{sweeps['crossAdmitted']} of {sweeps['crossPositions']} × "
          f"{sweeps['crossSentences']} over the re-wording test set; the same "
          f"re-worded claim is admitted at {sweeps['predAdmitted']} of "
          f"{sweeps['predPositions']} positions in {PREDECESSOR}")
    rows = bundle["rehearsalsLive"]
    reach = bundle["reach"]
    print(f"  repoint rehearsal, whole check driven under the substituted "
          f"register: {reach['reachedAtDepthZero']} of {reach['classes']} "
          f"post-guard finding classes reached on this path against "
          f"{reach['reachedAtDepthOne']} on the depth-1 path the predecessor "
          f"used; v23 {rows[0]['findings']} findings / "
          f"{rows[0]['roundsToGreen']} rounds / {rows[0]['leafEdits']} leaf "
          f"edits / exit 0 {rows[0]['reachedExitZero']}; v24 "
          f"{rows[1]['findings']} / {rows[1]['roundsToGreen']} / "
          f"{rows[1]['leafEdits']} / exit 0 {rows[1]['reachedExitZero']}; "
          f"joint fixed point converged {bundle['rehearsalConverged']}")
    print(f"  predecessor attribution: register substituted on "
          f"{bundle['attribution']['modulesSubstituted']} modules of its "
          f"transitive set; under a repoint the transitive arm reports "
          f"{bundle['attributionProbe']['transitiveGenuineDefects']} genuine "
          f"defects and the top-module-only arm reports "
          f"{bundle['attributionProbe']['topModuleOnlyGenuineDefects']}")
    print(f"  registry purity: the reviewer's "
          f"{LAST['purity']['reviewerSuiteAttempted']} constructions are "
          f"caught {LAST['purity']['reviewerSuiteCaughtByThePredecessorAstMeasure']}"
          f" by {PREDECESSOR_CHECKER}'s measure and "
          f"{LAST['purity']['reviewerSuiteCaughtByTheWidenedAstMeasure']} by "
          f"the widened one; a further "
          f"{LAST['purity']['widenedSuiteAttempted']} written against the "
          f"widened measure are caught "
          f"{LAST['purity']['widenedSuiteCaughtByTheWidenedAstMeasure']}")
    print("  scope: checker-scope evidence only; SPECIFIED / "
          "IMPLEMENTABLE_UNEXECUTED; CANDIDATE-NOT-APPLIED; no seal, freeze, "
          "status advance or product acceptance is declared")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
