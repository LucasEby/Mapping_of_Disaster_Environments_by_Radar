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
        self.x = x
        self.y = y
        self.z = z
        self.showMe = showMe



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

    def __init__(self, x, y, z, color, showMe):  # red, green, blue): # x, y, z, velocity, red, green, blue):
        self.x = x
        self.y = y
        self.z = z
        self.color = color
        self.showMe = showMe

    def createCube(self):
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
                glColor3fv(self.colors[4])
                glVertex3fv(self.vertices[vertex])
        glEnd()

    def plotCube(self):  # , x, y, z):
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
        self.createCube()
        pygame.display.flip()  # .update() doesn't work here for some reason
        pygame.time.wait(10)

        while self.showMe:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            glRotatef(1, 3, 1, 1)
            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
            self.createCube()
            pygame.display.flip()  # .update() doesn't work here for some reason
            pygame.time.wait(10)


colorSend = 0
Cube(random.randrange(-10, 10), random.randrange(-10, 10), random.randrange(-70, -50),
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
