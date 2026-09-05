#!/usr/bin/env python3
"""EVIDENCE register-validator successor: check-evidence-v10.py re-pointed at
the DECIDED CD-RT-5 product state.

WHY THIS FILE EXISTS
--------------------
`check-evidence-v10.py` is the registered EVIDENCE validator
(`claim-register.v1.json` -> EVIDENCE.validator; blueprint section 1.1).  On
2026-08-05 the product authority `sfbreen` DECIDED `CD-RT-5`.  Applying that
decision moved `CD-RT-5` out of `product-dispositions.v1.json#pendingDecisions`
and into `#decisions`, so `check-retention-custody.py::_authority_guard` began
reporting

    RC-14: $product.CD-RT-5: exact live state must be BLOCKED_ON_PHASE_1A,
           got None
    RC-14: $contract.custodyPolicy: does not match live product authority

and `check-evidence-v10.py` went to exit 1 on four findings, all one cause:

    PR-07-RETAINED-LINEAGE-FOUNDATION       ValueError from v8's _rt_context()
    PR-08-RETAINED-LINEAGE-MUTATION-SUITE   ValueError from v8's _rt_context()
    PR-22-VERSIONING-CHECKER-GREEN          check-versioning-v8.py's two reds
    PR-26-RETAINED-PREDECESSOR-CHECKER-GREEN  v9 inheriting both of the above

The first two matter more than a finding count suggests.  `_rt_context()`
RAISES, and it is the memoised gate to the entire retained v8 foundation suite,
so PR-07 and PR-08 measured NOTHING - freeze section 7.4's rule applies
literally: a non-zero exit is not evidence a guard fired, and symmetrically an
abort is not evidence a probe ran.  A repair that merely suppressed those two
strings would have printed green over two unexecuted suites.

Section 7.2 forbids editing `check-evidence-v10.py`; section 7.6 records that
immutability then prevents a proven fix from propagating and names the
successor as the propagation mechanism.  This file is that successor.

WHAT CHANGED, AND ONLY WHAT CHANGED
-----------------------------------
1.  The stale live-state assertion is RE-POINTED, not removed.  Section 4.4 is
    this corpus's forensic record of a FABRICATED `CD-RT-5` sign-off; the guard
    is the only mechanical defence section 4.4 built, so deleting it would
    destroy the repair rather than complete it.  `cd_rt_5_findings()` asserts
    the CURRENT decided state - `status`, `decidedBy`, `decidedOn`,
    `durableDefault`, `implicitDurableRetention` - with a placeholder guard, a
    silent-revert guard, and a scoped re-implementation of RT10's
    manufactured-authority vocabulary walk.
2.  The RC-14 site is repaired where it lives, so the aborted suites RUN.
    `repaired_rt_context()` reproduces `check-evidence-v8.py::_rt_context()`
    call for call - the same five pin verifications, the same
    `rt13mod.regenerate`, the same frozen-closure equality, the same 23-unique-
    raw-object assertion - changing exactly one line: the RT13 finding list is
    compared against the enumerated accounted RC-14 propagation instead of
    against emptiness.  The result is installed as the v8 module's
    `_RT_CONTEXT`, so PR-07, PR-08 and PR-26 execute their full suites on the
    predecessor's own bytes.  MEASURED ONCE DURING AUTHORING, in an experiment
    this file does not re-run and a reader cannot re-derive from it: with this
    repair alone and step 3 omitted, 24 of 26 probes went green.  It is recorded
    as an authoring observation, not as a fact about the current tree.
3.  `check-versioning-v8.py` has no such seam, so its two dependency
    executions are wrapped: its module-level `module()` loader is substituted
    with one that removes EXACTLY the accounted RC-14 finding from EXACTLY the
    two checkers that carry it, and only while the live packet is in the pinned
    decided state.  Every level of the chain is separately executed and hard-
    compared against an enumerated expectation (`chain_audit`), so a NEW finding
    anywhere fails this checker rather than riding out with the accounted one.
    With both repairs, `check-evidence-v10.py` reports 0 findings, its full
    probe set is green, and NOTHING is subtracted at the v10 layer - the repair
    is entirely at the RC-14 site.  That is not narrated: `_probe_census`
    hard-compares the predecessor's own probe log against `PROBE_IDS` on every
    run and the banner prints the compared figure, so this paragraph cannot
    outlive the fact it states.
4.  `--selftest` and `--emit-candidate` and the argument battery are the
    predecessor's, executed as the predecessor's bytes.

READ THE PACKET, OR PIN IT?  THE PROPERTY IS PINNED; THE VALUES ARE NOT.
------------------------------------------------------------------------
This file's FIRST answer was to hard-pin the current values: the whole-file
digest of `product-dispositions.v1.json` plus five literal authority and
posture fields.  THAT ANSWER WAS WRONG, AND THE CORPUS FALSIFIED IT WITHIN THE
HOUR.  Forty minutes after those pins were measured, a coordinator repaired
three positions in the packet - `$.status`, `$.invariants[4]` and
`$.knownLimitations[0]` - which still asserted the pre-decision state while
`$.decisions.CD-RT-5` said `DECIDED`.  The repair was legitimate and did not
touch CD-RT-5.  MEASURED: the packet's whole-file digest moved
`5fc59ad2...` -> `bbe24527...` while the canonical digest of
`$.decisions.CD-RT-5` stayed IDENTICAL at `90a9dd06...`.  An instrument
written to survive the CD-RT-5 decision did not survive the next edit to the
same file, and its own remedy - "repair is a successor instrument" - would mint
a new checker per packet edit.

Three candidate answers, and why the third wins:

  * READ the packet and assert it against itself.  A tautology.  It cannot fail
    on `decidedBy: "[UNSET - the authority's name]"`, on a substituted
    authority, or on a blanked date - the three things section 4.4 exists to
    catch.  Rejected.
  * PIN THE CURRENT VALUES.  Catches all of those, and also fails on every
    legitimate edit to a file the corpus is explicitly waiting to change.
    Rejected by measurement, above.
  * PIN THE PROPERTY.  What the guard must know is not "the packet says
    sfbreen on 2026-08-05".  It is: CD-RT-5 is in exactly one state; if that
    state is decided then a NAMED AUTHORITY - not a coordinator, reviewer or
    lane - filled both authority fields, on a real calendar date that does not
    precede the packet itself, and the decision's own narrative CORROBORATES
    both; no field is an unfilled placeholder; the decision never manufactures
    a signature; the two posture fields agree with each other; and no other
    position in the packet still asserts the pre-decision state without marking
    it superseded.

Those properties survive the coordinator's repair, survive the next legitimate
amendment, and still fail on fabrication, on silent reversion, on `[UNSET]`
placeholders, on a single-field posture flip, and on an authority substituted
without rewriting the narrative that names it.

THE FAILURE MODE THIS ACCEPTS, stated plainly.  An amendment that changes BOTH
posture fields coherently, or substitutes an authority AND rewrites the
narrative to agree, is ADMITTED.  This file cannot distinguish a coherent lie
from the truth; freeze section 7.8 is exactly that boundary - these instruments
bind structure and type, never the truth of content.  What it will no longer do
is fail on a repair to a paragraph it is not the guard for.

The authored values are still recorded, as `AUTHORED_CD_RT_5` and
`AUTHORED_CD_RT_5_DIGEST`, and reported as NAMED NON-FATAL NOTICES
(`-CDRT5-DIGEST-MOVED`, `-CDRT5-VALUE-MOVED`) so a reader can tell "the packet
legitimately advanced" from "the packet is wrong" without re-deriving it by
hand.  They say so in their own text and they never change the exit code.
Section 7.2.2's rider is that a measurement which cannot fail the build is
prose: these are prose ON PURPOSE, and the properties above are what fail the
build.

WHAT A GREEN RUN IS (section 7.8)
----------------------------------
Author-side evidence that `evidence.v10.json` and its pinned closure say what
they say consistently, that the immutable RT/VERSIONING chain carries no
finding other than the accounted one, and that the live `CD-RT-5` record is
byte-for-byte the decision this file was written against.  It is NOT evidence
that any of those artifacts is right.  The measured ways this checker can pass
on a wrong artifact are enumerated in `KNOWN_PASSES_ON_WRONG_ARTIFACT` and
printed by `--selftest`.

Supported usage only:
  python3 -I -B artifacts/check-evidence-v11.py [candidate] [--selftest]
  python3 -I -B artifacts/check-evidence-v11.py --emit-candidate
Exit: 0 clean; 1 findings; 2 unsupported invocation/input; 3 selftest refused
      because the base candidate is not clean.
"""
from __future__ import annotations

