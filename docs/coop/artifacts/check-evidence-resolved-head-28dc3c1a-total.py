#!/usr/bin/env python3
"""Retained validator for the RESOLVED HEAD of the EVIDENCE identity lineage.

TOTAL over hostile parsed JSON.  Successor to
`check-evidence-resolved-head-28dc3c1a.py` (`e01d3524…`), which its independent
review REJECTED at one blocker (`IR-EVRH-B1`).


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
what makes a successor instrument the propagation mechanism.  The predecessor's
bytes are reviewed and therefore frozen; a successor is the only repair
mechanism available.


THE NAME
--------
THE RULE (D-001 NOTE-1, adopted as a standing instruction): a checker's version
number is ITS OWN, never its subject's.  `check-evidence-v11.py` already exists
and it is *evidence.v10*'s checker -- the eleventh instrument of the
`check-evidence` lineage, re-pointed at the DECIDED `CD-RT-5` product state.  It
is NOT a checker of `evidence.v11`.  That collision is the corpus's recorded
naming trap.

THE PREDECESSOR DEFEATED THE TRAP STRUCTURALLY and this file does not undo that.
`28dc3c1a` is the sha256 prefix of the subject `evidence.v15.json`.  A digest
prefix cannot be misread as a version number in either direction, so the trap is
structurally unavailable rather than merely avoided.  THE SUBJECT HAS NOT
CHANGED -- it is still `evidence.v15` at `28dc3c1a…`, measured at authoring --
so dropping or altering the content address would make the name assert a subject
this file does not have.  It is therefore carried unchanged.

THE SUCCESSOR DISCRIMINATOR IS A PROPERTY WORD, NEVER AN ORDINAL:

    check-evidence-resolved-head-28dc3c1a-total.py

  * `-total` names exactly what this generation adds and nothing else: the
    checking layers are TOTAL over hostile parsed JSON.  That is `IR-EVRH-B1`'s
    repair and it is the whole reason this file exists.
  * It carries NO digit, so it cannot read as a subject version in either
    direction -- which is the property `-vN` does not have and the reason
    D-001 NOTE-1 exists.  The instruction "do not introduce a `-vN` token that
    could read as a subject version" is satisfied by construction: there is no
    numeric token at all.
  * The discipline generalises without ever needing an ordinal: each successor
    takes a word for the property it repairs, so the namespace does not run out
    and no reader ever has to decide whether a number is an instrument ordinal
    or a subject version.
  * MEASURED at authoring, not assumed: `ls check-evidence*` in
    `docs/coop/artifacts/` yields `check-evidence.py`, `check-evidence-v4.py`
    … `check-evidence-v11.py`, `check-evidence-resolved-head-28dc3c1a.py` and
    that file's review.  This name collides with none of them, and with no
    subject version.
  * When the lineage advances this name goes STALE-BUT-HONEST: it still names
    exactly the bytes it was built to validate.

The content-addressed form follows the corpus's own precedent: the CONTENT
identity branch of `check-completeness-v2.py::declaration_fields` already holds
that "a name is redundant when a digest is present -- the digest IS the
identity".


CHANGE RECORD -- WHAT CHANGED, WHY, AND WHAT IT MEASURES
--------------------------------------------------------
The predecessor was independently reviewed
(`check-evidence-resolved-head-28dc3c1a.review-independent.json`, `5ad6b9a6…`,
REJECT, 1 blocker + 6 advisories).  Every finding is dispositioned here.

`IR-EVRH-B1` (BLOCKER) -- the checking layers were not total over hostile
parsed JSON.  Three sites raised uncaught exceptions that terminated as a raw
traceback at exit 1 -- the code the instrument's own EXIT table reserves for
FINDINGS -- with zero findings and no banner, which is freeze section 7.8.1's
litmus defect D-6.  REPRODUCED HERE BEFORE REPAIR, on a disposable /tmp tree
copy, with no re-pinning: writing the two bytes `[]` over `evidence.v15.json`
gave EXIT=1, first line `Traceback (most recent call last):`, 0 stdout lines,
0 findings, 0 banner lines.  REPAIRED BY ARCHITECTURE, NOT BY THREE PATCHES.
The resolved head's own `pathConsumerGuard.predecessorDefect` states why a
per-site fix is the wrong shape: "A per-site fix would not have prevented a
fourth site, so the property is enforced over the whole reachable closure
instead."  And it was right: driving the sweep to zero surfaced a FOURTH and a
FIFTH site the review had not named -- `read_document` letting any non-JSONDecode
parse failure through, and the REVIEWED gated resolver bytes raising on a
non-object candidate this instrument handed them.  SIX independent mechanisms,
each separately measured:

  1. TOTAL ACCESSORS (section 5 below).  A closed, named set of primitives that
     are total over ANY parsed value.  Every checking layer consumes
     candidate-supplied values through them and never through a raw mapping
     method.  This is the root-cause repair: the three named sites were three
     instances of one habit, not three bugs.
  2. THE LAYER TOTALITY NET.  Every checking layer is invoked through ONE
     dispatcher, `run_layer`, which converts any unexpected exception into a
     typed `EVRH-TOTAL-01` finding.  This implements the resolved head's
     `hostileInputTotalityContract.exitDiscipline` first sentence verbatim --
     "An unexpected exception inside a layer becomes a reported finding and
     exit 1" -- and it is the backstop for a site nobody foresaw.
  3. THE INPUT GATE.  `read_document` refuses a REQUIRED input whose parsed
     root is not a JSON object, and refuses any parse failure at all, raising
     `Malformed` -> exit 2, "THE CHECK DID NOT RUN".  That is freeze section
     7.8.1 rule 2 and the disposition this file's own exit table already
     promised.  The refusal names the file, the shape measured, and -- when it
     is also true -- the digest mismatch, so a reader is never told only half
     of what is wrong.
  4. THE GATED-RESOLVER BOUNDARY.  `gated_call` wraps every invocation of the
     reviewed resolver bytes.  Those bytes are frozen (freeze sections 7.2/7.6)
     and their totality is not this instrument's to change -- handed a candidate
     whose root is not a JSON object they raise `AttributeError` -- but THE
     BOUNDARY IS THIS INSTRUMENT'S.  An exception from inside them becomes a
     typed `EVRH-GATE-02` finding naming the resolver, the shape handed to it,
     and the class that consequently did not run.  It is a FINDING, not an
     integrity failure: `EVRH-GATE-01` stays reserved for the trust root at
     exit 4.  This mechanism was NOT in the review's prescription; it was found
     by driving the sweep to zero, and it accounted for the last 39 escapes.
  5. THE GUARD SCAN (`EVRH-GUARD-01`), a syntactic tripwire over the layer
     closure.  It found six raw-consumption sites in this file's own first
     draft, which is the whole reason it exists.
  6. THE INJECTION SWEEP, in `--selftest`.  The ORACLE.  It calls the UNGUARDED
     layer functions directly, so mechanisms 2 and 4 cannot mask an escape, and
     it requires ZERO unguarded escapes.  See section 6.

  MEASURED, before and after, by the same harness at the same boundary (the
  resolved head's own 16-name injection vocabulary,
  `hostileInputTotalityContract.injections`; `evidence.v11`…`v15` enumerated at
  EVERY path at unlimited depth, `evidence.v10.json` at depth <= 1 only):

      PREDECESSOR  6351 executed cases, 145 escaping cases, 540 escape
                   records (case x layer) over 10 swept layers, across 8
                   distinct (layer, exception) signatures -- every one an
                   AttributeError or a TypeError.
      THIS FILE    the same 6351 executed cases, over 12 swept layers (a
                   SUPERSET: `check_head_leaves` and `check_path_domain` are
                   new), 0 escaping cases, 0 escape records, 0 signatures.

  The 12-layer figure is the external harness's.  The sweep SHIPPED in this
  file's `--selftest` drives the same table `validate` drives -- 7 chain layers
  plus 4 resolution layers, pinned as `LAYER_CENSUS` and hard-compared by
  `EVRH-HOSTILE-04` so a layer cannot enter the run without entering the sweep
  -- and measures the same 6351 cases at 0 escapes, over 41,641 unguarded layer
  invocations.

  ONE DEFECT THE SWEEP FOUND IN ITSELF, recorded because an unrecorded
  self-correction is the thing freeze section 7.2.2 exists to catch: the first
  build used `None` as the "injection does not apply here" sentinel, which
  collided with `null` -- one of the head's own sixteen classes -- at the ROOT
  position, silently dropping the single most important case in the sweep.  The
  census read 6,345.  With a distinct sentinel it reads 6,351, and the six
  recovered cases are exactly `null` at the root of each of the six chain
  files.

  The two counting units are both reported because they answer different
  questions: an escaping CASE is one hostile document that produced at least one
  traceback; an escape RECORD is one (case, layer) pair.  The review's own
  census is 122 escapes over 6,801 executed cases; its per-file breakdown
  (21/23/21/21/21/15) sums to 122 exactly, and its per-file case counts
  (748/1277/1292/1292/1372/704) sum to 6,685 rather than to the 6,801 it
  recites.  Neither the review's case total nor its exact literal injection
  values are reproducible from the head (the head names the sixteen injection
  CLASSES, not their literals), so this file does not claim to have re-run the
  review's sweep byte-for-byte.  It re-runs the review's METHOD at the review's
  stated boundary with the head's declared vocabulary and reports its own
  numbers, hard-compared, in both units.

`IR-EVRH-A1` (ADVISORY-HIGH, the C-2 v9 reparenting class) -- `leaf_paths`
joined path steps with an unescaped `/`, so a key literally named
`acceptedGolden/evidenceDigest` collided with the real path
`/acceptedGolden/evidenceDigest` and the later leaf silently overwrote the
earlier one, suppressing `EVRH-ACCT-03`.  REPRODUCED HERE BEFORE REPAIR with the
review's own mutant and its A/B control, on a disposable /tmp copy with the head
re-pinned: MUTANT (digest move plus the colliding key, publishing
`digestsMoved: 0`) gave finding classes `['EVRH-CANON-01']`; CONTROL (identical
digest move, no colliding key) gave `['EVRH-ACCT-03', 'EVRH-CANON-01']`.  The
collision, and only the collision, suppressed `EVRH-ACCT-03`.  REPAIRED with the
corpus's own recorded one-line repair, the shape freeze section 3's C-2 row
names: paths are no longer text joins.  A path is a LIST OF STEPS and its
identity is `j_canon` of that list -- the LENGTH-FRAMED, type-tagged, INVERTIBLE
encoding `check-c2-v9.py::jx_canon` already carries.  Injectivity is not
asserted: `j_decanon` inverts `j_canon`, the round trip is EXECUTED on every run
over every path the run emits plus a fixed witness set that includes this exact
collision pair, and the existence of the left inverse is the proof (if
`j_canon(a) == j_canon(b)` then `a = j_decanon(j_canon(a)) = j_decanon(j_canon(b))
= b`).  `EVRH-PATH-01` reports a failed round trip; the battery's
`reparenting-collision` mutation is the review's mutant shipped as a standing
probe and now requires `EVRH-ACCT-03`.

`IR-EVRH-A2` (ADVISORY) -- five head leaves were bound only by the head digest
pin, with the coverage boundary undisclosed.  REPAIRED: `EVRH-HEAD-02` binds all
five named leaves (`purpose`, `whatThisDoesNotDo`, `derivedFrom.rule`,
`derivedFrom.resolutionChain`, `operationAccounting.whyNoDigestMoves`) by
required substring against the accepted bytes, so a falsification with path and
JSON type unchanged is caught by NAME rather than only by the whole-document
pin.  The remaining boundary is DISCLOSED rather than closed, in section 7 and
in the `notMeasured` channel: the 34 top-level keys of the resolved contract
outside the 9 digest-pinned sections carry no per-section digest and no semantic
check (43 top-level keys measured, 9 pinned).

`IR-EVRH-A3` (ADVISORY) -- the shipped battery exercised 14 of 36 typed classes,
and the review had to fire the other 22 by hand to establish that none was
vacuous.  REPAIRED by moving that measurement INTO the instrument, where the
next reader does not have to go and find a verdict to know it.  The battery goes
from 8 artifact mutations to 17, the source self-mutations from 4 to 5, the gate
probe from 1 shape to 7; and three input-refusal shapes, the injection sweep and
a CLASS-COVERAGE PROBE are added.  The coverage probe fires, BY DIRECT CALL
against a planted input, every class no artifact mutation can reach -- 32 direct
probes -- and then requires that EVERY class this file declares is required by
some probe in the shipped suite.  The declared classes are READ FROM THIS FILE'S
OWN SYNTAX TREE, never transcribed, so the coverage claim cannot drift from the
code.  MEASURED: 51 declared classes, 51 covered, 0 uncovered, 0 misfires; total
suite census 34/34.  The `EVRH-PATH-01` probe is worth naming: it fires the
check against THE PREDECESSOR'S OWN `/`-join encoder, retained in these bytes as
`naive_join_encode` and used for nothing else, so the injectivity check is shown
to fire on the exact defect `IR-EVRH-A1` names.

`IR-EVRH-A4` (ADVISORY) -- the gate probe was narrower than the gate it
certifies (one resolver, one failure mode).  REPAIRED: `_run_gate_probe` now
executes all SEVEN shapes the review measured by hand -- digest mismatch on each
of the two gated resolvers, ABSENCE of each, a directory in place of the file,
non-UTF-8 bytes, and an empty file -- and every one must refuse with
`EVRH-GATE-01` naming the file and its gated pin, with no validation attempted.

`IR-EVRH-A5` (ADVISORY-MINOR) -- `--emit-resolved` writes the canonical bytes
plus a terminator newline and the header named the payload but not the
terminator.  REPAIRED as a MEASUREMENT rather than as a sentence: both digests
are pinned and recomputed on every run by `EVRH-CANON-03`.  The emitted stream
is exactly `canonical_bytes(resolved)` followed by ONE `b"\\n"`.  Payload
sha256 = `4976151e6ccfd6fd25487e2ebf9e20af3b971e5bc4879b66f11b11c43ba3c573`
(the pin).  WHOLE-STREAM sha256, terminator included, =
`b56fe8199610e2d94656273cdeb33bcf3c6616fa095b01e3ab7d6efae90883a0`, and the
stream is 163,785 bytes.  A reader who pipes the stream into `sha256sum`
reproduces the whole-stream value; the pin is reproduced by stripping the final
newline.  Both are measured here, so neither can drift into prose.

`IR-EVRH-A6` (ADVISORY-RECORD-ONLY) -- self-scan disclosure at or wider than its
measured boundary.  CARRIED FORWARD UNNARROWED and WIDENED by the three evasion
forms the review measured and named individually (`globals()["selftest"](root)`,
`getattr(sys.modules[__name__], "selftest")(root)`, and a dict dispatch table);
all three fall inside the general alias clause already disclosed, and naming
them individually makes the disclosure strictly wider.  Nothing here is claimed
closed.  Section 7 states it.

NOT DEFERRED, NOTHING DEFERRED BY NAME.  Every blocker and every advisory is
repaired in these bytes.  What is DISCLOSED rather than repaired is stated as a
residual in section 7 with the surface that owns it; a disclosure is not a
deferral of a finding, it is the finding's honest boundary.


1. THE GATED RESOLVER BYTES (freeze section 7.10 lesson)
--------------------------------------------------------
This instrument does not reimplement the corpus resolver.  It EXECUTES the two
reviewed resolvers, and it PINS THEM BY DIGEST first:

    check-completeness.py     af9f8837a5abc561cefebf071b862e2dd5fb427304f4738f7fadf5872c4f0f1f
    check-completeness-v2.py  dbe1e6955f66b0ccb032df115ca03fa780895b129b51fb39a49593581901bfb9

Both digests were MEASURED at authoring against the live tree AND independently
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
`check-retention-custody-v28.py` now permanently refuses because the
dialect-repaired resolvers moved under its gated pins, and the recorded reading
is "correct section 7.8.1 behavior, not a defect", with a successor that gates
the reviewed bytes named as the repair.  This file IS that successor pattern
applied to the EVIDENCE surface.  Section 7.8.1 rule 1 is the whole of it: a
missing or altered REQUIRED input must refuse, never proceed on a default,
because "derived from nothing" and "derived and found nothing" must never print
the same.

The verified bytes are executed from the SNAPSHOT that was hashed -- compiled
from the same `bytes` object that produced the digest -- so the bytes verified
and the bytes executed cannot diverge across a second read.  Each gated resolver
is read EXACTLY ONCE per run, so there is no TOCTOU window between the
measurement and the execution.


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

A green run of this file is AUTHOR-SIDE evidence.  It is not a review and it is
not "this artifact is right".

WHAT THIS INSTRUMENT DOES NOT DO, enumerated so no reader has to infer it:

  * It has NO claim-register motion authority.  It moves nothing in
    `claim-register.v1.json`, grants no seal, no freeze, no application, no
    product acceptance, and does not sign `CD-RT-5`.
  * It is NOT the section 3.1 Phase-1A packet and supplies no part of it.
  * It is NOT a review.  Independent review of these instrument bytes remains
    REQUIRED.
  * It does not adjudicate `evidence.v15`'s findings, does not apply it, and
    does not change its `CANDIDATE-NOT-APPLIED` / `DO-NOT-SEAL` posture.  It
    ASSERTS that posture and fails if it silently moves.
  * It measures nothing about production durability, atomicity, restart, crash
    or concurrency behaviour.
  * It does not adjudicate its own predecessor.  The predecessor's review stands
    on the predecessor's bytes; this file repairs, it does not overturn.

SELF-SCANS ARE TRIPWIRES; THE EXECUTABLE PROBES ARE THE ORACLE.  The resolved
head's `retainedResiduals[13]` is binding on this instrument and is restated
here in its own words: the source self-scans (`EVRH-MODE-05/06/07`,
`EVRH-GUARD-01`) prove properties of THIS FILE'S SYNTAX, never of its semantics.
They are drift tripwires for their measured coverage only.  The executable
probes -- the chain resolution, the recomputed digests, the mutation battery,
the injection sweep -- are the semantic oracle.


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

Exit 4 discharges an obligation the head binds on its successor: the head's
`exitDiscipline` states "The successor instrument for this artifact MUST
terminate trust-root integrity failures at a distinct declared exit code; this
sentence binds that obligation on the successor without renumbering the four
dispositions the retained checker implements."  Exit 4 is that distinct code;
0-3 are unrenumbered.

RULE 3 IS NOW KEPT ON EVERY PATH, WHICH IS WHAT `IR-EVRH-B1` MEASURED AS BROKEN.
`ONE` function, `run_validation`, is the single place a validation failure
becomes an exit disposition, and both `main()` and the selftest's
input-refusal probe drive it, so the code a document CLAIMS and the code the
file PRODUCES are the same bytes and are measured, not read.

ENTRYPOINTS AND FLAGS.  Two declared flags, the same argument discipline the
head declares: exactly one optional positional candidate path; a second
positional, an unknown flag, a candidate path supplied alongside the emission
mode, and both modes at once are each refused with exit 2 and a NAMED reason
rather than silently ignored; a repeated declared flag is accepted under set
semantics and asserts nothing.

    python3 -I -B artifacts/check-evidence-resolved-head-28dc3c1a-total.py
    python3 -I -B artifacts/check-evidence-resolved-head-28dc3c1a-total.py --selftest
    python3 -I -B artifacts/check-evidence-resolved-head-28dc3c1a-total.py --emit-resolved

ONE DEPARTURE, REPORTED RATHER THAN IMPROVISED, and carried unchanged from the
predecessor.  The head's second declared flag is `--emit-candidate`, which in the
retained checker emits a WHOLE-OBJECT DERIVATION of the successor from pinned
bytes.  This instrument holds no such derivation authority: it validates a
resolved head, it does not author one.  The DISCIPLINE is implemented exactly
(two declared flags, mutually exclusive, the emission mode takes no positional
path); the flag's NAME and payload differ -- `--emit-resolved` writes the
resolved effective contract's canonical bytes plus exactly one terminator
newline, both digests pinned and recomputed (see `IR-EVRH-A5` above).  This is
the one clause of the head's contract not implemented verbatim and it is named
here, not hidden.

SELFTEST REACHABILITY, per the head's clause and
`reviewFindingTransfers[33].closure`: there is no unconditional finding gate
before the mutation suite and no second undocumented selftest entrypoint.  Both
clauses are enforced over this file's own syntax tree by the DELIBERATELY
NARROWED comparison-node flag scan the transfer describes.  `--selftest` always
reaches the suite.  A dirty base refuses at exit 3, because a mutation suite
over a red base is not an oracle.


4. DISCIPLINES
---------------
python3 -I -B enforced at line 1; standard library only; no network; no writes
anywhere outside disposable per-probe copies under /tmp; deterministic output
ordering (every census sorted); every pin a full sha256; every check carries a
typed finding ID and a stated invariant; findings are scored as FINDING-SET
DELTAS, never as bare exit codes.

Duplicate-key discipline, and the one distinction that matters: a document that
is not JSON at all, that cannot be read, or WHOSE PARSED ROOT IS NOT A JSON
OBJECT, is an INPUT failure -> exit 2 (the head's "an input that cannot be read
or parsed exits 2", and freeze section 7.8.1 rule 2).  A document that IS a
valid JSON object but repeats a key is HOSTILE INPUT, not an unreadable one: it
is a typed finding (`EVRH-DUP-01`) naming the file and the key, analysis
continues on the permissive parse so the remaining classes are still measured,
and the run cannot exit 0.  Freeze section 7.5 measured this class across the
checker corpus; every file this instrument reads is parsed through the
rejecting hook.

Type exactness follows freeze section 7.2.2 and section 7.4 throughout: `True`
is not `1`, `1` is not `1.0`.  `j_type` decides `boolean` BEFORE `integer`
because `isinstance(True, int)` is true in the host language and that single
fact is the root of the whole class.  Every declared measurement is
hard-compared to the measurement it records; an uncompared recorded measurement
is prose that looks like evidence.


5. THE TOTALITY ARCHITECTURE (the `IR-EVRH-B1` repair)
-------------------------------------------------------
TOTAL ACCESSORS.  `j_type`, `m_get`, `m_has`, `m_obj`, `m_seq`, `m_keys`,
`m_items`, `m_str` and `m_text` are total over EVERY Python value, not merely
over well-shaped JSON.  They are the ONLY place in this file where a raw mapping
method appears, and that exemption is PAID FOR by
`check_accessor_totality`, which fires each of them against the head's sixteen
injection classes plus values outside the JSON universe and requires that none
raises.  A named exemption backed by a measurement is a contract; a named
exemption backed by nothing is a hole.

THE LAYER TOTALITY NET.  `run_layer` wraps every checking layer.  An unexpected
exception becomes `EVRH-TOTAL-01` and exit 1 -- the head's exitDiscipline first
sentence, implemented.  `TrustRootIntegrityError` is the one exception it
re-raises, because that failure is NEVER a finding: nothing was measured, the
check did not run, and it terminates at exit 4.

THE GUARD SCAN (`EVRH-GUARD-01`), modelled on the head's own `pathConsumerGuard`
and disclosed to the same standard.  THE SCAN'S MAP, stated exactly:
reachability ROOTS are the functions named in `GUARD_ROOTS`; the collector
follows DIRECT-NAME calls to PLAIN SYNCHRONOUS module-body function definitions
and, within a reached function, DESCENDS into nested definitions.  Indirection
of any form is invisible to it.  RECOGNISED UNGUARDED FORMS, exactly two:
(a) an `ast.Call` whose `func` is an `ast.Attribute` whose `attr` is one of
`get`, `items`, `keys`, `values`, `setdefault`, `pop` -- a raw mapping method
where a total accessor belongs; (b) an `ast.Call` to the name `sorted` with a
single positional argument that is a bare lowercase `ast.Name`, an
`ast.Attribute` or an `ast.Subscript` and NO `key=` keyword -- which is exactly
the `sorted()`-over-mixed-key-types shape that was the predecessor's third
site.  The `TOTAL_ACCESSORS` bodies are EXEMPT and are the only exemption.
SUBSCRIPTS ARE NOT SCANNED, and no recurrence guarantee is stated beyond this
map.  Sites outside it are governed by the ORACLE below and by review, never by
this scan.  IT IS NOT DECORATIVE: run against this file's own first draft it
reported six unguarded consumption sites -- two keyless `sorted()` calls in
`check_grammar`, a raw `.get()` in `check_residuals`, two raw `.items()` calls in
`check_transfers`, and a `.pop()` in `leaf_paths` -- and all six were repaired
before this file measured anything.  The `.pop()` was a LIST pop and therefore a
false positive of a deliberately narrow scan; the walker was rewritten to use
index arithmetic rather than widening the scan's bright line, because a scan
that is argued with is a scan that stops working.


6. THE INJECTION SWEEP -- THE ORACLE FOR TOTALITY
--------------------------------------------------
`--selftest` executes the resolved head's own hostile-input space against THIS
file's UNGUARDED layer functions.  It bypasses `run_layer` deliberately, so the
totality net cannot mask an escape -- the head's own generator clause requires
exactly this ("The selftest calls the unguarded checking layers directly, so a
broad exception handler cannot mask an escape").

VOCABULARY: the head's `hostileInputTotalityContract.injections`, all sixteen
names, READ FROM THE RESOLVED BYTES and hard-compared against the sixteen this
file implements (`EVRH-HOSTILE-02`), so the vocabulary cannot drift from its
source.  Fifteen are VALUE injections and `unknown-key` is the structural one,
applied at object positions; that split is this file's reading of the head's own
`measurement.injectionValues: 15` alongside a sixteen-name list, and it is
stated here rather than assumed silently.

BOUNDARY, STATED EXACTLY: `evidence.v11` … `evidence.v15` are enumerated at
EVERY path at unlimited depth, at every object key and every array index,
container positions and scalar leaf positions alike, plus the root.
`evidence.v10.json` is enumerated at depth <= 1 ONLY (44 of its paths), which is
the review's own boundary, carried so the before/after numbers compare.  An
injection whose canonical bytes equal the original is not hostile input and is
skipped and counted, never reported as a case.

A layer whose OWN ARGUMENTS are byte-identical to the clean baseline cannot
behave differently from the clean baseline, which raised nothing; those
invocations are counted as UNAFFECTED and skipped.  Every layer takes exactly
the documents it consumes as its arguments, so "unaffected" is a structural
fact about the call, not a judgement about the body.

ESCAPE DEFINITION, and the control that rules out misattribution: an escape is
any exception outside this file's DECLARED exception set (`Malformed`,
`UnsupportedInvocation`, `TrustRootIntegrityError`, `DuplicateKeyError`) raised
by an unguarded layer.  Those four are this instrument's OWN typed refusals and
are correct behaviour; counting them would inflate the census with the
instrument working as designed.  `EVRH-HOSTILE-01` fires on any escape.


7. RESIDUALS -- DISCLOSED, NOT CLOSED
--------------------------------------
  * THE 34 UNPINNED TOP-LEVEL KEYS.  The resolved contract carries 43 top-level
    keys; 9 are digest-pinned per section.  The other 34 are covered by
    `RESOLVED_CANONICAL` as a whole-document pin and carry no per-section digest
    and no semantic check.  A re-gate for a new head moves that pin, and after a
    re-gate those 34 keys are bound by nothing here.  Owning surface: the
    EVIDENCE head itself.
  * THE SELF-SCAN BLIND SPOTS, carried from the head's `retainedResiduals[13]`
    and WIDENED, never narrowed.  A dispatch reached through an ALIAS whose gate
    puts no undocumented flag literal inside a comparison node evades the flag
    scan; both measured forms (alias-plus-DECLARED-compared-literal and
    alias-plus-non-compared-gate) evade.  The predecessor's review measured
    three further forms individually and all three evade:
    `globals()["selftest"](root)`, `getattr(sys.modules[__name__],
    "selftest")(root)`, and a dict dispatch table.  All three fall inside the
    general alias clause; naming them makes the disclosure WIDER.  A second
    module-level function calling the suite directly IS caught, which is the
    correct behaviour.  A path consumer reached through any indirection evades
    the guard scan.  NOTHING HERE IS CLAIMED CLOSED.
  * THE GUARD SCAN DOES NOT SCAN SUBSCRIPTS.  `x[k]` on a candidate-supplied
    value is invisible to `EVRH-GUARD-01`.  The injection sweep is the oracle
    that covers it, at the sweep's stated boundary and no wider.
  * DEEP RECURSION.  `exact_equal` and `j_canon` recurse.  A document nested
    deeply enough to exhaust the interpreter's stack raises `RecursionError`,
    which `run_layer` converts into a typed `EVRH-TOTAL-01` finding rather than
    a traceback -- totality holds -- but the semantic class that was running is
    then NOT measured, and that is reported, never passed over.  `leaf_paths` is
    ITERATIVE precisely because it walks the 188 KB terminus.  `json.loads`
    refuses deeper input than the walkers can reach, and that refusal is an
    input failure at exit 2.
  * `evidence.v10.json` BELOW DEPTH 1 IS NOT SWEPT.  The review's boundary is
    carried unchanged so the before/after numbers compare; the v10 escape count
    is a floor at that boundary, not a total over v10's full path space.
  * THE TRUTH OF THE HEAD'S CONTENT is freeze section 7.8's bound and is not
    measurable by any instrument of this kind.
"""
from __future__ import annotations

