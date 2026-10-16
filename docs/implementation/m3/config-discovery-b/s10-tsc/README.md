# S10-TSC: the TypeScript configuration refusal (M3-B r8 successor S10)

**Design unit, contract successor, with a product commit. PROPOSED; not bound until Codex's ACCEPT-DESIGN-UNIT, the lead's assent and its lock commit.** Accepted law M3-B r8 (`../PROPOSAL-r8.md`, Codex `codex-m3b-r8-r3`) adds item 14a, the pre-Plan TypeScript configuration graph, and names successor **S10** (item 25, PROPOSAL-r8.md:1038). B2-c2, the JSONC reader and effective `allowJs`, lands with it. The B2-c plan r2 (§3, step 4) anticipated this: "if it is accepted, the B-S9 remedy route gets its successor rows". **Name:** this unit is S10-TSC, so that it is not confused with design unit B-S10 (the configuration schema admission materialization), which is not law r8's S10.

## What r8 requires of S10

Item 14a (PROPOSAL-r8.md:628-641) and the S10 row:
1. **The public detail registry:** the record `native.typescript-config-unresolved` and four `internalAliases` rows, one per internal key: `native.typescript-config-extends-unresolved`, `-extends-cycle`, `-bound` and `-malformed`.
2. **Its D9 row:** request-rejected, exit 2, D9 code `CONFIG.INVALID`, typed detail carrier "request rejection detail". The D9 code is not the public detail, so `CONFIG.INVALID`'s own remedy (B-S9) does not apply.
3. **Its remedy, keyed by `native.typescript-config-unresolved`,** in the public route remedies' successor (the native model's `PUBLIC_ROUTE_REMEDIES`) and its product carrier: one text true for all four internal classes.
4. **The product's detail vocabulary:** `schemas/sources/common-v4.schema.json` and its generated code, by B-S10's route.

## What it selects

