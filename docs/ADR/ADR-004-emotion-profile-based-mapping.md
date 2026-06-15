# ADR-004: Range-Based Emotion Profiles with Right-Shoulder Membership Functions

**Status:** Superseded by ADR-008

---

## Context

The emotion layer required a mechanism to transform neuron activations into base emotion signals while remaining sensitive to co-activated clusters and their intensities.

Multiple approaches were explored and are documented in:

`archive/emotion_mapping_v2_v6_evolution.md`

At the time, the main challenges were:

- Plateau effects from binary scoring
- Sparse activation maps
- Diminishing returns in HIGH ranges
- Missing cluster handling

---

## Decision

Adopt **range-based emotion profiles** using membership functions.
Each emotion was defined using predefined activation ranges (`LOW`, `MEDIUM`, `MEDIUM_HIGH`, `HIGH`) for each required cluster.
Right-shoulder membership functions were introduced to avoid diminishing returns for high activations.
Missing clusters contributed penalties rather than zero scores.
This architecture became the foundation of Emotion Layer V2.

---

## Consequences

### Benefits

- Sensitive to combinations of activated clusters.
- Smooth membership transitions.
- Reduced binary scoring behavior.
- Explicit handling of missing clusters.

### Limitations

The architecture introduced hard boundaries.
Near-miss activations produced the same output as complete absences.

Example:

```text
threat = 0.44

minimum = 0.45

↓

0 contribution
```

This conflicted with the continuous-state philosophy of MindSim and became increasingly incompatible with neuron lingering and accumulation.
Additionally, maintenance effort shifted toward calibrating ranges rather than improving psychological realism.

Common issues included:

- HIGH range calibration
- Membership function adjustments
- Missing cluster penalties
- Contradictory penalties

These limitations ultimately motivated the transition to ADR-008.

---

## Superseded By

See:

`ADR-008: Evidence Accumulation Emotion Mapping`
