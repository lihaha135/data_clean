
import csv
import os


def qinhao(root_path, save_path):
    csv_list = os.listdir(root_path)
    for ii in csv_list:
        file_path = root_path + ii
        new_data = []
        with open(file_path, 'r') as f:
            reader = csv.reader(f)
            for i in reader:
                i[4] = str(float(i[4]) - 170)
                new_data.append(i)
        save_path_1 = save_path + ii
        with open(save_path_1, 'a+') as f:
            f.truncate(0)
            for i in new_data:
                wf = csv.writer(f)
                wf.writerow(i)


root_path = '/media/wanji/lijingyang/马冰隧道数据/mabing_60_80/mabing_csv_类别过滤_数据增强_60_80/'
save_path = '/media/wanji/lijingyang/qinhao/qinhao_csv/'
qinhao(root_path, save_path)