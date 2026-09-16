"""Reference check of the author-01 report evidence design candidate (RP-DO-03/05/09/10); not approval, runtime, browser, generator or Run replay qualification.

Run from the candidate directory (or a copy of exactly the listed subject files):
  TMPDIR=<existing absolute scratch> /tmp/opensip-implementation/metadata-reference-env/bin/python -I -B check.py \
      --architecture /Users/sb/code/opensip-ai/opensip_arch --subject-strict [--out RESULT.json]
Closure (enforced): every governed read (architecture checkout and /tmp/opensip-implementation outside this directory and the reference
environment) must be pinned in source-pins.json and is re-hashed at open; directory listings must be pinned; executed modules are compiled from
verified source bytes (bytecode is never consulted); writes are refused except the declared --out, which may not be read; child processes are
refused. The host, interpreter and reference environment are trusted. --trace-closure records the closure instead (seal.py only).
"""
import argparse
import ast
import copy
import hashlib
import importlib.machinery
import importlib.util
import json
import marshal
import os
import re
import shutil
import struct
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.pycache_prefix = "/nonexistent-opensip-report-evidence-pycache"
ENV_DIR = "/tmp/opensip-implementation/metadata-reference-env"
ORIGINAL_GET_CODE = importlib.machinery.SourceFileLoader.get_code
SUBJECT05 = "/tmp/opensip-implementation/m1-report-projection-subject-05"
SUBJECT05_MANIFEST = "/tmp/opensip-implementation/m1-report-projection-subject-05.json"
SUBJECT05_MANIFEST_SHA256 = "a9f6c22a9b2af9487fc9683fdef76c58e391f5a6f64e2f8b09bfa75d288de2a4"
RID = "urn:opensip:product-v1:workflows:evaluator3:report-projection:1"
GQ = "urn:opensip:product-v1:workflows:evaluator3:graph-query:3#/$defs/"
N = "urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/"
CHILD_EVENTS = ("subprocess.Popen", "os.system", "os.exec", "os.posix_spawn", "os.spawn", "os.fork", "os.forkpty", "pty.spawn")
REMOVED = ["coupling-importer-package-membership", "entry-point-recognition", "symbol-metrics", "test-reachability"]


def norm(path):
    p = os.path.abspath(os.fsdecode(path))
    return p[len("/private"):] if p.startswith("/private/tmp/") else p


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


class Closure:
    def __init__(self, arch, trace, out):
        self.roots = [norm(arch), "/tmp/opensip-implementation"]
        self.excluded = [norm(HERE), ENV_DIR]
        self.trace, self.out, self.scratch = trace, (norm(out) if out else None), None
        self.files, self.directories = set(), set()
        self.pinned, self.listings, self.pinned_inodes, self.listing_inodes = {}, {}, {}, {}
        self.busy = False
        self.counts = {"rehashedOpens": 0, "listingRecomputes": 0, "verifiedSourceCompiles": 0, "declaredOutWrites": 0}

    @staticmethod
    def under(path, root):
        p, r = path.casefold(), root.casefold()
        return p == r or p.startswith(r + "/")

    def governed(self, path):
        spellings = {path, norm(os.path.realpath(path))}
        if self.scratch and any(self.under(p, self.scratch) for p in spellings):
            return False
        return any(any(self.under(p, r) for r in self.roots) and not any(self.under(p, e) for e in self.excluded) for p in spellings)

    @staticmethod
    def identity(path):
        try:
            st = os.stat(path)
        except OSError:
            return None
        return (st.st_dev, st.st_ino)

    def pin_for(self, path):
        return self.pinned.get(path) or self.pinned_inodes.get(self.identity(path))

    @staticmethod
    def listing_digest(path):
        return sha("\n".join(sorted(os.listdir(path))).encode())

    def verify_pins(self, pins):
        for pin in pins["files"]:
            raw = Path(pin["path"]).read_bytes()
            if len(raw) != pin["bytes"] or sha(raw) != pin["sha256"]:
                raise SystemExit("CLOSURE-PIN-DRIFT " + pin["path"])
            self.pinned[pin["path"]] = pin
            self.pinned_inodes[self.identity(pin["path"])] = pin
        for listing in pins["directoryListings"]:
            if self.listing_digest(listing["path"]) != listing["entriesSha256"]:
                raise SystemExit("CLOSURE-LISTING-DRIFT " + listing["path"])
            self.listings[listing["path"]] = listing["entriesSha256"]
            self.listing_inodes[self.identity(listing["path"])] = listing["entriesSha256"]

    def verify_source(self, path, data):
        path = norm(path)
        if not self.governed(path):
            return
        if self.trace:
            self.files.add(path)
            return
        pin = self.pin_for(path)
        if pin is None or len(data) != pin["bytes"] or sha(data) != pin["sha256"]:
            raise RuntimeError("SOURCE-PIN-DRIFT " + path)
        self.counts["verifiedSourceCompiles"] += 1

    def hook(self, event, args):
        if event.startswith(CHILD_EVENTS):
            raise RuntimeError("CHILD-PROCESS-REFUSED " + event)
        if self.busy or event not in ("open", "os.listdir", "os.scandir"):
            return
        if not args or not isinstance(args[0], (str, bytes, os.PathLike)):
            return
        path = norm(args[0])
        writing = False
        if event == "open":
            mode = args[1] if len(args) > 1 else None
            flags = args[2] if len(args) > 2 and isinstance(args[2], int) else 0
            writing = (isinstance(mode, str) and any(c in mode for c in "wax+")) or bool(flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND))
            if self.out is not None and path == self.out:
                if not writing:
                    raise RuntimeError("DECLARED-OUT-READ " + path)
                self.counts["declaredOutWrites"] += 1
                return
        if not self.governed(path):
            return
        self.busy = True
        try:
            if event == "open":
                if writing:
                    raise RuntimeError("UNDECLARED-WRITE " + path)
                if self.trace:
                    self.files.add(path)
                    return
                pin = self.pin_for(path)
                if pin is None:
                    raise RuntimeError("UNPINNED-LOAD " + path)
                with open(path, "rb") as handle:
                    raw = handle.read()
                if len(raw) != pin["bytes"] or sha(raw) != pin["sha256"]:
                    raise RuntimeError("CLOSURE-PIN-DRIFT-AT-OPEN " + path)
                self.counts["rehashedOpens"] += 1
            else:
                if self.trace:
                    self.directories.add(path)
                    return
                expected = self.listings.get(path) or self.listing_inodes.get(self.identity(path))
                if expected is None:
                    raise RuntimeError("UNPINNED-LISTING " + path)
                if self.listing_digest(path) != expected:
                    raise RuntimeError("CLOSURE-LISTING-DRIFT-AT-LISTING " + path)
                self.counts["listingRecomputes"] += 1
        finally:
            self.busy = False


