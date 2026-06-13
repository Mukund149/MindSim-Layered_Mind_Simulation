# Archive: Previous Pipeline Order (v1)

## Previous Design

```
Neuron Layer → Emotion Layer → Memory Layer → Personality Layer → Cognition → Meta-Cognition → Dream Layer
```

Memory retrieval occurred **after** emotion generation. Meta-Cognition was a separate layer following Cognition.

---

## Why It Was Created

This was the initial architecture design. The ordering followed an intuitive flow: perceive (neurons) → feel (emotion) → recall (memory) → personality filter → think → dream.

---

## Problems Discovered

- Emotions were generated without any memory context. The system had no way to modulate emotional response based on prior experience at the emotion-generation stage.
- Memory retrieved post-emotion had no pathway to influence the emotion already produced in that cycle.
- Meta-Cognition as a separate sequential layer added latency without clear benefit over combining it with Cognition.

---

## Why It Was Replaced

The current architecture moves Memory retrieval **before** the Emotion Layer so that retrieved memories can directly participate in emotion generation. Cognition and Meta-Cognition were merged into a single combined step. See [ADR-001](../adr/ADR-001-memory-before-emotion.md).
