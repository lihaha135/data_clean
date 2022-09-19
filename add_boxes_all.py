import os
import numpy as np
import csv
import random
import math
from tqdm import tqdm
import copy
PI_rads = math.pi / 180

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
    corners = corners_nd(dims, origin=origin)    # corners: [N, 8, 3]
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
    # gt_boxes_all = []
    # points = []
    # label_fpath = os.path.join(csv_path, labelfile)
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
        # get area of b
        area_b = (gt[1][0] - gt[5][0]) * (gt[5][1] - gt[6][1])

        # get left top x of IoU
        iou_x1 = np.maximum(org[5][0], gt[5][0])
        # get left top y of IoU
        iou_y1 = np.minimum(org[5][1], gt[5][1])
        # get right bottom of IoU
        iou_x2 = np.minimum(org[2][0], gt[2][0])
        # get right bottom of IoU
        iou_y2 = np.maximum(org[2][1], gt[2][1])
        iou_w = iou_x2 - iou_x1
        iou_h = iou_y1 - iou_y2
        if iou_w < 0:
            iou_w = 0
        if iou_h < 0:
            iou_h = 0
        # get width of IoU
        # iou_w = iou_x2 - iou_x1
        # # get height of IoU
        # iou_h = iou_y2 - iou_y1

        # get area of IoU
        area_iou = iou_w * iou_h
        # get overlap ratio between IoU and all area
        iou = area_iou / (area_a + area_b - area_iou)
        iou_list.append(iou)

    return iou_list


def calulate_corners(org_boxs_csv_path):
    axis = 2
    origin = (0.5, 0.5, 0)
    gt_boxes = []

    # 原始数据csv角点信息
    org_infos = create_data_infos(org_boxs_csv_path)
    org_boxes = org_infos['gt_boxes']
    org_rbbox_corners = center_to_corner_box3d(org_boxes[:, :3], org_boxes[:, 3:6], org_boxes[:, 6], origin=origin, axis=axis)
    # 添加的目标csv角点信息
    gt_infos = create_data_infos(org_boxs_csv_path)
    i = yuanduan_label[gt_point_csv_num]
    gt_boxes.append(
        [float(i[2]) / 100, float(i[3]) / 100, float(i[4]) / 100, float(i[7]) / 100, float(i[8]) / 100,
         float(i[9]) / 100, float(i[6]) * PI_rads])
    gt_boxes = np.array(gt_boxes)
    gt_rbbox_corners = center_to_corner_box3d(gt_boxes[:, :3], gt_boxes[:, 3:6], gt_boxes[:, 6], origin=origin, axis=axis)

    return gt_boxes, org_rbbox_corners, gt_rbbox_corners, org_boxes

root_point_path = '/media/wanji/lijingyang/鄂州项目数据集/马冰隧道/mabing_pcd/'
root_label_path = '/media/wanji/lijingyang/鄂州项目数据集/马冰隧道/mabing_csv_aug/'
csv_path = '/media/wanji/lijingyang/马冰隧道数据/mabing_yuanduan_boxes_60_80.csv'
pcd_path = '/media/wanji/lijingyang/马冰隧道数据/mabing_yuanduan_points_60_80/'
save_bin_path = '/media/wanji/lijingyang/鄂州项目数据集/马冰隧道/mabing_bin_aug/'
save_txt_path = '/media/wanji/lijingyang/鄂州项目数据集/马冰隧道/mabing_txt_aug/'

labelfiles = os.listdir(root_label_path)
yuanduan_label = []
for labelfile in tqdm(labelfiles):
    ################# 加载所有远端目标的标签 ###################
    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        for i in reader:
            yuanduan_label.append(i)

    ################## 将远端点云目标的点放入帧中 ##################
    point_path = root_point_path + labelfile.split('.')[0] + '.pcd'  # 加载原始数据的点
    points = []
    with open(point_path, 'r') as f:
        for line in f.readlines()[11:len(f.readlines())-1]:
              strs = line.split(' ')
              if len(strs[0]) < 0:
                  continue
              points.append([float(strs[0]),float(strs[1]),float(strs[2]),float(strs[3].strip())])

        for num_gt in range(3):
            gt_lines = []
            gt_point_csv_num = random.randint(0, 1823)   # 随机生成选取gt
            gt_point_csv_path = pcd_path + str(gt_point_csv_num) + '_60.csv'  # 选取gt point的地址
            org_boxs_csv_path = root_label_path + labelfile  # 增强的帧的标注文档地址
            with open(gt_point_csv_path, 'r') as f:  # 增强的目标
                reader = csv.reader(f)
                for line in reader:
                    gt_lines.append(line)

            gt_boxes, org_rbbox_corners, gt_rbbox_corners, org_boxes = calulate_corners(org_boxs_csv_path)
            # 计算IOU
            iou_list = iou(org_rbbox_corners, gt_rbbox_corners)
            iou_bol_list = []
            [iou_bol_list.append(True) if i == 0 else iou_bol_list.append(False) for i in iou_list]

            while False in iou_bol_list:
                gt_boxes = gt_boxes.tolist()
                gt_boxes[0][0] = gt_boxes[0][0] + 2
                for num_point in range(len(gt_lines)):
                     pp = float(gt_lines[num_point][0]) + 2
                     gt_lines[num_point][0] = str(pp)
                gt_boxes = np.array(gt_boxes)
                gt_rbbox_corners = center_to_corner_box3d(
                    gt_boxes[:, :3], gt_boxes[:, 3:6], gt_boxes[:, 6], origin=(0.5, 0.5, 0), axis=2)
                iou_list = iou(org_rbbox_corners, gt_rbbox_corners)
                iou_bol_list.clear()
                [iou_bol_list.append(True) if i == 0 else iou_bol_list.append(False) for i in iou_list]


            org_boxes = org_boxes.tolist()
            gt_boxes = gt_boxes.tolist()
            org_boxes.append(gt_boxes[0])
            for line in gt_lines:
                points.append(line)

            #保存csv
            with open(org_boxs_csv_path, 'a+') as f:
                wf = csv.writer(f)
                add_gt = copy.deepcopy(yuanduan_label[gt_point_csv_num])
                add_gt[2] = str(gt_boxes[0][0] * 100)
                wf.writerow(add_gt)


    p = np.array(points, dtype=np.float32)
    if os.path.exists(save_bin_path) is False:
        os.makedirs(save_bin_path)
    p.tofile(save_bin_path + labelfile.split('.')[0] + '.bin')

    if os.path.exists(save_txt_path) is False:
        os.makedirs(save_txt_path)
    save_txt = save_txt_path + labelfile.split('.')[0] + '.txt'
    with open(save_txt, 'a+') as f:
        for ii in p:
            wf = csv.writer(f)
            wf.writerow(ii)
