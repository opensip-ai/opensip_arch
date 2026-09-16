# Session standing — consumer-b.v24, source39 continuation

- Origin: the same original fresh blind origin `9d3dfb70-b2d3-498c-a3c1-f8de9e488514` (consumerId `consumer-b.v24`), continued in runtime
  `/private/tmp/opensip-design-corrections/consumer-b.v24-source39.v1`.
- Design inputs: only `subject/` listed in `subject/consumer-input-manifest.json` (SHA-256 `c2f2f88d…4ad80`, parent frozen subject
  `f71a5992…569009`, 104 members), plus `charter.md` and `requirements.json` of this runtime (task scope, not design authority).
- Own history: the prior runtime `/tmp/opensip-design-corrections/consumer-b.v24` is read-only own work. Only its helper source code was
  ported (`output/port-manifest.json`, path rebinding only). None of its vectors, Runs, replays, checkpoints or verdict is current evidence;
  every current result is recomputed against the source39 kit in this runtime. The prior subject is not read.
- Not read: the runtime harness files beside the charter (launch/process/prompt/public-events), the repository, author models, fixtures,
  goldens as oracles, reports, root results, other consumers or runtimes. Embedded kit examples and goldens are illustrations, not oracles.
- No subagents, no product implementation, no kit edits, no commits/pushes, no activation, no root acceptance. Output confined to `output/`.
- Interpreter: `/tmp/opensip-architecture-review-env/bin/python -I -B` (invoked through `python3 tools/runref.py`).
- Profile: identity/evaluator output major 3, PolicyDocumentV2/program2, required `executionInputsDigest`; unchanged native/input identities
  keep their declared major-2 recipes.
- Future qualification (real OS/compiler/crypto/SQLite, native provider execution as enforcement, host authentication, synthetic TCB as
  enforcement) is explicitly unperformed and never a design gap.
- Helper corrections continue the prior numbering from this origin's own work; every correction preserves the original failing bytes/log
  and cites the kit selector.
