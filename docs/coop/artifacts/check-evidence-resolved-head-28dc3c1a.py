#!/usr/bin/env python3
"""Retained validator for the RESOLVED HEAD of the EVIDENCE identity lineage.

SUBJECT
-------
`artifacts/evidence.v15.json` (sha256
`28dc3c1aaa97f723afa8c079682a43999ca5c79686e7cde0f11e38421a179b29`), the head of
the delta chain

    v15 -> v14 -> v13 -> v12 -> v11 -> v10

whose TERMINUS `evidence.v10.json` (`62a3a071…`) is the full-text standalone
(freeze section 7.3's terminus rule: resolution stops at the reviewed standalone
rather than recursing through its narrative).  `evidence.v15` was independently
ACCEPTED at 0 blockers (`evidence.v15.review-independent.json`, verdict
`3018c2f9…`).  The resolved effective contract's canonical digest is
`4976151e6ccfd6fd25487e2ebf9e20af3b971e5bc4879b66f11b11c43ba3c573` under
`check-completeness-v2.py::canonical_bytes`.

`DR-002` AC-3 requires the binding artifact and its validator to move together.
This file is that validator.  It is a NEW FILE and edits nothing: freeze section
7.2 forbids editing reviewed bytes and section 7.6 records that immutability is
what makes a successor instrument the propagation mechanism.


WHY THIS FILE IS NOT NAMED `check-evidence-v11.py`
--------------------------------------------------
THE RULE (D-001 NOTE-1, adopted as a standing instruction): a checker's version
number is ITS OWN, never its subject's.  `check-evidence-v11.py` already exists
and it is *evidence.v10*'s checker -- the eleventh instrument of the
`check-evidence` lineage, re-pointed at the DECIDED `CD-RT-5` product state.  It
is NOT a checker of `evidence.v11`.  That collision is the corpus's recorded
naming trap, and naming this file `check-evidence-v11.py` would both collide
with a live instrument and assert a subject it does not have.

THE RATIONALE FOR THE NAME CHOSEN.  Every `check-evidence-vN.py` slot reproduces
the trap by construction: `N` reads as an instrument ordinal to one reader and as
a subject version to the next, and `evidence.v4 … evidence.v15` all exist as real
subject versions.  So this instrument takes NO `-vN` token at all.  It is
CONTENT-ADDRESSED by the first eight hex digits of the subject it validates:

    check-evidence-resolved-head-28dc3c1a.py

  * `28dc3c1a` is the sha256 prefix of `evidence.v15.json`.  A digest prefix
    cannot be misread as a version number in either direction, so the trap is
    structurally unavailable rather than merely avoided.
  * `resolved-head` states the subject exactly: this validates the RESOLVED head
    of the lineage -- the delta file AND the effective contract it materialises
    -- not any single delta in isolation.
  * The name collides with no existing instrument (`ls check-evidence*` measured
    at authoring: `check-evidence.py`, `-v4` … `-v11`) and with no subject
    version.
  * When the lineage advances, this name goes STALE-BUT-HONEST: it still names
    exactly the bytes it was built to validate, which is the property a version
    number in the subject's namespace does not have.

The content-addressed form follows the corpus's own precedent: the CONTENT
identity branch of `check-completeness-v2.py::declaration_fields` already holds
that "a name is redundant when a digest is present -- the digest IS the
identity".


1. THE GATED RESOLVER BYTES (freeze section 7.10 lesson)
--------------------------------------------------------
This instrument does not reimplement the corpus resolver.  It EXECUTES the two
reviewed resolvers, and it PINS THEM BY DIGEST first:

    check-completeness.py     af9f8837a5abc561cefebf071b862e2dd5fb427304f4738f7fadf5872c4f0f1f
    check-completeness-v2.py  dbe1e6955f66b0ccb032df115ca03fa780895b129b51fb39a49593581901bfb9

Both digests were MEASURED at authoring against the live tree and independently
against `git show c06eaea:` -- the commit whose dialect-repair review
(`b161c7e6…`) returned PASS -- and the two measurements are byte-identical.  The
pins are therefore the REVIEWED bytes, not merely the current ones.

IF EITHER GATED FILE IS ABSENT OR FAILS ITS HASH THIS INSTRUMENT REFUSES: exit
4, `EVRH-GATE-01`, naming the file, the gated pin and the measured digest.  It
NEVER guesses, never falls back to a second read, and never resolves anything
with unverified resolver bytes.  Absence and hash failure are ONE class here
because the resolved head defines them as one: its `exitDiscipline` names "an
integrity failure of the trust root -- a pinned dependency missing or failing
its hash".

**A REFUSAL HERE IS CORRECT FREEZE SECTION 7.8.1 BEHAVIOUR, NOT A DEFECT.**  The
retention row for `retention-tiers.v28` records the precedent in bytes:
`check-retention-custody-v28.py` now permanently refuses at exit 2 because the
dialect-repaired resolvers moved under its gated pins, and the recorded reading
is "correct section 7.8.1 behavior, not a defect", with a successor that gates
the reviewed bytes named as the repair.  This file IS that successor pattern
applied to the EVIDENCE surface.  If a future reviewed repair moves either
resolver, this instrument refuses loudly and a successor re-gates the new
reviewed digests.  Section 7.8.1 rule 1 is the whole of it: a missing or altered
REQUIRED input must refuse, never proceed on a default, because "derived from
nothing" and "derived and found nothing" must never print the same.

The verified bytes are executed from the SNAPSHOT that was hashed -- compiled
from the same `bytes` object that produced the digest -- so the bytes verified
and the bytes executed cannot diverge across a second read.


2. WHAT A GREEN RUN PROVES, AND WHAT IT DOES NOT
-------------------------------------------------
Freeze section 7.8's bound, stated in its own terms:

    A GREEN RUN PROVES: this artifact says what it says, consistently, and
    drift will be caught.

    A GREEN RUN DOES NOT PROVE: that this artifact is RIGHT.

These instruments bind structure, type, digest and stated-invariant coherence.
They never bind the truth of content.  A coherent lie -- an amendment that moves
a sentence AND its citation AND the digest that covers it, together -- is
admitted, and that boundary is section 7.8's, not a shortfall of this file.

WHAT THIS INSTRUMENT DOES NOT DO, enumerated so no reader has to infer it:

  * It has NO claim-register motion authority.  It moves nothing in
    `claim-register.v1.json`, grants no seal, no freeze, no application, no
    product acceptance, and does not sign `CD-RT-5`.
  * It is NOT the section 3.1 Phase-1A packet and supplies no part of it.
  * It is NOT a review.  Independent review of these instrument bytes remains
    REQUIRED.  A green run of an author's own checker is checker-scope evidence
    only.
  * It does not adjudicate `evidence.v15`'s findings, does not apply it, and
    does not change its `CANDIDATE-NOT-APPLIED` / `DO-NOT-SEAL` posture.  It
    ASSERTS that posture and fails if it silently moves.
  * It measures nothing about production durability, atomicity, restart, crash
    or concurrency behaviour.

SELF-SCANS ARE TRIPWIRES; THE EXECUTABLE PROBES ARE THE ORACLE.  The resolved
head's `retainedResiduals[13]` is binding on this instrument and is restated
here in its own words: the source self-scans (`EVRH-MODE-05/06/07`) prove
properties of THIS FILE'S SYNTAX, never of its semantics.  They are drift
tripwires for their measured coverage only.  The executable probes -- the chain
resolution, the recomputed digests, the mutation battery -- are the semantic
oracle.  The head's two measured evasions of the same scan family are therefore
inherited here and are NOT claimed closed: a dispatch reached through an ALIAS
whose gate puts no undocumented flag literal inside a comparison node evades the
flag scan in both measured forms (alias-plus-DECLARED-compared-literal and
alias-plus-non-compared-gate), and a path consumer reached through any
indirection evades a guard scan.  This file adds one vacuity guard the head's
residual invites -- a comparison-node scan that collects ZERO flag literals is
reported as indistinguishable from a vacuous scan -- and claims nothing beyond
that.

The tripwires are nonetheless PROVEN TO FIRE rather than merely observed to
pass.  A scan that has only ever been seen to pass is indistinguishable from one
that measures nothing, so `--selftest` runs four SOURCE self-mutations against a
deliberately broken copy of this file's own syntax tree -- in memory, writing no
file at all -- and requires the corresponding scan to report each: an
undocumented flag literal reaching a comparison node, every flag literal removed
from every comparison node, a second undocumented selftest dispatch, and an
unconditional finding gate inserted in front of the suite.  The head's
`escapeRule` governs these too: a syntax-tree mutation that does not change the
tree, or that its scan does not report, is an ESCAPE, never a pass.


3. THE MODE CONTRACT IS THE RESOLVED HEAD'S OWN
------------------------------------------------
`checkerModeContract` and `hostileInputTotalityContract.exitDiscipline` are read
FROM THE RESOLVED BYTES and hard-compared against this file's behaviour; the
values below are not transcribed constants that could drift from their source.

EXIT CODES.  The four dispositions are the resolved head's `exitCodes` table,
MEASURED, not invented.  The banner and every `return` read from one `EXIT`
table (freeze section 7.8.1 rule 3: an exit code a document CLAIMS must be the
exit code the file PRODUCES).

    0  clean                            every measured class complete
    1  findings                         the run measured something inconsistent
    2  unsupportedInvocationOrInput     an argument vector or a REQUIRED input
                                        this file does not accept.  THE CHECK
                                        DID NOT RUN.  Not a finding.
    3  selftestRefusedDirtyBase         the mutation suite refused because the
                                        base is not clean (--selftest only)
    4  trustRootIntegrityFailure        NEW, and REQUIRED OF THIS SUCCESSOR

Exit 4 discharges an obligation the head binds on its successor.  The head's
`hostileInputTotalityContract.exitDiscipline` discloses that in the retained
checker a trust-root integrity failure "currently propagates uncaught from the
module-level bootstrap and terminates as a raw traceback at exit 1, the code
this table otherwise reserves for findings", so "by exit code alone an integrity
failure is indistinguishable from a red candidate", and states: "The successor
instrument for this artifact MUST terminate trust-root integrity failures at a
distinct declared exit code; this sentence binds that obligation on the
successor without renumbering the four dispositions the retained checker
implements."  Exit 4 is that distinct code; 0-3 are unrenumbered.

ENTRYPOINTS AND FLAGS.  Two declared flags, the same argument discipline the
head declares: exactly one optional positional candidate path; a second
positional, an unknown flag, a candidate path supplied alongside the emission
mode, and both modes at once are each refused with exit 2 and a NAMED reason
rather than silently ignored; a repeated declared flag is accepted under set
semantics and asserts nothing.

    python3 -I -B artifacts/check-evidence-resolved-head-28dc3c1a.py
    python3 -I -B artifacts/check-evidence-resolved-head-28dc3c1a.py --selftest
    python3 -I -B artifacts/check-evidence-resolved-head-28dc3c1a.py --emit-resolved

ONE DEPARTURE, REPORTED RATHER THAN IMPROVISED.  The head's second declared flag
is `--emit-candidate`, which in the retained checker emits a WHOLE-OBJECT
DERIVATION of the successor from pinned bytes.  This instrument holds no such
derivation authority: it validates a resolved head, it does not author one, and
implementing a flag by that name would assert an authority it does not have.
The DISCIPLINE is implemented exactly (two declared flags, mutually exclusive,
the emission mode takes no positional path); the flag's NAME and payload differ
-- `--emit-resolved` writes the resolved effective contract's canonical bytes,
which is a measurement this instrument actually takes.  This is the one clause
of the head's contract not implemented verbatim and it is named here, not
hidden.

SELFTEST REACHABILITY, per the head's clause and
`reviewFindingTransfers[33].closure`: there is no unconditional finding gate
before the mutation suite and no second undocumented selftest entrypoint.  Both
clauses are enforced over this file's own syntax tree by the DELIBERATELY
NARROWED comparison-node flag scan the transfer describes -- the `--`-prefixed
string literals appearing inside COMPARISON nodes, plus the `DECLARED_FLAGS`
constant's own literals, must equal the declared flag set, which must equal the
flags implied by the declared entrypoints; and there must be EXACTLY ONE call to
the selftest suite, lexically guarded by a declared flag, lexically preceding
any findings return.  `--selftest` always reaches the suite.  A dirty base
refuses at exit 3, because a mutation suite over a red base is not an oracle.


4. DISCIPLINES
---------------
python3 -I -B enforced at line 1; standard library only; no network; no writes
anywhere outside disposable per-mutation copies under /tmp; deterministic output
ordering (every census sorted); every pin a full sha256; every check carries a
typed finding ID and a stated invariant; findings are scored as FINDING-SET
DELTAS, never as bare exit codes.

Duplicate-key discipline, and the one distinction that matters: a document that
is not JSON at all, or that cannot be read, is an INPUT failure -> exit 2 (the
head's "an input that cannot be read or parsed exits 2").  A document that IS
valid JSON but repeats an object key is HOSTILE INPUT, not an unreadable one:
it is a typed finding (`EVRH-DUP-01`) naming the file and the key, analysis
continues on the permissive parse so the remaining classes are still measured,
and the run cannot exit 0.  Freeze section 7.5 measured this class across the
checker corpus; every file this instrument reads is parsed through the
rejecting hook.

Type exactness follows freeze section 7.2.2 and section 7.4 throughout: `True`
is not `1`, `1` is not `1.0`.  Every declared measurement is hard-compared to
the measurement it records; an uncompared recorded measurement is prose that
looks like evidence.
"""
from __future__ import annotations

