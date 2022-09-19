from PIL import Image
import numpy as np
import csv
import os
from tqdm import tqdm
import time

def find_error_class(root_path, labeltype):
    if labeltype =='1':
        labellist = ['11','6','7','9']
    else:
        labellist = ['11','22','10','13']
    for class_num in labellist:
        gt_pngs = os.listdir(root_path + class_num)
        for file in tqdm(gt_pngs):
            aa = file.split('(')[2].split('_')[0]# 中卡车
            if class_num == '6' or class_num == '22':
                if int(aa) < 700 or int(aa) > 1000:
                    error_path = root_path + class_num + '.txt'
                    error_file = open(error_path, 'a+')
                    ll = str(file) + '\n'
                    error_file.write(ll)
                    error_file.close()
            if class_num == '7' or  class_num == '10': # 大卡车
                if int(aa) > 1500 :
                    error_path = root_path + class_num + '.txt'
                    error_file = open(error_path, 'a+')
                    ll = str(file) + '\n'
                    error_file.write(ll)
                    error_file.close()
            if class_num == '11':  # 小卡车
                if int(aa) > 700 :
                    error_path = root_path + class_num + '.txt'
                    error_file = open(error_path, 'a+')
                    ll = str(file) + '\n'
                    error_file.write(ll)
                    error_file.close()
            if class_num == '13' or class_num == '9':  # 半挂车
                if int(aa) < 1500 :
                    error_path = root_path + class_num + '.txt'
                    error_file = open(error_path, 'a+')
                    ll = str(file) + '\n'
                    error_file.write(ll)
                    error_file.close()


def find_error_class_merge(root_path):
    labellist = ['7','8','9','10']
    for class_num in labellist:
        gt_pngs = os.listdir(root_path + class_num)
        for file in tqdm(gt_pngs):
            aa = file.split('(')[2].split('_')[0]# 中卡车
            if class_num == '8' :
                if int(aa) < 700 or int(aa) > 1000:
                    error_path = root_path + class_num + '.txt'
                    error_file = open(error_path, 'a+')
                    ll = str(file) + '\n'
                    error_file.write(ll)
                    error_file.close()
            if class_num == '9': # 大卡车
                if int(aa) > 1500 or int(aa) < 1000 :
                    error_path = root_path + class_num + '.txt'
                    error_file = open(error_path, 'a+')
                    ll = str(file) + '\n'
                    error_file.write(ll)
                    error_file.close()
            if class_num == '7':  # 小卡车
                if int(aa) > 700 :
                    error_path = root_path + class_num + '.txt'
                    error_file = open(error_path, 'a+')
                    ll = str(file) + '\n'
                    error_file.write(ll)
                    error_file.close()
            if class_num == '10' :  # 半挂车
                if int(aa) < 1500 :
                    error_path = root_path + class_num + '.txt'
                    error_file = open(error_path, 'a+')
                    ll = str(file) + '\n'
                    error_file.write(ll)
                    error_file.close()

root_path = '/media/wanji/lijingyang/隧道点云数据解密版/gt_database/'
labeltype = '2'
#find_error_class(root_path, labeltype)
find_error_class_merge(root_path)