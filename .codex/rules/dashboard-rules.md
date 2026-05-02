# Observability Layer: Streamlit Dashboard

## 1. Architectural Constraints
*   **Deterministic Only**: The dashboard is a read-only interface. NO AI AGENTS or LLM calls are allowed within this directory[cite: 1].
*   **Source of Truth**: All data must be pulled directly from the PostgreSQL database using SQLAlchemy[cite: 1].

## 2. Required Metrics & Views[cite: 1]
*   **Metrics Row**: Display 'Total Survivors Detected', 'Active CRITICAL Zones', 'Alerts Dispatched', and 'Pipeline Latency'[cite: 1].
*   **Zone Map**: Use `streamlit-folium` to map zones. Circle markers must be color-coded by urgency (Red for CRITICAL, Green for LOW)[cite: 1].
*   **Live Vision Feed**: Render the latest image with `supervision` bounding box overlays drawn from the `Detection` table[cite: 1].
*   **Audit Trail**: A scrolling list of JSONL logs showing agent decisions and tool invocations[cite: 1].