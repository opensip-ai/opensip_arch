# S-M compiler definition join, partial r1

ACCEPT for `S-M-COMPILER-DEFINITION-JOIN-PARTIAL-R1`. The subject manifest is 19683 bytes, SHA-256 `aaad3e2d70a7bb6e6d8f43d22bc288c025685c3de83ded7ccfffcb93a52a3407`, with 85 sorted unique members. Every member hash matches the stage. Product HEAD is `5e83ea843e86d5fab3affa32a3d6bba5ac10ddbb` (`Bind reviewed DT-MD1 dependency transport digest recipe.`) and the product tree is clean. Architecture HEAD is `8ce1f5edae0cbe245367c83bef752e1b24013b4a` (`Select exact dependency transport manifest digest recipe.`). The only architecture porcelain entry is the untracked `docs/implementation/m3/syntax-e/e2s/` path, which is outside this unit. This spike is absent from both trees.

`design-lock.json` is 617760 bytes, SHA-256 `4d1e353b311624d297c010a5d08032fc1fb8357fe495f7309e5c003c13e0d0ae`: 140 inventory successors ending at inventory v180, 156 contract successors, and 103 inventory passage rows. The current lock already contains the bound dependency-transport digest successor. This unit does not change inventory, contracts, product code, or the status board.

## Joins reproduced from the staged outputs

`audit-original.py` was not executed. The same cross-query was recomputed from the 32 staged stdout files. Each external stdout named by `results-all32.json` hashes equal to the staged copy, and every staged stderr is empty. All 32 rows exit 0, record `afterAnalysis`, and record niceness 10. Each file has one `after_expansion` event and one `after_analysis` event.

The definition-id join holds on every unit. Header, lexer, and HIR signature-span rows share one definition-id set. Export rows cover every local definition id. Stable `defPathHash` values are unique within each unit. Each header's export flag and definition kind equal the export row for that same id. Joining every lexer token's text reproduces that header exactly, and the token texts cover the header length. The observations include 42359 whitespace tokens among the retained lexer kinds. Header kinds are 521 `Fn` and 6308 `AssocFn`.

The totals are 6829 function headers, 1994 expanded headers, and 40453 local definition and export rows. Displayed definition paths repeat: 4610 extra rows share a path with another row in the same unit. The revised check distinguishes those rows by compiler definition id. The stored `cross-query-audit.json` matches these per-unit counts. A path-keyed join would collide on those repeated paths; that older assertion is not the check used here.

The driver borrows the expanded AST, clones each function or associated-function item, and clears attributes and the body only on that clone before printing the header. The walk continues on the borrowed crate. Metadata emission is the compile output. The first-party sources do not assign these debug ids or path hashes as an admitted `nativeSubjectId`.

## Pins and scope

The pinned unit graph has 65 units. Its readiness file names the same 32 eligible indexes that succeeded here. The other 33 are excluded, with no overlap: 15 build-script or procedural-macro units and 18 units that depend on an unexecuted build script or procedural macro. The four input pins, seven copied compiler sources, and four architecture authorities match their recorded hashes. `driver.rs` is 10852 bytes, SHA-256 `d3cbe2156b58c27efaed104bc772c1dafa1458e3046534154ff9bcb4eb3e48ba`, matching `build.json`. The 34 external probe, map, and metadata pins rehash equal, including the prepared map of 7836 files. `build.json` records bare rustc, `CargoRun` false, child niceness 10, and a private directory mode `0700`.

After analysis, the 32 units record 343 prepared-map reads and 4 refused outside-map reads. The loader accepts only prepared-map paths. That is the recorded source-map boundary. `confinementClaimed` stays false. No repository build script, procedural macro, or corpus code was executed by this probe. No retained provider closure id appears in the first-party probe sources.

`completeSymbolCensus`, `signatureTokensQualified`, `actualFactCandidates`, `actualC2Context`, `repositoryCodeExecuted`, `sourceAdmissionClaimed`, `SMComplete`, `effectiveL`, and `productQualification` stay false. The printed headers are body-free function declarations. They are not a qualified `signatureTokens` census.

`verify_design.py` was not run. Architecture-only publication of this supporting evidence still requires this acceptance, root substantive assent, and the lead design check. No product, lock, or status-board change, and no push, follows from this acceptance.
