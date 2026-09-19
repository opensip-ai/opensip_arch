# Independent review: inherited recovery reference69 and platform reference73 — Claude, r1

Reviewer: Claude (independent; Codex remains implementation owner). Date: 2026-09-18.
Scope: semantic review of the two correction deltas against their exact parents (reference60 → 69 → 73).
Not covered and not approved: the Rust drafts (product70 and successors), real signatures, current trust,
custody, any OS measurement or qualification, envelope66, reference101/102, formal selection. My bounded
reference101 verdict does not transfer here and this one does not transfer there.

## Bounded verdicts

| Subject | Verdict |
|---|---|
| **Recovery reference69** | **Semantics correct; changes required before selection.** Every correction is right and the refusal order now matches the owner. But **none of the nine corrections is pinned by any retained fixture** (B-1), and the correction is a point fix of a systemic grammar defect that remains at other presented-input sites (S-1). |
| **Platform reference73** | **Semantics correct; changes required before selection.** All 27 behaviour changes I probed are right and nothing improperly typed is still admitted. Same blocking gap: **none of the six corrections is pinned** (B-1). |

No correction in either delta is wrong, over-broad, or weakens an existing refusal. The required changes are
about durability of the corrections and completeness of the class, not about reverting anything.

## Reviewed bytes (independently verified)

| Item | SHA-256 | Result |
|---|---|---|
| `trials/recovery-reference-69/subject.tar.xz` (1,820,584 B) | `8094e3868cb730873476fa68379607cfd005f6228ab8ddfd39ffe3148fb6e6b3` | = pin; 1,284 members re-hashed from the tar before extraction |
| 69 `subject.json` / `README.md` / `archive-pin.json` | `dce45a1a…1986d9` / `c858cfa0…79d608` / `1aaf7fdb…a782c4` | |
| `trials/platform-reference-73/subject.tar.xz` (1,819,616 B) | `c1698c175fb134e36ffdc7b5cd7530106ed3ef7346e68cf1f7cd017e49e0214c` | = pin; 1,283 members re-hashed before extraction |
| 73 `subject.json` / `README.md` / `archive-pin.json` | `a3a6dde8…661301` / `a6ff4c8f…436b52` / `abedc920…baa8ae` | manifest hash equals the parent that reference101 declares |

No symlinks, non-regular members, absolute or `..` paths. Both extractions re-verified byte-identical after
all probes; all mutation runs used temporary copies under `claude-out/` that were removed; no `__pycache__`
written into a subject.

**Parent chain, confirmed by hash:** 69 `model-before69.py` = `f71aceff…` = the reference60 candidate model
I reviewed; 69 candidate model `015f7cbc…` = 73 `model-before73.py`; 73 candidate model `082f8681…` =
reference101's `model-before-corrections.py`. `diff -rq`: 60→69 and 69→73 each change exactly three files —
the model, the contract, and `security/source-pins.v1.json` (a two-hash rebind each). **No fixture, schema,
checker or registry file changes in either step.** 69's contract parent is byte-identical to the envelope66
contract, so both subjects inherit the envelope text (reference101 F3 applies unchanged).

Owners read: contract S4.5 (steps 1–4 and the new paragraph), S8 platform paragraph, retained v8
`linux_os_abi_predicate` (§8.4), `security-lifecycle.schemas.v1.json` (`TrustRecoveryEpochV1`,
`PendingRecoveryChallenge`), and the complete `recovery_challenge`, `recovery_apply`, `_epoch_shape`,
`_pending_shape`, `_observation`, `platform_admit`, `_macos_build_key` in all three model versions.

---

# Part 1 — Recovery reference69

## Adjudication of shape-before-quorum: derivable, and 69 is right

