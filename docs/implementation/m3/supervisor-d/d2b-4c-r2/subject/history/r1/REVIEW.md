# D2b-4c Rust3 successor/replay unit review

## Verdict

**ACCEPT-UNIT**

The frozen D2b-4c Rust3 successor/replay unit satisfies the reviewed acceptance boundary. The separately assessed repository inventory v238 candidate is **ACCEPT**. This verdict does not claim integration, inventory binding, the still-owed descriptions186 contract, status publication, push, or product qualification.

## Frozen subject and authority

- The frozen subject manifest is SHA-256 `e1b83b583fca33d03a39b5cc9715bfe8e0056b40322a8b6d821cca0c9bf552d8`, with all 910 declared members present and byte-exact and no undeclared subject member.
- All 35 candidate paths are byte-exact with the frozen product copies. The candidate worktree remains at product parent `0f5bbe492a40ff03c18262536f58c86e5af64be0` with exactly the requested 23 modified paths and 12 new paths.
- The 23 pre-existing path baselines match the frozen parent copies; the 12 additive paths are absent at the parent. The frozen architecture authority matches `fee2bce708521b653f37a324d03330c7edddde2a`, and the frozen product context matches the stated product parent.
- The product map covers exactly those 35 paths, adds no production caller or dependency, and keeps `productQualification` false.

## Rust3 successor assessment

- The implementation derives the census schema from the exact selected CompleteV3/CompleteSymbol schema, validates its fixed array and item-reference shape, and evaluates every row and examined path through the registered evaluator. It enforces row ordering, uniqueness, subject membership, canonical examined-path ordering, original received-node retention, and the 4 MiB received-CBOR limit. Its conservative typed upper-bound check rejects impossible over-limit counts without substituting a JSON-size cap; the exact-limit, one-byte-over, 100,000-row, and one-row-over controls cover the boundaries.
- The D-empty path constructs the required empty descriptor and validates its member set against the carrier source. Symbol request-key closure is accepted only with the C4-provided census cells and commitments. The code neither invents C4 selection authority nor assumes H's returned-symbol settlement authority.
- Signed-Hello token handling compares the exact HelloAck capabilities and identity versions before OpenUniverse. Reference tokens reconstruct the nonempty Rust subject set from the sealed manifest mapping with the established domain-subject recipe and verify both subject scope and domain commitment. The 1, 256, 257, and 513 reference controls, together with the no-token and oversized-inline controls, exercise the intended transition boundary.
- Complete census input is converted to the existing generated carrier while the original received buffer remains available for H. Terminal retention occurs only after accounting, table, conversion, and admission complete. Returned Coverage defers symbol scopes and counts only when C4 actually supplied a symbol census; nonsymbol coverage remains exact. Clean unavailable and budget-exhausted paths use the ordinary D-empty terminal coverage.
- The participant exercises all eight token combinations and the four null pairings, performs the raw pointer handoff once and only after terminal/ZeroExit/EOF completion, completes a partial Analyze write before one Cancel, and normalizes admitted input-rejected provider failure to the supervisor fault. The recomputation controls cover target attribution, census, and reference depth for both successors.
- No production caller, source39 expansion, C4 selection implementation, or H settlement implementation is introduced. Existing D2b-4a and D2b-4b behavior remains within its accepted boundary; the small shared policy, snapshot, dependency, and prepared-state edits centralize the inclusive sealed-manifest predicate needed by this replay.

## Historical replay assessment

- The frozen trial07 scope has 31 rules. Its 352 integer cases partition into 194 Rust3-scoped, 48 TS2, and 110 upstream cases, with the preserved raw floating-point ordinal refusal assessed separately as the 353rd case.
- The 20 Rust3 accounting cases use the actual recorder, size functions, and cardinality logic, including symbolic large-length inputs for the exact 64 MiB and 9 GiB boundaries. They do not require allocation of those large payloads.
- The sender replay covers 39 ordinary small cases plus the preserved 24-byte override and two large greedy-snapshot cases through the actual sender charging and chunk predicate. The original custody cases remain separately classified.
- The native full-scope audit contains 477 unique original case identifiers. Its step dispositions reconstruct exactly as 628 outside scope, 58 TS2, 34 current-profile literal refusals, 6 inherited table cases, 3 Rust predicate cases, and 2 shared-schema refusals. The six table cases remain present in the current Rust3 suite.
- The 34 literal views preserve their original bytes and framing. They are correctly identified as current selected-schema refusals, rather than relabeled as historical executor passes or later diagnoses. The two shared-schema boolean cases reject without integer coercion.

## Evidence assessment

- The base evidence records 362 component tests and 86 identity tests with empty failure sets. The final candidate evidence records 411 component tests, 86 identity tests, 136 focused Rust3 tests, and warning-denied all-target Clippy with empty failure sets.
- The final owning and repository evidence pins all 35 candidate sources. The mutation evidence contains eight distinct compiled runtime mutations: seven in the main mutation record and the separate nonsymbol-deferral mutation. Each records the intended witness failure, exit 101, and restoration. The later complete candidate run covers the final replay-only additions.
- Failed earlier census, reference, replay, and sender attempts are preserved as failed attempts and are not counted as acceptance evidence.
- The source census preserves the accepted owner annotations and accounts for the single ordinary census conversion row. Repository checks report success, receipt bindings remain current, and the package records no blind or private-data invocation.
- The admission carrier exposes 55 unique IDs. The duty table indexes the expected 36 Rust-or-shared rows, and its 88 source predicate hashes match the frozen source. I used the table as an index and independently checked the relevant source behavior.

## Inventory v238 candidate assessment

**ACCEPT**

- `docs/implementation/m2/repository-file-inventory.v238.json` is 803437 bytes with SHA-256 `a999a53ad099cbf10f8fd9bb482b46c9351b560438f32b18cf5134ca42e8cc6f`.
- Its parent `docs/implementation/m2/repository-file-inventory.v237.json` is 796271 bytes with SHA-256 `34bd48d05f737fdb9d6a543028a36d954b0888dcbc4b3387041a0324df697b68`.
- The successor record is 3678 bytes with SHA-256 `d353678ef33e105c713e483896eb35e631b31b25d56c69e911b8fe19b72dd89f`.
- The candidate preserves all 1,410 parent rows by value, removes or changes none, and adds exactly the 12 new D2b-4c paths. The resulting 1,422 rows are globally sorted and unique; packages, pending entries, and all other top-level data remain unchanged.
- The 12 new descriptions accurately state their file roles and authority limits. The mechanical meaning projection correctly combines the 145 inherited meanings with the five direct contract185 meanings, retains the original raw description across the accepted supersession, and reindexes all 150 resulting meanings to their v238 physical paths. The proposed inheritance record is the exact v238 rebind.

## Findings

None.

## Non-blocking observations

None.