| Copy | Parent(s) | Change |
|---|---|---|
| `registry/public-detail-registry.v1.json` | the m2 line's head, `m2/continuation-diagnostics-x4tc-r1/reference/public-detail-registry.json` (324 records), and the M3 snapshot-plan-c line's head, `m3/snapshot-plan-c/native-metadata-missing-r1/completion/public-detail-registry.v1.json` (319) | the union (328 records), plus the new record (329) and its four aliases (13); a new `standing`; two provenance fields, `snapshotPlanCCorrections` (the M3 line's `standing`, verbatim) and `typescriptConfigRefusalCorrection` |
| `design/common.schema.json` (the `workflows/schemas/common.schema.json` mirror of the closed enum) | the M3 line's selected copy, `native-metadata-missing-r1/completion/design/common.schema.json` | `DomainDetailCode` gains the member, appended |
| `reference/native_evidence_model.py` (the selected native reference) | B-S9's copy, with SD-7's bound line-1159 override applied | one `PUBLIC_ROUTE_REMEDIES` entry and one `D9_MAP` row, each keyed by the public detail, each with a two-line comment |
| `reference/native_evidence_model.v2.py` (the successor of the file law X12 names) | rustflags-long-lint-r1's copy, with SD-7's line-1159 meaning restored (LD-3) | the same two entries |
| `product/schemas/sources/common-v{1,3,4}.schema.json` | the accepted product sources, `native-publication/native-common-materialization-r1/sources/` | `DomainDetailCode` gains the member, appended, as that unit added its two |
| `admission-registry.json` | B-S10's copy | the three common rows and the common v1 alias row re-pinned; nothing else |
| `product/` | the product at `01c73e2` | exact copies of every changed product file (below) |

**The remedy** (568 ASCII characters, within `BoundedText`'s 1,024; SHA-256 `98fe066f…`):

> the TypeScript configuration could not be read before the Plan: make every extends base of the named configuration file present as a regular file inside the project, named by a well-formed ./ or ../ relative path or a lower-case package name, with no symbolic link the snapshot does not admit on its path, installing its package outside OpenSIP if needed; break any extends cycle; keep each file within 64 KiB and the graph within 32 files; or correct the file's syntax, so that it is JSONC with extends a string or an array of strings and allowJs and checkJs booleans

How it is true for each internal key (item 14a's table):

| Internal key | When (item 14a) | The next step the string gives |
|---|---|---|
| `-extends-unresolved` | no candidate regular file; absolute; rises above the root; a symbolic link before C1 | a regular file inside the project, named by a relative path or package name; no link the snapshot does not admit (before C1 it admits none; after C1, what its custody allows); install the package outside OpenSIP |
| `-extends-cycle` | the graph has a cycle | break any extends cycle |
| `-bound` | a file over 64 KiB, or over 32 nodes | keep each file within 64 KiB and the graph within 32 files |
| `-malformed` | not JSONC; `extends`, `allowJs` or `checkJs` of the wrong type; a malformed specifier | correct the syntax: JSONC, `extends` a string or array of strings, booleans; a well-formed `./`/`../` path or lower-case package name |

**The product change** (product commit; `product/` holds exact copies):
- **Vocabulary.** `common-v1`, `-v3` and `-v4` gain the enum member. The pinned contracts generator regenerated two outputs: `crates/contracts/src/generated/evidence.rs` (the `Common{1,3,4}DomainDetailCode::NativeTypescriptConfigUnresolved` variant, its `Display` and `FromStr`) and `apps/report/src/generated/report.ts` (its embedded source pins).
- **Pins.** `schemas/source-map.json` and `schemas/admission-source-map.json` select this unit's three source copies, and the admission map selects this unit's admission registry; `schemas/admission-registry.json` and the identity crate's `SOURCE_PINS` (`crates/identity/src/schema_registry.rs`) re-pin the three sources; the generator closure re-pins its four changed rows; the registry recipe follows.
- **The remedy's product carrier.** `crates/host/src/outcomes.rs` gains `REMEDY_TYPESCRIPT_CONFIG_UNRESOLVED`, the model string byte for byte, beside the other code-keyed remedies (`REMEDY_PROVIDER_NOT_SELECTED`). Its test (`outcomes_tests.rs`, `the_typescript_configuration_detail_is_admitted`) pins its length and SHA-256, parses the generated member, and admits the D9 row with the remedy and a subject as a `StepTermination` under the embedded common v4 schema.

## Lead decisions

Each is made under the owner's standing direction to decide on the lead's recommendation.

**LD-1. The form: complete successor copies (B-S9's form) with a product materialization (B-S10's form).** Every change is a new file at a new path, so no passage override is needed and the unit binds on today's verify_design. **Rejected:** passage overrides of `PUBLIC_ROUTE_REMEDIES` and `D9_MAP` on the B-S9 copies. An override replaces one line and cannot insert a row.

**LD-2. One registry, the union of the two accepted lines.** The registry has two accepted heads: the m2 line (initial-root binding, 468a, X4TC) and the M3 snapshot-plan-c line (C2PM-1, NIJ-1, DS4-P1, native-metadata-missing). Both descend from the same base. Their records are disjoint additions to it, and every shared field is equal (`check_s10_tsc.py` proves both). A new record must go into one selected registry, and only the union carries every accepted record. The copy takes the m2 head's form (records sorted by code; its correction fields kept) and keeps the M3 head's `standing` verbatim as a provenance field. **Rejected:**
- a copy of one head only, which would drop the other line's accepted records from the selected registry;
- a record added to each head, which leaves two registries.

**LD-3. Both model copies carry SD-7's bound meaning of line 1159.** SD-7 (contract successor 96) overrode line 1159 (`PROVIDER.NOT_SELECTED`) in both B-S9 copies, and the product carries its text (`REMEDY_PROVIDER_NOT_SELECTED`). The rustflags copies of the v2 file (successors 115 and 121) were made from B-S9's raw bytes, so their line 1159 still has the old text. This is B-S9's recorded residual hazard: verify_design cannot see a lost meaning on a new path. This unit's v2 copy restores SD-7's line. So both selected copies agree with each other and with the product. **Rejected:** copying the rustflags head as it is. That would select a copy without a bound meaning.

**LD-4. The product scope: the vocabulary and the remedy carrier; no route, row or alias table.** The host's terminations are item 10's outcome matrix (law M3-J1), whose `Observation` variants are rows. Adding a row for this refusal, and the four-row alias table of its instrument, belong to B2-c2, which produces the keys and cites this unit, as B2-c1's `INTERNAL_DETAIL_ALIASES` did for its keys. The remedy's carrier is a constant in `outcomes.rs` (`#[allow(dead_code)]` module, library only), so B2-c2 uses it without restating it. **Rejected:**
- an `Observation` variant now, which would change item 10's matrix in a vocabulary unit;
- materializing the M3 line's two codes that the product does not yet carry (`native.metadata-input-incomplete` and `native.path-manifest-limit`). They belong to their own units (DS4-P1 and native-metadata-missing).

**LD-5. The remedy text** is the table above. It names item 14a's limits exactly (64 KiB and 32 files). It describes the symbolic-link rule so that it stays true after C1. And it never restates `CONFIG.INVALID`'s remedy.

**LD-6. B2-c0 is unchanged.** B2-c0's wrapper pins B-S9's model bytes for its unit-discovery functions. This unit changes no function, only one remedy entry and one D9 row that no unit-discovery key reaches. `check_s10_tsc.py` replays the bound B2-c0 checker with this unit's model copy in place of B-S9's: every recorded result is equal. B2-c2's reference, which needs this detail's termination, loads this unit's copy.

**LD-7. The design mirror is included.** The S10 row names the registry and the product vocabulary. The closed enum's design mirror (`workflows/schemas/common.schema.json`) is drift-checked from the registry, and each M3 registry successor updated it. Leaving it out would let the mirror drift.

## Pre-existing conditions (recorded, not changed)

- **The product enum lags the registry by two codes.** They are the M3 line's unmaterialized `native.metadata-input-incomplete` and `native.path-manifest-limit` (LD-4).
- **The design mirror lacks nine m2-line records.** These are exactly the members the product carries only in common v4 (evaluator3 `common:4`), as before this unit. The checker records the gap (`missingFromMirror`), and it equals the product's v4-minus-v1 enum difference.
- **SD-7's line 1159 on the rustflags copies** (LD-3).

## Evidence

- **Scripts and records:**
  - `evidence/prepare_s10_tsc.py` (preparation; `preparation.json`, `prepare.log`);
  - `run_s10_tsc_generation.py` (B-S10's runner, paths and standing changed; `generation-summary.json`, `generation.log`);
  - `check_s10_tsc.py` (content);
  - `run_s10_tsc_checks.py` (candidate checks; `checks-r1/`);
  - `verify_scratch_s10_tsc.py` (`verify-scratch.json`);
  - `build_s10_tsc_package.py`.
- **The content check** (`check_s10_tsc.py`; 34 checks pass, recorded in `checks-r1/content-check.json`). It recomputes every copy's permitted difference from its parents. It executes both model copies (the B2-c0 loader's way) and checks `d9_map`, `D9_MAP`, `PUBLIC_ROUTE_REMEDIES` and `_detail` for each key against the S10 common v4 `DomainDetail`. It replays the bound B2-c0 checker with this unit's model copy: every recorded result is equal. And it compares the product copies with the worktree.
- **Candidate checks r1** (`run_s10_tsc_checks.py`, `checks-r1/`; lane held, priority 10, private 0700 TMPDIR). All rows pass:
  - the identity, contracts, host and storage suites, `--no-fail-fast`, on the base checkout and the candidate, with identical failure sets. Host has 8 failures and storage 33, the pre-existing crash-matrix synthetic cases B-S10 recorded. Host gains one passing test;
  - rustfmt on the three base-clean edited files (the generated `evidence.rs` is not rustfmt-clean at base and is the generator's output);
  - Clippy, warnings denied, all targets, over identity, contracts, host and storage;
  - the operability source census (114 rows, no finding);
  - the content check;
  - five mutations, each caught: a model D9 code flipped; an alias pointed at `CONFIG.INVALID`; an M3-line record dropped; a model remedy that restates `CONFIG.INVALID`'s; the product remedy altered (caught by the content check and by the host test).
- **Scratch binding** (`verify_scratch_s10_tsc.py`, `evidence/verify-scratch.json`). The product's `verify_design.verify` runs on the candidate worktree. The base lock refuses the candidate tree, because the S10 copies are not yet selected. With this record appended as successor 167, under a synthetic review and assent that are written to a scratch directory and then removed, it passes.
- **At integration**, after real acceptance and assent, with the bound lock in the candidate worktree: the report TypeScript lane, `tools/generate_contracts.py --check` and plain verify_design. This is as B-S10 did, because the lane's admission preflight needs the bound lock.

## Standing

No TypeScript resolution, JSONC reading or `allowJs` derivation; those are B2-c2's. No law change, no new D9 class, code or exit, and no new context-free alias beyond item 14a's four. No product qualification.
