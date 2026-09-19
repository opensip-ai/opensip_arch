# Independent review: inherited signed-security implementation group in frozen product106 — Claude, r1

Reviewer: Claude (independent; Codex remains implementation owner). Date: 2026-09-18.
Subject: `crates/security/src/trust.rs` (4,717 lines), `trust_time.rs` (582), `metadata_unicode15.rs` (796)
with their fixtures and manifests, exactly as frozen in `publication-corrections-draft-checkpoint-106` — the
cumulative form of pending drafts 54 / 57 / 59–75. Expected semantics: frozen reference107 (with 104 / 103
inherited), not raw v8 where superseded.

**Outside this review, as instructed:** `journal_store.rs`, `custody.rs`, `commit_authority.rs`,
`revocation.rs`, native final-gate / monitor, storage, lifecycle, evaluator; every dependency and target
question; release qualification. Product `fa72e50` is unchanged; private 106 is conditional and is not
current authority. My earlier bounded reviews (64 Unicode bridge, 105 key gate / quorum typing) are not
treated as approval of this group; I re-verified and re-ran from scratch. Open follow-ups 105 N-1 / N-2,
106 N-1 and 104 N-4 stay recorded.

## Bounded verdict

**Changes required — one substantive finding (S-1): the Rust recovery and platform logic implements the
reference73-era semantics, not the reference103 corrections that frozen107 inherits.** Everything else I
examined is sound: no admission difference from the reference in 42,000 differential inputs, no authority
conferred by malformed input, outputs own their bytes, and no persistence or signing exists in these files.

| Area | Result |
|---|---|
| Strict bounded metadata lexing / canonical encoding / profile separation | **Sound.** 30,027 byte-level inputs: 0 admission differences, 0 canonical-byte differences vs frozen107. |
| Digest and envelope-message framing | **Sound** (domain ‖ 0x00 ‖ C(value); six-field signed subject rebuilt from parsed fields, not caller text). |
| Complete root semantics, refusal ordering, reader caps | **Sound.** 12,000 mutated roots under three reader sets: 0 admission differences; refusal classes map one-to-one *including precedence*. |
| Root chain: dual quorum, counters, time, expiry, revocation | **Sound and well pinned** (7 of 7 chain mutants killed). |
| Signed recovery: challenge / epoch matching, boot, expiry, serial, floor exception, read-only proposal | Logic sound and well pinned (10 of 11 killed) **but missing the 103 exact-window rule (S-1a)**. |
| Signed profiles: core pin, current-root role | **Sound** (pin mutant killed). One precedence note (R-1). |
| Signed revocation: root-version binding, prior-revocation filtering | **Sound** (binding mutant killed; 105 showed the filter mutant killed). Monotonicity is correctly *not* claimed here. |
| Platform decision | Exact-type and grammar rules present, **but missing the 103 output-hygiene rules (S-1b)**. |
| Clock plausibility / floor state (`trust_time.rs`) | Malformed-continuity anchor rule present; **read only in part** — see coverage. |
| Malformed contexts never confer authority | **Holds** in everything I fuzzed; residual panic surface noted (R-3). |
| Outputs own exact bytes | **Holds**: `stored.to_vec()`, parsed payload re-compared to the verified body, digests recomputed, never copied from the caller. |
| Unauthorized persistence / signing | **None.** No filesystem write, no signing key or sign call in the three files; the crate exports nothing (`mod` private, `#![forbid(unsafe_code)]`). |

## Reviewed bytes (independently re-verified)

`subject.tar.xz` `4fcbe721fe2c2e48692d441d28fb5911f6e0bf253e9a0c7f2ab69a15bf41afc2`; manifest
`aba52347e5b9ea368d1651918d06d62fc9b9365d568ad6319d1796b8a338bc38`; all 387 members re-hashed from the tar
before extraction into a fresh workspace; 330 / 330 product pins match, 0 unlisted. Source reviewed:
`trust.rs` `aed5c88b5e234beb…`, `trust_time.rs` `86d5ea1ca8496a91…`, `metadata_unicode15.rs`
`aefc264bab1960ca…`. 0 unsafe archive members; extraction unchanged after all work; builds and mutants in
scratch copies only. `Cargo.lock` equals 105's, whose 51 packages I verified against lock checksums.
**Owner tests reproduced: 58 passed** (35 of them in the three files under review).

## S-1 (changes required) — the implementation lags the reference it is meant to satisfy

The Rust fixtures in this group are labelled and sourced from the 69 / 73 generation
(`"label":"reference69:nonce-final-LF"`; `fixture-provenance.json` lists the recovery, platform, chain,
profile and revocation corpora with no later source). Reference103 — inherited by frozen107, which the
request names as the expected semantics — added rules in response to my 69/73 findings R-2 and P-1 / P-2.
**Those rules are absent from the Rust**, which I confirmed by running the subject's own functions from a
test module inserted into a scratch copy (`claude-out/probes/misc.json`):

