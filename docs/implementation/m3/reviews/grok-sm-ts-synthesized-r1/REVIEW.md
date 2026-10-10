# S-M-TS-SYNTHESIZED-r1

Verdict: ACCEPT.

This packet is supplementary partial S-M evidence for one dev input. It fills no SM-2 or SM-8 placeholder, selects no workspace or nonregular policy, admits no production compiler or closure, and leaves L, qualification, and the plan incomplete. Acceptance grants no dependent gate. An architecture-only archive of this evidence still waits for owner root assent and actual design implementation verify. The review changes no product file.

The subject manifest is 10330 bytes, SHA-256 `c5220f5d5a9ceabab45b8d1d3d408a47b86b13e357d2ae2c89ee33a9b022a851`, schemaVersion 1, unit `S-M-TS-SYNTHESIZED-r1`, forty-five sorted unique members, each byte length and digest matched, one trailing newline. The spike directory contains those members and no extra file. The spike is absent from both repository heads. Product HEAD remains `25079c79575583b558753370d3918475209a05fd`. Architecture HEAD remains `6a5bc1338511f55f5f1394722679aad5dea630d2`. Porcelain on architecture is the untracked syntax-e `e2s` tree, outside this unit. O7, D3, and D13 stay closed. The accepted six-input cohort stays closed.

## Source and options

`source.json` pins the same two heads. Its four authority files match the architecture tree: provider-protocol L r5, the T2 corpus manifest draft, `native_evidence_model.v2.py`, and `discovery-defaults.py`. The generator closure matches the product tree, and its Node pin matches the recorded Node 24.16.0 bytes and digest. The pinned TypeScript 6.0.3 `typescript.js` bytes and digest match. The previous cohort report matches its pin, 4076 bytes, SHA-256 `dbabdd5701ebe764358c96e20482e474b62147edb9f629107004d250e0092bba`. Recorded flags keep repository execution, held-out inspection, qualification, and S-M completion false.

The synthesized branch in the native evidence model, when neither tsconfig nor jsconfig is present, uses synthesizer version 1 and the options `allowJs` true, `checkJs` false, `module` and `moduleResolution` `node16`, `target` `es2022`, `strict` false, `skipLibCheck` true, `types` empty, and `noEmit` true, adding `jsx` `preserve` only when a root ends in `.jsx` or `.tsx`. Program roots are the files whose suffix is in `.js`, `.mjs`, `.cjs`, `.jsx`, `.ts`, `.tsx`, `.mts`, or `.cts`, after the shared exact-segment exclusion of `node_modules`, `.git`, `.hg`, `.svn`, and `.jj`. `synthesized.cjs` implements that recipe. `resolutionCompletenessImplied` stays false in the model. `checkJs` false leaves JavaScript diagnostics off, and an absent external dependency tree leaves resolution unproved. A zero diagnostic count stays the compiler's report for this program.

The runner copies one T2 dev entry, `js-medium-express`, after `verify` has required the entry's tree and content digests. The packet records the returned digests and `heldOut` false. This review did not re-walk the corpus. The copy keeps regular files, follows no links, and checks inode, size, and timestamps around the read. The sealed inventory has 214 regular rows, zero nonregular exclusions, zero tsconfig names, and zero jsconfig names. No inventory path contains a dependency or VCS segment. The same filter predicts 141 roots, and all ten observations carry those 141 roots. None ends in `.jsx` or `.tsx`, and the recorded options omit `jsx`.

## Population and timing

Each of the ten stdout records is compiler 6.0.3, origin `synthesized`, synthesizer version 1, one configuration-free program, the options above, 204 Program files, diagnostic count 0, empty diagnostic counts, `dependencyTreePinned` false, `fullWorkspaceSemanticsClaimed` false, repository execution false, and emission false. Stderr is empty and the recorded exit is 0. The 204 Program files are the 141 JavaScript roots plus 63 declaration-library sources. The inventory pins 110 declaration libraries. The distinct successful reads are 205: those 204 files plus the root `package.json`. Blocked paths are empty. Every read path is in the sealed repository inventory or the pinned library inventory. The sum of those inventory byte lengths is 3384140, matching `readset-audit.json`. The audit script reobserves each path with no-follow, inode, size, and timestamp checks, a SHA-256 match, strict UTF-8, no UTF-8 BOM, and no UTF-16. The recorded audit says those checks matched, with an empty BOM list and zero UTF-16 reads. This review recomputed the path census and byte sum from the frozen stdout and inventory and did not re-stat the live tree.

The sample design matches the closed cohort's standalone timing scope. Ten separate processes run at parent and child priority 10, the first three marked warmup and the last seven measured. Whole-process time includes startup and sealed-data map preparation. On the seven measured processes the minimum is 255098916 ns, the median is 257128417 ns, and the maximum is 259056541 ns. `progress.json` carries the same median, maximum, and regular-row count. `wait4` `ru_maxrss` is stored with `rssUnit` `bytes` and `rssBytes` equal to `rssNative` on every run. That figure stays informational. The child environment is the parent environment with the private 0700 temporary directory set and `NODE_OPTIONS` and `NODE_PATH` removed, so HOME stays the parent value. The owned measurement lane is held for the set.

Wrapped public calls are present in each stdout: one `createProgram`, one options diagnostic call, one global diagnostic call, and syntactic and semantic diagnostics for each of the 204 Program files, 411 calls. On the seven measured processes the longest wrapped public call is `createProgram`, from 105494833 ns to 109893958 ns. Provider-protocol L defines SM-2 as a fresh-process Program creation plus a full semantic pass over the repository, in milliseconds, and SM-8 as the longest single synchronous compiler call inside that SM-2, the event-loop block. These whole-process spans and wrapped-call maxima are a different pair of observations. The closed cohort's Express row remains initialization only: zero matching configs and whole-process median 92756583 ns, maximum 93573084 ns. This packet leaves that row in place.

## Seven controls

`controls.json` records seven passing cases at priority 10, with `rssUnit` `bytes` and the lane held. The stage stdout and stderr agree:

- JavaScript root and TypeScript root: exit 0, empty stderr, one root, `allowJs` true, `checkJs` false, `noEmit` true, no diagnostics.
- TypeScript error: diagnostic 2322 once.
- Outside import: diagnostic 2307 once, and no read path ending in `/outside.ts` or `/outside.js`.
- JSX root: `jsx` is `preserve`.
- tsconfig present: exit 1, empty stdout, stderr contains `synthesized control requires no tsconfig`.
- jsconfig present: exit 1, empty stdout, stderr contains `jsconfig present; synthesized origin not established`.

Passing controls also record repository execution false and emission false. The controls exercise this synthesized branch. They leave production discovery and custody unselected.

## Open gates

The other five configured dev inputs from the closed cohort remain outside this program boundary: `poly-medium-napi-rs`, `ts-medium-powertools-lambda`, `ts-medium-smithy-typescript`, `ts-medium-umami`, and `ts-medium-vite`. Full configured coverage, workspace selection, nonregular policy, dependency semantics, the SM-8 event-loop span, Rust figures, and the complete S-M delta remain open. `SM2PlaceholderFilled`, `SM8PlaceholderFilled`, `SMComplete`, `LG1Met`, `effectiveL`, and `productQualification` stay false. No new law, numeric bound, product code, inventory row, or lock entry is in this packet.
