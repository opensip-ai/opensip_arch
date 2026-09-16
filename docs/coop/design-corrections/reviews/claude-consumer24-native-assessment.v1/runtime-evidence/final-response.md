All 11 of my assigned consumer24 findings are real design gaps; none is a consumer helper error. None was fixed between source37 and source38. Everything was probed against both sources and every result is identical. This is a nonblind coauthor assessment only: no patch, no acceptance, and nothing edited outside my runtime.

Custody checked out. Both source manifests and snapshots match exactly, all 102 consumer kit files match source37, and source38's parent is source37.

| Item | Disposition | Severity |
|---|---|---|
| M1 | Real gap across owners | MUST |
| M2 | Wrong record named in an identity annotation, hidden by a skipped check in the reference | MUST for a reader following the text |
| M3 | Real gap, plus the rule lives only in an excluded executable file | MUST |
| S1 | No registry exists, and nothing checks it | SHOULD |
| S2 | The level-specification join is unnamed | SHOULD |
| S3 | Two owners contradict each other | SHOULD (MUST if an empty default request can pass) |
| S4 | Identity-bearing field with no stated value | SHOULD |
| A1, A2 | Confirmed | advisory |
| A4, A5 | Confirmed; affect identity | recommend SHOULD |

- **M1:** Default analysis requires clone coverage over every file, including `package.json`/`tsconfig.json`. TypeScript and syntax universes must disclose "unsupported" for those files, so a default TS/JS Run can never pass. Rust has no such check at all, which is why the consumer saw Rust pass.
- **M2:** `nodeDigest` names the policy-1 `Predicate`, which refuses `endpoint` atoms that the v2 `Predicate` admits. The reference `close_run` still admits such a Run because it never applies the named record to fragments. Fixing the selector also needs that check added.
- **M3:** Nothing normative states the order of units and rows, yet reordered memberships are schema-valid with different digests. Run closure never recomputes membership. The consumer's chosen order is byte-identical to the reference model's. `discovery-defaults.py` doesn't contain the order either, so adding Python to the kit would make implementation the law without fixing this. A prose rule is needed.
- **S1:** The reference's own fixture seals a Run whose stage output schema is an unregistered fixture document, and `close_run` admits it.
- **S2:** Closure only checks that the level version is some retained blob, never joined to the grammar's normalizer specification. This one is static evidence only.
- **S3:** A repo with no markers gets zero capability requests by default, even though a syntax-only unit is representable and would request 10.
- **S4:** Setting `targetUniverse` to another universe, `null`, or an unbound hash is admitted and changes `executionInputsDigest`. The same change to `sourceUniverse` is refused.
- **A1:** There are 19 unannotated hash fields in two foundation schemas.
- **A2:** The v2 references resolve to definitions identical to v3, so there is no effect today.
- **A4:** Whether unread `node_modules`/`target` files belong in the snapshot inventory is decided nowhere.
- **A5:** The consumer's rule for the two JS flags disagrees with the reference in 4 of 8 configurations.

**For root:** the M1, M3, S2 and A2 remedies touch `enumeration-plan.schema.v1.json` or `native-evidence.schemas.v2.json`. Changing those bytes re-mints identities, so it needs a successor; prose and admission-check fixes can land without that. `identity-schemas.v3.json` and `execution-inputs.schema.v1.json` aren't registered payload schema documents.

**Limits:**
- Two first-pass probe defects (an unresolved schema reference, and registry rows I didn't sort) were corrected in a second pass; both attempts are kept.
- Probes use small inputs plus the maintained fixture; only M2 and S1 went through actual `close_run`.
- The consumer's Runs were read as evidence but not rerun.

Everything is in `/private/tmp/opensip-design-corrections/claude-consumer24-native-assessment.v1`; per-item selectors, file hashes, probe outputs and remedies are in `review.json`:
- review.md
- review.json (SHA-256 `aab1b8c6…6b78`)
- probes/probe_items.py
- probes/probe_items_v2.py
- receipts/