import sys

_STARTUP_REFUSAL = (
    "EV11-UNSUPPORTED-INVOCATION: caller must use "
    "python3 -I -B artifacts/check-evidence-v11.py")
if sys.flags.isolated != 1 or not sys.flags.dont_write_bytecode:
    print(_STARTUP_REFUSAL, file=sys.stderr)
    raise SystemExit(2)

import ast
import copy
import hashlib
import importlib.util
import io
import json
import pathlib
import datetime
import re
import types
from contextlib import redirect_stdout
from typing import Any, Callable


HERE = pathlib.Path(__file__).resolve().parent
CHECKER = "check-evidence-v11.py"
BINDING = "evidence.v10.json"
PREDECESSOR_CHECKER = "check-evidence-v10.py"
LINEAGE_CHECKER = "check-evidence-v8.py"
INTERMEDIATE_CHECKER = "check-evidence-v9.py"
VERSIONING_CHECKER = "check-versioning-v8.py"
PRODUCT = "product-dispositions.v1.json"

# ---------------------------------------------------------------------------
# Pins.  Every digest below was measured from the live tree by this file's
# author at 2026-08-06T01:21:51Z and re-measured, unchanged, at
# 2026-08-06T02:32:03Z immediately before this file was finalised.
#
# product-dispositions.v1.json is deliberately NOT in this table.  It is the
# one input the corpus is actively changing, and a whole-file pin on it fired
# on a legitimate repair within the hour - see the read-vs-pin section of the
# module docstring.  The guard on it is a set of PROPERTIES, not a digest.
#
# `check-evidence-v10.py` verifies its own 24 pins before executing anything,
# so the digests repeated here are the ones THIS file's own reasoning depends
# on: the predecessor itself, the binding product packet the re-pointed guard
# reads, and every member of the RC-14 chain whose finding text this file
# enumerates.  An accounted string is only valid for the bytes that produce it.
#
# IMPLEMENTATION-FREEZE.md and IMPLEMENTER-BLUEPRINT.md are deliberately NOT
# pinned.  Both were under concurrent edit while this file was authored, so a
# pin on either would be an environment dependency failing for reasons
# unrelated to EVIDENCE.  Freeze section 4.5 records exactly that outcome for
# check-retention-custody-v23/-v24: they went to exit 2 RT23-PIN-REFUSED before
# parsing, which silently disabled their own FREEZE_ANCHORS content guard.
# This checker asserts nothing about either document's bytes and must not be
# read as guarding them.
# ---------------------------------------------------------------------------
PINS: dict[str, str] = {
    PREDECESSOR_CHECKER:
        "0379bb9b9006558be9546774b177ed2a1e8c23d8000d16cc4a2cff9d8ed12bbd",
    BINDING:
        "62a3a07194062c8499f6e943b4986d7a77bdecc0c4ec499851ac078fd548e9b4",
    INTERMEDIATE_CHECKER:
        "22f4e53775b3b2e70a3fb42b461f8c3d3308778e24edfcf75e61e6fbf0bcd452",
    LINEAGE_CHECKER:
        "0771f3e1079b99b8e28f6b7a7154c722d2195ba5142e91f350438a2eae7ae525",
    VERSIONING_CHECKER:
        "82834720a8fd4ec8701dad2b43ad94d6ad9e52d21aeb077f4286fab5fb156844",
    "versioning-policy.v8.json":
        "ea4b52b5a4d187ec35ad994d8ffcd888db287566c8fb53f3df17e5203d84ae2e",
    "check-versioning-v7.py":
        "27cc2e22dd909de2ee3050387f87129477ee050e5b25c541dcf305902fbb9d76",
    "versioning-policy.v7.json":
        "0c0f2d7396c32854c3cd5a6aff794c6a0e1be2ffe833816f9ff66f0089b49985",
    "check-retention-custody.py":
        "15816cd8f9d22221b1187b94a160d71f644f9ab8fccb82423931fe18f6fc38d7",
    "check-retention-custody-v11.py":
        "2180497df7c1c4a9a2c6a389119e8ccc7d7069c21872af97d58e657707befbfe",
    "check-retention-custody-v12.py":
        "104a8f9bd01e92226c11c41c234358b5a9d991b42cf12ec9318582ed12b57851",
    "check-retention-custody-v13.py":
        "0290b4ae22816843c2fbce1288ea36f21e78b396361fa6c0bf5291338be519f6",
    "retention-tiers.v10.json":
        "606b5e7125d4a3a46f44f1a7565f9c9ea69132d9ab2783d00339e1b8aac5e026",
    "retention-tiers.v11.json":
        "ba36ccf18e5154336ffa062a0c3280c6f3f010bb6eeb3807ea8daec68818c600",
    "retention-tiers.v12.json":
        "1a034746512de51605b7a4bcc4fb0936bdc167db057a3018be74a2a047376dab",
    "retention-tiers.v13.json":
        "3f79668a6d26b5ecc7fd843be71aef90e779ac024a1ac54bb5cc2c8fc3e0a349",
    "evaluation-proof.v8.json":
        "4bb33f772c8c510c470643082f6bfb8a4df28a050b4720dda6cdd5187bd3e303",
    "check-evaluation-proof-v8.py":
        "c80ac50e21dcd350e5f5285958a6cfb94d52c5c3f7d64f2396d91b544fa82769",
}



RC14_ROOT_LIVE_STATE = (
    "RC-14: $product.CD-RT-5: exact live state must be BLOCKED_ON_PHASE_1A, "
    "got None")
RC14_ROOT_CUSTODY = (
    "RC-14: $contract.custodyPolicy: does not match live product authority")
RC14_RT11 = "pinned RT10 predecessor mechanism is red: " + RC14_ROOT_LIVE_STATE
RC14_RT12 = "pinned RT11 predecessor is red: " + RC14_RT11
RC14_RT13 = "pinned RT12 predecessor is red: " + RC14_RT12
RC14_VER7 = "RT12 dependency is red: " + RC14_RT12
RC14_VER8_A = "VERSIONING v7 predecessor is red: " + RC14_VER7
RC14_VER8_B = "RT13 dependency is red: " + RC14_RT13

CHAIN: tuple[tuple[str, str, str, tuple[str, ...]], ...] = (
    ("check-retention-custody.py", "retention-tiers.v10.json",
     "rt10_for_evidence_v11", (RC14_ROOT_LIVE_STATE, RC14_ROOT_CUSTODY)),
    ("check-retention-custody-v11.py", "retention-tiers.v11.json",
     "rt11_for_evidence_v11", (RC14_RT11,)),
    ("check-retention-custody-v12.py", "retention-tiers.v12.json",
     "rt12_for_evidence_v11", (RC14_RT12,)),
    ("check-retention-custody-v13.py", "retention-tiers.v13.json",
     "rt13_for_evidence_v11", (RC14_RT13,)),
    ("check-versioning-v7.py", "versioning-policy.v7.json",
     "ver7_for_evidence_v11", (RC14_VER7,)),
    ("check-versioning-v8.py", "versioning-policy.v8.json",
     "ver8_for_evidence_v11", (RC14_VER8_A, RC14_VER8_B)),
)

# Which pinned module's check() output may have which accounted findings
# removed, inside check-versioning-v8.py's dependency loader.  Nothing else is
# removed, from nothing else, anywhere.
ACCOUNTED_BY_CHECKER: dict[str, tuple[str, ...]] = {
    "check-versioning-v7.py": (RC14_VER7,),
    "check-retention-custody-v13.py": (RC14_RT13,),
}

# The four predecessor findings this successor closes, recorded so a reader can
# hard-compare what was repaired against what the predecessor still reports.
PREDECESSOR_FINDINGS_CLOSED: tuple[str, ...] = (
    "PR-07-RETAINED-LINEAGE-FOUNDATION",
    "PR-08-RETAINED-LINEAGE-MUTATION-SUITE",
    "PR-22-VERSIONING-CHECKER-GREEN",
    "PR-26-RETAINED-PREDECESSOR-CHECKER-GREEN",
)

