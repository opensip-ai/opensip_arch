"""Pre-spawn wire representability admission (candidate 03, RF-2). Reference scaffolding, not production admission.

Three successor selectors, each running AFTER its owner so owner refusals keep precedence:
  dependency_source_set_admit_successor  - wraps native_evidence_model.v2 dependency_source_set_admit (before PlanId)
  prepared_output_set_admit_successor    - wraps native_evidence_model.v2 prepared_output_set_admit (before Plan construction)
  plan_rust3_request / plan_ts2_request  - Plan-time pre-spawn planner over the exact host-to-worker frame sequence

Byte law (rust2 framing + limitPolicy.aggregateAccounting), read from REQUEST-WIRE-ACCOUNTING params: the frame limit
bounds the deterministic-CBOR ENVELOPE payload (lengthScope 'payload bytes only'; the payload is the whole envelope map);
request totals sum exact envelope payload bytes and EXCLUDE each 40-byte transport prefix. Chunk bytes are never
materialized: chunk frames are measured in closed form over wirecodec.encoded_length with ByteLen; check.py validates the
closed form against the owner wire-model encoder. Nothing is normalized, truncated or re-chunked to fit: a violation
refuses. Codec-level refusal of a malicious worker's frames is a separate (M2) obligation and is not claimed here.
"""
import unicodedata

import wirecodec as W

DEP_KEY = "native.dependency-source-not-wire-representable"
PREP_KEY = "native.prepared-output-exceeds-wire-limit"
REQ_KEY = "native.provider-request-exceeds-wire-limit"


def params(doc, rule_id):
    return next(r for r in doc["admission"] if r["id"] == rule_id).get("params", {})


def _nfc(s):
    return unicodedata.normalize("NFC", s) == s


def _fault(kind, subject):
    return {"kind": kind, "subject": subject}


def _refusal(doc, rule_id, faults):
    key = params(doc, rule_id)["route"]["routeKey"]
    return {"key": key, "raw": key + ":" + faults[0]["kind"], "faults": faults}


# ------------------------------------------------------------------ dependency sources (set admission)
def dependency_representability_faults(doc, packages, files_by_key):
    """packages: owner-admitted DependencyPackageSourceV1 rows; files_by_key: constructed key -> {path: {...}}.
    Faults in deterministic order (owner package order, then UTF-8 path order)."""
    kp = params(doc, "DEPSRC-SET-KEY-CONSTRAINTS")
    rep = params(doc, "DEPSRC-WIRE-REPRESENTABILITY")
    lex = doc["privateRepresentation"]["lexicalRules"]
    flags = doc["privateRepresentation"]["patternDialect"]["flags"]
    sep = lex["package-key"]["separator"]
    limit = int(kp["forbidInNameVersionAtOrBelow"])
    faults = []
    for row in packages:
        key = row["name"] + sep + row["version"] + sep + row["sourceId"]
        if any(ord(c) <= limit for c in row["name"] + row["version"]):
            faults.append(_fault(f"name-or-version-scalar-at-or-below-{limit}", key))
        if len(key) > int(kp["maxKeyScalars"]):
            faults.append(_fault(f"package-key-over-{kp['maxKeyScalars']}-scalars", str(len(key))))
        for field in rep["nfcFields"]:
            if not _nfc(row[field]):
                faults.append(_fault(f"non-nfc-{field}", key))
        for path in sorted(files_by_key.get(key, {}), key=lambda p: p.encode("utf-8", "surrogatepass")):
            if not _nfc(path):
                faults.append(_fault("non-nfc-path", path))
            elif len(path) > int(rep["maxPathScalars"]):
                faults.append(_fault(f"path-over-{rep['maxPathScalars']}-scalars", key))
            else:
                try:
                    W.lexical(lex, rep["pathLexical"], path, flags)
                except W.Refuse:
                    faults.append(_fault("path-lexical", path))
    return faults


def dependency_source_set_admit_successor(NE, doc, lock_text, provided, activated):
    out = NE.dependency_source_set_admit(lock_text, provided, activated)
    if not out["admitted"]:
        return dict(out, successorRefusal=None)
    files_by_key = {f'{r["name"]} {r["version"]} {r["sourceId"]}': r["files"] for r in provided}
    faults = dependency_representability_faults(doc, out["descriptor"]["packages"], files_by_key)
    if not faults:
        return dict(out, successorRefusal=None)
    return dict(out, admitted=False, identity=None, successorRefusal=_refusal(doc, "DEPSRC-WIRE-REPRESENTABILITY", faults))


