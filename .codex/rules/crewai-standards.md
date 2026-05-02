# Intelligence Layer: CrewAI Agents & Specialists

## 1. Agent Roles & Goals[cite: 1]
*   **Triage Analyst:** (Sonnet) Sorts survivors and ranks zone priorities.
*   **SAR Coordinator:** (Sonnet) Assigns USAR/Water/SCBA teams to zones.
*   **Medical Officer:** (Sonnet) Allocates resources based on pose-inferred trauma.
*   **Logistics Coordinator:** (Haiku) Manages asset routing and supply chains.
*   **Alert Officer:** (Haiku) Composes concise, ICS-standard operator alerts.

## 2. Tool Consumption
*   Agents MUST NOT use local tools. All tools are discovered via the **FastMCP Server**[cite: 1].
*   Agents rely on tool **docstrings** to match their current goal to the required tool functionality[cite: 1].