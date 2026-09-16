
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
