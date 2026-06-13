# Neuron Layer

## Responsibility

The neuron layer is the entry point for all stimuli. It converts raw input into a structured activation map of neuron clusters, applies Hebbian learning for pattern-based boosting, and decays activations over time to create a persistent lingering effect.

---

## Processing Pipeline

1. Receive the stimulus.
2. Convert the stimulus to vector embeddings.
3. Convert each cluster's reference definitions to vector format and compute cosine similarity between the stimulus embedding and each cluster's references.
4. Apply manual semantic scaling (see [Manual Semantic Scaling](#manual-semantic-scaling)).
5. Apply `Pre_Activation_Boost` from existing Hebbian synaptic bonds.
6. Fire clusters that exceed their individual threshold and are not in a refractory period.
7. Record firing timestamps; start a 2-second refractory timer per fired cluster.
8. Apply Hebbian strengthening for co-activated pairs.
9. Begin cluster decay — activated clusters decay over a span of up to ~5–10 minutes.

---

## Neuron Clusters

Clusters are inspired by Appraisal Theory and the OCC Model — adapted as confined, simulatable appraisals rather than exact replicas of research models.

| Cluster | Description |
|---|---|
| `Threat` | Perceived danger or harm |
| `Novelty` | Unexpected or unfamiliar input |
| `Reward` | Gain, positive outcome |
| `Urgency` | Time pressure or immediacy |
| `Familiarity` | Recognition, known context |
| `Discomfort` | Unpleasantness, aversion |
| `Social_Relevance` | Interpersonal or social significance |
| `Affinity` | Attraction, closeness |

---

## Manual Semantic Scaling

Raw cosine similarity scores against cluster references were found to be consistently low and not practically useful. To compensate:

- A `MAX_SEMANTIC_RANGE` of `0.75` is defined as the effective ceiling of raw cosine output.
- Raw scores are artificially scaled up relative to this ceiling before being stored as the cluster's `current_signal`.

---

## Pre_Activation_Boost

Applies synaptic boost from Hebbian-learned cluster pairs **before** firing, so that related clusters receive a push based on already-computed signals.

**Algorithm:**
1. Retrieve `synaptic_weight` for each relevant cluster pair.
2. Compute: `boost = synaptic_weight * source_cluster.current_signal`
3. Accumulate into `pending_boost` using **bounded absorption**:
   ```
   pending_boost[target] += boost * (1 - pending_boost[target])
   ```
   This creates natural resistance at high values — a target already at 0.8 will not simply add 0.2; the result will be less than 1.0.
4. After all boosts are calculated, apply `pending_boost` values to all targets in one batch.

> The pending/batch pattern prevents mid-calculation contamination where a cluster acting as a source in one synaptic is already boosted when evaluated as a source in another.

---

## Fire_Activation

- Each cluster has an **individual threshold**.
- All clusters share a **fixed refractory timer of 2 seconds**.
- A cluster fires only if `current_signal > threshold` AND the refractory timer has expired.
- On firing, the timestamp is recorded and the 2-second refractory period begins.

---

## Decaying

Each fired cluster decays continuously using its individual decay rate:

```
cluster.current_signal *= (1 - cluster.decay_rate)
```

Decay continues until `current_signal` reaches 0. Stronger initial signals can persist for up to **10 minutes**, creating a **lingering effect** — subsequent stimuli are processed against a non-zero activation map that carries traces of prior events.

> This lingering effect also indirectly contributes to the emotion layer's persistence, as non-zero clusters influence emotion scoring on future stimuli. This is an emergent property of the system.

---

## Hebbian Strengthening

Based on Hebb's rule: *"Neurons that fire together, wire together."*

Synaptic bonds are **unidirectional** (`source → target`). A bond from Threat → Novelty means Threat's activation boosts Novelty's signal, but not vice versa. The reverse relationship (Novelty → Threat) is a separate, independently formed bond.

### Streak-Based Bond Formation

A minimum **co-activation streak** must be reached before a meaningful synaptic bond forms:

- The initial streak requirement is **5 consecutive co-activations**.
- Streak requirement is dynamic and grows with `synaptic_weight` of the pair.
- If the source cluster fires **without** the target during an active streak, the streak is decremented by 1.
- This prevents coincidental co-activations from forming false bonds.

### Hebbian Decay

- If a cluster pair's `last_strengthening` timestamp is more than **2 days ago** (simulated time), the synaptic bond begins to decay.
- This prevents synaptic bonds from persisting permanently for patterns that are no longer relevant.
