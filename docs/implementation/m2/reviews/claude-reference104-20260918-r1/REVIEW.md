# Independent review: reference104 — explicit Ed25519 profile and root key validity — Claude, r1

Reviewer: Claude (independent; Codex remains implementation owner). Date: 2026-09-18.
Scope, as requested: my crypto59/62 findings A-1 (adopt the strict profile explicitly), C-1 (root key
validity) and T-1 (the profile must be pinned) **at the reference boundary**; my reference103 follow-ups F-1
(recovery reader) and F-2 (envelope qualification as a mechanism); independent adjudication of the point
decode / canonical rules, the doubling / small-order logic, the bounded cache, the equation and dependency
assumptions, exact OpenSSL agreement and differences, and **whether the Python profile agrees with the
proposed Rust profile (canonical key + pinned `dalek` `verify_strict`)**.

**Not covered and not approved:** product Rust changes, Q-1 (Rust quorum report typing), dependency and
per-target qualification (crypto59/62 D-1 stands), signing, custody, current trust, formal selection. N-4
remains open as declared.

## Bounded verdict

**No blocking finding in the profile, the root key rule, or the qualification mechanism. One required test
addition (T-104) before the profile is called pinned at the carrier.**

| Item | Adjudication |
|---|---|
| **A-1** explicit profile | **Closed.** `opensip.ed25519.canonical-cofactorless.1` is named in the contract with all six rules I asked for, including the two easy to get wrong: mixed-order keys are *accepted*, and cofactored / batch verification may not replace it. |
| **C-1** root key validity | **Closed.** Every `publicKey` in a root — referenced or not — must decode, be canonical and not be small-order. Both schemas. Pinned (2 mutants killed). |
| **Python ↔ Rust profile agreement** | **Agree on everything I could throw at them: 0 differences over 174,042 point encodings and 1,000 signatures**, including all 38 non-canonical `y` encodings, all torsion encodings, 280 mixed-order accepts over all seven torsion offsets, and 42 signatures with torsion in *both* A and R that cancels. |
| **T-1** profile pinned | **Pinned at the primitive, not at the carrier.** Replacing the profile call in `Verifier.verify` with raw OpenSSL passes the entire envelope checker and still writes a qualification receipt (T-104). |
| **103 F-1** recovery reader | **Closed and pinned** (mutant killed by the two new cases). |
| **103 F-2** envelope qualification as mechanism | **Closed.** All 15 missing / failed / stale / malformed receipts I made fail exactly one integration check. |

## Reviewed bytes (independently verified)

| Item | SHA-256 | Result |
|---|---|---|
| `trials/ed25519-profile-integration-checkpoint-104/subject.tar.xz` | `53584689a1a65dbae288b651938acd0993fe4bb3f37c17899e87e722de3a0982` | = `archive-pin.json` |
| `subject.json` (1,464 members) | `7bdca979dcdb24a29f6a006e7f200aa7d18db3606c46153dd8ef504df66223f5` | every member re-hashed from the tar **before** extraction |
| `frozen-candidate.json` (1,275 entries) | in manifest | all hash-match; 0 unlisted files |
| parent | — | `parent-inputs.json` **equals frozen reference103 exactly** (1,273 files) |

0 symlinks / non-regular members / unsafe paths; extraction re-verified byte-identical after all work; every
mutant ran in a temporary copy that was removed. **Change set vs 103:** 15 changed, 2 new
(`ed25519_profile_reference.py`, `ed25519-profile-cases.v1.json`), 0 removed.

## Owner checks, re-run in the required order (`claude-out/checks/`)

1. `check-signature-envelope.v1.py --output <fresh> --openssl …/openssl@3/bin/openssl` → exit 0: 160 explicit
   + 140 other + 1,803 recorded differential + 6,000 fuzz, 61 OpenSSL calls; `qualification-report.json`
   written, binding 1,262 source hashes, Python 3.12.13, UCD 15.0.0.
2. `check-integration.py --report … --envelope-report <fresh>/qualification-report.json` → **423 / 0**.
3. security **579 / 579**, 14 / 14 sweeps, pins valid; foundation 231; workflows 1,816; native 477 / 66.

All reproduce. Same-author checks; the adjudication rests on what follows.

## The profile module, read line by line

`_decode`: 32 bytes exactly; split sign bit and `y`; **refuse `y ≥ p`** (canonical); compute
`x² = (y²−1)/(dy²+1)`; candidate root by `(p+3)/8`, corrected by `√−1`; refuse if not a square; **refuse
`x = 0` with the sign bit set**; choose the root matching the sign. `_double`: the unified twisted-Edwards
addition with `a = −1` applied to `(P, P)` — complete on this curve because `d` is a non-square, so no
exceptional cases and no division by zero. `_admissible_bytes`: decode, double three times, refuse the
identity — i.e. refuse exactly the points of order dividing 8. `verify`: A admissible; message 32 bytes;
signature 64 bytes; **R admissible**; **`S < ℓ`**; then the retained OpenSSL primitive, accepted only when it
returns the literal `True`. Type guards are exact (`type(x) is bytes`): a `str`, a `bytearray` and a 31-byte
value are all refused.

