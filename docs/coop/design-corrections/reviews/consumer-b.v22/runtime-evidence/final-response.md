Generation 22's review is finished. The final from-scratch command ran after my last edit, all 53 stages exited 0, and it gave **ACCEPT-RECONSTRUCTABLE**. That verdict is my own reconstruction only. No root result was supplied, so none is claimed, and nothing here qualifies a host, OS, compiler or product. All compiler, provider and host observations are synthetic inputs I wrote.

**Deliverables:** `output/blind-review.md` and `output/blind-review.json`. The command's record is `output/verify-all.json`, with an identical copy that later runs never overwrite in `output/notes/v22-stage-io/20260912T124904/`.

## What was measured
- **Input kit:** all 102 files verified. Exactly one file changed from generation 20: `foundation/atom-evaluation-contract.v1.md`. The supplied delta inventory was checked against both sides rather than taken on trust.
- **Atom contract:** the atom evaluator didn't follow the new section 4 rules (V22-D2). While re-reading I also found an older bug: a runtime row marked "observable but not hit" was counted as a hit (V22-D3).
  - All five Runs were rebuilt, re-exported, closed, replayed in a separate process and put through their 14 tamper controls each. All replays match.
  - Findings went from 3 to 8 for rust and from 4 to 3 for typescript.
  - A separate checker that doesn't import the evaluator accepts all five Runs and rejects all five generation-20 copies, plus all four tampered copies.
- **Every requirement re-checked from its final files:** 126 pass. The other 5 are deliverable checks, which pass once the review is written. Each check records what kind of evidence it actually is (re-derived result, schema re-validation, re-run control, and so on); a string comparison or presence check never counts. Status: 131 executed, 3 future host-qualification items.
- **Query and mutation surfaces:** 20 query operations with real request/response records (110 checks, 0 failures, 8 negative controls). The mutation surface passes 29 checks and all 7 of its negative controls are rejected; the audit re-validates its retained records.
- **Design issues:** 0 MUST, 0 SHOULD, 1 advisory.

## Defects I found in my own earlier work (all corrected, old bytes kept)
- **V22-D1:** the generation-20 rebind rewrote a label inside a historical generation-19 sentence. Restored from the saved copy.
- **V22-D4:** the old status script marked some requirements done based on file presence, counts, a generation-16 note, or a hard-coded `True`. Status now comes only from the audit.
- **V22-D6:** the mutation replay-scope keys were hashed over records the schema rejects.
- **V22-D10:** several artifacts I reported as positive weren't what they claimed:
  - two "quotes" that weren't the kit's exact text;
  - a count field that read 0 when facts existed;
  - negative controls missing their first refusal, masking record or classification;
  - a mislabelled detector field;
  - a repair/test authorization requirement that was only a table of names. It now has records that pass their schemas, with seven controls that are rejected.
- **V22-D8 / V22-D11:** some stages read the *previous* command's outputs. The phase-4 stages had run before the Runs were rebuilt in every generation from 16 to 20, and phase 0 read old status files. Stages are reordered, and every stage now runs under a hook that logs each file it reads or writes; the command fails on any stale or undeclared read.
- **V22-D13:** the schema checker crashed on a selector that points into another document.
- **V22-D12:** the generation-20 report claimed reproducibility using diagnostic scripts that were never exported. That claim is not repeated.

The earlier failed runs of this generation (A and B, six failed stages each) and the two clean runs superseded by later edits (C and D) are recorded in `output/notes/v22-command-attempts.json`.

## Limits of this result
- **Synthetic-only atom cases:** incoming-direction atoms and endpoint=target atoms appear in no retained Run, so they are tested only on labelled synthetic models. No Run has an atom filter, an imported count-at-most atom, or a staleness check by revision.
- **Read log:** reads by child processes (Run builders and replays) aren't logged; their writes are.
- **Reproducibility:** results were not re-compared across separate commands this generation.
- **Open history:** generation 17's overwrite of two generation-16 files remains an open, disclosed item.
- **Nothing executed or changed:** no repair was applied and no test or native preparation ran. There were no kit or product edits and no commit or push, and all writes stayed under the generation-22 runtime.
