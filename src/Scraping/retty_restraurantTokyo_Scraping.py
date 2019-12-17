import requests
import pandas
from bs4 import BeautifulSoup
import re
import time
import ast
import json
import copy
import sys

from pprint import pprint

data = [['千代田区', 'https://retty.me/area/PRE13/city/13101/'], ['中央区', 'https://retty.me/area/PRE13/city/13102/'], ['港区', 'https://retty.me/area/PRE13/city/13103/'], ['新宿区', 'https://retty.me/area/PRE13/city/13104/'], ['文京区', 'https://retty.me/area/PRE13/city/13105/'], ['台東区', 'https://retty.me/area/PRE13/city/13106/'], ['墨田区', 'https://retty.me/area/PRE13/city/13107/'], ['江東区', 'https://retty.me/area/PRE13/city/13108/'], ['品川区', 'https://retty.me/area/PRE13/city/13109/'], ['目黒区', 'https://retty.me/area/PRE13/city/13110/'], ['大田区', 'https://retty.me/area/PRE13/city/13111/'], ['世田谷区', 'https://retty.me/area/PRE13/city/13112/'], ['渋谷区', 'https://retty.me/area/PRE13/city/13113/'], ['中野区', 'https://retty.me/area/PRE13/city/13114/'], ['杉並区', 'https://retty.me/area/PRE13/city/13115/'], ['豊島区', 'https://retty.me/area/PRE13/city/13116/'], ['北区', 'https://retty.me/area/PRE13/city/13117/'], ['荒川区', 'https://retty.me/area/PRE13/city/13118/'], ['板橋区', 'https://retty.me/area/PRE13/city/13119/'], ['練馬区', 'https://retty.me/area/PRE13/city/13120/'], ['足立区', 'https://retty.me/area/PRE13/city/13121/'], ['葛飾区', 'https://retty.me/area/PRE13/city/13122/'], ['江戸川区', 'https://retty.me/area/PRE13/city/13123/'], ['八王子市', 'https://retty.me/area/PRE13/city/13201/'], ['立川市', 'https://retty.me/area/PRE13/city/13202/'], ['武蔵野市', 'https://retty.me/area/PRE13/city/13203/'], ['三鷹市', 'https://retty.me/area/PRE13/city/13204/'], ['青梅市', 'https://retty.me/area/PRE13/city/13205/'], ['東京都 府中市', 'https://retty.me/area/PRE13/city/13206/'], ['昭島市', 'https://retty.me/area/PRE13/city/13207/'], ['調布市', 'https://retty.me/area/PRE13/city/13208/'], ['町田市', 'https://retty.me/area/PRE13/city/13209/'], ['小金井市', 'https://retty.me/area/PRE13/city/13210/'], ['小平市', 'https://retty.me/area/PRE13/city/13211/'], ['日野市', 'https://retty.me/area/PRE13/city/13212/'], ['東村山市', 'https://retty.me/area/PRE13/city/13213/'], ['国分寺市', 'https://retty.me/area/PRE13/city/13214/'], ['国立市', 'https://retty.me/area/PRE13/city/13215/'], ['福生市', 'https://retty.me/area/PRE13/city/13218/'], ['狛江市', 'https://retty.me/area/PRE13/city/13219/'], ['東大和市', 'https://retty.me/area/PRE13/city/13220/'], ['清瀬市', 'https://retty.me/area/PRE13/city/13221/'], ['東久留米市', 'https://retty.me/area/PRE13/city/13222/'], ['武蔵村山市', 'https://retty.me/area/PRE13/city/13223/'], ['多摩市', 'https://retty.me/area/PRE13/city/13224/'], ['稲城市', 'https://retty.me/area/PRE13/city/13225/'], ['羽村市', 'https://retty.me/area/PRE13/city/13227/'], ['あきる野市', 'https://retty.me/area/PRE13/city/13228/'], ['西東京市', 'https://retty.me/area/PRE13/city/13229/'], ['西多摩郡瑞穂町', 'https://retty.me/area/PRE13/city/13303/'], ['西多摩郡日の出町', 'https://retty.me/area/PRE13/city/13305/'], ['西多摩郡檜原村', 'https://retty.me/area/PRE13/city/13307/'], ['西多摩郡奥多摩町', 'https://retty.me/area/PRE13/city/13308/'], ['大島町', 'https://retty.me/area/PRE13/city/13361/'], ['利島村', 'https://retty.me/area/PRE13/city/13362/'], ['新島村', 'https://retty.me/area/PRE13/city/13363/'], ['神津島村', 'https://retty.me/area/PRE13/city/13364/'], ['三宅島三宅村', 'https://retty.me/area/PRE13/city/13381/'], ['御蔵島村', 'https://retty.me/area/PRE13/city/13382/'], ['八丈島八丈町', 'https://retty.me/area/PRE13/city/13401/'], ['小笠原村', 'https://retty.me/area/PRE13/city/13421/']]


