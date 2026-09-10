# Final root delta — bounded source-peer assessment (actual Claude)

**Subject:** `/tmp/opensip-design-corrections/v20-final-source.v1/work`
**Manifest:** `proposal.json` @ `cec32147433b2879721a1597206e03035b5c213cd75ead9a19ca0a725972163d` — **matches the given pin exactly.**

**Verdict: technically sound, with one required minor correction.**
Changes 1, 2, 4 and 5 assent as written. Change 3 is a real strengthening and is true where it runs, but its predicate is weaker than the claim `rootChanges[2]` makes for it. A two-line exact patch is supplied and verified.

This is a bounded peer assessment of the **final small root delta only**, on top of the completed route-coauthor nine-file overlay. It is not fresh independent source20 acceptance, not blind consumption, and not readiness or product qualification. I did not re-derive the preliminary source (owned by actual Claude `8edfd51b`) or the route overlay semantics (owned by route coauthor `132a831b`), and I did not run the six suites — root owns those after final pins.

---

## 1. Manifest and hash assent

All twelve final hashes verify against the work tree, and all twelve baseline hashes verify against the selection rule (route overlay where present — 9 files; preliminary work tree fallback — 3 files: `identity-model.py`, `identity-schemas.v2.json`, `native-cases.v2.json`).

| Manifest-level pin | Resolved |
|---|---|
| `preliminaryManifestSha256` `272a2e13…` | ✅ `v20-combined-source.v1/proposal.json` |
| `routeChangesSha256` `62150d8f…` | ✅ `v20-route-coauthor.v1/results/changed-files.json` — its 9 rows chain `preliminary → route` exactly as the manifest records |
| `parentManifestSha256` `312db9d9…` | ❌ not found in my readable scope (provenance only; binds no composition claim) |

Per-file hash assent for all twelve files is in `assessment.json`.

## 2. Completeness of the four root-diffs — verified, not taken on trust

I reconstructed the baseline (preliminary work + route overlay applied) and checked completeness two independent ways:

- **Regenerated** `diff -u` for all twelve manifest files and compared the `+`/`-` bodies against the shipped root-diffs → **identical for all twelve**.
- **Whole-tree recursive diff**, not just the twelve listed paths → **exactly 4 files differ, 0 added, 0 removed.**

The second check is the one that matters: it rules out a change hiding outside the manifest. The claim that the four nonempty root-diffs contain every additional root change **holds exactly**. The eight carry-forward files are byte-identical to baseline.

## 3. The five changes

**1 — `why` opening refined (schemas).** ✅ Assent. The old opening was wrong for the default path, and wrong in a way the same entry's own tail already contradicted: `default_capability_selection` builds every row with `required: True` literally, so its duplicates are byte-identical and disagree on nothing. The old text also asserted unconditionally that "both rows enter analysisSpecDigest and therefore PlanId"; the new text correctly makes that conditional (*"if admitted"*), which is the right modality since the guard refuses before admission. "Host invariant violation" is accurate and consistent with the entry's existing `host-generated-internal-layer` origin. No control couples to the removed phrasing — the one `native-cases.v2.json` note repeating the old wording scopes itself explicitly to rows "disagreeing only on `required`" and stays accurate.

**2 — Overbroad refusal claim narrowed (contract + checker comment).** ✅ Assent, and it corrected a genuine falsehood rather than a loose phrasing. `default_capability_selection` calls `admit_release_capability_registry` as its *first* statement, and that helper has at least three distinct `AdmissionError` raise sites; it also reaches `admit_analysis_spec` afterwards. So the default path reaches several refusals and this was never "the one". The model's parallel comment was already narrow at the route overlay, so the delta brings the checker and contract into agreement with the model rather than adding a third phrasing. No residual instance of the phrase survives anywhere in the tree.

**3 — Selected-scope positive strengthened.** ⚠️ Assent **with required change 1**.

The direction is right and the assertion is true. Probing at the check's own execution point, `_adopt([_SCOPE_ROW_A], SCOPE_DOCUMENT)` raises nothing at all and returns the artifact dict — so it passes for the right reason, and the old `not in _SCOPE_DETAILS` form was genuinely weaker (any third refusal satisfied it).

The defect is that the predicate does not do what its own name says. The helper projects a caught `Refusal` to `exc.detail`, and `W.Refusal.__init__` defaults `detail=None`. An AST pass over all 85 `Refusal()` constructions finds 10 with no detail — **one of them inside `adopt_baseline` itself** (`workflows_model.v1.py:744`, duplicate baseline entries). Probed executably at the same point:

```json
{"dup_refused": true, "dup_error_code": "CONFIG.INVALID",
 "dup_detail": null, "dup_would_pass_new_predicate": true}
```

