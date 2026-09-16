"""Reference host sender consuming the immutable canonical send plan (candidate 06; review-03 RF-4, review-04 RF-4, A-2,
review-05 RF-1).

This is NOT the M3 sender. It states and executes the private plan-consumption contract the M3 sender must honour:

- The Plan-time planner (tools/representability.py) produces an immutable canonical send plan: `schedule` (one slot per
  host-to-worker frame in P3 host order, with sequence, frameType, exact envelope payloadBytes, payloadSha256, chunk
  coordinates entry/chunkIndex/byteOffset/byteLength, seal totalChunkCount and, on an entry's last chunk slot,
  entryContentSha256), `cancelReserve` (one maximal Cancel) and `cancelEcho` (the planned correlation and the slots of
  Hello, OpenUniverse and Analyze).
- payloadSha256 is the SHA-256 of the deterministic-CBOR bytes of the planned frame payload. For a chunk slot it covers
  the chunk payload without its `bytes` member (payloadSha256Scope payload-without-bytes), because the planner never
  materializes chunk bytes; the bytes are bound by the manifest entry contentSha256 instead: the sender hashes the bytes
  it actually sends for an entry and compares at the entry's last chunk slot. Length-only chunk bytes (ByteLen, used by
  the reference realizations) cannot be hashed; consume reports how many entries it verified.
- The canonical chunk schedule is greedy: every chunk of an entry carries exactly the maximum chunk bytes except the
  entry's last; a zero-length entry has no chunk. It is frame-minimal, NOT byte-minimal.
- The sender MUST emit exactly the planned frames in order. Every slot is compared on sequence, frameType, chunk
  coordinates, seal count, payload byte length and payload digest BEFORE it becomes sent state, so a same-length
  substitution of OpenUniverse.executionId, Analyze.analysisOrdinal, a manifest or seal digest or a chunk header is
  refused at its own slot. A Cancel:
    * never precedes the Hello slot (P3-29 *PRE_COMPLETE excludes START; hostMaySendInStart is false);
    * echoes the correlation actually SENT (CANCEL-NULLABILITY): executionId null until an OpenUniverse frame has been
      consumed and then that frame's executionId; analysisOrdinal null until an Analyze frame has been consumed and then
      its analysisOrdinal; reason user-interrupt. Because every consumed slot is digest-bound, the sent correlation
      equals the planned one; the echo is nevertheless derived from sent state;
    * is compared by its deterministic-CBOR encoded typed bytes, never by host-language equality (false is not 0; 0.0
      has no encoding in the profile), and a payload that is not the exact echo is refused before it becomes sent state;
    * takes the next sequence number, is sent at most once, and nothing follows it.
  Any divergence refuses before the frame is written (SENDER_DIVERGENCE:<reason>). `progress`, when given, holds the
  sent state after the last accepted frame - the already-sent prefix - which a refused frame never extends.

DEFENSIVE BRANCHES, stated honestly:
- `cancel-over-reserve` cannot fire once `cancel-echo` has passed, because the reserve is measured on the maximal echo.
- `frame-limit` and `request-limit` cannot fire for a transcript that conforms to a plan the planner accepted under the
  same limits; they guard a plan consumed under different limits and are exercised only by vectors that do that.

realize() is an INDEPENDENT realization of the canonical schedule from the request (it shares no code with the planner),
so a plan and its realization agreeing - digests included - is evidence rather than self-agreement.
"""
import hashlib

import wirecodec as W

Refuse = W.Refuse
CHUNK_DIGEST_EXCLUDES = ("bytes",)


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


def _typed_bytes(payload):
    try:
        return W.encode(payload)
    except Refuse:
        return None


def measured(protocol, accounting, frame):
    value = _envelope(protocol)(frame["sequence"], frame["frameType"], frame["payload"]) if accounting["lengthScope"] == "envelope-payload" else frame["payload"]
    return W.encoded_length(value) + (int(accounting["prefixBytes"]) if accounting["prefixIncluded"] else 0)


def expected_cancel(plan, slots_consumed, sent=None):
    """The exact Cancel payload lawful after `slots_consumed` slots (None before Hello). `sent` is the correlation of the
    frames actually consumed ({executionId, analysisOrdinal}); without it the planned correlation is used."""
    echo = plan["cancelEcho"]
    if slots_consumed <= echo["helloSlot"]:
        return None
    src = sent if sent is not None else echo
    return {"executionId": src["executionId"] if slots_consumed > echo["openUniverseSlot"] else None,
            "analysisOrdinal": src["analysisOrdinal"] if slots_consumed > echo["analyzeSlot"] else None,
            "reason": echo["reason"]}


