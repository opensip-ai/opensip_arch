"""Generate/check selected contracts after independent design binding.

Explicit maintenance command. It provisions no packages and builds no tools.
The reviewed checkout containing this entry point is the developer trust anchor.
"""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import os
import sys

HERE = Path(__file__).resolve().parent


def module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def generate(args):
    if not sys.flags.isolated or sys.flags.optimize:
        raise ValueError('isolated Python without optimization required')
    # Only reviewed entry-point siblings execute before the supplied root is
    # admitted. A --root checkout cannot choose a replacement preflight module.
    verifier = module(HERE / 'verify_design.py', 'design_preflight')
    admission = module(HERE / 'contracts/admission.py', 'generator_admission')
    root = args.root.resolve(strict=True)
    lock = verifier.decode(admission.local(root, 'design-lock.json').read_bytes())
    approval = verifier.verify(args.architecture.resolve(strict=True), lock, root)
    registry, sources, recipes, registry_sha = admission.registry(root)
    if len(recipes) != 1 or recipes[0][0]['recipeId'] != 'contracts-v1':
        raise ValueError('exact contracts-v1 recipe required')
    recipe, options = recipes[0]
    if set(recipe['sourceSha256s']) != set(sources):
        raise ValueError('recipe source set differs from registry')
    closure_raw = admission.checked(root, 'tools/contracts/generator-closure.json', recipe['generatorClosureSha256'])
    # A registry self-hash alone is not review authority. Require these exact
    # manifest bytes to be a selected input of a verified architecture unit.
    accepted = [row for unit in approval.get('contractSuccessors', []) for row in unit['inputs']]
    if not any(row['sha256'] == recipe['generatorClosureSha256'] and row['bytes'] == len(closure_raw) for row in accepted):
        raise ValueError('generator closure is not selected by an accepted design unit')
    closure = verifier.decode(closure_raw)
    admission.closed(closure, ['schemaVersion', 'profile', 'files', 'toolchain'], 'generator closure')
    if type(closure['schemaVersion']) is not int or closure['schemaVersion'] != 1 or closure['profile'] != 'opensip-contracts-macos-development-2':
        raise ValueError('unselected generator closure profile')
    admission.sorted_unique([row['path'] for row in closure['files']], 'generator input paths')
    pinned = {}
    for row in closure['files']:
        admission.closed(row, ['path', 'bytes', 'sha256'], 'generator input pin')
        raw = admission.checked(root, row['path'], row['sha256'])
        if type(row['bytes']) is not int or len(raw) != row['bytes']:
            raise ValueError('generator input length differs')
        pinned[row['path']] = raw
    required = {'tools/generate_contracts.py', 'tools/verify_design.py', 'tools/build_contracts.py',
                'tools/contracts/pipeline.py', 'tools/contracts/admission.py', 'tools/contracts/adapter.py',
                'tools/contracts/options.json', 'tools/contracts/toolchain.json', 'tools/contracts/build-receipt.json',
                'schemas/source-map.json', 'schemas/profiles/report-codec.json',
                'schemas/wire/native-carriers-v1.json', 'schemas/wire/native-carriers-meta.schema.json'}
    if not required <= pinned.keys() or 'schemas/registry.json' in pinned or 'tools/contracts/generator-closure.json' in pinned:
        raise ValueError('generator closure omits required input or has recursive registry/closure pin')
    if pinned['tools/generate_contracts.py'] != Path(__file__).read_bytes():
        raise ValueError('entry point differs from selected closure')
    toolchain = verifier.decode(pinned['tools/contracts/toolchain.json'])['executables']
    if toolchain != closure['toolchain'] or set(toolchain) != {'node', 'generator', 'python'}:
        raise ValueError('toolchain input set differs')
    adapter = module(HERE / 'contracts/adapter.py', 'generator_adapter')
    adapter.validate_build_receipt(verifier.decode(pinned['tools/contracts/build-receipt.json']), pinned, toolchain['generator'])
    if recipe['optionsPath'] != 'tools/contracts/options.json' or pinned[recipe['optionsPath']] != admission.local(root, recipe['optionsPath']).read_bytes():
        raise ValueError('options closure join differs')
    # Pipeline imports no repository module until its byte snapshot is complete.
    # Selected helper bytes must also equal this trusted entry-point checkout.
    for name in ('pipeline.py', 'admission.py', 'adapter.py'):
        if pinned['tools/contracts/' + name] != (HERE / 'contracts' / name).read_bytes():
            raise ValueError('entry-point helper differs from selected closure')
    pipeline = module(HERE / 'contracts/pipeline.py', 'selected_pipeline')
    # The macOS framework reports a launcher in sys.executable. Admit the
    # explicit child interpreter through the same pinned toolchain as Node/Rust.
    result = pipeline.run(args, selected_closure=closure['files'], provenance={
        'registrySha256': registry_sha, 'generatorClosureSha256': recipe['generatorClosureSha256']})
    output_root = args.output.resolve(strict=True) / result['outputRoot']
    expected = {row['path'] for row in recipe['outputs']}
    actual = admission.collect_outputs(output_root, expected)
    existing = set()
    for parent in {str(Path(name).parent) for name in expected}:
        directory = admission.local(root, parent, existing=False)
        if directory.exists():
            for path in directory.rglob('*'):
                if path.is_symlink() or not path.is_file():
                    raise ValueError('unexpected generated directory member')
                existing.add(path.relative_to(root).as_posix())
    if existing - expected:
        raise ValueError('undeclared generated output present')
    changed = [name for name, raw in actual.items() if name not in existing or admission.local(root, name).read_bytes() != raw]
    if args.write:
        # Per-file replacement after complete collection, not a multi-file
        # transaction. A subsequent check detects interruption between members.
        for name in sorted(changed):
            path = admission.local(root, name, existing=False)
            path.parent.mkdir(parents=True, exist_ok=True)
            temporary = path.with_name('.' + path.name + '.new')
            fd = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o644)
            try:
                with os.fdopen(fd, 'wb') as stream:
                    stream.write(actual[name])
                os.replace(temporary, path)
            finally:
                if temporary.exists():
                    temporary.unlink()
    receipt = {'passed': args.write or not changed, 'sourceSchemasVerified': approval['generationSources']['sourcesVerified'],
               'generatorClosureSelected': True, 'outputs': len(actual), 'changed': sorted(changed), 'write': args.write,
               'standing': 'Selected development generation/drift check only; not semantic admission or release qualification'}
    (args.output / 'selection-result.json').write_text(json.dumps(receipt, indent=2) + '\n')
    return receipt


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=HERE.parent)
    parser.add_argument('--architecture', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True, help='Fresh work directory for logs and staged outputs')
    parser.add_argument('--node', type=Path, required=True)
    parser.add_argument('--generator', type=Path, required=True)
    parser.add_argument('--python', type=Path, required=True, help='Selected child interpreter; framework launcher aliases are not interchangeable')
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    result = generate(args)
    print(json.dumps(result))
    sys.exit(0 if result['passed'] else 1)