# ------------------------------------------------------------------ prepared outputs (set admission)
def prepared_limit_faults(doc, prepared):
    p = params(doc, "PREPARED-V3-WIRE-LIMIT")
    rows = prepared["rows"]
    if p["countScope"] == "all-inert-rows":
        counted = len(rows)
    elif p["countScope"] == "build-script-directives-only":
        counted = sum(1 for r in rows if r["kind"] == "build-script-directives")
    else:
        raise W.Refuse("UNKNOWN_COUNT_SCOPE")
    faults = []
    if counted > int(p["maxEntries"]):
        faults.append(_fault("entries", f"{counted}>{p['maxEntries']}"))
    blob = sum(r["blob"]["byteLength"] for r in rows)
    if blob > int(p["maxTotalBlobBytes"]):
        faults.append(_fault("blob-bytes", f"{blob}>{p['maxTotalBlobBytes']}"))
    return faults


def prepared_output_set_admit_successor(NE, doc, prepared, context, explicit_prepared_mode):
    out = NE.prepared_output_set_admit(prepared, context, explicit_prepared_mode)
    if out["outcome"] != "admitted":
        return dict(out, successorRefusal=None)
    faults = prepared_limit_faults(doc, prepared)
    if not faults:
        return dict(out, successorRefusal=None)
    return dict(out, outcome="rejected", successorRefusal=_refusal(doc, "PREPARED-V3-WIRE-LIMIT", faults))


# ------------------------------------------------------------------ Plan-time request accounting
def rust3_envelope(seq, frame_type, payload):
    return {"protocolMajor": 3, "direction": "host-to-worker", "sequence": seq, "frameType": frame_type, "payload": payload}


def ts2_envelope(seq, frame_type, payload):
    return {"protocolMajor": 2, "frameType": frame_type, "sequence": seq, "payload": payload}


