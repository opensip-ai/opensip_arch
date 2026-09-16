# Independent review: m1-canonical-subject-01 (first OpenSIP implementation unit)

## Status: INCOMPLETE, verdict withheld

Bash was denied for this entire session (don't-ask mode), so **no command ran**:
- no SHA-256 or manifest recomputation
- no `cargo test`, `cargo clippy` or `cargo metadata`
- no Python unittest or design verifier
- no probes

Reading source, tests, dependency sources and architecture documents is complete.
**Static reading found no required finding.** I am still not issuing
`ACCEPT-UNIT`, for three reasons:

1. I have not verified that the files I read are the manifest-bound subject.
2. I have not reproduced the claimed 9/7/46 passes against the snapshot.
3. The adversarial probes are written but have not run.

`review.json` therefore carries `"verdict": null`, so it fails closed. The probes
and exact commands are in `probes/RUN.md`. Running them, or granting Bash and
re-invoking this review, is what can turn this into a verdict.

- Subject manifest: `/tmp/opensip-implementation/m1-canonical-subject-01.json`.
  The claimed SHA-256 is `8b2c31253d4699c9b25539000930234553df7f915eea011643ec675d70a3ef07`
  (not recomputed).
- Scope reviewed: `crates/identity` lexical parse, canonical encoding, H and raw SHA-256;
  `design-lock.json` plus `tools/verify_design.py`; the root Cargo workspace.
  Not graded: schema carriers, descriptor/array-order admission, semantic replay,
  provider, CLI, M1 or release. The five plan refinements are not repeated here.

## 1. Canonical profile conformance (static)

Checked against identity-and-evidence.md §3 (lines 109–175),
admission-and-qualification.md §1 (lines 8–41) and `foundation/canonical.py`.
Every item below matched on reading.

| Obligation | Implementation | Assessment |
|---|---|---|
| Byte cap 4 MiB is inclusive and checked before decoding (§3:117–120, canonical.py:41) | canonical.rs:62–64, then UTF-8 check at :65 | Conforms. An input over the cap is refused, never truncated. |
| Depth 32: the root container counts as 1; scalars and keys add nothing (§3:117–119) | canonical.rs:104–106 (parse), :326 (encode) | Conforms. Same boundary as canonical.py:13 (depth ≥ 32 refused, 0-based). Recursion depth is at most 32. |
| Integer grammar, with floats and exponents refused before any numeric conversion (§3:113–116; §1:10–17) | canonical.rs:120–137 | Conforms. `01`, `-01`, `+1`, `-` and `.5` are malformed JSON. `.`, `e` and `E` after the integer token are refused as floats. |
| `-0` refused | canonical.rs:138–140 | Conforms. `-0.0` gives a float refusal first; both are refusals. |
| Range [-2^63, 2^64-1] | canonical.rs:7–8, 15–21, 144 | Conforms. i128 overflow and in-i128 out-of-profile values both map to `IntegerRange`. A 4 MiB digit run is scanned linearly and `parse::<i128>` fails early. |
| Booleans and numeric strings stay distinct from integers | `Value::Bool` / `Value::Integer` / `Value::String` | Conforms. Tested at canonical_tests.rs:72–79. |
| Malformed UTF-8 and non-scalar Unicode refused | canonical.rs:65 (whole input), :175–189 (surrogate pairs only, `char::from_u32` rejects a lone low surrogate) | Conforms. Chunk boundaries fall only on ASCII `"` or `\`, so the check at :157 cannot fail on valid input. |
| Raw C0 controls in strings refused; closed escape set | canonical.rs:194–195, :166–191 | Conforms. |
| Duplicate keys compared after escape decoding | canonical.rs:246–249 | Conforms. No normalization, so NFC and NFD keys stay distinct (§3:123). |
| JSON whitespace only; trailing content refused; BOM refused | canonical.rs:81–85, :68–71 | Conforms. |
| Canonical form: keys in UTF-8 byte order, no whitespace | canonical.rs:337–349 (`BTreeMap<String,_>` orders by bytes) | Conforms. Equals canonical.py's `sort_keys` code-point order for valid strings. |
| Escapes: `\"` `\\` `\b\t\n\f\r`, lowercase `\u00xx`; `/`, U+007F and U+2028 unescaped (§3:124–125, 160–161) | canonical.rs:286–313 | Conforms. Same as `json.dumps(ensure_ascii=False)`. |
| Arrays keep admitted order (§3:125–130) | canonical.rs:327–336 | Conforms. |
| Shortest decimal integers | canonical.rs:320–324 | Conforms. |
| Encoded size ≤ 4 MiB (canonical.py:72–73) | canonical.rs:278–284 | Conforms. The subtraction cannot underflow because `bytes.len()` ≤ `MAX_BYTES`. |
| H preimage (§3:170) | digest.rs:26–42 | Conforms byte for byte. Domain charset equals canonical.py:77. |
| Raw blob hash has no descriptor cap (§3:118–119, 172–173) | digest.rs:13–15 | Conforms. |

Panic and denial-of-service reading:
- **No reachable panic:**
  - Slices at :112, :138 and :143 are guarded by `get` or by the dispatch that
    precedes them.
  - `hex4` cannot overflow u16 (:213).
  - The surrogate arithmetic cannot underflow (:185).
  - `hex` uses `expect` on an infallible write (digest.rs:20).
- **No quadratic path:** every scan is linear, and duplicate checks are O(log n).
- **Admission and encoding agree:** every escape the encoder emits is the same
  length as its only admissible input spelling, and whitespace is removed. So
  `encode(parse(x))` is never longer than `x` and cannot hit `ByteLimit` on a
  parsed value.
- The only resource question is memory amplification (ADV-05).

Typed API:
- `Integer` has a private field and a checked constructor.
- `Value::String` can only hold scalar text, and `Value::Object` cannot hold
  duplicate keys.
- So any programmatic `Value` is lexically valid apart from depth and size, and
  `encode` checks both.
- `Value` is an explicit, inert lexical representation (canonical.rs:28). Its
  documentation disclaims schema and Run admission, and it is not a schema
  carrier. The forward risk is ADV-02.

## 2. Pure-layer and build inputs (static)

- **Workspace:** the only member is `crates/identity` (Cargo.toml:3).
  `exclude = ["providers/rust"]` names a directory that does not exist yet.
  There is no identity `build.rs`, and no package.json or other Node input in the
  snapshot. `Cargo.lock` has 9 packages (8 registry + product). No provider
  package or edge.
- **`sha2 0.11.0`** (`default-features = false`, identity Cargo.toml:10;
  `build = false`): its SHA-256 compression dispatches at runtime. On x86 and
  aarch64 it depends on `cpufeatures` (sha2 Cargo.toml:79–80; sha256.rs:49–78).
  The output bytes do not depend on which path runs.
- **`cpufeatures 0.3.1`** (`build = false`): what it does depends on the target.
  - aarch64-apple: `check!("sha2")` is the compile-time constant `true`
    (aarch64.rs:118–120), so no `sysctlbyname` call is made for SHA-256.
  - Linux and Android on aarch64: calls `libc::getauxval(AT_HWCAP)`
    (aarch64.rs:35–38).
  - x86: uses the CPUID instruction.
  - The result is cached in a process-global static.
  - It has a target-conditioned `libc` edge on aarch64 apple/linux/android and
    loongarch64-linux (cpufeatures Cargo.toml:57–71).
- **`libc 0.2.189`** has a build script:
  - It runs `$RUSTC --version`, or `$RUSTC_WRAPPER $RUSTC --version`, on every
    build (build.rs:87, 242–261) and reads several environment variables.
  - It runs `freebsd-version` only under `LIBC_CI` (build.rs:121–122).
  - It does not use the network or a package manager.
  - The product tree's `target/debug/build/libc-aa833a1d99b7670b/output` shows it
    ran on this host.
- **`unsafe` coverage:** the dependencies use `unsafe` (intrinsics, FFI).
  `forbid(unsafe_code)` (lib.rs:7; Cargo.toml:12–13) covers only the product crate.
- **Assessment:** these are pure-effect libraries. There is no filesystem,
  network, clock or environment input to the digest function, and the only
  build-time effect is the compiler version query. No constraint in layout
  14:196–200 or build-plan 664–668 is broken. Build-plan 847–850 requires these
  edges to be recorded against the inventory's permitted graph. That tooling is
  the pending M1 inventory/tooling successor, so this is ADV-01, not a required
  finding.
- **Not confirmed by execution:** `cargo metadata` and `cargo tree`.

## 3. Design binding and verifier (static)

- **Governing sources pinned:** `design-lock.json` pins 46 inputs in sorted order,
  including all four governing sources for this unit (identity-and-evidence.md,
  admission-and-qualification.md, canonical.py, check-foundation.py).
- **Approval pins:** source45, application46, activation, the actual Claude
  application review, the root assent and the completion.
- **Chain fields present in the real documents:**
  - completion.json:3–19 and :393
  - review.json:3–4 and :18–19
  - assessment.json:10 and :49
  - application-subject.v46.json:3191–3194
- **Chain enforcement** (verify_design.py:53–98):
  - It enforces the application → source link, the activation → application and
    review links, review ACCEPT with empty must/should lists, root assent true and
    bound to the application and review, and completion approval, pass and all
    four links.
  - It overlays application rows on source rows, so a superseded source hash is
    not selected.
  - It requires inputs to be field-closed, sorted and unique, and to match the
    effective row and the on-disk bytes and length.
- **Path handling:** absolute paths, `.`, `..`, backslashes, redundant or trailing
  separators, a final symlink, and any resolved path leaving the root are all
  refused (:32–41). An in-root parent symlink is allowed, but its bytes are still
  digest-bound. I found no way to get an unselected or altered byte accepted.
  Looser spots are listed in ADV-08.
- **Standing:** the documents themselves say `implementationAuthorized: false`.
  Per the brief, the final completion guide supplies standing, and I don't
  revisit that.

## 4. Test oracles

Independent of the implementation:
- Canonical vectors 1–5 (canonical_tests.rs:10–28) equal the check-foundation.py
  UR-1..5 goldens (:45–49) byte for byte.
- Vectors 6–8 are literal readings of §3 text.
- The SHA-256 vectors (:215–229) are the standard FIPS 180 vectors for `""`,
  `"abc"` and 10^6 × `a`.
- The literal H frame (:258–261) independently pins the preimage layout.
- Depth and size boundaries use exact positive and negative cases.
- The corrected control-expansion boundary is arithmetically right:
  699050×6+2 = 4,194,302 ≤ 4,194,304, and 699051×6+2 = 4,194,308. The
  implementation already met §3. The pre-fix expectation was the error, and the
  capture records it as an initial failure rather than a pass.

Weaker points (ADV-07):
- The four H hex goldens (:233–250) are labelled "independent hashlib goldens",
  but no command or provenance is kept, they don't appear in the architecture,
  and I couldn't recompute them. H correctness still follows from the literal
  frame plus the standard SHA vectors.
- 21 malformed-input cases assert only `is_err()` (:145).
- Untested:
  - key ordering across 1/2/3/4-byte UTF-8 widths and prefixes
  - the full C0 escape table, and escapes inside keys
  - uppercase `\u` hex
  - duplicates via `\/`
  - frame lengths over 255
  - mixed array/object depth
  - `ByteLimit` taking precedence over `InvalidUtf8`
- The Python verifier tests cover only the activation cross-link
  (test_design_binding.py:63–69). The review, assent and completion refusal
  branches are untested.

## 5. Required findings

None identified by static reading. This is provisional and depends on the
execution items in §8.

## 6. Advisories

- **ADV-01: transitive effects not yet recorded against a permitted graph.**
  - The chain is sha2 → cpufeatures → libc. libc is target-conditioned and has a
    build script that runs `RUSTC`/`RUSTC_WRAPPER`.
  - Details are in §2.
  - Forward obligation (build-plan 847–850): the M1 inventory permitted graph
    records these edges and effects. Otherwise, a successor must pick a SHA-256
    implementation without the libc edge.
  - `sha2`'s `soft` backend cfg does not remove the dependency.
- **ADV-02: public H minting accepts any lexical `Value` and any
  syntactically valid domain.**
  - Where: digest.rs:26–46, `pub mod` at lib.rs:11–12.
  - Counterexample: `digest::identity("snapshot", &parse(br#"{"inventory":[{"path":"b"},{"path":"a"}]}"#)?)`
    returns an H for a descriptor that §3:148–152 `path` order admission would
    refuse. The result is an untyped `[u8;32]`, while §3:173–174 says a semantic
    reference must name its domain.
  - This is documented as the caller's duty (digest.rs:25) and fits this unit's
    scope.
  - Forward obligation (layout 14:350–352): descriptors.rs and digests.rs make
    registered-domain H consume admitted typed descriptors, and `Value` never
    becomes the carrier.
- **ADV-03: file names and API surface differ from the approved inventory.**
  - `digest.rs` vs the inventory's `digests.rs` (14:351).
  - `canonical_tests.rs` is not in the inventory.
  - lib.rs publishes whole modules, while 14:352 says internal modules stay
    private.
  - Covered by the already-required layout-successor refinement; not repeated as
    a finding.
- **ADV-04: refusal precedence differs from the reference; both refuse.**
  - `{"a":1,"a":1.5}`: this parser returns `DuplicateKey` (the key is checked
    before the value, :247). canonical.py gives a float refusal, because
    `json.loads` decodes values before the pairs hook runs.
  - 33 nested arrays around `1.0`: this parser returns `DepthLimit`; the
    reference gives a float refusal.
  - No D9 code mapping is claimed. A future mapping must pin precedence if codes
    become observable.
- **ADV-05: memory amplification is bounded but unmeasured.**
  - I estimate `Value` at 32 bytes (i128 alignment).
  - A 4 MiB `[0,0,…]` (≈2.1M elements) grows a `Vec<Value>` toward about
    64–128 MiB. Distinct-key objects are of similar order.
  - Everything stays linear.
  - A probe with a counting allocator is prepared. Host memory gates are future
    scope.
- **ADV-06: derived traits recurse without a bound on caller-built values.**
  - `Clone`, `PartialEq`, `Debug` and `Drop` on caller-built values nested deeper
    than 32 recurse without a limit (canonical.rs:29–37).
  - Parsed values are bounded, and `encode` stops at depth 33.
- **ADV-07: test oracle provenance and coverage gaps** (§4).
- **ADV-08: verifier looseness, all failing closed or digest-bound.**
  - Approval rows are not field-closed, and `bytes` is optional (:48, :57–59).
    Input rows are closed (:92–93).
  - `completion.remainingRequiredDesignFindings` (real completion.json:32) is not
    checked.
  - A non-object approval document raises `AttributeError`, which main's catch
    set (:108) doesn't cover. It still exits non-zero.
  - The verifier proves membership in the accepted subject, not that a selected
    input (for example a `*.proposed.*` row) is the current normative source.
    Which inputs are current belongs to plan review.
- **ADV-09: validation evidence is not bound to this snapshot.**
  - m1-canonical-validation-01 ran in the product working tree
    (validation.json `cwd`), not in the snapshot.
  - It started with a mutating `cargo fmt --all`.
  - It records no source digests.
  - It does not capture the unittest (7) or verifier (46) runs.
  - The failing initial run's output is not kept; only the pre-fix source is.
  - Running the snapshot's unittest without `-B` writes `__pycache__` into the
    snapshot's `tools/` (test_design_binding.py:11–13).
- **ADV-10: minor API gap.** `digest::Error` has no `Display` or
  `core::error::Error` impl, unlike `canonical::Error` (canonical.rs:52–58).

## 7. Future milestone scope (not graded)

Not graded in this unit:
- the generated schema carrier
- closed-schema and `x-opensip-order` admission, including the exact validator
  keyword set
- maxLength in scalars, logical paths and spans
- domain registry, prefixes and identifier syntax
- D9 refusal codes
- descriptors.rs, closure.rs and digests.rs
- semantic replay, provider, CLI and TypeScript integers
- memory and size qualification gates
- the dependency permitted-graph tooling
- release

## 8. Executed checks

None. Every Bash invocation, including a plain `shasum`, was denied. What was done
is static reading and search with Read, Grep and Glob, listed in
`review.json.executedChecks`.

Checks still owed (see `probes/RUN.md`):
1. Manifest SHA and per-row hash and length, plus the design-lock hash.
2. Snapshot `cargo test` (9), clippy `-D warnings`, `fmt --check`, unittest (7)
   and the design verifier (46).
3. `cargo metadata` and `cargo tree` for all targets.
4. A differential against the digest-checked `canonical.py` over a seeded corpus
   of about 20k inputs, plus independent hashlib recomputation of the four H
   goldens.
5. Rust edge, boundary and amplification probes.
6. 34 verifier probes, including the real 46-input architecture run.

## 9. Limitations

- Subject identity is unverified. I read files at the snapshot paths but could
  not hash them. I did not compare them with the product working tree.
- No test, lint, verifier or probe was executed. The claimed passes are
  unreproduced.
- Probe expectations come from static reading and may contain reviewer errors.
  They are not results.
- The dependency analysis read the local registry sources for sha2, cpufeatures
  and libc only; block-buffer, crypto-common, digest, hybrid-array, typenum and
  cfg-if were inferred from the lockfile. The platform and target analysis is
  limited to the cfg branches I read.
- I did not read the architecture beyond the named sections, the approval
  documents' chain fields, and the layout and build-plan passages cited.
  Historical archives were not read.
