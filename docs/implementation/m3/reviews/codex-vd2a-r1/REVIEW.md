**Verdict: REQUIRED-FINDINGS for VD2-a; REQUIRED-FINDINGS for F8c's pinned record. One required finding: VD2A-RF-01.**

The implementation satisfies the requested fixtures, history rules and re-pin checks, but its new exact-review check accepts a different JSON selector. F8c's record is structurally correct; its assessment is held because resolving the verifier finding changes the reference candidate and dependent re-pin artifacts. There is no separate record-structure finding. These reviewed bytes are not accepted for integration.

Reviewed the detached product worktree `/Users/sb/code/opensip-ai/opensip-vd2a` at `4c761e8b7849a449b19df026127819ba4fc46c2f`, against accepted law VD2 r1 (31,850 bytes, `2e4f70b4a70b80f9d19123755102f58a07870bf2c9f4faea21f8c76a17892c90`). All 50 requested pins matched initially and at completion. The diff remains exactly seven modified files, +377/-13, with no added path or commit.

| Reviewed subject | Bytes | SHA-256 |
|---|---:|---|
| Product diff from `4c761e8` | 31,039 | `f7767bbe56747ddf449105aceb882893b82ced8b65733e5d777d9c692dac64d5` |
| `f8c-subject.json` | 3,808 | `058406b73d037c989de77644be78e141f8160162acf43627caea8f8a2c347e4d` |
| `f8c/successor.json` | 5,231 | `fda38d17afee4df6281144b7b1ce5121459528eda82506deec6cf1855f6af20d` |
| Product/reference verifier | 43,630 | `c01488fd5aacdb0e704767e2604f5f71a6933de8a0639f4d947e5c3e97378f1b` |

**VD2A-RF-01 — medium — exact review coverage loses selector identity.** Location: `tools/verify_design.py:419`.

For an accepted ordinary override of `doc.md` line 1, construct a valid supersession with both its selector and `supersedes.selector` equal to `{"line": 1}`. Put `{"line": true}` only in that supersession's independently pinned review list. The verifier accepts the lock and reports `contractPassageSupersessions: 1`, because Python nested equality treats `true` as `1`. A review selector `{"line": 1.0}` also passes. Both differ from the record's canonical selector, and `selected_passage` would reject either as an actual line selector. All review, manifest and assent hashes in the reproducer are properly rejoined: this is an authenticated wrong review list, not corrupt fixture bytes.

VD2 rule 2.7 requires the list to match the record exactly, in addition to its subject digest. Canonical selector identity in rule 2.3 distinguishes these values. The separate record checks still choose the correct target passage, so this does not allow a different passage's content to be substituted. It does defeat the additional explicit independent-review coverage that this law deliberately requires. A review naming an invalid selector cannot satisfy that coverage merely because Python coerces it during comparison.

Required: make the new review-list comparison respect JSON types and canonical selector identity, keeping object-key-order independence, list order and the existing `contract review superseded passages differ from the record` message. Add negative regression cases for boolean and floating-point review line selectors against an integer selector in the record. This can be fixed solely at the new review-list check; retain VD1's existing target-pin behavior.

Reproduce with `value-equality-probes.py` in the recorded private environment (`run-environment.json`). Its first two outcomes are currently PASSED and must refuse. The named-selector boolean control already refuses as `superseded passage is not in the named record`, showing that target lookup has the canonical identity that the review check lacks. A detached floating-point target-record byte count still passes, as the lead disclosed; the exact path/digest and numerically equal size do not select other content.

An illustrative scratch change comparing canonical JSON for the new list rejects both review mismatches with the existing message and passes all 117 existing tests. It leaves the target-pin equality case unchanged. See `review-list-fix-summary.json`, `review-list-fix-probes.json` and `review-list-fix-tests.stderr`. No fix was applied to the product or architecture repository. Any corrected tool must be carried through a fresh F8c reference/tool diff, closure/lane re-pin, registry/report generation, evidence and subject/record pins; the present assessment does not approve those future bytes.

**Law and test assessment.** The new contract branch correctly classifies by inventory-chain membership, names a strictly earlier accepted record, matches the full parent and canonical selector, checks `before` against the named `after`, permits an identical ordinary-root copy only before the first link, and extends only the tail. Restatement is refused after the unchanged conflict check. Publication and counts remain in lock order; no contract meaning enters inventory inheritance. The base lock's plain and implementation outputs are byte-value identical to the base verifier output except for the new zero contract count. The exception is the review identity defect above.

The law's 40 controls and all six VD2-NB-01 additions are present and pass independently. **VD2-NB-01 is CLOSED:** N16 wrong record length; N17 two links to one passage; N18 second link's own missing review list; P9 exact optional inventory-only list; N19 wrong present inventory-only list; P10 empty list on a record without links. The rewritten VD1 positive half now supplies its review list and asserts a successful contract link, contract count 1, inventory count 0 and the named `supersedes`. Its inventory-negative half still refuses with VD1's original message. The new equality regression cases are additional to that completed obligation.

**F8c assessment.** Independently checked all five parents against accepted history at the base lock: I1-a's closure, registry and generated report, plus F8b's lane registry and reference verifier. The subject has exactly the record plus all 17 candidates, with exact pins, complete coverage and no reused accepted candidate path. There are no overrides or supersessions. The four materialization-map rows match both the base worktree bytes and the candidate/product bytes. The tool-only diff equals the actual tool portion of the reviewed product diff, and `/usr/bin/patch` applied it in scratch to obtain the candidate exactly.

Only the verifier row changes in the 348-row closure and the 160-row lane registry. Only the recipe's closure digest changes in the schema registry; only report lines 2 and 3 change. The old five digests are absent from tracked worktree consumers. All seven modified paths exist in v135, with descriptions that remain true; no inventory successor is needed. No Rust source reads the changed verifier/re-pin files.

