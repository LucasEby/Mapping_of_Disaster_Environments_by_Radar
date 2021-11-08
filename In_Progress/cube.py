# from In_Progress.cubeListCreator import CubeListCreator
from modifying_cube_code.cubeComponents import CubeComponents
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *


class Cube:
    def __init__(self, x, y, z):  # , x_translation, y_translation, z_translation):
        """
        Stores the data for each of the cube points.
        """
        self.x = x
        self.y = y
        self.z = z
        # self.__vertices = self.set_vertices()

    def set_vertices(self):
        new_vertices = []

        for vert in CubeComponents.vertices:
            new_vert = []

            new_x = vert[0] + self.x
            new_y = vert[1] + self.y
            new_z = vert[2] + self.z

            new_vert.append(new_x)
            new_vert.append(new_y)
            new_vert.append(new_z)

            new_vertices.append(new_vert)
        return new_vertices

    # def return_vertices(self):
    #     return self.__vertices

    def drawCube(self, new_vertices):
        glBegin(GL_QUADS)
        # glColor3fv((0, 1, 0)) #sets constant color for block
        for surface in CubeComponents.surfaces:
            x = 0
            # green:
            # glColor3fv((0, 1, 0)) #sets surface color
            for vertex in surface:
                x += 1
                glColor3fv(CubeComponents.colors[x])
                # glColor3fv((0, 1, 0)) #sets vertex color
                glVertex(new_vertices[vertex])

        glEnd()

