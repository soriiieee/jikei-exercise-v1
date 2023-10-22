import os,sys,glob
import numpy as np
# print(np.__version__)

import pandas as pd
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

import warnings
warnings.simplefilter("ignore")

import cv2
import matplotlib.pyplot as plt
plt.rcParams["font.size"] = 15

import seaborn as sns

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

from prophet import Prophet


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

    ret, img_otsu = cv2.threshold(img_gray,0,255,cv2.THRESH_OTSU)
    img_adaptative = cv2.adaptiveThreshold(img_gray, 
                              255, 
                              cv2.ADAPTIVE_THRESH_MEAN_C, 
                              cv2.THRESH_BINARY, 
                              31, 
                              10)
    ################
    return None


def read_temperature_csv(point,year="all" ,month="all"):
    def convert_date(x):
        yy ,mm,dd = list(map(int,x.split("/")))
        return date(yy,mm,dd)

    temperature_csv = "input/{}_temp.csv".format(point)
    df = pd.read_csv(temperature_csv , encoding="cp932",skiprows=4)
    df.columns = ["Date" , "temp" , "quality" , "Num"]

    df["YY"] = df["Date"].apply(lambda x: int(x.split("/")[0]))
    df["MM"] = df["Date"].apply(lambda x: int(x.split("/")[1]))

    if year != "all":
        df = df[df["YY"]==int(year)]
    if month != "all":
        df = df[df["MM"]==int(month)]
         
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


def describe_temperature_file(point,year="all" ,month="all"):
    """_summary_
    Args:
        point (str): _description_
        year (str, optional): use Year. Defaults to "all".
        month (str, optional): use Month . Defaults to "all".
    
    return: (None) 
        Print max and minimum temperature day at Point site.
    """

    df = read_temperature_csv(point,year="all" ,month="all")

    index_list = list(df.index)
    max_temp,max_idx = df["temp"].max() , np.argmax(df["temp"])
    min_temp,min_idx = df["temp"].min() , np.argmin(df["temp"])
    average_temp = round(df["temp"].mean(),2)
    print("-"*100)
    print(point , "の気温について")
    print("使用年 = " , year , "使用月 = " , month)
    print(max_temp,"℃",index_list[max_idx])
    print(min_temp,"℃",index_list[min_idx])
    print("平均気温(All-Term) = " , average_temp,"℃")
    return None


def plot_boxmap(point):
    """
    気象庁のサイトからダウンロードしてみよう！
    https://www.data.jma.go.jp/gmd/risk/obsdl/index.php

    """
    # point = "funabashi"
    # point = "nagano"
    # point = "sapporo"


    df = read_temperature_csv(point)

    """ 8月だけを抜き取って、３０年間の玄関平均気温の推移を見てみる　"""

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


def predict_prophetAIModel(point):
    """_summary_

    Args:
        point (_type_): 分析する地点のポイント（finabashi .etc）
    Returns:
        _type_: None
    """
    df = read_temperature_csv(point)
    gr = df.groupby("YY").agg({"temp" : "mean"}).reset_index()
    gr = df.groupby(["YY","MM"]).agg({"temp" : "mean"}).reset_index()
    
    gr["ds"] = gr[["YY","MM"]].apply(lambda x: date(x[0],x[1],1),axis=1)
    gr = gr.rename(columns = {"temp" : "y"})
    
    # model = Prophet().fit(gr)
    model = Prophet(seasonality_mode='multiplicative', mcmc_samples=300).fit(gr, show_progress=False)

    future = model.make_future_dataframe(periods=12*30, freq='MS')
    fcst = model.predict(future)
    fig = model.plot(fcst)
    fig.suptitle("past30 and next30 years temperature Prediction!({})¥n Prophet(AI-timeSeries predict Model)".format(point))
    fig.savefig("./output/change_temperature_02_AI_Model.png",bbox_inches="tight")
    print("保存場所：", "./output/change_temperature_02_AI_Model.png")
    return None


def predict_LinearModel(point):
    """
    気温のモデル
    1: 通常の線形モデル
    2: Facebook開発のAIアルゴリズム(Prophet)
    ＊この他にも、さまざまなモデルがありますが・・・・興味がある人がぜひ探してみて！
    """
    df = read_temperature_csv(point)
    
    ave_temp = df["temp"].mean()
    gr = df.groupby(["YY","MM"]).agg({"temp" : "mean"}).reset_index()
    gr["YY2"] = gr["YY"].astype(float) + gr["MM"].astype(float)/12
    X,y = gr["YY2"].values.reshape(-1,1) , gr["temp"].values
    lr = LinearRegression().fit(X,y)
    
    X2 = PolynomialFeatures(2).fit_transform(gr["YY2"].values.reshape(-1,1))
    lr2 = LinearRegression().fit(X2,y)
    
    print("傾き(1年あたりの気温の上昇率) = ",lr.coef_ ,"度")

    dates = [ (datetime(2023, 8, 1) + relativedelta(months=i)).strftime("%Y-%m") for i in range(12*30)]
    df_future = pd.DataFrame({"dates" : dates})
    df_future["YY"] = df_future["dates"].apply(lambda x: int(x.split("-")[0]))
    df_future["MM"] = df_future["dates"].apply(lambda x: int(x.split("-")[1]))
    df_future["temp"] = np.nan
    df_future["YY2"] = df_future["YY"].astype(float) + df_future["MM"].astype(float)/12 
    
    futures = pd.DataFrame({})
    
    
    gr = pd.concat([gr,df_future],axis=0)
    gr["predict"] = lr.predict(gr["YY2"].values.reshape(-1,1))
    
    X2_pred = PolynomialFeatures(2).fit_transform(gr["YY2"].values.reshape(-1,1))
    gr["predict2"] = lr2.predict(X2_pred)
    
    # gr = gr.rename(columns = {"YY": "ds" , "temp" : "y"})
    gr["ds"] = gr[["YY","MM"]].apply(lambda x: date(x[0],x[1],1),axis=1)
    gr = gr.set_index("ds")
    
    fig,ax = plt.subplots(figsize=(16,8))
    
    ax.plot(gr["temp"],label="Observe" ,color = "k",marker="o" , markersize=3)
    ax.axhline(y=ave_temp , label="Average-Temp({}) 1993-2023(30Years) = {}度".format(point,np.round(ave_temp,4)),color="gray")
    ax.plot(gr["predict"],label="Predict(1) {}x+Const".format(np.round(lr.coef_,4)) ,color = "r")
    ax.plot(gr["predict2"],label="Predict(2)",color = "b")
    
    ax.grid()
    ax.legend(loc = "upper left")
    ax.set_title("past30 and next30 years temperature Prediction!({})".format(point))
    fig.savefig("./output/change_temperature_01_LinearModel.png",bbox_inches="tight")
    print("保存場所：", "./output/change_temperature_01_LinearModel.png")
    return None

#以降この関数をmoduleで利用することがあるかもしれません。
# そのときに、このように記述しておくと便利なので
if __name__ == "__main__":
    # calc()
    # show()

    # temp()
    # predict_LinearModel("funabashi")
    
    
    # predict_LinearModel("nagano")
    predict_prophetAIModel("nagano")

