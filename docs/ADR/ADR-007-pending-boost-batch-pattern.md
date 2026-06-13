# ADR-007: Pending Boost Batch Application Pattern

**Status:** Accepted

---

## Context

Two systems in MindSim compute boost/modifier values that must be applied to a set of targets: `Pre_Activation_Boost` (Hebbian synaptic boost applied to cluster signals) and `Regulate_Emotions` (suppression/release values applied to emotion tank values).

In both cases, the targets being modified are also potential sources used to compute boosts for other targets in the same calculation pass. For example:

- In `Pre_Activation_Boost`: Cluster A may be the source boosting Cluster B, while Cluster B is simultaneously the source boosting Cluster C. If A's boost is applied to B immediately, then when B's boost to C is calculated, it uses B's already-boosted value — not B's original value.
- In `Regulate_Emotions`: Suppression and release values for multiple emotions are all calculated from the same `target_emotion_tank` state. Applying them one at a time would cause earlier applications to influence later calculations within the same pass.

---

## Decision

In both `Pre_Activation_Boost` and `Regulate_Emotions`, all boost/modifier values are:
1. **Calculated first** and accumulated into a temporary pending store.
2. **Applied in a single batch** after all calculations are complete.

For `Pre_Activation_Boost`, accumulation uses bounded absorption:
```
pending_boost[target] += boost * (1 - pending_boost[target])
```

---

## Alternatives Considered

- **Apply immediately (sequential):** Rejected — causes order-of-evaluation contamination. The calculated boost depends on whether a source has already been boosted in the same pass, producing results that vary based on arbitrary processing order.
- **Copy-on-write (snapshot sources before modifying):** Functionally equivalent to the pending/batch pattern but more memory-intensive. The pending accumulator achieves the same isolation more efficiently.

---

## Consequences

**Benefits:**
- All boost calculations within a single pass are based on the same consistent pre-boost state.
- Processing order of clusters/emotions does not affect results.
- The bounded absorption formula for `Pre_Activation_Boost` additionally prevents runaway accumulation at high signal values.

**Tradeoffs:**
- Requires a temporary accumulation data structure in both systems.
- The bounded absorption formula for `Pre_Activation_Boost` means the relationship between raw boost values and final applied boosts is non-linear at high values — this is intentional but must be understood when tuning synaptic weights.
