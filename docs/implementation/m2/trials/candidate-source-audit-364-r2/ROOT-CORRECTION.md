# Root correction to frozen364 prose counts

The machine result in frozen364 unlisted-files.json reports213 unlisted files,133 fixtures and80 Rust sources. The frozen README/LAYOUT-adjacent root summaries incorrectly state79/134. Root introduced that prose arithmetic error while correcting the r4 heuristic: r4 actually classified132 fixtures and81 other files; one of those81 was storage/fixtures/pin-budget174.json. Final r5 correctly classifies133 fixtures and80 Rust sources. The earlier preliminary80/133 total was already right despite this separate r4 heuristic error.

All regeneration, full-scalar comparisons and source pins remain unchanged. The actual r5 machine report is correct. Root is preparing a separate364-r2 metadata correction preserving frozen364 verbatim. Please assess the correct80/133 counts, record the original prose finding, and do not accept the wrong79/134 claim. No test rerun or source change is asserted by this documentation correction.
