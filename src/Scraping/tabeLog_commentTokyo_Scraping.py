import requests
import pandas
from bs4 import BeautifulSoup
import re
import time
import ast
import json
import copy
import sys
import os
import csv

from pprint import pprint

data = [['千代田区', 'https://tabelog.com/tokyo/C13101/rstLst/'], ['中央区', 'https://tabelog.com/tokyo/C13102/rstLst/'], ['港区', 'https://tabelog.com/tokyo/C13103/rstLst/'], ['新宿区', 'https://tabelog.com/tokyo/C13104/rstLst/'], ['文京区', 'https://tabelog.com/tokyo/C13105/rstLst/'], ['台東区', 'https://tabelog.com/tokyo/C13106/rstLst/'], ['墨田区', 'https://tabelog.com/tokyo/C13107/rstLst/'], ['江東区', 'https://tabelog.com/tokyo/C13108/rstLst/'], ['品川区', 'https://tabelog.com/tokyo/C13109/rstLst/'], ['目黒区', 'https://tabelog.com/tokyo/C13110/rstLst/'], ['大田区', 'https://tabelog.com/tokyo/C13111/rstLst/'], ['世田谷区', 'https://tabelog.com/tokyo/C13112/rstLst/'], ['渋谷区', 'https://tabelog.com/tokyo/C13113/rstLst/'], ['中野区', 'https://tabelog.com/tokyo/C13114/rstLst/'], ['杉並区', 'https://tabelog.com/tokyo/C13115/rstLst/'], ['豊島区', 'https://tabelog.com/tokyo/C13116/rstLst/'], ['北区', 'https://tabelog.com/tokyo/C13117/rstLst/'], ['荒川区', 'https://tabelog.com/tokyo/C13118/rstLst/'], ['板橋区', 'https://tabelog.com/tokyo/C13119/rstLst/'], ['練馬区', 'https://tabelog.com/tokyo/C13120/rstLst/'], ['足立区', 'https://tabelog.com/tokyo/C13121/rstLst/'], ['葛飾区', 'https://tabelog.com/tokyo/C13122/rstLst/'], ['江戸川区', 'https://tabelog.com/tokyo/C13123/rstLst/'], ['八王子市', 'https://tabelog.com/tokyo/C13201/rstLst/'], ['立川市', 'https://tabelog.com/tokyo/C13202/rstLst/'], ['武蔵野市', 'https://tabelog.com/tokyo/C13203/rstLst/'], ['三鷹市', 'https://tabelog.com/tokyo/C13204/rstLst/'], ['青梅市', 'https://tabelog.com/tokyo/C13205/rstLst/'], ['府中市', 'https://tabelog.com/tokyo/C13206/rstLst/'], ['昭島市', 'https://tabelog.com/tokyo/C13207/rstLst/'], ['調布市', 'https://tabelog.com/tokyo/C13208/rstLst/'], ['町田市', 'https://tabelog.com/tokyo/C13209/rstLst/'], ['小金井市', 'https://tabelog.com/tokyo/C13210/rstLst/'], ['小平市', 'https://tabelog.com/tokyo/C13211/rstLst/'], ['日野市', 'https://tabelog.com/tokyo/C13212/rstLst/'], ['東村山市', 'https://tabelog.com/tokyo/C13213/rstLst/'], ['国分寺市', 'https://tabelog.com/tokyo/C13214/rstLst/'], ['国立市', 'https://tabelog.com/tokyo/C13215/rstLst/'], ['福生市', 'https://tabelog.com/tokyo/C13218/rstLst/'], ['狛江市', 'https://tabelog.com/tokyo/C13219/rstLst/'], ['東大和市', 'https://tabelog.com/tokyo/C13220/rstLst/'], ['多摩市', 'https://tabelog.com/tokyo/C13224/rstLst/'], ['清瀬市', 'https://tabelog.com/tokyo/C13221/rstLst/'], ['東久留米市', 'https://tabelog.com/tokyo/C13222/rstLst/'], ['武蔵村山市', 'https://tabelog.com/tokyo/C13223/rstLst/'], ['稲城市', 'https://tabelog.com/tokyo/C13225/rstLst/'], ['羽村市', 'https://tabelog.com/tokyo/C13227/rstLst/'], ['あきる野市', 'https://tabelog.com/tokyo/C13228/rstLst/'], ['西多摩郡日の出町', 'https://tabelog.com/tokyo/C13305/rstLst/'], ['西東京市', 'https://tabelog.com/tokyo/C13229/rstLst/'], ['西多摩郡奥多摩町', 'https://tabelog.com/tokyo/C13308/rstLst/'], ['西多摩郡瑞穂町', 'https://tabelog.com/tokyo/C13303/rstLst/'], ['西多摩郡檜原村', 'https://tabelog.com/tokyo/C13307/rstLst/'], ['大島町', 'https://tabelog.com/tokyo/C13361/rstLst/'], ['新島村', 'https://tabelog.com/tokyo/C13363/rstLst/'], ['三宅島三宅村', 'https://tabelog.com/tokyo/C13381/rstLst/'], ['八丈島八丈町', 'https://tabelog.com/tokyo/C13401/rstLst/'], ['小笠原村', 'https://tabelog.com/tokyo/C13421/rstLst/']]
score = ["料理・味","サービス","雰囲気","CP","酒・ドリンク"]

