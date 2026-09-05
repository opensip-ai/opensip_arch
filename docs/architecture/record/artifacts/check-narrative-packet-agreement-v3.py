#!/usr/bin/env python3
"""Executable agreement between the package's PROSE and the corpus it describes.

SUCCESSOR to `check-narrative-packet-agreement-v2.py`
(`26f6eea8520f8fa99fdae4752e742458185ed767aab29b696005e7eb8c007037`, 100627
bytes -- MEASURED HERE, not carried from the dispatch -- independently reviewed
at ACCEPT / 1 blocking / 9 non-blocking).  Freeze section 7.2 forbids editing
reviewed bytes, so every repair below is a new file and both predecessors are
untouched.

v2's three adjudicated repairs are KEPT AND NOT REOPENED: the AST direct-call
predicate (the `curl` false positive, re-derived exactly by a third independent
implementation), the undeclared-TOOL widening with declaration tested against
the Tool COLUMN rather than the section text, and the scoped named skip that
leaves five classes measuring when one per-class input is lost.  This file
repairs the two escapes the independent review found, and all nine of its
non-blocking observations -- two of them (NB-2, NB-3) closed in the half that
was reachable and carried into LIMITS as a NAMED residual for the half that was
not, rather than reported closed.

REPAIR 1 (BLOCKING) -- AN EXECUTED MODULE WAS PINNED BY A DIGEST SCRAPED FROM AN
UNPINNED DOCUMENT.

v2's `NPA-5` `exec(compile(...))`s a SECOND module -- the D9 oracle named by the
D9 contract's own `referenceDerivation` -- and gated that execution on whether
the module's live digest appeared among the 64-hex strings within +/-400
characters of its filename in `IMPLEMENTATION-FREEZE.md` or
`IMPLEMENTER-BLUEPRINT.md`.  Those two documents are NOT pinned, correctly and
deliberately, because they are the documents under comparison.  So the authority
to execute code was delegated to the surface the instrument exists to police.

  MEASURED ON v2's BYTES, BOTH STEPS EXECUTED AS REAL PROCESSES.
  Step 1: attacker-chosen bytes appended to the oracle, documents untouched ->
  exit 1, `NPA-5-ORACLE-SIGNATURE-UNRECORDED`, payload NOT executed.  That is
  the correct fail-closed direction and it is worth crediting.
  Step 2: the same hostile bytes, plus ONE digest string inserted into
  `IMPLEMENTER-BLUEPRINT.md` beside the module's name -> THE PAYLOAD EXECUTED,
  `NPA-5` raised nothing, and the run printed the full green banner at EXIT 0,
  including the line "every document claim above equals the measurement it
  describes."

  And v2's own docstring, under WHAT THIS FILE DOES NOT DO, states: "It pins
  exactly ONE file ... because it EXECUTES it."  It executes two.

  REPAIR.  There is now exactly ONE execution gate in this file --
  `load_pinned_module()` -- and it refuses any path that is not in
  `EXECUTED_PINS`, which is INTERNAL to these bytes.  Both executed modules are
  pinned there.  Drift becomes a NAMED, non-fatal skip of exactly the classes
  that needed the module, at exit 4, with the other classes still measuring:
  the shape this file already applied eleven hundred lines earlier to
  `check-package-coherence.py`, which it calls the most movable checker in the
  corpus and pins internally anyway.

  A pin whose value an attacker can write is not a pin; it is a lookup.  The
  digest the documents record near the oracle's name is still read -- but it is
  now a MEASUREMENT, compared against the internal pin and reported as
  `NPA-5-ORACLE-PIN-UNRECORDED` when they disagree.  It no longer authorises
  anything.  Freeze section 7.2.2's axis exactly: the document's digest is a
  recorded measurement and gets a hard comparison; the execution gate is an
  integrity boundary and gets a pin.  v2 used the recorded measurement AS the
  gate, which is the one combination that cannot work.

  AND THE LIST OF WHAT THIS FILE EXECUTES IS DERIVED FROM ITS OWN SOURCE, NOT
  TYPED.  `audit_execution_surface()` parses THIS file's bytes and finds every
  `exec` / `eval` / `compile` / `__import__` call, every `importlib` /
  `runpy` execution attribute, and any import of `runpy` or `subprocess`.  The
  audit requires every one of them to sit inside the single declared gate, and
  requires the gate to still contain the `compile` and `exec` sites it claims.
  A disagreement is a REFUSAL at exit 2 -- an instrument that cannot say what it
  executes must not certify anything -- and `--selftest` exercises it with a
  doctored copy of this file's own source.  The audit is printed in the banner
  on every run, so the published account of the execution surface is derived
  from the surface and cannot drift from it.

REPAIR 2 (THE TENTH LIMIT) -- DELETING A MENTION REMOVED COVERAGE INSTEAD OF
RAISING A FINDING.

`NPA-3` scopes its subjects to artifacts named in BOTH documents.  Measured on
v2: un-disclosing a REJECT in the freeze while leaving the name in both -> exit
1, one finding, correct.  ADDITIONALLY deleting the artifact's name from
`IMPLEMENTER-BLUEPRINT.md` -> EXIT 0, `subjectsGraded` 30 -> 29,
`subjectsRejected` 4 -> 3, ZERO findings.  Coverage was withdrawn by an edit and
nothing said so.

  THE DECISION, AND IT WAS MADE BY MEASUREMENT RATHER THAN PREFERENCE.  The
  obvious repair -- widen the class to "named by ANY document, checked in every
  document that names it" -- was BUILT AND RUN before it was rejected.  It costs
  TEN new findings on live bytes, and at least one of them is FALSE: it accuses
  `IMPLEMENTATION-FREEZE.md` of not disclosing that `retention-tiers.v26.json`
  is REJECTED, when the freeze block naming that artifact says, correctly, "what
  an independent review passed at 0 blockers -- verified".  The REJECT comes
  from `check-retention-custody-v26.review-independent.json`, a review whose
  SUBJECT is a checker and whose ruling is `ACCEPT_WITH_BLOCKERS`.  An
  oracle-free variant was then built -- one document attributes the REJECT on
  the same line, the other names the artifact and no block discloses it -- and
  it fires TWICE on live bytes, BOTH co-location false positives, which is
  `L-4`'s already-disclosed attribution weakness firing in the premise
  direction.  Publishing either set would be an instrument fabricating a
  specific, plausible accusation against a correct document: freeze section
  7.8.1's exact class, committed by the file written to close it.

  SO THE POPULATION IS RECORDED AND ITS WITHDRAWAL IS THE FINDING.  The set of
  REJECT-carrying artifacts both documents named at authoring is written into
  these bytes as a recorded measurement, and any member that is no longer in
  scope -- because an artifact vanished, or because a document stopped naming it
  -- raises `NPA-3-COVERAGE-WITHDRAWN`.  Growth is free and is published as a
  count; shrinkage is a finding.  That is freeze section 7.2.2's axis applied to
  a coverage figure: the population's growth is a continuing invariant and gets
  a semantic gate, its recorded members are a recorded measurement and get a
  hard comparison.  It is also the same shape as this file's own `NPA-2` --
  a record the live bytes no longer show is a FINDING, not a notice -- which is
  why a notice would have been inconsistent with the file's own vocabulary.

  AND EVERY POPULATION IS NOW PRINTED.  Freeze section 7.2.2's 2026-08-10
  sharpening records that a lane which does not publish how many rows it
  generated is making an uncheckable claim, and that a defect landed in exactly
  such a silence twice in one week.  The banner carries a POPULATIONS block: one
  row per class, saying what a row is and how many there were.  For `NPA-3` the
  REJECT-carrying corpus is partitioned FOUR ways -- named by both documents,
  by the freeze only, by the blueprint only, by neither -- the partition is
  hard-compared for exhaustiveness against a total DERIVED FROM DISK AND THE
  EXECUTED DERIVATION, which is a quantity neither document under comparison can
  write, and `--selftest` fails if the four cells do not sum to it.  That is
  freeze section 7.2.2's corollary: a partition must be bound to something the
  artifact does not supply.

  The 16 REJECT-carrying artifacts named by exactly one document are therefore
  PUBLISHED BY NAME and NOT GRADED, and that is stated as `L-10` rather than
  hidden.  A reader can see the exact size of what a green run does not cover.

ALSO REPAIRED, from the review's non-blocking set.

  `NB-1` A per-class input that PARSED but carried the wrong top-level shape
  escalated to a whole-run `NPA-INTERNAL-ERROR` at exit 2, so five classes that
  never needed the file stopped measuring.  `read_json_object()` now raises the
  same named `NPA-INPUT-MALFORMED` refusal a syntax error raises, at the tier
  the input belongs to.

  `NB-2` The widened call surface was incomplete in the direction a future
  author would reach for first.  `subprocess.call`, `getoutput`,
  `getstatusoutput`, `from os import system`, and the whole `os.exec*` /
  `os.spawn*` / `posix_spawn*` family are now covered, with the program-name
  argument index derived per API rather than assumed at 0.  MEASURED: the corpus
  census is BYTE-IDENTICAL before and after -- one dependent, `rg`, and the same
  four transitive dependents -- so the widening costs nothing today and closes
  the substitution.  v2's "STRICTLY WIDER in the directions that matter" is
  withdrawn as an overstatement about v2 and is now true of these bytes.

  `NB-3` is REPAIR 2 above.

  `NB-4` A negative control could be reduced to a no-op by a corpus edit, and a
  no-op negative control reports [SILENT] having tested nothing.  Every case in
  every suite now asserts that its overlay actually CHANGES the bytes it
  replaces; a no-op is reported `[NO-OP]` and fails the build.

  `NB-5` One fixture was keyed on the live identifier `P-1` and was dropped
  silently when it disappeared.  It is now DERIVED -- the first STATUS-graded
  table row `NPA-1` finds in `v1-slice.md` -- and its absence REFUSES the suite
  by name like its three siblings.  The `NPA-2` fabricated row is derived from
  the packet's own decided ids too, so no live corpus identifier is written into
  any predicate or fixture in this file.

  `NB-6` Two comments stated the suite's cost at 25 complete runs; it was 27.
  The figure is no longer written down: `run_check` counts its own invocations
  and the suite prints the measured number.

  `NB-7` The exit table claimed "only this code means finding" of exit 1, while
  `classify()` makes INCOMPLETE dominate and two measured runs exit 4 carrying
  real findings.  The behaviour is right; the sentence was wrong and is
  corrected below.

  `NB-8` This file's immunity to the transitive-closure filename heuristic was
  incidental -- its peer filenames happen to be preceded by `/` or a backtick
  rather than a quote.  `--selftest` now runs that exact heuristic over this
  file's own source and FAILS if it attributes a single execution edge here, so
  the immunity is asserted rather than lucky.

  `NB-9` v2's docstring inherited freeze section 7.8.1's overstatement of what
  the PREDECESSOR'S RUN emits.  The corrected shape, recorded in the freeze on
  2026-08-10 and reproduced independently: the three false
  `NPA-2-STALE-DISAGREEMENT-RECORD` findings are real AT THE `evaluate()` LAYER
  and UNREACHABLE AT PROCESS LEVEL, because `main()`'s banner re-reads the same
  paths with the same call and raises first, so all five reachable disk states
  give a traceback at exit 1 with zero findings printed.  The defect is
  undiminished and sharper than recorded: the predecessor is prevented from
  publishing its fabricated accusations only by a SECOND defect crashing first.
  A CRASH WAS LOAD-BEARING -- which is why the refusal was installed in the same
  act as the traceback was removed, never after.

  TWO RESIDUALS ARE CARRIED RATHER THAN CLOSED, and both are stated as limits
  rather than as repairs.  `NB-2`'s enumerated-API half is closed; the
  resolvability half is `L-6` and must stay open for the reason freeze section
  7.6 gives.  `NB-3`'s silence is closed; its scope half is `L-10`, and the
  measurement that decided it is published there rather than summarised.

WHAT THIS FILE DOES NOT DO, deliberately.

It does not pin `IMPLEMENTATION-FREEZE.md`, `IMPLEMENTER-BLUEPRINT.md` or
`v1-slice.md` by hash.  Those are the documents under comparison; pinning them
would make every legitimate edit a failure and would train the next author to
regenerate a pin instead of reading a diff.

IT EXECUTES TWO FILES, AND BOTH ARE PINNED INSIDE THESE BYTES.
`check-package-coherence.py`, because `NPA-3` measures whether the documents
disclose what THAT derivation finds and a second private copy of the rule could
disagree with `PC-7` invisibly; and the D9 oracle the D9 contract's own
`referenceDerivation` names, because `NPA-5` renders signatures from the live
module.  Freeze section 7.3 permits executing a verified closure and requires
the hash to hold BEFORE the bytes run.  The order for both is read, hash,
compare, then exec, through a single gate.  THE LIST ABOVE IS NOT THE AUTHORITY:
`EXECUTED_PINS` is, the gate refuses anything absent from it, and the AST audit
proves the gate is the only site.

It holds no opinion about wording, and none about whether a recorded
disagreement is ACCEPTABLE.  Freeze section 2's authority order settles that and
section 10 settles whether the narrative gets amended.  This measures AGREEMENT.

THE SIX CLASSES.

  NPA-1  UNRECORDED-PACKET-DISAGREEMENT
         An authority document presents, under a heading that declares its
         contents unresolved, a decision the binding product packet marks
         DECIDED or CONFIRMED -- and freeze section 5.1's disagreement register
         does not record it, or records it at the wrong grade.

  NPA-2  STALE-DISAGREEMENT-RECORD
         The register records a disagreement the live bytes no longer show.

  NPA-3  UNDISCLOSED-REJECT / COVERAGE-WITHDRAWN
         An artifact both package documents name, whose OWN independent review
         decides REJECT, is not disclosed together with that verdict in BOTH
         documents -- or a REJECT-carrying artifact this file RECORDED as graded
         has since left the graded population.

  NPA-4  UNDECLARED-EXTERNAL-TOOL / UNDECLARED-TOOL-DEPENDENT
         A checker needs an external binary -- directly, or through a checker
         whose bytes it compiles and executes -- and the blueprint's
         environment-prerequisites table does not DECLARE the binary, or the
         section does not NAME the dependent.

  NPA-5  ORACLE-SIGNATURE-UNRECORDED / ORACLE-PIN-UNRECORDED
         An export the D9 contract's own `referenceDerivation` names is not
         recorded in the blueprint at the call signature the live module
         exposes -- or the package documents no longer record the digest of the
         oracle this file pins and executes.

  NPA-6  IRREPRODUCIBLE-GOLDEN-UNRECORDED
         A `PLAN-ID-V1` golden vector whose own bytes omit some of the
         contract's declared preimage fields is not recorded in the blueprint at
         its measured completeness.

SCOPE OF THE FINDING SET, stated because it is a judgement and not a measurement.

Freeze section 2 ranks `architecture/` narrative LAST and admits it "only where
it does not conflict with the binding set".  `GORTEX-BORROW-REGISTER.md` carries
no product-disposition authority of its own.  Neither is a FINDING scope for
NPA-1; both are scanned and reported as OBSERVATIONS.  The finding scope is the
three documents that carry authority: the freeze, the blueprint, and
`v1-slice.md`.

LIMITS -- the freeze section 7.8 question, answered honestly and scoped.

The question is "can I make this checker pass on a wrong artifact?"  The answer
is YES, and the count is FIFTEEN, printed by `--limits` with a worked example
for each and SCOPED TO THE CLASS IT AFFECTS.  Of those, gated by an executed
selftest case: FIVE.  Both figures are compared to the data at `--selftest` and
disagreement fails the build.

v2 published EIGHT.  Its independent reviewer found a ninth and a tenth in
hours and wrote that eight "should be read as a FLOOR that is now known to be at
least ten, and nobody should read my two as the last two."  FIFTEEN is a floor
too.  SEVEN of these fifteen are new here; four of the seven were found by
building the repair that seemed obvious and MEASURING what it did rather than
shipping it, and one (`L-15`) was found by a process-level matrix run against
this file's own bytes.

Exit codes -- distinct, and this list is enforced by `--selftest`'s refusal
suite rather than asserted.

  0  the check RAN COMPLETELY and found nothing
  1  the check RAN COMPLETELY and found something
  2  REFUSED -- THE CHECK DID NOT RUN.  Bad invocation, a required input that
     cannot be read, parsed or shaped, this file's own execution-surface audit
     disagreeing with its own bytes, or an unforeseen internal error.  Never a
     finding
  3  `--selftest` did not execute its suite
  4  INCOMPLETE -- the check ran but at least one class was SKIPPED.  Every skip
     is named on stdout.  FINDINGS FROM THE CLASSES THAT DID RUN ARE PRINTED AND
     ARE REAL, SO EXIT 4 CARRIES FINDINGS TOO -- measured twice.  A CI rule of
     the form "exit 1 means findings" will miss them.  The rule that holds is:
     exit 0 means no findings; 1 and 4 both can carry them; 2 and 3 never do
"""

