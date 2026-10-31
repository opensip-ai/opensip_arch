# C2b-1a non-admission slot terms, derivation r4: a line-by-line ledger (author, 2026-10-29)

**Status: author draft, the companion subject to funding-r3's derivation (coordinator LD-Q-6).** It is reviewed with
FUNDING-DERIVATION by the funding-r3 R3 reviewer, under one verdict.

**r4 answers funding-r3 REVIEW-r3's RF-2:** the DFS state population. r3 answered REVIEW-r2's RF-2 to RF-6. r1, r2
and r3 are kept unchanged. REVIEW-r3 found no other companion defect.

## r4 changes

| finding | change |
| --- | --- |
| **REVIEW-r3 RF-2** (DFS state not bounded by G) | The DFS terms are re-derived over **every discovered key, missing edge targets included**, from the actual push rules at U:459-481. U:438-442 reports a missing target but continues. U:476-478 then pushes every edge target, and U:474, U:475 and U:463 insert, push and re-insert each newly discovered key, whether or not it is a node.<br>**The bounds:**<br>- discovered keys **K ≤ 1 + E**, the entry plus the edge targets;<br>- key pushes ≤ 1 + E, plus K done markers, so **pops ≤ 2 + 2E**;<br>- **2K state inserts**;<br>- key lengths over **L_key = max(\|entry\|, \|e\|max)**, because a missing target can be longer than every node path.<br>**Knock-on fixes:**<br>- U:482-490's lookups search the state population K, not G;<br>- U:469's cycle fault is formatted over L_key.<br>New control **S10**: a missing-target fan-out graph (one entry node, 64 distinct missing targets). It measures state members, insert attempts, pops and allocation against these bounds. | §2 U:459-481, U:482-490; §3 U:469; §5 S10 |

**Product pin:** main `9815938`.
- Ledger rows are checked by `scripts/slot_ledger_check.py`: **S1**, each range contains its construct; and **S6**,
  every non-blank, non-comment line of every reachable function lies in exactly one ledger row.
- Prefixes: `R` = `crates/evaluator/src/native_retention.rs`, `C` = `native_context.rs`, `U` = `native_universe.rs`.

## r3 changes

| finding | change |
| --- | --- |
| RF-2 (populations equated) | §0.3: each input has **its own** census population:<br>- context components K_c, distinct from the stdlib tree's `.d.ts` rows D_s;<br>- context graph paths P_c, distinct from graph nodes G;<br>- the lockfile path λ.<br>Each loop, comparison, diagnostic and exit uses its own source population, maximum or length. Refusal cardinalities are re-derived from them (§3). New vectors cover unequal populations and missing long paths (§5). |
| RF-3 (declared length) | Every BLOB is **BLOB(β(d))**, where β(d) is the **actual** byte length of the retained buffer under digest d. It is obtained by a funded census lookup into C2b-1a's own retained map (§0.3), never from a descriptor's `bytes` field. An absent digest costs only its search. New vector: large actual bytes, small declared length (§5). |
| RF-4 (missing / wrong) | The ledger is now **line by line**, with S6 coverage. Fixes:<br>- C:116's second, owned `BTreeSet<String>` (moved strings: insertion terms, no clone or fold);<br>- every map and set uses its **actual key bytes and entry size** (§0.2's type table);<br>- `sha256_text` is priced as written: a 7-byte prefix check, a 64-byte scan, then 32 pair parses (§0.4). |
| RF-5 (refusal ownership) | §3 prices refusals **by ownership path**:<br>- C's moved `format!`, and C's `.into()` of a literal;<br>- U's `fault(&format!(…))`, which formats, then makes a second owned copy (U:345-347);<br>- U's `fault(literal)`;<br>- the layout's local `BTreeSet<String>`, its `Vec` collect, then a re-copy into the universe set (U:241-243, :283-292).<br>**Every attempt** is priced, whether or not the set deduplicates it. |
| RF-6 (not disjoint) | Terms are now **disjoint** by construction. No term contains an owner call, an admission, W-REC or a copy. §4 publishes **one occurrence matrix** and one split sum per whole call, including mint's R:377 copy. Funding §12 must cite this matrix (a note to the funding author). |

