# Steering 03 — Compatibility and parity

**Status:** OPEN. This document holds the questions that exist *only* because a
product already ships. None of it is architecture.

---

## Feature coverage

A migration needs an inventory: every capability the product exposes today, and
what happens to it. That inventory is a **steering artifact**, not a design one —
its purpose is to prevent silent loss, not to define the target.

Two rules keep it from becoming a parity trap:

1. **"It exists today" is input, not a requirement.** Every row carries an explicit
   disposition: *retain / merge / compatibility-only / defer / experimental /
   **remove***. Without a real remove option, parity pressure quietly recreates
   the current shape inside the new one — which is exactly how a redesign becomes
   a reorganisation.
2. **Score by capability, not by row.** A raw "percentage covered" is gameable:
   splitting one low-risk command into ten rows moves the number more than
   sealing config or failure integrity. Gate on the P0 set being complete, not on
   a percentage.

Useful columns: stable capability ID, disposition, priority, affected journeys
(agent loop / CI / human review / authoring / operator), the decision it traces
to, how it will be verified, and **reachability** (incremental vs discontinuity).

---

## Naming and aliases

The target has **one analysis stage over profiles**
(`../architecture/05-rules-and-extensions.md`); the shipping product presents
several peer capabilities. That gap is a naming and compatibility problem, not a
design one.

- Existing capability names can survive as **profile identifiers and UX presets**
  for as long as the product wants them.
- Aliases resolve through the **same dispatch path** and never get distinct
  config, output, or persistence behaviour. An alias that behaves differently is
  a second implementation wearing a nickname.
- Whether aliases are permanent or windowed is a **product** decision. Either is
  compatible with the target; silently keeping two behaviours is not.

## Identity migration

Where the shipping product has two overlapping run-like identities, the target
has one. The migration is:

1. Allocate the target identity as the parent.
2. Dual-read legacy records so nothing existing becomes unreadable.
3. Always return the resolved identity, never an unresolved alias.
4. Retire the legacy reader only once nothing depends on it.

No destructive migration until the identity model is settled and dual-read has
run long enough to prove coverage.

## Baselines

Config, custom rules, waivers, the lockfile, and baselines all live in **user
repositories**. Baselines are the one whose content is **producer-derived** rather
than user-authored, so a producer change can invalidate them with no user edit —
which is why they are the migration that cannot be handled by shipping a new
version.

- A baseline declares the recipe version it was captured under.
- Compatibility is negotiated, with legacy matching or an explicit previewable
  upgrade.
- An unsupported recipe yields *indeterminate with repair instructions* —
  **never** a mass set of net-new findings.
- Support windows are published and bounded, not discovered.

This is the same requirement the target states in
`../architecture/06-evidence-and-persistence.md`; it appears here because the
*transition* is a migration event with real user impact.

## Legacy extension bridge

If existing whole-unit extensions must keep working, they run **out of process
behind a quarantined bridge** that translates one completion into host-owned
records. Conditions:

- No new capability may depend on the bridge.
- It has an evidence-driven deprecation decision, not an indefinite life.
- It is never the model for new contributions.

---

## Deletion discipline

**The single most important rule in this document:**

> **Package and command deletion must never lead the replacement capability.**

Every slice records parity criteria, rollback, data migration, and the exact
legacy surface it makes removable. Removal happens after the replacement is
proven, not before — and "proven" means fixture parity, not code review.

## What must not be inherited

Recorded because these are the specific ways a migration corrupts a design:

| Inherited thing | Why it must not cross into `architecture/` |
|-----------------|--------------------------------------------|
| Current capability boundaries | They are packaging history, not domain structure |
| Current rule corpus statistics | They measure yesterday's constraints |
| Current package layout | Distribution shape, not architecture |
| "That would be a big change" | Cost is a sequencing input, never a design argument |
