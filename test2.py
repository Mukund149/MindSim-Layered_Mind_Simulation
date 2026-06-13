from Simulation.simulationEnigine import SimulationEngine
import time
from pprint import pprint

engine = SimulationEngine()

engine.start()

TEST_STIMULI = [
    # THREAT scenarios
    "A man is pointing a gun at me",
    "I might lose my job tomorrow",
    "Someone is following me in the dark",
    "My medical test results came back abnormal",
    
    # REWARD scenarios
    "I just got accepted into my dream university",
    "My business idea got funded today",
    "I won the competition I trained months for",
    "My crush finally said yes",
    
    # NOVELTY scenarios
    "I just discovered a completely new way to solve this",
    "Something completely unexpected just happened",
    "I have never been in this situation before",
    
    # FAMILIARITY scenarios
    "Every morning I follow the same routine",
    "This is exactly what always happens",
    "I have been through this many times before",
    
    # URGENCY scenarios
    "The deadline is in ten minutes",
    "I need to act right now or it will be too late",
    "There is no time left to prepare",
    
    # DISCOMFORT scenarios
    "I have been suffering for days",
    "This situation is unbearable",
    "I am under enormous pressure right now",
    
    # SOCIAL scenarios
    "Everyone is watching and judging me",
    "My reputation is at stake here",
    "I need to impress these people",
    
    # AFFINITY scenarios
    "My best friend needs me right now",
    "The person I love is in danger",
    "Someone I deeply care about is hurting",
    
    # MIXED scenarios
    "I failed my exam and disappointed my parents",
    "My best friend betrayed me in front of everyone",
    "I just got promoted but my colleague got fired",
    "The building is on fire and my family is inside"
]

print("\nMindSim Runtime Started")
print("Type 'exit' to stop the simulation.\n")


try:

    while True:

        stimulus = input("Stimulus > ").strip()

        if stimulus.lower() == "exit":
            break

        if not stimulus:
            continue

        print("\n--- PROCESSING STIMULUS ---\n")

        engine.process_stimulus(stimulus)

        # SMALL DELAY
        # lets background thread evolve a little
        time.sleep(1)

        emotional_state = engine.mind_state.emotional_state

        print("\n========== CURRENT STATE ==========\n")

        print(f"Dominant Emotion : {emotional_state['dominant']}\n")

        print("Base Emotions:\n")

        for emotion, data in emotional_state["base"].items():

            print(
                f"{emotion:<15}"
                f"value={data['value']:.2f}   "
                f"label={data['label']:<15}   "
                f"strength={data['strength']:.2f}"
            )
        
        print("\nTarget Emotions:\n")

        for target_emotion, target in engine.emotion_layer.emotion_tanks.items():
            print(f"{target_emotion} : {target}")

        print("\nCompounds:\n")

        if emotional_state["compounds"]:

            for compound, value in emotional_state["compounds"].items():

                print(
                    f"{compound:<15}"
                    f"value={value:.2f}"
                )

        else:
            print("None")

        print("\nTrends:\n")

        for emotion, trend in emotional_state["trends"].items():

            print(
                f"{emotion:<15}{trend}"
            )

        print("\nActivation Map:\n")

        for emotion, data in engine.mind_state.activation_map.items():
            print(f"{emotion} : {data} : {engine.neuron_layer.clusters[emotion].last_fired}")
        
        print("\n Full Activation Map")

        for emotion, weight in engine.neuron_layer.Full_activation_map.items():
            print(f"{emotion} : {weight}")
        
        print("\nHebbian Synaptics")

        for pair, data in engine.neuron_layer.synaptic_weights.items():
            strength = data.weight
            if strength > 0:
                print(f"{pair} : {strength}")

        print("\n===================================\n")

except KeyboardInterrupt:

    print("\nSimulation Interrupted")

finally:

    engine.stop()

    print("\nMindSim Runtime Stopped")