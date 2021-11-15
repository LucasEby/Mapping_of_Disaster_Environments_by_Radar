# Standard Library Imports
import signal
from sys import exit

# Package Imports
import numpy as np
import matplotlib.pyplot as plot

# Self Imports
from manager import Manager
from data import MathUtils, DetectedObjectVoxel

class Plotter:
    """Plotter is a helper class to plot detected objects
    """
    def __init__(self):
        """__init__ initialize the plotter
        """
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
        """draw draw/re-draw this plot
        """
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

    def update(self, x: float, y: float, z: float, snr: float) -> None:
        """update update the values to plot

        Parameters
        ----------
        x : float
            a x-position
        y : float
            a y-position
        z : float
            a z-position
        snr : float
            signal to noise ratio
        """
        self.xs.append(x)
        self.ys.append(y)
        self.zs.append(z)
        self.cs.append(snr)

def main():
    # Init manager
    config_file_name = '../data/xwr68xx_profile_2021_11_06T20_15_26_698.cfg'
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

    # Dictinonary of voxels
    voxels_dict = {}

    # Main loop
    while True:
        # Always check if detected objects are present
        while manager.detected_objects_are_present():
            # Get the servo angle
            h, v = 0, 0
            hv = manager.get_servo_angle()
            if hv:
                h, v = hv

            # Get detected objects
            gotten = manager.get_detected_objects()

            # Iterate through each detected object
            for got in gotten:
                # Check that this object is not None (i.e. has members)
                if got.x and got.y and got.z and got.snr:
                    # Rotate the coordinates
                    x, y, z = MathUtils.b_to_d_rotation(got.x, got.y, got.z, h, v)

                    # Check if this detected object is in a new voxel or not
                    temp = DetectedObjectVoxel(x,y,z,snr=got.snr)
                    if voxels_dict.get(temp):
                        continue
                    # Detected object is a new object
                    else:
                        voxels_dict[temp] = temp
                        plotter.update(temp.x,temp.y,temp.z,temp.snr)

            # Draw/re-draw the plot
            plotter.draw()

            # Delete the list of detected objects
            del gotten

        # Pause for plot (for matplotlib to function)
        plot.pause(0.01)

        # Keep the program alive
        manager.staying_alive()


if __name__ == '__main__':
    main()
