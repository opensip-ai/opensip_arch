#!/usr/bin/env python3
"""Report four different completion questions without conflating them.

  1. Contract-shape completeness: invariants + schema + goldens + checker.
  2. Independent-review completeness: a registered current review exists.
  3. Seal readiness: every registered finding has a final adjudication, no
     claim blocker remains, and the adjudication does not say DO-NOT-SEAL.
  4. Product qualification: live operability DEMONSTRATED release evidence.

SUCCESSOR to `artifacts/check-completeness.py` (predecessor sha256
`6c52a5f9a4ac6a3ec3dae9fb0c87e82552744b18eb8cc38d1c4522ade3e549d6`, measured
2026-08-10).  The predecessor is pinned by 69 `artifacts/*.json` documents and
IMPLEMENTATION-FREEZE.md section 7.2 forbids editing reviewed bytes, so this is
a NEW FILE and nothing under `artifacts/` is altered by its existence.  The
predecessor's derivation reader was independently reviewed at 0 blockers
(`check-completeness.derivation-reader.review-independent.json`); that verdict
stands and is not overturned here.  What is repaired below is a SCOPE defect the
review was never asked about.

WHAT MOVED, AND ONLY THIS (freeze section 7.3 rider, 2026-08-10)

  DEFECT 1 -- ARRAY-FORM OPERATION PATHS WERE UNREADABLE.  The predecessor's
  `is_operation_list()` required `isinstance(item.get("path"), str)`.  Four live
  derivations encode each operation's `path` as an ARRAY OF TOKENS
  (`["version"]`) with a separate non-normative `pathDisplay`.  That encoding is
  a DELIBERATE HARDENING -- an array has no grammar to misparse -- and an
  independent reviewer praised it by name as an anti-`CMP-IR-01` measure.  The
  predecessor did not recognise it, so `declaration_fields()` found 1 name,
  1 digest and ZERO operation lists and returned None.  This file accepts BOTH
  encodings; the array form is the better one and the resolver meets it.

  DEFECT 2 -- THE REFUSAL BRANCH WAS GUARDED BY THE PREDICATE IT EXISTS TO
  REPORT ON.  The predecessor read:

      if any(is_operation_list(v) for v in value.values()) and (names or digests):
          errors.append(...)

  so when `is_operation_list` is the thing that is wrong, the refusal cannot be
  reported and the artifact is refused SILENTLY as `(None, [])` --
  indistinguishable from "not a derivation at all", after which the surface is
  scored by top-level KEY NAMES, which is precisely the `CMP-IR-01` behaviour
  the array encoding was adopted to escape.  This file gives the refusal path an
  INDEPENDENT test (`declaration_candidate`) that never consults the strict
  predicate, the path grammar, or the key name `derivedFrom`.  This is the
  structural half: it prevents the whole class recurring for the next author who
  improves the format.

  A THIRD THING FOLLOWED FROM DEFECT 1 rather than being a separate repair: one
  of the four array-form derivations states its predecessor identity purely by
  DIGEST, because its base is a RESOLVED document that exists in no file.  A
  name is redundant when a digest is present, so the identity rule below admits
  content addressing -- and requires EVERY declared digest to be accounted for
  by a measurement before the resolution is accepted (freeze section 7.2.2: an
  uncompared recorded measurement is prose that looks like evidence).

WHAT DID NOT MOVE.  The two name-based predicates, the scoring, the review and
adjudication logic, the register reading, the printed layout of the default run,
and `product_qualification()`'s input path are the predecessor's, unchanged.
`CMP-IR-01`'s RENAME half is still open and still printed as open.

EXIT CODES.  Stated here and PRODUCED by `EXIT` below -- the banner is rendered
from the same table the code returns, so a document and a file cannot disagree
about them (freeze section 7.8.1 rule 3).

    0  GREEN            every measured class complete
    1  FINDINGS         the run measured something that is not complete
    2  REFUSED          a REQUIRED input is missing or unreadable.
                        THE CHECK DID NOT RUN.  This is not a finding.
    3  SELFTEST-REFUSED the mutation suite did not run (--selftest only)
    4  BAD-INVOCATION   an argument this file does not implement
    5  CLASS-SKIPPED    every required input present and every other class
                        measured, but a per-class input is missing so that
                        class DID NOT RUN.  Named in the output.  Findings
                        dominate: with findings present the exit is 1 and the
                        skip is still printed by name.

Usage: python3 artifacts/check-completeness-v2.py [--selftest | --derivations]
"""
from __future__ import annotations

import copy
import hashlib
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
ARTIFACTS = ROOT / "artifacts"
REGISTER = ARTIFACTS / "claim-register.v1.json"
OPERABILITY = ARTIFACTS / "operability.v2.json"

# Exit codes are data, not literals scattered through the code, so the docstring
# above and every `return` below read from one table.  Freeze section 7.8.1
# rule 3: an exit code a document CLAIMS must be the exit code the file
# PRODUCES.
EXIT = {
    "GREEN": 0,
    "FINDINGS": 1,
    "REFUSED": 2,
    "SELFTEST-REFUSED": 3,
    "BAD-INVOCATION": 4,
    "CLASS-SKIPPED": 5,
}

# `grammar` added 2026-08-03.  This predicate infers "the artifact carries a
# contract schema" from top-level KEY NAMES, which makes the measurement
# sensitive to renaming rather than to content.  EVIDENCE scored 4/4 while its
# schema was called `bundleSchema` and dropped to 3/4 when `evidence.v10` named
# the same thing `canonicalWireGrammar` -- a section that declares scalar
# encoding, record rules, a tag registry and record definitions, and is a
# stricter schema than the one it replaced.  The artifact did not regress; the
# regex lost it.
#
# Carried here VERBATIM from the predecessor.  Widening it further is not this
# file's subject and would move figures the freeze quotes.  `CMP-IR-01`'s rename
# half remains open and is still printed as open.
SCHEMA_RE = re.compile(r"schema|grammar|vocabular|union|codemaps|fieldtypes|properties", re.I)
GOLDEN_RE = re.compile(r"fixtures$|goldens$|goldencases$|^cases$", re.I)
SKIP_PREFIX = ("METHOD.", "CLEANSHEET", "ARCH.")
FINAL_STATES = {"RESOLVED", "REJECTED"}

# ---- CMP-IR-01, second half: derivation-aware effective contract ------------
#
# `CMP-IR-01` names TWO fragilities in the two predicates above, and only one of
# them is a regex problem.
#
#   1. RENAME.  The predicates match top-level KEY NAMES, so renaming a section
#      loses it.  **This half is NOT closed here and is deliberately left
#      standing**: every artifact that declares no derivation is still scored by
#      name.  See `reach` in the printed output for the live split.
#
#   2. DERIVATION.  No alternation can reach this one.  A delta document
#      presents NO key to match -- not a badly-named key, none at all.  Scoring
#      the delta measures the delta; it does not measure the contract.
#
# The reader below resolves the declared derivation and scores the EFFECTIVE
# contract.  Five properties make that a measurement rather than a concession.
# The first four are the predecessor's and are preserved; the fifth is this
# file's repair.
#
#   * It READS the declaration.  No predecessor path, digest or operation is
#     hardcoded here.  An artifact that declares no derivation is scored exactly
#     as it was before this change.
#   * It finds the declaration by SHAPE, not by the key name `derivedFrom`.
#     Locating the declaration by name would reproduce, one level up, the exact
#     naming fragility being repaired.  Measured over the live corpus the
#     declaration test fires on 17 blocks in 17 artifacts and on nothing else --
#     zero false positives, and the seventeen are exactly the artifacts that
#     declare a derivation.
#   * It VERIFIES before it uses.  The predecessor is hashed and compared to the
#     declared digest before its bytes are parsed, and every `set` must restate
#     type-exactly the value it replaces.
#   * It NEVER degrades silently.  A missing predecessor, a digest mismatch, an
#     operation that does not describe the bytes it is applied to, an unknown
#     verb, an ambiguous declaration: each is a published finding that fails the
#     run.  The surface then reports `own-keys/DERIVATION-UNRESOLVED`, which
#     cannot manufacture a point, and the reason is printed.
#   * NEW: the test that decides "this block IS a derivation declaration" is
#     INDEPENDENT of the test that decides "this declaration is well formed".
#     A block that is recognisably a declaration and cannot be materialised is
#     REPORTED WITH A NAMED REASON.  `(None, [])` -- the predecessor's silent
#     refusal -- is now reachable only for a block that carries no derivation
#     signal at all.  Two shapes still reach it and are named in
#     `KNOWN_SILENT_SHAPES` below with the measurement that keeps them open.
#
# The effective contract is scored with the SAME two predicates used everywhere
# else.  A derivation whose effective contract does not carry a schema, or whose
# operations delete one, scores exactly as low as it deserves -- the selftest
# mutates precisely that case.
JSON_NAME_RE = re.compile(r"^[A-Za-z0-9._][A-Za-z0-9._/-]*\.json$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
# Dotted-dialect step grammar, same as check-c2-v9.py `_STEP_RE`, so this
# reader walks dotted STRING paths the way the surface's own registered checker
# walks them.  RFC 6901 pointer paths are parsed by a separate strict branch in
# `path_steps`, and both parses must round-trip to the exact declared path
# (repair of 2026-08-12; see the corpus-resolution record for the measurement).
STEP_RE = re.compile(r"\[(\d+)\]|\.?([^.\[\]]+)")
DERIVATION_OPS = ("set", "add")
DERIVATION_MAX_DEPTH = 8

# Members of the operation vocabulary, used ONLY by the shape-independent
# candidate test.  They are read as a SET of member names and as a set of verb
# VALUES, never as a required key -- so an author who renames `op` while keeping
# the verb "set", or who drops the verb while keeping `path`/`value`, is still
# recognised as declaring a derivation and still gets a NAMED refusal.
OPERATION_MEMBERS = frozenset({"op", "path", "from", "value"})

# The two declaration shapes that can still reach `(None, [])`, published with
# the measurement that decides them rather than left for the next reader.  Both
# are cases where the ONLY available signal is a list whose contents carry no
# derivation evidence at all, and where widening the test to reach them was
# measured against the live corpus and REJECTED because it manufactures findings
# against artifacts that declare no derivation (freeze section 7.8.1: a
# non-defect must never present as a substantive finding).
KNOWN_SILENT_SHAPES = (
    ("operations list present but every item is a NON-DICT "
     "(e.g. [\"a\", \"b\"])",
     "widening the candidate test to `one name + one digest + a non-empty "
     "non-dict list` fires on 15 further blocks that declare no derivation, "
     "TWO of them binding artifacts of scored claims "
     "(evidence.v10.json, rust-provider-protocol.v4.json). Measured "
     "2026-08-10 over 427 artifact JSON documents."),
)


class Refusal(Exception):
    """A REQUIRED input is missing or unreadable.  Raising this is how the run
    says THE CHECK DID NOT RUN.  Freeze section 7.8.1 rule 1: a missing input
    must refuse, never proceed on a default -- "derived from nothing" and
    "derived and found nothing" must never print the same."""


def load_path(rel: str) -> dict | None:
    path = ROOT / rel
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text())
    except (OSError, json.JSONDecodeError):
        return None


