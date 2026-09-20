# Independent review — native trust graph 272

**Standing:** bounded native-Rust review of frozen `native-trust-graph-checkpoint-272`. Full-dependency structural walk on the same operation Budget as signed 269 policy, after 271 source-bound decode. **Not** Operation `_walk` prepared-outcome/descriptor bindings, current/historical population, non-key subjects, other-root contexts, private-policy adoption/merge, artifact/repair/S4/floors, command/role/batch/whole-image effects, native custody/fence/census/durability/writers, source selection, or M3–M6. Archived 271 (`7a5b9704…6d60`) was not edited. Installed product remains `fa72e50`.

Python 3.12.13 `-I -B`. OpenSSL 3.6.3. Rust 1.95.0 `--offline --locked`. Review-local product copy only. Frozen fixture/key/result directories were not overwritten. Keys are **TEST ONLY**.

---

## Verification

Frozen archive: **5188496 B, 513 members, SHA256 `f2010bcccf06ae80ca2c4a4423ba38dc5186c50dcd7201a8152c7be353cff5c3`**. Pin, tar, member count, and every `subject.json` hash matched before extract; extract rehashed **513/513**. Product-inputs **400/400** live-equal.

Nested parent 271 pin `60312d34…8fc1` (5247812 B / 502 / 398 files) equals the reviewed 271 freeze; live trial tar still matches; `trust-before.rs` equals that 271 `trust.rs`. Nested 265 `73c3b3f5…86df`, graph 236 r1 `f09cb777…dc62` (9716 B / 22), and reader 232 r4 `26bf1187…e2e9` match reviewed archives. Schema `1328ba16…4208`. `Cargo.lock` unchanged vs 271.

Product vs 271: **400** files, **397** unchanged, **1** changed (`trust.rs` `852fb256…9165` — private `retained_trust_graph` plus two tests), **2** added (`graph272.ndjson`, `graph272-shared.ndjson`). Inherited 271 fixtures unchanged. No public API (`lib.rs` does not name the module). No skip/waiver parameter.

---

## What 272 adds

Private `walk(&mut Budget, kind, reference, store)` is FULL dependency mode only. Exhaustive 27-arm `RecordKind` route selects collection plus full `NodeRef`/`EventRef`/`PublicationRef` shape; that admit runs **before** `Budget.load`. `physical_ref` then projects `{sha256,bytes}` for load. Extra root fields (`unknown`) fail closed shape with **zero** captures.

Per edge: `Budget.load` charges **first** (cache hit still `edge(1)` and checks cached length), then 271 `decode_at` (children) or `Record::parse` + `root_locator` (root event store/sequence, publication `previousCapsule`), **then** active `(collection, SHA)` cycle guard and completed-typed cache `(collection, SHA, expected kind)`. BlobRef stays opaque. Distinct collections stay distinct. Iterative DFS keeps one child index per frame (sorted 271 edges, no full fan-out queue). No lifetime-64 cap. Failures latch `budget.scope`; owned `Arc` visits survive store/budget drop.

Same Budget as 269 `packaged_recovery_policies::prepare`. Signed empty-global policy + this closure graph in **both** orders: 14 objects / 21548 bytes / 14 physical captures; edges policy→graph→graph **42→60→78**, graph→policy→graph **18→60→78**. Exhausting graph edges also closes the policy producer.

This is not Operation `_walk` extra prepared-outcome/descriptor bindings (next owner). CPU/RSS/native capture custody are not claimed by the conditional object/edge/byte budget.

---

## Reproduction vs inspection

