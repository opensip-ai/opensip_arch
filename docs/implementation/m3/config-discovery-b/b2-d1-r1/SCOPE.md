# B2-d1 r1: the closed YAML subset reader (M3-B unit B2-d, sub-unit B2-d1)

**Lead scope record, 2026-10-16. Unreviewed candidate, round 1.**

It implements B2-d1 of the B2-d plan r3, section 2 (`../b2-d/PLAN-r3.md`; Codex `codex-b2d-plan-r3`), against the bound B2-d0 reference, contract successor 171 (Codex `codex-b2d0-reference-r4`).

**Base:** product main `c4f8edd`, which binds B2-d0 with 171 contract successors and inventory v209; architecture `11bd0d38`.

## What it delivers

### `crates/host/src/yaml_subset.rs` (new)

`parse_pnpm_packages(raw) -> Result<Vec<String>, OutsideSubset>`: pure, first-party, with no dependency. It is the Rust form of the reference's `parse_pnpm_packages`, rule by rule:

- **The document:** UTF-8, at most 64 KiB, with no byte order mark and no tab. Only CRLF pairs are line breaks; any other CR is outside, at the end of input included. Every character must be in YAML 1.2's c-printable set, less DEL, the C1 block, NEL, U+2028, U+2029 and an inner byte order mark.
- **The lines:** blank lines and `#` comment lines anywhere; the single key `packages:` at column 0, with an optional separated comment; then either:
  - the empty flow form, `packages: []`, separated from the key by at least one space; or
  - at least one block item: at least one space, `-`, at least one space, a scalar and an optional separated comment, with consistent indentation.
- **The scalars:**
  - **single-quoted**, with `''` as the only escape;
  - **double-quoted**, with `\"` and `\\` as the only escapes;
  - **plain:** no leading indicator character, no `:`, and not a form a YAML 1.1 or 1.2 parser would type: null, a boolean, an infinity, NaN, a digit-led number-like run, or a date.
- **The result:** the ordered globs, or one typed refusal (`Bound`, `NotUtf8`, `Character`, `Structure`, `Scalar`), never a partial list. Every refusal has the same effect: B2-d2's recognition discloses `config-requires-evaluation`.

The reference's regexes are hand-written as exact checks. The number pattern `[-+]?([0-9][0-9a-fA-FxXoObB_.:eE+-]*|\.[0-9][0-9_eE+-]*)` and the date pattern `[0-9]{4}-[0-9]{1,2}-[0-9]{1,2}([Tt ].*)?` are matched on ASCII digits only, as Python's `[0-9]` matches. The separation rules match ` +#.*` and ` *( +#.*)?` exactly.

### `crates/host/src/lib.rs`

One dead-code-allowed library module declaration, plus its test module, with a comment. There is no caller until B2-d2.

### The vectors (`tools/host/yaml_subset_vectors.py` → `crates/host/src/yaml_subset_vectors.json`, new)

- **The grammar table:** 103 hand-written cases, 24 accepted and 79 refused. Every production of plan section 2 is accepted at least once, and every exclusion is refused at least once. That includes all the cases from the plan's r2 and from B2-d0's three review rounds.
- **The bound:** exactly 64 KiB, and one past it.
- **The substitution sweep:** 1,435 cases, every single-byte substitution from a 19-byte alphabet over three seed documents. The alphabet covers structure, quoting, controls, CR, LF, NUL, DEL and non-ASCII bytes. Each expected result is the reference's.
- **The oracle:** the bound B2-d0 reference (contract successor 171), pinned by bytes. Generation fails unless it gives every hand-written result. The table also caught one wrong hand-written expectation of mine: `2024-01-02x` is a digit-led number-like run, which the reference rightly refuses. It is now a refusal vector, and the accepted near-date cases are `2024-01-02z` and `202-01-02/x`.

### `crates/host/src/yaml_subset_tests.rs` (new)

Three tests:
- **every vector:** all 1,540 equal the reference;
- **each reason:** a refusal of each kind names its reason;
- **the full sweep:** every byte value at every position of every accepted grammar document returns a result and never panics, and the same input gives the same result.

### FW-01 (`tools/tests/test_discovery_fw01.py`)

`yaml_subset.rs` joins `COVERED`, so it may not spawn a process, open a socket or write. It also joins `PURE`, so it does no filesystem, environment or process access of its own. The planted negative controls cover it, and `yaml_subset_tests.rs` is asserted to be outside production.

## Checks

Lane r1, `evidence/b2d1-checks-r1/`. Attempt 1 (`b2d1-checks-r1-attempt1/`) failed only Clippy's `type_complexity`, on the tests' case tuple, which is now the `Case` alias. Every other row of attempt 1 passed, and its seven mutations were caught. The second attempt is the lane of record:
- **the host suite** at base and candidate, with equal failure sets (8 at base) and three new tests;
- **rustfmt** on the new files and on `lib.rs`, which is clean at base;
- **warning-denied all-targets Clippy** on host;
- **the YAML subset tests,** and the vector `--check` against the bound reference;
- **FW-01,** environment exceptions, the operability source census and verify_design;
- **seven mutations of the reader,** each failing the YAML subset tests:
  - the dash separation dropped;
  - the characters unchecked;
  - a bare CR accepted;
  - a null `packages` accepted;
  - the number check dropped;
  - an unseparated empty flow accepted;
  - a plain `:` admitted.

## Not claimed

- No recognition (B2-d2).
- No caller.
- No qualification.
- No completion of B2-d, B2 or M3-B.

## Inventory

New paths for the inventory after acceptance:
- `crates/host/src/yaml_subset.rs`;
- `crates/host/src/yaml_subset_tests.rs`;
- `crates/host/src/yaml_subset_vectors.json`;
- `tools/host/yaml_subset_vectors.py`.
