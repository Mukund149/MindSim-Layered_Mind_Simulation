from Simulation.simulationEnigine import SimulationEngine
import time
from pprint import pprint

engine = SimulationEngine()

engine.start()

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

        print("\n===================================\n")

except KeyboardInterrupt:

    print("\nSimulation Interrupted")

finally:

    engine.stop()

    print("\nMindSim Runtime Stopped")