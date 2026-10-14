# Codex review: SM-RUST-SITE-CENSUS-r1

**Verdict: REQUIRED-FINDINGS.** One required finding, SM-SITE-R1-RF-01: the audit double-counts macro-expanded definitions in declaration aggregates. One nonblocking report-wording observation. The requested identity, variant, population, determinism, subject-count and non-completion fields otherwise match their expected values.

## Subject and boundaries

Manifest: `/tmp/opensip-implementation/sm-rust-site-census-r1-stage/subject.json`, 3,593 bytes, SHA-256 `1db9f9b16155e0f41d3f8d4936af6fb4994616f15a429863cadda51403d8009b`. All 15 members independently rehashed and matched. Prefix: `docs/implementation/m3/spikes/s-m-rust-site-census-2026-10-13`.

Bases checked live: clean product `95279fa8ae086f98bd221cd827f6c0efc156c0c5`; architecture `4bb9e62e39ce99d21cc629369e3c04179e6529c1`. Product lock remains 630,770 bytes, SHA-256 `6f041cb13f35f04092268c6906008bb060658fbfadb470b3fd03f2ea8b53c409`, with inventory187, 147 inventory successors and 161 contract successors.

No compiler, Cargo, driver, runner, tests, lane, network, other panes or delegation was used. No private 413 fixture, installation directory, signing keys or held-tree content was read. No repository, stage, producer or control file was edited. The expressly permitted audit was rerun and rewrote its existing external output byte-identically; only the two requested review files were otherwise written.

## Required finding: SM-SITE-R1-RF-01

`producer/site_walk.rs:22–23` records every observation in its base kind, and records an expanded observation again in the `kind.expanded` annotation counter. This is a valid way to retain a total and a subset separately.

The audit's `declares@syntactic` rule (`audit_sm_rust_site_census_r1.py:17`) selects every key starting `def.`. `offered_for` at line 25 therefore accepts both base keys and their `.expanded` subset keys. Lines 64–69 sum them into first-party/dependency declaration totals and per-covered-subject declaration distributions. Those derived totals count each expanded definition twice.

Independent aggregation of the raw first run gives:

| Ordinal/workload | Base first-party definition observations | Expanded subset | Published declaration total |
|---|---:|---:|---:|
| 0 / napi-rs | 69 | 2 | 71 |
| 2 / axum | 3,268 | 2,411 | 5,679 |
| 3 / hyper | 759 | 102 | 861 |
| 6 / tokio | 3 | 2 | 5 |

Dependency totals have the same error; napi's 54,433 base definitions plus its 17,777 expanded annotations produce 72,210 purported declaration sites. Per-subject distributions use the same predicate and inherit the error.

Labelling this grouping “offered” and “not candidates” correctly avoids inventing an emission factor, but does not make an annotation subset an additional observed definition site. M3-L r6 asks for actual compiler site counts as the decomposition input.

**Required correction:** omit `.expanded` annotation keys from base relation aggregates/distributions, or expose base totals and expanded subsets separately with explicit subset semantics. Preserve the raw events and by-kind counts, all population/coverage limitations and first-party/dependency separation. Regenerate and freeze the corrected audit output and its pins, then reproduce it byte-for-byte. Correcting this derivation does not require rerunning the compiler or corpus.

## Variant, walk and build

The closed source equals the committed framed-series source, 8,075 bytes, SHA-256 `43315ea6b81bd9b7a41174c1db41d50423b557ab6877be77db724ec96a7b75aa`. The 8,137-byte variant differs only in the requested extern/module pair, named TyCtxt parameter and one `site_walk::emit(tcx)` invocation after the closed timing event. No map, compiler-invocation or closed timing formula changes.

The walk counts local DefKind description categories through `iter_local_def_id`/`def_kind`/`def_span`; use resolution categories through HIR item/path resolutions; HIR expressions/paths/calls/fields/closures/bodies through an OnlyBodies visitor; and typed expressions/method resolution/receiver categories through the named TypeckResults queries. These are observation categories, not a selected candidate emission recipe. The pinned compiler's intravisit/map sources confirm the chosen item-like/OnlyBodies traversal. Its Span implementation recursively resolves `source_callsite()` to the outer source call site, consistent with the macro attribution description. `.expanded` is a subset annotation, which must stay separate when aggregating.

