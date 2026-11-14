# ERRATUM M3B-14A-E1 r2: the path specifier's candidates are formed from the normalized path (erratum to M3-B r10 item 14a)

**Status: PROPOSED (r2).** Not law until both reviewers (Codex, Claude) accept it. Author of r1: Claude
claude-opus-5-5/medium, implementation worker of DISCOVERY-FLAGS-1 stack fix round 1, for the lead, R2-DEEP (preflight:
`ROUTE-OK R2-DEEP claude claude-opus-5-5/medium`). Written under lead ruling F-4 (`RULINGS-STACK-FIX-1.md`), on Claude's
STK-R1 and STK-R2 (`review-opus/VERDICT-STACK.md`).

**Changes from r1 (by the lead, Claude Fable 5.2; nothing else differs):** statement 2 names its subject and no longer
gives one reason for every root (Codex M3B-14A-E1-RF-1: a project directory whose own name ends in `.json`; Claude's
advisory on the subject); the explanation of statement 2 under "the compiler's own function" is split into the two
cases; one observed row is added (Codex's probe); the sentence after the table counts three root rows; statement 1
says in words that normalization is the containment-aware one of M3B:631-632 (Codex section 2). The outcome of every
statement is unchanged.

**What it amends (the file is not edited):** M3-B r10, `ARCH/docs/implementation/m3/config-discovery-b/PROPOSAL.md`
(= **M3B**; byte-identical to `PROPOSAL-r10.md`), item 14a, "Resolution of one specifier S", the path-specifier
candidates sentence (M3B:638), and, as a consequence, DISCOVERY-FLAGS-E1a r4 item 7.2's first-candidate argument.

**The basis.** TypeScript 6.0.3 as provisioned: `tools/typescript-boundary/node_modules/typescript/lib/typescript.js`
under the packages root `/Users/sb/code/opensip-ai/opensip`, 9,144,216 bytes, sha256
`569177652966bd528c319171c7dd22860dbf72bde116cbc4f644f1d02bb12e39`, equal to the pin in `tools/typescript-lanes.json`
(:734-736); `package.json` version `6.0.3`. Line numbers below are of that file.

## Old

M3B:636-639: "**Resolution of one specifier S** from a configuration file in project-relative directory D (`""` for the
root): **A path specifier:** **Candidates:** the normalized `D/S` when S's last segment ends in `.json`; otherwise the
normalized `D/S`, then the normalized `D/S.json`. **Choice:** the first that is a regular file wins."

Read literally, the second candidate appends `.json` to S and then normalizes. When S's last segment is `.` or `..`,
that gives a different file from the compiler's: `./sub/.` gives `sub/..json` (the compiler reads `sub.json`),
`./x/..` from `app` gives `app/x/...json` (the compiler reads `app.json`), and `./a.json/.` tests `.json` on `.` and so
adds a second candidate the compiler never tries. The same reading breaks E1a 7.2's first-candidate argument: for
`./x/node_modules/..` the second candidate, `app/x/node_modules/...json`, holds a `node_modules` segment that the first
candidate, `app/x`, does not.

## New

1. Let N be the normalized `D/S` (lexical, as M3B:631 says; containment is decided as M3B:632 says, during that
   normalization: a `..` that would rise above the project root makes the specifier unresolved even if later segments
   would return inside). If N ends in
   `.json` (compared exactly, case-sensitively), the one candidate is N. Otherwise the candidates are N, then N followed
   by `.json`. The first that is a regular file wins (M3B:639, unchanged).
2. If, for a specifier S in a configuration file in directory D, N is the project root itself (no segment left), the
   specifier is unresolved (`native.typescript-config-extends-unresolved`). The root is a directory, never a regular
   file, so the first candidate never wins; and the compiler then either reads nothing (when the root directory's own
   name ends in `.json`, it tries no second candidate and fails to read the directory) or tries the root's own name
   followed by `.json`, a file outside the project. In neither case does the compiler read a file of the project.
3. Consequence for E1a 7.2: every segment of both candidates is a segment of N, except the last segment of the second,
   which is N's last segment with `.json` appended. That segment cannot equal a pruned name: each of the seven names
   (`node_modules`, `.git`, `.hg`, `.svn`, `.jj`, `.opensip`, `target`) is its own NFKC_Casefold image and none ends
   in `.json`, while the image of a segment ending in `.json` ends in `.json` (the five ASCII characters `.json` are
   fixed points of NFKC_Casefold, are starters, and compose with nothing before them). So the gate decided on N's
   segments decides both candidates, before either is opened.