KNOWN_PASSES_ON_WRONG_ARTIFACT: tuple[str, ...] = (
    "1. A string leaf in evidence.v10.json whose VALUE is false while its PATH "
    "and TYPE are unchanged. Freeze section 7.8 measured this on a sibling "
    "instrument at TWELVE distinct positions, including a central ruling "
    "reversed in prose. The predecessor binds structure, type and derived "
    "bytes; neither it nor this file binds the truth of content.",
    "2. A COHERENT amendment. Changing BOTH posture fields together, or "
    "substituting decidedBy AND rewriting the narrative that names it, passes "
    "every property gate. The guard binds internal consistency, not truth.",
    "3. Prose inside $.decisions.CD-RT-5 that contradicts the decision it "
    "records, anywhere the packet does not repeat a checked field. The digest "
    "notice reports that such prose moved; it does not fail the build.",
    "4. The accounted RC-14 subtraction and the repaired RT13 admission are "
    "justified by string equality against an enumerated expectation. A future "
    "chain finding whose text happened to equal an accounted string would be "
    "admitted. No such collision exists today; nothing prevents one.",
    "5. The predecessor's own source self-inspection scans "
    "(_selftest_reachability_findings, _path_guard_findings, "
    "_cli_argument_findings) read check-evidence-v10.py's bytes, not this "
    "file's. This file adds only a narrow AST reachability scan over itself, so "
    "its own source is materially less self-inspected than the predecessor's.",
    "6. This file's repair is installed by substituting module attributes on "
    "pinned modules (_RT_CONTEXT, module). The substitution is anchored by the "
    "predecessors' digests, but nothing re-derives that the installed context "
    "is byte-identical to what the unrepaired function would have built had the "
    "decision not been taken.",
    "7. Edits to product-dispositions.v1.json OUTSIDE $.decisions.CD-RT-5 are "
    "not bound here, by deliberate scope: this file is not the whole packet's "
    "guard, check-product-dispositions-v2.py is. The one exception is the "
    "cross-packet coherence gate, which fires when another position asserts "
    "the pre-decision state unmarked.",
)


class DuplicateKeyError(ValueError):
    """A JSON object repeated a key; the document is not canonical."""


def _pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
    """section 7.5: reject duplicate keys instead of keeping the last one."""
    result: dict[str, Any] = {}
    for key, value in items:
        if key in result:
            raise DuplicateKeyError(f"duplicate JSON key {key!r}")
        result[key] = value
    return result


def load_json(path: pathlib.Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=_pairs)


def sha_file(name: str) -> str:
    return hashlib.sha256((HERE / name).read_bytes()).hexdigest()


class _VerifiedSourceLoader:
    """Execute exactly the bytes that were hash-verified, never a re-read."""

    def __init__(self, filename: pathlib.Path, source: bytes):
        self.filename = filename
        self.source = source

    def create_module(self, _spec: Any) -> None:
        return None

    def exec_module(self, module: types.ModuleType) -> None:
        exec(compile(self.source, str(self.filename), "exec"), module.__dict__)


def _execute_verified(filename: str, alias: str) -> types.ModuleType:
    """Hash-before-execution, then execute the verified bytes."""
    path = (HERE / filename).resolve()
    source = path.read_bytes()
    actual = hashlib.sha256(source).hexdigest()
    if actual != PINS[filename]:
        raise RuntimeError(f"{filename}: {actual} != {PINS[filename]}")
    spec = importlib.util.spec_from_file_location(
        alias, path, loader=_VerifiedSourceLoader(path, source))
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot construct verified spec for {filename}")
    module = importlib.util.module_from_spec(spec)
    prior = sys.modules.get(alias)
    sys.modules[alias] = module
    try:
        spec.loader.exec_module(module)
    finally:
        if prior is None:
            sys.modules.pop(alias, None)
        else:
            sys.modules[alias] = prior
    return module


