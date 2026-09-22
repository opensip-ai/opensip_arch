"""Validate the recommended tests for O1 on the review-directory copy only.

Reviewer-authored (actual Claude Opus 5.5). Runs `cargo test ... private_access::reviewer_recommended`
with recommended_tests.rs appended to (1) the unmodified candidate and (2) each of the
surviving mutants P15/P16/P17. Expected: candidate passes; every mutant is killed.
The module copy is restored and re-verified after every run.
"""
import hashlib, json, pathlib, subprocess

R = pathlib.Path("/tmp/opensip-implementation/reviews/claude-opus5-private-access-narrow450-r1")
W = R / "work/ws"
MOD = W / "crates/security/src/private_access.rs"
MOD_SHA = "ecb3aa4db7f6b3384afc3c66368f065bdb5de86d14ca212396c806ec68c0717f"
MUTANTS = {
    "P15-file-mode-relaxed-to-no-group-other-bits": (
        "            if file_type != REGULAR || permissions != 0o600 {",
        "            if file_type != REGULAR || permissions & 0o077 != 0 {"),
    "P16-directory-type-check-removed": (
        "            if file_type != DIRECTORY || permissions != 0o700 {",
        "            if permissions != 0o700 {"),
    "P17-file-type-check-removed": (
        "            if file_type != REGULAR || permissions != 0o600 {",
        "            if permissions != 0o600 {"),
}


def sha(b):
    return hashlib.sha256(b).hexdigest()


def run(name):
    cmd = [str(R / "evidence/replay.sh"), name, str(W), "cargo", "test", "--locked", "--offline", "-p", "opensip-security",
           "--lib", "private_access::reviewer_recommended"]
    code = subprocess.run(cmd, env={"TARGET": str(R / "work/target-mut"), "PATH": "/usr/bin:/bin"}).returncode
    out = (R / "evidence/runs" / f"{name}.stdout").read_text()
    return code, [l for l in out.splitlines() if l.startswith("test ")]


original = MOD.read_bytes()
assert sha(original) == MOD_SHA
extra = (R / "evidence/recommended_tests.rs").read_bytes()
text = original.decode()
results = []
try:
    variants = [("rec-00-candidate", text)] + [
        ("rec-" + k, text.replace(old, new)) for k, (old, new) in MUTANTS.items() if text.count(old) == 1]
    assert len(variants) == 4
    for name, body in variants:
        MOD.write_bytes(body.encode() + extra)
        code, lines = run(name)
        MOD.write_bytes(original)
        results.append({"variant": name, "exitCode": code, "tests": lines})
        print(name, code, lines, flush=True)
finally:
    MOD.write_bytes(original)
assert sha(MOD.read_bytes()) == MOD_SHA
ok = results[0]["exitCode"] == 0 and all(r["exitCode"] != 0 for r in results[1:])
(R / "evidence/recommended-results.json").write_text(json.dumps(
    {"recommendedTestsSha256": sha(extra), "candidatePassesAndAllSurvivorsKilled": ok,
     "restoredAndVerified": True, "results": results}, indent=1) + "\n")
print("candidate passes and P15/P16/P17 killed:", ok)
