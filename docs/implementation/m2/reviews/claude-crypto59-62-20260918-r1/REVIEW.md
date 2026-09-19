# Independent review: strict Ed25519 primitive59 and signature quorum62 — Claude, r1

Reviewer: Claude (independent; Codex remains implementation owner). Date: 2026-09-18.
Scope: the concrete verification profile of draft59 (`verify_metadata_signature` over `ed25519-dalek =3.0.0`)
against retained actual OpenSSL 3.6.3; key / message / signature binding and keyId construction; weak,
small-order, mixed-order and non-canonical encodings; draft62's `verify_quorum` (distinct signers, threshold,
role / namespace separation, quorum scope, where revocation is owned); and a bounded examination of the
actually compiled dependency closure.

**Not covered and not approved:** root / envelope / recovery / platform references (reviewed separately;
69/73 still changes-required), the Unicode64 bridge (reviewed separately — the Unicode15/16 mismatch that
draft62's README mentions is that already-resolved finding and is not re-reported here), current trust,
custody, installation, release, formal selection, and cumulative product acceptance. This verdict is
conditional on those inherited owners. All keys used are synthetic test-only keys with no authority.

## Bounded verdicts

| Subject | Verdict |
|---|---|
| **Primitive59** — strict verification profile | **No blocking finding in the verifier.** The profile is exactly what the README claims and is strictly safer than OpenSSL on the one class where they differ. **The stricter profile should be adopted explicitly** (adjudication A-1). Two follow-ups are required before the profile can be called complete: C-1 (key validity at root admission) and D-1 (target-dependent code paths are untested). |
| **Quorum62** — `verify_quorum` | **No blocking finding in the counting logic.** Distinct-key counting, role / namespace separation, threshold and scope all behaved correctly under adversarial probing. One API-shape finding must be resolved before any consumer exists: Q-1 (`state: Met` is computed before revocation). |
| **Dependency closure** | **Bounded review only; not a dependency acceptance.** Archive integrity and the compiled closure are established; source review of the transitive crates is *not* done (list of what remains in "Dependency review"). |

## Reviewed bytes (independently verified)

| Item | SHA-256 | Result |
|---|---|---|
| `trials/signature-draft-checkpoint-59/subject.tar.xz` (11,247,840 B) | `e40a27504a61ead775356f65c585e341b490a6f91f7d1d054d4d425c4b8be4a1` | = pin; 393 members re-hashed from the tar before extraction |
| 59 `subject.json` / `README.md` / `archive-pin.json` | `f293e638…56c872` / `fe03ef80…a3448e` / `35fb735e…98e77b` | |
| `trials/signature-quorum-draft-checkpoint-62/subject.tar.xz` (3,161,448 B) | `cb71a44c87246bd3c38dc8d9a8dd16ebe3b499591bdde934110541de5506d613` | = pin; 338 members re-hashed before extraction |
| 62 `subject.json` / `README.md` / `archive-pin.json` | `17ae5d00…241df6` / `ae69ed36…54b2c9` / `96773843…69491a` | |
| 62 `crates/security/src/trust.rs` (the reviewed source) | `68c96784e18aea00cdaf…` | scratch copy hash-equal to the subject **before** I appended probes |

0 symlinks / non-regular members / unsafe paths. Both extractions re-verified byte-identical after all
work. Every build ran in a scratch copy (`claude-out/build62`) with its own target directory; the subjects
were never built in place. `Cargo.lock` is byte-identical between 59 and 62.

**Dependency archives.** All **40** registry packages in `Cargo.lock` have a retained `.crate` in 59's
`archives/`, and **all 40 SHA-256 values equal the `Cargo.lock` checksums** (`archive-verification.json`);
no archive is unlisted. I extracted exactly those bytes into a vendor directory (refusing any non-regular or
escaping tar member) and built with `--offline --locked` against it, so the code I ran is the pinned code.

## What the verifier actually is (read from the pinned source, not the docs)

`verify_metadata_signature(pk: &[u8;32], msg: &[u8;32], sig: &[u8;64])`:
1. `VerifyingKey::from_bytes` → `CompressedEdwardsY::decompress`. **ZIP-215-style decoding**: it refuses
   only byte strings that are not curve points. It does *not* refuse non-canonical `y ≥ p`, the `x = 0`
   sign-bit variants, or small-order points. (`ed25519-dalek-3.0.0/src/verifying.rs` l.175-183.)
2. `verify_strict` (l.367-391): `InternalSignature::try_from` → `check_scalar` =
   `Scalar::from_canonical_bytes` (the non-`legacy_compatibility` branch, which is the one compiled: no
   features are enabled) → **S must be < ℓ**; decompress R (refuse if not a point); **refuse if R or A is
   small-order**; recompute `R' = [S]B − [k]A` with `k = SHA-512(R ‖ A_bytes ‖ M)` and compare the
   **compressed bytes** `R' == R`. That is the **cofactorless** equation, and the byte comparison means a
   non-canonical R can never verify.
3. On success the wrapper returns `VerifiedSignature { key_id: SHA-256(pk bytes), message }` — an inert
   private struct; no role, threshold or authority.

No batch, prehash, context, hazmat, legacy or signing API is reachable: the crate is built with **no
features** (`cargo tree`: `ed25519-dalek v3.0.0 []`, `curve25519-dalek v5.0.0 [digest]`), and
`opensip-security` itself is `unsafe_code = "forbid"`.

## Independent adversarial evidence (`claude-out/probes/`)

I wrote a pure-Python Ed25519 reference (RFC 8032 arithmetic; validated by the fact that OpenSSL accepts its
honest signatures and my cofactor predictions below come out exactly), generated 59 vectors, recorded the
**actual OpenSSL 3.6.3** verdict for each, and ran each through the subject's `verify_metadata_signature`
and — to separate "strict" from "decoding" — through the same crate's non-strict `verify`.

| Class | n | OpenSSL | Rust strict (subject) | dalek non-strict |
|---|---:|---|---|---|
| honest signatures | 4 | accept | accept | accept |
| binding: other key / other message / R spliced from another signature | 3 | reject | refuse | refuse |
| non-canonical S (`S+ℓ`, `S+2ℓ`, `S=ℓ`) | 3 | reject | refuse | refuse |
| non-canonical R encoding | 1 | reject | refuse | refuse |
| small-order R with an honest key | 3 | reject | refuse | refuse |
| public key not a curve point | 3 | reject | refuse `PublicKey` | undecodable |
| **small-order public key, forged without any private key** (all 8 torsion points; canonical, `y+p` and `x=0`-sign-bit encodings; two messages each where `ord(A) ∣ k`) | **28** | **ACCEPT** | **refuse** | accept |
| small-order key with `R = identity, S = 0` where the equation does not hold | 6 | reject | refuse | refuse |
| **mixed-order key `A = aB + T₈`, messages with `8 ∣ k`** | 3 | accept | **accept** | accept |
| mixed-order key, messages with `8 ∤ k` (valid only under the *cofactored* equation) | 3 | reject | refuse | refuse |
| mixed-order R (cofactored-valid only) | 1 | reject | refuse | refuse |

**So, over my vectors, the subject differs from OpenSSL on exactly one class — small-order public keys — and
always in the refusing direction.** The README's single identity-key example understates it: OpenSSL accepts
forgeries under *every one of the eight* torsion points and under their non-canonical encodings, for any
message whose challenge is a multiple of the point's order (one message in eight for an order-8 key; I found
two per key within a few dozen tries). No private key is involved.

