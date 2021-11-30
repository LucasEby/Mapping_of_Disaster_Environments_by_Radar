from termios import error

from serial import Serial, SerialException
import time


class Servos:
    """Servos provides the data transfer between external computer and Arduino board
    """
    def __init__(self) -> None:
        """__init__ initialize the servos with Arduino serial port
        """
        self.queue = None
        self.serial = Serial(port='/dev/cu.usbserial-1430', baudrate=9600, timeout=.1)

    def transfer_input(self, cmd: str) -> None:
        """transfer the user-inputted servo angles to Arduino for motors movements

        Parameters
        ----------
        cmd : str
            the servo position input from GUI in string format
        """
        # try:
        self.serial = Serial(port='/dev/cu.usbserial-1430', baudrate=9600, timeout=.1)
        cmd = cmd.split(" ")
        self.serial.write(bytes(cmd[0], 'utf-8'))
        time.sleep(0.5)
        self.serial.write(bytes(cmd[1], 'utf-8'))
        time.sleep(0.1)

        read_buffer = self.serial.readline()
        print(read_buffer)
        time.sleep(0.1)
        read_buffer = self.serial.readline()
        print(read_buffer)

        # except (SerialException, OSError, error):
        #     print("SerialException or OSError or error")
        #     return
        # if len(read_buffer) > 0:
        #     read_buffer = read_buffer.decode('utf-8')
        #     print(read_buffer)
        #     read_buffer = read_buffer.split(",")
        #     try:
        #         print(read_buffer[0], read_buffer[1], read_buffer[2])
        #         # xyz_values = (int(read_buffer[0]), int(read_buffer[1]), int(read_buffer[2]))
        #         # self.queue.put(xyz_values)
        #     except IndexError:
        #         print("IndexError")
        #         return