I checked the subject's arithmetic against **my own independent group law** (written for my crypto59/62
review, not shared code): for 2,124 decodable encodings, `_double(P) == P + P` and "refused as small-order"
⇔ `8P = identity` — 0 mismatches. The cache is `lru_cache(maxsize=256)` keyed on immutable `bytes`: after
5,000 distinct inputs its size is 256. It caches a pure function of public bytes, so it cannot go stale and
holds nothing secret.

## Python profile vs the proposed Rust profile — independent differential (`claude-out/profile/`)

I built my own Rust harness against the **archive-verified, lock-pinned** `ed25519-dalek 3.0.0`
(`from_bytes` → `to_edwards().compress().to_bytes() == input` → `!is_weak()` → `verify_strict`) and compared
it with the subject's Python profile driving **actual OpenSSL 3.6.3**. All vectors come from my own
arithmetic, not from the subject's module and not from the retained 59.

**Point admission — 174,042 encodings, 0 differences** (89,736 admitted by both):
every `y` in `[0, 6000)` and `[p−3000, p)` with both sign bits; **every non-canonical `y` in `[p, 2²⁵⁵)` —
all 19 values × 2 signs**; all 8 torsion points in canonical, sign-flipped and (where representable)
`y + p` forms; 3,000 prime-order and 3,000 mixed-order points; 150,000 random strings.

**Signatures — 1,000 vectors, 0 differences:**

| Class | n | Python profile | Rust profile | raw OpenSSL |
|---|---:|---|---|---|
| honest | 120 | accept | accept | accept |
| `S + ℓ`; one-bit flips of R, S, A; wrong message | 200 | refuse | refuse | refuse |
| mixed-order A = aB + Tᵢ, **all seven i**, message with `ord(Tᵢ) ∣ k` | 280 | **accept** | **accept** | accept |
| mixed-order A, message with `ord(Tᵢ) ∤ k` (cofactored-only) | 280 | refuse | refuse | refuse |
| mixed-order R (cofactored-only) | 36 | refuse | refuse | refuse |
| **torsion in both A and R, chosen so `Tⱼ + k·Tᵢ = 0`** | 42 | **accept** | **accept** | accept |
| small-order A forgeries, all 8 torsion points and encodings | 26 | refuse | refuse | **ACCEPT** |
| small-order R with an honest key | 8 | refuse | refuse | refuse |
| **`R = identity`, `S = k·a` — made by the genuine key holder** | 8 | refuse | refuse | **ACCEPT** |

Two things follow. First, the agreement is exact on every class I could construct, including the awkward
one — a *mixed-order R* is admitted by both whenever the torsion cancels, so "non-small-order R" really is
the rule in both implementations, not "prime-order R". Second, **the profile differs from raw OpenSSL in two
classes, not one**: small-order A (known from 59/62) and **small-order R from a legitimate signer**. The
second is not a forgery — it needs the private scalar — but it is the class that matters for T-104.

This is differential evidence over constructed classes on aarch64 macOS. It is not a proof, and it says
nothing about other targets or backends (crypto59/62 D-1 stands).

## Root key admission (`cancel-and-roots.json`)

Through the subject's `admit_root_document`, both schemas, each key class placed either as `rootKeys[0]` or
as an **unreferenced extra entry in `keys`**: off-curve, identity, non-canonical identity (`y = p+1`),
order 2, order 4, order 8, `x = 0` with sign bit, `ff…ff` → **all refused**, in both positions and both
schemas, as `ROOT.RETAINED_SEMANTIC_POLICY` with the descriptive subject. Prime-order and **mixed-order** keys
→ accepted. Checking unreferenced keys is the right call: it removes the "two keyIds for one point" oddity
and means a dead key can never sit in the key table waiting to be referenced by a later edit. The placeholder
fixture keys had to change because they were never valid points; the key census, seeds and before-images are
retained, and the recorded signed corpus is untouched (1,803 differential, 0 unexplained).

## The qualification receipt (103 F-2) — tested, with its stated limit

`claude-out/receipts/`: I fed integration 15 bad receipts — `passed: false`, `passed: 1`, `passed: "true"`,
a stale model hash, a missing binding for the new profile module, an extra binding, UCD 16, wrong `kind`,
empty bindings, non-JSON, a JSON list, an empty file, no argument, a nonexistent path, a directory. **Every
one yields 422 passed and exactly the one expected failure**; the genuine receipt yields 423 / 0. The
comparison is exact equality of the whole binding map against hashes integration recomputes itself, so a
receipt cannot go stale silently. And in my mutation run, a mutant that made the envelope checker fail wrote
**no receipt**, while surviving mutants did — the "only on complete success" rule holds.

Limit, correctly stated by the owner: the receipt is self-asserted JSON, not authenticated. It makes the
routine run mechanical; it is not evidence that an honest run occurred. It also does not bind the OpenSSL
binary's identity or require non-zero case counts. Nonblocking.

