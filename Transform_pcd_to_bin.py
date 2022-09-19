import os
import numpy as np
from tqdm import tqdm

def pcd2bin(filename,save_path):
    points=[]
    with open(filename) as f:
       for line in f.readlines()[11:len(f.readlines())-1]:
          strs = line.split(' ')
          if len(strs[0]) < 0:
              continue

          #points.append([float(strs[0]),float(strs[1]),float(strs[2]),float(strs[3].strip())])
          points.append([float(strs[0]), float(strs[1]), float(strs[2].strip()), float(0)])
    p = np.array(points,dtype=np.float32)
    p.tofile(save_path)

def remove_error_pcd(pcd_list, pcd_data):
    pcd_list = os.listdir(pcd_data)
    n = 0
    for j in tqdm(pcd_list):
        filename = pcd_data + j
        with open(filename) as f:
            for line in f.readlines()[11:len(f.readlines()) - 1]:
                strs = line.split(' ')
                if len(strs) > 4 and strs[4] == '.PCD':
                    os.remove(pcd_data + j)
                    n = n + 1
                    break
    print('double:', n)

# 移除csv中有的而pcd中没有的
def remove_csv_have_pcd_donthave(pcd_data, csv_data):
    q = 0
    pcd_list = os.listdir(pcd_data)
    csv_list = os.listdir(csv_data)
    for p in tqdm(csv_list):
        if p.split('.')[0] + '.pcd' not in pcd_list:
            os.remove(csv_data + p)
            q = q + 1
    print('csv中有的而pcd中没有的:', q)

# 只转换csv中有的到bin
def transform_pcd_to_bin(pcd_data, save_dir, csv_data):
    pcd_list = os.listdir(pcd_data)
    for i in tqdm(pcd_list):
        # if i.split('.')[0] + ' .csv' in csv_list:
        filename = pcd_data + i
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)
        #print(filename)
        pcd2bin(filename, save_dir + i.replace('.pcd', '.bin'))

def main(pcd_data, csv_data, save_dir):
    #remove_error_pcd(pcd_data)
    #remove_csv_have_pcd_donthave(pcd_data, csv_data)
    transform_pcd_to_bin(pcd_data, save_dir, csv_data)

if __name__ == '__main__':
    pcd_data = '/media/wanji/lijingyang/docker/ezhou_data/eval/qifu_test_pcd/'
    csv_data = '/media/wanji/lijingyang/docker/ezhou_data/eval/qifu_test_pcd/'
    save_dir = '/media/wanji/lijingyang/docker/ezhou_data/eval/qifu_test_bin/'
    main(pcd_data, csv_data, save_dir)