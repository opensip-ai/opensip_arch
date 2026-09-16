# Independent Grok review: contracts-dependency-selection v1 (known-source enforcement)

**Reviewer:** Grok (explicitly authorized). Codex remains lead. Not Claude agreement.
**Subject manifest:** `docs/implementation/m1/contracts-dependency-selection-v1-subject.json`
**Manifest SHA-256:** `d6404eb9e18bdb7f7f76d57545e0e327154041de881ad90625f0ae3520e5e7be`
**Members:** 24
**Verdict:** **ACCEPT-DESIGN-UNIT**

Implementation/selection of known contracts source + dependency enforcement. Four owned files. SchemaVersion 2 adds exact local manifest + seven Rust-source pins to the historical 11-dependency lock checksums/resolved features and library-only target. All 11 dependency versions/checksums/features match `contracts-dependencies.v1.json`. This is **not** native-purity proof, compiler/wrapper/cfg attestation, or hashing of extracted registry trees. Not product install, M1, provider isolation, release, or fresh blind consumer. Inventory v10 is a separate layout unit. Frozen integration02 6/6 baseline is reproduction only.

## Custody and joins

24/24 subject members match architecture bytes before and after. Candidates cover the subject minus the successor. `passageOverrides: []`. Parents: live platform-backend-selection-v1 successor `f809813f…d865` / 5813, and proposed inventory v10 `6608fabd…8bc9` / 121810 (not live).

Four owned mappings pin-match; all four paths exist in inventory v10. Three code/config/test files are **byte-identical** to frozen integration02 (`a5994024…57563`, 242 entries / 192 files, archive `dbc06f65…ded7` / 1299182). `tools/README.md` extends the live guide. Frozen subject was not executed against.

## Implementation

`check_dependencies.py` requires `schemaVersion == 2` and a local package (`source is None`). It walks `crates/contracts/src` plus pinned `Cargo.toml`: sorted unique pins, symlink/nonregular refusal before read, exact bytes. Production targets excluding test/bench/example must be exactly one `lib`. Non-root resolved packages must be crates.io registry, match lock checksums, have no `links`, and match `resolvedFeatures`. Dev edges and `cfg(any())` version-coupling edges are skipped. Caller `--policy` is trusted after design verification; the helper is not an approval verifier.

Policy provenance: 11 names/versions/checksums equal the historical conditional audit; resolved feature sets equal by name (historical list vs policy map). `sourceOwner` remains `docs/implementation/m1/contracts-dependencies.v1.json`. Live `crates/contracts` bytes match all eight `localSources` pins.

## Tests and independent probes

Private copy of frozen integration02 product, Cargo 1.95.0:

```
python -I -B product/tools/tests/test_dependency_policy.py --cargo /opt/homebrew/Cellar/rust/1.95.0/bin/cargo --target aarch64-apple-darwin
```

**7/7 pass** (selected profile 11 deps / 8 sources; sibling `serde_json` `raw_value` feature unification; effectful `lib.rs` addition; extra `src/` file; symlink same bytes; FIFO; duplicate pin). Metadata is freshly captured `--locked --offline --filter-platform`; `Cargo.lock` bytes unchanged. Prior 6-test log is preserved.

Extra probes:

| Probe | Result |
| --- | --- |
| schemaVersion 1 policy | refuses `selected local contracts source profile required` |
| Extra regular file at `crates/contracts/unselected_root.rs` (not under `src/`) | **still passes** |
| Extra file under `crates/contracts/tests/` | **still passes** |

The census is the **pinned src+manifest set**, not the whole package directory. Extra compiled effects and extra `src/` members refuse. Package-root or `tests/` extras are outside that set (test-lane extras are also consistent with library-only production). Disclosed as **S1 should-fix / limit**, not a required finding against the stated known-source scope.

## Must-fix / should-fix

Must-fix: none. Required findings remain empty.

**S1 (should-fix / disclosed limit):** `check_sources` only observes `src/` plus `Cargo.toml`. Extra regular files elsewhere in the contracts package do not fail the set comparison. Do not treat a pass as a full package-tree census.

## Limits (not fulfilled M1 duties)

- Does not authenticate arbitrary policy, Cargo/rustc, or compiler wrappers.
- Does not rehash crates.io archives or extracted registry trees (compares lock checksums only).
- Does not attest arbitrary Rust cfg, proc-macro/build-script effects, or native TCB (historical ACCEPT-BOUNDED-NATIVE-TCB / ACCEPT-BUILD-HOST-EFFECTS remain bounds, not proofs).
- Provider isolation, build-input receipts, feature/platform matrices, M1, release, and fresh blind consumer remain open.
- Public/live activation waits for genuine inventory v10 + this successor (and ancestor passage re-projection). No fake approvals.
- Frozen 6/6 baseline does not approve these bytes.
