import pygame
from pygame.locals import *
from cube import create_triangles

from mesh import Mesh
from camera import Camera

WIDTH, HEIGHT = 720, 720

pygame.init()
flags = DOUBLEBUF
window = pygame.display.set_mode((WIDTH, HEIGHT), flags, 16)
clock = pygame.time.Clock()
fps = 60

meshCube = Mesh()
# meshCube.load_from_obj("hammer.obj")
create_triangles(meshCube)

def redraw_window(camera):
    window.fill((0,0,0))

    # draw triangles
    meshCube.update(camera)

def main():
    camera = Camera(window)

    run = True
    while run:
        dt = clock.tick(fps) / 1000
        meshCube.yaw += 1 * dt
        meshCube.pitch += 1 * dt

        events = pygame.event.get()
        for event in events:
            if event.type == QUIT: run = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE: run = False

        redraw_window(camera)
        pygame.display.update()


if __name__ == "__main__":
    main()