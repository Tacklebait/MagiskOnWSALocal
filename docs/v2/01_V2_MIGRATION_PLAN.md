# Influence V2 migration plan

## Decision and delivery boundary

Create Influence V2 in the isolated `influence/` workspace after the user
explicitly requested a new project. The legacy WSA utility stays unchanged.

## Required input to continue

The implementation starts from a new bounded foundation. Its next increments
are:

1. Re-run the audit against actual backend, frontend, data, and runtime flows.
2. Add additive goal, narrative arc, beat, plan, and consequence persistence.
3. Add typed services and deterministic fallback planning.
4. Expose compatible admin APIs and evolve daily arcs to daily chapters.
5. Integrate planned beats into the existing simulation and content flow.
6. Add admin and spectator presentation without removing legacy views.
7. Validate migrations, tests, observability, and deprecation paths.

## Preservation rule

No WSA build, download, installer, or configuration file is a valid target for
Influence domain changes. All new runtime files live below `influence/`.
