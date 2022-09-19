import numpy as np
import os
import csv
import math
import numba
import pdb
from tqdm import tqdm

PI_rads = math.pi / 180


def create_data_infos(labelfile, lidar_path):
    infos = {}
    gt_boxes = []
    gt_boxes_all = []
    points = []
    label_fpath = os.path.join(csv_path, labelfile)
    with open(lidar_path, 'r') as f:
        for line in f.readlines()[11:len(f.readlines()) - 1]:
            linestr = line.split(" ")
            if len(linestr) == 4:
                linestr_convert = list(map(float, linestr))
                points.append(linestr_convert)
            line = f.readline().strip()
    infos['points'] = np.array(points)
    with open(label_fpath, 'r') as f:
        reader = csv.reader(f)
        for i in reader:
            if int(i[1]) == 1:
                continue
            gt_boxes.append(
                [float(i[2]) / 100, float(i[3]) / 100, float(i[4]) / 100, float(i[7]) / 100, float(i[8]) / 100,
                 float(i[9]) / 100, float(i[6]) * PI_rads])  ##依次为x,y,z,l,w,h,angle，单位为厘米和角度，请对照自己的标签格式自行修改
            # gt_boxes_all.append([float(i[0]), float(i[1]),float(i[2]), float(i[3]), float(i[4]), float(i[5]),float(i[6]),float(i[7]), float(i[8]) ,
            #      float(i[9]),
            #      float(i[10]),
            #      float(i[11]),
            #      float(i[12]),
            #      float(i[13]),
            #      float(i[14])])
            gt_boxes_all.append(i)
    gt_boxes = np.array(gt_boxes)
    gt_boxes_all = np.array(gt_boxes_all)
    infos['gt_boxes'] = gt_boxes
    infos['gt_boxes_all'] = gt_boxes_all
    return infos


def corners_nd(dims, origin):
    ndim = int(dims.shape[1])
    corners_norm = np.stack(
        np.unravel_index(np.arange(2 ** ndim), [2] * ndim),
        axis=1).astype(dims.dtype)
    if ndim == 2:
        # generate clockwise box corners
        corners_norm = corners_norm[[0, 1, 3, 2]]
    elif ndim == 3:
        corners_norm = corners_norm[[0, 1, 3, 2, 4, 5, 7, 6]]
    corners_norm = corners_norm - np.array(origin, dtype=dims.dtype)
    corners = dims.reshape([-1, 1, ndim]) * corners_norm.reshape(
        [1, 2 ** ndim, ndim])
    return corners


def rotation_3d_in_axis(points, angles, axis=0):
    # print("points is :", points)
    # ("angles is :", angles)
    rot_sin = np.sin(angles)
    rot_cos = np.cos(angles)
    ones = np.ones_like(rot_cos)
    zeros = np.zeros_like(rot_cos)
    if axis == 1:
        rot_mat_T = np.stack([[rot_cos, zeros, -rot_sin], [zeros, ones, zeros],
                              [rot_sin, zeros, rot_cos]])
    elif axis == 2 or axis == -1:
        rot_mat_T = np.stack([[rot_cos, rot_sin, zeros],
                              [-rot_sin, rot_cos, zeros], [zeros, zeros, ones]])
    elif axis == 0:
        rot_mat_T = np.stack([[zeros, rot_cos, -rot_sin],
                              [zeros, rot_sin, rot_cos], [ones, zeros, zeros]])
    else:
        raise ValueError('axis should in range')
    new_points = np.einsum('aij,jka->aik', points, rot_mat_T)
    return new_points


def center_to_corner_box3d(centers, dims, angles=None, origin=None, axis=1):
    corners = corners_nd(dims, origin=origin)
    # corners: [N, 8, 3]
    if angles is not None:
        corners = rotation_3d_in_axis(corners, angles, axis=axis)
    corners += centers.reshape([-1, 1, 3])
    for i in range(len(corners)):
        z_h = max(corners[i, :, -1])
        z_0 = min(corners[i, :, -1])
        z_max = z_h - (z_h - z_0) / 2
        z_min = z_0 - (z_h - z_0) / 2
        corners[i, [0, 3, 4, 7], -1] = z_min
        corners[i, [1, 2, 5, 6], -1] = z_max
    return corners


def corner_to_surfaces_3d(corners):
    surfaces1 = np.array([
        [corners[:, 0], corners[:, 1], corners[:, 2], corners[:, 3]],
        [corners[:, 7], corners[:, 6], corners[:, 5], corners[:, 4]],
        [corners[:, 0], corners[:, 3], corners[:, 7], corners[:, 4]],
        [corners[:, 1], corners[:, 5], corners[:, 6], corners[:, 2]],
        [corners[:, 0], corners[:, 4], corners[:, 5], corners[:, 1]],
        [corners[:, 3], corners[:, 2], corners[:, 6], corners[:, 7]],
    ])
    surfaces = surfaces1.transpose([2, 0, 1, 3])
    return surfaces


