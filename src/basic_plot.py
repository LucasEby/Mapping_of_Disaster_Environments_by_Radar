from visualize import Plot2D
from data import Utils, DetectedObject
import matplotlib.pyplot as plt

objects = Utils.open_json("original_config.json")
plot = Plot2D(resolution=0.5)
for list_objects in objects:
    for object in list_objects:
        if object['snr'] > 0.5*object['noise']:
            obj = DetectedObject(object['x'], object['y'], object['z'])
            plot.update(obj)

plot.draw()
plt.ioff()
plt.show()