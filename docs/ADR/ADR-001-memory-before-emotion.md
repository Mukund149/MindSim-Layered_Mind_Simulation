# ADR-001: Memory Retrieval Before Emotion Layer

**Status:** Accepted

---

## Context

In the original pipeline, the layer order was:

```
Neuron Layer → Emotion Layer → Memory Layer → Personality Layer → Cognition → Meta-Cognition → Dream Layer
```

Memory retrieval occurred after the Emotion Layer. This meant the emotion generation step had no access to prior memories when computing the emotional response to a stimulus.

The design question was: should memory context be available to the emotion layer when generating emotions, or should emotions be generated purely from the raw appraisal signals of the current stimulus?

---

## Decision

Move Memory retrieval to occur **before** the Emotion Layer. The new pipeline order is:

```
Neuron Layer → Memory Layer (retrieval) → Emotion Layer → Personality Layer → Cognition + Meta-Cognition → Memory Layer (storage) → Dream Layer
```

---

## Alternatives Considered

- **Keep memory after emotion:** Simple ordering, but emotions are generated without any experiential context — the brain cannot modulate its emotional response based on prior experience at generation time.
- **Provide memory to emotion as a secondary input without reordering:** Architecturally messier; memory would need to be triggered mid-pipeline rather than as a clean sequential step.

---

## Consequences

**Benefits:**
- Retrieved memories are available to the Emotion Layer and can participate in emotion generation.
- The emotional response to a stimulus can be modulated by what the brain already knows or has experienced — closer to biological emotional processing.
- Cognition + Meta-Cognition were also merged into a single step, simplifying the tail end of the pipeline.

**Tradeoffs:**
- Memory retrieval now adds latency at the start of each stimulus cycle before emotion generation.
- The interaction between retrieved memories and emotion scoring is not yet fully specified.
