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
import progressbar

data = [['千代田区', 'https://tabelog.com/tokyo/C13101/rstLst/'], ['中央区', 'https://tabelog.com/tokyo/C13102/rstLst/'], ['港区', 'https://tabelog.com/tokyo/C13103/rstLst/'], ['新宿区', 'https://tabelog.com/tokyo/C13104/rstLst/'], ['文京区', 'https://tabelog.com/tokyo/C13105/rstLst/'], ['台東区', 'https://tabelog.com/tokyo/C13106/rstLst/'], ['墨田区', 'https://tabelog.com/tokyo/C13107/rstLst/'], ['江東区', 'https://tabelog.com/tokyo/C13108/rstLst/'], ['品川区', 'https://tabelog.com/tokyo/C13109/rstLst/'], ['目黒区', 'https://tabelog.com/tokyo/C13110/rstLst/'], ['大田区', 'https://tabelog.com/tokyo/C13111/rstLst/'], ['世田谷区', 'https://tabelog.com/tokyo/C13112/rstLst/'], ['渋谷区', 'https://tabelog.com/tokyo/C13113/rstLst/'], ['中野区', 'https://tabelog.com/tokyo/C13114/rstLst/'], ['杉並区', 'https://tabelog.com/tokyo/C13115/rstLst/'], ['豊島区', 'https://tabelog.com/tokyo/C13116/rstLst/'], ['北区', 'https://tabelog.com/tokyo/C13117/rstLst/'], ['荒川区', 'https://tabelog.com/tokyo/C13118/rstLst/'], ['板橋区', 'https://tabelog.com/tokyo/C13119/rstLst/'], ['練馬区', 'https://tabelog.com/tokyo/C13120/rstLst/'], ['足立区', 'https://tabelog.com/tokyo/C13121/rstLst/'], ['葛飾区', 'https://tabelog.com/tokyo/C13122/rstLst/'], ['江戸川区', 'https://tabelog.com/tokyo/C13123/rstLst/'], ['八王子市', 'https://tabelog.com/tokyo/C13201/rstLst/'], ['立川市', 'https://tabelog.com/tokyo/C13202/rstLst/'], ['武蔵野市', 'https://tabelog.com/tokyo/C13203/rstLst/'], ['三鷹市', 'https://tabelog.com/tokyo/C13204/rstLst/'], ['青梅市', 'https://tabelog.com/tokyo/C13205/rstLst/'], ['府中市', 'https://tabelog.com/tokyo/C13206/rstLst/'], ['昭島市', 'https://tabelog.com/tokyo/C13207/rstLst/'], ['調布市', 'https://tabelog.com/tokyo/C13208/rstLst/'], ['町田市', 'https://tabelog.com/tokyo/C13209/rstLst/'], ['小金井市', 'https://tabelog.com/tokyo/C13210/rstLst/'], ['小平市', 'https://tabelog.com/tokyo/C13211/rstLst/'], ['日野市', 'https://tabelog.com/tokyo/C13212/rstLst/'], ['東村山市', 'https://tabelog.com/tokyo/C13213/rstLst/'], ['国分寺市', 'https://tabelog.com/tokyo/C13214/rstLst/'], ['国立市', 'https://tabelog.com/tokyo/C13215/rstLst/'], ['福生市', 'https://tabelog.com/tokyo/C13218/rstLst/'], ['狛江市', 'https://tabelog.com/tokyo/C13219/rstLst/'], ['東大和市', 'https://tabelog.com/tokyo/C13220/rstLst/'], ['多摩市', 'https://tabelog.com/tokyo/C13224/rstLst/'], ['清瀬市', 'https://tabelog.com/tokyo/C13221/rstLst/'], ['東久留米市', 'https://tabelog.com/tokyo/C13222/rstLst/'], ['武蔵村山市', 'https://tabelog.com/tokyo/C13223/rstLst/'], ['稲城市', 'https://tabelog.com/tokyo/C13225/rstLst/'], ['羽村市', 'https://tabelog.com/tokyo/C13227/rstLst/'], ['あきる野市', 'https://tabelog.com/tokyo/C13228/rstLst/'], ['西多摩郡日の出町', 'https://tabelog.com/tokyo/C13305/rstLst/'], ['西東京市', 'https://tabelog.com/tokyo/C13229/rstLst/'], ['西多摩郡奥多摩町', 'https://tabelog.com/tokyo/C13308/rstLst/'], ['西多摩郡瑞穂町', 'https://tabelog.com/tokyo/C13303/rstLst/'], ['西多摩郡檜原村', 'https://tabelog.com/tokyo/C13307/rstLst/'], ['大島町', 'https://tabelog.com/tokyo/C13361/rstLst/'], ['新島村', 'https://tabelog.com/tokyo/C13363/rstLst/'], ['三宅島三宅村', 'https://tabelog.com/tokyo/C13381/rstLst/'], ['八丈島八丈町', 'https://tabelog.com/tokyo/C13401/rstLst/'], ['小笠原村', 'https://tabelog.com/tokyo/C13421/rstLst/']]
score = ["料理・味","サービス","雰囲気","CP","酒・ドリンク"]

