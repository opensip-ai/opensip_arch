"""Cross-implementation vectors for the analysis path's upward selection (M3-B r5 item 13; unit B2-b3a).

Developer tool only. Each case is a tree description that the security test suite materializes under a scratch
home and selects over natively (`project_admission_upward_tests.rs`). This tool turns the same description into
SLM's synthetic `fs` and runs B2-b0, the current discovery reference (contract successor 164), at its accepted
architecture bytes, and writes or checks crates/security/src/custody/discovery_upward_vectors.json: for an accepted
selection, the upward provenance (mode, configPath, walked, stopReason, vcs, explicitPathWasSymlink) and the
selected root; for a refusal, its code, path, detail and the rows walked before it.

The description-to-`fs` mapping is the observation adapter, and it is the only place this tool decides anything:
  * Paths are under the account home `/H`. The invoking user is 1000; every entry is owned by 1000, or by 1001
    when the case is `foreign` (the native test then selects as a uid other than the owner's). Every entry's
    group is 50, the scratch tree's own group; `groups` authorizes 50 (`own`) or 60 (`other`).
  * An ACL write grant (`acl`) to another user is `uid:1001`; to another group, `group:70`.
  * A directory's `vcs` is the first present of `.git`, `.hg`, `.svn` and `.jj` (B2-b3 plan r2, LD-B2B3-7): a
    directory is `true`; a regular `.git` file is an indirection whose target is its one `gitdir:` line (with an
    optional LF or CRLF end) when S3 file custody admits it, and null otherwise; any other marker is an indirection
    with a null target. The custody verdict is the bound model's own `_file_custody` over the file's `fs` entry, with
    no owner waiver (r2, Codex B2B3A-R1-RF-1); the adapter decides only the line grammar.
No case needs an unreadable ACL, a mount, the filesystem root or the 256-level walk bound: a scratch tree cannot hold
them (the retained path from `/` is itself bounded at 256 components, X2 item 9, so a launch that deep refuses at its
open), and they stay with the reference's own cases and the suite's own controls. SLM imports canonical.py, which imports jsonschema; the tool loads the
provisioned snapshot only after every file matches its generator-closure pin. No filesystem tree, network or
environment input.
"""
from pathlib import Path
import argparse
import copy
import hashlib
import importlib.util
import json
import sys

OUTPUT = 'crates/security/src/custody/discovery_upward_vectors.json'
REF = 'docs/implementation/m3/config-discovery-b/b2-b-reference/'
# Architecture inputs (contract successor 164 and its parents): path, bytes, SHA-256.
ARCH = (
    (REF + 'reference/discovery_scan_reference.py', 12574, '6714575ccee1474e2d7c20c4e5e9b6c95b498ad155ec1e69fc9d6ba5f3e7e32b'),
    ('docs/coop/design-corrections/security/discovery-cases.v1.json', 152804, '2b3f9fdbe99313f75b8545b53c62011a4533bcef4593149aa70b84bddf5303b3'),
)
UPWARD = ('mode', 'configPath', 'walked', 'stopReason', 'vcs', 'explicitPathWasSymlink')
HOME = '/H'
MARKERS = ('.git', '.hg', '.svn', '.jj')
MAX_CONFIG_BYTES = 4 * 1024 * 1024


def require(condition, message):
    if not condition:
        raise ValueError(message)


def pinned(root, path, size, digest):
    raw = (root / path).read_bytes()
    require(len(raw) == size and hashlib.sha256(raw).hexdigest() == digest, 'input pin mismatch: ' + path)
    return raw


def packages(product, packages_root):
    closure = json.loads((product / 'tools/contracts/generator-closure.json').read_bytes())
    rows = [r for r in closure['files'] if r['path'].startswith('tools/contracts/python-packages/')]
    require(rows, 'no pinned python packages')
    for row in rows:
        pinned(packages_root, row['path'], row['bytes'], row['sha256'])
    sys.path.insert(0, str(packages_root / 'tools/contracts/python-packages'))


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def d(rel, mode='0755', **opts):
    return dict(kind='dir', path=rel, mode=mode, **opts)


def f(rel, mode='0644', text='{}', **opts):
    return dict(kind='file', path=rel, mode=mode, text=text, **opts)


def big(rel, size, mode='0644', **opts):
    return dict(kind='file', path=rel, mode=mode, size=size, **opts)


def link(rel, target):
    return dict(kind='symlink', path=rel, target=target)


def fifo(rel):
    return dict(kind='fifo', path=rel, mode='0644')


def case(id_, tree, launch='', explicit=None, waive=False, foreign=False, groups=None):
    return dict(id=id_, tree=tree, launch=launch, explicit=explicit, waive=waive, foreign=foreign, groups=groups)


