#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Code to crop and save image fragments from larger images.
"""

import cv2, numpy as np
from datetime import datetime
import glob

input_path = r'/home/eric/deep_learning/fish/annotated_images/'
output_path = r"//home/eric/deep_learning/fish/small_images/"

window_params = {'width': 1500, 'height': 1800, 'x': 200, 'y': 200}

#%%
image_paths = np.sort(glob.glob(input_path + "*.bmp"))
num_images = len(image_paths)
print(f"You have {num_images} images")

image_ind = 25

image_path = image_paths[image_ind]
crop_count = 0
image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)  
(im_h, im_w) = image.shape
max_d = np.max([im_h, im_w])
line_width = int(np.ceil(max_d/1000)*3)
image_to_show = np.copy(image)
mouse_pressed = False
s_x = s_y = e_x = e_y = -1

def mouse_callback(event, x, y, flags, param):
    global image_to_show, s_x, s_y, e_x, e_y, mouse_pressed

    if event == cv2.EVENT_LBUTTONDOWN:
        mouse_pressed = True
        s_x, s_y = x, y
        image_to_show = np.copy(image)

    elif event == cv2.EVENT_MOUSEMOVE:
        if mouse_pressed:
            image_to_show = np.copy(image)
            cv2.rectangle(image_to_show, (s_x, s_y),
                          (x, y), (255, 255, 255), line_width)

    elif event == cv2.EVENT_LBUTTONUP:
        mouse_pressed = False
        e_x, e_y = x, y
        print(s_x, s_y, e_x, e_y)
        box_width = abs(e_x - s_x)
        box_height = abs(e_y - s_y)
        print(f"    Height/Width: {box_height}, {box_width}")
        text_val = f"{box_height} {box_width}"
        cv2.putText(image_to_show, text_val, (s_x-50, s_y-50), cv2.FONT_HERSHEY_SIMPLEX, 5, (255, 255, 255), 15) #scale, color, thickness

cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.resizeWindow('image', window_params['width'], window_params['height'])  #width, height
cv2.moveWindow('image', window_params['x'], window_params['y'])
cv2.setMouseCallback('image', mouse_callback)
while True:
    cv2.imshow('image', image_to_show)
    k = cv2.waitKey(1)

    if k == ord('s'):
        if s_y > e_y:
            s_y, e_y = e_y, s_y
        if s_x > e_x:
            s_x, e_x = e_x, s_x

        if e_y - s_y > 1 and e_x - s_x > 0:
            cropped_image = image[s_y:e_y, s_x:e_x]
            im_name = f"{image_ind:03d}" + '_' + datetime.now().strftime("%Y%m%d_%H%M%S") + r".png"
            im_path = output_path + im_name
            cv2.imwrite(im_path, cropped_image,  [cv2.IMWRITE_PNG_COMPRESSION, 0])
            crop_count += 1
            print(f"{im_path} saved")
            cv2.rectangle(image, (s_x, s_y),
                          (e_x, e_y), (0, 0, 0), line_width)
            image_to_show = np.copy(image)
            
    elif k == 27:
        break

cv2.destroyAllWindows()