def surface_equ_3d(polygon_surfaces):
    surface_vec = polygon_surfaces[:, :, :2, :] - \
                  polygon_surfaces[:, :, 1:3, :]
    normal_vec = np.cross(surface_vec[:, :, 0, :], surface_vec[:, :, 1, :])
    d = np.einsum('aij, aij->ai', normal_vec, polygon_surfaces[:, :, 0, :])
    return normal_vec, -d


def points_in_convex_polygon_3d_jit(points,
                                    polygon_surfaces,
                                    num_surfaces=None):
    num_polygons = polygon_surfaces.shape[0]  ##目标框个数
    if num_surfaces is None:
        num_surfaces = np.full((num_polygons,), 9999999, dtype=np.int64)
    normal_vec, d = surface_equ_3d(polygon_surfaces[:, :, :3, :])  ##求面的法向量
    return _points_in_convex_polygon_3d_jit(points, polygon_surfaces,
                                            normal_vec, d, num_surfaces)  ##根据长方体内部点与面的法向量之间的关系求得在目标框内部的点


@numba.njit
def _points_in_convex_polygon_3d_jit(points, polygon_surfaces, normal_vec, d,
                                     num_surfaces):
    ##polygon_surfaces：N个目标框的面，每个框6个面
    ## polygon_surfaces.shape[1:3] 一个长方体6个面 每个面4个点
    max_num_surfaces, max_num_points_of_surface = polygon_surfaces.shape[1:3]
    num_points = points.shape[0]
    num_polygons = polygon_surfaces.shape[0]
    ret = np.ones((num_points, num_polygons), dtype=np.bool_)
    sign = 0.0
    for i in range(num_points):
        for j in range(num_polygons):
            for k in range(max_num_surfaces):
                if k > num_surfaces[j]:
                    break
                sign = (
                        points[i, 0] * normal_vec[j, k, 0] +
                        points[i, 1] * normal_vec[j, k, 1] +
                        points[i, 2] * normal_vec[j, k, 2] + d[j, k])
                if sign >= 0:
                    ret[i, j] = False
                    break
    return ret


def points_in_rbbox(points, gt_boxes):
    axis = 2
    origin = (0.5, 0.5, 0)
    rbbox_corners = center_to_corner_box3d(
        gt_boxes[:, :3], gt_boxes[:, 3:6], gt_boxes[:, 6], origin=origin, axis=axis)  ##由中心点左边及长宽高计算出长方体角点
    surfaces = corner_to_surfaces_3d(rbbox_corners)
    indices = points_in_convex_polygon_3d_jit(points[:, :3], surfaces)  ##计算长方体面内点的个数
    return indices

def yuanduan_boxes_to_csv(csv_path, list):
    with open(csv_path, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(list)

def yuanduan_points_to_csv(csv_path, yuanduan_points, n):
    point_path = csv_path + str(n) +'_60.csv'
    with open(point_path, 'a+') as f:
        writer = csv.writer(f)
        writer.writerows(yuanduan_points)

if __name__ == "__main__":
    root_path = '/media/wanji/lijingyang/马冰隧道数据/mabing_csv_all'
    root_path1 = '/media/wanji/lijingyang/马冰隧道数据/'
    root_path_DataAug = '/media/wanji/lijingyang/马冰隧道数据/'
    csv_path = os.path.join(root_path, 'mabing_csv')  ##csv格式标签所在文件夹
    pcd_path = os.path.join(root_path1, 'mabing_pcd')  ##pcd格式的激光雷达数据所在文件夹

    csv_files = os.listdir(csv_path)
    pcd_files = os.listdir(pcd_path)
    csv_files.sort()
    pcd_files.sort()
    yuanduan_boxes = []
    yuanduan_points = []
    for csv_file in tqdm(csv_files):
        pcd_file = pcd_path + '/' + csv_file.split('.')[0] + '.pcd'
        infos = create_data_infos(csv_file, pcd_file)
        points = infos['points']
        gt_boxes = infos['gt_boxes']
        gt_boxes_all = infos['gt_boxes_all']
        num_obj = gt_boxes.shape[0]
        point_indices = points_in_rbbox(points, gt_boxes)
        for i in range(num_obj):
            gt_points = points[point_indices[:, i]]
            if gt_boxes[i,0] > 60 and gt_boxes[i,0] < 80:
                #gt_points[:, :3] -= gt_boxes[i, :3]
                yuanduan_boxes.append(gt_boxes_all[i])
                yuanduan_points.append(gt_points)


    yuanduan_boxes_to_csv('/media/wanji/lijingyang/马冰隧道数据/mabing_yuanduan_boxes_60_80.csv', yuanduan_boxes)
    n = 0
    for yuanduan_points in yuanduan_points:
        yuanduan_points_to_csv('/media/wanji/lijingyang/马冰隧道数据/mabing_yuanduan_points_60_80/', yuanduan_points,  n)
        n = n + 1
