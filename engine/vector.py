import math

# 2d vector class
class Vector2:
    def __init__(self, x=0.0, y=0.0):
        # position of vector at init
        self.x = x
        self.y = y

    # dunder add method
    def __add__(a ,b):
        if type(b) == Vector3:
            return Vector3(a. x + b.x, a. y + b.y)
        return Vector3(a. x +b, a. y + b)

    # dunder sub method
    def __sub__(a ,b):
        if type(b) == Vector3:
            return Vector3(a. x -b.x ,a. y -b.y)
        return Vector3(a. x -b ,a. y -b)

    # dunder multiply method
    def __mul__(a ,b):
        if type(b) == Vector3:
            return Vector3(a. x *b.x ,a. y *b.y)
        return Vector3(a. x *b ,a. y *b)

    # dunder divide method
    def __truediv__(a ,b):
        if type(b) == Vector3:
            return Vector3(a. x /b.x ,a. y /b.y)
        return Vector3(a. x /b ,a. y /b)

    # for requesting a tuple of the vector
    def get_tuple(self):
        return (self.x ,self.y)

    # unambiguous debug of object instance
    def __repr__(self):
        return "Instance of Vector2. Address: " +hex(id(self))

    # readable debug of object instance
    def __str__(self):
        return f"Vector2({self.x}, {self.y})"

    # when object is indexed
    def __getitem__(self, index):
        if index == 0: return self.x
        elif index == 1: return self.y
        else: raise IndexError

    # returns dot project of two vectors
    def dot(self ,b):
        return sum((self * b).get_tuple())

    # returns cross project of two vectors
    def cross(self ,b):
        if type(b) == Vector2: return ((self.x*b.y)-(self.y*b.x))
        elif type(b) == list or type(b) == tuple:
            if len(b) == 2: return ((self.x*b[1])-(self.y*b[0]))

# 3d vector class
class Vector3:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        # position of vector at init
        self.x = x
        self.y = y
        self.z = z
        self.w = 1.0

    # dunder add method
    def __add__(a ,b):
        if type(b) == Vector3:
            return Vector3(a. x +b.x ,a. y +b.y ,a. z +b.z)
        return Vector3(a.x +b ,a.y +b ,a.z +b)

    # dunder sub method
    def __sub__(a ,b):
        if type(b) == Vector3:
            return Vector3(a. x -b.x ,a. y -b.y ,a. z -b.z)
        return Vector3(a.x -b ,a.y -b ,a.z -b)

    # dunder multiply method
    def __mul__(a ,b):
        if type(b) == Vector3:
            return Vector3(a. x *b.x ,a. y *b.y ,a. z *b.z)
        if type(b) in (int, float):
            return Vector3(a.x *b ,a.y *b ,a.z *b)
        if len(b) == 3:
            return Vector3(a.x * b[0], a.y * b[1], a.z * b[2])
        return Vector3(a.x *b ,a.y *b ,a.z *b)

    # dunder divide method
    def __truediv__(a ,b):
        if type(b) == Vector3:
            return Vector3(a. x /b.x ,a. y /b.y ,a. z /b.z)
        return Vector3(a. x /b ,a. y /b ,a. z /b)

    # for requesting a tuple of the vector
    def get_tuple(self):
        return (self.x ,self.y ,self.z)

    # for converting the x and y components of a 3d vector to a 2d vector
    def to_Vector2(self):
        return Vector2(self.x,self.y)

    # unambiguous debug of object instance
    def __repr__(self):
        return "Instance of Vector3. Address: " +hex(id(self))

    # readable debug of object instance
    def __str__(self):
        return f"Vector3({self.x}, {self.y}, {self.z})"

    # when object is indexed
    def __getitem__(self, index):
        if index == 0: return self.x
        elif index == 1: return self.y
        elif index == 2: return self.z
        elif index == 3: return self.z
        else: raise IndexError

    # returns dot project of two vectors
    def dot(self ,b):
        return sum(x*y for x, y in zip(self.get_tuple(), b.get_tuple()))

    # returns length of vector - used in normalise
    def length(self):
        # return math.sqrt(self.dot(self))
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    # returns vector with mag 1
    def normalise(self):
        l = self.length()
        return Vector3(self.x / l, self.y / l, self.z / l)

    # returns cross project of two vectors
    def cross(self ,b):
        if type(b) == Vector3:
            return Vector3(((self.y * b.z) - (self.z * b.y)), (self.z*b.x)-(self.x*b.z), (self.x*b.y)-(self.y*b.x))
        elif type(b) == list or type(b) == tuple:
            if len(b) == 3:
                return Vector3(((self.y * b[2]) - (self.z * b[1])), (self.z*b[0])-(self.x*b[2]), (self.x*b[1])-(self.y*b[0]))