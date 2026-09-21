# Cumulative native development dependency closure — frozen 368

**Verdict: `ACCEPT-DEVELOPMENT-CLOSURE`**

Bounded **private/development host integration on this macOS arm64 host** for frozen `native-lineage-checkpoint-368`. This is **not** runtime25 selection, memory-safety proof, Linux/x86 execution, release qualification, inventory activation, or runtime authority. Checksum/layout acceptance of inventory55 does **not** substitute for this decision. Historical Claude **crypto59-62** and **crypto105** reviews explicitly did **not** accept dependency closure; they are not treated as prior acceptance. Product runtime bytes compared here are **`fa72e50`**. Workspace HEAD `373aae2c` (inventory55 layout selection; design-lock only) is root work, not this review and not runtime acceptance.

RequiredFindings: **none**.

---

## Subjects pinned

| Subject | Bytes | SHA-256 | Members |
| --- | ---: | --- | ---: |
| `trials/native-lineage-checkpoint-368` | 6928824 | `f01f6ef1650d2e58cf9f831221e6c37d0d88cb708de06724531703e4b99eecf9` | **644** (583 product) |
| `trials/materialization-preflight-368` | 30340 | `fabb8ed5831dbb8119d136bcb2f1af1d9e8348dc271af60172fecaf4856cc84d` | **68** |
| Exact source | — | `/tmp/opensip-implementation/m2-native-lineage-368/product` | **583** files, archive-equal |

Freeze product matches every archive `product/` pin. Inventory55 REVIEW `14ef27a6…7bc9` / `review.json` `9c7d41f5…0292` unchanged. 368 source REVIEW `f03f5e31…da78` unchanged.

---

## vs selected runtime `fa72e50`

Tracked live files **271**; candidate **583**. **256** identical; **15** changed; **312** added; **0** live files missing from the candidate. Changed paths: `Cargo.lock`, `Cargo.toml`, evaluator atom-registry/`lib.rs`, host Cargo.toml/`lib.rs`/`native_owner_tests.rs`, identity `closure.rs`/`lib.rs`, platform `filesystem.rs`/`lib.rs`, `tools/README.md`, contracts/identity dependency policies, `test_dependency_policy.py`.

Cargo.lock: selected **23** external rows → **51**. **28** additional rows (no removals): 27 new names plus **`syn 2.0.119`** beside retained **`syn 3.0.5`**. Three local owners added: `opensip-security`, `opensip-lifecycle`, `opensip-storage`.

---

## Profiles actually checked

Host `--feature-profile security-crypto-workspace`: same as `toml-workspace` except Cargo **metadata** features for `quote` and `proc-macro2` add `default` (`["default","proc-macro"]`). Standalone contracts profile and provider `toml-workspace` remain exact (`quote`/`proc-macro2` = `["proc-macro"]` only). No automatic fallback or union. Identity checker has **no** feature-profile option: 8-tuple TOML parse-only graph, `rootFeatures: []`, **299** source files verified; `memorySafetyProof: false`.

Independent replay of all **32** preflight jobs (2 lanes × 4 metadata targets × metadata/contracts/identity/edges vs inventory55): **32/32 exit 0**. Stdout SHA-256 **byte-identical** to frozen preflight `dependencies/result.json`. These are metadata/source checks, not target execution.

Resolved **host `aarch64-apple-darwin`** (this lane): `ed25519-dalek` features **[]** (manifest `default-features=false`); `curve25519-dalek` `["digest"]`; `unicode-normalization` `[]`; `rusqlite` `["bundled","limits","modern_sqlite"]`; `libsqlite3-sys` bundled/`cc`; `sha2` `[]`; `getrandom` `[]`; `syn` **3.0.5** only. **`syn 2.0.119` and `curve25519-dalek-derive` appear in x86_64 metadata, not aarch64.** Lock still carries both syn versions. Metadata `quote`/`proc-macro2` `default` is the explicit crypto-workspace allowance; it is not a claim that the Mac compiler enabled extra compiled features.

---

## TCB / what was inspected

Inspected: freeze+preflight archives; `fa72e50` tree vs freeze product; both Cargo.lock graphs; `security`/`identity`/`platform` manifests; `dependency-policy.json` three profiles; identity policy local/registry pins; 51 `.crate` SHA-256 = lock checksums; 32 checkers; host-materialization `sources.json` (**454**), `dependencies.json` (**51**, checksums = lock), `environment.json` (isolated `CARGO_HOME`, preserved `HOME`, Darwin user `TMPDIR`, `RUST_TEST_THREADS=1`), and **`receipt.json` (present, root-produced)**. Did **not** run cargo test/build (root host suite; no overlap).

`opensip-security` and `opensip-identity` `unsafe_code = "forbid"`. Platform `build.rs` only refuses ambient `getrandom_backend`. Bundled SQLite C (`libsqlite3-sys` + `cc`), proc-macros (`serde_derive`, `syn` 3, and on x86 `curve25519-dalek-derive`/`syn` 2), and the system compiler/SDK/linker remain **trusted build inputs**, not source-reviewed memory-safe crates. Crypto59-62 **D-1** (target-dependent paths untested) still stands for Linux/x86.

Root receipt standing: development host validation of frozen368; **no** dependency acceptance in that receipt. Commands all exit 0 (`build`, workspace `tests` 531.6s, `doctests`, `version`/`help`). This review treats that as **root’s** execution record, not a substitute for this closure decision.

---

## Decision

These **exact** lock bytes and explicit `security-crypto-workspace` / identity parse-only / toml-workspace selections are **acceptable for private macOS arm64 development host integration** of frozen368. Existing SQLite/identity/contracts **source** reviews support only unchanged portions with their own pins; they do not close this 28-package delta.

**Not granted:** runtime25; live product installation; Linux or x86_64 execution; release; five-member binding; current authority; writers; M2–M6; proof that `quote`/`proc-macro2` compiled features equal metadata.

---

## requiredFindings

None.
