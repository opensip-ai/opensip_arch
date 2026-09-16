"""Independent identity/filesystem counterexamples on a private mutant copy."""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

CARGO = "/opt/homebrew/Cellar/rust/1.95.0/bin/cargo"
REVIEW = Path("/tmp/opensip-implementation/m2-grok-foundation-primitives-selection-v1-review/review")
SRC = REVIEW / "copy" / "frozen-subject" / "product"
MUTANT = REVIEW / "copy" / "mutant-product"
SAFE_PATH = "/opt/homebrew/Cellar/rust/1.95.0/bin:/usr/bin:/bin:/usr/sbin:/sbin"

IDENTITY_PROBE = r'''
use crate::{canonical, digests, JsonValue};

#[test]
fn grok_wrong_expected_domain_is_frame_domain_not_inferred() {
    let value = canonical::parse(b"null").unwrap();
    let frame = digests::frame("native.context.rust.v2", &value).unwrap();
    assert_eq!(
        digests::unframe("native.context.rust.v2", &frame),
        Ok(JsonValue::Null)
    );
    assert_eq!(
        digests::unframe("run", &frame),
        Err(digests::Error::FrameDomain)
    );
    assert_eq!(
        digests::unframe("native.context.rust.v20", &frame),
        Err(digests::Error::FrameDomain)
    );
    assert_eq!(
        digests::unframe("native.context.rust", &frame),
        Err(digests::Error::FrameDomain)
    );
}

#[test]
fn grok_declared_length_mismatch_and_truncation_refuse() {
    let frame = digests::frame("run", &canonical::parse(br#"{"a":1}"#).unwrap()).unwrap();
    for n in 0..frame.len() {
        assert!(digests::unframe("run", &frame[..n]).is_err(), "truncation {n}");
    }
    let offset = b"opensip.product.v1\0run\0".len();
    let mut huge = frame.clone();
    huge[offset..offset + 8].copy_from_slice(&u64::MAX.to_be_bytes());
    assert_eq!(digests::unframe("run", &huge), Err(digests::Error::FrameLength));
    let mut short = frame.clone();
    short[offset..offset + 8].copy_from_slice(&0u64.to_be_bytes());
    assert_eq!(digests::unframe("run", &short), Err(digests::Error::FrameLength));
}

#[test]
fn grok_noncanonical_but_admitted_json_refuses() {
    fn wrap(payload: &[u8]) -> alloc::vec::Vec<u8> {
        let mut bytes = b"opensip.product.v1\0run\0".to_vec();
        bytes.extend_from_slice(&(payload.len() as u64).to_be_bytes());
        bytes.extend_from_slice(payload);
        bytes
    }
    for payload in [b" true".as_slice(), b"true ", br#"{"b":1,"a":0}"#, br#""\u0041""#] {
        assert!(canonical::parse(payload).is_ok(), "{payload:?}");
        assert_eq!(
            digests::unframe("run", &wrap(payload)),
            Err(digests::Error::FrameNoncanonical)
        );
    }
}
'''

FILESYSTEM_PROBE = r'''
    #[test]
    fn grok_flags_readonly_cloexec_nonblock() {
        let tree = Tree::new();
        fs::write(tree.0.join("f"), b"abc").unwrap();
        let f = tree.handle().open_regular("f").unwrap();
        let status = unsafe { libc::fcntl(f.as_raw_fd(), libc::F_GETFL) };
        let fdflags = unsafe { libc::fcntl(f.as_raw_fd(), libc::F_GETFD) };
        assert!(status >= 0 && fdflags >= 0);
        assert_eq!(status & libc::O_ACCMODE, libc::O_RDONLY);
        assert_ne!(fdflags & libc::FD_CLOEXEC, 0);
        assert_ne!(status & libc::O_NONBLOCK, 0);
        drop(f);
    }

    #[test]
    fn grok_symlink_fifo_dir_and_traversal_refuse() {
        let tree = Tree::new();
        fs::create_dir(tree.0.join("d")).unwrap();
        fs::write(tree.0.join("d/f"), b"ok").unwrap();
        symlink("d/f", tree.0.join("link")).unwrap();
        let handle = tree.handle();
        assert!(handle.open_regular("link").is_err());
        assert!(handle.open_regular("d").is_err());
        assert!(handle.open_regular("../d/f").is_err());
        assert!(handle.open_regular("/d/f").is_err());
        assert!(handle.open_regular("d//f").is_err());
        let fifo = CString::new(tree.0.join("fifo").as_os_str().as_encoded_bytes()).unwrap();
        assert_eq!(unsafe { libc::mkfifo(fifo.as_ptr(), 0o600) }, 0);
        assert!(handle.open_regular("fifo").is_err());
    }

    #[test]
    fn grok_retained_fd_survives_root_rename_and_leaf_symlink() {
        let tree = Tree::new();
        fs::create_dir(tree.0.join("root")).unwrap();
        fs::write(tree.0.join("root/file"), b"pinned").unwrap();
        fs::create_dir(tree.0.join("other")).unwrap();
        fs::write(tree.0.join("other/file"), b"other").unwrap();
        let handle = RetainedDirectory::from_retained_handle(File::open(tree.0.join("root")).unwrap()).unwrap();
        fs::rename(tree.0.join("root"), tree.0.join("kept")).unwrap();
        symlink("other", tree.0.join("root")).unwrap();
        let mut opened = handle.open_regular("file").unwrap();
        fs::rename(tree.0.join("kept/file"), tree.0.join("kept/old")).unwrap();
        symlink("../other/file", tree.0.join("kept/file")).unwrap();
        assert!(handle.open_regular("file").is_err());
        let mut text = String::new();
        opened.read_to_string(&mut text).unwrap();
        assert_eq!(text, "pinned");
    }
'''


