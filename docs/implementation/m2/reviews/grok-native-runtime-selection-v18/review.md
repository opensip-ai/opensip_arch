# Native-runtime selection v18 — formal implementation-unit review

**Verdict: `ACCEPT-DESIGN-UNIT`**

Root remains lead. Not Claude agreement. Not live install. SOURCE-38 is composed, not re-accepted. Concurrent feature advisory is archived, not this unit’s approval. Root assent and private activation remain required.

**subjectManifestSha256** `2e8cada462e72ea4b90e703bb55077f472df562956b1a6c92486d258c3ef36af`  
`docs/implementation/m2/native-runtime-selection-v18-subject.json` **21499** bytes, **95** members, 94 successor candidates + successor record, paths sorted unique, 0 pin mismatches.

Successor `docs/implementation/m2/native-runtime-selection-v18/successor.json` **22076** / `7824be204290185b5c1197aefbb1f6477437c6591947682b31306daa0c408ad1`. `passageOverrides` is `[]`. Candidates cover the subject minus the record; each candidate pin equals the subject row.

## Parents (`contract_successor` 221–229)

Live lock **24 inventory / 35 contract** (`72063` / `ecae54f79143183b65204f0a821827ebe3e0824307bb6aadaddb9eda9d3b8e2c`). Independent `verify_design.py` on this export **passed** (`productQualification: false`); selected inventory v26. All three parents match disk and the live accepted set. None overwrite a subject member.

| Parent | Bytes | SHA-256 | Live class |
| --- | ---: | --- | --- |
| inventory **candidate** v26 | 147952 | `1a861b0c…a324` | last inventory; 396 files, 20 packages |
| runtime-17 successor | 11769 | `d41ff9c8…4853` | contract record |
| integer-profile (E39) successor | 4354 | `536754c6…0265` | last contract record |

Parents sorted. Four live inheritance rows remain parented at **v26** with `before` equal to v26 descriptions: `/files/7` `bootstrap.rs`, `/files/13` report `package.json`, `/files/202` `package.json`, `/files/269` `imported-v1.schema.json`. Zero passage overrides on this successor.

## Composition

Implementation `docs/implementation/m2/trials/native-runtime-18/subject.json` **51559** / `d097ac8a8f281ad286158f58f9678719f56232719ff2a8513db8919e2081b8c9` (also evidence copy). Export `/tmp/opensip-implementation/m2-native-runtime-subject-18`: **283/283**.

**257** non-lock product files byte-identical to frozen SOURCE-38. `product/design-lock.json` equals current live 24/35. `target-attribution-v2.schema.json` and nested `tools/typescript-boundary/tests/fixtures/product/design-lock.json` retained. Materialization map **16** owned paths = SOURCE-38 `changed ∪ new` (13 changed + 3 new); every map pin matches export, architecture candidate copy, and SOURCE-38. New paths are inventory-26 planned rows. Evaluator still depends only on identity.

`evidence/design.stdout` **353943** / `dbfce730…9134` equals `export-design.stdout` (post-copy equality). Preflight `verify_design` used the explicit `--feature-profile toml-workspace` contracts check.

Archived SOURCE-38 report `060a30db…4ec9` / 5819 (`NO-REQUIRED-FINDINGS`) and root disposition `10b7165f…33b8` / 510. Feature-profile advisory/addendum/disposition are archived separately and are not this design-unit’s approval.

## Guards and isolation

Identity policy: 8 registry tuples, 299 sources, `rootFeatures []`, parse-only pins, optional `serde_core` omit only on `toml_datetime`/`serde_spanned` with exact unconditional normal resolve-edge match. Frozen identity-deps stdout matches.

Contracts: `standalone` `serde_core` remains `result,std`. `toml-workspace` adds **only** `alloc`. Four isolated CLI controls: host/provider default refuse the same `unselected resolved features: serde_core ['alloc', 'result', 'std']`; explicit `--feature-profile toml-workspace` passes. Original provider metadata-check refusal preserved; resumption did not claim a second compile.

Host isolation **138** sources / **23** archives; tests.stdout **129** + doctest **1** = **130**. Provider isolation **rebuilt** for identity change: **26** sources / **19** archives; three unavailable outputs exit 1. Source-guard 64 OK.

Law (archived SOURCE-38, not re-blinded): opaque `TomlDocument`; full `DeTable::parse`; BOM/empty-radix/year-0/leap-second syntax; 4 MiB / crate 80 / 1M nodes typed Limits aborting package projection; 2 MiB development stack; winnow compiled-unsafe TCB without memory proof. 1933 E39 comparisons + 7 local Limits. Not full enumeration, native compiler provider, Run, replay, or custody.

## requiredFindings

None.

## Limits / not claimed

Not live write, not SOURCE-38 re-acceptance, not full M2, not native analysis availability, not compiled `cfg(feature="alloc")` on serde_core, not aggregate M6 resource qualification. Standing is root assent + private activation.
