#!/usr/bin/env python3
"""Executable agreement between the package's PROSE and the corpus it describes.

WHY THIS FILE EXISTS.

A blind implementer litmus recorded ten defects.  Five of them (D-6..D-10) share
one shape, and the shape is not "a document is wrong".  It is:

    a package document makes a statement ABOUT the corpus, and nothing
    compares that statement to the corpus.

IMPLEMENTATION-FREEZE.md section 7.2.2 already names the rule -- "a recorded
measurement must be compared to the measurement it records" -- and applies it to
checkers.  It had not been applied to the documents.  `check-package-coherence.py`
compares the two package documents to EACH OTHER and to disk digests; nothing
compared either of them to what the artifacts SAY.

The sharpest instance was D-7.  `v1-slice.md` is authority level 2 -- above the
freeze's own implementation mapping -- it is digest-pinned in freeze section 2,
and section 6 of it presents `A1-RI-04` (CI layer 4) as a decision that "remains
before freeze", binding an implementer to a two-branch interim posture whose
second branch ("fail admission when an analysis-affecting layer-4 key is
present") is the OPPOSITE of what the binding product packet decides.  Measured
when this file was written: NO CHECKER IN artifacts/ READ `v1-slice.md` AT ALL.
Its bytes were pinned and its content was unread.  The contradiction was
therefore not merely unrecorded -- it was unobservable.

WHAT THIS FILE DOES NOT DO -- deliberately, and for the reason
`check-package-coherence.py` gives for the same choice.

It does not pin `IMPLEMENTATION-FREEZE.md`, `IMPLEMENTER-BLUEPRINT.md` or
`v1-slice.md` by hash.  Those are the documents under comparison; pinning them
would make every legitimate edit a failure and would train the next author to
regenerate a pin instead of reading a diff.  Freeze section 2 makes the same
argument for why the freeze gets content anchors rather than a byte pin.

It pins exactly ONE file: `check-package-coherence.py`, because this file
EXECUTES it.  Freeze section 7.3 permits executing a verified closure and
requires the hash to be checked before the bytes run.  `NPA-3` reuses that
checker's own `reviews_naming` / `review_state_of` derivation rather than
reimplementing it, because the property `NPA-3` measures is precisely that the
documents disclose what THAT derivation finds.  A second, independently written
copy of the derivation could disagree with `PC-7` and the disagreement would be
invisible -- which is the defect class this file exists to close.

It holds no opinion about wording.  Every class below compares a DERIVED set
against a RECORDED set, in both directions, so a record that goes stale is a
finding in its own right.

THE SIX CLASSES.

  NPA-1  UNRECORDED-PACKET-DISAGREEMENT
         An authority document presents, under a heading that declares its
         contents unresolved, a decision the binding product packet marks
         DECIDED or CONFIRMED -- and freeze section 5.1's disagreement register
         does not record it (or records it at the wrong grade).

  NPA-2  STALE-DISAGREEMENT-RECORD
         The register records a disagreement the live bytes no longer show.
         Symmetry matters: an amended `v1-slice.md` must not leave a record
         asserting a contradiction that has been repaired.

  NPA-3  UNDISCLOSED-REJECT
         An artifact both package documents name, whose OWN independent review
         decides REJECT, is not disclosed together with that verdict in BOTH
         documents.  Freeze section 9.1 asserts "That silence is now repaired";
         until this class existed, nothing measured the repair.

  NPA-4  UNDECLARED-EXTERNAL-TOOL
         A retained checker that invokes an external binary -- directly, or
         through a checker whose bytes it compiles and executes -- is not named
         in the blueprint's environment-prerequisites table.  A checker that
         aborts before evaluating any contract property has measured nothing,
         and a signer who meets its exit 1 unaccounted reads it as a finding.

  NPA-5  ORACLE-SIGNATURE-UNRECORDED
         An export the D9 contract's own `referenceDerivation` names as the
         axes-to-class oracle is not recorded in the blueprint at the call
         signature the live module actually exposes.  The blueprint instructs an
         implementer to drive these five by name; three of them raise TypeError
         when driven the way the instruction reads.

  NPA-6  IRREPRODUCIBLE-GOLDEN-UNRECORDED
         A `PLAN-ID-V1` golden vector whose own bytes omit some of the contract's
         declared preimage fields is not recorded in the blueprint at its
         measured completeness.  "Both pinned vectors reproduce byte-exactly" is
         true of the arithmetic and silent about an unstated cross-artifact join.

SCOPE OF THE FINDING SET, stated because it is a judgement and not a measurement.

Freeze section 2 ranks `architecture/` narrative LAST and admits it "only where
it does not conflict with the binding set" -- a conflict there is pre-resolved by
rule.  `GORTEX-BORROW-REGISTER.md` "carries no ... product-disposition ...
authority of its own".  Neither is therefore a FINDING scope for NPA-1; both are
scanned and reported as OBSERVATIONS, so a reader still learns they disagree.
The finding scope is the three documents that carry authority: the freeze, the
blueprint, and `v1-slice.md`.

Exit codes
  0  no findings
  1  findings
  2  bad invocation, or a pinned executed input drifted
  3  --selftest did not execute its mutation suite
"""

