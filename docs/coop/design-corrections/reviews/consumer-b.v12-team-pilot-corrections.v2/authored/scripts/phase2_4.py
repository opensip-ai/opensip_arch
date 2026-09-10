#!/usr/bin/env python3
"""Phases 2–4: capability admission, protocol traces, relation/rung tables."""
from __future__ import annotations

import json
import sys
from pathlib import Path

OUT = Path("/tmp/opensip-design-corrections/consumer-b.v12-team-pilot-corrections.v2/output")
KIT = Path("/tmp/opensip-design-corrections/consumer-b.v12-team-pilot-corrections.v2/subject")
sys.path.insert(0, str(OUT))

from helper.cap_manifest import capability_manifest_id, first_refusal  # noqa: E402
from helper.protocol3 import IDENTITY_TOKENS, run_trace  # noqa: E402
from helper.status import mark, write_checkpoint  # noqa: E402


def dump(rel: str, obj) -> str:
    p = OUT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=2) + "\n")
    return str(p)


# ---------- Phase 2: capability manifests ----------
# Independently chosen; not DELIVERY live authoring catalogues (those fail ADM-ORDER).

def provider(**kw):
    base = {
        "providerId": "typescript-semantic",
        "language": "typescript",
        "providerVersionSource": "release.typescript-provider",
        "toolchainIdentitySource": "release.typescript-runtime",
        "relations": {
            "calls": "resolved-callee",
            "clones": "normalized-body-hash",
            "control-flow": "syntactic",
            "declares": "syntactic",
            "file": "enumerated",
            "imports": "resolved-target",
            "literal": "syntactic",
            "package": "manifest-declared",
            "reachability": "from-resolved-calls",
            "references": "resolved-binding",
            "types": "checked",
            "unresolved-edge": "observed",
            "vcs-change": "vcs-reported",
        },
        "platformIds": [
            "linux-aarch64-gnu",
            "linux-x86_64-gnu",
            "macos-aarch64",
            "macos-x86_64",
        ],
    }
    base.update(kw)
    return base


good = {
    "schemaVersion": 1,
    "profile": "core",
    "providers": [
        provider(providerId="rust-semantic", language="rust"),
        provider(providerId="typescript-semantic", language="typescript"),
    ],
    "coverageForAbsent": [],
}
# providers must be sorted by providerId: rust-semantic < typescript-semantic (r < t)
assert good["providers"][0]["providerId"] < good["providers"][1]["providerId"]

pos = capability_manifest_id(good)
assert pos["ok"]

gates = []


def neg(name, manifest, expect_gate, hypothesized_later):
    r = first_refusal(manifest)
    assert r["ok"] is False, (name, r)
    rec = {
        "name": name,
        "classification": "invalid",
        "expectedGate": expect_gate,
        "firstRefusal": r["firstRefusal"],
        "gate": r["gate"],
        "masksLater": r["masksLater"],
        "hypothesizedLaterChecksMasked": hypothesized_later,
        "note": "First observed refusal only; later gates not executed.",
    }
    gates.append(rec)
    return rec


# ADM-TYPE: boolean schemaVersion (CVE1 would mint a wrong id)
t1 = dict(good)
t1["schemaVersion"] = True
neg("ADM-TYPE-boolean-schemaVersion", t1, "ADM-TYPE", ["ADM-CLOSED", "ADM-DOMAIN", "ADM-ORDER"])

t2 = dict(good)
t2["schemaVersion"] = "1"
neg("ADM-TYPE-string-schemaVersion", t2, "ADM-TYPE", ["ADM-CLOSED", "ADM-DOMAIN", "ADM-ORDER"])

# ADM-CLOSED: extra key
c1 = dict(good)
c1 = {**good, "comment": "no"}
neg("ADM-CLOSED-undeclared-key", c1, "ADM-CLOSED", ["ADM-DOMAIN", "ADM-ORDER"])

c2 = {k: v for k, v in good.items() if k != "coverageForAbsent"}
neg("ADM-CLOSED-missing-key", c2, "ADM-CLOSED", ["ADM-DOMAIN", "ADM-ORDER"])

# ADM-DOMAIN: platform case
d1 = json.loads(json.dumps(good))
d1["providers"][0]["platformIds"] = [
    "linux-aarch64-gnu",
    "linux-x86_64-gnu",
    "macos-aarch64",
    "ALL-SUPPORTED",
]
neg("ADM-DOMAIN-platform-case", d1, "ADM-DOMAIN", ["ADM-ORDER"])

