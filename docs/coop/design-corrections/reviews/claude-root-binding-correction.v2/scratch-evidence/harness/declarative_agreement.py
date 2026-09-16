"""Three-way agreement over the full differential corpus, for the representation claimed:

  (1) the STATED law   -- split on '/', exact segment equality (ordered() / normalize_explicit_root)
  (2) the DECLARATIVE  -- jsonschema validation of the scalar against the selector in the document
  (3) the EARLY GUARD  -- native_evidence_model.admit_unit_roots

All three must decide the same value set, otherwise the schema and the guard claim different
representations. Reports the first disagreements of each kind rather than only a count.
"""
import importlib.util
import itertools
import json
import sys

TREE = sys.argv[1]
OUT = sys.argv[2]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


NV = load('nv', TREE + '/docs/coop/design-corrections/native/native_evidence_model.v2.py')
MAXR = NV.SCHEMAS['$defs']['InternalUnitRootV1']['maxLength']
MAXM = NV.SCHEMAS['$defs']['CanonicalRelativeDirV1']['maxLength']

BASE = {'unitOrdinal': 0, 'languageFamily': 'tsjs', 'languageMode': 'ts-tsconfig',
        'unitKind': 'ts-program', 'markerPath': 'tsconfig.json', 'markerSha256': '0' * 64,
        'recognizerId': 'typescript-config', 'recognizerVersion': 1,
        'provenance': 'DISCOVERED', 'memberPackageRoots': []}


def law_dir(v):
    if v == '' or v.startswith('/') or '\\' in v or '\x00' in v:
        return False
    return not any(s in ('', '.', '..') for s in v.split('/'))


def law_root(v):
    return v == '' or law_dir(v)


def declarative(selector, value):
    try:
        NV.validate_native(selector, value)
        return True
    except Exception:
        return False


def guard_root(v):
    u = dict(BASE)
    u['rootPath'] = v
    try:
        NV.admit_unit_roots([u])
        return True
    except Exception:
        return False


def guard_member(v):
    u = dict(BASE)
    u['rootPath'] = ''
    u['memberPackageRoots'] = [v]
    try:
        NV.admit_unit_roots([u])
        return True
    except Exception:
        return False


def build_corpus():
    alphabet = ['a', '.', '/', '\n', '\\', '\x00']
    corpus = ['']
    for n in range(1, 6):
        for t in itertools.product(alphabet, repeat=n):
            corpus.append(''.join(t))
    corpus.extend(['a\n/../b', 'a\n/./b', 'a/.\n', 'a/..\n', 'a\n/b', 'a/b', 'crates/foo#bar',
                   '.hidden', 'a/.hidden', '..a', 'a..', 'a b', 'deep/a/b/c/d', '...',
                   '\r', 'a\r/../b', 'a /../b', 'a/b\n', 'a' * MAXR, 'a' * (MAXR + 1)])
    return corpus


def main():
    corpus = build_corpus()
    bad = []
    for v in corpus:
        lr = law_root(v) and len(v) <= MAXR
        ld = law_dir(v) and 1 <= len(v) <= MAXM
        dr = declarative('InternalUnitRootV1', v)
        dd = declarative('CanonicalRelativeDirV1', v)
        gr = guard_root(v)
        gm = guard_member(v)
        if not (lr == dr == gr):
            bad.append({'selector': 'InternalUnitRootV1', 'value': v, 'law': lr,
                        'declarative': dr, 'guard': gr})
        if not (ld == dd == gm):
            bad.append({'selector': 'CanonicalRelativeDirV1', 'value': v, 'law': ld,
                        'declarative': dd, 'guard': gm})
    print('corpus size            :', len(corpus))
    print('three-way disagreements:', len(bad))
    for b in bad[:25]:
        print('   %-24s %-16s law=%-6s declarative=%-6s guard=%s'
              % (b['selector'], repr(b['value'])[:16], b['law'], b['declarative'], b['guard']))
    json.dump({'standing': 'Three-way agreement (stated law / declarative selector / early guard) '
                           'over the full differential corpus, INCLUDING declared length bounds.',
               'tree': TREE, 'corpusSize': len(corpus), 'disagreements': len(bad),
               'samples': bad[:40]}, open(OUT, 'w'), indent=1)
    return 0 if not bad else 1


if __name__ == '__main__':
    raise SystemExit(main())
