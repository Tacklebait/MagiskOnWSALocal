# Influence V2 test strategy

## Baseline checks for this repository

Run Bash syntax validation for scripts, Python syntax compilation for helpers,
and `scripts/build.sh --help`. Run ShellCheck when available, matching CI.

## Deferred narrative test strategy

The correct Influence repository must test model state transitions, idempotent
planning/execution, structured provider parsing, consequence application,
legacy-data migration, simulation integration, admin APIs, and frontend
operator/spectator workflows. Deterministic provider fixtures must cover
career, creative, social, blocked/low-energy, relationship-conflict, and
no-provider cases.
