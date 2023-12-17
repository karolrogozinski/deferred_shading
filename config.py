"""
WINDOW PARAMS
"""
WIDTH = 800
HEIGTH = 600


"""
OBJECTS
    ((size), (position), (color))
"""
OBJECTS = {
    'CUBES': (
        ((1, 1, 1), (0, .5, 2), (1, 0, 0)),
        ((1, 1, 1), (3, .5, 0), (0, 0, 1)),
    ),
    'FLOOR': (
        ((8, 1, 8), (0, .49, 0), (0.5, 0.5, 0.5)),
    ),
    'CONES': (
        # height, position, color, radius
        (2, (-2, 0, 1), (.8, .1, .6), 1),
    ),
    'SPHERES': (
        (1, (-1.5, 1, -2), (0, 1, 0)),
    )
}


"""
CAMERA
"""
INIT_POS = [1, -1, -15]
INIT_ROT = [30, 15]

MOVE_SPEED = 0.1
ROTATION_SPEED = 1
ZOOM_SPEED = 0.1
