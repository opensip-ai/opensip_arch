"""Serial compiled-mutant RE-RUN of my 448 set over a COPY of the narrowed predicate (450).

Adapted from the 448 script: new ORIGINAL_SHA, prior verdicts recorded, and a count
of TMPDIR leftovers after each mutant to test the new Drop cleanup guard.
(First run omitted the per-mutant record fields through an adapter slip; corrected and re-run once.)

Reviewer-authored (actual Claude Opus 5.5). Mutates only
R/work/ws/crates/security/src/private_access.rs, a copy of the product's
uncommitted module; the product tree is never written. Each mutant is one exact
single-occurrence replacement, compiled and run with the requested focused
filter, then the original bytes are restored and re-verified.
KILLED = at least one private_access test failed or the mutant did not compile.
SURVIVED = all seven tests still passed.
"""
import hashlib, json, pathlib, subprocess

R = pathlib.Path("/tmp/opensip-implementation/reviews/claude-opus5-private-access-narrow450-r1")
W = R / "work/ws"
MODULE = W / "crates/security/src/private_access.rs"
ORIGINAL_SHA = "ecb3aa4db7f6b3384afc3c66368f065bdb5de86d14ca212396c806ec68c0717f"
PRIOR = {"P01": "KILLED", "P02": "KILLED", "P03": "KILLED", "P04": "SURVIVED", "P05": "KILLED", "P06": "KILLED",
         "P07": "KILLED", "P08": "KILLED", "P09": "KILLED", "P10": "KILLED", "P11": "KILLED", "P12": "KILLED",
         "P13": "KILLED", "P14": "SURVIVED", "P15": "SURVIVED", "P16": "SURVIVED", "P17": "SURVIVED",
         "P18": "KILLED", "P19": "KILLED", "P20": "KILLED"}
TMP = pathlib.Path(R) / "work/tmp"

MUTANTS = [
    ("P01-omission-admitted-as-empty", "admits omission",
     "        CapturedAclState::NotReturned => return Err(PrivateAccessRefusal::AclNotReturned),",
     "        CapturedAclState::NotReturned => 0,"),
    ("P02-sentinel-admitted-as-empty", "admits sentinel",
     "        CapturedAclState::NoAclSentinel => {\n            return Err(PrivateAccessRefusal::AclSentinelUnqualified);\n        }",
     "        CapturedAclState::NoAclSentinel => 0,"),
    ("P03-capture-path-treats-nonentry-as-empty", "entry() None / omission as empty",
     "        return assess_private_descendant(kind, invoking_uid, capture.metadata(), state, &[]);",
     "        return assess_private_descendant(kind, invoking_uid, capture.metadata(), CapturedAclState::Entries(0), &[]);"),
    ("P04-capture-path-skips-missing-entry", "entry() None skipped (count check still guards)",
     "        let Some(entry) = capture.entry(index) else {\n            return Err(PrivateAccessRefusal::InconsistentCapture);\n        };",
     "        let Some(entry) = capture.entry(index) else {\n            continue;\n        };"),
    ("P05-count-check-removed", "entry() None / short slice as empty",
     "    if entries.len() != count {\n        return Err(PrivateAccessRefusal::InconsistentCapture);\n    }\n",
     ""),
    ("P06-group-allow-admitted", "admits foreign allow",
     "            _ => Err(PrivateAccessRefusal::ForeignAclAccess),",
     "            CapturedAclPrincipal::Group(_) => Ok(()),\n            _ => Err(PrivateAccessRefusal::ForeignAclAccess),"),
    ("P07-unresolved-allow-admitted", "admits foreign allow",
     "            _ => Err(PrivateAccessRefusal::ForeignAclAccess),",
     "            CapturedAclPrincipal::Unresolved => Ok(()),\n            _ => Err(PrivateAccessRefusal::ForeignAclAccess),"),
    ("P08-other-user-allow-admitted", "admits foreign allow",
     "            CapturedAclPrincipal::User(uid) if uid == invoking_uid => Ok(()),",
     "            CapturedAclPrincipal::User(_) => Ok(()),"),
    ("P09-inherit-only-allow-exempt", "admits foreign allow",
     "    match entry.flags & ACE_KIND_MASK {",
     "    if entry.flags & (1 << 8) != 0 {\n        return Ok(());\n    }\n    match entry.flags & ACE_KIND_MASK {"),
    ("P10-unknown-kind-accepted", "admits unknown ACE kind",
     "        _ => Err(PrivateAccessRefusal::UnknownAceKind),",
     "        _ => Ok(()),"),
    ("P11-unknown-flags-accepted", "admits unknown ACE flags",
     "    if entry.flags & !KNOWN_ACE_FLAGS != 0 {\n        return Err(PrivateAccessRefusal::UnknownAceFlags);\n    }\n",
     ""),
    ("P12-deny-treated-as-grant", "over-refusal (pins deny acceptance)",
     "        ACE_DENY => Ok(()),",
     "        ACE_DENY => Err(PrivateAccessRefusal::ForeignAclAccess),"),
    ("P13-zero-right-allow-refused", "over-refusal (pins zero-right acceptance)",
     "        ACE_PERMIT if entry.rights == 0 => Ok(()),\n",
     ""),
    ("P14-directory-mode-relaxed-to-no-group-other-bits", "mode exactness",
     "            if file_type != DIRECTORY || permissions != 0o700 {",
     "            if file_type != DIRECTORY || permissions & 0o077 != 0 {"),
    ("P15-file-mode-relaxed-to-no-group-other-bits", "mode exactness",
     "            if file_type != REGULAR || permissions != 0o600 {",
     "            if file_type != REGULAR || permissions & 0o077 != 0 {"),
    ("P16-directory-type-check-removed", "kind/type binding",
     "            if file_type != DIRECTORY || permissions != 0o700 {",
     "            if permissions != 0o700 {"),
    ("P17-file-type-check-removed", "kind/type binding",
     "            if file_type != REGULAR || permissions != 0o600 {",
     "            if permissions != 0o600 {"),
    ("P18-file-link-check-removed", "hard-link aliasing",
     "            if metadata.links != 1 {\n                return Err(PrivateAccessRefusal::LinkCount);\n            }\n",
     ""),
    ("P19-owner-check-removed", "foreign owner",
     "    if metadata.uid != invoking_uid {\n        return Err(PrivateAccessRefusal::ForeignOwner);\n    }\n",
     ""),
    ("P20-known-flags-widened-bit11", "admits unknown ACE flags",
     "    ACE_KIND_MASK | (1 << 4) | (1 << 5) | (1 << 6) | (1 << 7) | (1 << 8) | (1 << 9) | (1 << 10);",
     "    ACE_KIND_MASK | (1 << 4) | (1 << 5) | (1 << 6) | (1 << 7) | (1 << 8) | (1 << 9) | (1 << 10) | (1 << 11);"),
]


