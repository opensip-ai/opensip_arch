"""v2 (LD-Q-135 MOVE-1: field visibility compared against declared field_deltas). LD-Q-125 condition 3: prove each moved item's body identical between the old and the new commit.

For every item of the MOVE-MAP (name, old file, new file), extract the item (its doc comments and attributes, then the
item through its matching close) from `git show <old>:<old file>` and `git show <new>:<new file>` (or the working tree
when <new> is `WORKTREE`), lex both into token streams (doc comments kept as tokens, whitespace and plain comments
dropped), remove ONLY the visibility tokens (`pub`, `pub(crate)`: the one allowed change), and require equality. Any
missing, ambiguous or differing item fails. Usage: move_identity.py <repo> <old commit> <new commit|WORKTREE> <map.json>
"""
import json
import re
import subprocess
import sys

TOKEN = re.compile(r'''
    (?P<doc>///[^\n]*|//![^\n]*)
  | (?P<comment>//[^\n]*|/\*.*?\*/)
  | (?P<ws>\s+)
  | (?P<str>b?r(?P<h>\#*)".*?"(?P=h)|b?"(?:\\.|[^"\\])*")
  | (?P<char>b?'(?:\\.|[^'\\])'(?!\w))
  | (?P<life>'[A-Za-z_]\w*)
  | (?P<num>\d[\w.]*)
  | (?P<ident>[A-Za-z_]\w*)
  | (?P<punct>::|->|=>|\.\.=|\.\.|<=|>=|==|!=|&&|\|\||[-+*/%^&|!<>=@.,;:\#$?~()\[\]{}])
''', re.X | re.S)


def lex(text):
    out = []
    for m in TOKEN.finditer(text):
        kind = m.lastgroup if m.lastgroup != 'h' else 'str'
        if kind in ('ws', 'comment'):
            continue
        tok = m.group(0)
        if kind == 'doc':
            tok = tok.rstrip()
        out.append(tok)
    return out


def strip_seal(toks):
    """A row's declared `seal` delta (S.9): drop a `crate::sealed::Sealed` supertrait (`: X` or `+ X`) only."""
    seal = ['crate', '::', 'sealed', '::', 'Sealed']
    out, i = [], 0
    while i < len(toks):
        if toks[i] in (':', '+') and toks[i + 1:i + 6] == seal:
            nxt = toks[i + 6] if i + 6 < len(toks) else ''
            i += 6
            if toks[i - 6] == ':' and nxt == '+':
                out.append(':'); i += 1
            continue
        out.append(toks[i]); i += 1
    return out


ITEM_KW = {'fn', 'const', 'static', 'struct', 'enum', 'type', 'trait', 'mod', 'use', 'unsafe', 'async', 'extern', 'impl'}


def strip_visibility(toks, field_deltas=(), applied=None):
    """v2 (LD-Q-135 MOVE-1): ITEM and METHOD visibility (a `pub`/`pub(crate)` followed by an item keyword) is erased;
    FIELD visibility (followed by a field name and `:`, or by a tuple field's type) is KEPT as a token and compared,
    except that a field listed in `field_deltas` (dicts: field, old, new) with exactly the declared new visibility is
    mapped back to its declared old visibility (recorded in `applied`)."""
    deltas = {d['field']: d for d in field_deltas}
    out, i = [], 0
    while i < len(toks):
        if toks[i] == 'pub':
            crate = toks[i + 1:i + 4] == ['(', 'crate', ')']
            vis, j = ('pub(crate)' if crate else 'pub'), i + (4 if crate else 1)
            nxt = toks[j] if j < len(toks) else ''
            if nxt in ITEM_KW:
                i = j
                continue
            name = nxt if j + 1 < len(toks) and toks[j + 1] == ':' else None
            d = deltas.get(name) if name else None
            if d and vis == d['new']:
                vis = d['old']
                if applied is not None:
                    applied.append(name)
            if vis != 'private':  # a private field carries no visibility token (w2C note 23a)
                out.append('VIS:' + vis)
            i = j
            continue
        out.append(toks[i])
        i += 1
    return out


