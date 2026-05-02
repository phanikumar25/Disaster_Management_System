# Perception Layer: Qwen2.5-VL Scene Classification

## 1. Goal
Provide rich, multimodal context for the disaster environment to influence hazard multipliers[cite: 1].

## 2. Scene Hazards & Multipliers[cite: 1]
| Scene Type | Hazard Multiplier | Primary Risk |
| :--- | :--- | :--- |
| **Fire** | 1.5x | Smoke, Toxic Gas, SCBA requirement |
| **Collapsed Building** | 1.4x | Rubble, Void Spaces, USAR requirement |
| **Flood** | 1.3x | Swift Water, Hypothermia, Boat requirement |
| **Traffic Accident** | 1.0x | Fuel Spills, Extraction requirement |

## 3. Implementation
*   **Model:** Qwen2.5-VL-7B via local Ollama endpoint[cite: 1].
*   **Output:** The `qwen_node` must return `{"scene_context": json_string}` containing both the hazard type and a 1-sentence context description[cite: 1].