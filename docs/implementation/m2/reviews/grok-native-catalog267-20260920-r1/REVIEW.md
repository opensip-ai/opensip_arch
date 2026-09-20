# Independent review — native recovery catalog 267

**Standing:** bounded native-Rust review of frozen `native-catalog-checkpoint-267`. Exact completed SemVer/constraints plus the signed-catalog **structural prefix** of the 254/265 semantic owner, after 266 union. **Not** full component admission, publisher↔authenticated-namespace↔catalog identity/digest/constraint joins, the complete existing manifest checker (next 268), policy/repair/artifact semantics, current population, other-root context, held custody/ancestry/floors/S4, batch/effects, native custody/fence/slot/census/durability/writers, source selection, or M3–M6. Archived 266 (`3e61d7be…207d`), 264/265, and the length investigation were not edited. Installed product remains `fa72e50`.

Python 3.12.13 `-I -B`. OpenSSL 3.6.3. Rust 1.95.0 `--offline --locked`. Review-local product copy only. Frozen fixture/key/result directories were not overwritten. Keys are **TEST ONLY**.

---

## Verification

Frozen archive: **4652440 B, 536 members, SHA256 `dee1d3e85cd7d1f768c140b29b0f99dc40e872a7f46453269360d202428994e6`**. Pin, tar, member count, and every `subject.json` hash matched before extract; extract rehashed 536/536. Product-inputs 377/377 live-equal.

Nested parent 266 pin `a4d4a473…ca86` (4535428 B / 519 / 373 files) equals the reviewed 266 freeze; `trust-before.rs` equals that 266 `trust.rs` (`9847b43a…9be3`). Nested 265 `73c3b3f5…86df`, 254 r1 `a22c65bd…5a01`, 253 `164dd2fa…f8b7`, 252 r2 `3816972f…ccff`, 250 r2 `dbf1aa27…cf85` match reviewed archives. 250 helper `44a38c7d…cea2b` equals the reviewed extract. Extra original completion corpus `compatibility-design-cases.v2.json` is separately pinned (`205a7b0b…a04d`, 69822 B) and byte-equal to `docs/coop/completion/` (omitted from the scoped 265 snapshot).

Product vs 266: **377** files, **371** unchanged, **2** changed (`trust.rs` `069f67d5…ad4b`, `lib.rs` `22c8ca47…e746`), **4** added (`metadata_versions.rs` `a7377e99…96fe` plus `catalog267-shape.ndjson`, `catalog267-signed.ndjson`, `metadata-versions267.ndjson`). Inherited 266 fixtures unchanged.

---

## What 267 adds

Private `metadata_versions` (crate-local, `allow(dead_code)` in `lib.rs`, not `pub`): completed SemVer parse/compare and exact/interval constraints. Decimal components compare by **length then digits**, no machine integer. Precedence ignores build; exact-string satisfaction uses `version.raw == exact.raw` (build included). Prerelease ranges require a bound with prerelease and the same core. Empty/reversed intervals are nonempty=false. Catalog `hostCoreConstraint` remains **interval-object-only**; exact-string constraints exist for a later manifest owner.

Private `recovery_catalog::prepare` is `budget.scope` and calls 266 `incoming_recovery_quorums::prepare` **once** on that budget, then requires exactly one catalog pair, parses its body, and `validate`s it. Evidence owns the 266 signed result, the catalog value, and a read-only full-tuple release index `(stableId, publisher, sourceClass, version) → row`. First-pass vs final 266 proofs stay on `signed()`.

`validate` closes catalog/releases/artifacts; exact `catalogSchema == 1` and positive counters; real issued/expires calendar with `issued < expires`; unique reserved commands (max 256); unique release tuples (max 100000); strict completed versions and nonempty interval objects. `rootVersionRequired` / `revocationVersionRequired` are positive integers only — **not** forced equal to the candidate context. Unpresented releases (`releases: []`) are allowed. Duplicate artifact rows are legal. Catalog publisher/reserved `$`-style tokens permit **one** trailing LF, distinct from strict envelope namespaces (no LF strip). Artifact `archiveProfileId` length is Unicode `chars()`, not bytes.

