# Standard Library Imports
import signal
from sys import exit
from abc import ABC, abstractclassmethod

# Package Imports
import matplotlib.pyplot as plt

# Self Imports
from manager import Manager
from data import MathUtils, DetectedObjectVoxel
from visualize import Plot1, Plot2

def main():
    # Init manager
    config_file_name = '../data/xwr68xx_profile_2021_11_06T20_15_26_698.cfg'
    manager = Manager(config_file_name)

    # Init plot
    plot = Plot1()

    # Dictionary of voxels
    voxels_dict = {}

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
                        plot.update(temp)

            # Draw/re-draw the plot
            plot.draw()

            # Delete the list of detected objects
            del gotten

        # Pause for plot (for matplotlib to function)
        plt.pause(0.01)

        # Keep the program alive
        manager.staying_alive()


if __name__ == '__main__':
    main()
