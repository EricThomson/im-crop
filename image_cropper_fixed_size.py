#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Code to crop and save image fragments from larger images.
This one has fixed image size and will only save sub-images of that size (rect_dims)
"""

import cv2, numpy as np
from datetime import datetime
import glob
import platform

if platform.system() == 'Linux':
    input_path = r'/home/eric/deep_learning/fish/annotated_images/'
    output_path = r"//home/eric/deep_learning/fish/small_images/"
else:
    input_path = r'C:/Users/Eric/Desktop/cnn_data/'
    output_path = r'C:/Users/Eric/Desktop/cnn_data/cropped/'

rect_dims = (1024, 1024)
window_params = {'width': 800, 'height': 1000, 'x': 2000, 'y': 10}

#%%
def mouse_callback(event, x, y, flags, param):
    global cropped_image, image_to_show, s_x, s_y, e_x, e_y, mouse_pressed

    if event == cv2.EVENT_RBUTTONDOWN:
        s_x, s_y = x, y
        e_x, e_y = x+rect_dims[1], y+rect_dims[0]
        image_to_show = np.copy(image)
        cv2.rectangle(image_to_show, (s_x, s_y),
                      (e_x, e_y), (255, 255, 255), 30)
        cropped_image = image[s_y:e_y, s_x:e_x]
        print(f"    Height/Width: {cropped_image.shape}")
        text_val = f"{cropped_image.shape}"
        cv2.putText(image_to_show, 
                    text_val, 
                    (s_x+20, s_y+150), 
                    cv2.FONT_HERSHEY_SIMPLEX, 
                    4, (255, 255, 255), 15) #scale, color, thickness
        
#%%
image_paths = np.sort(glob.glob(input_path + "*.bmp"))
num_images = len(image_paths)
print(f"You have {num_images} images")
image_ind = 0

image_path = image_paths[image_ind]
crop_count = 0
image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)  
line_width = 30
image_to_show = np.copy(image)
   
cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.resizeWindow('image', window_params['width'], window_params['height'])  #width, height
cv2.moveWindow('image', window_params['x'], window_params['y'])
cv2.setMouseCallback('image', mouse_callback)
while True:
    cv2.imshow('image', image_to_show)
    k = cv2.waitKey(1)

    if k == ord('s'):
        e_x = s_x + rect_dims[1]
        e_y = s_y + rect_dims[0]

        if e_y - s_y > 1 and e_x - s_x > 1:
            (cropped_h, cropped_w) = cropped_image.shape
            if cropped_h < 1024 or cropped_w < 1024:
                print("Selection is not correct size")
            else:
                #im_name = f"{image_ind:03d}" + '_' + datetime.now().strftime("%Y%m%d_%H%M%S") + r".png"
                im_name = f"{image_ind:03d}" + '_' + datetime.now().strftime("%Y%m%d_%H%M%S") + r".bmp"
                im_path = output_path + im_name
                #cv2.imwrite(im_path, cropped_image,  [cv2.IMWRITE_PNG_COMPRESSION, 0])
                cv2.imwrite(im_path, cropped_image)
                crop_count += 1
                print(f"{im_path} saved")
                cv2.rectangle(image, (s_x, s_y),
                              (e_x, e_y), (0, 0, 0), line_width)
                image_to_show = np.copy(image)
    elif k == ord('n'):
        print("Next image")
    elif k == 27:
        print("Stop")   
        break

cv2.destroyAllWindows()
