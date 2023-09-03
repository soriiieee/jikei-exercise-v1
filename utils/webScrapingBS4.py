from bs4 import BeautifulSoup
# import urllib.request
import requests

import warnings
warnings.simplefilter("ignore")

print("test = " , __name__)

######class & function(設定)#############
class WebScraping:
    
    def __init__(self):
        # self.url = "https://sakurazaka46.com/s/s46/search/artist?ima=0000"
        self.url = "https://www.nogizaka46.com/s/n46/search/artist?ima=2022"
    
    def getSoupData(self):
        # response = urllib.request.urlopen(self.url)
        response = requests.get(self.url)
        
        # print(dir(response))
        # print(response.status)
        # exit()
        if response.status_code == 200:
            soup = BeautifulSoup(response.content)
            response.close()
        return soup
            
    def nogisakaMembers(self):
        soup  = self.getSoupData()
        # print(type(soup))
        # exit()
        members = soup.select("div")
        # members = self.soup.select("div[class*='m--mem__in hv--thumb']")
        # members = soup.find_all(class_='mm--all__in')[0].select()
        # members = soup.select(class_='mm--all__in')
        print(members)
        exit()
        
        
        

######execute(実行)#############
def main():
    web = WebScraping()
    web.nogisakaMembers()
    
    
    return 


def main2():
    import requests
    url = "https://www.nogizaka46.com/images/46/ec1/9c670b4ade367a2f551f26eef4450.jpg"

    urlData = requests.get(url).content

    with open("./sample.jpg" ,mode='wb') as f: # wb でバイト型を書き込める
        f.write(urlData)


if __name__ == "__main__":
    main()