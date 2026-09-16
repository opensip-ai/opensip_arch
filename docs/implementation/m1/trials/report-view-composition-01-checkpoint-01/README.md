# Report view composition01 — staged integration

The current profile6 reader uses codec02 generated contracts. Evidence presentation now accepts the actual generated EvidencePanelV1 and source union, preserving retained Run IDs and displaying ephemeral Plan/evidence without inventing a Run. Overview, evidence, catalog and local navigation compose against32 current report projections. This is a three-view integration harness, not a completed application.

Navigation closes open dialogs inside a view before hiding it. Browser02 exposed the top-layer modal remaining active after a hash/history route change; browser03 verifies closure and focus restoration. Browser04 adds visual spacing between a focused expanded summary and its first field label. Source and failure evidence are preserved.

Strict TypeScript compilation and14 Chrome checks pass: all32 reports decode/compose; old profile refuses without partial data; exact source/row identities survive; retained and ephemeral forms are distinct; manual keyboard navigation works; help closes when routing hides its view; unknown routes show unavailable; disposal removes controls/listeners. Desktop/narrow retained screenshots and the unchanged ephemeral narrow screenshot were inspected. Page network is blocked and private Chrome profiles are closed after each run.

Nine parent inputs and140 compiler files are pinned. Only four local sources change: report-data.ts, evidence-view.ts, navigation.ts and report.css. Other copied view/help/generated modules remain exact. The reader validates format/version, not host source or native evidence custody. Extra source confidence is never inferred by display.

Pending: actual independent review, other report views, final application/assets/CSP/static parity and host delivery, supported-browser and accessibility release qualification. No product files were installed and no milestone is complete.