def env_for(target: Path) -> dict[str, str]:
    env = {
        "HOME": os.environ["HOME"],
        "PATH": SAFE_PATH,
        "CARGO_TARGET_DIR": str(target),
        "CARGO_TERM_COLOR": "never",
        "CARGO_HOME": os.environ.get("CARGO_HOME", str(Path(os.environ["HOME"]) / ".cargo")),
        "TMPDIR": "/tmp/osip-m2g",
        "TERM": "dumb",
    }
    sdk = os.environ.get("SDKROOT")
    if not sdk:
        try:
            sdk = subprocess.check_output(
                ["/usr/bin/xcrun", "--sdk", "macosx", "--show-sdk-path"], text=True
            ).strip()
        except (OSError, subprocess.CalledProcessError):
            sdk = None
    if sdk:
        env["SDKROOT"] = sdk
    return env


def main() -> None:
    if not sys.flags.isolated or sys.flags.optimize:
        raise SystemExit("isolated Python without optimization required")
    Path("/tmp/osip-m2g").mkdir(exist_ok=True)
    if MUTANT.exists():
        shutil.rmtree(MUTANT)
    shutil.copytree(
        SRC,
        MUTANT,
        ignore=shutil.ignore_patterns("target", "node_modules", "python-packages", "__pycache__"),
    )
    ident = MUTANT / "crates/identity/src/grok_probes.rs"
    ident.write_text(IDENTITY_PROBE)
    lib = MUTANT / "crates/identity/src/lib.rs"
    text = lib.read_text()
    if "mod grok_probes" not in text:
        text = text.replace("mod canonical_tests;", "mod canonical_tests;\nmod grok_probes;")
        lib.write_text(text)
    fs = MUTANT / "crates/platform/src/filesystem.rs"
    fs_text = fs.read_text()
    needle = "        assert_eq!(text, \"pinned\");\n    }\n}\n"
    if "grok_flags_readonly_cloexec_nonblock" not in fs_text:
        if needle not in fs_text:
            raise SystemExit("filesystem test insertion point missing")
        fs.write_text(fs_text.replace(needle, "        assert_eq!(text, \"pinned\");\n    }\n" + FILESYSTEM_PROBE + "}\n"))
    target = REVIEW / "probes" / "mutant-target"
    if target.exists():
        shutil.rmtree(target)
    target.mkdir(parents=True)
    env = env_for(target)
    ident_run = subprocess.run(
        [CARGO, "test", "--locked", "--offline", "-p", "opensip-identity", "grok_"],
        env=env, cwd=MUTANT, capture_output=True, text=True, timeout=180,
    )
    fs_run = subprocess.run(
        [CARGO, "test", "--locked", "--offline", "-p", "opensip-platform", "grok_"],
        env=env, cwd=MUTANT, capture_output=True, text=True, timeout=180,
    )
    (REVIEW / "results" / "logs" / "identity-probes.stdout").write_text(ident_run.stdout)
    (REVIEW / "results" / "logs" / "identity-probes.stderr").write_text(ident_run.stderr)
    (REVIEW / "results" / "logs" / "filesystem-probes.stdout").write_text(fs_run.stdout)
    (REVIEW / "results" / "logs" / "filesystem-probes.stderr").write_text(fs_run.stderr)
    out = {
        "identityExit": ident_run.returncode,
        "identityStdout": ident_run.stdout,
        "identityStderrTail": ident_run.stderr[-500:],
        "filesystemExit": fs_run.returncode,
        "filesystemStdout": fs_run.stdout,
        "filesystemStderrTail": fs_run.stderr[-500:],
        "passed": ident_run.returncode == 0 and fs_run.returncode == 0,
    }
    (REVIEW / "results" / "counterexamples.json").write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "identityExit": ident_run.returncode,
        "filesystemExit": fs_run.returncode,
        "passed": out["passed"],
        "identityTail": ident_run.stdout[-600:],
        "fsTail": fs_run.stdout[-600:],
        "identErr": ident_run.stderr[-400:],
        "fsErr": fs_run.stderr[-400:],
    }, indent=2))


if __name__ == "__main__":
    main()
