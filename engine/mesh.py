import math

from engine.matrix import Matrix
from engine.vector import Vector3
from engine.triangle import Triangle
from engine.tools import clip_tri_by_plane
from engine.light import Directional_Light, Point_Light
from colorama import Fore


# create a mesh object for every object in the scene
class Mesh:
    def __init__(self):
        self.triangles = []
        # self.color = (255,128,75)
        self.color = (255, 255, 255)
        self.transform = Matrix.identity()
        self.translate = Vector3(0, 0, 0)
        self.scale = 1
        self.pitch = 0
        self.yaw = 0
        self.roll = 0

    # create triangles by loading them from .obj file
    def load_from_obj(self, path):
        try:
            with open(path,'r') as f:
                verts = []
                lines = f.readlines()
                for line in lines:
                    if line[0] == "v" and line[1] == " ":
                        v = line.split(" ")
                        verts.append([float(v[1]),float(v[2]),float(v[3])])
                    elif line[0] == "f":
                        blocks = line.split(" ")
                        # pick the first value from each section
                        v1 = verts[int(blocks[1].split("/")[0])-1]
                        v2 = verts[int(blocks[2].split("/")[0])-1]
                        v3 = verts[int(blocks[3].split("/")[0])-1]
                        # add a triangle based on these values
                        self.triangles.append(Triangle((v1[0],v1[1],v1[2]),
                                                            (v2[0],v2[1],v2[2]),
                                                            (v3[0],v3[1],v3[2]), col=self.color))
        except Exception as e:
            if path[-4:] != ".obj" and type(e) != FileNotFoundError:
                print(f"{Fore.RED}invalid file type for '{path}', please use .obj files{Fore.WHITE}")
            else:
                print(f"{Fore.RED}{e}{Fore.WHITE}")

    # render the object to the screen
    def update(self, camera, lights):
        to_render = []

        # defines rotation matrices
        m_rot_x = Matrix.rotation_x(self.pitch)
        m_rot_y = Matrix.rotation_y(self.yaw)
        m_rot_z = Matrix.rotation_z(self.roll)
        m_world = m_rot_z.multiply_matrix(m_rot_y).multiply_matrix(m_rot_x)


        for tri in self.triangles:
            transformed = m_world.tri_by_4x4(tri)

            # translate vertices based on position
            transformed.vertices[0] += self.translate
            transformed.vertices[1] += self.translate
            transformed.vertices[2] += self.translate

            # define two lines of triangle
            line1 = transformed.vertices[1] - transformed.vertices[0]
            line2 = transformed.vertices[2] - transformed.vertices[0]

            # find the normal of the triangle
            normal = line1.cross(line2).normalise()

            # vector from the camera to the vertex
            camera_ray = transformed.vertices[0] - camera.pos

            # only render if visible
            if normal.dot(camera_ray) < 0.0:

                # apply camera transformations
                viewed = camera.view_matrix.tri_by_4x4(transformed)

                # clip triangles
                clipped_tris = clip_tri_by_plane(Vector3(0.0, 0.0, 0.1), Vector3(0.0, 0.0, 1.0), viewed,
                                                 debug=(camera.debug or camera.clip_debug))

                for clipped in clipped_tris:

                    # apply projection matrix
                    projected = Matrix.projection(camera).tri_by_4x4(clipped)

                    # moves mesh to centre of screen
                    projected.vertices[0] += 1
                    projected.vertices[1] += 1
                    projected.vertices[2] += 1

                    # enlarges mesh to size of screen
                    projected.vertices[0] *= [0.5 * camera.s_width, 0.5 * camera.s_height, 0.5]
                    projected.vertices[1] *= [0.5 * camera.s_width, 0.5 * camera.s_height, 0.5]
                    projected.vertices[2] *= [0.5 * camera.s_width, 0.5 * camera.s_height, 0.5]

                    # init arrays for clipping
                    q = [projected]
                    planes = [
                        [Vector3(0.0, 0.0, 0.0), Vector3(0.0, 1.0, 0.0)],
                        [Vector3(0.0, camera.s_height - 1, 0.0), Vector3(0.0, -1.0, 0.0)],
                        [Vector3(0.0, 0.0, 0.0), Vector3(1.0, 0.0, 0.0)],
                        [Vector3(camera.s_width - 1, 0.0, 0.0), Vector3(-1.0, 0.0, 0.0)]
                    ]
                    # clip against sides of screen
                    for plane in planes:
                        new_q = []
                        for triangle in q:
                            new_q += clip_tri_by_plane(plane[0], plane[1], triangle,
                                                       debug=(camera.debug or camera.clip_debug))
                        q = new_q

                    # loop for every new triangle
                    for final_tri in q:
                        # create shadows
                        center = (tri.vertices[0] + tri.vertices[1] + tri.vertices[2]) / 3.0
                        final_int = Vector3(0, 0, 0)
                        for light in lights:
                            intensity = 0.5
                            if type(lights[light]) == Point_Light:
                                light_dist = (center - lights[light].pos).length()
                                intensity = min(1.0, max(0.01, 1 / (light_dist ** 2) * lights[light].intensity))
                                intensity *= normal.normalise().dot((center - lights[light].pos).normalise())
                                intensity = max(-1.0, min(intensity, 0.1))
                            elif type(lights[light]) == Directional_Light:
                                intensity = max(0.1, lights[light].dir.dot(normal))
                            final_int += (lights[light].color / (255)) * intensity

                        final_int.x = min(-0.1, max(final_int.x, -1.0))
                        final_int.y = min(-0.1, max(final_int.y, -1.0))
                        final_int.z = min(-0.1, max(final_int.z, -1.0))

                        col = (abs(final_tri.col[0] * final_int.x), abs(final_tri.col[1] * final_int.y),
                               abs(final_tri.col[2] * final_int.z))

                        # save color to triangle
                        final_tri.temp_col = col
                        to_render.append(final_tri)

        return to_render