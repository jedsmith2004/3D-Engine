from engine.vector import Vector3


class Point_Light:
    def __init__(self, pos):
        self.pos = Vector3(pos[0], pos[1], pos[2])
        self.intensity = 1000
        self.color = Vector3(255, 255, 255)


class Directional_Light:
    def __init__(self, dir):
        self.dir = dir.normalise()
        self.intensity = 2000
        self.color = Vector3(255, 255, 255)