import sys

_STARTUP_REFUSAL = (
    "EVRH-UNSUPPORTED-INVOCATION: caller must use "
    "python3 -I -B artifacts/check-evidence-resolved-head-28dc3c1a-total.py")
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
from typing import Any, Callable, Iterable, Iterator, NamedTuple


HERE = pathlib.Path(__file__).resolve().parent
CHECKER = "check-evidence-resolved-head-28dc3c1a-total.py"
PREDECESSOR = "check-evidence-resolved-head-28dc3c1a.py"
PREDECESSOR_SHA256 = (
    "e01d3524cf7ddb51e0d9ca66e538d7d9b9d29925deaf3adb4397efb9b39737cb")
PREDECESSOR_REVIEW = (
    "check-evidence-resolved-head-28dc3c1a.review-independent.json, "
    "5ad6b9a55ec94c4eba28fdb8fbd2bf6915e0979b49214b451f80a84613bb4d98, "
    "REJECT, 1 blocker (IR-EVRH-B1) + 6 advisories")
SUBJECT = "evidence.v15.json"

# ---------------------------------------------------------------------------
# Exit table.  Data, not literals scattered through the code, so the docstring
# above, the banner, and every `return` read from one place (freeze section
# 7.8.1 rule 3).  The first four NAMES and VALUES are the resolved head's
# `checkerModeContract.exitCodes` and are hard-compared against it at run time
# by EVRH-MODE-01 -- measured from resolved bytes, not invented here.
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

# IR-EVRH-A5, repaired as a measurement.  `--emit-resolved` writes the canonical
# payload and then exactly one terminator newline.  BOTH digests are pinned so
# neither can drift into prose, and EVRH-CANON-03 recomputes both every run.
RESOLVED_STREAM_SHA256 = (
    "b56fe8199610e2d94656273cdeb33bcf3c6616fa095b01e3ab7d6efae90883a0")
RESOLVED_STREAM_BYTES = 163785
EMIT_TERMINATOR = b"\n"

# Per-section canonical digests of the RESOLVED contract.  Implied by
# RESOLVED_CANONICAL, pinned separately so a drift reports WHICH section moved
# instead of only that the whole document did.
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

# IR-EVRH-A2: the disclosed coverage boundary, MEASURED at authoring on the
# resolved contract and hard-compared every run by EVRH-SECT-02 so it cannot
# rot into prose.
RESOLVED_TOPLEVEL_KEYS = 43

# The two blocks item 4 requires to be byte-identical to the v10 terminus.
ITEM4_BLOCKS: tuple[str, ...] = ("sealedCapabilityContract",
                                 "availabilityDifferential")

# The head's own self-declared identity, type-exact.  This is the posture the
# instrument asserts does not move silently.
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

# ---------------------------------------------------------------------------
# IR-EVRH-A2 REPAIR.  The five head leaves the predecessor's review measured as
# bound ONLY by the head digest pin: falsifying any of them, with path and JSON
# type unchanged, produced a finding set of EXACTLY [].  Each is now bound by
# required substring against the ACCEPTED bytes, so the corpus's first-named
# escape class -- a string leaf whose VALUE is false -- is caught BY NAME here
# and not only by the whole-document pin.  Each phrase was measured from
# evidence.v15.json at authoring.
# ---------------------------------------------------------------------------
HEAD_LEAF_REQUIRED: tuple[tuple[tuple[str, ...], str], ...] = (
    (("purpose",),
     "Repair evidence.v14's two blockers with their review's prescribed "
     "repairs"),
    (("purpose",), "EV14-IR-A2 is record-only and asserts nothing new."),
    (("whatThisDoesNotDo",),
     "does not close DR-002: AC-2 for THIS candidate, AC-3 and AC-4 remain"),
    (("whatThisDoesNotDo",),
     "does not modify the retained checker; every standing obligation and "
     "deferral carries exactly as v14 bound them"),
    (("derivedFrom", "rule"),
     "apply operations in order; every set carries its exact prior value"),
    (("derivedFrom", "resolutionChain"),
     "v15 -> v14 -> v13 -> v12 -> v11 -> v10. v10 is the full-text standalone "
     "and the resolution TERMINUS."),
    (("operationAccounting", "whyNoDigestMoves"),
     "three prose corrections in retainedResiduals entries 3, 5 and 13 only; "
     "no pin, golden, recipe, schema or vector leaf"),
    (("operationAccounting", "whyNoDigestMoves"),
     "item-4 blocks remain byte-identical to v10 and the guard-scan map "
     "remains untouched."),
)

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

# Required and forbidden sentences binding the three residual entries v15
# rewrote and the transfer closure the head's own scan description lives in.
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
    "An unexpected exception inside a layer becomes a reported finding and "
    "exit 1.",
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
# The head's totality rule, bound by required substring so the property this
# file implements cannot drift from the sentence that demands it.
TOTALITY_RULE_REQUIRED: tuple[str, ...] = (
    "Every checking layer is total over hostile parsed JSON.",
    "Malformed input returns a deterministic finding and never an exception, "
    "at the root, at every root key, at every nested schema node and at every "
    "scalar leaf position.",
)

SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
SHA256_IN_TEXT_RE = re.compile(r"[0-9a-f]{64}|sha256:|run1:")
RECIPE_KEY_RE = re.compile(r"recipe", re.I)
DERIVATION_VERBS: tuple[str, ...] = ("set", "add")
ACCOUNTING_MEMBERS: tuple[str, ...] = (
    "adds", "digestsMoved", "recipesChanged", "removes", "sets", "total",
    "whyNoDigestMoves")
ACCOUNTING_COUNT_KEYS: tuple[str, ...] = ("adds", "removes", "sets", "total")


# ---------------------------------------------------------------------------
# Typed exceptions.  Each one maps to exactly one exit disposition.
# ---------------------------------------------------------------------------
class DuplicateKeyError(ValueError):
    """A JSON object repeated a key; the document is not canonical."""


class Malformed(Exception):
    """A REQUIRED input is missing, unreadable, not JSON, or not a JSON object.

    Exit 2.  THE CHECK DID NOT RUN.  Never a finding (freeze section 7.8.1
    rule 2).
    """


class UnsupportedInvocation(Exception):
    """The caller supplied an argument vector this file does not accept."""


class TrustRootIntegrityError(Exception):
    """A GATED byte string is absent or does not hash to its declared pin.

    This is the failure the resolved head's exitDiscipline requires a successor
    to terminate at a DISTINCT declared code.  It exits 4.  It is never a
    finding, because nothing was measured: the check did not run.
    """


class PathEncodingError(ValueError):
    """`j_decanon` was handed something `j_canon` did not produce."""


DECLARED_EXCEPTIONS: tuple[type[BaseException], ...] = (
    DuplicateKeyError, Malformed, UnsupportedInvocation, TrustRootIntegrityError)


class Finding(NamedTuple):
    """A typed finding.  `id` names the class, `invariant` states the property
    that was asserted, `detail` states what was measured instead."""

    id: str
    invariant: str
    detail: str

    def render(self) -> str:
        return f"{self.id}: {self.invariant} | measured: {self.detail}"


class _Absent:
    def __repr__(self) -> str:                        # pragma: no cover - label
        return "<absent>"


_ABSENT = _Absent()


# ---------------------------------------------------------------------------
# THE TOTAL ACCESSORS (header section 5).
#
# These are the ONLY functions in this file permitted to use a raw mapping
# method, and EVRH-GUARD-01 exempts exactly these names.  The exemption is paid
# for by `check_accessor_totality`, which fires every one of them against the
# head's sixteen injection classes and against values outside the JSON universe
# and requires that none raises.
# ---------------------------------------------------------------------------
TOTAL_ACCESSORS: tuple[str, ...] = (
    "j_type", "m_get", "m_obj", "m_seq", "m_keys", "m_items", "m_str",
    "m_text", "m_has")

JSON_TYPES: tuple[str, ...] = (
    "array", "boolean", "integer", "null", "number", "object", "string")
OUTSIDE_JSON = "outside-json"


def j_type(value: Any) -> str:
    """The JSON type of a value.  TOTAL over every Python object.

    `boolean` is decided BEFORE `integer` because `isinstance(True, int)` is
    true in the host language, and that single fact is the root of the whole
    `True is not 1` class (freeze section 7.2.2 / 7.4).  Every test is
    `type(x) is C`, never `isinstance`, so no subclass is mistaken for its base.
    """
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
    return OUTSIDE_JSON


def m_obj(node: Any) -> dict:
    """The node if it is an object, else an empty object.  TOTAL."""
    return node if type(node) is dict else {}


def m_seq(node: Any) -> list:
    """The node if it is an array, else an empty array.  TOTAL."""
    return node if type(node) is list else []


def m_get(node: Any, key: Any, default: Any = _ABSENT) -> Any:
    """Member lookup that is TOTAL over every node and every key.

    This is the site the predecessor's `document.value.get("derivedFrom")` was,
    and the reason `IR-EVRH-B1` site 1 existed.
    """
    if type(node) is not dict:
        return default
    try:
        return node.get(key, default)
    except TypeError:                                  # an unhashable key
        return default


def m_has(node: Any, key: Any) -> bool:
    """Membership that is TOTAL over every node and every key."""
    if type(node) is not dict:
        return False
    try:
        return key in node
    except TypeError:                                  # an unhashable key
        return False


def _key_order(key: Any) -> tuple:
    """A TOTAL sort key over object keys of any type.

    `sorted()` over a dict with mixed int/str keys raises `TypeError` -- that
    was `IR-EVRH-B1` site 3.  This orders strings first among themselves, then
    everything else by JSON type name and repr, so no comparison ever crosses
    types.
    """
    if type(key) is str:
        return (0, key)
    return (1, j_type(key), repr(key))


def m_keys(node: Any) -> list:
    """Deterministically ordered keys of an object, or []. TOTAL."""
    if type(node) is not dict:
        return []
    return sorted(node.keys(), key=_key_order)


def m_items(node: Any) -> list:
    """Deterministically ordered (key, value) pairs of an object, or []. TOTAL."""
    if type(node) is not dict:
        return []
    return [(key, node[key]) for key in sorted(node.keys(), key=_key_order)]


