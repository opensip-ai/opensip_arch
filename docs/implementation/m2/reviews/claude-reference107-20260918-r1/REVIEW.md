# Independent review: combined reference107 — carrier profile pinning and publication law — Claude, r1

Reviewer: Claude (independent; Codex remains implementation owner). Date: 2026-09-18.
Two bounded scopes, as requested:
1. **closure of my reference104 finding T-104** — the carrier did not have to use the Ed25519 profile — and
   whether the new tests pin the *integration* rather than duplicating the primitive;
2. **the publication78 stage law and its reconciliation with the draft106 contract**, against my
   publication findings R78-1, R78-2 and M-1…M-5, without overstating Linux or hardware qualification.

**Not covered and not approved:** N-4 (still open, as declared), dependency and per-target qualification,
the Rust drafts (105 and 106 are reviewed separately), storage97/99 decisions D1–D6, inherited implementation
reviews, custody, current trust, formal selection. 104's A-1 / C-1 / F-1 / F-2 are unchanged here and my
104 adjudication of them stands.

## Bounded verdict

**No blocking finding in either scope. T-104 is closed and the publication law is correctly stated and fully
pinned: 14 of 14 of my mutants are killed, with valid pins and all cases executed.**

| Item | Adjudication |
|---|---|
| **T-104** carrier could bypass the profile | **Closed, at the integration.** Replacing the profile call in `Verifier.verify` with raw OpenSSL now fails eight named carrier cases and **no qualification receipt is written**. |
| 104 coverage gap: no order-8 / unreferenced root key | **Closed.** Both schemas have an *unreferenced order-8* key negative; it kills both "two doublings" and "check referenced keys only". |
| `S < ℓ` and exact-`True` callback (equivalent under OpenSSL in 104) | **Now pinned independently of the backend**, by permissive-callback controls. |
| **R78-1** local POSIX filesystem | **Closed in the law**: an explicit, exact-typed prerequisite that can only ever *reduce* uncertainty. |
| **R78-2** fallback errnos unnamed; "receipt" easily over-read | **Closed**: errnos named; barrier ≠ hardware honoured it, stated. |
| **M-1…M-5** reconciliation with draft106 | **Coherent.** Contract wording and the Rust draft say the same thing on every point I checked. |

## Reviewed bytes (independently verified)

| Item | SHA-256 | Result |
|---|---|---|
| `trials/publication-reference-integration-checkpoint-107/subject.tar.xz` | `f54272b1f93ccde20a91bbd6b8c575b4f0cf2946c1cf190bde15c704942f3381` | = `archive-pin.json` |
| `subject.json` (1,517 members) | `27ea2e2a4c1c6c75b51da19b9736de7b88dc4c5a06dcb5512ba3ae7e26c701e2` | every member re-hashed from the tar **before** extraction |
| `frozen-candidate.json` (1,277 entries) | in manifest | all hash-match; 0 unlisted files |
| parent | — | `parent-inputs.json` **equals frozen reference104 exactly** (1,275 files) |

0 symlinks / non-regular members / unsafe paths; extraction unchanged after all work; mutants ran in
temporary copies that were removed. **Change set vs 104: 9 changed, 2 new**
(`publication_reference.py`, `publication-cases.v1.json`), 0 removed — 11 in all, as stated. Notably
**`ed25519_profile_reference.py`, `envelope_reference.py` and the model are unchanged**: T-104 is closed by
tests alone, which is the right shape for a finding that was about tests.

## Owner checks, re-run in the required order (`claude-out/checks/`)

Envelope qualification first → exit 0 (168 explicit + 145 other + 1,803 recorded differential + 6,000 fuzz,
61 OpenSSL calls), receipt written. Integration **with** that receipt → **423 / 0**; **without** it →
**422** and exactly `standalone-envelope-check-current-source-receipt`. Security **581 / 581**, **15 / 15**
sweeps (the new `publication-phase-local-filesystem-and-fallback` sweep reports 108 checks), pins valid.
Foundation 231; workflows 1,816; native 477 / 66. All reproduce.

---

# Scope 1 — T-104: is the integration pinned, or only the primitive?

The distinction matters because in 104 every profile vector called `_ED.verify` directly, so the carrier
could stop using the profile and nothing noticed. The only reachable difference at the carrier is a
small-order **R** from a legitimate signer (root admission already refuses small-order **keys**), and that
needs a private scalar.

**My own test, not the owner's** (`claude-out/probes/identity_r_carrier.py`). I derive 29 test keys from
public reviewer seeds with my own arithmetic — so I hold the scalars — build lawful roots from them, and for
each carrier kind sign the *actual envelope message* with `R = identity, S = k·a`:

