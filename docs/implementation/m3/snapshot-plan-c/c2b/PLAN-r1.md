# C2b-0 implementation plan r1: the `node_modules` layout (M3-C r8 items 3 and 10; NE §2.4)

**Lead plan, 2026-10-17. Proposed; it needs Codex review.** It plans the layout-only sub-unit of C2b. The prior gating record is `C2B-GATING-r1.md` (this directory). It finds that C2b's context half waits for C2a's manifest-admitted closures, and that the layout needs none. This plan is the first of that record's two unblocking units. **The rest of C2b, C2b-1, is not planned here** (§8).

**Bases:**
- product main `3d1d771` (the v221 lock): C1a1 to C1a4 integrated, including the capture session, the walk with its `SnapshotExtent`, sealing, and the snapshot ledger profile `2^21 / 2^24 / 2^33`;
- the current architecture head, with the C1b plan r3 accepted (`c1b/PLAN-r3.md`) and the C1c plan r2 in review (`c1c/PLAN-r2.md`). This plan depends on C1c-0 as r2 defines it, and is revised if that review changes C1c-0's interface.

**Authority:**
- **The law:** M3-C r8:
  - item 3 step 1 (`PROPOSAL.md`:305): "C2's TypeScript resolver computes `ResolvedNodeModulesLayoutV1` (NE:1399-1420). It reads only installed package manifests, and it observes links with `readlinkat` without following them";
  - item 10's TypeScript list, "the layout (item 3)" (:568);
  - item 1's capture-session rules (:207-226);
  - item 2's descriptor discipline (:271-279);
  - item 6's exclusions (:377-393);
  - the Units table: C2b (:1184); C1c's edge "C1a; C2b's layout" (:1182).
- **The contracts:**
  - NE's `ResolvedNodeModulesLayoutV1` (`docs/v2/contracts/product-v1/native-evidence.md`:1398-1419): `{schemaVersion: 1, entries}`, strictly ascending and unique by `installPath`, one row per installed package directory the resolver may read, `{packageName, packageVersion, installPath, realPath, contentSha256}`. `realPath` equals `installPath` with no link, and is otherwise itself an `installPath` of the layout. `contentSha256` is the raw SHA-256 of that package's manifest bytes;
  - its digest (NE:1490): `nodeModulesLayoutDigest` is the raw SHA-256 of `C(record)`, or null exactly when `nodeModulesInReadSet=false`;
  - its schema (`schemas/sources/native-v2.schema.json`:6971-7016, `$id` `urn:opensip:product-v1:native:evidence-schemas:v2`): `entries` at most 100,000; `packageName` and `packageVersion` 1 to 256 characters; `installPath` and `realPath` are `CanonicalPath` (:981-985, at most 4,096 characters);
  - IE's read-set join (`identity-and-evidence.md`:548-593);
  - SL:266-279 (a pruned tree is never custody-walked).
- **The reference model's consumer side:** `native_evidence_model.v2.py`:2811-2813 (the digest) and :2925-2943 (the retained-layout check, including `realPath ∈ installPaths`). **No reference function derives a layout.** The 16 cases that name one in `native-cases.v2.json` consume it as input. So C2b-0's derivation vectors are lead-authored (§4), and the review should judge them as such.
- **The admission it must agree with:** the evaluator's `inspect_typescript_universe` (`crates/evaluator/src/native_universe.rs`:142, with the layout checks at :235-252), and Run closure's `pruned_fault` (`plan_native.rs`:262-345).
- **The units it builds on:** C1c-0's `CaptureSession::capture_pruned` and the pruned-tree opener (C1c plan r2, LD-C1C-2); the walk's own `SnapshotExtent` (`snapshot_walk.rs`:69-90; LD-C1C-12).

## 1. What C2b-0 delivers

One host function, `resolve_node_modules_layout`, in a new module `crates/host/src/node_modules_layout.rs`. Given:
- the snapshot root and the capture session;
- a TypeScript unit's root directory, project-relative;
- the walk's `SnapshotExtent`;
- the caller's work scope,

it returns either an admitted `ResolvedNodeModulesLayoutV1` together with its raw digest, or a typed refusal (LD-C2B0-8). It is library only, with no production caller: C2b-1, C4a and J2 compose it. **That a layout is a Plan-selected context's own is not C2b-0's to establish** (LD-C2B0-9).

