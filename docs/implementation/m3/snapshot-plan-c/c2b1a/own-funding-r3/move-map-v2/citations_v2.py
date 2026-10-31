"""v2 (LD-Q-135 MOVE-2: full-path file identity). MOVE-MAP condition 3: every law/FUNDING citation of a moved line, resolved by NAME and mapped to its new location.

For each (document, pin commit), find every `snapshot.rs:N`, `snapshot_admission.rs:N[-M]` and
`node_modules_layout.rs:N[-M]` citation (a bare `:N` continuing the same file in the same table cell or sentence is
also taken), resolve each cited line at the pin to the enclosing column-0 item (the nearest item header above it whose
end is at or after the line), and report MOVED (with the item's new file:line from the MOVE-MAP) or STAYS.
Usage: citations.py <repo> <move-map.json> <doc>@<commit> ...
"""
import json
import re
import subprocess
import sys

PATHS = {'snapshot.rs': 'crates/host/src/snapshot.rs', 'snapshot_admission.rs': 'crates/host/src/snapshot_admission.rs',
         'node_modules_layout.rs': 'crates/host/src/node_modules_layout.rs',
         'snapshot_source.rs': 'crates/security/src/snapshot_source.rs',
         'discovery_walk.rs': 'crates/security/src/custody/discovery_walk.rs',
         'typescript_config.rs': 'crates/host/src/typescript_config.rs'}
FILES = tuple(PATHS)
HEAD = re.compile(r'^(?:pub(?:\(crate\))?\s+)?(?:const fn|fn|const|static|struct|enum|type|trait|impl(?:<[^>]*>)?)\s+([A-Za-z_]\w*)')
CITE = re.compile(r'(snapshot_admission|snapshot_source|snapshot|node_modules_layout|discovery_walk|typescript_config)\.rs`?((?::\d+(?:-\d+)?)(?:(?:,|`?,? `?| and |, and )`?:\d+(?:-\d+)?)*)')


def items_at(repo, commit, name):
    text = subprocess.run(['git', '-C', repo, 'show', f'{commit}:{PATHS[name]}'], capture_output=True,
                          text=True, check=True).stdout.split('\n')
    spans, cur = [], None
    for i, line in enumerate(text, 1):
        m = HEAD.match(line)
        if m:
            if cur:
                spans.append(cur)
            cur = [m.group(1), i, i]
        elif cur and (line.startswith('}') or line.endswith(';') and not line.startswith(' ')):
            cur[2] = i
    if cur:
        spans.append(cur)
    return spans


def main():
    repo, mapping = sys.argv[1], json.load(open(sys.argv[2]))
    # v2 (LD-Q-135 MOVE-2): ONE file identity on both sides, the full relative path (the map's `old` path; a
    # citation's basename resolved through PATHS to its one full path).
    moved = {(r['old'].rsplit(':', 1)[0], r['name']): r for r in mapping}
    cache = {}
    for arg in sys.argv[3:]:
        doc, commit = arg.rsplit('@', 1)
        for n, line in enumerate(open(doc).read().split('\n'), 1):
            for m in CITE.finditer(line):
                f = m.group(1) + '.rs'
                for a, b in re.findall(r':(\d+)(?:-(\d+))?', m.group(2)):
                    lo, hi = int(a), int(b or a)
                    key = (commit, f)
                    if key not in cache:
                        cache[key] = items_at(repo, commit, f)
                    names = sorted({s[0] for s in cache[key] if s[1] <= hi and s[2] >= lo} or
                                   {max((s for s in cache[key] if s[1] <= lo), key=lambda s: s[1], default=['?'])[0]})
                    for name in names:
                        r = moved.get((PATHS[f], name))
                        where = f"MOVED -> {r['new']}" if r else 'STAYS'
                        print(f'{doc.split("/")[-1]}:{n}  {f}:{lo}{"-" + str(hi) if hi != lo else ""} @{commit[:7]}  {name}  {where}')


main()
