import numpy as np
import math
import visualize_utils as V
import mayavi.mlab as mlab
import os
from tqdm import tqdm
import struct

def fused_crop_back(img_small, img_big, PC_data, grid_size_small, grid_size_big, thresh_small, thresh_big, h_thresh_x,
                    h_thresh_y, dis_thresh):
    grid_small_inv = 1 / grid_size_small
    im_size_small = round(200 * grid_small_inv)

    grid_big_inv = 1 / grid_size_big

    min_x, min_y = -100, -100
    point_num = PC_data.shape[0]
    in_points = np.zeros((point_num, 4))
    out_points = np.zeros((point_num, 4))
    count_in = 0
    count_out = 0
    if point_num == 0:
        print('there is no data')

    for i in range(point_num):
        temppoint = PC_data[i]
        tempx_small = math.floor((PC_data[i, 0] - min_x) * grid_small_inv)
        tempy_small = math.floor((PC_data[i, 1] - min_y) * grid_small_inv)

        tempx_big = math.floor((PC_data[i, 0] - min_x) * grid_big_inv)
        tempy_big = math.floor((PC_data[i, 1] - min_y) * grid_big_inv)

        if (tempx_small > im_size_small - 1) or (tempx_small < 0) or (tempy_small > im_size_small - 1) or (
                tempy_small < 0):
            continue
        elif (PC_data[i][2] - img_small[tempx_small, tempy_small, 3]) > thresh_small:
            in_points[count_in, :] = temppoint
            count_in += 1
        # elif abs(PC_data[i][0]) > 50 or abs(PC_data[i][1]) > 50:
        #     if ((PC_data[i][2] - img_big[tempx_big, tempy_big, 3]) > h_thresh):
        #         in_points[count_in, :] = temppoint
        #         count_in += 1
        #     else:
        #         out_points[count_out, :] = temppoint
        #         count_out += 1
        elif abs(PC_data[i][0]) < dis_thresh and abs(PC_data[i][1]) < dis_thresh:
            if ((PC_data[i][2] - img_big[tempx_big, tempy_big, 3]) > thresh_big):
                in_points[count_in, :] = temppoint
                count_in += 1
            else:
                out_points[count_out, :] = temppoint
                count_out += 1
        elif (abs(PC_data[i][0]) > dis_thresh):
            if PC_data[i][2] > h_thresh_x:
                in_points[count_in, :] = temppoint
                count_in += 1
            else:
                out_points[count_out, :] = temppoint
                count_out += 1
        elif (abs(PC_data[i][1]) > dis_thresh):
            if PC_data[i][2] > h_thresh_y:
                in_points[count_in, :] = temppoint
                count_in += 1
            else:
                out_points[count_out, :] = temppoint
                count_out += 1
        else:
            out_points[count_out, :] = temppoint
            count_out += 1
    in_points = in_points[:count_in, :]
    out_points = out_points[:count_out, :]
    # print('filter number: ')
    # print(count_in)
    return in_points, out_points

def fused_back(backdata, grid_size_small, grid_size_big):
    grid_small_inv = 1 / grid_size_small
    im_size_small = round(200 * grid_small_inv)

    grid_big_inv = 1 / grid_size_big
    im_size_big = round(200 * grid_big_inv)

    min_x, min_y = -100, -100

    img_small = np.zeros((im_size_small, im_size_small, 4))

    img_big = np.zeros((im_size_big, im_size_big, 4))

    # backdata = backdata[backdata[:, 2]>-5.5]
    point_num = backdata.shape[0]
    if point_num == 0:
        print('there is no data')
    for i in range(point_num):
        tempx_small = math.floor((backdata[i, 0] - min_x) * grid_small_inv)
        tempy_small = math.floor((backdata[i, 1] - min_y) * grid_small_inv)

        tempx_big = math.floor((backdata[i, 0] - min_x) * grid_big_inv)
        tempy_big = math.floor((backdata[i, 1] - min_y) * grid_big_inv)

        tempz = backdata[i, 2]
        if (tempx_small > im_size_small - 1) or (tempx_small < 0) or (tempy_small > im_size_small - 1) or (
                tempy_small < 0):
            continue
        elif (tempz < img_small[tempx_small, tempy_small, 3]):
            img_small[tempx_small, tempy_small, 3] = tempz

        elif (tempz < img_big[tempx_big, tempy_big, 3]):
            img_big[tempx_big, tempy_big, 3] = tempz
    return img_small, img_big


######zhu########
# txt_dir = '/media/wanji/lijingyang/马冰隧道数据/mabing_pcd_txt_60_90/'
# save_dir = '/media/wanji/lijingyang/马冰隧道数据/mabing_bin_dimian_60_90/'
txt_dir = '/media/wanji/lijingyang/马冰隧道数据/mabing_60_80/mabing_pcd_txt_60_80/'
save_dir = '/media/wanji/lijingyang/qinhao/qinhao_bin_dimian_60_80/'
if os.path.exists(save_dir):
    pass
else:
    os.makedirs(save_dir)
pcd_list = os.listdir(txt_dir)
for file in tqdm(pcd_list):
    pcd_data = txt_dir + file
    pcd_far_data = []
    # with open(pcd_data) as f:
    #     for line in f.readlines()[11:len(f.readlines()) - 1]:
    #         strs = line.split(' ')
    #         if len(strs[0]) < 0:
    #             continue
    #         pcd_far_data.append([float(strs[0]), float(strs[1]), float(strs[2]), float(strs[3].strip())])
    with open(pcd_data, "r") as f:
        for line in f.readlines():
            strs = line.split(',')
            if len(strs[0]) < 0:
                continue
            pcd_far_data.append([float(strs[0].split('[')[1]), float(strs[1]), float(strs[2])-1.7, float(strs[3].split(']')[0])])
    pcd_far_data = np.array(pcd_far_data)
    img_small, img_big = fused_back(pcd_far_data, 1, 7.0)
    in_points, out_points = fused_crop_back(img_small, img_big, pcd_far_data, 1, 7.0, 0.2, 0.4, -7, -7, 80)
    pp = in_points.tolist()
    p = np.array(pp, dtype=np.float32)
    pcd_dimian_save_dir = save_dir + file.split('.')[0] + '.bin'
    p.tofile(pcd_dimian_save_dir)
    # points1 = np.fromfile(save_path, dtype=np.float32, count=-1).reshape((-1, 4))
    # V.draw_scenes(points = points1)
    # mlab.show(stop=True)
