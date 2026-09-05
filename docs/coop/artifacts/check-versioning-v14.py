#!/usr/bin/env python3
"""VERSIONING register-validator successor: check-versioning-v8.py re-pointed
at the DECIDED CD-RT-5 product state.

WHY THIS FILE EXISTS
--------------------
`check-versioning-v8.py` is the registered VERSIONING validator
(`claim-register.v1.json` -> VERSIONING.validator; blueprint section 1.1) and
freeze section 9.1 asserts that it "exits 0".  On 2026-08-05 the product
authority `sfbreen` DECIDED `CD-RT-5`.  Applying that decision moved
`CD-RT-5` out of `product-dispositions.v1.json#pendingDecisions` and into
`#decisions`, and every checker that reached
`check-retention-custody.py::_authority_guard` began reporting

    RC-14: $product.CD-RT-5: exact live state must be BLOCKED_ON_PHASE_1A,
           got None
    RC-14: $contract.custodyPolicy: does not match live product authority

`check-versioning-v8.py` inherits both through two independent paths
(`check-versioning-v7.py` -> RT12 -> RT11 -> RT10, and RT13 -> RT12 -> RT11 ->
RT10) and now exits 1, falsifying the freeze section 9.1 claim.  Section 7.2
forbids editing it; section 7.6 records that immutability then prevents a
proven fix from propagating, and names the successor as the propagation
mechanism.  This file is that successor.

WHAT CHANGED, AND ONLY WHAT CHANGED
-----------------------------------
1.  The stale live-state assertion is RE-POINTED, not removed.  Section 4.4 is
    this corpus's forensic record of a FABRICATED `CD-RT-5` sign-off; the guard
    is what makes fabrication detectable, so deleting it would destroy the only
    mechanical defence section 4.4 built.  `cd_rt_5_findings()` below asserts
    the CURRENT decided state - `status`, `decidedBy`, `decidedOn`,
    `durableDefault`, `implicitDurableRetention` - plus a placeholder guard, a
    silent-revert guard, and a scoped re-implementation of RT10's
    manufactured-authority vocabulary walk.
2.  Findings that are EXACTLY the accounted RC-14 propagation are subtracted
    from the immutable chain's output, and only while the live packet is in the
    pinned decided state.  Every level of the chain is independently executed
    and its finding list is hard-compared against an enumerated expectation
    (`chain_audit`), so a NEW finding anywhere in the chain fails this checker
    instead of being swallowed with the accounted one.
3.  Candidate JSON is parsed through a duplicate-key-rejecting
    `object_pairs_hook` (section 7.5).  `check-versioning-v8.py` parses with a
    bare `json.loads`; its own inputs are sha-pinned, but the caller-supplied
    candidate was not defended.
4.  `--selftest` refusal is a distinct observable: a dirty base prints
    `SELFTEST-REFUSED` / `SELFTEST-NOT-RUN` and exits 3 (section 7.2, the
    EVIDENCE v8 dead-`--selftest` row).  The predecessor returned 1
    indistinguishably.

Everything else is the predecessor's, executed as the predecessor's own bytes:
`v8mod.check(value)` performs all six pin verifications, all three dependency
executions, and every structural assertion, unmodified.

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
A green run is AUTHOR-SIDE evidence that `versioning-policy.v8.json` says what
it says consistently, that the immutable RT/VERSIONING chain carries no finding
other than the accounted one, and that the live `CD-RT-5` record is byte-for-
byte the decision this file was written against.  It is NOT evidence that any
of those artifacts is RIGHT.  The measured ways this checker can pass on a
wrong artifact are enumerated in `KNOWN_PASSES_ON_WRONG_ARTIFACT` and printed
by `--selftest`.

NAME COLLISION HAZARD - READ BEFORE ASSUMING WHAT THIS FILE VALIDATES
---------------------------------------------------------------------
Everywhere else in this corpus `check-versioning-vN.py` validates
`versioning-policy.vN.json` (v13 -> v13, v12 -> v12, ...).  THIS FILE DOES NOT.
Its subject is `versioning-policy.v8.json`, because its subject is whatever the
claim register names as the VERSIONING validator's subject, and the register
names `artifacts/check-versioning-v8.py`.

The hazard is live.  A concurrent lane published
`versioning-policy.v14.json` at 18:29 on 2026-08-05, four minutes after this
file was created - `artifact: opensip.versioning-policy, version: 14,
supersedes: 8, status: CANDIDATE-NOT-APPLIED, reviewState:
AWAITING-INDEPENDENT-REVIEW`.  A reader who applies the corpus convention will
expect this file to validate that artifact.  IT DOES NOT, AND MUST NOT BE READ
AS DOING SO.  This filename was specified in this lane's brief; the collision
is recorded here rather than resolved by renaming, because renaming was outside
what this lane was authorised to do.

Usage: python3 -I -B artifacts/check-versioning-v14.py [candidate] [--selftest]
Exit: 0 clean; 1 findings; 2 I/O, JSON or invocation error;
      3 selftest refused because the base is not clean.
"""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import pathlib
import datetime
import re
import sys
import types
from typing import Any, Callable