Backend parity: I re-ran all 14 crate tests plus both my probes with
`--cfg sha2_backend="soft" --cfg curve25519_dalek_backend="serial"`; results are **byte-identical** to the
default build, which on this host uses ARMv8.2 SHA-512 intrinsics (see D-1).

## Adjudication A-1 — adopt the stricter profile explicitly

The request asks for explicit adjudication of "identity-key forgery accepted by OpenSSL and refused by
Rust". My adjudication: **the Rust behaviour is the correct profile and the retained OpenSSL verifier is the
one that is deficient for this use**, for a reason specific to this design:

- Root admission accepts small-order public keys (C-1 below). With the OpenSSL verifier, anyone can then
  produce a "valid" signature for that key over roughly one message in eight, with no secret. A threshold
  of 2-of-3 with one such key in the set is a 1-of-2 threshold for an attacker who can grind the signed
  subject (the envelope subject includes caller-chosen fields such as `namespace`).
- The reference verifiers I reviewed in envelope66 / reference102 use exactly that OpenSSL primitive. My
  102 negative control already showed signature validity has a single gate; this review shows what that gate
  lets through. **The 102 reference is therefore only as strict as OpenSSL**, and the reference/product
  difference is a real semantic difference, not a test artefact.

What must be written down, because it is not derivable from "RFC 8032" or "ZIP-215":
1. S canonical (`S < ℓ`); 2. R must decode and must not be small-order; 3. A must decode and must not be
small-order; 4. the **cofactorless** equation, compared on canonical R bytes; 5. `k` hashes the public-key
**bytes as presented**; 6. mixed-order (non-small-order, non-prime-order) keys **are accepted** — a holder of
such a key can produce signatures that this verifier accepts and a cofactored verifier (ZIP-215, batch
verification) would also accept, *and* signatures only a cofactored verifier accepts. That is harmless while
every verifier in the system is this one; it becomes a consensus hazard the day a second implementation
(batch, another language, a hardware verifier) is added. The contract should name this profile and forbid
mixing verifier equations. None of this is RFC/NIST equivalence, as the README correctly says.

