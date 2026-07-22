# Influence V2 test strategy

## Baseline checks for this repository

Run Bash syntax validation for scripts, Python syntax compilation for helpers,
and `scripts/build.sh --help`. Run ShellCheck when available, matching CI.

## Narrative test strategy

The new workspace tests model state transitions, idempotent daily planning, and
narrative-state retrieval. Future increments must add structured provider
parsing, consequence application, migration, simulation integration, and
frontend operator/spectator tests. Deterministic provider fixtures must cover
career, creative, social, blocked/low-energy, relationship-conflict, and
no-provider cases.
