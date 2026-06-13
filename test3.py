from Simulation.simulationEnigine import SimulationEngine
from collections import defaultdict
from statistics import mean
import json

TEST_STIMULI = [
    "My manager wants to talk to me tomorrow",
    "I think I made a mistake at work",
    "Someone looked angry when they saw me",
    "I might miss an important deadline",
    "I forgot where I parked my car",
    "I think I offended someone",
    "A storm is approaching my town",
    "I received an unexpected legal notice",
    "Someone is following me in the dark",
    "I think I am being watched",
    "I might lose my job tomorrow",
    "My medical test results came back abnormal",
    "A dog is growling at me",
    "My bank account was suddenly locked",
    "I heard footsteps behind me at night",
    "A man is pointing a gun at me",
    "Someone is breaking into my house",
    "I am trapped in a burning building",
    "A terrorist attack is happening nearby",
    "A nuclear missile is heading toward my city",
    "I got a compliment today",
    "My work was appreciated",
    "I solved a difficult problem",
    "I passed an exam",
    "I received a small bonus",
    "I made a new friend",
    "I won a local competition",
    "I got accepted into a university",
    "My business idea got funded",
    "My crush said yes",
    "I got my dream job",
    "My startup became profitable",
    "I won a national award",
    "I inherited a large amount of money",
    "I became financially independent",
    "I became a millionaire overnight",
    "I won the lottery",
    "I became the richest person alive",
    "I discovered a cure for cancer",
    "I become ruler of the world",
    "I tried a new restaurant",
    "I visited a new city",
    "I learned a new skill",
    "I met someone unusual",
    "I saw a strange animal",
    "I encountered a completely different culture",
    "I experienced a new technology",
    "I solved a problem in a new way",
    "I discovered a new method",
    "I have never been in this situation before",
    "Something completely unexpected happened",
    "The laws of my industry changed overnight",
    "A new species was discovered",
    "Time appeared to slow down",
    "A portal opened in front of me",
    "An alien civilization lands on Earth",
    "Gravity suddenly stopped working",
    "Humans made first contact with extraterrestrials",
    "Reality appears to be changing",
    "The laws of physics suddenly stopped working",
    "I have seen this before",
    "This reminds me of something",
    "I know how this usually goes",
    "This feels familiar",
    "I have done this many times",
    "This is part of my routine",
    "I have repeated this task for years",
    "Every morning I follow the same routine",
    "This is exactly what always happens",
    "I know this process perfectly",
    "I could do this with my eyes closed",
    "I have encountered this hundreds of times",
    "This environment feels like home",
    "I know every detail of this place",
    "This is my area of expertise",
    "I have spent decades doing this",
    "I know this situation better than anyone",
    "I have lived through this exact scenario repeatedly",
    "Nothing about this surprises me",
    "This feels completely predictable",
    "I should answer this soon",
    "I need to make a decision today",
    "I should finish this by tonight",
    "Time is running short",
    "The deadline is approaching",
    "I need to act quickly",
    "The deadline is in one hour",
    "I have only thirty minutes left",
    "The deadline is in ten minutes",
    "There is no time left to prepare",
    "I need to act right now",
    "The train is leaving",
    "I must move immediately",
    "Seconds matter now",
    "The building is collapsing",
    "The bridge is breaking",
    "Jump now or you will die",
    "The bomb will explode in seconds",
    "The plane is crashing",
    "Act now or everyone dies",
    "I feel a little tired",
    "I have a headache",
    "I feel stressed",
    "I am uncomfortable",
    "This situation is frustrating",
    "I am feeling anxious",
    "I am under pressure",
    "I feel emotionally drained",
    "I have been suffering for days",
    "This situation is unbearable",
    "I am under enormous pressure",
    "I cannot take much more of this",
    "I am experiencing severe pain",
    "Everything hurts",
    "I am completely exhausted",
    "Every second feels awful",
    "The pain is overwhelming",
    "I am experiencing agony",
    "The suffering is unbearable",
    "Every moment is torture",
    "A few people are listening",
    "My friends are watching",
    "People care about this decision",
    "My coworkers are paying attention",
    "My family is interested in the outcome",
    "Others are depending on me",
    "People are judging my work",
    "My reputation matters here",
    "Everyone is watching and judging me",
    "My reputation is at stake",
    "A large audience is waiting",
    "Thousands of people are following this",
    "Millions are watching",
    "The media is covering my actions",
    "My decision will affect many people",
    "The nation is watching",
    "The world is paying attention",
    "A billion people await my answer",
    "History will remember this choice",
    "The entire world is watching my next move",
    "An acquaintance asked for help",
    "A friend needs advice",
    "Someone I know is struggling",
    "A close friend is upset",
    "Someone I care about is sad",
    "My friend needs me",
    "My sibling is in trouble",
    "My best friend needs me right now",
    "Someone I deeply care about is hurting",
    "The person I love is upset",
    "My partner is in danger",
    "My child is crying",
    "A loved one is seriously ill",
    "My family needs my support",
    "The person I love is in danger",
    "My child is trapped in a burning building",
    "My entire family is threatened",
    "The most important person in my life is dying",
    "I may lose someone I love forever",
    "Everyone I care about is in danger",
    "My boss asked to meet privately",
    "I received a message saying call me",
    "An old friend contacted me unexpectedly",
    "I am moving to a new city next month",
    "I start a new job tomorrow",
    "Someone mentioned my name in a meeting",
    "I found a wallet on the street",
    "A stranger smiled at me",
    "My flight was suddenly cancelled",
    "My phone rang at 3 AM",
    "I got promoted but my colleague was fired",
    "My best friend betrayed me",
    "I passed but barely",
    "I won but hurt someone in the process",
    "My team succeeded without me",
    "I failed but learned something valuable",
    "I got rejected from one company and accepted by another",
    "Someone apologized after years",
    "I discovered a family secret",
    "A relationship ended peacefully",
    "I inherited money unexpectedly",
    "A competitor praised my work",
    "A friend became more successful than me",
    "I am leaving my hometown forever",
    "I received unexpected praise",
    "I received unexpected criticism",
    "I accidentally embarrassed myself publicly",
    "I have to choose between two good options",
    "I have to choose between two bad options",
    "My project succeeded but cost me my health",
    "The building is on fire and my family is inside",
    "I saved someone but got injured",
    "I lost my wallet but found an old photograph",
    "My exam results arrive tomorrow",
    "The doctor wants to discuss my results",
    "Someone knocked on my door at midnight",
    "A major opportunity just appeared",
    "My best friend moved away",
    "I am becoming a parent",
    "Tomorrow will change my life forever"
]

