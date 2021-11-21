from cube import Cube
from cubeListCreator import CubeListCreator
import math


class ObjectMaker:
    def __init__(self, list_creator: CubeListCreator, x: float, y: float, z: float, angle: float,
                 resolution: float) -> None:
        # Units are in meters:
        self.__round_amount = 1.0/3.0
        # Angle amount per color:
        self.__angle_per_color = 360.0/1531.0
        # Units are in meters:
        self.__list_creator = list_creator
        self.__x_min = x
        self.__x_max = x
        self.__y_min = y
        self.__y_max = y
        self.__z_min = z
        self.__z_max = z
        self.__angle_min = angle
        self.__angle_max = angle
        self.__resolution = resolution

    def __min_bounds(self, coordinate) -> float:
        print(str(coordinate - self.__round_amount - self.__resolution))
        return coordinate - self.__round_amount - self.__resolution

    def __max_bounds(self, coordinate) -> float:
        print(str(coordinate + self.__round_amount + self.__resolution))
        return coordinate + self.__round_amount + self.__resolution

    def __check_and_update_x(self, x) -> bool:
        if (x >= self.__min_bounds(self.__x_min)) and (x <= self.__max_bounds(self.__x_max)):
            if x < self.__x_min:
                self.__x_min = x
            elif x > self.__x_max:
                self.__x_max = x
            return True
        return False

    def __check_and_update_y(self, y) -> bool:
        if (y >= self.__min_bounds(self.__y_min)) and (y <= self.__max_bounds(self.__y_max)):
            if y < self.__y_min:
                self.__y_min = y
            elif y > self.__y_max:
                self.__y_max = y
            return True
        return False

    def __check_and_update_z(self, z) -> bool:
        if (z >= self.__min_bounds(self.__z_min)) and (z <= self.__max_bounds(self.__z_max)):
            if z < self.__z_min:
                self.__z_min = z
            elif z > self.__z_max:
                self.__z_max = z
            return True
        return False

    def __update_angle(self, angle) -> None:
        if (angle >= self.__angle_min) and (angle <= self.__angle_max):
            if angle < self.__angle_min:
                self.__angle_min = angle
            elif angle > self.__angle_max:
                self.__angle_max = angle

    def __calc_color(self, angle) -> int:
        colorIndex = angle / self.__angle_per_color
        colorIndex = int(math.floor(colorIndex))
        if colorIndex == 1531:
            colorIndex = 1530
        return colorIndex

    def add_new_point(self, x, y, z, horizontal_angle, is_object) -> None:
        if is_object:
            if not (self.__check_and_update_x(x) or self.__check_and_update_y(y) or self.__check_and_update_z(z)):
                # this new point is for a new object. We need to send the old object to the cubeListCreator
                # before we store this new point to check it against future points.
                # We can make this assumption because the objects that are received here are sorted by distance from
                # one another.
                half_x_length = (self.__x_max - self.__x_min) / 2
                half_y_length = (self.__y_max - self.__y_min) / 2
                half_z_length = (self.__z_max - self.__z_min) / 2
                if half_x_length == 0:
                    half_x_length = 0.5
                if half_y_length == 0:
                    half_y_length = 0.5
                if half_z_length == 0:
                    half_z_length = 0.5
                x_pos = self.__x_min + half_x_length
                y_pos = self.__y_min + half_y_length
                z_pos = self.__z_min + half_z_length
                colorIndex = self.__calc_color(((self.__angle_max - self.__angle_min) / 2) + self.__angle_min)

                print("x_pos: " + str(x_pos) + " half_x_length: " + str(half_x_length))
                print("y_pos: " + str(y_pos) + " half_y_length: " + str(half_y_length))
                print("z_pos: " + str(z_pos) + " half_z_length: " + str(half_z_length))
                self.__list_creator.add_new_cube(Cube(x_pos, y_pos, z_pos, colorIndex,
                                                      half_x_length, half_y_length, half_z_length))
                # set x, y, and z parameters to be the new object in consideration:
                self.__x_min = self.__x_max = x
                self.__y_min = self.__y_max = y
                self.__z_min = self.__z_max = z
                self.__angle_min = self.__angle_max = horizontal_angle
            else:
                self.__update_angle(horizontal_angle)
