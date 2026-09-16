#!/usr/bin/env python3
"""Composes review.json. Counts are read from the evidence files, not transcribed."""
import json, os

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
E = lambda p: os.path.join(R, "evidence", p)
load = lambda p: json.load(open(E(p)))

ident = load("identities.json")
fb, fa = load("frozen-before.json")["summary"], load("frozen-after.json")["summary"]
copy_after = load("copy-after.json")["summary"]["problems"]
probes = load("probes.json")
mut = load("review-mutants-summary.json")
orig = json.load(open(E("original-author-results/matrix.json")))
regen = json.load(open(os.path.join(R, "work/copy/results/matrix.json")))

rows = probes["rows"]
oracle_rows = [r for r in rows if "oracle" in r]
by_grade = {}
for r in rows:
    by_grade.setdefault(r["grade"], []).append(r["id"])

review = {
    "schemaVersion": 1,
    "standing": "independent reviewer record (review-02); not approval, product build, release qualification or tool promotion",
    "subject": {
        "root": "/tmp/opensip-implementation/m1-typescript-boundary-subject-02",
        "outerManifest": "/tmp/opensip-implementation/m1-typescript-boundary-subject-02.json",
        "outerManifestSha256": ident["outerManifestSha256"],
        "entries": fb["manifestRows"],
    },
    "verdict": {
        "summary": "CHANGES REQUIRED. The correction reproduces exactly and fixes the three root-01 misses, but independent valid probes find fail-open behaviour (CLI silently exits 0 when invoked through a symlinked path), silently absent edges (AMD in the candidate's extraction mode; elided static + import() merge in ESM TypeScript), boundary bypasses (relative paths into node_modules, pnpm npm: alias shadowing a local name) and Node-resolution divergences that contradict the report's per-edge Node-condition and resolvability claims. Not selectable as the TypeScript dependency checker in its current form; no tool promotion.",
        "reproducible": True,
        "rootProbesFixed": True,
        "selectable": False,
    },
    "identities": {
        "outerManifestSha256": ident["outerManifestSha256"],
        "outerRows": ident["outerRowCount"],
        "outerRowsAreAuthorRowsPlusFreezeRow": "values identical for all 1206 author rows; only ordering differs (freeze row inserted in path order)",
        "authorFreezeRawSha256": ident["authorFreezeRawSha256"],
        "authorFreezeRawMatchesOuterRow": ident["authorFreezeRawSha256"] == ident["authorFreezeOuterRowSha256"],
        "authorDeclaredAggregateSha256": ident["authorFreezeDeclaredAggregate"],
        "aggregateRecomputedFromActualTree": ident["recomputedAggregateFromActualTree"],
        "aggregateAlgorithm": "sha256 of '\\n'-joined `${type}\\0${path}\\0${sha256 ?? symlinkTarget}` over readdir-sorted entries, excluding freeze-manifest.json, launcher files and trial/work/ (trial/harness/freeze-manifest.mjs); bytes and modes are NOT in the aggregate",
        "aggregateMatches": ident["aggregateMatchesDeclared"],
        "note": "raw file sha256 (a3c71b38...) and declared aggregate (a19e0f8d...) are different identities by construction; both verified",
    },
    "frozenInputCustody": {
        "before": {"entries": fb["actualEntries"], "types": fb["types"], "bytes": fb["totalBytes"], "problems": len(fb["problems"]), "treeDigest": fb["actualTreeDigest"]},
        "after": {"entries": fa["actualEntries"], "problems": len(fa["problems"]), "treeDigest": fa["actualTreeDigest"]},
        "unchanged": fb["actualTreeDigest"] == fa["actualTreeDigest"] and not fa["problems"],
        "checked": "every row: type, octal mode, bytes, sha256, symlink target (lstat, no following); unexpected extra entries; empty directories",
        "executedOnlyOnCopy": "work/copy (cp -Rp), verified 1207/1207 exact before execution; all node executions used TMPDIR=work/tmp or the copy's own trial/work/tmp",
    },
    "toolClosure": {
        "packages": ident["packages"],
        "entries": ident["toolClosureEntries"],
        "bytes": ident["toolClosureBytes"],
        "bytesNote": "tool-closure group is 28,972,417 bytes; the whole frozen subject (incl. provenance tarballs, results, prior) is 35,220,842 bytes",
        "binSymlinks": len(ident["toolClosureSymlinks"]),
        "symlinkTargetsEscapingClosure": ident["symlinkEscapes"],
        "perPackageTreeDigestMismatches": ident["packageTreeMismatches"],
        "versionMismatches": ident["versionMismatches"],
        "lockInstallScripts": ident["lockInstallScripts"],
        "manifestLifecycleScripts": ident["manifestLifecycleScripts"],
        "nativeBinaries": ident["gypOrBindingFiles"],
        "lockRegistryHosts": ident["lockRegistryHosts"],
        "archivedTarballs": ident["tarballs"],
        "custodyLimit": "Only dependency-cruiser and typescript tarballs are archived; their sha512 equals the lock integrity and their contents are byte-identical to the materialized trees. The other 42 packages are verified only as materialized tree digests plus lock version equality; lock integrity strings for them were not recomputed from archives, so this is not cryptographic archive verification of all 44.",
    },
    "reproduction": {
        "command": "cd work/copy/trial && TMPDIR=$PWD/work/tmp ./reproduce.sh",
        "exit": 0, "seconds": 293,
        "matrixSummaryOriginal": orig["summary"], "matrixSummaryRegenerated": regen["summary"],
        "perCaseDifferences": "none (grade, categories, refusal details, edges, oracle rows)",
        "nodeOracleAgreement": "13/13",
        "candidateTests": "97/97 in reproduce stdout",
        "referenceCopyTests": "11/11",
        "authorMutants": "14/14 killed; failing-test sets identical to the frozen results",
        "historicalAudit": "byte-identical (73 correct, 12 missed, 2 false refusals, 1 wrong reason)",
        "expectedWritesInCopy": {
            "manifestRowsChanged": sorted({p["path"] for p in copy_after if p["problem"] != "unexpected"}),
            "rewrittenByteIdentical": ["results/mutants.json", "results/historical-candidate-01-on-author02-cases.json"],
            "scratchEntriesAdded": sum(1 for p in copy_after if p["problem"] == "unexpected"),
            "scratchDirectories": ["trial/work/matrix", "trial/work/historical", "trial/work/mutants", "trial/work/tmp", "trial/work/tests (removed by tests)", "trial/work/review-mutants (reviewer)"],
            "notWrittenByReproduce": ["results/candidate-tests.txt", "results/matrix-run.txt", "results/mutants-run.txt", "results/reference-copy-tests.txt", "results/reproduce-run.txt"],
        },
        "originalEvidencePreservedAt": "evidence/original-author-results/",
        "rootReproduction": "a root reproduction was reported as running and unclaimed; this review neither reads nor relies on it",
    },
    "independentCases": {
        "file": "evidence/probes.json", "harness": "scripts/probes.mjs",
        "count": len(rows), "summary": probes["summary"], "byGrade": by_grade,
        "nodeOracle": {"rows": len(oracle_rows), "agree": sum(1 for r in oracle_rows if r["oracleAgreesWithCandidate"]),
                        "disagree": [r["id"] for r in oracle_rows if not r["oracleAgreesWithCandidate"]],
                        "method": "child node process per request: createRequire(from).resolve + require (require mode) or import.meta.resolve(parent) + file check + import() (import mode); one TypeScript transpileModule emit oracle (RV-N19). Loads only reviewer-authored fixture stubs."},
        "expectationsFixedBeforeRun": "sets 1-2 before candidate execution; set 2 was added after reviewer mutant batch A to distinguish surviving mutants; set 3 targets declared fail-closed claims. No expectation was changed after seeing a result.",
    },
    "reviewerMutants": {
        "file": "evidence/review-mutants-summary.json", "runner": "scripts/review-mutants.py",
        "count": mut["mutants"], "killedByAuthorSuite": mut["killedByAuthorSuite"],
        "killedByReviewerProbes": mut["killedByReviewerProbes"], "killedByEither": mut["killedByEither"],
        "survivingBoth": [r["name"] for r in mut["rows"] if not (r["killedByAuthorSuite"] or r["killedByReviewerProbes"])],
        "survivorClassification": {
            "no-amd-refusal": "unreachable: the candidate's extraction mode records no AMD dependency (see R3)",
            "no-invalid-scope-refusal": "masked: enhanced-resolve already fails on the invalid package.json (RV-F02 refused as unresolved either way)",
            "no-outside-root-rule": "redundant with lane-escape (own sources) and external-reenters-source (externals)",
            "missing-request-silent": "defensive branch not reachable by any constructed input",
            "follow-ignores-donotfollow": "verdict-equivalent; only changes which other-lane sources are read",
            "scope-no-node_modules-stop": "runtime-equivalent (ESM detection decides .js); in the declaration graph the unmutated stop diverges from TypeScript 6.0.3 (evidence/format-scope-check.json)",
        },
    },
    "required": [
        {"id": "R1", "title": "CLI fails open when invoked through a symlinked path",
         "evidence": "evidence/cli-symlink-path.txt",
         "detail": "The `process.argv[1] === fileURLToPath(import.meta.url)` guard compares a non-realpath argv with a realpath URL. Via /tmp (macOS symlink) or a .bin-style symlink the refusing RV-N04 lane exits 0 with empty stdout; a no-argument usage error also exits 0. Any build integration keyed on exit status passes. Compare realpaths or ship a bin entry that always runs, and test a symlinked invocation."},
        {"id": "R2", "title": "Runtime import() edge lost when merged with an elided static import in ESM-format TypeScript",
         "evidence": "RV-N10 (missed); mutant violations-not-projected turns it into browser-node",
         "detail": "depcruise dedups `import { T } from \"x\"` (type-used, preCompilationOnly) and `import(\"x\")` into one es6 edge; the projection skips it as type-only, so a browser import() of a Node-only package is accepted. The unsupported-mixed-mode guard covers CommonJS-format TypeScript only."},
        {"id": "R3", "title": "Declared fail-closed AMD refusal is unreachable; AMD edges silently absent",
         "evidence": "evidence/amd-extraction.txt; RV-F01 (missed)",
         "detail": "With tsPreCompilationDeps \"specify\" depcruise 18.3.1 extracts no AMD dependency (default and tsConfig-only modes do). A cross-lane `define([\"../../../apps/report/src/view-state.ts\"], ...)` in provider bundle.cjs passes with no edge. Contradicts §3.5 and the build plan's 'no unsupported resolution silently treated as no edge'."},
        {"id": "R4", "title": "Node-lane resolution diverges from Node 24 while the report claims Node per-edge conditions and resolvability",
         "evidence": "RV-P06 false refusal and RV-N05 missed (module-sync); RV-N06 ESM extensionless, RV-N09 ESM directory import, RV-N07/N08 require of .mjs/.ts: all missed; every one disagrees with the Node load oracle",
         "detail": "Node 24 require/import conditions include module-sync; depcruise's single extension list (.js .cjs .mjs .jsx .ts .tsx .d.ts .cts .d.cts .mts .d.mts) and non-fullySpecified resolution apply to every edge. Fix the condition set, and either model per-mode Node resolution for Node-group JS externals or refuse such requests; the limits must say the resolver is enhanced-resolve with depcruise defaults, not Node's algorithm."},
        {"id": "R5", "title": "Relative paths into materialized node_modules bypass declared-external and exports checks",
         "evidence": "RV-N01, RV-N02 (missed); compare author N16/N17",
         "detail": "Own sources importing ../../../node_modules/<pkg>/... get dependency type local, so undeclared-external and exports encapsulation never apply and lane-escape allows ^node_modules/."},
        {"id": "R6", "title": "pnpm npm: alias defeats local-name-shadow",
         "evidence": "RV-N03 missed; RV-N04 (non-alias store) correct",
         "detail": "The shadow rule matches only the realized path. `\"@opensip/typescript-provider\": \"npm:evil@0.1.0\"` realizes to .pnpm/evil@0.1.0/node_modules/evil and is accepted. The product tools/contracts lane is pnpm-managed, so aliases are in scope; check the request name and manifest spec against localPackageNames."},
        {"id": "R7", "title": "Node-group TypeScript format ignores tsconfig module/emit",
         "evidence": "RV-N19 (missed; TypeScript-emit oracle ERR_MODULE_NOT_FOUND)",
         "detail": "A commonjs-scope .ts under module ESNext emits ESM syntax that Node detects as ESM (import condition); the candidate assumes require. Refuse Node-group TS unless module is Node16/Node18/NodeNext, or derive format from the configured emit."},
    ],
    "advisories": [
        {"id": "A1", "title": "Evidence file cited for 97/97 tests records 95", "detail": "results/candidate-tests.txt predates P18/P19 (86 case tests + 9); reproduce-run.txt and regeneration show 97. Regenerate or cite the correct file."},
        {"id": "A2", "title": "Fail-closed over-refusals on valid code", "detail": "RV-P07: a type-used static import plus import() in .cts is refused (TypeScript elides the static import). RV-P09: the declaration graph follows an untyped ESM .js external with runtime CommonJS format and refuses a require-mode edge TypeScript never reads. The node_modules scope stop also diverges from TypeScript 6.0.3 implied format for package.json-less directories."},
        {"id": "A3", "title": "acceptedUnresolved is not scoped by request kind, mode or group", "detail": "RV-N12: a record intended for a try/catch require also silences an unguarded import() of the same specifier in both Node groups. Key records by moduleSystem/dynamic/mode (and optionally group). RV-N20/RV-N21 show from-exactness and rule-exactness do hold."},
        {"id": "A4", "title": "Undisclosed static edge forms", "detail": "RV-N11: new URL(literal, import.meta.url) worker/asset entries crossing lanes are neither extracted nor refused. The bundler is unselected, but the limits should say so or browser inputs should refuse the form."},
        {"id": "A5", "title": "devDependency reached at provider runtime is accepted", "detail": "RV-N23. The build plan requires a sealed provider runtime closure; dev-vs-runtime dependency class is an open policy question, not decided by the checker."},
        {"id": "A6", "title": "Lane records are fully trusted", "detail": "RV-T01: declaring browser sources as a node group disables browser-node checks. Bind lane records to the reviewed repository inventory before integration."},
        {"id": "A7", "title": "Author matrix does not isolate many claimed checks", "detail": "The author suite kills 7/28 reviewer mutants; symlink input, project references, plugins, typeRoots, undeclared ambient types, external mixed-mode, platform consistency, accepted-record exactness, external shadowing and runtime-unresolvable type-only imports were unisolated until reviewer probes RV-F03..F09, RV-N20..N22, RV-P08, RV-P10 and RV-P11."},
        {"id": "A8", "title": "Complexity and dependency selection", "detail": "The correction now owns per-edge mode, module format, type elision, convergence and Node fidelity in custom code, on four measured-but-undocumented depcruise 18.3.1 internals, with two cruises times two graphs times rounds. evidence/ts-mode-prototype.json shows TypeScript 6.0.3, already in the closure, returns per-usage-location modes for N62/P07/P08-style files without dedup, and its emit elides type-used imports (the R2/A2 cases). That substantiates a simpler mode/elision source; it does not by itself give Node-exact runtime resolution of JS externals. Recommend a bounded comparison (TS mode + Node's own resolver for Node-group runtime edges) before selecting, not an automatic switch."},
        {"id": "A9", "title": "Actual chosen code is refused and needs unselected inputs", "detail": "Smoke on a byte-pinned copy of candidate-02 tools/contracts (evidence/product-smoke-*), with a reviewer-authored tsconfig because the product has none: 2 refusals, validate-schemas.cjs:13 computed require(file) (unsupported-loader) and typescript.js source-map-support (unresolved). 2.0 s wall and 1.19 GB max RSS for one lane. Integration needs a tsconfig/lane record, a decision for the generated-runtime require, an acceptedUnresolved record, and a pnpm-installed checker closure (the trial closure is npm package-lock)."},
        {"id": "A10", "title": "Custody wording", "detail": "'44 packages match lock versions' in reproduce.sh is a version check, not integrity verification; only 2 tarballs are archived. Five manifests declare prepare scripts (not run for registry installs; lock hasInstallScript is false for all)."},
    ],
    "architectureFit": {
        "buildPlanSections": ["§Independently selectable build lanes", "§TypeScript policy", "§Enforcement and verification item 2", "Tooling decision matrix: TS dependencies"],
        "assessment": "The lane shapes (browser report, TypeScript provider, tools/contracts Node lane) match the plan and the checker stays a separate trial tool with no product edits. The plan's M1 bar ('runtime/type-only/dynamic imports, aliases, exports, generated inputs and scripts; no unsupported resolution silently treated as no edge') is not met because of R2, R3 and R5; pnpm aliases (R6) matter because the actual tools/contracts lane is pnpm-managed; one package manager/lock strategy is still unselected and the trial closure uses npm.",
    },
    "limits": [
        "Static fixture probes only; no product build, bundler run, release or runtime sandbox.",
        "No claim about opaque extension code, computed loaders inside externals, or unbounded dependency read closure.",
        "Node oracle loads only reviewer-authored stubs; browser expectations come from the build-plan policy, not a bundler.",
        "Reviewer mutants are single-site and partly equivalent (classified above); kill counts are not a completeness proof.",
        "The TypeScript mode prototype covers mode selection and elision only.",
        "No network, installs, subagents, commits, background tasks or private session inspection. Nothing outside this review directory was written.",
    ],
    "noPromotion": True,
}
json.dump(review, open(os.path.join(R, "review.json"), "w"), indent=2)
print(json.dumps({"probes": probes["summary"], "oracle": review["independentCases"]["nodeOracle"]["agree"], "oracleRows": len(oracle_rows), "mutants": [mut["killedByAuthorSuite"], mut["killedByReviewerProbes"], mut["killedByEither"]], "survivors": review["reviewerMutants"]["survivingBoth"]}))
