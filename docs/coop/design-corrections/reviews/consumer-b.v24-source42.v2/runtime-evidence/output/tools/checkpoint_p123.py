import json
import sys

sys.path.insert(0, '/private/tmp/opensip-design-corrections/consumer-b.v24-source42.v2/output/tools')
import status as S

OUT = S.OUT
p1 = json.load(open(OUT + 'vectors/phase1-canonical.json'))
p2 = json.load(open(OUT + 'vectors/capability-manifests.json'))
p3 = json.load(open(OUT + 'traces/controls.json'))
assert p1["assertionFailures"] == [] and p2["assertionFailures"] == [] and p3["assertionFailures"] == []
st = S.load_status()
for rid in ['R-H-HELPER', 'R-CVE1-EIGHT-TYPES', 'R-LEXICAL-ADMISSION', 'R-SEMANTIC-VS-OPERATIONAL', 'R-RAW-VS-PARSED', 'R-ACYCLIC-JOINS']:
    S.set_status(st, rid, 'executed', artifact='vectors/phase1-canonical.json')
S.set_status(st, 'R-CVE1-EIGHT-TYPES', 'executed', artifact='vectors/cve1-eight-types.json')
S.set_status(st, 'R-LEXICAL-ADMISSION', 'executed', first_refusal='raw-input lexical boundary (see firstRefusal per vector)')
S.save_status(st)
S.write_checkpoint(1, st, ['ref/canonical.py', 'ref/schemas.py', 'ref/cve1.py', 'vectors/phase1_canonical.py', 'vectors/phase1-canonical.json', 'vectors/cve1-eight-types.json'], [],
                   "C/H, CVE1, raw lexical admission, raw-vs-parsed, semantic-vs-operational and acyclic-join vectors executed with assertions (exit 0). Chain vector is explanatory (no replay).")
for rid in ['R-CAP-ADMISSION', 'R-CAP-NAMED-GATES']:
    S.set_status(st, rid, 'executed', artifact='vectors/capability-manifests.json', first_refusal='per negative: ADM-TYPE|ADM-CLOSED|ADM-DOMAIN|ADM-ORDER|CVE1-ENCODE|LEX_*')
S.save_status(st)
S.write_checkpoint(2, st, ['vectors/phase2_capmanifest.py', 'vectors/capability-manifests.json'], [],
                   "Four gates in registry gateOrder before CVE1 encoding; masking recorded; successor RELATION-DOMAIN-V2/LADDER mirror drift-checked.")
for rid in ['R-TRACE-COMPLETE', 'R-TRACE-UNAVAILABLE', 'R-TRACE-CANCEL', 'R-TRACE-FAULT', 'R-TRACE-IDENTITY-BEFORE-SOURCE', 'R-TRACE-TERMINAL', 'R-TRACE-EXECUTED-VS-HOST']:
    S.set_status(st, rid, 'executed', artifact='traces/')
S.save_status(st)
cp = S.write_checkpoint(3, st, ['ref/protocol3.py', 'vectors/phase3_traces.py', 'traces/complete.json', 'traces/unavailable.json', 'traces/cancel.json', 'traces/fault.json', 'traces/terminal.json', 'traces/controls.json'], [],
                        "All 34 published rows exercised; rows pairwise disjoint; executed-vs-future-host recorded per trace. HelloAck echo mismatch modeled as s9.1 payload rule (not a table row).")
print(json.dumps({"phase3Unexecuted": cp["requirementIdsUnexecuted"], "executed": len(cp["requirementIdsExecuted"])}))