## Findings

### C-1 (medium; owner: root admission, not this primitive) — root admission accepts keys that can never verify
Using the subject's own `admit` on fixture root "2" with `rootKeys[0]` replaced (`quorum-results.json`):

| `publicKey` | root admission |
|---|---|
| not a curve point (`y = 2`) | **ADMITTED** |
| an order-8 torsion point | **ADMITTED** |
| non-canonical identity encoding (`y = p + 1`) | **ADMITTED** |
| `ff…ff` (non-canonical, non-weak, decodable) | **ADMITTED** |

The strict verifier makes all of these useless for forgery — this is *not* a bypass under draft59. But the
retained root policy `keys ≥ threshold + 1` is a redundancy rule about **usable** keys, and it is satisfied
by dead ones: a root `[good, dead, dead]` at threshold 2 is admitted, can never reach its own threshold, and
therefore can never sign its successor — a self-bricking root passes admission. And under the OpenSSL
reference the same root is forgeable (A-1). The byte-wise "unique public keys" rule also treats the
canonical and non-canonical encodings of one point as two distinct keys with two keyIds. (For non-small-order
points this is theoretical: non-canonical encodings exist only for `y < 19`, and nobody knows a discrete log
there.) **Required:** at root admission, every `publicKey` must decode, must re-encode to the same 32 bytes
(canonical), and must not be small-order — in both the Python model and the Rust `admit`, with retained
negatives. One rule closes the OpenSSL forgery, the dead-key redundancy hole and the two-keyIds-one-point
oddity together. The existing test `weak_key_forgery_cannot_complete_an_authorized_quorum` currently
*depends* on the weak key being admitted; it should become "root with a weak key is refused".

### Q-1 (medium) — `QuorumReport.state` is decided before revocation
`verify_quorum` has no revoked-key input; `state: Met` and `valid` are computed over all authorized keys.
The README is candid that revocation is owned elsewhere, and the Python owners do subtract revoked keys
before comparing to the threshold. But the report hands a consumer a ready-made `Met`, and the correct
consumer behaviour (discard `state`, subtract revoked from `valid`, re-compare with `required`) is nowhere
enforced by the type. With no consumer yet written, this is the cheap moment to fix it: either take the
revoked set as a parameter, or drop `state` from the report and expose only
`valid_before_revocation` + `required`, so "met" can only be computed by the layer that owns revocation.

