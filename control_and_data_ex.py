from data import Reader
from control import Control, Ports
from threads import ReadThread, QueueThread
from queue import Queue
import time
import matplotlib.pyplot as plot


config_file_name = 'xwr68xx_profile_2021_10_24T03_23_44_468.cfg'
ports = Ports()
reader = Reader(ports)
controller = Control(config_file_name, ports)

queue = Queue()


thread1 = ReadThread(reader, queue)
thread1.start()
thread2 = QueueThread(queue)
thread2.start()

#time.sleep()
controller.aoa_fov_cfg.set_and_write(controller, [-1, -10.0, 10.0, -10.0, 10.0])

#fig = plot.figure()
#axis = fig.add_subplot(projection='2d')
plot.scatter(0.0,0.0)
plot.ion()
plot.pause(0.01)

while True:
    try:
        gotten = queue.get()
        print(gotten)
        for got in gotten:
            plot.scatter(got.x,got.y)
            plot.pause(0.01)
            plot.show()
            
    except Empty:
        pass

