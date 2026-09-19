# Independent review: combined reference102 (signed-envelope integration) — Claude, r1

Reviewer: Claude (independent; Codex remains implementation owner). Date: 2026-09-18.
Scope, as requested: closure of my envelope66 findings E-B1 / E-M1 / E-M2 / E-M3 / E-L1 / E-L2 and my
reference101 follow-ups F1 / F2 / F3 and residuals R2 / R3, in the frozen reference102 bytes; plus an
independent adjudication of signature binding, old/new quorums, revoked keys, reader declarations,
unsupported kinds/schemas, shape failures, exception injection and route/schema/contract consistency.

**Not covered and not approved:** inherited recovery69 / platform73 (my separate review: changes required),
any Rust draft, strict Ed25519 / weak-key behaviour (59/62), current trust, custody, installation, release,
formal selection. Nothing here transfers to those.

## Bounded verdict

**No blocking finding within scope. Reviewed with specified nonblocking follow-ups, and with one stated
dependency that still blocks formal selection of the tree as a whole.**

| Finding | Adjudication |
|---|---|
| **E-B1** verifier exception boundary | **Closed.** Pinned (mutant killed). |
| **E-M1** reader support not modelled | **Closed.** Explicit, keyword-only, validated declarations; both branches pinned. |
| **E-M2** signed root only dispatched, overstated | **Closed.** Wording corrected *and* a composed boundary now refuses the signed stub. Pinned. |
| **E-M3** golden-snapshot expectations | **Closed.** 160 explicit expectations; they kill 9 of my 10 verifier mutants. |
| **E-L1** unregistered outcomes / order | **Closed.** Mapped onto retained RJ-4 outcomes; order written into the contract and matches the code. |
| **E-L2** three route tables, unplaced schema | **Closed.** One JSON route owner; schema, route owner and contract table agree; model table removed; all five inventories bind the seven new files. |
| **101 F1** generator drift unchecked | **Closed.** Executed by integration with extra-member negatives. Pinned. |
| **101 F2** three surviving mutants | **Closed.** All three now killed, by named cases. |
| **101 F3** contract carried an absent envelope owner | **Closed for the envelope.** The owner is placed and the contract cites real paths. |
| **101 R2** composed boundaries raise | **Closed.** 0 escaping exceptions in my fuzz. |
| **101 R3** profile reader fixed / chain subject | **Closed.** Reader is a parameter (pinned); the `remedy` asymmetry is now stated in the contract. |

**Dependency (blocks selection of the tree, not this verdict):** the 102 tree still contains the unmodified
69/73 recovery and platform code and fixtures. My 69/73 findings carry over unchanged — in particular
**none of their 15 corrections is pinned by a retained fixture**, and `recovery_apply` is still the one
root-consuming route that is neither document-composed nor signature-derived (see "Remaining").

Follow-ups N-1…N-4 below are nonblocking.

## Reviewed bytes (independently verified)

| Item | SHA-256 | Result |
|---|---|---|
| `trials/envelope-integration-checkpoint-102/subject.tar.xz` (1,972,016 B) | `a14078dabcba90965d418486934527f8cf35e9c791b73f8acf04cae0f61434af` | = `archive-pin.json` |
| `subject.json` (1,438 members) | `13625595a6834588260b063dd7f02f9f3cfc13e7ca19bd8d15f7d1d5e44f1ee5` | every member re-hashed from the tar **before** extraction |
| `README.md` / `archive-pin.json` | `42633a94…c087b` / `0c5b3fbb…d3db1c` | |
| `frozen-candidate.json` (1,273 entries) | in manifest | all hash-match; 0 unlisted files under `candidate/` |
| candidate model | `aadb233f2d8e05c1c73627c0607c23bf2df460ffacdd7d52a145efa663037e86` | = `envelope-source-pins.v1.json` |
| parent | — | `parent-inputs.json` file set **equals frozen reference101 exactly** (1,266 files, hash for hash) |

0 symlinks / non-regular members / unsafe paths. Extraction re-verified byte-identical after all probes; all
mutation trees were temporary copies under `claude-out/` and were removed; no `__pycache__` in the subject.
The archive itself contains synthetic test-only private keys under `envelope-check-r*/keys/` (declared as
such; no authority) — as does my `claude-out/probes/keys/`.

**Change set vs frozen101:** 12 changed (integration checker, the five inventories, security checker, two
root case files, the model, the generator, the contract) and 7 new files, all under
`design-corrections/security/`: `envelope_reference.py`, `signature-envelope.schema.json`,
`signature-envelope-routes.v1.json`, `envelope-source-pins.v1.json`, `check-signature-envelope.v1.py`, and
two recorded-differential fixtures. The placed schema is **structurally identical** to the envelope66 schema
I reviewed (no diff after normalisation).