HERE = pathlib.Path(__file__).resolve().parent
CHECKER = "check-versioning-v14.py"
BINDING = "versioning-policy.v8.json"
PREDECESSOR_CHECKER = "check-versioning-v8.py"
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
# IMPLEMENTATION-FREEZE.md and IMPLEMENTER-BLUEPRINT.md are deliberately NOT
# pinned.  Both were under concurrent edit while this file was authored, so a
# pin on either would be an environment dependency that fails for reasons
# unrelated to VERSIONING (freeze section 4.5 records exactly that outcome for
# check-retention-custody-v23/-v24, which went to exit 2 RT23-PIN-REFUSED and
# silently disabled their own FREEZE_ANCHORS content guard).  This checker
# therefore asserts nothing about either document's bytes and must not be read
# as guarding them.
# ---------------------------------------------------------------------------
PINS: dict[str, str] = {
    # the predecessor whose behaviour this file reproduces
    PREDECESSOR_CHECKER:
        "82834720a8fd4ec8701dad2b43ad94d6ad9e52d21aeb077f4286fab5fb156844",
    BINDING:
        "ea4b52b5a4d187ec35ad994d8ffcd888db287566c8fb53f3df17e5203d84ae2e",
    # the immutable chain whose findings are enumerated and accounted
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
}



# The exact, fully enumerated RC-14 propagation the decision made stale.  These
# strings compose level by level: a change to any message text, to the live
# product state embedded in the root message, or to the number of findings at
# any level, breaks the hard comparison in chain_audit() and fails this file.
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

# (checker, subject artifact, module alias, exactly these findings and no others)
CHAIN: tuple[tuple[str, str, str, tuple[str, ...]], ...] = (
    ("check-retention-custody.py", "retention-tiers.v10.json",
     "rt10_for_versioning_v14", (RC14_ROOT_LIVE_STATE, RC14_ROOT_CUSTODY)),
    ("check-retention-custody-v11.py", "retention-tiers.v11.json",
     "rt11_for_versioning_v14", (RC14_RT11,)),
    ("check-retention-custody-v12.py", "retention-tiers.v12.json",
     "rt12_for_versioning_v14", (RC14_RT12,)),
    ("check-retention-custody-v13.py", "retention-tiers.v13.json",
     "rt13_for_versioning_v14", (RC14_RT13,)),
    ("check-versioning-v7.py", "versioning-policy.v7.json",
     "ver7_for_versioning_v14", (RC14_VER7,)),
)

# What the predecessor's own two sub-checker executions produce today.  Both are
# hard-compared before any subtraction is applied.
ACCOUNTED_PREDECESSOR_FINDINGS: tuple[str, ...] = (RC14_VER8_A, RC14_VER8_B)

# Which module's check() output may have which accounted findings removed, and
# nothing else may be removed anywhere.
ACCOUNTED_BY_CHECKER: dict[str, tuple[str, ...]] = {
    "check-versioning-v7.py": (RC14_VER7,),
    "check-retention-custody-v13.py": (RC14_RT13,),
}