def m_str(node: Any) -> str | None:
    """The node if it is exactly a string, else None.  TOTAL."""
    return node if type(node) is str else None


def m_text(value: Any) -> str:
    """A display rendering of any value that never raises.  TOTAL."""
    try:
        return repr(value)
    except Exception:                                  # noqa: BLE001 - total
        return f"<unrenderable {type(value).__name__}>"


# ---------------------------------------------------------------------------
# THE CANONICAL VALUE TOKEN (the IR-EVRH-A1 repair).
#
# `j_canon` is the corpus's own recorded repair for the reparenting class,
# taken from `check-c2-v9.py::jx_canon`: a LENGTH-FRAMED, type-tagged encoding.
# Framing is what makes concatenation decodable, and decodability is what makes
# the encoding injective.  `j_decanon` inverts it; the existence of that inverse
# IS the injectivity proof, and the round trip is EXECUTED on every run rather
# than asserted.
# ---------------------------------------------------------------------------
def j_frame(tag: str, payload: str) -> str:
    """Length-framed token."""
    return tag + str(len(payload)) + ":" + payload


def j_canon(value: Any) -> str | None:
    """A total, injective, type-tagged encoding of a JSON value.

    Returns None for anything OUTSIDE the RFC 8259 value universe -- a
    non-finite float, or a Python object JSON cannot express.  Returning None
    rather than raising is what keeps every caller total; a None is reported as
    a typed finding by the layer that asked.
    """
    kind = j_type(value)
    if kind == "null":
        return j_frame("z", "")
    if kind == "boolean":
        return j_frame("b", "1" if value else "0")
    if kind == "integer":
        return j_frame("i", str(value))
    if kind == "number":
        if value != value or value in (float("inf"), float("-inf")):
            return None                                # NaN/Infinity are not JSON
        return j_frame("n", repr(value))
    if kind == "string":
        return j_frame("s", value)
    if kind == "array":
        parts: list[str] = []
        for item in value:
            token = j_canon(item)
            if token is None:
                return None
            parts.append(token)
        return j_frame("a", "".join(parts))
    if kind == "object":
        pairs: list[str] = []
        for key, item in m_items(value):
            key_token = j_canon(key)
            item_token = j_canon(item)
            if key_token is None or item_token is None:
                return None
            pairs.append(key_token + item_token)
        return j_frame("o", "".join(pairs))
    return None


def _j_decanon_at(text: str, position: int) -> tuple[Any, int]:
    if position >= len(text):
        raise PathEncodingError("token ended early")
    tag = text[position]
    colon = text.find(":", position + 1)
    if colon < 0:
        raise PathEncodingError("no length frame")
    digits = text[position + 1:colon]
    if not digits.isdigit():
        raise PathEncodingError(f"length frame {digits!r} is not a count")
    size = int(digits)
    start = colon + 1
    nxt = start + size
    if nxt > len(text):
        raise PathEncodingError("length frame overruns the token")
    payload = text[start:nxt]
    if tag == "z":
        return None, nxt
    if tag == "b":
        return payload == "1", nxt
    if tag == "i":
        return int(payload), nxt
    if tag == "n":
        return float(payload), nxt
    if tag == "s":
        return payload, nxt
    if tag == "a":
        out: list[Any] = []
        inner = 0
        while inner < len(payload):
            item, inner = _j_decanon_at(payload, inner)
            out.append(item)
        return out, nxt
    if tag == "o":
        mapping: dict[Any, Any] = {}
        inner = 0
        while inner < len(payload):
            key, inner = _j_decanon_at(payload, inner)
            item, inner = _j_decanon_at(payload, inner)
            mapping[key] = item
        return mapping, nxt
    raise PathEncodingError(f"unknown canonical tag {tag!r}")


def j_decanon(text: str) -> Any:
    """Inverse of `j_canon`.  Its existence is the injectivity proof."""
    if type(text) is not str:
        raise PathEncodingError("a canonical token is a string")
    value, position = _j_decanon_at(text, 0)
    if position != len(text):
        raise PathEncodingError("trailing bytes after a canonical token")
    return value


def encode_path(steps: Iterable[Any]) -> str | None:
    """The identity of a leaf path.  A path is a LIST OF STEPS, never a text
    join -- that join was `IR-EVRH-A1`.  Injectivity is `j_canon`'s."""
    return j_canon(list(steps))


def decode_path(token: str) -> tuple:
    """Inverse of `encode_path`."""
    return tuple(j_decanon(token))


def render_path(steps: Iterable[Any]) -> str:
    """A HUMAN rendering for finding text only.  It is NOT an identity and is
    never used as a dict key -- rendering with a `/` join is exactly the
    collision `IR-EVRH-A1` names."""
    return "/" + "/".join(m_text(step) if type(step) not in (str, int)
                          else str(step) for step in steps)


# The witness set for the executed injectivity proof.  The first pair IS the
# `IR-EVRH-A1` collision: under the predecessor's `/`-join both render to
# `/acceptedGolden/evidenceDigest`; under `encode_path` they cannot collide,
# and the round trip proves it rather than asserting it.
PATH_WITNESSES: tuple[tuple[Any, ...], ...] = (
    ("acceptedGolden", "evidenceDigest"),
    ("acceptedGolden/evidenceDigest",),
    (),
    ("a",),
    ("a", "b"),
    ("a/b",),
    ("a", 0),
    ("a", "0"),
    (0,),
    ("0",),
    ("", ""),
    ("/",),
    ("~", "~0", "~1"),
    ("a", "b", "c", "d", "e"),
    ("keyWith:colon", "keyWith5:digits"),
    ("s3:abc",),
)


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
    if type(left) is dict:
        if len(left) != len(right):
            return False
        for key in left:
            if not m_has(right, key):
                return False
            if not exact_equal(left[key], right[key]):
                return False
        return True
    if type(left) is list:
        return len(left) == len(right) and all(
            exact_equal(a, b) for a, b in zip(left, right))
    return left == right


def canonical_bytes(value: Any) -> bytes:
    """Local mirror of `check-completeness-v2.py::canonical_bytes`.

    Used ONLY as a cross-check: `check_canonical` computes the published figure
    with the GATED resolver's own function, and this mirror is compared against
    it (EVRH-CANON-02).  Two implementations that agree are a measurement; one
    implementation is an assumption.
    """
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False).encode("utf-8")


def pointer_steps(path: Any) -> list[Any] | None:
    """RFC 6901 pointer steps, parsed STRICTLY: the parse must round-trip to the
    exact declared path or this walker refuses.  TOTAL: any value that is not a
    conforming pointer string returns None."""
    if type(path) is not str or not path.startswith("/"):
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
        "/" + (str(step) if type(step) is int
               else step.replace("~", "~0").replace("/", "~1"))
        for step in steps)
    return steps if rebuilt == path else None


def has_step(node: Any, step: Any) -> bool:
    """TOTAL: is `step` addressable in `node`?"""
    if type(node) is dict:
        return type(step) is str and m_has(node, step)
    if type(node) is list:
        return type(step) is int and 0 <= step < len(node)
    return False


def resolve_steps(root: Any, steps: list[Any]) -> tuple[bool, Any]:
    """TOTAL: walk `steps` from `root`, refusing rather than raising."""
    node = root
    for step in steps:
        if not has_step(node, step):
            return False, None
        node = node[step]
    return True, node


def leaf_paths(value: Any, prefix: tuple = ()) -> Iterator[tuple[tuple, Any]]:
    """Every scalar leaf as (STEPS TUPLE, value), deterministically ordered.

    ITERATIVE, not recursive: this walks the 188 KB terminus and a recursion
    limit inside the deepest walker is a defect waiting for a deep document.
    Yields the STEPS, never a text join -- the join was `IR-EVRH-A1`.
    """
    stack: list[tuple[tuple, Any]] = [(prefix, value)]
    while stack:
        path, node = stack[-1]
        del stack[-1]
        kind = j_type(node)
        if kind == "object":
            for key in reversed(m_keys(node)):
                stack.append((path + (key,), node[key]))
        elif kind == "array":
            for index in range(len(node) - 1, -1, -1):
                stack.append((path + (index,), node[index]))
        else:
            yield path, node


class LeafDelta(NamedTuple):
    moved: list[tuple[tuple, Any, Any]]
    unencodable: list[tuple]


def changed_leaves(before: Any, after: Any) -> LeafDelta:
    """Leaf paths whose value moved, type-exactly compared, sorted by the
    CANONICAL path token.

    THE `IR-EVRH-A1` REPAIR LIVES HERE.  The predecessor keyed these dicts by a
    `/`-joined text, so a key literally named `acceptedGolden/evidenceDigest`
    collided with the real path `/acceptedGolden/evidenceDigest` and the later
    leaf silently overwrote the earlier one, suppressing EVRH-ACCT-03.  The key
    is now `encode_path`, which is length-framed and invertible; a path that
    cannot be encoded is REPORTED, never silently merged.
    """
    left: dict[str, Any] = {}
    right: dict[str, Any] = {}
    unencodable: list[tuple] = []
    for source, sink in ((before, left), (after, right)):
        for steps, value in leaf_paths(source):
            token = encode_path(steps)
            if token is None:
                unencodable.append(steps)
                continue
            sink[token] = value
    moved: list[tuple[tuple, Any, Any]] = []
    for token in sorted(set(left) | set(right), key=str):
        old = m_get(left, token)
        new = m_get(right, token)
        if not exact_equal(old, new):
            moved.append((decode_path(token), old, new))
    return LeafDelta(moved=moved, unencodable=unencodable)


