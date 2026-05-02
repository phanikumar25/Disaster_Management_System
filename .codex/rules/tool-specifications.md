# Agent Tool & FastMCP Specifications

## 1. Goal
Provide agents with a decoupled, discoverable service layer to interact with the PostgreSQL World Model and external services.

## 2. FastMCP Architecture
*   **Discovery**: All tools must be registered on the `Disaster-Tools-MCP` server using the `@mcp.tool()` decorator.
*   **Docstrings**: Tools are selected by agents based on docstrings. Descriptions must be optimized for machine discovery (e.g., "Retrieves past ZoneReports from the database to identify severity trends").

## 3. Tool Registry
### Perception & History
*   `get_zone_history(zone_id, n=5)`: Fetches the last N ZoneReports from the `zone_reports` table.
*   `compute_urgency_delta(zone_id)`: Calculates the shift in severity between the two most recent detections.

### Triage & Resource Dispatch
*   `classify_zone_severity(zone_report_json)`: Maps urgency and scene type to an ICS severity level.
*   `rank_zones_by_priority()`: Returns an ordered list of zones sorted by composite priority.
*   `assign_sar_team(zone_id, team_type, priority)`: Enters a new row into the `tasks` table[cite: 1].
*   `get_available_agents(agent_type)`: Queries the `agents` table for personnel with status='AVAILABLE'[cite: 1].

### Communications & Safety
*   `check_alert_deduplication(zone_id, window=10)`: Prevents redundant alerts within a 10-minute window[cite: 1].
*   `compose_operator_alert(...)`: Formats structured text based on ICS-standard messaging[cite: 1].