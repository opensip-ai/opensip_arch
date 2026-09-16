I've finished the reconciliation. The author's S1 remedy is coherent. The native schema bytes should stay as they are, with a note added to native §10 saying §10 governs over the stale annotation. The new §10 wording does mix up a native stage's selection with the whole Run's termination, and I've written minimal replacement text for it. This is remedy assistance only: not independent or successor acceptance, and it grants nothing.

Everything is in `/tmp/opensip-design-corrections/claude-consumer23-remedy-reconciliation.v2/`:
- `reconciliation.md` (`dccb49d8…`) and `reconciliation.json` (`972cb2ce…`); a consistency check against the receipts passes 24/24;
- `recommended-edits.diff` (`8dd70655…`) holds the five edits.

Each edit's anchor text occurs exactly once in the author's captured files. I applied them only to disposable copies, and the edited model still compiles. I read no live source, blind artifacts or consumer diagnostics. I ran one targeted probe on the author's files over frozen36, no suites, and nothing is left running.

## 1. S1: coherent
The author chose schema-first admission, which my gap assessment had recorded as the lawful alternative.
- **Measured:** a package endpoint with a missing or empty `packageManifestPath` gets `QUERY.PARAMS_MALFORMED` before any Run, view or availability check. That held with no Run, with a purged observation, and with a dummy Run, and the helper agrees.
- A well-formed endpoint gets past that check and is then refused `evidence.purged`.
- The graph-query schema is unchanged, and `QUERY.ENDPOINT_AMBIGUOUS` only comes out of a helper handed a pre-marked key.
- I withdraw my earlier preference for a request-side schema: the author's route changes no schema or planning input.

One precision edit is recommended. §2 defines a vertex by its complete tuple, so one complete tuple can never name two vertices under the contract itself. The closing clause "a vertex domain that could" should instead say the step is a closed refusal: an implementation that ever sees two vertex records for one tuple must refuse and never pick one.

## 2. Native schema annotation: keep the bytes
`coverage2` identities are built from the raw SHA-256 of that exact registered schema document. In my earlier rehearsal, changing those bytes broke an identity check and made every retained package13 Run refuse. So there is no remint or re-registration here.
- **Recommendation:** add a §10 note that points at `…/threeDistinctThingsNotToConflate/publicD9Termination`.
  - Its reference to the §10 columns still stands.
  - Its three-code list and its word `errorCode` are superseded: an indeterminate termination carries `reasonCodes`, and the codes are the full table.
  - Where the two differ, §10 governs; changing the annotation needs a schema-document successor.

## 3. §10 scope: a real conflation
The author's paragraph says the *Run's* primary deficiency is chosen from the Coverage entries plus the stage terminal. That is only what the native helper `run_termination(stage, coverage_entries)` sees. The owning contracts put the Run's termination above native:
- **Host builds it:** only the host finalizer constructs the termination (D9 `invariant-one-mapper`).
- **Host orders it:** the host picks faults, then rejections, then deficiencies, and takes the primary and secondary deficiencies from its own ordered set (D9 `concurrentConditionReducer`, `causeModel`).
- **Requirement-relative codes:** `required-relation-missing` and `confidence-floor-unmet` can't come from a Coverage entry; the cause registry marks them `none-in-entry`. Their D9 examples are requirement scenarios.
- **Verdict inputs:** required execution deficiencies and gating rules also make the verdict indeterminate (evaluator composition §5).

**Measured:** the helper only produces those two codes when an entry declares them. A stage-implied primary can also differ from the deficiency named in the typed detail: a budget-exhausted stage with a `resolution-incomplete` entry gives `COVERAGE.BUDGET_EXHAUSTED`.

**Recommended wording changes:**
- Rename the paragraph to "Native stage selection, and where it stops". It keeps the stage precedence, native causes, fault and cancel rules, and the complete deficiency-to-code map.
- It then states that the host reduction takes the Run's primary and secondary deficiencies.
- It explicitly does not define how requirement, proof-cause, import or verdict outcomes are ordered, and adds no per-requirement D9 code.
- Apply the same stage-scoping to the new fault-law sentence and to the `run_termination` docstring. That docstring is the only model change, and no behaviour changes.

**Advisory:** how a host pairs a `coverageId` with a termination whose code differs from the detail is left to host and D9.

## Limits and carried state
- No suites, pins, planning checks or report regeneration were run; the author applies the edits.
- One probe assertion of mine came out false because of how the model's type annotations print. The helper's inputs really are just its stage and entries, and the error is recorded.
- Still carried:
  - TCB-SCOPE-01 as one shared assumption over 13 dependent rows;
  - 32 product gates with 0 performed and condition 5 NOT MET;
  - 54 planned recovery cases, none executed;
  - source36 acceptance reopened.

  No final application or readiness authority is granted.