# ADM-DOMAIN: rung of another ladder (enumerated is file's rung, not calls)
d2 = json.loads(json.dumps(good))
d2["providers"][0]["relations"]["calls"] = "enumerated"
neg("ADM-DOMAIN-cross-ladder-rung", d2, "ADM-DOMAIN", ["ADM-ORDER"])

# ADM-ORDER: unsorted platformIds (linux-x86_64-gnu after macos would be wrong wait:
# linux-aarch64-gnu < linux-x86_64-gnu < macos-aarch64 < macos-x86_64
# reverse first two)
o1 = json.loads(json.dumps(good))
o1["providers"][0]["platformIds"] = [
    "linux-x86_64-gnu",
    "linux-aarch64-gnu",
    "macos-aarch64",
    "macos-x86_64",
]
neg("ADM-ORDER-platformIds", o1, "ADM-ORDER", [])

# ADM-ORDER: providers not sorted
o2 = json.loads(json.dumps(good))
o2["providers"] = list(reversed(o2["providers"]))
neg("ADM-ORDER-providers", o2, "ADM-ORDER", [])

# successor relation unresolved-edge is admitted (positive control)
assert "unresolved-edge" in good["providers"][0]["relations"]

dump(
    "vectors/cap-admission.json",
    {
        "kind": "standaloneCanonicalVector",
        "classification": "valid",
        "recipe": "CAP-MANIFEST-ID-V1",
        "selectors": [
            "docs/coop/artifacts/delivery.v4.json capabilityManifestIdentity CAP-MANIFEST-ID-V1",
            "docs/coop/design-corrections/native/capability-manifest-domains.v2.json (effective ADM-DOMAIN successor)",
            "docs/coop/artifacts/resolved-inputs.v2.json#planIdContract.canonicalValueEncoding",
        ],
        "gateOrder": ["ADM-TYPE", "ADM-CLOSED", "ADM-DOMAIN", "ADM-ORDER"],
        "positive": {
            "manifest": good,
            **pos,
            "outputMajorNote": "capabilityManifestId remains inherited bare-hex; not a typed prefix",
        },
        "note": "Admission before encoding. Independently chosen manifest; not a DELIVERY installProfiles authoring value.",
    },
)
dump(
    "vectors/cap-named-gates.json",
    {
        "kind": "standaloneCanonicalVector",
        "classification": "invalid",
        "vectors": gates,
        "positiveUnresolvedEdgeInSuccessorRegistry": True,
    },
)

mark(["R-CAP-ADMISSION"], status="executed", artifact="vectors/cap-admission.json")
mark(["R-CAP-NAMED-GATES"], status="executed", artifact="vectors/cap-named-gates.json")

# ---------- Phase 3: traces ----------
FULL_CAPS = list(IDENTITY_TOKENS) + [
    "sealed-vfs-v1",
    "multi-stage-analyze-v1",
    "rust-semantic-facts-v1",
    "resolution-completeness-v2",
    "unresolved-edge-v1",
    "dependency-source-v1",
    "prepared-output-v3",
    "native-context-v2",
]

complete_events = [
    {"frame": "Hello"},
    {"frame": "HelloAck", "capabilities": FULL_CAPS},
    {"frame": "OpenUniverse", "dependencyMode": True, "preparedMode": False},
    {"frame": "UniverseAccepted"},
    {"frame": "SnapshotManifest"},
    {"frame": "SnapshotFileChunk"},
    {"frame": "SnapshotSeal"},
    {"frame": "SnapshotAccepted"},
    {"frame": "DependencySourceManifest"},
    {"frame": "DependencySourceChunk"},
    {"frame": "DependencySourceSeal"},
    {"frame": "DependencySourceAccepted"},
    {"frame": "NativeContextVerified"},
    {"frame": "Analyze", "stageCount": 1},
    {"frame": "FactBatch"},
    {"frame": "CoverageV3"},
    {"frame": "Complete"},
    {"frame": "zero-exit"},
    {"frame": "eof"},
]
tr_complete = run_trace(complete_events, stage_count=1)
assert tr_complete["final"]["phase"] == "DONE"
assert tr_complete["final"]["terminalKind"] == "complete"
assert tr_complete["final"]["identityNegotiated"] is True
# identity before source: OpenUniverse is first source-byte frame
neg_idx = next(i for i, t in enumerate(tr_complete["trace"]) if t["event"]["frame"] == "OpenUniverse")
hello_idx = next(i for i, t in enumerate(tr_complete["trace"]) if t["event"]["frame"] == "HelloAck")
assert hello_idx < neg_idx
assert tr_complete["trace"][hello_idx]["identityNegotiated"] is True
assert tr_complete["trace"][hello_idx]["sourceBytesSent"] is False
assert tr_complete["trace"][neg_idx]["sourceBytesSent"] is True