Contract S4.5 step 3 fixes the order: "(a) **strict closed shape of the epoch and of the pending record
before any comparison** … (b) recovery-authority threshold; (c) a pending challenge exists, its `bootId` …
and `createdMono ≤ mono ≤ expiresMono`; (d) nonce … recordDigest … epochSerial; (e) every counter; (f)
issuedAt". The reference60 model even carried the comment "strict shapes first: epoch, observation, pending
challenge (before any comparison)" while checking the pending shape *after* the quorum. So this is not a
new ordering decision: 69 brings the code to the owner's stated order. The "pending absent" case correctly
stays at (c): with no pending record there is no shape to check, and `NO_PENDING_CHALLENGE` still follows
the quorum.

**Independent precedence test** (`claude-out/probes/recovery.json`). Eight single defects, one per contract
step, then all 28 pairs, across the three models. For every pair from different steps, reference73 reports
the earlier step's detail — **0 violations of (a)…(f)**. Across 60/69/73 exactly **one** pair changes:
malformed pending + insufficient quorum: `SIGNATURE_THRESHOLD` (60) → `PENDING_SHAPE` (69, 73). Absent
pending + weak quorum is `SIGNATURE_THRESHOLD` in all three. So the reordering is exactly as narrow as
claimed.

## Each correction, tested against the parent

| Input | reference60 | reference69 / 73 |
|---|---|---|
| epoch nonce **and** pending nonce both end in LF (matched) | **APPLIED** | REFUSE `SHAPE:challenge` |
| epoch nonce ends in LF only | `CHALLENGE_MISMATCH` (late) | `SHAPE:challenge` (at shape) |
| pending `recordDigest` ends in LF | `RECORD_CHANGED_SINCE_CHALLENGE` | `PENDING_SHAPE` |
| epoch `issuedAt` Feb 31 / year 0000 / second 60 | **untyped-path `Reject` escapes the boundary** | REFUSE `SHAPE:issuedAt` |
| pending `createdWall` Feb 31 | **APPLIED** | REFUSE `PENDING_SHAPE` |
| pending `bootId` 257 chars | `CHALLENGE_BOOT_CHANGED` | `PENDING_SHAPE`; 256 still admitted (boundary correct) |
| observation `wall` = `None` | **uncaught `TypeError`** | `Reject OBSERVATION_SHAPE` |
| challenge at `mono = i64max − TTL` | ISSUED, expires = i64max | ISSUED, expires = i64max (boundary correct) |
| challenge at `mono = i64max − TTL + 1` | **ISSUED with `expiresMono = 2^63`** (unrepresentable) | REFUSE `PENDING_SHAPE`, no challenge, no pending write |
| overflow + `reportOnly` | `REPORT_ONLY_CANNOT_CHALLENGE` | unchanged (report-only still wins; nothing is written either way) |
| challenge nonce ends in LF | **ISSUED** | `Reject NONCE_GRAMMAR` |

Two of the parent behaviours were real admissions of malformed input (matched LF nonce; impossible
`createdWall`), one emitted a value outside its own schema, and two were exceptions escaping a boundary.
All are closed. Reusing `PENDING_SHAPE` for the overflow refusal mints no public vocabulary and is accurate:
the pending record that would be written is the thing that cannot be shaped.

**Hand-written shape vs the closed input schema** (two statements of one shape): 20,000 mutated epochs and
pending records through both `_epoch_shape`/`_pending_shape` and the JSON schemas — they agree on 19,807;
the 193 disagreements are all *hand refuses, schema accepts*, and all are the two rules a schema cannot
express (calendar validity, `expiresMono ≥ createdMono`). **There is no input the schema refuses and the
hand-written shape admits.**

## Findings

### B-1 (blocking for selection, both subjects) — the corrections exist only in code; no retained fixture pins any of them
Neither 69 nor 73 changes a case file. I reverted each correction in a scratch copy of the 73 tree
(re-pinning only the mutated model so the checker runs) and ran the **retained 470-case checker**
(`claude-out/probes/mutation.json`):

