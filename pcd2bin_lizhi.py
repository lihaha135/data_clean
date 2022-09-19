import os
import numpy as np
from tqdm import tqdm

def pcd2bin(pcd_data, filename,save_path):
    points=[]
    with open(pcd_data + filename ) as f:
       for line in f.readlines()[11:len(f.readlines())-1]:
          strs = line.split(' ')
          if len(strs[0]) < 0:
              continue
          points.append([float(strs[0]),float(strs[1]),float(strs[2].strip())])
    p = np.array(points, dtype=np.float32)
    p.tofile(save_path)



pcd_data = '/media/wanji/lijingyang/data_cleaning/2/'
save_dir = '/media/wanji/lijingyang/data_cleaning/bin/'
pcd_list = os.listdir(pcd_data)



# 只转换csv中有的到bin
for filename in tqdm(pcd_list):
    pcd2bin(pcd_data, filename, save_dir+filename.replace('.pcd', '.bin'))

