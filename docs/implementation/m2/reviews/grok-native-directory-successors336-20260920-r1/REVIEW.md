# Independent review — native captured successor structural relations 336

**Standing:** bounded native-**security** review of frozen `native-directory-successors-checkpoint-336`. Private `inspect` joins **caller-materialized** BEFORE (full 127 `TrustCapsuleV1` even when the bucket is empty) to 335 captured canonical files via constructed `PublicationRef` and **329** `bind` on the **same** `Budget`. It is **not** a complete following-bucket census, durable publication proof, 215 action/T/auth, current authority, or write permission. Installed product remains `fa72e50`. 335 REVIEW was read and is **unchanged**.

Python 3.12.13 `-I -B` used only for pin/extract. Rust 1.95.0 `--offline --locked`. Review-local copies. Frozen fixture/mutant directories were not overwritten. r1=287 then exact counter assertion; r2/Clippy-r1 **test-only** `count` shadow compile-fail (`as_count` fix) — **not** a mutation kill; **final is security-r3 / 287 / mutation-r1**. No production behavior correction. No new `unsafe`. No public API.

---

## Verification

Pins, tar bytes, member counts, and every `subject.json` hash matched **before** extract.

Frozen archive: **6825256 B, 545 members, SHA256 `750951cc7b786e04c88f1929cb0c92c37e5a2a8fb1e4ee4356b310b93d51d1a0`**, `allMembersRehashed: true`, **486** product pins. Extract rehashed **545/545**. Parent 335 live tar SHA `1a0574ce…bfda` (6834912 / 556 / 485). 335 REVIEW `33530ca2…b20d` and 329 REVIEW `ddbcb191…1a70` unchanged.

Product vs 335: **484** unchanged, **1** changed (`trust.rs` include), **1** added (`trust/directory_successors.rs` SHA256 `3665640c…14cf` 13783 B). 335 capture remains `592b45c1…8666`. 329 `successor_record_bindings.rs` remains `c29e126f…1d2f`. `successor-link329.ndjson` remains `5da8e3b5…768c`. 330–334 helpers unchanged. libc `=0.2.189`.

---

## Composition (source)

One `budget.scope`:

1. Canonicalize BEFORE; `shapes::admit(Definition::TrustCapsuleV1, …)` **before** I/O, including empty buckets.
2. Relative component must equal lowercase SHA of those bytes (`BucketName` otherwise). This is **not** selected-collection / ancestor / current-BEFORE qualification.
3. 335 `capture` of **all** canonical names (same Budget).
4. For **every** record: `PublicationRef { previousCapsule: before-hash, sha256: record digest, bytes: raw.len() }`; 329 `bind(b, before, &reference, store)`; `link.raw() == record.raw()`.
5. Return owns BEFORE clone, `Captured` (Files/raw/observations), and all links. Later malformed candidate cannot return a prefix. Empty `links` is **not** authorized absence.

Store callback still owns physical collection/path custody. Dependent 329 reads may outlive 335 samples. Maximum shared profile (65536/131072/268435456) wraps native cases; original 329 field budgets stay in the unchanged oracle.

**329 scope is preserved, not expanded:** outer full 279 known-before projection/empty-event guards, 298 calendar, 265 operation, 241 optional outcome, 235 known-before events, mandatory 278 structural restore/DIRECT terminal/native-before join. Inherited 278 is **not** full historical 279/calendar/215/T/auth on nested capsules. Missing old-T in structural positives is **not** a generic time-proof exception.

---

## Tests vs 148-oracle

**61** first-round 329 positives are written as native files under the hashed-BEFORE bucket and compared (reference, capsule, before, raw, inode). SAMEBudget vs oracle counters: **+1** directory object, **+5** native visit/file edges, **+67** dot+canonical-name bytes; descriptor/evidence bytes once. **Not** all 148 negatives via native I/O. Extra native cases: empty still shapes BEFORE (counters `(1,3,3)`); wrong component / `Null` BEFORE fail **before** I/O (`(0,0,0)`); hash-correct malformed/misbound D → `Relation`; missing deps; late bad candidate after a good one (sorted after) → `Relation`, latch.

---

## Live cargo

**Executed** review-local product, `cargo clean -p opensip-security` then:

| Kind | Result |
|---|---|
| `cargo test --offline --locked -p opensip-security` | **287 passed / 0 failed / 2 ignored**; `Compiling opensip-security`; 12.75s; 4 new `directory_successors_*` tests ok |
| Workspace Clippy `--all-targets -D warnings` | exit 0 |
| `cargo fmt --all --check` | exit 0 |
| `rustfmt --check` of **22** included modules | exit 0 |

---

## Mutants

Eight compiled controls plus baseline replayed into `grok-out/io/mutation-check-live` (frozen r1 not overwritten). Live `report.json` SHA256 **`caf32e03…db7b`**, **byte-identical** to frozen r1. All **9** compiled.

| Control | First failure |
|---|---|
| `skip-empty-before-shape` | `Null` BEFORE accepted |
| `skip-bucket-component` | `"wrong"` component accepted |
| `wrong-reference-predecessor` | `empty-link-0` `reference predecessor` |
| `wrong-reference-length` | `Budget(Digest)` |
| `wrong-reference-digest` | `Budget(Capture)` |
| `only-first-relation` | late-bad still `Ok` |
| `fresh-relation-budget` | counters `(2,5,4545)` vs `(3,7,4966)` |
| `discard-relations` | links len 0 vs 1 |
| baseline | 287 passed / 2 ignored |

---

## Findings

336 is a **structural** join of 335 native files to 329 known-before relations under one Budget, with BEFORE shape and relative-bucket binding even when empty. It does not prove the BEFORE is current, the bucket is a complete census, or nested 278 is full historical replay.

**Actionable defects in this freeze:** none that make `inspect` self-contradictory with those bounds on the macOS 287 tests, 61 native-positive 329 cases, and 8 controls.

**Must not be counted closed:** complete following-bucket census; durable/current authority; 330 libc EOF holes; 332 ABA/exclusion; 333 historical samples; 334 root/parent capture accounting; original T/TCB; writers; M2–M6.

---

## Remaining (do not count closed)

Selected FS/libc/custody/fence; independently qualified root/parent capture; complete following-bucket proof; current producers; original T/TCB; source-selection; M2–M6.

---

## Verdicts

- [x] **336 as frozen private structural successor composition:** archive verified; 335/329 preserved; 127 BEFORE even empty; relative SHA component; 335 all-canonical capture; 329 every candidate on SAME Budget; 61 native positives with +1/+5/+67; empty ≠ absence; no partial success; live 287/2 ignored; Clippy/fmt22; 8 compiled controls + baseline frozen-r1-equal.
- [ ] **Not** complete census, durable/current authority, nested full-historical 279, or product installation.