## 0. Rules

### 0.1 Primitives and the split

These are funding-r3's §2 and §3.7, used as published:
- `pass{0,k,b}`, `owned(b)`, `search(m,q)`, `digest_cost(n)`, `btree_insert(m,key,entry)`, `growth(n,size)`,
  `formatted(n)`;
- `CLONE(x)`, `EQ(a,b) = {0, N(a)+N(b), B(a)+B(b)}`, `PARSE`, `FOLD`.

Two derived forms:
- `field(o,k)` is `search(K_o, |k|)`, with K_o the object's census member count;
- `BLOB(d)` is `search(|blobs|, 32)`, plus `digest_cost(β(d))` when d is present.

**The split** is SLOT-DERIVATION-r2 §0.2's table, unchanged:
- **allocation side:** owned, growth and formatted; the meter prices; the node part of btree_insert; CLONE's owned
  parts; FOLD's growth and owned parts;
- **pass side:** everything else.

Each ledger row gives both sides.

### 0.2 Collection entry sizes (64-bit; funding §2's sizes)

| collection (site) | key bytes | entry size |
| --- | --- | --- |
| R `inventory: BTreeMap<String, V>` (R:100-103) | \|path\| | 24 + 32 = 56 |
| R `frames: BTreeSet<(String,[u8;32])>` (R:284) | \|set name\| + 32 | 56 |
| R `blobs: BTreeSet<[u8;32]>` (R:182, :285) | 32 | 32 |
| R `closures: BTreeSet<String>` (R:257) | \|key\| | 24 |
| C `selected_set: BTreeSet<&String>` (C:101) | \|fold s\| | 8 |
| C `options_lib: BTreeSet<String>` (C:112-115) | \|fold h\| | 24 |
| C second set `BTreeSet<String>` (C:116, moved) | \|fold s\| | 24 |
| C `by_component: BTreeMap<&str,&str>` (C:129-139) | \|name\| | 32 |
| C `declared: BTreeSet<&str>` (C:145) | \|name\| | 16 |
| C `digests: BTreeSet<&str>` (C:168-171) | 64 | 16 |
| C `refusals: BTreeSet<String>` (C:187) | \|r\| | 24 |
| U `inventory: BTreeMap<&str,&V>` (U:182-185) | \|path\| | 24 |
| U `paths`, `context_paths: BTreeSet<&str>` (U:193-200) | \|path\| | 16 |
| U `by_path: BTreeMap<&str,&V>` (U:425-428) | \|path\| | 24 |
| U DFS `state: BTreeMap<&str,i32>` (U:459-474) | \|path\| | 24 (16 + 4, padded) |
| U DFS `stack: Vec<(&str,bool)>` (U:460-478) | — | 24 per slot |
| U `installed: BTreeSet<&str>` (U:279-282) | \|install\| | 16 |
| U layout `faults: BTreeSet<String>` (U:283-292) | \|f\| | 24 |
| U `refusals: BTreeSet<String>` (U:342-346) | \|r\| | 24 |

### 0.3 Census populations (RF-2, RF-3)

Each population is taken from its own record by the fused census funding-r3 §8 charges. Extra per-element charges
are stated and funded before they run.

| population | its record | extra charge |
| --- | --- | --- |
| R, \|p_i\|, \|row_i\|, max \|p\| | snapshot `sourceInventory` | running max {0,1,0} per row |
| S, \|s_k\|, c_k, max | context `toolchain.libSelection` | {0,1,\|s_k\|} for scalars; max |
| H, \|h\|, c_h | context `honoredOptions.lib` | {0,1,\|h\|} |
| **K_c**, \|κ\|, max | context `standardLibraryComponentDigests[].component` | max |
| **P_c**, \|π\|, max | context `configProjection.configGraphPaths` | max |
| **λ** | context `lockfileIdentity.path` (0 when null) | — |
| T_s, D_s, \|δ\| (basename), max | the stdlib closure's `tree` (D_s: rows whose `path` ends `.d.ts`) | {0,1,5} per row; {0,1,\|path\|} per matching row; max |
| T_t | the toolchain closure's `tree` | — |
| G, \|g\|, E, \|e\|, max | graph `nodes[].path`, `nodes[].extendsResolved[]` | max |
| Y, \|ι\|, \|ρ\|, max | layout `entries[].installPath`, `.realPath` | max |
| P, J, \|root\|, max | universe `programRootFiles`, `jsRootFiles` | max |
| Q | the universe's `synthesizedOptions` member count (0 when null) | — |
| **β(d)** for every referenced digest d | C2b-1a's retained blob map | search(\|blobs\|, 32) + {0,1,0} per reference |
| K_o for every object read | the census member count | — |

