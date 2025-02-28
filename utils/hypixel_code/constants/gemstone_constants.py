_breakingPowerSeven: dict = {
    22: 4000,
    21: 4187,
    20: 4391,
    19: 4616,
    18: 4865,
    17: 5143,
    16: 5455,
    15: 5807,
    14: 6207,
    12: 7200,
    11: 7827,
    10: 8572,
    9: 9474,
    8: 10589,
    7: 12001,
    6: 13847,
    5: 16364,
    4: 20000
}
_breakingPowerEight: dict = {
    22: 5067,
    21: 5303,
    20: 5561,
    19: 5847,
    18: 6163,
    17: 6515,
    16: 6910,
    15: 7355,
    14: 7863,
    13: 8445,
    12: 9120,
    11: 9914,
    10: 10858,
    9: 12001,
    8: 13412,
    7: 15201,
    6: 17539,
    5: 20728,
    4: 25334
}
_breakingPowerNine: dict = {
    24: 6368,
    23: 6639,
    22: 6934,
    21: 7256,
    20: 7610,
    19: 8001,
    18: 8433,
    17: 8915,
    16: 9455,
    15: 10065,
    11: 13566,
    10: 14858,
    9: 16422,
    8: 18353,
    7: 20801,
    6: 24000,
    5: 28364,
    4: 34667
}

THRESHOLDS: dict = {
    'RUBY': {
        'breakingPower': 6,
        'thresholds': {
            22: 3067,
            21: 3210,
            20: 3366,
            19: 3539,
            18: 3730,
            17: 3943,
            16: 4182,
            15: 4452,
            14: 4759,
            13: 5112,
            12: 5520,
            11: 6001,
            10: 6572,
            9: 7264,
            8: 8118,
            7: 9201,
            6: 10616,
            5: 12546,
            4: 15334
        }
    },
    'JADE': {'breakingPower': 7, 'thresholds': _breakingPowerSeven},
    'AMBER': {'breakingPower': 7, 'thresholds': _breakingPowerSeven},
    'SAPPHIRE': {'breakingPower': 7, 'thresholds': _breakingPowerSeven},
    'AMETHYST': {'breakingPower': 7, 'thresholds': _breakingPowerSeven},
    'TOPAZ': {'breakingPower': 8, 'thresholds': _breakingPowerEight},
    'OPAL': {'breakingPower': 8, 'thresholds': _breakingPowerEight},
    'JASPER': {
        'breakingPower': 9,
        'thresholds': {
            22: 6400,
            21: 6698,
            20: 7025,
            19: 7385,
            18: 7784,
            17: 8229,
            16: 8728,
            15: 9291,
            14: 9932,
            13: 10667,
            12: 11520,
            11: 12522,
            10: 13715,
            9: 15158,
            8: 16942,
            7: 19201,
            6: 22154,
            5: 26182,
            4: 32000
        }
    },
    'ONYX': {'breakingPower': 9, 'thresholds': _breakingPowerNine},
    'AQUAMARINE': {'breakingPower': 9, 'thresholds': _breakingPowerNine},
    'CITRINE': {'breakingPower': 9, 'thresholds': _breakingPowerNine},
    'PERIDOT': {'breakingPower': 9, 'thresholds': _breakingPowerNine}
}
