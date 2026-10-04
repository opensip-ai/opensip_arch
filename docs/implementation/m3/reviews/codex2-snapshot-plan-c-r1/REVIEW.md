# CODEX2 — M3-C r1 law review

**Verdict: REQUIRED-FINDINGS.** Four corrections are required: the complete analysis-spec is admitted before its inputs exist; the DS-2 extraction profile excludes Cargo-produced archives; the observation recipe nulls required schema fields; and the unit schedule does not support its critical-path claim.

Subject: `docs/implementation/m3/snapshot-plan-c/PROPOSAL.md`, 78,037 bytes, SHA-256 `ff9a5e8dc683b8ea98377ff833b98a87da09037c67b62429384d3ab04449ca69`.

All 26 supplied pins match. Product facts were inspected through Git at `30c5db1c1d2410135c5579f3a01ba6d152328bfb`, without changing the checkout. This is a law review only. No product code, cargo, tests, fetch, verification lane or lead run set was run; no delegation, repository edits or commits occurred. The real home and the 413 fixture were not accessed. Only review artifacts were written under this review directory. Digest and estimate scripts import only Python's standard library.

## Required findings

### C-R1 — Complete analysis-spec admission precedes its required snapshot and native bindings

**Location:** PROPOSAL.md:512, 523–535, 583–586.

Item 16 assembles and admits the analysis-spec at step 4. Snapshot sealing happens at step 6, dependency/prepared import at step 7, and context/universe binding at step 8. This cannot satisfy the assertion that each step consumes only admitted inputs.

COMP:9 requires exactly one `EnumerationPlanV1` parameter in the complete spec. `enumeration-contract.v1.md:13–24` requires snapshot inventory, `snapshotId`, admitted contexts and native universe bindings for available programs; its acyclic graph at :83–96 confirms these dependencies. Item 18 itself requires bindings covering every selected TypeScript universe's imports-cell population. An early spec must either omit required parameters, fabricate bindings, or acquire different bytes later. None is admission of the final committed spec.

**Fix:** Separate early capability selection/cardinality checks from complete spec construction. Admit the final spec after snapshot sealing, imports, contexts and universe binding, and before prospective-Plan bounds and `plan2`. Construct both required parameters from those admitted inputs. Preserve NE:4278's cardinality → schema → vocabulary refusal order at the applicable admission boundary. Add a control with an available native program showing that the admitted spec bytes equal the retained, Plan-bound bytes, without placeholders or later rebinding.

### C-R2 — The DS-2 ustar/regular-member profile excludes normal Cargo package output

**Location:** PROPOSAL.md:355–358, 378, 388.

The law promises deterministic extraction of locked `.crate` sources, but specifies gzip plus ustar and permits only regular-file members whose physical paths have the package prefix.

Cargo's published package writer creates GNU headers and calls `append_data`. [Cargo package source, source lines 899–911](https://docs.rs/cargo/latest/src/cargo/ops/cargo_package/mod.rs.html). That tar writer emits a GNU long-name control record, type `L`, named `././@LongLink` when a pathname cannot fit the header. [tar builder source, source lines 836–895](https://docs.rs/tar/latest/src/tar/builder.rs.html). Thus a Cargo-produced archive containing a regular file with a sufficiently long, otherwise legal path fails the proposed physical-member type and prefix tests. A strict ustar reader also does not describe Cargo's GNU header format. NE:1681–1684 requires authenticated tarball bytes and a host-computed deterministic manifest; it does not establish this incompatible archive restriction.

**Fix:** Define a bounded decoder profile that handles Cargo's GNU headers and required long-name control records. Allow only regular *logical output files*, validate the fully decoded effective path against the package prefix and LogicalPath grammar, and reject links, devices, traversal, duplicate effective paths and ambiguous/orphan extension records. Count metadata and decompression work against explicit bounds. Add a positive Cargo-compatible long-path archive control alongside the existing negative controls. A first-party decoder remains possible; using a library extractor is not required. Any deliberate unsupported-format restriction needs an explicit contract disposition rather than a claim of faithful DS-2 support.

This is source inspection of published producers, not a run of installed Cargo or a measurement of the pinned T2 corpus.

### C-R3 — “Every member null” is not an admitted observation preimage

**Location:** PROPOSAL.md:395–403, specifically :401.

NE:2708 spells the exact retained preimage as `ImportObservationV1 {schemaVersion:1, kind, window|null, population|null, selection|null, revisionRange|null}`. The workflow schema's `ImportObservationV1` at :246–264 requires all six members, fixes `schemaVersion` to 1 and requires a non-null import kind. NEM:401–402 likewise supplies the version and kind while nulling the four observation values. Literally nulling every member makes every generated wrapper's observation blob invalid.

