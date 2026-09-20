# Independent review — native restore proof and event composition 278

**Standing:** bounded native-Rust review of frozen `native-restore-bindings-checkpoint-278`. Complete original restore-proof path composed with optional 273 prepared outcomes, 276 descriptor/operation joins, and 274 literal event bindings on the **same** guarded operation Budget. **Not** live complete-bucket census, fork detection, smallest-digest witness choice, native custody/durability, authenticated accepted state, current population, transition/effect proof, clock/publication/role-effect authorization, historical/current population, non-key subjects, other-root contexts, private-policy merge, artifact/repair/S4/floors, command/role/batch/whole-image effects, fence/slots/writers, source selection, or M3–M6. Archived 277 (`bcdad807…d974`) was not edited. Installed product remains `fa72e50`.

Python 3.12.13 `-I -B`. OpenSSL 3.6.3. Rust 1.95.0 `--offline --locked`. Review-local product copy only. Frozen fixture/key/result directories were not overwritten. Keys are **TEST ONLY**.

---

## Verification

Frozen archive: **5940900 B, 729 members, SHA256 `1be3f3641e6b22a56d7abdab7a576178439f1a9cd809794ec3fe71c54bde548c`**. Pin, tar, member count, and every `subject.json` hash matched **before** extract; extract rehashed **729/729**. Product-inputs **412/412** live-equal.

Nested parent 277 pin `b0be547b…b921` (5502580 B / 685 / 411 files) equals the reviewed 277 freeze; live trial tar still matches; `trust-before.rs` equals that 277 `trust.rs`. Nested 265 `73c3b3f5…86df`. Nested 230 r3 helper `99288ae0…3c00`. Nested 235 r1 `112dc6a0…5468` (25584 B / 26). Schema `1328ba16…4208`. `Cargo.lock` unchanged vs 277. Inherited 277 fixtures and `trust_record_shapes.rs` byte-identical. `lib.rs` unchanged.

Product vs 277: **412** files, **410** unchanged, **1** changed (`trust.rs` `51cd6872…0e3f` — private restore composition plus 274 `bind_events` split), **1** added (`restore278.ndjson`). No public API. No full workspace rerun (277 515+2 predecessor only).

---

## What 278 adds

Still private: neither `restore_proof` nor `bind_events` is in `lib.rs`. Closed `Input` now also routes `Proof` → `RestoreProofV1`.

**Restore proof** (`restore_proof`): iterative stack, per-path SHA cycle (`enter_proof_path`). Full proof shape; `end > n` and chain length `end-n`; actual observed capsule revision/store. Every link unique, adjacent, exact store/revision+1/previous, bound operation. Ordinary links require DIRECT `nativeBefore`. A `restore-recovery` link schedules **its own** original complete proof with exact store/parent/`nativeBefore` expectations; it cannot stand in for the terminal. Reconstructed capsules must hash to the claimed proven image, which is also actually loaded. Terminal witness is outside the chain, adjacent, exact `N+1`/store/previous, DIRECT, and never a restore-recovery operation. Every link and terminal runs 274 literal event replay in original order, including nested proofs. **No** invented 64-depth cutoff.

**Publication path:** `PublicationRef` shape precedes physical Publications capture; full descriptor then optional 273 `bind_descriptor_raw` **exactly once** (`commandOutcome` present). Then 276 `descriptor` join. Restore calls private `publication_events::bind_events` (literal only). Existing 274 `bind` still retains/charges the optional outcome then delegates to `bind_events`, so inherited 274 tests stay byte-identical and restore does not duplicate descriptor/outcome accounting.

**Recovery-event wrapper** (`restore_event`): original 230 shell/event/action/ref/`recovery` variant, then the complete composed proof, then exact proof store and observed/native versus proven/logical before. Stronger than the old 230 structural-only proof call. Accepted role events remain explicit pending authenticated effects (`structural-bindings-only`). `RestoreBound` owns proof, captured inputs/order, event results, and actual prepared outcome/operation/descriptor after store/Budget drop.

Initial compile used nonexistent `Definition::PubRef` (`trust-before-publication-definition-fix.rs`); current code uses generated `PublicationRef`. Descriptor's fixed `link-operation-store` diagnostic is also used at a terminal; tests accept the old `witness-operation-store` label as equivalent without changing refusal behavior.

---

## Reproduction vs inspection

| Kind | Corpus | Result |
|---|---|---|
| Exact live | `cargo test -p opensip-security` | **220/220** |
| Exact live | workspace Clippy `--all-targets -D warnings` | **pass** |
| Exact live | `cargo fmt --all --check` | **pass** |
| Exact live | 33 compiled r2 controls + baseline | **34/34**; core fields/patches/source SHA-equal frozen `mutation-check-r2` |
| Exact live | Python source/fixture probes | **45/45** |
| Inspected | 118 restore rows / 19 positive | 5 `bridge235-*`; 42 `legacy230-reevaluated-*` (index 40 excluded); 300-link row **3854965 B** valid; nested/terminal guards; `accepted-role-effect-stays-pending` |
| Inspected | original 230 helper 195 checks | r1 report `original230Checks` length **195**. Not rerun here. |
| Inspected | 43 legacy proof calls / 1 symbolic excluded | `excluded.json` index **40**, dict-valued store (not bytes). Native labels skip `legacy230-reevaluated-40`. All 42 remaining legacy rows **valid=false** under the stronger bridge. |
| Inspected | 272/277 workspace | predecessor only; not rerun |