### Q-2 (low) — quorum scope is sound; two small observations
Confirmed by probe: 16 copies of one valid record → `valid = 1`, `BelowThreshold`; 17 records → `Limit`;
root signatures presented as RECOVERY or TR-CORE → `NoValidSignatures`; one flipped message bit → none
valid; key-1's signature under key-0's keyId is not counted; namespace with a final LF or an uppercase letter
→ `Namespace` (the hand-written byte check has no `$`-newline weakness, unlike the Python models — see my
69/73 S-1); a mixed-order key counts as one signer like any other. Observations: (a) `o["rootKeys"]`-style
indexing panics rather than refusing if `ValidatedRootPayload` ever stops guaranteeing the member — safe
today by type-state, but a panic is not a refusal; (b) the defensive
`verified.key_id != signature.key_id → InternalShape` aborts the whole report on what would be a root-admission
invariant failure; correct, just note it is an error, not a skipped signature.

### D-1 (medium) — the code that runs on x86_64 is not the code that was tested
From the pinned sources and `cargo tree --target`:
- **curve25519-dalek**: its `build.rs` selects `serial` on aarch64 (confirmed in my build output:
  `curve25519_dalek_bits="64"`, `backend="serial"`) but **`simd` by default on x86_64**, which adds the AVX2
  backend (runtime-detected via `cpufeatures`), the `curve25519-dalek-derive` **proc-macro**, and with it
  `syn`, `quote`, `proc-macro2`, `unicode-ident` — five more crates and build-time code execution that the
  Mac closure does not contain.
- **sha2 0.11**: SHA-512 dispatches at runtime to `aarch64_sha3` intrinsics on this Mac and to `x86_avx2`
  on x86_64; the portable `soft` backend is what runs elsewhere.
