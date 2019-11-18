#coding:utf-8
import requests
import pandas
from bs4 import BeautifulSoup
import re
import time
import ast
import json
import copy

from pprint import pprint



class tabeLogScraping():
    
    channel = {'北海道': 'hokkaido', '青森': 'aomori', '岩手': 'iwate', '宮城': 'miyagi', '秋田': 'akita', '山形': 'yamagata', '福島': 'fukushima', '茨城': 'ibaraki', '栃木': 'tochigi', '群馬': 'gunma', '埼玉': 'saitama', '千葉': 'chiba', '東京': 'tokyo', '神奈川': 'kanagawa', '新潟': 'niigata', '富山': 'toyama', '石川': 'ishikawa', '福井': 'fukui', '山梨': 'yamanashi', '長野': 'nagano', '岐阜': 'gifu', '静岡': 'shizuoka', '愛知': 'aichi', '三重': 'mie', '滋賀': 'shiga', '京都': 'kyoto', '大阪': 'osaka', '兵庫': 'hyogo', '奈良': 'nara', '和歌山': 'wakayama', '鳥取': 'tottori', '島根': 'shimane', '岡山': 'okayama', '広島': 'hiroshima', '山口': 'yamaguchi', '徳島': 'tokushima', '香川': 'kagawa', '愛媛': 'ehime', '高知': 'kochi', '福岡': 'fukuoka', '佐賀': 'saga', '長崎': 'nagasaki', '熊本': 'kumamoto', '大分': 'oita', '宮崎': 'miyazaki', '鹿児島': 'kagoshima', '沖縄': 'okinawa'}
    score = ["料理・味","サービス","雰囲気","CP","酒・ドリンク"]
    """
    def __init__(self):
        url = "https://tabelog.com/rstLst/"
        html = requests.get(url)
        soup = BeautifulSoup(html.text.encode(html.encoding))
        elems = soup.find_all("a",class_=re.compile("list-balloon__recommend-target"))
        for i in range(47):
            self.channel[elems[i].text.replace(" ","").replace('\n',"")] =  elems[i].get("href")[20:-1]
        print(self.channel)
    """


    def getData(self,where,Min,Max,csv):
        df = pandas.DataFrame()
        
        if csv == None:
            flag = False
        else:
            flag = True
        
        if Min > Max:
            print("Min > Max")
            exit()
        try:    
            word = self.channel[where]
        except Exception:
            print("input error")
            exit()
        
        url = "https://tabelog.com/sitemap/"+word+"/"
        html = requests.get(url)
        soup = BeautifulSoup(html.text.encode(html.encoding))
        elems = soup.find_all(href=re.compile(url+"A[0-9]{1,10}-A[0-9]{1,10}/"))
        MAX = int(len(elems))
        print(MAX)
        MIN = max(0,Min)
        MAX = min(MAX,max(Max,0))
        
        for i in range(MIN,MAX):
            goto = elems[i].get("href")
            print(goto)
            html = requests.get(goto)
            soup = BeautifulSoup(html.text.encode(html.encoding))
            elems = soup.find_all("a",href=re.compile(goto+"[a-z]*/"))
            for link in elems:
                gt = link.get("href")
                print(gt)
                html = requests.get(gt)
                soup = BeautifulSoup(html.text.encode(html.encoding))
                el = soup.find_all("a",href=re.compile("/"+word+"/A[0-9]*/A[0-9]*/[0-9]*/"))
                #print(soup)
                for shop in el:
                    gt = "https://tabelog.com" + shop.get("href")
                    print(gt)
                    df = self.getRestaurantData(gt,shop.get("href"),df)
                    time.sleep(1)
                time.sleep(1)

            time.sleep(1)

        if flag:
            df.to_csv(csv, mode='a', header=False)
        else:
            df.to_csv("AREA"+word+".csv")
        print("--end--")
        


    def getRestaurantData(self,goto,name,df):
        data = {}
        data["restaurantId"] = name
        Ht = requests.get(goto)
        soup = BeautifulSoup(Ht.text.encode(Ht.encoding))
        elems_b = soup.find_all("span",class_ = re.compile("rstdtl-navi__total-count"))
        try:
            k_num = elems_b[0].text
        except Exception:
            return df
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
        Url = goto + "reports/"
        data["name"] = name
        data["category"] = group.replace("\n","")
        data["phone"] = call
        data["url"] = Url
        df = self.getComment(goto+"dtlrvwlst",k_num,data,df)
        return df

    def getComment(self,goto,size,data,df):
        for i in range(-(-int(size)//20)):
            Ht = requests.get(goto + "/COND-0/smp1/?smp=1&lc=0&rvw_part=all&PG=" + str(i+1) + "/")
            soup = BeautifulSoup(Ht.text.encode(Ht.encoding), 'html.parser')
            elems_n = soup.find_all("div",class_=re.compile("rvw-item js-rvw-item-clickable-area"))
            
            for link in elems_n:
                all_score = link.find_all("b",class_=re.compile("c-rating__val c-rating__val--strong"))
                data["score"] = all_score[0].text
                userId = link.find_all("a",target=re.compile("_blank"))[0]

                data["userId"] = userId.get("href")[6:-1]
                comment = link.find_all("div",class_=re.compile("rvw-item__rvw-comment"))
                data["comment"] = comment[0].text
                kkk = link.find_all("strong",class_=re.compile("rvw-item__ratings-dtlscore-score"))
                for i in range(len(kkk)):
                    data[self.score[i]] = kkk[i].text.strip().replace("\n","")
                df = df.append(copy.deepcopy(data), ignore_index=True)
            time.sleep(1)
        return df