| Kind | Corpus | Result |
|---|---|---|
| Exact live | `cargo test -p opensip-security` | **209/209** |
| Exact live | `cargo test --workspace` | **508** passing (506 + 2 doctests) |
| Exact live | workspace Clippy `--all-targets -D warnings` | **pass** |
| Exact live | `cargo fmt --all --check` | **pass** |
| Exact live | 9 compiled r2 controls + baseline | **10/10**; core fields/patches/source SHA-equal frozen `mutation-check-r2` |
| Exact live | Python source/fixture probes | **32/32** |
| Inspected | 30 graph cases / 11 positive | 300-deep chain (303 captures); diamonds/shared roots; exact/one-short object/edge/byte budgets; missing/tamper/cross-collection; cached wrong event store/seq after same target done; cached hash wrong type; same hash two collections (5 objects / 4 captures); extra root field; cached wrong length |
| Inspected | 2 shared-order rows | 14/78/21548 both orders; graph exhaustion latches policy |
| Inspected | mutation-check-r1 done-cache control | **escaped** (4 passed) because deepcopy aliased `afterProjection.eventHead` with `events[0].event` |
| Inspected | mutation-check-r2 | copies the second EventRef; unsafe control now caught; production unchanged |
| Inspected | 268 workspace 493+2 | predecessor only; not rerun |

**Controls (honest):**

Wrong admission (`left: true` / `right: false`): skip full root-ref shape (`reference-extra-field` admits); completed-cache before source locator (`cached-event-wrong-sequence` admits); cross-collection fallback (`original-10` admits).

First fail **other** assertions (not exploit proofs):

- `skip-root-locator`: `original-15` capture count **2 vs 1** (walk still fails later; not a returned Ok on the wrong-locator root).
- `lifetime-history-depth-64`: `original-3` 300-chain over-refused `Cycle`.
- `omit-cycle-guard`: internal `not_active` unit test `Ok` vs `Err(Cycle)` — not a content-hash fixed-point cycle.
- `only-first-child`: `original-0` edges **3 vs 10** / missing visits.
- `reset-operation-budget`: `original-0` counters **0 vs 3**; shared test **14/42 vs 14/60**.
- `omit-outer-failure-latch`: follow-up walk is not `BudgetError::Closed`.

---

## Independent probes

| Probe | Result |
|---|---|
| Public API | module/`walk`/`Error` not exported from `lib.rs` |
| Load vs locator vs cache | `load` (charge) → `decode_at`/`root_locator` → `not_active` → `done.contains` |
| Cache-hit still charges | `Budget.load` calls `edge(1)` before `raw.get`; length mismatch on cached bytes is `Digest` |
| Extra root field | closed EventRef/NodeRef shape refuses; `physical_ref` cannot bypass admit; 0 captures |
| Same bytes, two collections | independent identities; 5 objects with 4 captures after prior |
| No skip list | `walk` takes only budget, kind, reference, store |
| r1 vs r2 done-cache | r1 escaped via EventRef object alias; r2 independent copy catches wrong sequence after done |

`skip-root-locator` is classified other-first because `original-15` still errors after an extra capture. That does not prove a successful admission of a wrong-locator root that has a complete child store.

---

## Remaining (do not count closed)

Operation `_walk` prepared outcome/input/event/clock/publication/restore descriptor joins; current/historical population and non-key subjects; other-root contexts; private-policy adoption/merge; artifact/repair/S4/floors; command/role/batch/whole-image effects; native custody/fence/slots/census/durability/writers; source selection; M3–M6. Structural FULL traversal is not current authority and not permission to walk old T for a scoped operation. 272 is not installed runtime source.

---

## Verdict

- [x] Archive/pins/members verified. 400 product files: 397 unchanged vs 271. Nested 271/265/236/232 pins match reviewed archives.
- [x] **209** security tests, **508** workspace tests, Clippy, and fmt reproduced. Nine r2 controls behave as documented (three wrong admissions; six other-first). r1 done-cache escape is a fixture-alias gap, repaired in r2 without production change.
- [x] Same Budget as 269 policy (42→60→78 / 18→60→78, 14 objects / 21548 bytes / 14 captures). Locator and 271 decode run before typed/active cache; every edge charges on physical cache hit; collections stay distinct.
- [ ] **Not** Operation `_walk` extras, current authority, native custody, or product installation.
