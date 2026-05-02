---
name: node-scaffold
description: Generates thread-safe, instrumented LangGraph nodes for the Disaster MAS.
---

# Skill: Scaffold LangGraph Node
**Description:** Generates thread-safe, instrumented LangGraph nodes for the Disaster MAS.

## Trigger
Use this when asked to "create a node," "add a step to the graph," or "implement a vision/agent node."

## Execution Steps
1.  **State Contract**: Verify the field being updated exists in `DisasterState`.
2.  **Telemetry**: Wrap the function with the OpenTelemetry tracer: `@tracer.start_as_current_span("[node_name]")`.
3.  **Function Pattern**:
    
```python
    def [node_name](state: DisasterState) -> dict:
        \"\"\"
        Input: state['[field]']
        Output: Updates [field]
        \"\"\"
        try:
            # Logic here...
            return {"[field]": [result]}
        except Exception as e:
            logger.error(f"Node [node_name] failed: {e}")
            return {} # Safe return to allow graph merge
    ```
4.  **Immutability**: Ensure the function returns a **new dictionary** and does not modify the `state` object in-place.