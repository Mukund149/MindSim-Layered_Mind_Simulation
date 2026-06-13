# Emotion Layer

## Responsibility

The emotion layer receives the `activation_map` from MindState and produces a dynamic emotional state. It generates 8 base emotions using cluster profiles, applies regulation, tracks trends, moves emotions gradually via inertia, checks intensity, compounds base emotions into complex emotions, and identifies the dominant emotion.

---

## Processing Pipeline

1. Receive `activation_map` from MindState.
2. Run `Process_Emotions` — score each base emotion against its cluster profile.
3. Store scores into `target_emotion_tank`.
4. Run `Regulate_Emotions` — apply suppressors and releasers.
5. Run `Trend_Check` — determine direction of emotional change.
6. Run `Update_Inertia` — move current emotion state gradually toward target values.
7. Run `Intensity_Check` — relabel base emotions based on strength.
8. Run `Compound_Emotion` — form complex emotions from base emotion pairs.
9. Determine `Dominant_Emotion`.

---

## Base Emotions

Based on **Plutchik's Wheel of Emotions**:

| Emotion | Low Intensity | Ideal | High Intensity |
|---|---|---|---|
| Fear | Apprehension | Fear | Terror |
| Anger | Annoyance | Anger | Rage |
| Joy | Serenity | Joy | Ecstasy |
| Sadness | Pensiveness | Sadness | Grief |
| Trust | Acceptance | Trust | Admiration |
| Disgust | Boredom | Disgust | Loathing |
| Anticipation | Interest | Anticipation | Vigilance |
| Surprise | Distraction | Surprise | Amazement |

---

## Emotion Profiles (Current — Range + Membership Based)

Each base emotion is defined by a cluster profile. Each cluster in the profile specifies a **required activation range** using a tuple of `(minimum, ideal, maximum)`.

**Example — Fear profile:**
```
fear = {
  threat:      HIGH         → (0.55, 0.65, 0.65)
  novelty:     HIGH         → (0.55, 0.65, 0.65)
  familiarity: LOW          → (0.25, 0.26, 1)
  urgency:     HIGH         → (0.55, 0.65, 0.65)
  discomfort:  MEDIUM_HIGH  → (0.50, 0.60, 1)
}
```

**Standard range tuples:**
```
LOW:         (0.25, 0.26, 1)
MEDIUM:      (0.35, 0.45, 1)
MEDIUM_HIGH: (0.50, 0.60, 1)
HIGH:        (0.55, 0.65, 0.65)
```

> Note: `LOW`, `MEDIUM`, `MEDIUM_HIGH` use a **right-shoulder** shape (anything ≥ ideal returns 1.0, using observed max as the ideal ceiling). `HIGH` also uses a right-shoulder but with `ideal = observed_max_across_200_stimuli` rather than a theoretical 1.0.

---

## Process_Emotions

1. Take `activation_map` from MindState.
2. For each base emotion, iterate through its cluster profile.
3. For each cluster **present** in the activation map: compute membership score.
4. For each cluster from the profile **absent** in the activation map: compute penalty.
5. Final emotion score:
   ```
   score = (sum of present cluster scores / count of present clusters) - total_penalties
   ```
6. Store computed scores into `target_emotion_tank`.

---

## Membership Function

Determines how much a cluster's current signal contributes to a specific emotion range.

**Out of range:**
```
if value < minimum OR value > maximum → return 0
```
(No contribution. Contradictory penalty for inverse-range cases is planned but not yet implemented.)

**Right shoulder** (used for LOW, MEDIUM, MEDIUM_HIGH ranges and HIGH):
```
if value >= ideal  → return 1.0
if value < ideal   → return (value - minimum) / (ideal - minimum)
```

**Normal triangle** (used for ranges that have a true peak, not a shoulder):
```
if value == ideal  → return 1.0
if value < ideal   → return (value - minimum) / (ideal - minimum)
if value > ideal   → return (maximum - value) / (maximum - ideal)
```

---

## Target Emotion Tank

The `target_emotion_tank` stores the reflexive emotional response to a stimulus — the **target** the emotional state is moving toward. The actual current emotion state does not jump immediately to this target; it moves toward it under inertia.

---

## Regulate_Emotions

Each base emotion has suppressor and releaser emotions defined in the emotion mapping.

**Example — Anger:**
- Suppressed by: `Trust`
- Released by: `Anticipation`

**Formulas:**
```
suppress_value = target_emotion_tanks[suppress_emotion] * SUPPRESSION_STRENGTH
release_value  = RELEASE_STRENGTH * (1 - target_emotion_tanks[release_emotion])
```

Regulation values are collected first, then applied in a single batch — same pending pattern as `Pre_Activation_Boost` — to avoid order-of-evaluation contamination.

---

## Trend_Check

Compares newly generated emotion values in `target_emotion_tank` against existing values to compute the **direction** of the emotion vector (rising, falling, stable).

> Future plan: track actual flow of emotion through inertia values rather than comparing raw tank values directly.

---

## Update_Inertia

Solves the continuous-state problem of sudden emotional jumps. Instead of snapping to `target_emotion_tank`, each emotion moves gradually toward its target under its individual **inertia rate**.

This creates the **lingering emotional effect** — an emotion that was strongly activated continues to persist and fade gradually rather than disappearing instantly.

> Current known issue: inertia rates are set too high, causing emotions to converge too quickly. Tuning is deferred because neuron decay already contributes lingering via the activation map — the two mechanisms produce an emergent combined effect. Whether explicit inertia tuning is necessary remains an open question.

---

## Intensity_Check

Once an emotion reaches its target value, its strength determines which intensity label is applied (e.g., low anger = Annoyance, ideal anger = Anger, high anger = Rage).

---

## Compound_Emotion

Complex emotions emerge from combinations of base emotions when both parent emotions exceed a defined threshold simultaneously.

**Example:**
```
Joy + Trust → Love
```

---

## Dominant_Emotion

After compounding, the dominant emotion — the single strongest active emotional signal — is identified and recorded in MindState.
