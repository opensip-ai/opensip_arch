I’ll finish the v1 semantic-replay delivery into a new v9 export path, then fix the two root-identified atom defects with discriminating controls. First I’ll read the probe, the v8 root review, and the current atom/semantic files.I have the two probe defects and the extra join checks. Next I’ll patch atom completeness/admission, add discriminating controls, then export to a fresh v9 directory.v9 is finished. Both root v8 probe defects now match the required values, the original 12 native-admitted graphs still close, and two new full graphs cover the incoming partition law. Old v1/v8 receipts were not overwritten.

## Probe (now matches required)

| Case | v8 observed | required | v9 observed |
|---|---|---|---|
| one-U-partition-does-not-prove-other-partition-searches-U | `true` | `indeterminate` | `indeterminate` (`source-target-search-unattested`) |
| optional-other-program-unavailable-poisons-outgoing | `indeterminate` | `true` | `true` |

Reproducer still: `/tmp/opensip-design-corrections/probe-atom-v8-open-joins.py`. Fresh output: `/tmp/opensip-design-corrections/grok-atom-contract.v9/probe-atom-v8-open-joins.jsonl`.

## Atom corrections

1. **Incoming search of U is per source partition.** Complete *S→U* on A no longer skips B that only has *S→V*. Each partition needs *S→U* Coverage **or** a provider-owned whole-source attestation. Groups are seeded from selected program contributors, so a provider with no emitted scope cannot disappear.
2. **Outgoing completeness is the current U/source partition.** Same-family optional unavailable no longer adds blocking `unavailable-program-binding`. Cross-family still discloses `cross-family-edge-not-owed` and stays non-blocking.
3. **`completeSearch` override is provider-scoped.** Another provider’s partial *S→U* does not make this provider’s complete attestation structurally invalid. Incoming evaluation stays unknown until every owed provider is complete.
4. **Incoming `targetUniverse` must be an admitted selected native universe** (portable domain and/or selected program identity). An unattached digest is `INCOMING_SEARCH_JOIN` even if unused.
5. **Runtime overload:** `FUNK` / `overload-ambiguous` only if the current native ID is in the path/QN hit set of size > 1. An unrelated symbol is `nomatch` on that row.

Synthetic map probes are **not** compiler qualification.

## Checks

- `check-atoms.v1.py`: **56/56** (was 50). Six new discriminating map controls.
- `check-semantic-replay.v3.py`: **14/14** (10 owner+`close_run` positives, 4 reminted semantic refusals). Original 8 graph runIds unchanged from v1.
- New full graphs (native/schema/identity then public `close_run`):
  - `incoming-partition-s-to-v-unknown` — complete *S→U* on foo, complete *S→V* on bar, incoming `none` of foo is indeterminate (`run3:b50aba10…`)
  - `incoming-attestation-covers-other-partition` — whole-source U1→U1 attestation covers the *S→V* partition; incoming `none` is true (`run3:88bba202…`)

Optional same-family unavailable is the exact map probe plus `test_optional_same_family_unavailable_does_not_poison_outgoing`. A full `close_run` graph for that cell was not added: it needs an unavailable EnumerationPlan binding (deficiency/nativeCause/unavailable inventories) and was not required to close the defect.

## v9 export (fresh; v1/v8 untouched)

`/tmp/opensip-design-corrections/grok-atom-contract.v9/`

- `check-atoms.report.json`
- `grok-native-replay.v1.json`
- `exports/` — 10 run/objects/base64 positives
- `hashes.json`
- `probe-atom-v8-open-joins.jsonl`

`/tmp/opensip-design-corrections/grok-native-replay.v1/exports` still has the original 8.

## Owned eight-file hashes (SHA-256)

| File | sha256 | lines | vs v8 |
|---|---|---|---|
| `atom_model.v1.py` | `50f2e3087faa07cab107e4feab19e2bc38f0b161a6956fb5d9279fc4384698f8` | 1967 | changed |
| `check-atoms.v1.py` | `51e77ad99e517e3871e74a26351411381ec6408c30a10a22b8ced33d5a5a2370` | 1624 | changed |
| `atom-evaluation-contract.v1.md` | `32a1cb806473452a98ee8bd4507b3c41127a70dbcbb1f261203a4e9160b6667b` | 158 | changed |
| `incoming-search.schema.v1.json` | `fd5c51ea69068e77eb46c8d5090ef7eb481f55165310da09f958679c427a1277` | 344 | changed |
| `evaluator_semantic_fixture.v3.py` | `442b94a3505742f6bbe69592cac76e9696f40158ec1c3554734f7c2fdf43f800` | 728 | new/updated |
| `check-semantic-replay.v3.py` | `49116da6fefbf6e449216605808c7fb44697cc9aa864dc8ac38fd3f640b44c01` | 439 | new/updated |
| `evaluator-projection-registry.v1.json` | `e77be0dd65f431f94cc3c70153ec90509fb886d699755499e9a8237724ce5609` | 1635 | **unchanged from v8** |
| `target-attribution.schema.v1.json` | `788bd9d000fb1da830ef368d14c119f441f7b60e8a56f8da3467ef0fbf0ed90e` | 307 | **unchanged from v8** |

Root-owned files were not edited.

## Unresolved (not silent drops)

- These fixtures must later adapt to execution-manifest / execution-input v3 before final acceptance; that input is not wired yet.
- Real compiler extraction is not claimed. Synthetic compiler data is admitted by the actual native owner and full replay.
- No full native-admitted graph for optional unavailable same-family outgoing (map probe is the exact reproducer).
- Root `check-replay.v3.py` (38 controls) was not run here; it is root-owned.