from __future__ import annotations

import ast
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
SELF_NAME = pathlib.Path(__file__).name
SELF_REL = "artifacts/" + SELF_NAME

FREEZE = "IMPLEMENTATION-FREEZE.md"
BLUEPRINT = "IMPLEMENTER-BLUEPRINT.md"
SLICE = "v1-slice.md"
PACKET = "artifacts/product-dispositions.v1.json"
D9_CONTRACT = "artifacts/d9-exit-contract.v1.14.json"
RESOLVED = "artifacts/resolved-inputs.v2.json"
PCM = "artifacts/check-package-coherence.py"
D9_ORACLE = "artifacts/check-d9-v1.14.py"

AUTHORITY_DOCS = (FREEZE, BLUEPRINT, SLICE)

# Required to run at all.  This file's OWN SOURCE is required too: the execution
# surface audit is derived from it, and an instrument that cannot derive what it
# executes must not certify anything.
REQUIRED_INPUTS = (SELF_REL, PACKET, FREEZE, BLUEPRINT)

# ---------------------------------------------------------------------------
# THE EXECUTION SURFACE.  This table is the AUTHORITY; the docstring above is a
# description of it, and `audit_execution_surface()` proves the description and
# the bytes agree.  Nothing outside this table is ever executed.
#
# Both digests were measured on the live tree at authoring, in this process's
# own words: read, hash, compare, then exec.  Neither is read from a document.
# ---------------------------------------------------------------------------
EXECUTED_PINS: dict[str, dict[str, str]] = {
    PCM: {
        "sha256": "8d56b5f56fed4fd031f4e9f602e63d4f90ac2a189e56b0b580498f20a107f2a6",
        "classes": "NPA-3",
        "skip": "NPA-3-NOT-RUN",
        "why": "NPA-3 measures whether the documents disclose what THAT "
               "derivation finds; a second private copy of the rule could "
               "disagree with PC-7 and neither instrument could see it",
    },
    D9_ORACLE: {
        "sha256": "513d69dd879dcb678d53d8df89a907d05dacd4b078ec43c7fedc939732c5e83e",
        "classes": "NPA-5",
        "skip": "NPA-5-NOT-RUN",
        "why": "NPA-5 renders each export's signature from the LIVE module, so "
               "the module must run; v2 gated that on a digest scraped from the "
               "unpinned documents under comparison, which is repair 1",
    },
}

# The single function permitted to contain an execution primitive.  Derived
# agreement with this name is enforced by `audit_execution_surface()`.
EXEC_GATE = "load_pinned_module"

# Builtins that execute a string or an object as code.
EXEC_CALL_NAMES = ("exec", "eval", "compile", "__import__")

# Attribute calls that construct or drive a module's execution.  `importlib`'s
# loader protocol is here in full because the protocol, not the builtin, is the
# route a future author is most likely to take.
EXEC_ATTR_NAMES = (
    "exec_module", "create_module", "module_from_spec", "spec_from_loader",
    "spec_from_file_location", "import_module", "load_module", "reload",
    "run_path", "run_module", "exec_dynamic",
)

# Importing either of these is itself an execution edge worth naming: `runpy`
# runs a file, and `subprocess` runs a binary.  This file imports neither, and
# the audit makes that a checked property rather than a claim.
EXEC_IMPORT_NAMES = ("runpy", "subprocess")

# ---------------------------------------------------------------------------
# NPA-3's RECORDED POPULATION -- a recorded measurement, gated by hard
# comparison, per freeze section 7.2.2.
#
# These are the REJECT-carrying artifacts that BOTH package documents named when
# this file was written, measured through the executed derivation below and not
# transcribed from any document.  A member that has LEFT the graded population
# is a finding.  A member that has JOINED it is not: growth is a continuing
# invariant and gets a semantic gate; the recorded members are a measurement and
# get a hard comparison.
#
# Recorded against IMPLEMENTATION-FREEZE.md
# 0b6af67df506cc9f5349e531822a668e7f3f7029445135bcdc5a177610033e0a and
# IMPLEMENTER-BLUEPRINT.md
# 93ea49a2622fdc12004027e7ff63ac8e878fc2ab3fb67edd395dc8badbc5f2f4.  Those two
# digests are CONTEXT, printed so a reader can see whether the documents have
# moved since.  They are NOT gates: pinning the documents under comparison is
# exactly what this file declines to do.
# ---------------------------------------------------------------------------
NPA_3_RECORDED_REJECT_POPULATION: tuple[str, ...] = (
    "c2-plan-stage-schema.v3.json",
    "retention-tiers.v25.json",
    "rust-provider-protocol.v2.json",
    "threat-model.v3.json",
)
NPA_3_RECORDED_AGAINST = {
    FREEZE: "0b6af67df506cc9f5349e531822a668e7f3f7029445135bcdc5a177610033e0a",
    BLUEPRINT: "93ea49a2622fdc12004027e7ff63ac8e878fc2ab3fb67edd395dc8badbc5f2f4",
}

UNRESOLVED_HEADING_TERMS = (
    r"remain(?:s|ing)? before freeze",
    r"open decision",
    r"undecided",
    r"pending decision",
    r"decisions that remain",
    r"not yet decided",
    r"remain open",
)
UNRESOLVED_HEADING = re.compile("|".join(UNRESOLVED_HEADING_TERMS), re.I)

NORMATIVE_MODAL = re.compile(
    r"\b(?:must not|must|shall not|shall|may not|"
    r"is required to|are required to|is to|are to)\b", re.I)

EDITORIAL_SUBJECT = re.compile(
    r"\b(?:reader|readers|note|notes|editor|editors|reviewer|reviewers|"
    r"author|authors|coordinator|coordinators|signer|signers|"
    r"implementer of this note|we|you|one)\s*$", re.I)

SUBJECT_WINDOW = 40

KIND_CONTENT = "CONTENT"
KIND_STATUS = "STATUS"

REGISTER_HEADING = re.compile(r"^#{2,4}\s*5\.1\b", re.M)
REGISTER_ROW = re.compile(
    r"^\|\s*`(?P<id>[A-Za-z0-9][A-Za-z0-9._-]*)`\s*"
    r"\|\s*`(?P<doc>[A-Za-z0-9][A-Za-z0-9._/-]*\.md)`\s*"
    r"\|[^|]*"
    r"\|\s*`(?P<kind>[A-Z-]+)`\s*\|",
    re.M,
)

ENV_HEADING = re.compile(r"^#{1,6}\s*.*environment prerequisites.*$", re.I | re.M)

INTERPRETER_ARGV0 = ("python3", "python", "sys.executable")

# NB-2.  `call`, `getoutput` and `getstatusoutput` are the APIs a future author
# reaches for and v2 did not carry.  Measured: adding them changes the live
# corpus census by nothing at all.
SUBPROCESS_CALLS = ("run", "Popen", "call", "check_output", "check_call",
                    "getoutput", "getstatusoutput")

# argv[0] is a SHELL COMMAND LINE for these -- the first word is the binary.
OS_SHELL_CALLS = ("system", "popen")

# The program name is a bare argument, and its INDEX differs by family:
# `exec*(file, args)` puts it first; `spawn*(mode, file, args)` puts it second.
# Derived per API rather than assumed, because assuming 0 silently reads a mode
# integer as a tool name.
OS_PROGRAM_CALLS = {
    "execv": 0, "execve": 0, "execl": 0, "execle": 0, "execlp": 0,
    "execlpe": 0, "execvp": 0, "execvpe": 0,
    "posix_spawn": 0, "posix_spawnp": 0,
    "spawnl": 1, "spawnle": 1, "spawnlp": 1, "spawnlpe": 1,
    "spawnv": 1, "spawnve": 1, "spawnvp": 1, "spawnvpe": 1,
}

EXTERNAL_CALL_TEXT = re.compile(
    r"subprocess\.(?:run|Popen|call|check_output|check_call)\(\s*\[\s*(['\"])([^'\"]+)\1")

REJECT_NEGATION = re.compile(
    r"(?:not|never|no longer|without|withdrawn|withdraw|withdraws|rather than|"
    r"instead of|avoids?|free of)\W{0,24}$", re.I)

CLOSURE_NEGATION = re.compile(
    r"(?:NOT|NEVER|NO LONGER|NOT YET|YET TO BE|AWAITING|BEFORE|UNTIL|"
    r"PENDING|WITHOUT|UNLESS|IF)\W{0,12}$")

HEX64 = re.compile(r"[0-9a-f]{64}")

TABLE_SEPARATOR_CELL = re.compile(r"^:?-{2,}:?$")
BACKTICKED = re.compile(r"`([^`]+)`")

# How far either side of a filename a recorded digest is looked for.  This is a
# MEASUREMENT window now, not an execution gate: v2's blocking defect was that
# whatever this window found was allowed to authorise `exec`.
DIGEST_WINDOW = 400


class Refusal(Exception):
    """A named refusal.  NEVER a finding, and never a bare traceback."""

    def __init__(self, token: str, subject: str, reason: str) -> None:
        super().__init__(f"{token} {subject}: {reason}")
        self.token = token
        self.subject = subject
        self.reason = reason


_DISK_BYTES: dict[str, bytes] = {}
_PINNED_MODULES: dict[str, Any] = {}
_REVIEW_STATE: dict[str, str] = {}
_SOURCE_FACTS: dict[tuple[str, str], tuple[set[str], bool, set[str]]] = {}

# NB-6.  v2 stated its suite's cost in two comments and both were stale by two.
# The figure is now measured instead of written down.
_RUN_CHECK_CALLS = 0


class Reader:
    """Every byte this checker reads passes through here."""

    def __init__(self, overlay: dict[str, Any] | None = None) -> None:
        self.overlay = dict(overlay or {})

    def read_bytes(self, rel: str) -> bytes:
        if rel in self.overlay:
            value = self.overlay[rel]
            if isinstance(value, BaseException):
                raise Refusal("NPA-INPUT-UNREADABLE", rel,
                              f"{type(value).__name__}: {value}")
            return value
        if rel in _DISK_BYTES:
            return _DISK_BYTES[rel]
        try:
            data = (COOP / rel).read_bytes()
        except OSError as exc:
            raise Refusal("NPA-INPUT-UNREADABLE", rel,
                          f"{type(exc).__name__}: {exc}") from None
        _DISK_BYTES[rel] = data
        return data

    def read_text(self, rel: str) -> str:
        data = self.read_bytes(rel)
        try:
            return data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise Refusal("NPA-INPUT-UNDECODABLE", rel, str(exc)) from None

    def read_json(self, rel: str) -> Any:
        text = self.read_text(rel)
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise Refusal("NPA-INPUT-MALFORMED", rel,
                          f"not valid JSON: {exc}") from None

    def read_json_object(self, rel: str) -> dict[str, Any]:
        """NB-1: a wrong top-level SHAPE refuses at the same tier a syntax error does.

        v2 converted `[]` into an `AttributeError` at the first `.get`, caught by
        `main`'s catch-all as `NPA-INTERNAL-ERROR` at exit 2 -- so a PER-CLASS
        input whose shape was wrong stopped five classes that never needed it.
        The direction was safe and the tier was wrong.
        """
        value = self.read_json(rel)
        if not isinstance(value, dict):
            raise Refusal("NPA-INPUT-MALFORMED", rel,
                          f"top-level JSON value is {type(value).__name__}, not an "
                          f"object, so no field this checker reads can exist on it")
        return value

    def digest(self, rel: str) -> str:
        return hashlib.sha256(self.read_bytes(rel)).hexdigest()


class Result:
    """What one run produced, including what it did NOT manage to do."""

    def __init__(self) -> None:
        self.findings: list[dict[str, str]] = []
        self.observations: list[str] = []
        self.skips: list[dict[str, str]] = []
        self.counts: dict[str, Any] = {}
        self.populations: list[tuple[str, str, Any]] = []
        self.executed: list[str] = []

    def add(self, fid: str, statement: str, detail: str) -> None:
        self.findings.append({"id": fid, "statement": statement, "detail": detail})

    def skip(self, classes: str, token: str, subject: str, reason: str) -> None:
        self.skips.append({"classes": classes, "token": token,
                           "subject": subject, "reason": reason})

    def population(self, lane: str, what: str, size: Any) -> None:
        """Publish how many rows a lane generated, and what a row IS.

        Freeze section 7.2.2, sharpened 2026-08-10: a lane that does not publish
        how many rows it generated is making an uncheckable claim, and a defect
        landed in exactly that silence twice in one week.
        """
        self.populations.append((lane, what, size))

    @property
    def ids(self) -> set[str]:
        return {f["id"] for f in self.findings}

    @property
    def fingerprints(self) -> set[str]:
        """(id, detail) pairs.  Finding-SET delta is the scoring unit here."""
        return {f"{f['id']}\x00{f['detail']}" for f in self.findings}

    @property
    def skipped_classes(self) -> set[str]:
        return {s["classes"] for s in self.skips}


EXIT_GREEN = 0
EXIT_FINDINGS = 1
EXIT_REFUSED = 2
EXIT_SELFTEST_NOT_RUN = 3
EXIT_INCOMPLETE = 4


def classify(result: Result) -> int:
    """Exit code from a completed run.  INCOMPLETE dominates FINDINGS."""
    if result.skips:
        return EXIT_INCOMPLETE
    return EXIT_FINDINGS if result.findings else EXIT_GREEN


# ---------------------------------------------------------------------------
# Text shaping -- freeze section 7.7: formatting is part of the bytes
# ---------------------------------------------------------------------------

def fold_markdown(text: str) -> str:
    """Collapse markdown structure so containment is not defeated by layout.

    Freeze section 7.7 measures this as "the sharpest false-negative generator
    in the package", and records that whitespace normalisation ALONE is
    insufficient -- the freeze's own most load-bearing sentence is a blockquote
    and stays invisible until the `>` markers are folded too.
    """
    out = []
    for line in text.splitlines():
        line = re.sub(r"^\s*>+\s?", " ", line)
        line = re.sub(r"^\s*(?:[-*+]|\d+\.)\s+", " ", line)
        line = line.replace("|", " ")
        line = re.sub(r"\\\s*$", " ", line)
        out.append(line)
    return re.sub(r"\s+", " ", " ".join(out))


def enclosing_block(text: str, start: int, end: int) -> str:
    """The paragraph or table row containing [start, end)."""
    left = text.rfind("\n\n", 0, start)
    left = 0 if left < 0 else left + 2
    right = text.find("\n\n", end)
    right = len(text) if right < 0 else right
    return text[left:right]


def enclosing_line(text: str, index: int) -> str:
    left = text.rfind("\n", 0, index)
    right = text.find("\n", index)
    return text[(0 if left < 0 else left + 1):(len(text) if right < 0 else right)]


def whole_token(ident: str) -> re.Pattern[str]:
    return re.compile(r"(?<![A-Za-z0-9_-])" + re.escape(ident) + r"(?![A-Za-z0-9_-])")


# ---------------------------------------------------------------------------
# THE EXECUTION SURFACE -- derived from this file's own bytes
# ---------------------------------------------------------------------------

def exec_edges(source: str) -> tuple[list[dict[str, str]], bool]:
    """(every execution primitive in `source`, with its enclosing scope), parsed_ok.

    DERIVED, NEVER TYPED.  The blocking defect this successor repairs was a
    second executed module whose existence the file's own published account of
    its execution surface denied.  A list of executed modules maintained by hand
    is exactly the list that goes stale the first time someone adds an `exec`,
    so the sites are read out of the AST and the declared gate is compared
    against them in both directions.

    Constants drop out for free: a string that merely SPELLS `exec(compile(` is
    not a `Call` node.  That is the same property repair 2 of the predecessor
    established for the external-tool census, reused here so that this file's
    own selftest probes cannot make it an instance of what it hunts.
    """
    try:
        tree = ast.parse(source)
    except (SyntaxError, ValueError):
        return [], False

    sites: list[dict[str, str]] = []

    def record(primitive: str, scope: str, line: int) -> None:
        sites.append({"primitive": primitive, "scope": scope, "line": str(line)})

    def visit(node: ast.AST, scope: str) -> None:
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                inner = child.name if scope == "<module>" else f"{scope}.{child.name}"
                visit(child, inner)
                continue
            if isinstance(child, ast.ClassDef):
                inner = child.name if scope == "<module>" else f"{scope}.{child.name}"
                visit(child, inner)
                continue
            if isinstance(child, ast.Call):
                func = child.func
                if isinstance(func, ast.Name) and func.id in EXEC_CALL_NAMES:
                    record(func.id, scope, child.lineno)
                elif isinstance(func, ast.Attribute) and func.attr in EXEC_ATTR_NAMES:
                    record(func.attr, scope, child.lineno)
            elif isinstance(child, ast.Import):
                for alias in child.names:
                    if alias.name.split(".")[0] in EXEC_IMPORT_NAMES:
                        record("import " + alias.name, scope, child.lineno)
            elif isinstance(child, ast.ImportFrom):
                root = (child.module or "").split(".")[0]
                if root in EXEC_IMPORT_NAMES:
                    record("from " + root, scope, child.lineno)
            visit(child, scope)

    visit(tree, "<module>")
    return sites, True