# freeze section 4.5: "Four artifacts still assert the pre-decision state ...
# versioning-policy.v8 ... each closable by exactly one successor."  This file
# is a checker; it cannot close an artifact.  The staleness is owned by
# check-product-dispositions-v2.py, which reports it as PD2-SCAN-CONFLICT.
#
# This file publishes NO claim about that instrument's exit code, deliberately.
# A figure about another checker's verdict is a recorded measurement nothing
# here recomputes, and section 7.2.2's rider is that a measurement which cannot
# fail the build is prose.  An earlier revision of this comment asserted that
# check-product-dispositions-v2.py "must stay red"; measured live at
# 2026-08-06T01:47Z it exits 0, because a concurrent lane published
# versioning-policy.v14.json and v10-disposition.v2.json and both conflicts
# reclassified from blocking to historical.  That is exactly the failure this
# note now avoids repeating, and the withdrawal is recorded in place.
#
# What this file DOES do is hard-compare the pair: if the artifact's frozen
# value moves, the predecessor's own dischargeStatus comparison fails; if the
# live value moves, cd_rt_5_findings() fails.  The accounted pair is the only
# silent one.
ACCOUNTED_STALE_ARTIFACT_VALUE = "BLOCKED"

# section 7.8: the operative question is "can I make this checker pass on a
# wrong artifact?"  These are the ways found while writing it.  A count that is
# not enumerated is not a measurement.
KNOWN_PASSES_ON_WRONG_ARTIFACT: tuple[str, ...] = (
    "1. A string leaf in versioning-policy.v8.json whose VALUE is false while "
    "its PATH and TYPE are unchanged, at any position the predecessor binds by "
    "containment rather than by equality (its forbiddenBackEdge, identityRule, "
    "cold rule and productRestartClaim terms are all `in` tests): keep every "
    "required needle and append a reversing sentence. Freeze section 7.8 "
    "measured 13 of 13 such negations escaping a sibling instrument.",
    "2. A COHERENT amendment. Changing BOTH posture fields together, or "
    "substituting decidedBy AND rewriting the narrative that names it, passes "
    "every property gate. The guard binds internal consistency, not truth.",
    "3. Prose inside $.decisions.CD-RT-5 that contradicts the decision it "
    "records, anywhere the packet does not repeat a checked field. The digest "
    "notice reports that such prose moved; it does not fail the build.",
    "4. The accounted RC-14 subtraction is justified by string equality against "
    "an enumerated expectation. A future chain finding whose text happens to "
    "equal an accounted string would be removed. No such collision exists "
    "today; nothing prevents one.",
    "5. This file inherits the predecessor's blindness to anything "
    "versioning-policy.v8.json does not declare. Neither instrument can observe "
    "a VERSIONING obligation that the artifact simply omits.",
    "6. Edits to product-dispositions.v1.json OUTSIDE $.decisions.CD-RT-5 are "
    "not bound here, by deliberate scope: this file is not the whole packet's "
    "guard, check-product-dispositions-v2.py is. The one exception is the "
    "cross-packet coherence gate, which fires when another position asserts "
    "the pre-decision state unmarked.",
)


class DuplicateKeyError(ValueError):
    """A JSON object repeated a key; the document is not canonical."""


class Refused(Exception):
    """An input could not be admitted."""


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


