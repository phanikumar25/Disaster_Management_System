# Storage Layer: PostgreSQL & Caching

## 1. Database Schema[cite: 1]
*   **Zones:** `zone_id`, `severity`, `survivor_metrics`, `last_updated`.
*   **Tasks:** `task_id`, `zone_id`, `type`, `status`, `assigned_agent`.
*   **InferenceCache:** `image_hash` (MD5), `zone_report_json`.

## 2. Persistence Standards
*   Use `SQLAlchemy 2.0` with connection pooling[cite: 1].
*   Use `PostgresSaver` for LangGraph checkpointing to allow for parallel node crash recovery[cite: 1].