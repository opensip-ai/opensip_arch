# ERRATUM E1A-E2 r2: a path candidate longer than item 14a's node-path bound is `bound`, judged before it is opened (erratum to DISCOVERY-FLAGS-E1a r4 and M3-B r10 item 14a)

**Status: PROPOSED (r2).** Not law until both reviewers (Codex, Claude) accept it. Author of r1: Claude
claude-opus-5-5/medium, implementation worker of DISCOVERY-FLAGS-1 stack fix round 3, for the lead, R2-DEEP (preflight:
`ROUTE-OK R2-DEEP claude claude-opus-5-5/medium`). Written under lead ruling F-6 ("Ruling after fix round 2",
`RULINGS-STACK-FIX-1.md`), on the S-1 findings of `HANDOFF-STACK-FIX-2.md` (item 3).

**Changes from r1 (by the lead, Claude Fable 5.2; nothing else differs):** (i) statement 1 and its "not skipped"
argument are limited to PATH candidates; an over-long PACKAGE candidate is left to erratum E1c, and the Open bullet
that extended the rule to package candidates is replaced (Claude E2-R1; Codex E1A-E2-A-1: a package specifier tries
ancestor directories next, and a later candidate can be shorter and can be the file the compiler reads); (ii)
statement 3 and the matching sentence of "Old" speak only of a file the discovery walk ENCOUNTERS within its admitted,
non-pruned scope, and say that nothing here widens the walk (Codex E1A-E2-RF-1: a file under a pruned tree or outside
an explicit root is never listed, so its existence does not choose the deciding phase); (iii) statement 1 says in
words that at the post-seal validation the result is a rederivation result under E1a 2.4, not a new direct
termination (Codex section 1); (iv) the compiler basis says the "no newly refused configuration" claim holds on Linux
as well as macOS (Claude A-2). The outcome of statement 1 for path candidates, and statement 2, are as in r1.

