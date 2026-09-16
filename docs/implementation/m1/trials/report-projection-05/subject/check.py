"""Reference check of the author-04 report/fit successor candidate; not approval, browser, generator, performance or product qualification.

Run (from the subject directory or a copy of exactly the listed subject files):
  TMPDIR=<own scratch> /tmp/opensip-implementation/metadata-reference-env/bin/python -I -B check.py --architecture ARCH [--subject-strict] [--out RESULT.json]
Closure (enforced, not advisory):
- every file this process opens for reading under the architecture checkout or /tmp/opensip-implementation (outside the subject directory and
  the reference environment) must be pinned in source-pins.json; pins are verified before any external import and re-hashed at every open;
- every directory listing under those roots must be pinned; its digest is recomputed at every listing event;
- every executed module is compiled from the bytes read by a fresh-source loader and verified against its pin; bytecode is never read;
- writes under those roots are refused except the declared --out path, which may not be read; a fresh TMPDIR child is the only scratch area;
- child processes are refused: the historical metadata checker runs in-process under the same hook.
The host (filesystem, interpreter, reference environment and start-time pin file) is trusted; concurrent writers between a verification and the
consuming read are outside this reference check. --trace-closure records the closure instead (used only by seal.py).
"""
import argparse
import copy
import hashlib
import importlib.machinery
import importlib.util
import io
import json
import marshal
import os
import re
import shutil
import struct
import sys
import tempfile
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
# Never read bytecode caches: the fresh-source loader below compiles verified source bytes; the prefix also disables adjacent __pycache__ lookup.
sys.pycache_prefix = "/nonexistent-opensip-report-projection-pycache"
ENV_DIR = "/tmp/opensip-implementation/metadata-reference-env"
ORIGINAL_GET_CODE = importlib.machinery.SourceFileLoader.get_code
RID = "urn:opensip:product-v1:workflows:evaluator3:report-projection:1"
ENV4 = "urn:opensip:product-v1:workflows:evaluator3:command-envelope:4"
ENV5 = "urn:opensip:product-v1:workflows:evaluator3:command-envelope:5"
INVS4 = "urn:opensip:product-v1:workflows:evaluator3:command-inventory:4"
INVS5 = "urn:opensip:product-v1:workflows:evaluator3:command-inventory:5"
GQ = "urn:opensip:product-v1:workflows:evaluator3:graph-query:3"
INV = "urn:opensip:product-v1:workflows:evaluator3:invocation:3"
C = "urn:opensip:product-v1:workflows:evaluator3:common:3#/$defs/"
G = GQ + "#/$defs/"
I = INV + "#/$defs/"
N = "urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/"
P = "urn:opensip:product-v1:policy-document:2#/$defs/"
EXIT = {"success": 0, "policy-failed": 1, "request-rejected": 2, "indeterminate": 3, "operational-failed": 4, "interrupted": 130}
FIT_NEW_FIELDS = ["candidates-truncated", "candidates-total-items", "candidates-next-cursor", "candidates-availability"]
CHILD_EVENTS = ("subprocess.Popen", "os.system", "os.exec", "os.posix_spawn", "os.spawn", "os.fork", "os.forkpty", "pty.spawn")
# Native offset of each embedded owner container within the document it is admitted in (owner knowledge; checked for completeness below).
NATIVE_OFFSETS = {
    ENV5: 0, G + "GraphQueryRequestV1": 0, G + "GraphQueryResponseV1": 0, G + "ResolvedView": 1, G + "GraphEndpoint": 3,
    N + "CoverageResultV3": 0, N + "ReleaseCapabilityRegistryV1": 0, "urn:opensip:product-v1:workflows:evaluator3:comparison:2": 0,
    I + "AnalysisResult": 1, I + "WorkflowRef": 1, I + "Mode": 1, I + "Cancellation": 1, I + "StepSpec/properties/dependsOn": 3,
    C + "StepTermination": 3, C + "DomainDetail": 2, C + "FindingSurface": 2, P + "Rule": 2,
}


def norm(path):
    p = os.path.abspath(os.fsdecode(path))
    return p[len("/private"):] if p.startswith("/private/tmp/") else p


class Refused(Exception):
    def __init__(self, code, text=""):
        super().__init__(code + (": " + text if text else ""))
        self.code = code


def need(condition, code, text=""):
    if not condition:
        raise Refused(code, text)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def pointer_get(doc, pointer):
    value = doc
    for token in [t for t in pointer.strip("/").split("/") if t != ""]:
        value = value[int(token)] if isinstance(value, list) else value[token]
    return value


class Ctx:
    pass


# ---------------------------------------------------------------------------
# closure enforcement

class Closure:
    def __init__(self, arch, trace, out):
        self.roots = [norm(arch), "/tmp/opensip-implementation"]
        self.excluded = [norm(HERE), ENV_DIR]
        self.trace = trace
        self.out = norm(out) if out else None
        self.scratch = None
        self.files, self.directories = set(), set()
        self.pinned, self.listings = {}, {}
        self.pinned_inodes, self.listing_inodes = {}, {}
        self.busy = False
        self.counts = {"rehashedOpens": 0, "listingRecomputes": 0, "verifiedSourceCompiles": 0, "declaredOutWrites": 0}

    @staticmethod
    def under(path, root):
        p, r = path.casefold(), root.casefold()
        return p == r or p.startswith(r + "/")

    def governed(self, path):
        """Alias-aware membership: the checked spellings are the given absolute path and its realpath (symlinks, '..'); comparison is case-folded
        because the volumes used here are case-insensitive. Hard links planted outside the roots are outside this trusted-reference claim."""
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

    def listing_for(self, path):
        return self.listings.get(path) or self.listing_inodes.get(self.identity(path))

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
        """Called by the fresh-source loader with the exact bytes it will compile."""
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
                expected = self.listing_for(path)
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
    """A valid-header stale pyc adjacent to a source: the stock loader executes it; the enforced loader executes the source bytes."""
    directory = tempfile.mkdtemp(prefix="opensip-rp04-pyc-", dir=scratch_root)
    closure.scratch = norm(directory)
    saved_prefix = sys.pycache_prefix
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
        exec(ORIGINAL_GET_CODE(importlib.machinery.SourceFileLoader("rp04_stock", source), "rp04_stock"), stock)
        exec(importlib.machinery.SourceFileLoader("rp04_enforced", source).get_code("rp04_enforced"), enforced)
    finally:
        sys.pycache_prefix = saved_prefix
        shutil.rmtree(directory)
        closure.scratch = None
    assert stock["VALUE"] == "stale-bytecode" and enforced["VALUE"] == "verified-source"
    return {"stockLoaderWithAdjacentCache": stock["VALUE"], "enforcedLoader": enforced["VALUE"], "pycachePrefixDuringRun": saved_prefix}


# ---------------------------------------------------------------------------
# report codec

def scan_depth(raw, limit):
    """Iterative maximum container nesting outside strings; independent of parser recursion."""
    depth = deepest = 0
    in_string = escape = False
    for byte in raw:
        if in_string:
            if escape:
                escape = False
            elif byte == 0x5C:
                escape = True
            elif byte == 0x22:
                in_string = False
        elif byte == 0x22:
            in_string = True
        elif byte in (0x7B, 0x5B):
            depth += 1
            if depth > limit:
                return depth
            deepest = max(deepest, depth)
        elif byte in (0x7D, 0x5D):
            depth -= 1
    return deepest


def parse_report(ctx, raw):
    b = ctx.budget
    need(type(raw) is bytes, "CODEC-LEXICAL")
    need(len(raw) <= b["documentMaxBytes"], "CODEC-BYTES")
    need(scan_depth(raw, b["maxJsonDepth"]) <= b["maxJsonDepth"], "CODEC-DEPTH")
    ref = ctx.reference

    def pairs(items):
        out = {}
        for key, value in items:
            if key in out:
                raise ref.AdmissionError("DUPLICATE_KEY")
            out[key] = value
        return out

    def integer(text):
        if text == "-0":
            raise ref.AdmissionError("NEGATIVE_ZERO")
        value = int(text)
        if not ref.MIN_INT <= value <= ref.MAX_INT:
            raise ref.AdmissionError("INTEGER_RANGE")
        return value

    def forbidden(_):
        raise ref.AdmissionError("FLOAT_OR_NONFINITE_FORBIDDEN")

    try:
        value = json.loads(raw.decode("utf-8", "strict"), object_pairs_hook=pairs, parse_int=integer, parse_float=forbidden, parse_constant=forbidden)
        scalars = [value]
        while scalars:
            item = scalars.pop()
            if type(item) is dict:
                scalars.extend(item.values())
            elif type(item) is list:
                scalars.extend(item)
            else:
                ref.typed(item)
    except (UnicodeError, ValueError, RecursionError) as exc:
        raise Refused("CODEC-LEXICAL", str(exc)[:80])
    need(ctx.M.canonical(value) == raw, "CODEC-NONCANONICAL")
    return value


def embedded_owner_records(doc):
    """(name, value, native offset, bounded by the envelope codec). Ledger terminations are structurally bounded only (budget derivation)."""
    out = [("envelope", doc["envelope"], 0, True)]
    panels = doc["panels"]
    present = lambda p: isinstance(p, dict) and p.get("state") == "present"
    out += [("ledger-termination", s["termination"], 3, False) for s in doc["invocationLedger"]["steps"] if s["recorded"]]
    if present(panels.get("graph")):
        for slot in panels["graph"]["data"]["slots"]:
            out += [("graph-request", slot["request"], 0, True), ("graph-response", slot["response"], 0, True)]
    if present(panels.get("evidence")):
        out += [("coverage-entry", e, 0, True) for e in panels["evidence"]["data"]["entries"]]
    if present(panels.get("comparison")):
        out.append(("comparison", panels["comparison"]["data"]["comparison"], 0, True))
    if present(panels.get("history")):
        for row in panels["history"]["data"]["runs"]:
            if present(row):
                out.append(("history-run", row["run"], 1, True))
                out += [("history-finding", f, 2, True) for f in row["findings"]]
    if present(panels.get("catalog")):
        rules, caps = panels["catalog"]["data"]["rules"], panels["catalog"]["data"]["capabilities"]
        if present(rules):
            out += [("policy-rule", r, 2, True) for r in rules["data"]["rules"]]
        if present(caps):
            out.append(("capability-registry", caps["data"]["declarations"], 0, True))
    return out


# ---------------------------------------------------------------------------
# envelope5 host admission (shared by json/human/agent/html)

def admit_envelope(ctx, env, command, schema_code="SCHEMA-ENV"):
    from jsonschema import ValidationError
    try:
        ctx.reference.ExactValidator(ctx.documents[ENV5], registry=ctx.registry).validate(env)
    except ValidationError as exc:
        raise Refused(schema_code, exc.message[:120])
    row = next(c for c in ctx.inventory5["commands"] if c["name"] == command)
    need(env["exitCode"] == EXIT[env["termination"]["class"]], "J-ENV-EXIT")
    if env["kind"] == "failure" and env["termination"]["class"] == "interrupted":
        need(not env.get("errors"), "J-ENV-INTERRUPTION-DETAIL",
             "no DomainDetailCode names an interruption; an error detail beside an interrupted termination misstates the event (RP-OBL-C01)")
    allowed ={"analysis": {"run", "failure"}, "query": {"query", "failure"}}.get(row["requestClass"], set())
    need(env["kind"] in allowed, "J-ENV-KIND")
    need(("advisoryReport" not in env) or ("advisoryDispatch" in row), "J-ENV-FIT-CARRIER", "carrier on a command without advisoryDispatch")
    dispatch = None
    if env["kind"] == "run":
        run = env["run"]
        if "runId" in env["termination"]:
            need(run.get("runId") == env["termination"]["runId"], "J-ENV-TERMINATION-RUN")
        need("availability" in env, "J-ENV-CAPABILITY-AVAILABILITY")
        if command == "audit" and env["termination"]["class"] != "interrupted":
            need("comparisonResultId" in run, "J-ENV-AUDIT-COMPARISON")
        if "advisoryDispatch" in row:
            need("advisoryReport" in env, "J-ENV-FIT-CARRIER")
            report = env["advisoryReport"]
            if report["state"] == "sealed-run-first-page":
                request, record, parity = report["request"], report["candidateList"], report["parity"]
                need(request["view"]["runId"] == run["runId"] and request["projectId"] == env["projectId"] and parity["runId"] == run["runId"], "J-ENV-FIT-RUN")
                try:
                    ctx.qsp.command_surface_summary("candidate-list", record, env)
                except ctx.qsp.QuerySurfaceProjectionError as exc:
                    raise Refused("J-ENV-" + exc.code)
                context = record["context"]
                need(context["resolvedView"]["runId"] == run["runId"], "J-ENV-FIT-RUN")
                listed = len(record["candidates"])
                need(listed <= 100 and context["truncated"] == (context["totalItems"] > listed), "J-ENV-FIT-PAGE")
                if context["truncated"]:
                    need(listed == 100 and "nextCursor" in context, "J-ENV-FIT-PAGE")
                    need(context["nextCursor"] == ctx.M.fit_cursor(env["projectId"], run["runId"], 100), "J-ENV-FIT-CURSOR")
                else:
                    need("nextCursor" not in context, "J-ENV-FIT-PAGE")
                expected = {"runId": run["runId"], "candidates": record["candidates"], "evidenceLevels": record["evidenceLevels"], "candidatesTruncated": context["truncated"],
                            "candidatesTotalItems": context["totalItems"], "candidatesNextCursor": context.get("nextCursor"), "candidatesAvailability": "sealed-run-first-page"}
                need(ctx.reference.equal_typed(parity, expected), "J-ENV-FIT-PARITY")
            dispatch = row["advisoryDispatch"]
    elif env["kind"] == "query":
        need(env["querySurface"] == row["queryDispatch"]["surface"], "J-ENV-SURFACE")
        try:
            summary = ctx.qsp.command_surface_summary(env["querySurface"], env["queryRecord"], env)
        except ctx.qsp.QuerySurfaceProjectionError as exc:
            raise Refused("J-ENV-" + exc.code)
        need(ctx.reference.equal_typed(env["query"], summary), "J-ENV-QUERYRESULT")
        dispatch = row["queryDispatch"]
    if dispatch is not None:
        need(set(dispatch["parityPaths"]) == set(row["parityFields"]), "J-ENV-PARITY-POINTER")
        try:
            return {f: pointer_get(env, p) for f, p in dispatch["parityPaths"].items()}
        except (KeyError, IndexError, TypeError):
            raise Refused("J-ENV-PARITY-POINTER")
    return None