**0 of 15 mutants are killed.** All nine recovery reverts (three `fullmatch` sites, both calendar checks,
the `bootId` bound, the overflow refusal, the shape-before-quorum order, the `wall` type check) and all six
platform reverts (both full-string grammars, ASCII digits, both truthiness predicates, the boolean
Secure Boot) pass 470/470 with valid pins.

The supporting evidence (69 `checks/cases.ndjson` — 418 cases; 73 `cases.ndjson` — 618 cases) lives only in
the one-shot archives with hard-coded paths and is executed by nothing after selection. This is my
reference60 finding M1 again, in its purest form, and reference101 does not fix it: 101 adds root, clock and
public-detail fixtures only, so **the same 15 mutants would survive in the 101 tree**. Required: retained
negatives in `trust-recovery-cases.v1.json` and `platform-admission-cases.v1.json` for each row of the two
tables in this review (roughly 12 recovery + 10 platform cases), including the one ordering case and both
overflow boundary values.

### S-1 (medium, systemic) — the final-LF grammar defect is fixed at three sites and remains at others
The root cause is one idiom: patterns written `^…$` and applied with `.match`, where `$` also matches
before a trailing newline. 69/73 repair the recovery and platform call sites. The model still has ~30
`.match(` call sites on the same patterns (`HEX64`, `CLOSURE_ID_RE`, `PROJECT_ID_RE`, `SNAPSHOT_ID_RE`,
`REPAIR_PLAN_ID_RE`). Most are shielded by an equality comparison against trusted context, or by the strict
schema that runs first on the root gate. My sweep — append one LF to every string leaf of every retained
positive case, 2,542 mutations over 14 models — shows which are **not** shielded on presented input:

| Model | Presented field still admitted with a trailing LF |
|---|---|
| `repo-exec-grant` | `grant.authorization.policyRecordId` |
| `repair-authorization` | `authorization.consent.policyRecordId` |
| `recovery-authorization` | `authorization.consent.policyRecordId` |
| `transition-intent` | `intent.platformProfileSetBodyDigest` |
| `storage-write` | `admittedPolicyRecord` |

(Other survivors in the sweep are trusted-side context, free-text members such as `keys[].label`, or the
uncomposed root paths that reference101 has since closed; they are listed in
`platform-and-sweep.json` and are not findings.) A digest or record id that is accepted with a trailing
byte is a second spelling of one identity — the same defect 69 treats as worth a correction for the nonce.
Required: fix the idiom once (anchor with `(?![\s\S])` as the schemas already do, or use `fullmatch`
everywhere) and add one LF negative per presented field, rather than a fourth and fifth point fix.

### R-1 (medium) — recovery consumes an accepted root that was never document-admitted
`recovery_apply` reads `accepted_root['recoveryAuthority']` from whatever dictionary it is given. A stub
`{"recoveryAuthority": {...}}` — nothing else — returns **APPLIED** in all three models, and the retained
fixture's own `acceptedRoot` is `ROOT.SHAPE` at the document boundary. This is reference60 M2 on a third
route: reference101 composed document admission into the root-chain and profile-set routes, but
`run_case('recovery-apply')` still goes to the primitive. Lowering a floor is the most sensitive effect in
this unit; it should not be the one route that skips the sole root boundary. Not introduced by 69, but 69
is the recovery correction and the natural place to close it. Fold into 102's composition rule.

### R-2 (medium) — the import does not enforce the 24-hour window it is described as having
S4.5 step 1 binds `expiresMono = createdMono + 24 h`. `_pending_shape` requires only
`expiresMono ≥ createdMono`, so a pending record with `expiresMono = i64max` is **APPLIED** (all three
models): the "single-window" property rests entirely on the writer. The pending record is local state
written under the fence, so this is defence in depth rather than a bypass — but 69's own principle ("all
present pending bytes are shape-admitted before any authority comparison") argues for checking the one
relation that defines the window, and its new overflow rule guarantees the sum is always representable.

