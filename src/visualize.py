
# Standard Library Imports
from abc import ABC, abstractmethod
from time import sleep

# Package Imports
import numpy as np
import matplotlib.pyplot as plt
import pygame
from pygame.locals import DOUBLEBUF, OPENGL
from OpenGL.GLU import gluPerspective
import open3d as o3d

# Self Imports
from data import DetectedObject, DetectedObjectVoxel, MathUtils
from cube_list_creator import CubeListCreator
from object_maker import ObjectMaker

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

class Plot3D(Plot):
    """Plot3D is a helper class to plot detected objects
    """
    def __init__(self, resolution: float = None):
        """__init__ initialize the plot

        Parameters
        ----------
        resolution : float, optional
            the plotting resolution, by default None
        """
        super(Plot3D, self).__init__(resolution)
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

class PlotOpen3D(Plot):
    def __init__(self, resolution: float = None):
        """__init__ initialize the plot

        Parameters
        ----------
        resolution : float, optional
            the plotting resolution, by default None
        """
        if resolution is None:
            raise AttributeError("Resolution is not set of the 3D plot")
        super(PlotOpen3D, self).__init__(resolution)
        self.xs = [0.0]
        self.ys = [0.0]
        self.zs = [0.0]
        self.points = np.vstack((np.array(self.xs), np.array(self.zs), np.array(self.ys))).T
        self.pcd = o3d.geometry.PointCloud()
        self.pcd.points = o3d.utility.Vector3dVector(self.points)
        self.voxel_grid = o3d.geometry.VoxelGrid.create_from_point_cloud(self.pcd,voxel_size=self.resolution)
        self.vis = o3d.visualization.Visualizer()
        self.vis.create_window()
        self.vis.add_geometry(self.voxel_grid)

    def draw(self) -> None:
        """draw draw/re-draw this plot
        """
        self.points = np.vstack((np.array(self.xs), np.array(self.zs), np.array(self.ys))).T
        self.pcd.points = o3d.utility.Vector3dVector(self.points)
        self.vis.remove_geometry(self.voxel_grid)
        self.voxel_grid = o3d.geometry.VoxelGrid.create_from_point_cloud(self.pcd,voxel_size=self.resolution)
        self.vis.add_geometry(self.voxel_grid)
        self.vis.poll_events()
        self.vis.update_renderer()
        sleep(0.1)

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


class Plot2D(Plot):

    def __init__(self, resolution: float = None):
        """__init__ initialize the plot

        Parameters
        ----------
        resolution : float, optional
            the plotting resolution, by default None
        """
        if resolution is None:
            raise AttributeError("Resolution is not set of the 2D plot")
        super(Plot2D, self).__init__(resolution)
        self.resolution = abs(resolution)
        self.eps = np.finfo(float).eps
        self.eps = (1+self.eps)*self.eps
        self.xaxis = np.arange(-5.0, 5.0, self.resolution)
        self.zaxis = np.arange(-5.0, 5.0, self.resolution)
        self.ys = []
        self.grid = np.zeros((max(self.xaxis.shape), max(self.zaxis.shape)))
        self.fig = plt.figure()
        self.fig_num = plt.gcf().number
        plt.imshow(np.flipud(self.grid), extent=[self.xaxis[0], self.xaxis[-1], self.zaxis[0], self.zaxis[-1]])
        plt.xlabel("X Axis (m)")
        plt.ylabel("Z Axis (m)")
        plt.title("Range Map")
        self.cbar = plt.colorbar()
        plt.clim(0.0, 5.0)
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
        xloc = np.where(np.abs(x-self.xaxis) < (self.resolution-self.eps))
        zloc = np.where(np.abs(z-self.zaxis) < (self.resolution-self.eps))
        if len(xloc) > 0 and len(zloc) > 0:
            xloc = xloc[0]
            zloc = zloc[0]
            try:
                self.grid[xloc,zloc] = y
                self.ys.append(y)
            except IndexError:
                pass

class PlotCubes(Plot):
    def __init__(self, resolution: float = None):
        """__init__ initialize the plot

        Parameters
        ----------
        resolution : float, optional
            the plotting resolution, by default None
        """
        super(PlotCubes, self).__init__(resolution)
        self.cube_list = CubeListCreator()
        self.maker = ObjectMaker(self.cube_list, 0, 0, 0, 0, self.resolution)
        self.x_rotation = 0
        self.y_rotation = 0
        pygame.init()
        display = (800, 600)
        pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
        # pygame.display.toggle_fullscreen()
        gluPerspective(45, (display[0] / display[1]), 1, 1000.0)

    def draw(self, x_rotation, y_rotation, z_translation, y_translation) -> None:
        """draw draw/re-draw this plot
        """
        self.cube_list.plot_cubes(x_rotation, y_rotation, z_translation, y_translation)

    def update(self, object: DetectedObjectVoxel) -> None:
        """update update the values to plot

        Parameters
        ----------
        object : DetectedObject
            the object used to update the values
        """
        azimuth = 90.0 + MathUtils.get_azimuth(object.x, object.z)
        if object.z >= 0.0:
            # self.maker.add_new_point(object.x, object.y, -50*object.z, azimuth, True)
            self.maker.add_new_point(50*object.x, 50*object.y, -50*object.z, azimuth, True)
