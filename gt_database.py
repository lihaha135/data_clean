from PIL import Image
import numpy as np
import csv
import os
from tqdm import tqdm


def draw_gt(root_path_bin, root_path_csv,  save_root_path):
    labelfiles = os.listdir(root_path_csv)
    for file in tqdm(labelfiles):
         with open(root_path_csv + '/' + file, 'r') as f:
            reader = csv.reader(f)
            index = 0
            for i in reader:
                # print(i)
                csv_gt = i
                points2 = []
                xl = float(i[2]) / 100 - float(i[7]) / 200 - 0.5
                xr = float(i[2]) / 100 + float(i[7]) / 200 + 0.5
                yl = float(i[3]) / 100 - float(i[8]) / 200 - 0.5
                yr = float(i[3]) / 100 + float(i[8]) / 200 + 0.5
                zl = float(i[4]) / 100 - float(i[9]) / 200
                zr = float(i[4]) / 100 + float(i[9]) / 200
                path_bin = root_path_bin + '/' + file.split('.')[0] + '.bin'
                points1 = np.fromfile(path_bin, dtype=np.float32, count=-1).reshape((-1, 4))
                for j in points1:
                    if j[0]>xl and j[0]<xr and j[1]>yl and j[1]<yr and j[2]>zl and j[2] < zr:
                            points2.append(j)
                img_size_x = int(abs(xr-xl)*10 + 5)
                img_size_y = int(abs(yr-yl)*10 + 5)
                img = Image.new('RGB', (img_size_x, img_size_y), 'black')
                points2 = np.array(points2)
                point_num = points2.shape[0]
                if point_num == 0:
                    no_data_path = save_root_path + '/' + 'no_data.txt'

                    no_data_file = open(no_data_path , 'a+')
                    file_rename = file
                    csv_gt_rename = csv_gt
                    ll = str(file_rename) +':' + str(csv_gt_rename) + ':there is no data' + '\n'
                    no_data_file.write(ll)
                    no_data_file.close()
                for i in range(point_num):
                    tempx = (points2[i, 0] - xl)*10
                    tempy = (points2[i, 1] - yl)*10
                    img.putpixel((int(tempx), int(tempy)), (255, 255, 0))
                save_path = save_root_path + '/' + csv_gt[1]
                if os.path.exists(save_path) is False:
                    os.makedirs(save_path)
                save_png_path = save_path + '/' + file.split('.')[0] + '-' + str(index) + '-(' + str(int(float(csv_gt[2]))) + '_' + str(int(float(csv_gt[3]))) + '_' + str(int(float(csv_gt[4])))+ ')-(' + str(int(float(csv_gt[7]))) + '_'+str(int(float(csv_gt[8]))) + '_' +str(int(float(csv_gt[9]))) + ').png'
                img.save(save_png_path)
                index = index + 1


root_path_bin = '/media/wanji/lijingyang/马冰隧道数据/mabing_bin'
root_path_csv = '/media/wanji/lijingyang/马冰隧道数据/mabing_csv_all/mabing_csv'
save_root_path = '/media/wanji/lijingyang/马冰隧道数据/gt_database'
draw_gt(root_path_bin, root_path_csv, save_root_path)