"""Consumer-B blind reconstruction: run every vector series and emit results."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
OUT = "/tmp/opensip-design-corrections/consumer-b.v1/output"

import cb_vectors as V  # noqa: E402
import cb_workflows as W  # noqa: E402
import cb_gaps as F  # noqa: E402


def main():
    V.series_A()
    G = V.series_B()
    V.series_C(G)
    V.series_D()
    W.build(V.RESULTS)
    W.build_inventory(V.RESULTS)
    F.build(V.RESULTS)

    os.makedirs(os.path.join(OUT, "vectors"), exist_ok=True)
    json.dump(G, open(os.path.join(OUT, "vectors",
                                   "run-descriptor-graph.json"), "w"),
              indent=1, sort_keys=True)
    series = {}
    for r in V.RESULTS:
        series.setdefault(r["id"][0], {"total": 0, "pass": 0})
        series[r["id"][0]]["total"] += 1
        series[r["id"][0]]["pass"] += 1 if r["pass"] else 0
    doc = {"tool": "consumer-b.v1 independent reference (disposable)",
           "series": series,
           "total": len(V.RESULTS),
           "passed": sum(1 for r in V.RESULTS if r["pass"]),
           "results": V.RESULTS}
    json.dump(doc, open(os.path.join(OUT, "vectors",
                                     "vector-results.json"), "w"),
              indent=1, sort_keys=True)
    print(json.dumps(series, sort_keys=True))
    print("TOTAL %d/%d" % (doc["passed"], doc["total"]))
    for r in V.RESULTS:
        if not r["pass"]:
            print(" FAIL", r["id"], r["title"][:80])
            print("   ", json.dumps(r["observed"])[:500])


if __name__ == "__main__":
    main()
