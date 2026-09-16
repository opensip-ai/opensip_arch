# 10 — Method

**Purpose:** how the claims in these documents were established, the rules that
govern them, and the errors made along the way — recorded because an architecture
document that hides its authors' mistakes gives the reader no way to calibrate
the rest.

Measurements of the *existing* implementation are **not** here. They live in
`../steering/01-current-state-evidence.md`, because they describe porting cost,
not design merit. Keeping them out of this tree is the point of the split.

---

## Method rules

**SEALED.** Learned the hard way during the deliberation.

### 1. Capability claims require closure tracing, not lexical call-site counts

Any claim of the form "N components use capability X" must trace **import and
call closure**, not grep for X's direct call sites. Where the tooling exists,
this is exactly what reference and caller queries are for.

### 2. No in-language signature is a capability boundary

Where ambient module resolution exists, authority is whatever the resolver and
runtime permit, not what a function declares.

**The test:** can the code obtain the capability by any path other than the one
granted — static import, dynamic import, `require`, filesystem, environment,
globals, or a transitive dependency? If yes, it is a convention.

### 3. Decisions close by artifact — at the altitude of the decision

<!-- disposition:METHOD.ALTITUDE -->
*(**METHOD.ALTITUDE** — the former **CANDIDATE** claim is
**NARROWED TO PROCESS GUIDANCE**, not sealed as a product or assurance claim. The
terminal disposition is binding in
`../artifacts/method-claim-dispositions.v1.json`.)*

A week-one decision is not closable until its governing choice is represented by
a checkable object. Checkability is necessary, not sufficient: review,
adjudication, consequence coverage, and the binding handoff still apply. Prose
agreement alone is how a deliberation reaches 200 KB with nothing executable in
it.

**Corrected after independent review.** As first stated this rule rewarded
artifacts that were easy to check, and detailed schemas are often easier to check
than architectural boundaries. The earlier 82%/33% estimates are withdrawn as
decision evidence: they measured document form with no reproducible classifier.

Altitude is determined by **consequence**: blast radius, external custody,
ownership boundary, reversibility, and who pays the change cost. An architectural
decision normally closes with an invariant, a responsibility boundary, an
ownership assignment, or a falsifying counterexample. A schema is detailed when
it merely implements a boundary already chosen; it is architectural when its exact
compatibility semantics **are** the externally held boundary. Field names and
hashes are therefore neither automatically architecture nor automatically detail.

For consumer B, a fork that an implementer would otherwise decide in week one
closes with **both** a governing invariant/falsifier and a binding implementation
contract. This is implementation-package guidance only. It does not prove that a
particular artifact is complete, reviewed, qualified, or demonstrated.

### 4. Internal consistency is not conformance

An artifact can be mechanically valid, internally coherent, and still silently
drop a sealed property from an earlier phase. Every artifact carries a
back-reference listing the decisions it must encode, and review checks that list.

### 5. Agreement between reviewers using the same instrument is not corroboration

See Error 1.

### 6. Measuring an existing implementation does not size a greenfield decision

**The rule this document set was restructured to enforce.** A measurement of a
shipping system tells you what it costs to *port* that system. It does not tell
you what a good design would choose, because the existing artifact was shaped by
constraints the new design does not have.

The tell is a sentence of the form *"only N% of today's X do Y, therefore the
design should treat Y as rare."* If today's system made Y expensive or
impossible, N measures the old constraint, not the requirement.

### 7. Do not seal what you have flagged for review

A claim cannot be simultaneously "settled, do not re-deliberate" and "please
challenge this." If it is open enough to challenge, it is not settled enough to
build on — and **never use an unreviewed claim as a premise for another
decision**, because the second decision inherits the first's uncertainty without
inheriting its review status.

### 8. Status attaches to claims, not containers

<!-- disposition:METHOD.CLAIM-STATUS-INTEGRITY -->
*(**METHOD.CLAIM-STATUS-INTEGRITY** — the former **CANDIDATE** broad completeness
claim is **ABANDONED**. `check-claims.py` remains a bounded diagnostic; it is not
whole-tree semantic proof. The terminal disposition is binding in
`../artifacts/method-claim-dispositions.v1.json`.)*