Registry rows are constants of the pinned identity-v3 `domainSets` and the evaluator registry (F1, F2).

### 0.4 Shared helpers

| helper | source | allocation | pass |
| --- | --- | --- | --- |
| `field`, `text`, `array`, `string` | C:44-67; U:43-63 | — | field: search(K_o, \|k\|); text/array: {0,1,0} |
| `sha256_text(s)` | U:64-81 | — | {0,1,7} (prefix) + {0,1,0} (length) + {0,64,64} (scan) + 32 × {0,1,2} (slice) + {0,32,64} (parse) |
| `raw_digest(v)` | R:140-142 | formatted(71) | text {0,1,0} + `sha256_text` |
| `optional_rows(v,k)` | R:131-139 | — | field + {0,1,0} |
| `spend(depth)` | R:144-150 | — | {0,1,0} |
| `path(v, p)` with step widths w_0 = 1, w_1, …, w_n | R:151-167 | owned(8) + Σ_t growth(w_t, 8) | Σ_t [{0,1,0} + w_{t-1} × ({0,1,0} + {0,1,2} + field)] |
| `blob(d, len)` | R:168-184 | btree_A(\|blobs\|, 32, 32) | {0,1,0} + BLOB(d) + (len: {0,1,0} + {0,1,0} + {0,1,0}) + btree_P |
| `fault(&str)` | U:345-347 | owned(\|s\|) + btree_A(Ref_u, \|s\|, 24) | btree_P |
| `refuse(impl Into)` | C:186-188 | moved `String`: btree_A(Ref_c, \|s\|, 24); `&'static str`: + owned(\|s\|) | btree_P |
| `nested_record` wrapper | U:297-319 | growth(\|rows\|, 8) + formatted(71) | per registry row: field + {0,1,0} + EQ(\|key\|); {0,1,0}; per path step: field; EQ(null); `sha256_text` |

### 0.5 Totality, the prefix rule, and T/L/N

These are r2's §0.5 and §0.6, unchanged, with one addition: every count above is the census count of the value as
given. On any accepted shape, a source exit performs a prefix of the full path. The allocating exits are priced:
- R:224 and R:238: owned(\|π\|max) and owned(λ);
- the host's Debug mapping: C2b-1a's own code.

**T/L/N: none.**

## 1. T-WALK-ROOT and T-WALK-CTX / T-WALK-UNI (retention, excluding admissions, owners and copies)

