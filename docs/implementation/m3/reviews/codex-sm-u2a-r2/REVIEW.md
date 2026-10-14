# Review: SM-U2A-DEPENDENCY-ARCHIVE-INTAKE-r1, round 2

**Verdict: ACCEPT.** SM-U2A-R1-RF-01 is resolved. No required findings or nonblocking observations.

## Exact subject and resolution

Rehashed subject.json in `/tmp/opensip-implementation/sm-u2a-r1-stage`:10455 bytes, SHA-256 `8b5f757b5cbeb4719ddf27c756345f24ab438e5d68a77c9dc01d8a4ff8141b74`. All **42 members** match their declared sizes and hashes.

Compared against the retained round-1 manifest, whose SHA-256 is `a1bf3a387f1cc95b737252401ef7ad1dc8de641ad00c1fac80a0d6d96fd4bb71`. Of the original39 members, only REPORT.md changes. Additions are the original subject, exact original report and round-2 freeze script. The original report matches its original size/hash. All experimental scripts and data retain their original pins. The earlier review was not modified.

REPORT now explicitly declares the index script's lock-derived name selection, comparison against template-r116 archive membership, lock pins/lockedBy provenance and locked-version/checksum assertions. It distinguishes that delta from the unchanged anonymous fetch behavior, and declares the packet's per-name version total. The corrected request and expected fields scope these changes accurately. This resolves the round-1 finding without changing acquisition evidence.

## Recipes and names

Diffed all five U-2a scripts against the named parents again and confirmed working/staged equality. The fetch preserves anonymous HTTPS, proxy/auth/cookie absence, redirect refusal and index row checks. Archive acquisition, intake and template copy behavior retain their previously inspected parent algorithms, with paths, names, counts and messages adapted. The packet correctly sums per-name publishedVersionRecords; its supplied-receipt path replaces the parent's retry selection. The new lock-selection/provenance/validation logic is now an explicit reviewed delta rather than a claimed literal-only derivation. No version winner is selected.

Reparsed all eight generated locks independently with tomllib and rehashed their receipt pins. Compared crates.io archive names with r116, reproducing **41 missing locked occurrences across23 names**. Every lockedBy list equals the independent reconstruction. Each locked version and checksum occurs in the pinned retained index; staged index bytes match their external originals.

## Archives and closed intake

The23 indexes contain exactly **1128 unique name/version records**. The archive receipt has exactly that whole population. Every record's expected checksum and recorded SHA-256 equal its index row, with success and whole-checksum-match recorded.

Rehashed **all1128 retained archives**, exceeding the requested sample. Every size/hash matches, totaling **292751770 bytes**. “Whole version sets” means the complete captured index populations; it does not assert completeness against an independently queried live registry.

Rehashed the closed lowercase supplied-entry image:76957192 bytes, SHA-256 `833dbc8a20471ed2efa061c7696bf2197d202d03d36df5a2f38ca286d486b722`. All six accepted final source pins match. Recorded argv selects that image and the supplied-entry function. The intake receipt's accepted-entry subject hash matches its ACCEPT review and original subject. The packet matches its pin.

The intake receipt's outcome equals the staged entry outcome and intake record:exit0, success,23 indexes,1128 archives/version records, whole supplied-index checksum matching and stock-cache serialization round trip. These unchanged records correspond to the closed checksum-association and cache encode/parse checks inspected in round 1. No image or intake was executed during either review.

## Template r117 and coverage

Reconstructed r117 as r116's paths union the intake paths, with intake pins taking precedence. All **11504 unique rows** match the correct source pins, and all11504 retained template files were freshly rehashed. Counts are **11054 archives and450 indexes**; the declared total bytes equal the row sum.

The **47 overlaps** equal the exact path intersection:24 byte-identical archive overlaps and23 explicitly replaced index slots. Every old/new overlap pin matches its source. No unrelated file is replaced.

Rehashed the coverage record's template pin and all nine lock pins. Independently recomputed crates.io row counts in listed order: **199,310,234,82,30,40,185,30,37**. Every row, including axum's, has its r117 archive with the lock checksum. All nine missing/mismatch counts are zero.

## Scope and boundaries

Live product HEAD remains clean `95279fa8ae086f98bd221cd827f6c0efc156c0c5`; architecture HEAD remains `f291975dfbfa76a12de94bb9d47c95cdc3e8227c`. Its only existing untracked entry is the held E2s tree, whose contents were not read.

This acceptance covers archive intake and a supplemental raw cache. It grants no source authentication, native admission or corpus resolution. DS4-P1 dependency-source sets remain U-2b; sealing and transfer series remain U-2c. Archive coverage does not establish activated dependency-source sets. Full S-M, L-G1, effective L and product qualification remain false. O7, D3 and D13 stay closed; only L-G1 remains open among L's gates. Native admission is no additional outside-product experiment gate.

Only read-only file reading, hashing, JSON/TOML parsing, source comparison and Git queries were used. No Cargo, image, intake, runner, tests, lane, network, other panes or delegation. No private413, installation, signing keys or held-tree contents were read. Neither repository, stage, working directory nor control files were edited. Only this directory's REVIEW.md and review.json were written. Nothing was pushed. Exact lead assent and fresh design verification before architecture-only publication remain lead work.
