# Independent review: private Rust draft105 — canonical Ed25519 key gate and revocation evidence typing — Claude, r1

Reviewer: Claude (independent; Codex remains implementation owner). Date: 2026-09-18.
Scope, as requested: closure of my crypto59/62 findings **A-1** (strict profile), **C-1** (root key
validity), **Q-1** (no pre-revocation `Met`) and **T-1** (profile pinned by tests) in the private Rust draft;
the API / profile boundary; the two changed fixtures; meaningful regressions; and any effect of my
reference104 findings.

**Not covered and not approved:** everything else in the 4,717-line `trust.rs` and the rest of the
workspace (inherited, pending), dependency acceptance, Linux / musl / x86-AVX target qualification
(59/62 **D-1 stands** — this is one aarch64 macOS lane), current trust, custody, installation, cumulative M2
acceptance, formal selection. Conditional on proposed reference104, which is itself unselected.

## Bounded verdict

**No blocking finding. A-1, C-1, Q-1 and T-1 are closed in this draft, and every correction is pinned: 12 of
12 of my mutants are killed by named tests.** Two nonblocking notes (N-1, N-2).

| Finding | Adjudication |
|---|---|
| **A-1** strict profile | **Closed.** One shared gate `admitted_public_key` (decode → not weak → `to_edwards().compress().to_bytes() == input`) feeds `verify_strict`. It agrees with the 104 Python profile on **175,000 inputs with 0 differences** when run through the subject's own functions. |
| **C-1** root key validity | **Closed.** `admit` runs the same gate over **every** entry of `keys`; failure is the existing internal `RetainedPolicy` error; a weak key can no longer enter a `ValidatedRootPayload`. |
| **Q-1** pre-revocation `Met` | **Closed by construction.** `verify_quorum` returns `SignatureEvidence`, which has no state. `QuorumReport` is built at exactly one site, inside `filter_revoked`, which **consumes** the evidence. All five production consumers read `.state` from a filtered report. |
| **T-1** strict profile pinned | **Closed.** `verify_strict → verify` is killed — by the new identity-R vector, the one class that still separates the two once weak keys are excluded. |
| **104 T-104** (profile bypassable at the carrier) | **Does not apply to this draft.** The Rust carrier calls `verify_metadata_signature` directly and there is no alternate primitive; the corresponding mutant is killed. |

## Reviewed bytes (independently verified)

| Item | SHA-256 | Result |
|---|---|---|
| `trials/crypto-profile-draft-checkpoint-105/subject.tar.xz` | `0ff50685aa59a53bd0a93681edfd59a0d05742ed6bd785d344c8dfd0490b18dd` | = `archive-pin.json` |
| `subject.json` (417 members) | `97686843208c415bc2cc0f877bdee9dd4bfa7e4483ddb5d1a8b8669b951a0857` | every member re-hashed from the tar **before** extraction |
| `product-inputs.json` | — | all **330** product pins match; 0 unlisted product files |
| parent100 (`parent-inputs.json`, manifest `63e1be99…16be08`) | — | exact-path comparison: **3 files changed, 0 added, 0 removed** — `trust.rs` and the two fixtures, as claimed |
| `trust-before-profile105.rs` | `8bdea533ce97bc60…` | equals the parent's pinned `trust.rs` |

0 symlinks / non-regular members / unsafe paths; extraction re-verified byte-identical after all work; every
build and mutant ran in a scratch copy. (Reviewer artefact, corrected: my first parent comparison split paths
on `product/` and mis-keyed the fixture `…/fixtures/product/design-lock.json`, briefly showing two phantom
changes; the exact-path comparison is the one reported.)

**Dependencies.** The lock has 51 registry packages. 40 are the archives I verified in the 59/62 review. The
other 11 (`rusqlite`, `libsqlite3-sys`, `cc`, `pkg-config`, `vcpkg`, `bitflags`, `smallvec`, `shlex`,
`find-msvc-tools`, `fallible-iterator`, `fallible-streaming-iterator`) are **not retained in this subject**;
I took them from the local Cargo cache and used each only after its SHA-256 equalled the `Cargo.lock`
checksum (`vendor-provenance.json`). That establishes lock integrity, not provenance, and none of them was
reviewed. Builds were `--offline --locked`.

**Owner tests reproduced:** 58 passed on the default backends and 58 passed with
`--cfg sha2_backend="soft" --cfg curve25519_dalek_backend="serial"`.

## The key gate and the primitive

