import random

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from cube import Cube


class CubeListCreator:

    def __init__(self):
        self.__cube_list = []

    def appendToList(self, cube_obj):
        self.__cube_list.append(cube_obj)

    def insertInList(self, position, cube_obj):
        temp = position
        # tempSize = len(self.__cube_list)
        tempSize = self.size()
        if tempSize > position:
            temp_obj = self.__cube_list.pop(position)
            del temp_obj
            self.__cube_list.insert(temp, cube_obj)

    def plotCubes(self):
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        for each_cube in self.__cube_list:
            each_cube.drawCube(each_cube.set_vertices())
        pygame.display.flip()  # .update() doesn't work here for some reason

    def size(self):
        # print(len(self.__cube_list))
        return len(self.__cube_list)


pygame.init()
display = (800, 600)
pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

gluPerspective(45, (display[0]/display[1]), 0.1, 100.0)
obj = CubeListCreator()
lastPosition = 0
for each in range(10):
    # each = Cube(random.randint(0, 5), random.randint(0, 5), random.randint(0, 5))
    obj.appendToList(Cube(random.randint(0, 10), random.randint(0, 10), random.randint(-70, -50)))
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    if obj.size() <= 10:
        obj.appendToList(Cube(random.randint(0, 10), random.randint(0, 10), random.randint(-70, -50)))
    else:
        if lastPosition >= 11:
            lastPosition = 0
        obj.insertInList(lastPosition, Cube(random.randint(0, 10), random.randint(0, 10), random.randint(-70, -50)))
        lastPosition = lastPosition + 1
        #print(obj.size)
    obj.plotCubes()
    pygame.time.wait(100)

# cube_dict = {}
# q = 0
# for x in range(20):
#     cube_dict[x] = Cube().set_vertices(1 + q, 2 + q, -50 + q)
#     q = q + 3

# class Cube:
#     def __init__(
#             self, x_translation, y_translation, z_translation):
#         """
#         Stores the data for each of the cube points.
#         """
#         self.x_translation = x_translation
#         self.y_translation = y_translation
#         self.z_translation = z_translation


# vertices = (
#     (1, -1, -1), #1, -2, -1 messes it up
#     (1, 1, -1),
#     (-1, 1, -1),
#     (-1, -1, -1),
#     (1, -1, 1),
#     (1, 1, 1),
#     (-1, -1, 1),
#     (-1, 1, 1)
#     )

# edges = (
#     (0, 1),
#     (0, 3),
#     (0, 4),
#     (2, 1),
#     (2, 3),
#     (2, 7),
#     (6, 3),
#     (6, 4),
#     (6, 7),
#     (5, 1),
#     (5, 4),
#     (5, 7)
#     )
#
# surfaces = (
#     (0, 1, 2, 3),
#     (3, 2, 7, 6),
#     (6, 7, 5, 4),
#     (4, 5, 1, 0),
#     (1, 5, 7, 2),
#     (4, 0, 3, 6)
#     )
#
# colors = (
#     (1, 0, 0),
#     (0, 1, 0),
#     (0, 0, 1),
#     (0, 1, 0),
#     (1, 1, 1),
#     (0, 1, 1),
#     (1, 0, 0),
#     (0, 1, 0),
#     (0, 0, 1),
#     (1, 0, 0),
#     (1, 1, 1),
#     (0, 1, 1)
#     )


# def set_vertices(x, y, z):
#     # x_value_change = random.randrange(-10, 10)
#     # y_value_change = -1 # random.randrange(-10, 10)
#     # z_value_change = random.randrange(-max_distance, -20)
#
#     new_vertices = []
#
#     for vert in vertices:
#         new_vert = []
#
#         new_x = vert[0] + x
#         new_y = vert[1] + y
#         new_z = vert[2] + z
#
#         new_vert.append(new_x)
#         new_vert.append(new_y)
#         new_vert.append(new_z)
#
#         new_vertices.append(new_vert)
#     return new_vertices

# def drawCube(new_vertices):
#     glBegin(GL_QUADS)
#     # glColor3fv((0, 1, 0)) #sets constant color for block
#     for surface in surfaces:
#         x = 0
#         # green:
#         # glColor3fv((0, 1, 0)) #sets surface color
#         for vertex in surface:
#             x += 1
#             glColor3fv(colors[x])
#             # glColor3fv((0, 1, 0)) #sets vertex color
#             glVertex(new_vertices[vertex])
#
#     glEnd()


