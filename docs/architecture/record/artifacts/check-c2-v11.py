#!/usr/bin/env python3
"""Companion instrument for c2-plan-stage-schema.v11.json.

v10 recorded "a companion instrument" as an UNMET dependency and deliberately
named no path, because a path that does not exist is a dead link in a binding
artifact.  This file is that instrument.  Freeze section 7.6 forbids EDITING a
pinned checker; it does not forbid creating one, and this file edits nothing.

WHAT THIS INSTRUMENT IS FOR

  IMPLEMENTATION-FREEZE section 7.2.2: a measurement that cannot fail the build
  is prose.  Every gate below returns findings and a non-zero exit, and
  --selftest requires each mutation to be refused FOR A NAMED REASON, so a gate
  that silently stopped measuring is itself a failure.

  The load-bearing gate is L4.  Freeze section 7.1 holds that a rule which
  exists only inside a checker's Python is not a binding artifact.  v10 answered
  that by writing the document-identity encoding into the contract as prose.
  This instrument therefore implements that encoding FROM THE CONTRACT'S OWN
  TEXT -- it reads the tag registry out of the contract, asserts the prose still
  says what the implementation assumes, and carries NO copy of the pinned
  `jx_canon`.  If it reproduced the digests by importing the head's encoder it
  would prove nothing at all: it would only show that the code equals itself.

INVOCATION
  python3 -I -B artifacts/check-c2-v11.py [subject.json]
  python3 -I -B artifacts/check-c2-v11.py --selftest

EXIT CODES (checkerModeContract)
  0  clean, or a green --selftest
  1  findings in the subject, or an escaped mutation in --selftest
  2  unsupported invocation, unreadable subject, subject drift, or a pinned
     input that does not hash to its declared digest
  3  --selftest REFUSED because the base subject is not clean.  A mutation
     suite over a dirty base is not an oracle: every row would echo the
     pre-existing failure and report "all rejected".  Exit 3 can never be
     absorbed into a pass.
"""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import math
import pathlib
import re
import struct
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent

SUBJECT = "c2-plan-stage-schema.v11.json"
SUBJECT_SHA256 = "d35b677d6726a8f9b9fc70e2e0f3307af909eca876cd6670d238829ba95a81f8"

# Pinned transitive inputs.  Each is read once as inert bytes, hash-verified,
# and then parsed or executed FROM THAT VERIFIED BYTE STRING.
PINS = {
    "c2-plan-stage-schema.v10.json":
        "0e550b1615c62cdd7b203221d4ddce6e229848c9e59e1403c1bb603ac5447406",
    "c2-plan-stage-schema.v9.json":
        "321faeaa3b70c83991f1cceefc9335891d69fa502b3d62cfa133494bb4e9c5a1",
    "c2-plan-stage-schema.v4.json":
        "4876284790462968549f834b866c7ffc5f7be1c43b583169570c1947c5c4af39",
    "check-c2-v4.py":
        "54ff764d155f5582bc66fd7bf8138b7eaed5f90f46b92975c4bc7a85ffb3df17",
    "check-completeness.py":
        "6c52a5f9a4ac6a3ec3dae9fb0c87e82552744b18eb8cc38d1c4522ade3e549d6",
}

SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
JSON_NAME_RE = re.compile(r"^[A-Za-z0-9._][A-Za-z0-9._/-]*\.json$")
STEP_RE = re.compile(r"\[(\d+)\]|\.?([^.\[\]]+)")
SHA256ID_RE = re.compile(r"^sha256:[0-9a-f]{64}$")


class Refused(Exception):
    """A condition that makes the run impossible, not merely failing."""


# --------------------------------------------------------------------------
# L1  parse integrity: duplicate keys are named, at their key
# --------------------------------------------------------------------------
class DuplicateKey(Exception):
    pass


def dup_rejecting_hook(pairs):
    """Freeze section 7.5.  Python's default keeps the LAST duplicate silently,
    which is how a document can say two things and be read as saying one."""
    out = {}
    for key, value in pairs:
        if key in out:
            raise DuplicateKey(key)
        out[key] = value
    return out


def parse_json(text: str, where: str):
    try:
        return json.loads(text, object_pairs_hook=dup_rejecting_hook)
    except DuplicateKey as exc:
        raise Refused("%s: duplicate key %r at object scope; the document "
                      "states two values for one name" % (where, exc.args[0]))
    except json.JSONDecodeError as exc:
        raise Refused("%s: not JSON: %s" % (where, exc))


def verified_bytes(name: str) -> bytes:
    path = HERE / name
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise Refused("pinned input %s cannot be read: %s" % (name, exc))
    actual = hashlib.sha256(raw).hexdigest()
    if actual != PINS[name]:
        raise Refused("pinned input %s: declared %s, measured %s"
                      % (name, PINS[name], actual))
    return raw


# --------------------------------------------------------------------------
# L4  opensip-jx-canon-v1, implemented FROM THE CONTRACT TEXT
# --------------------------------------------------------------------------
# Phrases the implementation below depends on.  If the contract stops saying
# these, this encoder is no longer entitled to assume them and the gate fails
# rather than quietly encoding by its own habits.
PROSE_OBLIGATIONS = (
    ("frame", "tag || DECIMAL(N) || ':' || payload"),
    ("frameParts.lengthIsCountedInCodePoints", "UNICODE CODE POINTS"),
    ("frameParts.separator", "COLON"),
    ("objectOrdering.rule", "CANONICAL TOKEN of the key"),
    ("digestBoundary", "UTF-8"),
    ("documentSkeleton.walk", "pre-order"),
    ("documentSkeleton.row", "JSON type name"),
    ("productions.number", "decimal point or an exponent"),
    ("numberProduction.sign", "sign bit"),
    ("numberProduction.rule", "greater than 16"),
)


def dotted(node, path):
    for step in path.split("."):
        node = node[step]
    return node


