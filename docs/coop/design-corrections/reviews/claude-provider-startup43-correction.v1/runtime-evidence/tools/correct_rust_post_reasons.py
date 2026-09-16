"""Correct a constructor mistake of author_startup_docs.py (receipt 10 kept as recorded).

author_startup_docs.py built the rust-semantic post-Analyze Unavailable reason set from the SHARED
native-evidence.schemas.v2.json UnavailableReasonV3 enum, which also carries node-modules-outside-read-set.
That member is added by native-evidence 9.4 for typescript-semantic only; section 9.2 lists the rust-semantic
additions as native-context-mismatch, dependency-source-incomplete, prepared-output-stale,
prepared-output-not-inert, capability-missing and identity-version-mismatch. The rust set is therefore the
inherited UnavailableV2 reasons plus those six, minus native-context-mismatch (pre-Analyze only).

usage: correct_rust_post_reasons.py <work-candidate-root>
"""
import hashlib
import json
import sys
from pathlib import Path

root = Path(sys.argv[1])
path = root / "docs" / "coop" / "design-corrections" / "native" / "provider-startup.schemas.v1.json"
rust = json.loads((root / "docs" / "coop" / "artifacts" / "rust-provider-protocol.v2.json").read_text(encoding="utf-8"))
raw = path.read_bytes()
doc = json.loads(raw)
assert (json.dumps(doc, indent=2, ensure_ascii=False) + "\n").encode("utf-8") == raw, "formatting not reproducible"
SECTION_92_ADDITIONS = ["native-context-mismatch", "dependency-source-incomplete", "prepared-output-stale",
                        "prepared-output-not-inert", "capability-missing", "identity-version-mismatch"]
inherited = rust["wireSchema"]["payloadSchemas"]["UnavailableV2"]["fields"]["reason"].split("|")
corrected = sorted((set(inherited) | set(SECTION_92_ADDITIONS)) - {"native-context-mismatch"})
before = doc["$defs"]["UnavailableV3"]["properties"]["reason"]["enum"]
doc["$defs"]["UnavailableV3"]["properties"]["reason"]["enum"] = corrected
doc["x-opensip-startup-law"]["postAnalyzeReasons"]["rust-semantic"] = corrected
out = (json.dumps(doc, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
path.write_bytes(out)
print(json.dumps({"before": before, "after": corrected, "removed": sorted(set(before) - set(corrected)),
                  "beforeSha256": hashlib.sha256(raw).hexdigest(), "afterSha256": hashlib.sha256(out).hexdigest()}))
