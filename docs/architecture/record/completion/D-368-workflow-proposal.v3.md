# D-368 — Reciprocal review and integrated architecture closure

Status: PROPOSED. Author: Codex. No readiness effect until adoption.

## Problem and authority

D-367 authorizes Codex and Claude to make all architecture decisions and review
each other's work. The previous three-agent operational practice used two independent
reviewers beyond the author and separate application and recording cycles.
This proposal makes the two-agent procedure explicit, preserving independent
challenge while reducing duplicated recording work. It is a scoped successor
to D-000's operational review practice, the historical orchestrator handoff's
dual Stage A/Stage B rule, the fixed Claude-author/Codex-reviewer assignment in
RECOMMENDATION-PROTOCOL, and D-056 eligibility 4–5's separate-cycle sequencing.

## Decision proposed

1. The author supplies a concrete contract or decision, source references,
   alternatives, consequences, executable design evidence where applicable, and
   explicit supersessions. Every fixture corpus includes a retained checker and
   a digest-pinned passing report at recording. This mandate is prospective;
   an older corpus relied upon by a new SATISFIED package receives a retained
   checker and passing report in that package, without rewriting its history. Each reviewed unit has exactly
   one recorded author; its independent reviewer authored none of its bytes.
   The verdict records both identities and the unit digest. The other agent independently reviews the fixed
   bytes and attempts counterexamples. Author assent and reviewer assent must
   both be recorded; only the latter is called independent review. There is
   one independent reviewer, not two fabricated independent verdicts.
2. The pair can exchange authorship across bounded work packages. Codex owns
   integration and ensures the exact integrated bytes are reviewed. Every
   integration edit is a new unit authored by the integrator, independently
   reviewed by the other agent if that agent authored none of the unit, or by
   a fresh agent with no conversation context. Mixed-authorship wholes require
   a fresh independent reviewer; neither contributor certifies the whole. Findings name a concrete defect,
   its consequence, and the evidence required to resolve it. Editorial fixes
   can be recorded without restarting unrelated technical decisions.
3. A review package may cover related rows. For EACH row it must separately
   state: applied contract and digest; prior obligations and dispositions;
   application-grade acceptance; D-056 gate-2/gate-3 finding; SATISFIED-GRADE
   verdict; and the exact proposed register edit. A package-wide ACCEPT cannot
   close a row lacking its own verdict. Contract application, delegated Class A
   opening, and MF-6 can be recorded in one integrated act after review rather
   than serial cycles. D-056's substantive evidence requirements stand. Here V2 "application"
   means recording exact bytes as an accepted design contract with
   application-grade acceptance at zero blockers (D-056 gate 1). `binds` stays
   NOTHING: no V1 route-A freeze, claim-register or qualification motion.
   SATISFIED cites the accepted design digest, not a V1 application claim.
4. All unresolved MUST-FIX and SHOULD-FIX findings prevent adoption. Three
   exchanges per verdict unit remain the limit (per row for a multi-row
   package, per decision for a non-row act). At three exchanges an unresolved
   unit is recorded CONTESTED and removed from that package; other units keep
   their own exchange counts and may proceed. Repackaging does not reset them.
   A fresh Claude or Codex instance, in a new Herdr pane or named third-agent
   session with no conversation context, receives the frozen turn-3 subject,
   both positions and verdicts, and cited authority. The exact adjudication
   dispatch text is retained frozen and digest-pinned alongside the ruling. Its retained digest-pinned
   ruling binds the surviving finding IDs: uphold (author repairs), dismiss
   (finding clears), or unresolved (remains CONTESTED). It cannot manufacture
   either party's assent. After UPHOLD, the adjudicator performs one bounded
   confirmation of the repair diff against the upheld finding, outside the
   three-exchange budget; failed or inconclusive confirmation returns the unit
   to CONTESTED without a fourth exchange. New defects, if discovered, are recorded separately
   and must be repaired before adoption; adjudication is not a license to
   ignore them. An unresolved ruling is parked and batched to the user under
   D-000 clause 2 while independent work proceeds. This explicitly amends
   D-000 clause 2's terminal step by adding independent adjudication first.
5. Reviewed unit files are frozen at mode 0444 and digest-pinned before
   dispatch. The verdict records HEAD at open, every unit digest, and the exact
   proposed register edit text (or explicit no-edit). Any byte change after
   dispatch creates a successor unit and invalidates reliance on the old
   verdict for new bytes. Frozen reviewed files and source digests are retained. Each adopted decision
   records its authority, author, reviewer verdict and hash, changed acceptance
   clauses, remaining qualification work and reversal procedure. Commit/push
   remains per coherent adopted decision under D-000/D-293. Source authority
   changes require explicit supersession; latest filename is not authority.
6. Every existing row remains in D-002's affected or deferral set. Adoption of this workflow
   changes no threshold, fixture obligation, product behavior or row standing;
   acts under it change standing only through their own per-row verdicts and
   MF-6 edits.
   Release qualification and V1 freeze remain separate from architecture
   completion. D-367 enables owner decisions, not evidence-free closure.

## Explicit sequencing supersessions

Under D-367 the delegated pair may amend the following adopted sequencing
clauses. Only serialization and reviewer-count practice change:

- D-056 **Eligibility (narrow)** gate 4: "A dedicated later D-000 cycle plus
  independent SATISFIED-GRADE review of *that row* accepts the split and
  records SATISFIED under this amendment." The dedicated-later-cycle portion
  is replaced by the integrated act in clause 3. The same replacement covers
  its **What is superseded** item 3 and **Decision** items 2 and 4's separate
  cycle / one-row-at-a-time sequence. Independent per-row review and MF-6
  edits survive, including their exact acceptance requirements.
- D-293 **Decision** item 5: "The D-056 Class A openings themselves are
  separate owner-controlled entries; this entry opens none of them." The
  separate-entry requirement is replaced by explicit delegated owner acts
  within the integrated recording. D-293 itself still opened none. Its
  fresh dual-review wording follows the one-independent-peer rule above.
- D-314 **Adopted text** item 2 G1-131: "Keep the agreed order: shared gate-2
  entry, fresh application-grade review of the exact final contract bytes,
  then the owner-controlled opening"; item 3 G1-133: "Use the shared gate-2
  entry, fresh application-grade review of the exact final provider-only
  contract bytes, and then the owner-controlled opening. Treat NT-6 authoring
  as a separate D1 act after that opening and before the later per-row cycle,
  not as opening content." These serial steps may be one reviewed act with
  separately stated content, after the design/fixtures have been authored.

D-056 gates 1–3, D-133's property-based eligibility, a fresh application-grade
review of exact final contract bytes cited by each opening, independent per-row
SATISFIED-GRADE review, and D-316's express lift of a named reservation all
survive. Each opening is recited as the delegated product owner's act under
D-367. No implicit lift and no missing design may enter the execution remainder.

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
count and serial cycles, specifically the quoted D-056 gate-4/Decision
sequence, D-293 item 5 and D-314 items 2–3, and D-000 clause 2's direct
terminal batching to the user without adjudication. Existing acts retain their accurately recorded review
provenance. Requiring their re-review must be stated explicitly; history is not
rewritten. No readiness count changes on adoption of this workflow.