## Owner checks, re-run into fresh output (`claude-out/checks/`)

| Check | Result |
|---|---|
| `security/check-security-lifecycle.v1.py` | 504/504, 13/13 sweeps |
| `check-integration.py` | 415 passed, 0 failed |
| `foundation/check-foundation.py` | 231/231 |
| `workflows/check_workflows.v1.py` | 1,816/1,816 |
| `native/check_native_evidence.v2.py` (report redirected) | 477/477, 66 cells |
| `security/check-signature-envelope.v1.py --output <fresh> --openssl 3.6.3` | 160 explicit + 45 composition/reader/drift + 1,803 recorded differential + 66 real crypto checks + 6,000 fuzz; passed |

All reproduce the reported counts. They are same-author checks; the adjudication rests on the probes below.

## Independent probes (`claude-out/probes/signed.py`, own keys, real OpenSSL 3.6.3 signatures)

I generated 32 fresh Ed25519 keys and built three lawful roots with **disjoint root-key sets**: R1 (v1, keys
A), R2 (v2, keys B), R3 (v3, schema 2, keys C), plus R2′ (v2, keys A, no rotation). Every expectation was
written before running. **41 cases, 0 unexpected.**

### Signed root chain — `admit_signed_root_chain`
| Case | Outcome (stage) |
|---|---|
| 2×old + 2×new signatures | ACCEPT, acceptedVersion 2 |
| old quorum only / new quorum only | REFUSE (carrier: no valid signature under the other root) |
| 2 old + 1 new | REFUSE `ROOT.CHAIN_NEW_THRESHOLD` |
| 1 old + 2 new | REFUSE `ROOT.CHAIN_OLD_THRESHOLD` |
| 2+2 with one **old** key revoked | REFUSE `ROOT.CHAIN_OLD_THRESHOLD` |
| 3+2 with one old key revoked | ACCEPT |
| 2+2 with one **new** key revoked | REFUSE `ROOT.CHAIN_NEW_THRESHOLD` |
| signed only by recovery + TR-CORE keys | REFUSE (carrier) |
| 2+2 **plus** 5 recovery-key signatures | ACCEPT — non-root keys neither help nor harm |
| valid envelope replayed over a different root body | REFUSE `RJ-4 DIGEST_MISMATCH` |
| signature bytes of key A1 presented under keyId A0 | not counted → `ROOT.CHAIN_OLD_THRESHOLD` |
| same root keys in old and new, 2 signatures | ACCEPT (one key lawfully counts for both roots) |
| two links A→B→C fully signed | ACCEPT v3 |
| link 2 signed by the **grandparent** keys (A) + C | REFUSE — continuity is to the immediate predecessor only |
| link 2 with 1 old + 2 new | REFUSE `ROOT.CHAIN_OLD_THRESHOLD` |
| R3 presented directly on R1 | REFUSE `ROOT.CHAIN_GAP` |
| **quorum-signed stub `{"rootSchema":2}`** | `verify` → `VERIFIED`; composition → REFUSE at `root-document` (`ROOT.SHAPE`) |
| fully signed but policy-defective successor / defective **stored** root | REFUSE `ROOT.RETAINED_SEMANTIC_POLICY` at `root-document` |
| `acceptedVersion` disagrees with stored root | REFUSE `ROOT.STATE_INCONSISTENT` |
| state with extra member / `acceptedVersion: true` / presented not a list / **item carrying asserted `signers`** | REFUSE (boundary) |
| reader `{1}`, schema-2 second link | REFUSE `ROOT.SCHEMA_UNSUPPORTED` |
| reader without kind `root` | REFUSE `unsupported kind for reader` |
| a `revocation`-kind envelope presented as a root link | REFUSE (routing) |

So: signer sets reach the chain owner **only** from signatures that verified under the exact previous root
and the exact new root; both thresholds are enforced; revoked keys are excluded on both sides; a caller
cannot supply signers (an item that tries is refused as malformed); and state is reported unchanged on every
valid-state refusal.

### Signed profile set — `admit_signed_profile_set`
Valid 2-of-3 → ACCEPT; 1 signature → carrier shortfall; 2 signatures with one revoked →
`PROFILE_SET.SIGNATURE_THRESHOLD`; 3 with one revoked → ACCEPT; signed by TR-CORE keys or by ROOT keys →
refused; wrong current-core pin → `PROFILE_SET.CORE_PIN_MISMATCH`; schema-1 verifying root → no active role;
foreign namespace → refused; validly signed but schema-invalid body → refused at `profile-set`; reader `{1}`
with a schema-2 verifying root → `ROOT.SCHEMA_UNSUPPORTED`; lone-surrogate publisher namespace (the E-B1
input) → `RJ-4 ENVELOPE_MISMATCH / boundary exception`.