from __future__ import annotations

import hashlib
import importlib.util
import inspect
import json
import pathlib
import re
import sys
from typing import Any, Callable

COOP = pathlib.Path(__file__).resolve().parent.parent
ARTIFACTS = COOP / "artifacts"

FREEZE = "IMPLEMENTATION-FREEZE.md"
BLUEPRINT = "IMPLEMENTER-BLUEPRINT.md"
SLICE = "v1-slice.md"
PACKET = "artifacts/product-dispositions.v1.json"

# The documents whose disagreement with the packet is a FINDING.  See the scope
# note in the module docstring: this is the set freeze section 2 ranks at or
# above "accepted product scope/dispositions", not a list of known defect sites.
AUTHORITY_DOCS = (FREEZE, BLUEPRINT, SLICE)

# The ONE executed input.  Freeze section 7.3: hash-verify before the bytes run.
# This is a pin on an instrument this file EXECUTES, not on a document it reads.
EXECUTED_PINS = {
    "artifacts/check-package-coherence.py":
        "8d56b5f56fed4fd031f4e9f602e63d4f90ac2a189e56b0b580498f20a107f2a6",
}

# A heading declares its contents unresolved.  These are structural phrases a
# document uses to say "this is not settled yet", not decision names.
UNRESOLVED_HEADING = re.compile(
    r"remain(?:s|ing)? before freeze"
    r"|open decision"
    r"|undecided"
    r"|pending decision"
    r"|decisions that remain"
    r"|not yet decided"
    r"|remain open",
    re.I,
)

# A row that BINDS an implementer to an interim posture is materially worse than
# one that merely mislabels a decision's status: the first can be built against.
NORMATIVE_MODAL = re.compile(r"\bmust\b", re.I)

KIND_CONTENT = "CONTENT"
KIND_STATUS = "STATUS"

# freeze section 5.1's register table.  Row shape:
#   | `DECISION-ID` | `document.md` | section | `KIND` | ... |
REGISTER_HEADING = re.compile(r"^#{2,4}\s*5\.1\b", re.M)
REGISTER_ROW = re.compile(
    r"^\|\s*`(?P<id>[A-Za-z0-9][A-Za-z0-9._-]*)`\s*"
    r"\|\s*`(?P<doc>[A-Za-z0-9][A-Za-z0-9._/-]*\.md)`\s*"
    r"\|[^|]*"
    r"\|\s*`(?P<kind>[A-Z-]+)`\s*\|",
    re.M,
)

ENV_HEADING = re.compile(r"^#{2,6}\s*.*environment prerequisites.*$", re.I | re.M)

EXTERNAL_CALL = re.compile(
    r"subprocess\.(?:run|Popen|check_output|check_call)\(\s*\[\s*(['\"])([^'\"]+)\1"
)
# argv[0] forms that are the running interpreter, not an external dependency.
INTERPRETER_ARGV0 = ("python3", "python", "sys.executable")

HEX64 = re.compile(r"[0-9a-f]{64}")

D9_CONTRACT = "artifacts/d9-exit-contract.v1.14.json"


class Reader:
    """Every byte this checker reads passes through here.

    The overlay exists so `--selftest` can mutate an input WITHOUT writing to
    the tree.  Freeze section 7.2 forbids editing reviewed bytes; a mutation
    suite that writes to disk to prove a guard fires is one interruption away
    from leaving the corpus mutated.
    """

    def __init__(self, overlay: dict[str, bytes] | None = None) -> None:
        self.overlay = dict(overlay or {})

    def read_bytes(self, rel: str) -> bytes:
        if rel in self.overlay:
            return self.overlay[rel]
        return (COOP / rel).read_bytes()

    def read_text(self, rel: str) -> str:
        return self.read_bytes(rel).decode("utf-8")

    def read_json(self, rel: str) -> Any:
        return json.loads(self.read_text(rel))


