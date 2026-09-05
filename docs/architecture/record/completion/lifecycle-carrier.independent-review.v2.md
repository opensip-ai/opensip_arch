# Independent lifecycle carrier repair review v2

**No objection within repair scope.** LCR-1 and LCR-2 are resolved in this subject; LCR-S1 is addressed. External replay reproduces **200/200**, byte-identical to the retained report. All six subject hashes remain unchanged.

Exact hashes, original repros and adjacent SQL observations are in [the review JSON](lifecycle-carrier.independent-review.v2.json). Freeze SHA-256: `0abd0839cb1797879ed77f5a476d2bd7b87fe28d774ed0171687124feee17656`.

The four original replacement paths now refuse through explicit collision guards. Required recursive triggers provide additional protection. Independent persisted-lease UPSERT probes preserve G1 after the project moves to G2, with recursive triggers both enabled and fault-injected off. Canonical string domains reject the original NUL suffixes and a same-byte-length middle-NUL digest through SQL CHECKs.

Successful publication, release, cleanup, rename, retirement, rollback, process-death and nonblocking lease probes still pass. No new MUST finding was identified in the scoped repair review.

Final distribution/security epoch, fence and registry adoption remain explicit integration requirements. No product/OS qualification, automatic acceptance/SATISFIED or register disposition is asserted. No subject bytes changed.
