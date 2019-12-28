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

data = [['千代田区', 'https://tabelog.com/tokyo/C13101/rstLst/'], ['中央区', 'https://tabelog.com/tokyo/C13102/rstLst/'], ['港区', 'https://tabelog.com/tokyo/C13103/rstLst/'], ['新宿区', 'https://tabelog.com/tokyo/C13104/rstLst/'], ['文京区', 'https://tabelog.com/tokyo/C13105/rstLst/'], ['台東区', 'https://tabelog.com/tokyo/C13106/rstLst/'], ['墨田区', 'https://tabelog.com/tokyo/C13107/rstLst/'], ['江東区', 'https://tabelog.com/tokyo/C13108/rstLst/'], ['品川区', 'https://tabelog.com/tokyo/C13109/rstLst/'], ['目黒区', 'https://tabelog.com/tokyo/C13110/rstLst/'], ['大田区', 'https://tabelog.com/tokyo/C13111/rstLst/'], ['世田谷区', 'https://tabelog.com/tokyo/C13112/rstLst/'], ['渋谷区', 'https://tabelog.com/tokyo/C13113/rstLst/'], ['中野区', 'https://tabelog.com/tokyo/C13114/rstLst/'], ['杉並区', 'https://tabelog.com/tokyo/C13115/rstLst/'], ['豊島区', 'https://tabelog.com/tokyo/C13116/rstLst/'], ['北区', 'https://tabelog.com/tokyo/C13117/rstLst/'], ['荒川区', 'https://tabelog.com/tokyo/C13118/rstLst/'], ['板橋区', 'https://tabelog.com/tokyo/C13119/rstLst/'], ['練馬区', 'https://tabelog.com/tokyo/C13120/rstLst/'], ['足立区', 'https://tabelog.com/tokyo/C13121/rstLst/'], ['葛飾区', 'https://tabelog.com/tokyo/C13122/rstLst/'], ['江戸川区', 'https://tabelog.com/tokyo/C13123/rstLst/'], ['八王子市', 'https://tabelog.com/tokyo/C13201/rstLst/'], ['立川市', 'https://tabelog.com/tokyo/C13202/rstLst/'], ['武蔵野市', 'https://tabelog.com/tokyo/C13203/rstLst/'], ['三鷹市', 'https://tabelog.com/tokyo/C13204/rstLst/'], ['青梅市', 'https://tabelog.com/tokyo/C13205/rstLst/'], ['府中市', 'https://tabelog.com/tokyo/C13206/rstLst/'], ['昭島市', 'https://tabelog.com/tokyo/C13207/rstLst/'], ['調布市', 'https://tabelog.com/tokyo/C13208/rstLst/'], ['町田市', 'https://tabelog.com/tokyo/C13209/rstLst/'], ['小金井市', 'https://tabelog.com/tokyo/C13210/rstLst/'], ['小平市', 'https://tabelog.com/tokyo/C13211/rstLst/'], ['日野市', 'https://tabelog.com/tokyo/C13212/rstLst/'], ['東村山市', 'https://tabelog.com/tokyo/C13213/rstLst/'], ['国分寺市', 'https://tabelog.com/tokyo/C13214/rstLst/'], ['国立市', 'https://tabelog.com/tokyo/C13215/rstLst/'], ['福生市', 'https://tabelog.com/tokyo/C13218/rstLst/'], ['狛江市', 'https://tabelog.com/tokyo/C13219/rstLst/'], ['東大和市', 'https://tabelog.com/tokyo/C13220/rstLst/'], ['多摩市', 'https://tabelog.com/tokyo/C13224/rstLst/'], ['清瀬市', 'https://tabelog.com/tokyo/C13221/rstLst/'], ['東久留米市', 'https://tabelog.com/tokyo/C13222/rstLst/'], ['武蔵村山市', 'https://tabelog.com/tokyo/C13223/rstLst/'], ['稲城市', 'https://tabelog.com/tokyo/C13225/rstLst/'], ['羽村市', 'https://tabelog.com/tokyo/C13227/rstLst/'], ['あきる野市', 'https://tabelog.com/tokyo/C13228/rstLst/'], ['西多摩郡日の出町', 'https://tabelog.com/tokyo/C13305/rstLst/'], ['西東京市', 'https://tabelog.com/tokyo/C13229/rstLst/'], ['西多摩郡奥多摩町', 'https://tabelog.com/tokyo/C13308/rstLst/'], ['西多摩郡瑞穂町', 'https://tabelog.com/tokyo/C13303/rstLst/'], ['西多摩郡檜原村', 'https://tabelog.com/tokyo/C13307/rstLst/'], ['大島町', 'https://tabelog.com/tokyo/C13361/rstLst/'], ['新島村', 'https://tabelog.com/tokyo/C13363/rstLst/'], ['三宅島三宅村', 'https://tabelog.com/tokyo/C13381/rstLst/'], ['八丈島八丈町', 'https://tabelog.com/tokyo/C13401/rstLst/'], ['小笠原村', 'https://tabelog.com/tokyo/C13421/rstLst/']]
score = ["料理・味","サービス","雰囲気","CP","酒・ドリンク"]

