# fscript

This repository stores some useful script write by myself, and some tools usage.

## useful script

### Image Processing

- mergeimgs.py : used for merge several images
    - Usage : `mergeimgs.py [-h] img1 img2 [img3 [...]]`
    - parameters:
        - `-h`: merge image in horizontal direction, default is vertical

- png2jpeg.py : convert png format image to jpeg formate image
    - Usage : `png2jpeg.py PNG_filename [JPG_filename]`
    - Note : if JPG filename isn't provided, it will create jpg image in the same directory.

- ss_proxy:
    - Usage : `source ss_proxy`
    - Note : It set current terminal proxy, but you should firstly open privoxy server listening at 8118.




