# DISCOVERY-FLAGS-E1a r4: effective `allowJs` at discovery, non-pruned graphs (erratum to M3-B r10 and MC8 C-N1)

**Status: PROPOSED (r4).** Not law until both reviewers (Codex, Claude) accept it. Author: Claude claude-opus-5-5/medium
for the lead, R2-DEEP (preflight re-run for r4: `ROUTE-OK R2-DEEP claude claude-opus-5-5/medium`).

**What r4 is.** A full replacement of E1a r3 (`ERRATUM-E1a-r3.md`, sha256
`781a17941653bbaabe57c34e71207e18ce4c62a26095216ffca9466bdd9cfb59`, 61,461 bytes, left untouched) that changes ONLY
what the two r3 verdicts require and the lead listed: Codex `review-codex/VERDICT-r3.md` (= **C3**) E1a-r3-RF-1 and its
note on choice (1); Claude `review-opus/VERDICT-r3.md` (= **O3**) R3-1, its advisory on 2.1.2, and its note of one
sentence missing from r3's table. The table "Changes from r3" lists every change; everything else is r3's text. Both r3
verdicts close every r2 finding and accept the author's choices (1), (3) and (4); both reject (2), the omission of
`target` (C3; O3 R3-1).

**What r3 was.** A full replacement of E1a r2 (`ERRATUM-E1a-r2.md`, sha256
`5157d43863e92e035c8c362ceb1c47b7dd74ff8013b005e064211c9e47e33724`, 50,318 bytes, left untouched) that changes ONLY
what the two r2 verdicts require and the lead listed: Codex `review-codex/VERDICT-r2.md` (= **C2**) E1a-RF-1, E1a-RF-2
and points 4, 5, 7; Claude `review-opus/VERDICT-r2.md` (= **O2**) R2-1 to R2-4 and its advisories. The table "Changes
from r2" lists every change; everything else is r2's text. Both r2 verdicts accept the scope gate, the Cargo cut, the
ordering, the binding's coverage, the source outcomes and the funding (C2 points 1, 4-6, 8; O2 sections 1-6, 8).

**What r2 was.** A full replacement of DISCOVERY-FLAGS-E1 r1 (`ERRATUM-r1.md`, sha256
`89dc57b7765b4ae8c62a0dff2e4c474671d7bbdb1360ecc51b96c1566ced779e`, 45,539 bytes, left untouched), cut to a smaller first
slice, E1a, as both r1 verdicts propose: Codex `review-codex/VERDICT-r1.md` (= **C1**) paragraph 7, and Claude
`review-opus/VERDICT-r1.md` (= **O1**) Q7. Every C1 and O1 finding is applied; the table "Changes from r1" says where.
Cargo policy and pruned (`node_modules`) bases are cut out behind one scope gate (item 7) and recorded as owed to
later errata E1b and E1c (section "Owed to E1b / E1c"). E1a binds no Cargo rule.

**The scope cut is the lead's choice; both reviewers are asked to confirm it.** C1 ¶7 proposes one host-invariant key,
`j3d-ts.discovery-flags-unimplemented`, with reason `cargo` or `pruned-base`, and cuts Cargo. O1 Q7 proposes two
differently named arms and would keep Cargo in ("I would keep it in E1-A unless 4.4 proves slow"), but allows the
Cargo cut ("(ii) Cargo, optionally"). The lead takes C1's single key and the Cargo cut because it is the smaller unit
and O1's verdict allows it.

**What it amends (neither file is edited):**
- M3-B r10, `ARCH/docs/implementation/m3/config-discovery-b/PROPOSAL.md` (= **M3B**), sha256
  `c1d7be049637bd481976153e5624c7344c228ab69516d3f3a536aff1a2a27d15` (144,164 bytes). Items 12, 14 (U-1) and 14a.
- MC8, `ARCH/docs/implementation/m3/snapshot-plan-c/PROPOSAL.md` (= **MC8**), sha256
  `910cf4d5ff6702aa8a6db1f9a8075b715b1bd44e17fac387c3e05ca61dc99a6e` (184,876 bytes). Item 1, C-N1's list of session
  reads, one bullet.
- Design repository head read: `cc25748a2`. Line numbers are from the live files above.

**Code it describes:** `opensip-sec-discover-1b` at `e56a4f6d9807344b2cf53bb020e88c4271142970`, read only, no build.
`h/` = `crates/host/src/`, `sec/` = `crates/security/src/`.

**Other short names.** MJ = `m3/host-pipeline-j/PROPOSAL.md` (r7, accepted). NE =
`ARCH/docs/v2/contracts/product-v1/native-evidence.md`. Q100, Q52 = lead rulings in `LC/j3d-ts/QUESTIONS.md`
(:1645-1662, :959-963; lead-adopted under OD-DECIDE-1, not design-repository law). LD-DEC-5 =
`LC/decisions/LD-DEC-5-user-caused-host-fault/DECISION.md`. CV / OV = the SEC-DISCOVER-1b verdicts
(`LC/j3d-ts/sec-discover-1b/review-codex/VERDICT.md`, `.../review-opus/VERDICT.md`). HO = `LC/j3d-ts/sec-discover-1b/HANDOFF.md`.

**Rule of this text.** Each item gives Old (quoted, file:line), New (the sentence that becomes law) and Rests on
(quoted adopted text, or **"proposed"**, with the alternatives rejected). Where C1 called a clause a mechanism rather
than an adopted obligation, it is marked proposed. E1a sets no price number, adds no D9 row and no public detail, and
does not weaken mode selection: every path either derives the flag from captured bytes, refuses on an adopted
refusal, or ends on a host invariant before any mode is chosen.

## The gap (unchanged from r1, in brief)

At the head, `h/analysis/discovery_source.rs`:149 captures each lent marker on the discovery ledger and `:181-182` set
`is_cargo_workspace: None`, `allow_js: None`. `h/discovery.rs`:626-628 read `None` as `allowJs` false for a
`tsconfig.json` and true for a `jsconfig.json`. The Plan's `effective_allow_js` call (`h/plan.rs`:2281) never compares
the mode (HO session 2, item 1). M3B:607 requires "the host computes the marker's effective `allowJs` before U-1
chooses the mode"; M3B:664 "The value is the marker observation's `allowJs` that U-1 reads"; CV ¶4 and OV Q4: a
refusal is not an adopted substitute.

## Map: the reviewers' demands to the items

| Demand | Source | Item |
|---|---|---|
| discovery-time byte access | CV ¶4 | 1, 3.2 |
| graph/extends capture; inventory inclusion | CV ¶4; OV Q4 (2) | 2 |
| the ONE `effective_allow_js` at discovery; relation to `plan.rs`:2281 | OV Q4 (3) | 1, 2.4 |
| ledger and precharged derivation costs | CV ¶4; OV Q4 (1) | 3 |
| unavailable/invalid-flag handling | CV ¶4; OV Q4 (4) | 5, 6, 7 |
| whether flags may be `None` in production | OV Q4 (5) | 6 |
| no placeholder modes (C1 RF-1, O1 F-1) | C1 ¶2; O1 F-1 | 1.3, 6.3 |
| bind every derived graph, selected or not (C1 RF-2, O1 F-3) | C1 ¶2; O1 F-3 | 2.4 |
| a validation window that exists in the composition (C2 E1a-RF-1, O2 R2-1) | C2 ¶2; O2 R2-1 | 2.4.2, O-10 |
| a pruned gate closed against aliases and member-root `.opensip` (C2 E1a-RF-2, O2 R2-2) | C2 ¶3; O2 R2-2 | 7.2, 2.1.2 |
| fund all work, error paths included (C1 RF-3, O1 F-6) | C1 ¶3; O1 F-6 | 3 |
| one closed scope gate for Cargo and pruned bases | C1 ¶7-8; O1 Q7 | 7 |
| must not silently weaken mode selection | CV ¶4 | every item; table at the end |

## Changes from r3

