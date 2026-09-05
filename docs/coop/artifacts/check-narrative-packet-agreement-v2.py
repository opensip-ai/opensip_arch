#!/usr/bin/env python3
"""Executable agreement between the package's PROSE and the corpus it describes.

SUCCESSOR to `check-narrative-packet-agreement.py`
(`6a2a3da526a5b6e4bb54cfb44dbf619d0c725d1506968a7053f7f88eae0d8148`, 36114 bytes,
independently reviewed at ACCEPT / 2 blocking / 7 non-blocking).  Freeze section
7.2 forbids editing reviewed bytes, so every repair below is a new file and the
predecessor is untouched.  Its ideas are kept; three measured defects are fixed.

WHY THE PREDECESSOR EXISTS, PRESERVED VERBATIM IN INTENT.

A blind implementer litmus recorded ten defects.  Five (D-6..D-10) share one
shape, and the shape is not "a document is wrong".  It is:

    a package document makes a statement ABOUT the corpus, and nothing
    compares that statement to the corpus.

The sharpest instance was D-7.  `v1-slice.md` is authority level 2 -- above the
freeze's own implementation mapping -- it is digest-pinned by freeze section 2
and sits inside the section 9.2 manifest, and NO CHECKER READ A BYTE OF ITS
CONTENT.  A pin is not a reader.  Its bytes were fixed and its meaning was
unobserved, so a contradiction inside it was not merely unrecorded -- it was
unobservable.  Six derived classes NPA-1..NPA-6 close that, and none of them has
a defect site written into it: every class compares a DERIVED set against a
RECORDED set, in both directions, so a record that goes stale is a finding in
its own right and a repaired document retires its own record.

THE THREE DEFECTS THIS SUCCESSOR REPAIRS, each measured against live bytes
before it was repaired.

  1  (BLOCKING, `IR-NPA-B2`)  IT FAILED ITS OWN CRASH TEST.
     Measured on the predecessor: invalid packet JSON -> bare traceback, exit 1.
     `v1-slice.md` removed -> bare traceback, exit 1, raised in the REPORTING
     block AFTER the analysis, so it is harder to notice rather than easier.
     An unreadable input -> bare traceback, exit 1.  And `load_pinned_module`
     raised `SystemExit(str)`, so a pin refusal exited **1** while the refusal
     text's own last words were "Exit 2."  Exit 1 therefore carried three
     meanings: findings, integrity refusal, and crash.  That is litmus defect
     D-6 -- "the guard never ran, so exit 1 is NOT a finding" -- committed by
     the instrument whose NPA-4 exists to detect it elsewhere.

     A FOURTH CASE, found here and not previously recorded: with `v1-slice.md`
     absent, `derive_disagreements` swallowed the `OSError` and the run produced
     **3 false `NPA-2-STALE-DISAGREEMENT-RECORD` findings** accusing freeze
     section 5.1 of recording disagreements the live bytes no longer show.  The
     live bytes showed nothing because they could not be read.  A missing input
     read as a verdict, which is the same defect wearing a quieter face.

     REPAIR.  Every byte enters through a `Reader` that converts `OSError`,
     `UnicodeDecodeError` and `JSONDecodeError` into a typed `Refusal` carrying
     a NAMED token.  Inputs are tiered.  A REQUIRED input that cannot be read
     refuses the whole run at exit 2 with `NPA-REFUSED` and the words THE CHECK
     DID NOT RUN.  A PER-CLASS input that cannot be read SKIPS exactly the
     classes that need it, names the skip, suppresses the findings that input
     would otherwise have distorted, and exits 4.  `main` is wrapped so that no
     exception of any kind can reach the interpreter: an unforeseen one prints
     `NPA-INTERNAL-ERROR` with its type and exits 2, never 1.

  2  (`IR-NPA-B1` cause one)  NPA-4's `curl` FALSE POSITIVE WAS FIXABLE and had
     been recorded as structural.  Measured: all five `EXTERNAL_CALL` hits in
     `check-rust-provider-protocol-v5.py` are in NON-EXECUTABLE TEXT -- one in
     the module docstring describing what v2 does, four in byte-string literals
     that are NEGATIVE PROBES asserting such code must be refused.  v5 contains
     no executable `curl` call of any kind.

     REPAIR.  The direct-call predicate is now an AST match -- `ast.Call` whose
     callee resolves to `subprocess.run/Popen/check_output/check_call`
     (including `import subprocess as sp` aliases and `from subprocess import
     run`, which the text regex missed) or to `os.system` / `os.popen`, with a
     literal string argv[0].  Docstrings and string/bytes constants drop out for
     free because they are not `Call` nodes.  Measured across the corpus:
     `curl` disappears, and every true positive is preserved.  This is a repair
     to the predicate, not a carve-out; v5's name appears nowhere in it.

     `rg` on v5 is NOT repaired and must not be.  v5 really does
     `exec(compile(...))` v2's bytes and v2 really does call `rg`; the edge is
     real and is inert only because v5 installs a stand-in `subprocess` module
     inside the executed closure at RUNTIME.  Freeze section 7.6 states the
     shape exactly -- a property true only at execution time is invisible to a
     static scan -- and the blueprint is right to record the counter-measurement
     rather than satisfy the instrument.

  3  (`IR-NPA-B1` proper)  NPA-4 TESTED FOR AN UNDECLARED CHECKER, NOT AN
     UNDECLARED TOOL.  The predecessor's whole test was `if fname not in
     env_section`: the TOOL NAME WAS NEVER COMPARED AGAINST ANYTHING.
     Reproduced here -- a real, executable, top-level `jq` invocation added to a
     lab copy of v5 made the instrument derive `externalTools ['curl','jq','rg']`
     and exit **0**, because v5's filename was already in the section.

     DECISION: WIDEN THE CLASS, and additionally RENAME the limb that was doing
     the narrower job so both are legible.  Justification, because the brief
     offered rename as an alternative: the class's own stated purpose is to
     protect a signer who meets an unaccounted exit 1 from reading it as a
     finding, and what protects that signer is knowing WHICH BINARY TO INSTALL.
     A section that names the checker and not the tool tells them nothing
     actionable, so `UNDECLARED-EXTERNAL-TOOL` is the right NAME for the
     property that matters and renaming it would have preserved the less useful
     half under an accurate label.  Both limbs are cheap because both sets were
     already computed.  So:

        NPA-4-UNDECLARED-EXTERNAL-TOOL   a derived tool is not DECLARED
        NPA-4-UNDECLARED-TOOL-DEPENDENT  a derived dependent is not NAMED

     "DECLARED" is not containment.  Measured while building this: `jq` occurs
     TWICE and `curl` THREE TIMES inside the environment-prerequisites section
     TODAY -- in the prose that describes them as instrument false positives --
     so a containment test over the section would admit exactly the tool the
     reviewer proved could be added undetected.  A tool is declared only when it
     is named in the TOOL COLUMN of a table row in that section.  If the table
     shape changes, the declared set empties and the class fires: over-reporting
     is the safe direction, and it is the same discipline the section 5.1
     register parser already states for itself.

ALSO REPAIRED, from the review's non-blocking set.

  `IR-NPA-N1` KIND was `\bmust\b` anywhere on the line.  Two words -- "Readers
  must note:" -- inserted into a row, changing nothing it asserts, flipped the
  grade STATUS -> CONTENT and raised a finding accusing the register of the
  wrong grade.  And the mode ran both ways: "shall", "is required to" and
  "implementers are to" were not detected at all.  REPAIR: the modal vocabulary
  is widened (`must`, `must not`, `shall`, `shall not`, `may not`, `is/are
  required to`, `is/are to`) and each occurrence is tested for an EDITORIAL
  SUBJECT immediately governing it, from a closed set of reader/reviewer/author
  roles.  A line grades CONTENT only if some modal on it is NOT editorial.  This
  is the design freeze section 7.10 credits in `check-versioning-v14.py` -- a
  closed set of non-qualifying roles, rejected by name.  A line carrying both an
  aside and a genuine binding still grades CONTENT; verified.

  `IR-NPA-N1` POLARITY.  `named_in` had none, so a line RECORDING A CLOSURE
  inside an unresolved-headed section read identically to one asserting the
  decision is open.  REPAIR: a line that names the identifier and also names one
  of the PACKET'S OWN closed-status tokens is recording the closure, not
  contradicting it.  The tokens are DERIVED from `$.decisions[*].status` at
  runtime, never transcribed, so this cannot go stale against a packet that
  starts using a third status word.

  `IR-NPA-N2` THE HEADING VOCABULARY IS THE REACH OF NPA-1 AND WAS DISCLOSED
  NOWHERE.  It is now printed in the banner in full, with `headingsMatched` per
  document so a reader can see when the predicate found nothing to look at.  And
  NPA-2 now DIAGNOSES which of the two reasons a record went stale: the document
  still has unresolved-headed sections and none names the id, or the document
  has NO unresolved-headed section at all -- the signature of a reworded
  heading, which is exactly the residual.  The residual itself is NOT closed and
  is not claimed to be: see LIMITS below.

  `IR-NPA-N3` NPA-3's disclosure window was containment over an undisclosed
  600-character magic constant.  REPAIR: the window is now the ENCLOSING BLOCK
  -- the paragraph or table row containing the artifact's name -- which is a
  structural unit rather than a number, and is immune to the line-wrapping
  false-negative generator freeze section 7.7 calls the sharpest in the package,
  because the block is folded before it is searched.  Polarity is now tested: a
  `REJECT` governed by a negation is not a disclosure.  Attribution WITHIN a
  block is still not established -- see LIMITS -- so the banner publishes
  `rejectDisclosureSameLine` alongside the block figure, which is the measure of
  how much of the disclosure is attributed rather than merely co-located.

  `IR-NPA-N4` THE INSTRUMENT PINS THE MOST MOVABLE CHECKER IN THE CORPUS.
  Freeze section 7.6 lists `check-package-coherence.py` among the five carrying
  no current-byte pin, and its worked example is a sibling in that list that was
  edited and silently invalidated eleven review artifacts.  Executing rather
  than reimplementing is still correct and the reason is unchanged: NPA-3
  measures whether the documents disclose what THAT derivation finds, and a
  second private copy could disagree with `PC-7` invisibly.  REPAIR is to the
  FAILURE MODE, per freeze section 7.10's closing rule -- "if a digest pin is
  kept anyway, make it a named, non-fatal drift notice distinguishable from a
  semantic failure".  Drift no longer stops the instrument: the bytes are still
  never executed unverified, NPA-3 alone is SKIPPED, the skip is named
  `NPA-3-NOT-RUN` on stdout, and the run exits 4.  Five classes that never
  needed that file keep measuring.  This deliberately differs from the review's
  suggested exit 2: exit 2 means the check did not run, and five sixths of it
  did.  The fragility is also stated in the banner on every run.

  `IR-NPA-N5` THE SELFTEST'S MUTATIONS WERE ALL REMOVALS OR CORRUPTIONS, so
  freeze section 7.8's harder standard -- "for every assertion, exhibit an input
  that is WRONG rather than merely EMPTY" -- was unmet, and neither false
  positive the review found would have been caught by it.  The suite now carries
  the predecessor's 7 plus WRONG-not-EMPTY cases (a negated REJECT disclosure
  that keeps the token; a real undeclared tool call; a genuinely binding new row
  under a live heading), NEGATIVE CONTROLS that must NOT fire (the two
  reproduced false positives, and a modal-synonym swap that must preserve the
  grade), and a REFUSAL SUITE that runs the whole hostile-input matrix and fails
  the build if any case produces the wrong token or the wrong exit code.  That
  last is freeze section 7.2.2's rider applied to this file's own crash claims:
  a claim that cannot fail the build is prose.

  `IR-NPA-N6` / `IR-NPA-N7` `curl` is gone by repair 2 rather than by
  documentation, and the banner now prints the dependent -> tool MAPPING
  instead of a bare count, which is the fact NPA-4 exists to make visible.

WHAT THIS FILE DOES NOT DO, deliberately, for the reason
`check-package-coherence.py` gives for the same choice.

It does not pin `IMPLEMENTATION-FREEZE.md`, `IMPLEMENTER-BLUEPRINT.md` or
`v1-slice.md` by hash.  Those are the documents under comparison; pinning them
would make every legitimate edit a failure and would train the next author to
regenerate a pin instead of reading a diff.  Freeze section 2 makes the same
argument for why the freeze gets content anchors rather than a byte pin, and
freeze section 7.10 generalises it: pin what you depend on and re-extract it.

It pins exactly ONE file, `check-package-coherence.py`, because it EXECUTES it.
Freeze section 7.3 permits executing a verified closure and requires the hash to
hold BEFORE the bytes run.  The order here is read, hash, compare, then exec.

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
         Symmetry matters: an amended `v1-slice.md` must not leave a record
         asserting a contradiction that has been repaired.

  NPA-3  UNDISCLOSED-REJECT
         An artifact both package documents name, whose OWN independent review
         decides REJECT, is not disclosed together with that verdict in BOTH
         documents.

  NPA-4  UNDECLARED-EXTERNAL-TOOL / UNDECLARED-TOOL-DEPENDENT
         A checker needs an external binary -- directly, or through a checker
         whose bytes it compiles and executes -- and the blueprint's
         environment-prerequisites table does not DECLARE the binary, or the
         section does not NAME the dependent.  A checker that aborts before
         evaluating any contract property has measured nothing, and a signer who
         meets its exit 1 unaccounted reads it as a finding.

  NPA-5  ORACLE-SIGNATURE-UNRECORDED
         An export the D9 contract's own `referenceDerivation` names as the
         axes-to-class oracle is not recorded in the blueprint at the call
         signature the live module actually exposes.

  NPA-6  IRREPRODUCIBLE-GOLDEN-UNRECORDED
         A `PLAN-ID-V1` golden vector whose own bytes omit some of the
         contract's declared preimage fields is not recorded in the blueprint at
         its measured completeness.

SCOPE OF THE FINDING SET, stated because it is a judgement and not a measurement.

Freeze section 2 ranks `architecture/` narrative LAST and admits it "only where
it does not conflict with the binding set" -- a conflict there is pre-resolved by
rule.  `GORTEX-BORROW-REGISTER.md` carries no product-disposition authority of
its own.  Neither is therefore a FINDING scope for NPA-1; both are scanned and
reported as OBSERVATIONS, so a reader still learns they disagree.  The finding
scope is the three documents that carry authority: the freeze, the blueprint,
and `v1-slice.md`.

LIMITS -- the freeze section 7.8 question, answered honestly and scoped.

The question is "can I make this checker pass on a wrong artifact?"  The answer
is YES, and the count is EIGHT, printed by `--limits` with a worked example for
each and SCOPED TO THE CLASS IT AFFECTS.  They are not printed under one
unqualified heading, because the review's sharpest procedural criticism of a
sibling instrument was residuals printed under a heading broader than the lane
that produced them while another lane contributed more that appeared nowhere.

Exit codes -- distinct, and this list is enforced by `--selftest`'s refusal
suite rather than asserted.

  0  the check RAN COMPLETELY and found nothing
  1  the check RAN COMPLETELY and found something.  Only this code means finding
  2  REFUSED -- THE CHECK DID NOT RUN.  Bad invocation, a required input that
     cannot be read or parsed, or an unforeseen internal error.  Never a finding
  3  `--selftest` did not execute its mutation suite
  4  INCOMPLETE -- the check ran but at least one class was SKIPPED.  Every skip
     is named on stdout.  Findings from the classes that DID run are still
     printed and are still real; the run is not green and is not complete
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

FREEZE = "IMPLEMENTATION-FREEZE.md"
BLUEPRINT = "IMPLEMENTER-BLUEPRINT.md"
SLICE = "v1-slice.md"
PACKET = "artifacts/product-dispositions.v1.json"
D9_CONTRACT = "artifacts/d9-exit-contract.v1.14.json"
RESOLVED = "artifacts/resolved-inputs.v2.json"
PCM = "artifacts/check-package-coherence.py"

# Documents whose disagreement with the packet is a FINDING.  This is the set
# freeze section 2 ranks at or above "accepted product scope/dispositions", not
# a list of known defect sites.
AUTHORITY_DOCS = (FREEZE, BLUEPRINT, SLICE)

# Required to run at all.  Losing any of these means the instrument measures
# nothing, so it REFUSES rather than reporting a partial answer as a verdict.
REQUIRED_INPUTS = (PACKET, FREEZE, BLUEPRINT)

# The ONE executed input.  Freeze section 7.3: hash-verify before the bytes run.
EXECUTED_PINS = {
    PCM: "8d56b5f56fed4fd031f4e9f602e63d4f90ac2a189e56b0b580498f20a107f2a6",
}

# A heading declares its contents unresolved.  Structural phrases a document
# uses to say "this is not settled yet", not decision names.  THIS LIST IS THE
# REACH OF NPA-1 AND IS EXHAUSTIVE OF NOTHING -- it is printed in the banner and
# named in LIMITS L-1 for exactly that reason.
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

# A row that BINDS an implementer to an interim posture is materially worse than
# one that merely mislabels a decision's status: the first can be built against.
NORMATIVE_MODAL = re.compile(
    r"\b(?:must not|must|shall not|shall|may not|"
    r"is required to|are required to|is to|are to)\b", re.I)

# A closed set of roles that are readers of the document rather than subjects of
# its rules.  A modal governed by one of these is editorial, not normative.
# Same design as check-versioning-v14.py's non-authority role set: rejected BY
# NAME, so the predicate says what it excludes instead of guessing.
EDITORIAL_SUBJECT = re.compile(
    r"\b(?:reader|readers|note|notes|editor|editors|reviewer|reviewers|"
    r"author|authors|coordinator|coordinators|signer|signers|"
    r"implementer of this note|we|you|one)\s*$", re.I)

# How far back a modal's governing subject is looked for.  A clause, not a line.
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

# argv[0] forms that are the running interpreter, not an external dependency.
INTERPRETER_ARGV0 = ("python3", "python", "sys.executable")

SUBPROCESS_CALLS = ("run", "Popen", "check_output", "check_call")
OS_SHELL_CALLS = ("system", "popen")

# Text fallback, used ONLY for a source the AST cannot parse.  Kept because a
# file that will not parse must over-report, never under-report.
EXTERNAL_CALL_TEXT = re.compile(
    r"subprocess\.(?:run|Popen|check_output|check_call)\(\s*\[\s*(['\"])([^'\"]+)\1")

# Negations that turn a REJECT token into a statement that there was no reject.
REJECT_NEGATION = re.compile(
    r"(?:not|never|no longer|without|withdrawn|withdraw|withdraws|rather than|"
    r"instead of|avoids?|free of)\W{0,24}$", re.I)

# A closed-status token under one of these is asserting OPENNESS, not closure.
# Without this guard the polarity repair introduces its own false negative: the
# heading vocabulary itself contains "not yet decided", so the most natural way
# to write a genuine disagreement -- "`A1-RI-04` is not yet decided" -- carries
# the token `DECIDED` and would have been read as a record of closure.
CLOSURE_NEGATION = re.compile(
    r"(?:NOT|NEVER|NO LONGER|NOT YET|YET TO BE|AWAITING|BEFORE|UNTIL|"
    r"PENDING|WITHOUT|UNLESS|IF)\W{0,12}$")

HEX64 = re.compile(r"[0-9a-f]{64}")

TABLE_SEPARATOR_CELL = re.compile(r"^:?-{2,}:?$")
BACKTICKED = re.compile(r"`([^`]+)`")


# ---------------------------------------------------------------------------
# Refusal -- the mechanism that makes "the check did not run" an observable
# ---------------------------------------------------------------------------

class Refusal(Exception):
    """A named refusal.  NEVER a finding, and never a bare traceback.

    Litmus defect D-6 in one sentence: a checker that aborts before evaluating
    any property has measured nothing, and a reader who meets its non-zero exit
    unaccounted records a false guard firing.  This type exists so that every
    such abort carries a token, a subject and the words "the check did not run".
    """

    def __init__(self, token: str, subject: str, reason: str) -> None:
        super().__init__(f"{token} {subject}: {reason}")
        self.token = token
        self.subject = subject
        self.reason = reason


# Process-level caches.  Nothing on disk is written during a run, and every
# mutation the selftest applies arrives through a Reader OVERLAY, which is
# consulted before any cache.  So these are safe, and they exist for one reason:
# `--selftest` performs 25 complete runs, and an instrument nobody will wait for
# is an instrument nobody runs.
_DISK_BYTES: dict[str, bytes] = {}
_PINNED_MODULES: dict[str, Any] = {}
_REVIEW_STATE: dict[str, str] = {}
_SOURCE_FACTS: dict[tuple[str, str], tuple[set[str], bool, set[str]]] = {}


class Reader:
    """Every byte this checker reads passes through here.

    The overlay exists so `--selftest` can mutate an input WITHOUT writing to
    the tree.  Freeze section 7.2 forbids editing reviewed bytes; a mutation
    suite that writes to disk to prove a guard fires is one interruption away
    from leaving the corpus mutated.  An overlay VALUE may also be an exception
    instance, which is how the refusal suite simulates an unreadable or absent
    input without touching the filesystem either.
    """

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

    def digest(self, rel: str) -> str:
        return hashlib.sha256(self.read_bytes(rel)).hexdigest()


class Result:
    """What one run produced, including what it did NOT manage to do."""

    def __init__(self) -> None:
        self.findings: list[dict[str, str]] = []
        self.observations: list[str] = []
        self.skips: list[dict[str, str]] = []
        self.counts: dict[str, Any] = {}

    def add(self, fid: str, statement: str, detail: str) -> None:
        self.findings.append({"id": fid, "statement": statement, "detail": detail})

    def skip(self, classes: str, token: str, subject: str, reason: str) -> None:
        self.skips.append({"classes": classes, "token": token,
                           "subject": subject, "reason": reason})

    @property
    def ids(self) -> set[str]:
        return {f["id"] for f in self.findings}

    @property
    def skipped_classes(self) -> set[str]:
        return {s["classes"] for s in self.skips}


EXIT_GREEN = 0
EXIT_FINDINGS = 1
EXIT_REFUSED = 2
EXIT_SELFTEST_NOT_RUN = 3
EXIT_INCOMPLETE = 4


def classify(result: Result) -> int:
    """Exit code from a completed run.  INCOMPLETE dominates FINDINGS.

    A partial run reported as "1 finding" understates itself: a reader cannot
    tell how much of the instrument was measuring.  Exit 4 says the run is not
    complete; the findings are still printed and are still real.
    """
    if result.skips:
        return EXIT_INCOMPLETE
    return EXIT_FINDINGS if result.findings else EXIT_GREEN


# ---------------------------------------------------------------------------
# Text shaping -- freeze section 7.7: formatting is part of the bytes
# ---------------------------------------------------------------------------

def fold_markdown(text: str) -> str:
    """Collapse markdown structure so containment is not defeated by layout.

    Freeze section 7.7 measures this as "the sharpest false-negative generator
    in the package": a byte-literal search for a phrase returns ABSENT because
    the phrase is wrapped, or blockquoted, or split across table cells.  It also
    records that whitespace normalisation ALONE is insufficient -- the freeze's
    own most load-bearing sentence is a blockquote and stays invisible until the
    `>` markers are folded too.  So fold quote markers, bullets, table pipes and
    trailing backslashes, then whitespace.
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
    """The paragraph or table row containing [start, end).

    A structural unit rather than a magic character count.  The predecessor used
    a 600-character window with no stated derivation; a block is derived from
    the document's own layout and does not need a number to justify.
    """
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
# Shared derivations
# ---------------------------------------------------------------------------

