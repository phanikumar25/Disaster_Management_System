# Disaster Response MAS: Agent Registry & Blueprint

## 1. Project Objective
This system automates the analysis of UAV disaster imagery to optimize Search and Rescue (SAR) resource allocation[cite: 1]. It utilizes a 5-layer architecture to transform raw pixels into coordinated emergency responses[cite: 1].

** Data Source **
Sequential image simulator utilizing the C2A dataset (10,215 UAV images)[cite: 1].(** from kaggle:- https://www.kaggle.com/datasets/rgbnihal/c2a-dataset/)

## 2. System Architecture
*   **Gateway (FastAPI):** The asynchronous entry point for image uploads and real-time status queries.
*   **L1 (Perception):** Parallel YOLO (Pose) and Qwen2.5-VL (Scene) nodes executing in LangGraph.
*   **L2 (World Model):** Persistent PostgreSQL storage for zones, tasks, and historical trends.
*   **L3 (Intelligence):** Specialized CrewAI agents consuming tools via FastMCP.
*   **L4 (Orchestration):** LangGraph state machine managing parallel execution and routing.
*   **L5 (Observability):** OpenTelemetry-instrumented traces and a Streamlit BI dashboard.

## 3. Core Formulas
The system calculates a composite priority for every zone using the following formula:
$$UrgencyScore = \frac{(Critical \times 10 + High \times 5 + Medium \times 2)}{\max(Total, 1)} \times HazardMultiplier$$

## 4. Core Engineering Directives
- **Parallel Perception**: All vision logic must support concurrent execution.
- **OTel Tracing**: Every agent tool and graph node must be instrumented for observability.
- **Postgres Backend**: All persistence must go through the SQLAlchemy 2.0 World Model.

## 5. Specialized Sub-Agents
When faced with complex domain-specific tasks, delegate to the following agents:

- **@vision-debugger**: Use for perception pipeline failures, VRAM issues, or vision model refactoring.
- **@scenario-simulator**: Use to create test cases, generate mock JSON payloads, or simulate disaster zones.
- **@graph-validator**: Use to audit `src/graph/workflow.py`, check for logic deadlocks, or optimize state handoffs.