def install_fresh_source_loader(closure):
    def get_code(self, fullname):
        path = self.get_filename(fullname)
        data = self.get_data(path)
        closure.verify_source(path, data)
        return compile(data, path, "exec", dont_inherit=True)

    original_sourceless = importlib.machinery.SourcelessFileLoader.get_code

    def sourceless(self, fullname):
        if closure.governed(norm(self.get_filename(fullname))):
            raise ImportError("BYTECODE-ONLY-MODULE-REFUSED " + self.get_filename(fullname))
        return original_sourceless(self, fullname)
    importlib.machinery.SourceFileLoader.get_code = get_code
    importlib.machinery.SourcelessFileLoader.get_code = sourceless


def bytecode_demo(closure, scratch_root):
    directory = tempfile.mkdtemp(prefix="opensip-rev01-pyc-", dir=scratch_root)
    closure.scratch = norm(directory)
    saved = sys.pycache_prefix
    try:
        source = os.path.join(directory, "mod.py")
        with open(source, "w") as handle:
            handle.write('VALUE = "verified-source"\n')
        stat = os.stat(source)
        cache = os.path.join(directory, "__pycache__", "mod." + sys.implementation.cache_tag + ".pyc")
        os.makedirs(os.path.dirname(cache))
        with open(cache, "wb") as handle:
            handle.write(importlib.util.MAGIC_NUMBER + struct.pack("<III", 0, int(stat.st_mtime) & 0xFFFFFFFF, stat.st_size & 0xFFFFFFFF)
                         + marshal.dumps(compile('VALUE = "stale-bytecode"\n', source, "exec")))
        sys.pycache_prefix = None
        stock, enforced = {}, {}
        exec(ORIGINAL_GET_CODE(importlib.machinery.SourceFileLoader("rev01_stock", source), "rev01_stock"), stock)
        exec(importlib.machinery.SourceFileLoader("rev01_enforced", source).get_code("rev01_enforced"), enforced)
    finally:
        sys.pycache_prefix = saved
        shutil.rmtree(directory)
        closure.scratch = None
    assert stock["VALUE"] == "stale-bytecode" and enforced["VALUE"] == "verified-source"
    return {"stockLoaderWithAdjacentCache": stock["VALUE"], "enforcedLoader": enforced["VALUE"]}


# ---------------------------------------------------------------------------
# helpers

def unescape(token):
    return token.replace("~1", "/").replace("~0", "~")


def pointer_parent(doc, path):
    tokens = [unescape(t) for t in path.strip("/").split("/")]
    node = doc
    for token in tokens[:-1]:
        node = node[int(token)] if isinstance(node, list) else node[token]
    return node, tokens[-1]


def apply_patch(doc, ops):
    out = copy.deepcopy(doc)
    for op in ops:
        parent, key = pointer_parent(out, op["path"])
        if op["op"] == "remove-rows":
            assert parent[key] == op["before"], "patch before mismatch " + op["path"]
            kept = [row for row in parent[key] if (row[op["matchKey"]] if "matchKey" in op else row) not in op["match"]]
            assert kept == op["after"] and len(kept) < len(parent[key]), "remove-rows after mismatch " + op["path"]
            parent[key] = kept
        elif op["op"] == "add":
            assert key not in parent, "patch add over existing " + op["path"]
            parent[key] = copy.deepcopy(op["after"])
        else:
            raise AssertionError("unknown op")
    return out


