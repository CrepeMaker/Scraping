import requests
import pandas
from bs4 import BeautifulSoup
import re
import time
import ast
import json
import copy

from pprint import pprint



"""
How to


基本的にはgetData()を用いてcsvを作成する

引数は"都道府県名(str)","とこから(int)","とこまで(int)","csv名/None(追記する時、ないときはNone)"


"""

class rettyScriping():

	pre = ['北海道', '青森', '岩手', '宮城', '秋田', '山形', '福島', '茨城', '栃木', '群馬', '埼玉', '千葉', '東京', '神奈川', '富山', '石川', '福井', '山梨', '長野', '岐阜', '静岡', '愛知', '三重', '滋賀', '京都', '大阪', '兵庫', '奈良', '和歌山', '鳥取', '島根', '岡山', '広島', '山口', '徳島', '香川', '愛媛', '高知', '福岡', '佐賀', '長崎', '熊本', '大分', '宮崎', '鹿児島', '沖縄']

	ch = {}

	for i in range(len(pre)):
	    if i <= 8:
	        ch[pre[i]] = str(0)+str(i+1)
	    else:
	        ch[pre[i]] = str(i+1)


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
	        num = ch[where]
	    except Exception:
	        print("input error")
	        exit()
	    url = "https://retty.me/area/PRE"+num+"/"
	    p2 = "page-2/"
	    html = requests.get(url+p2)
	    soup = BeautifulSoup(html.text.encode(html.encoding))
	    elems = soup.find_all(href=re.compile(url+"page-[0-9]{1,6}/"))
	    ma = int(elems[-1].text)

	    mi = max(0,Min)
	    ma = min(ma,max(Max,0))
	    count = 0
	    for i in range(mi,ma):
	        count += 1
	        goto = link.get("href")
	        df = getRestaurantData(goto,df)
	    
	    
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
	    kutikomi = re.search(r"口コミ\([0-9]*\)",elems_b[0].text).group()[4:-1]
	    
	    #基本情報の取得
	    compo = soup.find_all("dl",class_=re.compile("restaurant-info-table"))
	    na = soup.find_all("span",class_=re.compile("restaurant-summary__display-name"))
	    try:
	        name = na[0].text.replace(" ","")
	    except Exception:
	        name = None
	    try:
	        grp = compo[0].ul.text.replace("\n",",").replace(" ","")[1:]
	    except Exception:
	        grp = None
	    try:
	        call = re.search("[0-9]*-[0-9]*-[0-9]*",compo[2].text).group()
	    except Exception:
	        call = -1
	    Url = goto + "reports/"
	    data["name"] = name
	    data["grp"] = grp
	    data["call"] = call
	    data["url"] = Url
	    df = getComment(goto,cnum,data,df)
	    return df

	def getComment(self,goto,size,data,df):
	    for i in range(-(-int(size)//20)):
	        Ht = requests.get(goto + "reports/" + "page-" + str(i+1) + "/")
	        soup = BeautifulSoup(Ht.text.encode(Ht.encoding), 'html.parser')
	        elems_n = soup.find_all("ul",class_=re.compile("restaurant-detail__report-list js-report-list"))
	        print(goto + "reports/"+ "page-" + str(kk+1) + "/")
	        
	        #コメントのリストであるjsonを取得
	        try:
	            st = re.search("\[.*\]",elems_n[0]["v-bind"]).group()
	        except Exception:
	            break
	        end = st.replace("[","").replace("]","")
	        En = end.split(",{")
	        
	        #リストの中を探索
	        for kkk in En:
	            if kkk[0] != "{":
	                kkk = "{" + kkk
	            kkk = kkk.replace("'","\"")
	            kkk = re.sub("\"tagIds\".*,\"scoreTypeString\"","\"scoreTypeString\"",kkk)
	            try:
	                kkk = json.loads(kkk)
	                userId = kkk['userId']
	                comment = kkk["comment"]
	                restaurantId = kkk['restaurantId']
	                if kkk["scoreTypeString"] == "excellent":
	                    lank = 3
	                elif kkk["scoreTypeString"] == "good":
	                    lank = 2
	                else:
	                    lank = 1
	                data["userId"] = userId
	                data["comment"] = comment
	                data["restaurantId"] = restaurantId
	                data["lank"] = lank
	            except Exception:
	                continue
	            df = df.append(copy.deepcopy(data), ignore_index=True)
	        time.sleep(1)
	    return df


