import math

import pygame
from pygame.locals import *
from engine.mesh import Mesh
from engine.camera import Camera
from engine.scene import Scene
from engine.light import Point_Light
from datetime import datetime
from os import path, makedirs
from engine.vector import Vector3

# if you wanted to create a cube from defining vertices
from engine.cube import create_triangles

# setting the width and height of the screen - customisable
WIDTH, HEIGHT = 1280, 720

# define pygame variables and constants
pygame.init()
FLAGS = DOUBLEBUF
window = pygame.display.set_mode((WIDTH, HEIGHT), FLAGS, 16)
clock = pygame.time.Clock()
FPS = 60

# lock mouse to window
pygame.event.set_grab(True)
pygame.mouse.set_visible(False)

# create scene
scene = Scene()

scene.add_point_light("light-red", (-15, 8, -15))
scene.add_point_light("light-blue", (15, 8, 15))
scene.add_point_light("light-green", (-15, 8, 15))
scene.add_point_light("light-white", (15, 8, -15))
scene.lights["light-red"].color = Vector3(255,0,0)
scene.lights["light-blue"].color = Vector3(0,0,255)
scene.lights["light-green"].color = Vector3(0,255,0)
scene.lights["light-white"].color = Vector3(255,255,255)

# scene.add_point_light("light", (0,0,-10))


# add mesh to scene
# scene.create_mesh_from_obj("axis", "objects/axis.obj")
scene.create_mesh_from_obj("terrain" , "objects/terrian3.obj")

# scene.create_mesh_from_obj("cube", "objects/cube.obj")

# scene.meshes['axis'].translate.y += 4


def hsb_to_rgb(h, s, b):
    s /= 100
    b /= 100
    k = lambda n: (n + h / 60) % 6
    f = lambda n: b * (1 - s * max(0, min(k(n), 4 - k(n), 1)))
    return Vector3(255 * f(5), 255 * f(3), 255 * f(1))


# refreshing the screen
def redraw_window(camera):
    # fill the screen black
    window.fill((0,0,0))

    # draw triangles
    camera.render(scene)

def main():
    # creating a camera object
    camera = Camera(window, clock=clock)

    col = 0

    run = True
    while run:
        col += 1
        # scene.lights["light"].color = hsb_to_rgb(col % 360, 100, 100)
        # scene.lights["light"].pos = Vector3(*camera.pos.get_tuple())
        # scene.meshes["cube"].translate = Vector3(*camera.pos.get_tuple())
        pygame.display.set_caption(f"3D Engine - FPS: {str(clock.get_fps())}")
        dt = clock.tick() / 1000
        # camera.roll += dt

        # rotate the cute
        # meshCube.yaw += 1 * dt
        # meshCube.pitch += 1 * dt
        # scene.meshes['axis'].pitch += dt
        # scene.meshes['axis'].yaw += dt
        # scene.meshes['axis'].roll += dt

        # pygame system for detecting key presses and anything else that may cause an interrupt to the program
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT: run = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE: run = False
                if event.key == K_F2:
                    if not path.exists("screenshots"): makedirs("screenshots")
                    i = 2
                    while path.exists(f"screenshots/{datetime.now().strftime('%Y-%m-%d_%H.%M.%S')}_{i}.png") or path.exists(f"screenshots/{datetime.now().strftime('%Y-%m-%d_%H.%M.%S')}.png"):
                        pygame.image.save(window, f"screenshots/{datetime.now().strftime('%Y-%m-%d_%H.%M.%S')}_{i}.png")
                        i += 1
                    else:
                        pygame.image.save(window, f"screenshots/{datetime.now().strftime('%Y-%m-%d_%H.%M.%S')}.png")
                if event.key == K_F3: camera.debug = not camera.debug

        # detect current key presses
        keys = pygame.key.get_pressed()
        # movement in 3D space
        movement = camera.speed * dt
        if keys[K_w]:
            camera.pos += camera.direction * movement
        if keys[K_s]:
            camera.pos -= camera.direction * movement
        if keys[K_a]:
            camera.pos += camera.up.cross(camera.direction).normalise() * movement
        if keys[K_d]:
            camera.pos -= camera.up.cross(camera.direction).normalise() * movement
        if keys[K_SPACE]:
            camera.pos.y += movement
        if keys[K_LCTRL]:
            camera.pos.y -= movement
        if keys[K_LEFT]:
            camera.yaw += 2 * dt
        if keys[K_RIGHT]:
            camera.yaw -= 2 * dt
        if keys[K_DOWN]:
            camera.pitch += 2 * dt
        if keys[K_UP]:
            camera.pitch -= 2 * dt
        if keys[K_f]:
            camera.fov += movement
            print(camera.fov)
            camera.update_f()

        rel = pygame.mouse.get_rel()
        if pygame.mouse.get_pressed()[2] or True:
            camera.yaw -= rel[0] / 10 * dt
            # print(camera.yaw)
            camera.pitch += rel[1] / 10 * dt
            # if camera.yaw % (2*math.pi) < math.pi or camera.yaw % (2*math.pi) > -math.pi: camera.pitch += rel[1] / 10 * dt
            # else: camera.pitch -= rel[1] / 10 * dt

        redraw_window(camera)
        pygame.display.flip()

# runs when the program starts
if __name__ == "__main__":
    main()