| range | construct | allocation | pass |
| --- | --- | --- | --- |
| R:86-92 | `budget.steps == 0` | — | {0,1,0} |
| R:93-99 | `IdentityDomain::Snapshot` | (T-SNAPSHOT: funding) | (funding) |
| R:100-103 | `sourceInventory` | Σ_i [owned(\|p_i\|) + CLONE_A(row_i) + btree_A(i, \|p_i\|, 56)] | field + {0,1,0} + Σ_i [field(row) + {0,1,0} + CLONE_P(row_i) + btree_P] |
| R:104-113 | `NativeRetention {` | — | {0,1,0} |
| R:114 | `walk.frame(digest, set, 0)` | (the frame rows below) | |
| R:115-120 | `NativeRetentionChecks {` | — | {0,3,0} |
| R:131-139 | `fn optional_rows` | (§0.4) | |
| R:140-142 | `fn raw_digest` | (§0.4) | |
| R:143-150 | `fn spend` | (§0.4) | |
| R:151-167 | `fn path<` | (§0.4) | |
| R:168-184 | `fn blob(` | (§0.4) | |
| R:185-200 | `fn blob_joins` | per join: path; per node: raw_digest + `blob` | optional_rows; per join: {0,1,0} + field; per node: 2·field + field(lengthField) + `blob` |
| R:201-246 | `fn snapshot_joins` | context only: 2 joins. configGraphPaths: path(1,1); lockfile: path(1). Exits R:224/:238 per §0.5 | optional_rows + per join {0,1,0}; per node EQ(null) + {0,1,0} + field(form) + EQ(form); configGraphPaths: P_c × [{0,1,0} + {0,1,0} + {0,1,0} + search(R, \|π\|)]; lockfile: 3·field + 2·text + search(R, λ) + field(sha256) + EQ(64,64) |
| R:247-268 | `fn closure(` | owned(\|key\|) + btree_A(\|closures\|, \|key\|, 24); raw_digest(manifest) + `blob`; per tree row: raw_digest + `blob(len)` | {0,1,0}; (object: T-CLOSURE, funding); field + {0,1,0} + EQ(kind); btree_P; field(manifestDigest); per row: 2·field + `blob(len)` |
| R:269-281 | `fn frame(` | — | {0,1,0}; (frame_candidate: T-FRAME, funding); {0,2,0} |
| R:282-283 | `// The inputs are immutable` | (comment) | |
| R:284-287 | `self.frames.insert` | owned(\|set name\|) + btree_A(\|frames\|, \|name\|+32, 56) + btree_A(\|blobs\|, 32, 32) | btree_P ×2; snapshot_joins + blob_joins as above |
| R:288-323 | `nestedRecords` | per reference: path(1) + raw_digest + `blob(None)`; then the record's `blob_joins` (layout: path(1, Y)). INSPECT and W-REC: funding | optional_rows; per join: {0,1,0} + field(form) + EQ; per reference: EQ(null); 2·field (document, selector) |
| R:324-348 | `nestedIdentities` | — (empty in both TypeScript rows) | optional_rows: field + {0,1,0} |
| R:349-358 | `closureJoins` | per join: path(1,1); key: owned(\|id\|) (identity form) or formatted(9 + 64) (suffix form) | optional_rows; per join: field(path) + field(form) + EQ + field(kind) + text; then `closure` |
| R:359-370 | `contextField` | path(1) (bind) | {0,1,0} + field + {0,1,0} + field(contextForm) + EQ + text + `sha256_text`; then `frame(context)` |
| R:371-379 | `inspect_native_context(` | (T-OWNER-CTX; the copy is COPY-R377) | {0,1,0} |
| R:380-402 | `inspect_typescript_universe(` | (T-OWNER-UNI; the copy is COPY-R400) | {0,1,0} + EQ(domain) ≤ 3 |

**Who runs what.**
- **T-WALK-ROOT** is R:86-120: once per call.
- **T-WALK-CTX** is the context frame's rows: `frame`, `frames.insert`, snapshot_joins, blob_joins (none on the
  context row), nestedRecords (the layout), nestedIdentities (empty), closureJoins and two `closure` calls.
- **T-WALK-UNI** is the universe frame's rows: `frame`, `frames.insert`, nestedRecords (the graph), the empty joins
  and `contextField`.

## 2. T-OWNER-CTX and T-OWNER-UNI (owner bodies, excluding admissions, CLONE, W-REC and refusals)

Refusal construction and insertion (every `refuse`/`fault` call and its `format!`) are **T-REFUSE** (§3). These
rows price only the surrounding operations.

