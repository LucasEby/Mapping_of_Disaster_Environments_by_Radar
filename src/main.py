# Self Imports
from manager import Manager
from visualize import Plot2D, Plot3D, PlotCubes

# Standard Library Imports
import signal
from sys import exit
import argparse

# Package Imports
None

# Define signal handler
def signal_handler(sig, frame, manager: Manager = None):
    if sig == signal.SIGQUIT:
        manager.yeet(from_sigquit=True)
        exit(0)
    elif sig == signal.SIGINT:
        manager.reset()

# Main function
def main():
    # Arguments for this script
    parser = argparse.ArgumentParser(description="Main")
    parser.add_argument("--config-file", help="The configuration file to use to configure the IWR6843", default="sample_profile.cfg", type=str)
    parser.add_argument("--plot2d", help="Specifies if to use a 2D plot to visualize data", dest="plot", action="store_const", const=1)
    parser.add_argument("--plot3d", help="Specifies if to use a 3D plot to visualize data", dest="plot", action="store_const", const=2)
    parser.add_argument("--plot-cubes", help="Specifies if to use a 3D cube plot to visualize data", dest="plot", action="store_const", const=3)
    parser.add_argument("--plot2d-resolution", help="Specifies the resolution used in the 2D plot", default=0.1, type=float)
    parser.add_argument("--port-attach-time", help="Specifies how long the program should take to find/attach to serial ports before a timeout occurs", default=60.0, type=float)
    parser.add_argument("--object-queue-size", help="Specifies how large the queue of objects can reach before no more objects can be added", default=100, type=int)
    parser.add_argument("--use-arduino", help="Specifies if the arduino (outputting gimbal rotation) will be used", action="store_true")
    parser.add_argument("--output", help="The file name/path of where data will be outputted, must be a .json file", default="output.json",type=str)
    parser.set_defaults(plot=0, use_arduino=False)
    args = parser.parse_args()

    # Handle the plot arguments
    plot = None
    if args.plot == 0:
        raise AttributeError("The plot type was not specified either '--plot2d' or '--plot3d'")
    elif args.plot == 1:
        plot = Plot2D(args.plot2d_resolution)
    elif args.plot == 2:
        plot = Plot3D()
    elif args.plot == 3:
        plot = PlotCubes(args.plot2d_resolution)

    # Initialize the manager
    manager = Manager(args.config_file, plot, port_attach_time=args.port_attach_time, queue_size=args.object_queue_size, run_arduino_process=args.use_arduino, output_file_name=args.output)

    # Handle SIGINT and SIGQUIT
    signal_handler_use = lambda x, y: signal_handler(x,y,manager=manager)
    signal.signal(signal.SIGINT, signal_handler_use)
    signal.signal(signal.SIGQUIT, signal_handler_use)

    # Run the manager
    manager.run()


if __name__ == '__main__':
    main()
