#!env python

import os
import sys
import numpy as np
from PIL import Image
#import path

cur_dir = os.path.abspath(os.curdir)
script_name = os.path.basename(__file__)


if len(sys.argv)<2:
    print(f"Usage : {script_name} PNG_filename [JPG_filename]")
    exit()

final_path = None
if len(sys.argv)>=3:
    tp_name = sys.argv[2]
    if tp_name[-4:] not in ['.jpg', 'jpeg']:
        print("The output file suffix should be jpg or jpeg")
        exit()
    tp_dir = os.path.dirname(tp_name)
    if not os.path.isdir(tp_dir):
        print(f"Directory '{tp_dir}' isn't exist")
        exit()
    final_path = tp_name
if final_path is None:
    img_name = os.path.splitext(os.path.basename(sys.argv[1]))[0]
    final_path = img_name + '.jpg'

try:
    im = Image.open(os.path.join(cur_dir, sys.argv[1]))
except FileNotFoundError:
    print(f"FileNotFoundError : file {sys.argv[1]} don't exist!")
    exit()
except OSError:
    print(f"OSError : file {sys.argv[1]} may not an image!")
    exit()
# print('begin to process ...')
if im.mode!="RGBA":
    print(f"filie {sys.argv[1]} don't need to convert")
    exit()

# 透明的颜色全部变为白色
im_array = np.array(im)
im_array[:,:,0][im_array[:,:,3]<5]=255
im_array[:,:,1][im_array[:,:,3]<5]=255
im_array[:,:,2][im_array[:,:,3]<5]=255


Image.fromarray(im_array[:, :, :3]).save(final_path)

print(f"{final_path} ok!")