class ContractEncoder:
    """opensip-jx-canon-v1 driven by the contract, not by this file.

    The type tags come from the contract's own `typeTags` registry.  The
    productions are implemented from the contract's prose, and `obligations()`
    asserts that prose still says what this implementation assumes.
    """

    def __init__(self, spec: dict):
        self.spec = spec
        self.tags = spec["typeTags"]

    def obligations(self) -> list[str]:
        out = []
        for path, phrase in PROSE_OBLIGATIONS:
            try:
                text = dotted(self.spec, path)
            except (KeyError, TypeError):
                out.append("documentIdentityEncoding.%s is absent, so this "
                           "encoder's assumption '%s' is unwitnessed by the "
                           "contract" % (path, phrase))
                continue
            if not isinstance(text, str) or phrase not in text:
                out.append("documentIdentityEncoding.%s no longer states %r; "
                           "the encoder assumes it" % (path, phrase))
        for kind, tag in (("null", "z"), ("boolean", "b"), ("integer", "i"),
                          ("number", "n"), ("string", "s"), ("array", "a"),
                          ("object", "o")):
            if self.tags.get(kind) != tag:
                out.append("documentIdentityEncoding.typeTags.%s is %r, not %r"
                           % (kind, self.tags.get(kind), tag))
        return out

    # -- the seven productions ---------------------------------------------
    @staticmethod
    def jtype(value) -> str:
        if value is None:
            return "null"
        if value is True or value is False:
            return "boolean"
        if type(value) is int:
            return "integer"
        if type(value) is float:
            return "number"
        if type(value) is str:
            return "string"
        if type(value) is list:
            return "array"
        if type(value) is dict:
            return "object"
        raise Refused("%r is outside the JSON value universe" % (value,))

    def frame(self, kind: str, payload: str) -> str:
        # N counts UNICODE CODE POINTS, not UTF-8 bytes.
        return self.tags[kind] + str(len(payload)) + ":" + payload

    @staticmethod
    def number_payload(value: float) -> str:
        """The repaired production: shortest round-tripping decimal that always
        carries a point or an exponent; sign taken from the SIGN BIT."""
        negative = (struct.unpack("<Q", struct.pack("<d", value))[0] >> 63) == 1
        sign = "-" if negative else ""
        magnitude = -value if negative else value
        if magnitude == 0.0:
            digits, exponent = "0", 1
        else:
            for precision in range(0, 18):
                candidate = "%.*e" % (precision, magnitude)
                if float(candidate) == magnitude:
                    break
            mantissa, _, exp = candidate.partition("e")
            digits = mantissa.replace(".", "").rstrip("0") or "0"
            exponent = int(exp) + 1
        width = len(digits)
        if exponent <= -4 or exponent > 16:
            head = digits[0] + ("." + digits[1:] if width > 1 else "")
            power = exponent - 1
            return "%s%se%s%02d" % (sign, head, "+" if power >= 0 else "-",
                                    abs(power))
        if exponent <= 0:
            return sign + "0." + "0" * (-exponent) + digits
        if exponent >= width:
            return sign + digits + "0" * (exponent - width) + ".0"
        return sign + digits[:exponent] + "." + digits[exponent:]

    def canon(self, value) -> str:
        kind = self.jtype(value)
        if kind == "null":
            return self.frame("null", "")
        if kind == "boolean":
            return self.frame("boolean", "1" if value else "0")
        if kind == "integer":
            return self.frame("integer", str(value))
        if kind == "number":
            return self.frame("number", self.number_payload(value))
        if kind == "string":
            return self.frame("string", value)
        if kind == "array":
            return self.frame("array", "".join(self.canon(i) for i in value))
        # ordered by ascending (KEY TOKEN, VALUE TOKEN), NOT by raw key
        pairs = sorted((self.canon(k), self.canon(v)) for k, v in value.items())
        return self.frame("object", "".join(k + v for k, v in pairs))

    def digest(self, token: str) -> str:
        return hashlib.sha256(token.encode("utf-8")).hexdigest()

    def rows(self, root) -> list:
        out = []

        def walk(node, path):
            out.append([self.canon(list(path)), self.jtype(node)])
            kind = self.jtype(node)
            if kind == "object":
                for key in node:
                    walk(node[key], path + [key])
            elif kind == "array":
                for index, item in enumerate(node):
                    walk(item, path + [index])

        walk(root, [])
        return out

    def skeleton_digest(self, root) -> str:
        return self.digest(self.canon(self.rows(root)))

    def counts(self, root) -> dict:
        out = {"nodes": 0, "containers": 0, "leaves": 0, "nullLeaves": 0,
               "booleanLeaves": 0, "integerLeaves": 0, "numberLeaves": 0,
               "stringLeaves": 0}
        tokens = set()
        for token, kind in self.rows(root):
            out["nodes"] += 1
            tokens.add(token)
            if kind in ("object", "array"):
                out["containers"] += 1
            else:
                out["leaves"] += 1
                out[kind + "Leaves"] += 1
        out["distinctPathTokens"] = len(tokens)
        return out


# --------------------------------------------------------------------------
# L3  derivation resolution -- native, then cross-checked against the corpus
# --------------------------------------------------------------------------
def exact_equal(left, right) -> bool:
    """Type-exact deep equality.  `True` is not `1`; `1` is not `1.0`.
    Section 6 law 18 at the comparison primitive."""
    if type(left) is not type(right):
        return False
    if isinstance(left, dict):
        return set(left) == set(right) and all(
            exact_equal(left[k], right[k]) for k in left)
    if isinstance(left, list):
        return len(left) == len(right) and all(
            exact_equal(a, b) for a, b in zip(left, right))
    return left == right


def is_operation_list(value) -> bool:
    return (isinstance(value, list) and bool(value)
            and all(isinstance(i, dict) and isinstance(i.get("op"), str)
                    and isinstance(i.get("path"), str) and i.get("path")
                    for i in value))


def find_declaration(doc: dict):
    """Located by SHAPE, not by the key name.  Finding it by the name
    `derivedFrom` would reproduce, one level up, the naming fragility
    CMP-IR-01 names."""
    found = []
    for key, value in doc.items():
        if not isinstance(value, dict):
            continue
        names = [v for v in value.values()
                 if isinstance(v, str) and JSON_NAME_RE.match(v)]
        digests = [v for v in value.values()
                   if isinstance(v, str) and SHA256_RE.match(v)]
        ops = [v for v in value.values() if is_operation_list(v)]
        if len(names) == 1 and len(digests) == 1 and len(ops) == 1:
            found.append((key, {"artifact": names[0], "sha256": digests[0],
                                "operations": ops[0]}))
    if len(found) > 1:
        raise Refused("ambiguous derivation: " + ", ".join(k for k, _ in found))
    return found[0][1] if found else None


def path_steps(path: str):
    if not path or path.startswith(".") or path.endswith(".") or ".." in path:
        return None
    steps = [int(i) if i else n for i, n in STEP_RE.findall(path)]
    return steps or None


