"""Serial compiled-mutant re-run over a COPY of the 449 capture candidate.

Reviewer-authored (actual Claude Opus 5.5). This re-applies my inventory63 mutant
set (M01-M13; M08/M09 retargeted to the new injectable seams) to measure which
earlier survivors the candidate now kills, plus two public-wrapper bypass mutants.
Mutates only R/work/mut/ws/crates/platform/src/filesystem/descriptor_acl_capture.rs;
the worktree is never written. Each mutant is one exact single-occurrence
replacement, then the original bytes are restored and re-verified.
KILLED = at least one acl_capture_ test failed or the mutant did not compile.
"""
import hashlib, json, pathlib, subprocess

R = pathlib.Path("/tmp/opensip-implementation/reviews/claude-opus5-capture-gaps449-r1")
W = R / "work/mut/ws"
MODULE = W / "crates/platform/src/filesystem/descriptor_acl_capture.rs"
ORIGINAL_SHA = "c057ae14847190652b11dec6a8c42e8d831f6e5752da559b973fea8be7444ebf"
PRIOR = {"M01": "KILLED", "M02": "KILLED", "M03": "SURVIVED", "M04": "KILLED", "M05": "KILLED", "M06": "KILLED",
         "M07": "KILLED", "M08": "SURVIVED", "M09": "SURVIVED", "M10": "SURVIVED", "M11": "SURVIVED",
         "M12": "SURVIVED", "M13": "SURVIVED"}

MUTANTS = [
    ("M01-omission-becomes-empty", "admit absence",
     "        CapturedAclState::NotReturned\n    } else {",
     "        CapturedAclState::Entries(0)\n    } else {"),
    ("M02-sentinel-becomes-empty", "admit absence",
     "            CapturedAclState::NoAclSentinel\n        } else {",
     "            CapturedAclState::Entries(0)\n        } else {"),
    ("M03-omitted-acl-flags-fabricated", "admit absence",
     "        if self.layout.state == CapturedAclState::NotReturned {\n            None",
     "        if self.layout.state == CapturedAclState::NotReturned {\n            Some(0)"),
    ("M04-drop-unknown-right-bits", "drop a right",
     "            rights: word(&self.buffer, offset + 20).ok()?,",
     "            rights: word(&self.buffer, offset + 20).ok()? & 0x01ff_ffff,"),
    ("M05-drop-inheritance-flags", "drop a flag",
     "            flags: word(&self.buffer, offset + 16).ok()?,",
     "            flags: word(&self.buffer, offset + 16).ok()? & 0xf,"),
    ("M06-drop-after-bracket", "skip original-descriptor bracket",
     "    if before != after {\n        return Err(DescriptorAclCaptureError::Changed);\n    }\n    let (layout, principals) = pending?;",
     "    let _ = &after;\n    let (layout, principals) = pending?;"),
    ("M07-syscall-failure-skips-after-bracket", "skip original-descriptor bracket",
     "    let pending = if result != 0 {\n",
     "    if result != 0 {\n        return Err(DescriptorAclCaptureError::Io(io::Error::last_os_error()));\n    }\n    let pending = if result != 0 {\n"),
    ("M08-accounted-native-before-charge", "charge after native work",
     "    work.run(descriptor_acl_capture_cost(), |_| {\n        capture_with(file, call, resolver).map_err(WorkFailure::Operation)\n    })",
     "    let early = capture_with(file, call, resolver);\n    work.run(descriptor_acl_capture_cost(), |_| {\n        early.map_err(WorkFailure::Operation)\n    })"),
    ("M09-reserved-native-before-spend", "charge after native work",
     "    post.scope(|post| {\n        post.spend(descriptor_acl_capture_cost())?;\n        capture_with(file, call, resolver).map_err(WorkFailure::Operation)\n    })",
     "    let early = capture_with(file, call, resolver);\n    post.scope(|post| {\n        post.spend(descriptor_acl_capture_cost())?;\n        early.map_err(WorkFailure::Operation)\n    })"),
    ("M10-remove-128-entry-bound", "decoder bound",
     "            if count > MAX_ENTRIES || length != HEADER_BYTES + count * ENTRY_BYTES {",
     "            if length != HEADER_BYTES + count * ENTRY_BYTES {"),
    ("M11-undercharge-resolver-edges", "accounting",
     "        edges: 3 + MAX_ENTRIES,",
     "        edges: 3,"),
    ("M12-omitted-with-data-accepted", "decoder strictness",
     "        if length != 0 {\n            return Err(malformed(\"omitted ACL has data\"));\n        }\n",
     ""),
    ("M13-unknown-membership-kind-becomes-group", "principal result",
     "        (0, 1) => CapturedAclPrincipal::Group(id),",
     "        (0, _) => CapturedAclPrincipal::Group(id),"),
    ("M14-public-accounted-bypasses-seam", "charge bypass (new seam)",
     "        return capture_accounted_in(file, work, libc::fgetattrlist, resolve_native);",
     "        let _ = work;\n        return capture_with(file, libc::fgetattrlist, resolve_native).map_err(WorkFailure::Operation);"),
    ("M15-public-reserved-bypasses-seam", "spend bypass (new seam)",
     "        return capture_reserved_in(file, post, libc::fgetattrlist, resolve_native);",
     "        let _ = post;\n        return capture_with(file, libc::fgetattrlist, resolve_native).map_err(WorkFailure::Operation);"),
    ("M16-group-kind-becomes-unresolved", "principal result",
     "        (0, 1) => CapturedAclPrincipal::Group(id),",
     "        (0, 1) => CapturedAclPrincipal::Unresolved,"),
]