def sha(b):
    return hashlib.sha256(b).hexdigest()


def run(name):
    cmd = [str(R / "evidence/replay.sh"), name, str(W), "cargo", "test", "--locked", "--offline",
           "-p", "opensip-security", "--lib", "private_access"]
    env = {"TARGET": str(R / "work/target-mut"), "PATH": "/usr/bin:/bin"}
    code = subprocess.run(cmd, env=env).returncode
    out = (R / "evidence/runs" / f"{name}.stdout").read_text()
    err = (R / "evidence/runs" / f"{name}.stderr").read_text()
    failed = [l.split()[1] for l in out.splitlines() if l.startswith("test ") and l.endswith("FAILED")]
    summary = [l for l in out.splitlines() if l.startswith("test result:")]
    return code, failed, summary, ("error[" in err or "could not compile" in err)


def main():
    original = MODULE.read_bytes()
    assert sha(original) == ORIGINAL_SHA, "copy differs from the reviewed module"
    results = []
    code, failed, summary, _ = run("mut-00-baseline")
    assert code == 0 and not failed, "baseline must pass"
    results.append({"id": "P00-baseline", "exitCode": code, "summary": summary})
    text = original.decode()
    try:
        for ident, cls, old, new in MUTANTS:
            assert text.count(old) == 1, f"{ident}: target must occur exactly once"
            MODULE.write_bytes(text.replace(old, new).encode())
            code, failed, summary, ce = run("mut-" + ident)
            MODULE.write_bytes(original)
            assert sha(MODULE.read_bytes()) == ORIGINAL_SHA
            leftovers = sorted(p.name for p in TMP.iterdir())
            results.append({"id": ident, "defectClass": cls, "exitCode": code,
                            "verdict": "KILLED" if code != 0 else "SURVIVED", "prior448": PRIOR[ident[:3]],
                            "tmpdirLeftovers": leftovers,
                            "compileError": ce, "failedTests": failed, "summary": summary})
            print(ident, PRIOR[ident[:3]], "->", results[-1]["verdict"], "leftovers", len(leftovers), failed or summary, flush=True)
    finally:
        MODULE.write_bytes(original)
    assert sha(MODULE.read_bytes()) == ORIGINAL_SHA
    (R / "evidence/mutants.json").write_text(json.dumps(
        {"moduleSha256": ORIGINAL_SHA, "restoredAndVerified": True, "results": results}, indent=1) + "\n")


if __name__ == "__main__":
    main()
