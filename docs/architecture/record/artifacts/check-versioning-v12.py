#!/usr/bin/env python3
"""Conformance checker for VERSIONING v12 — prose-authority successor.

The v11 CONTRACT closed B-VER10R-01 and the independent reviewer could not
defeat the closure (versioning-policy.v11.review-independent.json: "THE OUTCOME
IS TRUE AND I COULD NOT DEFEAT IT"). The single blocker was that v11 declared a
class closed that its instrument only spelled:

  B-VER11R-01. prosePaperSealScan.rule states "this closes the class in free
  prose". It closes 16 phrases. The reviewer planted four differently-worded
  verdict-inheritance and acceptance claims at seven positions — 28 of 28
  ADMITTED at exit 0 with the full green banner, including into top-level
  `role` — and then ran the checker's own 257-position sweep with those
  wordings: 77 of 257, exactly the neutral sentence's figure. v11's headline
  asymmetry, "the reviewer's own sentence is admitted at 0 of 257", measures the
  pattern table against itself.

This checker does not repair the table. It removes free prose from the artifact.

  1. THE PAPER-SEAL CLASS IS CLOSED ON THE ARTIFACT SIDE BY A PARTITION OVER
     STRING LEAVES, NOT BY A PATTERN TABLE. Every string leaf in this contract is
     classified by HOW IT IS HELD: RENDERED (the whole value is eq-compared
     against a string this checker renders from its own constants and its own
     measurements), CARRIED (byte-identical to the SHA-verified adjudicated
     predecessor), PROTECTED (inside a top-level section canon-compared against
     the predecessor) or FREE. `free` is declared 0 and compared (VER12-PROSE).
     A re-wording cannot evade a rule that never reads the words: appending any
     sentence to any leaf changes the leaf, and every leaf is compared whole.
     That is measured, not argued — append_sweep() appends each sentence of a
     12-sentence re-wording test set, of which the reviewer's four are read from
     the review file rather than retyped, and counts what is admitted. It is 0.

  2. THE CLASS IS NOT ELIMINATED. IT IS RELOCATED TO THIS FILE, AND THAT IS
     PUBLISHED RATHER THAN CLAIMED AWAY. A rendered leaf cannot be authored from
     the artifact side; it can be authored from the instrument side, by editing
     the constant here AND the leaf there. What v12 closes is the one-file edit;
     what remains open is the two-file edit, and R-VER12-01 states the size of
     that surface in this checker's measured numbers. The lexical scan is kept —
     as a LINT with a published evasion rate, never as the closure. Against the
     12-sentence test set the lint catches a measured number and the partition
     catches 12 of 12; both figures are declared and compared.

  3. REGISTRY PURITY IS A NAMING LINT AND IS NOW LABELLED ONE. The reviewer
     showed that registry_purity() counts parameters literally named `value`,
     calls spelled `at(value,` and loops whose bound name came from
     `X = at(value, …)`, and wrote three builders that score 0 on all three. All
     three are checker constants here, compiled and measured on every run by BOTH
     instruments: the carried name-level lint catches 0 of 3, an AST measure that
     counts loops sized from ANY parameter catches 3 of 3. The AST measure does
     not report 0 for the honest builders either, and it is not supposed to:
     registries ARE parameter-sized. What closes the class is the PROVENANCE of
     the sizing parameters — SHA-verified pinned bytes, a checker constant, or an
     equality gate with a pinned fallback — and every AST-measured sizing
     parameter must appear in a declared provenance table whose key set is
     compared against the measured one (VER12-PURITY).

  4. THE UNDECLARED GATE IS DECLARED. v11's evidence_registry docstring says it
     "needs no artifact argument and cannot be sized by its subject". That is
     false and the reviewer proved it: `deps` IS value['decisionDependencies'].
     What held the line was an undeclared equality-gate-plus-fallback. Here the
     gate is a first-class declared guard and its firing is MEASURED on every run
     (deps_gate_probe): a decisionDependencies entry is appended, VER12-DEP must
     fire, and the registry position count must not grow.

  5. THE REGISTER REHEARSAL IS LIVE AND COVERS v24. The coordinator has advanced
     retention-tiers to v24 in both prose documents while the register still
     binds v22. rehearse_live() substitutes the register in-process, runs this
     whole checker, applies exactly what each finding names, iterates to a fixed
     point and reports findings, rounds, leaf edits, checker edits, index shifts
     and findingsNotSelfRepairing — for v23 AND for v24. The declared repair cost
     covers both.

  6. THE PREDECESSOR'S REDNESS IS ATTRIBUTED BY MEASUREMENT, NOT BY A SUBSTRING.
     v11 tolerated a red predecessor when `'registerBinding' in finding`, which
     review O-05 recorded as a text test standing in for a path test. Here the
     pinned predecessor is run twice — once against the live register and once
     against the register state its own record names — and only findings present
     in BOTH are genuine defects (VER12-PRED).

Everything outside successorRevision.proseAuthorityRepair, `role`,
knownLimitations and the three successor-identity leaves is carried from
versioning-policy.v11.json BYTE-IDENTICAL and gated leaf-wise against those
bytes; coverage_census() partitions every leaf position in the whole artifact
and declares the ungated count, which is 0.

Trust order: inert bytes -> SHA-256 verify -> execute from the verified snapshot.
A non-zero exit is not evidence a guard fired, so every finding carries a stable
VER12-* id and names the position under test, and --selftest asserts on BOTH,
on the FULL dotted path wherever the finding names a leaf.

Usage: python3 -I -B artifacts/check-versioning-v12.py [contract] [--selftest]
Exit:  0 clean · 1 findings · 2 IO error · 3 selftest refused or not run
"""
from __future__ import annotations

import ast
import copy
import hashlib
import importlib.util
import inspect
import json
import pathlib
import re
import subprocess
import sys
import textwrap
from typing import Any

HERE = pathlib.Path(__file__).resolve().parent
DEFAULT = HERE / "versioning-policy.v12.json"

PREDECESSOR = "versioning-policy.v11.json"
PREDECESSOR_CHECKER = "check-versioning-v11.py"
PREDECESSOR_REVIEW = "versioning-policy.v11.review-independent.json"
GRANDPARENT = "versioning-policy.v10.json"
GRANDPARENT_CHECKER = "check-versioning-v10.py"
GRANDPARENT_REVIEW = "versioning-policy.v10.review-independent.json"
ELDER = "versioning-policy.v9.json"
ELDER_CHECKER = "check-versioning-v9.py"
GREAT_ELDER = "versioning-policy.v8.json"
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
        "5e0d31de253fe1f02e7e2a51dcd438b0f0bb695286582eb0473afa1d8b528702",
    PREDECESSOR_CHECKER:
        "662781afc8ba4bb80f0e1939b79d4113066ca81a1874e9fea9a30cfb23d90347",
    PREDECESSOR_REVIEW:
        "5db9bb24b1d7c3985050af2ad564b721fbf672fbdc1445c64f88686dc4901d8c",
    GRANDPARENT:
        "194350399d4bd5861ac826eb8d7e0ce835f58cff1e049910552b85a71d002ed0",
    GRANDPARENT_CHECKER:
        "40e85b42648276e0bdb09524663248eff09885c39e53e3971a7f337a51f88612",
    GRANDPARENT_REVIEW:
        "d264dbdd83579d41f8bf8a5a1ac355aad33070991b818148bbcaf991cd2d8e3d",
    ELDER:
        "9d3f936ae492e2b692781215f92de4b50ef9b962911e9067c7d052825e0492a9",
    ELDER_CHECKER:
        "cf88da34a68a2697d5040d97d32eeaabcf7217162bf279ab5b546c066210bd80",
    GREAT_ELDER:
        "ea4b52b5a4d187ec35ad994d8ffcd888db287566c8fb53f3df17e5203d84ae2e",
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
# through v11 and again here: a CONTINUING INVARIANT gets a semantic gate,
# because a byte pin fails on the very repoint it anticipates; a RECORDED
# MEASUREMENT gets hard comparison, because an uncompared measurement is prose
# that looks like evidence.

CHANGED = {"version", "supersedes", "role", "knownLimitations",
           "successorRevision"}

REPAIR = "successorRevision.d9CitationRepair"
ENFORCE = "successorRevision.evidenceEnforcementRepair"
CLOSE = "successorRevision.enforcementClosureRepair"
AUTHOR = "successorRevision.proseAuthorityRepair"

EXPECTED_REVISION_KEYS = {
    "id", "candidateState", "supersedesCandidate", "inputs",
    "rawAuthorityKinds", "custodyRule", "storeAuthorityRule",
    "identityStability", "forbiddenBackEdge", "coldStoredReadRejoin",
    "dependencyLabelRule", "d9CitationRepair", "evidenceEnforcementRepair",
    "enforcementClosureRepair", "proseAuthorityRepair",
}

# Every successorRevision key carried byte-identical from the pinned
# predecessor. `id`, `supersedesCandidate` and `identityStability` necessarily
# move in a successor and are RENDERED instead; `proseAuthorityRepair` is this
# successor's new work.
FROZEN_REVISION_KEYS = (
    "candidateState", "inputs", "rawAuthorityKinds", "custodyRule",
    "storeAuthorityRule", "forbiddenBackEdge", "coldStoredReadRejoin",
    "dependencyLabelRule", "d9CitationRepair", "evidenceEnforcementRepair",
    "enforcementClosureRepair",
)
# The remainder: everything frozen that is not one of the three big blocks,
# gated per-leaf here rather than only as a canonical-JSON section.
FROZEN_REMAINDER = tuple(
    f"successorRevision.{k}" for k in FROZEN_REVISION_KEYS
    if k not in ("d9CitationRepair", "evidenceEnforcementRepair",
                 "enforcementClosureRepair"))

AUTHORED_ROOTS = (
    "version", "supersedes", "role", "knownLimitations",
    "successorRevision.id", "successorRevision.identityStability",
    "successorRevision.supersedesCandidate", AUTHOR,
)

# The protected top-level sections, gated PER LEAF rather than only as canonical
# JSON. The predecessor compared these as whole sections, which rejects an
# appended sentence but names the SECTION rather than the position — the same
# collateral-rejection weakness review O-04 recorded one level down. Naming them
# here is a checker constant: if the artifact's top-level key set moves at all,
# VER12-SURFACE fires before any of this is reached.
PROTECTED_ROOTS = (
    "adjudicationRevision", "agentProtocolNote", "artifact", "author",
    "comparisonFixtures", "comparisonSchema", "conformanceTests",
    "custodyClasses", "decisionDependencies", "detectorSemanticDelta",
    "dischargeStatus", "historicalSemanticsPolicy", "implementationBacklog",
    "migrators", "peerReviewRequired", "principle", "purpose", "resolves",
    "reviewStatus", "rules", "status", "supportWindows", "versionedIdentities",
)

# The one authority for what is partitioned.
PARTITION_SCOPES = (
    ("carriedD9CitationRepair", (REPAIR,)),
    ("carriedEnforcementBlock", (ENFORCE,)),
    ("carriedClosureBlock", (CLOSE,)),
    ("carriedRevisionRemainder", FROZEN_REMAINDER),
    ("protectedSurface", PROTECTED_ROOTS),
    ("authoredSurface", AUTHORED_ROOTS),
)

EXPECTED_AUTHOR_KEYS = (
    "findingId", "authoredBy", "reviewOfRecord", "defect",
    "whySuccessorAndNotInPlaceRepair", "proseAuthorityPartition",
    "appendAdmissionSweep", "rewordingTestSet", "lexicalSealLint",
    "registryPurity", "evidenceRegistryCorrection", "coverageCensus",
    "partitionClosure", "carriedByteIdentical", "registerAsOfAudit",
    "repointRehearsals", "predecessorDisposition", "demonstrations",
    "closedScalarAdmission", "selftestProfile", "residualRestatements",
    "recordedInputs", "recordedInputsRule", "retainedResiduals",
    "checkerDisposition", "notClaimed",
)

CARRIED_RESIDUAL_IDS = tuple(f"R-VER11-{n:02d}" for n in range(1, 12))

REQUIRED_RESIDUAL_IDS = (
    "R-VER12-01", "R-VER12-02", "R-VER12-03", "R-VER12-04", "R-VER12-05",
    "R-VER12-06", "R-VER12-07", "R-VER12-08", "R-VER12-09", "R-VER12-10",
)
RESTATED_RESIDUALS = ("R-VER11-01", "R-VER11-08")

OWNER_VOCABULARY = {
    "coordinator", "independent reviewer", "phase1a successor lane",
    "phase1a evidence-enforcement lane", "phase1a enforcement-closure lane",
    "phase1a prose-authority lane",
}

REPAIRED_CITATION = "artifacts/" + D9_HEAD

MEASURED = "MEASURED"
FROM_DISK = "disk"
FROM_CONSTANT = "constant"

# The prose-authority classes. `free` is the finding class and is declared 0.
RENDERED = "RENDERED"
CARRIED = "CARRIED"
FREE = "FREE"

REGISTRY_BUILDERS = ("carried_registry", "asof_registry", "authored_registry")
PREDECESSOR_REGISTRY_BUILDERS = ("evidence_registry", "frozen_registry",
                                 "closure_registry")

# The as-of rule, stated structurally rather than as a list of positions: any
# carried leaf whose path ends in one of these is a RECORDED MEASUREMENT of a
# file that moves, so it is compared against the LIVE register instead of
# against the carried byte. The count of such positions is declared and compared.
AS_OF_SUFFIXES = (".registerBinding", ".candidateBindingsInFamily")

SENTINEL_RT = "artifacts/retention-tiers.v9001.json"
SENTINEL_EP = "artifacts/evaluation-proof.v9001.json"
# The coordinator has advanced retention-tiers to v24 in both prose documents
# while the register still binds v22. Both live targets are rehearsed.
LIVE_REPOINT_TARGETS = ("artifacts/retention-tiers.v23.json",
                        "artifacts/retention-tiers.v24.json")
DEMONSTRATIONS = 6            # the plan in probe_pairs(), a checker constant
DOCUMENTED_RT_HEAD = "artifacts/retention-tiers.v24.json"

# ---- the re-wording test set -------------------------------------------------
# The reviewer's four wordings are READ FROM THE REVIEW FILE, not retyped, so
# this checker cannot quietly test something easier than what defeated v11.
# Six more are authored here to probe evasion strategies the reviewer's four do
# not: a sentence with no assurance vocabulary at all, a nominalised one, a
# purely numeric one, an indirect one, a quotation-shaped one and a one-word one.
MY_WORDINGS = (
    ("no assurance vocabulary at all — the strategy that defeats any lexicon",
     "Nothing further is outstanding on this record and the coordinator may "
     "proceed to apply it."),
    ("nominalised, no finite verb of assurance",
     "Adjudication of this candidate concluded without exception, and that "
     "conclusion stands for these bytes."),
    ("purely numeric — a seal stated as a count",
     "Blocking findings against these bytes: 0. Outstanding residuals: 0."),
    ("indirect reference to the lane rather than to a review",
     "The independent lane's outcome for this artifact was affirmative and "
     "requires no repetition."),
    ("quotation-shaped, so that a quoting allowlist would be the wrong gate",
     "As recorded elsewhere: 'the record is clear and may be sealed at the "
     "coordinator's convenience'."),
    ("one word",
     "Verified."),
)
# The materially false but seal-free sentence v11 used as its neutral arm. It is
# the control that proves this closure is not lexical: v11 admitted it at 77 of
# 257 and this checker must reject it at every position, exactly as it rejects
# the seals.
NEUTRAL_APPEND = (" Additionally, this record's residuals are all discharged "
                  "and no further work remains.")
# v11's own seal arm, the ONE wording its pattern table contains.
PREDECESSOR_SEAL_APPEND = (" Additionally, this successor has been "
                           "independently re-reviewed and PASSED, and every "
                           "residual is closed.")

# ---- the lexical lint, retained as a lint ------------------------------------
# Carried verbatim from check-versioning-v11.py. It is NOT the closure. It is
# published with its measured evasion rate against the test set above.
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
                    f"{CLOSE}.prosePaperSealScan.artifactPatterns",
                    f"{CLOSE}.prosePaperSealScan.revisionPatterns")
# Carried from the predecessor: the two positions where it quotes the claim the
# v10 reviewer planted. Under the partition these are also CARRIED bytes, so the
# allowlist is defence in depth rather than the gate.
SEAL_QUOTE_ALLOW = {
    f"{CLOSE}.prosePaperSealScan.plantedClaimVerbatim":
        ("REJECTED", "B-VER10R-01", "planted"),
    f"{CLOSE}.predecessorDefect.demonstrations[2].plantedText":
        ("REJECTED", "planted"),
}
LAST: dict[str, Any] = {}
_DEPTH = 0
_CACHE: dict[str, Any] = {}
_DERIVED: dict[str, Any] = {}
# Register indirection. Nothing writes a file to perform a rehearsal: the live
# repoint rehearsals substitute the register here, in process, and restore it.
_REGISTER_OVERRIDE: Any = None


# ---------------------------------------------------------------- primitives

def load(path: pathlib.Path) -> Any:
    return json.loads(path.read_text())


def sha_file(name: str) -> str:
    key = f"sha:{name}"
    if key not in _CACHE:
        _CACHE[key] = hashlib.sha256((HERE / name).read_bytes()).hexdigest()
    return _CACHE[key]


