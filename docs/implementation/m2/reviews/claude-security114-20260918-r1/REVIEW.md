# Independent bounded review — security follow-ups 114

Reviewer: Claude (actual independent reviewer; Codex remains implementation owner). 2026-09-18.
Request: `REQUEST.md`. Scope: the delta of frozen `security-followups-checkpoint-114` over frozen 113,
as closure of my signed112 N-1 to N-4. Not a whole-group review; Linux/profile helpers, R-1/R-2/R-3 and
the monotone-state group keep their own standing. No frozen/selected/product edit; scratch builds and
mutants only; no commit, push or delegation.

## 1. Subject verification (before extraction)

| Item | Value |
|---|---|
| `subject.tar.xz` | 4,078,392 bytes, SHA-256 `e9f44223b0462321ce50203c83f3d054b076a780def2f1c135ccd5ffc6040359` = request and `archive-pin.json` |
| `subject.json` | SHA-256 `9b2aec32391436db2c57aeb0a8835f0c1dc2414385b88f3e2c7f7026c5bb60b8` |
| Members | 379/379 regular, each length + SHA-256 equal to the manifest from the tar; 0 unsafe/extra; re-verified after the work |
| Product pins | 330/330 equal; none unpinned |
| Parent | `parent-inputs.json` equals **my own** verified extraction of frozen 113; 327 unchanged, 0 added/removed |
| Changed | `trust.rs` `b66f1553…9983` · `platform-admission-cases.ndjson` `265332dc…2a72` · `recovery-cases.ndjson` `5d2e6bdb…476b` |

Production delta, complete: the five-line `fsType` type check returning `Err(PlatformError::Observation)`
is **removed** and its comment replaced by the real rule ("cannot match the admitted set and receive
the same fixed refusal"). Test delta: `assert!(count > 500)` → `assert_eq!(count, 586)`; `1031` → `1037`.
`trust_time.rs` and `revocation.rs` are unchanged (pins).

Both fixture files contain their 113 bytes as an exact **byte prefix** (1,031 → 1,037 and 584 → 586
lines); nothing inherited was rewritten.

## 2. Evidence

- **New expectations recomputed from my verified reference107**: all 6 platform cases equal
  (64-emoji selector echoed, 65-emoji selector null, `fsType` ∈ {false, 7, [], {}} →
  `NT-TCB-BOOT:INSTALL_ROOT_FS` with the platform retained); both recovery cases equal
  (`createdMono = i64::MAX` with wrapped expiry → `PENDING_SHAPE`; the maximum exact window
  `MAX−86400 … MAX` passes the gate and reaches `CHALLENGE_CONTINUITY_MALFORMED`).
- **Scratch build**: security 64 passed / 0 failed.
- **My 112 corpus re-run on 114**: platform 15,607 of 15,611 representable cases projection-identical
  to 107 (112: 15,438); the remaining **4** are exactly the non-object observations (`null`, `[]`,
  `"x"`, `7`), which is the class rule now written in `diagnostic-map.json`. Recovery: all 855 results
  identical to 112 — the change did not move anything else.
- **Mutation** (all compiled, baseline green):

| Mutant | Result |
|---|---|
| old typed `fsType` error restored | killed |
| non-string `fsType` coerced to `apfs` (admission) | killed |
| selector bound counts bytes | killed (112 survivor) |
| window `wrapping_add` | killed (112 survivor) |
| recovery fixture truncated by two lines | killed — by the exact count (N-3) |
| window `saturating_add` | **survived** |

## 3. Closure

| 112 finding | Status |
|---|---|
| N-1 undocumented `fsType` divergence from 107 | **Closed** — Rust now returns 107's decision; comment states the real rule |
| N-2 two surviving mutants | **Closed** for both named mutants |
| N-3 inexact recovery count | **Closed** |
| N-4 mapping stated per fixture, not per class | **Closed** — two class rules, explicitly "not an admission override" |

## 4. Finding

- **N-1 (low, tests)** — `saturating_add` survives. It differs from `checked_add` only for
  `createdMono > MAX − 86400` with `expiresMono == MAX`: a window shorter than 24 h passes the gate.
  Measured on three such cases (`probes/recovery-sat.*`): frozen code `PENDING_SHAPE`, mutant
  `CHALLENGE_CONTINUITY_MALFORMED` — still a refusal, class only, and unreachable for any real
  monotonic clock. One more appended case (`created = MAX−1`, `expires = MAX` → `PENDING_SHAPE`) pins it.

Nothing else. Unchanged limits: one macOS lane; I did not rerun the workspace or a host lane; R-1/R-2/R-3,
104 N-4 and the Linux reading remain open by the owner's own statement.

## 5. Bounded verdict

**114: reviewed, no blocking finding; signed112 N-1, N-2, N-3 and N-4 are closed.** Not approval of any
inherited group, not cumulative approval or selection, and no dependency, OS, release or
current-authority qualification.

Evidence: `claude-out/pin-verification.json`, `product-pins.json`, `probes/fixture-recompute.json`,
`probes/mutation.json`, `probes/recovery-sat.{ndjson,rust}`, `probes/recovery-sat-mutant.rust`,
`probes/platform-mine.rust`, `probes/recovery-mine.rust`, `hashes.txt`.
