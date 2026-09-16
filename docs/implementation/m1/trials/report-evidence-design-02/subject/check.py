"""Reference check of the author-02 report evidence design candidate (RP-DO-03/05/09/10); not approval, runtime, browser, generator or Run replay qualification.

Run from the candidate directory or an exact copy of the listed subject files, from any cwd:
  TMPDIR=<existing absolute scratch> /tmp/opensip-implementation/metadata-reference-env/bin/python -I -B <copy>/check.py \
      --architecture /Users/sb/code/opensip-ai/opensip_arch --subject-strict [--out <absolute RESULT.json>]
Closure (enforced): governed reads (architecture checkout and /tmp/opensip-implementation outside this directory and the reference environment) must be
pinned and are re-hashed at open; listings must be pinned; open/listing events without an absolute path are refused; executed modules compile from verified
bytes (pinned sources, or overlay bytes this run wrote from pinned bytes plus the published successor transforms); writes are refused except the declared
--out (write-only); child processes are refused. The host, interpreter and reference environment are trusted.
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
import stat
import struct
import sys
import tempfile
import time
import types
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.pycache_prefix = "/nonexistent-opensip-report-evidence-02-pycache"
ENV_DIR = "/tmp/opensip-implementation/metadata-reference-env"
ORIGINAL_GET_CODE = importlib.machinery.SourceFileLoader.get_code
PARENT07 = "/tmp/opensip-implementation/m1-report-projection-subject-07"
PARENT07_MANIFEST = "/tmp/opensip-implementation/m1-report-projection-subject-07.json"
PARENT07_MANIFEST_SHA256 = "cee1eb24159187c3dc967493046eb08e2f86e242ed55eab23fe944c2cd43e6c8"
SUBJECT01_MANIFEST = "/tmp/opensip-implementation/m1-report-evidence-design-subject-01.json"
SUBJECT01_MANIFEST_SHA256 = "0af84231305e54ec218a5efeff4f0489b02f9dc69ade0c6101c632c96ffaaa11"
REVIEW01_JSON = "/tmp/opensip-implementation/m1-report-evidence-design-review-01/review.json"
RID = "urn:opensip:product-v1:workflows:evaluator3:report-projection:1"
GQ = "urn:opensip:product-v1:workflows:evaluator3:graph-query:3#/$defs/"
N = "urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/"
CHILD_EVENTS = ("subprocess.Popen", "os.system", "os.exec", "os.posix_spawn", "os.spawn", "os.fork", "os.forkpty", "pty.spawn")
REMOVED = ["coupling-importer-package-membership", "entry-point-recognition", "symbol-metrics", "test-reachability"]
BIG = 4194304
TRACE_RESULT = None


def norm(path):
    p = os.path.abspath(os.fsdecode(path))
    return p[len("/private"):] if p.startswith("/private/tmp/") else p


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


class Closure:
    def __init__(self, arch, trace, out):
        self.roots = [norm(arch), "/tmp/opensip-implementation"]
        self.excluded = [norm(HERE), ENV_DIR]
        self.trace, self.out = trace, (norm(out) if out else None)
        self.scratch = []
        self.overlay = {}
        self.files, self.directories = set(), set()
        self.pinned, self.listings, self.pinned_inodes, self.listing_inodes = {}, {}, {}, {}
        self.busy = False
        self.counts = {"rehashedOpens": 0, "listingRecomputes": 0, "verifiedSourceCompiles": 0, "verifiedOverlayCompiles": 0, "declaredOutWrites": 0}

    @staticmethod
    def under(path, root):
        p, r = path.casefold(), root.casefold()
        return p == r or p.startswith(r + "/")

    def in_scratch(self, path):
        return any(self.under(path, s) for s in self.scratch)

    def governed(self, path):
        spellings = {path, norm(os.path.realpath(path))}
        if any(self.in_scratch(p) for p in spellings):
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
        if self.in_scratch(path):
            expected = self.overlay.get(path)
            if expected is None or sha(data) != expected:
                raise RuntimeError("OVERLAY-SOURCE-UNVERIFIED " + path)
            self.counts["verifiedOverlayCompiles"] += 1
            return
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
        target = args[0] if args else None
        if not isinstance(target, (str, bytes, os.PathLike)) or not os.path.isabs(os.fsdecode(target)):
            raise RuntimeError("UNATTRIBUTABLE-PATH-EVENT %s %r" % (event, target))
        path = norm(target)
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
        if closure.governed(norm(self.get_filename(fullname))) or closure.in_scratch(norm(self.get_filename(fullname))):
            raise ImportError("BYTECODE-ONLY-MODULE-REFUSED " + self.get_filename(fullname))
        return original_sourceless(self, fullname)
    importlib.machinery.SourceFileLoader.get_code = get_code
    importlib.machinery.SourcelessFileLoader.get_code = sourceless


def remove_owned_tree(path):
    """Absolute scandir, lstat kind, unlink/rmdir; no symlink following and no dir_fd-relative opens."""
    info = os.lstat(path)
    if stat.S_ISDIR(info.st_mode):
        with os.scandir(path) as entries:
            children = [os.path.join(path, e.name) for e in entries]
        for child in children:
            remove_owned_tree(child)
        os.rmdir(path)
    else:
        os.unlink(path)


def bytecode_demo(closure, scratch_root):
    directory = norm(tempfile.mkdtemp(prefix="opensip-rev02-pyc-", dir=scratch_root))
    closure.scratch.append(directory)
    saved = sys.pycache_prefix
    try:
        source = os.path.join(directory, "mod.py")
        with open(source, "w") as handle:
            handle.write('VALUE = "verified-source"\n')
        st = os.stat(source)
        cache = os.path.join(directory, "__pycache__", "mod." + sys.implementation.cache_tag + ".pyc")
        os.makedirs(os.path.dirname(cache))
        with open(cache, "wb") as handle:
            handle.write(importlib.util.MAGIC_NUMBER + struct.pack("<III", 0, int(st.st_mtime) & 0xFFFFFFFF, st.st_size & 0xFFFFFFFF)
                         + marshal.dumps(compile('VALUE = "stale-bytecode"\n', source, "exec")))
        sys.pycache_prefix = None
        closure.overlay[source] = sha(b'VALUE = "verified-source"\n')
        stock, enforced = {}, {}
        exec(ORIGINAL_GET_CODE(importlib.machinery.SourceFileLoader("rev02_stock", source), "rev02_stock"), stock)
        exec(importlib.machinery.SourceFileLoader("rev02_enforced", source).get_code("rev02_enforced"), enforced)
    finally:
        sys.pycache_prefix = saved
        remove_owned_tree(directory)
        closure.scratch.remove(directory)
    assert stock["VALUE"] == "stale-bytecode" and enforced["VALUE"] == "verified-source"
    return {"stockLoaderWithAdjacentCache": stock["VALUE"], "enforcedLoader": enforced["VALUE"]}


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def load_text(closure, name, path, text):
    raw = text.encode("utf-8")
    closure.overlay[norm(path)] = sha(raw)
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    module.__file__ = str(path)
    sys.modules[name] = module
    closure.verify_source(str(path), raw)
    exec(compile(raw, str(path), "exec", dont_inherit=True), module.__dict__)
    return module


def unescape(token):
    return token.replace("~1", "/").replace("~0", "~")


def pointer_parent(doc, path):
    tokens = [unescape(t) for t in path.strip("/").split("/")]
    node = doc
    for token in tokens[:-1]:
        node = node[int(token)] if isinstance(node, list) else node[token]
    return node, tokens[-1]


def resolve_pointer(doc, path):
    node = doc
    for token in [unescape(t) for t in path.strip("/").split("/")]:
        if isinstance(node, dict) and token in node:
            node = node[token]
        elif isinstance(node, list) and token.isdigit() and int(token) < len(node):
            node = node[int(token)]
        else:
            raise KeyError(path)
    return node


class PatchRefused(Exception):
    pass


def apply_semantic(doc, ops):
    """The published operation law (report patch operationLaw): preconditions on the CURRENT document; any failure refuses the whole patch."""
    out = copy.deepcopy(doc)
    for op in ops:
        parent, key = pointer_parent(out, op["path"])
        if op["op"] == "remove-members":
            if "selectorGuard" in op:
                try:
                    guard = resolve_pointer(out, op["selectorGuard"]["path"])
                except KeyError:
                    raise PatchRefused("SELECTOR-GUARD " + op["path"])
                if guard != op["selectorGuard"]["equals"]:
                    raise PatchRefused("SELECTOR-GUARD " + op["path"])
            if key not in parent if isinstance(parent, dict) else False:
                raise PatchRefused("PATH " + op["path"])
            ident = (lambda r: r[op["key"]]) if "key" in op else (lambda r: r)
            rows = parent[key]
            for member in op["members"]:
                if sum(1 for r in rows if ident(r) == member) != 1:
                    raise PatchRefused("PRECONDITION member-not-present-once %s %s" % (op["path"], member))
            parent[key] = [r for r in rows if ident(r) not in op["members"]]
        elif op["op"] == "insert-members-after":
            rows = parent[key]
            if rows.count(op["anchor"]) != 1 or any(m in rows for m in op["members"]):
                raise PatchRefused("PRECONDITION anchor-or-members " + op["path"])
            index = rows.index(op["anchor"]) + 1
            parent[key] = rows[:index] + list(op["members"]) + rows[index:]
        elif op["op"] == "add":
            if key in parent:
                raise PatchRefused("PRECONDITION present " + op["path"])
            parent[key] = copy.deepcopy(op["value"])
        else:
            raise PatchRefused("UNKNOWN-OP " + op["op"])
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
        except (self.ValidationError, self.ref.AdmissionError):
            return "SCHEMA"


def main():
    global TRACE_RESULT
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--architecture", required=True, type=Path)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--trace-closure", action="store_true")
    parser.add_argument("--subject-strict", action="store_true")
    args = parser.parse_args()
    for name in ("architecture", "out"):
        value = getattr(args, name)
        if value is not None and not value.is_absolute():
            setattr(args, name, Path(os.path.abspath(value)))
    arch = args.architecture
    started = time.time()
    report = {"standing": "AUTHOR-02 candidate reference check; not approval, runtime, browser, generator, performance or Run replay qualification"}
    scratch_root = os.environ.get("TMPDIR", "")
    assert os.path.isabs(scratch_root) and os.path.isdir(scratch_root), "set TMPDIR to an existing absolute scratch directory"
    closure = Closure(arch, trace=args.trace_closure, out=args.out)
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
    probes = {}
    if not args.trace_closure:
        # strict mode only: a trace run records every governed open, so probing there would pin the unpinned target the probe must be refused
        head, tail = norm(arch).rsplit("/", 1)
        for label, alias in {"exact": norm(arch) + "/docs/implementation/README.md", "case-variant": head + "/" + tail.upper() + "/docs/implementation/README.md",
                             "dot-dot": norm(arch) + "/docs/implementation/m1/../README.md", "relative": "docs/implementation/README.md"}.items():
            try:
                with open(alias, "rb"):
                    probes[label] = "READ-NOT-REFUSED"
            except RuntimeError as exc:
                probes[label] = str(exc).split(" ")[0]
            except OSError as exc:
                probes[label] = "OSERROR-" + type(exc).__name__
        assert probes == {"exact": "UNPINNED-LOAD", "case-variant": "UNPINNED-LOAD", "dot-dot": "UNPINNED-LOAD", "relative": "UNATTRIBUTABLE-PATH-EVENT"}, probes
    report["aliasProbe"] = probes

    from jsonschema import Draft202012Validator, ValidationError
    from referencing import Resource
    from referencing.jsonschema import DRAFT202012

    # 1. immutable parents and prior subject
    p07_raw = Path(PARENT07_MANIFEST).read_bytes()
    assert sha(p07_raw) == PARENT07_MANIFEST_SHA256, "parent07 outer manifest drift"
    p07_files = {row["path"]: row for row in json.loads(p07_raw)["files"]}

    def p07(name):
        raw = Path(PARENT07 + "/" + name).read_bytes()
        assert sha(raw) == p07_files[name]["sha256"] and len(raw) == p07_files[name]["bytes"], "parent07 file drift " + name
        return raw
    assert sha(Path(SUBJECT01_MANIFEST).read_bytes()) == SUBJECT01_MANIFEST_SHA256, "subject01 outer manifest drift"
    review = json.loads(Path(REVIEW01_JSON).read_bytes())
    assert review["decision"] == "changes-required" and [f["id"] for f in review["findings"]] == ["F%d" % i for i in range(1, 10)]
    report["parents"] = {"parent07ManifestSha256": PARENT07_MANIFEST_SHA256, "subject01ManifestSha256": SUBJECT01_MANIFEST_SHA256, "review01Findings": 9}
    cm = load("check_metadata_v2", arch / "docs/implementation/m1/metadata-v2/check_metadata.py")
    ref, registry, documents = cm.load(arch)
    canonical = load("foundation_canonical", arch / "docs/coop/design-corrections/foundation/canonical.py")
    p07("report_model.py")
    RM = load("parent07_report_model", Path(PARENT07) / "report_model.py")
    NM = load("native_model_v2", arch / "docs/coop/design-corrections/native/native_evidence_model.v2.py")
    M = load("evidence_reference_model", HERE / "reference_model.py")
    M.bind(canonical, RM)
    bridge = load("evidence_identity_bridge", HERE / "identity_bridge.py")
    owner = load("evidence_build_owner", HERE / "build_owner.py")
    builder = load("evidence_build_fixtures", HERE / "build_fixtures.py")

    # 2. byte-identical regeneration
    owners = owner.build(arch, M, bridge)
    for name, value in owners.items():
        assert owner.dump(value) == (HERE / name).read_bytes(), "owner drift " + name
    p07_fixtures = json.loads(p07("fixtures.json"))
    fixture = builder.build(M, NM, p07_fixtures)
    fixture_raw = owner.dump(fixture)
    assert fixture_raw == (HERE / "fixtures.json").read_bytes(), "fixtures drift"
    report["regeneration"] = {"ownerFiles": sorted(owners), "fixturesSha256": sha(fixture_raw)}

    # 3. owner schema admission and semantic patch composition (F5)
    for extra in ("docs/coop/design-corrections/foundation/enumeration-plan.schema.v1.json", "docs/coop/design-corrections/foundation/subject-inventory.schema.v1.json"):
        doc = ref.parse((arch / extra).read_bytes())
        documents[doc["$id"]] = doc
        registry = registry.with_resource(doc["$id"], Resource(contents={k: v for k, v in doc.items() if k != "$schema"}, specification=DRAFT202012))
    parameter_raw = (HERE / "owner/framework-recognition-plan.schema.v1.json").read_bytes()
    parameter_sha = sha(parameter_raw)
    parameter = ref.parse(parameter_raw)
    Draft202012Validator.check_schema(parameter)
    native = documents["urn:opensip:product-v1:native:evidence-schemas:v2"]
    for name in ("FrameworkRecognitionV1", "FrameworkRecognitionResultV1", "EntryPointRecognitionV1", "InternalUnitRootV1"):
        assert ref.equal_typed(parameter["$defs"][name], native["$defs"][name]), "parameter copy drift " + name
    assert not re.findall(r'"\$ref":\s*"(?!#)', parameter_raw.decode())
    registry = registry.with_resource(parameter["$id"], Resource(contents={k: v for k, v in parameter.items() if k != "$schema"}, specification=DRAFT202012))
    for name in ("owner/command-envelope.v5.schema.json", "owner/command-inventory.v5.schema.json"):
        doc = ref.parse(p07(name))
        documents[doc["$id"]] = doc
        registry = registry.with_resource(doc["$id"], Resource(contents={k: v for k, v in doc.items() if k != "$schema"}, specification=DRAFT202012))
    patch = owners["owner/report-projection-successor-patch.v2.json"]
    parent_raw = p07("report-projection.schema.json")
    assert patch["parent"]["sha256"] == sha(parent_raw) and patch["parent"]["subjectManifestSha256"] == PARENT07_MANIFEST_SHA256
    parent = ref.parse(parent_raw)
    patched = apply_semantic(parent, patch["ops"])
    Draft202012Validator.check_schema(patched)
    for index, branch in enumerate(patched["allOf"]):
        states = branch.get("then", {}).get("properties", {}).get("featureStates", {}).get("const")
        if states is not None:
            assert not {s["featureId"] for s in states} & set(REMOVED)
    assert patched["$defs"]["BudgetProfileV1"]["properties"]["projectionPriority"]["const"] == ["comparison", "catalog", "evidence", "graph", "history", "symbolEvidence", "coupling"]
    # a real second obligation (RP-DO-11 stand-in: remove step-duration everywhere it occurs) through the same applier, both orders
    other = [{"op": "remove-members", "path": "/$defs/FeatureId/enum", "members": ["step-duration"], "precondition": "each-member-present-exactly-once"}]
    for index, branch in enumerate(parent["allOf"]):
        states = branch.get("then", {}).get("properties", {}).get("featureStates", {}).get("const")
        if states is not None and any(s["featureId"] == "step-duration" for s in states):
            other.append({"op": "remove-members", "path": "/allOf/%d/then/properties/featureStates/const" % index, "key": "featureId", "members": ["step-duration"],
                          "selectorGuard": {"path": "/allOf/%d/if/properties/command/const" % index, "equals": branch["if"]["properties"]["command"]["const"]}})
    first = apply_semantic(apply_semantic(parent, patch["ops"]), other)
    second = apply_semantic(apply_semantic(parent, other), patch["ops"])
    assert first == second, "patch composition order-dependent"
    refusals = {}
    for label, fn in (("thisPatchTwice", lambda: apply_semantic(patched, patch["ops"])),
                      ("otherObligationClaimsThisMember", lambda: apply_semantic(patched, [dict(other[0], members=["symbol-metrics"])])),
                      ("insertAnchorMissing", lambda: apply_semantic(parent, [dict(next(o for o in patch["ops"] if o["op"] == "insert-members-after"), anchor="nonexistent")])),
                      ("selectorGuardWrongCommand", lambda: apply_semantic(parent, [dict(other[1], selectorGuard=dict(other[1]["selectorGuard"], equals="repair-preview"))]))):
        try:
            fn()
            refusals[label] = "APPLIED"
        except PatchRefused as exc:
            refusals[label] = str(exc).split(" ")[0]
    assert all(v in ("PRECONDITION", "SELECTOR-GUARD") for v in refusals.values()), refusals
    registry = registry.with_resource(RID, Resource(contents={k: v for k, v in patched.items() if k != "$schema"}, specification=DRAFT202012))
    documents[RID] = patched
    for doc in (patched, parameter):
        for target in re.findall(r'"\$ref":\s*"([^"#]+)', json.dumps(doc)):
            assert target in documents, "unregistered " + target
    report["ownerAdmission"] = {"parameterSchemaSha256": parameter_sha, "reportPatchOps": len(patch["ops"]), "patchedReportCanonicalSha256": sha(ref.canonical(patched)),
                                "compositionBothOrdersIdentical": True, "otherObligationOps": len(other), "preconditionRefusals": refusals, "nativeCopiesDriftChecked": 4}

    # 4. F1 identity successor bridge over real retained evaluator3 Runs
    overlay_root = norm(tempfile.mkdtemp(prefix="opensip-rev02-identity-", dir=scratch_root))
    closure.scratch.append(overlay_root)
    try:
        written = bridge.build_overlay(arch, Path(overlay_root), parameter_raw)
        for rel, digest in written.items():
            closure.overlay[norm(os.path.join(overlay_root, rel))] = digest
        DCF = Path(overlay_root) / bridge.DC / "foundation"
        pred = types.SimpleNamespace(F=load("pred_graph_fixture", arch / bridge.DC / "foundation/evaluator_graph_fixture.v3.py"),
                                     R=load("pred_replay", arch / bridge.DC / "foundation/evaluator_replay_model.v3.py"))
        fixture_text = bridge.transform((arch / bridge.DC / "foundation/evaluator_graph_fixture.v3.py").read_text(), bridge.FIXTURE_TRANSFORMS)
        succ = types.SimpleNamespace(Fx=load_text(closure, "succ_graph_fixture", DCF / "evaluator_graph_fixture.v3.py", fixture_text),
                                     R=load("succ_replay", DCF / "evaluator_replay_model.v3.py"))
        demo = bridge.demonstrate(pred, succ, M, parameter_sha)
    finally:
        remove_owned_tree(overlay_root)
        closure.scratch.remove(overlay_root)
    assert demo["predecessorRunClosedByPinnedModel"]["result"] == "admitted" and demo["predecessorRunClosedBySuccessorModel"] == demo["predecessorRunClosedByPinnedModel"]
    assert demo["predecessorRunCustody"] == {"state": "not-plan-bound"} and demo["predecessorRunParameters"] == 2
    assert demo["newPlanRunClosedBySuccessorModel"]["result"] == "admitted" and demo["planIdsDiffer"]
    assert demo["newPlanRunCustody"]["state"] == "plan-bound" and demo["newPlanRunCustodyWhenParameterPurged"]["availability"] == "purged"
    assert demo["newPlanRunCustodyPartialMissing"]["state"] == "unavailable"
    assert demo["newPlanRunClosedByPinnedPredecessorModel"]["code"].startswith("AdmissionError:PAYLOAD_PARAMETER_UNREGISTERED:" + parameter_sha)
    assert demo["newPlanRunWithParameterBytesLost"]["code"].startswith("EvidenceUnavailable:EVIDENCE_UNAVAILABLE:")
    assert demo["duty"]["syntaxOnlySpecWithoutParameter"]["result"] == "admitted" and demo["duty"]["compilerSpecWithParameter"]["result"] == "admitted"
    assert demo["duty"]["compilerSpecWithoutParameter"]["code"].startswith("Refusal:NEW_PLAN_RECOGNITION_PARAMETER_REQUIRED")
    assert demo["duty"]["compilerSpecWithTwoParameters"]["code"].startswith("AdmissionError:ANALYSIS_SPEC_PARAMETER_SELECTION_AMBIGUOUS")
    assert demo["successorRegistryRowOptional"]
    report["identityBridge"] = demo

    # 5. glob law
    contract = (arch / "docs/coop/design-corrections/foundation/glob-pattern-contract.v1.md").read_text()
    table = contract.split("## Required examples", 1)[1].split("##", 1)[0]
    examples = []
    for line in table.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) == 3 and cells[2] in ("true", "false"):
            examples.append((re.findall(r"`([^`]*)`", cells[0])[0], re.findall(r"`([^`]*)`", cells[1])[0], cells[2] == "true"))
    tree = ast.parse((arch / "docs/coop/design-corrections/workflows/workflows_model.v1.py").read_bytes())
    fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "glob_match")
    namespace = {}
    exec(compile(ast.Module(body=[fn], type_ignores=[]), "workflows_model.v1.glob_match", "exec"), namespace)
    extra = [("**/*.test.*", "src/button.test.tsx", True), ("**/*.test.*", "src/helper.it.ts", False), ("src/**/*.test.ts", "packages/web/src/a.test.ts", False)]
    for pattern, candidate, expected in examples + extra:
        assert M.glob_match(pattern, candidate) == expected == namespace["glob_match"](pattern, candidate), (pattern, candidate)
    assert len(examples) == 22
    report["globLaw"] = {"contractExamples": 22, "extraExamples": len(extra), "agreesWithPinnedWorkflowsGlobMatch": True}

    # 6. worlds through the pinned native model
    V = Outcome(ref, registry, M, ValidationError)
    variants = builder.variants(M)
    descriptions = copy.deepcopy(fixture["descriptions"])
    world_data = {}

    def world(name):
        desc = copy.deepcopy(descriptions[name]) if name in descriptions else variants[name](copy.deepcopy(descriptions["mixed"]))
        data = builder.assemble(desc, M, NM, parameter_sha)
        V.schema(N + "UnitMembershipV1", data["membership"])
        V.schema("opensip.product.enumeration-plan.1", data["enumerationPlan"])
        for inv in data["subjectInventories"]:
            V.schema("opensip.product.subject-inventory.1", inv)
        for record in data["sourceUnitOwnership"].values():
            V.schema(N + "SourceUnitOwnershipV1", record)
        for record in data["rustUniverses"].values():
            V.schema(N + "RustUniverseV2ResolvedInputs", record)
        V.schema("opensip.product.framework-recognition-plan.1", data["recognitionRecord"])
        for result in data["nativeRecognition"].values():
            V.schema(N + "FrameworkRecognitionV1", result)
        if name != "dense-120":
            for f in data["facts"]:
                V.schema(GQ + "GraphEndpoint", f["source"])
                V.schema(GQ + "GraphEndpoint", f["target"])
        built = M.World(data)
        M.admit_recognition_plan(built, data["recognitionRecord"])
        world_data[name] = data
        return built

    worlds = {name: world(name) for name in ("mixed", "clean", "integration", "cross-universe-test", "jest-configured")}
    resolutions = fixture["resolutions"]
    mixed_data = world_data["mixed"]
    unit0 = mixed_data["membership"]["units"][0]
    native_root = mixed_data["nativeRecognition"][0]
    cargo = M.cargo_target_entries(worlds["mixed"], builder.UR)
    report["nativeModel"] = {
        "discoverUnitsCargoWorkspace": {k: unit0[k] for k in ("unitKind", "rootPath", "memberPackageRoots")},
        "pinnedRecognizerRootOnly": {"entryPoints": native_root["entryPoints"], "effects": sorted({p for r in native_root["recognized"] for p in r["effects"]["entryPoints"]})},
        "successorCargoTargetEntries": {"state": cargo["state"], "roots": sorted(t["crateRootPath"] for t in cargo["targets"])},
        "jestConfiguredNativeVsSuccessor": {"native": [r["unresolvedChoices"] for r in world_data["jest-configured"]["nativeRecognition"][0]["recognized"] if r["recognizerId"] == "vitest-jest"],
                                            "successor": [r["unresolvedChoices"] for u in world_data["jest-configured"]["recognitionRecord"]["units"] for r in u["recognition"]["recognized"] if r["recognizerId"] == "vitest-jest"]},
    }
    assert unit0["unitKind"] == "cargo-workspace" and unit0["memberPackageRoots"] == ["crates/app", "crates/core"]
    assert report["nativeModel"]["pinnedRecognizerRootOnly"] == {"entryPoints": {"state": "all", "source": "recognized"}, "effects": ["src/main.rs"]}
    assert report["nativeModel"]["successorCargoTargetEntries"] == {"state": "all", "roots": ["crates/app/src/main.rs", "crates/core/src/lib.rs", "src/main.rs"]}
    assert report["nativeModel"]["jestConfiguredNativeVsSuccessor"] == {"native": [[]], "successor": [["test-selection-configured"]]}

    def ctx(w, resolution, budget=BIG):
        return {"projectId": w.project_id, "runId": w.run_id, "resolution": resolution, "graphResolution": resolution, "bounds": M.PUBLIC_BOUNDS, "budget": budget}

    def build_panels(w, resolution, **kw):
        coupling = M.derive_coupling(w, budget=kw.get("budget", BIG), key_resolver=kw.get("key_resolver"), test_origin_state=M.test_origin_state_fn(w))
        evidence = M.derive_symbol_evidence(w, resolution, kw.get("budget", BIG), start_resolver=kw.get("start_resolver"), name_resolver=kw.get("name_resolver"))
        return coupling, evidence

    def admit_panels(w, resolution, coupling, evidence, budget=BIG):
        V.schema(RID + "#/$defs/CouplingPanelV1", coupling)
        M.admit_coupling(coupling, w.run_id, budget)
        V.schema(RID + "#/$defs/SymbolEvidencePanelV1", evidence)
        M.admit_symbol_evidence(evidence, ctx(w, resolution, budget))

    panels = {}
    for name, key in (("mixed", "mixed"), ("clean", "mixed"), ("integration", "integration"), ("cross-universe-test", "integration"), ("jest-configured", "integration")):
        c, e = build_panels(worlds[name], resolutions[key])
        admit_panels(worlds[name], resolutions[key], c, e)
        panels[name] = {"coupling": c, "symbolEvidence": e}

    # 7. positive expectations
    mc, me = panels["mixed"]["coupling"], panels["mixed"]["symbolEvidence"]
    keys = {}
    for o in mc["owners"]:
        alias = {"svc": "svc", "core": "core", "app": "app", "@fx/shared": "shared", "@fx/web": "web", "lodash": "lodash"}.get(o.get("packageName"))
        keys[alias or ("legacy" if o["keyKind"] == "workspace-unit" else None)] = o["ownerKey"]
    cell = {(r["fromOwnerKey"], r["toOwnerKey"]): r for r in mc["cells"]}
    counts = lambda a, b: tuple(cell[(keys[a], keys[b])][k] for k in ("facts", "programEdges", "sourceDependencies", "importerSymbols", "sharedImporterFacts"))
    expected_cells = {("app", "core"): (4, 3, 3, 2, 1), ("legacy", "web"): (2, 2, 1, 2, 0), ("core", "core"): (2, 2, 2, 2, 1), ("web", "shared"): (2, 2, 2, 1, 0),
                      ("shared", "web"): (1, 1, 1, 1, 0), ("web", "lodash"): (1, 1, 1, 1, 0), ("web", "web"): (1, 1, 1, 1, 0), ("svc", "app"): (1, 1, 1, 1, 0)}
    for pair, values in expected_cells.items():
        assert counts(*pair) == values, (pair, counts(*pair))
    assert len(mc["cells"]) == 8 and mc["cells"][0]["fromOwnerKey"] == keys["app"] and (keys["core"], keys["app"]) not in cell
    assert mc["totals"] == {"distinctFacts": 19, "attributedFacts": 13, "importerUnattributedFacts": 4, "targetUnattributedFacts": 2, "cellCount": 8, "cellFactSum": 14,
                            "targetBucketCount": 2, "ownerCount": 7, "importerSymbolPathOutsideAnchors": 1}
    assert mc["importerBuckets"] == [{"cause": "importer-anchor-owners-disagree", "facts": 1}, {"cause": "not-compiled-by-selected-targets", "facts": 2},
                                     {"cause": "owned-only-by-unselected-targets", "facts": 1}]
    assert mc["absence"] == {"blankCellMeans": "no-projected-fact", "absenceSupported": False, "blockers": ["evidence-limitations", "unattributed-importers", "unattributed-targets"]}
    assert panels["clean"]["coupling"]["absence"]["blockers"] == ["unattributed-importers"] or panels["clean"]["coupling"]["absence"]["absenceSupported"]
    ic = panels["integration"]["coupling"]
    assert ic["absence"] == {"blankCellMeans": "no-projected-fact", "absenceSupported": True, "blockers": []} and [c["facts"] for c in ic["cells"]] == [1, 1]
    sid = {e["endpoint"]["nativeSubjectId"]: e["subjectId"] for e in resolutions["mixed"] if e["state"] == "resolved"}
    metric = {(r["subjectId"], r["metricId"]): r for r in me["metrics"]}
    assert len(me["metrics"]) == 35 and me["metricsProjection"] == {"total": 35, "omitted": 0, "omissionCause": "none"}
    parse_in = metric[(sid["rs:core::parse"], "resolved-call-facts-incoming")]
    assert (parse_in["countState"], parse_in["value"], parse_in["zeroSupportsAbsence"]) == ("exact", 3, False)
    parse_out = metric[(sid["rs:core::parse"], "resolved-call-facts-outgoing")]
    assert (parse_out["countState"], parse_out["value"], parse_out["zeroSupportsAbsence"]) == ("exact", 0, True)
    trace = {t["subjectId"]: t for t in me["traces"]}
    states = {n: (trace[sid[n]]["state"], trace[sid[n]].get("blockers"), (trace[sid[n]].get("start") or {}).get("attributionPath")) for n in
              ("rs:core::parse", "rs:core::shared_fmt", "ts:web/api", "ts:web/button.test", "rs:core::both", "ts:legacy/old")}
    assert states == {"rs:core::parse": ("path-found", None, "crates/app/src/main.rs"), "rs:core::shared_fmt": ("path-found", None, "crates/app/src/main.rs"),
                      "ts:web/api": ("path-found", None, "packages/web/app/page.tsx"), "ts:web/button.test": ("no-entry-origin", ["entry-recognition-not-all"], None),
                      "rs:core::both": ("no-entry-origin", [], None), "ts:legacy/old": ("no-entry-origin", ["entry-recognition-not-all"], None)}, states
    assert trace[sid["rs:core::shared_fmt"]]["start"]["entry"]["provenance"][0]["source"] == "cargo-target"
    reach = {r["subjectId"]: r for r in me["testReachability"]}
    tstates = {n: (reach[sid[n]]["state"], reach[sid[n]].get("blockers"), ((reach[sid[n]].get("origin") or {}).get("endpoint") or {}).get("nativeSubjectId")) for n in
               ("rs:core::parse", "rs:core::shared_fmt", "ts:web/api", "ts:web/button.test", "rs:core::both", "ts:legacy/old")}
    assert tstates == {"rs:core::parse": ("static-path-from-test-origin", None, "rs:core::it_parses"), "rs:core::shared_fmt": ("not-found-incomplete", ["test-origin-set-partial"], None),
                       "ts:web/api": ("static-path-from-test-origin", None, "ts:web/button.test"), "ts:web/button.test": ("is-test-origin", None, None),
                       "rs:core::both": ("static-path-from-test-origin", None, "rs:core::it_parses"), "ts:legacy/old": ("unknown", None, None)}, tstates
    assert all(s["completeness"] in ("partial", "none") for s in me["testOrigins"])
    assert not any(r["state"] == "no-static-path-within-bound" for p in panels.values() for r in p["symbolEvidence"]["testReachability"])
    isid = {e["endpoint"]["nativeSubjectId"]: e["subjectId"] for e in resolutions["integration"] if e["state"] == "resolved"}
    cross = {r["subjectId"]: r for r in panels["cross-universe-test"]["symbolEvidence"]["testReachability"]}
    helper_cross = cross[isid["ts:src/helper.ts#helper"]]
    assert helper_cross["state"] == "static-path-from-test-origin" and helper_cross["origin"]["endpoint"]["universe"] == builder.UT
    jest = {r["subjectId"]: r for r in panels["jest-configured"]["symbolEvidence"]["testReachability"]}
    assert jest[isid["ts:src/helper.ts#helper"]]["state"] == "not-found-incomplete" and "test-origin-set-partial" in jest[isid["ts:src/helper.ts#helper"]]["blockers"]
    assert "test-selection-configured" in panels["jest-configured"]["symbolEvidence"]["testOrigins"][0]["limitations"]
    report["positive"] = {"mixedCells": 8, "mixedTotals": mc["totals"], "mixedTraceStates": states, "mixedTestStates": tstates,
                          "crossUniverseHelper": helper_cross["state"], "jestConfiguredHelper": jest[isid["ts:src/helper.ts#helper"]]["state"]}

    # 8. variants
    vr = {}

    def panels_for(name, resolution="mixed"):
        w = world(name)
        c, e = build_panels(w, resolutions[resolution])
        admit_panels(w, resolutions[resolution], c, e)
        return w, c, e
    w, c, e = panels_for("mixed-core-package-partial")
    vr["core-package-partial"] = {"importerBuckets": c["importerBuckets"], "targetBuckets": sorted(b["cause"] for b in c["targetBuckets"])}
    assert any(b["cause"] == "package-inventory-incomplete" for b in c["importerBuckets"]) and "package-inventory-incomplete" in vr["core-package-partial"]["targetBuckets"]
    core_manifest_key = M.owner_key({"keyKind": "first-party-package", "path": "crates/core/Cargo.toml"})
    assert not any(x["toOwnerKey"] == core_manifest_key or x["fromOwnerKey"] == core_manifest_key for x in c["cells"])
    for name, state, cause in (("mixed-not-plan-bound", {"state": "not-plan-bound"}, "recognition-not-plan-bound"),
                               ("mixed-recognition-purged", {"state": "unavailable", "availability": "purged"}, "recognition-unavailable"),
                               ("mixed-recognition-partial-missing", {"state": "unavailable", "availability": "partial"}, "recognition-unavailable")):
        w, c, e = panels_for(name)
        assert {k: v for k, v in e["entryRecognition"].items() if k != "parameterDigest"} == state
        assert {t["cause"] for t in e["traces"]} == {cause, "subject-descriptor-not-retained"}
        sets = {s["universe"]: s for s in e["testOrigins"]}
        assert sets[builder.UW]["source"] == "none" and sets[builder.UW]["cause"] == cause and sets[builder.UR]["source"] == "rust-test-targets"
        vr[name] = {"entryRecognition": state, "traceCause": cause, "custodyFromParameters": w.custody()}
    w, c, e = panels_for("mixed-recognition-partial-present")
    assert (e["entryRecognition"]["state"], e["entryRecognition"]["availability"]) == ("plan-bound", "partial")
    w, c, e = panels_for("mixed-no-reachability-view")
    assert {t["cause"] for t in e["traces"]} == {"reachability-evidence-unavailable", "subject-descriptor-not-retained"}
    w, c, e = panels_for("mixed-many-origins")
    assert {t["subjectId"]: t for t in e["traces"]}[sid["rs:core::both"]]["cause"] == "origin-page-set-not-embedded"
    w, c, e = panels_for("mixed-cargo-member-root-unresolved")
    cargo_entry = e["entryRecognition"]["cargoTargetEntries"][0]
    shared_trace = {t["subjectId"]: t for t in e["traces"]}[sid["rs:core::shared_fmt"]]
    assert (cargo_entry["state"], cargo_entry["missingCoverage"]) == ("partial", ["target-crate-root-unresolved"])
    assert (shared_trace["state"], shared_trace["blockers"]) == ("no-entry-origin", ["entry-recognition-not-all"])
    vr["cargo-member-root-unresolved"] = {"cargo": cargo_entry["missingCoverage"], "sharedFmtTrace": shared_trace["blockers"]}
    w, c, e = panels_for("mixed-whole-view-test-bound")
    assert c["projection"]["countBasis"] == "lower-bound" and "projection-lower-bound" in c["absence"]["blockers"] and c["totals"]["distinctFacts"] == 10
    assert "unexamined-work-bound" in c["projection"]["limitationKinds"]
    vr["whole-view-test-bound"] = {"countBasis": "lower-bound", "distinctFacts": 10}
    w, c, e = panels_for("mixed-zero-under-limitation")
    zero = {(r["subjectId"], r["metricId"]): r for r in e["metrics"]}[(sid["rs:core::parse"], "resolved-call-facts-outgoing")]
    assert (zero["countState"], zero["value"], zero["zeroSupportsAbsence"], zero["limitationKinds"]) == ("exact", 0, False, ["unresolved-edge-present"])
    vr["zero-under-limitation"] = {"zeroSupportsAbsence": False}
    w, c, e = panels_for("mixed-reached-universe-without-identity")
    reached_row = {r["subjectId"]: r for r in e["testReachability"]}[sid["rs:core::shared_fmt"]]
    assert (reached_row["state"], reached_row["blockers"], reached_row["reachedUniverses"]) == (
        "not-found-incomplete", ["reached-universe-without-test-origin-identity", "test-origin-set-partial"], sorted([builder.UR, builder.UL])), reached_row
    vr["reached-universe-without-identity"] = reached_row["blockers"]
    w, c, e = panels_for("mixed-cross-program-duplicate")
    dup = next(x for x in c["cells"] if x["fromOwnerKey"] == keys["shared"] and x["toOwnerKey"] == keys["web"])
    assert (dup["facts"], dup["programEdges"], dup["sourceDependencies"], len(dup["importerUniverses"])) == (2, 2, 1, 2)
    vr["cross-program-duplicate"] = {k: dup[k] for k in ("facts", "programEdges", "sourceDependencies")}
    w = world("mixed-fan-in-100001")
    lib = [{"subjectId": RM.subject_id(builder.ep(builder.UR, "symbol", "rs:core::lib")), "state": "resolved", "endpoint": builder.ep(builder.UR, "symbol", "rs:core::lib")}]
    rows, projection = M.derive_metrics(w, M.EvidenceGraphOwner(w), lib, BIG)
    for row in rows:
        V.schema(RID + "#/$defs/SymbolMetricV1", row)
    M.admit_symbol_metrics(rows, projection, ctx(w, lib))
    fan = {r["metricId"]: (r["countState"], r.get("value")) for r in rows}
    assert fan["resolved-call-facts-incoming"] == ("lower-bound", 100000) and fan["distinct-resolved-callers-within-1-hop"] == ("lower-bound", 100000)
    vr["fan-in-100001"] = fan
    full = len(RM.canonical(me["metrics"]))
    rows, projection = M.derive_metrics(worlds["mixed"], M.EvidenceGraphOwner(worlds["mixed"]), resolutions["mixed"], full // 2)
    assert projection["omissionCause"] == "byte-budget" and 0 < projection["omitted"] < 35 and rows == me["metrics"][:len(rows)]
    M.admit_symbol_metrics(rows, projection, ctx(worlds["mixed"], resolutions["mixed"]))
    vr["metric-byte-budget"] = projection
    w = world("mixed-run-evidence-purged")
    assert V.run(lambda: M.derive_coupling(w)) == "QUERY-EVIDENCE-UNAVAILABLE" and V.run(lambda: M.derive_symbol_evidence(w, resolutions["mixed"], BIG)) == "QUERY-EVIDENCE-UNAVAILABLE"
    for panel_name in ("CouplingPanelStateV1", "SymbolEvidencePanelStateV1"):
        V.schema(RID + "#/$defs/" + panel_name, {"state": "unavailable", "reason": "evidence-purged"})
    report["variants"] = vr

    # 9. dense coupling (F6)
    t0 = time.time()
    dense = world("dense-120")
    dense_full = M.coupling_full(dense)
    dense_panel = M.fit_coupling(dense, dense_full, BIG)
    V.schema(RID + "#/$defs/CouplingPanelV1", dense_panel)
    M.admit_coupling(dense_panel, dense.run_id, BIG)
    assert len(RM.canonical(dense_panel)) <= BIG and dense_panel["cellsProjection"]["omitted"] > 0 and dense_panel["absence"]["blankCellMeans"] == "not-determined-cells-omitted"
    assert "cells-omitted" in dense_panel["absence"]["blockers"] and not dense_panel["absence"]["absenceSupported"] and dense_full["totals"]["cellCount"] == 14280
    small = M.fit_coupling(dense, dense_full, 200000)
    M.admit_coupling(small, dense.run_id, 200000)
    assert len(RM.canonical(small)) <= 200000 and small["cellsProjection"]["omitted"] > dense_panel["cellsProjection"]["omitted"]
    assert M.fit_coupling(dense, dense_full, 1000) is None
    lied = copy.deepcopy(dense_panel)
    lied["absence"] = {"blankCellMeans": "no-projected-fact", "absenceSupported": True, "blockers": []}
    dense_cases = {"blankCellClaimedWithOmittedCells": V.run(lambda: M.admit_coupling(lied, dense.run_id, BIG)),
                   "panelOverItsBudget": V.run(lambda: M.admit_coupling(dense_panel, dense.run_id, 200000))}
    assert dense_cases == {"blankCellClaimedWithOmittedCells": "J-COUPLING-ABSENCE", "panelOverItsBudget": "J-COUPLING-BUDGET"}
    report["denseCoupling"] = {"packages": 120, "cells": 14280, "atExplorationCap": {k: dense_panel[k] for k in ("cellsProjection", "targetBucketsProjection", "drilldownProjection")},
                               "bytes": len(RM.canonical(dense_panel)), "at200000": small["cellsProjection"], "skeletonOver1000Bytes": "omitted", "cases": dense_cases,
                               "seconds": round(time.time() - t0, 1)}

    # 10. document, recognition and host cases
    owners_by_key = {o["ownerKey"]: o for o in mc["owners"]}

    def subject_alias(token):
        return sid[{"@parse": "rs:core::parse", "@shared": "rs:core::shared_fmt", "@api": "ts:web/api", "@button-test": "ts:web/button.test", "@both": "rs:core::both",
                    "@legacy": "ts:legacy/old"}[token]]

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

    def resolve_value(value, current, doc):
        if isinstance(value, dict):
            return {k: resolve_value(v, None, doc) for k, v in value.items()}
        if isinstance(value, list):
            return [resolve_value(v, None, doc) for v in value]
        if not isinstance(value, str) or not value.startswith("@"):
            return copy.deepcopy(value)
        if value in ("@lodash", "@web"):
            return keys[value[1:]]
        if value == "@core-lib-unit":
            return [t["unitId"] for t in owners_by_key[keys["core"]]["cargoTargets"] if t["targetKind"] == "lib"]
        if value == "@svc-bin-unit":
            return next(t["unitId"] for t in owners_by_key[keys["svc"]]["cargoTargets"] if t["targetKind"] == "bin")
        if value == "@reversed":
            return list(reversed(current))
        if value == "@owners-plus-unreferenced":
            unit = next(u for u in worlds["mixed"].units.values() if u["rootPath"] == "packages/web-legacy")
            extra_owner = {"keyKind": "workspace-unit", "workspaceUnit": worlds["mixed"].unit_ref(unit)}
            shared_unit = next(u for u in worlds["mixed"].units.values() if u["rootPath"] == "packages/shared")
            extra_owner = {"keyKind": "workspace-unit", "workspaceUnit": worlds["mixed"].unit_ref(shared_unit)}
            extra_owner = dict(extra_owner, ownerKey=M.owner_key(M.owner_key_record(extra_owner)))
            return sorted(current + [extra_owner], key=lambda o: o["ownerKey"].encode())
        if value == "@shared-unknown-identity":
            return {"subjectId": current["subjectId"], "state": "unknown", "cause": "no-test-origin-identity", "reach": current["reach"], "reachedUniverses": current["reachedUniverses"]}
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
            elif op["op"] == "swap":
                node[last][op["i"]], node[last][op["j"]] = node[last][op["j"]], node[last][op["i"]]
            elif op["op"] == "add":
                assert last not in node
                node[last] = resolve_value(op["value"], None, out)
            else:
                current = node[last] if (isinstance(node, list) or last in node) else None
                node[last] = resolve_value(op["value"], current, out)
        return out

    def document_outcome(panel_name, doc, w, resolution, budget=BIG):
        if panel_name == "coupling":
            return V.run(lambda: (V.schema(RID + "#/$defs/CouplingPanelV1", doc), M.admit_coupling(doc, w.run_id, budget)))
        return V.run(lambda: (V.schema(RID + "#/$defs/SymbolEvidencePanelV1", doc), M.admit_symbol_evidence(doc, ctx(w, resolution, budget))))

    doc_results = {}
    for case in fixture["documentCases"]:
        doc = mutate(panels["mixed"][case["panel"]], case["ops"])
        got = document_outcome(case["panel"], doc, worlds["mixed"], resolutions["mixed"])
        doc_results[case["id"]] = got
        assert got == case["expect"], (case["id"], got, case["expect"])
    report["documentCases"] = {"count": len(doc_results), "byCode": {c: sorted(k for k, v in doc_results.items() if v == c) for c in sorted(set(doc_results.values()))}}
    rec_results = {}
    for case in fixture["recognitionCases"]:
        record = mutate(mixed_data["recognitionRecord"], case["ops"])
        if case["rehash"]:
            for row in record["units"]:
                row["recognitionId"] = M.native_h(M.RECOGNITION_DOMAIN, row["recognition"])
        got = V.run(lambda: (V.schema("opensip.product.framework-recognition-plan.1", record), M.admit_recognition_plan(worlds["mixed"], record)))
        rec_results[case["id"]] = got
        assert got == case["expect"], (case["id"], got, case["expect"])
    report["recognitionCases"] = rec_results
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
        got = next((code for k, code in sections if doc[k] != lawful[k]), "accept") if browser == "accept" else browser
        host_results[case["id"]] = {"browserAdmission": browser, "outcome": got}
        assert got == case["expect"], (case["id"], browser, got, case["expect"])
    assert all(v["browserAdmission"] == "accept" for k, v in host_results.items() if k.startswith(("coupling-", "trace-")))
    report["hostCases"] = host_results

    # 11. report integration under parent07 audit-full, report-wide remaining budget and priority
    base = copy.deepcopy(p07_fixtures["bases"]["audit-full"])
    before_states = [f["featureId"] for f in base["featureStates"]]
    base["featureStates"] = [f for f in base["featureStates"] if f["featureId"] not in REMOVED]
    base["budgetProfile"]["projectionPriority"] = patched["$defs"]["BudgetProfileV1"]["properties"]["projectionPriority"]["const"]
    cap = RM.effective_exploration_budget(base["budgetProfile"], base["envelope"], base["invocationLedger"], patched["required"])
    iw = worlds["integration"]
    ires = resolutions["integration"]
    placed, budgets = M.place_successor_panels(base["panels"], cap, {"symbolEvidence": lambda b: M.derive_symbol_evidence(iw, ires, b),
                                                                    "coupling": lambda b: M.derive_coupling(iw, budget=b, test_origin_state=M.test_origin_state_fn(iw))})
    doc = dict(base, panels=placed)
    V.schema(RID, doc)
    M.admit_successor_placement(placed, cap)
    M.admit_panel_prerequisites(placed)
    graph_resolution = placed["graph"]["data"]["subjectResolution"]
    ictx = {"projectId": base["envelope"]["projectId"], "runId": base["envelope"]["run"]["runId"], "resolution": ires, "graphResolution": graph_resolution,
            "bounds": M.PUBLIC_BOUNDS, "budget": budgets["symbolEvidence"]}
    M.admit_symbol_evidence(placed["symbolEvidence"]["data"], ictx)
    M.admit_coupling(placed["coupling"]["data"], ictx["runId"], budgets["coupling"])
    dense_placed, dense_budgets = M.place_successor_panels(base["panels"], cap, {"symbolEvidence": lambda b: M.derive_symbol_evidence(iw, ires, b),
                                                                                "coupling": lambda b: M.fit_coupling(dense, dense_full, b)})
    V.schema(RID, dict(base, panels=dense_placed))
    M.admit_successor_placement(dense_placed, cap)
    assert dense_placed["coupling"]["state"] == "present" and len(RM.canonical(dense_placed)) <= cap
    M.admit_coupling(dense_placed["coupling"]["data"], dense.run_id, dense_budgets["coupling"])
    tight = len(RM.canonical(dict(base["panels"], symbolEvidence=M.OMITTED, coupling=M.OMITTED))) + 50
    tight_placed, _ = M.place_successor_panels(base["panels"], tight, {"symbolEvidence": lambda b: M.derive_symbol_evidence(iw, ires, b),
                                                                       "coupling": lambda b: M.derive_coupling(iw, budget=b)})
    assert tight_placed["symbolEvidence"] == M.OMITTED and tight_placed["coupling"] == M.OMITTED
    out_of_order = dict(tight_placed, coupling=placed["coupling"])
    retained = copy.deepcopy(doc)
    retained["featureStates"] = sorted(retained["featureStates"] + [{"featureId": "symbol-metrics", "view": "symbol-detail", "state": "unavailable", "reason": "no-admitted-owner",
                                                                    "obligationId": "RP-DO-09"}], key=lambda f: f["featureId"].encode())
    mismatch = dict(ictx, resolution=ires[:-1])
    no_graph = dict(placed, graph={"state": "omitted", "reason": "exploration-budget-exceeded"})
    integration = {"auditFullWithSuccessorPanels": "accept", "explorationBudget": cap, "successorBudgets": budgets, "panelsBytes": len(RM.canonical(placed)),
                   "denseCouplingInReport": dense_placed["coupling"]["data"]["cellsProjection"],
                   "couplingPresentAfterOmittedSymbolEvidence": V.run(lambda: M.admit_successor_placement(out_of_order, cap)),
                   "removedFeatureStateStillListed": V.run(lambda: V.schema(RID, retained)),
                   "subjectsNotGraphPanelSubjects": V.run(lambda: M.admit_symbol_evidence(placed["symbolEvidence"]["data"], mismatch)),
                   "symbolEvidenceWithoutGraph": V.run(lambda: M.admit_panel_prerequisites(no_graph)),
                   "featureStatesBefore": before_states, "featureStatesAfter": [f["featureId"] for f in doc["featureStates"]]}
    assert (integration["couplingPresentAfterOmittedSymbolEvidence"], integration["removedFeatureStateStillListed"], integration["subjectsNotGraphPanelSubjects"],
            integration["symbolEvidenceWithoutGraph"]) == ("J-BUDGET-ORDER", "SCHEMA", "J-SE-SUBJECTS", "J-SE-PREREQUISITE"), integration
    report["integration"] = integration

    # 12. register, featureMap refs and requirement text
    register = owners["owner/evidence-design-successor.v2.json"]
    obligations = {o["id"]: o for o in json.loads(p07("owner/design-obligations.v1.json"))["obligations"]}
    for rid in ("RP-DO-03", "RP-DO-05", "RP-DO-09", "RP-DO-10"):
        assert obligations[rid]["blocksReportDesignReadiness"] is True
    assert [d["id"] for d in register["findingDispositions"]] == ["F%d" % i for i in range(1, 10)] and all(d["disposition"] == "corrected" for d in register["findingDispositions"])
    refs = [r["ref"] for rows_ in register["featureMapSuccessor"].values() for r in rows_]
    for pointer in refs:
        resolve_pointer(patched, pointer)
    try:
        resolve_pointer(patched, "/$defs/GraphPanelV1/properties/reviewerBogusMember")
        bogus = "RESOLVED"
    except KeyError:
        bogus = "REFUSED"
    assert bogus == "REFUSED"
    flat = lambda text: " ".join(text.split())
    native_md = flat((arch / "docs/v2/contracts/product-v1/native-evidence.md").read_text())
    for sentence in ("explicit configuration wins and sets `entryPoints.source=explicit`", "never a prefix, never a nearest directory, never a first match",
                     "Rows are those whose `path` **equals** the enclosing fact's anchor path"):
        assert flat(sentence) in native_md, sentence
    inventory_md = flat((arch / "docs/v2/architecture/prototype-report-inventory.md").read_text())
    for sentence in ("Bind metrics and test reachability to the exact universe/identity and show unknown values", "a blank cell is not a global no-dependency proof",
                     "A missing path is unavailable, incomplete or absent within a stated scope"):
        assert flat(sentence) in inventory_md, sentence
    report["register"] = {"findingDispositions": {d["id"]: d["disposition"] for d in register["findingDispositions"]}, "featureMapRefsResolved": len(refs), "bogusRef": bogus,
                          "ownerSuccessors": [s["id"] for s in register["ownerSuccessors"]], "integrationDuties": [d["id"] for d in register["integrationDuties"]],
                          "remainingBlockers": register["remainingBlockers"]}
    report["closureCounts"] = dict(closure.counts)
    report["seconds"] = round(time.time() - started, 1)
    report["limits"] = ["worlds and graph owner are constructions following the cited laws, not the product engine, store, providers or browser",
                        "identity/evaluator Runs are the pinned synthetic evaluator3 reference fixtures, not product Runs",
                        "S1-S4 are proposals; no owner accepted them", "no runtime, browser, generator, Run replay or performance evidence"]
    if args.trace_closure:
        files = []
        for path in sorted(closure.files):
            with open(path, "rb") as handle:
                raw = handle.read()
            files.append({"path": path, "sha256": sha(raw), "bytes": len(raw)})
        TRACE_RESULT = {"files": files, "directoryListings": [{"path": d, "entriesSha256": closure.listing_digest(d)} for d in sorted(closure.directories)]}
        print("traced", len(files), "files")
        return
    if args.out:
        with open(args.out, "w") as handle:
            handle.write(json.dumps(report, indent=1, ensure_ascii=False) + "\n")
        assert closure.counts["declaredOutWrites"] == 1
        print("declared-out writes observed:", closure.counts["declaredOutWrites"])
    print(json.dumps({k: report[k] for k in ("documentCases", "hostCases", "variants")}, indent=1)[:4000])
    print("CHECK OK")


if __name__ == "__main__":
    main()
