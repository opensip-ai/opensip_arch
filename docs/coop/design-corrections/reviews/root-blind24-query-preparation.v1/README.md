# Current-format blind query verifier preparation

The new reader requires explicit frozen source/manifest and transport-reader hashes, Run id/label, exact export and vector paths. It supports blind24 objectTable lists and vectors[].hostObservations. It imports only root transport and frozen owners; no consumer code, repair, cursor translation or response-derived inputs.

Three synthetic boundary controls pass: structural refusal makes zero semantic/query calls; semantic refusal makes zero query calls; admitted control preserves exact request/host values and isolates mutations. The actual53 vector rows parse into explicit Run-label partitions only. This is not53 executed owner queries.

Actual barrier attempt1 accidentally supplied the consumer replay receipt instead of its store export and refused transport (missing objectTable). Attempt2 supplied the exact cmp-code.store.json: transport ADMIT, structural REFUSE for missing subject3:0d7170cae3291421f00d9736aeae56cb4a8369be74bb9e4389c22ac34e5bc26a, semantic NOT-REACHED, zero query calls. Both preserved. Attempt2 meets the intended prerequisite barrier; neither is consumer acceptance.

Future successful source/Run admission and substantive response/surface/token assessment remain required. Exit zero from this capture tool means capture completion only, never conformance. Negative missing/corrupt-byte vector labels need their actual retained input artifacts; the tool does not invent their mutations. This root verifier and all reports stay outside the blind normative kit.
