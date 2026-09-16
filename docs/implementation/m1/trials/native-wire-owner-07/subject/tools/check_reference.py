"""Reference-owner, admission-vector, ECMA dialect, owner-successor, path-site, representability, send-schedule and
wire-example checks (candidate 06). Runs the pinned reference models (native_evidence_model.v2, provider_startup_model.v1,
provider_wire_model.v1, identity-model.v3) both as pinned and with the owner pattern-evaluation successor installed in memory, and the
pinned ECMA-262 engine; never claims product execution. Architecture pins are verified by check.py before this module
imports any model."""
import copy, hashlib, importlib.util, json, re, subprocess
from pathlib import Path

from jsonschema import Draft202012Validator, validators
from jsonschema.exceptions import ValidationError
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

import admission_ref as AR
import check_routes as CR
import common as CM
import owner_successor as OS
import patterns as PT
import representability as REP
import sender_ref as SR
import wirecodec as W

Refuse = W.Refuse
SNAP = "snapshot2:" + "a" * 64
PLAN = "plan2:" + "b" * 64
NL, CR_, LS, PS, NUL = chr(10), chr(13), chr(0x2028), chr(0x2029), chr(0)
CORPUS = ["", "a", "a/b", "a/..", ".." + NL, "a/.." + NL, "a/." + NL, "a" + NL + "/../b", "a" + CR_ + "/../b", "a" + LS + "/..", "a" + PS + "/./b",
          "a" + NL + "b", "a" + CR_ + "b", "C:x", "a//b", "a/", "/a", "./a", "0" * 64, "0" * 64 + NL, "0" * 64 + CR_, "sha256:" + "0" * 64,
          "sha256:" + "0" * 64 + NL, "snapshot2:" + "a" * 64, "plan2:" + "b" * 64 + NL, "DISCLOSURE-ONLY", "DISCLOSURE-ONLY" + NL,
          "ENFORCED-PLATFORM:linux-5.x", "ENFORCED-PLATFORM:" + "a" * 65, "a" + chr(0x7f), "a" + chr(0x85), "a" + chr(0x9f), chr(0xfeff), chr(0xa0),
          "exec1_" + "0" * 32, "exec1_" + "0" * 32 + NL, "rust-file:sha256:" + "0" * 64, ".opensip/prepared/v3/0-" + "0" * 64 + ".blob",
          ".opensip/prepared/v3/01-" + "0" * 64 + ".blob", ".opensip/prepared/v3/0-" + "0" * 64 + ".blob" + NL, "a.b:c", "a..b", "x" * 256,
          "x" * 255 + "/y", "a" + NUL + "b", "a\\b", "e" + chr(0x301), "12", "a_1", "A-z", "prj1-" + "0" * 64]
PATH_CORPUS = ["a", "a/b", "a/../b", "../b", "a/..", "..", ".", "./a", "a/.", "/a", "a//b", "a/", "x" + NL + "/../y", "x" + NL + "/..",
               "a" + LS + "/../b", "a" + PS + "/./b", "a" + CR_ + "/./b", "a/.." + NL, ".." + NL, "a/." + NL, NL + "/..", "a" + NL + "b",
               "C:x", "c:/x", "x" * 256, "a/" + "b" * 255, "a" + NUL + "b", "a\\b", "e" + chr(0x301), ".." + NL + "/b",
               "a" + NL + NL + "/../../etc/passwd", " /../b", "a/...", "...", "a/.b", ".a/b"]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


C, raw_hex = AR.C, AR.raw_hex


def find(o, key):
    if isinstance(o, dict):
        if key in o:
            return o
        for v in o.values():
            r = find(v, key)
            if r is not None:
                return r
    elif isinstance(o, list):
        for v in o:
            r = find(v, key)
            if r is not None:
                return r
    return None


def has_bytes(v):
    if isinstance(v, bytes):
        return True
    if isinstance(v, dict):
        return any(has_bytes(x) for x in v.values())
    if isinstance(v, list):
        return any(has_bytes(x) for x in v)
    return False


def pointer_values(obj, pointer):
    cur = [obj]
    for part in [p for p in pointer.split("/") if p]:
        nxt = []
        for c in cur:
            if part == "*" and isinstance(c, list):
                nxt.extend(c)
            elif isinstance(c, dict) and part in c:
                nxt.append(c[part])
        cur = nxt
    return cur


def ecma_validator_class(flags):
    def pattern(validator, patrn, instance, schema):
        if validator.is_type(instance, "string") and not W.ecma_test(patrn, flags, instance):
            yield ValidationError(f"{instance!r} does not match ECMA-262 /{patrn}/{flags}")
    return validators.extend(Draft202012Validator, {"pattern": pattern})


def all_patterns(o, acc):
    if isinstance(o, dict):
        for k, v in o.items():
            if k == "pattern" and isinstance(v, str):
                acc.add(v)
            all_patterns(v, acc)
    elif isinstance(o, list):
        for v in o:
            all_patterns(v, acc)
    return acc


