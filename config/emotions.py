NEURON_EMOTION_MAPPING = {
    "threat": {
        "fear": 0.45, ## DROPPED FROM .55 - .45
        "anger": 0.35, ## RAISED FROM 0.20 - 0.35
        "disgust": 0.10,
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
        "anticipation": 0.40,
        "fear": 0.10 ## DROPPED FROM 0.20 - 0.10
    },
    "familiarity": {
        "trust": 0.70,
        "joy": 0.30
    },
    "social_relevance": {
        "anticipation": 0.35, ## 0.25 - 0.35
        "surprise": 0.25, ## added 
        "trust": 0.10, ## 0.35 - 0.1
        "fear": 0.20, ## 0.25 - 0.20
        "joy": 0.10 ## 0.15 - 0.10
    },
    "affinity": {
        "trust": 0.40, ## DROPPED FROM 0.4 - 0.35
        "joy": 0.25, ## 0.3 - 0.25
        "fear": 0.10,  ## 0.15 - 0.10
        "sadness": 0.10, ## added sadness
        "anticipation": 0.15
    },
    "discomfort": {
        "sadness": 0.30,
        "disgust": 0.30,
        "anger": 0.25, ## RAISD FROM 0.20 - 0.35
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