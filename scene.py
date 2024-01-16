from config import INIT_POS, INIT_ROT, OBJECTS, LIGHTS
from objects import Cube, Floor, Cone, Sphere, Light


class Scene:
    def __init__(self: None) -> None:
        self.objects = []
        self.lights = []
        self.camera_position = INIT_POS
        self.camera_rotation = INIT_ROT

        self.create_objects()
        self.create_lights()

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

    def create_lights(self) -> None:
        for light_name, light_params in LIGHTS.items():
            light = Light(light_name, light_params[0], light_params[1])
            self.lights.append(light)

    def render(self) -> None:
        for obj in self.objects:
            obj.draw()
        for light in self.lights:
            light.activate()
