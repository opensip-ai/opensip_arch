"""Reference SemVer/schema checks; no production resolver or signing claim."""
import copy
import functools
import hashlib
import json
from pathlib import Path
import re
from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError
B = Path(__file__).resolve().parent
SHA = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
SCHEMA = json.loads((B / 'version-constraint-schema.completed.v1.json').read_text())
VALIDATOR = Draft202012Validator(SCHEMA)

def version(v):
    if not re.fullmatch(SCHEMA['oneOf'][0]['pattern'], v):
        raise ValueError('SEMVER')
    main = v.split('+', 1)[0]
    core, sep, pre = main.partition('-')
    return tuple(int(x) for x in core.split('.')), pre.split('.') if sep else []

def compare(a, b):
    ac, ap = version(a); bc, bp = version(b)
    if ac != bc: return (ac > bc) - (ac < bc)
    if not ap or not bp: return (not ap) - (not bp)
    for x, y in zip(ap, bp):
        if x == y: continue
        if x.isdigit() and y.isdigit(): return (int(x) > int(y)) - (int(x) < int(y))
        if x.isdigit() != y.isdigit(): return -1 if x.isdigit() else 1
        return (x > y) - (x < y)
    return (len(ap) > len(bp)) - (len(ap) < len(bp))

def satisfies(v, constraint):
    try:
        VALIDATOR.validate(constraint); core, pre = version(v)
        if isinstance(constraint, str): return v == constraint
        low, high = compare(v, constraint['min']), compare(v, constraint['max'])
        if compare(constraint['min'], constraint['max']) > 0: return False
        if pre and not any(version(constraint[k])[0] == core and version(constraint[k])[1] for k in ('min', 'max')):
            return False
        return (low > 0 or low == 0 and constraint['includeMin']) and (high < 0 or high == 0 and constraint['includeMax'])
    except (ValueError, TypeError, ValidationError):
        # This reference checker refuses malformed inputs. Assertions in run still propagate.
        return False

def run():
    cases = json.loads((B / 'compatibility-design-cases.v1.json').read_text())
    results=[]
    for case in cases['versions']:
        try: version(case['input']); actual=True
        except ValueError: actual=False
        assert actual == case['expected'], case
        results.append({'id':case['id'],'passed':True})
    for case in cases['comparisons']:
        actual=compare(*case['input']); assert actual == case['expected'], case
        results.append({'id':case['id'],'passed':True})
    for case in cases['constraints']:
        actual=satisfies(case['version'],case['constraint']); assert actual == case['expected'], case
        results.append({'id':case['id'],'passed':True})
    lock_schema=json.loads((B/'component-lock-schema.completed.v1.json').read_text())
    Draft202012Validator.check_schema(lock_schema)
    validator=Draft202012Validator(lock_schema)
    for case in cases['locks']:
        actual=validator.is_valid(case['input']);assert actual==case['expected'],case['id']
        results.append({'id':case['id'],'passed':True})
    matrix=json.loads((B/'compatibility-matrix.completed.v1.json').read_text())
    assert len(matrix['rows'])==8
    assert {r['id'] for r in matrix['rows']}=={'S-CORE','S-SCHEMA','S-CTRL','S-TS1','S-RUST2','S-ROLE','S-STATE','S-EVIDENCE'}
    assert sum(r['previewActive'] for r in matrix['rows'])==5
    report={'kind':'compatibility-design-check','productQualification':False,'count':len(results),'passed':len(results),'matrixSurfaces':8,'results':results,'pins':{p.name:SHA(p) for p in [Path(__file__),B/'compatibility-design-cases.v1.json',B/'component-lock-schema.completed.v1.json',B/'version-constraint-schema.completed.v1.json',B/'compatibility-matrix.completed.v1.json']},'limitations':['No production dependency solver, signature admission, release artifact or platform execution.','Exact schema checks do not establish semantic closure or trust.']}
    (B/'compatibility-design-report.v1.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'count':len(results),'passed':len(results)}))
if __name__=='__main__':run()
