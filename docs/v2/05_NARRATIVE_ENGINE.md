# Influence V2 narrative engine

The initial narrative engine is a deterministic fallback planner in
`influence/backend/app/services.py`. It keeps planning separate from execution
and creates one schema-valid scheduled beat per active arc/date, idempotently.
LLM providers, consequence proposals, and simulation execution are intentionally
deferred until their typed boundaries are added.
