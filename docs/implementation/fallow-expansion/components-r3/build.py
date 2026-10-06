"""Build FX-COMP-1 insertion and exact subject; no acceptance or product writes."""
import argparse
import hashlib
import json
from pathlib import Path

ARCH = Path(__file__).resolve().parents[4]
BASE = 'docs/implementation/fallow-expansion/components-r3/'
PARENT = 'docs/v2/contracts/product-v1/native-evidence.md'


def raw(path):
    return (ARCH / path).read_bytes()


def pin(path, value=None):
    value = raw(path) if value is None else value
    return {'path': path, 'bytes': len(value), 'sha256': hashlib.sha256(value).hexdigest()}


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode()


def build(lock_path):
    lock = json.loads(lock_path.read_bytes())
    for binding in lock['contractSuccessors']:
        record = json.loads(raw(binding['record']['path']))
        for entry in record.get('passageOverrides', []) + record.get('passageSupersessions', []):
            assert not (entry['parent']['path'] == PARENT and entry['selector'] == {'line': 2777}), 'insertion selector changed; rebuild lineage'
    before = raw(PARENT).decode().splitlines()[2776]
    contract = raw(BASE + 'CONTRACT.md').decode()
    after = before + '\n\n### Shared original-source extraction model (FX-COMP-1)\n\n'
    after += ('The following exact source model is selected for staged Vue/Svelte/Astro/CSS adapter design. '
              'It is an extraction intermediate only; existing native capability cells, grammars, '
              'public fault routes and facts remain unchanged until their own reviewed adapter '
              'successors select a bridge. Its schema, pure reference and fixtures are the candidate '
              'members of FX-COMP-1.\n\n')
    after += '\n'.join(contract.splitlines()[4:])
    outputs = {BASE + 'PASSAGES.md': ('# FX-COMP-1 exact insertion\n\nParent line2777.\n\nBefore:\n~~~text\n' + before + '\n~~~\nAfter:\n~~~text\n' + after + '\n~~~\n').encode()}
    names = ['CONTRACT.md', 'component-source-model.schema.json', 'reference.py', 'fixtures.json', 'check.py', 'build.py']
    candidates = [pin(BASE + name) for name in names] + [pin(path, value) for path, value in outputs.items()]
    record = {'schemaVersion': 1, 'standing': 'PROPOSED FX-COMP-1 shared original-source model: native insertion only, no adapter capability or grammar selection; independent acceptance and root assent required',
              'parents': [pin(PARENT)],
              'passageOverrides': [{'parent': pin(PARENT), 'selector': {'line': 2777}, 'before': before, 'after': after}],
              'candidates': sorted(candidates, key=lambda row: row['path'])}
    outputs[BASE + 'successor.json'] = encoded(record)
    manifest = {'schemaVersion': 1, 'files': sorted(candidates + [pin(BASE + 'successor.json', outputs[BASE + 'successor.json'])], key=lambda row: row['path'])}
    outputs[BASE + 'subject.json'] = encoded(manifest)
    return outputs


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--lock', type=Path, default=Path('/Users/sb/code/opensip-ai/opensip-fx-design/design-lock.json'))
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    for path, value in build(args.lock).items():
        target = ARCH / path
        if args.check:
            assert target.read_bytes() == value, path
        else:
            target.write_bytes(value)
    print('FX-COMP-1 exact subject checked' if args.check else 'FX-COMP-1 proposed subject built')
