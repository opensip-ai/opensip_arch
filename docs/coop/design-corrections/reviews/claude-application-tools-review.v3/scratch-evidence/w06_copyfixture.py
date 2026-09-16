"""Copy my own v2 scratch fixture builder into v3 scratch (own prior output)."""
import hashlib
import shutil
from pathlib import Path

SRC = Path('/tmp/opensip-design-corrections/claude-application-tools-review.v2/scratch/fixture.py')
DST = Path(__file__).resolve().parent / 'fixture.py'
shutil.copyfile(SRC, DST)
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
print('copied', SRC, '->', DST)
print('identical:', sha(SRC) == sha(DST), sha(DST)[:16])
