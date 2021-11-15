# Self Imports
from control import Ports, Control
from data import DetectedObject
from processes import IWR6843ReadProcess, ArduinoReadProcess

# Standard Library Imports
from multiprocessing import Queue
from time import sleep
from typing import Tuple, List

# Package Imports
None

class Manager:
    """Manager starts and initializes any processes and objects for controlling and communicating with the IWR6843
    """

    def __init__(self, config_file_name: str, port_attach_time: float = 60.0, queue_size: int = 100, run_arduino_process: bool = True):
        """__init__ Initialize the manager with initial parameters and initialize its objects

        Parameters
        ----------
        config_file_name : str
            the initial configuration file
        port_attach_time : float, optional
            the time to wait to attach to the IWR6843 serial ports, by default 60.0
        queue_size : int, optional
            the size of the queue from reading from the serial port, by default 100
        """
        self.config_file_name = config_file_name
        self.port_attach_time = port_attach_time
        self.run_arduino_process = run_arduino_process
        self.ports = None
        self.control = None
        self.objects_queue = Queue(queue_size)
        self.iwr6843_process = None
        if self.run_arduino_process:
            self.angles_queue = Queue(1)
            self.arduino_process = None
        self.reset()

    def reset(self) -> None:
        """reset resets the manager, and restarts any processes, port finders, or controllers
        """
        self.yeet(yeet_queue=False)
        self.ports = Ports(attach_time=self.port_attach_time, attach_to_ports=False)
        self.iwr6843_process = IWR6843ReadProcess(self.objects_queue, self.ports.data_port, 921600, 0.1)
        if self.run_arduino_process:
            self.arduino_process = ArduinoReadProcess(self.angles_queue, self.ports.arduino_port, 9600, 0.1)
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
        return not(self.objects_queue.empty())

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

    def yeet(self, yeet_queue: bool = True) -> None:
        """yeet yeets (kills) any child processes and yeets (deletes) any data

        Parameters
        ----------
        yeet_queue : bool, optional
            if True the queues will be deleted if False the queues will be preserved, by default True
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
        del self.ports
        del self.control
        if yeet_queue:
            del self.objects_queue
            if self.run_arduino_process:
                del self.angles_queue
