import math
import math as m
from engine.matrix import Matrix
from engine.vector import Vector3
import pygame
from engine.triangle import Triangle
from threading import Thread

# bubble sort algorithm
def bubble_sort(lst):
    while True:
        swaps = 0
        for i in range(len(lst)):
            if i != len(lst) - 1:
                if (lst[i].vertices[0].z, lst[i].vertices[1].z, lst[i].vertices[2].z) < (
                        lst[i + 1].vertices[0].z, lst[i + 1].vertices[1].z, lst[i + 1].vertices[2].z):
                    swaps += 1
                    temp = lst[i]
                    lst[i] = lst[i + 1]
                    lst[i + 1] = temp
        print(swaps)

        if swaps == 0: return lst

# part of the quicksort algorithm
def partition(l, r, nums):
    # Last element will be the pivot and the first element the pointer
    pivot, ptr = nums[r], l
    p_z = Zsort(pivot)
    for i in range(l, r):
        if Zsort(nums[i]) <= p_z:
            # Swapping values smaller than the pivot to the front
            nums[i], nums[ptr] = nums[ptr], nums[i]
            ptr += 1
    # Finally swapping the last element with the pointer indexed number
    nums[ptr], nums[r] = nums[r], nums[ptr]
    return ptr

# quicksort algorithm
def quicksort(l, r, nums):
    if len(nums) == 1:  # Terminating Condition for recursion.
        return nums
    if l < r:
        pi = partition(l, r, nums)
        quicksort(l, pi - 1, nums)  # Recursively sorting the left values
        quicksort(pi + 1, r, nums)  # Recursively sorting the right values
    return nums

# comparison for swapping
def Zsort(val):
    if type(val) == Triangle:
        return (val.vertices[0].z + val.vertices[1].z + val.vertices[2].z) / 3.0 # finds average z value
    else: return val[2]


