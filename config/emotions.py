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


CLUSTER_RANGES = {
    "threat": {

        "LOW":         (0.25, 0.26, 0.38),
        "MEDIUM":      (0.35, 0.45, 0.55),
        "MEDIUM_HIGH": (0.50, 0.60, 0.70),
        "HIGH":        (0.55, 0.65, 0.65),
    },

    "reward": {

        "LOW":         (0.30, 0.31, 0.38),
        "MEDIUM":      (0.35, 0.42, 0.48),
        "MEDIUM_HIGH": (0.45, 0.50, 0.54),
        "HIGH":        (0.50, 0.60, 0.60),
    },

    "novelty": {

        "LOW":         (0.25, 0.26, 0.40),
        "MEDIUM":      (0.35, 0.50, 0.65),
        "MEDIUM_HIGH": (0.55, 0.70, 0.80),
        "HIGH":        (0.60, 0.70, 0.70),
    },

    "familiarity": {

        "LOW":         (0.35, 0.36, 0.44),
        "MEDIUM":      (0.40, 0.48, 0.55),
        "MEDIUM_HIGH": (0.50, 0.57, 0.61),
        "HIGH":        (0.58, 0.68, 0.68),
    },

    "urgency": {

        "LOW":         (0.30, 0.31, 0.40),
        "MEDIUM":      (0.35, 0.47, 0.58),
        "MEDIUM_HIGH": (0.50, 0.62, 0.70),
        "HIGH":        (0.60, 0.72, 0.72),
    },

    "social_relevance": {

        "LOW":         (0.25, 0.26, 0.34),
        "MEDIUM":      (0.30, 0.40, 0.50),
        "MEDIUM_HIGH": (0.45, 0.53, 0.60),
        "HIGH":        (0.55, 0.65, 0.65),
    },

    "discomfort": {

        "LOW":         (0.30, 0.31, 0.38),
        "MEDIUM":      (0.35, 0.44, 0.55),
        "MEDIUM_HIGH": (0.50, 0.58, 0.66),
        "HIGH":        (0.50, 0.62, 0.62),
    },

    "affinity": {

        "LOW":         (0.35, 0.36, 0.45),
        "MEDIUM":      (0.40, 0.50, 0.62),
        "MEDIUM_HIGH": (0.55, 0.65, 0.75),
        "HIGH":        (0.60, 0.80, 0.80),
    }
}

PENALTIES = {
    "LOW": 0.0,
    "MEDIUM": 0.10,
    "MEDIUM_HIGH": 0.15,
    "HIGH": 0.20
}


EMOTION_PROFILES = {

    "fear": {
        "threat": "HIGH",
        "novelty": "HIGH",
        "familiarity": "LOW",
        "urgency": "HIGH",
        "discomfort": "MEDIUM_HIGH"
    },

    "anger": {
        "threat": "HIGH",
        "novelty": "HIGH",
        "familiarity": "LOW",
        "urgency": "HIGH",
        "discomfort": "HIGH",
        "social_relevance": "MEDIUM"
    },

    "joy": {
        "reward": "HIGH",
        "affinity": "MEDIUM_HIGH",
        "novelty": "MEDIUM",
        "urgency": "LOW",
        "threat": "LOW",
        "discomfort": "LOW"
    },

    "sadness": {
        "discomfort": "HIGH",
        "threat": "MEDIUM",
        "reward": "LOW",
        "urgency": "LOW",
        "affinity": "MEDIUM_HIGH",
        "novelty": "LOW"
    },

    "trust": {
        "familiarity": "HIGH",
        "reward": "MEDIUM_HIGH",
        "social_relevance": "HIGH",
        "affinity": "HIGH",
        "threat": "LOW"
    },

    "disgust": {
        "discomfort": "HIGH",
        "reward": "LOW",
        "social_relevance": "MEDIUM"
    },

    "anticipation": {
        "reward": "MEDIUM_HIGH",
        "urgency": "MEDIUM",
        "novelty": "MEDIUM"
    },

    "surprise": {
        "novelty": "HIGH",
        "familiarity": "LOW",
        "urgency": "MEDIUM"
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
        (0.00, 0.40, "pensiveness"),
        (0.40, 0.75, "sadness"),
        (0.75, 1.01, "grief")
    ],

    "trust": [
        (0.00, 0.40, "acceptance"),
        (0.40, 0.75, "trust"),
        (0.75, 1.01, "admiration")
    ],

    "disgust": [
        (0.00, 0.40, "boredom"),
        (0.40, 0.75, "disgust"),
        (0.75, 1.01, "loathing")
    ],

    "anticipation": [
        (0.00, 0.40, "interest"),
        (0.40, 0.75, "anticipation"),
        (0.75, 1.01, "vigilance")
    ],

    "surprise": [
        (0.00, 0.40, "distraction"),
        (0.40, 0.75, "surprise"),
        (0.75, 1.01, "amazement")
    ]
}

COMPOUNDING_RULES = [
    # PRIMARY DYADS
    ("joy", "trust", "love"),
    ("trust", "fear", "submission"),
    ("fear", "surprise", "alarm"),
    ("surprise", "sadness", "disappointment"),
    ("sadness", "disgust", "remorse"),
    ("disgust", "anger", "contempt"),
    ("anger", "anticipation", "aggression"),
    ("anticipation", "joy", "optimism"),

    # SECONDARY DYADS
    ("joy", "fear", "guilt"),
    ("trust", "surprise", "curiosity"),
    ("fear", "sadness", "despair"),
    ("surprise", "disgust", "unbelief"),
    ("sadness", "anger", "envy"),
    ("disgust", "anticipation", "cynicism"),
    ("anger", "joy", "pride"),
    ("anticipation", "trust", "hope"),

    # TERTIARY DYADS
    ("joy", "surprise", "delight"),
    ("trust", "sadness", "sentimentality"),
    ("fear", "disgust", "shame"),
    ("surprise", "anger", "outrage"),
    ("sadness", "anticipation", "pessimism"),
    ("disgust", "joy", "morbidness"),
    ("anger", "trust", "dominance"),
    ("anticipation", "fear", "anxiety"),

    # OPPOSITE DYADS
    ("joy", "sadness", "bittersweetness"),
    ("trust", "disgust", "ambivalence"),
    ("fear", "anger", "frozenness"),
    ("surprise", "anticipation", "confusion")
]