This directory was a full rsync copy of the repository `docs/` tree, used only because
`native/check_native_evidence.v2.py` and `security/check-security-lifecycle.v1.py` verify
root-owned source pins that root refreshes AFTER this handoff, and because the native checker
writes its report before it checks those pins.

Reproduce with:

    rsync -a --exclude .git docs <sandbox>/
    cd <sandbox>
    python -I -B docs/coop/design-corrections/native/check_native_evidence.v2.py --regenerate-pins
    python -I -B docs/coop/design-corrections/native/check_native_evidence.v2.py
    # security has no --regenerate-pins; rewrite source-pins.v1.json sha256 fields from the copy
    python -I -B docs/coop/design-corrections/security/check-security-lifecycle.v1.py --report <out>

No pin in the repository was changed. The regenerated pin files from this sandbox are retained
beside this directory as native-sandbox-regenerated-pins.v2.json and
security-sandbox-regenerated-pins.v1.json so the runs can be audited without the 459M tree.