### Reader declarations
The constructor is keyword-only and refuses: no declaration, empty sets, `reader_schemas` containing 3 or
`True` or a duplicate, empty/unknown kinds, and a bare string for kinds (8/8). Kind support is not inferred
from schema support, as the contract now states.

### Exception injection
`ed25519_verify` raising `OSError` → `verify` returns `RJ-4 ENVELOPE_MISMATCH / boundary exception OSError`,
and the chain refuses at `carrier`; the chain owner raising → REFUSE at `boundary`. **Negative control:**
with `ed25519_verify` forced to return `True`, forged all-zero signatures are ACCEPTED — which confirms the
probes are genuinely exercising cryptography and that signature validity has exactly one gate (the retained
OpenSSL primitive; its strictness is the separate 59/62 question). Fuzz: 3,000 junk-typed mutations across
`verify`, the chain and the profile entry points, including `bytes` and arbitrary objects → **0 escaping
exceptions**.

### Route / schema / contract consistency
Schema `kind`, `domain` and `role` enums each equal the route owner's sets; the contract table has 8 rows
whose kinds, roles and domains match the route owner; `ENVELOPE_KINDS` is gone from the model; retained v8
`KIND_ROUTING` is a consistent subset. The contract's stated verification order matches
`_verify_checked` line by line, including the new early reader/kind and size checks.

## Mutation evidence (`claude-out/probes/mutation*.json`)

| Mutant | Checker | Result |
|---|---|---|
| composition skips the stored root | security | **killed** — `complete-root-admission-stored-root` |
| composition checks first link only | security | **killed** — `complete-root-admission-second-link` |
| threshold helper ignores namespaces | security | **killed** — `active-tr-repair/-profile-needs-namespaces` |
| UCD guard removed | security | **killed** — version-guard sweep |
| profile reader ignored | security | **killed** — `profile-explicit-reader1-refuses-root2` |
| reader-set validation removed | security | **killed** — three `malformed-reader-set-*` cases |
| chain-context pre-check removed | security | survives — near-equivalent (N-3) |
| generator drift check neutered | integration | **killed** — both extra-member negatives |
| `verify` exception boundary removed | envelope | **killed** |
| unsupported-kind check removed | envelope | **killed** |
| signed-root reader check removed | envelope | **killed** |
| chain skips presented-document admission | envelope | **killed** — `signed-stub-not-root-admitted` |
| chain counts only old-root signers | envelope | **killed** |
| chain verifies "new" under the old root | envelope | **killed** |
| RECOVERY selects root keys | envelope | **killed** |
| namespace membership ignored | envelope | **killed** |
| signatures counted by record, not distinct key | envelope | **killed** |
| **profile passes all claimed keyIds instead of verified ones** | envelope | **survives (N-2)** |

16 of 18 killed. That is a materially different standing from reference60 (nothing pinned) and from 69/73
(0 of 15).

## Nonblocking follow-ups

### N-1 — the envelope checker is run by nothing
`check-signature-envelope.v1.py` is pinned by all five inventories but no aggregate invokes it (it needs an
OpenSSL path, so it is standalone by design). That is the shape of reference101 F1: a guard that exists but
is not part of any routine run. Either list it explicitly in the selection/readiness procedure with its
required arguments, or have integration assert its presence and last-known result. Without that, the 9
verifier mutants above are "killed" only when someone remembers to run it.

### N-2 — one real test gap: claimed keyIds vs verified keyIds
The surviving mutant hands the profile rule every `keyId` *named* in the envelope instead of the verified
set. The shipped code is correct — I confirmed (`forged-extra.json`): two valid signatures with one signer
revoked, plus a third record carrying a **forged** signature under an authorized keyId → REFUSE
`PROFILE_SET.SIGNATURE_THRESHOLD`, while the mutant would ACCEPT. No retained case combines *forged extra
record* with *revoked valid signer*; add it for the profile path and the analogous one for the chain path
(I did not build the chain variant of this mutant).

### N-3 — the chain-context pre-check is nearly redundant
Removing `type(chain) is not list or not _signer_set_valid(revoked_keys)` survives because the surrounding
`except Exception: return refuse()` catches what it guards; the only observable difference is that a tuple of
valid links would be accepted. Harmless; either keep it as documentation or add a tuple negative.

