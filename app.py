import pygame as pg
from pygame.locals import K_UP, K_DOWN, K_LEFT, K_RIGHT, \
        K_w, K_s, K_a, K_d, K_q, K_e
from config import WIDTH, HEIGHT
from scene import Scene
from engine import Engine


class App:

    def __init__(self):
        pg.init()
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)
        pg.display.set_mode((WIDTH,HEIGHT), pg.OPENGL|pg.DOUBLEBUF)
        pg.mouse.set_pos((320,240))

        self.scene = Scene()

        self.engine = Engine(self.scene)

        self.mainLoop()

    def mainLoop(self):
        running = True
        while (running):
            for event in pg.event.get():
                if (event.type == pg.KEYDOWN and event.key==pg.K_ESCAPE):
                    running = False
            self.handleKeys()
            self.engine.draw(self.scene)
        self.quit()

    def handleKeys(self):
        keys = pg.key.get_pressed()

        # Move
        if keys[K_UP]:
            self.scene.camera.position[0] += 0.05
        if keys[K_DOWN]:
            self.scene.camera.position[0] -= 0.05
        if keys[K_LEFT]:
            self.scene.camera.position[1] += 0.05
        if keys[K_RIGHT]:
            self.scene.camera.position[1] -= 0.05
        # Rotate
        if keys[K_w]:
            self.scene.camera.eulers[0] += 0.5
        if keys[K_s]:
            self.scene.camera.eulers[0] -= 0.5
        if keys[K_a]:
            self.scene.camera.eulers[1] += 0.5
        if keys[K_d]:
            self.scene.camera.eulers[1] -= 0.5
        # Zoom
        if keys[K_q]:
            self.scene.camera.position[2] += 0.05
        if keys[K_e]:
            self.scene.camera.position[2] -= 0.05

    def quit(self):

        self.engine.quit()
        pg.quit()


myApp = App()