from math import pi, sin, cos

from OpenGL.GL import glBegin, glColor3f, GL_QUADS, glVertex3f, glEnd, \
    GL_TRIANGLES, glEnable, glLightfv, GL_LIGHT0, GL_POSITION, GL_DIFFUSE, \
    GL_SPECULAR, GL_LIGHTING
from OpenGL import GL


class Object:
    def __init__(self, position, color):
        self.position = position
        self.color = color

    def draw(self):
        pass


class Cube(Object):
    def __init__(self, size, position, color):
        super().__init__(position, color)
        self.size = size

    def draw(self):
        glBegin(GL_QUADS)
        glColor3f(*self.color)

        vertices = [
            (-0.5, -0.5, -0.5),
            (0.5, -0.5, -0.5),
            (0.5, 0.5, -0.5),
            (-0.5, 0.5, -0.5),
            (0.5, -0.5, 0.5),
            (-0.5, -0.5, 0.5),
            (-0.5, 0.5, 0.5),
            (0.5, 0.5, 0.5)
        ]

        indices = [
            (0, 1, 2, 3),
            (1, 4, 7, 2),
            (4, 5, 6, 7),
            (5, 0, 3, 6),
            (3, 2, 7, 6),
            (5, 4, 1, 0)
        ]

        for index in indices:
            for i in index:
                glVertex3f(
                    vertices[i][0] * self.size[0] + self.position[0],
                    vertices[i][1] * self.size[1] + self.position[1],
                    vertices[i][2] * self.size[2] + self.position[2]
                )

        glEnd()


class Floor(Object):
    def __init__(self, size, position, color):
        super().__init__(position, color)
        self.size = size

    def draw(self):
        glBegin(GL_QUADS)
        glColor3f(*self.color)

        vertices = [
            (-0.5, -0.5, -0.5),
            (0.5, -0.5, -0.5),
            (0.5, -0.5, 0.5),
            (-0.5, -0.5, 0.5),
        ]

        for i in range(4):
            glVertex3f(
                vertices[i][0] * self.size[0] + self.position[0],
                vertices[i][1] * self.size[1] + self.position[1],
                vertices[i][2] * self.size[2] + self.position[2]
            )

        glEnd()


class Cone(Object):
    def __init__(self, height, position, color, radius):
        super().__init__(position, color)
        self.radius = radius
        self.height = height

    def draw(self):
        glBegin(GL_TRIANGLES)
        glColor3f(*self.color)

        num_segments = 30
        for i in range(num_segments):
            theta1 = 2.0 * pi * float(i) / float(num_segments)
            theta2 = 2.0 * pi * float(i + 1) / float(num_segments)

            x1 = self.radius * cos(theta1) + self.position[0]
            y1 = self.position[1]
            z1 = self.radius * sin(theta1) + self.position[2]

            x2 = self.radius * cos(theta2) + self.position[0]
            y2 = self.position[1]
            z2 = self.radius * sin(theta2) + self.position[2]

            x3 = self.position[0]
            y3 = self.height + self.position[1]
            z3 = self.position[2]

            glVertex3f(x1, y1, z1)
            glVertex3f(x2, y2, z2)
            glVertex3f(x3, y3, z3)

            glVertex3f(self.position[0], self.position[1], self.position[2])
            glVertex3f(x1, y1, z1)
            glVertex3f(x2, y2, z2)

        glEnd()


class Sphere(Object):
    def __init__(self, radius, position, color):
        super().__init__(position, color)
        self.radius = radius

    def draw(self):
        glBegin(GL_TRIANGLES)
        glColor3f(*self.color)

        num_segments = 30
        for i in range(num_segments):
            for j in range(num_segments):
                theta1 = 2.0 * pi * float(i) / float(num_segments)
                phi1 = pi * float(j) / float(num_segments)
                theta2 = 2.0 * pi * float(i + 1) / float(num_segments)
                phi2 = pi * float(j + 1) / float(num_segments)

                x1 = self.radius * sin(phi1) * cos(theta1) + self.position[0]
                y1 = self.radius * sin(phi1) * sin(theta1) + self.position[1]
                z1 = self.radius * cos(phi1) + self.position[2]

                x2 = self.radius * sin(phi1) * cos(theta2) + self.position[0]
                y2 = self.radius * sin(phi1) * sin(theta2) + self.position[1]
                z2 = self.radius * cos(phi1) + self.position[2]

                x3 = self.radius * sin(phi2) * cos(theta2) + self.position[0]
                y3 = self.radius * sin(phi2) * sin(theta2) + self.position[1]
                z3 = self.radius * cos(phi2) + self.position[2]

                x4 = self.radius * sin(phi2) * cos(theta1) + self.position[0]
                y4 = self.radius * sin(phi2) * sin(theta1) + self.position[1]
                z4 = self.radius * cos(phi2) + self.position[2]

                glVertex3f(x1, y1, z1)
                glVertex3f(x2, y2, z2)
                glVertex3f(x3, y3, z3)

                glVertex3f(x1, y1, z1)
                glVertex3f(x3, y3, z3)
                glVertex3f(x4, y4, z4)

        glEnd()

class Light(Object):
    LIGHT_CONSTANTS = {
        'LIGHT0': GL.GL_LIGHT0,
        'LIGHT1': GL.GL_LIGHT1,
        'LIGHT2': GL.GL_LIGHT2,
        'LIGHT3': GL.GL_LIGHT3,
        'LIGHT4': GL.GL_LIGHT4,
        'LIGHT5': GL.GL_LIGHT5,
        'LIGHT6': GL.GL_LIGHT6,
        'LIGHT7': GL.GL_LIGHT7
    }

    def __init__(self, name, color, position):
        super().__init__(position, color)
        self.name = name

    def activate(self):
        glEnable(GL_LIGHTING)
        glEnable(self.LIGHT_CONSTANTS[self.name])
        glLightfv(self.LIGHT_CONSTANTS[self.name], GL_POSITION, \
                    (*self.position, 1.0))
        glLightfv(self.LIGHT_CONSTANTS[self.name], GL_DIFFUSE, \
                    (*self.color, 1.0))
        glLightfv(self.LIGHT_CONSTANTS[self.name], GL_SPECULAR, \
                    (*self.color, 1.0))