| range | construct | allocation | pass |
| --- | --- | --- | --- |
| C:368-375 | `fn inspect_native_context` | — | (T-FRAME-CTX: funding) |
| C:376-380 | `Checks {` | — | {0,1,0} |
| C:381-386 | `match frame.domain()` | — | EQ(domain) ≤ 3 |
| C:387-392 | `NativeContextChecks {` | owned(\|domain\|) (`to_string`); the result collect is in T-REFUSE-CTX | {0,1,0} |
| C:75-78 | `fn typescript(` | — | 4·field |
| C:79-86 | `typescriptStdlibMerkleRoot` | formatted(73) | field + {0,1,0} |
| C:189-215 | `fn closure(` | (object: T-CLOSURE, funding; error path: T-REFUSE) | {0,1,0} + EQ(error kind) ≤ 3 |
| C:216-221 | `"kind"` | — | field + {0,1,0} + EQ(kind) |
| C:222-223 | `descriptor().clone()` | (CLONE: funding §6) | |
| C:87-89 | `moduleResolutionMode` | — | 2·field + EQ |
| C:90-92 | `let fold` | — | (closure binding, no cost) |
| C:93-96 | `libSelection` | growth(S, 16) | field + {0,1,0} + S·{0,1,0} |
| C:97-100 | `fold(s)` | Σ_k FOLD_A(s_k) + growth(S, 24) | Σ_k FOLD_P(s_k) |
| C:101 | `selected_set` | Σ_k btree_A(k, \|fold s_k\|, 8) | Σ_k btree_P |
| C:102-104 | `selected_set.len()` | — | {0,1,0} |
| C:105-110 | `windows(2)` | — | pass{0, S, 2Σ\|s_k\|} |
| C:111-115 | `options_lib` | Σ_h [FOLD_A(h) + btree_A(h, \|fold h\|, 24)] | 2·field + EQ(null) + {0,1,0} + Σ_h [{0,1,0} + FOLD_P(h) + btree_P] |
| C:116-119 | `selected.into_iter()` | **Σ_k btree_A(k, \|fold s_k\|, 24)** (moved strings) | Σ_k btree_P + pass{0, S+H, 2Σ\|fold\|} (equality) |
| C:120-124 | `standardLibraryComponentDigests` | growth(**K_c**, 16) | field + {0,1,0} + K_c × [field + {0,1,0}] |
| C:125-127 | `names.windows(2)` | — | pass{0, K_c, 2Σ\|κ\|} |
| C:128-134 | `by_component` | — | {0,1,0}; field(tree) + {0,1,0}; **T_s** × [field + {0,1,0} + {0,1,5}] |
| C:135-139 | `rsplit('/')` | **D_s** × btree_A(d, \|δ\|, 32) | D_s × [{0,1,\|path\|} + field + {0,1,0} + btree_P] |
| C:140-144 | `ambiguous-basename` | (T-REFUSE) | |
| C:145 | `declared` | **K_c** × btree_A(k, \|κ\|, 16) | K_c × btree_P |
| C:146-151 | `for component in components` | — | **K_c** × [field + {0,1,0} + search(D_s, \|κ\|) + field + {0,1,0} + EQ(64)] |
| C:152-156 | `by_component.keys()` | — | **D_s** × search(K_c, \|δ\|) |
| C:157-161 | `for lib in selection` | S × [FOLD_A(s_k) + formatted(\|fold s_k\| + 9)] | S × [FOLD_P(s_k) + search(K_c, \|fold s_k\| + 9)] |
| C:162-167 | `"toolClosure.closureId"` | — | field + {0,1,0}; (T-CLOSURE, funding) |
| C:168-171 | `digests` | **T_t** × btree_A(t, 64, 16) | field + {0,1,0} + T_t × [field + {0,1,0} + btree_P] |
| C:172-174 | `semanticVersion` | — | 2·field + EQ |
| C:175-179 | `["compiler", "runtime"]` | — | 2 × [field + {0,1,0} + search(T_t, 64)] |
| C:180-185 | `compilerPackageDigest` | — | field + {0,1,0} + search(T_t, 64) |
| U:145-163 | `fn inspect_typescript_universe` | — | (T-FRAME-UNI: funding); 4·field + 4·{0,1,0} + 4·EQ |
| U:164-169 | `contextField` | — | field + {0,1,0} + field + `sha256_text` |
| U:170-175 | `ContextDomain` | — | (T-FRAME-CTX: funding); field + EQ |
| U:176-177 | `inspect_native_context(` | (its run: T-OWNER-CTX; COPY-U187 below) | |
| U:178-181 | `IdentityDomain::Snapshot` | — | (T-SNAPSHOT: funding) |
| U:182-185 | `sourceInventory` | R × btree_A(i, \|p_i\|, 24) | field + {0,1,0} + R × [field + {0,1,0} + btree_P] |
| U:186-188 | `TsChecks {` | (COPY-U187) | |
| U:189 | `checks.fields(u, c)` | (the `fields` rows) | |
| U:190 | `"configGraph"` | (nested_record wrapper §0.4; RECORD + W-REC: funding) | |
| U:191-196 | `let nodes` | G × btree_A(j, \|g_j\|, 16) | {0,1,0} + field + {0,1,0} + G × [field + {0,1,0} + btree_P] |
| U:197-200 | `context_paths` | **P_c** × btree_A(j, \|π_j\|, 16) | 2·field + {0,1,0} + P_c × [{0,1,0} + btree_P] |
| U:201-203 | `paths != context_paths` | — | pass{0, G + P_c, Σ\|g\| + Σ\|π\|} |
| U:204-214 | `for n in nodes` | — | G × [field + {0,1,0} + search(R, \|g_j\|) + field + EQ(64)] |
| U:215 | `checks.graph(&graph)` | (the `graph` rows) | |
| U:216-234 | `entryConfigPath` | — | field + EQ(null) + G × [field + EQ(entry)] + field + {0,1,0} + EQ + field + {0,1,0} + EQ |
| U:235-237 | `retained-input-missing:configGraph` | (T-REFUSE) | |
| U:238 | `"nodeModulesLayout"` | (nested_record wrapper §0.4; RECORD + W-REC: funding) | |
| U:239-247 | `nodeModulesLayoutDigest` | (the layout faults: T-REFUSE) | field + EQ(null) + {0,1,0} |
| U:248-255 | `["programRootFiles", "jsRootFiles"]` | — | 2·field + 2·{0,1,0} + (P+J) × [{0,1,0} + search(R, \|root\|)] |
| U:256-261 | `NativeUniverseChecks {` | (the result collect: T-REFUSE-UNI) | {0,1,0} |
| U:271-282 | `fn layout_real_path_faults` | Y × btree_A(y, \|ι_y\|, 16) | field + {0,1,0} + {0,1,0} + Y × [field + {0,1,0} + btree_P] |
| U:283-293 | `let mut faults` | (T-REFUSE: the layout path) | Y × [field + {0,1,0} + field + {0,1,0} + EQ(ρ, ι) + search(Y, \|ρ_y\|)] |
| U:297-340 | `fn nested_record` | (§0.4 wrapper; `:320`, `:325-336` and `:337-339` are W-REC/RECORD: funding) | |
| U:341-347 | `struct TsChecks` | (`fault`: §0.4) | |
| U:348-352 | `fn fields(` | owned(4) (`"none".into()`) | 3·field |
| U:353-378 | `let expected` | 6 × CLONE_A(scalar ≤ 32 bytes) | 9·field + 6·CLONE_P + 2·EQ(null) + EQ(bool) + {0,1,0} |
| U:379-383 | `for (k, v) in expected` | (T-REFUSE) | 8 × [field + EQ] |
| U:384-396 | `let synth` | (T-REFUSE) | 5·field + 3·{0,1,0} + 4·EQ |
| U:397-411 | `synthopts` | (T-REFUSE) | EQ(null) + Q × [field + EQ] + {0,1,0} + field + EQ |
| U:412-416 | `jsRootFiles` | (T-REFUSE) | 2·field + EQ + {0,1,0} |
| U:417-423 | `fn graph(` | **PARSE(registry 9,783 B)** | 2·field |
| U:424-428 | `by_path` | G × btree_A(j, \|g_j\|, 24) | field + {0,1,0} + G × [field + {0,1,0} + btree_P] |
| U:429-437 | `basenames.get(basename)` | — | G × [{0,1,\|g_j\|} + search(K_basenames, \|g_j\|) + field(otherwise) + field(kind) + EQ] |
| U:438-444 | `extendsResolved` | — | G × [field + {0,1,0}] + E × [{0,1,0} + search(G, \|e\|)] |
| U:445-456 | `entryConfigPath` | — | field + EQ(null) + {0,1,0} + {0,1,0} + search(G, \|entry\|) |
| U:457-458 | `// Iterative DFS` | (comment) | |
| U:459-481 | `let mut state` | owned(24) (`vec![(entry,false)]`) + growth(2 + 2E, 24) (the stack, over every push) + **2K × btree_A(K, L_key, 24)** (each discovered key inserted at :474, then at :463) | **(2 + 2E) pops** × [{0,1,0} + {0,1,0}]; (1 + E) false pops × search(K, L_key) (:466); 2K × btree_P; K × search(G, L_key) (:476 `by_path.get`); G × [field + {0,1,0}] (node keys only); E × [{0,1,0} + {0,1,0}] (edge pushes, :477-478); with **K = 1 + E** and **L_key = max(\|entry\|, \|e\|max)** |
| U:482-490 | `for path in by_path.keys()` | (T-REFUSE) | G × search(**K**, \|g\|) (the `state` lookup, :483) |