def sha(b):
    return hashlib.sha256(b).hexdigest()


def run(name):
    cmd = [str(R / "evidence/replay.sh"), name, str(W), "cargo", "test", "--locked", "--offline",
           "-p", "opensip-platform", "--lib", "acl_capture_"]
    env = {"TARGET": str(R / "work/target-mut"), "PATH": "/usr/bin:/bin"}
    code = subprocess.run(cmd, env=env).returncode
    out = (R / "evidence/runs" / f"{name}.stdout").read_text()
    err = (R / "evidence/runs" / f"{name}.stderr").read_text()
    failed = [l.split()[1] for l in out.splitlines() if l.startswith("test ") and l.endswith("FAILED")]
    summary = [l for l in out.splitlines() if l.startswith("test result:")]
    return code, failed, summary, ("error[" in err or "could not compile" in err)


def main():
    original = MODULE.read_bytes()
    assert sha(original) == ORIGINAL_SHA, "copy differs from the candidate"
    results = []
    code, failed, summary, _ = run("mut-00-baseline")
    assert code == 0 and not failed, "baseline must pass"
    results.append({"id": "M00-baseline", "exitCode": code, "summary": summary})
    text = original.decode()
    try:
        for ident, cls, old, new in MUTANTS:
            assert text.count(old) == 1, f"{ident}: target must occur exactly once"
            MODULE.write_bytes(text.replace(old, new).encode())
            code, failed, summary, ce = run("mut-" + ident)
            MODULE.write_bytes(original)
            assert sha(MODULE.read_bytes()) == ORIGINAL_SHA
            verdict = "KILLED" if code != 0 else "SURVIVED"
            results.append({"id": ident, "defectClass": cls, "exitCode": code, "verdict": verdict,
                            "inventory63Verdict": PRIOR.get(ident[:3], "NEW"),
                            "compileError": ce, "failedTests": failed, "summary": summary})
            print(ident, PRIOR.get(ident[:3], "NEW"), "->", verdict, failed or summary, flush=True)
    finally:
        MODULE.write_bytes(original)
    assert sha(MODULE.read_bytes()) == ORIGINAL_SHA
    (R / "evidence/mutants.json").write_text(json.dumps(
        {"moduleSha256": ORIGINAL_SHA, "restoredAndVerified": True, "results": results}, indent=1) + "\n")


if __name__ == "__main__":
    main()
