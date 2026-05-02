# Data Layer: UAV Feed Simulation

## 1. Sequential Image Replay
*   The `ImageFeedSimulator` must yield images from the C2A test split in alphabetical order to simulate a stable drone trajectory[cite: 1].
*   Images must be grouped into "Zones" (default: every 10 sequential images)[cite: 1].

## 2. Inference Cache Logic
*   Before triggering parallel nodes, compute the MD5 hash of the current image.
*   If the hash exists in the `InferenceCache` table, skip perception and load the existing `ZoneReport`[cite: 1].