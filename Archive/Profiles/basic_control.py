import serial
import time
from packet import PacketHandler

config_file_name = 'xwr68xx_profile_2021_10_24T03_23_44_468.cfg'

cli_port = None
data_port = None

def config(config_file='xwr68xx_profile_2021_10_24T03_23_44_468.cfg'):
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

cli_port, data_port = config()

parser = PacketHandler()
#reads = 1
#while reads < 1:
read_buffer = data_port.read(data_port.inWaiting())
if len(read_buffer) > 0:
    print(parser.parser(read_buffer))
        #ti_packet_parser.parser_one_mmw_demo_output_packet(read_buffer, len(read_buffer))