def add(findings: list[dict[str, str]], fid: str, statement: str, detail: str) -> None:
    findings.append({"id": fid, "statement": statement, "detail": detail})


# ---------------------------------------------------------------------------
# Shared derivations
# ---------------------------------------------------------------------------

def decided_ids(packet: Any) -> dict[str, str]:
    """Decision ids the packet has actually closed, with their chosen rule.

    Read from `$.decisions` by STATUS, never by position: an id parked in
    `$.pendingDecisions` (today `CD-RT-5`) is correctly open, and a narrative
    that calls it open is correct, not in disagreement.
    """
    out: dict[str, str] = {}
    for key, value in (packet.get("decisions") or {}).items():
        if not isinstance(value, dict):
            continue
        if str(value.get("status", "")).strip().upper() in ("DECIDED", "CONFIRMED"):
            out[key] = str(value.get("rule", ""))
    return out


def unresolved_sections(text: str) -> list[tuple[str, str]]:
    """(heading, body) for every section whose HEADING declares it unresolved.

    A section ends at the next heading of the same or higher level, so a
    subsection nested under an unresolved heading stays inside it.
    """
    out: list[tuple[str, str]] = []
    head: str | None = None
    level = 0
    buf: list[str] = []
    for line in text.splitlines():
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            depth, title = len(m.group(1)), m.group(2)
            if head is not None and depth <= level:
                out.append((head, "\n".join(buf)))
                head, buf = None, []
            if head is None and UNRESOLVED_HEADING.search(title):
                head, level, buf = title, depth, []
                continue
        if head is not None:
            buf.append(line)
    if head is not None:
        out.append((head, "\n".join(buf)))
    return out


def named_in(body: str, ident: str) -> list[str]:
    """Lines of `body` naming `ident` as a whole token."""
    pat = re.compile(r"(?<![A-Za-z0-9_-])" + re.escape(ident) + r"(?![A-Za-z0-9_-])")
    return [ln for ln in body.splitlines() if pat.search(ln)]


def derive_disagreements(rd: Reader, decided: dict[str, str], docs: tuple[str, ...]
                         ) -> dict[tuple[str, str], dict[str, str]]:
    """{(decision id, document): {kind, heading, line}} over `docs`.

    KIND is derived, not judged: a line carrying a normative modal BINDS an
    implementer to the interim posture and is graded CONTENT; a line that only
    files a closed decision under an unresolved heading is graded STATUS.
    """
    out: dict[tuple[str, str], dict[str, str]] = {}
    for rel in docs:
        try:
            text = rd.read_text(rel)
        except OSError:
            continue
        for heading, body in unresolved_sections(text):
            for ident in sorted(decided):
                lines = named_in(body, ident)
                if not lines:
                    continue
                kind = KIND_CONTENT if any(NORMATIVE_MODAL.search(ln) for ln in lines) \
                    else KIND_STATUS
                key = (ident, rel)
                if key not in out or kind == KIND_CONTENT:
                    out[key] = {
                        "kind": kind,
                        "heading": heading.strip(),
                        "line": max(lines, key=len).strip(),
                    }
    return out


def parse_register(freeze_text: str) -> dict[tuple[str, str], str]:
    """{(decision id, document): KIND} from freeze section 5.1.

    A row this parser cannot read is not silently accepted -- it simply does not
    enter the register, so the disagreement it was meant to record reads as
    UNRECORDED and NPA-1 fires.  That is the safe direction.
    """
    m = REGISTER_HEADING.search(freeze_text)
    if not m:
        return {}
    tail = freeze_text[m.end():]
    nxt = re.search(r"^#{1,4}\s", tail, re.M)
    section = tail[: nxt.start()] if nxt else tail
    return {(r.group("id"), r.group("doc")): r.group("kind")
            for r in REGISTER_ROW.finditer(section)}