def load_bytes(rel: str) -> bytes | None:
    """Raw bytes of a corpus file.  The derivation path hashes and parses THESE
    bytes, so the digest that is verified is the digest of what is then read."""
    try:
        return (ROOT / rel).read_bytes()
    except OSError:
        return None


def canonical_bytes(value: object) -> bytes:
    """Canonical serialisation used ONLY to check a declared digest of a
    RESOLVED value against the value this resolver produced.  Sorted keys,
    compact separators, UTF-8, no trailing newline.  This form is not inferred
    from prose: it is the form under which the one live artifact that declares
    such a digest reproduces its published value exactly, and any artifact using
    a different form gets a LOUD refusal naming the unaccounted digest rather
    than a silent pass."""
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False).encode("utf-8")


_DIGEST_INDEX: dict[str, list[str]] | None = None


def corpus_digest_index() -> dict[str, list[str]]:
    """sha256 -> the artifact files carrying exactly those bytes.

    Built lazily and only when a declaration identifies its predecessor by
    digest with no filename.  This is a MEASUREMENT of the tree, not a guess
    from a name."""
    global _DIGEST_INDEX
    if _DIGEST_INDEX is None:
        index: dict[str, list[str]] = {}
        try:
            paths = sorted(ARTIFACTS.glob("*.json"))
        except OSError:
            paths = []
        for path in paths:
            try:
                raw = path.read_bytes()
            except OSError:
                continue
            index.setdefault(hashlib.sha256(raw).hexdigest(), []).append(
                f"artifacts/{path.name}")
        _DIGEST_INDEX = index
    return _DIGEST_INDEX


def exact_equal(left: object, right: object) -> bool:
    """Type-exact deep equality.  `True` is not `1`, `1` is not `1.0`.

    Python's `==` would accept all three, which is exactly the coercion the
    predecessor's `from` restatement exists to forbid.
    """
    if type(left) is not type(right):
        return False
    if isinstance(left, dict):
        return set(left) == set(right) and all(
            exact_equal(left[key], right[key]) for key in left)
    if isinstance(left, list):
        return len(left) == len(right) and all(
            exact_equal(a, b) for a, b in zip(left, right))
    return left == right


def path_steps(path: str) -> list | None:
    """Steps of a STRING path -- an RFC 6901 JSON Pointer ('/a/b/0') or the
    dotted/indexed form ('a.b[0]') -- or None when the path is not plainly
    expressible.  Each dialect is parsed STRICTLY: the parse must round-trip to
    the exact declared path.  Guessing at a malformed path is how a resolver
    invents a contract the artifact never declared -- and until 2026-08-12 this
    function did exactly that to pointer paths, tokenising '/a/b' into ONE
    bogus step: every set then refused loudly, but an add would have SUCCEEDED
    by inventing a literal slash-named top-level key.  Measured in
    r1-lifetime-neutrality.conformance.v1.9.corpus-resolution.v1.json.

    Pointer rules: '~1' -> '/', '~0' -> '~', any other '~' refuses; an empty
    token refuses; a token in array-index form (0|[1-9][0-9]*) is an integer
    index, so a dict keyed by such a numeric string is refused at walk time
    rather than guessed at."""
    if not path:
        return None
    if path.startswith("/"):
        steps: list = []
        for token in path[1:].split("/"):
            if not token or re.search(r"~(?![01])", token):
                return None
            if re.fullmatch(r"0|[1-9][0-9]*", token):
                steps.append(int(token))
            else:
                steps.append(token.replace("~1", "/").replace("~0", "~"))
        rebuilt = "".join(
            "/" + (str(step) if isinstance(step, int)
                   else step.replace("~", "~0").replace("/", "~1"))
            for step in steps)
        return steps if rebuilt == path else None
    if path.startswith(".") or path.endswith(".") or ".." in path:
        return None
    steps = [int(index) if index else name for index, name in STEP_RE.findall(path)]
    if not steps:
        return None
    rebuilt = "".join(
        f"[{step}]" if isinstance(step, int)
        else (step if position == 0 else f".{step}")
        for position, step in enumerate(steps))
    return steps if rebuilt == path else None


def array_path_steps(tokens: list) -> list | None:
    """Steps of an ARRAY path: a JSON string is an object key, a JSON integer is
    a zero-based array index.  There is no grammar to get wrong, which is why
    this encoding is the better one.

    `bool` is tested BEFORE `int` because in Python `bool` subclasses `int`, so
    `[True]` would otherwise be admitted as index 1.  Freeze section 7.4 records
    that exact coercion class across this corpus.
    """
    if not tokens:
        return None
    steps: list = []
    for token in tokens:
        if isinstance(token, bool):
            return None
        if isinstance(token, str) or isinstance(token, int):
            steps.append(token)
            continue
        return None
    return steps


def operation_steps(operation: dict) -> tuple[list | None, str]:
    """(steps, display) for either encoding.  `display` is rendered from the
    NORMATIVE `path` member; a sibling `pathDisplay` is explicitly declared
    non-normative by the artifacts that carry it and is never read here."""
    raw = operation.get("path")
    if isinstance(raw, str):
        return path_steps(raw), raw
    if isinstance(raw, list):
        try:
            display = json.dumps(raw, ensure_ascii=False)
        except (TypeError, ValueError):
            display = repr(raw)
        return array_path_steps(raw), display
    return None, repr(raw)


def has_step(node: object, step: object) -> bool:
    if isinstance(node, dict):
        return isinstance(step, str) and step in node
    if isinstance(node, list):
        return isinstance(step, int) and not isinstance(step, bool) and 0 <= step < len(node)
    return False


def resolve_steps(root: object, steps: list) -> tuple[bool, object]:
    node = root
    for step in steps:
        if not has_step(node, step):
            return False, None
        node = node[step]
    return True, node


def recognised_path(raw: object) -> bool:
    """A path is RECOGNISED when its encoding is one this resolver walks.  Its
    CONTENTS are validated later, in `apply_operations`, so a malformed path
    fails in one place for both encodings and gets the same named refusal."""
    if isinstance(raw, str):
        return bool(raw)
    if isinstance(raw, list):
        return bool(raw)
    return False


def is_operation_list(value: object) -> bool:
    """STRICT: the list this resolver can execute.

    REPAIR 1.  The predecessor required `isinstance(item.get("path"), str)`,
    which rejected the array encoding outright.  Both encodings are accepted
    here and a mixed list is fine -- each operation is read on its own terms.
    """
    return (isinstance(value, list) and bool(value)
            and all(isinstance(item, dict) and isinstance(item.get("op"), str)
                    and recognised_path(item.get("path"))
                    for item in value))


def is_operation_shaped(item: object) -> bool:
    """WEAK, and deliberately NOT a function of `is_operation_list`.

    An item carries derivation evidence when ANY of these hold, so that a future
    author who improves the encoding is still RECOGNISED and therefore still
    gets a named refusal instead of silence:

      * it carries an `op` member (today's convention);
      * any of its string values is a declared verb (survives `op` being
        RENAMED, because the verb is read as a VALUE);
      * it carries two or more operation-vocabulary members (survives the verb
        being dropped entirely, e.g. `{"path": ..., "value": ...}`).

    Measured over 427 live artifact JSON documents each of the three alone, and
    all three together, select exactly the same 17 artifacts -- the seventeen
    that declare a derivation -- with zero false positives.  The union is used
    because it costs nothing measured and is the widest of the three.
    """
    if not isinstance(item, dict):
        return False
    if "op" in item:
        return True
    if any(isinstance(v, str) and v in DERIVATION_OPS for v in item.values()):
        return True
    return len(OPERATION_MEMBERS & set(item)) >= 2


def operation_shaped_lists(block: dict) -> list:
    return [v for v in block.values()
            if isinstance(v, list) and v and all(isinstance(i, dict) for i in v)
            and any(is_operation_shaped(i) for i in v)]


def declaration_identity(block: dict) -> tuple[list[str], list[str]]:
    names = [v for v in block.values()
             if isinstance(v, str) and JSON_NAME_RE.match(v)]
    digests = [v for v in block.values()
               if isinstance(v, str) and SHA256_RE.match(v)]
    return names, digests


def declaration_candidate(block: dict) -> str | None:
    """REPAIR 2, the structural half.  Does this block DECLARE a derivation?

    This test is the independent one.  It never calls `is_operation_list`, never
    parses a path, and never reads the key the block is filed under -- so it can
    still fire when the thing that is wrong is the operation encoding, which is
    exactly the case the predecessor could not report.

    Returns a short reason-shape name, or None when the block carries no
    derivation signal.

    A block declares a derivation when it states a predecessor identity (a
    filename or a digest, both by VALUE shape) and either

      OPERATION-SHAPED  some list value is a non-empty list of objects at least
                        one of which carries derivation evidence; or
      EMPTIED           it states a complete identity -- exactly one filename
                        and exactly one digest -- and carries at least one list,
                        every one of which is EMPTY.  A derivation whose
                        operation list was emptied states an identity and
                        executes nothing; measured over the live corpus this
                        shape fires on ZERO blocks, so admitting it costs no
                        false positive and closes the zero-operation-list trap
                        the predecessor documented and could not report.
    """
    names, digests = declaration_identity(block)
    if not (names or digests):
        return None
    if operation_shaped_lists(block):
        return "OPERATION-SHAPED"
    lists = [v for v in block.values() if isinstance(v, list)]
    if (len(names) == 1 and len(digests) == 1 and lists
            and all(not v for v in lists)):
        return "EMPTIED"
    return None