The bare-rustc SHA and driver argument lists follow the closed build recipe, using the same 1.95 rustc-dev sysroot, editions, optimization/dynamic/rpath/linker and explicit extern inputs, with the new source/output paths. Empty build logs are consistent with the successful recorded build; no build was rerun. The staged image is byte-identical to the build/runner image: 677,768 bytes, SHA-256 `d04be840c611ec01b65ff2fcb4c41bd0ec953150ace142ed2925880b89d14b9f`. Both linked-input pins and all five existing SHA-source pins rehash correctly. The recorded sysroot path matches the closed recipe and executor context; this review does not claim a new sysroot qualification.

## Runner and independent result checks

The executor and observer are unchanged and byte-identical to their committed closed copies, including their recorded pins: executor `721572db3859afd9d72ac1dacba495803c320135036ff5414474b571b4f37e85`; observer `b55cf3e457e17042d01a1a1184f53ff124708d183bbe29e03243d418a356cb6b`.

Source inspection confirms the runner acquires the owned lane directory before the complete run set, releases only its acquired lock, uses niceness10/private temporary output and runs `range(2)` per entry. It pin-checks the wrapper/executor/observer and source inputs, compares populations to the accepted pilot, and compares site events excluding only elapsed time.

Independently reparsed all nine two-run result populations and compared every `(unit index, standing, reason)` against the accepted pilots. All match. Each run's compiler count equals its launched-unit count; per-entry counts are 66,48,32,7,2,2,16,2,2, twice each, totaling **354**. Every launched unit has one site-walk event, one after-analysis event and completed analysis/metadata standing. All raw site event contents excluding `walkElapsedNanos` repeat exactly. Every site event says `sitesAreNotCandidates=true`; numeric site counts are nonnegative integers, and each expanded annotation is bounded by its corresponding base count. These successful repetition checks do not validate the faulty aggregate predicate.

## Audit and scope

Ran exactly the permitted `nice -n 10 python3 -I -B .../audit_sm_rust_site_census_r1.py`. It exited 0 and reproduced the staged output byte-for-byte: 22,761 bytes, SHA-256 `4aa7068c0c7b31e3faa8aecf196f8f39903cfce603a64a27e73fa5d135ffcef1`. Its external input/script copies match the frozen stage.

The audit verifies each selected T2 store tree, counts nonempty regular `.rs` files rather than symlink files, and constructs overlay subjects by admitted member mount. The seven repository S values match RUST3-LIM: 239,192,301,98,208,71,808. Both overlay entries yield S=279 (208+71), with no historical RUST3-LIM row fabricated. Every mapped first-party site file passes store-byte equality; no first-party site is outside the subject set. First-party and dependency units/counts are separated and the package/source labels agree with the pinned graphs.

No workload has complete subject coverage. Covered-subject counts are 4,0,19,18,0,0,1,0,0; **workloadsWithExactCoverage=0**. No SM-11 analysis/RSS quotient is derived. Site distributions over covered subjects are diagnostic site summaries, not SM-11 costs or SM-13 emitted-candidate values.

The relation labels use actual NE:590–601 spellings, including unresolved-edge; they do not assign stage grouping, requested keys, emission factors, census kinds or batching. The unit explicitly supplies neither fixed byte overheads nor a complete relation decomposition. Scratch, SM-13 per-stage values, SM-14, S-M completion, L-G1 closure, effective L and qualification are not claimed. Native admission is not imposed as an extra experiment gate.

## Nonblocking observation: SM-SITE-R1-NBO-01

REPORT.md's “use and extern crate items, with resolution” can suggest resolution observations for both. Source lines 90–94 record resolution categories for use items, but only an item count for extern crates. Clarify that distinction. The raw keys already distinguish the observations, and no semantic completeness claim depends on this wording.

This review does not accept the candidate for publication until the declaration aggregation finding is resolved. All accepted predecessor scopes remain closed.