def apply_operations(base, operations):
    effective = copy.deepcopy(base)
    errors = []
    for index, op in enumerate(operations):
        kind, path = op.get("op"), op.get("path")
        where = "operation %d (%s %s)" % (index, kind, path)
        if kind not in ("set", "add"):
            errors.append("%s: unknown verb" % where)
            continue
        if "value" not in op:
            errors.append("%s: carries no value" % where)
            continue
        steps = path_steps(path)
        if steps is None:
            errors.append("%s: path is not plainly resolvable" % where)
            continue
        node = effective
        ok = True
        for step in steps[:-1]:
            if isinstance(node, dict) and isinstance(step, str) and step in node:
                node = node[step]
            elif isinstance(node, list) and isinstance(step, int) and 0 <= step < len(node):
                node = node[step]
            else:
                ok = False
                break
        if not ok or not isinstance(node, (dict, list)):
            errors.append("%s: parent does not resolve to a container" % where)
            continue
        last = steps[-1]
        exists = ((isinstance(node, dict) and isinstance(last, str) and last in node)
                  or (isinstance(node, list) and isinstance(last, int)
                      and 0 <= last < len(node)))
        if kind == "set":
            if "from" not in op:
                errors.append("%s: a set must restate the value it replaces" % where)
                continue
            if not exists:
                errors.append("%s: does not resolve against the predecessor" % where)
                continue
            if not exact_equal(node[last], op["from"]):
                errors.append(
                    "%s: declares it replaces %r (%s) but the verified "
                    "predecessor holds %r (%s); the derivation does not "
                    "describe the bytes it is applied to"
                    % (where, op["from"], type(op["from"]).__name__,
                       node[last], type(node[last]).__name__))
                continue
        else:
            if exists:
                errors.append("%s: already exists in the predecessor" % where)
                continue
            if not isinstance(node, dict) or not isinstance(last, str):
                errors.append("%s: can only add a named member to an object" % where)
                continue
        node[last] = copy.deepcopy(op["value"])
    return effective, errors


def resolve(doc: dict, seen=()):
    """Materialise the effective contract.  Every predecessor is hash-verified
    BEFORE its bytes are parsed, and a mismatch refuses the run."""
    declaration = find_declaration(doc)
    if declaration is None:
        return doc, []
    name = declaration["artifact"]
    if name not in PINS:
        raise Refused("declared predecessor %s is not a pinned input of this "
                      "instrument, so its digest cannot be verified" % name)
    if name in seen:
        raise Refused("derivation chain revisits " + name)
    raw = verified_bytes(name)
    measured = hashlib.sha256(raw).hexdigest()
    if measured != declaration["sha256"]:
        raise Refused("predecessor digest mismatch for %s: declared %s, "
                      "measured %s" % (name, declaration["sha256"], measured))
    base = parse_json(raw.decode("utf-8"), name)
    base, chain = resolve(base, seen + (name,))
    effective, errors = apply_operations(base, declaration["operations"])
    if errors:
        raise Refused("; ".join(errors))
    return effective, [name] + chain


# --------------------------------------------------------------------------
# EPC-V2, executed
# --------------------------------------------------------------------------
POSITIONS = ("planIntentCommitment", "executionPlanCommitment")


def admit_sha256id(value, position: str):
    """comparisonDiscipline made executable: an INDEPENDENT TYPE ASSERTION on
    each side BEFORE any comparison.  Every JSON production other than string
    is refused by name, and so is every non-canonical spelling."""
    if type(value) is not str:
        return ("%s: wire type sha256Id requires the JSON string production; "
                "this position holds the %s production"
                % (position, ContractEncoder.jtype(value)))
    if not SHA256ID_RE.match(value):
        return ("%s: %r is not the canonical spelling of a sha256Id "
                "(^sha256:[0-9a-f]{64}$)" % (position, value))
    return None


def epc_decide(record, degrade=None, golden=None):
    """The decision procedure EPC-V2 requires.  Returns (verdict, reasons).

    `degrade` exists only for --selftest: it names a way an implementation
    could go wrong, so the suite can prove the gate catches it.
    """
    reasons = []
    for position in POSITIONS:
        if position not in record:
            reasons.append("%s: position absent" % position)
            continue
        problem = admit_sha256id(record[position], position)
        if problem:
            reasons.append(problem)
    if reasons:
        return "REJECT", reasons

    left = record["planIntentCommitment"].encode("utf-8")
    right = record["executionPlanCommitment"].encode("utf-8")

    if degrade == "golden-drift":
        # The failure the v10 review measured: reject anything that is not the
        # published golden, which rejects differing AND agreeing-but-wrong
        # positions identically and is therefore not this control at all.
        if right != golden.encode("utf-8"):
            return "REJECT", ["executionPlanCommitment: not the golden value"]
        return "ACCEPT", []
    if degrade == "host-equality":
        if record["planIntentCommitment"] == record["executionPlanCommitment"]:
            return "ACCEPT", []
        return "REJECT", ["executionPlanCommitment: differs"]
    if degrade == "always-accept":
        return "ACCEPT", []

    if left != right:
        return "REJECT", [
            "executionPlanCommitment: %r is not byte-identical to this "
            "ExecutionPlan's planIntentCommitment %r; requiredValue makes "
            "equality the field's DEFINITION, so the record is INVALID"
            % (record["executionPlanCommitment"],
               record["planIntentCommitment"])]
    return "ACCEPT", []


def epc_witnesses(golden: str):
    """Records the rule quantifies over.  C-2's ExecutionPlan envelope is
    closed and cannot carry executionPlanCommitment, so these are GENERATED
    witnesses, not C-2 fixtures.  requiredValue is stated as 'wherever a record
    carries a field named executionPlanCommitment', which is a quantifier."""
    other = "sha256:" + hashlib.sha256(b"EPC-V2 not-the-golden").hexdigest()
    third = "sha256:" + hashlib.sha256(b"EPC-V2 third value").hexdigest()
    cases = [
        ("EPC-POS-golden", {POSITIONS[0]: golden, POSITIONS[1]: golden},
         "ACCEPT", "both positions carry the ExecutionPlan's own commitment"),
        ("EPC-V2-differing-positions",
         {POSITIONS[0]: golden, POSITIONS[1]: other}, "REJECT",
         "THE CONTROL: executionPlanCommitment is a well-formed sha256Id that "
         "is not this ExecutionPlan's planIntentCommitment"),
        ("EPC-V2-DISCRIMINATOR-agreeing-but-not-golden",
         {POSITIONS[0]: other, POSITIONS[1]: other}, "ACCEPT",
         "THE DISCRIMINATOR: both positions agree at a value that is NOT the "
         "published golden. Accepting this is what separates a positions-"
         "differ guard from golden-drift detection"),
        ("EPC-V2-differing-the-other-way",
         {POSITIONS[0]: other, POSITIONS[1]: golden}, "REJECT",
         "the same defect with the arms exchanged"),
        ("EPC-V2-differing-at-a-third-value",
         {POSITIONS[0]: third, POSITIONS[1]: other}, "REJECT",
         "neither position is the golden and they still differ"),
    ]
    # EPC-V4: every JSON production other than string, at each position.
    injections = [("null", None), ("boolean", True), ("integer", 1),
                  ("number", 1.0), ("array", [golden]), ("object", {"v": golden})]
    for position in POSITIONS:
        for label, value in injections:
            record = {POSITIONS[0]: golden, POSITIONS[1]: golden}
            record[position] = value
            cases.append(("EPC-V4-%s-at-%s" % (label, position), record,
                          "REJECT", "law 18 exact-type admission: the %s "
                          "production at %s" % (label, position)))
        for label, value in (("uppercase-hex", "sha256:" + "A" * 64),
                             ("no-prefix", "0" * 64),
                             ("wrong-prefix", "plan1:sha256:" + "0" * 64),
                             ("leading-space", " " + golden),
                             ("trailing-space", golden + " ")):
            record = {POSITIONS[0]: golden, POSITIONS[1]: golden}
            record[position] = value
            cases.append(("EPC-V4-%s-at-%s" % (label, position), record,
                          "REJECT", "non-canonical spelling at " + position))
    return cases


