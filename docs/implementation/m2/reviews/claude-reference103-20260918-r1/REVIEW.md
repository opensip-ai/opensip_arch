# Independent review: combined reference103 (recovery / platform integration) — Claude, r1

Reviewer: Claude (independent; Codex remains implementation owner). Date: 2026-09-18.
Scope, as requested: closure of my reference69/73 findings B-1, S-1, R-1…R-4, P-1, P-2 and my reference102
follow-ups N-1…N-3 in the frozen reference103 bytes, plus an independent challenge of the newly added signed
recovery composition.

**Not covered and not approved:** the strict-Ed25519 / root-key-validity decision (my crypto59/62 A-1 and C-1
— explicitly *not* corrected here, and I did not expect it to be), Rust drafts, dependency / target
qualification, current trust, custody, persistence, installation, release, formal selection. `APPLIED` is an
inert write proposal; nothing here is authority.

## Bounded verdict

**No blocking finding within scope. Every 69/73 finding and every 102 follow-up in scope is closed and
pinned; two small nonblocking follow-ups (F-1, F-2) and the already-declared N-4 remain.**

| Finding | Adjudication | Pinned? (my mutation run) |
|---|---|---|
| **69/73 B-1** no retained fixture pinned any correction | **Closed.** | All 14 original behavioural mutants killed, each by a named `retained103-*` case |
| **69/73 S-1** final-LF idiom at other presented fields | **Closed at the root cause.** 0 `.match(` call sites remain in the model (was ~30); all five presented fields now refuse | 3 of 3 sampled reverts killed |
| **69/73 R-1** recovery consumed an unadmitted root | **Closed.** Document admission precedes the quorum; a stub root is `ROOT_NOT_ADMITTED` | killed |
| **69/73 R-2** 24 h window not enforced at import | **Closed.** `expiresMono == createdMono + 86400` exactly | killed (extend *and* shorten cases) |
| **69/73 R-3** malformed context raised | **Closed.** 0 escaping exceptions in my fuzz; string / dict collections refuse `CONTEXT_SHAPE` | killed |
| **69/73 R-4** stored-timestamp `Reject` escaped | **Closed.** Typed `CONTEXT_SHAPE` refusal | covered by the same boundary |
| **69/73 P-1** unvalidated observation reflected into output | **Closed.** Schema-owned UUID / cdhash grammar before either tier; fixed 27-character filesystem refusal | both killed |
| **69/73 P-2** platform selector not total | **Closed.** 0 exceptions in 8,000 mutations; selector bounded | killed |
| **102 N-1** envelope checker run by nothing | **Closed by contract** — a required, separately reported standalone run. Procedural, not mechanical (F-2) | n/a |
| **102 N-2** claimed vs verified keyIds | **Closed** for profile, both chain quorums, and recovery | 3 of 3 killed |
| **102 N-3** near-equivalent chain pre-check | **Closed** (tuple-chain sweep retained) | not re-mutated |
| **102 N-4** exception vs shape diagnostics | **Open, honestly declared** as nonblocking in the README and contract | — |
| **New: signed recovery composition** | **Sound** under 39 independent cases with real signatures | 4 of 5 verifier mutants killed; the 5th is equivalent (F-1) |

Overall mutation result: **29 of 31 killed**; both survivors are the same reader-parameter point (F-1), one
of them an equivalent mutant. Compare 0 of 15 on the 69/73 subjects.

## Reviewed bytes (independently verified)

| Item | SHA-256 | Result |
|---|---|---|
| `trials/recovery-platform-integration-checkpoint-103/subject.tar.xz` (2,063,832 B) | `252c2ad2fc52757fd27ca5864450fb6df3be835fa86555eb7036fbb8eadc2535` | = `archive-pin.json` |
| `subject.json` (1,689 members) | `c54c86848e0dacdd65c1dedb36d719ed69955b79b5bb7a0241ea19636db43f68` | every member re-hashed from the tar **before** extraction |
| `README.md` / `archive-pin.json` | `ed7e13fb…58d9992` / `747de64d…5ea40981` | |
| `frozen-candidate.json` (1,273 entries) | in manifest | all hash-match; 0 unlisted files under `candidate/` |
| parent | — | `parent-inputs.json` **equals frozen reference102 exactly** (1,273 files, hash for hash) |
| `envelope-reference-before-composition.py` | — | byte-identical to the frozen102 verifier I reviewed |

0 symlinks / non-regular members / unsafe paths. Extraction re-verified byte-identical after all work; every
mutation tree was a temporary copy under `claude-out/` and was removed; no `__pycache__` in the subject.

**Change set vs frozen102:** 19 changed, 0 added, 0 removed — the model, the verifier and its pin, both
checkers, the schema bundle, **seven case files** (recovery, platform, execution-principal, repair,
repair-recovery, storage-write, transition-journal), the contract, and the five inventories. That seven
fixture files changed is itself the answer to B-1: 69 and 73 changed none.

## Owner checks, re-run into fresh output (`claude-out/checks/`)

