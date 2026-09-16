# Software SHA-256 candidate

Root selects the exact `sha2-const-stable=0.1.0` package for the successor code
review. It has no runtime/build dependencies, target-conditioned dependencies,
build script, FFI or unsafe source. Root read the complete manifest and four
source files; their hashes are retained. Registry package bytes remain pinned
by Cargo.lock. This is a proposed reviewed external-library selection, not a
cryptographic audit or a statement about upstream endorsement/maintenance.

Claude's first static review classified sha2/cpufeatures/libc as a nonblocking
forward dependency-record obligation. Root takes the approved pure-layer
"no OS dependency" rule literally across targets, and chooses to remove that
chain rather than add a runtime getauxval exception. Software dispatch leaves
hash semantics unchanged. The existing9 Rust groups passed in an isolated
candidate. The live successor adds18 independent hashlib padding/size vectors,
including a raw blob above the JSON cap; its exact frozen validation is separate.
Actual Claude must inspect this changed dependency before unit acceptance.

The tradeoff is loss of the original hardware acceleration. Performance is not
qualified; future measurements may justify another reviewed pure implementation
while retaining identical public hash bytes. No custom SHA algorithm was added
to the OpenSIP crate.
