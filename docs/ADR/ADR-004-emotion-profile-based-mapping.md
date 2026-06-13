# ADR-004: Range-Based Emotion Profiles with Right-Shoulder Membership Functions

**Status:** Accepted

---

## Context

Emotion generation went through six design iterations (see [archive/emotion_mapping_v2_v6_evolution.md](../archive/emotion_mapping_v2_v6_evolution.md) for full history). The core problem was: given an activation map of cluster signals, how do you compute the strength of each of the 8 base emotions in a way that is sensitive to the pattern of co-activated clusters and their activation levels?

The approaches tried in sequence were:
1. Direct cluster weight mapping → could not distinguish emotion context (e.g., threat-for-fear vs. threat-for-anger)
2. Cosine similarity on dense ideal vectors → sparse runtime vectors artificially suppressed scores
3. Euclidean distance with NaN for missing clusters → distance metric doesn't naturally express intensity
4. Flat range scoring (binary in/out) → plateau problem: 0.60 and 0.90 both score 1 within the same range
5. Triangle membership function → diminishing returns for values above ideal in HIGH ranges (0.9 scores worse than 0.65)
6. Right shoulder with theoretical `ideal = 1.0` → gap between theoretical and observed maxima still produced diminishing returns for real HIGH outputs

---

## Decision

Use **range-based cluster profiles** with a **right-shoulder membership function** where the `ideal` for the HIGH range is set to the **observed maximum cluster score across 200 test stimuli**, not the theoretical maximum of 1.0.

**Membership function:**

*Out of range:*
```
if value < minimum OR value > maximum → return 0
```

*Right shoulder (used for LOW, MEDIUM, MEDIUM_HIGH, and HIGH ranges):*
```
if value >= ideal   → return 1.0
if value < ideal    → return (value - minimum) / (ideal - minimum)
```

*Normal triangle (for ranges with a true peak, not a shoulder):*
```
if value == ideal   → return 1.0
if value < ideal    → return (value - minimum) / (ideal - minimum)
if value > ideal    → return (maximum - value) / (maximum - ideal)
```

**Final range tuples (examples):**
```
LOW:         (min=0.25, ideal=0.26, max=1)
MEDIUM:      (min=0.35, ideal=0.45, max=1)
MEDIUM_HIGH: (min=0.50, ideal=0.60, max=1)
HIGH:        (min=0.55, ideal=0.65, max=0.65)   ← ideal = observed max from 200 stimuli
```

**Emotion score formula:**
```
score = (sum of present cluster membership scores / count of present clusters) - total_penalties
```

Missing clusters (required by the profile but absent from the activation map) contribute penalties rather than zero scores.

---

## Alternatives Considered

See archived evolution document for full details on each rejected approach: cosine similarity, euclidean distance, flat range, symmetric triangle, right shoulder with ideal=1.

---

## Consequences

**Benefits:**
- Sensitive to the pattern and combination of activated clusters, not just individual magnitudes.
- Membership function is smooth — values near the ideal contribute more than values at the boundary.
- Avoids the plateau problem (no flat binary scoring within a range).
- Avoids the HIGH range diminishing returns problem (right shoulder with calibrated ideal).
- Missing cluster handling is explicit via penalties.

**Tradeoffs / Known Limitations:**
- Profiles still define hard range boundaries. A cluster signal at `0.44` when the range minimum is `0.45` contributes zero — a near-miss produces the same result as a complete absence.
- This hardness is the primary motivation for the [Soft Emotion Mapping Redesign](../scheduled_updates/soft_emotion_mapping_redesign.md) currently under investigation.
- Contradictory cluster activations (inverse of required range) are not currently penalised — they are treated the same as out-of-range (zero contribution). See [Contradictory Penalties](../scheduled_updates/contradictory_penalties.md).
- The `ideal` for HIGH is calibrated to 200 test stimuli. If the stimulus distribution shifts significantly, recalibration may be required.
