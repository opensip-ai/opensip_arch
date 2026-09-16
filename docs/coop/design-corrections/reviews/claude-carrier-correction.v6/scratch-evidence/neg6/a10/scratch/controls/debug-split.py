import sys

ddl = open(sys.argv[1], encoding='utf-8').read()


def split_sql(script):
    out, buf, in_trigger = [], [], False
    for raw in script.split('\n'):
        line = raw.split('--')[0] if raw.strip().startswith('--') else raw
        if not line.strip():
            continue
        buf.append(line)
        upper = line.upper()
        if 'CREATE TRIGGER' in upper:
            in_trigger = True
        if in_trigger:
            if upper.rstrip().endswith('END;'):
                out.append('\n'.join(buf))
                buf, in_trigger = [], False
        elif line.rstrip().endswith(';'):
            out.append('\n'.join(buf))
            buf = []
    if [b for b in buf if b.strip()]:
        out.append('\n'.join(buf))
    return [s for s in out if s.strip()]


sts = split_sql(ddl)
print('statements', len(sts))
for i, s in enumerate(sts):
    first = s.strip().split('\n')[0][:80]
    print('---', i, 'endswith-semicolon=%s' % s.rstrip().endswith(';'), '|', first)
