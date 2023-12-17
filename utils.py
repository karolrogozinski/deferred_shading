import pygame
from pygame.locals import K_UP, K_DOWN, K_LEFT, K_RIGHT, \
        K_w, K_s, K_a, K_d, K_q, K_e

from scene import Scene
from config import MOVE_SPEED, ROTATION_SPEED, ZOOM_SPEED


def handle_input(scene: Scene) -> None:
    """
    Handling keyboard input.
    Currently only used for managing camera.
    """
    keys = pygame.key.get_pressed()

    # Move
    if keys[K_UP]:
        scene.camera_position[1] -= MOVE_SPEED
    if keys[K_DOWN]:
        scene.camera_position[1] += MOVE_SPEED
    if keys[K_LEFT]:
        scene.camera_position[0] += MOVE_SPEED
    if keys[K_RIGHT]:
        scene.camera_position[0] -= MOVE_SPEED

    # Rotate
    if keys[K_w]:
        scene.camera_rotation[0] += ROTATION_SPEED
    if keys[K_s]:
        scene.camera_rotation[0] -= ROTATION_SPEED
    if keys[K_a]:
        scene.camera_rotation[1] += ROTATION_SPEED
    if keys[K_d]:
        scene.camera_rotation[1] -= ROTATION_SPEED

    # Zoom
    if keys[K_q]:
        scene.camera_position[2] += ZOOM_SPEED
    if keys[K_e]:
        scene.camera_position[2] -= ZOOM_SPEED
