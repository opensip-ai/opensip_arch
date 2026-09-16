#!/usr/bin/env python3
"""Reviewer-authored single-site mutants (independent of the author's 14).
Each mutant copy lives under the MUTABLE copy's trial/work/review-mutants/ so the
copied tool closure resolves. Each mutant is run against (a) the author's own
candidate test suite and (b) the reviewer probes (differential against the
unmutated baseline probe output).

usage: review-mutants.py [NAME_REGEX] [--jobs N]
"""
import concurrent.futures, json, os, re, subprocess, sys, time

REVIEW = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRIAL = os.path.join(REVIEW, "work/copy/trial")
CAND = os.path.join(TRIAL, "candidate")
WORK = os.path.join(TRIAL, "work/review-mutants")
OUT = os.path.join(REVIEW, "evidence/review-mutants")
NODE = "/Users/sb/.nvm/versions/node/v24.16.0/bin/node"
ENV = {**os.environ, "TMPDIR": os.path.join(REVIEW, "work/tmp")}

C, S = "check-lane.mjs", "supplement.mjs"
MUTANTS = {
    "violations-not-projected": (C, r"violations[mode].filter(v => onProjection.has(`${v.from}\0${v.to}\0${mode}`))", r"violations[mode]"),
    "no-outside-root-rule": (C, "    { name: 'outside-materialized-root', severity: 'error', from: {}, to: { path: '^\\\\.\\\\./', couldNotResolve: false } },\n", ""),
    "shadow-rule-own-only": (C, "{ name: 'external-shadows-local-package', severity: 'error', from: {},", "{ name: 'external-shadows-local-package', severity: 'error', from: { path: ownSource },"),
    "type-only-without-precompilation": (C, "const isTypeOnly = dep => dep.preCompilationOnly === true || TYPE_ONLY_TYPES.some(t => has(dep, t));", "const isTypeOnly = dep => TYPE_ONLY_TYPES.some(t => has(dep, t));"),
    "scope-no-node_modules-stop": (C, "      if (path.posix.basename(dir) === 'node_modules') scope = 'commonjs';\n      else if", "      if (false) scope = 'commonjs';\n      else if"),
    "no-js-esm-detection": (C, "    if (esm) return 'module';\n", ""),
    "browser-static-follows-format": (C, "  if (platform === 'browser') return { mode: 'import' };\n", ""),
    "missing-request-silent": (C, "if (!resolved) { unsupported.push({ from: source, module: dep.module, reason: 'request missing from the ' + choice.mode + ' cruise' }); continue; }", "if (!resolved) continue;"),
    "follow-ignores-donotfollow": (C, "if (resolved.followable && !resolved.matchesDoNotFollow && !resolved.couldNotResolve && !resolved.coreModule) queue.push", "if (!resolved.couldNotResolve && !resolved.coreModule) queue.push"),
    "max-rounds-1": (C, "const MAX_ROUNDS = 8;", "const MAX_ROUNDS = 1;"),
    "accepted-any-rule": (C, "r.rule === 'unresolvable' && a.from === r.from", "a.from === r.from"),
    "accepted-ignores-from": (C, "a.from === r.from && a.module === r.to", "a.module === r.to"),
    "reentry-allows-own-lane": (C, "to: { pathNot: materialized,", "to: { pathNot: `^(?:node_modules/|${own})`,"),
    "undeclared-external-npm-no-pkg-only": (C, "dependencyTypes: ['npm-no-pkg', 'npm-unknown', 'undetermined']", "dependencyTypes: ['npm-no-pkg']"),
    "no-invalid-scope-refusal": (C, "if (format === 'invalid') return { unsupported: 'nearest package.json is not valid JSON' };", "if (false) return { unsupported: 'x' };"),
    "no-amd-refusal": (C, "  if (dep.moduleSystem === 'amd') return { unsupported: 'AMD module requests are not selected' };\n", ""),
    "no-platform-consistency": (C, "if (lane.browserRoots.some(root => file.startsWith(root)) !== (group.platform === 'browser')) fail(", "if (false) fail("),
    "type-graph-no-types-condition": (C, "      conditionNames: [...(graph === 'type' ? ['types'] : []), ...group.conditions, mode, 'default'],", "      conditionNames: [...group.conditions, mode, 'default'],"),
    "no-symlink-input-check": (S, "      if (stat.isSymbolicLink()) { findings.push({ category: 'symlink', message: 'symlink in declared input ' + file }); break; }\n", ""),
    "no-project-references": (S, "  if (parsed.projectReferences?.length) findings.push(", "  if (false) findings.push("),
    "no-compiler-plugins": (S, "  if (parsed.options.plugins?.length) findings.push(", "  if (false) findings.push("),
    "no-external-mixed-mode": (S, ", ...mixedModeFindings(program, root, externals, scopeOf));", ");"),
    "no-typeRoots": (S, "  if (typeRoots !== undefined) findings.push(", "  if (false) findings.push("),
    "scannable-mjs-only": (S, "const SCANNABLE = /\\.(?:[cm]?[jt]sx?)$/;", "const SCANNABLE = /\\.mjs$/;"),
    "no-config-include": (S, "for (const file of parsed.fileNames) if (!inputs.has(path.resolve(file))) findings.push(", "for (const file of parsed.fileNames) if (false) findings.push("),
    "no-getbuiltin-guard": (S, "      } else if (node.text === 'getBuiltinModule') {", "      } else if (false) {"),
    "no-config-owner": (S, "    if (!physical.split(path.sep).includes('node_modules') && (relative.startsWith('..') || path.isAbsolute(relative))) {", "    if (false) {"),
    "ambient-undeclared-allowed": (S, "    if (!declared.has(packageName) && !declared.has(name)) findings.push(", "    if (false) findings.push("),
}

