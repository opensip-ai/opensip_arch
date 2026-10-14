from pathlib import Path
import json, os, shutil, subprocess, tempfile, time, inspect
# Q0 §9.2 cold reset (harness/DESIGN.md:798-801), applied by the U-5a cold runner variants before EVERY run, warmups
# included: (1) delete the project's OpenSIP state (asserted absent; none is ever created) and the disposable analyzer
# caches (each run gets a fresh empty private 0700 TMPDIR under the set's TMPDIR; the previous run's is deleted first);
# (2) the caller then starts a new process; (3) record the OS page-cache state (vm_stat). The page cache is never
# claimed flushed. Label: "cold OpenSIP state, page cache recorded".
RECORDS = []; _current = [None]
STATE = Path('/Users/sb/Library/Application Support/OpenSIP')
def _vm_stat():
    raw = subprocess.check_output(['/usr/bin/vm_stat']).decode(); parsed = {}
    for line in raw.splitlines()[1:]:
        if ':' in line:
            k, v = line.split(':', 1); v = v.strip().rstrip('.')
            if v.isdigit(): parsed[k.strip()] = int(v)
    page = int(raw.splitlines()[0].split('page size of ')[1].split(' ')[0])
    return dict(raw=raw, pageSizeBytes=page, fileBackedPages=parsed.get('File-backed pages'), purgeablePages=parsed.get('Pages purgeable'), freePages=parsed.get('Pages free'))
def reset(env, set_tmpdir):
    caller = inspect.stack()[1]
    assert not STATE.exists()
    if _current[0] is not None: shutil.rmtree(_current[0])
    d = Path(tempfile.mkdtemp(prefix='cold-run-', dir=set_tmpdir)); d.chmod(0o700); _current[0] = d; env['TMPDIR'] = str(d)
    RECORDS.append(dict(index=len(RECORDS), callSiteLine=caller.lineno, monotonicNanos=time.monotonic_ns(), openSIPStateAbsent=True, runTMPDIR=str(d), runTMPDIREmpty=not any(d.iterdir()), pageCache=_vm_stat()))
def write(directory):
    if _current[0] is not None: shutil.rmtree(_current[0]); _current[0] = None
    Path(directory, 'cold-reset-records.json').write_text(json.dumps(dict(standing='Q0 9.2 COLD RESET RECORDS (U-5a); cold OpenSIP state, page cache recorded, never claimed flushed', records=RECORDS), indent=1) + '\n')
