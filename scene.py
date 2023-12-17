from config import INIT_POS, INIT_ROT, OBJECTS
from objects import Cube, Floor, Cone, Sphere


class Scene:
    def __init__(self: None) -> None:
        self.objects = []
        self.lights = []
        self.camera_position = INIT_POS
        self.camera_rotation = INIT_ROT

        self.create_objects()

    def add_light(self, light) -> None:
        self.lights.append(light)

    def create_objects(self) -> None:
        for cube in OBJECTS['CUBES']:
            cube_ = Cube(cube[0], cube[1], cube[2])
            self.objects.append(cube_)

        for floor in OBJECTS['FLOOR']:
            flore_ = Floor(floor[0], floor[1], floor[2])
            self.objects.append(flore_)

        for cone in OBJECTS['CONES']:
            cone_ = Cone(cone[0], cone[1], cone[2], cone[3])
            self.objects.append(cone_)

        for sphere in OBJECTS['SPHERES']:
            sphere_ = Sphere(sphere[0], sphere[1], sphere[2])
            self.objects.append(sphere_)

    def render(self) -> None:
        for obj in self.objects:
            obj.draw()
