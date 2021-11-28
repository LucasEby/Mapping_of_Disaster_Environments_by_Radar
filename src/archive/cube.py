from cubeComponents import CubeComponents
from OpenGL.GL import glBegin, GL_QUADS, glColor, glColor3fv, glVertex, glEnd, GL_LINES, glVertex3fv


class Cube:
    def __init__(self, x, y, z, color, half_x_length=0.5, half_y_length=0.5, half_z_length=0.5):
        """
        Stores the data for each of the cube points. These cubes, depending on the parameters passed, can technically
        be rectangles.
        """
        self.x = x
        self.y = y
        self.z = z
        self.half_x_length = half_x_length
        self.half_y_length = half_y_length
        self.half_z_length = half_z_length
        self.color = color
        self.vertices = (
            (self.half_x_length, -self.half_y_length, -self.half_z_length),
            (self.half_x_length, self.half_y_length, -self.half_z_length),
            (-self.half_x_length, self.half_y_length, -self.half_z_length),
            (-self.half_x_length, -self.half_y_length, -self.half_z_length),
            (self.half_x_length, -self.half_y_length, self.half_z_length),
            (self.half_x_length, self.half_y_length, self.half_z_length),
            (-self.half_x_length, -self.half_y_length, self.half_z_length),
            (-self.half_x_length, self.half_y_length, self.half_z_length)
        )

    def set_vertices(self) -> [float, float, float]:
        """
        This function calculates the vertices of the cube based on the cube's x, y, and z data.
        :return: the calculated float vertices as a list of length 3
        """
        new_vertices = []
        self.__set_vertices()
        for vert in self.vertices:
            new_vert = []
            new_x = vert[0] + self.x
            new_y = vert[1] + self.y
            new_z = vert[2] + self.z

            new_vert.append(new_x)
            new_vert.append(new_y)
            new_vert.append(new_z)

            new_vertices.append(new_vert)
        return new_vertices

    def set_half_lengths(self, half_x_length: float, half_y_length: float, half_z_length: float) -> None:
        """
        This function is used to set the half lengths of the x, y, and z axis of the cube. The half lengths are the
        value of 1/2 of the length of the cube in the specified direction. These values are used to calculate the
        center of the cube.
        :param half_x_length: float for half of the length of the cube in the x direction
        :param half_y_length: float for half of the length of the cube in the y direction
        :param half_z_length: float for half of the length of the cube in the z direction
        :return: nothing
        """
        self.half_x_length = half_x_length
        self.half_y_length = half_y_length
        self.half_z_length = half_z_length
        self.__set_vertices()

    def __set_vertices(self) -> None:
        """
        This function is used to update the cube's vertices with the set half length values.
        :return: nothing
        """
        self.vertices = (
            (self.half_x_length, -self.half_y_length, -self.half_z_length),
            (self.half_x_length, self.half_y_length, -self.half_z_length),
            (-self.half_x_length, self.half_y_length, -self.half_z_length),
            (-self.half_x_length, -self.half_y_length, -self.half_z_length),
            (self.half_x_length, -self.half_y_length, self.half_z_length),
            (self.half_x_length, self.half_y_length, self.half_z_length),
            (-self.half_x_length, -self.half_y_length, self.half_z_length),
            (-self.half_x_length, self.half_y_length, self.half_z_length)
        )

    def drawCube(self, new_vertices) -> None:
        """
        This class is used to plot the cube in its correct position and color.
        :param new_vertices: the positions of the vertices that are being plotted.
        :return: nothing
        """
        glBegin(GL_QUADS)
        glColor3fv(CubeComponents.colors[self.color])
        for surface in CubeComponents.surfaces:
            for vertex in surface:
                glVertex(new_vertices[vertex])
        glEnd()

        glBegin(GL_LINES)
        glColor3fv((1, 1, 1))
        for edge in CubeComponents.edges:
            for vertex in edge:
                glVertex3fv(new_vertices[vertex])
        glEnd()
        #load identitty matrix
        # gl load identity

    def get_data(self) -> [float, float, float, float, float, float, float]:
        """
        Used to get the data of the cube.
        :return: the cube data as a list.
        """
        return [self.x, self.y, self.z, self.color, self.half_x_length, self.half_y_length, self.half_z_length]
