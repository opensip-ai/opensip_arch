# Rust target-edition source check

Codex, 2026-09-06. Current correction evidence, not independent acceptance.

Cargo allows a target-specific edition with the package edition as its default. The field is deprecated but remains documented. [Cargo target edition](https://doc.rust-lang.org/cargo/reference/cargo-targets.html#the-edition-field).

The metadata format includes `targets[].edition` separately from the package default and explicitly allows targets to differ. [Cargo metadata JSON format](https://doc.rust-lang.org/cargo/commands/cargo-metadata.html#json-format).

Design consequence (Codex inference): the new source/body-to-compilation-owner join must use the target's effective edition, not assume a source-to-package join always identifies dialect. A same-package target override should be a valid representable control. This is a schema/reference obligation under the authorized mixed-edition correction. No Cargo/compiler/repository code was executed and no native implementation qualification is claimed. Actual Claude v5 was notified through its CODEX-PUBLIC-NOTE.md; final assessment remains pending.