| Item | Change in r4 | Finding; wording taken |
|---|---|---|
| 7.2 | `target` joins the lexical list, anywhere in the path, under the same NFKC_Casefold comparison; the passage saying `target` is unreachable is replaced by the reviewers' reason (explicit roots: an unlent sibling `Cargo.toml`, pruned by the snapshot walk) and their counterexample | C3 E1a-r3-RF-1 = O3 R3-1; C3's counterexample and code lines taken, O3's `snapshot_read_set.rs` lines added |
| 7.2 over-refusal; 2.1.2 | A lawful base under any directory named `target` now ends on the gate; E1c restores precision. 2.1.2's "every spelling" claim is limited to the platforms the unit supports and tests; NTFS trailing-dot/space equivalence is not claimed | C3 E1a-r3-RF-1; O3 R3-1; O3 advisory on choice (1) |
| 3.5, 8.6 | The NFKC_Casefold normalization and comparison of 7.2 is funded work and has its exact/one-short control | C3 on choice (1): "its normalization/comparison work must be prepaid" |
| 8.12 | The explicit-root / sibling-Cargo `target` case, refused before any candidate open | C3 E1a-r3-RF-1; O3 R3-1 |
| Changes from r2 | Adds the row for the E1c sentence "The same holds for 7.2's over-refusals", new in r3 and unlisted there | O3 (diff r2 to r3) |
| 7, table | 7's Rests on and the table row for 7 cite the `target` reason | follows the above |

## Changes from r2

| Item | Change in r3 | Finding; wording taken |
|---|---|---|
| 2.4.2 | The window is moved: selection needed to seal is provisional; validation after sealing and before program-specific planning or committing the selection, no later than the Plan's first step; a difference ends the invocation without reselection, resealing or retry; one sentence says why that binds the pre-seal consumers | C2 E1a-RF-1 = O2 R2-1; C2's three sentences verbatim, O2's "planned, recorded or projected" sentence and its "Plan's first step" as the latest point |
| O-10 | Only the exact step and ledger remain, "with all graphs funded and no budget reset" | C2 E1a-RF-1 |
| 7.2 | The path-specifier test is lexical and conservative under NFKC_Casefold: any segment equal to `node_modules`, a shared-rule VCS name or `.opensip`, anywhere; `target` stated as not reachable; over-refusal stated; no file-system probe | C2 E1a-RF-2 = O2 R2-2; O2's "more simply" alternative taken (no member-root input needed); normalization per O2's advisory |
| 2.1.2 | The restriction now rests on 7.2's lexical test, under every spelling the file system treats as the same name | C2 E1a-RF-2 ("its dependent 2.1.2 restriction") |
| 2.1.4 | "observed size permits early refusal" replaced: the observed size lets the source return the over-bound arm without reading; the refusal is judged in `visit`; C2 point 5 kept | O2 R2-3; C2 point 5 |
| 2.1.5 | Every other caller of `SnapshotRoot::open` keeps its present outcome for a link; the change goes through security-change review | O2 section 5 advisories |
| 3.1, 3.5 | "items 1-2, 6 and 7"; 3.5 adds 6.3's checks and 6.4's retained candidates and comparison | O2 R2-4 |
| 6.4 | Compares candidate identity, roots, winning markers and order, not counts; allowing mode/kind to differ admits no value other than the derivation's | C2 point 4 |
| 7 | The reason is part of the operational record; the Q52 handoff list names both key-and-reason pairs | O2 section 2 |
| 8.6, 8.8, 8.9, 8.10, 8.12 | 8.6 and 8.10: item 6's charges; 8.8: the real selection/sealing/validation sequence; 8.9: an NFC/NFD variant; 8.12: the case-alias, normalization-alias and member-root `.opensip` gates | O2 R2-4, section 7; C2 point 7, E1a-RF-2 |
| Owed to E1c | O2's advisory: a missing package ends at exit 4 in the interim where adopted law gives exit 2; and the sentence "The same holds for 7.2's over-refusals" (added in r3, listed here at r4) | O2 section 2 (advisory); O3 |
| Map, table | Rows for the window and the gate's aliases; table rows 2.1.2, 2.1.4, 2.4.2, 6.4, 7 updated | follows the above |

## Changes from r1

| r1 item | Change in E1a r2 | Finding; wording taken |
|---|---|---|
| 1.3 order | No bootstrap discovery. Candidate identification by mode-independent rules, then derivation, then ONE final U-1..U-9 construction | C1 RF-1 = O1 F-1; C1's sentence taken verbatim (O1's fix "leaves each mode undecided" is the same rule; C1's forbids the bootstrap outright, which is simpler to test) |
| 1.3 (a), 4 (Cargo) | Cut; the `cargo` gate (7.1); owed to E1b | Lead scope choice; C1 ¶7; O1 Q7 (ii) |
| 2.1.1 | Candidate metadata probes distinguished from successful captures | C1 disposition 2.1.1 |
| 2.1.2 | `capture` half kept; `capture_pruned` half cut; the `pruned-base` gate (7.2); owed to E1c | C1 disposition 2.1.2; O1 disposition 2.1.2 |
| 2.1.3 | Typed latch for the first fatal cause; no native work after it; the opener reports a link distinctly (a security-crate requirement) | O1 F-5; C1 "accept as new law" |
| 2.1.4 | M3B:611's order kept; a new `ConfigEntry` arm "regular file over the bound, not read"; the "function unchanged" claim dropped; C1's sentence on uncaptured candidates and kept captures | O1 F-4 + C1 disposition 2.1.4 (both sentences taken; they do not conflict) |
| 2.2.1 | Pruned-row clause removed (gate); walk rows and leftovers kept | C1 disposition 2.2.1; O1 Q7 |
| 2.3 | Basis now C-N1's closed list (MC8:207) and M3B:650/:653, not MC8:205 | O1 F-7; C1 ¶1 |
| 2.4.2 | Validate EVERY derived graph against the sealed inventory before program-specific planning, regardless of selection; graph and mode compared | C1 RF-2 = O1 F-3; C1's sentence taken verbatim (O1's "before the Plan's first step that consumes the discovery" is kept as the placement constraint) |
| 3.2 blob loading | Marked a proposed mechanism (MC8:218 binds retained bytes, not an API) | C1 ¶1 |
| 3.5-3.6 | Added: candidate identification and final discovery, the marker-map clone, loaded-byte copies, parsed-path memo, graph construction, retention, validation, error paths; per-actual-parse funding; "being inside a scope is not charging work"; C1's unmetered-precharge sentence as the general rule | C1 RF-3; O1 F-6; O1 4.4 disposition (probe is the control, not the proof) agrees |
| 4, 5.2, O-5, O-7 | Moved to "Owed to E1b" with both readings | Lead scope choice |
| 6 | tsconfig/jsconfig only; the invariant applies to the one final construction; shadowed markers read as another unit's base stay `None` | C1 ¶5; O1 F-1 |
| 7 controls | Revised for the slice; C1 ¶8 and O1 Q8 additions | C1 ¶8; O1 Q8 |
| O-1 | Closed by the lead's ordering, retargeted to E1a | C1 ¶6-7; O1 Q6 |
| O-2, O-3 | Moved to E1c | C1 ¶6; O1 Q6 |
| O-8 | Policy closed: under M3B:499 the discovery runs are charged; prices to implementation | C1 ¶3, ¶6; O1 F-6 |
| O-9 | Closed: marker leaves config-file custody; non-marker bases ordinary C1 source custody | C1 ¶6; O1 Q6 |
| new | Item 7, the scope gate | C1 ¶7 (sentence verbatim); O1 Q7 (closed condition) |

---

## 1. Who derives `allow_js`, from which bytes, and when

**Old.** M3B:607: "For each `tsjs` marker directory whose first present marker is `tsconfig.json` or `jsconfig.json`
(U-1), the host computes the marker's effective `allowJs` before U-1 chooses the mode. A `package.json`-only directory
needs none. One first-party function reads the graph." No adopted sentence names the bytes, the call or the order at
discovery.

**New.**
- 1.1 `MarkerFact.allow_js` is the `allow_js` of `EffectiveOptions` returned by item 14a's one function,
  `effective_allow_js` (`h/typescript_config.rs`:544), run at discovery over a `ConfigSource` whose bytes are the
  capture session's captures (item 2). Each capture is the one the host makes through `CaptureSession::capture` on
  the discovery ledger; the derivation reads no project file a second time.
- 1.2 The bytes the derivation reads are the capture's retained bytes in custody, never the project file.
- 1.3 Order, all on the discovery ledger: "Identify candidate directories and winning markers by the mode-independent
  shared rules; derive the flags needed for folding and mode selection; only then construct final U-1..U-9 output."
  In E1a the flags needed are `allow_js` of each candidate `tsjs` directory whose winning marker is `tsconfig.json` or
  `jsconfig.json`. Candidate identification chooses, carries and projects no mode. A refusal of candidate
  identification is discovery's refusal and reads no graph. The final construction is the only U-1..U-9 output the
  Run carries; its units are the candidates identification implied, with their modes decided (else 6.4).