A container's status marker silently promotes its contents: a section headed
SEALED that restates a candidate claim gives that claim two statuses depending on
where the reader looks. **Where a container carries a status, that status is the
minimum (weakest) of the claims inside it**, and a summary restating a candidate
must mark the clause inline.

This rule exists because instance-fixing failed three times (Error 5 and its two
recurrences). The register remains the single source for the live claims it
contains. `check-claims.py` checks its declared Markdown locations, dependencies,
product dispositions, a bounded lexical restatement set, and versioned filename
citations. It does **not** discover every semantic restatement or interpret status
inside arbitrary JSON. Surface-local checkers plus registered reviews and
adjudications remain the authority for those claims.

---

## Worked errors

### Error 1 — "no rule consumes the type checker"

A lexical search for direct compiler-checker call sites returned zero hits in the
rule packs, and this was reported as "essentially no rules need type fidelity."

**Wrong.** Authority flowed through a two-hop wrapper chain whose intermediate
name contained none of the searched substrings.

**Caught by:** a second reviewer tracing the import closure instead of repeating
the search.

**Aggravating factor:** a third reviewer independently *spot-checked* the claim,
reproduced the same search, and **confirmed the error**. Agreement between
reviewers using the same instrument is not corroboration — it is a correlated
blind spot.

### Error 2 — "the escape hatch is enforced by signature"

The claim was that an analyzer receiving a compiler handle as a parameter cannot
construct one.

**Wrong.** The module imports the compiler directly, and the compiler is a
declared runtime dependency. Ambient module authority defeats any in-language
signature.

**The pattern.** Errors 1 and 2 are the same shape — **a global property inferred
from a local form** — and the second was committed *in the same turn* that
articulated the rule against it.

**Consequence for the architecture, not just the process:** if reviewers who have
just stated a rule still violate it, the rule tiering must be **enforced by
tooling, not discipline**. That is why [05](05-rules-and-extensions.md) classifies
rules by predicate rather than by parser — a design requirement derived from an
observed human failure mode.

### Error 3 — "download counts settle whether sub-packages have consumers"

**Wrong.** A meta-package depending on its workspace packages makes every count
converge. The discriminating signal is **dependents**, not downloads.

### Error 4 — migration reasoning presented as greenfield design

**The largest error, and structural rather than factual.** A scoping note about
not rewriting an existing product hardened into a design constraint. Decisions
were justified by porting cost; one measurement of the existing corpus was used
to size a greenfield tier; and an entire workstream answered a question that had
not been asked.

**Caught by:** the coordinator — not by any of the three reviewers, all of whom
had been reasoning inside the wrong frame for several turns without noticing.

**Remedy:** this document set was split into `architecture/` and `steering/`, and
four decisions were re-derived. Three changed only in justification; one
([08](08-surfaces-and-topology.md) topology) reopened outright. What moved is
recorded in [00-overview](00-overview.md).

**Generalisation, now method rule 6:** a constraint inherited from a prior
discussion must be re-tested against the current question, not carried forward on
the assumption that it still applies. Framing errors are invisible from inside
the frame, and peer review does not catch them when every peer shares it.

### Error 5 — a circular seal

While filing "semantics is the primary fact tier" as an open question for
adversarial review, the same author simultaneously wrote it into the SEALED
thesis and into the do-not-redeliberate list, then used it as the premise for
reopening a *different* prior seal (execution topology).

**Wrong three times over:** the claim was underived, it was marked
unchallengeable while explicitly under challenge, and a second decision was made
to depend on it.

**Caught by:** the reviewing agent auditing document consistency, not by the
author, who had written all three statements within one editing pass.

**The pattern.** Same shape as Errors 1, 2 and 4 — a local convenience (wanting a
summary paragraph to read cleanly) silently created a global property nobody
authorised. That is now four instances of *local form producing an unintended
global claim*, which is enough to treat it as the dominant failure mode of this
exercise rather than a series of accidents.