**Fix:** Spell the record exactly: `{schemaVersion:1, kind:<dependency or prepared>, window:null, population:null, selection:null, revisionRange:null}`. Bind `kind` to the wrapper's kind and retain/hash this admitted preimage. Clarify that “no observations” refers to the four nullable observation values, and add a wrapper control for both kinds.

### C-R4 — The revised unit DAG increases the host-chain lower bound

**Location:** PROPOSAL.md:663–683; M3P-C at :655; item 19 scheduling at :609.

The unchanged-host-chain claim accounts for the C2 split but omits newly required C3 and C4 work. M3P:198 gives S/M/L durations of 1/2/3 days including review and integration. B2 finishes on day 5, C1a on 7, C3a on 10, C3b on 11 and C3c on 12. C4a depends on all C3, so it cannot start on day 10. Its L size then finishes on day 15, rather than the former combined C4/X12d finishing on day 12. Even allowing C2c authoring to finish early and ignoring all additional gates and run-set contention, H finishes on day 18 rather than 15. If C2c integration waits for C3b, the bound becomes later still.

The subject also uses five days for an L-sized C2b, while M3P assigns five days to hard XL work. Changing that assumption does not remove the C3c bottleneck. D1 being ready on day 2 removes its wait; it does not remove C3b's own unit duration.

**Fix:** Recalculate the full revised DAG, explicitly distinguish authoring from integration dependencies, reconcile C2b's size/duration, and update M3P-C and the host-chain claim. X12d can author beside H, but its required full X9 lead set must be serialized and complete before J2. Demonstrate that timing before claiming it contributes no delay. The scratch arithmetic in `schedule_estimates.json` is an optimistic counterexample, not a replacement measured schedule.

## Decisions on the requested questions

1. **Snapshot:** The walk, retained descriptor custody, no-follow/inode checks, refusal without retry, no late reads, and custody-backed byte retention are sound in principle against IE §3 and SL S3. Scope-independent capture correctly preserves config ancestors and lockfiles needed outside selected analysis roots. The closed TypeScript suffix set is a conservative host-declared read set at the permitted package granularity; providers must fault on any omitted file rather than extend it. The host-TCB caveat for pruned dependency trees is correctly retained. V2's `dirty:true` meaning fails closed and is acceptable through VCS-1; it cannot establish clean revision correspondence. The approximate 27,000-row arithmetic is sound, but the T2 overflow examples need the qualification below.

2. **Closure admission and V1/R1:** One signed admission route with synthetic signed fixtures is sound. CR-1 must update the host vocabulary, manifest schema and admission relation together. COMP:9 distinguishes closure identities/kinds; it does not forbid a distinct detector projection of the same authenticated core release. EC1 supplies the evaluator precedent. The detector projection includes the implementation bytes and document in the authenticated core tree, and its same-core join to the seal addresses LD-10. Rejecting a one-document tree is justified because it would not authenticate the detector implementation. CRC-1 must formalize the projections and joins before C2a. The adapter and provider-kind import-producer projections are sound only with the stated field confinement: they belong in import wrapper roles, are retained through selected imports, and cannot substitute for a semantic provider, detector, or evaluator input elsewhere.

3. **Imports and V3:** Null back-references plus identity equality to exactly one selected delivering import are a coherent proposed NIJ-1 recipe. The self-reference and config → snapshot → exact-snapshot import → config cycles are real. IE:1370–1373 does not require Plan import IDs to equal Config2's evidence import IDs; selecting native-input imports independently and retaining the union is sound. Snapshot-independent dependency set identity can coexist with snapshot-specific wrapper identity. X-2 is a real unresolved tension: the required payload path flows into payload digest, ImportId and PlanId, while WS:1539–1541 excludes user-input host paths from identity. A fixed harness directory is not a contract resolution. NIJ-1 must choose and encode the disposition before C3a. C-R3 corrects the wrapper's auxiliary observation record.

4. **DS/PO/launch:** DS-1's declared self-consistency, DS-3's declared locked-revision tree, DS-4's snapshot ownership and DS-6's activated-package completeness are sound; DS-2 needs C-R2. Bundled Cargo metadata through the private carrier is the required feature recipe, and treating it as a pre-Plan D-law tool launch is consistent with L's post-Plan provider cardinality rule. NE:1785–1791 is the direct metadata authority; NE:2499–2500 is the preparation ordering context. O7, D1 and D-law gating must remain effective. PO's inert kinds, media checks, bounds, four-way staleness binding, retained failure/fallback semantics and declared provenance are correct. Explicit-only prepared mode is a permissible M3 selection restriction, so PO-1's defaulted branch is unreachable here. R3 must settle the exact owner-manifest recipe before C3c.