## Rests on: the compiler's own function

`getExtendsConfigPath` (typescript.js:43744-43767), called once per `extends` string by `getExtendsConfigPathOrArray`
(:43650) with `basePath` the directory of the configuration file that names it (`directoryOfCombinedPath`, :43652):

```js
43745  extendedConfig = normalizeSlashes(extendedConfig);
43746  if (isRootedDiskPath(extendedConfig) || startsWith(extendedConfig, "./") || startsWith(extendedConfig, "../")) {
43747    let extendedConfigPath = getNormalizedAbsolutePath(extendedConfig, basePath);
43748    if (!host.fileExists(extendedConfigPath) && !endsWith(extendedConfigPath, ".json" /* Json */)) {
43749      extendedConfigPath = `${extendedConfigPath}.json`;
43750      if (!host.fileExists(extendedConfigPath)) {
43751        errors.push(createDiagnosticForNodeInSourceFileOrCompilerDiagnostic(sourceFile, valueExpression, Diagnostics.File_0_not_found, extendedConfig));
43752        return void 0;
43753      }
43754    }
43755    return extendedConfigPath;
43756  }
```

- Statement 1. Line 43747 normalizes first (`getNormalizedAbsolutePath`, :8893-8967, drops `.`, lets `..` remove the
  preceding segment, and returns no trailing separator for a path longer than its root). Line 43748 tests `.json` on
  that NORMALIZED path with `endsWith` (:3559-3562, case-sensitive when `ignoreCase` is absent, as here), and line
  43749 appends `.json` to the normalized path. When the normalized path ends in `.json` it is returned whether or not
  it exists (:43755), so it is the only candidate; an absent one fails later as "Cannot read file". `host.fileExists`
  is `sys.fileExists` (:8628-8630), `stat(...).isFile()`, so a directory never wins: "the first regular file wins".
- Statement 2. With N the project root, line 43748 finds no file (a directory). Two cases. (a) The root directory's
  absolute spelling does not end in `.json`: line 43749 forms `<root>.json`, the root's parent joined with the root's
  name and `.json`, outside the project. (b) The root directory's own name ends in `.json` (nothing forbids a project
  directory of that name): line 43748's second test fails, the append is skipped, the directory's path is returned
  (:43755) and the read fails ("Cannot read file", diagnostic 5083); no second candidate is tried. Either way no file
  of the project is read, which is what statement 2's outcome rests on.
- Statement 3 is a consequence of statement 1 and of 7.2's list; it uses nothing more of the compiler.

## Rests on: observed answers of the provisioned compiler

The pinned compiler (above), run by the pinned Node (120,573,328 bytes, sha256 `1ee75375...70c4b8`, equal to
`tools/typescript-lanes.json`'s `node` pin) through `ts.getParsedCommandLineOfConfigFile` over an in-memory host whose
`fileExists` is true only for the listed files and whose `directoryExists` is true only for the listed directories. The
probe script is the worker's scratch file `probe.js` (its cases are restated here, so the record does not depend on
it). Project root `/r`; `T` = `{"compilerOptions":{"allowJs":true}}`, `F` = `{"compilerOptions":{"allowJs":false}}`.

