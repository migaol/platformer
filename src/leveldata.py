test_level = [
    '                                                                                                    ',
    '                                                                                                    ',
    ' xx    xxx            xx                                                                            ',
    ' xx p              s z                                                                              ',
    ' xxxx         xxz   z    xx                                                                         ',
    '                                                                                                    ',
    '                                                                                                    ',
    ' xxxx       xx                                                                                      ',
    '                                                                                                    ',
    ' xx    x                                     xxxxxx                                                 ',
    '             s        s           x          x    x                                                 ',
    '       x          xx  xxx         x          xx   x                         x                       ',
    '    xxxx          xx  xxxx  z     x          x               z z z z z      x                       ',
    'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
]

level_1_1 = {
    'assets_path':  './assets/level/level_1/',
    'terrain':      './leveldata/1/1-1/1-1_terrain.csv',
    'animated_z1':  './leveldata/1/1-1/1-1_animated_z1.csv',
    'static_z1':    './leveldata/1/1-1/1-1_static_z1.csv',
    'static_z2':    './leveldata/1/1-1/1-1_static_z2.csv',
    'entities':     './leveldata/1/1-1/1-1_entities.csv'
}

world_data = [
    {
        'map': {
            'assets_path':  './assets/level/level_1/',
            'player':       './leveldata/1/1-levelmap/1-levelmap_player.csv',
            'terrain':      './leveldata/1/1-levelmap/1-levelmap_terrain.csv',
            'path':         './leveldata/1/1-levelmap/1-levelmap_path.csv',
            'portal':       './leveldata/1/1-levelmap/1-levelmap_levels.csv'
        },
        'levels': [
            level_1_1
        ]
    }
]