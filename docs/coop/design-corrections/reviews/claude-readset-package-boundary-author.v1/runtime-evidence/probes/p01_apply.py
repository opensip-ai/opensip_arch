"""p01: explicit nested package custody (resolves readset-nesting-review ADV-1) by exact counted replacements in this
runtime's work/source. Every owned file must still equal its baseline bytes (receipts/p00-copy.json) and every anchor
must occur exactly once, or nothing is written. Python edits are compiled before writing.
Output: receipts/p01-apply.json.
"""
import hashlib, json, sys
from pathlib import Path

BASE = Path('/tmp/opensip-design-corrections/claude-readset-package-boundary-author.v1')
W = BASE / 'work' / 'source'
MODEL = 'docs/coop/design-corrections/foundation/identity-model.v3.py'
CHECK = 'docs/coop/design-corrections/foundation/check-native-consumer24-corrections.v1.py'
IDN = 'docs/v2/contracts/product-v1/identity-and-evidence.md'
SEC = 'docs/v2/contracts/product-v1/security-and-lifecycle.md'

EDITS = [
    # ---------------------------------------------------------------- identity model: docstring
    (MODEL,
     "    package directory (`installPath` or `realPath`) of a retained ResolvedNodeModulesLayoutV1 whose context committed\n"
     "    nodeModulesInReadSet; a VCS-tree or Cargo build-output row is never a read input of any published universe.\n"
     "    Package-directory granularity is all the retained layout records. That no OTHER file of a listed package was\n"
     "    read, or that the host walked every first-party file, is a host TCB observation a bytes-only replay cannot\n"
     "    establish, and this join does not claim it.\"\"\"\n",
     "    package directory (`installPath` or `realPath`) of a retained ResolvedNodeModulesLayoutV1 whose context committed\n"
     "    nodeModulesInReadSet, with no further exact `node_modules` segment between that listed directory and the file:\n"
     "    explicit nested package custody, so a nested installed package is authorized only by its own row and never\n"
     "    through an enclosing listed directory. A VCS-tree or Cargo build-output row is never a read input of any\n"
     "    published universe, and the VCS exclusion is checked at every depth before any package authorization. Listed\n"
     "    directories are arbitrary admitted CanonicalPaths compared by exact segment prefix; no package root is parsed.\n"
     "    Replay decides every INVENTORIED row against the listed directories, nested boundaries included. That no other\n"
     "    file was read, that no read file is missing from the inventory, or that the host walked every first-party file,\n"
     "    is a host TCB observation a bytes-only replay cannot establish, and this join does not claim it.\"\"\"\n"),
    # ---------------------------------------------------------------- identity model: law
    (MODEL,
     "        if hit[1]=='dependency-tree' and any(path.startswith(package+'/') for package in packages):continue\n"
     "        faults.append(path)\n"
     "    return sorted(faults,key=lambda p:p.encode('utf-8'))\n",
     "        if hit[1]=='dependency-tree' and any(listed_package_authorizes_read(package,path,DD.DEPENDENCY_TREE_SEGMENTS)\n"
     "                                             for package in packages):continue\n"
     "        faults.append(path)\n"
     "    return sorted(faults,key=lambda p:p.encode('utf-8'))\n"
     "\n"
     "def listed_package_authorizes_read(package,path,dependency_segments):\n"
     "    \"\"\"Explicit nested package custody (identity section 3, consumer24 A4). A listed installPath or realPath\n"
     "    authorizes a read file below it only while the relative suffix below that exact directory has no further exact\n"
     "    dependency-tree segment: a nested installed package needs its own retained row whose directory lies below that\n"
     "    boundary. The listed directory is an arbitrary admitted CanonicalPath (a package-manager store directory or a\n"
     "    workspace link included); nothing is parsed from its spelling, and its own segments may contain node_modules.\"\"\"\n"
     "    if not path.startswith(package+'/'):return False\n"
     "    return not any(segment in dependency_segments for segment in path[len(package)+1:].split('/'))\n"),
    # ---------------------------------------------------------------- identity-and-evidence section 3
    (IDN,
     "build-output row is never a read input of any published universe. A dependency\n"
     "package's read allowance never overrides a VCS-tree exclusion deeper in that path;\n"
     "the VCS exclusion uses exact segments at every depth. Either violation refuses\n"
     "`SNAPSHOT_PRUNED_TREE_NOT_A_READ`. **What replay does not prove.** The\n"
     "custody walk and the read set are host TCB observations retained with the Run.\n"
     "Bytes-only replay re-checks every retained digest, and this join, at package-directory\n"
     "granularity. It cannot prove that the host walked every first-party file, that it\n"
     "read no other file of a listed package, or that every package it read is listed:\n"
     "those are properties of an unobserved host process, not of the retained bytes.\n",
     "build-output row is never a read input of any published universe. A dependency\n"
     "package's read allowance never overrides a VCS-tree exclusion deeper in that path;\n"
     "the VCS exclusion uses exact segments at every depth. **Nested packages have\n"
     "explicit custody.** A listed directory authorizes a read file below it only while\n"
     "the path suffix below that exact directory has no further exact `node_modules`\n"
     "segment. A nested installed package (for example\n"
     "`node_modules/left-pad/node_modules/evil`) is its own installed package directory\n"
     "and needs its own layout row; an enclosing listed directory never authorizes it.\n"
     "Listed directories are admitted `CanonicalPath` prefixes compared by exact segment,\n"
     "not package roots parsed from a path, so a package-manager store or workspace-link\n"
     "`realPath` authorizes its ordinary descendants, and a lookalike segment such as\n"
     "`node_modules-like` is no boundary. A row outside every pruned tree stays with the\n"
     "first-party custody walk even when a listed `realPath` contains it. Discovery's\n"
     "outermost pruned anchor is unchanged and is not this authorization boundary. Any\n"
     "violation refuses `SNAPSHOT_PRUNED_TREE_NOT_A_READ`. **What replay decides and\n"
     "what it does not prove.** Replay decides every inventoried row: a recorded read\n"
     "path that crosses a nested installed-package boundary without its own retained\n"
     "row refuses, whatever enclosing directory is listed. The custody walk and the read\n"
     "set are host TCB observations retained with the Run. Bytes-only replay re-checks\n"
     "every retained digest, and this join, at package-directory granularity. It cannot\n"
     "prove that the host walked every first-party file, that it read no file missing\n"
     "from the inventory, or which of a listed package's own files it read: those are\n"
     "properties of an unobserved host process, not of the retained bytes.\n"),
    # ---------------------------------------------------------------- security S3 matching sentence
    (SEC,
     "members joined at Run closure, refusing `SNAPSHOT_PRUNED_TREE_NOT_A_READ`.\n"
     "VCS trees and Cargo build output are never reads. Required inputs outside the\n",
     "members joined at Run closure, refusing `SNAPSHOT_PRUNED_TREE_NOT_A_READ`.\n"
     "A nested installed package below a listed directory (a further exact\n"
     "`node_modules` segment) needs its own row; the enclosing listed directory never\n"
     "authorizes it. VCS trees and Cargo build output are never reads, at any depth.\n"
     "Required inputs outside the\n"),
    # ---------------------------------------------------------------- checker: helper rows
    (CHECK,
     "    row(\"A4\", \"nested-vcs-lookalike-segments-remain-lawful-package-reads\",\n"
     "        faults([\"node_modules/left-pad/.git-like/index.js\", \"node_modules/left-pad/.gitignore\"]) == [])\n",
     "    row(\"A4\", \"nested-vcs-lookalike-segments-remain-lawful-package-reads\",\n"
     "        faults([\"node_modules/left-pad/.git-like/index.js\", \"node_modules/left-pad/.gitignore\"]) == [])\n"
     "    # Explicit nested package custody (identity section 3). Helper rows call the owner join directly over synthetic\n"
     "    # layouts; the real-Run rows below admit altered layouts through the maintained fixture constructors.\n"
     "\n"
     "    def with_rows(*extra_rows):\n"
     "        return {\"schemaVersion\": 1, \"entries\": sorted(layout[\"entries\"] + [\n"
     "            {\"packageName\": name, \"packageVersion\": \"1.0.0\", \"installPath\": install, \"realPath\": real, \"contentSha256\": \"4\" * 64}\n"
     "            for name, install, real in extra_rows], key=lambda r: r[\"installPath\"].encode())}\n"
     "\n"
     "    evil = \"node_modules/left-pad/node_modules/evil\"\n"
     "    row(\"A4\", \"a-listed-package-authorizes-its-ordinary-descendants\",\n"
     "        faults([\"node_modules/left-pad/index.js\", \"node_modules/left-pad/dist/index.d.ts\"]) == [])\n"
     "    row(\"A4\", \"an-enclosing-listed-package-never-authorizes-a-nested-installed-package\",\n"
     "        faults([evil + \"/index.js\", evil + \"/package.json\"]) == [evil + \"/index.js\", evil + \"/package.json\"])\n"
     "    listed_evil = with_rows((\"evil\", evil, evil))\n"
     "    row(\"A4\", \"a-separately-listed-nested-package-authorizes-its-own-files\",\n"
     "        faults([evil + \"/index.js\", evil + \"/lib/x.js\"], (listed_evil,)) == [])\n"
     "    row(\"A4\", \"a-nested-package-row-does-not-authorize-deeper-or-sibling-nested-packages\",\n"
     "        faults([evil + \"/node_modules/deeper/index.js\", \"node_modules/left-pad/node_modules/other/index.js\"], (listed_evil,))\n"
     "        == [evil + \"/node_modules/deeper/index.js\", \"node_modules/left-pad/node_modules/other/index.js\"])\n"
     "    row(\"A4\", \"nested-vcs-refuses-even-inside-a-separately-listed-nested-package\",\n"
     "        faults([evil + \"/.git/HEAD\", evil + \"/.jj/repo\"], (listed_evil,)) == [evil + \"/.git/HEAD\", evil + \"/.jj/repo\"])\n"
     "    scoped_inner = \"node_modules/@scope/util/node_modules/@inner/pkg\"\n"
     "    scoped_row = (\"@scope/util\", \"node_modules/@scope/util\", \"node_modules/@scope/util\")\n"
     "    row(\"A4\", \"a-listed-scoped-package-authorizes-its-ordinary-descendants\",\n"
     "        faults([\"node_modules/@scope/util/index.js\", \"node_modules/@scope/util/lib/a.js\"], (with_rows(scoped_row),)) == [])\n"
     "    row(\"A4\", \"a-nested-scoped-package-needs-its-own-row\",\n"
     "        faults([scoped_inner + \"/index.js\"], (with_rows(scoped_row),)) == [scoped_inner + \"/index.js\"]\n"
     "        and faults([scoped_inner + \"/index.js\"], (with_rows(scoped_row, (\"@inner/pkg\", scoped_inner, scoped_inner)),)) == [])\n"
     "    row(\"A4\", \"lookalike-and-case-variant-segments-are-no-nested-package-boundary\",\n"
     "        faults([\"node_modules/left-pad/node_modules-like/index.js\", \"node_modules/left-pad/Node_modules/x/index.js\",\n"
     "                \"node_modules/left-pad/my_node_modules/index.js\"]) == [])\n"
     "    store = \"node_modules/.pnpm/store-pkg@1.0.0/node_modules/store-pkg\"\n"
     "    store_rows = ((\"store-pkg\", \"node_modules/store-pkg\", store), (\"store-pkg\", store, store))\n"
     "    row(\"A4\", \"a-listed-store-realpath-authorizes-its-ordinary-descendants\",\n"
     "        faults([store + \"/index.js\", store + \"/lib/deep/x.js\", \"node_modules/store-pkg/index.js\"], (with_rows(*store_rows),)) == [])\n"
     "    row(\"A4\", \"a-nested-package-below-a-listed-store-realpath-needs-its-own-row\",\n"
     "        faults([store + \"/node_modules/dep/index.js\", \"node_modules/.pnpm/store-pkg@1.0.0/node_modules/dep/index.js\"],\n"
     "               (with_rows(*store_rows),))\n"
     "        == [\"node_modules/.pnpm/store-pkg@1.0.0/node_modules/dep/index.js\", store + \"/node_modules/dep/index.js\"]\n"
     "        and faults([store + \"/node_modules/dep/index.js\"],\n"
     "                   (with_rows(*store_rows, (\"dep\", store + \"/node_modules/dep\", store + \"/node_modules/dep\")),)) == [])\n"
     "    row(\"A4\", \"a-first-party-realpath-keeps-first-party-custody-and-its-nested-dependency-needs-a-row\",\n"
     "        faults([\"packages/lib/src/index.ts\"]) == []\n"
     "        and faults([\"packages/lib/node_modules/x/index.js\"]) == [\"packages/lib/node_modules/x/index.js\"]\n"
     "        and faults([\"packages/lib/node_modules/x/index.js\"],\n"
     "                   (with_rows((\"x\", \"packages/lib/node_modules/x\", \"packages/lib/node_modules/x\")),)) == [])\n"
     "    row(\"A4\", \"discovery-still-reports-the-outermost-anchor-for-a-nested-package-read\",\n"
     "        M.native_admission().DD.classify_path(evil + \"/index.js\", set()) == (\"node_modules\", \"dependency-tree\"))\n"),
    # ---------------------------------------------------------------- checker: ts_run with an altered fixture layout
    (CHECK,
     "    def ts_run(extra):\n"
     "        graph = SR.S.build_ts_semantic_graph(atom=SR.REFS_EXISTS_SRC, has_declares=False, has_references_fact=True,\n"
     "                                             extra_sources=extra)\n"
     "        return SR.close_positive(graph)\n",
     "    def ts_run(extra, packages=None):\n"
     "        \"\"\"A real complete Run. `packages` adds installed-package manifests to the fixture's layout for this Run only:\n"
     "        the maintained constructors mint the altered layout, native context, universe, Plan and every dependent\n"
     "        identity, then seed admission, derive, replay and close_run run as usual. The global is restored afterwards.\"\"\"\n"
     "        scope = SR.S.helpers().native_inputs.__globals__\n"
     "        saved = scope[\"TS_NODE_MODULES\"]\n"
     "        if packages is not None:\n"
     "            scope[\"TS_NODE_MODULES\"] = {**saved, **packages}\n"
     "        try:\n"
     "            graph = SR.S.build_ts_semantic_graph(atom=SR.REFS_EXISTS_SRC, has_declares=False, has_references_fact=True,\n"
     "                                                 extra_sources=extra)\n"
     "            return SR.close_positive(graph)\n"
     "        finally:\n"
     "            scope[\"TS_NODE_MODULES\"] = saved\n"
     "\n"
     "    def ts_context_layout(result):\n"
     "        run, objects, blobs, _ = result\n"
     "        for digest in objects[run[\"planId\"]][1][\"nativeContextDigests\"]:\n"
     "            domain, context = M.parse_h_frame(blobs[digest], \"native-context\")[:2]\n"
     "            if domain == \"native.context.typescript.v2\":\n"
     "                return context, sorted(e[\"installPath\"] for e in C.parse(blobs[context[\"nodeModulesLayoutDigest\"]])[\"entries\"])\n"
     "        return None, []\n"),
    # ---------------------------------------------------------------- checker: real-Run rows
    (CHECK,
     "        got = refusal_any(lambda e=extra: ts_run(e))\n"
     "        row(\"A4\", \"real-run-refuses-\" + name, got is not None and \"SNAPSHOT_PRUNED_TREE_NOT_A_READ\" in got, got)\n",
     "        got = refusal_any(lambda e=extra: ts_run(e))\n"
     "        row(\"A4\", \"real-run-refuses-\" + name, got is not None and \"SNAPSHOT_PRUNED_TREE_NOT_A_READ\" in got, got)\n"
     "    # Explicit nested package custody on the same actual full-Run fixture.\n"
     "    evil_manifest = {evil + \"/package.json\": b'{\"name\":\"evil\",\"version\":\"0.0.1\"}\\n'}\n"
     "    inner_manifest = {scoped_inner + \"/package.json\": b'{\"name\":\"@inner/pkg\",\"version\":\"0.0.1\"}\\n'}\n"
     "    for name, extra, packages in (\n"
     "            (\"an-unlisted-nested-package-under-a-listed-package\", {evil + \"/index.js\": b\"module.exports = 3;\\n\"}, None),\n"
     "            (\"an-unlisted-nested-scoped-package-under-a-listed-scoped-package\", {scoped_inner + \"/index.js\": b\"module.exports = 4;\\n\"}, None),\n"
     "            (\"nested-vcs-inside-a-separately-listed-nested-package\", {evil + \"/.git/HEAD\": b\"ref: refs/heads/main\\n\"}, evil_manifest)):\n"
     "        path = next(iter(extra))\n"
     "        got = refusal_any(lambda e=extra, p=packages: ts_run(e, p))\n"
     "        row(\"A4\", \"real-run-refuses-\" + name, got is not None and got.endswith(\"SNAPSHOT_PRUNED_TREE_NOT_A_READ:\" + path), got)\n"
     "    base_context, base_layout = ts_context_layout(ts_run({\"node_modules/left-pad/index.js\": b\"module.exports = 1;\\n\"}))\n"
     "    for name, extra, packages, installed in (\n"
     "            (\"the-nested-package-separately-listed\", {evil + \"/index.js\": b\"module.exports = 3;\\n\"}, evil_manifest, evil),\n"
     "            (\"the-nested-scoped-package-separately-listed\", {scoped_inner + \"/index.js\": b\"module.exports = 4;\\n\"}, inner_manifest,\n"
     "             scoped_inner)):\n"
     "        path = next(iter(extra))\n"
     "        try:\n"
     "            result = ts_run(extra, packages)\n"
     "        except Exception as exc:  # noqa: BLE001 - a refused positive is a failed control\n"
     "            row(\"A4\", \"real-run-closes-with-\" + name, False, type(exc).__name__ + \":\" + str(exc))\n"
     "            continue\n"
     "        run, objects, blobs, actual = result\n"
     "        context, installs = ts_context_layout(result)\n"
     "        ok = (installed in installs and installed not in base_layout\n"
     "              and context[\"nodeModulesLayoutDigest\"] != base_context[\"nodeModulesLayoutDigest\"]\n"
     "              and M.close_run(run, objects, blobs) == actual[\"runId\"]\n"
     "              and any(r[\"path\"] == path for r in objects[run[\"snapshotId\"]][1][\"sourceInventory\"]))\n"
     "        row(\"A4\", \"real-run-closes-with-\" + name, ok, {\"runId\": actual[\"runId\"], \"layout\": installs})\n"
     "    for name, path in ((\"a-nested-lookalike-segment\", \"node_modules/left-pad/node_modules-like/index.js\"),\n"
     "                       (\"a-listed-scoped-package-file\", \"node_modules/@scope/util/index.js\")):\n"
     "        got = refusal_any(lambda p=path: ts_run({p: b\"module.exports = 5;\\n\"}))\n"
     "        row(\"A4\", \"real-run-closes-with-\" + name, got is None, got)\n"),
]

