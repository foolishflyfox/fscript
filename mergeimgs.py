#!env python

import os
import sys
from PIL import Image
import numpy as np
#import path

cur_dir = os.path.abspath(os.curdir)
script_name = os.path.basename(__file__)


if len(sys.argv)<3:
    # -h 表示水平合并 默认竖直方向合并
    print(f"Usage : {script_name} [-h] img1 img2 [img3 [...]]")
    exit()

process_mode = 'v'
file1_index = 1

if sys.argv[1]=='-h':
    process_mode = 'h'
    file1_index = 2

postfix = os.path.splitext(os.path.basename(sys.argv[file1_index]))[1]
ims = []
width, height = None, None
for i in range(file1_index, len(sys.argv)):
    try:
        im = Image.open(os.path.join(cur_dir, sys.argv[i]))
    except FileNotFoundError:
        print(f"FileNotFoundError : file {sys.argv[i]} don't exist!")
        exit()
    except OSError:
        print(f"OSError : file {sys.argv[i]} may not an image!")
        exit()
    if process_mode=='v':
        if width==None:
            min_size = width = im.size[0]
        elif width != im.size[0]:
            print(f"{sys.argv[i]} width isn't equal to {sys.argv[file1_index]}"+
                "\n,it will merge as the minimum width")
            min_size = min(min_size, im.size[0])
            # exit()
    else:
        if height==None:
            min_size = height = im.size[1]
        elif height != im.size[1]:
            print(f"{sys.argv[i]} height isn't equal to {sys.argv[file1_index]}"+
                ",it will merge as the minimum height")
            min_size = min(min_size, im.size[1])               
            # exit()
    im = np.array(im)
    ims.append(im)

if process_mode=='v':
    ims =  [im[:, :min_size, :] for im in ims]
    merge_im = np.vstack(tuple(ims))
else:
    ims = [im[:min_size, :, :] for im in ims]
    merge_im = np.hstack(tuple(ims))

Image.fromarray(merge_im).save("merged"+postfix)
print(f"./merged{postfix} ok!")

