from PIL import Image
import numpy as np
import csv
import os
from tqdm import tqdm
import time


def draw_2D(root_path_bin, root_path_csv,  save_root_path):
    labelfiles = os.listdir(root_path_csv)
    for file in tqdm(labelfiles):
         print(file)
         path_bin = root_path_bin + '/' + file.split('.')[0] + '.bin'
         points1 = np.fromfile(path_bin, dtype=np.float32, count=-1).reshape((-1, 4))
         img_size_x = 4000
         img_size_y = 1000
         img = Image.new('RGB', (img_size_x, img_size_y), 'black')
         piax = img_size_x//2
         piay = img_size_y//2
         point1_num = points1.shape[0]
         for i in range(point1_num):
             tempx = points1[i, 0]*10 + piax
             tempy = points1[i, 1]*10 + piay
             if tempx <= img_size_x and tempx >= 0 and tempy <= img_size_y and tempy >= 0:
                img.putpixel((int(tempx), int(tempy)), (255, 255, 0))
         with open(root_path_csv + '/' + file, 'r') as f:
            reader = csv.reader(f)
            for i in reader:
                points2 = []
                xl = float(i[2]) / 10 - float(i[7]) / 20
                xr = float(i[2]) / 10 + float(i[7]) / 20
                yl = float(i[3]) / 10 - float(i[8]) / 20
                yr = float(i[3]) / 10 + float(i[8]) / 20
                zl = float(i[4]) / 10 - float(i[9]) / 20
                zr = float(i[4]) / 10 + float(i[9]) / 20
                path_bin = root_path_bin + '/' + file.split('.')[0] + '.bin'
                points1 = (np.fromfile(path_bin, dtype=np.float32, count=-1).reshape((-1, 4)))*10
                for j in points1:
                    if j[0]>xl and j[0]<xr and j[1]>yl and j[1]<yr and j[2]>zl and j[2] < zr:
                            points2.append(j)
                points2 = np.array(points2)
                point_num = points2.shape[0]
                if point_num == 0:
                    print(file + str(i) + ':there is no data')
                for i in range(point_num):
                    tempx = points2[i, 0] + piax
                    tempy = points2[i, 1] + piay
                    img.putpixel((int(tempx), int(tempy)), (255, 0, 0))
                save_path = save_root_path + '/' + 'draw_2D'
                if os.path.exists(save_path) is False:
                    os.makedirs(save_path)
            save_png_path = save_path + '/' + file.split('.')[0] + '.png'
            img.save(save_png_path)

root_path_bin = '/media/wanji/lijingyang/马冰隧道数据/mabing_bin'
root_path_csv = '/media/wanji/lijingyang/马冰隧道数据/mabing_csv_all/mabing_csv/'
save_root_path = '/media/wanji/lijingyang/马冰隧道数据'
draw_2D(root_path_bin, root_path_csv, save_root_path)