from engine.mesh import Mesh
from engine.light import Point_Light

class Scene:

    def __init__(self):
        self.meshes = {}
        self.lights = {}

    def add_mesh(self, name, mesh):
        self.meshes[name] = mesh

    def create_mesh_from_obj(self, name, path):
        mesh = Mesh()
        mesh.load_from_obj(path)
        self.meshes[name] = mesh

    def add_point_light(self, name, pos):
        self.lights[name] = Point_Light(pos)