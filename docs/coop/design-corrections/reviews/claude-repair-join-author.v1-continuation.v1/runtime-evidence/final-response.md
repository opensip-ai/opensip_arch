I've fixed both defects root found in the evaluator3 repair preview owner. A wrong or substituted Run ID is now refused before any descriptor is built, and a foreign exception that shares the owner's class name now propagates as the same object instead of being mapped to unavailability. The whole workflow checker still does not pass: the known unrelated oc2 grammar failure remains in every run, and I haven't fixed or relabelled it. This is author work only and still needs the later independent final-source review.

**Recovery of the interrupted jobs.** The four jobs from my earlier status-only turn never completed: they left no receipts, only empty stdout/stderr files. I kept those under `interrupted/` in this runtime and ran all four again here as new, separately labelled runs, finishing within this turn. Nothing is still running. Completed results from the original runtime were copied here with per-file hashes. A final check confirmed the original runtime, root's probe files, root's captured source and my earlier reviews are all unchanged.

**The change** touches four files, as a 218-line diff (sha `b7c04ff8…`) against root's captured source:
- **`workflows_model.v3.py`**:
  - `repair_preview` now refuses (`REQUEST.PRECONDITION_FAILED` / `REPAIR.EVIDENCE_RUN_UNAVAILABLE`) unless the request's `runId` equals identity-model.v3's own `identifier('run', …)` of the retained Run. This check runs before the target join and before the shared builder.
  - Both places that turn a missing retained record into that refusal now match only the owner's declared exception classes, by exact class identity. The name comparison is gone, and anything else propagates.
- **`repair_closed_world_selection.v1.py`**: the retained view now declares its own exception class (`RetainedRunView.UNAVAILABLE`). That lets a separately loaded copy of the module still reach the typed route.
- **`workflow-projection-contract.v3.md` §5**: the matching sentences for both rules.
- **`check-workflow-projection.v3.py`**: 19 new controls.

`workflows-and-surfaces.md` needed no change. The historical major-1 constructor, the repair:2 schema and recipe, and the existing refusal order are preserved.

**Results, in three groups:**

- **Known unrelated failure.** `oc2-owner-string-expression-case-is-policy-imperative-key-refused` fails in every checker run: root's run, baseline (795 checks) and edited (814 checks), so the checker exits 1 each time.
- **Repair controls.** On the edited tree all 19 new controls pass, and all 794 previously passing controls still pass. With the old owner files and the new checker, exactly 9 of the new controls fail. On the same real fixture:

  | Case | Before | After |
  |---|---|---|
  | Lawful preview | admitted | admitted, identical plan |
  | Same retained Run and Plan, wrong `run3:aaaa…` ID (root's case) | admitted | refused, no descriptor built |
  | `cw_dyn` / `cw_neg`, two other fully admitted Runs sharing the same Plan, IDs swapped either way | admitted (plan identical to `cw_dyn`'s own lawful plan) | refused, no descriptor built |
  | Declared missing finding record, both module copies | typed refusal | typed refusal; cause is that copy's own exception class |
  | Declared missing subject record, read by the selector, checker's separate module copy | escaped untyped | typed refusal |
  | Foreign exception with the owner's class name (root's case) | misrouted to unavailability | propagates as the same object |
  | `OSError` host fault | propagates | propagates as the same object |

  Root's own `probe.py`, run unchanged against my tree:
  - **Baseline copy:** reproduces root's report exactly.
  - **Edited tree:**
    - the lawful call is still admitted;
    - the wrong ID is refused;
    - the foreign exception comes out as its own class with no error code. Root's probe labels every exception "REFUSE", but this one propagated rather than being refused.

  An automated comparison of all these expectations passes.
- **Semantic and full-Run checks.** The real `cw_pos` Run and `cw_dyn` are each re-admitted to their own IDs by a separate `close_run`. The semantic golden replay passes 31 goldens with none blocked on both trees, with identical output.

**Limits:**
- **Behaviour change.** A view that declares no exception class now only gets the owner's own class mapped. The old code matched such views by class name; this change is intentional.
- **Trusted declaration.** The declared class is trusted like the rest of the adapter. A declaration that is too broad (such as plain `Exception`) would catch too much, and that is outside the trusted scope.
- **What the fixture proves.** The fixture adapters are synthetic over real admitted Runs, so nothing here qualifies a host, snapshot, trust or product.
- **What the ID check proves.** It shows the request names the retained Run exactly; it doesn't re-admit that Run.
- **Not run.** The six global groups.

Everything is in `/tmp/opensip-design-corrections/claude-repair-join-author.v1-continuation.v1`:
- `review.md`
- `review.json`
- `delta-vs-captured-source.diff`
- `receipts/c05-summary.final.json` (custody and command record)
