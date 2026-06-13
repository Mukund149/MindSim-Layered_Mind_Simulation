# ADR-002: Per-Cluster Decay Rates for Neuron Activation

**Status:** Accepted

---

## Context

The neuron decay system is responsible for the lingering effect — activated clusters fade gradually rather than resetting immediately. The initial implementation used a **uniform decay rate of ~0.05** applied to all clusters equally.

With `decay_rate = 0.05`, the decay formula `cluster.current_signal *= (1 - 0.05)` emptied the entire activation map in under **2 seconds**. By the time any subsequent stimulus arrived, all prior context was gone. The lingering effect existed in theory but had no measurable impact at runtime.

---

## Decision

Replace the uniform decay rate with **individual decay rates per cluster**. Each cluster is assigned its own `decay_rate` reflecting how quickly that type of appraisal signal should fade.

The decay formula remains:
```
cluster.current_signal *= (1 - cluster.decay_rate)
```

With per-cluster rates, stronger or more persistent signals can last **up to 10 minutes**, while others decay more quickly.

---

## Alternatives Considered

- **Keep uniform rate, lower the value:** Setting a much lower uniform rate (e.g., 0.001) would extend decay globally but cannot model the biological reality that different appraisal types have different persistence (e.g., threat signals are known to persist longer than novelty signals).
- **Reset on stimulus:** Clearing the activation map on each new stimulus was rejected because it eliminates inter-stimulus context entirely, which is a core feature of the system.

---

## Consequences

**Benefits:**
- Genuine lingering effect: prior emotional context carries forward across stimuli.
- Different cluster types can be tuned to reflect their real-world persistence characteristics.
- Emergent interaction: decaying clusters contribute to emotion scoring on future stimuli without explicit inter-stimulus memory — the activation map itself acts as short-term contextual memory.

**Tradeoffs / Known Issues:**
- Because MindSim is exposed to extreme and varied stimuli (not a living creature in a normal environment), long-running cluster signals can create what appears to be false activation for later, unrelated stimuli.
- The system's emergent continuous-state behaviour makes output expectations less predictable — direct stimulus-to-output relationships are obscured by the ongoing state.
- This is acknowledged as an inherent property of emergent continuous-state simulation: the expectation of clean direct output is incompatible with the design goal.
