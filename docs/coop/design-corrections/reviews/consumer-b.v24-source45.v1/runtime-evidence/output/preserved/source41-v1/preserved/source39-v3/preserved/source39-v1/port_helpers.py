"""Port this origin's own prior helper code into the source39 runtime, rebinding paths.

Copies every *.py under the prior runtime's output/{ref,builders,tools,vectors} into this output tree, replacing the prior runtime root
with this runtime root. Nothing else is copied: prior vectors, runs, reports and checkpoints stay in the read-only prior runtime and are
never treated as current results. Writes output/port-manifest.json with source/destination SHA-256 per file.
Usage: python3 output/port_helpers.py
"""
import hashlib
import json
import os

OLD = "/private/tmp/opensip-design-corrections/consumer-b.v24"
OLD_ALT = "/tmp/opensip-design-corrections/consumer-b.v24"
NEW = "/private/tmp/opensip-design-corrections/consumer-b.v24-source39.v1"
rows = []
for sub in ("ref", "builders", "tools", "vectors"):
    src_dir = f"{OLD_ALT}/output/{sub}"
    if not os.path.isdir(src_dir):
        continue
    for name in sorted(os.listdir(src_dir)):
        if not name.endswith(".py"):
            continue
        raw = open(os.path.join(src_dir, name), "rb").read()
        text = raw.decode("utf-8")
        ported = text.replace(OLD + "/", NEW + "/").replace(OLD_ALT + "/", NEW + "/").replace(f"'{OLD}'", f"'{NEW}'").replace(f'"{OLD}"', f'"{NEW}"')
        dst_dir = f"{NEW}/output/{sub}"
        os.makedirs(dst_dir, exist_ok=True)
        open(os.path.join(dst_dir, name), "w").write(ported)
        rows.append({"source": f"{OLD_ALT}/output/{sub}/{name}", "sourceSha256": hashlib.sha256(raw).hexdigest(),
                     "destination": f"output/{sub}/{name}", "destinationSha256": hashlib.sha256(ported.encode()).hexdigest(),
                     "pathRebindings": text.count(OLD) + text.count(OLD_ALT) - text.count(OLD_ALT) * 0})
json.dump({"standing": "own prior helper code of origin 9d3dfb70-b2d3-498c-a3c1-f8de9e488514, rebound to the source39 runtime; prior results are not current evidence",
           "files": rows}, open(f"{NEW}/output/port-manifest.json", "w"), indent=1)
print(len(rows), "files ported")