def cases():
    """The native-materializable upward cases: SLM's upward-only discovery cases that a scratch tree can hold (by
    their reference ids), then the rows, stops and VCS evidence the analysis path records."""
    repo = [d('repo')]
    out = [
        case('cwd-owned-by-other-user-refuses', [d('repo')], launch='repo', foreign=True),
        case('cwd-writable-by-others-refuses', [d('open', '0777')], launch='open'),
        case('sticky-shared-directory-as-cwd-refuses', [d('shared', '1777')], launch='shared'),
        case('group-writable-own-cwd-refuses-before-reading-planted-config', [d('repo', '0775'), f('repo/opensip.json')], launch='repo'),
        case('config-group-writable-refuses-not-skips', repo + [f('repo/opensip.json', '0664')], launch='repo'),
        case('config-symlink-refuses', repo + [link('repo/opensip.json', '/etc/hosts')], launch='repo'),
        case('config-hard-linked-refuses', repo + [f('repo/opensip.json', hardlink=True)], launch='repo'),
        case('config-over-4-mib-refuses', repo + [big('repo/opensip.json', MAX_CONFIG_BYTES + 1)], launch='repo'),
        case('explicit-foreign-owner-without-flag-refuses', [d('checkout')], explicit='checkout', foreign=True),
        case('trust-project-owner-never-waives-other-writable', [d('checkout', '0777')], explicit='checkout', waive=True, foreign=True),
        case('trust-project-owner-never-waives-config-group-write', [d('checkout'), f('checkout/opensip.json', '0664')], explicit='checkout', waive=True, foreign=True),
        case('explicit-path-absent-refuses', repo, explicit='repo/absent'),
        case('explicit-path-is-a-file-refuses', repo + [f('repo/opensip.json')], explicit='repo/opensip.json'),
        case('group-writable-own-directory-refuses-without-explicit-group-authorization', [d('repo', '0775')], launch='repo'),
        case('group-writable-directory-authorized-for-a-different-group-refuses', [d('repo', '0775')], launch='repo', groups='other'),
        case('acl-write-grant-to-another-user-on-directory-refuses-mode-bits-alone-insufficient', [d('repo', acl='user'), f('repo/opensip.json', '0600')], launch='repo'),
        case('acl-write-grant-to-another-group-on-config-file-refuses', repo + [f('repo/opensip.json', acl='group')], launch='repo'),
        # Further refusals.
        case('cwd-absent', [], launch='absent'),
        case('config-fifo-is-not-a-regular-file', repo + [fifo('repo/opensip.json')], launch='repo'),
        case('config-directory-is-not-a-regular-file', repo + [d('repo/opensip.json')], launch='repo'),
        case('config-acl-before-hard-link', repo + [f('repo/opensip.json', acl='user', hardlink=True)], launch='repo'),
        case('config-acl-before-size', repo + [big('repo/opensip.json', MAX_CONFIG_BYTES + 1, acl='group')], launch='repo'),
        case('config-hard-link-before-size', repo + [big('repo/opensip.json', MAX_CONFIG_BYTES + 1, hardlink=True)], launch='repo'),
        # Accepted selections: rows, stops and evidence.
        case('home-boundary-without-candidate', [d('code'), d('code/project')], launch='code/project'),
        case('home-as-launch', [], launch=''),
        case('config-at-an-ancestor', repo + [f('repo/opensip.json'), d('repo/sub')], launch='repo/sub'),
        case('config-with-a-vcs-directory', repo + [d('repo/.git'), f('repo/opensip.json')], launch='repo'),
        case('config-with-a-gitdir-file', repo + [f('repo/.git', text='gitdir: /elsewhere/.git/worktrees/repo\n'), f('repo/opensip.json')], launch='repo'),
        case('vcs-git-directory-from-below', repo + [d('repo/.git'), d('repo/src'), d('repo/src/inner')], launch='repo/src/inner'),
        case('vcs-hg-directory', repo + [d('repo/.hg')], launch='repo'),
        case('vcs-svn-directory', repo + [d('repo/.svn')], launch='repo'),
        case('vcs-jj-directory', repo + [d('repo/.jj')], launch='repo'),
        case('vcs-gitdir-file', [d('wt'), f('wt/.git', text='gitdir: /elsewhere/.git/worktrees/wt\n')], launch='wt'),
        case('vcs-gitdir-file-without-line-end', [d('wt'), f('wt/.git', text='gitdir: ../main/.git/worktrees/wt')], launch='wt'),
        case('vcs-gitdir-file-crlf', [d('wt'), f('wt/.git', text='gitdir: /elsewhere/wt\r\n')], launch='wt'),
        case('vcs-git-file-malformed', [d('wt'), f('wt/.git', text='not a gitdir line\n')], launch='wt'),
        case('vcs-git-file-two-lines', [d('wt'), f('wt/.git', text='gitdir: /a\ngitdir: /b\n')], launch='wt'),
        case('vcs-git-file-empty-target', [d('wt'), f('wt/.git', text='gitdir: \n')], launch='wt'),
        case('vcs-git-file-hard-linked', [d('wt'), f('wt/.git', text='gitdir: /elsewhere\n', hardlink=True)], launch='wt'),
        case('vcs-git-file-over-4-mib', [d('wt'), big('wt/.git', MAX_CONFIG_BYTES + 1)], launch='wt'),
        case('vcs-gitdir-file-bare-cr', [d('wt'), f('wt/.git', text='gitdir: /elsewhere/wt\r')], launch='wt'),
        # r2 (Codex B2B3A-R1-RF-1): the `.git` file is read only under S3 file custody, never waived.
        case('vcs-git-file-acl-grant-to-another-user-has-no-target', [d('wt'), f('wt/.git', text='gitdir: /elsewhere\n', acl='user')], launch='wt'),
        case('vcs-git-file-acl-grant-to-another-group-has-no-target', [d('wt'), f('wt/.git', text='gitdir: /elsewhere\n', acl='group')], launch='wt'),
        case('vcs-git-file-other-writable-has-no-target', [d('wt'), f('wt/.git', '0666', text='gitdir: /elsewhere\n')], launch='wt'),
        case('vcs-git-file-group-writable-has-no-target', [d('wt'), f('wt/.git', '0664', text='gitdir: /elsewhere\n')], launch='wt'),
        case('vcs-git-file-group-writable-authorized', [d('wt'), f('wt/.git', '0664', text='gitdir: /elsewhere\n')], launch='wt', groups='own'),
        case('vcs-git-file-owner-only', [d('wt'), f('wt/.git', '0600', text='gitdir: /elsewhere\n')], launch='wt'),
        case('explicit-foreign-gitdir-never-waived', [d('wt'), f('wt/.git', text='gitdir: /elsewhere\n')], explicit='wt', waive=True, foreign=True),
        case('vcs-git-symlink-never-followed', [d('wt'), link('wt/.git', '/elsewhere')], launch='wt'),
        case('vcs-git-fifo-never-opened', [d('wt'), fifo('wt/.git')], launch='wt'),
        case('vcs-hg-file', [d('wt'), f('wt/.hg')], launch='wt'),
        case('vcs-git-file-before-hg-directory', [d('wt'), f('wt/.git', text='gitdir: /elsewhere\n'), d('wt/.hg')], launch='wt'),
        case('ancestor-other-writable-is-a-custody-boundary', [d('above'), d('above/.git'), d('above/open', '0777'), d('above/open/launch')], launch='above/open/launch'),
        case('ancestor-acl-grant-is-a-custody-boundary', [d('above', acl='user'), d('above/launch')], launch='above/launch'),
        case('ancestor-group-write-authorized-passes', [d('shared', '0775'), d('shared/launch')], launch='shared/launch', groups='own'),
        case('explicit-with-config-and-vcs', repo + [d('repo/.git'), f('repo/opensip.json')], explicit='repo'),
        case('explicit-inside-a-repository', repo + [d('repo/.git'), d('repo/inner')], explicit='repo/inner'),
        case('explicit-foreign-owner-waived', [d('checkout'), f('checkout/opensip.json'), d('checkout/.git')], explicit='checkout', waive=True, foreign=True),
        case('explicit-acl-config-not-waived', [d('checkout'), f('checkout/opensip.json', acl='user')], explicit='checkout', waive=True, foreign=True),
    ]
    ids = [c['id'] for c in out]
    require(len(ids) == len(set(ids)), 'duplicate case id')
    return out


