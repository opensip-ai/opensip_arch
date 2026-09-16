"""Reference implementations of handwritten admission rules, parameterized by wire-carriers.v1.json rule `params`.

Test scaffolding for the AUTHOR candidate: vectors in admission-vectors.json execute these functions so that a changed
parameter or state-machine datum changes behaviour. NOT production admission and not a production wire decoder.
"""
import copy
import hashlib

import wirecodec as W

Refuse = W.Refuse


def params(doc, rule_id):
    return next(r for r in doc["admission"] if r["id"] == rule_id).get("params", {})


def C(domain, value):
    return "sha256:" + hashlib.sha256(domain.encode() + b"\x00" + W.encode(value)).hexdigest()


def raw_hex(value):
    return hashlib.sha256(W.encode(value)).hexdigest()


# ------------------------------------------------------------------ lexical
def path_admission(doc, rule_id, path):
    W.lexical(params(doc, rule_id)["lexical"], path, rule_id)


# ------------------------------------------------------------------ PER-KEY-SCOPE2
def per_key_scope2(doc, identity_fn, descriptor, key_commitment):
    p = params(doc, "PER-KEY-SCOPE2")
    d = {m: descriptor[m] for m in p["descriptorMembers"]}
    want = p["textPrefix"] + identity_fn(p["identityDomain"], d)
    if key_commitment != want:
        raise Refuse("SCOPE2_MISMATCH")


# ------------------------------------------------------------------ dependency sources
def constructed_key(doc, row):
    sep = params(doc, "PACKAGE-KEY-JOIN")["separator"]
    return row["name"] + sep + row["version"] + sep + row["sourceId"]


def depsrc_set_key_constraints(doc, packages):
    p = params(doc, "DEPSRC-SET-KEY-CONSTRAINTS")
    limit = int(p["forbidInNameVersionAtOrBelow"])
    for row in packages:
        if any(ord(c) <= limit for c in row["name"] + row["version"]) or len(constructed_key(doc, row)) > int(p["maxKeyScalars"]):
            raise Refuse("REQUEST.PRECONDITION_FAILED:" + p["refusal"]["detail"])


def package_key_join(doc, packages, key):
    if params(doc, "PACKAGE-KEY-JOIN")["join"] != "exact-constructed-key":
        raise Refuse("UNKNOWN_JOIN")
    hits = [r for r in packages if constructed_key(doc, r) == key]
    if len(hits) != 1:
        raise Refuse("PACKAGE_KEY_JOIN")
    return hits[0]


def depsrc_custody(doc, packages, manifest, file_manifest_fn=None):
    p = params(doc, "DEPSRC-CUSTODY")
    depsrc_set_key_constraints(doc, packages)
    entries = manifest["entries"]
    if not entries:
        if manifest["manifestSha256"] != hashlib.sha256(b"\x80").hexdigest() or packages:
            raise Refuse("DEPSRC_EMPTY_SET")
        return
    tuples, seen_packages = [], {}
    for e in entries:
        W.lexical(params(doc, "CANONICAL-PATH-ADMISSION")["lexical"], e["path"], "entries.path")
        row = package_key_join(doc, packages, e["packageKey"])
        record = dict(row, path=e["path"])
        tuples.append(tuple(record[k].encode(p["orderBytes"]) for k in p["entryOrder"]))
        seen_packages.setdefault(e["packageKey"], []).append(e)
    if tuples != sorted(tuples) or len(set(tuples)) != len(tuples):
        raise Refuse("DEPSRC_ORDER")
    if len(seen_packages) != len(packages):
        raise Refuse("DEPSRC_PACKAGE_MISSING")
    for row in packages:
        rows = seen_packages[constructed_key(doc, row)]
        if len(rows) != row["fileCount"] or sum(r["byteLength"] for r in rows) != row["totalBytes"]:
            raise Refuse("DEPSRC_FILE_COUNTS")
        if file_manifest_fn is not None:
            files = {r["path"]: {"sha256": r["contentSha256"], "byteLength": r["byteLength"]} for r in rows}
            if file_manifest_fn(files) != row["fileManifestSha256"]:
                raise Refuse("DEPSRC_FILE_MANIFEST")
    if manifest["manifestSha256"] != raw_hex(entries):
        raise Refuse("MANIFEST_DIGEST")


