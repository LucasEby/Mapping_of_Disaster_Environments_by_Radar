import math
import numpy as np


class FrameCalculator:
    def __init__(self):
        """
        Stores the data for each of the cube points.
        """
        self.__y_off = 2

    def b_to_d_rotation(self, x_recv, y_recv, z_recv, h_servo, v_servo) -> [float, float, float]:
        rotated_x = x_recv * math.cos(h_servo) + math.sin(h_servo) * math.cos(v_servo) * (self.__y_off - y_recv) \
                    + math.sin(h_servo) * math.sin(v_servo) * z_recv
        rotated_y = (y_recv - self.__y_off) * math.sin(v_servo) + z_recv * math.cos(v_servo)
        rotated_z = -x_recv * math.sin(h_servo) + (self.__y_off - y_recv) * math.cos(h_servo) * math.cos(v_servo) \
                    + z_recv * math.cos(h_servo) * math.sin(v_servo)
        pos_array = [rotated_x, rotated_y, rotated_z]
        return pos_array

    def horizontal_rotation(self, x_pos, y_pos, z_pos, angle) -> [float, float, float]:
        """
        A positive angle rotates the position to the window's left. A negative angle rotates the position to the
        window's right.

        :param x_pos: the current x position
        :param y_pos: the current y position
        :param z_pos: the current z position
        :return: a 3x1 array of floats
        """
        r_y = np.array([[math.cos(angle), 0, math.sin(angle)], [0, 1, 0], [-math.sin(angle), 0, math.cos(angle)]])
        current_pos = np.array([x_pos, y_pos, z_pos])
        new_pos = np.dot(r_y, current_pos)
        return new_pos

    def vertical_rotation(self, x_pos, y_pos, z_pos, angle) -> [float, float, float]:
        """
        A positive angle rotates the position to the window's up. A negative angle rotates the position to the
        window's down.

        :param x_pos: the current x position
        :param y_pos: the current y position
        :param z_pos: the current z position
        :return: a 3x1 array of floats
        """
        r_x = np.array([[1, 0, 0], [0, math.cos(angle), -math.sin(angle)], [0, math.sin(angle), math.cos(angle)]])
        current_pos = np.array([x_pos, y_pos, z_pos])
        new_pos = np.dot(r_x, current_pos)
        return new_pos
