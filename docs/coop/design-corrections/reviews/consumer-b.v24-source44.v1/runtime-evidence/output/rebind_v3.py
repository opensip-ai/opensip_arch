"""source42.v3 setup: rebind this runtime's copied executable helper code from the source42.v2 runtime root to the source42.v3 root.

The root copied the complete source42.v2 output/ byte-for-byte into this runtime. Executable *.py under output/{ref,builders,tools,vectors}
and the unchanged-helper execution copy output/preserved/pre-s42/ still name the v2 absolute root, so running them unchanged would read or
write the preserved v2 runtime. This script replaces only that root string (both the /private/tmp and /tmp spellings) and records every
file's sha256 before and after in output/rebind-v3-manifest.json. Exact-bytes history (preserved/s42-original-state, preserved/source41-v1,
output/port_and_preserve.py, output/rebind_v2.py) is not modified and is not executed. Refuses to run twice.
Usage: python3 output/rebind_v3.py
"""
import hashlib
import json
import os
import sys

OLD = "/private/tmp/opensip-design-corrections/consumer-b.v24-source42.v2"
OLD_ALT = "/tmp/opensip-design-corrections/consumer-b.v24-source42.v2"
NEW = "/private/tmp/opensip-design-corrections/consumer-b.v24-source42.v3"
OUT = NEW + "/output"
DIRS = ("ref", "builders", "tools", "vectors", "preserved/pre-s42/ref", "preserved/pre-s42/builders", "preserved/pre-s42/tools", "preserved/pre-s42/vectors")


def main():
    if os.path.exists(OUT + "/rebind-v3-manifest.json"):
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
            left += [f"{sub}/{x}" for x in os.listdir(base) if x.endswith(".py") and OLD_ALT in open(f"{base}/{x}").read()]
    with open(OUT + "/rebind-v3-manifest.json", "w") as fh:
        json.dump({"standing": "runtime-root rebinding of copied executable helper code from source42.v2 to source42.v3; no law, helper logic, claim, "
                               "export or expected result changed; exact-bytes history left untouched", "files": rows, "remainingV2RootReferences": left}, fh, indent=1)
    print(json.dumps({"rebound": len(rows), "occurrences": sum(r["occurrences"] for r in rows), "remainingV2RootReferences": left}))
    return 0 if not left else 1


if __name__ == "__main__":
    sys.exit(main())