def load_pinned_module(rd: Reader, rel: str, name: str) -> Any:
    """Hash-verify, then execute the verified bytes.  Never the other way round."""
    data = rd.read_bytes(rel)
    actual = hashlib.sha256(data).hexdigest()
    expected = EXECUTED_PINS[rel]
    if actual != expected:
        raise SystemExit(
            f"NPA-PIN {rel}: {actual} != {expected}\n"
            f"  This file EXECUTES that instrument, so freeze section 7.3 requires the\n"
            f"  hash to hold before the bytes run.  If the drift is a deliberate repair,\n"
            f"  re-pin here in the same change that made it; do not run against unverified\n"
            f"  bytes.  Exit 2."
        )
    module = importlib.util.module_from_spec(
        importlib.util.spec_from_loader(name, loader=None)
    )
    module.__file__ = str(COOP / rel)
    exec(compile(data.decode("utf-8"), str(COOP / rel), "exec", dont_inherit=True),
         module.__dict__)
    return module


def external_tool_closure(sources: dict[str, str]) -> dict[str, set[str]]:
    """{checker filename: external binaries it needs}, transitively.

    `check-rust-provider-protocol-v4.py` contains no `rg` call.  It compiles and
    executes v3, which does the same to v2, which shells out.  A census that read
    only direct call sites would report one dependent where three exist -- which
    is exactly the understatement this class was written to catch.
    """
    direct: dict[str, set[str]] = {}
    executes: dict[str, set[str]] = {}
    names = set(sources)
    for fname, src in sources.items():
        tools = {m.group(2) for m in EXTERNAL_CALL.finditer(src)}
        direct[fname] = {t for t in tools
                         if t not in INTERPRETER_ARGV0 and "executable" not in t}
        peers: set[str] = set()
        # Only a file that compiles or exec's source can inherit another's calls.
        if "exec_module" in src or re.search(r"\bexec\(\s*compile\(", src):
            for other in names:
                if other != fname and re.search(r"['\"]" + re.escape(other) + r"['\"]", src):
                    peers.add(other)
        executes[fname] = peers

    def walk(fname: str, seen: frozenset[str]) -> set[str]:
        if fname in seen:
            return set()
        seen = seen | {fname}
        out = set(direct.get(fname, ()))
        for peer in executes.get(fname, ()):
            out |= walk(peer, seen)
        return out

    return {f: walk(f, frozenset()) for f in sources}


def signature_literal(name: str, fn: Callable[..., Any]) -> str:
    params = ", ".join(inspect.signature(fn).parameters)
    return f"{name}({params})"


def resolve_dotted(module: Any, dotted: str) -> Any:
    obj: Any = module
    for part in dotted.split("."):
        obj = getattr(obj, part)
    return obj


def preimage_container(vector: dict[str, Any], field_names: set[str]) -> dict[str, Any]:
    """The vector's own input map: the direct child sharing most preimage names.

    Chosen by intersection rather than by key name because the two live vectors
    call it `input` and `planInputConstruction` respectively, and a third could
    call it something else again.
    """
    best: dict[str, Any] = {}
    best_score = -1
    for value in vector.values():
        if isinstance(value, dict):
            score = len(field_names & set(value))
            if score > best_score:
                best, best_score = value, score
    return best


# ---------------------------------------------------------------------------
# The check
# ---------------------------------------------------------------------------