class Accountant:
    def __init__(self, doc, envelope, frame_limit, total_limit=None, frames_limit=None):
        p = params(doc, "REQUEST-WIRE-ACCOUNTING")
        if p["chunking"] != "greedy-max-chunk":
            raise W.Refuse("UNKNOWN_CHUNKING")
        if p["lengthScope"] not in ("envelope-payload", "inner-payload"):
            raise W.Refuse("UNKNOWN_LENGTH_SCOPE")
        self.p = p
        self.enveloped = p["lengthScope"] == "envelope-payload"
        self.wrap = envelope if self.enveloped else (lambda seq, ft, payload: payload)
        self.prefix = int(p["prefixBytes"]) if p["prefixIncluded"] else 0
        self.frame_limit, self.total_limit, self.frames_limit = frame_limit, total_limit, frames_limit
        self.seq, self.total = 0, 0
        self.frame_faults, self.largest = [], {}
        self.memo, self.base_cache = {}, {}

    def frame(self, frame_type, payload):
        self._count(frame_type, W.encoded_length(self.wrap(self.seq, frame_type, payload), self.memo) + self.prefix)

    def chunk_sizes(self, frame_type, base_payload, length, max_chunk, cache_key):
        """Closed-form sizes of the greedy chunk frames of one entry, starting at the current sequence number."""
        if length == 0:
            return []
        bk = (frame_type, cache_key)
        if bk not in self.base_cache:
            probe = self.wrap(0, frame_type, dict(base_payload, chunkIndex=0, byteOffset=0, bytes=W.ByteLen(0)))
            # probe heads: sequence (enveloped only), chunkIndex, byteOffset and the empty byte string are 1 byte each
            self.base_cache[bk] = W.encoded_length(probe) - (4 if self.enveloped else 3)
        base, hl = self.base_cache[bk], W._head_len
        k = -(-length // max_chunk)
        out = []
        for i in range(k):
            n = max_chunk if i < k - 1 else length - (k - 1) * max_chunk
            out.append(base + (hl(self.seq + i) if self.enveloped else 0) + hl(i) + hl(i * max_chunk) + hl(n) + n + self.prefix)
        return out

    def chunks(self, frame_type, base_payload, length, max_chunk, cache_key):
        """Greedy chunking: every chunk carries max_chunk bytes except the last; a zero-length entry has no chunk."""
        for n in self.chunk_sizes(frame_type, base_payload, length, max_chunk, cache_key):
            self._count(frame_type, n)

    def _count(self, frame_type, n):
        if n > self.largest.get(frame_type, -1):
            self.largest[frame_type] = n
        if n > self.frame_limit and len(self.frame_faults) < 8:
            self.frame_faults.append(_fault("frame:" + frame_type, f"seq{self.seq}:{n}>{self.frame_limit}"))
        self.total += n
        self.seq += 1

    def result(self, doc):
        faults = list(self.frame_faults)
        if self.total_limit is not None and self.total > self.total_limit:
            faults.append(_fault("request-bytes", f"{self.total}>{self.total_limit}"))
        if self.frames_limit is not None and self.seq > self.frames_limit:
            faults.append(_fault("request-frames", f"{self.seq}>{self.frames_limit}"))
        return {"frames": self.seq, "payloadBytes": self.total, "largestFrame": self.largest, "faults": faults,
                "refusal": _refusal(doc, "REQUEST-WIRE-ACCOUNTING", faults) if faults else None}


def seal_payload(manifest, id_field, total_field, max_chunk, entry_len):
    entries = manifest["entries"]
    total = sum(entry_len(e) for e in entries)
    chunks = sum(-(-entry_len(e) // max_chunk) for e in entries)
    return {id_field: manifest[id_field], "manifestSha256": manifest["manifestSha256"], "entryCount": len(entries),
            total_field: total, "totalChunkCount": chunks}


def cancel_payload(req):
    return {"executionId": req["openUniverse"]["executionId"], "analysisOrdinal": req["analyze"]["analysisOrdinal"], "reason": "user-interrupt"}


def _totals(doc, protocol, limits):
    if protocol not in params(doc, "REQUEST-WIRE-ACCOUNTING")["totalsApplyTo"]:
        return None, None
    if "maxRequestPayloadBytesTotal" not in limits or "maxRequestFrames" not in limits:
        raise W.Refuse("NO_REQUEST_TOTAL_LIMITS_DECLARED")
    return int(limits["maxRequestPayloadBytesTotal"]), int(limits["maxRequestFrames"])


FILE_LEN = lambda e: e["byteLength"] if e["kind"] == "file" else 0


def plan_rust3_request(doc, limits, req):
    """req: {hello, openUniverse, snapshotManifest, dependencyManifest, preparedManifest|None, analyze}. Order is the P3
    host order (P3-01..P3-22) plus one reserved Cancel echoing the execution and analysis (P3-29)."""
    total_limit, frames_limit = _totals(doc, "rust-semantic", limits)
    acc = Accountant(doc, rust3_envelope, int(limits["maxFramePayloadBytes"]), total_limit, frames_limit)
    acc.frame("Hello", req["hello"])
    acc.frame("OpenUniverse", req["openUniverse"])
    sm = req["snapshotManifest"]
    acc.frame("SnapshotManifest", sm)
    for e in sm["entries"]:
        acc.chunks("SnapshotFileChunk", {"snapshotId": sm["snapshotId"], "path": e["path"]}, FILE_LEN(e), int(limits["maxSnapshotChunkBytes"]), (e["path"],))
    acc.frame("SnapshotSeal", seal_payload(sm, "snapshotId", "totalFileBytes", int(limits["maxSnapshotChunkBytes"]), FILE_LEN))
    dm = req["dependencyManifest"]
    acc.frame("DependencySourceManifest", dm)
    for e in dm["entries"]:
        acc.chunks("DependencySourceChunk", {"dependencySourceSetId": dm["dependencySourceSetId"], "packageKey": e["packageKey"], "path": e["path"]},
                   e["byteLength"], int(limits["maxDependencySourceChunkBytes"]), (e["packageKey"], e["path"]))
    acc.frame("DependencySourceSeal", seal_payload(dm, "dependencySourceSetId", "totalBytes", int(limits["maxDependencySourceChunkBytes"]), lambda e: e["byteLength"]))
    pm = req.get("preparedManifest")
    if pm is not None:
        acc.frame("PreparedOutputManifest", pm)
        for e in pm["entries"]:
            acc.chunks("PreparedOutputChunk", {"planId": pm["planId"], "outputOrdinal": e["outputOrdinal"]}, e["blobByteLength"],
                       int(limits["maxPreparedOutputChunkBytes"]), (e["outputOrdinal"],))
        acc.frame("PreparedOutputSeal", seal_payload(pm, "planId", "totalBlobBytes", int(limits["maxPreparedOutputChunkBytes"]), lambda e: e["blobByteLength"]))
    acc.frame("Analyze", req["analyze"])
    if acc.p["reserveCancel"]:
        acc.frame("Cancel", cancel_payload(req))
    return acc.result(doc)


def plan_ts2_request(doc, limits, req):
    """TypeScript major 2 declares no request totals; the per-frame maxFramePayloadBytes applies to every planned frame."""
    total_limit, frames_limit = _totals(doc, "typescript-semantic", limits)
    acc = Accountant(doc, ts2_envelope, int(limits["maxFramePayloadBytes"]), total_limit, frames_limit)
    acc.frame("Hello", req["hello"])
    acc.frame("OpenUniverse", req["openUniverse"])
    sm = req["snapshotManifest"]
    acc.frame("SnapshotManifest", sm)
    for e in sm["entries"]:
        acc.chunks("SnapshotFileChunk", {"snapshotId": sm["snapshotId"], "path": e["path"]}, FILE_LEN(e), int(limits["maxSnapshotChunkBytes"]), (e["path"],))
    acc.frame("SnapshotSeal", seal_payload(sm, "snapshotId", "totalFileBytes", int(limits["maxSnapshotChunkBytes"]), FILE_LEN))
    acc.frame("Analyze", req["analyze"])
    if acc.p["reserveCancel"]:
        acc.frame("Cancel", cancel_payload(req))
    return acc.result(doc)


def build_plan(plan, fx, prepared_entries_fn):
    """Build a planner request from a compact vector description: groups of n identical-length entries share one entry
    object (distinct fixed-width paths have identical encoded lengths), so hundreds of thousands of entries and
    gigabytes of chunk bytes are accounted without materialization. Hello/OpenUniverse are owner fixtures; the Analyze
    payload is an explicit minimal stub whose bytes count like any frame."""
    rust = plan["protocol"] == "rust-semantic"
    prepared = plan.get("prepared")
    if rust:
        hello, ou = fx["wireRustHello"], fx["startupRustOpenUniversePrepared" if prepared else "startupRustOpenUniverse"]
    else:
        hello, ou = fx["wireTsHello"], fx["startupTsOpenUniverse"]
    snap = []
    for g in plan["snapshot"]:
        e = {"path": "s" * g["pathScalars"], "kind": "file", "byteLength": g["byteLength"], "contentSha256": "1" * 64}
        e.update({"executable": False, "targetBytes": None} if rust else {"linkTarget": None})
        snap.extend([e] * g["n"])
    req = {"hello": hello, "openUniverse": ou, "snapshotManifest": {"snapshotId": ou["snapshotId"], "manifestSha256": "0" * 64, "entries": snap}}
    if rust:
        dep = []
        for g in plan["dependency"]:
            e = {"packageKey": g["packageKey"], "path": "d" * g["pathScalars"], "byteLength": g["byteLength"], "contentSha256": "1" * 64}
            dep.extend([e] * g["n"])
        req["dependencyManifest"] = {"dependencySourceSetId": ou["repositoryResolution"]["dependencySourceSetId"], "manifestSha256": "0" * 64, "entries": dep}
        req["preparedManifest"] = None
        if prepared:
            base = fx["prepInert"]["rows"][0]
            config = ["c%0255d" % i for i in range(prepared["configurationCount"])]
            rows = [dict(base, site=dict(base["site"], startByte=i, endByte=i + 1), configuration=config,
                         blob=dict(base["blob"], byteLength=prepared["blobByteLength"])) for i in range(prepared["n"])]
            req["preparedManifest"] = {"planId": ou["planId"], "manifestSha256": "0" * 64, "entries": prepared_entries_fn(rows)}
        req["analyze"] = {"analysisOrdinal": 0, "executionId": ou["executionId"], "snapshotId": ou["snapshotId"], "planId": ou["planId"], "stages": []}
    else:
        req["analyze"] = {"analysisOrdinal": 0, "executionId": ou["executionId"], "snapshotId": ou["snapshotId"], "planId": ou["planId"], "stageRequests": []}
    return req


def plan(doc, limits, plan_desc, fx, prepared_entries_fn):
    req = build_plan(plan_desc, fx, prepared_entries_fn)
    fn = plan_rust3_request if plan_desc["protocol"] == "rust-semantic" else plan_ts2_request
    return fn(doc, limits, req)


def rust3_frames_upper_bound(limits, minimal_dep_entry_len, minimal_snapshot_entry_len, manifest_overhead):
    """Upper bound on planned host-to-worker frames for any input the other admissions accept: an entry of length L
    needs ceil(L / chunk) <= 1 + floor(L / chunk) chunks, entry counts are capped by both the entry limits and the single
    manifest frame, and totals are capped by the total-bytes limits."""
    frame = int(limits["maxFramePayloadBytes"])
    dep_entries = min(int(limits["maxDependencySourceEntries"]), (frame - manifest_overhead) // minimal_dep_entry_len)
    snap_entries = min(int(limits["maxSnapshotEntries"]), (frame - manifest_overhead) // minimal_snapshot_entry_len)
    snap_chunks = snap_entries + int(limits["maxSnapshotTotalFileBytes"]) // int(limits["maxSnapshotChunkBytes"])
    dep_chunks = dep_entries + int(limits["maxDependencySourceTotalBytes"]) // int(limits["maxDependencySourceChunkBytes"])
    prep_chunks = int(limits["maxPreparedOutputEntries"]) + int(limits["maxPreparedOutputTotalBlobBytes"]) // int(limits["maxPreparedOutputChunkBytes"])
    fixed = 10  # Hello, OpenUniverse, 3 manifests, 3 seals, Analyze, reserved Cancel
    return {"bound": fixed + snap_chunks + dep_chunks + prep_chunks, "dependencyEntries": dep_entries, "snapshotEntries": snap_entries,
            "snapshotChunks": snap_chunks, "dependencyChunks": dep_chunks, "preparedChunks": prep_chunks, "fixedFrames": fixed}