- 1.4 The Plan keeps calling the same function at `plan.rs`:2281, bound to discovery's result by item 2.4.

**Rests on.**
- 1.1: Q100 item 3: "`allow_js` from item 14a's TypeScript-config reader over the captured bytes ... No second
  reader." Q100 item 1: "captures each lent marker path through `CaptureSession::capture` with the session's own
  custody, charged to the discovery ledger, and derives each `MarkerFact` from that capture." MC8:208 ("B2's marker and
  manifest content reads (discovery, on the discovery ledger; M3-B item 12)"); MC8:216 ("**No second read.**");
  M3B:581 ("C2's `TypeScriptConfigProjectionV2` must call the same function: one implementation"); OV Q4 (3).
- 1.2: MC8:215 ("**A capture is kept.** Each one keeps the bytes in custody, their digest, and the descriptor
  observation"); MC8:218 ("**One set of bytes.** So discovery and layout are always derived from the bytes the
  inventory holds"). The load mechanism is **proposed** (3.2).
- 1.3: M3B:607 ("before U-1 chooses the mode"). The sentence is C1 RF-1's; O1 F-1 states the same rule ("a state
  never carried or projected"). Which rules are mode-independent is a code fact: `allowJs` changes only the mode
  label (`h/discovery.rs`:624-641; O1 Q2: "`discover` uses the mode only to label the unit"), so with no `Cargo.toml`
  in the lend (item 7.1) survival does not depend on any flag. The construction as a whole is **proposed**. Rejected:
  (i) r1's bootstrap pass, which "calls U-1 with underived flags" (C1 RF-1) and which the old helper's doc
  (`typescript_config.rs`:605-611) does not license ("implementation precedent, not an exception to that law", C1
  ¶2); (ii) deriving for every configuration marker the lend names, shadowed or not (reads and may refuse on graphs
  of non-units; r1 1.3 rejection (i), not disputed).
- 1.4: M3B:607: "C2's `TypeScriptConfigProjectionV2` and its `TypeScriptConfigGraphV1` use the same function and the
  same resolution, so the two cannot describe different graphs."

## 2. The `extends` graph at discovery (non-pruned)

**Old.** M3B:611: "At most **64 KiB** per file and at most **32 nodes** in the graph. **(r10)** At most **64 entries**
in one file's `extends` array, repetitions included, and at most **4,096 characters** in a node's canonical path ...
The `extends` count is checked when the file's fields are read, after its JSONC and types and before any entry is
classified or resolved; the path length with the other new-node checks, before the node's bytes are judged."
M3B:612: "The fields read are `compilerOptions.allowJs`, `compilerOptions.checkJs` and `extends`." M3B:653: "A
configuration file, and each directory on its path, is read under C1's snapshot custody."

### 2.1 Which files are opened and captured, in what order

**New.**
- 2.1.1 The files captured are exactly the files `effective_allow_js` reads: the entry marker, then, depth first in
  `extends` entry order, each specifier's candidates in item 14a's order (M3B:636-643), the first regular file
  winning, and that file's own bases before the next specifier (`Walk::resolve`/`Walk::visit`,
  `h/typescript_config.rs`:454-532). A candidate probe that finds no regular file is a metadata observation and makes
  no capture; only a returned regular file is a capture. A node already captured (the entry, another unit's marker, a
  base shared by two graphs or two edges) is the kept capture and is not read again.
- 2.1.2 Every candidate E1a opens passes 7.2's lexical test, so it lies outside every shared-rule pruned tree under
  every spelling the file system treats as the same name, on the platforms the implementing unit supports and tests
  (the macOS lane named in 8.9 and 8.12, and any other lane that unit names; NTFS's trailing-dot and trailing-space
  equivalence, for example, is not claimed), and is opened through `CaptureSession::capture`
  (`h/snapshot.rs`:540). A candidate that 7.2's test catches is never opened, observed or captured under E1a.
- 2.1.3 The source's outcomes:
  - a regular file within the bound: captured and returned (`File`);
  - an absent path, or a path that is not a regular file and not a link: `NotAFile`, no capture, resolution goes on
    to the next candidate;
  - a symbolic link as any directory component of the candidate's path or as its leaf: `Link`, which item 14a refuses
    as `native.typescript-config-extends-unresolved`;
  - a regular file over the per-file bound: the new arm of 2.1.4;
  - any other open, read or charge failure (custody, a changed object, host I/O, the ledger), and the gate of item 7.2:
    fatal. A fatal outcome latches the source: the first fatal cause is kept in a typed latch, every later read
    answers `NotAFile` with no native work, so the next candidate cannot win, the function's result is discarded,
    and discovery ends on the latched cause.
- 2.1.4 The bound. `ConfigEntry` gains one arm, "regular file over the bound, not read", which `Walk::visit` judges
  where it judges bytes today (`h/typescript_config.rs`:477), after the cycle, 32-node and path-length checks, so
  M3B:611's order and M3B:680's subject are unchanged; `FundedSource` returns the same arm for a map entry over the
  bound. For an uncaptured candidate, the observed size lets the source return the over-bound arm without reading the
  bytes; the refusal is judged in `visit`. The observed size does not replace actual-byte enforcement: every returned
  node also satisfies the actual-byte limit. A kept capture, including another unit's already-captured marker, is
  checked without another project read.
- 2.1.5 Requirement on the implementing unit (security crate): `SnapshotRoot::open` reports a symbolic link at a
  directory component or at the leaf distinctly from absence and from a non-regular file. Every other caller of
  `SnapshotRoot::open` (O2 section 5 lists the marker capture, the walk and C2) keeps its present outcome for a link, so the change
  alters no behaviour outside 14a's source, and it goes through the project's security-change review by both
  reviewers. Today both sites return
  `SnapshotRefusal::NotARegularFile` (`sec/snapshot_source.rs`:930-938 for a component, :959-965 for the leaf).