class tabeLog_comment():

    channel = {}
    score = ["料理・味","サービス","雰囲気","CP","酒・ドリンク"]

    def __init__(self):

        for dt in data:
            self.channel[dt[0]] = dt[1]

    
    def getComment(self,name):

        df = pandas.DataFrame()

        if self.channel.get(name):
            url = self.channel[name]
        else:
            print("存在しない市区町村")
        
        if not os.path.exists("T_PRE"+name+".csv"):
            print("まだ作成されていない")

        with open("T_PRE"+name+".csv") as f:
            reader = csv.reader(f)
            for row in reader:
                data = {}
                if row[0] == "":
                    continue
                data["店舗ID"] = row[0]
                size = row[2]
                for i in range(-(-int(size)//20)):
                    Ht = requests.get(row[1] + "dtlrvwlst/COND-0/smp1/?smp=1&lc=0&rvw_part=all&PG=" + str(i+1) + "/")
                    data["URL"] = row[1] + "dtlrvwlst/COND-0/smp1/?smp=1&lc=0&rvw_part=all&PG=" + str(i+1) + "/"
                    soup = BeautifulSoup(Ht.text.encode(Ht.encoding), 'html.parser')
                    elems_n = soup.find_all("div",class_=re.compile("rvw-item js-rvw-item-clickable-area"))
                    for link in elems_n:
                        all_score = link.find_all("b",class_=re.compile("c-rating__val c-rating__val--strong"))
                        data["評価"] = all_score[0].text
                        userId = link.find_all("a",target=re.compile("_blank"))[0]
                        print(userId.get("href"))
                        data["投稿ID"] = userId.get("href")[6:-1]
                        comment = link.find_all("div",class_=re.compile("rvw-item__rvw-comment"))
                        data["コメント"] = comment[0].text
                        kkk = link.find_all("strong",class_=re.compile("rvw-item__ratings-dtlscore-score"))
                        for i in range(len(self.score)):
                            data[self.score[i]] = kkk[i].text.strip().replace("\n","")
                        df = df.append(copy.deepcopy(data), ignore_index=True)
                    time.sleep(1)
        df.to_csv("T_comment_"+name+".csv")
        print("--end--")



if __name__ == "__main__":
    args = sys.argv
    if len(args) != 2:
        print("引数は東京の市区町村のみ")
        exit()
    else:
        TR = tabeLog_comment()
        TR.getComment(args[1])