class Outcome:
    def __init__(self, ref, registry, M, ValidationError):
        self.ref, self.registry, self.M, self.ValidationError = ref, registry, M, ValidationError

    def schema(self, selector, value):
        self.ref.validate({"$ref": selector}, value, self.registry)

    def run(self, fn):
        try:
            fn()
            return "accept"
        except self.M.Refusal as exc:
            return exc.code
        except self.ValidationError:
            return "SCHEMA"
        except self.ref.AdmissionError:
            return "SCHEMA"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--architecture", required=True, type=Path)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--trace-closure", type=Path)
    parser.add_argument("--subject-strict", action="store_true")
    args = parser.parse_args()
    arch = args.architecture
    report = {"standing": "AUTHOR-01 report evidence design candidate reference check; not approval, runtime, browser, generator or Run replay qualification"}
    scratch_root = os.environ.get("TMPDIR", "")
    assert os.path.isabs(scratch_root) and os.path.isdir(scratch_root), "set TMPDIR to an existing absolute scratch directory"
    closure = Closure(arch, trace=bool(args.trace_closure), out=args.out or args.trace_closure)
    if not args.trace_closure:
        manifest = json.loads((HERE / "subject-files.json").read_bytes())
        listed = {row["path"] for row in manifest["files"]}
        for row in manifest["files"]:
            raw = (HERE / row["path"]).read_bytes()
            assert len(raw) == row["bytes"] and sha(raw) == row["sha256"], "subject drift " + row["path"]
        if args.subject_strict:
            present = {str(p.relative_to(HERE)) for p in HERE.rglob("*") if p.is_file() and "__pycache__" not in p.parts} - {"subject-files.json"}
            assert present == listed, ("subject directory differs from manifest", sorted(present ^ listed))
        report["subjectFiles"] = len(listed)
        report["subjectManifestSha256"] = sha((HERE / "subject-files.json").read_bytes())
        closure.verify_pins(json.loads((HERE / "source-pins.json").read_bytes()))
        report["externalPins"] = {"files": len(closure.pinned), "directoryListings": len(closure.listings)}
    sys.addaudithook(closure.hook)
    install_fresh_source_loader(closure)
    report["bytecodeDemo"] = bytecode_demo(closure, scratch_root)
    if not args.trace_closure:
        head, tail = norm(arch).rsplit("/", 1)
        aliases = {"exact": norm(arch) + "/docs/implementation/README.md", "case-variant": head + "/" + tail.upper() + "/docs/implementation/README.md",
                   "dot-dot": norm(arch) + "/docs/implementation/m1/../README.md"}
        probe = {}
        for label, alias in aliases.items():
            try:
                with open(alias, "rb"):
                    probe[label] = "READ-NOT-REFUSED"
            except RuntimeError as exc:
                probe[label] = str(exc).split(" ")[0]
            except OSError as exc:
                probe[label] = "OSERROR-" + type(exc).__name__
        assert all(v == "UNPINNED-LOAD" for v in probe.values()), probe
        report["aliasProbe"] = probe

    from jsonschema import Draft202012Validator, ValidationError
    from referencing import Resource
    from referencing.jsonschema import DRAFT202012

    # 1. parents: subject-05 frozen manifest, pinned owners, reference modules
    s05_manifest_raw = Path(SUBJECT05_MANIFEST).read_bytes()
    assert sha(s05_manifest_raw) == SUBJECT05_MANIFEST_SHA256, "subject-05 outer manifest drift"
    s05_files = {row["path"]: row for row in json.loads(s05_manifest_raw)["files"]}

    def s05(name):
        raw = Path(SUBJECT05 + "/" + name).read_bytes()
        assert sha(raw) == s05_files[name]["sha256"] and len(raw) == s05_files[name]["bytes"], "subject-05 file drift " + name
        return raw
    for name in ("report_model.py", "report-projection.schema.json", "fixtures.json", "owner/design-obligations.v1.json",
                 "owner/implementation-coverage-successor.v1.json", "owner/command-envelope.v5.schema.json", "owner/command-inventory.v5.schema.json"):
        s05(name)
    report["subject05"] = {"manifestSha256": SUBJECT05_MANIFEST_SHA256, "filesVerified": 7}
    cm = load("check_metadata_v2", arch / "docs/implementation/m1/metadata-v2/check_metadata.py")
    ref, registry, documents = cm.load(arch)
    canonical = load("foundation_canonical", arch / "docs/coop/design-corrections/foundation/canonical.py")
    RM = load("subject05_report_model", Path(SUBJECT05) / "report_model.py")
    M = load("evidence_reference_model", HERE / "reference_model.py")
    M.bind(canonical, RM)
    owner = load("evidence_build_owner", HERE / "build_owner.py")
    builder = load("evidence_build_fixtures", HERE / "build_fixtures.py")

    # 2. byte-identical regeneration
    owners = owner.build(arch, M)
    for name, value in owners.items():
        assert owner.dump(value) == (HERE / name).read_bytes(), "owner drift " + name
    s05_fixtures = json.loads(s05("fixtures.json"))
    fixture = builder.build(M, s05_fixtures)
    fixture_raw = owner.dump(fixture)
    assert fixture_raw == (HERE / "fixtures.json").read_bytes(), "fixtures drift"
    report["regeneration"] = {"ownerFiles": sorted(owners), "fixturesSha256": sha(fixture_raw)}

    # 3. owner schema admission: parameter document, report successor patch, identity registry patch
    for extra in ("docs/coop/design-corrections/foundation/enumeration-plan.schema.v1.json", "docs/coop/design-corrections/foundation/subject-inventory.schema.v1.json"):
        doc = ref.parse((arch / extra).read_bytes())
        Draft202012Validator.check_schema(doc)
        documents[doc["$id"]] = doc
        registry = registry.with_resource(doc["$id"], Resource(contents={k: v for k, v in doc.items() if k != "$schema"}, specification=DRAFT202012))
    parameter_raw = (HERE / "owner/framework-recognition-plan.schema.v1.json").read_bytes()
    parameter = ref.parse(parameter_raw)
    Draft202012Validator.check_schema(parameter)
    native = documents["urn:opensip:product-v1:native:evidence-schemas:v2"]
    for name in ("FrameworkRecognitionV1", "FrameworkRecognitionResultV1", "EntryPointRecognitionV1", "InternalUnitRootV1"):
        assert ref.equal_typed(parameter["$defs"][name], native["$defs"][name]), "parameter copy drift " + name
    assert not re.findall(r'"\$ref":\s*"(?!#)', parameter_raw.decode()), "parameter document must not reference other documents"
    registry = registry.with_resource(parameter["$id"], Resource(contents={k: v for k, v in parameter.items() if k != "$schema"}, specification=DRAFT202012))
    for name in ("owner/command-envelope.v5.schema.json", "owner/command-inventory.v5.schema.json"):
        doc = ref.parse(s05(name))
        documents[doc["$id"]] = doc
        registry = registry.with_resource(doc["$id"], Resource(contents={k: v for k, v in doc.items() if k != "$schema"}, specification=DRAFT202012))
    patch = owners["owner/report-projection-successor-patch.v1.json"]
    parent_raw = s05("report-projection.schema.json")
    assert patch["parent"]["sha256"] == sha(parent_raw) and patch["parent"]["subjectManifestSha256"] == SUBJECT05_MANIFEST_SHA256
    parent = ref.parse(parent_raw)
    patched = apply_patch(parent, patch["ops"])
    Draft202012Validator.check_schema(patched)
    changed = sorted(set(patched["$defs"]) ^ set(parent["$defs"]))
    assert all(patched["$defs"][k] == parent["$defs"][k] for k in parent["$defs"] if k not in ("FeatureId", "PanelsV1"))
    shared = [op["path"] for op in patch["ops"] if op["op"] == "remove-rows" and op["path"].startswith("/allOf/")]
    assert shared == ["/allOf/%d/then/properties/featureStates/const" % i for i in range(3, 10)], shared
    unshared = copy.deepcopy(patched)
    for op in patch["ops"]:
        if op["path"].startswith("/allOf/"):
            node, key = pointer_parent(unshared, op["path"])
            node[key] = copy.deepcopy(op["before"])
    assert {k: v for k, v in unshared.items() if k != "$defs"} == {k: v for k, v in parent.items() if k != "$defs"}, "root changes beyond the featureStates consts"
    # commutation with another obligation's remove-rows over the same shared selectors (step-duration stands in for RP-DO-11)
    other = [dict(op, match=["step-duration"], after=None) for op in patch["ops"] if op["op"] == "remove-rows"]

    def remove(doc, ops, match):
        out = copy.deepcopy(doc)
        for op in ops:
            if op["op"] != "remove-rows":
                continue
            node, key = pointer_parent(out, op["path"])
            node[key] = [r for r in node[key] if (r[op["matchKey"]] if "matchKey" in op else r) not in match]
        return out
    assert remove(remove(parent, patch["ops"], REMOVED), other, ["step-duration"]) == remove(remove(parent, other, ["step-duration"]), patch["ops"], REMOVED)
    assert patched["$defs"]["FeatureId"]["enum"] == [f for f in parent["$defs"]["FeatureId"]["enum"] if f not in REMOVED]
    assert patched["$defs"]["PanelsV1"]["properties"] == dict(parent["$defs"]["PanelsV1"]["properties"], coupling={"$ref": "#/$defs/CouplingPanelStateV1"},
                                                                symbolEvidence={"$ref": "#/$defs/SymbolEvidencePanelStateV1"})
    registry = registry.with_resource(RID, Resource(contents={k: v for k, v in patched.items() if k != "$schema"}, specification=DRAFT202012))
    documents[RID] = patched
    for doc in (patched, parameter):
        for target in re.findall(r'"\$ref":\s*"([^"#]+)', json.dumps(doc)):
            assert target in documents, "unregistered " + target
    ipatch = owners["owner/identity-parameter-registry-patch.v1.json"]
    identity_raw = (arch / "docs/coop/design-corrections/foundation/identity-schemas.v3.json").read_bytes()
    assert ipatch["parent"]["sha256"] == sha(identity_raw)
    identity = json.loads(identity_raw)
    rows = identity["x-opensip-payload-registry"]["classes"]["parameter"]["rows"]
    parent_node, key = pointer_parent(identity, ipatch["ops"][0]["path"])
    assert parent_node is rows and key not in rows
    vocabulary = set().union(*(set(r) for r in rows.values()))
    assert set(ipatch["ops"][0]["after"]) <= vocabulary and ipatch["ops"][0]["after"]["requiredForEvaluatorMajors"] == rows["foundation/enumeration-plan.schema.v1.json"]["requiredForEvaluatorMajors"]
    report["ownerAdmission"] = {"parameterSchemaSha256": sha(parameter_raw), "reportPatchOps": len(patch["ops"]), "newReportDefs": changed,
                                "patchedReportCanonicalSha256": sha(ref.canonical(patched)), "identityRowAddedWithExistingVocabulary": True,
                                "nativeCopiesDriftChecked": 4}

    # 4. glob law: contract examples, pinned workflows_model.glob_match (AST-extracted), unit-relative slicing examples
    contract = (arch / "docs/coop/design-corrections/foundation/glob-pattern-contract.v1.md").read_text()
    table = contract.split("## Required examples", 1)[1].split("##", 1)[0]
    examples = []
    for line in table.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) == 3 and cells[2] in ("true", "false"):
            pattern, candidate = re.findall(r"`([^`]*)`", cells[0])[0], re.findall(r"`([^`]*)`", cells[1])[0]
            examples.append((pattern, candidate, cells[2] == "true"))
    workflows_src = (arch / "docs/coop/design-corrections/workflows/workflows_model.v1.py").read_bytes()
    tree = ast.parse(workflows_src)
    fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "glob_match")
    namespace = {}
    exec(compile(ast.Module(body=[fn], type_ignores=[]), "workflows_model.v1.glob_match", "exec"), namespace)
    extra = [("**/*.test.*", "src/button.test.tsx", True), ("src/**/*.test.ts", "src/a.test.ts", True), ("src/**/*.test.ts", "packages/web/src/a.test.ts", False),
             ("**/__tests__/**", "src/__tests__/x.ts", True), ("**/*.spec.*", "src/button.tsx", False)]
    for pattern, candidate, expected in examples + extra:
        assert M.glob_match(pattern, candidate) == expected == namespace["glob_match"](pattern, candidate), (pattern, candidate)
    assert len(examples) == 22
    report["globLaw"] = {"contractExamples": len(examples), "unitRelativeExamples": len(extra), "agreesWithPinnedWorkflowsGlobMatch": True}

    # 5. worlds: owner-schema validation and closure joins
    V = Outcome(ref, registry, M, ValidationError)
    variants = builder.variants(M)
    descriptions = copy.deepcopy(fixture["descriptions"])

    def world(name):
        if name in descriptions:
            desc = copy.deepcopy(descriptions[name])
        else:
            desc = variants[name](copy.deepcopy(descriptions["mixed"]))
        data = builder.assemble(desc, M)
        V.schema(N + "UnitMembershipV1", data["membership"])
        V.schema("opensip.product.enumeration-plan.1", data["enumerationPlan"])
        for inv in data["subjectInventories"]:
            V.schema("opensip.product.subject-inventory.1", inv)
        for record in data["sourceUnitOwnership"].values():
            V.schema(N + "SourceUnitOwnershipV1", record)
        if data["recognition"]["record"] is not None:
            V.schema("opensip.product.framework-recognition-plan.1", data["recognition"]["record"])
        for fact in data["facts"]:
            V.schema(GQ + "GraphEndpoint", fact["source"])
            V.schema(GQ + "GraphEndpoint", fact["target"])
        built = M.World(data)
        if data["recognition"]["record"] is not None:
            M.admit_recognition_plan(built, data["recognition"]["record"])
        return built

    worlds = {name: world(name) for name in ("mixed", "clean", "integration")}
    resolutions = fixture["resolutions"]
    BIG = 4194304
    panels, admitted = {}, {}

    def ctx(w, resolution):
        return {"projectId": w.project_id, "runId": w.run_id, "resolution": resolution, "graphResolution": resolution, "bounds": M.PUBLIC_BOUNDS}

    def build_panels(w, resolution, **kw):
        coupling = M.derive_coupling(w, key_resolver=kw.get("key_resolver"), test_origin_state=M.test_origin_state_fn(w))
        evidence = M.derive_symbol_evidence(w, resolution, kw.get("metric_budget", BIG), start_resolver=kw.get("start_resolver"), name_resolver=kw.get("name_resolver"))
        return coupling, evidence

    def admit_panels(w, resolution, coupling, evidence):
        V.schema(RID + "#/$defs/CouplingPanelV1", coupling)
        M.admit_coupling(coupling, w.run_id)
        V.schema(RID + "#/$defs/SymbolEvidencePanelV1", evidence)
        M.admit_symbol_evidence(evidence, ctx(w, resolution))

    for name, resolution_key in (("mixed", "mixed"), ("clean", "mixed"), ("integration", "integration")):
        coupling, evidence = build_panels(worlds[name], resolutions[resolution_key])
        admit_panels(worlds[name], resolutions[resolution_key], coupling, evidence)
        panels[name] = {"coupling": coupling, "symbolEvidence": evidence}
    mixed_c, mixed_e = panels["mixed"]["coupling"], panels["mixed"]["symbolEvidence"]
    keys = {}
    for o in mixed_c["owners"]:
        alias = {"svc": "svc", "core": "core", "app": "app", "@fx/shared": "shared", "@fx/web": "web", "lodash": "lodash"}.get(o.get("packageName"))
        keys[alias or ("legacy" if o["keyKind"] == "workspace-unit" else None)] = o["ownerKey"]
    cell = {(r["fromOwnerKey"], r["toOwnerKey"]): r for r in mixed_c["cells"]}
    C = lambda a, b: cell.get((keys[a], keys[b]))
    strip = lambda c: {k: c[k] for k in ("facts", "edges", "importerSymbols", "sharedImporterFacts", "sharedTargetFacts", "internal")}
    expected_cells = {("app", "core"): (4, 3, 2, 1, 0, False), ("core", "core"): (2, 2, 2, 1, 0, True), ("svc", "app"): (1, 1, 1, 0, 0, False),
                      ("web", "shared"): (2, 2, 1, 0, 0, False), ("web", "lodash"): (1, 1, 1, 0, 0, False), ("legacy", "web"): (1, 1, 1, 0, 0, False),
                      ("shared", "web"): (1, 1, 1, 0, 0, False), ("web", "web"): (1, 1, 1, 0, 0, True)}
    for (a, b), values in expected_cells.items():
        assert tuple(strip(C(a, b)).values()) == values, ((a, b), strip(C(a, b)))
    assert len(mixed_c["cells"]) == 8 and C("app", "shared") is None and C("core", "app") is None
    assert mixed_c["totals"] == {"distinctFacts": 17, "attributedFacts": 12, "importerUnattributedFacts": 3, "targetUnattributedFacts": 2}
    assert mixed_c["importerBuckets"] == [{"cause": "not-compiled-by-selected-targets", "facts": 1}, {"cause": "owned-only-by-unselected-targets", "facts": 1},
                                          {"cause": "symbol-not-inventoried", "facts": 1}]
    assert sorted((b["cause"], b["fromOwnerKey"] == keys["web"]) for b in mixed_c["targetBuckets"]) == [("external-non-package-target", True), ("unknown-occupancy", True)]
    assert mixed_c["absence"] == {"blankCellMeans": "no-projected-fact", "absenceSupported": False, "blockers": ["evidence-limitations", "unattributed-importers", "unattributed-targets"]}
    owners_by_key = {o["ownerKey"]: o for o in mixed_c["owners"]}
    assert [t["targetKind"] for t in owners_by_key[keys["core"]]["cargoTargets"]] and {t["targetName"] for t in owners_by_key[keys["core"]]["cargoTargets"]} == {"core", "it"}
    assert owners_by_key[keys["legacy"]]["workspaceUnit"]["rootPath"] == "packages/web-legacy" and owners_by_key[keys["lodash"]]["keyKind"] == "external-package"
    assert {r["importerTestOrigin"] for r in mixed_c["drilldown"] if r["importer"]["nativeSubjectId"] == "ts:web/button.test"} == {"test-origin"}
    clean_c = panels["clean"]["coupling"]
    assert clean_c["absence"] == {"blankCellMeans": "no-projected-fact", "absenceSupported": True, "blockers": []} and not clean_c["importerBuckets"]
    integration_c = panels["integration"]["coupling"]
    assert integration_c["absence"]["absenceSupported"] and [c["facts"] for c in integration_c["cells"]] and sum(c["facts"] for c in integration_c["cells"]) == 2
    coupling_expect = {"mixedCells": 8, "mixedTotals": mixed_c["totals"], "cleanAbsenceSupported": True, "integrationAbsenceSupported": True}

    sid = {e["endpoint"]["nativeSubjectId"]: e["subjectId"] for e in resolutions["mixed"] if e["state"] == "resolved"}
    metric = {(r["subjectId"], r["metricId"]): r for r in mixed_e["metrics"]}
    assert len(mixed_e["metrics"]) == 35 and mixed_e["metricsProjection"] == {"total": 35, "omitted": 0, "omissionCause": "none"}
    readings = {m: (metric[(sid["rs:core::parse"], m)]["countState"], metric[(sid["rs:core::parse"], m)].get("value"), metric[(sid["rs:core::parse"], m)].get("zeroSupportsAbsence"))
                for m in M.METRIC_IDS}
    assert readings == {"distinct-resolved-callees-within-1-hop": ("exact", 0, True), "distinct-resolved-callers-within-1-hop": ("exact", 3, False),
                        "resolved-call-facts-incoming": ("exact", 3, False), "resolved-call-facts-outgoing": ("exact", 0, True),
                        "resolved-reference-facts-incoming": ("unknown", None, None)}, readings
    assert metric[(sid["rs:core::parse"], "resolved-reference-facts-incoming")]["cause"] == "native-evidence-unavailable"
    assert all(r["cause"] == "subject-descriptor-not-retained" for r in mixed_e["metrics"] if r["subjectId"].endswith(builder.H("descriptor-not-retained")))
    trace = {t["subjectId"]: t for t in mixed_e["traces"]}
    assert (trace[sid["rs:core::parse"]]["state"], trace[sid["rs:core::parse"]]["start"]["attributionPath"]) == ("path-found", "src/main.rs")
    assert [e["factId"] for e in trace[sid["rs:core::parse"]]["path"]["response"]["items"][0]["edges"]] == [builder.fact_id("c01")]
    assert (trace[sid["rs:core::shared_fmt"]]["state"], trace[sid["rs:core::shared_fmt"]]["blockers"], trace[sid["rs:core::shared_fmt"]]["originsOutsideEntrySet"]) == ("no-entry-origin", [], 1)
    api = trace[sid["ts:web/api"]]
    assert api["state"] == "path-found" and api["start"]["entry"]["provenance"][0]["recognizerId"] == "nextjs" and api["start"]["entry"]["provenance"][0]["unresolvedChoices"] == ["config-requires-evaluation"]
    assert len(api["path"]["response"]["items"][0]["edges"]) == 2
    assert trace[sid["ts:web/button.test"]]["blockers"] == ["entry-recognition-not-all"] and trace[sid["ts:legacy/old"]]["blockers"] == ["entry-recognition-not-all"]
    reach = {r["subjectId"]: r for r in mixed_e["testReachability"]}
    parse = reach[sid["rs:core::parse"]]
    assert parse["state"] == "static-path-from-test-origin" and parse["origin"]["endpoint"]["nativeSubjectId"] == "rs:core::it_parses"
    assert [e["factId"] for e in parse["witness"]["response"]["items"][0]["edges"]] == [builder.fact_id("c02"), builder.fact_id("c03")]
    assert reach[sid["rs:core::shared_fmt"]]["state"] == "not-found-incomplete" and reach[sid["rs:core::shared_fmt"]]["blockers"] == ["test-origin-set-partial"]
    assert reach[sid["ts:web/api"]]["origin"]["originEvidence"] == {"kind": "recognized-test-glob", "unitOrdinal": 2, "recognizerId": "vitest-jest", "glob": "**/*.test.*",
                                                                   "relativePath": "src/button.test.tsx"}
    assert reach[sid["ts:web/button.test"]]["state"] == "is-test-origin" and reach[sid["ts:legacy/old"]] == {"subjectId": sid["ts:legacy/old"], "state": "unknown", "cause": "no-test-origin-identity"}
    sets = {s["universe"]: s for s in mixed_e["testOrigins"]}
    assert sets[builder.UR]["limitations"] == ["in-target-unit-tests-not-identified", "shared-test-and-non-test-target-path"] and sets[builder.UR]["originCount"] == 1
    assert sets[builder.UW]["completeness"] == "partial" and sets[builder.UW]["limitations"] == ["foreign-unit-paths-not-matched"] and sets[builder.UL]["cause"] == "no-test-recognizer"
    ie = panels["integration"]["symbolEvidence"]
    isid = {e["endpoint"]["nativeSubjectId"]: e["subjectId"] for e in resolutions["integration"] if e["state"] == "resolved"}
    itrace = {t["subjectId"]: t for t in ie["traces"]}
    assert itrace[isid["ts:src/helper.ts#helper"]]["start"]["entry"]["provenance"] == [{"source": "explicit"}] and ie["entryRecognition"]["explicitEntryPointCount"] == 1
    ireach = {r["subjectId"]: r for r in ie["testReachability"]}
    assert ireach[isid["ts:src/index.ts#main"]]["state"] == "no-static-path-within-bound" and ireach[isid["ts:src/helper.ts#helper"]]["state"] == "static-path-from-test-origin"
    report["positive"] = {"coupling": coupling_expect, "mixedMetrics": 35, "mixedTraceStates": sorted({t["state"] for t in mixed_e["traces"]}),
                          "mixedTestStates": sorted({r["state"] for r in mixed_e["testReachability"]}),
                          "integrationTestStates": sorted({r["state"] for r in ie["testReachability"]})}

    # 6. variants (availability, custody, bounds and partial owner data)
    vr = {}
    w = world("mixed-core-package-partial")
    c, e = build_panels(w, resolutions["mixed"])
    admit_panels(w, resolutions["mixed"], c, e)
    vr["core-package-partial"] = {"importerBuckets": {b["cause"]: b["facts"] for b in c["importerBuckets"]},
                                  "targetBuckets": sorted((b["cause"], b["facts"]) for b in c["targetBuckets"])}
    # i04 (shared.rs, owned by core and app) and i05 (vendored util.rs, owned by core) lose their importer owner; i01-i03 keep importer app but
    # their core targets are unattributed. Partial knowledge never falls back to the remaining owner or a directory.
    assert vr["core-package-partial"]["importerBuckets"] == {"not-compiled-by-selected-targets": 1, "owned-only-by-unselected-targets": 1,
                                                             "package-inventory-incomplete": 2, "symbol-not-inventoried": 1}, vr
    assert ("package-inventory-incomplete", 3) in vr["core-package-partial"]["targetBuckets"] and not any(r["toOwnerKey"] == keys["core"] for r in c["drilldown"])
    for name, recognition_state, cause in (("mixed-not-plan-bound", {"state": "not-plan-bound"}, "recognition-not-plan-bound"),
                                           ("mixed-recognition-purged", {"state": "unavailable", "availability": "purged"}, "recognition-unavailable"),
                                           ("mixed-recognition-partial-missing", {"state": "unavailable", "availability": "partial"}, "recognition-unavailable")):
        w = world(name)
        c, e = build_panels(w, resolutions["mixed"])
        admit_panels(w, resolutions["mixed"], c, e)
        assert {k: v for k, v in e["entryRecognition"].items() if k != "parameterDigest"} == recognition_state
        assert {t["cause"] for t in e["traces"]} == {cause, "subject-descriptor-not-retained"}
        web = {s["universe"]: s for s in e["testOrigins"]}[builder.UW]
        assert web["source"] == "none" and web["cause"] == cause and {s["universe"]: s for s in e["testOrigins"]}[builder.UR]["source"] == "rust-test-targets"
        vr[name] = {"entryRecognition": recognition_state, "traceCause": cause}
    w = world("mixed-recognition-partial-present")
    c, e = build_panels(w, resolutions["mixed"])
    admit_panels(w, resolutions["mixed"], c, e)
    assert e["entryRecognition"]["state"] == "plan-bound" and e["entryRecognition"]["availability"] == "partial"
    vr["mixed-recognition-partial-present"] = "plan-bound/partial"
    w = world("mixed-no-reachability-view")
    c, e = build_panels(w, resolutions["mixed"])
    admit_panels(w, resolutions["mixed"], c, e)
    assert {t["cause"] for t in e["traces"]} == {"reachability-evidence-unavailable", "subject-descriptor-not-retained"}
    vr["mixed-no-reachability-view"] = "reachability-evidence-unavailable"
    w = world("mixed-many-origins")
    c, e = build_panels(w, resolutions["mixed"])
    admit_panels(w, resolutions["mixed"], c, e)
    assert {t["subjectId"]: t for t in e["traces"]}[sid["rs:core::shared_fmt"]]["cause"] == "origin-page-set-not-embedded"
    vr["mixed-many-origins"] = "origin-page-set-not-embedded"
    w = world("mixed-fan-in-100001")
    lib = [s for s in [{"subjectId": RM.subject_id(builder.ep(builder.UR, "symbol", "rs:core::lib")), "state": "resolved", "endpoint": builder.ep(builder.UR, "symbol", "rs:core::lib")}]]
    rows, projection = M.derive_metrics(w, M.EvidenceGraphOwner(w), lib, BIG)
    for row in rows:
        V.schema(RID + "#/$defs/SymbolMetricV1", row)
    M.admit_symbol_metrics(rows, projection, ctx(w, lib))
    fan = {r["metricId"]: (r["countState"], r.get("value")) for r in rows}
    assert fan["resolved-call-facts-incoming"] == ("lower-bound", 100000) and fan["distinct-resolved-callers-within-1-hop"] == ("lower-bound", 100000)
    assert fan["resolved-call-facts-outgoing"] == ("exact", 0)
    vr["mixed-fan-in-100001"] = fan
    w = worlds["mixed"]
    full_bytes = len(ref.canonical(mixed_e["metrics"]))
    rows, projection = M.derive_metrics(w, M.EvidenceGraphOwner(w), resolutions["mixed"], full_bytes // 2)
    assert projection["omissionCause"] == "byte-budget" and 0 < projection["omitted"] < 35 and projection["rejectedByteDelta"] > 0
    assert rows == mixed_e["metrics"][:len(rows)] and len(ref.canonical(rows)) <= full_bytes // 2 < len(ref.canonical(mixed_e["metrics"][:len(rows) + 1]))
    V.schema(RID + "#/$defs/ItemProjectionV1", projection)
    M.admit_symbol_metrics(rows, projection, ctx(w, resolutions["mixed"]))
    vr["metric-byte-budget"] = projection
    w = world("mixed-run-evidence-purged")
    assert V.run(lambda: M.derive_coupling(w)) == "QUERY-EVIDENCE-UNAVAILABLE" and V.run(lambda: M.derive_symbol_evidence(w, resolutions["mixed"], BIG)) == "QUERY-EVIDENCE-UNAVAILABLE"
    for panel_name in ("CouplingPanelStateV1", "SymbolEvidencePanelStateV1"):
        V.schema(RID + "#/$defs/" + panel_name, {"state": "unavailable", "reason": "evidence-purged"})
    vr["mixed-run-evidence-purged"] = "panels unavailable/evidence-purged"
    report["variants"] = vr

    # 7. document cases
    def subject_alias(token):
        names = {"@parse": "rs:core::parse", "@shared": "rs:core::shared_fmt", "@api": "ts:web/api", "@button-test": "ts:web/button.test", "@both": "rs:core::both",
                 "@legacy": "ts:legacy/old"}
        return sid[names[token]]

    def resolve_token(container, token, array_name):
        if not token.startswith("@"):
            return int(token) if isinstance(container, list) else token
        if array_name == "owners":
            return next(i for i, o in enumerate(container) if o["ownerKey"] == keys[token[1:]])
        if array_name == "cells":
            a, b = token[1:].split("-")
            return next(i for i, r in enumerate(container) if (r["fromOwnerKey"], r["toOwnerKey"]) == (keys[a], keys[b]))
        if array_name == "drilldown":
            a, b = token[len("@drill-"):].split("-")
            return next(i for i, r in enumerate(container) if (r["fromOwnerKey"], r["toOwnerKey"]) == (keys[a], keys[b]))
        if array_name == "metrics":
            return next(i for i, r in enumerate(container) if r["subjectId"] == sid["rs:core::parse"] and r["metricId"] == "resolved-call-facts-incoming")
        if array_name in ("traces", "testReachability"):
            return next(i for i, r in enumerate(container) if r["subjectId"] == subject_alias(token))
        if array_name == "testOrigins":
            return next(i for i, r in enumerate(container) if r["universe"] == {"@rust": builder.UR, "@web": builder.UW}[token])
        raise AssertionError(token)

    def resolve_value(value, current, target_row):
        if isinstance(value, dict):
            return {k: resolve_value(v, None, target_row) for k, v in value.items()}
        if isinstance(value, list):
            return [resolve_value(v, None, target_row) for v in value]
        if not isinstance(value, str) or not value.startswith("@"):
            return copy.deepcopy(value)
        if value in ("@lodash", "@web"):
            return keys[value[1:]]
        if value == "@unknown-row":
            return {k: target_row[k] for k in ("subjectId", "metricId", "interpretation", "request", "response")} | {"countState": "unknown", "cause": "native-evidence-unavailable"}
        if value == "@core-lib-unit":
            return [t["unitId"] for t in owners_by_key[keys["core"]]["cargoTargets"] if t["targetKind"] == "lib"]
        if value == "@shared-subject":
            return sid["rs:core::shared_fmt"]
        if value == "@reversed":
            return list(reversed(current))
        raise AssertionError(value)

    def mutate(doc, ops):
        out = copy.deepcopy(doc)
        for op in ops:
            tokens = op["path"].strip("/").split("/")
            node, array_name = out, None
            for token in tokens[:-1]:
                key = resolve_token(node, token, array_name)
                array_name = token if isinstance(node, dict) else array_name
                node = node[key]
            last = resolve_token(node, tokens[-1], array_name if isinstance(node, list) else None)
            if op["op"] == "remove":
                del node[last]
            elif op["op"] == "resort":
                node[last].sort(key=lambda r: tuple(r[k].encode() for k in op["by"]))
            elif op["op"] == "add":
                assert last not in node
                node[last] = resolve_value(op["value"], None, None)
            else:
                current = node[last] if (isinstance(node, list) or last in node) else None
                node[last] = resolve_value(op["value"], current, current)
        return out

    def document_outcome(panel_name, doc, w, resolution):
        if panel_name == "coupling":
            return V.run(lambda: (V.schema(RID + "#/$defs/CouplingPanelV1", doc), M.admit_coupling(doc, w.run_id)))
        return V.run(lambda: (V.schema(RID + "#/$defs/SymbolEvidencePanelV1", doc), M.admit_symbol_evidence(doc, ctx(w, resolution))))

    doc_results = {}
    for case in fixture["documentCases"]:
        doc = mutate(panels[case["base"]][case["panel"]], case["ops"])
        got = document_outcome(case["panel"], doc, worlds[case["base"]], resolutions["mixed"])
        doc_results[case["id"]] = got
        assert got == case["expect"], (case["id"], got, case["expect"])
    report["documentCases"] = {"count": len(doc_results), "byCode": {c: sorted(k for k, v in doc_results.items() if v == c) for c in sorted(set(doc_results.values()))}}

    # 8. recognition parameter owner-record cases
    base_record = worlds["mixed"].recognition["record"]
    rec_results = {}
    for case in fixture["recognitionCases"]:
        record = mutate(base_record, case["ops"])
        if case["rehash"]:
            for row in record["units"]:
                row["recognitionId"] = M.native_h(M.RECOGNITION_DOMAIN, row["recognition"])
        got = V.run(lambda: (V.schema("opensip.product.framework-recognition-plan.1", record), M.admit_recognition_plan(worlds["mixed"], record)))
        rec_results[case["id"]] = got
        assert got == case["expect"], (case["id"], got, case["expect"])
    report["recognitionCases"] = rec_results

    # 9. host derivation cases: an unlawful attribution builds an internally consistent document; only the host derivation refuses it
    host_results = {}
    for case in fixture["hostCases"]:
        w = worlds["mixed"] if "world" not in case else world(case["world"])
        lawful_c, lawful_e = build_panels(w, resolutions["mixed"])
        if case["feature"] == "coupling":
            doc = M.derive_coupling(w, key_resolver=builder.RESOLVERS[case["resolver"]], test_origin_state=M.test_origin_state_fn(w))
            browser = document_outcome("coupling", doc, w, resolutions["mixed"])
            lawful, sections = lawful_c, [("owners", "J-COUPLING-OWNER"), ("cells", "J-COUPLING-OWNER"), ("importerBuckets", "J-COUPLING-BUCKET"), ("targetBuckets", "J-COUPLING-BUCKET")]
        else:
            doc = M.derive_symbol_evidence(w, resolutions["mixed"], BIG, start_resolver=builder.START_RESOLVERS.get(case["resolver"]),
                                           name_resolver=builder.ORIGIN_RESOLVERS.get(case["resolver"]))
            browser = document_outcome("symbolEvidence", doc, w, resolutions["mixed"])
            lawful, sections = lawful_e, [("traces", "J-TRACE-ENTRY"), ("testOrigins", "J-TR-ORIGIN"), ("testReachability", "J-TR-ORIGIN")]
        if browser == "accept":
            got = next((code for key, code in sections if doc[key] != lawful[key]), "accept")
        else:
            got = browser
        host_results[case["id"]] = {"browserAdmission": browser, "outcome": got}
        assert got == case["expect"], (case["id"], browser, got, case["expect"])
    assert all(v["browserAdmission"] == "accept" for k, v in host_results.items() if k.startswith(("coupling-", "trace-"))), host_results
    report["hostCases"] = host_results

    # 10. report integration: subject-05 audit-full with the successor panels under the patched schema
    s05_base = copy.deepcopy(s05_fixtures["bases"]["audit-full"])
    before_states = [f["featureId"] for f in s05_base["featureStates"]]
    s05_base["featureStates"] = [f for f in s05_base["featureStates"] if f["featureId"] not in REMOVED]
    s05_base["panels"]["coupling"] = {"state": "present", "data": panels["integration"]["coupling"]}
    s05_base["panels"]["symbolEvidence"] = {"state": "present", "data": panels["integration"]["symbolEvidence"]}
    V.schema(RID, s05_base)
    graph_resolution = s05_base["panels"]["graph"]["data"]["subjectResolution"]
    ictx = {"projectId": s05_base["envelope"]["projectId"], "runId": s05_base["envelope"]["run"]["runId"], "resolution": resolutions["integration"],
            "graphResolution": graph_resolution, "bounds": M.PUBLIC_BOUNDS}
    M.admit_symbol_evidence(s05_base["panels"]["symbolEvidence"]["data"], ictx)
    M.admit_coupling(s05_base["panels"]["coupling"]["data"], ictx["runId"])
    retained = copy.deepcopy(s05_base)
    retained["featureStates"] = sorted(retained["featureStates"] + [{"featureId": "symbol-metrics", "view": "symbol-detail", "state": "unavailable",
                                                                    "reason": "no-admitted-owner", "obligationId": "RP-DO-09"}], key=lambda f: f["featureId"].encode())
    mismatch = copy.deepcopy(ictx)
    mismatch["resolution"] = resolutions["integration"][:-1]
    M.admit_panel_prerequisites(s05_base["panels"])
    no_graph = copy.deepcopy(s05_base["panels"])
    no_graph["graph"] = {"state": "omitted", "reason": "exploration-budget-exceeded"}
    prerequisite = V.run(lambda: M.admit_panel_prerequisites(no_graph))
    lawful_absent = copy.deepcopy(no_graph)
    lawful_absent["symbolEvidence"] = {"state": "unavailable", "reason": "prerequisite-panel-not-present"}
    M.admit_panel_prerequisites(lawful_absent)
    assert prerequisite == "J-SE-PREREQUISITE"
    exploration = len(ref.canonical(s05_base["panels"]["coupling"])) + len(ref.canonical(s05_base["panels"]["symbolEvidence"]))
    integration = {"auditFullWithSuccessorPanels": "accept", "removedFeatureStateStillListed": V.run(lambda: V.schema(RID, retained)),
                   "subjectsNotGraphPanelSubjects": V.run(lambda: M.admit_symbol_evidence(s05_base["panels"]["symbolEvidence"]["data"], mismatch)),
                   "featureStatesBefore": before_states, "featureStatesAfter": [f["featureId"] for f in s05_base["featureStates"]],
                   "successorPanelsCanonicalBytes": exploration}
    assert integration["removedFeatureStateStillListed"] == "SCHEMA" and integration["subjectsNotGraphPanelSubjects"] == "J-SE-SUBJECTS" and exploration <= BIG
    report["integration"] = integration

    # 11. register, parent obligations and requirement text
    register = owners["owner/evidence-design-successor.v1.json"]
    obligations = {o["id"]: o for o in json.loads(s05("owner/design-obligations.v1.json"))["obligations"]}
    coverage = json.loads(s05("owner/implementation-coverage-successor.v1.json"))
    for row in register["obligations"]:
        assert obligations[row["id"]]["featureId"] == row["featureId"] and obligations[row["id"]]["blocksReportDesignReadiness"] is True
        issue = coverage["reviewIssueAdditions"][int(row["coverageIssue"].rsplit("/", 1)[1])]
        assert issue["id"] == row["id"] and row["deliveredCarrier"].split("/")[-1] in patched["$defs"]
    assert sorted(r["featureId"] for r in register["obligations"]) == REMOVED and register["remainingBlockers"] == []
    for ref_row in [r for rows_ in register["featureMapSuccessor"].values() for r in rows_]:
        assert ref.equal_typed(pointer_parent(patched, ref_row["ref"])[0] is not None, True)
    flat = lambda text: " ".join(text.split())
    inventory_md = (arch / "docs/v2/architecture/prototype-report-inventory.md").read_text()
    requirement_text = {}
    for row_id in ("R07", "R08", "R12"):
        section = inventory_md.split("### " + row_id + " ", 1)[1].split("\n### ", 1)[0]
        requirement_text[row_id] = sha(section.encode())
    for sentence in ("Bind metrics and test reachability to the exact universe/identity and show unknown values",
                     "a blank cell is not a global no-dependency proof", "Replace browser entry-point heuristics"):
        assert flat(sentence) in flat(inventory_md), sentence
    native_md = flat((arch / "docs/v2/contracts/product-v1/native-evidence.md").read_text())
    for sentence in ("explicit configuration wins and sets `entryPoints.source=explicit`", "**FR-5** A recognizer version change is a Plan-visible change.",
                     "**`WorkspaceUnitV2` and `UnitMembershipV1` cannot supply this binding**", "never a prefix, never a nearest directory, never a first match"):
        assert flat(sentence) in native_md, sentence
    query_md = flat((arch / "docs/coop/design-corrections/workflows/query-projection-contract.v3.md").read_text())
    for sentence in ("Zero neighbor rows is not “no callers.”", "The host MUST NOT parse `SubjectIdV1` `namespace:opaque` spelling"):
        assert flat(sentence) in query_md, sentence
    workflows_md = flat((arch / "docs/v2/contracts/product-v1/workflows-and-surfaces.md").read_text())
    assert flat("— evidence, never Coverage and never a verdict") in workflows_md
    report["register"] = {"obligations": [r["id"] for r in register["obligations"]], "ownerSuccessors": [s["id"] for s in register["ownerSuccessors"]],
                          "integrationDuties": [d["id"] for d in register["integrationDuties"]], "remainingBlockers": register["remainingBlockers"],
                          "requirementSectionSha256": requirement_text}
    report["closureCounts"] = dict(closure.counts)
    report["limits"] = ["constructions following the cited laws, not the product engine, store, provider or browser",
                        "owner successors S1-S4 are proposals; no owner accepted them",
                        "no runtime, browser, generator, Run replay or performance evidence"]
    if args.trace_closure:
        # The hook stays installed for the process lifetime, so the trace is returned in memory (seal.py reads TRACE_RESULT) rather than re-read from disk.
        global TRACE_RESULT
        files = []
        for path in sorted(closure.files):
            with open(path, "rb") as handle:
                raw = handle.read()
            files.append({"path": path, "sha256": sha(raw), "bytes": len(raw)})
        TRACE_RESULT = {"files": files, "directoryListings": [{"path": d, "entriesSha256": closure.listing_digest(d)} for d in sorted(closure.directories)]}
        print("traced", len(files), "files")
        return
    if args.out:
        report["declaredOutWritesNote"] = "this result cannot count its own write; the run prints the observed count after writing"
        with open(args.out, "w") as handle:
            handle.write(json.dumps(report, indent=1, ensure_ascii=False) + "\n")
        assert closure.counts["declaredOutWrites"] == 1
        print("declared-out writes observed:", closure.counts["declaredOutWrites"])
    print(json.dumps({k: report[k] for k in ("documentCases", "recognitionCases", "hostCases", "variants")}, indent=1)[:6000])
    print("CHECK OK")


if __name__ == "__main__":
    main()
