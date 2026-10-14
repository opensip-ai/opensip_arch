# Review: SM-U2A-DEPENDENCY-ARCHIVE-INTAKE-r1

**Verdict: REQUIRED-FINDINGS.** One scope-declaration finding, SM-U2A-R1-RF-01. No nonblocking observations. Archive consistency, intake custody, template construction and lock coverage pass independent checks.

## Required finding: SM-U2A-R1-RF-01

The request permits only paths, names, counts and messages to change against each accepted parent, with one explicit exception for the packet's per-name version total. REPORT.md describes the recipes on the same restricted basis.

The index script exceeds that constraint. Against its named parent prepare_sm_hierarchy_missing_public_indexes_r7.py, it replaces diagnostic parsing with eight-lock parsing and template-r116 archive-membership analysis (lines9–17), records pinned locks and lockedBy provenance, and adds a locked-version/checksum-presence assertion (line31). These are derivation, validation and receipt logic changes, rather than substitutions of names or paths. Its HTTPS transport, redirect refusal and anonymous request behavior remain unchanged, and the new lock-derived results are correct; the issue is the inaccurate declared delta.

Therefore **recipesDerivedOnlyByPathsCounts=false**. Declare these index changes explicitly in the request/report and revise the expected field to reflect their actual scope, or identify a genuinely matching accepted parent. Preserve verified evidence and the closed fetch/intake behavior. No new network acquisition, intake, tests or corpus resolution is needed.

## Exact subject and recipe review

Rehashed subject.json:9732 bytes, SHA-256 `a1bf3a387f1cc95b737252401ef7ad1dc8de641ad00c1fac80a0d6d96fd4bb71`. All39 members match their declared sizes and hashes. All five working U-2a scripts equal the staged scripts.

Diffed each script against its named parent. Archive acquisition differs only in paths and commentary. The packet adapts paths/counts/messages and correctly sums per-name publishedVersionRecords because this receipt lacks a top-level total; the retry-path selection is reduced to the supplied U-2a receipt. The intake runner preserves the closed entry/source/image checks and execution recipe, changing only paths/messages. Template construction retains file checking, overlap handling and raw-copy logic with new paths/count assertions. Four parent recipes independently equal their committed architecture copies. The index-script delta is the exception detailed above.

Live product HEAD is clean `95279fa8ae086f98bd221cd827f6c0efc156c0c5`; architecture HEAD is `f291975dfbfa76a12de94bb9d47c95cdc3e8227c`, with only the existing untracked held E2s tree, whose contents were not read.

## Names and archives

Parsed all eight generated locks independently with tomllib and rehashed their receipt pins. Compared crates.io package archive names against template r116. Recomputed exactly41 missing locked occurrences across23 names; every lockedBy entry equals this reconstruction. Every locked version/checksum occurs in its retained index. Staged index bytes match pinned external originals.

The23 retained indexes contain exactly1128 unique name/version records. The archive receipt's name/version population equals that whole population, including retained published versions rather than a selected winner. Every archive record reports success and matches both its expected supplied index checksum and the actual index row.

Rehashed **all1128 retained archive files**, exceeding the requested sample check. Every size/hash matches; the total is **292751770 bytes**. This establishes consistency with the supplied indexes, not source authentication or completeness against a live registry.

## Closed intake and template r117

The intake executable rehashes to the accepted entry image:76957192 bytes, SHA-256 `833dbc8a20471ed2efa061c7696bf2197d202d03d36df5a2f38ca286d486b722`. All six final source pins match. The recorded argv names this image and the lowercase supplied-entry function. The accepted entry subject hash matches its ACCEPT review and the U-2a receipt. The packet rehashes to its recorded pin.

The retained outcome equals the receipt's outcome and staged intake record:exit0, success,23 indexes,1128 archives/version records, whole supplied-index checksum matching and stock-cache serialization round trip. Inspected the closed source's checksum association and SpikeSummariesCache encode/parse path; these flags correspond to actual closed checks. No image or intake was executed during review.

Reconstructed template r117 as the union of r116 and intake output paths, with intake pins taking precedence. Its **11504 unique rows** comprise11054 archives and450 index files. All rows' sizes/hashes match the proper parent/intake pins and all11504 retained template files independently rehash correctly. Recorded total bytes equal the row sum.

The **47 overlaps** are exactly the path intersection:24 byte-identical archive overlaps and23 named index replacements. Each old/new pin matches its source; archive pins agree. No unrelated slot is replaced.

## Nine-lock coverage and standing

Rehashed all nine coverage lock pins and the template manifest pin. Recomputed crates.io row counts in listed order: **199,310,234,82,30,40,185,30,37**. Every row has the corresponding r117 archive with the lock checksum; missingArchives and checksumMismatches are zero for each lock, including axum.

This is archive intake and supplemental raw-cache preparation. No source authentication, native admission, corpus resolution, dependency-source-set completion, full S-M, L-G1, effective L or product qualification is inferred. Dependency-source sets remain U-2b; sealing/transfer series remain U-2c. The accepted PLAN-r3 retains D-2's activated admitted non-path set definition; archive coverage alone does not establish those sets. O7, D3 and D13 remain closed, with only L-G1 open among L gates; native admission is no extra gate on this outside-product experiment.

Only read-only file reading, hashing, parsing, source inspection and Git queries were used. No Cargo, image, intake, runner, tests, lane, network, panes or delegation. No private413 fixture, installation, signing keys or held-tree contents were read. Neither repository, stage, working directory nor control files were edited. Only this directory's REVIEW.md and review.json were written. Nothing was pushed. Lead assent and fresh design verification remain separate lead work after the scope correction.
