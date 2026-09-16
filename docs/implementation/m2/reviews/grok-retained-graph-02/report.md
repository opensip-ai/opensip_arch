# Advisory: retained-graph trial 02 (local walker)

Not runtime/M2 acceptance. Not `open_run_closure`. Not fresh-consumer identity. Frozen/live/history not edited. Graph03 is out of scope.

Subject `docs/implementation/m2/trials/retained-graph-02/subject.json` SHA-256 `5a47940bc04f458c709b0c4183099bb7cf3f5d52093cd2ea834a1b2b4a413b0f` (41687 bytes, **233/233** files). Archive `55afb0f78d75fdf5c3ff6a4b8a56ad7647704db8c12dc267f8ae58e8c192e7dd` (1473702 bytes). Private copy used; Cargo paths are relative inside the trial (`../product/crates/{identity,host}`).

## What it is

`inspect_local_structure` walks identity-v3 `$defs` over borrowed maps:

- local `$ref` `#/$defs/` (depth ≤ 8), sibling merge
- `oneOf`: unique `matches_node` hit, else `AmbiguousBranch` if any option `carries_digest`, else **skip node** (same as selected `walk`)
- printed `prefix:hex` → visit; `h-identity` with `domain` → `prefix:hex` visit; **no** `domainSet` H-frame (`Unsupported`)
- `by-domain` via sibling `domain` + `x-opensip-digest-domains.byDomain`
- raw-artifact blob rehash; `artifactClass` → Unsupported
- `{path,sha256,bytes}` length vs blob (exactly three keys)
- local `bundle` canonical-records: `C(bytes)`, `$defs/{kind}` admit, `ordered` / scope `.` exception / stage-spec **provider** role
- fragment / owner-retained / capability-manifest-id / foreign payload-class → `Unsupported`

`visit` memos object keys; **no** Run/project/Plan joins (oracle wrapper matches). `StructuralChecks` counts are not semantic/replay tokens.

## Missing vs invalid / hash

Aligned with retained-input plus walk:

- absent object/blob → unavailable
- mutate bytes **under the same digest key** → `BlobDigest` (root: old-hash mutation is detected)
- **rekey** (new SHA, descriptor still names old) → MissingBlob on the referenced digest; the new blob is not “the same object”
- length / noncanonical / `1.0` / role / identity mismatch → invalid
- Unsupported owner rows → `unsupported` (9 corpus cases)

No false **local-success** found versus the **restricted** oracle: 2520-line replay is byte-identical (`87/246/2178/9`). Domain `admit_json` still runs for local records before nested walk, so a bad `oneOf` on `vcs.commitId` fails schema rather than the skip path.

The inherited **zero-match oneOf skip** (no digest-bearing option) can omit walking that node; it is the selected model’s `walk`, not a graph02 relaxation. Do not read it as full-closure coverage of metadata branches.

## Budget / memo

`steps`/`depth` fail `Limit`. `descriptor_work` is **reused** per candidate/schema eval (same as trial01). Cycle memo inserts the object key before finishing `walk`; remaining fields of the first visit still run after the recursive return (not a grey-node false OK for this DFS).

## Reproduction

Private workspace `cargo test --offline --all-targets`: **68** tests (including 7 retained-input/graph host tests). Clippy `-D warnings` pass. Harness over frozen `requests.ndjson`: **2520 lines = expected.txt**. Independent empty-map inspect → `unavailable`.

## requiredFindings

None against the stated restricted local subset.

## shouldFix (later walker, not this freeze)

1. Do not treat oneOf skip as “branch validated.”
2. Do not treat reused `descriptor_work` as one graph meter.
3. Keep Unsupported for H-frame/`admit_native_context` (frame advisory).

## Limits

Did not regenerate 2520 cases from identity-candidate ndjson (replayed frozen corpus). Did not run native/compiler. Product `design-lock` in this tree is historical 9/12, not selection of these walker bytes. Full owner joins remain later (graph03+).
