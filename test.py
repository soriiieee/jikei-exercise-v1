import os
import sys

import numpy as np
import pandas as pd
from datetime import datetime 


from modules import read_temperature_csv,temp,temp2
# import cv2


def main():
    
    """ この部分にプログラムを記述します。 """
    ################
    
    input_jpg = "./input/26842196_s.jpg"

    """ 色の調整 """
    
    # df = read_temperature_csv("funabashi")
    df = read_temperature_csv("tsuruga")
    print(df.head())
    # temp2()
    # plot_images([img_rgb ,  img_blur])

    ################
    return None



#以降この関数をmoduleで利用することがあるかもしれません。
# img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
# そのときに、このように記述しておくと便利なので
if __name__ == "__main__":
    main()