### N-4 — exceptions now become shape refusals indistinguishably
`admit_root_document` maps *any* internal exception to the plain `ROOT.SHAPE` refusal, and `run_case` does
the same for the root and profile routes. The direction is safe (never admission) and matches the v8 law,
but a genuine model defect and a malformed input now look identical, including to the fixtures — a case that
expects `ROOT.SHAPE` can pass because the gate crashed. The envelope verifier does better
(`boundary exception <Type>` in the detail). Suggest the same distinguishing detail, kept internal, so a
crash cannot satisfy a shape expectation.

## Remaining, outside this verdict

1. **Inherited 69/73 (dependency).** Unchanged in 102: my B-1 (0 of 15 recovery/platform corrections
   pinned), S-1 (final-LF idiom still admitted for `policyRecordId` ×3 models,
   `platformProfileSetBodyDigest`, `admittedPolicyRecord`), R-1…R-4, P-1, P-2 all apply to this tree.
2. **Recovery is now the odd route out.** Root chain and profile set are document-composed *and*
   signature-derived. `run_case('recovery-apply')` still calls `recovery_apply` with caller-asserted
   `signers` and an `acceptedRoot` that is never document-admitted, although the carrier already verifies
   `trust-recovery-epoch` under `recoveryAuthority` correctly. There is no `admit_signed_recovery_epoch`.
   Since lowering a floor is the most sensitive effect in the unit, this is the composition I would close
   next; it is the natural join of 69's successor with this verifier.
3. **Primitives remain importable** (`verify_root_chain`, `admit_profile_set_envelope`, and now
   `_admit_root_chain`, `_admit_profile_set`). The contract states their internal standing; this is naming,
   not cryptographic admission, as the request says.
4. **Strict Ed25519.** Signature validity has one gate, the OpenSSL primitive (negative control above). Weak
   / small-order keys and non-canonical encodings are the separate 59/62 review and are not settled here.
5. **No current trust.** The `{result, stage, outcome}` traces are reference evidence. Time, revocation
   population, the stored root and the current-core pin are TCB inputs to these functions.

## Commands and outcomes (all under `claude-out/`)

| Command | Outcome |
|---|---|
| `verify_extract.py` (before extraction; after all probes) | 1,438/1,438 verified from tar; 0 unsafe; extraction unchanged |
| six owner checkers (`checks/`) | all exit 0 with the reported counts |
| `probes/signed.py` | 29 chain + 12 profile cases, 0 unexpected; 8 constructor refusals; 4 injections; 3,000 fuzz → 0 escapes; 9 consistency joins true |
| `probes/mutation.py` **r1** | **Partly invalid — reviewer harness bug.** The 7 security-checker "kills" completed in < 1 s with 0 cases run: my harness rewrote `envelope-source-pins.v1.json` without re-pinning it, so the checker stopped at `sourcePinsValid: false`. Integration and envelope results in r1 are valid. Preserved as `mutation.failed-r1.*` |
| security mutants **r2** | **Invalid again** — re-serialising mutually pinned inventories cannot settle. Preserved as `mutation-security.failed-r2.json` |
| `probes/mutation_security_r3.py` | Valid: textual re-pin of the security inventory only; asserts `sourcePinsValid` and 504 cases run before trusting a result. 6 killed, 1 survivor |
| `probes/forged_extra.py` | shows the N-2 survivor is a real (test-only) gap; shipped code refuses |

The r1/r2 failure is worth stating plainly because it is the exact hazard I have been reporting in others'
evidence: a "killed" result that was really a pin refusal. The r3 harness refuses to report a verdict unless
the checker demonstrably ran its cases.

Interpreter: `/tmp/opensip-implementation/native-case15-reference-env/bin/python` (3.12.13 / UCD 15);
OpenSSL 3.6.3 at `/opt/homebrew/opt/openssl@3/bin/openssl`.

## Limits and unresolved assumptions
1. Reference model and reference verifier only. No Rust, no product, no custody, no OS qualification.
2. All keys are synthetic. OpenSSL acceptance is not strict-primitive qualification.
3. Mutation testing covers the 18 listed mutants, not the verifier exhaustively; a killed mutant shows a
   rule is pinned, not that the rule set is complete.
4. The 1,803 recorded cases remain golden differential evidence; I did not re-derive them.
5. I re-ran, but did not review, the foundation / workflows / native checkers.
6. The five inventories were verified against the candidate and against frozen101 (re-hashes ⊆ changed
   files, 7 additions each, no removals, no non-pin member changes); I did not audit the r1/r2 rebinding
   scripts themselves.
