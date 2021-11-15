# Standard Library Imports
from multiprocessing import Queue
from time import sleep
import signal             
from sys import exit       

# Package Imports
import numpy as np
import matplotlib.pyplot as plot

# Self Imports
from manager import Manager
from data import MathUtils

class Plotter:
    def __init__(self):
        self.fig = plot.figure()
        self.axis = self.fig.add_subplot(projection='3d')
        self.xs = [0.0]
        self.ys = [0.0]
        self.zs = [0.0]
        self.cs = [0.0]
        self.sp = self.axis.scatter(np.array(self.xs),np.array(self.ys),np.array(self.zs),np.array(self.cs))
        plot.ion()
        plot.pause(0.01)
        plot.show()
        self.axis.set_xlabel("X Position (m)")
        self.axis.set_ylabel("Y Position (m)")
        self.axis.set_zlabel("Z Position (m)")
        self.fig.colorbar(self.sp, label="SNR")

    def draw(self):
        self.sp._offsets3d = (np.array(self.xs),np.array(self.ys),np.array(self.zs))
        cs_array = np.array(self.cs)
        self.sp.set_array(cs_array)
        self.sp.set_clim(min(self.cs), np.quantile(cs_array, 0.8))
        self.axis.set_xlim([min(self.xs), max(self.xs)])
        self.axis.set_ylim([min(self.ys), max(self.ys)])
        self.axis.set_zlim([min(self.zs), max(self.zs)])
        self.fig.canvas.draw_idle()
        plot.show(block=False)
        plot.pause(0.01)

def main():
    # Init manager
    config_file_name = 'xwr68xx_profile_2021_11_06T20_15_26_698.cfg'
    manager = Manager(config_file_name)
    
    # Init plotter
    plotter = Plotter()

    # Define signal handler locally
    def signal_handler(sig, frame):
        if sig == signal.SIGQUIT:
            manager.yeet()
            exit(0)
        elif sig == signal.SIGINT:
            manager.reset()

    # Start signal handler
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGQUIT, signal_handler)

    # Main loop
    while True:      
        while manager.detected_objects_are_present():
            h = 0
            v = 0
            hv = manager.get_servo_angle()
            if hv:
                h, v = hv
            gotten = manager.get_detected_objects()
            for got in gotten:
                if got.x and got.y and got.z and got.snr:
                    x, y, z = MathUtils.b_to_d_rotation(got.x, got.y, got.z, h, v)
                    plotter.xs.append(x)
                    plotter.ys.append(y)
                    plotter.zs.append(z)
                    plotter.cs.append(got.snr)
            plotter.draw()
            del gotten
        plot.pause(0.01)
        manager.staying_alive()

if __name__ == '__main__':
    main()
