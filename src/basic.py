from control import Ports, Control
from data import DetectedObject, DetectedObjectVoxel, MathUtils, Utils, compare_detected_object_voxels
from processes import IWR6843ReadProcess, ArduinoReadProcess
from multiprocessing import Queue
import signal
from sys import exit
from time import sleep
from visualize import Plot2D
import matplotlib.pyplot as plt

def signal_handler(sig, frame, queue, process):
    if sig == signal.SIGINT or sig == signal.SIGQUIT:
        #process.terminate()
        temp = []
        while not(queue.empty()):
            temp.append(queue.get())
        Utils.dump_to_json(temp, "original_config.json")
        exit(0)

def main():
    # Init and shit
    config_file = "/Users/Anuj/Documents/Workspace/Capstone/Mapping_of_Disaster_Environments_by_Radar/data/sample_profile.cfg"
    objects_queue = Queue()
    plot = Plot2D(0.5)
    plt.pause(0.1)
    sleep(1.0)

    # Setup shit
    ports = Ports(attach_to_ports=False, find_arduino=False)
    print(ports.data_port)
    process = IWR6843ReadProcess(objects_queue, ports.data_port, 921600, 0.1)
    
    # Handle sigint
    signal_handler_use = lambda x,y: signal_handler(x,y,queue=objects_queue,process=process)
    signal.signal(signal.SIGINT, signal_handler_use)

    control = Control(config_file, ports)
    sleep(0.1)
    process.start()

    while True:
        #sleep(1.0)
        while not(objects_queue.empty()):
            try:
                objects = objects_queue.get()
                #print(objects)
                for object in objects:
                    #if object['snr'] > 0.5*object['noise']:
                    #obj = DetectedObject(object['x'], object['y'], object['z'])
                    #print("update")
                    if object.snr > 0.4*object.noise:
                    #if object.y <= 6.0:
                        plot.update(object)
                plot.draw()
                plt.pause(0.01)
            except:
                pass
            sleep(0.01)

if __name__ == '__main__':
    main()