# OpenUniverse before identity: HelloAck without identity tokens
no_id = [
    {"frame": "Hello"},
    {"frame": "HelloAck", "capabilities": ["sealed-vfs-v1"]},
    {"frame": "OpenUniverse", "dependencyMode": False, "preparedMode": False},
]
tr_noid = run_trace(no_id)
# P3-03 requires identityNegotiated true; otherwise P3-34 FAULT, sourceBytesSent still set on OpenUniverse update?
# Order on match: apply stateUpdates THEN next. If no match, noMatchLaw goes to FAULT without applying updates?
# protocol: "If no row matches, apply noMatchLaw" — OpenUniverse in READY_OPEN_UNIVERSE with identityNegotiated false
# does not match P3-03, so P3-34. stateUpdates only on successful row match.
assert tr_noid["final"]["phase"] == "FAULT"
assert tr_noid["final"]["sourceBytesSent"] is False
assert tr_noid["trace"][-1]["traceId"] == "P3-34"

unavail_events = complete_events[:13] + [  # through NativeContextVerified wait... index
    # START.. NativeContextVerified is events[0:13] which includes NativeContextVerified
]
# After NativeContextVerified we are READY_ANALYZE. Unavailable from WAIT_NATIVE_CONTEXT_VERIFIED is P3-21.
# Let's do Unavailable at WAIT_NATIVE_CONTEXT_VERIFIED instead of NativeContextVerified
unavail_events = complete_events[:12] + [
    {"frame": "Unavailable"},
    {"frame": "zero-exit"},
    {"frame": "eof"},
]
tr_unavail = run_trace(unavail_events)
assert tr_unavail["final"]["phase"] == "DONE"
assert tr_unavail["final"]["terminalKind"] == "unavailable"

cancel_events = complete_events[:14] + [  # through Analyze -> ANALYZING
    {"frame": "Cancel"},
    {"frame": "Cancelled"},
    {"frame": "zero-exit"},
    {"frame": "eof"},
]
tr_cancel = run_trace(cancel_events)
assert tr_cancel["final"]["phase"] == "DONE"
assert tr_cancel["final"]["terminalKind"] == "cancelled"

fault_events = [
    {"frame": "Hello"},
    {"frame": "HelloAck", "capabilities": FULL_CAPS},
    {"frame": "deadline"},  # *PROCESS_FAULT
]
tr_fault = run_trace(fault_events)
assert tr_fault["final"]["phase"] == "FAULT"
assert tr_fault["trace"][-1]["traceId"] == "P3-33"
# absorb
tr_fault2 = run_trace(fault_events + [{"frame": "Hello"}])
assert tr_fault2["trace"][-1]["traceId"] == "FAULT-absorb"

# post-terminal
post = complete_events[:17] + [  # through Complete -> WAIT_ZERO_EXIT
    {"frame": "FactBatch"},  # not zero-exit/eof/process-fault
]
tr_post = run_trace(post)
assert tr_post["final"]["phase"] == "FAULT"
assert tr_post["trace"][-1]["traceId"] == "post-terminal-frame"

dump("traces/complete.json", {"kind": "standaloneTraceVector", "classification": "valid", **tr_complete,
                               "executedVsHost": "executed reconstruction of published transitions; frame payload bytes and OS process are future-host assumptions"})
dump("traces/unavailable.json", {"kind": "standaloneTraceVector", "classification": "valid", **tr_unavail,
                                  "executedVsHost": "executed"})
dump("traces/cancel.json", {"kind": "standaloneTraceVector", "classification": "valid", **tr_cancel,
                             "executedVsHost": "executed"})
