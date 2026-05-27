from Brain.Neuron_Layer import *
from Brain.Emotion_layer import *

from Simulation.mind_state import MindState
from Simulation.TimeSimulations import Mind_clock

import time


mind_state = MindState()

neuron_layer = NeuronLayer()

emotion_layer = EmotionLayer(
    mind_state
)

mind_time = Mind_clock()


while True:
    
    stimulus = input("Enter the stimulus : ")
    if stimulus == "exit":
        break
    if stimulus == "time":
         print(mind_time.now())


    # --------------------------------
    # STIMULUS PROCESSING
    # --------------------------------

    mind_state.current_stimulus = stimulus

    stimulus_vector = (
        neuron_layer.process_stimulus(
            stimulus
        )
    )

    activation_map = (
        neuron_layer.fireActivations()
    )


    mind_state.activation_map = (
        activation_map
    )

    mind_state.stimulus_vector = (
        stimulus_vector
    )

    neuron_layer.hebbian_strengthening()
    neuron_layer.hebbian_decay()


    # --------------------------------
    # GENERATE EMOTIONAL TARGETS
    # --------------------------------

    emotion_layer.process_targets()


    print("\nTARGET EMOTIONS")
    for emotion, values in emotion_layer.emotion_tanks.items():
        print(f"{emotion} : {values}\n")

    print("\nTRENDS")
    for emotion, trend in mind_state.emotional_state["trends"].items():
        print(
            f"{emotion}: {trend}"
        )


    # --------------------------------
    # INTERNAL EMOTIONAL EVOLUTION
    # --------------------------------

    neuron_layer.decay()
    for tick in range(10):
        emotion_layer.emotional_tick()

    print("\nBASE EMOTIONS")

    for emotion, data in (
            mind_state
            .emotional_state[
                "base"
            ]
            .items()
        ):

        print(
                f"{emotion}: "
                f"{round(data['value'],3)} "
                f"| "
                f"{data['label']}: "
                f"{data['strength']}"
            )


    print("\nCOMPOUNDS")

    for compound, strength in mind_state.emotional_state["compounds"].items():
            print(
                f"{compound} : {strength}"
            )
        
    print("\nDOMINANT")

    print(
            mind_state.emotional_state["dominant"]
        )
    for pair, synaptic in neuron_layer.synaptic_weights.items():
        print(
        f"{pair} : {round(synaptic.weight, 3)}"
        )
    time.sleep(1)