def audit_execution_surface(source: str) -> tuple[list[dict[str, str]], list[str]]:
    """(sites, problems).  A non-empty `problems` REFUSES the run.

    Two directions, because one alone is decorative.  Nothing outside the single
    declared gate may execute anything -- that is what makes `EXECUTED_PINS` the
    complete list.  And the gate must still CONTAIN the `compile` and `exec`
    sites it is declared to hold -- otherwise an audit could pass by describing
    a gate that had been emptied, which is freeze section 7.2.2's paper seal.
    """
    sites, parsed = exec_edges(source)
    problems: list[str] = []
    if not parsed:
        return [], ["this file's own source did not parse, so its execution "
                    "surface could not be derived and nothing here can be trusted "
                    "to be the only execution site"]
    for site in sites:
        if site["scope"] != EXEC_GATE:
            problems.append(
                f"`{site['primitive']}` at line {site['line']} sits in "
                f"{site['scope']}(), outside the single declared execution gate "
                f"{EXEC_GATE}()")
    inside = {s["primitive"] for s in sites if s["scope"] == EXEC_GATE}
    for want in ("compile", "exec"):
        if want not in inside:
            problems.append(
                f"the declared execution gate {EXEC_GATE}() no longer contains a "
                f"`{want}` site, so this audit is describing a gate that is not "
                f"there")
    return sites, problems


def load_pinned_module(rd: Reader, rel: str, name: str, res: Result | None = None) -> Any:
    """THE ONLY PLACE THIS FILE EXECUTES ANYTHING.  Hash-verify, then execute.

    Freeze section 7.3 requires the hash to hold BEFORE the bytes run.  The
    order is read, hash, compare, then exec, and the expected hash comes from
    `EXECUTED_PINS` inside these bytes.

    A PATH THAT IS NOT PINNED HERE IS NOT EXECUTED.  That is repair 1.  The
    predecessor derived the D9 oracle's expected digest from the two documents
    under comparison, neither of which it pins -- so inserting one string into
    `IMPLEMENTER-BLUEPRINT.md` beside the module's name was enough to make it
    execute attacker-chosen bytes and print a green banner.  A pin whose value
    the adversary can write is not a pin.

    The stated reason the predecessor gave for NOT pinning internally -- "a pin
    copied into this file would advance silently when the D9 head advances" --
    is sound for a RECORDED MEASUREMENT and wrong for an EXECUTION GATE, which
    is freeze section 7.2.2's axis.  Advance does not go unnoticed here: it
    produces a NAMED skip at exit 4 and the other classes keep measuring, which
    is the cost this file already accepts for the most movable checker in the
    corpus.
    """
    entry = EXECUTED_PINS.get(rel)
    if entry is None:
        raise Refusal(
            "NPA-EXEC-UNPINNED", rel,
            f"this file executes only modules pinned INSIDE its own bytes, and "
            f"this path is in none of them (pinned: {sorted(EXECUTED_PINS)}). A "
            f"digest read out of a document under comparison is not a pin, it is "
            f"a lookup: its value is writable by the surface this instrument "
            f"exists to police. If this module SHOULD be executed, a successor to "
            f"THIS file pins it; freeze section 7.2 forbids editing these bytes")
    data = rd.read_bytes(rel)
    actual = hashlib.sha256(data).hexdigest()
    expected = entry["sha256"]
    if actual == expected and actual in _PINNED_MODULES:
        # Keyed on the DIGEST, never on the path: a run whose overlay supplies
        # different bytes for this path cannot be served a module built from
        # other bytes, so the cache cannot weaken the gate below.
        if res is not None and rel not in res.executed:
            res.executed.append(rel)
        return _PINNED_MODULES[actual]
    if actual != expected:
        raise Refusal(
            "NPA-PIN-DRIFT", rel,
            f"live {actual} != pinned {expected}. This file EXECUTES that "
            f"module, so freeze section 7.3 requires the hash to hold before the "
            f"bytes run, and they were NOT run. If the drift is a deliberate "
            f"repair, a successor to THIS file re-pins it; freeze section 7.2 "
            f"forbids editing these bytes")
    module = importlib.util.module_from_spec(
        importlib.util.spec_from_loader(name, loader=None))
    module.__file__ = str(COOP / rel)
    try:
        exec(compile(data.decode("utf-8"), str(COOP / rel), "exec",
                     dont_inherit=True), module.__dict__)
    except Exception as exc:                                # noqa: BLE001
        raise Refusal("NPA-PIN-EXEC-FAILED", rel,
                      f"{type(exc).__name__}: {exc}") from None
    _PINNED_MODULES[actual] = module
    if res is not None and rel not in res.executed:
        res.executed.append(rel)
    return module


# ---------------------------------------------------------------------------
# Shared derivations -- carried from the predecessor unchanged in substance
# ---------------------------------------------------------------------------

def decided_ids(packet: Any) -> dict[str, str]:
    """Decision ids the packet has actually closed, with their chosen rule."""
    out: dict[str, str] = {}
    for key, value in (packet.get("decisions") or {}).items():
        if not isinstance(value, dict):
            continue
        if str(value.get("status", "")).strip().upper() in ("DECIDED", "CONFIRMED"):
            out[key] = str(value.get("rule", ""))
    return out


def closed_status_tokens(packet: Any) -> set[str]:
    """The packet's OWN vocabulary for "this is closed".  Derived, not transcribed."""
    tokens = set()
    for value in (packet.get("decisions") or {}).values():
        if isinstance(value, dict):
            status = str(value.get("status", "")).strip().upper()
            if status in ("DECIDED", "CONFIRMED"):
                tokens.add(status)
    return tokens or {"DECIDED", "CONFIRMED"}


def unresolved_sections(text: str) -> list[tuple[str, str]]:
    """(heading, body) for every section whose HEADING declares it unresolved."""
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


def binds_implementer(line: str) -> bool:
    """True if some normative modal on this line is NOT an editorial aside."""
    for m in NORMATIVE_MODAL.finditer(line):
        before = line[max(0, m.start() - SUBJECT_WINDOW):m.start()].rstrip()
        if not EDITORIAL_SUBJECT.search(before):
            return True
    return False


def records_closure(line: str, tokens: set[str]) -> bool:
    """True if this line RECORDS the decision as closed rather than open."""
    upper = line.upper()
    for token in tokens:
        for m in whole_token(token).finditer(upper):
            if not CLOSURE_NEGATION.search(upper[max(0, m.start() - 24):m.start()]):
                return True
    return False


def named_in(body: str, ident: str, closed_tokens: set[str]) -> list[str]:
    """Lines of `body` naming `ident` as a whole token and NOT recording closure."""
    pat = whole_token(ident)
    return [ln for ln in body.splitlines()
            if pat.search(ln) and not records_closure(ln, closed_tokens)]


def derive_disagreements(rd: Reader, decided: dict[str, str], docs: tuple[str, ...],
                         closed_tokens: set[str],
                         ) -> tuple[dict[tuple[str, str], dict[str, str]],
                                    dict[str, int], list[tuple[str, Refusal]]]:
    """({(id, doc): {kind, heading, line}}, {doc: headings matched}, refusals).

    A document that cannot be READ is returned as a refusal rather than skipped
    silently.  The FIRST predecessor swallowed the `OSError` here; the measured
    consequence at the `evaluate()` layer was three FALSE `NPA-2` findings
    blaming freeze section 5.1 for a document that was simply absent, and at
    PROCESS level a bare traceback, because its banner re-read the same paths
    and raised first.  A crash was load-bearing there: removing the traceback
    without installing this refusal would have made the accusations REACHABLE.
    """
    out: dict[tuple[str, str], dict[str, str]] = {}
    headings: dict[str, int] = {}
    refusals: list[tuple[str, Refusal]] = []
    for rel in docs:
        try:
            text = rd.read_text(rel)
        except Refusal as exc:
            refusals.append((rel, exc))
            continue
        sections = unresolved_sections(text)
        headings[rel] = len(sections)
        for heading, body in sections:
            for ident in sorted(decided):
                lines = named_in(body, ident, closed_tokens)
                if not lines:
                    continue
                kind = KIND_CONTENT if any(binds_implementer(ln) for ln in lines) \
                    else KIND_STATUS
                key = (ident, rel)
                if key not in out or kind == KIND_CONTENT:
                    out[key] = {
                        "kind": kind,
                        "heading": heading.strip(),
                        "line": max(lines, key=len).strip(),
                    }
    return out, headings, refusals


def parse_register(freeze_text: str) -> dict[tuple[str, str], str]:
    """{(decision id, document): KIND} from freeze section 5.1."""
    m = REGISTER_HEADING.search(freeze_text)
    if not m:
        return {}
    tail = freeze_text[m.end():]
    nxt = re.search(r"^#{1,4}\s", tail, re.M)
    section = tail[: nxt.start()] if nxt else tail
    return {(r.group("id"), r.group("doc")): r.group("kind")
            for r in REGISTER_ROW.finditer(section)}


def unnegated_reject(segment: str) -> bool:
    """True if a folded segment carries a REJECT token that is not negated."""
    folded = fold_markdown(segment)
    for hit in re.finditer(r"REJECT", folded):
        before = folded[max(0, hit.start() - 30):hit.start()]
        if not REJECT_NEGATION.search(before):
            return True
    return False


# ---------------------------------------------------------------------------
# NPA-4 derivations
# ---------------------------------------------------------------------------

