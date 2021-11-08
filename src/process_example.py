# Standard Library Imports
from multiprocessing import Queue
from time import sleep

# Package Imports
import numpy as np
import matplotlib.pyplot as plot

# Self Imports
from control import Ports, Control
from processes import SerialProcess

if __name__ == '__main__':
    config_file_name = 'xwr68xx_profile_2021_11_06T20_15_26_698.cfg'
    queue = Queue(100)
    ports = Ports(attach_time=20.0, attach_to_ports=False)
    process = SerialProcess(queue, ports.data_port, 921600, 0.1)
    control = Control(config_file_name, ports)
    sleep(0.1)
    process.start()
    
    fig = plot.figure()
    axis = fig.add_subplot(projection='3d')
    xs = [0.0]
    ys = [0.0]
    zs = [0.0]
    cs = [0.0]
    sp = axis.scatter(np.array(xs),np.array(ys),np.array(zs),np.array(cs))
    plot.ion()
    plot.pause(0.01)
    plot.show()
    axis.set_xlabel("X Position (m)")
    axis.set_ylabel("Y Position (m)")
    axis.set_zlabel("Z Position (m)")

    fig.colorbar(sp, label="SNR")

    while True:
        while not(queue.empty()):
            gotten = queue.get(block=True)
            for got in gotten:
                xs.append(got.x)
                ys.append(got.y)
                zs.append(got.z)
                cs.append(got.snr)
            sp._offsets3d = (np.array(xs),np.array(ys),np.array(zs))
            cs_array = np.array(cs)
            sp.set_array(cs_array)
            sp.set_clim(min(cs), np.quantile(cs_array, 0.8))
            axis.set_xlim([min(xs), max(xs)])
            axis.set_ylim([min(ys), max(ys)])
            axis.set_zlim([min(zs), max(zs)])
            fig.canvas.draw_idle()
            plot.show(block=False)
            plot.pause(0.01)
        plot.pause(0.01)

    #while True:
    #    if not(queue.empty()):
    #        print(queue.get())
    #    sleep(0.01)
    