# ---------------------------------------------------------------------------
# report admission

def subject_run(env, command):
    if env["kind"] == "run":
        return env["run"]["runId"] if env["run"]["authority"] == "authoritative" else None
    if env["kind"] != "query":
        return None
    record = env["queryRecord"]
    if command == "candidates":
        return record["context"]["resolvedView"].get("runId")
    if command == "inspect":
        return record["inspection"]["runId"]
    if command == "review-brief":
        return record["brief"]["runId"]
    return None


def check_projection(proj, embedded, cap, code):
    need(proj["total"] == embedded + proj["omitted"], code)
    cause = proj["omissionCause"]
    need((cause == "none") == (proj["omitted"] == 0), code)
    if cause == "item-cap":
        need(embedded == cap, code)


def admit_ledger(ctx, doc, env, command):
    ledger = doc["invocationLedger"]
    row = next(c for c in ctx.inventory5["commands"] if c["name"] == command)
    steps = ledger["steps"]
    need(ledger["requestId"] == env["requestId"], "J-LEDGER-REQUEST")
    need(ledger["workflow"] == {"kind": "builtin", "name": command}, "J-LEDGER-COMMAND")
    need([s["stepId"] for s in steps] == list(range(len(steps))) and [s["kind"] for s in steps] == row["steps"], "J-LEDGER-STEPS")
    need(all(not s["recorded"] for s in steps if s["kind"] == "render"), "J-LEDGER-RENDER")
    need(ledger["missingChildren"] == ctx.M.missing_children(steps), "J-LEDGER-MISSING")
    execution_ids = []
    for step in steps:
        if not step["recorded"]:
            continue
        attempts = step["attempts"]
        execution_ids += [a["executionId"] for a in attempts]
        if step["outcome"] == "completed":
            need(attempts and attempts[-1]["outcome"] == "completed", "J-LEDGER-ATTEMPTS")
        need(all(not a.get("retried") for a in attempts[-1:]), "J-LEDGER-ATTEMPTS")
        need((step["outcome"] == "cancelled") == (step["termination"]["class"] == "interrupted"), "J-LEDGER-CANCELLATION", "cancelled outcome iff interrupted termination")
    need(len(execution_ids) == len(set(execution_ids)), "J-LEDGER-ATTEMPTS")
    by_id = {s["stepId"]: s for s in steps}
    terminal = ("completed", "rejected", "failed", "skipped", "abandoned")
    for step in steps:
        if not (step["recorded"] and step["outcome"] == "skipped"):
            continue
        need(step["attempts"] == [], "J-LEDGER-SKIPPED", "a skipped step executed no attempt")
        outcomes = [by_id[d]["outcome"] if by_id[d]["recorded"] else None for d in step["dependsOn"] if d in by_id and d < step["stepId"]]
        supported = {"dependency-cancelled": any(o == "cancelled" for o in outcomes),
                     "dependency-not-completed": any(o != "completed" for o in outcomes),
                     "dependency-not-terminal": any(o not in terminal for o in outcomes)}[step["skipReason"]]
        need(supported, "J-LEDGER-SKIPPED", "skipReason is not supported by the recorded dependency outcomes (owner dependency gate)")
    produced ={s["analysisRunId"] for s in steps if s.get("analysisRunId")}
    need(all(s["kind"] in ("analysis", "verify") for s in steps if s.get("analysisRunId")), "J-LEDGER-RUN")
    if env["kind"] == "run" and env["run"]["authority"] == "authoritative":
        need(env["run"]["runId"] in produced, "J-LEDGER-RUN")
    if "runId" in env["termination"]:
        need(env["termination"]["runId"] in produced, "J-LEDGER-RUN")
    if env["kind"] == "run":
        need(ledger["mode"]["ephemeral"] == (env["run"]["authority"] == "ephemeral"), "J-LEDGER-MODE")
    cancellation = ledger["cancellation"]
    need(cancellation["requested"] is False and cancellation["phase"] == "none", "J-LEDGER-CANCELLATION",
         "the report is projected inside the required render step; a signal then is before-settle, cancels this render and no report document is delivered")
    try:
        aggregate = ctx.M.invocation_aggregate(steps, ledger["cancellation"])
    except ctx.M.ModelRefusal as exc:
        raise Refused(exc.code, str(exc))
    need(aggregate is not None and ctx.reference.equal_typed(aggregate, env["termination"]), "J-LEDGER-AGGREGATE")
    need(len(ctx.M.canonical(ledger)) <= ctx.derivations["perCommand"][command]["ledgerMaxBytes"], "J-LEDGER-BOUND")