security 565/565 with 14/14 sweeps and valid pins; integration 415/0; foundation 231/231; workflows
1,816/1,816; native 477/477 (66 cells, report redirected); envelope checker 160 explicit + 73 composition /
reader / drift + 1,803 recorded differential + 66 real crypto checks + 6,000 fuzz, passed. All reproduce the
reported counts. Same-author checks; the adjudication rests on what follows.

## Signed recovery composition — independent challenge (`claude-out/probes/signed_recovery.py`)

Own keys (26 fresh Ed25519 test-only keys), real OpenSSL 3.6.3 signatures. I did not reuse a fixture epoch:
I took a lawful record, issued a **fresh challenge with the real `recovery_challenge`**, built the matching
`TrustRecoveryEpochV1`, canonicalised it, and signed the envelope with the root's `recoveryAuthority` keys.
Every expectation was written before running. **39 cases, 0 unexpected, and the supplied record was
byte-unchanged after every call.**

| Challenge | Outcome (stage) |
|---|---|
| 3 recovery-authority signatures | APPLIED |
| 2 signatures | REFUSE — carrier `THRESHOLD-SHORTFALL` |
| 3 signatures, one signer revoked | REFUSE — `SIGNATURE_THRESHOLD` |
| 4 signatures, one revoked | APPLIED |
| **3 valid (one revoked) + a forged record under an authorized keyId** | REFUSE — `SIGNATURE_THRESHOLD` (forged record never counts) |
| signed by ROOT keys / by TR-CORE keys / 2 recovery + 3 root | REFUSE at carrier — root keys never count for recovery |
| role token `ROOT` on a recovery epoch | REFUSE — routing |
| valid envelope replayed over a different epoch body | REFUSE — `RJ-4 DIGEST_MISMATCH` |
| genuinely signed epoch for another nonce / another record digest | `CHALLENGE_MISMATCH` / `RECORD_CHANGED_SINCE_CHALLENGE` |
| record counter advanced since the challenge | `RECORD_CHANGED_SINCE_CHALLENGE` |
| genuinely signed **higher** counter | `COUNTER_MISMATCH` |
| other boot / one second after the window / one second before the challenge | `CHALLENGE_BOOT_CHANGED` / `CHALLENGE_EXPIRED` / `CHALLENGE_CONTINUITY_MALFORMED` |
| exactly at the window end | APPLIED (boundary correct) |
| pending window 24 h + 1 s / extended to i64max | `PENDING_SHAPE` (R-2) |
| signed far-future `issuedAt` / signed impossible calendar date | `ISSUED_IN_FUTURE` / `SHAPE:issuedAt` |
| **REPLAY:** the same signed epoch after its proposed writes are applied to a copy | `NO_PENDING_CHALLENGE` |
| **REPLAY:** the old signed epoch against a *new* challenge | `CHALLENGE_MISMATCH` |
| verifying root fails document admission / stub root with only `recoveryAuthority` + `keys` (R-1) | REFUSE at carrier |
| reader `{1}` with a schema-2 root / reader without the recovery kind | `ROOT.SCHEMA_UNSUPPORTED` / unsupported kind |
| schema-2 verifying root under a dual reader | APPLIED (recoveryAuthority is schema-independent) |
| `revoked_keys` as a **string**, a dict, uppercase member, member with final LF, int member | `CONTEXT_SHAPE` (all five) |
| record is a list / observation wall impossible date / lone-surrogate bootId / stored `lastAccepted` impossible date (R-4) | REFUSE, typed |

Fuzz: 3,000 junk-typed mutations (including `bytes` and arbitrary objects) of envelope, root, record,
observation and revocation → **0 escaping exceptions**, and every APPLIED outcome was UTF-8 serialisable.

**Pure model, asserted-signer path** (declared TCB, as the README says): a single 64-hex **string** as the
signer collection, and a 192-character string of three concatenated ids, both refuse `CONTEXT_SHAPE` — so
Python's "a string is an iterable of characters / a substring test" cannot masquerade as a signer set; a
dict refuses; a tuple is accepted; a stub root is `ROOT_NOT_ADMITTED`.

**Challenge export:** an impossible stored `lastAccepted`, a string or lone-surrogate `rootVersion`, and an
integer `evalHighWater` all give typed `Reject RECOVERY.REFUSED:CONTEXT_SHAPE` instead of exporting an
invalid bound record.

**What the composition does and does not establish.** No caller-supplied signer set and no separately
supplied epoch body enter `admit_signed_recovery_epoch`: the epoch is parsed from the very bytes whose
digest the carrier authenticated, and only `evidence['valid']` reaches the rules. Carrier-then-payload
precedence is explicit and I confirmed it: below-threshold is refused at `carrier` before any payload rule,
and revocation is applied afterwards, so a quorum that is met only with a revoked key refuses at the
payload stage. The record, root selection, observation and revocation population are TCB inputs — correctly
declared. The proposed `writes` are returned, not applied; persistence, the fence and single-use consumption
remain with their owner (my replay test had to apply the writes itself, which is the right shape).

## Platform and systemic re-checks (my 69/73 probes, re-run against 103)