class Reference:
    def __init__(self, arch, subject, static):
        native = Path(arch) / "docs/coop/design-corrections/native"
        self.s = static
        self.osucc = static.osucc
        self.NE = load("ref_ne", native / "native_evidence_model.v2.py")
        self.ST = load("ref_st", native / "provider_startup_model.v1.py")
        self.WI = load("ref_wi", native / "provider_wire_model.v1.py")
        self.IM3 = load("ref_im3", Path(arch) / "docs/coop/design-corrections/foundation" / OS.MODEL_FILES["identityModel3"])
        succ = OS.load_models(arch, self.osucc, "succ_")
        self.NE_S, self.ST_S, self.WI_S, self.IM3_S = succ["NE"], succ["ST"], succ["WI"], succ["IM3"]
        self.wire = static.wire
        self.p3 = static.p3
        self.flags = self.wire["privateRepresentation"]["patternDialect"]["flags"]
        self.V = ecma_validator_class(self.flags)
        self.reg = Registry().with_resources([(d["$id"], Resource(contents=d, specification=DRAFT202012)) for d in static.effective.values()])
        self.K = W.Carriers(self.wire, self.extern)
        cases = json.loads(static.raw["nativeCases"])
        self.fx = cases["fixtures"]
        self.cov_fx = find(cases, "scopeDescriptor")
        self.tokens = list(self.NE.IDENTITY_TOKENS)
        self.results = []
        self.node_ok = None

    def extern(self, gen, v, where):
        ref = None
        for sid, ns in CM.EXTERN_NS.items():
            if gen.startswith(ns) and sid in self.s.docs:
                name = gen[len(ns):]
                ref = sid + ("#" if name == "Root" else "#/$defs/" + name)
        if ref is None:
            raise Refuse("EXTERN_UNKNOWN", gen)
        if has_bytes(v):
            raise Refuse("EXTERN_BYTES", where)
        errs = list(self.V({"$ref": ref}, registry=self.reg).iter_errors(v))
        if errs:
            raise Refuse("EXTERN_SCHEMA", where + ":" + errs[0].message[:100])
        for rid in ("CANONICAL-PATH-ADMISSION", "TS2-LOGICAL-PATH-ADMISSION"):
            for m in AR.params(self.wire, rid).get("externMembers", []):
                if m["generatedType"] == gen:
                    for value in pointer_values(v, m["pointer"]):
                        AR.path_admission(self.wire, rid, value)
        if gen == "Native2DependencySourceManifestV3":
            for e in v["entries"]:
                W.lexical(self.wire["privateRepresentation"]["lexicalRules"], "package-key", e["packageKey"], self.flags, where + ".entries.packageKey")

    def add(self, id_, ok, detail=""):
        self.results.append({"id": id_, "ok": bool(ok), "detail": detail if isinstance(detail, str) else json.dumps(detail, default=str, ensure_ascii=False)[:900]})

    def expect(self, id_, fn, code=None):
        got = self.code_of(fn)
        self.add(id_, got == code, {"expected": code, "got": got})
        return got == code

    def code_of(self, fn):
        try:
            fn()
            return None
        except Refuse as exc:
            return exc.code
        except Exception as exc:  # noqa: BLE001
            return "EXCEPTION:" + type(exc).__name__ + ":" + str(exc)[:160]

    def limits(self, protocol, override=None):
        name = "ProtocolLimitsV3" if protocol == "rust-semantic" else "TypeScriptProtocolLimitsV1"
        return dict({k: x["const"] for k, x in self.s.hs["$defs"][name]["properties"].items()}, **(override or {}))

    def lexical_ok(self, rule, value):
        try:
            W.lexical(self.wire["privateRepresentation"]["lexicalRules"], rule, value, self.flags)
            return True
        except Refuse:
            return False

    # ------------------------------------------------------------------ owner-run cases
    def depsrc_case(self, c):
        row = copy.deepcopy(self.fx["vendoredRow"])
        for f in ("name", "version", "sourceId"):
            if f in c:
                row[f] = c[f]
        files = c.get("files", ["Cargo.toml", "src/lib.rs"])
        row["files"] = {p: {"sha256": "1" * 64, "byteLength": 3} for p in files}
        row["cargoChecksumJson"]["files"] = {p: "1" * 64 for p in files}
        checksum = c.get("lockChecksum", row["cargoChecksumJson"]["package"])
        lock = 'version = 4\n\n[[package]]\nname = "%s"\nversion = "%s"\nsource = "%s"\nchecksum = "%s"\n' % (row["name"], row["version"], row["sourceId"], checksum)
        return lock, [row], [f'{row["name"]} {row["version"]} {row["sourceId"]}']

    def prepared_case(self, c):
        prep = copy.deepcopy(self.fx[c["fixture"]])
        base = prep["rows"][0]
        rows = []
        for i in range(c["rows"]):
            r = copy.deepcopy(base)
            if r.get("site") is not None:
                r["site"]["startByte"], r["site"]["endByte"] = i, i + 1
            else:
                r["ownerKey"] = f'{base["ownerKey"]}#{i}'
            rows.append(r)
        for idx, n in c.get("blobByteLengths", []):
            rows[idx]["blob"]["byteLength"] = n
        for idx in (range(len(rows)) if c.get("stale") == "all" else c.get("stale", [])):
            rows[idx]["inputBinding"]["toolchainDigest"] = "9" * 64
        for idx in c.get("nonInert", []):
            rows[idx] = copy.deepcopy(self.fx["prepDylib"]["rows"][0])
        for idx in c.get("badSite", []):
            rows[idx]["site"]["path"] = "x" + NL + "/../y.rs"
        for idx in c.get("failed", []):
            rows[idx]["status"], rows[idx]["failureDetail"] = "failed", "build script failed"
        prep["rows"] = rows
        return prep, c.get("explicit", True)

    def prepared_path_case(self, c):
        prep = copy.deepcopy(self.fx[c.get("fixture", "prepGenerated")])
        if "generatedLogicalPath" in c:
            for r in prep["rows"]:
                if r["kind"] == "generated-file":
                    r["generated"]["logicalPath"] = c["generatedLogicalPath"]
        if "sitePath" in c:
            next(r for r in prep["rows"] if r.get("site"))["site"]["path"] = c["sitePath"]
        if c.get("addNonInert"):
            prep["rows"].append(copy.deepcopy(self.fx["prepDylib"]["rows"][0]))
        return prep, c.get("explicit", True)

    # ------------------------------------------------------------------ vectors
    def expand(self, x):
        if isinstance(x, dict):
            if "$bytesHex" in x:
                return bytes.fromhex(x["$bytesHex"])
            if "$repeat" in x:
                item = self.expand(x["$repeat"]["item"])
                return [item] * x["$repeat"]["n"]
            if "$concat" in x:
                return [e for part in x["$concat"] for e in self.expand(part)]
            if "$scopeDescriptor" in x:
                d = dict(self.cov_fx["scopeDescriptor"], **x["$scopeDescriptor"])
                return self.NE.subject_scope_descriptor(d["snapshotId"], d["relation"], d["resolution"], d["sourceUniverse"],
                                                        d["targetUniverse"], d["enumeratorClosure"], d["subjects"])
            if "$ownerCommit" in x:
                o = x["$ownerCommit"]
                if o["doc"] == "rust2":
                    domain = re.search(r"UTF8\(([^)]+)\)", self.s.r2["commitments"][o["recipe"]]).group(1)
                else:
                    domain = self.s.w2["commitments"]["domains"][o["recipe"]]
                return {"$domain": domain, "value": o["value"]}
            if "$inheritedTsPerStage" in x:
                return C("opensip.coverage.subject-scope.v1", [{"path": s} for s in self.cov_fx["scopeDescriptor"]["subjects"]])
            return {k: self.expand(v) for k, v in x.items()}
        if isinstance(x, list):
            return [self.expand(v) for v in x]
        return x

    def path_site_frame(self, site, value):
        K = self.K
        if site in ("generated-logicalPath", "expansion-site-path"):
            prep, _ = self.prepared_path_case({"generatedLogicalPath": value} if site == "generated-logicalPath" else {"sitePath": value})
            entries = AR.prepared_entries(prep["rows"])
            return K.frame_payload("rust-semantic", "PreparedOutputManifest", {"planId": PLAN, "manifestSha256": raw_hex(entries), "entries": entries})
        if site == "crateRootPaths":
            ou = copy.deepcopy(self.fx["startupRustOpenUniverse"])
            find(ou, "crateRootPaths")["crateRootPaths"] = [value]
            return K.frame_payload("rust-semantic", "OpenUniverse", ou)
        if site in ("jsRootFiles", "programRootFiles"):
            ou = copy.deepcopy(self.fx["startupTsOpenUniverse"])
            find(ou, site)[site] = [value]
            return K.frame_payload("typescript-semantic", "OpenUniverse", ou)
        if site == "dependency-manifest-path":
            entries = [{"packageKey": "serde 1.0.200 registry+x", "path": value, "byteLength": 1, "contentSha256": "1" * 64}]
            return K.frame_payload("rust-semantic", "DependencySourceManifest", {"dependencySourceSetId": "sha256:" + "1" * 64, "manifestSha256": raw_hex(entries), "entries": entries})
        if site == "occupancy-LogicalPath":
            # the scoped consumer (owner successor scope provider-wire-model): the wire model's own validator and registry
            try:
                self.WI_S.C.validate({"$ref": CM.OC + "#/$defs/LogicalPath"}, value, registry=self.WI_S.REGISTRY)
            except ValidationError:
                raise Refuse("EXTERN_SCHEMA", site)
            return None
        raise Refuse("UNKNOWN_PATH_SITE", site)

    def owner_case(self, c):
        NE_S, fx = self.NE_S, self.fx
        call, value = c["call"], c["value"]
        try:
            if call == "validate":
                if c["def"] == "DependencyFileManifestV1":
                    payload = [{"path": value, "contentSha256": "1" * 64, "byteLength": 1}]
                else:
                    gen = next(r for r in fx["prepGenerated"]["rows"] if r["kind"] == "generated-file")["generated"]
                    payload = dict(copy.deepcopy(gen), logicalPath=value)
                NE_S.validate_native(c["def"], payload)
            elif call == "logical-re":
                if not NE_S._LOGICAL_RE.match(value):
                    raise Refuse("OWNER_LOGICAL_RE")
            elif call == "startup-open-universe":
                ou = copy.deepcopy(fx["startupRustOpenUniverse"])
                find(ou, "crateRootPaths")["crateRootPaths"] = [value]
                self.ST_S.C.validate({"$ref": self.s.st["$id"] + "#/$defs/OpenUniverseV3"}, ou, registry=self.ST_S.REGISTRY)
            elif call == "dependency-set":
                lock, provided, activated = self.depsrc_case({"files": ["Cargo.toml", value]})
                out = NE_S.dependency_source_set_admit(lock, provided, activated)
                if not (out["admitted"] and out["identity"]):
                    raise Refuse("OWNER_NOT_ADMITTED")
            elif call == "prepared-set":
                prep, explicit = self.prepared_path_case({"generatedLogicalPath": value})
                out = NE_S.prepared_output_set_admit(prep, fx["ctx"], explicit)
                if out["outcome"] != "admitted":
                    raise Refuse("OWNER_" + out["outcome"].upper())
            else:
                raise Refuse("UNKNOWN_OWNER_CALL", call)
        except Refuse:
            raise
        except Exception as exc:  # noqa: BLE001
            raise Refuse("OWNER_SCHEMA:" + type(exc).__name__)

    def relation_case(self, mod, c):
        """Retained fact admission's relation payload call (identity-model.v3 registered_payload calls
        validate_registered_record) on the relation-payload document; `mod` is the scoped successor or the pinned model."""
        if mod is self.IM3_S:
            OS.require_installed(mod)
        payload = dict(c["payload"], **{c["property"]: c["value"]})
        try:
            mod.validate_registered_record(OS.RELATION_DOC_PATH, "#/$defs/" + c["def"], payload)
        except mod.C.AdmissionError as exc:
            raise Refuse(str(exc).split(":")[0])

    def send_case(self, inp):
        doc = self.wire
        p = inp["send"]
        desc = p["plan"]
        rust = desc["protocol"] == "rust-semantic"
        limits = self.limits(desc["protocol"], desc.get("limitsOverride"))
        req = REP.build_plan(desc, self.fx, AR.prepared_entries)
        plan = (REP.plan_rust3_request if rust else REP.plan_ts2_request)(doc, limits, req)
        if plan["refusal"]:
            raise Refuse("PLAN_REFUSED")
        frames = self.mutate_transcript(SR.realize(req, desc["protocol"], limits, materialize=bool(desc.get("contentFromZeroBytes"))), req, plan, p["transcript"])
        consume_limits = dict(limits, **p.get("consumeLimitsOverride", {}))
        res = SR.consume(plan, desc["protocol"], AR.params(doc, "REQUEST-WIRE-ACCOUNTING"), consume_limits, frames)
        reserve = plan["cancelReserve"]["payloadBytes"] if plan["cancelReserve"] else 0
        if inp.get("expectMatchesPlan") and (res["framesSent"] != plan["frames"] - (1 if plan["cancelReserve"] else 0) or res["payloadBytesSent"] != plan["payloadBytes"] - reserve or not res["complete"]):
            raise Refuse("SENDER_RESULT_MISMATCH:plan", json.dumps(res))
        if "expectPayloadBytesSent" in inp and res["payloadBytesSent"] != inp["expectPayloadBytesSent"]:
            raise Refuse("SENDER_RESULT_MISMATCH:payloadBytesSent", str(res["payloadBytesSent"]))
        if "expectContentVerifiedEntries" in inp and res["chunkContentVerifiedEntries"] != inp["expectContentVerifiedEntries"]:
            raise Refuse("SENDER_RESULT_MISMATCH:chunkContentVerifiedEntries", str(res["chunkContentVerifiedEntries"]))
        if "expectComplete" in inp and res["complete"] != inp["expectComplete"]:
            raise Refuse("SENDER_RESULT_MISMATCH:complete")
        return res

    @staticmethod
    def renumber(frames):
        for i, f in enumerate(frames):
            f["sequence"] = i
        return frames

    def mutate_transcript(self, frames, req, plan, t):
        kind = t["kind"]
        null_echo = {"executionId": None, "analysisOrdinal": None, "reason": plan["cancelEcho"]["reason"]}
        echo = lambda k: SR.expected_cancel(plan, k) or dict(null_echo)
        if kind == "canonical":
            return frames
        if kind == "cancel-at-end":
            return frames + [SR.cancel_frame(len(frames), echo(len(frames)))]
        if kind == "cancel-after":
            return frames[:t["frames"]] + [SR.cancel_frame(t["frames"], echo(t["frames"]))]
        if kind == "cancel-at":
            k = len(frames) if t["frames"] == -1 else t["frames"]
            payload = dict(echo(k))
            for name, value in t.get("override", {}).items():
                if value == "$planned":
                    value = plan["cancelEcho"][name]
                elif value == "$wrong-same-length":
                    planned = plan["cancelEcho"][name]
                    value = planned[:-1] + ("0" if planned[-1] != "0" else "1")
                payload[name] = value
            return frames[:k] + [SR.cancel_frame(k, payload)]
        if kind == "substitute":
            i = next(i for i, f in enumerate(frames) if f["frameType"] == t["frameType"])
            payload = dict(frames[i]["payload"])
            value = t["value"]
            if value == "$wrong-same-length":
                value = payload[t["field"]][:-1] + ("0" if payload[t["field"]][-1] != "0" else "1")
            payload[t["field"]] = value
            out = frames[:i] + [dict(frames[i], payload=payload)]
            if t.get("cancelAfter") == "planned":
                return out + [SR.cancel_frame(i + 1, echo(i + 1))]
            if t.get("cancelAfter") == "sent":
                return out + [SR.cancel_frame(i + 1, dict(echo(i + 1), **{t["field"]: value}))]
            return out + frames[i + 1:]
        if kind == "materialized-flip":
            i = next(i for i, f in enumerate(frames) if f["frameType"] == t["frameType"])
            flipped = bytearray(frames[i]["payload"]["bytes"])
            flipped[0] ^= 1
            frames[i] = dict(frames[i], payload=dict(frames[i]["payload"], bytes=bytes(flipped)))
            return frames
        if kind == "truncate":
            return frames[:t["frames"]]
        if kind == "extra-frame":
            return frames + [dict(frames[-1], sequence=len(frames))]
        if kind == "second-cancel":
            return frames[:3] + [SR.cancel_frame(3, echo(3)), SR.cancel_frame(4, echo(3))]
        if kind == "cancel-over-reserve":
            return frames[:3] + [SR.cancel_frame(3, dict(echo(3), executionId=req["openUniverse"]["executionId"] + "x"))]
        if kind == "payload-bytes":
            frames[1] = dict(frames[1], payload=dict(frames[1]["payload"], executionId=frames[1]["payload"]["executionId"] + "x"))
            return frames
        if kind == "payload-bytes-chunk":
            i = next(i for i, f in enumerate(frames) if f["frameType"] == "SnapshotFileChunk")
            frames[i] = dict(frames[i], payload=dict(frames[i]["payload"], snapshotId=frames[i]["payload"]["snapshotId"] + "0"))
            return frames
        if kind == "seal-count":
            i = next(i for i, f in enumerate(frames) if f["frameType"] == "SnapshotSeal")
            frames[i] = dict(frames[i], payload=dict(frames[i]["payload"], totalChunkCount=frames[i]["payload"]["totalChunkCount"] + 1))
            return frames
        if kind == "reorder":
            frames[0], frames[1] = frames[1], frames[0]
            return self.renumber(frames)
        if kind == "sequence-boolean-zero":
            frames[0] = dict(frames[0], sequence=False)
            return frames
        if kind == "sequence-gap":
            frames[2] = dict(frames[2], sequence=frames[2]["sequence"] + 1)
            return frames
        if kind == "alternate-chunking":
            chunk_types = ("SnapshotFileChunk", "DependencySourceChunk", "PreparedOutputChunk")
            idx = next(i for i, f in enumerate(frames) if f["frameType"] in chunk_types and f["payload"]["bytes"].n >= 2
                       and not (i + 1 < len(frames) and frames[i + 1]["frameType"] == f["frameType"] and frames[i + 1]["payload"]["chunkIndex"] > 0))
            f = frames[idx]
            n = f["payload"]["bytes"].n
            a = dict(f, payload=dict(f["payload"], bytes=W.ByteLen(n // 2)))
            b = dict(f, payload=dict(f["payload"], chunkIndex=f["payload"]["chunkIndex"] + 1, byteOffset=f["payload"]["byteOffset"] + n // 2, bytes=W.ByteLen(n - n // 2)))
            return self.renumber(frames[:idx] + [a, b] + frames[idx + 1:])
        if kind == "alternate-split":
            idxs = [i for i, f in enumerate(frames) if f["frameType"] == t["frameType"]]
            base = {k: v for k, v in frames[idxs[0]]["payload"].items() if k not in ("chunkIndex", "byteOffset", "bytes")}
            new, off = [], 0
            for ci, n in enumerate(t["sizes"]):
                new.append({"frameType": t["frameType"], "sequence": 0, "payload": dict(base, chunkIndex=ci, byteOffset=off, bytes=W.ByteLen(n))})
                off += n
            return self.renumber(frames[:idxs[0]] + new + frames[idxs[-1] + 1:])
        raise Refuse("UNKNOWN_TRANSCRIPT_KIND", kind)

    def run_vector(self, rid, inp):
        doc, NE = self.wire, self.NE
        if rid in ("CANONICAL-PATH-ADMISSION", "TS2-LOGICAL-PATH-ADMISSION"):
            return AR.path_admission(doc, rid, inp["path"])
        if rid == "PACKAGE-KEY-JOIN":
            return AR.package_key_join(doc, inp["packages"], inp["key"])
        if rid == "DEPSRC-SET-KEY-CONSTRAINTS":
            return AR.depsrc_set_key_constraints(doc, inp["packages"])
        if rid == "DEPSRC-WIRE-REPRESENTABILITY":
            lock, provided, activated = self.depsrc_case(inp["depsrc"])
            try:
                out = REP.dependency_source_set_admit_successor(self.NE_S, doc, lock, provided, activated)
            except Refuse:
                raise
            except Exception as exc:  # noqa: BLE001
                raise Refuse("OWNER_EXCEPTION:" + type(exc).__name__)
            ref = out["successorRefusal"]
            if ref:
                raise Refuse("ROUTE:" + ref["key"] + ":" + ref["faults"][0]["kind"])
            if not out["admitted"]:
                raise Refuse("OWNER:" + "/".join(sorted({r["rule"] for r in out["refusals"]})))
            return None
        if rid in ("PREPARED-V3-WIRE-LIMIT", "PREPARED-V3-PATH-REPRESENTABILITY"):
            c = inp["prepared"]
            prep, explicit = self.prepared_case(c) if "rows" in c else self.prepared_path_case(c)
            try:
                out = REP.prepared_output_set_admit_successor(self.NE_S, doc, prep, self.fx["ctx"], explicit)
            except Refuse:
                raise
            except Exception as exc:  # noqa: BLE001
                raise Refuse("OWNER_EXCEPTION:" + type(exc).__name__)
            ref = out["successorRefusal"]
            if ref:
                raise Refuse("ROUTE:" + ref["key"] + ":" + ref["faults"][0]["kind"])
            if out["outcome"] == "rejected":
                raise Refuse("OWNER:rejected:" + out["d9"]["detail"])
            for key, field in (("expectOutcome", "outcome"), ("expectOwnerOutcome", "ownerOutcome")):
                if key in inp and out.get(field) != inp[key]:
                    raise Refuse("OUTCOME_MISMATCH:%s:%s" % (field, out.get(field)))
            if "expectDisclosure" in inp and [f["kind"] for f in out.get("wireLimitDisclosure") or []] != inp["expectDisclosure"]:
                raise Refuse("DISCLOSURE_MISMATCH")
            if "expectUsableRows" in inp and len(out.get("usableRows", [])) != inp["expectUsableRows"]:
                raise Refuse("USABLE_ROWS_MISMATCH:%d" % len(out.get("usableRows", [])))
            if "expectStaleRows" in inp and len(out.get("staleRows", [])) != inp["expectStaleRows"]:
                raise Refuse("STALE_ROWS_MISMATCH:%d" % len(out.get("staleRows", [])))
            if "expectReadAuthorityDisclosure" in inp and [f["kind"] for f in out.get("readAuthorityDisclosure") or []] != inp["expectReadAuthorityDisclosure"]:
                raise Refuse("READ_AUTHORITY_DISCLOSURE_MISMATCH")
            if out["outcome"] == "fallback-non-prepared" and out.get("usableRows"):
                raise Refuse("PARTIAL_STALE_SET_SELECTED")
            basis = out.get("wireLimitBasis") or {}
            for k, want in inp.get("expectBasis", {}).items():
                if basis.get(k) != want:
                    raise Refuse("BASIS_MISMATCH:%s:%s" % (k, basis.get(k)))
            # review-04 RF-1: every non-rejected outcome ran the path law over every row before the owner and the bound over
            # every carried row; the owner's usable rows are a subset of the carried rows.
            if not out.get("ownerRan") or basis.get("carriedRows") != len(prep["rows"]) or basis.get("ownerUsableRows", -1) > basis["carriedRows"]:
                raise Refuse("BASIS_NOT_CARRIED_ROWS")
            if out.get("wireLimitDisclosure") and (out.get("usableRows") or out["outcome"] != "fallback-non-prepared" or not out.get("disclosure")):
                raise Refuse("WIRE_LIMIT_FALLBACK_NOT_WHOLE_SET")
            if out["outcome"] == "fallback-non-prepared" and not out.get("disclosure"):
                raise Refuse("FALLBACK_NOT_DISCLOSED")
            return None
        if rid == "REQUEST-WIRE-ACCOUNTING":
            p = inp["plan"]
            res = REP.plan(doc, self.limits(p["protocol"], p.get("limitsOverride")), p, self.fx, AR.prepared_entries)
            if "expectFrames" in p and res["frames"] != p["expectFrames"]:
                raise Refuse("FRAMES_MISMATCH:%d" % res["frames"])
            if "expectPayloadBytes" in p and res["payloadBytes"] != p["expectPayloadBytes"]:
                raise Refuse("PAYLOAD_BYTES_MISMATCH:%d" % res["payloadBytes"])
            for ft, n in p.get("expectLargestFrame", {}).items():
                if res["largestFrame"].get(ft) != n:
                    raise Refuse("LARGEST_FRAME_MISMATCH:%s:%s" % (ft, res["largestFrame"].get(ft)))
            for ft, want in p.get("expectSeals", {}).items():
                got = res["seals"].get(ft, {})
                if any(got.get(k) != x for k, x in want.items()):
                    raise Refuse("SEAL_MISMATCH:" + ft)
            if res["refusal"]:
                raise Refuse("ROUTE:" + res["refusal"]["key"] + ":" + res["faults"][0]["kind"])
            return None
        if rid == "HOST-SEND-SCHEDULE":
            self.send_case(inp)
            return None
        if rid == "PATH-SITE-SEGMENT-LAW":
            try:
                return self.path_site_frame(inp["site"], inp["value"])
            except Refuse as exc:
                raise Refuse(exc.code.split(":")[0])
        if rid == "OWNER-PATTERN-EVALUATION":
            return self.owner_case(inp["owner"])
        if rid == "DEPSRC-CUSTODY":
            return AR.depsrc_custody(doc, inp["packages"], inp["manifest"])
        if rid == "PREPARED-V3-ENTRY":
            prep = copy.deepcopy(self.fx[inp["setFixture"]])
            mut = inp.get("mutate", {})
            if "generatedBlobSha256" in mut:
                next(r for r in prep["rows"] if r["kind"] == "generated-file")["generated"]["blob"]["sha256"] = mut["generatedBlobSha256"]
            entries = AR.prepared_entries(prep["rows"])
            if "entry" in mut:
                entries[mut["entry"]]["contentSha256"] = mut["contentSha256"]
            self.K.frame_payload("rust-semantic", "PreparedOutputManifest", {"planId": PLAN, "manifestSha256": raw_hex(entries), "entries": entries})
            return AR.prepared_entry_join(entries)
        if rid == "RUST3-PROVIDER-FAULT":
            self.K.frame_payload("rust-semantic", "ProviderFault", inp["fault"])
            return AR.provider_fault(doc, self.p3, self.tokens, inp["events"], inp["fault"])
        if rid == "P3-OVERLAY":
            res = AR.overlay_run(doc, self.p3, self.tokens, inp["events"], inp["stageCount"])
            if res["finalPhase"] == "FAULT":
                raise Refuse(res["trace"][-1])
            if inp.get("tail") not in res["trace"]:
                raise Refuse("OVERLAY_TAIL_MISSING")
            return None
        if rid == "COMMIT-MAP":
            want = inp["commitment"]
            stages = inp["stages"]
            value = stages[-1] if want["value"] == "stage" else [e for s in stages for e in s]
            if AR.commit_value(doc, inp["field"], stages) != C(want["$domain"], value):
                raise Refuse("COMMIT_MISMATCH")
            return None
        if rid in ("ANCHOR-WIRE-SPAN", "ANCHOR-FACT-REF-REFUSED"):
            return AR.anchor_admission(doc, inp["language"], inp["anchors"], inp["manifest"], SNAP, W.cve1)
        if rid in ("TS2-MANIFEST-DIGEST", "RAW-MANIFEST-DIGEST"):
            return AR.manifest_digest(inp["manifest"])
        if rid == "ACCEPTED-EQUALS-SEAL":
            return AR.accepted_equals_seal(inp["seal"], inp["accepted"])
        if rid == "CHUNK-CUSTODY":
            return AR.chunk_custody(inp["entry"], inp["chunks"])
        if rid == "SEAL-AGGREGATES":
            return AR.seal_aggregates(inp["entries"], inp["chunkCount"], inp["seal"], inp["total"])
        if rid == "CANCEL-NULLABILITY":
            return AR.cancel_nullability(inp["sent"], inp["cancel"])
        if rid == "CANCELLED-ECHO":
            return AR.cancelled_echo(inp["cancel"], inp["cancelled"])
        if rid == "RUST3-CANCEL-TYPES":
            self.K.frame_payload("rust-semantic", "Cancelled", inp["cancelled"])
            return AR.cancelled_echo(inp["cancel"], inp["cancelled"], inp["hostSendPhase"])
        if rid == "RUST3-BUDGET-EXHAUSTED":
            return AR.budget_observed(doc, inp["payload"], inp["planBudget"])
        if rid == "OCCUPANCY-JOIN":
            return AR.occupancy_join(inp["batch"])
        if rid == "PER-KEY-SCOPE2":
            desc = inp["descriptor"]
            commitment = inp["commitment"] if "commitment" in inp else NE.subject_scope_commitment(inp["commitmentOf"])["subjectScopeCommitment"]
            return AR.per_key_scope2(doc, NE.C.identity, desc, commitment)
        if rid == "PREPARED-V3-READ-AUTHORITY":
            prep, _ = self.prepared_case(inp["prepared"])
            return AR.prepared_read_authority(AR.prepared_entries(prep["rows"]), inp["ordinal"])
        if rid == "RELATION-PAYLOAD-PATH-LAW":
            return self.relation_case(self.IM3_S, inp["relation"])
        raise Refuse("NO_VECTOR_HANDLER", rid)

    def vectors(self):
        for rid, vecs in self.s.vectors["vectors"].items():
            oks = []
            for vec in vecs:
                inp = self.expand(vec["input"])
                code = vec["expect"] if vec["kind"] == "refuse" else None
                oks.append(self.expect(f"vector:{rid}:{vec['id']}", lambda: self.run_vector(rid, inp), code))
            self.add("vectors:" + rid, all(oks) and len(oks) >= 2, f"{sum(oks)}/{len(oks)}")

    def routes(self):
        CR.Routes(self).run()

    # ------------------------------------------------------------------ owner runs (retained)
    def scope2(self):
        NE, ST, K = self.NE, self.ST, self.K
        desc, payload = self.cov_fx["scopeDescriptor"], self.cov_fx["coveragePayload"]
        commit = NE.subject_scope_commitment(desc)
        src, tgt = "sha256:" + desc["sourceUniverse"], "sha256:" + desc["targetUniverse"]
        base = {"relation": desc["relation"], "resolution": desc["resolution"], "sourceUniverseId": src, "targetUniverseId": tgt,
                "subjectScopeCommitment": commit["subjectScopeCommitment"]}
        ts_key = dict(base, producer="typescript-semantic", producerVersion="typescript-provider 1.0.0", schemaVersion=1)
        rs_key = dict(base, producer="rust-semantic", producerVersion="rust-provider 1.0.0", schemaVersion=1)

        def ts():
            K.check({"t": "ref", "ref": "Ts2CoverageKeyV1"}, ts_key, "key")
            frame = {"analysisOrdinal": 0, "stageId": "s1", "entries": [payload], "coverageCommitment": C("opensip.ts-provider.stage-coverage.v1", [payload])}
            K.frame_payload("typescript-semantic", "Coverage", frame)
            ST.admit_coverage_frame("typescript-semantic", frame, "s1", [ts_key])
            if NE.admit_coverage_result_v3(payload, desc, [])["result"] != "ADMIT":
                raise Refuse("NOT_ADMITTED")
            AR.per_key_scope2(self.wire, NE.C.identity, desc, ts_key["subjectScopeCommitment"])
        self.expect("scope2-ts2-admits", ts)

        def rs():
            K.check({"t": "ref", "ref": "Rust3CoverageKeyV2"}, rs_key, "key")
            frame = {"analysisOrdinal": 0, "stageId": "s1", "entries": [payload], "coverageCommitment": C("opensip.rust-provider.stage-coverage.v2", [payload])}
            K.frame_payload("rust-semantic", "CoverageV3", frame)
            ST.admit_coverage_frame("rust-semantic", frame, "s1", [rs_key])
            if NE.admit_coverage_result_v3(payload, desc, [])["result"] != "ADMIT":
                raise Refuse("NOT_ADMITTED")
        self.expect("scope2-rust3-admits", rs)
        refused = []
        for value in (C("opensip.coverage.subject-scope.v1", [{"path": s} for s in desc["subjects"]]), C("opensip.rust-provider.subject-scope.v2", desc["subjects"])):
            bad = copy.deepcopy(payload)
            bad["key"]["subjectScopeCommitment"] = value
            bad["entry"]["examinedUniverse"]["subjectScopeCommitment"] = value
            out = NE.admit_coverage_result_v3(bad, desc, [])
            refused.append(out["result"] == "REFUSE" and "native.subject-scope-commitment-mismatch" in out["refusals"])
        self.add("scope2-per-stage-value-refused", all(refused), refused)
        other = [NE.subject_scope_descriptor(desc["snapshotId"], desc["relation"], r, desc["sourceUniverse"], t, desc["enumeratorClosure"], desc["subjects"])
                 for r, t in (("syntactic-name-match", desc["targetUniverse"]), (desc["resolution"], "f" * 64))]
        self.add("scope2-keys-differ", len({NE.subject_scope_commitment(d)["subjectScopeCommitment"] for d in [desc] + other}) == 3, "")

    def anchors(self):
        line = self.s.lines("identityModel3")[1891]
        expr = re.search(r"if not (.+?):raise", line).group(1)
        permits = eval(expr, {}, {"a": 4, "b": 4, "raw": b"0123456789", "len": len})  # exact pinned source expression
        self.add("fact2-anchor-range-permits-empty", permits and not eval(expr, {}, {"a": 5, "b": 4, "raw": b"0123456789", "len": len}), expr)
        span = {"kind": "source-span", "snapshotId": SNAP, "path": "b", "contentSha256": "1" * 64, "startByte": 0, "endByte": 1, "factId": None}
        a1, a2 = dict(span, contentSha256="f" * 64), dict(span, path="aa", contentSha256="0" * 64)
        cb, cv = [x["path"] for x in sorted([a1, a2], key=W.encode)], [x["path"] for x in sorted([a1, a2], key=W.cve1)]
        self.add("anchor-order-languages-differ", cb != cv, {"ts2-cbor": cb, "rust3-cve1": cv})
        p1, p2 = dict(span), dict(span, path="aa")
        self.add("anchor-order-path-only-same", [x["path"] for x in sorted([p1, p2], key=W.encode)] == [x["path"] for x in sorted([p1, p2], key=W.cve1)], "")
        self.expect("anchor-fact-ref-refused", lambda: AR.anchor_admission(self.wire, "rust-semantic", [{"kind": "fact-ref", "snapshotId": None, "path": None, "contentSha256": None, "startByte": None, "endByte": None, "factId": "x"}], {}, SNAP, W.cve1), "ANCHOR_FACT_REF_UNDER_FACT2")
        self.expect("anchor-empty-interval-refused-on-wire", lambda: AR.anchor_admission(self.wire, "typescript-semantic", [dict(span, endByte=0)], {"b": {"kind": "file", "byteLength": 1, "contentSha256": "1" * 64}}, SNAP, W.cve1), "ANCHOR_EMPTY_OR_OUT_OF_BOUNDS")

    def manifests(self):
        K = self.K
        entries = [{"path": "src/a.ts", "kind": "file", "byteLength": 3, "contentSha256": hashlib.sha256(b"abc").hexdigest(), "linkTarget": None},
                   {"path": "src/z.ts", "kind": "symlink", "byteLength": 0, "contentSha256": None, "linkTarget": "../outside/" + "x" * 5000}]
        man = {"snapshotId": SNAP, "manifestSha256": raw_hex(entries), "entries": entries}

        def raw():
            if hashlib.sha256(self.WI.wire_cbor(entries)).hexdigest() != man["manifestSha256"]:
                raise Refuse("ENCODER_DISAGREES_WITH_WIRE_MODEL")
            K.frame_payload("typescript-semantic", "SnapshotManifest", W.decode(W.encode(man), "ts2-cbor"))
            AR.manifest_digest(man)
        self.expect("ts2-manifest-digest-raw", raw)
        self.expect("ts2-manifest-domain-form-refused", lambda: K.frame_payload("typescript-semantic", "SnapshotManifest", dict(man, manifestSha256=C("opensip.ts-provider.snapshot-manifest.v1", entries))), "TEXT_PATTERN")
        big = dict(entries[0], path="a\n/../b")
        self.expect("wire-ts2-path-newline-dotdot-refused", lambda: K.check_record("Ts2SnapshotEntryV1", big), "PATH_LEXICAL")

    def depsrc(self):
        NE, K, fx = self.NE, self.K, self.fx
        row = fx["vendoredRow"]
        key = f'{row["name"]} {row["version"]} {row["sourceId"]}'
        adm = NE.dependency_source_set_admit(fx["lock"], [row], [key])
        pkgs = adm["descriptor"]["packages"]
        entries = [{"packageKey": key, "path": p, "byteLength": row["files"][p]["byteLength"], "contentSha256": row["files"][p]["sha256"]}
                   for p in sorted(row["files"], key=lambda x: x.encode())]
        man = {"dependencySourceSetId": adm["identity"], "manifestSha256": raw_hex(entries), "entries": entries}

        def join():
            if not adm["admitted"]:
                raise Refuse("FIXTURE_NOT_ADMITTED")
            AR.depsrc_custody(self.wire, pkgs, man, NE.file_manifest_identity)
            K.frame_payload("rust-semantic", "DependencySourceManifest", man)
            chunk = {"dependencySourceSetId": adm["identity"], "packageKey": key, "path": "Cargo.toml", "chunkIndex": 0, "byteOffset": 0, "bytes": b"a" * 100}
            K.frame_payload("rust-semantic", "DependencySourceChunk", W.decode(W.encode(chunk), "rust3-cbor"))
            seal = {"dependencySourceSetId": adm["identity"], "manifestSha256": man["manifestSha256"], "entryCount": 2, "totalBytes": 2100, "totalChunkCount": 3}
            K.frame_payload("rust-semantic", "DependencySourceSeal", seal)
            K.frame_payload("rust-semantic", "DependencySourceAccepted", seal)
        self.expect("depsrc-file-manifest-join", join)
        self.expect("depsrc-file-manifest-mismatch-refused", lambda: AR.depsrc_custody(self.wire, [dict(pkgs[0], fileManifestSha256="0" * 64)], man, NE.file_manifest_identity), "DEPSRC_FILE_MANIFEST")

        def non_self_ref():
            first = raw_hex(man["entries"])
            for trial in ("0" * 64, "f" * 64):
                if raw_hex(dict(man, manifestSha256=trial)["entries"]) != first:
                    raise Refuse("RECIPE_DEPENDS_ON_OWN_FIELD")
        self.expect("depsrc-digest-non-self-referential", non_self_ref)
        self.expect("depsrc-empty-set", lambda: AR.depsrc_custody(self.wire, [], {"dependencySourceSetId": adm["identity"], "manifestSha256": hashlib.sha256(b"\x80").hexdigest(), "entries": []}))
        self.expect("wire-depsrc-manifest-native-pattern-bypass-refused", lambda: K.frame_payload("rust-semantic", "DependencySourceManifest", dict(man, entries=[dict(entries[0], path="a\n//b")])), "PATH_LEXICAL")
        self.expect("wire-depsrc-chunk-empty-sourceid-key", lambda: K.frame_payload("rust-semantic", "DependencySourceChunk", {"dependencySourceSetId": adm["identity"], "packageKey": "a 1 ", "path": "src/lib.rs", "chunkIndex": 0, "byteOffset": 0, "bytes": b"x"}))

    def prepared(self):
        NE, K, fx = self.NE, self.K, self.fx
        prep = fx["prepGenerated"]
        admitted = NE.prepared_output_set_admit(prep, fx["ctx"], True)
        entries = AR.prepared_entries(prep["rows"])
        man = {"planId": PLAN, "manifestSha256": raw_hex(entries), "entries": entries}

        def build():
            if admitted["outcome"] != "admitted":
                raise Refuse("FIXTURE_SET_NOT_ADMITTED")
            AR.prepared_wire_limit(self.wire, prep, PLAN)
            K.frame_payload("rust-semantic", "PreparedOutputManifest", man)
            AR.prepared_entry_join(entries)
            seal = {"planId": PLAN, "manifestSha256": man["manifestSha256"], "entryCount": len(entries), "totalBlobBytes": sum(e["blobByteLength"] for e in entries), "totalChunkCount": 1}
            K.frame_payload("rust-semantic", "PreparedOutputSeal", seal)
            K.frame_payload("rust-semantic", "PreparedOutputAccepted", seal)
        self.expect("prepared-v3-entries-from-set", build)
        gen = [e["planRow"] for e in entries if e["kind"] == "generated-file"]
        self.add("prepared-v3-generated-blob-equality", bool(gen) and all(r["generated"]["blob"] == r["blob"] for r in gen), str(len(gen)))
        rebuilt = {"schemaVersion": 3, "preparation": prep["preparation"], "rows": [e["planRow"] for e in entries]}
        self.add("prepared-v3-set-identity-join", NE.prepared_output_set_identity(rebuilt) == NE.prepared_output_set_identity(prep), "")
        v2 = copy.deepcopy(man)
        v2["entries"][0]["planRow"] = {"packageId": "p", "cfg": [], "outputDigest": "0" * 64}
        self.expect("prepared-v3-v2-planrow-refused", lambda: K.frame_payload("rust-semantic", "PreparedOutputManifest", v2), "EXTERN_SCHEMA")
        big = {"planId": PLAN, "manifestSha256": "0" * 64, "entries": [dict(entries[0], outputOrdinal=i, logicalPath=f".opensip/prepared/v3/{i}-{entries[0]['blobSha256']}.blob") for i in range(257)]}
        self.expect("wire-prepared-257-entries-refused", lambda: K.frame_payload("rust-semantic", "PreparedOutputManifest", big), "ARRAY_BOUND")
        chunk = {"planId": PLAN, "outputOrdinal": 256, "chunkIndex": 0, "byteOffset": 0, "bytes": b"x"}
        self.expect("wire-prepared-ordinal-256-refused", lambda: K.frame_payload("rust-semantic", "PreparedOutputChunk", chunk), "UINT_BOUND")
        small = [{"packageId": 1}]
        self.add("encoded-length-exact", all(W.encoded_length(v) == len(W.encode(v)) for v in (man, small, {"x": [b"\x00" * 300, -70000, "é" * 70]})), "")

    def transitions(self):
        NE, ST = self.NE, self.ST
        vecs = self.s.vectors["vectors"]
        f = lambda *names: [{"frame": n} for n in names]
        caps = {"frame": "HelloAck", "capabilities": self.tokens}
        head = f("Hello") + [caps, {"frame": "OpenUniverse", "dependencyMode": True, "preparedMode": False}] + f(
            "UniverseAccepted", "SnapshotManifest", "SnapshotFileChunk", "SnapshotSeal", "SnapshotAccepted",
            "DependencySourceManifest", "DependencySourceChunk", "DependencySourceSeal", "DependencySourceAccepted")
        prepared_head = f("Hello") + [caps, {"frame": "OpenUniverse", "dependencyMode": True, "preparedMode": True}] + f(
            "UniverseAccepted", "SnapshotManifest", "SnapshotSeal", "SnapshotAccepted", "DependencySourceManifest", "DependencySourceSeal",
            "DependencySourceAccepted", "PreparedOutputManifest", "PreparedOutputChunk", "PreparedOutputSeal", "PreparedOutputAccepted")
        base = head + f("NativeContextVerified", "Analyze")
        tail = f("zero-exit", "eof")
        traces = {"complete": (base + f("FactBatch", "CoverageV3", "Complete") + tail, 1),
                  "two-stage": (base + f("FactBatch", "CoverageV3", "CoverageV3", "Complete") + tail, 2),
                  "prepared": (prepared_head + f("NativeContextVerified", "Analyze", "CoverageV3", "Complete") + tail, 1),
                  "unavailable-before-output": (base + f("Unavailable") + tail, 1),
                  "pre-analyze-unavailable": (head + f("Unavailable") + tail, 1),
                  "budget": (base + f("FactBatch", "BudgetExhausted") + tail, 1),
                  "fault": (head[:4] + f("ProviderFault") + tail, 1),
                  "cancel": (head[:6] + f("Cancel", "Cancelled") + tail, 1),
                  "cancel-start": (f("Cancel"), 1),
                  "no-identity": (f("Hello", "HelloAck", "OpenUniverse"), 1),
                  "post-terminal": (base + f("Unavailable", "FactBatch"), 1)}
        diffs = {}
        for name, (ev, n) in traces.items():
            a, b = NE.protocol3_run(ev, stage_count=n), AR.overlay_run(self.wire, self.p3, self.tokens, ev, n)
            if (a["finalPhase"], a["terminalKind"], a["trace"]) != (b["finalPhase"], b["terminalKind"], b["trace"]):
                diffs[name] = [a["trace"], b["trace"]]
        self.add("p3-overlay-differential", not diffs, diffs or sorted(traces))
        after = base + f("FactBatch", "Unavailable")
        m, o = NE.protocol3_run(after, 1), AR.overlay_run(self.wire, self.p3, self.tokens, after, 1)
        self.add("p3-unavailable-after-output-faults", o["finalPhase"] == "FAULT" and o["trace"][-1] == "P3-34" and m["trace"][-1] == "P3-25",
                 {"publishedTable": m["trace"][-2:], "overlay": o["trace"][-2:]})
        ob = AR.overlay_run(self.wire, self.p3, self.tokens, base + f("Unavailable") + tail, 1)
        self.add("p3-unavailable-before-output-admits", ob["finalPhase"] == "DONE" and "P3-25" in ob["trace"], ob["trace"][-3:])
        self.add("p3-cancel-in-start-no-row", NE.protocol3_run(f("Cancel"))["trace"] == ["P3-34"] and AR.overlay_run(self.wire, self.p3, self.tokens, f("Cancel"))["trace"] == ["P3-34"], "")
        race = [x["input"]["events"] for x in vecs["RUST3-PROVIDER-FAULT"] if x["id"] in ("fault-inflight-snapshot-manifest-unread", "fault-inflight-analyze-unread")]
        owner = [NE.protocol3_run(ev + [{"frame": "ProviderFault"}]) for ev in race]
        overlay = [AR.overlay_run(self.wire, self.p3, self.tokens, ev + [{"frame": "ProviderFault"}]) for ev in race]
        self.add("p3-race-traces-admitted-by-owner-table", len(race) == 2 and all(r["trace"][-1] == "P3-28" and r["terminalKind"] == "provider-fault" for r in owner + overlay),
                 [r["trace"][-2:] for r in owner])
        tcaps = {"frame": "HelloAck", "capabilities": list(ST.IDENTITY_TOKENS)}
        tbase = f("Hello") + [tcaps] + f("OpenUniverse", "UniverseAccepted", "SnapshotManifest", "SnapshotSeal", "SnapshotAccepted", "NativeContextVerified", "Analyze")
        post = {"frame": "Unavailable", "unavailablePayload": "post-analyze"}
        t_after, t_before, t_start = ST.typescript_protocol2_run(tbase + f("FactBatch") + [post]), ST.typescript_protocol2_run(tbase + [post]), ST.typescript_protocol2_run(f("Cancel"))
        self.add("ts2-order-unchanged", t_after["finalPhase"] == "FAULT" and t_before["trace"][-1] == "T2-14" and t_start["trace"] == ["T2-18"], [t_after["trace"][-1], t_before["trace"][-1], t_start["trace"]])

    def commitments(self):
        K, WI = self.K, self.WI
        payload = {"name": "x"}
        anchor = {"kind": "source-span", "snapshotId": SNAP, "path": "src/a.ts", "contentSha256": "1" * 64, "startByte": 0, "endByte": 1, "factId": None}
        vec = {"candidateOrdinal": 0, "relation": "declares", "resolution": "syntactic", "layer": "syntax", "producer": "typescript-semantic",
               "producerVersion": "typescript-provider 1.0.0", "schemaVersion": 1, "language": "typescript", "sourceUniverseId": "sha256:" + "1" * 64,
               "targetUniverseId": "sha256:" + "1" * 64, "confidenceMillionths": 1000000, "relationSchemaId": "opensip.relation.declares.v1",
               "canonicalRelationPayloadHex": W.encode(payload).hex(), "decodedRelationPayload": payload, "anchors": [anchor]}
        wire_c = {k: v for k, v in vec.items() if k not in ("canonicalRelationPayloadHex", "decodedRelationPayload")}
        wire_c["canonicalRelationPayload"] = W.encode(payload)
        commit = C("opensip.ts-provider.fact-batch.v1", [wire_c])

        def fb():
            out = WI.admit_fact_batch("typescript-semantic", {"analysisOrdinal": 0, "stageId": "s1", "batchIndex": 0, "facts": [vec], "batchCommitment": commit}, [])
            if not out["batchCommitmentVerified"] or out["wireCandidatesCborHex"] != W.encode([wire_c]).hex():
                raise Refuse("WIRE_MODEL_DISAGREES")
            K.frame_payload("typescript-semantic", "FactBatch", W.decode(W.encode({"analysisOrdinal": 0, "stageId": "s1", "batchIndex": 0, "facts": [wire_c], "batchCommitment": commit}), "ts2-cbor"), "false")
        self.expect("commit-ts2-fact-batch-matches-wire-model", fb)
        self.add("commit-empty-stream", W.encode([]) == b"\x80" and C("opensip.rust-provider.stage-facts.v2", []) == "sha256:" + hashlib.sha256(b"opensip.rust-provider.stage-facts.v2\x00\x80").hexdigest(), "")
        rust_c = dict(wire_c, producer="rust-semantic", language="rust", producerVersion="rust-provider 1.0.0")
        rust_v3 = {"schemaVersion": 3, "analysisOrdinal": 0, "stageId": "s1", "batchIndex": 0, "candidates": [rust_c], "occupancyCompanions": []}
        self.expect("wire-fact-batch-v3-rust3", lambda: K.frame_payload("rust-semantic", "FactBatch", W.decode(W.encode(rust_v3), "rust3-cbor"), "true"))
        self.expect("wire-fact-batch-v3-without-token-refused", lambda: K.frame_payload("rust-semantic", "FactBatch", rust_v3, "false"), "UNKNOWN_MEMBER")
        self.expect("wire-hex-vector-member-refused", lambda: K.check({"t": "ref", "ref": "Rust3FactCandidateV1"}, dict(rust_c, canonicalRelationPayloadHex="00"), "c"), "UNKNOWN_MEMBER")
        self.expect("wire-ts-producer-const", lambda: K.check({"t": "ref", "ref": "Ts2FactCandidateV1"}, rust_c, "c"), "CONST")
        self.expect("wire-rust3-anchor-path-lexical", lambda: K.check({"t": "ref", "ref": "Rust3FactCandidateV1"}, dict(rust_c, anchors=[dict(anchor, path="x\n/..")]), "c"), "PATH_LEXICAL")

    def wire_examples(self):
        K = self.K
        chunk = {"snapshotId": SNAP, "path": "src/a.ts", "chunkIndex": 0, "byteOffset": 0, "bytes": b"abc"}
        self.expect("wire-ts2-chunk-roundtrip", lambda: K.frame_payload("typescript-semantic", "SnapshotFileChunk", W.decode(W.encode(chunk), "ts2-cbor")))
        neg = W.encode(dict(chunk, chunkIndex=-1))
        self.expect("wire-ts2-negative-int-decodes-then-type-refuses", lambda: K.frame_payload("typescript-semantic", "SnapshotFileChunk", W.decode(neg, "ts2-cbor")), "TYPE_UINT64")
        self.expect("wire-rust3-negative-int-forbidden", lambda: W.decode(neg, "rust3-cbor"), "NEGATIVE_INTEGER_FORBIDDEN")
        self.expect("wire-non-shortest", lambda: W.decode(b"\x18\x05", "rust3-cbor"), "NON_SHORTEST")
        self.expect("wire-map-order", lambda: W.decode(b"\xa2" + W.encode("b") + W.encode(1) + W.encode("a") + W.encode(1), "ts2-cbor"), "MAP_ORDER")
        self.expect("wire-length-first-map-order", lambda: W.decode(b"\xa2" + W.encode("aa") + W.encode(1) + W.encode("b") + W.encode(1), "rust3-cbor"), "MAP_ORDER")
        self.expect("wire-duplicate-key", lambda: W.decode(b"\xa2" + W.encode("a") + W.encode(1) + W.encode("a") + W.encode(1), "ts2-cbor"), "DUPLICATE_KEY")
        self.expect("wire-float", lambda: W.decode(b"\xf9\x00\x00", "ts2-cbor"), "FLOAT_OR_SIMPLE")
        self.expect("wire-tag", lambda: W.decode(b"\xc0\x60", "rust3-cbor"), "TAG")
        self.expect("wire-indefinite", lambda: W.decode(b"\x5f\xff", "ts2-cbor"), "INDEFINITE_OR_RESERVED")
        self.expect("wire-non-nfc", lambda: W.decode(W.encode("e" + chr(0x301)), "rust3-cbor"), "NON_NFC")
        self.expect("wire-bytes-as-hex-text", lambda: K.frame_payload("typescript-semantic", "SnapshotFileChunk", dict(chunk, bytes="616263")), "TYPE_BYTES")
        self.expect("wire-bytes-as-json-array", lambda: K.frame_payload("rust-semantic", "SnapshotFileChunk", dict(chunk, bytes=[97, 98, 99])), "TYPE_BYTES")
        self.expect("wire-bytes-empty", lambda: K.frame_payload("rust-semantic", "SnapshotFileChunk", dict(chunk, bytes=b"")), "BYTES_BOUND")
        self.expect("wire-unknown-member", lambda: K.frame_payload("rust-semantic", "SnapshotFileChunk", dict(chunk, extra=1)), "UNKNOWN_MEMBER")
        self.expect("wire-missing-member", lambda: K.frame_payload("rust-semantic", "SnapshotFileChunk", {k: v for k, v in chunk.items() if k != "path"}), "MISSING_MEMBER")
        self.expect("wire-rust3-path-newline-dotdot", lambda: K.frame_payload("rust-semantic", "SnapshotFileChunk", dict(chunk, path="a\n/../b")), "PATH_LEXICAL")
        self.expect("wire-rust3-path-newline-plain", lambda: K.frame_payload("rust-semantic", "SnapshotFileChunk", dict(chunk, path="a\nb")))
        self.expect("wire-rust3-path-4097-bytes", lambda: K.frame_payload("rust-semantic", "SnapshotFileChunk", dict(chunk, path="é" * 2049)), "TEXT_UTF8_BYTES")
        cancel = {"executionId": None, "analysisOrdinal": None, "reason": "user-interrupt"}
        self.expect("wire-ts2-cancel-null-present", lambda: K.frame_payload("typescript-semantic", "Cancel", cancel))
        self.expect("wire-ts2-cancel-null-omitted-refused", lambda: K.frame_payload("typescript-semantic", "Cancel", {"analysisOrdinal": None, "reason": "user-interrupt"}), "MISSING_MEMBER")
        self.expect("wire-ts2-execution-id-grammar", lambda: K.frame_payload("typescript-semantic", "Cancel", dict(cancel, executionId="exec1_" + "0" * 32 + "\n")), "TEXT_PATTERN")

        def rust_cancel():
            K.frame_payload("rust-semantic", "Cancel", {"executionId": "exec1_" + "0" * 32, "analysisOrdinal": 0, "reason": "user-interrupt"})
            K.frame_payload("rust-semantic", "Cancelled", {"executionId": None, "analysisOrdinal": None, "observedPhase": "RECEIVING_DEPENDENCY"})
            K.frame_payload("rust-semantic", "ProviderFault", {"executionId": None, "analysisOrdinal": None, "phase": "WAIT_HELLO_ACK", "faultKind": "input-rejected", "detailCode": "x"})
        self.expect("rust3-cancel-types", rust_cancel)
        self.expect("rust3-cancel-host-shutdown-refused", lambda: K.frame_payload("rust-semantic", "Cancel", dict(cancel, reason="host-shutdown")), "CONST")
        self.expect("rust3-cancelled-start-phase-refused", lambda: K.frame_payload("rust-semantic", "Cancelled", {"executionId": None, "analysisOrdinal": None, "observedPhase": "START"}), "ENUM")
        stage = {"kind": "fact-derivation", "stageId": "s1", "relations": ["calls"], "operator": "semantic-provider"}
        self.expect("wire-optional-absent", lambda: K.check({"t": "ref", "ref": "Rust3C2PlanStageV3"}, stage, "planStage"))
        self.expect("wire-optional-null-refused", lambda: K.check({"t": "ref", "ref": "Rust3C2PlanStageV3"}, dict(stage, budget=None), "planStage"), "TYPE_MAP")
        pre = {"executionId": "exec1_" + "0" * 32, "snapshotId": SNAP, "planId": PLAN, "reason": "native-context-mismatch",
               "nativeContextId": "sha256:" + "1" * 64, "recomputedNativeContextId": "sha256:" + "2" * 64}
        self.expect("wire-unavailable-pre-analyze-selected", lambda: K.frame_payload("rust-semantic", "Unavailable", pre, "WAIT_NATIVE_CONTEXT_VERIFIED"))
        self.expect("wire-unavailable-pre-analyze-in-analyzing-refused", lambda: K.frame_payload("rust-semantic", "Unavailable", pre, "ANALYZING"), "EXTERN_SCHEMA")
        self.expect("wire-unavailable-unlawful-selector", lambda: K.frame_payload("typescript-semantic", "Unavailable", pre, "READY_ANALYZE"), "SELECTOR_UNLAWFUL")
        self.expect("wire-ts2-no-coveragev3-frame", lambda: K.frame_payload("typescript-semantic", "CoverageV3", {}), "UNKNOWN_FRAME")
        self.expect("wire-rust3-no-coverage-frame", lambda: K.frame_payload("rust-semantic", "Coverage", {}), "UNKNOWN_FRAME")
        env = {"protocolMajor": 3, "direction": "host-to-worker", "sequence": 0, "frameType": "SnapshotFileChunk", "payload": chunk}
        self.expect("wire-rust3-envelope", lambda: K.check_record("Rust3ProviderFrameV3", W.decode(W.encode(env), "rust3-cbor")))
        self.expect("wire-ts2-envelope-major-refused", lambda: K.check_record("Ts2FrameV2", {"protocolMajor": 3, "frameType": "Hello", "sequence": 0, "payload": {}}), "CONST")
        file_e = {"path": "src/lib.rs", "kind": "file", "byteLength": 1, "contentSha256": "1" * 64, "executable": False, "targetBytes": None}
        link_e = {"path": "src/link.rs", "kind": "symlink", "byteLength": None, "contentSha256": None, "executable": None, "targetBytes": b"lib.rs"}
        self.expect("wire-rust3-snapshot-variants", lambda: [K.check_record("Rust3SnapshotEntryV2", e) for e in (file_e, link_e)])
        self.expect("wire-rust3-symlink-executable-refused", lambda: K.check_record("Rust3SnapshotEntryV2", dict(link_e, executable=False)), "TYPE_NULL")
        big = "é" * 4096
        schema_accepts = not list(self.V({"$ref": CM.HS + "#/$defs/IdentityText"}, registry=self.reg).iter_errors(big))
        try:
            K.check({"t": "ref", "ref": "Rust3IdentityText"}, big, "id")
            code = None
        except Refuse as exc:
            code = exc.code
        self.add("json-schema-maxlength-not-byte-bound", schema_accepts and code == "TEXT_UTF8_BYTES", {"schemaAccepts": schema_accepts, "carrier": code})
        budget = {"analysisOrdinal": 0, "triggerStageId": "s1", "unit": "work-units", "limit": 7, "observed": 8, "coverage": [], "coverageCommitment": C("opensip.rust-provider.coverage-stream.v2", [])}

        def observed():
            K.frame_payload("rust-semantic", "BudgetExhausted", budget)
            AR.budget_observed(self.wire, budget, {"unit": "work-units", "limit": 7})
        self.expect("rust3-observed-limit-plus-one", observed)

    # ------------------------------------------------------------------ executed dialect (review-02 RF-3, review-03 RF-2)
    def node_run(self, flags, cases):
        if not self.node_ok:
            raise RuntimeError("reference engine bytes not verified; not executed")
        proc = subprocess.run([CM.NODE["path"], str(self.s.out / "tools" / "ecma_probe.js")], input=json.dumps({"flags": flags, "cases": cases}),
                              capture_output=True, text=True, env={"PATH": "/usr/bin:/bin"}, timeout=600)
        if proc.returncode != 0:
            raise RuntimeError("reference engine failed: " + proc.stderr[-300:])
        return json.loads(proc.stdout)

    def ecma(self):
        d = self.wire["privateRepresentation"]["patternDialect"]
        raw = Path(CM.NODE["path"]).read_bytes()
        self.node_ok = hashlib.sha256(raw).hexdigest() == CM.NODE["sha256"] == d["referenceEngine"]["sha256"] and len(raw) == CM.NODE["bytes"]
        engine = self.node_run(self.flags, [])["engine"] if self.node_ok else None
        self.add("ecma-engine-pinned", self.node_ok and engine == CM.NODE["versions"] == d["referenceEngine"]["versions"], {"engine": engine, "bytesVerified": self.node_ok})
        patterns = sorted({x["pattern"] for x in d["patternSites"]} | {x["pattern"] for x in PT.closure(self.wire, self.s.effective)["sites"]})
        out = self.node_run(self.flags, [{"pattern": p, "strings": CORPUS} for p in patterns])
        dis, py_dis = [], 0
        for p, res in zip(patterns, out["results"]):
            if isinstance(res, dict):
                dis.append([p, "engine-error", res])
                continue
            for s, r in zip(CORPUS, res):
                if W.ecma_test(p, self.flags, s) != r:
                    dis.append([p, s, r])
                py_dis += (re.search(p, s) is not None) != r
        self.add("ecma-differential", not dis and len(patterns) >= 13 and len(out["results"]) == len(patterns),
                 {"patterns": len(patterns), "strings": len(CORPUS), "disagreements": dis[:5], "pythonReDisagreementsForContrast": py_dis})
        prior = json.loads((self.s.out / "prior/review-02/probe_ecma_compare.json").read_text())
        pats = {"native2CanonicalPath": self.s.ne["$defs"]["CanonicalPath"]["pattern"], "logicalPath": self.s.ids3["$defs"]["LogicalPath"]["pattern"],
                "identityText": self.s.hs["$defs"]["IdentityText"]["pattern"]}
        mism, cases = [], []
        for name, p in pats.items():
            strings = [json.loads(k) for k in prior["ecma"][name]]
            cases.append({"pattern": p, "strings": strings})
            for s, want in zip(strings, prior["ecma"][name].values()):
                if W.ecma_test(p, self.flags, s) != want:
                    mism.append([name, "translation", s, want])
        replay = self.node_run(self.flags, cases)["results"]
        for (name, _), res in zip(pats.items(), replay):
            if res != list(prior["ecma"][name].values()):
                mism.append([name, "engine", res])
        self.add("ecma-review-probe-replayed", not mism and set(prior["ecma"]) == set(pats), mism[:6])

    def ecma_owner(self):
        pats = set()
        for dct in list(self.s.effective.values()) + list(self.s.docs.values()) + [self.s.relation, self.s.relation_effective]:
            all_patterns(dct, pats)
        pats |= {r["ecmaPattern"] for r in self.osucc["modelRegexRows"]}
        patterns = sorted(pats)
        strings = CORPUS + PATH_CORPUS
        out = self.node_run(self.flags, [{"pattern": p, "strings": strings} for p in patterns])
        dis = []
        for p, res in zip(patterns, out["results"]):
            if isinstance(res, dict):
                dis.append([p, "engine-error"])
                continue
            try:
                for s, r in zip(strings, res):
                    if W.ecma_test(p, self.flags, s) != r:
                        dis.append([p, s, r])
            except W.UnsupportedPattern as exc:
                dis.append([p, "unsupported", str(exc)])
        self.add("ecma-owner-differential", not dis and len(patterns) >= 20, {"ownerPatterns": len(patterns), "strings": len(strings), "disagreements": dis[:5]})

    def review03_replay(self):
        prior = json.loads((self.s.out / "prior/review-03/probe_canon_newline.out.json").read_text())["out"]
        native = self.s.ne["$defs"]["CanonicalPath"]["pattern"]
        lp = self.s.oc["$defs"]["LogicalPath"]
        pats = {"native2Canonical": native, "logicalPath": lp["pattern"], "logicalPathNot": lp["not"]["pattern"]}
        mism = []
        for name, p in pats.items():
            strings = [json.loads(k) for k in prior[name]]
            engine = self.node_run(self.flags, [{"pattern": p, "strings": strings}])["results"][0]
            for s, want, e in zip(strings, prior[name].values(), engine):
                if W.ecma_test(p, self.flags, s) != want or e != want:
                    mism.append([name, s, want])
        corrected = OS.corrected(native)
        strings = [json.loads(k) for k in prior["native2Canonical"]]
        engine = self.node_run(self.flags, [{"pattern": corrected, "strings": strings}])["results"][0]
        lexical = [self.lexical_ok("relative-path-dot-segments", s) for s in strings]
        changed = [s for s, before, after in zip(strings, prior["native2Canonical"].values(), engine) if before != after]
        ok = (not mism and engine == lexical and bool(changed)
              and all(any(t in s for t in (NL, CR_, LS, PS)) and not self.lexical_ok("relative-path-dot-segments", s) for s in changed)
              and all(e for s, e in zip(strings, engine) if s in ("a/.." + NL, ".." + NL, "a/." + NL)))
        self.add("ecma-review03-probe-replayed", ok, {"pinnedReplayMismatches": mism[:4], "correctedChanges": changed, "correctedEqualsLexical": engine == lexical})

    def newline(self):
        NE, K = self.NE, self.K
        native = self.s.ne["$defs"]["CanonicalPath"]["pattern"]
        cx = ["a/..\n", "a/.\n", "..\n"]
        engine = self.node_run(self.flags, [{"pattern": native, "strings": cx}])["results"][0]
        trans = [W.ecma_test(native, self.flags, x) for x in cx]
        python_re = [re.search(native, x) is not None for x in cx]
        lexical = []
        for x in cx:
            try:
                AR.path_admission(self.wire, "CANONICAL-PATH-ADMISSION", x)
                lexical.append(True)
            except Refuse:
                lexical.append(False)
        entries = [{"packageKey": "serde 1.0.200 registry+x", "path": x, "byteLength": 1, "contentSha256": "1" * 64} for x in cx]
        man = {"dependencySourceSetId": "sha256:" + "1" * 64, "manifestSha256": raw_hex(entries), "entries": entries}
        try:
            K.frame_payload("rust-semantic", "DependencySourceManifest", man)
            carrier = None
        except Refuse as exc:
            carrier = exc.code
        self.add("ecma-newline-counterexamples", engine == trans == lexical == [True] * 3 and python_re == [False] * 3 and carrier is None,
                 {"engine": engine, "translation": trans, "pythonRe": python_re, "canonicalPathSegments": lexical, "dependencyManifestCarrier": carrier})

    # ------------------------------------------------------------------ review-03 RF-1 / RF-2 owner successor behaviour
    def path_site_bindings(self):
        sites = [x for x in self.wire["pathSites"] if x["kind"] == "schema-string"]
        cases = []
        for site in sites:
            node = OS.node_at(self.s.effective[site["location"]["document"]], site["location"]["pointer"])
            neg = node["not"].get("pattern") if isinstance(node.get("not"), dict) else None
            cases += [{"pattern": node["pattern"], "strings": PATH_CORPUS}, {"pattern": neg or "(?!)", "strings": PATH_CORPUS}]
        results = self.node_run(self.flags, cases)["results"]
        bad, bindings = [], 0
        for i, site in enumerate(sites):
            effective = [p and not n for p, n in zip(results[2 * i], results[2 * i + 1])]
            for b in site["bindings"]:
                bindings += 1
                lx = [self.lexical_ok(b["rule"], x) for x in PATH_CORPUS]
                if b["relation"] == "equivalent" and lx != effective:
                    bad.append([site["location"]["pointer"], b["rule"], [x for x, l_, e in zip(PATH_CORPUS, lx, effective) if l_ != e][:3]])
                if b["relation"] == "narrowed" and any(l_ and not e for l_, e in zip(lx, effective)):
                    bad.append([site["location"]["pointer"], b["rule"], "narrowed admits beyond the schema"])
        for site in [x for x in self.wire["pathSites"] if x["kind"] == "wire-lexical-scalar"]:
            rule = site["bindings"][0]["rule"]
            if self.lexical_ok(rule, "x" + NL + "/../y") or not self.lexical_ok(rule, "a/.." + NL):
                bad.append([site["location"]["pointer"], rule, "normative rule does not compare complete segments"])
        self.add("path-site-bindings-executed", not bad and len(sites) >= 7 and bindings >= 8, {"schemaSites": len(sites), "bindings": bindings, "bad": bad[:4]})

    def owner_successor_behaviour(self):
        NE, NE_S = self.NE, self.NE_S
        node = OS.node_at(self.s.effective[CM.NE], "#/$defs/DependencyFileManifestV1/items/properties/path")
        engine = self.node_run(self.flags, [{"pattern": node["pattern"], "strings": PATH_CORPUS}])["results"][0]

        def owner_results(mod):
            out = []
            for x in PATH_CORPUS:
                try:
                    mod.validate_native("DependencyFileManifestV1", [{"path": x, "contentSha256": "1" * 64, "byteLength": 1}])
                    out.append(True)
                except Exception:  # noqa: BLE001
                    out.append(False)
            return out
        succ_r, pinned_r = owner_results(NE_S), owner_results(NE)
        self.add("owner-successor-evaluates-ecma", succ_r == engine and pinned_r != engine,
                 {"successorDisagreements": [x for x, a, b in zip(PATH_CORPUS, succ_r, engine) if a != b][:4],
                  "pinnedDisagreements": [x for x, a, b in zip(PATH_CORPUS, pinned_r, engine) if a != b][:6]})
        outcomes = {}
        dep_cases = {"a/.." + NL: "admitted", ".." + NL: "admitted", "a/." + NL: "admitted", "a" + NL + "b": "admitted",
                     "a" + NL + "/../b": "route", "x" + LS + "/../y": "route", "./a": "route", "/abs": "route", "C:x": "route"}
        for path, want in dep_cases.items():
            lock, provided, activated = self.depsrc_case({"files": ["Cargo.toml", path]})
            try:
                out = REP.dependency_source_set_admit_successor(NE_S, self.wire, lock, provided, activated)
                got = "admitted" if out["admitted"] and out["identity"] else ("route" if out["successorRefusal"] else "owner-refusal")
            except Exception as exc:  # noqa: BLE001
                got = "EXCEPTION:" + type(exc).__name__
            outcomes["dependency " + json.dumps(path)] = [got, want]
        prep_cases = [({"generatedLogicalPath": "a/.." + NL}, "admitted"), ({"generatedLogicalPath": "x" + NL + "/../../escape.rs"}, "route"),
                      ({"generatedLogicalPath": "../escape.rs"}, "route"), ({"sitePath": "x" + NL + "/../y.rs"}, "route"), ({"sitePath": "a/.." + NL}, "admitted")]
        for case, want in prep_cases:
            prep, explicit = self.prepared_path_case(case)
            try:
                out = REP.prepared_output_set_admit_successor(NE_S, self.wire, prep, self.fx["ctx"], explicit)
                got = out["outcome"] if out["outcome"] != "rejected" else ("route" if out["successorRefusal"] else "owner-refusal")
            except Exception as exc:  # noqa: BLE001
                got = "EXCEPTION:" + type(exc).__name__
            outcomes["prepared " + json.dumps(case)] = [got, want]
        self.add("owner-successor-no-untyped-exception", all(g == w for g, w in outcomes.values()), outcomes)

        def pinned(fn):
            try:
                r = fn()
                return r
            except Exception as exc:  # noqa: BLE001
                return type(exc).__name__
        lock, provided, activated = self.depsrc_case({"files": ["Cargo.toml", "a/.." + NL]})
        dep = pinned(lambda: NE.dependency_source_set_admit(lock, provided, activated)["admitted"])
        prep_legit, _ = self.prepared_path_case({"generatedLogicalPath": "a/.." + NL})
        prep_escape, _ = self.prepared_path_case({"generatedLogicalPath": "x" + NL + "/../../escape.rs"})
        legit = pinned(lambda: NE.prepared_output_set_admit(prep_legit, self.fx["ctx"], True)["outcome"])
        escape = pinned(lambda: NE.prepared_output_set_admit(prep_escape, self.fx["ctx"], True)["outcome"])
        self.add("owner-pinned-model-python-re-divergence", dep == "ValidationError" and legit == "ValidationError" and escape == "admitted",
                 {"pinnedDependencySetLegitName": dep, "pinnedPreparedSetLegitName": legit, "pinnedPreparedSetNewlineHiddenEscape": escape,
                  "recorded": "defects of the PINNED owner; owner-pattern-successor.v1.json is the proposed reference owner correction (author candidate) and its behaviour is owner-successor-evaluates-ecma and owner-successor-no-untyped-exception"})

    # ------------------------------------------------------------------ RF-2 (review-02): reachability, accounting, bound
    def reachability(self):
        NE, NE_S, doc = self.NE, self.NE_S, self.wire
        dep = {}
        for name, case in [("drive-prefix", {"files": ["Cargo.toml", "C:x"]}), ("empty-segment", {"files": ["Cargo.toml", "a//b"]}),
                           ("trailing-slash", {"files": ["Cargo.toml", "a/"]}), ("non-nfc-path", {"files": ["Cargo.toml", "e" + chr(0x301) + ".rs"]}),
                           ("non-nfc-name", {"name": "e" + chr(0x301)}), ("space-in-name", {"name": "se rde"}),
                           ("newline-hidden-dotdot", {"files": ["Cargo.toml", "a" + NL + "/../b"]})]:
            lock, provided, activated = self.depsrc_case(case)
            owner = NE.dependency_source_set_admit(lock, provided, activated)
            succ = REP.dependency_source_set_admit_successor(NE_S, doc, lock, provided, activated)
            dep[name] = bool(owner["admitted"] and owner["identity"] and succ["successorRefusal"] and succ["identity"] is None)
        self.add("owner-admits-unrepresentable-dependency-inputs", all(dep.values()) and len(dep) == 7, dep)
        prep = {}
        for name, case in [("257-rows", {"fixture": "prepInert", "rows": 257}), ("blob-over", {"fixture": "prepInert", "rows": 2, "blobByteLengths": [[0, 1073741824], [1, 1]]})]:
            p, explicit = self.prepared_case(case)
            owner = NE.prepared_output_set_admit(copy.deepcopy(p), self.fx["ctx"], explicit)
            succ = REP.prepared_output_set_admit_successor(NE_S, doc, p, self.fx["ctx"], explicit)
            prep[name] = owner["outcome"] == "admitted" and succ["successorRefusal"] is not None
        rows_max = self.s.ne["$defs"]["PreparedOutputSetV3"]["properties"]["rows"]["maxItems"]
        self.add("owner-admits-over-limit-prepared-sets", all(prep.values()) and rows_max > int(AR.params(doc, "PREPARED-V3-WIRE-LIMIT")["maxEntries"]), dict(prep, ownerRowsMaxItems=rows_max))

    def accounting(self):
        WI, doc = self.WI, self.wire
        enc = WI.wire_cbor
        detail, ok = {}, True
        cases, bad = 0, []
        for proto, env, ft, base in (("rust-semantic", REP.rust3_envelope, "DependencySourceChunk", {"dependencySourceSetId": "sha256:" + "1" * 64, "packageKey": "a 1 x", "path": "src/lib.rs"}),
                                     ("rust-semantic", REP.rust3_envelope, "SnapshotFileChunk", {"snapshotId": SNAP, "path": "a"}),
                                     ("rust-semantic", REP.rust3_envelope, "PreparedOutputChunk", {"planId": PLAN, "outputOrdinal": 255}),
                                     ("typescript-semantic", REP.ts2_envelope, "SnapshotFileChunk", {"snapshotId": SNAP, "path": "a"})):
            for seq in (0, 22, 23, 254, 255, 65534, 65535, 2 ** 32 - 1, 2 ** 32):
                for length, max_chunk in ((1, 1048576), (23, 1048576), (24, 1048576), (255, 1048576), (256, 1048576), (65535, 1048576),
                                          (65536, 1048576), (1048576, 1048576), (300, 24), (600, 256), (131073, 65536)):
                    acc = REP.Accountant(doc, env, 2 ** 64)
                    acc.seq = seq
                    sizes = [x[0] for x in acc.chunk_sizes(ft, base, length, max_chunk, ("probe",))]
                    k = -(-length // max_chunk)
                    real = [len(enc(env(seq + i, ft, dict(base, chunkIndex=i, byteOffset=i * max_chunk, bytes=b"\x00" * (max_chunk if i < k - 1 else length - (k - 1) * max_chunk)))))
                            for i in range(k)]
                    cases += 1
                    if sizes != real:
                        bad.append([ft, seq, length, max_chunk, sizes[:3], real[:3]])
        detail["chunkClosedForm"] = {"cases": cases, "mismatches": bad[:3]}
        ok = ok and not bad
        vec = next(x for x in self.s.vectors["vectors"]["REQUEST-WIRE-ACCOUNTING"] if x["id"] == "dependency-manifest-frame-exactly-at-limit")
        req = REP.build_plan(vec["input"]["plan"], self.fx, AR.prepared_entries)
        dm = req["dependencyManifest"]
        seq = 4
        empty = len(enc(REP.rust3_envelope(seq, "DependencySourceManifest", dict(dm, entries=[]))))
        groups, last = [], None
        for e in dm["entries"]:
            if e is not last:
                groups.append([e, 0])
                last = e
            groups[-1][1] += 1
        closed = empty - 1 + W._head_len(len(dm["entries"])) + sum(n * len(enc(e)) for e, n in groups)
        limit = int(self.limits("rust-semantic")["maxFramePayloadBytes"])
        planned = REP.plan(doc, self.limits("rust-semantic"), vec["input"]["plan"], self.fx, AR.prepared_entries)["largestFrame"]["DependencySourceManifest"]
        detail["dependencyManifestBoundary"] = {"closedForm": closed, "planned": planned, "limit": limit, "entries": len(dm["entries"])}
        ok = ok and closed == planned == limit
        small = next(x for x in self.s.vectors["vectors"]["REQUEST-WIRE-ACCOUNTING"] if x["id"] == "frames-small-request")["input"]["plan"]
        req = REP.build_plan(small, self.fx, AR.prepared_entries)
        lim = self.limits("rust-semantic")
        frames = [("Hello", req["hello"]), ("OpenUniverse", req["openUniverse"]), ("SnapshotManifest", req["snapshotManifest"])]
        for e in req["snapshotManifest"]["entries"]:
            frames += [("SnapshotFileChunk", {"snapshotId": req["snapshotManifest"]["snapshotId"], "path": e["path"], "chunkIndex": 0, "byteOffset": 0, "bytes": b"\x00" * e["byteLength"]})]
        frames.append(("SnapshotSeal", REP.seal_payload(req["snapshotManifest"], "snapshotId", "totalFileBytes", int(lim["maxSnapshotChunkBytes"]), REP.FILE_LEN)))
        dm = req["dependencyManifest"]
        frames.append(("DependencySourceManifest", dm))
        for e in dm["entries"]:
            frames.append(("DependencySourceChunk", {"dependencySourceSetId": dm["dependencySourceSetId"], "packageKey": e["packageKey"], "path": e["path"], "chunkIndex": 0, "byteOffset": 0, "bytes": b"\x00" * e["byteLength"]}))
        frames.append(("DependencySourceSeal", REP.seal_payload(dm, "dependencySourceSetId", "totalBytes", int(lim["maxDependencySourceChunkBytes"]), lambda e: e["byteLength"])))
        frames += [("Analyze", req["analyze"]), ("Cancel", {"executionId": req["openUniverse"]["executionId"], "analysisOrdinal": 0, "reason": "user-interrupt"})]
        materialized = sum(len(enc(REP.rust3_envelope(i, ft, p))) for i, (ft, p) in enumerate(frames))
        res = REP.plan(doc, lim, small, self.fx, AR.prepared_entries)
        detail["smallRequest"] = {"materializedBytes": materialized, "plannedBytes": res["payloadBytes"], "materializedFrames": len(frames), "plannedFrames": res["frames"]}
        ok = ok and materialized == res["payloadBytes"] and len(frames) == res["frames"]
        for ft, p in frames:
            if ft in ("Hello", "OpenUniverse", "SnapshotFileChunk", "DependencySourceChunk", "SnapshotSeal", "DependencySourceManifest", "DependencySourceSeal", "Cancel"):
                try:
                    self.K.frame_payload("rust-semantic", ft, p)
                except Refuse as exc:
                    detail.setdefault("carrierRefusedPlannedFrame", []).append([ft, exc.code])
        ok = ok and "carrierRefusedPlannedFrame" not in detail
        self.add("request-accounting-closed-form-matches-owner-encoder", ok, detail)
        limits = self.limits("rust-semantic")
        min_dep = len(enc({"packageKey": "a 1 ", "path": "a", "byteLength": 0, "contentSha256": "0" * 64}))
        min_snap = len(enc({"path": "a", "kind": "file", "byteLength": 0, "contentSha256": "0" * 64, "executable": False, "targetBytes": None}))
        b = REP.rust3_frames_upper_bound(limits, min_dep, min_snap, 0)
        self.add("request-frames-bound-unreachable", b["bound"] < int(limits["maxRequestFrames"]), dict(b, maxRequestFrames=limits["maxRequestFrames"], minimalDependencyEntryBytes=min_dep, minimalSnapshotEntryBytes=min_snap))

    # ------------------------------------------------------------------ review-03 RF-4: send schedule
    def schedule(self):
        doc, enc = self.wire, self.WI.wire_cbor
        base = {"dependencySourceSetId": "sha256:" + "1" * 64, "packageKey": "serde 1.0.200 registry+x", "path": "src/lib.rs"}

        def total(sizes):
            t, off = 0, 0
            for i, n in enumerate(sizes):
                t += len(enc(REP.rust3_envelope(i, "DependencySourceChunk", dict(base, chunkIndex=i, byteOffset=off, bytes=b"\x00" * n))))
                off += n
            return t
        greedy = total([24, 6])
        alternatives = {str(a): total(a) for a in ([6, 24], [7, 23], [8, 22])}
        planned = sum(x[0] for x in REP.Accountant(doc, REP.rust3_envelope, 2 ** 64).chunk_sizes("DependencySourceChunk", base, 30, 24, ("probe",)))
        vec = next(x for x in self.s.vectors["vectors"]["HOST-SEND-SCHEDULE"] if x["id"] == "byte-smaller-alternate-chunking-still-refused")
        refused = self.code_of(lambda: self.run_vector("HOST-SEND-SCHEDULE", self.expand(vec["input"])))
        smaller = [k for k, t in alternatives.items() if t < greedy]
        self.add("schedule-not-byte-minimal", planned == greedy and bool(smaller) and refused == "SENDER_DIVERGENCE:chunk-schedule",
                 {"greedyBytes": greedy, "alternativeBytes": alternatives, "plannedGreedyBytes": planned, "senderOnSmallerAlternative": refused})
        agree, checked = [], 0
        for vec in self.s.vectors["vectors"]["REQUEST-WIRE-ACCOUNTING"]:
            p = vec["input"]["plan"]
            if vec["kind"] != "accept" or p.get("limitsOverride"):
                continue
            limits = self.limits(p["protocol"])
            req = REP.build_plan(p, self.fx, AR.prepared_entries)
            plan = (REP.plan_rust3_request if p["protocol"] == "rust-semantic" else REP.plan_ts2_request)(doc, limits, req)
            frames = SR.realize(req, p["protocol"], limits)
            frames = frames + [SR.cancel_frame(len(frames), SR.expected_cancel(plan, len(plan["schedule"])))]
            try:
                res = SR.consume(plan, p["protocol"], AR.params(doc, "REQUEST-WIRE-ACCOUNTING"), limits, frames)
                good = res["complete"] and res["framesSent"] == plan["frames"] and res["payloadBytesSent"] <= plan["payloadBytes"] and res["slotsConsumed"] == len(plan["schedule"])
            except Refuse as exc:
                good = False
                agree.append([vec["id"], exc.code])
            checked += 1
            if not good and not agree[-1:]:
                agree.append([vec["id"], "totals"])
        self.add("schedule-realization-agrees", not agree and checked >= 10, {"plansRealizedAndConsumed": checked, "failures": agree[:4]})

    # ------------------------------------------------------------------ review-04 RF-2 / RF-3: scope, no-change, relation payloads
    def owner_scope(self):
        """The ECMA interpretation reaches exactly the declared (document, consumer) pairs: each consumer changes as declared,
        only the scoped instances carry the scoped canonical view, only the scoped documents are marked, no canonical
        module class is modified, and every non-parent document review-04 found affected is evaluated as pinned."""
        bad, legit = "x" + NL + "/../y.rs", "a/.." + NL

        def verdict(fn):
            try:
                fn()
                return True
            except Exception:  # noqa: BLE001 - any owner refusal
                return False

        def startup(mod, value):
            ou = copy.deepcopy(self.fx["startupRustOpenUniverse"])
            find(ou, "crateRootPaths")["crateRootPaths"] = [value]
            mod.validate_startup("OpenUniverseV3", ou)
        probes = {
            "native-evidence-model": lambda m, v: m["NE"].validate_native("DependencyFileManifestV1", [{"path": v, "contentSha256": "1" * 64, "byteLength": 1}]),
            "provider-startup-model": lambda m, v: startup(m["ST"], v),
            "provider-wire-model": lambda m, v: m["WI"].C.validate({"$ref": CM.OC + "#/$defs/LogicalPath"}, v, registry=m["WI"].REGISTRY),
            "identity-model-v3-registered-records": lambda m, v: m["IM3"].validate_registered_record(OS.RELATION_DOC_PATH, "#/$defs/FilePayloadV1", {"byteLength": 3, "contentSha256": "1" * 64, "path": v}),
        }
        pinned = {"NE": self.NE, "ST": self.ST, "WI": self.WI, "IM3": self.IM3}
        succ = {"NE": self.NE_S, "ST": self.ST_S, "WI": self.WI_S, "IM3": self.IM3_S}
        declared = [x["id"] for x in self.osucc["scope"]]
        consumers, ok = {}, sorted(declared) == sorted(probes)
        for sid, probe in probes.items():
            r = {"successor[newline-hidden, dotdot-lf]": [verdict(lambda: probe(succ, bad)), verdict(lambda: probe(succ, legit))],
                 "pinned[newline-hidden, dotdot-lf]": [verdict(lambda: probe(pinned, bad)), verdict(lambda: probe(pinned, legit))]}
            consumers[sid] = r
            ok = ok and r["successor[newline-hidden, dotdot-lf]"] == [False, True] and r["pinned[newline-hidden, dotdot-lf]"] != [False, True]
        scoped = [self.NE_S.C, self.ST_S.C, self.WI_S.C, self.IM3_S.C]
        unscoped = {"NE.IM.C": self.NE_S.IM.C, "NE.STARTUP.C": self.NE_S.STARTUP.C, "NE.WIRE.C": self.NE_S.WIRE.C, "WI.FP": self.WI_S.FP}
        instances_ok = all(isinstance(x, OS.ScopedCanonical) for x in scoped) and not any(isinstance(x, OS.ScopedCanonical) for x in unscoped.values())
        classes_ok = all(x._base.ExactValidator.VALIDATORS["pattern"] is Draft202012Validator.VALIDATORS["pattern"] for x in scoped) and \
            all(m.ExactValidator.VALIDATORS["pattern"] is Draft202012Validator.VALIDATORS["pattern"] for m in (self.NE_S.IM.C, self.NE_S.STARTUP.C, self.NE_S.WIRE.C))
        marked, pinned_marked = set(), set()
        for m in (self.NE_S, self.NE_S.IM, self.NE_S.STARTUP, self.NE_S.WIRE, self.ST_S, self.WI_S, self.WI_S.FP, self.IM3_S):
            OS.marked_documents(vars(m), marked)
        for m in (self.NE, self.ST, self.WI, self.IM3):
            OS.marked_documents(vars(m), pinned_marked)
        want_docs = {x["document"] for x in self.osucc["scope"]}
        self.add("owner-successor-scope-installed", ok and instances_ok and classes_ok and marked == want_docs and not pinned_marked,
                 {"consumers": consumers, "scopedInstancesOnly": instances_ok, "canonicalClassesUnmodified": classes_ok,
                  "markedDocuments": sorted(marked), "declaredDocuments": sorted(want_docs), "pinnedMarked": sorted(pinned_marked)})

        prior = json.loads((self.s.out / "prior/review-04/probe_dialect_scope.out.json").read_text())["perDocument"]
        named = sorted(k for k, d in prior.items() if not d["inSuccessorParents"] and d["pythonVsEcmaChangedOnCorpus"] and k not in OS.ROW_DOC_KEYS)
        no_change = [x["key"] for x in self.osucc["noChangeDocuments"]]
        self.add("owner-successor-no-change-set-closed", named == sorted(no_change),
                 {"review04AffectedNonParentDocuments": named, "declaredNoChange": no_change, "nowInScope": [k for k in OS.ROW_DOC_KEYS if k in prior]})
        registered = lambda doc: (lambda m, sel, v: m["IM3"].validate_registered_record(doc, sel, v))
        consumer_sets = {
            "identitySchemas2": [("native model IM (identity-model.py) validate_registered_record", lambda m, sel, v: m["NE"].IM.validate_registered_record("foundation/identity-schemas.v2.json", sel, v)),
                                 ("identity-model.v3 validate_registered_record", registered("foundation/identity-schemas.v2.json"))],
            "identitySchemas3": [("identity-model.v3 validate_registered_record", registered("foundation/identity-schemas.v3.json"))],
            "workflowCommon": [("native model validate_workflow", lambda m, sel, v: m["NE"].validate_workflow(m["NE"].WORKFLOW_COMMON_DOC, sel, v))],
        }
        pattern_consumers = [(inst + ".C (scoped canonical view)", (lambda inst: lambda m, pat, v: m[inst].C.validate({"pattern": pat}, v))(inst)) for inst in ("NE", "ST", "WI", "IM3")]
        examples = [(k, ex) for k in no_change for ex in prior.get(k, {}).get("changedExamples", [])]
        engine = self.node_run(self.flags, [{"pattern": ex[1], "strings": [ex[2]]} for _, ex in examples])["results"] if examples else []
        extra = ["a/b", "a/..", "../b", "x" + NL + "/../y", "a" + LS + "/../b", ".." + NL]
        for key in no_change:
            rows, good = [], True
            for (k, (pointer, pattern, string)), res in zip(examples, engine):
                if k != key:
                    continue
                python_re = re.search(pattern, string) is not None
                marked_view = verdict(lambda: self.NE_S.C.validate({"pattern": pattern, OS.NODE_MARK: True}, string))
                row = {"pointer": pointer, "string": string, "engine": res[0], "pythonRe": python_re, "markedNodeWouldEvaluate": marked_view}
                if pointer.startswith("#/$defs/"):
                    selector = "#/$defs/" + pointer.split("/")[2]
                    cons = [(name, (lambda fn: lambda m, v: fn(m, selector, v))(fn)) for name, fn in consumer_sets[key]]
                else:
                    cons = [(name, (lambda fn: lambda m, v: fn(m, pattern, v))(fn)) for name, fn in pattern_consumers]
                for name, fn in cons:
                    for value in [string] + (extra if pointer.startswith("#/$defs/") else []):
                        a, b = verdict(lambda: fn(pinned, value)), verdict(lambda: fn(succ, value))
                        if a != b:
                            row.setdefault("changed", []).append([name, value, a, b])
                row["consumers"] = [name for name, _ in cons]
                good = good and res[0] != python_re and marked_view == res[0] and "changed" not in row
                rows.append(row)
            self.add("owner-successor-no-change:" + key, good and bool(rows), rows)

    def relation_payload(self):
        sites = self.osucc["relationPayloadPathSites"]
        vecs = self.s.vectors["vectors"].get("RELATION-PAYLOAD-PATH-LAW", [])
        per_site = {}
        for x in vecs:
            c = x["input"]["relation"]
            site = "#/$defs/%s/properties/%s" % (c["def"], c["property"])
            pinned = self.code_of(lambda: self.relation_case(self.IM3, c))
            per_site.setdefault(site, []).append([x["id"], x["kind"], pinned])
        divergent = {site: any(k == "refuse" and p is None for _, k, p in rows) and any(k == "accept" and p == "REGISTERED_RECORD" for _, k, p in rows)
                     for site, rows in per_site.items()}
        text = self.s.raw["identityModel3"].decode("utf-8")
        i = text.find("def registered_payload(")
        retained_call = i >= 0 and "validate_registered_record(row['document'],row['selector'],value)" in text[i:i + 2400]
        self.add("relation-payload-sites-covered-and-pinned-divergence", sorted(per_site) == sorted(sites) and len(sites) == 4 and all(divergent.values()) and retained_call,
                 {"sites": sites, "pinnedDivergenceBothDirections": divergent, "retainedFactAdmissionCallsValidateRegisteredRecord": retained_call, "pinnedCodes": per_site,
                  "notDriven": "admit_frame over a retained Run bundle (needs a retained bundle); validate_registered_record is the call it makes"})

    def fact_plane_path(self):
        """The historical fact-plane v1 CBOR-profile checker check-fact-plane.py _is_path (review-05 A-1 framing): it has no
        terminator-bounded lookahead and is unchanged by the successor. It is stricter than its own normative
        sharedTypes.CanonicalPath because it reuses _is_nfc_text. Retained fact2 admission never calls it."""
        strings = PATH_CORPUS
        corrected = OS.corrected(self.s.relation["$defs"]["CanonicalPath"]["pattern"])
        engine = self.node_run(self.flags, [{"pattern": corrected, "strings": strings}])["results"][0]
        fp_p, fp_s = [self.WI.FP._is_path(x) for x in strings], [self.WI_S.FP._is_path(x) for x in strings]
        hidden = [x for x in strings if any(t in x for t in (NL, CR_, LS, PS)) and not self.lexical_ok("relative-path-dot-segments", x)]
        unsafe = [x for x, f in zip(strings, fp_s) if f and not self.lexical_ok("relative-path-dot-segments", x)]
        narrower = [x for x, f, e in zip(strings, fp_s, engine) if e and not f]
        normative = self.s.fp["factRecordContractV1"]["relationPayloadSchemaRegistryV1"]["sharedTypes"]["CanonicalPath"]
        fact2_calls = "_is_path" in self.s.raw["identityModel3"].decode("utf-8")
        self.add("fact-plane-path-law-no-change", fp_p == fp_s and not isinstance(self.WI_S.FP, OS.ScopedCanonical) and not unsafe and bool(hidden)
                 and not any(self.WI_S.FP._is_path(x) for x in hidden) and "control" not in normative and not fact2_calls,
                 {"checker": "check-fact-plane.py _is_path (pin checkFactPlane): the historical fact-plane v1 deterministic-CBOR profile checker", "sameUnderSuccessor": fp_p == fp_s,
                  "admitsARealDotSegment": unsafe, "refusesTerminatorHiddenSegments": hidden, "checkerRefusesNamesTheCorrectedSchemaAdmits": narrower,
                  "normativeSharedTypesCanonicalPath": normative, "identityModelV3ReferencesIsPath": fact2_calls,
                  "reading": "the checker's control-scalar refusal comes from _is_nfc_text (the CanonicalText clause), not from the normative CanonicalPath type; retained fact2 admission (identity-model.v3 registered_payload) does not call it, so it neither refuses nor admits fact2 relation payload paths"})

    def relation_gap(self):
        """review-05 A-1: the relation v2 CanonicalPath path-normalization gap, recorded as a relation-registry / fact-plane
        duty and deliberately NOT corrected by the scoped successor."""
        inherited = self.s.fp["factRecordContractV1"]["relationPayloadSchemaRegistryV1"]["sharedTypes"]["CanonicalPath"]
        cases = {"a//b.rs": "empty segment", "a/": "empty final segment", "a" + chr(7) + "b.rs": "C0 control"}
        rows = {}
        for x, why in cases.items():
            pinned = self.code_of(lambda: self.IM3.validate_registered_record(OS.RELATION_DOC_PATH, "#/$defs/CanonicalPath", x))
            scoped = self.code_of(lambda: self.IM3_S.validate_registered_record(OS.RELATION_DOC_PATH, "#/$defs/CanonicalPath", x))
            rows[json.dumps(x)] = {"why": why, "pinnedAdmits": pinned is None, "scopedAdmits": scoped is None}
        text = self.s.raw["identityModel3"].decode("utf-8")
        rule = next(r for r in self.wire["admission"] if r["id"] == "RELATION-PAYLOAD-PATH-LAW")["rule"]
        duties = " ".join(self.s.succ.get("futureQualification", []))
        relation_rows = [r for r in self.osucc["schemaPatternRows"] if r["document"] == self.s.relation["$id"]]
        i = text.find("def registered_payload(")
        ok = (all(r["pinnedAdmits"] and r["scopedAdmits"] for r in rows.values()) and "no empty" in inherited and "_is_path" not in text and i >= 0
              and "does not call the historical fact-plane v1 checker _is_path" in rule and "path-normalization gap" in rule.replace("path normalization", "path-normalization") + duties
              and "path-normalization gap" in duties and len(relation_rows) == 1)
        self.add("relation-registry-path-normalization-gap-recorded", ok,
                 {"relationV2CanonicalPath": rows, "inheritedFactPlaneV1CanonicalPath": inherited, "successorRelationRows": len(relation_rows),
                  "identityModelV3CallsIsPath": "_is_path" in text, "ruleStatesFact2DoesNotCallIsPath": "does not call the historical fact-plane v1 checker _is_path" in rule,
                  "dutyDeclared": "path-normalization gap" in duties})

    def sender_cancel_law(self):
        """The reference sender's Cancel echo law equals CANCEL-NULLABILITY (tools/admission_ref.py) at every position."""
        doc, acc = self.wire, AR.params(self.wire, "REQUEST-WIRE-ACCOUNTING")
        bad, positions = [], 0
        for proto, vid in (("rust-semantic", "frames-small-request"), ("typescript-semantic", "frames-ts2-small-request")):
            p = next(x for x in self.s.vectors["vectors"]["REQUEST-WIRE-ACCOUNTING"] if x["id"] == vid)["input"]["plan"]
            limits = self.limits(proto)
            req = REP.build_plan(p, self.fx, AR.prepared_entries)
            plan = (REP.plan_rust3_request if proto == "rust-semantic" else REP.plan_ts2_request)(doc, limits, req)
            frames = SR.realize(req, proto, limits)
            for k in range(len(frames) + 1):
                positions += 1
                want = SR.expected_cancel(plan, k)
                if k == 0:
                    if want is not None:
                        bad.append([proto, k, "echo before Hello"])
                    continue
                sent = [{"frame": f["frameType"], "payload": f["payload"]} for f in frames[:k]]
                if self.code_of(lambda: AR.cancel_nullability(sent, want)) is not None or self.code_of(lambda: SR.consume(plan, proto, acc, limits, frames[:k] + [SR.cancel_frame(k, want)])) is not None:
                    bad.append([proto, k, "planned echo refused"])
                for alt in (dict(want, executionId=None if want["executionId"] is not None else plan["cancelEcho"]["executionId"]),
                            dict(want, analysisOrdinal=None if want["analysisOrdinal"] is not None else plan["cancelEcho"]["analysisOrdinal"])):
                    if self.code_of(lambda: AR.cancel_nullability(sent, alt)) is None:
                        bad.append([proto, k, "alternative admitted by CANCEL-NULLABILITY"])
                    if self.code_of(lambda: SR.consume(plan, proto, acc, limits, frames[:k] + [SR.cancel_frame(k, alt)])) != "SENDER_DIVERGENCE:cancel-echo":
                        bad.append([proto, k, "alternative not refused by the sender"])
        self.add("sender-cancel-echo-matches-cancel-nullability", not bad and positions >= 16, {"positions": positions, "failures": bad[:6]})

    # ------------------------------------------------------------------ review-05 RF-1: content-bound slots and sent state
    def sender_state(self):
        doc, acc = self.wire, AR.params(self.wire, "REQUEST-WIRE-ACCOUNTING")
        vecs = {x["id"]: x for x in self.s.vectors["vectors"]["REQUEST-WIRE-ACCOUNTING"]}
        bound_bad, slots = [], 0
        for vid in ("frames-small-request", "frames-ts2-small-request", "seal-counts-multi-chunk", "prepared-manifest-entries-at-bound"):
            p = vecs[vid]["input"]["plan"]
            limits = self.limits(p["protocol"])
            req = REP.build_plan(p, self.fx, AR.prepared_entries)
            plan = (REP.plan_rust3_request if p["protocol"] == "rust-semantic" else REP.plan_ts2_request)(doc, limits, req)
            frames = SR.realize(req, p["protocol"], limits)
            last = {}
            for i, (slot, f) in enumerate(zip(plan["schedule"], frames)):
                slots += 1
                chunk = "chunkIndex" in slot
                realized = W.encoded_digest(f["payload"], SR.CHUNK_DIGEST_EXCLUDES if chunk else ())
                if not re.fullmatch(r"[0-9a-f]{64}", slot.get("payloadSha256") or "") or slot["payloadSha256"] != realized or (chunk and slot.get("payloadSha256Scope") != "payload-without-bytes"):
                    bound_bad.append([vid, i, slot["frameType"], "digest"])
                if not chunk and slot["payloadSha256"] != hashlib.sha256(W.encode(f["payload"])).hexdigest():
                    bound_bad.append([vid, i, slot["frameType"], "streamed digest differs from full encoding"])
                if chunk:
                    last[tuple(slot["entry"])] = slot
            bound_bad += [[vid, "last chunk without entryContentSha256", list(k)] for k, slot in last.items() if "entryContentSha256" not in slot]
        self.add("schedule-slots-content-bound", not bound_bad and slots >= 30, {"slotsChecked": slots, "failures": bound_bad[:6]})

        p = vecs["frames-small-request"]["input"]["plan"]
        limits = self.limits("rust-semantic")
        req = REP.build_plan(p, self.fx, AR.prepared_entries)
        plan = REP.plan_rust3_request(doc, limits, req)
        frames = SR.realize(req, "rust-semantic", limits)
        n, ou = len(frames), plan["cancelEcho"]["openUniverseSlot"]
        sm = next(i for i, f in enumerate(frames) if f["frameType"] == "SnapshotManifest")
        wrong = lambda v: v[:-1] + ("0" if v[-1] != "0" else "1")
        sub_ou = dict(frames[ou], payload=dict(frames[ou]["payload"], executionId=wrong(frames[ou]["payload"]["executionId"])))
        attacks = {}

        def run(name, transcript, offending, want, lim=limits):
            progress = {}
            code = self.code_of(lambda: SR.consume(plan, "rust-semantic", acc, lim, transcript, progress))
            attacks[name] = {"code": code, "expected": want, "framesSentAtRefusal": progress.get("framesSent", 0), "offendingFrameIndex": offending,
                             "sentCorrelation": progress.get("sentCorrelation"), "cancelled": progress.get("cancelled", False)}
            return code == want and progress.get("framesSent", 0) == offending and not progress.get("cancelled", False)
        ok = run("openuniverse-substituted-then-planned-echo", frames[:ou] + [sub_ou, SR.cancel_frame(ou + 1, SR.expected_cancel(plan, ou + 1))], ou, "SENDER_DIVERGENCE:payload-digest")
        ok = run("openuniverse-substituted-then-sent-echo", frames[:ou] + [sub_ou, SR.cancel_frame(ou + 1, dict(SR.expected_cancel(plan, ou + 1), executionId=sub_ou["payload"]["executionId"]))], ou,
                 "SENDER_DIVERGENCE:payload-digest") and ok
        ok = run("snapshot-manifest-digest-substituted", frames[:sm] + [dict(frames[sm], payload=dict(frames[sm]["payload"], manifestSha256="f" * 64))] + frames[sm + 1:], sm,
                 "SENDER_DIVERGENCE:payload-digest") and ok
        ok = run("cancel-analysis-ordinal-false", frames + [SR.cancel_frame(n, dict(SR.expected_cancel(plan, n), analysisOrdinal=False))], n, "SENDER_DIVERGENCE:cancel-echo") and ok
        ok = run("request-frames-limit-during-commit", frames, 5, "SENDER_DIVERGENCE:request-limit", dict(limits, maxRequestFrames=5)) and ok
        planned = {"executionId": plan["cancelEcho"]["executionId"], "analysisOrdinal": plan["cancelEcho"]["analysisOrdinal"]}
        ok = ok and attacks["cancel-analysis-ordinal-false"]["sentCorrelation"] == planned and attacks["openuniverse-substituted-then-planned-echo"]["sentCorrelation"] == {"executionId": None, "analysisOrdinal": None}
        self.add("sender-refusal-before-sent-state", ok, attacks)

        fake = {"executionId": "exec-sent-state", "analysisOrdinal": 5}
        mid, end = SR.expected_cancel(plan, ou + 1, fake), SR.expected_cancel(plan, n, fake)
        full = SR.consume(plan, "rust-semantic", acc, limits, frames + [SR.cancel_frame(n, SR.expected_cancel(plan, n))])
        derived = mid == {"executionId": "exec-sent-state", "analysisOrdinal": None, "reason": plan["cancelEcho"]["reason"]} and end["analysisOrdinal"] == 5
        self.add("sender-echo-derived-from-sent-state", derived and full["sentCorrelation"] == {"executionId": req["openUniverse"]["executionId"], "analysisOrdinal": req["analyze"]["analysisOrdinal"]},
                 {"echoFromGivenSentState": [mid, end], "consumedSentCorrelation": full["sentCorrelation"],
                  "equivalence": "consume derives the echo from the consumed correlation; while payloadSha256 binding holds, the consumed correlation equals the planned one, so a consume-level plan-echo mutant is equivalent and is not a control"})

        prior = json.loads((self.s.out / "prior/review-05/probe_05.out.json").read_text())["S_sender"]
        recorded = {k: prior[k] for k in ("ordinalFalseInsteadOf0", "openUniverseExecutionIdSubstitutedSameLength_thenPlannedEchoCancel", "snapshotManifestDigestSubstitutedSameLength")}
        was = all(v.startswith("accepted:") for v in recorded.values()) and prior["openUniverseExecutionIdSubstituted_thenEchoOfWhatWasSent"].startswith("refused:")
        now = {"ordinalFalseInsteadOf0": attacks["cancel-analysis-ordinal-false"]["code"],
               "openUniverseExecutionIdSubstitutedSameLength_thenPlannedEchoCancel": attacks["openuniverse-substituted-then-planned-echo"]["code"],
               "openUniverseExecutionIdSubstituted_thenEchoOfWhatWasSent": attacks["openuniverse-substituted-then-sent-echo"]["code"],
               "snapshotManifestDigestSubstitutedSameLength": attacks["snapshot-manifest-digest-substituted"]["code"]}
        wrong_prior = prior["openUniverseExecutionIdSubstitutedSameLength_thenPlannedEchoCancel"]
        self.add("review05-sender-attacks-replayed", was and prior["cancelEcho"] == plan["cancelEcho"] and all(c and c.startswith("SENDER_DIVERGENCE:") for c in now.values()),
                 {"candidate05Recorded": dict(recorded, openUniverseExecutionIdSubstituted_thenEchoOfWhatWasSent=prior["openUniverseExecutionIdSubstituted_thenEchoOfWhatWasSent"]),
                  "candidate06": now, "samePlanCancelEcho": prior["cancelEcho"] == plan["cancelEcho"], "note": wrong_prior[:40]})

    def fault_d9(self):
        NE = self.NE
        p = AR.params(self.wire, "RUST3-PROVIDER-FAULT")["d9Equivalence"]
        a, b = NE.stage_authority(p["ownerTerminalKind"]), NE.stage_authority(p["refusedPayloadTerminalKind"])
        owner_kind = NE.protocol3_run([{"frame": "Hello"}, {"frame": "ProviderFault"}])["terminalKind"]
        same = all(a[k] == b[k] for k in ("d9", "factsAdmitted", "coverageEntriesAdmitted", "runMayBeSealed", "authority"))
        self.add("provider-fault-refusal-same-d9", same and owner_kind == p["ownerTerminalKind"], {"ownerTerminal": owner_kind, "providerFault": a["d9"], "refusedPayload": b["d9"]})

    def run(self):
        for step in (self.ecma, self.vectors, self.routes, self.scope2, self.anchors, self.manifests, self.depsrc, self.prepared, self.transitions,
                     self.commitments, self.wire_examples, self.ecma_owner, self.review03_replay, self.newline, self.path_site_bindings,
                     self.owner_successor_behaviour, self.owner_scope, self.relation_payload, self.fact_plane_path,
                     self.reachability, self.accounting, self.schedule, self.sender_cancel_law, self.sender_state, self.relation_gap, self.fault_d9):
            try:
                step()
            except Exception as exc:  # noqa: BLE001
                self.add("step:" + step.__name__, False, type(exc).__name__ + ": " + str(exc)[:400])
        return self.results
