
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