def evaluate(rd: Reader) -> tuple[list[dict[str, str]], dict[str, Any], list[str]]:
    findings: list[dict[str, str]] = []
    observations: list[str] = []
    counts: dict[str, Any] = {}

    packet = rd.read_json(PACKET)
    decided = decided_ids(packet)
    freeze_text = rd.read_text(FREEZE)
    blueprint_text = rd.read_text(BLUEPRINT)

    counts["packetDecided"] = len(decided)
    counts["packetPending"] = len(packet.get("pendingDecisions") or {})

    # ---------------- NPA-1 / NPA-2 -------------------------------------
    derived = derive_disagreements(rd, decided, AUTHORITY_DOCS)
    register = parse_register(freeze_text)
    counts["authorityDocsScanned"] = len(AUTHORITY_DOCS)
    counts["disagreementsDerived"] = len(derived)
    counts["disagreementsRecorded"] = len(register)

    for key in sorted(derived):
        ident, doc = key
        info = derived[key]
        if key not in register:
            add(findings, "NPA-1-UNRECORDED-PACKET-DISAGREEMENT",
                "an authority document presents a decided packet row as unresolved, "
                "and freeze §5.1 does not record the disagreement",
                f"{doc} — heading {info['heading']!r} names `{ident}`, which "
                f"product-dispositions.v1.json#decisions.{ident} marks decided "
                f"(grade {info['kind']}); no §5.1 register row for "
                f"(`{ident}`, `{doc}`)")
        elif register[key] != info["kind"]:
            add(findings, "NPA-1-UNRECORDED-PACKET-DISAGREEMENT",
                "freeze §5.1 records a disagreement at a grade the live bytes "
                "no longer support",
                f"(`{ident}`, `{doc}`): register says {register[key]}, "
                f"measured {info['kind']} — the recorded line is {info['line'][:160]!r}")

    for key in sorted(register):
        if key not in derived:
            ident, doc = key
            add(findings, "NPA-2-STALE-DISAGREEMENT-RECORD",
                "freeze §5.1 records a disagreement the live bytes do not show",
                f"(`{ident}`, `{doc}`): no unresolved-headed section of {doc} names "
                f"`{ident}`, or the packet no longer marks it decided. A repaired "
                f"contradiction must have its record withdrawn, not left standing")

    # Narrative documents: reported, never a finding.  See the scope note.
    narrative = sorted(
        str(p.relative_to(COOP))
        for p in list(COOP.glob("*.md")) + list((COOP / "architecture").glob("*.md"))
        if str(p.relative_to(COOP)) not in AUTHORITY_DOCS
    )
    for key, info in sorted(derive_disagreements(rd, decided, tuple(narrative)).items()):
        observations.append(
            f"{key[1]}: names decided `{key[0]}` under {info['heading']!r} "
            f"(grade {info['kind']}) — narrative, ranked last by §2 and pre-resolved "
            f"by the authority order; recorded here, not raised")

    # ---------------- NPA-3 ---------------------------------------------
    pcm = load_pinned_module(rd, "artifacts/check-package-coherence.py", "npa_pcm")
    subjects = [
        p for p in sorted(ARTIFACTS.glob("*.json"))
        if not any(mark in p.name.lower() for mark in pcm.REVIEW_MARKERS)
        and p.name in freeze_text and p.name in blueprint_text
    ]
    counts["subjectsGraded"] = len(subjects)
    rejected = [p for p in subjects if pcm.review_state_of(p) == "REJECT"]
    counts["subjectsRejected"] = len(rejected)
    for path in rejected:
        stem = path.name[: -len(".json")]
        for doc, text in ((FREEZE, freeze_text), (BLUEPRINT, blueprint_text)):
            disclosed = any(
                re.search(r"REJECT", text[max(0, m.start() - 600): m.start() + 600])
                for m in re.finditer(re.escape(stem), text)
            )
            if not disclosed:
                add(findings, "NPA-3-UNDISCLOSED-REJECT",
                    "an artifact both documents name carries a REJECT on its own bytes "
                    "and one of them does not disclose it",
                    f"{path.name}: independent review decides REJECT; {doc} names it "
                    f"but never within 600 characters of the word REJECT. §2 rule 3 "
                    f"forbids implementing a REJECTED version, so a reader of that "
                    f"document alone cannot know")

    # ---------------- NPA-4 ---------------------------------------------
    sources = {p.name: p.read_text(encoding="utf-8", errors="replace")
               for p in sorted(ARTIFACTS.glob("check-*.py"))
               if p.name != pathlib.Path(__file__).name}
    closure = external_tool_closure(sources)
    env_section = ""
    m = ENV_HEADING.search(blueprint_text)
    if m:
        tail = blueprint_text[m.end():]
        nxt = re.search(r"^#{1,6}\s", tail, re.M)
        env_section = tail[: nxt.start()] if nxt else tail
    dependents = {f: t for f, t in closure.items() if t}
    counts["checkersScanned"] = len(sources)
    counts["externalToolDependents"] = len(dependents)
    counts["externalTools"] = sorted({t for ts in dependents.values() for t in ts})
    if dependents and not env_section:
        add(findings, "NPA-4-UNDECLARED-EXTERNAL-TOOL",
            "the blueprint has no environment-prerequisites section to declare in",
            f"{len(dependents)} checker(s) need an external binary and no heading "
            f"matching 'environment prerequisites' exists in {BLUEPRINT}")
    else:
        for fname in sorted(dependents):
            if fname not in env_section:
                add(findings, "NPA-4-UNDECLARED-EXTERNAL-TOOL",
                    "a checker needs an external binary the blueprint's environment "
                    "table does not name",
                    f"{fname} requires {sorted(dependents[fname])} "
                    f"(directly or through a checker whose bytes it executes) and is "
                    f"absent from the blueprint's environment-prerequisites section. "
                    f"Without the binary it aborts before evaluating any contract "
                    f"property, so its exit 1 measures nothing and must not be read "
                    f"as a finding")

    # ---------------- NPA-5 ---------------------------------------------
    contract = rd.read_json(D9_CONTRACT)
    ref = ""

    def first_impl(node: Any) -> str:
        """The `<path>.py::<export>+...` string under a referenceDerivation.

        The key holds a bare string in some revisions and an object with an
        `implementation` member in others, so the shape is discovered rather
        than assumed -- a reader that assumed one would report the contract as
        having no reference derivation, which is a false negative on the very
        field this class depends on.
        """
        if isinstance(node, str):
            return node if "::" in node else ""
        if isinstance(node, dict):
            for value in node.values():
                hit = first_impl(value)
                if hit:
                    return hit
        elif isinstance(node, list):
            for value in node:
                hit = first_impl(value)
                if hit:
                    return hit
        return ""

    def find_ref(node: Any) -> None:
        nonlocal ref
        if ref:
            return
        if isinstance(node, dict):
            for key, value in node.items():
                if key == "referenceDerivation":
                    hit = first_impl(value)
                    if hit:
                        ref = hit
                        return
                find_ref(value)
        elif isinstance(node, list):
            for value in node:
                find_ref(value)

    find_ref(contract)
    counts["oracleExports"] = 0
    if not ref or "::" not in ref:
        add(findings, "NPA-5-ORACLE-SIGNATURE-UNRECORDED",
            "the D9 contract no longer names a reference derivation",
            f"{D9_CONTRACT}: no `referenceDerivation` of the form "
            f"`artifacts/<checker>.py::<export>+<export>...` was found, so the "
            f"blueprint's port instruction has no subject to be checked against")
    else:
        mod_rel, exports = ref.split("::", 1)
        mod_rel = mod_rel.strip()
        names = [n.strip() for n in exports.split("+") if n.strip()]
        counts["oracleExports"] = len(names)
        oracle_path = COOP / mod_rel
        actual = hashlib.sha256(oracle_path.read_bytes()).hexdigest()
        # The expected digest is DERIVED from the package's own record, not
        # transcribed here: a pin copied into this file would advance silently
        # when the D9 head advances.
        recorded = set()
        for text in (freeze_text, blueprint_text):
            for hit in re.finditer(re.escape(oracle_path.name), text):
                window = text[max(0, hit.start() - 400): hit.start() + 400]
                recorded |= set(HEX64.findall(window))
        if actual not in recorded:
            add(findings, "NPA-5-ORACLE-SIGNATURE-UNRECORDED",
                "the D9 oracle on disk is not the one the package documents pin",
                f"{mod_rel}: live {actual}, recorded near its name {sorted(recorded)}")
        else:
            module = importlib.util.module_from_spec(
                importlib.util.spec_from_loader("npa_d9", loader=None))
            module.__file__ = str(oracle_path)
            exec(compile(oracle_path.read_bytes().decode("utf-8"), str(oracle_path),
                         "exec", dont_inherit=True), module.__dict__)
            for name in names:
                try:
                    fn = resolve_dotted(module, name)
                except AttributeError:
                    add(findings, "NPA-5-ORACLE-SIGNATURE-UNRECORDED",
                        "the D9 contract names an export the oracle does not have",
                        f"{mod_rel}: `{name}` is named by referenceDerivation and "
                        f"does not resolve on the executed module")
                    continue
                if not callable(fn):
                    continue
                literal = signature_literal(name, fn)
                if literal not in blueprint_text:
                    add(findings, "NPA-5-ORACLE-SIGNATURE-UNRECORDED",
                        "the blueprint tells an implementer to drive an oracle export "
                        "without recording the arity it actually has",
                        f"`{literal}` is the live signature and does not appear in "
                        f"{BLUEPRINT}. Driving it as the instruction reads raises "
                        f"TypeError before any golden is compared")

    # ---------------- NPA-6 ---------------------------------------------
    resolved = rd.read_json("artifacts/resolved-inputs.v2.json")
    plan = resolved.get("planIdContract") or {}
    field_names = {f.get("name") for f in (plan.get("preimageFields") or [])
                   if isinstance(f, dict)}
    field_names.discard(None)
    vectors = ((plan.get("goldenVectors") or {}).get("positive") or [])
    counts["preimageFields"] = len(field_names)
    counts["goldenVectors"] = len(vectors)
    for vector in vectors:
        if not isinstance(vector, dict):
            continue
        vid = str(vector.get("id") or "")
        container = preimage_container(vector, field_names)
        have = len(field_names & set(container))
        total = len(field_names)
        literal = (f"`{vid}` carries {have} of {total} `PLAN-ID-V1` preimage fields")
        stale = re.search(
            r"`" + re.escape(vid) + r"` carries (\d+) of (\d+) `PLAN-ID-V1` preimage fields",
            blueprint_text)
        if have < total and literal not in blueprint_text:
            add(findings, "NPA-6-IRREPRODUCIBLE-GOLDEN-UNRECORDED",
                "a PLAN-ID-V1 golden vector is not independently reproducible from its "
                "own bytes and the blueprint does not record that",
                f"`{vid}`: {have} of {total} preimage fields present; missing "
                f"{sorted(field_names - set(container))}. Reproducing it needs an "
                f"unstated cross-artifact join, so it is not evidence the recipe is "
                f"re-derivable from the package. Expected literal in {BLUEPRINT}: "
                f"{literal!r}")
        elif stale and (int(stale.group(1)), int(stale.group(2))) != (have, total):
            add(findings, "NPA-6-IRREPRODUCIBLE-GOLDEN-UNRECORDED",
                "the blueprint records a golden vector's completeness at a figure the "
                "live artifact contradicts",
                f"`{vid}`: blueprint says {stale.group(1)} of {stale.group(2)}, "
                f"measured {have} of {total}")

    return findings, counts, observations