CLUSTERS = [
    "threat",
    "reward",
    "novelty",
    "familiarity",
    "urgency",
    "social_relevance",
    "discomfort",
    "affinity"
]

results = []
cluster_stats = defaultdict(list)

print("\n=== MINDSIM CALIBRATION RUN ===\n")

for stimulus in TEST_STIMULI:

    # completely fresh runtime
    engine = SimulationEngine()
    engine.start()

    try:

        engine.neuron_layer.process_stimulus(stimulus)
        engine.neuron_layer.fireActivations()

        full_map = dict(engine.neuron_layer.activation_map)

        results.append({
            "stimulus": stimulus,
            **full_map
        })

        print(f"\n{stimulus}")

        for cluster, weights in full_map.items():

            value = full_map.get(cluster, 0.0)

            cluster_stats[cluster].append(value)

            print(
                f"{cluster:<20}"
                f"{value:.3f}"
            )

    finally:

        engine.stop()

print("\n\n=== CLUSTER STATISTICS ===\n")

for cluster in CLUSTERS:

    values = cluster_stats[cluster]

    values_sorted = sorted(values)

    percentile_95_index = int(len(values_sorted) * 0.95)
    percentile_95_index = min(
        percentile_95_index,
        len(values_sorted) - 1
    )

    p95 = values_sorted[percentile_95_index]

    print(f"\n{cluster.upper()}")

    print(f"min   : {min(values):.3f}")
    print(f"mean  : {mean(values):.3f}")
    print(f"max   : {max(values):.3f}")
    print(f"95%   : {p95:.3f}")

print("\n\n=== RAW RESULTS JSON ===\n")

with open("mindsim_calibration_results6.json", "w") as file:
    json.dump(
        results,
        file,
        indent=4
    )

print(
    "Saved -> mindsim_calibration_results.json"
)