dump("traces/fault.json", {"kind": "standaloneTraceVector", "classification": "valid", **tr_fault,
                            "absorb": tr_fault2["trace"][-1],
                            "openUniverseWithoutIdentity": {
                                "trace": tr_noid,
                                "sourceBytesSent": False,
                                "identityNegotiated": False,
                            },
                            "executedVsHost": "executed"})
dump("traces/identity-before-source.json", {
    "kind": "standaloneTraceVector",
    "completeTrace": {
        "helloAckIndex": hello_idx,
        "openUniverseIndex": neg_idx,
        "identityNegotiatedBeforeSource": True,
        "helloAckSourceBytesSent": False,
    },
    "faultOpenUniverseWithoutIdentity": {
        "finalPhase": tr_noid["final"]["phase"],
        "sourceBytesSent": tr_noid["final"]["sourceBytesSent"],
        "traceId": tr_noid["trace"][-1]["traceId"],
    },
    "identityTokens": list(IDENTITY_TOKENS),
    "selector": "native-evidence.md §9.1 and protocol3-transitions.v1.json guardLaw",
})
dump("traces/terminal.json", {
    "kind": "standaloneTraceVector",
    "completeReachesDone": tr_complete["final"]["phase"] == "DONE",
    "postTerminal": tr_post,
    "terminalKindsExercised": ["complete", "unavailable", "cancelled"],
    "processFault": "P3-33",
    "note": "Reaching a terminal does not end the exchange: zero-exit then eof to DONE.",
    "executedVsHost": "executed transitions; actual process waitpid/EOF is future-host",
})
dump("traces/executed-vs-host.json", {
    "kind": "standingRule",
    "executed": "transition table, guards, identityNegotiated, sourceBytesSent, terminals, post-terminal, FAULT absorb",
    "futureHostAssumptions": [
        "real worker process spawn/exit/EOF",
        "frame payload schema validation and digest/VFS custody of chunks",
        "native compiler/cargo execution",
        "HelloAck capability array exact recursive equality vs Hello (payload law owned by §9.1; we reconstructed the identityNegotiated boolean the table consumes)",
    ],
})

for i, art in [
    ("R-TRACE-COMPLETE", "traces/complete.json"),
    ("R-TRACE-UNAVAILABLE", "traces/unavailable.json"),
    ("R-TRACE-CANCEL", "traces/cancel.json"),
    ("R-TRACE-FAULT", "traces/fault.json"),
    ("R-TRACE-IDENTITY-BEFORE-SOURCE", "traces/identity-before-source.json"),
    ("R-TRACE-TERMINAL", "traces/terminal.json"),
    ("R-TRACE-EXECUTED-VS-HOST", "traces/executed-vs-host.json"),
]:
    mark([i], status="executed", artifact=art)

ck2 = write_checkpoint(2, notes="Capability-manifest admission before encoding using domains.v2 successor registry. Named gates with first-refusal and masking.",
                       artifacts=["vectors/cap-admission.json", "vectors/cap-named-gates.json"])
ck3 = write_checkpoint(3, notes="Protocol3 traces reconstructed from protocol3-transitions.v1.json. Identity before source. Terminal zero-exit/eof. Executed vs future-host labeled.",
                       artifacts=["traces/complete.json", "traces/unavailable.json", "traces/cancel.json", "traces/fault.json",
                                  "traces/identity-before-source.json", "traces/terminal.json", "traces/executed-vs-host.json",
                                  "helper/protocol3.py"])

# ---------- Phase 4 ----------
rel_doc = json.loads((KIT / "docs/coop/design-corrections/foundation/relation-payload-schemas.v2.json").read_text())
reg = rel_doc["x-opensip-relation-registry"]["relations"]
RESOLVED_RUNGS = {
    "resolved-target",
    "resolved-binding",
    "resolved-callee",
    "checked",
    "from-resolved-calls",
}

rows = []
for name, row in sorted(reg.items()):
    ladder = row["ladder"]
    for rung in ladder:
        resolved = rung in RESOLVED_RUNGS
        rows.append({
            "relation": name,
            "rung": rung,
            "registeredPair": True,
            "subjectKind": row.get("subjectKind"),
            "anchorLaw": row.get("anchorLaw"),
            "universeRule": row.get("universeRule"),
            "snapshotJoins": row.get("snapshotJoins", []),
            "coverageTotality": row.get("coverageTotality"),
            "isResolvedRung": resolved,
            "rc1StateIfNoResolutionClaim": None if resolved else "not-applicable",
            "fileMustNotInventResolvedRung": name != "file" or rung == "enumerated",
        })