# ------------------------------------------------------------------ prepared outputs
def prepared_entries(rows):
    return [{"outputOrdinal": i, "kind": r["kind"], "planRow": r,
             "logicalPath": f".opensip/prepared/v3/{i}-{r['blob']['sha256']}.blob",
             "blobByteLength": r["blob"]["byteLength"], "blobSha256": r["blob"]["sha256"],
             "contentByteLength": r["blob"]["byteLength"], "contentSha256": r["blob"]["sha256"]} for i, r in enumerate(rows)]


def prepared_wire_limit(doc, prepared_set, plan_id):
    p = params(doc, "PREPARED-V3-WIRE-LIMIT")
    rows = prepared_set["rows"]
    if p["countScope"] == "all-inert-rows":
        counted = len(rows)
    elif p["countScope"] == "build-script-directives-only":
        counted = sum(1 for r in rows if r["kind"] == "build-script-directives")
    else:
        raise Refuse("UNKNOWN_COUNT_SCOPE")
    detail = "REQUEST.PRECONDITION_FAILED:" + p["refusal"]["detail"]
    if counted > int(p["maxEntries"]):
        raise Refuse(detail + ":entries")
    if sum(r["blob"]["byteLength"] for r in rows) > int(p["maxTotalBlobBytes"]):
        raise Refuse(detail + ":blob-bytes")
    entries = prepared_entries(rows)
    manifest = {"planId": plan_id, "manifestSha256": "0" * 64, "entries": entries}
    if W.encoded_length(manifest) > int(p["maxManifestBytes"]):
        raise Refuse(detail + ":manifest-bytes")
    if any(e["outputOrdinal"] > int(p["maxOrdinal"]) for e in entries):
        raise Refuse(detail + ":ordinal")
    return entries


def prepared_entry_join(entries):
    for i, e in enumerate(entries):
        r = e["planRow"]
        if (e["outputOrdinal"] != i or e["kind"] != r["kind"] or e["blobSha256"] != r["blob"]["sha256"]
                or e["blobByteLength"] != r["blob"]["byteLength"] or e["contentSha256"] != e["blobSha256"]
                or e["contentByteLength"] != e["blobByteLength"] or e["logicalPath"] != f".opensip/prepared/v3/{i}-{r['blob']['sha256']}.blob"):
            raise Refuse("PREPARED_ENTRY_JOIN")
        if r["kind"] == "generated-file" and (r.get("generated") is None or r["generated"]["blob"] != r["blob"]):
            raise Refuse("PREPARED_GENERATED_BLOB")


# ------------------------------------------------------------------ P3 overlay (data-driven)
def overlay_run(doc, p3, identity_tokens, events, stage_count=1):
    ov = doc["protocols"]["rust-semantic"]["transitions"]
    rules = copy.deepcopy(p3["rules"])
    pre = list(p3["wildcards"]["*PRE_COMPLETE"]["phases"])
    if ov["cancel"]["hostMaySendInStart"]:
        pre_cancel = ["START"] + pre
    else:
        pre_cancel = pre
    for r in rules:
        r.setdefault("guard", {}).update(ov["guardAdditions"].get(r["id"], {}))
    pf = set(p3["wildcards"]["*PROCESS_FAULT"]["frames"])
    src = {f for u in p3["stateUpdates"] if "sourceBytesSent" in u["sets"] for f in u.get("onFrames", [])}
    state = dict(p3["initialState"], **ov["stateAdditions"])
    trace, phases = [], []
    for ev in events:
        phase, frame = state["phase"], ev["frame"]
        if phase == "FAULT":
            trace.append("FAULT-absorb"); phases.append(state["phase"]); continue
        if phase in ("WAIT_ZERO_EXIT", "WAIT_EOF", "DONE") and frame not in ("zero-exit", "eof") and frame not in pf:
            state["phase"] = "FAULT"; trace.append("post-terminal-frame"); phases.append("FAULT"); continue
        if frame in pf:
            state["phase"] = "FAULT"; trace.append("P3-33"); phases.append("FAULT"); continue
        match = None
        for r in rules:
            rp = r["phase"]
            if rp == "*ANY":
                continue
            allowed = (pre_cancel if r["frame"] == "Cancel" else pre) if rp == "*PRE_COMPLETE" else [rp]
            if phase not in allowed or r["frame"] != frame:
                continue
            if all(state.get(k) == v for k, v in r.get("guard", {}).items()):
                match = r; break
        if match is None:
            state["phase"] = "FAULT"; trace.append("P3-34"); phases.append("FAULT"); continue
        if frame == "HelloAck":
            state["identityNegotiated"] = all(t in ev.get("capabilities", []) for t in identity_tokens)
        if frame == "OpenUniverse":
            state["dependencyMode"], state["preparedMode"] = bool(ev.get("dependencyMode", True)), bool(ev.get("preparedMode"))
        if frame == "Analyze":
            state["stageCount"], state["stageIndex"] = stage_count, 0
        for upd in ov["stateUpdateAdditions"]:
            if frame in upd["onFrames"]:
                state.update(upd["sets"])
        if frame in src:
            state["sourceBytesSent"] = True
        nxt = match["next"]
        if nxt == "ANALYZING_OR_READY_COMPLETE":
            state["stageIndex"] += 1; state["stagesCompleted"] += 1
            nxt = "READY_COMPLETE" if state["stageIndex"] == state["stageCount"] else "ANALYZING"
        if "terminal" in match:
            state["terminalKind"] = match["terminal"]
        state["phase"] = nxt; trace.append(match["id"]); phases.append(nxt)
    return {"finalPhase": state["phase"], "terminalKind": state["terminalKind"], "trace": trace, "phases": phases}


