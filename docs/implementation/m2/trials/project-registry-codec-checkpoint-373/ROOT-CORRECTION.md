# Correction to author373 fault evidence

The original nine author fault detections are INVALID. check_faults.py resolved its directory to /private/tmp but recorded compiler paths used /tmp. Its string replacement therefore did not redirect source/output paths to each mutant. Each check then failed to find the proposed mutant probe. Counting every nonzero Python exit as a semantic fault detection incorrectly counted FileNotFoundError. Those source/log/claims remain preserved in frozen373; they are not nine killed mutants. The ordinary differential37412 baseline was real and is unaffected.

The reviewer independently compiled actual mutants using explicit paths; root is separately auditing that evidence and requested an addendum, without rewriting its original report. This revised author runner constructs commands from explicit source/output paths, checks compiler success and artifact existence, and accepts only a structured mismatching result or the exact Rust typed-roundtrip/projection assertion from a running harness. A missing executable, compiler failure or other infrastructure error fails the control run and is never counted. Both aliasing and error classification require correction; fixing only path spelling would leave false-positive vulnerability.

Codec source bytes are unchanged. No native/product/source-policy acceptance is inferred from this harness repair.
