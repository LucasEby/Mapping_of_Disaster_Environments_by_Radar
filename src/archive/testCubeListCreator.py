import keyboard
import pygame
from OpenGL.GLU import gluPerspective
from pygame.locals import DOUBLEBUF, OPENGL

from cube import Cube
from cubeListCreator import CubeListCreator
from frameCalculator import FrameCalculator

pygame.init()
display = (800, 600)
pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
gluPerspective(45, (display[0]/display[1]), 0.1, 200.0)
cubeList = CubeListCreator()
frameCalculator = FrameCalculator()
lastPosition = 0
posIncrement = 0
colorIncrement = 0
for each in range(1):
    # each = Cube(random.randint(0, 5), random.randint(0, 5), random.randint(0, 5))
    # receivedPoints
    cubeList.add_new_cube(Cube(0, 0, -100, colorIncrement, 20, 20, 20))
    colorIncrement = colorIncrement + 50
    cubeList.add_new_cube(Cube(100, 5, 0, colorIncrement, 20, 20, 20))
    colorIncrement = colorIncrement + 50
    cubeList.add_new_cube(Cube(0, 0, 100, colorIncrement, 20, 20, 20))
    colorIncrement = colorIncrement + 50
    cubeList.add_new_cube(Cube(-5, 100, 0, colorIncrement, 20, 20, 20))
    posIncrement = posIncrement + 1
    colorIncrement = colorIncrement + 50
    if colorIncrement > 1530:
        colorIncrement = 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    if keyboard.is_pressed("left"):
        cubeList.rotate_horizontally(0.1)
        cubeList.plotCubes()
    if keyboard.is_pressed("right"):
        cubeList.rotate_horizontally(-0.1)
        cubeList.plotCubes()
    if keyboard.is_pressed("up"):
        cubeList.rotate_vertically(-0.1)
        cubeList.plotCubes()
    if keyboard.is_pressed("down"):
        cubeList.rotate_vertically(0.1)
        cubeList.plotCubes()

    # cubeList.add_new_cube(Cube(random.randint(-50, 50), random.randint(-50, 50), random.randint(-70, -50)))
    cubeList.plotCubes()
    pygame.time.wait(50)
