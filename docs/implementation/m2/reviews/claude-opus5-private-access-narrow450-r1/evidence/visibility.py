"""Compile-time visibility probe for the narrowed predicate (review-directory copy only).

Reviewer-authored (actual Claude Opus 5.5). Appends a sibling module to the COPY's
crates/security/src/lib.rs and runs `cargo check -p opensip-security --lib`:
  V1 candidate + call to assess_private_descendant_capture     -> must compile (control)
  V2 candidate + call to assess_private_descendant (narrowed)  -> must fail, E0603 private
  V3 HEAD 34dcc94/0cf4470 bytes + the same narrowed call        -> compiled before narrowing
Originals are restored and re-verified after every variant.
"""
import hashlib, json, pathlib, subprocess

R = pathlib.Path("/tmp/opensip-implementation/reviews/claude-opus5-private-access-narrow450-r1")
W = R / "work/ws"
LIB = W / "crates/security/src/lib.rs"
MOD = W / "crates/security/src/private_access.rs"
LIB_SHA = "6e0e6115f506c67d951e3336503ee9680ae3ef32a5aaf50f4a04bf2700b63916"
MOD_SHA = "ecb3aa4db7f6b3384afc3c66368f065bdb5de86d14ca212396c806ec68c0717f"
HEAD_MOD_SHA = "e41d0813c063ab1c4db0046a1aacd4e60f2457704b3b0b6cfad3ea6d27f3d069"

CONTROL = """
#[allow(dead_code)]
mod reviewer_visibility_probe {
    fn allowed(capture: &opensip_platform::DescriptorAclCapture) {
        let _ = crate::private_access::assess_private_descendant_capture(
            crate::private_access::PrivateObjectKind::Directory, 0, capture);
    }
}
"""
NARROWED = """
#[allow(dead_code)]
mod reviewer_visibility_probe {
    fn narrowed(metadata: &opensip_platform::DescriptorMetadata) {
        let _ = crate::private_access::assess_private_descendant(
            crate::private_access::PrivateObjectKind::Directory, 0, metadata,
            opensip_platform::CapturedAclState::Entries(0), &[]);
    }
}
"""


def sha(b):
    return hashlib.sha256(b).hexdigest()


def check(name):
    cmd = [str(R / "evidence/replay.sh"), name, str(W), "cargo", "check", "--locked", "--offline", "-p", "opensip-security", "--lib"]
    code = subprocess.run(cmd, env={"TARGET": str(R / "work/target-mut"), "PATH": "/usr/bin:/bin"}).returncode
    err = (R / "evidence/runs" / f"{name}.stderr").read_text()
    return code, [l for l in err.splitlines() if l.startswith("error")]


lib, mod = LIB.read_bytes(), MOD.read_bytes()
assert sha(lib) == LIB_SHA and sha(mod) == MOD_SHA
head_mod = subprocess.run(["git", "-C", "/Users/sb/code/opensip-ai/opensip", "show", "0cf4470:crates/security/src/private_access.rs"],
                          capture_output=True, env={"GIT_OPTIONAL_LOCKS": "0", "PATH": "/usr/bin:/bin"}).stdout
assert sha(head_mod) == HEAD_MOD_SHA
results = []
try:
    for name, module, probe, want in [("vis-V1-candidate-capture-entry-control", mod, CONTROL, "compiles"),
                                      ("vis-V2-candidate-narrowed-fn-from-sibling", mod, NARROWED, "E0603"),
                                      ("vis-V3-head-bytes-narrowed-fn-from-sibling", head_mod, NARROWED, "compiles")]:
        MOD.write_bytes(module)
        LIB.write_bytes(lib + probe.encode())
        code, errors = check(name)
        LIB.write_bytes(lib)
        MOD.write_bytes(mod)
        ok = (code == 0) if want == "compiles" else (code != 0 and any("E0603" in e and "assess_private_descendant" in e for e in errors))
        results.append({"variant": name, "expected": want, "exitCode": code, "errors": errors, "asExpected": ok})
        print(name, code, want, "OK" if ok else "UNEXPECTED", errors[:2], flush=True)
finally:
    LIB.write_bytes(lib)
    MOD.write_bytes(mod)
assert sha(LIB.read_bytes()) == LIB_SHA and sha(MOD.read_bytes()) == MOD_SHA
(R / "evidence/visibility.json").write_text(json.dumps({"restoredAndVerified": True, "results": results}, indent=1) + "\n")
