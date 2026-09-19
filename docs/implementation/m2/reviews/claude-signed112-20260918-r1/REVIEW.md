# Independent bounded review — signed-security corrections 112

Reviewer: Claude (actual independent reviewer; Codex remains implementation owner). 2026-09-18.
Request: `REQUEST.md`. Scope: the delta of frozen `signed-security-corrections-checkpoint-112` over
frozen 110 — `crates/security/src/trust.rs` and three existing fixture files — as closure of my
signed-security106 S-1a, S-1b, T-1, T-2, T-3. Inherited groups, R-1/R-2/R-3 and everything the
request lists as separate are **not** reviewed here. No frozen/selected/product edit; scratch builds
and mutants only; no commit, push or delegation.

## 1. Subject verification (before extraction)

| Item | Value |
|---|---|
| `subject.tar.xz` | 4,191,880 bytes, SHA-256 `268e41e124b516a18092b25a8d72b6e3e28d28e7847e32475ecad558ed42b27f` = `archive-pin.json` |
| `subject.json` | SHA-256 `1e962bd0673134e430f0906f2671b771ed81bbe9ad4e3e90feda3d7a1f61c6d4` |
| Members | 414/414 regular, each length + SHA-256 equal to the manifest from the tar; 0 unsafe/extra; re-verified after all work |
| Product pins | 330/330 equal; no unpinned file |
| Parent | `parent-inputs.json` equals **my own** verified extraction of frozen 110; 326 unchanged, 0 added/removed; `trust-before112.rs` equals my 110 copy |
| Changed | `trust.rs` `f0d0f3a85072e3995e77339d16236d6296000cc59a1d61495837317136fca3b8` · `complete-envelope-cases.ndjson` `6f3cad3b…7f4f` · `platform-admission-cases.ndjson` `0a39729c…fd64` · `recovery-cases.ndjson` `c2646a36…2886` |
| Reference | reference107 model `2f4bd78f…4037` — equal to the copy in my own verified 107 extraction, which is what I ran |

`trust.rs`: 142 added / 16 removed lines. Production changes are five: the pending window
(`created.checked_add(86_400) != Some(expires)`); `platform` becomes `Option<String>` bounded at 64
scalars, non-string/overlong → `platform-not-in-population` with a null selector; the filesystem
refusal is the fixed string `NT-TCB-BOOT:INSTALL_ROOT_FS`; `kernUuid` (upper-case UUID) and
`dyldCdhash` (40 lower-hex) are validated **before either tier** retains drift; the projection emits
null for an absent selector. Everything else is tests and two count literals.
`complete-envelope-cases.ndjson` is the 110 file byte-for-byte plus two appended lines.

## 2. Evidence

**Owner checks, scratch build**: security 64 passed / 0 failed (baseline of my mutation run).

**Fixture expectations recomputed** from my verified reference107 (`probes/recompute.json`):
platform 1,031/1,031 equal; recovery: of 584 cases 7 are primary-carrier failures that are not recomputable by construction;
of the other 577, 576 are equal and the one difference is exactly the documented exception `reference69:overlong-pending-boot`
(reference `Refused CONTEXT_SHAPE`, fixture `Input OBSERVATION_SHAPE`). The four `pending-window`
cases (0, 86,399, 86,401, i64 max) are all `PENDING_SHAPE`.

**Differential, my own cases** (`probes/recompute_and_generate.py`, probes inserted into a scratch
`trust.rs`, `catch_unwind` around every call):

