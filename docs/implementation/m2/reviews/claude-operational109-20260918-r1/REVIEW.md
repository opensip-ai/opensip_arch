# Independent bounded review — operational-file codec 109 (Rust)

Reviewer: Claude (actual independent reviewer; Codex remains implementation owner). 2026-09-18.
Request: `REQUEST.md` (copy of `operational109-20260918-REQUEST.md`).
Scope: the single changed file `crates/security/src/journal_store.rs` in frozen
`operational-file-draft-checkpoint-109`, as an implementation of the byte profile I reviewed in
reference 108 (D1). **Not** a review of the rest of `journal_store.rs`, of the value constructors'
history (review 97), of storage, dependencies, targets or any current authority.
No frozen, selected or product byte was edited; builds and mutants ran in scratch copies under
`claude-out/`; no commit, push or delegation.

## 1. Subject verification (done by me, before extraction)

| Item | Value |
|---|---|
| `subject.tar.xz` | 4,120,112 bytes, SHA-256 `14a2f6294ccda60b51b6bd60b4f6a863331fbc90a6c2482f5382ff4943425b74` = `archive-pin.json` |
| `subject.json` | SHA-256 `0cf7010c3d28ac04928be2d0db5f793020a00a25790b7d41f470f2c4cae578e3` |
| Members | 378 of 378 regular files, each length + SHA-256 equal to the manifest, read from the tar before any write; 0 symlinks/unsafe paths/extras; re-verified after all work (`mode: re-verified`) |
| Product pins | 330 of 330 equal on disk; no unpinned product file |
| Parent | `parent-inputs.json` (330) equals **my own** verified extraction of frozen 106, file by file; 329 unchanged, 0 added, 0 removed |
| Changed | `crates/security/src/journal_store.rs` → `bd737a0620822ab8e08423c364a6c7200caa3de1652251abefcea86e9fafc899`; `journal_store-before109.rs` equals my 106 copy |
| Diff | 146 added lines, **0 removed or modified** (`claude-out/journal_store.diff`) |

The README's "explicit metadata dependency" is the in-crate path `crate::trust::metadata`; no
manifest or lock changed, which the pins confirm.

## 2. What the change is

`decode_operational_file(raw, admit)`: `metadata::parse(raw)` → `admit(&value)` (the existing closed
`Witness::from_value` / `CarrierFloor::from_value`) → `metadata::encode(&value)` → `raw == canonical`
→ `AdmittedOperationalFile { record, bytes: raw.to_vec() }`. `encode_operational_file` admits the
value first and then returns `metadata::encode`. Errors are the local enum
`Decode | Shape | Encode | NonCanonical`. There is no I/O, no presence/absence decision, no floor or
witness write, and no caller outside `#[cfg(test)]` — consistent with the stated standing.

This is exactly the order of the frozen 108 reference (`load_json_strict` → `_shape` → byte
equality), and the value is parsed once, so the admitted record and the compared bytes cannot come
from different parses.

## 3. Evidence

**Owner checks, fresh scratch build** (Rust 1.95.0, `--offline --locked`, my previously verified
51-crate vendor directory): `cargo test -p opensip-security` 60 passed / 0 failed;
`cargo clippy -p opensip-security --all-targets -- -D warnings` clean.

**Embedded corpus provenance.** The 143-case constant is *value-equal* to the 108 case file I
verified myself (`61274747…a1d1`, 80,369 bytes): same 143 ids, kinds, `rawHex`, expectations, 8
positives. It is not byte-equal (74,350 bytes, compacted). "Exact 108 reference cases" is therefore
true of the values, not of the file bytes; the provenance file should say "value-equal".

**Differential against the frozen 108 Python reference** (`probes/gen.py`, `rust_probe.rs`,
UCD-15 interpreter): 41,117 inputs — 18k canonically-encoded shape-pool values presented to *both*
kinds, 27 textual spellings of 9 canonical seeds, 24,000 byte-level mutations, structural extremes.

| Reference → Rust | Count |
|---|---|
| OK → OK | 1,963 |
| SHAPE → SHAPE | 24,588 |
| DECODE → DECODE | 14,448 |
| NONCANONICAL → NonCanonical | 116 |
| SHAPE → **DECODE** | 2 |

**Admission differences: 0.** On every Rust acceptance the probe also asserted, after overwriting
the caller's buffer, `file.bytes == raw` and `encode_file(parse(raw)) == raw`; no assertion failed.
The two class differences are the single input `"\ud800"` (lone-surrogate escape) for each kind:
the Python loader yields a string and refuses at shape, Rust refuses at decode. Both refuse; it is
the Rust-side mirror of my 108 N-2 and cannot reach admission because every admitted string is
64-hex or a fixed token.

**Mutation** (`probes/mutation.py`, scratch copy, compile failures would not be counted — none
occurred; baseline green first):

| Mutant | Result |
|---|---|
| skip raw equality | killed (both new tests) |
| length-only equality | killed (corpus: reordered keys keep length) |
| prefix equality (`starts_with`) | killed (corpus: trailing bytes) |
| encoder skips shape | killed |
| encoder appends newline | killed |
| canonical check moved before shape | **survived** — changes refusal class only, never admission |
| return `canonical` instead of `raw` | survived — **equivalent** (equal on every accepting path) |

5 of 5 behaviour-changing mutants killed. I confirm the owner's two.

## 4. Findings

No blocking finding.

- **N-1 (low) — refusal class is unpinned.** The corpus test asserts only `is_ok() == expected`;
  only negative zero, empty, 4 MiB and depth 65 assert a class. The class-order mutant survives.
  D2's Step 4 wording (my C2a, Codex item 1) makes the *reason* part of the reportable observation
  ("exact raw-byte SHA-256 + bounded reason"), so the successor that wires this codec in should pin
  class for one representative per class and per kind, including "bad shape **and** non-canonical →
  Shape".
- **N-2 (low, carried) — reference/Rust class split on lone-surrogate escapes** (`SHAPE` vs
  `Decode`). No admission effect. Decide which is normative when 108 N-2 is dispositioned; do not
  let a future shared corpus with classes encode both.
- **N-3 (note) — provenance wording**: value-equal, not byte-equal (above).
- **N-4 (note, boundary) — `from_file_bytes(&[])` is `Decode`.** Correct for a codec. The README
  already says the capture layer must classify empty/unreadable before calling; when that layer is
  written, `Decode` on empty input must not be mapped to `witnessMalformed` without that prior
  classification (v8: absent → `witnesslessRestore`, not malformed). Nothing to change here.
- **108 N-1 does not apply**: the input is `&[u8]` and the accepted bytes are copied into an owned
  `Vec`; I exercised it on all 1,963 acceptances. Agreed with the owner's statement.

Unresolved assumptions: `trust::metadata::{parse, encode}` are taken as reviewed in my
signed-security 106 review (30,027-input differential there); I did not re-review them. No Linux,
no x86_64, no dependency qualification. D2 and D3–D6 remain open and are untouched by this subject.

## 5. Bounded verdict

**Codec 109 (`journal_store.rs` delta only): reviewed, no blocking findings; N-1/N-2 to carry to the
successor that gives the codec a caller.** This is not approval of `journal_store.rs` as a whole, of
any file I/O, custody, recovery or floor authority, nor cumulative approval or selection.

Evidence index: `claude-out/pin-verification.json`, `product-pins.json`, `embedded-cases.json`,
`journal_store.diff`, `probes/*`, `hashes.txt` (the failed first generator run is preserved as
`probes/gen.FAILED-r1.txt`).