**What it amends (the files are not edited):**
- M3-B r10 (`ARCH/docs/implementation/m3/config-discovery-b/PROPOSAL.md`, = **M3B**), item 14a: the place of the
  node-path check ("the path length with the other new-node checks, before the node's bytes are judged", M3B:611; the
  order of a node's checks, M3B:47), for the sources at discovery and at the post-seal validation.
- DISCOVERY-FLAGS-E1a r4 (= **E1a**) item 8.4's "4,096 / 4,097 characters" leg (what the 4,097 leg is).

**The basis.** TypeScript 6.0.3 as provisioned: `tools/typescript-boundary/node_modules/typescript/lib/typescript.js`
under the packages root `/Users/sb/code/opensip-ai/opensip`, sha256
`569177652966bd528c319171c7dd22860dbf72bde116cbc4f644f1d02bb12e39` (the `tools/typescript-lanes.json` pin, as in
erratum M3B-14A-E1 r2). Pinned Node: sha256 `1ee75375e33b94fc34b3b19aede049e11dae90efb63b374dc96d6bdace70c4b8` (the
lane file's `node` pin), v24.16.0 darwin-arm64. Line numbers are of that `typescript.js`.

## Old

M3B:611: "at most **4,096 characters** in a node's canonical path ... the path length with the other new-node checks,
before the node's bytes are judged." M3B:47: "for a new base, the 32-node check; then, for every node, the entry
included, the 4,096-character path check, the 64 KiB check, ...". E1a 8.4: "4,096 / 4,097 characters ... Each ends
as `native.typescript-config-unresolved` / `CONFIG.INVALID` / exit 2 before the final construction."

At discovery and validation the node-path check runs only after a candidate has been READ, and every path the
session can read is a `LogicalPath` (`identity/src/descriptors.rs` `LogicalPath::parse`: at most 4,096 scalars). So a
4,097-character candidate is never read and never judged by item 14a: it is refused first by `LogicalPath`, in the
discovery walk when the walk lists such a file within its admitted, non-pruned scope, and otherwise in the candidate
open, and ends today as
`j3d-ts.unprojected:capture`, an illegal-state end for a property of the user's configuration (fix round 2, S-1).

## New

1. **The bound on a node's path is decided on each PATH candidate's spelling, before the candidate is opened.** At
   discovery (the capturing source) and at the post-seal validation (the sealed source), each path specifier's candidate's
   character count is compared with item 14a's 4,096-character bound, the comparison charged before it is made, after
   item 7.2's gate decides that candidate and before any open, observation, capture or load of it. A candidate over
   the bound is item 14a's `native.typescript-config-bound` for that node (subject: the candidate's canonical path,
   M3B's subject rule), with nothing opened. It is **not** skipped in favour of the next candidate: the path
   specifier's resolution ends at that candidate, as it ends at the first regular file. At the post-seal validation
   this is the outcome of the REDERIVATION that E1a 2.4 compares: a graph that derived at discovery and rederives to
   this refusal differs, and ends as E1a 2.4 says (`discovery-graph-differs`); statement 1 adds no direct
   termination there. The refusal then takes item 14a's
   existing order of a new node's checks (M3B:47): the 32-node check for a new base comes first, so a 33rd node that
   is also over the path bound refuses `bound` with its parent as subject, as today. The entry is not affected: it is
   a lent marker, already a `LogicalPath`.
   - For a PATH specifier, skipping would never change which file wins: its second candidate is the first followed by
     `.json`, so it is longer; when the first is over the bound, so is the second. It changes only the refusal: a
     skip would end on `extends-unresolved`, which tells the user the base is missing when it is too long.
   - When the first candidate N is within the bound and absent, and the second, N followed by `.json`, is over it
     (N of 4,092 to 4,096 characters), the second is `bound` without being opened.
   - This statement says nothing about PACKAGE candidates. They are all gated today (E1a 7.2). A package specifier's
     later candidates lie in ancestor directories and can be SHORTER than an over-long nearest one, so whether an
     over-long package candidate is refused or passed over can change which file wins; that rule belongs to erratum
     E1c, which ungates packages, and is not decided here.
2. **E1a 8.4's 4,097-character leg is this refusal**, exercised with a base that is ABSENT from the project: a
   specifier whose (only, or first) candidate is 4,097 characters ends as `native.typescript-config-bound`, aliased
   `native.typescript-config-unresolved` / `CONFIG.INVALID` / exit 2, before the final construction, with no capture
   or open of the candidate. The 4,096-character leg is unchanged (a present base of 4,096 characters admits).
3. **Not changed:** a file that the existing discovery walk ENCOUNTERS within its admitted, non-pruned scope, and
   whose project path exceeds `LogicalPath`'s limit, remains the walk's refusal (`discovery_walk.rs` `listed_path`,
   `NameUnrepresentable`), before any configuration is read, as today. Its outcome row (a name the snapshot cannot
   represent) is a separate matter, recorded for the refusal-projection follow-up; this erratum does not touch it.
   Nothing here widens the walk or authorizes an observation of a file the walk does not visit (a pruned tree,
   M3B:565, :650; a tree outside the named roots, M3B:865). Existence alone does not choose the deciding phase: for a
   candidate naming a file outside the walk's scope, statement 1 decides on the candidate's spelling without probing
   for the file; for a pruned candidate, the gate of E1a 7.2 decides first.

## Rests on: the compiler's own function

`getExtendsConfigPath` (typescript.js:43744-43767, quoted in erratum M3B-14A-E1 r2) forms N
(`getNormalizedAbsolutePath`, :43747), probes it with `host.fileExists`, and, when it is not a file and does not end
in `.json`, probes N followed by `.json` (:43748-43750). It has **no bound of its own on a path's length**: nothing in
`getExtendsConfigPath`, `getNormalizedAbsolutePath` or the config parse compares a length. On a real file system
`host.fileExists` is `sys.fileExists` (:8628-8630), `fileSystemEntryExists` (:8614-8626) over `statSync`
(:8412-8418), which catches every error and answers `undefined`, so a path the operating system cannot stat is simply
"not a file", and `readFile` of it fails ("Cannot read file", 5083).

So the compiler's answer for an over-long base depends on the host, not on a bound: an in-memory host reads it; the
real macOS file system cannot stat an absolute path of 1,024 bytes or more (PATH_MAX), so the compiler reports the
base, or even the entry, as unreadable. Item 14a's 4,096 bound is the product's own (M3B:37: `CanonicalPath`'s
`maxLength`), not the compiler's. Statement 1 refuses what the record cannot hold; the compiler, on the real lane,
fails on every such path too (rows E-F below; on Linux as well: a project-relative path of 4,097 characters is at
least 4,097 bytes, so its absolute spelling exceeds Linux's PATH_MAX of 4,096), so no compiler-accepted configuration
that a real lane can read is newly refused. What statement 1 changes is only the product's refusal key (from a capture invariant to item 14a's
`bound`).

## Rests on: observed answers of the provisioned compiler

The pinned compiler under the pinned Node. Rows A-D: `ts.getParsedCommandLineOfConfigFile` over an in-memory host
(root `/r`; `fileExists` and `readFile` answer from the listed files only); the probe and read columns give each path's
length in characters relative to the root. Rows E-F: the real file system through `ts.sys`. `T` =
`{"compilerOptions":{"allowJs":true}}`. Scratch scripts: `e2probe/probe.js`, `e2probe/pathmax.js` in the worker's
scratch directory; their cases are restated here.

| Row | Entry and `extends` | Files present | Compiler's probes | Read | Result |
|---|---|---|---|---|---|
| A | `app/tsconfig.json`, `./<chain>/base.json` | the base, 4,097 chars, `T` | 4,097 | 17, 4,097 | `allowJs` true: read, no bound |
| B | the same | none | 4,097 | 17, 4,097 | 5083 "Cannot read file" |
| C | `app/tsconfig.json`, `./<chain>/base` (N 4,096 chars) | `N.json`, 4,101 chars, `T` | 4,096, 4,101 | 17, 4,101 | `allowJs` true: the second candidate, over 4,096 |
| D | the same with N of 4,097 | `N.json`, 4,102 chars, `T` | 4,097, 4,102 | 17, 4,102 | `allowJs` true |
| E | real FS: deep entry `app/<chain>/tsconfig.json` (4,084 chars relative, 4,201 bytes absolute) extending `./bbbbbbbbbbbbbbbbbbbb.json` (4,096 chars, present) | both | - | - | 5083 "Cannot read file" on the ENTRY; `sys.fileExists(entry)` false |
| F | real FS: `tsconfig.json` at absolute lengths 1,000 / 1,023 / 1,024 / 1,025 / 1,100 bytes | each | - | - | `sys.fileExists` and `sys.readFile`: true, true, false, false, false |

The compiler's probes are statement 1's candidates in order in every row (A-D). Rows A, C and D show that only the
product bounds the length; rows E and F show that on the real macOS lane the compiler itself cannot read any of
these files (nor any config whose absolute path reaches 1,024 bytes).

## Open (for the lead and the reviewers)

- **The compiler fails far below 4,096 on the real lane** (rows E, F). Statement 1 is consistent with it (both
  refuse every path over 4,096), and the ruling did not depend on the compiler. But it means the 4,096 leg that the
  product admits (fix round 2's control: a 4,084-character entry and a 4,096-character base) is a configuration the
  pinned compiler, run on macOS over that tree, reports as unreadable. This is a pre-existing gap between the
  product's bound (relative characters, opened component by component) and the compiler's (absolute bytes, one
  system call), inherited from M3B r10, not created here. Whether the product should bound the absolute spelling, or
  the provider must open paths component by component, is not this erratum's question; it bears on statement 1 only
  in that "the compiler's own answer" for such paths is a host failure, not a rule.
- Package candidates are gated today (7.2: every package candidate lies under `node_modules`). Statement 1 does NOT
  extend to them: the rule for an over-long package candidate is owed to erratum E1c (see statement 1's last
  bullet).
- The provider follow-on (erratum M3B-14A-E1's) should implement statement 1 in `providers/typescript/src/context/
  graph.ts` too, so the two cannot describe different outcomes for an over-long candidate.

## Sentence | adopted basis or proposed

| Sentence | Basis |
|---|---|
| Statement 1 (decided before open, `bound`, not skipped) | **proposed**, lead ruling F-6; M3B:611 and :672 (the bound and its key, unchanged); M3B:47 (the order, kept) |
| Statement 2 (8.4's 4,097 leg) | **proposed**, F-6; E1a 8.4 (its outcome, unchanged) |
| Statement 3 (the walk's refusal unchanged) | adopted behaviour (SEC-DISCOVER-1b walk); its row: **open**, the refusal-projection follow-up |
