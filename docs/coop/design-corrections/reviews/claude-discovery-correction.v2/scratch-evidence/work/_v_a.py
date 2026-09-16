
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
