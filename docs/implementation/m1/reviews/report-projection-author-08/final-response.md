The author-08 candidate is sealed and ready for one combined review of the review-06 fixes and the interruption integration. The pinned run passed, and so did strict runs from an exact copy started in the copy, the architecture checkout and `/`. The three strict results are identical, and the pinned run matches them. The run shows 0 child processes and 2069 re-hashed opens.

**Freeze anchor:** `subject-files.json` `4c6b4e70b380c0675ff842f80800654f8b2342fee3a3b31ca42f7a74e848975f`. It lists 20 files; the only new one is `owner/interruption-binding.v1.json`. The closure pins 96 files (11 new, none dropped) and 3 directory listings. Run evidence is in `scratch/closure-evidence.json`, outside the subject.

**Current counts**

| Item | Count |
|---|---|
| Report cases | 194 (30 accept, 29 schema, 15 codec/boundary, 18 envelope host, 48 ledger, 29 graph, 25 other) |
| Envelope cases | 47 (14 accept, 11 schema, 22 host) |
| Aggregate cases | 22 |
| Delivered goldens | 68, over 17 scenarios |
| Coverage rows | 323, valid with no workaround |
| Metadata cases through envelope5 and envelope6 | 43 each, same outcomes |

Three author-07 case ids only made sense under envelope5, so I renamed them rather than dropping them. Their envelope5 outcome is still reproduced by the new "major 5" cases, and the old-to-new mapping is in `contract.md` §5. No other expected outcome changed.

**Interruption integration**
- **Bound exactly:**
  - schema6 is the report envelope. It is `bdd5d270…`, 39969 B; my earlier note of `fd2663c2…` was the subject-05 hash. The check restores it byte-for-byte to the unchanged envelope5 (`45de2b0a…`).
  - The three prose overrides (lines 224-228, 1302-1338, 1340-1349) are bound by before and after sha256.
  - Model line 380 is executed in both its old and new form.
  - The recorded-error, payload, result-kind and skipped-step joins are applied.
  - Both composite delivery entry points (`validate_interruption_delivery`, `validate_preplanning_delivery`) run on every interruption golden.
- **Delivered goldens** (status "delivered in candidate, pending joint review"), each produced by the real owner model and admitted by the envelope6 schema, the composite entry point with the native availability projector, and report host admission:
  - 36 builtin scenarios (12 variants × 3), giving 144 renderer rows;
  - 9 before-planning carriers (32 renderer rows);
  - 3 profile cases where only the new model keeps an optional analysis Run;
  - the 8 former pending empty-error goldens, now delivered. The analyze rows use the plannable primary steps, because import is not plannable (P01).
- **154 negative controls** (omitted or invented availability, erased Run, invented or omitted detail, selection on a step that never started, dropped selection, major 5). Three of them are refused only by the composite entry point, which shows why it is mandatory.
- **New host rules:**
  - an interrupted carrier must carry the last committed Run if one exists, otherwise be a failure with no Run;
  - commands with the availability parity duty must carry availability even before any Run.
- **C01 and C02** are marked "implemented in candidate, pending joint review". They stay M1 blockers, and envelope5 is still unaccepted.
- **Settled behaviour:** D9 aggregation and metadata compatibility are unchanged.

**L02 capacity (open, M1 blocker)**
- **Regression:** it runs the real native functions. The 4,167,140 B analysis-spec produces a schema-valid availability account of 4,231,826 B; with two steps it is 8,463,605 B. The composite join and host admission accept the full envelope, and the exact 4 MiB codec refuses it with `BYTE_LIMIT`. Truncated, empty or omitted accounts are refused.
- **What the owners say:**
  - workflows 226: interruption before settlement exits 130;
  - workflows 238: the settled ordering does not rank interruption;
  - workflows 1135 and 1147: a missing required field or a failed required renderer exits 4;
  - projection contract 123: output overflow is a serialization failure, exit 4.
- **Precedence:** no owner orders 130 against those failures for the interruption carrier's own output, and no bounded correction follows from existing text. L02 stays open with the issue's closure criteria, and nothing is truncated, emptied or given invented precedence.

**Still open**
- **Q-FIT-1 (new question for the joint review):** an interrupted fit run carrier currently omits the candidate-list report rather than inventing one. No owner text requires or forbids it there.
- **Integration duties:** rebasing metadata, CLI, generated sources and the registry; host custody of the request context and retained selections; calling the entry points at every real delivery boundary; renderer parity; L02.
- **Separate owners:** all 11 feature owners stay separate, and none of the author-02 or root proposal bytes were adopted. P01 and X01 remain M5 blockers.

I re-hashed report subject-07 (20 files), interruption subject-07 (51 files) and the trial copy; all are unchanged. The architecture checkout shows only its earlier edits that aren't mine. There is no runtime, browser, M1 or whole-project approval claim.
