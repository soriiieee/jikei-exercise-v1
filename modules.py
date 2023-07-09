import os,sys,glob
import numpy as np
# print(np.__version__)

import pandas as pd
from datetime import datetime, date
import cv2

import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.linear_model import LinearRegression
from prophet import Prophet


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
    
    if not isinstance(list_images,list):
        list_images = [list_images]
    
    f,ax = plt.subplots(1,len(list_images) , figsize=(11*len(list_images) , 8))

    
    def plot_ax(ax,img):
        if img.ndim==2:
            ax.imshow(img,cmap="gray")
        else:
            ax.imshow(img)
        
    if len(list_images)==1:
        img = list_images[0]
        plot_ax(ax,img)
        
    else:
        for i,img in enumerate(list_images):
            
            plot_ax(ax[i],img)
            if i==0:
                ax[i].set_title("Original-Image¥n Image-Size = {}".format(img.shape))
    
    f.savefig("./output/img.png",bbox_inches="tight")
    print("画像は、./output/img.png に保存されています！")
    plt.close()
    return None


def show():
    """ この部分にプログラムを記述します。 """
    ################
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


def read_temperature_csv(point):
    def convert_date(x):
        yy ,mm,dd = list(map(int,x.split("/")))
        return date(yy,mm,dd)

    temperature_csv = "input/{}_temp.csv".format(point)
    df = pd.read_csv(temperature_csv , encoding="cp932",skiprows=4)
    df.columns = ["Date" , "temp" , "quality" , "Num"]

    df["YY"] = df["Date"].apply(lambda x: int(x.split("/")[0]))
    df["MM"] = df["Date"].apply(lambda x: int(x.split("/")[1]))

    df["Date"] = df["Date"].apply(lambda x: convert_date(x))
    
    df = df[df["quality"]>=5]
    df = df.set_index("Date")
    return df

def plot_temps(df , title="sample"):
    f,ax = plt.subplots(figsize=(15,8))

    ax.plot(df["temp"],label="temperature")
    ax.set_title(title)


    f.savefig("./output/temp.png")
    plt.close()
    return None


def temp():
    """
    気象庁のサイトからダウンロードしてみよう！
    https://www.data.jma.go.jp/gmd/risk/obsdl/index.php

    """
    point = "funabashi"
    # point = "nagano"
    # point = "sapporo"


    df = read_temperature_csv(point)
    df = df[df["MM"] == 8]



    index_list = list(df.index)
    max_temp,max_idx = df["temp"].max() , np.argmax(df["temp"])
    min_temp,min_idx = df["temp"].min() , np.argmin(df["temp"])
    average_temp = round(df["temp"].mean(),2)
    print("-"*100)
    print(point , "の気温について")
    print(max_temp,"℃",index_list[max_idx])
    print(min_temp,"℃",index_list[min_idx])
    print("Average-temperature(All-Term) = " , average_temp,"℃")

    plot_temps(df, title="timeSeries {} temperature".format(point))


def temp2(point):
    """
    気象庁のサイトからダウンロードしてみよう！
    https://www.data.jma.go.jp/gmd/risk/obsdl/index.php

    """
    # point = "funabashi"
    # point = "nagano"
    # point = "sapporo"


    df = read_temperature_csv(point)

    """ 8月だけを抜き取って、３０年間の玄関平均気温の推移を見てみる　"""
    df = df[df["MM"] == 8]

    if 1:
        gr = df.groupby("YY").agg({"temp" : "mean"})
        plot_temps(gr, title="timeSeries {} temperature".format(point))

    if 1:
        f,ax = plt.subplots(figsize=(15,7))
        sns.boxplot(df,x = "YY",y = "temp",orient="v",ax=ax)
        f.savefig("./output/boxplot_temp.png",bbox_inches="tight")
        plt.close()

    # print(gr.head())
    sys.exit()


def temp3():
    """
    気温のモデル
    1: 通常の線形モデル
    2: Facebook開発のAIアルゴリズム(Prophet)
    ＊この他にも、さまざまなモデルがありますが・・・・興味がある人がぜひ探してみて！
    """
    point = "funabashi"
    # point = "nagano"
    # point = "sapporo"


    df = read_temperature_csv(point)
    # df = df[df["MM"] == 8]
    gr = df.groupby("YY").agg({"temp" : "mean"}).reset_index()

    # X,y = gr["YY"].values.reshape(-1,1) , gr["temp"].values
    # lr = LinearRegression()
    # lr.fit(X,y)
    # print(lr.coef_ , lr.intercept_)

    gr = df.groupby(["YY","MM"]).agg({"temp" : "mean"}).reset_index()
    # print(gr.head())
    # sys.exit()

    # gr = gr.rename(columns = {"YY": "ds" , "temp" : "y"})
    gr["ds"] = gr[["YY","MM"]].apply(lambda x: date(x[0],x[1],1),axis=1)
    gr = gr.rename(columns = {"temp" : "y"})
    # print(gr.head())
    # sys.exit()
    
    # model = Prophet().fit(gr)
    model = Prophet(seasonality_mode='multiplicative', mcmc_samples=300).fit(gr, show_progress=False)

    future = model.make_future_dataframe(periods=12*30, freq='MS')
    fcst = model.predict(future)
    fig = model.plot(fcst)
    fig.savefig("./output/prophet.png",bbox_inches="tight")

    # forecast = model.predict(future)

    print(fcst)






    print(gr.head())







    

    ###本当に暑くなっているの？


    # print(df.head())
    
    
    # print(df.dtypes)
    # print(df.columns)

#以降この関数をmoduleで利用することがあるかもしれません。
# そのときに、このように記述しておくと便利なので
if __name__ == "__main__":
    # calc()
    # show()

    # temp()
    temp2()
    # temp3()
