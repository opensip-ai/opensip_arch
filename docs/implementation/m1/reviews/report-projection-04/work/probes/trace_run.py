"""Reviewer whole-process trace (review-04): records open (path, mode, flags), listdir/scandir, subprocess/exec/spawn/fork events for all paths,
then runs the target as __main__. Output via os.write(2) at exit (no open event). Usage: python -I -B -X pycache_prefix=P trace_run.py TARGET args..."""
import os, sys, json, runpy, atexit
events = []
WATCH = ("open", "os.listdir", "os.scandir", "subprocess.Popen", "os.exec", "os.posix_spawn", "os.system", "os.fork", "os.forkpty", "compile", "marshal.loads", "import")
def hook(event, args):
    if event not in WATCH:
        return
    try:
        if event == "open":
            p = args[0]
            p = os.fsdecode(p) if isinstance(p, (bytes, os.PathLike)) else p
            events.append(("open", p if isinstance(p, str) else repr(p)[:80], args[1] if len(args) > 1 else None, args[2] if len(args) > 2 else None))
        elif event == "compile":
            events.append(("compile", str(args[1])[:300] if len(args) > 1 else None, None, None))
        elif event == "marshal.loads":
            events.append(("marshal.loads", None, None, None))
        elif event == "import":
            events.append(("import", str(args[0])[:120], str(args[1])[:300] if len(args) > 1 and args[1] else None, None))
        else:
            a0 = args[0] if args else None
            a0 = os.fsdecode(a0) if isinstance(a0, (bytes, os.PathLike)) else a0
            events.append((event, a0 if isinstance(a0, str) else repr(a0)[:120], None, None))
    except Exception:
        pass
sys.addaudithook(hook)
target = sys.argv[1]
sys.argv = sys.argv[1:]
atexit.register(lambda: os.write(2, ("\nTRACE-JSON " + json.dumps(events) + "\n").encode()))
runpy.run_path(target, run_name="__main__")