def declaration_fields(block: dict) -> dict | None:
    """The parts a derivation must state, located by value shape.

    Two identity forms are admitted, and both are hard-verified before use:

      NAMED    exactly one artifact filename and exactly one sha256.  This is
               the predecessor's rule, unchanged, so every artifact it resolved
               resolves here identically.
      CONTENT  no filename and one or more sha256.  A name is redundant when a
               digest is present -- the digest IS the identity -- so a
               declaration may address its predecessor purely by content.  The
               resolver then locates the predecessor by MEASURING the tree, and
               requires every declared digest to be accounted for.
    """
    names, digests = declaration_identity(block)
    operations = [v for v in block.values() if is_operation_list(v)]
    if len(operations) != 1:
        return None
    if len(names) == 1 and len(digests) == 1:
        return {"identity": "named", "artifact": names[0], "sha256": digests[0],
                "digests": [digests[0]], "operations": operations[0]}
    if not names and digests:
        return {"identity": "content", "artifact": None, "sha256": None,
                "digests": list(digests), "operations": operations[0]}
    return None


def declaration_refusal(key: str, block: dict) -> str:
    """Why a recognised declaration could not be materialised, NAMED.

    Every branch here is reachable only because `declaration_candidate` said the
    block is a declaration, which is decided without reference to any of the
    predicates whose failure is reported below.
    """
    names, digests = declaration_identity(block)
    strict = [v for v in block.values() if is_operation_list(v)]
    shaped = operation_shaped_lists(block)
    lists = [v for v in block.values() if isinstance(v, list)]

    if not shaped and lists and all(not v for v in lists):
        return (f"'{key}' states one predecessor name and one digest and its only "
                "list(s) are EMPTY; a derivation with no operations materialises "
                "no effective contract, so it is refused rather than scored as if "
                "no derivation had been declared")

    identity_ok = (len(names) == 1 and len(digests) == 1) or (not names and digests)
    if not identity_ok:
        # Wording preserved from the predecessor so the one live artifact that
        # already refuses loudly keeps refusing with the same named error.
        return (f"'{key}' carries an operation list and {len(names)} predecessor "
                f"name(s) and {len(digests)} digest(s); a derivation must state "
                "exactly one of each, so no effective contract can be materialised")

    if len(strict) > 1:
        return (f"'{key}' carries {len(strict)} operation lists; a derivation must "
                "state exactly one, so no effective contract can be materialised")

    if not strict:
        detail = describe_unreadable_operations(shaped)
        return (f"'{key}' states a predecessor identity and a list that declares "
                f"operations, but this resolver cannot execute that list: {detail}. "
                "No effective contract can be materialised, and the artifact is "
                "NOT scored as if it had declared no derivation")

    return (f"'{key}' is recognisable as a derivation declaration and could not be "
            "materialised; no effective contract exists for it")


def describe_unreadable_operations(shaped: list) -> str:
    """Name the FIRST operation this resolver cannot execute and say why.  A
    refusal that does not say which item is wrong sends the reader to read the
    whole list."""
    for operations in shaped:
        for index, item in enumerate(operations):
            if not isinstance(item, dict):
                return f"operation {index} is not an object"
            if not isinstance(item.get("op"), str):
                kind = type(item.get("op")).__name__
                return (f"operation {index} carries no string verb "
                        f"(its 'op' member is {kind})")
            raw = item.get("path")
            if not recognised_path(raw):
                if isinstance(raw, (str, list)) and not raw:
                    return (f"operation {index} ({item['op']}) carries an EMPTY path; "
                            "an empty path addresses the document root, which is not "
                            "a position an operation may replace")
                kind = type(raw).__name__
                return (f"operation {index} ({item['op']}) carries a path of type "
                        f"{kind}; the encodings this resolver walks are a non-empty "
                        "STRING (RFC 6901 pointer or dotted/indexed) and a "
                        "non-empty ARRAY of tokens")
    return "no readable operation was found in it"


def derivation_declaration(artifact: dict) -> tuple[dict | None, list[str]]:
    """(declaration, errors).  A block that DECLARES a derivation and does not
    state all its parts unambiguously is reported, never skipped quietly.

    The predecessor's error branch read `if any(is_operation_list(v) ...) and
    (names or digests)`, so it shared a predicate with the success branch and
    could not report the case where that predicate is wrong.  The candidate test
    used here shares nothing with it.
    """
    found: list[tuple[str, dict]] = []
    errors: list[str] = []
    for key, value in artifact.items():
        if not isinstance(value, dict):
            continue
        if declaration_candidate(value) is None:
            continue
        fields = declaration_fields(value)
        if fields is not None:
            found.append((key, fields))
            continue
        errors.append(declaration_refusal(key, value))
    if len(found) > 1:
        errors.append("ambiguous derivation: "
                      + ", ".join(sorted(key for key, _ in found)))
        return None, errors
    return (found[0][1] if found else None), errors


def apply_operations(base: object, operations: list) -> tuple[object, list[str]]:
    """Apply the declared operations in order.  Any refusal is a finding and the
    whole derivation is abandoned -- a partially applied delta is not a
    contract anyone declared."""
    effective = copy.deepcopy(base)
    errors: list[str] = []
    for index, op in enumerate(operations):
        kind = op.get("op")
        steps, display = operation_steps(op)
        where = f"operation {index} ({kind} {display})"
        if kind not in DERIVATION_OPS:
            errors.append(f"{where}: unknown verb; declared verbs are "
                          f"{list(DERIVATION_OPS)}")
            continue
        if "value" not in op:
            errors.append(f"{where}: carries no value")
            continue
        if steps is None:
            errors.append(f"{where}: path is not plainly resolvable")
            continue
        found, parent = resolve_steps(effective, steps[:-1])
        if not found or not isinstance(parent, (dict, list)):
            errors.append(f"{where}: parent does not resolve to a container")
            continue
        exists = has_step(parent, steps[-1])
        if kind == "set":
            if "from" not in op:
                errors.append(f"{where}: a set must restate the value it replaces")
                continue
            if not exists:
                errors.append(f"{where}: does not resolve against the predecessor")
                continue
            current = parent[steps[-1]]
            if not exact_equal(current, op["from"]):
                errors.append(
                    f"{where}: declares it replaces {op['from']!r} "
                    f"({type(op['from']).__name__}) but the verified predecessor "
                    f"holds {current!r} ({type(current).__name__}); the derivation "
                    "does not describe the bytes it is applied to")
                continue
        else:
            if exists:
                errors.append(f"{where}: already exists in the predecessor")
                continue
            if not isinstance(parent, dict) or not isinstance(steps[-1], str):
                errors.append(f"{where}: can only add a named member to an object")
                continue
        parent[steps[-1]] = copy.deepcopy(op["value"])
    return effective, errors


def locate_named_predecessor(artifact_rel: str, declaration: dict,
                             provenance: dict) -> tuple[bytes | None, list[str]]:
    name = declaration["artifact"]
    parent_dir = pathlib.PurePosixPath(artifact_rel).parent
    candidates = [str(parent_dir / name)] if str(parent_dir) != "." else [name]
    if "/" in name:
        candidates.append(name)
    provenance["predecessor"] = candidates[0]
    for candidate in candidates:
        raw = load_bytes(candidate)
        if raw is not None:
            provenance["predecessor"] = candidate
            return raw, []
    return None, [f"declared predecessor is absent: {candidates[0]}"]


def locate_content_predecessor(declaration: dict,
                               provenance: dict) -> tuple[bytes | None, list[str]]:
    """Locate a predecessor addressed purely by digest, by MEASURING the tree.

    Where several declared digests identify files on disk, the base is the HEAD
    of the declared chain -- the matched file that no other matched file names
    as ITS predecessor.  If that is not unique the resolution is refused; this
    resolver never picks one of several candidates and calls it the contract.
    """
    index = corpus_digest_index()
    on_disk = {d: index[d] for d in declaration["digests"] if index.get(d)}
    if not on_disk:
        return None, ["declaration addresses its predecessor by digest and none of "
                      f"the {len(declaration['digests'])} declared digest(s) "
                      "identifies a file under artifacts/"]
    for digest, paths in sorted(on_disk.items()):
        if len(paths) > 1:
            return None, [f"declared digest {digest[:16]}… identifies "
                          f"{len(paths)} files ({', '.join(sorted(paths))}); the "
                          "predecessor is not uniquely addressed"]
    subsumed: set[str] = set()
    for digest, paths in sorted(on_disk.items()):
        raw = load_bytes(paths[0])
        if raw is None:
            continue
        try:
            doc = json.loads(raw)
        except json.JSONDecodeError:
            continue
        if not isinstance(doc, dict):
            continue
        inner, _ = derivation_declaration(doc)
        if inner is None:
            continue
        for other in on_disk:
            if other != digest and other in inner["digests"]:
                subsumed.add(other)
    heads = sorted(set(on_disk) - subsumed)
    if len(heads) != 1:
        return None, [f"{len(on_disk)} declared digest(s) identify files on disk and "
                      f"{len(heads)} of them is/are the head of the declared chain; "
                      "the predecessor is not uniquely addressed"]
    head = heads[0]
    provenance["predecessor"] = on_disk[head][0]
    provenance["declaredDigest"] = head
    provenance["addressedBy"] = "content"
    return load_bytes(on_disk[head][0]), []


