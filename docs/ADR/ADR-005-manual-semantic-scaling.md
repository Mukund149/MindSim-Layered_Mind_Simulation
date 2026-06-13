# ADR-005: Manual Semantic Score Scaling (MAX_SEMANTIC_RANGE)

**Status:** Accepted

---

## Context

The neuron layer uses cosine similarity between the stimulus embedding and each cluster's reference embeddings to determine how strongly the stimulus activates each cluster. Raw cosine similarity scores were consistently low — not matching expected signal strengths — making direct use of raw scores impractical for downstream emotion processing.

---

## Decision

Introduce a manual calibration constant `MAX_SEMANTIC_RANGE = 0.75`. Raw cosine similarity scores are artificially scaled up relative to this ceiling before being stored as the cluster's `current_signal`.

The effective scaling maps raw scores from `[0, MAX_SEMANTIC_RANGE]` to `[0, 1.0]`, ensuring the full signal range is utilised.

---

## Alternatives Considered

- **Use raw cosine scores directly:** Rejected — scores were too compressed in a low range to drive meaningful downstream differentiation between clusters.
- **Retrain/reconfigure embeddings to produce higher similarity scores:** Not mentioned as a considered option; manual calibration was the chosen pragmatic solution.
- **Normalise per-stimulus (relative scaling):** Not mentioned; absolute scaling against a fixed ceiling was chosen.

---

## Consequences

**Benefits:**
- Cluster signals occupy the full `[0, 1]` range, making thresholds and emotion profile ranges practical to define.
- Simple, transparent, and easily adjustable constant.

**Tradeoffs:**
- `MAX_SEMANTIC_RANGE = 0.75` is empirically set and may need recalibration if embeddings, cluster references, or similarity computation changes.
- The scaling is applied uniformly — it does not account for potential variation in raw score distributions across different cluster types.
- Any future change to the embedding model or reference definitions should re-evaluate whether `0.75` remains the appropriate ceiling.