import sys

_STARTUP_REFUSAL = (
    "EVRH-UNSUPPORTED-INVOCATION: caller must use "
    "python3 -I -B artifacts/check-evidence-resolved-head-28dc3c1a.py"
)
if sys.flags.isolated != 1 or not sys.flags.dont_write_bytecode:
    print(_STARTUP_REFUSAL, file=sys.stderr)
    raise SystemExit(2)

import ast
import copy
import hashlib
import json
import pathlib
import re
import shutil
import tempfile
import types
from typing import Any, Callable, Iterable, Mapping, NamedTuple


HERE = pathlib.Path(__file__).resolve().parent
CHECKER = "check-evidence-resolved-head-28dc3c1a.py"
SUBJECT = "evidence.v15.json"

# ---------------------------------------------------------------------------
# Exit table.  Data, not literals scattered through the code, so the docstring
# above, the banner, and every `return` read from one place (freeze section
# 7.8.1 rule 3).  The first four NAMES and VALUES are the resolved head's
# `checkerModeContract.exitCodes` and are hard-compared against it at run time
# by EVRH-MODE-01 -- they are measured from resolved bytes, not invented here.
# The fifth discharges the head's exitDiscipline obligation on its successor.
# ---------------------------------------------------------------------------
EXIT: dict[str, int] = {
    "clean": 0,
    "findings": 1,
    "unsupportedInvocationOrInput": 2,
    "selftestRefusedDirtyBase": 3,
    "trustRootIntegrityFailure": 4,
}
HEAD_EXIT_NAMES: tuple[str, ...] = (
    "clean", "findings", "unsupportedInvocationOrInput", "selftestRefusedDirtyBase")
SUCCESSOR_EXIT_NAME = "trustRootIntegrityFailure"

DECLARED_FLAGS: tuple[str, ...] = ("--selftest", "--emit-resolved")
SELFTEST_SUITE = "selftest"

# ---------------------------------------------------------------------------
# GATED PINS -- the reviewed resolver bytes (section 1 of the header).
# Measured at authoring against the live tree AND against
# `git show c06eaea:docs/coop/artifacts/<name>`; both measurements identical.
# ---------------------------------------------------------------------------
RESOLVER_PINS: dict[str, str] = {
    "check-completeness.py":
        "af9f8837a5abc561cefebf071b862e2dd5fb427304f4738f7fadf5872c4f0f1f",
    "check-completeness-v2.py":
        "dbe1e6955f66b0ccb032df115ca03fa780895b129b51fb39a49593581901bfb9",
}
RESOLVER_REVIEW = (
    "check-completeness.dialect-repair.v1.review-independent.json, verdict "
    "b161c7e6…, PASS at commit c06eaea")

# ---------------------------------------------------------------------------
# THE CHAIN, head first, terminus last.  Every link is a full sha256 and every
# one is measured before use.  `evidence.v10.json` is the resolution TERMINUS
# per freeze section 7.3: it is the full-text standalone and declares no
# derivation of its own.
# ---------------------------------------------------------------------------
CHAIN_PINS: tuple[tuple[str, str], ...] = (
    ("evidence.v15.json",
     "28dc3c1aaa97f723afa8c079682a43999ca5c79686e7cde0f11e38421a179b29"),
    ("evidence.v14.json",
     "938ce4b48344d4fc4862442eb3d4a3f8af3c453c91b0dc1ea8735c9e4a529c26"),
    ("evidence.v13.json",
     "da8c3768a0ff39c9769defab6c3b36366c5e2b045e3dda2703d408116486fadd"),
    ("evidence.v12.json",
     "2077c0868c374907e10c0fa13c2578065afd9d3efb2a22e06a959f8e51af618a"),
    ("evidence.v11.json",
     "c3d9491028ac862115f8a70af222e875cf464c1c2d1b7fbe9b54a42b278198c3"),
    ("evidence.v10.json",
     "62a3a07194062c8499f6e943b4986d7a77bdecc0c4ec499851ac078fd548e9b4"),
)
HEAD_FILE = CHAIN_PINS[0][0]
TERMINUS_FILE = CHAIN_PINS[-1][0]

RESOLVED_CANONICAL = (
    "4976151e6ccfd6fd25487e2ebf9e20af3b971e5bc4879b66f11b11c43ba3c573")

# Per-section canonical digests of the RESOLVED contract.  Implied by
# RESOLVED_CANONICAL, pinned separately so a drift reports WHICH section moved
# instead of only that the whole document did -- the difference between a
# finding a reader can act on and a finding a reader must go and reproduce.
SECTION_PINS: dict[str, str] = {
    "admissionAndSealOrdering":
        "8a2bf341c29806ee813a815af1138a75b05655b5c2b838b9b32f0398ba5f517e",
    "availabilityDifferential":
        "218c36ad8d3263372efa861d9a5a669ef8596164ecbc00d79c87cb5b389c342d",
    "canonicalWireGrammar":
        "e9783f37aacb2d56e0e864397e39a34238dfba28b9fcc789284d6e174d6bf6bd",
    "checkerModeContract":
        "5dc23ac7d63495e6a857cfcb174eaa448e98436fc038e0344185e353fc0a90fe",
    "hostileInputTotalityContract":
        "c598a883fae7d7d186613c6fa7eb79441dd02b35a9611744080f448e4ed4671d",
    "invariants":
        "7d2fc8e2e66889c089384c83d7af88bd4e3a7747508770c5a21a753690adc3ed",
    "retainedResiduals":
        "fd0c75a6c943242de4537fa2ca6a132dd474a4a2f9dc75b7f54cd4b8370f6bf0",
    "reviewFindingTransfers":
        "ce4529e7961927a0c440db5ba38d253052bee7e0b1185c083e7ef678a870408a",
    "sealedCapabilityContract":
        "94839bd89984cfd25e45ee8595506732d6e33b212242c23ae73bdd46b5f72d9f",
}

# The two blocks item 4 requires to be byte-identical to the v10 terminus.
# RECOMPUTED from the terminus bytes on every run; the pins above are a second,
# independent comparison, never the primary one.
ITEM4_BLOCKS: tuple[str, ...] = ("sealedCapabilityContract",
                                 "availabilityDifferential")

# The head's own self-declared identity, type-exact.  This is the posture the
# instrument asserts does not move silently: CANDIDATE-NOT-APPLIED, DO-NOT-SEAL,
# binds NOTHING.
HEAD_IDENTITY: dict[str, Any] = {
    "artifact": "opensip.evidence.v15",
    "version": 15,
    "date": "2026-08-13",
    "documentClass": "EVIDENCE-SUCCESSOR",
    "status": "CANDIDATE-NOT-APPLIED",
    "reviewStatus": "AWAITING-INDEPENDENT-REVIEW",
    "sealRecommendation": "DO-NOT-SEAL",
    "binds": "NOTHING",
}

# The five wire record types the grammar declares.  Named, not counted: a count
# survives a rename, the closed set does not.
GRAMMAR_RECORDS: tuple[str, ...] = (
    "RawProofInventoryItemV1",
    "RawProofInventoryV1",
    "RunIdentityPreimageV1",
    "SemanticEvidenceV1",
    "TerminalRunV1",
)
GRAMMAR_ID = "EVIDENCE-RUN-TERMINAL-GRAMMAR-V1"
GRAMMAR_MEMBERS: tuple[str, ...] = (
    "commitments", "domainEnvelope", "id", "recordRules", "scalarEncoding",
    "tagRegistry")
GRAMMAR_RULE_MEMBERS: tuple[str, ...] = ("decoding", "order", "presence", "sets")
GRAMMAR_SCALAR_MEMBERS: tuple[str, ...] = (
    "blobFrame", "byteOrder", "canonicalUnsignedDecimal", "componentFrame", "text")
GRAMMAR_COMMITMENTS: tuple[str, ...] = (
    "EvidenceDigest", "RunId", "canonicalJsonRawCas", "runSealRef",
    "semanticEvidenceCasRef")
TAG_REGISTRY_SIZE = 48

RESIDUAL_COUNT = 14
TRANSFER_COUNT = 44
TRANSFER_KEYSHAPES: tuple[tuple[str, ...], ...] = (
    ("closure", "evidence", "id", "state"),
    ("closure", "id", "provenBy", "source", "sourceSha256", "state"),
)
TRANSFER_STATE_CENSUS: dict[str, int] = {
    "CANDIDATE-MECHANISM-SPECIFIED-NOT-APPLIED": 3,
    "CLOSED-BY-DERIVATION": 14,
    "CLOSED-BY-EXECUTED-PROBE": 12,
    "MECHANICALLY-CLOSED-IN-CANDIDATE-NOT-APPLIED": 1,
    "OPEN-CARRIED-RESIDUAL": 11,
    "REPAIRED-IN-CANDIDATE-NOT-APPLIED": 3,
}

# Required and forbidden sentences.  These bind the three residual entries v15
# rewrote and the transfer closure the head's own scan description lives in.
# Required-substring binding freezes prose, which is the point: prose is what
# the three v15 repairs moved, and a digest alone would say only "something
# moved".  Each forbidden string is the exact predecessor wording the repair
# replaced, so a silent revert is caught by name.
RESIDUAL_REQUIRED: dict[int, tuple[str, ...]] = {
    3: (
        "V10 remains unresolved and G19 remains blocked -- both halves live, "
        "in the carried words, re-inflected (EV14-IR-A1).",
        "This artifact does not decide the product default and does not sign "
        "CD-RT-5.",
        "both are restored in v14, EV13-IR-A5",
    ),
    5: (
        "as of v10's authoring (2026-08-02, the count's date -- pinned per "
        "EV13-IR-A4, corrected per EV14-IR-02)",
    ),
    13: (
        "BOTH-SELF-SCANS-ARE-SYNTACTIC",
        "blind-spot boundary completed in v15 per EV14-IR-01, path-scan clause "
        "per EV14-IR-A3",
        "direct non-plain-def forms need no indirection at all -- see the map",
        "both the alias-plus-DECLARED-compared-literal and the "
        "alias-plus-non-compared-gate forms, measured across two reviews",
        "The executable probes, not the self-scans, are the semantic oracle; "
        "both scans are drift tripwires for their measured coverage only.",
    ),
}
RESIDUAL_FORBIDDEN: dict[int, tuple[str, ...]] = {
    3: ("both are restored here, EV13-IR-A5",),
    5: ("as of v10's authoring (2026-08-12",),
    13: ("evades the flag scan only in the measured "
         "alias-plus-DECLARED-compared-literal form",),
}
TRANSFER33_INDEX = 33
TRANSFER33_REQUIRED: tuple[str, ...] = (
    "DELIBERATELY NARROWED SCAN",
    "requires exactly one call to the selftest suite, lexically guarded by a "
    "declared flag",
    "citation corrected in v14 per EV13-IR-A1: line 3327 is code",
    "See retainedResiduals[13].",
)
TRANSFER33_STATE = "CLOSED-BY-EXECUTED-PROBE"

# The head's exitDiscipline must keep disclosing the fifth termination
# behaviour AND keep binding the successor obligation this file discharges.
EXIT_DISCIPLINE_REQUIRED: tuple[str, ...] = (
    "propagates uncaught from the module-level bootstrap and terminates as a "
    "raw traceback at exit 1",
    "The successor instrument for this artifact MUST terminate trust-root "
    "integrity failures at a distinct declared exit code",
    "without renumbering the four dispositions the retained checker implements",
)
EXIT_CODES_NOTE_REQUIRED: tuple[str, ...] = (
    "hostileInputTotalityContract.exitDiscipline",
    "A fifth termination behavior",
)

SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
SHA256_IN_TEXT_RE = re.compile(r"[0-9a-f]{64}|sha256:|run1:")
RECIPE_KEY_RE = re.compile(r"recipe", re.I)
DERIVATION_VERBS: tuple[str, ...] = ("set", "add")
ACCOUNTING_MEMBERS: tuple[str, ...] = (
    "adds", "digestsMoved", "recipesChanged", "removes", "sets", "total",
    "whyNoDigestMoves")


