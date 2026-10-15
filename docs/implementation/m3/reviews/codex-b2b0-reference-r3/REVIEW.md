# B2-B0-REFERENCE-r3 review

**Verdict: ACCEPT-DESIGN-UNIT.** All four prior findings are resolved. No required findings or nonblocking observations.

## Subject and bases

Rehashed the 1,134-byte subject manifest, SHA-256 `bf2168eb694311f587d4a0ee23dddaa52d7089a409fec820ca0baad68f2ba40f`, and all five members. Every size and digest matches. The successor record is 2,964 bytes, SHA-256 `45008a6c43bad96b7d882aec778f605b2acbc3cd2c9c94e824b497a0b3b16660`. The reference is 12,574 bytes, SHA-256 `6714575ccee1474e2d7c20c4e5e9b6c95b498ad155ec1e69fc9d6ba5f3e7e32b`.

Verified product HEAD `94e5fdebd63a174694dadbb5e647063855614b77` and architecture HEAD `3b2a55d48c442b66d188369a4d8a9307fdaeb14b`, with clean tracked state. All eight sorted parent pins match accepted source/application manifests, earlier successor candidates or selected inventory. The four candidate pins cover the reviewed subject exactly apart from its included record. No passage overrides exist. With 163 bound successors, 164 is the correct next position.

## Prior finding closure

**B2B0REF-1 and B2B0REF-2 stay resolved.** The upward/downward evidence split and root-started second pass remain intact. Actual first-pass upward provenance is restored separately; below-root cwd/explicit spellings do not seed downward observations. Unexpected replay exceptions remain failures, exact successful coverage is asserted, and the injected consistency-fault checker control verifies passed=false and nonzero exit.

**B2B0REF-3 is resolved.** The adapter tracks directories whose interior was actually probed: selected root, listed directories, boundary probes and chain directories. Only those retain `vcs`. Pruned anchors retain their own metadata but no derived VCS annotation. Independently repeated the previous reproduction for all four reasons; `.opensip`, `node_modules`, `.git` and Cargo `target` now retain their pruned row without becoming nested repositories. Direct controls also supply hidden Git evidence and assert the entry-field projection. Other relevant synthetic fields describe the object's own custody state rather than hidden boundary evidence; retained ACL fields do not license reads or source admission.

**B2B0REF-4 is resolved.** The depth check now precedes child-boundary detection. A depth-257 directory is not boundary-probed and carries no VCS evidence; only its allowed marker names are observed. Depth-258 entries remain absent. Independently repeated the depth-257 config reproduction: `opensip.json` is omitted and no nested project is reported. Config and VCS controls exercise 256/257/258, checking both result boundaries and retained evidence.

## Reference assessment

The pinned SLM is unedited; current mode replaces its DD global with the exact successor-163 copy, while historical mode keeps the original DD. The changed reference behavior is confined to the observation adapter and partial V3 projection, preserving historical replay separately.

The population follows parent-first traversal, pruning before boundaries and exact-source confinement. Pruned entries contribute no children. Ordinary boundary directories retain their permitted detection evidence without admitting descendants. Explicit/config chains retain ancestor Cargo evidence, stop before a pruned prefix and preserve earlier crossing refusals; unrelated siblings are absent. The previous upward-overlap and depth controls remain present.

The two-pass mechanism preserves pre-finish refusals and requires root/source agreement. Pass-one upward provenance remains distinct from pass-two downward results. The V3 projection explicitly leaves workspaceDeclarations pending; shape-only reader fills are used in validation inputs and are not emitted as observations. The complete boundary inventory is derived through the bound V3 converter. No reader completion, product code or qualification is inferred.

## Checker and evidence

Ran the exact permitted checker, with temporary negative-control output confined beneath this review directory using TMPDIR and automatically removed. [checker-rerun.json](checker-rerun.json) is byte-identical to staged `evidence/checks.json`: 34,085 bytes, SHA-256 `7db7d5ce0d6c20735ad0220fd90e93162ae0e559d06afc4e484586c74cd19b15`.

All **36 controls** pass. The checker successfully replays and V3-validates all 64 discovery cases, explicitly classifies the four boundary-model cases, and validates all 35 accepted inventories. The rule swap and population cause no existing case outcome changes. The two removed `vendor/lib` observations are explained by explicit/config source confinement. Population checks, the four-reason projection controls, boundary-depth cases and the injected-fault negative control provide sufficient evidence for this reference unit.

Inspected the supplied reproduction and scratch verification reports. They agree with the corrected reproductions and name this exact subject/record, reporting base-lock and synthetic successor-164 binding compatibility. No scratch builder or full design verification was executed in this review. Actual lead assent, architecture publication and the separate product-lock binding remain subsequent steps.

## Boundaries

Used only permitted read-only inspection, hashing, JSON parsing, Git queries, the staged checker and reference imports over synthetic inputs. Ran no Cargo, tests, builds or lane; used no network, other panes or delegation; accessed no private fixture, installation directory, signing keys, held trees or T2 held-out entry. Neither repository, stage nor control files were edited. Wrote only `REVIEW.md`, `review.json` and permitted checker output in this review directory.
