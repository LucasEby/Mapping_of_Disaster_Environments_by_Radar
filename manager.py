# Standard Library Imports
from queue import Queue

# Package Imports
None

# Self Imports
from data import Reader
from control import Control, Ports
from threads import ReadThread
from timer import Timer, TimeOutException

class Manager:
    """Manager manages various main thread and threaded processes in communicating with the IWR6843
    """    

    def __init__(self, config_file_name: str, read_wait_time: float = 0.0, port_attach_time: float = 60.0, queue_size: int = 100):
        """__init__ Initialize the manager with initial parameters and initialize its objects

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
        self.ports = Ports(attach_time=port_attach_time)
        self.reader = Reader(self.ports)
        self.config_file_name = config_file_name
        self.controller = Control(self.config_file_name, self.ports)
        self.queue = Queue(queue_size)
        self.read_thread = ReadThread(self.reader, self.queue, wait_time=read_wait_time)
    
    def start(self):
        """start Start the manager
        """        
        self.read_thread.start()