**C2b-0 on its own satisfies the law's C1c edge**, "C1a; C2b's layout" (`PROPOSAL.md`:1182). So C1c-1 integrates after C2b-0, and is not held behind C2a.

## 2. Order and dependencies

| Unit | Depends on | Unblocks |
| --- | --- | --- |
| **C2b-0** (this plan) | C1a (integrated); **C1c-0** (`capture_pruned`, the pruned opener, `read_set_path`): its manifest reads below a pruned anchor need C1c-0's opener (LD-C1C-2, "That is why C1c-0 lands before C2b"). | C1c-1's integration (`PROPOSAL.md`:1182) |
| C2b-1 (not this plan) | C2a, C2b-0 | the TypeScript context and `bind_typescript_universe` |

C2b-0 may be **authored** now, against C1c-0's interface as C1c plan r2 states it. It **integrates** after C1c-0.

## 3. Lead decisions

- **LD-C2B0-1. Where the resolver looks.** Node's resolution reaches an installed package through a `node_modules` directory on the ancestor chain of the importing file, inside the project. The resolver therefore enumerates every `node_modules` directory that:
  - is the unit root's own `node_modules`, or an ancestor's, up to and including the project root's; and
  - lies inside the project root (NE:1404: "the project-relative directory as the resolver walks it"; nothing outside the project root is a snapshot path, IE:548-593).

  It also enumerates every `node_modules` directory reached below an enumerated package (LD-C2B0-3). Directories above the project root are never read.
- **LD-C2B0-2. Which entries are package directories.**
  - **Recognized:** a child `name` of a `node_modules` directory, and a child `@scope/name` of a scoped directory `@scope`.
  - **Excluded:** an entry whose name begins with `.`: `.bin`, `.cache`, and pnpm's `.pnpm` store, which is reached only through links (LD-C2B0-4).
  - **Admitted:** a recognized entry, when it is a directory or a link to one, and it holds a `package.json` regular file. That entry is a candidate row.
  - **No manifest:** a recognized directory without a `package.json` is not a row. Whether it should refuse instead is Q1.
