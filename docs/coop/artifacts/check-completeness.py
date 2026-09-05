#!/usr/bin/env python3
"""Report four different completion questions without conflating them.

  1. Contract-shape completeness: invariants + schema + goldens + checker.
  2. Independent-review completeness: a registered current review exists.
  3. Seal readiness: every registered finding has a final adjudication, no
     claim blocker remains, and the adjudication does not say DO-NOT-SEAL.
  4. Product qualification: live operability DEMONSTRATED release evidence.

Review files are data, not commentary.  A review applicable to a current binding
artifact must be registered in claim-register.currentReviewArtifacts.  Its
findings remain OPEN until a registered adjudication resolves or rejects every ID.

Usage: python3 artifacts/check-completeness.py [--selftest]
Exit: 0 only when contract shape, review and seal readiness are complete;
      product qualification is reported separately and does not self-seal design.
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

# `grammar` added 2026-08-03.  This predicate infers "the artifact carries a
# contract schema" from top-level KEY NAMES, which makes the measurement
# sensitive to renaming rather than to content.  EVIDENCE scored 4/4 while its
# schema was called `bundleSchema` and dropped to 3/4 when `evidence.v10` named
# the same thing `canonicalWireGrammar` -- a section that declares scalar
# encoding, record rules, a tag registry and record definitions, and is a
# stricter schema than the one it replaced.  The artifact did not regress; the
# regex lost it.
#
# Widening the alternation restores this instance and costs nothing measurable:
# across all 31 registered claims exactly one schema verdict changes, EVIDENCE
# via `canonicalWireGrammar`, with no other claim affected.  It does NOT fix the
# class -- the next artifact that names its schema something else will be missed
# the same way.  That limitation is named in IMPLEMENTATION-FREEZE §7 as
# `CMP-IR-01` rather than left for the next reader to rediscover.
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
#      loses it.  EVIDENCE scored 4/4 while its schema was `bundleSchema` and
#      fell to 3/4 when `evidence.v10` named the same thing `canonicalWireGrammar`.
#      Adding `grammar` to the alternation recovered that instance.  **This half
#      is NOT closed by the code below and is deliberately left standing**: every
#      artifact that declares no derivation is still scored by name, and the next
#      section that is renamed to something outside the alternation will still be
#      lost.  See `reach` in the printed output for the live split.
#
#   2. DERIVATION.  No alternation can reach this one.  `c2-plan-stage-schema.v9`
#      is a delta document: its own `derivedFrom.rule` states the effective
#      contract is the VERIFIED predecessor with the listed operations applied
#      "and nothing else. No byte of the predecessor is transcribed into this
#      file."  That is freeze §7.3's anti-transcription discipline, and its
#      consequence is that the delta file presents NO key to match -- not a
#      badly-named key, none at all.  Scoring the delta measures the delta; it
#      does not measure the contract.  The corpus's own discipline had made its
#      completeness instrument blind.
#
# The reader below resolves the declared derivation and scores the EFFECTIVE
# contract.  Four properties make that a measurement rather than a concession:
#
#   * It READS the declaration.  No predecessor path, digest or operation is
#     hardcoded here.  An artifact that declares no derivation is scored exactly
#     as it was before this change.
#   * It finds the declaration by SHAPE, not by the key name `derivedFrom`.
#     Locating the declaration by name would reproduce, one level up, the exact
#     naming fragility being repaired.  A declaration is a top-level object that
#     carries exactly one artifact filename, exactly one sha256, and exactly one
#     non-empty operation list.  Measured over all 371 artifact JSON documents in
#     this corpus this fires on exactly the five c2 delta documents (v5..v9) and
#     nothing else, with zero near-misses.
#   * It VERIFIES before it uses.  The predecessor is hashed and compared to the
#     declared digest before its bytes are parsed, and every `set` must restate
#     type-exactly the value it replaces -- the same rule `check-c2-v9.py`
#     applies to the same declaration.
#   * It NEVER degrades silently.  A missing predecessor, a digest mismatch, an
#     operation that does not describe the bytes it is applied to, an unknown
#     verb, an ambiguous declaration: each is a published finding that fails the
#     run.  The surface then reports `own-keys/DERIVATION-UNRESOLVED`, which
#     cannot manufacture a point, and the reason is printed.
#
# The effective contract is scored with the SAME two predicates used everywhere
# else.  A derivation whose effective contract does not carry a schema, or whose
# operations delete one, scores exactly as low as it deserves -- the selftest
# mutates precisely that case.
JSON_NAME_RE = re.compile(r"^[A-Za-z0-9._][A-Za-z0-9._/-]*\.json$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
# Dotted-dialect step grammar, same as check-c2-v9.py `_STEP_RE`, so this
# reader walks dotted paths the way the surface's own registered checker walks
# them.  RFC 6901 pointer paths and array-token paths are parsed by separate
# strict branches in `path_steps`, and a string parse must round-trip to the
# exact declared path (repair of 2026-08-12; see the corpus-resolution record).
STEP_RE = re.compile(r"\[(\d+)\]|\.?([^.\[\]]+)")
DERIVATION_OPS = ("set", "add")
DERIVATION_MAX_DEPTH = 8


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


def path_steps(path) -> list | None:
    """Steps of a declared operation path, or None when the path cannot be
    expressed in a grammar this reader walks.  Three dialects are read, each
    STRICTLY -- a string parse must round-trip to the exact declared path,
    because guessing at a malformed path is how a resolver invents a contract
    the artifact never declared.  Until 2026-08-12 this function did exactly
    that to RFC 6901 pointer paths, tokenising '/a/b' into ONE bogus step:
    every set then refused loudly, but an add would have SUCCEEDED by
    inventing a literal slash-named top-level key.  Measured in
    r1-lifetime-neutrality.conformance.v1.9.corpus-resolution.v1.json.

      ARRAY    ['a', 'b', 0] -- a string token is an object key, an int a
               zero-based index.  bool is tested BEFORE int because bool
               subclasses int, so [True] would otherwise be index 1.
      POINTER  '/a/b/0' -- RFC 6901.  '~1' -> '/', '~0' -> '~', any other '~'
               refuses; an empty token refuses; a token in array-index form
               (0|[1-9][0-9]*) is an integer index, so a dict keyed by such a
               numeric string is refused at walk time rather than guessed at.
      DOTTED   'a.b[0]' -- the original grammar, unchanged for every path it
               already parsed; a parse that does not round-trip now refuses
               instead of walking a guess."""
    if isinstance(path, list):
        if not path:
            return None
        for token in path:
            if isinstance(token, bool) or not isinstance(token, (str, int)):
                return None
            if isinstance(token, str) and not token:
                return None
            if isinstance(token, int) and token < 0:
                return None
        return list(path)
    if not isinstance(path, str) or not path:
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


def has_step(node: object, step: object) -> bool:
    if isinstance(node, dict):
        return isinstance(step, str) and step in node
    if isinstance(node, list):
        return isinstance(step, int) and 0 <= step < len(node)
    return False


def resolve_steps(root: object, steps: list) -> tuple[bool, object]:
    node = root
    for step in steps:
        if not has_step(node, step):
            return False, None
        node = node[step]
    return True, node


def is_operation_list(value: object) -> bool:
    """A list this reader can execute.  A path may be a non-empty string
    (pointer or dotted dialect) or a non-empty array of tokens; each operation
    is read on its own terms.  Widened 2026-08-12 from string-only, which made
    the array encoding invisible: the block was not recognised at all and the
    artifact silently fell back to key-name scoring -- the exact CMP-IR-01
    behaviour the array encoding was adopted to escape (freeze §7.3 rider)."""
    return (isinstance(value, list) and bool(value)
            and all(isinstance(item, dict) and isinstance(item.get("op"), str)
                    and ((isinstance(item.get("path"), str) and item.get("path"))
                         or (isinstance(item.get("path"), list)
                             and bool(item.get("path"))))
                    for item in value))


def operation_shaped(value: object) -> bool:
    """WEAK detection used ONLY by the refusal path, deliberately independent
    of `is_operation_list` -- a validity gate whose error branch shares its
    success branch's predicate cannot report the case where the predicate is
    wrong (freeze §7.3 rider, 2026-08-10)."""
    return (isinstance(value, list) and bool(value)
            and all(isinstance(item, dict) for item in value)
            and any("op" in item for item in value)
            and not is_operation_list(value))


def declaration_fields(block: dict) -> dict | None:
    """The three things a derivation must state, located by value shape."""
    names = [v for v in block.values()
             if isinstance(v, str) and JSON_NAME_RE.match(v)]
    digests = [v for v in block.values()
               if isinstance(v, str) and SHA256_RE.match(v)]
    operations = [v for v in block.values() if is_operation_list(v)]
    if len(names) == 1 and len(digests) == 1 and len(operations) == 1:
        return {"artifact": names[0], "sha256": digests[0],
                "operations": operations[0]}
    return None


def derivation_declaration(artifact: dict) -> tuple[dict | None, list[str]]:
    """(declaration, errors).  A block that looks like a derivation but does not
    state all three parts unambiguously is reported, never skipped quietly."""
    found: list[tuple[str, dict]] = []
    errors: list[str] = []
    for key, value in artifact.items():
        if not isinstance(value, dict):
            continue
        fields = declaration_fields(value)
        if fields is not None:
            found.append((key, fields))
            continue
        names = [v for v in value.values()
                 if isinstance(v, str) and JSON_NAME_RE.match(v)]
        digests = [v for v in value.values()
                   if isinstance(v, str) and SHA256_RE.match(v)]
        if any(is_operation_list(v) for v in value.values()) and (names or digests):
            errors.append(
                f"'{key}' carries an operation list and {len(names)} predecessor "
                f"name(s) and {len(digests)} digest(s); a derivation must state "
                "exactly one of each, so no effective contract can be materialised")
        elif (names or digests) and any(operation_shaped(v) for v in value.values()):
            errors.append(
                f"'{key}' states a predecessor identity and a list that declares "
                "operations, but this reader cannot execute that list (an "
                "operation's path must be a non-empty string or a non-empty array "
                "of tokens); no effective contract can be materialised, and the "
                "refusal is loud by design (2026-08-12)")
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
        kind, path = op.get("op"), op.get("path")
        where = f"operation {index} ({kind} {path})"
        if kind not in DERIVATION_OPS:
            errors.append(f"{where}: unknown verb; declared verbs are "
                          f"{list(DERIVATION_OPS)}")
            continue
        if "value" not in op:
            errors.append(f"{where}: carries no value")
            continue
        steps = path_steps(path)
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


def resolve_derivation(artifact_rel: str, declaration: dict,
                       seen: tuple[str, ...] = ()) -> tuple[object | None, dict, list[str]]:
    """Materialise the effective contract, or explain why it cannot be."""
    name = declaration["artifact"]
    parent_dir = pathlib.PurePosixPath(artifact_rel).parent
    candidates = [str(parent_dir / name)] if str(parent_dir) != "." else [name]
    if "/" in name:
        candidates.append(name)
    provenance = {"predecessor": candidates[0], "declaredDigest": declaration["sha256"],
                  "operations": len(declaration["operations"]), "depth": len(seen) + 1,
                  # Which path dialect(s) this declaration writes, so the next
                  # dialect is a census row rather than a surprise (2026-08-12).
                  "pathDialect": sorted({
                      "array-tokens" if isinstance(op.get("path"), list)
                      else "json-pointer" if isinstance(op.get("path"), str)
                      and op.get("path").startswith("/")
                      else "dotted"
                      for op in declaration["operations"]})}

    raw = None
    for candidate in candidates:
        raw = load_bytes(candidate)
        if raw is not None:
            provenance["predecessor"] = candidate
            break
    if raw is None:
        return None, provenance, [
            f"declared predecessor is absent: {candidates[0]}"]
    if len(seen) >= DERIVATION_MAX_DEPTH:
        return None, provenance, [
            f"derivation chain exceeds {DERIVATION_MAX_DEPTH} links"]
    if provenance["predecessor"] in seen:
        return None, provenance, [
            f"derivation chain revisits {provenance['predecessor']}"]

    actual = hashlib.sha256(raw).hexdigest()
    provenance["measuredDigest"] = actual
    if actual != declaration["sha256"]:
        return None, provenance, [
            f"predecessor digest mismatch for {provenance['predecessor']}: declared "
            f"{declaration['sha256']}, measured {actual}"]
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


def product_qualification() -> dict:
    op = load_path("artifacts/operability.v2.json") or {}
    decision = op.get("releaseDecision", {})
    total = len(op.get("requiredPropertyRegistry", {}).get("properties", []))
    demonstrated = decision.get("demonstratedPropertyCount", 0)
    return {
        "state": "RELEASE-QUALIFIED" if decision.get("state") == "RELEASABLE" else
                 "NOT-RELEASE-QUALIFIED",
        "demonstrated": demonstrated,
        "total": total,
    }


def derivation_selftest() -> tuple[bool, list[str]]:
    """Mutations a broken derivation resolver would fail.

    The interesting ones are not the malformed inputs -- they are the two at the
    end.  A resolver that trusted the declaration instead of scoring its result
    would keep awarding the schema point to a derivation that DELETES the schema,
    and would keep awarding the goldens point to one that empties the fixtures.
    That failure would manufacture seal-readiness out of a declaration, which is
    a worse defect than the blindness being repaired.
    """
    base = {
        "stageSchemas": {"kinds": {"probe": {"required": ["probeId"]}}},
        "planFixtures": [{"id": "a", "valid": True}, {"id": "b", "valid": False}],
        "version": 4,
        "enabled": True,
        # The live C-2 derivation edits nested paths
        # (`hostileScalarLeafTotality.contractRoot.containerPaths`,
        # `planIntent.integerConstantRegisterV8`), so the nested walk is exercised
        # here rather than trusted.
        "counters": {"contractRoot": {"containerPaths": 794}},
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
    files = {"artifacts/base.json": raw}
    documents = {
        "preserving": delta(bump),
        "renamed-declaration": delta(bump, key="materialisedFrom"),
        "wrong-digest": delta(bump, sha=zero),
        "missing-predecessor": delta(bump, name="absent.json"),
        "altered-operations": delta([{"op": "set", "path": "version",
                                      "from": 99, "value": 9}]),
        "coerced-from": delta([{"op": "set", "path": "enabled",
                                "from": 1, "value": False}]),
        # Deliberately at a path the predecessor does NOT hold, so only the verb
        # gate can refuse it.  Aimed at an existing path it would be caught by
        # the add-collision gate instead and the verb gate would go untested.
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
        # --- dialects repaired 2026-08-12 ------------------------------------
        "pointer-preserving": delta([{"op": "set", "path": "/version",
                                      "from": 4, "value": 9}]),
        "pointer-nested": delta([
            {"op": "set", "path": "/counters/contractRoot/containerPaths",
             "from": 794, "value": 797},
            {"op": "add", "path": "/stageSchemas/kinds/rule-evaluation",
             "value": {"forbidden": ["operator"]}}]),
        "pointer-index": delta([{"op": "set", "path": "/planFixtures/1/valid",
                                 "from": False, "value": True}]),
        "pointer-add-top": delta([{"op": "add", "path": "/extraFixtures",
                                   "value": [{"id": "c"}]}]),
        "array-preserving": delta([{"op": "set", "path": ["version"],
                                    "from": 4, "value": 9}]),
        "array-bool-token": delta([{"op": "set",
                                    "path": ["planFixtures", True, "valid"],
                                    "from": False, "value": True}]),
        "pointer-bad-escape": delta([{"op": "set", "path": "/ver~2sion",
                                      "from": 4, "value": 9}]),
        "guessed-path-add": delta([{"op": "add", "path": "]extraFixtures[",
                                    "value": [{"id": "c"}]}]),
        "unreadable-operations": {"artifact": "delta", "derivedFrom": {
            "artifact": "base.json", "sha256": digest,
            "operations": [{"op": "set", "path": 7, "from": 4, "value": 9}]}},
    }
    paths = {f"artifacts/{name}.json": doc for name, doc in documents.items()}

    original_load, original_bytes = globals()["load_path"], globals()["load_bytes"]
    globals()["load_path"] = lambda rel: copy.deepcopy(paths.get(rel))
    globals()["load_bytes"] = lambda rel: files.get(rel)
    try:
        def shape(name):
            return contract_shape({
                "id": name, "invariants": ["i"],
                "bindingArtifact": f"artifacts/{name}.json",
                "validator": "artifacts/check-completeness.py"})
        measured = {name: shape(name) for name in documents}
        # Resolve two documents directly so the effective bytes -- not just the
        # score -- can be asserted, including that one resolution cannot leak
        # into another through a shared mutable base.
        effective = {}
        for name in ("nested-paths", "preserving", "pointer-nested",
                     "pointer-add-top"):
            rel = f"artifacts/{name}.json"
            declaration, _ = derivation_declaration(paths[rel])
            effective[name], _, _ = resolve_derivation(rel, declaration)
    finally:
        globals()["load_path"] = original_load
        globals()["load_bytes"] = original_bytes

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

    checks = [
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
        # ---- dialects repaired 2026-08-12 ----------------------------------
        (resolved("pointer-preserving", True, 2, 4),
         "accept  RFC 6901 POINTER path resolves (dialect repair)",
         "ESCAPE  a pointer-form derivation was refused -- the dialect gap is back"),
        (resolved("pointer-nested", True, 2, 4)
         and effective["pointer-nested"]["counters"]["contractRoot"]["containerPaths"] == 797
         and "rule-evaluation" in effective["pointer-nested"]["stageSchemas"]["kinds"]
         and exact_equal(effective["pointer-nested"], effective["nested-paths"]),
         "accept  nested POINTER set/add land, exactly equal to the dotted spelling",
         "FAIL    the pointer and dotted spellings of one derivation diverged"),
        (resolved("pointer-index", True, 2, 4),
         "accept  POINTER numeric token addresses a list index",
         "FAIL    a pointer index token was not walked"),
        (resolved("pointer-add-top", True, 3, 4)
         and "extraFixtures" in effective["pointer-add-top"]
         and "/extraFixtures" not in effective["pointer-add-top"],
         "accept  POINTER add lands on the named key, never on a literal '/key'",
         "ESCAPE  a pointer add invented a literal slash-named key -- the silent hazard"),
        (resolved("array-preserving", True, 2, 4),
         "accept  ARRAY-form path is now read (the silent (None, []) class closes)",
         "ESCAPE  an array-form derivation is still invisible to this reader"),
        (refused("array-bool-token", "path is not plainly resolvable"),
         "reject  array token True is not index 1 -- bool before int",
         "ESCAPE  a bool token was coerced to an array index"),
        (refused("pointer-bad-escape", "path is not plainly resolvable"),
         "reject  pointer with an undefined '~' escape",
         "ESCAPE  a malformed pointer escape was guessed at"),
        (refused("guessed-path-add", "path is not plainly resolvable"),
         "reject  add whose path parses only by GUESSING -- refusal, not invention",
         "ESCAPE  a non-round-tripping path was walked on a guess"),
        (measured["unreadable-operations"]["source"] == "own-keys/DERIVATION-UNRESOLVED"
         and any("cannot execute that list" in item
                 for item in measured["unreadable-operations"]["errors"]),
         "reject  operation-shaped list with an unreadable path is LOUD, not silent",
         "ESCAPE  an unreadable operation list fell back to key-name scoring"),
    ]
    lines = [f"  {ok_text}" if ok else f"  {bad_text}" for ok, ok_text, bad_text in checks]
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
    return 0 if ok else 1


def main() -> int:
    if "--selftest" in sys.argv:
        return selftest()
    register = json.loads(REGISTER.read_text())
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
    # quoted in freeze §3 and §9.1; a reader whose output cannot be reconciled
    # to the artifacts is not an improvement over one that guesses.
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
    product = product_qualification()
    print(f"\n  contract-shape completeness: {shape_complete}/{len(rows)}")
    print(f"  independently reviewed completeness: {reviewed_complete}/{len(rows)}")
    print(f"  seal readiness: {seal_ready}/{len(rows)}")
    print(f"  product implementation/release qualification: {product['state']} "
          f"({product['demonstrated']}/{product['total']} required properties demonstrated)")
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
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