**Controls (honest):**

Wrong admission (`left: true` / `right: false`): omit witness-is-recovery-operation, witness-not-direct, operation-action, operation-ref, event-store, proof-ref, proof-store, event-native-before, event-logical-before.

First fail **other** assertions (not exploit proofs):

- `omit-proof-cycle`: path-guard unit panic (re-entry of a recorded identity on a **separate** path is admitted; not a content-hash cycle).
- `omit-proof-chain-length` / `observed-image` / `adjacency` / `descriptor-join` / `link-native-before` / `proven-image` / `witness-adjacency` / `nested-proof-parent`: extra captures.
- `omit-nested-proof-store`: later reason `nested-native-before` on `nested-exact-store-guard`.
- `omit-nested-native-before`: later reason `proof-adjacency` on `nested-exact-native-before-guard`.
- `omit-proof-repeated-descriptor` / `omit-witness-in-chain` / `omit-witness-descriptor-join`: later reasons.
- `omit-restore-variant`: panic missing field.
- `omit-prepared-outcome-binding`: outcome count **0 vs 2**.
- `omit-nested-proof`: later `link-native-before` on `bridge235-3`.
- `reset-operation-budget`: `bridge235-0` counters **(0,0,0) vs (8,9,9273)**.
- `proof-chain-lifetime-64`: over-refusal of valid `full-300-links`.
- `duplicate-prepared-outcome-charges`: extra edges **(9,19,10373) vs (9,13,10373)** when restore calls full `bind` instead of `bind_events`.
- `omit-owned-inputs` / `omit-link-event-bindings` / `omit-terminal-event-bindings`: lost facts.
- `omit-failure-latch`: follow-up not `BudgetError::Closed`.

Frozen `mutation-check-r1`/`r2` were not overwritten. r2 baseline `sourceSha256` is current `trust.rs` `51cd6872…0e3f`.

---

## Focused findings

### Same-Budget original proof + 265 bridge

Iterative per-path cycle; PublicationRef → Publications capture → full D → optional 273 once → 276 descriptor → 274 `bind_events` per link and terminal. Nested restore-recovery proofs are scheduled on the same Budget with cloned path sets. Recovery-event wrapper runs the complete composed proof, not the old structural-only 230 helper.

### Symbolic Unverified call

43 legacy proof helper calls; **1** excluded at index **40** (`reference-fixtures-r1/excluded.json`) because store values are dicts, not bytes. Native corpus has 42 `legacy230-reevaluated-*` rows and **none** are positive. Stronger current `Operation.proof` owner re-evaluates them; they are not assumed to hold because the weaker helper passed.

### r1 nested-guard escape

r1 `omit-nested-proof-store`, `omit-nested-native-before`, and `omit-witness-is-recovery-operation` **escaped** (`expectedOutcome` false, exit 0). r2 added `nested-exact-store-guard`, `nested-exact-native-before-guard`, and `terminal-must-not-be-restore-operation`. Production functions unchanged vs those fixture-only repairs. Live r2: witness-is-recovery is a **wrong admission**; the two nested-store/nativeBefore omits still first-fail as later reasons, but they now fail the tests.

---

## Independent probes

| Probe | Result |
|---|---|
| Public API | restore helpers not in `lib.rs` |
| PubRef compile error | beforeimage `Definition::PubRef`; current `PublicationRef` |
| 273 once | `commandOutcome` → `bind_descriptor_raw` in `proof_publication` only |
| Restore uses `bind_events` | two calls; 274 `bind` still charges outcome then delegates |
| No lifetime 64 | production has none; mutant over-refuses 300-link row |
| 300-link fixture | valid, 3854965 B < 4MiB product parser |
| Path-guard unit | re-entry same identity on a new set admits; not a hash cycle |
| Pending roles | `accepted-role-effect-stays-pending` present |
| Witness label | tests accept `link-operation-store` ≡ `witness-operation-store` |
| r1 vs r2 | three nested/terminal guards escaped r1; r2 34/34, 9 wrong / 24 other-first |

---

## Remaining (do not count closed)

Capsule/descriptor phase/role consistency; clock and accepted role effects/base selection; current/historical populations/nonkeys/other roots/private-policy merge/artifacts/repair/S4/floors/whole-state effects; native custody/fence/slots/census/durability/writers; runtime/source selection; M3–M6. Structural composition is not native census, fork detection, smallest witness, durability, or current authority. These are private review candidates, not shipped behavior.

---

## Verdict

- [x] Archive/pins/members verified. 412 product files: 410 unchanged vs 277. Nested 277/265/230/235 pins match live trial archives.
- [x] **220** security tests, Clippy, and fmt reproduced. Thirty-three compiled r2 controls behave as documented (nine wrong admissions; twenty-four other-first). No workspace rerun.
- [x] Same-Budget iterative proof; PublicationRef then 273 once then 276 then 274 `bind_events`; one Unverified dict-store call excluded; r1 nested/terminal guards repaired by isolated fixtures.
- [ ] **Not** native census, fork/smallest-witness, durability, authentication, current authority, or product installation.
