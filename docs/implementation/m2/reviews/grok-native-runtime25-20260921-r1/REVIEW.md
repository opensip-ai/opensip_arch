# Cumulative source/runtime25 — design-unit review

**Verdict: `ACCEPT-DESIGN-UNIT`**

Bounded **development source integration** of frozen368 onto live inventory55 / runtime24. Not release, not M2 completion, not current authority, not writers, not five-member binding, not S9.3, not account/home qualification, not product installation. Root assent is **not** manufactured. Live product was **not** written (`HEAD` `373aae2c`; `Cargo.lock` still fa72e50 6111 B).

**subjectManifestSha256** `3b4fa33915e92ff60240fb222389725680ca22101c27bc40d539f305163bbe5a`  
`docs/implementation/m2/native-runtime-selection-v25-subject.json` **8436** B, **39** members, paths sorted unique, **0** pin mismatches. Successor `candidates` cover the other 38 members. `passageOverrides`: [].

Parents (selected bases): runtime24 successor `1ad92c24…f027` / 16469 B; inventory55 `093d0da4…8e35` / 276439 B / 697 files.

Prior dependency368 REVIEW `33f06479…6fa8` / review.json `49d4652a…98bd` (`ACCEPT-DEVELOPMENT-CLOSURE`) are in this subject and match `/tmp` bytes. 368/367/366 source reviews are bound only within their actual scopes.

---

## Map v2 and staging (reproduced)

`materialization-map.json` schemaVersion **2**: **327** mapped writes (15 replacements + 312 additions) + **255** unchanged non-lock = **582** non-lock; archive `design-lock.json` excluded so live selected inventory55 lock is preserved. `baseProductHead` `373aae2c`. Historical v1 map consumer is not used.

Independent `stage.py` to a **new** path `grok-out/staged-product`: verified all **644** archive members **before** creating output; rehashed live **271**-file baseline; refused destination collisions; staged 327 mapped files from the archive; copied 255 unchanged from live; final **582** non-lock hashes match 368 product; staged `design-lock.json` **byte-equal** live selected lock; live product pins unchanged after staging.

`before` hashes of the 15 replacements match `fa72e50` runtime bytes (including `Cargo.lock` 6111 / `36889e3d…`). Additions have `before: null`.

---

## Composition (not only hashes)

Host `installation_lineage` remains a macos-gated provisional module: one fence, original node files and store markers, 367 walker, `Closed` latch, no `File`/root escape, no create/repair. Lifecycle lineage is a six-field codec + supplied callback, not native publication. Security/storage/platform owners stay at their 366–368 reviewed boundaries. Evaluator atom-registry/`lib.rs` and identity `closure.rs`/`lib.rs` are in the 15-file delta (hence the **fresh** provider rebuild). CLI/provider stay unimplemented: provider receipt `nativeCompilerIntegrationImplemented: false`; three unavailable probes expected exit 1.

Generated security tables remain generated; wrappers keep `#[path]`. Tests/fixtures from 368 are mapped additions, not rewritten live.

**tools/README** in frozen368 still says the crypto profile “remains proposed pending independent dependency review.” Runtime25 README/successor/`evidence/dependency-review.json` bind the **accepted** development-closure review (`49d4652a…`) instead of rewriting already-tested 368 bytes. That is documented preservation, **not** a blocking integration defect and **not** a requirement to mint a metadata successor before this unit. A later README-only successor could clarify live docs; it is not required to accept this composition.

---

## Checks actually performed

| Check | Result |
| --- | --- |
| 39-member subject rehash | 0 mismatches |
| Independent restage | 644 archive / 582 non-lock / live unchanged |
| `verify_design.py` on staged lock+implementation | **passed**; stdout SHA **byte-equal** frozen evidence `dbfdf1ce…ab7e` (465793 B); **31** inventory successors / **44** contract successors; generation **40**; admission **48** |
| `test_design_binding.py` | **64** OK |
| `test_dependency_policy.py` | **9** OK |
| Native 755+6 | **not rerun** (root complete; 369 `test-counts.json` 755/0/2 + 6 doctests) |
| Compiled artifacts (369) | **47** unique external compiled packages vs **51** lock rows (`syn 2.0.119` + `curve25519-dalek-derive` absent on aarch64 host compile, as in the dependency review) |
| Provider 26/19 + 3 unavailable | root 369 receipt; unimplemented |

---

## 211/218 and remaining limits

This unit **does** propose the 288 inventory55 paths (including `account.rs` and checkpoint211 files) as development **source**. It does **not** discharge the two carried unresolved obligations: OS-account/home qualification, or treating those pending strings as selected32 policy. S9.3 / full five-member binding / writers / current authority / platform qualification / M2–M6 remain **open**. Provisional observations must not mint admitted registry/binding authority.

---

## requiredFindings

None.
