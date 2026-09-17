# Import payload layout v23

Adds evaluator/import_payloads.rs, evaluator/import-payload-registry.json and host/tests/fixtures/import-payload-fixtures.json. All387inherited rows remain equal by value, yielding390files and unchanged20packages/DAG. Pure schema/payload admission stays in evaluator; imports.rs in host retains workflow I/O. A closed independently derived registry checks two-key selection and owner binding drift. No new identity API, production dependency or package is introduced.

The separate fixture shares raw blobs across explicit requests to remain under the existing4MiB parser cap, without changing runtime limits. Prior native and import-correspondence fixture bytes stay unchanged. This layout approves neither payload source29 nor the proposed import-totality reference correction.

Parent is the accepted inventory22candidate. Runtime14 is separately under review on20/28base and must activate before this inventory. Its direct imported-schema description override must be inherited alongside the three earlier overrides whenever it is selected. Project all applicable description overrides by stable file path; do not hard-code the earlier count of three. Source review, runtime composition and private activation remain required.
