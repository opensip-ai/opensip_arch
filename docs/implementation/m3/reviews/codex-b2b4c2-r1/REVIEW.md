# B2-B4C2-r1 review

Verdict: **ACCEPT-UNIT**

Required findings: none. One non-blocking observation is recorded below.

## Subject and authority

Rehashed the 7531-byte subject manifest (`edcb2febbd307c1456df89a057bbc0f2b1b88ade325b61f41def9636a3f3ed11`) and all 34 members; every size and digest matches. Checked every source authority pin and the product-lock pin. Product main is clean at `c1778a167502eb0f963802c64e75b6169052c65f`; architecture HEAD is `039db81fe5558b201d2e22ae92b50a66bf098a76`. Read plan r6 section 2.5, the owner decision, and the accepted B2-b4c1 r2 record.

Each product-map candidate equals its archived bytes and the candidate worktree. Both existing-file parent pins match main; the new receipt is absent from main. The candidate changes exactly the two declared existing files and adds the receipt.

## Run and receipt

The reviewed run script invokes blind mode once, after asserting a clean, equal-base worktree, an absent receipt and tool equality with main. The accepted B2-b4c1 r2 archived tool, main, candidate tool and run-record tool pin agree: SHA-256 `6ea8a1ab7ecad60220896790df6fb07aa53d2eac7efe7e6120a441b7b75c7dfd`. The script then invokes ordinary `--write` followed by `--check`. The recorded exits are zero. Captured stdout is exactly `Blind held-out census: 10 entries, 10 measured, 10 passing, 0 errors.` followed by a newline; captured stderr is empty. The script and reviewed blind implementation confine the blind tool's output to the receipt and summary. This conclusion about the historical run rests on the supplied script, run record and captured evidence; the reviewer did not repeat the blind run.

The receipt is 7249 bytes, SHA-256 `e859e7fc9ebe906753f583c93772c43e4dbc8f96d591287fdbf7ab08c7c86b02`. Checked the exact top-level and binding key sets and every measured-row field/value against the closed format. Its ten unique ids equal the manifest's held-out ids in order. All ten rows are measured, integrity/population true, with exactly three nonnegative integer margins and consistent true `passes2x`; there are no error rows or extra content fields.

Rehashed the manifest, tool, all closure files and every reference-loading input against current product/architecture. Limits and root lengths agree with the census; the successful independent ordinary check also validates the computed binding object, including sizes and code-derived caps. The smallest per-mille margins are objects 80,944, edges 39,008 and bytes 88,958; all exceed 2,000. The derived state is `holds (blind census)`.

## Composition and margin gate

Independently compared parsed base and candidate census records. Exactly ten entry rows change, each from its outstanding form to the precise receipt-derived blind-census form; the only other change is `heldOutMargin`. Every other top-level field and every lead-readable/workspace row is equal. `failingEntries` remains empty and `caps` remains `recorded-margin-holds`.

Read the unchanged Rust margin test and its closed-result classifier. Verified its entry, workspace and held-out identity digests against the composed record and manifest. It checks measured margins, state derivation, coverage, recorded failures and profile limits; the supplied six-test census log records all six passing, including the margin test. Together with the independently successful ordinary regeneration check, this supports the repository-entry gate. The reviewer did not run Rust tests. Every workspace full-ledger margin remains explicitly outstanding; neither B2-b nor the entire plan is claimed complete.

## Test adjustment and evidence

The only blind-test modification adds a receipt snapshot and replaces the absence assertion with byte-for-byte preservation. This remains correct both before and after a receipt exists: every abbreviated-argument refusal must preserve the initial receipt state. No other test behavior changes; this test file is outside the receipt's bound tool/reference closure.

Independently ran only the permitted checks in the candidate worktree:

- Operability source census: 114 rows, passed, no findings.
- Synthetic census controls: 18 tests passed.
- Synthetic blind controls: 19 tests passed.
- Ordinary census `--check` with the specified architecture, packages root and T2 cache: both generated outputs verified.

Inspected checks.json and the captured check logs. The three receipt controls each exit 1 with the expected census-output mismatch: a consistently marked margin tamper, a comment-only tool drift, and removal of the receipt. The control script restores original bytes and uses ordinary mode exclusively. The recorded security comparison has identical sets of 14 failures and 1128 passes at base and candidate; these are recorded results, not a reviewer rerun. The recorded verifier reports passed without product qualification.

## Scope and remaining work

No production caller, environment read, Rust source, law or schema is added. The run/check scripts and ordinary-mode dispatch preserve the held-out access boundary: only the previously reviewed blind mode opens real held-out stores. This review opened none. The owner-authorized historical blind run is assessed from its public receipt and evidence.

Lead assent/publication and the product commit remain subsequent steps. Inventory v200 must then add the new generated receipt. Workspace full-ledger margins and remaining plan work are outside this acceptance; no qualification or entire-plan completion is granted.

Non-blocking observation **B2B4C2-R1-NBO-1:** `source.json.contractSuccessorsUnchanged` says 164, while its exact pinned lock contains 165, as SCOPE.md and the request correctly state. The base pin and all substantive receipt/margin checks remain correct.

The reviewer wrote only REVIEW.md and review.json in the requested directory. No repository, worktree, stage or control files were edited. No compiler, Cargo, builds, lane, network, other panes or delegation were used; no private fixture, installation directory, signing keys or real held-out stores/overlays were opened.
