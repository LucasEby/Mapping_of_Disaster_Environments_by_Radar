# Standard Library Imports
from time import sleep

# Package Imports
None

# Self Imports
from manager import Manager

if __name__ == '__main__':
    config_file_name = 'xwr68xx_profile_2021_10_24T03_23_44_468.cfg'
    manager = Manager(config_file_name, read_wait_time=0.0, port_attach_time=10.0, queue_size=10)
    manager.start()

    while True:    
        while not(manager.queue.empty()):
            print(manager.queue.get(timeout=1.0), flush=True)
        sleep(0.01)        