So every retained result (Codex's and mine) exercises *serial curve + ARM hardware SHA-512*. Linux x86_64 —
the other release target — will execute AVX2 field arithmetic and AVX2 SHA-512 that no test here has run.
I showed the portable configuration agrees on this host; I could not run the AVX2 paths. **Options for the
owner:** pin `--cfg curve25519_dalek_backend="serial"` and `--cfg sha2_backend="soft"` in the workspace
`.cargo/config.toml` (one tested code path everywhere; verification is not throughput-critical here, and it
removes the proc-macro chain from the x86_64 closure's *use*), or keep the defaults and make the
adversarial vectors a required test on every release target. Either way the vectors in
`claude-out/probes/vectors.json` are portable.

### T-1 (medium) — the retained crate tests do not pin the strict profile beyond the identity key
`signature-cases.ndjson` (4 valid + 1,024 bit-flips) agrees with OpenSSL by construction, so it cannot
distinguish `verify_strict` from `verify`: replacing `verify_strict` with `verify` in the wrapper would still
pass all 1,028. The only test that distinguishes them is the single identity-key case. None of: the other
seven torsion points, non-canonical encodings, `S ≥ ℓ`, small-order R, mixed-order keys, or the
cofactored-only signatures is retained. (I did not run this as a mutation; it follows from the table above,
where "dalek non-strict" differs from "Rust strict" only on the small-order rows.) Add the 59 vectors, or an
owner-generated equivalent, with explicit expectations — including the three mixed-order *accepts*, so that
a future move to a cofactored or batch verifier is a visible, deliberate change.

## Dependency review — what was done, and what remains

Done (`dep-scan.json`, `cargo-tree-host.txt`):
- integrity of all 40 archives against `Cargo.lock`; offline locked build from those bytes;
- the **host-compiled crypto closure is 16 crates**: ed25519-dalek, curve25519-dalek, ed25519, signature,
  sha2, digest, block-buffer, crypto-common, hybrid-array, typenum, subtle, cpufeatures, cfg-if, libc, plus
  build-only rustc_version and semver. `fiat-crypto`, `getrandom` and `r-efi` are in `Cargo.lock` but are
  **not compiled** for the host or for x86_64-linux (no `rand_core`/`fiat` configuration is enabled);
- build-time execution in that closure: `curve25519-dalek/build.rs` (**read in full**: it only reads
  `CARGO_CFG_*` / rustc version and prints `cargo:rustc-cfg` lines — no network, no file writes, no native
  compilation) and `libc/build.rs` (not read);
- no `extern "C"` / `#[link]` / `asm!` in the dalek crates; FFI is confined to `libc` (used by `cpufeatures`
  for `sysctlbyname` on Apple). `sha2` contains 11 `asm!` sites and `cpufeatures` 1 — all in
  non-host backends (loongarch / riscv / x86 cpuid) by file, not verified by expansion;
- `unsafe` token counts (comments stripped): ed25519-dalek **0** (`forbid`), ed25519 0, signature 0,
  digest 0, crypto-common 0, typenum 0; curve25519-dalek 33 (15 in the AVX2 `packed_simd.rs`, not compiled
  here); sha2 50 (hardware backends); hybrid-array 37; block-buffer 21; cpufeatures 11; subtle 2; semver 47
  (build-only); libc 668.

**Not done — remains for a dependency acceptance:**
1. No line-by-line review of `curve25519-dalek` field / scalar / Edwards arithmetic, `sha2` compression
   functions, or the `unsafe` in `hybrid-array` and `block-buffer` (both sit under every hash call).
2. `libc/build.rs` and the 387-file `libc` crate: not reviewed (only `sysctlbyname` is reached on Apple).
3. The x86_64-only chain (`curve25519-dalek-derive`, `syn`, `quote`, `proc-macro2`, `unicode-ident`) and the
   AVX2 code: not reviewed and not executed.
4. I did not compare the archives against upstream repositories or tags; integrity is relative to
   `Cargo.lock`, i.e. to crates.io as fetched by the owner. These version numbers (ed25519-dalek 3.0.0,
   curve25519-dalek 5.0.0, sha2 0.11) are newer than anything I have independent knowledge of, so I relied
   only on the bytes in the archive, not on recollection of upstream behaviour.
5. No timing / side-channel assessment. Verification handles only public data, so this matters little here,
   but it is not assessed.
6. No licence review.

## Commands and outcomes (all under `claude-out/`)

| Command | Outcome |
|---|---|
| `verify_extract.py` (before extraction; after all work) | 393 + 338 members verified from tar; 0 unsafe; extractions unchanged |
| `vendor_setup.py` **r1** | **Failed — reviewer bug**: my filename regex mis-split three `+spec` versions and reported them missing. Preserved (`vendor_setup.failed-r1.py`, note). r2: 40/40 verified |
| `cargo test -p opensip-security --offline --locked` (scratch copy, vendored bytes) | 14 passed, 0 failed |
| `cargo tree` host + three `--target`s | closures recorded; x86_64 adds the proc-macro chain |
| `probes/gen_vectors.py` | 59 vectors with actual OpenSSL verdicts |
| reviewer test `claude_vectors` (appended to the **scratch** `trust.rs` only) | ran the subject's private verifier over all 59; table above |
| reviewer test `claude_quorum_probe` (scratch only) | 15 quorum / admission cases |
| full tests + both probes with `sha2_backend="soft"`, `curve25519_dalek_backend="serial"` | 16 passed; probe outputs byte-identical to the default build |
| dependency scan **r1** (inline shell) | **Invalid — reviewer bug**: zsh expanded an unquoted `--include=*.rs`, so every unsafe/asm/FFI count printed 0. Preserved as a note; replaced by `probes/dep_scan.py` |
| a vacuous check, kept visible | my Rust probe's `canonicalKeyEncoding` column is always `true` because `VerifyingKey::to_bytes()` returns the bytes it was given; canonicity in this review was decided in Python instead |

Toolchain: Rust 1.95.0 (`/opt/homebrew/Cellar/rust/1.95.0/bin`), OpenSSL 3.6.3, Python 3.12.13.

## Limits and unresolved assumptions
1. Tested on aarch64-apple-darwin only. No x86_64, no Linux, no AVX2 path (D-1).
2. 59 adversarial vectors plus the owner's 1,028 and 1,492 are evidence about classes, not a proof over the
   signature space; my Python reference is itself unreviewed, though OpenSSL's agreement on the honest and
   cofactor cases constrains it well.
3. "Differs from OpenSSL only on small-order keys" is an empirical statement over these classes. I did not
   read OpenSSL's Ed25519 source.
4. Dependency source review is bounded as listed; this is not a dependency acceptance.
5. Revocation, time, root chain, envelope and custody are other owners; Q-1 is about the interface to them.
6. Conditional on the inherited root / Unicode / current-trust owners; 69/73 remain changes-required; no
   cumulative product acceptance or formal selection is implied.