sha = lambda b: hashlib.sha256(b).hexdigest()
baseline = json.loads((BASE / 'receipts' / 'p00-copy.json').read_text())['ownedBaseline']
texts, problems = {}, []
for rel in sorted({e[0] for e in EDITS}):
    raw = (W / rel).read_bytes()
    if sha(raw) != baseline[rel]:
        problems.append('not at baseline: ' + rel)
    texts[rel] = raw.decode('utf-8')
for rel, old, new in EDITS:
    n = texts[rel].count(old)
    if n != 1:
        problems.append('%s anchor count %d: %r' % (rel, n, old[:90]))
        continue
    texts[rel] = texts[rel].replace(old, new)
out = {'standing': 'explicit nested package custody edits in this runtime work/source', 'edits': len(EDITS)}
if not problems:
    for rel in (MODEL, CHECK):
        try:
            compile(texts[rel], rel, 'exec')
        except SyntaxError as exc:
            problems.append('compile %s: %s' % (rel, exc))
if problems:
    out.update(written=False, problems=problems)
else:
    rows = []
    for rel, text in texts.items():
        (W / rel).write_text(text, encoding='utf-8')
        rows.append({'path': rel, 'before': baseline[rel], 'after': sha((W / rel).read_bytes())})
    out.update(written=True, files=rows)
(BASE / 'receipts' / 'p01-apply.json').write_text(json.dumps(out, indent=1) + '\n')
print(json.dumps(out, indent=1))
sys.exit(0 if not problems else 1)
