# OD-REVIEW-ORDER-1: Codex reviews ordinary production code after merge

Status: accepted owner decision; effective 2026-11-13 UTC.
Scope: when the cross-vendor (Codex) review of a product change happens. It
amends OD-PACE-1 rule 2 for one class of change. It changes no product law.

## Owner instruction

The owner asked what limits delivery speed. The lead answered that review is
the limit (about 500 commits on branches since 2026-11-11, about twenty
requests queued for one rate-limited reviewer) and listed four things that
would move it. The owner answered:

> do all you recommended to move it

The four, as the lead put them:

1. "Change when Codex reviews ordinary production code (your decision). Today
   every change needs Codex before merge. I recommend letting non-security
   production code integrate on an independent Claude review plus green lanes,
   with Codex reviewing afterwards and any finding fixed forward. Codex stays
   before merge for security-boundary code, signing, durable formats and law
   text. Nobody installs main yet, so a late rejection costs only a follow-up
   commit. This sets aside part of your recorded rule, so I won't do it
   without you."
2. "Batch the Codex queue. When Codex resets, I'll send it stacked batches in
   dependency order instead of 20 separate requests."
3. "I take the composition skeleton myself if session 16 does not commit a
   Run."
4. "Start no new side units until the queue drains."

The details below are the lead's. They are not further quotations from the owner.

## What is decided

1. **Ordinary production code integrates before its Codex review.** A change
   to production code may be integrated and pushed after one accepted
   independent Claude review and green lanes (macOS strict lane and Linux
   lane). Its Codex review still happens: the request is written before the
   integration, sent at the next opportunity, and reviewed against the
   integrated commits.
2. **What stays reviewed by Codex before merge.** Each of these keeps its
   existing rule (OD-PACE-1 rules 2 and 4, OD-REVIEW-1):
   - security-boundary code (confinement, launch, spawn, the supervisor's
     refusals, admission of provider output, anything marked a security
     change);
   - signing;
   - durable on-disk formats (schemas, stored record shapes, ledger and
     journal definitions, identifiers whose bytes are pinned);
   - final qualification;
   - law text: design records, errata and contracts in this repository.
3. **Code that rests on an unbound record is not integrated before the record
   binds.** A unit marked at risk on an erratum or a proposed record waits for
   that record's reviews, whatever its own class.
4. **When in doubt, the stricter class.** A change that touches both an
   ordinary and a kept class takes the kept class's rule. The lead states the
   class and its basis in each integration report.
5. **A late Codex finding is fixed forward.** A required finding on integrated
   code becomes the next unit on that code, ahead of new work on it. If the
   finding shows the change should not be on main, the lead reverts it and
   reports that. The live map lists every integrated change whose Codex review
   is still owed, so none is forgotten.
6. **Batched requests.** Codex may be given several stacked units in one
   request, in dependency order, with one verdict per unit.

## What is not changed

- Nobody accepts their own work; the Claude reviewer is independent of the
  author and of the lead's rulings on the unit.
- The full lanes are green before anything merges.
- Two reviewers for security-boundary code, signing, durable formats and
  qualification.
- OD-TS1-RUN-1 decision 3 (test-only batches) stands; this decision does not
  narrow it.
- The standing permission to push, with each push reported.
- The owner's review of everything implemented after M3, before any M4+ work.

## When this ends

It is revisited when main is first given to anyone to install, or at the
owner's word. From then a late rejection no longer costs only a follow-up
commit.
