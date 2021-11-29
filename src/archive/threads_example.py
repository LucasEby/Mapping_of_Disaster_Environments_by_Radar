# Standard Library Imports
from queue import Queue, Empty

# Package Imports
import numpy as np
import matplotlib.pyplot as plot

# Self Imports
from data import Reader
from control import Control, Ports
from threads import ReadThread

if __name__ == '__main__':
    #config_file_name = 'xwr68xx_profile_2021_10_24T03_23_44_468.cfg'
    config_file_name = 'xwr68xx_profile_2021_11_06T20_15_26_698.cfg'
    #config_file_name = '/Users/Anuj/Downloads/profile_2021_11_06T23_37_39_285.cfg'
    ports = Ports(attach_time=30.0)
    reader = Reader(ports)
    controller = Control(config_file_name, ports)

    queue = Queue()
    thread1 = ReadThread(reader, queue)
    thread1.start()

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
        try:
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
        except Empty:
            pass
