I fixed the §5 wording, added the combined goldens, and narrowed the owner to a derived "analysis projection" of the step termination. The optional `executionId`, `domainDetail` and `authority` members are now left to their existing owners instead of being banned. The reduction law itself is unchanged. This is coauthor work only, not acceptance; v1 was not modified (its source still verifies against its retained after-state), and nothing touched pins, suites, planning, freeze, commit, push or root sources.

**§5 wording.** Your reading was right: the law already named the stage carrier; only the prose was wrong. §5 now says the carrier is chosen from every condition at the primary rank. Conditions that never carry one (evaluator-only causes, work budget, the requirement-relative ones) don't suppress another condition's carrier. `coverageId` is omitted only when no condition at that rank has a declared or stage carrier.

**Projection versus optional fields.** Requiring the whole `StepTermination` to match would override other owners:
- `executionId` is a fresh random ID per attempt (workflows-and-surfaces §1, identity-and-evidence §2), so two attempts' full terminations differ by design.
- `domainDetail` is detail the host attaches (workflows-and-surfaces §8–9, the detail registry, composition §8 for `EVALUATION.WORK_BUDGET_EXHAUSTED`).
- `authority` belongs to workflows-and-surfaces §9.

So the owner now derives only: class, `runId`, `reasonCodes` and their order, `coverageId` presence and value, and the absence of `errorCode`, `faultCause` and `signal`. v1's `check_candidate`/`admit_termination` are replaced by `check_projection`/`admit_projection`, which refuse in a fixed order:
1. a member that is neither derived nor delegated;
2. any mismatch in the derived fields;
3. a delegated member with no shape validator, or one the `StepTermination` schema rejects.

A delegated member that passes comes back marked `owner-validation-required`, never lawful. Contract §1, §2 and §6, the model, and my W§9 paragraph (+4/−2 since v1) now say this consistently. Note that your scope probe calls v1's `check_candidate`; v2's equivalent is `check_projection`.

**New goldens** in `check-semantic-replay.v3.py` (30/30 passing; v1 had 26, and all 8 v1 termination rows are unchanged):
- **Work budget + stage `budget-exhausted`** (your Run `00efec09…`): coverageId is the stage carrier `b6919b2c…`. Omitting it, naming the unstaged record, or putting the generic reason first all refuse.
- **Work budget + stage `unavailable`** (your Run `2525a299…`): `[COVERAGE.PROVIDER_UNAVAILABLE, COVERAGE.BUDGET_EXHAUSTED, VERDICT.INDETERMINATE]`. Work budget first, swapped or dropped secondaries, and a missing or wrong carrier all refuse.
- **Discovery order:** all 720 orders of that Run's conditions give one termination, while D9's reducer used as written gives 6 sequences and 3 different primaries.
- **Projection boundary:** a schema-valid `executionId`, work-budget `domainDetail` or `authority` passes as owner-validation-required. Each of these still refuses with its expected code: wrong reason order, omitted carrier, wrong `runId` or class, a `faultCause`, an unregistered member, a malformed `executionId`, `authority=ephemeral` alongside a `runId`, or no shape validator.
- Both of your variants, replayed against Runs that re-derive your recorded projections exactly, now pass as owner-validation-required instead of being refused.

**Checks.** A mutation probe swapped ten wrong versions of the law into the unchanged checker; each failed at least one row and the correct version passed. The ten include v1's unconditional omission, v1's whole-termination equality, delegated fields that skip validation or are reported lawful, and unknown fields passed through. Workflow projection (459), query projection (138), `check_workflows` (1803/1803), identity (1596/0) and integration (412) all produce output byte-identical to v1. The fixture didn't change, so I didn't rerun its other consumers.

**Coordination.** No overlap with the query-fault author: v2 touches only the three run-termination files, `check-semantic-replay.v3.py`, and my W§9 paragraph (now +13/−0 against frozen37) for you to merge into your §9 base. The stale pin rows and the pin additions for the three new files are unchanged from v1.

**Limits:**
- **Partial mixed-owner coverage.** The combined goldens cover work budget with native accounts that retained stage terminals, plus v1's native causes with stage terminals. They do not cover `required-relation-missing`, `confidence-floor-unmet`, language-tier or input-closure causes, or enumeration and import obligations; those rest on the contract's ranking table.
- **Shape fixtures only.** The delegated-field controls check shape, not whether any real attribution or remedy value is lawful; this owner doesn't validate that.
- **Prose edit after checks.** My last §5 edit came after the checks ran; no checker or model reads that text.
- **Same author, no blind reconstruction.** The contract, model and goldens share one author; the Runs are synthetic.
- **Still unperformed.** TCB-SCOPE-01 with its 13 accounts, the 32 gates and the 54 recovery cases.

Everything is in `/private/tmp/opensip-design-corrections/claude-source37-host-finalizer-author.v2`, with per-file diffs, before/after images and all 14 command receipts alongside:
- `review.md`
- `review.json` (SHA-256 `8012c379…2294`)
- `v1-to-v2.diff` (`a8980fd1…78b9`)
- `frozen37-to-final.diff` (`f52e7823…556d`)
- `after-manifest.json`