So `... is None` is satisfied by "refused with no detail" exactly as by "returned". This is present code in the function under test, not a speculative future control. It is **not** a live false pass — the fixture passes `entries=[]` — but the check name *"returns-without-any-refusal"* and `rootChanges[2]` *"reject any Refusal"* both outrun the implemented control. Root's scoping of the claim is otherwise accurate: this is a helper projection over caller-admitted inputs, not a closed-Run or output-schema claim.

**4 — coverageView fragment digest refreshed.** ✅ Assent; arithmetic checked independently and exact. `registered_schema_documents()` is the raw SHA-256 of each registered document's full bytes, so the correct value is the sha256 of the final schema file: I computed `f20b8353…`, identical to the fixture's new value and to the manifest `afterSha256`, and confirmed it **is** a member of the 6-element registered set while stale `b1fff…` is **not**. No self-reference hazard (the digest lives in `native-cases.v2.json`, not inside the schema it names).

The change is necessary, not cosmetic, and **the drift came from upstream**: the route overlay rewrote the schema `b1fff → 82745fa9` without touching the fixture, so at route-overlay state the fixture named a digest matching neither the file nor the registered set.

**5 — Durable fragment membership guard.** ✅ Assent. Non-vacuous under mutation (passes as shipped; fails on stale, empty, 64-zero junk, and valid-plus-junk — so the nonemptiness conjunct really does block the trivial-subset escape). Complete for its object: `coverageView` is the **only** fixture declaring `schemaDigests`. And counterfactually decisive — run against the route-overlay baseline it **fails**, i.e. it would have caught precisely the drift change 4 repairs. Root's framing is right and I don't overstate it: a set-membership test over a fixture's declared list, deriving nothing and replaying no Run — fixture-drift prevention, not full-Run qualification. It parallels without duplicating `identity-model.py:730`, which enforces the same membership dynamically inside the closure walk.

## 4. Check-count arithmetic

Independently corroborates root's 1592 expectation:

| Tree | Result |
|---|---|
| Reconstructed baseline | `{"passed": 1591, "failed": 0}` exit 0 |
| Final composition | `{"passed": 1592, "failed": 0}` exit 0 |
| With required-change-1 patch | `{"passed": 1592, "failed": 0}` exit 0 |

Exactly one check added (change 5); change 3 renames without changing the count.

## 5. Required change

**RC-1 — minor, precision. Does not block the six suites or the freeze.** Patch in `required-change-1.patch`: return a sentinel instead of `None` so the positive rejects any `Refusal`, matching its name and the manifest claim. `_adopt_scope_detail` has exactly one use site, so the change is local; verified at 1592/0. If root prefers zero code churn at this stage, the alternative is to narrow `rootChanges[2]` to "reject any Refusal *that carries a detail*" — but the code patch is the better fix, since the claim should not outrun the control.

## 6. Observations, scoped

- **Advisory, non-blocking.** `v20-root-augmentation.json` at the root of the proposed work tree still records `"nativeFixtureSchemaDigest": b1fff…`, which this delta supersedes. It is **not** a manifest file, is **not** changed by the delta, and has **zero consumers** — no reference to the file or the key exists anywhere in the final, route or combined-source trees. It is root staging residue (absolute `/Users/sb/code/…` paths, standing "not integrated or accepted"). **Not a semantic defect and no suite is affected.** Flagged only because it sits inside the tree proposed as source while stating a digest that same tree contradicts. Root's call: refresh or exclude.
- **Cosmetic, optional.** `native-evidence.md` l.788–789 wrap at 96/44 chars inside a block otherwise near 80. No line-width law exists in the file (281 lines already exceed 88), so nothing is violated.
- **Informational.** Changes 4 and 5 are the right shape together: 4 repairs the instance, 5 makes the class non-silent. I infer no further defect from the absence of equivalent guards over other fixture kinds — `coverageView` is currently the only fixture declaring `schemaDigests`, so the guard is complete for its object as the tree stands.

## 7. Limitations

- I ran **one** of the six suites (`check-identity.py`), twice plus two instrumented variants, because three of five delta changes live in it and the count arithmetic is the delta's own evidence. Root still owns all six after final pins.
- All execution was against **private copies**. `v20-final-source.v1` was never written to; re-verified afterwards that its `proposal.json` hash is unchanged and no `__pycache__` or stray file was created there. Parent untouched; all public evidence preserved.
- I assessed only the four-file delta and the 12-file composition — not the route overlay's nine-file semantics, not the preliminary source.
- `parentManifestSha256` unresolved in my scope.
- **My first post-hoc replay of the change-3 positive was invalid and I discarded it**: interrogating the namespace after the whole script ran measured mutated module state and disagreed with the real result. Only at-point instrumented figures are reported above; the invalid output is preserved as `work/probe/postsuite-replay-INVALID.out`.
- Detail-lessness reasoning used an AST pass over `workflows_model.v1.py` only.
- No product, readiness, durability or platform qualification is claimed or implied.
