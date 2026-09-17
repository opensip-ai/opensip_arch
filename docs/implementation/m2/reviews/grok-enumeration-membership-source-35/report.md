# Frozen trial review: enumeration-membership-35

**Reviewer:** Grok. Root remains lead. Not Claude agreement.
**Kind:** Scoped source review of `inspect_enumeration_membership`. **Not runtime, not complete enumeration, discovery, security custody, package projection, or replay.**
**Work tree:** `/tmp/opensip-implementation/m2-grok-enumeration-membership-source-35-review/review`. Live/frozen/history not edited. No commits.

Advisory-35 + exact-profile JSON addendum were archived separately (`acd512eb…e1c4` / 5471, `7e667dfa…c7a4` / 609) and are **not** this source’s acceptance. SOURCE-34 report `de03e583…ab3d` / 3472 remains no-required, accepted narrowly for later integration.

Private inherited lock is `515f092c…b523` / 36241 (**9/15**). Live independently **23 inventory / 32 contract** (`393a690e28f3f9bb301b2818460599a001fb232c432a85592f514d4ebcf0b722` / 68099); last inventory candidate v25; last contract runtime-16-r2. That live base is **not** this trial. Live has **no** `enumeration.rs`.

## Subject pin

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| `docs/implementation/m2/trials/enumeration-membership-35/subject.json` | 52059 | `65c400e375f29c7f1d8575f1c198d3d739708de91da06a02b4a671ce38b58920` |
| adjacent `subject.tar.xz` | 1662848 | `2ae61304d9863bdb197ddb09eff0c060f12df940320466b8f5c944d39ae2c085` |
| export | `/tmp/opensip-implementation/m2-enumeration-membership-subject-35` | **288/288**; 0 extra |

288 paths unique and string-sorted. Dependency pins hash-match SOURCE-34 `15a286df…1d4f`, SOURCE-32 `c52cf367…ec96`, SOURCE-34 report, advisory-35, JSON addendum.

## Source delta vs frozen 34

**251** product files byte-identical, including identity sources, Cargo.lock, evaluator Cargo.toml. **No new paths.** Four changed: `enumeration.rs` (**20457** / `cdbcadb378e6e3140630e3b3564cb0e68afe99bec63d9e188b0cbbe640f2eff4`), `lib.rs` export, host tests, fixture **2842447** / `16d873d3…a2a2` under 4 MiB. Fixture `cases`/`values` **3712** extent cases **equal by value** to SOURCE-34. External TCB tuples unchanged.

Harness uses SOURCE-32 pinned overlay `enumeration_model.v1.py` **49811** / `69b0eee39a45a941d7ab1ef22c0c8be161edd436b1441b27017f98fd1bcffe85`, not a stale sibling.

## Algorithm / schema / errors / resources

`inspect_enumeration_membership(&RegisteredSchemas, membership, snapshot_paths, steps)`:

1. **Unit roots first** (`ENUMERATION_MEMBERSHIP_UNIT_ROOT`) and **return** — no later laws mixed.
2. Snapshot coverage / unique paths (`ENUMERATION_ADMISSION_PRECONDITION`).
3. UTF-8/`>=` unit and member-root order, ordinals, TS/JS kind projection, row path order, `unsupportedFiles` / `outsideBoundaryFiles` projection (`ENUMERATION_MEMBERSHIP_ORDER`).
4. Per-row derivation: pruned `node_modules`/VCS/`target` under Cargo roots; deepest same-family unit; grammar-only vs unsupported from **bundled** suffix metadata; outside-boundary rechecks **suffix family + null ordinal only** (Plan does not retain security inventory). Mismatch → `ENUMERATION_MEMBERSHIP_ROW_DERIVATION`.
5. Recomputed **inside-only** native `UnitMembershipV1` (empty `outsideBoundaryFiles`/`erasedFiles`) is `canonical_bytes` + `registry.schema(urn:…native:evidence-schemas:v2, /$defs/UnitMembershipV1).admit_json` — same as selected `assign_membership`. Schema `Mismatch` → row-derivation; schema `Limit` → `Limit`; other schema errors → `Shape`.

`RegisteredSchemas::from_sources` is the only public constructor: exact `SOURCE_PINS` census, length then hash then `$id`. No arbitrary schemas. Host tests use `embedded_schema_registry()`.

Steps copy-bound local row/unit/segment visits **and** the recomputed schema check; not an aggregate Plan work unit. Semantic refusals stay `Ok(checks)` with named codes; `Shape`/`Limit` stay typed errors.

Not discovery, native input admission, security custody, package projection, complete enumeration, or replay.

## Reproduction (rustc 1.95.0, `--locked --offline`)

- Frozen membership actual vs expected: **2025/2025**, 0 mismatch (2019 checked with 0–2 refusals; **6** `Limit` controls `limit-{0,1,2}-{0,1}`).
- Host `enumeration_membership_rederives_rows_order_roots_and_snapshot_coverage` and extent test ok. Workspace **124** passed. Clippy `-D warnings` Finished. Identity policy `sourceFilesVerified: 110`.

Preserved: **7** duplicate-member-root mismatches (`initial-missing-recomputed-shape`) where omitting the recomputed schema check dropped `ROW_DERIVATION`; current actual includes both ORDER and ROW_DERIVATION. Preserved initial test import failure (`embedded_schema_registry` not in scope, exit 101) then corrected.

## requiredFindings

None.

## Limits (not required findings)

- Does not implement discovery, security-boundary inventory, package projection, full enumeration, parser, Run, or replay.
- Live 23/32 (layout-25 / runtime-16-r2) is a **separate** runtime base; this trial keeps inherited 9/15.
- Advisory-35 / JSON addendum are not this unit’s acceptance.
- SOURCE-34 remains a narrow prior, not re-opened here.

## Verdict

No required findings. Private membership diagnostics match the selected assign_membership composition on 2025 cases, admit only pinned `RegisteredSchemas`, and do not claim enumeration or runtime authority.
