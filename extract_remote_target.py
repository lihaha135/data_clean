import os
import random
import numpy as np
import math
import csv
import copy
from tqdm import tqdm
PI_rads = math.pi / 180
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


def compute_iou(rec1, rec2):
    """
    computing IoU
    :param rec1: (y0, x0, y1, x1), which reflects
            (top, left, bottom, right)
    :param rec2: (y0, x0, y1, x1)
    :return: scala value of IoU
    """
    # computing area of each rectangles
    S_rec1 = abs((rec1[1][0] - rec1[0][0]) * (rec1[1][1] - rec1[0][1]))
    S_rec2 = abs((rec2[1][0] - rec2[0][0]) * (rec2[1][1] - rec2[0][1]))

    # computing the sum_area
    sum_area = S_rec1 + S_rec2

    # find the each edge of intersect rectangle
    left_line = max(rec1[0][0], rec2[0][0])
    right_line = min(rec1[1][0], rec2[1][0])
    top_line = min(rec1[0][1], rec2[0][1])
    bottom_line = max(rec1[1][1], rec2[1][1])

    # judge if there is an intersect
    if left_line >= right_line or top_line <= bottom_line:
        return 0
    else:
        intersect = (right_line - left_line) * (bottom_line - top_line)
        return (intersect / (sum_area - intersect)) * 1.0

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

def add_box_point(pcd_path, csv_path, points_all, csv_all, root_path, pcd_name):
    points = []
    et_boxes_all = []
    with open(pcd_path) as f:
        for line in f.readlines()[11:len(f.readlines()) - 1]:
            strs = line.split(' ')
            if len(strs[0]) < 0:
                continue
            points.append([float(strs[0]), float(strs[1]), float(strs[2]), float(strs[3].strip())])
    for i in range(2):
        enhancement_target_num = random.randint(0, 5096)
        enhancement_target_csv = copy.deepcopy(csv_all[enhancement_target_num])
        enhancement_target_points = copy.deepcopy(points_all[enhancement_target_num])
        axis = 2
        origin = (0.5, 0.5, 0)
        with open(csv_path) as f:
            reader = csv.reader(f)
            gt_boxes = []
            for line in reader:
                gt_boxes.append(
                    [float(line[2]) / 100, float(line[3]) / 100, float(line[4]) / 100, float(line[7]) / 100, float(line[8]) / 100,
                     float(line[9]) / 100, float(line[6]) * PI_rads])
            gt_boxes = np.array(gt_boxes)
            gt_rbbox_corners = center_to_corner_box3d(gt_boxes[:, :3], gt_boxes[:, 3:6], gt_boxes[:, 6], origin=origin, axis=axis)

        et_boxes = []
        et_boxes.append(
            [float(enhancement_target_csv[2]) / 100, float(enhancement_target_csv[3]) / 100, float(enhancement_target_csv[4]) / 100, float(enhancement_target_csv[7]) / 100,
             float(enhancement_target_csv[8]) / 100, float(enhancement_target_csv[9]) / 100, float(enhancement_target_csv[6]) * PI_rads])
        et_boxes = np.array(et_boxes)
        et_rbbox_corners = center_to_corner_box3d(et_boxes[:, :3], et_boxes[:, 3:6], et_boxes[:, 6], origin=origin,
                                                  axis=axis)

        iou_list = []
        for j in gt_rbbox_corners:
            rect1, rect2 = [], []
            rect1.append(j[5][:2])
            rect1.append(j[2][:2])
            rect2.append(et_rbbox_corners[0][5][:2])
            rect2.append(et_rbbox_corners[0][2][:2])
            iou = compute_iou(rect1, rect2)
            if iou == 0:
                iou_list.append(False)
            else:
                iou_list.append(True)

        while True in iou_list :
            iou_list.clear()
            et_boxes[0][0] = et_boxes[0][0] + 6
            for ll in range(len(enhancement_target_points)):
                enhancement_target_points[ll][0] = enhancement_target_points[ll][0] + 6
            et_rbbox_corners = center_to_corner_box3d(et_boxes[:, :3], et_boxes[:, 3:6], et_boxes[:, 6], origin=origin, axis=axis)
            for j in gt_rbbox_corners:
                rect1, rect2 = [], []
                rect1.append(j[5][:2])
                rect1.append(j[2][:2])
                rect2.append(et_rbbox_corners[0][5][:2])
                rect2.append(et_rbbox_corners[0][2][:2])
                iou = compute_iou(rect1, rect2)
                if iou == 0 :
                    iou_list.append(False)
                else:
                    iou_list.append(True)
        with open(csv_path, 'a+') as f:
            write = csv.writer(f)  # 创建writer对象
            enhancement_target_csv[2] = str((et_boxes[0][0])*100)
            write.writerow(enhancement_target_csv)
        for rr in enhancement_target_points:
            points.append(rr)
    #p = np.array(points, dtype=np.float32)
    save_path = root_path + pcd_name.split('.')[0] + '.txt'
    with open(save_path, 'a+') as fi:
        for point in points:
            point = str(point) + '\n'
            fi.write(point)


def add_far_target(yuanduan_pcd_path, yuanduan_csv_path, pcds_path, csvs_path, root_path):
    yuanduan_pcd = os.listdir(yuanduan_pcd_path)
    yuanduan_pcd.sort(key=lambda x:int(x.split('.')[0].split('_')[0]))
    points_all = []
    for i in yuanduan_pcd:
        points = []
        pcd_filename = yuanduan_pcd_path + '/' +  i
        with open(pcd_filename) as f:
            for line in f.readlines():
                strs = line.split(",")
                points.append([float(strs[0]),float(strs[1]),float(strs[2]),float(strs[3])])
        points_all.append(points)

    csv_all = []
    with open(yuanduan_csv_path) as f:
        reader = csv.reader(f)
        for line in reader:
            csv_all.append(line)

    pcd_list = os.listdir(pcds_path)
    for pcd_name in tqdm(pcd_list):
        pcd_path = pcds_path + '/' + pcd_name
        csv_path = csvs_path + '/' + pcd_name.split('.')[0] + '.csv'
        add_box_point(pcd_path, csv_path, points_all, csv_all, root_path, pcd_name)


yuanduan_pcd_path = '/media/wanji/lijingyang/马冰隧道数据/mabing_yuanduan_points_60_80'
yuanduan_csv_path = '/media/wanji/lijingyang/马冰隧道数据/mabing_yuanduan_boxes_60_80.csv'
pcds_path = '/media/wanji/lijingyang/马冰隧道数据/mabing_pcd'

csvs_path = '/media/wanji/lijingyang/马冰隧道数据/mabing_60_80/mabing_csv_类别过滤_数据增强_60_80'
root_path = '/media/wanji/lijingyang/马冰隧道数据/mabing_60_80/mabing_pcd_txt_60_80/'

add_far_target(yuanduan_pcd_path, yuanduan_csv_path, pcds_path, csvs_path, root_path)







































































