class retty_restraurant():

    channel = {}

    def __init__(self):
        for dt in data:
            self.channel[dt[0]] = dt[1]

    def getData(self,name):
        df = pandas.DataFrame()

        df2 = pandas.DataFrame()
        
        if self.channel.get(name):
            url = self.channel[name]
        else:
            print("存在しない市区町村")

        
        p2 = "page-2/"
        html = requests.get(url+p2)
        soup = BeautifulSoup(html.text.encode(html.encoding))
        elems = soup.find_all(href=re.compile(url+"page-[0-9]{1,6}/"))
        MAX = int(elems[-1].text)
        for i in range(MAX):
            goto = url + "page-" + str(i+1)+"/"
            html = requests.get(goto)
            soup = BeautifulSoup(html.text.encode(html.encoding))
            elems = soup.find_all(href=re.compile("https://retty.me/area/PRE13/ARE[0-9]{1,7}/SUB[0-9]{1,7}/[0-9]*/"))
            for link in elems:
                goto = link.get("href")
                print(goto)
                df,df2 = self.getRestaurantData(goto,df,df2,name)
                time.sleep(1)
            time.sleep(1)

        df.to_csv("R_restraurant_"+name+".csv")
        df2.to_csv("R_PRE"+name+".csv")

        print("--end--")

    def getRestaurantData(self,goto,df,df2,where):
        data = {}
        data2 = {}

        Ht = requests.get(goto)
        soup = BeautifulSoup(Ht.text.encode(Ht.encoding))

        elems_b = soup.find_all("ul",class_ = re.compile("restaurant-navigation-bar"))
        k_num = re.search(r"口コミ\([0-9]*\)",elems_b[0].text).group()[4:-1]
        #基本情報の取得
        composition = soup.find_all("dl",class_=re.compile("restaurant-info-table"))
        na = soup.find_all("span",class_=re.compile("restaurant-summary__display-name"))
        try:
            name = na[0].text.replace(" ","")
        except Exception:
            name = None
        try:
            group = composition[0].ul.text.replace("\n",",").replace(" ","")[1:]
        except Exception:
            group = None
        try:
            call = re.search("[0-9]*-[0-9]*-[0-9]*",composition[2].text).group()
        except Exception:
            call = -1

        position = soup.find_all("a",href=re.compile(goto+"map/"))


        data["店舗ID"] = re.findall(r'/[0-9]+/',goto)[0][1:-1]
        data["店舗名"] = name
        data["カテゴリー"] = group[:-1]
        data["電話番号"] = call
        data["URL"] = goto
        data["地区名小"] = where
        if len(position) >= 1:
            data["住所"] = position[1].text.replace(" ","")
        else:
            data["住所"] = None


        data2["店舗ID"] = re.findall(r'/[0-9]+/',goto)[0][1:-1]
        data2["URL"] = goto
        data2["number"] = k_num

        df = df.append(data, ignore_index=True)
        df2 = df2.append(data2, ignore_index=True)

        return df,df2






"""
if __name__ == "__main__":
    url = "https://retty.me/area/PRE13/city/"
    html = requests.get(url)
    soup = BeautifulSoup(html.text.encode(html.encoding))
    elems_b = soup.find_all("a",href = re.compile("https://retty.me/area/PRE13/city/[0-9]*/"))
    nn = []
    for data in elems_b:
        if data.text != "町域一覧":
            nn.append([data.text,data.get("href")])
    print(nn)
"""

if __name__ == "__main__":
    args = sys.argv
    if len(args) != 2:
        print("引数は東京の市区町村のみ")
        exit()
    else:
        RR = retty_restraurant()
        RR.getData(args[1])