
# Standard Library Imports
from abc import ABC, abstractmethod

# Package Imports
import numpy as np
import matplotlib.pyplot as plt

# Self Imports
from data import DetectedObject

class Plot(ABC):
    """Plot is a base class to plot detected objects
    """    

    def __init__(self, resolution: float = None):
        """__init__ initialize the plot

        Parameters
        ----------
        resolution : float, optional
            the plotting resolution, by default None
        """        
        if resolution:
            self.resolution = resolution
        
    def draw(self) -> None:
        """draw draw/re-draw this plot
        """
        plt.show(block=False)
        plt.pause(0.01)

    @abstractmethod
    def update(self, object: DetectedObject) -> None:
        """update update the values to plot

        Parameters
        ----------
        object : DetectedObject
            the object used to update the values
        """
        pass

class Plot1(Plot):
    """Plot1 is a helper class to plot detected objects
    """
    def __init__(self, resolution: float = None):
        """__init__ initialize the plot

        Parameters
        ----------
        resolution : float, optional
            the plotting resolution, by default None
        """    
        super(Plot1, self).__init__(resolution)
        self.fig = plt.figure()
        self.axis = self.fig.add_subplot(projection='3d')
        self.xs = [0.0]
        self.ys = [0.0]
        self.zs = [0.0]
        self.cs = [0.0]
        self.sp = self.axis.scatter(np.array(self.xs),np.array(self.ys),np.array(self.zs),np.array(self.cs))
        plt.ion()
        plt.pause(0.01)
        plt.show()
        self.axis.set_xlabel("X Position (m)")
        self.axis.set_ylabel("Y Position (m)")
        self.axis.set_zlabel("Z Position (m)")
        self.fig.colorbar(self.sp, label="SNR")

    def draw(self) -> None:
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
        super().draw()

    def update(self, object: DetectedObject) -> None:
        """update update the values to plot

        Parameters
        ----------
        object : DetectedObject
            the object used to update the values
        """
        self.xs.append(object.x)
        self.ys.append(object.y)
        self.zs.append(object.z)
        self.cs.append(object.snr)

class Plot2(Plot):

    def __init__(self, resolution: float = None):
        """__init__ initialize the plot

        Parameters
        ----------
        resolution : float, optional
            the plotting resolution, by default None
        """    
        super(Plot2, self).__init__(resolution)
        self.eps = np.finfo(float).eps
        self.eps = (1+self.eps)*self.eps
        self.xaxis = np.arange(-10.0, 10.0, self.resolution)  
        self.zaxis = np.arange(-10.0, 10.0, self.resolution)  
        self.grid = np.zeros((max(self.xaxis.shape), max(self.zaxis.shape)))
        self.fig = plt.figure()
        self.fig_num = plt.gcf().number
        plt.imshow(np.flipud(self.grid), extent=[self.xaxis[0], self.xaxis[-1], self.zaxis[0], self.zaxis[-1]])
        plt.xlabel("X Axis (m)")
        plt.ylabel("Z Axis (m)")
        plt.title("Range Map")
        self.cbar = plt.colorbar()
        self.cbar.ax.set_ylabel("Range (m)")
        
    def draw(self) -> None:
        """draw draw/re-draw this plot
        """
        plt.figure(self.fig_num)
        plt.imshow(np.flipud(self.grid),extent=[self.xaxis[0], self.xaxis[-1], self.zaxis[0], self.zaxis[-1]])
        super().draw()

    def update(self, object: DetectedObject) -> None:
        """update update the values to plot

        Parameters
        ----------
        object : DetectedObject
            the object used to update the values
        """
        x = object.x
        y = object.y
        z = object.z
        xloc = np.where(np.abs(x-self.xaxis)<(self.resolution-self.eps))
        zloc = np.where(np.abs(z-self.zaxis)<(self.resolution-self.eps))
        if len(xloc)>0 and len(zloc)>0:
            xloc = xloc[0]
            zloc = zloc[0]
            self.grid[xloc,zloc] = y
        plt.clim(np.min(self.grid), np.max(self.grid))
