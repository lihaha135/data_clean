import os
import cv2
import numpy as np


su_root_path = '/media/wanji/lijingyang/data_cleaning/2d_su_cai/'
xian_root_path = '/media/wanji/lijingyang/data_cleaning/2d_xian_cai/'
save_path = '/media/wanji/lijingyang/data_cleaning/2d_merge_cai/'
su_imgs = os.listdir(su_root_path)
xian_imgs = os.listdir(xian_root_path)
su_imgs = sorted(su_imgs)
xian_imgs = sorted(xian_imgs)
for i in su_imgs:
    img1 = cv2.imread(su_root_path + i)
    img2 = cv2.imread(xian_root_path + i)
    image = np.vstack((img2, img1))
    cv2.imwrite(save_path + i, image)