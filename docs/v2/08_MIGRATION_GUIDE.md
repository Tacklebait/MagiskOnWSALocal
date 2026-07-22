# Influence V2 migration guide status

The new workspace defines the initial additive narrative schema in SQLAlchemy
and includes a revision boundary under `influence/backend/alembic/versions/`.
SQLite is supported for local development and PostgreSQL is provided through
Docker Compose. Before production, replace the placeholder migration body with
generated/validated Alembic DDL and add legacy backfill tests.