class Camera:
    def __init__(self, window, clock=None):
        self.pos = Vector3(0,0,-10)
        self.direction = Vector3(0,0,1)
        self.up = Vector3(0,1,0)
        self.target = self.pos
        self.speed = 8

        self.pitch = 0.0
        self.yaw = 0.0
        # self.roll = 35.0

        self.rotation = Matrix.rotation_y(self.yaw)
        self.view_matrix = Matrix.identity()

        self.window = window
        self.s_width = window.get_width()
        self.s_height = window.get_height()
        self.a = self.s_height / self.s_width
        self.fov = 90
        self.f = 1/(m.tan(self.fov * 0.5 / 180 * 3.14159))
        self.z_far = 10000
        self.z_near = 0.1
        self.q = self.z_far/(self.z_far-self.z_near)

        self.wireframe = False
        self.axis = False
        self.stats = False
        self.clock = clock
        self.vis_tris = 0
        self.total_tris = 0
        self.mesh_info = False
        self.clip_debug = False
        self.show_lights = False
        self.light_icon = pygame.image.load("icons/point_light_icon_white.png").convert_alpha()


        self.debug = False

    def update_f(self):
        self.f = 1 / (m.tan(self.fov * 0.5 / 180 * 3.14159))

    def render(self, scene):
        # creates 'look at' matrix and inverts it
        self.direction = Vector3(0, 0, 1)
        self.up = Vector3(0, 1, 0)
        self.target = Vector3(0, 0, 1)
        self.pitch = max(-math.pi/2+0.001, min(self.pitch, math.pi/2-0.001))
        rotation_x = Matrix.rotation_x(self.pitch)
        rotation_y = Matrix.rotation_y(self.yaw)
        # rotation_z = Matrix.rotation_z(self.roll)
        self.rotation = rotation_x.multiply_matrix(rotation_y)
        self.direction = self.rotation.matrix_by_vector(self.target)
        self.target = self.pos + self.direction
        self.view_matrix = Matrix.point_at(self.pos, self.target, self.up)  # check point at
        self.view_matrix.quick_inverse()  # check inverse
        # self.view_matrix = rotation_z.multiply_matrix(self.view_matrix)
        self.target = Vector3(0, 0, 1)

        render_light_icons = []
        if self.show_lights or self.debug:
            render_light_icons = self.render_light_icons(scene)

        render_queue = []

        self.total_tris = 0

        # render each mesh
        for mesh in scene.meshes:
            self.total_tris += len(scene.meshes[mesh].triangles)
            render_queue += scene.meshes[mesh].update(self, scene.lights)

        self.render_tris(render_queue + render_light_icons)


    def render_light_icons(self, scene):
        to_render = []
        for light in scene.lights:
            # orig_center = self.light_icon.get_rect().center
            light_pos = scene.lights[light].pos
            light_pos = self.view_matrix.matrix_by_vector(light_pos)
            z = light_pos.z

            if z > 1:
                light_pos = Matrix.projection(self).matrix_by_vector(light_pos)
                light_pos += 1
                light_pos *= [0.5 * self.s_width, 0.5 * self.s_height, 0.5]
                icon = pygame.transform.scale(self.light_icon,
                                              ((self.light_icon.get_width() / z, self.light_icon.get_height() / z)))
                var = pygame.PixelArray(icon)
                var.replace((255,255,255),scene.lights[light].color.get_tuple())
                del var
                send_z = light_pos.z
                light_pos = light_pos.to_Vector2()
                light_pos = light_pos
                to_render.append([icon, light_pos.get_tuple(), send_z])
        return to_render

    def render_tris(self, queue):
        # queue.sort(key=Zsort)
        self.vis_tris = len(queue)
        queue = quicksort(0, self.vis_tris-1, queue)
        for t in queue:
            # print(type(t))
            if type(t) == Triangle:
                # draw faces
                t.fill_triangle(self.window, t.temp_col)
                # draw wireframe
                if self.wireframe or self.debug:
                    t.draw_triangle(self.window)
            else:
                self.window.blit(t[0], t[1])

        if self.axis or self.debug:
            self.draw_axis()

        if self.stats or self.debug:
            self.draw_stats()


    def draw_axis(self):
        axis_origin = Vector3(self.s_width - 70, 70, 0)

        axis = [(self.rotation.matrix_by_vector(Vector3(50, 0, 0)), (255, 0, 0)),
                (self.rotation.matrix_by_vector(Vector3(0, -50, 0)), (0, 255, 0)),
                (self.rotation.matrix_by_vector(Vector3(0, 0, 50)), (0, 0, 255))]

        axis.sort(key=lambda a: a[0].z)
        axis = axis[::-1]

        for a in axis:
            pygame.draw.line(self.window, a[1], axis_origin.to_Vector2().get_tuple(),
                            (axis_origin + a[0]).to_Vector2().get_tuple(), 3)

        pygame.draw.circle(self.window, (255, 255, 255), axis_origin.to_Vector2().get_tuple(), 5)

    def draw_stats(self):
        FONT = pygame.font.SysFont('', 32)

        WHITE = (255, 255, 255)
        stats = []
        if self.clock is not None:
            fps = FONT.render(f"FPS ~ {str(round(self.clock.get_fps(), 2))}", True, WHITE)

            stats.append(fps)

        coords_x = FONT.render(f"x ~ {round(self.pos.x, 2)}", True, WHITE)
        stats.append(coords_x)
        coords_y = FONT.render(f"y ~ {round(self.pos.y, 2)}", True, WHITE)
        stats.append(coords_y)
        coords_z = FONT.render(f"z ~ {round(self.pos.z, 2)}", True, WHITE)
        stats.append(coords_z)

        vis_tris = FONT.render(f"TRIS ~ {round(self.vis_tris, 2)} / {self.total_tris}", True, WHITE)
        stats.append(vis_tris)

        buffer = 5
        total_h = 0
        for i in range(len(stats)):
            self.window.blit(stats[i], (buffer, buffer * (i + 1) + total_h))
            total_h += stats[i].get_height()