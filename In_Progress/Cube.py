import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random

vertices = (
        (1, -1, -1),
        (1, 1, -1),
        (-1, 1, -1),
        (-1, -1, -1),
        (1, -1, 1),
        (1, 1, 1),
        (-1, -1, 1),
        (-1, 1, 1)
        )

class CubeDictionary:

    def __init__(self, vertices):  # red, green, blue): # x, y, z, velocity, red, green, blue):
        """
        Initializes the CubeDictionary class.
        """
        self.x = x
        self.y = y
        self.z = z
        self.show_me = show_me


class Cube:

    vertices = (
        (1, -1, -1),
        (1, 1, -1),
        (-1, 1, -1),
        (-1, -1, -1),
        (1, -1, 1),
        (1, 1, 1),
        (-1, -1, 1),
        (-1, 1, 1)
        )

    edges = (
        (0, 1),
        (0, 3),
        (0, 4),
        (2, 1),
        (2, 3),
        (2, 7),
        (6, 3),
        (6, 4),
        (6, 7),
        (5, 1),
        (5, 4),
        (5, 7)
        )

    surfaces = (
        (0, 1, 2, 3),
        (3, 2, 7, 6),
        (6, 7, 5, 4),
        (4, 5, 1, 0),
        (1, 5, 7, 2),
        (4, 0, 3, 6)
    )

    colors = (
        (1, 0, 0),
        (0, 1, 0),
        (0, 0, 1),
        (0, 1, 0),
        (1, 1, 1),
        (0, 1, 1),
        (1, 0, 0),
        (0, 1, 0),
        (0, 0, 1),
        (1, 0, 0),
        (1, 1, 1),
        (0, 1, 1)
    )

    def __init__(
            self, x, y, z, color, show_me):  # red, green, blue): # x, y, z, velocity, red, green, blue):
        """
        Initializes the Cube class.
        """
        self.x = x
        self.y = y
        self.z = z
        self.color = color
        self.show_me = show_me

    def create_cube(self):
        """
        Creates the cubes that will be later plotted.

        This method will be used to plot each cube if the cubes
        are plotted in sequence as opposed to all at once.
        """
        glBegin(GL_QUADS)
        # glColor3fv((0, 1, 0)) # sets constant color for block
        for surface in self.surfaces:
            # x = 0
            # green:
            if self.color > 10:
                self.color = 0
            glColor3fv(self.colors[self.color])  # sets surface color
            # self.color += 1
            for vertex in surface:
                # x += 1
                # glColor3fv(self.colors[x])
                # glColor3fv((0, 1, 0)) #sets vertex color
                glVertex(self.vertices[vertex])
        glEnd()
        glBegin(GL_LINES)
        for edge in self.edges:
            for vertex in edge:
                # x = (0, 0, 0)
                # glColor3fv(x) #self.colors[4])
                glColor3fv(self.colors[4])
                glVertex3fv(self.vertices[vertex])
        glEnd()

    def plotCube(self):  # , x, y, z):
        """
        Plots a single cube.

        This method will be used if the cubes can be plotted
        in sequence as opposed to all at once.
        """
        pygame.init()
        display = (800, 600)
        pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

        gluPerspective(45, (display[0]/display[1]), 0.1, 100)

        glTranslatef(self.x, self.y, self.z)

        glRotate(0, 0, 0, 0)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        glRotatef(1, 3, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        self.create_cube()
        pygame.display.flip()  # .update() doesn't work here for some reason
        pygame.time.wait(10)

        while self.show_me:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            glRotatef(1, 3, 1, 1)
            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
            self.create_cube()
            pygame.display.flip()  # .update() doesn't work here for some reason
            pygame.time.wait(10)

    def create_cube_map(self):
        """
        Creates and returns a map of cubes

        This cube_map will be sent to the view so all of
        the cubes are plotted at the same time.
        """
        print("socks")


colorSend = 0
Cube(random.randrange(-10, 10), random.randrange(-10, 10), random.randrange(-50, -30),
                               colorSend, True).plotCube()
# for each in range(20):
#     if colorSend > 10:
#         colorSend = 0
#         Cube(random.randrange(-10, 10), random.randrange(-10, 10), random.randrange(-70, -50),
#                                colorSend, True).plotCube()
#     else:
#         colorSend += 1
#         Cube(random.randrange(-10, 10), random.randrange(-10, 10), random.randrange(-70, -50),
#                                colorSend, True).plotCube()
# tryMe = Cube(random.randrange(-10, 10), random.randrange(-10, 10), random.randrange(-70, -50), 2, True)
# tryMe.plotCube()
pygame.time.wait(1500)
# tryMe.ShowMe = False
pygame.quit()
quit()
