"""Render logs/results.json and logs/python-grants.json into logs/summary.md (no new runs)."""
import json, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import confine as C


def cell(value):
    if isinstance(value, dict) and 'result' in value:
        return value['result'] + ('' if value.get('errno') is None else f" (errno {value['errno']})") + \
            (f" = {value['detail']}" if value['result'] == 'ALLOWED' and value.get('detail') not in (None, True) else '')
    return '—' if value is None else str(value)


def main():
    results = json.loads((C.LOGS / 'results.json').read_text())
    grants = json.loads(C.GRANTS.read_text())
    positive, negative = results['positive'], results['negative']
    out = ['# Generated summary (scripts/summarize.py)', '', '## Positive', '']
    for label in ('confined-1', 'confined-2', 'unconfined-entry'):
        run = positive[label]
        out.append(f"- `{label}`: exit {run['exitCode']}, stderr {run['stderr']!r}, collection {json.dumps(run['collection'])}")
    out += ['', '```json', json.dumps(positive['parity'], indent=1), '```', '',
            f"- direct reference files: {json.dumps(positive['referenceDirect'])}",
            f"- work tree unchanged: {results['workTreeUnchanged']}; grants still pinned: {results['grantsStillPinned']}",
            f"- collector: `{results['collector']['path']}` sha256 `{results['collector']['sha256']}`", '']
    for mode, title in (('main', 'Probe (main)'), ('exec', 'Probe (exec)')):
        confined, control = negative['probe-' + mode], negative['control-probe-' + mode]
        rows_c, rows_u = confined['probe'].get(mode, {}), control['probe'].get(mode, {})
        out += [f'## {title}', '', f"confined exit {confined['exitCode']} stderr `{confined['stderr'].strip()}`; "
                f"control exit {control['exitCode']} stderr `{control['stderr'].strip()}`", '',
                '| attempt | confined | unconfined control |', '|---|---|---|']
        for key in sorted(set(rows_c) | set(rows_u)):
            if key != 'info':
                out.append(f'| {key} | {cell(rows_c.get(key))} | {cell(rows_u.get(key))} |')
        if 'info' in rows_c:
            out += ['', '```json', json.dumps(rows_c['info'], indent=1), '```']
        out += ['', f"output entries after confined probe: {json.dumps(confined['outputEntries'])}", '']
    out += ['## Network', '', '| attempt | confined (+_socket) | confined (+_socket, no map-executable) | unconfined control |', '|---|---|---|---|']
    widened, nomap, control = (negative[k]['probe'].get('network', {}) for k in
                               ('probe-network-widened', 'probe-network-widened-without-map', 'control-probe-network'))
    for key in sorted(control):
        out.append(f'| {key} | {cell(widened.get(key))} | {cell(nomap.get(key))} | {cell(control.get(key))} |')
    out += ['', f"listeners: confined {negative['probe-network-widened']['listenerObserved']}, "
            f"no-map {negative['probe-network-widened-without-map']['listenerObserved']}, "
            f"control {negative['control-probe-network']['listenerObserved']}", '',
            f"collection of confined probe output: {json.dumps(negative['collectionAfterProbe'])}", '', '## Ablations', '',
            '| run | exit | output entries | stderr | sandbox denials reported |', '|---|---|---|---|---|']
    for key in ('withoutIsolatedFlag', 'withoutNoSiteFlag', 'withoutBytecodeFlag', 'withoutMapExecutable',
                'withoutRuntimeVocabularyGrant', 'nonEmptyOutputRoot', 'undeclaredExec', 'launcherStubExec'):
        run = negative[key]
        stderr = run['stderr'].strip().replace('|', '/').replace('\n', ' ')
        out.append(f"| {key} | {run['exitCode']} | {run['outputEntries']} | `{stderr}` | {len(run.get('sandboxDenials') or [])} |")
    out += ['', f"canary unchanged: {negative['canaryUnchanged']}; forbidden outside paths absent: {json.dumps(negative['forbiddenOutsideAbsent'])}",
            '', '## Pinned interpreter grants', '', f"{grants['interpreter']['version']}", '',
            f"- executable `{grants['interpreter']['executable']['path']}` `{grants['interpreter']['executable']['sha256']}`",
            f"- library `{grants['interpreter']['library']['path']}` `{grants['interpreter']['library']['sha256']}`"]
    for row in grants['sources'] + grants['extensions']:
        out.append(f"- `{row['path'][len(str(C.STDLIB)) + 1:]}` `{row['sha256']}`" + (f" links {row['linkage']}" if 'linkage' in row else ''))
    out += ['', 'directories (listing only): ' + ', '.join('`' + d[len(str(C.STDLIB)):] + '/`' for d in grants['directories']),
            '', 'built-in/frozen/not-found: ' + json.dumps(grants['builtinOrFrozen']), '']
    (C.LOGS / 'summary.md').write_text('\n'.join(out))
    print('wrote', C.LOGS / 'summary.md')


if __name__ == '__main__':
    main()
