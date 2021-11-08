# Standard Library Imports
from multiprocessing import Queue
from time import sleep

# Package Imports
import pygame
from pygame.locals import DOUBLEBUF, OPENGL
from OpenGL.GLU import gluPerspective

# Self Imports
from cube import Cube
from cube_list import CubeListCreator
from control import Ports, Control
from processes import SerialProcess, ArduinoSerialProcess

def main():
    # Configuration file
    config_file_name = 'xwr68xx_profile_2021_11_06T20_15_26_698.cfg'
    
    # Setup ports and control
    ports = Ports(attach_time=20.0, attach_to_ports=False)
    control = Control(config_file_name, ports)
    sleep(0.1)

    # Setup queue and process
    queue = Queue(10)
    process = SerialProcess(queue, ports.data_port, 921600, 0.1)
    process.start()
    arduino_process = ArduinoSerialProcess("/dev/tty.usbserial-14410", 9600, 0.1)
    arduino_process.start()
    
    
    # Setup pygame and cubes
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    aspect_ratio = (display[0]/display[1])
    gluPerspective(90, aspect_ratio, 0.01, 100.0)
    obj = CubeListCreator()

    # Main loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        while not(queue.empty()):
            gotten = queue.get()
            for got in gotten:
                cube = Cube(got.x, got.z, -got.y-10)
                obj.appendToList(cube)
            del gotten
        obj.plotCubes()
        pygame.time.wait(100)

if __name__ == '__main__':
    main()