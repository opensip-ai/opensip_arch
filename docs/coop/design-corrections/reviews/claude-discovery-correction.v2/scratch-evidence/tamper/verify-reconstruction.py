"""Portable reconstruction verifier for the Claude XA-01 + XA-02/CR-25 correction.

Replaces the v1 reproduce.sh, which was NOT runnable as advertised. Three defects, all reproduced:
  1. it invoked WORK/apply-correction.py and WORK/stages/*.json without ever copying the bundled
     scripts or stage files into WORK;
  2. it used mkdir -p, so it would happily write into a populated directory;
  3. it replayed development edit stages instead of applying the authored result.
Root also asked whether the pre-copy of successor was redundant because the XA-01 applier owns
creation. Verified: it does NOT. apply-reference-correction.py reads (copy/rel) and asserts it equals
the source bytes, so it REQUIRES an existing tree; with a missing --copy it exits 1 with
FileNotFoundError. Evidence: evidence/xa01-applier-behaviour/. The pre-copy was correct.

This verifier applies the AUTHORED FULL FILES as an exact overlay, so the audit package and the XA-01
applier are no longer dependencies at all: the authored bytes already contain the XA-01 result.

Order: verify every bundled artifact against the manifest, then verify every before-hash against the
frozen source, then overlay, then verify every after-hash, then run the suites. Nothing is written
outside the new output root, and the frozen source is only ever read.
"""
import argparse, hashlib, json, os, shutil, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--frozen-source", type=Path, required=True, help="frozen candidate25 root; read only")
    ap.add_argument("--out", type=Path, required=True, help="NEW output root; must not already exist")
    ap.add_argument("--interpreter", default=sys.executable, help="python 3.12 with jsonschema")
    ap.add_argument("--skip-suites", action="store_true")
    args = ap.parse_args()
    if args.out.exists():
        raise SystemExit("REFUSED: output root already exists: %s" % args.out)
    src = args.frozen_source.resolve()
    if not (src / "docs").is_dir():
        raise SystemExit("REFUSED: frozen source has no docs/ tree: %s" % src)
    out = args.out.resolve()
    if str(out) == str(src) or str(out).startswith(str(src) + os.sep) or str(src).startswith(str(out) + os.sep):
        raise SystemExit("REFUSED: output root overlaps the frozen source")

    manifest = json.loads((HERE / "artifact-manifest.json").read_text())
    print("STEP 1  verify bundled artifacts against the deliverable manifest")
    bad = []
    for row in manifest["files"]:
        p = HERE / row["path"]
        if not p.exists():
            bad.append((row["path"], "missing")); continue
        if sha(p) != row["sha256"]:
            bad.append((row["path"], "sha256 mismatch"))
    if bad:
        for r in bad: print("   BAD", r)
        raise SystemExit("REFUSED: %d bundled artifacts do not match the manifest" % len(bad))
    print("        %d artifacts verified" % len(manifest["files"]))

    changed = json.loads((HERE / "changed-source.json").read_text())["files"]
    print("STEP 2  verify every before-hash against the frozen source (no writes)")
    pre = []
    for row in changed:
        o = src / row["path"]
        if not o.exists():
            pre.append((row["path"], "absent in frozen source")); continue
        got = sha(o)
        if got != row["beforeSha256"]:
            pre.append((row["path"], "before %s got %s" % (row["beforeSha256"][:12], got[:12])))
        full = HERE / "changed-files" / row["path"]
        if not full.exists():
            pre.append((row["path"], "authored full file not bundled")); continue
        if sha(full) != row["afterSha256"]:
            pre.append((row["path"], "bundled full file does not match its afterSha256"))
    if pre:
        for r in pre: print("   BAD", r)
        raise SystemExit("REFUSED: %d before-hash or bundle checks failed; nothing was written" % len(pre))
    print("        %d files: frozen before-hashes and bundled after-hashes agree" % len(changed))

    print("STEP 3  copy the frozen source into the new output root")
    tree = out / "successor"
    shutil.copytree(src, tree)
    print("        copied to %s" % tree)

    print("STEP 4  exact full-file overlay")
    rows = []
    for row in changed:
        target = tree / row["path"]
        before = sha(target)
        if before != row["beforeSha256"]:
            raise SystemExit("REFUSED: copy drifted for %s" % row["path"])
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            target.chmod(target.stat().st_mode | 0o200)
        shutil.copyfile(HERE / "changed-files" / row["path"], target)
        after = sha(target)
        if after != row["afterSha256"]:
            raise SystemExit("REFUSED: overlay produced %s for %s" % (after[:12], row["path"]))
        rows.append({"path": row["path"], "beforeSha256": before, "afterSha256": after})
        print("        %-70s %s to %s" % (row["path"], before[:12], after[:12]))
    (out / "overlay-report.json").write_text(json.dumps({
        "standing": "reconstruction of an AUTHORED correction; not acceptance, not qualification",
        "frozenSource": str(src), "files": rows}, indent=2) + chr(10))

    if sha(src / changed[0]["path"]) != changed[0]["beforeSha256"]:
        raise SystemExit("REFUSED: the frozen source changed during the run")
    print("        frozen source re-checked: unwritten")

    if args.skip_suites:
        print("STEP 5  skipped by request"); return
    print("STEP 5  run the applicable suites and the control set")
    D = tree / "docs/coop/design-corrections"
    reports = out / "reports"; reports.mkdir()
    jobs = [
        ("security", [str(D / "security/check-security-lifecycle.v1.py"), "--report", str(reports / "security.json")], D / "security"),
        ("native", [str(D / "native/check_native_evidence.v2.py"), "--report", str(reports / "native-run.json")], D / "native"),
        ("integration", [str(D / "check-integration.py"), "--report", str(reports / "integration.json")], D),
        ("foundation-identity", [str(D / "foundation/check-identity.py"), "--report", str(reports / "foundation-identity.json")], D / "foundation"),
    ]
    failures = []
    for name, argv, cwd in jobs:
        r = subprocess.run([args.interpreter, "-I", "-B"] + argv, capture_output=True, text=True, cwd=str(cwd))
        head = [l for l in r.stdout.strip().splitlines() if l]
        print("        %-20s rc=%d %s" % (name, r.returncode, (head[0][:150] if head else "")))
        if r.returncode != 0: failures.append(name)
    ctl = HERE / "controls-xa02-cr25.v2.py"
    r = subprocess.run([args.interpreter, "-I", "-B", str(ctl), "--source", str(tree), "--out", str(reports / "controls.json")], capture_output=True, text=True)
    tail = [l for l in r.stdout.strip().splitlines() if l]
    print("        %-20s rc=%d %s" % ("controls", r.returncode, (tail[-1] if tail else "")))
    if r.returncode != 0: failures.append("controls")
    if failures:
        raise SystemExit("RECONSTRUCTION FAILED in: %s" % ", ".join(failures))
    print("RECONSTRUCTED. Reference results only; no product qualification and no acceptance.")


if __name__ == "__main__":
    main()
