"""Create this runtime's regular-file work source from v1/source, verified against root's partial capture.

1. Reads root's partial-public-artifact-manifest.json (digest printed) and the frozen source38 manifest (digest pinned).
2. For every manifest entry whose runtimePath is under `source/`, verifies the v1 file: an entry with `sha256` must
   match it; an entry with `sameAsSubjectPath` must match that path's source38 manifest digest. Any v1 source file
   with no entry, any missing file and any unknown entry shape is a failure.
3. Only if all of that holds: copies v1/source to ./source with shutil.copy2 (regular files, no links, no
   __pycache__) and re-hashes the copy against v1. Also copies v1's runner.py, run_checks.py, copy_source.py and
   probes/*.py that do not already exist here. Never writes into v1.
Usage: copy_v1.py [--verify-only]
"""
import hashlib
import json
import os
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
V1 = Path("/private/tmp/opensip-design-corrections/claude-consumer24-native-author.v1")
PARTIAL = Path("/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/"
               "claude-consumer24-native-author.v1-partial/partial-public-artifact-manifest.json")
SUBJECT = Path("/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v38.json")
SUBJECT_SHA = "2ddfa0dbfc101b264c24d2a1f63de1e4e70908ac2a7346eaf0dab09d37f7e5c5"


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


partial_raw = PARTIAL.read_bytes()
subject_raw = SUBJECT.read_bytes()
if hashlib.sha256(subject_raw).hexdigest() != SUBJECT_SHA:
    raise SystemExit("source38 manifest digest mismatch")
partial = json.loads(partial_raw)
subject = {f["path"]: f for f in json.loads(subject_raw)["files"]}
entries = [e for e in partial["files"] if str(e.get("runtimePath", "")).startswith("source/")]
faults, unknown = [], []
expected = {}
for e in entries:
    rel = e["runtimePath"][len("source/"):]
    if "sha256" in e:
        expected[rel] = e["sha256"]
    elif "sameAsSubjectPath" in e and e["sameAsSubjectPath"] in subject:
        expected[rel] = subject[e["sameAsSubjectPath"]]["sha256"]
    else:
        unknown.append(e)
present = set()
for d, dirs, files in os.walk(V1 / "source"):
    dirs[:] = [x for x in dirs if x != "__pycache__"]
    for name in files:
        present.add(os.path.relpath(os.path.join(d, name), V1 / "source"))
missing = sorted(set(expected) - present)
unlisted = sorted(present - set(expected))
for rel in sorted(set(expected) & present):
    if sha(V1 / "source" / rel) != expected[rel]:
        faults.append(rel)
summary = {"partialManifestSha256": hashlib.sha256(partial_raw).hexdigest(), "partialEntriesUnderSource": len(entries),
           "v1SourceFiles": len(present), "digestMismatches": faults, "missingInV1": missing,
           "unlistedInV1": unlisted[:20], "unlistedCount": len(unlisted), "unknownEntryShapes": unknown[:3],
           "sampleEntry": entries[:1]}
ok = not faults and not missing and not unlisted and not unknown and len(entries) > 0
summary["v1MatchesRootCapture"] = ok
if not ok or "--verify-only" in sys.argv:
    print(json.dumps(summary, indent=1))
    raise SystemExit(0 if ok else 1)
dest = HERE / "source"
if dest.exists():
    raise SystemExit("destination source/ already exists")
shutil.copytree(V1 / "source", dest, symlinks=False, copy_function=shutil.copy2,
                ignore=shutil.ignore_patterns("__pycache__"))
copy_faults = []
for rel in sorted(present):
    p = dest / rel
    if p.is_symlink() or not p.is_file() or os.stat(p).st_nlink > 1 or sha(p) != expected[rel]:
        copy_faults.append(rel)
copied_tools = []
for rel in ["runner.py", "run_checks.py", "copy_source.py"] + [str(p.relative_to(V1)) for p in sorted((V1 / "probes").glob("*.py"))]:
    target = HERE / rel
    if not target.exists():
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(V1 / rel, target)
        copied_tools.append({"path": rel, "sha256": sha(target)})
summary.update({"copiedFiles": len(present), "copyFaults": copy_faults, "copiedTools": copied_tools})
print(json.dumps(summary, indent=1))
raise SystemExit(1 if copy_faults else 0)