# RC-0 negative: unresolved-edge@enumerated
rc0_bad = {"relation": "unresolved-edge", "rung": "enumerated", "registeredPair": False}

dump("vectors/relation-rung-table.json", {
    "kind": "standaloneCanonicalVector",
    "selector": "foundation/relation-payload-schemas.v2.json#/x-opensip-relation-registry",
    "pairCount": len(rows),
    "relationCount": len(reg),
    "coveragePartitionLaw": rel_doc["x-opensip-relation-registry"]["coveragePartitionLaw"]["partitionKey"],
    "coverageTotalityRelations": [n for n, r in reg.items() if "coverageTotality" in r],
    "pairs": rows,
    "rc0UnregisteredPairRefused": rc0_bad,
    "fileLadder": reg["file"]["ladder"],
    "note": "Do not invent a resolved rung for file facts. file@enumerated only.",
})

# count/class/attempt applied to scopes/Coverage with and without facts
def rc1_mint(relation, rung):
    if rung not in reg[relation]["ladder"]:
        return {"ok": False, "firstRefusal": {"code": "RC-0", "message": "unregistered pair"}}
    resolved = rung in RESOLVED_RUNGS
    if not resolved:
        return {
            "ok": True,
            "state": "not-applicable",
            "attempted": False,
            "unresolvedEdgeCount": 0,
            "unresolvedEdgeClasses": [],
            "note": "fact-free entry over empty examined scope is judged the same way",
        }
    return {"ok": True, "resolved": True, "stateDecidedByRC2": True}


def rc2(attempted, examined_exhaustive, stage_terminal, edge_count):
    if not attempted:
        return "not-attempted"
    if stage_terminal != "complete" or not examined_exhaustive:
        return "partial"
    if edge_count == 0:
        return "complete"
    return "incomplete"


count_vectors = [
    {"name": "file-enumerated-fact-free", **rc1_mint("file", "enumerated"), "facts": []},
    {"name": "clones-fact-free", **rc1_mint("clones", "normalized-body-hash"), "facts": []},
    {"name": "imports-resolved-zero-edges-complete-stage", "rc2": rc2(True, True, "complete", 0), "facts": []},
    {"name": "imports-resolved-one-edge-incomplete", "rc2": rc2(True, True, "complete", 1)},
    {"name": "imports-resolved-unavailable-zero-edges-partial", "rc2": rc2(True, True, "unavailable", 0)},
    {"name": "imports-resolved-skipped-not-attempted", "rc2": rc2(False, True, None, 0)},
    {"name": "imports-resolved-partial-exam-zero-edges-partial", "rc2": rc2(True, False, "complete", 0)},
    {"name": "unregistered-unresolved-edge-enumerated", **rc1_mint("unresolved-edge", "enumerated")},
    {"name": "zero-count-never-implies-complete", "statement": "A zero count therefore never implies complete", "rc2_not_attempted_zero": rc2(False, True, None, 0)},
]
assert count_vectors[0]["state"] == "not-applicable"
assert count_vectors[2]["rc2"] == "complete"
assert count_vectors[3]["rc2"] == "incomplete"
assert count_vectors[4]["rc2"] == "partial"
assert count_vectors[5]["rc2"] == "not-attempted"
assert count_vectors[6]["rc2"] == "partial"
assert count_vectors[7]["ok"] is False

dump("vectors/count-class-attempt.json", {
    "kind": "standaloneCanonicalVector",
    "selector": "native-evidence.md §4.3 RC-0/RC-1/RC-2",
    "resolvedRungs": sorted(RESOLVED_RUNGS),
    "vectors": count_vectors,
    "appliedToFactAbsentScopes": True,
})

