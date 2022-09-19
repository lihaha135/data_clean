from PIL import Image
import numpy as np
import csv
import os
from tqdm import tqdm
import time




def merge_class(root_path, labeltype, label, change_label, save_path):
    csv_path = root_path + 'train_sets/' + 'point_data_label/'
    labelfiles = os.listdir(csv_path)
    for file in tqdm(labelfiles):
        new_data = []
        file_path = csv_path + file
        save_file_path = save_path + file
        with open(file_path, 'r') as f:
            reader = csv.reader(f)
            for i in reader:
                label_index = label.index(i[1])
                i[1] = change_label[label_index]
                new_data.append(i)
        with open(save_file_path, 'a+') as f:
            for i in new_data:
                wf = csv.writer(f)
                wf.writerow(i)





root_path = '/media/wanji/lijingyang/隧道点云数据解密版/GZ-3D-sig-tunnel-rain-20210604/'
save_path = '/media/wanji/lijingyang/隧道点云数据解密版/merge_class_label/'
if os.path.exists(save_path) is False:
    os.makedirs(save_path)
labeltype = '2'
if labeltype == '1':
    label = ['1','0','2','10','3','4','5','11','6','7','9','12','8']
else:
    label = ['1','0','2','4','5','6','8','11','22','10','13','23','12']
change_label = ['0','1','2','3','4','5','6','7','8','9','10','11','12']
merge_class(root_path, labeltype, label, change_label, save_path)