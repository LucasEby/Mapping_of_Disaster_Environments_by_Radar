# Standard Library Imports
from multiprocessing import Process, Queue
from time import sleep

# Package Imports
None

# Self Imports
from control import Ports, Control
from processes import IWR6843ReadProcess, ArduinoReadProcess

class Starter:
    """Starter starts and initializes any processes and objects for controlling and communicating with the IWR6843
    """    

    def __init__(self, config_file_name: str, read_wait_time: float = 0.0, port_attach_time: float = 60.0, queue_size: int = 100):
        """__init__ Initialize the starter with initial parameters and initialize its objects

        Parameters
        ----------
        config_file_name : str
            the initial configuration file
        read_wait_time : float, optionl
            the time to wait to read after another read
        port_attach_time : float, optional
            the time to wait to attach to the IWR6843 serial ports, by default 60.0
        queue_size : int, optional
            the size of the queue from reading from the serial port, by default 100
        """
        self.config_file_name = config_file_name
        self.objects_queue = Queue(10)
        self.angles_queue = Queue(1)
        self.ports = Ports(attach_time=20.0, attach_to_ports=False)
        self.iwr6843_process = IWR6843ReadProcess(self.objects_queue, self.ports.data_port, 921600, 0.1)
        self.arduino_process = ArduinoReadProcess(self.angles_queue, self.ports.arduino_port, 9600, 0.1)
        self.control = Control(self.config_file_name, self.ports)
        sleep(0.1)
        self.iwr6843_process.start()       
        self.arduino_process.start() 