def ast_direct_tools(source: str) -> tuple[set[str], bool]:
    """({external argv[0] literals invoked by this source}, parsed_ok).

    An AST match, not a text scan, and that distinction is the predecessor's
    adjudicated repair 2, kept here byte-for-byte in behaviour.  The regex
    matched a `curl` invocation's CHARACTERS wherever they occurred, including
    inside a module docstring describing another file and inside byte-string
    literals that are NEGATIVE PROBES asserting such code must be REFUSED.
    Constants are not `Call` nodes, so they drop out for free.

    WIDENED HERE (NB-2), and the widening was measured before it was kept: the
    corpus census is byte-identical with and without it -- the same one tool and
    the same four transitive dependents -- so nothing is gained today and the
    substitution a future author would reach for first is closed.  The program
    argument INDEX is derived per API: `exec*` puts the program first, `spawn*`
    puts a mode integer there and the program second, and assuming 0 for both
    would read a mode as a tool name.
    """
    try:
        tree = ast.parse(source)
    except (SyntaxError, ValueError):
        return set(), False

    sub_aliases = {"subprocess"}
    os_aliases = {"os"}
    bare: dict[str, tuple[str, int]] = {}
    calls: list[ast.Call] = []
    # ONE walk, not two: imports and candidate calls are collected together and
    # the calls classified afterwards, because the alias table must be complete
    # before any call is judged.
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            if node.args:
                calls.append(node)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == "subprocess":
                    sub_aliases.add(alias.asname or alias.name)
                elif alias.name == "os":
                    os_aliases.add(alias.asname or alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module == "subprocess":
                for alias in node.names:
                    if alias.name in SUBPROCESS_CALLS:
                        bare[alias.asname or alias.name] = ("argv", 0)
            elif node.module == "os":
                for alias in node.names:
                    if alias.name in OS_SHELL_CALLS:
                        bare[alias.asname or alias.name] = ("shell", 0)
                    elif alias.name in OS_PROGRAM_CALLS:
                        bare[alias.asname or alias.name] = (
                            "program", OS_PROGRAM_CALLS[alias.name])

    tools: set[str] = set()
    for node in calls:
        func = node.func
        kind: str | None = None
        index = 0
        if isinstance(func, ast.Attribute) and isinstance(func.value, ast.Name):
            if func.attr in SUBPROCESS_CALLS and func.value.id in sub_aliases:
                kind, index = "argv", 0
            elif func.attr in OS_SHELL_CALLS and func.value.id in os_aliases:
                kind, index = "shell", 0
            elif func.attr in OS_PROGRAM_CALLS and func.value.id in os_aliases:
                kind, index = "program", OS_PROGRAM_CALLS[func.attr]
        elif isinstance(func, ast.Name) and func.id in bare:
            kind, index = bare[func.id]
        if kind is None or index >= len(node.args):
            continue
        first = node.args[index]
        if isinstance(first, (ast.List, ast.Tuple)) and first.elts:
            head = first.elts[0]
            if isinstance(head, ast.Constant) and isinstance(head.value, str):
                tools.add(head.value)
        elif isinstance(first, ast.Constant) and isinstance(first.value, str):
            if kind == "program":
                # A bare program name, not a command line -- do not split it.
                tools.add(first.value)
            else:
                words = first.value.split()
                if words:
                    tools.add(words[0])
    return ({t for t in tools
             if t not in INTERPRETER_ARGV0 and "executable" not in t}, True)


def text_direct_tools(source: str) -> set[str]:
    """Conservative fallback for a source the AST cannot parse.  Over-reports."""
    tools = {m.group(2) for m in EXTERNAL_CALL_TEXT.finditer(source)}
    return {t for t in tools if t not in INTERPRETER_ARGV0 and "executable" not in t}


def closure_peers(source: str, fname: str, names: set[str]) -> set[str]:
    """Peer checkers whose bytes `source` compiles and executes.

    Factored out of the census (NB-8) so `--selftest` can run the SAME predicate
    over this file's own source and FAIL if it attributes an execution edge
    here.  The predecessor's immunity to this heuristic was incidental -- its
    peer filenames happen to sit behind a `/` or a backtick rather than a quote
    -- and an incidental property is one an ordinary edit removes.
    """
    if "exec_module" not in source and not re.search(r"\bexec\(\s*compile\(", source):
        return set()
    return {other for other in names
            if other != fname
            and re.search(r"['\"]" + re.escape(other) + r"['\"]", source)}


def external_tool_closure(sources: dict[str, str]
                          ) -> tuple[dict[str, set[str]], list[str]]:
    """({checker filename: external binaries it needs}, unparsed filenames).

    Transitive.  `check-rust-provider-protocol-v4.py` contains no `rg` call: it
    compiles and executes v3, which does the same to v2, which shells out.  A
    census that read only direct call sites would report one dependent where
    four exist -- exactly the understatement this class was written to catch.
    """
    direct: dict[str, set[str]] = {}
    executes: dict[str, set[str]] = {}
    unparsed: list[str] = []
    names = set(sources)
    names_key = hashlib.sha256("\0".join(sorted(names)).encode()).hexdigest()
    for fname, src in sources.items():
        cache_key = (hashlib.sha256(src.encode("utf-8", "replace")).hexdigest(),
                     names_key)
        if cache_key in _SOURCE_FACTS:
            tools, ok, peers = _SOURCE_FACTS[cache_key]
            direct[fname] = set(tools)
            executes[fname] = set(peers)
            if not ok:
                unparsed.append(fname)
            continue
        tools, ok = ast_direct_tools(src)
        if not ok:
            unparsed.append(fname)
            tools = text_direct_tools(src)
        direct[fname] = tools
        peers = closure_peers(src, fname, names)
        executes[fname] = peers
        _SOURCE_FACTS[cache_key] = (set(tools), ok, set(peers))

    def walk(fname: str, seen: frozenset[str]) -> set[str]:
        if fname in seen:
            return set()
        seen = seen | {fname}
        out = set(direct.get(fname, ()))
        for peer in executes.get(fname, ()):
            out |= walk(peer, seen)
        return out

    return {f: walk(f, frozenset()) for f in sources}, sorted(unparsed)


def env_section_of(blueprint_text: str) -> str:
    """The blueprint's environment-prerequisites section, or "" if it has none."""
    m = ENV_HEADING.search(blueprint_text)
    if not m:
        return ""
    tail = blueprint_text[m.end():]
    nxt = re.search(r"^#{1,6}\s", tail, re.M)
    return tail[: nxt.start()] if nxt else tail


def declared_tools(env_section: str) -> tuple[set[str], int]:
    """({tool names DECLARED in the section's tables}, declaration row count).

    A tool is DECLARED when it is named in the TOOL COLUMN of a table row, not
    when the section merely mentions it.  That distinction is the predecessor's
    adjudicated repair 3 and its counterfactual is load-bearing: `jq` occurs
    TWICE and `curl` THREE TIMES in this section's PROSE -- inside the very
    paragraphs describing them as instrument false positives -- so a containment
    test over the section would have ADMITTED the exact escape a reviewer proved
    could be added undetected.

    The tool column is located from the table's own header row rather than
    assumed at index 0.  If the table shape changes so that no header names a
    Tool column and no row parses, the declared set empties and every derived
    tool becomes a finding: over-reporting is the safe direction.
    """
    tools: set[str] = set()
    rows = 0
    lines = env_section.splitlines()
    tool_col = 0

    def cells(line: str) -> list[str]:
        return [c.strip() for c in line.strip().strip("|").split("|")]

    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped.startswith("|") or stripped.count("|") < 2:
            continue
        row = cells(line)
        if all(TABLE_SEPARATOR_CELL.match(c) for c in row if c):
            continue
        nxt = lines[i + 1].strip() if i + 1 < len(lines) else ""
        if nxt.startswith("|"):
            nxt_cells = cells(nxt)
            if nxt_cells and all(TABLE_SEPARATOR_CELL.match(c)
                                 for c in nxt_cells if c):
                for idx, cell in enumerate(row):
                    if "tool" in cell.replace("`", "").strip().lower():
                        tool_col = idx
                        break
                continue
        cell = row[tool_col] if tool_col < len(row) else row[0]
        found = {t.strip() for t in BACKTICKED.findall(cell) if t.strip()}
        if found:
            rows += 1
            tools |= found
    return tools, rows


# ---------------------------------------------------------------------------
# NPA-5 / NPA-6 helpers
# ---------------------------------------------------------------------------

def signature_literal(name: str, fn: Callable[..., Any]) -> str:
    params = ", ".join(inspect.signature(fn).parameters)
    return f"{name}({params})"


def resolve_dotted(module: Any, dotted: str) -> Any:
    obj: Any = module
    for part in dotted.split("."):
        obj = getattr(obj, part)
    return obj


def first_impl(node: Any) -> str:
    """The `<path>.py::<export>+...` string under a referenceDerivation."""
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


def find_reference_derivation(contract: Any) -> str:
    found = ""

    def walk(node: Any) -> None:
        nonlocal found
        if found:
            return
        if isinstance(node, dict):
            for key, value in node.items():
                if key == "referenceDerivation":
                    hit = first_impl(value)
                    if hit:
                        found = hit
                        return
                walk(value)
        elif isinstance(node, list):
            for value in node:
                walk(value)

    walk(contract)
    return found


def digests_recorded_near(texts: tuple[str, ...], filename: str) -> set[str]:
    """Every 64-hex string the documents write near `filename`.

    IN v2 THIS WAS THE EXECUTION GATE.  It is now a MEASUREMENT: what the
    package RECORDS about a module this file pins independently.  The two are
    hard-compared and a disagreement is `NPA-5-ORACLE-PIN-UNRECORDED`.
    """
    recorded: set[str] = set()
    for text in texts:
        for hit in re.finditer(re.escape(filename), text):
            window = text[max(0, hit.start() - DIGEST_WINDOW):
                          hit.start() + DIGEST_WINDOW]
            recorded |= set(HEX64.findall(window))
    return recorded


def preimage_container(vector: dict[str, Any], field_names: set[str]) -> dict[str, Any]:
    """The vector's own input map: the direct child sharing most preimage names."""
    best: dict[str, Any] = {}
    best_score = -1
    for value in vector.values():
        if isinstance(value, dict):
            score = len(field_names & set(value))
            if score > best_score:
                best, best_score = value, score
    return best


# ---------------------------------------------------------------------------
# The classes
# ---------------------------------------------------------------------------

def check_npa_1_2(rd: Reader, res: Result, packet: Any, freeze_text: str) -> None:
    decided = decided_ids(packet)
    closed_tokens = closed_status_tokens(packet)
    res.counts["packetDecided"] = len(decided)
    res.counts["packetPending"] = len(packet.get("pendingDecisions") or {})
    res.counts["packetClosedStatusTokens"] = sorted(closed_tokens)

    derived, headings, refusals = derive_disagreements(
        rd, decided, AUTHORITY_DOCS, closed_tokens)
    register = parse_register(freeze_text)

    unread = {rel for rel, _ in refusals}
    for rel, exc in refusals:
        res.skip(f"NPA-1/NPA-2 over {rel}", exc.token, exc.subject, exc.reason)

    res.counts["authorityDocsScanned"] = len(AUTHORITY_DOCS) - len(unread)
    res.counts["unresolvedHeadingsMatched"] = {d: headings.get(d, 0)
                                               for d in AUTHORITY_DOCS}
    res.counts["disagreementsDerived"] = len(derived)
    res.counts["disagreementsRecorded"] = len(register)

    scanned = len(AUTHORITY_DOCS) - len(unread)
    res.population(
        "NPA-1/NPA-2",
        "(decided packet id x authority document) pairs examined; a row is one "
        "pair tested for a naming under an unresolved-declaring heading",
        f"{len(decided)} x {scanned} = {len(decided) * scanned}  "
        f"(derived {len(derived)}, recorded {len(register)})")

    for key in sorted(derived):
        ident, doc = key
        info = derived[key]
        if key not in register:
            res.add("NPA-1-UNRECORDED-PACKET-DISAGREEMENT",
                    "an authority document presents a decided packet row as "
                    "unresolved, and freeze section 5.1 does not record the "
                    "disagreement",
                    f"{doc} — heading {info['heading']!r} names `{ident}`, which "
                    f"product-dispositions.v1.json#decisions.{ident} marks decided "
                    f"(grade {info['kind']}); no section 5.1 register row for "
                    f"(`{ident}`, `{doc}`). Line: {info['line'][:180]!r}")
        elif register[key] != info["kind"]:
            res.add("NPA-1-UNRECORDED-PACKET-DISAGREEMENT",
                    "freeze section 5.1 records a disagreement at a grade the live "
                    "bytes no longer support",
                    f"(`{ident}`, `{doc}`): register says {register[key]}, "
                    f"measured {info['kind']} — the recorded line is "
                    f"{info['line'][:180]!r}")

    for key in sorted(register):
        ident, doc = key
        if key in derived:
            continue
        if doc in unread:
            # The document could not be read.  Saying its record is stale would
            # be a measurement of nothing presented as a verdict.
            continue
        if headings.get(doc, 0) == 0:
            diagnosis = (
                f"{doc} matched ZERO unresolved-declaring headings this run. If "
                f"its heading was reworded, this instrument's heading vocabulary "
                f"{list(UNRESOLVED_HEADING_TERMS)} may no longer reach the section "
                f"— check that before withdrawing the record")
        else:
            diagnosis = (
                f"{doc} has {headings.get(doc, 0)} unresolved-declaring heading(s) "
                f"and none of them names `{ident}`, or the packet no longer marks "
                f"`{ident}` decided")
        res.add("NPA-2-STALE-DISAGREEMENT-RECORD",
                "freeze section 5.1 records a disagreement the live bytes do not show",
                f"(`{ident}`, `{doc}`): {diagnosis}. A repaired contradiction must "
                f"have its record withdrawn, not left standing")

    narrative = sorted(
        str(p.relative_to(COOP))
        for p in list(COOP.glob("*.md")) + list((COOP / "architecture").glob("*.md"))
        if str(p.relative_to(COOP)) not in AUTHORITY_DOCS
    )
    narrative_hits, _, _ = derive_disagreements(
        rd, decided, tuple(narrative), closed_tokens)
    res.counts["narrativeDocsScanned"] = len(narrative)
    for key, info in sorted(narrative_hits.items()):
        res.observations.append(
            f"{key[1]}: names decided `{key[0]}` under {info['heading']!r} "
            f"(grade {info['kind']}) — narrative, ranked last by freeze section 2 "
            f"and pre-resolved by the authority order; recorded here, not raised")


def check_npa_3(rd: Reader, res: Result, freeze_text: str, blueprint_text: str) -> None:
    try:
        pcm = load_pinned_module(rd, PCM, "npa3_pcm", res)
    except Refusal as exc:
        res.skip("NPA-3", exc.token, exc.subject, exc.reason)
        for key in ("subjectsGraded", "subjectsRejected", "rejectSubjectsInCorpus"):
            res.counts[key] = None
        res.population("NPA-3", "REJECT-carrying artifacts graded", "NOT RUN")
        return

    def review_state(path: pathlib.Path) -> str:
        # Memoised because the executed derivation reads the review corpus from
        # DISK, not through the overlay -- so its answer cannot vary between
        # selftest cases, and recomputing it once per case only costs time.
        key = str(path)
        if key not in _REVIEW_STATE:
            _REVIEW_STATE[key] = pcm.review_state_of(path)
        return _REVIEW_STATE[key]

    # THE POPULATION, derived from DISK and the EXECUTED derivation -- a total
    # neither document under comparison can write.  Freeze section 7.2.2's
    # corollary: a registry sized from the artifact cannot police that artifact,
    # so a partition must be bound to something the artifact does not supply.
    candidates = [p for p in sorted(ARTIFACTS.glob("*.json"))
                  if not any(mark in p.name.lower() for mark in pcm.REVIEW_MARKERS)]
    rejects = [p for p in candidates if review_state(p) == "REJECT"]

    both, freeze_only, blueprint_only, neither = [], [], [], []
    for p in rejects:
        in_f = p.name in freeze_text
        in_b = p.name in blueprint_text
        (both if (in_f and in_b) else
         freeze_only if in_f else
         blueprint_only if in_b else neither).append(p)

    res.counts["rejectSubjectsInCorpus"] = len(rejects)
    res.counts["rejectSubjectsNamedByBothDocs"] = [p.name for p in both]
    res.counts["rejectSubjectsNamedByFreezeOnly"] = [p.name for p in freeze_only]
    res.counts["rejectSubjectsNamedByBlueprintOnly"] = [p.name for p in blueprint_only]
    res.counts["rejectSubjectsNamedByNeither"] = len(neither)
    partition_sum = len(both) + len(freeze_only) + len(blueprint_only) + len(neither)
    res.counts["rejectPartitionExhaustive"] = (partition_sum == len(rejects))

    subjects = [p for p in candidates
                if p.name in freeze_text and p.name in blueprint_text]
    res.counts["subjectsGraded"] = len(subjects)
    res.counts["subjectsRejected"] = len(both)
    # Published because a reader wants to know WHICH artifacts carry a REJECT,
    # and because `--selftest` derives its NPA-3 fixtures from this list rather
    # than naming an artifact in its own source.
    res.counts["subjectsRejectedNames"] = [p.name for p in both]

    res.population(
        "NPA-3 (disclosure)",
        "(REJECT-carrying artifact x naming document) pairs graded; a row is one "
        "artifact's REJECT tested for disclosure in one document",
        f"{len(both)} x 2 = {len(both) * 2} graded, out of "
        f"{len(rejects)} REJECT-carrying artifacts in the corpus "
        f"({len(freeze_only) + len(blueprint_only)} named by exactly one document "
        f"and NOT graded — see --limits L-10; {len(neither)} named by neither)")
    res.population(
        "NPA-3 (coverage)",
        "recorded population members re-tested for continued membership; a row "
        "is one artifact this file RECORDED as graded at authoring",
        f"{len(NPA_3_RECORDED_REJECT_POPULATION)} recorded, {len(both)} live")

    # ----- COVERAGE: the recorded population, hard-compared ------------------
    # Freeze section 7.2.2's axis.  The recorded members are a MEASUREMENT and
    # get a hard comparison in the shrinking direction; growth is a continuing
    # INVARIANT and gets a semantic gate, i.e. nothing but a published count.
    live_reject_names = {p.name for p in both}
    all_names = {p.name for p in candidates}
    for name in NPA_3_RECORDED_REJECT_POPULATION:
        if name in live_reject_names:
            continue
        if name not in all_names:
            why = (f"no artifacts/{name} on disk (or its name now matches a review "
                   f"marker, which removes it from the candidate set)")
        elif name not in freeze_text and name not in blueprint_text:
            why = "neither package document names it any more"
        elif name not in freeze_text:
            why = f"{FREEZE} no longer names it, so this class no longer grades it"
        elif name not in blueprint_text:
            why = f"{BLUEPRINT} no longer names it, so this class no longer grades it"
        else:
            why = ("both documents still name it, but the executed review-state "
                   "derivation no longer decides REJECT for it")
        res.add("NPA-3-COVERAGE-WITHDRAWN",
                "an artifact this instrument RECORDED as a graded REJECT subject "
                "has left the graded population, so coverage shrank without a "
                "notice",
                f"{name}: {why}. Deleting a mention is not a repair — freeze "
                f"section 2 rule 3 still forbids implementing a REJECTED version, "
                f"and a reader of the document that still names it still cannot "
                f"know. If the withdrawal is deliberate, a successor to THIS file "
                f"re-records the population; freeze section 7.2 forbids editing "
                f"these bytes. Recorded population "
                f"{list(NPA_3_RECORDED_REJECT_POPULATION)}, live "
                f"{sorted(live_reject_names)}")

    joined = sorted(live_reject_names - set(NPA_3_RECORDED_REJECT_POPULATION))
    res.counts["rejectPopulationJoinedSinceRecord"] = joined
    for name in joined:
        res.observations.append(
            f"NPA-3 coverage GREW: {name} is a REJECT-carrying subject both "
            f"documents now name and this file's recorded population predates. "
            f"Growth is graded, not raised — the recorded set is a floor")

    # ----- DISCLOSURE, unchanged in definition and in finding set ------------
    tight: dict[str, int] = {}
    for path in both:
        stem = path.name[: -len(".json")]
        for doc, text in ((FREEZE, freeze_text), (BLUEPRINT, blueprint_text)):
            disclosed = False
            same_line = 0
            for m in re.finditer(re.escape(stem), text):
                if unnegated_reject(enclosing_block(text, m.start(), m.end())):
                    disclosed = True
                if re.search(r"REJECT", enclosing_line(text, m.start())):
                    same_line += 1
            tight[f"{stem}@{doc}"] = same_line
            if not disclosed:
                res.add("NPA-3-UNDISCLOSED-REJECT",
                        "an artifact both documents name carries a REJECT on its own "
                        "bytes and one of them does not disclose it",
                        f"{path.name}: independent review decides REJECT; {doc} names "
                        f"it and no block containing its name carries an unnegated "
                        f"REJECT. Freeze section 2 rule 3 forbids implementing a "
                        f"REJECTED version, so a reader of that document alone "
                        f"cannot know")
    res.counts["rejectDisclosureSameLine"] = tight


def check_npa_4(rd: Reader, res: Result, blueprint_text: str) -> None:
    sources: dict[str, str] = {}
    unreadable: list[str] = []
    for path in sorted(ARTIFACTS.glob("check-*.py")):
        if path.name == SELF_NAME:
            # Self-excluded, as both predecessors were.  What makes it harmless
            # is a PROPERTY, not an intention: this file imports no `subprocess`
            # and invokes no external binary, and its own execution-surface
            # audit refuses the run if that ever stops being true.  The
            # exclusion therefore removes nothing measurable -- it only avoids
            # reporting this instrument's own selftest fixtures as corpus
            # dependencies.  `--selftest` additionally runs the peer heuristic
            # over these bytes and fails if it attributes an edge here (NB-8).
            continue
        try:
            sources[path.name] = rd.read_text(f"artifacts/{path.name}")
        except Refusal as exc:
            unreadable.append(f"{path.name} ({exc.token})")
    closure, unparsed = external_tool_closure(sources)

    env_section = env_section_of(blueprint_text)

    dependents = {f: t for f, t in closure.items() if t}
    tools = sorted({t for ts in dependents.values() for t in ts})
    declared, declaration_rows = declared_tools(env_section)

    res.counts["checkersScanned"] = len(sources)
    res.counts["checkersUnparsed"] = unparsed
    res.counts["checkersUnreadable"] = unreadable
    res.counts["externalToolDependents"] = {f: sorted(t)
                                            for f, t in sorted(dependents.items())}
    res.counts["externalTools"] = tools
    res.counts["toolsDeclaredInEnvTable"] = sorted(declared)
    res.counts["envDeclarationRows"] = declaration_rows
    res.population(
        "NPA-4",
        "checker sources parsed for a direct or transitive external-binary call; "
        "a row is one checker",
        f"{len(sources)} scanned, {len(dependents)} dependents, {len(tools)} "
        f"distinct tools, {len(declared)} names declared across "
        f"{declaration_rows} table row(s)")

    if unreadable:
        res.skip("NPA-4 over unreadable checker sources", "NPA-INPUT-UNREADABLE",
                 ", ".join(unreadable),
                 "a checker whose bytes cannot be read cannot be scanned for "
                 "external-tool calls, so this census is incomplete")

    if dependents and not env_section:
        # Explanatory, and deliberately NOT a short circuit.  Deleting the
        # section makes BOTH limbs' facts true at once, so reporting one of them
        # and returning would understate the damage by exactly the other limb.
        res.add("NPA-4-UNDECLARED-EXTERNAL-TOOL",
                "the blueprint has no environment-prerequisites section to declare in",
                f"{len(dependents)} checker(s) need an external binary and no heading "
                f"matching 'environment prerequisites' exists in {BLUEPRINT}; derived "
                f"tools {tools}. Every tool below is undeclared and every dependent "
                f"below is unnamed, because there is nowhere for either to be stated")

    for tool in tools:
        if tool not in declared:
            needs = sorted(f for f, t in dependents.items() if tool in t)
            res.add("NPA-4-UNDECLARED-EXTERNAL-TOOL",
                    "a checker needs an external binary the blueprint's "
                    "environment-prerequisites table does not DECLARE",
                    f"`{tool}` is required by {needs} (directly or through a checker "
                    f"whose bytes they execute) and is named in no Tool column of "
                    f"that section's table(s); declared there today: "
                    f"{sorted(declared)}. Without the binary those checkers abort "
                    f"before evaluating any contract property, so their exit 1 "
                    f"measures nothing and must not be read as a finding. A mention "
                    f"in the section's prose is not a declaration")

    for fname in sorted(dependents):
        if fname not in env_section:
            res.add("NPA-4-UNDECLARED-TOOL-DEPENDENT",
                    "a checker that needs an external binary is not named in the "
                    "blueprint's environment-prerequisites section",
                    f"{fname} requires {sorted(dependents[fname])} (directly or "
                    f"through a checker whose bytes it executes) and does not appear "
                    f"in that section, so a signer who meets its unaccounted exit "
                    f"cannot tell that the guard never ran")


def check_npa_5(rd: Reader, res: Result, freeze_text: str, blueprint_text: str) -> None:
    try:
        contract = rd.read_json_object(D9_CONTRACT)
    except Refusal as exc:
        res.skip("NPA-5", exc.token, exc.subject, exc.reason)
        res.counts["oracleExports"] = None
        res.population("NPA-5", "oracle exports whose signature is compared", "NOT RUN")
        return

    ref = find_reference_derivation(contract)
    res.counts["oracleExports"] = 0
    if not ref or "::" not in ref:
        res.add("NPA-5-ORACLE-SIGNATURE-UNRECORDED",
                "the D9 contract no longer names a reference derivation",
                f"{D9_CONTRACT}: no `referenceDerivation` of the form "
                f"`artifacts/<checker>.py::<export>+<export>...` was found, so the "
                f"blueprint's port instruction has no subject to be checked against")
        res.population("NPA-5", "oracle exports whose signature is compared", 0)
        return

    mod_rel, exports = ref.split("::", 1)
    mod_rel = mod_rel.strip()
    names = [n.strip() for n in exports.split("+") if n.strip()]
    res.counts["oracleExports"] = len(names)
    res.counts["oracleModule"] = mod_rel

    # THE MEASUREMENT.  What the package documents record near the oracle's
    # name, compared against the pin these bytes hold.  In v2 this SET WAS THE
    # EXECUTION GATE, and inserting one string into the unpinned blueprint was
    # enough to execute attacker-chosen bytes at exit 0.  It is now a claim
    # about the documents and authorises nothing.
    recorded = digests_recorded_near((freeze_text, blueprint_text),
                                     pathlib.PurePosixPath(mod_rel).name)
    res.counts["oracleDigestsRecordedInDocs"] = sorted(recorded)
    entry = EXECUTED_PINS.get(mod_rel)
    res.counts["oraclePinnedHere"] = entry["sha256"] if entry else None
    if entry is not None and entry["sha256"] not in recorded:
        res.add("NPA-5-ORACLE-PIN-UNRECORDED",
                "the package documents do not record the digest of the D9 oracle "
                "this instrument pins and executes",
                f"{mod_rel}: pinned here {entry['sha256']}, recorded near its name "
                f"in the two package documents {sorted(recorded)}. One of the two "
                f"is wrong and a reader cannot tell which from the documents alone. "
                f"This is a claim about the documents; it is NOT the execution "
                f"gate, which is the internal pin")

    try:
        module = load_pinned_module(rd, mod_rel, "npa5_d9", res)
    except Refusal as exc:
        res.skip("NPA-5", exc.token, exc.subject,
                 f"{exc.reason}. The oracle's bytes were NOT executed, so no "
                 f"signature was rendered and NPA-5 measured nothing")
        res.population("NPA-5", "oracle exports whose signature is compared",
                       "NOT RUN")
        return

    compared = 0
    for name in names:
        try:
            fn = resolve_dotted(module, name)
        except AttributeError:
            res.add("NPA-5-ORACLE-SIGNATURE-UNRECORDED",
                    "the D9 contract names an export the oracle does not have",
                    f"{mod_rel}: `{name}` is named by referenceDerivation and does "
                    f"not resolve on the executed module")
            continue
        if not callable(fn):
            continue
        try:
            literal = signature_literal(name, fn)
        except (TypeError, ValueError) as exc:
            res.skip("NPA-5 signature of " + name, "NPA-SIGNATURE-UNAVAILABLE",
                     f"{mod_rel}::{name}", f"{type(exc).__name__}: {exc}")
            continue
        compared += 1
        if literal not in blueprint_text:
            res.add("NPA-5-ORACLE-SIGNATURE-UNRECORDED",
                    "the blueprint tells an implementer to drive an oracle export "
                    "without recording the arity it actually has",
                    f"`{literal}` is the live signature and does not appear in "
                    f"{BLUEPRINT}. Driving it as the instruction reads raises "
                    f"TypeError before any golden is compared")
    res.population(
        "NPA-5",
        "exports named by the contract's own referenceDerivation whose LIVE "
        "signature is rendered and compared to the blueprint; a row is one export",
        f"{compared} compared of {len(names)} named")


def check_npa_6(rd: Reader, res: Result, blueprint_text: str) -> None:
    try:
        resolved = rd.read_json_object(RESOLVED)
    except Refusal as exc:
        res.skip("NPA-6", exc.token, exc.subject, exc.reason)
        res.counts["preimageFields"] = None
        res.counts["goldenVectors"] = None
        res.population("NPA-6", "golden vectors whose completeness is recomputed",
                       "NOT RUN")
        return

    plan = resolved.get("planIdContract") or {}
    if not isinstance(plan, dict):
        plan = {}
    field_names = {f.get("name") for f in (plan.get("preimageFields") or [])
                   if isinstance(f, dict)}
    field_names.discard(None)
    vectors = ((plan.get("goldenVectors") or {}).get("positive") or [])
    res.counts["preimageFields"] = len(field_names)
    res.counts["goldenVectors"] = len(vectors)
    res.population(
        "NPA-6",
        "positive PLAN-ID-V1 golden vectors whose preimage completeness is "
        "recomputed and hard-compared to the blueprint; a row is one vector",
        f"{len(vectors)} vectors against {len(field_names)} declared preimage fields")

    for vector in vectors:
        if not isinstance(vector, dict):
            continue
        vid = str(vector.get("id") or "")
        container = preimage_container(vector, field_names)
        have = len(field_names & set(container))
        total = len(field_names)
        literal = f"`{vid}` carries {have} of {total} `PLAN-ID-V1` preimage fields"
        stale = re.search(
            r"`" + re.escape(vid) + r"` carries (\d+) of (\d+) `PLAN-ID-V1` "
            r"preimage fields", blueprint_text)
        if have < total and literal not in blueprint_text:
            res.add("NPA-6-IRREPRODUCIBLE-GOLDEN-UNRECORDED",
                    "a PLAN-ID-V1 golden vector is not independently reproducible "
                    "from its own bytes and the blueprint does not record that",
                    f"`{vid}`: {have} of {total} preimage fields present; missing "
                    f"{sorted(field_names - set(container))}. Reproducing it needs an "
                    f"unstated cross-artifact join, so it is not evidence the recipe "
                    f"is re-derivable from the package. Expected literal in "
                    f"{BLUEPRINT}: {literal!r}")
        elif stale and (int(stale.group(1)), int(stale.group(2))) != (have, total):
            res.add("NPA-6-IRREPRODUCIBLE-GOLDEN-UNRECORDED",
                    "the blueprint records a golden vector's completeness at a figure "
                    "the live artifact contradicts",
                    f"`{vid}`: blueprint says {stale.group(1)} of {stale.group(2)}, "
                    f"measured {have} of {total}")


def run_check(rd: Reader) -> Result:
    """Run every class.  Raises `Refusal` only for a REQUIRED input.

    THE EXECUTION-SURFACE AUDIT RUNS FIRST, before anything is executed.  An
    instrument that cannot derive which modules it executes is in no position to
    certify a package, so a disagreement between its own AST and its own
    declared gate is a REFUSAL at exit 2, not a finding and not a skip.
    """
    global _RUN_CHECK_CALLS
    _RUN_CHECK_CALLS += 1

    res = Result()
    self_source = rd.read_text(SELF_REL)
    sites, problems = audit_execution_surface(self_source)
    if problems:
        raise Refusal(
            "NPA-EXEC-AUDIT-DISAGREES", SELF_REL,
            "this file's DERIVED execution surface disagrees with its DECLARED "
            "one: " + "; ".join(problems) + ". The declared surface is "
            f"EXECUTED_PINS {sorted(EXECUTED_PINS)}, reached only through "
            f"{EXEC_GATE}(). Nothing was executed and nothing was measured")
    res.counts["execAuditSites"] = [
        f"{s['primitive']} @ {s['scope']}:{s['line']}" for s in sites]
    res.counts["execAuditGate"] = EXEC_GATE
    res.counts["execModulesPinned"] = sorted(EXECUTED_PINS)

    packet = rd.read_json_object(PACKET)
    freeze_text = rd.read_text(FREEZE)
    blueprint_text = rd.read_text(BLUEPRINT)

    check_npa_1_2(rd, res, packet, freeze_text)
    check_npa_3(rd, res, freeze_text, blueprint_text)
    check_npa_4(rd, res, blueprint_text)
    check_npa_5(rd, res, freeze_text, blueprint_text)
    check_npa_6(rd, res, blueprint_text)

    res.counts["modulesExecutedThisRun"] = sorted(res.executed)
    return res


# ---------------------------------------------------------------------------
# LIMITS -- freeze section 7.8, answered with a count, worked examples, and
# which of them a selftest case actually EXECUTES
# ---------------------------------------------------------------------------

LIMITS: tuple[dict[str, str], ...] = (
    {
        "id": "L-1",
        "lane": "NPA-1 (unrecorded disagreements only)",
        "limit": "the heading vocabulary is 7 alternatives and is exhaustive of "
                 "nothing",
        "worked": "Head a genuinely contradicting section 'Unsettled questions' "
                  "rather than 'Open decisions'. Independently re-measured against "
                  "v2 with a matched control: 7 of 7 out-of-vocabulary heading "
                  "rewrites produce 3 NPA-2 findings each, never silence, so a "
                  "RECORDED disagreement is rescued; a NEW disagreement under an "
                  "unknown heading is invisible at exit 0.",
        "why": "NOT CLOSED, and not claimed to be. Symmetry cannot rescue a "
               "disagreement that was never recorded: nothing goes stale, so it is "
               "invisible in both directions. The vocabulary and the per-document "
               "match counts are printed on every run so the gap is legible.",
        "gate": "reword the live unresolved heading",
    },
    {
        "id": "L-2",
        "lane": "NPA-1 (grade only, not existence)",
        "limit": "a genuine binding written without any of the eight modal forms "
                 "grades STATUS instead of CONTENT",
        "worked": "Write 'CI execution follows RI-LAYER4-CI-PROVISIONAL until "
                  "superseded' -- an imperative with no modal. The disagreement is "
                  "still FOUND and still compared to the register; only its grade "
                  "is understated.",
        "why": "Bounded by design: this limb can understate severity, never hide a "
               "disagreement.",
        "gate": "",
    },
    {
        "id": "L-3",
        "lane": "NPA-1 (polarity exclusion)",
        "limit": "a line that names one of the packet's closed-status tokens is "
                 "treated as recording the closure, so appending 'DECIDED' to an "
                 "otherwise contradicting line removes it from the derived set",
        "worked": "'`A1-RI-04` — DECIDED elsewhere, but an implementation must fail "
                  "admission until superseded' drops out of the derived set.",
        "why": "The price of repairing the reproduced polarity false positive, paid "
               "asymmetrically: for a RECORDED disagreement the row's disappearance "
               "raises NPA-2, so the evasion converts one finding into another "
               "rather than into silence. For an UNRECORDED one it is the same gap "
               "as L-1.",
        "gate": "NEGATED closed-status token",
    },
    {
        "id": "L-4",
        "lane": "NPA-3 (disclosure attribution)",
        "limit": "attribution WITHIN a block is not established -- a block naming "
                 "artifact X that separately reports artifact Y as REJECTED "
                 "satisfies the test for X",
        "worked": "Measured live: a freeze block naming `rust-provider-protocol.v2` "
                  "discloses via a sentence about a DIFFERENT checker being 'REJECT "
                  "FOR REPAIR'. Independently re-measured on that artifact in that "
                  "document: 6 of its 11 REJECT-carrying blocks disclose on the same "
                  "LINE as its name, 5 only somewhere in the block, and the banner "
                  "publishes that same figure on every run.",
        "why": "Narrowed, not closed, and MEASURED AT ITS LIMIT while building this "
               "successor: the same weakness defeats the oracle-free repair for "
               "NB-3 in the PREMISE direction, manufacturing 2 false accusations on "
               "live bytes (see L-10). The banner publishes rejectDisclosureSameLine "
               "so a reader can see how much disclosure is attributed rather than "
               "merely co-located.",
        "gate": "negate the disclosure",
    },
    {
        "id": "L-5",
        "lane": "NPA-4 (tool declaration)",
        "limit": "any backticked token in a Tool column counts as a declared tool",
        "worked": "The live table's Tool cell contains `PATH`, so a checker "
                  "invoking a binary literally named `PATH` would be admitted.",
        "why": "Accepted. The alternative -- a curated list of what may appear in a "
               "Tool cell -- is a transcription this instrument would then be "
               "testing instead of the document.",
        "gate": "",
    },
    {
        "id": "L-6",
        "lane": "NPA-4 (static reachability)",
        "limit": "a tool invoked through a name the AST cannot resolve to a literal "
                 "argv[0] is invisible",
        "worked": "`subprocess.run([TOOL_NAME, ...])` where `TOOL_NAME` is a module "
                  "constant, or an argv list built at runtime, or `importlib` used "
                  "in place of `exec(compile(...))` for the closure edge.",
        "why": "Structural, and it is freeze section 7.6's shape: a property true "
               "only at execution time is invisible to a static reader. The same "
               "fact is why the `rg` edge on check-rust-provider-protocol-v5 is "
               "correctly REPORTED and correctly NOT repaired -- the edge is real "
               "and only runtime substitution of a stand-in module makes it inert. "
               "NB-2's enumerated-API half is closed here; this resolvability half "
               "cannot be.",
        "gate": "",
    },
    {
        "id": "L-7",
        "lane": "NPA-5 / NPA-6 (recorded-figure classes)",
        "limit": "these bind the ARITY and the COUNT, not the truth of the prose "
                 "around them",
        "worked": "Keep `derive_codes(axes, maps)` correct and write beside it 'this "
                  "export takes one argument'. Both classes stay green.",
        "why": "Freeze section 7.8's measured boundary: an instrument can bind any "
               "prose that asserts a MEASUREMENT by re-deriving it, and nothing "
               "binds prose that asserts a JUDGEMENT.",
        "gate": "",
    },
    {
        "id": "L-8",
        "lane": "the whole instrument",
        "limit": "it measures AGREEMENT between two statements of the same facts, "
                 "and holds no opinion about whether either is right",
        "worked": "Amend freeze section 5.1 to record a disagreement AND amend "
                  "`v1-slice.md` to contain it. Green, and the corpus still "
                  "contradicts the binding packet at authority level 2.",
        "why": "Freeze section 7.8's bound: a companion instrument converts an "
               "unverifiable attestation into a re-runnable check and converts "
               "neither into independent evidence.",
        "gate": "",
    },
    {
        "id": "L-9",
        "lane": "NPA-3 / NPA-5 (the internal execution pins -- NEW)",
        "limit": "both executed modules are pinned inside these bytes, so a "
                 "LEGITIMATE advance of either stops its class rather than "
                 "following it",
        "worked": "Publish a repaired `check-package-coherence.py`, or advance the "
                  "D9 head so the contract's referenceDerivation names a successor "
                  "oracle. The class is SKIPPED by name, the run exits 4, and the "
                  "other classes keep measuring until a successor to this file "
                  "re-pins.",
        "why": "The deliberate cost of repair 1, and the correct trade: v2 avoided "
               "it by taking the oracle's digest from the unpinned documents, which "
               "is how one inserted string bought arbitrary code execution at a "
               "green exit 0. An advance that is announced by name at exit 4 is the "
               "failure mode freeze section 7.10 asks for; silent following is not.",
        "gate": "executed pin drifted",
    },
    {
        "id": "L-10",
        "lane": "NPA-3 (finding scope -- NEW)",
        "limit": "a REJECT-carrying artifact named by EXACTLY ONE package document "
                 "is published and NOT graded, so its undisclosed REJECT raises "
                 "nothing",
        "worked": "16 such artifacts exist today and every one is printed by name "
                  "in the banner. Six are named only by the freeze and undisclosed "
                  "there; four only by the blueprint and undisclosed there.",
        "why": "NOT CLOSED, and the reason is a MEASUREMENT rather than a "
               "preference. Widening the class to the union costs 10 findings and "
               "at least one is FALSE -- it accuses the freeze of hiding that "
               "`retention-tiers.v26.json` is REJECTED, where the REJECT comes from "
               "a review whose SUBJECT is a checker, at ACCEPT_WITH_BLOCKERS, and "
               "the freeze block says correctly that an independent review passed "
               "it at 0 blockers. An oracle-free variant fires twice and both are "
               "L-4 co-location false positives. An instrument that fabricates a "
               "plausible accusation against a correct document is freeze section "
               "7.8.1's class. What IS closed is the silence: the population is "
               "published, the partition is exhaustive against a disk-derived "
               "total, and withdrawal from the graded set is a finding (L-11).",
        "gate": "",
    },
    {
        "id": "L-11",
        "lane": "NPA-3 (recorded population -- NEW)",
        "limit": "the recorded REJECT population is a measurement taken at "
                 "authoring, so a LEGITIMATE document edit that drops one of those "
                 "four names raises NPA-3-COVERAGE-WITHDRAWN",
        "worked": "Delete every mention of a recorded subject from "
                  "`IMPLEMENTER-BLUEPRINT.md` as part of an honest cleanup: exit 1, "
                  "one finding, and the remedy is a successor to this file rather "
                  "than an edit to it.",
        "why": "Accepted deliberately. Freeze section 7.2.2: an uncompared "
               "measurement is prose that looks like evidence, and going stale is a "
               "TRUE POSITIVE about these bytes. The alternative -- a notice that "
               "cannot fail the build -- is the same section's rider, and it is "
               "what let deleting a mention buy silence in v2. The surface is "
               "deliberately the four REJECT-carrying members rather than all 30 "
               "graded subjects, which covers 100% of the hazard freeze section 2 "
               "rule 3 names at 13% of the staleness surface.",
        "gate": "COVERAGE-WITHDRAWN",
    },
    {
        "id": "L-12",
        "lane": "NPA-3 (the executed oracle -- NEW)",
        "limit": "every NPA-3 verdict rests on a review-state derivation this file "
                 "EXECUTES and does not audit, and that derivation is measured to "
                 "mis-attribute at least one subject",
        "worked": "`retention-tiers.v26.json` scores REJECT because "
                  "`check-retention-custody-v26.review-independent.json` -- a review "
                  "of a CHECKER, ruling ACCEPT_WITH_BLOCKERS -- names it. If "
                  "`review_state_of` is wrong for a subject inside the graded "
                  "population, NPA-3 is wrong with it and nothing here would see it.",
        "why": "Structural and deliberate: executing the derivation rather than "
               "reimplementing it is what keeps NPA-3 measuring the SAME rule PC-7 "
               "measures, and a second private copy could disagree with it "
               "invisibly. The independent review of v2 recorded the same gap in "
               "its own whatIDidNotCheck. Disclosed, bounded, not closed.",
        "gate": "",
    },
    {
        "id": "L-13",
        "lane": "the execution-surface audit (NEW)",
        "limit": "the audit binds THIS file's static surface only; a module this "
                 "file executes may execute further modules under its own rules",
        "worked": "`check-d9-v1.14.py` carries its own `exec(compile(...))` and "
                  "`importlib` loader machinery. Its bytes are pinned here, so what "
                  "it can do is fixed -- but it is fixed by ITS pin, not audited by "
                  "this one, and its own execution decisions are not derived here.",
        "why": "Honest bound rather than a repair. Auditing transitively would mean "
               "auditing every module in a closure this file does not own, and the "
               "pin already fixes the bytes. Stated so that 'this file executes two "
               "modules' is not read as 'exactly two modules run'.",
        "gate": "",
    },
    {
        "id": "L-14",
        "lane": "the execution-surface audit (NEW)",
        "limit": "the audit is STATIC, so an execution primitive reached through a "
                 "name it cannot resolve is invisible to it",
        "worked": "`getattr(__builtins__, 'e' + 'xec')(...)` or an execution "
                  "primitive fetched out of a dict. The declared gate would still "
                  "look like the only site.",
        "why": "L-6's shape one level in, and it is why the audit is a NECESSARY "
               "condition rather than a sufficient one. The load-bearing guard is "
               "not the audit but `load_pinned_module`'s refusal of any path absent "
               "from EXECUTED_PINS: a hidden primitive would still have to obtain "
               "bytes, and every path this file reads is named here.",
        "gate": "",
    },
    {
        "id": "L-15",
        "lane": "the execution-surface audit (NEW)",
        "limit": "the audit derives its answer from the bytes that are RUNNING, so "
                 "it proves the declared gate is the only site in THIS file -- it "
                 "cannot prove that this file is the file anyone reviewed",
        "worked": "Found by measurement at process level while testing this "
                  "successor: replacing these bytes on disk means the interpreter "
                  "loads the replacement and the audit reads the replacement, which "
                  "agrees with itself. An edit that adds an execution site AND "
                  "updates EXECUTED_PINS and the gate together passes the audit.",
        "why": "Honest bound, and the correct division of labour rather than a hole "
               "to plug. Freeze section 7.2 binds a verdict to BYTES, so what "
               "protects these bytes is a reviewer recording their digest and the "
               "corpus comparing it -- not a self-check, which can only ever attest "
               "to whatever is running. Recorded because a reader could otherwise "
               "take the printed audit as an integrity guarantee ABOUT this file "
               "rather than a consistency guarantee WITHIN it. A self-pinning "
               "variant was considered and rejected: freeze section 7.6 measures "
               "that a self-pinned checker cannot be repaired in place at all, and "
               "this file exists as a successor precisely because that is the "
               "lawful route.",
        "gate": "",
    },
)


_NUMBER_WORDS = {
    "ZERO": 0, "ONE": 1, "TWO": 2, "THREE": 3, "FOUR": 4, "FIVE": 5, "SIX": 6,
    "SEVEN": 7, "EIGHT": 8, "NINE": 9, "TEN": 10, "ELEVEN": 11, "TWELVE": 12,
    "THIRTEEN": 13, "FOURTEEN": 14, "FIFTEEN": 15, "SIXTEEN": 16,
    "SEVENTEEN": 17, "EIGHTEEN": 18, "NINETEEN": 19, "TWENTY": 20,
}


def gated_limits() -> tuple[dict[str, str], ...]:
    return tuple(lim for lim in LIMITS if lim.get("gate"))


def limits_count_disagreement() -> list[str]:
    """Every disagreement between the docstring's published figures and the data.

    Freeze section 7.2.2's rider: a measurement that cannot fail the build is
    prose.  This module's docstring publishes TWO counts -- how many ways it can
    be made to pass on a wrong package, and how many of those an executed
    selftest case exercises -- and a count written in prose beside a list is
    exactly the figure that goes stale the first time the list is extended.
    """
    # Whitespace-folded before matching, and NOT optionally.  Freeze section 7.7
    # calls line wrapping "the sharpest false-negative generator in the package",
    # and this gate reproduced it against ITSELF on first run: the docstring wraps
    # between "executed" and "selftest case", so a byte-literal search reported
    # the figure ABSENT and the build failed on a document that was correct.
    doc = re.sub(r"\s+", " ", __doc__ or "")
    problems: list[str] = []
    for pattern, actual, what in (
            (r"the count is ([A-Z]+)", len(LIMITS), "len(LIMITS)"),
            (r"gated by an executed selftest case: ([A-Z]+)", len(gated_limits()),
             "the number of LIMITS rows carrying a gate"),
    ):
        m = re.search(pattern, doc)
        if not m:
            problems.append(f"the module docstring no longer publishes a figure "
                            f"matching /{pattern}/, so nothing can be compared to "
                            f"{what}")
            continue
        word = m.group(1)
        if word not in _NUMBER_WORDS:
            problems.append(f"the docstring publishes an unreadable figure {word!r} "
                            f"for {what}")
        elif _NUMBER_WORDS[word] != actual:
            problems.append(f"the docstring publishes {word} "
                            f"({_NUMBER_WORDS[word]}) for {what}, which is {actual}")
    return problems


def print_limits() -> None:
    gated = gated_limits()
    print("LIMITS -- can I make this checker pass on a wrong artifact?")
    print(f"  YES, {len(LIMITS)} ways. Each is scoped to the lane it describes;")
    print("  none is printed under a heading broader than the class it affects.")
    print(f"  {len(gated)} of the {len(LIMITS)} are GATED by an executed selftest")
    print("  case, named on each row. The rest are disclosed and unexercised.")
    print("  This count is a FLOOR. v2 published EIGHT and an independent reviewer")
    print("  found a ninth and a tenth in hours.")
    print()
    for lim in LIMITS:
        print(f"  {lim['id']}  [{lim['lane']}]")
        print(f"      limit:  {lim['limit']}")
        print(f"      worked: {lim['worked']}")
        print(f"      status: {lim['why']}")
        print(f"      gate:   {lim['gate'] or 'UNGATED -- disclosed, not exercised'}")
        print()


# ---------------------------------------------------------------------------
# Non-vacuity: every class must be shown to fire, from outside itself
# ---------------------------------------------------------------------------

def overlay_is_noop(rd: Reader, overlay: dict[str, Any]) -> bool:
    """True if this overlay replaces every byte it touches with itself.

    NB-4.  A negative control whose mutation matched nothing reported [SILENT]
    having tested nothing, and the published count still said 3 of 3 silent.
    The asymmetry is the interesting part: POSITIVE cases are fail-safe, because
    a no-op produces no finding and is reported as an escape. Only NEGATIVE
    controls are exposed, because for them silence is the pass condition and a
    no-op is indistinguishable from a genuine non-firing. Every case in every
    suite is now checked, because the cost is one comparison.
    """
    touched = 0
    for rel, value in overlay.items():
        if isinstance(value, BaseException):
            return False
        try:
            original = rd.read_bytes(rel)
        except Refusal:
            return False
        if value != original:
            return False
        touched += 1
    return touched > 0


def selftest() -> int:
    """Mutation suite, negative controls, and the hostile-input matrix.

    Freeze section 7.8's harder standard is "for every assertion, exhibit an
    input that is WRONG rather than merely EMPTY".  Scoring is by FINDING-SET
    DELTA against the base run, not by the presence of an id: a case passes only
    if it produces a finding the base did not have.  That is strictly stronger
    than the predecessor's test and it keeps working if the base ever stops
    being green, which the predecessor's could not.
    """
    global _RUN_CHECK_CALLS
    _RUN_CHECK_CALLS = 0
    try:
        base = run_check(Reader())
    except Refusal as exc:
        print(f"SELFTEST-REFUSED: base run refused -- {exc.token} {exc.subject}: "
              f"{exc.reason}")
        print("  The mutation suite DID NOT RUN. This is not a finding.")
        return EXIT_SELFTEST_NOT_RUN
    if base.skips:
        print("SELFTEST-REFUSED: base run is INCOMPLETE, so a class that never ran "
              "cannot be distinguished from a class that ran and found nothing")
        for s in base.skips:
            print(f"  {s['token']} [{s['classes']}] {s['subject']}: {s['reason']}")
        return EXIT_SELFTEST_NOT_RUN

    base_fp = base.fingerprints
    rd0 = Reader()
    freeze_text = rd0.read_text(FREEZE)
    blueprint_text = rd0.read_text(BLUEPRINT)
    slice_text = rd0.read_text(SLICE)
    self_source = rd0.read_text(SELF_REL)

    register_marker = REGISTER_ROW.search(freeze_text)
    if register_marker is None:
        print("SELFTEST-NOT-RUN: no section 5.1 register row to mutate")
        return EXIT_SELFTEST_NOT_RUN
    env = ENV_HEADING.search(blueprint_text)
    if env is None:
        print("SELFTEST-NOT-RUN: no environment-prerequisites heading to mutate")
        return EXIT_SELFTEST_NOT_RUN
    slice_sections = unresolved_sections(slice_text)
    if not slice_sections:
        print(f"SELFTEST-NOT-RUN: {SLICE} has no unresolved-declaring heading to "
              f"mutate, so the NPA-1/NPA-2 cases have no subject")
        return EXIT_SELFTEST_NOT_RUN
    live_heading = slice_sections[0][0]

    # Every fixture below is DERIVED from the live corpus.  Freeze section 7.8.1
    # records the reason in one sentence: an instrument that hard-codes an
    # example of what it hunts becomes an instance of it, and v2's first draft
    # did exactly that twice.  NB-5 found the one place v2 had not applied the
    # rule -- a fixture keyed on the live identifier `P-1`, silently dropped when
    # it disappeared -- so that one is derived here too.
    packet = rd0.read_json_object(PACKET)
    decided = decided_ids(packet)
    closed_tokens = closed_status_tokens(packet)
    register = parse_register(freeze_text)

    fabricated_id = next((i for i in sorted(decided)
                          if (i, BLUEPRINT) not in register), "")
    if not fabricated_id:
        print(f"SELFTEST-NOT-RUN: every decided packet id already has a section 5.1 "
              f"register row for {BLUEPRINT}, so no fabricated row can be derived "
              f"that would be stale by construction")
        return EXIT_SELFTEST_NOT_RUN
    bogus_row = (f"| `{fabricated_id}` | `{BLUEPRINT}` | section 0 | `STATUS` | "
                 f"fabricated | x | x |\n")

    slice_derived, _, _ = derive_disagreements(rd0, decided, (SLICE,), closed_tokens)
    status_row = next((info["line"] for key, info in sorted(slice_derived.items())
                       if info["kind"] == KIND_STATUS
                       and info["line"].strip().startswith("|")), "")
    if not status_row:
        print(f"SELFTEST-NOT-RUN: NPA-1 derives no STATUS-graded TABLE ROW from "
              f"{SLICE}, so the incidental-modal negative control has no subject. "
              f"(NB-5: this guard exists because the predecessor dropped the same "
              f"fixture silently when its subject disappeared)")
        return EXIT_SELFTEST_NOT_RUN
    status_row_line = next((ln for ln in slice_text.splitlines()
                            if ln.strip() == status_row), "")
    if not status_row_line:
        print(f"SELFTEST-NOT-RUN: the derived STATUS row could not be located "
              f"verbatim in {SLICE}")
        return EXIT_SELFTEST_NOT_RUN

    env_section = env_section_of(blueprint_text)
    env_named = [p.name for p in sorted(ARTIFACTS.glob("check-*.py"))
                 if p.name != SELF_NAME and p.name in env_section]
    if not env_named:
        print(f"SELFTEST-NOT-RUN: no checker filename appears in {BLUEPRINT}'s "
              f"environment-prerequisites section, so the undeclared-tool case has "
              f"no subject that satisfies its precondition")
        return EXIT_SELFTEST_NOT_RUN
    tool_source = env_named[-1]
    try:
        tool_text = rd0.read_text(f"artifacts/{tool_source}")
    except Refusal as exc:
        print(f"SELFTEST-NOT-RUN: the derived undeclared-tool subject is unreadable "
              f"-- {exc.token} {exc.subject}: {exc.reason}")
        return EXIT_SELFTEST_NOT_RUN

    reject_names = base.counts.get("subjectsRejectedNames") or []
    reject_stem = next((n[: -len(".json")] for n in reject_names
                        if n[: -len(".json")] in blueprint_text), "")
    if not reject_stem:
        print(f"SELFTEST-NOT-RUN: NPA-3 derived no REJECT subject named in "
              f"{BLUEPRINT}, so the disclosure-polarity case has no subject")
        return EXIT_SELFTEST_NOT_RUN

    withdraw_name = next((n for n in NPA_3_RECORDED_REJECT_POPULATION
                          if n in blueprint_text), "")
    if not withdraw_name:
        print(f"SELFTEST-NOT-RUN: no member of this file's recorded REJECT "
              f"population is named in {BLUEPRINT} today, so the coverage-withdrawal "
              f"case has no subject. That state is itself an NPA-3-COVERAGE-WITHDRAWN "
              f"finding on a normal run")
        return EXIT_SELFTEST_NOT_RUN

    oracle_name = pathlib.PurePosixPath(D9_ORACLE).name
    oracle_pin = EXECUTED_PINS[D9_ORACLE]["sha256"]
    if oracle_name not in blueprint_text:
        print(f"SELFTEST-NOT-RUN: {BLUEPRINT} does not name {oracle_name}, so the "
              f"forged-digest case cannot forge a digest beside its name")
        return EXIT_SELFTEST_NOT_RUN
    try:
        oracle_bytes = rd0.read_bytes(D9_ORACLE)
    except Refusal as exc:
        print(f"SELFTEST-NOT-RUN: the pinned D9 oracle is unreadable -- "
              f"{exc.token} {exc.subject}: {exc.reason}")
        return EXIT_SELFTEST_NOT_RUN
    good_pcm = rd0.read_bytes(PCM)

    # The hostile oracle raises when EXECUTED, and does nothing when merely read.
    # That is what makes "the payload did not run" observable in memory: if the
    # bytes reached `exec`, the run reports NPA-PIN-EXEC-FAILED; if the gate held
    # first, it reports NPA-PIN-DRIFT and never the other.  Assembled from
    # fragments for the reason NB-8 and freeze section 7.8.1 both name.
    hostile_oracle = oracle_bytes + ("\n_NPA_V3_PAYLOAD = 1 " + "/" + " 0\n").encode()
    forged_digest = hashlib.sha256(hostile_oracle).hexdigest()
    cut = blueprint_text.find(oracle_name) + len(oracle_name)
    forged_blueprint = (blueprint_text[:cut] + " " + forged_digest
                        + blueprint_text[cut:])

    # A doctored copy of THIS file's own source, carrying one execution
    # primitive OUTSIDE the declared gate.  Built by transforming the live
    # source rather than by writing a second file, so the probe cannot go stale
    # against these bytes -- and spelled in fragments so that no text-scanning
    # census anywhere in the corpus reads it as a call site.
    doctored_self = self_source + (
        "\n_NPA_AUDIT_PROBE = " + "com" + "pile('1', '<probe>', 'eval')\n")
    unparseable_self = self_source + "\ndef (\n"

    # ----- POSITIVE cases: (expected finding id, label, overlay) --------------
    positives: list[tuple[str, str, dict[str, Any]]] = []

    positives.append((
        "NPA-1-UNRECORDED-PACKET-DISAGREEMENT",
        "EMPTY: delete the section 5.1 register heading",
        {FREEZE: freeze_text.replace("### 5.1", "### 5.1x", 1).encode()},
    ))
    positives.append((
        "NPA-1-UNRECORDED-PACKET-DISAGREEMENT",
        "CORRUPT: downgrade a CONTENT register row to STATUS",
        {FREEZE: freeze_text.replace("| `CONTENT` |", "| `STATUS` |", 1).encode()},
    ))
    positives.append((
        "NPA-2-STALE-DISAGREEMENT-RECORD",
        "WRONG: add a register row for a disagreement that does not exist "
        "(the id is DERIVED from the packet's own decided set, not named here)",
        {FREEZE: freeze_text.replace(
            register_marker.group(0),
            register_marker.group(0) + "\n" + bogus_row, 1).encode()},
    ))
    positives.append((
        "NPA-2-STALE-DISAGREEMENT-RECORD",
        "WRONG: reword the live unresolved heading out of the vocabulary "
        "(L-1's own evasion -- symmetry must convert it into findings, not silence)",
        {SLICE: slice_text.replace(live_heading, "Unsettled questions", 1).encode()},
    ))
    positives.append((
        "NPA-1-UNRECORDED-PACKET-DISAGREEMENT",
        "WRONG: a genuinely binding, genuinely unrecorded new row under the LIVE "
        "heading, written with a NEGATED closed-status token ('is not yet decided') "
        "-- the phrasing the polarity repair would delete if its negation guard "
        "were removed",
        {SLICE: slice_text.replace(
            live_heading,
            live_heading + "\n\n| `G3-SUBSTRATE` | is not yet decided; until it is, "
            "an implementation must build against the interim posture | owner |\n",
            1).encode()},
    ))
    positives.append((
        "NPA-3-UNDISCLOSED-REJECT",
        "EMPTY: strip every REJECT token from the blueprint",
        {BLUEPRINT: blueprint_text.replace("REJECT", "PASSED").encode()},
    ))
    positives.append((
        "NPA-3-UNDISCLOSED-REJECT",
        "WRONG: keep every REJECT token but negate the disclosure "
        "(freeze 7.8's containment-monotonicity attack)",
        {BLUEPRINT: re.sub(r"(?<![A-Za-z])REJECT", "not REJECT",
                           blueprint_text).encode()},
    ))
    positives.append((
        "NPA-3-COVERAGE-WITHDRAWN",
        "WRONG: delete a RECORDED REJECT subject's name from the blueprint -- the "
        "tenth limit. On v2 this took the run from exit 1 to EXIT 0 with zero "
        "findings and subjectsGraded 30 -> 29; coverage must not be withdrawable "
        "by an edit",
        {BLUEPRINT: blueprint_text.replace(withdraw_name,
                                           withdraw_name[:-5] + " artifact").encode()},
    ))
    positives.append((
        "NPA-4-UNDECLARED-TOOL-DEPENDENT",
        "EMPTY: rename the environment-prerequisites heading",
        {BLUEPRINT: (blueprint_text[: env.start()] + "#### Notes\n"
                     + blueprint_text[env.end():]).encode()},
    ))
    # The probe sources below are ASSEMBLED from fragments rather than written
    # as literals, and the reason is MEASURED rather than stylistic: a
    # text-scanning external-tool census reads raw source and cannot tell a call
    # from a string that merely looks like one. Written verbatim, these probes
    # make every such census attribute a `jq` dependency to THIS file -- measured
    # on the FIRST predecessor, which went exit 0 -> exit 1 reporting a phantom
    # dependency sourced entirely from this file's test data.
    probe_tool = "jq"
    sp_call = "subprocess" + ".run"
    sp_call2 = "subprocess" + ".call"
    os_call = "os" + ".system"

    positives.append((
        "NPA-4-UNDECLARED-EXTERNAL-TOOL",
        "WRONG: add a real undeclared external-tool call to a checker whose "
        "FILENAME is already declared (the reviewer's jq demonstration -- the "
        "first predecessor stayed green here)",
        {f"artifacts/{tool_source}": (
            "import subprocess\n"
            f"_PROBE = {sp_call}(['{probe_tool}', '-r', '.x'])\n"
            + tool_text).encode()},
    ))
    positives.append((
        "NPA-4-UNDECLARED-EXTERNAL-TOOL",
        "WRONG: the same call through an ALIASED import, invisible to the first "
        "predecessor's text predicate",
        {f"artifacts/{tool_source}": (
            "import subprocess as _sp\n"
            f"_PROBE = _sp.run(['{probe_tool}', '-r', '.x'])\n"
            + tool_text).encode()},
    ))
    positives.append((
        "NPA-4-UNDECLARED-EXTERNAL-TOOL",
        "WRONG: the same call through a shell-string invocation",
        {f"artifacts/{tool_source}": (
            "import os\n"
            f"_PROBE = {os_call}('{probe_tool} -r .x')\n"
            + tool_text).encode()},
    ))
    positives.append((
        "NPA-4-UNDECLARED-EXTERNAL-TOOL",
        "WRONG: the same call through subprocess.call -- NB-2's named gap, the "
        "oldest and simplest of these APIs, which v2 did not carry",
        {f"artifacts/{tool_source}": (
            "import subprocess\n"
            f"_PROBE = {sp_call2}(['{probe_tool}', '-r', '.x'])\n"
            + tool_text).encode()},
    ))
    positives.append((
        "NPA-4-UNDECLARED-EXTERNAL-TOOL",
        "WRONG: the same call through os.spawnlp, whose program argument is the "
        "SECOND one -- an index this file derives per API instead of assuming",
        {f"artifacts/{tool_source}": (
            "import os\n"
            f"_PROBE = os.spawnlp(os.P_WAIT, '{probe_tool}', '{probe_tool}', '.x')\n"
            + tool_text).encode()},
    ))
    positives.append((
        "NPA-5-ORACLE-SIGNATURE-UNRECORDED",
        "CORRUPT: falsify a recorded oracle signature",
        {BLUEPRINT: blueprint_text.replace("derive_codes(ax, maps)",
                                           "derive_codes(ax)").encode()},
    ))
    positives.append((
        "NPA-5-ORACLE-PIN-UNRECORDED",
        "WRONG: replace the oracle digest the documents record with a different, "
        "well-formed one -- the package's record and this file's pin must be "
        "hard-compared, and the DOCUMENT is no longer the authority",
        {FREEZE: freeze_text.replace(oracle_pin, "f" * 64).encode(),
         BLUEPRINT: blueprint_text.replace(oracle_pin, "f" * 64).encode()},
    ))
    positives.append((
        "NPA-6-IRREPRODUCIBLE-GOLDEN-UNRECORDED",
        "CORRUPT: falsify the recorded golden-vector completeness figure",
        {BLUEPRINT: re.sub(r"carries (\d+) of (\d+) `PLAN-ID-V1` preimage fields",
                           r"carries 99 of \2 `PLAN-ID-V1` preimage fields",
                           blueprint_text).encode()},
    ))

    # ----- NEGATIVE controls: these must produce NO NEW finding ---------------
    negatives: list[tuple[str, dict[str, Any]]] = []

    negatives.append((
        "CONTROL (incidental modal): insert 'Readers must note:' into the DERIVED "
        "STATUS row -- asserts nothing new and must not flip the grade",
        {SLICE: slice_text.replace(
            status_row_line,
            status_row_line.replace("| ", "| Readers must note: ", 1), 1).encode()},
    ))
    negatives.append((
        "CONTROL (polarity): record a closure inside the unresolved section -- a "
        "line saying a decision IS DECIDED must not read as a line saying it is open",
        {SLICE: slice_text.replace(
            live_heading,
            live_heading + "\n\n| `G3-SUBSTRATE` | was DECIDED on 2026-08-05 by the "
            "product authority and is no longer open | closed |\n", 1).encode()},
    ))
    negatives.append((
        "CONTROL (modal synonym): rewrite the derived STATUS row's modal vocabulary "
        "-- a synonym swap must not move the grade in either direction",
        {SLICE: slice_text.replace("execution must follow",
                                   "execution shall follow", 1).encode()},
    ))
    # ----- REFUSAL matrix: this file's own exit-code claims, gated ------------
    # (label, overlay, expected exit, expected token, forbidden token, noop_ok)
    #
    # `noop_ok` exists for exactly one case and inverts NB-4's check rather than
    # waiving it.  A CONTROL that re-supplies pinned bytes VERBATIM is meant to
    # change nothing: that is what makes it evidence that the drift cases below
    # are caused by their mutations and not by the overlay mechanism.  For every
    # other case a no-op means the case tested nothing and fails the build.
    refusals: list[tuple[str, dict[str, Any], int, str, str, bool]] = [
        ("invalid packet JSON",
         {PACKET: b"{ this is not json"}, EXIT_REFUSED, "NPA-INPUT-MALFORMED", "", False),
        ("required input has the WRONG TOP-LEVEL SHAPE (packet is a list) -- NB-1",
         {PACKET: b"[]"}, EXIT_REFUSED, "NPA-INPUT-MALFORMED", "", False),
        ("required document missing (freeze)",
         {FREEZE: FileNotFoundError("No such file or directory")},
         EXIT_REFUSED, "NPA-INPUT-UNREADABLE", "", False),
        ("required document unreadable (blueprint)",
         {BLUEPRINT: PermissionError("Permission denied")},
         EXIT_REFUSED, "NPA-INPUT-UNREADABLE", "", False),
        ("required input undecodable (packet is not UTF-8)",
         {PACKET: b"\xff\xfe\x00binary"}, EXIT_REFUSED, "NPA-INPUT-UNDECODABLE", "", False),
        ("this file's OWN SOURCE unreadable -- the execution-surface audit is a "
         "required input",
         {SELF_REL: FileNotFoundError("No such file or directory")},
         EXIT_REFUSED, "NPA-INPUT-UNREADABLE", "", False),
        ("this file's own source carries an execution primitive OUTSIDE the "
         "declared gate -- the audit must refuse the whole run",
         {SELF_REL: doctored_self.encode()},
         EXIT_REFUSED, "NPA-EXEC-AUDIT-DISAGREES", "", False),
        ("this file's own source does not parse, so its execution surface cannot "
         "be derived",
         {SELF_REL: unparseable_self.encode()},
         EXIT_REFUSED, "NPA-EXEC-AUDIT-DISAGREES", "", False),
        ("per-class document missing (v1-slice.md)",
         {SLICE: FileNotFoundError("No such file or directory")},
         EXIT_INCOMPLETE, "NPA-INPUT-UNREADABLE", "", False),
        ("executed pin drifted (check-package-coherence.py)",
         {PCM: good_pcm + b"\n# drift\n"}, EXIT_INCOMPLETE, "NPA-PIN-DRIFT", "", False),
        ("executed pin missing",
         {PCM: FileNotFoundError("No such file or directory")},
         EXIT_INCOMPLETE, "NPA-INPUT-UNREADABLE", "", False),
        ("D9 ORACLE PIN DRIFTED -- the second executed module, which v2 pinned "
         "from an UNPINNED document",
         {D9_ORACLE: oracle_bytes + b"\n# drift\n"},
         EXIT_INCOMPLETE, "NPA-PIN-DRIFT", "NPA-PIN-EXEC-FAILED", False),
        ("D9 oracle missing",
         {D9_ORACLE: FileNotFoundError("No such file or directory")},
         EXIT_INCOMPLETE, "NPA-INPUT-UNREADABLE", "", False),
        # THE REVIEWER'S ATTACK, executed in memory.  Attacker-chosen oracle bytes
        # that RAISE if they are ever executed, plus a forged digest inserted into
        # the unpinned blueprint beside the module's name.  On v2 this printed the
        # full green banner at exit 0 with the payload executed.  The forbidden
        # token is what proves the payload did not run: reaching `exec` would
        # report NPA-PIN-EXEC-FAILED instead of NPA-PIN-DRIFT.
        ("BLOCKING-1: attacker-chosen oracle bytes PLUS a forged digest inserted "
         "into the unpinned blueprint beside the oracle's name",
         {D9_ORACLE: hostile_oracle, BLUEPRINT: forged_blueprint.encode()},
         EXIT_INCOMPLETE, "NPA-PIN-DRIFT", "NPA-PIN-EXEC-FAILED", False),
        ("per-class contract malformed (D9)",
         {D9_CONTRACT: b"{"}, EXIT_INCOMPLETE, "NPA-INPUT-MALFORMED", "", False),
        ("per-class contract has the WRONG TOP-LEVEL SHAPE (D9 is a list) -- NB-1",
         {D9_CONTRACT: b"[]"}, EXIT_INCOMPLETE, "NPA-INPUT-MALFORMED", "", False),
        ("per-class contract missing (resolved-inputs)",
         {RESOLVED: FileNotFoundError("No such file or directory")},
         EXIT_INCOMPLETE, "NPA-INPUT-UNREADABLE", "", False),
        ("per-class input has the WRONG TOP-LEVEL SHAPE (resolved-inputs is a "
         "list) -- NB-1: v2 turned this into a whole-run internal error at exit 2, "
         "stopping five classes that never needed the file",
         {RESOLVED: b"[]"}, EXIT_INCOMPLETE, "NPA-INPUT-MALFORMED", "", False),
        # The two controls.  NPA-PIN-EXEC-FAILED is deliberately unreachable
        # through an overlay: the hash gate runs FIRST, so any byte that would
        # make a module fail to execute has already failed the pin.  Verified
        # rather than assumed -- these re-supply each pinned module's bytes
        # verbatim and the run must be COMPLETE and GREEN, which proves the
        # drift and exec cases above are caused by their mutations and not by
        # the overlay mechanism itself.
        ("CONTROL: check-package-coherence.py re-supplied verbatim -- must run "
         "complete and green",
         {PCM: good_pcm}, EXIT_GREEN, "", "", True),
        ("CONTROL: the pinned D9 oracle re-supplied verbatim -- must run complete "
         "and green, so the two drift cases above are caused by their mutations",
         {D9_ORACLE: oracle_bytes}, EXIT_GREEN, "", "", True),
    ]

    escapes = 0
    print(f"SELFTEST: {len(positives)} positive mutations, {len(negatives)} negative "
          f"controls, {len(refusals)} hostile inputs, against a base at "
          f"{len(base.findings)} finding(s)")
    print("  scoring: FINDING-SET DELTA against the base run. A positive case passes "
          "only if it")
    print("  produces a finding the base did NOT have; a negative passes only if the "
          "delta is EMPTY.")
    print()
    print("  GATES -- this file's own published figures and its own structure")

    for problem in limits_count_disagreement():
        escapes += 1
        print(f"    [STALE] {problem}")
    if not limits_count_disagreement():
        print(f"    [AGREES] the docstring publishes {len(LIMITS)} limits and "
              f"{len(gated_limits())} gated, and both equal the data")

    # Every limit that CLAIMS a gate must name a case this suite actually runs.
    # A gate is satisfied by a case's LABEL or by the finding id that case
    # expects, because the id is what identifies the class being exercised.
    all_labels = ([f"{exp} {lab}" for exp, lab, _ in positives]
                  + [lab for lab, _ in negatives]
                  + [lab for lab, _, _, _, _, _ in refusals])
    for lim in gated_limits():
        if not any(lim["gate"] in lab for lab in all_labels):
            escapes += 1
            print(f"    [UNGATED] {lim['id']} claims the gate {lim['gate']!r} and no "
                  f"case in this suite carries it")
    if all(any(l["gate"] in lab for lab in all_labels) for l in gated_limits()):
        print(f"    [AGREES] all {len(gated_limits())} gated limits name a case this "
              f"suite executes")

    # The execution-surface audit, on these bytes, printed rather than assumed.
    sites, problems = audit_execution_surface(self_source)
    if problems:
        escapes += 1
        print(f"    [EXEC-AUDIT FAILED] {'; '.join(problems)}")
    else:
        print(f"    [AGREES] {len(sites)} execution primitive(s) in these bytes, all "
              f"inside {EXEC_GATE}(); modules pinned: {sorted(EXECUTED_PINS)}")

    # Both directions of the pin table: nothing executes unpinned (structural,
    # by the gate), and no pin is dead weight (measured, by the base run).
    if sorted(base.counts.get("modulesExecutedThisRun") or []) != sorted(EXECUTED_PINS):
        escapes += 1
        print(f"    [PIN/EXEC MISMATCH] pinned {sorted(EXECUTED_PINS)} but the base "
              f"run executed {sorted(base.counts.get('modulesExecutedThisRun') or [])}")
    else:
        print(f"    [AGREES] every pinned module was executed this run and no other "
              f"module was")

    # NB-8: the transitive-closure heuristic must attribute NO execution edge to
    # this file.  v2 escaped it by an accident of punctuation; this asserts it.
    peer_names = {p.name for p in sorted(ARTIFACTS.glob("check-*.py"))}
    self_peers = closure_peers(self_source, SELF_NAME, peer_names)
    if self_peers:
        escapes += 1
        print(f"    [SELF-ATTRIBUTION] the peer heuristic attributes execution edges "
              f"{sorted(self_peers)} to this file, so it would inject a synthetic "
              f"dependency into the census it participates in")
    else:
        print("    [AGREES] the peer heuristic attributes ZERO execution edges to "
              "this file, asserted rather than incidental (NB-8)")

    if base.counts.get("rejectPartitionExhaustive") is not True:
        escapes += 1
        print(f"    [PARTITION] NPA-3's four-way partition of the REJECT-carrying "
              f"corpus does not sum to the disk-derived total "
              f"{base.counts.get('rejectSubjectsInCorpus')}")
    else:
        print(f"    [AGREES] NPA-3's partition is exhaustive against "
              f"{base.counts.get('rejectSubjectsInCorpus')} REJECT-carrying "
              f"artifacts derived from disk, a total neither document can write")

    print()
    print("  POSITIVE -- each must add a NEW finding of the class named for it")
    for expected, label, overlay in positives:
        if overlay_is_noop(rd0, overlay):
            escapes += 1
            print(f"    [NO-OP] {expected}")
            print(f"        {label}")
            print("        -- the overlay replaced every byte it touched with "
                  "itself, so this case tested nothing")
            continue
        try:
            found = run_check(Reader(overlay))
            new = {fp.split("\x00", 1)[0] for fp in found.fingerprints - base_fp}
        except Refusal as exc:
            new = {f"REFUSED:{exc.token}"}
        ok = expected in new
        if not ok:
            escapes += 1
        print(f"    [{'REJECTED' if ok else 'ADMITTED'}] {expected}")
        print(f"        {label}")
        if not ok:
            print(f"        -- new findings: {sorted(new) or 'none'}")

    print()
    print("  NEGATIVE -- each must add NO finding and REMOVE none")
    for label, overlay in negatives:
        if overlay_is_noop(rd0, overlay):
            escapes += 1
            print(f"    [NO-OP] {label}")
            print("        -- the overlay changed nothing, so silence proves "
                  "nothing (NB-4)")
            continue
        try:
            found = run_check(Reader(overlay))
            delta = sorted(
                [f"+{fp.split(chr(0), 1)[0]}" for fp in found.fingerprints - base_fp]
                + [f"-{fp.split(chr(0), 1)[0]}" for fp in base_fp - found.fingerprints])
        except Refusal as exc:
            delta = [f"REFUSED:{exc.token}"]
        ok = not delta
        if not ok:
            escapes += 1
        print(f"    [{'SILENT' if ok else 'MOVED'}] {label}")
        if not ok:
            print(f"        -- finding-set delta {delta}")

    print()
    print("  HOSTILE INPUT -- each must exit on the claimed code with a NAMED token, "
          "no traceback,")
    print("  and never the forbidden token where one is named")
    for label, overlay, want_exit, want_token, forbidden, noop_ok in refusals:
        is_noop = overlay_is_noop(rd0, overlay)
        if is_noop != noop_ok:
            escapes += 1
            if is_noop:
                print(f"    [NO-OP] {label}")
                print("        -- the overlay changed nothing, so this case tested "
                      "nothing (NB-4)")
            else:
                print(f"    [NOT-A-CONTROL] {label}")
                print("        -- this case is declared a verbatim control and its "
                      "overlay does NOT match the live bytes")
            continue
        try:
            result = run_check(Reader(overlay))
            got_exit = classify(result)
            tokens = {s["token"] for s in result.skips}
        except Refusal as exc:
            got_exit = EXIT_REFUSED
            tokens = {exc.token}
        except Exception as exc:                            # noqa: BLE001
            escapes += 1
            print(f"    [TRACEBACK] {label} -- {type(exc).__name__}: {exc}")
            continue
        token_ok = (not want_token) or (want_token in tokens)
        clean = (not forbidden) or (forbidden not in tokens)
        ok = got_exit == want_exit and token_ok and clean
        if not ok:
            escapes += 1
        note = "" if not forbidden else f"  [never {forbidden}: {clean}]"
        print(f"    [{'NAMED' if ok else 'WRONG'}] exit {got_exit} "
              f"(claimed {want_exit}) tokens {sorted(tokens) or 'none'}{note}")
        print(f"        {label}")

    print()
    if escapes:
        print(f"SELFTEST FAILED: {escapes} case(s) did not behave as claimed")
        return EXIT_FINDINGS
    print(f"SELFTEST PASSED: {len(positives)}/{len(positives)} mutations each added a "
          f"NEW finding of the class named for it;")
    print(f"  {len(negatives)}/{len(negatives)} negative controls moved the finding "
          f"set by nothing, and none was a no-op;")
    print(f"  {len(refusals)}/{len(refusals)} hostile inputs refused on the claimed "
          f"exit code with a named token, zero tracebacks;")
    print(f"  {_RUN_CHECK_CALLS} complete runs of the checker were executed to say so "
          f"(counted, not stated -- NB-6).")
    print("  bound: mutations are applied to in-memory copies. Nothing is written to")
    print("  the tree, so this suite proves the classes FIRE and the refusals are")
    print("  NAMED -- not that the tree is safe to edit. Run normally after any edit.")
    print("  bound: a negative control proves a specific false positive is gone. It")
    print("  is not evidence that the predicate is precise in general; see --limits.")
    return EXIT_GREEN


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

BANNER_KEYS = (
    "packetDecided", "packetPending", "packetClosedStatusTokens",
    "authorityDocsScanned", "narrativeDocsScanned", "unresolvedHeadingsMatched",
    "disagreementsDerived", "disagreementsRecorded",
    "rejectSubjectsInCorpus", "rejectSubjectsNamedByBothDocs",
    "rejectSubjectsNamedByFreezeOnly", "rejectSubjectsNamedByBlueprintOnly",
    "rejectSubjectsNamedByNeither", "rejectPartitionExhaustive",
    "rejectPopulationJoinedSinceRecord",
    "subjectsGraded", "subjectsRejected", "subjectsRejectedNames",
    "rejectDisclosureSameLine",
    "checkersScanned", "checkersUnparsed", "checkersUnreadable",
    "externalToolDependents", "externalTools", "toolsDeclaredInEnvTable",
    "envDeclarationRows",
    "oracleModule", "oracleExports", "oraclePinnedHere",
    "oracleDigestsRecordedInDocs",
    "preimageFields", "goldenVectors",
    "modulesExecutedThisRun",
)


def report(rd: Reader, result: Result) -> int:
    print("NARRATIVE/PACKET AGREEMENT v3 -- package prose <-> the corpus it describes")
    print()
    print("  inputs read as data (no pin: these are the documents under comparison):")
    for rel in (PACKET, FREEZE, BLUEPRINT, SLICE, D9_CONTRACT, RESOLVED):
        try:
            print(f"    {rel:44s} {rd.digest(rel)}")
        except Refusal as exc:
            print(f"    {rel:44s} <{exc.token}: {exc.reason[:60]}>")
    print()
    print("  MODULES THIS FILE EXECUTES -- the complete list, and how each is pinned")
    print("  (freeze section 7.3: read, hash, compare, THEN exec -- one gate only):")
    for rel, entry in sorted(EXECUTED_PINS.items()):
        print(f"    {rel:44s} {entry['sha256']}")
        print(f"      pinned INTERNALLY; on drift: {entry['skip']} skips "
              f"{entry['classes']} by name at exit 4, other classes keep measuring")
        print(f"      why executed: {entry['why']}")
    sites = result.counts.get("execAuditSites") or []
    print(f"    AST AUDIT of these bytes: {len(sites)} execution primitive(s), all "
          f"inside {EXEC_GATE}():")
    for site in sites:
        print(f"      {site}")
    print("    NO DIGEST READ FROM A DOCUMENT AUTHORISES EXECUTION HERE. The")
    print("    predecessor derived the D9 oracle's expected digest from the two")
    print("    UNPINNED documents under comparison; inserting one string beside the")
    print("    module's name bought arbitrary code execution at a green exit 0.")
    print("    See --limits L-13/L-14 for what this audit does NOT bind.")
    print()
    print("  measured this run:")
    for key in BANNER_KEYS:
        value = result.counts.get(key)
        if isinstance(value, dict):
            print(f"    {key}")
            if not value:
                print("      (none)")
            for k in sorted(value):
                print(f"      {str(k):50s} {value[k]}")
        else:
            print(f"    {key:36s} {value}")
    print()
    print("  POPULATIONS -- how many rows each lane generated, and what a row IS.")
    print("  Freeze section 7.2.2, sharpened 2026-08-10: a lane that does not publish")
    print("  how many rows it generated is making an uncheckable claim.")
    for lane, what, size in result.populations:
        print(f"    {lane}: {size}")
        print(f"      row = {what}")
    print()
    print("  NPA-3 recorded REJECT population (a MEASUREMENT, hard-compared; a member")
    print("  that leaves the graded set is NPA-3-COVERAGE-WITHDRAWN, growth is free):")
    for name in NPA_3_RECORDED_REJECT_POPULATION:
        print(f"    {name}")
    print("    recorded against, for context only -- these are NOT pins, because")
    print("    these are the documents under comparison:")
    for rel, digest in sorted(NPA_3_RECORDED_AGAINST.items()):
        try:
            live = rd.digest(rel)
        except Refusal:
            live = "<unreadable>"
        moved = "" if live == digest else "   <-- MOVED since this was recorded"
        print(f"      {rel:34s} {digest}{moved}")
    print()
    print("  NPA-1 reach -- the heading vocabulary that defines what it can see:")
    for term in UNRESOLVED_HEADING_TERMS:
        print(f"    /{term}/i")
    print("    This list is exhaustive of nothing. See --limits L-1: a reworded")
    print("    heading is caught for a RECORDED disagreement by the both-ways")
    print("    comparison and is invisible for an UNRECORDED one.")

    if result.observations:
        print()
        print("  observations (not findings):")
        for obs in result.observations:
            print(f"    {obs}")

    if result.skips:
        print()
        print("  CLASSES THAT DID NOT RUN -- this run is INCOMPLETE:")
        for s in result.skips:
            print(f"    {s['token']} [{s['classes']}] {s['subject']}")
            print(f"      {s['reason']}")
        print("    A class that did not run has found NOTHING. Do not read its")
        print("    silence as a pass.")

    print()
    if result.findings:
        print(f"FINDINGS: {len(result.findings)}")
        for f in result.findings:
            print(f"  {f['id']}: {f['statement']}")
            print(f"    {f['detail']}")
    exit_code = classify(result)
    if exit_code == EXIT_GREEN:
        print("OK: every derived disagreement is recorded, every record is live, every")
        print("  derived external tool is declared and every dependent named, the")
        print("  recorded REJECT population is intact, and every document claim above")
        print("  equals the measurement it describes.")
    elif exit_code == EXIT_INCOMPLETE:
        print(f"INCOMPLETE: {len(result.skips)} class(es) did not run; "
              f"{len(result.findings)} finding(s) from the classes that did.")
        print("  Exit 4 CAN carry findings. A CI rule reading 'exit 1 means findings'")
        print("  will miss the ones above.")
    print("  scope: agreement only. Says nothing about whether a recorded")
    print("  disagreement is ACCEPTABLE -- freeze section 2's authority order decides")
    print("  that, and section 10 decides whether the narrative gets amended.")
    print(f"  Run --limits for the {len(LIMITS)} ways this instrument can be made to")
    print(f"  pass on a wrong package, {len(gated_limits())} of them gated by an")
    print("  executed selftest case. That count is a FLOOR, not a ceiling.")
    return exit_code


def main(argv: list[str]) -> int:
    if not (sys.flags.isolated and sys.dont_write_bytecode):
        print("NPA-UNSUPPORTED-INVOCATION: run as `python3 -I -B "
              f"artifacts/{SELF_NAME}`. THE CHECK DID NOT RUN.")
        return EXIT_REFUSED
    if len(argv) > 2 or (len(argv) == 2 and argv[1] not in ("--selftest", "--limits")):
        print("NPA-UNSUPPORTED-INVOCATION: accepts no arguments, or --selftest, or "
              "--limits. THE CHECK DID NOT RUN.")
        return EXIT_REFUSED

    try:
        if len(argv) == 2 and argv[1] == "--limits":
            print_limits()
            return EXIT_GREEN
        if len(argv) == 2:
            return selftest()
        reader = Reader()
        result = run_check(reader)
        return report(reader, result)
    except Refusal as exc:
        print(f"NPA-REFUSED: {exc.token} {exc.subject}")
        print(f"  {exc.reason}")
        print("  THE CHECK DID NOT RUN. This is exit 2, not a finding: no class was")
        print("  evaluated, so nothing has been measured about the package. Litmus")
        print("  defect D-6 is exactly the mistake of recording this as a finding.")
        return EXIT_REFUSED
    except KeyboardInterrupt:
        print("NPA-INTERRUPTED: THE CHECK DID NOT RUN.")
        return EXIT_REFUSED
    except Exception as exc:                                # noqa: BLE001
        print(f"NPA-INTERNAL-ERROR: {type(exc).__name__}: {exc}")
        print("  THE CHECK DID NOT RUN TO COMPLETION. This is exit 2, not a finding.")
        print("  An unforeseen error in this instrument says nothing whatever about")
        print("  the package it was asked to measure. Report it against this file.")
        return EXIT_REFUSED


if __name__ == "__main__":
    sys.exit(main(sys.argv))