def build(name):
    file, site, repl = MUTANTS[name]
    d = os.path.join(WORK, name)
    os.makedirs(d, exist_ok=True)
    for f in (C, S):
        text = open(os.path.join(CAND, f)).read()
        if f == file:
            n = text.count(site)
            if n != 1:
                raise SystemExit(f"{name}: site occurs {n} times in {file}")
            text = text.replace(site, repl)
        open(os.path.join(d, f), "w").write(text)
    return os.path.join(d, C)

def run(name):
    checker = build(name)
    t0 = time.time()
    tap = subprocess.run([NODE, "--test", "--test-reporter=tap", os.path.join(CAND, "test-check-lane.mjs")], cwd=TRIAL,
                         env={**ENV, "OPENSIP_TRIAL_CHECKER": checker}, capture_output=True, text=True)
    failing = re.findall(r"^not ok \d+ - (.*)$", tap.stdout, re.M)
    probe_out = os.path.join(OUT, f"probes-{name}.json")
    pr = subprocess.run([NODE, os.path.join(REVIEW, "scripts/probes.mjs"), "--checker", checker, "--out", probe_out, "--no-oracle"],
                        cwd=REVIEW, env=ENV, capture_output=True, text=True)
    base = {r["id"]: r for r in json.load(open(os.path.join(REVIEW, "evidence/probes.json")))["rows"]}
    changed = []
    if pr.returncode == 0:
        for r in json.load(open(probe_out))["rows"]:
            b = base[r["id"]]
            if (r["passed"], sorted(r["categories"])) != (b["passed"], sorted(b["categories"])):
                changed.append({"id": r["id"], "baseline": [b["passed"], b["categories"]], "mutant": [r["passed"], r["categories"]]})
    else:
        changed.append({"probeHarnessError": pr.stderr[-400:]})
    return {"name": name, "file": MUTANTS[name][0], "authorSuiteExit": tap.returncode, "authorSuiteFailing": failing,
            "killedByAuthorSuite": tap.returncode != 0 and bool(failing), "probeDifferences": changed,
            "killedByReviewerProbes": bool(changed), "seconds": round(time.time() - t0)}

if __name__ == "__main__":
    args = sys.argv[1:]
    jobs = int(args[args.index("--jobs") + 1]) if "--jobs" in args else 4
    pat = next((a for a in args if not a.startswith("--") and not a.isdigit()), None)
    names = [n for n in MUTANTS if not pat or re.search(pat, n)]
    os.makedirs(OUT, exist_ok=True)
    for n in names:
        build(n)  # validate every site before spending time
    with concurrent.futures.ThreadPoolExecutor(jobs) as ex:
        for res in ex.map(run, names):
            json.dump(res, open(os.path.join(OUT, res["name"] + ".json"), "w"), indent=1)
            print(f"{res['name']:40} author:{'killed' if res['killedByAuthorSuite'] else 'SURVIVED'}({len(res['authorSuiteFailing'])}) "
                  f"probes:{'killed' if res['killedByReviewerProbes'] else 'survived'}({len(res['probeDifferences'])}) {res['seconds']}s", flush=True)
