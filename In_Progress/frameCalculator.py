import math
import numpy as np


class FrameCalculator:
    def __init__(self):
        """
        Stores the data for each of the cube points.
        """
        self.__y_off = 1

    def b_to_d_rotation(self, x, y, z, h_angle, v_angle) -> [float, float, float]:
        # v_servo origin is 180 degrees
        # h_servo origin is 115 degrees.
        h_angle = h_angle - 115
        v_angle = -(v_angle - 180)

        rotated_x = x * math.cos(h_angle) + math.sin(h_angle) * math.cos(v_angle) * (self.__y_off - y) \
                    + math.sin(h_angle) * math.sin(v_angle) * z
        rotated_y = (y - self.__y_off) * math.sin(v_angle) + z * math.cos(v_angle)
        rotated_z = -x * math.sin(h_angle) + (self.__y_off - y) * math.cos(h_angle) * math.cos(v_angle) \
                    + z * math.cos(h_angle) * math.sin(v_angle)
        pos_array = [rotated_x, rotated_y, rotated_z]
        return pos_array

    def horizontal_rotation(self, x, y, z, angle) -> [float, float, float]:
        """
        A positive angle rotates the position to the window's left. A negative angle rotates the position to the
        window's right.

        :param x: the current x position
        :param y: the current y position
        :param z: the current z position
        :param angle: the angle the user wishes to rotate the cubes
        :return: a 3x1 array of floats
        """
        r_y = np.array([[math.cos(angle), 0, math.sin(angle)], [0, 1, 0], [-math.sin(angle), 0, math.cos(angle)]])
        current_pos = np.array([x, y, z])
        new_pos = np.dot(r_y, current_pos)
        return new_pos

    def vertical_rotation(self, x, y, z, angle) -> [float, float, float]:
        """
        A positive angle rotates the position to the window's up. A negative angle rotates the position to the
        window's down.

        :param x: the current x position
        :param y: the current y position
        :param z: the current z position
        :param angle: the angle the user wishes to rotate the cubes
        :return: a 3x1 array of floats
        """
        r_x = np.array([[1, 0, 0], [0, math.cos(angle), -math.sin(angle)], [0, math.sin(angle), math.cos(angle)]])
        current_pos = np.array([x, y, z])
        new_pos = np.dot(r_x, current_pos)
        return new_pos
