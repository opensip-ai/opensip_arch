# CODEX2 review — D4 descriptions r3

## Verdict

**ACCEPT-DESIGN-UNIT**

The frozen subject manifest SHA-256 is `67782dac36ab41e84deea6c79f85dfe19fd1db3e52cf04cc1c4108da81bfe2f5`. All 22 declared members rehash exactly, and the frozen stage contains only those members plus the subject manifest. The live product and architecture heads match `639922d58ae03acf6576d07e65970440aee512ff` and `962d3783503fbdc524cb6a2c44e9efc04e79d192`; the current design lock is 784,306 bytes with SHA-256 `58a4b2240a80f18ee2e29743f34174d430c5c61a2047fc437ba6f1c178efc676`.

## R2 publication repair

R2's `ACCEPT-DESIGN-UNIT` remains design acceptance only. Its accepted manifest, 11 manifest members, review, and root assent are recoverable byte-for-byte from the frozen history. The separate lead finding and the original verifier refusal correctly record that no description contract was committed or bound. The rejected R1 subject, stage, review, and `D4-DESC-R1-RF-1` are likewise preserved byte-for-byte.

The archived R2 subject and candidate lists reproduce the stated defect: both place the nested `.../d4-descriptions-r1/README.md` before the sibling `.../d4-descriptions-r1-subject.json`, contrary to lexical string order. R3 corrects both verifier inputs. Its 22 subject-member paths and 21 contract-candidate paths are unique, relative POSIX paths in exact lexical order. The candidate set is exactly the subject-member set minus `successor.json`, and every candidate pin equals its manifest pin. This is the condition enforced by the unchanged `pin_rows` implementation; no verifier relaxation is proposed.

The successor changes only its publication envelope and standing relative to R2. Its eight `passageOverrides` and fourteen `passageSupersessions` are byte-for-byte equal to the independently accepted R2 arrays. Relative to rejected R1, the sole passage change remains `/files/510/description` for `crates/lifecycle/src/installation.rs`: it now describes the actual debug/test and debug-plus-`scenario-fixtures` read hook and its `TreeFault::Io { call: "read" }` mapping. The other 21 passages, all selectors and `before` values, and every supersession reference remain unchanged.

## Contract and source assessment

The six authority pins and all 32 current source pins rehash against the live repositories, and the current source pins equal the accepted D4 pins. The integrated D4 code commit is an ancestor of the product head. Source inspection confirms the accepted descriptions: accounted `ControlContext` and launch assembly share the caller `WorkScope`; the factory performs all native rechecks before the sole production `VerifiedLaunch::from_recheck`; pristine TS2 and Rust3 senders are checked and then consumed by participant composition; retained members expose the resolved member suffix and move the already funded bound path while retaining the operation capability; and the fixture conversion and retained-tree read hook remain guarded from ordinary release builds. The factory remains a pre-spawn library boundary with no Source access, spawn, effects, or settlement.

The current lock contains 186 contract successors, 199 inventory successors, and 161 inheritance entries, all reproduced by value in the source record. Each direct override selects its exact raw inventory239 description and has no inherited-meaning collision. Each supersession selects the exact current inherited meaning and names one exact passage in an accepted earlier contract: eleven target prior overrides and three target prior supersessions. The 22 physical paths are unique. Replacing fourteen current meanings and adding eight direct meanings yields 169 effective meanings without double replacement or loss. Inventory239 adds exactly the separately listed ten paths, changes or removes no predecessor row, and those ten paths are disjoint from the 22 qualified paths.

The operability description remains scoped correctly: 115 owner rows and 470 lexical mint rows are present, including the seven D4 additions over the 463-row parent census. It does not turn lexical matching or constructor metadata into D5 Cargo/cfg reachability or identity authority.

## Findings

None.

## Non-blocking observations

None.

## Acceptance boundary

This review accepts the exact description187 r3 design unit. It does not infer that R2 was bound, and it does not itself bind R3. Root assent, unchanged-verifier binding, status publication, and push remain separate. C4/native selection/Plan/signed-descriptor producers, production operation-lifetime enforcement, J2/H/CI4/source39/D5/platform/Linux/privacy/owner/clock/T2/CF, and full-project qualification remain open. `productQualification` is false.
