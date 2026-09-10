"""BV6-V5-CR-1 verification: exactly one JSON string value changed, and what that implies for the
registered document digest. Limits: structural diff proves no OTHER value moved; it does not judge
whether the new wording is correct, which is reviewed by reading."""
import hashlib, json, pathlib
B = pathlib.Path('/private/tmp/opensip-design-corrections/bv6-corrections-author.v5/work')
A = pathlib.Path('/private/tmp/opensip-design-corrections/bv6-corrections-author.v6/work')
P = 'docs/coop/design-corrections/native/native-evidence.schemas.v2.json'
b, a = json.loads((B / P).read_text()), json.loads((A / P).read_text())

def walk(o, path=()):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from walk(v, path + (k,))
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from walk(v, path + (i,))
    else:
        yield path, o

fb, fa = dict(walk(b)), dict(walk(a))
changed = [k for k in fb if k in fa and fb[k] != fa[k]]
out = {
 'standing': __doc__, 'file': P,
 'beforeSha256': hashlib.sha256((B / P).read_bytes()).hexdigest(),
 'afterSha256': hashlib.sha256((A / P).read_bytes()).hexdigest(),
 'leafPathsBefore': len(fb), 'leafPathsAfter': len(fa),
 'addedPaths': sorted('/'.join(map(str, k)) for k in set(fa) - set(fb)),
 'removedPaths': sorted('/'.join(map(str, k)) for k in set(fb) - set(fa)),
 'changedPaths': ['/'.join(map(str, k)) for k in changed],
 'exactlyOneStringChanged': len(changed) == 1 and not (set(fa) ^ set(fb))
                            and isinstance(fa[changed[0]], str),
 # the corrected clause must not have disturbed the surrounding law
 'siblingKeysUnchanged': all(fb[k] == fa[k] for k in fb
                             if k[:4] == tuple(changed[0][:4]) and k != changed[0]),
 # registered-document consequence: CoverageResultV3 lives in THIS document, and a Coverage record
 # commits its payload SCHEMA digest, so this document's digest is committed content.
 'definesCoverageResultV3': 'CoverageResultV3' in a.get('$defs', {}),
 'documentDigestChanges': hashlib.sha256((B / P).read_bytes()).hexdigest()
                          != hashlib.sha256((A / P).read_bytes()).hexdigest(),
}
print(json.dumps(out, indent=1))
