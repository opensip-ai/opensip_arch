"""List selectors already bound by the product design lock's contract successors (NSS-F1 evidence)."""
import json, sys, subprocess, collections
arch, prod = sys.argv[1], sys.argv[2]
lock = json.load(open(f"{prod}/design-lock.json"))
bound = collections.defaultdict(list)
latest = {}
for c in lock["contractSuccessors"]:
    p = c["record"]["path"]
    s = json.load(open(f"{arch}/{p}"))
    for o in s.get("passageOverrides", []):
        bound[o["parent"]["path"]].append((json.dumps(o["selector"]), p))
    for cand in s.get("candidates", []):
        latest[cand.get("path", json.dumps(cand)[:80])] = p
for parent, sels in sorted(bound.items()):
    print(f"== {parent}: {len(sels)}")
    if "native-evidence.md" in parent or "startup" in parent or "handshake" in parent:
        for sel, p in sorted(sels):
            print("  ", sel, p.split('/')[-2])
print("== candidates touching handshake/startup/native-evidence:")
for k, v in latest.items():
    if any(t in k for t in ("handshake", "startup", "native-evidence", "native-carriers")):
        print("  ", k, "<-", v)