# ---------------------------------------------------------------------------
# The gated trust root
# ---------------------------------------------------------------------------
def load_gated_module(root: pathlib.Path, name: str, pin: str,
                      alias: str) -> types.ModuleType:
    """Hash-verify a gated resolver, then execute THE VERIFIED SNAPSHOT.

    The bytes that produced the digest are the bytes that are compiled: there is
    no second read between the measurement and the execution, so there is no
    TOCTOU window.  `__file__` is set before execution so the resolver's own
    `ROOT` lands on the tree it is being asked about -- which is how the selftest
    points the SAME verified bytes at a disposable /tmp copy without ever
    relaxing the pin.
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
    measured: dict[str, str] = {}
    modules: dict[str, types.ModuleType] = {}
    for index, name in enumerate(sorted(RESOLVER_PINS)):
        pin = RESOLVER_PINS[name]
        module = load_gated_module(root, name, pin, f"_gated_resolver_{index}")
        modules[name] = module
        measured[name] = pin
    return Resolvers(r1=modules["check-completeness.py"],
                     r2=modules["check-completeness-v2.py"],
                     measured=measured)


# ---------------------------------------------------------------------------
# Document loading -- THE INPUT GATE (IR-EVRH-B1 mechanism 3)
# ---------------------------------------------------------------------------
class Document(NamedTuple):
    name: str
    raw: bytes
    measured: str
    declared: str
    value: Any
    duplicate: str | None


def read_document(root: pathlib.Path, name: str, declared: str) -> Document:
    """Read, hash and parse a REQUIRED input, refusing anything this file does
    not accept.

    Freeze section 7.8.1 rule 2: a REQUIRED input this file does not accept
    refuses the whole run at exit 2 saying THE CHECK DID NOT RUN.  A parsed root
    that is not a JSON object is such an input, and the predecessor proceeded
    into it -- that was `IR-EVRH-B1`'s reachable minimal repro.

    Every refusal names the digest mismatch too when there is one, so a reader
    is never told only half of what is wrong.
    """
    path = root / "artifacts" / name
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise Malformed(
            f"{name}: REQUIRED input cannot be read ({type(exc).__name__}); "
            "THE CHECK DID NOT RUN") from exc
    measured = sha256_hex(raw)
    note = ("" if measured == declared else
            f"; its digest also does not match its gated pin (pinned "
            f"{declared}, measured {measured})")
    try:
        text = raw.decode("utf-8")
    except UnicodeError as exc:
        raise Malformed(
            f"{name}: REQUIRED input is not UTF-8; THE CHECK DID NOT "
            f"RUN{note}") from exc
    duplicate: str | None = None
    try:
        value = json.loads(text, object_pairs_hook=_pairs)
    except DuplicateKeyError as exc:
        duplicate = str(exc)
        try:
            value = json.loads(text)
        except Exception as inner:                     # noqa: BLE001 - total
            raise Malformed(
                f"{name}: REQUIRED input is not JSON ({type(inner).__name__}: "
                f"{inner}); THE CHECK DID NOT RUN{note}") from inner
    except Exception as exc:                           # noqa: BLE001 - total
        raise Malformed(
            f"{name}: REQUIRED input is not JSON ({type(exc).__name__}: {exc}); "
            f"THE CHECK DID NOT RUN{note}") from exc
    kind = j_type(value)
    if kind != "object":
        raise Malformed(
            f"{name}: REQUIRED input parses to a JSON {kind}, not an object; "
            f"THE CHECK DID NOT RUN{note}")
    return Document(name=name, raw=raw, measured=measured,
                    declared=declared, value=value, duplicate=duplicate)


# ---------------------------------------------------------------------------
# Independent pointer walk -- a third opinion on the resolution.
#
# The predecessor's review measured this function as ALREADY TOTAL at the site
# `stepwise_effective` was not, and named it as the shape to copy from.  It is
# carried unchanged in behaviour and converted to the total accessors.
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
        declaration = m_get(document.value, "derivedFrom")
        if j_type(declaration) != "object":
            errors.append(f"{document.name}: no derivedFrom object")
            return None, errors, unwalkable
        operations = m_get(declaration, "operations")
        if j_type(operations) != "array" or not operations:
            errors.append(f"{document.name}: derivedFrom carries no operations")
            return None, errors, unwalkable
        for index, operation in enumerate(operations):
            where = f"{document.name} operation {index}"
            if j_type(operation) != "object":
                errors.append(f"{where}: not an object")
                return None, errors, unwalkable
            verb = m_get(operation, "op")
            if verb not in DERIVATION_VERBS:
                errors.append(
                    f"{where}: verb {m_text(verb)} outside "
                    f"{list(DERIVATION_VERBS)}")
                return None, errors, unwalkable
            steps = pointer_steps(m_get(operation, "path"))
            if steps is None:
                unwalkable.append(
                    f"{where}: path {m_text(m_get(operation, 'path'))}")
                return None, errors, unwalkable
            if not m_has(operation, "value"):
                errors.append(f"{where}: carries no value")
                return None, errors, unwalkable
            found, parent = resolve_steps(base, steps[:-1])
            if not found or j_type(parent) not in ("object", "array"):
                errors.append(f"{where}: parent does not resolve to a container")
                return None, errors, unwalkable
            exists = has_step(parent, steps[-1])
            if verb == "set":
                if not m_has(operation, "from"):
                    errors.append(f"{where}: a set must restate the value it replaces")
                    return None, errors, unwalkable
                if not exists:
                    errors.append(f"{where}: does not resolve against the predecessor")
                    return None, errors, unwalkable
                declared_from = m_get(operation, "from")
                if not exact_equal(parent[steps[-1]], declared_from):
                    errors.append(
                        f"{where}: 'from' is not what the verified predecessor "
                        f"holds (type-exact comparison); declared "
                        f"{j_type(declared_from)}, held "
                        f"{j_type(parent[steps[-1]])}")
                    return None, errors, unwalkable
            else:
                if exists:
                    errors.append(f"{where}: add over an existing member")
                    return None, errors, unwalkable
                if j_type(parent) != "object" or type(steps[-1]) is not str:
                    errors.append(f"{where}: add can only name a member of an object")
                    return None, errors, unwalkable
            parent[steps[-1]] = copy.deepcopy(m_get(operation, "value"))
    return base, errors, unwalkable


def stepwise_effective(chain: list[Document]) -> dict[str, Any]:
    """Effective document after each delta, keyed by the delta that produced it.

    Used by the operation-accounting probes, which must compare the document
    BEFORE and AFTER a delta to decide whether a digest leaf or a recipe leaf
    actually moved -- `digestsMoved: 0` is a measurement claim and gets a hard
    comparison, not a reading.

    `IR-EVRH-B1` SITES 2 AND 3 ARE REPAIRED HERE, in the shape the review
    prescribed -- the one `independent_resolve` above already had.  The
    predecessor's `(declaration or {}).get("operations")` caught only FALSY
    non-objects, so a TRUTHY non-object `derivedFrom` reached `.get` and raised
    (site 2); and it guarded a non-addressable step for LIST parents only, so an
    INT step against a DICT parent produced a dict with mixed int/str keys,
    which is not representable as JSON and which `sorted()` then refused (site
    3).  Both are now the same explicit type test `independent_resolve` uses.
    """
    states: dict[str, Any] = {chain[-1].name: copy.deepcopy(chain[-1].value)}
    base = copy.deepcopy(chain[-1].value)
    for document in reversed(chain[:-1]):
        declaration = m_get(document.value, "derivedFrom")
        if j_type(declaration) != "object":
            break                                      # SITE 2
        operations = m_get(declaration, "operations")
        if j_type(operations) != "array":
            break
        nxt = copy.deepcopy(base)
        ok = True
        for operation in operations:
            if j_type(operation) != "object":
                ok = False
                break
            steps = pointer_steps(m_get(operation, "path"))
            if steps is None or not m_has(operation, "value"):
                ok = False
                break
            found, parent = resolve_steps(nxt, steps[:-1])
            if not found or j_type(parent) not in ("object", "array"):
                ok = False
                break
            if j_type(parent) == "array" and not has_step(parent, steps[-1]):
                ok = False
                break
            if j_type(parent) == "object" and type(steps[-1]) is not str:
                ok = False                             # SITE 3
                break
            parent[steps[-1]] = copy.deepcopy(m_get(operation, "value"))
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

      * a CALL to the suite that is not itself inside the suite's own
        definition is a DISPATCH; exactly one may exist.
      * a dispatch is GUARDED when a declared flag literal appears in the test
        of an enclosing `if`.
      * the ORDER clause is scoped to `main()`'s own top-level statement list,
        because that is where an unconditional finding gate could sit in front
        of the suite.
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
# THE GUARD SCAN (EVRH-GUARD-01) -- the systemic half of the IR-EVRH-B1 repair.
#
# Modelled on the resolved head's own `pathConsumerGuard` and disclosed to the
# same standard.  The MAP is stated in header section 5 and restated in the
# docstrings below; nothing outside that map is claimed.
# ---------------------------------------------------------------------------
RAW_MAPPING_METHODS: tuple[str, ...] = (
    "get", "items", "keys", "values", "setdefault", "pop")


def module_functions(tree: ast.Module) -> dict[str, ast.FunctionDef]:
    """PLAIN SYNCHRONOUS module-body function definitions, by name.

    An `async def`, a module-bound lambda, or a `def` inside a conditional
    module-level block is NOT a reachability root and is invisible here.  That
    is the head's own measured map, carried; it is a boundary, not a claim.
    """
    found: dict[str, ast.FunctionDef] = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            found[node.name] = node
    return found


def reachable_closure(tree: ast.Module, roots: Iterable[str]) -> list[str]:
    """Names reachable from `roots` by DIRECT-NAME calls.  Indirection of any
    form -- getattr, a dispatch table, globals() -- is invisible."""
    functions = module_functions(tree)
    seen: set[str] = set()
    frontier = [name for name in roots if name in functions]
    while frontier:
        name = frontier.pop()
        if name in seen:
            continue
        seen.add(name)
        for node in ast.walk(functions[name]):
            if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                    and node.func.id in functions
                    and node.func.id not in seen):
                frontier.append(node.func.id)
    return sorted(seen)


def raw_consumption_sites(tree: ast.Module,
                          roots: Iterable[str]) -> list[tuple[str, int, str]]:
    """Every RECOGNISED unguarded consumption inside the reached closure.

    RECOGNISED FORMS, exactly two, and no others:
      (a) a Call whose func is an Attribute whose attr is in
          RAW_MAPPING_METHODS -- a raw mapping method where a total accessor
          belongs;
      (b) a Call to the name `sorted` with a single positional argument that is
          a bare lowercase Name, an Attribute or a Subscript, and no `key=`
          keyword -- the `sorted()`-over-mixed-key-types shape that was
          IR-EVRH-B1 site 3.

    The TOTAL_ACCESSORS bodies are the ONE exemption, because they are where the
    raw form is implemented; that exemption is paid for by
    `check_accessor_totality`.  SUBSCRIPTS ARE NOT SCANNED.  Within a reached
    function the walk DESCENDS into nested definitions, so a nested def's
    direct-syntax consumption is reported even if never called.
    """
    functions = module_functions(tree)
    sites: list[tuple[str, int, str]] = []
    for name in reachable_closure(tree, roots):
        if name in TOTAL_ACCESSORS:
            continue
        for node in ast.walk(functions[name]):
            if not isinstance(node, ast.Call):
                continue
            if (isinstance(node.func, ast.Attribute)
                    and node.func.attr in RAW_MAPPING_METHODS):
                sites.append((name, node.lineno,
                              f".{node.func.attr}() on a raw mapping"))
            if (isinstance(node.func, ast.Name) and node.func.id == "sorted"
                    and len(node.args) == 1 and not node.keywords):
                argument = node.args[0]
                if isinstance(argument, (ast.Attribute, ast.Subscript)) or (
                        isinstance(argument, ast.Name)
                        and not argument.id.isupper()):
                    sites.append((name, node.lineno,
                                  "sorted() with no key= over a "
                                  "possibly-candidate value"))
    return sorted(sites)


# The reachability ROOTS of the guard scan: the layers that consume
# candidate-supplied values.  Named as a constant so the scan's scope is data
# the reader can check, not a judgement buried in code.
GUARD_ROOTS: tuple[str, ...] = (
    "check_documents", "check_declared_links", "check_terminus",
    "check_head_identity", "check_head_leaves", "check_accounting",
    "check_path_domain", "check_canonical", "check_item4", "check_grammar",
    "check_residuals", "check_transfers", "check_mode_contract",
    "check_provenance", "check_agreement", "resolve_with", "gated_call",
    "independent_resolve", "stepwise_effective")


# ---------------------------------------------------------------------------
# THE INJECTION VOCABULARY (header section 6).
#
# The NAMES are the resolved head's own `hostileInputTotalityContract
# .injections`, all sixteen, and EVRH-HOSTILE-02 hard-compares the sixteen
# implemented here against the sixteen read from the resolved bytes, so the
# vocabulary cannot drift from its source.  Fifteen are VALUE injections and
# `unknown-key` is the structural one; that split is this file's stated reading
# of the head's own `measurement.injectionValues: 15` alongside a sixteen-name
# list.
# ---------------------------------------------------------------------------
INJECTION_VALUES: dict[str, Any] = {
    "null": None,
    "integer": 7,
    "negative": -1,
    "float": 1.5,
    "true": True,
    "false": False,
    "empty-text": "",
    "text": "nope",
    "empty-array": [],
    "empty-object": {},
    "nested-array": [[1]],
    "nested-object": {"a": {"b": 1}},
    "control-text": "\u0000\u0001\u007f",
    "bom-text": "\ufeffnope",
    "digest-text": "sha256:" + "6e" * 32,
}
STRUCTURAL_INJECTION = "unknown-key"
INJECTED_KEY = "opensipUnknownInjectedKey"
INJECTION_NAMES: tuple[str, ...] = tuple(
    sorted(INJECTION_VALUES)) + (STRUCTURAL_INJECTION,)


# ---------------------------------------------------------------------------
# THE LAYER TOTALITY NET (IR-EVRH-B1 mechanism 2).
# ---------------------------------------------------------------------------
def run_layer(name: str, call: Callable[[], list[Finding]]) -> list[Finding]:
    """Invoke one checking layer.  An unexpected exception becomes a FINDING.

    This implements the resolved head's `hostileInputTotalityContract
    .exitDiscipline` first sentence verbatim: "An unexpected exception inside a
    layer becomes a reported finding and exit 1."  It is the BACKSTOP, not the
    property: the property is that the layers do not raise at all, and the
    injection sweep measures that by calling them UNGUARDED so this handler
    cannot mask an escape.

    `TrustRootIntegrityError` is re-raised, never converted.  That failure is
    NEVER a finding -- nothing was measured, the check did not run, and it
    terminates at exit 4.
    """
    try:
        return call()
    except TrustRootIntegrityError:
        raise
    except Exception as exc:                           # noqa: BLE001 - reported
        return [Finding(
            "EVRH-TOTAL-01",
            "every checking layer is TOTAL over hostile parsed JSON: an "
            "unexpected exception inside a layer becomes a reported finding "
            "and exit 1, never a raw traceback at the code the exit table "
            "reserves for findings (resolved head hostileInputTotalityContract"
            ".exitDiscipline; freeze section 7.8.1 defect D-6)",
            f"layer {name} raised {type(exc).__name__}: {exc}. The classes that "
            "layer measures were NOT measured on this run.")]


# ---------------------------------------------------------------------------
# The checks.  Every one carries a typed ID and a stated invariant, and every
# one consumes candidate-supplied values through the TOTAL ACCESSORS only.
# ---------------------------------------------------------------------------
def check_documents(chain: list[Document]) -> list[Finding]:
    findings: list[Finding] = []
    for document in chain:
        if j_type(document.value) != "object":
            findings.append(Finding(
                "EVRH-SHAPE-01",
                "every chain document's parsed root is a JSON object -- the "
                "shape every layer below is written against",
                f"{document.name}: root parses to a JSON "
                f"{j_type(document.value)}"))
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
        declaration = m_get(document.value, "derivedFrom")
        if j_type(declaration) != "object":
            findings.append(Finding(
                "EVRH-CHAIN-02",
                "every delta declares its predecessor by name and by full "
                "sha256",
                f"{document.name}: derivedFrom is a JSON "
                f"{j_type(declaration)}, not an object"))
            continue
        declared_name = m_get(declaration, "artifact")
        declared_digest = m_get(declaration, "sha256")
        if declared_name != expected_name:
            findings.append(Finding(
                "EVRH-CHAIN-02",
                "every delta names the next pinned chain link as its "
                "predecessor",
                f"{document.name}: declares {m_text(declared_name)}, chain "
                f"expects {expected_name!r}"))
        if declared_digest != pinned[expected_name]:
            findings.append(Finding(
                "EVRH-CHAIN-02",
                "every delta's declared predecessor digest equals that link's "
                "gated pin",
                f"{document.name}: declares {m_text(declared_digest)}, gated "
                f"pin is {pinned[expected_name]}"))
    return findings


def gated_call(label: str, document: Any, call: Callable[[], Any],
               default: Any) -> tuple[Any, list[Finding]]:
    """Invoke the REVIEWED gated resolver bytes across a TOTAL boundary.

    The gated resolvers are reviewed and frozen (freeze sections 7.2/7.6): their
    totality is not this instrument's to change, and they are not total -- handed
    a candidate whose root is not a JSON object they raise, because they were
    written against a well-shaped one.  THE BOUNDARY IS THIS INSTRUMENT'S, and
    this is where it is made total.  An exception from inside the gated bytes
    becomes a typed `EVRH-GATE-02` finding naming the resolver, the shape handed
    to it, and the class that consequently did NOT run.

    This is a FINDING, not a trust-root integrity failure: the gated bytes hash
    to their reviewed pins and are exactly right, and it is the candidate that
    is hostile.  `EVRH-GATE-01` remains reserved for integrity, at exit 4.
    """
    try:
        return call(), []
    except Exception as exc:                           # noqa: BLE001 - reported
        return default, [Finding(
            "EVRH-GATE-02",
            "the boundary this instrument owns around the REVIEWED gated "
            "resolver bytes is TOTAL: a candidate the gated resolver cannot "
            "consume becomes a typed finding here, never a traceback, and the "
            "class it would have measured is named as NOT measured (resolved "
            "head hostileInputTotalityContract.rule; the gated bytes are "
            "frozen and correct, so this is a finding and not an EVRH-GATE-01 "
            "integrity refusal at exit "
            f"{EXIT[SUCCESSOR_EXIT_NAME]})",
            f"{label} raised {type(exc).__name__} on a candidate whose root is "
            f"a JSON {j_type(document)}: {exc}")]


def check_terminus(terminus: Document, resolvers: Resolvers) -> list[Finding]:
    """Freeze section 7.3: the resolution TERMINUS is the reviewed full-text
    standalone and must declare no derivation of its own.  A terminus that grew
    a derivation would silently extend the chain past its reviewed bytes -- the
    exact `retention-tiers.v26` false positive the freeze records."""
    findings: list[Finding] = []
    for label, module in (("check-completeness.py", resolvers.r1),
                          ("check-completeness-v2.py", resolvers.r2)):
        outcome, guard = gated_call(
            f"{label}::derivation_declaration", terminus.value,
            lambda module=module: module.derivation_declaration(terminus.value),
            None)
        findings.extend(guard)
        if outcome is None:
            continue
        declaration, errors = outcome
        if declaration is not None or errors:
            findings.append(Finding(
                "EVRH-CHAIN-05",
                "the resolution terminus declares no derivation (freeze "
                "section 7.3)",
                f"{label} reads a declaration in {terminus.name}: "
                f"declaration={declaration is not None}, "
                f"errors={m_text(errors)}"))
    return findings


def _join_errors(errors: Any) -> str:
    """TOTAL rendering of a resolver's error channel, whatever it holds."""
    if j_type(errors) == "array":
        return "; ".join(m_text(item) if type(item) is not str else item
                         for item in errors)
    return m_text(errors)


def resolve_with(module: Any, label: str,
                 head: Document) -> tuple[Any, list[Finding], Any]:
    findings: list[Finding] = []
    outcome, guard = gated_call(
        f"{label}::derivation_declaration", head.value,
        lambda: module.derivation_declaration(head.value), None)
    findings.extend(guard)
    if outcome is None:
        return None, findings, None
    declaration, errors = outcome
    if errors:
        findings.append(Finding(
            "EVRH-CHAIN-03",
            "the gated resolver reads exactly one unambiguous derivation "
            "declaration from the head",
            f"{label}: {_join_errors(errors)}"))
        return None, findings, None
    if declaration is None:
        findings.append(Finding(
            "EVRH-CHAIN-03",
            "the head declares a derivation the gated resolver recognises",
            f"{label}: no declaration found in {head.name}"))
        return None, findings, None
    outcome, guard = gated_call(
        f"{label}::resolve_derivation", head.value,
        lambda: module.resolve_derivation(f"artifacts/{head.name}",
                                          declaration),
        None)
    findings.extend(guard)
    if outcome is None:
        return None, findings, None
    effective, provenance, resolve_errors = outcome
    if resolve_errors or effective is None:
        findings.append(Finding(
            "EVRH-CHAIN-03",
            "the gated resolver materialises the effective contract with zero "
            "refusals",
            f"{label}: {_join_errors(resolve_errors) or 'no effective contract'}"))
        return None, findings, provenance
    return effective, findings, provenance


def check_provenance(provenance: Any, label: str,
                     chain_pins: tuple[tuple[str, str], ...]) -> list[Finding]:
    """The resolver's own provenance walk must visit exactly the pinned chain,
    in order, and stop at the terminus."""
    findings: list[Finding] = []
    walked: list[tuple[Any, Any]] = []
    node = provenance
    seen = 0
    while j_type(node) == "object" and seen <= len(chain_pins) + 2:
        walked.append((m_get(node, "predecessor", "?"),
                       m_get(node, "measuredDigest", "?")))
        node = m_get(node, "via")
        seen += 1
    expected = [(f"artifacts/{name}", digest) for name, digest in chain_pins[1:]]
    if walked != expected:
        findings.append(Finding(
            "EVRH-CHAIN-04",
            "the resolver's provenance walk visits exactly the pinned chain, "
            "in order, terminating at the terminus",
            f"{label}: walked {m_text(walked)}, gated chain is "
            f"{m_text(expected)}"))
    return findings


def check_agreement(candidates: dict[str, Any]) -> list[Finding]:
    """Three independent resolutions must be type-exactly the same document."""
    findings: list[Finding] = []
    labels = sorted(candidates, key=str)
    reference = m_get(candidates, labels[0])
    for label in labels[1:]:
        if not exact_equal(reference, m_get(candidates, label)):
            findings.append(Finding(
                "EVRH-CHAIN-06",
                "both gated resolvers and this instrument's own pointer walk "
                "produce type-exactly the same effective contract",
                f"{labels[0]} and {label} disagree"))
    return findings


def check_canonical(resolved: Any, resolvers: Resolvers) -> list[Finding]:
    findings: list[Finding] = []
    raw, guard = gated_call(
        "check-completeness-v2.py::canonical_bytes", resolved,
        lambda: resolvers.r2.canonical_bytes(resolved), None)
    findings.extend(guard)
    if raw is None:
        return findings
    gated = sha256_hex(raw)
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
    # IR-EVRH-A5, repaired as a MEASUREMENT: the emission stream is the
    # canonical payload plus EXACTLY ONE terminator newline, and both digests
    # are recomputed here so neither can drift into prose.
    stream = canonical_bytes(resolved) + EMIT_TERMINATOR
    stream_digest = sha256_hex(stream)
    if stream_digest != RESOLVED_STREAM_SHA256 or len(stream) != RESOLVED_STREAM_BYTES:
        findings.append(Finding(
            "EVRH-CANON-03",
            "the --emit-resolved stream is exactly the canonical payload plus "
            "one terminator newline: the WHOLE-STREAM sha256 and byte count "
            "are pinned alongside the payload pin, so a reader who pipes the "
            "stream into sha256 reproduces a published figure rather than "
            "silently missing the terminator (IR-EVRH-A5)",
            f"stream sha256 pinned {RESOLVED_STREAM_SHA256}, measured "
            f"{stream_digest}; bytes pinned {RESOLVED_STREAM_BYTES}, measured "
            f"{len(stream)}"))
    # IR-EVRH-A2's disclosed boundary, held as a measurement rather than prose.
    if j_type(resolved) == "object" and len(resolved) != RESOLVED_TOPLEVEL_KEYS:
        findings.append(Finding(
            "EVRH-SECT-02",
            "the resolved contract's top-level key census is the gated one -- "
            f"{RESOLVED_TOPLEVEL_KEYS} keys, of which {len(SECTION_PINS)} are "
            "digest-pinned per section and the remainder are covered only by "
            "the whole-document pin (disclosed boundary, header section 7)",
            f"{len(m_obj(resolved))} top-level keys, gated census "
            f"{RESOLVED_TOPLEVEL_KEYS}"))
    for section in sorted(SECTION_PINS):
        if not m_has(resolved, section):
            findings.append(Finding(
                "EVRH-SECT-01",
                "every gated section of the resolved contract is present and "
                "hashes to its pin",
                f"{section}: absent from the resolved contract"))
            continue
        measured = sha256_hex(canonical_bytes(m_get(resolved, section)))
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
        actual = m_get(head.value, key)
        if not exact_equal(actual, expected):
            findings.append(Finding(
                "EVRH-HEAD-01",
                "the head's self-declared identity and posture are exactly "
                "what the accepted bytes declare, type-exact",
                f"{key}: expected {expected!r} ({j_type(expected)}), measured "
                f"{m_text(actual)} ({j_type(actual)})"))
    return findings


def check_head_leaves(head: Document) -> list[Finding]:
    """IR-EVRH-A2's repair.

    The predecessor's review measured five head leaves as bound ONLY by the head
    digest pin: falsifying any of them, with path and JSON type unchanged,
    produced a finding set of EXACTLY [].  That is the corpus's first-named
    escape class -- a string leaf whose VALUE is false -- and a whole-document
    pin says only that SOMETHING moved.  Each leaf is now bound by required
    substring against the accepted bytes, so a falsification is caught BY NAME.
    """
    findings: list[Finding] = []
    for steps, phrase in HEAD_LEAF_REQUIRED:
        found, node = resolve_steps(head.value, list(steps))
        if not found:
            findings.append(Finding(
                "EVRH-HEAD-02",
                "each semantically-bound head leaf is present at its declared "
                "path",
                f"{render_path(steps)}: does not resolve in {head.name}"))
            continue
        text = ""
        if type(node) is str:
            text = node
        elif j_type(node) == "array":
            text = "\n".join(item for item in node if type(item) is str)
        else:
            findings.append(Finding(
                "EVRH-HEAD-02",
                "each semantically-bound head leaf is a string or an array of "
                "strings",
                f"{render_path(steps)}: is a JSON {j_type(node)}"))
            continue
        if phrase not in text:
            findings.append(Finding(
                "EVRH-HEAD-02",
                "each semantically-bound head leaf carries the exact sentence "
                "the ACCEPTED bytes state -- the head digest pin says only "
                "that something moved, this says what (IR-EVRH-A2)",
                f"{render_path(steps)} is missing {phrase!r}"))
    return findings


def check_path_domain(chain: list[Document]) -> list[Finding]:
    """Every leaf of every chain document is inside the canonical value domain,
    and every leaf path round-trips through the injective encoding.

    This is the standing, whole-corpus half of the IR-EVRH-A1 proof: the
    injectivity witness set is fixed and small, but the round trip is ALSO
    executed over every path this run actually emits, so the property is
    measured on the real corpus and not only on a witness.
    """
    findings: list[Finding] = []
    for document in chain:
        outside = 0
        first_outside: tuple | None = None
        unencodable = 0
        first_unencodable: tuple | None = None
        broken: list[str] = []
        for steps, value in leaf_paths(document.value):
            if j_canon(value) is None:
                outside += 1
                if first_outside is None:
                    first_outside = steps
            token = encode_path(steps)
            if token is None:
                unencodable += 1
                if first_unencodable is None:
                    first_unencodable = steps
                continue
            if len(broken) < 3:
                try:
                    if decode_path(token) != tuple(steps):
                        broken.append(render_path(steps))
                except PathEncodingError as exc:
                    broken.append(f"{render_path(steps)} ({exc})")
        if outside:
            findings.append(Finding(
                "EVRH-SHAPE-02",
                "every leaf of every chain document is inside the RFC 8259 "
                "value universe -- no NaN, no Infinity, nothing a canonical "
                "serialisation cannot express",
                f"{document.name}: {outside} leaf/leaves outside the JSON "
                f"value universe, first at "
                f"{render_path(first_outside or ())}"))
        if unencodable:
            findings.append(Finding(
                "EVRH-PATH-02",
                "every leaf path of every chain document is canonically "
                "encodable, so the digest and recipe accounting over it is "
                "MEASURED rather than skipped",
                f"{document.name}: {unencodable} unencodable path(s), first at "
                f"{render_path(first_unencodable or ())}"))
        if broken:
            findings.append(Finding(
                "EVRH-PATH-01",
                "the canonical path encoding is INJECTIVE, proved by the "
                "existence of its inverse and executed over every path this "
                "run emits (the IR-EVRH-A1 repair, the shape check-c2-v9.py "
                "records: hash a length-framed, invertible token, never a "
                "text join)",
                f"{document.name}: round trip failed at {broken}"))
    return findings


def check_item4(resolved: Any, chain: list[Document]) -> list[Finding]:
    """RECOMPUTE, do not trust.  Every delta in the chain claims the item-4
    blocks are byte-identical to v10; that claim is a measurement and gets a
    hard comparison against the terminus bytes."""
    findings: list[Finding] = []
    terminus = chain[-1].value
    for block in ITEM4_BLOCKS:
        in_resolved = m_has(resolved, block)
        in_terminus = m_has(terminus, block)
        if not in_resolved or not in_terminus:
            findings.append(Finding(
                "EVRH-ITEM4-01",
                "both item-4 blocks are present in the resolved contract and "
                "in the terminus",
                f"{block}: resolved={in_resolved}, terminus={in_terminus}"))
            continue
        if not exact_equal(m_get(resolved, block), m_get(terminus, block)):
            findings.append(Finding(
                "EVRH-ITEM4-01",
                "each item-4 block is type-exactly identical to the v10 "
                "terminus (RECOMPUTED, never read from the delta's claim)",
                f"{block}: resolved canonical "
                f"{sha256_hex(canonical_bytes(m_get(resolved, block)))}, "
                f"terminus canonical "
                f"{sha256_hex(canonical_bytes(m_get(terminus, block)))}"))
    for document in chain[:-1]:
        declaration = m_get(document.value, "derivedFrom")
        for index, operation in enumerate(m_seq(m_get(declaration, "operations"))):
            path = m_str(m_get(operation, "path"))
            if path is None:
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
        accounting = m_get(document.value, "operationAccounting")
        declaration = m_get(document.value, "derivedFrom")
        operations = m_get(declaration, "operations")
        if j_type(accounting) != "object":
            findings.append(Finding(
                "EVRH-ACCT-01",
                "every delta publishes an operationAccounting object",
                f"{name}: operationAccounting is a JSON {j_type(accounting)}"))
            continue
        if m_keys(accounting) != sorted(ACCOUNTING_MEMBERS):
            findings.append(Finding(
                "EVRH-ACCT-01",
                "operationAccounting declares exactly its closed member set",
                f"{name}: members {m_keys(accounting)}, expected "
                f"{sorted(ACCOUNTING_MEMBERS)}"))
        if j_type(operations) != "array":
            continue
        verbs = [m_get(operation, "op") for operation in operations
                 if j_type(operation) == "object"]
        measured = {
            "total": len(operations),
            "sets": sum(1 for verb in verbs if verb == "set"),
            "adds": sum(1 for verb in verbs if verb == "add"),
            "removes": sum(1 for verb in verbs if verb == "remove"),
        }
        for key in ACCOUNTING_COUNT_KEYS:
            declared = m_get(accounting, key)
            if not exact_equal(declared, measured[key]):
                findings.append(Finding(
                    "EVRH-ACCT-01",
                    "operationAccounting's counts equal the operations the "
                    "delta actually carries, compared type-exactly (freeze "
                    "section 7.2.2: 3 is not 3.0 and is not True)",
                    f"{name}.{key}: declares {m_text(declared)} "
                    f"({j_type(declared)}), measured {measured[key]!r} (int)"))
        legal = {repr(item) for item in DERIVATION_VERBS}
        for verb in sorted({m_text(item) for item in verbs}):
            if verb not in legal:
                findings.append(Finding(
                    "EVRH-ACCT-02",
                    "every operation verb is inside the resolver's declared "
                    "verb set",
                    f"{name}: verb {verb} outside {list(DERIVATION_VERBS)}"))
        before = m_get(states, order[position - 1])
        after = m_get(states, name)
        if before is _ABSENT or after is _ABSENT:
            findings.append(Finding(
                "EVRH-ACCT-03",
                "the digestsMoved and recipesChanged claims are verified by "
                "recomputing the effective contract before and after the delta",
                f"{name}: the stepwise effective contract could not be built, "
                "so the two claims were NOT measured"))
            continue
        delta = changed_leaves(before, after)
        if delta.unencodable:
            findings.append(Finding(
                "EVRH-PATH-02",
                "every leaf path compared by the accounting probe is "
                "canonically encodable, so no leaf is silently dropped from "
                "the digestsMoved/recipesChanged recomputation",
                f"{name}: {len(delta.unencodable)} unencodable path(s), first "
                f"at {render_path(delta.unencodable[0])}"))
        digest_moves = [steps for steps, old, new in delta.moved
                        if any(type(item) is str and SHA256_IN_TEXT_RE.search(item)
                               for item in (old, new))]
        recipe_moves = [steps for steps, _old, _new in delta.moved
                        if any(type(step) is str and RECIPE_KEY_RE.search(step)
                               for step in steps)]
        for key, moves in (("digestsMoved", digest_moves),
                           ("recipesChanged", recipe_moves)):
            declared = m_get(accounting, key)
            if not exact_equal(declared, len(moves)):
                findings.append(Finding(
                    "EVRH-ACCT-03",
                    f"the published {key} count equals the recomputed count of "
                    "changed leaves of that kind (a recorded measurement is "
                    "compared to the measurement it records), where a leaf's "
                    "identity is the INJECTIVE canonical encoding of its path "
                    "and not a text join (IR-EVRH-A1)",
                    f"{name}.{key}: declares {m_text(declared)}, recomputed "
                    f"{len(moves)} "
                    f"({sorted((render_path(steps) for steps in moves), key=str)})"))
    return findings


def check_grammar(resolved: Any) -> list[Finding]:
    findings: list[Finding] = []
    grammar = m_get(resolved, "canonicalWireGrammar")
    if j_type(grammar) != "object":
        return [Finding(
            "EVRH-GRAM-01",
            "the resolved contract carries a canonicalWireGrammar object",
            f"canonicalWireGrammar is a JSON {j_type(grammar)}")]
    if m_keys(grammar) != sorted(GRAMMAR_MEMBERS + ("records",)):
        findings.append(Finding(
            "EVRH-GRAM-01",
            "the wire grammar declares exactly its closed member set",
            f"members {m_keys(grammar)}, expected "
            f"{sorted(GRAMMAR_MEMBERS + ('records',))}"))
    if m_get(grammar, "id") != GRAMMAR_ID:
        findings.append(Finding(
            "EVRH-GRAM-01",
            "the wire grammar's identity is the declared one",
            f"id {m_text(m_get(grammar, 'id'))}, expected {GRAMMAR_ID!r}"))
    records = m_get(grammar, "records")
    if j_type(records) != "object" or m_keys(records) != sorted(GRAMMAR_RECORDS):
        findings.append(Finding(
            "EVRH-GRAM-02",
            "the grammar declares exactly the five ...V1 record types, named "
            "(a count survives a rename; the closed set does not)",
            f"records {m_keys(records) if j_type(records) == 'object' else m_text(records)},"
            f" expected {sorted(GRAMMAR_RECORDS)}"))
    for name, record in m_items(records):
        if type(name) is not str or not name.endswith("V1"):
            findings.append(Finding(
                "EVRH-GRAM-02",
                "every declared record type is a ...V1 record",
                f"{m_text(name)} does not end in V1"))
        if j_type(record) != "object":
            findings.append(Finding(
                "EVRH-GRAM-02", "every record declaration is an object",
                f"{m_text(name)} is a JSON {j_type(record)}"))
            continue
        fields = m_get(record, "fields")
        required = m_get(record, "required")
        if j_type(fields) != "array" or j_type(required) != "array":
            findings.append(Finding(
                "EVRH-GRAM-02",
                "every record declares a required list and a fields list",
                f"{m_text(name)}: required={j_type(required)}, "
                f"fields={j_type(fields)}"))
            continue
        names = [m_get(field, "name") for field in fields
                 if j_type(field) == "object"]
        if names != required:
            findings.append(Finding(
                "EVRH-GRAM-02",
                "a record's field ORDER is exactly its required list -- the "
                "grammar's recordRules.order is 'exact field order below', so "
                "order is normative, not presentational",
                f"{m_text(name)}: fields {m_text(names)}, required "
                f"{m_text(required)}"))
        tokens = [j_canon(item) for item in names]
        if len(set(tokens)) != len(tokens):
            findings.append(Finding(
                "EVRH-GRAM-02", "no record repeats a field name",
                f"{m_text(name)}: {m_text(names)}"))
        for field in fields:
            if j_type(field) != "object" or not m_has(field, "const"):
                continue
            const = m_get(field, "const")
            if j_type(const) != "integer":
                findings.append(Finding(
                    "EVRH-GRAM-05",
                    "a declared const scalar is a type-exact int, never a bool "
                    "and never a float (freeze section 7.4's 1.0 == 1 class)",
                    f"{m_text(name)}.{m_text(m_get(field, 'name'))}: const "
                    f"{m_text(const)} ({j_type(const)})"))
    registry = m_get(grammar, "tagRegistry")
    if j_type(registry) != "array":
        findings.append(Finding(
            "EVRH-GRAM-03", "the grammar declares a tagRegistry list",
            f"tagRegistry is a JSON {j_type(registry)}"))
        registry = []
    tags = [j_canon(m_get(row, "tag")) for row in registry
            if j_type(row) == "object"]
    if len(registry) != TAG_REGISTRY_SIZE:
        findings.append(Finding(
            "EVRH-GRAM-03", "the tag registry census is the gated one",
            f"{len(registry)} rows, gated census {TAG_REGISTRY_SIZE}"))
    if len(set(tags)) != len(tags):
        duplicates = sorted({tag for tag in tags if tags.count(tag) > 1}, key=str)
        findings.append(Finding(
            "EVRH-GRAM-03", "no tag is registered twice",
            f"duplicates {duplicates}"))
    # Tag identities are CANONICAL TOKENS, never raw values: a raw list or
    # object tag would be unhashable and would have raised here.  The token is
    # injective, so two tags share one only if they are the same JSON value.
    used: set = set()
    for _name, record in m_items(records):
        if j_type(record) != "object":
            continue
        used.add(j_canon(m_get(record, "recordTag")))
        for field in m_seq(m_get(record, "fields")):
            if j_type(field) == "object":
                used.add(j_canon(m_get(field, "tag")))
    envelope = m_get(grammar, "domainEnvelope")
    if j_type(envelope) == "object":
        used.add(j_canon(m_get(envelope, "recordTag")))
        for field in m_seq(m_get(envelope, "fields")):
            if j_type(field) == "object":
                used.add(j_canon(m_get(field, "tag")))
    absent = j_canon(None)
    unregistered = sorted(
        (token for token in used - set(tags)
         if token is not None and token != absent), key=str)
    if unregistered:
        findings.append(Finding(
            "EVRH-GRAM-03",
            "every record tag and every field tag the grammar uses is present "
            "in the tag registry",
            f"unregistered tags {unregistered}"))
    for member, expected in (("recordRules", GRAMMAR_RULE_MEMBERS),
                             ("scalarEncoding", GRAMMAR_SCALAR_MEMBERS),
                             ("commitments", GRAMMAR_COMMITMENTS)):
        block = m_get(grammar, member)
        if j_type(block) != "object" or m_keys(block) != sorted(
                expected, key=str):
            findings.append(Finding(
                "EVRH-GRAM-04",
                f"the grammar's {member} declares exactly its closed member set",
                f"{member}: "
                f"{m_keys(block) if j_type(block) == 'object' else m_text(block)}, "
                f"expected {sorted(expected, key=str)}"))
    return findings


def check_residuals(resolved: Any) -> list[Finding]:
    findings: list[Finding] = []
    residuals = m_get(resolved, "retainedResiduals")
    if j_type(residuals) != "array":
        return [Finding(
            "EVRH-RES-01", "retainedResiduals is a list",
            f"retainedResiduals is a JSON {j_type(residuals)}")]
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
                f"residual {index} is a JSON {j_type(entry)}"))
    for index in sorted(RESIDUAL_REQUIRED):
        if index >= len(residuals) or type(residuals[index]) is not str:
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
        for phrase in m_get(RESIDUAL_FORBIDDEN, index, ()):
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
    transfers = m_get(resolved, "reviewFindingTransfers")
    if j_type(transfers) != "array":
        return [Finding(
            "EVRH-XFER-01", "reviewFindingTransfers is a list",
            f"reviewFindingTransfers is a JSON {j_type(transfers)}")]
    if len(transfers) != TRANSFER_COUNT:
        findings.append(Finding(
            "EVRH-XFER-01",
            "the review-finding-transfer census is the gated one",
            f"{len(transfers)} transfers, gated census {TRANSFER_COUNT}"))
    census: dict[str, int] = {}
    for index, entry in enumerate(transfers):
        if j_type(entry) != "object":
            findings.append(Finding(
                "EVRH-XFER-01", "every transfer is an object",
                f"transfer {index} is a JSON {j_type(entry)}"))
            continue
        shape = tuple(m_keys(entry))
        if shape not in TRANSFER_KEYSHAPES:
            findings.append(Finding(
                "EVRH-XFER-01",
                "every transfer carries one of the two admitted key shapes",
                f"transfer {index} ({m_text(m_get(entry, 'id'))}) has "
                f"{list(shape)}"))
        state = m_str(m_get(entry, "state"))
        if state is not None:
            census[state] = m_get(census, state, 0) + 1
        digest = m_get(entry, "sourceSha256")
        if digest is not _ABSENT and digest is not None and not (
                type(digest) is str and SHA256_RE.match(digest)):
            findings.append(Finding(
                "EVRH-XFER-01",
                "every declared source digest is a full lowercase sha256",
                f"transfer {index} ({m_text(m_get(entry, 'id'))}): "
                f"{m_text(digest)}"))
    if census != TRANSFER_STATE_CENSUS:
        findings.append(Finding(
            "EVRH-XFER-02",
            "the closure-state census equals the gated census exactly -- a "
            "finding cannot change closure state without the census moving",
            f"measured {dict(m_items(census))}, gated "
            f"{dict(m_items(TRANSFER_STATE_CENSUS))}"))
    if TRANSFER33_INDEX < len(transfers) and j_type(
            transfers[TRANSFER33_INDEX]) == "object":
        entry = transfers[TRANSFER33_INDEX]
        if m_get(entry, "state") != TRANSFER33_STATE:
            findings.append(Finding(
                "EVRH-XFER-03",
                "the retained-checker scan description is closed by an "
                "EXECUTED probe, not by a derivation",
                f"transfer {TRANSFER33_INDEX} state "
                f"{m_text(m_get(entry, 'state'))}, expected "
                f"{TRANSFER33_STATE!r}"))
        closure = m_str(m_get(entry, "closure"))
        if closure is None:
            findings.append(Finding(
                "EVRH-XFER-03", "the transfer's closure is prose",
                f"closure is a JSON {j_type(m_get(entry, 'closure'))}"))
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
    contract = m_get(resolved, "checkerModeContract")
    if j_type(contract) != "object":
        return [Finding(
            "EVRH-MODE-01", "the resolved contract carries a checkerModeContract",
            f"checkerModeContract is a JSON {j_type(contract)}")]

    table = m_get(contract, "exitCodes")
    if j_type(table) != "object":
        findings.append(Finding(
            "EVRH-MODE-01", "the mode contract publishes an exitCodes table",
            f"exitCodes is a JSON {j_type(table)}"))
    else:
        if m_keys(table) != sorted(HEAD_EXIT_NAMES):
            findings.append(Finding(
                "EVRH-MODE-01",
                "the head's exitCodes table names exactly the four "
                "dispositions this instrument implements unrenumbered",
                f"head names {m_keys(table)}, implemented "
                f"{sorted(HEAD_EXIT_NAMES)}"))
        for name in sorted(HEAD_EXIT_NAMES):
            declared = m_get(table, name)
            mine = m_get(EXIT, name)
            if not exact_equal(declared, mine):
                findings.append(Finding(
                    "EVRH-MODE-01",
                    "this instrument's exit code for each of the head's four "
                    "dispositions IS the head's, measured from resolved bytes "
                    "and compared type-exactly -- not invented and not "
                    "transcribed",
                    f"{name}: head {m_text(declared)} ({j_type(declared)}), "
                    f"instrument {m_text(mine)} ({j_type(mine)})"))
        if EXIT[SUCCESSOR_EXIT_NAME] in {EXIT[name] for name in HEAD_EXIT_NAMES}:
            findings.append(Finding(
                "EVRH-MODE-04",
                "the successor's trust-root integrity code is DISTINCT from "
                "the four dispositions it must not renumber",
                f"{SUCCESSOR_EXIT_NAME} is {EXIT[SUCCESSOR_EXIT_NAME]}, which "
                "collides with a head disposition"))

    declared_flags = m_get(contract, "declaredFlags")
    entrypoints = m_get(contract, "entrypoints")
    if j_type(entrypoints) == "array" and j_type(declared_flags) == "array":
        implied = sorted({token for line in entrypoints
                          if type(line) is str
                          for token in line.split()
                          if token.startswith("--")})
        if implied != sorted((item for item in declared_flags), key=str):
            findings.append(Finding(
                "EVRH-MODE-02",
                "the head's declaredFlags equal the flags implied by its own "
                "entrypoints -- the same equality this instrument enforces "
                "over itself",
                f"entrypoints imply {implied}, declaredFlags "
                f"{m_text(declared_flags)}"))
    else:
        findings.append(Finding(
            "EVRH-MODE-02",
            "the head declares an entrypoints list and a declaredFlags list",
            f"entrypoints={j_type(entrypoints)}, "
            f"declaredFlags={j_type(declared_flags)}"))

    note = m_str(m_get(contract, "exitCodesNote"))
    if note is None:
        findings.append(Finding(
            "EVRH-MODE-03",
            "the v14-added exitCodesNote is present and points at the "
            "disclosure it summarises",
            f"exitCodesNote is a JSON "
            f"{j_type(m_get(contract, 'exitCodesNote'))}"))
    else:
        for phrase in EXIT_CODES_NOTE_REQUIRED:
            if phrase not in note:
                findings.append(Finding(
                    "EVRH-MODE-03",
                    "the exitCodesNote still names the fifth termination "
                    "behaviour and the section that discloses it",
                    f"exitCodesNote is missing {phrase!r}"))

    hostile = m_get(resolved, "hostileInputTotalityContract")
    discipline = m_str(m_get(hostile, "exitDiscipline"))
    if discipline is None:
        findings.append(Finding(
            "EVRH-MODE-04",
            "hostileInputTotalityContract.exitDiscipline discloses the fifth "
            "termination behaviour AND binds an unexpected layer exception to "
            "a reported finding",
            f"exitDiscipline is a JSON "
            f"{j_type(m_get(hostile, 'exitDiscipline'))}"))
    else:
        for phrase in EXIT_DISCIPLINE_REQUIRED:
            if phrase not in discipline:
                findings.append(Finding(
                    "EVRH-MODE-04",
                    "the exitDiscipline still binds BOTH obligations this "
                    "instrument discharges: an unexpected layer exception "
                    "becomes a reported finding (EVRH-TOTAL-01), and a "
                    "trust-root integrity failure terminates at the distinct "
                    f"code {EXIT[SUCCESSOR_EXIT_NAME]}",
                    f"exitDiscipline is missing {phrase!r}"))

    # The totality RULE itself is bound, so the property this file implements
    # cannot drift from the sentence that demands it (IR-EVRH-B1).
    rule = m_str(m_get(hostile, "rule"))
    if rule is None:
        findings.append(Finding(
            "EVRH-HOSTILE-03",
            "hostileInputTotalityContract states the totality rule this "
            "instrument implements",
            f"rule is a JSON {j_type(m_get(hostile, 'rule'))}"))
    else:
        for phrase in TOTALITY_RULE_REQUIRED:
            if phrase not in rule:
                findings.append(Finding(
                    "EVRH-HOSTILE-03",
                    "the totality rule still says what this instrument's "
                    "layers are built to satisfy and what its selftest sweep "
                    "measures",
                    f"rule is missing {phrase!r}"))

    # The injection VOCABULARY is read from the resolved bytes and hard-compared
    # against the sixteen this file implements, so the sweep cannot drift from
    # the space the head declares.
    declared_injections = m_get(hostile, "injections")
    if j_type(declared_injections) != "array":
        findings.append(Finding(
            "EVRH-HOSTILE-02",
            "hostileInputTotalityContract declares the injection vocabulary "
            "the selftest sweep executes",
            f"injections is a JSON {j_type(declared_injections)}"))
    elif sorted((item for item in declared_injections), key=str) != sorted(
            INJECTION_NAMES):
        findings.append(Finding(
            "EVRH-HOSTILE-02",
            "the injection vocabulary this instrument sweeps IS the head's "
            "declared vocabulary, measured from the resolved bytes rather "
            "than transcribed into a constant that could drift from it",
            f"head declares {sorted((item for item in declared_injections), key=str)}, "
            f"instrument implements {sorted(INJECTION_NAMES)}"))
    return findings


def check_self_scans(tree: ast.Module | None = None) -> list[Finding]:
    """TRIPWIRES.  See header section 2: these prove properties of this file's
    SYNTAX and nothing about its semantics.

    `tree` is the subject.  It defaults to this file's own tree; the source
    self-mutation battery passes a DELIBERATELY BROKEN tree instead, so that
    each scan is shown to fire rather than merely shown to pass.
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

    # THE GUARD SCAN.  Systemic half of the IR-EVRH-B1 repair; map disclosed in
    # header section 5 and in `raw_consumption_sites`.
    reached = reachable_closure(tree, GUARD_ROOTS)
    if not reached:
        findings.append(Finding(
            "EVRH-GUARD-01",
            "the layer-closure guard scan is non-vacuous -- a scan that "
            "reaches zero functions cannot be distinguished from one that "
            "measures nothing",
            "the closure walk reached 0 functions from GUARD_ROOTS"))
    sites = raw_consumption_sites(tree, GUARD_ROOTS)
    if sites:
        findings.append(Finding(
            "EVRH-GUARD-01",
            "no checking layer in the reachable closure consumes a "
            "candidate-supplied value through a raw mapping method or through "
            "a keyless sorted() -- every such consumption goes through the "
            "TOTAL ACCESSORS, which are the one exemption and are themselves "
            "measured by check_accessor_totality (IR-EVRH-B1, the systemic "
            "repair; scan map disclosed in header section 5)",
            f"{len(sites)} unguarded consumption site(s): "
            f"{[f'{name}:{line} {what}' for name, line, what in sites[:6]]}"))
    return findings


def check_accessor_totality() -> list[Finding]:
    return accessor_totality(REAL_ACCESSORS, ACCESSOR_KEY_WITNESSES)


def accessor_totality(accessors: Iterable[tuple[str, Callable[[Any], Any]]],
                      keys: Iterable[Any]) -> list[Finding]:
    """The TOTAL ACCESSORS are total.  Measured, because they are the one place
    EVRH-GUARD-01 exempts and an unmeasured exemption is a hole.

    Every accessor is fired against every one of the head's injection classes,
    against a container holding them, and against values OUTSIDE the JSON
    universe entirely.  None may raise; the sorting accessors must additionally
    order a MIXED int/str-keyed object, which is the exact shape that raised
    `TypeError` at IR-EVRH-B1 site 3.
    """
    findings: list[Finding] = []
    hostile: list[Any] = [INJECTION_VALUES[name] for name in sorted(INJECTION_VALUES)]
    hostile.extend([
        {"a": 1}, [1, 2], {0: "int-key", "b": "str-key"},
        {True: "bool-key", 2: "int-key", "c": "str-key"},
        object(), _ABSENT, float("nan"), float("inf"), b"bytes", (1, 2),
        {frozenset(): "unhashable-ish"},
    ])
    for label, call in accessors:
        for value in hostile:
            try:
                call(value)
            except Exception as exc:                   # noqa: BLE001 - reported
                findings.append(Finding(
                    "EVRH-TOTAL-02",
                    "every TOTAL ACCESSOR is total over every value, including "
                    "values outside the JSON universe and objects with mixed "
                    "key types -- the exemption EVRH-GUARD-01 grants them is "
                    "paid for by this measurement",
                    f"{label} raised {type(exc).__name__} on a "
                    f"{type(value).__name__}: {exc}"))
    for key in keys:
        try:
            m_get({"k": 1}, key)
            m_has({"k": 1}, key)
        except Exception as exc:                       # noqa: BLE001 - reported
            findings.append(Finding(
                "EVRH-TOTAL-02",
                "m_get and m_has are total over every KEY as well as every "
                "node, including unhashable keys",
                f"key {m_text(key)} raised {type(exc).__name__}: {exc}"))
    if len(INJECTION_NAMES) != 16:
        findings.append(Finding(
            "EVRH-HOSTILE-02",
            "this instrument implements exactly sixteen injection classes, "
            "which is the head's declared vocabulary size",
            f"{len(INJECTION_NAMES)} implemented"))
    return findings


REAL_ACCESSORS: tuple[tuple[str, Callable[[Any], Any]], ...] = (
        ("j_type", j_type),
        ("m_obj", m_obj),
        ("m_seq", m_seq),
        ("m_keys", m_keys),
        ("m_items", m_items),
        ("m_str", m_str),
        ("m_text", m_text),
        ("m_get", lambda node: m_get(node, "k")),
        ("m_has", lambda node: m_has(node, "k")),
    )
# The accessors' KEYS are exercised too, not only their nodes -- including an
# unhashable one, which `dict.get` refuses and `m_get` must not.
ACCESSOR_KEY_WITNESSES: tuple[Any, ...] = (
    None, 1, 1.5, True, "k", (1, 2), [1], {"a": 1})


def naive_join_encode(steps: Iterable[Any]) -> str | None:
    """THE PREDECESSOR'S ENCODER, retained as a PROBE and never used to measure
    anything.  `f"{prefix}/{key}"` -- unescaped, unframed, not injective.  It
    exists so `check_path_encoding` is shown to FIRE on the exact defect
    IR-EVRH-A1 names, rather than only ever shown to pass."""
    return "/" + "/".join(str(step) for step in steps)


def check_path_encoding() -> list[Finding]:
    return path_encoding_findings(encode_path, decode_path)


def path_encoding_findings(encode: Callable[[Iterable[Any]], str | None],
                           decode: Callable[[str], tuple]) -> list[Finding]:
    """THE INJECTIVITY PROOF, EXECUTED (the IR-EVRH-A1 repair).

    Injectivity is not asserted.  `decode_path` is a left inverse of
    `encode_path`, and the round trip is executed here over a fixed witness set
    whose FIRST TWO MEMBERS ARE THE COLLISION THE REVIEW MEASURED: under the
    predecessor's `/`-join, `("acceptedGolden", "evidenceDigest")` and
    `("acceptedGolden/evidenceDigest",)` both render to the same text and the
    later one silently overwrote the earlier.  Given the round trip, injectivity
    follows: if `encode_path(a) == encode_path(b)` then
    `a = decode_path(encode_path(a)) = decode_path(encode_path(b)) = b`.
    """
    findings: list[Finding] = []
    tokens: dict[str, tuple] = {}
    for steps in PATH_WITNESSES:
        token = encode(steps)
        if token is None:
            findings.append(Finding(
                "EVRH-PATH-01",
                "every witness path is inside the canonical encoding's domain",
                f"{render_path(steps)} did not encode"))
            continue
        try:
            back = decode(token)
        except Exception as exc:                       # noqa: BLE001 - reported
            findings.append(Finding(
                "EVRH-PATH-01",
                "decode_path is a LEFT INVERSE of encode_path -- its existence "
                "is the injectivity proof and the round trip is executed, "
                "never asserted",
                f"{render_path(steps)} -> {token!r} did not decode: {exc}"))
            continue
        if back != tuple(steps) or [j_type(item) for item in back] != [
                j_type(item) for item in steps]:
            findings.append(Finding(
                "EVRH-PATH-01",
                "the round trip returns the SAME steps, type-exactly -- an "
                "int step and a str step of the same spelling are different "
                "paths (freeze section 7.2.2)",
                f"{render_path(steps)} -> {token!r} -> {m_text(back)}"))
            continue
        if token in tokens and tokens[token] != tuple(steps):
            findings.append(Finding(
                "EVRH-PATH-01",
                "no two distinct paths share a canonical token -- the "
                "IR-EVRH-A1 reparenting collision is structurally unavailable, "
                "not merely avoided",
                f"{render_path(steps)} and {render_path(tokens[token])} both "
                f"encode to {token!r}"))
            continue
        tokens[token] = tuple(steps)
    # The collision the review measured, checked by name so the proof cannot
    # quietly stop covering the case it exists for.
    left = encode(("acceptedGolden", "evidenceDigest"))
    right = encode(("acceptedGolden/evidenceDigest",))
    if left is None or right is None or left == right:
        findings.append(Finding(
            "EVRH-PATH-01",
            "the exact IR-EVRH-A1 collision pair encodes to two DIFFERENT "
            "tokens: a key literally named 'acceptedGolden/evidenceDigest' is "
            "not the path /acceptedGolden/evidenceDigest",
            f"left {m_text(left)}, right {m_text(right)}"))
    # A value outside the JSON universe must be REFUSED by the encoder rather
    # than encoded to something that cannot be inverted.
    for outside in (float("nan"), float("inf"), object(), b"bytes"):
        if j_canon(outside) is not None:
            findings.append(Finding(
                "EVRH-PATH-01",
                "j_canon refuses every value outside the RFC 8259 universe "
                "rather than emitting a token it cannot invert",
                f"{type(outside).__name__} encoded to "
                f"{m_text(j_canon(outside))}"))
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
# THE LAYER TABLE.
#
# ONE table drives both `validate` (through the totality net) and the selftest's
# injection sweep (UNGUARDED).  That is why the sweep provably covers every
# layer the run executes: it is the same table, and EVRH-HOSTILE-04 compares its
# census against a pinned constant so a layer cannot be added to the run without
# being added to the sweep.
#
# Each entry declares the documents it CONSUMES, and each layer takes exactly
# those documents as its arguments -- so "this injection cannot affect this
# layer" is a structural fact about the call, never a judgement about the body.
# ---------------------------------------------------------------------------
class LayerCall(NamedTuple):
    name: str
    consumes: tuple[str, ...]
    call: Callable[[], Any]


def chain_layers(chain: list[Document], resolvers: Resolvers,
                 chain_pins: tuple[tuple[str, str], ...]) -> tuple[LayerCall, ...]:
    """Layers over the CHAIN documents that return findings."""
    head = chain[0]
    terminus = chain[-1]
    every = tuple(document.name for document in chain)
    return (
        LayerCall("check_documents", every,
                  lambda: check_documents(chain)),
        LayerCall("check_declared_links", every,
                  lambda: check_declared_links(chain, chain_pins)),
        LayerCall("check_terminus", (terminus.name,),
                  lambda: check_terminus(terminus, resolvers)),
        LayerCall("check_head_identity", (head.name,),
                  lambda: check_head_identity(head)),
        LayerCall("check_head_leaves", (head.name,),
                  lambda: check_head_leaves(head)),
        LayerCall("check_path_domain", every,
                  lambda: check_path_domain(chain)),
        LayerCall("check_accounting", every,
                  lambda: check_accounting(chain)),
    )


def resolution_layers(chain: list[Document],
                      resolvers: Resolvers) -> tuple[LayerCall, ...]:
    """Layers over the CHAIN documents that return a resolution, not findings."""
    head = chain[0]
    every = tuple(document.name for document in chain)
    return (
        LayerCall("independent_resolve", every,
                  lambda: independent_resolve(chain)),
        LayerCall("stepwise_effective", every,
                  lambda: stepwise_effective(chain)),
        LayerCall("resolve_with:check-completeness.py", (head.name,),
                  lambda: resolve_with(resolvers.r1, "check-completeness.py",
                                       head)),
        LayerCall("resolve_with:check-completeness-v2.py", (head.name,),
                  lambda: resolve_with(resolvers.r2,
                                       "check-completeness-v2.py", head)),
    )


def resolved_layers(resolved: Any, resolvers: Resolvers,
                    chain: list[Document]) -> tuple[LayerCall, ...]:
    """Layers over the RESOLVED effective contract."""
    return (
        LayerCall("check_canonical", (),
                  lambda: check_canonical(resolved, resolvers)),
        LayerCall("check_item4", (),
                  lambda: check_item4(resolved, chain)),
        LayerCall("check_grammar", (), lambda: check_grammar(resolved)),
        LayerCall("check_residuals", (), lambda: check_residuals(resolved)),
        LayerCall("check_transfers", (), lambda: check_transfers(resolved)),
        LayerCall("check_mode_contract", (),
                  lambda: check_mode_contract(resolved)),
    )


# Pinned so a layer cannot be added to the run without being added to the sweep.
LAYER_CENSUS: dict[str, int] = {"chain": 7, "resolution": 4, "resolved": 6}


def run_value_layer(name: str, call: Callable[[], Any],
                    default: Any) -> tuple[Any, list[Finding]]:
    """The totality net for a layer that returns a VALUE rather than findings."""
    try:
        return call(), []
    except TrustRootIntegrityError:
        raise
    except Exception as exc:                           # noqa: BLE001 - reported
        return default, [Finding(
            "EVRH-TOTAL-01",
            "every checking layer is TOTAL over hostile parsed JSON: an "
            "unexpected exception inside a layer becomes a reported finding "
            "and exit 1, never a raw traceback at the code the exit table "
            "reserves for findings (resolved head hostileInputTotalityContract"
            ".exitDiscipline; freeze section 7.8.1 defect D-6)",
            f"layer {name} raised {type(exc).__name__}: {exc}. The classes that "
            "layer measures were NOT measured on this run.")]


# ---------------------------------------------------------------------------
# The run
# ---------------------------------------------------------------------------
def check_layer_census(census: dict[str, int]) -> list[Finding]:
    if census == LAYER_CENSUS:
        return []
    return [Finding(
        "EVRH-HOSTILE-04",
        "the layer census this run executes equals the pinned census the "
        "selftest's injection sweep enumerates, so a layer cannot enter the "
        "run without entering the sweep",
        f"measured {dict(m_items(census))}, pinned "
        f"{dict(m_items(LAYER_CENSUS))}")]


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

    findings.extend(check_layer_census(
        {"chain": len(chain_layers(chain, resolvers, chain_pins)),
         "resolution": len(resolution_layers(chain, resolvers)),
         "resolved": len(resolved_layers(None, resolvers, chain))}))

    for layer in chain_layers(chain, resolvers, chain_pins):
        findings.extend(run_layer(layer.name, layer.call))

    candidates: dict[str, Any] = {}
    provenances: dict[str, Any] = {}
    for label, module in (("check-completeness.py", resolvers.r1),
                          ("check-completeness-v2.py", resolvers.r2)):
        outcome, guard_findings = run_value_layer(
            f"resolve_with:{label}",
            lambda module=module, label=label: resolve_with(module, label, head),
            (None, [], None))
        findings.extend(guard_findings)
        effective, resolve_findings, provenance = outcome
        findings.extend(resolve_findings)
        if effective is not None:
            candidates[label] = effective
            provenances[label] = provenance

    walk, walk_guard = run_value_layer(
        "independent_resolve", lambda: independent_resolve(chain),
        (None, [], []))
    findings.extend(walk_guard)
    walked, walk_errors, unwalkable = walk
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

    for label in sorted(provenances, key=str):
        findings.extend(run_layer(
            f"check_provenance:{label}",
            lambda label=label: check_provenance(
                m_get(provenances, label), label, chain_pins)))
    if len(candidates) > 1:
        findings.extend(run_layer("check_agreement",
                                  lambda: check_agreement(candidates)))

    resolved = m_get(candidates, "check-completeness-v2.py", None) or (
        m_get(candidates, "check-completeness.py", None) or walked)
    measured: dict[str, Any] = {
        "gatedResolvers": dict(sorted(resolvers.measured.items())),
        "chain": [(document.name, document.measured) for document in chain],
        "resolvedCanonical": None,
        "sections": {},
    }
    if resolved is None:
        not_measured.append(
            "EVRH-CANON-01..03/EVRH-SECT-01..02/EVRH-GRAM-*/EVRH-RES-*/"
            "EVRH-XFER-*/EVRH-MODE-01..04/EVRH-HOSTILE-02..03/EVRH-ITEM4-*: "
            "the effective contract could not be materialised, so no class "
            "over the RESOLVED document ran. This is not a pass.")
    else:
        stream, stream_guard = run_value_layer(
            "canonical_serialisation",
            lambda: (sha256_hex(resolvers.r2.canonical_bytes(resolved)),
                     {section: sha256_hex(canonical_bytes(m_get(resolved, section)))
                      for section in sorted(SECTION_PINS)
                      if m_has(resolved, section)}),
            (None, {}))
        findings.extend(stream_guard)
        measured["resolvedCanonical"], measured["sections"] = stream
        for layer in resolved_layers(resolved, resolvers, chain):
            findings.extend(run_layer(layer.name, layer.call))
    findings.extend(run_layer("check_self_scans", check_self_scans))
    # Tree- and candidate-independent, so they contribute identically to the
    # selftest baseline and to every mutation and cannot distort a finding-set
    # delta.  They are run HERE rather than only in the default path so that
    # "the base is clean" means the same thing in both modes.
    findings.extend(run_layer("check_accessor_totality", check_accessor_totality))
    findings.extend(run_layer("check_path_encoding", check_path_encoding))
    findings.extend(run_layer("check_argument_discipline",
                              check_argument_discipline))

    findings.sort(key=lambda item: (item.id, item.detail))
    return Report(findings=findings, resolved=resolved, measured=measured,
                  notMeasured=sorted(not_measured))


def run_validation(root: pathlib.Path) -> tuple[Report | None, int, str]:
    """THE ONE PLACE a validation failure becomes an exit disposition.

    Freeze section 7.8.1 rule 3 -- an exit code a document CLAIMS must be the
    exit code the file PRODUCES -- is kept by making this the single decision
    point that both `main()` and the selftest's input-refusal probe drive.  The
    probe therefore MEASURES the mapping rather than reading it, which is
    exactly what IR-EVRH-B1 found the predecessor could not do.
    """
    try:
        return validate(root), EXIT["clean"], ""
    except TrustRootIntegrityError as exc:
        return None, EXIT[SUCCESSOR_EXIT_NAME], str(exc)
    except Malformed as exc:
        return None, EXIT["unsupportedInvocationOrInput"], f"EVRH-INPUT: {exc}"


# ---------------------------------------------------------------------------
# Mutation selftest.  DISPOSABLE /tmp COPIES ONLY -- the live tree is never
# written to, and every copy is removed on completion.
# ---------------------------------------------------------------------------
TMP_ROOT = "/tmp"
TMP_PREFIX = "evrh-total-28dc3c1a-"

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
    re-pinned by any mutation except the ones that exist to prove they refuse.
    """
    document = json.loads(_read_text(target, HEAD_FILE))
    edit(document)
    _write_text(target, HEAD_FILE,
                json.dumps(document, indent=1, ensure_ascii=False) + "\n")


def _repin_head(target: pathlib.Path) -> tuple[str, str]:
    raw = (target / "artifacts" / HEAD_FILE).read_bytes()
    return HEAD_FILE, sha256_hex(raw)


def _append_operation(document: dict, operation: dict, verb: str) -> None:
    """Append an operation and keep the published accounting honest, so a
    mutation isolates the class it targets instead of also tripping the counts."""
    document["derivedFrom"]["operations"].append(operation)
    accounting = document["operationAccounting"]
    accounting["total"] = accounting["total"] + 1
    accounting[verb] = accounting[verb] + 1


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
        _append_operation(document, {
            "op": "set",
            "path": "/availabilityDifferential/mutation",
            "from": "remove one replay-only raw object from current RT13 "
                    "availability",
            "value": "remove two replay-only raw objects from current RT13 "
                     "availability",
        }, "sets")
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


def _mutate_head_posture(target: pathlib.Path) -> None:
    """The posture this instrument exists to assert does not move silently."""
    def edit(document: dict) -> None:
        document["status"] = "APPLIED"
    _edit_head(target, edit)


def _mutate_head_version_respell(target: pathlib.Path) -> None:
    """A TYPE respell with the value unchanged: 15 -> 15.0 (freeze 7.2.2)."""
    def edit(document: dict) -> None:
        document["version"] = 15.0
    _edit_head(target, edit)


def _mutate_head_leaf(target: pathlib.Path) -> None:
    """IR-EVRH-A2's escape, shipped as a standing probe: a string leaf whose
    VALUE is false with its path and JSON type unchanged."""
    def edit(document: dict) -> None:
        document["purpose"] = "This artifact seals CD-RT-5 and applies itself."
    _edit_head(target, edit)


def _mutate_reparenting_collision(target: pathlib.Path) -> None:
    """IR-EVRH-A1's mutant, shipped as a standing probe.

    A real digest move at /acceptedGolden/evidenceDigest PLUS a key literally
    named `acceptedGolden/evidenceDigest`, publishing `digestsMoved: 0`.  Under
    the predecessor's `/`-joined leaf paths the two collided and the later leaf
    restored the pre-move value, so the recomputed count was 0 and the false
    claim passed with only EVRH-CANON-01 firing.  Under the injective encoding
    they cannot collide and EVRH-ACCT-03 is REQUIRED here.
    """
    real = ("sha256:6edbf46f919565e5a10426e4ff9f1dcf56588d18d1b75ad1c32cd848"
            "b19f47b9")
    def edit(document: dict) -> None:
        _append_operation(document, {
            "op": "set", "path": "/acceptedGolden/evidenceDigest",
            "from": real, "value": "sha256:" + "bb" * 32}, "sets")
        _append_operation(document, {
            "op": "add", "path": "/acceptedGolden~1evidenceDigest",
            "value": real}, "adds")
        document["operationAccounting"]["digestsMoved"] = 0
    _edit_head(target, edit)


def _mutate_predecessor_digest(target: pathlib.Path) -> None:
    """A digest moved to a different-but-REAL artifact: v15 declaring v13's
    true digest rather than v14's."""
    def edit(document: dict) -> None:
        document["derivedFrom"]["sha256"] = dict(CHAIN_PINS)["evidence.v13.json"]
    _edit_head(target, edit)


def _mutate_nan(target: pathlib.Path) -> None:
    """A value outside the RFC 8259 universe.  `json.loads` accepts NaN by
    default, so a hostile document really can carry one and no canonical
    serialisation can express it."""
    def edit(document: dict) -> None:
        document["opensipOutsideJsonProbe"] = float("nan")
    _edit_head(target, edit)


def _mutate_grammar_const(target: pathlib.Path) -> None:
    """A grammar const int respelled as a float (freeze section 7.4)."""
    def edit(document: dict) -> None:
        _append_operation(document, {
            "op": "set",
            "path": "/canonicalWireGrammar/records/RawProofInventoryV1/"
                    "fields/0/const",
            "from": 1, "value": 1.0}, "sets")
    _edit_head(target, edit)


def _mutate_residual_type(target: pathlib.Path) -> None:
    """A retained residual respelled from a string to an int."""
    def edit(document: dict) -> None:
        document["derivedFrom"]["operations"][2]["value"] = 7
    _edit_head(target, edit)


def _mutate_transfer_state(target: pathlib.Path) -> None:
    """A finding changing closure state without the census moving honestly."""
    def edit(document: dict) -> None:
        _append_operation(document, {
            "op": "set", "path": "/reviewFindingTransfers/33/state",
            "from": TRANSFER33_STATE, "value": "OPEN-CARRIED-RESIDUAL"}, "sets")
    _edit_head(target, edit)


class Mutation(NamedTuple):
    label: str
    apply: Callable[[pathlib.Path], None]
    repin: bool
    required: tuple[str, ...]
    invariantClass: str


MUTATIONS: tuple[Mutation, ...] = (
    Mutation("chain-link-digest", _mutate_chain_link_digest, False,
             ("EVRH-CHAIN-01", "EVRH-CHAIN-03"), "chain-link digest"),
    Mutation("canonical-digest", _mutate_canonical, True,
             ("EVRH-CANON-01", "EVRH-SECT-01"), "resolved canonical digest"),
    Mutation("residual-sentence", _mutate_residual_sentence, True,
             ("EVRH-RES-02", "EVRH-SECT-01"), "a residual sentence"),
    Mutation("item-4-byte", _mutate_item4_byte, True,
             ("EVRH-ITEM4-01", "EVRH-ITEM4-02"), "an item-4 byte"),
    Mutation("type-respell", _mutate_type_respell, True,
             ("EVRH-ACCT-01",), "a type respell (3 -> 3.0)"),
    Mutation("duplicate-key-injection", _mutate_duplicate_key, True,
             ("EVRH-DUP-01",), "a duplicate-key injection"),
    Mutation("dropped-operation", _mutate_dropped_operation, True,
             ("EVRH-ACCT-01", "EVRH-CANON-01"), "a dropped operation"),
    Mutation("from-drift", _mutate_from_drift, True,
             ("EVRH-CHAIN-03", "EVRH-CHAIN-07"), "a 'from' drift"),
    Mutation("head-posture-move", _mutate_head_posture, True,
             ("EVRH-HEAD-01",), "the head's asserted posture"),
    Mutation("head-version-respell", _mutate_head_version_respell, True,
             ("EVRH-HEAD-01",), "a head type respell (15 -> 15.0)"),
    Mutation("head-leaf-falsification", _mutate_head_leaf, True,
             ("EVRH-HEAD-02",), "a head leaf whose VALUE is false (IR-EVRH-A2)"),
    Mutation("reparenting-collision", _mutate_reparenting_collision, True,
             ("EVRH-ACCT-03",),
             "a reparenting that collides with a real path (IR-EVRH-A1)"),
    Mutation("predecessor-digest-substitution", _mutate_predecessor_digest, True,
             ("EVRH-CHAIN-02",), "a digest moved to a different-but-REAL artifact"),
    Mutation("outside-json-value", _mutate_nan, True,
             ("EVRH-SHAPE-02",), "a value outside the RFC 8259 universe"),
    Mutation("grammar-const-float", _mutate_grammar_const, True,
             ("EVRH-GRAM-05",), "a grammar const int respelled as a float"),
    Mutation("residual-type-respell", _mutate_residual_type, True,
             ("EVRH-RES-01",), "a residual respelled from string to int"),
    Mutation("transfer-state-move", _mutate_transfer_state, True,
             ("EVRH-XFER-02", "EVRH-XFER-03"), "a transfer's closure state"),
)


# ---------------------------------------------------------------------------
# Source self-mutation battery.
#
# The self-scans pass on every honest run, which is exactly what makes them
# worthless as published evidence unless each is also shown to FIRE.  These
# mutations break one scanned property at a time in an IN-MEMORY syntax tree --
# no file is written, not even under /tmp -- and require the corresponding scan
# to report it.
#
# The head's escapeRule governs here too: a syntax-tree mutation that does not
# change the tree, or that its scan does not report, is an ESCAPE, never a pass.
# ---------------------------------------------------------------------------
def _function_body(tree: ast.Module, name: str) -> list[Any] | None:
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == name:
            return node.body
    return None


def _main_body(tree: ast.Module) -> list[Any] | None:
    return _function_body(tree, "main")


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


def _sm_raw_consumption(tree: ast.Module) -> None:
    """A raw mapping method reintroduced into a reached checking layer -- the
    habit that produced all three IR-EVRH-B1 sites."""
    body = _function_body(tree, "check_documents")
    if body is not None:
        body.insert(0, ast.parse('_probe = chain.get("derivedFrom")\n').body[0])


SOURCE_MUTATIONS: tuple[tuple[str, Callable[[ast.Module], None], str, str], ...] = (
    ("undocumented-flag", _sm_undocumented_flag, "EVRH-MODE-05",
     "an undocumented flag literal reaching a comparison node"),
    ("vacuous-flag-scan", _sm_vacuous_scan, "EVRH-MODE-05",
     "every flag literal removed from every comparison node"),
    ("second-dispatch", _sm_second_dispatch, "EVRH-MODE-06",
     "a second, undocumented selftest entrypoint"),
    ("finding-gate-first", _sm_finding_gate, "EVRH-MODE-07",
     "an unconditional finding gate in front of the suite"),
    ("raw-consumption", _sm_raw_consumption, "EVRH-GUARD-01",
     "a raw mapping method reintroduced into a reached checking layer"),
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


# ---------------------------------------------------------------------------
# THE GATE PROBE, widened to the seven shapes IR-EVRH-A4 measured by hand.
# ---------------------------------------------------------------------------
def _gate_mismatch(name: str) -> Callable[[pathlib.Path], None]:
    def apply(target: pathlib.Path) -> None:
        path = target / "artifacts" / name
        path.write_bytes(path.read_bytes() + b"\n# gated-pin tamper probe\n")
    return apply


def _gate_absent(name: str) -> Callable[[pathlib.Path], None]:
    def apply(target: pathlib.Path) -> None:
        (target / "artifacts" / name).unlink()
    return apply


def _gate_directory(name: str) -> Callable[[pathlib.Path], None]:
    def apply(target: pathlib.Path) -> None:
        path = target / "artifacts" / name
        path.unlink()
        path.mkdir()
    return apply


def _gate_non_utf8(name: str) -> Callable[[pathlib.Path], None]:
    def apply(target: pathlib.Path) -> None:
        (target / "artifacts" / name).write_bytes(b"\xff\xfe\x00 not utf-8")
    return apply


def _gate_empty(name: str) -> Callable[[pathlib.Path], None]:
    def apply(target: pathlib.Path) -> None:
        (target / "artifacts" / name).write_bytes(b"")
    return apply


GATE_SHAPES: tuple[tuple[str, str, Callable[[pathlib.Path], None]], ...] = (
    ("mismatch-v2", "check-completeness-v2.py",
     _gate_mismatch("check-completeness-v2.py")),
    ("mismatch-v1", "check-completeness.py",
     _gate_mismatch("check-completeness.py")),
    ("absent-v2", "check-completeness-v2.py",
     _gate_absent("check-completeness-v2.py")),
    ("absent-v1", "check-completeness.py",
     _gate_absent("check-completeness.py")),
    ("directory-v2", "check-completeness-v2.py",
     _gate_directory("check-completeness-v2.py")),
    ("non-utf8-v1", "check-completeness.py",
     _gate_non_utf8("check-completeness.py")),
    ("empty-v2", "check-completeness-v2.py",
     _gate_empty("check-completeness-v2.py")),
)


def _run_gate_shape(label: str, name: str,
                    apply: Callable[[pathlib.Path], None]) -> dict[str, Any]:
    """The gated-pin refusal, proven rather than asserted, and proven with NO
    VALIDATION ATTEMPTED: the refusal must arrive as TrustRootIntegrityError
    from the gate, never as a report."""
    target = pathlib.Path(tempfile.mkdtemp(dir=TMP_ROOT, prefix=TMP_PREFIX))
    try:
        _stage(target)
        path = target / "artifacts" / name
        before = path.read_bytes()
        apply(target)
        if path.is_file() and path.read_bytes() == before:
            return {"label": label, "escape": True,
                    "reason": "the tamper applied without changing any byte"}
        try:
            validate(target)
        except TrustRootIntegrityError as exc:
            text = str(exc)
            ok = ("EVRH-GATE-01" in text and name in text
                  and RESOLVER_PINS[name] in text)
            return {"label": label, "escape": not ok,
                    "reason": "" if ok else
                    "refused, but the refusal did not name the file and its "
                    "gated pin"}
        except Exception as exc:                       # noqa: BLE001 - reported
            return {"label": label, "escape": True,
                    "reason": f"refused with {type(exc).__name__}, not with "
                              "the typed TrustRootIntegrityError"}
        return {"label": label, "escape": True,
                "reason": "tampered resolver bytes were executed instead of "
                          "refused"}
    finally:
        shutil.rmtree(target, ignore_errors=True)


# ---------------------------------------------------------------------------
# THE INPUT-REFUSAL PROBE (the IR-EVRH-B1 minimal repro, shipped as a standing
# probe).  Each shape must refuse the WHOLE RUN at exit 2 saying THE CHECK DID
# NOT RUN, with no report produced -- freeze section 7.8.1 rule 2.  It drives
# `run_validation`, which is the same single decision point `main()` drives, so
# the exit code a document CLAIMS is MEASURED to be the one the file PRODUCES
# (rule 3).
# ---------------------------------------------------------------------------
INPUT_REFUSAL_SHAPES: tuple[tuple[str, str, bytes], ...] = (
    ("non-object-root-array", HEAD_FILE, b"[]"),
    ("non-object-root-scalar", "evidence.v13.json", b"7"),
    ("not-json-at-all", "evidence.v11.json", b"{"),
)


def _run_input_refusal(label: str, name: str, payload: bytes) -> dict[str, Any]:
    target = pathlib.Path(tempfile.mkdtemp(dir=TMP_ROOT, prefix=TMP_PREFIX))
    try:
        _stage(target)
        (target / "artifacts" / name).write_bytes(payload)
        try:
            report, code, message = run_validation(target)
        except Exception as exc:                       # noqa: BLE001 - reported
            return {"label": label, "escape": True,
                    "reason": f"terminated as an uncaught "
                              f"{type(exc).__name__} instead of refusing"}
        ok = (report is None
              and code == EXIT["unsupportedInvocationOrInput"]
              and "THE CHECK DID NOT RUN" in message
              and name in message)
        return {"label": label, "escape": not ok,
                "reason": "" if ok else
                f"report={report is not None}, exit={code}, "
                f"message={message[:120]!r}"}
    finally:
        shutil.rmtree(target, ignore_errors=True)


# ---------------------------------------------------------------------------
# THE INJECTION SWEEP -- THE ORACLE FOR TOTALITY (header section 6).
#
# It calls the UNGUARDED layer functions directly, bypassing `run_layer`, so the
# totality net cannot mask an escape.  Zero unguarded escapes is the required
# result; anything else is EVRH-HOSTILE-01.
# ---------------------------------------------------------------------------
SWEEP_DEPTH_LIMITS: dict[str, int] = {"evidence.v10.json": 1}


def sweep_paths(value: Any, depth_limit: int | None) -> list[tuple]:
    """Root first, then every path at every object key and every array index,
    container positions and scalar leaf positions alike.  ITERATIVE."""
    out: list[tuple] = []
    stack: list[tuple[tuple, Any, int]] = [((), value, 0)]
    while stack:
        path, node, depth = stack[-1]
        del stack[-1]
        out.append(path)
        if depth_limit is not None and depth >= depth_limit:
            continue
        kind = j_type(node)
        if kind == "object":
            for key in reversed(m_keys(node)):
                stack.append((path + (key,), node[key], depth + 1))
        elif kind == "array":
            for index in range(len(node) - 1, -1, -1):
                stack.append((path + (index,), node[index], depth + 1))
    return out


def _node_at(document: Any, steps: tuple) -> tuple[bool, Any]:
    return resolve_steps(document, list(steps))


class _NotApplicable:
    """A sentinel distinct from every JSON value.

    `None` cannot serve here: `null` IS one of the head's sixteen injection
    classes and injecting it at the ROOT produces a document that IS None, so a
    None return would silently drop the single most important case in the sweep
    -- a document whose whole root is null.  Measured while building this
    sweep: with None as the sentinel the census was 6,345 cases; with this
    sentinel it is 6,351, and the six recovered cases are exactly `null` at the
    root of each of the six chain files.
    """

    def __repr__(self) -> str:                        # pragma: no cover - label
        return "<not-applicable>"


_NOT_APPLICABLE = _NotApplicable()


def _assign_at(document: Any, steps: tuple, new: Any) -> Any:
    if not steps:
        return new
    found, parent = resolve_steps(document, list(steps[:-1]))
    if not found or not has_step(parent, steps[-1]):
        return _NOT_APPLICABLE
    parent[steps[-1]] = new
    return document


def apply_injection(base: Any, steps: tuple, injection: str) -> Any:
    """Return the injected document, or `_NOT_APPLICABLE` when the injection
    does not apply at this position.  TOTAL."""
    document = copy.deepcopy(base)
    if injection == STRUCTURAL_INJECTION:
        found, node = _node_at(document, steps)
        if not found or j_type(node) != "object":
            return _NOT_APPLICABLE
        node[INJECTED_KEY] = "injected"
        return document
    return _assign_at(document, steps,
                      copy.deepcopy(INJECTION_VALUES[injection]))


def _sweep_canon(value: Any) -> str:
    token = j_canon(value)
    return token if token is not None else "<outside-json>"


def run_injection_sweep(root: pathlib.Path) -> dict[str, Any]:
    """Execute the head's own hostile-input space against the UNGUARDED layers.

    Returns a deterministic census.  A layer whose OWN ARGUMENTS are unchanged
    from the clean baseline cannot behave differently from the clean baseline,
    which raised nothing, so those invocations are counted as UNAFFECTED and
    skipped -- a structural fact about the call, since every layer takes exactly
    the documents it consumes as its arguments.
    """
    resolvers = gate_resolvers(root)
    base_chain = [read_document(root, name, pin) for name, pin in CHAIN_PINS]
    base_values = {document.name: document.value for document in base_chain}

    per_file: list[dict[str, Any]] = []
    escapes: list[str] = []
    total_cases = 0
    total_noops = 0
    total_invocations = 0
    total_unaffected = 0

    for name, _pin in CHAIN_PINS:
        base_value = m_get(base_values, name)
        baseline_token = _sweep_canon(base_value)
        paths = sweep_paths(base_value, m_get(SWEEP_DEPTH_LIMITS, name, None))
        cases = 0
        noops = 0
        skipped = 0
        file_escapes = 0
        for steps in paths:
            for injection in INJECTION_NAMES:
                document = apply_injection(base_value, steps, injection)
                if document is _NOT_APPLICABLE:
                    continue
                if _sweep_canon(document) == baseline_token:
                    noops += 1
                    continue
                cases += 1
                chain = [item._replace(value=document) if item.name == name
                         else item._replace(value=copy.deepcopy(item.value))
                         for item in base_chain]
                layers = (chain_layers(chain, resolvers, CHAIN_PINS)
                          + resolution_layers(chain, resolvers))
                for layer in layers:
                    if name not in layer.consumes:
                        skipped += 1
                        continue
                    total_invocations += 1
                    try:
                        layer.call()
                    except DECLARED_EXCEPTIONS:
                        pass                           # this file's OWN refusals
                    except BaseException as exc:       # noqa: BLE001 - the census
                        file_escapes += 1
                        if len(escapes) < 12:
                            escapes.append(
                                f"{name} {render_path(steps)} [{injection}] "
                                f"-> {layer.name} raised "
                                f"{type(exc).__name__}: {str(exc)[:80]}")
        total_cases += cases
        total_noops += noops
        total_unaffected += skipped
        per_file.append({"file": name, "paths": len(paths), "cases": cases,
                         "noops": noops, "unaffected": skipped,
                         "escapes": file_escapes})
    return {
        "perFile": per_file,
        "cases": total_cases,
        "noops": total_noops,
        "layerInvocations": total_invocations,
        "unaffectedInvocations": total_unaffected,
        "escapes": sum(int(item["escapes"]) for item in per_file),
        "escapeDetail": sorted(escapes),
        "vocabulary": sorted(INJECTION_NAMES),
    }


def sweep_findings(census: dict[str, Any]) -> list[Finding]:
    """The sweep's own typed class.  Named in header section 6 and EMITTED here,
    so the citation is carried rather than mentioned."""
    if not m_get(census, "escapes", 0):
        return []
    return [Finding(
        "EVRH-HOSTILE-01",
        "the injection sweep measures ZERO unguarded escapes: every one of the "
        "head's sixteen injection classes, at every enumerated path, leaves "
        "every UNGUARDED checking layer returning a deterministic result "
        "rather than raising (resolved head hostileInputTotalityContract.rule; "
        "the layers are called without the EVRH-TOTAL-01 net so it cannot mask "
        "an escape)",
        f"{m_get(census, 'escapes', 0)} unguarded escape(s) over "
        f"{m_get(census, 'cases', 0)} executed cases: "
        f"{m_get(census, 'escapeDetail', [])}")]


def _run_sweep_probe(root: pathlib.Path) -> dict[str, Any]:
    try:
        census = run_injection_sweep(root)
    except Exception as exc:                           # noqa: BLE001 - reported
        return {"label": "hostile-input-sweep", "escape": True, "census": None,
                "reason": f"the sweep itself raised {type(exc).__name__}: {exc}"}
    return {"label": "hostile-input-sweep", "escape": bool(census["escapes"]),
            "census": census,
            "reason": "" if not census["escapes"] else
            f"{census['escapes']} unguarded escape(s)"}


# ---------------------------------------------------------------------------
# THE CLASS-COVERAGE PROBE (the IR-EVRH-A3 repair).
#
# The predecessor's shipped battery exercised 14 of its 36 typed classes; its
# review had to fire the other 22 by hand to establish that none was vacuous.
# That measurement belongs in the instrument, not in a verdict a later reader
# has to go and find.  Here every class the file DECLARES -- read from its own
# syntax tree, never transcribed -- must be required by some probe in the
# shipped suite, and every class no artifact mutation can reach is fired by
# DIRECT CALL against a planted input.
#
# The planted inputs are the point: a scan or a check that has only ever been
# observed to pass is indistinguishable from one that measures nothing.
# ---------------------------------------------------------------------------
def declared_finding_classes(tree: ast.Module) -> set[str]:
    """Every typed class this file declares, READ FROM ITS OWN TREE."""
    pattern = re.compile(r"EVRH-[A-Z0-9]+-[0-9]+")
    return {node.value for node in ast.walk(tree)
            if isinstance(node, ast.Constant) and isinstance(node.value, str)
            and pattern.fullmatch(node.value)}


def _probe_document(name: str, value: Any) -> Document:
    return Document(name=name, raw=b"", measured="0" * 64, declared="0" * 64,
                    value=value, duplicate=None)


def _divergent_serialiser(resolvers: Resolvers) -> Resolvers:
    stub = types.ModuleType("_probe_divergent_serialiser")
    stub.canonical_bytes = lambda value: b"a divergent canonical serialisation"
    return Resolvers(r1=resolvers.r1, r2=stub, measured={})


def _probe_accounting_chain() -> list[Document]:
    head = _probe_document(HEAD_FILE, {
        "derivedFrom": {"operations": [
            {"op": "remove", "path": "/a", "from": 1, "value": 2}]},
        "operationAccounting": {name: 0 for name in ACCOUNTING_MEMBERS}})
    return [head, _probe_document(TERMINUS_FILE, {"a": 1})]


def class_probes(resolvers: Resolvers) -> tuple[
        tuple[str, str, Callable[[], list[Finding]]], ...]:
    """Direct-call proofs for the classes no artifact mutation can reach."""
    return (
        ("EVRH-TOTAL-01", "a checking layer that raises",
         lambda: run_layer("planted-raising-layer", lambda: 1 // 0)),
        ("EVRH-TOTAL-02", "a total accessor that is not total",
         lambda: accessor_totality(
             (("planted-raw-accessor", lambda node: node.get("k")),), ())),
        ("EVRH-GATE-02", "a candidate the REVIEWED gated resolver cannot consume",
         lambda: check_terminus(_probe_document(TERMINUS_FILE, []), resolvers)),
        ("EVRH-SHAPE-01", "a chain document whose root is not a JSON object",
         lambda: check_documents([_probe_document(HEAD_FILE, [])])),
        ("EVRH-SHAPE-02", "a leaf outside the RFC 8259 value universe",
         lambda: check_path_domain(
             [_probe_document(HEAD_FILE, {"a": float("nan")})])),
        ("EVRH-PATH-01",
         "THE PREDECESSOR'S OWN `/`-join encoder, which is not injective",
         lambda: path_encoding_findings(naive_join_encode, decode_path)),
        ("EVRH-PATH-02", "a leaf path with a step outside the JSON key domain",
         lambda: check_path_domain(
             [_probe_document(HEAD_FILE, {"a": {(1, 2): "x"}})])),
        ("EVRH-HOSTILE-01", "an unguarded escape in the injection sweep",
         lambda: sweep_findings({"escapes": 1, "cases": 1, "escapeDetail": [
             "planted escape, so the sweep's own finding class is shown to "
             "fire"]})),
        ("EVRH-HOSTILE-02", "an injection vocabulary that is not the head's",
         lambda: check_mode_contract(
             {"checkerModeContract": {},
              "hostileInputTotalityContract": {"injections": ["null"]}})),
        ("EVRH-HOSTILE-03", "a totality rule the head no longer states",
         lambda: check_mode_contract(
             {"checkerModeContract": {},
              "hostileInputTotalityContract": {"rule": "not the rule"}})),
        ("EVRH-HOSTILE-04", "a layer census the sweep does not enumerate",
         lambda: check_layer_census({"chain": 0, "resolution": 0,
                                     "resolved": 0})),
        ("EVRH-CANON-02", "a divergent gated canonical serialiser",
         lambda: check_canonical({}, _divergent_serialiser(resolvers))),
        ("EVRH-CANON-03", "an emission stream that is not payload-plus-newline",
         lambda: check_canonical({}, resolvers)),
        ("EVRH-SECT-02", "a resolved top-level key census that is not the gated one",
         lambda: check_canonical({}, resolvers)),
        ("EVRH-CHAIN-04", "a provenance walk that is not the pinned chain",
         lambda: check_provenance({"predecessor": "artifacts/nowhere.json",
                                   "measuredDigest": "0" * 64},
                                  "planted", CHAIN_PINS)),
        ("EVRH-CHAIN-06", "two resolutions that disagree",
         lambda: check_agreement({"a": {"x": 1}, "b": {"x": 2}})),
        ("EVRH-CLI-01", "a planted battery expectation",
         lambda: argument_discipline_findings((("planted", ["x"], False),))),
        ("EVRH-MODE-01", "a head exit code this instrument does not implement",
         lambda: check_mode_contract(
             {"checkerModeContract": {"exitCodes": {"clean": 9}}})),
        ("EVRH-MODE-02", "a head that declares no entrypoints",
         lambda: check_mode_contract({"checkerModeContract": {}})),
        ("EVRH-MODE-03", "a head that carries no exitCodesNote",
         lambda: check_mode_contract({"checkerModeContract": {}})),
        ("EVRH-MODE-04", "a head that no longer binds the exitDiscipline",
         lambda: check_mode_contract({"checkerModeContract": {}})),
        ("EVRH-GRAM-01", "a resolved contract with no wire grammar",
         lambda: check_grammar({})),
        ("EVRH-GRAM-02", "a record set that is not the declared five",
         lambda: check_grammar(
             {"canonicalWireGrammar": {"records": {"NotARecord": 7}}})),
        ("EVRH-GRAM-03", "a tag registry that is not a list",
         lambda: check_grammar({"canonicalWireGrammar": {"tagRegistry": 7}})),
        ("EVRH-GRAM-04", "a grammar block whose member set is not closed",
         lambda: check_grammar({"canonicalWireGrammar": {"recordRules": 7}})),
        ("EVRH-GRAM-05", "a const scalar that is not a type-exact int",
         lambda: check_grammar({"canonicalWireGrammar": {"records": {
             "RawProofInventoryItemV1": {"required": ["f"], "fields": [
                 {"name": "f", "const": 1.0}]}}}})),
        ("EVRH-XFER-01", "a transfer list that is not a list",
         lambda: check_transfers({"reviewFindingTransfers": 7})),
        ("EVRH-ACCT-02", "an operation verb outside the resolver's verb set",
         lambda: check_accounting(_probe_accounting_chain())),
        ("EVRH-RES-01", "a residual list that is not a list",
         lambda: check_residuals({"retainedResiduals": 7})),
        ("EVRH-ITEM4-01", "an item-4 block absent from the resolved contract",
         lambda: check_item4({}, [_probe_document(TERMINUS_FILE, {})])),
        ("EVRH-HEAD-02", "a head leaf that does not resolve",
         lambda: check_head_leaves(_probe_document(HEAD_FILE, {}))),
        ("EVRH-CHAIN-05", "a terminus that grew a derivation",
         lambda: check_terminus(_probe_document(TERMINUS_FILE, {
             "derivedFrom": {"artifact": "x", "sha256": "0" * 64,
                             "operations": [
                                 {"op": "set", "path": "/a", "from": 1,
                                  "value": 2}]}}), resolvers)),
    )


def _run_class_probes(resolvers: Resolvers) -> dict[str, Any]:
    """Fire every directly-probed class and check the coverage of ALL of them."""
    probes = class_probes(resolvers)
    misfires: list[str] = []
    for required, description, call in probes:
        try:
            produced = {item.id for item in call()}
        except Exception as exc:                       # noqa: BLE001 - reported
            misfires.append(f"{required} ({description}) raised "
                            f"{type(exc).__name__}: {exc}")
            continue
        if required not in produced:
            misfires.append(f"{required} ({description}) did not fire; the "
                            f"probe produced {sorted(produced)}")
    declared = declared_finding_classes(own_tree())
    covered = ({required for required, _d, _c in probes}
               | {item for mutation in MUTATIONS for item in mutation.required}
               | {required for _l, _a, required, _d in SOURCE_MUTATIONS}
               | {"EVRH-GATE-01"})
    uncovered = sorted(declared - covered)
    return {"label": "class-coverage", "escape": bool(misfires or uncovered),
            "probes": len(probes), "declared": len(declared),
            "covered": len(declared & covered), "uncovered": uncovered,
            "misfires": misfires,
            "reason": "" if not (misfires or uncovered) else
            f"{len(misfires)} misfire(s), {len(uncovered)} uncovered class(es)"}


# The whole battery: the artifact mutations, the source self-mutations, the
# seven gate shapes, the three input-refusal shapes, the injection sweep and the
# class-coverage probe.  ONE constant so the refusal banner and the pass census
# cannot quote different totals.
MUTATION_CENSUS = (len(MUTATIONS) + len(SOURCE_MUTATIONS) + len(GATE_SHAPES)
                   + len(INPUT_REFUSAL_SHAPES) + 2)


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
        print(f"SELFTEST-NOT-RUN: 0 of {MUTATION_CENSUS} probes executed; "
              f"exit {EXIT['selftestRefusedDirtyBase']} distinguishes this "
              "refusal from a green selftest and from an ordinary failure.")
        return EXIT["selftestRefusedDirtyBase"]

    baseline = frozenset(item.id for item in base.findings)
    print(f"mutation self-test -- {SUBJECT} resolved head, TOTAL over hostile "
          "parsed JSON")
    print("  every probe runs in a DISPOSABLE copy under /tmp; the live tree "
          "is never written to")
    print("  ESCAPE RULE: a mutation that fails to apply, or that applies "
          "without changing bytes,")
    print("  or that does not produce every required finding ID, is an ESCAPE "
          "-- never a pass")
    results = [_run_mutation(mutation, baseline) for mutation in MUTATIONS]
    caught = sum(1 for item in results if not item["escape"])
    for mutation, result in zip(MUTATIONS, results):
        status = "ESCAPE" if result["escape"] else "caught"
        print(f"  {status:<6} {mutation.label:<32} mutates "
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
        print(f"  {status:<6} {result['label']:<32} mutates this file's own "
              f"syntax tree: {result['description']}")
        print(f"         required {result['required']}; scan reported "
              f"{result['produced']}")
        if result["escape"]:
            print(f"         {result['reason']}")

    gate_results = [_run_gate_shape(*shape) for shape in GATE_SHAPES]
    gate_caught = sum(1 for item in gate_results if not item["escape"])
    for result in gate_results:
        status = "ESCAPE" if result["escape"] else "caught"
        print(f"  {status:<6} {'gate:' + result['label']:<32} tampers the "
              "gated resolver bytes")
        print(f"         required a typed TrustRootIntegrityError naming "
              f"EVRH-GATE-01 and the gated pin, terminating at exit "
              f"{EXIT[SUCCESSOR_EXIT_NAME]} with NO validation attempted"
              f"{'' if not result['escape'] else '; ' + result['reason']}")

    refusal_results = [_run_input_refusal(*shape)
                       for shape in INPUT_REFUSAL_SHAPES]
    refusal_caught = sum(1 for item in refusal_results if not item["escape"])
    for result in refusal_results:
        status = "ESCAPE" if result["escape"] else "caught"
        print(f"  {status:<6} {'input:' + result['label']:<32} makes a "
              "REQUIRED input one this file does not accept")
        print(f"         required a whole-run refusal at exit "
              f"{EXIT['unsupportedInvocationOrInput']} saying THE CHECK DID "
              f"NOT RUN, with no report and no banner (freeze 7.8.1 rule 2)"
              f"{'' if not result['escape'] else '; ' + result['reason']}")

    sweep = _run_sweep_probe(root)
    sweep_ok = not sweep["escape"]
    print(f"  {'caught' if sweep_ok else 'ESCAPE':<6} "
          f"{'hostile-input-sweep':<32} injects the head's OWN sixteen-class "
          "vocabulary")
    census = sweep["census"]
    if census is None:
        print(f"         {sweep['reason']}")
    else:
        print("         boundary: evidence.v11..v15 at EVERY path at "
              "unlimited depth; evidence.v10.json at depth <= 1")
        print(f"         vocabulary {census['vocabulary']}")
        for row in census["perFile"]:
            print(f"           {row['file']:<20} {row['paths']:>5} paths  "
                  f"{row['cases']:>5} cases  {row['noops']:>4} no-op  "
                  f"{row['unaffected']:>6} unaffected  "
                  f"{row['escapes']:>3} escape(s)")
        print(f"         {census['cases']} executed cases, "
              f"{census['layerInvocations']} unguarded layer invocations, "
              f"{census['escapes']} unguarded escape(s)")
        print("         the layers are called UNGUARDED, so the EVRH-TOTAL-01 "
              "net cannot mask an escape")
        for finding in sweep_findings(census):
            print("         -", finding.render())

    coverage = _run_class_probes(gate_resolvers(root))
    coverage_ok = not coverage["escape"]
    print(f"  {'caught' if coverage_ok else 'ESCAPE':<6} "
          f"{'class-coverage':<32} fires every class no artifact mutation "
          "reaches, by DIRECT CALL")
    print(f"         {coverage['probes']} direct probes; "
          f"{coverage['covered']}/{coverage['declared']} declared classes "
          "required by some probe in this suite (IR-EVRH-A3)")
    print("         the classes read from this file's OWN syntax tree, never "
          "transcribed; NO CLASS IS VACUOUS")
    for line in coverage["misfires"]:
        print(f"         MISFIRE {line}")
    if coverage["uncovered"]:
        print(f"         UNCOVERED {coverage['uncovered']}")

    total = MUTATION_CENSUS
    caught_total = (caught + source_caught + gate_caught + refusal_caught
                    + (1 if sweep_ok else 0) + (1 if coverage_ok else 0))
    print(f"  census: {caught_total}/{total} caught, "
          f"{total - caught_total} escape(s)")
    print("  scope, per the resolved head's retainedResiduals[13]: the "
          "artifact mutations, the gate")
    print("         and input probes, and the injection sweep are the SEMANTIC "
          "oracle. The five source")
    print("         mutations prove only that the EVRH-MODE-05/06/07 and "
          "EVRH-GUARD-01 tripwires FIRE --")
    print("         they remain SYNTACTIC, for their measured coverage only, "
          "and the head's recorded")
    print("         evasions of this scan family are inherited here and are "
          "NOT claimed closed.")
    if caught_total != total:
        return EXIT["findings"]
    print(f"SELFTEST-PASS: {caught_total}/{total} probes caught")
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
    ("none-vector", None, False),
    ("flag-is-not-a-string", ["x", 7, 8], False),
)


def check_argument_discipline() -> list[Finding]:
    return argument_discipline_findings(ARGUMENT_BATTERY)


def argument_discipline_findings(
        battery: Iterable[tuple[str, Any, bool]]) -> list[Finding]:
    findings: list[Finding] = []
    for label, argv, accepted in battery:
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
    print(f"EVIDENCE resolved-head validator (TOTAL) -- subject {SUBJECT} "
          f"({dict(CHAIN_PINS)[HEAD_FILE][:16]}…)")
    print(f"  successor to {PREDECESSOR} ({PREDECESSOR_SHA256[:16]}…), "
          "repairing IR-EVRH-B1 and six advisories")
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
    print(f"  --emit-resolved stream: {RESOLVED_STREAM_SHA256} "
          f"({RESOLVED_STREAM_BYTES} bytes = the canonical payload above plus "
          "one terminator newline)")
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
    print("  disclosed residuals (header section 7): the 34 unpinned top-level "
          "keys of the")
    print("    resolved contract; the self-scan blind spots carried from the "
          "head's residual 13")
    print("    and WIDENED, not narrowed; the guard scan does not scan "
          "subscripts; deep")
    print("    recursion becomes a typed EVRH-TOTAL-01 finding rather than a "
          "measured class;")
    print("    evidence.v10.json below depth 1 is not swept.")


def main(argv: list[str]) -> int:
    try:
        flags, requested = parse_argv(argv)
    except UnsupportedInvocation as exc:
        print(f"EVRH-UNSUPPORTED-INVOCATION: {exc}", file=sys.stderr)
        return EXIT["unsupportedInvocationOrInput"]
    root = pathlib.Path(requested).resolve() if requested is not None \
        else HERE.parent

    if "--emit-resolved" in flags:
        report, code, message = run_validation(root)
        if report is None:
            print(message, file=sys.stderr)
            return code
        if report.resolved is None:
            print("EVRH-INPUT: the effective contract could not be "
                  "materialised; nothing is emitted", file=sys.stderr)
            return EXIT["unsupportedInvocationOrInput"]
        # A write failure on the emission sink -- a closed pipe being the
        # ordinary case -- must NOT propagate as an uncaught traceback at
        # exit 1.  That is the defect shape freeze section 7.8.1 names D-6 and
        # the one IR-EVRH-B1 measured on three other paths in the predecessor;
        # header section 5 states the four mechanisms that close it there.
        try:
            sys.stdout.buffer.write(canonical_bytes(report.resolved))
            sys.stdout.buffer.write(EMIT_TERMINATOR)
            sys.stdout.buffer.flush()
        except OSError as exc:
            print(f"EVRH-INPUT: the emission sink could not be written "
                  f"({type(exc).__name__}); nothing was emitted", file=sys.stderr)
            return EXIT["unsupportedInvocationOrInput"]
        return EXIT["clean"]

    if "--selftest" in flags:
        return selftest(root)

    report, code, message = run_validation(root)
    if report is None:
        print(message, file=sys.stderr)
        return code

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
          f"residuals, {TRANSFER_COUNT} transfers checked; every layer total "
          "over hostile parsed JSON")
    print_scope()
    return EXIT["clean"]


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
