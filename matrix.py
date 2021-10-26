from vector import Vector3
from triangle import Triangle
from math import cos, sin

class Matrix:
    def __init__(self,mat):
        self.matrix = mat
        self.rows = len(mat)
        self.cols = len(mat[0])

    def __matmul__(self, other):
        new_mat = []
        if self.rows == 4 and type(other) == list:
            new_mat = []
            for col in range(self.cols):
                new_mat.append(other[0]*self.matrix[0][col]+other[1]*self.matrix[1][col]+other[2]*self.matrix[2][col]+other[3]*self.matrix[3][col])
            w = new_mat[3]
            if w != 0: new_mat = Vector3(new_mat[0]/w,new_mat[1]/w,new_mat[2]/w)
        elif self.rows == other.cols:
            new_mat = [[0 for _ in range(other.cols)] for _ in range(self.rows)]
            for row in range(self.rows):
                for _col in range(other.cols):
                    for _row in range(other.rows):
                        new_mat[_col][row] += self.matrix[row][_row] * other.matrix[_row][_col]
            return Matrix(new_mat)
        elif self.cols == other.rows:
            new_mat = [[0 for _ in range(other.rows)] for _ in range(self.cols)]
            for row in range(self.cols):
                for _col in range(other.rows):
                    for _row in range(other.cols):
                        new_mat[_col][row] += self.matrix[row][_row] * other.matrix[_row][_col]
            return Matrix(new_mat)

        return new_mat

    def tri_by_4x4(self, tri):
        final = []
        for point in tri.vertices:
            final.append(self @ [point.x,point.y,point.z,1])
        return Triangle(final[0],final[1],final[2])

    @classmethod
    def rotation_x(cls,angle):
        return cls([
            [1, 0.0, 0.0, 0.0],
            [0.0, cos(angle), sin(angle), 0.0],
            [0.0, -sin(angle), cos(angle), 0.0],
            [0.0, 0.0, 0.0, 1]
        ])

    @classmethod
    def rotation_y(cls, angle):
        return cls([
            [cos(angle), 0.0, -sin(angle), 0.0],
            [0.0, 1, 0.0, 0.0],
            [sin(angle), 0.0, cos(angle), 0.0],
            [0.0, 0.0, 0.0, 1]
        ])

    @classmethod
    def rotation_z(cls, angle):
        return cls([
            [cos(angle), sin(angle), 0.0, 0.0],
            [-sin(angle), cos(angle), 0.0, 0.0],
            [0.0, 0.0, 1, 0.0],
            [0.0, 0.0, 0.0, 1]
        ])

    @classmethod
    def scaling(cls, scale):
        return cls([
            [scale, 0.0, 0.0, 0.0],
            [0.0, scale, 0.0, 0.0],
            [0.0, 0.0, scale, 0.0],
            [0.0, 0.0, 0.0, 1]
        ])

    @classmethod
    def translate(cls, trans: Vector3):
        return cls([
            [1, 0.0, 0.0, trans.x],
            [0.0, 1, 0.0, trans.y],
            [0.0, 0.0, 1, trans.z],
            [0.0, 0.0, 0.0, 1]
        ])