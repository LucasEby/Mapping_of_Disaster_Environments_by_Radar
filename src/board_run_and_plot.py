# Standard Library Imports
from sys import exit
import signal

# Package Imports
import matplotlib.pyplot as plot

# Self Imports
from manager import Manager
from data import DetectedObjectVoxel
from main import Plotter

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
            # Get detected objects
            gotten = manager.get_detected_objects()

            # Iterate through each detected object
            for got in gotten:
                # Check that this object is not None (i.e. has members)
                if got.x and got.y and got.z and got.snr:
                    # Rotate the coordinates
                    temp = DetectedObjectVoxel(got.x,got.y,got.z,snr=got.snr)

                    # Check if this detected object is in a new voxel or not
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
