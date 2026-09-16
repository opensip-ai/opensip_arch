#!/usr/bin/env python3
"""Reference check of the native wire-carrier AUTHOR candidate; not approval, not a production decoder, not product
qualification.

Run: /tmp/opensip-implementation/metadata-reference-env/bin/python -I -B check.py [--architecture ARCH] [--out check-result.json]
"""
import argparse, json, signal, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "tools"))
from jsonschema import Draft202012Validator  # noqa: E402
import common as CM  # noqa: E402
from check_static import Static  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--architecture", default=CM.ARCH_DEFAULT)
    ap.add_argument("--out", default=str(HERE / "check-result.json"))
    ap.add_argument("--static-only", action="store_true")
    args = ap.parse_args()
    signal.alarm(900)
    st = Static(args.architecture, HERE)
    results = st.run(Draft202012Validator)
    if not args.static_only:
        from check_reference import Reference
        results += Reference(args.architecture, HERE, st).run()
    ids = {r["id"] for r in results}
    for row in st.succ["rows"]:
        for cid in row["referenceChecks"]:
            if cid not in ids:
                results.append({"id": "successor-check-exists:" + cid, "ok": False, "detail": row["id"]})
    failed = [r for r in results if not r["ok"]]
    doc = {"standing": "AUTHOR candidate reference check; not approval, not a production wire decoder, not M2/M3 qualification",
           "checks": len(results), "failed": len(failed), "failures": failed, "results": results}
    Path(args.out).write_text(json.dumps(doc, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"checks": len(results), "failed": len(failed), "failures": failed[:40]}, indent=1, ensure_ascii=False)[:8000])
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
