from PIL import Image
import numpy as np
import csv
import os
from tqdm import tqdm
import time

def change_to_bigtruck(file,aa,class_num,labeltype):
    if int(aa) > 1000 and int(aa) < 1500:
        file_path = root_path + 'train_sets/' + 'point_data_label/' + file.split('-')[0] + '.csv'
        new_data = []
        with open(file_path, 'r') as f:
            reader = csv.reader(f)
            for i in reader:
                if int(float(i[7])) == int(aa):
                    if labeltype == '1':
                        i[1] = '7'
                    else:
                        i[1] = '10'
                    print(i)
                    new_data.append(i)
                else:
                    new_data.append(i)
        with open(file_path, 'a+') as f:
            f.truncate(0)
            for i in new_data:
                wf = csv.writer(f)
                wf.writerow(i)


def change_to_semitrailer(file,aa,class_num,labeltype):
    if int(aa) > 1500:
        file_path = root_path + 'train_sets/' + 'point_data_label/' + file.split('-')[0] + '.csv'
        new_data = []
        with open(file_path, 'r') as f:
            reader = csv.reader(f)
            for i in reader:
                if int(float(i[7])) == int(aa):
                    if labeltype == '1':
                        i[1] = '9'
                    else:
                        i[1] = '13'
                    print(i)
                    new_data.append(i)
                else:
                    new_data.append(i)
        with open(file_path, 'a+') as f:
            f.truncate(0)
            for i in new_data:
                wf = csv.writer(f)
                wf.writerow(i)


def change_to_smalltruck(file, aa, class_num, labeltype):
    if int(aa) < 700:
        file_path = root_path + 'train_sets/' + 'point_data_label/' + file.split('-')[0] + '.csv'
        new_data = []
        with open(file_path, 'r') as f:
            reader = csv.reader(f)
            for i in reader:
                if int(float(i[7])) == int(aa):
                    i[1] = '11'
                    print(i)
                    new_data.append(i)
                else:
                    new_data.append(i)
        with open(file_path, 'a+') as f:
            f.truncate(0)
            for i in new_data:
                wf = csv.writer(f)
                wf.writerow(i)

def change_to_middletruck(file, aa, class_num, labeltype):
    if int(aa) > 700 and int(aa) < 1000:
        file_path = root_path + 'train_sets/' + 'point_data_label/' + file.split('-')[0] + '.csv'
        new_data = []
        with open(file_path, 'r') as f:
            reader = csv.reader(f)
            for i in reader:
                if int(float(i[7])) == int(aa):
                    if labeltype == '1':
                        i[1] = '6'
                    else:
                        i[1] = '22'
                    print(i)
                    new_data.append(i)
                else:
                    new_data.append(i)
        with open(file_path, 'a+') as f:
            f.truncate(0)
            for i in new_data:
                wf = csv.writer(f)
                wf.writerow(i)


def change_class_truck(root_path,  labeltype, labellist):
    for class_num in labellist:
        gt_pngs = os.listdir(root_path + class_num)
        for file in tqdm(gt_pngs):
            aa = file.split('(')[2].split('_')[0]
            ###################### 中卡车###########################
            if class_num == '602' or class_num == '22':
                change_to_smalltruck(file, aa, class_num, labeltype)
                change_to_bigtruck(file,aa,class_num,labeltype)
                change_to_semitrailer(file,aa,class_num,labeltype)
            ###################### 大卡车###########################
            if class_num == '6011' or  class_num == '10':
                change_to_smalltruck(file, aa, class_num, labeltype)
                change_to_middletruck(file, aa, class_num, labeltype)
                change_to_semitrailer(file, aa, class_num, labeltype)
            ###################### 小卡车###########################
            if class_num == '603':
                change_to_middletruck(file, aa, class_num, labeltype)
                change_to_bigtruck(file, aa, class_num, labeltype)
                change_to_semitrailer(file, aa, class_num, labeltype)
            ###################### 半挂车###########################
            if class_num == '6012' or class_num == '9':
                change_to_smalltruck(file, aa, class_num, labeltype)
                change_to_middletruck(file, aa, class_num, labeltype)
                change_to_bigtruck(file, aa, class_num, labeltype)

def change_class_bus(root_path,  labeltype, labellist):
    for class_num in labellist:
        gt_pngs = os.listdir(root_path + class_num)
        for file in tqdm(gt_pngs):
            aa = file.split('(')[2].split('_')[0]
            ###################### 中卡车###########################
            if class_num == '602' or class_num == '22':
                change_to_smalltruck(file, aa, class_num, labeltype)
                change_to_bigtruck(file,aa,class_num,labeltype)
                change_to_semitrailer(file,aa,class_num,labeltype)
            ###################### 大卡车###########################
            if class_num == '6011' or  class_num == '10':
                change_to_smalltruck(file, aa, class_num, labeltype)
                change_to_middletruck(file, aa, class_num, labeltype)
                change_to_semitrailer(file, aa, class_num, labeltype)
            ###################### 小卡车###########################
            if class_num == '603':
                change_to_middletruck(file, aa, class_num, labeltype)
                change_to_bigtruck(file, aa, class_num, labeltype)
                change_to_semitrailer(file, aa, class_num, labeltype)
            ###################### 半挂车###########################
            if class_num == '6012' or class_num == '9':
                change_to_smalltruck(file, aa, class_num, labeltype)
                change_to_middletruck(file, aa, class_num, labeltype)
                change_to_bigtruck(file, aa, class_num, labeltype)


if __name__ == '__main__':
    label_file_truck = {'1': ['6011', '602', '603', '6012'],
                        '2': ['11', '22', '10', '13']}
    label_file_bus = {'20211009': ['12', '23']}
    labellist_truck = label_file_truck['1']
    labellist_bus = label_file_truck['1']
    root_path = '/media/wanji/lijingyang/马冰隧道数据/'
    change_class_truck(root_path, labellist_truck)
    change_class_bus(root_path, labellist_bus)