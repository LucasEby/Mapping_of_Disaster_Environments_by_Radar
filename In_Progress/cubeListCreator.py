# import random
import pygame
# from pygame.locals import DOUBLEBUF, OPENGL
from OpenGL.GL import glClear, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT
# from OpenGL.GLU import gluPerspective
from cube import Cube
from frameCalculator import FrameCalculator


class CubeListCreator:

    def __init__(self) -> None:
        self.__fc_obj = FrameCalculator()
        self.__horizontal_rotation = 0
        self.__vertical_rotation = 0
        self.__all_real_points = False
        self.__index_pos = 0
        self.__list_length = 10000
        self.__cube_list = []
        # Place fake objects in list:
        for each in range(self.__list_length):
            self.__cube_list.append(Cube(-1, -1, -1, 0))

    def add_new_cube(self, cube_obj) -> None:
        if self.__index_pos >= (self.__list_length - 1):
            self.__index_pos = 0
            self.__all_real_points = True
        temp_obj = self.__cube_list.pop(self.__index_pos)
        del temp_obj
        self.__cube_list.insert(self.__index_pos, cube_obj)
        self.__index_pos = self.__index_pos + 1
        # Rotate the cube so it is located in the correct position (with respect to the other rotated cubes):
        self.rotate_vertically(self.__vertical_rotation)
        self.rotate_horizontally(self.__horizontal_rotation)


    def plotCubes(self) -> None:
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        if self.__all_real_points:
            for each_cube in self.__cube_list:
                each_cube.drawCube(each_cube.set_vertices())
        else:
            for index in range(self.__index_pos):
                self.__cube_list[index].drawCube(self.__cube_list[index].set_vertices())
        pygame.display.flip()  # .update() doesn't work here for some reason

    def size(self) -> int:
        if self.__all_real_points:
            return len(self.__cube_list)
        else:
            return self.__index_pos

    def rotate_horizontally(self, angle):
        self.__horizontal_rotation = self.__horizontal_rotation + angle
        if self.__all_real_points:
            for each_cube in self.__cube_list:
                temp = self.__fc_obj.horizontal_rotation(each_cube.x, each_cube.y, each_cube.z, angle=angle)
                each_cube.x = temp[0]
                each_cube.y = temp[1]
                each_cube.z = temp[2]
        else:
            for index in range(self.__index_pos):
                temp = self.__fc_obj.horizontal_rotation(self.__cube_list[index].x, self.__cube_list[index].y,
                                                         self.__cube_list[index].z, angle=angle)
                self.__cube_list[index].x = temp[0]
                self.__cube_list[index].y = temp[1]
                self.__cube_list[index].z = temp[2]

    def rotate_vertically(self, angle):
        self.__vertical_rotation = self.__vertical_rotation + angle
        if self.__all_real_points:
            for each_cube in self.__cube_list:
                temp = self.__fc_obj.vertical_rotation(each_cube.x, each_cube.y, -each_cube.z, angle=angle)
                each_cube.x = temp[0]
                each_cube.y = temp[1]
                each_cube.z = -temp[2]
        else:
            for index in range(self.__index_pos):
                temp = self.__fc_obj.vertical_rotation(self.__cube_list[index].x, self.__cube_list[index].y,
                                                       -self.__cube_list[index].z, angle=angle)
                self.__cube_list[index].x = temp[0]
                self.__cube_list[index].y = temp[1]
                self.__cube_list[index].z = -temp[2]


# pygame.init()
# display = (800, 600)
# pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
#
# gluPerspective(45, (display[0]/display[1]), 0.1, 100.0)
# obj = CubeListCreator()
# lastPosition = 0
# for each in range(10):
#     # each = Cube(random.randint(0, 5), random.randint(0, 5), random.randint(0, 5))
#     obj.add_new_cube(Cube(random.randint(-50, 50), random.randint(-50, 50), random.randint(-70, -50)))
# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             quit()
#     obj.add_new_cube(Cube(random.randint(-50, 50), random.randint(-50, 50), random.randint(-70, -50)))
#     obj.plotCubes()
#     pygame.time.wait(100)

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