No generator rebuild is needed: `validate_build_receipt` joins the executable to the five Rust manifest/source inputs and `tools/build_contracts.py`, all unchanged. The real public drift gate reran every receipt/closure/toolchain check against rebuild-02 and passed with 40 sources, eight outputs and `changed: []`. The staged lock selects each of the five changed design materializations exactly once through F8c, while leaving 95 inventory successors, v135, 100 inheritance rows and 21 VD1 links unchanged. The placeholder review/assent overlay is confined to scratch; plain verifier, generator and TypeScript checker each still refuse at `SCRATCH-F8C/review.json`, as required before real acceptance.

**Judgment calls, direct answers.**

1. Agree with v4-only review coverage in `successor_chain` and the numbered per-record order. This preserves earlier lock versions and original conflict precedence; a second decode keeps the count as the sole output addition.
2. VD1-compatible target-pin equality may remain: fixed exact path/digest and an equal byte count cannot refer to different content, while target selectors remain canonical. The new review-list comparison must distinguish JSON types and canonical selectors. Its current Python equality is not acceptable; VD2A-RF-01 is the required change.
3. Keep the root-kind guard as an invariant. A previously published contract supersession necessarily set the tail, so its root-kind-only condition is unreachable. The expected sole mutation survivor is explained; no reachable refusal is missing coverage.
4. Accept the optional `listed` fixture argument and new AUTO helper. Old VD1 callers retain absent lists. N15 correctly reaches the unchanged v3 supersession refusal before any classifier.
5. Accept the I1-a/F8b parent selection. Each exact pin is the accepted base at the frozen head; there is no intervening closure writer in this worktree.
6. Accept and retain the tool-only diff as non-circular provenance. It reproduces the candidate exactly. A full product diff contains the lock/manifest pin and would create the identified circular reference; excluding tests from the re-pin subject is appropriate because they are pinned nowhere in these registries.
7. Accept the separate unit and contract JSON review shape. The contract review's top-level verdict is what the lock would bind after acceptance. Both verdicts are REQUIRED-FINDINGS this round because correcting the tool changes F8c's frozen subject.
8. Accept the absence of an inventory successor and omit `inventoryCandidateAssessment` from both JSON reviews.
9. Accept the bounded Rust validation scope. Independently reran all listed checks, including the optional `schema_sources` test; no broader Rust test lane or crash-matrix set is warranted for this diff.

**Independent validation.** Results were checked from retained logs and JSON, rather than inferred from the lead's table.

| Check | Result |
|---|---|
| Initial/final request pins and exact product diff | 50/50 match at both checks |
| Design binding / TypeScript tool / crash-matrix tool unit tests | 117 / 3 / 26 pass; no matrix set |
| Law fixture / extension controls | 40/40 / 46/46 expected outcomes |
| Real-lock probe, corrected only for moved unbound reference inputs | 17/17 expected outcomes |
| Base/new verifier over HEAD lock, plain and implementation | Equal except added contract count 0; 94 contracts, 95 inventory successors |
| New tests against base / law prototype | Expected 34 failed/error assertions / 117 pass |
| Mutation suite | 17/18 killed; sole unreachable root-kind invariant survives; expected exit 1 |
| Scratch staged verifier | Pass; 95 contracts; 40 generation sources, 48 admission sources, 15 aliases |
| Real public drift scratch | Pass; 40 sources, eight outputs, `changed: []` |
| Scratch TypeScript preflight | Registry selected once, 12 tracked rows and both trusted entry points match; expected missing offline node_modules refusal before any child |
| Plain staged verifier / generator / TypeScript checker | All exit 1 at missing `SCRATCH-F8C/review.json` |
| Cargo fmt / host and provider metadata | Pass |
| Optional host `schema_sources` tests | 25 pass |
| Host/provider package edges / package edge tests | Both pass; host 12 packages, 22 declared and 20 resolved edges; 14 tests pass |
| Dependency check / identity dependency check | Pass: 11 dependencies, eight local sources / eight dependencies, 305 sources |
| Dependency / identity dependency tests | 9 / 5 pass |
| Scratch illustrative review-list fix | Both added mismatches refuse; all 117 original tests pass |

The pinned real-lock probe initially failed because the lead's unbound SD7-r1 `contracts/native-evidence.md` had moved during SD7-r2 drafting. `probe_real_lock.retained-context.py` changes only two reference reads: it supplies the law review's retained NE7 (380,848 bytes, `0dd155c2e2439b2223cdcfaec2ecad61c89bcf6a348f3be3c8f3350e9555ebd3`) and SD7-r1 record (5,440 bytes, `c1b9baa76f0b888300cd72696d5b3e73ca5c94bdd3fdbd6e7a6249ab71914a4d`). The verifier, 17 cases and all bound architecture reads are unchanged. The resulting effective native-evidence text equals that retained NE7 byte for byte. See `probe-context.json` and `probe-real-lock-retained-context.json`; the initial unavailable-live-context log is also retained.

Full TypeScript lane children remain unrun because the existing offline esbuild boundary is absent; the scratch script's success denotes the expected refusal and valid preflight, not a passing TypeScript lane. The optional full materialization replay was not run; exact delta/map/diff application and the real public drift gate provide independent checks of the prospective bytes.

All runs used nice 19 and the recorded private 0700 Darwin-user TMPDIR. Cargo used the review-local target and cloned offline registry, with a process guard before Cargo and Cargo-invoking policy drivers. The generator guard found no competing generator before the required drift replay. Git was read-only and used only the named product worktree. There were no repository edits, commits, delegated tasks, crash-matrix sets, real OpenSIP application-home access or private 413 fixture reads. Review and evidence outputs are retained under this review directory.