```
admitted_public_key(pk):  from_bytes(pk)?  →  refuse if is_weak()
                          →  refuse if to_edwards().compress().to_bytes() != pk
verify_metadata_signature: admitted_public_key(pk)?  →  verify_strict(msg, sig)
```
The re-encoding comparison is the correct test and the comment says why: `VerifyingKey::to_bytes()` returns
the bytes it was given, so it can never detect a non-canonical encoding. (I made exactly that mistake in my
59/62 probe and reported it there; the mutant that swaps in `to_bytes()` is killed here.) Order is right:
decode, then weakness, then canonicity, all before any hashing; both failures are `SignatureError::PublicKey`,
so the identity-key test now reports `PublicKey` rather than `Invalid` — a correct and more precise change.

**Through the subject's own functions** (a test module appended to the *scratch* `trust.rs`, reading my 104
corpora): 174,042 point encodings, 950 signatures and 8 identity-R signatures — **0 differences** from my
independent Rust-profile harness and therefore from the 104 Python profile driving real OpenSSL. Accepted:
89,736 keys; 400 signatures (120 honest + 280 mixed-order with `ord(T) | k`, all seven torsion offsets);
**0 of 8 identity-R**. Mixed-order, non-small-order keys are admitted, as the named profile specifies.

## Q-1: the type separation, checked at every consumer

`SignatureEvidence { root_digest, message, role, namespace, valid_before_revocation, required }` — no state.
`QuorumReport { …, valid, required, state }` — one construction site (`trust.rs` l.2559, inside
`filter_revoked(mut SignatureEvidence, &revoked) -> QuorumReport`, which moves its argument).
`EnvelopeEvidence<Q = SignatureEvidence>` is generic over the evidence; `filter_envelope_revoked` rebuilds it
as `EnvelopeEvidence<QuorumReport>`, and the three proposal structs (recovery l.2970, profile l.3574,
revocation l.4335) and the chain link (l.2523-2524) can only hold the filtered form.

Production reads of quorum state — all on a `QuorumReport`:

| Consumer | Line | Revoked set |
|---|---|---|
| root chain — continuity (old root) | 2668 | `context.revoked` |
| root chain — possession (new root) | 2687 | `context.revoked` |
| recovery epoch (`required ≥ 3` and `Met`) | 3191 | `input.revoked` |
| platform profile set | 3790 | `revoked` |
| revocation list | 4410 | `previously_revoked_keys` |

`raw_quorum_state` exists only under `#[cfg(test)]`. The one production read of `valid_before_revocation`
(l.2259, "no valid signature at all") is a pre-revocation *negative*, which is safe: a set consisting only
of revoked signers passes it and is then reported `NoValidSignatures` by the filtered state. All these types
are module-private, so nothing outside `root_payload` can fabricate a report.

The revocation-list consumer filtering by *previously* revoked keys is the right rule and worth noting: a new
list cannot be authorised by keys an earlier list revoked.

## Mutation evidence (`claude-out/probes/mutation.json`)

Each mutant built and run against the crate's own tests in a scratch tree; all 12 applied and compiled.

| Mutant | Killed by |
|---|---|
| canonical re-encoding check removed | `complete_root_payload_matches_corrected_reference` |
| `to_bytes()` accessor instead of re-encoding | same |
| weak-key check removed | `root_with_weak_key_is_refused_before_quorum`, `strict_profile_refuses_identity_key_forgery`, root corpus |
| root-admission key loop removed | `root_with_weak_key_is_refused_before_quorum`, root corpus |
| `verify_strict` → `verify` | `actual_ed25519_matches_explicit_profile_vectors_and_tampering` |
| `filter_revoked` stops removing keys | `quorum_state_is_created_only_after_revocation_filtering` + 3 signed-path tests |
| chain continuity ignores revocation | `real_signature_chain_matches_reference_and_owns_exact_evidence` |
| chain possession ignores revocation | same |
| recovery ignores revocation | `actual_signed_recovery_matches_corrected_reference_without_persisting` |
| profile ignores revocation | `signed_profile_is_bound_to_supplied_core_pin_role_and_nonrevoked_quorum` |
| revocation list ignores prior revocation | `signed_revocation_evidence_requires_current_supplied_root_quorum_and_owns_bytes` |
| recovery accepts below threshold | `actual_signed_recovery_…` |

**12 of 12 killed.** That is the strongest result in this review series, and it matters most for Q-1: every
one of the five consumers individually loses a test if it stops honouring revocation.

## The two changed fixtures (`claude-out/probes/fixtures.json`)

