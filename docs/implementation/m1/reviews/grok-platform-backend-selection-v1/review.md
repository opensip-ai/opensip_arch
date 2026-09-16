# Independent Grok review: platform-backend-selection v1 (getrandom override guard)

**Reviewer:** Grok (explicitly authorized). Codex remains lead. Not Claude agreement.
**Subject manifest:** `docs/implementation/m1/platform-backend-selection-v1-subject.json`
**Manifest SHA-256:** `3ad044c637d3d6b5c8010957bdd8337dce696c89c6d8f8cc79812555e2240134`
**Members:** 24
**Verdict:** **ACCEPT-DESIGN-UNIT**

Implementation/selection of CLI A-03: refuse an **effective** `getrandom_backend` override from `RUSTFLAGS`, `CARGO_ENCODED_RUSTFLAGS`, or Cargo config. `crates/platform/build.rs` panics if `CARGO_CFG_GETRANDOM_BACKEND` is set; pinned `getrandom = "=0.4.3"` (`default-features = false`) keeps the target default. No runtime entropy API change. Not product install, M1, release, or fresh blind consumer. Inventory v9 is a separate layout unit. Guard01 frozen baseline (4/5 lock) is reproduction source only, not authority for these bytes.

## Custody and joins

24/24 subject members match architecture bytes before and after. Candidates cover the subject minus the successor. `passageOverrides: []`. Parents: live bootstrap-selection-v1 successor `7ae04bcb…3906` / 28288, and proposed inventory v9 `75e5210a…58e2` / 120724 (not live).

Four owned mappings pin-match; all four paths exist in inventory v9. First three owned files are **byte-identical** to frozen guard01 (`442df270…29c3d`, 177 entries / 142 files, archive `e299f86e…3903ef` / 1160782). `tools/README.md` extends the installed bootstrap guide with an entropy-guard section. Live `Cargo.toml` lacks `build = "build.rs"` (211 vs 230 bytes); getrandom pin is unchanged.

Frozen guard subject was not executed against. Tests ran from `review/copy/guard-product`.

## Implementation

```rust
if env::var_os("CARGO_CFG_GETRANDOM_BACKEND").is_some() {
    panic!("OpenSIP refuses an explicit getrandom_backend override; ...");
}
```

Cargo sets `CARGO_CFG_*` from **effective** `--cfg` after env and config. The guard does not parse `RUSTFLAGS` itself, so an ignored ambient `RUSTFLAGS` under empty `CARGO_ENCODED_RUSTFLAGS` does not false-refuse (encoded flags take precedence). `cargo:rerun-if-env-changed` covers `CARGO_CFG_GETRANDOM_BACKEND` and `CARGO_ENCODED_RUSTFLAGS`. Compiler/toolchain authenticity remains trusted and out of scope.

## Tests and independent probes

Permanent suite, Cargo 1.95.0, isolated Python:

```
python -I -B product/tools/tests/test_entropy_backend.py --cargo /opt/homebrew/Cellar/rust/1.95.0/bin/cargo
```

**5/5 pass** (default build; RUSTFLAGS refuse; encoded flags refuse; `--config build.rustflags` refuse; ineffective RUSTFLAGS + empty encoded flags still builds).

Extra private probes **required cases pass**:

| Probe | Result |
| --- | --- |
| Unrelated `--cfg osip_probe` | builds (no false positive) |
| Target-triple `rustflags` setting `getrandom_backend` | exit 101, guard panic |
| Bare `--cfg getrandom_backend` (no value) | exit 101, guard panic (`is_some`) |
| Inject `CARGO_CFG_GETRANDOM_BACKEND=custom` into Cargo env | exit 101, guard panic (does not bypass) |

Root’s first wrong-CWD baseline failure is preserved in evidence; not treated as a pass.

## Must-fix / should-fix

None in this design-selection scope. Required findings remain empty.

## Limits

- Does not authenticate rustc/Cargo or block a malicious wrapper that never sets `CARGO_CFG_GETRANDOM_BACKEND`.
- Other cfg/flags, OS fallback, non-macOS targets, and release qualification remain open.
- Does not change getrandom version/features or host entropy functions.
- Public/live activation waits for genuine inventory v9 + this successor (and full ancestor passage re-projection). No fake approvals.
- Guard01 4/5 lock is not this unit’s authority.