class tabeLog_comment():

    channel = {}
    score = ["料理・味","サービス","雰囲気","CP","酒・ドリンク"]

    def __init__(self):

        for dt in data:
            self.channel[dt[0]] = dt[1]

    def getOneComment(self,url):
        try:
            Ht = requests.get(url)
            soup = BeautifulSoup(Ht.content, 'lxml')
            comment = soup.find_all("div",class_=re.compile("rvw-item__rvw-comment"))[0]
            for br in soup.find_all('br'):
                br.replace_with('\n')

            return comment.text
        except Exception:
            return "Error:Nothing"


    def getComment(self,name):

        if self.channel.get(name):
            url = self.channel[name]
        else:
            print("存在しない市区町村")

        csv_path = "T_PRE"+name+".csv"

        if not os.path.exists(csv_path):
            print("まだ作成されていない")

        bar_sum = 0
        bar_val = 0

        with open(csv_path) as f:
            reader = csv.reader(f)
            for row in reader:
                if row[0] == "":
                    continue
                bar_sum += int(row[2])

        bar = progressbar.ProgressBar(max_value=bar_sum)
        bar.update(bar_val)

        with open(csv_path) as f:
            reader = csv.reader(f)
            flag = True
            for row in reader:
                data = {}
                df = pandas.DataFrame()
                if row[0] == "":
                    continue
                data["店舗ID"] = row[3]
                size = row[2]
                for i in range(-(-int(size)//20)):
                    Ht = requests.get(row[1] + "dtlrvwlst/COND-0/smp1/?smp=1&lc=0&rvw_part=all&PG=" + str(i+1) + "/")
                    soup = BeautifulSoup(Ht.content, 'lxml')

                    elems_n = soup.find_all("div",class_=re.compile("rvw-item js-rvw-item-clickable-area"))

                    for link in elems_n:
                        all_score = link.find_all("b",class_=re.compile("c-rating__val c-rating__val--strong"))
                        try:
                            data["評価"] = all_score[0].text
                        except Exception:
                            data["評価"] = "-1"
                        userId = link.find_all("a",target=re.compile("_blank"))[0]
                        try:
                            data["投稿ID"] = userId.get("href")[6:-1]
                        except Exception:
                            data["投稿ID"] = "-1"
                        tourl = "https://tabelog.com"+link.get("data-detail-url")
                        data["URL"] = tourl
                        data["コメント"] = self.getOneComment(tourl)
                        kkk = link.find_all("strong",class_=re.compile("rvw-item__ratings-dtlscore-score"))
                        for i in range(len(self.score)):
                            try:
                                data[self.score[i]] = kkk[i].text.strip().replace("\n","")
                            except Exception:
                                data[self.score[i]] = "-1"

                        data["ID"] = int(bar_val)

                        df = df.append(copy.deepcopy(data), ignore_index=True)

                        bar_val += 1
                        bar.update(bar_val)

                        time.sleep(1)
                    time.sleep(1)
                try:
                    df = df.set_index('ID')
                except Exception:
                    continue
                if flag:
                    df.to_csv("T_comment_"+name+".csv")
                    flag = False
                else:
                    df.to_csv("T_comment_"+name+".csv", mode='a', header=False)
                time.sleep(1)
        bar.finish()
        #print("--end--")



if __name__ == "__main__":
    args = sys.argv
    if len(args) != 2:
        print("引数は東京の市区町村のみ")
        exit()
    else:
        TR = tabeLog_comment()
        TR.getComment(args[1])
