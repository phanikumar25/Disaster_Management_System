# Perception Layer: YOLO & Pose Classification

## 1. Goal
Detect all visible humans and classify their poses to infer medical urgency[cite: 1].

## 2. Pose-to-Urgency Mapping[cite: 1]
| Pose ID | Label | Urgency Level | Triage Tag |
| :--- | :--- | :--- | :--- |
| 0 | Bent | **CRITICAL** | Red (Immediate) |
| 1 | Kneeling | HIGH | Yellow (Delayed) |
| 2 | Lying | **CRITICAL** | Red (Immediate) |
| 3 | Sitting | HIGH | Yellow (Delayed) |
| 4 | Upright | LOW | Green (Minor) |

## 3. Technical Requirements
*   **Small Object Detection:** 47% of C2A annotations are < 10px[cite: 1]. You MUST use **SAHI** (Sliced Aided Hyper Inference) for images > 1280px[cite: 1].
*   **Implementation:** The `yolo_node` must return `{"raw_detections": list[Detection]}`[cite: 1].