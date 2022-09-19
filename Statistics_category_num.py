import os
import csv

def statistics(root_path, file):
    statistics_dict = {}
    labelfiles = os.listdir(root_path)
    for labelfile in labelfiles:
        print(labelfile)
        label_path = root_path + labelfile
        with open(label_path, 'r') as f:
            reader = csv.reader(f)
            for i in reader:
                class_ = list(file.keys())[list(file.values()).index(int(float(i[1])))]
                if class_ in statistics_dict.keys():
                    statistics_dict[class_] = statistics_dict[class_] + 1
                else:
                    statistics_dict[class_] = 1

    print(statistics_dict)

if __name__ == '__main__':
    file_20211009 = {'car': 6, 'passenger_car': 8, 'small_truck': 11, 'middle_truck': 22, 'big_truck': 10, 'big_semitrailer': 24,
                     'semitrailer': 13, 'small_bus': 23, 'big_bus': 12, 'bicycle': 2, 'people': 0, 'moto': 4, 'trimoto': 5}
    file_mabing = {'car': 4, 'passenger_car': 5, 'small_truck': 603, 'middle_truck': 602, 'big_truck': 6011, 'big_semitrailer': 6013,
                   'semitrailer': 6012, 'small_bus': 703, 'middle_bus': 702, 'big_bus': 701, 'bicycle': 201, 'people': 0, 'moto': 202,
                   'trimoto': 3, 'none': 1}
    file_ezhou = {'car': 4, 'passenger_car': 5, 'small_truck': 603, 'middle_truck': 602, 'big_truck': 6011, 'big_semitrailer': 6013,
                   'semitrailer': 6012, 'small_bus': 703, 'middle_bus': 702, 'big_bus': 701, 'bicycle': 201, 'people': 0, 'moto': 202,
                   'trimoto': 3, 'none': 1}
    root_path = '/media/wanji/lijingyang/docker/ezhou_data/train/csv/'
    statistics(root_path, file_mabing)