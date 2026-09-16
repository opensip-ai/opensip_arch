# PS-01 / PS-04 revision 2 — all eight issues resolved

v1 is immutable (19/19 hashes verified) and copied here as `v1-baseline/`. Frozen25 (12869 members, 0 mismatches) and the nine frozen planning inputs are unmodified.

---

## 1. Manifest self-reference — resolved by excluding exactly one path

Took your first option. `assetManifestPath` stays under `assetRoot`, is **forbidden as an asset row** (`MANIFEST_SELF_LISTED`), and completeness now reads "every regular file under the asset root **except exactly that one pinned path**" — exact path equality, never a prefix or filename pattern. Coverage stays total: every byte is covered either by a row's digest or by the manifest's own independent pin, and the self-referential digest cannot arise.

Executed against a **real temporary release tree** (`check_report_asset_fixture.py`) — builds files, emits the manifest, computes the pin, reads back: **12/12**.

```
ok  accepts-a-well-formed-release-tree        -> None
ok  rejects-a-mutated-manifest-byte           -> manifest-digest-mismatch
ok  rejects-a-truncated-manifest              -> manifest-length-mismatch
ok  rejects-a-mutated-member                  -> member-length-mismatch:report/app.js
ok  rejects-an-equal-length-mutated-member    -> member-digest-mismatch:report/app.js
ok  rejects-an-extra-unlisted-file            -> EXTRA_UNLISTED_FILE:report/extra.js
ok  rejects-a-listed-file-that-is-absent      -> LISTED_FILE_ABSENT:report/style.css
ok  rejects-a-self-listed-manifest            -> MANIFEST_SELF_LISTED
ok  rejects-a-wrong-asset-root                -> manifest-outside-asset-root
ok  rejects-a-manifest-outside-the-asset-root -> manifest-outside-asset-root
ok  rejects-a-symlinked-member                -> SYMLINK_UNDER_ASSET_ROOT
ok  rejects-an-unsupported-projection         -> projection-incompatible
```
`everyFileCoveredOnceByRowOrPin: true`, `manifestIsListed: false`. No browser or release qualification claimed.

## 2. Optional-surface failure — no longer resets the outcome

The law is workflows §8 lines 230–232: the aggregate is over **required steps only**, and an optional step's failure *never changes the aggregate*. Line 844 and the line-990 golden are instances whose underlying aggregate was already success — neither licenses a reset. Demonstrated:

| underlying required class | exit before | exit after optional asset failure |
|---|---|---|
| success | 0 | **0** |
| policy-failed | 1 | **1** |
| indeterminate | 3 | **3** |
| operational-failed | 4 | **4** |

`v1WordingWouldHaveResetTheseToZero: [indeterminate, policy-failed, operational-failed]`. Required delivery stays separate: a *required* fault still dominates policy-failed → exit 4.

## 3. Digest recipe — reordering claim withdrawn

You were right. `canonical()` is `json.dumps(..., sort_keys=True, ...)`, so input key order is not observable. The control now **imports the frozen canonicalizer** (`foundation/canonical.py`, sha `d47f25db0fb09ceb…`) instead of a stand-in:

- `inputKeyOrderIrrelevant: true` — two differently-ordered inputs give one digest
- `addRemoveRenameChangesDigest: true` — add/remove/rename are genuinely different
- `rawDigestIsNotFramedIdentity: true` — raw `1131162e…` vs framed `identity()` `22b89e84…`, so "mints no H-domain" is now proven from the real code rather than asserted
- the canonicalizer's own `parse()` refuses duplicate keys, floats, negative zero and over-range integers

## 4. Floors — split three ways

The v1 sentence was too broad and did contradict A5. Now: an **authorized S9 transition** keeps S9 exactly (migration copies floors forward; rollback sets the maximum of both stores; only S4.5 lowers a poisoned floor). A **fresh installation** has no predecessor. An **evidence-bundle restore or portable adoption** allocates its own identity, restores no trust floor and grants no local authority — and that rule explicitly *does not touch* the migration carry-forward. A11 also records that a restore keeps floors, so nothing here lowers one.

## 5–7. Record redesigned: per-triple node, not per-attempt row

This single change dissolves all three issues.

`StoreLineageNodeV1` is keyed by the admitted triple `(storeInstanceId, storeGeneration, stateSchema)` and written **only after** the journal record is durably `COMMITTED`.

