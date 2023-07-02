import os,sys,glob
import numpy as np
# print(np.__version__)

import pandas as pd
from datetime import datetime 
import cv2

import matplotlib.pyplot as plt


# def cv2imshow(windowname,img):
#     while(1):
#         cv2.imshow(windowname, img)
#         key = cv2.waitKey(100) & 0xff
#         if key != 255 or cv2.getWindowProperty(windowname, cv2.WND_PROP_AUTOSIZE) == -1:
#             cv2.destroyAllWindows()
#             exit()

BackendError = type('BackendError', (Exception,), {})
def _is_visible(winname):
    try:
        ret = cv2.getWindowProperty(
            winname, cv2.WND_PROP_VISIBLE
        )

        if ret == -1:
            raise BackendError('Use Qt as backend to check whether window is visible or not.')

        return bool(ret)

    except cv2.error:
        return False


ORD_ESCAPE = 0x1b
def closeable_imshow(winname, img, *, break_key=ORD_ESCAPE):
    while True:
        cv2.imshow(winname, img)
        key = cv2.waitKey(10)

        if key == break_key:
            break
        if not _is_visible(winname):
            break
    
    cv2.destroyWindow(winname)


def calc():
    """ この部分にプログラムを記述します。 """
    ################
    # ans = (4**3) / 2  + np.exp(2)

    sum=1
    N = 10

    for i in range(1,N+1):
        sum = sum * i # sum +=1
    

    ans = sum
    print("数字の合計 {}までの足し算= Answers".format(10), ans)
    ################
    return None

def plot_images(list_images):
    f,ax = plt.subplots(1,len(list_images) , figsize=(11*len(list_images) , 8))

    for i,img in enumerate(list_images):

        if img.ndim==2:
            ax[i].imshow(img,cmap="gray")
        else:
            ax[i].imshow(img)
        if i==0:
            ax[i].set_title("Original-Image")
    
    f.savefig("./output/img.png",bbox_inches="tight")
    plt.close()
    return None


def show():
    """ この部分にプログラムを記述します。 """
    ################
    # ans = (4**3) / 2  + np.exp(2)

    input_jpg = "./input/26842196_s.jpg"

    """ 色の調整 """
    img_bgr = cv2.imread(input_jpg)
    img_rgb = cv2.cvtColor(img_bgr,cv2.COLOR_BGR2RGB)
    # img_hsv = cv2.cvtColor(img_bgr,cv2.COLOR_BGR2HSV)
    img_gray = cv2.cvtColor(img_bgr,cv2.COLOR_BGR2GRAY)

    # plot_images([img_rgb ,  img_bgr, img_hsv,img_gray])

    """ フィルターエッジ検出 """
    # img_blur=cv2.blur(img_rgb,(7,7))
    # img_gau=cv2.GaussianBlur(img_rgb,(5,5),3)
    # img_median = cv2.medianBlur(img_rgb,9)
    # plot_images([img_rgb ,  img_blur, img_gau,img_median])

    """ 色輪郭抽出 """

    ret, img_otsu =cv2.threshold(img_gray,0,255,cv2.THRESH_OTSU)
    img_adaptative = cv2.adaptiveThreshold(img_gray, 
                              255, 
                              cv2.ADAPTIVE_THRESH_MEAN_C, 
                              cv2.THRESH_BINARY, 
                              31, 
                              10)
    plot_images([img_rgb ,  img_gray, img_otsu,img_adaptative])
    

    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    ################
    return None

#以降この関数をmoduleで利用することがあるかもしれません。
# そのときに、このように記述しておくと便利なので
if __name__ == "__main__":
    # calc()
    show()
