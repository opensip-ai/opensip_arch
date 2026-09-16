"""Reference host sender consuming the immutable canonical send plan (candidate 04; review-03 RF-4, A-5, A-7).

This is NOT the M3 sender. It states and executes the private plan-consumption contract the M3 sender must honour:

- The Plan-time planner (tools/representability.py) produces an immutable canonical send plan: `schedule` (one slot per
  host-to-worker frame in P3 host order, with sequence, frameType, exact envelope payloadBytes, chunk coordinates
  entry/chunkIndex/byteOffset/byteLength and seal totalChunkCount), `cancelReserve` (one maximal Cancel) and totals.
- The canonical chunk schedule is greedy: every chunk of an entry carries exactly the maximum chunk bytes except the
  entry's last; a zero-length entry has no chunk. It is frame-minimal, NOT byte-minimal, and no other lawful chunking
  is claimed to fit the budget computed for it.
- The sender MUST emit exactly the planned frames in order. A Cancel may take the next sequence number at most once, at
  any point, with payload bytes <= the reserve, and nothing follows it. Any other divergence refuses before the frame is
  written (SENDER_DIVERGENCE:<reason>); running totals are re-checked against the owner limits after every frame.

realize() is an INDEPENDENT realization of the canonical schedule from the request (it shares no code with the planner),
so a plan and its realization agreeing is evidence rather than self-agreement.
"""
import wirecodec as W

Refuse = W.Refuse


def _div(reason, detail=""):
    return Refuse("SENDER_DIVERGENCE:" + reason, detail)


def _envelope(protocol):
    if protocol == "rust-semantic":
        return lambda seq, ft, payload: {"protocolMajor": 3, "direction": "host-to-worker", "sequence": seq, "frameType": ft, "payload": payload}
    return lambda seq, ft, payload: {"protocolMajor": 2, "frameType": ft, "sequence": seq, "payload": payload}


def _nbytes(b):
    return b.n if isinstance(b, W.ByteLen) else len(b)


def _entry_of(frame_type, payload):
    if frame_type == "SnapshotFileChunk":
        return [payload["path"]]
    if frame_type == "DependencySourceChunk":
        return [payload["packageKey"], payload["path"]]
    return [payload["outputOrdinal"]]


def measured(protocol, accounting, frame):
    value = _envelope(protocol)(frame["sequence"], frame["frameType"], frame["payload"]) if accounting["lengthScope"] == "envelope-payload" else frame["payload"]
    return W.encoded_length(value) + (int(accounting["prefixBytes"]) if accounting["prefixIncluded"] else 0)


def consume(plan, protocol, accounting, limits, transcript):
    schedule, reserve = plan["schedule"], plan["cancelReserve"]
    frame_limit = int(limits["maxFramePayloadBytes"])
    totals = protocol in accounting["totalsApplyTo"]
    slot, total, frames, cancelled = 0, 0, 0, False
    for f in transcript:
        if cancelled:
            raise _div("frame-after-cancel", f["frameType"])
        if f["sequence"] != frames:
            raise _div("sequence", "%s!=%s" % (f["sequence"], frames))
        n = measured(protocol, accounting, f)
        if f["frameType"] == "Cancel":
            if reserve is None or n > reserve["payloadBytes"]:
                raise _div("cancel-over-reserve", str(n))
            cancelled = True
        else:
            if slot >= len(schedule):
                raise _div("frame-not-planned", f["frameType"])
            s = schedule[slot]
            if s["frameType"] != f["frameType"]:
                raise _div("frame-type", "%s!=%s" % (f["frameType"], s["frameType"]))
            if "chunkIndex" in s:
                p = f["payload"]
                if (_entry_of(f["frameType"], p), p["chunkIndex"], p["byteOffset"], _nbytes(p["bytes"])) != (s["entry"], s["chunkIndex"], s["byteOffset"], s["byteLength"]):
                    raise _div("chunk-schedule", "slot %d" % slot)
            if "totalChunkCount" in s and f["payload"]["totalChunkCount"] != s["totalChunkCount"]:
                raise _div("seal-count", "slot %d" % slot)
            if n != s["payloadBytes"]:
                raise _div("payload-bytes", "slot %d: %d!=%d" % (slot, n, s["payloadBytes"]))
            slot += 1
        if n > frame_limit:
            raise _div("frame-limit", str(n))
        frames += 1
        total += n
        if totals and (total > int(limits["maxRequestPayloadBytesTotal"]) or frames > int(limits["maxRequestFrames"])):
            raise _div("request-limit", "%d bytes %d frames" % (total, frames))
    return {"framesSent": frames, "payloadBytesSent": total, "slotsConsumed": slot, "cancelled": cancelled,
            "complete": cancelled or slot == len(schedule)}


def realize(req, protocol, limits):
    """The canonical transcript for a request, derived independently of the planner (chunk bytes as ByteLen)."""
    frames = []

    def add(ft, payload):
        frames.append({"frameType": ft, "sequence": len(frames), "payload": payload})

    def custody(manifest_type, chunk_type, seal_type, manifest, id_field, total_field, max_chunk, base_of, length_of):
        add(manifest_type, manifest)
        count = 0
        for e in manifest["entries"]:
            length, offset, index = length_of(e), 0, 0
            while offset < length:
                n = min(max_chunk, length - offset)
                add(chunk_type, dict(base_of(e), chunkIndex=index, byteOffset=offset, bytes=W.ByteLen(n)))
                offset, index, count = offset + n, index + 1, count + 1
        add(seal_type, {id_field: manifest[id_field], "manifestSha256": manifest["manifestSha256"], "entryCount": len(manifest["entries"]),
                        total_field: sum(length_of(e) for e in manifest["entries"]), "totalChunkCount": count})

    add("Hello", req["hello"])
    add("OpenUniverse", req["openUniverse"])
    sm = req["snapshotManifest"]
    custody("SnapshotManifest", "SnapshotFileChunk", "SnapshotSeal", sm, "snapshotId", "totalFileBytes", int(limits["maxSnapshotChunkBytes"]),
            lambda e: {"snapshotId": sm["snapshotId"], "path": e["path"]}, lambda e: e["byteLength"] if e["kind"] == "file" else 0)
    if protocol == "rust-semantic":
        dm = req["dependencyManifest"]
        custody("DependencySourceManifest", "DependencySourceChunk", "DependencySourceSeal", dm, "dependencySourceSetId", "totalBytes",
                int(limits["maxDependencySourceChunkBytes"]),
                lambda e: {"dependencySourceSetId": dm["dependencySourceSetId"], "packageKey": e["packageKey"], "path": e["path"]}, lambda e: e["byteLength"])
        pm = req.get("preparedManifest")
        if pm is not None:
            custody("PreparedOutputManifest", "PreparedOutputChunk", "PreparedOutputSeal", pm, "planId", "totalBlobBytes", int(limits["maxPreparedOutputChunkBytes"]),
                    lambda e: {"planId": pm["planId"], "outputOrdinal": e["outputOrdinal"]}, lambda e: e["blobByteLength"])
    add("Analyze", req["analyze"])
    return frames


def cancel_frame(req, sequence, execution_id=None):
    return {"frameType": "Cancel", "sequence": sequence,
            "payload": {"executionId": execution_id if execution_id is not None else req["openUniverse"]["executionId"],
                        "analysisOrdinal": req["analyze"]["analysisOrdinal"], "reason": "user-interrupt"}}