## 3. T-REFUSE-CTX, T-REFUSE-UNI and the copies, by ownership path (RF-5)

Every **attempt** is priced. Sets may deduplicate a result, but its construction and its insertion still run.

**The context owner** (each attempt `refuse(x)`, C:186-188):

| site | attempts | path | per-attempt allocation | per-attempt pass |
| --- | --- | --- | --- | --- |
| C:88, :103, :109, :117, :126, :173, :181 | 1 each | literal `.into()` | owned(\|lit\|) + btree_A(Ref_c, \|lit\|, 24) | btree_P |
| C:212 (or :218), per `closure` call | ≤ 1 per call × 2 | `format!` moved | formatted(\|prefix\| + \|label\|) + btree_A | btree_P |
| C:140-142 | ≤ D_s | `format!` moved | formatted(\|prefix\| + \|δ\|max) + btree_A | btree_P |
| C:149 | ≤ **K_c** | `format!` moved | formatted(\|prefix\| + \|κ\|max) + btree_A | btree_P |
| C:153-155 | ≤ D_s | `format!` moved | formatted(\|prefix\| + \|δ\|max) + btree_A | btree_P |
| C:159 | ≤ S | `format!` moved | formatted(\|prefix\| + \|s\|max) + btree_A | btree_P |
| C:177 | ≤ 2 | `format!` moved | formatted(\|prefix\| + 8) + btree_A | btree_P |
| result C:390 | 1 | `into_iter().collect()` (moved) | growth(Ref_c, 24) | pass{0, Ref_c, 0} |