# ---------------------------------------------------------------------------
# Typed exceptions.  Each one maps to exactly one exit disposition.
# ---------------------------------------------------------------------------
class DuplicateKeyError(ValueError):
    """A JSON object repeated a key; the document is not canonical."""


class Malformed(Exception):
    """A REQUIRED input is missing, unreadable, or is not JSON.  Exit 2."""


class UnsupportedInvocation(Exception):
    """The caller supplied an argument vector this file does not accept."""


class TrustRootIntegrityError(Exception):
    """A GATED byte string is absent or does not hash to its declared pin.

    This is the failure the resolved head's exitDiscipline requires a successor
    to terminate at a DISTINCT declared code.  It exits 4.  It is never a
    finding, because nothing was measured: the check did not run.
    """


class Finding(NamedTuple):
    """A typed finding.  `id` names the class, `invariant` states the property
    that was asserted, `detail` states what was measured instead."""

    id: str
    invariant: str
    detail: str

    def render(self) -> str:
        return f"{self.id}: {self.invariant} | measured: {self.detail}"


# ---------------------------------------------------------------------------
# Primitives
# ---------------------------------------------------------------------------
def sha256_hex(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
    """Object hook that REFUSES a repeated key (freeze section 7.5)."""
    result: dict[str, Any] = {}
    for key, value in items:
        if key in result:
            raise DuplicateKeyError(f"duplicate object key {key!r}")
        result[key] = value
    return result


def exact_equal(left: Any, right: Any) -> bool:
    """Type-exact deep equality (freeze section 7.2.2 / 7.4).

    `True` is not `1`; `1` is not `1.0`.  Python's `==` accepts all three, which
    is precisely the coercion a `from` restatement exists to forbid.  This is
    this instrument's OWN implementation; it is deliberately not imported from
    the gated resolvers, so the independent walk in `independent_resolve` does
    not inherit whatever the resolver's equality happens to be.
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


def canonical_bytes(value: Any) -> bytes:
    """Local mirror of `check-completeness-v2.py::canonical_bytes`.

    Used ONLY as a cross-check: `resolved_canonical_digest` computes the
    published figure with the GATED resolver's own function, and this mirror is
    compared against it (EVRH-CANON-02).  Two implementations that agree are a
    measurement; one implementation is an assumption.
    """
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False).encode("utf-8")


def pointer_steps(path: Any) -> list[Any] | None:
    """RFC 6901 pointer steps, parsed STRICTLY: the parse must round-trip to the
    exact declared path or this walker refuses.  Only the pointer dialect is
    implemented here on purpose -- the whole live chain writes pointers and
    nothing else (measured), and a dialect this instrument cannot walk is
    REPORTED as an unrun class rather than guessed at."""
    if not isinstance(path, str) or not path.startswith("/"):
        return None
    steps: list[Any] = []
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


def has_step(node: Any, step: Any) -> bool:
    if isinstance(node, dict):
        return isinstance(step, str) and step in node
    if isinstance(node, list):
        return (isinstance(step, int) and not isinstance(step, bool)
                and 0 <= step < len(node))
    return False


def resolve_steps(root: Any, steps: list[Any]) -> tuple[bool, Any]:
    node = root
    for step in steps:
        if not has_step(node, step):
            return False, None
        node = node[step]
    return True, node


def leaf_paths(value: Any, prefix: str = "") -> Iterable[tuple[str, Any]]:
    """Every scalar leaf, deterministically ordered (dict keys sorted)."""
    if isinstance(value, dict):
        for key in sorted(value):
            yield from leaf_paths(value[key], f"{prefix}/{key}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            yield from leaf_paths(item, f"{prefix}/{index}")
    else:
        yield prefix, value


def changed_leaves(before: Any, after: Any) -> list[tuple[str, Any, Any]]:
    """Leaf paths whose value moved, type-exactly compared, sorted by path."""
    left = dict(leaf_paths(before))
    right = dict(leaf_paths(after))
    moved: list[tuple[str, Any, Any]] = []
    for path in sorted(set(left) | set(right)):
        old = left.get(path, _ABSENT)
        new = right.get(path, _ABSENT)
        if not exact_equal(old, new):
            moved.append((path, old, new))
    return moved


class _Absent:
    def __repr__(self) -> str:                        # pragma: no cover - label
        return "<absent>"


_ABSENT = _Absent()


# ---------------------------------------------------------------------------
# The gated trust root
# ---------------------------------------------------------------------------
def load_gated_module(root: pathlib.Path, name: str, pin: str,
                      alias: str) -> types.ModuleType:
    """Hash-verify a gated resolver, then execute THE VERIFIED SNAPSHOT.

    The bytes that produced the digest are the bytes that are compiled: there is
    no second read between the measurement and the execution.  `__file__` is set
    before execution so the resolver's own `ROOT` (its parent's parent) lands on
    the tree it is being asked about -- which is how the selftest can point the
    SAME verified bytes at a disposable /tmp copy without ever relaxing the pin.
    """
    path = root / "artifacts" / name
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise TrustRootIntegrityError(
            f"EVRH-GATE-01: gated resolver {name} cannot be read "
            f"({type(exc).__name__}); gated pin {pin}") from exc
    measured = sha256_hex(raw)
    if measured != pin:
        raise TrustRootIntegrityError(
            f"EVRH-GATE-01: gated resolver {name} does not match its reviewed "
            f"pin; gated {pin}, measured {measured}. The reviewed bytes are "
            f"{RESOLVER_REVIEW}. This refusal is correct freeze section 7.8.1 "
            "behaviour, not a defect: a successor instrument re-gates the new "
            "reviewed digests, this one never guesses.")
    module = types.ModuleType(alias)
    module.__file__ = str(path)
    try:
        code = compile(raw.decode("utf-8"), str(path), "exec")
        exec(code, module.__dict__)                    # noqa: S102 - gated bytes
    except Exception as exc:                           # noqa: BLE001 - reported
        raise TrustRootIntegrityError(
            f"EVRH-GATE-01: gated resolver {name} hashed to its pin but could "
            f"not be executed: {type(exc).__name__}: {exc}") from exc
    return module


class Resolvers(NamedTuple):
    r1: types.ModuleType
    r2: types.ModuleType
    measured: dict[str, str]


def gate_resolvers(root: pathlib.Path) -> Resolvers:
    measured = {}
    modules = {}
    for index, (name, pin) in enumerate(sorted(RESOLVER_PINS.items())):
        module = load_gated_module(root, name, pin, f"_gated_resolver_{index}")
        modules[name] = module
        measured[name] = pin
    return Resolvers(r1=modules["check-completeness.py"],
                     r2=modules["check-completeness-v2.py"],
                     measured=measured)


# ---------------------------------------------------------------------------
# Document loading
# ---------------------------------------------------------------------------
class Document(NamedTuple):
    name: str
    raw: bytes
    measured: str
    declared: str
    value: Any
    duplicate: str | None


def read_document(root: pathlib.Path, name: str, declared: str) -> Document:
    path = root / "artifacts" / name
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise Malformed(
            f"{name}: REQUIRED input cannot be read ({type(exc).__name__})"
        ) from exc
    try:
        text = raw.decode("utf-8")
    except UnicodeError as exc:
        raise Malformed(f"{name}: REQUIRED input is not UTF-8") from exc
    duplicate: str | None = None
    try:
        value = json.loads(text, object_pairs_hook=_pairs)
    except DuplicateKeyError as exc:
        duplicate = str(exc)
        try:
            value = json.loads(text)
        except json.JSONDecodeError as inner:          # pragma: no cover
            raise Malformed(f"{name}: not JSON: {inner}") from inner
    except json.JSONDecodeError as exc:
        raise Malformed(f"{name}: REQUIRED input is not JSON: {exc}") from exc
    return Document(name=name, raw=raw, measured=sha256_hex(raw),
                    declared=declared, value=value, duplicate=duplicate)


# ---------------------------------------------------------------------------
# Independent pointer walk -- a third opinion on the resolution
# ---------------------------------------------------------------------------
def independent_resolve(chain: list[Document]) -> tuple[Any, list[str], list[str]]:
    """Resolve terminus -> head using ONLY this file's own pointer walk.

    (resolved, errors, unwalkable).  This exists so the resolution is not a
    single implementation's word.  `errors` are refusals; `unwalkable` names
    operations written in a dialect this walker does not implement, so a dialect
    change is a NAMED unrun class rather than a silent pass.
    """
    errors: list[str] = []
    unwalkable: list[str] = []
    base = copy.deepcopy(chain[-1].value)
    for document in reversed(chain[:-1]):
        declaration = document.value.get("derivedFrom")
        if not isinstance(declaration, dict):
            errors.append(f"{document.name}: no derivedFrom object")
            return None, errors, unwalkable
        operations = declaration.get("operations")
        if not isinstance(operations, list) or not operations:
            errors.append(f"{document.name}: derivedFrom carries no operations")
            return None, errors, unwalkable
        for index, operation in enumerate(operations):
            where = f"{document.name} operation {index}"
            if not isinstance(operation, dict):
                errors.append(f"{where}: not an object")
                return None, errors, unwalkable
            verb = operation.get("op")
            if verb not in DERIVATION_VERBS:
                errors.append(f"{where}: verb {verb!r} outside {list(DERIVATION_VERBS)}")
                return None, errors, unwalkable
            steps = pointer_steps(operation.get("path"))
            if steps is None:
                unwalkable.append(f"{where}: path {operation.get('path')!r}")
                return None, errors, unwalkable
            if "value" not in operation:
                errors.append(f"{where}: carries no value")
                return None, errors, unwalkable
            found, parent = resolve_steps(base, steps[:-1])
            if not found or not isinstance(parent, (dict, list)):
                errors.append(f"{where}: parent does not resolve to a container")
                return None, errors, unwalkable
            exists = has_step(parent, steps[-1])
            if verb == "set":
                if "from" not in operation:
                    errors.append(f"{where}: a set must restate the value it replaces")
                    return None, errors, unwalkable
                if not exists:
                    errors.append(f"{where}: does not resolve against the predecessor")
                    return None, errors, unwalkable
                if not exact_equal(parent[steps[-1]], operation["from"]):
                    errors.append(
                        f"{where}: 'from' is not what the verified predecessor "
                        f"holds (type-exact comparison); declared "
                        f"{type(operation['from']).__name__}, held "
                        f"{type(parent[steps[-1]]).__name__}")
                    return None, errors, unwalkable
            else:
                if exists:
                    errors.append(f"{where}: add over an existing member")
                    return None, errors, unwalkable
                if not isinstance(parent, dict) or not isinstance(steps[-1], str):
                    errors.append(f"{where}: add can only name a member of an object")
                    return None, errors, unwalkable
            parent[steps[-1]] = copy.deepcopy(operation["value"])
    return base, errors, unwalkable


def stepwise_effective(chain: list[Document]) -> dict[str, Any]:
    """Effective document after each delta, keyed by the delta that produced it.

    Used by the operation-accounting probes, which must compare the document
    BEFORE and AFTER a delta to decide whether a digest leaf or a recipe leaf
    actually moved -- `digestsMoved: 0` is a measurement claim and gets a hard
    comparison, not a reading.
    """
    states: dict[str, Any] = {chain[-1].name: copy.deepcopy(chain[-1].value)}
    base = copy.deepcopy(chain[-1].value)
    for document in reversed(chain[:-1]):
        declaration = document.value.get("derivedFrom")
        operations = (declaration or {}).get("operations")
        if not isinstance(operations, list):
            break
        nxt = copy.deepcopy(base)
        ok = True
        for operation in operations:
            if not isinstance(operation, dict):
                ok = False
                break
            steps = pointer_steps(operation.get("path"))
            if steps is None or "value" not in operation:
                ok = False
                break
            found, parent = resolve_steps(nxt, steps[:-1])
            if not found or not isinstance(parent, (dict, list)):
                ok = False
                break
            if isinstance(parent, list) and not has_step(parent, steps[-1]):
                ok = False
                break
            parent[steps[-1]] = copy.deepcopy(operation["value"])
        if not ok:
            break
        states[document.name] = nxt
        base = nxt
    return states


# ---------------------------------------------------------------------------
# The source self-scans.  TRIPWIRES, NOT AN ORACLE (head residual 13).
# ---------------------------------------------------------------------------
_OWN_TREE: ast.Module | None = None


def own_tree() -> ast.Module:
    global _OWN_TREE
    if _OWN_TREE is None:
        source = pathlib.Path(__file__).read_bytes().decode("utf-8")
        _OWN_TREE = ast.parse(source)
    return _OWN_TREE


def comparison_flag_literals(tree: ast.Module) -> set[str]:
    """The DELIBERATELY NARROWED scan described in the resolved head's
    `reviewFindingTransfers[33].closure`, implemented as that entry describes
    it: a string literal beginning with two hyphens only ACTS as a command flag
    when it is TESTED against the argument vector, so the closed set is the
    literals appearing inside COMPARISON nodes.  Flag-shaped strings that appear
    only as inert data -- refusal-battery vectors, mutation payloads -- gate
    nothing and are not entrypoints.
    """
    flags: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Compare):
            for child in ast.walk(node):
                if (isinstance(child, ast.Constant)
                        and isinstance(child.value, str)
                        and child.value.startswith("--")):
                    flags.add(child.value)
    return flags


def declared_flag_literals(tree: ast.Module) -> set[str]:
    """The `DECLARED_FLAGS` constant's own literals, read from the tree."""
    literals: set[str] = set()
    for node in tree.body:
        target = None
        if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            target = node.target.id
        elif (isinstance(node, ast.Assign) and len(node.targets) == 1
              and isinstance(node.targets[0], ast.Name)):
            target = node.targets[0].id
        if target != "DECLARED_FLAGS" or node.value is None:
            continue
        for child in ast.walk(node.value):
            if isinstance(child, ast.Constant) and isinstance(child.value, str):
                literals.add(child.value)
    return literals


