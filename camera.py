import math as m
from matrix import Matrix
from vector import Vector3


class Camera:
    def __init__(self,window):
        self.pos = Vector3(0,0,0)
        self.window = window
        self.s_width = window.get_width()
        self.s_height = window.get_height()
        self.a = self.s_width / self.s_height
        self.fov = 90
        self.f = 1/(m.tan(self.fov * 0.5 / 180 * 3.14159))
        self.z_far = 1000
        self.z_near = 0.1
        self.q = self.z_far/(self.z_far-self.z_near)
        self.proj_matrix = Matrix([[(self.a * self.f), 0, 0, 0],
                              [0, self.f, 0, 0],
                              [0, 0, self.q, 1],
                              [0, 0, -self.z_near * self.q, 0]])