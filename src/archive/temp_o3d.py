from data import Utils
import open3d as o3d
import numpy as np

points = Utils.open_json("../data/sample_output_3.json")
xs = []
ys = []
zs = []

for val in points:
    xs.append(val['x'])
    ys.append(val['z'])
    zs.append(val['y'])

points = np.vstack((np.array(xs), np.array(ys), np.array(zs))).T

pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(points)

#o3d.visualization.draw_geometries([pcd])

voxel_grid = o3d.geometry.VoxelGrid.create_from_point_cloud(pcd,voxel_size=0.1)
o3d.visualization.draw_geometries([voxel_grid])