def gitdir_value(text):
    """One `gitdir:` line with an optional LF or CRLF end (r2, Codex B2B3A-R1-NBO-1), else null."""
    if not text.startswith('gitdir: '):
        return None
    value = text[len('gitdir: '):]
    value = value[:-2] if value.endswith('\r\n') else value[:-1] if value.endswith('\n') else value
    return value if value and not any(c in value for c in '\n\r\0') else None


def slm_input(slm, c):
    owner = 1001 if c['foreign'] else 1000
    groups = [50 if c['groups'] == 'own' else 60] if c['groups'] else []
    kinds = {e['path']: e for e in c['tree']}
    fs = {HOME: dict(kind='dir', uid=1000, gid=50, mode='0700', dev=1)}
    for e in c['tree']:
        p = HOME + '/' + e['path']
        row = dict(kind=e['kind'], uid=owner, gid=50, mode=e.get('mode', '0777'), dev=1)
        if e['kind'] == 'file':
            row['nlink'] = 2 if e.get('hardlink') else 1
            row['size'] = e['size'] if 'size' in e else len(e['text'].encode())
        if e.get('acl'):
            row['aclWrite'] = ['uid:1001' if e['acl'] == 'user' else 'group:70']
        fs[p] = row
    for rel, e in [('', None)] + list(kinds.items()):
        if e is not None and e['kind'] != 'dir':
            continue
        for marker in MARKERS:
            m = kinds.get((rel + '/' if rel else '') + marker)
            if m is None:
                continue
            if m['kind'] == 'dir':
                vcs = True
            elif m['kind'] == 'file' and marker == '.git':
                row = fs[HOME + '/' + m['path']]
                admitted = slm._file_custody(row, 1000, False, set(groups)) is None
                vcs = dict(kind='indirection', target=gitdir_value(m.get('text', '')) if admitted else None)
            else:
                vcs = dict(kind='indirection', target=None)
            fs[HOME + ('/' + rel if rel else '')]['vcs'] = vcs
            break
    inp = dict(invokingUid=1000, accountHome=HOME, cwd=HOME + ('/' + c['launch'] if c['launch'] else ''), fs=fs)
    if c['explicit'] is not None:
        inp['explicitProject'] = HOME + '/' + c['explicit']
    if c['waive']:
        inp['trustProjectOwner'] = True
    if groups:
        inp['authorizedGroupIds'] = groups
    return inp


