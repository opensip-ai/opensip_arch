"""Read-only probe 2 (prints only): exact retained values that source44 startup payload vectors join, taken from my admitted ts-pass and rust-mixed stores.
Usage: python3 tools/runref.py tools/probe_s44_records2.py
"""
import json
import sys

OUT = "/private/tmp/opensip-design-corrections/consumer-b.v24-source44.v1/output"
sys.path.insert(0, OUT + "/ref")
import canonical as K  # noqa: E402
from store import Store  # noqa: E402

for name in ("ts-pass", "rust-mixed"):
    exp = json.load(open(f"{OUT}/runs/{name}.store.json"))
    s = Store.load(exp)
    run = s.get_object(exp["runId"])
    plan = s.get_object(run["planId"])
    print("==", name, "run.planId", run["planId"], "plan.snapshotId", plan["snapshotId"], "ctx", plan["nativeContextDigests"])
    for h, lab in sorted(exp["blobLabels"].items(), key=lambda kv: kv[1]):
        if lab.startswith("native-universe") or lab.startswith("native-context"):
            try:
                dom, v = s.get_frame(h, {"native.semantic-universe.typescript.v2", "native.semantic-universe.rust.v2",
                                         "native.context.typescript.v2", "native.context.rust.v2"})
            except Exception as exc:
                print("frame parse", lab, type(exc).__name__, exc)
                continue
            print(lab, "domain", dom, "H==key", K.H(dom, v) == h)
            if isinstance(v, dict):
                print("  keys", sorted(v))
                for f in ("nativeContextId", "dependencySourceSetId", "preparedOutputSetId", "preparedResolution", "languageMode", "sourceUnitOwnershipId"):
                    if f in v:
                        print("  ", f, v[f])
    n = 0
    for h, lab in sorted(exp["blobLabels"].items(), key=lambda kv: kv[1]):
        if lab.startswith("coverage-payload") and n < 2:
            v = s.get_record(h)
            print(lab, json.dumps(v["key"]), "entry.keys", sorted(v["entry"]), "coverage", v["entry"]["coverage"], "rc", v["entry"]["resolutionCompleteness"])
            n += 1
print("parse_frame signature:", K.parse_frame.__doc__)
