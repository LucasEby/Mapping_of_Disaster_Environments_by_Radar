# Standard Library Imports
import math

# Package Imports
import numpy as np

# Self Imports
None

class FrameCalculator:
    """ [summary]
    """

    def __init__(self):
        """
        This class is used to translate the radar data into the origin's frame.
        """
        # This variable represents the offset of the radar board in the y direction (the y direction is in reference
        # to the board's reference frame, which has the y axis pointing in the direction of the radar signal).
        self.__y_off = 0  # 31.21 / 1000.0

    def b_to_d_rotation(self, x, y, z, h_angle, v_angle) -> [float, float, float]:
        """
        This function is used to calculate the position of the cubes with respect to the origin.
        :param x: the original x position
        :param y: the original y position
        :param z: the original z position
        :param h_angle: the horizontal angle at which the radar board has been rotated
        :param v_angle: the vertical angle at which the radar board has been rotated.
        :return: the calculated float vertices as a list of length 3
        """
        # v_servo origin is 180 degrees
        # h_servo origin is 115 degrees.
        # h_angle = h_angle - 115
        # v_angle = -(v_angle - 180)

        # Previous
        # rotated_x = x * math.cos(h_angle) + math.sin(h_angle) * math.cos(v_angle) * (self.__y_off - y) \
        #     + math.sin(h_angle) * math.sin(v_angle) * z
        # rotated_y = (y - self.__y_off) * math.sin(v_angle) + z * math.cos(v_angle)
        # rotated_z = -x * math.sin(h_angle) + (self.__y_off - y) * math.cos(h_angle) * math.cos(v_angle) \
        #     + z * math.cos(h_angle) * math.sin(v_angle)
        # pos_array = [rotated_x, rotated_y, rotated_z]

        #Testing:
        rotated_x = x * math.cos(h_angle) -z * math.sin(h_angle)
        rotated_y = x * math.cos(v_angle) * math.sin(h_angle) + y * math.sin(v_angle) + z * math.cos(h_angle) * math.cos(v_angle)
        rotated_z = x * math.sin(h_angle) * math.sin(v_angle) - y * math.cos(v_angle) + z * math.cos(h_angle) * math.sin(v_angle)
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
