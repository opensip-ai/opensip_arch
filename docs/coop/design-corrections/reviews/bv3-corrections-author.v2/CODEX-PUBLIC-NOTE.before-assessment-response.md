# Additional concrete M2 admission gap from Codex — assess with this follow-up

While you address the five prompt points, Codex reviewed the COMPLETE v12->v1 diffs of all three models and found one affected policy/Run admission join that still differs. This is within the existing M2 scope, not a new product feature.

Actual probe and result are retained at:
`/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/codex-post-reset.v1/bv3-policy-evidence-declaration.v1/`

Read both files and the custody explanation. The probe uses the same exact released v1 source and extracted synthetic builder already accounted in your root-input. It changes the atom in place before graph construction, so policy, compiled program and addressed witness all carry the same predicate. The legal positive control has runtime-observation@observed, evidence=runtime and evidenceUse=[{kind:runtime,requirement:required}]. Both normal policy admission and retained Run closure admit it. The second case omits ONLY that rule-level evidenceUse declaration: resolve_policy refuses IMPORT.ABSENT_FOR_PREDICATE, yet M.close_run ADMITs the full Run. Both examples are empty/indeterminate with absent runtime evidence; this is a declaration-admission inconsistency, not a claimed false finding or native execution exploit.

The new foundation open_run_closure loop calls W.admit_atom for policy/program atoms but omits resolve_policy's matching rule-level evidenceUse check. Reuse the complete relevant policy admission at that boundary (and retain compiled-program atom checks/compilation join), or otherwise enforce precisely the same declared evidence obligation with valid controls. Do not weaken resolve_policy or relabel the missing declaration valid. No new host product implementation is needed. Preserve the successful16 pure-helper cases; their recorded scope explicitly did not prove host admission, so the new counterexample does not rewrite them.

Please include this concrete point in your assessment/handoff along with the five existing prompt points. Read this full note before the next substantive batch and before handoff; hashing it is not evidence of substantive review. Original v1 reports remain immutable.
