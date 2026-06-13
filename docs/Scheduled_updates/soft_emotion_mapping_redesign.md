# Scheduled Update: Soft Emotion Mapping Redesign

**Status:** `Investigating` — core approach defined, implementation problem unsolved

---

## Current Situation

The current emotion mapping uses range-based cluster profiles with a membership function. Each emotion defines required activation ranges per cluster (e.g., fear requires `threat: HIGH`, `novelty: HIGH`, `familiarity: LOW`).

**The problem:** Hard range boundaries mean a stimulus that activates `threat: 0.45`, `novelty: 0.39`, `urgency: 0.40`, `discomfort: 0.35` — all slightly below the defined HIGH and MEDIUM_HIGH ranges — produces `fear = 0`. But intuitively, a small amount of fear should emerge from this activation pattern. The hard range system breaks the emergent, continuous-state nature of MindSim.

Additionally, hard ranges do not align well with the neuron layer's lingering behaviour — clusters decay gradually, so their activation often sits between named ranges rather than cleanly within them.

---

## Planned Change

Replace range-based profiles with **soft positive/negative cluster mappings**:

```
fear = {
  positives: { threat, novelty, urgency, discomfort },
  negatives: { familiarity }
}
```

**Base formula:**
```
fear = avg(positives) * ( 1 - avg(negatives) )
```

This approach:
- Removes hard boundaries — any positive cluster activation contributes to the emotion proportionally.
- Negatives act as contradictory suppressors (replacing the current out-of-range penalty system).
- Missing penalties for absent positive clusters can also be introduced for realism.
- Makes the emotion layer fully dependent on the weighted activation values coming from the neuron layer.

---

## Reason for Change

- Hard ranges produce binary zero-output for near-miss activations.
- Does not reflect the continuous, gradual nature of the underlying neuron signals.
- Breaks the emergent design principle of MindSim.
- The positive/negative design is simpler, more flexible, and naturally handles continuous activation values.

---

## Open Problem — Required Clusters

Certain emotions are semantically dependent on specific clusters. Fear without `threat` is not really fear. But with the soft positive/negative formula, the remaining positive clusters (`novelty`, `urgency`, `discomfort`) could average to a strong fear score even when `threat` is absent.

**Proposed solutions under consideration:**

### Option A — Required cluster multiplier
```
fear = {
  required: [threat],
  positives: { novelty, urgency, discomfort },
  negatives: { familiarity }
}

if required cluster is missing:
  fear *= 0.25   (soft enforcement)
  OR
  fear = 0       (hard enforcement)
```

### Option B — Required-weighted formula
```
fear = required_cluster_value * avg(positives excluding required) * (1 - avg(negatives))
```

**Problem with Option B:** Over-dependence on the required cluster. If `threat` is low, fear is suppressed regardless of the other positive clusters — making the required cluster a bottleneck that dominates the entire score.

---

## Current Status

**Problem remains unsolved.** The soft mapping direction is agreed upon. The handling of required clusters is the open blocker. No implementation has been chosen.

**Open questions:**
- Should required clusters enforce hard zero or soft reduction?
- Should the required cluster's value be a multiplicative factor or an additive prerequisite?
- How do contradictory penalties interact with the positive/negative model?
