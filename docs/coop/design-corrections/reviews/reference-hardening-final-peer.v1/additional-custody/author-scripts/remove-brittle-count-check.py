"""Remove ONE redundant source-text-count control and its now-inapplicable explanatory comment
from foundation/check-identity.py. Starts from the FIRST coauthor proposal's file so the five new
third-document controls are carried over byte-for-byte. Refuses unless the anchor occurs once and
unless the control id disappears exactly once.
"""
import sys
from pathlib import Path

SRC = Path(sys.argv[1])
DST = Path(sys.argv[2])
text = SRC.read_text()

REMOVED_ID = 'the-scope-ambiguity-detail-is-a-code-this-model-already-published'

# Comment + check, removed together. The comment exists only to introduce the check.
OLD = """# It also invents no NEW detail: the ambiguity reuses a code the file already emits elsewhere.
check('the-scope-ambiguity-detail-is-a-code-this-model-already-published',
      (H.parent/'workflows/workflows_model.v1.py').read_text().count("'CONFIG.INVALID', 'CONFIG.INVALID'")==1
      and (H.parent/'workflows/workflows_model.v1.py').read_text().count("CONFIG.INVALID")>2)
"""

n = text.count(OLD)
if n != 1:
    raise SystemExit('REFUSED: anchor occurs %d times, expected exactly 1' % n)
if text.count(REMOVED_ID) != 1:
    raise SystemExit('REFUSED: control id occurs %d times, expected exactly 1' % text.count(REMOVED_ID))

out = text.replace(OLD, '')
if REMOVED_ID in out:
    raise SystemExit('REFUSED: control id survives the removal')

# Nothing else may move: the removal must be a pure deletion of those four lines.
if out != text[:text.index(OLD)] + text[text.index(OLD) + len(OLD):]:
    raise SystemExit('REFUSED: removal was not a contiguous deletion')

DST.write_text(out)
print('removed control %r (%d bytes)' % (REMOVED_ID, len(OLD)))
print('wrote', DST, DST.stat().st_size, 'bytes')
