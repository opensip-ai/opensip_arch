# Independent bounded review — recovery evidence follow-ups 163 (Rust)

Reviewer: Claude (actual independent reviewer; Codex remains implementation owner). 2026-09-19.
Request: received as a chat message (verbatim in `claude-out/REQUEST-as-read.md`); subject README read. Scope: the
delta of frozen `recovery-evidence-followups-checkpoint-163` over frozen 162 — three `cfg(test)` modules and one
private production change (`LedgerAnchor` construction), answering my 156 T-1/T-2 and 157 T-1/N-2. No join, read,
transaction, dependency or public-facade change; no host mapping. No frozen/selected/product edit; scratch only,
`-I -B`, dedicated targets; no commit, push or delegation; no cumulative approval.

## 1. Subject verification (before use)
| Item | Value |
|---|---|
| `subject.tar.xz` | 4,129,512 bytes, SHA-256 `a17e388a3d0dd854a20631984a53bcd470e945003f20487098266a769d86e3c9` = request = `archive-pin.json` |
| Members | 420/420 regular, length + SHA-256 equal to the manifest, from the tar before extraction; 0 unsafe/extra; re-verified at the end |
| Product pins | 343/343; none unpinned |
| Parent | `parent-inputs.json` = **my own** verified 162 extraction (343/343); 339 unchanged; 4 changed; 0 added |
| Production equality | `bracketed_capture.rs`, `generation_anchor.rs`, `ledger_store.rs`: everything before the `#[cfg(test)]` module is byte-identical to 162. `recovery_snapshot.rs` has no test module — it **is** the production change (§2). All fixtures unchanged |
| Owner checks, fresh scratch | 121/121 security + 37/37 storage tests; strict workspace Clippy clean |

No host receipt is claimed for this delta; I agree a private view-only refactor plus tests does not need one, and I
built and linted the whole workspace here.

## 2. The production change (read in full — 12 lines)
`anchor()` still returns `None` unless the standing is `ContinueCarrier`; it then builds
`LedgerAnchor { capture: self, association: self.association.as_ref()? }` and every getter reads the bound reference.
The `expect` is gone: if the join law ever yields `ContinueCarrier` without an association, the result is "no anchor",
not a panic in a recovery path — exactly 157 N-2. The new field is private; both borrows share the evidence's
lifetime, so the anchor still cannot outlive or be detached from its evidence.

## 3. Evidence (`probes/closure.py`, `probes/compile_boundaries.py`)
**3.1 Closure, executed.** My surviving mutants from 156 and 157, re-applied to this tree:

| Survivor | 163 | Killing test |
|---|---|---|
| 156 T-1 mask-1 witness *before*-slot filled with the after read | **killed** | within-bracket test, now asserting the exact `Judgment` |
| 156 T-1 mask-2 floor *before*-slot filled with the after read | **killed** | same |
| 156 T-1 mask-3 witness slots exchanged (+ my new floor-exchange variant) | **killed** | same |
| 156 T-2 mask-6 a marker on any generation quarantines the requested one | **killed** | valid marker on another generation |
| 157 T-1 retained binding execution copied from the association | **killed** | foreign association body under the requested execution |
| 157 T-1 attempt looked up by the association's execution | **killed** | same |
| new: anchor gating dropped (any captured association yields an anchor) | **killed** | two tests |

**3.2 My 157 physical probe, unchanged, on this tree:** output byte-identical to 157 (standing `UnknownCustody`,
supplied binding retained, no foreign attempt, no anchor, foreign bytes exactly as stored).

**3.3 Privacy / lifetime** (clients in the parent module): **13/13 rejected**, including the two the new field
invites — an anchor literal with a caller-chosen association (E0451) and re-pointing a genuine anchor's
`association` at another candidate (E0616); plus outliving (E0505) and detaching (E0515) the evidence. The three
boundary clients compile as before. (My first edit of this script had a quoting error; preserved as
`compile_boundaries-FAILED-r1.py`.)

## 4. Findings
No defect and no finding of substance.
- **N-1 (note)** `anchor()` now has two independent reasons to return `None` (standing; missing association) and a
  caller cannot tell them apart — fine, because the second is unreachable under today's join law and both mean "no
  anchor". If the join law changes, a test that asserts `ContinueCarrier ⇒ anchor().is_some()` (the 16-combination
  test already does) will flag the divergence rather than hide it. Nothing to do.
- Carried, unchanged and correctly still open: 150 F-2 (host mapping of capture failures), 157 N-1 (un-mirrored
  store/namespace/execution surface as `UnknownCustody`).

## 5. Closure of my items
| Item | Status |
|---|---|
| anchor156 **T-1** inequality-only assertion | **Closed** — exact judgment asserted; all before/after slot mutants killed |
| anchor156 **T-2** marker on another generation | **Closed** |
| ledger157 **T-1** foreign body execution | **Closed** — both mutants killed; my probe's state is now an owner test |
| ledger157 **N-2** `expect` on a cross-module invariant | **Closed** — bound at construction with `?` |

## 6. Bounded verdict
**163: reviewed, no finding of substance. Three test modules and a 12-line private change: the anchor view now binds
its association at construction and cannot panic; it still cannot be forged, re-pointed, detached or outlive its
evidence (13/13). All seven of my surviving 156/157 mutants are killed by real-I/O tests, and my 157 physical probe
gives byte-identical output.** Not approval of host composition, host mapping (150 F-2 remains open), custody or any
cumulative standing.

Evidence (`claude-out/`): `pin-verification.json`, `pins.py` → `product-pins.json`, `diffs/`, `owner/`,
`probes/{closure.py, closure.json, closure.log, compile_boundaries.py, compile_boundaries-FAILED-r1.py, compile-boundaries.json/.log, compile-*.stderr}`,
`io/body-execution.txt`, `hashes.txt`.