def resolve_derivation(artifact_rel: str, declaration: dict,
                       seen: tuple[str, ...] = ()) -> tuple[object | None, dict, list[str]]:
    """Materialise the effective contract, or explain why it cannot be."""
    provenance = {
        "predecessor": declaration.get("artifact") or "(addressed by digest)",
        "declaredDigest": declaration.get("sha256") or declaration["digests"][0],
        "operations": len(declaration["operations"]),
        "depth": len(seen) + 1,
        "verifiedDigests": [],
        # Which path dialect(s) this declaration writes, so the next dialect is
        # a census row rather than a surprise (2026-08-12).
        "pathDialect": sorted({
            "array-tokens" if isinstance(op.get("path"), list)
            else "json-pointer" if isinstance(op.get("path"), str)
            and op.get("path").startswith("/")
            else "dotted"
            for op in declaration["operations"]}),
    }

    if declaration["identity"] == "named":
        raw, errors = locate_named_predecessor(artifact_rel, declaration, provenance)
    else:
        raw, errors = locate_content_predecessor(declaration, provenance)
    if raw is None:
        return None, provenance, errors
    if len(seen) >= DERIVATION_MAX_DEPTH:
        return None, provenance, [
            f"derivation chain exceeds {DERIVATION_MAX_DEPTH} links"]
    if provenance["predecessor"] in seen:
        return None, provenance, [
            f"derivation chain revisits {provenance['predecessor']}"]

    actual = hashlib.sha256(raw).hexdigest()
    provenance["measuredDigest"] = actual
    if actual != provenance["declaredDigest"]:
        return None, provenance, [
            f"predecessor digest mismatch for {provenance['predecessor']}: declared "
            f"{provenance['declaredDigest']}, measured {actual}"]
    provenance["verifiedDigests"] = [actual]
    try:
        base = json.loads(raw)
    except json.JSONDecodeError as exc:
        return None, provenance, [
            f"verified predecessor {provenance['predecessor']} is not JSON: {exc}"]
    if not isinstance(base, dict):
        return None, provenance, [
            f"verified predecessor {provenance['predecessor']} is not a JSON object"]

    # A predecessor may itself be a delta.  Resolve the chain, verifying each
    # link, rather than scoring a delta that merely happens to sit one step back.
    inner, inner_errors = derivation_declaration(base)
    if inner_errors:
        return None, provenance, [
            f"{provenance['predecessor']}: {item}" for item in inner_errors]
    if inner is not None:
        base, inner_provenance, errors = resolve_derivation(
            provenance["predecessor"], inner, seen + (provenance["predecessor"],))
        provenance["via"] = inner_provenance
        if base is None:
            return None, provenance, errors
        provenance["verifiedDigests"] = (provenance["verifiedDigests"]
                                         + inner_provenance.get("verifiedDigests", []))

    # Freeze section 7.2.2: a recorded measurement must be compared to the
    # measurement it records.  A content-addressed declaration may carry digests
    # of things that are NOT files -- the canonical value of the resolved base
    # being the live case.  Every declared digest must be accounted for by a
    # measurement this resolver actually took, or the declaration is refused.
    if declaration["identity"] == "content":
        accounted = set(provenance["verifiedDigests"])
        resolved_digest = hashlib.sha256(canonical_bytes(base)).hexdigest()
        provenance["resolvedBaseCanonicalDigest"] = resolved_digest
        accounted.add(resolved_digest)
        unaccounted = [d for d in declaration["digests"] if d not in accounted]
        if unaccounted:
            return None, provenance, [
                f"declaration records {len(declaration['digests'])} digest(s) and "
                f"{len(unaccounted)} of them matches neither a verified file in the "
                "resolved chain nor the canonical value of the resolved base "
                f"({', '.join(d[:16] + '…' for d in unaccounted)}); an uncompared "
                "recorded digest is not evidence"]

    effective, errors = apply_operations(base, declaration["operations"])
    if errors:
        return None, provenance, errors
    return effective, provenance, []


def score_document(document: object) -> dict:
    """The two name-based predicates, applied to whatever document is the
    contract.  Unchanged in substance -- only WHICH document reaches it moves."""
    state = {"schema": False, "schemaKeys": [], "goldens": 0, "goldenKeys": []}
    if not isinstance(document, dict):
        return state
    for key, value in document.items():
        if SCHEMA_RE.search(key) and isinstance(value, dict):
            state["schema"] = True
            state["schemaKeys"].append(key)
    for key, value in document.items():
        if not GOLDEN_RE.search(key):
            continue
        if isinstance(value, list):
            count = len(value)
        elif isinstance(value, dict) and isinstance(value.get("fixtures"), list):
            count = len(value["fixtures"])
        else:
            continue
        state["goldens"] += count
        state["goldenKeys"].append((key, count))
    return state


def contract_shape(claim: dict) -> dict:
    rel = claim.get("bindingArtifact", "") or ""
    artifact = load_path(rel)
    invariants = bool(claim.get("invariants"))
    validator = claim.get("validator")
    checker = bool(validator and (ROOT / validator).exists())

    own = score_document(artifact)
    scored, source, provenance = own, "own-keys", None
    errors: list[str] = []

    if isinstance(artifact, dict):
        declaration, detect_errors = derivation_declaration(artifact)
        errors.extend(detect_errors)
        if detect_errors:
            source = "own-keys/DERIVATION-UNRESOLVED"
        elif declaration is not None:
            effective, provenance, resolve_errors = resolve_derivation(rel, declaration)
            errors.extend(resolve_errors)
            if effective is None:
                source = "own-keys/DERIVATION-UNRESOLVED"
            else:
                scored, source = score_document(effective), "derivation"

    def total(shape: dict) -> int:
        return sum((invariants, shape["schema"], shape["goldens"] > 0, checker))

    return {
        "invariants": invariants,
        "checker": checker,
        "schema": scored["schema"],
        "schemaKeys": scored["schemaKeys"],
        "goldens": scored["goldens"],
        "goldenKeys": scored["goldenKeys"],
        "score": total(scored),
        "ownScore": total(own),
        "ownSchemaKeys": own["schemaKeys"],
        "ownGoldens": own["goldens"],
        "source": source,
        "derivation": provenance,
        "errors": errors,
    }


def finding_ids(review: dict) -> set[str]:
    ids = {item.get("id") for item in review.get("findings", [])
           if isinstance(item, dict) and item.get("id")}
    ids |= set((review.get("resolves") or {}).keys())
    return ids


def resolution_state(adjudication: dict, finding_id: str) -> str | None:
    state = (adjudication.get("resolves") or {}).get(finding_id)
    if not isinstance(state, str):
        return None
    upper = state.upper()
    if upper.startswith("RESOLVED"):
        return "RESOLVED"
    if upper.startswith("REJECTED"):
        return "REJECTED"
    if upper == "CONFIRMED-PRIOR-REJECTION":
        return "REJECTED"
    if upper.startswith("OPEN"):
        return "OPEN"
    return upper


def review_state(claim: dict) -> tuple[dict, list[str]]:
    errors: list[str] = []
    review_paths = claim.get("currentReviewArtifacts", [])
    adjudication_paths = claim.get("adjudicationArtifacts", [])
    reviews: list[tuple[str, dict]] = []
    adjudications: list[tuple[str, dict]] = []
    for path in review_paths:
        item = load_path(path)
        if item is None:
            errors.append(f"registered review missing/invalid: {path}")
        else:
            reviews.append((path, item))
    for path in adjudication_paths:
        item = load_path(path)
        if item is None:
            errors.append(f"registered adjudication missing/invalid: {path}")
        else:
            adjudications.append((path, item))
    review_path_set = set(review_paths)
    for path, item in adjudications:
        adjudicates = item.get("adjudicates")
        if not isinstance(adjudicates, list) or not set(adjudicates) & review_path_set:
            errors.append(f"adjudication does not name a current review: {path}")
        if not isinstance(item.get("findingDispositions"), list):
            errors.append(f"adjudication has no findingDispositions array: {path}")
        verdict = item.get("sealRecommendation")
        if not isinstance(verdict, dict) or verdict.get("verdict") not in {
                "SEAL", "SEAL-WITH-CHANGES", "DO-NOT-SEAL"}:
            errors.append(f"adjudication has no closed seal verdict: {path}")

    ids = set().union(*(finding_ids(item) for _, item in reviews)) if reviews else set()
    open_ids: list[str] = []
    for review_path, review in reviews:
        for finding_id in sorted(finding_ids(review)):
            states: list[str] = []
            for adjudication_path, adjudication in adjudications:
                if review_path not in adjudication.get("adjudicates", []):
                    continue
                state = resolution_state(adjudication, finding_id)
                if state is not None:
                    states.append(state)
                    disposition_ids = {
                        item.get("findingId")
                        for item in adjudication.get("findingDispositions", [])
                        if isinstance(item, dict)
                    }
                    if finding_id not in disposition_ids:
                        errors.append(
                            f"{adjudication_path} resolves {finding_id} without a disposition"
                        )
            final_states = set(states) & FINAL_STATES
            if len(final_states) > 1:
                errors.append(f"conflicting adjudications for {finding_id}: {sorted(final_states)}")
            if not final_states:
                open_ids.append(finding_id)
    open_ids = sorted(set(open_ids))
    do_not_seal = any(
        isinstance(item.get("sealRecommendation"), dict)
        and item["sealRecommendation"].get("verdict") == "DO-NOT-SEAL"
        for _, item in adjudications
    )
    reviewed = bool(reviews)
    ready = reviewed and not open_ids and not claim.get("sealBlockers") and not do_not_seal
    return {
        "reviewed": reviewed,
        "reviewCount": len(reviews),
        "findingCount": len(ids),
        "openIds": open_ids,
        "doNotSeal": do_not_seal,
        "ready": ready,
    }, errors


def review_targets(path: pathlib.Path, data: dict) -> set[str]:
    values = []
    for key in ("reviewOf", "reviews"):
        value = data.get(key)
        if isinstance(value, str):
            values.append(value)
    return {pathlib.Path(value).name for value in values}


def unregistered_current_reviews(claims: list[dict]) -> list[str]:
    bindings = {pathlib.Path(c.get("bindingArtifact", "")).name: c for c in claims}
    registered = {str((ROOT / rel).resolve()) for c in claims
                  for rel in c.get("currentReviewArtifacts", [])}
    errors: list[str] = []
    for path in sorted(ARTIFACTS.glob("*.review-reviewer*.json")):
        try:
            data = json.loads(path.read_text())
        except (OSError, json.JSONDecodeError):
            continue
        targets = review_targets(path, data)
        if targets & set(bindings) and str(path.resolve()) not in registered:
            errors.append(f"unregistered current review: artifacts/{path.name}")
    return errors


