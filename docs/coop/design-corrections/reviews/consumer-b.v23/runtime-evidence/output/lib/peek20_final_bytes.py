"""Read-only final-byte reconciliation peek (generation 20).

Recomputes the sha256 of every artifact the final blind-review.json claims to
have retained and compares it to the recorded digest, then asks whether the
rendered blind-review.md carries the same digest table.  This instrument writes
nothing; it only reports whether the reports agree with the bytes on disk after
the last fresh-process command.
"""
import hashlib
import json
import os
import re

OUT = '/tmp/opensip-design-corrections/consumer-b.v23/output'


def sha(path):
    with open(path, 'rb') as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def digest_of(record):
    return record if isinstance(record, str) else record.get('sha256')


def main():
    with open(os.path.join(OUT, 'blind-review.json'), encoding='utf-8') as fh:
        review = json.load(fh)
    table = review['retainedArtifactDigests']

    missing, mismatched = [], []
    for rel, record in sorted(table.items()):
        path = os.path.join(OUT, rel)
        if not os.path.exists(path):
            missing.append(rel)
            continue
        measured = sha(path)
        if measured != digest_of(record):
            mismatched.append((rel, digest_of(record), measured))

    print('artifact rows in table : %d' % len(table))
    print('missing on disk        : %s' % (missing or 'none'))
    print('digest mismatches      : %d' % len(mismatched))
    for rel, want, got in mismatched[:20]:
        print('  MISMATCH %-48s recorded %s measured %s' % (rel, want[:16], got[:16]))

    with open(os.path.join(OUT, 'blind-review.md'), encoding='utf-8') as fh:
        md = fh.read()

    for rel in ('query/indep-query-surface.json', 'vectors/indep-mutation-surface.json'):
        rec = digest_of(table.get(rel)) if rel in table else None
        print('%s -> recorded %s ; named in md %d time(s) ; digest in md %s'
              % (rel, (rec or 'ABSENT')[:24], md.count(os.path.basename(rel)),
                 bool(rec and rec in md)))

    md_digests = set(re.findall(r'[0-9a-f]{64}', md))
    table_digests = {digest_of(v) for v in table.values()}
    print('distinct 64-hex digests in md            : %d' % len(md_digests))
    print('table digests also present in md         : %d of %d'
          % (len(md_digests & table_digests), len(table_digests)))

    # Reports quoting each other: the json must not claim a digest for the md
    # that the md bytes no longer have.
    for key in ('finalOwnOutputDigests', 'finalReportDigests', 'ownOutputDigests'):
        if key in review:
            print('%s: %s' % (key, json.dumps(review[key])[:400]))
    print('measured blind-review.md   sha256: %s' % sha(os.path.join(OUT, 'blind-review.md')))
    print('measured blind-review.json sha256: %s' % sha(os.path.join(OUT, 'blind-review.json')))


if __name__ == '__main__':
    main()
