"""CB7-ADV-4: publish PROTOCOL3_RULES as a machine-readable artifact, DERIVED from the exact rows."""
import importlib.util
import json
import pathlib

W = pathlib.Path('/private/tmp/opensip-design-corrections/v19-native-coauthor.v1/work')
NATIVE = W / 'docs/coop/design-corrections/native'

spec = importlib.util.spec_from_file_location('nem', NATIVE / 'native_evidence_model.v2.py')
N = importlib.util.module_from_spec(spec)
spec.loader.exec_module(N)

artifact = {
    "artifact": "opensip.native-evidence.protocol3-transitions",
    "version": 1,
    "status": "PROPOSED",
    "standing": (
        "NORMATIVE and CLOSED. The Rust major-3 provider protocol transition table of "
        "native-evidence section 9.2, published here so an independent consumer can reconstruct the "
        "host state machine WITHOUT reading author code. It states existing behaviour exactly; it is "
        "not a protocol redesign, adds no frame, no phase and no terminal, and changes no wire format."),
    "purpose": (
        "Section 9.2 named this table and described its frames in prose, but the 34 transition rows, "
        "their ORDER, their guards and their terminal semantics existed only inside "
        "native_evidence_model.v2.PROTOCOL3_RULES, which a review kit that excludes author code cannot "
        "read. The rows below are the same rows, and the reference model READS them from this document "
        "rather than carrying a second copy, so there is one authority and no transcription to drift."),
    "consumedBy": "docs/coop/design-corrections/native/native_evidence_model.v2.py (PROTOCOL3_PHASES, PROTOCOL3_RULES, protocol3_run)",
    "phases": list(N.PROTOCOL3_PHASES),
    "matchLaw": (
        "FIRST MATCH WINS in the declared `rules` order. A row matches when (a) its `phase` equals the "
        "current phase, or is the wildcard `*PRE_COMPLETE` and the current phase is a member of that "
        "wildcard's `phases`; AND (b) its `frame` equals the incoming frame; AND (c) every key of its "
        "`guard` equals the identically named field of the current state. Order is therefore "
        "load-bearing: the three `WAIT_SNAPSHOT_ACCEPTED` rows P3-08..P3-10 are distinguished only by "
        "their guards, and P3-14/P3-15 likewise, so reordering or re-sorting these rows changes which "
        "transition a conforming host takes."),
    "wildcards": {
        "*ANY": (
            "A phase wildcard used ONLY by the two catch-all rows P3-33 and P3-34. They are never "
            "reached by the matching loop above, which skips `*ANY` rows; they are applied by the two "
            "code paths named in `preMatchLaw` and `noMatchLaw` and are published as rows so that the "
            "trace vocabulary is complete."),
        "*PRE_COMPLETE": {
            "meaning": "Any phase in which the exchange has begun and has not yet reached a terminal.",
            "derivation": "`phases[1:17]` of the published `phases` list - from WAIT_HELLO_ACK through READY_COMPLETE inclusive.",
            "phases": list(N._PRE_COMPLETE)},
        "*": "A frame wildcard matching ANY frame; it appears only in the final fallback row P3-34.",
        "*PROCESS_FAULT": {
            "meaning": "Not a protocol frame at all: an out-of-band process observation.",
            "frames": sorted(N._PROCESS_FAULTS)},
    },
    "preMatchLaw": [
        "FAULT is ABSORBING: once the phase is FAULT every further event is recorded as `FAULT-absorb` and nothing transitions.",
        "In WAIT_ZERO_EXIT, WAIT_EOF or DONE, any frame other than `zero-exit`, `eof` or a `*PROCESS_FAULT` member is a post-terminal frame and goes to FAULT with trace `post-terminal-frame`.",
        "Any `*PROCESS_FAULT` member goes to FAULT with trace `P3-33` from ANY phase, which is what row P3-33 states.",
    ],
    "noMatchLaw": "An event matching no row goes to FAULT with trace `P3-34`, which is what the final fallback row states. There is no default transition and no silent ignore.",
    "guardLaw": (
        "Guard keys name fields of the host's own transition state and are compared for EXACT equality; "
        "all keys of a row's guard must hold for that row to match. `identityNegotiated` is set true "
        "only when the HelloAck frame's capabilities contain every identity token, so OpenUniverse - "
        "which carries snapshot2 and plan2 - is unreachable before negotiation and the run faults with "
        "no source byte sent."),
    "stateUpdates": [
        {"onFrame": "HelloAck", "sets": "identityNegotiated = every identity token is present in the frame's `capabilities`"},
        {"onFrame": "OpenUniverse", "sets": "dependencyMode and preparedMode from the frame's booleans; these are the guards P3-08..P3-10 and P3-14..P3-15 select on"},
        {"onFrame": "Analyze", "sets": "stageCount = the invocation's stage count; stageIndex = 0"},
        {"onFrames": sorted(N._SOURCE_FRAMES), "sets": "sourceBytesSent = true; this is the observable that proves no source byte preceded negotiation"},
    ],
    "stageDependentTransitions": {
        "ANALYZING_OR_READY_COMPLETE": (
            "The `next` of row P3-24 (CoverageV3 in ANALYZING) is NOT a phase. It increments both "
            "stageIndex and stagesCompleted and then resolves to READY_COMPLETE when stageIndex equals "
            "stageCount, and to ANALYZING otherwise. Without this the table cannot be interpreted at "
            "all for a multi-stage analysis: one CoverageV3 per stage is expected, and only the last "
            "one may be followed by Complete.")},
    "terminalLaw": (
        "A row carrying `terminal` records that terminalKind on the state as it transitions. The five "
        "terminal kinds are exactly those appearing in `rules`. Reaching a terminal does not end the "
        "exchange: the worker must still be observed at `zero-exit` and then `eof` (P3-31, P3-32) to "
        "reach DONE, and any other frame in between is the post-terminal fault above."),
    "ownedByProse": [
        "What each frame's PAYLOAD is and how it is validated (section 9.2's frame table and the payload schemas). This document is transitions only.",
        "The identity token set that decides `identityNegotiated`, which is negotiated in section 9.1 and is not a transition.",
        "The mapping from a terminalKind to stage authority, D9 class and exit code (section 10 / `stage_authority`, `run_termination`).",
        "The chunking, custody and digest obligations behind the manifest/chunk/seal frames (sections 3 and 5).",
        "The stage COUNT itself, which is an invocation property supplied to the transition system, not a value the table can derive.",
    ],
    "ruleCount": len(N.PROTOCOL3_RULES),
    "rules": [dict(row) for row in N.PROTOCOL3_RULES],
}

out = NATIVE / 'protocol3-transitions.v1.json'
out.write_text(json.dumps(artifact, indent=1, ensure_ascii=False) + '\n', encoding='utf-8')
print('wrote', out, artifact['ruleCount'], 'rows;', len(artifact['phases']), 'phases')
