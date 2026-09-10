I’ll implement the corrected atom law as executable full-scan reference plus the three draft files, using owner-admitted inputs only. First I’ll read the current drafts and locate `sufficiency_v2` / import-owner functions to reuse.I’ll apply the A–H law corrections in the three drafts, then implement `atom_model.v1.py` and the discriminating checks.Native `sufficiency_v2` imports cleanly. Next I’ll write the full-scan atom model and the discriminating check suite.Implemented the corrected atom law as executable full-scan reference over owner-admitted inputs. Frozen/live sources were not edited. **Not closed** — root still owns composition, schema3, findings, and gating.

## Files (isolated successor foundation)

| File | SHA-256 | bytes |
|---|---|---|
| `evaluator-projection-registry.v1.json` | `17072b4aaea01fff552d93227ff730c572cfa111b16fad706a22a326bb1871dc` | 55158 |
| `target-attribution.schema.v1.json` | `545dc06b46bd4c3bd0ae8f0500a4fcc4f80685ed836173051286a171abb7538b` | 11101 |
| `atom-evaluation-contract.v1.md` | `6db9ffe36abab22fd3fc60850e275e27da29057abff83809b3809263d0ae5a10` | 8717 |
| `atom_model.v1.py` | `84b05d65963006704ae4147f0c59f2ec4df44099f4ddbf9ffd50112a38db8f8d` | 55333 |
| `check-atoms.v1.py` | `4a57ada311388d661e196a0b9005d663922517921e1cf4dc70563ab216cfdcf4` | 31347 |

Helpers: `grok-atom-contract.v4/check-atoms.report.json` (`eb0b0bbc…`), `hashes.json`.

## Checks

`/tmp/opensip-architecture-review-env/bin/python -I -B …/check-atoms.v1.py` → **16/16**. Draft 2020-12 metaschema on both JSON documents. These are unit scans of admitted record maps, **not** full Run replay.

Covered: known-hit+partial ⇒ `none` false; unobservable-only ⇒ unknown; history empty complete `all-paths` ⇒ covered; scope *S*→*V* does not invent (*S*,*U*) and does not match the *V* fact; incoming `subjectKind` is source importer; same nativeId other *U* does not match; two-cap identical inventory is one identity; sidecar kind/external/evaluator-producer refuse; `file@enumerated` all-covered with `not-applicable`; resolved partial ⇒ `resolution-incomplete`; `neq export` and hex universe admit-refuse; `neq` other valid domain is true; `tests=[]`+`exitStatus=1` failed coarse; zero wrappers unknown without a gating bit; count>N despite partial sibling; `listed-paths` miss ⇒ outside/unknown; oracle flags refuse.

## Law applied (A–H)

- *E*=(*U*,*K*,*N*). Host ephemeral projection vs provider sidecar; unknown cannot override known; conflicts refuse; `producerClosure.kind=provider` only.
- Incoming scopes: all *S*-scopes **regardless of targetUniverse**; match facts with actual `targetU=U`; no empty Cartesian Coverage. Absence needs represented `CoverageResultV3` or `IncomingSearchAttestationV1`.
- `all-covered` calls `sufficiency_v2` (confidence/derivation/`DEPENDS_ON`). Non-resolved: existential+complete (`not-applicable` allowed). Resolved: universal-negative+complete.
- Runtime complete wrapper does not observe a missing/unobservable subject. History `all-paths`/`in-scope` may cover with no row; `listed-paths` miss is outside.
- Universe: closed domain enum; `neq` of two valid domains is true. Runtime subject scalars: `path` vs `symbol`, not a concat.
- Causes are a closed set; native `DeficiencyV2` is separate; gating is root/`evidenceUse`.
- API: `evaluate_atom(atom, subject, inputs)` returns known/uncertain ids and addresses, Coverage/scope ids, value, cause set, native deficiencies.

## Boundaries (root compose)

Does **not** evaluate boolean nodes, emit finding3, apply waivers, or mint proof3. Does **not** admit facts/imports/Coverage (precondition: already owner-admitted). Does **not** call repair `imported_requirement_outcome` (fingerprint-target). Reuses `native_evidence_model.v2.sufficiency_v2`. Enumeration plan/inventory files untouched. `identity-schemas.v3` / emission plan untouched. No product implementation.
