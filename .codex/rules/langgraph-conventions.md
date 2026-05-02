# Orchestration Layer: LangGraph & State Management

## 1. State Definition (`DisasterState`)
The state must be a `TypedDict` containing[cite: 1]:
*   `raw_detections`: Intermediate YOLO output.
*   `scene_context`: Intermediate VLM output.
*   `current_zone_report`: Final aggregated Pydantic model.
*   `triage_output`: LLM ranking and severity flags.

## 2. Parallel Node Topology[cite: 1]
1.  **START** → Branch to `yolo_node` AND `qwen_node` (Parallel Fan-out).
2.  `yolo_node` + `qwen_node` → Join at `zone_builder_node` (Fan-in).
3.  `zone_builder_node` → `triage_node`.
4.  `triage_node` → `route_after_triage` (Conditional Edge).

## 3. Urgency Scoring Formula[cite: 1]
$$UrgencyScore = \frac{(Critical \times 10 + High \times 5 + Medium \times 2)}{\max(Total, 1)} \times HazardMultiplier$$

## 4. Routing Logic[cite: 1]
*   Score >= 7.5 OR Critical Count >= 3 → `alert_node` → `resource_node`.
*   Score >= 3.0 → `resource_node`.
*   Else → `END`.