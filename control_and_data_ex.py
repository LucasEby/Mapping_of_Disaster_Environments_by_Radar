from data import Reader
from control import Control, Ports

#config_file_name = 'xwr68xx_profile_2021_10_24T03_23_44_468.cfg'
ports = Ports()
reader = Reader(ports)
#controller = Control(config_file_name, ports)

success_read = 0
while success_read < 5:
    read = reader.read()
    if read:
        print(read)
        success_read = success_read + 1

#controller.aoa_fov_cfg.set_and_write(controller, [-1, -10.0, 10.0, -10.0, 10.0])

success_read = 0
while success_read < 1000:
    read = reader.read()
    if read:
        print(read)
        success_read = success_read + 1