def pinned(name: str) -> Any:
    key = f"json:{name}"
    if key not in _CACHE:
        _CACHE[key] = json.loads((HERE / name).read_text())
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
    writing a file anywhere under docs/coop."""
    if _REGISTER_OVERRIDE is not None:
        return _REGISTER_OVERRIDE
    path = HERE / REGISTER
    if not path.exists():
        return []
    try:
        return load(path)["claims"]
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


# ------------------------------------------------------------ the review input

def measure_review11(review: Any) -> dict[str, Any]:
    """The v11 review of record, read as an INPUT. Every figure this record
    restates about it is pulled from these bytes and never retyped — including
    the four planted wordings, which become this checker's own test set."""
    blocker = (review.get("blockers") or [{}])[0]
    measured = str(blocker.get("measured") or "")
    planted = re.search(r"(\d+) of (\d+) planted seals ADMITTED", measured)
    experiment = blocker.get("theDecisiveExperiment") or {}
    results = experiment.get("results") or {}

    def figure(key_fragment: str) -> Any:
        for key, text in results.items():
            if key_fragment in key:
                hit = re.match(r"(\d+) of (\d+)", str(text))
                if hit:
                    return int(hit.group(1)), int(hit.group(2))
        return None, None

    neutral, swept = figure("NEUTRAL_APPEND")
    sealed, _ = figure("SEAL_APPEND")
    reworded, _ = figure("re-worded seal A")
    wordings: list[str] = []
    for row in blocker.get("theFourWordings") or []:
        hit = re.match(r"^[A-Z]:\s*'(.*)'\s*$", str(row), re.S)
        wordings.append(hit.group(1) if hit else str(row))
    return {
        "verdict": review.get("verdict"),
        "blockingFindingCount": review.get("blockingFindingCount"),
        "nonBlockingObservationCount": review.get("nonBlockingObservationCount"),
        "blockerId": blocker.get("id"),
        "plantedAdmitted": int(planted.group(1)) if planted else None,
        "plantedAttempted": int(planted.group(2)) if planted else None,
        "plantedPositions": len(blocker.get("theSevenPositions") or []),
        "wordings": wordings,
        "sweptPositions": swept,
        "neutralAdmitted": neutral,
        "predecessorSealAdmitted": sealed,
        "rewordedAdmitted": reworded,
    }


