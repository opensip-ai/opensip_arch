"""Pre-spawn wire representability admission and the canonical host send plan (candidate 05). Reference scaffolding,
not production admission and not the M3 sender.

Successor selectors (the owner models passed in MUST carry the owner pattern-evaluation successor, tools/owner_successor.py):
  dependency_source_set_admit_successor - phase A (before the owner): a file path of a package the owner will hash that
      fails the owner path schema is a routed refusal (the owner cannot mint its file-manifest identity; before the
      successor it raised an untyped exception). Phase B (after the owner admits; owner DS refusals keep precedence):
      NFC, name/version scalars, key length and canonical-path narrowing.
  prepared_output_set_admit_successor - phase A (before the owner, mode-independent): an ExpansionSiteV1.path or
      GeneratedFileV1.logicalPath failing its owner path schema is a routed refusal; it outranks the owner non-inert and
      stale refusals. Phase B (every non-rejected owner outcome: admitted, or the defaulted partial-stale fallback; owner
      rejections keep precedence): the rows the manifest carries - every row of the set - over the row or blob-byte bound
      refuse when prepared mode was selected explicitly and are not selected (zero usable rows, disclosure, non-prepared
      fallback) when it was defaulted - the owner PO-1 mode law. The owner's usable rows are a subset of the carried rows
      (prepared_limit_basis checks the owner partition), so the carried bound implies the usable-row bound.
  plan_rust3_request / plan_ts2_request - the Plan-time planner, producing the immutable canonical send plan.

Byte law (rust2 framing + limitPolicy.aggregateAccounting): every frame is its exact deterministic-CBOR envelope payload;
the 40-byte prefix is excluded; request totals sum envelope payload bytes. Chunk bytes are never materialized. The
canonical schedule is greedy (frame-minimal, NOT byte-minimal); a refusal means "does not fit under the canonical host
send schedule", never "no lawful encoding exists". Codec-level refusal of malicious worker frames is M2 and not claimed.
"""
import json
import unicodedata

import owner_successor as OS
import wirecodec as W

DEP_KEY = "native.dependency-source-not-wire-representable"
PREP_PATH_KEY = "native.prepared-output-not-wire-representable"
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


def owner_schema_ok(NE, pointer, value):
    """Evaluate one value against an owner schema node with the owner validator (successor installed)."""
    try:
        NE.C.validate(dict(NE.SCHEMAS, **{"$ref": pointer}), value)
        return True
    except Exception:  # noqa: BLE001 - jsonschema ValidationError from the owner validator
        return False


# ------------------------------------------------------------------ dependency sources (set admission)
def owner_hashed_rows(NE, lock_text, provided, activated):
    """The provided rows whose files the owner will pass to file_manifest_identity: activated, present in the lock,
    not path-kind (owner _source_kind), provided. Mirrors the owner selection without re-deciding any DS rule."""
    lock = NE.parse_cargo_lock(lock_text)
    by_key = {f'{p["name"]} {p["version"]} {p["source"]}': p for p in lock["packages"]}
    provided_by_key = {f'{r["name"]} {r["version"]} {r["sourceId"]}': r for r in provided}
    out = []
    for key in sorted(activated):
        lock_pkg, row = by_key.get(key), provided_by_key.get(key)
        if lock_pkg is None or row is None:
            continue
        try:
            if NE._source_kind(lock_pkg["source"]) == "path":
                continue
        except NE.AdmissionError:
            continue
        out.append((key, row))
    return out


def dependency_representability_faults(doc, packages, files_by_key):
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
    OS.require_installed(NE)
    rep = params(doc, "DEPSRC-WIRE-REPRESENTABILITY")
    phase_a = []
    for key, row in owner_hashed_rows(NE, lock_text, provided, activated):
        for path in sorted(row["files"], key=lambda p: p.encode("utf-8", "surrogatepass")):
            if not owner_schema_ok(NE, rep["ownerPathSchema"], path):
                phase_a.append(_fault("path-owner-schema", path))
    if phase_a:
        return {"admitted": False, "identity": None, "refusals": [], "ownerRan": False, "successorRefusal": _refusal(doc, "DEPSRC-WIRE-REPRESENTABILITY", phase_a)}
    out = NE.dependency_source_set_admit(lock_text, provided, activated)
    if not out["admitted"]:
        return dict(out, ownerRan=True, successorRefusal=None)
    files_by_key = {f'{r["name"]} {r["version"]} {r["sourceId"]}': r["files"] for r in provided}
    faults = dependency_representability_faults(doc, out["descriptor"]["packages"], files_by_key)
    if not faults:
        return dict(out, ownerRan=True, successorRefusal=None)
    return dict(out, ownerRan=True, admitted=False, identity=None, successorRefusal=_refusal(doc, "DEPSRC-WIRE-REPRESENTABILITY", faults))


