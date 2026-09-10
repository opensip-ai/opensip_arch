"""Run only the named checks out of check-identity, by executing it once and filtering results.

check-identity is a script whose results accumulate in a module-level list, so a bounded run means
executing it once (~75s) and reading `results`. For iterating on ONE control that is still far too
slow, which is why the discriminating work happens through bounded_loader; this is used sparingly to
confirm named controls in situ."""
import importlib.util,json,sys,pathlib
def run(dc,prefixes):
    argv=sys.argv;sys.argv=['check-identity.py']
    spec=importlib.util.spec_from_file_location('named_check',pathlib.Path(dc)/'foundation/check-identity.py')
    m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m
    try:spec.loader.exec_module(m)
    except SystemExit:pass
    finally:sys.argv=argv
    hits=[r for r in m.results if any(r['id'].startswith(p) for p in prefixes)]
    return m,hits
if __name__=='__main__':
    m,hits=run(sys.argv[1],sys.argv[2:])
    print(json.dumps({'total':len(m.results),'failed':[r['id'] for r in m.results if not r['passed']],
                      'named':hits},indent=1))