def decided_ids(packet: Any) -> dict[str, str]:
    """Decision ids the packet has actually closed, with their chosen rule.

    Read from `$.decisions` BY STATUS, never by position: an id parked in
    `$.pendingDecisions` is correctly open, and a narrative that calls it open is
    correct rather than in disagreement.
    """
    out: dict[str, str] = {}
    for key, value in (packet.get("decisions") or {}).items():
        if not isinstance(value, dict):
            continue
        if str(value.get("status", "")).strip().upper() in ("DECIDED", "CONFIRMED"):
            out[key] = str(value.get("rule", ""))
    return out


def closed_status_tokens(packet: Any) -> set[str]:
    """The packet's OWN vocabulary for "this is closed".

    Derived, not transcribed.  If the packet begins using a third status word
    for a closed decision, the polarity test below follows it without an edit --
    which is the difference between a gate and a copy of a gate.
    """
    tokens = set()
    for value in (packet.get("decisions") or {}).values():
        if isinstance(value, dict):
            status = str(value.get("status", "")).strip().upper()
            if status in ("DECIDED", "CONFIRMED"):
                tokens.add(status)
    return tokens or {"DECIDED", "CONFIRMED"}


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


def binds_implementer(line: str) -> bool:
    """True if some normative modal on this line is NOT an editorial aside.

    The predecessor graded CONTENT on `\\bmust\\b` anywhere on the line, for any
    reason.  Measured against that: inserting the two words "Readers must note:"
    into a row -- changing nothing the row asserts -- flipped its grade and
    raised a finding accusing the register of recording the wrong one.  The
    modal is now looked up together with the subject that governs it.
    """
    for m in NORMATIVE_MODAL.finditer(line):
        before = line[max(0, m.start() - SUBJECT_WINDOW):m.start()].rstrip()
        if not EDITORIAL_SUBJECT.search(before):
            return True
    return False


