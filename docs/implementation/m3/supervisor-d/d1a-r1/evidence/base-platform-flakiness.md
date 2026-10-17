# The platform lib suite at base is flaky in parallel (lead record, 2026-10-16)

On product main `808ad64`, with no D1a change, `cargo test --locked --offline -p opensip-platform --lib`, run four times in parallel (the default):

| Run | Result |
| --- | --- |
| 1 | `fatal runtime error: IO Safety violation: owned file descriptor already closed, aborting` |
| 2 | `ok. 234 passed; 0 failed; 1 ignored` |
| 3 | `ok. 234 passed; 0 failed; 1 ignored` |
| 4 | `FAILED. 233 passed; 1 failed`: `filesystem::path_binding::tests::removal_files_and_symlinks_never_become_successful_rechecks` |

The same suite run three times serially (`-- --test-threads=1`): `ok. 234 passed; 0 failed; 1 ignored` each time.

D1a's lane attempts 1 and 2 hit the same races:
- **attempt 1:** a different `path_binding` failure at base and at candidate;
- **attempt 2:** the IO-safety abort at both base and candidate, so the lib suite produced no counts.

The lane of record (attempt 3) therefore runs the platform suite serially on both sides. The race is existing test interference, unrelated to D1a. It is recorded here and not fixed in this unit.