# ------------------------------------------------------------------ prepared outputs (set admission)
def prepared_path_faults(NE, doc, prepared):
    p = params(doc, "PREPARED-V3-PATH-REPRESENTABILITY")
    faults = []
    for i, row in enumerate(prepared.get("rows", [])):
        site, gen = row.get("site"), row.get("generated")
        if isinstance(site, dict) and isinstance(site.get("path"), str) and not owner_schema_ok(NE, p["siteSchema"], site["path"]):
            faults.append(_fault("site-path-owner-schema", "rows[%d]" % i))
        if isinstance(gen, dict) and isinstance(gen.get("logicalPath"), str) and not owner_schema_ok(NE, p["generatedSchema"], gen["logicalPath"]):
            faults.append(_fault("generated-logical-path-owner-schema", "rows[%d]" % i))
    return faults


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


def prepared_limit_basis(prepared, owner_out):
    """review-04 RF-1: the rows the Plan-bound PreparedOutputManifest carries (every row of the set: PREPARED-V3-ENTRY,
    PREPARED-V3-SET-JOIN) and the owner partition of them into usable, stale and failed rows. The partition check is
    defensive: the pinned owner assigns every non-refused row to exactly one of the three."""
    rows = prepared["rows"]
    basis = {"carriedRows": len(rows), "carriedBlobBytes": sum(r["blob"]["byteLength"] for r in rows),
             "ownerUsableRows": len(owner_out.get("usableRows", [])), "ownerStaleRows": len(owner_out.get("staleRows", [])),
             "ownerFailedRows": len(owner_out.get("failedRows", []))}
    if basis["ownerUsableRows"] + basis["ownerStaleRows"] + basis["ownerFailedRows"] != basis["carriedRows"]:
        raise W.Refuse("PREPARED_ROW_PARTITION", json.dumps(basis))
    return basis


def prepared_output_set_admit_successor(NE, doc, prepared, context, explicit_prepared_mode):
    OS.require_installed(NE)
    phase_a = prepared_path_faults(NE, doc, prepared)
    if phase_a:
        return {"outcome": "rejected", "ownerRan": False, "d9": None, "usableRows": [], "successorRefusal": _refusal(doc, "PREPARED-V3-PATH-REPRESENTABILITY", phase_a)}
    out = NE.prepared_output_set_admit(prepared, context, explicit_prepared_mode)
    # review-04 RF-1: the wire limit is judged over EVERY row of the Plan-bound set for EVERY non-rejected owner outcome
    # (admitted, and the defaulted partial-stale fallback-non-prepared), because PREPARED-V3-ENTRY and
    # PREPARED-V3-SET-JOIN make the manifest answer every row of the set; owner rejections keep precedence.
    if out["outcome"] not in ("admitted", "fallback-non-prepared"):
        return dict(out, ownerRan=True, successorRefusal=None)
    basis = prepared_limit_basis(prepared, out)
    faults = prepared_limit_faults(doc, prepared)
    if not faults:
        return dict(out, ownerRan=True, successorRefusal=None, wireLimitBasis=basis)
    action = params(doc, "PREPARED-V3-WIRE-LIMIT")["modes"]["explicit" if explicit_prepared_mode else "defaulted"]
    if action == "refuse":
        return dict(out, ownerRan=True, outcome="rejected", usableRows=[], successorRefusal=_refusal(doc, "PREPARED-V3-WIRE-LIMIT", faults), wireLimitBasis=basis)
    if action == "fallback-non-prepared-with-disclosure":
        return dict(out, ownerRan=True, ownerOutcome=out["outcome"], outcome="fallback-non-prepared", usableRows=[], successorRefusal=None, preparedOutputSetSelected=False,
                    ownerDisclosure=out.get("disclosure"), disclosure="prepared output set exceeds the provider wire limits; not selected, owners analyzed non-prepared",
                    wireLimitDisclosure=faults, wireLimitBasis=basis)
    raise W.Refuse("UNKNOWN_PREPARED_MODE_ACTION", action)


