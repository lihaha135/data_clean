from PIL import Image
import numpy as np
import csv
import os
from tqdm import tqdm
import time

def calulate_distance(root_path_csv,  save_root_path):
    labelfiles = os.listdir(root_path_csv)
    len = ['0','10','20','30','40','50','60','70','80','90']
    len_80_90, len_70_80, len_60_70, len_50_60 =  [], [], [], []
    len_40_50 = []
    len_30_40 = []
    len__80__90 = []
    len__70__80 = []
    len_30 = []
    for file in tqdm(labelfiles):
        with open(root_path_csv + '/' + file, 'r') as f:
            reader = csv.reader(f)
            for i in reader:
                if float(i[2]) > 8000:
                    len_80_90.append(float(i[2]))
                if float(i[2]) < 8000 and float(i[2]) > 7000:
                    len_70_80.append(float(i[2]))
                if float(i[2]) < 7000 and float(i[2]) > 6000:
                    len_60_70.append(float(i[2]))
                if float(i[2]) < 6000 and float(i[2]) > 5000:
                    len_50_60.append(float(i[2]))
                if float(i[2]) < 5000 and float(i[2]) > 4000:
                    len_40_50.append(float(i[2]))
                if float(i[2]) < 4000 and float(i[2]) > 3000:
                    len_30_40.append(float(i[2]))
                if float(i[2]) < 3000 :
                    len_30.append(float(i[2]))
                if float(i[2]) > -9000 and float(i[2]) < -8000:
                    len__80__90.append(float(i[2]))
                if float(i[2]) > -8000 and float(i[2]) < -7000:
                    len__70__80.append(float(i[2]))
    #len.sort()
    print(len(len_80_90))
    print(len(len_70_80))
    print(len(len_60_70))
    print(len(len_50_60))
    print(len(len_40_50))
    print(len(len_30_40))
    print(len(len__80__90))
    print(len(len__70__80))
                # save_path = save_root_path + '/' + 'draw_2D'
                # if os.path.exists(save_path) is False:
                #         os.makedirs(save_path)
                #save_png_path = save_path + '/' + file.split('.')[0] + '.png'


root_path_csv = '/media/wanji/lijingyang/马冰隧道数据/mabing_60_90/mabing_csv_类别过滤_数据增强_60_90'
save_root_path = '/media/wanji/lijingyang/隧道数据清洗前/clean_ago'
calulate_distance( root_path_csv, save_root_path)