def selftest_dispatch_scan(tree: ast.Module) -> dict[str, Any]:
    """The dispatch half of the head's `selftestReachability` clause.

    Implemented the way the retained checker implements it, so both scans
    measure the same property:

      * a CALL to the suite that is not itself inside the suite's own
        definition is a DISPATCH; exactly one may exist.
      * a dispatch is GUARDED when a declared flag literal appears in the test
        of an enclosing `if`.
      * the ORDER clause is scoped to `main()`'s own top-level statement list,
        because that is where an unconditional finding gate could sit in front
        of the suite.  Comparing raw line numbers across the whole module would
        compare a helper's early return against the dispatch and report a
        defect that does not exist.
    """
    dispatches: list[dict[str, Any]] = []

    def visit(node: Any, inside_suite: bool, guarded_by: tuple[str, ...]) -> None:
        if isinstance(node, ast.FunctionDef) and node.name == SELFTEST_SUITE:
            inside_suite = True
        if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                and node.func.id == SELFTEST_SUITE and not inside_suite):
            dispatches.append({"line": node.lineno, "guards": sorted(guarded_by)})
        if isinstance(node, ast.If):
            literals = tuple(sorted({
                child.value for child in ast.walk(node.test)
                if isinstance(child, ast.Constant)
                and isinstance(child.value, str)
                and child.value in DECLARED_FLAGS}))
            for child in node.body:
                visit(child, inside_suite, literals or guarded_by)
            for child in node.orelse:
                visit(child, inside_suite, guarded_by)
            visit(node.test, inside_suite, guarded_by)
            return
        for child in ast.iter_child_nodes(node):
            visit(child, inside_suite, guarded_by)

    visit(tree, False, ())

    mains = [node for node in tree.body
             if isinstance(node, ast.FunctionDef) and node.name == "main"]
    dispatch_index: int | None = None
    findings_index: int | None = None
    if len(mains) == 1:
        for index, statement in enumerate(mains[0].body):
            text = ast.dump(statement)
            if dispatch_index is None and \
                    f"Name(id='{SELFTEST_SUITE}'" in text and \
                    any(f"'{flag}'" in text for flag in DECLARED_FLAGS):
                dispatch_index = index
            if findings_index is None and "Return(" in text and \
                    "'findings'" in text:
                findings_index = index
    return {"dispatches": dispatches, "mainCount": len(mains),
            "dispatchIndex": dispatch_index, "findingsIndex": findings_index}


# ---------------------------------------------------------------------------
# The checks.  Every one carries a typed ID and a stated invariant.
# ---------------------------------------------------------------------------
def check_documents(chain: list[Document]) -> list[Finding]:
    findings: list[Finding] = []
    for document in chain:
        if document.duplicate is not None:
            findings.append(Finding(
                "EVRH-DUP-01",
                "no file this instrument reads repeats a JSON object key "
                "(freeze section 7.5)",
                f"{document.name}: {document.duplicate}"))
        if document.measured != document.declared:
            findings.append(Finding(
                "EVRH-CHAIN-01",
                "every chain link hashes to its gated pin before it is parsed",
                f"{document.name}: pinned {document.declared}, measured "
                f"{document.measured}"))
    return findings


def check_declared_links(chain: list[Document],
                         chain_pins: tuple[tuple[str, str], ...]) -> list[Finding]:
    findings: list[Finding] = []
    pinned = dict(chain_pins)
    for index, document in enumerate(chain[:-1]):
        expected_name = chain[index + 1].name
        declaration = document.value.get("derivedFrom")
        if not isinstance(declaration, dict):
            findings.append(Finding(
                "EVRH-CHAIN-02",
                "every delta declares its predecessor by name and by full "
                "sha256",
                f"{document.name}: derivedFrom is "
                f"{type(declaration).__name__}, not an object"))
            continue
        declared_name = declaration.get("artifact")
        declared_digest = declaration.get("sha256")
        if declared_name != expected_name:
            findings.append(Finding(
                "EVRH-CHAIN-02",
                "every delta names the next pinned chain link as its "
                "predecessor",
                f"{document.name}: declares {declared_name!r}, chain expects "
                f"{expected_name!r}"))
        if declared_digest != pinned[expected_name]:
            findings.append(Finding(
                "EVRH-CHAIN-02",
                "every delta's declared predecessor digest equals that link's "
                "gated pin",
                f"{document.name}: declares {declared_digest!r}, gated pin is "
                f"{pinned[expected_name]}"))
    return findings


def check_terminus(chain: list[Document], resolvers: Resolvers) -> list[Finding]:
    """Freeze section 7.3: the resolution TERMINUS is the reviewed full-text
    standalone and must declare no derivation of its own.  A terminus that grew
    a derivation would silently extend the chain past its reviewed bytes -- the
    exact `retention-tiers.v26` false positive the freeze records."""
    findings: list[Finding] = []
    terminus = chain[-1]
    for label, module in (("check-completeness.py", resolvers.r1),
                          ("check-completeness-v2.py", resolvers.r2)):
        declaration, errors = module.derivation_declaration(terminus.value)
        if declaration is not None or errors:
            findings.append(Finding(
                "EVRH-CHAIN-05",
                "the resolution terminus declares no derivation (freeze "
                "section 7.3)",
                f"{label} reads a declaration in {terminus.name}: "
                f"declaration={declaration is not None}, errors={errors}"))
    return findings


def resolve_with(module: Any, label: str,
                 head: Document) -> tuple[Any, list[Finding], Any]:
    findings: list[Finding] = []
    declaration, errors = module.derivation_declaration(head.value)
    if errors:
        findings.append(Finding(
            "EVRH-CHAIN-03",
            "the gated resolver reads exactly one unambiguous derivation "
            "declaration from the head",
            f"{label}: {'; '.join(errors)}"))
        return None, findings, None
    if declaration is None:
        findings.append(Finding(
            "EVRH-CHAIN-03",
            "the head declares a derivation the gated resolver recognises",
            f"{label}: no declaration found in {head.name}"))
        return None, findings, None
    effective, provenance, resolve_errors = module.resolve_derivation(
        f"artifacts/{head.name}", declaration)
    if resolve_errors or effective is None:
        findings.append(Finding(
            "EVRH-CHAIN-03",
            "the gated resolver materialises the effective contract with zero "
            "refusals",
            f"{label}: {'; '.join(resolve_errors) or 'no effective contract'}"))
        return None, findings, provenance
    return effective, findings, provenance


def check_provenance(provenance: Any, label: str,
                     chain_pins: tuple[tuple[str, str], ...]) -> list[Finding]:
    """The resolver's own provenance walk must visit exactly the pinned chain,
    in order, and stop at the terminus."""
    findings: list[Finding] = []
    walked: list[tuple[str, str]] = []
    node = provenance
    while isinstance(node, dict):
        walked.append((node.get("predecessor", "?"),
                       node.get("measuredDigest", "?")))
        node = node.get("via")
    expected = [(f"artifacts/{name}", digest) for name, digest in chain_pins[1:]]
    if walked != expected:
        findings.append(Finding(
            "EVRH-CHAIN-04",
            "the resolver's provenance walk visits exactly the pinned chain, "
            "in order, terminating at the terminus",
            f"{label}: walked {walked!r}, gated chain is {expected!r}"))
    return findings


def check_agreement(candidates: dict[str, Any]) -> list[Finding]:
    """Three independent resolutions must be type-exactly the same document."""
    findings: list[Finding] = []
    labels = sorted(candidates)
    reference = candidates[labels[0]]
    for label in labels[1:]:
        if not exact_equal(reference, candidates[label]):
            findings.append(Finding(
                "EVRH-CHAIN-06",
                "both gated resolvers and this instrument's own pointer walk "
                "produce type-exactly the same effective contract",
                f"{labels[0]} and {label} disagree"))
    return findings


def check_canonical(resolved: Any, resolvers: Resolvers) -> list[Finding]:
    findings: list[Finding] = []
    gated = sha256_hex(resolvers.r2.canonical_bytes(resolved))
    if gated != RESOLVED_CANONICAL:
        findings.append(Finding(
            "EVRH-CANON-01",
            "the resolved effective contract's canonical digest under the "
            "gated check-completeness-v2.py::canonical_bytes equals the pin",
            f"pinned {RESOLVED_CANONICAL}, measured {gated}"))
    local = sha256_hex(canonical_bytes(resolved))
    if local != gated:
        findings.append(Finding(
            "EVRH-CANON-02",
            "this instrument's own canonical serialisation agrees with the "
            "gated resolver's",
            f"gated {gated}, local {local}"))
    for section in sorted(SECTION_PINS):
        if section not in resolved:
            findings.append(Finding(
                "EVRH-SECT-01",
                "every gated section of the resolved contract is present and "
                "hashes to its pin",
                f"{section}: absent from the resolved contract"))
            continue
        measured = sha256_hex(canonical_bytes(resolved[section]))
        if measured != SECTION_PINS[section]:
            findings.append(Finding(
                "EVRH-SECT-01",
                "every gated section of the resolved contract hashes to its "
                "pin",
                f"{section}: pinned {SECTION_PINS[section]}, measured "
                f"{measured}"))
    return findings


def check_head_identity(head: Document) -> list[Finding]:
    findings: list[Finding] = []
    for key in sorted(HEAD_IDENTITY):
        expected = HEAD_IDENTITY[key]
        actual = head.value.get(key, _ABSENT)
        if not exact_equal(actual, expected):
            findings.append(Finding(
                "EVRH-HEAD-01",
                "the head's self-declared identity and posture are exactly "
                "what the accepted bytes declare, type-exact",
                f"{key}: expected {expected!r} ({type(expected).__name__}), "
                f"measured {actual!r} ({type(actual).__name__})"))
    return findings


def check_item4(resolved: Any, chain: list[Document]) -> list[Finding]:
    """RECOMPUTE, do not trust.  Every delta in the chain claims the item-4
    blocks are byte-identical to v10; that claim is a measurement and gets a
    hard comparison against the terminus bytes."""
    findings: list[Finding] = []
    terminus = chain[-1].value
    for block in ITEM4_BLOCKS:
        if block not in resolved or block not in terminus:
            findings.append(Finding(
                "EVRH-ITEM4-01",
                "both item-4 blocks are present in the resolved contract and "
                "in the terminus",
                f"{block}: resolved={block in resolved}, "
                f"terminus={block in terminus}"))
            continue
        if not exact_equal(resolved[block], terminus[block]):
            findings.append(Finding(
                "EVRH-ITEM4-01",
                "each item-4 block is type-exactly identical to the v10 "
                "terminus (RECOMPUTED, never read from the delta's claim)",
                f"{block}: resolved canonical "
                f"{sha256_hex(canonical_bytes(resolved[block]))}, terminus "
                f"canonical {sha256_hex(canonical_bytes(terminus[block]))}"))
    for document in chain[:-1]:
        declaration = document.value.get("derivedFrom") or {}
        for index, operation in enumerate(declaration.get("operations") or []):
            if not isinstance(operation, dict):
                continue
            path = operation.get("path")
            if not isinstance(path, str):
                continue
            for block in ITEM4_BLOCKS:
                if path == f"/{block}" or path.startswith(f"/{block}/"):
                    findings.append(Finding(
                        "EVRH-ITEM4-02",
                        "no operation in any chain delta addresses a path "
                        "inside an item-4 block",
                        f"{document.name} operation {index} addresses {path}"))
    return findings


