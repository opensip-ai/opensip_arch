"""source44.v1 setup: rebind this runtime's copied executable helper code from the source43.v1 runtime root to the source44.v1 root.

The root copied my complete source43.v1 output/ byte-for-byte into this runtime. Executable *.py under output/{ref,builders,tools,vectors} and the
unchanged-helper execution copy output/preserved/pre-s42/ still name the source43.v1 absolute root, so running them unchanged would read the source43
kit or write the preserved source43.v1 runtime. This script replaces only that root string (both the /private/tmp and /tmp spellings) and records
every file's sha256 before and after in output/rebind-s44-manifest.json. Exact-bytes history under preserved/ (other than the pre-s42 execution copy)
and the top-level setup scripts of earlier runtimes are not modified and not executed. Refuses to run twice.
Usage: python3 output/rebind_s44.py
"""
import hashlib
import json
import os
import sys

OLD = "/private/tmp/opensip-design-corrections/consumer-b.v24-source43.v1"
OLD_ALT = "/tmp/opensip-design-corrections/consumer-b.v24-source43.v1"
NEW = "/private/tmp/opensip-design-corrections/consumer-b.v24-source44.v1"
OUT = NEW + "/output"
DIRS = ("ref", "builders", "tools", "vectors", "preserved/pre-s42/ref", "preserved/pre-s42/builders", "preserved/pre-s42/tools", "preserved/pre-s42/vectors")


def main():
    if os.path.exists(OUT + "/rebind-s44-manifest.json"):
        print("already rebound; refusing to run twice")
        return 1
    rows = []
    for sub in DIRS:
        base = f"{OUT}/{sub}"
        if not os.path.isdir(base):
            continue
        for name in sorted(os.listdir(base)):
            if not name.endswith(".py"):
                continue
            path = f"{base}/{name}"
            raw = open(path, "rb").read()
            text = raw.decode("utf-8")
            n = text.count(OLD) + text.replace(OLD, "").count(OLD_ALT)
            if not n:
                continue
            new = text.replace(OLD, NEW).replace(OLD_ALT, NEW)
            with open(path, "w") as fh:
                fh.write(new)
            rows.append({"file": f"{sub}/{name}", "beforeSha256": hashlib.sha256(raw).hexdigest(),
                         "afterSha256": hashlib.sha256(new.encode()).hexdigest(), "occurrences": n})
    left = []
    for sub in DIRS:
        base = f"{OUT}/{sub}"
        if os.path.isdir(base):
            left += [f"{sub}/{x}" for x in os.listdir(base) if x.endswith(".py") and "consumer-b.v24-source43.v1" in open(f"{base}/{x}").read()]
    with open(OUT + "/rebind-s44-manifest.json", "w") as fh:
        json.dump({"standing": "runtime-root rebinding of copied executable helper code from source43.v1 to source44.v1; no law, helper logic, claim, "
                               "export or expected result changed; exact-bytes history left untouched", "files": rows,
                   "remainingSource43RootReferences": left}, fh, indent=1)
    print(json.dumps({"rebound": len(rows), "occurrences": sum(r["occurrences"] for r in rows), "remainingSource43RootReferences": left}))
    return 0 if not left else 1


if __name__ == "__main__":
    sys.exit(main())
