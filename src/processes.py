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
        # Temp
        self.counter = 0

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
                    #self.counter = self.counter + 1
                    #print(self.counter)
                    self.queue.put(parsed)
            sleep(0.01)

    def kill(self):
        try:
            self.serial.close()
            del self.serial
        except AttributeError:
            pass
        try:
            del self.parser
        except AttributeError:
            pass
        super().kill()

class ArduinoReadProcess(Process):
    """ArduinoReadProcess represents a process to handle reading from the arduino serial port in another process
    """
    def __init__(self, input_queue: Queue, queue: Queue, serial_port: str, baudrate: int, timeout: float):
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
        self.input_queue = input_queue
        self.queue = queue
        self.serial = None
        self.target = self.read_serial
        self.wait_flag = False

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
            if not(self.input_queue.empty()):
                input_angles = self.input_queue.get().split(" ")
                self.serial.write(bytes(input_angles[0], 'utf-8'))
                sleep(0.5)
                self.serial.write(bytes(input_angles[1], 'utf-8'))
                sleep(0.5)
            read_buffer = []
            try:
                read_buffer = self.serial.readline()
            except (SerialException, OSError, error):
                break
            if len(read_buffer) > 0:
                try:
                    read_buffer = read_buffer.decode('utf-8')
                except UnicodeDecodeError:
                    pass
                try:
                    if read_buffer == "start":
                        self.wait_flag = True
                    elif read_buffer == "stop":
                        self.wait_flag = False
                except:
                    pass
                try:
                    read_buffer = read_buffer.split(",")
                    try:
                        hv_values = (float(read_buffer[0]),float(read_buffer[1]))
                        self.queue.put(hv_values)
                        self.wait_flag = False
                    except IndexError:
                        break
                except:
                    pass
            sleep(0.01)

    def kill(self):
        try:
            self.serial.close()
            del self.serial
        except AttributeError:
            pass
        super().kill()
