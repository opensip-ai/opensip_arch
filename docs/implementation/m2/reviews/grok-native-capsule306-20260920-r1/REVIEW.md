# Independent review — captured retained capsule image 306

**Standing:** bounded native-Rust review of frozen `native-captured-capsule-checkpoint-306`. Private `capture` admits a retained capsule **IMAGE** on one existing operation Budget, then reuses 279 consistency and 298 phase/calendar. This is **not** live `state.v1`, current-head/history proof, custody, qualified publication-bucket resolution, or OS policy. Installed product remains `fa72e50`. Keys are **TEST ONLY**. Prior 298–305 reports were not edited (305 fully read and left archived).

Python 3.12.13 `-I -B`. OpenSSL 3.6.3. Rust 1.95.0 `--offline --locked`. Review-local copies only. Frozen fixture/key/result directories were not overwritten. No workspace rerun (284's 529 is predecessor). No 306 host run.

---

## Verification

Pins, tar bytes, member counts, and every `subject.json` hash matched **before** extract.

Frozen archive: **9056852 B, 930 members, SHA256 `f28502851a50144e2f9fe2b67f1a0237125e27e851e9ec24025a39464b96ad26`**. Standing: private unselected306 raw retained capsule image; no current authority, history, custody or publication qualification. Extract rehashed **930/930**. Product-inputs **459/459**. Nested 305 pin `87d4cd14…933d` (live tar match). Nested 222 r6 `5b6df2a5…1d5c`, 227 r9 `818604dd…6e44`. `shape_join_model227.py` SHA256 `781061b6…cdf2` matches the nested 227 copy. Included `kernel201.py` `df45c9c5…2299`. `lib.rs`, `clock_observation.rs`, and `trust_time.rs` are byte-identical to 305. `trust-before.rs` equals 305 `trust.rs` (`8d566f6c…098f`). Product vs 305: **459** files, **456** unchanged. Changed: `trust.rs` `a7d96739…11a5` (private `include!("trust/captured_capsule_clock.rs")`). Added: `trust/captured_capsule_clock.rs` `c88b1511…826f`, `captured-capsule306.ndjson` (15878294 B, SHA256 `e8aefc23…b202`). `capture` / `CapturedClock` are **not** in `lib.rs`. No operational caller.

Production text before `#[cfg(test)]` is **byte-identical** to `before-test-api-fix/captured_capsule_clock.rs`. Inherited `//!` include comments (`security-inherited-r1`, E0753 × 4) were replaced with ordinary `//`. Test-only `JsonInteger`/`Phase::Pending` mistakes (`security-integrated-r2`) were corrected to `n.get()` and `Phase::Evaluated`. Those test fixes did not change the production prefix.

---

## What the composition does

`capture(budget, reference, before_ref, store)`:

1. **Before I/O:** full `NodeRef` shape on the root and, if present, the optional predecessor (`canonical_bytes` + `shapes::admit(NodeRef)`).
2. **Same Budget** `load(Records, reference, store)`: closed `{sha256,bytes}`, length 1..=4 MiB, length checked **before** the callback, SHA-256 and length of returned bytes, cache hit still charges an edge and does **not** re-invoke the store.
3. `Record::parse(TrustCapsuleV1, raw, 131072)`: existing 271/125 product-canonical admit, typed source edges, owned exact raw. No recanonicalization of unadmitted bytes.
4. Descriptor identity is taken from the capsule's own `publication` `{sha256,bytes}` (not a caller descriptor). `load(Publications, physical, store)`, then `decode_at("/publication", raw)`: unique source pointer, SHA/length, `previousCapsule` locator, `PublicationDescriptorV1`.
5. If `before_ref` is present: SHA of that NodeRef must equal `capsule.previous`; then same-Budget `load(Records)` and full `TrustCapsuleV1` parse. **No** `before_ref` means none was captured, not proven absence of a prior state.
6. Existing `capsule_clock` (279 `capsule_consistency` then 298 phase/calendar) on the captured values. Nested `Budget::scope` latches with the outer capture scope.
7. Result retains the exact root NodeRef, owned capsule/descriptor Records, optional `(before NodeRef, Record)`, and `CapsuleClock`. Tests inspect those after dropping input JSON, callback store, and Budget.

The store callback is `(Collection, digest, cap)`. That is **not** the 222 r6 `publications/by-predecessor/H/D` filesystem locator or a live bucket census. Old T/root/event targets are not loaded.

Reference fixtures: exact 227 r9 joins, 125 shapes, 265 calendar, primary operation-budget model. **763** rows = **741** inherited 298 + **22** raw/ref/missing/predecessor/budget cases; **150** first-round positives / **150** repeat positives. Baseline first inherited row: **2 objects / 2 edges / 3234 B** then repeat **2 / 4 / 3234** with **2** captures. **613** rows latch `failed`. 306's parent SHA-join is **stricter** than 298's free-standing before document: some inherited 298 befores are not `capsule.previous` and refuse here before the third load.

**Executed:** `cargo clean -p opensip-security` then **251 passed / 0 failed / 1 ignored** with `Compiling opensip-security` (305's host pilot still ignored; no 306 host run). Workspace Clippy `-D warnings`, cargo fmt, rustfmt of **ten** include files (nine prior plus `captured_capsule_clock.rs`). 10/10 r1 compiled controls core-equal frozen `mutation-check-r1` (`report.json` SHA256 `b6e59b65…bd2f`). Frozen mutant dir not overwritten.

**10 compiled controls — classified by first frozen failure, not the `left: true` heuristic:**

Faulty **acceptance** (baseline refuses, mutant admits): `canonicalize-unadmitted-capsule` (`raw-capsule-whitespace` becomes `ok`).

Wrong **refusal** of work the baseline accepts: `wrong-capsule-collection` / `wrong-descriptor-collection` (`Budget(Capture)`); `wrong-source-edge` (`Record(SourcePointer)` on `/clock/timeEvidence`); `drop-before-image` (279 `empty-event publication needs exact before image`).

**Counters / latch / identity** (ok bit may still match): `omit-root-full-reference` (`bytes/0` charges 1 edge; baseline 0); `omit-before-full-reference` (`before-reference-extra` extra edge); `omit-before-parent-join` (loads a non-parent before: 3/3/12759 vs 2/2/8678); `binding-failure-not-latched` (repeat round charges edges after a failure; not `Closed`); `substitute-descriptor-reference-for-capsule` (retained `reference()` is the descriptor digest, not the capsule NodeRef).

---

## Findings

### 1. Source-derived edge, hash/len, canonical — hold

Descriptor bytes are bound by the capsule `/publication` edge. A caller cannot pass a substitute descriptor into `capture`. `Record::parse` admits the exact captured bytes; the whitespace/float/duplicate-key/invalid-utf8 rows refuse unless the recanonicalizing mutant is applied. `load` rehashes and checks declared length.

### 2. Optional parent — SHA join is real; absence is not a proof

When `before_ref` is supplied it must be this image's predecessor, including nonempty publications. Skipping the join is caught on Budget (third object) before any claim of 279 success. Omitting the captured before on a case that 279 requires is a Clock Binding refusal. `before_ref = None` does not prove `previous` is null.

### 3. Aggregate Budget / cache / fail-stop — hold

One Budget for capsule, descriptor, and optional before. Cache hits increment edges only. Outer `scope` latches; bypassing it is caught on round-1 counters. The in-memory callback is a **conditional store**, not qualified host I/O: missing keys are `Capture`, digest mismatch `Digest`. Physical by-prev publication layout remains unimplemented.

### 4. Ownership after drop — hold

Accepted rows keep exact raw Records and refs after the fixture JSON/store/Budget are dropped. Substituting the descriptor digest into `CapturedClock.reference` is caught as an identity fact, not an admission boolean.

**Actionable defects in this freeze:** none that make the private image boundary self-contradictory.

---

## Combined reproduction table

| Kind | Result |
|---|---|
| 306 pins before extract | match |
| Nested 305 / 222 r6 / 227 r9 | match |
| `lib.rs` / `clock_observation.rs` / `trust_time.rs` vs 305 | byte-identical |
| Production prefix vs test-API beforeimage | byte-identical |
| Fixtures | 763 rows; 150 / 150; 2/2/3234 → 2/4/3234 |
| Live `cargo test -p opensip-security` | **251 passed / 1 ignored** after force rebuild |
| Clippy / fmt / rustfmt 10 includes | pass |
| 306 r1 mutants | 10/10 frozen-equal; 1 faulty-acceptance |
| 306 host / workspace | **not run** |
| Current head / OS / product | **not decided by this archive** |

---

## Remaining (do not count closed)

This image is not live `state.v1` admission. Current-head/history/T provenance, OS-sample-to-S4 ownership (305's 1 s still unqualified), storage-owned publication gate and 222 durability, post-S4 guards/effects, custody/fences/census/writers, qualified by-predecessor publication locators, source selection, and M3–M6 remain open. No operational consumer calls `capture`.

---

## Verdicts

- [x] **306 as private image boundary:** archive verified; NodeRef-before-IO; same-Budget SHA/len loads; source-derived `/publication` edge; optional parent SHA-join; 279/298 after capture; owned raw/refs after drop; 10/10 mutants with classified first failures; 251/1 ignored, Clippy, fmt, 10-file rustfmt.
- [ ] **Not** live-state admission, current authority, qualified filesystem publication, OS policy selection, completeness, grant, or product installation.