- The 27 exact-type / grammar outcomes are unchanged from reference73; the only targeted input still
  admitted is the correct one (`secureBoot: 1`).
- **P-1:** a `dict` `kernUuid` / 5,000-character `dyldCdhash` at baseline tier is now **REFUSE** and nothing
  is recorded as drift; the filesystem refusal is a fixed 27-character string.
- **P-2:** 8,000 junk mutations of `observed` → **0 exceptions** (was 427).
- **S-1:** my 3,421-mutation final-LF sweep no longer lists any of the five presented fields
  (`policyRecordId` ×3 models, `platformProfileSetBodyDigest`, `admittedPolicyRecord`). Remaining survivors
  are trusted-side context, stored timestamps the recovery path does not consume, and free-text `label`.
  `grep` finds **no** `.match(` in the model. This was the right way to fix it: the idiom, not the sites.
- The contract now states that the v8 Linux truthiness predicate is superseded (my 69/73 note); I re-ran v8
  and it still passes `"yes"` and `true`, as historical bytes should.

## Nonblocking follow-ups

### F-1 — the recovery reader parameter is unpinned in the pure model
Reverting `_recovery_apply` to a hard-coded `(1, 2)` reader survives the 565-case checker, because
`run_case('recovery-apply')` never passes `readerSchemas` and no recovery case uses an explicit reader. It is
not an equivalent mutant: the shipped model called with reader `(1,)` and a schema-2 root returns
`ROOT_NOT_ADMITTED` (`reader-probe.json`; malformed declarations `[True]`, `None`, `'12'` also refuse). The
README already discloses the dual-reader default for projected fixtures. One routed case with
`readerSchemas: [1]` closes it. The *verifier-level* counterpart (not passing `self.reader_schemas`) also
survives but **is** equivalent: `verify()` has already admitted the same root under the same reader set, so
the carrier refuses first.

### F-2 — N-1 is closed by procedure, not by mechanism
The contract now requires the standalone envelope run with a preserved report, and says plainly that
integration does not run it. That is an honest and acceptable closure. It still means the nine-plus
verifier protections are enforced only if the selection procedure is followed; a one-line integration check
that a fresh envelope report exists and names the current verifier hash would make the rule self-enforcing.

### N-4 — carried, as declared
Internal exceptions in the model wrappers still collapse into the ordinary shape/context refusal
(`CONTEXT_SHAPE`, `ROOT.SHAPE`, `platform-not-in-population`), so a crash can satisfy a fixture that expects
that refusal. 103 adds three more such wrappers. The signed boundary keeps the exception type in its
internal trace; the pure model does not. Correctly reported by the owner as not fixed.

## Dependencies and what this verdict does not carry

1. **Crypto59/62 A-1 and C-1 are open in this tree by design.** Signature validity in every composed path
   here is decided by the retained OpenSSL primitive, which accepts forgeries under small-order public keys,
   and root admission still admits such keys. Until that successor lands, "signature-derived" means
   "OpenSSL-valid", not "strict-profile-valid". The README states this dependency; I repeat it because
   recovery — the route that lowers a floor — inherits it too.
2. No Rust draft, target qualification or dependency acceptance is implied.
3. Formal selection still requires the owner's process; five inventories were verified by the owner checkers
   (`sourcePinsValid: true` in my run) and by my harness, which only produces a result when pins are valid. I
   did not separately re-derive all eight rebinding rounds.

## Commands and outcomes (all under `claude-out/`)

| Command | Outcome |
|---|---|
| `verify_extract.py` (before extraction; after all work) | 1,689/1,689 verified from tar; 0 unsafe; extraction unchanged |
| six owner checkers (`checks/`) | all exit 0 with the reported counts |
| `probes/signed_recovery.py` | 39 signed cases, 0 unexpected, record never mutated; 7 pure-model cases; 4 challenge-export cases; 3,000 fuzz → 0 escapes |
| `probes/platform_and_sweep.py` (my 69/73 probe, retargeted) | 27 outcomes unchanged; P-1, P-2, S-1 closed |
| `probes/mutation.py` | 31 mutants, **harness validity asserted per mutant** (pins valid and all 565 cases executed, or envelope checker not stopped by its pin): 29 killed, 2 survive (F-1) |
| `probes/reader_probe.py` | shows the model-level survivor is a real, small test gap |

No probe failed this round. The mutation harness is the corrected one from my 102 review: it refuses to
report a verdict unless the checker demonstrably ran its cases, so none of these kills is a pin refusal.

Interpreter: `/tmp/opensip-implementation/native-case15-reference-env/bin/python` (3.12.13 / UCD 15);
OpenSSL 3.6.3.

## Limits and unresolved assumptions
1. Reference model and reference verifier only; all keys synthetic.
2. OpenSSL acceptance is the signature gate in every probe; strictness is the separate 59/62 question.
3. 31 mutants cover the findings in scope, not the whole model; I sampled three of the ~30 converted
   `fullmatch` sites rather than reverting each.
4. I re-ran but did not review the foundation / workflows / native checkers, and did not review the four
   non-recovery case files beyond what my sweep exercised.
5. The 1,803 recorded cases remain golden differential evidence.
