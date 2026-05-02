---
name: db-migration
description: Manages idempotent PostgreSQL schema updates for the Disaster Response World Model.
---

# Skill: PostgreSQL Migration Management
**Description:** Manages idempotent schema updates for the SQLAlchemy World Model.

## Trigger
Use this when "updating database models," "adding a table," or "modifying the schema."

## Execution Steps
1.  **Model Sync**: Check `src/world_model/models.py` for changes.
2.  **Idempotency**: Generate a script in `scripts/migrate.py` that uses `CREATE TABLE IF NOT EXISTS` or SQLAlchemy's `checkfirst=True`.
3.  **Data Types**: Force the use of `JSONB` for `pose_distribution` and `TIMESTAMPTZ` for all event logging.
4.  **Verification**: After running, query the `information_schema.tables` to confirm the update.