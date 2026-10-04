"""F8b step 7: npm ci --offline on a scratch copy of tools/contracts with the licensed
package.json and the unchanged package-lock.json (decision 3, L1 call 5).

Control: the same lock with package.json's typescript changed to 6.0.2 must refuse with
EUSAGE, which shows npm's package.json/lock sync check is active. Uses the selected Node
24.16.0/npm 11.13.0, ~/opensip-deps/npm-cache, empty user and global configs, and a private
HOME. Never touches the worktree."""
import hashlib, json, os, shutil, subprocess, sys, tempfile
from pathlib import Path
W = Path(sys.argv[1]).resolve(strict=True)
NODE_BIN = Path('/Users/sb/.nvm/versions/node/v24.16.0/bin')
CACHE = Path('/Users/sb/opensip-deps/npm-cache')
def pin(b): return {'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
def run(directory, home, cfg):
    env = {'PATH': f'{NODE_BIN}:/usr/bin:/bin', 'HOME': str(home), 'npm_config_cache': str(CACHE),
           'npm_config_userconfig': str(cfg / 'user.npmrc'), 'npm_config_globalconfig': str(cfg / 'global.npmrc'), 'LANG': 'C', 'TZ': 'UTC'}
    p = subprocess.run([str(NODE_BIN / 'npm'), 'ci', '--offline', '--ignore-scripts', '--no-audit', '--no-fund'],
                       cwd=directory, env=env, capture_output=True, text=True, timeout=600)
    err = p.stderr.strip().splitlines()
    return {'exit': p.returncode, 'stdoutTail': p.stdout.strip().splitlines()[-3:], 'stderrHead': err[:3], 'errorCode': next((l.split()[-1] for l in err if l.startswith('npm error code ')), None)}
work = Path(tempfile.mkdtemp(prefix='f8b-npm-')); cfg = work / 'cfg'; cfg.mkdir()
(cfg / 'user.npmrc').write_text(''); (cfg / 'global.npmrc').write_text('')
manifest = (W / 'tools/contracts/package.json').read_bytes(); lock = (W / 'tools/contracts/package-lock.json').read_bytes()
assert pin(manifest)['sha256'] == '678aa95d9a72a96d0740db1aa6ba8be35d6e5cc5b8b75641fb861513b6b04df5'
assert pin(lock)['sha256'] == '6829272b59645fedb7511dfb95fbb59ebc2c16e46dad6c10a7d24578dd078f03'
out = {'standing': 'F8b step 7 evidence; scratch copies only', 'node': str(NODE_BIN / 'node'),
       'npmVersion': subprocess.run([str(NODE_BIN / 'npm'), '--version'], capture_output=True, text=True, env={'PATH': f'{NODE_BIN}:/usr/bin:/bin', 'HOME': str(work)}).stdout.strip(),
       'packageJson': pin(manifest), 'packageLock': pin(lock)}
for name, text in (('licensed', manifest), ('control-mismatch', manifest.replace(b'"typescript": "6.0.3"', b'"typescript": "6.0.2"'))):
    d = work / name; d.mkdir(); (d / 'package.json').write_bytes(text); (d / 'package-lock.json').write_bytes(lock)
    home = work / (name + '-home'); home.mkdir()
    out[name] = run(d, home, cfg)
    if name == 'licensed':
        out[name]['typescriptInstalled'] = json.loads((d / 'node_modules/typescript/package.json').read_bytes())['version'] if (d / 'node_modules/typescript/package.json').exists() else None
        out[name]['lockUnchanged'] = (d / 'package-lock.json').read_bytes() == lock
out['passed'] = out['licensed']['exit'] == 0 and out['licensed']['typescriptInstalled'] == '6.0.3' and out['licensed']['lockUnchanged'] and out['control-mismatch']['exit'] != 0 and out['control-mismatch']['errorCode'] == 'EUSAGE'
shutil.rmtree(work)
print(json.dumps(out, indent=2))
