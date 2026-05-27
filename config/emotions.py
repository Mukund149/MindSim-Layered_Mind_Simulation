NEURON_EMOTION_MAPPING = {
    "threat": {
        "fear": 0.55,
        "anger": 0.20,
        "disgust": 0.15,
        "surprise": 0.10
    },
    "reward": {
        "joy": 0.50,
        "anticipation": 0.25,
        "trust": 0.15,
        "surprise": 0.10
    },
    "urgency": {
        "anticipation": 0.45,
        "fear": 0.35,
        "surprise": 0.20
    },
    "novelty": {
        "surprise": 0.50,
        "anticipation": 0.30,
        "fear": 0.20
    },
    "familiarity": {
        "trust": 0.70,
        "joy": 0.30
    },
    "social_relevance": {
        "trust": 0.35,
        "anticipation": 0.25,
        "fear": 0.25,
        "joy": 0.15
    },
    "affinity": {
        "trust": 0.40,
        "joy": 0.30,
        "fear": 0.15,
        "anticipation": 0.15
    },
    "discomfort": {
        "sadness": 0.35,
        "disgust": 0.30,
        "anger": 0.20,
        "fear": 0.15
    }
}

REGULATIONS = {
    "fear":         { "suppress": "anger",        "release": "trust"       },
    "anger":        { "suppress": "trust",        "release": "anticipation"},
    "joy":          { "suppress": "sadness",      "release": "trust"       },
    "sadness":      { "suppress": "joy",          "release": "trust"       },
    "trust":        { "suppress": "disgust",      "release": "joy"         },
    "disgust":      { "suppress": "trust",        "release": "anger"       },
    "anticipation": { "suppress": "surprise",     "release": "joy"         },
    "surprise":     { "suppress": "anticipation", "release": "fear"        },
} 

EMOTION_INTENSITY_ZONES = {
    "fear": [
        (0.00, 0.40, "apprehension"),
        (0.40, 0.75, "fear"),
        (0.75, 1.01, "terror")
    ],

    "anger": [
        (0.00, 0.40, "annoyance"),
        (0.40, 0.75, "anger"),
        (0.75, 1.01, "rage")
    ],

    "joy": [
        (0.00, 0.40, "serenity"),
        (0.40, 0.75, "joy"),
        (0.75, 1.01, "ecstasy")
    ],

    "sadness": [
        (0.00, 0.40, "melancholy"),
        (0.40, 0.75, "sadness"),
        (0.75, 1.01, "grief")
    ],

    "trust": [
        (0.00, 0.40, "comfort"),
        (0.40, 0.75, "trust"),
        (0.75, 1.01, "admiration")
    ],

    "disgust": [
        (0.00, 0.40, "aversion"),
        (0.40, 0.75, "disgust"),
        (0.75, 1.01, "loathing")
    ],

    "anticipation": [
        (0.00, 0.40, "interest"),
        (0.40, 0.75, "anticipation"),
        (0.75, 1.01, "vigilance")
    ],

    "surprise": [
        (0.00, 0.40, "alertness"),
        (0.40, 0.75, "surprise"),
        (0.75, 1.01, "amazement")
    ]
}

COMPOUNDING_RULES = [
    ("joy", "trust",          "love"),
    ("fear", "anticipation",  "anxiety"),
    ("anger", "disgust",      "contempt"),
    ("sadness", "fear",       "despair"),
    ("joy", "anticipation",   "optimism"),
    ("trust", "fear",         "submission"),
    ("anger", "anticipation", "aggressiveness"),
    ("sadness", "surprise",   "disapproval"),
    ("fear", "surprise",      "awe"),
    ("sadness", "disgust",    "remorse")
]