**(5) Aborted vs active.** An aborted attempt writes nothing, so nothing can be misread as lineage; its retained evidence is the owner's own ABORTED journal footprint. The v1 rewrite-vs-discard contradiction disappears. Recovery is now **total over all six** owner states, and `PREPARED` records the owner's core-operation ABORT with `companionAction: none` — a missing node there is *expected*, never a quarantine.

**(6) core-rollback.** Node-writing is derived from the intent's own values, because S9.2 publishes no store rule for `core-rollback`:

```
[5,1] unchanged          writesNode=False  core-repair
[5,1] unchanged          writesNode=False  core-update, schema unchanged
[5,1] unchanged          writesNode=False  core-rollback, schema unchanged
[4,1] ancestor-reselect  writesNode=False  core-rollback, schema retreats
[4,1] ancestor-reselect  writesNode=False  store-rollback
[6,2] forward-selection  writesNode=True   store-migrate
[6,2] forward-selection  writesNode=True   core-update, schema raised
```
Same-store and ancestor-reselect are now distinct, and neither mints a fresh identity.

**(7) Retry.** You were right that a byte-identical intent can recur: after an abort the core generation is unchanged, so `preconditionGeneration` and all 11 members reproduce. Executed trace: attempt-1 aborts at PREPARED writing no node; attempt-2 with the *same* `intentDigest` is admitted, commits, writes `(z…,6,2)` — `primaryKeyCollision: false`; attempt-3 replaying after the commit is refused by the **owner's own** `TRANSITION.CURRENT_STORE_MISMATCH`. No private attempt counter and no new public field.

**Atomicity is no longer claimed.** Fixed order: journal `COMMITTED` durable first, then the node. The node is **derivable** from the journal's own from/to members plus the two store-root markers, so a one-sided footprint reconciles by reconstruction (`reconstructedFromCommitted: true`), an unreadable marker quarantines, and an ABORTED journal reconstructs nothing. An UNDETERMINED barrier follows security v8 §5.6: refuse further effects, reopen, reconcile, never assume.

## 8. Normative S9.3 owner patch

`patches/security-and-lifecycle.md.S9.3.patch` — **one hunk, +62/−0**, inserted between S9.2 and S10, removing no line, so it three-way merges cleanly with the carrier author's S1/S6/S9/WA13 edits. `94428 B / 12dcebea…` → `98652 B / c0e8153e…`. The control asserts single-hunk, zero removals, and that no closed record is widened.

**Not expanded:** no core release manifest authored. The CORE catalog/manifest shape is recorded as *not provided by candidate25 and unassigned* — explicitly **not** the grant-journal carrier author's work, who owns carrier format and recovery, not release distribution.

---

## Deliverables and evidence

| File | v1 → v2 | Patch |
|---|---|---|
| `implementation-boundaries-and-build-plan.md` | 82985 → 85756 B | 4 hunks, +59/−18 |
| `store-instance-lineage.v1.json` | 30224 → 35761 B | 8 hunks, +272/−217 |
| `report-asset-binding.v1.json` | 22929 → 27714 B | 6 hunks, +40/−7 |
| `security-and-lifecycle.md` (frozen25) | 94428 → 98652 B | 1 hunk, +62/−0 |

Eight of nine planning inputs byte-identical to frozen. Both generated plan blocks byte-identical to the frozen input — no collision with the CR-19 F32 pass. JSON valid with no duplicate keys, no trailing whitespace, no tabs, no broken links.

**All five controls PASS**: both planning checkers unchanged (198 paths; 320 mappings, 38 cases), `check_store_instance_lineage` (4 executed properties), `check_report_asset_binding` (17 vectors + the optional-failure property), `check_report_asset_fixture` (12/12 on a real tree). Focused only; no evaluator suite.

## Limitations

Proposed, unaccepted, unfrozen — I do not accept my own corrections and another substantive review on newly frozen bytes is required. No product code; all named modules already exist in the inventory, so no inventory row and no generated-section change, and both companions are planned architecture sources rather than product inventory files. The digest property uses the exact frozen canonicalizer, but the node, retry and reconciliation rules remain **models**, not carrier tests; the asset fixture is temporary-filesystem evidence, not a release build or browser test. Whole-install-root substitution stays undetected — frozen25's existing stated bound. S9.2 publishes no store rule for `core-rollback`, so the derived cases must be rechecked if the owner later publishes one. COV-03 and the separately active carrier work remain open, with the required join named rather than assumed.
