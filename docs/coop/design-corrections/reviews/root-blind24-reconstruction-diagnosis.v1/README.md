# Exact blind24 export failures

**ROOT-B24-01**

All25 structurally refused exports lack a promised evaluation-subject frame. Directly inspected ts-pass has only subjects attached to its two findings. Consumer evaluator enumerates every selected subject and places each identity in proof predicate rows, but inserts evaluation-subject into output objects only inside mint_finding (line713). Closure/digestlaw inspect explicitly admitted records and bare digest annotations; they do not generally resolve typed-prefix references in the proof. Complete replay compares only its own incomplete output map, so this omission is shared by builder and checker. The normative composition section7 requires every subject descriptor and every referenced output preimage. Identity closing-digest law explicitly excludes typed prefixes from bare-hex annotations because their prefixes select identity domains, not because the references need no retained bytes. No design change or exported-byte repair made. This root diagnosis is nonblind evidence and must not be supplied to the blind origin as an oracle.

**ROOT-B24-02**

cmp-empty reaches semantic join but refuses ENUMERATION_BINDING_PROGRAM_ENTRY. Its retained EnumerationPlan program bindings combine provenance=default-unit with programEntry=tsconfig.json. Source37/38 EnumerationPlan schema AvailableBinding.programEntry explicitly says U-1 default uses null and host derives the actual graph entry; enumeration model refuses a nonnull entry on default-unit. Graph entry may itself still be tsconfig.json. Exact export is preserved unchanged; no expected replacement Run constructed or validator relaxed. This first failure masks any later semantic mismatch and is not a claim that correcting this field would complete replay.
