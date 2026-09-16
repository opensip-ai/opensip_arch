"""Independent whole-process trace: records every open/listdir/scandir/subprocess/exec event (all paths), then runs a target script as __main__.
Output goes to fd 2 via os.write (raises no open audit event). Usage: python -I -B trace_run.py TARGET [args...]"""
import os, sys, json, runpy
events = []
def hook(event, args):
    if event in ("open", "os.listdir", "os.scandir", "subprocess.Popen", "os.exec", "os.posix_spawn", "os.system"):
        try:
            a0 = args[0] if args else None
            if isinstance(a0, (bytes, os.PathLike)): a0 = os.fsdecode(a0)
            events.append((event, a0 if isinstance(a0, str) else repr(a0)[:300]))
        except Exception:
            pass
sys.addaudithook(hook)
target = sys.argv[1]
sys.argv = sys.argv[1:]
def dump():
    os.write(2, ("\nTRACE-JSON " + json.dumps(events) + "\n").encode())
import atexit
atexit.register(dump)
runpy.run_path(target, run_name="__main__")
