"""p03: items 1 and 2 remaining edits by exact counted replacements in v2 work/edited:
- run_termination_model.v1.py: the receipt inventory join and the derivation-binding joins in the committed branch;
- check-semantic-replay.v3.py: composition observations use the Run's actual execution plan and stage count and
  receipts minted by the reference commit path; new observation spec keys;
- run-termination-goldens.v1.json: the composition golden's why text;
- run-termination-contract.v1.md: sections 6, 7.2, 7.3, 7.6, 7.7 and 8.
Anchors must each occur once; nothing is written unless all do. Output: receipts/p03-apply-composition.json.
"""
import hashlib, json, sys
from pathlib import Path

BASE = Path('/tmp/opensip-design-corrections/claude-source38-advisory-author.v2')
ED = BASE / 'work' / 'edited'
FND = 'docs/coop/design-corrections/foundation/'
MODEL, CHECK, GOLD, CONTRACT = (FND + 'run_termination_model.v1.py', FND + 'check-semantic-replay.v3.py',
                                FND + 'run-termination-goldens.v1.json', FND + 'run-termination-contract.v1.md')

EDITS = [
    (MODEL,
     '    derived = derive(run, objects, blobs)\n'
     '    receipt = observation["commitReceipt"]\n'
     '    if receipt["runId"] != derived["termination"]["runId"]:\n'
     '        _refuse("RUN_TERMINATION_RECEIPT_RUN_MISMATCH")\n'
     '    if receipt["executionId"] != terminating["executionId"]:\n'
     '        _refuse("RUN_TERMINATION_RECEIPT_ATTEMPT_MISMATCH")\n'
     '    if terminating["derivation"]["planId"] != run["planId"]:\n'
     '        _refuse("RUN_TERMINATION_ATTEMPT_PLAN_MISMATCH")\n',
     '    derived = derive(run, objects, blobs)\n'
     '    run_id = derived["termination"]["runId"]\n'
     '    receipt = observation["commitReceipt"]\n'
     '    if receipt["runId"] != run_id:\n'
     '        _refuse("RUN_TERMINATION_RECEIPT_RUN_MISMATCH")\n'
     '    if receipt["executionId"] != terminating["executionId"]:\n'
     '        _refuse("RUN_TERMINATION_RECEIPT_ATTEMPT_MISMATCH")\n'
     '    # The receipt names the exact published commit-inventory of this Run (identity-and-evidence commit-inventory);\n'
     '    # receipt schema admission does not establish it, so re-derive it over the Run content composed here.\n'
     '    if receipt["inventoryDigest"] != M.commit_inventory(run_id, objects, blobs)[1]:\n'
     '        _refuse("RUN_TERMINATION_RECEIPT_INVENTORY_MISMATCH")\n'
     '    binding = terminating["derivation"]\n'
     '    if binding["planId"] != run["planId"]:\n'
     '        _refuse("RUN_TERMINATION_ATTEMPT_PLAN_MISMATCH")\n'
     '    # One attempt owns exactly one execution plan (invocation-record DerivationBinding): the Run\'s admitted plan is\n'
     '    # its evaluation seal\'s executionPlanId, which close_run has joined to the proof and to the Run\'s planId.\n'
     '    execution_plan_id = objects[run["evaluationSealId"]][1]["executionPlanId"]\n'
     '    if binding["executionPlanId"] != execution_plan_id:\n'
     '        _refuse("RUN_TERMINATION_ATTEMPT_EXECUTION_PLAN_MISMATCH")\n'
     '    stages = objects[execution_plan_id][1]["stages"]\n'
     '    if binding["stageCount"] != len(stages):\n'
     '        _refuse("RUN_TERMINATION_ATTEMPT_STAGE_COUNT_MISMATCH")\n'
     '    # stagesCompleted and firstFailedStage are runtime progress no retained record re-derives: bound them by the\n'
     '    # plan, never infer completion from scheduled stages.\n'
     '    if binding["stagesCompleted"] > binding["stageCount"] or (\n'
     '            "firstFailedStage" in binding and binding["firstFailedStage"] not in {s["ordinal"] for s in stages}):\n'
     '        _refuse("RUN_TERMINATION_ATTEMPT_STAGE_PROGRESS_MISMATCH")\n'),
    (CHECK,
     '    invocation-record Attempt and a commit receipt whose inventoryDigest is the retained commit inventory. For an\n',
     '    invocation-record Attempt, whose derivation binding names the Run\'s actual execution plan and stage count, and a\n'
     '    commit receipt minted by the reference commit path (identity-model.v3 EvidenceStore). For an\n'),
    (CHECK,
     '            if spec is not None:\n'
     '                own_plan = run["planId"] if run is not None else "plan2:" + "2" * 64\n'
     '                plan = "plan2:" + "0" * 64 if spec.get("plan") == "other" else own_plan\n'
     '                attempts = []\n',
     '            if spec is not None:\n'
     '                if run is not None:\n'
     '                    execution_plan = objects[run["evaluationSealId"]][1]["executionPlanId"]\n'
     '                    stage_count = len(objects[execution_plan][1]["stages"])\n'
     '                    own_plan = run["planId"]\n'
     '                else:  # ephemeral cases compose no Run, so no plan join applies\n'
     '                    execution_plan, stage_count, own_plan = "exec-plan2:" + "2" * 64, 1, "plan2:" + "2" * 64\n'
     '                plan = "plan2:" + "0" * 64 if spec.get("plan") == "other" else own_plan\n'
     '                binding = {"planId": plan,\n'
     '                           "executionPlanId": "exec-plan2:" + "0" * 64 if spec.get("executionPlan") == "other" else execution_plan,\n'
     '                           "stageCount": stage_count + spec.get("stageCountDelta", 0),\n'
     '                           # a host observation, never derived from the plan: "all" is the fixture\'s assumption\n'
     '                           "stagesCompleted": {"all": stage_count, "partial": stage_count - 1,\n'
     '                                               "over": stage_count + 1}[spec.get("stagesCompleted", "all")]}\n'
     '                if "firstFailedStage" in spec:\n'
     '                    binding["firstFailedStage"] = spec["firstFailedStage"]\n'
     '                attempts = []\n'),
    (CHECK,
     '                        attempts.append({"executionId": ids["done"], "outcome": "completed",\n'
     '                                         "derivation": {"planId": plan, "executionPlanId": "exec-plan2:" + "e" * 64,\n'
     '                                                        "stageCount": 1, "stagesCompleted": 1}})\n',
     '                        attempts.append({"executionId": ids["done"], "outcome": "completed", "derivation": dict(binding)})\n'),
    (CHECK,
     '                    who, which = spec["receipt"]\n'
     '                    _, inventory_digest = M.commit_inventory(derived["runId"], objects, blobs)\n'
     '                    receipt = {"schemaVersion": 2, "runId": derived["runId"] if which == "run" else other_run,\n'
     '                               "executionId": ids[who], "namespaceId": "reference-private-namespace",\n'
     '                               "commitSequence": 1, "inventoryDigest": inventory_digest,\n'
     '                               "sealedAssurance": "replayable", "signerKeyId": "reference-host-signer"}\n',
     '                    who, which = spec["receipt"]\n'
     '                    receipt = committed_receipt(run, objects, blobs, ids[who])\n'
     '                    if which != "run":\n'
     '                        receipt["runId"] = other_run\n'
     '                    if spec.get("inventory") == "other":\n'
     '                        receipt["inventoryDigest"] = "f" * 64\n'
     '                    elif spec.get("inventory") == "missing-object":\n'
     '                        receipt["inventoryDigest"] = M.commit_inventory(derived["runId"], dict(list(objects.items())[1:]), blobs)[1]\n'),
    (GOLD,
     'Operational carriers return to their owners without a Run. Attempts, receipts and the installation observation are synthetic host inputs, not a product host.",',
     'Operational carriers return to their owners without a Run. Attempt derivation bindings name each Run\'s actual admitted execution plan and stage count, and receipts are minted by the reference commit path (identity-model.v3 EvidenceStore.prepare and commit); a wrong execution plan, stage count, stage progress beyond the plan, or a receipt inventory that is not the Run\'s refuses while the same candidate is otherwise admitted. Stage progress is a host observation the fixture assumes complete; one control shows partial progress is neither derived nor refused. Attempts, receipts and the installation observation are synthetic host inputs, not a product host.",'),
    # ---------------- contract
    (CONTRACT,
     'Refused: unrelated registered details (`HOST.INVARIANT_VIOLATED`, `QUERY.PARAMS_MALFORMED`, `DOCTOR.DEFECTS_FOUND`); a detail without its prerequisite or on a verdict; an omitted selected detail; an earlier or foreign `executionId`; a receipt or plan of another attempt or Run;',
     'Refused: unrelated registered details (`HOST.INVARIANT_VIOLATED`, `QUERY.PARAMS_MALFORMED`, `DOCTOR.DEFECTS_FOUND`); a detail without its prerequisite or on a verdict; an omitted selected detail; an earlier or foreign `executionId`; a receipt or plan of another attempt or Run; an attempt bound to another execution plan or stage count, or reporting stage progress outside that plan; a receipt whose inventory is not the Run\'s published inventory;'),
    (CONTRACT,
     'Admitted: each allowlisted detail with its prerequisite, a lawful omission, a retried terminating attempt, and an ephemeral `authority`;',
     'Admitted: each allowlisted detail with its prerequisite, a lawful omission, a retried terminating attempt, a receipt minted by the reference commit path, partial stage progress, and an ephemeral `authority`;'),
    (CONTRACT,
     '| the step\'s `StepResult.attempts` (`invocation-record.schema.json#/$defs/Attempt`) | host-supplied operational identity | the terminating attempt: the last attempt, with `outcome=completed` and its `derivation` binding. No earlier attempt is `completed`, and no `ExecutionId` repeats |',
     '| the step\'s `StepResult.attempts` (`invocation-record.schema.json#/$defs/Attempt`) | host-supplied operational identity and progress | the terminating attempt: the last attempt, with `outcome=completed` and its `derivation` binding (`planId`, `executionPlanId`, `stageCount`, `stagesCompleted`, optional `firstFailedStage`). No earlier attempt is `completed`, and no `ExecutionId` repeats |'),
    (CONTRACT,
     '| the attempt\'s commit receipt (`identity-schemas.v3.json#/$defs/commit-receipt`) | host-supplied operational record: required for a committed Run, absent for an ephemeral attempt | the `executionId` that committed `runId` |',
     '| the attempt\'s commit receipt (`identity-schemas.v3.json#/$defs/commit-receipt`) | host-supplied operational record: required for a committed Run, absent for an ephemeral attempt | the `executionId` that committed `runId`, and the `inventoryDigest` of what that commit published |'),
    (CONTRACT,
     '### 7.3 `executionId` binds the actual admitted attempt, step and Run\n\n'
     'For a committed Run, these joins hold before any candidate member is judged:\n'
     '- the receipt\'s `runId` is the derived `runId` (`RUN_TERMINATION_RECEIPT_RUN_MISMATCH`);\n'
     '- the receipt\'s `executionId` is the terminating attempt\'s (`RUN_TERMINATION_RECEIPT_ATTEMPT_MISMATCH`). The\n'
     '  reference commit path issues one receipt per committing attempt (`identity-model.v3` `EvidenceStore.commit`);\n'
     '- the terminating attempt\'s `derivation.planId` is the Run\'s `planId` (`RUN_TERMINATION_ATTEMPT_PLAN_MISMATCH`).\n',
     '### 7.3 `executionId`, the attempt\'s derivation binding and the receipt bind the actual admitted attempt, step and Run\n\n'
     'For a committed Run, these joins hold before any candidate member is judged, in this order:\n'
     '- the receipt\'s `runId` is the derived `runId` (`RUN_TERMINATION_RECEIPT_RUN_MISMATCH`);\n'
     '- the receipt\'s `executionId` is the terminating attempt\'s (`RUN_TERMINATION_RECEIPT_ATTEMPT_MISMATCH`). The\n'
     '  reference commit path issues one receipt per committing attempt (`identity-model.v3` `EvidenceStore.commit`);\n'
     '- the receipt\'s `inventoryDigest` is `commit_inventory(runId, objects, blobs)` (`identity-model.v3`), re-derived\n'
     '  over the Run content composed here: identity-and-evidence\'s `commit-inventory`, "the exact set of typed object\n'
     '  identities and retained raw blob digests the commit published for that Run"\n'
     '  (`RUN_TERMINATION_RECEIPT_INVENTORY_MISMATCH`). The `objects` and `blobs` composed are therefore the Run\'s\n'
     '  published retained content, as the reference commit path inventories them, not a wider shared store.\n'
     '  Receipt schema admission does not establish this join, and no owner invoked on this path discharges it: the\n'
     '  commit path mints the digest, and read-only recovery joins it only between the receipt and the association\n'
     '  (`attempt-custody.schema.v1.json` `joins.toReceipt`);\n'
     '- the terminating attempt\'s `derivation.planId` is the Run\'s `planId` (`RUN_TERMINATION_ATTEMPT_PLAN_MISMATCH`);\n'
     '- its `derivation.executionPlanId` is the Run\'s admitted execution plan, `objects[run.evaluationSealId].executionPlanId`\n'
     '  (`RUN_TERMINATION_ATTEMPT_EXECUTION_PLAN_MISMATCH`). The Run record carries no execution plan of its own;\n'
     '  `close_run` joins the seal\'s plan to the proof bundle and to the Run\'s `planId`, and the `DerivationBinding` owner\n'
     '  states that one attempt owns exactly one execution plan;\n'
     '- its `derivation.stageCount` is the number of `stages` of that plan (`RUN_TERMINATION_ATTEMPT_STAGE_COUNT_MISMATCH`):\n'
     '  workflows-and-surfaces §1 records the attempt\'s derivation DAG and its size in that binding;\n'
     '- its stage progress stays inside that plan: `stagesCompleted` is at most `stageCount`, and a present\n'
     '  `firstFailedStage` is the `ordinal` of one of its stages (`RUN_TERMINATION_ATTEMPT_STAGE_PROGRESS_MISMATCH`).\n'
     '  `stagesCompleted` and `firstFailedStage` are runtime progress of the host attempt (the native protocol counts a\n'
     '  stage when its Coverage arrives, `protocol3-transitions.v1.json` P3-24), and no retained record re-derives them.\n'
     '  A scheduled stage is not a completed one, so the composition does **not** require `stagesCompleted` to equal\n'
     '  `stageCount` and does not decide whether a completed attempt may carry `firstFailedStage`; both stay with the\n'
     '  host attempt owner (workflows-and-surfaces §1).\n'
     '\n'
     '`namespaceId`, `commitSequence`, `sealedAssurance` and `signerKeyId` stay with the receipt\'s own admission and\n'
     'its signer and custody checks; nothing here authenticates them.\n'),
    (CONTRACT,
     '4. For a committed Run: `close_run` and the derivation, then the §7.3 joins, `check_projection` (§6),\n'
     '   `authority`, `executionId`, and finally `domainDetail` (§7.5).\n',
     '4. For a committed Run: `close_run` and the derivation; the §7.3 receipt joins (`runId`, `executionId`,\n'
     '   `inventoryDigest`) and derivation-binding joins (`planId`, `executionPlanId`, `stageCount`, stage progress);\n'
     '   `check_projection` (§6); `authority`; `executionId`; and finally `domainDetail` (§7.5).\n'),
    (CONTRACT,
     'is outside this contract\'s threat model, as it is for every trusted host observation behind D9\n'
     '`invariant-one-mapper`. Nothing here qualifies authentication, containment, durability or a product host.\n',
     'is outside this contract\'s threat model, as it is for every trusted host observation behind D9\n'
     '`invariant-one-mapper`. The §7.3 joins catch accidental disagreement between the host\'s attempt, its receipt and\n'
     'the admitted Run; they do not authenticate the receipt. Nothing here qualifies authentication, containment,\n'
     'durability or a product host.\n'),
    (CONTRACT,
     '  The `host-composition-boundary` controls compose over actually closed Runs. They use synthetic attempt records,\n'
     '  receipts built from the retained commit inventory and a boolean installation observation.',
     '  The `host-composition-boundary` controls compose over actually closed Runs. They use synthetic attempt records\n'
     '  bound to each Run\'s actual execution plan and stage count, receipts minted by the reference commit path\n'
     '  (`EvidenceStore.prepare` and `commit`) and a boolean installation observation. Fixture execution plans have one\n'
     '  stage (ordinal 0), and the fixture assumes full stage progress as a host observation.'),
]


def sha(b):
    return hashlib.sha256(b).hexdigest()


texts, problems = {}, []
for rel in sorted({e[0] for e in EDITS}):
    texts[rel] = (ED / rel).read_text(encoding='utf-8')
for rel, old, new in EDITS:
    n = texts[rel].count(old)
    if n != 1:
        problems.append('%s anchor count %d: %r' % (rel, n, old[:100]))
        continue
    texts[rel] = texts[rel].replace(old, new)
out = {'standing': 'items 1-2 exact replacements in v2 work/edited', 'edits': len(EDITS)}
if problems:
    out.update(problems=problems, written=False)
else:
    json.loads(texts[GOLD])
    compile(texts[MODEL], MODEL, 'exec')
    compile(texts[CHECK], CHECK, 'exec')
    rows = []
    for rel, text in texts.items():
        before = sha((ED / rel).read_bytes())
        (ED / rel).write_text(text, encoding='utf-8')
        rows.append({'path': rel, 'before': before, 'after': sha((ED / rel).read_bytes())})
    out.update(written=True, files=rows)
(BASE / 'receipts' / 'p03-apply-composition.json').write_text(json.dumps(out, indent=1) + '\n')
print(json.dumps(out, indent=1))
sys.exit(0 if not problems else 1)