matrix = json.loads((KIT / "docs/coop/design-corrections/native/native-capability-matrix.v2.json").read_text())
cells = matrix["cells"]
# code vs data: syntaxOnlyGrammarClass in limitations
code_vs_data = {
    "selector": "native-capability-matrix.v2.json limitations.syntaxOnlyGrammarClass and capabilities",
    "codeGrammars": ["rust", "typescript", "javascript"],
    "dataDocumentGrammars": ["json", "toml", "markdown", "yaml"],
    "inventoryUngatedByGrammar": True,
    "dataDocumentMintsNoBodyIdentity": True,
    "clonesNearAuthority": "candidate-only",
    "clonesCrossAuthority": "candidate-only",
    "cellsByCapabilityMode": {(c["capability"], c["mode"]): c["state"] for c in cells},
}
# advertised modes
modes = matrix["languageModes"]
mode_paths = []
for m in modes:
    caps = [c["capability"] for c in cells if c["mode"] == m]
    mode_paths.append({
        "languageMode": m,
        "analysisPath": {
            "ts-tsconfig": "TypeScript compiler universe native.context.typescript.v2 + native.semantic-universe.typescript.v2",
            "js-allowjs": "TypeScript analyzer universe over JS bodies (allowJs); body language javascript, provider typescript",
            "js-synthesized": "synthesized tsconfig; TypeScript analyzer universe; L-JS1 limitations",
            "rust-cargo": "Rust cargo universe native.context.rust.v2 + native.semantic-universe.rust.v2",
            "rust-cargo-prepared": "Rust prepared-output mode; inert prepared rows; prepare-code grant",
            "syntax-only": "native.context.syntax.v2 + native.semantic-universe.syntax.v2; bundled grammars; no compiler",
        }[m],
        "chosenGrammar": {
            "ts-tsconfig": "typescript",
            "js-allowjs": "javascript-via-typescript-engine",
            "js-synthesized": "javascript-via-typescript-engine",
            "rust-cargo": "rust",
            "rust-cargo-prepared": "rust",
            "syntax-only": "bundled: rust|typescript|javascript (code) and json|toml|markdown|yaml (data-document)",
        }[m],
        "capabilityCountNamed": len(caps),
    })

dump("vectors/code-vs-data-matrix.json", {
    "kind": "standaloneCanonicalVector",
    "platformFamilies": matrix["platformFamilies"],
    "languageModes": modes,
    "capabilities": [c["id"] for c in matrix["capabilities"]],
    "syntaxOnlyGrammarClass": matrix["limitations"]["syntaxOnlyGrammarClass"],
    "candidateOnly": ["clones-near", "clones-cross-tsjs"],
    "notSelectedCells": [c for c in cells if c["state"] == "NOT-SELECTED"],
    "unsupportedTypedCells": [c for c in cells if c["state"] == "UNSUPPORTED-TYPED"],
})
dump("vectors/enum-vs-resolution.json", {
    "kind": "standingRule",
    "fileRung": "enumerated",
    "fileResolvedRungInvented": False,
    "rc6DoesNotEquateEnumerationWithResolution": True,
    "selector": "native-evidence.md §4.3 RC-6; relation-payload-schemas.v2 file.ladder",
})
dump("vectors/advertised-mode-paths.json", {
    "kind": "standingRule",
    "modes": mode_paths,
    "allAdvertisedHavePath": all(m["analysisPath"] for m in mode_paths),
})

mark(["R-RELATION-RUNG-TABLE"], status="executed", artifact="vectors/relation-rung-table.json")
mark(["R-COUNT-CLASS-ATTEMPT"], status="executed", artifact="vectors/count-class-attempt.json")
mark(["R-CODE-VS-DATA-MATRIX"], status="executed", artifact="vectors/code-vs-data-matrix.json")
mark(["R-ENUM-VS-RESOLUTION"], status="executed", artifact="vectors/enum-vs-resolution.json")
mark(["R-ADVERTISED-MODE-PATHS"], status="executed", artifact="vectors/advertised-mode-paths.json")

ck4 = write_checkpoint(4, notes="Complete registered relation/rung table (13 relations). RC-0/1/2 count/class/attempt including fact-absent. Code vs data matrix. File remains enumerated. All six advertised modes have a documented analysis path.",
                       artifacts=["vectors/relation-rung-table.json", "vectors/count-class-attempt.json",
                                  "vectors/code-vs-data-matrix.json", "vectors/enum-vs-resolution.json",
                                  "vectors/advertised-mode-paths.json"])
print("phase2-4 ok", "p2", len(ck2["requirementIdsExecuted"]), "p4", len(ck4["requirementIdsExecuted"]))
print("cap id", pos["capabilityManifestId"])
