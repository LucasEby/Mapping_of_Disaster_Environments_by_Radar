import pygame
from OpenGL.GL import glClear, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT
from cube import Cube
from frameCalculator import FrameCalculator


class CubeListCreator:

    def __init__(self) -> None:
        """
        Initializes the list of cubes and other needed variables needed to work with the list.
        """
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
        """
        This function is used to add a new cube object to the list. This cube object will replace a cube object that
        is already in the list.
        :param cube_obj: the cube object that is being added to the list.
        :return: nothing
        """
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
        """

        :return: nothing
        """
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        if self.__all_real_points:
            for each_cube in self.__cube_list:
                each_cube.drawCube(each_cube.set_vertices())
        else:
            for index in range(self.__index_pos):
                self.__cube_list[index].drawCube(self.__cube_list[index].set_vertices())
        pygame.display.flip()  # .update() doesn't work here for some reason

    def size(self) -> int:
        """
        This function is used to get the number of real cubes that are in the list.
        :return: an integer that represents the number of real cubes that are in the list.
        """
        if self.__all_real_points:
            return len(self.__cube_list)
        else:
            return self.__index_pos

    def rotate_horizontally(self, angle) -> None:
        """
        This function is used to rotate the cubes horizontally in the global frame of reference.
        :param angle: The angle at which the cubes are rotated about the origin.
        :return: nothing
        """
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

    def rotate_vertically(self, angle) -> None:
        """
        This function is used to rotate the cubes vertically in the global frame of reference.
        :param angle: The angle at which the cubes are rotated about the origin.
        :return: nothing
        """
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