Catalog prefix oracle is exact unedited AST of 265 `trust_metadata_reference._prepare` statements 6–8 (`Try` schema/calendar, `releases = {}`, `For` uniqueness+SemVer) — not the later component-join loop. A signed invalid component (`component-semantics-pending`) is intentionally accepted here.

---

## Reproduction vs inspection

| Kind | Corpus | Result |
|---|---|---|
| Exact live | `cargo test -p opensip-security` | **193/193** (266’s 190 plus catalog prefix, signed catalog, versions) |
| Exact live | workspace Clippy `--all-targets -D warnings` | **pass** |
| Exact live | `cargo fmt --all --check` | **pass** |
| Exact live | 10 compiled controls + baseline | **11/11**, SHA-equal frozen `mutation-check-r1` |
| Inspected | 340 catalog-prefix cases | native `validate` vs 265 AST 6–8 |
| Inspected | 32 signed / 14 positive | baseline **14/40/21470**; empty catalog, duplicate artifacts, trailing LF, 64-char Unicode profile, large version, future required root/list, pending component |
| Inspected | 4189 version/constraint cases | original completion corpus + deterministic random including 512-digit parts |
| Inspected | r1 fixture driver | failed missing `compatibility-design-cases.v2.json` in scoped 265 **before** any native corpus; r2 reads the separately pinned original; r1 script/log/fixtures/keys retained |
| Inspected | 264 workspace 486+2 | predecessor only; not rerun |

**Controls (honest):**

Wrong catalog admission (`left: true` / `right: false`): skip exact discriminator (`catalogSchema` 0); skip validity window; skip release-tuple uniqueness; skip release version parse; skip nonempty interval; skip reserved uniqueness.

Wrong **version predicate** (not a signed-admission exploit): `exact-ignores-build` — `1.0.0+a` satisfies exact `1.0.0+b` if compare-equal replaces raw equality.

First fail **other** assertions:

- `omit-outer-latch`: follow-up prepare not `Err(Closed)` after a failed catalog.
- `numeric-precedence-lexical`: `1.0.0-beta.2` vs `1.0.0-beta.11` order +1 vs −1.
- `core-u64-overrefusal`: 29-digit core `999…9.0.0` valid=true but `u64` parse refuses.

---

## Independent probes

| Probe | Result |
|---|---|
| Public API | `recovery_catalog` / `metadata_versions` / `Error` not `pub` |
| Envelope `namespace()` vs catalog `schema_token` | envelope has no LF strip; catalog allows one final LF |
| `str_range` for artifact profile | `chars().count()` (Unicode) |
| String `hostCoreConstraint` in catalog | shape refuse (`signed-string-constraint-not-catalog`) |
| Store cleared after success | owned catalog/release index remain |
| 266 first-pass vs final groups | still on `signed()`; catalog does not collapse them |

---

## Remaining (do not count closed)

Full component checker and body-publisher↔namespace↔catalog identity/digest/constraint joins (268); policy/repair/artifact/current population/non-key subjects; other-root contexts; held custody/ancestry/floors/S4; batch/effects; native fence/slot/census/durability/writers; source selection; M3–M6. Host adapter still owns cap-before-allocation and custody. 267 is not installed runtime source or a registry grant.

---

## Verdict

- [x] Archive/pins/members verified. 377 product files: 371 unchanged vs 266. Nested 266/265/254/253/252/250 pins match reviewed archives. Extra completion corpus separately pinned.
- [x] **193** security tests, Clippy, and fmt reproduced. Ten controls behave as documented (six wrong catalog admissions; one exact-constraint build predicate; three other-first).
- [x] Same-budget 266 prepare; catalog structural prefix only; SemVer without machine integers; one trailing LF preserved on catalog name tokens.
- [ ] **Not** full metadata admission, current authority, native custody, or product installation.