def _plain_module(filename: str, alias: str) -> types.ModuleType:
    spec = importlib.util.spec_from_file_location(alias, HERE / filename)
    if spec is None or spec.loader is None:
        raise ImportError(filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# ---------------------------------------------------------------------------
# The re-pointed CD-RT-5 guard.
#
# PROPERTIES ARE FATAL; CURRENT VALUES ARE A NON-FATAL NOTICE.
#
# `cd_rt_5_findings()` is a pure function of a parsed packet.  It performs no
# I/O and consults no digest, so an external driver can import this file
# unmodified and mutate a packet in memory to prove the guard is not vacuous -
# the section 7.8 "prove non-vacuity from outside itself" discipline.
# ---------------------------------------------------------------------------

# A decided row's status vocabulary.  This is a CLOSED VOCABULARY (a continuing
# invariant, section 7.2.2), not a snapshot of today's value.
DECIDED_STATUSES = frozenset({"DECIDED"})

# Strings that ASSERT the pre-decision retention state.  The corpus retains
# superseded text verbatim (sections 4.4 and 4.5), so a bare substring hunt
# would fire on an honest supersession record.  A hit is a contradiction only
# when nothing in the same leaf, or in its path, marks it as superseded.
PENDING_STATE_TOKENS = (
    "BLOCKED_ON_PHASE_1A", "blocked on Phase 1A", "blocked on phase 1a",
    "remains visibly blocked", "intentionally unresolved", "UNSELECTED",
)
SUPERSESSION_MARKERS = (
    "SUPERSEDED", "SUPERSEDES", "supersedes", "superseded",
    "read verbatim", "retained here verbatim", "prior value",
    "historical", "no longer", "withdrawn",
)

# A decision is constituted by an AUTHORITY.  Section 4.4's fabrication was a
# recommendation converted into a declaration; the roles below are the ones the
# corpus records as unable to constitute a product decision, so finding one in
# `decidedBy` is the section 4.4 shape recurring.
NON_AUTHORITY_DECIDERS = frozenset({
    "coordinator", "architecture", "architect", "reviewer", "review",
    "lane", "agent", "assistant", "checker", "instrument", "unknown",
    "tbd", "todo", "n/a", "na", "none", "null", "system", "auto",
    "automated", "implementer", "author",
})

# Posture coherence.  A decided row must select a posture, and the two posture
# fields must agree with each other.  This is an internal-consistency invariant,
# so a COHERENT future amendment passes while a single-field flip does not.
UNSELECTED_POSTURES = frozenset({
    "", "UNSELECTED", "UNDECIDED", "PENDING", "TBD", "NONE", "NULL",
})
DURABLE_POSTURE = "DURABLE_RETAINED"
IMPLICIT_WHEN_DURABLE = "YES"
IMPLICIT_WHEN_NOT_DURABLE = "NO"

# ---------------------------------------------------------------------------
# NON-FATAL observation.  Recorded so a reader can tell "the decision text
# legitimately advanced" from "the decision is wrong", and explicitly NOT a
# gate: the verdict is decided by the properties above.  Measured
# 2026-08-06T02:16Z over the canonical serialisation of $.decisions.CD-RT-5.
#
# This used to be a fatal whole-FILE digest pin on product-dispositions.v1.json.
# It was wrong, and the corpus proved it within the hour: the packet's
# whole-file digest moved 5fc59ad2... -> bbe24527... while the CD-RT-5 subtree
# digest stayed IDENTICAL at 90a9dd06... - measured, both revisions.  The edit
# repaired three positions ($.status, $.invariants[4], $.knownLimitations[0])
# that still asserted the pre-decision state, which is a REAL defect this
# file's own consistency gate reports on the pre-repair bytes.  A pin that
# quantifies over content the instrument is not the guard for produces failures
# carrying no information about its subject; freeze section 4.5 already
# recorded that cost when check-retention-custody-v23/-v24 hit exit 2
# RT23-PIN-REFUSED and silently disabled their own FREEZE_ANCHORS guard.
# ---------------------------------------------------------------------------
# The value the row carried while it was pending, used only by the mutation
# suite to reconstruct a reverted packet.  It is NOT asserted anywhere.
SUPERSEDED_PENDING_STATE = "BLOCKED_ON_PHASE_1A"
AUTHORED_CD_RT_5_DIGEST = "90a9dd062d12917905dfaf40b196e3787b83f54e64c3dac1a5020c10ba124a65"
AUTHORED_CD_RT_5 = {
    "status": "DECIDED",
    "decidedBy": "sfbreen",
    "decidedOn": "2026-08-05",
    "defaultPosture.durableDefault": "DURABLE_RETAINED",
    "defaultPosture.implicitDurableRetention": "YES",
}

_PLACEHOLDER_RE = re.compile(
    r"\[\s*(UNSET|TBD|TODO|FIXME|PENDING|PLACEHOLDER|FILL|NAME|DATE|SIGNER)\b",
    re.IGNORECASE)
_BRACKET_WRAPPED_RE = re.compile(r"^\s*\[[^\]]*\]\s*$")

_FORBIDDEN_AUTHORITY_KEYS = frozenset({
    "signoff", "signedoff", "signature", "signer", "productacceptance",
    "productsignoff", "acceptedby", "approvedby", "approval",
})
_FORBIDDEN_AUTHORITY_VALUES = frozenset({
    "SIGNED", "SIGNEDOFF", "PRODUCTSIGNEDOFF", "APPROVED", "SEALED",
    "ACCEPTED",
})
_STATE_KEYS = frozenset({
    "status", "state", "currentstate", "disposition", "verdict", "outcome",
})
DECISION_PATH = "$.decisions.CD-RT-5"

# Non-fatal notices from the most recent guard run, printed by the banner.
_NOTICES: list[str] = []


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")


def _dotted(node: Any, path: str) -> Any:
    for step in path.split("."):
        if not isinstance(node, dict) or step not in node:
            return None
        node = node[step]
    return node


def _string_leaves(node: Any, prefix: str):
    if isinstance(node, dict):
        for key, child in node.items():
            yield from _string_leaves(child, f"{prefix}.{key}")
    elif isinstance(node, list):
        for index, child in enumerate(node):
            yield from _string_leaves(child, f"{prefix}[{index}]")
    elif isinstance(node, str):
        yield prefix, node


def _is_placeholder(text: str) -> bool:
    return bool(_PLACEHOLDER_RE.search(text) or _BRACKET_WRAPPED_RE.match(text))


def cd_rt_5_digest(packet: Any) -> str | None:
    decision = _dotted(packet, "decisions.CD-RT-5") \
        if isinstance(packet, dict) else None
    if decision is None:
        return None
    try:
        return hashlib.sha256(canonical(decision)).hexdigest()
    except (TypeError, ValueError):
        return None


def cd_rt_5_notices(packet: Any) -> list[str]:
    """NON-FATAL drift observations.  These never change the exit code.

    Section 7.2.2's rider says a measurement that cannot fail the build is
    prose.  These are prose, deliberately and by name: the build is failed by
    `cd_rt_5_findings()`, and these exist only so a reader can distinguish a
    legitimate advance from a defect without re-deriving it by hand.
    """
    out: list[str] = []
    digest = cd_rt_5_digest(packet)
    if digest is not None and digest != AUTHORED_CD_RT_5_DIGEST:
        out.append(
            f"EV11-CDRT5-DIGEST-MOVED (NOTICE, not a finding): "
            f"{DECISION_PATH} canonicalises to {digest}; this instrument was "
            f"authored against {AUTHORED_CD_RT_5_DIGEST}. The verdict is "
            "decided by the property gates, not by this digest.")
    decision = _dotted(packet, "decisions.CD-RT-5") \
        if isinstance(packet, dict) else None
    if isinstance(decision, dict):
        for path, authored in AUTHORED_CD_RT_5.items():
            actual = _dotted(decision, path)
            if actual != authored:
                out.append(
                    f"EV11-CDRT5-VALUE-MOVED (NOTICE, not a finding): "
                    f"{DECISION_PATH}.{path} is {actual!r}; authored against "
                    f"{authored!r}.")
    return out


def cd_rt_5_findings(packet: Any) -> list[str]:
    """Assert the PROPERTIES a constituted CD-RT-5 decision must have.

    Re-points `check-retention-custody.py::_authority_guard`'s live-state
    check.  The predecessor asserted the literal value
    `pendingDecisions.CD-RT-5.status == BLOCKED_ON_PHASE_1A`; the authority
    decided on 2026-08-05, so that literal is false and this asserts the
    properties of a decision instead - which survives the next legitimate
    amendment and still fails on fabrication, silent reversion and unfilled
    placeholders.
    """
    out: list[str] = []
    if not isinstance(packet, dict):
        return [f"EV11-CDRT5-SHAPE: product packet root is not an object"]

    decisions = packet.get("decisions")
    pending = packet.get("pendingDecisions")
    if not isinstance(decisions, dict):
        out.append(f"EV11-CDRT5-SHAPE: $.decisions is not an object")
    if pending is not None and not isinstance(pending, dict):
        out.append(f"EV11-CDRT5-SHAPE: $.pendingDecisions is not an object")

    in_decided = isinstance(decisions, dict) and "CD-RT-5" in decisions
    in_pending = isinstance(pending, dict) and "CD-RT-5" in pending

    if in_decided and in_pending:
        out.append(
            f"EV11-CDRT5-DUPLICATED: CD-RT-5 appears in BOTH $.decisions and "
            "$.pendingDecisions; a row is in exactly one state and a duplicate "
            "lets a reader pick the answer they prefer")
    if in_pending and not in_decided:
        entry = pending["CD-RT-5"]
        state = entry.get("status") if isinstance(entry, dict) else entry
        out.append(
            f"EV11-CDRT5-REVERTED: CD-RT-5 is in $.pendingDecisions with "
            f"status {state!r} and not in $.decisions; the decision has been "
            "reverted")
    if not in_decided and not in_pending:
        out.append(
            f"EV11-CDRT5-ABSENT: CD-RT-5 is in neither $.decisions nor "
            "$.pendingDecisions; the binding packet no longer carries the row "
            "at all")
    if not in_decided:
        return out

    decision = decisions["CD-RT-5"]
    if not isinstance(decision, dict):
        out.append(f"EV11-CDRT5-SHAPE: {DECISION_PATH} is "
                   f"{type(decision).__name__}, not an object")
        return out

    # -- the row is under $.decisions, so it must BE a decision --------------
    status = decision.get("status")
    if status not in DECIDED_STATUSES:
        out.append(
            f"EV11-CDRT5-STATUS: {DECISION_PATH}.status is {status!r}; a row "
            f"under $.decisions must carry one of {sorted(DECIDED_STATUSES)!r}")

    leaves = list(_string_leaves(decision, DECISION_PATH))

    # -- authority: filled, by a named authority, on a real date ------------
    decided_by = decision.get("decidedBy")
    if not isinstance(decided_by, str) or not decided_by.strip():
        out.append(f"EV11-CDRT5-AUTHORITY: {DECISION_PATH}.decidedBy is not a "
                   f"non-empty string ({decided_by!r})")
    elif _is_placeholder(decided_by):
        out.append(
            f"EV11-CDRT5-PLACEHOLDER: {DECISION_PATH}.decidedBy is an "
            f"unfilled placeholder ({decided_by!r}); a prepared amendment may "
            "not read as a taken decision")
    else:
        normalized = re.sub(r"[^a-z]", "", decided_by.lower())
        if normalized in NON_AUTHORITY_DECIDERS:
            out.append(
                f"EV11-CDRT5-AUTHORITY: {DECISION_PATH}.decidedBy is "
                f"{decided_by!r}, a role the corpus records as unable to "
                "constitute a product decision (freeze section 4.4: a "
                "recommendation converted into a declaration)")
        elif len(decided_by.strip()) < 3:
            out.append(f"EV11-CDRT5-AUTHORITY: {DECISION_PATH}.decidedBy is "
                       f"too short to identify an authority ({decided_by!r})")
        else:
            corroborating = [
                path for path, text in leaves
                if path != f"{DECISION_PATH}.decidedBy" and decided_by in text]
            if not corroborating:
                out.append(
                    f"EV11-CDRT5-UNCORROBORATED: {DECISION_PATH}.decidedBy is "
                    f"{decided_by!r} and no other leaf of the decision names "
                    "it. Freeze section 4.4's fabrication was a single-source "
                    "attribution; a bare authority field is that shape.")

    decided_on = decision.get("decidedOn")
    if not isinstance(decided_on, str) or not decided_on.strip():
        out.append(f"EV11-CDRT5-AUTHORITY: {DECISION_PATH}.decidedOn is not a "
                   f"non-empty string ({decided_on!r})")
    elif _is_placeholder(decided_on):
        out.append(
            f"EV11-CDRT5-PLACEHOLDER: {DECISION_PATH}.decidedOn is an "
            f"unfilled placeholder ({decided_on!r})")
    else:
        try:
            when = datetime.date.fromisoformat(decided_on)
        except ValueError:
            when = None
            out.append(f"EV11-CDRT5-AUTHORITY: {DECISION_PATH}.decidedOn is "
                       f"not a real ISO-8601 calendar date ({decided_on!r})")
        if when is not None:
            authored = packet.get("date")
            if isinstance(authored, str):
                try:
                    if when < datetime.date.fromisoformat(authored):
                        out.append(
                            f"EV11-CDRT5-AUTHORITY: {DECISION_PATH}.decidedOn "
                            f"({decided_on}) precedes the packet's own "
                            f"authoring date ({authored}); a decision cannot "
                            "predate the document that constitutes it")
                except ValueError:
                    pass
            corroborating = [
                path for path, text in leaves
                if path != f"{DECISION_PATH}.decidedOn" and decided_on in text]
            if not corroborating:
                out.append(
                    f"EV11-CDRT5-UNCORROBORATED: {DECISION_PATH}.decidedOn is "
                    f"{decided_on!r} and no other leaf of the decision names "
                    "it.")

    # -- posture: selected, and internally coherent -------------------------
    durable = _dotted(decision, "defaultPosture.durableDefault")
    implicit = _dotted(decision, "defaultPosture.implicitDurableRetention")
    if not isinstance(durable, str) or durable.strip().upper() in \
            UNSELECTED_POSTURES or _is_placeholder(durable):
        out.append(
            f"EV11-CDRT5-POSTURE: "
            f"{DECISION_PATH}.defaultPosture.durableDefault is {durable!r}; a "
            "decided row must select a posture")
    elif not isinstance(implicit, str) or _is_placeholder(implicit):
        out.append(
            f"EV11-CDRT5-POSTURE: "
            f"{DECISION_PATH}.defaultPosture.implicitDurableRetention is "
            f"{implicit!r}; a decided row must state it")
    else:
        expected = IMPLICIT_WHEN_DURABLE if durable == DURABLE_POSTURE \
            else IMPLICIT_WHEN_NOT_DURABLE
        if implicit != expected:
            out.append(
                f"EV11-CDRT5-POSTURE-INCOHERENT: durableDefault={durable!r} "
                f"requires implicitDurableRetention={expected!r}, packet says "
                f"{implicit!r}. The two posture fields disagree, so one of them "
                "was changed without the other.")

    # -- no unfilled placeholder anywhere in the decision --------------------
    for path, text in leaves:
        if path in (f"{DECISION_PATH}.decidedBy", f"{DECISION_PATH}.decidedOn"):
            continue
        if _is_placeholder(text):
            out.append(
                f"EV11-CDRT5-PLACEHOLDER: {path} carries an unfilled "
                f"placeholder ({text[:72]!r}); a prepared amendment may not "
                "read as a taken decision")

    # -- a decision is not a signature (freeze section 4.5) -----------------
    def walk(node: Any, path: str) -> None:
        if isinstance(node, dict):
            for key, child in node.items():
                normalized = re.sub(r"[^a-z]", "", str(key).lower())
                if normalized in _FORBIDDEN_AUTHORITY_KEYS:
                    out.append(
                        f"EV11-CDRT5-FABRICATION: {path}.{key} manufactures a "
                        "product signature; freeze section 4.5 - a decision is "
                        "not a signature, and section 11's Product signer line "
                        "is still [UNSET]")
                if isinstance(child, str) and normalized in _STATE_KEYS:
                    value = re.sub(r"[^A-Z]", "", child.upper())
                    if value in _FORBIDDEN_AUTHORITY_VALUES:
                        out.append(
                            f"EV11-CDRT5-FABRICATION: {path}.{key} declares "
                            f"positive authority state {child!r}")
                walk(child, f"{path}.{key}")
        elif isinstance(node, list):
            for index, child in enumerate(node):
                walk(child, f"{path}[{index}]")

    walk(decision, DECISION_PATH)

    # -- the rest of the packet must not still assert the pending state -----
    # The corpus retains superseded text verbatim, so a hit counts only when
    # nothing in the leaf or its path marks it superseded.  Measured: this
    # gate reports 0 on the live packet, 3 on the revision immediately before
    # it ($.status, $.invariants[4], $.knownLimitations[0]) - which is the
    # self-contradiction that revision was repaired to remove.
    for path, text in _string_leaves(packet, "$"):
        if path.startswith(DECISION_PATH):
            continue
        token = next((t for t in PENDING_STATE_TOKENS if t in text), None)
        if token is None:
            continue
        if any(marker in text for marker in SUPERSESSION_MARKERS) or \
                any(marker in path for marker in SUPERSESSION_MARKERS):
            continue
        out.append(
            f"EV11-CDRT5-PACKET-INCOHERENT: {path} still asserts the "
            f"pre-decision retention state ({token!r}) with no supersession "
            f"marker, while {DECISION_PATH} records a taken decision: "
            f"{text[:80]!r}")
    return out


def product_packet_findings() -> tuple[list[str], list[str], bool]:
    """Load the binding packet and apply the property guard.

    Returns (findings, notices, state_ok).  `state_ok` gates every accounted
    subtraction below: nothing is subtracted unless CD-RT-5 is validly decided,
    whatever values that decision happens to carry.
    """
    try:
        packet = load_json(HERE / PRODUCT)
    except (OSError, UnicodeError, json.JSONDecodeError, DuplicateKeyError) as exc:
        return ([f"EV11-PACKET-UNREADABLE: {PRODUCT}: "
                 f"{type(exc).__name__}: {exc}"], [], False)
    findings = cd_rt_5_findings(packet)
    return findings, cd_rt_5_notices(packet), (not findings)


# ---------------------------------------------------------------------------
# Section 2.  The immutable chain, enumerated level by level.
# ---------------------------------------------------------------------------

def chain_audit(state_ok: bool) -> list[str]:
    """Execute every level of the RC-14 chain and hard-compare its findings.

    Section 7.2.2: a recorded measurement must be compared to the measurement it
    records.  The accounted RC-14 propagation is a recorded measurement of these
    exact bytes, so it is compared, not narrated.  A level that grows a finding,
    loses one, or changes its wording fails here - which is what makes the
    admission in `repaired_rt_context` and the subtraction in `_AccountedCheck`
    safe rather than trusted.
    """
    out: list[str] = []
    for checker, subject, alias, expected in CHAIN:
        try:
            module = _plain_module(checker, alias)
            value = load_json(HERE / subject)
            findings = module.check(value)
        except Exception as exc:                      # noqa: BLE001 - reported
            out.append(f"EV11-CHAIN-RAISED: {checker} on {subject} raised "
                       f"{type(exc).__name__}: {exc}")
            continue
        if not isinstance(findings, list):
            out.append(f"EV11-CHAIN-SHAPE: {checker} did not return a list")
            continue
        wanted = list(expected) if state_ok else []
        if sorted(findings) != sorted(wanted):
            out.append(
                f"EV11-CHAIN-DRIFT: {checker} on {subject} reported "
                f"{len(findings)} finding(s), expected exactly {len(wanted)} "
                f"accounted; unaccounted="
                f"{[f for f in findings if f not in wanted]!r}; "
                f"missing={[f for f in wanted if f not in findings]!r}")
    return out


# ---------------------------------------------------------------------------
# Section 3.  The repair, installed at the RC-14 site.
# ---------------------------------------------------------------------------

class _AccountedCheck:
    """A pinned module with exactly the accounted RC-14 findings removed."""

    def __init__(self, module: types.ModuleType, accounted: tuple[str, ...]):
        self._module = module
        self._accounted = frozenset(accounted)
        self.removed: list[str] = []

    def __getattr__(self, name: str) -> Any:
        return getattr(self._module, name)

    def check(self, *args: Any, **kwargs: Any) -> Any:
        outcome = self._module.check(*args, **kwargs)
        if not isinstance(outcome, list):
            return outcome
        kept = []
        for finding in outcome:
            if finding in self._accounted:
                self.removed.append(finding)
            else:
                kept.append(finding)
        return kept


def repaired_rt_context(v8mod: types.ModuleType) -> dict[str, Any]:
    """`check-evidence-v8.py::_rt_context()` with one line re-pointed.

    Every assertion the original makes is made here, using the original's own
    helpers and the original's own PINS, so this is a re-execution rather than
    a re-implementation.  The single change is marked RE-POINTED below: the
    RT13 finding list is compared against the enumerated accounted RC-14
    propagation instead of against emptiness.
    """
    for filename in ("evaluation-proof.v8.json", "check-evaluation-proof-v8.py",
                     "retention-tiers.v13.json",
                     "check-retention-custody-v13.py",
                     "check-retention-custody.py"):
        if v8mod.sha_file(filename) != v8mod.PINS[filename]:
            raise ValueError(f"pinned RT13 input drift: {filename}")
    rt = v8mod.load("retention-tiers.v13.json")
    ep = v8mod.load("evaluation-proof.v8.json")
    rt13mod = v8mod._module(
        "check-retention-custody-v13.py", "rt13_authority_for_evidence_v11")
    ep8mod = v8mod._module(
        "check-evaluation-proof-v8.py", "ep8_authority_for_evidence_v11")
    rtcore = v8mod._module(
        "check-retention-custody.py", "rtcore_authority_for_evidence_v11")
    findings = rt13mod.check(rt)
    # RE-POINTED.  Original: `if findings: raise ValueError(...)`.
    residual = [row for row in findings if row != RC14_RT13]
    if residual:
        raise ValueError(f"pinned RT13 is red: {residual[0]}")
    if RC14_RT13 not in findings:
        raise ValueError(
            "the accounted RC-14 propagation is absent from RT13; the "
            "re-pointed admission is not load-bearing on these bytes")
    derived = rt13mod.regenerate(rt, ep, ep8mod, rtcore)
    frozen = rt["capabilityClosure"]["semanticClosure"]
    if derived["proofRefs"] != frozen["proofRefs"] or \
            derived["units"] != frozen["units"] or \
            derived["closureCommitment"] != frozen["closureCommitment"]:
        raise ValueError("cold RT13 derivation differs from authoritative closure")
    pin_refs = sorted([{
        "projectId": row["projectId"],
        "recordCasRef": row["recordCasRef"],
        "recordKind": row["recordKind"],
    } for row in derived["proofRefs"]], key=v8mod.canonical)
    if len(pin_refs) != 23 or len({v8mod.canonical(row) for row in pin_refs}) != 23:
        raise ValueError("RT13 does not derive exactly 23 unique raw objects")
    return {
        "contract": rt,
        "checker": rt13mod,
        "core": rtcore,
        "derived": derived,
        "pinRefs": pin_refs,
        "unitIds": [row["unitId"] for row in derived["units"]],
    }


def repair_authority(authority: Any) -> list[str]:
    """Install the re-pointed guard into one pinned authority closure."""
    problems: list[str] = []
    v8mod = authority.module(LINEAGE_CHECKER)
    if getattr(v8mod, "_RT_CONTEXT", None) is not None:
        problems.append(
            f"{LINEAGE_CHECKER}._RT_CONTEXT was already populated; the "
            "re-pointed context would not be the one its probes use")
    else:
        context = repaired_rt_context(v8mod)
        v8mod._RT_CONTEXT = context
        if v8mod._rt_context() is not context:
            problems.append(
                f"{LINEAGE_CHECKER}._rt_context() did not return the "
                "re-pointed context; the repair is not installed")
    vermod = authority.module(VERSIONING_CHECKER)
    original: Callable[..., types.ModuleType] = vermod.module
    proxies: list[_AccountedCheck] = []

    def loader(filename: str, alias: str) -> Any:
        module = original(filename, alias)
        accounted = ACCOUNTED_BY_CHECKER.get(filename)
        if not accounted:
            return module
        proxy = _AccountedCheck(module, accounted)
        proxies.append(proxy)
        return proxy

    vermod.module = loader
    authority._ev11_versioning_proxies = proxies
    return problems


def repair(predecessor: types.ModuleType) -> tuple[list[Any], list[str]]:
    """Repair every authority closure the predecessor's probes reach.

    Two closures exist: the predecessor's own, and the one
    `check-evidence-v9.py` builds for itself and which PR-26 executes.
    """
    problems: list[str] = []
    authorities = [predecessor._BOOTSTRAP_AUTHORITY]
    try:
        v9mod = predecessor._BOOTSTRAP_AUTHORITY.module(INTERMEDIATE_CHECKER)
        authorities.append(v9mod._BOOTSTRAP_AUTHORITY)
    except Exception as exc:                          # noqa: BLE001 - reported
        problems.append(f"EV11-REPAIR: cannot reach {INTERMEDIATE_CHECKER}'s "
                        f"authority: {type(exc).__name__}: {exc}")
    for authority in authorities:
        try:
            problems.extend(f"EV11-REPAIR: {row}"
                            for row in repair_authority(authority))
        except Exception as exc:                      # noqa: BLE001 - reported
            problems.append(f"EV11-REPAIR: installing the re-pointed context "
                            f"raised {type(exc).__name__}: {exc}")
    return authorities, problems


# ---------------------------------------------------------------------------
# Section 4.  This file's own reachability scan.
#
# The predecessor's three source self-inspection scans read
# check-evidence-v10.py, not this file.  This is the narrow replacement, and
# KNOWN_PASSES_ON_WRONG_ARTIFACT item 5 records that it is narrower.
# ---------------------------------------------------------------------------

_REQUIRED_REACHABLE: dict[str, tuple[str, ...]] = {
    "main": ("_parse_argv", "check", "selftest"),
    "check": ("prepare", "_pin_findings", "product_packet_findings",
              "cd_rt_5_findings", "chain_audit", "repair", "repair_authority",
              "repaired_rt_context", "_self_reachability_findings",
              "_probe_census", "cd_rt_5_notices", "cd_rt_5_digest"),
    "selftest": ("prepare", "guard_sweep", "cd_rt_5_findings",
                 "_packet_mutations", "repair", "repaired_rt_context"),
}


def _self_reachability_findings() -> list[str]:
    """Transitive reachability over this file's own local call graph.

    The predecessor's own three source scans read check-evidence-v10.py.  This
    is the narrow replacement: it proves each declared layer is still reachable
    from the entry point that is supposed to reach it, so a layer cannot be
    orphaned by an edit while the banner keeps claiming it ran.
    """
    out: list[str] = []
    try:
        tree = ast.parse((HERE / CHECKER).read_text(encoding="utf-8"))
    except (OSError, UnicodeError, SyntaxError) as exc:
        return [f"EV11-SELF-SCAN: cannot parse this checker's own source: "
                f"{type(exc).__name__}: {exc}"]
    # Module-level definitions only.  A class method that happens to share a
    # name with a module-level function must not shadow it here.
    functions = {node.name: node for node in tree.body
                 if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))}
    direct: dict[str, set[str]] = {}
    for name, node in functions.items():
        direct[name] = {child.func.id for child in ast.walk(node)
                        if isinstance(child, ast.Call)
                        and isinstance(child.func, ast.Name)
                        and child.func.id in functions}

    def reachable(root: str) -> set[str]:
        seen: set[str] = set()
        stack = [root]
        while stack:
            current = stack.pop()
            for callee in direct.get(current, ()):
                if callee not in seen:
                    seen.add(callee)
                    stack.append(callee)
        return seen

    for name, required in sorted(_REQUIRED_REACHABLE.items()):
        if name not in functions:
            out.append(f"EV11-SELF-SCAN: {name}() is not defined")
            continue
        found = reachable(name)
        for callee in required:
            if callee not in found:
                out.append(f"EV11-SELF-SCAN: {callee}() is no longer reachable "
                           f"from {name}(); a layer has been orphaned")
    if not KNOWN_PASSES_ON_WRONG_ARTIFACT:
        out.append("EV11-SELF-SCAN: the section 7.8 bound is unenumerated")
    return out


