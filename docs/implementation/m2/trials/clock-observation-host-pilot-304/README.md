# Clock observation host pilot304

Descriptive execution on this running host only. This is not platform, load, suspend, VM, namespace or S4 publication qualification, and does not select proposed302's one-second budgets. No product or trust state was changed.

The executable uses opensip-platform's existing public observe_clock via the rlib compiled from the pinned303 product. The source/library SHA and exact compile command are recorded. Raw wall and boot values are deliberately not printed; samples.ndjson records durations, counts and exceptional outcomes only. The exact executable is not needed as durable evidence; source, command and input pin permit rebuilding, while each new run will have different timings.

1000 no-injected-delay pairs: no errors, boot changes or reversed pair ordering; median sample span9375ns, p99 11916ns, maximum62042ns; pair age max75084ns.100 pairs with a requested2ms sleep: max pair age3099417ns.2 pairs with a requested1100ms sleep: both ages exceed1s (1108817167ns and1110085625ns). These are observations under the current process scheduling conditions, not portable bounds or claimed verification of the host publication protocol.

The pilot demonstrates the raw clock collector is callable and provides useful brackets on this machine. It deliberately does not create a qualified observation, run S4/S4.5, test proofs/fsync/capsule replacement, inject clock changes, pause the process, or exercise the complete proposed302 final-use gate. Those remain required before installation. The policy review must not count this narrow pilot as full qualification.
