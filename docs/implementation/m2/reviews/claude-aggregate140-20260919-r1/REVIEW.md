# Independent bounded review — aggregate test follow-ups 140 (Rust)

Reviewer: Claude (actual independent reviewer; Codex remains implementation owner). 2026-09-19.
Request: `aggregate140-20260919-REQUEST.md`. Scope: the delta of frozen `aggregate-followups-checkpoint-140` over
frozen 139 — test-only changes closing my aggregate136 T-1, T-2, T-3. The owner states production bytes are unchanged
and that no isolated-host repeat was made for a test-only change; I check the first and record the second. No
authority, OS, entropy-distribution or cumulative claim. No frozen/selected/product edit; scratch builds, dedicated
target dirs; no commit, push or delegation.

## 1. Subject verification (before use)

| Item | Value |
|---|---|
| `subject.tar.xz` | 4,017,428 bytes, SHA-256 `80538cc06467342f8d5725137e4b984acc389dcb922ca363b57cfc601adba253` = request and `archive-pin.json` |
| Members | 358/358 regular, length + SHA-256 equal to the manifest, from the tar before extraction; 0 unsafe/extra; re-verified clean at the end |
| Product pins | 330/330 equal; none unpinned |
| Parent | `parent-inputs.json` equals **my own** verified 139 extraction (330/330); 329 unchanged; only `trust.rs`; no fixture change |
| Host receipt | none in this subject, as disclosed — the 139 host85 run covers the identical production bytes (next row) |
| **Production bytes** | With every `#[cfg(test)] mod … { … }` block removed by my own brace-matched stripper, `trust.rs` of 139 and 140 are **byte-identical** (138,227 bytes, SHA-256 `b5500f41…ea74f5`; 17 test modules stripped from each, same module list). All changed hunks lie inside `chain_tests`, `challenge_tests` and `platform_tests` |

## 2. Evidence
80/80 security tests; strict workspace Clippy clean. The 26-line diff read in full:
- *chain test*: walks `previous_digest` from the anchor and asserts `continuity().root_digest() == previous` for each
  link, then advances to the link's own root — continuity is now distinguished from possession by **which root it is
  under**, not by the (shared) message;
- *challenge test*: a second **production** `issue_recovery_challenge` call on the same inputs; nonces differ, neither
  equals the fixture constant `ab…`, and the second proposal's pending/exported join and pending admission are checked;
- *platform test*: `expected_observation` is cloned **before** the caller's buffer is nulled (line order checked), and
  `observed()` must equal it afterwards.

**Discrimination** (`probes/mutation.py`): my three mutants that **survived** 136 are re-run unchanged and are now
**killed** by exactly the tests above. Three variants are killed as well: the *mirror* getter (`possession()` returning
continuity — so both directions are pinned, not just the one I reported); a constant nonce that is **not** the
fixture constant; and a nonce hashed from a fixed string, which *looks* random and passes any format check but never
changes. **6/6.**

## 3. Closure of aggregate136

| Item | Status |
|---|---|
| **T-1** `continuity()` unpinned | **Closed** — and its mirror |
| **T-2** `observed()` unpinned | **Closed** — exact equality after the input buffer is dropped |
| **T-3** production entropy source unpinned | **Closed as a wiring assertion** — any constant or deterministic source is killed. As the owner says, this is not a statement about distribution or the OS source: a generator returning `counter++` would pass. That is the right scope for this test; quality of the source belongs to platform qualification |

## 4. Findings
None.

## 5. Bounded verdict
**140: reviewed, no finding. Production code outside the test modules is byte-identical to 139 by my own comparison;
the three 136 test gaps are closed and discriminate — my three survivors and three variants are all killed (6/6).**
Test-only successor; no isolated-host repeat (disclosed). Not approval of entropy quality, callers, custody, OS,
release or any cumulative standing.

Evidence: `claude-out/pin-verification.json`, `product-pins.json` (incl. the production-bytes comparison), `trust.diff`,
`owner/`, `probes/{mutation.py,mutation.json,mutation.log}`, `hashes.txt`.