**Ref_c** ≤ 7 + 2 + D_s + K_c + D_s + S + 2.

**The universe owner** (U:345-347 `fault(&str)` makes a second owned copy):

| site | attempts | path | per-attempt allocation |
| --- | --- | --- | --- |
| U:381 | 8 | `fault(&format!)` | formatted(\|prefix\| + \|k\|max) + owned(same) + btree_A(Ref_u, ·, 24) |
| U:386, :389, :395, :409, :413 | 1 each | `fault(literal)` | owned(\|lit\|) + btree_A |
| U:403-405 | ≤ Q | `fault(&format!)` | formatted + owned + btree_A |
| U:202, :228, :233, :236, :245 | 1 each | `fault(literal)` | owned + btree_A |
| U:212 | ≤ G | `fault(&format!)` | formatted(\|prefix\| + \|g\|max) + owned + btree_A |
| U:252 | ≤ P + J | `fault(&format!)` | formatted(\|prefix\| + \|root\|max) + owned + btree_A |
| U:436 | ≤ G | `fault(&format!)` | formatted(\|prefix\| + \|g\|max) + owned + btree_A |
| U:441 | ≤ E | `fault(&format!)` | formatted(\|prefix\| + \|e\|max) + owned + btree_A |
| U:448, :454 | 1 each | literal / `format!` | ≤ formatted(\|prefix\| + \|entry\|) + owned + btree_A |
| U:469 | ≤ 1 + E | `fault(&format!)` | formatted(\|prefix\| + **L_key**) + owned + btree_A |
| U:485 | ≤ G | `fault(&format!)` | formatted(\|prefix\| + \|g\|max) + owned + btree_A |
| **layout** U:283-292 then U:241-243 | ≤ Y | `format!` → local `faults` set; `into_iter().collect()` into a `Vec`; then `fault(&f)` copies each into the universe set | per attempt: formatted(\|prefix\| + \|ρ\|max) + btree_A(Y, ·, 24) (local) + owned(same) + btree_A(Ref_u, ·, 24); once: growth(Y, 24) (the `Vec`) |
| result U:259 | 1 | `into_iter().collect()` | growth(Ref_u, 24) |

