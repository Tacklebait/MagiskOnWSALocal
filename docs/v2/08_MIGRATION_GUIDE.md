# Influence V2 migration guide status

There is no database or migration framework in this repository. No migration
was created, because adding a PostgreSQL schema to a WSA build utility would be
unsafe and unrelated. In the actual Influence repository, migrations must be
additive, preserve legacy free-form goals and daily-arc history, be idempotent,
and provide intentional indexes and foreign-key behavior.
