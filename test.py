import os
import sys

import numpy as np
import pandas as pd
from datetime import datetime 


from modules import plot_images,describe_temperature_file,predict_prophetAIModel,predict_LinearModel 
import cv2


def main():
    
    print("start main function!")
    """ この部分にプログラムを記述します。 """
    ################
    
    point = "funabashi"
    describe_temperature_file(point)
    
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