def check_accounting(chain: list[Document]) -> list[Finding]:
    findings: list[Finding] = []
    states = stepwise_effective(chain)
    order = list(reversed([document.name for document in chain]))
    for position, name in enumerate(order):
        if position == 0:
            continue
        document = next(item for item in chain if item.name == name)
        accounting = document.value.get("operationAccounting")
        declaration = document.value.get("derivedFrom") or {}
        operations = declaration.get("operations")
        if not isinstance(accounting, dict):
            findings.append(Finding(
                "EVRH-ACCT-01",
                "every delta publishes an operationAccounting object",
                f"{name}: operationAccounting is {type(accounting).__name__}"))
            continue
        if sorted(accounting) != sorted(ACCOUNTING_MEMBERS):
            findings.append(Finding(
                "EVRH-ACCT-01",
                "operationAccounting declares exactly its closed member set",
                f"{name}: members {sorted(accounting)}, expected "
                f"{sorted(ACCOUNTING_MEMBERS)}"))
        if not isinstance(operations, list):
            continue
        verbs = [operation.get("op") for operation in operations
                 if isinstance(operation, dict)]
        measured = {
            "total": len(operations),
            "sets": sum(1 for verb in verbs if verb == "set"),
            "adds": sum(1 for verb in verbs if verb == "add"),
            "removes": sum(1 for verb in verbs if verb == "remove"),
        }
        for key in sorted(measured):
            declared = accounting.get(key, _ABSENT)
            if not exact_equal(declared, measured[key]):
                findings.append(Finding(
                    "EVRH-ACCT-01",
                    "operationAccounting's counts equal the operations the "
                    "delta actually carries, compared type-exactly (freeze "
                    "section 7.2.2: 3 is not 3.0 and is not True)",
                    f"{name}.{key}: declares {declared!r} "
                    f"({type(declared).__name__}), measured {measured[key]!r} "
                    f"(int)"))
        for verb in sorted({str(item) for item in verbs}):
            if verb not in DERIVATION_VERBS:
                findings.append(Finding(
                    "EVRH-ACCT-02",
                    "every operation verb is inside the resolver's declared "
                    "verb set",
                    f"{name}: verb {verb!r} outside {list(DERIVATION_VERBS)}"))
        before = states.get(order[position - 1])
        after = states.get(name)
        if before is None or after is None:
            findings.append(Finding(
                "EVRH-ACCT-03",
                "the digestsMoved and recipesChanged claims are verified by "
                "recomputing the effective contract before and after the delta",
                f"{name}: the stepwise effective contract could not be built, "
                "so the two claims were NOT measured"))
            continue
        moved = changed_leaves(before, after)
        digest_moves = [
            path for path, old, new in moved
            if any(isinstance(item, str) and SHA256_IN_TEXT_RE.search(item)
                   for item in (old, new))]
        recipe_moves = [path for path, _, _ in moved
                        if RECIPE_KEY_RE.search(path)]
        for key, actual in (("digestsMoved", len(digest_moves)),
                            ("recipesChanged", len(recipe_moves))):
            declared = accounting.get(key, _ABSENT)
            if not exact_equal(declared, actual):
                findings.append(Finding(
                    "EVRH-ACCT-03",
                    f"the published {key} count equals the recomputed count of "
                    "changed leaves of that kind (a recorded measurement is "
                    "compared to the measurement it records)",
                    f"{name}.{key}: declares {declared!r}, recomputed {actual} "
                    f"({sorted(digest_moves if key == 'digestsMoved' else recipe_moves)})"))
    return findings


def check_grammar(resolved: Any) -> list[Finding]:
    findings: list[Finding] = []
    grammar = resolved.get("canonicalWireGrammar")
    if not isinstance(grammar, dict):
        return [Finding(
            "EVRH-GRAM-01",
            "the resolved contract carries a canonicalWireGrammar object",
            f"canonicalWireGrammar is {type(grammar).__name__}")]
    if sorted(grammar) != sorted(GRAMMAR_MEMBERS + ("records",)):
        findings.append(Finding(
            "EVRH-GRAM-01",
            "the wire grammar declares exactly its closed member set",
            f"members {sorted(grammar)}, expected "
            f"{sorted(GRAMMAR_MEMBERS + ('records',))}"))
    if grammar.get("id") != GRAMMAR_ID:
        findings.append(Finding(
            "EVRH-GRAM-01",
            "the wire grammar's identity is the declared one",
            f"id {grammar.get('id')!r}, expected {GRAMMAR_ID!r}"))
    records = grammar.get("records")
    if not isinstance(records, dict) or sorted(records) != sorted(GRAMMAR_RECORDS):
        findings.append(Finding(
            "EVRH-GRAM-02",
            "the grammar declares exactly the five ...V1 record types, named "
            "(a count survives a rename; the closed set does not)",
            f"records {sorted(records) if isinstance(records, dict) else records!r},"
            f" expected {sorted(GRAMMAR_RECORDS)}"))
        records = records if isinstance(records, dict) else {}
    for name in sorted(records):
        record = records[name]
        if not name.endswith("V1"):
            findings.append(Finding(
                "EVRH-GRAM-02",
                "every declared record type is a ...V1 record",
                f"{name} does not end in V1"))
        if not isinstance(record, dict):
            findings.append(Finding(
                "EVRH-GRAM-02", "every record declaration is an object",
                f"{name} is {type(record).__name__}"))
            continue
        fields = record.get("fields")
        required = record.get("required")
        if not isinstance(fields, list) or not isinstance(required, list):
            findings.append(Finding(
                "EVRH-GRAM-02",
                "every record declares a required list and a fields list",
                f"{name}: required={type(required).__name__}, "
                f"fields={type(fields).__name__}"))
            continue
        names = [field.get("name") for field in fields if isinstance(field, dict)]
        if names != required:
            findings.append(Finding(
                "EVRH-GRAM-02",
                "a record's field ORDER is exactly its required list -- the "
                "grammar's recordRules.order is 'exact field order below', so "
                "order is normative, not presentational",
                f"{name}: fields {names}, required {required}"))
        if len(set(names)) != len(names):
            findings.append(Finding(
                "EVRH-GRAM-02", "no record repeats a field name",
                f"{name}: {names}"))
        for field in fields:
            if not isinstance(field, dict) or "const" not in field:
                continue
            const = field["const"]
            if type(const) is not int or isinstance(const, bool):
                findings.append(Finding(
                    "EVRH-GRAM-05",
                    "a declared const scalar is a type-exact int, never a bool "
                    "and never a float (freeze section 7.4's 1.0 == 1 class)",
                    f"{name}.{field.get('name')}: const {const!r} "
                    f"({type(const).__name__})"))
    registry = grammar.get("tagRegistry")
    if not isinstance(registry, list):
        findings.append(Finding(
            "EVRH-GRAM-03", "the grammar declares a tagRegistry list",
            f"tagRegistry is {type(registry).__name__}"))
        registry = []
    tags = [row.get("tag") for row in registry if isinstance(row, dict)]
    if len(registry) != TAG_REGISTRY_SIZE:
        findings.append(Finding(
            "EVRH-GRAM-03", "the tag registry census is the gated one",
            f"{len(registry)} rows, gated census {TAG_REGISTRY_SIZE}"))
    if len(set(tags)) != len(tags):
        duplicates = sorted({tag for tag in tags if tags.count(tag) > 1})
        findings.append(Finding(
            "EVRH-GRAM-03", "no tag is registered twice", f"duplicates {duplicates}"))
    used: set[Any] = set()
    for record in records.values():
        if not isinstance(record, dict):
            continue
        used.add(record.get("recordTag"))
        for field in record.get("fields") or []:
            if isinstance(field, dict):
                used.add(field.get("tag"))
    envelope = grammar.get("domainEnvelope")
    if isinstance(envelope, dict):
        used.add(envelope.get("recordTag"))
        for field in envelope.get("fields") or []:
            if isinstance(field, dict):
                used.add(field.get("tag"))
    unregistered = sorted(str(tag) for tag in used - set(tags) if tag is not None)
    if unregistered:
        findings.append(Finding(
            "EVRH-GRAM-03",
            "every record tag and every field tag the grammar uses is present "
            "in the tag registry",
            f"unregistered tags {unregistered}"))
    for member, expected in (("recordRules", GRAMMAR_RULE_MEMBERS),
                             ("scalarEncoding", GRAMMAR_SCALAR_MEMBERS),
                             ("commitments", GRAMMAR_COMMITMENTS)):
        block = grammar.get(member)
        if not isinstance(block, dict) or sorted(block) != sorted(expected):
            findings.append(Finding(
                "EVRH-GRAM-04",
                f"the grammar's {member} declares exactly its closed member set",
                f"{member}: "
                f"{sorted(block) if isinstance(block, dict) else block!r}, "
                f"expected {sorted(expected)}"))
    return findings


def check_residuals(resolved: Any) -> list[Finding]:
    findings: list[Finding] = []
    residuals = resolved.get("retainedResiduals")
    if not isinstance(residuals, list):
        return [Finding(
            "EVRH-RES-01", "retainedResiduals is a list",
            f"retainedResiduals is {type(residuals).__name__}")]
    if len(residuals) != RESIDUAL_COUNT:
        findings.append(Finding(
            "EVRH-RES-01",
            "the retained-residual census is the gated one -- a residual "
            "cannot be dropped without the count moving",
            f"{len(residuals)} residuals, gated census {RESIDUAL_COUNT}"))
    for index, entry in enumerate(residuals):
        if type(entry) is not str or not entry.strip():
            findings.append(Finding(
                "EVRH-RES-01",
                "every retained residual is a non-empty string",
                f"residual {index} is {type(entry).__name__}"))
    for index in sorted(RESIDUAL_REQUIRED):
        if index >= len(residuals) or not isinstance(residuals[index], str):
            findings.append(Finding(
                "EVRH-RES-02",
                "the three residual entries v15 rewrote are present and carry "
                "their repaired sentences",
                f"residual {index} is absent or not a string"))
            continue
        text = residuals[index]
        for phrase in RESIDUAL_REQUIRED[index]:
            if phrase not in text:
                findings.append(Finding(
                    "EVRH-RES-02",
                    "each v15-repaired residual carries the exact sentence the "
                    "accepted bytes state (required-substring binding: a "
                    "section digest says only that something moved, this says "
                    "what)",
                    f"residual {index} is missing {phrase!r}"))
        for phrase in RESIDUAL_FORBIDDEN.get(index, ()):
            if phrase in text:
                findings.append(Finding(
                    "EVRH-RES-02",
                    "no v15-repaired residual has silently reverted to the "
                    "wording its repair replaced",
                    f"residual {index} carries the superseded wording "
                    f"{phrase!r}"))
    return findings


def check_transfers(resolved: Any) -> list[Finding]:
    findings: list[Finding] = []
    transfers = resolved.get("reviewFindingTransfers")
    if not isinstance(transfers, list):
        return [Finding(
            "EVRH-XFER-01", "reviewFindingTransfers is a list",
            f"reviewFindingTransfers is {type(transfers).__name__}")]
    if len(transfers) != TRANSFER_COUNT:
        findings.append(Finding(
            "EVRH-XFER-01",
            "the review-finding-transfer census is the gated one",
            f"{len(transfers)} transfers, gated census {TRANSFER_COUNT}"))
    census: dict[str, int] = {}
    for index, entry in enumerate(transfers):
        if not isinstance(entry, dict):
            findings.append(Finding(
                "EVRH-XFER-01", "every transfer is an object",
                f"transfer {index} is {type(entry).__name__}"))
            continue
        shape = tuple(sorted(entry))
        if shape not in TRANSFER_KEYSHAPES:
            findings.append(Finding(
                "EVRH-XFER-01",
                "every transfer carries one of the two admitted key shapes",
                f"transfer {index} ({entry.get('id')}) has {list(shape)}"))
        state = entry.get("state")
        if isinstance(state, str):
            census[state] = census.get(state, 0) + 1
        digest = entry.get("sourceSha256")
        if digest is not None and not (
                isinstance(digest, str) and SHA256_RE.match(digest)):
            findings.append(Finding(
                "EVRH-XFER-01",
                "every declared source digest is a full lowercase sha256",
                f"transfer {index} ({entry.get('id')}): {digest!r}"))
    if census != TRANSFER_STATE_CENSUS:
        findings.append(Finding(
            "EVRH-XFER-02",
            "the closure-state census equals the gated census exactly -- a "
            "finding cannot change closure state without the census moving",
            f"measured {dict(sorted(census.items()))}, gated "
            f"{dict(sorted(TRANSFER_STATE_CENSUS.items()))}"))
    if TRANSFER33_INDEX < len(transfers) and isinstance(
            transfers[TRANSFER33_INDEX], dict):
        entry = transfers[TRANSFER33_INDEX]
        if entry.get("state") != TRANSFER33_STATE:
            findings.append(Finding(
                "EVRH-XFER-03",
                "the retained-checker scan description is closed by an "
                "EXECUTED probe, not by a derivation",
                f"transfer {TRANSFER33_INDEX} state {entry.get('state')!r}, "
                f"expected {TRANSFER33_STATE!r}"))
        closure = entry.get("closure")
        if not isinstance(closure, str):
            findings.append(Finding(
                "EVRH-XFER-03", "the transfer's closure is prose",
                f"closure is {type(closure).__name__}"))
        else:
            for phrase in TRANSFER33_REQUIRED:
                if phrase not in closure:
                    findings.append(Finding(
                        "EVRH-XFER-03",
                        "the transfer that describes the narrowed flag scan "
                        "still states every clause this instrument implements "
                        "from it",
                        f"transfer {TRANSFER33_INDEX} closure is missing "
                        f"{phrase!r}"))
    else:
        findings.append(Finding(
            "EVRH-XFER-03",
            "the transfer describing the narrowed flag scan is at its gated "
            "index",
            f"transfer {TRANSFER33_INDEX} is absent or not an object"))
    return findings


