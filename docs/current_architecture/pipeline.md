# Architecture Pipeline

## Current Pipeline

```
Neuron Layer
     │
     ▼ (activation_map → MindState)
Memory Layer  ◄── (retrieval: pulls memories relevant to current stimulus)
     │
     ▼ (working_memory → MindState)
Emotion Layer ◄── (reads activation_map + working_memory from MindState)
     │
     ▼ (emotion_map → MindState)
Personality Layer ◄── (modulates emotion_map based on current personality)
     │
     ▼
Cognition + Meta-Cognition ◄── (reads all MindState data; generates response)
     │
     ▼
Memory Layer  ◄── (storage: converts response to memory and stores it)
     │
     ▼
Dream Layer  (background/idle state — design pending)
```

---

## Layer Summary

| Layer | Input | Output |
|---|---|---|
| Neuron Layer | Raw stimulus | `activation_map` in MindState |
| Memory Layer (retrieval) | `activation_map` | `working_memory` in MindState |
| Emotion Layer | `activation_map`, `working_memory` | `emotion_map` in MindState |
| Personality Layer | `emotion_map` | Modulated emotion state |
| Cognition + Meta-Cognition | All MindState data | Final response |
| Memory Layer (storage) | Final response | Stored memory in brain |
| Dream Layer | (TBD) | (TBD) |

---

## Key Structural Decision

Memory retrieval was moved **before** the Emotion Layer in the current architecture. This allows retrieved memories to inform emotion generation — a stimulus is assessed not just on its raw appraisal clusters, but in the context of what the brain already remembers about similar situations.

In the previous architecture, memory retrieval occurred **after** the Emotion Layer, meaning emotions were generated without memory context.

See [ADR-001](../adr/ADR-001-memory-before-emotion.md) for the full decision record.
