# API Gateway Standards: FastAPI

## 1. Objective
To provide a high-performance, asynchronous REST interface for the Disaster Response MAS.

## 2. Implementation Rules
*   **Asynchronous Endpoints:** All route handlers MUST be defined with `async def` to prevent blocking the event loop during model inference.
*   **Pydantic Validation:** Every request (e.g., zone metadata) and response (e.g., triage summary) MUST use Pydantic models derived from the World Model schemas.
*   **Dependency Injection:** Use FastAPI `Depends` to inject the PostgreSQL session and the OpenTelemetry tracer into route handlers.
*   **File Handling:** Large UAV images must be handled using `UploadFile` to allow streaming and efficient memory usage.

## 3. Endpoint Structure
*   `POST /analyze`: The primary endpoint. Receives an image, generates an `image_hash`, and triggers the `disaster_app.ainvoke()` LangGraph call.
*   `GET /zones/{zone_id}`: Retrieves the current state of a specific disaster zone from PostgreSQL.
*   `GET /health`: Returns the status of the Ollama (Qwen) and PostgreSQL connections.

## 4. Telemetry Requirements
*   Every request must start a root span.
*   The `TraceID` from the API layer must be propagated through the LangGraph nodes to the CrewAI agents.