def check_mode_contract(resolved: Any) -> list[Finding]:
    """The instrument's own mode contract IS the resolved head's, measured."""
    findings: list[Finding] = []
    contract = resolved.get("checkerModeContract")
    if not isinstance(contract, dict):
        return [Finding(
            "EVRH-MODE-01", "the resolved contract carries a checkerModeContract",
            f"checkerModeContract is {type(contract).__name__}")]

    table = contract.get("exitCodes")
    if not isinstance(table, dict):
        findings.append(Finding(
            "EVRH-MODE-01", "the mode contract publishes an exitCodes table",
            f"exitCodes is {type(table).__name__}"))
    else:
        if sorted(table) != sorted(HEAD_EXIT_NAMES):
            findings.append(Finding(
                "EVRH-MODE-01",
                "the head's exitCodes table names exactly the four "
                "dispositions this instrument implements unrenumbered",
                f"head names {sorted(table)}, implemented "
                f"{sorted(HEAD_EXIT_NAMES)}"))
        for name in sorted(HEAD_EXIT_NAMES):
            declared = table.get(name, _ABSENT)
            mine = EXIT.get(name, _ABSENT)
            if not exact_equal(declared, mine):
                findings.append(Finding(
                    "EVRH-MODE-01",
                    "this instrument's exit code for each of the head's four "
                    "dispositions IS the head's, measured from resolved bytes "
                    "and compared type-exactly -- not invented and not "
                    "transcribed",
                    f"{name}: head {declared!r} "
                    f"({type(declared).__name__}), instrument {mine!r} "
                    f"({type(mine).__name__})"))
        if EXIT[SUCCESSOR_EXIT_NAME] in set(EXIT[name] for name in HEAD_EXIT_NAMES):
            findings.append(Finding(
                "EVRH-MODE-04",
                "the successor's trust-root integrity code is DISTINCT from "
                "the four dispositions it must not renumber",
                f"{SUCCESSOR_EXIT_NAME} is {EXIT[SUCCESSOR_EXIT_NAME]}, which "
                "collides with a head disposition"))

    declared_flags = contract.get("declaredFlags")
    entrypoints = contract.get("entrypoints")
    if isinstance(entrypoints, list) and isinstance(declared_flags, list):
        implied = sorted({token for line in entrypoints
                          if isinstance(line, str)
                          for token in line.split()
                          if token.startswith("--")})
        if implied != sorted(declared_flags):
            findings.append(Finding(
                "EVRH-MODE-02",
                "the head's declaredFlags equal the flags implied by its own "
                "entrypoints -- the same equality this instrument enforces "
                "over itself",
                f"entrypoints imply {implied}, declaredFlags "
                f"{sorted(declared_flags)}"))
    else:
        findings.append(Finding(
            "EVRH-MODE-02",
            "the head declares an entrypoints list and a declaredFlags list",
            f"entrypoints={type(entrypoints).__name__}, "
            f"declaredFlags={type(declared_flags).__name__}"))

    note = contract.get("exitCodesNote")
    if not isinstance(note, str):
        findings.append(Finding(
            "EVRH-MODE-03",
            "the v14-added exitCodesNote is present and points at the "
            "disclosure it summarises",
            f"exitCodesNote is {type(note).__name__}"))
    else:
        for phrase in EXIT_CODES_NOTE_REQUIRED:
            if phrase not in note:
                findings.append(Finding(
                    "EVRH-MODE-03",
                    "the exitCodesNote still names the fifth termination "
                    "behaviour and the section that discloses it",
                    f"exitCodesNote is missing {phrase!r}"))

    hostile = resolved.get("hostileInputTotalityContract")
    discipline = hostile.get("exitDiscipline") if isinstance(hostile, dict) else None
    if not isinstance(discipline, str):
        findings.append(Finding(
            "EVRH-MODE-04",
            "hostileInputTotalityContract.exitDiscipline discloses the fifth "
            "termination behaviour",
            f"exitDiscipline is {type(discipline).__name__}"))
    else:
        for phrase in EXIT_DISCIPLINE_REQUIRED:
            if phrase not in discipline:
                findings.append(Finding(
                    "EVRH-MODE-04",
                    "the exitDiscipline still discloses the uncaught "
                    "trust-root failure AND still binds the distinct-exit-code "
                    "obligation this instrument discharges at exit "
                    f"{EXIT[SUCCESSOR_EXIT_NAME]}",
                    f"exitDiscipline is missing {phrase!r}"))
    return findings


def check_self_scans(tree: ast.Module | None = None) -> list[Finding]:
    """TRIPWIRES.  See the header: these prove properties of this file's SYNTAX
    and nothing about its semantics.

    `tree` is the subject.  It defaults to this file's own tree; the source
    self-mutation battery passes a DELIBERATELY BROKEN tree instead, so that
    each scan is shown to fire rather than merely shown to pass.  A scan that
    has never been observed to fail is indistinguishable from one that measures
    nothing.
    """
    findings: list[Finding] = []
    tree = own_tree() if tree is None else tree
    compared = comparison_flag_literals(tree)
    declared_literals = declared_flag_literals(tree)
    declared = set(DECLARED_FLAGS)
    implied = {token for line in MODE_CONTRACT["entrypoints"]
               for token in line.split() if token.startswith("--")}

    if not compared:
        findings.append(Finding(
            "EVRH-MODE-05",
            "the comparison-node flag scan is non-vacuous -- a scan that "
            "collects zero flag literals cannot be distinguished from one that "
            "measures nothing",
            "the scan collected 0 flag literals from comparison nodes"))
    collected = compared | declared_literals
    if collected != declared:
        findings.append(Finding(
            "EVRH-MODE-05",
            "the flag literals inside comparison nodes, together with the "
            "DECLARED_FLAGS constant's own literals, equal the declared flag "
            "set (the head's narrowed scan, applied to this file)",
            f"collected {sorted(collected)}, declared {sorted(declared)}"))
    if implied != declared:
        findings.append(Finding(
            "EVRH-MODE-05",
            "the declared flag set equals the flags implied by this "
            "instrument's own declared entrypoints",
            f"entrypoints imply {sorted(implied)}, declared {sorted(declared)}"))

    scan = selftest_dispatch_scan(tree)
    if len(scan["dispatches"]) != 1:
        findings.append(Finding(
            "EVRH-MODE-06",
            "there is EXACTLY ONE dispatch to the selftest suite, so there is "
            "no second undocumented selftest entrypoint",
            f"{len(scan['dispatches'])} dispatch(es) at "
            f"{[item['line'] for item in scan['dispatches']]}"))
    for dispatch in scan["dispatches"]:
        if not set(dispatch["guards"]) & declared:
            findings.append(Finding(
                "EVRH-MODE-06",
                "the single selftest dispatch is lexically guarded by a "
                "declared flag",
                f"dispatch at line {dispatch['line']} is guarded by "
                f"{dispatch['guards']}"))
    if scan["mainCount"] != 1:
        findings.append(Finding(
            "EVRH-MODE-07",
            "this instrument defines exactly one main()",
            f"{scan['mainCount']} main() definition(s)"))
    elif scan["dispatchIndex"] is None:
        findings.append(Finding(
            "EVRH-MODE-07",
            "main() dispatches to the selftest suite under a declared flag",
            "main() carries no flag-guarded selftest dispatch"))
    elif (scan["findingsIndex"] is not None
            and scan["findingsIndex"] < scan["dispatchIndex"]):
        findings.append(Finding(
            "EVRH-MODE-07",
            "within main(), the selftest dispatch PRECEDES any findings "
            "return, so no unconditional finding gate can sit in front of the "
            "mutation suite",
            f"findings return at main() statement {scan['findingsIndex']}, "
            f"selftest dispatch at statement {scan['dispatchIndex']}"))
    return findings


# ---------------------------------------------------------------------------
# This instrument's own mode contract, rendered from the same constants the
# code uses so a document and a file cannot disagree about it.
# ---------------------------------------------------------------------------
MODE_CONTRACT: dict[str, Any] = {
    "entrypoints": [
        f"python3 -I -B artifacts/{CHECKER}",
        f"python3 -I -B artifacts/{CHECKER} {DECLARED_FLAGS[0]}",
        f"python3 -I -B artifacts/{CHECKER} {DECLARED_FLAGS[1]}",
    ],
    "declaredFlags": list(DECLARED_FLAGS),
    "exitCodes": dict(EXIT),
}


# ---------------------------------------------------------------------------
# The run
# ---------------------------------------------------------------------------
class Report(NamedTuple):
    findings: list[Finding]
    resolved: Any
    measured: dict[str, Any]
    notMeasured: list[str]


def validate(root: pathlib.Path,
             chain_pins: tuple[tuple[str, str], ...] = CHAIN_PINS) -> Report:
    """Every class, against one tree.  Returns findings sorted deterministically
    and names every class that DID NOT RUN, so an absent measurement can never
    be read as a passing one (freeze section 7.8.1).

    `chain_pins` defaults to the GATED table.  Only the mutation suite ever
    passes a different one, and only ever for a disposable /tmp copy: re-pinning
    in scratch is how a mutation reaches the semantic layers instead of stopping
    at the digest gate.  The RESOLVER pins are not parameterised at all.
    """
    resolvers = gate_resolvers(root)
    chain = [read_document(root, name, pin) for name, pin in chain_pins]
    head = chain[0]

    findings: list[Finding] = []
    not_measured: list[str] = []
    findings.extend(check_documents(chain))
    findings.extend(check_declared_links(chain, chain_pins))
    findings.extend(check_terminus(chain, resolvers))
    findings.extend(check_head_identity(head))
    findings.extend(check_accounting(chain))

    candidates: dict[str, Any] = {}
    provenances: dict[str, Any] = {}
    for label, module in (("check-completeness.py", resolvers.r1),
                          ("check-completeness-v2.py", resolvers.r2)):
        effective, resolve_findings, provenance = resolve_with(module, label, head)
        findings.extend(resolve_findings)
        if effective is not None:
            candidates[label] = effective
            provenances[label] = provenance

    walked, walk_errors, unwalkable = independent_resolve(chain)
    if unwalkable:
        not_measured.append(
            "EVRH-CHAIN-07 independent pointer walk: the chain uses a path "
            f"dialect this instrument does not implement ({unwalkable}); the "
            "walk was NOT run and the gated resolvers were not cross-checked "
            "against it")
    for error in walk_errors:
        findings.append(Finding(
            "EVRH-CHAIN-07",
            "this instrument's own pointer walk resolves the chain, verifying "
            "every set's 'from' type-exactly against the predecessor it is "
            "applied to -- independently of the gated resolvers",
            error))
    if walked is not None:
        candidates["independent-pointer-walk"] = walked

    for label in sorted(provenances):
        findings.extend(check_provenance(provenances[label], label, chain_pins))
    if len(candidates) > 1:
        findings.extend(check_agreement(candidates))

    resolved = candidates.get("check-completeness-v2.py") or (
        candidates.get("check-completeness.py") or walked)
    measured: dict[str, Any] = {
        "gatedResolvers": dict(sorted(resolvers.measured.items())),
        "chain": [(document.name, document.measured) for document in chain],
        "resolvedCanonical": None,
        "sections": {},
    }
    if resolved is None:
        not_measured.append(
            "EVRH-CANON-01/EVRH-SECT-01/EVRH-GRAM-*/EVRH-RES-*/EVRH-XFER-*/"
            "EVRH-MODE-01..04/EVRH-ITEM4-*: the effective contract could not "
            "be materialised, so no class over the RESOLVED document ran. "
            "This is not a pass.")
    else:
        measured["resolvedCanonical"] = sha256_hex(
            resolvers.r2.canonical_bytes(resolved))
        measured["sections"] = {
            section: sha256_hex(canonical_bytes(resolved[section]))
            for section in sorted(SECTION_PINS) if section in resolved}
        findings.extend(check_canonical(resolved, resolvers))
        findings.extend(check_item4(resolved, chain))
        findings.extend(check_grammar(resolved))
        findings.extend(check_residuals(resolved))
        findings.extend(check_transfers(resolved))
        findings.extend(check_mode_contract(resolved))
    findings.extend(check_self_scans())
    # Tree-independent, so it contributes identically to the selftest baseline
    # and to every mutation and cannot distort a finding-set delta.  It is run
    # HERE rather than only in the default path so that "the base is clean"
    # means the same thing in both modes.
    findings.extend(check_argument_discipline())

    findings.sort(key=lambda item: (item.id, item.detail))
    return Report(findings=findings, resolved=resolved, measured=measured,
                  notMeasured=sorted(not_measured))


