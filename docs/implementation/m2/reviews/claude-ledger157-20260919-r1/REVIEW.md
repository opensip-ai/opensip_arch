# Independent bounded review — owned ledger recovery evidence 157 (Rust)

Reviewer: Claude (actual independent reviewer; Codex remains implementation owner). 2026-09-19.
Request: `ledger157-20260919-REQUEST.md` (bytes as read: `claude-out/REQUEST-as-read.md`); subject README read in full.
Scope: the delta of frozen `ledger-evidence-checkpoint-157` over frozen 156 — `storage/src/ledger_store.rs` and the new
child `ledger_store/recovery_snapshot.rs`: a sealed `CapturedLedger` and a gated, borrowed `LedgerAnchor`. Supplied
path and binding remain caller context; this is **not** commitment, custody, current authority or the composed proof,
and I infer none. No frozen/selected/product edit; scratch only, `-I -B`, dedicated targets; no commit, push or
delegation; no cumulative approval.

## 1. Subject verification (before use)
| Item | Value |
|---|---|
| `subject.tar.xz` | 4,198,824 bytes, SHA-256 `10ddefc12638465cf34f70bcf43dc50ca661982607d79f4f9c72686bb77fbe46` = request = `archive-pin.json` |
| Members | 428/428 regular, length + SHA-256 equal to the manifest, from the tar before extraction; 0 unsafe/extra; re-verified at the end |
| Product pins | 342/342; none unpinned |
| Parent | `parent-inputs.json` = **my own** verified 156 extraction (341/341); 340 unchanged; 1 changed, 1 added |
| Edges | `crates/storage/Cargo.toml` dependencies unchanged; no `security` dependency; nothing new is `pub` beyond `pub(crate)` |
| Host pins | host99 receipt: 222 sources all equal the product pins; no command failed |
| Owner checks, fresh scratch | 36/36 storage tests; strict workspace Clippy clean |

## 2. What it is (read in full)
`capture(snapshot, binding)` performs the three existing reads on the caller's one `ReadSnapshot` — `read_pair`
(definition check, both rows, the four association mirrors), `load_attempt` — runs the unchanged `join_ledger`, and
seals binding strings, both parsed candidates (with their exact `raw` bytes), the attempt and the standing. `anchor()`
exists only when the standing is `ContinueCarrier`; the anchor is a borrow of the whole evidence and reads generation,
journal sequence, journal digest, operation, run and commit sequence from the **joined association**. `read_recovery`
opens, captures and drops the snapshot; `ReadSnapshot::recovery_ledger` keeps the caller's transaction.
The `.expect("ContinueCarrier requires a joined association")` is sound today: `join_ledger` yields `ContinueCarrier`
only in its `(Some, Some)` arm (N-2).

## 3. Evidence
**3.1 Privacy** (`probes/compile_boundaries.py`, clients in the parent module): **12/12 rejected** — evidence literal
with a chosen standing; upgrading the standing; writing through `standing()`; splicing another association; an anchor
literal over evidence that is *not* `ContinueCarrier`; an anchor outliving its evidence (E0505) or returned without it
(E0515); `Clone`; `Default`; writing through `receipt_bytes()`; mutating the attempt through its getter; a
parent-written forging impl. Three compile and mark the line: a bare `LedgerStanding::ContinueCarrier` is a plain enum
value (it cannot enter evidence — same rule as 150 N-1: consumers take `&CapturedLedger` / `LedgerAnchor`, never a bare
standing); capture runs with any caller-supplied binding; read-only use of anchor plus evidence.

**3.2 Mutants** (`probes/mutation.py`, 9, complementary to the owner's eight; all compiled; baseline green): 7 killed by
the owner's tests (carrier taken from the association; anchor digest = receipt digest; run/operation exchanged;
receipt bytes falling back to the association; anchor whenever both rows exist; anchor withheld while settlement is
pending; namespace dropped). **2 survive — T-1.**

**3.3 A physical state the owner's tests do not build** (`probes/rust_probe.rs.txt` → `io/body-execution.txt`): an
association row **filed under execution b whose body is execution c's association**. The frozen DDL accepts it;
`read_pair` does not mirror store/namespace/execution against the body (it mirrors sequence, carrier, generation and
journal sequence), and `join_ledger` answers `UnknownCustody`. On the real database the sealed evidence says: standing
`UnknownCustody`; retained binding execution = the **supplied** one; **no attempt** (an admitted attempt exists only
for the foreign execution c and is correctly *not* exposed); no anchor; association bytes = the foreign body, exactly
as stored. Correct on every point.

## 4. Findings
- **T-1 (low) — two evidence-integrity regressions pass all 36 tests; §3.3 catches both.**
  | Surviving mutant | Effect in the §3.3 state |
  |---|---|
  | retained binding `execution` copied from the association when present | evidence reports execution **c** as "supplied" |
  | attempt looked up by the association's execution | evidence exposes the **foreign** execution's admitted attempt |
  Neither changes the standing (the join refuses first), which is why the 16-combination test cannot see them; both
  falsify what the evidence says was *asked* and *found*. One real-SQL case (row key ≠ body execution, attempt present
  only for the body's execution) pins them.
- **N-1 (note, pre-existing, now more visible)** `read_pair` leaves store/namespace/execution un-mirrored and relies on
  `join_ledger` to refuse. That is sound, but it means a *physically inconsistent row* surfaces as the conditional
  standing `UnknownCustody` rather than as the `Configuration("association_index")` error the other four mirrors give.
  With evidence now retained for host composition, the host should know both shapes mean "this ledger row is not
  usable", and the retained association bytes in that case are the foreign body — evidence of the inconsistency, not of
  the supplied execution.
- **N-2 (note)** The `ContinueCarrier ⇒ association present` invariant is enforced in `recovery.rs` and relied on, by
  `expect`, in `recovery_snapshot.rs`. Establishing it where the evidence is constructed (or returning `None` from
  `anchor()` when the association is absent) would keep a future change of the join law from becoming a panic in a
  recovery path.
- **N-3 (note)** `attempt()` returns `&AttemptRecord` whose fields are readable by the crate; it is immutable through
  the getter (client rejected), which is what matters.

No behavioural defect found. I did not re-derive the WAL-release property independently: the owner's test forces a
write and a `TRUNCATE` checkpoint while the evidence is alive and their `forget(snapshot)` mutant is killed by it; I ran
that suite (36/36) and read the test.

## 5. Bounded verdict
**157: reviewed, no blocking finding and no behavioural defect. Evidence is built only from one `ReadSnapshot` by the
existing readers and the unchanged join; it cannot be forged, upgraded, spliced, cloned or defaulted, and an anchor
cannot be made for a non-`ContinueCarrier` result or outlive its evidence (12/12). In a physically inconsistent
row-key/body state the evidence is exact: supplied binding retained, no foreign attempt, no anchor. T-1: two mutants
that falsify the retained binding or expose a foreign attempt pass the owner's tests because no test builds that
state.** Not approval of binding/path custody, the composed proof with the security owner's `AnchorAssessment`,
current authority, or any cumulative standing.

Evidence (`claude-out/`): `pin-verification.json`, `pins.py` → `product-pins.json`, `diffs/`, `owner/`,
`probes/{rust_probe.rs.txt, compile_boundaries.py, compile-boundaries.json/.log, compile-*.stderr, mutation.py, mutation.json, mutation.log}`,
`io/body-execution.txt`, `hashes.txt`.