# ---------------------------------------------------------------------------
# Non-vacuity: every class must be shown to fire, from outside itself
# ---------------------------------------------------------------------------

def selftest() -> int:
    base_findings, _, _ = evaluate(Reader())
    if base_findings:
        print("SELFTEST-REFUSED: base is not green, so an admitted mutation cannot be "
              "distinguished from a pre-existing finding")
        for f in base_findings:
            print(f"  {f['id']}: {f['detail'][:160]}")
        return 3

    freeze_text = (COOP / FREEZE).read_text(encoding="utf-8")
    blueprint_text = (COOP / BLUEPRINT).read_text(encoding="utf-8")

    # Each case: overlay -> the finding id it must produce.
    cases: list[tuple[str, str, dict[str, bytes]]] = []

    cases.append((
        "NPA-1-UNRECORDED-PACKET-DISAGREEMENT",
        "delete the §5.1 register heading",
        {FREEZE: freeze_text.replace("### 5.1", "### 5.1x", 1).encode()},
    ))
    cases.append((
        "NPA-1-UNRECORDED-PACKET-DISAGREEMENT",
        "downgrade a CONTENT register row to STATUS",
        {FREEZE: freeze_text.replace("| `CONTENT` |", "| `STATUS` |", 1).encode()},
    ))

    # A register row naming a decided id in a document that does not disagree.
    register_marker = REGISTER_ROW.search(freeze_text)
    if register_marker is None:
        print("SELFTEST-NOT-RUN: no §5.1 register row to mutate")
        return 3
    bogus = "| `P-1` | `IMPLEMENTER-BLUEPRINT.md` | §0 | `STATUS` | fabricated | x | x |\n"
    cases.append((
        "NPA-2-STALE-DISAGREEMENT-RECORD",
        "add a register row for a disagreement that does not exist",
        {FREEZE: freeze_text.replace(register_marker.group(0),
                                     register_marker.group(0) + "\n" + bogus, 1).encode()},
    ))

    cases.append((
        "NPA-3-UNDISCLOSED-REJECT",
        "strip every REJECT token from the blueprint",
        {BLUEPRINT: blueprint_text.replace("REJECT", "PASSED").encode()},
    ))

    env = ENV_HEADING.search(blueprint_text)
    if env is None:
        print("SELFTEST-NOT-RUN: no environment-prerequisites heading to mutate")
        return 3
    cases.append((
        "NPA-4-UNDECLARED-EXTERNAL-TOOL",
        "rename the environment-prerequisites heading",
        {BLUEPRINT: (blueprint_text[: env.start()] + "#### Notes\n"
                     + blueprint_text[env.end():]).encode()},
    ))

    cases.append((
        "NPA-5-ORACLE-SIGNATURE-UNRECORDED",
        "corrupt a recorded oracle signature",
        {BLUEPRINT: blueprint_text.replace("derive_codes(ax, maps)",
                                           "derive_codes(ax)").encode()},
    ))
    cases.append((
        "NPA-6-IRREPRODUCIBLE-GOLDEN-UNRECORDED",
        "corrupt the recorded golden-vector completeness figure",
        # Every recorded figure at once: a vector recorded complete goes stale
        # (NPA-6's second branch) and one recorded incomplete loses its required
        # literal (the first).  Mutating only the first match would rewrite
        # `13 of 13` to `13 of 13` and prove nothing -- which it did, once.
        {BLUEPRINT: re.sub(r"carries (\d+) of (\d+) `PLAN-ID-V1` preimage fields",
                           r"carries 99 of \2 `PLAN-ID-V1` preimage fields",
                           blueprint_text).encode()},
    ))

    escapes = 0
    print(f"SELFTEST: {len(cases)} mutations against a green base")
    for expected, label, overlay in cases:
        found, _, _ = evaluate(Reader(overlay))
        ids = {f["id"] for f in found}
        ok = expected in ids
        if not ok:
            escapes += 1
        print(f"  [{'REJECTED' if ok else 'ADMITTED'}] {expected}: {label}"
              + ("" if ok else f"  -- produced {sorted(ids) or 'nothing'}"))
    print()
    if escapes:
        print(f"SELFTEST FAILED: {escapes} mutation(s) admitted")
        return 1
    print(f"SELFTEST PASSED: {len(cases)}/{len(cases)} mutations rejected by the class "
          f"named for each; base green")
    print("  bound: mutations are applied to in-memory copies. Nothing is written to")
    print("  the tree, so this suite proves the classes FIRE, not that the tree is safe")
    print("  to edit -- run the checker normally after any edit.")
    return 0


