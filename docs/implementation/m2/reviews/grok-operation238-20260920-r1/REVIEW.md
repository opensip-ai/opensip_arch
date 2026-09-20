# Independent review — shared retained trust operation budget 238 r1

Unselected composition over frozen 237 primary modules. **Not native custody, host admission,
current authority, or cumulative protocol approval.** The completed 237 review
`/tmp/opensip-implementation/reviews/grok-primary237-20260920-r1/` is untouched. No repo, product,
or candidate edit. 237 algorithms are imported, not modified.

## Verification

- Frozen `trust-operation-budget-wip-238-r1` `631d5402…5f0e` (19420 B, 34 members): pin and every
  subject member verified before extraction; extract re-verified after runs.
- Dependency 237 `dca9a702…d050` via output-local sibling
  `m2-producer-integration-reference-237/candidate` from the already-reviewed extract.
  `inputs.json` 7 primary hashes all match (record/input/event/restore/index/graph modules + 122-def
  schema). Python 3.12.13 `-I -B`.
- Tests pull **literal AST function/class bodies** from pinned predecessor fixtures
  (`test-inputs/`, hashes equal 236/234/235 sources) and supply 237 implementation modules.
- Mutation runner used a fresh work tree because frozen `operation-variants-r2/` already exists.
  Variant files rewrite `PRIMARY` to the local 237 path (harness-only); mutation before/after
  strings and baseline refusals match frozen r2. Source SHA of those copies therefore differs,
  as expected.
- Regenerated `operation-check-r2.json` **byte-identical** (43 cases). Nine variants all
  **unsafe-admit** while baseline refuses. `operation-check-r1.json` (38 cases) binds
  `operation_work-before-failstop.py` `9431ab84…0164`. Current source `d9cc5957…b8e9` matches r2.
  The five added cases are fail-stop closes after semantic/pair/shape refusals.

## Accounting semantics

One `Budget` is shared by `InputWork`, `GraphWork`, `MetadataIndex` subclasses, `Operation.walk`,
and `Operation.proof` (235 nested restore/event bridge via 237 `trust_restore_reference` +
`input_work`). Identity is `(collection, raw SHA-256)`. Limits are positive ints, lower-only:
65536 objects / 131072 edges / 256 MiB / 4 MiB per object.

Mixed index→graph→input: **9 objects, 17 edges**; opaque catalog bytes share the `objects` key
across metadata delivery and graph `BlobRef`s. Exact-fit admits; one-short object/edge/byte refuse
before extra `store.get`. Nested restore after that mix increments by the same object/edge/byte
counts as a standalone 237 `I.Work()` on the same proof. Nested `event-store-operation` still
refuses (unchanged 235 bind).

Every graph/input `load` charges an edge, including cache hits. A new `MetadataIndex` charges its
full declared-member list on first member `load` (so a second index at `edges=6` fails
`operation-edge-budget` **before** any capture callback). Re-select of an already-indexed path adds
no declared edge. New listed paths still presence-capture known hashes (second index: 4 captures,
+6 edges). Tampered delivery of a cached hash refuses `operation-reference-bytes`. Same hash in
`objects` vs `records` counts twice; records do not borrow the objects cache
(`operation-capture-cap`).

Known-size object/byte caps run **before** `store.get` (probe: 0 gets). Unknown-size first captures
receive remaining allowance capped at 4 MiB. Failures latch: later `load` / `walk` / `index` /
`select` refuse `operation-budget-closed`. `guard()` also latches helper `Refusal`s (shape, unowned
pair, event-store-operation). 237 standalone `I.Work()` remains a separate class and ledger;
callers must pass `operation.input_work`. Profile 0 / `True` / `-1` / cap+1 refuse.

Nine mutants each admit the forbidden case: metadata-edge omission, reference-edge omission, object
cap, byte cap, separate index `Budget()`, separate proof `InputWork(Budget())`, records→objects
fallback, presence bypass, latch bypass. The r1 harness wrongly used the mutant’s own counters;
that failed run is retained. r2 uses the **baseline** allowance; implementation was not changed to
pass the test.

## Remaining findings

#### F-1 (stated native remainder, demonstrated) — presence re-read of a known hash passes 4 MiB to the callback

`available()` returns `CAP` on a cache hit. A new listed path with `presence=True` therefore calls
capture with 4 MiB even when remaining operation bytes are smaller. Accounting does not double-count
(retain sees the existing key). Native allocation-before-cap is still the capture owner’s job, as
README says. Not an object/byte-ledger hole.

#### F-2 (stated) — 237 default `Work()` paths are not this budget

`trust_input_reference.Work` still constructs a private ledger. This composition is shared only when
the native actor builds one `Operation` and passes `input_work`. Old standalone entry points are
unchanged and unintegrated.

#### F-3 (stated, from 237) — FULL graph / pending events / opaque metadata

This module does not add S4.5/safe-ABORT skip lists, does not authorize pending role effects, and
does not authenticate signed metadata. Cached bytes are immutable for the `Operation` lifetime.

No unsafe counter reset, collection fallback, or fail-stop bypass was found in the unmodified
source. Parent `Index` still has its own default 65536/131072/256MiB fields; overridden
`load`/`retain` plus `charge_declared_edges` keep the **operation** cap in charge and cannot enlarge
it.

## Verdict

- [x] One `Budget` across input, graph, metadata indexes, and nested restore/event proof.
- [x] `(collection, hash)` identity, before-get caps, presence vs cache, fail-stop latch hold.
- [x] 43/9 reproduce; nested bad-event refusal preserved.
- [ ] **Not host/native install, not semantic admission, not cumulative approval.**

No harness failure.