| Kind | honest control | raw OpenSSL on the identity-R signatures | carrier on all-identity-R | 1 identity-R + 2 honest |
|---|---|---|---|---|
| manifest, catalog, revocation, inventory, payload, platform-profile-set, root | VERIFIED | **accepts** | **`RJ-4 ENVELOPE_MISMATCH` — no valid signature** | VERIFIED, `valid=2` |
| trust-recovery-epoch | VERIFIED | **accepts** | **`RJ-4 ENVELOPE_MISMATCH`** | `THRESHOLD-SHORTFALL`, `valid=2 threshold=3` |

All eight kinds; and my pure-Python *honest* signatures are VERIFIED by the carrier, which validates the
signing code that produced the adversarial ones. The mixed row is the important one: an identity-R signature
is simply not counted — it neither poisons the envelope nor counts toward the threshold.

Composed paths: root chain with the **old**-root signatures identity-R → REFUSE at carrier; with the
**new**-root signatures identity-R → REFUSE at carrier; profile with two identity-R → REFUSE; profile with
one identity-R + one honest → REFUSE (`valid=1 threshold=2`); recovery with three identity-R → REFUSE;
recovery with one identity-R + two honest → REFUSE (`valid=2 threshold=3`); all three honest controls
ACCEPT / APPLIED. **17 cases, 0 unexpected.**

**Mutation, valid pins** (`mutation.json`): carrier calls raw OpenSSL → **killed** by
`identity-R-carrier-*` for every kind, no receipt written; profile R-admission removed → **killed** by the
same carrier cases; `S < ℓ` removed → **killed** by `scalar-upper-bound-before-permissive-callback`; callback
truthiness → **killed** by `callback-must-return-true-not-truthy`; two doublings → **killed** in the
*security* checker by the new order-8 root cases; "check only referenced keys" → **killed** by the same.
In 104 the first four of these survived. So the answer to the request's question is yes: these tests pin the
integration. The carrier cases fail when the carrier stops using the profile even though the profile module
itself is untouched.

One design point I checked deliberately: the owner's tests verify each identity-R equation with **actual
OpenSSL before** asserting the profile refuses it. That ordering is what makes the refusal meaningful — it
proves the signature is a genuine valid equation the profile rejects by rule, not a malformed input that
anything would reject.

---

# Scope 2 — the publication law and its reconciliation with draft106

## The model (`publication_reference.py`)

`disposition(stage, error, *, local_filesystem_admitted)` — the prerequisite is **keyword-only** and must be
an exact `bool`. I restated the law independently and compared exhaustively
(`publication-model.json`): all **90** stage × error × locality combinations agree; the case file has 90
cases, 90 distinct, covering all 90, 0 expectation mismatches. Properties that hold over the whole table:

- never `unchanged` after an attempted rename unless the filesystem is admitted **and** a non-EIO errno was
  captured;
- `sync-directory` is always indeterminate;
- pre-rename stages are always `unchanged`, and locality is irrelevant to them (correct: the target has not
  been named yet);
- `retryWithoutReconcile` implies `unchanged` and `ENOSPC`/`EDQUOT`;
- **admission can only make an outcome less uncertain, never more** — so a caller that wrongly passes
  `False` is merely conservative, and one that omits the keyword gets a `TypeError`, not a default.

Type guards: `1`, `None`, `"true"` as the prerequisite → `ValueError`; unknown stage, lower-case error, list
stage → `ValueError`. `mac_directory_fallback_allowed` is true for exactly `EINVAL`, `ENOTSUP`, `ENOTTY` and
false for `EIO`, `ENOSPC`, `EINTR`, `EBADF`, empty, `None`, and the integer `22`.

**Mutation:** locality ignored; rename-`EIO` unchanged; lost errno unchanged; directory-barrier failure
unchanged; retry allowed while uncertain; admission flag by truthiness; fallback includes `EIO`; fallback
drops `ENOTTY` — **8 of 8 killed** by `sweep_publication_phase_law`, with 581 cases executed each time.

The README is candid that the prerequisite is a boolean a caller supplies and that "no actual filesystem
observation is established" by it. That is the correct standing: the model states what may be *inferred*
given an admission, not how admission is obtained.

## Contract ↔ draft106, point by point