class tabeLog_restraurant():
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

        html = requests.get(url)
        soup = BeautifulSoup(html.text.encode(html.encoding), features="lxml")

        elemm = soup.find_all("a",class_=re.compile("c-link-arrow"))
        for ii in range(len(elemm)):
            url = elemm[ii].get("href")
            print(url)
            html = requests.get(url)
            soup = BeautifulSoup(html.text.encode(html.encoding), features="lxml")
            elems = soup.find_all("span",class_=re.compile("c-page-count__num"))
            MAX = int(elems[2].text)
            for i in range(-(-MAX//20)):
                num = i + 1
                print("---{0} / {1}---".format(i+1,-(-MAX//20)))
                html = requests.get(url+str(num)+"/")
                soup = BeautifulSoup(html.text.encode(html.encoding), features="lxml")
                elems = soup.find_all(class_=re.compile("list-rst__rst-name-target cpy-rst-name"))
                for link in elems:
                    gt = link.get("href")
                    print(gt)
                    df,df2 = self.getRestaurantData(gt,df,df2,name)
                    time.sleep(1)
                break
                time.sleep(1)
            break
            time.sleep(1)


        df.to_csv("T_restraurant_"+name+".csv")
        df2.to_csv("T_PRE"+name+".csv")
        print("--end--")

    def getRestaurantData(self,goto,df,df2,where):
        data = {}
        data2 = {}

        Ht = requests.get(goto)
        soup = BeautifulSoup(Ht.text.encode(Ht.encoding), features="lxml")

        review_link = soup.find(id="rdnavi-review")
        review_link_badge = review_link.find(class_ = re.compile("rstdtl-navi__total-count"))

        adl = soup.find_all("p",class_ = re.compile("rstinfo-table__address"))

        if review_link_badge:
            k_num = review_link_badge.text
        else:
            k_num = 0

        composition = soup.find_all("table",class_=re.compile("c-table c-table--form rstinfo-table__table"))
        na = soup.find_all("h2",class_=re.compile("display-name"))
        try:
            name = na[0].text.replace(" ","").replace("\n","")
        except Exception:
            name = None
        try:
            group = composition[0].find_all("td")[1].text
        except Exception:
            grp = None
        try:
            call = soup.find_all("strong",class_=re.compile("rstinfo-table__tel-num"))[0].text
        except Exception:
            call = -1

        try:
            strings = ""
            for i in range(len(adl)):
                strings += adl[i].text
        except Exception:
            strings = None

        data["店舗ID"] = re.findall(r'/[0-9]+/',goto)[0][1:-1]
        data["店舗名"] = name
        data["カテゴリー"] = group.replace("\n","")
        data["電話番号"] = call
        data["URL"] = goto
        data["地区名小"] = where
        data["住所"] = strings

        data2["店舗ID"] = re.findall(r'/[0-9]+/',goto)[0][1:-1]
        data2["URL"] = goto
        data2["number"] = k_num

        df = df.append(data, ignore_index=True)
        df2 = df2.append(data2, ignore_index=True)

        #print(len((df,df2)))
        return df,df2



"""
if __name__ == "__main__":
    url = "https://tabelog.com/tokyo/"
    html = requests.get(url)
    soup = BeautifulSoup(html.text.encode(html.encoding))
    elems_b = soup.find_all("a",href = re.compile("https://tabelog.com/tokyo/C[0-9]*/rstLst/"))
    nn = []
    for data in elems_b:
        nn.append([data.text,data.get("href")])
    print(nn)
"""

if __name__ == "__main__":
    args = sys.argv
    if len(args) != 2:
        print("引数は東京の市区町村のみ")
        exit()
    else:
        TR = tabeLog_restraurant()
        TR.getData(args[1])
