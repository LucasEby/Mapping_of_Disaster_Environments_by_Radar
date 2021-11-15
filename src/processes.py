# Standard Library Imports
from multiprocessing import Process, Queue
from time import sleep
from termios import error

# Package Imports
from serial import Serial, SerialException

# Self Imports
from data import PacketHandler

class IWR6843ReadProcess(Process):
    """SerialProcess represents a process to handle reading from the IWR6843 serial data port in another process
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
        super(IWR6843ReadProcess, self).__init__(target=self.read_serial, args=(serial_port, baudrate, timeout))
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
        self.serial = Serial(serial_port, baudrate=baudrate, timeout=timeout)
        while True:
            read_buffer = []
            try:
                read_buffer = self.serial.read(self.serial.inWaiting())
            except (SerialException, OSError, error):
                break
            if len(read_buffer) > 0:
                parsed = self.parser.parser(read_buffer)
                if parsed:
                    self.queue.put(parsed)
            sleep(0.01)

class ArduinoReadProcess(Process):
    """ArduinoReadProcess represents a process to handle reading from the arduino serial port in another process
    """
    def __init__(self, queue: Queue, serial_port: str, baudrate: int, timeout: float):
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
        super(ArduinoReadProcess, self).__init__(target=self.read_serial, args=(serial_port, baudrate, timeout))
        self.queue = queue
        self.serial = None
        self.target = self.read_serial

    def read_serial(self, serial_port: str, baudrate: int, timeout: float):
        """read_serial is the target of this process which starts the serial port and reads from the serial port

        Parameters
        ----------
        serial_port : str
            the serial port to connect to
        baudrate : int
            the baud rate of the serial port
        timeout : float
            the timeout to add to the serial port
        """
        self.serial = Serial(serial_port, baudrate=baudrate, timeout=timeout)
        while True:
            read_buffer = []
            try:
                read_buffer = self.serial.readline()
            except (SerialException, OSError, error):
                break
            if len(read_buffer) > 0:
                read_buffer = read_buffer.decode('utf-8')
                read_buffer = read_buffer.split(",")
                try:
                    hv_values = (int(read_buffer[0]),int(read_buffer[1]))
                    self.queue.put(hv_values)
                except (IndexError):
                    break
            sleep(0.01)