### R-3 (medium, same class as 101 R2 / envelope66 E-B1) — malformed context raises instead of refusing
8,000 junk-typed mutations of a valid import: uncaught `TypeError` (257), `AttributeError` (258),
`KeyError` (149) and `UnicodeEncodeError` (71 — a lone surrogate in a bound record field reaches
`_record_digest`). 69 converted two escapes into typed outcomes; the boundary as a whole is still not
total. Note also the asymmetry that remains by design: a malformed **epoch** is a typed
`RECOVERY.REFUSED`, a malformed **observation** is a model `Reject`. That is defensible (the observation is
host-produced), but the contract does not say so.

### R-4 (low) — three of the five `ts()` consumers in `recovery_apply` are still outside the typed refusal
`ts(record.get('lastAccepted'))` and `ts(record.get('evalHighWater'))` raise `Reject` on a calendar-invalid
stored value rather than refusing typed. Stored state, so low; listed for completeness of "real calendar
instants".

---

# Part 2 — Platform reference73

## Adjudication

The S8 paragraph 73 adds is accurate to the code and says the right thing about its own limits ("they do
not authenticate an OS measurement"). Probed on retained positive fixtures (macOS baseline, macOS exact,
Linux `secure-boot-lockdown`), reference69 vs 73 (`claude-out/probes/platform-and-sweep.json`):

| Observation | reference69 | reference73 |
|---|---|---|
| macOS build with trailing LF | **ADMIT** baseline | `NT-TCB-IDENTITY:BUILD_GRAMMAR` |
| macOS build in Arabic-Indic / full-width digits | **ADMIT** baseline | `BUILD_GRAMMAR` |
| macOS build as int / list / bool | **uncaught `TypeError`** | `BUILD_GRAMMAR` |
| Linux release with trailing LF | **ADMIT exact-measured** | `NT-TCB-IDENTITY:OSRELEASE_GRAMMAR` |
| Linux release with a non-ASCII digit | refused late, echoing the value | `OSRELEASE_GRAMMAR` |
| Linux release as int / list | **uncaught `TypeError`** | `OSRELEASE_GRAMMAR` |
| `procVersionUbuntu` = `1`, `"true"`, `"yes"`, `[1]`, `1.0` | **ADMIT** (all five) | `PROC_VERSION_NOT_UBUNTU` |
| `dpkgInstalled` / `dpkgMaintainerUbuntu` = same five | **ADMIT** | `KERNEL_PACKAGE_NOT_INSTALLED_BY_UBUNTU` |
| `secureBoot` = `true` or `1.0` | **ADMIT** | `SECURE_BOOT_OFF` |
| `secureBoot` = `1` | ADMIT | ADMIT (the only targeted input still admitted — correctly) |

27 of my targeted inputs change outcome, all in the refusing direction, all to an *existing* detail. `"yes"`
being read as "the kernel package was installed by Ubuntu" is the clearest illustration of why truthiness
has no place at an admission predicate; `type(x) is int` is the right test because `True == 1` in Python.
The already-exact predicates (`sip is True`, `uefiSignerPresent is True`, `nsUnchanged is True`,
`authenticatedRoot == 'enabled'`) are unchanged and correct.

**Divergence from the retained v8 owner, in the strict direction.** v8's `linux_os_abi_predicate` (§8.4)
still *passes* `procVersionUbuntu: "yes"` and `secureBoot: true` — I ran it. It already used `fullmatch`
(so LF and non-ASCII digits fail there, by accident of `\d` plus a later equality). v8 stays historical and
is not consumed for this predicate, so nothing breaks; but the successor is now the only correct statement,
and the contract should say the v8 predicate is superseded on this point rather than merely "retained".

## Findings

**B-1 applies** (six of six platform mutants survive the retained checker; see Part 1).

### P-1 (medium) — unvalidated observation values are reflected into outputs
Not in 73's delta, but it is the same "make the asserted observation boundary explicit" principle, and the
same class as reference60 L3:
- a `BASELINE-ATTESTED` **ADMIT** copies `kernUuid` and `dyldCdhash` into `drift` with no type or grammar
  check — a `dict` and a 5,000-character string were admitted and recorded as drift;
