Verdict: **changes-required**. Your fixes for R1–R4 hold up against my own probes, but I found two new small gaps in the checks you added. This is still a development-trusted-host adapter: not hermetic, not product integration, not M1 acceptance.

**Pins:** the manifest SHA matches before and after all probing, with all 79 files matching and none extra. Candidate-02's generator, node, rustfmt, python, the four libraries and the 140-file TypeScript tree all match the closure. All 28 source-map pins match the architecture checkout.

**What I ran:**
- **Baseline:** 586 schema refs checked, no drift across the 8 outputs. `test_generation` passes 18 tests and `test_dependencies` passes 9.
- **Test fixture:** it matches real `cargo metadata` output.
- **Round-01 battery:** all 46 adapter probes ported, plus 12 new adapter probes, 21 dependency-guard probes and a consumer-workspace feature probe.

**Inherited findings:**
- **R1 resolved:** unknown keywords and remote refs are refused, including nested ones. A nested `$id` is caught by the runtime check before the generator runs.
- **R2 resolved:** wrong output roles are refused.
- **R3 resolved as a guard against accidental misuse:** no `-I` or `-O` both refuse, and no asserts remain. Injected startup code can still overwrite `sys.flags` and get past it; I've put that under A1, since the entrypoint can't vouch for its own interpreter.
- **R4 resolved:** dev, inactive target, optional and `cfg(any())` declarations and root feature changes are all refused.
- **A5 and A9 resolved.** A4 is resolved as far as internal consistency goes. A3, A6 and A8 are partly resolved.
- **A1 still open:** the native library list and the entrypoint still verify themselves.
- **A2 still open, with new evidence:** the candidate-01 and candidate-02 generators were built from identical sources and lock. Their hashes differ but their outputs are identical, so the build isn't reproducible and an executable pin alone can't show which sources it came from.

**New required findings:**
- **NR1:** the superseded-handshake check matches exact refs only. Adding `…#/$defs/HelloV3/properties/protocolMajor` as an entry point is accepted with `--write`, and the type ends up in `report.ts` and `evidence.rs`. **Fix:** treat each denied ref as a subtree, refusing anything that equals it or starts with it plus `/`, in both `validate_options` and `flatten`.
- **NR2:** the dependency guard doesn't check the root crate's declared `[features]` table. An inactive feature `reviewer-rc = ["serde/rc"]` passes, and a consumer that enables it gets serde with `rc`. **Fix:** add `subjectDeclaredFeatures: {}` to the policy and require the root's feature table to match it exactly.

**Advisories:**
- **NA1:** the Python side strips a nested `$id` without comparing it to the owner. Only the runtime check catches it today.
- **NA2:** `report.ts`'s registry validates any ref you pass it, including unselected and superseded ones. That belongs with the TS runtime owner.
- **NA3:** a consistent edit across registry, options and source map is still caught only by review. An `--architecture` check of the source-map pins would close that.
- **NA4:** a test should confirm every allowed keyword that can contain subschemas is walked by both checkers.
- **NA5:** the runtime check writes its transpiled file into the generator's input directory.
- **NA6:** the source map is pinned as part of the tool closure, mixing tool identity with data ownership.

Before a hermetic recipe or product integration, the remaining work is:
- NR1 and NR2
- A1 (the native formatter closure, entrypoint trust and effect confinement) and A2 (build provenance)
- an explicit, verified offline provisioning lane
- full-run refusal tests using stub executables, and clean machine-readable output
- the protocol obligations and the separately pending inventory-successor and design-lock decisions

Files are in `/tmp/opensip-implementation/m1-generator-adapter-review-02`:
- review.json
- review.md
- logs/
- work/
