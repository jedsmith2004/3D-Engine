from matrix import Matrix
from vector import Vector3
from triangle import Triangle
import math as m


indentity = [[1,0,0],
             [0,1,0],
             [0,0,1]]

class Mesh:
    def __init__(self):
        self.triangles = []
        self.color = (255,128,75)
        self.pos = 0,0
        self.transform = indentity
        self.translate = indentity
        self.scale = 1
        self.pitch = 0
        self.yaw = 0
        self.roll = 0

    def load_from_obj(self, path):
        with open(path,'r') as f:
            verts = []
            lines = f.readlines()
            for line in lines:
                if line[0] == "v":
                    v = line.split(" ")
                    verts.append([float(v[1]),float(v[2]),float(v[3])])
                elif line[0] == "f":
                    blocks = line.split(" ")
                    v1 = verts[int(blocks[1].split("/")[0])-1]
                    v2 = verts[int(blocks[2].split("/")[0])-1]
                    v3 = verts[int(blocks[3].split("/")[0])-1]
                    self.triangles.append(Triangle((v1[0],v1[1],v1[2]),
                                                        (v2[0],v2[1],v2[2]),
                                                        (v3[0],v3[1],v3[2])))


    def update(self,camera):
        m_rot_x = Matrix.rotation_x(self.pitch)
        m_rot_y = Matrix.rotation_y(self.yaw)
        m_rot_z = Matrix.rotation_z(self.roll)
        for tri in self.triangles:
            tri_rotated_x = m_rot_x.tri_by_4x4(tri)
            tri_rotated_xy = m_rot_y.tri_by_4x4(tri_rotated_x)
            tri_rotated_xyz = m_rot_z.tri_by_4x4(tri_rotated_xy)

            translated = tri_rotated_xyz
            translated.vertices[0].z = tri_rotated_xyz.vertices[0].z + 8
            translated.vertices[1].z = tri_rotated_xyz.vertices[1].z + 8
            translated.vertices[2].z = tri_rotated_xyz.vertices[2].z + 8

            line1 = Vector3(translated.vertices[1].x - translated.vertices[0].x,
                             translated.vertices[1].y - translated.vertices[0].y,
                             translated.vertices[1].z - translated.vertices[0].z)
            line2 = Vector3(translated.vertices[2].x - translated.vertices[0].x,
                             translated.vertices[2].y - translated.vertices[0].y,
                             translated.vertices[2].z - translated.vertices[0].z)
            normal = Vector3(line1.y * line2.z - line1.z * line2.y,
                             line1.z * line2.x - line1.x * line2.z,
                             line1.x * line2.y - line1.y * line2.x)

            length = m.sqrt(normal.x**2 + normal.y**2 + normal.z**2)
            normal /= length

            if (normal.x * (translated.vertices[0].x - camera.pos.x) +
                normal.y * (translated.vertices[0].y - camera.pos.y) +
                normal.z * (translated.vertices[0].z - camera.pos.z) < 0):

                light_dir = Vector3(0,0,-1)
                length = m.sqrt(light_dir.x**2+light_dir.y**2+light_dir.z**2)
                light_dir /= length

                dp = normal.x * light_dir.x + normal.y * light_dir.y + normal.z * light_dir.z
                col = (abs(self.color[0]*dp),abs(self.color[1]*dp),abs(self.color[2]*dp))


                projected = camera.proj_matrix.tri_by_4x4(translated)
                projected.vertices[0] += 1
                projected.vertices[1] += 1
                projected.vertices[2] += 1

                projected.vertices[0] *= [0.5 * camera.s_width, 0.5 * camera.s_height, 0]
                projected.vertices[1] *= [0.5 * camera.s_width, 0.5 * camera.s_height, 0]
                projected.vertices[2] *= [0.5 * camera.s_width, 0.5 * camera.s_height, 0]

                projected.fill_triangle(camera.window, col)