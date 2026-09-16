"""Apply single mutations to a scratch copy of the subject tool; run subject tests and reviewer probes."""
import json
import os
import shutil
import subprocess
from pathlib import Path

R = Path(__file__).resolve().parents[1]
SRC = R / 'subject-copy/tools'
SCRATCH = R / 'scratch/mutants'
MUTANTS = {
    'drop manifest/metadata cross-check': ("require(len(observed) == len(set(observed)) and set(observed) == set(declared), ", "(len(observed) == len(set(observed)) and set(observed) == set(declared), "),
    'manifest ignores target tables': ("tables = [(None, document), *document.get('target', {}).items()]", "tables = [(None, document)]"),
    'manifest ignores build-dependencies': ("('build-dependencies', 'build'), ", ""),
    'manifest forbidden edge check removed': ("require(owner in policy[name]['dependencies'], 'forbidden manifest", "(owner in policy[name]['dependencies'], 'forbidden manifest"),
    'manifest optional ignored': ("kind, target, dep.get('optional', False)))", "kind, target, False))"),
    'metadata optional ignored': ("dep.get('target'), dep.get('optional', False)))", "dep.get('target'), False))"),
    'explicit() not called': ("        explicit(manifest_doc)\n", ""),
    'target source check removed': ("require(Path(target['src_path']).resolve(strict=True).is_relative_to", "(Path(target['src_path']).resolve(strict=True).is_relative_to"),
    'registry shadow check removed': ("require(name not in policy, 'registry package shadows", "(name not in policy, 'registry package shadows"),
    'workspace lane allows all': ("else set(policy) - {'opensip-rust-provider'}", "else set(policy)"),
    'workspace root check removed': ("require(Path(metadata['workspace_root']).resolve() == expected_root", "(Path(metadata['workspace_root']).resolve() == expected_root"),
    'resolved forbidden check removed': ("require(b in policy[a]['dependencies'], 'forbidden resolved", "(b in policy[a]['dependencies'], 'forbidden resolved"),
    'external import check removed': ("require(source in local, 'external package", "(source in local, 'external package"),
    'relocation owner check weakened': ("paths.get(manifest.parent) == name and ", "manifest.parent in paths and "),
    'duplicate local owner removed': ("require(name not in local.values(), ", "(name not in local.values(), "),
    'metadata declared forbidden removed': ("require(target in policy[name]['dependencies'], 'forbidden declared", "(target in policy[name]['dependencies'], 'forbidden declared"),
    'metadata pathless internal check removed': ("require(dep['name'] not in policy, 'internal dependency must", "(dep['name'] not in policy, 'internal dependency must"),
    'manifest pathless internal check removed': ("require(owner not in policy, 'internal manifest dependency", "(owner not in policy, 'internal manifest dependency"),
    'manifest package name check removed': ("require(manifest_doc['package']['name'] == name, ", "(manifest_doc['package']['name'] == name, "),
    'local missing from resolve removed': ("require(local.keys() <= nodes.keys(), ", "(local.keys() <= nodes.keys(), "),
    'inventory escape check removed': ("require(path.is_relative_to(repository), ", "(path.is_relative_to(repository), "),
    'aliased owner name check weakened': ("target is not None and target == dep['name']", "target is not None"),
    'manifest owner-path check weakened': ("require(paths.get(path) == owner, ", "(paths.get(path) == owner, "),
    'manifest rename ignored (alias->owner)': ("found.append((owner, alias, ", "found.append((owner, owner, "),
    'workspace inheritance check removed': ("require(value.get('workspace') is not True, ", "(value.get('workspace') is not True, "),
    'empty workspace allowed': ("require(bool(workspace_names) and workspace_names <= allowed", "require(workspace_names <= allowed"),
    'default member check removed': ("require(set(metadata['workspace_default_members']) <= set(workspace_ids)", "(set(metadata['workspace_default_members']) <= set(workspace_ids)"),
}
SCRATCH.mkdir(parents=True, exist_ok=True)
out = []
for name, (old, new) in MUTANTS.items():
    d = SCRATCH / ''.join(c if c.isalnum() else '-' for c in name)
    shutil.rmtree(d, ignore_errors=True)
    shutil.copytree(SRC, d / 'tools')
    tool = d / 'tools/check_package_edges.py'
    text = tool.read_text()
    assert text.count(old) == 1, name
    tool.write_text(text.replace(old, new))
    env = {**os.environ, 'TMPDIR': str(R / 'scratch')}
    unit = subprocess.run(['python3', '-m', 'unittest', 'discover', '-s', str(d / 'tools/tests')], capture_output=True, text=True, env=env)
    probe = subprocess.run(['python3', str(R / 'probes/probe_real_cargo.py')], capture_output=True, text=True, env={**env, 'TOOL': str(tool)})
    failed = [x['case'] for x in json.loads(probe.stdout)['results'] if not x['asExpected']]
    out.append({'mutant': name, 'killedBySubjectTests': unit.returncode != 0, 'reviewerProbesDetecting': failed})
    shutil.rmtree(d)
print(json.dumps(out, indent=1))
