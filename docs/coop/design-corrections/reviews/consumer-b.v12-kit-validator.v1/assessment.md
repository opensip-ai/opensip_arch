I'll start from the kit itself: manifests, requirements, and the bounded syntax-code Run export, then reconstruct the closure/replay checks from the published laws only.I'll verify the kit hashes and read the bounded requirements before touching the Run export.Manifests are in hand; next I’ll hash-verify the 80-file kit and snapshot, then load the five contract owners and the syntax-code Run.Hashes match. Next I’ll inspect the syntax-code export and extract join/replay laws from the five contract owners.The replay script looks like identity remint, not full proof recompute. I’ll extract the join/replay laws and audit the rest of the export path.I’ll pull the exact C/H, snapshotJoins, coverage, and replay selectors from the contracts so the probes can be derived from law, not from the consumer helper.I’ll read the syntax-universe, relation-registry, and proof-verdict laws next so the probes can target those joins directly.I have the join laws. Next I’ll implement independent probes against the exported store, without treating the consumer evaluator as an oracle.I'll write an independent probe runner that loads the export, reapplies the published join laws, and records first refusal separately from later omissions.I'll correct my own policy-schema probe, independently recompute L0 body identity, and keep the original failures on disk.I have independent probe results and diagnostic corrections. Next I’ll write the scoped `review.md` and `review.json`.**Outcome: `PILOT_REFUSED`** for the first syntax-code Run export and its closure/replay implementation. This is not a whole-design verdict and not whole-consumer acceptance.

Kit custody passed: `consumer-input-manifest.json` SHA `ea2fa750ff863ef0bbfffb8bd2748dc4b776a7cbf4e43ddd4c8e6998214e6bf8`, parent SHA `a70f5830c9d54f5a6bc3285cb05c34fb6331d5278ae1c46e12147a5f95a10bbb`, **80/80** subject files, **37/37** snapshot files.

**First actual refusal** (after H-frame parse and identity-record schema): native context admission. native-evidence §1.2 requires the grammar bundle manifest and normalizer specification in the retained `kind=grammar` closure tree. Those blobs exist in the store and rehash, but they are **not members of `closure.tree`**.

Further independent static omissions on the same export, not hypothesized:

- `DeclaresPayloadV1` `container`/`declared` fail `SubjectIdV1` (`hello.rs` / `add`); the consumer never schema-checked that payload.
- L0/L1 body-identity **frames are not retained** under their 64-hex suffixes. Independently, the L0 *recipe* from the syntax `languageVersionBinding` **does** equal claimed `sha256:72a35a8b…`.
- Invented syntax-only unit with `unitOrdinal: 0` versus U-4 `null`.
- Three missing `SubjectInventoryV1` records.
- Replay from export prints the **saved** verdict. `proofCompareEqual` is reminted C self-equality. Tamper is C inequality of a mutated verdict field, not comparison of a freshly recomputed complete proof.

`newMustIssues` and `newShouldIssues` are empty: these are consumer corrections against existing laws, not design gaps.

Delivered: `output/review.md`, `output/review.json`, plus preserved probes in `output/diagnostics/`. Reproduce with:

```bash
/tmp/opensip-architecture-review-env/bin/python -I -B \
  /tmp/opensip-design-corrections/consumer-b.v12-kit-validator.v1/output/diagnostics/syntax_code_pilot_probes.py
/tmp/opensip-architecture-review-env/bin/python -I -B \
  /tmp/opensip-design-corrections/consumer-b.v12-kit-validator.v1/output/diagnostics/syntax_code_pilot_corrections.py
```