def cross_cutting_state(register: dict) -> tuple[dict, list[str]]:
    pseudo = {
        "currentReviewArtifacts": register.get("crossCuttingReviewArtifacts", []),
        "adjudicationArtifacts": register.get("crossCuttingAdjudicationArtifacts", []),
        "sealBlockers": register.get("crossCuttingSealBlockers", []),
    }
    return review_state(pseudo)


def product_qualification() -> tuple[dict | None, str | None]:
    """(state, skipReason).  The input path is the predecessor's, unchanged.

    REPAIR to the REFUSAL SHAPE only, not to the measurement: the predecessor
    read this file with `load_path(...) or {}`, so an ABSENT operability
    artifact printed `NOT-RELEASE-QUALIFIED (0/0)` -- a specific, plausible,
    substantive accusation about the product, manufactured by a missing input.
    Freeze section 7.8.1 names exactly that shape.  Here the class is SKIPPED BY
    NAME and no product verdict is printed at all.
    """
    rel = "artifacts/operability.v2.json"
    if not (ROOT / rel).exists():
        return None, f"{rel} is absent"
    op = load_path(rel)
    if not isinstance(op, dict):
        return None, f"{rel} is present but is not a readable JSON object"
    decision = op.get("releaseDecision", {})
    total = len(op.get("requiredPropertyRegistry", {}).get("properties", []))
    demonstrated = decision.get("demonstratedPropertyCount", 0)
    return {
        "state": "RELEASE-QUALIFIED" if decision.get("state") == "RELEASABLE" else
                 "NOT-RELEASE-QUALIFIED",
        "demonstrated": demonstrated,
        "total": total,
    }, None


# ---- corpus derivation census ----------------------------------------------


def derivation_census() -> list[dict]:
    """Execute the resolver against every artifact that DECLARES a derivation.

    Freeze section 7.3 rider consequence 3: before applying ANY derivation,
    execute the resolver against it and require a POSITIVE resolution -- not
    merely the absence of an error.  This mode exists so that requirement can be
    met by running something rather than by reading something.
    """
    try:
        paths = sorted(ARTIFACTS.glob("*.json"))
    except OSError as exc:
        raise Refusal(f"artifacts/ cannot be listed: {exc}") from exc
    if not paths:
        raise Refusal("artifacts/ contains no JSON documents")
    rows: list[dict] = []
    for path in paths:
        rel = f"artifacts/{path.name}"
        try:
            document = json.loads(path.read_text())
        except (OSError, json.JSONDecodeError):
            continue
        if not isinstance(document, dict):
            continue
        declares = any(isinstance(v, dict) and declaration_candidate(v) is not None
                       for v in document.values())
        if not declares:
            continue
        declaration, errors = derivation_declaration(document)
        if errors:
            rows.append({"artifact": rel, "verdict": "REFUSED", "stage": "declaration",
                         "reasons": errors, "provenance": None})
            continue
        if declaration is None:
            rows.append({"artifact": rel, "verdict": "REFUSED", "stage": "declaration",
                         "reasons": ["recognised as a derivation declaration and no "
                                     "declaration could be read from it"],
                         "provenance": None})
            continue
        effective, provenance, resolve_errors = resolve_derivation(rel, declaration)
        if effective is None:
            rows.append({"artifact": rel, "verdict": "REFUSED", "stage": "resolution",
                         "reasons": resolve_errors, "provenance": provenance})
            continue
        shape = score_document(effective)
        rows.append({"artifact": rel, "verdict": "RESOLVED", "stage": "resolution",
                     "reasons": [], "provenance": provenance,
                     "identity": declaration["identity"],
                     "operations": len(declaration["operations"]),
                     "pathForms": sorted({
                         "array" if isinstance(op.get("path"), list) else "string"
                         for op in declaration["operations"]}),
                     "effectiveTopLevelKeys": len(effective),
                     "effectiveSchema": shape["schema"],
                     "effectiveGoldens": shape["goldens"]})
    return rows


def print_derivation_census() -> int:
    rows = derivation_census()
    resolved = [r for r in rows if r["verdict"] == "RESOLVED"]
    refused = [r for r in rows if r["verdict"] == "REFUSED"]
    print("derivation resolution census -- every artifact that DECLARES a derivation")
    print("a POSITIVE resolution is required before a derivation is applied"
          " (freeze section 7.3 rider)\n")
    print(f"  {'artifact':<48} {'verdict':<9} {'paths':<7} {'ops':>4} {'identity':<8}")
    for row in rows:
        if row["verdict"] == "RESOLVED":
            print(f"  {row['artifact']:<48} {'RESOLVED':<9}"
                  f" {'+'.join(row['pathForms']):<7} {row['operations']:>4}"
                  f" {row['identity']:<8}"
                  f"  -> {row['effectiveTopLevelKeys']} top-level keys,"
                  f" schema={row['effectiveSchema']},"
                  f" goldens={row['effectiveGoldens']}")
        else:
            print(f"  {row['artifact']:<48} {'REFUSED':<9} {'-':<7} {'-':>4} {'-':<8}")
            for reason in row["reasons"]:
                print(f"      reason: {reason}")
    print(f"\n  declared derivations: {len(rows)}")
    print(f"  POSITIVELY RESOLVED:  {len(resolved)}")
    print(f"  REFUSED, each named:  {len(refused)}")
    print("  silently refused:     0"
          "  (a declaration this resolver recognises always produces a named"
          " reason)")
    for shape, why in KNOWN_SILENT_SHAPES:
        print(f"  STILL UNREACHABLE: {shape}")
        print(f"      not closed because: {why}")
    return EXIT["GREEN"] if not refused else EXIT["FINDINGS"]


# ---- selftest ---------------------------------------------------------------


