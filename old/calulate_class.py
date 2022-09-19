from PIL import Image
import numpy as np
import csv
import os
from tqdm import tqdm
import time

def calulate_class(root_path_csv):
    labelfiles = os.listdir(root_path_csv)
    car, bicycle, bus, tricycle = 0, 0, 0, 0
    pedestrian, semitrailer, small_truck, middle_truck, big_truck = 0, 0, 0, 0, 0
    for file in tqdm(labelfiles):
        with open(root_path_csv + '/' + file, 'r') as f:
            reader = csv.reader(f)
            for i in reader:
                if str(i[1]) == '1':
                    pedestrian = pedestrian + 1
                if str(i[1]) in ['2', '3']:
                    bicycle = bicycle + 1
                if str(i[1]) in ['4', '5']:
                    car = car + 1
                if str(i[1]) == '2':
                    tricycle = tricycle + 1
                if str(i[1]) == '603':
                    small_truck = small_truck + 1
                if str(i[1]) == '602':
                    middle_truck = middle_truck + 1
                if str(i[1]) == '6011':
                    big_truck = big_truck + 1
                if str(i[1]) in ['701', '702', '703']:
                    bus = bus + 1
                if str(i[1]) == '6012':
                    semitrailer = semitrailer + 1
    print('car:', car)
    print('bus:', bus)
    print('semitrailer:', semitrailer)
    print('small_truck:', small_truck)
    print('middle_truck:', middle_truck)
    print('big_truck:', big_truck)




root_path_csv = '/media/wanji/lijingyang/docker/second_kd_far/wanji_data/eval_csv_mabing'
calulate_class(root_path_csv)