def vector(slm, reference_cases, c):
    inp = slm_input(slm, c)
    if c['id'] in reference_cases:
        # A reference case keeps its own outcome: the native tree reproduces its code, detail and path.
        want = reference_cases[c['id']]['expect']
    else:
        want = None
    result = slm.discovery(copy.deepcopy(inp))
    prov = result['provenance']
    rows = copy.deepcopy(prov['walked'])
    if result['status'] == 'REFUSE':
        expected = dict(status='REFUSE', refusal=result['refusal'], path=result['path'], detail=result['detail'],
                        mode=prov['mode'], walked=rows, explicitPathWasSymlink=prov['explicitPathWasSymlink'])
    else:
        vcs = prov['vcs']
        if vcs is not None:
            require(vcs.pop('followed') is False, 'followed vcs')
        expected = dict(status='ACCEPT', selectedRoot=prov['selectedRoot'], **{k: copy.deepcopy(prov[k]) for k in UPWARD})
        expected['vcs'] = vcs
    if want is not None:
        for k, v in want.items():
            if k in ('status', 'refusal', 'detail'):
                require(expected.get(k) == v, 'reference case outcome differs: %s %s' % (c['id'], k))
    return dict(id=c['id'], reference=c['id'] in reference_cases, tree=c['tree'], launch=c['launch'], explicit=c['explicit'],
                waive=c['waive'], foreign=c['foreign'], groups=c['groups'], slmInput=inp, expected=expected)


def vectors(arch, product, packages_root):
    packages(product, packages_root)
    for row in ARCH:
        pinned(arch, *row)
    ref = load('discovery_scan_reference', arch / ARCH[0][0])
    slm, _rule = ref.load(arch)
    reference_cases = {c['id']: c for c in json.loads((arch / ARCH[1][0]).read_bytes())['cases'] if c.get('model', 'discovery') == 'discovery'}
    body = {'schemaVersion': 1,
            'standing': 'B2-b0 current-reference vectors for the analysis path\'s upward selection (M3-B r5 item 13; unit B2-b3a). '
                        'Generated by tools/security/discovery_upward_vectors.py at the reference\'s accepted bytes over tree '
                        'descriptions the security tests materialize natively; design reference results, not product qualification.',
            'sources': [dict(path=p, bytes=n, sha256=h) for p, n, h in ARCH],
            'cases': [vector(slm, reference_cases, c) for c in cases()]}
    return (json.dumps(body, separators=(',', ':'), ensure_ascii=True) + '\n').encode()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--check', action='store_true', help='compare the output without writing repository files')
    mode.add_argument('--write', action='store_true', help='regenerate the output')
    parser.add_argument('--architecture', type=Path, required=True, help='architecture checkout holding the reference')
    parser.add_argument('--packages-root', type=Path, required=True, help='checkout holding the provisioned python-packages snapshot')
    args = parser.parse_args()
    product = Path(__file__).resolve().parent.parent.parent
    raw = vectors(args.architecture.resolve(strict=True), product, args.packages_root.resolve(strict=True))
    target = product / OUTPUT
    if args.check:
        require(target.is_file() and target.read_bytes() == raw, 'vectors differ: ' + OUTPUT)
    else:
        target.write_bytes(raw)
    print(('Verified ' if args.check else 'Generated ') + OUTPUT + ' from the B2-b0 reference at its accepted bytes.')


if __name__ == '__main__':
    try:
        main()
    except (ValueError, KeyError, TypeError, OSError) as error:
        print(f'Discovery upward vector generation failed: {error}', file=sys.stderr)
        raise SystemExit(1)
