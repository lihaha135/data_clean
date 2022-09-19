from PIL import Image
import numpy as np
import csv
import os
from tqdm import tqdm
import matplotlib.pyplot as plt
import numpy as np
import time
import cv2
import math
import add_boxes
from add_boxes import center_to_corner_box3d, rotation_3d_in_axis


def draw_2D(root_path_bin, root_path_csv,  save_root_path):
    labelfiles = os.listdir(root_path_bin)
    for file in tqdm(labelfiles):
        path_bin = root_path_bin + file
        points1 = np.fromfile(path_bin, dtype=np.float32, count=-1).reshape((-1, 3))
        w = 2600
        h = 700
        img = np.zeros((h, w, 3))

        for point in points1:
            tempx = round(point[0] * 10)
            tempy = round(point[1] * 10)
            tempx = int(tempx + 1300)
            tempy = int(tempy + 350)
            cv2.circle(img, (tempx, tempy), 1, (255, 255, 255), thickness=-1)
        # cv2.namedWindow("1",0)
        # cv2.imshow('1',img)
        # cv2.waitKey()
        bev_corner_all = []
        with open(root_path_csv,'r') as f:
            reader = csv.reader(f)
            n = 0
            corners_all = []
            file_num = file.split('.')[0].split('_')[-1]
            for i in reader:
                if i[2] == file_num and i[3] not in ['42', '90', '197', '208', '601']:
                    gt_boxes = []
                    PI_rads = math.pi / 180
                    gt_boxes.append(
                        [float(i[4]) * 10, float(i[5]) * 10, float(i[6]) * 10, float(i[8]) * 10, float(i[7]) * 10,
                         float(i[9]) * 10, float(i[11]) * PI_rads - math.pi / 2.5])
                    axis = 2
                    origin = (0.5, 0.5, 0)
                    gt_boxes = np.array(gt_boxes)
                    org_rbbox_corners = center_to_corner_box3d(
                        gt_boxes[:, :3], gt_boxes[:, 3:6], gt_boxes[:, 6], origin=origin, axis=axis)
                    corners_all.append(org_rbbox_corners[0])

            for i in corners_all:
                bev_corner = []
                bev_corner.append(i[6][0:2])
                bev_corner.append(i[5][0:2])
                bev_corner.append(i[2][0:2])
                bev_corner.append(i[1][0:2])
                bev_corner_all.append(bev_corner)
            green = (0, 255, 0)
            for i in range(len(bev_corner_all)):
                for ii in range(len(bev_corner_all[i])):
                    bev_corner_all[i][ii][0] = int(float(bev_corner_all[i][ii][0])) + 1300
                    bev_corner_all[i][ii][1] = int(float(bev_corner_all[i][ii][1])) + 350
            # bev_corner = np.array(bev_corner).astype(int)
            print((tuple(bev_corner[0])))
            for bev_corner in bev_corner_all:
                bev_corner = np.array(bev_corner).astype(int)
                cv2.line(img, tuple(bev_corner[0]), tuple(bev_corner[1]), green, 2)
                cv2.line(img, tuple(bev_corner[1]), tuple(bev_corner[3]), green, 2)
                cv2.line(img, tuple(bev_corner[3]), tuple(bev_corner[2]), green, 2)
                cv2.line(img, tuple(bev_corner[2]), tuple(bev_corner[0]), green, 2)
            # cv2.namedWindow("1", 0)
            # cv2.imshow('1', img)
            # cv2.waitKey()
            save_path = save_root_path + file_num + '.jpg'
            cv2.imwrite(save_path, img)


root_path_bin = '/media/wanji/lijingyang/data_cleaning/bin/'
root_path_csv = '/media/wanji/lijingyang/data_cleaning/box_su/AllPcBoxInfo.csv'
save_root_path = '/media/wanji/lijingyang/data_cleaning/2d_su/'
draw_2D(root_path_bin, root_path_csv, save_root_path)