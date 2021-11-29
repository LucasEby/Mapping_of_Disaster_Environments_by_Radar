import json
from typing import Any, Dict
import matplotlib.pyplot as plot
import numpy as np
from data import DetectedObjectVoxel

class Utils:
    @classmethod
    def dump_json_default(cls, obj: Any):
        try:
            return str(obj)
        except:
            return obj.__dict__

    @classmethod
    def dump_to_json(cls, data: Dict, file: str) -> None:
        """dump_to_json dumps a Dict into a JSON

        Parameters
        ----------
        data : Dict
            the Dict to dump
        file : str
            the JSON filepath
        """
        with open(file, "w") as write_file:
            json.dump(data, write_file, indent=4, sort_keys=True, default=cls.dump_json_default)

    @classmethod
    def open_json(cls, file: str) -> Dict:
        """open_json opens a JSON file

        Parameters
        ----------
        file : str
            the JSON filepath

        Returns
        -------
        Dict
            a dict representing the JSON objects in the file
        """
        with open(file, "r") as read_file:
            return json.load(read_file)


def main():
    xs = [0.0]
    zs = [0.0]
    ys = [0.0]

    voxels_dict = {}

    data = Utils.open_json("../data/sample.json")
    for dat in data:
        temp = DetectedObjectVoxel(dat['x'], dat['y'], dat['z'])
        if not(voxels_dict.get(temp) is None):
            continue
        else:
            voxels_dict[temp] = temp
            xs.append(temp.x)
            ys.append(temp.y)
            zs.append(temp.z)

    """
    fig = plot.figure()
    axis = fig.add_subplot()
    sp = axis.scatter(np.array(xs),np.array(zs),c=np.array(ys))
    plot.ion()
    plot.pause(0.01)
    plot.show()
    axis.set_xlabel("X Position (m)")
    axis.set_ylabel("Z Position (m)")
    c = fig.colorbar(sp, label="Y Position (m)")
    
    ys_array = np.array(ys)
    sp.set_offsets(np.array([np.array(xs), np.array(zs)]).T)
    sp.set_array(ys_array)
    axis.set_xlim([min(xs), max(xs)])
    axis.set_ylim([min(zs), max(zs)])
    sp.set_clim([min(ys), max(ys)])
    fig.canvas.draw_idle()
    plot.ioff()
    plot.show()

    """
    res = 0.2
    eps = np.finfo(float).eps
    eps = (1+eps)*eps
    xaxis = np.arange(min(xs), max(xs), res)
    zaxis = np.arange(min(zs), max(zs), res)
    grid = np.zeros((max(xaxis.shape), max(zaxis.shape)))

    for i, (x,y,z) in enumerate(zip(xs,ys,zs)):
        xloc = np.where(np.abs(x-xaxis)<(res-eps))
        zloc = np.where(np.abs(z-zaxis)<(res-eps))

        if len(xloc)>0 and len(zloc)>0:
            xloc = xloc[0]
            zloc = zloc[0]
            grid[xloc,zloc] = y

    plot.imshow(np.flipud(grid),extent=[xaxis[0], xaxis[-1], zaxis[0], zaxis[-1]])
    plot.xlabel("X Axis (m)")
    plot.ylabel("Z Axis (m)")
    plot.title("Range Map")
    c = plot.colorbar()
    c.ax.set_ylabel("Range (m)")
    #plot.clabel("Range (m)")
    plot.show()

if __name__ == "__main__":
    main()