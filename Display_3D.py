import mayavi.mlab as mlab
import visualize_utils as V
import numpy as np
import csv
import math
import torch


def draw_3D(bin_path, csv_path, label_name, class_names, PI_rads):
    wjdata_infos=[]
    infos = {}
    gt_names = []
    gt_names_number = []
    gt_boxes = []
    infos['lidar_path'] = bin_path + label_name.split('.')[0] + '.bin'
    label_fpath = csv_path + label_name
    points1 = np.fromfile(infos['lidar_path'], dtype=np.float32, count=-1).reshape((-1, 4))
    with open(label_fpath,'r') as f:
        reader=csv.reader(f)
        for i in reader:
            gt_boxes.append(
                [float(i[2]) / 100, float(i[3]) / 100, float(i[4]) / 100, float(i[7]) / 100,
                 float(i[8]) / 100, float(i[9]) / 100, (float(i[6])) * PI_rads ])
            gt_names.append(class_names[str(i[0])])
            gt_names_number.append(int(i[0]))
    infos['gt_boxes'] = np.array(gt_boxes)
    infos['gt_names'] = np.array(gt_names)
    wjdata_infos.append(infos)
    V.draw_scenes(points = points1, ref_boxes=torch.Tensor(gt_boxes), ref_scores=torch.Tensor(gt_names_number))
    mlab.show(stop=True)

def main(bin_path, csv_path, label_name, class_names, PI_rads):
    draw_3D(bin_path, csv_path, label_name, class_names, PI_rads)


if __name__=="__main__":
    class_names = {
        '0': 'pedeef',
        '1': 'sdadsad',
        '2': 'sadsd',
        '3': 'sad',
        '4': 'sadsad',
        '5': 'ssad',
        '6': 'asdad',
        '7': 'sada',
        '8': 'jlhlh',
        '9': 'jklkl',
        '10': 'jkljklkj',
        '11': 'khjkjhk',
        '12': 'hjkhjk',
        '13': 'hjkhjk',
        '14': 'jhkjhk',
        '22': 'bus',
        '23': 'sad'
    }
    PI_rads = math.pi / 180
    # bin_path = '/media/wanji/lijingyang/鄂州项目数据集/马冰隧道/mabing_bin_aug/'
    # csv_path = '/media/wanji/lijingyang/鄂州项目数据集/马冰隧道/mabing_csv_aug/'

    bin_path = '/media/wanji/lijingyang/马冰隧道数据/mabing_bin/'
    csv_path = '/media/wanji/lijingyang/马冰隧道数据/mabing_csv_all/mabing_csv/'


    # bin_path = '/media/wanji/lijingyang/docker/ezhou_data/train/bin/'
    # csv_path = '/media/wanji/lijingyang/docker/ezhou_data/train/csv/'

    label_name = '20210610_3D_tr_pec_sig_tun0001_sun_01380.csv'
    main(bin_path, csv_path, label_name, class_names, PI_rads)