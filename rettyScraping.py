import requests
import pandas
from bs4 import BeautifulSoup
import re
import time
import ast
import json
import copy

from pprint import pprint



class rettyScraping():
    
    channel = {}
    
    def __init__(self):
        pre = ['北海道', '青森', '岩手', '宮城', '秋田', '山形', '福島', '茨城', '栃木', '群馬', '埼玉', '千葉', '東京', '神奈川', '富山', '石川', '福井', '山梨', '長野', '岐阜', '静岡', '愛知', '三重', '滋賀', '京都', '大阪', '兵庫', '奈良', '和歌山', '鳥取', '島根', '岡山', '広島', '山口', '徳島', '香川', '愛媛', '高知', '福岡', '佐賀', '長崎', '熊本', '大分', '宮崎', '鹿児島', '沖縄']
        for i in range(len(pre)):
            if i <= 8:
                self.channel[pre[i]] = str(0)+str(i+1)
            else:
                self.channel[pre[i]] = str(i+1)


    def getData(self,where,Min,Max,csv):
        df = pandas.DataFrame()
        
        if csv == None:
            flag = False
        else:
            flag = True
        
        if Min > Max:
            print("Min > Max")
            exit()
        print(self.channel)
        try:    
            num = self.channel[where]
        except Exception:
            print("input error")
            exit()
        
        url = "https://retty.me/area/PRE"+num+"/"
        p2 = "page-2/"
        html = requests.get(url+p2)
        soup = BeautifulSoup(html.text.encode(html.encoding))
        elems = soup.find_all(href=re.compile(url+"page-[0-9]{1,6}/"))
        MAX = int(elems[-1].text)
        print(MAX)
        MIN = max(0,Min)
        MAX = min(MAX,max(Max,0))
        for i in range(MIN,MAX):
            goto = url + "page-" + str(i+1)+"/"
            html = requests.get(goto)
            soup = BeautifulSoup(html.text.encode(html.encoding))
            elems = soup.find_all(href=re.compile(url+"ARE[0-9]{1,7}/SUB[0-9]{1,7}/[0-9]*/"))
            for link in elems:
                goto = link.get("href")
                df = self.getRestaurantData(goto,df)
                time.sleep(1)
            time.sleep(1)
        
        if flag:
            df.to_csv(csv, mode='a', header=False)
        else:
            df.to_csv("PRE"+num+".csv")
        


    def getRestaurantData(self,goto,df):
        data = {}

        Ht = requests.get(goto)
        soup = BeautifulSoup(Ht.text.encode(Ht.encoding))

        #口コミ数
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
            group = compo[0].ul.text.replace("\n",",").replace(" ","")[1:]
        except Exception:
            grp = None
        try:
            call = re.search("[0-9]*-[0-9]*-[0-9]*",compo[2].text).group()
        except Exception:
            call = -1
        Url = goto + "reports/"
        data["name"] = name
        data["category"] = grp
        data["phone"] = call
        data["url"] = Url
        df = self.getComment(goto,k_num,data,df)
        return df

    def getComment(self,goto,size,data,df):
        for i in range(-(-int(size)//20)):
            Ht = requests.get(goto + "reports/" + "page-" + str(i+1) + "/")
            soup = BeautifulSoup(Ht.text.encode(Ht.encoding), 'html.parser')
            elems_n = soup.find_all("ul",class_=re.compile("restaurant-detail__report-list js-report-list"))
            print(goto + "reports/"+ "page-" + str(i+1) + "/")
            
            #コメントのリストであるjsonを取得
            try:
                st = re.search("\[.*\]",elems_n[0]["v-bind"]).group()
            except Exception:
                break

            En = st.replace("[","").replace("]","").split(",{")
            
            #リストの中を探索
            for dictionary in En:
                if dictionary[0] != "{":
                    dictionary = "{" + dictionary
                dictionary = dictionary.replace("'","\"")
                dictionary = re.sub("\"tagIds\".*,\"scoreTypeString\"","\"scoreTypeString\"",dictionary)
                try:
                    dictionary = json.loads(dictionary)
                    userId = dictionary['userId']
                    comment = dictionary["comment"]
                    restaurantId = dictionary['restaurantId']
                    if dictionary["scoreTypeString"] == "excellent":
                        rank = 3
                    elif dictionary["scoreTypeString"] == "good":
                        rank = 2
                    else:
                        rank = 1
                    data["userId"] = userId
                    data["comment"] = comment
                    data["restaurantId"] = restaurantId
                    data["score"] = rank
                except Exception:
                    continue
                df = df.append(copy.deepcopy(data), ignore_index=True)
            time.sleep(1)
        return df



