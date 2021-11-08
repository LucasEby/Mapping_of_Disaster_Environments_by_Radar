# Standard Library Imports
from multiprocessing import Process, Queue
from time import sleep

# Package Imports
from serial import Serial

# Self Imports
from data import PacketHandler

class SerialProcess(Process):
    """SerialProcess represents a process to handle reading from a serial port in another process
    """    
    def __init__(self, queue: Queue, serial_port: str, baudrate: int, timeout: float):
        """__init__ sets up the data for the serial process

        Parameters
        ----------
        queue : Queue
            the queue to add data into
        serial_port : str
            the serial port to connect to
        baudrate : int
            the baud rate of the serial port
        timeout : float
            the timeout to add to the serial port
        """        
        super(SerialProcess, self).__init__(target=self.read_serial, args=(serial_port, baudrate, timeout))
        self.queue = queue
        self.serial = None
        self.parser = PacketHandler()
        self.target = self.read_serial

    def read_serial(self, serial_port: str, baudrate: int, timeout: float):
        """read_serial is the target of this process which starts the serial port and reads from the serial port

        Parameters
        ----------
        serial_port : str
            [description]
        baudrate : int
            the baud rate of the serial port
        timeout : float
            the timeout to add to the serial port
        """        
        self.serial = Serial(serial_port, baudrate=baudrate, timeout=timeout, exclusive=True)
        while True:
            read_buffer = self.serial.read(self.serial.inWaiting())
            if len(read_buffer) > 0:
                parsed = self.parser.parser(read_buffer)
                if parsed:
                    self.queue.put(parsed)
            sleep(0.01)

class ArduinoSerialProcess(Process):
    """SerialProcess represents a process to handle reading from a serial port in another process
    """    
    def __init__(self, serial_port: str, baudrate: int, timeout: float):
        """__init__ sets up the data for the serial process

        Parameters
        ----------
        serial_port : str
            the serial port to connect to
        baudrate : int
            the baud rate of the serial port
        timeout : float
            the timeout to add to the serial port
        """        
        super(ArduinoSerialProcess, self).__init__(target=self.read_serial, args=(serial_port, baudrate, timeout))
        self.serial = None
        self.target = self.read_serial

    def read_serial(self, serial_port: str, baudrate: int, timeout: float):
        """read_serial is the target of this process which starts the serial port and reads from the serial port

        Parameters
        ----------
        serial_port : str
            [description]
        baudrate : int
            the baud rate of the serial port
        timeout : float
            the timeout to add to the serial port
        """        
        self.serial = Serial(serial_port, baudrate=baudrate, timeout=timeout, exclusive=True)
        sleep(0.1)
        self.serial.write("hi".encode('utf-8'))
        sleep(1.0)
        while True:
            read_buffer = self.serial.readline()
            if len(read_buffer) > 0:
                print(read_buffer.decode('utf-8'))
            sleep(0.01)