# Self Imports
from control import Ports, Control
from data import DetectedObject, DetectedObjectVoxel, MathUtils, Utils, compare_detected_object_voxels
from processes import IWR6843ReadProcess, ArduinoReadProcess
from visualize import Plot
# from page_control import PageControlProcess
from page_matplotlib import PageMatplotlib

# Standard Library Imports
from multiprocessing import Queue
from time import sleep
from typing import Tuple, List, Dict
from functools import cmp_to_key
from enum import Enum
import keyboard
from sys import exit

# Package Imports
import matplotlib.pyplot as plt
import pygame

class PlotMode(Enum):
    NONE = 0
    PLOT_2D = 1
    PLOT_3D = 2
    PLOT_CUBES = 3

class Manager:
    """Manager starts and initializes any processes and objects for controlling and communicating with the IWR6843
    """

    def __init__(self, config_file_name: str, plot: Plot, plot_mode: PlotMode, port_attach_time: float = 60.0, queue_size: int = 100, run_arduino_process: bool = False, output_file_name: str = 'output.json'):
        """__init__ Initialize the manager with initial parameters and initialize its objects

        Parameters
        ----------
        config_file_name : str
            the initial configuration file
        plot : Plot
            the Plot object to use to visualize detected objects
        plot_mode : PlotMode
            the plotting to use
        port_attach_time : float, optional
            the time to wait to attach to the IWR6843 serial ports, by default 60.0
        queue_size : int, optional
            the size of the queue from reading from the serial port, by default 100
        """
        self.config_file_name = config_file_name
        self.rotation = (0.0,0.0)
        self.port_attach_time = port_attach_time
        self.run_arduino_process = run_arduino_process
        self.output_file_name = output_file_name
        self.voxels_dict: Dict[DetectedObject, DetectedObject] = {}
        self.plot = plot
        self.plot_mode = plot_mode
        self.ports = None
        self.control = None
        self.objects_queue = Queue(queue_size)
        self.iwr6843_process = None
        if self.run_arduino_process:
            self.input_angles_queue = Queue(1)  # TODO: my edits
            self.angles_queue = Queue(1)
            self.arduino_process = None
            # self.page_control: PageControlProcess = PageControlProcess(self.input_angles_queue)
            self.input_page: PageMatplotlib = PageMatplotlib(self.input_angles_queue)
        self.reset()
        self.x_rotation = 0
        self.y_rotation = 0
        self.z_translation = 0
        self.y_translation = 0

    def reset(self) -> None:
        """reset resets the manager, and restarts any processes, port finders, or controllers
        """
        self.yeet(yeet_queue=False)
        self.ports = Ports(attach_time=self.port_attach_time, attach_to_ports=False, find_arduino=self.run_arduino_process)
        self.iwr6843_process = IWR6843ReadProcess(self.objects_queue, self.ports.data_port, 921600, 0.1)
        if self.run_arduino_process:
            self.arduino_process = ArduinoReadProcess(self.input_angles_queue, self.angles_queue, self.ports.arduino_port, 9600, 1)
        self.control = Control(self.config_file_name, self.ports)
        sleep(0.1)
        self.iwr6843_process.start()
        if self.run_arduino_process:
            self.arduino_process.start()
            # self.page_control.run()
            self.input_page.start()

    def get_servo_angle(self) -> Tuple[int,int]:
        """get_servo_angle get the angle of the servo

        Returns
        -------
        Tuple[int,int]
            the horizontal and vertical angle
        """
        if self.run_arduino_process:
            if not(self.angles_queue.empty()):
                hv = self.angles_queue.get()
                hv_new = (MathUtils.radians_to_degrees(hv[0]), MathUtils.radians_to_degrees(hv[1]))
                return hv_new
        return None

    def detected_objects_are_present(self) -> bool:
        """detected_objects_are_present checks if there any queued detected objects

        Returns
        -------
        bool
            True if there are any list of detected objects queued, False if not
        """
        try:
            return not(self.objects_queue.empty())
        except AttributeError:
            return False

    def get_detected_objects(self) -> List[DetectedObject]:
        """get_detected_objects retrieve any list of detected objects from the queue of detected objects

        Returns
        -------
        List[DetectedObject]
            a list of detected objects
        """
        return self.objects_queue.get()

    def staying_alive(self) -> None:
        """staying_alive keep the child processes and controller alive.
        If one of the processes fails, the manager resets (and yeets some of itself)

        Ah, ha, ha, ha, stayin' alive, stayin' alive
        Ah, ha, ha, ha, stayin' alive
        Life goin' nowhere, somebody help me
        Somebody help me, yeah
        Life goin' nowhere, somebody help me, yeah
        I'm stayin' alive
        """
        try:
            if self.run_arduino_process:
                if not(self.iwr6843_process.is_alive()) or not(self.arduino_process.is_alive()):
                    self.reset()
            else:
                if not(self.iwr6843_process.is_alive()):
                    self.reset()
        except AttributeError:
            self.reset()

    def yeet(self, yeet_queue: bool = True, from_sigquit: bool = False) -> None:
        """yeet yeets (kills) any child processes and yeets (deletes) any data

        Parameters
        ----------
        yeet_queue : bool, optional
            if True the queues will be deleted if False the queues will be preserved, by default True
        from_siqquit : bool, optional
            if True then the manager knows that the program wants to quit so will perform actions based off the sigquit signal, by default False
        """
        try:
            if self.iwr6843_process:
                self.iwr6843_process.terminate()
                del self.iwr6843_process
        except AttributeError:
            pass
        try:
            if self.run_arduino_process:
                if self.arduino_process:
                    self.arduino_process.terminate()
                    del self.arduino_process
        except AttributeError:
            pass
        try:
            del self.ports
            del self.control
        except AttributeError:
            pass
        try:
            if yeet_queue:
                del self.objects_queue
                if self.run_arduino_process:
                    del self.angles_queue
        except AttributeError:
            pass
        if from_sigquit:
            try:
                keyboard.unhook_all()
                pygame.quit()
            except:
                pass
            Utils.dump_to_json(list(self.voxels_dict.values()), self.output_file_name)
            try:
                del self.voxels_dict
            except AttributeError:
                pass

    def handle_detected_objects(self, detected_objects: List[DetectedObject], sort: bool = False) -> None:
        """handle_detected_objects handles a list of detected objects if given a rotation angle or not

        Parameters
        ----------
        detected_objects : List[DetectedObject]
            the list of detected objects
        rotation : Tuple[int,int], optional
            the h and v rotation angles, by default ()
        sort : bool
            specifies whether or not to sort the dictionary after adding detected objects, by default False
        """
        if not(self.arduino_process.wait_flag):
            # Loop through each detected object
            for object in detected_objects:
                # Check that this object is not None (i.e. has members)
                if object.x and object.y and object.z and object.snr:
                    x = object.x
                    y = object.y
                    z = object.z

                    # Rotate the coordinates if needed
                    #x,y,z = MathUtils.b_to_d_rotation(x,y,z,self.rotation[0],self.rotation[1])

                    # Check if this detected object is in a new voxel or not
                    temp = DetectedObjectVoxel(x,y,z,snr=object.snr,noise=object.noise)
                    if temp.snr > 0.5*temp.noise:
                        self.voxels_dict[temp] = temp
                        self.plot.update(temp)
                    #try:
                    #    getting = self.voxels_dict[temp]
                    #    del getting
                    # Detected object is a new object
                    #except KeyError:
                    #    self.voxels_dict[temp] = temp
                    #    self.plot.update(temp)
            if sort:
                self.voxels_dict = {k: v for k, v in sorted(self.voxels_dict.items(), key=cmp_to_key(compare_detected_object_voxels))}

    def routine(self):
        """routine a single routine of the manager where it retrieves and handles data and re-draws the plot based on data
        """

        # Get the rotation angles if present or using arduino process to get the servo angle
        if self.run_arduino_process:
            temp = self.get_servo_angle()
            if temp and (temp != self.rotation):
                self.rotation = temp

        # Get detected objects
        detected_objects = self.get_detected_objects()

        # Handle the detected objects
        self.handle_detected_objects(detected_objects)

        # Draw/re-draw the plot
        if self.plot_mode == PlotMode.PLOT_CUBES:
            self.plot.draw(self.x_rotation, self.y_rotation, self.z_translation, self.y_translation)
        else:
            self.plot.draw()

        # Add in for drawing with the cube plot
        if self.plot_mode == PlotMode.PLOT_CUBES:
            self.plot.cube_list.plot_cubes(self.x_rotation, self.y_rotation, self.z_translation, self.y_translation)

        # Delete objects no longer being used
        del detected_objects

        return

    def handle_keyboard_inputs(self):
        if self.plot_mode == PlotMode.PLOT_CUBES:
            if keyboard.is_pressed("left"):
                self.y_rotation = self.y_rotation - 5
            elif keyboard.is_pressed("right"):
                self.y_rotation = self.y_rotation + 5
            elif keyboard.is_pressed("up"):
                self.x_rotation = self.x_rotation - 5
            elif keyboard.is_pressed("down"):
                self.x_rotation = self.x_rotation + 5
            elif keyboard.is_pressed("/"):
                self.z_translation = self.z_translation + 5
            elif keyboard.is_pressed("Shift"):
                self.z_translation = self.z_translation - 5
            elif keyboard.is_pressed(";"):
                self.y_translation = self.y_translation - 5
            elif keyboard.is_pressed("\'"):
                self.y_translation = self.y_translation + 5
            elif keyboard.is_pressed("."):
                # resets all keys
                self.x_rotation = 0
                self.y_rotation = 0
                self.z_translation = 0
                self.y_translation = 0

    def handle_pygame_events(self):
        if self.plot_mode == PlotMode.PLOT_CUBES:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    self.yeet(from_sigquit=True)
                    exit(0)

    def run(self):
        """
        run runs the main routine of the manager where it grabs detected objects, handles data, re-draws the plot, and
        keeps itself alive
        """
        # self.page_control.start_page()   # TODO:
        # self.input_page: PageMatplotlib = PageMatplotlib(self.input_angles_queue)
        # self.input_page.start()
        while True:
            # Handle pygame events
            self.handle_pygame_events()

            # Handle keyboard inputs
            self.handle_keyboard_inputs()

            # Parse all detected objects
            while self.detected_objects_are_present():
                # Handle keyboard inputs
                self.handle_keyboard_inputs()

                # Run routine
                self.routine()

                # Sleep
                sleep(0.01)

            # Stay alive
            self.staying_alive()

            # Sleeps/pauses
            sleep(0.01)
            if self.plot_mode != PlotMode.PLOT_CUBES:
                plt.pause(0.01)