# ---------------------------------------------------------------------------
# Mutation selftest.  DISPOSABLE /tmp COPIES ONLY -- the live tree is never
# written to, and every copy is removed on completion.
# ---------------------------------------------------------------------------
TMP_ROOT = "/tmp"
TMP_PREFIX = "evrh-28dc3c1a-"

COPIED_FILES: tuple[str, ...] = tuple(
    sorted(RESOLVER_PINS) + [name for name, _ in CHAIN_PINS])


def _stage(target: pathlib.Path) -> None:
    (target / "artifacts").mkdir(parents=True, exist_ok=True)
    for name in COPIED_FILES:
        shutil.copyfile(HERE / name, target / "artifacts" / name)


def _read_text(target: pathlib.Path, name: str) -> str:
    return (target / "artifacts" / name).read_text(encoding="utf-8")


def _write_text(target: pathlib.Path, name: str, text: str) -> None:
    (target / "artifacts" / name).write_text(text, encoding="utf-8")


def _edit_head(target: pathlib.Path, edit: Callable[[dict], None]) -> None:
    """Rewrite the head with an edit applied and RE-PIN it in the working copy.

    Re-pinning in scratch is what lets a mutation reach the semantic layers
    instead of stopping at the digest gate -- the same technique the freeze
    section 7.8 instruments used to show, separately, that the pin fires on
    drift and the semantics fire on gutting.  The GATED RESOLVER pins are never
    re-pinned by any mutation except the one that exists to prove they refuse.
    """
    document = json.loads(_read_text(target, HEAD_FILE))
    edit(document)
    _write_text(target, HEAD_FILE,
                json.dumps(document, indent=1, ensure_ascii=False) + "\n")


def _repin_head(target: pathlib.Path) -> tuple[str, str]:
    raw = (target / "artifacts" / HEAD_FILE).read_bytes()
    return HEAD_FILE, sha256_hex(raw)


def _mutate_chain_link_digest(target: pathlib.Path) -> None:
    text = _read_text(target, "evidence.v13.json")
    _write_text(target, "evidence.v13.json",
                text.replace('"date": "2026-08-13"', '"date": "2026-08-14"', 1))


def _mutate_canonical(target: pathlib.Path) -> None:
    def edit(document: dict) -> None:
        operations = document["derivedFrom"]["operations"]
        operations[2]["value"] = operations[2]["value"].replace(
            "for their measured coverage only.",
            "for their measured coverage only. ", 1)
    _edit_head(target, edit)


def _mutate_residual_sentence(target: pathlib.Path) -> None:
    def edit(document: dict) -> None:
        operations = document["derivedFrom"]["operations"]
        operations[1]["value"] = operations[1]["value"].replace(
            "(2026-08-02, the count's date", "(2026-08-12, the count's date", 1)
    _edit_head(target, edit)


def _mutate_item4_byte(target: pathlib.Path) -> None:
    def edit(document: dict) -> None:
        operations = document["derivedFrom"]["operations"]
        operations.append({
            "op": "set",
            "path": "/availabilityDifferential/mutation",
            "from": "remove one replay-only raw object from current RT13 "
                    "availability",
            "value": "remove two replay-only raw objects from current RT13 "
                     "availability",
        })
        document["operationAccounting"]["total"] = 4
        document["operationAccounting"]["sets"] = 4
    _edit_head(target, edit)


def _mutate_type_respell(target: pathlib.Path) -> None:
    def edit(document: dict) -> None:
        document["operationAccounting"]["sets"] = 3.0
    _edit_head(target, edit)


def _mutate_duplicate_key(target: pathlib.Path) -> None:
    text = _read_text(target, HEAD_FILE)
    _write_text(target, HEAD_FILE,
                text.replace('"version": 15,', '"version": 15,\n "version": 15,',
                             1))


def _mutate_dropped_operation(target: pathlib.Path) -> None:
    def edit(document: dict) -> None:
        del document["derivedFrom"]["operations"][1]
    _edit_head(target, edit)


def _mutate_from_drift(target: pathlib.Path) -> None:
    def edit(document: dict) -> None:
        operations = document["derivedFrom"]["operations"]
        operations[0]["from"] = operations[0]["from"].replace(
            "V10 remains unresolved.", "V10 remains unresolved!", 1)
    _edit_head(target, edit)


class Mutation(NamedTuple):
    label: str
    apply: Callable[[pathlib.Path], None]
    repin: bool
    required: tuple[str, ...]
    invariantClass: str


MUTATIONS: tuple[Mutation, ...] = (
    Mutation("chain-link-digest", _mutate_chain_link_digest, False,
             ("EVRH-CHAIN-01", "EVRH-CHAIN-03"),
             "chain-link digest"),
    Mutation("canonical-digest", _mutate_canonical, True,
             ("EVRH-CANON-01", "EVRH-SECT-01"),
             "resolved canonical digest"),
    Mutation("residual-sentence", _mutate_residual_sentence, True,
             ("EVRH-RES-02", "EVRH-SECT-01"),
             "a residual sentence"),
    Mutation("item-4-byte", _mutate_item4_byte, True,
             ("EVRH-ITEM4-01", "EVRH-ITEM4-02"),
             "an item-4 byte"),
    Mutation("type-respell", _mutate_type_respell, True,
             ("EVRH-ACCT-01",),
             "a type respell (3 -> 3.0)"),
    Mutation("duplicate-key-injection", _mutate_duplicate_key, True,
             ("EVRH-DUP-01",),
             "a duplicate-key injection"),
    Mutation("dropped-operation", _mutate_dropped_operation, True,
             ("EVRH-ACCT-01", "EVRH-CANON-01"),
             "a dropped operation"),
    Mutation("from-drift", _mutate_from_drift, True,
             ("EVRH-CHAIN-03", "EVRH-CHAIN-07"),
             "a 'from' drift"),
)


# ---------------------------------------------------------------------------
# Source self-mutation battery.
#
# The three self-scans (EVRH-MODE-05/06/07) pass on every honest run, which is
# exactly what makes them worthless as published evidence unless each is also
# shown to FIRE.  These mutations break one scanned property at a time in an
# IN-MEMORY syntax tree -- no file is written, not even under /tmp -- and
# require the corresponding scan to report it.
#
# The head's escapeRule governs here too: a syntax-tree mutation that does not
# change the tree, or that its scan does not report, is an ESCAPE, never a pass.
# ---------------------------------------------------------------------------
def _main_body(tree: ast.Module) -> list[Any] | None:
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == "main":
            return node.body
    return None


def _sm_undocumented_flag(tree: ast.Module) -> None:
    """An undocumented flag literal reaching a comparison node."""
    body = _main_body(tree)
    if body is not None:
        body.insert(0, ast.parse(
            'if "--undocumented" in flags:\n    pass\n').body[0])


def _sm_second_dispatch(tree: ast.Module) -> None:
    """A second, undocumented selftest entrypoint."""
    body = _main_body(tree)
    if body is not None:
        body.insert(0, ast.parse(
            'if "--selftest" in flags:\n    return selftest(root)\n').body[0])


def _sm_finding_gate(tree: ast.Module) -> None:
    """An unconditional finding gate in front of the mutation suite."""
    body = _main_body(tree)
    if body is not None:
        body.insert(0, ast.parse('return EXIT["findings"]\n').body[0])


def _sm_vacuous_scan(tree: ast.Module) -> None:
    """Every flag literal removed from every comparison node, which is what a
    scan rewritten into vacuity would look like."""
    for node in ast.walk(tree):
        if not isinstance(node, ast.Compare):
            continue
        for child in ast.walk(node):
            if (isinstance(child, ast.Constant)
                    and isinstance(child.value, str)
                    and child.value.startswith("--")):
                child.value = "<removed>"


SOURCE_MUTATIONS: tuple[tuple[str, Callable[[ast.Module], None], str, str], ...] = (
    ("undocumented-flag", _sm_undocumented_flag, "EVRH-MODE-05",
     "an undocumented flag literal reaching a comparison node"),
    ("vacuous-flag-scan", _sm_vacuous_scan, "EVRH-MODE-05",
     "every flag literal removed from every comparison node"),
    ("second-dispatch", _sm_second_dispatch, "EVRH-MODE-06",
     "a second, undocumented selftest entrypoint"),
    ("finding-gate-first", _sm_finding_gate, "EVRH-MODE-07",
     "an unconditional finding gate in front of the suite"),
)


def _run_source_mutation(label: str, apply: Callable[[ast.Module], None],
                         required: str, description: str) -> dict[str, Any]:
    subject = copy.deepcopy(own_tree())
    before = ast.dump(subject)
    apply(subject)
    ast.fix_missing_locations(subject)
    if ast.dump(subject) == before:
        return {"label": label, "escape": True, "required": required,
                "produced": [], "description": description,
                "reason": "the syntax-tree mutation did not change the tree"}
    try:
        produced = {item.id for item in check_self_scans(subject)}
    except Exception as exc:                           # noqa: BLE001 - reported
        return {"label": label, "escape": True, "required": required,
                "produced": [], "description": description,
                "reason": f"the scan raised {type(exc).__name__}"}
    return {"label": label, "escape": required not in produced,
            "required": required, "produced": sorted(produced),
            "description": description,
            "reason": "" if required in produced else
            "the corresponding scan did not report the broken property"}


# The whole battery: the eight invariant-class mutations, the four source
# self-mutations, and the gated-pin tamper probe.  One constant so the refusal
# banner and the pass census cannot quote different totals.
MUTATION_CENSUS = len(MUTATIONS) + len(SOURCE_MUTATIONS) + 1


def _run_mutation(mutation: Mutation, baseline: frozenset[str]) -> dict[str, Any]:
    target = pathlib.Path(tempfile.mkdtemp(dir=TMP_ROOT, prefix=TMP_PREFIX))
    try:
        _stage(target)
        before = {name: (target / "artifacts" / name).read_bytes()
                  for name in COPIED_FILES}
        mutation.apply(target)
        after = {name: (target / "artifacts" / name).read_bytes()
                 for name in COPIED_FILES}
        touched = sorted(name for name in COPIED_FILES
                         if before[name] != after[name])
        if not touched:
            return {"label": mutation.label, "escape": True, "delta": [],
                    "missing": list(mutation.required), "touched": [],
                    "reason": "the mutation applied without changing any byte"}
        pins = dict(CHAIN_PINS)
        if mutation.repin:
            name, digest = _repin_head(target)
            pins[name] = digest
        report = validate(target,
                          tuple((name, pins[name]) for name, _ in CHAIN_PINS))
        produced = frozenset(item.id for item in report.findings)
        delta = sorted(produced - baseline)
        missing = sorted(set(mutation.required) - produced)
        return {"label": mutation.label, "escape": bool(missing), "delta": delta,
                "missing": missing, "touched": touched, "reason": ""}
    finally:
        shutil.rmtree(target, ignore_errors=True)


def _run_gate_probe() -> dict[str, Any]:
    """The gated-pin refusal, proven rather than asserted."""
    target = pathlib.Path(tempfile.mkdtemp(dir=TMP_ROOT, prefix=TMP_PREFIX))
    try:
        _stage(target)
        name = "check-completeness-v2.py"
        path = target / "artifacts" / name
        before = path.read_bytes()
        path.write_bytes(before + b"\n# gated-pin tamper probe\n")
        if path.read_bytes() == before:
            return {"label": "gated-resolver-tamper", "escape": True,
                    "reason": "the tamper applied without changing any byte"}
        try:
            validate(target)
        except TrustRootIntegrityError as exc:
            text = str(exc)
            ok = ("EVRH-GATE-01" in text and name in text
                  and RESOLVER_PINS[name] in text)
            return {"label": "gated-resolver-tamper", "escape": not ok,
                    "reason": "" if ok else
                    "refused, but the refusal did not name the file and its "
                    "gated pin"}
        return {"label": "gated-resolver-tamper", "escape": True,
                "reason": "tampered resolver bytes were executed instead of "
                          "refused"}
    finally:
        shutil.rmtree(target, ignore_errors=True)