def admit_document(ctx, raw):
    from jsonschema import ValidationError
    M, b, eq = ctx.M, ctx.budget, ctx.reference.equal_typed
    doc = parse_report(ctx, raw)
    try:
        ctx.reference.ExactValidator(ctx.schema, registry=ctx.registry).validate(doc)
    except ValidationError as exc:
        raise Refused("SCHEMA", exc.message[:120])
    env, command, panels = doc["envelope"], doc["command"], doc["panels"]
    need(len(M.canonical(env)) <= b["envelopeMaxCanonicalBytes"], "ENVELOPE-SERIALIZATION-BOUNDARY")
    for name, value, native, codec_bounded in embedded_owner_records(doc):
        try:
            ctx.reference.typed(value, native)
        except ctx.reference.AdmissionError as exc:
            raise Refused("CODEC-OWNER-DEPTH", name + ":" + str(exc))
        if codec_bounded and name != "envelope":
            need(len(M.canonical(value)) <= b["embeddedPanelOwnerMaxCanonicalBytes"], "CODEC-OWNER-BYTES", name)
    row = next(c for c in ctx.inventory5["commands"] if c["name"] == command)
    html = next(r for r in ctx.inventory5["renderers"] if r["format"] == "html")
    need("html" in row["formats"] and row["requestClass"] in html["applicability"] and doc["renderer"]["version"] == html["version"], "J-RENDERER")
    admit_envelope(ctx, env, command, schema_code="SCHEMA")
    admit_ledger(ctx, doc, env, command)
    anchor = subject_run(env, command)
    run = env.get("run", {})
    present = lambda p: isinstance(p, dict) and p.get("state") == "present"
    subjects = M.policy_subjects(env, command) if env["kind"] != "failure" else []
    budget_bytes = M.effective_exploration_budget(b, env, doc["invocationLedger"], ctx.schema["required"])

    states = [(n, v) for n, v in panels.items()]
    if present(panels.get("catalog")):
        states += [("catalog." + k, v) for k, v in panels["catalog"]["data"].items()]
    for name, value in states:
        if present(value):
            continue
        reason = value["reason"]
        if env["kind"] == "failure":
            need(reason == "no-admitted-result", "J-FAILURE-PANELS", name)
            continue
        need(reason != "no-admitted-result", "J-STATE-REASON", name)
        if reason == "no-run-identity":
            need(anchor is None and name in ("graph", "history"), "J-STATE-REASON", name)
        if reason == "prerequisite-panel-not-present":
            need(name == "history" and "comparisonResultId" in run and not present(panels.get("comparison")), "J-STATE-REASON", name)
        if reason == "not-selected":
            need((name == "comparison" and "comparisonResultId" not in run) or (name == "graph" and not subjects), "J-NOT-SELECTED", name)
    if env["kind"] == "run" and "comparison" in panels:
        if "comparisonResultId" not in run:
            need(panels["comparison"] == {"state": "omitted", "reason": "not-selected"}, "J-COMPARISON-ID")

    priority = b["projectionPriority"]
    for i, name in enumerate(priority):
        value = panels.get(name)
        if value is None:
            continue
        budget_omitted = value.get("reason") == "exploration-budget-exceeded" or (name == "catalog" and present(value) and any(s.get("reason") == "exploration-budget-exceeded" for s in value["data"].values()))
        if budget_omitted:
            need(not any(present(panels[p]) for p in priority[i + 1:] if p in panels), "J-BUDGET-ORDER", name)

    deltas = []
    graph = panels.get("graph")
    if present(graph):
        need(anchor is not None, "J-ANCHOR")
        data = graph["data"]
        need(bool(subjects) and [r["subjectId"] for r in data["subjectResolution"]] == subjects, "J-SLOT-SUBJECTS")
        for res in data["subjectResolution"]:
            if res["state"] == "resolved":
                need(M.subject_id(res["endpoint"]) == res["subjectId"], "J-SUBJECT-INDEX-MISMATCH")
        plan = M.plan_slots(data["subjectResolution"], env["projectId"], anchor)
        projection = data["slotsProjection"]
        need(projection["total"] == len(plan) and len(data["slots"]) <= len(plan), "J-SLOT-POLICY")
        check_projection(projection, len(data["slots"]), b["maxGraphSlots"], "J-GRAPH-SLOT-COUNTS")
        if projection["omissionCause"] == "byte-budget":
            deltas.append(projection["rejectedByteDelta"])
        for slot, planned in zip(data["slots"], plan):
            request, response = slot["request"], slot["response"]
            bare = {k: v for k, v in request.items() if k != "page"}
            need(slot["purpose"] == planned["purpose"] and slot["anchorSubjectIds"] == planned["anchorSubjectIds"] and eq(bare, planned["request"]), "J-SLOT-POLICY")
            rctx, params, items, size = response["context"], request["params"], response["items"], request["page"]["size"]
            need(rctx["resolvedView"]["runId"] == anchor and request["view"]["runId"] == anchor, "J-GRAPH-RUN")
            need(request["projectId"] == rctx["projectId"] == env["projectId"], "J-GRAPH-PROJECT")
            need(request["operation"] == response["operation"], "J-GRAPH-OPERATION")
            violation = M.page_law(rctx, len(items), size, b["graphPublicBounds"])
            need(violation is None, "J-GRAPH-COUNT", violation or "")
            cursor = rctx.get("nextCursor")
            if cursor is not None:
                need(cursor == M.graph_cursor(request, len(items)), "J-GRAPH-CURSOR")
            need(slot["hostProjection"]["continuation"] == M.continuation_for(rctx), "J-GRAPH-CONTINUATION")
            need((slot["hostProjection"]["pageSizeCause"] == "ladder-first") == (size == b["graphPageSizeLadder"][0]), "J-GRAPH-PAGE-CAUSE")
            if slot["hostProjection"]["pageSizeCause"] == "byte-budget-reduced":
                need(rctx["traversalCoverage"] == "truncated-page", "J-BUDGET-CAUSE", "a page that is not full cannot shrink")
                deltas.append(slot["hostProjection"]["rejectedByteDelta"])
            table = M.TABLE.get((params["relation"], params["minResolution"]))
            need(table is not None, "J-GRAPH-RELATION-UNSUPPORTED")
            op = request["operation"]
            if op == "graph.neighbors":
                for item in items:
                    need(item["relation"] == params["relation"], "J-GRAPH-RELATION")
                    need(item["resolution"] == params["minResolution"], "J-GRAPH-RESOLUTION")
                    need(item["source"]["kind"] in table["source"] and item["target"]["kind"] in table["target"], "J-GRAPH-KINDS")
                    touches = {"outgoing": [item["source"]], "incoming": [item["target"]], "both": [item["source"], item["target"]]}[params["direction"]]
                    need(any(eq(e, params["endpoint"]) for e in touches), "J-GRAPH-ENDPOINT")
                    if slot["purpose"] == "package-coupling":
                        need(item["target"]["kind"] == "package" and params["direction"] == "incoming", "J-GRAPH-COUPLING")
                keys = [(M.endpoint_tuple(r["source"]), M.endpoint_tuple(r["target"]), r["factId"].encode()) for r in items]
                need(keys == sorted(keys) and len(set(keys)) == len(keys), "J-GRAPH-ORDER")
            elif op == "graph.reach":
                for item in items:
                    depth = item["depth"]
                    need(depth <= params["maxDepth"] and (depth > 0 or (params.get("includeStart") is True and eq(item["endpoint"], params["start"]))), "J-GRAPH-REACH")
                    need(("viaFactId" in item) == (depth > 0), "J-GRAPH-REACH")
                    need(depth == 0 or item["endpoint"]["kind"] in table["target"], "J-GRAPH-KINDS")
                keys = [M.endpoint_tuple(r["endpoint"]) for r in items]
                need(keys == sorted(keys) and len(set(keys)) == len(keys), "J-GRAPH-ORDER")
            else:
                for item in items:
                    need(eq(item["start"], params["start"]) and eq(item["target"], params["target"]), "J-GRAPH-ENDPOINT")
                    nodes, edges = item["nodes"], item["edges"]
                    need(item["hopCount"] == len(edges) == len(nodes) - 1 and item["hopCount"] <= params["maxDepth"], "J-GRAPH-PATH")
                    need(eq(nodes[0], item["start"]) and eq(nodes[-1], item["target"]), "J-GRAPH-PATH")
                    need(len({M.canonical(n) for n in nodes}) == len(nodes) and len({e["factId"] for e in edges}) == len(edges), "J-GRAPH-PATH")
                    for i, edge in enumerate(edges):
                        need(eq(edge["source"], nodes[i]) and eq(edge["target"], nodes[i + 1]), "J-GRAPH-PATH")
                    need(all(n["kind"] in table["target"] | table["source"] for n in nodes), "J-GRAPH-KINDS")
        expected_index = M.subject_index(data["slots"], data["subjectResolution"])
        by_endpoint = {M.canonical(r["endpoint"]): r["subjectId"] for r in data["subjectIndex"]}
        for key, sid in by_endpoint.items():
            need(sid == M.subject_id(json.loads(key)), "J-SUBJECT-INDEX-MISMATCH")
        need(eq(data["subjectIndex"], expected_index), "J-SUBJECT-INDEX-COVERAGE")
        not_retained = {r["subjectId"] for r in data["subjectResolution"] if r["state"] != "resolved"}
        need(not (not_retained & {r["subjectId"] for r in data["subjectIndex"]}), "J-SLOT-RESOLUTION-CONTRADICTED", "a descriptor stated not retained is present in an embedded owner row")
    elif graph is not None and not present(graph) and env["kind"] != "failure" and graph.get("reason") == "not-selected":
        need(not subjects, "J-NOT-SELECTED")

    evidence = panels.get("evidence")
    if present(evidence):
        data = evidence["data"]
        need(env["kind"] == "run" and run.get("coverageId") == data["coverageId"], "J-EVIDENCE-COVERAGE")
        check_projection(data["entriesProjection"], len(data["entries"]), b["maxEvidenceEntries"], "J-EVIDENCE-COUNTS")
        keys = [M.canonical(e["key"]) for e in data["entries"]]
        need(len(keys) == len(set(keys)), "J-EVIDENCE-KEYS")
        if data["entriesProjection"]["omissionCause"] == "byte-budget":
            deltas.append(data["entriesProjection"]["rejectedByteDelta"])

    comparison = panels.get("comparison")
    if present(comparison):
        result = comparison["data"]["comparison"]
        need(run.get("comparisonResultId") == result["comparisonResultId"], "J-COMPARISON-ID")
        need(result["descriptor"]["currentRunId"] == run["runId"], "J-COMPARISON-RUN")

    history = panels.get("history")
    if present(history):
        need(anchor is not None, "J-ANCHOR")
        need(not ("comparisonResultId" in run and not present(comparison)), "J-HISTORY-PREREQUISITE")
        data, sel = history["data"], history["data"]["selection"]
        source = sel["baselineSourceRunId"]
        need((source is not None) == present(comparison) and (sel["baselineId"] is None) == (source is None), "J-HISTORY-BASELINE")
        if present(comparison):
            need(sel["baselineId"] == comparison["data"]["comparison"]["descriptor"]["baselineId"], "J-HISTORY-BASELINE")
        need(source is None or source not in [p["runId"] for p in sel["priorRuns"]], "J-HISTORY-BASELINE", "baseline source Run is excluded from prior Runs")
        seqs = [p["commitSequence"] for p in sel["priorRuns"]]
        need(all(s < sel["currentCommitSequence"] for s in seqs) and all(a > b_ for a, b_ in zip(seqs, seqs[1:])), "J-HISTORY-ORDER")
        limit = b["maxHistoryRuns"] - (1 if source else 0)
        need(len(sel["priorRuns"]) == min(limit, sel["priorRunsInSnapshot"]), "J-HISTORY-COUNT")
        need(sel["requestedRunIds"] == ([source] if source else []) + [p["runId"] for p in sel["priorRuns"]], "J-HISTORY-POLICY")
        need(anchor not in sel["requestedRunIds"], "J-HISTORY-CURRENT")
        need([r["runId"] for r in data["runs"]] == sel["requestedRunIds"], "J-HISTORY-SELECTION")
        sequence = {p["runId"]: p["commitSequence"] for p in sel["priorRuns"]}
        for entry in data["runs"]:
            if present(entry):
                need(entry["run"]["runId"] == entry["runId"], "J-HISTORY-RUN")
                need(entry["commitSequence"] == sequence.get(entry["runId"]), "J-HISTORY-SEQUENCE")
                check_projection(entry["findingsProjection"], len(entry["findings"]), b["maxHistoryFindingsPerRun"], "J-HISTORY-COUNTS")
                if entry["findingsProjection"]["omissionCause"] == "byte-budget":
                    deltas.append(entry["findingsProjection"]["rejectedByteDelta"])

    catalog = panels.get("catalog")
    if present(catalog):
        rules, caps = catalog["data"]["rules"], catalog["data"]["capabilities"]
        if present(rules):
            need(env["kind"] == "run" and rules["data"]["source"]["planId"] == run["planId"], "J-CATALOG-PLAN")
            need({f["ruleId"] for f in env.get("findings", [])} <= {r["ruleId"] for r in rules["data"]["rules"]}, "J-CATALOG-RULES")
        if present(caps):
            need(caps["data"]["source"]["registrySha256"] == sha(M.canonical(caps["data"]["declarations"])), "J-CATALOG-DIGEST")

    final = len(M.canonical(panels))
    need(final <= budget_bytes, "J-BUDGET-BYTES")
    for delta in deltas:
        need(final + delta > budget_bytes, "J-BUDGET-CAUSE", "rejected addition would have fit")
    need(eq(doc["disclosures"], M.document_disclosures(panels)), "J-DISCLOSURES")
    text = M.static_parity_text(env, row, doc["disclosures"]).encode("utf-8")
    need(doc["staticParity"]["textSha256"] == sha(text) and doc["staticParity"]["textBytes"] == len(text), "J-STATIC-PARITY")
    return doc


# ---------------------------------------------------------------------------
# fixture operations