| Entry `extends` (from `app/tsconfig.json` unless said) | Files present | Compiler's existence probes, in order | File read | `allowJs` |
|---|---|---|---|---|
| `./sub/.` (STK-R1) | `app/sub.json`=T, `app/sub/..json`=F, dir `app/sub` | `app/sub`, `app/sub.json` | `app/sub.json` | true |
| `./x/..` | `app.json`=T, `app/x/...json`=F | `app`, `app.json` | `app.json` | true |
| `./a.json/..` | `app.json`=T | `app`, `app.json` | `app.json` | true |
| `./x/node_modules/..` (STK-R2 1) | `app/x`=T (a file) | `app/x` | `app/x` | true |
| `./node_modules/..` (STK-R2 2) | `app.json`=T, dir `app/node_modules` | `app`, `app.json` | `app.json` | true |
| `./a.json/.` | `app/a.json`=T | `app/a.json` | `app/a.json` | true |
| `./a.json/.` | only `app/a.json.json`=T | `app/a.json` | (fails: "Cannot read file '/r/app/a.json'") | - |
| `./b.json` | only `app/b.json.json`=T | `app/b.json` | (fails: "Cannot read file") | - |
| `./b.JSON` | `app/b.JSON.json`=T | `app/b.JSON`, `app/b.JSON.json` | `app/b.JSON.json` | true |
| `./d.json` | dir `app/d.json`, `app/d.json.json`=T | `app/d.json` | (fails: "Cannot read file") | - |
| `./base` | `app/base`=T, `app/base.json`=F | `app/base` | `app/base` | true |
| `./.` from `tsconfig.json` at the root | `/r.json`=T | `/r`, `/r.json` | `/r.json` (outside) | true |
| `./..` | `/r.json`=T | `/r`, `/r.json` | `/r.json` (outside) | true |
| `./.` | `app.json`=T | `app`, `app.json` | `app.json` | true |
| `./..` from `/r.json/app/tsconfig.json` (project root `/r.json`; Codex's probe) | `/r.json.json`=T | `/r.json` | (fails: "Cannot read file '/r.json'", 5083) | - |

Every row agrees with statements 1 and 2: the compiler's probes are exactly the candidates of statement 1, in order,
and the three root rows either read outside the project or read nothing, which statement 2 refuses. Under the old literal reading the first
five rows and the `./a.json/.` rows give different candidates; under statement 1 the product's candidates equal the
compiler's probes in every row.

## Open (the compiler does something the three statements do not say)

These do not contradict statements 1-3: each is a specifier that item 14a's grammar (M3B:620-628, unchanged by this
erratum) classifies before resolution, and the product REFUSES it as `malformed` where the compiler resolves. No case
was found where the product, under statements 1-3, resolves to a different file from the compiler's. They are listed
so that the reviewers and the lead can decide whether the grammar should follow the compiler; this draft does not
choose.

- O-1. **A trailing separator.** `./sub/` with `app/sub.json`=T: the compiler probes `app/sub`, `app/sub.json` and reads
  `app/sub.json` (line 43747's normalization removes the trailing separator). M3B:622 makes S "ends with `/`"
  malformed. This is the refusal Claude's verdict section 1 already lists for backslashes (also normalized by the
  compiler, line 43745).
- O-2. **A bare `.` or `..` (no slash).** Line 43746 does not take the path branch for `.` or `..`; the compiler hands
  them to `nodeNextJsonConfigResolver` (:43757, :45327-45343), whose relative-name branch treats them as a DIRECTORY
  (`normalizePathForCJSResolution`, :45478-45483, adds a trailing separator when the last part is `.` or `..`). Observed:
  from `app/sub/tsconfig.json`, `".."` probes `app/package.json` then `app/tsconfig.json` and reads `app/tsconfig.json`
  (or, when `app/package.json` has `"tsconfig": "./base.json"`, reads that `base.json`); `"."` from `app/tsconfig.json`
  probes `app/package.json`, `app/tsconfig.json` and refuses on a cycle (itself); `".."` from `app/tsconfig.json` with
  only `/r.json` present finds nothing ("File '..' not found"); a plain `app.json` or `index.json` is not a candidate.
  Item 14a classifies `.` and `..` as package specifiers whose name fails `^...[a-z0-9~-]...`, so malformed. The
  compiler's answer here also depends on `package.json`'s `tsconfig` field, which M3B:643 says is not evaluated.
- O-3. Not a new case, recorded for completeness: a `..` that rises above the project root and comes back
  (`../r/x` from the root) is refused by M3B:632 although the compiler would read inside the project. Unchanged.

## What this erratum does not change

Item 14a's grammar and classification (M3B:620-628), containment (M3B:632), package-specifier candidates (M3B:640-643),
graph identity, bounds, inheritance and the four keys; E1a r4 items 1-8 except that 7.2's "its candidates normalized
(M3B:630-633)" now reads the candidates of statement 1. No price number, no D9 row, no public detail.

## The code that follows it (DISCOVERY-FLAGS-1 stack fix round 1, F-4)

`h/typescript_config.rs` `candidates`: N is normalized once; an empty N is `ExtendsUnresolved`; the second candidate is
`N.json` unless N ends in `.json`. Controls: the pure configuration vectors and gate tests with the inputs of the
table's first five rows, expecting the compiler's file. See `HANDOFF-STACK-FIX-1.md`.