# ---------------------------------------------------------------------------
# Section 5.  Composition.
# ---------------------------------------------------------------------------

def _pin_findings() -> list[str]:
    out: list[str] = []
    for name, expected in sorted(PINS.items()):
        try:
            actual = sha_file(name)
        except OSError as exc:
            out.append(f"EV11-PIN-UNREADABLE: {name}: "
                       f"{type(exc).__name__}: {exc}")
            continue
        if actual != expected:
            out.append(f"EV11-PIN-DRIFT: {name} is {actual}, pinned {expected}")
    return out


def prepare() -> tuple[Any, Any, list[str], bool]:
    """Verify, execute and repair the predecessor.  Returns
    (module, authority, findings, state_ok)."""
    findings: list[str] = []
    findings.extend(_pin_findings())
    findings.extend(_self_reachability_findings())
    packet_findings, packet_notices, state_ok = product_packet_findings()
    findings.extend(packet_findings)
    _NOTICES[:] = packet_notices
    findings.extend(chain_audit(state_ok))
    sink = io.StringIO()
    try:
        with redirect_stdout(sink):
            predecessor = _execute_verified(
                PREDECESSOR_CHECKER, "opensip_ev11_predecessor_ev10")
    except BaseException as exc:                      # noqa: BLE001 - reported
        findings.append(f"EV11-PREDECESSOR-IMPORT: {PREDECESSOR_CHECKER}: "
                        f"{type(exc).__name__}: {exc}")
        return None, None, findings, state_ok
    if not state_ok:
        # The live packet is not the state this repair was written for, so no
        # repair is installed.  The predecessor then reports its own findings
        # unmodified, which is the correct behaviour: nothing is suppressed on
        # a tree this instrument does not recognise.
        return predecessor, predecessor._BOOTSTRAP_AUTHORITY, findings, state_ok
    _authorities, problems = repair(predecessor)
    findings.extend(problems)
    return predecessor, predecessor._BOOTSTRAP_AUTHORITY, findings, state_ok


