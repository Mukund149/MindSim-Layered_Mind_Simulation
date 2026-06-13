# MindState

## Responsibility

MindState is the **central data bus** of MindSim. It is the single entity responsible for all information exchange between layers. No layer communicates with another layer directly — all inter-layer data flows through MindState.

---

## Role

MindState represents the **complete current state of the mind** at any given moment. It is both a snapshot and a live store — updated continuously as each layer processes and produces output.

---

## Contents

| Field | Source | Description |
|---|---|---|
| `current_stimulus` | External input | The active stimulus being processed |
| `activation_map` | Neuron Layer | Map of fired cluster signals and their current strengths |
| `emotion_map` | Emotion Layer | Current emotional state after inertia, regulation, and compounding |
| `working_memory` | Memory Layer | Memories retrieved as context relevant to the current stimulus |

---

## Design Principle

MindState acts as a **shared blackboard**. Each layer reads what it needs from MindState and writes its output back to MindState. This decouples layers from each other and ensures that any layer can be modified, replaced, or inspected without requiring changes to the layers around it.
