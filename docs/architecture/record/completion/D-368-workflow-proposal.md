# D-368 — Reciprocal review and integrated architecture closure

Status: PROPOSED. Author: Codex. No readiness effect until adoption.

## Problem and authority

D-367 authorizes Codex and Claude to make all architecture decisions and review
each other's work. The previous three-agent procedure required two independent
reviewers beyond the author and separate application and recording cycles.
This proposal makes the two-agent procedure explicit, preserving independent
challenge while reducing duplicated recording work. It is a scoped successor
to D-000's operational review practice, the historical orchestrator handoff's
dual Stage A/Stage B rule, the fixed Claude-author/Codex-reviewer assignment in
RECOMMENDATION-PROTOCOL, and D-056 eligibility 4–5's separate-cycle sequencing.

## Decision proposed

1. The author supplies a concrete contract or decision, source references,
   alternatives, consequences, executable design evidence where applicable, and
   explicit supersessions. The other agent independently reviews the fixed
   bytes and attempts counterexamples. Author assent and reviewer assent must
   both be recorded; only the latter is called independent review. There is
   one independent reviewer, not two fabricated independent verdicts.
2. The pair can exchange authorship across bounded work packages. Codex owns
   integration and ensures the exact integrated bytes are reviewed. A material
   integration change receives renewed review. Findings name a concrete defect,
   its consequence, and the evidence required to resolve it. Editorial fixes
   can be recorded without restarting unrelated technical decisions.
3. A review package may cover related rows. For EACH row it must separately
   state: applied contract and digest; prior obligations and dispositions;
   application-grade acceptance; D-056 gate-2/gate-3 finding; SATISFIED-GRADE
   verdict; and the exact proposed register edit. A package-wide ACCEPT cannot
   close a row lacking its own verdict. Contract application, delegated Class A
   opening, and MF-6 can be recorded in one integrated act after review rather
   than serial cycles. D-056's substantive evidence requirements stand.
4. All unresolved MUST-FIX and SHOULD-FIX findings prevent adoption. Three
   exchanges per decision remain the limit. A persistent split is recorded
   CONTESTED and the pair works another surface or obtains an independent
   adjudication; disagreement is not manufactured into consensus. New work
   cannot evade the limit by merely renumbering the same unresolved proposal.
5. Frozen reviewed files and source digests are retained. Each adopted decision
   records its authority, author, reviewer verdict and hash, changed acceptance
   clauses, remaining qualification work and reversal procedure. Commit/push
   remains per coherent adopted decision under D-000/D-293. Source authority
   changes require explicit supersession; latest filename is not authority.
6. Every existing row remains in D-002's affected or deferral set. This act
   changes no threshold, fixture obligation, product behavior or row standing.
   Release qualification and V1 freeze remain separate from architecture
   completion. D-367 enables owner decisions, not evidence-free closure.

## Alternatives and tradeoff

- Retain a third author plus two independent reviewers: more independent eyes,
  but inconsistent with the requested direct two-agent collaboration as the
  default and a repeated source of duplicate process work. Additional reviewers
  remain available for an unresolved technical dispute or final audit.
- Let the author self-certify: rejected. No independent challenge.
- Collapse review to one global verdict: rejected. Loses row-specific evidence.

One independent reviewer offers less redundancy than two. Fixed inputs,
bidirectional authorship, explicit row verdicts, concrete design examples and a
separate integrated audit mitigate that loss without misrepresenting it.

## Reversibility

Revoke this workflow prospectively and restore the prior independent-review
count and serial cycles. Existing acts retain their accurately recorded review
provenance. Requiring their re-review must be stated explicitly; history is not
rewritten. No readiness count changes on adoption of this workflow.