# ------------------------------------------------------------------ RUST3-PROVIDER-FAULT
HOST_TO_WORKER = {"Hello", "OpenUniverse", "SnapshotManifest", "SnapshotFileChunk", "SnapshotSeal", "DependencySourceManifest",
                  "DependencySourceChunk", "DependencySourceSeal", "PreparedOutputManifest", "PreparedOutputChunk",
                  "PreparedOutputSeal", "Analyze", "Cancel"}


def provider_fault(doc, p3, identity_tokens, events, fault):
    """events: host-ordered frames before the ProviderFault (each {frame, payload?, capabilities?}); fault: payload."""
    p = params(doc, "RUST3-PROVIDER-FAULT")
    if p.get("readHelloFirst") and (not events or events[0]["frame"] != "Hello"):
        raise Refuse("PROVIDER_FAULT_BEFORE_HELLO")
    anchor = 0
    for i, ev in enumerate(events):
        if ev["frame"] not in HOST_TO_WORKER:
            anchor = i
    if p["hostAdmission"] != "possible-phase-set" or p["phaseSemantics"] != "worker-observed":
        prefixes = [len(events)]  # host-receipt view: only the full host transcript
    else:
        prefixes = list(range(anchor + 1, len(events) + 1))
    run = overlay_run(doc, p3, identity_tokens, events)
    candidates = []
    for n in prefixes:
        prefix = events[:n]
        phase = run["phases"][n - 1]
        values = {}
        for member, frame in p["nullLaw"].items():
            sent = [ev for ev in prefix if ev["frame"] == frame]
            values[member] = sent[-1]["payload"][member] if sent else None
        candidates.append((phase, values))
    for phase, values in candidates:
        if fault["phase"] != phase:
            continue
        if p.get("jointConsistency"):
            if all(fault[m] == values[m] for m in p["nullLaw"]):
                return
        else:
            if all(fault[m] in (None, values[m]) for m in p["nullLaw"]):
                return
    raise Refuse("PROVIDER_FAULT_OBSERVATION")


# ------------------------------------------------------------------ anchors
def anchor_admission(doc, language, anchors, manifest, snapshot2, cve1_fn):
    p = params(doc, "ANCHOR-WIRE-SPAN")
    if not 1 <= len(anchors) <= int(p["maxCount"]):
        raise Refuse("ANCHOR_COUNT")
    for a in anchors:
        if a["kind"] == "fact-ref":
            raise Refuse("ANCHOR_FACT_REF_UNDER_FACT2")
        lex = "TS2-LOGICAL-PATH-ADMISSION" if language == "typescript-semantic" else "CANONICAL-PATH-ADMISSION"
        W.lexical(params(doc, lex)["lexical"], a["path"], "anchor.path")
        e = manifest.get(a["path"])
        if e is None or e["kind"] != "file" or e["contentSha256"] != a["contentSha256"] or a["snapshotId"] != snapshot2:
            raise Refuse("ANCHOR_SOURCE_JOIN")
        ok = a["startByte"] < a["endByte"] if p["nonEmpty"] else a["startByte"] <= a["endByte"]
        if not (ok and a["endByte"] <= e["byteLength"]):
            raise Refuse("ANCHOR_EMPTY_OR_OUT_OF_BOUNDS")
    key = W.encode if p["order"][language] == "cbor-bytes-strict" else cve1_fn
    encoded = [key(a) for a in anchors]
    if encoded != sorted(encoded) or len(set(encoded)) != len(encoded):
        raise Refuse("ANCHOR_ORDER")