def derivation_selftest() -> tuple[bool, list[str]]:
    """Mutations a broken derivation resolver would fail.

    Every case the predecessor ran is carried here unchanged, so a divergence
    would show up as a failing line rather than as a missing one.  The new cases
    are the array encoding, the mixed encoding, the shape-independent refusal
    test, and the content-addressed identity.

    The interesting ones are still not the malformed inputs -- they are
    `deletes-schema` and `empties-goldens`.  A resolver that trusted the
    declaration instead of scoring its result would keep awarding the schema
    point to a derivation that DELETES the schema.  That failure would
    manufacture seal-readiness out of a declaration, which is a worse defect
    than the blindness being repaired.
    """
    base = {
        "stageSchemas": {"kinds": {"probe": {"required": ["probeId"]}}},
        "planFixtures": [{"id": "a", "valid": True}, {"id": "b", "valid": False}],
        "version": 4,
        "enabled": True,
        "counters": {"contractRoot": {"containerPaths": 794}},
        "rows": [{"n": 1}, {"n": 2}],
    }
    raw = json.dumps(base, indent=1).encode("utf-8")
    digest = hashlib.sha256(raw).hexdigest()
    zero = "0" * 64

    def delta(operations, name="base.json", sha=digest, key="derivedFrom"):
        return {"artifact": "delta", key: {
            "artifact": name, "sha256": sha,
            "rule": "no byte of the predecessor is transcribed into this file",
            "operations": operations}}

    bump = [{"op": "set", "path": "version", "from": 4, "value": 9}]
    array_bump = [{"op": "set", "path": ["version"], "pathDisplay": "$.version",
                   "from": 4, "value": 9}]
    files = {"artifacts/base.json": raw}
    documents = {
        # --- carried verbatim from the predecessor's suite -------------------
        "preserving": delta(bump),
        "renamed-declaration": delta(bump, key="materialisedFrom"),
        "wrong-digest": delta(bump, sha=zero),
        "missing-predecessor": delta(bump, name="absent.json"),
        "altered-operations": delta([{"op": "set", "path": "version",
                                      "from": 99, "value": 9}]),
        "coerced-from": delta([{"op": "set", "path": "enabled",
                                "from": 1, "value": False}]),
        "unknown-verb": delta([{"op": "merge", "path": "extraFixtures",
                                "value": [{"id": "c"}]}]),
        "add-over-existing": delta([{"op": "add", "path": "version", "value": 9}]),
        "sets-absent-path": delta([{"op": "set", "path": "notThere",
                                    "from": None, "value": {"a": 1}}]),
        "nested-paths": delta([
            {"op": "set", "path": "counters.contractRoot.containerPaths",
             "from": 794, "value": 797},
            {"op": "add", "path": "stageSchemas.kinds.rule-evaluation",
             "value": {"forbidden": ["operator"]}}]),
        "adds-block": delta([{"op": "add", "path": "extraFixtures",
                              "value": [{"id": "c"}]}]),
        "deletes-schema": delta([{"op": "set", "path": "stageSchemas",
                                  "from": copy.deepcopy(base["stageSchemas"]),
                                  "value": "moved to the successor"}]),
        "empties-goldens": delta([{"op": "set", "path": "planFixtures",
                                   "from": copy.deepcopy(base["planFixtures"]),
                                   "value": []}]),
        "ambiguous": {**delta(bump), "alsoDerivedFrom": {
            "artifact": "base.json", "sha256": digest, "operations": bump}},
        "no-derivation": {"artifact": "plain", "stageSchemas": {"a": {}},
                          "planFixtures": [{"id": "a"}]},
        "plain-no-shape": {"artifact": "plain", "notes": {"a": 1}},
        # --- REPAIR 1: the array encoding ------------------------------------
        "array-preserving": delta(array_bump),
        "array-nested": delta([
            {"op": "set", "path": ["counters", "contractRoot", "containerPaths"],
             "pathDisplay": "$.counters.contractRoot.containerPaths",
             "from": 794, "value": 797},
            {"op": "add", "path": ["stageSchemas", "kinds", "rule-evaluation"],
             "pathDisplay": "$.stageSchemas.kinds['rule-evaluation']",
             "value": {"forbidden": ["operator"]}}]),
        "array-index": delta([{"op": "set", "path": ["rows", 1, "n"],
                               "from": 2, "value": 5}]),
        "array-dotted-key": delta([
            {"op": "add", "path": ["stageSchemas", "kinds", "a.b"],
             "value": {"required": ["x"]}}]),
        "mixed-encodings": delta([
            {"op": "set", "path": "version", "from": 4, "value": 9},
            {"op": "set", "path": ["counters", "contractRoot", "containerPaths"],
             "from": 794, "value": 797}]),
        "array-altered-from": delta([{"op": "set", "path": ["version"],
                                      "from": 99, "value": 9}]),
        "array-bool-index": delta([{"op": "set", "path": ["rows", True, "n"],
                                    "from": 2, "value": 5}]),
        "array-empty-path": delta([{"op": "set", "path": [], "from": 4, "value": 9}]),
        "array-bad-token": delta([{"op": "set", "path": [{"k": 1}], "from": 4,
                                   "value": 9}]),
        "array-deletes-schema": delta([
            {"op": "set", "path": ["stageSchemas"],
             "from": copy.deepcopy(base["stageSchemas"]),
             "value": "moved to the successor"}]),
        # --- the POINTER dialect (repair of 2026-08-12) ----------------------
        "pointer-preserving": delta([{"op": "set", "path": "/version",
                                      "from": 4, "value": 9}]),
        "pointer-nested": delta([
            {"op": "set", "path": "/counters/contractRoot/containerPaths",
             "from": 794, "value": 797},
            {"op": "add", "path": "/stageSchemas/kinds/rule-evaluation",
             "value": {"forbidden": ["operator"]}}]),
        "pointer-index": delta([{"op": "set", "path": "/rows/1/n",
                                 "from": 2, "value": 5}]),
        "pointer-add-top": delta([{"op": "add", "path": "/extraFixtures",
                                   "value": [{"id": "c"}]}]),
        "pointer-bad-escape": delta([{"op": "set", "path": "/ver~2sion",
                                      "from": 4, "value": 9}]),
        "pointer-empty-token": delta([{"op": "set", "path": "/version/",
                                       "from": 4, "value": 9}]),
        "guessed-path-add": delta([{"op": "add", "path": "]extraFixtures[",
                                    "value": [{"id": "c"}]}]),
        # --- REPAIR 2: refusals that the predecessor could not report --------
        "unreadable-path-type": delta([{"op": "set", "path": 7, "from": 4, "value": 9}]),
        "no-verb-member": delta([{"path": ["version"], "from": 4, "value": 9}]),
        "renamed-verb-member": delta([{"verb": "set", "path": ["version"],
                                       "from": 4, "value": 9}]),
        "missing-digest": {"artifact": "delta", "derivedFrom": {
            "artifact": "base.json", "operations": array_bump}},
        "two-names": {"artifact": "delta", "derivedFrom": {
            "artifact": "base.json", "alsoFrom": "other.json", "sha256": digest,
            "operations": array_bump}},
        "two-digests": {"artifact": "delta", "derivedFrom": {
            "artifact": "base.json", "sha256": digest, "otherSha256": zero,
            "operations": array_bump}},
        "empty-operations": {"artifact": "delta", "derivedFrom": {
            "artifact": "base.json", "sha256": digest, "operations": []}},
        "two-operation-lists": {"artifact": "delta", "derivedFrom": {
            "artifact": "base.json", "sha256": digest,
            "operations": array_bump, "alsoOperations": bump}},
        "ops-not-dicts": {"artifact": "delta", "derivedFrom": {
            "artifact": "base.json", "sha256": digest,
            "operations": ["set version 9", "add fixtures"]}},
        "no-value": delta([{"op": "set", "path": ["version"], "from": 4}]),
        # --- content-addressed identity --------------------------------------
        "content-addressed": {"artifact": "delta", "derivedFrom": {
            "predecessorSha256": digest, "operations": array_bump}},
        "content-unknown-digest": {"artifact": "delta", "derivedFrom": {
            "predecessorSha256": zero, "operations": array_bump}},
        "content-unaccounted-digest": {"artifact": "delta", "derivedFrom": {
            "predecessorSha256": digest, "strayDigest": "1" * 64,
            "operations": array_bump}},
    }
    paths = {f"artifacts/{name}.json": doc for name, doc in documents.items()}

    original_load, original_bytes = globals()["load_path"], globals()["load_bytes"]
    original_index = globals()["_DIGEST_INDEX"]
    globals()["load_path"] = lambda rel: copy.deepcopy(paths.get(rel))
    globals()["load_bytes"] = lambda rel: files.get(rel)
    # The content-addressed route measures the tree.  In the selftest the tree
    # is the fixture set, declared here rather than read from disk, so the case
    # is exercised without depending on any live artifact.
    globals()["_DIGEST_INDEX"] = {digest: ["artifacts/base.json"]}
    try:
        def shape(name):
            return contract_shape({
                "id": name, "invariants": ["i"],
                "bindingArtifact": f"artifacts/{name}.json",
                "validator": "artifacts/check-completeness-v2.py"})
        measured = {name: shape(name) for name in documents}
        effective = {}
        for name in ("nested-paths", "preserving", "array-nested", "array-preserving",
                     "array-index", "array-dotted-key", "mixed-encodings",
                     "content-addressed", "pointer-preserving", "pointer-nested",
                     "pointer-index", "pointer-add-top"):
            rel = f"artifacts/{name}.json"
            declaration, _ = derivation_declaration(paths[rel])
            effective[name], _, _ = resolve_derivation(rel, declaration)
        # The silent-refusal sweep: no recognised declaration may produce
        # (None, []).  Measured directly on the reader, not inferred from the
        # score, because the score cannot distinguish "refused" from "declared
        # nothing".
        sweep = {}
        for name, document in documents.items():
            declares = any(isinstance(v, dict) and declaration_candidate(v) is not None
                           for v in document.values())
            decl, errs = derivation_declaration(document)
            sweep[name] = (declares, decl is not None, bool(errs))
    finally:
        globals()["load_path"] = original_load
        globals()["load_bytes"] = original_bytes
        globals()["_DIGEST_INDEX"] = original_index

    def resolved(name, schema, goldens, score):
        state = measured[name]
        return (state["source"] == "derivation" and not state["errors"]
                and state["schema"] is schema and state["goldens"] == goldens
                and state["score"] == score)

    def refused(name, because):
        """Refused for the STATED reason.  Without pinning the reason a mutant
        that breaks one gate can be caught by an unrelated one and the gate it
        broke never gets tested -- which is how a mutation suite passes while
        measuring nothing."""
        state = measured[name]
        return (state["source"] == "own-keys/DERIVATION-UNRESOLVED"
                and any(because in item for item in state["errors"])
                and state["score"] == state["ownScore"]
                and state["schema"] is False and state["goldens"] == 0)

    silent = sorted(name for name, (declares, ok, err) in sweep.items()
                    if declares and not ok and not err)
    unrecognised = sorted(name for name, (declares, ok, err) in sweep.items()
                          if not declares and name not in
                          ("no-derivation", "plain-no-shape", "ops-not-dicts"))

    checks = [
        # ---- predecessor parity -------------------------------------------
        (resolved("preserving", True, 2, 4),
         "accept  derivation that preserves schema+goldens scores the EFFECTIVE contract",
         "FAIL    a resolvable derivation was not resolved"),
        (measured["preserving"]["ownScore"] == 2,
         "accept  the same delta scores 2/4 on its own keys -- the +2 is the repair",
         "FAIL    own-key baseline is not 2/4, so the delta is not measurable"),
        (resolved("renamed-declaration", True, 2, 4),
         "accept  declaration found by SHAPE when its key is renamed",
         "ESCAPE  a renamed declaration key blinded the reader (CMP-IR-01 again)"),
        (refused("wrong-digest", "digest mismatch"),
         "reject  predecessor whose measured digest is not the declared one",
         "ESCAPE  an unverified predecessor was scored"),
        (refused("missing-predecessor", "is absent"),
         "reject  declared predecessor that is absent",
         "ESCAPE  a missing predecessor degraded silently"),
        (refused("altered-operations", "does not describe the bytes"),
         "reject  set whose 'from' is not what the verified predecessor holds",
         "ESCAPE  an operation list that lies about its base was applied"),
        (refused("coerced-from", "does not describe the bytes"),
         "reject  set restating 'from' as 1 where the predecessor holds true",
         "ESCAPE  bool/int coercion let a false restatement through"),
        (refused("unknown-verb", "unknown verb"),
         "reject  operation verb outside the declared set",
         "ESCAPE  an undeclared verb was executed"),
        (refused("add-over-existing", "already exists in the predecessor"),
         "reject  add at a path the predecessor already holds",
         "ESCAPE  an add silently overwrote predecessor bytes"),
        (refused("sets-absent-path", "does not resolve against the predecessor"),
         "reject  set at a path the verified predecessor does not hold",
         "ESCAPE  a set invented a path the predecessor never carried"),
        (resolved("nested-paths", True, 2, 4)
         and effective["nested-paths"]["counters"]["contractRoot"]["containerPaths"] == 797
         and "rule-evaluation" in effective["nested-paths"]["stageSchemas"]["kinds"]
         and effective["preserving"]["counters"]["contractRoot"]["containerPaths"] == 794
         and "rule-evaluation" not in effective["preserving"]["stageSchemas"]["kinds"],
         "accept  nested set/add land on the effective contract and do not leak"
         " between resolutions",
         "FAIL    nested paths were not applied, or one resolution mutated another"),
        (resolved("adds-block", True, 3, 4),
         "accept  add of a new goldens array is counted in the effective contract",
         "FAIL    a declared add was not applied"),
        (resolved("deletes-schema", False, 2, 3) and measured["deletes-schema"]["score"]
         < measured["deletes-schema"]["ownScore"] + 2,
         "reject  DERIVATION THAT DELETES THE SCHEMA still loses the schema point",
         "ESCAPE  a declaration bought a schema point the effective contract lacks"),
        (resolved("empties-goldens", True, 0, 3),
         "reject  DERIVATION THAT EMPTIES THE FIXTURES still loses the goldens point",
         "ESCAPE  a declaration bought a goldens point the effective contract lacks"),
        (refused("ambiguous", "ambiguous derivation"),
         "reject  two competing derivation declarations in one artifact",
         "ESCAPE  the reader picked one of two declarations and called it the contract"),
        (measured["no-derivation"]["source"] == "own-keys"
         and measured["no-derivation"]["score"] == 4
         and not measured["no-derivation"]["errors"],
         "accept  artifact declaring no derivation scores exactly as before",
         "FAIL    a non-derived artifact changed score"),
        (measured["plain-no-shape"]["source"] == "own-keys"
         and measured["plain-no-shape"]["score"] == 2,
         "accept  artifact carrying neither schema nor goldens still scores 2/4",
         "FAIL    a shapeless artifact gained a point"),
        # ---- REPAIR 1: the array encoding ----------------------------------
        (resolved("array-preserving", True, 2, 4)
         and effective["array-preserving"]["version"] == 9,
         "accept  ARRAY-FORM path resolves and lands (repair 1)",
         "ESCAPE  an array-form derivation was not recognised -- defect 1 is back"),
        (resolved("array-nested", True, 2, 4)
         and effective["array-nested"]["counters"]["contractRoot"]["containerPaths"] == 797
         and "rule-evaluation" in effective["array-nested"]["stageSchemas"]["kinds"],
         "accept  nested ARRAY set/add land on the effective contract",
         "FAIL    nested array paths were not applied"),
        (resolved("array-index", True, 2, 4)
         and effective["array-index"]["rows"][1]["n"] == 5,
         "accept  ARRAY integer token addresses a list index",
         "FAIL    an array index token was not walked"),
        (resolved("array-dotted-key", True, 2, 4)
         and "a.b" in effective["array-dotted-key"]["stageSchemas"]["kinds"],
         "accept  ARRAY token carrying a dot is ONE key -- the encoding the string"
         " grammar cannot express",
         "FAIL    a dotted array token was split or refused"),
        (resolved("mixed-encodings", True, 2, 4)
         and effective["mixed-encodings"]["version"] == 9
         and effective["mixed-encodings"]["counters"]["contractRoot"]["containerPaths"] == 797,
         "accept  a list mixing both encodings -- each operation read on its own terms",
         "FAIL    a mixed-encoding operation list was refused or misapplied"),
        # ---- the POINTER dialect (2026-08-12) ------------------------------
        (resolved("pointer-preserving", True, 2, 4)
         and effective["pointer-preserving"]["version"] == 9,
         "accept  RFC 6901 POINTER path resolves and lands (dialect repair)",
         "ESCAPE  a pointer-form derivation was refused -- the dialect gap is back"),
        (resolved("pointer-nested", True, 2, 4)
         and effective["pointer-nested"]["counters"]["contractRoot"]["containerPaths"] == 797
         and "rule-evaluation" in effective["pointer-nested"]["stageSchemas"]["kinds"]
         and canonical_bytes(effective["pointer-nested"]) == canonical_bytes(effective["nested-paths"]),
         "accept  nested POINTER set/add land, byte-identical to the dotted spelling",
         "FAIL    the pointer and dotted spellings of one derivation diverged"),
        (resolved("pointer-index", True, 2, 4)
         and effective["pointer-index"]["rows"][1]["n"] == 5,
         "accept  POINTER numeric token addresses a list index",
         "FAIL    a pointer index token was not walked"),
        (resolved("pointer-add-top", True, 3, 4)
         and "extraFixtures" in effective["pointer-add-top"]
         and "/extraFixtures" not in effective["pointer-add-top"],
         "accept  POINTER add lands on the named key, never on a literal '/key'",
         "ESCAPE  a pointer add invented a literal slash-named key -- the silent hazard"),
        (refused("pointer-bad-escape", "path is not plainly resolvable"),
         "reject  pointer with an undefined '~' escape",
         "ESCAPE  a malformed pointer escape was guessed at"),
        (refused("pointer-empty-token", "path is not plainly resolvable"),
         "reject  pointer with an empty token",
         "ESCAPE  an empty pointer token was guessed at"),
        (refused("guessed-path-add", "path is not plainly resolvable"),
         "reject  add whose path parses only by GUESSING -- refusal, not invention",
         "ESCAPE  a non-round-tripping path was walked on a guess"),
        (refused("array-altered-from", "does not describe the bytes"),
         "reject  ARRAY set whose 'from' is not what the predecessor holds",
         "ESCAPE  the array path skipped the 'from' restatement gate"),
        (refused("array-bool-index", "path is not plainly resolvable"),
         "reject  ARRAY index token that is a bool (bool tested BEFORE int)",
         "ESCAPE  True was admitted as index 1 -- the 1.0==1 class, section 7.4"),
        (refused("array-empty-path", "carries an EMPTY path"),
         "reject  ARRAY path that is empty -- NAMED at the declaration gate, the same"
         " treatment an empty STRING path gets",
         "ESCAPE  an empty array path resolved to the document root"),
        (refused("array-bad-token", "path is not plainly resolvable"),
         "reject  ARRAY path token that is neither string nor integer",
         "ESCAPE  an unwalkable token was guessed at"),
        (resolved("array-deletes-schema", False, 2, 3),
         "reject  ARRAY derivation that DELETES the schema still loses the point",
         "ESCAPE  the array path bought a schema point the contract lacks"),
        # ---- REPAIR 2: refusals independent of the operation predicate ------
        (refused("unreadable-path-type", "the encodings this resolver walks"),
         "reject  path of an encoding this resolver does not know -- NAMED, not silent"
         " (repair 2)",
         "ESCAPE  an unknown path encoding was refused SILENTLY -- defect 2 is back"),
        (refused("no-verb-member", "carries no string verb"),
         "reject  operation with no verb member at all -- NAMED",
         "ESCAPE  a verbless operation list was dropped silently"),
        (refused("renamed-verb-member", "carries no string verb"),
         "reject  operation whose verb member is RENAMED -- still recognised as a"
         " declaration, still NAMED",
         "ESCAPE  renaming 'op' blinded the refusal path"),
        (refused("missing-digest", "1 predecessor name(s) and 0 digest(s)"),
         "reject  declaration with a name and no digest -- NAMED",
         "ESCAPE  a digestless declaration was refused silently"),
        (refused("two-names", "2 predecessor name(s)"),
         "reject  declaration naming two predecessors -- NAMED (the live"
         " retention-tiers.v27 class)",
         "ESCAPE  a two-predecessor declaration was refused silently"),
        (refused("two-digests", "2 digest(s)"),
         "reject  declaration carrying two digests -- NAMED",
         "ESCAPE  a two-digest declaration was refused silently"),
        (refused("empty-operations", "list(s) are EMPTY"),
         "reject  declaration whose operation list is EMPTY -- NAMED (the"
         " zero-operation-list trap, now reportable)",
         "ESCAPE  an emptied operation list was refused silently"),
        (refused("two-operation-lists", "carries 2 operation lists"),
         "reject  declaration carrying two operation lists -- NAMED",
         "ESCAPE  a two-list declaration was refused silently"),
        (refused("no-value", "carries no value"),
         "reject  operation carrying neither a value nor a recognised verb path",
         "ESCAPE  a valueless operation was applied"),
        (not silent,
         "accept  SWEEP: every recognised declaration in this suite produces a NAMED"
         " reason -- none returns (None, [])",
         f"ESCAPE  silent refusal survives for: {silent}"),
        (not unrecognised,
         "accept  SWEEP: every malformed declaration in this suite is RECOGNISED as a"
         " declaration",
         f"FAIL    not recognised as declarations: {unrecognised}"),
        (sweep["ops-not-dicts"] == (False, False, False),
         "declare RESIDUAL: an operations list of NON-DICTS is not recognised and is"
         " refused silently -- published, not hidden (see KNOWN_SILENT_SHAPES)",
         "FAIL    the published residual does not reproduce; the disclosure is stale"),
        # ---- content-addressed identity ------------------------------------
        (resolved("content-addressed", True, 2, 4)
         and effective["content-addressed"]["version"] == 9,
         "accept  predecessor addressed purely by DIGEST is located by measuring the"
         " tree",
         "FAIL    a content-addressed declaration did not resolve"),
        (refused("content-unknown-digest", "identifies a file under artifacts/"),
         "reject  content-addressed declaration whose digest matches no file -- NAMED",
         "ESCAPE  a content address with no referent degraded silently"),
        (refused("content-unaccounted-digest", "an uncompared recorded digest is not"
                 " evidence"),
         "reject  content-addressed declaration carrying a digest that matches neither"
         " a chain file nor the resolved base (section 7.2.2)",
         "ESCAPE  a recorded digest went uncompared and the resolution was accepted"),
    ]
    lines = [f"  {ok_text}" if ok else f"  {bad_text}" for ok, ok_text, bad_text in checks]
    caught = sum(1 for ok, _, _ in checks if ok)
    lines.append(f"  measured: {caught}/{len(checks)} derivation cases behaved as stated")
    return all(ok for ok, _, _ in checks), lines


