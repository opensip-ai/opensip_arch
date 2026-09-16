"""Final20 surface claims: protocol capability tokens, mutation keys, multistep availability.

READ-ONLY over consumer20's exact final public files and frozen source33. No consumer execution.
"""
import ast
import hashlib
import json
import re
from pathlib import Path

B = Path("/tmp/opensip-design-corrections")
C20 = B / "consumer-b.v20"
S = B / "candidate-subject.v33"
DC = S / "docs/coop/design-corrections"
out = {"standing": "READ-ONLY inspection of consumer20 final public files vs frozen source33."}


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


# --- 1. Protocol capability tokens in FINAL20 phase3 ----------------------------------------
p3 = C20 / "output/lib/phase3_traces.py"
tok = {"path": str(p3), "exists": p3.is_file()}
if p3.is_file():
    src = p3.read_text()
    tok["sha256"] = sha(p3)
    tok["capabilityLiteralLines"] = [
        {"line": i + 1, "text": l.strip()[:220]}
        for i, l in enumerate(src.splitlines())
        if re.search(r"snapshot2|plan2|fact2|coverage2|scope2|view2", l)
        and re.search(r"capab|Capab|HelloAck|hello_ack", l)
    ]
    # Every string literal that looks like an identity alias token.
    aliases = sorted({m for m in re.findall(
        r"['\"](snapshot2|plan2|fact2|coverage2|scope2|view2)['\"]", src)})
    tok["aliasTokenLiteralsPresent"] = aliases
    owning = sorted({m for m in re.findall(
        r"['\"](source-identity-snapshot2|plan-identity-plan2|fact-identity-fact2|coverage-v3)['\"]",
        src)})
    tok["owningTokenLiteralsPresent"] = owning
out["final20Phase3Tokens"] = tok

# --- 2. The owning four tokens, as published ------------------------------------------------
nm = DC / "native/native_evidence_model.v2.py"
src = nm.read_text()
hits = []
for m in re.finditer(r"source-identity-snapshot2|plan-identity-plan2|fact-identity-fact2|coverage-v3",
                     src):
    line = src[:m.start()].count("\n") + 1
    hits.append({"line": line, "token": m.group(0)})
out["owningTokensInFrozenModel"] = {"path": str(nm), "sha256": sha(nm),
                                    "hits": hits[:20], "hitCount": len(hits)}
# Published in the native contract chapter?
ne = S / "docs/v2/contracts/product-v1/native-evidence.md"
ne_src = ne.read_text()
ctr = []
for t in ("source-identity-snapshot2", "plan-identity-plan2", "fact-identity-fact2", "coverage-v3"):
    idxs = [ne_src[:m.start()].count("\n") + 1 for m in re.finditer(re.escape(t), ne_src)]
    ctr.append({"token": t, "linesInNativeContract": idxs[:6], "count": len(idxs)})
out["owningTokensInNativeContract"] = {"path": str(ne), "sha256": sha(ne), "tokens": ctr}
# And are the ALIASES ever named as capability tokens in the contract?
alias_ctx = []
for t in ("snapshot2", "plan2", "fact2", "coverage2", "scope2", "view2"):
    cnt = len(re.findall(re.escape(t), ne_src))
    alias_ctx.append({"token": t, "occurrencesAnywhereInNativeContract": cnt})
out["aliasOccurrencesInNativeContract"] = alias_ctx

# --- 3. Mutation keys in FINAL20 ------------------------------------------------------------
mk = []
vec = C20 / "output/vectors"
if vec.is_dir():
    for p in sorted(vec.rglob("*.json")):
        try:
            txt = p.read_text()
        except Exception:  # noqa: BLE001
            continue
        if "req-7f3a1c" in txt or "step-2" in txt or "mutation" in p.name:
            mk.append({"path": str(p.relative_to(C20)), "sha256": sha(p),
                       "hasReq7f3a1c": "req-7f3a1c" in txt,
                       "hasStep2Literal": '"step-2"' in txt or "'step-2'" in txt})
out["final20MutationVectors"] = mk

# --- 4. The published RequestId / StepId shapes ---------------------------------------------
common = DC / "workflows/schemas/common.schema.json"
inv = DC / "workflows/schemas/invocation-record.schema.json"
shapes = {}
if common.is_file():
    j = json.loads(common.read_text())
    defs = j.get("$defs", {})
    shapes["common.sha256"] = sha(common)
    for k in ("RequestId", "StepId"):
        if k in defs:
            shapes[k] = defs[k]
if inv.is_file():
    j = json.loads(inv.read_text())
    d = j.get("$defs", {}).get("MutationReplayScopeV1")
    shapes["invocation-record.sha256"] = sha(inv)
    shapes["MutationReplayScopeV1"] = d
out["publishedIdShapes"] = shapes

# --- 5. Independent mutation-surface probes the consumer added -------------------------------
probes = []
for p in sorted((C20 / "output/lib").rglob("*mutation*")):
    probes.append({"path": str(p.relative_to(C20)), "sha256": sha(p), "bytes": p.stat().st_size})
out["final20MutationSurfaceFiles"] = probes

print(json.dumps(out, indent=2, default=str))