def selftest(root: pathlib.Path) -> int:
    """Always reaches the suite; refuses a dirty base at a distinct code.

    A mutation suite over a red base is not an oracle: with findings already
    present, a mutation that produces the same findings is indistinguishable
    from one that is caught.  So a dirty base refuses at exit 3 and the dirty
    base is reported.
    """
    try:
        base = validate(root)
    except TrustRootIntegrityError as exc:
        print(f"SELFTEST-REFUSED: {exc}", file=sys.stderr)
        return EXIT[SUCCESSOR_EXIT_NAME]
    except Malformed as exc:
        print(f"SELFTEST-REFUSED: {exc}", file=sys.stderr)
        return EXIT["unsupportedInvocationOrInput"]
    if base.findings:
        print("SELFTEST-REFUSED: the base is not clean, so the mutation suite "
              "is not an oracle over it.")
        print(f"  dirty base: {len(base.findings)} finding(s)")
        for finding in base.findings[:10]:
            print("  base-finding:", finding.render())
        if len(base.findings) > 10:
            print(f"  ... {len(base.findings) - 10} further base finding(s)")
        print(f"SELFTEST-NOT-RUN: 0 of {MUTATION_CENSUS} mutations executed; "
              f"exit {EXIT['selftestRefusedDirtyBase']} distinguishes this "
              "refusal from a green selftest and from an ordinary failure.")
        return EXIT["selftestRefusedDirtyBase"]

    baseline = frozenset(item.id for item in base.findings)
    print(f"mutation self-test -- {SUBJECT} resolved head")
    print("  every mutation runs in a DISPOSABLE copy under /tmp; the live "
          "tree is never written to")
    print("  ESCAPE RULE: a mutation that fails to apply, or that applies "
          "without changing bytes,")
    print("  or that does not produce every required finding ID, is an ESCAPE "
          "-- never a pass")
    results = [_run_mutation(mutation, baseline) for mutation in MUTATIONS]
    caught = sum(1 for item in results if not item["escape"])
    for mutation, result in zip(MUTATIONS, results):
        status = "ESCAPE" if result["escape"] else "caught"
        print(f"  {status:<6} {mutation.label:<24} mutates "
              f"{mutation.invariantClass}")
        print(f"         required {list(mutation.required)}; "
              f"finding-set delta {result['delta']}")
        if result["escape"]:
            print(f"         MISSING {result['missing']} "
                  f"{result['reason']}".rstrip())
    source_results = [_run_source_mutation(*item) for item in SOURCE_MUTATIONS]
    source_caught = sum(1 for item in source_results if not item["escape"])
    for result in source_results:
        status = "ESCAPE" if result["escape"] else "caught"
        print(f"  {status:<6} {result['label']:<24} mutates this file's own "
              f"syntax tree: {result['description']}")
        print(f"         required {result['required']}; scan reported "
              f"{result['produced']}")
        if result["escape"]:
            print(f"         {result['reason']}")
    gate = _run_gate_probe()
    gate_ok = not gate["escape"]
    print(f"  {'caught' if gate_ok else 'ESCAPE':<6} "
          f"{'gated-resolver-tamper':<24} mutates the gated resolver bytes")
    print(f"         required a typed refusal at exit "
          f"{EXIT[SUCCESSOR_EXIT_NAME]} naming EVRH-GATE-01 and the gated pin;"
          f" {'refused as required' if gate_ok else gate['reason']}")
    total = MUTATION_CENSUS
    caught_total = caught + source_caught + (1 if gate_ok else 0)
    print(f"  census: {caught_total}/{total} caught, "
          f"{total - caught_total} escape(s)")
    print("  scope, per the resolved head's retainedResiduals[13]: the "
          "artifact mutations and the")
    print("         gate probe are the SEMANTIC oracle. The four source "
          "mutations prove only that")
    print("         the EVRH-MODE-05/06/07 tripwires FIRE -- they remain "
          "SYNTACTIC, for their measured")
    print("         coverage only, and the head's two recorded evasions of "
          "this scan family are")
    print("         inherited here and are NOT claimed closed.")
    if caught_total != total:
        return EXIT["findings"]
    print(f"SELFTEST-PASS: {caught_total}/{total} mutations caught")
    return EXIT["clean"]


# ---------------------------------------------------------------------------
# Argument discipline -- the head's, total.
# ---------------------------------------------------------------------------
def parse_argv(argv: Any) -> tuple[frozenset[str], Any]:
    if not isinstance(argv, (list, tuple)) or not argv:
        raise UnsupportedInvocation("no argument vector was supplied")
    flags: list[str] = []
    positional: list[Any] = []
    for item in list(argv)[1:]:
        if isinstance(item, str) and item.startswith("--"):
            if item not in DECLARED_FLAGS:
                raise UnsupportedInvocation(f"unknown flag {item!r}")
            flags.append(item)
        else:
            positional.append(item)
    if len(positional) > 1:
        raise UnsupportedInvocation(
            f"{len(positional)} positional corpus roots supplied; exactly one "
            "is accepted")
    if DECLARED_FLAGS[0] in flags and DECLARED_FLAGS[1] in flags:
        raise UnsupportedInvocation(
            f"{DECLARED_FLAGS[0]} and {DECLARED_FLAGS[1]} are mutually exclusive")
    if DECLARED_FLAGS[1] in flags and positional:
        raise UnsupportedInvocation(
            f"{DECLARED_FLAGS[1]} takes no positional path")
    return frozenset(flags), (positional[0] if positional else None)


ARGUMENT_BATTERY: tuple[tuple[str, Any, bool], ...] = (
    ("bare", ["x"], True),
    ("root-only", ["x", "docs/coop"], True),
    ("selftest", ["x", DECLARED_FLAGS[0]], True),
    ("selftest-with-root", ["x", "docs/coop", DECLARED_FLAGS[0]], True),
    ("selftest-repeated", ["x", DECLARED_FLAGS[0], DECLARED_FLAGS[0]], True),
    ("selftest-before-path", ["x", DECLARED_FLAGS[0], "docs/coop"], True),
    ("emit", ["x", DECLARED_FLAGS[1]], True),
    ("unknown-flag", ["x", "--foundation-selftest"], False),
    ("unknown-flag-with-selftest", ["x", DECLARED_FLAGS[0], "--bogus"], False),
    ("bare-double-dash", ["x", "--"], False),
    ("two-positionals", ["x", "a", "b"], False),
    ("two-positionals-with-selftest", ["x", "a", "b", DECLARED_FLAGS[0]], False),
    ("emit-with-root", ["x", DECLARED_FLAGS[1], "a"], False),
    ("emit-and-selftest", ["x", DECLARED_FLAGS[1], DECLARED_FLAGS[0]], False),
    ("empty-vector", [], False),
    ("not-a-vector", "x --selftest", False),
)


def check_argument_discipline() -> list[Finding]:
    findings: list[Finding] = []
    for label, argv, accepted in ARGUMENT_BATTERY:
        try:
            parse_argv(argv)
        except UnsupportedInvocation:
            if accepted:
                findings.append(Finding(
                    "EVRH-CLI-01",
                    "every supported invocation in the declared discipline is "
                    "accepted and every unsupported one is refused by name, "
                    "never silently ignored",
                    f"{label} is supported but was refused"))
            continue
        except Exception as exc:                       # noqa: BLE001 - reported
            findings.append(Finding(
                "EVRH-CLI-01",
                "an unsupported invocation is refused, not raised through",
                f"{label} raised {type(exc).__name__}"))
            continue
        if not accepted:
            findings.append(Finding(
                "EVRH-CLI-01",
                "an unsupported invocation is refused with a named reason",
                f"{label} was accepted silently"))
    return findings


def print_banner(report: Report) -> None:
    print(f"EVIDENCE resolved-head validator -- subject {SUBJECT} "
          f"({dict(CHAIN_PINS)[HEAD_FILE][:16]}…)")
    print("  gated resolver bytes (reviewed; a mismatch REFUSES at exit "
          f"{EXIT[SUCCESSOR_EXIT_NAME]}, which is correct freeze section 7.8.1 "
          "behaviour, not a defect):")
    for name in sorted(report.measured["gatedResolvers"]):
        print(f"    {name:<26} {report.measured['gatedResolvers'][name]}")
    print("  chain, head first, terminating at the section 7.3 terminus:")
    for name, digest in report.measured["chain"]:
        mark = " (TERMINUS)" if name == TERMINUS_FILE else ""
        print(f"    {name:<20} {digest}{mark}")
    print(f"  resolved canonical: {report.measured['resolvedCanonical']}")
    print("  gated section digests, recomputed:")
    for section in sorted(report.measured["sections"]):
        print(f"    {section:<30} {report.measured['sections'][section]}")
    print("  exit table (rendered from the same EXIT table every return reads):")
    for name in sorted(EXIT, key=lambda item: EXIT[item]):
        origin = ("resolved head's checkerModeContract.exitCodes, measured"
                  if name in HEAD_EXIT_NAMES
                  else "successor obligation from exitDiscipline, discharged here")
        print(f"    {EXIT[name]}  {name:<30} {origin}")


def print_scope() -> None:
    print("  what a green run proves (freeze section 7.8): this artifact says "
          "what it says,")
    print("    consistently, and drift will be caught. NOT that this artifact "
          "is right.")
    print("  what it does NOT do: no claim-register motion authority; not the "
          "section 3.1")
    print("    Phase-1A packet; not a review; grants no seal, freeze, "
          "application or product")
    print("    acceptance; does not sign CD-RT-5. Independent review of these "
          "instrument bytes")
    print("    remains REQUIRED.")


def main(argv: list[str]) -> int:
    try:
        flags, requested = parse_argv(argv)
    except UnsupportedInvocation as exc:
        print(f"EVRH-UNSUPPORTED-INVOCATION: {exc}", file=sys.stderr)
        return EXIT["unsupportedInvocationOrInput"]
    root = pathlib.Path(requested).resolve() if requested is not None \
        else HERE.parent

    if "--emit-resolved" in flags:
        try:
            report = validate(root)
        except TrustRootIntegrityError as exc:
            print(str(exc), file=sys.stderr)
            return EXIT[SUCCESSOR_EXIT_NAME]
        except Malformed as exc:
            print(f"EVRH-INPUT: {exc}", file=sys.stderr)
            return EXIT["unsupportedInvocationOrInput"]
        if report.resolved is None:
            print("EVRH-INPUT: the effective contract could not be "
                  "materialised; nothing is emitted", file=sys.stderr)
            return EXIT["unsupportedInvocationOrInput"]
        # A write failure on the emission sink -- a closed pipe being the
        # ordinary case -- must NOT propagate as an uncaught traceback at
        # exit 1.  That is precisely the defect shape the resolved head's
        # exitDiscipline discloses in the retained checker: a non-finding
        # terminating at the code the table reserves for findings.  The
        # successor does not reproduce it.
        try:
            sys.stdout.buffer.write(canonical_bytes(report.resolved))
            sys.stdout.buffer.write(b"\n")
            sys.stdout.buffer.flush()
        except OSError as exc:
            print(f"EVRH-INPUT: the emission sink could not be written "
                  f"({type(exc).__name__}); nothing was emitted", file=sys.stderr)
            return EXIT["unsupportedInvocationOrInput"]
        return EXIT["clean"]

    if "--selftest" in flags:
        return selftest(root)

    try:
        report = validate(root)
    except TrustRootIntegrityError as exc:
        print(str(exc), file=sys.stderr)
        return EXIT[SUCCESSOR_EXIT_NAME]
    except Malformed as exc:
        print(f"EVRH-INPUT: {exc}", file=sys.stderr)
        return EXIT["unsupportedInvocationOrInput"]

    findings = list(report.findings)
    print_banner(report)
    if report.notMeasured:
        print("  classes that DID NOT RUN (an absent measurement is not a "
              "passing one):")
        for line in report.notMeasured:
            print(f"    - {line}")
    if findings:
        classes = sorted({item.id for item in findings})
        print(f"  {len(findings)} finding(s) across {len(classes)} class(es): "
              f"{classes}")
        for finding in findings:
            print("  -", finding.render())
        print_scope()
        return EXIT["findings"]
    print(f"  0 findings; chain of {len(CHAIN_PINS)} links verified; "
          f"{len(RESOLVER_PINS)} gated resolvers hash-verified before "
          f"execution; {len(SECTION_PINS)} sections recomputed; "
          f"{len(GRAMMAR_RECORDS)} wire record types, {RESIDUAL_COUNT} "
          f"residuals, {TRANSFER_COUNT} transfers checked")
    print_scope()
    return EXIT["clean"]


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
