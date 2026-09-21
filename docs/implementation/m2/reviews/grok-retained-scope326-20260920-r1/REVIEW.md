# Independent source review — retained-T structural corpus 326

**Standing:** bounded **source investigation** of frozen `retained-scope-investigation-326`. It supplies a **non-vacuous** retained-phase corpus for unchanged 265 `Operation.proof` / 235 known-before / full 227/279 joins, answering 324’s finding that all 19 old restore positives had **zero** T locators. Not a native constructor, census, original-T admission, full-restore-without-T policy, or product installation. Installed product remains `fa72e50`. No native/schema/helper edits in this packet.

Python 3.12.13 `-I -B`. Frozen extract reports restored; independent rerun in `grok-out/probe-live`. 324 REVIEW+ADDENDUM and 325 REVIEW were not edited.

Pins **before** extract: **2864748 B, 650 members, SHA256 `c64ccac15050c08ed9148136d2270c92c1e88c9db4064415f704ea1128f4741e`**. Extract rehashed **650/650**. Nested 324 pin `b7c3a83e…270d` (2848616 / 639) live-equal; `source324/` file count **639**. Packet `review324/REVIEW.md` / `ADDENDUM.md` byte-identical (`9990fb78…b0c0` / `08685351…7694`). 325 REVIEW unchanged (`e9ff6ae4…aabe`).

---

## What 324 left open

324 restore probes: 19 structural positives, **`timeTargets: []`**. That proved “no accidental T read” on a corpus **without** T locators. 325 closed **local-trace** clock-evaluation absent/malformed with actual previous EventRefs. 326 is the restore/279/235 **structural** corpus that actually **carries** `timeEvidence` (and clock-write `evaluation`) NodeRefs.

---

## Independent rerun and target inspection

`check_retained_scopes326.py` rerun from a review-local copy: **24** fixtures / **27** report rows, stdout `non-vacuous T-target checks and required dependencies passed`. Live `probe-report.json` / `fixtures.ndjson` SHA-equal frozen (`1014f844…70ea`).

Independent `build()` inspection (`grok-out/target-inspection.json`):

| Graph | Pairs | Empty events | Capsules | T locators | Clock-write eval | Proof | Absent ≡ malformed | T reads |
|---|---|---|---|---|---|---|---|---|
| `empty-retained-chain` | 2 | `[True, True]` | 3, all `timeEvidence` | **1** (`55…55`) | none | ok | yes, 6 reads / `[6,7,18654]` | **0** |
| `clock-retained-chain` | 2 | `[False, True]` | 3, all `timeEvidence` | **2** (`55…55` + `aa…aa` evaluation) | yes, `kind: kept` (no proof) | ok | yes, 7 / `[7,8,19428]` | **0** |
| `longer-retained-chain` | 4 | `[False, True, True, True]` | 5, all `timeEvidence` | **2** (same two hashes) | yes | ok | yes, 9 / `[9,12,28738]` | **0** |

Every adjacent pair was passed to **full** `admit_shapes_and_joins(after, d, real before)`. Empty pairs take 279’s extra empty-event before guards; nonempty pairs still run 279’s common phase/role/head/projection checks (no weaker nonempty subset). `Operation.proof` uses reconstructed `cur` as 235 before, not current C roles, not 272 DFS. Standing `structural-restore-and-event-bindings-only`.

**Non-vacuous:** target sets are nonempty; assertions require that; reads never include those hashes even when malformed bytes sit at the declared digest. This is “unrequested locators are not followed,” not validation of T contents. Placeholder digests (`55…` cloned from the 279 empty-event before image; `aa…` from 274 `original-1` evaluation) are still real NodeRefs on every capsule / clock-write.

---

## Required non-time losses and before-owner split

**15** missing-required refusals (`operation-capture-cap`, `failed` latch): observed image, proven image, first child descriptor, direct terminal, operation record × 3 graphs. **3** `witness-is-recovery-operation` when the terminal’s action is restore-recovery even though original proof bytes exist. **3** known-before mismatches at the **correct** owner: empty graph → 279 `empty-event predecessor binding`; clock graphs → 235 `event-chain` (wrong `eventHead`). Missing T does not license a wrong before or a restore terminal.

Generator setup: first `timeEvidence: {kind: keep, proof}` refused `TrustEventV1` shape; schema is `kind: kept` with **no** proof for a non-`lastAccepted` write. Corrected generator only (`before-kept-shape-fix.py`). Helpers/schema/verdicts unchanged.

---

## Does this close the 324 corpus gap?

**Yes, only** the **structural** gap: 265 `Operation.proof` + full 279 adjacent pairs + 235 known-before on retained-phase graphs that **actually declare** T/evaluation locators, with absence ≡ malformed-present and required non-time still unavailable.

**Not closed (and not honestly claimed by README):**

- Nested restore proofs that **carry** T (existing 278 nested cases are not this corpus).
- Live 222 complete-bucket census / custody / fence / unreadable / foreign names.
- Original T **admission** (S4 replay, signatures, TCB).
- Owner policy that full restore may skip original time proof of N.
- 325 local-trace scope (already separately non-vacuous for clock evaluation).
- Optional `commandOutcome`, cross-store continuity intent, creation marker.

Opaque heads/history/metadata in these fixtures are not reachable lifecycle grants.

---

## Verdicts

- [x] **326 as non-vacuous structural T-bearing corpus:** archive verified; 324/325 reports preserved; independent rerun 24/27; nonempty targets; zero T reads; 279 real-before; missing non-time and non-direct terminal refuse; before mismatch at 279 vs 235 correctly split.
- [ ] **Not** native census, original-T validity, nested-T restore coverage, full-restore-without-T selection, or product installation.
