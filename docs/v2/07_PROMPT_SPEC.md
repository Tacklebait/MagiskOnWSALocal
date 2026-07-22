# Influence V2 prompt specification status

No paid LLM provider is required for the initial slice. The deterministic
daily-chapter fallback is schema-valid and idempotent. Future provider adapters
must version their templates and typed input/output schemas, and never mutate
state without deterministic validation.