**Rests on.**
- 2.1.1: M3B:607, :636-648 ("The cycle and 32-node checks run over these node identities, as the graph is built");
  MC8:216. The capture order equalling the reader's order is **proposed**; C1 "Accept"; O1 "Accept". Rejected:
  pre-capturing a guessed candidate list (contrary to M3B:650's "actually reads").
- 2.1.2: `capture`'s doc (`h/snapshot.rs`:537-539): "A pre-walk capture of `path` (B2's and C2's reads)". M3B:650:
  "Reading inside `node_modules` is a read-set access, not discovery descent." The non-pruned restriction is the scope
  of E1a (item 7); resting it on 7.2's lexical test, not on the exact-segment rule, is C2 E1a-RF-2's change ("change 7
  and its dependent 2.1.2 restriction"). C1 disposition 2.1.2: "Pruned graph reads are enabled only after their custody and read-set
  authorization law is accepted; otherwise the explicit scope gate in paragraph 7 applies."
- 2.1.3: the link arm: M3B:670 (`extends-unresolved` when a specifier "names no candidate regular file ... or meets a
  symbolic link before C1. **This refuses whatever inheritance would otherwise settle.**"); M3B:654-655 ("A symbolic
  link on the path is followed only as that custody allows. Until C1's composition exists, the resolver reads no
  symbolic link: a link is unresolved."); M3B:702 forbids "Treating an unresolved base as absent." The latch is
  **proposed** (C1: "Accept as new law: distinguish absent/non-file, link and fatal capture failures; preserve the
  first fatal cause in a typed latch and perform no further native work after it"; O1 F-5). Code reason:
  `ConfigSource::read` cannot return a refusal (`h/typescript_config.rs`:49-51), and an unlatched `NotAFile` would let
  the next candidate win (`:463-465`). Precedent: B-20's latch (`h/mb14a_funded.rs`:37-38, "A refusal at any charge
  latches, and the source returns `NotAFile` from then on"). Rejected: mapping a custody refusal to
  `extends-unresolved` (not one of M3B:670's conditions; M3B:678's remedy would be false).
- 2.1.4: M3B:611 (quoted); M3B:680 ("The subject. It names the internal class and the project-relative path of the
  configuration file that refused"). O1 F-4: "`Walk::visit` checks the cycle and the 32-node bound before
  `visit(target)` judges the size". The new arm, its placement, and the observed-size sentence are **proposed**; the
  sentence is O2 R2-3's replacement of C1's "permits early refusal", which read as a refusal at open, and keeps C2
  point 5 ("Observed-size refusal does not replace actual-byte enforcement. Kept marker captures are checked without
  rereading the project"). Rejected: r1's open-time refusal, which moved a 33rd oversize node's subject from the parent to the
  base (O1 F-4), and capturing every base whole before judging it, which makes the outcome depend on ledger headroom
  (row 21, exit 4, instead of row 59, exit 2; r1 2.1.4).
- 2.1.5: **proposed**; O1 F-5 ("a security change the unit owns"). Without it 2.1.3's link arm cannot be told from
  absence, and M3B:670 would be unenforceable. C2 point 5: "The security-opener change is an explicit implementation
  obligation, not something current source already supplies." O2 section 5 (advisories): every other caller keeps its
  present outcome, and the change goes through the security-change review.

### 2.2 Inventory rows and change detection

**New.**
- 2.2.1 Every captured graph node is a resolved input of its unit's mode. A node the walk reaches is the walk's
  inventory row, with the kept capture's bytes. A captured node the walk does not reach is a leftover, and sealing
  refuses (MC8:219).
- 2.2.2 A captured graph node rewritten before the walk reaches it refuses the snapshot, as a marker does (C1-T24).
- 2.2.3 Custody of a graph node: a marker leaf takes config-file custody, as the opener applies it; a non-marker base
  takes ordinary C1 source custody (the opener's S3 directory custody and descriptor discipline), and no stronger
  rule.

**Rests on.**
- 2.2.1: MC8:219: "**Leftover captures refuse.** ... If any resolved input depends on such a capture, sealing refuses
  rather than binding an uninventoried byte". "Resolved input" for a graph node is **proposed**; C1 and O1 accept it.
- 2.2.2: MC8:217 ("**A change refuses.** ... It does not retry (SL:315), and it never re-reads"); MC8:230 (C1-T24).
  Extension to graph nodes **proposed**; C1: "Accept change detection for every captured graph node reached by walk".
- 2.2.3: M3B:653 ("read under C1's snapshot custody"). Code: the leaf is judged under config-file custody only
  `if marker` (`sec/snapshot_source.rs`:968-981). C1 ¶6: "marker leaves get config-file custody; non-marker bases get
  ordinary C1 source/read-set custody. A stronger semantic 'all configuration bytes are config-file custody' rule would
  be new policy"; O1 Q6 (O-9): "Adding config-file custody would be a stricter rule the adopted text does not state."
  Read-set custody belongs to E1c.

### 2.3 MC8 C-N1's list (the MC8 sentence)

**Old.** MC8:207: "Every source read before sealing goes through it, keyed by logical path. Those reads are:" B2's
marker and manifest content reads (:208); C2's installed-package manifests (:209); the walk itself (:210).

**New.** A bullet after MC8:208: "B2's TypeScript configuration graph reads: the `extends` bases item 14a's resolution
actually reads outside every pruned tree (discovery, on the discovery ledger; M3-B item 14a as DISCOVERY-FLAGS-E1a
amends it)."

**Rests on.** MC8:207's closed list ("Those reads are"), amended by this bullet, and M3B:650/:653 (bases are read
"under C1's snapshot custody"). **Proposed** as an extension of that list (C1: "Accept the additional C-N1 bullet as an
explicit extension, with the corrected basis"; O1 F-7: "rest the sentence on C-N1's closed list (MC8:207 'Those reads
are') and M3B:650/:653").

### 2.4 Binding every derived graph to the sealed inventory

**New.**
- 2.4.1 Discovery keeps, per derived marker, beside its `MarkerFact`, the `ConfigGraph` that `effective_allow_js`
  returned (entry; per node its path, sha256, kind and ordered edges). The record is operational: not a field of
  `UnitDiscoveryV3`, not in identity.
- 2.4.2 "Before program-specific planning, rederive and compare every graph used to choose discovery modes against the
  sealed inventory, regardless of selection; selected Plan projections must agree with that validation." The
  comparison is of the whole graph and of the mode: the rederived `allow_js` is true exactly when the unit's mode is
  `js-allowjs`. "Selection needed to construct the snapshot is provisional. After sealing, and before program-specific
  planning or committing the selection, rederive and compare every discovery graph and mode, regardless of
  selection. A difference ends the invocation without reselection, resealing or retry." The latest point is the Plan's
  first step. The pre-seal steps that use the modes (membership, capability and program selection, the layout units)
  are bound by the validation because its refusal ends the invocation before any of their outputs is planned,
  recorded or projected.
- 2.4.3 Until a D9 row is adopted for that refusal (O-4), it ends on a named host-invariant arm under Q52.

**Rests on.**
- 2.4.1: **proposed**; C1 "Accept per-marker graph retention, operational and priced"; O1 "Accept".
- 2.4.2: **proposed**; the sentence is C1 RF-2's. Captures bind what discovery read (2.2), but not a candidate it found
  absent: a file created at an earlier candidate after discovery and before the walk is inventoried and chosen by the
  sealed-tree resolution (`FundedSource` answers `NotAFile` only for a path absent from the map,
  `h/mb14a_funded.rs`:192-193). r1 bound only selected programs; `plan.rs`:2281 runs per program, and programs are only
  units "that a requested tuple names" (`h/analysis/programs.rs`:6-7, :97-103); C1 RF-2 and O1 F-3 give the
  unselected-unit counterexample. M3B:607 ("cannot describe different graphs") requires the graph, not only the
  boolean (C1: "Comparing the boolean alone is insufficient"). No retry: MC8:217, SL:315. The window: r2's "before the first
  step that consumes the discovery's modes (selection included)" was empty at `e56a4f6d`, because the modes are
  consumed before sealing: `configured_capability_selection` reads them (`analysis/captured.rs`:304), programs and
  layout units are selected before `seal_snapshot` (`:338-372`; `:207-238` resolve the layouts and read set before
  sealing; the Q11 contract `:315-321`; `seal_snapshot`'s doc `:157-160`: "the walk, each named unit's layout, the read
  set over those layouts and the seal"), and membership runs right after discovery (`analysis.rs`:380) (C2 E1a-RF-1;
  O2 R2-1). The three quoted sentences are C2 E1a-RF-1's; "planned, recorded or projected" and "the Plan's first
  step" are O2 R2-1's, restoring O1 F-3's "the Plan's first step". Rejected: C2's alternative, a new preselection
  inventory/ordering contract (larger, and not needed once selection before sealing is provisional). Rejected: reuse of discovery's
  result in the Plan (misses the race); O1 F-3's alternative, the walk refusing when it inventories a probed-absent
  candidate (it needs the probe list retained and checked per walked path; the validation reuses the one function and
  B-20's funded source).
- 2.4.3: Q52: "A variant whose owner has no projection is a NAMED arm ending on the host-invariant row with the key in
  the operational record". C1 ¶6 and O1 Q6 accept the interim. The key's spelling is the implementing unit's, listed
  in its handoff (Q52).

## 3. The ledger and the price

**Old.** M3B:498-499: "**Downward unit discovery and the D15 member observation** run **after** the installation fence
is released ... They are charged to one **discovery ledger** per invocation." M3B:500: its caps "2^22 objects, 2^21
edges and 2^30 bytes".

**New.**
- 3.1 All work of items 1-2, 6 and 7, on the discovery ledger, and the validation of 2.4.2 on the ledger of the step it
  runs in, is charged before it is done, error paths included. Being inside a ledger's scope is not charging work. A
  refused charge on the discovery ledger ends as MJ row 21 (`WORK.BUDGET_EXHAUSTED`), never as an item 14a key.
- 3.2 Loading a capture's retained bytes uses the charges of the load half of `CaptureSession::parse_captured`
  (`h/snapshot.rs`:624-683), reused unchanged, loading at most `limit + 1` bytes for a configuration node.
- 3.3 Capturing a graph node is charged by the opener and `read_once` as the marker capture is; a candidate probe
  that finds no regular file pays the opener's own charges and inserts nothing.
- 3.4 The JSONC read and the walk are charged per actual parse by B-20's charges (`h/mb14a_funded.rs`:27-39 steps
  (1)-(3), `shadow_and_delta` :144-171, the walk precharge and refusal allowances in `funded_read` :173-), with
  `prepay_diagnostic` (:129) and `entry_in_bound` (:118) before each walk, reused unchanged on the discovery ledger,
  except that B-20's map lookup is replaced by 3.2-3.3's charges. A node repeated within one graph is parsed once and
  funded once (B-20's memo); a base shared by separate graphs is parsed once per graph and funded per graph.
- 3.5 Prices owed by the implementing unit, derived and reviewed there: candidate identification and the final
  U-1..U-9 construction (`discover_units`); `observe_effective_allow_js`'s marker-map clone, or whatever replaces it;
  each loaded-byte copy; the parsed-path memo's searches and inserts; graph construction (`ConfigNode`, `ConfigGraph`,
  `node_bytes`); the retention of 2.4.1; the validation and comparison of 2.4.2; the checks of 6.3; the retained
  candidates and the comparison of 6.4; the NFKC_Casefold normalization and comparison of 7.2, per candidate segment;
  the typed latch; each refusal record.
- 3.6 Constraints on every owed price: a closed function of quantities known before the work (a capture's recorded
  length, path lengths, `extends` counts and specifier lengths, node, edge, marker and unit counts within M3B:611's and
  M3B:500's bounds); charged by the host on the ledger of 3.1; each charge shown by a control that makes it one short
  and observes the refusal with no native work after it, and passes at the exact budget. "An unmetered precharge has a
  source-derived bound over all admissible inputs of the pinned implementation; adversarial allocation probes validate
  it, including failures and destruction." A census shows the discovery ledger's caps (M3B:500) still hold.

**Rests on.**
- 3.1: M3B:499 (quoted). "Being inside a scope is not charging work" is C1 RF-3's sentence; O1 F-6: "M3B:499 already says
  'Downward unit discovery ... charged to one discovery ledger', so O-8 cannot be closed by a ruling that puts U-1..U-9
  outside the ledger". Code fact: `discover_units` takes no `WorkScope` and runs after the ledger scope closes
  (`h/analysis.rs`:362-376, `h/discovery.rs`:996-1001), so the implementing unit moves it onto the ledger. MJ:793 (row
  21): "Discovery or snapshot ledger exhausted | operational-failed / 4 | ... | `WORK.BUDGET_EXHAUSTED`". The latch's
  end on row 21 at discovery (where the Plan maps it to `PlanError::Exhausted`, `plan.rs`:2282-2284) is **proposed**;
  O1 "Accept".
- 3.2: **proposed** mechanism (C1 ¶1: MC8:218 binds retained bytes, not a blob-loading API). HO LTC-1b-1: "The session
  has no priced raw-bytes read of a capture outside `plan.rs`'s private B-1 map". `parse_captured`'s load half already
  runs on the discovery ledger for C2's manifests (`h/node_modules_layout.rs`:1260). Sound when its charges depend
  only on path length, capture and blob counts and loaded length. O1: "The length check and attempt envelope adapted
  to the truncated load are an implementation note."
- 3.3: CV ¶3: "The step, marker capture, map insertion, path copy and digest text use the passed discovery scope".
  Parity of `capture`'s map charges with `capture_pruned`'s is O-6.
- 3.4: B-20's doc (`h/mb14a_funded.rs`:28-31): "MB14a's JSONC parse IS C2b-1b's metered parser run with the no-op meter
  ... and `parse_metered`'s charges are a pure function of the bytes and the grammar"; `jsonc.rs`:29-34. The memo:
  `:44-45` ("MB14a's `visit` parses a node once ..., so a repeat read pays the lookup and the copy only"). Reuse is
  **proposed**, sound when (a) the charges depend on nothing of the scope but its headroom; (b) every parse the function
  runs was shadow-parsed and its delta paid first; (c) the latch ends on 3.1's row; (d) B-20's overhead ("one extra
  parse per node, at most 32 × 64 KiB per program", `:39`) is counted per graph in the census. The per-graph rule is C1
  RF-3: "Repeated nodes within one graph and shared bases across separate graphs must fund the actual number of
  parses." C1 and O1 accept the reuse.
- 3.5-3.6: **proposed** constraints, no number. The list is C1 RF-3's and O1 F-6's, with item 6's work added at O2
  R2-4 and 7.2's normalization and comparison at C3 ("its normalization/comparison work must be prepaid"). The unmetered-precharge sentence is
  C1 RF-3's; O1's 4.4 disposition agrees ("the bound is argued for every input up to the byte bound, and the
  allocation probe is the control, not the proof"). M3B item 12's charge-before-allocation obligation (C1 RF-3).

## 5. When `allow_js` cannot be derived

(Item 4, Cargo, is not in E1a; see item 7.1 and "Owed to E1b". Numbering follows r1.)

**Old = New (restated, unchanged).** M3B:666: "Each is an internal decision key, aliased at the host boundary to one
new public record (successor S10), so a configuration graph that cannot be read refuses before the Plan". The keys
(M3B:670-673): `native.typescript-config-extends-unresolved`, `-extends-cycle`, `-bound`, `-malformed`. M3B:676-677:
alias `native.typescript-config-unresolved`; request-rejected, exit 2, `CONFIG.INVALID`. M3B:680 (subject). MJ:831
(row 59).

**New (the discovery-time mapping).**
- `Link` (2.1.3), a specifier with no regular-file candidate, an absolute specifier, one rising above the root:
  `extends-unresolved`;
- a node met again on the current path: `extends-cycle`;
- the over-bound arm (2.1.4) or a returned node over 64 KiB, a 33rd node, a 65th `extends` entry, a path over 4,096
  characters: `bound`, judged in M3B:611's order with M3B:680's subject;
- bytes that are not JSONC, a non-object root or `compilerOptions`, a field of the wrong type, a malformed specifier
  (including a malformed package specifier): `malformed`;
- a latched fatal cause (2.1.3): its own end (row 21 for a charge; the capture's refusal for custody, change or host
  I/O; item 7 for the gate);
- the entry marker answered `NotAFile` although it is a lent, captured marker: the host invariant
  `NATIVE_TYPESCRIPT_CONFIG_ENTRY_NOT_A_FILE` (`h/typescript_config.rs`:561-565).

Each refusal ends discovery before the final construction, and the Run takes no mode for that unit.

**Rests on.** M3B:666-680, MJ:831 (quoted); M3B:695 rejects "Guessing a mode for an unreadable graph"; M3B:696
rejects "A partial graph with a disclosure field (`UnitDiscoveryV3` is closed)"; M3B:702. The four conditions are the
ones `Walk::visit`/`resolve` return (`h/typescript_config.rs`:454-500). The latched and invariant lines are **proposed**
(2.1.3); O1: "Accept"; C1: accept as new law. CV ¶4: "Missing implementation is not one of those user-input failures",
hence item 7 ends on a host invariant, never on these keys.

## 6. When `allow_js` may be `None`

**Old.** `h/discovery.rs`:56-60 (`allow_js: Option<bool>`). M3B:607: "A `package.json`-only directory needs none."

**New.**
- 6.1 In the final construction (1.3), `allow_js` is `Some` for the winning marker of every `tsjs` unit whose winning
  marker is `tsconfig.json` or `jsconfig.json`, and `None` for every other marker: a `package.json`, and a
  configuration marker that is shadowed or whose directory is not a unit, also when its bytes are read as another
  unit's base.
- 6.2 A `package.json`-only directory reads no configuration graph and is `js-synthesized` as at the head
  (`h/discovery.rs`:630).
- 6.3 In the final construction and every later reader, a `None` where 6.1 requires `Some` is a host invariant
  (key `j3d-ts.marker-flag-not-derived`). The defaulting reads `fact.allow_js == Some(true)` and
  `fact.allow_js.unwrap_or(true)` (`h/discovery.rs`:626, :628) are replaced by matches that end on that invariant for
  `None`. Candidate identification reads no `allow_js`, so it never meets this invariant.
- 6.4 Final units that differ, other than in mode and kind, from the candidates identification implied are a host
  invariant (key `j3d-ts.discovery-candidates-differ`). The comparison is of each candidate's identity, root, winning
  marker and order, not of counts. Allowing mode and kind to differ admits no value in their place other than the
  derivation's (1.3, 6.1, 6.3).

**Rests on.**
- 6.1-6.2: M3B:607 (quoted); NE:664-672's omitted-value defaults govern an omitted `allowJs` in read bytes, not an
  underived observation (C1 ¶5: "Section 6 correctly distinguishes an omitted option in successfully read bytes from
  an underived observation"). C1 ¶5: "shadowed/non-unit configuration markers may remain `None` ... Preserve the
  distinction when a shadowed marker is nevertheless read as another unit's base." CV ¶4: "Item 14a exempts
  package-only directories". The partition is **proposed**.
- 6.3: LD-DEC-5 item 1 (DECISION.md:51-56): "A state the host itself produced is a host invariant." MJ:774 (row 2):
  "operational-failed / 4 | `SYSTEM.OUTCOME.ILLEGAL_STATE` / host-invariant | absent; the key goes to the operational
  record"; Q52. CV ¶4: "a main entry must not expose the guessing path as implemented". O1 Q5: "The key
  `j3d-ts.marker-flag-not-derived` on MJ row 2 under Q52 is right". Its restriction to the final construction is O1
  F-1's fix and C1 ¶5's ("it must not be triggered by the proposed bootstrap pass"). **Proposed.** `:533`/`:600`'s Cargo
  reads are not reached under E1a (item 7.1) and are E1b's.
- 6.4: **proposed**, from O1 Q8 (h) ("The second discovery's units equal the first's except for modes and kinds;
  otherwise a host invariant"), restated for the one final construction. The key's name is proposed. The comparison's terms are C2 point 4's ("must
  compare candidate identity, roots, winning markers and order, not merely counts; allowing mode/kind differences does
  not permit arbitrary values in place of the derivation").

## 7. The scope gate (new)

**New.** "If a lent `Cargo.toml` marker is present, or resolution attempts a candidate in a shared-rule pruned tree,
end before deriving a placeholder kind or performing the pruned read: operational-failed/4,
`SYSTEM.OUTCOME.ILLEGAL_STATE`, host-invariant key `j3d-ts.discovery-flags-unimplemented`, with reason `cargo` or
`pruned-base`." It is implementation unavailability, not malformed user configuration; `extends-unresolved` is not
used for a valid base. Existing graph failures keep their adopted refusals (item 5). The reason is part of the
operational record beside the key, and the implementing unit's Q52 handoff list names both pairs,
`j3d-ts.discovery-flags-unimplemented` / `cargo` and `j3d-ts.discovery-flags-unimplemented` / `pruned-base`, so the two
ends stay distinguishable. The conditions are closed:
- 7.1 **`cargo`.** The gate fires when any path in the step's lend (`marker_paths()`) has the basename `Cargo.toml`,
  wherever it lies and whether or not it would decide a unit, before candidate identification, before any graph is
  read and before any `discover_units` work.
- 7.2 **`pruned-base`.** During the walk, when an `extends` specifier is reached in walk order and has been classified
  (M3B:620-628) and its candidates normalized (M3B:630-633), the gate fires, before any candidate of that specifier is
  opened, when:
  - the specifier is a well-formed **package specifier** (M3B:626-628): every one of its candidates is
    `E/node_modules/N/...` (M3B:641), so all lie in a pruned tree; or
  - it is a **path specifier** that passed containment and any of its normalized candidates has a segment, wherever it
    occurs, that is equal under NFKC_Casefold (Unicode's `toNFKC_Casefold` mapping, which applies compatibility
    normalization, full case folding and removal of default-ignorable code points) to the NFKC_Casefold of one of the
    shared rule's pruned names: `node_modules`, `.git`, `.hg`, `.svn`, `.jj`, `.opensip` or `target`
    (`sec/custody/discovery_rule.rs`:22-24, :29). Examples: `./node_modules/pkg/tsconfig.json`,
    `./NODE_MODULES/p/base.json`, `./member/.opensip/local.json`, `../other/target/base.json`, and a `node_modules`
    spelled with a decomposed or compatibility form.

  The test is lexical: it reads only the specifier and the candidate strings, never the file system, and needs neither
  the admitted member roots nor any Cargo root. `target` is in the list although the shared rule prunes it only
  directly under a directory holding a `Cargo.toml` (`discovery_rule.rs`:24, :164-166), because 7.1 does not exclude
  every Cargo root: with explicit roots the discovery walk covers only the named roots
  (`sec/custody/discovery_walk.rs`:978-987, :1098-1102, :1192-1210) and the lend exports markers only from that scope
  (`sec/custody/discovery_step.rs`:317-325, :336-352), so a `Cargo.toml` outside them is not lent and the `cargo` gate
  does not fire, while the snapshot walk observes it, adds its Cargo root and prunes its `target`
  (`sec/snapshot_walk.rs`:1002-1033, :690-708; `sec/snapshot_read_set.rs`:141, :630). Counterexample: explicit root
  `app`, `app/tsconfig.json` extending `../other/target/base.json`, with `other/Cargo.toml` and
  `other/target/base.json` present; without `target` in the list the base would be opened inside a pruned tree. The
  test over-refuses on purpose: a directory named `.opensip` that is not at the root or a member root, a directory
  legitimately named `Node_Modules` on a case-sensitive file system, and a lawful base under any directory named
  `target`, also end on the gate. E1c restores precision. The Unicode version of NFKC_Casefold is the one the implementing unit pins and the reviewers
  accept.

  A malformed specifier stays `malformed`, an absolute or escaping one stays `extends-unresolved` (item 5); those are
  decided by classification and containment before this condition is tested. A gate is a fatal cause and latches the
  source (2.1.3): an earlier fatal cause in walk order wins, and nothing in a pruned tree, under any spelling, is
  opened, observed or captured. A later sealing refusal (for example the leftover of MC8:219) does not satisfy this
  requirement. An entry marker never lies in a pruned tree, because markers come from the walk, which does not descend
  into one (M3B:650, U-4a).
- 7.3 Both fixtures of the milestone lie inside the slice: `ts-small-constructs` has no `Cargo.toml` and only
  `"../tsconfig.json"` bases; `js-small-body-parser` reads no graph (survey Q5; O1 Q7).

**Rests on.** **Proposed by this erratum**; the sentence is C1 ¶7's ("This is implementation unavailability, not
malformed user configuration; do not misuse `extends-unresolved` for a valid base. Existing graph failures keep their
adopted refusals."). O1 Q7: "Every package specifier's candidates lie under `node_modules` (M3B:640), so (i) is a
closed condition"; O1 Q7 (i): "It is not `extends-unresolved`, whose M3B:678 remedy would be false." The class: LD-DEC-5
item 1, "A budget or limit crossing on a lawful input is a host defect and stays on the host-fault route" (the input is
lawful; the host cannot yet read it, O1 Q7 (i)); MJ:774 (row 2); Q52 for the named arm. The irrelevant-`Cargo.toml`
trigger is C1 ¶8 ("both out-of-slice gates, including an irrelevant Cargo marker"). Rejected: O1's two keys
(`j3d-ts.typescript-config-pruned-base-unsupported`, `j3d-ts.cargo-workspace-not-derived`), for one key with a
reason (lead's choice; see the header); a fixture allowlist (C1 ¶7: "This semantic cut admits the two stated fixtures
without a fixture allowlist"); reading the pruned base (E1c); deciding Cargo (E1b). **Not a weakening:** every gated
tree ends before any mode or kind is chosen.
The aliases: C2 E1a-RF-2: on a case-insensitive file system `./NODE_MODULES/p/base.json` is "a contained path
specifier; its normalized spelling has no exact shared-rule `node_modules` segment" (the rule compares segments
exactly, `discovery_rule.rs`:118-128; the opener resolves the supplied names, `sec/snapshot_source.rs`:923-967), and "A
later sealing refusal cannot satisfy 'nothing in a pruned tree is opened, observed or captured.'" O2 R2-2: `.opensip`
under a D15 member root is pruned only when the rule is given the member roots (`discovery_rule.rs`:135-151,
`classify_path` :157-178), and reading it is a source read of custody state, which MC8:107 rule 1 says "is never
source"; O2's fix: "Or, more simply, it treats any candidate holding a `node_modules`, VCS or `.opensip` segment as
`pruned-base`." The lexical, conservative form is **proposed**; normalization is O2's advisory (8.9). Rejected:
`classify_path` with the lend's member roots (O2's first fix), because it still compares exact segments and so misses
the case alias; and a file-system probe of the directory-entry spelling, because the probe would itself observe inside
the pruned tree. NFKC_Casefold is chosen as at least as wide as canonical equivalence plus case folding, the two
equivalences the reviewers name; it may refuse more than a given file system equates, which is the stated
over-refusal. `target`: C3 E1a-r3-RF-1 ("The omission's premise is false for explicit discovery roots ... A later
leftover refusal is insufficient under 7.2's no-pruned-read promise"; smallest correction "include `target`, anywhere
and under the same NFKC_Casefold comparison, in the conservative lexical gate"); O3 R3-1 ("add `target` to 7.2's lexical
list. The over-refusal is a lawful base under any directory named `target`"). Rejected: C3's alternative, "a reviewed
mechanism proving the relevant Cargo population complete before reading" (the present lend does not prove it, C3).

## 8. What the implementing unit must deliver (controls)

**New (proposed as the unit's controls).** Each runs through the real discovery step and capture session; each is red
at `e56a4f6d` unless marked.
- 8.1 A `tsconfig.json` with `"allowJs": true` is `js-allowjs` / `js-program`. This replaces
  `sec_discover_1b_known_limit_a_tsconfig_with_allow_js_true_is_discovered_ts_tsconfig` (`h/durable_run_tests.rs`:2200),
  which is deleted.
- 8.2 A `tsconfig.json` inheriting `allowJs: true` through `extends` (a later array entry beating an earlier one; own
  options beating a base) is `js-allowjs`; the base is captured once and is one walk-origin inventory row.
- 8.3 A `jsconfig.json` with `"allowJs": false` is `ts-tsconfig`; one with no `allowJs` is `js-allowjs` with
  `Some(true)` derived, not defaulted.
- 8.4 Bounds at discovery: 64 KiB admits and 64 KiB + 1 refuses `bound`, for the entry and for a base, the uncaptured
  base refused on observed size without being read; a marker already captured as another unit's marker and over the
  bound as this graph's base refuses `bound` with no further project read; 32 nodes admit, 33 refuse; a 33rd node that
  is also over 64 KiB refuses `bound` with the parent as subject; 64 `extends` entries admit, 65 refuse before any
  resolves; 4,096 / 4,097 characters; a cycle; a missing base; an absolute specifier; an escape above the root; a
  malformed specifier; a symbolic-link leaf and a symbolic-link directory component of a base, each
  `extends-unresolved`, not the next candidate. Each ends as `native.typescript-config-unresolved` /
  `CONFIG.INVALID` / exit 2 before the final construction.
- 8.5 The latch: a custody or I/O refusal at the first candidate, with the second candidate present, ends as the
  capture's refusal, never `File` from the second; the first fatal cause is the one reported when a later cause would
  also occur; no native work follows it.
- 8.6 Charges: exact and one short at every charged step: candidate identification, the final construction, the
  marker-map clone (or its replacement), each node capture, an absent candidate's probe, each load, each shadow
  parse, each delta, each walk precharge, the memo, the prepaid diagnostic, graph construction, the retention, the
  latch and refusal records, the validation of 2.4.2, the checks of 6.3, 6.4's retained candidates and
  comparison, and 7.2's NFKC_Casefold normalization and comparison. Each one-short ends on its ledger's exhaustion with no
  native read or parse after it; the exact budget passes.
- 8.7 Parse funding: a base shared by two units' graphs is funded twice; a base repeated as two edges within one graph
  is funded once; the charged parse count equals the actual one.
- 8.8 Binding, through the real sequence (discovery, provisional selection and layout units, walk, read set, seal,
  then the validation): a file created at an earlier candidate after discovery's capture and before the walk ends the
  invocation at the validation (2.4.2), for a selected unit and for a unit no requested tuple names, before
  program-specific planning, with no reselection, resealing or retry; a changed graph with an unchanged `allowJs` also
  refuses. A captured base rewritten before the walk refuses the snapshot
  (2.2.2).
- 8.9 Leftover: on the case-insensitive macOS lane, a `"./Base.json"` specifier against a file `base.json` captures
  under the specified spelling, the walk inventories `base.json`, and sealing refuses on the leftover; the Run never
  plans. The same holds for a Unicode-normalization variant: an NFC-spelled specifier against a file whose name is
  stored NFD.
- 8.10 `None` and candidates: candidate identification chooses no mode; 6.3's invariant fires only in the final
  construction; a shadowed `jsconfig.json` read as a base stays `None`; a mutation replacing a derived flag with
  `None` or a constant is red; final units differing from the identified candidates in identity, root, winning marker
  or order end on 6.4's invariant, and its retained set and comparison are charged (8.6).
- 8.11 Custody: a marker leaf is judged under config-file custody and a non-marker base is not (2.2.3).
- 8.12 Gates: a lent `Cargo.toml` anywhere (including one under `tests/fixtures/` that decides no unit) ends on
  `j3d-ts.discovery-flags-unimplemented` / `cargo` before any graph read or `discover_units` work; a package
  specifier and a path specifier into `node_modules` each end on `pruned-base` with no open, observation or capture
  under the pruned tree; so do, on the case-insensitive macOS lane, `./NODE_MODULES/p/base.json` against a physical
  `node_modules/p/base.json`, a `node_modules` segment spelled in a normalization variant, and
  `./member/.opensip/local.json` under an admitted D15 member root; so does, with explicit root `app` and a sibling
  `other/Cargo.toml` that is not lent, `app/tsconfig.json` extending `../other/target/base.json`, refused before any
  candidate is opened; the operational record carries the key and the reason; a malformed package specifier is `malformed`, not the gate; an earlier fatal cause in walk
  order wins over a later gate.
- 8.13 A `package.json`-only directory reads nothing beyond its marker capture and is `js-synthesized` (green at the
  head; kept).
- 8.14 The two milestone fixtures give their recorded units: `ts-small-constructs` three `ts-program` units, each
  nested base read and inventoried once, no gate; `js-small-body-parser` one `js-synthesized` unit.

**Rests on.** M3B:704-720 (14a's controls), rerun at discovery; MC8:230 (C1-T24); C1 ¶8; O1 Q8 (a), (c)-(i). The list as
a requirement is **proposed**. Not in E1a: O1 Q8 (b) and C1 ¶8's "lawful TOML resource exhaustion" (E1b); C1 ¶8's
"package/base with no selected layout authorization" (E1c). C1 ¶8: these controls "do not clear SEC-DISCOVER-1b's
outstanding member/VCS wiring finding."

## What E1a does not change

- Item 14a's grammar, resolution, bounds, inheritance rule and four keys (M3B:609-673), the S10 termination
  (M3B:675-678), and U-1's precedence (M3B:580). The function gains one `ConfigEntry` arm (2.1.4) and nothing else.
- U-2 (M3B:582) and every Cargo behaviour: not reached under E1a (7.1).
- B-20's charges at the Plan (`plan.rs`:2276-2289); the discovery ledger's caps (M3B:500).
- No D9 row, no public detail, no price number.

## Owed to E1b (Cargo) and E1c (pruned bases)

Neither binds anything here; this records what the reviewers already said so the work is not lost.

**E1b (Cargo; removes the `cargo` gate).** r1 items 4, 5.2, O-5, O-7 are its starting text.
- **Which manifests are parsed (O1 F-2).** "derive `is_cargo_workspace` exactly for the `Cargo.toml` markers whose flag
  U-2 reads: the selected explicit roots, and, in depth order, each `Cargo.toml` directory that no shallower derived
  workspace encloses. Every other `Cargo.toml` keeps `None`". Reason: a member below a workspace is folded "on
  `under_unit` alone (`discovery.rs`:580-596)", so r1's "every lent manifest" refuses trees U-2 admits. Control O1 Q8
  (b): "A folded member's malformed `Cargo.toml` under a workspace is not parsed and the tree admits."
- **Classification (C1 RF-4).** Accept a request rejection for invalid UTF-8, syntax and non-table `workspace`, "with
  an adopted alias/row/remedy before claiming that public termination". Replacement sentence: "Syntax, encoding and
  workspace-shape failures are the new configuration rejection; parser resource exhaustion on otherwise lawful input
  remains a host fault unless a separately adopted upstream input bound applies." "SL:126-127 already supplies the 4 MiB
  config-file custody bound; retain its owner's route rather than relabeling it TOML syntax."
- **O-7, O1 F-8.** "5.2 names the bounds: 4 MiB (`canonical.rs`:5), the pinned parser's recursion limit, and
  1,000,000 nodes (`toml.rs`:8). They become the manifest's stated bounds, and the O-5 remedy names each one. A
  crossing is then a request rejection, by M3B:672 and LD-DEC-5 item 1's 'upstream bound'." **Not reconciled here:**
  C1 keeps resource exhaustion a host fault unless an upstream bound is separately adopted; O1 proposes adopting the
  parser's limits as that bound. The two agree on the condition and differ on whether E1b should adopt the bound;
  E1b must choose, with both reviewers.
- **O-5.** Public alias, D9 row and remedy before the exit-2 projection (C1 ¶6: "an interim host-fault arm cannot
  simultaneously satisfy control 7.5's exit-2 assertion"; O1 Q6: Q52 named arms until CLI wiring, LD-DEC-5 item 8).
- **TOML price (C1 RF-3; O1 4.4).** "An unmetered precharge has a source-derived bound over all admissible inputs of
  the pinned implementation; adversarial allocation probes validate it, including failures and destruction." "Prove
  the stated stack profile before parse **and drop**." O1: the 2 MiB stack "is shown for the thread that actually runs
  discovery (main thread, or a thread spawned with an explicit stack size)". O1: 4.3 (typed result) is an
  implementation note; 4.1-4.2 carry the law. C1 ¶8 control: lawful TOML resource exhaustion.

**E1c (pruned bases; removes the `pruned-base` gate).** r1 2.1.2's `capture_pruned` half, 2.2.1's pruned-row clause,
O-2, O-3 and control 7.12 are its starting text.
- **O-2 (C1 ¶6).** "may close in implementation by constructing the admitted extent from the lend and resolved
  ignores."
- **O-3 (C1 ¶6).** "needs a C1c authorization successor before pruned support is enabled ... 'refuses at sealing' is not
  the promised support in M3B:650." C1 disposition 2.2.1: "a permanent missing authorization is not fulfillment of the
  inventory obligation." C1 ¶8: full support needs a control with "a package/base with no selected layout
  authorization, not only an already-authorized package."
- **O-3 (O1 Q6).** "need an MC8 (C1c) successor before any pruned base is read. 7.12's 'refuses at sealing' is not
  shown. `read_set` re-origins a captured file it reaches below an admitted package (`snapshot.rs`:790-797), and
  `leftovers()` filters only `origin.is_none()` (:995-999). So a base inside an admitted package would not be a
  leftover." r1's 7.12 claim is therefore withdrawn, not carried.
- O1 disposition 2.1.2: the `capture_pruned` half "is an implementation note, outside the first cut".
- **Interim cost (O2 section 2, advisory).** "a package specifier whose package is simply missing now ends at exit 4,
  where adopted law would give `extends-unresolved` at exit 2. That is acceptable for the interim; E1c restores it."
  The same holds for 7.2's over-refusals (a lawful base under a directory 7.2's lexical test catches).

## Open after E1a

Each is put to both reviewers; E1a closes none except as stated.
- **O-4. The D9 row for the validation's refusal (2.4.2).** Interim: a Q52 named arm (2.4.3). *Closes by:* an MJ
  successor row before CLI wiring (LD-DEC-5 item 8; C1 ¶6; O1 Q6).
- **O-6. `capture`'s map charges.** `capture` charges no lookup before `contains_key` (`h/snapshot.rs`:547) and its
  insert inside `read_once` (`:1098-1099`); `capture_pruned` charges `capture_map_cost` first (`:571-580`). *Closes by:*
  the implementing unit's charge control (C1 ¶6; O1 Q6).
- **O-8 (prices only).** The policy is closed by 3.1 (M3B:499). The prices of 3.5 are the implementing unit's.
- **O-10. The exact step and ledger of the validation (2.4.2).** E1a fixes the window: after sealing, before
  program-specific planning or committing the selection, no later than the Plan's first step. *Closes by:* the
  implementing unit naming the step and ledger, "with all graphs funded and no budget reset" (C2 E1a-RF-1), under 3.6,
  accepted in implementation review by both reviewers.

**Closed here.** O-1: no main integration and no Run before the unit implementing E1a is in the composition and accepted
by both reviewers (`LEAD-NOTES.md`, the lead's ordering; C1 ¶6: "no interim gate is needed on the unexecuted branch";
O1 Q6: "the lead's ordering is enough"); SEC-DISCOVER-1b's stated limit and pinning test stand on the branch only.
O-9: by 2.2.3. O-2, O-3, O-5, O-7: moved to E1c/E1b.

## Sentence | adopted basis or proposed

| Sentence | Basis |
|---|---|
| 1.1 `allow_js` from `effective_allow_js` over captures; no second project read | Adopted: M3B:581, :607; MC8:208, :216; Q100 items 1, 3 (lead) |
| 1.2 bytes are the capture's retained bytes | Adopted: MC8:215, :218; load mechanism **proposed** |
| 1.3 candidates by mode-independent rules, then derivation, then one final construction; no placeholder mode | **Proposed** (C1 RF-1 sentence; M3B:607 basis) |
| 1.4 the Plan keeps the same function | Adopted: M3B:581, :607 |
| 2.1.1 capture exactly what the reader reads, in its order; probes are not captures | Adopted: M3B:607, :636-648; order and probe distinction **proposed** |
| 2.1.2 `capture` for every candidate E1a opens; none caught by 7.2's lexical test | Adopted: `capture`'s role (MC8:208), M3B:650; restriction **proposed** (scope) |
| 2.1.3 File / NotAFile / Link / over-bound / fatal; typed latch, no work after it | Link: adopted M3B:654-655, :670, :702; the rest **proposed** |
| 2.1.4 new `ConfigEntry` over-bound arm judged in `visit`; observed size returns the arm without reading; actual bytes still enforced | Order adopted: M3B:611, :680; arm and sentences **proposed** (O2 R2-3, C2 point 5) |
| 2.1.5 the opener reports a link distinctly (security crate) | **Proposed** (requirement) |
| 2.2.1 graph nodes are resolved inputs; walk rows; leftovers refuse | Adopted: MC8:219; "resolved input" **proposed** |
| 2.2.2 a captured base rewritten before the walk refuses | Adopted: MC8:217, :230; extension **proposed** |
| 2.2.3 marker leaf config-file custody; non-marker base ordinary C1 source custody | Adopted: M3B:653; reading of both reviewers (C1 ¶6, O1 Q6) |
| 2.3 MC8 C-N1 bullet | Adopted basis: MC8:207, M3B:650/:653; sentence **proposed** |
| 2.4.1 discovery keeps each derived graph (operational) | **Proposed** |
| 2.4.2 pre-seal selection provisional; after sealing and before program-specific planning or committing the selection, validate every graph and mode; no reselection, resealing or retry; binds the pre-seal consumers | **Proposed** (C1 RF-2, C2 E1a-RF-1 sentences; O2 R2-1; M3B:607; MC8:217) |
| 2.4.3 interim Q52 named arm | Adopted (lead): Q52; row O-4 |
| 3.1 everything in items 1-2, 6 and 7 charged before its work, error paths included; scope is not charging; discovery exhaustion is row 21 | Adopted: M3B:499, MJ:793; latch end and C1's scope sentence **proposed** |
| 3.2 `parse_captured`'s load-half charges, `limit + 1` | **Proposed** |
| 3.3 node captures charged as the marker capture | Adopted reading: CV ¶3; parity O-6 |
| 3.4 B-20 reused on the discovery ledger; per-actual-parse funding | **Proposed** (B-20's doc as basis) |
| 3.5-3.6 owed prices; constraints; unmetered-precharge rule | **Proposed** (no number) |
| 5 tsconfig/jsconfig failures: four keys, `native.typescript-config-unresolved`, `CONFIG.INVALID`, exit 2 | Adopted: M3B:666-680, :695-702; MJ:831 |
| 5 latched-cause and entry-invariant lines | **Proposed** |
| 6.1 `Some`/`None` partition | **Proposed** (M3B:607 basis; C1 ¶5) |
| 6.2 package-only directories read nothing | Adopted: M3B:607; CV ¶4 |
| 6.3 missing required flag is `j3d-ts.marker-flag-not-derived`, final construction only | Adopted rule: LD-DEC-5 item 1, MJ:774, Q52; key and scope **proposed** |
| 6.4 final units differ from candidates in identity, root, winning marker or order: `j3d-ts.discovery-candidates-differ`; no value but the derivation's | **Proposed** (O1 Q8 (h); C2 point 4) |
| 7 scope gate `j3d-ts.discovery-flags-unimplemented` (`cargo`, `pruned-base`), closed lexical conditions under NFKC_Casefold, reason in the operational record | **Proposed** (C1 ¶7 sentence; C2 E1a-RF-2; O2 R2-2, section 2; LD-DEC-5 item 1, MJ:774, Q52; M3B:626-641; `discovery_rule.rs`:22-29; `target`: C3 E1a-r3-RF-1, O3 R3-1) |
| 8 the controls; replacement of the known-limit test | **Proposed** (M3B:704-720, MC8:230 basis) |
