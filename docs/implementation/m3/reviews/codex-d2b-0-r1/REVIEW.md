# D2B-0-r1 review

**Verdict: REQUIRED-FINDINGS.** Product code: **ACCEPT-UNIT**. LD-D2B0-A: **REJECT** pending the authority correction below. No non-blocking observations. This is not product qualification or authorization to bind the unit.

Subject manifest: `8b5f799c471da120b1ac3d6c71cd2bafd9169aab8872f8da65786a9b02201119` (46,093 bytes). All 167 members rehashed successfully. Product base: `23b3871269c6553c96097084dd412b3aa95dec68`; architecture base: `ae83833d05d956a0562e188f0ad04fc37a63944b`.

## Required finding

### D2B0-R1-RF-1 — The manual-carrier branch exceeds the proposed plan amendment

**Location:** `d2b-0-r1/SCOPE.md:40-47`, LD-D2B0-A's replacement of the order bullets and §0 codec requirement.

Admission-only materialization now, with generation and the associated refresh deferred to the codec units, is supported by the evidence. However, the proposed alternative permits those units to write typed successor carriers and never generate them. This is a change to governing requirements, rather than simply a scheduling change:

- M3-D item 10, `supervisor-d/PROPOSAL-r5.md:381` (also r3:335), requires the decoded tree to be converted into **generated carrier types**. The accepted D2b plan expressly names this law as its authority.
- The accepted `fa-2/materialization-map.json` and `rust3-lim/materialization-map.json` standing passages require the implementing units to add source-map and admission rows, re-pin the registries and regenerate carriers. Their disclaimer that the maps do not fix those changes leaves implementation to the units; it does not waive the duties.

LD-D2B0-A quotes and replaces only passages of D2b PLAN-r3. It leaves these other obligations in force. A later codec can therefore follow its manual-carrier branch and still breach its governing sources. The schema checks and depth obligation do not resolve that authority conflict.

**Required correction:** either preserve mandatory generation in D2b-3/D2b-4, deferring the profile/annotation extensions and refresh to those units, or explicitly propose the necessary narrow amendments to M3-D item 10 and both accepted successor materialization obligations. An exception must preserve schema admission, the complete successor-aware depth computation, protocol separation, no serde wire decoding, and the refresh following every actual closure change. No product-code defect is alleged by this finding.

## Materialization assessment

The nine product paths match their archived candidates and product-map pins, including their base images. Both new schema documents are the exact accepted FA-2/RUST3-LIM bytes. The admission registry advances from 50 to 52 sources, retains 15 aliases, and equals the new architecture copy. The admission source map adds the correct accepted-source pins and selects that copy. Identity pins are correct and ordered; both embeddings follow pin order. The host count assertion changes to 52.

The two identity annotation additions enter the existing ignored-annotation branch; they add no evaluation behavior. The generator's selected pattern table does omit SubjectIdV1's pattern. The three named precedents are admitted but absent from generation sources. Walking the two new schemas confirms that their respective root law annotations are their only unsupported generator keywords. This supports deferring a separately reviewed generator extension.

No generator input/output, generated carrier, Cargo manifest/lock, census tool or blind receipt changes. The permitted live preflight passes: 99 tracked inputs/outputs/manifests/receipt checked, no differences. Unbound verification refuses the unselected architecture copy; accepting only that copy in memory yields 41 generation sources unchanged, 52 admission sources and 15 aliases. The permitted live operability source check passes, 114 rows and no findings. **Generator inputs are unchanged and the blind receipt stays current for this candidate.**

The successor's three parents match accepted inputs of the current product lock. Its 166 candidates plus its own record exactly cover the 167-member subject; source-authority pins verify.

## Handshake and deferred work

The recorded three-way derivation reports a clean merge equal to the current handshake. Independent JSON comparison confirms that all ten changed locations from the maps' common before-image through the RUST3-LIM image are retained in the current RCA-1 handshake. The 35,746-byte map after-image differs from the 38,182-byte current document by the later accepted RCA-1 changes; no handshake edit is needed here.

The namespace, source-mapping, definition entry-point and provider-entry-point decisions are assigned to the later generator-taking codec unit. LD-D2B-2's complete successor-aware closure and the codecs' schema checks remain explicit. The refresh procedure remains owned and required whenever the closure changes. These deferrals are coherent subject to RF-1: the manual branch cannot silently discharge the existing generation duties.

## Recorded controls and lane-base judgment

Reviewed the preparer, builder, preflight and lane runners as text; did not execute preparation, generation, builds or lanes. Attempt 3's logs support equal failure sets: identity 72/72 passes, evaluator 47/47, host 407/409 with the same eight failures, storage 137/137 with the same 33 failures. Host gains exactly the two successor tests: selection of every definition under its document pin, and representative shape boundaries/refusals. This is comparative regression evidence, not a wholly green suite.

Recorded rustfmt and all-targets warning-denied Clippy pass. Host schema-source tests pass 29, storage 1. The identity schema-registry filter matches zero tests; coverage comes from the full 72-test identity suite and the embedding tests. Census check, FW-01 (8), environment exceptions (10), operability and closure checks pass as recorded. The closure check has no changed-path intersection. All six mutants fail their specified detectors; Rust mutants produce test failures rather than compilation failures, and the admission-map mutant reports coverage mismatch. Attempts 1 and 2 are void history, not acceptance evidence.

LD-D2B0-8's focused post-rebase check is sufficient for this materialization. The intervening D2b-1 code and lock commits are disjoint from its nine paths; identity/lib.rs adds only the NFC helper and version export. The package-base check recompiles and compares the identity suite (72), host admission tests (10 passes, same eight failures), host schema sources (29), and storage schema sources (1); all results equal attempt 3, with the exact candidate pins recorded. It does not establish qualification of the later codecs or their integration.

Only the two requested review artifacts were written. Neither repository was edited. No prohibited stores, private fixtures, installation directory or keys were read.