**Remedy attempt 1 (insufficient):** method rule 7, and a `CANDIDATE (C-n)`
marker distinguishing "sealed" from "re-derived but unreviewed."

**It recurred twice more.** The next audit found the replacement C-1 wording
sitting inside the still-SEALED thesis paragraph, and a SEALED product-boundary
row choosing a semantic provider while that decision was formally open. Each
repair had fixed the occurrence the auditor cited; none had stated the invariant,
so the next edit reintroduced it somewhere new.

**Remedy attempt 2 (structural, later narrowed):** method rule 8, plus a
machine-checked claim register (`../artifacts/claim-register.v1.json`,
`../artifacts/check-claims.py`). Status lives in one place per registered live
claim, and the checker catches the encoded placement/version mutations. The
former **CANDIDATE** `METHOD.CLAIM-STATUS-INTEGRITY` claim that this was complete
document-set enforcement is now abandoned; Error 6 and its follow-up reviews
showed that stronger reading false.

**Honest note on the checker:** its first run against the live documents produced
three findings, **all three false positives** — the retirement context ("that
argument is withdrawn") followed the quoted phrase rather than preceding it, and
the inline-mark pattern was too narrow. The fix was to the checker, not to the
documents. A validator that cries wolf is worse than none, which is the same
failure this architecture designs against in the ratchet
([06](06-evidence-and-persistence.md)).

### Error 6 — the status checker was blind to 54 of its 55 locations

`check-claims.py` was cited all session as evidence that no claim was presented
above its registered status. Reviewer B audited the checker itself and found the
location check ran only where a claim carried a hand-added `_probe`. Exactly one
of thirty claims had one.

**Measured: 1 location examined, 54 silently skipped**, while the tool printed
"30 claims, CHK-1..CHK-4 clean" — output that reads as coverage and wasn't. Adding
a single probe immediately surfaced two real violations, one of them on
`METHOD.CLAIM-STATUS-INTEGRITY` itself: **the claim asserting status integrity was
in violation of status integrity.**

Three compounding defects, all mine:

1. **Coverage was opt-in.** A missing anchor was a `continue`, not a finding.
2. **The self-test proved a happy path.** It asserted three expected findings
   appeared, never that every required location was examined — so it passed while
   the dominant failure mode was total.
3. **The inline-mark pattern only recognised `C-n`/`R-n`/`P-n` ids**, so claims
   like `D9` and `ARCH.PROBE-CONTRACT` could not be marked at all. The check was
   *unsatisfiable* for them, not merely unsatisfied.

**Remedy:** anchors are derived from the fragments the register already carries, so
coverage is a property of the data rather than a manual step; unresolvable
locations are `CHK-0` findings; the run prints actual coverage counts; the
self-test asserts that unexamined locations equal reported ones; the inline marker
is claim-id-aware; and `CHK-5` catches prose citing a superseded binding artifact
(`07` was two versions stale while the register was correct).

**The generalisation, which is the part that matters:** *a checker's silence means
nothing until you know what it examined.* Report coverage, not just verdicts. Four
of the six recorded errors in this exercise were invisible to a passing check;
this one was invisible **because** of a passing check. Later audits still found
semantic and artifact-JSON blind spots after the mechanical repairs, so the broad
completeness claim was abandoned rather than paper-sealed.

---

## Known gaps in the evidence base

These bound how much any claim in this tree should be trusted.

1. **No working graph evidence.** The analysis client was bound to the wrong
   project root throughout. Every claim rests on direct source measurement or
   reasoning — and Error 1 is precisely what the unavailable caller and reference
   queries would have caught in one step.
2. **Source briefs deleted.** Two appendices were reconstructed and are labelled
   as such; they must be re-derived before adoption.
3. **The declarative/imperative split is unmeasured** against a real fact schema.
   Any figure derived from the existing corpus measures the old constraint.
4. **Scale behaviour is extrapolated** past a small measured tier.
