The self-audit is finished and the verdict is **CHANGES_REQUIRED**. That rests only on the carried kit finding s39-M1: native U-4b assigns no tsjs `unitKind`, yet `UnitMembershipV1` enters the PlanId. Two schema-valid spellings of one unit mint different membership digests (`34d0e48f…` vs `52a0e505…`). No new normative owner was supplied, and I did not invent the mapping. All other stop conditions now hold; this is not an acceptance.

**What the audit found in my own earlier work.** Output construction and closure validation were not separated.
- My source39.v1 closure never checked the typed-prefix output references (finding3, subject3, finding-key2) before replay. It only compared the evaluator's own emitted objects.
- The evaluator also only exported subject descriptors for subjects that produced a finding.
- So all 27 v1 "positives" were missing descriptors that composition §7 requires, and v1 still admitted them. That was my defect, not the kit's.

I built a separate retained-graph validator (`ref/retained_graph.py`) that works from the kit's schemas and registries only. It reads just the exported blobs, never the emitter's object table, and closure runs it after owner admission and before replay. Corrections HC-33..HC-38 are recorded in `tools/hc_v2.py`, with original failures preserved. HC-37 and HC-38 were made in this runtime: the validator had been admitting two mutations only owner admission refused (an unselected evaluation import, and a non-derived `unitId`).

**Measured on the final exports:**
- **Closure matrix (fresh processes):**

  | Code \ bytes | v1 stores | final stores |
  |---|---|---|
  | old code | 27/27 admit | 27/27 admit |
  | corrected code | 26/27 refuse (`cmp-empty` references no subject, so its bytes never changed) | 27/27 admit |

- **Identities:** all Run, proof, evidence and seal identities are unchanged; the only byte change is the added subject descriptors.
- **Positives:** all 27 pass owning-schema admission, owner graph admission, the independent validator, replay and reachable-set equality. The replay export for all 27 has byte-equal proofs, identities and 520 witnesses. The review lists each positive's `runId` and store SHA-256.
- **Negatives:** 32 were built, one per applicable retention/reference class from the kit census; all pass and record first refusal and masking.
  - 11 are refused first by the new validator where owner admission sees nothing. Under the old code, one of those (missing subject descriptor) was admitted and the rest were caught only at replay.
  - 3 classes appear in no constructed Run, so they have no negative and are not claimed.
- **Replay-all:** 62 stores. The validator agrees on 10 of the 33 refusals. The other 23 are owner-level laws it deliberately leaves to owner admission; they are listed as a limitation.
- **Other controls:** all tamper controls are refused, graph query ran 53 vectors and run termination covered 28 Runs, each with 0 failures. Custody passed at start and end.

**Completing the work here.**
- This runtime started from an exact copy of v2's output. The steps v2 never ran are now done: replay export, final run termination, negatives, provenance, checkpoints and review.
- Results that don't touch the closure (store builds, phases 1–4 and 6, discovery, phase-8 compare) are reused from v2. The mtime evidence and ledger are in `notes/12-v3-completion.md`.
- Everything that depends on closure was re-run here after HC-37/38.
- All 131 IDs are executed with none failed, and checkpoints 0–11 are written. The v2 runtime is byte-unchanged.

**Failed attempts, kept:**
- My rebind script rewrote its own constants; the executed bytes are restored.
- The first negatives attempt didn't re-sort records correctly.
- The first checkpoint-9 write failed two IDs because the new files lacked `firstRefusal`/`masksLater` and classification fields; they were re-emitted.

**New advisories, nonblocking:**
- **A-v2-1:** the kit doesn't say whether typed values inside workflow input documents are closure references. A literal reading makes lawful Runs like `cmp-empty` unclosable.
- **A-v2-2:** `policy-derivation3` isn't reachable from `run3`.
- **A-v2-3:** identity §3 calls the retention modes "closed" while the native and relation bundles publish more.

**Limitations:** root admission of these exports is unobserved, and future qualification wasn't performed.

Files are in `/private/tmp/opensip-design-corrections/consumer-b.v24-source39.v3/output`:
- `blind-review.md`
- `blind-review.json`
- `requirement-status.json`
- `checkpoints/`
- `notes/`