**S-1a — recovery pending window is not exact.** Reference: `expiresMono == createdMono + 86400`
(contract: "import rechecks this writer invariant rather than accepting an extended window").
Rust `admit_recovery_pending` requires only `expires ≥ created`:

| pending window | reference107 | Rust 106 |
|---|---|---|
| exactly 24 h | admit | ADMITTED |
| 24 h + 1 s | `PENDING_SHAPE` | **ADMITTED** |
| 24 h − 1 s | `PENDING_SHAPE` | **ADMITTED** |
| zero length | `PENDING_SHAPE` | **ADMITTED** |
| extended to `i64::MAX` | `PENDING_SHAPE` | **ADMITTED** |

The Rust *issuer* does compute `mono + 86400` with a checked add and refuses overflow, so a well-behaved
writer produces only exact windows; the gap is that the importer trusts stored state for the one relation
that defines "single-window".

**S-1b — platform output hygiene.** Reference103: macOS UUID and cdhash observations "at both tiers, must
satisfy the same closed field schemas … before any value is recorded as drift"; the filesystem refusal
"never echoes unbounded observed text"; a non-string or over-64-scalar selector is `platform: null`.

| observation | reference107 | Rust 106 |
|---|---|---|
| baseline tier, `kernUuid` = a JSON object | REFUSE `NT-TCB-IDENTITY:kernUuid` | **ADMIT**, object recorded as drift |
| baseline tier, `dyldCdhash` = 5,000 characters | REFUSE | **ADMIT**, 5,000 characters recorded |
| baseline tier, lower-case UUID | REFUSE (grammar) | **ADMIT** |
| `fsType` = 5,000 characters | fixed 27-character refusal | refusal string of **5,028** characters |
| selector = 5,000 characters | `platform: null` | refused, but **5,000 characters copied into the decision** |
| selector = integer | typed refusal | typed `Err(Observation)` — fine |

These are not authority bypasses — every observation is a declared assertion and the decision says so — but
an ADMIT that records an unvalidated object as "drift" is precisely what 103 closed, and a Rust consumer
built on this would inherit it. Required: port the two rule sets and regenerate the recovery and platform
corpora from the 103+ reference. The other 103 items are already met or exceeded in Rust: full-string
grammars throughout (hand-written byte checks, no `$`-newline idiom), typed observation/record errors, and a
challenge issuer that validates the exported bound record.

## Independent differential evidence (`claude-out/probes/`)

Expectations come from the **frozen107 Python reference**; inputs are mine.

**Codec — 30,027 byte strings** (27 seeds covering NFC/NFD, the Unicode-15 boundary `U+0897`, surrogate
pairs and lone surrogates, i64 edges, `-0`, floats, exponents, duplicate and NFC-colliding keys, BOM, depth
64 / 65, plus 30,000 byte-level mutations): both accept 2,755 with **identical canonical bytes**; both
refuse 27,272; **0 admission differences**. Refusal *class* agrees on 26,876 of 27,272; the 396 differences
are inputs with two defects, where Rust reports the lexically earlier one (`InvalidUnicode` /
`DuplicateKey`) and Python's parse-then-check reports `MALFORMED_JSON` or a numeric error. Neither order is
wrong; nothing depends on it.

**Root admission — 12,000 mutated roots**, each under `{1,2}`, `{1}` or `{2}`: 2,707 accepted by both, **0
admission differences**, and the refusal confusion table is diagonal — `ROOT.SCHEMA_SHAPE`/`ROOT.SHAPE →
Shape`, `ROOT.SCHEMA_UNSUPPORTED → Unsupported`, `ROOT.UNKNOWN_KEY → UnknownKey`,
`ROOT.RETAINED_SEMANTIC_POLICY → RetainedPolicy`, `ROOT.SCHEMA_CONSTANT_TYPE → SchemaConstant`, threshold,
previous-version, expiry, root-keys, timestamp and recovery classes likewise — so **refusal precedence
matches the reference**, not just the verdict. A targeted follow-up on the class the random corpus did not
reach: schema-2 extension-role and kernel-key reuse (seven placements) — reference and Rust agree on all
(`ROOT.KEY_REUSE` ↔ `KeyReuse`).

Neither differential produced a panic (each ran as a single test that would have aborted).

## Mutation evidence (`mutation.json`) — each mutant built and run against the crate's tests

**24 of 29 killed; 1 did not compile and is not counted.**

Killed: chain — gap, backdated, state-inconsistent, expired-no-chain, final-expired, final-future, link
admitted under the wrong reader set; envelope — stored digest, preimage, role routing, publisher namespace;
recovery — boot, expiry, continuity, nonce, **fresh record digest**, serial, counters, before-last-accepted,
future, too-old; profile — core pin; revocation — root-version binding; quorum — namespace membership.

Survivors:

| Mutant | Assessment |
|---|---|
| envelope: root domain vs payload `rootSchema` check removed | **Real test gap (T-1).** A schema-1 root body carried under the `root.2` domain tag would verify. The retained carrier fixtures do not include it, although the 66 / 102 reference suite does. |
| recovery: verifying-root version vs `record.rootVersion` removed | **Real test gap (T-2).** Nothing else ties the supplied root to the record's root counter; no case has them differ. |
| root: key-reuse check removed | **Real test gap (T-3).** The retained v8 rules catch reuse among core lists, which is why it survives; reuse involving `TR-REPAIR` / `TR-PROFILE` / kernel keys is caught *only* by this check. The shipped code refuses all seven placements I tried; no retained case does. |
| profile: schema-1 root allowed | Equivalent — a schema-1 root cannot carry `TR-PROFILE`, so the next clause refuses. |
| quorum: inactive role allowed | Equivalent given root admission — a role with keys is always `active`; an absent role has threshold 0 and is `RoleUnavailable`. |

## Residual questions (nonblocking)

**R-1 — profile refusal precedence differs from the reference composition.** `verify_profile_set` checks
shape and the core pin **before** the carrier signature; the reference composes carrier first, then profile
rules. Both refuse the same inputs; they can name different reasons, and the Rust reports a reason derived
from unauthenticated bytes. Pick one order and state it (the recovery path in the same file verifies the
carrier before the payload rules).

**R-2 — no explicit reader / kind declaration at the carrier.** The reference `Verifier` requires
`reader_schemas` and `supported_kinds` (my envelope66 E-M1); Rust `verify_envelope` has neither. Root
*schema* support is enforced where it matters — `admit(…, readers)` on the anchor and on every chain link —
so a `{1}` reader cannot adopt a schema-2 root. But a stage-1 reader refusing the *added kinds*
(`trust-recovery-epoch`, `platform-profile-set`) is not expressible. Decide whether kind support is a carrier
input in Rust or an obligation of each caller, and say so.

**R-3 — refusal by panic is still possible in principle.** After a closed-shape check the code indexes
(`o["entries"]`) and unwraps freely; I count several hundred such sites in `trust.rs` including tests. The
ones I traced are guarded by a preceding shape check (e.g. `revocation_shape` validates calendar time before
`timestamp_seconds(…).unwrap()`), and my 42,000 differential inputs raised none. But the guarantee is
structural-by-inspection, not enforced; a per-boundary fuzz target (chain, recovery, profile, revocation,
platform) would turn it into evidence. A panic is not a refusal.

**R-4 — revocation monotonicity and "current" are not here, correctly.** `verify_revocation` returns a
verified document with its version and issue time and its own comment says callers still need admitted
time, durable monotonic counters and root custody. That is the right boundary; it means list monotonicity is
unreviewed in this group because it lives in the excluded `revocation.rs`.

## Coverage — stated honestly

Read in full: metadata value bounds and parser; retained v8 root semantics (`assess`); digest and
envelope-message framing; key gate and primitive; complete root admission; quorum; envelope verification;
root chain; recovery pending / observation / proposal / challenge issuance; signed profile and revocation
verification; revocation shape; the macOS half of the platform decision and `evaluate_platform`.
**Not read line by line:** the canonical encoder (covered by the 30,027-input byte differential and my 64
review), profile shape helpers, the Linux half of the platform decision (behaviour known from my 69/73
probes of the reference, not re-probed in Rust), `observe_revocation`, and the body of `trust_time::assess`
(I confirmed the malformed-continuity anchor rule is present and that its 2 tests pass; I did not run a clock
differential). The huge inline / included fixtures were treated as data: I verified provenance labels and
re-derived the two I changed in 105; I did not re-derive the chain, recovery, profile or revocation corpora.

## Commands and outcomes (all under `claude-out/`)

| Command | Outcome |
|---|---|
| `verify_extract.py` (before extraction; after all work) | 387 / 387 from tar; 330 / 330 product pins; unchanged |
| `cargo test -p opensip-security --offline --locked` (scratch) | 58 passed |
| `probes/gen_inputs.py` → reviewer tests in scratch `trust.rs` | codec 30,027 and roots 12,000 + 7: 0 admission differences |
| reviewer test `claude_recovery_window_and_platform_outputs` | S-1a / S-1b tables above |
| `probes/mutation.py` | 29 mutants: 24 killed, 5 survive (3 real test gaps, 2 equivalent), 1 compile failure not counted |

Toolchain: Rust 1.95.0, Python 3.12.13 / UCD 15 (frozen107 reference); aarch64 macOS.

## Limits
1. One macOS lane; no dependency, target or release qualification; nothing outside the three files.
2. Differentials cover the codec and root admission; chain, recovery, profile and revocation rest on
   reading plus mutation over the owner's fixtures, which are 69/73-generation (S-1).
3. All keys and signatures in the fixtures are synthetic; signer identity, time, revocation population,
   record custody and root selection are supplied inputs here, not authenticated facts.
4. This review does not make private 106 current authority and does not close 105 N-1 / N-2, 106 N-1 or
   104 N-4.