def test_sentences(review: dict[str, Any]) -> list[dict[str, str]]:
    """The re-wording test set: the reviewer's four, read from the review file,
    plus six authored here. A checker that retyped the reviewer's sentences
    could quietly test something easier than what defeated its predecessor."""
    rows: list[dict[str, str]] = []
    for index, text in enumerate(review["wordings"]):
        rows.append({
            "provenance": f"read from {PREDECESSOR_REVIEW} "
                          f"blockers[0].theFourWordings[{index}]",
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


def ast_structural_source(source: str) -> dict[str, Any]:
    """The same measure over a source STRING, so the compiled evasion
    constructions — which inspect.getsource() cannot read — are measured by
    exactly the same walk as the real builders."""
    tree = ast.parse(textwrap.dedent(source))
    fndef = tree.body[0]
    if not isinstance(fndef, (ast.FunctionDef, ast.AsyncFunctionDef)):
        return {"parameterSizedLoops": 0, "loopCount": 0,
                "sizingParameters": []}

    params: list[str] = [a.arg for a in fndef.args.posonlyargs]
    params += [a.arg for a in fndef.args.args]
    params += [a.arg for a in fndef.args.kwonlyargs]
    if fndef.args.vararg:
        params.append(fndef.args.vararg.arg)
    if fndef.args.kwarg:
        params.append(fndef.args.kwarg.arg)
    tainted: set[str] = set(params)
    origin: dict[str, set[str]] = {p: {p} for p in params}

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

    # Taint starts at the parameter list and propagates through assignment,
    # through iteration and through OUT-PARAMETERS: a call that receives a
    # tainted argument taints every other name it receives, which is how
    # `leaf_items(pinned, root, items)` makes `items` pinned-sized. That
    # direction over-taints, which is the safe direction for this measure.
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
                src = set()
                for arg in args:
                    src |= sources_of(arg)
                if src:
                    for arg in args:
                        if isinstance(arg, ast.Name):
                            changed |= taint(arg.id, src)

    loops = 0
    total = 0
    sizing: set[str] = set()
    for node in ast.walk(fndef):
        if isinstance(node, (ast.For, ast.AsyncFor, ast.comprehension)):
            total += 1
            src = sources_of(node.iter)
            if src:
                loops += 1
                sizing |= src
    return {"parameterSizedLoops": loops, "loopCount": total,
            "sizingParameters": sorted(sizing)}


# The reviewer's three constructions, held as source so BOTH instruments measure
# the same bytes on every run. They are the test set for the purity claim, the
# way the twelve sentences are the test set for the prose claim.
EVASION_SOURCE = (
    ("a builder that takes the artifact under a name that is not `value`",
     "def evil_registry(artifact, pinned):\n"
     "    rows = artifact['knownLimitations']\n"
     "    reg = {}\n"
     "    for i, _r in enumerate(rows):\n"
     "        reg['knownLimitations[%d]' % i] = None\n"
     "    return reg\n"),
    ("a builder that reads the artifact by subscript instead of by at()",
     "def evil_subscript(value):\n"
     "    rows = value['knownLimitations']\n"
     "    reg = {}\n"
     "    for i, _r in enumerate(rows):\n"
     "        reg['k[%d]' % i] = None\n"
     "    return reg\n"),
    ("a genuine artifact-sized loop with no intermediate binding",
     "def evil_inline(value):\n"
     "    reg = {}\n"
     "    for i in range(len(at(value, 'knownLimitations'))):\n"
     "        reg['k[%d]' % i] = None\n"
     "    return reg\n"),
)


def name_level_lint_source(source: str) -> dict[str, int]:
    """The name-level lint applied to a source STRING, for the compiled evasions
    (inspect.getsource cannot read a function built from a string)."""
    params = len(re.findall(r"\bdef \w+\([^)]*\bvalue\b", source))
    reads = len(re.findall(r"\b(?:at|resolves_in)\(\s*value\s*,", source))
    bound = re.findall(r"(\w+)\s*=\s*at\(\s*value\s*,", source)
    loops = sum(1 for name in bound
                if re.search(rf"for .*\b{re.escape(name)}\b", source))
    return {"artifactParameters": params, "artifactReads": reads,
            "artifactSizedLoops": loops}


# Where every loop-sizing parameter of every builder in THIS checker gets its
# size. The KEY SET is compared against the AST-measured set on every run, so a
# future editor who adds a parameter that sizes a loop must declare where its
# size comes from or the check fails naming the pair. This is what replaces the
# predecessor's "it is not possible to write an artifact-sized loop": the loops
# exist, and what is closed is their provenance.
PROVENANCE = {
    ("carried_registry", "pinned"):
        "SHA-verified pinned bytes. PINS is verified unconditionally at the top "
        "of _check(), not gated by verify_files, so a drifted predecessor "
        "returns VER12-PIN rather than a resized registry.",
    ("carried_registry", "root"):
        "a checker constant — one of the roots of PARTITION_SCOPES.",
    ("asof_registry", "audit"):
        "measure_audit() over deps, which the equality gate in _check() forces "
        "equal to the pinned predecessor's decisionDependencies before any "
        "registry is built; the gate's firing is measured every run by "
        "deps_gate_probe().",
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
    predecessor's, and of the three evasion constructions. Source does not move
    inside a process, so it is measured once and reused; nothing here reads the
    subject."""
    if "purity" in _CACHE:
        return _CACHE["purity"]
    mine: dict[str, Any] = {}
    for name in REGISTRY_BUILDERS:
        fn = globals()[name]
        mine[name] = {"lint": name_level_lint(fn), "ast": ast_structural(fn)}
    theirs: dict[str, Any] = {}
    for name in PREDECESSOR_REGISTRY_BUILDERS:
        fn = getattr(pred_module, name)
        theirs[name] = {"lint": name_level_lint(fn), "ast": ast_structural(fn)}
    evasions = []
    for note, source in EVASION_SOURCE:
        lint = name_level_lint_source(source)
        struct = ast_structural_source(source)
        evasions.append({
            "construction": note,
            "nameLevelLintArtifactSizedLoops": lint["artifactSizedLoops"],
            "astStructuralParameterSizedLoops": struct["parameterSizedLoops"],
            "caughtByTheNameLevelLint": lint["artifactSizedLoops"] > 0,
            "caughtByTheAstMeasure": struct["parameterSizedLoops"] > 0,
        })
    declared = sorted(PROVENANCE)
    measured = sorted({(name, p) for name in REGISTRY_BUILDERS
                       for p in mine[name]["ast"]["sizingParameters"]})
    _CACHE["purity"] = {
        "mine": mine, "theirs": theirs, "evasions": evasions,
        "myNameLevelArtifactSizedLoops":
            sum(mine[n]["lint"]["artifactSizedLoops"] for n in mine),
        "myAstParameterSizedLoops":
            sum(mine[n]["ast"]["parameterSizedLoops"] for n in mine),
        "predecessorNameLevelArtifactSizedLoops":
            sum(theirs[n]["lint"]["artifactSizedLoops"] for n in theirs),
        "predecessorAstParameterSizedLoops":
            sum(theirs[n]["ast"]["parameterSizedLoops"] for n in theirs),
        "evasionsCaughtByTheNameLevelLint":
            sum(1 for e in evasions if e["caughtByTheNameLevelLint"]),
        "evasionsCaughtByTheAstMeasure":
            sum(1 for e in evasions if e["caughtByTheAstMeasure"]),
        "evasionsAttempted": len(evasions),
        "declaredProvenanceEntries": len(declared),
        "measuredSizingParameters": len(measured),
        "sizingParametersWithoutDeclaredProvenance":
            sorted(set(measured) - set(declared)),
        "declaredProvenanceWithoutAMeasuredParameter":
            sorted(set(declared) - set(measured)),
    }
    return _CACHE["purity"]


def predecessor_evidence_registry_defect(pred_module: Any) -> dict[str, Any]:
    """O-02, measured rather than restated. The predecessor's evidence_registry
    docstring claims it 'needs no artifact argument and cannot be sized by its
    subject'. Both halves are checked here: the sentence is located in the pinned
    source, and the call site is shown to pass an artifact-derived argument."""
    if "evidenceDefect" in _CACHE:
        return _CACHE["evidenceDefect"]
    fn = getattr(pred_module, "evidence_registry")
    doc = inspect.getdoc(fn) or ""
    claim = "needs no artifact argument and cannot be sized by its subject"
    check_source = inspect.getsource(pred_module._check)
    binds = bool(re.search(r"deps\s*=\s*value\.get\(\s*[\"']"
                           r"decisionDependencies[\"']\s*\)", check_source))
    passes = bool(re.search(r"evidence_registry\(\s*deps\s*,", check_source))
    fallback = bool(re.search(r"deps\s*=\s*list\(\s*pred_deps\s*\)",
                              check_source))
    struct = ast_structural(fn)
    _CACHE["evidenceDefect"] = {
        "docstringContainsTheClaim": claim in " ".join(doc.split()),
        "theClaim": claim,
        "depsIsBoundFromTheArtifact": binds,
        "depsIsPassedToTheBuilder": passes,
        "astParameterSizedLoopsInThatBuilder": struct["parameterSizedLoops"],
        "sizingParameters": struct["sizingParameters"],
        "equalityGateWithPinnedFallbackExists": fallback,
    }
    return _CACHE["evidenceDefect"]


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
        for pattern in SEAL_PATTERNS_ARTIFACT:
            if re.search(pattern, text, re.I):
                hits.append((path, pattern))
    for path, text in revision:
        if path.startswith(SEAL_SCAN_EXEMPT):
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
    never reads the words. This is the repair of B-VER11R-01: the predecessor
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


def in_a_scope(path: str) -> bool:
    return any(path == root or path.startswith(root + ".") or
               path.startswith(root + "[") for root in SCOPE_ROOTS)


def predecessor_census_correction(pred_module: Any,
                                  pred_artifact: Any) -> dict[str, Any]:
    """Review O-03, published as numbers rather than as a principle. The
    predecessor's census is computed HERE BY ITS OWN INSTRUMENT — its
    coverage_census() over its own bytes — and the one figure it did not publish
    is added: how many leaves it counted under `scope` are ALSO byte-carried.
    Its declared byte-carry figure understates its real byte-carried surface by
    exactly that number, in the safe direction."""
    if "predCensus" in _CACHE:
        return _CACHE["predCensus"]
    census = pred_module.coverage_census(pred_artifact, pinned(GRANDPARENT))
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
        "declaredByteCarry": census["carry"],
        "doubleGated": both,
        "byteCarriedIncludingDoubleGated": census["carry"] + both,
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
    inside it has no classification (VER12-COVER) and a row deleted from it
    leaves a classification with nothing to compare (VER12-COVER)."""
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
    if canon(declared) == canon(payload):
        return None
    if type(declared) is not type(payload) and (
            isinstance(declared, (int, float, bool)) or
            isinstance(payload, (int, float, bool))):
        return (f"VER12-LEAFTYPE: {path} declares {declared!r} "
                f"({type(declared).__name__}); this checker measured "
                f"{payload!r} ({type(payload).__name__}). freeze §6 law 18: "
                f"closed-scalar admission is exact-type in BOTH directions")
    # Both messages END with the measured value, so a repair can be followed by
    # taking everything after the last "; this checker measured ". That is not a
    # stylistic choice: rehearse_live() repairs a record by reading exactly
    # these strings and counts every one it cannot follow.
    if path.endswith(AS_OF_SUFFIXES):
        return (f"VER12-ASOF: {path} is a RECORDED MEASUREMENT of the live "
                f"{REGISTER}, so a stale value here is a TRUE POSITIVE about "
                f"these bytes, not a false alarm about the register "
                f"(R-VER12-05). Repair in place: restate this leaf and "
                f"re-measure "
                f"{AUTHOR}.carriedByteIdentical.carriedDelta.count/.digest — a "
                f"count and a digest, so there is no index to shift. It "
                f"declares {show(declared)}; this checker measured "
                f"{show(payload)}")
    return (f"VER12-LEAF: {path} declares {show(declared)}; this checker "
            f"measured {show(payload)}")


def evaluate(value: Any, reg: dict[str, Any],
             scope: tuple[str, ...]) -> tuple[list[str], dict[str, Any]]:
    errors: list[str] = []
    items: list[tuple[str, Any]] = []
    for root in scope:
        if resolves_in(value, root):
            leaf_items(at(value, root), root, items)
        else:
            add(errors, "VER12-COVER",
                f"declared scope root {root} is absent")
    found = [path for path, _v in items]
    graded = 0
    origin = {FROM_DISK: 0, FROM_CONSTANT: 0}
    for path, declared in items:
        entry = reg.get(path)
        if entry is None:
            add(errors, "VER12-COVER",
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
            add(errors, "VER12-COVER",
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
    grows. In this checker the as-of registry is additionally sized by the
    CARRIED position set rather than by deps, so the growth figure is 0 for two
    independent reasons and both are recorded."""
    candidate = copy.deepcopy(value)
    deps = candidate.get("decisionDependencies")
    if not isinstance(deps, list):
        return {"gateFires": False, "positionsBefore": 0, "positionsAfter": 0,
                "findingIds": ""}
    inner(copy.deepcopy(value))
    before = len(LAST.get("asofPositions") or [])
    deps.append({"id": "ADVERSARIAL-PROBE",
                 "source": "artifacts/nothing.v1.json",
                 "claim": "a probe entry appended to size a registry",
                 "direction": "none", "note": "probe"})
    errors = inner(candidate)
    after = len(LAST.get("asofPositions") or [])
    return {
        "gateFires": any(e.startswith("VER12-DEP:") for e in errors),
        "positionsBefore": before,
        "positionsAfter": after,
        "registryGrew": after > before,
        "findingIds": ",".join(sorted({e.split(":")[0] for e in errors})),
    }


# ------------------------------------------------- predecessor attribution

def recorded_register_state(pred_artifact: Any,
                            live: list[Any]) -> list[Any]:
    """The register state the PINNED PREDECESSOR'S OWN RECORD names, rebuilt from
    its declared registerAsOfAudit. Used to run the predecessor twice and
    attribute its redness by measurement instead of by a substring over the
    finding text (review O-05)."""
    entries = []
    path = f"{CLOSE}.registerAsOfAudit.entries"
    if resolves_in(pred_artifact, path):
        entries = at(pred_artifact, path)
    recorded: dict[str, Any] = {}
    for row in entries if isinstance(entries, list) else []:
        if isinstance(row, dict) and row.get("registerBinding"):
            recorded[family_of(row["registerBinding"])] = row["registerBinding"]
    out = copy.deepcopy(live)
    for claim in out:
        binding = claim.get("bindingArtifact") if isinstance(claim, dict) \
            else None
        if isinstance(binding, str):
            was = recorded.get(family_of(binding))
            if was:
                claim["bindingArtifact"] = was
    return out


def predecessor_attribution(pred_module: Any, pred_artifact: Any,
                            live: list[Any]) -> dict[str, Any]:
    """Run the pinned predecessor pair twice: once against the register as it is,
    once against the register state its own record names. A finding present in
    BOTH is a genuine defect; a finding present only in the first is coupled to
    a coordinator act on a binding the predecessor recorded. v11 made this
    judgement with `'registerBinding' in finding` — a text test standing in for a
    path test, which review O-05 recorded and which this measures instead."""
    try:
        live_findings = pred_module.inner(copy.deepcopy(pred_artifact))
    except Exception as exc:
        live_findings = [f"{type(exc).__name__}: {exc}"]
    substituted = recorded_register_state(pred_artifact, live)
    original = pred_module.load
    try:
        def patched(path: Any) -> Any:
            if pathlib.Path(str(path)).name == REGISTER:
                return {"claims": substituted}
            return original(path)
        pred_module.load = patched
        try:
            as_recorded = pred_module.inner(copy.deepcopy(pred_artifact))
        except Exception as exc:
            as_recorded = [f"{type(exc).__name__}: {exc}"]
    finally:
        pred_module.load = original
    genuine = [f for f in live_findings if f in set(as_recorded)]
    return {
        "findingsAgainstItsOwnBytes": len(live_findings),
        "findingsUnderTheRegisterStateItRecorded": len(as_recorded),
        "findingsAttributableToACoordinatorRepoint":
            len(live_findings) - len(genuine),
        "genuineDefects": len(genuine),
        "genuineDefectTexts": genuine,
        "method": "the pinned predecessor pair is executed twice — against the "
                  "live register and against the register state its own "
                  "registerAsOfAudit names — and only a finding present in BOTH "
                  "is a genuine defect",
    }


# ----------------------------------------------------------- the rehearsals

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
    r"^VER12-(?:ASOF|LEAF): (\S+) .*; this checker measured (.*)$")


def rehearse_live(value: Any, target: str) -> dict[str, Any]:
    """THE ARMED EVENT, REHEARSED LIVE AND IN PROCESS. Substitute the register,
    run this whole checker, apply EXACTLY what each finding names — nothing else
    — and iterate to a fixed point. What is reported is the true repair cost:
    findings on the first round, rounds to green, leaf edits, checker edits
    (0 by construction: this function never writes a file and never touches this
    checker), index shifts, and the number of findings whose printed repair
    instruction was NOT machine-followable, which must be 0 for the claim
    'the repair path is self-documenting' to mean anything."""
    global _REGISTER_OVERRIDE
    claims = copy.deepcopy(register_claims())
    for claim in claims:
        if isinstance(claim, dict) and claim.get("id") == "ARCH.RETENTION-TIERS":
            claim["bindingArtifact"] = target
    saved = _REGISTER_OVERRIDE
    candidate = copy.deepcopy(value)
    first_findings = 0
    first_ids = ""
    edits: list[str] = []
    unfollowable = 0
    rounds = 0
    green = False
    try:
        _REGISTER_OVERRIDE = claims
        while rounds < 8:
            errors = inner(candidate)
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
                    replacement = json.loads(now)
                except ValueError:
                    continue
                set_at(candidate, path, replacement)
                edits.append(path)
                progressed = True
            if not progressed:
                break
        # What could NOT be followed is measured at the FIXED POINT, not on the
        # way to it: a finding that a later round repairs was followable, it
        # simply had a prerequisite. If the loop reaches exit 0 this is 0 by
        # construction and the construction is the measurement.
        unfollowable = 0 if green else len(inner(candidate))
    finally:
        _REGISTER_OVERRIDE = saved
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
    }


# --------------------------------------------------------------- the probes

def probe_pairs(pred_module: Any, pred_artifact: Any, subject: Any,
                sentences: list[dict[str, str]]) -> list[dict[str, Any]]:
    """The demonstrations, executed on every run against BOTH the pinned
    predecessor pair and these bytes. Five plant a re-worded assurance claim at a
    position the predecessor admits; the sixth appends the predecessor's OWN
    seal wording, which its pattern table does catch — the control that shows the
    predecessor's asymmetry was lexical, not semantic."""
    last = len(subject.get("knownLimitations") or []) - 1
    pred_last = len(pred_artifact.get("knownLimitations") or []) - 1
    plan = [
        ("plant a re-worded verdict-inheritance claim in top-level role",
         "role", "role", sentences[0]["sentence"]),
        ("plant a re-worded acceptance claim in the last knownLimitation",
         f"knownLimitations[{pred_last}]", f"knownLimitations[{last}]",
         sentences[2]["sentence"]),
        ("plant a re-worded discharge claim in a retained residual",
         f"{CLOSE}.retainedResiduals[0].residual",
         f"{AUTHOR}.retainedResiduals[0].residual", sentences[3]["sentence"]),
        ("plant a re-worded claim in the successor identity-stability reason",
         "successorRevision.identityStability.reason",
         "successorRevision.identityStability.reason",
         sentences[4]["sentence"]),
        ("append a materially false sentence carrying NO assurance vocabulary",
         f"{CLOSE}.notClaimed[0]", f"{AUTHOR}.notClaimed[0]",
         NEUTRAL_APPEND.strip()),
        ("CONTROL — append the predecessor's own seal wording, the one its "
         "pattern table contains",
         f"{CLOSE}.notClaimed[0]", f"{AUTHOR}.notClaimed[0]",
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


# ----------------------------------------------------- the rendered content

def probe_positions(value: Any) -> list[str]:
    """One string position from each prose-authority class and each authored
    sub-block, so the twelve-sentence cross product is measured ACROSS the
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
        f"{AUTHOR}.proseAuthorityPartition.rule",
        f"{AUTHOR}.checkerDisposition.scopeOfThatBoolean",
        f"{CLOSE}.notClaimed[0]",
        f"{CLOSE}.prosePaperSealScan.rule",
        f"{REPAIR}.siblingCitationAudit.method",
        "purpose",
    ]


ADDED_LIMITATION_COUNT = 5

V12_REQUIRED_INPUTS = (
    (PREDECESSOR,
     "protected predecessor; every position outside "
     "successorRevision.proseAuthorityRepair, role, knownLimitations and the "
     "three successor-identity leaves is carried from these bytes and gated "
     "against them leaf-wise"),
    (PREDECESSOR_CHECKER,
     "predecessor checker; the subject of blocker B-VER11R-01, executed by this "
     "checker on every run to reproduce the admissions and to measure the "
     "evasion rate of its pattern table and of its registry_purity()"),
    (PREDECESSOR_REVIEW,
     "the independent verdict that binds the v11 bytes; the four planted "
     "wordings this checker uses as its own test set are READ FROM THIS FILE "
     "rather than retyped, and every figure restated about the review is read "
     "here too"),
    (GRANDPARENT,
     "the v10 bytes the carried enforcement record is measured against"),
    (GRANDPARENT_CHECKER,
     "the v10 checker whose four admissions B-VER10R-01 measured; executed "
     "transitively by the predecessor checker on every run"),
    (GRANDPARENT_REVIEW,
     "the v10 independent verdict, whose B-VER10R-01 the predecessor closed"),
    (ELDER,
     "the v9 bytes the carried d9 citation repair record is measured against"),
    (ELDER_CHECKER,
     "the v9 checker; retained as historical evidence of what was enforced when "
     "v9 was reviewed, not repaired"),
    (GREAT_ELDER,
     "the v8 bytes B-SCV2-06's recorded resolution must survive unchanged "
     "through every successor in this chain"),
    (D9_SUPERSEDED,
     "superseded citation endpoint of the span the carried record measures"),
    (D9_HEAD,
     "repaired citation target and the live register's D9 binding"),
    (D9_HEAD_CHECKER,
     "executed on every run; the D9 head dependency must be green for this "
     "record to be green"),
    (V4,
     "the artifact check-versioning.py is hardcoded to and whose D9 citation is "
     "frozen by §7.2"),
    (V4_CHECKER,
     "permanently red by construction; recorded because its AttributeError "
     "exits 1 indistinguishably from a finding"),
)

RESIDUAL_OWNERS = {
    "R-VER12-01": "phase1a prose-authority lane",
    "R-VER12-02": "phase1a prose-authority lane",
    "R-VER12-03": "phase1a prose-authority lane",
    "R-VER12-04": "independent reviewer",
    "R-VER12-05": "coordinator",
    "R-VER12-06": "coordinator",
    "R-VER12-07": "coordinator",
    "R-VER12-08": "independent reviewer",
    "R-VER12-09": "phase1a prose-authority lane",
    "R-VER12-10": "phase1a prose-authority lane",
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


def authored(m: dict[str, Any]) -> dict[str, tuple[Any, str]]:
    """Every position this successor authors, rendered from this checker's own
    constants and its own measurements. The same map generates the artifact and
    gates it: there is no free-prose position anywhere in this block, which is
    the whole of the B-VER11R-01 repair, and there is nothing here that is not
    also compared."""
    f: dict[str, tuple[Any, str]] = {}
    review = m["review11"]
    pur = m["purity"]
    census = m["census"]
    parts = m["partitions"]
    prose = m["prose"]
    lint = m["lint"]
    sweeps = m["sweeps"]
    rows = m["sentences"]
    probes = m["probes"]
    attr = m["attribution"]
    live = m["rehearsalsLive"]
    synth = m["rehearsalsSynthetic"]
    gate = m["depsGate"]
    defect = m["evidenceDefect"]
    pred_limits = len(pinned(PREDECESSOR).get("knownLimitations") or [])
    a = AUTHOR

    # ---- identity, top level ------------------------------------------------
    put(f, "version", 12)
    put(f, "supersedes", 11)
    put(f, "role",
        "A-prime v4 prose-authority successor; the v11 enforcement-closure "
        "record is carried byte-identical and gated leaf-wise against those "
        "bytes, B-VER11R-01 is closed on the artifact side by classifying every "
        "string leaf as RENDERED, CARRIED or PROTECTED instead of by a pattern "
        "table, and the relocation of the paper-seal class from this contract "
        "to check-versioning-v12.py is published as a measured residual rather "
        "than claimed away")
    for index in range(pred_limits):
        put(f, f"knownLimitations[{index}]",
            pinned(PREDECESSOR)["knownLimitations"][index], FROM_DISK)
    added = [
        f"A paper seal is a claim about assurance state made where the artifact "
        f"has no authority to make it. VERSIONING v11 declared that class "
        f"closed in free prose; its instrument closed "
        f"{len(SEAL_PATTERNS_ARTIFACT) + len(SEAL_PATTERNS_REVISION)} phrases, "
        f"and the independent reviewer planted "
        f"{review['plantedAdmitted']} of {review['plantedAttempted']} "
        f"differently-worded claims at exit 0. In v12 no string leaf in this "
        f"contract is free prose: {prose['rendered']} are RENDERED and compared "
        f"whole against a value check-versioning-v12.py produces, "
        f"{prose['carried']} are CARRIED byte-identical from the pinned "
        f"predecessor, of which {prose['alsoProtectedAsASection']} also sit "
        f"inside a canonically compared protected section. {prose['free']} are "
        f"free, and an appended sentence is rejected at every one of them by a "
        f"finding naming the position.",
        f"The class is not eliminated. It is relocated to the instrument. A "
        f"rendered leaf cannot be authored from this contract, but it can be "
        f"authored from check-versioning-v12.py by editing the constant there "
        f"and the leaf here together, so what v12 closes is the one-file edit "
        f"and what stays open is the two-file edit. The measured size of the "
        f"relocated surface is {prose['rendered']} rendered string leaves, and "
        f"an appended sentence is admitted at "
        f"{sweeps['authoredAdmitted']} of {sweeps['authoredPositions']} "
        f"authored string positions across "
        f"{sweeps['authoredSentences']} wordings.",
        f"registry_purity() in the predecessor is a naming lint, not a "
        f"structural proof. Measured here on every run: it catches "
        f"{pur['evasionsCaughtByTheNameLevelLint']} of "
        f"{pur['evasionsAttempted']} of the reviewer's own constructions, and "
        f"an AST measure that counts loops sized from ANY parameter catches "
        f"{pur['evasionsCaughtByTheAstMeasure']} of "
        f"{pur['evasionsAttempted']}. This checker's builders are NOT loop-free "
        f"— they contain {pur['myAstParameterSizedLoops']} parameter-sized "
        f"loops — and the class is closed by the declared provenance of every "
        f"sizing parameter instead, of which "
        f"{len(pur['sizingParametersWithoutDeclaredProvenance'])} are "
        f"undeclared.",
        f"The guard that actually held the predecessor's evidence registry was "
        f"undeclared. Its docstring says it \"{defect['theClaim']}\", which is "
        f"false: deps IS value['decisionDependencies'] and that builder has "
        f"{defect['astParameterSizedLoopsInThatBuilder']} parameter-sized "
        f"loops. What held the line was an equality gate with a pinned "
        f"fallback. Here that gate is declared and its firing is measured on "
        f"every run: appending a decisionDependencies entry fires VER12-DEP and "
        f"the as-of registry grows by "
        f"{minus(gate['positionsAfter'], gate['positionsBefore'])} "
        f"positions.",
        f"The coordinator has advanced retention-tiers to v24 in both prose "
        f"documents while claim-register.v1.json still binds "
        f"{m['liveRetentionTiers']}. Both live repoints are rehearsed in "
        f"process on every run: v23 costs {live[0]['findings']} findings and "
        f"{live[0]['leafEdits']} leaf edits, v24 costs {live[1]['findings']} "
        f"findings and {live[1]['leafEdits']} leaf edits, each with "
        f"{live[0]['checkerEdits']} checker edits, {live[0]['indexShifts']} "
        f"index shifts and {live[0]['findingsNotSelfRepairing']} findings whose "
        f"printed repair instruction could not be followed mechanically.",
    ]
    for offset, text in enumerate(added):
        put(f, f"knownLimitations[{pred_limits + offset}]", text, FROM_DISK)

    put(f, "successorRevision.id",
        "VERSIONING-v12-PROSE-AUTHORITY-SUCCESSOR")
    put(f, "successorRevision.supersedesCandidate.artifact", PREDECESSOR)
    put(f, "successorRevision.supersedesCandidate.sha256", PINS[PREDECESSOR],
        FROM_DISK)
    put(f, "successorRevision.supersedesCandidate.checker", PREDECESSOR_CHECKER)
    put(f, "successorRevision.supersedesCandidate.checkerSha256",
        PINS[PREDECESSOR_CHECKER], FROM_DISK)
    put(f, "successorRevision.identityStability.predecessor", "VERSIONING-v11")
    put(f, "successorRevision.identityStability.state",
        "EXACT-CUSTODY-IDENTITIES-UNCHANGED")
    put(f, "successorRevision.identityStability.reason",
        f"B-VER11R-01 is a defect of the enforcement instrument and of one "
        f"leaf of narration, not of any custody identity. No custodyClass, "
        f"versionedIdentity, rule, supportWindow or migrator moves in v12; "
        f"{prose['carried']} of the {prose['stringLeaves']} string leaves in "
        f"this contract are held byte-identical against "
        f"versioning-policy.v11.json.")

    # ---- the block ----------------------------------------------------------
    put(f, f"{a}.findingId", review["blockerId"])
    put(f, f"{a}.authoredBy", "phase1a prose-authority lane")

    r = f"{a}.reviewOfRecord"
    put(f, f"{r}.artifact", PREDECESSOR_REVIEW)
    put(f, f"{r}.sha256", sha_file(PREDECESSOR_REVIEW), FROM_DISK)
    put(f, f"{r}.verdict", review["verdict"], FROM_DISK)
    put(f, f"{r}.blockingFindingCount", review["blockingFindingCount"],
        FROM_DISK)
    put(f, f"{r}.nonBlockingObservationCount",
        review["nonBlockingObservationCount"], FROM_DISK)
    put(f, f"{r}.blockerIsAgainst", PREDECESSOR_CHECKER)
    put(f, f"{r}.plantedSealsAdmitted", review["plantedAdmitted"], FROM_DISK)
    put(f, f"{r}.plantedSealsAttempted", review["plantedAttempted"], FROM_DISK)
    put(f, f"{r}.plantedPositions", review["plantedPositions"], FROM_DISK)
    put(f, f"{r}.decisiveSweepPositions", review["sweptPositions"], FROM_DISK)
    put(f, f"{r}.decisiveSweepNeutralAdmitted", review["neutralAdmitted"],
        FROM_DISK)
    put(f, f"{r}.decisiveSweepPredecessorSealAdmitted",
        review["predecessorSealAdmitted"], FROM_DISK)
    put(f, f"{r}.decisiveSweepRewordedSealAdmitted", review["rewordedAdmitted"],
        FROM_DISK)

    put(f, f"{a}.defect",
        f"versioning-policy.v11.json "
        f"successorRevision.enforcementClosureRepair.prosePaperSealScan.rule "
        f"declares \"The seal FIELDS were already gated; this closes the class "
        f"in free prose.\" The scan closes "
        f"{len(SEAL_PATTERNS_ARTIFACT)} verdict-inheritance patterns over every "
        f"string leaf and {len(SEAL_PATTERNS_REVISION)} bare seal patterns over "
        f"successorRevision — {len(SEAL_PATTERNS_ARTIFACT) + len(SEAL_PATTERNS_REVISION)} "
        f"phrases. The reviewer planted {review['plantedAdmitted']} of "
        f"{review['plantedAttempted']} re-worded claims at exit 0 across "
        f"{review['plantedPositions']} positions including top-level role, and "
        f"the same wordings run through the checker's own sweep were admitted "
        f"at {review['rewordedAdmitted']} of {review['sweptPositions']} — "
        f"exactly the neutral sentence's {review['neutralAdmitted']}. The "
        f"declared {review['predecessorSealAdmitted']}-of-"
        f"{review['sweptPositions']} asymmetry measured the pattern table "
        f"against itself.", FROM_DISK)
    put(f, f"{a}.whySuccessorAndNotInPlaceRepair",
        "freeze §7.2 binds a verdict to bytes. versioning-policy.v11.json was "
        "reviewed at 5e0d31de… and check-versioning-v11.py at 662781af…; "
        "repairing either in place would silently retune bytes an independent "
        "reviewer adjudicated. The repair is also not a patch to the pattern "
        "table: a table is what failed, and adding phrases to it would "
        "reproduce B-VER11R-01 at the next re-wording.")

    # ---- the closure --------------------------------------------------------
    p = f"{a}.proseAuthorityPartition"
    put(f, f"{p}.rule",
        "Every string leaf in this contract is classified by HOW IT IS HELD, "
        "never by what it says. RENDERED: the whole value is equality-compared "
        "against a string check-versioning-v12.py produces from its own "
        "constants and its own measurements. CARRIED: the whole value is "
        "equality-compared against the SHA-verified pinned predecessor's byte "
        "at that position. FREE: neither, which is a finding naming the "
        "position. A re-wording cannot evade a rule that never reads the "
        "words, and every rejection names the leaf rather than the section it "
        "sits in.")
    put(f, f"{p}.stringLeaves", prose["stringLeaves"], FROM_DISK)
    put(f, f"{p}.RENDERED", prose["rendered"], FROM_DISK)
    put(f, f"{p}.CARRIED", prose["carried"], FROM_DISK)
    put(f, f"{p}.FREE", prose["free"], FROM_DISK)
    put(f, f"{p}.alsoProtectedAsACanonicalJsonSection",
        prose["alsoProtectedAsASection"], FROM_DISK)
    put(f, f"{p}.positionDigest", prose["digest"], FROM_DISK)
    put(f, f"{p}.whyThisIsNotAPhraseList",
        "The predecessor's scan asked whether a sentence spells one of 16 "
        "phrases. This asks whether a position is one the artifact may author "
        "at all. The first question has an unbounded number of wrong answers "
        "and the reviewer found four of them; the second has no wording in it.")
    put(f, f"{p}.theRenderedSubtreeIsComparedWhole",
        "beyond the per-position comparison, the entire authored subtree — "
        "role, knownLimitations, version, supersedes, the three "
        "successor-identity leaves and this block — is rebuilt from the same "
        "map that generates the registry and compared as canonical JSON "
        "against what this contract carries. A shape the checker does not "
        "produce is a position the artifact authored on its own authority.")
    put(f, f"{p}.whatThisDoesNotClose",
        "It does not make any sentence true. A rendered leaf is fixed, not "
        "verified: check-versioning-v12.py holds the bytes and compares them, "
        "and a false sentence agreed between this contract and that checker "
        "passes. That is R-VER12-01 and it is the honest ceiling of this "
        "repair.")

    s = f"{a}.appendAdmissionSweep"
    put(f, f"{s}.rule",
        "The closure is measured, not argued. Each sentence of the re-wording "
        "test set is APPENDED to a string leaf — removing nothing, so every "
        "substring any comparator might require survives — and the whole "
        "checker is run against each candidate in turn. Admission is exit 0 "
        "OR rejection by a finding that does not name the position.")
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
    put(f, f"{s}.predecessorAdmittedInsideItsDeclaredBoundary",
        sweeps["predInside"], FROM_DISK)
    put(f, f"{s}.predecessorAdmittedOutsideItsDeclaredBoundary",
        sweeps["predOutside"], FROM_DISK)
    put(f, f"{s}.predecessorPositionsOutsideItsDeclaredBoundary",
        sweeps["predOutsidePositions"], FROM_DISK)
    put(f, f"{s}.thePredecessorBoundaryWidened",
        f"R-VER11-01 publishes a sweep scoped to the "
        f"{review['sweptPositions']} string positions of its closure block, and "
        f"review O-04 recorded that positions outside it also admit. Measured "
        f"here: {sweeps['predOutside']} of the "
        f"{sweeps['predOutsidePositions']} authored string positions OUTSIDE "
        f"that boundary admit an appended re-worded assurance claim — top-level "
        f"role, the five added knownLimitations, and "
        f"successorRevision.identityStability.reason, which the review did not "
        f"name. The widened figure is {sweeps['predAdmitted']} of "
        f"{sweeps['predPositions']}.", FROM_DISK)
    put(f, f"{s}.whatTheCrossProductCovers",
        "one string position from each prose-authority class and from each "
        "authored and carried sub-block, so the test set is measured across "
        "the partition rather than at one convenient leaf")
    put(f, f"{s}.whatIsNotSweptOnAPlainRun",
        f"the {prose['carried']} CARRIED string leaves. --selftest sweeps every "
        f"string leaf in the contract, all {prose['stringLeaves']} of them, and "
        f"that figure is declared below and compared there.")
    put(f, f"{s}.wholeContractSweepPositions", prose["stringLeaves"], FROM_DISK)
    put(f, f"{s}.wholeContractSweepAdmittedUnderSelftest", 0)

    w = f"{a}.rewordingTestSet"
    put(f, f"{w}.rule",
        f"{len(review['wordings'])} of these sentences are READ FROM "
        f"{PREDECESSOR_REVIEW} rather than retyped, so this checker cannot "
        f"quietly test something easier than what defeated its predecessor. "
        f"The remaining {len(MY_WORDINGS)} are authored here to probe evasion "
        f"strategies the reviewer's four do not: a sentence with no assurance "
        f"vocabulary at all, a nominalised one, a purely numeric one, an "
        f"indirect one, a quotation-shaped one and a one-word one.")
    for index, row in enumerate(rows):
        put(f, f"{w}.sentences[{index}].index", index)
        put(f, f"{w}.sentences[{index}].provenance", row["provenance"],
            FROM_DISK)
        put(f, f"{w}.sentences[{index}].sentence",
            f"\"{row['sentence']}\" — planted and REJECTED at every position "
            f"swept here (B-VER11R-01)", FROM_DISK)
        put(f, f"{w}.sentences[{index}].caughtByTheLexicalLint",
            row["caughtByTheLint"], FROM_DISK)
        put(f, f"{w}.sentences[{index}].admittedHere", row["admittedHere"],
            FROM_DISK)
    put(f, f"{w}.sentenceCount", len(rows), FROM_DISK)
    put(f, f"{w}.readFromTheReview", len(review["wordings"]), FROM_DISK)
    put(f, f"{w}.authoredHere", len(MY_WORDINGS))
    put(f, f"{w}.caughtByTheLexicalLint", m["lintCatches"], FROM_DISK)
    put(f, f"{w}.caughtByTheProseAuthorityPartition", len(rows), FROM_DISK)
    put(f, f"{w}.admittedHere", sweeps["crossAdmitted"], FROM_DISK)

    x = f"{a}.lexicalSealLint"
    put(f, f"{x}.status",
        f"RETAINED AS A LINT, NOT AS A CLOSURE. It is carried verbatim from "
        f"{PREDECESSOR_CHECKER} so that its evasion rate is measured against "
        f"the same bytes the review defeated. Its measured catch rate over the "
        f"test set is {m['lintCatches']} of {len(rows)}; the partition's is "
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
    put(f, f"{x}.whyItIsKept",
        "a hit is a cheap signal and costs nothing; publishing it beside its "
        "measured evasion rate is the difference between an instrument and a "
        "claim. The predecessor published the same instrument as the closure "
        "of a class, which is B-VER11R-01.")

    # ---- purity -------------------------------------------------------------
    y = f"{a}.registryPurity"
    put(f, f"{y}.principleCorrected",
        f"The predecessor's docstring says \"it is not possible to write an "
        f"artifact-sized loop in one\". That overstates what its instrument "
        f"measures. This checker's registry builders contain "
        f"{pur['myAstParameterSizedLoops']} parameter-sized loops by AST "
        f"measure, and that number is published rather than driven to zero: "
        f"registries ARE parameter-sized. What closes the class is the "
        f"PROVENANCE of every sizing parameter.", FROM_DISK)
    for index, name in enumerate(REGISTRY_BUILDERS):
        row = pur["mine"][name]
        put(f, f"{y}.builders[{index}].function", name)
        put(f, f"{y}.builders[{index}].nameLevelArtifactParameters",
            row["lint"]["artifactParameters"], FROM_DISK)
        put(f, f"{y}.builders[{index}].nameLevelArtifactSizedLoops",
            row["lint"]["artifactSizedLoops"], FROM_DISK)
        put(f, f"{y}.builders[{index}].astLoops", row["ast"]["loopCount"],
            FROM_DISK)
        put(f, f"{y}.builders[{index}].astParameterSizedLoops",
            row["ast"]["parameterSizedLoops"], FROM_DISK)
        put(f, f"{y}.builders[{index}].astSizingParameters",
            " | ".join(row["ast"]["sizingParameters"]), FROM_DISK)
    for index, name in enumerate(PREDECESSOR_REGISTRY_BUILDERS):
        row = pur["theirs"][name]
        put(f, f"{y}.predecessorBuilders[{index}].function", name)
        put(f, f"{y}.predecessorBuilders[{index}].nameLevelArtifactSizedLoops",
            row["lint"]["artifactSizedLoops"], FROM_DISK)
        put(f, f"{y}.predecessorBuilders[{index}].astParameterSizedLoops",
            row["ast"]["parameterSizedLoops"], FROM_DISK)
        put(f, f"{y}.predecessorBuilders[{index}].astSizingParameters",
            " | ".join(row["ast"]["sizingParameters"]), FROM_DISK)
    for index, row in enumerate(pur["evasions"]):
        put(f, f"{y}.evasionSuite[{index}].construction", row["construction"],
            FROM_DISK)
        put(f, f"{y}.evasionSuite[{index}].nameLevelLintArtifactSizedLoops",
            row["nameLevelLintArtifactSizedLoops"], FROM_DISK)
        put(f, f"{y}.evasionSuite[{index}].astParameterSizedLoops",
            row["astStructuralParameterSizedLoops"], FROM_DISK)
        put(f, f"{y}.evasionSuite[{index}].caughtByTheNameLevelLint",
            row["caughtByTheNameLevelLint"], FROM_DISK)
        put(f, f"{y}.evasionSuite[{index}].caughtByTheAstMeasure",
            row["caughtByTheAstMeasure"], FROM_DISK)
    put(f, f"{y}.evasionsAttempted", pur["evasionsAttempted"], FROM_DISK)
    put(f, f"{y}.evasionsCaughtByTheNameLevelLint",
        pur["evasionsCaughtByTheNameLevelLint"], FROM_DISK)
    put(f, f"{y}.evasionsCaughtByTheAstMeasure",
        pur["evasionsCaughtByTheAstMeasure"], FROM_DISK)
    put(f, f"{y}.evasionSuiteProvenance",
        "the three constructions are the ones the independent reviewer wrote to "
        "defeat the predecessor's registry_purity(); they are held as source "
        "in this checker and compiled and measured on every run")
    for index, key in enumerate(sorted(PROVENANCE)):
        put(f, f"{y}.provenance[{index}].builder", key[0])
        put(f, f"{y}.provenance[{index}].parameter", key[1])
        put(f, f"{y}.provenance[{index}].source", PROVENANCE[key])
    put(f, f"{y}.declaredProvenanceEntries", pur["declaredProvenanceEntries"],
        FROM_DISK)
    put(f, f"{y}.measuredSizingParameters", pur["measuredSizingParameters"],
        FROM_DISK)
    put(f, f"{y}.sizingParametersWithoutDeclaredProvenance",
        len(pur["sizingParametersWithoutDeclaredProvenance"]), FROM_DISK)
    put(f, f"{y}.theGate",
        "the AST-measured set of (builder, sizing parameter) pairs is compared "
        "against the declared provenance table's key set. A future editor who "
        "adds a parameter that sizes a loop must declare where its size comes "
        "from, or this check fails naming the pair.")
    put(f, f"{y}.nameLevelLintDisposition",
        f"published as the naming lint it is. It reports "
        f"{pur['myNameLevelArtifactSizedLoops']} artifact-sized loops here and "
        f"{pur['predecessorNameLevelArtifactSizedLoops']} in "
        f"{PREDECESSOR_CHECKER}'s builders, and it catches "
        f"{pur['evasionsCaughtByTheNameLevelLint']} of "
        f"{pur['evasionsAttempted']} constructions written to defeat it.",
        FROM_DISK)

    e = f"{a}.evidenceRegistryCorrection"
    put(f, f"{e}.subject",
        f"{PREDECESSOR_CHECKER} evidence_registry()")
    put(f, f"{e}.predecessorDocstringClaim", defect["theClaim"], FROM_DISK)
    put(f, f"{e}.thatClaimIsPresentInThePinnedSource",
        defect["docstringContainsTheClaim"], FROM_DISK)
    put(f, f"{e}.correctedStatement",
        "FALSE AS WRITTEN. deps IS value['decisionDependencies']: the "
        "predecessor's _check() binds it from the artifact and passes it to "
        "evidence_registry(), whose audit loop emits one group of positions per "
        "dependency. The builder is artifact-sized through deps.", FROM_DISK)
    put(f, f"{e}.depsIsBoundFromTheArtifact",
        defect["depsIsBoundFromTheArtifact"], FROM_DISK)
    put(f, f"{e}.depsIsPassedToTheBuilder", defect["depsIsPassedToTheBuilder"],
        FROM_DISK)
    put(f, f"{e}.astParameterSizedLoopsInThatBuilder",
        defect["astParameterSizedLoopsInThatBuilder"], FROM_DISK)
    put(f, f"{e}.theGateThatActuallyHolds",
        "an equality gate with a pinned fallback: canon(deps) is compared "
        "against the pinned predecessor's decisionDependencies and, on any "
        "difference, VER12-DEP is emitted AND deps is replaced with the pinned "
        "list BEFORE any registry is built. The predecessor's record declared "
        "no such mechanism; the reviewer found it by reading the source and "
        "could not get past it.")
    put(f, f"{e}.gateExistsInThePredecessor",
        defect["equalityGateWithPinnedFallbackExists"], FROM_DISK)
    put(f, f"{e}.gateFiresHere", gate["gateFires"], FROM_DISK)
    put(f, f"{e}.gateFindingIds", gate["findingIds"], FROM_DISK)
    put(f, f"{e}.asOfRegistryPositionsBeforeTheProbe", gate["positionsBefore"],
        FROM_DISK)
    put(f, f"{e}.asOfRegistryPositionsAfterTheProbe", gate["positionsAfter"],
        FROM_DISK)
    put(f, f"{e}.andSeparately",
        "in this checker the as-of registry is sized by the CARRIED position "
        "set rather than by deps at all: measure_audit() supplies values, and "
        "the position set comes from the pinned predecessor's bytes. The gate "
        "is therefore defence in depth here rather than the only guard, and "
        "both facts are measured rather than asserted.")

    # ---- census and partition ----------------------------------------------
    c = f"{a}.coverageCensus"
    put(f, f"{c}.rule",
        "every leaf position in the whole contract is assigned to exactly one "
        "gate: an enforcement scope, the canonical-JSON comparison of the "
        "protected surface, or byte-carry against the pinned predecessor. A "
        "position that lands in none increments the ungated count, which is "
        "declared and compared.")
    put(f, f"{c}.artifactLeafPositions", census["total"], FROM_DISK)
    put(f, f"{c}.gatedPerLeafByAnEnforcementScope", census["scope"], FROM_DISK)
    put(f, f"{c}.gatedOnlyByASectionComparison", census["sectionOnly"],
        FROM_DISK)
    put(f, f"{c}.ungated", census["ungated"], FROM_DISK)
    put(f, f"{c}.alsoByteCarriedAgainstThePredecessor",
        census["alsoByteCarried"], FROM_DISK)
    put(f, f"{c}.alsoProtectedAsACanonicalJsonSection",
        census["alsoProtectedAsASection"], FROM_DISK)
    put(f, f"{c}.predecessorDeclaredByteCarryFigure",
        m["predCensus"]["declaredByteCarry"], FROM_DISK)
    put(f, f"{c}.predecessorLeavesInBothAScopeAndByteCarry",
        m["predCensus"]["doubleGated"], FROM_DISK)
    put(f, f"{c}.predecessorByteCarriedIncludingDoubleGated",
        m["predCensus"]["byteCarriedIncludingDoubleGated"], FROM_DISK)
    put(f, f"{c}.whyTheDoubleGatedFiguresArePublished",
        f"review O-03: the predecessor's census assigned each leaf to its "
        f"strongest gate and published only that figure. Measured here with the "
        f"predecessor's OWN coverage_census() over its own bytes: it declares "
        f"{m['predCensus']['declaredByteCarry']} byte-carried leaves, while "
        f"{m['predCensus']['doubleGated']} of the leaves it counted under a "
        f"scope are byte-carried as well, so its real byte-carried surface is "
        f"{m['predCensus']['byteCarriedIncludingDoubleGated']}. The error is in "
        f"the safe direction — every one of those leaves is gated twice — but a "
        f"published figure should be the one that was measured. Here every leaf "
        f"is gated per leaf and both further gates are counted and published "
        f"rather than folded in.", FROM_DISK)
    put(f, f"{c}.whyTheProtectedSurfaceIsNowPerLeaf",
        "the predecessor compared its protected top-level sections as whole "
        "canonical-JSON blobs. That rejects an appended sentence, but the "
        "finding names the SECTION and not the position — the collateral "
        "rejection review O-04 recorded one level down. Measured before this "
        "repair: an appended re-worded assurance claim was rejected without "
        "its position being named at 1742 of the 2823 string leaves in this "
        "contract. Per-leaf comparison is what took that figure to 0.")

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
    put(f, f"{q}.everyPositionIsMEASURED",
        "there is no GROUNDED and no UNMEASURABLE position in any scope of this "
        "successor. The predecessor's closure block carried 89 GROUNDED prose "
        "positions gated on measured substrings, which is what made an appended "
        "sentence admissible there. Substring enforcement is gone from the "
        "authored surface; what replaces it is fixity, not truth, and "
        "R-VER12-01 says so.")

    b = f"{a}.carriedByteIdentical"
    put(f, f"{b}.rule",
        f"every successorRevision key except id, supersedesCandidate, "
        f"identityStability and proseAuthorityRepair is carried from "
        f"{PREDECESSOR} byte-identical and gated leaf-wise against those bytes, "
        f"and every top-level key except version, supersedes, role, "
        f"knownLimitations and successorRevision is compared as canonical JSON "
        f"against them.")
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
        "and there is no index to shift. A carried position may differ from the "
        "predecessor's bytes only where an as-of comparison independently "
        "re-measures it against the live register.")
    put(f, f"{b}.asOfPositions", m["asofPositions"], FROM_DISK)
    put(f, f"{b}.asOfRule",
        f"any carried leaf whose path ends in {' or '.join(AS_OF_SUFFIXES)} is "
        f"a RECORDED MEASUREMENT of a file that moves, so it is compared "
        f"against the live register instead of against the carried byte. The "
        f"rule is a suffix test over the carried position set, not a list of "
        f"paths, so a new register column is covered the day it appears.")

    # ---- register -----------------------------------------------------------
    g = f"{a}.registerAsOfAudit"
    put(f, f"{g}.principle",
        "R-VER10-08's axis, upheld unchanged and applied rather than quoted: "
        "measurements get hard comparison, invariants get semantic gates. A "
        "registerBinding is a recorded measurement — at authoring, X was Y — so "
        "going stale is a true positive about these bytes. "
        "decisionDependencies[4].source is a continuing invariant and is gated "
        "against the register's LIVE D9 binding, because a byte pin fails on "
        "the very repoint it anticipates.")
    put(f, f"{g}.noRegisterDigestIsRecordedInThisBlock", True)
    put(f, f"{g}.whyNot",
        "a digest of a file that is expected to move is a timestamp, not "
        "evidence, and recording one uncompared is the B-VER9R-01 shape. What "
        "is recorded instead is the set of bindings this artifact depends on, "
        "and every one of them is hard-compared.")
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
        "run: the register is substituted behind one indirection, this whole "
        "checker is run, exactly what each finding names is applied and nothing "
        "else, and the loop iterates to a fixed point. No file anywhere under "
        "docs/coop is written to perform a rehearsal.")
    for index, row in enumerate(live):
        put(f, f"{k}.live[{index}].target", row["target"])
        put(f, f"{k}.live[{index}].findingsOnTheFirstRound", row["findings"],
            FROM_DISK)
        put(f, f"{k}.live[{index}].findingIds", row["findingIds"], FROM_DISK)
        put(f, f"{k}.live[{index}].roundsToExitZero", row["roundsToGreen"],
            FROM_DISK)
        put(f, f"{k}.live[{index}].leafEdits", row["leafEdits"], FROM_DISK)
        put(f, f"{k}.live[{index}].checkerEdits", row["checkerEdits"], FROM_DISK)
        put(f, f"{k}.live[{index}].indexShifts", row["indexShifts"], FROM_DISK)
        put(f, f"{k}.live[{index}].positionsAddedOrRemoved",
            row["positionsAddedOrRemoved"], FROM_DISK)
        put(f, f"{k}.live[{index}].findingsNotSelfRepairing",
            row["findingsNotSelfRepairing"], FROM_DISK)
        put(f, f"{k}.live[{index}].reachedExitZero", row["reachedExitZero"],
            FROM_DISK)
    for index, row in enumerate(synth):
        put(f, f"{k}.syntheticCouplingSurface[{index}].event", row["event"])
        put(f, f"{k}.syntheticCouplingSurface[{index}]."
               f"enumeratedByThePredecessorResidual", row["enumerated"])
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
    put(f, f"{k}.theRepairPathIsSelfDocumenting",
        f"each VER12-ASOF and VER12-LEAF message prints the measured value in "
        f"full when it is at most {SHOW_LIMIT} canonical characters, and marks "
        f"it with an ellipsis when it is not. The rehearsal follows only what "
        f"the messages print and counts every message it could not follow; "
        f"that count is declared above and it is the boundary of this claim.",
        FROM_DISK)

    # ---- predecessor --------------------------------------------------------
    d = f"{a}.predecessorDisposition"
    put(f, f"{d}.rule",
        "the pinned predecessor pair is executed against its own bytes rather "
        "than assumed green, and it is NOT required to be silent: it is frozen, "
        "and a coordinator repoint makes it red through no fault of any "
        "artifact. Requiring silence from an instrument nobody may repair would "
        "be the defect, not the guard.")
    put(f, f"{d}.attributionMethod", attr["method"], FROM_DISK)
    put(f, f"{d}.whyNotASubstring",
        f"review O-05: the predecessor bounded this with `'registerBinding' not "
        f"in finding`, a substring over the finding TEXT standing in for a test "
        f"that the finding names a registerBinding PATH. Here the predecessor "
        f"is run twice and the attribution is measured, so a genuine defect "
        f"whose prose happens to contain the token is not admitted.")
    put(f, f"{d}.findingsAgainstItsOwnBytes", attr["findingsAgainstItsOwnBytes"],
        FROM_DISK)
    put(f, f"{d}.findingsUnderTheRegisterStateItRecorded",
        attr["findingsUnderTheRegisterStateItRecorded"], FROM_DISK)
    put(f, f"{d}.findingsAttributableToACoordinatorRepoint",
        attr["findingsAttributableToACoordinatorRepoint"], FROM_DISK)
    put(f, f"{d}.genuineDefects", attr["genuineDefects"], FROM_DISK)
    put(f, f"{d}.predecessorSealScanEvasionRate",
        f"{m['lintCatches']} of {len(rows)} test-set sentences are caught by "
        f"the predecessor's pattern table; {sweeps['predAdmitted']} of "
        f"{sweeps['predPositions']} authored string positions in "
        f"{PREDECESSOR} admit an appended re-worded seal under "
        f"{PREDECESSOR_CHECKER}.", FROM_DISK)
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

    n = f"{a}.closedScalarAdmission"
    put(f, f"{n}.law", "freeze §6 law 18 — closed-scalar admission is "
                       "exact-type in BOTH directions")
    put(f, f"{n}.booleanLeavesSwept", m["boolSweep"]["total"], FROM_DISK)
    put(f, f"{n}.boolToIntAdmitted", m["boolSweep"]["admitted"], FROM_DISK)
    put(f, f"{n}.sweptBy", "a plain invocation as well as --selftest")
    put(f, f"{n}.scope", "successorRevision")

    t = f"{a}.selftestProfile"
    put(f, f"{t}.countedBy", "type transition, not label text")
    put(f, f"{t}.mutations", m["census12"]["total"], FROM_DISK)
    put(f, f"{t}.floatRespellings", m["census12"]["floatRespellings"],
        FROM_DISK)
    put(f, f"{t}.booleanRespellings", m["census12"]["booleanRespellings"],
        FROM_DISK)
    put(f, f"{t}.assertionsOnAFullDottedPath", m["fullPathAssertions"],
        FROM_DISK)
    put(f, f"{t}.assertionsOnASectionName", m["sectionAssertions"], FROM_DISK)
    put(f, f"{t}.distinctFindingIdsExercised", m["distinctIds"], FROM_DISK)
    put(f, f"{t}.predecessorMutations", m["census11"]["total"], FROM_DISK)
    put(f, f"{t}.predecessorFloatRespellings",
        m["census11"]["floatRespellings"], FROM_DISK)
    put(f, f"{t}.predecessorBooleanRespellings",
        m["census11"]["booleanRespellings"], FROM_DISK)

    # ---- residual restatements ---------------------------------------------
    restated = [
        ("R-VER11-01",
         "B-VER11R-01",
         f"The predecessor recorded that of the 257 string positions in its "
         f"closure block, {review['neutralAdmitted']} admit an appended false "
         f"sentence, and that the reviewer's verdict-inheritance sentence is "
         f"admitted at {review['predecessorSealAdmitted']} of "
         f"{review['sweptPositions']}.",
         f"The second figure was lexical. Re-worded, the same claim returns to "
         f"{review['rewordedAdmitted']} of {review['sweptPositions']}. Measured "
         f"here across the whole predecessor authored surface: "
         f"{sweeps['predAdmitted']} of {sweeps['predPositions']} positions "
         f"admit it. In v12 the figure is {sweeps['authoredAdmitted']} of "
         f"{sweeps['authoredPositions']} over "
         f"{sweeps['authoredSentences']} wordings, because the enforcement is "
         f"no longer by substring."),
        ("R-VER11-08",
         "R-VER10-08 upheld",
         f"The predecessor rehearsed the pending repoint against a synthetic "
         f"target and declared a cost of "
         f"{synth[0]['declaredLeavesThatWouldChange']} leaves on the coupling "
         f"surface.",
         f"Upheld and extended to the live targets the coordinator has actually "
         f"created. v23 costs {live[0]['findings']} findings and "
         f"{live[0]['leafEdits']} leaf edits; v24 — the head both prose "
         f"documents now name — costs {live[1]['findings']} findings and "
         f"{live[1]['leafEdits']} leaf edits. Neither adds a position, neither "
         f"shifts an index, and neither needs a checker edit."),
    ]
    for index, (rid, observation, was, now) in enumerate(restated):
        put(f, f"{a}.residualRestatements[{index}].id", rid)
        put(f, f"{a}.residualRestatements[{index}].reviewObservation",
            observation)
        put(f, f"{a}.residualRestatements[{index}].wasRecorded", was, FROM_DISK)
        put(f, f"{a}.residualRestatements[{index}].nowMeasured", now, FROM_DISK)

    for index, (name, role) in enumerate(V12_REQUIRED_INPUTS):
        put(f, f"{a}.recordedInputs[{index}].artifact", name)
        put(f, f"{a}.recordedInputs[{index}].sha256", sha_file(name), FROM_DISK)
        put(f, f"{a}.recordedInputs[{index}].role", role)
    put(f, f"{a}.recordedInputsRule",
        f"freeze §7.2 — filename and sha256 for every input this record depends "
        f"on. {len(V12_REQUIRED_INPUTS)} inputs, each measured from disk on "
        f"every run. {REGISTER} is deliberately absent: it is expected to move, "
        f"and a digest of a moving file is a timestamp rather than evidence.")

    # ---- retained residuals, each stating its boundary in measured digits ---
    residuals = [
        ("R-VER12-01",
         "The paper-seal class is closed on the artifact side and RELOCATED to "
         "the instrument, not eliminated.",
         f"{prose['rendered']} string leaves are RENDERED: their whole value is "
         f"compared against a string check-versioning-v12.py produces. An "
         f"appended sentence is admitted at {sweeps['authoredAdmitted']} of "
         f"{sweeps['authoredPositions']} authored positions and at "
         f"{sweeps['crossAdmitted']} of the "
         f"{sweeps['crossPositions']} × {sweeps['crossSentences']} test-set "
         f"cross product. But a rendered leaf is FIXED, not VERIFIED: a false "
         f"sentence agreed between this contract and that checker passes. The "
         f"surface an editor must move to plant a seal is 2 files rather than "
         f"1, and {prose['rendered']} leaves rather than "
         f"{sweeps['predAdmitted']}.",
         "Bounded and published rather than closed. Closing it would require "
         "the instrument to decide whether a sentence is true, which no "
         "byte-and-substring instrument can do and which this record does not "
         "claim."),
        ("R-VER12-02",
         "The lexical seal scan is retained only as a lint, and its evasion "
         "rate is the reason.",
         f"Carried verbatim from {PREDECESSOR_CHECKER}: "
         f"{len(SEAL_PATTERNS_ARTIFACT) + len(SEAL_PATTERNS_REVISION)} "
         f"patterns. Measured against the "
         f"{len(rows)}-sentence re-wording test set on every run, it catches "
         f"{m['lintCatches']}; the prose-authority partition catches "
         f"{len(rows)}. Nothing in this record rests on the lint, and its "
         f"hitsOutsideTheAllowlist figure of "
         f"{lint['hitsOutsideTheAllowlist']} is a signal, not a closure.",
         "Disclosed, not relied upon."),
        ("R-VER12-03",
         "The AST purity measure is conservative and its provenance table is "
         "authored, not derived.",
         f"The measure over-taints deliberately — a call that receives a "
         f"tainted argument taints every name it receives — so "
         f"{pur['myAstParameterSizedLoops']} parameter-sized loops are reported "
         f"here and {pur['predecessorAstParameterSizedLoops']} in the "
         f"predecessor's builders. It catches "
         f"{pur['evasionsCaughtByTheAstMeasure']} of "
         f"{pur['evasionsAttempted']} constructions the name-level lint catches "
         f"{pur['evasionsCaughtByTheNameLevelLint']} of. What it does NOT do is "
         f"prove that a declared provenance is the true one: "
         f"{pur['declaredProvenanceEntries']} provenance entries are written by "
         f"hand and only their KEY SET is compared against the "
         f"{pur['measuredSizingParameters']} measured pairs.",
         "Bounded. The key-set comparison closes silent addition; it does not "
         "close a mis-stated source."),
        ("R-VER12-04",
         "v12 carries no independent review.",
         f"The verdict of record is {review['verdict']} with "
         f"{review['blockingFindingCount']} blocking finding against "
         f"{PREDECESSOR_CHECKER}, and it binds the v11 bytes in either "
         f"direction, not these. status remains CANDIDATE-NOT-APPLIED, "
         f"reviewStatus remains AWAITING-INDEPENDENT-COMBINED-REREVIEW and "
         f"dischargeStatus.seal remains DO-NOT-SEAL.",
         "A new verdict on these bytes is required before v12 can carry one. "
         "Nothing here claims one."),
        ("R-VER12-05",
         "The register columns are a recorded measurement, hard-compared "
         "against a coordinator-owned file that moves.",
         f"Accepted deliberately and not weakened. What is bounded is the blast "
         f"radius, measured live on every run: repointing ARCH.RETENTION-TIERS "
         f"to {LIVE_REPOINT_TARGETS[0]} produces {live[0]['findings']} findings "
         f"and {live[0]['leafEdits']} leaf edits; to "
         f"{LIVE_REPOINT_TARGETS[1]} it produces {live[1]['findings']} findings "
         f"and {live[1]['leafEdits']} leaf edits. Checker edits "
         f"{live[1]['checkerEdits']}, index shifts {live[1]['indexShifts']}, "
         f"positions added or removed {live[1]['positionsAddedOrRemoved']}, "
         f"findings whose printed repair instruction could not be followed "
         f"mechanically {live[1]['findingsNotSelfRepairing']}.",
         "Accepted deliberately; the cost is declared, measured and in place."),
        ("R-VER12-06",
         "v12 is not the register-bound head.",
         f"{REGISTER} binds VERSIONING to {m['liveVersioning']}, which is "
         f"{m['versioningVersionsBehind']} versions behind these bytes, and "
         f"binds ARCH.RETENTION-TIERS to {m['liveRetentionTiers']} while both "
         f"prose documents name {DOCUMENTED_RT_HEAD}. This checker reads both "
         f"from the live register on every run and declares them rather than "
         f"assuming them.",
         "Deliberate. The register is coordinator-owned and was not touched by "
         "this successor."),
        ("R-VER12-07",
         "check-versioning.py remains permanently red and its crash is "
         "exit-code-indistinguishable from a finding.",
         f"{V4_CHECKER} hardcodes its subject to {V4} and its VER-DEP loop "
         f"calls d.get('source') over decisionDependencies, which from v7 "
         f"onward carries bare label strings, raising AttributeError. An "
         f"uncaught exception exits 1 — the same code as a legitimate finding.",
         "Not closable here; the only in-place fix is forbidden. This is why "
         "every finding in check-versioning-v12.py carries a stable id and "
         "names its position, and why --selftest asserts on both."),
        ("R-VER12-08",
         "The predecessor checkers are not repaired and still admit what this "
         "one rejects.",
         f"Executed on every run of this checker: {PREDECESSOR_CHECKER} admits "
         f"an appended re-worded assurance claim at {sweeps['predAdmitted']} of "
         f"{sweeps['predPositions']} authored string positions in its own "
         f"contract, and its registry_purity() catches "
         f"{pur['evasionsCaughtByTheNameLevelLint']} of "
         f"{pur['evasionsAttempted']} constructions written to defeat it. All "
         f"predecessor checkers are pinned by sha256 and cannot be edited.",
         "Recorded, not repaired. The chain's gate is the newest checker."),
        ("R-VER12-09",
         "The whole-contract append sweep runs under --selftest; a plain run "
         "sweeps the authored surface and a cross product.",
         f"A plain run sweeps {sweeps['authoredPositions']} authored string "
         f"positions across {sweeps['authoredSentences']} wordings and a "
         f"{sweeps['crossPositions']} × {sweeps['crossSentences']} cross "
         f"product spanning every prose-authority class. --selftest sweeps all "
         f"{prose['stringLeaves']} string leaves in the contract. The "
         f"{prose['carried']} CARRIED leaves are therefore measured once per "
         f"selftest rather than once per run; their gate is the same per-leaf "
         f"equality against the pinned predecessor either way.",
         "Deliberate scope, stated as a measured number rather than as a "
         "sample."),
        ("R-VER12-10",
         "A position being gated is not the same as its meaning being checked.",
         f"The census proves coverage, not correctness: "
         f"{census['total']} leaf positions, {census['scope']} classified "
         f"per-leaf by an enforcement scope, {census['sectionOnly']} gated only "
         f"as members of a protected top-level section, "
         f"{census['ungated']} ungated. For each class this checker establishes "
         f"that the bytes are what an adjudicated predecessor carried or what "
         f"it itself renders — not that the surrounding sentence is true. The "
         f"carried D9 span is still measured at "
         f"{m['d9SpanEndpoints']} endpoints only, with "
         f"{m['d9SpanIntermediates']} intermediate versions on disk unread.",
         "Disclosed. It is the honest ceiling of a byte instrument, and it is "
         "why every residual boundary here is stated in this checker's own "
         "measured numbers."),
    ]
    for index, (rid, residual, measured, disposition) in enumerate(residuals):
        put(f, f"{a}.retainedResiduals[{index}].id", rid)
        put(f, f"{a}.retainedResiduals[{index}].residual", residual)
        put(f, f"{a}.retainedResiduals[{index}].measured", measured, FROM_DISK)
        put(f, f"{a}.retainedResiduals[{index}].disposition", disposition)
        put(f, f"{a}.retainedResiduals[{index}].ownedBy", RESIDUAL_OWNERS[rid])

    z = f"{a}.checkerDisposition"
    put(f, f"{z}.successorCheckerRequired", True)
    put(f, f"{z}.checker", pathlib.Path(__file__).name, FROM_DISK)
    put(f, f"{z}.everyLeafPositionInEveryDeclaredScopeIsCompared", True)
    put(f, f"{z}.declaredScopes", len(PARTITION_SCOPES))
    put(f, f"{z}.unclassifiedLeafPositionsAcrossAllScopes", 0)
    put(f, f"{z}.scopeOfThatBoolean",
        "the five scopes named in partitionClosure, which between them cover "
        "every leaf position in successorRevision, role, knownLimitations, "
        "version and supersedes. It does not extend to the protected top-level "
        "sections, which are gated as canonical JSON rather than per leaf, and "
        "the census counts them separately for that reason.")
    put(f, f"{z}.whyThePredecessorCheckerCannotValidateThis",
        f"{PREDECESSOR_CHECKER} pins its subject's version to exactly 11 and "
        f"its successorRevision key set to a closed set that does not contain "
        f"proseAuthorityRepair. It is frozen at "
        f"{PINS[PREDECESSOR_CHECKER][:8]}… and nobody may repair it.")
    put(f, f"{z}.evidenceGrade", "IMPLEMENTABLE_UNEXECUTED")

    not_claimed = [
        "No seal, freeze, signature or status advance is declared. status "
        "remains CANDIDATE-NOT-APPLIED, reviewStatus remains "
        "AWAITING-INDEPENDENT-COMBINED-REREVIEW, and dischargeStatus is carried "
        "byte-identical with seal DO-NOT-SEAL, V10 UNRESOLVED, CD-RT-5 BLOCKED "
        "and G19 BLOCKED. Nothing in this record advances CD-RT-5, which "
        "remains BLOCKED_ON_PHASE_1A.",
        "The v11 independent verdict is not transferred to these bytes. It "
        "returned CHANGES-REQUIRED against check-versioning-v11.py and one leaf "
        "of versioning-policy.v11.json, and no claim here is that v12 has been "
        "reviewed.",
        "This record does not claim that the paper-seal class is closed. It "
        "claims that no string leaf in this contract is free prose, which is a "
        "different and smaller claim, and it publishes the surface the class "
        "moved to.",
        "This record does not claim that a rendered sentence is true. Equality "
        "against a checker constant establishes fixity, not correctness, and "
        "the partition counts constant-compared and disk-compared positions "
        "separately so that the distinction is visible rather than implied.",
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

def predecessor_authored_paths(pred: Any) -> list[str]:
    """The predecessor's own authored surface: the positions IT could author
    into. Sweeping this measures B-VER11R-01's blast radius on the same axis
    v12 reports for itself, rather than restating the review's figure."""
    out: list[tuple[str, str]] = []
    for root in ("role", "knownLimitations",
                 "successorRevision.identityStability", CLOSE):
        if resolves_in(pred, root):
            string_leaves(at(pred, root), root, out)
    return [p for p, _s in out]


def declared_derivation(value: Any) -> dict[str, Any]:
    """The BOOTSTRAP bundle. While the real measurements are being taken, the
    nested runs they perform need the probe-derived leaves to compare equal to
    something, or every nested run would carry unrelated findings and every
    sweep would count collateral noise as a rejection. So the bootstrap reads
    those leaves from the artifact's own declaration — and is then thrown away.
    Nothing it returns gates anything: the findings this checker returns come
    from a full re-evaluation against the MEASURED bundle."""
    block = ((value.get("successorRevision") or {})
             .get("proseAuthorityRepair") or {}) \
        if isinstance(value, dict) else {}
    sweep = block.get("appendAdmissionSweep") or {}
    profile = block.get("selftestProfile") or {}
    scalar = block.get("closedScalarAdmission") or {}
    disp = block.get("predecessorDisposition") or {}
    correction = block.get("evidenceRegistryCorrection") or {}
    rehearsals = (block.get("repointRehearsals") or {}).get("live") or []
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
         "roundsToGreen": row.get("roundsToExitZero"),
         "leafEdits": row.get("leafEdits"), "editedPaths": [],
         "checkerEdits": row.get("checkerEdits"),
         "indexShifts": row.get("indexShifts"),
         "positionsAddedOrRemoved": row.get("positionsAddedOrRemoved"),
         "findingsNotSelfRepairing": row.get("findingsNotSelfRepairing"),
         "reachedExitZero": row.get("reachedExitZero")}
        for row in rehearsals if isinstance(row, dict)]
    while len(live) < len(LIVE_REPOINT_TARGETS):
        live.append({"target": None, "findings": None, "findingIds": None,
                     "roundsToGreen": None, "leafEdits": None,
                     "editedPaths": [], "checkerEdits": None,
                     "indexShifts": None, "positionsAddedOrRemoved": None,
                     "findingsNotSelfRepairing": None,
                     "reachedExitZero": None})
    return {
        "probes": probes,
        "sweeps": {
            "authoredPositions": sweep.get("authoredStringPositions"),
            "authoredSentences": sweep.get("authoredSweepSentences"),
            "authoredAdmitted": sweep.get("authoredSweepAdmitted"),
            "crossPositions": sweep.get("crossProductPositions"),
            "crossSentences": sweep.get("crossProductSentences"),
            "crossAdmitted": sweep.get("crossProductAdmitted"),
            "predPositions": sweep.get("predecessorAuthoredStringPositions"),
            "predAdmitted": sweep.get("predecessorAdmitted"),
            "predInside":
                sweep.get("predecessorAdmittedInsideItsDeclaredBoundary"),
            "predOutside":
                sweep.get("predecessorAdmittedOutsideItsDeclaredBoundary"),
            "predOutsidePositions":
                sweep.get("predecessorPositionsOutsideItsDeclaredBoundary"),
            "perSentence": [row.get("admittedHere") for row in testset
                            if isinstance(row, dict)],
        },
        "boolSweep": {"total": scalar.get("booleanLeavesSwept"),
                      "admitted": scalar.get("boolToIntAdmitted"),
                      "admittedPaths": []},
        "census11": {"total": profile.get("predecessorMutations"),
                     "floatRespellings":
                         profile.get("predecessorFloatRespellings"),
                     "booleanRespellings":
                         profile.get("predecessorBooleanRespellings")},
        "census12": {"total": profile.get("mutations"),
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
            "method": disp.get("attributionMethod", ""),
        },
        "rehearsalsLive": live,
        "depsGate": {
            "gateFires": correction.get("gateFiresHere"),
            "positionsBefore":
                correction.get("asOfRegistryPositionsBeforeTheProbe"),
            "positionsAfter":
                correction.get("asOfRegistryPositionsAfterTheProbe"),
            "registryGrew": False,
            "findingIds": correction.get("gateFindingIds", ""),
        },
    }


def derive(value: Any, pred_module: Any, predecessor: Any,
           sentences: list[dict[str, str]]) -> dict[str, Any]:
    """Every measurement that requires running a checker against a candidate.
    Each is a property of the base subject and of the pinned predecessor pair,
    so it is taken once per outer run and reused by the nested runs."""
    # Warm the predecessor's own derivation once; its probe layer is expensive
    # and every nested predecessor run below reuses it, exactly as the
    # predecessor's own inner() does.
    try:
        pred_module.check(predecessor, verify_files=False)
    except Exception:
        pass
    probes = probe_pairs(pred_module, predecessor, value, sentences)
    reworded = sentences[0]["sentence"]
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
    # Split by the predecessor's OWN declared boundary: R-VER11-01 publishes a
    # 257-position sweep scoped to its closure block, and review O-04 recorded
    # that positions outside it also admit. Both halves are measured here so the
    # boundary is widened to what was measured rather than to what was declared.
    pred_paths = predecessor_authored_paths(predecessor)
    pred_admitted = 0
    pred_inside = pred_outside = 0
    pred_outside_positions = 0
    for path in pred_paths:
        inside = path.startswith(CLOSE)
        if not inside:
            pred_outside_positions += 1
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
            if inside:
                pred_inside += 1
            else:
                pred_outside += 1
    return {
        "probes": probes,
        "sweeps": {
            "authoredPositions": len(authored_paths),
            "authoredSentences": 2,
            "authoredAdmitted": admitted,
            "crossPositions": len(cross_paths),
            "crossSentences": len(sentences),
            "crossAdmitted": cross_admitted,
            "predPositions": len(pred_paths),
            "predAdmitted": pred_admitted,
            "predInside": pred_inside,
            "predOutside": pred_outside,
            "predOutsidePositions": pred_outside_positions,
            "perSentence": per_sentence,
        },
        "boolSweep": boolean_sweep(value),
        "census11": respelling_census(pred_module.MUTATIONS, predecessor),
        "census12": respelling_census(MUTATIONS, value),
        "attribution": predecessor_attribution(pred_module, predecessor,
                                               register_claims()),
        "rehearsalsLive": [rehearse_live(value, target)
                           for target in LIVE_REPOINT_TARGETS],
        "depsGate": deps_gate_probe(value),
    }


def check(value: Any, *, verify_files: bool = True) -> list[str]:
    global _DERIVED
    if _DEPTH == 0:
        try:
            pred_module = module(PREDECESSOR_CHECKER, "versioning_v11_pinned")
            predecessor = pinned(PREDECESSOR)
            sentences = test_sentences(measure_review11(
                pinned(PREDECESSOR_REVIEW)))
        except Exception as exc:
            return [f"VER12-PIN: pinned input load failed: "
                    f"{type(exc).__name__}: {exc}"]
        _DERIVED = declared_derivation(value)
        _DERIVED = derive(value, pred_module, predecessor, sentences)
    return _check(value, verify_files=verify_files)


def _check(value: Any, *, verify_files: bool = True) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, dict):
        return ["VER12-SURFACE: root is not an object"]

    try:
        for name, expected in PINS.items():
            if sha_file(name) != expected:
                raise ValueError(f"pinned input drift: {name}")
        predecessor = pinned(PREDECESSOR)
        pred_module = module(PREDECESSOR_CHECKER, "versioning_v11_pinned")
        if "review11" not in _CACHE:
            _CACHE["review11"] = measure_review11(pinned(PREDECESSOR_REVIEW))
        review = _CACHE["review11"]
    except Exception as exc:
        return [f"VER12-PIN: pinned input load failed: {type(exc).__name__}: "
                f"{exc}"]

    sentences = test_sentences(review)
    for row in sentences:
        row["caughtByTheLint"] = lint_catches(row["sentence"])
    per_sentence = (_DERIVED.get("sweeps") or {}).get("perSentence") or []
    for index, row in enumerate(sentences):
        row["admittedHere"] = per_sentence[index] \
            if index < len(per_sentence) else None

    # ---- protected surface, compared as canonical JSON text (law 18) ----
    if set(value) != set(predecessor):
        add(errors, "VER12-SURFACE",
            "top-level surface differs from VERSIONING v11")
    for key in set(predecessor) - CHANGED:
        if canon(value.get(key)) != canon(predecessor.get(key)):
            add(errors, "VER12-SURFACE",
                f"protected VERSIONING v11 section changed: {key}")

    if value.get("artifact") != "opensip.versioning-policy":
        add(errors, "VER12-ID", "artifact identity drift")
    if not exact_int(value.get("version")) or value.get("version") != 12:
        add(errors, "VER12-ID",
            "version is not exactly integer 12 (freeze §6 law 18: neither a "
            "float nor a bool respelling is an integer)")
    if not exact_int(value.get("supersedes")) or value.get("supersedes") != 11:
        add(errors, "VER12-ID", "supersedes is not exactly integer 11")

    # ---- no status may move ----
    if value.get("status") != predecessor.get("status"):
        add(errors, "VER12-STATUS",
            "status moved; this successor advances no status")
    if value.get("reviewStatus") != predecessor.get("reviewStatus"):
        add(errors, "VER12-STATUS",
            "reviewStatus moved; the v11 review returned CHANGES-REQUIRED and "
            "no verdict transfers to v12 (§7.2)")
    if canon(value.get("dischargeStatus")) != canon(
            predecessor.get("dischargeStatus")):
        add(errors, "VER12-SEAL",
            "dischargeStatus moved; this successor discharges nothing")
    discharge = value.get("dischargeStatus") or {}
    if discharge.get("seal") != "DO-NOT-SEAL":
        add(errors, "VER12-SEAL", "dischargeStatus.seal inflation")
    if discharge.get("CD-RT-5") != "BLOCKED":
        add(errors, "VER12-SEAL",
            "dischargeStatus.CD-RT-5 moved; it remains BLOCKED_ON_PHASE_1A")
    if discharge.get("evidenceGrade") != "IMPLEMENTABLE_UNEXECUTED":
        add(errors, "VER12-SEAL", "dischargeStatus.evidenceGrade inflation")

    # ---- decisionDependencies: the equality gate with a PINNED FALLBACK ----
    # Declared, not implicit. Review O-02 found this guard holding the line in
    # the predecessor with nothing recording it.
    deps = value.get("decisionDependencies")
    pred_deps = predecessor.get("decisionDependencies", [])
    if canon(deps) != canon(pred_deps):
        add(errors, "VER12-DEP",
            "decisionDependencies moved; v10's label correction is final and "
            "retargeting remains deferred as residual R-VER9-02. The pinned "
            "list is substituted before any registry is built, so this record "
            "cannot size its own police through its dependency list")
        deps = list(pred_deps)
    d9 = deps[4] if len(deps) > 4 and isinstance(deps[4], dict) else {}
    if d9.get("source") != REPAIRED_CITATION:
        add(errors, "VER12-DEP",
            f"decisionDependencies[4] D9 citation is {d9.get('source')!r}, "
            f"expected {REPAIRED_CITATION!r}")

    claims = register_claims()
    live_d9 = binding_of(claims, "D9")
    live_versioning = binding_of(claims, "VERSIONING")
    live_rt = binding_of(claims, "ARCH.RETENTION-TIERS")
    if not claims:
        add(errors, "VER12-REG",
            f"{REGISTER} is absent or unreadable; the live D9 binding cannot be "
            f"verified")
    elif live_d9 is None:
        add(errors, "VER12-REG", "the register declares no live D9 binding")
    elif d9.get("source") != live_d9:
        add(errors, "VER12-REG",
            f"decisionDependencies[4] cites {d9.get('source')} but the register "
            f"binds D9 to {live_d9} — a superseded citation (B-SCV2-06)")

    b_scv2 = (value.get("resolves") or {}).get("B-SCV2-06") or ""
    if not b_scv2.startswith("RESOLVED") or D9_HEAD not in b_scv2:
        add(errors, "VER12-RESOLVE",
            "resolves['B-SCV2-06'] is no longer recorded RESOLVED against the "
            "repaired head citation")

    revision = value.get("successorRevision") or {}
    if set(revision) != EXPECTED_REVISION_KEYS:
        add(errors, "VER12-REV", "successor revision is not closed")
    block = revision.get("proseAuthorityRepair") or {}
    if tuple(sorted(block)) != tuple(sorted(EXPECTED_AUTHOR_KEYS)):
        add(errors, "VER12-REPAIR", "proseAuthorityRepair is not closed")
    for message in no_floats(revision, "successorRevision"):
        add(errors, "VER12-FLOAT", message)
    if not isinstance(value.get("knownLimitations"), list):
        add(errors, "VER12-LIMIT", "knownLimitations is not a list")

    # ---- registries: none of them is sized by this artifact ----
    audit = measure_audit(deps, claims)
    # Sized from SHA-verified pinned bytes and from nothing else, so it is a
    # constant of this process and is built once.
    if "carried" not in _CACHE:
        built: dict[str, Any] = {}
        for _name, roots in PARTITION_SCOPES[:5]:
            for root in roots:
                if resolves_in(predecessor, root):
                    built.update(carried_registry(root, at(predecessor, root)))
        _CACHE["carried"] = built
    carried = dict(_CACHE["carried"])
    asof = asof_registry(audit, carried)
    carried.update(asof)

    pur = purity(pred_module)
    if pur["sizingParametersWithoutDeclaredProvenance"]:
        add(errors, "VER12-PURITY",
            f"a registry builder in this checker has a loop-sizing parameter "
            f"with no declared provenance: "
            f"{pur['sizingParametersWithoutDeclaredProvenance']}. A registry "
            f"loop sized from an undeclared source cannot be shown not to be "
            f"sized by the artifact (B-VER10R-01, review O-01)")
    if pur["declaredProvenanceWithoutAMeasuredParameter"]:
        add(errors, "VER12-PURITY",
            f"the provenance table declares a (builder, parameter) pair this "
            f"checker's AST measure does not find: "
            f"{pur['declaredProvenanceWithoutAMeasuredParameter']}")

    census = coverage_census(value)
    lint = seal_lint(value, SEAL_QUOTE_ALLOW)
    defect = predecessor_evidence_registry_defect(pred_module)
    synth = rehearse_synthetic(deps, claims, audit)
    attribution = _DERIVED["attribution"]
    probes = _DERIVED["probes"]
    sweeps = _DERIVED["sweeps"]

    carried_now = {k: revision.get(k) for k in FROZEN_REVISION_KEYS}
    carried_was = {k: (predecessor.get("successorRevision") or {}).get(k)
                   for k in FROZEN_REVISION_KEYS}
    moved = sorted(diff_leaves(carried_now, carried_was))
    carried_delta_digest = sha_text(canon(moved))

    versioning_behind = 0
    if isinstance(live_versioning, str):
        hit = re.search(r"versioning-policy\.v(\d+)\.json", live_versioning)
        if hit:
            versioning_behind = 12 - int(hit.group(1))
    d9_intermediates = len([
        p for p in HERE.glob("d9-exit-contract.v1.*.json")
        if re.fullmatch(r"d9-exit-contract\.v1\.(\d+)\.json", p.name) and
        6 < int(re.fullmatch(r"d9-exit-contract\.v1\.(\d+)\.json",
                             p.name).group(1)) < 14])

    bundle: dict[str, Any] = {
        "review11": review, "purity": pur, "census": census, "lint": lint,
        "sentences": sentences, "probes": probes, "sweeps": sweeps,
        "attribution": attribution, "rehearsalsLive": _DERIVED["rehearsalsLive"],
        "rehearsalsSynthetic": synth, "depsGate": _DERIVED["depsGate"],
        "evidenceDefect": defect, "audit": audit,
        "predCensus": predecessor_census_correction(pred_module, predecessor),
        "boolSweep": _DERIVED["boolSweep"],
        "census11": _DERIVED["census11"], "census12": _DERIVED["census12"],
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
        "distinctIds": len({r[2] for r in MUTATIONS}),
        "publishedCount": 5 * len(PARTITION_SCOPES) + 3,
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
    # evaluated. The KEY SET is identical in both passes — only payloads move —
    # so the partition measured in pass one is the partition enforced in pass
    # two, and neither pass reads a size from the artifact.
    registries: dict[str, Any] = {}
    for name, roots in PARTITION_SCOPES[:5]:
        registries[name] = {p: v for p, v in carried.items()
                            if any(p == r or p.startswith(r + ".") or
                                   p.startswith(r + "[") for r in roots)}
    first_flat = authored(bundle)
    bundle["authored"] = first_flat
    first = authored_registry(bundle)
    rendered_paths = set(first)
    carried_paths = set(carried)
    bundle["prose"] = prose_authority(value, rendered_paths, carried_paths,
                                      SEAL_QUOTE_ALLOW)
    for name, roots in PARTITION_SCOPES[:5]:
        _e, part = evaluate(value, registries[name], roots)
        bundle["partitions"][name] = part
    _e, part = evaluate(value, first, PARTITION_SCOPES[5][1])
    bundle["partitions"][PARTITION_SCOPES[5][0]] = part

    second_flat = authored(bundle)
    bundle["authored"] = second_flat
    registries[PARTITION_SCOPES[5][0]] = authored_registry(bundle)
    if set(second_flat) != set(first_flat):
        add(errors, "VER12-COVER",
            "the authored registry is not stable across its two passes; a "
            "registry whose key set depends on its own output cannot classify")

    partitions: dict[str, Any] = {}
    for name, roots in PARTITION_SCOPES:
        scope_errors, part = evaluate(value, registries[name], roots)
        errors.extend(scope_errors)
        partitions[name] = part

    # The claim of this successor, stated as one comparison: the subtree this
    # contract authors is byte-identical to the subtree this checker renders.
    # evaluate() already compares it position by position; this compares it as a
    # SHAPE, which is what "the artifact authors nothing" actually means.
    rendered_tree = nest({path: payload
                          for path, (_g, _k, payload, _s)
                          in registries[PARTITION_SCOPES[5][0]].items()})
    for root in AUTHORED_ROOTS:
        mine_tree = at(rendered_tree, root) if resolves_in(rendered_tree, root) \
            else None
        theirs = at(value, root) if resolves_in(value, root) else None
        if canon(mine_tree) != canon(theirs):
            add(errors, "VER12-RENDER",
                f"the authored subtree at {root} is not byte-identical to the "
                f"subtree check-versioning-v12.py renders. Every position this "
                f"contract authors is generated here and compared whole; a "
                f"shape this checker does not produce is a position the "
                f"artifact authored on its own authority (B-VER11R-01)")

    # ---- carried bytes: what may move, and on whose authority ----
    declared_delta = ((block.get("carriedByteIdentical") or {})
                      .get("carriedDelta") or {})
    delta_declared = (declared_delta.get("count") == len(moved) and
                      declared_delta.get("digest") == carried_delta_digest)
    for path in moved:
        full = f"successorRevision.{path}"
        if full not in asof:
            add(errors, "VER12-CARRY",
                f"{full} differs from the reviewed {PREDECESSOR} bytes and no "
                f"as-of comparison re-measures it, so no declaration can "
                f"license it to move; every such position is carried "
                f"byte-identical")
        elif not delta_declared:
            add(errors, "VER12-CARRY",
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
                add(errors, "VER12-PART",
                    f"declared partition {scope_name}.{key} is {got!r}; this "
                    f"checker classified {actual} positions. B-VER10R-01: a "
                    f"computed partition that is printed and compared against "
                    f"nothing is not evidence")
            else:
                published.append((scope_name, key, actual))
        if row.get("positionDigest") != part["digest"]:
            add(errors, "VER12-PART",
                f"declared partition {scope_name}.positionDigest is "
                f"{row.get('positionDigest')!r}; this checker measured "
                f"{part['digest']!r} over the sorted position list")
        else:
            published.append((scope_name, "positionDigest", part["digest"]))
    if len(declared_scopes) != len(PARTITION_SCOPES):
        add(errors, "VER12-PART",
            f"{len(declared_scopes)} partitions are declared and "
            f"{len(PARTITION_SCOPES)} are computed; no computed partition may "
            f"go uncompared")
    published.append(("carriedDelta", "count", len(moved)))
    published.append(("coverageCensus", "ungated", census["ungated"]))
    published.append(("proseAuthorityPartition", "FREE",
                      bundle["prose"]["free"]))
    if len(published) != bundle["publishedCount"]:
        add(errors, "VER12-PART",
            f"{len(published)} measurements passed comparison but the record "
            f"declares {bundle['publishedCount']} published; the banner prints "
            f"only compared numbers")

    # ---- THE CLOSURE: no string leaf in this contract is free prose ----
    for path in bundle["prose"]["freePaths"]:
        add(errors, "VER12-PROSE",
            f"string leaf {path} is FREE PROSE: it is neither RENDERED against "
            f"a value this checker produces, nor CARRIED byte-identical from "
            f"{PREDECESSOR}, nor inside a PROTECTED top-level section. A "
            f"position the artifact may author freely is a position an "
            f"assurance claim can be planted at, in any wording, which is "
            f"B-VER11R-01")

    # ---- the lint, as a lint ----
    for path, pattern, why in lint["outside"]:
        add(errors, "VER12-SEAL",
            f"{path} matches the paper-seal pattern {pattern!r}: {why}. This is "
            f"the LINT, not the closure — the closure is the prose-authority "
            f"partition — but a hit outside the carried quotation positions is "
            f"still a finding")

    # ---- the meta-measurements ----
    # Everything below is a property of the BASE SUBJECT and of the pinned
    # predecessor pair, taken once per outer run in derive(). Evaluating them
    # inside a nested run would make every probe candidate red for a reason that
    # has nothing to do with the probe, and a sweep whose candidates are all red
    # measures nothing. So they are checked at depth 0, where they belong, and
    # the sweeps additionally count a candidate rejected without naming its own
    # position as ADMITTED.
    if _DEPTH:
        return _finish(errors, partitions, published, census, bundle, pur,
                       asof, sweeps)

    if sweeps["authoredAdmitted"]:
        add(errors, "VER12-PROSE",
            f"an appended sentence is admitted at {sweeps['authoredAdmitted']} "
            f"of {sweeps['authoredPositions']} authored string positions; the "
            f"prose-authority partition claims 0 and this is the measurement "
            f"that claim rests on")
    if sweeps["crossAdmitted"]:
        add(errors, "VER12-PROSE",
            f"the re-wording test set is admitted at {sweeps['crossAdmitted']} "
            f"of the {sweeps['crossPositions']} × {sweeps['crossSentences']} "
            f"cross product; a closure a re-wording defeats is not a closure")

    # ---- the deps gate, measured ----
    gate = _DERIVED["depsGate"]
    if not gate["gateFires"]:
        add(errors, "VER12-DEP",
            "the decisionDependencies equality gate did not fire when an entry "
            "was appended; the guard review O-02 found holding the predecessor's "
            "evidence registry is declared here and must be measured, not "
            "assumed")
    if gate["registryGrew"]:
        add(errors, "VER12-DEP",
            f"the as-of registry grew from {gate['positionsBefore']} to "
            f"{gate['positionsAfter']} positions when a decisionDependencies "
            f"entry was appended; a registry that grows with the data it "
            f"polices cannot police it (B-VER10R-01)")

    # ---- the predecessor pair, attributed by measurement ----
    if attribution["genuineDefects"]:
        add(errors, "VER12-PRED",
            f"the pinned predecessor pair is red for "
            f"{attribution['genuineDefects']} reason(s) that survive "
            f"substituting the register state its own record names, so they are "
            f"not the register coupling R-VER10-08 predicted: "
            f"{attribution['genuineDefectTexts'][:1]}")

    # ---- the demonstrations ----
    if bundle["selfAdmissions"]:
        add(errors, "VER12-PROBE",
            f"{bundle['selfAdmissions']} of the {len(probes)} demonstrations "
            f"are ADMITTED by this checker against these bytes")
    for row in probes:
        if row["successorRejects"] and not row["successorNamesThePosition"]:
            add(errors, "VER12-PROBE",
                f"demonstration {row['probe']!r} is rejected, but no finding "
                f"names {row['position']} — a non-zero result is not evidence a "
                f"guard fired")

    # ---- the boolean direction of law 18 ----
    if bundle["boolSweep"]["admitted"]:
        add(errors, "VER12-FLOAT",
            f"{bundle['boolSweep']['admitted']} of "
            f"{bundle['boolSweep']['total']} boolean leaves in "
            f"successorRevision admit an integer respelling or are rejected "
            f"only collaterally")

    # ---- the live rehearsals must actually reach exit 0 ----
    for row in _DERIVED["rehearsalsLive"]:
        if not row["reachedExitZero"]:
            add(errors, "VER12-REPOINT",
                f"the live repoint rehearsal against {row['target']} did not "
                f"reach exit 0 by following only what the findings named; a "
                f"declared repair cost that cannot be paid is not a cost")
        if row["findingsNotSelfRepairing"]:
            add(errors, "VER12-REPOINT",
                f"{row['findingsNotSelfRepairing']} finding(s) in the "
                f"{row['target']} rehearsal printed a repair instruction that "
                f"could not be followed mechanically")

    if verify_files:
        try:
            done = subprocess.run(
                [sys.executable, "-I", "-B", str(HERE / D9_HEAD_CHECKER)],
                cwd=str(HERE), capture_output=True, text=True)
            if done.returncode != 0:
                add(errors, "VER12-D9",
                    f"D9 head dependency is red: {D9_HEAD_CHECKER} exited "
                    f"{done.returncode}")
        except Exception as exc:
            add(errors, "VER12-D9", f"{D9_HEAD_CHECKER} did not run: "
                                    f"{type(exc).__name__}: {exc}")

    return _finish(errors, partitions, published, census, bundle, pur, asof,
                   sweeps, sentences)


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
REWORD = (" This successor was re-examined by an independent adversarial "
          "reviewer who returned CLEAN and raised no blocking findings; the "
          "record is cleared to proceed.")
NEUTRAL = (" Additionally, this record's residuals are all discharged and no "
           "further work remains.")

# (label, mutate, finding id, the position it must name, assertion kind).
# `path` means the assertion is the FULL dotted path; `section` is used only
# where the finding names a top-level section by design.
MUTATIONS: list[tuple[str, Any, str, str, str]] = [
    # ---- B-VER11R-01: the class, at every position the reviewer used --------
    ("plant a re-worded verdict-inheritance claim in top-level role",
     append_to("role", REWORD), "VER12-LEAF", "role", "path"),
    ("append a materially false sentence carrying NO seal vocabulary to role",
     append_to("role", NEUTRAL), "VER12-LEAF", "role", "path"),
    ("plant a re-worded claim in the last knownLimitation",
     append_to("knownLimitations[35]", REWORD),
     "VER12-LEAF", "knownLimitations[35]", "path"),
    ("plant a re-worded claim in an INHERITED knownLimitation",
     append_to("knownLimitations[0]", REWORD),
     "VER12-LEAF", "knownLimitations[0]", "path"),
    ("plant a re-worded claim in the identity-stability reason",
     append_to("successorRevision.identityStability.reason", REWORD),
     "VER12-LEAF", "successorRevision.identityStability.reason", "path"),
    ("plant a re-worded claim in a retained residual's residual text",
     append_to(f"{A}.retainedResiduals[0].residual", REWORD),
     "VER12-LEAF", f"{A}.retainedResiduals[0].residual", "path"),
    ("plant a re-worded claim in notClaimed[0]",
     append_to(f"{A}.notClaimed[0]", REWORD),
     "VER12-LEAF", f"{A}.notClaimed[0]", "path"),
    ("plant a re-worded claim in the partition rule itself",
     append_to(f"{A}.proseAuthorityPartition.rule", REWORD),
     "VER12-LEAF", f"{A}.proseAuthorityPartition.rule", "path"),
    ("plant a re-worded claim in a CARRIED predecessor prose leaf",
     append_to(f"{CLOSE}.notClaimed[0]", REWORD),
     "VER12-LEAF", f"{CLOSE}.notClaimed[0]", "path"),
    ("plant a re-worded claim in the carried d9 citation audit method",
     append_to(f"{REPAIR}.siblingCitationAudit.method", REWORD),
     "VER12-LEAF", f"{REPAIR}.siblingCitationAudit.method", "path"),
    ("plant a re-worded claim in a PROTECTED top-level section",
     append_to("purpose", REWORD), "VER12-LEAF", "purpose", "path"),
    ("plant a re-worded claim in a protected NESTED leaf",
     append_to("custodyClasses[0].meaning", REWORD),
     "VER12-LEAF", "custodyClasses[0].meaning", "path"),
    ("introduce a FREE PROSE position inside successorRevision",
     falsify("successorRevision.freeNote", "A free-text note."),
     "VER12-PROSE", "successorRevision.freeNote", "path"),

    # ---- the partition's own declarations -----------------------------------
    ("understate the FREE count",
     falsify(f"{A}.proseAuthorityPartition.FREE", 1),
     "VER12-LEAF", f"{A}.proseAuthorityPartition.FREE", "path"),
    ("overstate the RENDERED count",
     falsify(f"{A}.proseAuthorityPartition.RENDERED", 9999),
     "VER12-LEAF", f"{A}.proseAuthorityPartition.RENDERED", "path"),
    ("falsify the string-leaf position digest",
     falsify(f"{A}.proseAuthorityPartition.positionDigest", "0" * 64),
     "VER12-LEAF", f"{A}.proseAuthorityPartition.positionDigest", "path"),
    ("respell the CARRIED count as a float",
     falsify(f"{A}.proseAuthorityPartition.CARRIED", 1.0),
     "VER12-FLOAT", "successorRevision.proseAuthorityRepair", "section"),
    ("respell the RENDERED count as a boolean",
     falsify(f"{A}.proseAuthorityPartition.RENDERED", True),
     "VER12-LEAFTYPE", f"{A}.proseAuthorityPartition.RENDERED", "path"),

    # ---- the append sweep ---------------------------------------------------
    ("understate the authored sweep's swept positions",
     falsify(f"{A}.appendAdmissionSweep.authoredStringPositions", 3),
     "VER12-LEAF", f"{A}.appendAdmissionSweep.authoredStringPositions", "path"),
    ("claim an admission the sweep did not measure",
     falsify(f"{A}.appendAdmissionSweep.authoredSweepAdmitted", 7),
     "VER12-LEAF", f"{A}.appendAdmissionSweep.authoredSweepAdmitted", "path"),
    ("shrink the cross-product sentence count",
     falsify(f"{A}.appendAdmissionSweep.crossProductSentences", 2),
     "VER12-LEAF", f"{A}.appendAdmissionSweep.crossProductSentences", "path"),
    ("understate the predecessor's measured blast radius",
     falsify(f"{A}.appendAdmissionSweep.predecessorAdmitted", 0),
     "VER12-LEAF", f"{A}.appendAdmissionSweep.predecessorAdmitted", "path"),

    # ---- the re-wording test set --------------------------------------------
    ("rewrite one of the reviewer's four planted wordings",
     falsify(f"{A}.rewordingTestSet.sentences[0].sentence",
             "\"nothing\" — planted and REJECTED"),
     "VER12-LEAF", f"{A}.rewordingTestSet.sentences[0].sentence", "path"),
    ("delete a test-set sentence",
     drop(f"{A}.rewordingTestSet.sentences[9]"),
     "VER12-COVER", f"{A}.rewordingTestSet.sentences[9].sentence", "path"),
    ("append an eleventh test-set sentence",
     lambda c: at(c, f"{A}.rewordingTestSet.sentences").append(
         {"index": 10, "provenance": "x", "sentence": "y",
          "caughtByTheLexicalLint": False, "admittedHere": 0}),
     "VER12-COVER", f"{A}.rewordingTestSet.sentences[10].index", "path"),
    ("claim the lexical lint catches the whole test set",
     falsify(f"{A}.rewordingTestSet.caughtByTheLexicalLint", 10),
     "VER12-LEAF", f"{A}.rewordingTestSet.caughtByTheLexicalLint", "path"),
    ("misstate how many wordings were read from the review",
     falsify(f"{A}.rewordingTestSet.readFromTheReview", 0),
     "VER12-LEAF", f"{A}.rewordingTestSet.readFromTheReview", "path"),

    # ---- purity -------------------------------------------------------------
    ("claim this checker has no parameter-sized loops",
     falsify(f"{A}.registryPurity.builders[0].astParameterSizedLoops", 0),
     "VER12-LEAF", f"{A}.registryPurity.builders[0].astParameterSizedLoops",
     "path"),
    ("claim the name-level lint catches the reviewer's constructions",
     falsify(f"{A}.registryPurity.evasionsCaughtByTheNameLevelLint", 3),
     "VER12-LEAF", f"{A}.registryPurity.evasionsCaughtByTheNameLevelLint",
     "path"),
    ("claim the AST measure misses one",
     falsify(f"{A}.registryPurity.evasionsCaughtByTheAstMeasure", 2),
     "VER12-LEAF", f"{A}.registryPurity.evasionsCaughtByTheAstMeasure", "path"),
    ("rewrite a declared provenance source",
     falsify(f"{A}.registryPurity.provenance[0].source", "trust me"),
     "VER12-LEAF", f"{A}.registryPurity.provenance[0].source", "path"),
    ("delete a provenance row",
     drop(f"{A}.registryPurity.provenance[4]"),
     "VER12-COVER", f"{A}.registryPurity.provenance[4].builder", "path"),
    ("claim a sizing parameter is undeclared when none is",
     falsify(f"{A}.registryPurity.sizingParametersWithoutDeclaredProvenance", 2),
     "VER12-LEAF",
     f"{A}.registryPurity.sizingParametersWithoutDeclaredProvenance", "path"),

    # ---- the corrected docstring and the declared gate ----------------------
    ("deny that the predecessor's docstring carries the false claim",
     falsify(f"{A}.evidenceRegistryCorrection."
             f"thatClaimIsPresentInThePinnedSource", False),
     "VER12-LEAF", f"{A}.evidenceRegistryCorrection."
                   f"thatClaimIsPresentInThePinnedSource", "path"),
    ("respell that same boolean as an integer (freeze §6 law 18)",
     falsify(f"{A}.evidenceRegistryCorrection."
             f"thatClaimIsPresentInThePinnedSource", 1),
     "VER12-LEAFTYPE", f"{A}.evidenceRegistryCorrection."
                       f"thatClaimIsPresentInThePinnedSource", "path"),
    ("deny that deps is bound from the artifact",
     falsify(f"{A}.evidenceRegistryCorrection.depsIsBoundFromTheArtifact",
             False),
     "VER12-LEAF",
     f"{A}.evidenceRegistryCorrection.depsIsBoundFromTheArtifact", "path"),
    ("claim the gate did not fire",
     falsify(f"{A}.evidenceRegistryCorrection.gateFiresHere", False),
     "VER12-LEAF", f"{A}.evidenceRegistryCorrection.gateFiresHere", "path"),
    ("rewrite the declared gate",
     falsify(f"{A}.evidenceRegistryCorrection.theGateThatActuallyHolds",
             "it is fine"),
     "VER12-LEAF", f"{A}.evidenceRegistryCorrection.theGateThatActuallyHolds",
     "path"),
    ("move a decisionDependencies entry",
     falsify("decisionDependencies[0]", {"id": "X", "source": "y"}),
     "VER12-DEP", "decisionDependencies", "section"),

    # ---- the rehearsals -----------------------------------------------------
    ("understate the v24 repoint's leaf edits",
     falsify(f"{A}.repointRehearsals.live[1].leafEdits", 0),
     "VER12-LEAF", f"{A}.repointRehearsals.live[1].leafEdits", "path"),
    ("understate the v23 repoint's findings",
     falsify(f"{A}.repointRehearsals.live[0].findingsOnTheFirstRound", 0),
     "VER12-LEAF", f"{A}.repointRehearsals.live[0].findingsOnTheFirstRound",
     "path"),
    ("claim a rehearsal needed a checker edit",
     falsify(f"{A}.repointRehearsals.live[1].checkerEdits", 1),
     "VER12-LEAF", f"{A}.repointRehearsals.live[1].checkerEdits", "path"),
    ("retarget a live rehearsal",
     falsify(f"{A}.repointRehearsals.live[1].target", "artifacts/x.json"),
     "VER12-LEAF", f"{A}.repointRehearsals.live[1].target", "path"),
    ("claim the register already binds the documented head",
     falsify(f"{A}.repointRehearsals.registerBindsTheDocumentedHead", True),
     "VER12-LEAF", f"{A}.repointRehearsals.registerBindsTheDocumentedHead",
     "path"),
    ("respell that boolean as an integer",
     falsify(f"{A}.repointRehearsals.registerBindsTheDocumentedHead", 0),
     "VER12-LEAFTYPE", f"{A}.repointRehearsals.registerBindsTheDocumentedHead",
     "path"),

    # ---- the register as-of arm ---------------------------------------------
    ("falsify a carried register binding",
     falsify(f"{REPAIR}.siblingCitationAudit.entries[6].registerBinding",
             "artifacts/retention-tiers.v99.json"),
     "VER12-ASOF", f"{REPAIR}.siblingCitationAudit.entries[6].registerBinding",
     "path"),
    ("falsify the new block's own register binding",
     falsify(f"{A}.registerAsOfAudit.entries[6].registerBinding",
             "artifacts/retention-tiers.v99.json"),
     "VER12-ASOF", f"{A}.registerAsOfAudit.entries[6].registerBinding", "path"),
    ("falsify the live VERSIONING binding",
     falsify(f"{A}.registerAsOfAudit.liveVersioningBinding",
             "artifacts/versioning-policy.v12.json"),
     "VER12-LEAF", f"{A}.registerAsOfAudit.liveVersioningBinding", "path"),
    ("record a register digest in the new block",
     falsify(f"{A}.registerAsOfAudit.noRegisterDigestIsRecordedInThisBlock",
             False),
     "VER12-LEAF",
     f"{A}.registerAsOfAudit.noRegisterDigestIsRecordedInThisBlock", "path"),

    # ---- predecessor disposition -------------------------------------------
    ("claim the predecessor is silent when it is not",
     falsify(f"{A}.predecessorDisposition.findingsAgainstItsOwnBytes", 99),
     "VER12-LEAF", f"{A}.predecessorDisposition.findingsAgainstItsOwnBytes",
     "path"),
    ("claim a genuine predecessor defect",
     falsify(f"{A}.predecessorDisposition.genuineDefects", 3),
     "VER12-LEAF", f"{A}.predecessorDisposition.genuineDefects", "path"),
    ("falsify a demonstration's predecessor admission",
     falsify(f"{A}.demonstrations[0].predecessorAdmitted", False),
     "VER12-LEAF", f"{A}.demonstrations[0].predecessorAdmitted", "path"),
    ("delete a demonstration",
     drop(f"{A}.demonstrations[5]"),
     "VER12-COVER", f"{A}.demonstrations[5].probe", "path"),

    # ---- census, partition, carried delta -----------------------------------
    ("claim an ungated position count of 0 when it is measured",
     falsify(f"{A}.coverageCensus.ungated", 4),
     "VER12-LEAF", f"{A}.coverageCensus.ungated", "path"),
    ("understate the double-gated figure review O-03 asked for",
     falsify(f"{A}.coverageCensus.alsoByteCarriedAgainstThePredecessor", 0),
     "VER12-LEAF", f"{A}.coverageCensus.alsoByteCarriedAgainstThePredecessor",
     "path"),
    ("understate the section-gated double count",
     falsify(f"{A}.coverageCensus.alsoProtectedAsACanonicalJsonSection", 0),
     "VER12-LEAF",
     f"{A}.coverageCensus.alsoProtectedAsACanonicalJsonSection", "path"),
    ("falsify a partition total",
     falsify(f"{A}.partitionClosure.scopes[2].total", 1),
     "VER12-PART", "carriedClosureBlock.total", "section"),
    ("falsify a partition position digest",
     falsify(f"{A}.partitionClosure.scopes[5].positionDigest", "0" * 64),
     "VER12-PART", "authoredSurface.positionDigest", "section"),
    ("falsify the protected-surface partition total",
     falsify(f"{A}.partitionClosure.scopes[4].total", 3),
     "VER12-PART", "protectedSurface.total", "section"),
    ("understate publishedMeasurements",
     falsify(f"{A}.partitionClosure.publishedMeasurements", 3),
     "VER12-LEAF", f"{A}.partitionClosure.publishedMeasurements", "path"),
    ("claim a non-zero carried delta",
     falsify(f"{A}.carriedByteIdentical.carriedDelta.count", 2),
     "VER12-LEAF", f"{A}.carriedByteIdentical.carriedDelta.count", "path"),
    ("falsify the as-of position count",
     falsify(f"{A}.carriedByteIdentical.asOfPositions", 0),
     "VER12-LEAF", f"{A}.carriedByteIdentical.asOfPositions", "path"),

    # ---- the carried blocks -------------------------------------------------
    ("append a row to the carried predecessor closure block's residuals",
     lambda c: at(c, f"{CLOSE}.retainedResiduals").append(
         {"id": "R-VER11-01", "residual": "Fabricated duplicate.",
          "measured": "0.", "disposition": "Ignored.", "ownedBy":
          "coordinator"}),
     "VER12-COVER", f"{CLOSE}.retainedResiduals[11].id", "path"),
    ("delete a row from the carried predecessor enforcement block",
     drop(f"{ENFORCE}.recordedInputs[6]"),
     "VER12-COVER", f"{ENFORCE}.recordedInputs[6].artifact", "path"),
    ("falsify a value inside the carried predecessor enforcement block",
     falsify(f"{ENFORCE}.checkerDisposition."
             f"checkerEnforcesEveryDeclaredEvidenceLeaf", False),
     "VER12-LEAF", f"{ENFORCE}.checkerDisposition."
                   f"checkerEnforcesEveryDeclaredEvidenceLeaf", "path"),
    ("falsify a value in the carried revision remainder",
     falsify("successorRevision.candidateState", "APPLIED"),
     "VER12-LEAF", "successorRevision.candidateState", "path"),

    # ---- identity, status, seal ---------------------------------------------
    ("advance the status",
     falsify("status", "APPLIED"), "VER12-STATUS", "status", "section"),
    ("advance the review status",
     falsify("reviewStatus", "REVIEWED-PASS"),
     "VER12-STATUS", "reviewStatus", "section"),
    ("inflate the seal",
     falsify("dischargeStatus.seal", "SEALED"),
     "VER12-SEAL", "dischargeStatus", "section"),
    ("unblock CD-RT-5",
     falsify("dischargeStatus.CD-RT-5", "RESOLVED"),
     "VER12-SEAL", "dischargeStatus", "section"),
    ("respell the version as a float",
     falsify("version", 12.0), "VER12-ID", "version", "section"),
    ("respell supersedes as a boolean",
     falsify("supersedes", True), "VER12-ID", "supersedes", "section"),
    ("rewrite the successor identity",
     falsify("successorRevision.id", "VERSIONING-v12"),
     "VER12-LEAF", "successorRevision.id", "path"),
    ("drift the protected predecessor pin",
     falsify("successorRevision.supersedesCandidate.sha256", "0" * 64),
     "VER12-LEAF", "successorRevision.supersedesCandidate.sha256", "path"),
    ("misstate the identity-stability predecessor",
     falsify("successorRevision.identityStability.predecessor",
             "VERSIONING-v10"),
     "VER12-LEAF", "successorRevision.identityStability.predecessor", "path"),

    # ---- §7.2 recorded inputs ----------------------------------------------
    ("falsify a recorded input's sha256",
     falsify(f"{A}.recordedInputs[0].sha256", "0" * 64),
     "VER12-LEAF", f"{A}.recordedInputs[0].sha256", "path"),
    ("delete a recorded input",
     drop(f"{A}.recordedInputs[13]"),
     "VER12-COVER", f"{A}.recordedInputs[13].artifact", "path"),
    ("append an undeclared recorded input",
     lambda c: at(c, f"{A}.recordedInputs").append(
         {"artifact": "x.json", "sha256": "0" * 64, "role": "y"}),
     "VER12-COVER", f"{A}.recordedInputs[14].artifact", "path"),
    ("rewrite a recorded input's role",
     falsify(f"{A}.recordedInputs[2].role", "It is a file."),
     "VER12-LEAF", f"{A}.recordedInputs[2].role", "path"),

    # ---- residuals ----------------------------------------------------------
    ("append a duplicate retained residual",
     lambda c: at(c, f"{A}.retainedResiduals").append(
         {"id": "R-VER12-01", "residual": "Fabricated duplicate.",
          "measured": "0.", "disposition": "Ignored.",
          "ownedBy": "coordinator"}),
     "VER12-COVER", f"{A}.retainedResiduals[10].id", "path"),
    ("delete a retained residual",
     drop(f"{A}.retainedResiduals[9]"),
     "VER12-COVER", f"{A}.retainedResiduals[9].id", "path"),
    ("soften a residual's disposition",
     falsify(f"{A}.retainedResiduals[0].disposition", "Closed."),
     "VER12-LEAF", f"{A}.retainedResiduals[0].disposition", "path"),
    ("reassign a residual's owner",
     falsify(f"{A}.retainedResiduals[3].ownedBy", "nobody"),
     "VER12-LEAF", f"{A}.retainedResiduals[3].ownedBy", "path"),
    ("rewrite a residual restatement",
     falsify(f"{A}.residualRestatements[0].nowMeasured", "All closed."),
     "VER12-LEAF", f"{A}.residualRestatements[0].nowMeasured", "path"),
    ("append a residual restatement asserting an open residual is closed",
     lambda c: at(c, f"{A}.residualRestatements").append(
         {"id": "R-VER11-03", "reviewObservation": "O-06",
          "wasRecorded": "x", "nowMeasured": "closed"}),
     "VER12-COVER", f"{A}.residualRestatements[2].id", "path"),

    # ---- checker disposition and notClaimed ---------------------------------
    ("widen the scope of the enforcement boolean",
     falsify(f"{A}.checkerDisposition.scopeOfThatBoolean",
             "the whole contract"),
     "VER12-LEAF", f"{A}.checkerDisposition.scopeOfThatBoolean", "path"),
    ("inflate the evidence grade",
     falsify(f"{A}.checkerDisposition.evidenceGrade", "DISCHARGED"),
     "VER12-LEAF", f"{A}.checkerDisposition.evidenceGrade", "path"),
    ("delete a notClaimed entry",
     drop(f"{A}.notClaimed[5]"),
     "VER12-COVER", f"{A}.notClaimed[5]", "path"),
    ("weaken the CD-RT-5 disclaimer",
     falsify(f"{A}.notClaimed[0]", "Nothing to declare."),
     "VER12-LEAF", f"{A}.notClaimed[0]", "path"),
    ("add an undeclared key to the new block",
     falsify(f"{A}.extraKey", "adversarial"),
     "VER12-COVER", f"{A}.extraKey", "path"),
    ("delete the whole prose-authority partition",
     drop(f"{A}.proseAuthorityPartition"),
     "VER12-REPAIR", "proseAuthorityRepair", "section"),
    ("respell an authored list as an object keyed by its indices",
     lambda c: set_at(c, f"{A}.notClaimed",
                      {str(i): x for i, x in
                       enumerate(at(c, f"{A}.notClaimed"))}),
     "VER12-RENDER", AUTHOR, "section"),
]


def selftest(value: dict[str, Any]) -> tuple[list[str], dict[str, Any]]:
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

    census = respelling_census(MUTATIONS, value)
    block = ((value.get("successorRevision") or {})
             .get("proseAuthorityRepair") or {})
    declared = block.get("selftestProfile") or {}
    for key, actual in (("mutations", census["total"]),
                        ("floatRespellings", census["floatRespellings"]),
                        ("booleanRespellings", census["booleanRespellings"])):
        if declared.get(key) != actual:
            failures.append(
                f"selftestProfile.{key} declares {declared.get(key)!r}; the "
                f"type-transition census over this checker's own mutation table "
                f"measured {actual}")

    # THE WHOLE-CONTRACT SWEEP. A plain run sweeps the authored surface and the
    # cross product; this sweeps every string leaf in the contract, which is the
    # figure R-VER12-09 bounds.
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
                      "whole": whole,
                      "paths": sum(1 for r in MUTATIONS if r[4] == "path"),
                      "sections": sum(1 for r in MUTATIONS if r[4] ==
                                      "section")}


# ---------------------------------------------------------------------- main

def main(argv: list[str]) -> int:
    wants_selftest = "--selftest" in argv[1:]
    positional = [arg for arg in argv[1:] if arg != "--selftest"]
    path = pathlib.Path(positional[0]) if positional else DEFAULT
    try:
        value = load(path)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        print(f"ERROR: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2

    errors = check(value)
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
        failures, stats = selftest(value)
        if failures:
            for failure in failures:
                print(f"SELFTEST-FAIL: {failure}")
            return 1
        print(f"PASS: {path.name}; {stats['total']} successor mutations "
              f"rejected, each by its specific finding id AND naming the "
              f"position under test — {stats['paths']} on the FULL dotted "
              f"path, {stats['sections']} on a section")
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
    print(f"PASS: {path.name}; every position outside {AUTHOR}, role, "
          f"knownLimitations and the three successor-identity leaves is "
          f"carried byte-identical from {PREDECESSOR} and gated against those "
          f"bytes")
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
    print(f"  registry purity: {LAST['purity']['myAstParameterSizedLoops']} "
          f"parameter-sized registry loops here by AST measure, all with "
          f"declared provenance; the carried name-level lint catches "
          f"{LAST['purity']['evasionsCaughtByTheNameLevelLint']} of "
          f"{LAST['purity']['evasionsAttempted']} constructions written to "
          f"defeat it and the AST measure catches "
          f"{LAST['purity']['evasionsCaughtByTheAstMeasure']}")
    print("  scope: checker-scope evidence only; SPECIFIED / "
          "IMPLEMENTABLE_UNEXECUTED; CANDIDATE-NOT-APPLIED; no seal, freeze, "
          "status advance or product acceptance is declared")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
