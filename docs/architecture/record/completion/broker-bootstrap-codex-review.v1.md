# Broker bootstrap review

OBJECT: one MUST-FIX, one SHOULD-FIX. All127 retained checks replay identically and all eight frozen inputs match.

BROKER-M1: request admission checks only the broker token; a valid HE-2 handle with explicit project-read denial still returns GRANTED. Check the underlying token and exact scope as well as the broker permission.

BROKER-S1: collision retry has no bound; add exhaustion refusal without launch.

The environment/strict parser/SDK identity work is sound within its declared reference scope. HE-2 data delivery remains a separately declared missing design dependency. Full details and retained reproduction are in the JSON verdict.