def consume(plan, protocol, accounting, limits, transcript, progress=None):
    schedule, reserve = plan["schedule"], plan["cancelReserve"]
    frame_limit = int(limits["maxFramePayloadBytes"])
    totals = protocol in accounting["totalsApplyTo"]
    slot, total, frames, cancelled = 0, 0, 0, False
    sent = {"executionId": None, "analysisOrdinal": None}
    entry_hash, verified_entries = None, 0
    for f in transcript:
        if cancelled:
            raise _div("frame-after-cancel", f["frameType"])
        if type(f["sequence"]) is not int or f["sequence"] != frames:
            raise _div("sequence", "%s!=%s" % (f["sequence"], frames))
        n = measured(protocol, accounting, f)
        is_cancel, entry_verified = f["frameType"] == "Cancel", False
        if is_cancel:
            if reserve is None:
                raise _div("cancel-without-reserve")
            want = expected_cancel(plan, slot, sent)
            if want is None:
                raise _div("cancel-before-hello", "slot %d" % slot)
            same = _typed_bytes(f["payload"]) == W.encode(want)
            if not same:
                raise _div("cancel-echo", "slot %d" % slot)
            if n > reserve["payloadBytes"]:  # defensive: unreachable once the echo is exact (the reserve is the maximal echo)
                raise _div("cancel-over-reserve", str(n))
        else:
            if slot >= len(schedule):
                raise _div("frame-not-planned", f["frameType"])
            s = schedule[slot]
            if s["frameType"] != f["frameType"]:
                raise _div("frame-type", "%s!=%s" % (f["frameType"], s["frameType"]))
            chunk = "chunkIndex" in s
            if chunk:
                p = f["payload"]
                if (_entry_of(f["frameType"], p), p["chunkIndex"], p["byteOffset"], _nbytes(p["bytes"])) != (s["entry"], s["chunkIndex"], s["byteOffset"], s["byteLength"]):
                    raise _div("chunk-schedule", "slot %d" % slot)
            if "totalChunkCount" in s and f["payload"]["totalChunkCount"] != s["totalChunkCount"]:
                raise _div("seal-count", "slot %d" % slot)
            if n != s["payloadBytes"]:
                raise _div("payload-bytes", "slot %d: %d!=%d" % (slot, n, s["payloadBytes"]))
            if s.get("payloadSha256") is None or W.encoded_digest(f["payload"], CHUNK_DIGEST_EXCLUDES if chunk else ()) != s["payloadSha256"]:
                raise _div("payload-digest", "slot %d" % slot)
            if chunk:
                b = f["payload"]["bytes"]
                if s["chunkIndex"] == 0:
                    entry_hash = hashlib.sha256()
                if isinstance(b, W.ByteLen):
                    entry_hash = None
                elif entry_hash is not None:
                    entry_hash = entry_hash.copy()
                    entry_hash.update(b)
                if "entryContentSha256" in s and entry_hash is not None:
                    if entry_hash.hexdigest() != s["entryContentSha256"]:
                        raise _div("chunk-content", "slot %d" % slot)
                    entry_verified = True
        if n > frame_limit:  # defensive: reachable only when a plan is consumed under limits other than its planning limits
            raise _div("frame-limit", str(n))
        if totals and (total + n > int(limits["maxRequestPayloadBytesTotal"]) or frames + 1 > int(limits["maxRequestFrames"])):  # defensive, as above
            raise _div("request-limit", "%d bytes %d frames" % (total + n, frames + 1))
        # every check passed: the frame becomes sent state
        frames += 1
        total += n
        if is_cancel:
            cancelled = True
        else:
            if f["frameType"] == "OpenUniverse":
                sent["executionId"] = f["payload"]["executionId"]
            elif f["frameType"] == "Analyze":
                sent["analysisOrdinal"] = f["payload"]["analysisOrdinal"]
            verified_entries += 1 if entry_verified else 0
            slot += 1
        if progress is not None:
            progress.update(framesSent=frames, payloadBytesSent=total, slotsConsumed=slot, cancelled=cancelled, sentCorrelation=dict(sent),
                            chunkContentVerifiedEntries=verified_entries)
    return {"framesSent": frames, "payloadBytesSent": total, "slotsConsumed": slot, "cancelled": cancelled,
            "complete": cancelled or slot == len(schedule), "sentCorrelation": dict(sent), "chunkContentVerifiedEntries": verified_entries}


def realize(req, protocol, limits, materialize=False):
    """The canonical transcript for a request, derived independently of the planner. Chunk bytes are ByteLen, or zero
    bytes when `materialize` (for requests whose entries' contentSha256 are the digests of zero bytes)."""
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
                add(chunk_type, dict(base_of(e), chunkIndex=index, byteOffset=offset, bytes=bytes(n) if materialize else W.ByteLen(n)))
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


def cancel_frame(sequence, payload):
    return {"frameType": "Cancel", "sequence": sequence, "payload": payload}
