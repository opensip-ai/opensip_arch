# M3 implementation status r47

ACCEPT.

This is an operational status snapshot. It carries the accepted r46 ledger forward by value and adds two scoped records: the bound NCA-1 design choice and the accepted 24 key-carrier shape controls. Inventory stays at v184 with 144 successors. Contract successors stay at 161. The page counts 131 continuation records, and that count is a scoped evidence total. It is a count of records, and the major-unit families stay open.

## Subject and cutoff

Subject manifest `docs/implementation/m3/status/2026-10-10-r47-subject.json` is 7088 bytes, SHA-256 `e7130da737d96d03715ca112c3cf64544943b4c99d4778dbfa0e80ad13ee7239`, with one trailing newline. Its 33 members are unique, sorted, and byte-identical to the named files.

Live product HEAD `d4b7ce130406875e1ccf4647254bc457c3fb766e` is clean. Its subject is “Bind reviewed NCA-1 configuration association and key records.” It parents `e35fc24009e7be34ff1707b087379cc1b7d4811b`, and that commit changes only `design-lock.json`. Live architecture HEAD `ae07f234dede8dabe34dada88195a51800285bdd` matches the cutoff. Its subject is “Record actual native configuration key carrier boundary controls.” Its parent is `097fc1e8c503bca80d22d0982e97c83181c83d7b`. The only untracked architecture path is `docs/implementation/m3/syntax-e/e2s/`, outside this snapshot. This r47 directory is absent from that architecture head.

`design-lock.json` is 627281 bytes, SHA-256 `7798b8d47964e4e91a82e7dff6eb5efd965f6ab90c60dca67e01b8f29d2cd465`. It holds 144 inventory successors ending at v184 and 161 contract successors. The same cutoff is recorded in `accepted-work.json` and `source.json`.

## Inherited r46 snapshot

Twenty-six members match the committed r46 files byte for byte. They include the update protocol, the three C2a advisories, `decisions.json`, the combined-host evidence, the rejected-r1 and rejected-r35 history, the owner packet, and the post-review logs.

`history/previous-board.md` is the accepted r46 page: 77688 bytes, SHA-256 `5d2820b791f1395b3ed22f2b21c2c2dccc32786158aae41ef463c1719d1ecde1`. `source.json` pins that page as the previous original and as this snapshot, at architecture `35630f75be3e33a19d0bb511831bd5776fc02b95`. The historical subject is `docs/implementation/m3/status/2026-10-10-r46-subject.json`, 7088 bytes, SHA-256 `ec61766f9476c72fd421c2506de53d8d4f7437efb4c2832cbd06d31159846cfa`. The r46 r2 review is 366 bytes, SHA-256 `974f66c66382dd6797023e39d9fc865d1a6f249735ad62bc214c29ebc9966523`, verdict ACCEPT, 129 scoped records, inventory 184, and 160 contract successors. The r46 r2 lead assent is 1677 bytes, SHA-256 `21387b31f2ed37439d3b9688c3c68cb6415bcb6fa17af4fa6df4ba047e9ae27d`, status `ACCEPTED-OPERATIONAL-STATUS-RECORD`, unit `IMPLEMENTATION-STATUS-2026-10-10-r46`, with root substantive assent and an empty required-finding list. Those three pins match the architecture head.

The accepted-work standing is unchanged. Its first 129 records, `E001` through `E129`, equal the r46 records by value. The new records are `E130` and `E131`. The 131 identifiers are unique and contiguous.

## New records

`E130` records NCA-1 as an accepted design unit bound at contract 161. Its architecture commit is `097fc1e8c503bca80d22d0982e97c83181c83d7b` and its product reference is `d4b7ce130406875e1ccf4647254bc457c3fb766e`. The pinned review is 767 bytes, SHA-256 `ba8103cecb6051065c4a4e0d86790b57967dcca9713b0a10d3a132ca6c1edb4e`, verdict `ACCEPT-DESIGN-UNIT`. The record keeps the closed choice: root-inclusive nearest-first original discovery, legacy spelling with a malformed legacy file still selected, a distinct CC-5 census, same-attempt definition mapping, and complete key notation under the existing 64 and 256 Unicode-scalar carrier. It records 18 notation goldens, 1404 round trips, 1396 unique paths, and six typed refusals. Owned discovery, key classification, new numeric bounds, public failure routes, product implementation, owner admission, qualification, and the six publication duties stay open.

`E131` records the supporting key-carrier controls. Its architecture commit is `ae07f234dede8dabe34dada88195a51800285bdd`, and it names no product commit. The pinned review is 625 bytes, SHA-256 `826f82e53322b0a133a81e344821d025662f3e31d491fbb2cf5d7ec73f2fab09`, verdict ACCEPT. It records 24 first-party shape controls, a complete current registry check, and agreement with the Python reference at 64 and 65 keys and at 256 and 257 Unicode scalars, including the quoted-Unicode case whose 256 scalars are 510 UTF-8 bytes. The cross-population overlap is structurally valid. `crossPopulationDisjointnessImplemented` stays false, so semantic disjointness remains owed. Owned discovery, key classification, a published source profile, the six publication duties, owner admission, qualification, and plan completion stay false.

The binding ledger keeps all 48 inventory rows, v137 through v184, equal to the r46 ledger. Its first 63 contract rows equal the r46 rows and cover bindings 98 through 160. The added row is contract 161, the NCA-1 successor, review, and assent pins. Those 64 rows equal the last 64 successors in the current design lock. The lock tail is the NCA-1 successor `a5bbe9a8706f9bda38f969fea4947def007d3e750411f74e7736bbb45a0ccdcc`.

## Page, register, and checks

The status page differs from the accepted r46 page in the cutoff heads, the r47 links, the ledger sentence, and one new paragraph. Line 11 states 131 continuation records and contract bindings 98–161. The new paragraph records the NCA-1 choice, the 18/1404/1396/six notation results, the 24 shape controls, the structurally valid overlap, and the still-open semantic, discovery, classification, publication, and qualification gates. The C2a and CF register rows and the matching unit-register evidence cells gain that same short sentence. Every other unit-register row is unchanged. The register still holds 23 family rows, and its standing still withholds parent completion from child acceptance.

`checks.json` changes two fields from the r46 checks: `scopedRecords` 129 to 131, and `contractBindingsSinceBaseline` 63 to 64. Inventory bindings stay 48. `combinedHostLibraryTestsPassed` stays 289, and the four combined-host evidence files match the r46 bytes. The host evidence checks still expect 289 tests. That evidence remains the accepted r39 scope. `ownerAssentInferred`, `productQualification`, `entirePlanComplete`, `fullPublicationDutiesClosed`, and `actualNativeOwnerAdmission` stay false. `productTestsRun` stays 0.

`decisions.json` matches the accepted r46 file. O7 remains `ADOPTED-EXISTING-PROPOSAL`. D3 and D13 remain `SIGNED-OFF`. Their block lists are empty. The thirteen relative links on the status page resolve. `source.json` adds seven authority pins and leaves the previous 126 unchanged: the r46 r2 review and assent, the NCA-1 subject, unit, and review, and the key-carrier subject and review. Each pin matches the architecture head.

NCP-1 remains the closed contract-160 record inside the inherited 129. The new paragraph leaves that scope closed. No accepted law, inventory candidate, or product source is opened by this snapshot.

This review did not run `verify_design.py`. Under the standing ML5 rule, this acceptance grants no dependent gate. An architecture-only status commit follows this acceptance, recorded root assent, and a current `verify_design`. There is no lock, code, law, or inventory commit. Nothing is pushed.

Required findings: none.
