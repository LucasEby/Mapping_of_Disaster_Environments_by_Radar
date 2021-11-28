# Self Imports
from control import Ports, Control
from data import DetectedObject, DetectedObjectVoxel, MathUtils, Utils, compare_detected_object_voxels
from processes import IWR6843ReadProcess, ArduinoReadProcess
from visualize import Plot
from page_control import PageControl
from servos import Servos

# Standard Library Imports
from multiprocessing import Queue
from time import sleep
from typing import Tuple, List, Dict
from functools import cmp_to_key

# Package Imports
import matplotlib.pyplot as plt

class Manager:
    """Manager starts and initializes any processes and objects for controlling and communicating with the IWR6843
    """

    def __init__(self, config_file_name: str, plot: Plot, port_attach_time: float = 60.0, queue_size: int = 100, run_arduino_process: bool = False, output_file_name: str = 'output.json'):
        """__init__ Initialize the manager with initial parameters and initialize its objects

        Parameters
        ----------
        config_file_name : str
            the initial configuration file
        plot : Plot
            the Plot object to use to visualize detected objects
        port_attach_time : float, optional
            the time to wait to attach to the IWR6843 serial ports, by default 60.0
        queue_size : int, optional
            the size of the queue from reading from the serial port, by default 100
        """
        self.config_file_name = config_file_name
        self.port_attach_time = port_attach_time
        self.run_arduino_process = run_arduino_process
        self.output_file_name = output_file_name
        self.voxels_dict: Dict[DetectedObject, DetectedObject] = {}
        self.plot = plot
        self.ports = None
        self.control = None
        self.objects_queue = Queue(queue_size)
        self.iwr6843_process = None
        if self.run_arduino_process:
            self.angles_queue = Queue(1)
            self.input_angles_queue = Queue(1)  # TODO: my edits
            self.arduino_process = None
        # self.page: Page = Page()
        self.page_control: PageControl = PageControl(self.input_angles_queue)
        self.reset()

    def reset(self) -> None:
        """reset resets the manager, and restarts any processes, port finders, or controllers
        """
        self.yeet(yeet_queue=False)
        self.ports = Ports(attach_time=self.port_attach_time, attach_to_ports=False, find_arduino=self.run_arduino_process)
        self.iwr6843_process = IWR6843ReadProcess(self.objects_queue, self.ports.data_port, 921600, 0.1)
        if self.run_arduino_process:
            self.arduino_process = ArduinoReadProcess(self.input_angles_queue, self.angles_queue, self.ports.arduino_port, 9600, 0.1)
        self.control = Control(self.config_file_name, self.ports)
        sleep(0.1)
        self.iwr6843_process.start()
        if self.run_arduino_process:
            self.arduino_process.start()

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
                return hv

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
        if self.run_arduino_process:
            if not(self.iwr6843_process.is_alive()) or not(self.arduino_process.is_alive()):
                self.reset()
        else:
            if not(self.iwr6843_process.is_alive()):
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
            Utils.dump_to_json(list(self.voxels_dict.values()), self.output_file_name)
            try:
                del self.voxels_dict
            except AttributeError:
                pass

    def handle_detected_objects(self, detected_objects: List[DetectedObject], rotation: Tuple[int,int] = (), sort: bool = False) -> None:
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
        # Loop through each detected object
        for object in detected_objects:
            # Check that this object is not None (i.e. has members)
            if object.x and object.y and object.z and object.snr:
                x = object.x
                y = object.y
                z = object.z

                # Rotate the coordinates if needed
                if rotation:
                    x,y,z = MathUtils.b_to_d_rotation(x,y,z,rotation[0],rotation[1])

                # Check if this detected object is in a new voxel or not
                temp = DetectedObjectVoxel(x,y,z,snr=object.snr)
                try:
                    getting = self.voxels_dict[temp]
                    del getting
                # Detected object is a new object
                except KeyError:
                    self.voxels_dict[temp] = temp
                    self.plot.update(temp)
        if sort:
            self.voxels_dict = {k: v for k, v in sorted(self.voxels_dict.items(), key=cmp_to_key(compare_detected_object_voxels))}

    def routine(self):
        """routine a single routine of the manager where it retrieves and handles data and re-draws the plot based on data
        """

        # Get the rotation angles if present or using arduino process to get the servo angle
        rotation = ()
        if self.run_arduino_process:
            rotation = self.get_servo_angle()

        # Get detected objects
        detected_objects = self.get_detected_objects()

        # Handle the detected objects
        self.handle_detected_objects(detected_objects, rotation)

        # Draw/re-draw the plot
        self.plot.draw()

        # Delete objects no longer being used
        del rotation
        del detected_objects

        return

    def run(self):
        """run the main routine of the manager where it grabs detected objects, handles data, re-draws the plot, and keeps itself alive
        """
        self.page_control.start_page()   # TODO:
        while True:
            while self.detected_objects_are_present():
                self.routine()
            plt.pause(0.01)
            self.staying_alive()
