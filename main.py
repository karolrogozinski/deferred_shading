from OpenGL.GL import glEnable, glClear, GL_COLOR_BUFFER_BIT, \
    GL_DEPTH_BUFFER_BIT, GL_DEPTH_TEST, glLoadIdentity, glTranslatef, glRotatef
from OpenGL.GLU import gluPerspective

import pygame
from pygame.locals import DOUBLEBUF, OPENGL, QUIT

from scene import Scene
from utils import handle_input
from config import WIDTH, HEIGTH


def main():
    pygame.init()

    pygame.display.set_mode((WIDTH, HEIGTH), DOUBLEBUF | OPENGL)
    glEnable(GL_DEPTH_TEST)

    scene = Scene()
    clock = pygame.time.Clock()

    # Main loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return

        handle_input(scene)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # Camera settings
        gluPerspective(45, (WIDTH / HEIGTH), 0.1, 50.0)
        glTranslatef(*scene.camera_position)
        glRotatef(scene.camera_rotation[0], 1, 0, 0)
        glRotatef(scene.camera_rotation[1], 0, 1, 0)

        scene.render()

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