| My finding | Contract (107) | Rust draft106 | Coherent? |
|---|---|---|---|
| R78-1 local POSIX filesystem | caller must bind the handle to an admitted local POSIX filesystem; network filesystems can apply a rename and report non-EIO; a retained handle proves neither | module header: same obligation, explicitly not authenticated by the module | yes |
| R78-2(b) fallback errnos | exactly `EINVAL`, `ENOTSUP`, `ENOTTY`; `EIO`, `ENOSPC`, `EINTR`, unknown must propagate | `unsupported_directory_full_flush` — same three; table test | yes |
| M-1 not an `fsync` | "`File::sync_all` on the pinned Apple Rust toolchain issues `F_FULLFSYNC` and is not that fallback"; single direct `fsync(2)` | `libc::fsync`, once | yes |
| no retry | "a failed barrier is never retried by this primitive" | one call; test asserts `calls == 1` | yes |
| R78-2(c) what a receipt proves | "these calls request barriers; receipts do not prove that hardware honored them, power-loss survival, or media integrity" | header says the same | yes |
| M-2 metadata | new inode, requested `0600` subject to umask; old owner / ACL / xattrs / flags not copied; parent defaults may inherit; caller must admit the *resulting* custody | same | yes |
| M-3 staging namespace | `.opensip-stage-` reserved; refused by publication, confirmation and handle-relative read | three sites, every path component on read | yes |
| crash leftovers | fenced managed-state maintenance that must establish ownership / liveness; "not a read-side scavenger and is not implemented by this primitive" | same; primitive cleans only its own call | yes |
| M-4 read-back | "compares cached bytes before the barriers; it is not a media check" | same | yes |
| M-5 Linux | "Linux/musl symbol and runtime behavior require their own target qualification" | not built or run | yes — not overstated |

The supersession is scoped correctly: the heading says it supersedes v8 §5.6's **failure classification**,
the text says v8 remains historical evidence and that this rule "does not model journal append or SQLite
commit failures as filesystem replacement". I searched the contract for any remaining blanket statement that
a failed rename preserves the old state: the only hit is the sentence that supersedes it.

## Observations (nonblocking)

**O-1 — the Rust primitive has no locality input, by design.** Draft106's `publication_failure` reports
`Unchanged` for any captured non-EIO rename errno; the reference requires
`local_filesystem_admitted = True` for the same conclusion. These are consistent only because the contract
makes filesystem admission a precondition of *calling* the primitive. That is a legitimate design, but it
means the Rust type system does not carry the prerequisite: nothing stops a future caller from constructing
a `RetainedDirectory` over an unadmitted volume and trusting `Unchanged`. When the admission owner exists,
consider making `RetainedDirectory::from_retained_handle` take an admission token so the precondition is a
type, not a comment.

**O-2 — the model still accepts impossible stage/error pairs** (e.g. `write-temp` + `RENAME_FAILED`), now
declared as "conservative unreachable combinations". Every one resolves safely; I verified that as part of
the exhaustive properties. Fine as stated.

**O-3 — 106's N-1 is outside this subject.** The reference cannot pin the Rust *wiring* of the fallback
closure; that follow-up stays with the Rust draft.

## Remaining, outside this verdict
N-4; per-target and dependency qualification (59/62 D-1); OpenSSL as the equation backend (one build, one
platform); storage97/99 D1–D6; inherited implementation reviews; formal selection. The qualification receipt
remains self-asserted routine evidence, not authenticated proof — as the owner says.

## Commands and outcomes (all under `claude-out/`)

| Command | Outcome |
|---|---|
| `verify_extract.py` (before extraction; after all work) | 1,517 / 1,517 verified from tar; 0 unsafe; unchanged |
| owner checkers, required order (`checks/`) | envelope pass + receipt; integration 423 / 0 with receipt, 422 without; security 581 / 15; foundation 231; workflows 1,816; native 477 / 66 |
| `probes/identity_r_carrier.py` | 8 carrier kinds + 9 composed cases with reviewer-held scalars: 0 unexpected |
| `probes/publication_model.py` | 90 / 90 agree with my restatement; 5 table-wide properties hold; 7 type guards; 10 fallback inputs |
| `probes/mutation.py` | 14 mutants, all valid (pins valid, 581 cases run, or no pin refusal): **14 killed** |

No probe failed this round. Toolchain: Python 3.12.13 / UCD 15, OpenSSL 3.6.3; aarch64 macOS.

## Limits
1. Reference and tests only; all keys synthetic; no signing API, custody or authority is involved.
2. The publication model is a pure function of labels. It establishes no filesystem fact, and no fault was
   induced on any filesystem in this review (my real-fault evidence is in the 78/79/88 and 106 reviews, on
   macOS only).
3. One platform and one OpenSSL build; nothing here qualifies Linux, musl, x86 or hardware durability.
4. I re-ran but did not review the foundation / workflows / native checkers, and verified the pin inventories
   through the checkers and my harness rather than re-deriving the two rebinding rounds.
