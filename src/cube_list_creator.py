# Standard Library Imports
import json

# Package Imports
import pygame
from OpenGL.GL import glClear, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT, glRotatef, glPushMatrix, glPopMatrix, glTranslatef

# Self Imports
from cube import Cube
from frame_calculator import FrameCalculator

class CubeListCreator:
    """ [summary]
    """

    def __init__(self) -> None:
        """
        Initializes the list of cubes and other needed variables needed to work with the list.
        """
        self.__fc_obj = FrameCalculator()
        self.__horizontal_rotation = 0
        self.__vertical_rotation = 0
        self.__all_real_points = False
        self.__index_pos = 0
        self.__list_length = 100
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

    def plot_cubes(self, x_rotation, y_rotation, z_translation, y_translation) -> None:
        """
        This function is used to plot the cubes on the screen.
        :return: nothing
        """
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()
        glTranslatef(0, 0, z_translation)
        glRotatef(x_rotation, 1, 0, 0)
        glRotatef(y_rotation, 0, 1, 0)
        glTranslatef(0, y_translation, 0)

        if self.__all_real_points:
            for each_cube in self.__cube_list:
                each_cube.draw_cube(each_cube.set_vertices())
        else:
            for index in range(self.__index_pos):
                self.__cube_list[index].draw_cube(self.__cube_list[index].set_vertices())
        pygame.display.flip()  # .update() doesn't work here for some reason
        glPopMatrix()

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

        def load_file(self, filename) -> None:
            """
            This function is used to rotate the cubes vertically in the global frame of reference.
            :param filename: The angle at which the cubes are rotated about the origin.
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

        def save_file(self, filename) -> None:
            """
            This function is used to rotate the cubes vertically in the global frame of reference.
            :param filename: The angle at which the cubes are rotated about the origin.
            :return: nothing
            """
            send_me = []
            if self.__all_real_points:
                for each_cube in self.__cube_list:
                    temp = each_cube.get_data
                    send_me.append(temp[0] + " " + temp[1] + " " + temp[2] + " " + temp[3] + " " + temp[4] + " " + temp[5] + " " + temp[6] + " " + "\n")
            else:
                for index in range(self.__index_pos):
                    temp = self.__cube_list[index].get_data
                    send_me.append(temp[0] + " " + temp[1] + " " + temp[2] + " " + temp[3] + " " + temp[4] + " " + temp[5] + " " + temp[6] + " " + "\n")
            with open('data.json', 'w') as outfile:
                json.dump(send_me, outfile)
