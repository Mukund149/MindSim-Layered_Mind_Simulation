# Scheduled Update: Contradictory Penalties in Membership Function

**Status:** `Planned` — acknowledged, not yet designed

---

## Current Situation

The current `Membership` function returns `0` for any cluster value that falls outside the defined range `(minimum, maximum)` for a given emotion profile entry. This means a cluster that is completely out of range contributes nothing — but receives no penalty either.

**The gap:** If an emotion profile requires `familiarity: LOW` but the activation map shows `familiarity: HIGH`, the current system treats this as "not contributing" (score = 0). However, a high familiarity signal is not merely absent evidence for fear — it is actively contradictory evidence. The system should penalise this case differently from a cluster simply not being present.

**Example:**
```
Fear requires: familiarity → LOW
Activation map: familiarity = 0.85 (HIGH range)

Current behaviour: familiarity score = 0 (out of range, no contribution, no penalty)
Expected behaviour: familiarity = 0.85 HIGH should actively penalise fear score
```

---

## Planned Change

Introduce **contradictory penalties**: when a cluster's activation is not only out of range but is in the **inverse** of the required range, apply an explicit penalty to the emotion score.

The mechanism for detecting contradiction would be: if the required range is LOW and the actual value is HIGH (or vice versa), flag as contradictory and apply a configurable `CONTRADICTORY_PENALTY` weight.

---

## Reason for Change

The absence of a penalty in inverse cases allows the system to generate emotions even when the activation pattern contains strong signals that are semantically opposed to that emotion. This reduces the accuracy and realism of emotion generation.

---

## Current Status

**Planned.** No implementation design has been finalised. The question of whether to charge contradictory penalties is marked as unresolved in the source document. The soft emotion mapping redesign (see `soft_emotion_mapping_redesign.md`) may supersede this if ranges are removed entirely — in that case, contradictory clusters would naturally be captured as `negatives` in the new model.
