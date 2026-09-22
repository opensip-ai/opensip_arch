"""Append reviewer_probe.rs to the review-directory copy, run it once, restore.

Reviewer-authored (actual Claude Opus 5.5). Only R/work/ws is modified, and the
original module bytes are restored and re-verified afterwards.
"""
import hashlib, json, pathlib, subprocess, sys

R = pathlib.Path("/tmp/opensip-implementation/reviews/claude-opus5-private-access448-inventory64-r1")
MODULE = R / "work/ws/crates/security/src/private_access.rs"
ORIGINAL_SHA = "e41d0813c063ab1c4db0046a1aacd4e60f2457704b3b0b6cfad3ea6d27f3d069"

# --parse-only re-reads the saved stdout without any native job (used once to fix
# parsing of the first PROBE line, which libtest prefixes with the test name).
PARSE_ONLY = sys.argv[1:] == ["--parse-only"]
original = MODULE.read_bytes()
assert hashlib.sha256(original).hexdigest() == ORIGINAL_SHA
probe = (R / "evidence/reviewer_probe.rs").read_bytes()
code = json.loads((R / "evidence/runs/07-reviewer-native-probe.json").read_text())["exitCode"] if PARSE_ONLY else None
if not PARSE_ONLY:
    try:
        MODULE.write_bytes(original + probe)
        cmd = [str(R / "evidence/replay.sh"), "07-reviewer-native-probe", str(R / "work/ws"), "cargo", "test", "--locked",
               "--offline", "-p", "opensip-security", "--lib", "private_access::reviewer_probe", "--", "--nocapture"]
        code = subprocess.run(cmd, env={"TARGET": str(R / "work/target-mut"), "PATH": "/usr/bin:/bin"}).returncode
    finally:
        MODULE.write_bytes(original)
assert hashlib.sha256(MODULE.read_bytes()).hexdigest() == ORIGINAL_SHA
out = (R / "evidence/runs/07-reviewer-native-probe.stdout").read_text()
rows = [json.loads(l[l.index("PROBE {") + len("PROBE "):]) for l in out.splitlines() if "PROBE {" in l]
summary = [l for l in out.splitlines() if l.startswith("test result:")]
(R / "evidence/probe-results.json").write_text(json.dumps(
    {"exitCode": code, "summary": summary, "moduleRestoredAndVerified": True,
     "probeSourceSha256": hashlib.sha256(probe).hexdigest(), "cases": rows}, indent=1) + "\n")
print(code, summary)
for r in rows:
    print(r)
