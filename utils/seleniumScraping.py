import os
from bs4 import BeautifulSoup
# import urllib.request
import requests

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# from webdriver_manager.chrome import ChromeDriverManager


import warnings
warnings.simplefilter("ignore")
# print("test = " , __name__)
import pandas as pd
import time
from datetime import datetime

from pathlib import Path
import re

######class & function(設定)#############
class Nogisaka46:
    
    HOME = Path(__file__).parent.parent
    DATA = os.path.join(HOME , "output")
    IMG = os.path.join(HOME , "img")
    
    def __init__(self):
        os.makedirs(self.DATA , exist_ok=True)
        os.makedirs(self.IMG , exist_ok=True)
        
        self.members_csv = os.path.join(self.DATA,"nogisaka46_members.csv")
        
    @classmethod
    def membersList(cls):
        url = "https://www.nogizaka46.com/s/n46/search/artist?ima=0538"
        # Selenium tool
        driver = webdriver.Chrome()
        driver.implicitly_wait(10) # seconds
        
        driver.get(url)
        # elements = driver.find_elements(By.CLASS_NAME, "m--bg.js-bg.is-l") #画像イメージ
        elements = driver.find_elements(By.CLASS_NAME, "m--mem.js-pos.a--tx") #メンバー
        print(len(elements))
        
        members = {}
        for i,e in enumerate(elements):
            
            # if i>0 and i%5==4:
            #     driver.execute_script('window.scrollBy(0, 200);')
            
            detail_page,image_path = cls.getMemberPageAndImageJPEGpath(e)
            
            while True:
                flg,[name,kana,birt,bloo,star,hght] = cls.makeMembersInfo(driver,detail_page)
                if flg==1: break
                
                time.sleep(1.0)
            
            members[i] = [name,kana,birt,bloo,star,hght,detail_page,image_path]
            print(datetime.now(),"[pickUp-END]" , i , members[i])
        
        df = pd.DataFrame(members).T
        df.columns = ["Name" , "Kana" ,"BirthDay","BloodType","Star","Height","DetailSite" ,"ImagePath"]
        df.to_csv(os.path.join(cls.DATA , "nogisaka46_members.csv"),index=False)
        #browser shut Down...
        driver.quit()
    
    @staticmethod
    def getMemberPageAndImageJPEGpath(e):
        
        detail_page = e.find_element(By.CSS_SELECTOR, "a[class='m--mem__in hv--thumb']").get_attribute('href')
        image_path = e.find_element(By.CLASS_NAME,"m--bg.js-bg.is-l").get_attribute('style')
        image_path= image_path.split('url(')[1].replace('"','').replace(')','').replace(';','')
        # name = e.find_element(By.CLASS_NAME, "m--mem__name").text
        # kana = e.find_element(By.CLASS_NAME, "m--mem__kn").text
        # name2 = e.find_element(By.CLASS_NAME, "m--mem__names.f--head").find_elements(By.TAG_NAME, "p")[0].text
        return detail_page,image_path
    
    @staticmethod
    def makeMembersInfo(driver,url):
        
        driver.execute_script('window.open()')
        driver.switch_to.window(driver.window_handles[-1])
        
        driver.get(url)
        
        try:
            WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located)
            # time.sleep(8.)
            
            name = driver.find_element(By.CLASS_NAME,"md--hd__ttl.f--head.a--tx.js-tdi.js-membername").text
            kana = driver.find_element(By.CLASS_NAME,"md--hd__j.f--head.a--tx.js-tdi").text
            infos = driver.find_elements(By.CLASS_NAME,"md--hd__data__d.f--head")
            
            birt = infos[0].text
            bloo = infos[1].text
            star = infos[2].text
            hght = infos[3].text
            flg = 1
        
        except:
            name,kana,birt,bloo,star,hght = '','','','','',''
            flg = 0
        
        # if name =='' or kana==''or birt=='' or bloo=='' or star=='' or hght=='':
        #     cls.makeMembersInfo(driver,url)
        
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        
        return flg,[name,kana,birt,bloo,star,hght] 
        