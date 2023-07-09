import os
import sys

import numpy as np
import pandas as pd
from datetime import datetime 


from modules import plot_images
import cv2


def main():
    
    print("start main function!")
    """ この部分にプログラムを記述します。 """
    ################
    
    #input_jpg = "./input/26842196_s.jpg"
    #input_jpg = "./input/gahag-0109509551.jpg"

    """ 色の調整 """
    #img_bgr = cv2.imread(input_jpg)
    #img_rgb = cv2.cvtColor(img_bgr,cv2.COLOR_BGR2RGB)
    #img_hsv = cv2.cvtColor(img_bgr,cv2.COLOR_BGR2HSV)
    #img_gray = cv2.cvtColor(img_bgr,cv2.COLOR_BGR2GRAY)

    #plot_images([img_rgb,img_bgr , img_hsv])
    a = 100
    b=1000
    print(a+b)

    ################
    return None


def test():
    try:
        print("test is OK!!!")
    except Exception as e:
        print("Not Ok... Please check any settings...")


#以降この関数をmoduleで利用することがあるかもしれません。
# img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
# そのときに、このように記述しておくと便利なので
if __name__ == "__main__":
    
    test()
    main()