# ------------------------------------------------------------------ digests, echoes, custody
def manifest_digest(manifest):
    if manifest["manifestSha256"] != raw_hex(manifest["entries"]):
        raise Refuse("MANIFEST_DIGEST")


def accepted_equals_seal(seal, accepted):
    if seal != accepted:
        raise Refuse("ACCEPTED_NOT_SEAL")


def chunk_custody(entry, chunks):
    offset = 0
    data = b""
    if entry["byteLength"] == 0 and chunks:
        raise Refuse("CHUNK_FOR_EMPTY_ENTRY")
    for i, c in enumerate(chunks):
        if c["path"] != entry["path"] or c["chunkIndex"] != i or c["byteOffset"] != offset:
            raise Refuse("CHUNK_ORDER")
        offset += len(c["bytes"])
        data += c["bytes"]
    if offset != entry["byteLength"] or hashlib.sha256(data).hexdigest() != entry["contentSha256"]:
        raise Refuse("CHUNK_DIGEST_OR_LENGTH")


def seal_aggregates(entries, chunk_count, seal, total_member):
    files = [e for e in entries if e.get("kind", "file") == "file"]
    if seal["entryCount"] != len(entries) or seal[total_member] != sum(e["byteLength"] for e in files) or seal["totalChunkCount"] != chunk_count:
        raise Refuse("SEAL_AGGREGATES")


def cancel_nullability(sent_frames, cancel):
    ou = [f for f in sent_frames if f["frame"] == "OpenUniverse"]
    an = [f for f in sent_frames if f["frame"] == "Analyze"]
    if cancel["executionId"] != (ou[-1]["payload"]["executionId"] if ou else None):
        raise Refuse("CANCEL_EXECUTION_ID")
    if cancel["analysisOrdinal"] != (an[-1]["payload"]["analysisOrdinal"] if an else None):
        raise Refuse("CANCEL_ANALYSIS_ORDINAL")


def cancelled_echo(cancel, cancelled, host_send_phase=None):
    if cancelled["executionId"] != cancel["executionId"] or cancelled["analysisOrdinal"] != cancel["analysisOrdinal"]:
        raise Refuse("CANCELLED_ECHO")
    if host_send_phase is not None and cancelled.get("observedPhase") != host_send_phase:
        raise Refuse("CANCELLED_OBSERVED_PHASE")


def budget_observed(doc, payload, plan_budget):
    p = params(doc, "RUST3-BUDGET-EXHAUSTED")
    if plan_budget is None or plan_budget["unit"] == "milliseconds":
        raise Refuse("BUDGET_NOT_EXHAUSTIBLE")
    if payload["unit"] != plan_budget["unit"] or payload["limit"] != plan_budget["limit"]:
        raise Refuse("BUDGET_JOIN")
    if payload["observed"] != payload["limit"] + int(p["observedMinusLimit"]):
        raise Refuse("BUDGET_OBSERVED")


def occupancy_join(batch):
    by = {c["candidateOrdinal"]: c for c in batch["candidates"]}
    comps = batch["occupancyCompanions"]
    ords = [c["candidateOrdinal"] for c in comps]
    if len(comps) > len(batch["candidates"]) or ords != sorted(set(ords)) or len(ords) != len(set(ords)):
        raise Refuse("OCCUPANCY_ORDER")
    for c in comps:
        cand = by.get(c["candidateOrdinal"])
        if cand is None or cand["targetUniverseId"] != c["targetUniverseId"]:
            raise Refuse("OCCUPANCY_JOIN")


# ------------------------------------------------------------------ COMMIT-MAP
def commit_row(doc, field):
    for r in doc["commitmentMap"]["rows"]:
        if r["field"] == field:
            return r
    raise Refuse("COMMIT_FIELD_UNMAPPED", field)


def commit_value(doc, field, stages_entries):
    """stages_entries: list of per-stage arrays. Returns the commitment the map assigns to `field` for the LAST stage
    (stage classes) or for the stage-major concatenation (stage-major classes)."""
    r = commit_row(doc, field)
    if r["valueClass"] in ("stage-entries", "stage-candidates"):
        value = stages_entries[-1]
    elif r["valueClass"] in ("stage-major-entries", "stage-major-candidates"):
        value = [e for s in stages_entries for e in s]
    else:
        raise Refuse("COMMIT_CLASS_NOT_STREAM")
    return C(r["domain"], value)