_LAST_CENSUS: dict[str, int] = {"green": 0, "total": 0, "removed": 0}


def _probe_census(predecessor: Any, authority: Any,
                  state_ok: bool) -> list[str]:
    """Hard-compare the predecessor's own probe log and the subtraction count.

    Section 7.2.2: a recorded measurement must be compared to the measurement it
    records.  The banner publishes both figures, so both are compared here
    rather than asserted in prose.
    """
    out: list[str] = []
    log = getattr(authority, "probe_log", None)
    ids = getattr(predecessor, "PROBE_IDS", ())
    if not isinstance(log, dict) or not ids:
        out.append("EV11-PROBE-CENSUS: the predecessor's probe log is not "
                   "available; its probe coverage cannot be compared")
        return out
    green = sum(1 for value in log.values() if value)
    _LAST_CENSUS["green"] = green
    _LAST_CENSUS["total"] = len(ids)
    if set(log) != set(ids) or green != len(ids):
        out.append(
            f"EV11-PROBE-CENSUS: {green}/{len(ids)} probes green over "
            f"{len(log)} recorded; missing={sorted(set(ids) - set(log))!r}; "
            f"red={sorted(k for k, v in log.items() if not v)!r}")
    if state_ok:
        removed = sum(len(proxy.removed)
                      for proxy in getattr(authority,
                                           "_ev11_versioning_proxies", []))
        _LAST_CENSUS["removed"] = removed
        if removed == 0:
            out.append(
                "EV11-SUBTRACTION-NOT-LOAD-BEARING: no accounted RC-14 finding "
                "was removed inside check-versioning-v8.py's dependency "
                "loader; a subtraction that never fires is a guard that proves "
                "nothing")
    return out