- a refusal embeds `fsType` verbatim: `NT-TCB-BOOT:INSTALL_ROOT_FS_<5,000 chars>` — a 5,044-character
  refusal string built from observed input, unbounded, in the position the D9 code is derived from
  (`refusals[0].split(':')[0]` — safe today only because the prefix is fixed).
Required: type/grammar-check the two identity members before recording them, and bound or drop the echoed
`fsType`.

### P-2 (medium, R-3 class) — the platform boundary is still not total
8,000 junk mutations of `observed` alone: `TypeError` 282, `KeyError` 145, all on the `platform` member
(`observed['platform']` absent; unhashable value in `plat in _ALIAS_TO_PLATFORM`; non-string
`.startswith`). 73 made the two identity members total and left the selector that precedes them. One
`isinstance(plat, str)` guard with the existing `platform-not-in-population` refusal closes it.

---

## Interaction with other reviewed subjects

| Subject | Interaction |
|---|---|
| reference101 | Changes none of the recovery/platform code or fixtures: B-1, S-1, R-1…R-4, P-1, P-2 all carry into the 101 tree unchanged. 101's guarded `ts()` and UCD guard are compatible with both deltas (they share only `ts()` and `HEX64`). |
| reference101 M2 / editable102 | R-1 is the third uncomposed root consumer; one composition rule should cover chain, profile-set **and** recovery. |
| reference101 R2, envelope66 E-B1 | R-3 and P-2 are the same missing "exception is a refusal" law; fix once. |
| envelope66 | Both subjects' contracts carry the envelope section (69's contract parent *is* the 66 contract). Sequencing per reference101 F3. |
| Rust product70+ | Not reviewed. If those drafts mirror this model's `.match` idiom, S-1 applies to them independently; regex semantics for `$` differ by engine, so each must be tested, not inferred. |

## Commands and outcomes (all under `claude-out/`)

| Command | Outcome |
|---|---|
| `verify_extract.py` (before extraction; after all probes) | 1,284 + 1,283 members verified from tar; 0 unsafe; extractions unchanged |
| hash / `diff -rq` chain checks | 60→69→73→101 confirmed; three files change per step |
| `probes/recovery.py` | control APPLIED ×3; 18 targeted rows; 28-pair precedence, 0 violations; 20,000-input shape-vs-schema differential; stub-root APPLIED; 8,000-input exception fuzz |
| `probes/platform_and_sweep.py` | 3 controls; 60 targeted inputs, 27 change 69→73, 1 (correctly) still admitted; v8 predicate comparison; reflection cases; 8,000-input fuzz; 2,542-mutation final-LF sweep |
| `probes/mutation.py` | 15 mutants applied, **0 killed** by the retained 470-case checker |

Interpreter: `/tmp/opensip-implementation/native-case15-reference-env/bin/python` (3.12.13, UCD 15). No
probe failed this round. I did not re-run the subjects' own 470-case regression as evidence (it was executed
15 times inside the mutation harness, passing each time with valid pins, which also confirms the reported
470/11 on unmutated logic by construction of the harness baseline — but I did not separately record an
unmutated run; limit 3).

## Limits and unresolved assumptions
1. Reference model only. No Rust, no real signatures, no custody, no OS observation; signer ids are
   asserted. Nothing here qualifies an operating system or a release.
2. The S-1 sweep covers only fields that occur in retained *positive* fixtures; a presented field with no
   positive fixture was not exercised. The `.match` call-site list in the review is from source inspection.
3. I did not record a standalone unmutated run of the 73 checker or re-execute the archived 418/618-case
   corpora; my conclusions rest on my own probes against the three model versions.
4. Whether R-2 (window length) and the observation-`Reject` asymmetry in R-3 are intended is an owner
   decision; I report them as inconsistencies with the contract's own wording, not as bypasses.
5. The contract text for envelope66 inherited by both subjects was not re-reviewed here.
