# Ordinary writer inventory81

Adds exactly two sources to selected inventory80:
- crates/security/src/custody/ordinary_writer.rs
- crates/security/src/custody/ordinary_writer_tests.rs

It keeps all 749 existing rows by value, along with the packages and dependencies, the pending decisions and the carried unresolved obligations, for 751 planned files. No crate or dependency is added. The rows are unit X1a, law X1 r1 items 1 to 8.

- ordinary_writer.rs (composition) is the ordinary writer's admission: the write receipt, its recheck, the law 468 durable write gate with the receipt's sealed `DurableBarrierQualification` as its only input, and the receipt's recheck again under the held fence. A failed second recheck releases the fence.
- ordinary_writer_tests.rs (test) checks it on scratch homes with a creator-published P0, and pins that each purpose's receipt lends only its own sealed qualification.

The unit's other changes edit existing rows:
- custody.rs gains the module wiring.
- read_premise.rs generalizes 458c-a's receipt into `PlatformReceipt<P>` with the sealed purposes `Read` and `Write`, keeps `ReadPremiseReceipt` and `produce_read_platform` unchanged in behavior, and adds `WritePlatformReceipt` and `produce_write_platform` from the same composition.

read_premise.rs's effective description is 461b's override on inventory80. It says the receipt lends only `ReadPremiseQualification`, with no barrier policy, which is no longer the whole file: the write purpose lends `DurableBarrierQualification`. An inventory successor carries inherited rows by value, so this successor projects 461b's text unchanged. The correction is X1b, a description-only contract successor on inventory81 (law X1 item 8).

The sixteen effective description overrides stay bound by stable file path, with parent inventory80: the eight rows inherited through inventory80 and the eight 461b overrides on inventory80. verify_projection.py is the inventory80 helper with its row count raised from 8 to 16; run it with python3 -I -B. evidence/build_v81.py rebuilds inventory81 and successor.json deterministically. The selected product verifier is unchanged.
