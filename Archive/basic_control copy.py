import serial
import time
from data import Reader, PacketHandler
from control_working import Control, Ports
config_file_name = 'xwr68xx_profile_2021_10_24T03_23_44_468.cfg'

ports = Ports()
controller = Control(config_file_name, ports)
cli_port = ports.cli_port
data_port = ports.data_port

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
#cli_port.write("aoaFovCfg 0 -1 1 -1 1\n".encode("latin-1"))
#controller.aoa_fov_cfg = [-1, -90.0, 90.0, -90.0, 90.0]
#print(controller.aoa_fov_cfg)
time.sleep(0.01)

"""
success_read = 0
print("another read")

while success_read < 5:
    read_buffer = data_port.read(data_port.inWaiting())
    if len(read_buffer) > 0:
        parsed = parser.parser(read_buffer)
        if parsed:
            print(parsed)
            success_read = success_read + 1
"""