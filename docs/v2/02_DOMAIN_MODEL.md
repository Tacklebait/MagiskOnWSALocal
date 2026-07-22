# Influence V2 domain model

## Status

This is a target-model record, not an implementation in this repository. No
existing persistence layer exists here to host these entities safely.

## Required ownership model for the correct repository

* **Character** owns stable identity and continuing life state.
* **Goal** owns intended outcomes, hierarchy, status, and auditable progress.
* **Narrative arc** owns durable story progression and current state.
* **Narrative beat** owns a planned or completed meaningful unit of story.
* **Plan** owns time-bounded intentions from weekly through daily horizons.
* **Event** owns simulated occurrences and links back to narrative context.
* **Memory** owns subjective recollection, not formal progress state.
* **Post** owns published content and why it was shared.
* **World** owns shared environmental context only.

The implementation must use dedicated typed records with explicit transitions
and audit history; it must not collapse this state into a generic JSON blob.
