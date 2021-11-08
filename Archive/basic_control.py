import serial
import time
from data import Reader, PacketHandler
from config_writer import Config
config_file_name = 'xwr68xx_profile_2021_10_24T03_23_44_468.cfg'

cli_port = None
data_port = None

def config(config_file):
    cli_port = serial.Serial('/dev/tty.SLAB_USBtoUART', 115200)
    data_port = serial.Serial('/dev/tty.SLAB_USBtoUART4', 921600)
    cli_port.reset_input_buffer()
    cli_port.reset_output_buffer()
    data_port.reset_input_buffer()
    data_port.reset_output_buffer()

    # Read the configuration file and send it to the board
    config = [line.rstrip('\r\n') for line in open(config_file)]
    for i in config:
        cli_port.write((i+'\n').encode('latin-1'))
        print(i)
        time.sleep(0.01)

    return cli_port, data_port

#cli_port, data_port = config()
configger = Config(config_file_name)
cli_port = configger.cli_port
data_port = configger.get_data_port()

parser = PacketHandler()
success_read = 0

while success_read < 5:
    read_buffer = data_port.read(data_port.inWaiting())
    if len(read_buffer) > 0:
        parsed = parser.parser(read_buffer)
        if parsed:
            print(parsed)
            success_read = success_read + 1

#configger.aoa_fov_cfg = [0, -90.0, 1.0, -1.0, 1.0]
cli_port.write("aoaFovCfg 0 -1 1 -1 1\n".encode("latin-1"))
#time.sleep(0.01)

success_read = 0
print("another read")

while success_read < 5:
    read_buffer = data_port.read(data_port.inWaiting())
    if len(read_buffer) > 0:
        parsed = parser.parser(read_buffer)
        if parsed:
            print(parsed)
            success_read = success_read + 1