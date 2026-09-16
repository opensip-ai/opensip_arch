# Root assessment of the authored discovery correction

The complete authored report and all model/prose patches were read. Root reproduces two version-handoff problems: schema-valid V1 provenance with no pruned rows silently becomes V2; schema-valid V1 boundary rows are accepted by input dispatch and then rejected under UnitDiscoveryV2 for missing markerCountBasis. Historical reading must remain explicit without silent upgrade. The packaged reproduce.sh also references unpopulated WORK scripts and precreates a copy that the XA01 applier itself owns. A focused Claude continuation is required before integration. Existing positive controls remain separate evidence.

Correction after reading the applier: the pre-copy itself is lawful and required; that suspicion is withdrawn. The executed packaging control reaches successful three-file XA01 application, then fails because WORK/apply-correction.py was never supplied. Full stdout/stderr retained in reproduction-control.json.
