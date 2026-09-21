# Independent review — lineage reader 367

**Standing:** bounded **lifecycle read-only syntax** of frozen `lineage-reader-checkpoint-367`. `StoreLineageNodeV1` is a six-field product-canonical codec with physical-owner203 cap **4096** and path `transitions/lineage/S/G/K.node`. `inspect_supplied` walks a caller-supplied callback. This is **not** native custody, physical uniqueness, immutable publication, intent authorization, registry namespace, five-member `StoreGenerationBindingV1`, current authority, or S9 acceptance. Product remains `fa72e50`. Inventory **v54** does **not** list the three new paths; a later successor is required. Source 367 remains **outside** the 54 verdict. Native tests were **not** run (root 368 synthetic native integration; wait for clear).

Prior 54 REVIEW `02c0b801…9a76` / `review.json` `3ff38b0c…0bcc` (**NEEDS-CHANGES**), 366 `0d875631…dcf5`, 365 `0d1e8a10…9f57`, 364 REVIEW/ADDENDUM/CORRECTION-REVIEW were read and are **unchanged**.

Python 3.12.13 `-I -B` + jsonschema **4.25.1** (`source-audit364-env`). rustc/cargo **1.95.0**. Isolated `grok-out/`; freeze and extract product **not** overwritten. **This review reproduced:** schema corpus 565; `cargo test -p opensip-lifecycle` **32** (12 `lineage::`); six compiled fault controls + restored 12; rustfmt of the three changed lifecycle sources; Clippy `-p opensip-lifecycle --all-targets -D warnings`. Security/native suite **not rerun**.

---

## Verification

Archive-pin and every `subject.json` member matched **before** extract. Frozen archive: **6942100 B, 640 members, SHA256 `20ace56eee2bd74d6811bcb2b297976ba1de5f11dbda4fbb89e9c6cfeffd742a`**. Standing: “Private read-only lineage syntax and supplied chains; no native/full binding authority”. Parent 366 rehashed first: **759 / 7259480 B / `1e9f064f…1715`**. Extract rehash: 0 mismatches; **582** product files.

Vs 366:

| Class | Count |
|---|---|
| Unchanged | **578** |
| Changed | **1** (`crates/lifecycle/src/lib.rs` 441 → 715, SHA256 `ae67f08c…c2c1`) |
| Added | **3** |
| Removed | **0** |

Added: `lineage.rs` `8cf22604…1566` / 7311 B; `lineage/tests.rs` `62dd9299…a035` / 11872 B; fixture `lineage-node367.json` `aa99c66d…56f9` / 218081 B. `Cargo.toml` dependencies unchanged (`opensip-identity` + `opensip-platform` only). No security crate change.

Pinned law: `lineage-source.json` SHA256 **`919d1717b53f202b2e53a4f580b7f3df13f908b3575d4a97ad22e7bc6f185210`**. `physical-owner203.md` SHA256 `292dbab3…e5ac` (working unselected text). Using those bytes does **not** settle application46/S9 standing.

---

## Codec and supplied reader

Six required members match the closed companion schema: `schemaVersion` const 1, `storeInstanceId` 32 lowercase hex via existing `StoreComponent`, `storeGeneration` 0..=i64::MAX (not monotonic), `stateSchema` {1,2}, `predecessor` null or the same three-field triple, `selectedByIntentDigest` null or 64 lowercase hex. Cap **4096** is checked **before** parse. Canonical product bytes required; duplicates/types/non-integers refuse. Null origin fields are paired (`RootPair`); self-predecessor refuses. Relative path is `transitions/lineage/{S}/{G}/{K}.node` (G shortest decimal, K 1 or 2). Both full triples are validated.

`inspect_supplied` is iterative, component-local, and returns **no** partial success: `Limit` (caller `max_nodes`, engineering bound, checked before read), `Read`, `Missing`, `Misbound`, `Cycle`. Every returned node is compared to the requested key. Root is required (`predecessor == None` ends the walk). Unrelated stores are not scanned. Equal generations and repeated intent digests are lawful. The callback cannot prove physical uniqueness, immutable publication, original intent authorization, custody, registry namespace, full five-member binding, or authority — those remain **OPEN**.

Public reexports from `lib.rs` (`DecodedLineageNodeV1`, `inspect_supplied_lineage`, caps/errors/keys) are syntax only.

---

## Live checks (this review)

Isolated generator (jsonschema 4.25.1 Exact integer checker + canonical/null-pair/self rules) reproduced **565** cases, **110** accept / **455** refuse, fixture SHA `aa99c66d…56f9` **byte-equal** frozen. `cargo test --offline --locked -p opensip-lifecycle`: **32 passed** (0.32s), including **12** `lineage::` (corpus, domains, null-pair/self, cap/canonical, 300-node iteration, cycles/limit, missing/unreadable/misbound, component scoping, revalidation). rustfmt `--check --edition 2024` of `lib.rs` / `lineage.rs` / `tests.rs`: exit 0. Clippy `-p opensip-lifecycle --all-targets -D warnings`: exit 0.

Six compiled faults (null pair, self edge, canonical bytes, key binding, cycle, work bound) each **compiled** and failed the **intended** test; source restored; **12** lineage tests pass again. Extract `lineage.rs` SHA unchanged. Freeze `controls-r1` not overwritten.

Author `lineage-r1` **E0716** (temporary predecessor key borrowed) is retained failed history, not a pass. `initial-test-source.rs` preserved.

Native `opensip-security` tests **not run**. Author workspace Clippy not independently rerun as a workspace job.

---

## Findings

367 is a lifecycle codec + supplied-callback walker over already-pinned six-field shape and 203 path grammar. Algorithms in security/native 366 are untouched.

**Actionable 367 source defect:** none that make the six-field closed shape, 4096-before-parse, paired nulls, self-predecessor, canonical bytes, distinct walk errors, or 565/12/6-control evidence self-contradictory.

**Must not be counted closed:** physical uniqueness; immutable publication; intent authorization; custody/fence; registry namespace; five-member store binding; S9/application46 standing; native 368 integration; inventory listing of these three paths (54 excluded them; 55 is a later cumulative from selected 32).

---

## Remaining (do not count closed)

Native validation when root signals clear. Inventory successor for the three new paths. Writers, current authority, M2–M6. Selected inventory still 32.

---

## Verdicts

- [x] **367 as frozen private lineage syntax/supplied reader:** 640-member archive verified; 578/1/3 vs 366; schema pin `919d1717…`; corpus 565; lifecycle **32** + 12 lineage; 6 intended control failures + restored 12. Private/uninstalled.
- [ ] **Not** native/full binding, inventory 54/55 activation, S9 acceptance, or product installation.