def records_closure(line: str, tokens: set[str]) -> bool:
    """True if this line RECORDS the decision as closed rather than open.

    `named_in` had no polarity, so a line saying a decision WAS DECIDED read
    identically to one saying it is open.  Both directions of that error are
    live: this admits the closure record, and the both-ways hard comparison
    against the register still catches the case where the closure record is a
    disguise, because a recorded disagreement whose derivation vanishes becomes
    an NPA-2 finding rather than silence.

    A NEGATED closed-status token is not a closure record.  That guard is not
    decorative: the unresolved-heading vocabulary this file already carries
    includes the phrase "not yet decided", so the plainest way to write a real
    disagreement contains the token `DECIDED`, and without the guard the
    polarity repair would silently delete the very rows NPA-1 exists to find.
    """
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

    KIND is derived, not judged: a line whose normative modal governs something
    other than the reader BINDS an implementer to the interim posture and is
    graded CONTENT; a line that only files a closed decision under an unresolved
    heading is graded STATUS.

    A document that cannot be READ is returned as a refusal rather than skipped
    silently.  The predecessor swallowed the OSError here, and the measured
    consequence was three FALSE `NPA-2` findings blaming the register for a
    document that was simply absent.  An unreadable input must never present as
    a measurement of the thing it was supposed to measure.
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
    """Hash-verify, then execute the verified bytes.  Never the other way round.

    Freeze section 7.3.  A mismatch raises `Refusal`, which the caller converts
    into a NAMED skip of exactly the classes that needed this module.  The
    predecessor raised `SystemExit(str)`, which Python renders as exit 1 -- its
    findings code -- while the message's own last words promised exit 2.
    """
    data = rd.read_bytes(rel)
    actual = hashlib.sha256(data).hexdigest()
    expected = EXECUTED_PINS[rel]
    if actual == expected and actual in _PINNED_MODULES:
        # Keyed on the DIGEST, never on the path: a run whose overlay supplies
        # different bytes for this path cannot be served a module built from
        # other bytes, so the cache cannot weaken the gate below.
        return _PINNED_MODULES[actual]
    if actual != expected:
        raise Refusal(
            "NPA-PIN-DRIFT", rel,
            f"live {actual} != pinned {expected}. This file EXECUTES that "
            f"instrument, so freeze section 7.3 requires the hash to hold before "
            f"the bytes run, and they were NOT run. If the drift is a deliberate "
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
    return module


# ---------------------------------------------------------------------------
# NPA-4 derivations
# ---------------------------------------------------------------------------

def ast_direct_tools(source: str) -> tuple[set[str], bool]:
    """({external argv[0] literals invoked by this source}, parsed_ok).

    An AST match, not a text scan, and that distinction is the whole of repair 2.
    The predecessor's regex matched a `curl` invocation's CHARACTERS wherever
    they occurred, including inside a module docstring describing another file
    and inside byte-string literals that are NEGATIVE PROBES asserting such code
    must be REFUSED.  Constants are not `Call` nodes, so they drop out here for
    free -- no file is named and no case is carved out.

    It is also STRICTLY WIDER than the regex in the directions that matter:
    `import subprocess as sp; sp.run([...])` and `from subprocess import run`
    were both invisible to the text predicate, and so is `os.system` /
    `os.popen`.  Measured across the corpus: zero live call sites of any of the
    three, so widening costs nothing today and closes the substitution a future
    author would reach for first.
    """
    try:
        tree = ast.parse(source)
    except (SyntaxError, ValueError):
        return set(), False

    aliases = {"subprocess"}
    bare: dict[str, str] = {}
    os_aliases = {"os"}
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
                    aliases.add(alias.asname or alias.name)
                elif alias.name == "os":
                    os_aliases.add(alias.asname or alias.name)
        elif isinstance(node, ast.ImportFrom) and node.module == "subprocess":
            for alias in node.names:
                if alias.name in SUBPROCESS_CALLS:
                    bare[alias.asname or alias.name] = alias.name

    tools: set[str] = set()
    for node in calls:
        func = node.func
        shell_string = False
        matched = False
        if isinstance(func, ast.Attribute) and isinstance(func.value, ast.Name):
            if func.attr in SUBPROCESS_CALLS and func.value.id in aliases:
                matched = True
            elif func.attr in OS_SHELL_CALLS and func.value.id in os_aliases:
                matched, shell_string = True, True
        elif isinstance(func, ast.Name) and func.id in bare:
            matched = True
        if not matched:
            continue
        first = node.args[0]
        if isinstance(first, (ast.List, ast.Tuple)) and first.elts:
            head = first.elts[0]
            if isinstance(head, ast.Constant) and isinstance(head.value, str):
                tools.add(head.value)
        elif isinstance(first, ast.Constant) and isinstance(first.value, str):
            words = first.value.split()
            if words:
                tools.add(words[0])
        elif shell_string:
            continue
    return ({t for t in tools
             if t not in INTERPRETER_ARGV0 and "executable" not in t}, True)


def text_direct_tools(source: str) -> set[str]:
    """Conservative fallback for a source the AST cannot parse.  Over-reports."""
    tools = {m.group(2) for m in EXTERNAL_CALL_TEXT.finditer(source)}
    return {t for t in tools if t not in INTERPRETER_ARGV0 and "executable" not in t}


def external_tool_closure(sources: dict[str, str]
                          ) -> tuple[dict[str, set[str]], list[str]]:
    """({checker filename: external binaries it needs}, unparsed filenames).

    Transitive.  `check-rust-provider-protocol-v4.py` contains no `rg` call: it
    compiles and executes v3, which does the same to v2, which shells out.  A
    census that read only direct call sites would report one dependent where
    three exist -- exactly the understatement this class was written to catch.
    """
    direct: dict[str, set[str]] = {}
    executes: dict[str, set[str]] = {}
    unparsed: list[str] = []
    names = set(sources)
    names_key = hashlib.sha256("\0".join(sorted(names)).encode()).hexdigest()
    for fname, src in sources.items():
        # Content-keyed, so `--selftest`'s 25 runs re-derive only the ONE source
        # a case mutated.  The key includes the peer-name set because `executes`
        # is a fact about this source AND about which other checkers exist.
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
        peers = set()
        # Only a file that compiles or exec's source can inherit another's calls.
        if "exec_module" in src or re.search(r"\bexec\(\s*compile\(", src):
            for other in names:
                if other != fname and re.search(
                        r"['\"]" + re.escape(other) + r"['\"]", src):
                    peers.add(other)
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
    when the section merely mentions it.  That distinction is not pedantic and
    was measured while this file was written: `jq` occurs TWICE and `curl` THREE
    TIMES in this section's PROSE today -- inside the paragraphs describing them
    as instrument false positives -- so a containment test over the section
    admits precisely the tool a reviewer proved could be added undetected.

    The tool column is located from the table's own header row rather than
    assumed at index 0, and the last-seen header governs subsequent rows so a
    continuation table without its own header is still read correctly.  If the
    table shape changes so that no header names a Tool column and no row parses,
    the declared set empties and every derived tool becomes a finding.  That is
    the same safe direction the section 5.1 register parser states for itself:
    an unreadable declaration is treated as absent, never as satisfied.
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
# NPA-5 / NPA-6 helpers -- carried forward; the review graded these the
# best-constructed pair and this successor changes only their error handling
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
    """The `<path>.py::<export>+...` string under a referenceDerivation.

    The key holds a bare string in some revisions and an object with an
    `implementation` member in others, so the shape is discovered rather than
    assumed -- a reader that assumed one would report the contract as having no
    reference derivation, which is a false negative on the very field this class
    depends on.
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
            # be a measurement of nothing presented as a verdict -- the exact
            # defect this successor exists to remove.  The skip above already
            # names it.
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
    for key, info in sorted(narrative_hits.items()):
        res.observations.append(
            f"{key[1]}: names decided `{key[0]}` under {info['heading']!r} "
            f"(grade {info['kind']}) — narrative, ranked last by freeze section 2 "
            f"and pre-resolved by the authority order; recorded here, not raised")


def check_npa_3(rd: Reader, res: Result, freeze_text: str, blueprint_text: str) -> None:
    try:
        pcm = load_pinned_module(rd, PCM, "npa2_pcm")
    except Refusal as exc:
        res.skip("NPA-3", exc.token, exc.subject, exc.reason)
        res.counts["subjectsGraded"] = None
        res.counts["subjectsRejected"] = None
        return

    subjects = [
        p for p in sorted(ARTIFACTS.glob("*.json"))
        if not any(mark in p.name.lower() for mark in pcm.REVIEW_MARKERS)
        and p.name in freeze_text and p.name in blueprint_text
    ]
    res.counts["subjectsGraded"] = len(subjects)

    def review_state(path: pathlib.Path) -> str:
        # Memoised because the executed derivation reads the review corpus from
        # DISK, not through the overlay -- so its answer cannot vary between
        # selftest cases, and recomputing it 25 times only costs time.
        key = str(path)
        if key not in _REVIEW_STATE:
            _REVIEW_STATE[key] = pcm.review_state_of(path)
        return _REVIEW_STATE[key]

    rejected = [p for p in subjects if review_state(p) == "REJECT"]
    res.counts["subjectsRejected"] = len(rejected)
    # Published because a reader wants to know WHICH artifacts carry a REJECT,
    # and because `--selftest` derives its NPA-3 fixture from this list rather
    # than naming an artifact in its own source.
    res.counts["subjectsRejectedNames"] = [p.name for p in rejected]

    tight: dict[str, int] = {}
    for path in rejected:
        stem = path.name[: -len(".json")]
        for doc, text in ((FREEZE, freeze_text), (BLUEPRINT, blueprint_text)):
            disclosed = False
            same_line = 0
            for m in re.finditer(re.escape(stem), text):
                block = fold_markdown(enclosing_block(text, m.start(), m.end()))
                for hit in re.finditer(r"REJECT", block):
                    before = block[max(0, hit.start() - 30):hit.start()]
                    if not REJECT_NEGATION.search(before):
                        disclosed = True
                        break
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
            # Self-excluded, as the predecessor was.  Stated rather than left
            # implicit, because an instrument omitting itself from its own
            # census is the shape freeze section 7.2.2 keeps catching.  What
            # makes it harmless here is a property, not an intention: this file
            # imports no `subprocess` and invokes no external binary at all, so
            # the excluded row is empty under any predicate. The exclusion
            # therefore removes nothing measurable -- it only avoids reporting
            # this instrument's own selftest fixtures as corpus dependencies.
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

    if unreadable:
        res.skip("NPA-4 over unreadable checker sources", "NPA-INPUT-UNREADABLE",
                 ", ".join(unreadable),
                 "a checker whose bytes cannot be read cannot be scanned for "
                 "external-tool calls, so this census is incomplete")

    if dependents and not env_section:
        # Explanatory, and deliberately NOT a short circuit.  Deleting the
        # section makes BOTH limbs' facts true at once -- nothing is declared
        # and nobody is named -- so reporting one of them and returning would
        # understate the damage by exactly the other limb.  Both run below.
        res.add("NPA-4-UNDECLARED-EXTERNAL-TOOL",
                "the blueprint has no environment-prerequisites section to declare in",
                f"{len(dependents)} checker(s) need an external binary and no heading "
                f"matching 'environment prerequisites' exists in {BLUEPRINT}; derived "
                f"tools {tools}. Every tool below is undeclared and every dependent "
                f"below is unnamed, because there is nowhere for either to be stated")

    # Limb 1 -- the class's NAME.  Repair 3: the tool itself must be declared.
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

    # Limb 2 -- what the predecessor actually tested, renamed to say so.
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
        contract = rd.read_json(D9_CONTRACT)
    except Refusal as exc:
        res.skip("NPA-5", exc.token, exc.subject, exc.reason)
        res.counts["oracleExports"] = None
        return

    ref = find_reference_derivation(contract)
    res.counts["oracleExports"] = 0
    if not ref or "::" not in ref:
        res.add("NPA-5-ORACLE-SIGNATURE-UNRECORDED",
                "the D9 contract no longer names a reference derivation",
                f"{D9_CONTRACT}: no `referenceDerivation` of the form "
                f"`artifacts/<checker>.py::<export>+<export>...` was found, so the "
                f"blueprint's port instruction has no subject to be checked against")
        return

    mod_rel, exports = ref.split("::", 1)
    mod_rel = mod_rel.strip()
    names = [n.strip() for n in exports.split("+") if n.strip()]
    res.counts["oracleExports"] = len(names)

    try:
        oracle_bytes = rd.read_bytes(mod_rel)
    except Refusal as exc:
        res.skip("NPA-5", exc.token, exc.subject, exc.reason)
        return
    actual = hashlib.sha256(oracle_bytes).hexdigest()

    # The expected digest is DERIVED from the package's own record, not
    # transcribed here: a pin copied into this file would advance silently when
    # the D9 head advances.  Freeze section 7.10 -- pin what you depend on and
    # re-extract it -- applied to a file the corpus expects to move.
    oracle_name = pathlib.PurePosixPath(mod_rel).name
    recorded: set[str] = set()
    for text in (freeze_text, blueprint_text):
        for hit in re.finditer(re.escape(oracle_name), text):
            window = text[max(0, hit.start() - 400): hit.start() + 400]
            recorded |= set(HEX64.findall(window))
    if actual not in recorded:
        res.add("NPA-5-ORACLE-SIGNATURE-UNRECORDED",
                "the D9 oracle on disk is not the one the package documents pin",
                f"{mod_rel}: live {actual}, recorded near its name {sorted(recorded)}")
        return

    module = importlib.util.module_from_spec(
        importlib.util.spec_from_loader("npa2_d9", loader=None))
    module.__file__ = str(COOP / mod_rel)
    try:
        exec(compile(oracle_bytes.decode("utf-8"), str(COOP / mod_rel), "exec",
                     dont_inherit=True), module.__dict__)
    except Exception as exc:                                # noqa: BLE001
        res.skip("NPA-5", "NPA-ORACLE-EXEC-FAILED", mod_rel,
                 f"{type(exc).__name__}: {exc}. The oracle's digest matched the "
                 f"package record, so this is not drift; the module did not run")
        return

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
        if literal not in blueprint_text:
            res.add("NPA-5-ORACLE-SIGNATURE-UNRECORDED",
                    "the blueprint tells an implementer to drive an oracle export "
                    "without recording the arity it actually has",
                    f"`{literal}` is the live signature and does not appear in "
                    f"{BLUEPRINT}. Driving it as the instruction reads raises "
                    f"TypeError before any golden is compared")


def check_npa_6(rd: Reader, res: Result, blueprint_text: str) -> None:
    try:
        resolved = rd.read_json(RESOLVED)
    except Refusal as exc:
        res.skip("NPA-6", exc.token, exc.subject, exc.reason)
        res.counts["preimageFields"] = None
        res.counts["goldenVectors"] = None
        return

    plan = resolved.get("planIdContract") or {}
    field_names = {f.get("name") for f in (plan.get("preimageFields") or [])
                   if isinstance(f, dict)}
    field_names.discard(None)
    vectors = ((plan.get("goldenVectors") or {}).get("positive") or [])
    res.counts["preimageFields"] = len(field_names)
    res.counts["goldenVectors"] = len(vectors)

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

    Everything narrower is converted into a NAMED skip on the Result, so the
    caller can always distinguish "this class did not run" from "this class
    found nothing".
    """
    res = Result()
    packet = rd.read_json(PACKET)
    freeze_text = rd.read_text(FREEZE)
    blueprint_text = rd.read_text(BLUEPRINT)

    check_npa_1_2(rd, res, packet, freeze_text)
    check_npa_3(rd, res, freeze_text, blueprint_text)
    check_npa_4(rd, res, blueprint_text)
    check_npa_5(rd, res, freeze_text, blueprint_text)
    check_npa_6(rd, res, blueprint_text)
    return res


# ---------------------------------------------------------------------------
# LIMITS -- freeze section 7.8, answered with a count and worked examples
# ---------------------------------------------------------------------------

LIMITS: tuple[dict[str, str], ...] = (
    {
        "id": "L-1",
        "lane": "NPA-1 (unrecorded disagreements only)",
        "limit": "the heading vocabulary is 7 alternatives and is exhaustive of "
                 "nothing",
        "worked": "Head a genuinely contradicting section 'Unsettled questions' "
                  "rather than 'Open decisions'. Measured by the independent review "
                  "with a matched control: the SAME normative section is CAUGHT "
                  "under 'Open decisions' and COMPLETELY MISSED under 'Unsettled "
                  "questions', and likewise under five further ordinary synonyms.",
        "why": "NOT CLOSED, and not claimed to be. For a RECORDED disagreement the "
               "both-ways hard comparison rescues it -- the review tried to break "
               "the class this way and could not, because all six rewrites produce "
               "NPA-2 findings instead of silence. Symmetry cannot rescue a NEW "
               "disagreement that was never recorded: nothing goes stale, so it is "
               "invisible in both directions. This successor narrows the DIAGNOSIS "
               "(NPA-2 now says when a document matched zero headings) and prints "
               "the vocabulary and per-document match counts, so the gap is legible "
               "rather than silent. It does not close it.",
    },
    {
        "id": "L-2",
        "lane": "NPA-1 (grade only, not existence)",
        "limit": "a genuine binding written without any of the eight modal forms "
                 "grades STATUS instead of CONTENT",
        "worked": "Write 'CI execution follows RI-LAYER4-CI-PROVISIONAL until "
                  "superseded' -- an imperative with no modal. The disagreement is "
                  "still FOUND and still compared to the register; only its grade is "
                  "understated, and a register row recorded at CONTENT then fires "
                  "NPA-1 for the grade mismatch.",
        "why": "Bounded by design: this limb can understate severity, never hide a "
               "disagreement.",
    },
    {
        "id": "L-3",
        "lane": "NPA-1 (polarity exclusion, new in this successor)",
        "limit": "a line that names one of the packet's closed-status tokens is "
                 "treated as recording the closure, so appending 'DECIDED' to an "
                 "otherwise contradicting line removes it from the derived set",
        "worked": "'`A1-RI-04` — DECIDED elsewhere, but an implementation must fail "
                  "admission until superseded' drops out of the derived set.",
        "why": "This is the price of repairing the reproduced polarity false "
               "positive, and it is paid asymmetrically: for a RECORDED "
               "disagreement the row's disappearance raises NPA-2, so the evasion "
               "converts one finding into another rather than into silence. For an "
               "UNRECORDED one it is a genuine new gap, and it is the same gap as "
               "L-1.",
    },
    {
        "id": "L-4",
        "lane": "NPA-3 (disclosure attribution)",
        "limit": "attribution WITHIN a block is not established -- a block naming "
                 "artifact X that separately reports artifact Y as REJECTED "
                 "satisfies the test for X",
        "worked": "Measured live: a freeze block naming `rust-provider-protocol.v2` "
                  "discloses via a sentence about `check-delivery-v4.py` being "
                  "'REJECT FOR REPAIR'. The disclosure is real but not attributed.",
        "why": "Narrowed, not closed. The window is now the enclosing block rather "
               "than an undisclosed 600-character constant, and negated REJECTs no "
               "longer count. The banner publishes rejectDisclosureSameLine so a "
               "reader can see how much disclosure is attributed rather than merely "
               "co-located, instead of being told a single boolean.",
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
               "fact is why v5's `rg` edge is correctly REPORTED and correctly NOT "
               "repaired -- the edge is real and only runtime substitution makes it "
               "inert. Recorded rather than chased.",
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
               "binds prose that asserts a JUDGEMENT. These two re-derive the "
               "measurement; they do not read the sentence next to it.",
    },
    {
        "id": "L-8",
        "lane": "the whole instrument",
        "limit": "it measures AGREEMENT between two statements of the same facts, "
                 "and holds no opinion about whether either is right",
        "worked": "Amend freeze section 5.1 to record a disagreement AND amend "
                  "`v1-slice.md` to contain it. Green, and the corpus still "
                  "contradicts the binding packet at authority level 2.",
        "why": "Freeze section 7.8's bound, in this instrument's vocabulary: a "
               "companion instrument converts an unverifiable attestation into a "
               "re-runnable check and converts neither into independent evidence. "
               "Whether a recorded disagreement is ACCEPTABLE is settled by freeze "
               "section 2's authority order, and whether the narrative gets amended "
               "by section 10.",
    },
)


_NUMBER_WORDS = {
    "ZERO": 0, "ONE": 1, "TWO": 2, "THREE": 3, "FOUR": 4, "FIVE": 5, "SIX": 6,
    "SEVEN": 7, "EIGHT": 8, "NINE": 9, "TEN": 10, "ELEVEN": 11, "TWELVE": 12,
}


def limits_count_disagreement() -> str | None:
    """"" if the docstring's published limit count equals the real one.

    Freeze section 7.2.2's rider: a measurement that cannot fail the build is
    prose.  This module's docstring publishes a COUNT of the ways it can be made
    to pass on a wrong artifact, and a count written in prose beside a list is
    exactly the figure that goes stale the first time the list is extended.  So
    the count is compared to the list, in both directions, and `--selftest`
    fails if they disagree -- the design the namespace successor used to stop
    its own disclosure going stale.
    """
    doc = __doc__ or ""
    m = re.search(r"the count is ([A-Z]+)", doc)
    if not m:
        return ("the module docstring no longer publishes a limit count in the form "
                "'the count is <WORD>', so nothing can be compared to len(LIMITS)")
    word = m.group(1)
    if word not in _NUMBER_WORDS:
        return f"the docstring publishes an unreadable limit count {word!r}"
    if _NUMBER_WORDS[word] != len(LIMITS):
        return (f"the docstring publishes {word} ({_NUMBER_WORDS[word]}) limits and "
                f"LIMITS carries {len(LIMITS)}")
    return None


def print_limits() -> None:
    print("LIMITS -- can I make this checker pass on a wrong artifact?")
    print(f"  YES, {len(LIMITS)} ways. Each is scoped to the lane it describes;")
    print("  none is printed under a heading broader than the class it affects.")
    print()
    for lim in LIMITS:
        print(f"  {lim['id']}  [{lim['lane']}]")
        print(f"      limit:  {lim['limit']}")
        print(f"      worked: {lim['worked']}")
        print(f"      status: {lim['why']}")
        print()


# ---------------------------------------------------------------------------
# Non-vacuity: every class must be shown to fire, from outside itself
# ---------------------------------------------------------------------------

def _bogus_register_row() -> str:
    return ("| `P-1` | `IMPLEMENTER-BLUEPRINT.md` | section 0 | `STATUS` | "
            "fabricated | x | x |\n")


def selftest() -> int:
    """Mutation suite, negative controls, and the hostile-input matrix.

    Freeze section 7.8's harder standard is "for every assertion, exhibit an
    input that is WRONG rather than merely EMPTY", and the predecessor's seven
    cases were all removals or corruptions.  The POSITIVE cases below keep those
    seven and add wrong-not-empty ones; the NEGATIVE controls assert that the two
    false positives the independent review reproduced no longer fire; and the
    REFUSAL matrix makes this file's own exit-code claims fail the build if they
    are false, which is freeze section 7.2.2's rider turned on this instrument.
    """
    try:
        base = run_check(Reader())
    except Refusal as exc:
        print(f"SELFTEST-REFUSED: base run refused -- {exc.token} {exc.subject}: "
              f"{exc.reason}")
        print("  The mutation suite DID NOT RUN. This is not a finding.")
        return EXIT_SELFTEST_NOT_RUN
    if base.skips:
        print("SELFTEST-REFUSED: base run is INCOMPLETE, so an admitted mutation "
              "cannot be distinguished from a class that never ran")
        for s in base.skips:
            print(f"  {s['token']} [{s['classes']}] {s['subject']}: {s['reason']}")
        return EXIT_SELFTEST_NOT_RUN
    if base.findings:
        print("SELFTEST-REFUSED: base is not green, so an admitted mutation cannot "
              "be distinguished from a pre-existing finding")
        for f in base.findings:
            print(f"  {f['id']}: {f['detail'][:160]}")
        return EXIT_SELFTEST_NOT_RUN

    rd0 = Reader()
    freeze_text = rd0.read_text(FREEZE)
    blueprint_text = rd0.read_text(BLUEPRINT)
    slice_text = rd0.read_text(SLICE)

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

    # The undeclared-tool fixture needs a checker whose FILENAME is already in
    # the environment section -- that is the precondition the reviewer's jq
    # demonstration exploited.  DERIVED, never named here, for two reasons.
    # First, a filename written into this file is a defect site written into the
    # instrument, which every class above is built to avoid.  Second and
    # measured: the transitive-closure heuristic this file inherits treats a
    # quoted checker filename in a source that also compiles code as an
    # execution edge, so hardcoding one made the PREDECESSOR attribute
    # `['curl','rg']` to THIS file and go exit 0 -> exit 1. An instrument must
    # not inject a synthetic edge into the census it participates in.
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

    # Likewise derived from NPA-3's own measurement rather than named here.
    reject_names = base.counts.get("subjectsRejectedNames") or []
    reject_stem = next((n[: -len(".json")] for n in reject_names
                        if n[: -len(".json")] in blueprint_text), "")
    if not reject_stem:
        print(f"SELFTEST-NOT-RUN: NPA-3 derived no REJECT subject named in "
              f"{BLUEPRINT}, so the disclosure-polarity case has no subject")
        return EXIT_SELFTEST_NOT_RUN

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
        "WRONG: add a register row for a disagreement that does not exist",
        {FREEZE: freeze_text.replace(
            register_marker.group(0),
            register_marker.group(0) + "\n" + _bogus_register_row(), 1).encode()},
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
        "NPA-4-UNDECLARED-TOOL-DEPENDENT",
        "EMPTY: rename the environment-prerequisites heading",
        {BLUEPRINT: (blueprint_text[: env.start()] + "#### Notes\n"
                     + blueprint_text[env.end():]).encode()},
    ))
    # The three probe sources below are ASSEMBLED from fragments rather than
    # written as literals, and the reason is MEASURED rather than stylistic.
    #
    # A text-scanning external-tool census reads raw source and cannot tell a
    # call from a string that merely looks like one -- that is repair 2's whole
    # subject.  Written verbatim here, these probes make every such census
    # attribute a `jq` dependency to THIS file.  Measured directly: with the
    # literal form present, the PREDECESSOR goes exit 0 -> exit 1 and reports
    # `externalTools ['curl','jq','rg']`, a phantom dependency sourced entirely
    # from this file's test data.
    #
    # So this is repair 2's own false-positive class arriving from the other
    # side, and the obligation runs the other way too: an instrument must not
    # inject a synthetic dependency into the corpus it measures. This file's own
    # AST predicate is immune either way -- these fragments are not Call nodes
    # under any spelling -- which is precisely why the assembly costs nothing.
    probe_tool = "jq"
    sp_call = "subprocess" + ".run"
    os_call = "os" + ".system"

    positives.append((
        "NPA-4-UNDECLARED-EXTERNAL-TOOL",
        "WRONG: add a real undeclared external-tool call to a checker whose "
        "FILENAME is already declared (the reviewer's jq demonstration -- the "
        "predecessor stayed green here)",
        {f"artifacts/{tool_source}": (
            "import subprocess\n"
            f"_PROBE = {sp_call}(['{probe_tool}', '-r', '.x'])\n"
            + tool_text).encode()},
    ))
    positives.append((
        "NPA-4-UNDECLARED-EXTERNAL-TOOL",
        "WRONG: the same call through an ALIASED import, invisible to the "
        "predecessor's text predicate",
        {f"artifacts/{tool_source}": (
            "import subprocess as _sp\n"
            f"_PROBE = _sp.run(['{probe_tool}', '-r', '.x'])\n"
            + tool_text).encode()},
    ))
    positives.append((
        "NPA-4-UNDECLARED-EXTERNAL-TOOL",
        "WRONG: the same call through a shell-string invocation, which no "
        "predicate here previously covered",
        {f"artifacts/{tool_source}": (
            "import os\n"
            f"_PROBE = {os_call}('{probe_tool} -r .x')\n"
            + tool_text).encode()},
    ))
    positives.append((
        "NPA-5-ORACLE-SIGNATURE-UNRECORDED",
        "CORRUPT: falsify a recorded oracle signature",
        {BLUEPRINT: blueprint_text.replace("derive_codes(ax, maps)",
                                           "derive_codes(ax)").encode()},
    ))
    positives.append((
        "NPA-6-IRREPRODUCIBLE-GOLDEN-UNRECORDED",
        "CORRUPT: falsify the recorded golden-vector completeness figure",
        # Every recorded figure at once: a vector recorded complete goes stale
        # (NPA-6's second branch) and one recorded incomplete loses its required
        # literal (the first).
        {BLUEPRINT: re.sub(r"carries (\d+) of (\d+) `PLAN-ID-V1` preimage fields",
                           r"carries 99 of \2 `PLAN-ID-V1` preimage fields",
                           blueprint_text).encode()},
    ))

    # ----- NEGATIVE controls: these must produce NOTHING ----------------------
    # Freeze 7.8 asks for inputs that are WRONG rather than EMPTY.  A repair to a
    # false positive needs the mirror of that: an input that is RIGHT and must
    # stay silent.  Both cases below were reproduced as findings by the
    # independent review against the predecessor.
    negatives: list[tuple[str, dict[str, Any]]] = []

    p1_row = None
    for line in slice_text.splitlines():
        if whole_token("P-1").search(line) and line.strip().startswith("|"):
            p1_row = line
            break
    if p1_row is not None:
        negatives.append((
            "CONTROL (IR-NPA-N1 incidental modal): insert 'Readers must note:' into "
            "a STATUS row -- asserts nothing new and must not flip the grade",
            {SLICE: slice_text.replace(
                p1_row, p1_row.replace("| ", "| Readers must note: ", 1), 1).encode()},
        ))
    negatives.append((
        "CONTROL (IR-NPA-N1 polarity): record a closure inside the unresolved "
        "section -- a line saying a decision IS DECIDED must not read as a "
        "line saying it is open",
        {SLICE: slice_text.replace(
            live_heading,
            live_heading + "\n\n| `G3-SUBSTRATE` | was DECIDED on 2026-08-05 by the "
            "product authority and is no longer open | closed |\n", 1).encode()},
    ))
    negatives.append((
        "CONTROL (modal synonym): rewrite the live CONTENT row's 'must' as "
        "'shall' -- the grade must survive a synonym swap in both directions",
        {SLICE: slice_text.replace("execution must follow",
                                   "execution shall follow", 1).encode()},
    ))

    # ----- REFUSAL matrix: this file's own exit-code claims, gated ------------
    # (label, overlay, expected exit code, expected token or None)
    good_pcm = rd0.read_bytes(PCM)
    refusals: list[tuple[str, dict[str, Any], int, str]] = [
        ("invalid packet JSON",
         {PACKET: b"{ this is not json"}, EXIT_REFUSED, "NPA-INPUT-MALFORMED"),
        ("required document missing (freeze)",
         {FREEZE: FileNotFoundError("No such file or directory")},
         EXIT_REFUSED, "NPA-INPUT-UNREADABLE"),
        ("required document unreadable (blueprint)",
         {BLUEPRINT: PermissionError("Permission denied")},
         EXIT_REFUSED, "NPA-INPUT-UNREADABLE"),
        ("required input undecodable (packet is not UTF-8)",
         {PACKET: b"\xff\xfe\x00binary"}, EXIT_REFUSED, "NPA-INPUT-UNDECODABLE"),
        ("per-class document missing (v1-slice.md)",
         {SLICE: FileNotFoundError("No such file or directory")},
         EXIT_INCOMPLETE, "NPA-INPUT-UNREADABLE"),
        ("executed pin drifted (check-package-coherence.py)",
         {PCM: good_pcm + b"\n# drift\n"}, EXIT_INCOMPLETE, "NPA-PIN-DRIFT"),
        ("executed pin missing",
         {PCM: FileNotFoundError("No such file or directory")},
         EXIT_INCOMPLETE, "NPA-INPUT-UNREADABLE"),
        # A no-op control.  NPA-PIN-EXEC-FAILED is deliberately unreachable
        # through this overlay: the hash gate runs FIRST, so any byte that would
        # make the module fail to execute has already failed the pin.  Verified
        # rather than assumed -- this case re-supplies the pinned bytes verbatim
        # and the run must be complete and green, proving the refusal cases
        # above are caused by their mutations and not by the harness.
        ("CONTROL: executed pin re-supplied verbatim -- must run complete and green",
         {PCM: good_pcm}, EXIT_GREEN, ""),
        ("per-class contract malformed (D9)",
         {D9_CONTRACT: b"{"}, EXIT_INCOMPLETE, "NPA-INPUT-MALFORMED"),
        ("per-class contract missing (resolved-inputs)",
         {RESOLVED: FileNotFoundError("No such file or directory")},
         EXIT_INCOMPLETE, "NPA-INPUT-UNREADABLE"),
    ]

    escapes = 0
    print(f"SELFTEST: {len(positives)} positive mutations, {len(negatives)} negative "
          f"controls, {len(refusals)} hostile inputs, against a green base")
    print()
    print("  PUBLISHED-FIGURE GATE -- this file's own disclosure must not go stale")
    disagreement = limits_count_disagreement()
    if disagreement:
        escapes += 1
        print(f"    [STALE] {disagreement}")
    else:
        print(f"    [AGREES] the docstring's published limit count equals "
              f"len(LIMITS) = {len(LIMITS)}")
    print()
    print(f"  POSITIVE -- each must be REJECTED by the class named for it")
    for expected, label, overlay in positives:
        try:
            found = run_check(Reader(overlay))
            ids = found.ids
        except Refusal as exc:
            ids = {f"REFUSED:{exc.token}"}
        ok = expected in ids
        if not ok:
            escapes += 1
        print(f"    [{'REJECTED' if ok else 'ADMITTED'}] {expected}")
        print(f"        {label}")
        if not ok:
            print(f"        -- produced {sorted(ids) or 'nothing'}")

    print()
    print(f"  NEGATIVE -- each must produce NO finding "
          f"(the reproduced false positives)")
    for label, overlay in negatives:
        try:
            found = run_check(Reader(overlay))
            ids = sorted(found.ids)
        except Refusal as exc:
            ids = [f"REFUSED:{exc.token}"]
        ok = not ids
        if not ok:
            escapes += 1
        print(f"    [{'SILENT' if ok else 'FALSE-POSITIVE'}] {label}")
        if not ok:
            print(f"        -- produced {ids}")

    print()
    print(f"  HOSTILE INPUT -- each must exit on the claimed code with a NAMED "
          f"token and no traceback")
    for label, overlay, want_exit, want_token in refusals:
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
        ok = got_exit == want_exit and token_ok
        if not ok:
            escapes += 1
        print(f"    [{'NAMED' if ok else 'WRONG'}] exit {got_exit} "
              f"(claimed {want_exit}) tokens {sorted(tokens) or 'none'}: {label}")

    print()
    if escapes:
        print(f"SELFTEST FAILED: {escapes} case(s) did not behave as claimed")
        return EXIT_FINDINGS
    print(f"SELFTEST PASSED: {len(positives)}/{len(positives)} mutations rejected by "
          f"the class named for each; {len(negatives)}/{len(negatives)} negative "
          f"controls silent;")
    print(f"  {len(refusals)}/{len(refusals)} hostile inputs refused on the claimed "
          f"exit code with a named token and zero tracebacks; base green.")
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
    "authorityDocsScanned", "unresolvedHeadingsMatched",
    "disagreementsDerived", "disagreementsRecorded",
    "subjectsGraded", "subjectsRejected", "subjectsRejectedNames",
    "rejectDisclosureSameLine",
    "checkersScanned", "checkersUnparsed", "checkersUnreadable",
    "externalToolDependents", "externalTools", "toolsDeclaredInEnvTable",
    "envDeclarationRows", "oracleExports", "preimageFields", "goldenVectors",
)


