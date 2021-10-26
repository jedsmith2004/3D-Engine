from vector import Vector3
import pygame

class Triangle:
    def __init__(self,v1=None,v2=None,v3=None):
        self.vertices = [Vector3(v1[0],v1[1],v1[2]),Vector3(v2[0],v2[1],v2[2]),Vector3(v3[0],v3[1],v3[2])]

    def draw_triangle(self, window):
        pygame.draw.line(window, (255, 255, 255), (self.vertices[0].x, self.vertices[0].y),
                         (self.vertices[1].x, self.vertices[1].y))
        pygame.draw.line(window, (255, 255, 255), (self.vertices[1].x, self.vertices[1].y),
                         (self.vertices[2].x, self.vertices[2].y))
        pygame.draw.line(window, (255, 255, 255), (self.vertices[2].x, self.vertices[2].y),
                         (self.vertices[0].x, self.vertices[0].y))

    def fill_triangle(self, window, col):
        pygame.draw.polygon(window,col,((self.vertices[0].x,self.vertices[0].y),
                                        (self.vertices[1].x,self.vertices[1].y),
                                        (self.vertices[2].x,self.vertices[2].y)))