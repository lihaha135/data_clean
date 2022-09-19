import os
import numpy as np
import csv
import random
import math
PI_rads = math.pi / 180

def corners_nd(dims, origin):
    ndim = int(dims.shape[1])
    corners_norm = np.stack(
        np.unravel_index(np.arange(2 ** ndim), [2] * ndim),
        axis=1).astype(dims.dtype)
    if ndim == 2:
        corners_norm = corners_norm[[0, 1, 3, 2]]
    elif ndim == 3:
        corners_norm = corners_norm[[0, 1, 3, 2, 4, 5, 7, 6]]
    corners_norm = corners_norm - np.array(origin, dtype=dims.dtype)
    corners = dims.reshape([-1, 1, ndim]) * corners_norm.reshape(
        [1, 2 ** ndim, ndim])
    return corners

def rotation_3d_in_axis(points, angles, axis=0):
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

def create_data_infos(gt_boxs_csv_path):
    infos = {}
    gt_boxes = []
    with open(gt_boxs_csv_path, 'r') as f:
        reader = csv.reader(f)
        for i in reader:
            if int(i[1]) == 1:
                continue
            gt_boxes.append(
                [float(i[2]) / 100, float(i[3]) / 100, float(i[4]) / 100, float(i[7]) / 100, float(i[8]) / 100,
                 float(i[9]) / 100, float(i[6]) * PI_rads])  ##依次为x,y,z,l,w,h,angle，单位为厘米和角度，请对照自己的标签格式自行修改
    gt_boxes = np.array(gt_boxes)
    infos['gt_boxes'] = gt_boxes
    return infos

def iou(orgs, gt):
    iou_list = []
    orgs = orgs.tolist()
    gt = gt.tolist()[0]
    for org in orgs:
        area_a = (org[1][0] - org[5][0]) * (org[5][1] - org[6][1])
        area_b = (gt[1][0] - gt[5][0]) * (gt[5][1] - gt[6][1])

        iou_x1 = np.maximum(org[5][0], gt[5][0])        # get left top x of IoU
        iou_y1 = np.minimum(org[5][1], gt[5][1])        # get left top y of IoU
        iou_x2 = np.minimum(org[2][0], gt[2][0])        # get right bottom of IoU
        iou_y2 = np.maximum(org[2][1], gt[2][1])        # get right bottom of IoU
        iou_w = iou_x2 - iou_x1
        iou_h = iou_y1 - iou_y2
        if iou_w < 0:
            iou_w = 0
        if iou_h < 0:
            iou_h = 0

        area_iou = iou_w * iou_h    # get area of IoU
        iou = area_iou / (area_a + area_b - area_iou)    # get overlap ratio between IoU and all area
        iou_list.append(iou)

    return iou_list

def add_boxes(yuanduan_label, points):
    gt_boxes = []
    gt_lines = []
    gt_point_csv_num = random.randint(0, 1823)  # 随机生成选取gt
    gt_point_csv_path = pcd_path + str(gt_point_csv_num) + '_60.csv'  # 选取gt point的地址
    org_boxs_csv_path = root_label_path  # 增强的帧的标注文档地址
    with open(gt_point_csv_path, 'r') as f:  # 增强的目标
        reader = csv.reader(f)
        for line in reader:
            gt_lines.append(line)
    axis = 2
    origin = (0.5, 0.5, 0)

    # 原始数据csv角点信息
    org_infos = create_data_infos(org_boxs_csv_path)
    org_boxes = org_infos['gt_boxes']
    org_rbbox_corners = center_to_corner_box3d(
        org_boxes[:, :3], org_boxes[:, 3:6], org_boxes[:, 6], origin=origin, axis=axis)

    # 添加的目标csv角点信息
    gt_infos = create_data_infos(org_boxs_csv_path)
    i = yuanduan_label[gt_point_csv_num]
    gt_boxes.append(
        [float(i[2]) / 100, float(i[3]) / 100, float(i[4]) / 100, float(i[7]) / 100, float(i[8]) / 100,
         float(i[9]) / 100, float(i[6]) * PI_rads])
    gt_boxes = np.array(gt_boxes)
    gt_rbbox_corners = center_to_corner_box3d(
        gt_boxes[:, :3], gt_boxes[:, 3:6], gt_boxes[:, 6], origin=origin, axis=axis)
    # 计算IOU
    iou_list = iou(org_rbbox_corners, gt_rbbox_corners)
    iou_bol_list = []
    for i in iou_list:
        if i == 0:
            iou_bol_list.append(True)
        else:
            iou_bol_list.append(False)
    while False in iou_bol_list:
        gt_boxes = gt_boxes.tolist()
        gt_boxes[0][0] = gt_boxes[0][0] + 4
        for gt_line in gt_lines:
            gt_line[0] = float(gt_line[0]) + 4
            gt_line[0] = str(gt_line[0])
        gt_boxes = np.array(gt_boxes)
        gt_rbbox_corners = center_to_corner_box3d(
            gt_boxes[:, :3], gt_boxes[:, 3:6], gt_boxes[:, 6], origin=origin, axis=axis)
        iou_list = iou(org_rbbox_corners, gt_rbbox_corners)
        iou_bol_list.clear()
        for i in iou_list:
            if i == 0:
                iou_bol_list.append(True)
            else:
                iou_bol_list.append(False)

    org_boxes = org_boxes.tolist()
    gt_boxes = gt_boxes.tolist()
    org_boxes.append(gt_boxes[0])
    for line in gt_lines:
        points.append(line)
    # 保存csv
    with open(root_label_path, 'a+') as f:
        wf = csv.writer(f)
        add_gt = yuanduan_label[gt_point_csv_num]
        add_gt[2] = str(gt_boxes[0][0] * 100)
        wf.writerow(add_gt)

    return points

def main(root_point_path, root_label_path, csv_path, pcd_path, save_bin_path, save_label_path):

    yuanduan_label = []
    points = []

    with open(csv_path, 'r') as f:  # 加载所有远端目标的点云
        reader = csv.reader(f)
        for i in reader:
            yuanduan_label.append(i)

    with open(root_point_path, 'r') as f:  # 将远端点云目标的点放入帧中
        for line in f.readlines()[11:len(f.readlines())-1]:
            strs = line.split(' ')
            if len(strs[0]) < 0:
                continue
            points.append([float(strs[0]),float(strs[1]),float(strs[2]),float(strs[3].strip())])

        for num_gt in range(3):
            points = add_boxes(yuanduan_label, points)
        p = np.array(points, dtype=np.float32)
        print(p.shape)
        p.tofile(save_bin_path)


if __name__ == '__main__':
    root_point_path = '/media/wanji/lijingyang/数据增强文件/20210604_3D_tr_pec_sig_tun0001_ran_01601.pcd'
    root_label_path = '/media/wanji/lijingyang/数据增强文件/20210604_3D_tr_pec_sig_tun0001_ran_01601.csv'
    csv_path = '/media/wanji/lijingyang/数据增强文件/yuanduan_boxes_60.csv'
    pcd_path = '/media/wanji/lijingyang/数据增强文件/yuanduan_points_60/'

    save_bin_path = '/media/wanji/lijingyang/数据增强文件/20210604_3D_tr_pec_sig_tun0001_ran_01601.bin'
    save_label_path = '/media/wanji/lijingyang/数据增强文件/20210604_3D_tr_pec_sig_tun0001_sun_00002_yuanduan.csv'
    main(root_point_path, root_label_path, csv_path, pcd_path, save_bin_path, save_label_path)