**`signature-cases.ndjson`, 1,028 → 1,088.** The first 1,028 rows are byte-identical to the before-image.
Of the 60 added rows, **59 are byte-equal to my 59/62 vectors**; the 60th is the owner's
`profile105:valid-cofactorless-equation-with-small-order-R`. I verified that supplement independently: its
public key is admissible, **raw OpenSSL accepts the signature**, and the 104 profile refuses it — so it is a
genuine equation with `R = identity` that only the key holder could have made, and it is exactly the vector
that distinguishes strict from non-strict verification after weak keys are excluded. I re-derived **every
one of the 1,088 expectations** with the 104 Python profile over real OpenSSL: 0 disagreements; 11 positives
(4 historical + 4 honest + 3 mixed-order), matching the test's `assert_eq!(positives, 11)`. Among the added
rows raw OpenSSL would accept 29 that the profile refuses.

**`root-payload-cases.ndjson`, 7,515 → 7,527 cases, 17,674 pooled nodes.** I decoded the pooled format for
both the new file and the retained before-image and compared them case by case:
- labels and order of the 7,515 historical cases preserved; reader sets unchanged in all of them;
- **acceptance changes: 0** (227 accepted before and after);
- the only leaf differences between old and new roots are 64-hex strings — **22 distinct substitutions,
  consistent everywhere (0 conflicting mappings), injective**, and every new value is either an admissible
  public key or the SHA-256 keyId of one (0 "neither"); no non-hex leaf changed anywhere;
- I ran **all 7,527 roots through the 104 Python model** with each case's reader set: **0 disagreements**
  with the recorded expectation and 0 exceptions;
- the 12 appended cases are the 104 bad-key negatives for both schemas, all `accepted: false`.
So no regression is masked by the migration: nothing that was refused became accepted or vice versa, and the
substitution is a clean relabelling. (Two of the replaced placeholder keys happened to be admissible already;
replacing them as well is harmless and keeps the mapping uniform.)

## Nonblocking notes

### N-1 — the root corpus has no order-8 key and no unreferenced-key case
Same observation as reference104: the twelve key negatives cover off-curve, identity, order 4,
non-canonical identity, `x = 0` sign bit and `ff…ff`. An order-8 key is covered at the signature layer (my
torsion vectors) and the weak-key mutant is killed, so this is coverage symmetry, not a gap in behaviour. A
case with a bad key present in `keys` but referenced by no role would pin the "every key, not just used
keys" rule, which today is pinned only indirectly.

### N-2 — canonical-key mutants are killed only through the 4 MB root corpus
Both canonicity mutants die in `complete_root_payload_matches_corrected_reference` and nowhere else: there is
no direct unit test of `admitted_public_key` with a non-canonical, non-weak encoding (`ff…ff` decodes to a
point of large order with `y = 18 + p`). A three-line direct test would make the failure legible.

## Remaining, outside this verdict
1. **Targets (59/62 D-1).** Unchanged: x86_64 selects the AVX2 curve backend and AVX2 SHA-512 and pulls in
   the proc-macro chain. The README's requirement that the adversarial vectors run on every qualified target
   is right and unmet. I re-confirmed portable-backend parity on this host only.
2. **Dependencies.** 51 packages, none source-reviewed by me; 11 of them not even retained in this subject.
3. **The rest of `trust.rs`.** Root chain, recovery, profile and revocation consumers were read only where
   they touch quorum state; their own rules (time, counters, pins, persistence) are inherited and pending.
4. Reference104 is unselected; this draft is conditional on it and on its T-104 successor (reference107).

## Commands and outcomes (all under `claude-out/`)

| Command | Outcome |
|---|---|
| `verify_extract.py` (before extraction; after all work) | 417 / 417 verified from tar; 0 unsafe; unchanged |
| product pin check / parent comparison | 330 / 330; exactly 3 files changed vs parent100 |
| vendor extension | 40 from verified 59 archives + 11 from local cache, each equal to its lock checksum |
| `cargo test -p opensip-security --offline --locked` | 58 passed (default); 58 passed (soft SHA-512 + serial curve) |
| first build attempt | **Failed — reviewer setup**: my 59/62 vendor directory lacked the 11 SQLite-related crates (`no matching package named rusqlite`). Resolved as above; recorded here rather than hidden. |
| `probes/fixtures.py` | 1,088 signature expectations and 7,527 root expectations re-derived: 0 disagreements; migration is a consistent injective relabelling |
| reviewer test `claude105_corpora` (scratch `trust.rs` only) | 175,000 inputs through the subject's functions: 0 differences |
| `probes/mutation.py` | 12 mutants, all compiled: **12 killed** |

Toolchain: Rust 1.95.0, OpenSSL 3.6.3, Python 3.12.13 / UCD 15; aarch64 macOS.

## Limits
1. One platform, two backend configurations on it. No Linux, no musl, no x86.
2. All keys and signatures are synthetic test-only material.
3. "0 differences" is over constructed classes, not a proof of equivalence.
4. Mutation covers the twelve corrections in scope, not the file.
5. No dependency, target, cumulative or formal-selection acceptance.
