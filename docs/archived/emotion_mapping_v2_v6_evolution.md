# Archive: Emotion Mapping Evolution — Intermediate Approaches (v2–v4)

These are the intermediate designs explored between the v1 direct-weight mapping and the current right-shoulder membership system. Each approach was implemented or seriously considered, discovered to have a specific flaw, and replaced.

---

## v2 — Cosine Similarity on Emotion Vector Profiles

### Design
Define each emotion as an ideal vector of cluster activations using the **Component Model**. At runtime, take the activation map and compute cosine similarity between the runtime vector and each emotion's ideal vector.

**Example — ideal fear vector:**
```
fear = { threat: 0.65, novelty: 0.70, familiarity: 0.36, urgency: 0.70, discomfort: 0.55 }
```

### Problem Discovered — Sparse Vector Penalty
The runtime activation map is sparse (only fired clusters are present). The ideal emotion vector is dense (all relevant clusters defined). When computing cosine similarity between a dense ideal vector and a sparse runtime vector:

- Zero dimensions in the runtime vector contribute `0` to the dot product numerator.
- But the ideal vector's values in those same dimensions still inflate the denominator (the magnitude of the ideal vector).
- Result: even when all **present** clusters perfectly match the emotion profile, the similarity score is artificially suppressed by the missing dimensions.

This made cosine similarity an unreliable measure of emotion strength when activation maps were incomplete.

---

## v3 — Euclidean Distance with NaN for Missing Clusters

### Design
Abandon cosine similarity. Treat each emotion profile as a point in cluster-space and compute Euclidean distance between the profile point and the runtime activation map. Set missing cluster values to `NaN` and exclude them from distance computation.

### Problem Discovered
Euclidean distance measures spatial separation between two points. It does not naturally express **emotion strength** — only deviation from an ideal point. Any movement away from the exact ideal coordinates increases distance, making it difficult to translate distance values into meaningful emotion intensity scores. Small variations from the ideal produced disproportionately large distance penalties.

---

## v4 — Flat Range Scoring (Binary In-Range Check)

### Design
Instead of exact profile points, define ranges for each cluster's required activation level per emotion. A cluster is "contributing" if its activation falls within the range; otherwise it scores 0.

**Example:**
```
threat: HIGH → range (0.65 – 1.0)
```

If `threat.current_signal` is within `(0.65, 1.0)`, it contributes a score of `1`. If outside, it contributes `0`.

### Problem Discovered — The Plateau Problem
With flat binary scoring, a cluster signal of `0.60` and a cluster signal of `0.90` both fall in the same range and both return a contribution score of `1`. But `0.90` should represent a much stronger contribution to the emotion than `0.60`. The flat range created a **plateau** — the scoring system was insensitive to variation within a valid range.

---

## v5 — Triangle Membership Function

### Design
Introduce a **triangular membership function**: instead of binary in/out, define each range with three values `(minimum, ideal, maximum)`. A cluster's contribution score peaks at `ideal` and falls off linearly toward `minimum` and `maximum`.

**Example ranges:**
```
LOW:         (0.25, 0.26, 0.38)
MEDIUM:      (0.35, 0.45, 0.55)
MEDIUM_HIGH: (0.50, 0.60, 0.70)
HIGH:        (0.55, 0.65, 1)
```

### Problem Discovered — Flawed HIGH Range Behaviour
For the `HIGH` range with `ideal = 1.0`, a cluster signal of `0.9` (high but below ideal) produces diminishing returns compared to `0.65` (closer to ideal on the way up). This is the wrong behaviour — `0.9` should contribute more than `0.65` to a HIGH-required emotion. The symmetric triangle shape is inappropriate for `HIGH` ranges because there is no meaningful "too high" for a cluster that is supposed to be maximally activated.

---

## v6 — Right Shoulder with Theoretical ideal = 1.0 for HIGH

### Design
Replace the triangle for `HIGH` ranges with a **right-shoulder function**: `if value >= ideal → return 1.0`. Set `ideal = 1.0` and `maximum = 1.0` for HIGH ranges.

### Problem Discovered
With `ideal = 1.0`, any real-world HIGH activation (e.g., `0.70`, `0.65`) is always below ideal and thus always on the rising slope — producing diminishing returns even for genuinely strong signals. The gap between real observed maxima and the theoretical `1.0` ideal was too large.

---

## Resolution → Current Architecture (v7)

The `ideal` for HIGH ranges was set to the **observed maximum cluster score across 200 test stimuli** rather than the theoretical `1.0`. For the right shoulder, any value `>= ideal` returns `1.0` (maximum contribution). Values below the observed max get a proportional score.

LOW, MEDIUM, and MEDIUM_HIGH also use right-shoulder shapes with their effective tuples. This resolved both the plateau problem and the high-range diminishing return problem.

**Final range tuples:**
```
LOW:         (0.25, 0.26, 1)
MEDIUM:      (0.35, 0.45, 1)
MEDIUM_HIGH: (0.50, 0.60, 1)
HIGH:        (0.55, 0.65, 0.65)   ← ideal = observed max from 200 stimuli
```

See [ADR-004](../adr/ADR-004-emotion-profile-based-mapping.md) and the current [Emotion Layer](../current_architecture/emotion_layer.md) for the accepted implementation.