def selftest() -> int:
    review = {"findings": [{"id": "F-1"}], "resolves": {"F-1": "OPEN"}}
    base_claim = {"currentReviewArtifacts": ["review.json"], "sealBlockers": []}
    good_shape = {
        "adjudicates": ["review.json"],
        "findingDispositions": [{"findingId": "F-1"}],
        "sealRecommendation": {"verdict": "SEAL-WITH-CHANGES"},
    }
    fixtures = {
        "review.json": review,
        "paper.json": {**good_shape, "resolves": {"F-1": "OPEN — checker passes"}},
        "resolved.json": {**good_shape, "resolves": {"F-1": "RESOLVED"}},
        "rejected.json": {**good_shape, "resolves": {"F-1": "REJECTED"}},
        "unrelated.json": {
            **good_shape,
            "adjudicates": ["other-review.json"],
            "resolves": {"F-1": "RESOLVED"},
        },
    }
    original_loader = globals()["load_path"]
    globals()["load_path"] = lambda rel: fixtures.get(rel)
    try:
        unresolved = review_state({**base_claim, "adjudicationArtifacts": []})[0]["openIds"] == ["F-1"]
        paper = review_state({**base_claim, "adjudicationArtifacts": ["paper.json"]})[0]["openIds"] == ["F-1"]
        resolved = review_state({**base_claim, "adjudicationArtifacts": ["resolved.json"]})[0]["ready"]
        rejected = review_state({**base_claim, "adjudicationArtifacts": ["rejected.json"]})[0]["ready"]
        unrelated_state, unrelated_errors = review_state(
            {**base_claim, "adjudicationArtifacts": ["unrelated.json"]}
        )
        unrelated = unrelated_state["openIds"] == ["F-1"] and bool(unrelated_errors)
    finally:
        globals()["load_path"] = original_loader
    derivation_ok, derivation_lines = derivation_selftest()
    ok = (unresolved and resolved and rejected and paper and unrelated
          and derivation_ok)
    print("completeness mutation self-test")
    print("  reject  registered OPEN review with no adjudication" if unresolved else
          "  ESCAPE  open review disappeared")
    print("  accept  explicit RESOLVED adjudication" if resolved else
          "  FAIL    resolved adjudication not understood")
    print("  accept  reasoned REJECTED adjudication" if rejected else
          "  FAIL    rejected adjudication not understood")
    print("  reject  prose containing 'checker passes' while state remains OPEN" if paper else
          "  ESCAPE  prose green-washed an OPEN state")
    print("  reject  adjudication that does not name the current review" if unrelated else
          "  ESCAPE  unrelated adjudication resolved a current finding")
    print("derivation-aware contract-shape mutation self-test (CMP-IR-01 second half)")
    for line in derivation_lines:
        print(line)
    return EXIT["GREEN"] if ok else EXIT["FINDINGS"]