def check(candidate: Any, source: Any = None) -> list[str]:
    """Everything check-evidence-v10.py does, plus the re-pointed guard."""
    predecessor, authority, findings, state_ok = prepare()
    if predecessor is None:
        return findings
    try:
        findings.extend(predecessor.check(candidate, authority, source))
    except Exception as exc:                          # noqa: BLE001 - reported
        findings.append(f"EV11-PREDECESSOR-RAISED: "
                        f"{PREDECESSOR_CHECKER}.check raised "
                        f"{type(exc).__name__}: {exc}")
        return findings
    findings.extend(_probe_census(predecessor, authority, state_ok))
    return findings


# ---------------------------------------------------------------------------
# Section 6.  Selftest.
# ---------------------------------------------------------------------------

def _packet_mutations() -> list[tuple[str, Callable[[dict[str, Any]], None]]]:
    def revert(packet: dict[str, Any]) -> None:
        decision = packet["decisions"].pop("CD-RT-5")
        packet["pendingDecisions"]["CD-RT-5"] = {
            "status": SUPERSEDED_PENDING_STATE,
            "question": decision.get("question"),
        }

    def drop(packet: dict[str, Any]) -> None:
        packet["decisions"].pop("CD-RT-5")

    def duplicate_into_pending(packet: dict[str, Any]) -> None:
        packet["pendingDecisions"]["CD-RT-5"] = {
            "status": SUPERSEDED_PENDING_STATE}

    def author(packet: dict[str, Any]) -> None:
        packet["decisions"]["CD-RT-5"]["decidedBy"] = "coordinator"

    def blank_date(packet: dict[str, Any]) -> None:
        packet["decisions"]["CD-RT-5"]["decidedOn"] = ""

    def placeholder_author(packet: dict[str, Any]) -> None:
        packet["decisions"]["CD-RT-5"]["decidedBy"] = \
            "[UNSET — the authority's name]"

    def placeholder_date(packet: dict[str, Any]) -> None:
        packet["decisions"]["CD-RT-5"]["decidedOn"] = "[UNSET — date]"

    def posture(packet: dict[str, Any]) -> None:
        packet["decisions"]["CD-RT-5"]["defaultPosture"]["durableDefault"] = \
            "EPHEMERAL_ONLY"

    def implicit(packet: dict[str, Any]) -> None:
        packet["decisions"]["CD-RT-5"]["defaultPosture"][
            "implicitDurableRetention"] = "NO"

    def status(packet: dict[str, Any]) -> None:
        packet["decisions"]["CD-RT-5"]["status"] = "PENDING"

    def signature(packet: dict[str, Any]) -> None:
        packet["decisions"]["CD-RT-5"]["signOff"] = \
            "SIGNED OFF 2026-07-31 by product owner"

    def positive_state(packet: dict[str, Any]) -> None:
        packet["decisions"]["CD-RT-5"]["decision"]["status"] = \
            "PRODUCT-SIGNED-OFF"

    def nested_placeholder(packet: dict[str, Any]) -> None:
        packet["decisions"]["CD-RT-5"]["decision"]["reasonCodeRequired"] = \
            "[TBD]"

    def author_human(packet: dict[str, Any]) -> None:
        # A plausible human name. Only the corroboration gate catches this one:
        # the decision's own narrative still names the real authority.
        packet["decisions"]["CD-RT-5"]["decidedBy"] = "jdoe"

    def substitute_date(packet: dict[str, Any]) -> None:
        packet["decisions"]["CD-RT-5"]["decidedOn"] = "2026-07-31"

    def unselect_posture(packet: dict[str, Any]) -> None:
        packet["decisions"]["CD-RT-5"]["defaultPosture"]["durableDefault"] = \
            "UNSELECTED"

    def reassert_pending(packet: dict[str, Any]) -> None:
        packet["knownLimitations"].append(
            "CD-RT-5 is intentionally unresolved because its required "
            "Phase-1A input is in flight.")

    return [
        ("revert-to-pending", revert),
        ("delete-decision", drop),
        ("duplicate-into-pending", duplicate_into_pending),
        ("substitute-decidedBy", author),
        ("substitute-decidedBy-plausible-human", author_human),
        ("blank-decidedOn", blank_date),
        ("substitute-decidedOn", substitute_date),
        ("placeholder-decidedBy", placeholder_author),
        ("placeholder-decidedOn", placeholder_date),
        ("flip-durableDefault", posture),
        ("flip-implicitDurableRetention", implicit),
        ("unselect-durableDefault", unselect_posture),
        ("flip-status", status),
        ("manufacture-signOff", signature),
        ("manufacture-positive-state", positive_state),
        ("nested-placeholder", nested_placeholder),
        ("packet-reasserts-pending-elsewhere", reassert_pending),
    ]