def slot_panel_bytes(doc):
    return len(json.dumps(doc["panels"], ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode())


def apply_ops(ctx, doc, ops, as_bytes=True):
    M, builder = ctx.M, ctx.builder
    doc = copy.deepcopy(doc)
    raw_op = None
    graph = lambda: doc["panels"]["graph"]["data"]
    for op in ops:
        kind = op["op"]
        if kind in ("set", "remove"):
            *parent, last = op["path"].strip("/").split("/")
            target = pointer_get(doc, "/" + "/".join(parent)) if parent else doc
            key = int(last) if isinstance(target, list) else last
            if kind == "set":
                target[key] = copy.deepcopy(op["value"])
            else:
                del target[key]
        elif kind == "x-append-copy":
            array = pointer_get(doc, op["path"])
            array.append(copy.deepcopy(array[0]))
        elif kind == "x-remove-index":
            del pointer_get(doc, op["path"])[op["index"]]
        elif kind == "x-remove-feature":
            doc["featureStates"] = [s for s in doc["featureStates"] if s["featureId"] != op["featureId"]]
        elif kind == "x-bytes":
            raw_op = op["kind"]
        elif kind == "x-refresh":
            builder.refresh(doc)
        elif kind == "x-disclosure":
            doc["disclosures"][op["key"]] = op["value"]
        elif kind == "x-feature-reason":
            next(s for s in doc["featureStates"] if s["featureId"] == op["featureId"])["reason"] = op["reason"]
        elif kind == "x-provenance-move":
            provenance = doc["panels"][op["panel"]]["data"]["provenance"]
            provenance["hostAsserted"].remove(op["label"])
            provenance["verifiedInDocument"] = sorted(provenance["verifiedInDocument"] + [op["label"]])
        elif kind == "x-history-copy-current-findings":
            row = doc["panels"]["history"]["data"]["runs"][0]
            row["findings"] = copy.deepcopy(doc["envelope"]["findings"])
            row["findingsProjection"] = {"total": len(row["findings"]), "omitted": 0, "omissionCause": "none"}
        elif kind == "x-empty-registry":
            caps = doc["panels"]["catalog"]["data"]["capabilities"]["data"]
            caps["declarations"] = []
            caps["source"]["registrySha256"] = sha(M.canonical([]))
        elif kind == "x-deep-rule-predicate":
            rule = doc["panels"]["catalog"]["data"]["rules"]["data"]["rules"][0]
            atom = rule["emitWhen"]
            for _ in range(op["notChain"]):
                atom = {"op": "not", "operand": atom}
            rule["emitWhen"] = atom
        elif kind == "x-worst-findings":
            rows = []
            for i in range(op["count"]):
                row = copy.deepcopy(ctx.worst["finding"])
                row["findingId"] = "finding3:" + sha(b"worst-finding-%d" % i)
                rows.append(row)
            doc["envelope"]["findings"] = sorted(rows, key=lambda r: r["findingId"].encode())
        elif kind == "x-inflate-evidence":
            base = doc["panels"]["evidence"]["data"]["entries"][0]
            rows = []
            for i in range(op["count"]):
                row = copy.deepcopy(base)
                row["key"]["subjectScopeCommitment"] = "sha256:" + sha(b"scope-%d" % i)
                rows.append(row)
            doc["panels"]["evidence"]["data"]["entries"] = rows
            doc["panels"]["evidence"]["data"]["entriesProjection"] = {"total": op["count"], "omitted": 0, "omissionCause": "none"}
        elif kind == "x-fill-to-budget-edge":
            base = doc["panels"]["evidence"]["data"]["entries"][0]
            lo, hi = 1, ctx.budget["maxEvidenceEntries"]
            def with_count(n):
                rows = []
                for i in range(n):
                    row = copy.deepcopy(base)
                    row["key"]["subjectScopeCommitment"] = "sha256:" + sha(b"edge-%d" % i)
                    rows.append(row)
                doc["panels"]["evidence"]["data"]["entries"] = rows
                doc["panels"]["evidence"]["data"]["entriesProjection"] = {"total": n, "omitted": 0, "omissionCause": "none"}
                return slot_panel_bytes(doc)
            limit = M.effective_exploration_budget(ctx.budget, doc["envelope"], doc["invocationLedger"], ctx.schema["required"])
            while lo < hi:
                mid = (lo + hi + 1) // 2
                if with_count(mid) <= limit:
                    lo = mid
                else:
                    hi = mid - 1
            with_count(lo)
        elif kind == "x-subject-index-forge-last":
            graph()["subjectIndex"][-1]["subjectId"] = "subject3:" + "f" * 64
        elif kind == "x-fit-truncate-claim":
            report = doc["envelope"]["advisoryReport"]
            context = report["candidateList"]["context"]
            context.update(truncated=True, totalItems=len(report["candidateList"]["candidates"]) + op["extra"], nextCursor=M.fit_cursor(doc["envelope"]["projectId"], doc["envelope"]["run"]["runId"]))
            report["parity"].update(candidatesTruncated=True, candidatesTotalItems=context["totalItems"], candidatesNextCursor=context["nextCursor"])
        elif kind == "x-fit-cursor":
            env = doc["envelope"] if "envelope" in doc else doc
            report = env["advisoryReport"]
            cursor = M.fit_cursor(env["projectId"], env["run"]["runId"], 99 if op["value"] == "position-99" else 100)
            report["candidateList"]["context"]["nextCursor"] = cursor
            report["parity"]["candidatesNextCursor"] = cursor
        elif kind == "x-ledger-record-render":
            step = doc["invocationLedger"]["steps"][-1]
            step.update(recorded=True, outcome="completed", attempts=[{"executionId": "exec1_" + "9" * 32, "outcome": "completed"}], termination={"class": "success"})
        elif kind == "x-ledger-duplicate-execution":
            steps = doc["invocationLedger"]["steps"]
            steps[1]["attempts"][0]["executionId"] = steps[0]["attempts"][0]["executionId"]
        elif kind == "x-delivery-termination":
            doc["envelope"] = M.failure_envelope(doc["envelope"], M.renderer_failure(doc["envelope"]["termination"]["runId"]))
            builder.refresh(doc)
        elif kind == "x-pinned-failure":
            run_id = doc["envelope"]["run"]["runId"]
            char = op["char"]
            lo, hi = 1, 4096
            while lo < hi:
                mid = (lo + hi + 1) // 2
                if len(M.canonical(M.failure_envelope(doc["envelope"], builder.pinned_termination(mid, run_id, char)))) <= ctx.budget["envelopeMaxCanonicalBytes"]:
                    lo = mid
                else:
                    hi = mid - 1
            first = builder.pinned_termination(lo, run_id, char)
            big = first if op["stepPins"] == "envelope-max" else builder.pinned_termination(4096, run_id, char)
            for i, step in enumerate(s for s in doc["invocationLedger"]["steps"] if s["recorded"]):
                step["termination"] = first if i == 0 else (big if i < op["bigSteps"] else {"class": "request-rejected", "errorCode": "REQUEST.PRECONDITION_FAILED"})
                step["outcome"] = "rejected"
                step["attempts"][-1]["outcome"] = "rejected"
            doc["envelope"] = M.failure_envelope(doc["envelope"], first)
            doc["panels"] = {k: {"state": "unavailable", "reason": "no-admitted-result"} for k in doc["panels"]}
            builder.refresh(doc)
        elif kind == "x-cancel-before-settle":
            run_id = doc["envelope"]["run"]["runId"]
            doc["envelope"]["run"].pop("comparisonResultId", None)
            doc["envelope"].update(termination={"class": "interrupted", "signal": "SIGINT", "runId": run_id}, exitCode=130)
            for step in doc["invocationLedger"]["steps"][1:]:
                if step["recorded"]:
                    step.update(outcome="cancelled", termination={"class": "interrupted", "signal": "SIGINT"})
                    step["attempts"][-1]["outcome"] = "cancelled"
            doc["invocationLedger"]["cancellation"] = {"requested": True, "signal": "SIGINT", "phase": "before-settle"}
            builder.refresh(doc)
        elif kind == "x-swap-resolution":
            rows = graph()["subjectResolution"]
            rows[op["a"]], rows[op["b"]] = rows[op["b"]], rows[op["a"]]
        elif kind == "x-slot-relation":
            params = graph()["slots"][op["slot"]]["request"]["params"]
            params.update(relation=op["relation"], minResolution=op["rung"])
        elif kind == "x-slice-slot-items":
            slot = graph()["slots"][op["slot"]]
            slot["response"]["items"] = slot["response"]["items"][:op["count"]]
        elif kind == "x-graph-relabel":
            data = graph()
            slot = data["slots"][op.get("slot", 0)]
            context = slot["response"]["context"]
            variant = op["variant"]
            if not op.get("keepItems"):
                slot["response"]["items"] = slot["response"]["items"][:1]
            if variant in ("complete-lower-bound", "complete-exact", "cap-spill-complete"):
                context.update(traversalCoverage="complete", truncated=False)
                context.pop("nextCursor", None)
                if variant != "cap-spill-complete":
                    context["countBasis"] = "lower-bound" if variant == "complete-lower-bound" else "exact"
            elif variant == "truncated-page-lower-bound":
                context["countBasis"] = "lower-bound"
            elif variant == "truncated-bound-lower-bound":
                context.update(traversalCoverage="truncated-bound", truncated=True, countBasis="lower-bound", totalItems=1, producedItems=1)
                context.pop("nextCursor", None)
            elif variant in ("review04-G4", "review04-G5", "review04-G6", "produced-equals-total-sliced-no-cursor"):
                bounds = ctx.budget["graphPublicBounds"]
                context.pop("nextCursor", None)
                if variant == "review04-G4":
                    context.update(traversalCoverage="truncated-bound", truncated=True, countBasis="lower-bound", producedItems=bounds["maxItemsPerOperation"], totalItems=1)
                elif variant == "review04-G5":
                    context.update(traversalCoverage="truncated-bound", truncated=True, countBasis="lower-bound", visitedNodes=bounds["maxVisitedNodes"], producedItems=50, totalItems=1)
                elif variant == "review04-G6":
                    context.update(traversalCoverage="complete", truncated=False, countBasis="exact", producedItems=1000, totalItems=1)
                else:
                    context.update(traversalCoverage="truncated-bound", truncated=True, countBasis="lower-bound", producedItems=bounds["maxItemsPerOperation"],
                                   totalItems=bounds["maxItemsPerOperation"])
            slot["hostProjection"] = {"continuation": M.continuation_for(context), "pageSizeCause": "ladder-first"}
            data["subjectIndex"] = M.subject_index(data["slots"], data["subjectResolution"])
        elif kind == "x-slot-public-cap-spill":
            data = graph()
            slot = data["slots"][0]
            start = slot["request"]["params"]["endpoint"]
            facts = [{"factId": "fact2:" + sha(b"public-cap-%d" % i), "relation": "calls", "resolution": "resolved-callee", "source": start,
                      "target": {"universe": start["universe"], "kind": "symbol", "nativeSubjectId": "ts:src/cap.ts#c%06d" % i}} for i in range(ctx.budget["graphPublicBounds"]["maxItemsPerOperation"] + 1)]
            response = M.MockGraphOwner(facts, ctx.material["template"]).execute(slot["request"])
            assert response["context"]["countBasis"] == "lower-bound" and response["context"]["producedItems"] == ctx.budget["graphPublicBounds"]["maxItemsPerOperation"]
            slot["response"] = response
            slot["hostProjection"] = {"continuation": M.continuation_for(response["context"]), "pageSizeCause": "ladder-first"}
            data["subjectIndex"] = M.subject_index(data["slots"], data["subjectResolution"])
        elif kind == "x-not-retained-replan":
            data = graph()
            env = doc["envelope"]
            sid = M.subject_id(ctx.material[op["subject"]])
            assert any(r["subjectId"] == sid for r in data["subjectResolution"])
            data["subjectResolution"] = [{"subjectId": r["subjectId"], "state": "descriptor-not-retained"} if r["subjectId"] == sid else r for r in data["subjectResolution"]]
            plan = M.plan_slots(data["subjectResolution"], env["projectId"], env["run"]["runId"])
            slots = []
            for i, planned in enumerate(plan):
                request = copy.deepcopy(planned["request"])
                request["page"] = {"size": M.LADDER[0]}
                response = ctx.owner.execute(request)
                slots.append({"ordinal": i, "purpose": planned["purpose"], "anchorSubjectIds": planned["anchorSubjectIds"], "request": request, "response": response,
                              "hostProjection": {"continuation": M.continuation_for(response["context"]), "pageSizeCause": "ladder-first"}})
            data.update(slots=slots, slotsProjection={"total": len(plan), "omitted": 0, "omissionCause": "none"}, subjectIndex=M.subject_index(slots, data["subjectResolution"]))
            builder.refresh(doc)
        elif kind == "x-slot-cursor":
            context = graph()["slots"][op["slot"]]["response"]["context"]
            context["nextCursor"] = context["nextCursor"].rsplit(".", 1)[0] + ".99"
        elif kind == "x-row-resolution":
            graph()["slots"][op["slot"]]["response"]["items"][op["row"]]["resolution"] = op["resolution"]
        elif kind == "x-row-target":
            graph()["slots"][op["slot"]]["response"]["items"][op["row"]]["target"] = ctx.material[op["target"]]
        elif kind == "x-reverse-slot-items":
            graph()["slots"][op["slot"]]["response"]["items"].reverse()
        elif kind == "x-path-extra-node":
            slot = next(s for s in graph()["slots"] if s["purpose"] == "path")
            slot["response"]["items"][0]["nodes"].append(ctx.material["util"])
        elif kind == "x-reach-depth-zero":
            slot = next(s for s in graph()["slots"] if s["purpose"] == "reach")
            slot["response"]["items"][0] = {"endpoint": slot["request"]["params"]["start"], "depth": 0}
        elif kind == "x-resolution-endpoint":
            graph()["subjectResolution"][op["index"]]["endpoint"] = ctx.material[op["target"]]
        elif kind == "x-reissue-slot":
            data = graph()
            slot = data["slots"][op["slot"]]
            before = slot_panel_bytes(doc)
            request = copy.deepcopy(slot["request"])
            request["page"] = {"size": op["size"]}
            response = ctx.owner.execute(request)
            host = {"continuation": M.continuation_for(response["context"]), "pageSizeCause": "byte-budget-reduced", "rejectedByteDelta": 0}
            slot.update(request=request, response=response, hostProjection=host)
            data["subjectIndex"] = M.subject_index(data["slots"], data["subjectResolution"])
            for _ in range(4):
                host["rejectedByteDelta"] = before - slot_panel_bytes(doc)
        elif kind == "x-history-swap-prior":
            prior = doc["panels"]["history"]["data"]["selection"]["priorRuns"]
            prior[0], prior[1] = prior[1], prior[0]
        elif kind == "x-history-baseline-as-prior":
            selection = doc["panels"]["history"]["data"]["selection"]
            selection["priorRuns"][0]["runId"] = selection["baselineSourceRunId"]
        elif kind == "x-history-understate":
            data = doc["panels"]["history"]["data"]
            selection = data["selection"]
            dropped = selection["priorRuns"].pop()
            selection["priorRunsInSnapshot"] = len(selection["priorRuns"])
            selection["requestedRunIds"] = [r for r in selection["requestedRunIds"] if r != dropped["runId"]]
            data["runs"] = [r for r in data["runs"] if r["runId"] != dropped["runId"]]
            builder.refresh(doc)
        elif kind == "x-finding-rule":
            doc["envelope"]["findings"][0]["ruleId"] = op["value"]
        else:
            raise AssertionError("unknown op " + kind)
    if not as_bytes:
        return doc
    raw = M.canonical(doc)
    if raw_op is None:
        return raw
    replacements = {"negative-zero": b'"schemaMajor":-0,', "float": b'"schemaMajor":1.0,', "exponent": b'"schemaMajor":1e0,', "nan": b'"schemaMajor":NaN,',
                    "integer-out-of-range": b'"schemaMajor":18446744073709551616,'}
    if raw_op == "duplicate-key":
        return b'{"schemaMajor":1,' + raw[1:]
    if raw_op in replacements:
        assert b'"schemaMajor":1,' in raw
        return raw.replace(b'"schemaMajor":1,', replacements[raw_op], 1)
    if raw_op == "lone-surrogate":
        return raw.replace(b'"reportObservedAt":"2026-09-14T12:00:00Z"', b'"reportObservedAt":"\\ud800"', 1)
    if raw_op == "invalid-utf8":
        return raw.replace(b'"reportObservedAt":"2026', b'"reportObservedAt":"\xff026', 1)
    if raw_op == "noncanonical-whitespace":
        return raw.replace(b'{"', b'{ "', 1)
    if raw_op == "noncanonical-key-order":
        return json.dumps(doc, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    if raw_op == "oversize":
        return raw + b" " * (ctx.budget["documentMaxBytes"] - len(raw) + 1)
    if raw_op == "deep-array":
        return b"[" * 200000 + b"]" * 200000
    raise AssertionError(raw_op)


def outcome(fn, *args):
    try:
        fn(*args)
        return "accept", None
    except Refused as exc:
        return exc.code, str(exc)


# ---------------------------------------------------------------------------
# derivations

def embedding_depths(schema, documents):
    found = {}
    def resolve_local(ref):
        node = schema
        for token in ref[2:].split("/"):
            node = node[token]
        return node
    def walk(node, depth, stack):
        if not isinstance(node, dict):
            return
        ref = node.get("$ref")
        if ref:
            if ref.startswith("#/"):
                if ref not in stack:
                    walk(resolve_local(ref), depth, stack | {ref})
            else:
                found[ref] = max(found.get(ref, -1), depth)
        for key in ("allOf", "anyOf", "oneOf"):
            for child in node.get(key, []):
                walk(child, depth, stack)
        for key in ("if", "then", "else", "not"):
            walk(node.get(key), depth, stack)
        for child in node.get("properties", {}).values():
            walk(child, depth + 1, stack)
        if isinstance(node.get("items"), dict):
            walk(node["items"], depth + 1, stack)
    walk(schema, 0, frozenset())
    return found


def is_container(ref, documents, seen=None):
    seen = seen or set()
    if ref in seen:
        return True
    seen.add(ref)
    base, _, fragment = ref.partition("#")
    node = documents[base]
    for token in [t for t in fragment.split("/") if t]:
        node = node[token]
    def check(n):
        if not isinstance(n, dict):
            return False
        if "type" in n:
            types = n["type"] if isinstance(n["type"], list) else [n["type"]]
            return any(t in ("object", "array") for t in types)
        if "$ref" in n:
            target = n["$ref"] if not n["$ref"].startswith("#") else base + n["$ref"]
            return is_container(target, documents, seen)
        if any(k in n for k in ("properties", "items")):
            return True
        for k in ("oneOf", "anyOf", "allOf"):
            if k in n and any(check(c) for c in n[k]):
                return True
        return False
    return check(node)


def property_names(node, out):
    if isinstance(node, dict):
        out.update(node.get("properties", {}).keys())
        for value in node.values():
            property_names(value, out)
    elif isinstance(node, list):
        for value in node:
            property_names(value, out)
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--architecture", required=True, type=Path)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--trace-closure", type=Path)
    parser.add_argument("--subject-strict", action="store_true")
    args = parser.parse_args()
    arch = args.architecture
    report = {"standing": "AUTHOR-05 candidate reference check; not approval, not browser/generator/performance or release qualification"}
    # No tempfile.gettempdir(): it writes a probe file into TMPDIR before the hook exists. The declared TMPDIR is only used after the hook, through mkdtemp.
    scratch_root = os.environ.get("TMPDIR", "")
    assert os.path.isabs(scratch_root) and os.path.isdir(scratch_root), "set TMPDIR to an existing absolute scratch directory"

    # 0. subject manifest and external closure, before any external import
    closure = Closure(arch, trace=bool(args.trace_closure), out=args.out)
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
        # Alias probe: spellings of the unpinned, mutable docs/implementation/README.md; the hook refuses before any byte is read.
        head, tail = norm(arch).rsplit("/", 1)
        aliases = {"exact": norm(arch) + "/docs/implementation/README.md", "case-variant": head + "/" + tail.upper() + "/docs/implementation/README.md",
                   "dot-dot": norm(arch) + "/docs/implementation/m1/../README.md"}
        alias_results = {}
        for label, alias in aliases.items():
            try:
                with open(alias, "rb"):
                    alias_results[label] = "READ-NOT-REFUSED"
            except RuntimeError as exc:
                alias_results[label] = str(exc).split(" ")[0]
            except OSError as exc:
                alias_results[label] = "OSERROR-" + type(exc).__name__
        assert all(v == "UNPINNED-LOAD" for v in alias_results.values()), alias_results
        report["aliasProbe"] = alias_results

    from jsonschema import Draft202012Validator, ValidationError
    from referencing import Resource
    from referencing.jsonschema import DRAFT202012

    ctx = Ctx()
    cm = load("check_metadata", arch / "docs/implementation/m1/metadata-v2/check_metadata.py")
    ctx.reference, registry, documents = cm.load(arch)
    ctx.qsp = load("query_surface_projection", arch / "docs/coop/design-corrections/workflows/query_surface_projection.v3.py")
    identity_model = load("identity_model", arch / "docs/coop/design-corrections/foundation/identity-model.v3.py")
    planning = load("check_implementation_planning", arch / "docs/operations/check_implementation_planning.py")
    ctx.M = load("report_model", HERE / "report_model.py")
    owner = load("build_owner", HERE / "build_owner.py")
    builder = load("build_fixtures", HERE / "build_fixtures.py")
    ctx.builder = builder
    M = ctx.M

    # 1. byte-identical regeneration
    for name, value in owner.build().items():
        assert owner.dump(value) == (HERE / name).read_bytes(), "owner drift " + name
    fixture_raw = json.dumps(builder.build(), indent=1, ensure_ascii=False).encode("utf-8") + b"\n"
    assert fixture_raw == (HERE / "fixtures.json").read_bytes(), "fixtures drift"
    fixture = json.loads(fixture_raw)

    new = {}
    for name in ("owner/command-envelope.v5.schema.json", "owner/command-inventory.v5.schema.json", "report-projection.schema.json"):
        doc = ctx.reference.parse((HERE / name).read_bytes())
        Draft202012Validator.check_schema(doc)
        assert doc["$id"] not in documents
        new[doc["$id"]] = doc
        registry = registry.with_resource(doc["$id"], Resource(contents={k: v for k, v in doc.items() if k != "$schema"}, specification=DRAFT202012))
    documents = dict(documents, **new)
    for doc in new.values():
        for target in re.findall(r'"\$ref":\s*"([^"#]+)', json.dumps(doc)):
            assert target in documents, "unregistered " + target
    ctx.registry, ctx.documents, ctx.schema = registry, documents, documents[RID]
    ctx.budget = {k: v["const"] for k, v in ctx.schema["$defs"]["BudgetProfileV1"]["properties"].items()}
    ctx.derivations = json.loads((HERE / "owner/budget-derivations.v1.json").read_bytes())
    ctx.inventory5 = json.loads((HERE / "owner/command-inventory.v5.json").read_bytes())
    report["projectionSchemaSha256"] = sha((HERE / "report-projection.schema.json").read_bytes())

    # 2. additive successors, preserved metadata behaviour, historical metadata checker in-process under the same closure
    env4, env5 = documents[ENV4], copy.deepcopy(documents[ENV5])
    for key in ("$id", "title", "description"):
        env5[key] = env4[key]
    env5["properties"]["schemaMajor"]["const"] = 4
    del env5["properties"]["advisoryReport"]
    del env5["allOf"][-3:]
    meta = next(e for e in env5["allOf"] if e.get("if", {}).get("properties", {}).get("kind", {}).get("const") == "meta")
    assert meta["then"]["not"]["anyOf"].pop() == {"required": ["advisoryReport"]}
    for name in ("FitAdvisoryReportV1", "FitSealedParityV1", "FitEphemeralParityV1"):
        del env5["$defs"][name]
    assert env5 == env4, "envelope5 not additive"
    invs4, invs5 = documents[INVS4], copy.deepcopy(documents[INVS5])
    invs5["$id"], invs5["properties"]["schemaMajor"]["const"] = invs4["$id"], 4
    del invs5["$defs"]["Command"]["properties"]["advisoryDispatch"], invs5["$defs"]["AdvisoryDispatch"]
    invs5["$defs"]["Command"]["allOf"].pop()
    assert invs5 == invs4, "inventory schema5 not additive"
    inv4 = json.loads((arch / "docs/implementation/m1/metadata-v2/command-inventory.v4.json").read_bytes())
    inv5 = copy.deepcopy(ctx.inventory5)
    inv5["schemaMajor"], inv5["standing"] = 4, inv4["standing"]
    fit = next(c for c in inv5["commands"] if c["name"] == "fit")
    assert fit["parityFields"][-4:] == FIT_NEW_FIELDS
    fit["parityFields"] = fit["parityFields"][:-4]
    del fit["advisoryDispatch"]
    inv5["renderers"][1], inv5["renderers"][3] = inv4["renderers"][1], inv4["renderers"][3]
    assert inv5["goldens"].pop()["id"] == "fit-ephemeral-non-authoritative"
    assert inv5 == inv4, "inventory5 not additive"
    fit_flag = next(f for f in next(c for c in ctx.inventory5["commands"] if c["name"] == "fit")["flags"] if f["flag"] == "--ephemeral")
    assert fit_flag == next(f for f in next(c for c in inv4["commands"] if c["name"] == "fit")["flags"] if f["flag"] == "--ephemeral"), "fit --ephemeral join changed"
    ctx.reference.validate(documents[INVS5], ctx.inventory5, registry)
    mfix = json.loads((arch / "docs/implementation/m1/metadata-v2/fixtures.json").read_bytes())
    for case in mfix["cases"]:
        value = copy.deepcopy(case["value"])
        if type(value.get("schemaMajor")) is int:
            value["schemaMajor"] += 1
        try:
            cm.admit(ctx.reference, registry, documents[ENV5], value, mfix["catalogue"], mfix["build"])
            accepted = True
        except (ValidationError, AssertionError, ctx.reference.AdmissionError):
            accepted = False
        assert accepted == case["accepted"], ("metadata case diverged under envelope5", case["id"])
        if case["accepted"]:
            assert not ctx.reference.ExactValidator(documents[ENV5], registry=registry).is_valid(case["value"])
    saved_argv, saved_stdout, captured = sys.argv, sys.stdout, io.StringIO()
    sys.argv, sys.stdout = [str(arch / "docs/implementation/m1/metadata-v2/check_metadata.py"), "--architecture", str(arch)], captured
    try:
        cm.main()
    finally:
        sys.argv, sys.stdout = saved_argv, saved_stdout
    historical = json.loads(captured.getvalue())
    assert historical["passed"] is True and historical["productQualification"] is False
    report["successorCompatibility"] = {"envelope5RestoresEnvelope4": True, "inventorySchema5RestoresSchema4": True, "inventory5RestoresInventory4": True,
                                        "fitEphemeralFlagJoinUnchanged": True, "metadataCasesThroughEnvelope5": len(mfix["cases"]),
                                        "historicalMetadataChecker": {"mode": "in-process under the closure hook and fresh-source loader; no child process",
                                                                      "passed": True, "cases": len(historical["cases"]), "schemasVerified": historical["schemasVerified"]}}

    # 3. coverage overlay: exact selectors/values, owners, milestones, the full owned validator with one scoped pre-existing workaround
    overlay = json.loads((HERE / "owner/implementation-coverage-successor.v1.json").read_bytes())
    base_raw = (arch / overlay["base"]["path"]).read_bytes()
    assert sha(base_raw) == overlay["base"]["sha256"] and len(base_raw) == overlay["base"]["bytes"]
    base = json.loads(base_raw)
    applied = owner.apply_overlay(base, overlay, with_workaround=False)
    sources = {}
    for key, pin in base["sources"].items():
        raw = (arch / pin["path"]).read_bytes()
        assert sha(raw) == pin["sha256"], pin["path"]
        sources[key] = json.loads(raw) if pin["path"].endswith(".json") else raw.decode()
    sources_next = dict(sources, commands=ctx.inventory5, **{"workflows-and-surfaces": owner.overridden_text(base["sources"]["workflows-and-surfaces"]["path"])})
    expected = planning.expected_groups(sources_next)
    inventory_doc = json.loads((arch / "docs/implementation/m1/repository-file-inventory.v3.json").read_bytes())
    files = {r["path"] for r in inventory_doc["files"]}
    for group, rows in applied["groups"].items():
        assert {r["id"] for r in rows} == set(expected[group]), group
        for row in rows:
            key, selector, value = expected[group][row["id"]]
            assert row["source"] == {"key": key, "selector": selector, "valueSha256": planning.digest(value)}, (group, row["id"])
            assert set(row["owners"]) <= files, (group, row["id"], row["owners"])
    renderer_m = {r["id"]: r["milestone"] for r in applied["groups"]["renderers"]}
    command_m = {r["id"]: r["milestone"] for r in applied["groups"]["commands"]}
    assert all(r["milestone"] >= renderer_m[f] for r in applied["groups"]["commands"] for f in r["formats"])
    assert all(r["milestone"] >= command_m[r["command"]] for r in applied["groups"]["workflowGoldens"])
    delivery = lambda data: {o for g in ("commands", "queryOperations", "renderers", "capabilityCells", "workflowGoldens") for r in data["groups"][g] for o in r["owners"]}
    assert delivery(applied) == delivery(base), "delivery owner set changed"
    workaround = overlay["scopedValidatorWorkaround"]["moduleFirstMilestone"]["add"]
    assert delivery(base) - set(base["moduleFirstMilestone"]) == set(workaround) and not set(base["moduleFirstMilestone"]) - delivery(base), "scoped condition is not exactly the pre-existing key-set gap"

    def validator(data, srcs):
        try:
            planning.validate_coverage(data, srcs, inventory_doc)
            return "valid"
        except ValueError as exc:
            return str(exc)
    unscoped = [validator(base, sources), validator(applied, sources_next)]
    assert unscoped == ["Missing/extra module milestone prerequisite"] * 2, unscoped
    empty = {"rowChanges": [], "rowAdditions": [], "reviewIssueAdditions": [], "scopedValidatorWorkaround": overlay["scopedValidatorWorkaround"]}
    scoped_base, scoped_overlay = owner.apply_overlay(base, empty, True), owner.apply_overlay(base, overlay, True)
    scoped = [validator(scoped_base, sources), validator(scoped_overlay, sources_next)]
    assert scoped == ["valid", "valid"], scoped
    c2 = copy.deepcopy(scoped_overlay)
    next(r for r in c2["groups"]["commands"] if r["id"] == "fit")["parityFields"] = next(r for r in base["groups"]["commands"] if r["id"] == "fit")["parityFields"]
    c2_result = validator(c2, sources_next)
    assert c2_result == "Command metadata drift", c2_result
    register = json.loads((HERE / "owner/design-obligations.v1.json").read_bytes())
    feature_rows = {r["id"]: r for r in scoped_overlay["groups"]["reportFeatures"]}
    issues = {r["id"]: r for r in scoped_overlay["reviewIssues"]}
    for obligation in register["obligations"]:
        row = feature_rows[owner.FEATURES[obligation["featureId"]][0]]
        assert obligation["id"] in issues
        if obligation["blocksReportDesignReadiness"]:
            assert obligation["id"] in row["reviewIssues"] and "an unavailable feature-state disclosure does not satisfy this row" in row["verification"]["method"]
        else:
            assert obligation["id"] not in row["reviewIssues"] and issues[obligation["id"]]["affects"] == [], "conditional obligation holds a row open"
    c01_rows = []
    for group, ids in (("commands", owner.C01_COMMANDS), ("renderers", owner.C01_RENDERERS), ("workflowGoldens", owner.C01_GOLDENS)):
        rows_ = [r for r in scoped_overlay["groups"][group] if r["id"] in ids]
        assert len(rows_) == len(ids), (group, ids)
        for row in rows_:
            assert "RP-OBL-C01" in row["reviewIssues"] and "Open RP-OBL-C01" in row["verification"]["method"], (group, row["id"])
            c01_rows.append(group + ":" + row["id"])
    golden_row = next(r for r in scoped_overlay["groups"]["workflowGoldens"] if r["id"] == "interrupted-before-settle")
    assert golden_row["sourceClass"] == "interrupted" and golden_row["sourceExitCode"] == 130 and issues["RP-OBL-C01"]["standing"].startswith("open")
    assets = "crates/reporting/src/assets.rs"
    assets_rows = [(g, r["id"], r["milestone"]) for g in ("commands", "queryOperations", "renderers", "capabilityCells", "workflowGoldens") for r in base["groups"][g] if assets in r["owners"]]
    assert assets_rows == [("commands", "version", "M1")], assets_rows
    workaround_values = {}
    for value in ("M0", "M1", "M6"):
        trial = owner.apply_overlay(base, overlay, True)
        trial["moduleFirstMilestone"][assets] = value
        workaround_values[value] = validator(trial, sources_next)
    assert workaround_values["M0"] == workaround_values["M1"] == "valid" and workaround_values["M6"] != "valid", workaround_values
    report["coverageOverlay"] = {"rowsRechecked": sum(len(r) for r in applied["groups"].values()), "rowChanges": len(overlay["rowChanges"]), "rowAdditions": len(overlay["rowAdditions"]),
                                 "reviewIssueAdditions": len(overlay["reviewIssueAdditions"]),
                                 "ownedValidatorUnscoped": {"base": unscoped[0], "overlay": unscoped[1]},
                                 "scopedWorkaround": workaround, "ownedValidatorScoped": {"base": scoped[0], "overlay": scoped[1]},
                                 "reviewC2ControlWithoutFitParityFields": c2_result, "historicalCoverageBytesUnchanged": True,
                                 "rpObligationC01Rows": c01_rows, "assetsDeliveryRows": assets_rows, "workaroundValueControls": workaround_values,
                                 "conditionalRpDo02HoldsNoRowOpen": True}

    # 4. passage overrides (parents unchanged; before-text exact)
    overrides = json.loads((HERE / "owner/passage-overrides.v1.json").read_bytes())["overrides"]
    for row in overrides:
        assert (arch / row["path"]).read_text().splitlines()[row["line"] - 1] == row["before"]
    report["passageOverrides"] = [(r["path"].rsplit("/", 1)[-1], r["line"]) for r in overrides]

    # 5. gating, feature map, design-obligation register, goldens, derivations
    html_commands = sorted(c["name"] for c in ctx.inventory5["commands"] if "html" in c["formats"])
    assert html_commands == sorted(ctx.schema["$defs"]["ReportCommand"]["enum"])
    inventory_text = (arch / "docs/v2/architecture/prototype-report-inventory.md").read_text()
    advertised = re.search(r"HTML is advertised by exactly (.*?)\. Graph", inventory_text, re.S).group(1)
    assert sorted(re.findall(r"`([a-z-]+)`", advertised)) == html_commands
    rows = re.findall(r"^### (R\d\d) — ", inventory_text, re.M)
    assert rows == ["R%02d" % i for i in range(1, 25)] and sorted(fixture["featureMap"]) == rows
    per_command = {b_["if"]["properties"]["command"]["const"]: b_["then"]["properties"] for b_ in ctx.schema["allOf"] if "command" in b_.get("if", {}).get("properties", {})}
    used = {s["featureId"] for props in per_command.values() for s in props["featureStates"]["const"]}
    assert used == set(ctx.schema["$defs"]["FeatureId"]["enum"]) == set(owner.FEATURES)
    register_ids = {r["id"]: r for r in register["obligations"]}
    for cmd, props in per_command.items():
        for state in props["featureStates"]["const"]:
            row_, obligation, reason, views = owner.FEATURES[state["featureId"]]
            assert state["view"] in props["supportedReportViews"]["const"] and state["obligationId"] == obligation and state["reason"] == reason
            assert register_ids[obligation]["featureId"] == state["featureId"]
    for rid, entries in fixture["featureMap"].items():
        assert entries and all(set(e) == {"kind", "ref"} for e in entries), rid
        for e in entries:
            if e["kind"] == "report":
                pointer_get(ctx.schema, e["ref"])
            elif e["kind"] == "envelope":
                pointer_get(documents[ENV5], e["ref"])
            elif e["kind"] == "featureState":
                assert owner.FEATURES[e["ref"]][0] == rid
            elif e["kind"] == "obligation":
                assert e["ref"] in fixture["obligations"]
            else:
                raise AssertionError("prose mapping " + rid)
    assert register["readiness"]["reportDesign"] == "blocked" and register["readiness"]["auditG10"] == "open"
    assert register["readiness"]["blockers"] == [r["id"] for r in register["obligations"] if r["blocksReportDesignReadiness"]]
    required_keys = {"id", "featureId", "requirement", "owningDesignUnit", "status", "gapKind", "milestone", "gate", "closureCriterion", "carrierSuccessor", "blocksReportDesignReadiness", "standing"}
    for row in register["obligations"]:
        assert set(row) - {"integrationNote"} == required_keys and row["milestone"] == "M4" and row["closureCriterion"] and row["carrierSuccessor"], row["id"]
        assert row["standing"].startswith("proposal to the owning design unit; not accepted"), row["id"]
        assert (arch / row["owningDesignUnit"]["document"]).is_file(), row["owningDesignUnit"]["document"]
    integration = {r["id"]: r for r in register["integrationObligations"]}
    assert list(integration) == ["RP-OBL-C01", "RP-OBL-L01", "RP-OBL-K01"] and register["readiness"]["m1FinalIntegrationBlockers"] == ["RP-OBL-C01", "RP-OBL-K01"]
    parent = integration["RP-OBL-C01"]["parentDependency"]
    envelope5_raw = (HERE / "owner/command-envelope.v5.schema.json").read_bytes()
    assert sha(envelope5_raw) == parent["envelope6ParentEnvelope5Sha256"] == owner.ENVELOPE5_SHA256 and len(envelope5_raw) == 36852, "envelope5 bytes changed: envelope6 parent binding broken"
    assert parent["adoptedByThisCandidate"] is False and integration["RP-OBL-C01"]["status"] == "pending-integration"
    for name in ("report-projection.schema.json", "owner/command-envelope.v5.schema.json", "owner/command-inventory.v5.schema.json", "owner/command-inventory.v5.json"):
        assert "command-envelope:6" not in (HERE / name).read_text(), "envelope6 silently adopted in " + name
    native_text = (arch / "docs/v2/contracts/product-v1/native-evidence.md").read_text()
    evidence = {"F03-unit-membership-owned": "UnitMembershipV1" in native_text and "WorkspaceUnitV2" in native_text,
                "F05-entry-points-owned-natively": "entryPoints" in json.dumps(documents["urn:opensip:product-v1:native:evidence-schemas:v2"]["$defs"].get("FrameworkRecognitionV1", {})),
                "R14-run-show-operation-exists": {"run.show", "run.list"} <= set(documents[GQ]["$defs"]["Operation"]["enum"]),
                "R03-no-owned-duration-member": not any(("duration" in n.lower() or "elapsed" in n.lower()) for n in property_names(documents[INV], set()) | property_names(documents[C.split("#")[0]], set()))}
    assert all(evidence.values()), evidence
    report["designObligations"] = {"count": len(register["obligations"]), "reportDesignBlockers": register["readiness"]["blockers"], "ownerEvidence": evidence,
                                   "integrationObligations": {k: v["status"] for k, v in integration.items()}, "m1FinalIntegrationBlockers": register["readiness"]["m1FinalIntegrationBlockers"],
                                   "envelope6": {"parentEnvelope5Sha256": parent["envelope6ParentEnvelope5Sha256"], "envelope5BytesUnchanged": True, "adopted": False}}
    assert "step-attempt-ledger" not in used and "run-history-selection" not in used
    for base_name, base_doc in fixture["bases"].items():
        for res in base_doc["panels"].get("graph", {}).get("data", {}).get("subjectResolution", []):
            if res["state"] == "resolved":
                descriptor = dict({"schemaVersion": 3}, **res["endpoint"])
                assert M.subject_id(res["endpoint"]) == "subject3:" + ctx.reference.identity("evaluation-subject", descriptor) == identity_model.identifier("evaluation-subject", descriptor) == res["subjectId"]
    aggregate_results = []
    for golden in fixture["aggregateCases"]:
        try:
            got = M.invocation_aggregate(golden["steps"], golden["cancellation"])
            result = "accept"
        except M.ModelRefusal as exc:
            got, result = None, exc.code
        if "refusal" in golden:
            assert result == golden["refusal"], (golden["id"], result)
        else:
            assert result == "accept" and ctx.reference.equal_typed(got, golden["expect"]), golden["id"]
            ctx.reference.validate({"$ref": C + "StepTermination"}, got, registry)
        aggregate_results.append((golden["id"], result if result != "accept" else got["class"]))
    report["aggregateCases"] = aggregate_results
    delivery_results = {}
    for golden in fixture["deliveryGoldens"]:
        row = next(c for c in ctx.inventory5["commands"] if c["name"] == golden["command"])
        recomputed = M.delivery_outcome(golden["format"], golden["priorSteps"], golden["render"], golden["envelope"], golden["committedRunId"], row, golden["cancellation"])
        assert ctx.reference.equal_typed(recomputed, {k: v for k, v in golden.items() if k not in ("id", "scenario", "command", "priorSteps", "render", "committedRunId")}), golden["id"]
        assert [s["termination"] for s in golden["priorSteps"]] == recomputed["priorStepTerminations"], "prior step terminations rewritten"
        ctx.reference.validate({"$ref": C + "StepTermination"}, recomputed["aggregate"], registry)
        assert outcome(admit_envelope, ctx, recomputed["envelope"], golden["command"]) == ("accept", None), golden["id"]
        delivery_results.setdefault(golden["scenario"], set()).add((recomputed["aggregate"]["class"], recomputed["aggregate"].get("domainDetail", {}).get("code"), recomputed["exitCode"],
                                                                    recomputed["renderAttempts"], recomputed["delivered"] is not None))
    assert all(len(v) == 1 for v in delivery_results.values()), "renderers disagree"
    delivery_results = {k: next(iter(v)) for k, v in delivery_results.items()}
    assert delivery_results["fit-query-refused-required-render-failed"][:2] == ("operational-failed", "DELIVERY.RENDERER_FAILED_AFTER_COMMIT")
    assert delivery_results["fit-query-refused-optional-render-failed"][:2] == ("request-rejected", "QUERY.VIEW_UNKNOWN")
    assert delivery_results["fit-query-refused-no-render-selected"][3] == 0
    assert delivery_results["fit-query-io-failed-required-render-failed-tie"][1] == "evidence.purged"
    assert delivery_results["candidates-no-run-query-refused-required-render-failed"][1] == "DELIVERY.REQUIRED_PROJECTION_FAILED"
    assert delivery_results["fit-signal-during-required-render-before-settle"][0] == "interrupted" and delivery_results["fit-signal-during-required-render-before-settle"][2] == 130
    interrupted = next(g for g in fixture["deliveryGoldens"] if g["scenario"] == "fit-signal-during-required-render-before-settle")
    assert interrupted["aggregate"].get("runId") == interrupted["committedRunId"] and interrupted["envelope"]["kind"] == "run" and interrupted["delivered"] is None
    assert delivery_results["fit-analysis-rejected-query-skipped-render-written"][:3] == ("request-rejected", "CONFIG.INVALID", 2)
    assert delivery_results["fit-analysis-rejected-query-skipped-required-render-failed"][1] == "DELIVERY.REQUIRED_PROJECTION_FAILED"
    assert delivery_results["fit-analysis-rejected-query-skipped-optional-render-failed"][:2] == ("request-rejected", "CONFIG.INVALID")
    assert delivery_results["audit-baseline-rejected-comparison-skipped-render-written"][:2] == ("request-rejected", "CONFIG.INVALID")
    assert delivery_results["audit-baseline-rejected-comparison-skipped-required-render-failed"][1] == "DELIVERY.RENDERER_FAILED_AFTER_COMMIT"
    for golden in fixture["deliveryGoldens"]:
        if "skipped" in golden["scenario"]:
            assert any(s["outcome"] == "skipped" and s["skipReason"] for s in golden["priorSteps"]) and any(t == builder.SKIPPED_TERMINATION for t in golden["priorStepTerminations"])
    pending_results = {}
    for row in fixture["pendingGoldens"]:
        aggregate = M.invocation_aggregate(row["steps"], row["cancellation"])
        assert ctx.reference.equal_typed(aggregate, row["aggregate"]) and "runId" not in aggregate and aggregate["class"] == "interrupted"
        assert row["countsAsDeliveredBehavior"] is False and row["status"] == "pending-integration" and row["obligation"] == "RP-OBL-C01"
        for name, form in row["candidateForms"].items():
            result, detail = outcome(admit_envelope, ctx, form["envelope"], row["command"])
            assert result == form["expectedEnvelope5Outcome"], (row["id"], name, result, detail)
            pending_results.setdefault(row["command"] + ":" + name, set()).add(result)
    assert all(len(v) == 1 for v in pending_results.values())
    report["pendingGoldens"] = {"rows": len(fixture["pendingGoldens"]), "countedAsDelivered": 0, "obligation": "RP-OBL-C01",
                                "envelope5Outcomes": {k: next(iter(v)) for k, v in pending_results.items()}}
    tmax = builder.pinned_termination(4096, "run3:" + "a" * 64, "\x01")
    ctx.reference.validate({"$ref": C + "StepTermination"}, tmax, registry)
    ctx.reference.typed(tmax, 3)
    tmax_raw = M.canonical(tmax)
    try:
        ctx.reference.parse(tmax_raw)
        codec_outcome = "admitted"
    except ctx.reference.AdmissionError as exc:
        codec_outcome = "refused " + str(exc)[:60]
    assert ctx.budget["envelopeMaxCanonicalBytes"] < len(tmax_raw) <= ctx.derivations["stepTerminationStructuralMaxBytes"] and codec_outcome.startswith("refused")
    report["codecReachability"] = {"maximalStepTerminationBytes": len(tmax_raw), "schemaValid": True, "exactCodecParse": codec_outcome,
                                   "structuralBound": ctx.derivations["stepTerminationStructuralMaxBytes"], "consequence": "structural ledger bound kept; codec record bound pending owner statement RP-OBL-L01"}
    report["deliveryGoldens"] = {"rows": len(fixture["deliveryGoldens"]), "formats": ["human", "json", "agent", "html"],
                                 "scenarios": {k: {"class": v[0], "detail": v[1], "exitCode": v[2], "renderAttempts": v[3], "delivered": v[4]} for k, v in delivery_results.items()}}
    depths = embedding_depths(ctx.schema, documents)
    gains = {}
    for ref_, depth in depths.items():
        if ref_ in NATIVE_OFFSETS:
            gains[ref_] = depth - NATIVE_OFFSETS[ref_]
        else:
            assert not is_container(ref_, documents), "embedded container without native offset: " + ref_
    assert ctx.budget["maxJsonDepth"] == ctx.budget["ownerCodecDepth"] + max(gains.values()) == ctx.reference.MAX_DEPTH + max(gains.values())
    assert ctx.budget["maxSubjectIndexRows"] == owner.subject_index_bound()
    assert ctx.budget["documentMaxBytes"] == ctx.derivations["documentMaxBytes"] and ctx.budget["ledgerMaxBytes"] == ctx.derivations["ledgerMaxBytes"]
    for base_doc in fixture["bases"].values():
        assert M.effective_exploration_budget(ctx.budget, base_doc["envelope"], base_doc["invocationLedger"], ctx.schema["required"]) == ctx.budget["explorationMaxCanonicalBytes"]
    report["derivations"] = {"maxEmbeddingGain": max(gains.values()), "subjectIndexBound": owner.subject_index_bound(), "documentMaxBytes": ctx.derivations["documentMaxBytes"],
                             "ledgerMaxBytes": ctx.derivations["ledgerMaxBytes"], "stepTerminationStructuralMaxBytes": ctx.derivations["stepTerminationStructuralMaxBytes"]}

    # 6. cases
    ctx.material = builder.material()
    ctx.owner = M.MockGraphOwner(ctx.material["facts"], ctx.material["template"])
    ctx.worst = worst_values(ctx)
    env_results, mismatches = [], []
    for case in fixture["envelopeCases"]:
        env = apply_ops(ctx, case["envelope"], case["ops"], as_bytes=False)
        result, detail = outcome(admit_envelope, ctx, env, case["command"])
        if result != case["expect"]:
            mismatches.append((case["id"], result, case["expect"], detail))
        env_results.append({"id": case["id"], "result": result})
    report["envelopeCases"] = env_results
    results = []
    for case in fixture["reportCases"]:
        raw = apply_ops(ctx, fixture["bases"][case["base"]], case["ops"])
        started = time.perf_counter()
        result, detail = outcome(admit_document, ctx, raw)
        if result != case["expect"]:
            mismatches.append((case["id"], result, case["expect"], detail))
        results.append({"id": case["id"], "result": result, "detail": detail, "bytes": len(raw), "referenceSeconds": round(time.perf_counter() - started, 3)})
    assert not mismatches, "case outcomes diverged:\n" + "\n".join(map(repr, mismatches))
    report["reportCases"] = results
    report["reviewCounterexamples"] = {k: next(r["result"] for r in results + env_results if r["id"] == v) for k, v in fixture["reviewCounterexamples"].items()}
    report["reviewCounterexamples"]["RPR3-3/D1-aggregate"] = dict(aggregate_results)["review-D1-query-refused-then-required-render-failed"]
    report["reviewCounterexamples"]["RPR3-3/D2-aggregate"] = dict(aggregate_results)["review-D2-interrupted-without-cancellation"]
    report["reviewCounterexamples"]["RPR3-5/C2-control"] = c2_result
    report["reviewCounterexamples"]["RPR4-2/skipped-request-rejected-aggregate"] = dict(aggregate_results)["review-RPR4-2-skipped-required-request-rejected"]
    report["reviewCounterexamples"]["RPR4-2/skipped-indeterminate-aggregate"] = dict(aggregate_results)["review-RPR4-2-skipped-required-indeterminate"]
    for name, golden in fixture["staticParityGoldens"].items():
        base_doc = fixture["bases"][name]
        text = M.static_parity_text(base_doc["envelope"], next(c for c in ctx.inventory5["commands"] if c["name"] == base_doc["command"]), base_doc["disclosures"]).encode()
        assert sha(text) == golden["textSha256"] and len(text) == golden["textBytes"]
    audit = fixture["bases"]["audit-full"]
    index = {r["subjectId"]: r for r in audit["panels"]["graph"]["data"]["subjectIndex"]}
    lookalike = next(f for f in audit["envelope"]["findings"] if f["subjectPath"] == "src/legacy.js" and f["subjectId"] not in index)
    assert lookalike and all(f["subjectId"] in index for f in audit["envelope"]["findings"] if f["findingId"] != lookalike["findingId"])

    # 7. owner page law under reference test bounds, byte law through a re-issuing mock owner, worst-case sizes
    report["graphPageLawControls"] = graph_page_law_controls(ctx)
    report["byteLawScenario"] = byte_law_scenario(ctx, fixture, builder, owner)
    report["worstCase"] = worst_case_table(ctx)

    report["closure"] = dict({k: v for k, v in closure.counts.items() if k != "declaredOutWrites"}, freshSourceLoader=True, childProcesses=0, declaredOut=str(args.out) if args.out else None,
                             declaredOutWrites="observed after this result is written and printed on stdout (a result cannot count its own write)",
                             aliasPolicy="realpath and case-folded spellings; pinned identity by (st_dev, st_ino)",
                             hostTrust="filesystem, interpreter, reference environment and the start-time pin file are trusted; a concurrent writer between verification and consuming read is not excluded")
    report["passed"] = True
    report["productQualification"] = False
    if args.trace_closure:
        args.trace_closure.write_text(json.dumps({"roots": closure.roots, "files": sorted(closure.files), "directories": sorted(closure.directories)}, indent=1))
    if args.out:
        args.out.write_text(json.dumps(report, indent=1, ensure_ascii=False) + "\n")
        assert closure.counts["declaredOutWrites"] == 1, closure.counts
        print("declared-out writes observed:", closure.counts["declaredOutWrites"])
    summary = {k: report.get(k) for k in ("passed", "subjectFiles", "subjectManifestSha256", "externalPins", "projectionSchemaSha256", "closure", "bytecodeDemo", "aliasProbe",
                                          "pendingGoldens", "codecReachability", "successorCompatibility",
                                          "coverageOverlay", "designObligations", "reviewCounterexamples", "deliveryGoldens", "aggregateCases", "graphPageLawControls", "byteLawScenario",
                                          "worstCase", "derivations")}
    print(json.dumps(summary, indent=1, ensure_ascii=False))
    print("reportCases:", len(results), "accepted:", sum(r["result"] == "accept" for r in results), "envelopeCases:", len(env_results))


def graph_page_law_controls(ctx):
    """host.testBounds may only lower caps for reference controls: those pages satisfy the law under their test bounds and are refused under public bounds."""
    M, material = ctx.M, ctx.material
    public = ctx.budget["graphPublicBounds"]
    base = {"schemaFamily": "opensip.product.query", "schemaMajor": 3, "projectId": material["project"], "view": {"runId": material["run"]}, "completeness": "best-effort"}
    reach = dict(base, operation="graph.reach", params={"relation": "calls", "minResolution": "resolved-callee", "direction": "outgoing", "start": material["main"], "maxDepth": 2, "includeStart": False})
    incoming = dict(base, operation="graph.neighbors", params={"relation": "imports", "minResolution": "resolved-target", "direction": "incoming", "endpoint": material["legacy"]})
    rows = []
    for label, request, cap, size in (("truncated-bound-last-page", reach, 3, 100), ("lower-bound-truncated-page", reach, 3, 2), ("exactly-at-cap-complete", incoming, 1, 100)):
        request = dict(copy.deepcopy(request), page={"size": size})
        bounds = dict(public, maxItemsPerOperation=cap)
        response = M.MockGraphOwner(material["facts"], material["template"], max_items_per_operation=cap).execute(request)
        ctx.reference.validate({"$ref": G + "GraphQueryResponseV1"}, response, ctx.registry)
        context = response["context"]
        under_test = M.page_law(context, len(response["items"]), size, bounds)
        under_public = M.page_law(context, len(response["items"]), size, public)
        assert under_test is None
        rows.append({"control": label, "coverage": context["traversalCoverage"], "countBasis": context["countBasis"], "items": len(response["items"]), "cursor": "nextCursor" in context,
                     "continuation": M.continuation_for(context), "lawUnderTestBounds": "lawful", "lawUnderPublicBounds": under_public or "lawful"})
    assert rows[0]["lawUnderPublicBounds"] != "lawful" and rows[1]["lawUnderPublicBounds"] != "lawful" and rows[2]["lawUnderPublicBounds"] == "lawful"
    law = lambda resp, size, bounds, position=0: M.page_law(resp["context"], len(resp["items"]), size, bounds, position)

    def walk(owner, request, size, bounds):
        pages, position, cursor = [], 0, None
        while True:
            page = {"size": size}
            if cursor is not None:
                page["cursor"] = cursor
            req = dict(copy.deepcopy(request), page=page)
            resp = owner.execute(req)
            ctx.reference.validate({"$ref": G + "GraphQueryResponseV1"}, resp, ctx.registry)
            violation = law(resp, size, bounds, position)
            assert violation is None, violation
            pages.append(resp)
            cursor = resp["context"].get("nextCursor")
            if cursor is None:
                return pages
            position += len(resp["items"])
            assert cursor == M.graph_cursor(req, position)

    neighbors = dict(base, operation="graph.neighbors", params={"relation": "calls", "minResolution": "resolved-callee", "direction": "outgoing", "endpoint": material["main"]})
    unbounded = M.MockGraphOwner(material["facts"], material["template"]).execute(dict(copy.deepcopy(neighbors), page={"size": 1000}))
    positive = []
    exact_pages = walk(M.MockGraphOwner(material["facts"], material["template"]), neighbors, 50, public)
    assert len(exact_pages) > 2 and [i for p in exact_pages for i in p["items"]] == unbounded["items"]
    assert all(p["context"]["traversalCoverage"] == "truncated-page" for p in exact_pages[:-1]) and exact_pages[-1]["context"]["traversalCoverage"] == "complete"
    positive.append({"control": "exact-multi-page-partial-set", "pageRows": [len(p["items"]) for p in exact_pages], "totalItems": exact_pages[0]["context"]["totalItems"],
                     "lastCoverage": "complete", "concatenationEqualsUnboundedAnswer": True})
    cap = 60
    capped_pages = walk(M.MockGraphOwner(material["facts"], material["template"], max_items_per_operation=cap), neighbors, 25, dict(public, maxItemsPerOperation=cap))
    last = capped_pages[-1]["context"]
    assert [i for p in capped_pages for i in p["items"]] == unbounded["items"][:cap] and all(p["context"]["totalItems"] == p["context"]["producedItems"] == cap for p in capped_pages)
    assert last["traversalCoverage"] == "truncated-bound" and last["countBasis"] == "lower-bound" and "nextCursor" not in last
    assert all(law(p, 25, public, i * 25) is not None for i, p in enumerate(capped_pages))
    positive.append({"control": "capped-multi-page-partial-set-under-test-bound-60", "pageRows": [len(p["items"]) for p in capped_pages], "lastCoverage": "truncated-bound",
                     "concatenationEqualsProducedPrefix": True, "refusedUnderPublicBounds": True})
    limit, start = public["maxItemsPerOperation"], material["main"]
    facts = [{"factId": "fact2:" + sha(b"control-cap-%d" % i), "relation": "calls", "resolution": "resolved-callee", "source": start,
              "target": {"universe": start["universe"], "kind": "symbol", "nativeSubjectId": "ts:src/cap.ts#c%06d" % i}} for i in range(limit + 1)]
    cap_owner = M.MockGraphOwner(facts, material["template"])
    first_req = dict(copy.deepcopy(neighbors), page={"size": 100})
    first = cap_owner.execute(first_req)
    last_position = limit - 100
    final = cap_owner.execute(dict(copy.deepcopy(neighbors), page={"size": 100, "cursor": M.graph_cursor(first_req, last_position)}))
    for resp, position in ((first, 0), (final, last_position)):
        ctx.reference.validate({"$ref": G + "GraphQueryResponseV1"}, resp, ctx.registry)
        assert law(resp, 100, public, position) is None
    assert "nextCursor" in first["context"] and "nextCursor" not in final["context"] and final["context"]["traversalCoverage"] == "truncated-bound" and final["context"]["countBasis"] == "lower-bound"
    assert [i["target"]["nativeSubjectId"] for i in final["items"]] == ["ts:src/cap.ts#c%06d" % i for i in range(last_position, limit)]
    positive.append({"control": "public-item-cap-reached", "facts": limit + 1, "producedItems": final["context"]["producedItems"], "firstPageCoverage": first["context"]["traversalCoverage"],
                     "lastPagePosition": last_position, "lastPageCoverage": "truncated-bound", "lastPageIsProducedSuffix": True})
    small = M.MockGraphOwner(material["facts"], material["template"]).execute(dict(copy.deepcopy(neighbors), page={"size": 25}))
    big = M.MockGraphOwner(material["facts"], material["template"]).execute(dict(copy.deepcopy(neighbors), page={"size": 100}))
    assert small["items"] == big["items"][:25] and small["context"]["totalItems"] == big["context"]["totalItems"] == big["context"]["producedItems"]
    positive.append({"control": "re-issued-smaller-first-page-is-prefix", "sizes": [25, 100]})
    last_page, last_start = exact_pages[-1], sum(len(p["items"]) for p in exact_pages[:-1])
    middle = copy.deepcopy(exact_pages[0])
    middle["context"].pop("nextCursor")
    middle["context"]["traversalCoverage"] = "complete"
    negatives = {"continuation-dropped-mid-set": law(middle, 50, public),
                 "total-not-produced": law(dict(last_page, context=dict(last_page["context"], totalItems=last_page["context"]["totalItems"] + 1)), 50, public, last_start),
                 "page-beyond-produced-prefix": law(last_page, 50, public, last_start + 1),
                 "last-page-at-wrong-position": law(last_page, 50, public, last_start - 1)}
    assert all(v is not None for v in negatives.values()), negatives
    return {"testBoundControls": rows, "positiveControls": positive, "modelNegatives": negatives}


def worst_values(ctx):
    M = ctx.M
    wide = "\U0001F600"
    universe = ctx.material["main"]["universe"]
    symbols = [{"universe": universe, "kind": "symbol", "nativeSubjectId": wide * 4093 + "%03d" % i} for i in range(130)]
    segments, used = [], 0
    while used + (255 if not segments else 256) <= 4096:
        used += 255 if not segments else 256
        segments.append(wide * 255)
    finding = {"findingId": "finding3:" + "a" * 64, "ruleId": "a" * 128, "subjectId": "subject3:" + "a" * 64, "subjectPath": "/".join(segments), "subjectKind": "symbol",
               "qualifiedName": wide * 4096, "severity": "warning", "messageCode": wide * 4096, "correspondence": {"state": "matched", "reason": None},
               "fingerprint": "finding-key2:" + "a" * 64, "waived": False, "parameterDigest": "a" * 64, "partialFingerprints": {"opensip/finding-key2": "finding-key2:" + "a" * 64}}
    facts = [{"factId": "fact2:" + sha(b"worst-%d" % i), "relation": "calls", "resolution": "resolved-callee", "source": symbols[0], "target": symbols[i]} for i in range(1, 121)]
    chain = [{"factId": "fact2:" + sha(b"chain-%d" % i), "relation": "calls", "resolution": "resolved-callee", "source": symbols[i], "target": symbols[i + 1]} for i in range(64, 128)]
    return {"finding": finding, "symbols": symbols, "facts": facts, "chain": chain}


def worst_case_table(ctx):
    M, ref, reg, w = ctx.M, ctx.reference, ctx.registry, ctx.worst
    ref.validate({"$ref": C + "FindingSurface"}, w["finding"], reg)
    owner = M.MockGraphOwner(w["facts"] + w["chain"], ctx.material["template"])
    base = {"schemaFamily": "opensip.product.query", "schemaMajor": 3, "projectId": ctx.material["project"], "view": {"runId": ctx.material["run"]}, "completeness": "best-effort"}
    neighbors = owner.execute(dict(base, operation="graph.neighbors", page={"size": 100}, params={"relation": "calls", "minResolution": "resolved-callee", "direction": "outgoing", "endpoint": w["symbols"][0]}))
    path = owner.execute(dict(base, operation="graph.path", page={"size": 1}, params={"relation": "calls", "minResolution": "resolved-callee", "direction": "outgoing", "start": w["symbols"][64], "target": w["symbols"][128], "maxDepth": 64}))
    for response in (neighbors, path):
        ref.validate({"$ref": G + "GraphQueryResponseV1"}, response, reg)
    assert path["items"] and path["items"][0]["hopCount"] == 64 and neighbors["context"]["traversalCoverage"] == "truncated-page"
    envelope_cap, cap = ctx.budget["envelopeMaxCanonicalBytes"], ctx.budget["explorationMaxCanonicalBytes"]
    finding_bytes = len(M.canonical(w["finding"]))
    return {"label": "owner-schema-valid constructions answered by the mock owner under the query contract; sizes only, not performance",
            "FindingSurface": finding_bytes, "worstFindingsWithinEnvelopeCodec": envelope_cap // finding_bytes,
            "neighborRow": len(M.canonical(neighbors["items"][0])), "neighborPage100Bytes": len(M.canonical(neighbors)), "neighborPageFitsOwnerCodec": len(M.canonical(neighbors)) <= envelope_cap,
            "path64HopResponseBytes": len(M.canonical(path)), "path64HopFitsExplorationCap": len(M.canonical(path)) <= cap}


def byte_law_scenario(ctx, fixture, builder, owner_builder):
    M, w = ctx.M, ctx.worst
    base = copy.deepcopy(fixture["bases"]["default-run"])
    env = base["envelope"]
    template = copy.deepcopy(env["findings"][0])
    w0, w1 = w["symbols"][0], w["symbols"][1]
    findings = [dict(template, findingId="finding3:" + sha(b"scenario-0"), subjectId=M.subject_id(w0), severity="error"),
                dict(template, findingId="finding3:" + sha(b"scenario-1"), subjectId=M.subject_id(w1), severity="warning")]
    env["findings"] = sorted(findings, key=lambda f: f["findingId"].encode())
    resolution = [{"subjectId": M.subject_id(e), "state": "resolved", "endpoint": e} for e in (w0, w1)]
    facts = w["facts"]
    material = ctx.material
    entries = []
    for i in range(2000):
        entry = copy.deepcopy(material["coverage"])
        entry["key"]["subjectScopeCommitment"] = "sha256:" + sha(b"scenario-scope-%d" % i)
        entries.append(entry)
    history = base["panels"]["history"]["data"]
    rows = []
    for row in history["runs"]:
        row = copy.deepcopy(row)
        if row["state"] == "present":
            row["findings"] = sorted([dict(template, findingId="finding3:" + sha(("hist-%s-%d" % (row["runId"], i)).encode())) for i in range(3000)], key=lambda f: f["findingId"].encode())
            row.pop("findingsProjection", None)
        rows.append(row)
    sources = {"catalog": base["panels"]["catalog"]["data"], "evidence": {"coverageId": material["coverageId"], "entries": entries, "cap": ctx.budget["maxEvidenceEntries"]},
               "history": {"selection": history["selection"], "runs": rows, "cap": ctx.budget["maxHistoryFindingsPerRun"]}}
    budget_bytes = M.effective_exploration_budget(ctx.budget, env, base["invocationLedger"], ctx.schema["required"])
    outcomes = []
    for _ in range(2):
        mock = M.MockGraphOwner(facts, material["template"])
        plan = M.plan_slots(resolution, env["projectId"], env["run"]["runId"])
        panels = M.project_exploration(sources, owner_builder.PROVENANCE, owner_builder.PANELS["default"], budget_bytes, resolution, mock, plan)
        outcomes.append((panels, [c["page"]["size"] for c in mock.calls]))
    assert M.canonical(outcomes[0][0]) == M.canonical(outcomes[1][0]) and outcomes[0][1] == outcomes[1][1], "projector not deterministic"
    panels, sizes = outcomes[0]
    fresh = M.MockGraphOwner(facts, material["template"])
    for slot in panels["graph"]["data"]["slots"]:
        assert M.canonical(slot["response"]) == M.canonical(fresh.execute(slot["request"])), "embedded page is not the owner answer to its own request"
    base["panels"] = panels
    builder.refresh(base)
    admit_document(ctx, M.canonical(base))
    graph = panels["graph"]["data"]
    reduced = [s for s in graph["slots"] if s["hostProjection"]["pageSizeCause"] == "byte-budget-reduced"]
    assert reduced and all(s["response"]["context"]["traversalCoverage"] == "truncated-page" for s in reduced)
    history_proj = [r["findingsProjection"] for r in panels["history"]["data"]["runs"] if r["state"] == "present"] if panels["history"]["state"] == "present" else []
    return {"deterministic": True, "effectiveExplorationBudget": budget_bytes, "reissuedPageSizes": sizes, "embeddedPagesEqualFreshOwnerAnswers": True, "documentAdmits": True,
            "panelsBytes": len(M.canonical(panels)), "evidence": panels["evidence"]["data"]["entriesProjection"] if panels["evidence"]["state"] == "present" else panels["evidence"],
            "slots": [(s["purpose"], s["request"]["page"]["size"], len(s["response"]["items"]), s["hostProjection"]["pageSizeCause"]) for s in graph["slots"]],
            "slotsProjection": graph["slotsProjection"], "historyProjections": history_proj}


if __name__ == "__main__":
    sys.setrecursionlimit(20000)
    main()
