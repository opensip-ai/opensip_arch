"""Build the B-S10 architecture package (contract successor, rust3 materialization form) in the work stage."""
from pathlib import Path
import json, hashlib, shutil, subprocess, os
D = Path('/Users/sb/code/.opensip-implementation-cache/work-2026-10-14/b-s10'); W = Path('/Users/sb/code/opensip-ai/opensip-b-s10'); A = Path('/Users/sb/code/opensip-ai/opensip_arch')
PRE = 'docs/implementation/m3/config-discovery-b/b-s10'; S = D / 'architecture'; R = S / PRE
E = dict(os.environ, GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null')
for k in ('GIT_CONFIG_COUNT', 'GIT_DIR', 'GIT_WORK_TREE'): E.pop(k, None)
def git(*a): return subprocess.check_output(['/usr/bin/git', *a], cwd=W, env=E).decode()
def pin(root, path): b = (root / path).read_bytes(); return dict(path=path, bytes=len(b), sha256=hashlib.sha256(b).hexdigest())
changed = sorted(git('diff', '--name-only').split() + git('ls-files', '--others', '--exclude-standard').split())
changed = [c for c in changed if not c.startswith(('tools/contracts/node_modules/', 'tools/contracts/python-packages/', 'tools/typescript-boundary/node_modules/'))]
for c in changed: t = R / 'product' / c; t.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(W / c, t)
ev = R / 'evidence'; ev.mkdir(exist_ok=True)
for n in ['prepare_b_s10.py', 'run_b_s10_generation.py', 'run_b_s10_checks_r9.py', 'build_b_s10_package.py', 'preparation.json', 'generation-summary.json', 'prepare.log', 'generation.log', 'checks-r9.log', 'base-admission-tests.log']:
    shutil.copyfile(D / n, ev / n)
shutil.copytree(D / 'checks-r9', ev / 'checks-r9', dirs_exist_ok=True)
hist = ev / 'history'; hist.mkdir(exist_ok=True)
for att in ['attempt0', 'attempt1', 'attempt2', 'attempt3', 'attempt4', 'attempt5']:
    for p in sorted((D / att).rglob('*')):
        if p.is_file() and p.suffix in ('.log', '.json', '.py'): t = hist / att / p.relative_to(D / att); t.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(p, t)
prep = json.loads((D / 'preparation.json').read_text())
pcs, pv = prep['newSources']
parents = sorted([dict(path=pcs['arch'], bytes=pcs['archPin']['bytes'], sha256=pcs['archPin']['sha256']), {k: pv['parentArch'][k] for k in ('path', 'bytes', 'sha256')},
                  {k: prep['parentAdmissionRegistry'][k] for k in ('path', 'bytes', 'sha256')}], key=lambda r: r['path'])
(R / 'README.md').write_text(f"""# B-S10: configuration schema admission materialization

**Design unit, contract successor (materialization form). PROPOSED; arch only until bound.** This is the prerequisite of M3-B unit B1-a that the accepted B1-a plan names (`../b1-a/PLAN-r2.md` §2; Codex `codex-b1a-plan-r2` ACCEPT, with NBO-01). The product validates schemas at runtime only through the admission registry (`SOURCE_PINS`), and `verify_design` binds `schemas/admission-registry.json` to an accepted architecture copy. So the two configuration carriers need a new accepted copy before B1-a can admit them.

## What it selects

- **`admission-registry.json`.** The parent registry (`{prep['parentAdmissionRegistry']['path']}`) plus two rows, sorted by schema ID:
  - `urn:opensip:product-configuration:2`, which is PCS (`{pcs['arch']}`, `{pcs['sha'][:8]}…`);
  - `urn:opensip:preview-configuration:1`, the preview v1 carrier, through the copy below.
- **`preview-configuration.schema.v1.profiled.json` (lead decision).** The product's exact schema profile (`crates/identity/src/schema.rs`, `opensip-exact-schema-reference-1`) admits no `$comment`. The accepted preview carrier (`{pv['parentArch']['path']}`, `{pv['parentArch']['sha256'][:8]}…`) has exactly one: a top-level prose note on the paired reader.
  - The copy removes that one member: line 603, and the comma that ended line 602.
  - Every validating keyword is unchanged; the build asserts the two documents are equal once that member is dropped.
  - The parent stays as historical bytes.
  - **Rejected:** widening the schema profile's annotation set. That changes a selected profile for one prose note.
- **`product/`.** Exact copies of every product file the change touches. The product commit copies them byte for byte:
  - **Generation sources.** PCS joins `schemas/registry.json` (owner `crates/host/src/configuration.rs`, major 2), `schemas/source-map.json` and `tools/contracts/options.json`, as namespace `ProductConfiguration2` in module `invocation`, because it is an input carrier.
  - **Admission-only.** The preview v1 carrier joins the admission maps only (B1A-PLAN-R2-NBO-01).
  - **Pins.** Both sources join the identity `SOURCE_PINS` and the host's and storage's identical `SOURCES` lists, which host `admission_tests` requires to be equal; its count assertion and two comments go from 48 to 50. The generator closure gains PCS's row and re-pins `source-map.json` and `options.json`, and the registry recipe is re-pinned.
  - **Regeneration.** The pinned contracts generator regenerated two outputs: `crates/contracts/src/generated/invocation.rs` (the new `ProductConfiguration2Root` carrier) and `apps/report/src/generated/report.ts`.

## Evidence

- **Scripts and records.** `evidence/prepare_b_s10.py`, `run_b_s10_generation.py`, `run_b_s10_checks_r9.py` and their records.
- **Checks r9** (lane held, priority 10, private TMPDIR):
  - rustfmt on the hand-edited files;
  - the identity and contracts test suites pass;
  - Clippy, warnings denied, over identity, contracts, host and storage;
  - host and storage suites run `--no-fail-fast` on the base checkout and on the candidate, with identical failure sets: host 8 and storage 33. These are pre-existing crash-matrix synthetic cases, failing identically at base (`base-admission-tests.log`).
- **Two pre-existing conditions,** recorded and not changed here:
  - the identity dependency policy fails its source census at base and candidate alike (`checks-r9/identity-policy-baseline.json`);
  - neither the host nor the identity crate is rustfmt-clean at base.
- **The report TypeScript lane** runs `verify_design`'s admission preflight, so it can pass only once this successor is accepted. (r2, NBO-01) The scratch verification runs only `verify_design.verify`, with a synthetic appended entry: that admission preflight passes. The actual report lane, and the standard `generate_contracts.py` check, run at integration after real acceptance and assent, with the bound lock in the candidate worktree.
- **(r2, RF-01) Recipe admission.** The registry recipe's `optionsSha256` follows the candidate options bytes, and the generation runner first passes the standard recipe admission (`tools/contracts/admission.py` `registry()`).
- **History.** `evidence/history/attempt0-3`:
  - attempt 0: unsorted generator options;
  - attempt 1: output module changed to `invocation`;
  - attempt 2: `$comment` refused by the profile;
  - attempt 3: storage `SOURCES` missing;
  - attempt 4: the recipe options pin was stale (round 1, Codex B-S10-R1-RF-01), and the new standard recipe admission then refused the unsorted `registry.json` source row.

## Standing

No resolver semantics; those are B1-a's. No law change, and no new consumer of either schema yet. Not bound until Codex's ACCEPT-DESIGN-UNIT, the lead's assent, and its own lock commit.
""")
cands = sorted([pin(S, p.relative_to(S).as_posix()) for p in sorted(R.rglob('*')) if p.is_file()], key=lambda r: r['path'])
record = dict(schemaVersion=1, standing='PROPOSED B-S10 configuration schema admission materialization (admission-registry copy, profiled preview v1 carrier copy, exact product copies); no resolver semantics',
              parents=parents, passageOverrides=[], candidates=cands)
(R / 'successor.json').write_text(json.dumps(record, indent=2) + '\n')
subj = sorted(cands + [pin(S, PRE + '/successor.json')], key=lambda r: r['path'])
(S / (PRE + '-subject.json')).write_text(json.dumps(dict(schemaVersion=1, unit='B-S10', files=subj), indent=2) + '\n')
print(len(changed), 'product files;', len(cands), 'candidates')
