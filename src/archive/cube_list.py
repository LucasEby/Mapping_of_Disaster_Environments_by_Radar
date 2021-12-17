import pygame
from OpenGL.GL import glClear, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT

class CubeListCreator:
    def __init__(self):
        self.__cube_list = []

    def appendToList(self, cube_obj):
        self.__cube_list.append(cube_obj)

    def insertInList(self, position, cube_obj):
        temp = position
        tempSize = self.size()
        if tempSize > position:
            temp_obj = self.__cube_list.pop(position)
            del temp_obj
            self.__cube_list.insert(temp, cube_obj)

    def plotCubes(self):
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        for each_cube in self.__cube_list:
            each_cube.drawCube(each_cube.set_vertices())
        pygame.display.flip()

    def size(self):
        return len(self.__cube_list)