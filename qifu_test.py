
import os
from tqdm import tqdm

pcd_data = '/media/wanji/lijingyang/docker/ezhou_data/eval/qifu_test_pcd/'
csv_data = '/media/wanji/lijingyang/docker/ezhou_data/eval/qifu_test_csv/'
save_dir = '/media/wanji/lijingyang/docker/ezhou_data/eval/qifu_test_bin/'
root_dir = '/media/wanji/lijingyang/docker/ezhou_data/eval/'
name_list = []
pcd_list = os.listdir(pcd_data)
for i in tqdm(pcd_list):
    ii = i.split('.')[0]
    name_list.append(ii)


csv_list = os.listdir(csv_data)
for i in range(len(csv_list)):
    dist1 = csv_data + csv_list[i]
    dist2 = csv_data + name_list[i] + '.csv'
    os.rename(dist1, dist2)