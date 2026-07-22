"""Initial Influence V2 narrative foundation.

The runtime currently creates the same additive schema for local SQLite
development. This revision is retained as the authoritative PostgreSQL
migration boundary when Alembic is enabled in deployment.
"""

revision = "20260722_01"
down_revision = None


def upgrade():
    # Schema is defined in app.models and applied by the deployment migration job.
    # Kept explicit rather than destructive: no legacy WSA tables are touched.
    pass


def downgrade():
    # Narrative history must not be removed automatically.
    pass