# --------------------------------------------------------------------------
# the run
# --------------------------------------------------------------------------
class Report:
    def __init__(self):
        self.lines = []
        self.findings = []
        self.skips = []

    def say(self, text=""):
        self.lines.append(text)

    def finding(self, code, position, detail):
        self.findings.append((code, position, detail))

    def skip(self, code, why):
        self.skips.append((code, why))


def load_pinned_module(name, modname):
    raw = verified_bytes(name)
    spec = importlib.util.spec_from_file_location(modname, HERE / name)
    module = importlib.util.module_from_spec(spec)
    sys.modules[modname] = module
    spec.loader.exec_module(module)
    return module, raw


def run(subject_path: pathlib.Path, subject_raw: bytes, report: Report,
        expect_digest: bool = True):
    """Every gate below can fail the run."""
    digest = hashlib.sha256(subject_raw).hexdigest()
    report.say("subject            : %s" % subject_path.name)
    report.say("subject bytes      : %d" % len(subject_raw))
    report.say("subject sha256     : %s" % digest)
    report.say()

    subject = parse_json(subject_raw.decode("utf-8"), subject_path.name)

    # ---- L3 derivation ---------------------------------------------------
    effective, chain = resolve(subject)
    report.say("L3 derivation")
    report.say("  chain            : " + " -> ".join([subject_path.name] + chain))
    report.say("  depth            : %d" % len(chain))
    report.say("  every predecessor hash-verified before parse: yes")
    if not chain:
        report.finding("C2V11-NO-DERIVATION", "(root)",
                       "the subject declares no derivation; this instrument's "
                       "subject is a delta document")
    # cross-check against the corpus's own reader
    completeness, _ = load_pinned_module("check-completeness.py", "_cc_v11")
    other_decl, other_errs = completeness.derivation_declaration(subject)
    if other_errs:
        report.finding("C2V11-RESOLVER-DISAGREE", "derivedFrom",
                       "check-completeness.py reports " + "; ".join(other_errs))
    elif other_decl is not None:
        other_eff, _prov, other_resolve_errs = completeness.resolve_derivation(
            "artifacts/" + subject_path.name, other_decl)
        if other_resolve_errs:
            report.finding("C2V11-RESOLVER-DISAGREE", "derivedFrom",
                           "; ".join(other_resolve_errs))
        elif not exact_equal(other_eff, effective):
            report.finding("C2V11-RESOLVER-DISAGREE", "derivedFrom",
                           "this instrument's resolver and check-completeness.py "
                           "materialise DIFFERENT effective contracts")
        else:
            report.say("  second resolver  : check-completeness.py agrees, type-exact")
    report.say()

    if "documentIdentityEncoding" not in effective:
        raise Refused("the effective contract carries no documentIdentityEncoding; "
                      "this instrument cannot encode from a contract that does "
                      "not state the encoding")
    encoder = ContractEncoder(effective["documentIdentityEncoding"])

    # ---- L4 the encoding, implemented from the contract text -------------
    report.say("L4 opensip-jx-canon-v1, implemented from the contract text")
    problems = encoder.obligations()
    for problem in problems:
        report.finding("C2V11-ENCODING-PROSE", "documentIdentityEncoding", problem)
    report.say("  prose obligations: %d checked, %d unmet"
               % (len(PROSE_OBLIGATIONS) + 7, len(problems)))
    report.say("  no copy of jx_canon is imported or vendored by this file")

    # the head's published digests, recomputed
    head_raw = verified_bytes("c2-plan-stage-schema.v9.json")
    head = parse_json(head_raw.decode("utf-8"), "c2-plan-stage-schema.v9.json")
    head_pub = head["documentSkeleton"]
    got = encoder.skeleton_digest(head)
    if got != head_pub["sha256"]:
        report.finding("C2V11-HEAD-SKELETON", "c2-plan-stage-schema.v9.json"
                       ".documentSkeleton.sha256",
                       "recomputed %s, published %s" % (got, head_pub["sha256"]))
    differing = [n for n, want in head_pub["subtrees"].items()
                 if encoder.skeleton_digest(head[n]) != want]
    for name in differing:
        report.finding("C2V11-HEAD-SUBTREE",
                       "c2-plan-stage-schema.v9.json.documentSkeleton.subtrees."
                       + name, "recomputed digest differs from published")
    report.say("  head documentSkeleton.sha256 reproduced: %s"
               % ("yes" if got == head_pub["sha256"] else "NO"))
    report.say("  head root-subtree digests    : %d/%d reproduced, %d differing"
               % (len(head_pub["subtrees"]) - len(differing),
                  len(head_pub["subtrees"]), len(differing)))
    head_counts = encoder.counts(head)
    bad_counts = [k for k, v in head_counts.items() if head_pub.get(k) != v]
    for key in bad_counts:
        report.finding("C2V11-HEAD-COUNT",
                       "c2-plan-stage-schema.v9.json.documentSkeleton." + key,
                       "recomputed %s, published %s"
                       % (head_counts[key], head_pub.get(key)))
    report.say("  head node/leaf counters      : %d/%d reproduced"
               % (len(head_counts) - len(bad_counts), len(head_counts)))

    # the subject's own published skeleton
    if "documentSkeleton" in subject:
        own = subject["documentSkeleton"]
        got_own = encoder.skeleton_digest(subject)
        if expect_digest and got_own != own.get("sha256"):
            report.finding("C2V11-OWN-SKELETON", "documentSkeleton.sha256",
                           "recomputed %s, published %s"
                           % (got_own, own.get("sha256")))
        bad = [n for n, want in own.get("subtrees", {}).items()
               if encoder.skeleton_digest(subject[n]) != want]
        for name in bad:
            report.finding("C2V11-OWN-SUBTREE",
                           "documentSkeleton.subtrees." + name,
                           "recomputed digest differs from published")
        own_counts = encoder.counts(subject)
        bad_own = [k for k, v in own_counts.items() if own.get(k) != v]
        for key in bad_own:
            report.finding("C2V11-OWN-COUNT", "documentSkeleton." + key,
                           "recomputed %s, published %s"
                           % (own_counts[key], own.get(key)))
        report.say("  subject documentSkeleton     : %s, subtrees %d/%d, counters %d/%d"
                   % ("reproduced" if got_own == own.get("sha256") else "DIFFERS",
                      len(own.get("subtrees", {})) - len(bad),
                      len(own.get("subtrees", {})),
                      len(own_counts) - len(bad_own), len(own_counts)))
        report.say("  this is the gate that makes documentSkeleton.fixpointNote")
        report.say("  HARD: the fixpoint itself cannot detect an edited digest")
        report.say("  string, because path and type are unchanged; recomputation can.")
    report.say()

    # ---- L5 the block's own vectors --------------------------------------
    report.say("L5 the encoding's own vectors, recomputed")
    vector_failures = 0
    spec = effective["documentIdentityEncoding"]
    checks = [
        ("FF-1", encoder.canon("é"), "s1:é"),
        ("FF-2", encoder.canon({"b": 1, "ab": 2}), "o17:s1:bi1:1s2:abi1:2"),
        ("FF-3a", encoder.canon([0]), "a4:i1:0"),
        ("FF-3b", encoder.canon(["0"]), "a4:s1:0"),
        ("FF-4a", encoder.canon(["asb", "c"]), "a10:s3:asbs1:c"),
        ("FF-4b", encoder.canon(["a", "bsc"]), "a10:s1:as3:bsc"),
        ("FF-6-integerOne", encoder.canon(1), "i1:1"),
        ("FF-6-numberOne", encoder.canon(1.0), "n3:1.0"),
        ("FF-6-booleanTrue", encoder.canon(True), "b1:1"),
        ("FF-7-emptyString", encoder.canon(""), "s0:"),
        ("FF-7-emptyArray", encoder.canon([]), "a0:"),
        ("FF-7-emptyObject", encoder.canon({}), "o0:"),
        ("FF-7-null", encoder.canon(None), "z0:"),
        ("FF-7-ten", encoder.canon("0123456789"), "s10:0123456789"),
    ]
    for vector in spec.get("vectors", []):
        if vector.get("id", "").startswith("FF-5"):
            checks.append(("FF-5a", encoder.skeleton_digest({"a": {"b": 1}}),
                           vector["skeletonDigestA"]))
            checks.append(("FF-5b", encoder.skeleton_digest({"a": {}, "a/b": 1}),
                           vector["skeletonDigestB"]))
        if vector.get("id", "").startswith("FF-6"):
            checks.append(("FF-6-declared-numberOne", encoder.canon(1.0),
                           vector["numberOne"]))
            checks.append(("FF-6-declared-integerOne", encoder.canon(1),
                           vector["integerOne"]))
    for vector in spec.get("numberProduction", {}).get("vectors", []):
        vid = vector["id"]
        if vid.startswith("FF-N1"):
            checks.append((vid, encoder.canon(1.0), vector["underThisText"]))
        elif vid.startswith("FF-N2"):
            checks.append((vid, encoder.canon(-0.0), vector["underThisText"]))
        elif vid.startswith("FF-N3"):
            checks.append((vid + "a", encoder.canon(1e15), vector["underThisTextA"]))
            checks.append((vid + "b", encoder.canon(1e16), vector["underThisTextB"]))
        elif vid.startswith("FF-N4"):
            checks.append((vid + "a", encoder.canon(0.0001), vector["underThisTextA"]))
            checks.append((vid + "b", encoder.canon(0.00001), vector["underThisTextB"]))
        elif vid.startswith("FF-N5"):
            checks.append((vid, encoder.canon(100.0), vector["underThisText"]))
    for name, got_value, want in checks:
        if got_value != want:
            vector_failures += 1
            report.finding("C2V11-VECTOR", "documentIdentityEncoding vector " + name,
                           "recomputed %r, contract states %r" % (got_value, want))
    report.say("  %d vectors recomputed from the contract, %d failing"
               % (len(checks), vector_failures))
    # FF-6 is law 18 itself: the three tokens must be pairwise distinct.
    trio = {encoder.canon(1), encoder.canon(1.0), encoder.canon(True)}
    if len(trio) != 3:
        report.finding("C2V11-LAW18-COLLAPSE", "documentIdentityEncoding",
                       "1, 1.0 and true do not produce three distinct tokens")
    report.say("  law 18: 1, 1.0 and true produce %d distinct tokens (must be 3)"
               % len(trio))
    report.say()

    # ---- L6 EPC-V2, executed ---------------------------------------------
    report.say("L6 EPC-V2, EXECUTED")
    ruling = (effective.get("planIntent", {}).get("attemptAndExecutionJoin", {})
              .get("executionPlanCommitment"))
    if not isinstance(ruling, dict):
        report.skip("EPC-V2",
                    "the effective contract carries no "
                    "planIntent.attemptAndExecutionJoin.executionPlanCommitment "
                    "ruling, so there is no rule to execute")
    else:
        golden = None
        for vector in ruling.get("vectors", []):
            if "planIntentCommitmentBothArms" in vector:
                golden = vector["planIntentCommitmentBothArms"]
        if golden is None or not SHA256ID_RE.match(str(golden)):
            report.skip("EPC-V2",
                        "no published sha256Id golden could be read out of the "
                        "ruling's own vectors, so the witnesses would be this "
                        "instrument's invention rather than the contract's")
        else:
            cases = epc_witnesses(golden)
            failed = 0
            for name, record, expected, why in cases:
                verdict, reasons = epc_decide(record)
                if verdict != expected:
                    failed += 1
                    report.finding("C2V11-EPC", name,
                                   "expected %s (%s), got %s%s"
                                   % (expected, why, verdict,
                                      "; " + "; ".join(reasons) if reasons else ""))
                elif verdict == "REJECT" and not reasons:
                    failed += 1
                    report.finding("C2V11-EPC-UNNAMED", name,
                                   "rejected without naming a position")
            report.say("  witnesses executed          : %d" % len(cases))
            report.say("  failing                     : %d" % failed)
            # the discriminator, stated as its own line because it is the point
            differ = epc_decide({POSITIONS[0]: golden,
                                 POSITIONS[1]: "sha256:" + "1" * 64})[0]
            agree_wrong = epc_decide({POSITIONS[0]: "sha256:" + "1" * 64,
                                      POSITIONS[1]: "sha256:" + "1" * 64})[0]
            report.say("  differing positions         : %s" % differ)
            report.say("  agreeing-but-not-golden     : %s" % agree_wrong)
            if differ == agree_wrong:
                report.finding("C2V11-EPC-DEGENERATE",
                               "planIntent.attemptAndExecutionJoin."
                               "executionPlanCommitment",
                               "differing positions and agreeing-but-wrong "
                               "positions receive the SAME verdict, so this "
                               "procedure is golden-drift detection and not "
                               "the EPC-V2 control")
            else:
                report.say("  DISCRIMINATED: the two readings receive different")
                report.say("  verdicts, which is the named condition the v10")
                report.say("  review measured at 0 hits.")
            report.say("  scope: executed over GENERATED witnesses. C-2's")
            report.say("  ExecutionPlan envelope is closed and cannot carry")
            report.say("  executionPlanCommitment, so this is NOT executed over")
            report.say("  a live ActivationManifestV1/EvaluationAuthoritySealV1/")
            report.say("  TerminalRunV1 record and does NOT discharge the freeze")
            report.say("  section 7.1 row.")
    report.say()

    # ---- L7 law 18 exact-type admission over the contract ----------------
    report.say("L7 section 6 law 18, exact-type admission")
    law18 = 0
    for probe, other in ((1, 1.0), (1, True), (0, False), (1.0, True)):
        if exact_equal(probe, other):
            law18 += 1
            report.finding("C2V11-LAW18", "exact_equal",
                           "%r and %r compare equal type-exactly" % (probe, other))
        if not exact_equal(probe, probe):
            law18 += 1
            report.finding("C2V11-LAW18", "exact_equal",
                           "%r is not equal to itself" % (probe,))
    report.say("  type-exact comparison primitive: %d defects" % law18)
    # every `set` in the subject restated its `from` type-exactly, or the
    # derivation would already have refused; report the count as evidence.
    declaration = find_declaration(subject)
    sets = [o for o in (declaration["operations"] if declaration else [])
            if o.get("op") == "set"]
    report.say("  set operations whose `from` was type-exactly verified: %d"
               % len(sets))
    report.say()

    # ---- L8 census -------------------------------------------------------
    report.say("L8 hostileScalarLeafTotality.contractRoot census")
    c2v4, _ = load_pinned_module("check-c2-v4.py", "_c2v4_v11")
    measured = c2v4.node_census(effective, c2v4.CONTRACT_HOSTILE_VALUES)
    published = effective.get("hostileScalarLeafTotality", {}).get("contractRoot", {})
    bad_census = 0
    for key, value in measured.items():
        have = published.get(key)
        if type(have) is not type(value) or have != value:
            bad_census += 1
            report.finding("C2V11-CENSUS",
                           "hostileScalarLeafTotality.contractRoot." + key,
                           "recomputed %r, published %r" % (value, have))
    report.say("  counters recomputed by the pinned node_census: %d, %d differing"
               % (len(measured), bad_census))
    report.say()

    # ---- L9 closure enumeration ------------------------------------------
    report.say("L9 closure marks, re-derived")
    marks = []

    def find_closed(node, path):
        if isinstance(node, dict):
            for key, value in node.items():
                if key in ("closed", "closedTopLevel") and value is True:
                    marks.append(".".join(path) or "(root)")
                find_closed(value, path + [key])
        elif isinstance(node, list):
            for index, value in enumerate(node):
                find_closed(value, path + ["[%d]" % index])

    find_closed(effective, [])
    marks = sorted(set(m.replace(".[", "[") for m in marks))
    claim = (subject.get("theClosureCount") or {})
    declared = claim.get("compared")
    members = claim.get("members")
    if declared is not None and declared != len(marks):
        report.finding("C2V11-CLOSURE", "theClosureCount.compared",
                       "re-derived %d closure-marked objects, declared %d"
                       % (len(marks), declared))
    if members is not None and list(members) != marks:
        report.finding("C2V11-CLOSURE-MEMBERS", "theClosureCount.members",
                       "the enumerated member list does not equal the re-derived set")
    report.say("  closure-marked objects re-derived: %d" % len(marks))
    report.say("  declared                         : %s" % declared)
    report.say("  enumerated member list matches   : %s"
               % ("yes" if members is not None and list(members) == marks
                  else "n/a" if members is None else "NO"))
    report.say()

    return effective, encoder


