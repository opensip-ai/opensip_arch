"""Reviewer-05 mutants: fresh copy of scratch/copy (40 inputs), one seeded defect, check.py -I -B with private TMPDIR/pycache."""
import json, os, shutil, subprocess, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent; SRC = HERE / "copy"
PY = "/tmp/opensip-implementation/metadata-reference-env/bin/python"
def text(name, old, new):
    def f(root):
        s = (root / name).read_text(); assert old in s, (name, old[:80]); (root / name).write_text(s.replace(old, new, 1))
    return f
M = {
 # review-04 survivors, re-seeded against candidate-05 code
 "s4_scope_ne_only": text("tools/owner_successor.py", '        if only is not None and s["id"] not in only:', '        if s["instance"] != "NE" or (only is not None and s["id"] not in only):'),
 "s4_sender_no_payload_bytes": text("tools/sender_ref.py", '                raise _div("payload-bytes", "slot %d: %d!=%d" % (slot, n, s["payloadBytes"]))', '                pass'),
 "s4_sender_no_request_limit": text("tools/sender_ref.py", '            raise _div("request-limit", "%d bytes %d frames" % (total, frames))', '            pass'),
 "s4_remedy_drop_generated_phrase": text("public-route-successor.v1.json", "prepared output site path or generated-file logical path", "prepared output site path"),
 # new
 "n_sender_echo_size_only": text("tools/sender_ref.py", '            if f["payload"] != want:', '            if measured(protocol, accounting, f) > reserve["payloadBytes"]:'),
 "n_sender_ordinal_before_analyze": text("tools/sender_ref.py", 'if slots_consumed > echo["analyzeSlot"] else None', 'if slots_consumed > echo["openUniverseSlot"] else None'),
 "n_prepared_admitted_only": text("tools/representability.py", 'if out["outcome"] not in ("admitted", "fallback-non-prepared"):', 'if out["outcome"] not in ("admitted",):'),
 "n_prepared_count_usable_only": text("tools/representability.py", "    faults = prepared_limit_faults(doc, prepared)\n    if not faults:\n        return dict(out, ownerRan=True, successorRefusal=None, wireLimitBasis=basis)",
                                      "    faults = prepared_limit_faults(doc, dict(prepared, rows=[r for r in prepared['rows']][:len(out.get('usableRows') or prepared['rows'])]))\n    if not faults:\n        return dict(out, ownerRan=True, successorRefusal=None, wireLimitBasis=basis)"),
 "n_entry_bound_off": text("tools/representability.py", '        if name is not None and name in limits and count > int(limits[name]):', '        if False:'),
 "n_scoped_view_all_nodes_ecma": text("tools/owner_successor.py", '            if isinstance(schema, dict) and schema.get(NODE_MARK) is True:', '            if isinstance(schema, dict):'),
 "n_no_relation_row": text("tools/owner_successor.py", 'ROW_DOC_KEYS = ["evidence", "relationRegistry2"]', 'ROW_DOC_KEYS = ["evidence"]'),
 "n_fallback_drops_stale_evidence": text("tools/representability.py", 'outcome="fallback-non-prepared", usableRows=[], successorRefusal=None,', 'outcome="fallback-non-prepared", usableRows=[], staleRows=[], successorRefusal=None,'),
}
res = {}
for name, fn in M.items():
    root = HERE / "mut" / name
    shutil.rmtree(root, ignore_errors=True); shutil.copytree(SRC, root, ignore=shutil.ignore_patterns("tmp", "__pycache__"))
    (root / "tmp" / "pycache").mkdir(parents=True)
    try:
        fn(root)
    except AssertionError as e:
        res[name] = {"seedFailed": str(e)}; print(name, "SEED FAILED", e, flush=True); shutil.rmtree(root); continue
    env = {"PATH": "/usr/bin:/bin", "HOME": "/tmp", "OPENSIP_ARCH": "/Users/sb/code/opensip-ai/opensip_arch", "TMPDIR": str(root / "tmp"),
           "PYTHONDONTWRITEBYTECODE": "1", "PYTHONPYCACHEPREFIX": str(root / "tmp" / "pycache")}
    p = subprocess.run([PY, "-I", "-B", "check.py", "--out", str(root / "tmp" / "r.json")], cwd=root, env=env, capture_output=True, text=True, timeout=900)
    try:
        r = json.loads((root / "tmp" / "r.json").read_text()); failed = [x["id"] for x in r["failures"]]
    except Exception:
        failed = ["NO-RESULT:" + p.stderr[-300:]]
    res[name] = {"failedCount": len(failed), "failed": failed[:10]}; print(name, len(failed), failed[:5], flush=True)
    shutil.rmtree(root)
(HERE / "mutants.out.json").write_text(json.dumps(res, indent=1) + "\n")