def main(argv: list[str]) -> int:
    if not (sys.flags.isolated and sys.dont_write_bytecode):
        print("NPA-UNSUPPORTED-INVOCATION: run as `python3 -I -B "
              "artifacts/check-narrative-packet-agreement.py`")
        return 2
    if len(argv) > 2 or (len(argv) == 2 and argv[1] != "--selftest"):
        print("NPA-UNSUPPORTED-INVOCATION: accepts no arguments, or --selftest")
        return 2
    if len(argv) == 2:
        return selftest()

    reader = Reader()
    findings, counts, observations = evaluate(reader)

    print("NARRATIVE/PACKET AGREEMENT -- package prose <-> the corpus it describes")
    print()
    print("  inputs read as data:")
    for rel in (PACKET, FREEZE, BLUEPRINT, SLICE, D9_CONTRACT,
                "artifacts/resolved-inputs.v2.json"):
        digest = hashlib.sha256((COOP / rel).read_bytes()).hexdigest()
        print(f"    {rel:44s} {digest}")
    print()
    print("  input executed after hash verification (freeze §7.3):")
    for rel, pin in EXECUTED_PINS.items():
        print(f"    {rel:44s} {pin}")
    print()
    print("  measured this run:")
    for key in ("packetDecided", "packetPending", "authorityDocsScanned",
                "disagreementsDerived", "disagreementsRecorded", "subjectsGraded",
                "subjectsRejected", "checkersScanned", "externalToolDependents",
                "externalTools", "oracleExports", "preimageFields", "goldenVectors"):
        print(f"    {key:26s} {counts.get(key)}")
    if observations:
        print()
        print("  observations (narrative scope -- not findings):")
        for obs in observations:
            print(f"    {obs}")
    print()
    if not findings:
        print("OK: every derived disagreement is recorded, every record is live, and "
              "every")
        print("  document claim above is equal to the measurement it describes.")
        print("  scope: agreement only. Says nothing about whether a recorded")
        print("  disagreement is ACCEPTABLE -- freeze §2's authority order decides that,")
        print("  and §10 decides whether the narrative gets amended.")
        return 0
    print(f"FINDINGS: {len(findings)}")
    for f in findings:
        print(f"  {f['id']}: {f['statement']}")
        print(f"    {f['detail']}")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
