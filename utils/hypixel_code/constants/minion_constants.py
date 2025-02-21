"""
Changelog:
    - 21-02-2025 - Merged the two inferno constants into one constant, INFERNO_MINION, for it to be more organized
"""

INFERNO_MINION: dict = {
    1: {'speed': 1013, 'storage': 1},
    2: {'speed': 982, 'storage': 3},
    3: {'speed': 950, 'storage': 3},
    4: {'speed': 919, 'storage': 6},
    5: {'speed': 886, 'storage': 6},
    6: {'speed': 855, 'storage': 9},
    7: {'speed': 823, 'storage': 9},
    8: {'speed': 792, 'storage': 12},
    9: {'speed': 760, 'storage': 12},
    10: {'speed': 728, 'storage': 15},
    11: {'speed': 697, 'storage': 15}
}

INFERNO_MINION_TABLE: dict = {
    'Base': {
        'Chili Pepper': 1 / 136,
        'Inferno Vertex': 1 / 5950,
        'Inferno Apex': 1 / 1309091,
        'Reaper Pepper': 1 / 458182,
        'Gabagool The Fish': 1 / 3927273
    },
    'Eyesdrops': {
        'Chili Pepper': 1 / 104.6,
        'Inferno Vertex': 1 / 4576.9,
        'Inferno Apex': 1 / 1006993.1,
        'Reaper Pepper': 1 / 352447.7,
        'Gabagool The Fish': 1 / 3020979.2
    }
}