| | Cases reaching Rust | Result |
|---|---|---|
| Platform decisions (16,005 generated; 394 contain a float and cannot be represented in the Rust value type at all) | 15,611 | 15,438 projection-**identical**; 173 Rust `Err(Observation)` where the reference returns a `REFUSE` decision; **0 ADMIT disagreements**; 0 panics. Longest refusal string 81 chars, longest drift value 42 (was 5,028 in 106). |
| Recovery proposals (880; 176 window cases) | 855 | **0 admission differences; 0 write/`floorLowered` differences** on the 13 applied; 0 panics. Class pairs differ only as "Rust checks shape earlier": `CONTEXT_SHAPE → Input(OBSERVATION_SHAPE)` ×162 (the owner's documented mapping, confirmed at scale), and `SIGNATURE_THRESHOLD`/`RECORD_CHANGED…`/etc. → `Input(RECORD_SHAPE)` or `Context` ×49. |

All 173 platform errors have one cause: `fsType` present and neither string nor null (plus three
non-object observations). Both sides refuse.

**New carrier cases.** Whether the three signatures on each wrong-domain root are genuine is settled
by mutation rather than by trusting the label: with the schema/domain equality removed, both cases
are *accepted* and the carrier test fails. They could only be accepted if quorum verification passed
over the wrong-domain preimage, so the signatures are real and the refusal is caused by the check.

**Mutation** (`probes/mutation.py`; baseline green; all 14 compiled — a compile failure would not
have been counted):

| Mutant | Result |
|---|---|
| S-1a old rule `expires >= created` | killed |
| S-1a "at most 24 h" | killed |
| S-1a 86,401 | killed |
| S-1a `wrapping_add` | **survived** |
| S-1b bound 65 | killed |
| S-1b bound counts **bytes** not scalars | **survived** |
| S-1b `fsType` echoed again | killed |
| S-1b `kernUuid` unvalidated / `dyldCdhash` upper-hex / length unchecked | killed ×3 |
| T-1 root schema/domain equality removed | killed (only by the two new cases) |
| T-2 recovery root-version context removed | killed (only by the new test) |
| T-3 kernel keys excluded / extension roles skipped in reuse check | killed ×2 |

12 of 14. Both survivors are real behaviour changes (`probes/survivors.json`): the byte-count mutant
changes 97 of my platform cases (64-scalar multibyte selectors become null); the wrapping mutant
changes `PENDING_SHAPE` to `CHALLENGE_CONTINUITY_MALFORMED` for `createdMono` within 86,400 of i64
max — still a refusal, caught by a later check.

## 3. Closure of the 106 findings

| 106 finding | Status |
|---|---|
| **S-1a** pending window unenforced | **Closed.** Exact, overflow-checked, agrees with 107 on 176 boundary cases. |
| **S-1b** unvalidated identity retained as drift; `fsType` reflected; selector unbounded | **Closed.** Validation precedes both tiers; no observed text reaches a refusal; selector ≤ 64 scalars or null. The raw observation remains caller-supplied evidence and the README says so. |
| **T-1** root domain vs `rootSchema` untested | **Closed** (see mutation). |
| **T-2** root-version context untested | **Closed.** The test changes the *verifying root's* counters while the record stays fixed and expects `Context`. |
| **T-3** extension/kernel key reuse untested | **Closed**, five pairs with a positive control first. |

The 70 + 6 changed historical expectations are the intended consequence of adopting 103/107
semantics and each recomputes from 107; I found no case where 112 departs from 107 on admission.

## 4. Findings

No blocking finding.

- **N-1 (low) — non-string `fsType` is still `Err(Observation)` while 107 returns a `REFUSE`
  decision.** The code comment gives the reason as "diagnostic rendering is only for string/absent
  filesystem observations" — but 112 removed that rendering, so the stated reason no longer exists,
  and 112 made the opposite choice for `platform` (non-string → decision). Neither admits. Either
  mirror 107 (decision with the fixed refusal) or keep the typed error and rewrite the comment to the
  real reason; today it is an undocumented divergence that no fixture can contain, because the
  replay test `unwrap()`s every decision.
- **N-2 (low, tests) — the two survivors.** Add one selector of exactly 64 multibyte scalars
  (expected: echoed) and one of 65 (null); add one window case with `createdMono` near i64 max and
  assert `PENDING_SHAPE`. Both already exist in my corpus with 107-derived expectations.
- **N-3 (note) — `assert!(count > 500)`** in the recovery replay (the platform and carrier replays
  assert exact counts). The pin protects the file; an exact `584` would protect the test.
- **N-4 (note)** — `diagnostic-map.json` lists one label, which is accurate for the *fixture*; the
  same mapping applies to every malformed observation (162 of mine). Worth stating as a class rule,
  not a single exception.

Still open by the owner's own statement and untouched here: R-1, R-2, R-3, 104 N-4, Linux lane.

## 5. Smallest remaining inherited scope (as asked; not reviewed here)

I have **not** read these in full in any review, and nothing above covers them:

1. `trust_time.rs` `assess` (l.177 onward; file 582 lines) — clock plausibility and floor state; my 106
   report says "read only in part".
2. The Linux half of `platform_decision` with `linux_profile` / `profile_shape` (`trust.rs` ≈ l.3655–3800
   and the Linux arm after l.4100) — my differential exercises it against 107 (1,029 `DISTRO_SERIES`,
   771 kernel-package, 407 archive-key refusals agree) but I have not read it, and no Linux host ran.
3. `observe_revocation` (`trust.rs` l.4630 onward) with `revocation.rs` (340 lines) — list monotonicity
   and latch behaviour.

A coherent next request would be (1)+(3) together — both are "monotone state under untrusted time" —
with (2) as a separate, smaller reading task.

## 6. Bounded verdict

**112: reviewed, no blocking findings. signed-security106 S-1a, S-1b, T-1, T-2 and T-3 are closed;
N-1/N-2 are small follow-ups.** This does not alter 107 semantics on admission anywhere I could
measure. It is not approval of the inherited signed-security group, not cumulative approval or
selection, and carries no current-authority, target or dependency qualification.

Evidence: `claude-out/pin-verification.json`, `product-pins.json`, `trust.diff`, `probes/*`,
`hashes.txt`.