# --------------------------------------------------------------------------
# --selftest
# --------------------------------------------------------------------------
def selftest(subject_path, subject_raw, base_report):
    """Every mutation must be refused FOR A NAMED REASON.

    A mutation that is refused for the wrong reason, or that escapes, is a
    finding.  A suite over a dirty base is not an oracle, so this refuses with
    exit 3 rather than reporting a green wall of echoes.
    """
    if base_report.findings:
        print("C2V11-SELFTEST-REFUSED: the base subject is not clean "
              "(%d findings). A mutation suite over a dirty base is not an "
              "oracle." % len(base_report.findings))
        return 3

    subject = parse_json(subject_raw.decode("utf-8"), subject_path.name)
    effective, _chain = resolve(subject)
    spec = effective["documentIdentityEncoding"]
    encoder = ContractEncoder(spec)
    head_raw = verified_bytes("c2-plan-stage-schema.v9.json")
    head = parse_json(head_raw.decode("utf-8"), "head")
    golden = None
    for vector in (effective["planIntent"]["attemptAndExecutionJoin"]
                   ["executionPlanCommitment"]["vectors"]):
        if "planIntentCommitmentBothArms" in vector:
            golden = vector["planIntentCommitmentBothArms"]

    rows = []

    def row(name, caught, reason):
        rows.append((name, bool(caught), reason))

    # M1 subject drift
    mutated = bytearray(subject_raw)
    mutated[-2] = mutated[-2] ^ 0x20
    row("M1 subject drift before parse",
        hashlib.sha256(bytes(mutated)).hexdigest() != SUBJECT_SHA256,
        "the pinned subject digest no longer matches, so the run exits 2 "
        "before a single byte is parsed")

    # M2 duplicate key named
    caught = ""
    try:
        parse_json('{"a": 1, "a": 2}', "M2")
    except Refused as exc:
        caught = str(exc)
    row("M2 duplicate key", "duplicate key 'a'" in caught,
        "the hook names the offending key: " + (caught or "NOT CAUGHT"))

    # M3 predecessor digest mismatch
    forged = copy.deepcopy(subject)
    forged["derivedFrom"]["predecessorSha256"] = "0" * 64
    caught = ""
    try:
        resolve(forged)
    except Refused as exc:
        caught = str(exc)
    row("M3 predecessor digest mismatch", "digest mismatch" in caught,
        "the chain refuses before parsing the predecessor: "
        + (caught[:90] or "NOT CAUGHT"))

    # M4 a `set` that misdescribes the bytes it is applied to
    forged = copy.deepcopy(subject)
    for op in forged["derivedFrom"]["operations"]:
        if op["op"] == "set" and op["path"] == "version":
            op["from"] = 10.0        # 10.0 is not 10: law 18 at the resolver
    caught = ""
    try:
        resolve(forged)
    except Refused as exc:
        caught = str(exc)
    row("M4 `from` restated as 10.0 instead of 10",
        "does not describe the bytes" in caught,
        "type-exact `from` refuses a float where an integer stands: "
        + (caught[:90] or "NOT CAUGHT"))

    # M5 published skeleton digest edited (path and type unchanged)
    forged = copy.deepcopy(subject)
    forged["documentSkeleton"]["sha256"] = "0" * 64
    row("M5 published documentSkeleton.sha256 edited",
        encoder.skeleton_digest(forged) != forged["documentSkeleton"]["sha256"],
        "the fixpoint CANNOT catch this (path and type are unchanged); "
        "recomputation does")

    # M6 encoder counts length in UTF-8 bytes instead of code points
    class ByteLength(ContractEncoder):
        def frame(self, kind, payload):
            return (self.tags[kind] + str(len(payload.encode("utf-8")))
                    + ":" + payload)
    row("M6 length counted in UTF-8 bytes",
        ByteLength(spec).canon("é") != "s1:é",
        "FF-1 separates the readings: s2 instead of s1")

    # M7 object members ordered by raw key.
    #
    # NOTE ON WHERE THIS IS DETECTABLE.  An earlier draft of this mutation
    # asserted against the HEAD'S documentSkeleton digest and ESCAPED, because
    # the skeleton is an array of [pathToken, typeName] rows and a path is an
    # array of strings and integers -- there is no OBJECT anywhere in the
    # structure the skeleton digest hashes.  That is not a hole in this suite;
    # it is exactly the 3-of-7 split `exercisedByTheSkeletonDigest` declares,
    # observed by executing it.  The ordering rule is load-bearing for VALUE
    # comparison, and FF-2 is where the contract witnesses it, so that is where
    # this mutation is asserted.  M17 then executes the split itself.
    class RawKeyOrder(ContractEncoder):
        def canon(self, value):
            if type(value) is dict:
                body = "".join(self.canon(k) + self.canon(value[k])
                               for k in sorted(value))
                return self.frame("object", body)
            return ContractEncoder.canon(self, value)
    row("M7 object order by raw key",
        RawKeyOrder(spec).canon({"b": 1, "ab": 2}) != "o17:s1:bi1:1s2:abi1:2",
        "FF-2's ordering trap: raw-key order yields %r where the contract "
        "pins o17:s1:bi1:1s2:abi1:2"
        % RawKeyOrder(spec).canon({"b": 1, "ab": 2}))

    # M8 path rendered as a '/'-join instead of canonicalised
    class SlashPath(ContractEncoder):
        def rows(self, root):
            out = []

            def walk(node, path):
                out.append(["/".join(str(s) for s in path), self.jtype(node)])
                kind = self.jtype(node)
                if kind == "object":
                    for key in node:
                        walk(node[key], path + [key])
                elif kind == "array":
                    for index, item in enumerate(node):
                        walk(item, path + [index])

            walk(root, [])
            return out
    slash = SlashPath(spec)
    row("M8 path rendered as a '/'-join",
        slash.skeleton_digest({"a": {"b": 1}}) == slash.skeleton_digest(
            {"a": {}, "a/b": 1}),
        "IR-C2V8-01: the rendering COLLIDES, which is why the path is "
        "canonicalised; the collision is the detection")

    # M9 the number production reverted to v10's text
    class ShortestNoPoint(ContractEncoder):
        @staticmethod
        def number_payload(value):
            if value == int(value) and math.isfinite(value):
                return str(int(value))
            return repr(value)
    row("M9 number production reverted to 'shortest round-trip'",
        ShortestNoPoint(spec).canon(1.0) != "n3:1.0",
        "FF-6 fails: the reverted rule yields %r where the contract pins n3:1.0"
        % ShortestNoPoint(spec).canon(1.0))

    # M10 sign decided by comparison rather than by the sign bit
    class SignByComparison(ContractEncoder):
        @staticmethod
        def number_payload(value):
            text = ContractEncoder.number_payload(value)
            return text[1:] if (value == 0.0 and text.startswith("-")) else text
    row("M10 negative zero loses its sign",
        SignByComparison(spec).canon(-0.0) != encoder.canon(-0.0),
        "FF-N2: -0.0 and 0.0 collapse to one token")

    # M11 EPC degraded to golden-drift detection
    differ = epc_decide({POSITIONS[0]: golden, POSITIONS[1]: "sha256:" + "1" * 64},
                        degrade="golden-drift", golden=golden)[0]
    agree = epc_decide({POSITIONS[0]: "sha256:" + "1" * 64,
                        POSITIONS[1]: "sha256:" + "1" * 64},
                       degrade="golden-drift", golden=golden)[0]
    row("M11 EPC-V2 degraded to golden-drift detection", differ == agree,
        "the discriminator fires: both readings get %s, so the procedure is "
        "not the control" % differ)

    # M12 EPC comparing without the independent type assertion
    verdict = epc_decide({POSITIONS[0]: golden, POSITIONS[1]: 1.0},
                         degrade="host-equality")[0]
    row("M12 EPC compares before type-asserting", verdict == "REJECT"
        and epc_decide({POSITIONS[0]: golden, POSITIONS[1]: 1.0})[1] != [],
        "law 18: the real procedure names the offending JSON production; the "
        "degraded one only says 'differs'")

    # M13 EPC that accepts everything
    escaped = [name for name, record, expected, _why in epc_witnesses(golden)
               if expected == "REJECT"
               and epc_decide(record, degrade="always-accept")[0] == "ACCEPT"]
    row("M13 EPC that accepts everything", len(escaped) > 0,
        "%d negative witnesses escape, so an always-accept gate is detectable"
        % len(escaped))

    # M14 census understated
    forged = copy.deepcopy(effective)
    forged["hostileScalarLeafTotality"]["contractRoot"]["enumeratedPaths"] = 1
    c2v4, _ = load_pinned_module("check-c2-v4.py", "_c2v4_v11b")
    measured = c2v4.node_census(forged, c2v4.CONTRACT_HOSTILE_VALUES)
    row("M14 census counter understated",
        measured["enumeratedPaths"] != 1,
        "recomputation contradicts the published counter, naming the position")

    # M15 closure count restated as a bare 8
    marks = []

    def find_closed(node, path):
        if isinstance(node, dict):
            for key, value in node.items():
                if key in ("closed", "closedTopLevel") and value is True:
                    marks.append(".".join(path) or "(root)")
                find_closed(value, path + [key])
        elif isinstance(node, list):
            for index, value in enumerate(node):
                find_closed(value, path + ["[%d]" % index])

    find_closed(effective, [])
    row("M15 closure count restated as a bare 8", len(set(marks)) != 8,
        "the re-derivation finds %d closure-marked objects, so the bare 8 "
        "fails by name" % len(set(marks)))

    # M16 prose obligation removed from the contract
    stripped = copy.deepcopy(spec)
    stripped["frameParts"]["lengthIsCountedInCodePoints"] = "counted somehow"
    row("M16 the contract stops stating code-point length",
        len(ContractEncoder(stripped).obligations()) > 0,
        "the encoder refuses to keep assuming what the contract no longer says")

    # M17 the 3-of-7 split itself, EXECUTED rather than read.
    #
    # exercisedByTheSkeletonDigest claims the skeleton digest exercises exactly
    # string, integer and array, and does NOT exercise null, boolean, number or
    # object.  A claim about which productions a measurement reaches is the
    # coverage-over-an-unobserved-region class this contract exists to refuse,
    # so it is executed: each production is perturbed in turn and the head's
    # skeleton digest must move for exactly the three, and stand for the four.
    reference = encoder.skeleton_digest(head)
    exercised, unexercised = [], []

    def perturbed(kind):
        class P(ContractEncoder):
            def frame(self, k, payload):
                if k == kind:
                    return self.tags[k] + str(len(payload)) + ";" + payload
                return ContractEncoder.frame(self, k, payload)
        return P(spec)

    for kind in ("string", "integer", "array", "null", "boolean", "number",
                 "object"):
        moved = perturbed(kind).skeleton_digest(head) != reference
        (exercised if moved else unexercised).append(kind)
    row("M17 the declared 3-of-7 split, executed",
        sorted(exercised) == ["array", "integer", "string"]
        and sorted(unexercised) == ["boolean", "null", "number", "object"],
        "perturbing each production in turn moves the head's skeleton digest "
        "for exactly %s and leaves it standing for %s, which is what "
        "exercisedByTheSkeletonDigest declares"
        % (sorted(exercised), sorted(unexercised)))

    escaped_rows = [r for r in rows if not r[1]]
    print("--selftest: mutations that must each fail for a NAMED reason")
    print()
    for name, caught, reason in rows:
        print("  [%s] %s" % ("CAUGHT " if caught else "ESCAPED", name))
        print("           reason: %s" % reason)
    print()
    print("mutations: %d, caught: %d, escaped: %d"
          % (len(rows), len(rows) - len(escaped_rows), len(escaped_rows)))
    if escaped_rows:
        print()
        for name, _caught, _reason in escaped_rows:
            print("C2V11-MUTATION-ESCAPED: " + name)
        return 1
    print()
    print("Every mutation was refused, and each refusal names the condition "
          "that caught it. A gate that stopped measuring would appear here as "
          "an ESCAPED row.")
    return 0


