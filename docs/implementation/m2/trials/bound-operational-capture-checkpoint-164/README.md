# Named operational capture 164

Unaccepted cumulative candidate over163.344 product files:338 unchanged,5changed,1added. No product installation, reference selection, permanent custody or cumulative authority approval.

## Implementation

The recovery adapter's FileSource now requires RetainedDirectoryPath. All four witness/floor reads use a shared bounded actual-file reader that checks the complete retained root-to-leaf name chain before open, after open even when open failed, and after read. A relocated/substituted name is Unreadable(Context); failed observations remain Unreadable(Io). An open ENOENT becomes Absent only after a successful name check. Exact raw/empty bytes and existing byte-limit/context/refusal laws remain intact. The old descriptor-only helper retains its explicit caller-custody contract for lower-level mechanisms/tests; the bracketed adapter cannot receive that weaker type.

New bound_operational.rs owns this private composition. Its private sequencing hook schedules actual filesystem mutations only and cannot inject handles, open results, bytes or check results. The common reader remains in journal_store.rs; no duplicate parser or raw observation constructor is exposed. Current and inherited anchor semantics, at-most-two capture law and WAL release tests remain unchanged. The two other security files change only fixture construction to retain absolute chains.

Actual Claude161F1 is corrected at the platform boundary: ENOTDIR/ELOOP for a named child is a definite substitution and returns false. Other failures remain errors. Exact file/symlink/removed/replaced tests pin the distinction.161N2/N3/N4 are documented: OS aliases may resolve byte-distinct paths to the same identity; all ancestors require readable O_RDONLY directory opens (search-only ancestors unsupported); this public platform mechanism grants no security authority.161N1/N5 link-count/root/device comparisons retain their previously disclosed qualification limits; Linux is unexecuted.

## Evidence

126 security tests,42 platform tests and strict whole-workspace/all-target Clippy pass. Five new security tests cover exact raw/empty/missing/bounded behavior, actual leaf and ancestor moves at all three checks (including failed open), file/symlink replacements, permission denial, relocation between physical brackets, and pre-existing relocation through all four adapter read sites. Existing platform replacement assertion now demands exact false. Two baselines plus ten compiled mutants are caught, including skipping each check, checking only the leaf link, accepting a changed binding, misclassifying substitution, and bypassing each of the four bound adapter reads. Positive boundary client compiles; raw descriptor, private hook access and outliving binding clients all fail for the expected reasons. All36 fixtures unchanged. Final isolated host101:224sources,36fixtures,51cached dependency archives;355 workspace tests and2doctests pass.

Earlier security/Clippyr1 preceded one added adapter-only test; finalsecurity/Clippyr2, mutationr1,privacyr1 andhost101 use finalbytes. No failed product test. The author script plus beforeimages and final frozen source are retained; the later adapter test and formatting are in finalbytes/beforeimages-r2.

## Limits and next work

Named-chain sampling is not exclusion: ABA, changes after checking, owner/ACL/local-filesystem admission and future consumption remain host obligations. Detached bytes are historical evidence. No comparison of path strings establishes a journal/witness/floor identity relationship; SQLite path/sidecars and continuous custody/exclusion remain separate.124F1/118I2 are not closed.150F2 actual host mapping stays open; reference165 names its required unknown-custody route. Actual162T1's additional logical-byte and record-budget propagation tests are tracked for166, together with read-only carrier dispatch. No migration/witness/floor writes or writer authority are introduced.

The first, never-submitted freeze undercounted the passing workspace tests as352; final receipt counts355. Its bytes are preserved under freeze-r1; only this reporting correction changed before the submitted freeze.
