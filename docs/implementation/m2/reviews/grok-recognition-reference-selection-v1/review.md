# Recognition-derived reference selection v1 — scoped design-unit review

**Verdict: `ACCEPT-DESIGN-UNIT`**

Not Rust/runtime selection. Not full M2. Not a complete compiler Run or completeReplay. Frozen/live/history not edited.

Subject `docs/implementation/m2/recognition-derived-reference-selection-v1-subject.json` SHA-256 `18c63bd33fcd234fdec4f46c69498b6db27674ddd4859acb4d48ea9305aca020` (2810 bytes, **12/12** files). Successor `…/successor.json` 3599 bytes SHA-256 `4b771e6eea7c1565a5b7afbbad81d19bc9a3bce6a6e4250be695af5f96334711`. Candidates (11) are sorted unique and equal the subject minus the successor record. Parents (4) sorted unique and pin-match: feature_model, identity_model.proposed.v3, admission-runtime successor, exact-profile canonical. `passageOverrides: []`.

## What changed

One closed `h-identity` branch when `annotation.domain == 'native.framework-recognition.v1'`:

- require `retention==derived` and `form==sha256-text` else `RECOGNITION_IDENTITY_RECIPE`
- sibling `recognition` else `RECOGNITION_IDENTITY_PREIMAGE`
- `value == 'sha256:'+C.identity('native.framework-recognition.v1', siblings['recognition'])` else `RECOGNITION_IDENTITY_MISMATCH`
- **return** — no `PREFIX` lookup, no `visit`, no `admit_frame`

That is selected `feature_model.native_h` / **J-FRP-ID** (line 875), unchanged in the parent. Independently: remainder of `identity_model.py` is **AST-identical** to proposed.v3 after popping that one `If`. Capability `derived` and core/domainSet `h-identity` still call the original stubs.

## Bounded checks (portable `--architecture`)

`check-derived.py --architecture $ARCH` independently: **13/13**.

Predecessor KeyError reproduced. Matching inline id: no visit/frame. Refuses: wrong id, changed preimage, missing/non-object siblings, wrong form, wrong retention. Core `fact` still `visit(fact2:…)`. `domainSet` still `admit_frame`. Capability derived still records the id.

Schema-valid UnitRecognitionV1 uses selected source-selection FRP bytes (equal to live product `49aacd86…`) and accepted exact-profile canonical.

## Scope limits honored

- No generic derived skip.
- Feature J-FRP-EVIDENCE/ENTRY/SUMMARY/unit totality remain **mandatory** in feature admission; hash agreement is not those joins.
- Native-v2/report `preimage-frame` / `compilation-unit.v1` not broadened (foreign_payload only recurses `foundation/`; no reachable counterexample in this walker).
- Fully bound Plan claim remains schema+field reachability, not a compiler Run.
- Syntax fixture RunId in evidence is overlay `open_run_closure` (not completeReplay); AST remainder implies that fixture is unchanged by this branch. Did **not** re-execute the overlay graph (temporary paths).
- 1738 supplemental record cases not independently regenerated; bounded 13 is the portable gate. Rust graph04 is **not** selected.

## requiredFindings

None.

## shouldFix

`check-base-graph.py` / overlay 1738 scripts keep temporary paths. Use `check-derived.py --architecture`.
