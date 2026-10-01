# X3b-4 r3

ACCEPT-UNIT. RF-1 is closed. Inventory v108 on v112 is ACCEPT. The rollover source is the r2 diff.

This recheck covers the standing sentences only. r2's judgment of the rollover, the succession, the capacity window, and the r9 and r10 end-step rules stands.

## RF-1

`repository-file-inventory.v108.json` standing is "PROPOSED additive grant-generation rollover layout (law X3b r10, unit X3b-4); no release, custody, profile, boot or creator qualification". `journal-rollover-x3b4-inventory-v108/successor.json` standing is the same sentence with "independent review and lead assent required". Neither file contains `law X3b r8`.

Replacing that one standing phrase in v108 with the r2 phrase `law X3b r8` restores r2's bytes and sha256 (`372606`, `54f505f276e18399b4b806c64e3f4c6d268187ad9430ba0bed39cff06092082d`). The other two `law X3b r10` phrases in v108 are the two added descriptions, already r10 at r2. Inherited rows are the 789 v112 rows by value. Schema, packages, and pending decisions match v112. The two added paths are `carrier_rollover.rs` and `carrier_rollover_tests.rs`.

The successor record's parent is v112 (`365881`, `acfc4bc9cc896bab1f916d4a06eb6adc87bab89b2a1c809696dba09b13c7473a`). Its candidate pin is the rebuilt v108 (`372607`, `000ec2ac87208bded12c94d91692530780d0ad75e32cdc6806fa89a05f692040`). Restoring the standing phrase and that candidate pin restores r2's successor (`20205`, `3c1dc96a795ed060dd791c436eb3329ef91c83a56151e1d6cbf37ff543f24ce1`).

`build_v108.py` is the only edited source. Its two standing literals are the sentences above. Restoring those two literals restores r2's script (`11818`, `28deee349928c1a2ee194ef0f41ee3ad07033a51971497483ec0883394d596bf`). The README, verify helpers, verifier anchor, and verification records match r2's pins, including `verification.stdout`. The builder was not re-executed here; it writes the architecture tree. The byte restoration is the check that a rebuild changed only those strings and the candidate pin they produce.

## Unchanged product

The worktree `opensip-x3b4` is detached at `f1b832183c1c9fc0ef1da647945b45453061a06c` and selects v112. `git diff` is 163034 bytes, sha256 `a53c78f97742497506bacdf5574c8d5c6dbd005449ed61d711cefbb7ea6aaf13`, equal to r2. All nine product pins match r2. `~/Library/Application Support/OpenSIP` is absent. No product test was repeated.

The shared repository's `main` ref is `704251ee4e6643bb2673c3f50d191ce27059be21`, and that checkout selects v106. The worktree under review is still f1b8321 with the r2 diff, so that later tip is outside this unit.

## Replay

`verify_projection` against the worktree lock: 16 rows, pass, 83 corruptions refused. `verify_scratch` over that lock: passed, 74 inventory successors, 72 contract successors, 16 inheritance rows, v108 selected.

Subject manifest sha256 `5fdf62b62b42ff7104cfe26c150314185c86c9f77b05f8270762db0baee85516` (2154 bytes). Each file it names matches.
