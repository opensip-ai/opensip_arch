"""Read-only probe (prints only): record kinds in my retained ts-pass and rust-mixed stores that source44 startup payloads must join
(plan native contexts, semantic universes, coverage), so the startup vectors take their values from admitted Run records.
Usage: python3 tools/runref.py tools/probe_s44_records.py
"""
import collections
import json
import sys

OUT = "/private/tmp/opensip-design-corrections/consumer-b.v24-source45.v1/output"
sys.path.insert(0, OUT + "/ref")
import canonical as K  # noqa: E402
from store import Store  # noqa: E402

for name in ("ts-pass", "rust-mixed"):
    exp = json.load(open(f"{OUT}/runs/{name}.store.json"))
    labels = collections.Counter(v.split(":")[0] for v in exp.get("blobLabels", {}).values())
    print("==", name, "runId", exp["runId"])
    print("labels", sorted(labels.items()))
    print("domains", sorted(collections.Counter(r["domain"] for r in exp["objectTable"]).items()))
    s = Store.load(exp)
    run = s.get_object(exp["runId"])
    plan = s.get_object(run["planId"])
    print("plan keys", sorted(plan))
    print("nativeContextDigests", plan.get("nativeContextDigests"), "snapshotId", plan.get("snapshotId"))
    for h, lab in exp.get("blobLabels", {}).items():
        if any(t in lab for t in ("universe", "context", "coverage", "scope")):
            try:
                v = s.get_record(h)
                print("record", lab, h[:12], "keys", sorted(v)[:20] if isinstance(v, dict) else type(v).__name__)
            except Exception as exc:  # frames are not records
                print("frame/other", lab, h[:12], type(exc).__name__)