def _module(filename: str, alias: str) -> types.ModuleType:
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
            f"VER14-CDRT5-DIGEST-MOVED (NOTICE, not a finding): "
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
                    f"VER14-CDRT5-VALUE-MOVED (NOTICE, not a finding): "
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
        return [f"VER14-CDRT5-SHAPE: product packet root is not an object"]

    decisions = packet.get("decisions")
    pending = packet.get("pendingDecisions")
    if not isinstance(decisions, dict):
        out.append(f"VER14-CDRT5-SHAPE: $.decisions is not an object")
    if pending is not None and not isinstance(pending, dict):
        out.append(f"VER14-CDRT5-SHAPE: $.pendingDecisions is not an object")

    in_decided = isinstance(decisions, dict) and "CD-RT-5" in decisions
    in_pending = isinstance(pending, dict) and "CD-RT-5" in pending

    if in_decided and in_pending:
        out.append(
            f"VER14-CDRT5-DUPLICATED: CD-RT-5 appears in BOTH $.decisions and "
            "$.pendingDecisions; a row is in exactly one state and a duplicate "
            "lets a reader pick the answer they prefer")
    if in_pending and not in_decided:
        entry = pending["CD-RT-5"]
        state = entry.get("status") if isinstance(entry, dict) else entry
        out.append(
            f"VER14-CDRT5-REVERTED: CD-RT-5 is in $.pendingDecisions with "
            f"status {state!r} and not in $.decisions; the decision has been "
            "reverted")
    if not in_decided and not in_pending:
        out.append(
            f"VER14-CDRT5-ABSENT: CD-RT-5 is in neither $.decisions nor "
            "$.pendingDecisions; the binding packet no longer carries the row "
            "at all")
    if not in_decided:
        return out

    decision = decisions["CD-RT-5"]
    if not isinstance(decision, dict):
        out.append(f"VER14-CDRT5-SHAPE: {DECISION_PATH} is "
                   f"{type(decision).__name__}, not an object")
        return out

    # -- the row is under $.decisions, so it must BE a decision --------------
    status = decision.get("status")
    if status not in DECIDED_STATUSES:
        out.append(
            f"VER14-CDRT5-STATUS: {DECISION_PATH}.status is {status!r}; a row "
            f"under $.decisions must carry one of {sorted(DECIDED_STATUSES)!r}")

    leaves = list(_string_leaves(decision, DECISION_PATH))

    # -- authority: filled, by a named authority, on a real date ------------
    decided_by = decision.get("decidedBy")
    if not isinstance(decided_by, str) or not decided_by.strip():
        out.append(f"VER14-CDRT5-AUTHORITY: {DECISION_PATH}.decidedBy is not a "
                   f"non-empty string ({decided_by!r})")
    elif _is_placeholder(decided_by):
        out.append(
            f"VER14-CDRT5-PLACEHOLDER: {DECISION_PATH}.decidedBy is an "
            f"unfilled placeholder ({decided_by!r}); a prepared amendment may "
            "not read as a taken decision")
    else:
        normalized = re.sub(r"[^a-z]", "", decided_by.lower())
        if normalized in NON_AUTHORITY_DECIDERS:
            out.append(
                f"VER14-CDRT5-AUTHORITY: {DECISION_PATH}.decidedBy is "
                f"{decided_by!r}, a role the corpus records as unable to "
                "constitute a product decision (freeze section 4.4: a "
                "recommendation converted into a declaration)")
        elif len(decided_by.strip()) < 3:
            out.append(f"VER14-CDRT5-AUTHORITY: {DECISION_PATH}.decidedBy is "
                       f"too short to identify an authority ({decided_by!r})")
        else:
            corroborating = [
                path for path, text in leaves
                if path != f"{DECISION_PATH}.decidedBy" and decided_by in text]
            if not corroborating:
                out.append(
                    f"VER14-CDRT5-UNCORROBORATED: {DECISION_PATH}.decidedBy is "
                    f"{decided_by!r} and no other leaf of the decision names "
                    "it. Freeze section 4.4's fabrication was a single-source "
                    "attribution; a bare authority field is that shape.")

    decided_on = decision.get("decidedOn")
    if not isinstance(decided_on, str) or not decided_on.strip():
        out.append(f"VER14-CDRT5-AUTHORITY: {DECISION_PATH}.decidedOn is not a "
                   f"non-empty string ({decided_on!r})")
    elif _is_placeholder(decided_on):
        out.append(
            f"VER14-CDRT5-PLACEHOLDER: {DECISION_PATH}.decidedOn is an "
            f"unfilled placeholder ({decided_on!r})")
    else:
        try:
            when = datetime.date.fromisoformat(decided_on)
        except ValueError:
            when = None
            out.append(f"VER14-CDRT5-AUTHORITY: {DECISION_PATH}.decidedOn is "
                       f"not a real ISO-8601 calendar date ({decided_on!r})")
        if when is not None:
            authored = packet.get("date")
            if isinstance(authored, str):
                try:
                    if when < datetime.date.fromisoformat(authored):
                        out.append(
                            f"VER14-CDRT5-AUTHORITY: {DECISION_PATH}.decidedOn "
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
                    f"VER14-CDRT5-UNCORROBORATED: {DECISION_PATH}.decidedOn is "
                    f"{decided_on!r} and no other leaf of the decision names "
                    "it.")

    # -- posture: selected, and internally coherent -------------------------
    durable = _dotted(decision, "defaultPosture.durableDefault")
    implicit = _dotted(decision, "defaultPosture.implicitDurableRetention")
    if not isinstance(durable, str) or durable.strip().upper() in \
            UNSELECTED_POSTURES or _is_placeholder(durable):
        out.append(
            f"VER14-CDRT5-POSTURE: "
            f"{DECISION_PATH}.defaultPosture.durableDefault is {durable!r}; a "
            "decided row must select a posture")
    elif not isinstance(implicit, str) or _is_placeholder(implicit):
        out.append(
            f"VER14-CDRT5-POSTURE: "
            f"{DECISION_PATH}.defaultPosture.implicitDurableRetention is "
            f"{implicit!r}; a decided row must state it")
    else:
        expected = IMPLICIT_WHEN_DURABLE if durable == DURABLE_POSTURE \
            else IMPLICIT_WHEN_NOT_DURABLE
        if implicit != expected:
            out.append(
                f"VER14-CDRT5-POSTURE-INCOHERENT: durableDefault={durable!r} "
                f"requires implicitDurableRetention={expected!r}, packet says "
                f"{implicit!r}. The two posture fields disagree, so one of them "
                "was changed without the other.")

    # -- no unfilled placeholder anywhere in the decision --------------------
    for path, text in leaves:
        if path in (f"{DECISION_PATH}.decidedBy", f"{DECISION_PATH}.decidedOn"):
            continue
        if _is_placeholder(text):
            out.append(
                f"VER14-CDRT5-PLACEHOLDER: {path} carries an unfilled "
                f"placeholder ({text[:72]!r}); a prepared amendment may not "
                "read as a taken decision")

    # -- a decision is not a signature (freeze section 4.5) -----------------
    def walk(node: Any, path: str) -> None:
        if isinstance(node, dict):
            for key, child in node.items():
                normalized = re.sub(r"[^a-z]", "", str(key).lower())
                if normalized in _FORBIDDEN_AUTHORITY_KEYS:
                    out.append(
                        f"VER14-CDRT5-FABRICATION: {path}.{key} manufactures a "
                        "product signature; freeze section 4.5 - a decision is "
                        "not a signature, and section 11's Product signer line "
                        "is still [UNSET]")
                if isinstance(child, str) and normalized in _STATE_KEYS:
                    value = re.sub(r"[^A-Z]", "", child.upper())
                    if value in _FORBIDDEN_AUTHORITY_VALUES:
                        out.append(
                            f"VER14-CDRT5-FABRICATION: {path}.{key} declares "
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
            f"VER14-CDRT5-PACKET-INCOHERENT: {path} still asserts the "
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
        return ([f"VER14-PACKET-UNREADABLE: {PRODUCT}: "
                 f"{type(exc).__name__}: {exc}"], [], False)
    findings = cd_rt_5_findings(packet)
    return findings, cd_rt_5_notices(packet), (not findings)


# ---------------------------------------------------------------------------
# Layer 2.  The immutable chain, enumerated level by level.
# ---------------------------------------------------------------------------

def chain_audit(state_ok: bool) -> list[str]:
    """Execute every level of the RC-14 chain and hard-compare its findings.

    Section 7.2.2: a recorded measurement must be compared to the measurement it
    records.  The accounted RC-14 propagation is a recorded measurement of these
    exact bytes, so it is compared, not narrated.  A level that grows a finding,
    loses one, or changes its wording fails here - which is what makes the
    subtraction in `_AccountedLoader` safe.
    """
    out: list[str] = []
    for checker, subject, alias, expected in CHAIN:
        try:
            module = _module(checker, alias)
            value = load_json(HERE / subject)
            findings = module.check(value)
        except Exception as exc:                      # noqa: BLE001 - reported
            out.append(f"VER14-CHAIN-RAISED: {checker} on {subject} raised "
                       f"{type(exc).__name__}: {exc}")
            continue
        if not isinstance(findings, list):
            out.append(f"VER14-CHAIN-SHAPE: {checker} did not return a list")
            continue
        wanted = list(expected) if state_ok else []
        if list(findings) != wanted:
            out.append(
                f"VER14-CHAIN-DRIFT: {checker} on {subject} reported "
                f"{len(findings)} finding(s), expected exactly {len(wanted)} "
                f"accounted; unaccounted="
                f"{[f for f in findings if f not in wanted]!r}; "
                f"missing={[f for f in wanted if f not in findings]!r}")
    return out


class _AccountedCheck:
    """A pinned module with exactly the accounted RC-14 findings removed.

    Nothing else is removed, from nothing else, and only while the live packet
    is in the pinned decided state.  The predecessor loads its three dependency
    modules through its own module-level `module()` helper; substituting that
    helper re-points the guard at the exact site the decision made false while
    leaving every other assertion the predecessor makes running on its own
    bytes.
    """

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


def _install_accounted_loader(predecessor: types.ModuleType,
                              enabled: bool) -> list[_AccountedCheck]:
    original: Callable[..., types.ModuleType] = predecessor.module
    proxies: list[_AccountedCheck] = []

    def loader(filename: str, alias: str) -> Any:
        module = original(filename, alias)
        accounted = ACCOUNTED_BY_CHECKER.get(filename) if enabled else None
        if not accounted:
            return module
        proxy = _AccountedCheck(module, accounted)
        proxies.append(proxy)
        return proxy

    predecessor.module = loader
    return proxies


# ---------------------------------------------------------------------------
# Layer 3.  Composition.
# ---------------------------------------------------------------------------

def _pin_findings() -> list[str]:
    out: list[str] = []
    for name, expected in sorted(PINS.items()):
        try:
            actual = sha_file(name)
        except OSError as exc:
            out.append(f"VER14-PIN-UNREADABLE: {name}: "
                       f"{type(exc).__name__}: {exc}")
            continue
        if actual != expected:
            out.append(f"VER14-PIN-DRIFT: {name} is {actual}, pinned {expected}")
    return out


def _accounted_staleness_findings(value: Any, state_ok: bool) -> list[str]:
    """Hard-compare the one divergence freeze section 4.5 already accounts for.

    versioning-policy.v8.json#dischargeStatus.CD-RT-5 is frozen at "BLOCKED"
    while the live packet records DECIDED.  Closing that needs a
    versioning-policy successor, not a checker; check-product-dispositions-v2.py
    already reports it as a genuine PD2-SCAN-CONFLICT and must stay red.  What
    is silent here is exactly one pair of values, and both halves are compared.
    """
    if not state_ok:
        return []
    frozen = _dotted(value if isinstance(value, dict) else {},
                     "dischargeStatus.CD-RT-5")
    if frozen != ACCOUNTED_STALE_ARTIFACT_VALUE:
        return [f"VER14-ACCOUNTED-STALENESS-DRIFT: {BINDING}"
                f"$.dischargeStatus.CD-RT-5 is {frozen!r}, accounted "
                f"{ACCOUNTED_STALE_ARTIFACT_VALUE!r}; the divergence freeze "
                "section 4.5 records is no longer the one this file accounts"]
    return []


def check(value: Any, *, verify_files: bool = True) -> list[str]:
    """Everything check-versioning-v8.py does, plus the re-pointed guard."""
    findings: list[str] = []
    findings.extend(_pin_findings())

    packet_findings, packet_notices, state_ok = product_packet_findings()
    findings.extend(packet_findings)
    _NOTICES[:] = packet_notices

    if verify_files:
        findings.extend(chain_audit(state_ok))

    try:
        predecessor = _module(PREDECESSOR_CHECKER, "versioning_v8_for_v14")
    except Exception as exc:                          # noqa: BLE001 - reported
        findings.append(f"VER14-PREDECESSOR-IMPORT: {PREDECESSOR_CHECKER}: "
                        f"{type(exc).__name__}: {exc}")
        return findings

    if verify_files:
        # Measure the UNREPAIRED predecessor first, and hard-compare it.  This
        # is what makes the subtraction auditable rather than trusted: the
        # accounted set is a recorded measurement of these bytes and is
        # compared to the measurement it records (section 7.2.2).
        try:
            raw = predecessor.check(copy.deepcopy(value))
        except Exception as exc:                      # noqa: BLE001 - reported
            findings.append(f"VER14-PREDECESSOR-RAISED: unrepaired "
                            f"{PREDECESSOR_CHECKER}.check raised "
                            f"{type(exc).__name__}: {exc}")
            raw = None
        if isinstance(raw, list):
            wanted = list(ACCOUNTED_PREDECESSOR_FINDINGS) if state_ok else []
            if sorted(raw) != sorted(wanted):
                findings.append(
                    f"VER14-PREDECESSOR-DRIFT: unrepaired "
                    f"{PREDECESSOR_CHECKER} reported {len(raw)} finding(s), "
                    f"expected exactly {len(wanted)} accounted; unaccounted="
                    f"{[f for f in raw if f not in wanted]!r}; "
                    f"missing={[f for f in wanted if f not in raw]!r}")
        elif raw is not None:
            findings.append(
                f"VER14-PREDECESSOR-SHAPE: {PREDECESSOR_CHECKER}.check did not "
                "return a list")

    proxies = _install_accounted_loader(predecessor, enabled=state_ok)
    try:
        repaired = predecessor.check(value, verify_files=verify_files)
    except Exception as exc:                          # noqa: BLE001 - reported
        findings.append(f"VER14-PREDECESSOR-RAISED: repaired "
                        f"{PREDECESSOR_CHECKER}.check raised "
                        f"{type(exc).__name__}: {exc}")
        repaired = []
    if not isinstance(repaired, list):
        findings.append(f"VER14-PREDECESSOR-SHAPE: {PREDECESSOR_CHECKER}.check "
                        "did not return a list")
        repaired = []
    findings.extend(repaired)

    if verify_files and state_ok:
        removed = sorted({f for proxy in proxies for f in proxy.removed})
        if removed != sorted({RC14_VER7, RC14_RT13}):
            findings.append(
                "VER14-SUBTRACTION-DRIFT: the accounted RC-14 removals were "
                f"{removed!r}; expected exactly one per dependency chain. A "
                "subtraction that does not fire is a guard that is not "
                "load-bearing.")

    findings.extend(_accounted_staleness_findings(value, state_ok))
    return findings


# ---------------------------------------------------------------------------
# Layer 4.  Selftest.
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


def selftest(value: Any) -> list[str]:
    """Predecessor mutation suite + re-pointed-guard mutation sweep."""
    failures: list[str] = []

    try:
        predecessor = _module(PREDECESSOR_CHECKER, "versioning_v8_selftest_v14")
    except Exception as exc:                          # noqa: BLE001 - reported
        return [f"cannot import {PREDECESSOR_CHECKER}: "
                f"{type(exc).__name__}: {exc}"]
    _packet_findings, _notices, state_ok = product_packet_findings()
    _install_accounted_loader(predecessor, enabled=state_ok)

    # The predecessor's own 15 successor mutations, run against the repaired
    # dependency loader so they measure what they were written to measure.
    inherited = predecessor.selftest(copy.deepcopy(value))
    failures.extend(f"inherited: {row}" for row in inherited)

    # The re-pointed guard, proved non-vacuous against the live packet.
    try:
        packet = load_json(HERE / PRODUCT)
    except Exception as exc:                          # noqa: BLE001 - reported
        return failures + [f"cannot load {PRODUCT}: {type(exc).__name__}: {exc}"]
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

    # A guard that fires on everything is as useless as one that fires on
    # nothing.  An unrelated edit elsewhere in the packet must NOT be reported
    # by the semantic layer (the digest pin is what covers the whole file).
    # Two negative controls.  A guard that fires on everything proves nothing,
    # and the second one is the whole point of the property rewrite: a
    # COHERENT future amendment must be ADMITTED, not refused.
    unrelated = copy.deepcopy(packet)
    if isinstance(unrelated.get("knownLimitations"), list):
        unrelated["knownLimitations"].append("v14 negative control")
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
# Layer 5.  Entry point.
# ---------------------------------------------------------------------------

def main(argv: list[str]) -> int:
    arguments = list(argv[1:])
    flags = [item for item in arguments if item.startswith("--")]
    positional = [item for item in arguments if not item.startswith("--")]
    if any(flag != "--selftest" for flag in flags) or len(positional) > 1:
        print(f"VER14-UNSUPPORTED-INVOCATION: usage: python3 -I -B "
              f"artifacts/{CHECKER} [candidate] [--selftest]", file=sys.stderr)
        return 2

    path = pathlib.Path(positional[0]) if positional else HERE / BINDING
    try:
        value = load_json(path)
    except (OSError, UnicodeError, json.JSONDecodeError,
            DuplicateKeyError) as exc:
        print(f"ERROR: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2

    findings = check(value)
    for notice in _NOTICES:
        print(f"NOTICE: {notice}")
    if findings:
        for finding in findings:
            print(f"FAIL: {finding}")
        if "--selftest" in flags:
            print("SELFTEST-REFUSED: the base candidate is not clean")
            print("SELFTEST-NOT-RUN: no mutation was executed")
            return 3
        return 1

    if "--selftest" in flags:
        failures = selftest(value)
        if failures:
            for failure in failures:
                print(f"SELFTEST-FAIL: {failure}")
            return 1
        print(f"PASS: {path.name}; predecessor's 15 successor mutations "
              f"rejected; {len(_packet_mutations())} CD-RT-5 authority "
              "mutations rejected; 2 negative controls silent")
        print("  what a green selftest is NOT (freeze section 7.8) - measured "
              f"ways this checker can pass on a wrong artifact: "
              f"{len(KNOWN_PASSES_ON_WRONG_ARTIFACT)}")
        for row in KNOWN_PASSES_ON_WRONG_ARTIFACT:
            print(f"    {row}")
        return 0

    print(f"PASS: {path.name}; VERSIONING v8 re-pointed at the DECIDED "
          f"CD-RT-5 state; {len(PINS)} inputs hash-verified; "
          f"{len(CHAIN)} chain levels enumerated; "
          f"{len(ACCOUNTED_PREDECESSOR_FINDINGS)} accounted RC-14 findings "
          "subtracted and no others")
    print("  live CD-RT-5: " + _live_decision_summary())
    print(f"  accounted, NOT closed: {BINDING}$.dischargeStatus.CD-RT-5 is "
          f"{ACCOUNTED_STALE_ARTIFACT_VALUE!r} while the live packet records "
          "DECIDED. Freeze section 4.5 lists this artifact as closable by "
          "exactly one successor, and a checker is not one. Both halves of "
          "that pair are hard-compared here; no claim is made about any other "
          "instrument's exit code.")
    print(f"  NAME COLLISION: this file's subject is {BINDING}, NOT "
          "versioning-policy.v14.json, despite the corpus convention that "
          "check-versioning-vN.py validates versioning-policy.vN.json. See "
          "the module docstring.")
    print("  scope: author-side evidence that these bytes are self-consistent "
          "and that drift is caught. It is not evidence that any of them is "
          "right. No seal, freeze, integration or product acceptance is "
          "declared here.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