# ------------------------------------------------------------------ Plan-time canonical send plan
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
        self.frame_faults, self.entry_faults, self.largest, self.schedule, self.seals = [], [], {}, [], {}
        self.cancel_reserve, self.cancel_payload = None, None
        self.memo, self.base_cache = {}, {}

    def frame(self, frame_type, payload, extra=None):
        n = W.encoded_length(self.wrap(self.seq, frame_type, payload), self.memo) + self.prefix
        self._count(frame_type, n, extra)

    def entry_bound(self, manifest_type, count, limits):
        """review-04 RF-1 defence in depth: a manifest whose entry count exceeds its declared entry bound refuses."""
        name = self.p["entryBounds"].get(manifest_type)
        if name is not None and name in limits and count > int(limits[name]):
            self.entry_faults.append(_fault("entries:" + manifest_type, "%d>%s" % (count, limits[name])))

    def reserve_cancel(self, payload):
        self.cancel_payload = dict(payload)
        n = W.encoded_length(self.wrap(self.seq, "Cancel", payload)) + self.prefix
        self.cancel_reserve = {"frameType": "Cancel", "payloadBytes": n, "maxCount": 1, "sequence": "the next sequence number at the moment of interrupt"}
        self._count("Cancel", n, None, record=False)

    def chunk_sizes(self, frame_type, base_payload, length, max_chunk, cache_key):
        """Closed-form sizes of the greedy chunk frames of one entry: (size, chunkIndex, byteOffset, byteLength)."""
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
            out.append((base + (hl(self.seq + i) if self.enveloped else 0) + hl(i) + hl(i * max_chunk) + hl(n) + n + self.prefix, i, i * max_chunk, n))
        return out

    def chunks(self, frame_type, base_payload, length, max_chunk, entry):
        for size, i, offset, n in self.chunk_sizes(frame_type, base_payload, length, max_chunk, tuple(entry)):
            self._count(frame_type, size, {"entry": list(entry), "chunkIndex": i, "byteOffset": offset, "byteLength": n})

    def _count(self, frame_type, n, extra, record=True):
        if n > self.largest.get(frame_type, -1):
            self.largest[frame_type] = n
        if n > self.frame_limit and len(self.frame_faults) < 8:
            self.frame_faults.append(_fault("frame:" + frame_type, f"seq{self.seq}:{n}>{self.frame_limit}"))
        if record:
            slot = {"sequence": self.seq, "frameType": frame_type, "payloadBytes": n}
            if extra:
                slot.update(extra)
            self.schedule.append(slot)
        self.total += n
        self.seq += 1

    def result(self, doc):
        faults = list(self.entry_faults) + list(self.frame_faults)
        if self.total_limit is not None and self.total > self.total_limit:
            faults.append(_fault("request-bytes", f"{self.total}>{self.total_limit}"))
        if self.frames_limit is not None and self.seq > self.frames_limit:
            faults.append(_fault("request-frames", f"{self.seq}>{self.frames_limit}"))
        slots = {s["frameType"]: i for i, s in reversed(list(enumerate(self.schedule))) if s["frameType"] in ("Hello", "OpenUniverse", "Analyze")}
        echo = None
        if self.cancel_reserve is not None and self.cancel_payload is not None:
            echo = dict(self.cancel_payload, helloSlot=slots["Hello"], openUniverseSlot=slots["OpenUniverse"], analyzeSlot=slots["Analyze"])
        return {"schedule": self.schedule, "cancelReserve": self.cancel_reserve, "cancelEcho": echo, "seals": self.seals,
                "frames": self.seq, "payloadBytes": self.total, "largestFrame": self.largest, "faults": faults,
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


def _custody(acc, manifest_type, chunk_type, seal_type, manifest, id_field, total_field, max_chunk, base_of, length_of, entry_of, limits):
    acc.entry_bound(manifest_type, len(manifest["entries"]), limits)
    acc.frame(manifest_type, manifest)
    for e in manifest["entries"]:
        acc.chunks(chunk_type, base_of(e), length_of(e), max_chunk, entry_of(e))
    seal = seal_payload(manifest, id_field, total_field, max_chunk, length_of)
    acc.seals[seal_type] = seal
    acc.frame(seal_type, seal, {"totalChunkCount": seal["totalChunkCount"]})


def plan_rust3_request(doc, limits, req):
    """Canonical send plan for major 3: P3 host order (P3-01..P3-22) plus one reserved maximal Cancel (P3-29)."""
    total_limit, frames_limit = _totals(doc, "rust-semantic", limits)
    acc = Accountant(doc, rust3_envelope, int(limits["maxFramePayloadBytes"]), total_limit, frames_limit)
    acc.frame("Hello", req["hello"])
    acc.frame("OpenUniverse", req["openUniverse"])
    sm = req["snapshotManifest"]
    _custody(acc, "SnapshotManifest", "SnapshotFileChunk", "SnapshotSeal", sm, "snapshotId", "totalFileBytes", int(limits["maxSnapshotChunkBytes"]),
             lambda e: {"snapshotId": sm["snapshotId"], "path": e["path"]}, FILE_LEN, lambda e: [e["path"]], limits)
    dm = req["dependencyManifest"]
    _custody(acc, "DependencySourceManifest", "DependencySourceChunk", "DependencySourceSeal", dm, "dependencySourceSetId", "totalBytes",
             int(limits["maxDependencySourceChunkBytes"]),
             lambda e: {"dependencySourceSetId": dm["dependencySourceSetId"], "packageKey": e["packageKey"], "path": e["path"]},
             lambda e: e["byteLength"], lambda e: [e["packageKey"], e["path"]], limits)
    pm = req.get("preparedManifest")
    if pm is not None:
        _custody(acc, "PreparedOutputManifest", "PreparedOutputChunk", "PreparedOutputSeal", pm, "planId", "totalBlobBytes", int(limits["maxPreparedOutputChunkBytes"]),
                 lambda e: {"planId": pm["planId"], "outputOrdinal": e["outputOrdinal"]}, lambda e: e["blobByteLength"], lambda e: [e["outputOrdinal"]], limits)
    acc.frame("Analyze", req["analyze"])
    if acc.p["reserveCancel"]:
        acc.reserve_cancel(cancel_payload(req))
    return acc.result(doc)


def plan_ts2_request(doc, limits, req):
    """Canonical send plan for major 2 (no request totals declared; the frame bound applies to every planned frame)."""
    total_limit, frames_limit = _totals(doc, "typescript-semantic", limits)
    acc = Accountant(doc, ts2_envelope, int(limits["maxFramePayloadBytes"]), total_limit, frames_limit)
    acc.frame("Hello", req["hello"])
    acc.frame("OpenUniverse", req["openUniverse"])
    sm = req["snapshotManifest"]
    _custody(acc, "SnapshotManifest", "SnapshotFileChunk", "SnapshotSeal", sm, "snapshotId", "totalFileBytes", int(limits["maxSnapshotChunkBytes"]),
             lambda e: {"snapshotId": sm["snapshotId"], "path": e["path"]}, FILE_LEN, lambda e: [e["path"]], limits)
    acc.frame("Analyze", req["analyze"])
    if acc.p["reserveCancel"]:
        acc.reserve_cancel(cancel_payload(req))
    return acc.result(doc)


def build_plan(plan, fx, prepared_entries_fn):
    """Build a planner request from a compact vector description: groups of n identical-length entries share one entry
    object, so hundreds of thousands of entries and gigabytes of chunk bytes are accounted without materialization.
    Hello/OpenUniverse are owner fixtures; the Analyze payload is an explicit minimal stub whose bytes count like any frame."""
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
    """Upper bound on canonical-schedule host-to-worker frames for any input the other admissions accept."""
    frame = int(limits["maxFramePayloadBytes"])
    dep_entries = min(int(limits["maxDependencySourceEntries"]), (frame - manifest_overhead) // minimal_dep_entry_len)
    snap_entries = min(int(limits["maxSnapshotEntries"]), (frame - manifest_overhead) // minimal_snapshot_entry_len)
    snap_chunks = snap_entries + int(limits["maxSnapshotTotalFileBytes"]) // int(limits["maxSnapshotChunkBytes"])
    dep_chunks = dep_entries + int(limits["maxDependencySourceTotalBytes"]) // int(limits["maxDependencySourceChunkBytes"])
    prep_chunks = int(limits["maxPreparedOutputEntries"]) + int(limits["maxPreparedOutputTotalBlobBytes"]) // int(limits["maxPreparedOutputChunkBytes"])
    fixed = 10  # Hello, OpenUniverse, 3 manifests, 3 seals, Analyze, reserved Cancel
    return {"bound": fixed + snap_chunks + dep_chunks + prep_chunks, "dependencyEntries": dep_entries, "snapshotEntries": snap_entries,
            "snapshotChunks": snap_chunks, "dependencyChunks": dep_chunks, "preparedChunks": prep_chunks, "fixedFrames": fixed}