def item(text, name, kind_hint=None):
    """The item named `name` at column 0 (fn, const, static, struct, enum, type; `impl <name>` for an inherent impl),
    with its leading doc comments and attributes, through its end. Exactly one such item must exist."""
    if name.startswith('impl '):
        pat = re.compile(rf'^impl(?:<[^>\n]*>)?\s+{re.escape(name[5:])}\b', re.M)
    else:
        pat = re.compile(rf'^(?:pub(?:\(crate\))?\s+)?(?:const fn|fn|const|static|struct|enum|type|trait)\s+{re.escape(name)}\b', re.M)
    found = list(pat.finditer(text))
    if len(found) != 1:
        raise SystemExit(f'{name}: {len(found)} definitions')
    start = found[0].start()
    lines_before = text[:start].split('\n')[:-1]
    k = len(lines_before)
    while k > 0 and (lines_before[k - 1].startswith('///') or lines_before[k - 1].startswith('#[')):
        k -= 1
    begin = len('\n'.join(lines_before[:k])) + (1 if k else 0)
    # the end: the first `;` at depth 0, or the close of the first `{` block at depth 0
    depth, i = 0, start
    for m in TOKEN.finditer(text, start):
        t = m.group(0)
        if m.lastgroup in ('ws', 'comment', 'doc', 'str', 'char', 'life'):
            continue
        if t in '([{':
            depth += 1
        elif t in ')]}':
            depth -= 1
            if depth == 0 and t == '}' and text[start:m.start()].count('{') and not re.match(r'\s*[;,)]', text[m.end():]):
                head = text[start:m.end()]
                if head.lstrip().startswith(('fn', 'pub fn', 'pub(crate) fn', 'impl', 'struct', 'pub struct', 'pub(crate) struct', 'enum', 'pub enum', 'pub(crate) enum', 'const fn', 'pub const fn', 'pub(crate) const fn')):
                    return text[begin:m.end()]
        elif t == ';' and depth == 0:
            return text[begin:m.end()]
    raise SystemExit(f'{name}: no end')


def show(repo, commit, path):
    if commit == 'WORKTREE':
        return open(f'{repo}/{path}').read()
    return subprocess.run(['git', '-C', repo, 'show', f'{commit}:{path}'], capture_output=True, text=True, check=True).stdout


def main():
    repo, old, new, mapping = sys.argv[1:5]
    rows = json.load(open(mapping))
    bad = 0
    replaced = {r['name'] for r in rows if r.get('status', 'MOVED').split()[0] == 'REPLACED'}
    checked = 0
    for r in rows:
        status = r.get('status', 'MOVED').split()[0]
        if status != 'MOVED':  # STAYS / REPLACED / REWRITTEN / NEW: no identity claim (w2C note 23a)
            print(f"SKIPPED   {r['name']:32} status {r.get('status')}")
            continue
        checked += 1
        old_path, new_path = r['old'].rsplit(':', 1)[0], r['new'].rsplit(':', 1)[0]
        a = item(show(repo, old, old_path), r['name'])
        b = item(show(repo, new, new_path), r['name'])
        applied = []
        ta, tb = strip_visibility(lex(a)), strip_visibility(lex(b), r.get('field_deltas', []), applied)
        if 'seal' in r.get('deltas', []):
            tb = strip_seal(tb)
        declared = sorted(d['field'] for d in r.get('field_deltas', []))
        same = ta == tb and sorted(applied) == declared
        bad += not same
        print(f"{'IDENTICAL' if same else 'DIFFERS  '} {r['name']:32} {r['old']} -> {r['new']} ({len(ta)} tokens)"
              + (f" field deltas applied {sorted(applied)}" if declared or applied else ''))
        impl = 'impl ' + r['name']
        if impl in replaced:
            print(f"SKIPPED   {impl:32} declared REPLACED")
        elif f'\n{impl} ' in '\n' + show(repo, old, old_path) or re.search(rf'^impl(?:<[^>\n]*>)?\s+{re.escape(r["name"])}\s*\{{', show(repo, old, old_path), re.M):
            ia, ib = item(show(repo, old, old_path), impl), item(show(repo, new, new_path), impl)
            same = strip_visibility(lex(ia)) == strip_visibility(lex(ib))
            bad += not same
            print(f"{'IDENTICAL' if same else 'DIFFERS  '} {impl:32} (inherent impl)")
    print(f'{checked} items: {"ALL IDENTICAL" if not bad else f"{bad} DIFFER"}')
    sys.exit(1 if bad else 0)


main()