5. **Harness:** Fetch-only network access, pinned tarballs, offline script-disabled installation accepted through Q0's canary, read-only workload copies, and declarative prepared fixtures preserve M3P:355 and Q0:688–692. Product import is not authorization to execute preparation. Deferring faithful T2 prepared-mode measurement follows from the M3 execution prohibition; declarative T1 controls cannot stand as that measurement. T2-DEP must carry the dependency pin and fetch/installation recipe changes before H-DEP/H-NM.

6. **Plan/X12d:** The fourteen member sources, minimal direct closure membership, exact budget/config equality and pack-derived policy fields are sound. Item 17 reproduces the prospective bounds, producer-boundary context check, first-overflow declaration order and corruption/request distinction. Complete spec construction needs C-R1. Item 18 correctly includes the TypeScript imports-cell symbol population and the distinct detector emission row. The release-pack corpus amendment is justified: at the reviewed product commit, `policy.rs:1361–1367` checks `RELEASE_PACKS`, while :1412's test registry is private and `cfg(test)`. Replay is the right point for the structural pack/core-detector joins before derivation. Regeneration must produce coherent admitted empty-population bindings, not merely erase old fixture fields. Pin amendments and an X9 rerun on the resulting exact commit remain required unit evidence.

7. **M3-L:** No intrinsic contradiction was found with items 1–17. Cache and regeneration keys are absent at M3; future reuse remains Plan-bound and changed-scope reuse remains successor-gated. Closure-shipped baseCfg, preserved config/scope bindings and the separate adapter launch fit L's boundaries. X-1 and X-3 correctly identify follow-up measurement/transport obligations rather than silently changing protocols. This review does not accept the draft L record.

8. **Successors/units:** The named identity, native, security, corpus and inventory successors cover the principal deliberate contract changes. X12-A and M3P-C are necessary record corrections. R3, X-3/R4 and the cross-law carrier/baseCfg/discovery questions must retain named dispositions and their relevant implementation gates. The code breakdown and X9-6/P0/L/I1 gates are broadly sound; C-R4 rejects its current schedule. Each contract successor still needs its own `ACCEPT-DESIGN-UNIT`; code and X12d still need `ACCEPT-UNIT` and `inventoryCandidateAssessment`.

## Nonblocking observations

- **C-N1 — Make bootstrap byte reuse explicit.** Items 1 and C1-T2 already require one project read site, so B1 configuration parsing and C2 installed-manifest resolution must consume captures made through that site. Spell out a capture session that starts before these bootstrap reads and reuses their retained bytes/rows during the later walk/read-set assembly. In particular, item 3's package.json read must not become a second read when the suffix walk reaches it. A rewrite between bootstrap resolution and sealing should neither change the resolved inputs silently nor produce a layout/config derived from bytes different from the inventory. This is an implementation-interface clarification under the existing one-read rule.

- **C-N2 — T2 tree counts are not snapshot counts.** All four quoted `blobEntries` values match T2M. A sample canonical row with a 50-byte ASCII path and a four-digit length is 150 bytes, 151 including its array separator, fitting 27,776 rows before the snapshot envelope. That supports the approximate estimate. T2's fetch tree includes entries the discovery walk may exclude; actual path lengths and file-length digits also vary. Rephrase “exceed” as a risk estimate until SM-5/SM-6 measures the admitted inventory and full canonical descriptor. S-R should remain conditional on that evidence and specify a new identity recipe plus bounds for the referenced inventory.

- **C-N3 — Keep acceptance and successor gates explicit.** The request includes L acceptance in this law's gate, whereas PROPOSAL.md:22 also permits unchanged draft INC text. Unchanged text is not L acceptance; follow the request's gate. Likewise, listing X-2 does not resolve it, and citing SL:1076–1082 does not itself specify an owner file-manifest construction recipe. Preserve NIJ-1 before C3a and R3 before C3c, with exact schema/recipe dispositions in their reviews.

`input_checks.json` records the supplied pin checks, supplemental authority hashes and size arithmetic. `schedule_estimates.json` records the stated planning assumptions and counterexamples. Neither is product validation or unit acceptance.
