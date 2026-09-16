"""Reviewer-04 mutants: copy scratch/copy (39 declared inputs, tmp excluded) to mut/<name>, seed one defect, run check.py
with -I -B, own TMPDIR and pycache prefix; record failing ids (0 = uncaught)."""
import json, os, shutil, subprocess, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent; SRC = HERE / "copy"
PY = "/tmp/opensip-implementation/metadata-reference-env/bin/python"
def text(name, old, new):
    def f(root):
        s = (root / name).read_text(); assert old in s, (name, old[:70]); (root / name).write_text(s.replace(old, new, 1))
    return f
M = {
 "m_patch_native_C_only_not_IM": text("tools/owner_successor.py", "    for C in _canonical_modules(mod):", "    for C in [getattr(mod, 'C')] if hasattr(mod, 'C') else []:"),
 "m_correction_token_noop": text("tools/owner_successor.py", 'CORRECT_TOKEN = "(?![\\\\s\\\\S]*("', 'CORRECT_TOKEN = "(?!.*("'),
 "m_sender_no_payload_bytes_check": text("tools/sender_ref.py", '                raise _div("payload-bytes", "slot %d: %d!=%d" % (slot, n, s["payloadBytes"]))', '                pass'),
 "m_sender_no_cancel_reserve_check": text("tools/sender_ref.py", 'if reserve is None or n > reserve["payloadBytes"]:', 'if reserve is None:'),
 "m_sender_no_seal_count_check": text("tools/sender_ref.py", '                raise _div("seal-count", "slot %d" % slot)', '                pass'),
 "m_sender_no_request_limit_recheck": text("tools/sender_ref.py", 'if totals and (total > int(limits["maxRequestPayloadBytesTotal"]) or frames > int(limits["maxRequestFrames"])):', 'if False:'),
 "m_fallback_keeps_partial_rows": text("tools/representability.py", 'outcome="fallback-non-prepared", usableRows=[],', 'outcome="fallback-non-prepared",'),
 "m_phase_a_prepared_explicit_only": text("tools/representability.py", "    phase_a = prepared_path_faults(NE, doc, prepared)\n", "    phase_a = prepared_path_faults(NE, doc, prepared) if explicit_prepared_mode else []\n"),
 "m_remedy_drop_generated_phrase": text("public-route-successor.v1.json", "prepared output site path or generated-file logical path", "prepared output site path"),
 "m_cancel_reserve_zero_bytes_in_totals": text("tools/representability.py", '        self._count("Cancel", n, None, record=False)', '        self._count("Cancel", 0, None, record=False)'),
}
res = {}
for name, fn in M.items():
    if sys.argv[1:] and name not in sys.argv[1:]: continue
    root = HERE / "mut" / name
    shutil.rmtree(root, ignore_errors=True); shutil.copytree(SRC, root, ignore=shutil.ignore_patterns("tmp", "__pycache__"))
    (root / "tmp" / "pycache").mkdir(parents=True)
    try:
        fn(root)
    except AssertionError as e:
        res[name] = {"seedFailed": str(e)}; print(name, "SEED FAILED", e); shutil.rmtree(root); continue
    env = {"PATH": "/usr/bin:/bin", "HOME": os.environ.get("HOME", ""), "OPENSIP_ARCH": "/Users/sb/code/opensip-ai/opensip_arch",
           "TMPDIR": str(root / "tmp"), "PYTHONDONTWRITEBYTECODE": "1", "PYTHONPYCACHEPREFIX": str(root / "tmp" / "pycache")}
    p = subprocess.run([PY, "-I", "-B", "check.py", "--out", str(root / "tmp" / "check-result.json")], cwd=root, env=env, capture_output=True, text=True, timeout=900)
    try:
        r = json.loads((root / "tmp" / "check-result.json").read_text()); failed = [f["id"] for f in r["failures"]]
    except Exception as exc:  # noqa: BLE001
        failed = ["NO-RESULT:" + p.stderr[-300:]]
    res[name] = {"failedCount": len(failed), "failed": failed[:10]}
    print(name, len(failed), failed[:5], flush=True)
    shutil.rmtree(root)
(HERE / "mutants.out.json").write_text(json.dumps(res, indent=1) + "\n")
