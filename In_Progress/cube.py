# from In_Progress.cubeListCreator import CubeListCreator
# from modifying_cube_code.cubeComponents import CubeComponents
from cubeComponents import CubeComponents
from OpenGL.GL import glBegin, GL_QUADS, glColor, glColor3fv, glVertex, glEnd, GL_LINES, glVertex3fv


class Cube:
    def __init__(self, x, y, z, color, half_x_length=0.5, half_y_length=0.5, half_z_length=0.5):
        """
        Stores the data for each of the cube points.
        """
        self.x = x
        self.y = y
        self.z = z
        self._half_x_length = half_x_length
        self._half_y_length = half_y_length
        self._half_z_length = half_z_length
        self._color = color
        self.vertices = (
            (self._half_x_length, -self._half_y_length, -self._half_z_length),
            (self._half_x_length, self._half_y_length, -self._half_z_length),
            (-self._half_x_length, self._half_y_length, -self._half_z_length),
            (-self._half_x_length, -self._half_y_length, -self._half_z_length),
            (self._half_x_length, -self._half_y_length, self._half_z_length),
            (self._half_x_length, self._half_y_length, self._half_z_length),
            (-self._half_x_length, -self._half_y_length, self._half_z_length),
            (-self._half_x_length, self._half_y_length, self._half_z_length)
        )

        # self.__vertices = self.set_vertices()

    def set_vertices(self):
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

    def set_half_lengths(self, half_x_length: float, half_y_length: float, half_z_length: float):
        self._half_x_length = half_x_length
        self._half_y_length = half_y_length
        self._half_z_length = half_z_length
        self.__set_vertices()

    def __set_vertices(self):
        self.vertices = (
            (self._half_x_length, -self._half_y_length, -self._half_z_length),
            (self._half_x_length, self._half_y_length, -self._half_z_length),
            (-self._half_x_length, self._half_y_length, -self._half_z_length),
            (-self._half_x_length, -self._half_y_length, -self._half_z_length),
            (self._half_x_length, -self._half_y_length, self._half_z_length),
            (self._half_x_length, self._half_y_length, self._half_z_length),
            (-self._half_x_length, -self._half_y_length, self._half_z_length),
            (-self._half_x_length, self._half_y_length, self._half_z_length)
        )

    def drawCube(self, new_vertices):
        glBegin(GL_QUADS)
        # glColor3fv((0, 1, 0)) #sets constant color for block
        for surface in CubeComponents.surfaces:
            # x = 0
            glColor3fv(CubeComponents.colors[self._color])  # sets surface color
            # glColor(1.0, 0.9, 0.8)
            for vertex in surface:
                # x += 1
                # glColor3fv(CubeComponents.colors[x])
                # glColor3fv((0, 1, 0)) #sets vertex color
                glVertex(new_vertices[vertex])

        glEnd()

        glBegin(GL_LINES)
        glColor3fv((1, 1, 1))
        for edge in CubeComponents.edges:
            for vertex in edge:
                glVertex3fv(new_vertices[vertex])
        glEnd()