- **LD-C2B0-3. Nesting.** A package directory's own `node_modules`, at `node_modules/a/node_modules/b`, holds nested installs. Each nested package is its own row, and the enclosing row never stands for it (IE:572-577; C1-T12). The resolver enumerates nested `node_modules` iteratively, never recursively, each step charged (LD-C2B0-7). The bound is the schema's 100,000 rows; depth is bounded only by `CanonicalPath`'s 4,096 characters (:981-985), and no other depth bound is invented.
- **LD-C2B0-4. Links are observed, never followed** (`PROPOSAL.md`:305; item 3's "Rejected: reading through `installPath` symlinks").
  - A recognized entry that is a symlink is read with `readlinkat` on the held parent descriptor. Its target is resolved **lexically**, against the link's directory, into a project-relative `CanonicalPath`. That is `realPath`.
  - A target outside the project root, or one that is not a `CanonicalPath` (`..` above the root, an absolute path elsewhere, NUL), refuses as `LayoutLink` (Q2).
  - The target directory is then reached by C1c-0's no-follow opener from the retained root, never through the link. A link whose resolved target is itself a link, or is not a directory, refuses.
  - **`realPath` must itself be an `installPath` of the layout** (NE:1405-1406; the reference check at `native_evidence_model.v2.py`:2940-2943). So a link target becomes a row of its own.
    - For pnpm, `node_modules/foo` links to `node_modules/.pnpm/foo@1/node_modules/foo`, and that directory is a row whose `installPath` and `realPath` are both that path.
    - For a workspace link to a first-party package (`node_modules/x` → `packages/x`), `packages/x` is a row.
  - The rows a link target adds are enumerated in turn (LD-C2B0-3). So pnpm's sibling links under `.pnpm/<id>/node_modules/` are reached, while the `.pnpm` store as a whole is never listed.
- **LD-C2B0-5. The manifest read, and its identity.**
  - Each candidate's `package.json` is captured **once** through the session:
    - below a pruned anchor, by `CaptureSession::capture_pruned` (C1c-0);
    - for a first-party workspace-link target, by the ordinary `capture`, or reused from B2's earlier capture of the same path (item 1, :207-216; :216, "No second read"). It is never read twice, and a changed object refuses `ChangedSinceCapture`.
  - `contentSha256` is the capture's raw SHA-256 (NE:1407-1408).
  - `packageName` and `packageVersion` are the manifest's `name` and `version` strings. The manifest is parsed by the identity crate's JSON reader, within its `MAX_BYTES` of 4 MiB (`crates/identity/src/canonical.rs`:5). Strict JSON is the existing reader's grammar; whether a non-strict manifest should refuse or be omitted is Q3.
  - A missing or non-string `name` or `version`, or one longer than 256 characters (the schema), refuses `LayoutManifest`.
  - LD-C1C-2 sends the parse bound to C2b and introduces no per-manifest cap. C2b-0 adds none either: it reuses the reader's existing 4 MiB.
- **LD-C2B0-6. Exclusions first (LD-C1C-12).**
  - The walk's own `SnapshotExtent` applies before any descent or read: B2's `AdmittedBoundaries` and the validated Config2 `ignorePaths` (`snapshot_walk.rs`:69-90). An excluded `node_modules` directory, package directory or link target is never read and yields no row.
  - C1c-0's `read_set_path` decides VCS and Cargo-output exclusions at every depth (LD-C1C-5). A package directory inside a VCS tree, or inside a Cargo `target` under a package-local Cargo root, is never a row.
  - The layout cannot override any exclusion that item 6 keeps.
- **LD-C2B0-7. Bounded and charged.**
  - Every directory listing, link read, status read, manifest capture and parse is charged to the caller's work scope before it is made, as the bounded walks of C1a1 and D3a-0 do. No listing is collected whole.
  - **Which ledger (lead decision; Q5).** Item 1 assigns B2's reads through the session to the discovery ledger (`PROPOSAL.md`:209), but names no ledger for C2's layout reads (:210). The lead's choice is the **snapshot ledger**, the one the same capture session's walk and sealing use: the layout's captures are retained in the session and become inventory bytes through the read set, so they are part of the sealed snapshot's work. **C2b-0 therefore owns a layout term in `snapshot_ledger_model.py`**, with its vectors and its derivation under r9's fixed caps and the 2× rule, before C2b-0's acceptance, as C1b-1 and C1c-1 own theirs (LD-C1B-6, LD-C1C-8).
  - If the caps do not hold, C2b-0 stops for a law revision rather than raise a cap.
  - Census accounting follows C1b plan r3's LD-C1B-7 and C1c plan r2's LD-C1C-9, per receipt. The model and vector changes alter the **companion snapshot receipt's** bindings. No discovery-closure file changes, so the discovery receipt's delta is empty. The generated-output `--check` commands pass after regeneration, and the stale receipt is recorded separately from public fields. C2b-0 joins whichever batch is open when it integrates, as LD-C1C-9 describes.
- **LD-C2B0-8. Refusals are typed.**
  - `LayoutRefusal {Link, Manifest, Bound, Order, Custody, Io}`:
    - `Bound` is more than 100,000 rows (the schema's `maxItems`);
    - `Order` is a duplicate `installPath`, which cannot happen by construction and is defence in depth.
  - Work exhaustion stays the ledger's `Budget` failure.
  - The public projection is J2's, as LD-C1B-8 and LD-C1C-11 have it.
  - **What the host does with a refused layout,** whether a refused `Bound` means `nodeModulesInReadSet=false` (item 3's last bullet, `PROPOSAL.md`:311) or a refused request, is C4a's and J2's composition (Q4). C2b-0 never silently drops rows to fit.
- **LD-C2B0-9. Admission and the composition precondition.**
  - The result is admitted against `$defs/ResolvedNodeModulesLayoutV1` through the embedded registry, as framework recognition rows are (B2-d2), with rows sorted by `installPath` bytes. Its digest is the raw SHA-256 of the canonical encoding (NE:1490; `native_evidence_model.v2.py`:2811-2813).
  - Before returning, C2b-0 runs the same retained-layout check the evaluator applies at Run closure (`native_universe.rs`:235-252): every `realPath` is an `installPath`. So mint and Run closure agree (item 10, :562).
  - That the layout is a Plan-selected context's own, and that its unit root and extent come from the same root, are **composition preconditions** bound by C2b-1, C4a and J2, as LD-C1C-1 states.
- **LD-C2B0-10. The no-layout case.** When no `node_modules` directory exists on the unit's chain, C2b-0 returns `None`, not an empty-entries layout. NE makes the digest null exactly when `nodeModulesInReadSet=false` (NE:1490), and an empty layout would commit `nodeModulesInReadSet=true` to nothing. The context then carries a null digest (C2b-1).

## 4. Controls

The vectors are lead-authored synthetic trees, since no reference derivation exists. Each states its expected layout by hand.
- **npm, flat:** two top-level packages, one scoped (`@s/b`). Rows are sorted by `installPath`, `realPath` equals `installPath`, and the digests are the manifests' digests (C1-T12's npm half).
- **npm, nested:** `node_modules/a/node_modules/b` is its own row (C1-T12's nested half).
- **pnpm:** a top-level link into `.pnpm/<id>/node_modules/<pkg>`. The target is its own row. A sibling link inside `.pnpm/<id>/node_modules/` is reached. No other `.pnpm` content is listed. Every `realPath` is an `installPath` (C1-T12's pnpm half).
- **A workspace link** to a first-party `packages/x`. That row reuses B2's capture with no second read (the C1A-T1 spy).
- **Ancestor chain:** a unit at `apps/web` sees `apps/web/node_modules` and the root's `node_modules`, and never a directory outside the project.
- **Links, refused:** a link outside the project root; a link through `..` above the root; a link to a link; a link to a file.
- **Manifests, refused:** a missing `name`, a non-string `version`, a 257-character `name`, and a manifest over 4 MiB. A recognized directory without `package.json` is not a row (or refuses, per Q1).
- **Exclusions:** an ignored package (`ignorePaths`), a package under an admitted boundary, a package inside a `.git` tree, and one inside a package-local Cargo `target`. None is a row, and none is read (LD-C2B0-6).
- **Descriptor discipline:** an inode swap between status and open refuses, and a change during a manifest read refuses (C1c-0's opener).
- **Bounds:** 100,000 rows admit and 100,001 refuse `Bound`. Exhaustion is `Budget`. The charge equals the recorded calls' price.
- **Agreement:** each produced layout passes the evaluator's `inspect_typescript_universe` layout checks, and its digest equals `C(record)`'s raw SHA-256 recomputed independently.
- **No layout:** a unit with no `node_modules` on its chain returns `None`.
- **Model:** `snapshot_ledger_model.py --check` with the layout term, and the r9 cap derivation.

## 5. Mutations

Each must fail the controls:
- a link followed;
- a nested package merged into its enclosing row;
- a `.`-prefixed entry listed;
- an `ignorePaths` exclusion skipped;
- a manifest read twice;
- `realPath` taken from the link text unresolved;
- the row bound off by one;
- a listing step uncharged;
- an empty layout returned instead of `None`.

## 6. Checks

The lane covers:
- the host and security suites at base and candidate;
- warning-denied all-targets Clippy, and rustfmt;
- the focused layout tests;
- the snapshot model `--check`, and the census generated-output `--check` commands passing after regeneration, with the receipt-specific stale record;
- the environment exceptions, the operability source census with its mint audit, and verify_design;
- the mutations.

## 7. Open questions

- **Q1.** Should a recognized package directory without a `package.json` refuse the layout instead of yielding no row? Node can resolve such a directory through `index.js`. Without a row, a provider read there faults as `node-modules-outside-read-set` (NE:2953), and that is the safe failure. **Recommendation:** no row.
- **Q2.** Is a link whose lexical target is outside the project root a refusal (recommended), or no row?
- **Q3.** Should a `package.json` that is not strict JSON refuse `LayoutManifest` (recommended, since the reader has one grammar), or yield no row?
- **Q4.** Is the host's response to a refused layout C4a's and J2's composition, as LD-C2B0-8 states, given item 3's `nodeModulesInReadSet=false` fallback (`PROPOSAL.md`:311)?
- **Q5.** Is the snapshot ledger the right ledger for the layout's reads (LD-C2B0-7), given that item 1 names the discovery ledger only for B2's reads (`PROPOSAL.md`:209-210)? The alternative is a separate resolution ledger, which leaves those captures outside r9's derivation even though they become inventory bytes.

## 8. Not delivered

- **C2b-1:** the TypeScript context (`TypeScriptNativeContextV2`), the honored and stripped options, `libSelection` and the stdlib join, the lockfile identity, and `bind_typescript_universe`. It waits for C2a (`C2B-GATING-r1.md`).
- The read set itself (C1c-1), and the suffix table (C2's semantics, reviewed with F, `PROPOSAL.md`:310).
- Any production caller.

## 9. Not claimed

- No context, universe, Plan selection or qualification.
- No reference-derived oracle for the layout (§Authority).
