"""B-S10 addendum: rustfmt the two edited Rust files (inserted SourcePin/include rows) with the pinned toolchain."""
import subprocess, hashlib
from pathlib import Path
W = Path('/Users/sb/code/opensip-ai/opensip-b-s10'); files = ['crates/identity/src/schema_registry.rs', 'crates/host/src/schema_sources.rs']
before = {f: hashlib.sha256((W / f).read_bytes()).hexdigest() for f in files}
subprocess.run(['/opt/homebrew/Cellar/rust/1.95.0/bin/rustfmt', '--edition', '2024', *files], cwd=W, check=True)
print({f: (before[f][:8], hashlib.sha256((W / f).read_bytes()).hexdigest()[:8]) for f in files})
