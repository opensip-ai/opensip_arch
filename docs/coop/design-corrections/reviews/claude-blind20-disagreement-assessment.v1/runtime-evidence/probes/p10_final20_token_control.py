"""Does the blind19 protocol-token finding actually hold on FINAL20's own literals?

Root's control ran on consumer19. The task says not to infer that it automatically holds for
final20, so this repeats it on final20's exact bytes. Inert AST literals only; the frozen
reference protocol machine is executed, consumer code never is.

READ-ONLY.
"""
import ast
import copy
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

B = Path("/tmp/opensip-design-corrections")
SRC = B / "candidate-subject.v33"
P = B / "consumer-b.v20/output/lib/phase3_traces.py"
TRACES = B / "consumer-b.v20/output/traces"


def sha(b):
    return hashlib.sha256(b).hexdigest()


out = {"standing": "READ-ONLY. Inert AST literals from FINAL20; frozen reference machine executed; "
                   "no consumer code run, no consumer file written, no acceptance implied.",
       "phase3Path": str(P), "phase3Sha256": sha(P.read_bytes())}

tree = ast.parse(P.read_text())
names = {}
for node in tree.body:
    if isinstance(node, ast.Assign):
        for t in node.targets:
            if isinstance(t, ast.Name):
                try:
                    names[t.id] = ast.literal_eval(node.value)
                except Exception:  # noqa: BLE001
                    pass
out["helloAckFullLiteral"] = names.get("HELLO_ACK_FULL")


def literal(n):
    if isinstance(n, ast.Name):
        return copy.deepcopy(names[n.id])
    if isinstance(n, ast.List):
        return [literal(x) for x in n.elts]
    if isinstance(n, ast.Tuple):
        return tuple(literal(x) for x in n.elts)
    return ast.literal_eval(n)


main = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "main")
node = next(n for n in main.body
            if isinstance(n, ast.Assign)
            and any(isinstance(t, ast.Name) and t.id == "full" for t in n.targets))
events = [{"frame": x[0], **x[1]} if isinstance(x, tuple) else {"frame": x}
          for x in literal(node.value)]
out["eventFrames"] = [e["frame"] for e in events]

model = SRC / "docs/coop/design-corrections/native/native_evidence_model.v2.py"
spec = importlib.util.spec_from_file_location("blind20_protocol33", model)
M = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = M
spec.loader.exec_module(M)
out["frozenModelSha256"] = sha(model.read_bytes())
out["owningIdentityTokens"] = list(M.IDENTITY_TOKENS)

actual = M.protocol3_run(events)
corrected = copy.deepcopy(events)
next(x for x in corrected if x["frame"] == "HelloAck")["capabilities"] = list(M.IDENTITY_TOKENS)
control = M.protocol3_run(corrected)

out["asFinal20Wrote"] = {k: actual.get(k) for k in
                         ("finalPhase", "terminalKind", "identityNegotiated",
                          "sourceBytesSent", "stagesCompleted")}
out["asFinal20WroteTrace"] = actual.get("trace")
out["withOwningTokensOnly"] = {k: control.get(k) for k in
                               ("finalPhase", "terminalKind", "identityNegotiated",
                                "sourceBytesSent", "stagesCompleted")}
out["withOwningTokensOnlyTrace"] = control.get("trace")
out["tokenListIsTheOnlyChange"] = (
    [e["frame"] for e in events] == [e["frame"] for e in corrected]
    and all(a == b for a, b in zip(events, corrected)
            if a.get("frame") != "HelloAck"))

# What does final20 itself claim for this trace?
claimed = None
comp = TRACES / "complete.json"
if comp.is_file():
    rows = json.loads(comp.read_text())
    claimed = next((x for x in rows if x.get("trace") == "complete"), None)
    out["final20TracesSha256"] = sha(comp.read_bytes())
out["final20OwnClaim"] = {k: claimed.get(k) for k in
                          ("finalPhase", "terminalKind", "identityNegotiated",
                           "sourceBytesSent", "stagesCompleted")} if claimed else None
out["frameSequenceMatchesFinal20Claim"] = (
    claimed is not None and [e["frame"] for e in events] == claimed.get("events"))

first_div = None
if claimed and actual.get("trace"):
    for i, (a, c) in enumerate(zip(actual["trace"], claimed.get("ruleTrace") or [])):
        if a != c:
            first_div = {"index": i, "reference": a, "consumer": c}
            break
out["firstRuleTraceDivergence"] = first_div
print(json.dumps(out, indent=2, default=str))
