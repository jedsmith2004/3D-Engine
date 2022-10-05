from engine.vector import Vector3
import pygame

# triangle class
class Triangle:
    def __init__(self,v1=None,v2=None,v3=None,col=(255,255,255)):
        # defines vertices as three vectors provided
        self.vertices = [Vector3(v1[0],v1[1],v1[2]),Vector3(v2[0],v2[1],v2[2]),Vector3(v3[0],v3[1],v3[2])]
        if type(v1) == list and type(v2) == list and type(v3) == list:
            if len(v1) == 4: self.vertices[0].w = v1[3]
            if len(v2) == 4: self.vertices[1].w = v2[3]
            if len(v2) == 4: self.vertices[2].w = v2[3]
        self.col = col
        self.temp_col = col


    # draws triangle skeleton
    def draw_triangle(self, window):
        pygame.draw.line(window, (255, 255, 255), (self.vertices[0].x, self.vertices[0].y), (self.vertices[1].x, self.vertices[1].y))

        pygame.draw.line(window, (255, 255, 255), (self.vertices[1].x, self.vertices[1].y), (self.vertices[2].x, self.vertices[2].y))

        pygame.draw.line(window, (255, 255, 255), (self.vertices[2].x, self.vertices[2].y), (self.vertices[0].x, self.vertices[0].y))

    # draws triangle as polygon
    def fill_triangle(self, window, col):
        pygame.draw.polygon(window,col,((self.vertices[0].x,self.vertices[0].y),
                                        (self.vertices[1].x,self.vertices[1].y),
                                        (self.vertices[2].x,self.vertices[2].y)))