# Influence V2 migration plan

## Decision

Do not implement Influence V2 in `MagiskOnWSALocal`. The audited codebase has
none of the prerequisite application or data systems. Creating them here would
violate the requirement to evolve an existing application incrementally rather
than build a greenfield prototype.

## Required input to continue

Provide the checkout containing the Influence FastAPI backend, Next.js
frontend, PostgreSQL migrations, and existing simulation/domain systems. Once
available, use this sequence:

1. Re-run the audit against actual backend, frontend, data, and runtime flows.
2. Add additive goal, narrative arc, beat, plan, and consequence persistence.
3. Add typed services and deterministic fallback planning.
4. Expose compatible admin APIs and evolve daily arcs to daily chapters.
5. Integrate planned beats into the existing simulation and content flow.
6. Add admin and spectator presentation without removing legacy views.
7. Validate migrations, tests, observability, and deprecation paths.

## Preservation rule

No WSA build, download, installer, or configuration file is a valid target for
Influence domain changes. This documentation-only change preserves all current
runtime behavior.
