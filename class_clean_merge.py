from PIL import Image
import numpy as np
import csv
import os
from tqdm import tqdm
import time

def change_to_bigtruck(file,aa):
    if int(aa) > 1000 and int(aa) < 1500:
        file_path = root_path + 'mabing_csv/' + file.split('-')[0] + '.csv'
        new_data = []
        with open(file_path, 'r') as f:
            reader = csv.reader(f)
            for i in reader:
                if int(float(i[7])) == int(aa):
                    i[1] = '6011'
                    new_data.append(i)
                else:
                    new_data.append(i)
        with open(file_path, 'a+') as f:
            f.truncate(0)
            for i in new_data:
                wf = csv.writer(f)
                wf.writerow(i)


def change_to_semitrailer(file,aa):
    if int(aa) > 1500:
        file_path = root_path + 'mabing_csv/' + file.split('-')[0] + '.csv'
        new_data = []
        with open(file_path, 'r') as f:
            reader = csv.reader(f)
            for i in reader:
                if int(float(i[7])) == int(aa):
                    i[1] = '6012'
                    new_data.append(i)
                else:
                    new_data.append(i)
        with open(file_path, 'a+') as f:
            f.truncate(0)
            for i in new_data:
                wf = csv.writer(f)
                wf.writerow(i)


def change_to_smalltruck(file, aa):
    if int(aa) < 700:
        file_path = root_path + 'mabing_csv/' + file.split('-')[0] + '.csv'
        new_data = []
        with open(file_path, 'r') as f:
            reader = csv.reader(f)
            for i in reader:
                if int(float(i[7])) == int(aa):
                    i[1] = '603'
                    new_data.append(i)
                else:
                    new_data.append(i)
        with open(file_path, 'a+') as f:
            f.truncate(0)
            for i in new_data:
                wf = csv.writer(f)
                wf.writerow(i)

def change_to_middletruck(file, aa):
    if int(aa) > 700 and int(aa) < 1000:
        file_path = root_path + 'mabing_csv/' + file.split('-')[0] + '.csv'
        new_data = []
        with open(file_path, 'r') as f:
            reader = csv.reader(f)
            for i in reader:
                if int(float(i[7])) == int(aa):
                    i[1] = '602'
                    new_data.append(i)
                else:
                    new_data.append(i)
        with open(file_path, 'a+') as f:
            f.truncate(0)
            for i in new_data:
                wf = csv.writer(f)
                wf.writerow(i)


def change_class_truck(root_path):
    labellist = ['6011','602','603','6012']
    for class_num in labellist:
        gt_pngs = os.listdir(root_path + 'gt_database/' + class_num)
        for file in tqdm(gt_pngs):
            aa = file.split('(')[2].split('_')[0]
            ###################### 中卡车###########################
            if class_num == '602' :
                change_to_smalltruck(file, aa)
                change_to_bigtruck(file,aa)
                change_to_semitrailer(file,aa)
            ###################### 大卡车###########################
            if class_num == '6011' :
                change_to_smalltruck(file, aa)
                change_to_middletruck(file, aa)
                change_to_semitrailer(file, aa)
            ###################### 小卡车###########################
            if class_num == '603':
                change_to_middletruck(file, aa)
                change_to_bigtruck(file, aa)
                change_to_semitrailer(file, aa)
            ###################### 半挂车###########################
            if class_num == '6012' :
                change_to_smalltruck(file, aa)
                change_to_middletruck(file, aa)
                change_to_bigtruck(file, aa)

def change_class_bus(root_path):
    labellist = ['6011','602','603','6012']
    for class_num in labellist:
        gt_pngs = os.listdir(root_path + 'gt_database/' + class_num)
        for file in tqdm(gt_pngs):
            aa = file.split('(')[2].split('_')[0]
            ###################### 中卡车###########################
            if class_num == '602' :
                change_to_smalltruck(file, aa)
                change_to_bigtruck(file,aa)
                change_to_semitrailer(file,aa)
            ###################### 大卡车###########################
            if class_num == '6011' :
                change_to_smalltruck(file, aa)
                change_to_middletruck(file, aa)
                change_to_semitrailer(file, aa)
            ###################### 小卡车###########################
            if class_num == '603':
                change_to_middletruck(file, aa)
                change_to_bigtruck(file, aa)
                change_to_semitrailer(file, aa)
            ###################### 半挂车###########################
            if class_num == '6012' :
                change_to_smalltruck(file, aa)
                change_to_middletruck(file, aa)
                change_to_bigtruck(file, aa)


if __name__ == '__main__':
    root_path = '/media/wanji/lijingyang/马冰隧道数据/'
    change_class_truck(root_path)