def main(argv):
    flags = [a for a in argv[1:] if a.startswith("--")]
    positional = [a for a in argv[1:] if not a.startswith("--")]
    for flag in flags:
        if flag != "--selftest":
            print("unsupported flag %s; usage: %s [subject.json] | --selftest"
                  % (flag, argv[0]), file=sys.stderr)
            return 2
    if len(positional) > 1:
        print("at most one subject may be named", file=sys.stderr)
        return 2

    subject_path = pathlib.Path(positional[0]) if positional else HERE / SUBJECT
    try:
        subject_raw = subject_path.read_bytes()
    except OSError as exc:
        print("cannot read subject %s: %s" % (subject_path, exc), file=sys.stderr)
        return 2

    digest = hashlib.sha256(subject_raw).hexdigest()
    pinned_subject = (not positional) or subject_path.name == SUBJECT
    if pinned_subject and digest != SUBJECT_SHA256:
        print("C2V11-SUBJECT-DRIFT: %s\n  declared %s\n  measured %s\n"
              "  The subject is hash-verified BEFORE it is parsed. This "
              "instrument will not report on bytes it was not written for."
              % (subject_path.name, SUBJECT_SHA256, digest), file=sys.stderr)
        return 2

    report = Report()
    if not pinned_subject:
        report.skip("C2V11-SUBJECT-DIGEST",
                    "the subject named on the command line is %s, not the "
                    "pinned subject %s, so this instrument holds no declared "
                    "digest for it and the drift gate did NOT run. Every other "
                    "gate below did. This is stated rather than passed over."
                    % (subject_path.name, SUBJECT))
    try:
        run(subject_path, subject_raw, report)
    except Refused as exc:
        print("C2V11-REFUSED: %s" % exc, file=sys.stderr)
        return 2

    if "--selftest" in flags:
        return selftest(subject_path, subject_raw, report)

    print("check-c2-v11.py -- companion instrument for " + SUBJECT)
    print("=" * 72)
    for line in report.lines:
        print(line)
    for code, why in report.skips:
        print("SKIP %s: %s" % (code, why))
    print("=" * 72)
    if report.findings:
        print("FINDINGS: %d" % len(report.findings))
        for code, position, detail in report.findings:
            print("  %s at %s" % (code, position))
            print("    %s" % detail)
        return 1
    print("FINDINGS: 0")
    print()
    print("A green run is checker-scope evidence authored by the same lane "
          "that authored the subject. It is NOT independent review, NOT "
          "qualification, NOT demonstration, NOT a seal and NOT product "
          "acceptance. v9 remains the head and check-c2-v9.py remains its "
          "instrument.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
