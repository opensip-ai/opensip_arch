# Independent bounded review — typed retained graph reader 236 r1

ROOT full-dependency walker over the source-bound 232 r4 decoder. **Not cumulative protocol
approval, not S4.5/safe-ABORT scope, not native custody, signatures, or current authority.** The
completed 235 review
`/tmp/opensip-implementation/reviews/grok-publication235-20260920-r1/` is untouched. No repo,
product, or candidate edit.

This module walks **structural** dependencies only. Hash-only fields (`previousCapsule` as a digest
on capsules, `nativeBefore`, `intentDigest`, `ClosureId`) are not generic edges. Raw `objects` stay
opaque. Expected root type is a trusted internal owner input. FULL mode has no caller skip list.

## Verification and reproduction

- Frozen `trust-graph-wip-236-r1` `f09cb777…dc62` (9716 B, 22 members): pin and every subject member
  verified from the tar before extraction; extracted copy re-verified after the runs.
- 232 r4 from the already-verified extract (`26bf1187…e2e9`); `reference_reader.py`
  `c365187a…42cd` equals `inputs.json`. 201 sibling canonical `d47f25db…b442`; schema `a3a0b4f4…8520`.
  Output-local siblings only. Python 3.12.13 `-I -B`.
- Mutation runner copied to a fresh work tree because `graph-variants-r2/` already exists in the
  frozen subject.
- Regenerated `graph-check-r3.json` **byte-identical** (35 cases). Regenerated
  `graph-variants-r2/results.json` **byte-identical** (5/5). Empty `graph-check-r1.json` is a retained
  failed run, not counted passing.
- Initial illegal merge fixtures (`parents:[lr,lr]` and single-parent merge chain) are in
  `check_graph-before-merge-fixture.py`. Current corpus uses a real `prior` list chain and a merge of
  two distinct parents sharing a dependency.

## Iterator, source binding, cache, budgets

`walk` is iterative DFS with `active` identities `(collection, sha256)` and completed typed visits
`(collection, sha256, expected)`. Child order is 232's reversed-extract order. Root collection is
derived: `PublicationDescriptorV1` → publications, `*EventV1` → events, else records.

Every **child** is `R.decode_edge(source_type, source_raw, source_pointer, target_raw)` — probe of a
history walk recorded nine instance pointers (`/admittingRoot`, `/list/body`, `/list/envelope`, six
anchor body/envelope rows). No caller edge list or schema row. Root uses `extract` plus root
EventRef/PublicationRef locators.

Repeated exact `(collection, sha)` shares retained bytes; **every** incoming edge still `decode_edge`s
before the typed-done skip. Probe: after a successful `TrustEventV1` walk, a new publication whose
EventRef has the same sha256 but **wrong sequence** refuses `event-locator-binding` on the shared
`Work`. Cached targets do not evade locator/type checks.

`Work` is shared across successive walks and never resets: objects stay, edges accumulate (10 then
20 on a second root). Caps are positive and only lowerable (`0` / `True` / cap+1 refuse
`budget-profile`). Object and byte checks precede `store.get`; one-short objects refused after 2
gets (the third physical object is not fetched). Distinct `(collection, hash)` keys count as two
objects even when raw hashes match; repeating the same key only increments edges. No
records↔objects fallback. `get((collection, sha))` is the only adapter operation.

Five mutants: objects/edges/bytes/collection-fallback are exact-oracle kills. `root-event-locator`
deletion yields the tuple `(root-event-locator, missing-object, root-event-locator)` — a **secondary
missing-object** diagnostic, not unsafe admission (children of the mis-located event then fail
collection lookup). Matches the frozen standing.

300-deep actual-hash `prior` chain is iterative (303 visits). Creation event → operation → input →
marker, publication → events, and capsule → publication closures pass; store insertion order does
not change the result. Child publication predecessor locator is 232's `publication-locator-binding`.

The cycle guard is defensive: `identity in active`. No SHA-256-self-consistent cycle was built;
negative cycle bytes would fail rehash first. Do not treat guard absence as a demonstrated kill.
227 toy-ID cycle cases are a different abstraction and were not re-run.

## Remaining findings

#### F-1 (stated / demonstrated) — `Work` caches captures; it does not re-read the store

After a walk, tampering `store[(objects, sha)]` and walking again on the **same** `Work` still
**ADMITS** (cached raw). A **fresh** `Work` refuses `reference-bytes`. README requires immutable
supplied bytes; this is not a live re-validation of a mutated adapter. Dictionary custody remains
the native owner's job.

#### F-2 (stated) — FULL mode is not S4.5 / safe-ABORT

`walk(definition, reference, store, work)` has no skip/exclusion argument. Missing evidence refuses
`missing-object`. Those operations must not use this walker until their narrow old-T producer is
wired through every current/embedded `beforeClock` path.

#### F-3 (stated) — budgets are this graph, not 230/234

Object/edge/byte counters are not the restore-proof `Work` or the 234 capture ledger. Common
operation accounting is owed, not claimed.

No omitted source-bind, typed-cache, or collection-fallback hole was found inside the claimed
FULL-structural surface. Opaque objects, hash-only non-edges, and trusted root type are explicit.

## Verdict

- [x] Every child is source-bound `decode_edge`; locators/types re-check even on completed targets.
- [x] Shared `Work` survives walks, counts physical `(collection, hash)`, every edge, retained bytes;
  checks before get; no cross-collection fallback.
- [x] 35/5 reproduce; root-event-locator mutant is a secondary diagnostic, not unsafe admission.
- [ ] **Not S4.5/ABORT, not native custody, not current authority, not cumulative approval.**

No harness failure.
