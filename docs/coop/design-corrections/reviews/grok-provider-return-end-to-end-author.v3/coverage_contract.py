"""Coverage counts and historical evidence constants for evaluator3 application.

These are existing guarded-stage obligations. They are not grades.
Historical Claude finding IDs and the v13 manifest digest stay historical.
"""
AR_IDS = tuple(f'AR-{i:02d}' for i in range(1, 17))
FW_IDS = tuple(f'FW-{i:02d}' for i in range(1, 16))
OWNER_IDS = tuple(f'DR-{i}' for i in range(201, 206))
INHERITED_PARENTS = tuple(f'DR-{i:03d}' for i in range(1, 12))
INHERITED_RESIDUALS = tuple(f'DR-011-R{i:02d}' for i in range(1, 17))
INHERITED_IDS = INHERITED_PARENTS + INHERITED_RESIDUALS
CONDITION2_IDS = (
    'DR-101', 'DR-102', 'DR-103', 'DR-104', 'DR-105', 'DR-106', 'DR-107',
    'DR-109', 'DR-110', 'DR-111', 'DR-112', 'DR-113', 'DR-114', 'DR-115',
    'DR-117', 'DR-118', 'DR-119', 'DR-120', 'DR-121', 'DR-122', 'DR-123',
    'DR-124', 'DR-125', 'DR-126', 'DR-127', 'DR-130', 'DR-131', 'DR-133',
)
CONDITION2_EXCLUDED = {
    'DR-108': 'credentials',
    'DR-116': 'third-party publisher/ecosystem',
    'DR-128': 'untrusted contributions',
    'DR-129': 'TUI',
}
GATE_IDS = tuple(f'DR-G{i:02d}' for i in range(1, 33))
EVALUATION_RESIDUAL_COUNT = 30
D9_CARRIED_ROWS = ('DR-007', 'DR-011-R08')
REQUIRED_FINDING_KEYS = ('newMustIssues', 'newShouldIssues')

# Historical evidence. Do not rename to Grok. Do not treat as evaluator3 acceptance.
HISTORICAL_V13_MANIFEST_SHA256 = '8e6670f74d6e0bbed50b6c4914b3c7b29f627221f1591f4add5567f652f4c023'
HISTORICAL_V13_MATRIX_CELLS = 60
HISTORICAL_V13_ADVISORY_IDS = ('CLAUDE-V13-ADV-1', 'CLAUDE-V13-ADV-2')
HISTORICAL_V21_SUBJECT_SHA256 = '360c2758c0409ebc307966c7a385c385c2d7f580b4623dd760b7ba0e26bf18c1'
HISTORICAL_CLAUDE_EXCLUDED_SESSION = '5dec928a-6357-4726-9ea8-49a3079fb726'

# Coauthor sessions observed in this collaboration. Independent review must not reuse them.
KNOWN_GROK_COAUTHOR_SESSIONS = (
    '0d7f2cda-0e54-45e1-9a68-a8782587a8a0',
    '3d9960a7-f46b-49e2-bb4f-96a8568e8619',
    '01a081ad-93f0-7d40-b717-ce8978680670',
)

assert len(AR_IDS) == 16
assert len(FW_IDS) == 15
assert len(OWNER_IDS) == 5
assert len(INHERITED_PARENTS) == 11
assert len(INHERITED_RESIDUALS) == 16
assert len(INHERITED_IDS) == 27
assert len(CONDITION2_IDS) == 28
assert len(GATE_IDS) == 32
