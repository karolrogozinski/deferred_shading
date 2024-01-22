from config import GROUND, CUBES, SPHERES, CONES, LIGHTS
from utils import Camera
from objects import Object, Light
import random

class Scene:

    def __init__(self):
        self.ground = [Object(GROUND)]
        self.cubes = [Object(position = CUBES[i]) for i in range(len(CUBES))]
        self.spheres = [Object(position = SPHERES[i]) for i in range(len(SPHERES))]
        self.cones = [Object(position = CONES[i]) for i in range(len(CONES))]
        self.objects_count = len(self.cubes) + len(self.cones) + len(self.spheres)
        self.lights = [Light(position = LIGHTS[i], strength = 2 ,color = [random.uniform(a = 0.5, b = 1) for x in range(3)]) for i in range(len(LIGHTS))]
        self.camera = Camera(position = [-10, 0, 0],eulers = [0, 0, 0])
