All 589 selected refs now have at least one witness that passes both the exact codec and the original schema, and no refs are left uncovered. The independent checker (`check.py`) passes with zero defects.

**Results** (from `result.json`)
- **Cases:** 1343 in total. 1161 were generated from the original schemas and 182 were seeded from the harvest corpus.
- **Coverage:** the generator alone covered all 589 refs. The seeds overlap 110 of them, so no ref depends only on a seed.
- **Uncovered and unsatisfiable:** 0 and 0. No budget was exhausted, and no "proved unsatisfiable" claim was needed.
- **Per ref:** at least 1 case; 15 refs have exactly one.
- **Size:** the largest witness is 2996 canonical bytes. Generation took about 4 seconds.
- **Weakest witness:** only `urn:opensip:product-v1:workflows:evaluator3:graph-query:3#/$defs/Params` has nothing but a trivial witness (`{}`). It's valid, but it tells you little.

**How witnesses were checked:** each case goes through `reference.typed`, then `canonical`, then `parse`, then an exact round-trip comparison. After that it must pass `reference.validate` and `ExactValidator({'$ref': ref}, registry).is_valid`. Schemas come only from `check_metadata.load()`, which verifies the 28 schema pins and the `canonical.py` pin. As a spot check, the check rejected all six deliberately broken values I tried: an extra key on a closed object, a float, an integer of 2^64, reversed utf8 order, a missing required token, and a boolean where a const was expected.

**How witnesses were generated:** a bounded depth-first search over the original schemas. It combines `$ref`/`allOf`, branches on `oneOf`/`anyOf`/`if`, and settles simple discriminator `if`s up front. It builds strings from their regex patterns and fixes up objects by following validator errors. Arrays respect `contains`, `uniqueItems` and `x-opensip-order`. Every candidate is re-validated before it's kept. I never read any generated Rust or TypeScript code. A search dead end is only called a proof of unsatisfiability if every pruning step was a sound schema contradiction. Any heuristic cutoff blocks that claim, but none of it was needed in this run.

**Worth knowing:**
- The first full run found 8 refs it couldn't cover. They were generator gaps, not impossible schemas:
  - Arrays that need several different `contains` elements: `RustCapabilitiesV3`, `TypeScriptCapabilitiesV2` and the Hello/HelloAck defs that use them.
  - `QueryDispatch.parityPaths`, whose key names can only come from `propertyNames`.
  
  I fixed both and regenerated.
- The `sources` list in `source-map.json` differs from `sources.json` in 6 metadata-v1/v2 local schema paths. I used `sources.json` as instructed and recorded the difference in `manifest.json`.
- The architecture repo has uncommitted changes. Its HEAD is recorded, but the sha256 pins are what the checks rely on.
- The 3 superseded Hello defs are still among the 589 targets.
- The harvest file's sha256 matched after the run, and I didn't change any original evidence. I made no commits.

Files are in `/tmp/opensip-implementation/m1-schema-witnesses-01`:
- witnesses.json
- result.json
- manifest.json
- seed-index.json
- generation-report.json
- generate.log
- generate.py
- check.py
- witness_common.py

Rerun with `../metadata-reference-env/bin/python -I -B generate.py`, then the same command with `check.py`.