# ---- main -------------------------------------------------------------------


def read_register() -> dict:
    """The register is a REQUIRED input.  Every branch here says THE CHECK DID
    NOT RUN rather than proceeding on an empty default."""
    if not REGISTER.exists():
        raise Refusal(f"required input is absent: {REGISTER}")
    try:
        raw = REGISTER.read_text()
    except OSError as exc:
        raise Refusal(f"required input cannot be read: {REGISTER}: {exc}") from exc
    try:
        register = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise Refusal(f"required input is not JSON: {REGISTER}: {exc}") from exc
    if not isinstance(register, dict) or not isinstance(register.get("claims"), list):
        raise Refusal(f"required input carries no claims array: {REGISTER}")
    for claim in register["claims"]:
        if not isinstance(claim, dict) or not isinstance(claim.get("id"), str):
            raise Refusal(f"required input carries a claim with no string id: {REGISTER}")
    return register


def run() -> int:
    if not ARTIFACTS.is_dir():
        raise Refusal(f"required input directory is absent: {ARTIFACTS}")
    register = read_register()
    all_claims = [c for c in register["claims"] if not c["id"].startswith(SKIP_PREFIX)]
    claims = [c for c in all_claims if c.get("claimClass") != "decision"]
    decisions = [c for c in all_claims if c.get("claimClass") == "decision"]
    errors = unregistered_current_reviews(claims)
    rows = []
    for claim in sorted(claims, key=lambda item: item["id"]):
        shape = contract_shape(claim)
        review, row_errors = review_state(claim)
        errors.extend(f"{claim['id']}: {item}" for item in row_errors)
        errors.extend(f"{claim['id']}: derivation: {item}" for item in shape["errors"])
        rows.append((claim, shape, review))
    cross, cross_errors = cross_cutting_state(register)
    errors.extend(f"cross-cutting: {item}" for item in cross_errors)

    print(f"{'surface':<20} {'shape':>7} {'reviewed':>9} {'open':>5} {'seal-ready':>11}")
    for claim, shape, review in rows:
        print(f"  {claim['id']:<18} {shape['score']}/4"
              f" {'Y' if review['reviewed'] else '.':>9}"
              f" {len(review['openIds']):>5}"
              f" {'Y' if review['ready'] and shape['score'] == 4 else '.':>11}")
        if review["openIds"]:
            print("    open: " + ", ".join(review["openIds"]))

    # Where each shape figure came from, and what moved.  The figures above are
    # quoted in freeze section 3 and section 9.1; a reader whose output cannot be
    # reconciled to the artifacts is not an improvement over one that guesses.
    print("\n  contract-shape provenance (which document was scored, and the delta)")
    for claim, shape, _ in rows:
        delta = shape["score"] - shape["ownScore"]
        print(f"    {claim['id']:<24} {shape['source']:<32}"
              f" {shape['ownScore']}/4 -> {shape['score']}/4  {delta:+d}")
        derivation = shape["derivation"]
        if derivation:
            print(f"      effective contract = {derivation['predecessor']}"
                  f" @ {derivation['declaredDigest'][:16]}…"
                  f" + {derivation['operations']} declared operations")
            print(f"      digest verified before use:"
                  f" {derivation.get('measuredDigest', '(not reached)')[:16]}…")
        if shape["source"] != "own-keys" or delta:
            print(f"      schema keys: {shape['schemaKeys'] or '(none)'}")
            print(f"      golden arrays: "
                  + (", ".join(f"{key}={count}" for key, count in shape["goldenKeys"])
                     or "(none)")
                  + f"  total {shape['goldens']}")
    derived_rows = [r for r in rows if r[1]["source"] == "derivation"]
    unresolved_rows = [r for r in rows if "UNRESOLVED" in r[1]["source"]]
    print(f"    reach: {len(derived_rows)}/{len(rows)} surfaces scored from a resolved"
          " derivation;"
          f" {len(rows) - len(derived_rows) - len(unresolved_rows)}/{len(rows)}"
          " still scored by SCHEMA_RE/GOLDEN_RE over their own top-level key NAMES")
    print("    CMP-IR-01 is NOT closed: the rename half of the class is untouched."
          " A non-derived artifact that renames its schema section outside the"
          " alternation is still lost the way EVIDENCE was.")
    if unresolved_rows:
        print(f"    {len(unresolved_rows)} surface(s) declared a derivation that could"
              " NOT be resolved; each is a finding below and none was scored as if"
              " no derivation had been declared")

    shape_complete = sum(shape["score"] == 4 for _, shape, _ in rows)
    reviewed_complete = sum(review["reviewed"] for _, _, review in rows)
    seal_ready = sum(shape["score"] == 4 and review["ready"]
                     for _, shape, review in rows)
    product, product_skip = product_qualification()
    print(f"\n  contract-shape completeness: {shape_complete}/{len(rows)}")
    print(f"  independently reviewed completeness: {reviewed_complete}/{len(rows)}")
    print(f"  seal readiness: {seal_ready}/{len(rows)}")
    if product is not None:
        print(f"  product implementation/release qualification: {product['state']} "
              f"({product['demonstrated']}/{product['total']} required properties demonstrated)")
    else:
        print("  product implementation/release qualification: CLASS SKIPPED --"
              " THIS CLASS DID NOT RUN")
        print(f"    its input is missing: {product_skip}")
        print("    no product verdict is reported; an absent input is not a"
              " NOT-RELEASE-QUALIFIED measurement")
    print(f"  cross-cutting open findings: {len(cross['openIds'])}")
    if cross["openIds"]:
        print("    open: " + ", ".join(cross["openIds"]))
    if errors:
        print(f"  registry/instrument errors: {len(errors)}")
        for error in errors:
            print("    -", error)

    # Decision claims are reported through their implementing contracts, without
    # adding a fifth meaning of completeness.
    by_id = {claim["id"]: (shape, review) for claim, shape, review in rows}
    for decision in decisions:
        implementation = decision.get("implementedBy")
        if implementation in by_id:
            shape, review = by_id[implementation]
            print(f"  decision {decision['id']}: implemented by {implementation}; "
                  f"shape {shape['score']}/4, seal-ready={'yes' if review['ready'] else 'no'}")
        else:
            errors.append(f"decision {decision['id']} has no scored implementation")

    ok = (shape_complete == len(rows) and reviewed_complete == len(rows)
          and seal_ready == len(rows) and not cross["openIds"] and not errors)
    if not ok:
        return EXIT["FINDINGS"]
    if product is None:
        return EXIT["CLASS-SKIPPED"]
    return EXIT["GREEN"]


def usage() -> None:
    print("usage: python3 artifacts/check-completeness-v2.py"
          " [--selftest | --derivations]")
    print("exit codes:")
    for name, code in sorted(EXIT.items(), key=lambda item: item[1]):
        print(f"  {code}  {name}")


def main(argv: list[str]) -> int:
    known = {"--selftest", "--derivations"}
    unknown = [a for a in argv if a not in known]
    if unknown:
        print(f"BAD INVOCATION: unknown argument(s) {unknown}. THE CHECK DID NOT RUN.")
        usage()
        return EXIT["BAD-INVOCATION"]
    if "--selftest" in argv and "--derivations" in argv:
        print("BAD INVOCATION: --selftest and --derivations are separate modes."
              " THE CHECK DID NOT RUN.")
        usage()
        return EXIT["BAD-INVOCATION"]
    if "--selftest" in argv:
        try:
            return selftest()
        except Refusal as exc:
            print(f"SELFTEST-REFUSED: {exc}")
            print("SELFTEST-NOT-RUN: the mutation suite did not execute. This is not"
                  " a finding about any artifact.")
            return EXIT["SELFTEST-REFUSED"]
        except Exception as exc:  # noqa: BLE001
            print(f"SELFTEST-REFUSED: unexpected {type(exc).__name__}: {exc}")
            print("SELFTEST-NOT-RUN: the mutation suite did not execute. This is not"
                  " a finding about any artifact.")
            return EXIT["SELFTEST-REFUSED"]
    if "--derivations" in argv:
        return print_derivation_census()
    return run()


if __name__ == "__main__":
    # A CRASH MUST NOT READ AS A FINDING (freeze section 7.8, litmus D-6; section
    # 7.8.1).  Every abnormal exit below states, in words, that the check did not
    # run, and uses an exit code no green or findings run can produce.
    try:
        CODE = main(sys.argv[1:])
    except Refusal as EXC:
        print(f"REFUSED: {EXC}")
        print("THE CHECK DID NOT RUN. No statement is made about any artifact,"
              " surface or claim.")
        CODE = EXIT["REFUSED"]
    except Exception as EXC:  # noqa: BLE001
        print(f"REFUSED: unexpected {type(EXC).__name__}: {EXC}")
        print("THE CHECK DID NOT RUN. No statement is made about any artifact,"
              " surface or claim. This is an instrument defect, not a finding.")
        CODE = EXIT["REFUSED"]
    raise SystemExit(CODE)