def guard_sweep() -> list[str]:
    """Prove the re-pointed guard fires, and that it is not indiscriminate."""
    failures: list[str] = []
    try:
        packet = load_json(HERE / PRODUCT)
    except Exception as exc:                          # noqa: BLE001 - reported
        return [f"cannot load {PRODUCT}: {type(exc).__name__}: {exc}"]
    packet_findings, _notices, packet_ok = product_packet_findings()
    if not packet_ok:
        return [f"the live packet does not satisfy the property guard, so this "
                f"sweep would not measure the shipped baseline: "
                f"{packet_findings[0] if packet_findings else 'unknown'}"]
    if cd_rt_5_findings(packet):
        failures.append("baseline: the live packet does not satisfy the "
                        "re-pointed CD-RT-5 guard")
    for label, mutate in _packet_mutations():
        mutated = copy.deepcopy(packet)
        try:
            mutate(mutated)
        except Exception as exc:                      # noqa: BLE001 - reported
            failures.append(f"mutation {label} failed to apply: "
                            f"{type(exc).__name__}: {exc}")
            continue
        if mutated == packet:
            failures.append(f"mutation {label} changed nothing")
            continue
        if not cd_rt_5_findings(mutated):
            failures.append(f"mutation {label} escaped the CD-RT-5 guard")
    # Two negative controls.  A guard that fires on everything proves nothing,
    # and the second one is the whole point of the property rewrite: a
    # COHERENT future amendment must be ADMITTED, not refused.
    unrelated = copy.deepcopy(packet)
    if isinstance(unrelated.get("knownLimitations"), list):
        unrelated["knownLimitations"].append("v11 negative control")
        if cd_rt_5_findings(unrelated):
            failures.append("negative control: the guard fired on an edit "
                            "outside $.decisions.CD-RT-5 that asserts nothing "
                            "about the retention state")
    coherent = copy.deepcopy(packet)
    posture = coherent.get("decisions", {}).get("CD-RT-5", {}).get(
        "defaultPosture")
    if isinstance(posture, dict):
        posture["durableDefault"] = "EPHEMERAL_ONLY"
        posture["implicitDurableRetention"] = "NO"
        if cd_rt_5_findings(coherent):
            failures.append("negative control: the guard refused a COHERENT "
                            "posture amendment; it is pinning values again")
    return failures


def selftest(candidate: Any, source: bytes, path: pathlib.Path) -> int:
    """The predecessor's full suite plus the re-pointed guard's own sweep."""
    predecessor, authority, findings, _state_ok = prepare()
    if predecessor is None:
        for finding in findings:
            print("FAIL:", finding)
        print("SELFTEST-REFUSED: the predecessor could not be admitted")
        print("SELFTEST-NOT-RUN: 0 mutations executed")
        return 3
    if findings:
        print("SELFTEST-REFUSED: this successor's own layers are not clean, so "
              "the mutation suite is not an oracle over them.")
        for finding in findings[:10]:
            print("  base-finding:", finding)
        print("SELFTEST-NOT-RUN: 0 mutations executed; exit 3 distinguishes "
              "this refusal from a green selftest and from an ordinary failure.")
        return 3
    sweep = guard_sweep()
    if sweep:
        for failure in sweep:
            print("SELFTEST-FAIL:", failure)
        print(f"SELFTEST-NOT-RUN: the predecessor suite was not reached; "
              f"{len(sweep)} CD-RT-5 guard failure(s) came first")
        return 1
    outcome = predecessor.selftest(candidate, source, authority, path)
    if outcome != 0:
        return outcome
    print(f"SELFTEST-PASS: {CHECKER} adds "
          f"{len(_packet_mutations())} CD-RT-5 authority mutations, all "
          "rejected, and 2 negative controls that stayed silent")
    print("  what a green selftest is NOT (freeze section 7.8) - measured ways "
          f"this checker can pass on a wrong artifact: "
          f"{len(KNOWN_PASSES_ON_WRONG_ARTIFACT)}")
    for row in KNOWN_PASSES_ON_WRONG_ARTIFACT:
        print(f"    {row}")
    return 0


def _live_decision_summary() -> str:
    """Report what the packet SAYS, measured this run - not what was authored."""
    try:
        packet = load_json(HERE / PRODUCT)
    except Exception as exc:                          # noqa: BLE001 - reported
        return f"unreadable ({type(exc).__name__})"
    decision = _dotted(packet, "decisions.CD-RT-5")
    if not isinstance(decision, dict):
        return "absent from $.decisions"
    return (f"{decision.get('status')!r} on {decision.get('decidedOn')!r} by "
            f"{decision.get('decidedBy')!r}; durableDefault="
            f"{_dotted(decision, 'defaultPosture.durableDefault')!r}; "
            f"implicitDurableRetention="
            f"{_dotted(decision, 'defaultPosture.implicitDurableRetention')!r}; "
            f"decision subtree sha256={cd_rt_5_digest(packet)}")


# ---------------------------------------------------------------------------
# Section 7.  Entry point.  The predecessor's declared argument contract.
# ---------------------------------------------------------------------------

DECLARED_FLAGS: tuple[str, ...] = ("--selftest", "--emit-candidate")


def _parse_argv(argv: Any) -> tuple[frozenset[str], Any]:
    if not isinstance(argv, (list, tuple)) or not argv:
        raise ValueError("no argument vector was supplied")
    flags: list[str] = []
    positional: list[Any] = []
    for item in list(argv)[1:]:
        if isinstance(item, str) and item.startswith("--"):
            if item not in DECLARED_FLAGS:
                raise ValueError(f"unknown flag {item!r}")
            flags.append(item)
        else:
            positional.append(item)
    if len(positional) > 1:
        raise ValueError(f"{len(positional)} positional candidate paths "
                         "supplied; exactly one is accepted")
    if DECLARED_FLAGS[0] in flags and DECLARED_FLAGS[1] in flags:
        raise ValueError(f"{DECLARED_FLAGS[0]} and {DECLARED_FLAGS[1]} are "
                         "mutually exclusive")
    if DECLARED_FLAGS[1] in flags and positional:
        raise ValueError(f"{DECLARED_FLAGS[1]} takes no candidate path")
    return frozenset(flags), (positional[0] if positional else None)


def main(argv: list[str]) -> int:
    try:
        flags, requested = _parse_argv(argv)
    except ValueError as exc:
        print(f"EV11-UNSUPPORTED-INVOCATION: {exc}", file=sys.stderr)
        return 2

    if "--emit-candidate" in flags:
        predecessor, authority, findings, _ok = prepare()
        if predecessor is None or findings:
            for finding in findings:
                print(f"FAIL: {finding}", file=sys.stderr)
            return 2
        try:
            sys.stdout.buffer.write(
                predecessor.pretty(predecessor.expected_successor(authority)))
        except Exception as exc:                      # noqa: BLE001 - reported
            print(f"cannot emit candidate: {type(exc).__name__}: {exc}",
                  file=sys.stderr)
            return 2
        return 0

    path = pathlib.Path(requested) if requested is not None else HERE / BINDING
    try:
        source = path.read_bytes()
        candidate = json.loads(source.decode("utf-8"), object_pairs_hook=_pairs)
    except (OSError, UnicodeError, json.JSONDecodeError,
            DuplicateKeyError) as exc:
        print(f"cannot load Evidence candidate: {type(exc).__name__}: {exc}",
              file=sys.stderr)
        return 2

    if "--selftest" in flags:
        return selftest(candidate, source, path)

    findings = check(candidate, source)
    for notice in _NOTICES:
        print(f"NOTICE: {notice}")
    if findings:
        print(f"{len(findings)} finding(s) in {path.name}:")
        for finding in findings:
            print("  -", finding)
        return 1

    print(f"Evidence v11 OK - {path.name}; check-evidence-v10.py executed from "
          f"verified bytes with the CD-RT-5 guard RE-POINTED at the DECIDED "
          f"state; {len(PINS)} inputs hash-verified here in addition to the "
          f"predecessor's own 24; {len(CHAIN)} chain levels enumerated and "
          "hard-compared")
    print("  live CD-RT-5: " + _live_decision_summary())
    print(f"  predecessor findings closed: "
          f"{', '.join(PREDECESSOR_FINDINGS_CLOSED)} - PR-07/PR-08/PR-26 by "
          "re-executing suites the predecessor ABORTED, not by suppressing "
          "their message; nothing is subtracted at the predecessor's own layer")
    print(f"  compared this run: {_LAST_CENSUS['green']}/"
          f"{_LAST_CENSUS['total']} predecessor probes green over its full "
          f"declared probe set; {_LAST_CENSUS['removed']} accounted RC-14 "
          "finding(s) removed inside check-versioning-v8.py's dependency "
          "loader and none anywhere else")
    print("  scope: author-side evidence that these bytes are self-consistent "
          "and that drift is caught. It is not evidence that any of them is "
          "right. Checker-scope evidence only; SPECIFIED / "
          "IMPLEMENTABLE_UNEXECUTED; CANDIDATE-NOT-APPLIED / "
          "AWAITING-INDEPENDENT-REVIEW; no seal, freeze, integration or "
          "product acceptance is declared here.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