## Finding

### T-104 (required before the profile is called pinned) — the carrier does not have to use the profile
Mutation run (`mutation.json`, `mutation-extra.json`; harness asserts pins valid and all 579 cases executed,
or no pin refusal, before trusting any result). **15 mutants: 9 killed, 6 survive.** Two survivors are one
real gap:

| Surviving mutant | Assessment |
|---|---|
| **`Verifier.verify` calls raw OpenSSL instead of the profile** | **Real gap.** The whole envelope checker passes and a qualification receipt is written. The 59 retained vectors and the 8 torsion checks call the profile module *directly*, so they pin the primitive but not its use. No carrier-level case can now reach the difference through a small-order **key** — root admission refuses such roots first — so the only reachable difference is **small-order R from a genuine signer**, and no case has one. I confirmed the difference is real (`identity-R.json`: 8 of 8 accepted by raw OpenSSL, refused by the profile and by Rust). |
| **R admission removed from `verify`** | Same gap, same fix. |
| `S < ℓ` check removed | Equivalent *given OpenSSL*, which refuses `S ≥ ℓ` itself. Keep the check: the profile must not depend on the backend for a rule it names. A vector with `S + ℓ` asserted at the profile level with a permissive stub callback would pin it. |
| callback truthiness instead of `is True` | Equivalent with the current callback. |
| `x = 0` sign-bit check removed | **Equivalent:** `x = 0` forces `y = ±1`, both small-order, so the next rule refuses them anyway. Harmless redundancy that matches the contract wording. |
| two doublings instead of three (security checker only) | Killed by the envelope checker; survives the security checker because the twelve new root negatives cover identity and order 4 but **no order-8 key**. Add one. |

Required: one signed carrier case per composed path (at least `verify` itself) whose signature has
`R = identity` from an authorized test key, expected `RJ-4 ENVELOPE_MISMATCH / no valid signature`; plus an
order-8 root key negative. With those, both real survivors die and the profile is pinned where it is used.
Killed, with named cases: root key admission removed; first-key-only; recovery reader not forwarded;
small-order test removed (both checkers); non-canonical `y` admitted; A admission removed in `verify`;
two-doublings (envelope).

## Remaining, outside this verdict
1. **Rust side.** The contract names the Rust profile precisely (canonical re-encoding via
   `to_edwards().compress()`, not `to_bytes()` — the exact trap I fell into in my 59/62 probe). The product
   Rust change itself is not in this subject and is not reviewed.
2. **Targets.** Everything ran on aarch64 macOS with serial curve arithmetic and ARM SHA-512; x86_64 runs
   different code (59/62 D-1). The contract's "every qualified target" sentence is the right requirement and
   is not yet met.
3. **OpenSSL is still the equation.** The reference depends on OpenSSL 3.6.3 being cofactorless with a
   canonical-R byte comparison. My vectors support that (cofactored-only signatures refused, 280 + 42
   cofactorless accepts); I did not read OpenSSL's source. A different OpenSSL build is a different backend.
4. Q-1, N-4, dependency acceptance, and the inherited pending implementation groups.

## Commands and outcomes (all under `claude-out/`)

| Command | Outcome |
|---|---|
| `verify_extract.py` (before extraction; after all work) | 1,464 / 1,464 verified from tar; 0 unsafe; unchanged |
| owner checkers, required order (`checks/`) | envelope pass + receipt; integration 423 / 0; security 579 / 14; foundation 231; workflows 1,816; native 477 / 66 |
| `receipts/` — 16 integration runs | genuine 423 / 0; 15 bad receipts each 422 + the one expected failure |
| `profile/rust` (offline, pinned `ed25519-dalek 3.0.0`) | reviewer harness for the Rust profile |
| `profile/differential.py` | 174,042 points, 950 signatures: 0 differences; doubling / small-order vs my own group law: 0 mismatches; cache bounded at 256 |
| `profile/cancel_and_roots.py` | 42 cancelling-torsion signatures: all three accept, 0 differences; 40 root-admission placements |
| `profile/identity_R.py` | 8 / 8: raw OpenSSL accepts, profile and Rust refuse |
| `mutation.py`, `mutation_extra.py` | 15 mutants, all valid: 9 killed, 6 survive (2 real, 1 coverage, 3 equivalent) |

No probe failed this round. Toolchain: Python 3.12.13 / UCD 15, OpenSSL 3.6.3, Rust 1.95.0.

## Limits
1. Reference only; all keys synthetic; nothing here is signing, custody or authority.
2. "0 differences" is over the classes I constructed; it is not a proof of equivalence.
3. One platform, one curve backend, one OpenSSL build.
4. I re-ran but did not review the foundation / workflows / native checkers.
5. I verified the pin inventories only through the checkers (`sourcePinsValid`, the receipt's 1,262
   bindings) and my harness; I did not re-derive the two rebinding rounds.
