"""Independent Grok probes for native-wire-owner06. Writes only under review/results."""
from __future__ import annotations

import hashlib
import json
import re
import sys
import traceback
from pathlib import Path

REVIEW = Path("/tmp/opensip-implementation/m1-grok-native-review-06/root-reproduction")
COPY = REVIEW / "copy"
RESULTS = REVIEW / "results"
RESULTS.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(COPY / "tools"))

import sender_ref as SR  # noqa: E402
import wirecodec as W  # noqa: E402
import admission_ref as AR  # noqa: E402


class Cases:
    def __init__(self):
        self.rows = []

    def rec(self, name, passed, **detail):
        self.rows.append({"name": name, "passed": bool(passed), **detail})
        print(("PASS" if passed else "FAIL"), name)
        return passed


def code_of(fn):
    try:
        fn()
        return "accepted"
    except W.Refuse as exc:
        return exc.code
    except Exception as exc:  # noqa: BLE001
        return type(exc).__name__ + ":" + str(exc)[:200]


def main():
    C = Cases()
    wire = json.loads((COPY / "wire-carriers.v1.json").read_text())
    contract = (COPY / "contract.md").read_text()
    owner = json.loads((COPY / "owner-pattern-successor.v1.json").read_text())
    succ = json.loads((COPY / "successor.json").read_text())
    routes = json.loads((COPY / "public-route-successor.v1.json").read_text())

    claim = re.compile(r"(?i)selected[ _-]*final[ _-]*owner|final[ _-]+owner|selectedOwner|approved[ _-]+(owner|successor)|authoritative[ _-]+owner")
    dialect_standing = wire["privateRepresentation"]["patternDialect"]["standing"]
    C.rec(
        "pattern-dialect-standing-still-says-selected-final-owner",
        "selected final owner" in dialect_standing.lower(),
        standing=dialect_standing,
        note="This is a defect probe: True means the forbidden RF-2 phrase remains in the published carrier.",
    )
    admission_text = json.dumps([r["rule"] for r in wire["admission"]])
    C.rec(
        "admission-rules-do-not-contain-selected-final-owner",
        "selected final owner" not in admission_text.lower(),
    )
    owner_rule = next(r for r in wire["admission"] if r["id"] == "OWNER-PATTERN-EVALUATION")
    C.rec(
        "owner-pattern-evaluation-uses-proposed-correction-and-promotion-condition",
        "proposed reference owner correction" in owner_rule["rule"]
        and "effective as selected semantics only after root acceptance and source-bridge promotion" in owner_rule["rule"],
        ruleStart=owner_rule["rule"][:240],
    )
    author_scan_texts = {
        "admission": admission_text,
        "owner": json.dumps(owner),
        "routes": json.dumps(routes),
        "p3": (COPY / "p3-guard-successor.v1.json").read_text(),
        "successor": json.dumps(succ),
        "contract": contract,
    }
    author_hits = {k: sorted({m.group(0) for m in claim.finditer(v)}) for k, v in author_scan_texts.items()}
    full_carrier_hits = sorted({m.group(0) for m in claim.finditer(json.dumps(wire))})
    C.rec(
        "rf2-wording-check-misses-pattern-dialect-standing",
        not any(author_hits.values()) and bool(full_carrier_hits),
        authorScanHits=author_hits,
        fullCarrierHits=full_carrier_hits,
    )
    C.rec(
        "contract-claims-check-covers-carrier-rules",
        "forbids premature owner-selection claims in the carrier rules" in contract,
    )

    selftest = (COPY / "selftest.py").read_text()
    # Count CONTROLS keys of the form "name": (
    keys = re.findall(r'\n    "([A-Za-z0-9_]+)": \(', selftest)
    # The CONTROLS dict starts after CONTROLS = {
    start = selftest.find("CONTROLS = {")
    end = selftest.find("\n}\n\n\ndef run_control")
    body = selftest[start:end]
    control_keys = re.findall(r'\n    "([A-Za-z0-9_]+)": \(', body)
    C.rec("selftest-declares-149-controls", len(control_keys) == 149, count=len(control_keys), keysHead=control_keys[:8], keysTail=control_keys[-8:])
    for name in (
        "r5_sender_slot_digest_unchecked",
        "r5_cancel_python_equality",
        "rf1_echo_ignores_sent_state",
        "rf1_chunk_content_unchecked",
        "a2_partial_stale_set_selected",
        "a2_failed_row_readable",
        "rf2_selected_owner_wording_restored",
        "rf2_root_mutants_attributed",
    ):
        C.rec("control-present:" + name, name in control_keys)

    # Direct sender consume: synthetic three-slot plan.
    protocol = "rust-semantic"
    accounting = {
        "lengthScope": "envelope-payload",
        "prefixBytes": "40",
        "prefixIncluded": False,
        "totalsApplyTo": ["rust-semantic"],
    }
    limits = {
        "maxFramePayloadBytes": "1000000",
        "maxRequestPayloadBytesTotal": "10000000",
        "maxRequestFrames": "1000",
    }

    def nbytes(seq, ft, payload):
        env = {
            "protocolMajor": 3,
            "direction": "host-to-worker",
            "sequence": seq,
            "frameType": ft,
            "payload": payload,
        }
        return W.encoded_length(env)

    hello, ou, analyze = {"k": "hello"}, {"executionId": "exec-2026-09-13-0001"}, {"analysisOrdinal": 0}
    payloads = [("Hello", hello), ("OpenUniverse", ou), ("Analyze", analyze)]
    schedule = []
    frames = []
    for i, (ft, pl) in enumerate(payloads):
        schedule.append({"frameType": ft, "payloadBytes": nbytes(i, ft, pl), "payloadSha256": W.encoded_digest(pl)})
        frames.append({"frameType": ft, "sequence": i, "payload": pl})
    plan = {
        "schedule": schedule,
        "cancelReserve": {"payloadBytes": 100000},
        "cancelEcho": {
            "helloSlot": 0,
            "openUniverseSlot": 1,
            "analyzeSlot": 2,
            "executionId": ou["executionId"],
            "analysisOrdinal": 0,
            "reason": "user-interrupt",
        },
    }
    ok = SR.consume(plan, protocol, accounting, limits, frames)
    C.rec("synthetic-canonical-transcript-accepted", ok["complete"] and ok["framesSent"] == 3, result=ok)

    sub_ou = dict(frames[1], payload=dict(ou, executionId="exec-2026-09-13-0000"))
    progress = {}
    code = code_of(lambda: SR.consume(plan, protocol, accounting, limits, frames[:1] + [sub_ou], progress))
    C.rec(
        "same-length-openuniverse-executionid-refused-payload-digest-before-sent",
        code == "SENDER_DIVERGENCE:payload-digest" and progress.get("framesSent") == 1 and progress.get("sentCorrelation", {}).get("executionId") is None,
        code=code,
        progress=progress,
    )
    progress = {}
    planned_echo = SR.expected_cancel(plan, 2)
    code = code_of(lambda: SR.consume(plan, protocol, accounting, limits, frames[:1] + [sub_ou, SR.cancel_frame(2, planned_echo)], progress))
    C.rec(
        "substituted-openuniverse-then-planned-echo-still-payload-digest",
        code == "SENDER_DIVERGENCE:payload-digest" and progress.get("framesSent") == 1,
        code=code,
        progress=progress,
    )
    progress = {}
    false_echo = dict(SR.expected_cancel(plan, 3), analysisOrdinal=False)
    code = code_of(lambda: SR.consume(plan, protocol, accounting, limits, frames + [SR.cancel_frame(3, false_echo)], progress))
    C.rec(
        "cancel-analysisordinal-false-for-zero-refused-typed-bytes",
        code == "SENDER_DIVERGENCE:cancel-echo"
        and progress.get("sentCorrelation") == {"executionId": ou["executionId"], "analysisOrdinal": 0}
        and not progress.get("cancelled"),
        code=code,
        progress=progress,
        falseCbor=W.encode(False).hex(),
        zeroCbor=W.encode(0).hex(),
    )
    C.rec("cbor-false-is-not-zero", W.encode(False) != W.encode(0) and W.encode(False) == b"\xf4" and W.encode(0) == b"\x00")
    progress = {}
    code = code_of(lambda: SR.consume(plan, protocol, accounting, limits, frames + [SR.cancel_frame(3, dict(SR.expected_cancel(plan, 3), analysisOrdinal=0.0))], progress))
    C.rec(
        "cancel-analysisordinal-float-zero-refuses-before-or-at-echo",
        code in ("UNENCODABLE:float", "SENDER_DIVERGENCE:cancel-echo", "UNENCODABLE"),
        code=code,
        progress=progress,
    )
    progress = {}
    seq_false = [dict(frames[0], sequence=False)] + frames[1:]
    code = code_of(lambda: SR.consume(plan, protocol, accounting, limits, seq_false, progress))
    C.rec("sequence-boolean-zero-refused", code == "SENDER_DIVERGENCE:sequence" and progress.get("framesSent", 0) == 0, code=code, progress=progress)

    # Chunk content: two-chunk entry; flip first chunk; last chunk refuses; first chunk already sent.
    body = bytes(10)
    c0, c1 = body[:5], bytearray(body[5:])
    flipped = bytearray(body[:5])
    flipped[0] ^= 1
    flipped = bytes(flipped)
    entry_digest = hashlib.sha256(body).hexdigest()

    def chunk(seq, index, offset, data, last=False):
        payload = {
            "snapshotId": "snap",
            "path": "a.rs",
            "chunkIndex": index,
            "byteOffset": offset,
            "bytes": data,
            "totalChunkCount": 2,
        }
        slot = {
            "frameType": "SnapshotFileChunk",
            "entry": ["a.rs"],
            "chunkIndex": index,
            "byteOffset": offset,
            "byteLength": len(data),
            "totalChunkCount": 2,
            "payloadBytes": nbytes(seq, "SnapshotFileChunk", payload),
            "payloadSha256": W.encoded_digest(payload, SR.CHUNK_DIGEST_EXCLUDES),
            "payloadSha256Scope": "payload-without-bytes",
        }
        if last:
            slot["entryContentSha256"] = entry_digest
        return slot, {"frameType": "SnapshotFileChunk", "sequence": seq, "payload": payload}

    # Rebuild a 2-slot chunk-only plan (illegal as a full request; consume only checks schedule vs transcript).
    s0, f0 = chunk(0, 0, 0, flipped)
    s1, f1 = chunk(1, 1, 5, bytes(c1), last=True)
    # Digests exclude bytes, so the planned digest must be computed from the *planned* (unflipped) first chunk.
    planned0, _ = chunk(0, 0, 0, body[:5])
    chunk_plan = {
        "schedule": [planned0, s1],
        "cancelReserve": None,
        "cancelEcho": {"helloSlot": 99, "openUniverseSlot": 99, "analyzeSlot": 99, "executionId": None, "analysisOrdinal": None, "reason": "user-interrupt"},
    }
    progress = {}
    code = code_of(lambda: SR.consume(chunk_plan, protocol, accounting, limits, [f0, f1], progress))
    C.rec(
        "early-chunk-corruption-sent-last-chunk-refused-chunk-content",
        code == "SENDER_DIVERGENCE:chunk-content" and progress.get("framesSent") == 1,
        code=code,
        progress=progress,
        note="Contracted: an earlier corrupt chunk may already have been sent; receiver must not publish before last-chunk/manifest/seal admission.",
    )
    # Last-chunk flip refuses before that last frame is sent.
    last_flip = bytearray(body[5:])
    last_flip[0] ^= 1
    s0u, f0u = chunk(0, 0, 0, body[:5])
    s1b, f1b = chunk(1, 1, 5, bytes(last_flip), last=True)
    last_plan = {
        "schedule": [s0u, s1],
        "cancelReserve": None,
        "cancelEcho": chunk_plan["cancelEcho"],
    }
    progress = {}
    code = code_of(lambda: SR.consume(last_plan, protocol, accounting, limits, [f0u, f1b], progress))
    C.rec(
        "last-chunk-corruption-refused-before-that-frame-sent",
        code == "SENDER_DIVERGENCE:chunk-content" and progress.get("framesSent") == 1,
        code=code,
        progress=progress,
    )

    # Prepared read authority
    entries = [
        {"outputOrdinal": 0, "planRow": {"status": "ok"}, "logicalPath": "ok-0"},
        {"outputOrdinal": 1, "planRow": {"status": "failed"}, "logicalPath": "failed-1"},
        {"outputOrdinal": 2, "planRow": {"status": "ok"}, "logicalPath": "ok-2"},
    ]
    C.rec("prepared-read-ok-row", AR.prepared_read_authority(entries, 0) == "ok-0")
    C.rec("prepared-read-ok-after-failed", AR.prepared_read_authority(entries, 2) == "ok-2")
    C.rec("prepared-read-failed-row-refused", code_of(lambda: AR.prepared_read_authority(entries, 1)) == "PREPARED_ROW_NOT_READABLE")
    C.rec("prepared-read-unknown-ordinal-refused", code_of(lambda: AR.prepared_read_authority(entries, 3)) == "PREPARED_ORDINAL_UNKNOWN")

    # Encoded digest equals full encoding for non-excluded maps.
    C.rec(
        "encoded-digest-matches-sha256-of-full-encode",
        W.encoded_digest(ou) == hashlib.sha256(W.encode(ou)).hexdigest(),
        digest=W.encoded_digest(ou),
    )
    chunk_payload = {"snapshotId": "snap", "path": "a.rs", "chunkIndex": 0, "byteOffset": 0, "bytes": b"abc", "totalChunkCount": 1}
    without = {k: v for k, v in chunk_payload.items() if k != "bytes"}
    C.rec(
        "chunk-digest-excludes-bytes-and-matches-encode-without-bytes",
        W.encoded_digest(chunk_payload, ("bytes",)) == hashlib.sha256(W.encode(without)).hexdigest(),
    )

    # Preserved failed controls from root-check-01
    failed01 = json.loads((COPY / "prior/root-continuation-06/root-check-01.json").read_text())
    C.rec(
        "root-check-01-failures-preserved",
        failed01["failed"] == 4 and {f["id"] for f in failed01["failures"]}
        == {
            "unpromoted-successor-authority-wording",
            "root-attribution-matches-receipts",
            "vector:HOST-SEND-SCHEDULE:cancel-analysis-ordinal-float-zero-refused",
            "vectors:HOST-SEND-SCHEDULE",
        },
        failures=[f["id"] for f in failed01["failures"]],
        checks=failed01["checks"],
    )
    author06 = (COPY / "prior/author06-quota-harness/final-response.md").read_bytes()
    C.rec("author06-quota-harness-preserved", len(author06) == 75, bytes=len(author06), text=author06.decode("utf-8", "replace"))
    receipt = json.loads((COPY / "prior/root-continuation-06/receipt.json").read_text())
    C.rec(
        "root-receipt-claims-596-and-149-and-selftest-isolation",
        receipt["checks"] == 596
        and receipt["failed"] == 0
        and receipt["rootSelftestExecuted"] is True
        and receipt["mutationControls"]["caught"] == 149,
        receipt=receipt,
    )
    # filelist INPUTS = 41
    import filelist as FL  # noqa: E402

    C.rec("filelist-inputs-41", len(FL.INPUTS) == 41, count=len(FL.INPUTS))

    failed = [r for r in C.rows if not r["passed"]]
    # The wording-leak probe is expected to PASS as a detection (the phrase is present).
    # That is evidence of a required finding, not a failed probe.
    out = {
        "standing": "Independent Grok probes of native-wire-owner06; not product acceptance",
        "passed": not failed,
        "caseCount": len(C.rows),
        "failedCount": len(failed),
        "failed": [r["name"] for r in failed],
        "checks": C.rows,
    }
    (RESULTS / "independent-probes.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({"passed": out["passed"], "caseCount": out["caseCount"], "failed": out["failed"]}))
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception:
        Path("/tmp/opensip-implementation/m1-grok-native-review-06/root-reproduction/results/independent-probes.exc").write_text(traceback.format_exc())
        raise
