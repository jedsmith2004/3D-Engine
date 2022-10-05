from engine.vector import Vector3
from engine.triangle import Triangle
from math import cos, sin

# custom matrix class
class Matrix:
    def __init__(self, mat):
        # self.matrix being a 2d array
        self.matrix = mat
        self.rows = len(mat)
        self.cols = len(mat[0])
        self.flag = None

    # multiply a matrix by a matrix
    def multiply_matrix(self, other):
        if self.cols != other.rows:
            raise ArithmeticError('Number of A columns must equal number of B rows.')

        result = []
        for m in range(self.rows):
            rows = []
            for i in range(other.cols):
                columns = 0
                for j in range(self.cols):
                    columns += self.matrix[m][j] * other.matrix[j][i]
                rows.append(columns)
            result.append(rows)
        return Matrix(result)

    # multiply a matrix by a 3D vector
    def matrix_by_vector(self, other):
        mat = self @ [other.x, other.y, other.z, 1]
        # print(mat)
        return Vector3(mat[0], mat[1], mat[2])

    # another matrix multiplication method specifically for tri_by_4x4
    def __matmul__(self, other):
        new_mat = []

        # print(other)

        if self.rows == 4 and type(other) == list:
            new_mat = []
            for col in range(self.cols):
                new_mat.append(other[0]*self.matrix[0][col]+other[1]*self.matrix[1][col]+other[2]*self.matrix[2][col]+other[3]*self.matrix[3][col])
            w = new_mat[3]
            if self.flag == 'projection': new_mat = Vector3(new_mat[0]/w,new_mat[1]/w,new_mat[2]/w)

        return new_mat

    # multiplies a triangle's vertices by this matrix
    def tri_by_4x4(self, tri):
        final = []
        for point in tri.vertices:
            final.append(self @ [point.x,point.y,point.z,point.w])
        return Triangle(final[0],final[1],final[2],col=tri.col)

    # provides rotation matrix around x axis
    @classmethod
    def rotation_x(cls,angle):
        return cls([
            [1, 0.0, 0.0, 0.0],
            [0.0, cos(angle), sin(angle), 0.0],
            [0.0, -sin(angle), cos(angle), 0.0],
            [0.0, 0.0, 0.0, 1]
        ])

    # provides rotation matrix around y axis
    @classmethod
    def rotation_y(cls, angle):
        return cls([
            [cos(angle), 0.0, -sin(angle), 0.0],
            [0.0, 1, 0.0, 0.0],
            [sin(angle), 0.0, cos(angle), 0.0],
            [0.0, 0.0, 0.0, 1]
        ])

    # provides rotation matrix around z axis
    @classmethod
    def rotation_z(cls, angle):
        return cls([
            [cos(angle), sin(angle), 0.0, 0.0],
            [-sin(angle), cos(angle), 0.0, 0.0],
            [0.0, 0.0, 1, 0.0],
            [0.0, 0.0, 0.0, 1]
        ])

    # provides scaling matrix
    @classmethod
    def scaling(cls, scale):
        return cls([
            [scale, 0.0, 0.0, 0.0],
            [0.0, scale, 0.0, 0.0],
            [0.0, 0.0, scale, 0.0],
            [0.0, 0.0, 0.0, 1]
        ])

    # provides translation matrix
    @classmethod
    def translate(cls, trans: Vector3):
        return cls([
            [1, 0.0, 0.0, trans.x],
            [0.0, 1, 0.0, trans.y],
            [0.0, 0.0, 1, trans.z],
            [0.0, 0.0, 0.0, 1]
        ])

    # provides projection matrix
    @classmethod
    def projection(cls, camera):
        m = cls([
            [(camera.a * camera.f), 0,        0,                         0],
            [0,                     camera.f, 0,                         0],
            [0,                     0,        camera.q,                  -1],
            [0,                     0,        -camera.z_near * camera.q, 0]
        ])
        m.flag = 'projection'
        return m

    # provides identity matrix
    @classmethod
    def identity(cls):
        return cls([[1.0, 0.0, 0.0, 0.0],
                       [0.0, 1.0, 0.0, 0.0],
                       [0.0, 0.0, 1.0, 0.0],
                       [0.0, 0.0, 0.0, 1.0]])

    # provides 'point at' matrix
    @classmethod
    def point_at(cls, pos: Vector3, target: Vector3, up: Vector3):
        # C vector of length 1
        new_forward = (target - pos).normalise()

        # B vector of length 1
        a = new_forward * up.dot(new_forward)
        new_up = (up - a).normalise()

        # A vector of length 1
        newRight = new_up.cross(new_forward)

        return cls([[newRight.x,    newRight.y,    newRight.z,    0.0],
                    [new_up.x,      new_up.y,      new_up.z,      0.0],
                    [new_forward.x, new_forward.y, new_forward.z, 0.0],
                    [pos.x,         pos.y,         pos.z,         1.0]])

    # inverses 'look at' matrix only
    def quick_inverse(self):
        # creates fresh matrix
        new = self.identity()
        new.matrix[0][0], new.matrix[0][1], new.matrix[0][2], new.matrix[0][3] = self.matrix[0][0], self.matrix[1][0], self.matrix[2][0], 0.0
        new.matrix[1][0], new.matrix[1][1], new.matrix[1][2], new.matrix[1][3] = self.matrix[0][1], self.matrix[1][1], self.matrix[2][1], 0.0
        new.matrix[2][0], new.matrix[2][1], new.matrix[2][2], new.matrix[2][3] = self.matrix[0][2], self.matrix[1][2], self.matrix[2][2], 0.0
        new.matrix[3][0] = -(self.matrix[3][0] * new.matrix[0][0] + self.matrix[3][1] * new.matrix[1][0] + self.matrix[3][2] * new.matrix[2][0])
        new.matrix[3][1] = -(self.matrix[3][0] * new.matrix[0][1] + self.matrix[3][1] * new.matrix[1][1] + self.matrix[3][2] * new.matrix[2][1])
        new.matrix[3][2] = -(self.matrix[3][0] * new.matrix[0][2] + self.matrix[3][1] * new.matrix[1][2] + self.matrix[3][2] * new.matrix[2][2])
        new.matrix[3][3] = 1

        self.matrix = new.matrix