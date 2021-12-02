from visualize import PlotCubes
from data import MathUtils, Utils
import math


point = (0.0,5.0,0.0)

new_point = MathUtils.b_to_d_rotation(point[0],point[1],point[2],(math.pi/180.0)*50.0,(math.pi/180.0)*30.0)
print(new_point)

