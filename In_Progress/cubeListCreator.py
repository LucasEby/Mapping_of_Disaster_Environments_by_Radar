import random

import pygame
from pygame.locals import DOUBLEBUF, OPENGL
from OpenGL.GL import glClear, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT
from OpenGL.GLU import gluPerspective
from In_Progress.cube import Cube


class CubeListCreator:

    def __init__(self) -> None:
        self.__all_real_points = False
        self.__index_pos = 0
        self.__list_length = 10000
        self.__cube_list = []
        # Place fake objects in list:
        for each in range(self.__list_length):
            self.__cube_list.append(Cube(-1, -1, -1))

    def add_new_cube(self, cube_obj) -> None:
        if self.__index_pos >= (self.__list_length - 1):
            self.__index_pos = 0
            self.__all_real_points = True
        temp_obj = self.__cube_list.pop(self.__index_pos)
        del temp_obj
        self.__cube_list.insert(self.__index_pos, cube_obj)
        self.__index_pos = self.__index_pos + 1

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


pygame.init()
display = (800, 600)
pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

gluPerspective(45, (display[0]/display[1]), 0.1, 100.0)
obj = CubeListCreator()
lastPosition = 0
for each in range(10):
    # each = Cube(random.randint(0, 5), random.randint(0, 5), random.randint(0, 5))
    obj.add_new_cube(Cube(random.randint(-50, 50), random.randint(-50, 50), random.randint(-70, -50)))
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    obj.add_new_cube(Cube(random.randint(-50, 50), random.randint(-50, 50), random.randint(-70, -50)))
    obj.plotCubes()
    pygame.time.wait(100)
