# Project Overview: Disaster Response MAS

## Purpose
The Disaster Response MAS is designed to turn UAV disaster imagery into coordinated Search and Rescue (SAR) decisions. Based on the current repository materials, the system is intended to process sequential aerial images from the C2A dataset, extract scene and pose signals, maintain a persistent world model, and route those results through an agentic orchestration stack toward actionable response priorities.

This document reflects the current documented architecture in the repository. At the moment, the repo primarily contains blueprint-level guidance in `AGENTS.md`, so this overview describes the intended system design and engineering constraints rather than a fully implemented code path.

## Data Source
The documented source dataset is the C2A UAV image dataset, with 10,215 images referenced from Kaggle:

`https://www.kaggle.com/datasets/rgbnihal/c2a-dataset/`

The project framing suggests a sequential image simulator built on top of that dataset, which implies the system is expected to reason over evolving disaster scenes rather than isolated single-image inference alone.

## Five-Layer Architecture

### Layer 0 Mindset
Although the stack is described as a 5-layer architecture, the practical input to the system is raw UAV imagery entering through the gateway. The architectural goal is to transform those pixels into ranked rescue actions.

### L1: Perception
Perception is the first analytical layer and is explicitly parallel by design.

- A YOLO-based pose pipeline is responsible for structured visual detection.
- A Qwen2.5-VL scene understanding pipeline is responsible for richer semantic interpretation.
- Both are expected to run concurrently inside LangGraph.

This design matters because disaster scenes have two distinct information types:

- Localized visual evidence such as people, posture, or damage cues.
- Global scene context such as flood, fire, debris, blockage, and environmental hazard interpretation.

The documented engineering directive is that all vision logic must support concurrent execution. That means this layer should be built to avoid serialized perception bottlenecks.

### L2: World Model
The world model is the persistent memory of the system.

- PostgreSQL is the system of record.
- SQLAlchemy 2.0 is the required persistence interface.
- Stored entities include zones, tasks, and historical trends.

This layer is where transient detections become structured operational state. In practice, that means perception outputs should be normalized into durable records that support re-querying, trend analysis, and downstream planning.

### L3: Intelligence
The intelligence layer consists of specialized CrewAI agents consuming tools via FastMCP.

This indicates a tool-using agent layer that operates over the world model and perception outputs rather than performing raw vision itself. Its likely responsibilities include:

- Interpreting zone severity.
- Recommending task prioritization.
- Coordinating follow-up actions.
- Using shared tools consistently through an MCP interface.

The design strongly suggests that agent behavior should be observable, structured, and integrated with the rest of the orchestration flow rather than acting as an isolated chatbot layer.

### L4: Orchestration
LangGraph is the control plane for execution flow.

- It manages parallel execution.
- It routes state between layers and nodes.
- It is responsible for branching, joins, and progression through the workflow.

This layer is especially important because the project depends on concurrent perception and multi-agent reasoning. LangGraph is the place where those paths are coordinated into a deterministic operational workflow.

### L5: Observability
Observability is a first-class architectural layer, not an afterthought.

- OpenTelemetry traces are required across graph nodes and agent tools.
- A Streamlit BI dashboard is intended to expose operational and analytical visibility.

The observability requirement implies the system should support both:

- Runtime inspection of how work flows through the MAS.
- Operator-facing monitoring of outcomes, bottlenecks, and historical behavior.

## Triage and Priority Formula
The current documented triage formula is:

```text
UrgencyScore = ((Critical * 10 + High * 5 + Medium * 2) / max(Total, 1)) * HazardMultiplier
```

### Interpretation
- `Critical`, `High`, and `Medium` represent counts of findings or individuals in each severity band.
- The weighting scheme emphasizes critical cases most heavily, then high-severity, then medium-severity.
- `max(Total, 1)` prevents division by zero and normalizes the score by the total number of observations.
- `HazardMultiplier` adjusts the normalized severity score according to environmental risk or situational danger.

### Operational Effect
This formula produces a composite zone-level urgency score rather than a raw count. That is a better fit for disaster triage because it balances:

- Severity mix.
- Total detected population or events.
- Contextual hazard escalation.

The practical implication is that a zone with fewer people but much higher severity or hazard exposure can outrank a larger but less critical zone.

## Specialized Sub-Agents
The repo-level guidance defines three specialized sub-agents for complex tasks.

### `@vision-debugger`
Use this agent when the perception pipeline is the problem area.

- Investigates model failures in the YOLO or Qwen2.5-VL path.
- Diagnoses VRAM pressure and inference resource issues.
- Supports perception refactoring and pipeline stabilization.

This role is best suited to failures involving detection quality, GPU memory behavior, batching, preprocessing, postprocessing, or multimodal inference integration.

### `@scenario-simulator`
Use this agent when the system needs realistic input generation or controlled testing scenarios.

- Creates test cases.
- Generates mock JSON payloads.
- Simulates disaster zones and evolving conditions.

This role is important because a disaster-response system needs repeatable scenarios for workflow validation, regression testing, and scoring logic checks.

### `@graph-validator`
Use this agent when orchestration logic needs inspection.

- Audits `src/graph/workflow.py`.
- Looks for logic deadlocks or bad routing.
- Optimizes state handoffs between graph stages.

This role is specifically aligned with LangGraph correctness, especially where concurrency, joins, retries, or state mutation can produce subtle workflow bugs.

## Observability Implementation Model
The repo explicitly requires OpenTelemetry instrumentation for every agent tool and graph node. Based on that directive, observability in this system should be implemented around traceable execution units.

### Required Instrumentation Targets
- FastAPI request lifecycle spans.
- LangGraph node spans, especially parallel perception branches.
- CrewAI agent tool invocation spans.
- Database interaction spans around the SQLAlchemy world model.
- Cross-layer correlation identifiers so one incident can be followed end to end.

### Why This Matters
In a multi-agent, parallel, vision-heavy system, failures are often distributed:

- A perception branch may degrade without fully failing.
- A graph node may stall on a join or state transition.
- An agent tool may return valid syntax but bad semantics.
- Persistence may succeed while downstream orchestration misinterprets the result.

Without tracing, those issues are difficult to localize. OpenTelemetry gives the system the structure needed to answer questions such as:

- Which node introduced latency?
- Which tool call changed the final task priority?
- Which zone record was written from which perception result?
- Where did a workflow branch fail or diverge?

### Operator-Facing Visibility
The documented Streamlit BI dashboard suggests a second observability surface beyond tracing:

- System health and throughput.
- Zone-level trends.
- Historical task allocation patterns.
- Potential audit views for urgency scoring outcomes.

That makes observability both a developer concern and an operational one.

## Engineering Directives That Shape Implementation
Three directives define the project’s implementation posture:

### Parallel Perception
The perception layer must be concurrent. This is a design requirement, not an optimization.

### OTel Tracing Everywhere
Observability must cover graph nodes and agent tools consistently. Instrumentation gaps will make distributed debugging materially harder.

### SQLAlchemy 2.0 World Model
All persistence must route through the PostgreSQL-backed world model using SQLAlchemy 2.0. That centralizes state management and avoids fragmented storage logic.

## Current Repository State
At the time of writing, the repository appears to be in an early blueprint stage. The locally visible files are primarily:

- `AGENTS.md`
- `project_structure.md` (currently empty)

Because of that, this overview represents the current documented understanding of the Disaster Response MAS rather than a code-verified architecture walkthrough. As implementation files appear, this document should be updated to reference concrete modules, APIs, schemas, traces, and dashboards.