The pass side of each attempt is its btree_P terms, plus pass{0, Y, 0} for the `Vec` collect.

**Ref_u** ≤ |COPY-U187| + 8 + 5 + Q + 5 + G + (P + J) + G + E + 2 + (1 + E) + G + Y.

**The copies:**

| copy | site | allocation | pass |
| --- | --- | --- | --- |
| COPY-R377 / COPY-R400 | `refusals().into()`: `&[String]` → `Vec<String>` | owned(24·Ref) + Σ owned(\|r\|) | pass{0, Ref, Σ\|r\|} |
| COPY-U187 | `iter().cloned().collect()` into `BTreeSet<String>` | Σ [owned(\|r\|) + btree_A(i, \|r\|, 24)] | Σ [{0,1,\|r\|} + btree_P] |

## 4. The occurrence matrix and the two whole calls (RF-6)

Terms are disjoint. The funding column is funding-r3 §6, unchanged.

| term | mint | bind |
| --- | --- | --- |
| T-WALK-ROOT | 1 | 1 |
| T-WALK-CTX | 1 | 1 |
| T-WALK-UNI | 0 | 1 |
| T-OWNER-CTX | 1 | 2 (retention R:374; universe U:176) |
| T-REFUSE-CTX | 1 | 2 |
| T-OWNER-UNI | 0 | 1 |
| T-REFUSE-UNI | 0 | 1 |
| COPY-R377 (Ref_c) | 1 | 1 |
| COPY-U187 (Ref_c) | 0 | 1 |
| COPY-R400 (Ref_u) | 0 | 1 |
| funding §6 column | mint | bind |

Each whole call's price is the sum of its column, split into its allocation side and its pass side by §0.1. Each
`btree` population is taken at its maximum, so the price is monotone (P8).

## 5. Controls

| control | check |
| --- | --- |
| S1 + S6 | `scripts/slot_ledger_check.py`. **S1:** each ledger row's range contains its construct. **S6:** every non-blank, non-comment line in the reachable functions (R:86-120, :131-402; C:44-67, :75-223, :368-392; U:43-81, :145-261, :271-293, :297-490) is in exactly one row. |
| S2 | The refusal-site census: the `refuse(` / `fault(` / `faults.insert(` sites in the TypeScript branches equal §3's tables, attempt multiplicities included. |
| S3 | FOLD's use count: C:99, :114 and :158. |
| S4 | The model mirror includes these terms and equals the Rust on the vectors, malformed shapes included. |
| S5 | F8 measures each term's allocation side on the fixtures. |
| S7 | (RF-2) Unequal populations: a 1-row `.d.ts` stdlib tree against 100 distinct context components; P_c ≠ G; a lockfile path absent from the inventory and longer than every member. The price ≥ the measured allocation on each. |
| S8 | (RF-3) Large actual / small declared: a retained member of 1 MiB whose descriptor declares 1 byte. Its price includes digest_cost(1 MiB), and the run refuses `BlobLength` after hashing. |
| S9 | (RF-5) A layout real-path fault vector (Y faults), and a dynamic universe diagnostic (G `source-mismatch` faults), each allocation-measured. |
| S10 | (r4, REVIEW-r3 RF-2) **Missing-target fan-out.** A graph with one valid entry node and 64 distinct missing `extendsResolved` targets, some longer than every node path, measured by the model mirror's transcription of U:459-481 and by the allocation binary. It checks: state members ≤ K, state insert attempts ≤ 2K, pops ≤ 2 + 2E, edge pushes = E, and allocation ≤ the row's allocation side. Expected values for this graph: K = 65, inserts = 130, pops = 130. |
