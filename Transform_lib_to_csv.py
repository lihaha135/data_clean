import os


root_path_csv = '/media/wanji/lijingyang/docker/ezhou_data/train/ezhou_lib'
labelfiles = os.listdir(root_path_csv)

for file in labelfiles:
    portion = os.path.splitext(file)
    newname = portion[0] + '.csv'
    os.chdir(root_path_csv)
    os.rename(file, newname)