def report(rd: Reader, result: Result) -> int:
    print("NARRATIVE/PACKET AGREEMENT v2 -- package prose <-> the corpus it describes")
    print()
    print("  inputs read as data (no pin: these are the documents under comparison):")
    for rel in (PACKET, FREEZE, BLUEPRINT, SLICE, D9_CONTRACT, RESOLVED):
        try:
            print(f"    {rel:44s} {rd.digest(rel)}")
        except Refusal as exc:
            print(f"    {rel:44s} <{exc.token}: {exc.reason[:60]}>")
    print()
    print("  input executed after hash verification (freeze section 7.3):")
    for rel, pin in EXECUTED_PINS.items():
        print(f"    {rel:44s} {pin}")
    print("    NOTE: freeze section 7.6 lists that file among the five checkers")
    print("    carrying no current-byte pin -- i.e. among the few still editable, and")
    print("    its worked example is a sibling in that list whose edit silently")
    print("    invalidated eleven review artifacts. If it moves, NPA-3 alone is")
    print("    SKIPPED by name and this run exits 4; the other five classes continue.")
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
            print(f"    {key:26s} {value}")
    print()
    print("  NPA-1 reach -- the heading vocabulary that defines what it can see:")
    for term in UNRESOLVED_HEADING_TERMS:
        print(f"    /{term}/i")
    print("    This list is exhaustive of nothing. See --limits L-1: a reworded")
    print("    heading is caught for a RECORDED disagreement by the both-ways")
    print("    comparison and is invisible for an UNRECORDED one.")

    if result.observations:
        print()
        print("  observations (narrative scope -- not findings):")
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
        print("  derived external tool is declared and every dependent named, and every")
        print("  document claim above equals the measurement it describes.")
    elif exit_code == EXIT_INCOMPLETE:
        print(f"INCOMPLETE: {len(result.skips)} class(es) did not run; "
              f"{len(result.findings)} finding(s) from the classes that did.")
    print("  scope: agreement only. Says nothing about whether a recorded")
    print("  disagreement is ACCEPTABLE -- freeze section 2's authority order decides")
    print("  that, and section 10 decides whether the narrative gets amended.")
    print("  Run --limits for the eight ways this instrument can be made to pass on a")
    print("  wrong artifact, each scoped to the class it affects.")
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
